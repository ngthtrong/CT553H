"""In-memory sliding-window rate limiter. Keys are salted hashes of the client address, held in memory only."""
from __future__ import annotations

import hashlib
import secrets
import threading
import time
from collections import defaultdict, deque
from collections.abc import Callable


class RateLimiter:
    def __init__(self, window_seconds: int = 60, clock: Callable[[], float] = time.monotonic):
        self.window = window_seconds
        self.clock = clock
        self._salt = secrets.token_bytes(16)
        self._hits: dict[tuple[str, str], deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def _key(self, client: str, bucket: str) -> tuple[str, str]:
        return hashlib.sha256(self._salt + client.encode()).hexdigest()[:24], bucket

    def check(self, client: str, bucket: str, limit: int) -> tuple[bool, int]:
        """-> (allowed, retry_after_seconds). A rejected request is not counted."""
        now = self.clock()
        k = self._key(client, bucket)
        with self._lock:
            q = self._hits[k]
            while q and now - q[0] >= self.window:
                q.popleft()
            if len(q) >= limit:
                return False, max(1, int(self.window - (now - q[0])) + 1)
            q.append(now)
            if len(self._hits) > 50000:                     # bound memory under address churn
                for key in [key for key, d in self._hits.items() if not d or now - d[-1] >= self.window]:
                    del self._hits[key]
            return True, 0
