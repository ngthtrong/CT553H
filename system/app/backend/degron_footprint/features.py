"""Feature builder of the M3 model (180 features), vectorised over the 532 substitutions of a tile.

Layout, identical to the research code: [0:20] wild-type one-hot, [20:40] mutant one-hot,
[40:60] amino-acid composition of the whole tile, [60:180] one-hot residue at the six context offsets
-3,-2,-1,+1,+2,+3. This module is deliberately written in a different style from
research/calibration-p6-2026-10-22/predict.py (matrix fill instead of a per-cell loop); tests compare the two.
"""
from __future__ import annotations

import numpy as np

from .constants import AA_INDEX, AAS, CONTEXT_OFFSETS, N_FEATURES, TILE_LEN


def substitutions(seq: str) -> list[tuple[int, str]]:
    """The 532 (position, mutant) pairs: position ascending, then the alphabet without the wild-type letter."""
    return [(pos, aa) for pos in range(1, len(seq) + 1) for aa in AAS if aa != seq[pos - 1]]


def feature_matrix(seq: str) -> tuple[np.ndarray, list[tuple[int, str]]]:
    """-> (X with one row per substitution, the substitution list). `seq` must be 28 standard residues."""
    if len(seq) != TILE_LEN:
        raise ValueError(f'tile must have {TILE_LEN} residues')
    idx = np.fromiter((AA_INDEX[c] for c in seq), dtype=np.int64, count=len(seq))
    cells = substitutions(seq)
    n = len(cells)
    rows = np.arange(n)
    pos0 = np.fromiter((p - 1 for p, _ in cells), dtype=np.int64, count=n)
    mut = np.fromiter((AA_INDEX[a] for _, a in cells), dtype=np.int64, count=n)

    X = np.zeros((n, N_FEATURES))
    X[rows, idx[pos0]] = 1.0
    X[rows, 20 + mut] = 1.0
    X[:, 40:60] = np.bincount(idx, minlength=20) / len(seq)
    for b, off in enumerate(CONTEXT_OFFSETS):
        j = pos0 + off
        ok = (j >= 0) & (j < len(seq))
        X[rows[ok], 60 + b * 20 + idx[j[ok]]] = 1.0
    return X, cells
