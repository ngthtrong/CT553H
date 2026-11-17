"""Experimental import and comparison (UC-05, UC-09; api-spec §6–§7). Implementation plan WP6."""
from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, Response

from degron_footprint.errors import DomainError

from .. import datasets, importer
from .. import workspace_store as ws
from ..core import Core
from ..requests import read_json_body, read_raw_body
from ..workspace import dataset_relpath, resolve_stored

router = APIRouter(tags=['workspace'])
log = logging.getLogger('api.datasets')
MULTIPART_OVERHEAD = 64 * 1024


def _core(request: Request) -> Core:
    return request.app.state.core


@router.get('/v1/projects/{project_id}/datasets')
def list_datasets(request: Request, project_id: str, offset: int = Query(0), limit: int = Query(50)):
    pid = ws.parse_id(project_id, 'project_id')
    ws.check_page(offset, limit)
    with _core(request).factory() as s, s.begin():
        ws.get_project(s, pid)
        return datasets.list_datasets(s, pid, offset, limit)


@router.post('/v1/projects/{project_id}/datasets', status_code=201)
async def preview_import(request: Request, project_id: str):
    """IMP-01: a staged validation preview, never a committed dataset; the file is stored under a generated name."""
    core = _core(request)
    st = core.settings
    pid = ws.parse_id(project_id, 'project_id')
    body = await read_raw_body(request, st.max_import_bytes + MULTIPART_OVERHEAD)
    parts = importer.parse_multipart(body, request.headers.get('content-type', ''))
    if len(parts['file']) > st.max_import_bytes:
        raise DomainError('PAYLOAD_TOO_LARGE', f'The file must not exceed {st.max_import_bytes} bytes.', 413, 'file')
    meta = importer.parse_metadata(parts['metadata'])

    def work():
        did = str(uuid.uuid4())
        with core.factory() as s:
            ws.require_active(ws.get_project(s, pid))
            report = importer.validate(parts['file'], meta, st.max_import_rows, datasets.protein_lookup(s))
        rel = dataset_relpath(pid, did, report.suffix)
        path = resolve_stored(st.workspace_dir, rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(parts['file'])
        try:
            with core.factory() as s, s.begin():
                ws.require_active(ws.get_project(s, pid))
                d = datasets.create_staged(s, project_id=pid, dataset_id=did, meta=meta, report=report,
                                           sha=importer.sha256(parts['file']), relpath=rel,
                                           hours=st.staged_import_hours)
                return datasets.dataset_dict(d)
        except Exception:
            path.unlink(missing_ok=True)                 # no orphan file when the database refuses
            raise
    out = await run_in_threadpool(work)
    log.info('import previewed dataset=%s rows=%d valid=%d rejected=%d committable=%s', out['dataset_id'],
             out['counts']['rows'], out['counts']['valid'], out['counts']['rejected'], out['committable'])
    return JSONResponse(out, status_code=201)


@router.get('/v1/datasets/{dataset_id}')
def get_dataset(request: Request, dataset_id: str):
    did = ws.parse_id(dataset_id, 'dataset_id')
    with _core(request).factory() as s, s.begin():
        d = datasets.get_dataset(s, did)
        datasets.expire_if_due(d, ws.now())
        return datasets.dataset_dict(d)


@router.post('/v1/datasets/{dataset_id}')
async def commit_dataset(request: Request, dataset_id: str):
    core = _core(request)
    did = ws.parse_id(dataset_id, 'dataset_id')
    body = await read_json_body(request, core.settings.max_body_bytes)
    if set(body) - {'action', 'acknowledge_warnings'} or body.get('action') != 'commit':
        raise DomainError('INVALID_REQUEST', 'Send {"action": "commit", "acknowledge_warnings": true|false}.', 422,
                          'action')
    ack = body.get('acknowledge_warnings')
    if not isinstance(ack, bool):
        raise DomainError('INVALID_REQUEST', 'acknowledge_warnings must be true or false.', 422,
                          'acknowledge_warnings')

    def work():
        with core.factory() as s:
            with s.begin():
                d = datasets.get_dataset(s, did, for_update=True)
                expired = datasets.expire_if_due(d, ws.now())
            if expired:                                   # keep the expiry even though commit is refused
                raise DomainError('IMPORT_EXPIRED', 'This preview has expired; upload the file again.', 409)
            with s.begin():
                d = datasets.get_dataset(s, did, for_update=True)
                ws.require_active(ws.get_project(s, d.project_id))
                datasets.commit(s, d, ack)
                return datasets.dataset_dict(d)
    out = await run_in_threadpool(work)
    log.info('import committed dataset=%s revision=%d', did, out['revision'])
    return out


@router.delete('/v1/datasets/{dataset_id}', status_code=204)
def delete_dataset(request: Request, dataset_id: str, confirm: bool = Query(False)):
    core = _core(request)
    did = ws.parse_id(dataset_id, 'dataset_id')
    with core.factory() as s:
        d = datasets.get_dataset(s, did)
        deps = datasets.dataset_dependencies(s, did)
        rel = d.file_path
    if not confirm:
        raise ws.confirmation_required(deps)
    try:
        resolve_stored(core.settings.workspace_dir, rel).unlink(missing_ok=True)
    except OSError as exc:
        log.error('dataset delete incomplete id=%s files=%s', did, type(exc).__name__)
        raise DomainError('SERVICE_UNAVAILABLE', 'The dataset file could not be removed; nothing was deleted. '
                          'Repeat the deletion to retry.', 503) from None
    with core.factory() as s, s.begin():
        datasets.delete_dataset_rows(s, datasets.get_dataset(s, did))
    log.info('dataset deleted id=%s observations=%d comparisons=%d', did, deps['observations'], deps['comparisons'])
    return Response(status_code=204)


# --- comparisons ----------------------------------------------------------------------------------------------------

@router.get('/v1/analyses/{analysis_id}/comparisons')
def list_comparisons(request: Request, analysis_id: str, offset: int = Query(0), limit: int = Query(50)):
    aid = ws.parse_id(analysis_id, 'analysis_id')
    ws.check_page(offset, limit)
    with _core(request).factory() as s:
        ws.get_analysis(s, aid)
        return datasets.list_comparisons(s, aid, offset, limit)


@router.post('/v1/analyses/{analysis_id}/comparisons', status_code=201)
async def compare_dataset(request: Request, analysis_id: str):
    core = _core(request)
    aid = ws.parse_id(analysis_id, 'analysis_id')
    body = await read_json_body(request, core.settings.max_body_bytes)
    if set(body) - {'dataset_id', 'replicate_id', 'aggregation'}:
        raise DomainError('INVALID_REQUEST', 'The request has a field that is not part of the interface.', 422)
    if not isinstance(body.get('dataset_id'), str):
        raise DomainError('INVALID_REQUEST', 'dataset_id is required.', 422, 'dataset_id')
    did = ws.parse_id(body['dataset_id'], 'dataset_id')
    rep, agg = body.get('replicate_id'), body.get('aggregation')
    if (rep is None) == (agg is None):
        raise DomainError('INVALID_REQUEST', 'Choose one replicate_id or one aggregation (mean or median).', 422)
    if rep is not None and (not isinstance(rep, str) or not 1 <= len(rep) <= 200):
        raise DomainError('INVALID_REQUEST', 'replicate_id must be text.', 422, 'replicate_id')
    if agg is not None and agg not in ('mean', 'median'):
        raise DomainError('INVALID_REQUEST', 'aggregation must be "mean" or "median".', 422, 'aggregation')

    def work():
        with core.factory() as s, s.begin():
            run = ws.get_analysis(s, aid)
            ws.require_active(ws.get_project(s, run.project_id))
            d = datasets.get_dataset(s, did, for_update=True)
            c = datasets.compare(s, run, d, rep, agg)
            return datasets.comparison_dict(c)
    out = await run_in_threadpool(work)
    log.info('comparison created id=%s matched=%d compatible=%s', out['comparison_id'], out['matched'],
             out['compatible'])
    return JSONResponse(out, status_code=201)


@router.get('/v1/comparisons/{comparison_id}')
def get_comparison(request: Request, comparison_id: str):
    cid = ws.parse_id(comparison_id, 'comparison_id')
    from db.models import Comparison
    with _core(request).factory() as s:
        c = s.get(Comparison, cid)
        if c is None:
            raise DomainError('COMPARISON_NOT_FOUND', 'No comparison has this id.', 404)
        return datasets.comparison_dict(c)
