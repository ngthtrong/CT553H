"""Assemble the PredictionResult object (openapi.yaml) and its warnings from plain values."""
from __future__ import annotations

from datetime import datetime

from .model import TilePrediction
from .provenance import ModelInfo, build_provenance

WARNING_TEXT = {
    'DOMAIN_UNKNOWN': 'The domain of this tile is unknown: it was not measured in the GPS screen and no gate model '
                      'covers it. The model was trained only on tiles with intrinsic wild-type PSI <= 4.0; scores '
                      'for a stable tile are not meaningful.',
    'DOMAIN_BORDERLINE': 'The domain gate places this tile between its in-domain and out-of-domain cuts '
                         '(0.5 <= P(in domain) < 0.8): the scores may not apply to it.',
    'DOMAIN_UNRELIABLE': 'The tile is in the GPS screen but its measurement is unreliable (too few reads or no PSI). '
                         'Whether it belongs to the training domain is uncertain.',
    'OUT_OF_DOMAIN_OVERRIDDEN': 'The domain gate places this tile outside the training domain (P(in domain) < 0.5). '
                                'You asked for scores anyway; treat them as unsupported.',
    'PREDICTED_DOMAIN': 'The domain status comes from a gate model, not from a measurement.',
    'TRAINING_PEPTIDE': 'This tile is among the peptides the model was trained on; its scores are not an '
                        'out-of-sample estimate.',
}


def warning(code: str) -> dict:
    return {'code': code, 'message': WARNING_TEXT[code]}


def domain_message(status: str, psi: float | None, reads: float | None, gate_model_id: str | None) -> str:
    if status == 'measured_in_domain':
        return 'Tile PSI measured in the GPS peptidome screen (replicate 1).'
    if status == 'measured_out_of_domain':
        return (f'Screen PSI {psi:.2f} (GPS peptidome, replicate 1) maps to P(in domain) < 0.5 under gate '
                f'{gate_model_id or "R3"}: outside the training domain.')
    if status == 'measured_borderline':
        return (f'Screen PSI {psi:.2f} (GPS peptidome, replicate 1) maps to 0.5 <= P(in domain) < 0.8 under gate '
                f'{gate_model_id or "R3"}: borderline.')
    if status == 'measured_unreliable':
        return 'The tile is in the GPS peptidome screen, but too few reads or no PSI: the measurement is unreliable.'
    if status.startswith('predicted_'):
        return f'Domain predicted by gate model {gate_model_id}; not measured.'
    return 'Domain unknown: no measurement and no gate model for this tile.'


def build_domain(status: str, psi: float | None, reads: float | None, gate_model_id: str | None = None) -> dict:
    return {
        'status': status,
        'psi_wt_measured': psi if status.startswith('measured_') else None,
        'reads_measured': reads if status.startswith('measured_') else None,
        'gate_model_id': gate_model_id,
        'message': domain_message(status, psi, reads, gate_model_id),
    }


def warnings_for(status: str, overridden: bool, training_peptide: bool) -> list[dict]:
    codes: list[str] = []
    if status == 'unknown':
        codes.append('DOMAIN_UNKNOWN')
    if status == 'measured_unreliable':
        codes.append('DOMAIN_UNRELIABLE')
    if status.endswith('_borderline'):
        codes.append('DOMAIN_BORDERLINE')
    if status.startswith('predicted_'):
        codes.append('PREDICTED_DOMAIN')
    if overridden:
        codes.append('OUT_OF_DOMAIN_OVERRIDDEN')
    if training_peptide:
        codes.append('TRAINING_PEPTIDE')
    return [warning(c) for c in codes]


def _optional(values, i: int) -> float | None:
    return None if values is None else float(values[i])


def cells_payload(pred: TilePrediction) -> list[dict]:
    """Cell objects; the seed spread fields (plan-system 1.3) are null for a model without seeds."""
    return [
        {'position': int(p), 'wt_aa': w, 'mut_aa': m, 'score_dpsi_raw': float(s),
         'p_dpsi_ge_1_calibrated': float(q), 'rank_in_tile': int(r), 'top10pct_in_tile': bool(t),
         'score_seed_sd': _optional(pred.seed_sd, i), 'score_seed_min': _optional(pred.seed_min, i),
         'score_seed_max': _optional(pred.seed_max, i)}
        for i, (p, w, m, s, q, r, t) in enumerate(zip(pred.positions, pred.wt, pred.mut, pred.score, pred.prob,
                                                      pred.rank, pred.top10, strict=False))
    ]


def build_result(model: ModelInfo, pred: TilePrediction, tile: dict, domain: dict, warnings: list[dict],
                 extra_sources: list[dict] | None = None, generated_at: datetime | None = None) -> dict:
    return {
        'provenance': build_provenance(model, extra_sources, generated_at),
        'tile': tile,
        'domain': domain,
        'warnings': warnings,
        'cells': cells_payload(pred),
    }
