"""Read and write access to the database. Plain functions over a Session; no request or HTTP types here."""
from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from db.models import ClinvarVariant, DataSource, MeasuredCell, ModelVersion, PredictionCell, PredictionRun, Protein, Tile
from degron_footprint.validation import n_tiles


def source_dict(row: DataSource) -> dict:
    return {
        'source_id': row.source_id, 'name': row.name, 'version': row.version, 'citation': row.citation,
        'url': row.url, 'license_name': row.license_name, 'attribution_text': row.attribution_text,
        'disclaimer_text': row.disclaimer_text, 'redistribution_ok': row.redistribution_ok,
    }


def get_sources(s: Session, ids: list[str]) -> list[dict]:
    """Sources by id, in the order asked; unknown ids are skipped (a deployment may not have loaded them)."""
    rows = {r.source_id: r for r in s.execute(select(DataSource).where(DataSource.source_id.in_(ids))).scalars()}
    return [source_dict(rows[i]) for i in ids if i in rows and rows[i].redistribution_ok]


def servable_sources(s: Session) -> list[dict]:
    rows = s.execute(select(DataSource).where(DataSource.redistribution_ok.is_(True))
                     .order_by(DataSource.source_id)).scalars()
    return [source_dict(r) for r in rows]


# ----------------------------------------------------------------- proteins and tiles
def get_protein(s: Session, acc: str) -> Protein | None:
    return s.get(Protein, acc)


def protein_summary(p: Protein) -> dict:
    return {'uniprot_id': p.uniprot_acc, 'gene_symbol': p.gene_symbol, 'protein_name': p.protein_name,
            'length': p.length, 'n_tiles': n_tiles(p.length)}


def _like_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


def search_proteins(s: Session, query: str, limit: int) -> list[dict]:
    """Gene symbol or accession; exact match first, then prefix; ties by gene then accession."""
    q = query.upper()
    like = _like_escape(q) + '%'
    gene_u = func.upper(Protein.gene_symbol)
    acc_u = func.upper(Protein.uniprot_acc)
    stmt = (select(Protein)
            .where(or_(gene_u.like(like, escape='\\'), acc_u.like(like, escape='\\')))
            .limit(500))
    rows = list(s.execute(stmt).scalars())

    def rank(p: Protein) -> tuple[int, str, str]:
        g = (p.gene_symbol or '').upper()
        a = p.uniprot_acc.upper()
        score = 0 if g == q else 1 if a == q else 2 if g.startswith(q) else 3
        return score, g or '~', a
    rows.sort(key=rank)
    return [protein_summary(p) for p in rows[:limit]]


def get_tile(s: Session, acc: str, tile_index: int) -> Tile | None:
    return s.execute(select(Tile).where(Tile.uniprot_acc == acc, Tile.tile_index == tile_index)).scalar_one_or_none()


def tile_by_id(s: Session, tile_id: int) -> Tile | None:
    return s.get(Tile, tile_id)


def list_tiles(s: Session, acc: str) -> list[Tile]:
    return list(s.execute(select(Tile).where(Tile.uniprot_acc == acc).order_by(Tile.tile_index)).scalars())


def tile_is_training(s: Session, tile_id: int) -> bool:
    return s.execute(select(MeasuredCell.tile_id).where(
        MeasuredCell.tile_id == tile_id, MeasuredCell.in_training_set.is_(True)).limit(1)).first() is not None


def measured_cells(s: Session, tile_id: int) -> list[MeasuredCell]:
    return list(s.execute(select(MeasuredCell).where(MeasuredCell.tile_id == tile_id)
                          .order_by(MeasuredCell.position, MeasuredCell.mut_aa)).scalars())


def clinvar_variants(s: Session, acc: str, start: int, end: int) -> list[ClinvarVariant]:
    return list(s.execute(select(ClinvarVariant).where(
        ClinvarVariant.uniprot_acc == acc, ClinvarVariant.protein_pos.between(start, end))
        .order_by(ClinvarVariant.protein_pos, ClinvarVariant.variation_id)).scalars())


def clinvar_file_date(s: Session) -> date | None:
    return s.execute(select(func.max(ClinvarVariant.clinvar_file_date))).scalar_one_or_none()


# ----------------------------------------------------------------- models
def list_model_rows(s: Session) -> list[ModelVersion]:
    rows = list(s.execute(select(ModelVersion).order_by(ModelVersion.model_id)).scalars())
    rows.sort(key=lambda m: (not m.is_default, m.role, m.model_id))
    return rows


def get_model_row(s: Session, model_id: str) -> ModelVersion | None:
    return s.get(ModelVersion, model_id)


# ----------------------------------------------------------------- shared runs
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_run(s: Session, *, run_id: str, input_kind: str, tile_id: int | None, sequence: str, model_id: str,
               gate_model_id: str | None, domain_status: str, warning_codes: list[str], token_hash: str,
               created_at: datetime, expires_at: datetime, cells: list[dict]) -> None:
    s.add(PredictionRun(run_id=run_id, input_kind=input_kind, tile_id=tile_id, input_sequence=sequence,
                        model_id=model_id, gate_model_id=gate_model_id, domain_status=domain_status,
                        warnings=warning_codes, share_token_hash=token_hash, created_at=created_at,
                        expires_at=expires_at))
    s.flush()
    s.add_all([PredictionCell(run_id=run_id, position=c['position'], mut_aa=c['mut_aa'], score_raw=c['score_dpsi_raw'],
                              prob_calibrated=c['p_dpsi_ge_1_calibrated'], rank_in_tile=c['rank_in_tile'])
               for c in cells])


def get_run(s: Session, run_id: str) -> PredictionRun | None:
    return s.get(PredictionRun, run_id)


def run_cells(s: Session, run_id: str) -> list[PredictionCell]:
    return list(s.execute(select(PredictionCell).where(PredictionCell.run_id == run_id)
                          .order_by(PredictionCell.position, PredictionCell.mut_aa)).scalars())


def delete_run(s: Session, run_id: str) -> None:
    s.execute(delete(PredictionCell).where(PredictionCell.run_id == run_id))
    s.execute(delete(PredictionRun).where(PredictionRun.run_id == run_id))


def purge_expired(s: Session, now: datetime | None = None) -> int:
    """Delete shared runs past their expiry; their cells go with them (NFR-10)."""
    now = now or datetime.now(UTC)
    ids = list(s.execute(select(PredictionRun.run_id).where(PredictionRun.expires_at < now)).scalars())
    for rid in ids:
        delete_run(s, rid)
    return len(ids)


def aware(dt: datetime) -> datetime:
    """SQLite returns naive datetimes; they are stored as UTC."""
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def new_expiry(created: datetime, days: int) -> datetime:
    return created + timedelta(days=days)
