"""worker_heartbeat: liveness of job workers for the local admin page

Revision ID: 0007
Revises: 0006

plan-system 4.2/4.5 (18 Nov 2026). One row per worker process (owner = host:pid:random), updated at most every few
seconds while it runs and stamped when it stops. Operational data only: no sequence, no input id.
"""
import sqlalchemy as sa
from alembic import op


revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('worker_heartbeat',
    sa.Column('owner', sa.Text(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('stopped_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('items_done', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.CheckConstraint('items_done >= 0', name=op.f('ck_worker_heartbeat_items_nonneg')),
    sa.PrimaryKeyConstraint('owner', name=op.f('pk_worker_heartbeat'))
    )


def downgrade() -> None:
    op.drop_table('worker_heartbeat')
