"""GET /v1/runs/{run_id} and its export. A wrong token looks exactly like an unknown run (no probing)."""
from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Header, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from degron_footprint.errors import DomainError

from .. import repository as repo
from ..core import Core
from .predict import NO_STORE, file_response

router = APIRouter()


def _load(core: Core, run_id: str, token: str | None) -> dict:
    if not token:
        raise DomainError('TOKEN_REQUIRED', 'Send the share token in the X-Share-Token header.', 401)
    not_found = DomainError('RUN_NOT_FOUND', 'No shared run matches this id and token.', 404)
    try:
        run_id = str(uuid.UUID(run_id))
    except ValueError:
        raise not_found from None
    expired = False
    result: dict | None = None
    with core.factory() as s, s.begin():
        run = repo.get_run(s, run_id)
        if run is None or not secrets.compare_digest(run.share_token_hash, repo.hash_token(token)):
            raise not_found
        if repo.aware(run.expires_at) < datetime.now(UTC):
            repo.delete_run(s, run_id)                       # opportunistic purge (db-design §9); committed below
            expired = True
        else:
            result = core.predictor.rebuild_run(s, run)
    if expired:
        raise DomainError('RUN_EXPIRED', 'This shared run has expired and was deleted.', 410)
    assert result is not None
    return result


@router.get('/v1/runs/{run_id}', tags=['sharing'])
async def get_run(request: Request, run_id: str, x_share_token: str | None = Header(None)):
    core: Core = request.app.state.core
    result = await run_in_threadpool(_load, core, run_id, x_share_token)
    return JSONResponse(result, headers=NO_STORE)


@router.get('/v1/runs/{run_id}/export', tags=['sharing'])
async def export_run(request: Request, run_id: str, format: str | None = Query(None),
                     x_share_token: str | None = Header(None)):
    core: Core = request.app.state.core
    if format is None:
        raise DomainError('INVALID_REQUEST', 'The query parameter "format" (csv or json) is required.', 400, 'format')
    if format not in ('csv', 'json'):
        raise DomainError('INVALID_FORMAT', 'format must be "csv" or "json".', 400, 'format')
    result = await run_in_threadpool(_load, core, run_id, x_share_token)
    return file_response(result, format)
