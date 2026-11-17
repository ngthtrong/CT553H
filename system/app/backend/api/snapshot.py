"""Frozen snapshots of a saved analysis (api-spec §4, db-design §11, implementation plan A-5/A-6).

A snapshot is built once, when the analysis is saved or a job item finishes, from the prediction outcome and the
reference rows of that moment. Reopening history reads it back; nothing here is ever recomputed from current tables.
"""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from degron_footprint.provenance import utc_iso
from degron_footprint.sources import CLINVAR_PREFIX
from degron_footprint.validation import tile_bounds

from . import repository as repo
from .requests import PredictRequest
from .service import LoadedModel, Outcome

SNAPSHOT_VERSION = 1

ANNOTATION_STATES = ('available', 'no_match', 'mapping_unavailable', 'source_unavailable', 'mapping_conflict')


def clinvar_annotation(s: Session, tile: dict) -> dict[str, Any]:
    """ClinVar for one tile, with the four "nothing to show" cases kept apart (FR-18, FR-35, ANN-01).

    * mapping_unavailable — typed sequence: no verified accession, so ClinVar is not looked up (never "no variants").
    * source_unavailable — ClinVar is not loaded in this database.
    * mapping_conflict — a variant's reference residue differs from the tile residue at that position.
    * no_match — ClinVar is loaded and the tile has no missense variant. Absence is not evidence of benignity.
    """
    if not tile.get('uniprot_id') or not tile.get('tile_index'):
        return {'state': 'mapping_unavailable', 'variants': [],
                'reason': 'Typed sequence: no verified UniProt mapping, so ClinVar was not looked up.'}
    file_date = repo.clinvar_file_date(s)
    sources = [x for x in repo.servable_sources(s) if x['source_id'].startswith(CLINVAR_PREFIX)]
    if file_date is None or not sources:
        return {'state': 'source_unavailable', 'variants': [], 'reason': 'ClinVar is not loaded in this database.'}
    start, end = tile_bounds(int(tile['tile_index']))
    seq = tile['sequence']
    variants, conflicts = [], 0
    for v in repo.clinvar_variants(s, tile['uniprot_id'], start, end):
        pos = v.protein_pos - start + 1
        matches = 1 <= pos <= len(seq) and seq[pos - 1] == v.ref_aa
        conflicts += not matches
        variants.append({'variation_id': v.variation_id, 'protein_pos': v.protein_pos, 'position': pos,
                         'ref_aa': v.ref_aa, 'alt_aa': v.alt_aa, 'clinsig': v.clinsig,
                         'review_status': v.review_status, 'residue_matches': matches,
                         'last_evaluated': v.last_evaluated.isoformat() if v.last_evaluated else None})
    state = 'mapping_conflict' if conflicts else ('available' if variants else 'no_match')
    return {'state': state, 'variants': variants, 'conflicts': conflicts, 'clinvar_file_date': file_date.isoformat(),
            'sources': [{k: x[k] for k in ('source_id', 'version', 'attribution_text', 'disclaimer_text')}
                        for x in sources]}


def measured_annotation(s: Session, tile_id: int | None) -> dict[str, Any]:
    if tile_id is None:
        return {'state': 'mapping_unavailable', 'cells': []}
    cells = repo.measured_cells(s, tile_id)
    return {'state': 'available' if cells else 'no_match',
            'cells': [{'position': c.position, 'mut_aa': c.mut_aa, 'delta_psi': c.delta_psi,
                       'in_training_set': c.in_training_set} for c in cells]}


def reference_snapshot(s: Session, tile: dict) -> dict[str, Any]:
    if not tile.get('uniprot_id'):
        return {'uniprot_id': None, 'uniprot_release': None, 'protein_sequence_sha256': None}
    prot = repo.get_protein(s, tile['uniprot_id'])
    if prot is None:                                     # cannot happen right after a successful prediction
        return {'uniprot_id': tile['uniprot_id'], 'uniprot_release': None, 'protein_sequence_sha256': None}
    return {'uniprot_id': prot.uniprot_acc, 'uniprot_release': prot.uniprot_release, 'protein_length': prot.length,
            'protein_sequence_sha256': hashlib.sha256(prot.sequence.encode()).hexdigest()}


def build(s: Session | None, outcome: Outcome, req: PredictRequest, lm: LoadedModel, gate_model_id: str | None,
          created: datetime) -> tuple[dict, dict, dict]:
    """(result, provenance, annotation snapshot) for a new analysis_run row."""
    result = outcome.result
    tile = result['tile']
    calibrator = req.calibrator or getattr(lm.adapter, 'default_calibrator', None)
    provenance = {
        'snapshot_version': SNAPSHOT_VERSION,
        'request': {'input_kind': outcome.input_kind, 'sequence': outcome.sequence,
                    'uniprot_id': tile.get('uniprot_id'), 'tile_index': tile.get('tile_index'),
                    'model_id': req.model_id, 'calibrator': req.calibrator, 'override_domain': req.override_domain},
        'model': {'model_id': lm.info.model_id, 'kind': lm.info.kind, 'weights_sha256': lm.info.weights_sha256,
                  'calibrator': calibrator},
        'gate': {'gate_model_id': outcome.gate_model_id or gate_model_id},
        'domain': result['domain'],
        'warning_codes': outcome.warning_codes,
        'code_version': result['provenance']['code_version'],
        'created_at': utc_iso(created),
    }
    if s is None:
        annotations: dict[str, Any] = {
            'clinvar': clinvar_annotation_typed(), 'measured': {'state': 'mapping_unavailable', 'cells': []},
            'reference': {'uniprot_id': None, 'uniprot_release': None, 'protein_sequence_sha256': None}}
    else:
        annotations = {'clinvar': clinvar_annotation(s, tile), 'measured': measured_annotation(s, outcome.tile_id),
                       'reference': reference_snapshot(s, tile)}
    return result, provenance, annotations


def clinvar_annotation_typed() -> dict[str, Any]:
    return {'state': 'mapping_unavailable', 'variants': [],
            'reason': 'Typed sequence: no verified UniProt mapping, so ClinVar was not looked up.'}


def response_snapshot(provenance: dict, annotations: dict) -> dict:
    """The `snapshot` object of SavedAnalysis: provenance plus the annotations saved with it."""
    return {**provenance, 'annotations': annotations}
