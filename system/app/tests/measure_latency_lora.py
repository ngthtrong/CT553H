"""WP10.5 / NFR-01: latency of the optional LoRA-D model against the npz model, over real HTTP, on a running stack.

    python tests/measure_latency_lora.py --base http://127.0.0.1:8080 --container degron-footprint-api-1

Scores N stored tiles of one protein with each model (sequential, override_domain so that every tile is scored), after
one warm-up request per model (the LoRA network is built on first use). With --container it also reads the API
container's memory (docker stats) and the image size. Writes tests/results/latency-lora.json; the numbers hold for this
host and configuration only, and are recorded whether or not they meet the proposed 300 ms p95 (they do not).
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

APP = Path(__file__).resolve().parents[1]
LORA = 'esm2-35m-lora-d-aa4fc2b7'


def host() -> dict:
    cpu = next((line.split(':', 1)[1].strip() for line in open('/proc/cpuinfo') if line.startswith('model name')), '?')
    mem_kb = int(next(line.split()[1] for line in open('/proc/meminfo') if line.startswith('MemTotal')))
    return {'platform': platform.platform(), 'cpu_model': cpu, 'logical_cpus': os.cpu_count(),
            'mem_total_mb': round(mem_kb / 1024), 'load_average_1_5_15': os.getloadavg(),
            'note': 'WSL2 on the author laptop; Docker Engine in the same VM; other processes may share the CPU'}


def stats(xs: list[float]) -> dict:
    s = sorted(xs)
    q = lambda p: s[min(len(s) - 1, int(p * len(s)))]       # noqa: E731
    return {'n': len(s), 'p50_ms': round(q(.5), 1), 'p95_ms': round(q(.95), 1), 'mean_ms': round(statistics.mean(s), 1),
            'min_ms': round(s[0], 1), 'max_ms': round(s[-1], 1)}


def docker(*args: str) -> str:
    return subprocess.run(['docker', *args], capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8080')
    ap.add_argument('--protein', default='A6NMZ7')
    ap.add_argument('--n', type=int, default=10)
    ap.add_argument('--container', default=None)
    ap.add_argument('--image', default=None)
    ap.add_argument('--out', type=Path, default=APP / 'tests/results/latency-lora.json')
    a = ap.parse_args()
    out: dict = {'date': datetime.now(UTC).isoformat(timespec='seconds'), 'host': host(), 'base': a.base,
                 'protein': a.protein, 'tiles': list(range(1, a.n + 1))}
    with httpx.Client(base_url=a.base, timeout=600) as c:
        health = c.get('/healthz').json()
        out['health'] = health
        models = {m['model_id']: m for m in c.get('/v1/models').json()['items']}
        assert LORA in models, 'LoRA-D is not registered (run the ETL with the bundle present)'
        # each model once (the default may be LoRA-D), and the warm-up on a tile outside the measured ones: since the
        # prediction cache (plan-system 1.2) a repeated tile would be a cache hit, not a model computation
        for model in dict.fromkeys((health['default_model_id'], LORA)):
            body = lambda i, model=model: {'uniprot_id': a.protein, 'tile_index': i, 'model_id': model,  # noqa: E731
                                           'override_domain': True}
            t = time.perf_counter()
            r = c.post('/v1/predict', json=body(len(out['tiles']) + 1))
            warm = (time.perf_counter() - t) * 1000
            assert r.status_code == 200, (model, r.status_code, r.text[:300])
            times = []
            for i in out['tiles']:
                t = time.perf_counter()
                r = c.post('/v1/predict', json=body(i))
                times.append((time.perf_counter() - t) * 1000)
                assert r.status_code == 200 and len(r.json()['cells']) == 532, (model, i, r.status_code)
                assert r.json()['provenance']['model_id'] == model
            out[model] = {'kind': models[model]['kind'], 'first_request_ms': round(warm, 1), **stats(times)}
    if a.container:
        raw = docker('stats', '--no-stream', '--format', '{{json .}}', a.container)
        out['api_container_stats_after'] = json.loads(raw)
        env = docker('inspect', '--format', '{{json .Config.Env}}', a.container)
        out['api_container_lora_threads'] = next((e.split('=', 1)[1] for e in json.loads(env)
                                                  if e.startswith('DF_LORA_THREADS=')), None)
    if a.image:
        out['image'] = {'name': a.image, 'size_bytes': int(docker('image', 'inspect', '--format', '{{.Size}}', a.image))}
    out['threshold_proposed'] = {'NFR-01_predict_p95_le_300ms': {m: out[m]['p95_ms'] <= 300 for m in
                                                                 dict.fromkeys((health['default_model_id'], LORA))}}
    out['caveats'] = ['one protein, sequential requests, warm network; through nginx (web container) and the API',
                      'each measured tile is requested once per model in a freshly started API process, so none is a '
                      'prediction-cache hit (warm-up on another tile)',
                      'LoRA-D runs 3 seeds x (1 + 532) ESM-2 35M forward passes per tile on the CPU',
                      'not a benchmark of the model quality; development_not_gate_closure']
    a.out.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
