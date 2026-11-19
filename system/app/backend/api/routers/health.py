from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from degron_footprint import __version__

router = APIRouter()


@router.get('/healthz', tags=['operations'])
def health(request: Request):
    core = request.app.state.core
    try:
        with core.engine.connect() as c:
            c.execute(text('SELECT 1'))
        db = 'ok'
    except Exception:
        db = 'unavailable'
    default = core.registry.default
    body = {
        'status': 'ok' if (db == 'ok' and default is not None) else 'degraded',
        'version': __version__, 'model_loaded': default is not None,
        'default_model_id': default.info.model_id if default else None, 'database': db,
        # plan-system 4.3: where the default came from and its weights hash, checkable against the serving decision
        'default_model_source': core.registry.default_source if default else None,
        'default_model_sha256': default.info.weights_sha256 if default else None,
    }
    return JSONResponse(body, status_code=200 if body['status'] == 'ok' else 503, headers={'Cache-Control': 'no-store'})
