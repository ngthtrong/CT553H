"""New fitted mutation-effect predictors, with train-only transforms and OOF output."""
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from .common import SEEDS, atomic_json
from .data import arm_mask, balanced_weights
from .features import features
from .metrics import per_peptide, summarize, paired_ci


class FittedRidge:
    def __init__(self, alpha, pca_k=0, seed=17):
        self.alpha, self.pca_k, self.seed = alpha, pca_k, seed

    def fit(self, X, y, w=None):
        self.scaler = StandardScaler().fit(X, sample_weight=w)
        Z = self.scaler.transform(X)
        self.pca = None
        if self.pca_k:
            rng = np.random.default_rng(self.seed)
            sample = rng.choice(len(Z), min(len(Z), 20000), replace=False)
            self.pca = PCA(n_components=min(self.pca_k, len(sample)-1, Z.shape[1]),
                           svd_solver='randomized', random_state=self.seed).fit(Z[sample])
            Z = self.pca.transform(Z)
        self.model = Ridge(alpha=self.alpha).fit(Z, y, sample_weight=w)
        return self

    def predict(self, X):
        return self.model.predict(self._transform(X))

    def _transform(self, X):
        Z = self.scaler.transform(X)
        if self.pca is not None:
            Z = self.pca.transform(Z)
        return Z


class CombinedRidge:
    """PCA applies only to pLM features; the linear context block stays intact."""
    def __init__(self, alpha, n_context, pca_k=64, seed=17):
        self.alpha, self.n_context, self.pca_k, self.seed = alpha, n_context, pca_k, seed

    def _transform(self, X):
        blocks = []
        if self.n_context:
            blocks.append(self.context_scaler.transform(X[:, :self.n_context]))
        if X.shape[1] > self.n_context:
            delta = self.plm_scaler.transform(X[:, self.n_context:])
            blocks.append(self.pca.transform(delta))
        return np.concatenate(blocks, axis=1)

    def fit(self, X, y, w=None):
        if self.n_context:
            self.context_scaler = StandardScaler().fit(X[:, :self.n_context], sample_weight=w)
        if X.shape[1] > self.n_context:
            self.plm_scaler = StandardScaler().fit(X[:, self.n_context:], sample_weight=w)
            rng = np.random.default_rng(self.seed)
            sample = rng.choice(len(X), min(len(X), 20000), replace=False)
            delta = self.plm_scaler.transform(X[sample, self.n_context:])
            self.pca = PCA(n_components=min(self.pca_k, len(delta)-1, delta.shape[1]),
                           svd_solver='randomized', random_state=self.seed).fit(delta)
        self.model = Ridge(alpha=self.alpha).fit(self._transform(X), y, sample_weight=w)
        return self

    def predict(self, X):
        return self.model.predict(self._transform(X))


def train_oof(ds, frame, X, out, recipe, arm='D', seed_list=SEEDS, alphas=(.1, 1., 10., 100., 1000.),
              n_context=None, pca_k=0, smoke=False, quality=False, extra_scan=None, train_fraction=1.):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    frame = frame.reset_index(drop=True)
    y = frame.dpsi_mean.to_numpy(float)
    chosen = arm_mask(frame, arm)
    predictions = []
    info = []
    def make(alpha, seed):
        return FittedRidge(alpha, seed=seed) if n_context is None else CombinedRidge(alpha, n_context, pca_k, seed)
    def subset(rows, seed):
        if train_fraction == 1.:
            return rows
        import hashlib
        groups = sorted(set(frame.group_id.iloc[rows]), key=lambda g: hashlib.sha256(f'{seed}:{g}'.encode()).hexdigest())
        selected = set(groups[:max(1, int(np.ceil(len(groups)*train_fraction)))])
        return rows[frame.group_id.iloc[rows].isin(selected).to_numpy()]
    for seed in seed_list:
        pred = np.full(len(frame), np.nan)
        for fold in sorted(frame.outer_fold.unique()):
            checkpoint = out / f'{recipe}-seed{seed}-fold{fold}.joblib'
            saved = checkpoint.with_suffix('.json')
            role = ds.role(frame, int(fold), seed)
            tr = subset(np.flatnonzero((role == 'train') & chosen), seed)
            va = np.flatnonzero(role == 'validation')
            te = np.flatnonzero(role == 'test')
            if not len(te):
                continue
            if min(len(tr), len(va)) == 0:
                raise ValueError(f'Empty train/validation fold {fold}, arm {arm}; do not bypass gate')
            assert not set(frame.group_id.iloc[tr]) & set(frame.group_id.iloc[te])
            assert not set(frame.group_id.iloc[va]) & set(frame.group_id.iloc[te])
            def fit_rows(rows):
                weight = balanced_weights(frame.iloc[rows]) if arm == 'E' else np.ones(len(rows))
                if quality:
                    # Robust train-only scale/cap; test disagreement is never read to fit weights.
                    disagreement = frame.iloc[rows].replicate_disagreement.to_numpy(float)
                    scale = max(float(np.median(disagreement)), .05)
                    weight *= np.clip(1/(1+(disagreement/scale)**2), .1, 1.)
                xx, yy = X[rows], y[rows]
                if extra_scan is not None:
                    sf, sx, sy, source_weight = extra_scan
                    sr = ds.role(sf, int(fold), seed)
                    keep = (sr == 'train') & np.isfinite(sy)
                    assert not set(sf.group_id[keep]) & set(frame.group_id.iloc[np.r_[va, te]])
                    xx = np.concatenate([xx, sx[keep]])
                    yy = np.concatenate([yy, sy[keep]])
                    weight = np.r_[weight, np.full(keep.sum(), source_weight)]
                return xx, yy, weight/weight.mean()
            if checkpoint.exists() and saved.exists():
                metadata = json.loads(saved.read_text())
                assert metadata['data_identity'] == ds.identity and metadata['recipe'] == recipe
                model = joblib.load(checkpoint)  # trusted local generated artifact only
            else:
                tx, ty, w = fit_rows(tr)
                # Fit train-only transforms once, not a fresh PCA for every alpha.
                candidate = make(alphas[0], seed).fit(tx, ty, w)
                ztrain, zval = candidate._transform(tx), candidate._transform(X[va])
                scores = []
                for alpha in alphas:
                    candidate.model = Ridge(alpha=alpha).fit(ztrain, ty, sample_weight=w)
                    scores.append(float(np.square(candidate.model.predict(zval)-y[va]).mean()))
                alpha = alphas[int(np.argmin(scores))]
                candidate.model = Ridge(alpha=alpha).fit(ztrain, ty, sample_weight=w)
                calibration = frame.iloc[va][['cell_id', 'peptide_id', 'group_id', 'dpsi_mean']].copy()
                calibration['prediction'] = candidate.model.predict(zval)
                calibration['seed'] = seed; calibration['outer_fold'] = int(fold)
                calibration.to_parquet(out / f'{recipe}-seed{seed}-fold{fold}-calibration.parquet', index=False)
                final = subset(np.flatnonzero(np.isin(role, ['train', 'validation']) & chosen), seed)
                tx, ty, w = fit_rows(final)
                model = make(alpha, seed).fit(tx, ty, w)
                metadata = dict(recipe=recipe, arm=arm, seed=seed, fold=int(fold), alpha=alpha,
                                validation_mse=min(scores), n_train=len(tr), n_validation=len(va),
                                n_refit=len(final), n_test=len(te), data_identity=ds.identity,
                                train_fraction=train_fraction,
                                training_groups=sorted(set(frame.group_id.iloc[final])),
                                pca_train_sample_cap=20000, mode='smoke' if smoke else 'official')
                joblib.dump(model, checkpoint); atomic_json(saved, metadata)
            pred[te] = model.predict(X[te]); info.append(metadata)
            print(recipe, 'seed', seed, 'fold', fold, 'alpha', metadata['alpha'], flush=True)
        assert np.isfinite(pred).all(), 'OOF predictions incomplete'
        rows = frame[['cell_id', 'peptide_id', 'group_id', 'outer_fold', 'psi_stratum', 'dpsi_mean']].copy()
        rows['prediction'] = pred; rows['seed'] = seed; rows['recipe'] = recipe
        rows['mode'] = 'smoke' if smoke else 'official'; rows['data_identity'] = ds.identity
        predictions.append(rows)
    all_predictions = pd.concat(predictions, ignore_index=True)
    all_predictions.to_parquet(out / f'{recipe}-oof.parquet', index=False)
    ensemble = all_predictions.groupby('cell_id').prediction.mean().reindex(frame.cell_id).to_numpy()
    report = dict(recipe=recipe, mode='smoke' if smoke else 'official', data_identity=ds.identity,
                  per_seed={str(s): summarize(frame, r.prediction.to_numpy())
                            for s, r in all_predictions.groupby('seed', sort=False)},
                  ensemble=summarize(frame, ensemble), fits=info)
    atomic_json(out / f'{recipe}-results.json', report)
    return all_predictions, per_peptide(frame, ensemble)


def linear_stage(ds, out, config):
    frame = ds.sample_smoke(ds.sat) if config['smoke'] else ds.sat.copy()
    results = {}; summaries = []
    for kind, radius, arm in config['linear_recipes']:
        recipe = f'{kind}-w{radius}-{arm}'
        X = features(frame, kind, radius)
        _, pp = train_oof(ds, frame, X, out, recipe, arm=arm,
                          seed_list=config['seeds'], alphas=config['alphas'], smoke=config['smoke'])
        results[recipe] = pp
        summaries.append(dict(recipe=recipe, mae=pp.mae.mean(), auroc_plus=pp.auroc_plus.mean()))
    comparisons = {}
    if 'ordered-w5-B' in results:
        for arm in ('D', 'E'):
            key = 'ordered-w5-' + arm
            if key in results:
                comparisons[key+'-B'] = paired_ci(results[key], results['ordered-w5-B'],
                    n_boot=100 if config['smoke'] else 5000, multiplicity=2)
    atomic_json(Path(out) / 'comparisons.json', comparisons)
    if config.get('learning_curves', not config['smoke']):
        for fraction in (.25, .5, .75):
            recipe = f'ordered-w5-D-fraction{fraction}'
            _, pp = train_oof(ds, frame, features(frame, 'ordered', 5), out, recipe, arm='D',
                seed_list=config['seeds'], alphas=config['alphas'], smoke=config['smoke'], train_fraction=fraction)
            summaries.append(dict(recipe=recipe, mae=pp.mae.mean(), auroc_plus=pp.auroc_plus.mean()))
    pd.DataFrame(summaries).to_csv(Path(out) / 'summary.csv', index=False)
    return pd.DataFrame(summaries)
