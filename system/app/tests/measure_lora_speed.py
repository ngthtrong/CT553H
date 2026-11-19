"""plan-system 1.4 (PERF-01/02): where the time of one LoRA-D tile goes, and what batch size, threads and merging the
LoRA update change — on this host, against the parity fixture (two W tiles).

    .venv-lora/bin/python tests/measure_lora_speed.py            # writes tests/results/lora-speed.json

Every configuration is checked against the fixture's per-seed raw scores: max |difference| is recorded, and a
configuration whose difference exceeds 1e-5 would need a new model id (plan-system 1.4 b). Numbers hold for this host.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP / 'backend'))
MANIFEST = APP.parents[1] / 'data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1.json'


def load(batch: int, threads: int, merge: bool):
    os.environ['DF_LORA_BATCH'] = str(batch)
    os.environ['DF_LORA_THREADS'] = str(threads)
    os.environ['DF_LORA_MERGE'] = '1' if merge else '0'
    from degron_footprint.lora import LoraEnsembleModel
    sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    return LoraEnsembleModel.from_file('esm2-35m-lora-d-aa4fc2b7', MANIFEST, sha)


def breakdown(model, seq: str) -> dict:
    """Seconds spent in tokenisation, backbone forward and head for one tile (first seed network, all 532 mutants)."""
    import torch

    from degron_footprint.features import substitutions
    from degron_footprint.lora import composition_features
    tok, nets = model._ensure()
    net = nets[0]
    cells = substitutions(seq)
    mutants = [seq[:p - 1] + a + seq[p:] for p, a in cells]
    t = {'tokenize': 0.0, 'forward': 0.0, 'head': 0.0}
    aux = torch.from_numpy(composition_features(seq, cells))
    with torch.inference_mode():
        t0 = time.perf_counter()
        enc = tok(mutants, return_tensors='pt', padding=True)
        t['tokenize'] = time.perf_counter() - t0
        t0 = time.perf_counter()
        for lo in range(0, len(mutants), model.batch):
            _ = net.backbone(**{k: v[lo:lo + model.batch] for k, v in enc.items()}).last_hidden_state
        t['forward'] = time.perf_counter() - t0
        t0 = time.perf_counter()
        x = torch.zeros(len(cells), 2 * net.backbone.config.hidden_size)
        net.head(torch.cat([x, aux], 1))
        t['head'] = time.perf_counter() - t0
    return {k: round(v, 3) for k, v in t.items()}


def main() -> int:
    import torch
    fx = np.load(MANIFEST.parent / 'esm2-35m-lora-d-v1/parity-fixture.npz', allow_pickle=False)
    tiles = [(str(fx['tile_w_sequence']), fx['tile_w_per_seed']),
             (str(fx['tile_typed_sequence']), fx['tile_typed_per_seed'])]
    configs = [(64, 4, False), (128, 4, False), (256, 4, False), (532, 4, False), (128, 6, False), (128, 4, True),
               (256, 6, True)]
    out: dict = {'date': datetime.now(UTC).isoformat(timespec='seconds'), 'host': platform.platform(),
                 'cpu_count': os.cpu_count(), 'torch': torch.__version__, 'configs': []}
    for batch, threads, merge in configs:
        model = load(batch, threads, merge)
        t0 = time.perf_counter()
        model._ensure()
        build = time.perf_counter() - t0
        times, diff = [], 0.0
        for seq, ref in tiles:
            t0 = time.perf_counter()
            per_seed, _ = model.raw_scores(seq)
            times.append(time.perf_counter() - t0)
            diff = max(diff, float(np.max(np.abs(per_seed - ref.astype(np.float64)))))
        row = {'batch': batch, 'threads': threads, 'merge': merge, 'build_s': round(build, 2),
               'tile_s': [round(x, 2) for x in times], 'mean_tile_s': round(sum(times) / len(times), 2),
               'max_abs_diff_vs_fixture': diff, 'parity_le_1e-5': diff <= 1e-5}
        if (batch, threads, merge) == (64, 4, False):
            row['breakdown_first_seed'] = breakdown(model, tiles[0][0])
        print(json.dumps(row), flush=True)
        out['configs'].append(row)
    base = out['configs'][0]['mean_tile_s']
    best = min((c for c in out['configs'] if c['parity_le_1e-5']), key=lambda c: c['mean_tile_s'])
    out['summary'] = {'baseline_mean_tile_s': base, 'best': best, 'speedup': round(base / best['mean_tile_s'], 2),
                      'target_proposed_p95_le_15s_4threads': None,
                      'note': ('mean of two tiles in this process (warm after the first); p95 over more tiles is '
                               'measured in Docker by measure_latency_lora.py')}
    (APP / 'tests/results/lora-speed.json').write_text(json.dumps(out, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
