"""Effect models: frozen weights, calibration and ranking. `ModelAdapter` is the plug point for a v2 model."""
from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np

from .constants import N_FEATURES, TOP_K
from .features import feature_matrix


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class WeightsError(Exception):
    """Weights file missing, unreadable or different from the registered hash (NFR-06)."""


@dataclass(frozen=True)
class TilePrediction:
    positions: np.ndarray        # (532,) 1-based within the tile
    wt: list[str]
    mut: list[str]
    score: np.ndarray            # raw regression output
    prob: np.ndarray             # calibrated P(DeltaPSI >= 1)
    rank: np.ndarray             # 1 = highest raw score
    top10: np.ndarray            # bool, rank <= ceil(10 % * 532)


class ModelAdapter(Protocol):
    """What the API needs from an effect model. A second model kind registers a loader in LOADERS."""

    model_id: str
    calibrators: tuple[str, ...]
    default_calibrator: str

    def predict_tile(self, seq: str, calibrator: str | None = None) -> TilePrediction: ...


def rank_scores(score: np.ndarray) -> np.ndarray:
    order = np.argsort(-score, kind='stable')
    rank = np.empty(len(score), dtype=np.int64)
    rank[order] = np.arange(1, len(score) + 1)
    return rank


class RidgePlattModel:
    """Ridge M3 on 180 features with Platt and isotonic calibrators (weights from build_model.py)."""

    kind = 'ridge_platt'

    def __init__(self, model_id: str, arrays: dict[str, np.ndarray]):
        self.model_id = model_id
        self.coef = np.asarray(arrays['coef'], dtype=np.float64)
        if self.coef.shape != (N_FEATURES,):
            raise WeightsError(f'expected {N_FEATURES} coefficients, got {self.coef.shape}')
        self.intercept = float(arrays['intercept'][0])
        self.platt_a = float(arrays['platt_coef'][0])
        self.platt_b = float(arrays['platt_intercept'][0])
        self.iso_x = np.asarray(arrays['iso_x'], dtype=np.float64)
        self.iso_y = np.asarray(arrays['iso_y'], dtype=np.float64)
        self.default_calibrator = str(arrays['calibrator'])
        self.calibrators = ('platt', 'iso')
        self.n_peptides = int(arrays['n_peptides'][0])
        self.n_cells = int(arrays['n_cells'][0])

    @classmethod
    def from_file(cls, model_id: str, path: Path, expected_sha256: str | None) -> RidgePlattModel:
        if not path.is_file():
            raise WeightsError('weights file is missing')
        if expected_sha256 is not None and sha256_file(path) != expected_sha256:
            raise WeightsError('weights file hash differs from the registered value')
        try:
            z = np.load(path, allow_pickle=False)
            return cls(model_id, {k: z[k] for k in z.files})
        except (OSError, ValueError, KeyError) as exc:
            raise WeightsError(f'weights file cannot be read: {type(exc).__name__}') from exc

    def calibrate(self, score: np.ndarray, which: str | None = None) -> np.ndarray:
        which = which or self.default_calibrator
        if which == 'platt':
            with np.errstate(over='ignore'):
                return 1.0 / (1.0 + np.exp(-(self.platt_a * score + self.platt_b)))
        if which == 'iso':
            return np.interp(score, self.iso_x, self.iso_y)
        raise ValueError(which)

    def predict_tile(self, seq: str, calibrator: str | None = None) -> TilePrediction:
        X, cells = feature_matrix(seq)
        score = X @ self.coef + self.intercept
        prob = self.calibrate(score, calibrator)
        rank = rank_scores(score)
        return TilePrediction(
            positions=np.fromiter((p for p, _ in cells), dtype=np.int64, count=len(cells)),
            wt=[seq[p - 1] for p, _ in cells], mut=[a for _, a in cells],
            score=score, prob=prob, rank=rank, top10=rank <= TOP_K)


LOADERS: dict[str, Callable[[str, Path, str | None], ModelAdapter]] = {
    'ridge_platt': RidgePlattModel.from_file,       # type: ignore[dict-item]
}
