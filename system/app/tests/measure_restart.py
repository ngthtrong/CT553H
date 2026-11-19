"""DEP-02 / BATCH-05 / HIST-02 with real processes: stop the running instance hard, start it again, check recovery.

    .venv/bin/python tests/measure_restart.py

On a private copy of .data/dev.db: start uvicorn with the embedded worker, create a project, save an analysis, submit a
whole-protein job, SIGKILL the server (API and worker die together) while the job runs, wait for the lease to expire,
start the same instance again and check that the job finishes with every tile counted once, one saved analysis per
succeeded tile, and the saved analysis reopens byte-identical. Writes tests/results/dep02-restart.json.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

APP = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(APP)]
from tests.measure_latency import host  # noqa: E402

PORT = 8766
BASE = f'http://127.0.0.1:{PORT}'
LEASE = 8


def start(db: Path, ws: Path) -> subprocess.Popen:
    env = {**os.environ, 'DF_DATABASE_URL': f'sqlite:///{db}', 'DF_WORKSPACE_DIR': str(ws), 'DF_EMBEDDED_WORKER': '1',
           'DF_WORKER_POLL_SECONDS': '0.1', 'DF_JOB_LEASE_SECONDS': str(LEASE), 'DF_RATE_LIMIT_PREDICT': '100000',
           'DF_RATE_LIMIT_REFERENCE': '100000', 'PYTHONPATH': str(APP / 'backend')}
    p = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'api.main:create_app', '--factory', '--host', '127.0.0.1',
                          '--port', str(PORT), '--no-access-log'], cwd=APP / 'backend', env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(100):
        try:
            if httpx.get(f'{BASE}/healthz', timeout=1).status_code == 200:
                return p
        except httpx.HTTPError:
            pass
        time.sleep(0.2)
    raise RuntimeError('server did not start')


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix='df-dep02-'))
    db, ws = tmp / 'dev.db', tmp / 'workspace'
    shutil.copy(APP / '.data/dev.db', db)
    c = httpx.Client(base_url=BASE, timeout=30)
    out: dict = {'generated_at': datetime.now(UTC).isoformat(timespec='seconds'), 'host': host(), 'lease_seconds': LEASE}
    server = start(db, ws)
    pid = c.post('/v1/projects', json={'name': 'restart check'}).json()['project_id']
    saved = c.post(f'/v1/projects/{pid}/analyses', json={'request': {'uniprot_id': 'A6NMZ7', 'tile_index': 28}}).json()
    acc = 'Q8NF91'
    job = c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'protein', 'protein': {'uniprot_id': acc}, 'override_domain': True}).json()
    while (j := c.get(f"/v1/jobs/{job['job_id']}").json())['counts']['succeeded'] < 60:
        time.sleep(0.05)
    os.killpg(server.pid, signal.SIGKILL)                       # API and the embedded worker die together
    server.wait()
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    at_kill = dict(con.execute('SELECT state, count(*) FROM job_item WHERE job_id = ? GROUP BY state', (job['job_id'],)).fetchall())
    runs_at_kill = con.execute('SELECT count(*) FROM analysis_run WHERE job_id = ?', (job['job_id'],)).fetchone()[0]
    con.close()
    out['at_kill'] = {'item_states': at_kill, 'analyses_from_job': runs_at_kill}
    time.sleep(LEASE + 1)                                       # an item held by the dead worker becomes reclaimable
    t = time.perf_counter()
    server = start(db, ws)
    restart_s = time.perf_counter() - t
    deadline = time.monotonic() + 600
    while (j := c.get(f"/v1/jobs/{job['job_id']}").json())['state'] not in ('completed', 'partial', 'failed', 'cancelled'):
        assert time.monotonic() < deadline
        time.sleep(0.2)
    again = c.get(f"/v1/analyses/{saved['analysis_id']}").json()
    history = c.get(f'/v1/projects/{pid}/analyses?limit=1').json()['total']
    os.killpg(server.pid, signal.SIGTERM)
    server.wait(timeout=20)
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    runs = con.execute('SELECT count(*), count(DISTINCT item_id) FROM analysis_run WHERE job_id = ?', (job['job_id'],)).fetchone()
    con.close()
    out['after_restart'] = {'restart_seconds': round(restart_s, 2), 'job_state': j['state'], 'counts': j['counts'],
                            'total': j['total'],
                            'analyses_from_job': runs[0], 'distinct_items_with_analysis': runs[1],
                            'saved_analysis_identical': again == saved, 'history_total': history}
    ok = (j['state'] == 'completed' and j['counts']['succeeded'] == j['total'] == runs[0] == runs[1] and again == saved
          and history == j['total'] + 1)
    out['passed'] = ok
    (APP / 'tests/results/dep02-restart.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    shutil.rmtree(tmp)
    print(json.dumps(out, indent=2))
    if not ok:
        raise SystemExit('DEP-02 check failed')


if __name__ == '__main__':
    main()
