"""initial schema (system/db-design.md §4)

Revision ID: 0001
Revises:

The 30-day lifetime of a shared run is a PostgreSQL CHECK (interval arithmetic); SQLite relies on the application.
"""
from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('data_source',
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('version', sa.Text(), nullable=False),
    sa.Column('citation', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('license_name', sa.Text(), nullable=False),
    sa.Column('license_class', sa.Text(), nullable=False),
    sa.Column('redistribution_ok', sa.Boolean(), nullable=False),
    sa.Column('attribution_text', sa.Text(), nullable=False),
    sa.Column('disclaimer_text', sa.Text(), nullable=True),
    sa.Column('sha256', sa.CHAR(length=64), nullable=True),
    sa.Column('retrieved_on', sa.Date(), nullable=True),
    sa.CheckConstraint("license_class IN ('open','attribution_required','internal_only','unknown')", name=op.f('ck_data_source_license_class')),
    sa.CheckConstraint("redistribution_ok OR license_class IN ('internal_only','unknown')", name=op.f('ck_data_source_servable')),
    sa.PrimaryKeyConstraint('source_id', name=op.f('pk_data_source'))
    )
    op.create_table('etl_run',
    sa.Column('etl_run_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('git_commit', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('report', sa.JSON(), nullable=False),
    sa.CheckConstraint("status IN ('running','succeeded','failed')", name=op.f('ck_etl_run_status')),
    sa.PrimaryKeyConstraint('etl_run_id', name=op.f('pk_etl_run'))
    )
    op.create_table('model_version',
    sa.Column('model_id', sa.Text(), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.Column('kind', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('is_default', sa.Boolean(), server_default=sa.text('(false)'), nullable=False),
    sa.Column('tile_length', sa.Integer(), server_default=sa.text('(28)'), nullable=False),
    sa.Column('feature_spec', sa.Text(), nullable=False),
    sa.Column('weights_path', sa.Text(), nullable=False),
    sa.Column('weights_sha256', sa.CHAR(length=64), nullable=False),
    sa.Column('event_definition', sa.Text(), nullable=False),
    sa.Column('domain_description', sa.Text(), nullable=False),
    sa.Column('metrics', sa.JSON(), nullable=False),
    sa.Column('calibration', sa.JSON(), nullable=True),
    sa.Column('trained_on_sources', sa.JSON(), nullable=False),
    sa.Column('evidence_label', sa.Text(), server_default='development OOF benchmark, not external validation', nullable=False),
    sa.Column('card_markdown', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('frozen_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("NOT is_default OR status = 'frozen'", name=op.f('ck_model_version_default_is_frozen')),
    sa.CheckConstraint("role IN ('effect','gate')", name=op.f('ck_model_version_role')),
    sa.CheckConstraint("status <> 'frozen' OR frozen_at IS NOT NULL", name=op.f('ck_model_version_frozen_has_date')),
    sa.CheckConstraint("status IN ('candidate','frozen','retired')", name=op.f('ck_model_version_status')),
    sa.PrimaryKeyConstraint('model_id', name=op.f('pk_model_version'))
    )
    with op.batch_alter_table('model_version', schema=None) as batch_op:
        batch_op.create_index('model_default_idx', ['role'], unique=True, postgresql_where=sa.text('is_default'), sqlite_where=sa.text('is_default'))

    op.create_table('usage_daily',
    sa.Column('day', sa.Date(), nullable=False),
    sa.Column('endpoint', sa.Text(), nullable=False),
    sa.Column('model_id', sa.Text(), server_default='', nullable=False),
    sa.Column('n_requests', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('n_errors', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.PrimaryKeyConstraint('day', 'endpoint', 'model_id', name=op.f('pk_usage_daily'))
    )
    op.create_table('etl_input',
    sa.Column('etl_run_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('sha256_expected', sa.CHAR(length=64), nullable=False),
    sa.Column('sha256_actual', sa.CHAR(length=64), nullable=False),
    sa.ForeignKeyConstraint(['etl_run_id'], ['etl_run.etl_run_id'], name=op.f('fk_etl_input_etl_run_id_etl_run'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['source_id'], ['data_source.source_id'], name=op.f('fk_etl_input_source_id_data_source')),
    sa.PrimaryKeyConstraint('etl_run_id', 'source_id', 'file_path', name=op.f('pk_etl_input'))
    )
    op.create_table('protein',
    sa.Column('uniprot_acc', sa.Text(), nullable=False),
    sa.Column('gene_symbol', sa.Text(), nullable=True),
    sa.Column('protein_name', sa.Text(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('sequence', sa.Text(), nullable=False),
    sa.Column('uniprot_release', sa.Text(), nullable=False),
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.CheckConstraint('length = length(sequence)', name=op.f('ck_protein_length_matches')),
    sa.CheckConstraint('length > 0', name=op.f('ck_protein_length_pos')),
    sa.ForeignKeyConstraint(['source_id'], ['data_source.source_id'], name=op.f('fk_protein_source_id_data_source')),
    sa.PrimaryKeyConstraint('uniprot_acc', name=op.f('pk_protein'))
    )
    with op.batch_alter_table('protein', schema=None) as batch_op:
        batch_op.create_index('protein_gene_idx', ['gene_symbol'], unique=False)

    op.create_table('clinvar_variant',
    sa.Column('variation_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('uniprot_acc', sa.Text(), nullable=False),
    sa.Column('protein_pos', sa.Integer(), nullable=False),
    sa.Column('ref_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('alt_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('clinsig', sa.Text(), nullable=False),
    sa.Column('review_status', sa.Text(), nullable=True),
    sa.Column('last_evaluated', sa.Date(), nullable=True),
    sa.Column('clinvar_file_date', sa.Date(), nullable=False),
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.CheckConstraint("clinsig IN ('pathogenic','likely_pathogenic','vus','likely_benign','benign','conflicting','other')", name=op.f('ck_clinvar_variant_clinsig')),
    sa.CheckConstraint('protein_pos >= 1', name=op.f('ck_clinvar_variant_pos_pos')),
    sa.CheckConstraint('ref_aa <> alt_aa', name=op.f('ck_clinvar_variant_ref_ne_alt')),
    sa.ForeignKeyConstraint(['source_id'], ['data_source.source_id'], name=op.f('fk_clinvar_variant_source_id_data_source')),
    sa.ForeignKeyConstraint(['uniprot_acc'], ['protein.uniprot_acc'], name=op.f('fk_clinvar_variant_uniprot_acc_protein'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('variation_id', name=op.f('pk_clinvar_variant'))
    )
    with op.batch_alter_table('clinvar_variant', schema=None) as batch_op:
        batch_op.create_index('clinvar_pos_idx', ['uniprot_acc', 'protein_pos'], unique=False)

    op.create_table('tile',
    sa.Column('tile_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), autoincrement=True, nullable=False),
    sa.Column('uniprot_acc', sa.Text(), nullable=False),
    sa.Column('tile_index', sa.Integer(), nullable=False),
    sa.Column('start_pos', sa.Integer(), nullable=False),
    sa.Column('end_pos', sa.Integer(), nullable=False),
    sa.Column('sequence', sa.CHAR(length=28), nullable=False),
    sa.Column('scorable', sa.Boolean(), nullable=False),
    sa.Column('screen_peptide_id', sa.Text(), nullable=True),
    sa.Column('psi_wt_measured', sa.Float(), nullable=True),
    sa.Column('reads_measured', sa.Float(), nullable=True),
    sa.Column('psi_wt_predicted', sa.Float(), nullable=True),
    sa.Column('psi_wt_predicted_by', sa.Text(), nullable=True),
    sa.Column('domain_status', sa.Text(), server_default='unknown', nullable=False),
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.CheckConstraint("domain_status IN ('measured_in_domain','measured_out_of_domain','measured_unreliable','predicted_in_domain','predicted_out_of_domain','unknown')", name=op.f('ck_tile_domain_status')),
    sa.CheckConstraint("domain_status NOT LIKE 'measured_%' OR psi_wt_measured IS NOT NULL OR domain_status = 'measured_unreliable'", name=op.f('ck_tile_measured_backed')),
    sa.CheckConstraint("domain_status NOT LIKE 'predicted_%' OR (psi_wt_predicted IS NOT NULL AND psi_wt_predicted_by IS NOT NULL)", name=op.f('ck_tile_predicted_backed')),
    sa.CheckConstraint("scorable OR domain_status = 'unknown'", name=op.f('ck_tile_scorable_or_unknown')),
    sa.CheckConstraint('end_pos = start_pos + 27', name=op.f('ck_tile_end_formula')),
    sa.CheckConstraint('length(sequence) = 28', name=op.f('ck_tile_len28')),
    sa.CheckConstraint('reads_measured IS NULL OR reads_measured >= 0', name=op.f('ck_tile_reads_nonneg')),
    sa.CheckConstraint('start_pos = (tile_index - 1) * 23 + 1', name=op.f('ck_tile_start_formula')),
    sa.CheckConstraint('tile_index >= 1', name=op.f('ck_tile_index_pos')),
    sa.ForeignKeyConstraint(['psi_wt_predicted_by'], ['model_version.model_id'], name=op.f('fk_tile_psi_wt_predicted_by_model_version')),
    sa.ForeignKeyConstraint(['source_id'], ['data_source.source_id'], name=op.f('fk_tile_source_id_data_source')),
    sa.ForeignKeyConstraint(['uniprot_acc'], ['protein.uniprot_acc'], name=op.f('fk_tile_uniprot_acc_protein'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tile_id', name=op.f('pk_tile')),
    sa.UniqueConstraint('uniprot_acc', 'tile_index', name=op.f('uq_tile_uniprot_acc'))
    )
    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.create_index('tile_domain_idx', ['uniprot_acc', 'domain_status'], unique=False)
        batch_op.create_index('tile_screen_idx', ['screen_peptide_id'], unique=False, postgresql_where=sa.text('screen_peptide_id IS NOT NULL'), sqlite_where=sa.text('screen_peptide_id IS NOT NULL'))

    op.create_table('measured_cell',
    sa.Column('tile_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('mut_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('delta_psi', sa.Float(), nullable=False),
    sa.Column('in_training_set', sa.Boolean(), server_default=sa.text('(true)'), nullable=False),
    sa.Column('source_id', sa.Text(), nullable=False),
    sa.CheckConstraint("mut_aa IN ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')", name=op.f('ck_measured_cell_mut_aa')),
    sa.CheckConstraint('position BETWEEN 1 AND 28', name=op.f('ck_measured_cell_position_range')),
    sa.ForeignKeyConstraint(['source_id'], ['data_source.source_id'], name=op.f('fk_measured_cell_source_id_data_source')),
    sa.ForeignKeyConstraint(['tile_id'], ['tile.tile_id'], name=op.f('fk_measured_cell_tile_id_tile'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tile_id', 'position', 'mut_aa', name=op.f('pk_measured_cell'))
    )
    op.create_table('prediction_run',
    sa.Column('run_id', sa.String(length=36), nullable=False),
    sa.Column('input_kind', sa.Text(), nullable=False),
    sa.Column('tile_id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=True),
    sa.Column('input_sequence', sa.CHAR(length=28), nullable=False),
    sa.Column('model_id', sa.Text(), nullable=False),
    sa.Column('gate_model_id', sa.Text(), nullable=True),
    sa.Column('domain_status', sa.Text(), nullable=False),
    sa.Column('warnings', sa.JSON(), nullable=False),
    sa.Column('share_token_hash', sa.CHAR(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("input_kind IN ('sequence','uniprot_tile')", name=op.f('ck_prediction_run_input_kind')),
    sa.CheckConstraint('expires_at > created_at', name=op.f('ck_prediction_run_expiry_after_creation')),
    sa.CheckConstraint('length(input_sequence) = 28', name=op.f('ck_prediction_run_len28')),
    sa.ForeignKeyConstraint(['gate_model_id'], ['model_version.model_id'], name=op.f('fk_prediction_run_gate_model_id_model_version')),
    sa.ForeignKeyConstraint(['model_id'], ['model_version.model_id'], name=op.f('fk_prediction_run_model_id_model_version')),
    sa.ForeignKeyConstraint(['tile_id'], ['tile.tile_id'], name=op.f('fk_prediction_run_tile_id_tile')),
    sa.PrimaryKeyConstraint('run_id', name=op.f('pk_prediction_run')),
    sa.UniqueConstraint('share_token_hash', name=op.f('uq_prediction_run_share_token_hash'))
    )
    with op.batch_alter_table('prediction_run', schema=None) as batch_op:
        batch_op.create_index('prediction_run_expiry_idx', ['expires_at'], unique=False)

    if op.get_bind().dialect.name == 'postgresql':
        op.create_check_constraint('ttl_30d', 'prediction_run',
                                   "expires_at <= created_at + interval '30 days'")
    op.create_table('prediction_cell',
    sa.Column('run_id', sa.String(length=36), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('mut_aa', sa.CHAR(length=1), nullable=False),
    sa.Column('score_raw', sa.Float(), nullable=False),
    sa.Column('prob_calibrated', sa.Float(), nullable=False),
    sa.Column('rank_in_tile', sa.Integer(), nullable=False),
    sa.CheckConstraint('position BETWEEN 1 AND 28', name=op.f('ck_prediction_cell_position_range')),
    sa.CheckConstraint('prob_calibrated BETWEEN 0 AND 1', name=op.f('ck_prediction_cell_prob_range')),
    sa.CheckConstraint('rank_in_tile BETWEEN 1 AND 532', name=op.f('ck_prediction_cell_rank_range')),
    sa.ForeignKeyConstraint(['run_id'], ['prediction_run.run_id'], name=op.f('fk_prediction_cell_run_id_prediction_run'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('run_id', 'position', 'mut_aa', name=op.f('pk_prediction_cell'))
    )


def downgrade() -> None:
    op.drop_table('prediction_cell')
    with op.batch_alter_table('prediction_run', schema=None) as batch_op:
        batch_op.drop_index('prediction_run_expiry_idx')

    op.drop_table('prediction_run')
    op.drop_table('measured_cell')
    with op.batch_alter_table('tile', schema=None) as batch_op:
        batch_op.drop_index('tile_screen_idx', postgresql_where=sa.text('screen_peptide_id IS NOT NULL'), sqlite_where=sa.text('screen_peptide_id IS NOT NULL'))
        batch_op.drop_index('tile_domain_idx')

    op.drop_table('tile')
    with op.batch_alter_table('clinvar_variant', schema=None) as batch_op:
        batch_op.drop_index('clinvar_pos_idx')

    op.drop_table('clinvar_variant')
    with op.batch_alter_table('protein', schema=None) as batch_op:
        batch_op.drop_index('protein_gene_idx')

    op.drop_table('protein')
    op.drop_table('etl_input')
    op.drop_table('usage_daily')
    with op.batch_alter_table('model_version', schema=None) as batch_op:
        batch_op.drop_index('model_default_idx', postgresql_where=sa.text('is_default'), sqlite_where=sa.text('is_default'))

    op.drop_table('model_version')
    op.drop_table('etl_run')
    op.drop_table('data_source')
