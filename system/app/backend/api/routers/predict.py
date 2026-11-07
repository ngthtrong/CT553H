"""POST /v1/predict, /v1/export, /v1/runs (stateless unless a share link is requested)."""
from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, Response

from degron_footprint.errors import DomainError
from degron_footprint.export import filename, to_csv, to_json_payload

from ..core import Core
from ..requests import PredictRequest, parse_predict, read_json_body
from ..service import Outcome

router = APIRouter()
NO_STORE = {'Cache-Control': 'no-store'}


def _run(core: Core, req: PredictRequest) -> Outcome:
    """Blocking part: database lookups and the 532 dot products."""
    needs_db = req.sequence is None
    if needs_db:
        with core.factory() as s:
            return core.predictor.predict(req, s)
    # a typed sequence needs no tile lookup; sources of the model are already in the registry
    return core.predictor.predict(req, None)


@router.post('/v1/predict', tags=['prediction'])
async def predict(request: Request):
    core: Core = request.app.state.core
    req = parse_predict(await read_json_body(request, core.settings.max_body_bytes))
    outcome = await run_in_threadpool(_run, core, req)
    request.state.model_id = outcome.model_id
    return JSONResponse(outcome.result, headers=NO_STORE)


@router.post('/v1/export', tags=['prediction'])
async def export_stateless(request: Request):
    core: Core = request.app.state.core
    body = await read_json_body(request, core.settings.max_body_bytes)
    fmt = body.get('format', None) if isinstance(body, dict) else None
    if 'format' not in body:
        raise DomainError('INVALID_REQUEST', 'The field "format" (csv or json) is required.', 422, 'format')
    if fmt not in ('csv', 'json'):
        raise DomainError('INVALID_FORMAT', 'format must be "csv" or "json".', 400, 'format')
    req = parse_predict(body, frozenset({'format'}))
    outcome = await run_in_threadpool(_run, core, req)
    request.state.model_id = outcome.model_id
    return file_response(outcome.result, fmt)


def file_response(result: dict, fmt: str) -> Response:
    name = filename(result, fmt)
    headers = {**NO_STORE, 'Content-Disposition': f'attachment; filename="{name}"'}
    if fmt == 'csv':
        return Response(to_csv(result), media_type='text/csv; charset=utf-8', headers=headers)
    return JSONResponse(to_json_payload(result, datetime.now(UTC)), headers=headers)


@router.post('/v1/runs', status_code=201, tags=['sharing'])
async def create_run(request: Request):
    core: Core = request.app.state.core
    s = core.settings
    body = await read_json_body(request, s.max_body_bytes)
    ttl = body.get('ttl_days', s.share_ttl_default_days) if isinstance(body, dict) else None
    if isinstance(ttl, bool) or not isinstance(ttl, int) or not 1 <= ttl <= s.share_ttl_max_days:
        raise DomainError('INVALID_REQUEST', f'ttl_days must be an integer from 1 to {s.share_ttl_max_days}.',
                          422, 'ttl_days')
    req = parse_predict(body, frozenset({'ttl_days'}))

    def work():
        with core.factory() as sess, sess.begin():
            outcome = core.predictor.predict(req, sess)
            run_id, token, expires = core.predictor.store_run(sess, outcome, ttl)
        return outcome, run_id, token, expires

    outcome, run_id, token, expires = await run_in_threadpool(work)
    request.state.model_id = outcome.model_id
    return JSONResponse({'run_id': run_id, 'share_token': token,
                         'expires_at': expires.strftime('%Y-%m-%dT%H:%M:%SZ'), 'result': outcome.result},
                        status_code=201, headers=NO_STORE)
