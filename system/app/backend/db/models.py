"""SQLAlchemy 2 tables, one to one with system/db-design.md §4. The same revision files serve PostgreSQL and SQLite.

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
DOMAIN_STATUSES = ("('measured_in_domain','measured_out_of_domain','measured_unreliable',"
                   "'predicted_in_domain','predicted_out_of_domain','unknown')")

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
