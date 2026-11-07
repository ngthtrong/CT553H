"""Aggregate counters per day, endpoint template and model; never sequences, accessions or addresses."""
from __future__ import annotations

import threading
from collections import Counter
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from db.models import UsageDaily


class UsageCounter:
    def __init__(self) -> None:
        self._n: Counter[tuple[date, str, str]] = Counter()
        self._err: Counter[tuple[date, str, str]] = Counter()
        self._lock = threading.Lock()

    def record(self, endpoint: str, model_id: str, error: bool) -> None:
        key = (datetime.now(UTC).date(), endpoint, model_id)
        with self._lock:
            self._n[key] += 1
            if error:
                self._err[key] += 1

    def flush(self, factory: sessionmaker[Session]) -> int:
        with self._lock:
            n, err = self._n, self._err
            self._n, self._err = Counter(), Counter()
        if not n:
            return 0
        with factory() as s, s.begin():
            for key, count in n.items():
                row = s.execute(select(UsageDaily).where(
                    UsageDaily.day == key[0], UsageDaily.endpoint == key[1],
                    UsageDaily.model_id == key[2])).scalar_one_or_none()
                if row is None:
                    s.add(UsageDaily(day=key[0], endpoint=key[1], model_id=key[2],
                                     n_requests=count, n_errors=err.get(key, 0)))
                else:
                    row.n_requests += count
                    row.n_errors += err.get(key, 0)
        return len(n)
