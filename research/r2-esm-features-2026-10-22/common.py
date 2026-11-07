"""Phần dùng chung R2: nạp tập nới ngưỡng 4,0 đúng như run_curve.py, và cách chia train/val/test từng (seed, fold).

Chia (seed, fold) sao chép nguyên văn kịch bản 'ext' của learning-curve-2026-10-22/run_curve.py:
  pool = hàng bộ gốc không thuộc cụm test  ∪  hàng nới ngưỡng không thuộc cụm test,
  GroupShuffleSplit(test_size=.2, random_state=seed) theo cụm → train/val; test = ô outer-test của fold.
Cổng ở notebook: ridge M3 qua đường này phải cho đúng 0,8208 (ensemble) và 0,8204/0,8210/0,8209 từng seed.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
sys.path.insert(0, str(TOPIC / 'research/notebook-kit-2026-10-22'))

SEEDS = (17, 29, 43)
ALPHAS = (1, 10, 100, 1000)
SEQTAB = TOPIC / 'data/processed/r12-seqtable.npz'


def load_combined():
    """Bộ gộp 92.337 ô: 47.847 ô bộ gốc trước, 44.490 ô nới ngưỡng sau (đúng thứ tự run_curve.main)."""
    import residue_data as rd
    import run_curve as rc
    from nbkit import StableGroupKFold as GroupKFold   # cùng fold với G2 trên mọi bản sklearn
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    base_set = set(peps0)
    new_peps = [p for p in pepsE if p not in base_set]
    pos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[pos[p]]) for p in new_peps])
    Xc = np.vstack([X0, XE[new_rows]])
    yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    st = np.load(SEQTAB)
    assert np.array_equal(st['y'], yc), 'bảng trình tự lệch nhãn bộ gộp'
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'folds không trùng G2'
    return {'Xc': Xc, 'yc': yc, 'rowgc': rowgc, 'y0': y0, 'idx0': np.asarray(idx0), 'groups0': np.asarray(groups0),
            'peps0': list(peps0), 'rowg0': rowg0, 'base_n': len(y0), 'folds_te': [te for _, te in folds],
            'fold_clusters': fold_clusters, 'seqtab': st}


def pool_split(data, seed, fold):
    from sklearn.model_selection import GroupShuffleSplit
    rowg0, rowgc, base_n, yc = data['rowg0'], data['rowgc'], data['base_n'], data['yc']
    test_clusters = set(data['fold_clusters'][fold])
    tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
    extra = np.array([i for i in range(base_n, len(yc)) if rowgc[i] not in test_clusters], dtype=int)
    pool = np.concatenate([tr_base, extra])
    ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                  .split(pool, yc[pool], rowgc[pool]))
    train, val = pool[ti], pool[vi]
    assert not (set(rowgc[train]) & test_clusters) and not (set(rowgc[val]) & test_clusters)
    return train, val, data['folds_te'][fold], pool


def ridge_full(X, y, tr, va, te):
    """Như run_curve.ridge nhưng dùng TOÀN BỘ cột của X (run_curve.ridge cắt [:, :180]). Cùng lưới alpha."""
    from sklearn.linear_model import Ridge
    best = min((float(np.mean((Ridge(alpha=a).fit(X[tr], y[tr]).predict(X[va]) - y[va]) ** 2)), a)
               for a in ALPHAS)[1]
    full = np.concatenate([tr, va])
    return Ridge(alpha=best).fit(X[full], y[full]).predict(X[te]), best
