"""Projects and saved analyses (UC-10, FR-14/22/31–33; api-spec §4). Implementation plan WP4."""
from __future__ import annotations

import logging
import time
from datetime import UTC, datetime

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, Response

from degron_footprint.errors import DomainError

from .. import exports, snapshot
from .. import workspace_store as ws
from ..core import Core
from ..requests import parse_predict, read_json_body
from ..workspace import remove_project_dir
from .predict import NO_STORE

router = APIRouter(tags=['workspace'])
log = logging.getLogger('api.workspace')


def _core(request: Request) -> Core:
    return request.app.state.core


def _text(body: dict, key: str, *, required: bool, max_len: int) -> str | None:
    if key not in body:
        if required:
            raise DomainError('INVALID_REQUEST', f'"{key}" is required.', 422, key)
        return None
    value = body[key]
    if not isinstance(value, str):
        raise DomainError('INVALID_REQUEST', f'"{key}" must be text.', 422, key)
    value = value.strip()
    if key == 'name' and not 1 <= len(value) <= max_len:
        raise DomainError('INVALID_REQUEST', f'"{key}" must have 1 to {max_len} characters.', 422, key)
    if len(value) > max_len:
        raise DomainError('INVALID_REQUEST', f'"{key}" must have at most {max_len} characters.', 422, key)
    return value


def _only(body: dict, allowed: set[str]) -> None:
    if any(k not in allowed for k in body):
        raise DomainError('INVALID_REQUEST', 'The request has a field that is not part of the interface.', 422)


# --- projects -----------------------------------------------------------------------------------------------------

@router.get('/v1/projects')
def list_projects(request: Request, offset: int = Query(0), limit: int = Query(50)):
    ws.check_page(offset, limit)
    with _core(request).factory() as s:
        return ws.list_projects(s, offset, limit)


@router.post('/v1/projects', status_code=201)
async def create_project(request: Request):
    core = _core(request)
    body = await read_json_body(request, core.settings.max_body_bytes)
    _only(body, {'name', 'description'})
    name = _text(body, 'name', required=True, max_len=200)
    description = _text(body, 'description', required=False, max_len=2000) or ''

    def work():
        with core.factory() as s, s.begin():
            p = ws.create_project(s, name or '', description)
            return ws.project_dict(s, p)
    out = await run_in_threadpool(work)
    log.info('project created id=%s', out['project_id'])
    return JSONResponse(out, status_code=201)


@router.get('/v1/projects/{project_id}')
def get_project(request: Request, project_id: str):
    pid = ws.parse_id(project_id, 'project_id')
    with _core(request).factory() as s:
        return ws.project_dict(s, ws.get_project(s, pid))


@router.patch('/v1/projects/{project_id}')
async def rename_project(request: Request, project_id: str):
    core = _core(request)
    pid = ws.parse_id(project_id, 'project_id')
    body = await read_json_body(request, core.settings.max_body_bytes)
    _only(body, {'name', 'description'})
    name = _text(body, 'name', required=False, max_len=200)
    description = _text(body, 'description', required=False, max_len=2000)

    def work():
        with core.factory() as s, s.begin():
            p = ws.get_project(s, pid)
            ws.require_active(p)
            if name is not None:
                p.name = name
            if description is not None:
                p.description = description
            p.updated_at = ws.now()
            s.flush()
            return ws.project_dict(s, p)
    return await run_in_threadpool(work)


@router.delete('/v1/projects/{project_id}', status_code=204)
def delete_project(request: Request, project_id: str, confirm: bool = Query(False)):
    """HIST-03: dependency summary first; then cancel jobs and block late worker writes, remove owned files, and
    only then remove owned rows. A file-cleanup failure leaves the project in `deleting` for a retry."""
    core = _core(request)
    pid = ws.parse_id(project_id, 'project_id')
    started = time.perf_counter()
    with core.factory() as s, s.begin():
        p = ws.get_project(s, pid, for_update=True)
        deps = ws.project_dependencies(s, pid)
        if not confirm:
            raise ws.confirmation_required(deps)
        p.deletion_state = 'deleting'
        cancelled = ws.cancel_project_jobs(s, pid)
    problem = remove_project_dir(core.settings.workspace_dir, pid)
    if problem is not None:
        log.error('project delete incomplete id=%s files=%s', pid, problem.split(':')[0])
        raise DomainError('SERVICE_UNAVAILABLE', 'The project files could not be removed; nothing else was deleted '
                          'yet. Repeat the deletion to retry.', 503)
    with core.factory() as s, s.begin():
        s.delete(ws.get_project(s, pid))
    log.info('project deleted id=%s analyses=%d jobs=%d datasets=%d cancelled=%d ms=%.0f', pid, deps['analyses'],
             deps['jobs'], deps['datasets'], cancelled, (time.perf_counter() - started) * 1000)
    return Response(status_code=204)


# --- analyses -----------------------------------------------------------------------------------------------------

@router.get('/v1/projects/{project_id}/analyses')
def list_analyses(request: Request, project_id: str, offset: int = Query(0), limit: int = Query(50)):
    pid = ws.parse_id(project_id, 'project_id')
    ws.check_page(offset, limit)
    with _core(request).factory() as s:
        ws.get_project(s, pid)
        return ws.list_analyses(s, pid, offset, limit)


@router.post('/v1/projects/{project_id}/analyses', status_code=201)
async def save_analysis(request: Request, project_id: str):
    """Compute and store in one transaction (FR-32). The unsaved preview is POST /v1/predict and never stored."""
    core = _core(request)
    pid = ws.parse_id(project_id, 'project_id')
    body = await read_json_body(request, core.settings.max_body_bytes)
    _only(body, {'request', 'parent_analysis_id'})
    if not isinstance(body.get('request'), dict):
        raise DomainError('INVALID_REQUEST', '"request" must be a prediction request object.', 422, 'request')
    req = parse_predict(body['request'])
    parent = body.get('parent_analysis_id')
    if parent is not None:
        if not isinstance(parent, str):
            raise DomainError('INVALID_REQUEST', 'parent_analysis_id must be a UUID.', 422, 'parent_analysis_id')
        parent = ws.parse_id(parent, 'parent_analysis_id')

    def work():
        with core.factory() as s, s.begin():
            p = ws.get_project(s, pid)
            ws.require_active(p)
            if parent is not None:
                prow = s.get(ws.AnalysisRun, parent)
                if prow is None or prow.project_id != pid:
                    raise DomainError('ANALYSIS_NOT_FOUND', 'The parent analysis is not in this project.', 404,
                                      'parent_analysis_id')
            outcome = core.predictor.predict(req, s)
            lm = core.predictor.pick_model(req.model_id)
            created = datetime.now(UTC).replace(microsecond=0)
            result, prov, ann = snapshot.build(s, outcome, req, lm, core.gate.gate_model_id, created)
            run = ws.insert_analysis(s, project_id=pid, result=result, provenance=prov, annotations=ann,
                                     input_kind=outcome.input_kind, sequence=outcome.sequence,
                                     model_id=outcome.model_id, domain_status=outcome.status, created=created,
                                     parent_analysis_id=parent)
            return ws.analysis_dict(s, run), outcome.model_id
    out, model_id = await run_in_threadpool(work)
    request.state.model_id = model_id
    log.info('analysis saved project=%s analysis=%s', pid, out['analysis_id'])
    return JSONResponse(out, status_code=201, headers=NO_STORE)


@router.get('/v1/analyses/{analysis_id}')
def get_analysis(request: Request, analysis_id: str):
    aid = ws.parse_id(analysis_id, 'analysis_id')
    with _core(request).factory() as s:
        return JSONResponse(ws.analysis_dict(s, ws.get_analysis(s, aid)), headers=NO_STORE)


@router.delete('/v1/analyses/{analysis_id}', status_code=204)
def delete_analysis(request: Request, analysis_id: str, confirm: bool = Query(False)):
    aid = ws.parse_id(analysis_id, 'analysis_id')
    with _core(request).factory() as s, s.begin():
        run = ws.get_analysis(s, aid)
        if not confirm:
            raise ws.confirmation_required(ws.analysis_dependencies(s, aid))
        ws.delete_analysis(s, run)
    log.info('analysis deleted id=%s', aid)
    return Response(status_code=204)


@router.get('/v1/analyses/{analysis_id}/export')
def export_analysis(request: Request, analysis_id: str, format: str | None = Query(None),
                    comparison_id: str | None = Query(None)):
    """Historical export from the stored snapshot only (api-spec §8)."""
    aid = ws.parse_id(analysis_id, 'analysis_id')
    if format is None:
        raise DomainError('INVALID_REQUEST', 'The query parameter "format" (csv or json) is required.', 422, 'format')
    if format not in ('csv', 'json'):
        raise DomainError('INVALID_FORMAT', 'format must be "csv" or "json".', 400, 'format')
    with _core(request).factory() as s:
        run = ws.get_analysis(s, aid)
        data = ws.analysis_dict(s, run)
        comparison = None
        if comparison_id is not None:
            comparison = exports.comparison_for_export(s, ws.parse_id(comparison_id, 'comparison_id'), aid)
    return exports.analysis_file(data, format, comparison)
