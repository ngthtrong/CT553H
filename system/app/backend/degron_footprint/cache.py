"""Prediction cache (plan-system 1.2): the model's scores for one tile, keyed by everything that determines them.

Key = sha256(sequence · model_id · weights_sha256 · calibrator · CODE_VERSION). Only the model output is cached
(positions, letters, raw score, probability, rank, top-10 flag); the domain status, warnings and annotations depend on
the reference database and are always recomputed by the caller.

Modes (DF_PREDICTION_CACHE):
* ``memory`` (default): a bounded LRU per process; nothing reaches the disk.
* ``disk``: also writes one ``<key>.npz`` per tile under DF_PREDICTION_CACHE_DIR. The file names are hashes, but the
  stored wild-type letters spell the sequence: the disk mode keeps user sequences on the disk without an explicit save
  (NFR-09/10), so it is opt-in and documented in INSTALL.md and DEVIATIONS.md.
* ``off``: no cache.

The cache never logs or exposes a sequence; statistics are counts only.
"""
from __future__ import annotations

import hashlib
import logging
import os
import tempfile
import threading
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .constants import CODE_VERSION
from .model import TilePrediction

log = logging.getLogger('degron_footprint.cache')
MODES = ('off', 'memory', 'disk')
_FIELDS = ('positions', 'score', 'prob', 'rank', 'top10')
_OPTIONAL = ('seed_sd', 'seed_min', 'seed_max')               # ensembles only (plan-system 1.3)


def cache_key(seq: str, model_id: str, weights_sha256: str, calibrator: str, code_version: str = CODE_VERSION) -> str:
    h = hashlib.sha256()
    for part in (seq, model_id, weights_sha256, calibrator, code_version):
        h.update(part.encode('utf-8'))
        h.update(b'\x1f')                                    # unit separator: no ambiguity between fields
    return h.hexdigest()


def _frozen(pred: TilePrediction) -> TilePrediction:
    """A copy whose arrays cannot be modified by a caller (the cached object is shared)."""
    arrays = {}
    for name in _FIELDS + _OPTIONAL:
        value = getattr(pred, name)
        if value is None:
            continue
        a = np.array(value, copy=True)
        a.flags.writeable = False
        arrays[name] = a
    return TilePrediction(wt=list(pred.wt), mut=list(pred.mut), **arrays)


@dataclass
class CacheStats:
    mode: str
    entries: int
    max_entries: int
    hits: int
    misses: int
    disk_hits: int
    disk_writes: int
    errors: int

    def as_dict(self) -> dict:
        return dict(self.__dict__)


class PredictionCache:
    def __init__(self, mode: str = 'memory', max_entries: int = 512, directory: Path | None = None):
        if mode not in MODES:
            raise ValueError(f'prediction cache mode must be one of {MODES}')
        if mode == 'disk' and directory is None:
            raise ValueError('the disk prediction cache needs a directory')
        self.mode = mode
        self.max_entries = max(0, int(max_entries))
        self.directory = directory
        self._lru: OrderedDict[str, TilePrediction] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = self.misses = self.disk_hits = self.disk_writes = self.errors = 0
        self._logged: tuple[int, int] | None = None
        if mode == 'disk' and directory is not None:
            directory.mkdir(parents=True, exist_ok=True)
            os.chmod(directory, 0o700)

    @property
    def enabled(self) -> bool:
        return self.mode != 'off' and self.max_entries > 0

    # ------------------------------------------------------------------ lookup / store
    def get(self, key: str) -> TilePrediction | None:
        if not self.enabled:
            return None
        with self._lock:
            pred = self._lru.get(key)
            if pred is not None:
                self._lru.move_to_end(key)
                self.hits += 1
                return pred
        if self.mode == 'disk':
            pred = self._read(key)
            if pred is not None:
                with self._lock:
                    self.hits += 1
                    self.disk_hits += 1
                    self._remember(key, pred)
                return pred
        with self._lock:
            self.misses += 1
        return None

    def put(self, key: str, pred: TilePrediction) -> TilePrediction:
        """Store and return the frozen copy (callers use the returned object so a hit and a miss look the same)."""
        frozen = _frozen(pred)
        if not self.enabled:
            return frozen
        with self._lock:
            self._remember(key, frozen)
        if self.mode == 'disk':
            self._write(key, frozen)
        return frozen

    def _remember(self, key: str, pred: TilePrediction) -> None:
        self._lru[key] = pred
        self._lru.move_to_end(key)
        while len(self._lru) > self.max_entries:
            self._lru.popitem(last=False)

    # ------------------------------------------------------------------ disk mode
    def _path(self, key: str) -> Path:
        assert self.directory is not None
        return self.directory / f'{key}.npz'

    def _write(self, key: str, pred: TilePrediction) -> None:
        assert self.directory is not None
        try:
            fd, tmp = tempfile.mkstemp(dir=self.directory, suffix='.tmp')
            with os.fdopen(fd, 'wb') as fh:
                np.savez(fh, wt=np.array(pred.wt, dtype='U1'), mut=np.array(pred.mut, dtype='U1'),
                         **{name: getattr(pred, name) for name in _FIELDS + _OPTIONAL
                            if getattr(pred, name) is not None})
            os.replace(tmp, self._path(key))
            with self._lock:
                self.disk_writes += 1
        except OSError as exc:
            with self._lock:
                self.errors += 1
            log.error('prediction cache write failed: %s', type(exc).__name__)

    def _read(self, key: str) -> TilePrediction | None:
        path = self._path(key)
        if not path.is_file():
            return None
        try:
            with np.load(path, allow_pickle=False) as z:
                pred = TilePrediction(wt=[str(x) for x in z['wt']], mut=[str(x) for x in z['mut']],
                                      **{name: z[name] for name in _FIELDS + _OPTIONAL if name in z.files})
            return _frozen(pred)
        except (OSError, ValueError, KeyError) as exc:
            with self._lock:
                self.errors += 1
            log.error('prediction cache entry unreadable, ignored: %s', type(exc).__name__)
            return None

    # ------------------------------------------------------------------ statistics
    def stats(self) -> CacheStats:
        with self._lock:
            return CacheStats(self.mode, len(self._lru), self.max_entries, self.hits, self.misses, self.disk_hits,
                              self.disk_writes, self.errors)

    def log_stats_if_changed(self) -> None:
        """Counts only, one structured line when they changed since the last call (no sequence, no key)."""
        st = self.stats()
        if self._logged == (st.hits, st.misses):
            return
        self._logged = (st.hits, st.misses)
        log.info('prediction cache mode=%s entries=%d hits=%d misses=%d disk_hits=%d disk_writes=%d errors=%d',
                 st.mode, st.entries, st.hits, st.misses, st.disk_hits, st.disk_writes, st.errors)


__all__ = ['PredictionCache', 'CacheStats', 'cache_key', 'MODES']
