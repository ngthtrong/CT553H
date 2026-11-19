"""Local admin page endpoints (plan-system 4.2)."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from .. import admin
from .predict import NO_STORE

router = APIRouter(tags=['operations'])
log = logging.getLogger('api.admin')


def _guard(request: Request):
    core = request.app.state.core
    admin.check_allowed(getattr(request.state, 'client_ip', None), core.settings.admin_allowed_networks)
    return core


@router.get('/v1/admin/status')
async def admin_status(request: Request):
    core = _guard(request)
    return JSONResponse(await run_in_threadpool(admin.status, core), headers=NO_STORE)


@router.post('/v1/admin/registry/reload')
async def reload_registry(request: Request):
    """Reload the registry: every weights file is hashed again; a mismatch takes the model out of service."""
    core = _guard(request)
    await run_in_threadpool(core.reload_registry)
    log.info('registry reloaded from the admin page: %d models serving', len(core.registry.models))
    return JSONResponse(await run_in_threadpool(admin.status, core), headers=NO_STORE)
