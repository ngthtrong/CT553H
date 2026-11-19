"""Comparison of two saved analyses / two models (plan-system 2.2)."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, Response

from degron_footprint.errors import DomainError

from .. import model_compare as mc
from .. import workspace_store as ws
from ..requests import read_json_body
from .predict import NO_STORE

router = APIRouter(tags=['workspace'])
log = logging.getLogger('api.model_compare')
FIELDS = {'analysis_a', 'analysis_b', 'save'}


@router.post('/v1/analyses/compare')
async def compare_analyses(request: Request):
    core = request.app.state.core
    body = await read_json_body(request, core.settings.max_workspace_body_bytes)
    if not isinstance(body, dict) or set(body) - FIELDS:
        raise DomainError('INVALID_REQUEST', 'Send {analysis_a, analysis_b, save}.', 422)
    ra, rb = body.get('analysis_a'), body.get('analysis_b')
    a = ws.parse_id(ra, 'analysis_a') if isinstance(ra, str) else None
    b = ws.parse_id(rb, 'analysis_b') if isinstance(rb, str) else None
    if a is None or b is None:
        raise DomainError('INVALID_REQUEST', 'analysis_a and analysis_b must be analysis ids.', 422,
                          'analysis_a' if a is None else 'analysis_b')
    save = body.get('save', False)
    if not isinstance(save, bool):
        raise DomainError('INVALID_REQUEST', 'save must be true or false.', 422, 'save')

    def work():
        with core.factory() as s, s.begin():
            return mc.compare(s, a, b, save)
    out, saved = await run_in_threadpool(work)
    if saved:
        log.info('model comparison saved id=%s', out['comparison_id'])
    return JSONResponse(out, status_code=201 if saved else 200, headers=NO_STORE)


@router.get('/v1/analyses/{analysis_id}/suggestions')
def analysis_suggestions(request: Request, analysis_id: str, compare_with: str | None = Query(None),
                         limit: int = Query(20), include_out_of_domain: bool = Query(False),
                         format: str | None = Query(None)):
    """plan-system 2.6: candidates to verify in this tile, each with its reasons; CSV for a lab notebook."""
    from .. import suggestions
    aid = ws.parse_id(analysis_id, 'analysis_id')
    other = ws.parse_id(compare_with, 'compare_with') if compare_with is not None else None
    if not 1 <= limit <= 100:
        raise DomainError('INVALID_REQUEST', 'limit must be between 1 and 100.', 422, 'limit')
    if format not in (None, 'json', 'csv'):
        raise DomainError('INVALID_FORMAT', 'format must be "json" or "csv".', 400, 'format')
    with request.app.state.core.factory() as s:
        data = suggestions.suggest(s, aid, other, limit, include_out_of_domain)
    if format == 'csv':
        name = f'degron-footprint_candidates-{aid[:8]}.csv'
        return Response(suggestions.to_csv(data), media_type='text/csv; charset=utf-8',
                        headers={**NO_STORE, 'Content-Disposition': f'attachment; filename="{name}"'})
    return JSONResponse(data, headers=NO_STORE)


@router.get('/v1/model-comparisons/{comparison_id}')
def get_model_comparison(request: Request, comparison_id: str):
    cid = ws.parse_id(comparison_id, 'comparison_id')
    with request.app.state.core.factory() as s:
        return mc.get(s, cid)


@router.get('/v1/projects/{project_id}/model-comparisons')
def list_model_comparisons(request: Request, project_id: str, offset: int = Query(0), limit: int = Query(50),
                           analysis_id: str | None = Query(None)):
    pid = ws.parse_id(project_id, 'project_id')
    aid = ws.parse_id(analysis_id, 'analysis_id') if analysis_id is not None else None
    ws.check_page(offset, limit)
    with request.app.state.core.factory() as s:
        ws.get_project(s, pid)
        return mc.list_for_project(s, pid, offset, limit, aid)


@router.get('/v1/projects/{project_id}/agreement')
def project_agreement(request: Request, project_id: str):
    """plan-system 4.4: agreement with imported data over time; flags are warnings only."""
    from .. import agreement
    pid = ws.parse_id(project_id, 'project_id')
    with request.app.state.core.factory() as s:
        ws.get_project(s, pid)
        return agreement.series(s, pid)


@router.get('/v1/model-comparisons/{comparison_id}/export')
def export_model_comparison(request: Request, comparison_id: str, format: str | None = Query(None)):
    cid = ws.parse_id(comparison_id, 'comparison_id')
    if format is None:
        raise DomainError('INVALID_REQUEST', 'The query parameter "format" (csv or json) is required.', 422, 'format')
    if format not in ('csv', 'json'):
        raise DomainError('INVALID_FORMAT', 'format must be "csv" or "json".', 400, 'format')
    with request.app.state.core.factory() as s:
        data = mc.get(s, cid)
    name = f'degron-footprint_model-comparison-{cid[:8]}.{format}'
    headers = {**NO_STORE, 'Content-Disposition': f'attachment; filename="{name}"'}
    if format == 'csv':
        return Response(mc.to_csv(data), media_type='text/csv; charset=utf-8', headers=headers)
    return JSONResponse(data, headers=headers)
