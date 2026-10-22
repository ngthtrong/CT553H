from __future__ import annotations

import shutil
import sys
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


def pytest_collection_modifyitems(config, items):
    if REAL:
        return
    skip = pytest.mark.skip(reason='real research data not present')
    for item in items:
        if 'realdata' in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope='session')
def mini(tmp_path_factory):
    return minidata.build(tmp_path_factory.mktemp('mini'))


@pytest.fixture(scope='session')
def mini_db(mini, tmp_path_factory):
    """A SQLite file loaded by the real ETL from the miniature tree (ClinVar scope 'all')."""
    from alembic import command
    from alembic.config import Config
    path = tmp_path_factory.mktemp('db') / 'mini.db'
    url = f'sqlite:///{path}'
    cfg = Config(str(APP / 'backend/alembic.ini'))
    cfg.set_main_option('sqlalchemy.url', url)
    command.upgrade(cfg, 'head')
    report = etl.run(url, mini['topic'], mini['sources'], mini['params'], 'all', mini['model_dir'])
    return {'url': url, 'path': path, 'report': report}


def settings_for(mini, url, **kw) -> Settings:
    base = dict(database_url=url, model_dir=mini['model_dir'], background_jobs=False, openapi_contract=CONTRACT,
                rate_limit_predict=100000, rate_limit_reference=100000)
    base.update(kw)
    return Settings(**base)


@pytest.fixture(scope='session')
def client(mini, mini_db):
    app = create_app(settings_for(mini, mini_db['url']))
    with TestClient(app) as c:
        yield c


def mk_client(mini, url, **kw):
    app = create_app(settings_for(mini, url, **kw))
    return TestClient(app), app


@pytest.fixture()
def dbcopy(mini_db, tmp_path):
    """URL of a private copy of the loaded database, for tests that write or tamper."""
    path = tmp_path / 'copy.db'
    shutil.copy(mini_db['path'], path)
    return f'sqlite:///{path}'
