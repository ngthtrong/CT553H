"""Dựng bảng trình tự cho 92.337 ô của tập huấn luyện nới ngưỡng 4,0 (R1 và R2 dùng chung).

Cache `learning-curve-sat-{base,ext4.0}.npz` chỉ giữ đặc trưng M3 và nhãn, KHÔNG giữ trình tự. R2 cần trình
tự để chạy ESM-2, R1 cần trình tự để chấm điểm Degformer. Bảng này dựng lại đúng thứ tự hàng mà
`run_curve.py` dùng khi gộp (hàng bộ gốc 91 peptide trước, 85 peptide nới ngưỡng sau) và kiểm khớp
nhãn + đặc trưng với hai cache. Đây là bước CHUẨN BỊ DỮ LIỆU (không huấn luyện gì).

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/r2-esm-features-2026-10-22/make_seqtable.py
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
import sys
import hashlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import residue_data as rd          # noqa: E402
import derisk as dr                # noqa: E402
import run_curve as rc             # noqa: E402

OUT = TOPIC / 'data/processed/r12-seqtable.npz'


def main():
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    d = rd.load_all(degron_psi_max=rc.EXT_PSI_MAX)
    peps, rows, y, idx = dr.rows_and_labels(d['sat'], 'sat')
    assert list(peps) == list(pepsE), 'thứ tự peptide của load_all khác cache ext'
    assert np.array_equal(np.asarray(y), yE), 'nhãn dựng lại khác cache ext'
    posE = {p: i for i, p in enumerate(pepsE)}
    base_set = set(peps0)
    new_peps = [p for p in pepsE if p not in base_set]

    comb_peps = list(peps0) + new_peps
    seqs_wt, pos_l, aa_l, mut_l, pep_l, y_l, grp_l, rows_src = [], [], [], [], [], [], [], []
    ranges = []
    for k, p in enumerate(comb_peps):
        a, b = idxE[posE[p]]
        start = len(y_l)
        for j in range(a, b):
            seq, pos, aa = rows[j]
            assert seq[pos - 1] != aa
            mut = seq[:pos - 1] + aa + seq[pos:]
            pos_l.append(pos); aa_l.append(aa); mut_l.append(mut); pep_l.append(k)
            y_l.append(y[j]); rows_src.append(j)
        seqs_wt.append(rows[a][0])
        ranges.append((start, len(y_l)))
        grp_l.append(groupsE[posE[p]])
    y_c = np.asarray(y_l)
    base_n = len(y0)
    # cổng 1: nhãn khớp hai cache theo đúng thứ tự gộp của run_curve
    assert np.array_equal(y_c[:base_n], y0), 'hàng bộ gốc lệch nhãn'
    new_rows_cache = np.concatenate([np.arange(*idxE[posE[p]]) for p in new_peps])
    assert np.array_equal(y_c[base_n:], yE[new_rows_cache]), 'hàng nới ngưỡng lệch nhãn'
    # cổng 2: đặc trưng dựng lại khớp cache trên mẫu ngẫu nhiên
    Xc = np.vstack([X0, XE[new_rows_cache]])
    rng = np.random.default_rng(0)
    sample = np.sort(rng.choice(len(y_c), 600, replace=False))
    rr = [(seqs_wt[pep_l[i]], pos_l[i], aa_l[i]) for i in sample]
    Xs = dr.featurize(rr, {'pair', 'comp', 'ctx'})
    assert np.allclose(Xs, Xc[sample]), 'đặc trưng dựng lại khác cache'
    assert [tuple(r) for r in np.asarray(ranges)[:len(peps0)]] == [tuple(map(int, r)) for r in idx0], \
        'idx bộ gốc lệch'
    np.savez_compressed(
        OUT,
        peps=np.asarray(comb_peps), groups=np.asarray(grp_l), wt_seq=np.asarray(seqs_wt),
        idx=np.asarray(ranges, dtype=np.int64), pos=np.asarray(pos_l, dtype=np.int16),
        aa=np.asarray(aa_l), mut_seq=np.asarray(mut_l), pep_of_row=np.asarray(pep_l, dtype=np.int32),
        y=y_c, base_n=np.asarray(base_n), n_base_peptides=np.asarray(len(peps0)))
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f'-> {OUT}  {len(comb_peps)} peptide, {len(y_c)} ô (gốc {base_n} + nới {len(y_c) - base_n})')
    print(f'sha256 {sha}')


if __name__ == '__main__':
    main()
