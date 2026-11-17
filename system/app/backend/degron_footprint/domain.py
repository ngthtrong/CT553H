"""Domain gate: is a tile inside the domain on which the effect model was trained (intrinsic PSI(WT) <= 4.0)?

Tier 1 maps the PSI measured in the GPS peptidome screen through the R3 logistic; tier 2 predicts it from the
sequence (degron_footprint/gate_r3.py, registered in GATE_LOADERS). The screen PSI is on another scale than the
intrinsic PSI(WT), so it is never compared with 4.0 (DEVIATIONS.md §7). Without a gate, `NullGate` answers
"not available" and statuses stay `unknown` / `measured_unreliable`.
"""
from __future__ import annotations

import json
import logging
import math
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .constants import READ_MIN

log = logging.getLogger('degron_footprint.domain')

# Same list as the DB CHECK (db/models.py DOMAIN_STATUSES) and openapi DomainStatus. The borderline states are produced
# once the R3 gate is integrated (WP7); until then the rules below never return them.
STATUSES = (
    'measured_in_domain', 'measured_out_of_domain', 'measured_unreliable', 'measured_borderline',
    'predicted_in_domain', 'predicted_out_of_domain', 'predicted_borderline', 'unknown',
)


def status_from_measurement(psi: float | None, reads: float | None, gate: GateAdapter | None = None) -> str:
    """Tier-1 rule. Unreliable when the tile has too few reads or PSI is missing (`reads >= 10` is reliable);
    otherwise the gate's tier-1 logistic decides; with no gate the measured tile stays `unknown`."""
    if psi is None or reads is None or math.isnan(psi) or math.isnan(reads) or reads < READ_MIN:
        return 'measured_unreliable'
    tier1 = getattr(gate, 'tier1_status', None)
    return tier1(psi) if tier1 is not None else 'unknown'


@dataclass(frozen=True)
class GateAssessment:
    status: str                    # predicted_in_domain | predicted_out_of_domain
    psi_wt_predicted: float
    gate_model_id: str


class GateAdapter(Protocol):
    available: bool
    gate_model_id: str | None
    weights_sha256: str | None

    def assess(self, seq: str) -> GateAssessment | None: ...


class NullGate:
    """No gate model: every unscreened tile and every typed sequence stays 'unknown'."""

    available: bool = False
    gate_model_id: str | None = None
    weights_sha256: str | None = None

    def assess(self, seq: str) -> GateAssessment | None:
        return None


GATE_LOADERS: dict[str, Callable[[Path, dict], GateAdapter]] = {}


def load_gate(weights: Path | None, card: Path | None) -> GateAdapter:
    """Return the registered gate model or NullGate. Files that are present but of an unknown kind, or whose weights
    do not match the card, are ignored loudly. `weights` may be None when the card names its weights file."""
    if card is None or not card.is_file():
        return NullGate()
    try:
        info = json.loads(card.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        log.warning('gate card unreadable; gate disabled')
        return NullGate()
    if weights is None and isinstance(info.get('weights_file'), str):
        weights = card.parent / Path(info['weights_file']).name
    if weights is None or not weights.is_file():
        log.warning('gate weights missing; gate disabled')
        return NullGate()
    loader = GATE_LOADERS.get(str(info.get('kind')))
    if loader is None:
        log.warning('gate files present but kind %r has no loader; gate disabled', info.get('kind'))
        return NullGate()
    try:
        return loader(weights, info)
    except Exception as exc:                          # a bad file must not take the service down (NFR-06)
        log.error('gate not loaded: %s', type(exc).__name__)
        return NullGate()
