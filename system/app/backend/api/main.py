"""Application factory. `uvicorn api.main:app` for production, `create_app(settings)` in tests."""
from __future__ import annotations

import asyncio
import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import Engine

from db.session import make_engine, make_session_factory
from degron_footprint import __version__

from . import errors
from .config import Settings
from .core import build_core, load_contract
from .middleware import CoreMiddleware
from .routers import admin, datasets, health, jobs, model_compare, predict, projects, reference, runs

log = logging.getLogger('api')


async def _periodic(seconds: int, fn, name: str) -> None:
    while True:
        await asyncio.sleep(seconds)
        try:
            await asyncio.to_thread(fn)
        except Exception as exc:                                  # a failed housekeeping run must not stop the service
            log.error('%s failed: %s', name, type(exc).__name__)


def create_app(settings: Settings | None = None, engine: Engine | None = None) -> FastAPI:
    settings = settings or Settings()
    logging.basicConfig(level=settings.log_level, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    engine = engine or make_engine(settings.database_url)
    factory = make_session_factory(engine)
    core = build_core(settings, engine, factory)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        stop = threading.Event()
        worker_thread = None
        if settings.embedded_worker:                      # single-command local start; A-2 default is a process
            from .worker import from_core
            worker_thread = threading.Thread(target=from_core(core).run, args=(stop,), name='job-worker', daemon=True)
            worker_thread.start()
        if settings.background_jobs:
            core.tasks = [
                asyncio.create_task(_periodic(settings.purge_interval_seconds, core.purge_expired, 'purge')),
                asyncio.create_task(_periodic(settings.usage_flush_seconds,
                                              lambda: core.usage.flush(factory), 'usage flush')),
                asyncio.create_task(_periodic(settings.usage_flush_seconds,
                                              core.predictor.cache.log_stats_if_changed, 'cache stats')),
            ]
        yield
        stop.set()
        if worker_thread is not None:
            worker_thread.join(timeout=10)
        for t in core.tasks:
            t.cancel()
        try:
            core.usage.flush(factory)
        except Exception as exc:
            log.error('final usage flush failed: %s', type(exc).__name__)

    app = FastAPI(
        title='Degron Footprint API', version=__version__, lifespan=lifespan,
        docs_url='/docs' if settings.enable_docs else None,
        redoc_url=None, openapi_url='/openapi.json' if settings.enable_docs else None)
    app.state.core = core

    contract = load_contract(settings.openapi_contract)
    if contract is not None:                       # the served documentation is the contract, not a re-derivation
        app.openapi = lambda: contract             # type: ignore[method-assign]

    errors.install(app)
    app.include_router(predict.router)
    app.include_router(runs.router)
    app.include_router(reference.router)
    app.include_router(model_compare.router)        # before projects: /v1/analyses/compare is a static path
    app.include_router(projects.router)
    app.include_router(jobs.router)
    app.include_router(datasets.router)
    app.include_router(health.router)
    app.include_router(admin.router)
    app.add_middleware(CoreMiddleware, core=core)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware, allow_origins=settings.allowed_origins, allow_methods=['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['Content-Type', 'X-Share-Token'],
        expose_headers=['X-Request-Id', 'Content-Disposition', 'Retry-After'], max_age=600)
    return app
