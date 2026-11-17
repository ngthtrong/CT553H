"""Per-application state shared by the routers (settings, database, models, limiter, counters)."""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from degron_footprint.domain import GateAdapter, load_gate
from degron_footprint.gate_r3 import GATE_CARD  # importing it also registers the R3 gate loader

from . import repository as repo
from .config import Settings
from .ratelimit import RateLimiter
from .service import Predictor, Registry, load_registry
from .usage import UsageCounter

log = logging.getLogger('api.core')


@dataclass
class Core:
    settings: Settings
    engine: Engine
    factory: sessionmaker[Session]
    registry: Registry
    gate: GateAdapter
    predictor: Predictor
    limiter: RateLimiter
    usage: UsageCounter = field(default_factory=UsageCounter)
    tasks: list[asyncio.Task] = field(default_factory=list)

    def reload_registry(self) -> None:
        self.registry = load_registry(self.factory, self.settings.model_dir)
        self.predictor.registry = self.registry

    def purge_expired(self) -> int:
        """Legacy expired share runs, plus abandoned import previews (db-design §9: proposed 24 h)."""
        from .datasets import purge_expired_staged
        from .workspace import WorkspacePathError, resolve_stored
        with self.factory() as s, s.begin():
            n = repo.purge_expired(s)
            files = purge_expired_staged(s)
        for _project, rel in files:
            try:
                resolve_stored(self.settings.workspace_dir, rel).unlink(missing_ok=True)
            except (OSError, WorkspacePathError) as exc:
                log.error('staged import file not removed: %s', type(exc).__name__)
        return n + len(files)


def build_core(settings: Settings, engine: Engine, factory: sessionmaker[Session]) -> Core:
    registry = load_registry(factory, settings.model_dir)
    gate = load_gate(settings.gate_weights, settings.gate_card or settings.model_dir / GATE_CARD)
    return Core(settings=settings, engine=engine, factory=factory, registry=registry, gate=gate,
                predictor=Predictor(registry, gate, factory), limiter=RateLimiter(settings.rate_window_seconds))


def load_contract(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    return json.loads(json.dumps(data, default=str))
