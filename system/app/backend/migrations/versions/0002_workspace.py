"""workspace tables (system/db-design.md §11)

Revision ID: 0002
Revises: 0001

Eight project-owned tables: project, analysis_job, job_item, analysis_run, analysis_cell, import_dataset,
import_observation, comparison. Reference tables of 0001 are not touched. Composite foreign keys on (project_id, …) keep
runs, jobs, datasets and comparisons inside one project. The new domain_status checks already carry the two R3
borderline states; migration 0003 extends the existing `tile` constraint.
"""
from alembic import op
import sqlalchemy as sa


revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('project',
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('deletion_state', sa.Text(), server_default='active', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("deletion_state IN ('active','deleting')", name=op.f('ck_project_deletion_state')),
    sa.CheckConstraint('length(name) BETWEEN 1 AND 200', name=op.f('ck_project_name_length')),
    sa.PrimaryKeyConstraint('project_id', name=op.f('pk_project'))
    )
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.create_index('project_updated_idx', ['updated_at', 'project_id'], unique=False)

    op.create_table('analysis_job',
    sa.Column('job_id', sa.String(length=36), nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('mode', sa.Text(), nullable=False),
    sa.Column('state', sa.Text(), server_default='pending', nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('input_snapshot', sa.JSON(), nullable=False),
    sa.Column('configuration_snapshot', sa.JSON(), nullable=False),
    sa.Column('coverage', sa.JSON(), nullable=True),
    sa.Column('model_id', sa.Text(), nullable=False),
    sa.Column('model_sha256', sa.CHAR(length=64), nullable=False),
    sa.Column('calibrator', sa.Text(), nullable=False),
    sa.Column('gate_model_id', sa.Text(), nullable=True),
    sa.Column('gate_sha256', sa.CHAR(length=64), nullable=True),
    sa.Column('cancel_requested', sa.Boolean(), server_default=sa.text('(false)'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("mode IN ('peptides','protein')", name=op.f('ck_analysis_job_mode')),
    sa.CheckConstraint("state IN ('pending','running','completed','partial','failed','cancelled')", name=op.f('ck_analysis_job_state')),
    sa.CheckConstraint('total >= 0', name=op.f('ck_analysis_job_total_nonneg')),
    sa.ForeignKeyConstraint(['gate_model_id'], ['model_version.model_id'], name=op.f('fk_analysis_job_gate_model_id_model_version')),
    sa.ForeignKeyConstraint(['model_id'], ['model_version.model_id'], name=op.f('fk_analysis_job_model_id_model_version')),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], name=op.f('fk_analysis_job_project_id_project'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('job_id', name=op.f('pk_analysis_job')),
    sa.UniqueConstraint('project_id', 'job_id', name='uq_analysis_job_project_job')
    )
    with op.batch_alter_table('analysis_job', schema=None) as batch_op:
        batch_op.create_index('analysis_job_project_idx', ['project_id', 'created_at', 'job_id'], unique=False)
        batch_op.create_index('analysis_job_state_idx', ['state', 'created_at'], unique=False)

    op.create_table('import_dataset',
    sa.Column('dataset_id', sa.String(length=36), nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('state', sa.Text(), server_default='staged', nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('sha256', sa.CHAR(length=64), nullable=False),
    sa.Column('assay', sa.Text(), nullable=False),
    sa.Column('assay_version', sa.Text(), nullable=True),
    sa.Column('endpoint', sa.Text(), nullable=False),
    sa.Column('units', sa.Text(), nullable=False),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('reference_description', sa.Text(), nullable=False),
    sa.Column('compatibility', sa.Text(), nullable=False),
    sa.Column('rights_note', sa.Text(), nullable=True),
    sa.Column('committable', sa.Boolean(), nullable=False),
    sa.Column('counts', sa.JSON(), nullable=False),
    sa.Column('validation_report', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('committed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("compatibility IN ('zhang_gps_dpsi','other')", name=op.f('ck_import_dataset_compatibility')),
    sa.CheckConstraint("state <> 'committed' OR committed_at IS NOT NULL", name=op.f('ck_import_dataset_committed_has_date')),
    sa.CheckConstraint("state <> 'staged' OR expires_at IS NOT NULL", name=op.f('ck_import_dataset_staged_expires')),
    sa.CheckConstraint("state IN ('staged','committed','expired')", name=op.f('ck_import_dataset_state')),
    sa.CheckConstraint('length(name) BETWEEN 1 AND 200', name=op.f('ck_import_dataset_name_length')),
    sa.CheckConstraint('revision >= 1', name=op.f('ck_import_dataset_revision_pos')),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], name=op.f('fk_import_dataset_project_id_project'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('dataset_id', name=op.f('pk_import_dataset')),
    sa.UniqueConstraint('project_id', 'dataset_id', name='uq_import_dataset_project_dataset'),
    sa.UniqueConstraint('project_id', 'name', 'revision', name='uq_import_dataset_revision')
    )
    with op.batch_alter_table('import_dataset', schema=None) as batch_op:
        batch_op.create_index('import_dataset_project_idx', ['project_id', 'state'], unique=False)

    op.create_table('import_observation',
    sa.Column('observation_id', sa.String(length=36), nullable=False),
    sa.Column('dataset_id', sa.String(length=36), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('peptide_id', sa.Text(), nullable=False),
    sa.Column('wt_sequence', sa.CHAR(length=28), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('wt_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('mut_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('replicate_id', sa.Text(), nullable=False),
    sa.Column('observed_value', sa.Float(), nullable=True),
    sa.Column('missing_reason', sa.Text(), nullable=True),
    sa.Column('uniprot_acc', sa.Text(), nullable=True),
    sa.Column('reference_release', sa.Text(), nullable=True),
    sa.Column('start_pos', sa.Integer(), nullable=True),
    sa.CheckConstraint("mut_aa IN ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')", name=op.f('ck_import_observation_mut_aa')),
    sa.CheckConstraint("wt_aa IN ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')", name=op.f('ck_import_observation_wt_aa')),
    sa.CheckConstraint('(observed_value IS NULL) <> (missing_reason IS NULL)', name=op.f('ck_import_observation_value_or_reason')),
    sa.CheckConstraint('length(replicate_id) >= 1', name=op.f('ck_import_observation_replicate_present')),
    sa.CheckConstraint('length(wt_sequence) = 28', name=op.f('ck_import_observation_len28')),
    sa.CheckConstraint('mut_aa <> wt_aa', name=op.f('ck_import_observation_mut_ne_wt')),
    sa.CheckConstraint('position BETWEEN 1 AND 28', name=op.f('ck_import_observation_position_range')),
    sa.CheckConstraint('row_number >= 1', name=op.f('ck_import_observation_row_pos')),
    sa.CheckConstraint('start_pos IS NULL OR start_pos >= 1', name=op.f('ck_import_observation_start_pos')),
    sa.ForeignKeyConstraint(['dataset_id'], ['import_dataset.dataset_id'], name=op.f('fk_import_observation_dataset_id_import_dataset'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('observation_id', name=op.f('pk_import_observation')),
    sa.UniqueConstraint('dataset_id', 'wt_sequence', 'position', 'mut_aa', 'replicate_id', name='uq_import_observation_key')
    )
    op.create_table('job_item',
    sa.Column('job_id', sa.String(length=36), nullable=False),
    sa.Column('item_id', sa.Text(), nullable=False),
    sa.Column('ordinal', sa.Integer(), nullable=False),
    sa.Column('input_id', sa.Text(), nullable=False),
    sa.Column('sequence', sa.Text(), nullable=True),
    sa.Column('uniprot_acc', sa.Text(), nullable=True),
    sa.Column('reference_release', sa.Text(), nullable=True),
    sa.Column('tile_index', sa.Integer(), nullable=True),
    sa.Column('start_pos', sa.Integer(), nullable=True),
    sa.Column('end_pos', sa.Integer(), nullable=True),
    sa.Column('state', sa.Text(), server_default='pending', nullable=False),
    sa.Column('domain_status', sa.Text(), nullable=True),
    sa.Column('error', sa.JSON(), nullable=True),
    sa.Column('lease_owner', sa.Text(), nullable=True),
    sa.Column('lease_expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('attempts', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("domain_status IS NULL OR domain_status IN ('measured_in_domain','measured_out_of_domain','measured_unreliable','measured_borderline','predicted_in_domain','predicted_out_of_domain','predicted_borderline','unknown')", name=op.f('ck_job_item_domain_status')),
    sa.CheckConstraint("state <> 'running' OR (lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL)", name=op.f('ck_job_item_running_has_lease')),
    sa.CheckConstraint("state IN ('pending','running','succeeded','refused','failed','cancelled')", name=op.f('ck_job_item_state')),
    sa.CheckConstraint('attempts >= 0', name=op.f('ck_job_item_attempts_nonneg')),
    sa.CheckConstraint('ordinal >= 1', name=op.f('ck_job_item_ordinal_pos')),
    sa.CheckConstraint('tile_index IS NULL OR (tile_index >= 1 AND start_pos = (tile_index - 1) * 23 + 1 AND end_pos = start_pos + 27)', name=op.f('ck_job_item_tile_formula')),
    sa.ForeignKeyConstraint(['job_id'], ['analysis_job.job_id'], name=op.f('fk_job_item_job_id_analysis_job'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('job_id', 'item_id', name=op.f('pk_job_item')),
    sa.UniqueConstraint('job_id', 'ordinal', name='uq_job_item_job_ordinal')
    )
    with op.batch_alter_table('job_item', schema=None) as batch_op:
        batch_op.create_index('job_item_lease_idx', ['lease_expires_at'], unique=False)
        batch_op.create_index('job_item_state_idx', ['job_id', 'state'], unique=False)

    op.create_table('analysis_run',
    sa.Column('analysis_id', sa.String(length=36), nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('job_id', sa.String(length=36), nullable=True),
    sa.Column('item_id', sa.Text(), nullable=True),
    sa.Column('parent_analysis_id', sa.String(length=36), nullable=True),
    sa.Column('model_id', sa.Text(), nullable=False),
    sa.Column('input_kind', sa.Text(), nullable=False),
    sa.Column('input_sequence', sa.CHAR(length=28), nullable=False),
    sa.Column('uniprot_acc', sa.Text(), nullable=True),
    sa.Column('tile_index', sa.Integer(), nullable=True),
    sa.Column('domain_status', sa.Text(), nullable=False),
    sa.Column('snapshot_version', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('result', sa.JSON(), nullable=False),
    sa.Column('provenance', sa.JSON(), nullable=False),
    sa.Column('annotation_snapshot', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("domain_status IN ('measured_in_domain','measured_out_of_domain','measured_unreliable','measured_borderline','predicted_in_domain','predicted_out_of_domain','predicted_borderline','unknown')", name=op.f('ck_analysis_run_domain_status')),
    sa.CheckConstraint("input_kind IN ('sequence','uniprot_tile')", name=op.f('ck_analysis_run_input_kind')),
    sa.CheckConstraint('(job_id IS NULL) = (item_id IS NULL)', name=op.f('ck_analysis_run_job_item_pair')),
    sa.CheckConstraint('length(input_sequence) = 28', name=op.f('ck_analysis_run_len28')),
    sa.CheckConstraint('snapshot_version >= 1', name=op.f('ck_analysis_run_snapshot_version_pos')),
    sa.ForeignKeyConstraint(['job_id', 'item_id'], ['job_item.job_id', 'job_item.item_id'], name='fk_analysis_run_job_item', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['model_id'], ['model_version.model_id'], name=op.f('fk_analysis_run_model_id_model_version')),
    sa.ForeignKeyConstraint(['project_id', 'job_id'], ['analysis_job.project_id', 'analysis_job.job_id'], name='fk_analysis_run_project_job', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], name=op.f('fk_analysis_run_project_id_project'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('analysis_id', name=op.f('pk_analysis_run')),
    sa.UniqueConstraint('job_id', 'item_id', name='uq_analysis_run_job_item'),
    sa.UniqueConstraint('project_id', 'analysis_id', name='uq_analysis_run_project_analysis')
    )
    with op.batch_alter_table('analysis_run', schema=None) as batch_op:
        batch_op.create_index('analysis_run_project_idx', ['project_id', 'created_at', 'analysis_id'], unique=False)

    op.create_table('analysis_cell',
    sa.Column('analysis_id', sa.String(length=36), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('mut_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('wt_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('score_raw', sa.Float(), nullable=False),
    sa.Column('prob_calibrated', sa.Float(), nullable=False),
    sa.Column('rank_in_tile', sa.Integer(), nullable=False),
    sa.Column('top10', sa.Boolean(), nullable=False),
    sa.CheckConstraint("mut_aa IN ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')", name=op.f('ck_analysis_cell_mut_aa')),
    sa.CheckConstraint("wt_aa IN ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')", name=op.f('ck_analysis_cell_wt_aa')),
    sa.CheckConstraint('mut_aa <> wt_aa', name=op.f('ck_analysis_cell_mut_ne_wt')),
    sa.CheckConstraint('position BETWEEN 1 AND 28', name=op.f('ck_analysis_cell_position_range')),
    sa.CheckConstraint('prob_calibrated BETWEEN 0 AND 1', name=op.f('ck_analysis_cell_prob_range')),
    sa.CheckConstraint('rank_in_tile BETWEEN 1 AND 532', name=op.f('ck_analysis_cell_rank_range')),
    sa.ForeignKeyConstraint(['analysis_id'], ['analysis_run.analysis_id'], name=op.f('fk_analysis_cell_analysis_id_analysis_run'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('analysis_id', 'position', 'mut_aa', name=op.f('pk_analysis_cell'))
    )
    op.create_table('comparison',
    sa.Column('comparison_id', sa.String(length=36), nullable=False),
    sa.Column('project_id', sa.String(length=36), nullable=False),
    sa.Column('analysis_id', sa.String(length=36), nullable=False),
    sa.Column('dataset_id', sa.String(length=36), nullable=False),
    sa.Column('replicate_id', sa.Text(), nullable=True),
    sa.Column('aggregation', sa.Text(), nullable=True),
    sa.Column('compatible', sa.Boolean(), nullable=False),
    sa.Column('matched', sa.Integer(), nullable=False),
    sa.Column('counts', sa.JSON(), nullable=False),
    sa.Column('mae', sa.Float(), nullable=True),
    sa.Column('spearman', sa.Float(), nullable=True),
    sa.Column('metric_unavailable_reason', sa.Text(), nullable=True),
    sa.Column('rows', sa.JSON(), nullable=False),
    sa.Column('provenance', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("aggregation IS NULL OR aggregation IN ('mean','median')", name=op.f('ck_comparison_aggregation')),
    sa.CheckConstraint('(replicate_id IS NULL) <> (aggregation IS NULL)', name=op.f('ck_comparison_replicate_or_aggregation')),
    sa.CheckConstraint('matched >= 0', name=op.f('ck_comparison_matched_nonneg')),
    sa.ForeignKeyConstraint(['project_id', 'analysis_id'], ['analysis_run.project_id', 'analysis_run.analysis_id'], name='fk_comparison_project_analysis', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id', 'dataset_id'], ['import_dataset.project_id', 'import_dataset.dataset_id'], name='fk_comparison_project_dataset', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], name=op.f('fk_comparison_project_id_project'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('comparison_id', name=op.f('pk_comparison'))
    )
    with op.batch_alter_table('comparison', schema=None) as batch_op:
        batch_op.create_index('comparison_analysis_idx', ['analysis_id', 'created_at', 'comparison_id'], unique=False)
        batch_op.create_index('comparison_dataset_idx', ['dataset_id'], unique=False)



def downgrade() -> None:
    with op.batch_alter_table('comparison', schema=None) as batch_op:
        batch_op.drop_index('comparison_dataset_idx')
        batch_op.drop_index('comparison_analysis_idx')

    op.drop_table('comparison')
    op.drop_table('analysis_cell')
    with op.batch_alter_table('analysis_run', schema=None) as batch_op:
        batch_op.drop_index('analysis_run_project_idx')

    op.drop_table('analysis_run')
    with op.batch_alter_table('job_item', schema=None) as batch_op:
        batch_op.drop_index('job_item_state_idx')
        batch_op.drop_index('job_item_lease_idx')

    op.drop_table('job_item')
    op.drop_table('import_observation')
    with op.batch_alter_table('import_dataset', schema=None) as batch_op:
        batch_op.drop_index('import_dataset_project_idx')

    op.drop_table('import_dataset')
    with op.batch_alter_table('analysis_job', schema=None) as batch_op:
        batch_op.drop_index('analysis_job_state_idx')
        batch_op.drop_index('analysis_job_project_idx')

    op.drop_table('analysis_job')
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_index('project_updated_idx')

    op.drop_table('project')
