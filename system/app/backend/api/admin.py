"""Local admin status (plan-system 4.2): counts and states only — no sequence, no input id, no imported value.

Shown to clients from `DF_ADMIN_ALLOWED_NETWORKS` (loopback by default). Safe actions only: reload the model registry,
which re-checks every weights hash. There is deliberately no ETL, delete or restore action here.
"""
from __future__ import annotations

import ipaddress
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from db.models import AnalysisJob, EtlRun, JobItem, WorkerHeartbeat
from degron_footprint import __version__
from degron_footprint.constants import CODE_VERSION
from degron_footprint.errors import DomainError

from .core import Core

ALIVE_SECONDS = 30                    # a worker beats every 5 s while idle or busy; 30 s without a beat = not alive


def check_allowed(client_ip: str | None, networks: list[str]) -> None:
    try:
        addr = ipaddress.ip_address((client_ip or '').strip())
    except ValueError:
        addr = None
    if addr is not None:
        if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
            addr = addr.ipv4_mapped
        for n in networks:
            try:
                if addr in ipaddress.ip_network(n, strict=False):
                    return
            except ValueError:
                continue
    raise DomainError('LOCAL_ONLY', 'The admin page answers only on this computer (DF_ADMIN_ALLOWED_NETWORKS).', 403)


def _dir_size(path: Path) -> dict[str, int]:
    files = size = 0
    if path.is_dir():
        for root, _dirs, names in os.walk(path):
            for n in names:
                try:
                    size += (Path(root) / n).stat().st_size
                    files += 1
                except OSError:
                    continue
    return {'bytes': size, 'files': files}


def _db_size(s: Session, url: str) -> int | None:
    try:
        if s.get_bind().dialect.name == 'postgresql':
            return int(s.execute(text('SELECT pg_database_size(current_database())')).scalar() or 0)
        path = url.split('///', 1)[-1]
        return Path(path).stat().st_size if path and Path(path).exists() else None
    except Exception:
        return None


def _etl(s: Session) -> dict[str, Any] | None:
    row = s.scalars(select(EtlRun).order_by(EtlRun.etl_run_id.desc()).limit(1)).first()
    if row is None:
        return None
    report = row.report or {}
    # numbers only from the report (row counts, durations); no paths, no free text
    counts = {k: v for k, v in report.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return {'status': row.status, 'started_at': row.started_at.isoformat() if row.started_at else None,
            'finished_at': row.finished_at.isoformat() if row.finished_at else None, 'git_commit': row.git_commit,
            'numbers': counts}


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def status(core: Core) -> dict[str, Any]:
    now = datetime.now(UTC)
    reg = core.registry
    out: dict[str, Any] = {'generated_at': now.isoformat(timespec='seconds'), 'version': __version__,
                           'code_version': CODE_VERSION}
    out['models'] = {
        'default_model_id': reg.default_id, 'default_source': reg.default_source,
        'loaded': [{'model_id': m, 'kind': lm.info.kind, 'weights_sha256': lm.info.weights_sha256,
                    'expected_tile_seconds': core.predictor.expected_tile_seconds(m)} for m, lm in sorted(reg.models.items())],
        'not_loaded': [{'model_id': m, 'reason': r} for m, r in sorted(reg.errors.items())],
        'gate_model_id': core.gate.gate_model_id,
    }
    out['cache'] = core.predictor.cache.stats().as_dict()
    with core.factory() as s:
        try:
            out['schema_revision'] = s.execute(text('SELECT version_num FROM alembic_version')).scalar()
        except Exception:
            out['schema_revision'] = None
        out['etl'] = _etl(s)
        jobs = dict(s.execute(select(AnalysisJob.state, func.count()).group_by(AnalysisJob.state)).all())
        items = dict(s.execute(select(JobItem.state, func.count())
                               .where(JobItem.state.in_(('pending', 'running'))).group_by(JobItem.state)).all())
        oldest = s.scalar(select(func.min(AnalysisJob.created_at)).where(AnalysisJob.state.in_(('pending', 'running'))))
        oldest = _aware(oldest)
        out['queue'] = {'jobs_by_state': {k: int(v) for k, v in jobs.items()},
                        'items_pending': int(items.get('pending', 0)), 'items_running': int(items.get('running', 0)),
                        'oldest_open_job_seconds': round((now - oldest).total_seconds()) if oldest else None}
        workers = []
        try:
            for w in s.scalars(select(WorkerHeartbeat).order_by(WorkerHeartbeat.last_seen_at.desc()).limit(20)):
                seen = _aware(w.last_seen_at)
                alive = w.stopped_at is None and seen is not None and now - seen < timedelta(seconds=ALIVE_SECONDS)
                started, stopped = _aware(w.started_at), _aware(w.stopped_at)
                workers.append({'owner': w.owner, 'alive': alive, 'started_at': started.isoformat() if started else None,
                                'last_seen_at': seen.isoformat() if seen else None,
                                'stopped_at': stopped.isoformat() if stopped else None,
                                'items_done': int(w.items_done or 0)})
        except Exception:
            workers = []
        out['workers'] = {'alive': sum(1 for w in workers if w['alive']), 'recent': workers,
                          'alive_after_seconds': ALIVE_SECONDS}
        if out['queue']['items_pending'] and not out['workers']['alive']:
            out['workers']['warning'] = 'Items are waiting but no worker has reported in the last 30 s.'
        out['storage'] = {'database_bytes': _db_size(s, core.settings.database_url),
                          'workspace': _dir_size(core.settings.workspace_dir)}
    return out


__all__ = ['status', 'check_allowed', 'ALIVE_SECONDS']
