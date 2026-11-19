"""plan-system 1.2 acceptance: reopening or exporting the same LoRA-D tile a second time takes < 1 s (prediction cache).

    .venv/bin/python tests/measure_cache.py --base http://127.0.0.1:8080

On a running stack: for each of a few stored tiles not scored before in this API process, time (1) the first
prediction (model computation), (2) the same prediction again, (3) the CSV export of the same tile, (4) the JSON export.
Requests (2)–(4) must be answered from the cache. The answers of (1) and (2) are compared cell by cell (bit identity,
NFR-05). Writes tests/results/cache-lora.json; numbers hold for this host only and are recorded whether or not they
meet the target.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx
from measure_latency_lora import LORA, host  # same directory (run as a script)

APP = Path(__file__).resolve().parents[1]


def timed(fn, *args, **kw):
    t0 = time.perf_counter()
    r = fn(*args, **kw)
    return r, round((time.perf_counter() - t0) * 1000, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8080')
    ap.add_argument('--protein', default='A6NMZ7')
    ap.add_argument('--tiles', default='41,42,43')
    ap.add_argument('--out', type=Path, default=APP / 'tests/results/cache-lora.json')
    a = ap.parse_args()
    out: dict = {'date': datetime.now(UTC).isoformat(timespec='seconds'), 'host': host(), 'base': a.base,
                 'model_id': LORA, 'protein': a.protein, 'target': 'second open/export of the same tile < 1000 ms',
                 'tiles': []}
    with httpx.Client(base_url=a.base, timeout=600) as c:
        out['health'] = c.get('/healthz').json()
        for n in (int(x) for x in a.tiles.split(',')):
            body = {'uniprot_id': a.protein, 'tile_index': n, 'model_id': LORA, 'override_domain': True}
            r1, first = timed(c.post, '/v1/predict', json=body)
            r2, again = timed(c.post, '/v1/predict', json=body)
            r3, csv_ms = timed(c.post, '/v1/export', json={**body, 'format': 'csv'})
            r4, json_ms = timed(c.post, '/v1/export', json={**body, 'format': 'json'})
            for r in (r1, r2, r3, r4):
                r.raise_for_status()
            same = r1.json()['cells'] == r2.json()['cells'] == r4.json()['cells']
            out['tiles'].append({'tile_index': n, 'first_ms': first, 'second_predict_ms': again,
                                 'export_csv_ms': csv_ms, 'export_json_ms': json_ms, 'cells_identical': same,
                                 'seed_spread_present': r1.json()['cells'][0].get('score_seed_sd') is not None})
    rows = out['tiles']
    out['summary'] = {'max_cached_ms': max(max(t['second_predict_ms'], t['export_csv_ms'], t['export_json_ms']) for t in rows),
                      'min_first_ms': min(t['first_ms'] for t in rows),
                      'all_identical': all(t['cells_identical'] for t in rows)}
    out['summary']['target_met'] = out['summary']['max_cached_ms'] < 1000 and out['summary']['all_identical']
    out['caveats'] = ['one protein, sequential requests, same API process; the cache is per process (memory mode)',
                      'tiles chosen so that they were not scored before in this process; first_ms includes the model']
    a.out.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out['summary']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
