"""SQLAlchemy 2 tables, one to one with system/db-design.md §4 (reference) and §11 (workspace, migration 0002).
The same revision files serve PostgreSQL and SQLite.

Differences from the DDL, forced by SQLite: UUIDs are text(36), `jsonb` is JSON, `timestamptz` is a timezone-aware
DateTime, and the 30-day expiry CHECK of `prediction_run` (an `interval` expression) is enforced by the application
and added as a PostgreSQL-only constraint in the migration.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    CHAR,
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}
AMINO = "('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')"
# Migration 0003 adds the two borderline states of the R3 gate (DEVIATIONS.md §7); 0001 holds the older list.
DOMAIN_STATUSES = ("('measured_in_domain','measured_out_of_domain','measured_unreliable','measured_borderline',"
                   "'predicted_in_domain','predicted_out_of_domain','predicted_borderline','unknown')")

# bigint primary keys must be INTEGER on SQLite to auto-increment
BigPk = BigInteger().with_variant(Integer(), 'sqlite')


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING)


class DataSource(Base):
    __tablename__ = 'data_source'
    __table_args__ = (
        CheckConstraint("license_class IN ('open','attribution_required','internal_only','unknown')",
                        name='license_class'),
        CheckConstraint("redistribution_ok OR license_class IN ('internal_only','unknown')", name='servable'),
    )
    source_id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(Text)
    citation: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(Text)
    license_name: Mapped[str] = mapped_column(Text)
    license_class: Mapped[str] = mapped_column(Text)
    redistribution_ok: Mapped[bool] = mapped_column(Boolean)
    attribution_text: Mapped[str] = mapped_column(Text)
    disclaimer_text: Mapped[str | None] = mapped_column(Text)
    sha256: Mapped[str | None] = mapped_column(CHAR(64))
    retrieved_on: Mapped[date | None] = mapped_column(Date)


class ModelVersion(Base):
    __tablename__ = 'model_version'
    __table_args__ = (
        CheckConstraint("role IN ('effect','gate')", name='role'),
        CheckConstraint("status IN ('candidate','frozen','retired')", name='status'),
        CheckConstraint("status <> 'frozen' OR frozen_at IS NOT NULL", name='frozen_has_date'),
        CheckConstraint("NOT is_default OR status = 'frozen'", name='default_is_frozen'),
        Index('model_default_idx', 'role', unique=True,
              postgresql_where=text('is_default'), sqlite_where=text('is_default')),
    )
    model_id: Mapped[str] = mapped_column(Text, primary_key=True)
    role: Mapped[str] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'))
    tile_length: Mapped[int] = mapped_column(Integer, default=28, server_default=text('28'))
    feature_spec: Mapped[str] = mapped_column(Text)
    weights_path: Mapped[str] = mapped_column(Text)
    weights_sha256: Mapped[str] = mapped_column(CHAR(64))
    event_definition: Mapped[str] = mapped_column(Text)
    domain_description: Mapped[str] = mapped_column(Text)
    metrics: Mapped[dict] = mapped_column(JSON)
    calibration: Mapped[dict | None] = mapped_column(JSON)
    trained_on_sources: Mapped[list] = mapped_column(JSON)
    evidence_label: Mapped[str] = mapped_column(
        Text, default='development OOF benchmark, not external validation',
        server_default='development OOF benchmark, not external validation')
    card_markdown: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    frozen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Protein(Base):
    __tablename__ = 'protein'
    __table_args__ = (
        CheckConstraint('length > 0', name='length_pos'),
        CheckConstraint('length = length(sequence)', name='length_matches'),
        Index('protein_gene_idx', 'gene_symbol'),
    )
    uniprot_acc: Mapped[str] = mapped_column(Text, primary_key=True)
    gene_symbol: Mapped[str | None] = mapped_column(Text)
    protein_name: Mapped[str | None] = mapped_column(Text)
    length: Mapped[int] = mapped_column(Integer)
    sequence: Mapped[str] = mapped_column(Text)
    uniprot_release: Mapped[str] = mapped_column(Text)
    source_id: Mapped[str] = mapped_column(ForeignKey('data_source.source_id'))


class Tile(Base):
    __tablename__ = 'tile'
    __table_args__ = (
        UniqueConstraint('uniprot_acc', 'tile_index'),
        CheckConstraint('tile_index >= 1', name='index_pos'),
        CheckConstraint('start_pos = (tile_index - 1) * 23 + 1', name='start_formula'),
        CheckConstraint('end_pos = start_pos + 27', name='end_formula'),
        CheckConstraint('length(sequence) = 28', name='len28'),
        CheckConstraint('reads_measured IS NULL OR reads_measured >= 0', name='reads_nonneg'),
        CheckConstraint(f'domain_status IN {DOMAIN_STATUSES}', name='domain_status'),
        CheckConstraint("domain_status NOT LIKE 'measured_%' OR psi_wt_measured IS NOT NULL "
                        "OR domain_status = 'measured_unreliable'", name='measured_backed'),
        CheckConstraint("domain_status NOT LIKE 'predicted_%' OR "
                        '(psi_wt_predicted IS NOT NULL AND psi_wt_predicted_by IS NOT NULL)', name='predicted_backed'),
        CheckConstraint("scorable OR domain_status = 'unknown'", name='scorable_or_unknown'),
        Index('tile_screen_idx', 'screen_peptide_id',
              postgresql_where=text('screen_peptide_id IS NOT NULL'),
              sqlite_where=text('screen_peptide_id IS NOT NULL')),
        Index('tile_domain_idx', 'uniprot_acc', 'domain_status'),
    )
    tile_id: Mapped[int] = mapped_column(BigPk, primary_key=True, autoincrement=True)
    uniprot_acc: Mapped[str] = mapped_column(ForeignKey('protein.uniprot_acc', ondelete='CASCADE'))
    tile_index: Mapped[int] = mapped_column(Integer)
    start_pos: Mapped[int] = mapped_column(Integer)
    end_pos: Mapped[int] = mapped_column(Integer)
    sequence: Mapped[str] = mapped_column(CHAR(28))
    scorable: Mapped[bool] = mapped_column(Boolean)
    screen_peptide_id: Mapped[str | None] = mapped_column(Text)
    psi_wt_measured: Mapped[float | None] = mapped_column(Float)
    reads_measured: Mapped[float | None] = mapped_column(Float)
    psi_wt_predicted: Mapped[float | None] = mapped_column(Float)
    psi_wt_predicted_by: Mapped[str | None] = mapped_column(ForeignKey('model_version.model_id'))
    domain_status: Mapped[str] = mapped_column(Text, default='unknown', server_default='unknown')
    source_id: Mapped[str] = mapped_column(ForeignKey('data_source.source_id'))


class MeasuredCell(Base):
    __tablename__ = 'measured_cell'
    __table_args__ = (
        CheckConstraint('position BETWEEN 1 AND 28', name='position_range'),
        CheckConstraint(f'mut_aa IN {AMINO}', name='mut_aa'),
    )
    tile_id: Mapped[int] = mapped_column(ForeignKey('tile.tile_id', ondelete='CASCADE'), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    mut_aa: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    delta_psi: Mapped[float] = mapped_column(Float)
    in_training_set: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text('true'))
    source_id: Mapped[str] = mapped_column(ForeignKey('data_source.source_id'))


class ClinvarVariant(Base):
    __tablename__ = 'clinvar_variant'
    __table_args__ = (
        CheckConstraint('protein_pos >= 1', name='pos_pos'),
        CheckConstraint('ref_aa <> alt_aa', name='ref_ne_alt'),
        CheckConstraint("clinsig IN ('pathogenic','likely_pathogenic','vus','likely_benign','benign',"
                        "'conflicting','other')", name='clinsig'),
        Index('clinvar_pos_idx', 'uniprot_acc', 'protein_pos'),
    )
    variation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    uniprot_acc: Mapped[str] = mapped_column(ForeignKey('protein.uniprot_acc', ondelete='CASCADE'))
    protein_pos: Mapped[int] = mapped_column(Integer)
    ref_aa: Mapped[str] = mapped_column(CHAR(1))
    alt_aa: Mapped[str] = mapped_column(CHAR(1))
    clinsig: Mapped[str] = mapped_column(Text)
    review_status: Mapped[str | None] = mapped_column(Text)
    last_evaluated: Mapped[date | None] = mapped_column(Date)
    clinvar_file_date: Mapped[date] = mapped_column(Date)
    source_id: Mapped[str] = mapped_column(ForeignKey('data_source.source_id'))


class PredictionRun(Base):
    __tablename__ = 'prediction_run'
    __table_args__ = (
        CheckConstraint("input_kind IN ('sequence','uniprot_tile')", name='input_kind'),
        CheckConstraint('expires_at > created_at', name='expiry_after_creation'),
        CheckConstraint('length(input_sequence) = 28', name='len28'),
        Index('prediction_run_expiry_idx', 'expires_at'),
    )
    run_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    input_kind: Mapped[str] = mapped_column(Text)
    tile_id: Mapped[int | None] = mapped_column(ForeignKey('tile.tile_id'))
    input_sequence: Mapped[str] = mapped_column(CHAR(28))
    model_id: Mapped[str] = mapped_column(ForeignKey('model_version.model_id'))
    gate_model_id: Mapped[str | None] = mapped_column(ForeignKey('model_version.model_id'))
    domain_status: Mapped[str] = mapped_column(Text)
    warnings: Mapped[list] = mapped_column(JSON, default=list)
    share_token_hash: Mapped[str] = mapped_column(CHAR(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class PredictionCell(Base):
    __tablename__ = 'prediction_cell'
    __table_args__ = (
        CheckConstraint('position BETWEEN 1 AND 28', name='position_range'),
        CheckConstraint('prob_calibrated BETWEEN 0 AND 1', name='prob_range'),
        CheckConstraint('rank_in_tile BETWEEN 1 AND 532', name='rank_range'),
    )
    run_id: Mapped[str] = mapped_column(ForeignKey('prediction_run.run_id', ondelete='CASCADE'), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    mut_aa: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    score_raw: Mapped[float] = mapped_column(Float)
    prob_calibrated: Mapped[float] = mapped_column(Float)
    rank_in_tile: Mapped[int] = mapped_column(Integer)


class UsageDaily(Base):
    __tablename__ = 'usage_daily'
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    endpoint: Mapped[str] = mapped_column(Text, primary_key=True)
    model_id: Mapped[str] = mapped_column(Text, primary_key=True, default='', server_default='')
    n_requests: Mapped[int] = mapped_column(Integer, default=0, server_default=text('0'))
    n_errors: Mapped[int] = mapped_column(Integer, default=0, server_default=text('0'))


class EtlRun(Base):
    __tablename__ = 'etl_run'
    __table_args__ = (CheckConstraint("status IN ('running','succeeded','failed')", name='status'),)
    etl_run_id: Mapped[int] = mapped_column(BigPk, primary_key=True, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    git_commit: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    report: Mapped[dict] = mapped_column(JSON, default=dict)


class EtlInput(Base):
    __tablename__ = 'etl_input'
    etl_run_id: Mapped[int] = mapped_column(ForeignKey('etl_run.etl_run_id', ondelete='CASCADE'), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey('data_source.source_id'), primary_key=True)
    file_path: Mapped[str] = mapped_column(Text, primary_key=True)
    sha256_expected: Mapped[str] = mapped_column(CHAR(64))
    sha256_actual: Mapped[str] = mapped_column(CHAR(64))


# ---------------------------------------------------------------------------------------------------------------
# Workspace tables (db-design.md §11, migration 0002). Project-owned; they never reference the mutable reference rows
# (`tile`, `clinvar_variant`) by key, so replacing a reference load cannot change a saved result (A-6). Composite
# foreign keys on (project_id, …) stop a run, job, dataset or comparison from pointing into another project.
# ---------------------------------------------------------------------------------------------------------------

JOB_STATES = "('pending','running','completed','partial','failed','cancelled')"
ITEM_STATES = "('pending','running','succeeded','refused','failed','cancelled')"
Uuid = String(36)


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = (
        CheckConstraint('length(name) BETWEEN 1 AND 200', name='name_length'),
        CheckConstraint("deletion_state IN ('active','deleting')", name='deletion_state'),
        Index('project_updated_idx', 'updated_at', 'project_id'),
    )
    project_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, default='', server_default='')
    deletion_state: Mapped[str] = mapped_column(Text, default='active', server_default='active')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AnalysisJob(Base):
    __tablename__ = 'analysis_job'
    __table_args__ = (
        UniqueConstraint('project_id', 'job_id', name='uq_analysis_job_project_job'),
        CheckConstraint("mode IN ('peptides','protein')", name='mode'),
        CheckConstraint(f'state IN {JOB_STATES}', name='state'),
        CheckConstraint('total >= 0', name='total_nonneg'),
        Index('analysis_job_state_idx', 'state', 'created_at'),
        Index('analysis_job_project_idx', 'project_id', 'created_at', 'job_id'),
    )
    job_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey('project.project_id', ondelete='CASCADE'))
    mode: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(Text, default='pending', server_default='pending')
    total: Mapped[int] = mapped_column(Integer)
    # Frozen at submission (FR-27): never rewritten afterwards.
    input_snapshot: Mapped[dict] = mapped_column(JSON)
    configuration_snapshot: Mapped[dict] = mapped_column(JSON)
    coverage: Mapped[dict | None] = mapped_column(JSON)
    model_id: Mapped[str] = mapped_column(ForeignKey('model_version.model_id'))
    model_sha256: Mapped[str] = mapped_column(CHAR(64))
    calibrator: Mapped[str] = mapped_column(Text)
    gate_model_id: Mapped[str | None] = mapped_column(ForeignKey('model_version.model_id'))
    gate_sha256: Mapped[str | None] = mapped_column(CHAR(64))
    cancel_requested: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class JobItem(Base):
    __tablename__ = 'job_item'
    __table_args__ = (
        UniqueConstraint('job_id', 'ordinal', name='uq_job_item_job_ordinal'),
        CheckConstraint(f'state IN {ITEM_STATES}', name='state'),
        CheckConstraint('ordinal >= 1', name='ordinal_pos'),
        CheckConstraint('attempts >= 0', name='attempts_nonneg'),
        CheckConstraint("state <> 'running' OR (lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL)",
                        name='running_has_lease'),
        CheckConstraint('tile_index IS NULL OR (tile_index >= 1 AND start_pos = (tile_index - 1) * 23 + 1 '
                        'AND end_pos = start_pos + 27)', name='tile_formula'),
        CheckConstraint(f'domain_status IS NULL OR domain_status IN {DOMAIN_STATUSES}', name='domain_status'),
        Index('job_item_state_idx', 'job_id', 'state'),
        Index('job_item_lease_idx', 'lease_expires_at'),
    )
    job_id: Mapped[str] = mapped_column(ForeignKey('analysis_job.job_id', ondelete='CASCADE'), primary_key=True)
    item_id: Mapped[str] = mapped_column(Text, primary_key=True)
    ordinal: Mapped[int] = mapped_column(Integer)                 # stable manifest order and pagination key
    input_id: Mapped[str] = mapped_column(Text)
    sequence: Mapped[str | None] = mapped_column(Text)            # normalised peptide; NULL when the input was refused
    uniprot_acc: Mapped[str | None] = mapped_column(Text)         # verified mapping only (no FK: reference is mutable)
    reference_release: Mapped[str | None] = mapped_column(Text)
    tile_index: Mapped[int | None] = mapped_column(Integer)
    start_pos: Mapped[int | None] = mapped_column(Integer)
    end_pos: Mapped[int | None] = mapped_column(Integer)
    state: Mapped[str] = mapped_column(Text, default='pending', server_default='pending')
    domain_status: Mapped[str | None] = mapped_column(Text)
    error: Mapped[dict | None] = mapped_column(JSON)
    lease_owner: Mapped[str | None] = mapped_column(Text)
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=0, server_default=text('0'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AnalysisRun(Base):
    """A saved analysis. Immutable: the repository has no update path; "Run again" inserts a new row (A-5)."""
    __tablename__ = 'analysis_run'
    __table_args__ = (
        UniqueConstraint('project_id', 'analysis_id', name='uq_analysis_run_project_analysis'),
        UniqueConstraint('job_id', 'item_id', name='uq_analysis_run_job_item'),
        ForeignKeyConstraint(['project_id', 'job_id'], ['analysis_job.project_id', 'analysis_job.job_id'],
                             name='fk_analysis_run_project_job', ondelete='CASCADE'),
        ForeignKeyConstraint(['job_id', 'item_id'], ['job_item.job_id', 'job_item.item_id'],
                             name='fk_analysis_run_job_item', ondelete='CASCADE'),
        CheckConstraint('(job_id IS NULL) = (item_id IS NULL)', name='job_item_pair'),
        CheckConstraint("input_kind IN ('sequence','uniprot_tile')", name='input_kind'),
        CheckConstraint('length(input_sequence) = 28', name='len28'),
        CheckConstraint(f'domain_status IN {DOMAIN_STATUSES}', name='domain_status'),
        CheckConstraint('snapshot_version >= 1', name='snapshot_version_pos'),
        Index('analysis_run_project_idx', 'project_id', 'created_at', 'analysis_id'),
    )
    analysis_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey('project.project_id', ondelete='CASCADE'))
    job_id: Mapped[str | None] = mapped_column(Uuid)
    item_id: Mapped[str | None] = mapped_column(Text)
    # Lineage pointer only (no FK): deleting a parent must not rewrite an immutable child; the API reports a missing
    # parent explicitly instead.
    parent_analysis_id: Mapped[str | None] = mapped_column(Uuid)
    model_id: Mapped[str] = mapped_column(ForeignKey('model_version.model_id'))
    input_kind: Mapped[str] = mapped_column(Text)
    input_sequence: Mapped[str] = mapped_column(CHAR(28))
    uniprot_acc: Mapped[str | None] = mapped_column(Text)
    tile_index: Mapped[int | None] = mapped_column(Integer)
    domain_status: Mapped[str] = mapped_column(Text)
    snapshot_version: Mapped[int] = mapped_column(Integer, default=1, server_default=text('1'))
    result: Mapped[dict] = mapped_column(JSON)                    # the PredictionResult as returned at run time
    provenance: Mapped[dict] = mapped_column(JSON)                # model/calibrator/gate ids + hashes, code, config
    annotation_snapshot: Mapped[dict] = mapped_column(JSON)       # ClinVar/UniProt/GPS data and source revisions
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AnalysisCell(Base):
    __tablename__ = 'analysis_cell'
    __table_args__ = (
        CheckConstraint('position BETWEEN 1 AND 28', name='position_range'),
        CheckConstraint(f'mut_aa IN {AMINO}', name='mut_aa'),
        CheckConstraint(f'wt_aa IN {AMINO}', name='wt_aa'),
        CheckConstraint('mut_aa <> wt_aa', name='mut_ne_wt'),
        CheckConstraint('prob_calibrated BETWEEN 0 AND 1', name='prob_range'),
        CheckConstraint('rank_in_tile BETWEEN 1 AND 532', name='rank_range'),
    )
    analysis_id: Mapped[str] = mapped_column(ForeignKey('analysis_run.analysis_id', ondelete='CASCADE'),
                                             primary_key=True)
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    mut_aa: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    wt_aa: Mapped[str] = mapped_column(CHAR(1))
    score_raw: Mapped[float] = mapped_column(Float)
    prob_calibrated: Mapped[float] = mapped_column(Float)
    rank_in_tile: Mapped[int] = mapped_column(Integer)
    top10: Mapped[bool] = mapped_column(Boolean)


class ImportDataset(Base):
    """One revision of an uploaded observation file. Immutable after commit; a new file is a new revision."""
    __tablename__ = 'import_dataset'
    __table_args__ = (
        UniqueConstraint('project_id', 'dataset_id', name='uq_import_dataset_project_dataset'),
        UniqueConstraint('project_id', 'name', 'revision', name='uq_import_dataset_revision'),
        CheckConstraint("state IN ('staged','committed','expired')", name='state'),
        CheckConstraint('revision >= 1', name='revision_pos'),
        CheckConstraint("compatibility IN ('zhang_gps_dpsi','other')", name='compatibility'),
        CheckConstraint("state <> 'committed' OR committed_at IS NOT NULL", name='committed_has_date'),
        CheckConstraint("state <> 'staged' OR expires_at IS NOT NULL", name='staged_expires'),
        CheckConstraint('length(name) BETWEEN 1 AND 200', name='name_length'),
        Index('import_dataset_project_idx', 'project_id', 'state'),
    )
    dataset_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey('project.project_id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(Text)                       # sanitised display name, never a path
    revision: Mapped[int] = mapped_column(Integer)
    state: Mapped[str] = mapped_column(Text, default='staged', server_default='staged')
    file_path: Mapped[str] = mapped_column(Text)                  # generated, relative to the workspace root
    sha256: Mapped[str] = mapped_column(CHAR(64))
    assay: Mapped[str] = mapped_column(Text)
    assay_version: Mapped[str | None] = mapped_column(Text)
    endpoint: Mapped[str] = mapped_column(Text)
    units: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(Text)
    reference_description: Mapped[str] = mapped_column(Text)
    compatibility: Mapped[str] = mapped_column(Text)
    rights_note: Mapped[str | None] = mapped_column(Text)
    committable: Mapped[bool] = mapped_column(Boolean)
    counts: Mapped[dict] = mapped_column(JSON)
    validation_report: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    committed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ImportObservation(Base):
    __tablename__ = 'import_observation'
    __table_args__ = (
        UniqueConstraint('dataset_id', 'wt_sequence', 'position', 'mut_aa', 'replicate_id',
                         name='uq_import_observation_key'),
        CheckConstraint('row_number >= 1', name='row_pos'),
        CheckConstraint('length(wt_sequence) = 28', name='len28'),
        CheckConstraint('position BETWEEN 1 AND 28', name='position_range'),
        CheckConstraint(f'mut_aa IN {AMINO}', name='mut_aa'),
        CheckConstraint(f'wt_aa IN {AMINO}', name='wt_aa'),
        CheckConstraint('mut_aa <> wt_aa', name='mut_ne_wt'),
        CheckConstraint('length(replicate_id) >= 1', name='replicate_present'),
        # A value or an explicit reason, never a silent zero (api-spec §6).
        CheckConstraint('(observed_value IS NULL) <> (missing_reason IS NULL)', name='value_or_reason'),
        CheckConstraint('start_pos IS NULL OR start_pos >= 1', name='start_pos'),
    )
    observation_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    dataset_id: Mapped[str] = mapped_column(ForeignKey('import_dataset.dataset_id', ondelete='CASCADE'))
    row_number: Mapped[int] = mapped_column(Integer)
    peptide_id: Mapped[str] = mapped_column(Text)
    wt_sequence: Mapped[str] = mapped_column(CHAR(28))
    position: Mapped[int] = mapped_column(Integer)
    wt_aa: Mapped[str] = mapped_column(CHAR(1))
    mut_aa: Mapped[str] = mapped_column(CHAR(1))
    replicate_id: Mapped[str] = mapped_column(Text)
    observed_value: Mapped[float | None] = mapped_column(Float)
    missing_reason: Mapped[str | None] = mapped_column(Text)
    uniprot_acc: Mapped[str | None] = mapped_column(Text)
    reference_release: Mapped[str | None] = mapped_column(Text)
    start_pos: Mapped[int | None] = mapped_column(Integer)


class Comparison(Base):
    __tablename__ = 'comparison'
    __table_args__ = (
        ForeignKeyConstraint(['project_id', 'analysis_id'], ['analysis_run.project_id', 'analysis_run.analysis_id'],
                             name='fk_comparison_project_analysis', ondelete='CASCADE'),
        ForeignKeyConstraint(['project_id', 'dataset_id'], ['import_dataset.project_id', 'import_dataset.dataset_id'],
                             name='fk_comparison_project_dataset', ondelete='CASCADE'),
        CheckConstraint('(replicate_id IS NULL) <> (aggregation IS NULL)', name='replicate_or_aggregation'),
        CheckConstraint("aggregation IS NULL OR aggregation IN ('mean','median')", name='aggregation'),
        CheckConstraint('matched >= 0', name='matched_nonneg'),
        Index('comparison_analysis_idx', 'analysis_id', 'created_at', 'comparison_id'),
        Index('comparison_dataset_idx', 'dataset_id'),
    )
    comparison_id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey('project.project_id', ondelete='CASCADE'))
    analysis_id: Mapped[str] = mapped_column(Uuid)
    dataset_id: Mapped[str] = mapped_column(Uuid)
    replicate_id: Mapped[str | None] = mapped_column(Text)
    aggregation: Mapped[str | None] = mapped_column(Text)
    compatible: Mapped[bool] = mapped_column(Boolean)
    matched: Mapped[int] = mapped_column(Integer)
    counts: Mapped[dict] = mapped_column(JSON)
    mae: Mapped[float | None] = mapped_column(Float)
    spearman: Mapped[float | None] = mapped_column(Float)
    metric_unavailable_reason: Mapped[str | None] = mapped_column(Text)
    rows: Mapped[list] = mapped_column(JSON)
    provenance: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
