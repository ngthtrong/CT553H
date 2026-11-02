"""Additional posthoc diagnostics of the saved Kaggle official predictions.

Run from the repository root with Python -I, numpy, pandas, pyarrow, scipy,
and scikit-learn. Reads saturation only; does not access scan_T or checkpoints.
The base output-analysis.json must refer to the current imported manifest.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
sys.path.insert(0, str(HERE))

import numpy as np
import pandas as pd

from degron_v3.metrics import paired_ci, per_peptide


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--analysis', type=Path, default=HERE / 'output-analysis.json')
    parser.add_argument('--saturation', type=Path, default=TOPIC /
                        'data/processed/degron-data-v3-fullpsi/tables/saturation-cells.parquet')
    parser.add_argument('--destination', type=Path, default=HERE / 'output-analysis-details.json')
    args = parser.parse_args()
    analysis = json.loads(args.analysis.read_text(encoding='utf8'))
    root = HERE / analysis['source']
    assert digest(root / 'pipeline-manifest.json') == analysis['source_manifest_sha256']
    manifest = json.loads((root / 'pipeline-manifest.json').read_text(encoding='utf8'))
    assert manifest['plan']['mode'] == 'official'
    assert manifest['plan']['data_identity'] == analysis['data_identity']

    metadata = pd.read_parquet(args.saturation, columns=[
        'cell_id', 'wt_aa', 'mut_aa', 'dpsi_mean', 'group_id'])
    assert not metadata.cell_id.duplicated().any()
    metadata['pair'] = metadata.wt_aa + metadata.mut_aa
    pair_spec = root / manifest['tasks']['06']['path'] / 'pair-diagnostic-spec.json'
    scan_pairs = json.loads(pair_spec.read_text(encoding='utf8'))['scan_pairs']
    metadata['pair_cohort'] = np.where(metadata.pair.isin(scan_pairs), 'scan20', 'other360')

    keys = ['ordered-w5-D', 'esm2_35m-cnn-B', 'esm2_35m-cnn-D',
            'esm2_35m-mcnn-E', 'cnn-transfer-scratch-D', 'cnn-transfer-dpsi_rep1-D']
    peptide_tables, fold_mae, pair_tables, pair_metrics = {}, {}, {}, {}
    input_files = {}
    for recipe in keys:
        paths = [root / name for name in analysis['recipes'][recipe]['files']]
        input_files.update({path.relative_to(root).as_posix(): digest(path) for path in paths})
        frame = pd.concat([pd.read_parquet(path) for path in paths], ignore_index=True)
        assert set(frame['mode']) == {'official'}
        assert set(frame.data_identity) == {analysis['data_identity']}
        assert set(frame.seed) == {17, 29, 43}
        assert not frame.duplicated(['seed', 'cell_id']).any()
        reference = frame[frame.seed == 17].drop(columns=['seed', 'prediction']).copy()
        assert len(reference) == 122412
        for seed, rows in frame.groupby('seed'):
            columns = ['peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']
            pd.testing.assert_frame_equal(rows.set_index('cell_id')[columns].sort_index(),
                reference.set_index('cell_id')[columns].sort_index(), check_dtype=False, check_exact=True)
        reference['prediction'] = reference.cell_id.map(frame.groupby('cell_id').prediction.mean())
        assert np.isfinite(reference.prediction).all()
        reference = reference.merge(metadata, on='cell_id', suffixes=('', '_source'), validate='one_to_one')
        assert len(reference) == len(metadata)
        assert np.array_equal(reference.dpsi_mean, reference.dpsi_mean_source)
        assert np.array_equal(reference.group_id, reference.group_id_source)
        pp = per_peptide(reference, reference.prediction.to_numpy())
        peptide_tables[recipe] = pp
        with_folds = pp.merge(reference[['peptide_id', 'outer_fold']].drop_duplicates(),
                              on='peptide_id', validate='one_to_one')
        fold_mae[recipe] = with_folds.groupby('outer_fold').mae.mean().to_dict()
        if recipe in ['ordered-w5-D', 'cnn-transfer-scratch-D',
                      'cnn-transfer-dpsi_rep1-D', 'esm2_35m-cnn-D']:
            pair_metrics[recipe], pair_tables[recipe] = {}, {}
            for cohort in ['scan20', 'other360']:
                sub = reference[reference.pair_cohort == cohort]
                pp = per_peptide(sub, sub.prediction.to_numpy())
                pair_tables[recipe][cohort] = pp
                pair_metrics[recipe][cohort] = dict(cells=len(sub), pairs=sub.pair.nunique(),
                    peptides=len(pp), clusters=int(pp.group_id.nunique()), mae=float(pp.mae.mean()),
                    auroc_plus=float(pp.auroc_plus.mean()),
                    eligible_plus=int(pp.auroc_plus.notna().sum()))

    contrasts = {}
    for left, right in [('esm2_35m-mcnn-E', 'esm2_35m-cnn-D'),
                        ('esm2_35m-cnn-D', 'esm2_35m-cnn-B')]:
        for metric in ['mae', 'auroc_plus']:
            for stratum in [None, 'le3']:
                a, b = peptide_tables[left], peptide_tables[right]
                if stratum:
                    a, b = a[a.psi_stratum == stratum], b[b.psi_stratum == stratum]
                key = f'{left} minus {right}; {metric}' + (f'; {stratum}' if stratum else '')
                contrasts[key] = paired_ci(a, b, metric)
    for cohort in ['scan20', 'other360']:
        for left, right in [('cnn-transfer-dpsi_rep1-D', 'cnn-transfer-scratch-D'),
                            ('esm2_35m-cnn-D', 'ordered-w5-D')]:
            key = f'{left} minus {right}; mae; {cohort}'
            contrasts[key] = paired_ci(pair_tables[left][cohort], pair_tables[right][cohort])

    comparison = peptide_tables['esm2_35m-cnn-D'].merge(
        peptide_tables['ordered-w5-D'][['peptide_id', 'mae']],
        on='peptide_id', suffixes=('_cnn', '_ridge'))
    groups = comparison.assign(delta=comparison.mae_cnn-comparison.mae_ridge).groupby('group_id').delta.mean()
    wins = dict(cnn_better_peptides=int((comparison.mae_cnn < comparison.mae_ridge).sum()),
                total_peptides=len(comparison), cnn_better_groups=int((groups < 0).sum()), total_groups=len(groups))
    epochs = {}
    for recipe in ['esm2_35m-pointwise-D', 'esm2_35m-cnn-D', 'esm2_35m-mcnn-D']:
        values = [json.loads(path.read_text(encoding='utf8'))['epoch']
                  for path in root.glob(f'tasks/05-*/{recipe}-*-fit.json')]
        assert len(values) == 15
        epochs[recipe] = dict(count=len(values), min=min(values), max=max(values),
            median=float(np.median(values)), histogram=dict(Counter(values)))
    curves = {}
    for recipe in ['ordered-w5-D-fraction0.25', 'ordered-w5-D-fraction0.5',
                   'ordered-w5-D-fraction0.75', 'ordered-w5-D']:
        entry = analysis['recipes'][recipe]
        curves[recipe] = dict(seed_mae=entry['seed_mae'],
            mean_seed_mae=float(np.mean(list(entry['seed_mae'].values()))),
            ensemble_mae=entry['ensemble']['all']['mae'])
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(),
        source_manifest_sha256=analysis['source_manifest_sha256'],
        data_identity=analysis['data_identity'], script_sha256=digest(Path(__file__)),
        saturation_table_sha256=digest(args.saturation), oof_sha256=input_files,
        purpose='Additional posthoc development diagnostics; no held-source test access',
        methods=dict(predictions='mean per cell of seeds 17,29,43', metric='peptide-macro',
            bootstrap='5000 paired protein-group resamples, seed1729',
            intervals='descriptive CI95, no multiplicity adjustment',
            pair_cohorts='20 directed scanning substitution types vs remaining 360; no identity substitutions',
            learning_curve='Seed-specific training subsets differ; ensemble union exceeds each subset'),
        fold_mae=fold_mae, pair_diagnostics=pair_metrics, contrasts=contrasts,
        win_counts=wins, selected_epochs=epochs, learning_curve=curves)
    args.destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf8')
    print(f'Saved {args.destination}; checked {len(input_files)} OOF files, six recipes.')


if __name__ == '__main__':
    main()
