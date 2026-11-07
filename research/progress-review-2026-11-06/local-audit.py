"""Read campaign/data bytes and independently check OOF evidence for progress review.

Run: .venv/bin/python -I research/progress-review-2026-11-06/local-audit.py
Only local-audit.json and source-inventory.json beside this script are written.
No models are deserialized; the original Windows paths are resolved by campaign
basename into the existing, read-only Linux copy, never by rewriting manifests.
"""
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path, PureWindowsPath
import subprocess

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
REPO = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
ROAD = TOPIC / 'research/kaggle-roadmap-2026-10-31'
DATA = TOPIC / 'data/processed/v3-fullpsi'
CAMPAIGN = ROAD / 'output/local/ef138c84579c842e'
TZ = timezone(timedelta(hours=8))
SOURCES = {}
HASHES = {}


def digest(path):
    path = Path(path)
    if path not in HASHES:
        with path.open('rb') as stream:
            HASHES[path] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return HASHES[path]


def source(path):
    path = Path(path)
    key = path.relative_to(REPO).as_posix()
    if key not in SOURCES:
        SOURCES[key] = {'bytes': path.stat().st_size, 'sha256': digest(path)}
    return path


def read(path):
    return json.loads(source(path).read_text())


def campaign_path(record):
    original = record.get('artifact_campaign')
    if not original:
        return CAMPAIGN
    name = PureWindowsPath(original).name if '\\' in original else Path(original).name
    assert name in {'ef138c84579c842e', 'e7097449883a51d8'}
    return CAMPAIGN.parent / name


def metric_rows(frame):
    rows = []
    for peptide, s in frame.groupby('peptide_id', observed=True):
        y, pred = s.dpsi_mean.to_numpy(), s.prediction.to_numpy()
        row = {'peptide_id': peptide, 'group_id': s.group_id.iloc[0],
               'psi_stratum': s.psi_stratum.iloc[0], 'outer_fold': int(s.outer_fold.iloc[0]),
               'cells': len(s), 'mae': float(np.abs(pred-y).mean()),
               'rmse': float(np.sqrt(np.square(pred-y).mean()))}
        rho = spearmanr(y, pred).statistic if np.ptp(y) and np.ptp(pred) else np.nan
        row['spearman'] = float(rho) if np.isfinite(rho) else None
        for direction, label, score in [('plus', y >= 1, pred), ('minus', y <= -1, -pred)]:
            eligible = min(label.sum(), len(label)-label.sum()) >= 3
            row['auroc_'+direction] = float(roc_auc_score(label, score)) if eligible else None
            row['auprc_'+direction] = float(average_precision_score(label, score)) if eligible else None
        rows.append(row)
    return pd.DataFrame(rows)


def summary(rows):
    result = {'peptides': len(rows), 'groups': int(rows.group_id.nunique()), 'cells': int(rows.cells.sum())}
    for m in ['mae', 'rmse', 'spearman', 'auroc_plus', 'auprc_plus', 'auroc_minus', 'auprc_minus']:
        vals = rows[m].dropna()
        result[m] = float(vals.mean()) if len(vals) else None
        result[m+'_eligible_peptides'] = len(vals)
    return result


def subgroup_error(frame, keys):
    # Macro over peptides within each subgroup; counts are explicit because the
    # conditioning changes the estimand, especially for effects of large size.
    rows = []
    for key, sub in frame.groupby(keys, observed=True):
        key = key if isinstance(key, tuple) else (key,)
        rows.append({**dict(zip(keys, key)), 'cells': len(sub),
                     'peptides': int(sub.peptide_id.nunique()), 'groups': int(sub.group_id.nunique()),
                     'mae': float(sub.groupby('peptide_id', observed=True).error.mean().mean()),
                     'zero_mae': float(sub.groupby('peptide_id', observed=True).zero_error.mean().mean()),
                     'mean_signed_error_cell_micro': float(sub.signed_error.mean())})
    return rows


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def main():
    saved = read(ROAD/'local-output-analysis.json')
    state = read(CAMPAIGN/'state.json'); plan = read(CAMPAIGN/'plan.json')
    queue = read(CAMPAIGN/'queue.json'); manifest = read(DATA/'DATA_MANIFEST.json')
    data_identity = digest(DATA/'DATA_MANIFEST.json')
    assert data_identity == plan['data_identity'] == saved['data_identity']
    data_checks = []
    for item in manifest['files']:
        path = DATA/item['path']
        assert path.is_file() and path.stat().st_size == item['bytes'], str(path)
        assert digest(path) == item['sha256'], str(path)
        data_checks.append(item['path'])
    print('PASS data manifest', len(data_checks), flush=True)
    assert set(state['jobs']) == {j['id'] for j in queue}
    checked = {}; inherited = 0
    for job, record in state['jobs'].items():
        if record['status'] != 'complete':
            continue
        origin = campaign_path(record)
        if origin != CAMPAIGN:
            inherited += 1
            assert digest(origin/'plan.json') == record['source_plan_sha256']
        for entry in record['files']:
            path = origin/entry['path']
            assert path.resolve().is_relative_to(origin.resolve())
            assert path.is_file() and path.stat().st_size == entry['bytes'], str(path)
            assert digest(path) == entry['sha256'], str(path)
            checked[path] = entry['bytes']
    kaggle = ROAD/'output/official'/plan['source_campaign']
    kmanifest = read(kaggle/'pipeline-manifest.json'); kchecked = {}
    for task in kmanifest['tasks'].values():
        if task['status'] != 'complete':
            continue
        for item in task['files']:
            path = kaggle/item['path']
            assert path.stat().st_size == item['bytes'] and digest(path) == item['sha256']
            kchecked[path] = item['bytes']
    lineage = read(CAMPAIGN/'inheritance.json')
    assert digest(CAMPAIGN.parent/PureWindowsPath(lineage['source_campaign']).name/'state.json') == lineage['source_state_sha256']
    assert inherited == lineage['inherited_complete'] == 456
    newline_reconciliations = []
    for name, expected in saved['source_files'].items():
        p = ROAD/name
        if p.stat().st_size != expected['bytes'] or digest(p) != expected['sha256']:
            raw = p.read_bytes()
            reconstructed = raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
            assert p.suffix == '.json' and len(reconstructed) == expected['bytes'] and hashlib.sha256(reconstructed).hexdigest() == expected['sha256'], name
            newline_reconciliations.append({'path':name,'stored_expected':expected,
                'actual':{'bytes':len(raw),'sha256':digest(p)},'resolution':'LF to CRLF byte reconstruction exactly matches pinned SHA and size; no source modification.'})
    print('PASS artifact/analysis-source hashes', len(checked), len(kchecked), flush=True)
    sat = pd.read_parquet(source(DATA/'tables/saturation-cells.parquet'))
    wide = pd.read_parquet(source(DATA/'splits/wide-outer.parquet'))
    reference = sat.set_index('cell_id')[['peptide_id','group_id','psi_stratum','dpsi_mean']].copy()
    reference['outer_fold'] = reference.peptide_id.map(wide.set_index('peptide_id').outer_fold)
    reference = reference.sort_index()
    assert len(reference) == 122412 and reference.groupby('group_id').outer_fold.nunique().max() == 1
    split_checks = []
    for seed in [17,29,43]:
        split = pd.read_parquet(source(DATA/f'splits/inner-seed{seed}.parquet'))
        for fold, sub in split.groupby('outer_fold'):
            assert not sub.group_id.duplicated().any()
            assert set(sub.role) == {'train','validation','test','held_source'}
            expected = set(reference.loc[reference.outer_fold == fold].group_id)
            assert set(sub.loc[sub.role=='test','group_id']) == expected
            split_checks.append({'seed': seed, 'fold': int(fold), 'groups_per_role': sub.role.value_counts().to_dict()})
    recipes = {}; core_frames = {}; core_peptides = {}; diagnostics = {}
    for group in ['collect-family','collect-core']:
        collection = read(CAMPAIGN/'jobs'/group/'collection.json')
        for recipe, report in collection['reports'].items():
            frame = pd.read_parquet(source(CAMPAIGN/'jobs'/group/(recipe+'-oof.parquet')))
            assert sorted(frame.seed.unique()) == [17,29,43]
            assert set(frame['mode']) == {'official'} and set(frame.data_identity) == {data_identity}
            assert not frame.duplicated(['seed','cell_id']).any() and np.isfinite(frame.prediction).all()
            seed_mae = {}
            for seed, sub in frame.groupby('seed'):
                pd.testing.assert_frame_equal(sub.set_index('cell_id')[reference.columns].sort_index(),reference,check_dtype=False,check_exact=True)
                m = float(sub.assign(error=(sub.prediction-sub.dpsi_mean).abs()).groupby('peptide_id').error.mean().mean())
                expected_seeds = report.get('per_seed', saved['local_recipes'][recipe]['per_seed'])
                expected_seed = expected_seeds[str(seed)]
                expected_seed = expected_seed.get('all', expected_seed)
                assert abs(m-expected_seed['mae']) < 1e-10
                seed_mae[str(seed)] = m
            ensemble = reference.copy()
            ensemble['prediction'] = frame.groupby('cell_id').prediction.mean().reindex(reference.index)
            pp = metric_rows(ensemble) if group == 'collect-core' else None
            mae = float((ensemble.prediction-ensemble.dpsi_mean).abs().groupby(ensemble.peptide_id).mean().mean())
            assert abs(mae-report['ensemble']['all']['mae']) < 1e-10
            recipes[recipe] = {'mae': mae, 'per_seed_mae': seed_mae, 'oof_rows': len(frame), 'seeds': [17,29,43]}
            if pp is not None:
                measured = summary(pp)
                for key, actual in measured.items():
                    if key in report['ensemble']['all']:
                        expected = report['ensemble']['all'][key]
                        assert actual == expected if expected is None else abs(actual-expected) < 1e-10
                recipes[recipe]['metrics'] = measured
                core_peptides[recipe] = pp; core_frames[recipe] = ensemble
                diagnostic = ensemble.join(sat.set_index('cell_id')[['wt_aa','mut_aa','position_1based','accession']])
                diagnostic['signed_error'] = diagnostic.prediction-diagnostic.dpsi_mean
                diagnostic['error'] = diagnostic.signed_error.abs()
                diagnostic['zero_error'] = diagnostic.dpsi_mean.abs()
                diagnostic['effect_class'] = np.where(diagnostic.dpsi_mean>=1,'positive_ge1',np.where(diagnostic.dpsi_mean<=-1,'negative_le-1','neutral'))
                diagnostic['absolute_effect_ge1'] = diagnostic.dpsi_mean.abs()>=1
                diagnostics[recipe] = {
                    'per_peptide': pp.to_dict('records'),
                    'per_fold': subgroup_error(diagnostic,['outer_fold']),
                    'per_stratum': subgroup_error(diagnostic,['psi_stratum']),
                    'per_mutant_aa': subgroup_error(diagnostic,['mut_aa']),
                    'per_substitution': subgroup_error(diagnostic,['wt_aa','mut_aa']),
                    'per_effect_class': subgroup_error(diagnostic,['effect_class']),
                    'per_large_effect': subgroup_error(diagnostic,['absolute_effect_ge1']),
                    'largest_cell_errors': diagnostic.sort_values('error',ascending=False).head(20).reset_index().to_dict('records'),
                    'worst_peptides': pp.sort_values('mae',ascending=False).head(20).to_dict('records'),
                }
            print('PASS OOF', recipe, flush=True)
    contrasts = {}
    for arm in ['B','D']:
        a = core_peptides['esm2_35m-lora-'+arm]
        b = core_peptides['esm2_35m-frozen-'+arm]
        merged = a[['peptide_id','group_id','outer_fold','psi_stratum','mae']].merge(b[['peptide_id','mae']],on='peptide_id',suffixes=('_lora','_frozen'))
        merged['delta_mae'] = merged.mae_lora-merged.mae_frozen
        grouped = merged.groupby('group_id').delta_mae.mean()
        contrasts[arm] = {
            'peptides_improved': int((merged.delta_mae<0).sum()), 'peptides_worsened': int((merged.delta_mae>0).sum()),
            'groups_improved': int((grouped<0).sum()), 'groups_worsened': int((grouped>0).sum()),
            'mean_delta_peptide_macro': float(merged.delta_mae.mean()),
            'delta_peptide_quantiles': {str(q): float(merged.delta_mae.quantile(q)) for q in [0,.1,.25,.5,.75,.9,1]},
            'per_peptide': merged.to_dict('records'),
            'per_group': grouped.rename('delta_mae').reset_index().to_dict('records'),
            'leave_one_group_out_delta_range': [float(merged.loc[merged.group_id!=g].delta_mae.mean()) for g in grouped.index],
        }
        values = contrasts[arm].pop('leave_one_group_out_delta_range')
        contrasts[arm]['leave_one_group_out_delta_range'] = [min(values),max(values)]
    nested = read(CAMPAIGN/'jobs/collect-family/collection.json')['reports']['nested-family-selection']['choices']
    for choice in nested:
        candidates = []
        for job in queue:
            if job['kind']=='ridge' and job['seed']==choice['seed'] and job['fold']==choice['fold']:
                fit = read(campaign_path(state['jobs'][job['id']])/'jobs'/job['id']/'fit.json')
                candidates.append((fit['validation_mse'],fit['recipe']))
        assert min(candidates) == (choice['validation_mse'],choice['recipe'])
    adapter_fits = []
    for job in queue:
        if job['kind']=='tune':
            fit = read(campaign_path(state['jobs'][job['id']])/'jobs'/job['id']/'fit.json')
            if job['mode']=='lora':
                assert any('lora_' in n for n in fit['changed_parameters'])
            adapter_fits.append({'job':job['id'],'mode':job['mode'],'selected_epoch':fit['selected_epoch'],'changed_tensors':len(fit['changed_parameters'])})
    calibration = {}
    for recipe in core_frames:
        p = CAMPAIGN/'jobs/calibrate-core'/recipe/'calibrated-oof.parquet'
        f = pd.read_parquet(source(p)); print('calibration schema',recipe,f.columns.tolist(),flush=True)
        probability = f.groupby('cell_id')[['p_minus','p_neutral','p_plus']].mean().reindex(reference.index).to_numpy()
        assert np.isfinite(probability).all() and np.allclose(probability.sum(1),1)
        label = np.where(reference.dpsi_mean.to_numpy()<=-1,0,np.where(reference.dpsi_mean.to_numpy()>=1,2,1))
        error = np.square(probability-np.eye(3)[label]).sum(1)
        brier = float(error.mean())
        assert abs(brier-saved['calibration'][recipe]['multiclass_brier_cell_micro'])<1e-10
        calibration[recipe] = {'multiclass_brier_cell_micro':brier,'finite_probabilities_sum_one':True}
    held = pd.read_parquet(source(CAMPAIGN/'jobs/locked-transfer-w5/ordered-w5-D/held-scanning.parquet'))
    assert set(held.partition) == {'scan_T'} and set(held.mut_aa) == {'R','A','S'}
    assert not set(held.group_id) & set(reference.group_id)
    scanning = pd.read_parquet(source(DATA/'tables/scanning-cells.parquet'))
    assert not set(held.group_id) & set(scanning.loc[scanning.partition=='scan_dev','group_id'])
    assert np.array_equal(held.dpsi_mean, held.dpsi_rep1)
    held = held.copy(); held['outer_fold'] = -1
    transfer_metrics = summary(metric_rows(held))
    for key, actual in transfer_metrics.items():
        if key in saved['transfer']['population']['all']:
            expected = saved['transfer']['population']['all'][key]
            assert actual == expected if expected is None else abs(actual-expected)<1e-10
    transfer_zero_mae = float(held.assign(zero_error=held.dpsi_mean.abs()).groupby('peptide_id').zero_error.mean().mean())
    assert abs(transfer_zero_mae-saved['transfer']['zero_baseline']['all']['mae'])<1e-10
    transfer = {'metrics':transfer_metrics,'zero_mae':transfer_zero_mae,
        'only_mutant_amino_acids':['A','R','S'],'label':'dpsi_rep1',
        'groups_disjoint_from_W_and_scan_dev':True,'not_external_independent_lab':True,
        'lora_not_evaluated_on_T':True}
    history = {}
    for path in CAMPAIGN.parent.glob('*/state.json'):
        old = read(path); starts = [r['started_unix'] for r in old['jobs'].values() if 'started_unix' in r]
        history[path.parent.name] = {'counts':dict(Counter(r['status'] for r in old['jobs'].values())),
            'latest_recorded_job_start_local':datetime.fromtimestamp(max(starts),TZ).isoformat(),
            'filesystem_mtime_local':datetime.fromtimestamp(path.stat().st_mtime,TZ).isoformat(),
            'warning':'Copied files mtime is not the execution time; starts come from saved job records.'}
    result = {
        'generated_local':datetime.now(TZ).isoformat(), 'analysis':'independent_read_only_saved_artifact_audit',
        'scope':'Saved local campaign copy accessible in Linux; no live observation of original Windows runtime.',
        'script_sha256':digest(Path(__file__)), 'repository_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'data_identity':data_identity, 'data_manifest_files_verified':len(data_checks),
        'state_counts':dict(Counter(r['status'] for r in state['jobs'].values())),
        'local_artifacts_verified':len(checked),'local_bytes_verified':sum(checked.values()),
        'kaggle_artifacts_verified':len(kchecked),'kaggle_bytes_verified':sum(kchecked.values()),
        'inherited_complete_jobs_counted_once':inherited,'saved_analysis_sources_checked':len(saved['source_files']),
        'saved_analysis_sources_exact_byte_matches':len(saved['source_files'])-len(newline_reconciliations),
        'saved_analysis_source_newline_reconciliations':newline_reconciliations,
        'session':read(CAMPAIGN/'session.json'),'history':history,'split_role_checks':split_checks,
        'recipe_metrics':recipes,'core_diagnostics':diagnostics,'matched_lora_minus_frozen':contrasts,
        'nested_choice_argmin_verified':len(nested),'tuning_fits':adapter_fits,'calibration':calibration,'transfer':transfer,
        'diagnostic_status':'Posthoc descriptive development analysis; no causal mechanism, clinical result, or new independent test.',
        'limits':['No retraining or model deserialization; fit.json records, not direct tensor comparisons, verify adapter-change declarations.',
                  'No new MMseqs2 search; data manifest and split-role checks verify saved bundle, not completeness of homology grouping.',
                  'Confidence intervals remain the hash-verified saved cluster-bootstrap results; residual subgroup tables have no new significance tests.',
                  'Outer OOF has been inspected for many recipes; it is development evidence, not an untouched test.',
                  'Portability: original analyzer uses Windows artifact paths and a data folder absent by that name on Linux; this audit maps existing campaign basenames and verifies the actual v3-fullpsi bundle hash without modifying originals.']}
    (HERE/'source-inventory.json').write_text(json.dumps(clean({'generated_local':result['generated_local'],'files':SOURCES}),indent=2,ensure_ascii=False)+'\n')
    (HERE/'local-audit.json').write_text(json.dumps(clean(result),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print('PASS all checks; wrote local-audit.json and source-inventory.json',flush=True)


if __name__ == '__main__':
    main()
