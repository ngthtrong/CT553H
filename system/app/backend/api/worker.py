"""Local job worker (implementation plan WP5; A-2…A-4). Run as a separate process:

    python -m api.worker            (from system/app/backend, with DF_DATABASE_URL set; `make dev-worker`)

The queue is the `job_item` table. A worker claims one item with a compare-and-set UPDATE that only succeeds when the
item is pending or its lease has expired, so two workers can never both own it; on PostgreSQL the candidate is also
selected with FOR UPDATE SKIP LOCKED to avoid contention. Scoring happens outside any transaction. The commit step
re-checks that this worker still owns the lease, that the job was not cancelled and that the project is not being
deleted; the unique (job_id, item_id) of analysis_run makes a duplicate result impossible even if those checks raced.

Logs carry job/item ids, states, counts and durations only — never a sequence (NFR-09, NFR-19).
"""
from __future__ import annotations

import logging
import os
import signal
import socket
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased, sessionmaker

from db.models import AnalysisJob, JobItem, Project
from degron_footprint.errors import DomainError

from . import jobs, snapshot
from . import workspace_store as ws
from .config import Settings
from .requests import PredictRequest
from .service import Predictor

log = logging.getLogger('api.worker')


@dataclass
class Processed:
    job_id: str
    item_id: str
    state: str                          # succeeded | refused | failed | cancelled | lost
    ms: float


class Worker:
    def __init__(self, factory: sessionmaker[Session], predictor: Predictor, settings: Settings,
                 gate_model_id: str | None, owner: str | None = None, gate_sha256: str | None = None):
        self.factory = factory
        self.predictor = predictor
        self.settings = settings
        self.gate_model_id = gate_model_id
        self.gate_sha256 = gate_sha256
        self.owner = owner or f'{socket.gethostname()}:{os.getpid()}:{uuid.uuid4().hex[:8]}'
        self._beat_at = 0.0
        self._done_since_beat = 0

    # ------------------------------------------------------------------ heartbeat (plan-system 4.2)
    HEARTBEAT_SECONDS = 5.0

    def heartbeat(self, *, force: bool = False, stopped: bool = False) -> None:
        """Upsert this worker's row at most every HEARTBEAT_SECONDS; never fails the loop."""
        mono = time.monotonic()
        if not force and not stopped and mono - self._beat_at < self.HEARTBEAT_SECONDS:
            return
        try:
            from db.models import WorkerHeartbeat
            t = datetime.now(UTC)
            with self.factory() as s, s.begin():
                row = s.get(WorkerHeartbeat, self.owner)
                if row is None:
                    row = WorkerHeartbeat(owner=self.owner, started_at=t, last_seen_at=t, items_done=0)
                    s.add(row)
                row.last_seen_at = t
                row.items_done = (row.items_done or 0) + self._done_since_beat
                row.stopped_at = t if stopped else None
            self._done_since_beat = 0
            self._beat_at = mono
        except Exception as exc:                        # pre-0007 database or a brief outage: keep working
            log.warning('worker heartbeat not written: %s', type(exc).__name__)

    # ------------------------------------------------------------------ claim
    def claim(self, now: datetime | None = None) -> tuple[str, str] | None:
        now = now or datetime.now(UTC)
        reclaimable = or_(JobItem.state == 'pending',
                          and_(JobItem.state == 'running', JobItem.lease_expires_at < now))
        with self.factory() as s, s.begin():
            # plan-system 4.5: at most job_max_running_items live items per job; higher priority, then oldest job first
            live = aliased(JobItem)
            running = (select(func.count()).select_from(live)
                       .where(live.job_id == JobItem.job_id, live.state == 'running', live.lease_expires_at >= now)
                       .correlate(JobItem).scalar_subquery())
            q = (select(JobItem.job_id, JobItem.item_id)
                 .join(AnalysisJob, AnalysisJob.job_id == JobItem.job_id)
                 .join(Project, Project.project_id == AnalysisJob.project_id)
                 .where(reclaimable, AnalysisJob.cancel_requested.is_(False),
                        AnalysisJob.state.in_(('pending', 'running')), Project.deletion_state == 'active',
                        running < self.settings.job_max_running_items)
                 .order_by(AnalysisJob.priority.desc(), AnalysisJob.created_at, AnalysisJob.job_id, JobItem.ordinal)
                 .limit(1))
            if s.get_bind().dialect.name == 'postgresql':
                q = q.with_for_update(skip_locked=True, of=JobItem)
            row = s.execute(q).first()
            if row is None:
                return None
            job_id, item_id = row
            res = s.execute(update(JobItem)
                            .where(JobItem.job_id == job_id, JobItem.item_id == item_id, reclaimable)
                            .values(state='running', lease_owner=self.owner, attempts=JobItem.attempts + 1,
                                    lease_expires_at=now + timedelta(seconds=self.settings.job_lease_seconds),
                                    updated_at=now))
            if res.rowcount != 1:                       # type: ignore[attr-defined]
                return None                             # someone else won; the loop simply tries again
            job = s.get(AnalysisJob, job_id)
            if job is not None:
                jobs.refresh_state(s, job, now)
            return job_id, item_id

    # ------------------------------------------------------------------ process
    def _score(self, s: Session, job: AnalysisJob, item: JobItem):
        if self.gate_model_id != job.gate_model_id or self.gate_sha256 != job.gate_sha256:
            raise DomainError('SNAPSHOT_UNAVAILABLE', 'The domain gate pinned when the job was submitted is not the '
                              'one loaded now; the item is not scored with a different gate.', 409)
        lm = self.predictor.registry.models.get(job.model_id)
        if lm is None or lm.info.weights_sha256 != job.model_sha256:
            raise DomainError('MODEL_NOT_FOUND', 'The model pinned when the job was submitted is no longer serving '
                              'with the same weights.', 409)
        if item.uniprot_acc is not None and item.tile_index is not None:
            req = PredictRequest(None, item.uniprot_acc, item.tile_index, job.model_id, job.calibrator,
                                 bool(job.configuration_snapshot.get('override_domain')))
        else:
            req = PredictRequest(item.sequence, None, None, job.model_id, job.calibrator,
                                 bool(job.configuration_snapshot.get('override_domain')))
        outcome = self.predictor.predict(req, s)
        created = datetime.now(UTC).replace(microsecond=0)
        result, prov, ann = snapshot.build(s, outcome, req, lm, self.gate_model_id, created)
        if item.start_pos is not None:                  # protein mode: keep the protein coordinates of the window
            prov['protein_window'] = {'input_id': item.input_id, 'tile_index': item.tile_index,
                                      'start_pos': item.start_pos, 'end_pos': item.end_pos,
                                      'uniprot_id': item.uniprot_acc, 'reference_release': item.reference_release}
        return outcome, result, prov, ann, created

    def process(self, job_id: str, item_id: str) -> Processed:
        started = time.perf_counter()
        error: DomainError | None = None
        scored = None
        with self.factory() as s:
            job = s.get(AnalysisJob, job_id)
            item = s.get(JobItem, (job_id, item_id))
            if job is None or item is None:
                return Processed(job_id, item_id, 'lost', 0.0)
            try:
                scored = self._score(s, job, item)
            except DomainError as exc:
                error = exc
            except Exception as exc:                    # a bug must fail one item, not the worker
                log.error('item crashed job=%s item=%s error=%s', job_id, item_id, type(exc).__name__)
                error = DomainError('INTERNAL_ERROR', 'Unexpected error while scoring this item.', 500)
        try:
            state = self._commit(job_id, item_id, scored, error, started)
        except IntegrityError:                          # project deleted underneath us, or a duplicate result
            state = 'lost'
        ms = (time.perf_counter() - started) * 1000
        log.info('item done job=%s item=%s state=%s ms=%.1f', job_id, item_id, state, ms)
        return Processed(job_id, item_id, state, ms)

    def _commit(self, job_id: str, item_id: str, scored, error: DomainError | None, started: float | None = None) -> str:
        with self.factory() as s, s.begin():
            # Take the write lock first: a compare-and-set touch of the item we own. On SQLite this makes every read
            # below see the latest committed state (a cancellation committed a moment ago is not missed); on
            # PostgreSQL it locks the item row. Without it the job state could be written from a stale cancel flag.
            t = ws.now()
            owned = s.execute(update(JobItem).where(JobItem.job_id == job_id, JobItem.item_id == item_id,
                                                    JobItem.state == 'running', JobItem.lease_owner == self.owner)
                              .values(updated_at=t))
            if owned.rowcount != 1:                     # type: ignore[attr-defined]
                return 'lost'                           # lease expired and reclaimed, or rows deleted
            job = s.get(AnalysisJob, job_id, with_for_update=True, populate_existing=True)
            item = s.get(JobItem, (job_id, item_id), populate_existing=True)
            if job is None or item is None or item.state != 'running' or item.lease_owner != self.owner:
                return 'lost'                           # lease expired and reclaimed, or rows deleted
            project = s.get(Project, job.project_id)
            if job.cancel_requested or project is None or project.deletion_state != 'active':
                item.state = 'cancelled'
            elif error is not None:
                item.state = 'refused' if error.code in jobs.REFUSED_CODES else 'failed'
                item.error = {'code': error.code, 'message': error.message, 'field': None}
            else:
                outcome, result, prov, ann, created = scored
                ws.insert_analysis(s, project_id=job.project_id, result=result, provenance=prov, annotations=ann,
                                   input_kind=outcome.input_kind, sequence=outcome.sequence,
                                   model_id=outcome.model_id, domain_status=outcome.status, created=created,
                                   job_id=job_id, item_id=item_id)
                item.state = 'succeeded'
                item.domain_status = outcome.status
            item.lease_owner = None
            item.lease_expires_at = None
            item.updated_at = t
            if started is not None and item.state != 'cancelled':        # plan-system 1.7: ETA input
                item.duration_ms = round((time.perf_counter() - started) * 1000, 1)
            s.flush()
            before = job.state
            counts = jobs.refresh_state(s, job, t)
            if job.state != before and job.state in jobs.TERMINAL_JOB:
                took = (repo_aware(job.finished_at) - repo_aware(job.created_at)).total_seconds()
                log.info('job finished job=%s state=%s total=%d succeeded=%d refused=%d failed=%d cancelled=%d '
                         'seconds=%.1f', job_id, job.state, job.total, counts['succeeded'], counts['refused'],
                         counts['failed'], counts['cancelled'], took)
            return item.state

    # ------------------------------------------------------------------ loop
    def run_once(self) -> Processed | None:
        claimed = self.claim()
        p = self.process(*claimed) if claimed else None
        if p is not None and p.state not in ('lost',):
            self._done_since_beat += 1
        self.heartbeat()
        return p

    def drain(self, limit: int = 100_000) -> list[Processed]:
        """Process until no claimable item is left (tests, and the CLI with --drain)."""
        done: list[Processed] = []
        while len(done) < limit:
            p = self.run_once()
            if p is None:
                break
            done.append(p)
        return done

    def run(self, stop: threading.Event) -> None:
        log.info('worker started owner=%s lease=%ss', self.owner, self.settings.job_lease_seconds)
        self.heartbeat(force=True)
        while not stop.is_set():
            try:
                p = self.run_once()
            except Exception as exc:                    # database briefly unavailable: wait and retry
                log.error('worker loop error: %s', type(exc).__name__)
                p = None
            if p is None:
                stop.wait(self.settings.worker_poll_seconds)
        self.heartbeat(stopped=True)
        log.info('worker stopped owner=%s', self.owner)


def repo_aware(dt: datetime | None) -> datetime:
    from . import repository as repo
    return repo.aware(dt) if dt is not None else datetime.now(UTC)


def from_core(core, owner: str | None = None) -> Worker:
    return Worker(core.factory, core.predictor, core.settings, core.gate.gate_model_id, owner,
                  core.gate.weights_sha256)


def main() -> None:                                     # pragma: no cover - exercised manually and in DEP tests
    import argparse

    from db.session import make_engine, make_session_factory

    from .core import build_core

    ap = argparse.ArgumentParser(description='Degron Footprint local job worker')
    ap.add_argument('--drain', action='store_true', help='process every claimable item, then exit')
    args = ap.parse_args()
    settings = Settings()
    logging.basicConfig(level=settings.log_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    engine = make_engine(settings.database_url)
    factory = make_session_factory(engine)
    core = build_core(settings, engine, factory)
    worker = from_core(core)
    if args.drain:
        worker.drain()
        return
    stop = threading.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())
    worker.run(stop)


if __name__ == '__main__':                              # pragma: no cover
    main()
