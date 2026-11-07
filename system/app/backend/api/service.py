"""Orchestration: model registry, domain gate, one prediction, and rebuilding a stored run."""
from __future__ import annotations

import logging
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from db.models import DataSource, ModelVersion, PredictionRun, Tile
from degron_footprint.domain import GateAdapter, NullGate, status_from_measurement
from degron_footprint.errors import DomainError
from degron_footprint.model import LOADERS, ModelAdapter, WeightsError
from degron_footprint.prediction import build_domain, build_result, warnings_for
from degron_footprint.provenance import ModelInfo
from degron_footprint.sources import SRC_ZHANG_GEO
from degron_footprint.validation import (
    check_accession,
    check_tile_index,
    is_scorable,
    n_tiles,
    normalize_sequence,
    tile_bounds,
    tile_sequence,
)

from . import repository as repo
from .requests import PredictRequest, valid_model_id

log = logging.getLogger('api.service')


@dataclass
class LoadedModel:
    info: ModelInfo
    adapter: ModelAdapter
    is_default: bool


@dataclass
class Registry:
    models: dict[str, LoadedModel] = field(default_factory=dict)
    default_id: str | None = None
    errors: dict[str, str] = field(default_factory=dict)       # model_id -> why it is not serving
    database_ok: bool = True

    @property
    def default(self) -> LoadedModel | None:
        return self.models.get(self.default_id) if self.default_id else None


def load_registry(factory: sessionmaker[Session], model_dir: Path) -> Registry:
    """Load every frozen effect model whose weights hash matches the registry. A mismatch does not abort the
    process: the model is left out and /healthz reports 503 (NFR-06)."""
    reg = Registry()
    try:
        with factory() as s:
            rows = list(s.execute(select(ModelVersion).where(
                ModelVersion.role == 'effect', ModelVersion.status == 'frozen')).scalars())
            for row in rows:
                try:
                    loader = LOADERS[row.kind]
                except KeyError:
                    reg.errors[row.model_id] = f'no loader for kind {row.kind}'
                    continue
                try:
                    adapter = loader(row.model_id, model_dir / Path(row.weights_path).name, row.weights_sha256)
                except WeightsError as exc:
                    reg.errors[row.model_id] = str(exc)
                    log.error('model %s not loaded: %s', row.model_id, exc)
                    continue
                src_ids = list(row.trained_on_sources or [])
                sources = repo.get_sources(s, src_ids) if src_ids else []
                info = ModelInfo(
                    model_id=row.model_id, kind=row.kind, weights_sha256=row.weights_sha256,
                    feature_spec=row.feature_spec, event_definition=row.event_definition,
                    evidence_label=row.evidence_label, domain_description=row.domain_description,
                    trained_on_sources=tuple(sources))
                reg.models[row.model_id] = LoadedModel(info, adapter, row.is_default)
                if row.is_default:
                    reg.default_id = row.model_id
    except Exception as exc:                                                 # database down at start-up
        reg.database_ok = False
        log.error('registry not loaded: %s', type(exc).__name__)
    if reg.default_id is None and reg.models and reg.database_ok:
        reg.default_id = sorted(reg.models)[0]
    return reg


@dataclass
class Outcome:
    result: dict
    tile_id: int | None
    input_kind: str
    sequence: str
    model_id: str
    gate_model_id: str | None
    status: str
    warning_codes: list[str]
    generated_at: datetime


class Predictor:
    def __init__(self, registry: Registry, gate: GateAdapter | None, factory: sessionmaker[Session]):
        self.registry = registry
        self.gate = gate or NullGate()
        self.factory = factory

    # ------------------------------------------------------------------ model choice
    def pick_model(self, model_id: str | None) -> LoadedModel:
        if model_id is not None:
            lm = self.registry.models.get(model_id) if valid_model_id(model_id) else None
            if lm is None:
                raise DomainError('MODEL_NOT_FOUND', 'No frozen effect model has this id. See GET /v1/models.',
                                  404, 'model_id')
            return lm
        lm = self.registry.default
        if lm is None:
            raise DomainError('SERVICE_UNAVAILABLE',
                              'No model is available: the weights are missing or do not match the registry.', 503)
        return lm

    # ------------------------------------------------------------------ one prediction
    def predict(self, req: PredictRequest, s: Session | None) -> Outcome:
        """Validation order of api-spec.md §3 steps 4-8, then the score. `s` may be None only for typed sequences."""
        tile_row: Tile | None = None
        if req.sequence is not None:
            seq = normalize_sequence(req.sequence)
            tile: dict[str, Any] = {'uniprot_id': None, 'tile_index': None, 'start_pos': None, 'end_pos': None, 'sequence': seq}
            status, psi, reads, gate_id = 'unknown', None, None, None
            training = False
            extra_sources: list[str] = []
            input_kind = 'sequence'
        else:
            acc = check_accession(req.uniprot_id)
            if s is None:
                raise DomainError('SERVICE_UNAVAILABLE', 'The database is unavailable.', 503)
            prot = repo.get_protein(s, acc)
            if prot is None:
                raise DomainError('UNKNOWN_ACCESSION', 'This accession is not among the reviewed human proteins '
                                  'loaded in this service.', 404, 'uniprot_id')
            n_max = n_tiles(prot.length)
            idx = check_tile_index(req.tile_index, n_max)
            tile_row = repo.get_tile(s, acc, idx)
            seq = tile_row.sequence if tile_row else (tile_sequence(prot.sequence, idx) or '')
            if not is_scorable(seq):
                raise DomainError('TILE_NOT_SCORABLE',
                                  'This tile contains a residue that is not one of the 20 standard amino acids and '
                                  'cannot be scored.', 422, 'tile_index')
            start, end = tile_bounds(idx)
            tile = {'uniprot_id': acc, 'tile_index': idx, 'start_pos': start, 'end_pos': end, 'sequence': seq}
            status = tile_row.domain_status if tile_row else 'unknown'
            psi = tile_row.psi_wt_measured if tile_row else None
            reads = tile_row.reads_measured if tile_row else None
            gate_id = tile_row.psi_wt_predicted_by if tile_row else None
            training = tile_row is not None and repo.tile_is_training(s, tile_row.tile_id)
            extra_sources = [prot.source_id]
            input_kind = 'uniprot_tile'
        lm = self.pick_model(req.model_id)
        if status == 'unknown':
            a = self.gate.assess(seq)
            if a is not None:
                status, psi, gate_id = a.status, a.psi_wt_predicted, a.gate_model_id
        overridden = False
        if status in ('measured_out_of_domain', 'predicted_out_of_domain'):
            if not req.override_domain:
                what = 'measured' if status.startswith('measured') else 'predicted'
                val = f' ({psi:.1f})' if psi is not None else ''
                raise DomainError(
                    'OUT_OF_DOMAIN',
                    f'The {what} wild-type PSI of this tile{val} is above the 4.0 limit of the training domain. '
                    'Set override_domain to true to score it anyway.', 422)
            overridden = True
        if status.startswith('measured_'):
            extra_sources.append(SRC_ZHANG_GEO)
        pred = lm.adapter.predict_tile(seq, req.calibrator)
        domain = build_domain(status, psi, reads, gate_id)
        warnings = warnings_for(status, overridden, training)
        now = datetime.now(UTC).replace(microsecond=0)
        src = repo.get_sources(s, extra_sources) if (s is not None and extra_sources) else []
        result = build_result(lm.info, pred, tile, domain, warnings, src, now)
        return Outcome(result, tile_row.tile_id if tile_row else None, input_kind, seq, lm.info.model_id,
                       gate_id, status, [w['code'] for w in warnings], now)

    # ------------------------------------------------------------------ shared runs
    def store_run(self, s: Session, outcome: Outcome, ttl_days: int) -> tuple[str, str, datetime]:
        run_id = str(uuid.uuid4())
        token = secrets.token_urlsafe(16)                      # 128 bits, 22 characters
        created = outcome.generated_at
        expires = repo.new_expiry(created, ttl_days)
        repo.create_run(s, run_id=run_id, input_kind=outcome.input_kind, tile_id=outcome.tile_id,
                        sequence=outcome.sequence, model_id=outcome.model_id, gate_model_id=outcome.gate_model_id,
                        domain_status=outcome.status, warning_codes=outcome.warning_codes,
                        token_hash=repo.hash_token(token), created_at=created, expires_at=expires,
                        cells=outcome.result['cells'])
        return run_id, token, expires

    def rebuild_run(self, s: Session, run: PredictionRun) -> dict:
        """The stored result, identical to the one returned when it was created."""
        import numpy as np

        from degron_footprint.model import TilePrediction
        from degron_footprint.prediction import warning

        lm = self.registry.models.get(run.model_id)
        if lm is None:
            raise DomainError('SERVICE_UNAVAILABLE', 'The model of this run is not serving.', 503)
        cells = repo.run_cells(s, run.run_id)
        seq = run.input_sequence
        tile_row = repo.tile_by_id(s, run.tile_id) if run.tile_id else None
        if tile_row is not None:
            tile = {'uniprot_id': tile_row.uniprot_acc, 'tile_index': tile_row.tile_index,
                    'start_pos': tile_row.start_pos, 'end_pos': tile_row.end_pos, 'sequence': seq}
            psi, reads = tile_row.psi_wt_measured, tile_row.reads_measured
            prot = repo.get_protein(s, tile_row.uniprot_acc)
            extra = [prot.source_id] if prot else []
        else:
            tile = {'uniprot_id': None, 'tile_index': None, 'start_pos': None, 'end_pos': None, 'sequence': seq}
            psi = reads = None
            extra = []
        if run.domain_status.startswith('measured_'):
            extra.append(SRC_ZHANG_GEO)
        pred = TilePrediction(
            positions=np.array([c.position for c in cells], dtype=np.int64),
            wt=[seq[c.position - 1] for c in cells], mut=[c.mut_aa for c in cells],
            score=np.array([c.score_raw for c in cells]), prob=np.array([c.prob_calibrated for c in cells]),
            rank=np.array([c.rank_in_tile for c in cells], dtype=np.int64),
            top10=np.array([c.rank_in_tile <= 54 for c in cells]))
        domain = build_domain(run.domain_status, psi, reads, run.gate_model_id)
        warnings = [warning(c) for c in (run.warnings or [])]
        return build_result(lm.info, pred, tile, domain, warnings, repo.get_sources(s, extra) if extra else [],
                            repo.aware(run.created_at))


def tile_status_for_tier1(psi: float | None, reads: float | None) -> str:
    return status_from_measurement(psi, reads)


__all__ = ['Registry', 'LoadedModel', 'Predictor', 'Outcome', 'load_registry', 'DataSource']
