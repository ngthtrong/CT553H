"""analysis_job.priority: small jobs before long scans

Revision ID: 0008
Revises: 0007

plan-system 4.5 (18 Nov 2026). Workers claim items of higher-priority jobs first (then oldest job first). Existing jobs
get 0 (normal).
"""
import sqlalchemy as sa
from alembic import op


revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('analysis_job', recreate='never') as batch_op:
        batch_op.add_column(sa.Column('priority', sa.Integer(), server_default=sa.text('0'), nullable=False))


def downgrade() -> None:
    with op.batch_alter_table('analysis_job', recreate='never') as batch_op:
        batch_op.drop_column('priority')
