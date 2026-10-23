"""Engine and session factory. SQLite gets foreign keys switched on (it is off by default)."""
from __future__ import annotations

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


def make_engine(url: str, echo: bool = False) -> Engine:
    kwargs: dict = {'echo': echo, 'future': True}
    if url.startswith('sqlite'):
        kwargs['connect_args'] = {'check_same_thread': False}
        if url in ('sqlite://', 'sqlite:///:memory:'):
            kwargs['poolclass'] = StaticPool
    else:
        kwargs['pool_pre_ping'] = True
    engine = create_engine(url, **kwargs)
    if engine.dialect.name == 'sqlite':
        @event.listens_for(engine, 'connect')
        def _fk_on(dbapi_conn, _record):               # pragma: no cover - trivial
            cur = dbapi_conn.cursor()
            cur.execute('PRAGMA foreign_keys=ON')
            cur.close()
    return engine


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)
