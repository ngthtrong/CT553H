"""add the R3 borderline domain states to tile.domain_status (DEVIATIONS.md §7)

Revision ID: 0003
Revises: 0002

Only the CHECK constraint changes; no row is rewritten or relabelled (db-design §3.3: historical snapshots are not
relabelled under a newer gate). SQLite cannot alter a CHECK in place, so batch mode rebuilds `tile` with the same
columns, keys and indexes. Downgrade refuses while any tile still holds a borderline state rather than deleting or
silently mapping it.
"""
from alembic import op
import sqlalchemy as sa


revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

OLD = ("domain_status IN ('measured_in_domain','measured_out_of_domain','measured_unreliable',"
       "'predicted_in_domain','predicted_out_of_domain','unknown')")
NEW = ("domain_status IN ('measured_in_domain','measured_out_of_domain','measured_unreliable','measured_borderline',"
       "'predicted_in_domain','predicted_out_of_domain','predicted_borderline','unknown')")


def _swap(expr: str) -> None:
    bind = op.get_bind()
    # The SQLite rebuild drops the old `tile`; with foreign keys on, that DROP would cascade into measured_cell.
    if bind.dialect.name == 'sqlite' and bind.execute(sa.text('PRAGMA foreign_keys')).scalar():
        raise RuntimeError('run this migration with PRAGMA foreign_keys=OFF (the Alembic env does so by default)')
    # 'auto': PostgreSQL alters in place; SQLite must rebuild the table to drop a CHECK.
    with op.batch_alter_table('tile', recreate='auto') as batch_op:
        batch_op.drop_constraint(op.f('ck_tile_domain_status'), type_='check')
        batch_op.create_check_constraint('domain_status', expr)


def upgrade() -> None:
    _swap(NEW)


def downgrade() -> None:
    n = op.get_bind().execute(sa.text(
        "SELECT count(*) FROM tile WHERE domain_status IN ('measured_borderline','predicted_borderline')")).scalar()
    if n:
        raise RuntimeError(f'{n} tiles hold a borderline domain status; reload or relabel them before downgrading')
    _swap(OLD)
