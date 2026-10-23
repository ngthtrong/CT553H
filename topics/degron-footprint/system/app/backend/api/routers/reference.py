"""Read-only reference endpoints: protein search, tiles, measured and ClinVar overlays, models, sources."""
from __future__ import annotations

import re

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from degron_footprint.errors import DomainError
from degron_footprint.provenance import build_provenance, utc_iso
from degron_footprint.sources import CLINVAR_PREFIX, NOT_USED_SOURCES, SRC_ZHANG_GEO, SRC_ZHANG_SAT
from degron_footprint.validation import MODEL_ID_RE, check_accession, n_tiles, tile_bounds

from .. import repository as repo
from ..core import Core
from ..deps import get_core, get_session

router = APIRouter()
QUERY_RE = re.compile(r'^[A-Za-z0-9._\-]+$')
TILE_IN_PATH = re.compile(r'^[0-9]{1,6}$')


def _default_info(core: Core):
    lm = core.registry.default
    if lm is None:
        raise DomainError('SERVICE_UNAVAILABLE', 'No model is available, so provenance cannot be stated.', 503)
    return lm.info


def _protein(s: Session, uniprot_id: str):
    acc = check_accession(uniprot_id)
    prot = repo.get_protein(s, acc)
    if prot is None:
        raise DomainError('UNKNOWN_ACCESSION', 'This accession is not among the reviewed human proteins '
                          'loaded in this service.', 404, 'uniprot_id')
    return prot


def _tile(s: Session, uniprot_id: str, tile_index: str):
    prot = _protein(s, uniprot_id)
    if not TILE_IN_PATH.match(tile_index):
        raise DomainError('INVALID_REQUEST', 'tile_index must be a positive integer.', 422, 'tile_index')
    idx = int(tile_index)
    n_max = n_tiles(prot.length)
    tile = repo.get_tile(s, prot.uniprot_acc, idx) if 1 <= idx <= n_max else None
    if tile is None:
        msg = (f'tile_index must be between 1 and {n_max} for this protein.' if n_max
               else 'This protein is shorter than 28 residues and has no tile.')
        raise DomainError('TILE_OUT_OF_RANGE', msg, 404, 'tile_index')
    return prot, tile


def _tile_info(prot, tile) -> dict:
    return {'uniprot_id': prot.uniprot_acc, 'tile_index': tile.tile_index, 'start_pos': tile.start_pos,
            'end_pos': tile.end_pos, 'sequence': tile.sequence}


@router.get('/v1/proteins', tags=['reference'])
def search_proteins(query: str | None = Query(None), limit: int = Query(10), s: Session = Depends(get_session)):
    if query is None:
        raise DomainError('INVALID_REQUEST', 'The query parameter "query" is required.', 400, 'query')
    if not 2 <= len(query) <= 32 or not QUERY_RE.match(query):
        raise DomainError('INVALID_REQUEST', 'query must have 2 to 32 characters: letters, digits, "." "_" "-".',
                          422, 'query')
    if not 1 <= limit <= 50:
        raise DomainError('INVALID_REQUEST', 'limit must be between 1 and 50.', 422, 'limit')
    return {'items': repo.search_proteins(s, query, limit)}


@router.get('/v1/proteins/{uniprot_id}/tiles', tags=['reference'])
def list_tiles(uniprot_id: str, core: Core = Depends(get_core), s: Session = Depends(get_session)):
    prot = _protein(s, uniprot_id)
    tiles = repo.list_tiles(s, prot.uniprot_acc)
    srcs = repo.get_sources(s, [prot.source_id, SRC_ZHANG_GEO])
    return {
        'protein': repo.protein_summary(prot),
        'tiles': [{'tile_index': t.tile_index, 'start_pos': t.start_pos, 'end_pos': t.end_pos,
                   'sequence': t.sequence, 'scorable': t.scorable, 'domain_status': t.domain_status,
                   'psi_wt_measured': t.psi_wt_measured, 'reads_measured': t.reads_measured} for t in tiles],
        'provenance': build_provenance(_default_info(core), srcs),
    }


@router.get('/v1/proteins/{uniprot_id}/tiles/{tile_index}/measured', tags=['reference'])
def measured(uniprot_id: str, tile_index: str, core: Core = Depends(get_core), s: Session = Depends(get_session)):
    prot, tile = _tile(s, uniprot_id, tile_index)
    cells = repo.measured_cells(s, tile.tile_id)
    return {
        'tile': _tile_info(prot, tile),
        'cells': [{'position': c.position, 'mut_aa': c.mut_aa, 'delta_psi': c.delta_psi,
                   'in_training_set': c.in_training_set} for c in cells],
        'provenance': build_provenance(_default_info(core), repo.get_sources(s, [SRC_ZHANG_SAT])),
    }


@router.get('/v1/proteins/{uniprot_id}/tiles/{tile_index}/clinvar', tags=['reference'])
def clinvar(uniprot_id: str, tile_index: str, core: Core = Depends(get_core), s: Session = Depends(get_session)):
    prot, tile = _tile(s, uniprot_id, tile_index)
    file_date = repo.clinvar_file_date(s)
    cv_sources = [x for x in repo.servable_sources(s) if x['source_id'].startswith(CLINVAR_PREFIX)]
    if file_date is None or not cv_sources:
        raise DomainError('SERVICE_UNAVAILABLE', 'ClinVar data are not loaded in this deployment.', 503)
    start, end = tile_bounds(tile.tile_index)
    variants = repo.clinvar_variants(s, prot.uniprot_acc, start, end)
    return {
        'tile': _tile_info(prot, tile),
        'variants': [{'variation_id': v.variation_id, 'protein_pos': v.protein_pos,
                      'position': v.protein_pos - start + 1, 'ref_aa': v.ref_aa, 'alt_aa': v.alt_aa,
                      'clinsig': v.clinsig, 'review_status': v.review_status,
                      'last_evaluated': v.last_evaluated.isoformat() if v.last_evaluated else None}
                     for v in variants],
        'clinvar_file_date': file_date.isoformat(),
        'provenance': build_provenance(_default_info(core), cv_sources),
    }


@router.get('/v1/models', tags=['models'])
def list_models(s: Session = Depends(get_session)):
    return {'items': [{'model_id': m.model_id, 'role': m.role, 'kind': m.kind, 'status': m.status,
                       'is_default': m.is_default} for m in repo.list_model_rows(s)]}


@router.get('/v1/models/{model_id}', tags=['models'])
def model_card(model_id: str, s: Session = Depends(get_session)):
    m = repo.get_model_row(s, model_id) if MODEL_ID_RE.fullmatch(model_id) else None
    if m is None:
        raise DomainError('MODEL_NOT_FOUND', 'No model has this id. See GET /v1/models.', 404)
    from degron_footprint.provenance import source_ref
    trained = [source_ref(x) for x in repo.get_sources(s, list(m.trained_on_sources or []))]
    metrics = dict(m.metrics or {})
    return {
        'model_id': m.model_id, 'role': m.role, 'kind': m.kind, 'status': m.status, 'is_default': m.is_default,
        'weights_sha256': m.weights_sha256, 'event_definition': m.event_definition,
        'domain_description': m.domain_description, 'evidence_label': m.evidence_label,
        'metrics': metrics, 'metrics_source_file': str(metrics.get('source_file', '')),
        'calibration': m.calibration, 'trained_on_sources': trained, 'card_markdown': m.card_markdown,
        'not_used_sources': [dict(x) for x in NOT_USED_SOURCES],
        'frozen_at': utc_iso(repo.aware(m.frozen_at)) if m.frozen_at else None,
    }


@router.get('/v1/sources', tags=['reference'])
def sources(s: Session = Depends(get_session)):
    keys = ('source_id', 'name', 'version', 'citation', 'url', 'license_name', 'attribution_text', 'disclaimer_text')
    return {'items': [{k: x[k] for k in keys} for x in repo.servable_sources(s)]}
