"""seed spread of ensemble scores; measured duration of job items

Revision ID: 0005
Revises: 0004

plan-system 1.3 and 1.7 (18 Nov 2026). Nullable columns only, no row changes, no constraint (SQLite adds columns in
place with recreate='never'):

* `analysis_cell` and `prediction_cell`: `score_seed_sd` (population standard deviation, ddof = 0, of the per-seed raw
  scores), `score_seed_min`, `score_seed_max`. NULL for models without seeds (the npz ridge model) and for every row
  written before this revision; snapshots stay readable (FR-22).
* `job_item.duration_ms`: wall time the worker spent on the item (scoring and commit), used for the job ETA. NULL for
  items refused at submission and for items finished before this revision.
"""
import sqlalchemy as sa
from alembic import op


revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None

SEED_COLUMNS = ('score_seed_sd', 'score_seed_min', 'score_seed_max')


def upgrade() -> None:
    for table in ('analysis_cell', 'prediction_cell'):
        with op.batch_alter_table(table, recreate='never') as batch_op:
            for name in SEED_COLUMNS:
                batch_op.add_column(sa.Column(name, sa.Float(), nullable=True))
    with op.batch_alter_table('job_item', recreate='never') as batch_op:
        batch_op.add_column(sa.Column('duration_ms', sa.Float(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('job_item', recreate='never') as batch_op:
        batch_op.drop_column('duration_ms')
    for table in ('prediction_cell', 'analysis_cell'):
        with op.batch_alter_table(table, recreate='never') as batch_op:
            for name in reversed(SEED_COLUMNS):
                batch_op.drop_column(name)
