import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score


def per_peptide(frame, prediction):
    prediction = np.asarray(prediction, dtype=float)
    assert len(prediction) == len(frame) and np.isfinite(prediction).all()
    data = frame[['peptide_id', 'group_id', 'psi_stratum', 'dpsi_mean']].copy()
    data['prediction'] = prediction
    result = []
    for peptide, sub in data.groupby('peptide_id', sort=True):
        y, p = sub.dpsi_mean.to_numpy(), sub.prediction.to_numpy()
        row = dict(peptide_id=peptide, group_id=sub.group_id.iloc[0], psi_stratum=sub.psi_stratum.iloc[0],
                   n=len(y), mae=float(np.abs(p-y).mean()), rmse=float(np.sqrt(np.square(p-y).mean())))
        r = spearmanr(y, p).statistic if np.ptp(y) > 0 and np.ptp(p) > 0 else np.nan
        row['spearman'] = float(r) if np.isfinite(r) else None
        for event, label, score in [('plus', y >= 1, p), ('minus', y <= -1, -p)]:
            count = int(label.sum()); eligible = min(count, len(y)-count) >= 3
            row[f'positive_{event}'] = count
            row[f'auroc_{event}'] = float(roc_auc_score(label, score)) if eligible else None
            row[f'auprc_{event}'] = float(average_precision_score(label, score)) if eligible else None
            row[f'event_rate_{event}'] = float(label.mean())
            for fraction in (.05, .1, .2):
                k = max(1, int(np.ceil(len(y)*fraction)))
                precision = float(label[np.argsort(-score, kind='stable')[:k]].mean())
                row[f'precision_{event}_{fraction}'] = precision
                row[f'enrichment_{event}_{fraction}'] = precision/label.mean() if count else None
        result.append(row)
    return pd.DataFrame(result)


def summarize(frame, prediction):
    rows = per_peptide(frame, prediction)
    def report(sub):
        metrics = ['mae', 'rmse', 'spearman', 'auroc_plus', 'auprc_plus', 'auroc_minus', 'auprc_minus']
        out = dict(peptides=len(sub), clusters=sub.group_id.nunique(), cells=int(sub.n.sum()))
        for name in metrics:
            values = sub[name].dropna()
            out[name] = float(values.mean()) if len(values) else None
            out[name+'_eligible_peptides'] = len(values)
        return out
    return dict(all=report(rows), strata={str(s): report(r) for s, r in rows.groupby('psi_stratum')})


def paired_ci(a, b, metric='mae', n_boot=5000, seed=1729, multiplicity=1):
    pairs = a[['peptide_id', 'group_id', metric]].merge(
        b[['peptide_id', metric]], on='peptide_id', suffixes=('_a', '_b')).dropna()
    if not len(pairs):
        return dict(delta=None, ci95=None, reason='no_eligible_paired_peptides')
    pairs['delta'] = pairs[metric+'_a']-pairs[metric+'_b']
    grouped = pairs.groupby('group_id').delta.agg(['sum', 'count'])
    rng = np.random.default_rng(seed)
    sampled = rng.integers(0, len(grouped), size=(n_boot, len(grouped)))
    draws = grouped['sum'].to_numpy()[sampled].sum(1)/grouped['count'].to_numpy()[sampled].sum(1)
    q = .025 / multiplicity
    return dict(delta=float(pairs.delta.mean()), ci95=np.quantile(draws, [.025, .975]).tolist(),
                ci_adjusted=np.quantile(draws, [q, 1-q]).tolist(), multiplicity=multiplicity,
                peptides=len(pairs), clusters=len(grouped), bootstrap=n_boot)
