from __future__ import annotations

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from .core import Core


def get_core(request: Request) -> Core:
    return request.app.state.core


def get_session(request: Request) -> Iterator[Session]:
    core: Core = request.app.state.core
    with core.factory() as s:
        yield s
