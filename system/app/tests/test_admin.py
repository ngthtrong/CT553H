"""Local admin page (plan-system 4.2): OPS-04…06."""
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

from db.models import WorkerHeartbeat
from db.session import make_engine, make_session_factory
from tests.conftest import mk_client
from tests.contract import check
from tests.test_jobs import SEQ, SEQ2, worker

LOCAL = {'X-Forwarded-For': '127.0.0.1'}


def _client(mini, dbcopy, tmp_path):
    return mk_client(mini, dbcopy, trust_proxy=True, workspace_dir=tmp_path / 'ws')


def test_ops06_only_allowed_networks(mini, dbcopy, tmp_path):
    c, _ = _client(mini, dbcopy, tmp_path)
    assert c.get('/v1/admin/status', headers=LOCAL).status_code == 200
    r = c.get('/v1/admin/status', headers={'X-Forwarded-For': '203.0.113.9'})
    assert r.status_code == 403 and r.json()['code'] == 'LOCAL_ONLY'
    assert c.post('/v1/admin/registry/reload', headers={'X-Forwarded-For': '203.0.113.9'}).status_code == 403
    assert c.get('/v1/admin/status', headers={'X-Forwarded-For': 'not-an-ip'}).status_code == 403
    c2, _ = mk_client(mini, dbcopy)                                       # no proxy: TestClient address is not an IP
    assert c2.get('/v1/admin/status').status_code == 403
    c3, _ = mk_client(mini, dbcopy, trust_proxy=True, admin_allowed_networks=['172.16.0.0/12'])
    assert c3.get('/v1/admin/status', headers={'X-Forwarded-For': '172.19.0.1'}).status_code == 200
    assert c3.get('/v1/admin/status', headers=LOCAL).status_code == 403


def test_ops04_worker_and_queue_states_and_ops05_no_biological_payload(mini, dbcopy, tmp_path):
    c, app = _client(mini, dbcopy, tmp_path)
    pid = c.post('/v1/projects', json={'name': 'admin'}).json()['project_id']
    c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'peptides', 'peptides': [
        {'input_id': 'secret-input-id', 'sequence': SEQ}, {'input_id': 'b', 'sequence': SEQ2}]})
    st = c.get('/v1/admin/status', headers=LOCAL).json()
    check('AdminStatus', st)
    assert st['queue']['items_pending'] == 2 and st['workers']['alive'] == 0 and 'warning' in st['workers']
    assert st['schema_revision'] == '0008' and st['models']['default_model_id'] == 'test-model-v1'
    w = worker(app, owner='host:1:abc')
    w.heartbeat(force=True)
    w.drain()
    w.heartbeat(force=True)                      # counts are written with the next beat (every 5 s while running)
    st = c.get('/v1/admin/status', headers=LOCAL).json()
    assert st['queue']['items_pending'] == 0 and st['workers']['alive'] == 1
    rec = next(x for x in st['workers']['recent'] if x['owner'] == 'host:1:abc')
    assert rec['alive'] is True and rec['items_done'] == 2
    # the worker stops: stamped, no longer alive; a silent worker becomes not alive after 30 s
    w.heartbeat(stopped=True)
    st = c.get('/v1/admin/status', headers=LOCAL).json()
    assert st['workers']['alive'] == 0
    eng = make_engine(dbcopy)
    with make_session_factory(eng)() as s, s.begin():
        s.add(WorkerHeartbeat(owner='old:2:def', started_at=datetime.now(UTC) - timedelta(hours=1),
                              last_seen_at=datetime.now(UTC) - timedelta(seconds=45), items_done=3))
    eng.dispose()
    st = c.get('/v1/admin/status', headers=LOCAL).json()
    assert next(x for x in st['workers']['recent'] if x['owner'] == 'old:2:def')['alive'] is False
    assert st['cache']['mode'] == 'memory' and st['storage']['database_bytes'] > 0
    text = json.dumps(st)
    for needle in (SEQ, SEQ2, 'secret-input-id'):
        assert needle not in text                                         # OPS-05


def test_registry_reload_rechecks_hashes(mini, dbcopy, tmp_path):
    c, app = _client(mini, dbcopy, tmp_path)
    r = c.post('/v1/admin/registry/reload', headers=LOCAL)
    assert r.status_code == 200 and r.json()['models']['loaded'][0]['model_id'] == 'test-model-v1'
