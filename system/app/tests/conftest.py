from __future__ import annotations

import os
import shutil
import sys
import uuid
import warnings
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP / 'backend'))
sys.path.insert(0, str(APP))
warnings.filterwarnings('ignore', category=DeprecationWarning)

from fastapi.testclient import TestClient  # noqa: E402

from api.config import Settings  # noqa: E402
from api.main import create_app  # noqa: E402
from etl import load as etl  # noqa: E402
from tests import minidata  # noqa: E402

TOPIC = next((p for p in APP.parents if (p / 'data' / 'README.md').exists()), None)
REAL = TOPIC is not None and (TOPIC / 'data/processed/calibration-p6-model.npz').exists()
CONTRACT = APP.parent / 'openapi.yaml'


# WP8: the same suite on PostgreSQL 16. DF_TEST_BACKEND=postgresql with DF_TEST_PG_URL pointing at a database whose
# role may CREATE DATABASE (the local Docker container: postgres:16-alpine, superuser `degron`).
BACKEND = os.environ.get('DF_TEST_BACKEND', 'sqlite')
PG_ADMIN = os.environ.get('DF_TEST_PG_URL')
if BACKEND == 'postgresql' and not PG_ADMIN:
    raise RuntimeError('DF_TEST_BACKEND=postgresql needs DF_TEST_PG_URL')


def pytest_configure(config):
    config.addinivalue_line('markers', 'sqlite_only: reads the SQLite file or uses SQLite-only statements')


def pytest_collection_modifyitems(config, items):
    skip_real = pytest.mark.skip(reason='real research data not present')
    skip_pg = pytest.mark.skip(reason='SQLite-specific check; not applicable on PostgreSQL')
    for item in items:
        if 'realdata' in item.keywords and (not REAL or BACKEND == 'postgresql'):
            item.add_marker(skip_real)
        if 'sqlite_only' in item.keywords and BACKEND == 'postgresql':
            item.add_marker(skip_pg)


def _pg_admin():
    from sqlalchemy import create_engine
    return create_engine(PG_ADMIN, isolation_level='AUTOCOMMIT')


def _pg_url(name: str) -> str:
    return PG_ADMIN.rsplit('/', 1)[0] + '/' + name


def pg_create(template: str | None = None) -> str:
    """A new empty (or template-copied) PostgreSQL database; returns its URL."""
    from sqlalchemy import text as _text
    name = f'df_test_{uuid.uuid4().hex[:12]}'
    eng = _pg_admin()
    with eng.connect() as c:
        c.execute(_text(f'CREATE DATABASE {name}' + (f' TEMPLATE {template}' if template else '')))
    eng.dispose()
    return _pg_url(name)


def pg_drop(url: str) -> None:
    from sqlalchemy import text as _text
    eng = _pg_admin()
    with eng.connect() as c:
        c.execute(_text(f'DROP DATABASE IF EXISTS {url.rsplit("/", 1)[1]} WITH (FORCE)'))
    eng.dispose()


def fresh_db_url(tmp_path, name: str = 'e.db') -> str:
    """An empty database of the backend under test (SQLite file, or a new PostgreSQL database)."""
    return pg_create() if BACKEND == 'postgresql' else f'sqlite:///{tmp_path / name}'


@pytest.fixture(scope='session')
def mini(tmp_path_factory):
    return minidata.build(tmp_path_factory.mktemp('mini'))


@pytest.fixture(scope='session')
def mini_db(mini, tmp_path_factory):
    """The miniature tree loaded by the real ETL (ClinVar scope 'all'): a SQLite file, or on PostgreSQL a template
    database that nothing stays connected to (copies are made from it with CREATE DATABASE … TEMPLATE)."""
    from alembic import command
    from alembic.config import Config

    from db.session import make_engine
    path = tmp_path_factory.mktemp('db') / 'mini.db'
    url = pg_create() if BACKEND == 'postgresql' else f'sqlite:///{path}'
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')
    engine = make_engine(url)
    report = etl.run(url, mini['topic'], mini['sources'], mini['params'], 'all', mini['model_dir'], engine=engine)
    engine.dispose()
    if BACKEND != 'postgresql':
        yield {'url': url, 'path': path, 'report': report, 'template': None}
        return
    template = url.rsplit('/', 1)[1]
    shared = pg_create(template)            # what tests read directly; the template itself stays unconnected
    yield {'url': shared, 'path': None, 'report': report, 'template': template}
    pg_drop(shared)
    pg_drop(url)


def copy_db(mini_db, tmp_path) -> str:
    """URL of a private copy of the loaded database."""
    if BACKEND == 'postgresql':
        return pg_create(mini_db['template'])
    path = tmp_path / f'copy-{uuid.uuid4().hex[:6]}.db'
    shutil.copy(mini_db['path'], path)
    return f'sqlite:///{path}'


def settings_for(mini, url, **kw) -> Settings:
    base = dict(database_url=url, model_dir=mini['model_dir'], background_jobs=False, openapi_contract=CONTRACT,
                rate_limit_predict=100000, rate_limit_reference=100000)
    base.update(kw)
    return Settings(**base)


@pytest.fixture(scope='session')
def client(mini, mini_db, tmp_path_factory):
    app = create_app(settings_for(mini, mini_db['url']))
    with TestClient(app) as c:
        yield c


def mk_client(mini, url, **kw):
    app = create_app(settings_for(mini, url, **kw))
    return TestClient(app), app


@pytest.fixture()
def dbcopy(mini_db, tmp_path):
    """URL of a private copy of the loaded database, for tests that write or tamper."""
    url = copy_db(mini_db, tmp_path)
    yield url
    if BACKEND == 'postgresql':
        pg_drop(url)


@pytest.fixture(scope='session')
def r3_gate(tmp_path_factory):
    """The frozen R3 gate with the application's own card (as the ETL writes it)."""
    import json as _json

    from degron_footprint.gate_r3 import R3Gate, card_for
    root = next(p for p in APP.parents if (p / 'CLAUDE.md').exists())
    src = root / 'research/r3-domain-gate-2026-10-22/run-kaggle-20261022'
    d = tmp_path_factory.mktemp('gate')
    w = d / 'gate-r3-v1.npz'
    shutil.copyfile(src / 'gate-weights.npz', w)
    return R3Gate(w, card_for(w, 'gate-r3-v1', _json.loads((src / 'gate-card.json').read_text(encoding='utf-8'))))


def db_contains(url: str, needle: str) -> bool:
    """Whether any stored byte sequence contains `needle`: the SQLite file, or every row of every PostgreSQL table
    rendered as text (SEC-01/SEC-04 on both back-ends)."""
    if url.startswith('sqlite:///'):
        return needle.encode() in open(url.removeprefix('sqlite:///'), 'rb').read()
    from sqlalchemy import create_engine, inspect
    from sqlalchemy import text as _text
    eng = create_engine(url)
    try:
        with eng.connect() as c:
            for t in inspect(eng).get_table_names():
                if c.execute(_text(f'SELECT 1 FROM "{t}" x WHERE x::text LIKE :n LIMIT 1'),
                             {'n': f'%{needle}%'}).first():
                    return True
        return False
    finally:
        eng.dispose()
