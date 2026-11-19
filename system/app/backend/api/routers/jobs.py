"""Peptide and whole-protein jobs (UC-08; api-spec §5). Implementation plan WP5."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, StreamingResponse

from degron_footprint.errors import DomainError

from .. import exports, jobs
from .. import workspace_store as ws
from ..core import Core
from ..requests import read_json_body

router = APIRouter(tags=['workspace'])
log = logging.getLogger('api.jobs')


def _core(request: Request) -> Core:
    return request.app.state.core


@router.get('/v1/projects/{project_id}/jobs')
def list_jobs(request: Request, project_id: str, offset: int = Query(0), limit: int = Query(50)):
    pid = ws.parse_id(project_id, 'project_id')
    ws.check_page(offset, limit)
    with _core(request).factory() as s:
        ws.get_project(s, pid)
        return jobs.list_jobs(s, pid, offset, limit)


@router.post('/v1/projects/{project_id}/jobs', status_code=202)
async def submit_job(request: Request, project_id: str):
    core = _core(request)
    pid = ws.parse_id(project_id, 'project_id')
    body = await read_json_body(request, core.settings.max_workspace_body_bytes)

    def work():
        with core.factory() as s, s.begin():
            p = ws.get_project(s, pid)
            ws.require_active(p)
            job = jobs.submit(s, core.predictor, core.settings, pid, body, core.gate.gate_model_id,
                              core.gate.weights_sha256)
            return jobs.job_dict(s, job)
    out = await run_in_threadpool(work)
    request.state.model_id = out['configuration_snapshot']['model_id']
    log.info('job submitted job=%s mode=%s total=%d refused_at_submit=%d', out['job_id'], out['mode'], out['total'],
             out['counts']['refused'])
    return JSONResponse(out, status_code=202)


@router.get('/v1/jobs/{job_id}')
def get_job(request: Request, job_id: str):
    jid = ws.parse_id(job_id, 'job_id')
    with _core(request).factory() as s:
        return jobs.job_dict(s, jobs.get_job(s, jid))


@router.get('/v1/jobs/{job_id}/items')
def list_items(request: Request, job_id: str, offset: int = Query(0), limit: int = Query(50)):
    jid = ws.parse_id(job_id, 'job_id')
    ws.check_page(offset, limit)
    with _core(request).factory() as s:
        jobs.get_job(s, jid)
        return jobs.list_items(s, jid, offset, limit)


@router.get('/v1/jobs/{job_id}/footprint')
def job_footprint(request: Request, job_id: str, input_id: str | None = Query(None)):
    """plan-system 2.1: per-tile footprint of a finished whole-protein job, in protein coordinates; with several
    proteins (3.3) one protein at a time, chosen by input_id (default: the first scored one)."""
    jid = ws.parse_id(job_id, 'job_id')
    if input_id is not None and not 1 <= len(input_id) <= 200:
        raise DomainError('INVALID_REQUEST', 'input_id must have 1 to 200 characters.', 422, 'input_id')
    with _core(request).factory() as s:
        return jobs.footprint(s, jobs.get_job(s, jid), input_id)


@router.post('/v1/jobs/{job_id}/cancel', status_code=202)
def cancel_job(request: Request, job_id: str):
    jid = ws.parse_id(job_id, 'job_id')
    with _core(request).factory() as s, s.begin():
        job = jobs.get_job(s, jid, for_update=True)
        jobs.cancel(s, job)
        out = jobs.job_dict(s, job)
    log.info('job cancel requested job=%s state=%s', jid, out['state'])
    return JSONResponse(out, status_code=202)


@router.get('/v1/jobs/{job_id}/export')
def export_job(request: Request, job_id: str, format: str | None = Query(None)):
    core = _core(request)
    jid = ws.parse_id(job_id, 'job_id')
    if format is None:
        raise DomainError('INVALID_REQUEST', 'The query parameter "format" (csv or json) is required.', 422, 'format')
    if format not in ('csv', 'json'):
        raise DomainError('INVALID_FORMAT', 'format must be "csv" or "json".', 400, 'format')
    with core.factory() as s:
        job = jobs.job_dict(s, jobs.get_job(s, jid))
    name = f'degron-footprint_job-{jid[:8]}_{job["mode"]}.{format}'
    headers = {**exports.NO_STORE, 'Content-Disposition': f'attachment; filename="{name}"'}
    if format == 'csv':
        return StreamingResponse(exports.job_csv(core.factory, job), media_type='text/csv; charset=utf-8',
                                 headers=headers)
    return StreamingResponse(exports.job_json(core.factory, job), media_type='application/json', headers=headers)
