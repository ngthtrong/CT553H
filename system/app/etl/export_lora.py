#!/usr/bin/env python3
"""Export the LoRA-D serving bundle (plan 2.12, WP10) from the branch-1 artifacts of campaign aa4fc2b7ce29abf9.

Run with the optional environment that has PyTorch, Transformers, scikit-learn and pandas (`make lora-bundle`, which
uses system/app/.venv-lora). Inputs are read-only:

* research/kaggle-roadmap-2026-10-31/output/local/aa4fc2b7ce29abf9/jobs/model-card-parity/model-card.json and the
  files it pins (three refit `model.pt`, the final calibrator), each checked against its SHA-256;
* the pinned ESM-2 35M snapshot of the research runtime (output/weights/esm2_35m, per-file SHA-256 from status.json);
* data/processed/v3-fullpsi (identity b0376e05...) for the cross-runtime parity rows.

Output, outside git (data/ is ignored), recorded in data/README.md:

    data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1.json      manifest = registered weights file of the model row
    data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1/          adapters (.npz), calibrator (.npz), base/, fixture

No pickle is written: torch/joblib objects are converted to plain float32/float64 arrays in deterministic .npz files
(fixed zip timestamps), so the manifest hash is reproducible. The script also

1. reruns the research implementation (degron_v3.finetune.MutationRegressor) on the CPU for the 32 W rows that the
   CUDA parity job scored, and reports the CUDA -> CPU difference (model card: cross_runtime_parity pending);
2. scores two full tiles (532 substitutions each) with the research implementation and stores them as the parity
   fixture that backend tests compare with the independent serving implementation (degron_footprint.lora);
3. runs the serving implementation on the same tiles and reports the difference.

The report goes to system/app/tests/results/lora-bundle.json. Nothing here promotes the model to serving: the bundle is
registered as a non-default frozen model; `serving_promotion` stays `not_authorized_by_research_execution`.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import shutil
import sys
import time
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
APP = HERE.parent
ROOT = next(p for p in APP.parents if (p / 'CLAUDE.md').is_file())
V3 = ROOT / 'research/kaggle-roadmap-2026-10-31'
CAMPAIGN = V3 / 'output/local/aa4fc2b7ce29abf9'
CARD = CAMPAIGN / 'jobs/model-card-parity/model-card.json'
RESULTS = ROOT / 'research/lora-refit-transfer-2026-11-16/results.json'
DATA_V3 = ROOT / 'data/processed/v3-fullpsi'
DATA_IDENTITY = 'b0376e05d690d991c95143d6122b5418e457318394da032928d0d1e53f914738'
OUT = ROOT / 'data/processed/lora-d-serving-v1'
NAME = 'esm2-35m-lora-d-v1'
MODEL_ID = 'esm2-35m-lora-d-aa4fc2b7'
REPORT = APP / 'tests/results/lora-bundle.json'
FEATURES = ['cell_id', 'peptide_id', 'group_id', 'wt_sequence', 'mutant_sequence', 'position_1based', 'wt_aa', 'mut_aa']
# Second fixture tile: the typed sequence of the real-backend e2e test. It turned out to be a W peptide as well (checked
# 17 Nov 2026 against training-sequences.txt); the fixture is about implementation parity, not held-out accuracy.
TYPED_TILE = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'

sys.path.insert(0, str(V3))
sys.path.insert(0, str(APP / 'backend'))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def write_npz(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """np.savez without the wall-clock zip timestamps, so equal arrays give equal bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with zipfile.ZipFile(tmp, 'w', compression=zipfile.ZIP_STORED) as zf:
        for key, value in arrays.items():
            buf = io.BytesIO()
            np.lib.format.write_array(buf, np.asarray(value), allow_pickle=False)
            info = zipfile.ZipInfo(key + '.npy', date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            zf.writestr(info, buf.getvalue())
    tmp.replace(path)


def substitution_frame(seq: str):
    import pandas as pd

    from degron_footprint.features import substitutions
    cells = substitutions(seq)
    return pd.DataFrame({
        'cell_id': [f'fixture:{p}{a}' for p, a in cells], 'peptide_id': 'fixture', 'group_id': 'fixture',
        'wt_sequence': seq, 'mutant_sequence': [seq[:p - 1] + a + seq[p:] for p, a in cells],
        'position_1based': [p for p, _ in cells], 'wt_aa': [seq[p - 1] for p, _ in cells],
        'mut_aa': [a for _, a in cells]})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--out', type=Path, default=OUT)
    a = ap.parse_args(argv)

    import joblib
    import sklearn
    import torch
    import transformers

    torch.set_num_threads(a.threads)
    t0 = time.time()
    card = json.loads(CARD.read_text(encoding='utf-8'))
    assert card['scientific_status'] == 'development_not_gate_closure'
    assert card['campaign'] == CAMPAIGN.name
    bundle = a.out / NAME
    if bundle.exists():
        shutil.rmtree(bundle)
    bundle.mkdir(parents=True)

    # ---------------------------------------------------------------- adapters (learned state of each refit)
    seeds = []
    states = {}
    for m in card['models']:
        src = ROOT / m['path']
        assert sha256(src) == m['sha256'], f'{src} differs from the model card'
        saved = torch.load(src, map_location='cpu', weights_only=True)
        fit = json.loads((src.parent / 'fit.json').read_text(encoding='utf-8'))
        assert saved['model_id'] == m['model_id'] == fit['model_id'] and saved['seed'] == m['seed']
        assert saved['base_revision'] == card['base_revision'] and saved['mode'] == 'lora'
        learned = saved['learned_state']
        names = list(learned)
        arrays = {n: learned[n].detach().cpu().numpy().astype(np.float32) for n in names}
        from degron_footprint.lora import learned_state_digest
        digest = learned_state_digest(names, arrays)
        assert digest == saved['learned_state_sha256'] == fit['learned_state_sha256'], 'learned state digest differs'
        assert names == fit['changed_parameters'], 'parameter order differs from fit.json'
        file = f'adapter-seed{m["seed"]}.npz'
        write_npz(bundle / file, {'__order__': np.array(names), **arrays})
        states[m['seed']] = learned
        seeds.append({'seed': m['seed'], 'model_id': m['model_id'], 'epochs': m['epochs'], 'file': file,
                      'learned_state_sha256': digest, 'source_model_pt_sha256': m['sha256'],
                      'source_fit_json_sha256': sha256(src.parent / 'fit.json'),
                      'train_cells': fit['train_cells'], 'T_fit_cells': fit['T_fit_cells']})

    # ---------------------------------------------------------------- calibrator
    calsrc = ROOT / card['calibrator']['path']
    assert sha256(calsrc) == card['calibrator']['sha256']
    cal = joblib.load(calsrc)                     # own artifact of the branch-1 campaign, hash-checked above
    calibration_json = json.loads((calsrc.parent / 'calibration.json').read_text(encoding='utf-8'))
    assert calibration_json['T_fit_cells'] == 0 and calibration_json['fit_population'] == 'ensemble_OOF_W'
    coef = np.asarray(cal.coef_, dtype=np.float64)
    intercept = np.asarray(cal.intercept_, dtype=np.float64)
    classes = np.asarray(cal.classes_, dtype=np.int64)
    assert coef.shape == (3, 1) and intercept.shape == (3,) and classes.tolist() == [0, 1, 2]
    from degron_footprint.lora import softmax_rows
    grid = np.linspace(-6, 6, 2401)
    sk = cal.predict_proba(grid.reshape(-1, 1))
    mine = softmax_rows(np.outer(grid, coef[:, 0]) + intercept)
    cal_diff = float(np.max(np.abs(sk - mine)))
    assert cal_diff < 1e-12, cal_diff
    write_npz(bundle / 'calibrator.npz', {'coef': coef, 'intercept': intercept, 'classes': classes})

    # ---------------------------------------------------------------- base model snapshot
    status = json.loads((V3 / 'output/weights/esm2_35m/status.json').read_text(encoding='utf-8'))
    assert status['status'] == 'complete' and status['revision'] == card['base_revision']
    snap = V3 / 'output/weights/esm2_35m' / status['revision']
    for f in status['files']:
        s = snap / f['path']
        assert s.stat().st_size == f['bytes'] and sha256(s) == f['sha256'], f['path']
        (bundle / 'base').mkdir(exist_ok=True)
        shutil.copyfile(s, bundle / 'base' / f['path'])

    # ---------------------------------------------------------------- research implementation on the CPU
    from degron_v3.data import Dataset
    from degron_v3.finetune import MutationRegressor, infer
    from degron_v3.local_refit import probabilities
    from degron_v3.plm import Encoder
    ds = Dataset(DATA_V3)
    assert ds.identity == DATA_IDENTITY
    rows32 = ds.sat[FEATURES].head(32).copy()
    # The model's own training tiles, so the API can warn TRAINING_PEPTIDE for this model (the npz model has 176).
    training = sorted(set(map(str, ds.sat.wt_sequence)))
    assert len(training) == ds.sat.peptide_id.nunique(), 'W peptides do not map one-to-one to wild-type tiles'
    (bundle / 'training-sequences.txt').write_text('\n'.join(training) + '\n', encoding='ascii')
    w_tile = str(ds.sat.wt_sequence.iloc[0])
    fixtures = {'tile_w': w_tile, 'tile_typed': TYPED_TILE}
    frames = {k: substitution_frame(v) for k, v in fixtures.items()}
    cross = []
    research: dict[str, list[np.ndarray]] = {k: [] for k in fixtures}
    for m in card['models']:
        enc = Encoder('esm2_35m', [V3 / 'output/weights'], 'cpu', 'float32')
        model = MutationRegressor(enc, 'lora', m['seed'])
        model.restore(states[m['seed']])
        cpu32 = infer(model, rows32, batch=8)
        cuda32 = np.load(CAMPAIGN / f'jobs/model-card-parity/seed{m["seed"]}.npy')
        cross.append({'seed': m['seed'], 'rows': len(rows32), 'max_absolute_difference': float(np.max(np.abs(cpu32 - cuda32))),
                      'cuda_runtime': 'Windows, RTX 5060 Laptop, Torch 2.13.0+cu130 (campaign parity job)'})
        for k, fr in frames.items():
            research[k].append(infer(model, fr, batch=8))
        del model, enc

    fixture_arrays: dict[str, np.ndarray] = {}
    for k, seq in fixtures.items():
        per_seed = np.stack(research[k])                                   # (3, 532) float32
        mean = np.mean(list(per_seed), axis=0)
        fixture_arrays[f'{k}_sequence'] = np.array(seq)
        fixture_arrays[f'{k}_per_seed'] = per_seed
        fixture_arrays[f'{k}_score'] = mean
        fixture_arrays[f'{k}_prob'] = probabilities(cal, mean)[:, 2]
    write_npz(bundle / 'parity-fixture.npz', fixture_arrays)

    # ---------------------------------------------------------------- manifest
    results = json.loads(RESULTS.read_text(encoding='utf-8'))
    lora_all = results['metrics']['esm2_35m-lora-D']['all']
    evaluation = {
        'source_file': 'research/lora-refit-transfer-2026-11-16/results.json',
        'source_sha256': sha256(RESULTS),
        'evaluation': results['evaluation'], 'primary_endpoint': results['primary_endpoint'],
        'denominators': results['denominators'],
        'peptide_macro_mae': lora_all['mae'], 'spearman': lora_all['spearman'],
        'auroc_plus': lora_all['auroc_plus'], 'auroc_plus_eligible_peptides': lora_all['auroc_plus_eligible_peptides'],
        'contrasts': {k: {kk: v[kk] for kk in ('delta', 'ci_adjusted', 'multiplicity', 'peptides', 'clusters',
                                                  'bootstrap')}
                      for k, v in results['contrasts'].items()},
        'contrast_metric': 'peptide macro MAE difference (negative = LoRA-D lower error); CI 97.5 % adjusted x2',
        'gt5_peptide_macro_mae': {k: results['metrics'][k]['strata']['gt5']['mae'] for k in ('esm2_35m-lora-D', 'zero')},
        'zero_baseline_note': 'In the T stratum PSI(WT) > 5 the zero predictor has lower peptide macro MAE than '
                              'LoRA-D (results.json metrics.*.strata.gt5).',
        'limitations': results['limitations'],
    }
    files = {}
    for f in sorted(bundle.rglob('*')):
        if f.is_file():
            files[f.relative_to(bundle).as_posix()] = {'sha256': sha256(f), 'bytes': f.stat().st_size}
    manifest = {
        'schema_version': 1, 'kind': 'torch_lora', 'model_id': MODEL_ID, 'bundle_dir': NAME,
        'scientific_status': card['scientific_status'], 'serving_promotion': card['serving_promotion'],
        'G2_G3': card['G2_G3'], 'claim_boundary': card['claim_boundary'],
        'campaign': card['campaign'], 'source_model_card_sha256': sha256(CARD),
        'source_model_card': CARD.relative_to(ROOT).as_posix(),
        'base': {'repo': card['base_model'], 'revision': card['base_revision'], 'dir': 'base', 'dtype': card['dtype']},
        'adapter': card['adapter'], 'features': card['features'],
        'head': {'layers': 'Linear(2*480+60,64) ReLU Dropout(0.2) Linear(64,1)', 'output': 'raw DeltaPSI'},
        'ensemble': card['ensemble'], 'seeds': seeds,
        'calibrator': {'file': 'calibrator.npz', 'kind': 'multinomial_logistic', 'classes': [0, 1, 2],
                       'class_meaning': ['DeltaPSI <= -1', 'neutral', 'DeltaPSI >= 1'], 'event_class': 2,
                       'fit': card['calibrator']['fit'], 'source_sha256': card['calibrator']['sha256'],
                       'train_cells': calibration_json['train_cells'], 'T_fit_cells': calibration_json['T_fit_cells']},
        'training': {'population': 'W (saturation cells, arm D: all wild-type PSI)', 'cells': seeds[0]['train_cells'],
                     'data_identity': DATA_IDENTITY},
        'event_definition': 'P(DeltaPSI >= 1.0)',
        'parity_fixture': 'parity-fixture.npz', 'evaluation': evaluation, 'files': files,
        'training_sequences': {'file': 'training-sequences.txt', 'count': len(training),
                               'meaning': 'wild-type 28-mers of the W saturation peptides the refit was trained on'},
    }
    a.out.mkdir(parents=True, exist_ok=True)
    mpath = a.out / f'{NAME}.json'
    mpath.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    # ---------------------------------------------------------------- serving implementation on the same tiles
    from degron_footprint.lora import LoraEnsembleModel
    served = LoraEnsembleModel.from_file(MODEL_ID, mpath, sha256(mpath))
    served.threads = a.threads
    serving = {}
    for k, seq in fixtures.items():
        t1 = time.perf_counter()
        pred = served.predict_tile(seq)
        sec = time.perf_counter() - t1
        per_seed, _ = served.raw_scores(seq)
        serving[k] = {
            'seconds_first_call_included': round(sec, 3),
            'max_abs_diff_per_seed_raw': float(np.max(np.abs(per_seed - fixture_arrays[f'{k}_per_seed']))),
            'max_abs_diff_ensemble_score': float(np.max(np.abs(pred.score - fixture_arrays[f'{k}_score']))),
            'max_abs_diff_prob': float(np.max(np.abs(pred.prob - fixture_arrays[f'{k}_prob']))),
            'cells': int(len(pred.score))}

    report = {
        'schema_version': 1, 'generated_by': 'system/app/etl/export_lora.py', 'model_id': MODEL_ID,
        'scientific_status': 'development_not_gate_closure',
        'serving_promotion': 'not_authorized_by_research_execution',
        'manifest': {'path': mpath.relative_to(ROOT).as_posix(), 'sha256': sha256(mpath), 'bytes': mpath.stat().st_size},
        'bundle_bytes': sum(v['bytes'] for v in files.values()), 'bundle_files': len(files),
        'calibrator_sklearn_vs_softmax_max_diff': cal_diff,
        'cross_runtime_parity': {
            'scope': 'research implementation, same 32 W rows: CUDA (Windows campaign parity job) vs CPU (this run)',
            'tests': cross, 'max_absolute_difference': max(t['max_absolute_difference'] for t in cross)},
        'serving_parity': {
            'scope': 'research implementation (degron_v3, CPU) vs serving implementation (degron_footprint.lora, CPU) '
                     'on two full tiles', 'tiles': serving},
        'runtime': {'python': platform.python_version(), 'torch': torch.__version__,
                    'transformers': transformers.__version__, 'sklearn': sklearn.__version__,
                    'numpy': np.__version__, 'platform': platform.platform(), 'threads': a.threads},
        'seconds': round(time.time() - t0, 1),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
