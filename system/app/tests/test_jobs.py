"""WP5: durable jobs and the worker (UC-08; BATCH-01…06 of test-plan.md), on private copies of the mini database."""
from __future__ import annotations

import csv
import io
import json
import logging
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select

from api.worker import Worker, from_core
from db.models import AnalysisRun, JobItem
from db.session import make_engine

from .conftest import mk_client
from .contract import check

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
SEQ2 = 'MKTAYIAKQRQISFVKSHFSRQLEERLG'


@pytest.fixture()
def wc(mini, dbcopy, tmp_path):
    c, app = mk_client(mini, dbcopy, workspace_dir=tmp_path / 'ws')
    with c:
        yield c, app, dbcopy


def project(c) -> str:
    return c.post('/v1/projects', json={'name': 'jobs'}).json()['project_id']


def submit(c, pid, **body):
    return c.post(f'/v1/projects/{pid}/jobs', json=body)


def items(c, job_id, limit=200):
    page = c.get(f'/v1/jobs/{job_id}/items?limit={limit}').json()
    check('JobItemPage', page)
    return page['items']


def worker(app, owner=None) -> Worker:
    return from_core(app.state.core, owner)


def n_runs(url) -> int:
    with make_engine(url).connect() as conn:
        return conn.execute(select(func.count()).select_from(AnalysisRun)).scalar()


# --- BATCH-01 -------------------------------------------------------------------------------------------------------

def test_batch01_peptide_input_and_preview_counts(wc):
    c, app, _ = wc
    pid = project(c)
    r = submit(c, pid, mode='peptides', peptides=[
        {'input_id': 'a', 'sequence': SEQ}, {'input_id': 'b', 'sequence': 'ACD'},
        {'input_id': 'c', 'sequence': SEQ.lower()}, {'input_id': 'd', 'sequence': SEQ[:27] + 'X'}])
    assert r.status_code == 202, r.text
    job = r.json()
    check('Job', job)
    assert job['state'] == 'pending' and job['total'] == 4
    assert job['configuration_snapshot']['input_summary'] == {'inputs': 4, 'valid': 2, 'invalid': 2,
                                                              'duplicate_sequences': 1}
    got = items(c, job['job_id'])
    assert [i['item_id'] for i in got] == ['p0001', 'p0002', 'p0003', 'p0004']
    assert [i['state'] for i in got] == ['pending', 'refused', 'pending', 'refused']
    assert got[1]['error']['code'] == 'INVALID_LENGTH' and got[3]['error']['code'] == 'INVALID_CHARACTER'
    worker(app).drain()
    done = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert done['state'] == 'partial'
    assert done['counts'] == {'pending': 0, 'running': 0, 'succeeded': 2, 'refused': 2, 'failed': 0, 'cancelled': 0}


@pytest.mark.parametrize('body, code', [
    ({'mode': 'peptides', 'peptides': []}, 'INVALID_REQUEST'),
    ({'mode': 'peptides', 'peptides': [{'input_id': 'a', 'sequence': SEQ}, {'input_id': 'a', 'sequence': SEQ}]},
     'INVALID_REQUEST'),
    ({'mode': 'peptides', 'peptides': [{'input_id': f'p{i}', 'sequence': SEQ} for i in range(101)]},
     'PAYLOAD_TOO_LARGE'),
    ({'mode': 'protein', 'protein': {'uniprot_id': 'P12345', 'sequence': SEQ}}, 'INVALID_REQUEST'),
    ({'mode': 'protein', 'protein': {'uniprot_id': 'Q99999'}}, 'UNKNOWN_ACCESSION'),
    ({'mode': 'protein', 'protein': {'input_id': 'x', 'sequence': 'A' * 10001}}, 'PAYLOAD_TOO_LARGE'),
    ({'mode': 'protein', 'protein': {'input_id': 'x', 'sequence': 'ACDE1FGH' * 5}}, 'INVALID_CHARACTER'),
    ({'mode': 'protein', 'protein': {'uniprot_id': 'P12345', 'reference_release': '1999_01'}}, 'INVALID_REQUEST'),
    ({'mode': 'batch'}, 'INVALID_REQUEST'),
    ({'mode': 'peptides', 'peptides': [{'input_id': 'a', 'sequence': SEQ}], 'priority': 1}, 'INVALID_REQUEST'),
])
def test_batch01_invalid_submissions(wc, body, code):
    c, _, url = wc
    pid = project(c)
    r = submit(c, pid, **body)
    assert r.json()['code'] == code
    with make_engine(url).connect() as conn:
        assert conn.execute(select(func.count()).select_from(JobItem)).scalar() == 0


# --- BATCH-02 -------------------------------------------------------------------------------------------------------

def test_batch02_configuration_is_pinned(wc):
    c, app, _ = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', calibrator='iso', peptides=[{'input_id': 'a', 'sequence': SEQ}]).json()
    cfg = job['configuration_snapshot']
    lm = app.state.core.registry.default
    assert cfg['model_id'] == lm.info.model_id and cfg['weights_sha256'] == lm.info.weights_sha256
    assert cfg['calibrator'] == 'iso' and cfg['gate_model_id'] == 'gate-r3-v1'
    assert cfg['gate_sha256'] == app.state.core.gate.weights_sha256
    assert {s['source_id'] for s in cfg['sources']} >= {'uniprot-2026_03'}
    # the serving model changes after submission: the item is not scored with different weights
    lm.info = type(lm.info)(**{**lm.info.__dict__, 'weights_sha256': 'f' * 64})
    worker(app).drain()
    got = items(c, job['job_id'])
    assert got[0]['state'] == 'failed' and got[0]['error']['code'] == 'MODEL_NOT_FOUND'


def test_batch02_results_match_single_tile_scoring(wc):
    """Every tile scored by a job equals the stateless single-tile prediction (plan WP5 criterion)."""
    c, app, _ = wc
    pid = project(c)
    job = submit(c, pid, mode='protein', protein={'uniprot_id': 'P12345'}, override_domain=True).json()
    worker(app).drain()
    for it in items(c, job['job_id']):
        if it['state'] != 'succeeded':
            continue
        saved = c.get(f"/v1/analyses/{it['analysis_id']}").json()['result']
        single = c.post('/v1/predict', json={'uniprot_id': 'P12345', 'tile_index': it['tile_index'],
                                             'override_domain': True}).json()
        assert saved['cells'] == single['cells']
        assert saved['domain']['status'] == single['domain']['status'] == it['domain_status']


# --- BATCH-03 -------------------------------------------------------------------------------------------------------

def test_batch03_cancel_keeps_finished_items_and_is_idempotent(wc):
    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(4)]).json()
    w = worker(app)
    w.run_once()                                                     # p0001 succeeds
    claimed = w.claim()                                              # p0002 held by a live worker
    first = c.post(f"/v1/jobs/{job['job_id']}/cancel")
    assert first.status_code == 202
    assert first.json()['cancel_requested'] is True and first.json()['state'] == 'running'
    assert w.process(*claimed).state == 'cancelled'                  # the in-flight item is not written
    again = c.post(f"/v1/jobs/{job['job_id']}/cancel").json()
    assert again['state'] == 'cancelled'
    assert again['counts']['succeeded'] == 1 and again['counts']['cancelled'] == 3
    assert n_runs(url) == 1
    assert w.claim() is None


def test_batch03_completed_job_cannot_be_cancelled(wc):
    c, app, _ = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': 'a', 'sequence': SEQ}]).json()
    worker(app).drain()
    assert c.get(f"/v1/jobs/{job['job_id']}").json()['state'] == 'completed'
    r = c.post(f"/v1/jobs/{job['job_id']}/cancel")
    assert r.status_code == 409 and r.json()['code'] == 'JOB_STATE_CONFLICT'


# --- BATCH-04 -------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize('length, tiles, uncovered', [(28, 1, []), (50, 1, [{'start': 29, 'end': 50}]),
                                                      (51, 2, []), (52, 2, [{'start': 52, 'end': 52}])])
def test_batch04_typed_protein_tiling(wc, length, tiles, uncovered):
    c, _, _ = wc
    pid = project(c)
    seq = (SEQ * 3)[:length]
    job = submit(c, pid, mode='protein', protein={'input_id': 'fasta-1', 'sequence': seq}).json()
    assert job['total'] == tiles and job['coverage']['uncovered'] == uncovered
    assert job['coverage']['uniprot_id'] is None                      # typed: never given an accession
    got = items(c, job['job_id'])
    assert [(i['start_pos'], i['end_pos']) for i in got] == [((n - 1) * 23 + 1, (n - 1) * 23 + 28)
                                                             for n in range(1, tiles + 1)]


def test_batch04_shorter_than_one_tile(wc):
    c, _, _ = wc
    r = submit(c, project(c), mode='protein', protein={'input_id': 'x', 'sequence': SEQ[:27]})
    assert r.status_code == 422 and r.json()['code'] == 'INVALID_LENGTH'


def test_batch04_unscorable_window_and_out_of_domain_do_not_fail_the_job(wc):
    c, app, _ = wc
    pid = project(c)
    p2 = submit(c, pid, mode='protein', protein={'uniprot_id': 'P22222'}).json()
    assert p2['coverage']['unscorable_windows'] == [{'tile_index': 4, 'start': 70, 'end': 97}]
    p1 = submit(c, pid, mode='protein', protein={'uniprot_id': 'P12345'}).json()
    worker(app).drain()
    by_tile = {i['tile_index']: i for i in items(c, p1['job_id'])}
    assert by_tile[2]['state'] == 'refused' and by_tile[2]['error']['code'] == 'OUT_OF_DOMAIN'
    assert by_tile[1]['state'] == 'succeeded'
    assert c.get(f"/v1/jobs/{p1['job_id']}").json()['state'] == 'partial'
    assert items(c, p2['job_id'])[3]['error']['code'] == 'TILE_NOT_SCORABLE'


def test_batch04_window_keeps_protein_coordinates(wc):
    c, app, _ = wc
    pid = project(c)
    job = submit(c, pid, mode='protein', protein={'input_id': 'fasta', 'sequence': SEQ + SEQ2}).json()
    worker(app).drain()
    it = items(c, job['job_id'])[1]
    snap = c.get(f"/v1/analyses/{it['analysis_id']}").json()['snapshot']
    assert snap['protein_window'] == {'input_id': 'fasta', 'tile_index': 2, 'start_pos': 24, 'end_pos': 51,
                                      'uniprot_id': None, 'reference_release': None}


# --- BATCH-05 -------------------------------------------------------------------------------------------------------

def test_batch05_crashed_worker_lease_is_reclaimed_without_duplicates(wc):
    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(3)]).json()
    dead = worker(app, 'dead-worker')
    held = dead.claim()                                              # claimed, then the process "dies"
    live = worker(app, 'live-worker')
    assert live.claim(datetime.now(UTC)) != held                     # a live lease is respected
    later = datetime.now(UTC) + timedelta(seconds=app.state.core.settings.job_lease_seconds + 5)
    with make_engine(url).begin() as conn:                           # release the item claimed just above
        conn.execute(JobItem.__table__.update().where(JobItem.lease_owner == 'live-worker')
                     .values(state='pending', lease_owner=None, lease_expires_at=None))
    order = []
    while (got := live.claim(later)) is not None:
        order.append(got)
        assert live.process(*got).state == 'succeeded'
    assert held in order                                             # the expired lease was reclaimed
    assert dead.process(*held).state == 'lost'                       # the late commit of the dead worker is refused
    final = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert final['state'] == 'completed' and final['counts']['succeeded'] == 3
    assert n_runs(url) == 3


def test_batch05_restart_resumes_the_same_job(mini, wc):
    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(3)]).json()
    worker(app).run_once()
    c2, app2 = mk_client(mini, url)                                  # API and worker restarted on the same database
    with c2:
        assert c2.get(f"/v1/jobs/{job['job_id']}").json()['counts']['succeeded'] == 1
        done = worker(app2).drain()
        assert len(done) == 2
        assert c2.get(f"/v1/jobs/{job['job_id']}").json()['state'] == 'completed'
    assert n_runs(url) == 3


def test_batch05_project_deletion_blocks_late_worker_writes(wc):
    c, app, url = wc
    pid = project(c)
    submit(c, pid, mode='peptides', peptides=[{'input_id': 'a', 'sequence': SEQ}, {'input_id': 'b', 'sequence': SEQ}])
    w = worker(app)
    held = w.claim()
    assert c.delete(f'/v1/projects/{pid}?confirm=true').status_code == 204
    assert w.process(*held).state == 'lost'
    assert w.claim() is None
    assert n_runs(url) == 0


# --- BATCH-06 -------------------------------------------------------------------------------------------------------

def test_batch06_export_covers_every_item(wc):
    c, app, _ = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': '=cmd|calc', 'sequence': SEQ},
                                                     {'input_id': 'short', 'sequence': 'ACD'}]).json()
    worker(app).drain()
    text = c.get(f"/v1/jobs/{job['job_id']}/export?format=csv").text
    rows = list(csv.reader(io.StringIO('\n'.join(ln for ln in text.splitlines() if not ln.startswith('#')))))
    header, body = rows[0], rows[1:]
    assert header[:9] == ['peptide', 'tile', 'position', 'wt_aa', 'mut_aa', 'score_dpsi_raw',
                          'p_dpsi_ge_1_calibrated', 'rank_in_tile', 'top10pct_in_tile']
    # plan-system 1.3: the seed spread follows the nine FR-12 columns (empty for the npz model)
    assert header[9:12] == ['score_seed_sd', 'score_seed_min', 'score_seed_max']
    assert header[12:] == ['project_id', 'job_id', 'item_id', 'input_id', 'uniprot_id', 'reference_release',
                           'start_pos', 'end_pos', 'protein_position', 'status', 'error_code', 'domain_status']
    assert len(body) == 532 + 1
    assert body[0][9:12] == ['', '', '']
    assert body[0][15] == "'=cmd|calc"                                 # formula neutralised (SEC-02)
    assert body[-1][14] == 'p0002'
    assert body[-1][:12] == [''] * 12 and body[-1][-3:-1] == ['refused', 'INVALID_LENGTH']
    payload = json.loads(c.get(f"/v1/jobs/{job['job_id']}/export?format=json").text)
    assert len(payload['manifest']) == 2 and len(payload['analyses']) == 1
    assert len(payload['analyses'][0]['result']['cells']) == 532


def test_batch_logs_hold_no_sequence(wc, caplog):
    c, app, _ = wc
    caplog.set_level(logging.INFO)
    pid = project(c)
    submit(c, pid, mode='protein', protein={'input_id': 'secret-fasta', 'sequence': SEQ + SEQ2})
    worker(app).drain()
    assert SEQ not in caplog.text and SEQ2 not in caplog.text
    assert 'job finished' in caplog.text


def test_job_listing(wc):
    c, _, _ = wc
    pid = project(c)
    a = submit(c, pid, mode='peptides', peptides=[{'input_id': 'a', 'sequence': SEQ}]).json()
    b = submit(c, pid, mode='peptides', peptides=[{'input_id': 'b', 'sequence': SEQ}]).json()
    page = c.get(f'/v1/projects/{pid}/jobs').json()
    check('JobPage', page)
    assert [j['job_id'] for j in page['items']] == [b['job_id'], a['job_id']]
    assert c.get(f'/v1/projects/{pid}').json()['counts']['jobs'] == 2


@pytest.mark.slow
def test_batch05_sigkill_worker_process_then_restart(mini, wc):
    """The WP5 acceptance check with a real process: SIGKILL the worker mid-job, start a new one, and the job
    finishes with every item counted once and one saved analysis per succeeded item."""
    import os
    import signal
    import subprocess
    import sys
    import time
    from pathlib import Path

    c, _, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(100)]).json()
    app_dir = Path(__file__).resolve().parents[1]
    env = {**os.environ, 'DF_DATABASE_URL': url, 'DF_MODEL_DIR': str(mini['model_dir']), 'DF_JOB_LEASE_SECONDS': '1',
           'DF_WORKER_POLL_SECONDS': '0.05', 'PYTHONPATH': str(app_dir / 'backend')}

    def succeeded() -> int:
        with make_engine(url).connect() as conn:
            return conn.execute(select(func.count()).select_from(JobItem).where(
                JobItem.state == 'succeeded')).scalar()

    proc = subprocess.Popen([sys.executable, '-m', 'api.worker'], cwd=app_dir / 'backend', env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 60
    while succeeded() < 3 and time.monotonic() < deadline:
        time.sleep(0.01)
    proc.send_signal(signal.SIGKILL)
    proc.wait()
    at_kill = succeeded()
    assert 3 <= at_kill < 100, at_kill
    time.sleep(1.5)                                                  # the dead worker's lease expires
    subprocess.run([sys.executable, '-m', 'api.worker', '--drain'], cwd=app_dir / 'backend', env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    final = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert final['state'] == 'completed' and final['counts']['succeeded'] == 100
    assert n_runs(url) == 100


def test_two_workers_in_parallel_process_each_item_once(wc):
    """WP8.6 / A-4: two workers draining one queue at the same time (SKIP LOCKED + compare-and-set on PostgreSQL,
    serialised writes on SQLite). Every item is processed exactly once and no analysis is duplicated."""
    import threading

    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(60)]).json()
    results: dict[str, list] = {'a': [], 'b': []}
    errors: list[BaseException] = []

    def run(name):
        try:
            results[name] = worker(app, f'worker-{name}').drain()
        except BaseException as exc:                                  # surfaced below
            errors.append(exc)
    threads = [threading.Thread(target=run, args=(n,)) for n in ('a', 'b')]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)
    assert not errors, errors
    done = [(p.job_id, p.item_id) for p in results['a'] + results['b'] if p.state == 'succeeded']
    assert len(done) == len(set(done)) == 60
    final = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert final['state'] == 'completed' and final['counts']['succeeded'] == 60
    assert n_runs(url) == 60


@pytest.mark.slow
def test_cancel_racing_a_live_worker_always_ends_cancelled(wc):
    """Regression (17 Nov 2026, NF-07 run): a cancellation committed while the worker was finishing an item left the
    job `partial`, because the worker read the cancel flag before taking the write lock. Repeated race, real thread."""
    import threading
    import time

    c, app, _ = wc
    pid = project(c)
    for attempt in range(15):
        job = submit(c, pid, mode='peptides', peptides=[{'input_id': f'p{i}', 'sequence': SEQ} for i in range(40)]).json()
        stop = threading.Event()
        w = worker(app, f'race-{attempt}')
        w.settings.worker_poll_seconds = 0.01
        t = threading.Thread(target=w.run, args=(stop,), daemon=True)
        t.start()
        while c.get(f"/v1/jobs/{job['job_id']}").json()['counts']['succeeded'] < 2 + attempt % 5:
            time.sleep(0.002)
        c.post(f"/v1/jobs/{job['job_id']}/cancel")
        deadline = time.monotonic() + 20
        while (state := c.get(f"/v1/jobs/{job['job_id']}").json())['state'] not in ('cancelled', 'partial', 'completed', 'failed'):
            assert time.monotonic() < deadline
            time.sleep(0.005)
        stop.set()
        t.join(timeout=5)
        assert state['state'] == 'cancelled', (attempt, state['counts'])
        assert state['counts']['succeeded'] + state['counts']['cancelled'] == 40


@pytest.mark.slow
def test_whole_protein_windows_match_the_reference_tiles(mini, tmp_path):
    """plan.md 2.5: on a copy of the real dev.db, every window of a whole-protein job has the 1-based coordinates and
    the sequence of the stored `tile` row with the same index (482,216 tiles from the ETL)."""
    import shutil
    import sqlite3
    from pathlib import Path

    from fastapi.testclient import TestClient

    from api.config import Settings
    from api.main import create_app

    src = Path(__file__).resolve().parents[1] / '.data/dev.db'
    if not src.exists():
        pytest.skip('.data/dev.db not present')
    db = tmp_path / 'dev.db'
    shutil.copy(src, db)
    from alembic import command

    from tests.test_workspace_schema import alembic_cfg
    command.upgrade(alembic_cfg(f'sqlite:///{db}'), 'head')       # the copy may be older than the code (0005: 18 Nov)
    app = create_app(Settings(database_url=f'sqlite:///{db}', workspace_dir=tmp_path / 'ws', background_jobs=False,
                              openapi_contract=None, rate_limit_predict=10**6, rate_limit_reference=10**6))
    with TestClient(app) as c:
        pid = c.post('/v1/projects', json={'name': 'tiles'}).json()['project_id']
        con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        for acc in ('P60484', 'A6NMZ7', 'Q8NF91'):
            job = c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'protein', 'protein': {'uniprot_id': acc}}).json()
            ref = {r[0]: r[1:] for r in con.execute(
                'SELECT tile_index, start_pos, end_pos, sequence FROM tile WHERE uniprot_acc = ? ORDER BY tile_index', (acc,))}
            items = c.get(f"/v1/jobs/{job['job_id']}/items?limit=200").json()
            got = list(items['items'])
            while len(got) < items['total']:
                got += c.get(f"/v1/jobs/{job['job_id']}/items?offset={len(got)}&limit=200").json()['items']
            assert job['total'] == len(ref), acc
            for it in got:
                start, end, seq = ref[it['tile_index']]
                assert (it['start_pos'], it['end_pos']) == (start, end), (acc, it['tile_index'])
            con2 = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
            stored = dict(con2.execute('SELECT tile_index, sequence FROM job_item WHERE job_id = ? AND sequence IS NOT NULL',
                                       (job['job_id'],)).fetchall())
            con2.close()
            assert all(stored[i] == ref[i][2] for i in stored), acc
        con.close()


# --- BATCH-08 (plan-system 1.7): ETA from measured item times ----------------------------------------------------------

def test_batch08_eta_from_measured_items_and_null_when_not_enough_or_finished(wc):
    c, app, url = wc
    pid = project(c)
    peptides = [{'input_id': f'p{i}', 'sequence': s} for i, s in enumerate([SEQ, SEQ2] * 4)]
    job = submit(c, pid, mode='peptides', peptides=peptides).json()
    check('Job', job)
    assert job['eta_seconds'] is None                                   # nothing measured yet
    w = worker(app)
    w.run_once()
    w.run_once()
    assert c.get(f"/v1/jobs/{job['job_id']}").json()['eta_seconds'] is None      # 2 < ETA_MIN_SAMPLES
    w.run_once()
    j = c.get(f"/v1/jobs/{job['job_id']}").json()
    check('Job', j)
    with make_engine(url).connect() as conn:
        ms = conn.execute(select(JobItem.duration_ms).where(JobItem.job_id == job['job_id'],
                                                            JobItem.duration_ms.is_not(None))).scalars().all()
    assert len(ms) == 3 and all(x > 0 for x in ms)
    open_ = j['counts']['pending'] + j['counts']['running']
    assert open_ == 5 and j['eta_seconds'] == round(sum(ms) / 3 / 1000 * open_, 1)
    w.drain()
    done = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert done['state'] == 'completed' and done['eta_seconds'] is None
    # the model list falls back to the median item time of recent jobs when this process has not scored yet
    app.state.core.predictor._timings.clear()                           # as if the worker were another process
    secs = next(m for m in c.get('/v1/models').json()['items'] if m['model_id'] == 'test-model-v1')
    assert secs['expected_tile_seconds'] is not None and secs['expected_tile_seconds'] > 0


def test_batch08_refused_items_have_no_duration(wc):
    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=[{'input_id': 'bad', 'sequence': 'ACD'}]).json()
    assert job['state'] == 'failed' and job['eta_seconds'] is None
    with make_engine(url).connect() as conn:
        assert conn.execute(select(JobItem.duration_ms).where(JobItem.job_id == job['job_id'])).scalar() is None


# --- VIZ-01/02 (plan-system 2.1): protein footprint ---------------------------------------------------------------------

def test_viz01_viz02_protein_footprint_per_tile_without_averaging_overlaps(wc):
    c, app, _ = wc
    pid = project(c)
    prot = (SEQ + SEQ2) * 2 + 'ACDEFGHIK'                               # 121 residues: 5 windows (1–120), 121 uncovered
    job = submit(c, pid, mode='protein', override_domain=True,
                 protein={'input_id': 'typed-prot', 'sequence': prot}).json()
    r = c.get(f"/v1/jobs/{job['job_id']}/footprint")
    assert r.status_code == 409 and r.json()['code'] == 'JOB_STATE_CONFLICT'          # not finished yet
    worker(app).drain()
    r = c.get(f"/v1/jobs/{job['job_id']}/footprint")
    assert r.status_code == 200, r.text
    fp = r.json()
    check('JobFootprint', fp)
    assert fp['protein'] == {'input_id': 'typed-prot', 'uniprot_id': None, 'length': 121, 'tiles': 5}
    assert fp['uncovered'] == [{'start': 121, 'end': 121}]
    assert fp['label'].startswith('Each tile is scored independently')
    assert [t['tile_index'] for t in fp['tiles']] == [1, 2, 3, 4, 5]
    for t in fp['tiles']:
        assert t['state'] == 'succeeded' and len(t['positions']) == 28
        assert [p['protein_pos'] for p in t['positions']] == list(range(t['start_pos'], t['end_pos'] + 1))
        # VIZ-01: equal to the recomputation from the saved cells of that tile
        cells = c.get(f"/v1/analyses/{t['analysis_id']}").json()['result']['cells']
        for p in t['positions']:
            at = [x for x in cells if x['position'] == p['protein_pos'] - t['start_pos'] + 1]
            assert len(at) == 19
            assert abs(p['mean_prob'] - sum(x['p_dpsi_ge_1_calibrated'] for x in at) / 19) < 1e-9
            assert abs(p['mean_raw'] - sum(x['score_dpsi_raw'] for x in at) / 19) < 1e-9
    # VIZ-02: the 5 shared residues of consecutive windows appear in both tiles, each with its own value
    t1, t2 = fp['tiles'][0], fp['tiles'][1]
    shared = set(p['protein_pos'] for p in t1['positions']) & set(p['protein_pos'] for p in t2['positions'])
    assert shared == {24, 25, 26, 27, 28}
    v1 = {p['protein_pos']: p['mean_raw'] for p in t1['positions']}
    v2 = {p['protein_pos']: p['mean_raw'] for p in t2['positions']}
    assert any(v1[k] != v2[k] for k in shared)                       # context differs: no merged value
    assert sum(len(t['positions']) for t in fp['tiles']) == 5 * 28


def test_viz_footprint_refuses_peptide_jobs_and_keeps_unscored_tiles(wc):
    c, app, _ = wc
    pid = project(c)
    pep = submit(c, pid, mode='peptides', peptides=[{'input_id': 'a', 'sequence': SEQ}]).json()
    worker(app).drain()
    r = c.get(f"/v1/jobs/{pep['job_id']}/footprint")
    assert r.status_code == 409 and r.json()['code'] == 'JOB_STATE_CONFLICT'
    assert c.get('/v1/jobs/00000000-0000-4000-8000-000000000000/footprint').status_code == 404
    assert c.get('/v1/jobs/not-a-uuid/footprint').status_code == 422
    prot = SEQ + 'X' * 23 + SEQ2                                       # window 2 has non-standard residues
    job = submit(c, pid, mode='protein', override_domain=True, protein={'input_id': 'x', 'sequence': prot}).json()
    worker(app).drain()
    fp = c.get(f"/v1/jobs/{job['job_id']}/footprint").json()
    check('JobFootprint', fp)
    refused = [t for t in fp['tiles'] if t['state'] == 'refused']
    assert refused and all(t['positions'] == [] and t['analysis_id'] is None and t['training_peptide'] is None
                           for t in refused)


# --- BATCH-10 (plan-system 3.3): several proteins in one job -----------------------------------------------------------

def test_batch10_several_proteins_total_limit_and_isolated_failures(wc):
    c, app, _ = wc
    pid = project(c)
    p1 = (SEQ + SEQ2) * 2                                                    # 112 residues: 4 windows
    body = {'mode': 'protein', 'override_domain': True, 'proteins': [
        {'input_id': 'first', 'sequence': p1},
        {'uniprot_id': 'Q99999'},                                             # not loaded: refused, the others go on
        {'input_id': 'third', 'sequence': 'ACDEFGHIKL'},                     # shorter than one tile: refused
        {'uniprot_id': 'P12345'}]}
    r = submit(c, pid, **body)
    assert r.status_code == 202, r.text
    job = r.json()
    check('Job', job)
    cov = job['coverage']
    assert cov['version'] == 2 and [x['input_id'] for x in cov['proteins']] == ['first', 'Q99999', 'third', 'P12345']
    assert [x.get('refused') for x in cov['proteins']] == [None, 'UNKNOWN_ACCESSION', 'INVALID_LENGTH', None]
    worker(app).drain()
    its = items(c, job['job_id'])
    assert [i['item_id'] for i in its if i['input_id'] == 'first'] == ['p01t00001', 'p01t00002', 'p01t00003', 'p01t00004']
    refused = {i['input_id']: i['error']['code'] for i in its if i['item_id'].endswith('t00000')}
    assert refused == {'Q99999': 'UNKNOWN_ACCESSION', 'third': 'INVALID_LENGTH'}
    done = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert done['state'] == 'partial'
    assert done['counts']['succeeded'] == sum(1 for i in its if i['state'] == 'succeeded')
    assert sum(1 for i in its if i['input_id'] == 'first' and i['state'] == 'succeeded') == 4
    # manifest export carries the protein of every row (input_id column)
    text = c.get(f"/v1/jobs/{job['job_id']}/export?format=csv").text
    rows = list(csv.reader(io.StringIO('\n'.join(ln for ln in text.splitlines() if not ln.startswith('#')))))
    col = rows[0].index('input_id')
    assert {r[col] for r in rows[1:]} == {'first', 'Q99999', 'third', 'P12345'}
    # footprint, one protein at a time
    fp = c.get(f"/v1/jobs/{job['job_id']}/footprint").json()
    check('JobFootprint', fp)
    assert fp['proteins'] == ['first', 'P12345'] and fp['protein']['input_id'] == 'first' and len(fp['tiles']) == 4
    fp2 = c.get(f"/v1/jobs/{job['job_id']}/footprint?input_id=P12345").json()
    assert fp2['protein']['uniprot_id'] == 'P12345' and all(t['start_pos'] >= 1 for t in fp2['tiles'])
    assert c.get(f"/v1/jobs/{job['job_id']}/footprint?input_id=Q99999").status_code == 422


def test_batch10_limits_and_request_shape(wc):
    c, app, _ = wc
    pid = project(c)
    big = 'A' * 6000
    r = submit(c, pid, mode='protein', proteins=[{'input_id': 'a', 'sequence': big}, {'input_id': 'b', 'sequence': big}])
    assert r.status_code == 413 and 'in total' in r.json()['message']
    r = submit(c, pid, mode='protein', proteins=[{'input_id': 'a', 'sequence': SEQ}, {'input_id': 'a', 'sequence': SEQ2}])
    assert r.status_code == 422 and 'used twice' in r.json()['message']
    assert submit(c, pid, mode='protein', proteins=[]).status_code == 422
    assert submit(c, pid, mode='protein', proteins=[{'input_id': 'x', 'sequence': SEQ}] * 21).status_code == 422
    r = submit(c, pid, mode='protein', protein={'uniprot_id': 'P12345'}, proteins=[{'uniprot_id': 'P12345'}])
    assert r.status_code == 422
    r = submit(c, pid, mode='peptides', peptides=[{'input_id': 'a', 'sequence': SEQ}], proteins=[{'uniprot_id': 'P12345'}])
    assert r.status_code == 422
    assert submit(c, pid, mode='protein', proteins=[{'input_id': 'x'}]).status_code == 422


# --- BATCH-11 (plan-system 4.5): several workers, priority, running limit per job -------------------------------------

def _peptides(n, prefix='p'):
    seqs = [SEQ, SEQ2]
    return [{'input_id': f'{prefix}{i}', 'sequence': seqs[i % 2]} for i in range(n)]


def test_batch11_priority_and_running_limit(wc):
    c, app, url = wc
    pid = project(c)
    big = submit(c, pid, mode='peptides', peptides=_peptides(12, 'big')).json()
    small = submit(c, pid, mode='peptides', peptides=_peptides(2, 'small')).json()
    assert big['priority'] == 'normal' and small['priority'] == 'high'
    w1, w2, w3, w4 = (worker(app, owner=f'w{i}') for i in range(4))
    # the small job goes first although it was submitted later
    assert w1.claim()[0] == small['job_id'] and w2.claim()[0] == small['job_id']
    # then the big job, but never more than 2 of its items at once
    assert w3.claim()[0] == big['job_id'] and w4.claim()[0] == big['job_id']
    assert worker(app, owner='w5').claim() is None
    # a user may raise a big job
    hi = submit(c, pid, mode='peptides', peptides=_peptides(12, 'hi'), priority='high').json()
    assert hi['priority'] == 'high'
    assert submit(c, pid, mode='peptides', peptides=_peptides(1), priority='urgent').status_code == 422


def test_batch11_three_workers_never_process_an_item_twice(wc):
    import threading
    c, app, url = wc
    pid = project(c)
    jobs_ = [submit(c, pid, mode='peptides', peptides=_peptides(8, f'j{k}-')).json() for k in range(3)]
    workers = [worker(app, owner=f'thread-{i}') for i in range(3)]
    errors: list[BaseException] = []

    def run(w):
        try:
            w.drain()
        except BaseException as exc:                                      # noqa: BLE001
            errors.append(exc)
    threads = [threading.Thread(target=run, args=(w,)) for w in workers]
    for t in threads:
        t.start()
    for t in threads:
        t.join(120)
    assert not errors
    with make_engine(url).connect() as conn:
        rows = conn.execute(select(JobItem.item_id, JobItem.state, JobItem.attempts)
                            .where(JobItem.job_id.in_([j['job_id'] for j in jobs_]))).all()
        runs = conn.execute(select(func.count()).select_from(AnalysisRun)
                            .where(AnalysisRun.job_id.in_([j['job_id'] for j in jobs_]))).scalar()
    assert len(rows) == 24 and all(r.state == 'succeeded' for r in rows)
    assert runs == 24                                                     # one analysis per item, none twice
    assert all(r.attempts == 1 for r in rows)


def test_batch11_cancel_with_several_workers(wc):
    c, app, url = wc
    pid = project(c)
    job = submit(c, pid, mode='peptides', peptides=_peptides(12)).json()
    w1, w2 = worker(app, owner='a'), worker(app, owner='b')
    claimed = [w1.claim(), w2.claim()]
    assert all(x and x[0] == job['job_id'] for x in claimed)
    c.post(f"/v1/jobs/{job['job_id']}/cancel")
    for w, cl in zip((w1, w2), claimed, strict=True):
        assert w.process(*cl).state == 'cancelled'
    assert worker(app, owner='c').claim() is None
    done = c.get(f"/v1/jobs/{job['job_id']}").json()
    assert done['state'] == 'cancelled' and done['counts']['succeeded'] == 0
