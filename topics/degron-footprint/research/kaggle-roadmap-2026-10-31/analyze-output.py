"""Audit saved official OOF predictions without loading model checkpoints.

Run from the repository root with Python, pandas, pyarrow, scipy and sklearn.
This writes derived analysis only; it never modifies the imported output tree.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # permit python -I while importing this reviewed runner

import numpy as np
import pandas as pd

from degron_v3.metrics import paired_ci, per_peptide


METRICS = ['mae', 'rmse', 'spearman', 'auroc_plus', 'auprc_plus',
           'auroc_minus', 'auprc_minus']
META = ['peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']


def summary(rows):
    def report(sub):
        result = dict(peptides=len(sub), clusters=sub.group_id.nunique(),
                      cells=int(sub.n.sum()))
        for metric in METRICS:
            values = sub[metric].dropna()
            result[metric] = float(values.mean()) if len(values) else None
            result[metric + '_eligible_peptides'] = len(values)
        for event in ['plus', 'minus']:
            eligible = sub[sub['auroc_' + event].notna()]
            result['event_rate_' + event + '_eligible_macro'] = float(
                eligible['event_rate_' + event].mean()) if len(eligible) else None
            result['event_rate_' + event + '_all_macro'] = float(
                sub['event_rate_' + event].mean())
            for fraction in [.05, .1, .2]:
                for metric in ['precision', 'enrichment']:
                    key = f'{metric}_{event}_{fraction}'
                    values = eligible[key].dropna()
                    result[key + '_eligible_macro'] = float(values.mean()) if len(values) else None
        return result
    return dict(all=report(rows), strata={str(k): report(sub)
                for k, sub in rows.groupby('psi_stratum', observed=True)})


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, default=HERE / 'output/official/369cb2fe6a1e31e0')
    parser.add_argument('--destination', type=Path, default=HERE / 'output-analysis.json')
    args = parser.parse_args()
    root = args.run.resolve()
    manifest = json.loads((root / 'pipeline-manifest.json').read_text(encoding='utf8'))
    assert manifest['plan']['mode'] == 'official'
    identity = manifest['plan']['data_identity']
    entries = [entry for task in manifest['tasks'].values() for entry in task.get('files', [])]
    mismatches = []
    for entry in entries:
        path = root / entry['path']
        if not path.is_file() or path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
            mismatches.append(entry['path'])
    assert not mismatches, mismatches
    print(f'Verified {len(entries)} files against the saved manifest.', flush=True)

    grouped = defaultdict(list)
    reported = defaultdict(dict)
    for task in manifest['tasks'].values():
        if task['status'] != 'complete':
            continue
        task_root = root / task['path']
        allowed = {entry['path'] for entry in task['files']}
        for path in sorted(task_root.glob('*-oof.parquet')):
            assert path.relative_to(root).as_posix() in allowed
            grouped[path.name.removesuffix('-oof.parquet')].append(path)
        for path in task_root.glob('*-results.json'):
            result = json.loads(path.read_text(encoding='utf8'))
            recipe = path.name.removesuffix('-results.json')
            if 'per_seed' in result:
                reported[recipe].update({seed: r['all'] for seed, r in result['per_seed'].items()})
            else:
                seeds = json.loads((task_root / 'run-manifest.json').read_text(encoding='utf8'))['config']['seeds']
                if len(seeds) == 1:
                    reported[recipe][str(seeds[0])] = result['all']

    reference = None
    per_recipe = {}
    peptide_tables = {}
    for recipe, paths in sorted(grouped.items()):
        frame = pd.concat([pd.read_parquet(path) for path in paths], ignore_index=True)
        assert set(frame['mode']) == {'official'}
        assert set(frame.data_identity) == {identity}
        assert not frame.duplicated(['seed', 'cell_id']).any(), recipe
        assert np.isfinite(frame.prediction).all(), recipe
        seeds = sorted(int(seed) for seed in frame.seed.unique())
        seed_mae = {}
        for seed, rows in frame.groupby('seed', sort=True):
            meta = rows.set_index('cell_id')[META].sort_index()
            if reference is None:
                reference = meta
                assert len(reference) == 122412
                assert reference.peptide_id.nunique() == 235
                assert reference.group_id.nunique() == 221
                assert reference.groupby('group_id').outer_fold.nunique().max() == 1
            pd.testing.assert_frame_equal(meta, reference, check_dtype=False, check_exact=True)
            error = np.abs(rows.prediction.to_numpy() - rows.dpsi_mean.to_numpy())
            mae = float(pd.Series(error).groupby(rows.peptide_id.to_numpy()).mean().mean())
            seed_mae[str(seed)] = mae
            if str(seed) in reported[recipe]:
                assert abs(mae - reported[recipe][str(seed)]['mae']) < 1e-10
        ensemble = frame.groupby('cell_id', sort=True).prediction.mean().reindex(reference.index)
        pp = per_peptide(reference.reset_index(), ensemble.to_numpy())
        peptide_tables[recipe] = pp
        per_recipe[recipe] = dict(seeds=seeds, files=[str(p.relative_to(root).as_posix()) for p in paths],
                                  oof_rows=len(frame), ensemble=summary(pp), seed_mae=seed_mae,
                                  reported_per_seed=reported[recipe])
        # A result written within one task already summarizes that task's seed ensemble.
        if len(paths) == 1:
            path = paths[0].with_name(recipe + '-results.json')
            if path.exists():
                source = json.loads(path.read_text(encoding='utf8'))
                source = source.get('ensemble', source)['all']
                for metric in METRICS:
                    assert abs(source[metric] - per_recipe[recipe]['ensemble']['all'][metric]) < 1e-10
        print(recipe, 'seeds', seeds, 'MAE', round(float(pp.mae.mean()), 6), flush=True)

    zero = per_peptide(reference.reset_index(), np.zeros(len(reference)))
    contrasts = {}

    def contrast(a, b, metric='mae', stratum=None, multiplicity=1, family='exploratory'):
        left, right = peptide_tables[a], peptide_tables[b]
        if stratum:
            left = left[left.psi_stratum == stratum]
            right = right[right.psi_stratum == stratum]
        key = f'{a} minus {b}; {metric}' + (f'; {stratum}' if stratum else '')
        contrasts[key] = dict(a=a, b=b, metric=metric, stratum=stratum, family=family,
                             prediction_aggregation='mean_of_available_seeds',
                             **paired_ci(left, right, metric, multiplicity=multiplicity))

    for arm in 'DE':
        contrast('ordered-w5-' + arm, 'ordered-w5-B', multiplicity=2, family='Q1_prespecified')
        contrast('ordered-w5-' + arm, 'ordered-w5-B', 'auroc_plus', 'le3', family='Q1_guardrail_descriptive')
    for a, b, family in [
        ('nested-family-selection', 'ordered-w5-D', 'Q2_selection_procedure'),
        ('esm2_35m-context-D', 'ordered-w5-D', 'development_fixed_recipe'),
        ('esm2_35m-only-D', 'ordered-w5-D', 'development_fixed_recipe'),
        ('esm2_35m-cnn-D', 'esm2_35m-pointwise-D', 'Q3_D_descriptive'),
        ('esm2_35m-cnn-B', 'esm2_35m-pointwise-B', 'Q3_B_descriptive'),
        ('onehot-cnn-D', 'onehot-pointwise-D', 'head_control'),
        ('esm2_35m-mcnn-D', 'esm2_35m-cnn-D', 'secondary_head'),
        ('esm2_35m-cnn-D', 'onehot-cnn-D', 'representation_control'),
        ('esm2_35m-cnn-D', 'ordered-w5-D', 'development_fixed_recipe'),
        ('sat-quality-D', 'sat-only-D', 'scanning_exploratory'),
        ('scan-rep1-D', 'sat-only-D', 'scanning_exploratory'),
        ('cnn-transfer-dpsi_rep1-D', 'cnn-transfer-scratch-D', 'scanning_exploratory'),
        ('cnn-transfer-dpsi_rep12_mean-D', 'cnn-transfer-scratch-D', 'scanning_exploratory'),
        ('cnn-transfer-dpsi_rep12_mean-D', 'cnn-transfer-dpsi_rep1-D', 'replicate_exploratory'),
        ('cnn-transfer-dpsi_rep1-D', 'esm2_35m-cnn-D', 'development_fixed_recipe'),
    ]:
        contrast(a, b, family=family)
        contrast(a, b, metric='auroc_plus', family=family)

    completed = [v for v in manifest['tasks'].values() if v['status'] == 'complete']
    seconds = {}
    for key, task in manifest['tasks'].items():
        status_file = root / task['path'] / 'status.json'
        if status_file.exists():
            seconds[key] = json.loads(status_file.read_text(encoding='utf8'))['seconds']
    result = dict(
        generated_utc=datetime.now(timezone.utc).isoformat(),
        plan_id=manifest['plan_id'], source='output/official/' + root.name,
        source_manifest_sha256=digest(root / 'pipeline-manifest.json'),
        data_identity=identity, source_updated_utc=manifest['updated_utc'],
        scientific_status=manifest['scientific_status'],
        integrity=dict(files_checked=len(entries), bytes_checked=sum(e['bytes'] for e in entries),
                       mismatches=mismatches, oof_files=sum(map(len, grouped.values())),
                       oof_recipes=len(grouped), labels_and_fold_metadata_match=True,
                       unique_cells_per_seed=len(reference)),
        task_status_counts=dict(Counter(t['status'] for t in manifest['tasks'].values())),
        completed_sections=sorted(set(t['section'] for t in completed)),
        incomplete_tasks={key: val['status'] for key, val in manifest['tasks'].items() if val['status'] != 'complete'},
        completed_task_seconds=seconds, baseline_zero=summary(zero), recipes=per_recipe,
        contrasts=contrasts,
        notes=[
            'All reported ensemble metrics are recomputed from mean per-cell predictions, including split stage05 jobs.',
            'Stage11 frozen has only seed17; do not compare it as a three-seed ensemble.',
            'Q1 adjusted intervals are 97.5%; other contrasts are descriptive 95% intervals without a global multiplicity correction.',
            'Seed variation is not an independent-sample statistical confidence interval.',
            'Model ranking is development analysis, not independent confirmation or automatic G2/G3 closure.',
            'A running entry in an imported manifest does not prove the remote process is currently alive.',
        ])
    args.destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf8')
    print('Saved', args.destination, flush=True)


if __name__ == '__main__':
    main()
