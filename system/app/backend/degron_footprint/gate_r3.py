"""The R3 domain gate (research/r3-domain-gate-2026-10-22; DEVIATIONS.md §7; implementation plan WP7).

Two tiers, both a two-parameter logistic of a PSI on the *screen* scale (the screen PSI is offset from the intrinsic
PSI(WT) the model was trained on by about 0.9, so the raw 4.0 threshold must never be applied to it):

* tier 1, measured tile:  P = σ(a1 + b1·x), x = screen PSI (reads ≥ 10)
* tier 2, sequence only:  x̂ = counts(20 aa + 400 adjacent pairs) · coef + intercept;  P = σ(a2 + b2·x̂)

in-domain if P ≥ 0.8, out-of-domain if P < 0.5, borderline in between. The weights file is the frozen R3 output; the
card next to it is written by the application's ETL (the R3 files are never edited) and pins the weights' SHA-256.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from .constants import AA_INDEX
from .domain import GATE_LOADERS, GateAdapter, GateAssessment

KIND = 'r3-logistic-ridge'
GATE_CARD = 'gate.json'                 # written by the ETL into the model directory
N_FEATURES = 420


def sigmoid(z: float) -> float:
    """Numerically stable logistic (no overflow for large |z|)."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def features(seq: str) -> np.ndarray:
    """Same features as run_r3.feats: counts of the 20 amino acids, then of the 400 adjacent pairs (index a*20+b)."""
    x = np.zeros(N_FEATURES)
    idx = [AA_INDEX[c] for c in seq]
    for a in idx:
        x[a] += 1.0
    for a, b in zip(idx, idx[1:], strict=False):
        x[20 + a * 20 + b] += 1.0
    return x


def features_matrix(seqs: list[str]) -> np.ndarray:
    """features() for many 28-mers at once (the ETL scores every unscreened tile)."""
    idx = np.array([[AA_INDEX[c] for c in s] for s in seqs], dtype=np.int64).reshape(len(seqs), -1)
    x = np.zeros((len(seqs), N_FEATURES))
    rows = np.arange(len(seqs))
    for col in range(idx.shape[1]):
        np.add.at(x, (rows, idx[:, col]), 1.0)
    pairs = 20 + idx[:, :-1] * 20 + idx[:, 1:]
    np.add.at(x, (np.repeat(rows, pairs.shape[1]), pairs.ravel()), 1.0)
    return x


class GateWeightsError(RuntimeError):
    pass


class R3Gate:
    available = True

    def __init__(self, weights: Path, card: dict):
        sha = hashlib.sha256(weights.read_bytes()).hexdigest()
        if sha != card['weights_sha256']:
            raise GateWeightsError('gate weights do not match the SHA-256 in the gate card')
        z = np.load(weights, allow_pickle=False)
        self.gate_model_id: str | None = str(card['gate_model_id'])
        self.weights_sha256: str | None = sha
        self.coef = np.asarray(z['tier2_coef'], dtype=float)
        self.intercept = float(np.asarray(z['tier2_intercept']).ravel()[0])
        m1, m2 = np.asarray(z['m1'], dtype=float).ravel(), np.asarray(z['m2'], dtype=float).ravel()
        self.m1: tuple[float, float] = (float(m1[0]), float(m1[1]))
        self.m2: tuple[float, float] = (float(m2[0]), float(m2[1]))
        self.p_in = float(np.asarray(z['p_in']).ravel()[0])
        self.p_out = float(np.asarray(z['p_out']).ravel()[0])
        self.usable_tier1 = bool(np.asarray(z['usable_tier1']).ravel()[0])
        self.usable_tier2 = bool(np.asarray(z['usable_tier2']).ravel()[0])
        if self.coef.shape != (N_FEATURES,):
            raise GateWeightsError('tier-2 coefficients must have 420 entries')

    # ------------------------------------------------------------------ shared
    def _status(self, p: float, prefix: str) -> str:
        if p >= self.p_in:
            return f'{prefix}_in_domain'
        if p < self.p_out:
            return f'{prefix}_out_of_domain'
        return f'{prefix}_borderline'

    # ------------------------------------------------------------------ tier 1
    def tier1_probability(self, screen_psi: float) -> float:
        return sigmoid(self.m1[0] + self.m1[1] * screen_psi)

    def tier1_status(self, screen_psi: float) -> str:
        return self._status(self.tier1_probability(screen_psi), 'measured')

    # ------------------------------------------------------------------ tier 2
    def predict_screen_psi(self, seq: str) -> float:
        return float(features(seq) @ self.coef + self.intercept)

    def assess(self, seq: str) -> GateAssessment | None:
        if not self.usable_tier2 or len(seq) != 28 or any(c not in AA_INDEX for c in seq):
            return None
        x_hat = self.predict_screen_psi(seq)
        p = sigmoid(self.m2[0] + self.m2[1] * x_hat)
        return GateAssessment(self._status(p, 'predicted'), x_hat, self.gate_model_id or '')

    def assess_many(self, seqs: list[str]) -> list[tuple[str, float]]:
        """(status, x̂) for many scorable 28-mers; same numbers as assess()."""
        if not seqs:
            return []
        x_hat = features_matrix(seqs) @ self.coef + self.intercept
        p = 1.0 / (1.0 + np.exp(-(self.m2[0] + self.m2[1] * x_hat)))
        return [(self._status(float(pi), 'predicted'), float(xi)) for pi, xi in zip(p, x_hat, strict=True)]

    def cuts(self) -> dict:
        """PSI cut points equivalent to the probability thresholds (for documentation and tests)."""
        def cut(m: tuple[float, float], p: float) -> float:
            return (math.log(p / (1 - p)) - m[0]) / m[1]
        return {'tier1': {'in_at_or_below': cut(self.m1, self.p_in), 'out_at_or_above': cut(self.m1, self.p_out)},
                'tier2': {'in_at_or_below': cut(self.m2, self.p_in), 'out_at_or_above': cut(self.m2, self.p_out)}}


def card_for(weights: Path, gate_model_id: str, source_card: dict) -> dict:
    """The application's own card for the R3 weights (written by the ETL next to the copied weights)."""
    return {'kind': KIND, 'gate_model_id': gate_model_id, 'weights_file': weights.name,
            'weights_sha256': hashlib.sha256(weights.read_bytes()).hexdigest(),
            'source': 'research/r3-domain-gate-2026-10-22 (run-kaggle-20261022)',
            'tier1': source_card.get('tier1', {}), 'tier2': source_card.get('tier2', {}),
            'limits': source_card.get('limits', []), 'evidence_label': 'R3 OOF evaluation, development only'}


def _load(weights: Path, card: dict) -> GateAdapter:
    return R3Gate(weights, card)


def load_card(card_path: Path) -> tuple[Path, dict]:
    card = json.loads(card_path.read_text(encoding='utf-8'))
    return card_path.parent / card['weights_file'], card


GATE_LOADERS[KIND] = _load
