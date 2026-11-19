"""model_comparison: descriptive comparison of two saved analyses of the same tile

Revision ID: 0006
Revises: 0005

plan-system 2.2 (18 Nov 2026). A saved comparison of two analyses (usually two models) of one tile sequence: metrics,
largest disagreements and the provenance of both sides. Owned by the project of both analyses; deleted with either
analysis or the project (FK cascade, as `comparison`).
"""
import sqlalchemy as sa
from alembic import op


revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('model_comparison',
    sa.Column('comparison_id', sa.String(length=36), nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('analysis_a', sa.String(length=36), nullable=False),
    sa.Column('analysis_b', sa.String(length=36), nullable=False),
    sa.Column('sequence_sha256', sa.CHAR(length=64), nullable=False),
    sa.Column('metrics', sa.JSON(), nullable=False),
    sa.Column('disagreements', sa.JSON(), nullable=False),
    sa.Column('provenance', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint('analysis_a <> analysis_b', name=op.f('ck_model_comparison_distinct_analyses')),
    sa.ForeignKeyConstraint(['project_id', 'analysis_a'], ['analysis_run.project_id', 'analysis_run.analysis_id'], name='fk_model_comparison_project_analysis_a', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id', 'analysis_b'], ['analysis_run.project_id', 'analysis_run.analysis_id'], name='fk_model_comparison_project_analysis_b', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], name=op.f('fk_model_comparison_project_id_project'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('comparison_id', name=op.f('pk_model_comparison'))
    )
    with op.batch_alter_table('model_comparison', schema=None) as batch_op:
        batch_op.create_index('model_comparison_project_idx', ['project_id', 'created_at', 'comparison_id'], unique=False)
        batch_op.create_index('model_comparison_a_idx', ['analysis_a'], unique=False)
        batch_op.create_index('model_comparison_b_idx', ['analysis_b'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('model_comparison', schema=None) as batch_op:
        batch_op.drop_index('model_comparison_b_idx')
        batch_op.drop_index('model_comparison_a_idx')
        batch_op.drop_index('model_comparison_project_idx')
    op.drop_table('model_comparison')
