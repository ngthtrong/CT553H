"""Domain gate: is a tile inside the domain on which the effect model was trained (PSI(WT) <= 4.0)?

Tier 1 is the PSI measured in the GPS peptidome screen (stored per tile by the ETL). Tier 2 is a gate model
(experiment R3) that does not exist yet: `NullGate` answers 'not available'. A real gate registers its
loader in GATE_LOADERS once the R3 notebook has delivered `gate-weights.npz` and `gate-card.json`.
"""
from __future__ import annotations

import json
import logging
import math
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .constants import DOMAIN_PSI_MAX, READ_MIN

log = logging.getLogger('degron_footprint.domain')

STATUSES = (
    'measured_in_domain', 'measured_out_of_domain', 'measured_unreliable',
    'predicted_in_domain', 'predicted_out_of_domain', 'unknown',
)


def status_from_measurement(psi: float | None, reads: float | None) -> str:
    """Tier-1 rule. Unreliable when the tile has too few reads or PSI is missing; `reads >= 10` is reliable."""
    if psi is None or reads is None or math.isnan(psi) or math.isnan(reads) or reads < READ_MIN:
        return 'measured_unreliable'
    return 'measured_in_domain' if psi <= DOMAIN_PSI_MAX else 'measured_out_of_domain'


@dataclass(frozen=True)
class GateAssessment:
    status: str                    # predicted_in_domain | predicted_out_of_domain
    psi_wt_predicted: float
    gate_model_id: str


class GateAdapter(Protocol):
    available: bool
    gate_model_id: str | None

    def assess(self, seq: str) -> GateAssessment | None: ...


class NullGate:
    """No gate model: every unscreened tile and every typed sequence stays 'unknown'."""

    available: bool = False
    gate_model_id: str | None = None

    def assess(self, seq: str) -> GateAssessment | None:
        return None


GATE_LOADERS: dict[str, Callable[[Path, dict], GateAdapter]] = {}


def load_gate(weights: Path | None, card: Path | None) -> GateAdapter:
    """Return the registered gate model or NullGate. Files that are present but of an unknown kind are ignored loudly."""
    if weights is None or card is None or not weights.is_file() or not card.is_file():
        return NullGate()
    try:
        info = json.loads(card.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        log.warning('gate card unreadable; gate disabled')
        return NullGate()
    loader = GATE_LOADERS.get(str(info.get('kind')))
    if loader is None:
        log.warning('gate files present but kind %r has no loader; gate disabled', info.get('kind'))
        return NullGate()
    return loader(weights, info)
