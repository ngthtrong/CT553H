"""Descriptive comparison of two saved analyses of one tile — usually two models (plan-system 2.2, CMP-01…03).

Read-only over the immutable snapshots: Spearman and Pearson of the raw scores, Spearman of the probabilities, mean
and largest absolute differences, the overlap of the top 10 % (k = 54, Jaccard) and the cells where the calibrated
probabilities disagree most. The probability is the common scale of two models (same event, same assay); raw scores of
different models need not share a scale, so their agreement is reported by rank (Spearman) first.

It never says which model is right: there is no observation here. A saved comparison stores metrics, disagreements
and the provenance of both sides; the per-cell table is rebuilt from the two analyses, which cannot change.
"""
from __future__ import annotations

import csv
import hashlib
import io
import uuid
from typing import Any

import numpy as np
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from db.models import AnalysisRun, ModelComparison
from degron_footprint.constants import TOP_K
from degron_footprint.errors import DomainError

from . import workspace_store as ws
from .datasets import spearman

LABEL = ('Descriptive comparison of two models (or two runs) on the same tile; it does not tell which model is right. '
         'Development benchmark, not external validation.')
N_DISAGREEMENTS = 20


def _side(run: AnalysisRun) -> dict[str, Any]:
    res, prov = run.result, run.provenance or {}
    model = prov.get('model') or {}
    return {'analysis_id': run.analysis_id, 'model_id': res['provenance']['model_id'],
            'model_kind': res['provenance'].get('model_kind'), 'weights_sha256': res['provenance']['weights_sha256'],
            'calibrator': model.get('calibrator'), 'evidence_label': res['provenance']['evidence_label'],
            'domain_status': res['domain']['status'], 'warning_codes': [w['code'] for w in res.get('warnings') or []],
            'created_at': ws.iso(run.created_at)}


def _cells(a: AnalysisRun, b: AnalysisRun) -> list[dict]:
    bb = {(c['position'], c['mut_aa']): c for c in b.result['cells']}
    out = []
    for ca in sorted(a.result['cells'], key=lambda c: (c['position'], c['mut_aa'])):
        cb = bb.get((ca['position'], ca['mut_aa']))
        if cb is None:
            continue
        out.append({'position': ca['position'], 'wt_aa': ca['wt_aa'], 'mut_aa': ca['mut_aa'],
                    'raw_a': ca['score_dpsi_raw'], 'raw_b': cb['score_dpsi_raw'],
                    'prob_a': ca['p_dpsi_ge_1_calibrated'], 'prob_b': cb['p_dpsi_ge_1_calibrated'],
                    'rank_a': ca['rank_in_tile'], 'rank_b': cb['rank_in_tile']})
    return out


def metrics_of(cells: list[dict]) -> dict[str, Any]:
    ra = np.array([c['raw_a'] for c in cells], dtype=float)
    rb = np.array([c['raw_b'] for c in cells], dtype=float)
    pa = np.array([c['prob_a'] for c in cells], dtype=float)
    pb = np.array([c['prob_b'] for c in cells], dtype=float)
    top_a = {(c['position'], c['mut_aa']) for c in cells if c['rank_a'] <= TOP_K}
    top_b = {(c['position'], c['mut_aa']) for c in cells if c['rank_b'] <= TOP_K}
    union = top_a | top_b
    pearson = None
    if len(cells) >= 3 and ra.std() > 0 and rb.std() > 0:
        pearson = float(np.corrcoef(ra, rb)[0, 1])
    return {
        'n_cells': len(cells),
        'spearman_raw': spearman(ra.tolist(), rb.tolist()),
        'pearson_raw': pearson,
        'spearman_prob': spearman(pa.tolist(), pb.tolist()),
        'mean_abs_diff_raw': float(np.mean(np.abs(ra - rb))) if len(cells) else None,
        'mean_abs_diff_prob': float(np.mean(np.abs(pa - pb))) if len(cells) else None,
        'max_abs_diff_prob': float(np.max(np.abs(pa - pb))) if len(cells) else None,
        'top_k': TOP_K,
        'top_k_overlap': len(top_a & top_b),
        'top_k_jaccard': (len(top_a & top_b) / len(union)) if union else None,
    }


def disagreements_of(cells: list[dict], n: int = N_DISAGREEMENTS) -> list[dict]:
    """Largest |P_b − P_a| first; ties by position then mutant (reproducible)."""
    ranked = sorted(cells, key=lambda c: (-abs(c['prob_b'] - c['prob_a']), c['position'], c['mut_aa']))
    return [{**c, 'diff_prob': c['prob_b'] - c['prob_a'], 'diff_raw': c['raw_b'] - c['raw_a']} for c in ranked[:n]]


def _check_pair(a: AnalysisRun, b: AnalysisRun) -> str:
    if a.analysis_id == b.analysis_id:
        raise DomainError('INVALID_REQUEST', 'Choose two different analyses.', 422, 'analysis_b')
    sa, sb = a.result['tile']['sequence'], b.result['tile']['sequence']
    if sa != sb:
        raise DomainError('INVALID_REQUEST', 'The two analyses score different tile sequences; only analyses of the '
                          'same 28-residue tile can be compared cell by cell.', 422, 'analysis_b')
    return sa


def build(a: AnalysisRun, b: AnalysisRun, comparison_id: str | None = None, created: str | None = None,
          stored: ModelComparison | None = None) -> dict:
    seq = _check_pair(a, b)
    cells = _cells(a, b)
    return {'comparison_id': comparison_id, 'project_id': a.project_id, 'label': LABEL,
            'tile': a.result['tile'], 'sequence_sha256': hashlib.sha256(seq.encode()).hexdigest(),
            'metrics': stored.metrics if stored else metrics_of(cells),
            'disagreements': stored.disagreements if stored else disagreements_of(cells),
            'provenance': stored.provenance if stored else {'a': _side(a), 'b': _side(b)},
            'cells': cells, 'created_at': created}


def compare(s: Session, a_id: str, b_id: str, save: bool) -> tuple[dict, bool]:
    a, b = ws.get_analysis(s, a_id), ws.get_analysis(s, b_id)
    out = build(a, b)
    if not save:
        return out, False
    if a.project_id != b.project_id:
        raise DomainError('INVALID_REQUEST', 'Both analyses must belong to the same project to save the comparison.',
                          422, 'analysis_b')
    ws.require_active(ws.get_project(s, a.project_id))
    t = ws.now()
    row = ModelComparison(comparison_id=str(uuid.uuid4()), project_id=a.project_id, analysis_a=a.analysis_id,
                          analysis_b=b.analysis_id, sequence_sha256=out['sequence_sha256'], metrics=out['metrics'],
                          disagreements=out['disagreements'], provenance=out['provenance'], created_at=t)
    s.add(row)
    ws.touch(s, a.project_id)
    s.flush()
    return {**out, 'comparison_id': row.comparison_id, 'created_at': ws.iso(t)}, True


def get(s: Session, comparison_id: str) -> dict:
    row = s.get(ModelComparison, comparison_id)
    if row is None:
        raise DomainError('COMPARISON_NOT_FOUND', 'No model comparison has this id.', 404)
    a, b = ws.get_analysis(s, row.analysis_a), ws.get_analysis(s, row.analysis_b)
    return build(a, b, row.comparison_id, ws.iso(row.created_at), row)


def summary(row: ModelComparison) -> dict:
    return {'comparison_id': row.comparison_id, 'project_id': row.project_id, 'analysis_a': row.analysis_a,
            'analysis_b': row.analysis_b, 'model_a': row.provenance['a']['model_id'],
            'model_b': row.provenance['b']['model_id'], 'spearman_raw': row.metrics.get('spearman_raw'),
            'top_k_jaccard': row.metrics.get('top_k_jaccard'), 'created_at': ws.iso(row.created_at)}


def list_for_project(s: Session, project_id: str, offset: int, limit: int, analysis_id: str | None = None) -> dict:
    q = select(ModelComparison).where(ModelComparison.project_id == project_id)
    if analysis_id:
        q = q.where(or_(ModelComparison.analysis_a == analysis_id, ModelComparison.analysis_b == analysis_id))
    total = int(s.scalar(select(func.count()).select_from(q.subquery())) or 0)
    rows = s.scalars(q.order_by(ModelComparison.created_at.desc(), ModelComparison.comparison_id)
                     .offset(offset).limit(limit)).all()
    return ws.page([summary(r) for r in rows], total, offset, limit)


EXPORT_COLUMNS = ['position', 'wt_aa', 'mut_aa', 'raw_a', 'raw_b', 'prob_a', 'prob_b', 'diff_prob', 'rank_a', 'rank_b']


def to_csv(data: dict) -> str:
    """Provenance of both sides as comment lines, then one row per substitution (CMP-03)."""
    out = io.StringIO()
    m, pa, pb = data['metrics'], data['provenance']['a'], data['provenance']['b']
    head = [('model_comparison_id', data['comparison_id']), ('label', LABEL),
            ('tile', f"{data['tile'].get('uniprot_id') or 'typed'} {data['tile'].get('tile_index') or ''}".strip()),
            ('sequence_sha256', data['sequence_sha256'])]
    for tag, p in (('a', pa), ('b', pb)):
        head += [(f'{tag}_analysis_id', p['analysis_id']), (f'{tag}_model_id', p['model_id']),
                 (f'{tag}_weights_sha256', p['weights_sha256']), (f'{tag}_calibrator', p['calibrator']),
                 (f'{tag}_evidence_label', p['evidence_label']), (f'{tag}_domain_status', p['domain_status'])]
    head += [(k, m[k]) for k in ('spearman_raw', 'pearson_raw', 'spearman_prob', 'mean_abs_diff_raw',
                                 'mean_abs_diff_prob', 'top_k', 'top_k_overlap', 'top_k_jaccard')]
    for k, v in head:
        out.write(f"# {k}={str(v).replace(chr(10), ' ').replace(chr(13), ' ')}\n")
    w = csv.writer(out, lineterminator='\n')
    w.writerow(EXPORT_COLUMNS)
    for c in data['cells']:
        w.writerow([c['position'], c['wt_aa'], c['mut_aa'], f"{c['raw_a']:.10g}", f"{c['raw_b']:.10g}",
                    f"{c['prob_a']:.10g}", f"{c['prob_b']:.10g}", f"{c['prob_b'] - c['prob_a']:.10g}",
                    c['rank_a'], c['rank_b']])
    return out.getvalue()


__all__ = ['compare', 'get', 'list_for_project', 'to_csv', 'metrics_of', 'disagreements_of', 'LABEL']
