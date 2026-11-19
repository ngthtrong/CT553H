"""Agreement with imported measurements over time (plan-system 4.4).

One point per saved comparison of the project (compatible endpoints only: MAE and Spearman exist only there), in time
order, with n. A point is flagged when it is clearly worse than the earlier ones; the flag is a **warning only**:
nothing changes a model or retrains anything (R-7, R-8), and the text says why a change may have other causes.
"""
from __future__ import annotations

from statistics import mean
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import AnalysisRun, Comparison

from . import workspace_store as ws

MIN_N = 5                   # points with fewer matched pairs are shown but neither flagged nor used as reference
MIN_EARLIER = 2             # earlier comparable points needed before a flag
MAE_RATIO = 1.25            # MAE above 1.25 × the mean of earlier MAEs
SPEARMAN_DROP = 0.2         # Spearman below the mean of earlier values by more than 0.2
CAVEAT = ('A worse agreement may come from another assay, conditions, replicate handling or tiles; it does not by '
          'itself mean that the model is wrong. Nothing is changed automatically.')


def series(s: Session, project_id: str) -> dict[str, Any]:
    rows = s.execute(select(Comparison, AnalysisRun.model_id, AnalysisRun.tile_index, AnalysisRun.uniprot_acc)
                     .join(AnalysisRun, AnalysisRun.analysis_id == Comparison.analysis_id)
                     .where(Comparison.project_id == project_id)
                     .order_by(Comparison.created_at, Comparison.comparison_id)).all()
    points: list[dict[str, Any]] = []
    for c, model_id, tile_index, acc in rows:
        prov = c.provenance or {}
        p: dict[str, Any] = {'comparison_id': c.comparison_id, 'analysis_id': c.analysis_id, 'dataset_id': c.dataset_id,
             'dataset_name': prov.get('dataset_name'), 'dataset_revision': prov.get('dataset_revision'),
             'model_id': model_id, 'tile': f'{acc} tile {tile_index}' if acc else 'typed tile',
             'created_at': ws.iso(c.created_at), 'n': c.matched, 'compatible': bool(c.compatible),
             'mae': c.mae, 'spearman': c.spearman, 'flags': []}
        ref = [q for q in points if q['compatible'] and q['n'] >= MIN_N]
        if p['compatible'] and p['n'] >= MIN_N and len(ref) >= MIN_EARLIER:
            maes = [q['mae'] for q in ref if q['mae'] is not None]
            sps = [q['spearman'] for q in ref if q['spearman'] is not None]
            if p['mae'] is not None and maes and p['mae'] > MAE_RATIO * mean(maes):
                p['flags'].append({'code': 'mae_worse', 'text': f"MAE {p['mae']:.3f} is above {MAE_RATIO} × the mean of "
                                   f"{len(maes)} earlier comparisons ({mean(maes):.3f})."})
            if p['spearman'] is not None and sps and p['spearman'] < mean(sps) - SPEARMAN_DROP:
                p['flags'].append({'code': 'spearman_worse', 'text': f"Spearman {p['spearman']:.3f} is more than "
                                   f"{SPEARMAN_DROP} below the mean of {len(sps)} earlier comparisons ({mean(sps):.3f})."})
        points.append(p)
    return {'project_id': project_id, 'caveat': CAVEAT, 'points': points,
            'rules': {'min_n': MIN_N, 'min_earlier': MIN_EARLIER, 'mae_ratio': MAE_RATIO, 'spearman_drop': SPEARMAN_DROP},
            'flagged': sum(1 for p in points if p['flags'])}


__all__ = ['series', 'CAVEAT']
