"""Database access for the workspace tables (db-design §11). Routers and the worker call these; nothing else writes.

Saved analyses are immutable: there is an insert and a delete, and no update function (A-5).
"""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import Session

from db.models import AnalysisCell, AnalysisJob, AnalysisRun, Comparison, ImportDataset, ImportObservation, JobItem, Project
from degron_footprint.errors import DomainError
from degron_footprint.provenance import utc_iso

from . import repository as repo

MAX_PAGE = 200
MAX_OFFSET = 1_000_000_000          # beyond any local workspace; larger values overflow a database integer


def now() -> datetime:
    """Stored with microseconds so "most recent first" is right within one second; shown to the second."""
    return datetime.now(UTC)


def iso(dt: datetime | None) -> str | None:
    return utc_iso(repo.aware(dt)) if dt is not None else None


def parse_id(value: str, field: str) -> str:
    """A path id must be a canonical UUID; anything else is a request error, never a lookup."""
    try:
        canon = str(uuid.UUID(value))
    except (ValueError, AttributeError, TypeError):
        raise DomainError('INVALID_REQUEST', f'{field} must be a UUID.', 422, field) from None
    if canon != value.lower():
        raise DomainError('INVALID_REQUEST', f'{field} must be a UUID.', 422, field)
    return canon


def check_page(offset: int, limit: int) -> None:
    if not 0 <= offset <= MAX_OFFSET:
        raise DomainError('INVALID_REQUEST', f'offset must be between 0 and {MAX_OFFSET}.', 422, 'offset')
    if not 1 <= limit <= MAX_PAGE:
        raise DomainError('INVALID_REQUEST', f'limit must be between 1 and {MAX_PAGE}.', 422, 'limit')


def page(items: list, total: int, offset: int, limit: int) -> dict:
    return {'items': items, 'total': total, 'offset': offset, 'limit': limit}


# --- projects -----------------------------------------------------------------------------------------------------

def project_counts(s: Session, project_id: str) -> dict[str, int]:
    def n(model, col) -> int:
        return int(s.scalar(select(func.count()).select_from(model).where(col == project_id)) or 0)
    return {'analyses': n(AnalysisRun, AnalysisRun.project_id), 'jobs': n(AnalysisJob, AnalysisJob.project_id),
            'datasets': n(ImportDataset, ImportDataset.project_id)}


def project_dict(s: Session, p: Project) -> dict:
    out: dict[str, Any] = {'project_id': p.project_id, 'name': p.name, 'description': p.description or '',
                           'created_at': iso(p.created_at), 'updated_at': iso(p.updated_at),
                           'counts': project_counts(s, p.project_id)}
    if p.deletion_state == 'deleting':
        out['deletion_pending'] = True
    return out


def get_project(s: Session, project_id: str, *, for_update: bool = False) -> Project:
    p = s.get(Project, project_id, with_for_update=for_update)
    if p is None:
        raise DomainError('PROJECT_NOT_FOUND', 'No project has this id.', 404)
    return p


def require_active(p: Project) -> None:
    if p.deletion_state != 'active':
        raise DomainError('JOB_STATE_CONFLICT', 'This project is being deleted; repeat the deletion to finish it.', 409)


def list_projects(s: Session, offset: int, limit: int) -> dict:
    total = int(s.scalar(select(func.count()).select_from(Project)) or 0)
    rows = s.scalars(select(Project).order_by(Project.updated_at.desc(), Project.project_id)
                     .offset(offset).limit(limit)).all()
    return page([project_dict(s, p) for p in rows], total, offset, limit)


def create_project(s: Session, name: str, description: str) -> Project:
    t = now()
    p = Project(project_id=str(uuid.uuid4()), name=name, description=description, created_at=t, updated_at=t)
    s.add(p)
    s.flush()
    return p


def touch(s: Session, project_id: str) -> None:
    p = s.get(Project, project_id)
    if p is not None:
        p.updated_at = now()


def project_dependencies(s: Session, project_id: str) -> dict[str, int]:
    c = project_counts(s, project_id)
    job_ids = select(AnalysisJob.job_id).where(AnalysisJob.project_id == project_id)
    ds_ids = select(ImportDataset.dataset_id).where(ImportDataset.project_id == project_id)
    c['job_items'] = int(s.scalar(select(func.count()).select_from(JobItem).where(JobItem.job_id.in_(job_ids))) or 0)
    c['observations'] = int(s.scalar(select(func.count()).select_from(ImportObservation)
                                     .where(ImportObservation.dataset_id.in_(ds_ids))) or 0)
    c['comparisons'] = int(s.scalar(select(func.count()).select_from(Comparison)
                                    .where(Comparison.project_id == project_id)) or 0)
    c['running_jobs'] = int(s.scalar(select(func.count()).select_from(AnalysisJob).where(
        AnalysisJob.project_id == project_id, AnalysisJob.state.in_(('pending', 'running')))) or 0)
    return c


def confirmation_required(dependencies: dict[str, int]) -> DomainError:
    return DomainError('CONFIRMATION_REQUIRED',
                       'Deleting removes the records counted in "dependencies". Repeat with confirm=true.', 409,
                       dependencies=dependencies)


def cancel_project_jobs(s: Session, project_id: str) -> int:
    """Mark every unfinished job cancelled so the worker stops claiming its items and refuses late writes."""
    jobs = s.scalars(select(AnalysisJob).where(AnalysisJob.project_id == project_id,
                                               AnalysisJob.state.in_(('pending', 'running')))).all()
    t = now()
    for j in jobs:
        j.cancel_requested = True
        j.updated_at = t
    s.execute(update(JobItem)
              .where(JobItem.job_id.in_([j.job_id for j in jobs]), JobItem.state.in_(('pending', 'running')))
              .values(state='cancelled', lease_owner=None, lease_expires_at=None, updated_at=t))
    for j in jobs:
        j.state = 'cancelled'
        j.finished_at = t
    return len(jobs)


# --- analyses -----------------------------------------------------------------------------------------------------

def insert_analysis(s: Session, *, project_id: str, result: dict, provenance: dict, annotations: dict,
                    input_kind: str, sequence: str, model_id: str, domain_status: str, created: datetime,
                    parent_analysis_id: str | None = None, job_id: str | None = None,
                    item_id: str | None = None) -> AnalysisRun:
    tile = result['tile']
    run = AnalysisRun(analysis_id=str(uuid.uuid4()), project_id=project_id, job_id=job_id, item_id=item_id,
                      parent_analysis_id=parent_analysis_id, model_id=model_id, input_kind=input_kind,
                      input_sequence=sequence, uniprot_acc=tile.get('uniprot_id'), tile_index=tile.get('tile_index'),
                      domain_status=domain_status, result=result, provenance=provenance,
                      annotation_snapshot=annotations, created_at=created)
    s.add(run)
    s.flush()
    s.execute(insert(AnalysisCell), [
        {'analysis_id': run.analysis_id, 'position': c['position'], 'mut_aa': c['mut_aa'], 'wt_aa': c['wt_aa'],
         'score_raw': c['score_dpsi_raw'], 'prob_calibrated': c['p_dpsi_ge_1_calibrated'],
         'rank_in_tile': c['rank_in_tile'], 'top10': c['top10pct_in_tile']} for c in result['cells']])
    touch(s, project_id)
    return run


def get_analysis(s: Session, analysis_id: str) -> AnalysisRun:
    run = s.get(AnalysisRun, analysis_id)
    if run is None:
        raise DomainError('ANALYSIS_NOT_FOUND', 'No saved analysis has this id.', 404)
    return run


def analysis_dict(s: Session, run: AnalysisRun) -> dict:
    from .snapshot import response_snapshot
    result = run.result
    if not isinstance(result, dict) or not result.get('cells') or not result.get('provenance'):
        raise DomainError('SNAPSHOT_UNAVAILABLE', 'The stored snapshot of this analysis is incomplete.', 409)
    out: dict[str, Any] = {'analysis_id': run.analysis_id, 'project_id': run.project_id,
                           'parent_analysis_id': run.parent_analysis_id, 'created_at': iso(run.created_at),
                           'result': result, 'snapshot': response_snapshot(run.provenance, run.annotation_snapshot)}
    if run.parent_analysis_id is not None:
        out['parent_available'] = s.get(AnalysisRun, run.parent_analysis_id) is not None
    return out


def analysis_summary(run: AnalysisRun) -> dict:
    """SavedAnalysisSummary: a history row without the 532 cells."""
    out: dict[str, Any] = {'analysis_id': run.analysis_id, 'project_id': run.project_id,
                           'parent_analysis_id': run.parent_analysis_id, 'job_id': run.job_id,
                           'created_at': iso(run.created_at), 'input_kind': run.input_kind,
                           'tile': run.result.get('tile'), 'domain_status': run.domain_status,
                           'model_id': run.model_id,
                           'warning_codes': list((run.provenance or {}).get('warning_codes') or [])}
    return out


def list_analyses(s: Session, project_id: str, offset: int, limit: int) -> dict:
    q = select(AnalysisRun).where(AnalysisRun.project_id == project_id)
    total = int(s.scalar(select(func.count()).select_from(q.subquery())) or 0)
    rows = s.scalars(q.order_by(AnalysisRun.created_at.desc(), AnalysisRun.analysis_id)
                     .offset(offset).limit(limit)).all()
    return page([analysis_summary(r) for r in rows], total, offset, limit)


def analysis_dependencies(s: Session, analysis_id: str) -> dict[str, int]:
    return {'comparisons': int(s.scalar(select(func.count()).select_from(Comparison)
                                        .where(Comparison.analysis_id == analysis_id)) or 0)}


def delete_analysis(s: Session, run: AnalysisRun) -> None:
    s.execute(delete(Comparison).where(Comparison.analysis_id == run.analysis_id))
    s.execute(delete(AnalysisCell).where(AnalysisCell.analysis_id == run.analysis_id))
    project_id = run.project_id
    s.delete(run)
    touch(s, project_id)
