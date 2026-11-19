"""index clinvar_variant.clinvar_file_date

Revision ID: 0004
Revises: 0003

NF-07 (17 Nov 2026): `SELECT max(clinvar_file_date)` is evaluated for every saved or job-scored tile and by the ClinVar
overlay; on the real reference (2,338,863 rows) it was a full scan of about 290 ms, which made whole-protein jobs
spend ~324 ms per tile instead of ~47 ms. The index turns it into a lookup. No row changes.
"""
from alembic import op


revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('clinvar_variant', recreate='never') as batch_op:
        batch_op.create_index('clinvar_file_date_idx', ['clinvar_file_date'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('clinvar_variant', recreate='never') as batch_op:
        batch_op.drop_index('clinvar_file_date_idx')
