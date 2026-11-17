"""Peptide and whole-protein jobs (UC-08; FR-24…27, FR-36; api-spec §5). Implementation plan WP5.

Submission validates and expands the input into job items, pins the model/calibrator/gate/source versions and stores
everything in one transaction; the worker (api/worker.py) does the scoring. Inputs that can never be scored (wrong
length, non-standard residue, unscorable window) are recorded as refused items at submission, so the manifest always
accounts for every input.
"""
from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from db.models import AnalysisJob, AnalysisRun, DataSource, JobItem
from degron_footprint.constants import CODE_VERSION
from degron_footprint.errors import DomainError
from degron_footprint.validation import check_accession, is_scorable, n_tiles, normalize_sequence, tile_bounds, tile_sequence

from . import repository as repo
from . import workspace_store as ws
from .config import Settings
from .service import Predictor

JOB_FIELDS = {'mode', 'peptides', 'protein', 'model_id', 'calibrator', 'override_domain'}
ITEM_STATES = ('pending', 'running', 'succeeded', 'refused', 'failed', 'cancelled')
TERMINAL_JOB = ('completed', 'partial', 'failed', 'cancelled')
LETTERS = re.compile(r'^[A-Z]+$')
# A prediction that fails for these reasons is a property of the input, not a malfunction.
REFUSED_CODES = frozenset({'OUT_OF_DOMAIN', 'TILE_NOT_SCORABLE', 'INVALID_LENGTH', 'INVALID_CHARACTER'})


def _err(code: str, message: str) -> dict:
    return {'code': code, 'message': message, 'field': None}


# --- submission -----------------------------------------------------------------------------------------------------

def _peptide_items(peptides: Any, settings: Settings) -> tuple[list[dict], dict]:
    if not isinstance(peptides, list) or not peptides:
        raise DomainError('INVALID_REQUEST', '"peptides" must be a non-empty list.', 422, 'peptides')
    if len(peptides) > settings.max_batch_peptides:
        raise DomainError('PAYLOAD_TOO_LARGE', f'A job takes at most {settings.max_batch_peptides} peptides.', 413,
                          'peptides')
    items: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_seq: dict[str, int] = {}
    for i, p in enumerate(peptides, 1):
        if not isinstance(p, dict) or set(p) - {'input_id', 'sequence'}:
            raise DomainError('INVALID_REQUEST', f'Peptide {i} must be {{input_id, sequence}}.', 422, 'peptides')
        input_id, raw = p.get('input_id'), p.get('sequence')
        if not isinstance(input_id, str) or not 1 <= len(input_id) <= 200:
            raise DomainError('INVALID_REQUEST', f'Peptide {i}: input_id must have 1 to 200 characters.', 422,
                              'peptides')
        if input_id in seen_ids:
            raise DomainError('INVALID_REQUEST', f'Peptide {i}: input_id is used twice; ids must be unique.', 422,
                              'peptides')
        seen_ids.add(input_id)
        if not isinstance(raw, str) or len(raw) > 64:
            raise DomainError('INVALID_REQUEST', f'Peptide {i}: sequence must be text of at most 64 characters.',
                              422, 'peptides')
        item: dict[str, Any] = {'item_id': f'p{i:04d}', 'ordinal': i, 'input_id': input_id}
        try:
            seq = normalize_sequence(raw)
            item['sequence'] = seq
            seen_seq[seq] = seen_seq.get(seq, 0) + 1
        except DomainError as exc:
            item.update(state='refused', error=_err(exc.code, exc.message))
        items.append(item)
    summary = {'inputs': len(items), 'valid': sum('sequence' in it for it in items),
               'invalid': sum('error' in it for it in items),
               'duplicate_sequences': sum(n - 1 for n in seen_seq.values())}
    return items, summary


def _protein_items(s: Session, protein: Any, settings: Settings) -> tuple[list[dict], dict, dict]:
    if not isinstance(protein, dict) or set(protein) - {'input_id', 'uniprot_id', 'sequence', 'reference_release'}:
        raise DomainError('INVALID_REQUEST', '"protein" must be {uniprot_id} or {input_id, sequence}.', 422, 'protein')
    has_acc, has_seq = protein.get('uniprot_id') is not None, protein.get('sequence') is not None
    if has_acc == has_seq:
        raise DomainError('INVALID_REQUEST', 'Give exactly one of protein.uniprot_id or protein.sequence.', 422,
                          'protein')
    release = protein.get('reference_release')
    if has_acc:
        acc = check_accession(protein['uniprot_id'], 'protein.uniprot_id')
        prot = repo.get_protein(s, acc)
        if prot is None:
            raise DomainError('UNKNOWN_ACCESSION', 'This accession is not among the proteins loaded in this service.',
                              404, 'protein.uniprot_id')
        if release is not None and release != prot.uniprot_release:
            raise DomainError('INVALID_REQUEST', f'The loaded reference is UniProt {prot.uniprot_release}, not the '
                              'requested release; the mapping cannot be verified.', 422, 'protein.reference_release')
        seq, input_id, release, mapped = prot.sequence, str(protein.get('input_id') or acc), prot.uniprot_release, acc
    else:
        typed_id = protein.get('input_id')
        if not isinstance(typed_id, str) or not 1 <= len(typed_id) <= 200:
            raise DomainError('INVALID_REQUEST', 'protein.input_id must have 1 to 200 characters.', 422,
                              'protein.input_id')
        raw = protein['sequence']
        if not isinstance(raw, str):
            raise DomainError('INVALID_REQUEST', 'protein.sequence must be text.', 422, 'protein.sequence')
        input_id = typed_id
        seq = re.sub(r'\s+', '', raw).upper()
        if not LETTERS.fullmatch(seq or 'A'):
            raise DomainError('INVALID_CHARACTER', 'protein.sequence may contain only letters (one-letter codes).',
                              422, 'protein.sequence')
        mapped, release = None, None                    # typed proteins are never silently given an accession
    if len(seq) > settings.max_protein_residues:
        raise DomainError('PAYLOAD_TOO_LARGE', f'A protein job takes at most {settings.max_protein_residues} '
                          'residues.', 413, 'protein')
    n = n_tiles(len(seq))
    if n == 0:
        raise DomainError('INVALID_LENGTH', 'The protein is shorter than one 28-residue tile; nothing can be scored.',
                          422, 'protein')
    items, unscorable = [], []
    for i in range(1, n + 1):
        start, end = tile_bounds(i)
        window = tile_sequence(seq, i) or ''
        item: dict[str, Any] = {'item_id': f't{i:05d}', 'ordinal': i, 'input_id': input_id, 'tile_index': i,
                                'start_pos': start, 'end_pos': end, 'uniprot_acc': mapped,
                                'reference_release': release}
        if is_scorable(window):
            item['sequence'] = window
        else:
            item.update(state='refused', error=_err('TILE_NOT_SCORABLE', 'This window contains a residue that is not '
                                                    'one of the 20 standard amino acids.'))
            unscorable.append({'tile_index': i, 'start': start, 'end': end})
        items.append(item)
    last_end = tile_bounds(n)[1]
    coverage = {'version': 1, 'input_id': input_id, 'uniprot_id': mapped, 'reference_release': release,
                'protein_length': len(seq), 'sequence_sha256': hashlib.sha256(seq.encode()).hexdigest(),
                'tile_length': 28, 'step': 23, 'tiles': n,
                # windows start at residue 1, so only the C-terminal end can be uncovered (api-spec §5)
                'uncovered': [{'start': last_end + 1, 'end': len(seq)}] if last_end < len(seq) else [],
                'unscorable_windows': unscorable,
                'note': 'Overlapping windows are scored separately; substitutions are never averaged across tiles.'}
    summary = {'inputs': 1, 'tiles': n, 'scorable_tiles': n - len(unscorable)}
    return items, coverage, summary


def _sources(s: Session) -> list[dict]:
    rows = s.scalars(select(DataSource).order_by(DataSource.source_id)).all()
    return [{'source_id': r.source_id, 'version': r.version, 'sha256': r.sha256} for r in rows]


def submit(s: Session, predictor: Predictor, settings: Settings, project_id: str, body: dict,
           gate_model_id: str | None, gate_sha256: str | None = None) -> AnalysisJob:
    if any(k not in JOB_FIELDS for k in body):
        raise DomainError('INVALID_REQUEST', 'The request has a field that is not part of the interface.', 422)
    mode = body.get('mode')
    calibrator = body.get('calibrator')
    if calibrator is not None and calibrator not in ('platt', 'iso'):
        raise DomainError('INVALID_REQUEST', 'calibrator must be "platt" or "iso".', 422, 'calibrator')
    override = body.get('override_domain', False)
    if not isinstance(override, bool):
        raise DomainError('INVALID_REQUEST', 'override_domain must be true or false.', 422, 'override_domain')
    model_id = body.get('model_id')
    if model_id is not None and not isinstance(model_id, str):
        raise DomainError('INVALID_REQUEST', 'model_id must be a string.', 422, 'model_id')
    coverage = None
    if mode == 'peptides':
        if 'protein' in body:
            raise DomainError('INVALID_REQUEST', 'A peptides job takes "peptides" only.', 422, 'protein')
        items, summary = _peptide_items(body.get('peptides'), settings)
    elif mode == 'protein':
        if 'peptides' in body:
            raise DomainError('INVALID_REQUEST', 'A protein job takes "protein" only.', 422, 'peptides')
        items, coverage, summary = _protein_items(s, body.get('protein'), settings)
    else:
        raise DomainError('INVALID_REQUEST', 'mode must be "peptides" or "protein".', 422, 'mode')
    lm = predictor.pick_model(model_id)                 # FR-27: pin what is serving now
    calibrator = calibrator or getattr(lm.adapter, 'default_calibrator', None) or 'platt'
    t = ws.now()
    job = AnalysisJob(
        job_id=str(uuid.uuid4()), project_id=project_id, mode=mode, state='pending', total=len(items),
        input_snapshot={'version': 1, 'mode': mode,
                        'peptides': [{'input_id': it['input_id'], 'sequence': it.get('sequence')} for it in items]
                        if mode == 'peptides' else None,
                        'protein': {k: v for k, v in (coverage or {}).items()
                                    if k in ('input_id', 'uniprot_id', 'reference_release', 'protein_length',
                                             'sequence_sha256')} if mode == 'protein' else None},
        configuration_snapshot={'version': 1, 'model_id': lm.info.model_id, 'weights_sha256': lm.info.weights_sha256,
                                'model_kind': lm.info.kind, 'calibrator': calibrator, 'override_domain': override,
                                'gate_model_id': gate_model_id, 'gate_sha256': gate_sha256,
                                'code_version': CODE_VERSION,
                                'sources': _sources(s), 'input_summary': summary,
                                'limits': {'peptides': settings.max_batch_peptides,
                                           'protein_residues': settings.max_protein_residues}},
        coverage=coverage, model_id=lm.info.model_id, model_sha256=lm.info.weights_sha256, calibrator=calibrator,
        gate_model_id=gate_model_id, gate_sha256=gate_sha256, cancel_requested=False, created_at=t, updated_at=t)
    s.add(job)
    s.flush()
    for it in items:
        s.add(JobItem(job_id=job.job_id, item_id=it['item_id'], ordinal=it['ordinal'], input_id=it['input_id'],
                      sequence=it.get('sequence'), uniprot_acc=it.get('uniprot_acc'),
                      reference_release=it.get('reference_release'), tile_index=it.get('tile_index'),
                      start_pos=it.get('start_pos'), end_pos=it.get('end_pos'), state=it.get('state', 'pending'),
                      error=it.get('error'), updated_at=t))
    s.flush()
    refresh_state(s, job)
    ws.touch(s, project_id)
    return job


# --- state ----------------------------------------------------------------------------------------------------------

def item_counts(s: Session, job_id: str) -> dict[str, int]:
    rows = s.execute(select(JobItem.state, func.count()).where(JobItem.job_id == job_id).group_by(JobItem.state))
    counts = dict.fromkeys(ITEM_STATES, 0)
    counts.update({state: int(n) for state, n in rows})
    return counts


def refresh_state(s: Session, job: AnalysisJob, now: datetime | None = None) -> dict[str, int]:
    """api-spec §5: completed = every item succeeded; partial = terminal mix with ≥1 success; no success = failed
    unless cancelled. Counts always reconcile with the manifest."""
    counts = item_counts(s, job.job_id)
    open_ = counts['pending'] + counts['running']
    before = job.state
    if open_ == 0:
        if job.cancel_requested:
            job.state = 'cancelled'
        elif counts['succeeded'] == job.total:
            job.state = 'completed'
        else:
            job.state = 'partial' if counts['succeeded'] else 'failed'
    elif counts['running'] or job.started_at is not None:     # refused-at-submission items do not start a job
        job.state = 'running'
    else:
        job.state = 'pending'
    t = now or ws.now()
    if job.state != before:
        job.updated_at = t
        if job.state == 'running' and job.started_at is None:
            job.started_at = t
        if job.state in TERMINAL_JOB:
            job.finished_at = t
    return counts


def cancel(s: Session, job: AnalysisJob) -> None:
    """Idempotent. Pending items are cancelled now; an item a live worker holds is cancelled when it tries to commit;
    an item whose lease already expired (dead worker) is cancelled now."""
    if job.state in TERMINAL_JOB:
        if job.state == 'cancelled':
            return
        raise DomainError('JOB_STATE_CONFLICT', f'The job is already {job.state}; there is nothing to cancel.', 409)
    t = ws.now()
    job.cancel_requested = True
    job.updated_at = t
    s.execute(update(JobItem).where(JobItem.job_id == job.job_id, JobItem.state == 'pending')
              .values(state='cancelled', updated_at=t))
    s.execute(update(JobItem).where(JobItem.job_id == job.job_id, JobItem.state == 'running',
                                    JobItem.lease_expires_at < t)
              .values(state='cancelled', lease_owner=None, lease_expires_at=None, updated_at=t))
    refresh_state(s, job, t)


# --- reading --------------------------------------------------------------------------------------------------------

def get_job(s: Session, job_id: str, *, for_update: bool = False) -> AnalysisJob:
    job = s.get(AnalysisJob, job_id, with_for_update=for_update)
    if job is None:
        raise DomainError('JOB_NOT_FOUND', 'No job has this id.', 404)
    return job


def job_dict(s: Session, job: AnalysisJob) -> dict:
    out: dict[str, Any] = {'job_id': job.job_id, 'project_id': job.project_id, 'mode': job.mode, 'state': job.state,
                           'total': job.total, 'counts': item_counts(s, job.job_id),
                           'configuration_snapshot': job.configuration_snapshot,
                           'cancel_requested': bool(job.cancel_requested),
                           'created_at': ws.iso(job.created_at), 'updated_at': ws.iso(job.updated_at)}
    if job.coverage is not None:
        out['coverage'] = job.coverage
    return out


def list_jobs(s: Session, project_id: str, offset: int, limit: int) -> dict:
    q = select(AnalysisJob).where(AnalysisJob.project_id == project_id)
    total = int(s.scalar(select(func.count()).select_from(q.subquery())) or 0)
    rows = s.scalars(q.order_by(AnalysisJob.created_at.desc(), AnalysisJob.job_id).offset(offset).limit(limit)).all()
    return ws.page([job_dict(s, j) for j in rows], total, offset, limit)


def item_dict(it: JobItem, analysis_id: str | None) -> dict:
    out: dict[str, Any] = {'item_id': it.item_id, 'input_id': it.input_id, 'state': it.state}
    for key in ('tile_index', 'start_pos', 'end_pos', 'domain_status'):
        value = getattr(it, key)
        if value is not None:
            out[key] = value
    if analysis_id:
        out['analysis_id'] = analysis_id
    if it.error:
        out['error'] = it.error
    return out


def list_items(s: Session, job_id: str, offset: int, limit: int) -> dict:
    total = int(s.scalar(select(func.count()).select_from(JobItem).where(JobItem.job_id == job_id)) or 0)
    rows = s.execute(
        select(JobItem, AnalysisRun.analysis_id)
        .outerjoin(AnalysisRun, (AnalysisRun.job_id == JobItem.job_id) & (AnalysisRun.item_id == JobItem.item_id))
        .where(JobItem.job_id == job_id).order_by(JobItem.ordinal).offset(offset).limit(limit)).all()
    return ws.page([item_dict(it, aid) for it, aid in rows], total, offset, limit)
