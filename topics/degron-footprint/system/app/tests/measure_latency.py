"""NF-01..NF-03: latency and memory of the API over real HTTP on loopback, against the real database.

    make -C topics/degron-footprint/system/app latency        (needs .data/dev.db built by `make etl`)

Starts uvicorn as a subprocess, warms it up, then measures: sequential predictions (typed sequence and UniProt
tile), 10-way concurrent predictions, the tile list of a 1,000-residue protein, and the resident memory of the server
process. Writes tests/results/latency.json including the host configuration; the numbers hold for that host only.
"""
from __future__ import annotations

import json
import os
import platform
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

import httpx

APP = Path(__file__).resolve().parents[1]
PORT = 8765
BASE = f'http://127.0.0.1:{PORT}'
SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
N_SEQ, N_CONC, N_LIST = 300, 600, 300


def host() -> dict:
    cpu = next((line.split(':', 1)[1].strip() for line in open('/proc/cpuinfo') if line.startswith('model name')), '?')
    mem_kb = int(next(line.split()[1] for line in open('/proc/meminfo') if line.startswith('MemTotal')))
    return {'platform': platform.platform(), 'cpu_model': cpu, 'logical_cpus': os.cpu_count(),
            'mem_total_mb': round(mem_kb / 1024), 'python': platform.python_version(),
            'load_average_1_5_15': os.getloadavg(), 'note': 'WSL2 on the author laptop; other processes may share the CPU'}


def pct(xs: list[float]) -> dict:
    xs = sorted(xs)
    q = lambda p: xs[min(len(xs) - 1, int(p * len(xs)))]       # noqa: E731
    return {'n': len(xs), 'p50_ms': round(q(.50), 2), 'p95_ms': round(q(.95), 2), 'p99_ms': round(q(.99), 2),
            'mean_ms': round(statistics.mean(xs), 2), 'max_ms': round(xs[-1], 2)}


def timed(client: httpx.Client, method: str, url: str, **kw) -> tuple[float, int]:
    t = time.perf_counter()
    r = client.request(method, url, **kw)
    return (time.perf_counter() - t) * 1000, r.status_code


def rss_mb(pid: int) -> float:
    for line in open(f'/proc/{pid}/status'):
        if line.startswith('VmRSS'):
            return round(int(line.split()[1]) / 1024, 1)
    return -1.0


def main() -> int:
    db = APP / '.data/dev.db'
    if not db.exists():
        print('build the database first: make -C topics/degron-footprint/system/app etl', file=sys.stderr)
        return 2
    env = {**os.environ, 'DF_DATABASE_URL': f'sqlite:///{db}', 'DF_RATE_LIMIT_PREDICT': '1000000',
           'DF_RATE_LIMIT_REFERENCE': '1000000', 'DF_ALLOWED_ORIGINS': '["http://localhost:5173"]',
           'OPENBLAS_NUM_THREADS': '1'}
    proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'api.main:create_app', '--factory', '--port', str(PORT),
                             '--no-access-log', '--log-level', 'warning'], cwd=APP / 'backend', env=env)
    try:
        client = httpx.Client(base_url=BASE, timeout=30)
        for _ in range(100):
            try:
                if client.get('/healthz').status_code == 200:
                    break
            except httpx.HTTPError:
                time.sleep(0.2)
        else:
            raise RuntimeError('server did not start')
        for _ in range(30):                                                    # warm-up
            client.post('/v1/predict', json={'sequence': SEQ})
            client.post('/v1/predict', json={'uniprot_id': 'A6NMZ7', 'tile_index': 28})
            client.get('/v1/proteins/P12109/tiles')
        rss_idle = rss_mb(proc.pid)
        out: dict = {'date': datetime.now(UTC).isoformat(timespec='seconds'), 'host': host(), 'server_rss_after_warmup_mb': rss_idle}

        lat, bad = [], 0
        for _ in range(N_SEQ):
            ms, st = timed(client, 'POST', '/v1/predict', json={'sequence': SEQ})
            lat.append(ms)
            bad += st != 200
        out['predict_typed_sequence_sequential'] = {**pct(lat), 'non_200': bad}

        lat, bad = [], 0
        for _ in range(N_SEQ):
            ms, st = timed(client, 'POST', '/v1/predict', json={'uniprot_id': 'A6NMZ7', 'tile_index': 28})
            lat.append(ms)
            bad += st != 200
        out['predict_uniprot_tile_sequential'] = {**pct(lat), 'non_200': bad}

        def one(_):
            with httpx.Client(base_url=BASE, timeout=30) as c:
                return timed(c, 'POST', '/v1/predict', json={'sequence': SEQ})
        # a pool of 10 persistent clients, each issuing its share of requests
        def worker(n: int) -> list[tuple[float, int]]:
            with httpx.Client(base_url=BASE, timeout=60) as c:
                return [timed(c, 'POST', '/v1/predict', json={'uniprot_id': 'A6NMZ7', 'tile_index': 28}) for _ in range(n)]
        t0 = time.perf_counter()
        with ThreadPoolExecutor(10) as ex:
            res = [r for part in ex.map(worker, [N_CONC // 10] * 10) for r in part]
        wall = time.perf_counter() - t0
        out['predict_10_way_concurrent'] = {**pct([r[0] for r in res]), 'non_200': sum(r[1] != 200 for r in res),
                                            'throughput_req_per_s': round(len(res) / wall, 1)}
        out['server_rss_after_load_mb'] = rss_mb(proc.pid)

        lat, bad = [], 0
        for _ in range(N_LIST):
            ms, st = timed(client, 'GET', '/v1/proteins/P12109/tiles')
            lat.append(ms)
            bad += st != 200
        n_tiles = len(client.get('/v1/proteins/P12109/tiles').json()['tiles'])
        out['tiles_list_1028_aa_protein'] = {**pct(lat), 'non_200': bad, 'tiles': n_tiles}

        lat = [timed(client, 'GET', '/v1/proteins?query=COL6')[0] for _ in range(N_LIST)]
        out['protein_search'] = pct(lat)

        # thresholds proposed in srs.md; each is "met" only on this host and with this many requests
        out['thresholds_proposed'] = {
            'NFR-01_predict_p95_le_300ms': out['predict_typed_sequence_sequential']['p95_ms'] <= 300
            and out['predict_uniprot_tile_sequential']['p95_ms'] <= 300,
            'NFR-02_tiles_list_p95_le_200ms': out['tiles_list_1028_aa_protein']['p95_ms'] <= 200,
            'NFR-18_server_rss_le_512mb': out['server_rss_after_load_mb'] <= 512,
        }
        out['caveats'] = ['loopback HTTP, no TLS, no reverse proxy; SQLite database on local disk',
                          'server time plus loopback; the browser time of NFR-03 is not measured here',
                          'host shared with other processes; rerun on the reference host (2 vCPU / 2 GB) for NF-01..03']
        (APP / 'tests/results').mkdir(exist_ok=True)
        (APP / 'tests/results/latency.json').write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
