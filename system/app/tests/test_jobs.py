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
    assert header[9:] == ['project_id', 'job_id', 'item_id', 'input_id', 'uniprot_id', 'reference_release',
                          'start_pos', 'end_pos', 'protein_position', 'status', 'error_code', 'domain_status']
    assert len(body) == 532 + 1
    assert body[0][12] == "'=cmd|calc"                                 # formula neutralised (SEC-02)
    assert body[-1][11] == 'p0002'
    assert body[-1][:9] == [''] * 9 and body[-1][-3:-1] == ['refused', 'INVALID_LENGTH']
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
