import os

from alembic import context
from sqlalchemy import create_engine, pool

from db.models import Base

config = context.config
target_metadata = Base.metadata


def _url() -> str:
    return (config.get_main_option('sqlalchemy.url') or os.environ.get('DF_DATABASE_URL')
            or 'sqlite:///./degron.db')


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True,
                      render_as_batch=_url().startswith('sqlite'))
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = config.attributes.get('connection')
    if connectable is None:
        connectable = create_engine(_url(), poolclass=pool.NullPool)
        owns = True
    else:
        owns = False
    conn = connectable if not owns else connectable.connect()
    try:
        context.configure(connection=conn, target_metadata=target_metadata,
                          render_as_batch=conn.dialect.name == 'sqlite')
        with context.begin_transaction():
            context.run_migrations()
    finally:
        if owns:
            conn.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
