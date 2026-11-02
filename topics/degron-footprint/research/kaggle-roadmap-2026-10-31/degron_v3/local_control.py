"""Local session control and recoverable checkpoints; no scientific settings."""
from contextlib import contextmanager
import hashlib
import json
import os
import pickle
from pathlib import Path
import random
import signal
import time

import numpy as np
import torch

from .common import atomic_json


class Paused(Exception):
    pass


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def atomic_torch(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('wb') as stream:
        torch.save(state, stream)
        stream.flush()
        os.fsync(stream.fileno())
    if path.exists():
        try:
            torch.load(path, map_location='cpu', weights_only=True)
            valid = True
        except (RuntimeError, EOFError, OSError, ValueError, pickle.UnpicklingError):
            valid = False
        if valid:
            os.replace(path, path.with_suffix(path.suffix + '.previous'))
    os.replace(temporary, path)


def load_torch(path, identity=None):
    path = Path(path)
    for candidate in [path, path.with_suffix(path.suffix + '.previous')]:
        if not candidate.exists():
            continue
        try:
            state = torch.load(candidate, map_location='cpu', weights_only=True)
        except (RuntimeError, EOFError, OSError, ValueError, pickle.UnpicklingError):
            continue
        if identity is not None and state.get('identity') != identity:
            raise ValueError('Checkpoint identity changed; use a new campaign')
        return state
    if path.exists() or path.with_suffix(path.suffix + '.previous').exists():
        raise ValueError(f'No readable checkpoint generation: {path}')
    return None


def rng_state():
    n = np.random.get_state()
    return dict(python=random.getstate(), numpy=[n[0], n[1].tolist(), n[2], n[3], n[4]],
                torch=torch.get_rng_state(), cuda=torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [])


def restore_rng(state):
    random.setstate(state['python'])
    n = state['numpy']
    np.random.set_state((n[0], np.asarray(n[1], dtype=np.uint32), n[2], n[3], n[4]))
    torch.set_rng_state(state['torch'])
    if state['cuda']:
        torch.cuda.set_rng_state_all(state['cuda'])


class Control:
    def __init__(self, campaign, job, deadline=0, checkpoint_seconds=120, log_seconds=20):
        self.campaign, self.job = Path(campaign), job
        self.deadline, self.interval, self.log_interval = deadline, checkpoint_seconds, log_seconds
        self.stop_file = self.campaign / 'STOP'
        self.requested = False
        self.last_checkpoint = self.last_log = time.monotonic()
        self.steps, self.pause_after_steps = 0, None  # deterministic validation hook

    def interrupted(self, *_):
        self.requested = True

    def stopping(self):
        return (self.requested or self.stop_file.exists() or
                bool(self.deadline and time.time() >= self.deadline) or
                bool(self.pause_after_steps is not None and self.steps >= self.pause_after_steps))

    def check(self):
        if self.stopping():
            raise Paused('Session deadline or pause request; committed work retained')

    def due(self):
        return self.stopping() or time.monotonic() - self.last_checkpoint >= self.interval

    def committed(self, detail):
        self.last_checkpoint = time.monotonic()
        self.log('CHECKPOINT ' + detail, force=True)

    def log(self, message, force=False, **progress):
        if force or time.monotonic() - self.last_log >= self.log_interval:
            self.last_log = time.monotonic()
            suffix = ''
            if torch.cuda.is_initialized():
                suffix = f' | GPU allocated={torch.cuda.memory_allocated()/2**30:.2f}GiB reserved={torch.cuda.memory_reserved()/2**30:.2f}GiB'
            print(time.strftime('%H:%M:%S'), self.job, message + suffix, flush=True)
            atomic_json(self.campaign / 'progress.json', dict(job=self.job, message=message,
                updated_unix=time.time(), **progress))


@contextmanager
def process_lock(path):
    """An OS-owned lock releases even when a terminal is closed or a process dies."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        if path.stat().st_size == 0:
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError('Another local session already owns the GPU/session lock') from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def install_pause_handler(control):
    signal.signal(signal.SIGINT, control.interrupted)
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, control.interrupted)
