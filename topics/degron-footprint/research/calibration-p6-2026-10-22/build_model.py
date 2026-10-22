"""Dựng mô hình của nguyên mẫu G3: ridge M3 trên toàn bộ 176 peptide (mức ext 4,0) + bộ hiệu chuẩn.

Quy trình đúng PROTOCOL §7: alpha chọn bằng inner validation theo cụm (seed 17), khớp lại trên
train+val; bộ hiệu chuẩn khớp trên OOF cross-fit 5 inner fold theo cụm của TOÀN BỘ pool; loại
bộ hiệu chuẩn theo results.json (`verdict.prototype_calibrator`). Ghi:
  data/processed/calibration-p6-model.npz   (mô hình, KHÔNG lên git)
  data/processed/calibration-p6-trainpath.npz (điểm/xác suất theo đường huấn luyện, để verify.py đối chiếu)

  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/calibration-p6-2026-10-22/build_model.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import Ridge

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(HERE))
import run_calibration as cal        # noqa: E402  (nạp run_curve)
rc, rd = cal.rc, cal.rd

SEED = 17


def main():
    res = json.loads((HERE / 'results.json').read_text())
    which = res['verdict']['prototype_calibrator']
    peps, X, y, idx, rowg, groups, psiwt = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    n = len(y)
    pool = np.arange(n)
    gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=SEED)
    ti, vi = next(gsp.split(pool, y, rowg))
    _, alpha = rc.ridge(X, y, pool[ti], pool[vi], pool[:1])
    mdl = Ridge(alpha=alpha).fit(X[:, :180], y)
    oof = cal.crossfit_oof(X, y, rowg, pool, alpha, SEED, 99)
    lab = (y >= rd.RESCUE_DELTA).astype(float)
    pl, io = cal.fit_platt(oof, lab), cal.fit_iso(oof, lab)
    score = mdl.predict(X[:, :180])
    np.savez_compressed(
        TOPIC / 'data/processed/calibration-p6-model.npz',
        coef=mdl.coef_, intercept=np.array([mdl.intercept_]), alpha=np.array([alpha]),
        platt_coef=pl.coef_[0], platt_intercept=pl.intercept_,
        iso_x=io.X_thresholds_, iso_y=io.y_thresholds_,
        calibrator=np.array(which), n_peptides=np.array([len(peps)]), n_cells=np.array([n]),
        n_clusters=np.array([len(set(groups))]))
    np.savez_compressed(
        TOPIC / 'data/processed/calibration-p6-trainpath.npz',
        score=score, platt=cal.apply_platt(pl, score), iso=io.predict(score), peps=np.asarray(peps),
        idx=np.asarray(idx))
    print(f'mô hình: {len(peps)} peptide, {len(set(groups))} cụm, {n} ô; alpha {alpha}; '
          f'bộ hiệu chuẩn nguyên mẫu = {which}')
    print(f'platt: {pl.coef_[0, 0]:.4f}*s {pl.intercept_[0]:+.4f}; iso: {len(io.X_thresholds_)} nút')


if __name__ == '__main__':
    main()
