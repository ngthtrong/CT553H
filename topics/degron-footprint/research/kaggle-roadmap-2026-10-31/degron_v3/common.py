from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import time

import numpy as np

AAS = 'ACDEFGHIKLMNPQRSTVWY'
AA_INDEX = {a: i for i, a in enumerate(AAS)}
SEEDS = (17, 29, 43)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(4 << 20), b''):
            h.update(b)
    return h.hexdigest()


def atomic_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    def convert(x):
        if isinstance(x, (np.integer, np.floating)):
            return x.item()
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, Path):
            return str(x)
        raise TypeError(type(x).__name__)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=convert,
                               allow_nan=False) + '\n')
    os.replace(temp, path)


def seeds(seed):
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
    except ImportError:
        pass


def environment():
    import importlib.metadata
    names = ['numpy', 'pandas', 'pyarrow', 'scipy', 'scikit-learn', 'torch',
             'transformers', 'peft', 'accelerate', 'sentencepiece', 'safetensors']
    versions = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    result = dict(python=platform.python_version(), platform=platform.platform(), versions=versions)
    try:
        import torch
        result['cuda'] = torch.cuda.is_available()
        result['devices'] = [dict(name=torch.cuda.get_device_name(i),
                                  bytes=torch.cuda.get_device_properties(i).total_memory)
                             for i in range(torch.cuda.device_count())]
    except ImportError:
        pass
    return result


@contextmanager
def execution(out, stage, config):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    config_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    previous = out / 'run-manifest.json'
    if previous.exists():
        assert json.loads(previous.read_text())['config_sha256'] == config_hash, 'Use a new output directory for changed config'
    atomic_json(previous, dict(stage=stage, mode='smoke' if config['smoke'] else 'official',
                              config_sha256=config_hash, config=config,
                              started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
    atomic_json(out / 'env.json', environment())
    start = time.monotonic()
    try:
        yield out
    except Exception as e:
        atomic_json(out / 'status.json', dict(status='failed', error=f'{type(e).__name__}: {e}',
                                             seconds=time.monotonic() - start))
        raise
    else:
        atomic_json(out / 'status.json', dict(status='complete', mode='smoke' if config['smoke'] else 'official',
                                             seconds=time.monotonic() - start))


class UnionFind:
    def __init__(self, names):
        self.parent = {n: n for n in names}

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def stratum(psi):
    return 'le3' if psi <= 3 else 'gt3_le4' if psi <= 4 else 'gt4_le5' if psi <= 5 else 'gt5'
