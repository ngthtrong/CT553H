"""Import datasets and comparisons (UC-05, UC-09; FR-17/28–30; api-spec §6–§7). Implementation plan WP6.

A preview stores the uploaded file under a generated path and the valid rows as a `staged` revision; commit only flips
it to `committed` (immutable). A comparison is a frozen snapshot computed from one analysis and one committed dataset.
Nothing here changes the reference tables or any model (D-8, D-11).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from statistics import mean, median
from typing import Any

import numpy as np
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import Session

from db.models import AnalysisRun, Comparison, ImportDataset, ImportObservation
from degron_footprint.errors import DomainError

from . import repository as repo
from . import workspace_store as ws
from .importer import Report

META_COLUMNS = ('name', 'assay', 'assay_version', 'endpoint', 'units', 'source', 'reference_description',
                'compatibility', 'rights_note')
NOTE = 'comparison only; not used to retrain the model'


def protein_lookup(s: Session):
    def look(acc: str) -> tuple[str, str] | None:
        p = repo.get_protein(s, acc) if acc and len(acc) <= 10 else None
        return (p.uniprot_release, p.sequence) if p else None
    return look


# --- datasets -------------------------------------------------------------------------------------------------------

def next_revision(s: Session, project_id: str, name: str) -> int:
    n = s.scalar(select(func.max(ImportDataset.revision)).where(ImportDataset.project_id == project_id,
                                                                ImportDataset.name == name))
    return int(n or 0) + 1


def create_staged(s: Session, *, project_id: str, dataset_id: str, meta: dict, report: Report, sha: str,
                  relpath: str, hours: int) -> ImportDataset:
    t = ws.now()
    d = ImportDataset(dataset_id=dataset_id, project_id=project_id, name=meta['name'],
                      revision=next_revision(s, project_id, meta['name']), state='staged', file_path=relpath,
                      sha256=sha, assay=meta['assay'], assay_version=meta.get('assay_version'),
                      endpoint=meta['endpoint'], units=meta['units'], source=meta['source'],
                      reference_description=meta['reference_description'], compatibility=meta['compatibility'],
                      rights_note=meta.get('rights_note'), committable=report.committable, counts=report.counts,
                      validation_report=report.issue_list(), created_at=t, expires_at=t + timedelta(hours=hours))
    s.add(d)
    s.flush()
    if report.rows:
        s.execute(insert(ImportObservation), [{'observation_id': str(uuid.uuid4()), 'dataset_id': dataset_id, **r}
                                              for r in report.rows])
    ws.touch(s, project_id)
    return d


def get_dataset(s: Session, dataset_id: str, *, for_update: bool = False) -> ImportDataset:
    d = s.get(ImportDataset, dataset_id, with_for_update=for_update)
    if d is None:
        raise DomainError('DATASET_NOT_FOUND', 'No dataset has this id.', 404)
    return d


def expire_if_due(d: ImportDataset, now: datetime) -> bool:
    if d.state == 'staged' and d.expires_at is not None and repo.aware(d.expires_at) <= now:
        d.state = 'expired'
        return True
    return False


def dataset_dict(d: ImportDataset) -> dict:
    out: dict[str, Any] = {
        'dataset_id': d.dataset_id, 'project_id': d.project_id, 'revision': d.revision, 'state': d.state,
        'sha256': d.sha256, 'metadata': {k: getattr(d, k) for k in META_COLUMNS if getattr(d, k) is not None},
        'committable': bool(d.committable) and d.state == 'staged', 'counts': d.counts, 'issues': d.validation_report,
        'created_at': ws.iso(d.created_at)}
    if d.committed_at is not None:
        out['committed_at'] = ws.iso(d.committed_at)
    return out


def list_datasets(s: Session, project_id: str, offset: int, limit: int) -> dict:
    q = select(ImportDataset).where(ImportDataset.project_id == project_id)
    total = int(s.scalar(select(func.count()).select_from(q.subquery())) or 0)
    rows = s.scalars(q.order_by(ImportDataset.created_at.desc(), ImportDataset.dataset_id)
                     .offset(offset).limit(limit)).all()
    return ws.page([dataset_dict(d) for d in rows], total, offset, limit)


def commit(s: Session, d: ImportDataset, acknowledge_warnings: bool) -> None:
    if d.state == 'committed':
        return                                                  # idempotent; the revision is immutable
    if expire_if_due(d, ws.now()) or d.state == 'expired':
        raise DomainError('IMPORT_EXPIRED', 'This preview has expired; upload the file again.', 409)
    if not d.committable:
        raise DomainError('IMPORT_INVALID', 'The preview has blocking errors; fix the file and upload it again.', 409)
    if any(i.get('severity') == 'warning' for i in d.validation_report) and not acknowledge_warnings:
        raise DomainError('IMPORT_INVALID', 'The preview has warnings; acknowledge them to commit.', 409,
                          'acknowledge_warnings')
    d.state = 'committed'
    d.committed_at = ws.now()
    d.expires_at = None
    ws.touch(s, d.project_id)


def dataset_dependencies(s: Session, dataset_id: str) -> dict[str, int]:
    def n(model, col) -> int:
        return int(s.scalar(select(func.count()).select_from(model).where(col == dataset_id)) or 0)
    return {'observations': n(ImportObservation, ImportObservation.dataset_id),
            'comparisons': n(Comparison, Comparison.dataset_id)}


def delete_dataset_rows(s: Session, d: ImportDataset) -> None:
    s.execute(delete(Comparison).where(Comparison.dataset_id == d.dataset_id))
    s.execute(delete(ImportObservation).where(ImportObservation.dataset_id == d.dataset_id))
    project_id = d.project_id
    s.delete(d)
    ws.touch(s, project_id)


def purge_expired_staged(s: Session, now: datetime | None = None) -> list[tuple[str, str]]:
    """Mark abandoned previews expired and drop their observations; returns (project_id, file path) to delete."""
    now = now or ws.now()
    out = []
    for d in s.scalars(select(ImportDataset).where(ImportDataset.state == 'staged',
                                                   ImportDataset.expires_at <= now)).all():
        d.state = 'expired'
        d.committable = False
        s.execute(delete(ImportObservation).where(ImportObservation.dataset_id == d.dataset_id))
        out.append((d.project_id, d.file_path))
    return out


# --- comparison -----------------------------------------------------------------------------------------------------

def _ranks(v: np.ndarray) -> np.ndarray:
    order = np.argsort(v, kind='mergesort')
    ranks = np.empty(len(v))
    sv = v[order]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1                  # average rank for ties
        i = j + 1
    return ranks


def spearman(x: list[float], y: list[float]) -> float | None:
    if len(x) < 3:
        return None
    rx, ry = _ranks(np.asarray(x, float)), _ranks(np.asarray(y, float))
    if np.all(rx == rx[0]) or np.all(ry == ry[0]):
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def compare(s: Session, run: AnalysisRun, d: ImportDataset, replicate_id: str | None,
            aggregation: str | None) -> Comparison:
    if d.project_id != run.project_id:
        raise DomainError('DATASET_NOT_FOUND', 'No dataset with this id in the project of the analysis.', 404,
                          'dataset_id')
    if expire_if_due(d, ws.now()) or d.state != 'committed':
        raise DomainError('DATASET_NOT_COMMITTED', 'Commit the dataset before comparing with it.', 409, 'dataset_id')
    obs = s.scalars(select(ImportObservation).where(ImportObservation.dataset_id == d.dataset_id)
                    .order_by(ImportObservation.row_number)).all()
    if replicate_id is not None and not any(o.replicate_id == replicate_id for o in obs):
        raise DomainError('INVALID_REQUEST', 'The dataset has no observation with this replicate_id.', 422,
                          'replicate_id')
    result = run.result
    seq = result['tile']['sequence']
    tile = result['tile']
    counts = dict.fromkeys(('observations', 'selected', 'matched', 'unmatched_sequence', 'missing_value',
                            'mapping_conflict', 'other_replicates'), 0)
    groups: dict[tuple[int, str], list[float]] = {}
    for o in obs:
        counts['observations'] += 1
        if replicate_id is not None and o.replicate_id != replicate_id:
            counts['other_replicates'] += 1
            continue
        counts['selected'] += 1
        if o.wt_sequence != seq:
            counts['unmatched_sequence'] += 1
            continue
        # if both sides carry a protein mapping it must agree (api-spec §7)
        if o.uniprot_acc and tile.get('uniprot_id') and (
                o.uniprot_acc != tile['uniprot_id'] or o.start_pos != tile.get('start_pos')):
            counts['mapping_conflict'] += 1
            continue
        if o.observed_value is None:
            counts['missing_value'] += 1
            continue
        groups.setdefault((o.position, o.mut_aa), []).append(o.observed_value)
    compatible = d.compatibility == 'zhang_gps_dpsi'
    rows, pred, observed = [], [], []
    for c in result['cells']:
        values = groups.get((c['position'], c['mut_aa']))
        if not values:
            continue
        if replicate_id is not None:
            value = values[0]
        else:
            value = mean(values) if aggregation == 'mean' else median(values)
        rows.append({'position': c['position'], 'wt_aa': c['wt_aa'], 'mut_aa': c['mut_aa'], 'observed': value,
                     'n_replicates': len(values), 'units': d.units,
                     'predicted_dpsi_raw': c['score_dpsi_raw'] if compatible else None,
                     'residual': c['score_dpsi_raw'] - value if compatible else None})
        pred.append(c['score_dpsi_raw'])
        observed.append(value)
    counts['matched'] = len(rows)
    mae = rho = None
    reason = None
    if not compatible:
        reason = ('The dataset endpoint is not declared comparable with GPS ΔPSI; observations are shown in their own '
                  'units and no pooled residual or metric is computed.')
    elif not rows:
        reason = 'No observation matches the analysed sequence, position and mutant.'
    else:
        mae = float(np.mean(np.abs(np.asarray(pred) - np.asarray(observed))))
        rho = spearman(pred, observed)
        if rho is None:
            reason = 'Spearman needs at least three pairs and values that are not all equal.'
    t = ws.now()
    cmp = Comparison(
        comparison_id=str(uuid.uuid4()), project_id=run.project_id, analysis_id=run.analysis_id,
        dataset_id=d.dataset_id, replicate_id=replicate_id, aggregation=aggregation, compatible=compatible,
        matched=len(rows), counts=counts, mae=mae, spearman=rho, metric_unavailable_reason=reason, rows=rows,
        provenance={'version': 1, 'note': NOTE, 'dataset_revision': d.revision, 'dataset_name': d.name,
                    'dataset_sha256': d.sha256, 'endpoint': d.endpoint, 'units': d.units,
                    'compatibility': d.compatibility, 'replicate_id': replicate_id, 'aggregation': aggregation,
                    'n_pairs': len(rows), 'residual': 'predicted_dpsi_raw - observed',
                    'analysis_model_id': run.model_id,
                    'analysis_weights_sha256': (run.provenance or {}).get('model', {}).get('weights_sha256'),
                    'never_compared': 'p_dpsi_ge_1_calibrated (a probability, not a ΔPSI)'},
        created_at=t)
    s.add(cmp)
    s.flush()
    return cmp


def comparison_dict(c: Comparison) -> dict:
    return {'comparison_id': c.comparison_id, 'analysis_id': c.analysis_id, 'dataset_id': c.dataset_id,
            'compatible': c.compatible, 'matched': c.matched, 'counts': c.counts, 'mae': c.mae,
            'spearman': c.spearman, 'metric_unavailable_reason': c.metric_unavailable_reason, 'rows': c.rows,
            'provenance': c.provenance}


def list_comparisons(s: Session, analysis_id: str, offset: int, limit: int) -> dict:
    q = select(Comparison).where(Comparison.analysis_id == analysis_id)
    total = int(s.scalar(select(func.count()).select_from(q.subquery())) or 0)
    rows = s.scalars(q.order_by(Comparison.created_at.desc(), Comparison.comparison_id).offset(offset).limit(limit))
    return ws.page([comparison_dict(c) for c in rows], total, offset, limit)
