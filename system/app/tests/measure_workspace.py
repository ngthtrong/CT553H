"""NF-07 (and NF-04/05 bounds): representative workspace jobs on a copy of the real database.

    .venv/bin/python tests/measure_workspace.py          (needs .data/dev.db at revision 0003)

Measures, on a private copy of .data/dev.db (the original is never written):
  * a 100-peptide job: submit time, time to the first claimed item, total duration, per-item time;
  * the largest loaded protein of at most 10,000 residues as a whole-protein job: same, plus manifest export time/size;
  * a 100,000-row CSV import preview and commit;
  * cancellation latency of a running job; database and workspace growth; peak resident memory of this process.
The API runs in process (FastAPI TestClient) and the worker is the real api.worker loop in a thread, polling every
50 ms. Results: tests/results/workspace-performance.json with the host configuration; the numbers hold for that host.
"""
from __future__ import annotations

import json
import resource
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(APP / 'backend'), str(APP)]

from fastapi.testclient import TestClient  # noqa: E402

from api.config import Settings  # noqa: E402
from api.main import create_app  # noqa: E402
from api.worker import from_core  # noqa: E402
from tests.measure_latency import host  # noqa: E402

SRC = APP / '.data/dev.db'
OUT = APP / 'tests/results/workspace-performance.json'


def rss_mb() -> float:
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)


def wait(c: TestClient, job_id: str, timeout: float = 900) -> tuple[dict, float | None]:
    started = time.perf_counter()
    first_claim = None
    while time.perf_counter() - started < timeout:
        j = c.get(f'/v1/jobs/{job_id}').json()
        if first_claim is None and (j['counts']['running'] or j['counts']['succeeded'] or j['counts']['failed']):
            first_claim = time.perf_counter() - started
        if j['state'] in ('completed', 'partial', 'failed', 'cancelled'):
            return j, first_claim
        time.sleep(0.05)
    raise TimeoutError(job_id)


def main() -> None:
    if not SRC.exists():
        raise SystemExit('.data/dev.db is missing; run make etl first')
    tmp = Path(tempfile.mkdtemp(prefix='df-perf-'))
    db = tmp / 'dev.db'
    shutil.copy(SRC, db)
    ws = tmp / 'workspace'
    settings = Settings(database_url=f'sqlite:///{db}', workspace_dir=ws, background_jobs=False, openapi_contract=None,
                        rate_limit_predict=10**6, rate_limit_reference=10**6, worker_poll_seconds=0.05)
    app = create_app(settings)
    out: dict = {'generated_at': datetime.now(UTC).isoformat(timespec='seconds'), 'host': host(),
                 'database': {'source': '.data/dev.db (copy)', 'bytes_before': db.stat().st_size}, 'results': {}}
    with TestClient(app) as c:
        stop = threading.Event()
        worker = threading.Thread(target=from_core(app.state.core, 'perf-worker').run, args=(stop,), daemon=True)
        worker.start()
        pid = c.post('/v1/projects', json={'name': 'performance'}).json()['project_id']
        con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        tiles = [r[0] for r in con.execute(
            "SELECT sequence FROM tile WHERE scorable = 1 AND domain_status IN ('measured_in_domain', 'predicted_in_domain') "
            'ORDER BY tile_id LIMIT 100')]
        acc, length = con.execute('SELECT uniprot_acc, length FROM protein WHERE length <= 10000 '
                                  'ORDER BY length DESC LIMIT 1').fetchone()
        con.close()

        # --- 100 peptides
        t = time.perf_counter()
        r = c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'peptides',
                                                    'peptides': [{'input_id': f'p{i}', 'sequence': s} for i, s in enumerate(tiles)]})
        submit_s = time.perf_counter() - t
        job, first = wait(c, r.json()['job_id'])
        dur = time.perf_counter() - t
        out['results']['peptides_100'] = {'submit_seconds': round(submit_s, 3), 'first_claim_seconds': round(first or 0, 3),
                                          'total_seconds': round(dur, 2), 'per_item_ms': round(dur / 100 * 1000, 1),
                                          'state': job['state'], 'counts': job['counts']}

        # --- largest protein ≤ 10,000 residues
        t = time.perf_counter()
        r = c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'protein', 'protein': {'uniprot_id': acc}, 'override_domain': True})
        submit_s = time.perf_counter() - t
        job, first = wait(c, r.json()['job_id'])
        dur = time.perf_counter() - t
        t = time.perf_counter()
        csv_bytes = len(c.get(f"/v1/jobs/{job['job_id']}/export?format=csv").content)
        export_s = time.perf_counter() - t
        t = time.perf_counter()
        page = c.get(f"/v1/jobs/{job['job_id']}/items?offset=200&limit=200")
        page_ms = (time.perf_counter() - t) * 1000
        out['results']['protein'] = {'uniprot_id': acc, 'length': length, 'tiles': job['total'], 'submit_seconds': round(submit_s, 3),
                                     'first_claim_seconds': round(first or 0, 3), 'total_seconds': round(dur, 2),
                                     'per_tile_ms': round(dur / job['total'] * 1000, 1), 'state': job['state'],
                                     'counts': job['counts'], 'export_csv_seconds': round(export_s, 2),
                                     'export_csv_mb': round(csv_bytes / 1e6, 1), 'item_page_200_ms': round(page_ms, 1),
                                     'item_page_status': page.status_code}

        # --- cancellation of a running job
        r = c.post(f'/v1/projects/{pid}/jobs', json={'mode': 'protein', 'protein': {'uniprot_id': acc}, 'override_domain': True})
        jid = r.json()['job_id']
        while c.get(f'/v1/jobs/{jid}').json()['counts']['succeeded'] < 5:
            time.sleep(0.02)
        t = time.perf_counter()
        c.post(f'/v1/jobs/{jid}/cancel')
        final, _ = wait(c, jid)
        out['results']['cancel'] = {'seconds_to_cancelled': round(time.perf_counter() - t, 3), 'state': final['state'],
                                    'kept_succeeded': final['counts']['succeeded'], 'cancelled': final['counts']['cancelled']}

        # --- 100,000-row import
        seq = tiles[0]
        aas = 'ACDEFGHIKLMNPQRSTVWY'
        rows = ['peptide_id,wt_sequence,position,wt_aa,mut_aa,observed_value,replicate_id']
        n = 0
        rep = 0
        while n < 100_000:
            for pos in range(1, 29):
                for aa in aas:
                    if aa == seq[pos - 1] or n >= 100_000:
                        continue
                    rows.append(f'p,{seq},{pos},{seq[pos - 1]},{aa},{(n % 97) / 10},r{rep}')
                    n += 1
            rep += 1
        body = '\n'.join(rows).encode()
        meta = {'name': 'perf', 'assay': 'GPS', 'endpoint': 'delta_psi', 'units': 'PSI', 'source': 'synthetic',
                'reference_description': 'performance test', 'compatibility': 'zhang_gps_dpsi'}
        t = time.perf_counter()
        r = c.post(f'/v1/projects/{pid}/datasets', files={'file': ('perf.csv', body, 'text/csv')}, data={'metadata': json.dumps(meta)})
        preview_s = time.perf_counter() - t
        d = r.json()
        t = time.perf_counter()
        cm = c.post(f"/v1/datasets/{d['dataset_id']}", json={'action': 'commit', 'acknowledge_warnings': True})
        out['results']['import_100k'] = {'file_mb': round(len(body) / 1e6, 2), 'rows': d['counts']['rows'],
                                         'valid': d['counts']['valid'],
                                         'preview_seconds': round(preview_s, 2), 'commit_seconds': round(time.perf_counter() - t, 3),
                                         'committed': cm.json().get('state')}
        stop.set()
        worker.join(timeout=10)
    out['database']['bytes_after'] = db.stat().st_size
    out['database']['growth_mb'] = round((db.stat().st_size - out['database']['bytes_before']) / 1e6, 1)
    out['workspace_files_mb'] = round(sum(f.stat().st_size for f in ws.rglob('*') if f.is_file()) / 1e6, 2)
    out['peak_rss_mb_api_worker_one_process'] = rss_mb()
    OUT.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    shutil.rmtree(tmp)
    print(json.dumps(out['results'], indent=2))
    print('peak RSS MB', out['peak_rss_mb_api_worker_one_process'], 'db growth MB', out['database']['growth_mb'])


if __name__ == '__main__':
    main()
