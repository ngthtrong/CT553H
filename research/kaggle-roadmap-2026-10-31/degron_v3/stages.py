from pathlib import Path
import hashlib
import json
import shutil
import time

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score

from .common import AAS, SEEDS, atomic_json, execution, sha256
from .data import Dataset, arm_mask, balanced_weights
from .features import features
from .learning import linear_stage, train_oof, FittedRidge, CombinedRidge
from .metrics import summarize, per_peptide, paired_ci


def audit_stage(ds, out, config):
    frame = ds.sat
    assert len(frame) == 122412 and frame.peptide_id.nunique() == 235
    assert not frame.cell_id.duplicated().any()
    assert frame[['dpsi_a', 'dpsi_b', 'dpsi_mean']].notna().all().all()
    assert np.allclose(frame.dpsi_mean, (frame.dpsi_a+frame.dpsi_b)/2, atol=1e-12)
    assert ((1-frame.psi_wt_sat-1e-9 <= frame.dpsi_mean) &
            (frame.dpsi_mean <= 6-frame.psi_wt_sat+1e-9)).all()
    assert (frame.loc[frame.psi_wt_sat > 5, 'dpsi_mean'] < 1).all()
    assert ds.wide.groupby('group_id').outer_fold.nunique().max() == 1
    scan = ds.scanning(include_held=True)
    assert not set(scan.loc[scan.partition == 'scan_T', 'group_id']) & set(frame.group_id)
    report = dict(status='pass', data_identity=ds.identity, saturation_cells=len(frame),
                  saturation_peptides=frame.peptide_id.nunique(), wide_groups=frame.group_id.nunique(),
                  scanning_cells=len(scan), mapping_missing=int(ds.peptides.group_id.isna().sum()))
    atomic_json(Path(out) / 'gates.json', report)
    summary = frame.groupby('psi_stratum', observed=True).agg(cells=('cell_id', 'size'),
            peptides=('peptide_id', 'nunique'), mean_dpsi=('dpsi_mean', 'mean'))
    summary.to_csv(Path(out) / 'data-summary.csv')
    return summary.reset_index()


def reproduce_legacy(ds, out):
    """No dependency on sklearn GroupKFold tie ordering or mutable raw input."""
    base = np.load(ds.root / 'historical/legacy-base.npz', allow_pickle=False)
    ext = np.load(ds.root / 'historical/legacy-ext4.npz', allow_pickle=False)
    folds = json.loads((ds.root / 'historical/g2-reference.json').read_text())['folds']
    new_rows = np.concatenate([np.arange(a, b) for p, (a, b) in zip(ext['peps'], ext['idx'])
                               if p not in set(base['peps'])])
    X = np.vstack([base['X'], ext['X'][new_rows]])
    y = np.r_[base['y'], ext['y'][new_rows]]
    group = np.r_[base['rowg'], ext['rowg'][new_rows]]
    predictions = {'base': [], 'ext4': []}
    for seed in SEEDS:
        ps = {k: np.zeros(len(base['y'])) for k in predictions}
        for fold in folds:
            test_groups = set(fold['test_clusters'])
            test = np.flatnonzero(np.isin(base['rowg'], list(test_groups)))
            for tag in predictions:
                limit = len(base['y']) if tag == 'base' else len(y)
                pool = np.flatnonzero(~np.isin(group[:limit], list(test_groups)))
                ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed).split(
                    pool, y[pool], group[pool]))
                tr, va = pool[ti], pool[vi]
                alpha = min((float(np.square(Ridge(alpha=a).fit(X[tr], y[tr]).predict(X[va])-y[va]).mean()), a)
                            for a in (1, 10, 100, 1000))[1]
                ps[tag][test] = Ridge(alpha=alpha).fit(X[pool], y[pool]).predict(X[test])
        for tag in predictions:
            predictions[tag].append(ps[tag])
    metrics = {}
    for tag, values in predictions.items():
        pred = np.mean(values, 0)
        scores = [roc_auc_score(base['y'][a:b] >= 1, pred[a:b]) for a, b in base['idx']
                  if len(set(base['y'][a:b] >= 1)) == 2]
        metrics[tag] = float(np.mean(scores))
    assert abs(metrics['base']-.808185975) < 1e-4 and abs(metrics['ext4']-.820822359) < 1e-4, metrics
    atomic_json(Path(out) / 'legacy-reproduction.json', dict(status='pass', metrics=metrics,
                note='Historical raw Ridge/splits, separate from new stricter W grouped evaluation.'))
    return metrics


def family_stage(ds, out, config):
    from .plm import feature_data
    frame = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.copy()
    context = features(frame, 'ordered', 5)
    candidates = config.get('pooled_features', {})
    if config['smoke']:
        rng = np.random.default_rng(17)
        candidates = {'synthetic_smoke': None}
    assert candidates, 'Attach complete pooled feature bundles and set POOLED_FEATURES'
    summaries, candidate_paths = [], []
    for model_id, path in candidates.items():
        delta = rng.normal(size=(len(frame), 16)).astype('float32') if path is None else feature_data(
            path, frame, ds.identity, config['smoke'])[0]
        for arm in config.get('family_arms', ['B', 'D']):
            for include_context in (False, True):
                X = np.concatenate([context, delta], 1) if include_context else delta
                n_context = context.shape[1] if include_context else 0
                recipe = f'{model_id}-'+('context-' if include_context else 'only-')+arm
                predictions, pp = train_oof(ds, frame, X, out, recipe, arm,
                    seed_list=config['seeds'], alphas=config['alphas'], n_context=n_context,
                    pca_k=64, smoke=config['smoke'])
                candidate_paths.append((recipe, predictions))
                summaries.append(dict(recipe=recipe, mae=pp.mae.mean(), auroc_plus=pp.auroc_plus.mean()))
    # Select each outer-fold/seed recipe by its inner-validation loss, never outer outcomes.
    nested = []
    selected = []
    for seed in config['seeds']:
        for fold in sorted(frame.outer_fold.unique()):
            options = []
            for recipe, predictions in candidate_paths:
                info = json.loads((Path(out) / f'{recipe}-seed{seed}-fold{fold}.json').read_text())
                options.append((info['validation_mse'], recipe, predictions))
            loss, recipe, prediction = min(options, key=lambda v: (v[0], v[1]))
            rows = prediction[(prediction.seed == seed) & (prediction.outer_fold == fold)].copy()
            rows['selected_recipe'] = recipe; rows['recipe'] = 'nested-family-selection'
            nested.append(rows); selected.append(dict(seed=seed, fold=int(fold), recipe=recipe, validation_mse=loss))
    pd.concat(nested).to_parquet(Path(out) / 'nested-family-selection-oof.parquet', index=False)
    atomic_json(Path(out) / 'nested-selection.json', dict(data_identity=ds.identity, choices=selected,
        note='Evaluates the selection procedure; not a claim that one fixed family won on independent data.'))
    return pd.DataFrame(summaries)


def scanning_stage(ds, out, config):
    frame = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.copy()
    scan = ds.scanning()
    scan = scan[scan.partition == 'scan_dev'].copy().reset_index(drop=True)
    if config['smoke']:
        scan = scan.groupby('group_id', sort=True).head(4).head(1000).copy().reset_index(drop=True)
    assert not set(scan.group_id) & set(frame.group_id), 'scan_dev expected disjoint from saturation in this transfer design'
    pair_counts = scan.availability_mask.value_counts().to_dict()
    complete = scan.dropna(subset=['dpsi_rep1', 'dpsi_rep2'])
    corr = float(complete[['dpsi_rep1', 'dpsi_rep2']].corr().iloc[0, 1]) if len(complete)>2 else None
    atomic_json(Path(out) / 'replicate-audit.json', dict(availability=pair_counts, same_cohort_rows=len(complete),
        pearson=corr, note='Replicates remain separate; BAG6 WT is excluded.'))
    scan = complete.copy().reset_index(drop=True)  # identical cohort for rep1 versus mean12
    sx = features(scan, 'ordered', 5); x = features(frame, 'ordered', 5)
    # Source indicator is an explicit input for assay/batch correction, not biological PSI metadata.
    x = np.column_stack([x, np.zeros(len(x))]); sx = np.column_stack([sx, np.ones(len(sx))])
    summaries = []
    for recipe, quality, target in [('sat-only-D', False, None), ('sat-quality-D', True, None),
                                    ('scan-rep1-D', False, 'dpsi_rep1'), ('scan-mean12-D', False, 'dpsi_rep12_mean')]:
        extra = None if target is None else (scan, sx, scan[target].to_numpy(float), .1)
        _, pp = train_oof(ds, frame, x, out, recipe, arm='D', seed_list=config['seeds'],
            alphas=config['alphas'], smoke=config['smoke'], quality=quality, extra_scan=extra)
        summaries.append(dict(recipe=recipe, mae=pp.mae.mean(), auroc_plus=pp.auroc_plus.mean()))
    atomic_json(Path(out) / 'pair-diagnostic-spec.json', dict(scan_pairs=sorted(set(scan.scan_pair)),
        note='Use saved cell OOF with these pair IDs for same-cohort 20/360 diagnostics; report eligibility.'))
    if config.get('scan_neural_transfer', True):
        from .neural import scanning_neural_stage
        neural_results = scanning_neural_stage(ds, out, config)
        summaries += neural_results.to_dict('records')
    return pd.DataFrame(summaries)


def event_labels(y):
    return np.where(np.asarray(y) <= -1, 0, np.where(np.asarray(y) >= 1, 2, 1))


def probability(calibrator, prediction):
    out = np.zeros((len(prediction), 3))
    out[:, calibrator.classes_.astype(int)] = calibrator.predict_proba(np.asarray(prediction).reshape(-1, 1))
    assert np.allclose(out.sum(1), 1.)
    return out


def calibration_stage(ds, out, config):
    source = Path(config['training_output'])
    recipe = config.get('selected_recipe', 'ordered-w5-D')
    raw = pd.read_parquet(source / f'{recipe}-oof.parquet')
    assert set(raw.data_identity) == {ds.identity}
    assert set(raw['mode']) == ({'smoke'} if config['smoke'] else {'official'})
    # Selection lock is written before loading held-source labels.
    lock = dict(data_identity=ds.identity, recipe=recipe, model_ids=config.get('selected_model_ids', []),
                training_output=str(source), input_oof_sha256=sha256(source / f'{recipe}-oof.parquet'),
                mode='smoke' if config['smoke'] else 'official', event_labels=['minus', 'neutral', 'plus'])
    atomic_json(Path(out) / 'selection-lock.json', lock)
    calibrated = []
    for (seed, fold), rows in raw.groupby(['seed', 'outer_fold']):
        path = source / f'{recipe}-seed{seed}-fold{fold}-calibration.parquet'
        inner = pd.read_parquet(path)
        assert not set(inner.group_id) & set(rows.group_id)
        classes = event_labels(inner.dpsi_mean)
        if len(np.unique(classes)) < 2:
            raise ValueError('Calibration inner population has fewer than two classes')
        cal = LogisticRegression(C=1., max_iter=1000).fit(inner[['prediction']].to_numpy(), classes)
        probs = probability(cal, rows.prediction.to_numpy())
        rr = rows.copy()
        for i, name in enumerate(['p_minus', 'p_neutral', 'p_plus']):
            rr[name] = probs[:, i]
        calibrated.append(rr)
    calibrated = pd.concat(calibrated)
    calibrated.to_parquet(Path(out) / 'calibrated-oof.parquet', index=False)
    mean = calibrated.groupby('cell_id')[['prediction', 'p_minus', 'p_neutral', 'p_plus']].mean()
    observed = ds.sat.set_index('cell_id').loc[mean.index]
    yclass = event_labels(observed.dpsi_mean)
    brier = float(np.square(mean[['p_minus', 'p_neutral', 'p_plus']].to_numpy()-np.eye(3)[yclass]).sum(1).mean())
    summary = dict(multiclass_brier=brier, oof_cells=len(mean), recipe=recipe,
                   note='Outer-fold calibrator trained only on that fold inner-validation predictions. Missing classes get zero probability.')
    # Final cross-fit calibration learns from development OOF; no held-source observations enter fit.
    final_cal = LogisticRegression(C=1., max_iter=1000).fit(mean[['prediction']].to_numpy(), yclass)
    joblib.dump(final_cal, Path(out) / 'final-calibrator.joblib')
    if recipe.startswith('ordered-w5-'):
        arm = recipe.rsplit('-', 1)[1]
        population = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat
        train = population.loc[arm_mask(population, arm)].copy()
        alpha_values = [json.loads(p.read_text())['alpha'] for p in source.glob(f'{recipe}-seed*-fold*.json')]
        assert alpha_values
        alpha = sorted(alpha_values)[len(alpha_values)//2]
        weights = balanced_weights(train) if arm == 'E' else None
        model = FittedRidge(alpha).fit(features(train, 'ordered', 5), train.dpsi_mean.to_numpy(), weights)
        joblib.dump(model, Path(out) / 'final-model.joblib')
        # Even in smoke, keep the explicit T read after the selection lock and restrict the rows.
        held = ds.scanning(include_held=True)
        held = held[(held.partition == 'scan_T') & held.dpsi_rep1.notna()].copy()
        if config['smoke']:
            held = held.groupby('peptide_id', sort=True).head(8).head(80).copy()
        held['dpsi_mean'] = held.dpsi_rep1
        # Strata belong to scanning WT, never to an unseen saturation PSI.
        peptide_index = ds.peptides.set_index('peptide_id')
        held['psi_stratum'] = held.peptide_id.map(peptide_index.psi_wt_scan_rep1).map(
            lambda v: 'le3' if v <= 3 else 'gt3_le4' if v <= 4 else 'gt4_le5' if v <= 5 else 'gt5')
        start = time.monotonic(); p = model.predict(features(held, 'ordered', 5)); elapsed = time.monotonic()-start
        probs = probability(final_cal, p)
        held['prediction'] = p
        for i, name in enumerate(['p_minus', 'p_neutral', 'p_plus']):
            held[name] = probs[:, i]
        held.to_parquet(Path(out) / 'held-scanning.parquet', index=False)
        summary.update(held=summarize(held, p), inference_seconds=elapsed,
                       final_alpha=float(alpha), arm=arm, trained_cells=len(train))
    else:
        summary['final_promotion_status'] = 'calibrated_cv_only_use_architecture_specific_final_refit_before_serving'
    atomic_json(Path(out) / 'model-card.json', {**lock, **summary,
        'claim_boundary': 'Reporter mutation effects; development plus previously explored same-lab transfer, not clinical validation.'})
    return pd.DataFrame([dict(recipe=recipe, multiclass_brier=brier, cells=len(mean))])


def external_stage(ds, out, config):
    source = config.get('external_table')
    if not source:
        atomic_json(Path(out) / 'external-audit.json', dict(status='source_pending',
            required=['experimental table', 'assay and units', 'WT/mutant sequence', 'source manifest', 'mapping and overlap audit'],
            not_training_or_validation=True))
        return pd.DataFrame([dict(status='source_pending', detail='Attach a reviewed external table; none was fabricated')])
    path = Path(source)
    frame = pd.read_parquet(path) if path.suffix == '.parquet' else pd.read_csv(path)
    required = {'peptide_id', 'wt_sequence', 'position_1based', 'mut_aa', 'effect', 'assay_id', 'units', 'source_id'}
    assert required <= set(frame), sorted(required-set(frame))
    assert np.isfinite(frame.effect).all() and not frame[['wt_sequence']].isna().any().any()
    overlap = set(frame.wt_sequence) & set(ds.peptides.wt_sequence)
    report = dict(status='audited_not_pooled', rows=len(frame), peptides=frame.peptide_id.nunique(),
        lengths=frame.wt_sequence.str.len().value_counts().to_dict(), exact_wt_overlap=len(overlap),
        units=sorted(frame.units.unique()), assay_ids=sorted(frame.assay_id.unique()),
        note='Different lengths/endpoints require a source protocol; no automatic padding or relabeling.')
    atomic_json(Path(out) / 'external-audit.json', report)
    return pd.DataFrame([dict(rows=len(frame), exact_wt_overlap=len(overlap), status=report['status'])])


def structure_stage(ds, out, config):
    source = config.get('structure_table')
    if not source:
        atomic_json(Path(out) / 'structure-audit.json', dict(status='structure_pending',
            required=['peptide_id', 'combined_sequence', 'structure_source', 'structure_sha256', 'chain_residue_map'],
            note='SaProt weights alone are not structural ground truth; no WT 3Di tokens fabricated.'))
        return pd.DataFrame([dict(status='structure_pending')])
    structure = pd.read_parquet(source)
    assert {'peptide_id', 'combined_sequence', 'structure_source', 'structure_sha256', 'chain_residue_map'} <= set(structure)
    assert not structure.peptide_id.duplicated().any()
    for _, row in structure.iterrows():
        assert len(row.combined_sequence) == 56
        wt = ds.peptides.set_index('peptide_id').loc[row.peptide_id, 'wt_sequence']
        assert row.combined_sequence[::2] == wt
        assert set(row.combined_sequence[1::2]) <= set('acdefghiklmnpqrstvwy#'), 'Invalid 3Di alphabet'
    assert any(s[1::2].replace('#', '') for s in structure.combined_sequence), 'True structure arm needs observed 3Di tokens'
    structure.to_parquet(Path(out) / 'audited-structure-input.parquet', index=False)
    atomic_json(Path(out) / 'structure-audit.json', dict(status='mapping_pass', peptides=len(structure),
        structure_table_sha256=sha256(source),
        note='Static WT 3Di is reused for each mutant; validity for isolated reporter peptides remains an assumption.'))
    if not config.get('run_saprot', False):
        return pd.DataFrame([dict(status='mapping_pass_training_opt_in', peptides=len(structure))])
    from .plm import extract, feature_data
    frame = ds.sat[ds.sat.peptide_id.isin(structure.peptide_id)].copy().reset_index(drop=True)
    if config['smoke']:
        raise ValueError('SaProt true/masked training requires official mode and a reviewed real structure table')
    frame['combined_sequence'] = frame.peptide_id.map(structure.set_index('peptide_id').combined_sequence)
    model_id = config.get('saprot_model', 'saprot_35m')
    summaries = []
    # Sequence-only baseline shares exactly the mapped cohort and the original W roles.
    _, pp = train_oof(ds, frame, features(frame, 'ordered', 5), out, 'structure-cohort-w5-D',
        arm='D', seed_list=config['seeds'], alphas=config['alphas'])
    summaries.append(dict(recipe='structure-cohort-w5-D', mae=pp.mae.mean()))
    for arm in ('true', 'masked'):
        combined = frame.copy()
        wt = combined.combined_sequence if arm == 'true' else combined.wt_sequence.map(lambda s: ''.join(a+'#' for a in s))
        combined['wt_sequence'] = wt
        combined['mutant_sequence'] = [s[:2*(p-1)]+a+s[2*(p-1)+1:]
            for s, p, a in zip(wt, combined.position_1based, combined.mut_aa)]
        feature_out = Path(out)/('saprot-'+arm+'-features')
        extract(ds, model_id, config['weight_roots'], feature_out,
            dict(config, row_scope='sat', row_start=0, row_stop=None, crop=False), frame_override=combined)
        delta, _ = feature_data(feature_out, frame, ds.identity)
        context = features(frame, 'ordered', 5)
        X = np.concatenate([context, delta], 1)
        recipe = f'{model_id}-{arm}-cohort-D'
        _, pp = train_oof(ds, frame, X, out, recipe, arm='D', seed_list=config['seeds'],
            alphas=config['alphas'], n_context=context.shape[1], pca_k=64)
        summaries.append(dict(recipe=recipe, mae=pp.mae.mean()))
    return pd.DataFrame(summaries)


def aggregate_stage(ds, out, config):
    source = Path(config['results_root'])
    files = sorted(source.rglob('*-oof.parquet'))
    mode = 'smoke' if config['smoke'] else 'official'
    records = []
    for path in files:
        if Path(out) in path.parents:
            continue
        data = pd.read_parquet(path)
        if not {'recipe', 'mode', 'data_identity', 'prediction', 'cell_id'} <= set(data):
            continue
        if set(data['mode']) != {mode} or set(data.data_identity) != {ds.identity}:
            continue
        mean = data.groupby('cell_id').prediction.mean()
        frame = ds.sat[ds.sat.cell_id.isin(mean.index)]
        if not config['smoke']:
            assert len(frame) == len(ds.sat), f'Incomplete official OOF: {path}'
        pp = per_peptide(frame, mean.reindex(frame.cell_id).to_numpy())
        records.append(dict(recipe=data.recipe.iloc[0], source=str(path), oof_sha256=sha256(path),
            cells=len(frame), peptides=frame.peptide_id.nunique(), clusters=frame.group_id.nunique(),
            macro_mae=float(pp.mae.mean()), macro_auroc_plus=float(pp.auroc_plus.mean()) if pp.auroc_plus.notna().any() else None))
    atomic_json(Path(out) / 'evidence.json', dict(mode=mode, data_identity=ds.identity, results=records,
        note='Same dataset identity/mode required. Candidate tables are development; nested selection and locked transfer remain separate.'))
    return pd.DataFrame(records)


def run(stage, data_root, out, config):
    stage = str(stage).zfill(2)
    ds = Dataset(data_root)
    config = dict(config, data_identity=ds.identity)
    config['protocol_sha256'] = sha256(Path(__file__).resolve().parents[1]/'EXECUTION-PROTOCOL.md')
    with execution(out, stage, config):
        if stage == '00':
            result = audit_stage(ds, out, config)
            if config.get('reproduce_legacy', not config['smoke']):
                reproduce_legacy(ds, out)
        elif stage == '01':
            result = linear_stage(ds, out, config)
        elif stage == '02':
            from .plm import preflight
            result = preflight(config['model_ids'], config['weight_roots'], out, config['smoke'])
        elif stage == '03':
            from .plm import extract
            result = pd.DataFrame([extract(ds, config['model_id'], config['weight_roots'], out, config)])
        elif stage == '04':
            result = family_stage(ds, out, config)
        elif stage == '05':
            from .neural import neural_stage
            result = neural_stage(ds, out, config)
        elif stage == '06':
            result = scanning_stage(ds, out, config)
        elif stage == '07':
            result = calibration_stage(ds, out, config)
        elif stage == '08':
            result = external_stage(ds, out, config)
        elif stage == '09':
            result = structure_stage(ds, out, config)
        elif stage == '10':
            result = aggregate_stage(ds, out, config)
        elif stage == '11':
            from .finetune import finetune_stage
            result = finetune_stage(ds, out, config)
        else:
            raise ValueError(stage)
        if isinstance(result, pd.DataFrame):
            result.to_csv(Path(out) / 'stage-summary.csv', index=False)
        return result
