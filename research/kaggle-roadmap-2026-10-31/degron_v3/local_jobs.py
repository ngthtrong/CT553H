"""Independent local work units reusing the reviewed v3 scientific components."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import zipfile

import joblib
import numpy as np
import pandas as pd
import requests
import torch
from sklearn.linear_model import Ridge

from .common import atomic_json, sha256
from .data import arm_mask
from .features import features
from .learning import CombinedRidge
from .local_control import atomic_torch, fingerprint
from .local_training import fit, predict
from .metrics import summarize, per_peptide, paired_ci
from .plm import Encoder, preflight, resolve_snapshot, specification, prefix_hash, INFERENCE_DTYPES

HERE = Path(__file__).resolve().parents[1]
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
SOURCE = HERE/'output/official/369cb2fe6a1e31e0'
MODELS = ['esm2_8m', 'esm2_35m', 'esm2_150m', 'esm2_650m', 'esm1b_650m',
          'esm1v_650m_1', 'esmc_300m', 'prott5_encoder', 'ankh_base']


class Blocked(Exception):
    def __init__(self, message, kind='resource_blocked'):
        super().__init__(message); self.kind = kind


def artifact_directory(campaign, job):
    campaign = Path(campaign)
    state = json.loads((campaign/'state.json').read_text())['jobs']
    record = state.get(job, {})
    origin = Path(record.get('artifact_campaign', campaign)).resolve()
    if origin != campaign.resolve():
        assert origin.parent == campaign.resolve().parent, 'Inherited artifact outside campaign root'
        assert record['status'] == 'complete', 'Only completed artifacts can be referenced'
        assert sha256(origin/'plan.json') == record['source_plan_sha256'], 'Inherited source plan changed'
    return origin/'jobs'/job


def roots(campaign):
    return [campaign.parent/'weights', HERE/'output/weights']


def budget(campaign, incoming=0):
    used = sum(p.stat().st_size for p in campaign.parent.rglob('*') if p.is_file())
    if used+incoming > 50*2**30 or shutil.disk_usage(campaign).free < incoming+30*2**30:
        raise Blocked('50 GiB local budget or 30 GiB free-disk reserve reached')


def import_kaggle(ds, out, control):
    manifest = json.loads((SOURCE/'pipeline-manifest.json').read_text())
    assert manifest['plan']['data_identity'] == ds.identity
    count = 0
    for task in manifest['tasks'].values():
        if task['status'] != 'complete': continue
        for entry in task['files']:
            path = SOURCE/entry['path']
            assert path.is_file() and path.stat().st_size == entry['bytes'] and sha256(path) == entry['sha256'], entry['path']
            count += 1
            if count % 100 == 0:
                control.log(f'import verified {count} files', force=True); control.check()
    atomic_json(out/'import.json', dict(status='verified_reference_only', files_verified=count,
        source=str(SOURCE), manifest_sha256=sha256(SOURCE/'pipeline-manifest.json'),
        data_identity=ds.identity, source_runtime=manifest['tasks']['00']['runtime'],
        note='Read-only Kaggle references; local training uses separate runtime and outputs.'))


def weights(model, campaign, out, control):
    for root in roots(campaign):
        try:
            folder, status = resolve_snapshot(model, [root])
        except FileNotFoundError:
            continue
        assert status['revision']==specification(model)['checkpoint_revision'], 'Unexpected checkpoint revision'
        for entry in status['files']:
            assert sha256(folder/entry['path']) == entry['sha256']
        atomic_json(out/'weights.json', dict(status='reused', model=model, source=str(folder)))
        control.log(f'WEIGHTS REUSED {model}', force=True)
        return
    target_root = roots(campaign)[0]; target_root.mkdir(parents=True, exist_ok=True)
    archive = TOPIC/'data/processed/packages/degron-weights-v3-fd5593922ec4.zip'
    if archive.exists() and model in ('esm2_8m', 'esm2_650m'):
        expected = json.loads((HERE/'weights-build.json').read_text())
        expected_hash = expected.get('sha256')
        # This package was inspected before implementation; pin even if builder schema changes.
        assert sha256(archive) == (expected_hash or '3cfba44bebfc12c8f424437ac1846f18c8b8737b77528d7701c8ac12c5ba5193')
        with zipfile.ZipFile(archive) as z:
            prefix = f'plm-weights-v3/{model}/'
            entries = sorted([info for info in z.infolist() if info.filename.startswith(prefix) and not info.is_dir()],
                             key=lambda info: info.filename.endswith('/status.json'))
            budget(campaign, sum(i.file_size for i in entries))
            for info in entries:
                relative = Path(info.filename).relative_to('plm-weights-v3')
                path = (target_root/relative).resolve()
                assert path.is_relative_to(target_root.resolve())
                path.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, path.with_suffix(path.suffix+'.partial').open('wb') as dst:
                    shutil.copyfileobj(src, dst)
                os.replace(path.with_suffix(path.suffix+'.partial'), path)
                control.log(f'unpacked {relative}', force=True); control.check()
        return weights(model, campaign, out, control)
    import download_weights as downloader
    spec = specification(model)
    control.check()
    meta_response = requests.get(f"https://huggingface.co/api/models/{spec['checkpoint']}/revision/{spec['checkpoint_revision']}?blobs=true", timeout=30)
    meta_response.raise_for_status(); meta = meta_response.json()
    assert meta['sha'] == spec['checkpoint_revision']
    selected = downloader.select_files(meta['siblings'])
    budget(campaign, sum(e['size'] for e in selected))
    weight_bytes = sum(e['size'] for e in selected if e['rfilename'].endswith(('.bin', '.safetensors')))
    if weight_bytes/2+2*2**30 > 6*2**30:
        raise Blocked('Conservative pre-download estimate exceeds the 6 GiB GPU budget')
    folder = target_root/model/meta['sha']; folder.mkdir(parents=True, exist_ok=True)
    records = []
    for entry in selected:
        relative = Path(entry['rfilename']); assert not relative.is_absolute() and '..' not in relative.parts
        path = folder/relative; path.parent.mkdir(parents=True, exist_ok=True)
        part = path.with_suffix(path.suffix+'.partial')
        if not downloader.valid_file(path, entry):
            for attempt in range(3):
                control.check()
                offset = part.stat().st_size if part.exists() else 0
                assert offset <= entry['size']
                if offset == entry['size']: break
                url = f"https://huggingface.co/{meta['id']}/resolve/{meta['sha']}/{relative.as_posix()}"
                try:
                    with requests.get(url, headers={'Range': f'bytes={offset}-'} if offset else {}, stream=True, timeout=(15,30)) as r:
                        r.raise_for_status()
                        append = offset > 0 and r.status_code == 206
                        if append: assert r.headers.get('Content-Range','').startswith(f'bytes {offset}-')
                        written = offset if append else 0
                        with part.open('ab' if append else 'wb') as stream:
                            for chunk in r.iter_content(1<<20):
                                if chunk:
                                    stream.write(chunk); written += len(chunk)
                                control.log(f'download {model}/{relative} {written/2**20:.1f}/{entry["size"]/2**20:.1f}MiB')
                                control.check()
                    if part.stat().st_size == entry['size']: break
                except requests.RequestException:
                    control.check()
                    if attempt == 2: raise
            assert downloader.valid_file(part, entry), f'Weight integrity mismatch: {relative}'
            os.replace(part, path)
        records.append(dict(path=relative.as_posix(), bytes=path.stat().st_size, sha256=sha256(path)))
        control.log(f'verified {model}/{relative}', force=True)
    atomic_json(target_root/model/'status.json', dict(status='complete', model_id=model,
        repo=meta['id'], revision=meta['sha'], files=records))
    (target_root/model/'SOURCE.md').write_text(f"Pinned source: https://huggingface.co/{meta['id']}\nRevision: {meta['sha']}\nSHA-256: status.json. No remote Python executed.\n", encoding='utf8')
    atomic_json(out/'weights.json', dict(status='downloaded', model=model, source=str(folder)))


def probe(model, campaign, out, control):
    try:
        preflight([model], roots(campaign), out, smoke=False)
    except (AttributeError, ImportError, ValueError, AssertionError, RuntimeError) as exc:
        raise Blocked(f'{type(exc).__name__}: {exc}', 'adapter_blocked') from exc
    report = json.loads((out/'preflight.json').read_text())['models'][0]
    if report['status'] != 'feasible':
        reason = report.get('reason','Unknown preflight failure')
        raise Blocked(reason, 'resource_blocked' if any(k in reason.lower() for k in ['memory','cuda out of']) else 'adapter_blocked')
    if report['peak_vram_bytes'] > 6*2**30:
        raise Blocked('Preflight exceeds 6 GiB GPU allocation budget')
    control.check()


def extract(ds, model, campaign, out, control, frame=None, scope='sat'):
    frame = ds.sat.reset_index(drop=True) if frame is None else frame.reset_index(drop=True)
    encoder = Encoder(model, roots(campaign), 'cuda', 'float16')
    dim = encoder.tensor([frame.wt_sequence.iloc[0]]).shape[-1]
    identity = fingerprint(dict(data=ds.identity, model=model, revision=encoder.lock['revision'],
        cells=frame.cell_id.tolist(), scope=scope, dtype='float16', feature='delta_site_and_mean',
        runtime=json.loads((campaign/'plan.json').read_text())['runtime'], encoder_dtype=str(encoder.dtype)))
    path = out/'pool.npy'; progress = out/'progress.json'
    if path.exists() and progress.exists():
        saved = json.loads(progress.read_text()); assert saved['identity'] == identity
        values = np.load(path, mmap_mode='r+'); completed = saved['completed']
        assert prefix_hash(values, completed) == saved['prefix_sha256']
    else:
        budget(campaign, len(frame)*2*dim*2)
        values = np.lib.format.open_memmap(path, mode='w+', dtype='float16', shape=(len(frame), 2*dim)); completed = 0
    wt_cache = {}
    for start in range(completed, len(frame), 8):
        rows = frame.iloc[start:start+8]
        missing = [s for s in dict.fromkeys(rows.wt_sequence) if s not in wt_cache]
        if missing:
            wt_cache.update(zip(missing, encoder(missing)))
        delta = encoder(rows.mutant_sequence.tolist())-np.stack([wt_cache[s] for s in rows.wt_sequence])
        positions = rows.position_1based.to_numpy(int)-1
        values[start:start+len(rows)] = np.concatenate([delta[np.arange(len(rows)), positions], delta.mean(1)], 1)
        end = start+len(rows)
        assert np.isfinite(values[start:end]).all()
        control.log(f'extract {model} {end}/{len(frame)}', rows=end, total_rows=len(frame))
        if end % 512 == 0 or end == len(frame) or control.stopping():
            values.flush(); atomic_json(progress, dict(identity=identity, completed=end, prefix_sha256=prefix_hash(values,end)))
        control.check()
    frame[['cell_id','peptide_id']].to_parquet(out/'rows.parquet', index=False)
    atomic_json(out/'feature-manifest.json', dict(status='complete', identity=identity,
        data_identity=ds.identity, model_id=model, rows=len(frame), mode='official', scope=scope,
        revision=encoder.lock['revision'], dtype='float16', feature_kind='delta_site_and_mean',
        encoder_dtype=str(encoder.dtype),
        files=[dict(path=p.name,sha256=sha256(p)) for p in [path,out/'rows.parquet']]))


def oof_rows(frame, prediction, recipe, seed, identity):
    rows = frame[['cell_id','peptide_id','group_id','outer_fold','psi_stratum','dpsi_mean']].copy()
    rows['prediction'] = prediction; rows['recipe'] = recipe; rows['seed'] = seed
    rows['mode'] = 'official'; rows['data_identity'] = identity; rows['platform'] = 'local'
    assert np.isfinite(rows.prediction).all()
    return rows


def ridge_fold(ds, job, campaign, out, control):
    model, arm, context, seed, fold = [job[k] for k in ['model','arm','context','seed','fold']]
    delta = np.asarray(np.load(artifact_directory(campaign, f'extract-{model}')/'pool.npy', mmap_mode='r'), dtype='float32')
    ctx = features(ds.sat, 'ordered', 5) if context else None
    X = np.concatenate([ctx, delta],1) if context else delta
    role = ds.role(ds.sat, fold, seed); chosen = arm_mask(ds.sat, arm)
    tr = np.flatnonzero((role=='train') & chosen); va = np.flatnonzero(role=='validation'); te = np.flatnonzero(role=='test')
    recipe = f'{model}-'+('context-' if context else 'only-')+arm
    candidate = None; checkpoint = out/'model.joblib'; metadata = out/'fit.json'
    if checkpoint.exists() and metadata.exists():
        info = json.loads(metadata.read_text()); candidate = joblib.load(checkpoint)
    else:
        alphas = [.1,1.,10.,100.,1000.]
        weight = np.ones(len(tr))
        candidate = CombinedRidge(alphas[0], 260 if context else 0, 64, seed).fit(X[tr], ds.sat.dpsi_mean.to_numpy()[tr], weight)
        ztr, zva = candidate._transform(X[tr]), candidate._transform(X[va]); scores = []
        for alpha in alphas:
            candidate.model = Ridge(alpha=alpha).fit(ztr, ds.sat.dpsi_mean.to_numpy()[tr], sample_weight=weight)
            scores.append(float(np.square(candidate.model.predict(zva)-ds.sat.dpsi_mean.to_numpy()[va]).mean()))
            control.log(f'Ridge alpha={alpha} mse={scores[-1]:.6f}', force=True); control.check()
        alpha = alphas[int(np.argmin(scores))]
        candidate.model = Ridge(alpha=alpha).fit(ztr, ds.sat.dpsi_mean.to_numpy()[tr], sample_weight=weight)
        calibration = ds.sat.iloc[va][['cell_id','peptide_id','group_id','dpsi_mean']].copy()
        calibration['prediction'] = candidate.model.predict(zva); calibration.to_parquet(out/'calibration.parquet', index=False)
        final = np.flatnonzero(np.isin(role,['train','validation']) & chosen)
        candidate = CombinedRidge(alpha, 260 if context else 0, 64, seed).fit(X[final], ds.sat.dpsi_mean.to_numpy()[final], np.ones(len(final)))
        temporary = checkpoint.with_suffix('.tmp'); joblib.dump(candidate, temporary); os.replace(temporary, checkpoint)
        info = dict(recipe=recipe, model=model, arm=arm, context=context, seed=seed, fold=fold,
                    alpha=alpha, validation_mse=min(scores), data_identity=ds.identity)
        atomic_json(metadata, info)
    control.check()
    oof_rows(ds.sat.iloc[te], candidate.predict(X[te]), recipe, seed, ds.identity).to_parquet(out/'oof.parquet', index=False)


def finetune_fold(ds, job, campaign, out, control):
    from .finetune import MutationRegressor
    seed, fold, arm, mode = [job[k] for k in ['seed','fold','arm','mode']]
    recipe = f'esm2_35m-{mode}-{arm}'
    role = ds.role(ds.sat, fold, seed); mask = arm_mask(ds.sat, arm)
    train = ds.sat.loc[(role=='train') & mask].copy(); validation = ds.sat.loc[role=='validation'].copy()
    test = ds.sat.loc[role=='test'].copy()
    encoder = Encoder('esm2_35m', roots(campaign), 'cuda','float32')
    model = MutationRegressor(encoder, mode, seed); initial = model.learned_state()
    epoch, vmse = fit(model, train, validation, seed, out/'inner.pt', control)
    cal = validation[['cell_id','peptide_id','group_id','dpsi_mean']].copy()
    cal['prediction'] = predict(model, validation, out/'calibration.npy', control)
    cal.to_parquet(out/'calibration.parquet',index=False)
    model.restore(initial)
    final = ds.sat.loc[np.isin(role,['train','validation']) & mask].copy()
    fit(model, final, validation, seed, out/'refit.pt', control, epochs=epoch, refit=True)
    learned = model.learned_state()
    changed = [name for name in learned if not torch.equal(learned[name], initial[name])]
    assert changed and (mode != 'lora' or any('lora_' in name for name in changed))
    oof_rows(test, predict(model, test, out/'test.npy',control), recipe,seed,ds.identity).to_parquet(out/'oof.parquet',index=False)
    atomic_torch(out/'model.pt', dict(learned_state=learned,model_id='esm2_35m',mode=mode,arm=arm,seed=seed,
        fold=fold,data_identity=ds.identity,base_revision=encoder.lock['revision'],selected_epoch=epoch))
    atomic_json(out/'fit.json', dict(recipe=recipe,seed=seed,fold=fold,arm=arm,mode=mode,
        selected_epoch=epoch,validation_mse=vmse,changed_parameters=changed,data_identity=ds.identity))
