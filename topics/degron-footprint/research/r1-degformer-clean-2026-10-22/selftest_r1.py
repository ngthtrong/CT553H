"""Kiểm đường code của run_r1.py trên dữ liệu GIẢ rất nhỏ (vài giây, CPU). Đây KHÔNG phải huấn luyện R1.

  .venv/bin/python -I topics/degron-footprint/research/r1-degformer-clean-2026-10-22/selftest_r1.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_r1 as r1                                       # noqa: E402


def main():
    consts = r1.published_constants()
    assert consts == {'MAX_LEN': 28, 'BATCH_SIZE': 512, 'EPOCHS': 50, 'LR': 1e-4}, consts
    Net = r1.degformer_class()
    rng = np.random.default_rng(0)
    n = 3000
    enc = rng.integers(0, 20, size=(n, 28), dtype=np.uint8)
    y = rng.normal(3.7, 1.2, n)
    group = rng.integers(0, 150, n).astype(np.int64)
    tm = rng.integers(0, 20, size=(64, 28), dtype=np.uint8)
    tw = rng.integers(0, 20, size=(64, 28), dtype=np.uint8)
    sc, rec, state = r1.train_fold(Net, enc, y, np.arange(n), group, tm, tw, 17, 0, 'cpu', consts,
                                   max_epochs=2, log=lambda *a: None)
    assert sc.shape == (64,) and np.isfinite(sc).all()
    assert rec['n_train'] + rec['n_val'] == n and rec['best_epoch'] in (1, 2)
    sc2, _, _ = r1.train_fold(Net, enc, y, np.arange(n), group, tm, tw, 17, 0, 'cpu', consts,
                              max_epochs=2, log=lambda *a: None)
    print('tất định (CPU, cùng seed): max |Δ| =', float(np.abs(sc - sc2).max()))
    assert np.abs(sc - sc2).max() < 1e-5
    enc2 = r1.encode_seqs(['A' * 27 + '*', 'ACDEFGHIKLMNPQRSTVWYACDEFGHI'])
    assert enc2[0, -1] == 20 and enc2.shape == (2, 28)
    # quy tắc kết luận
    import aggregate_r1 as ag
    assert ag.verdict(.01, [.002, .02], {17: .01, 29: .01, 43: .01}, 3).startswith('Degformer sạch cụm HƠN')
    assert ag.verdict(.01, [.002, .02], {17: .01}, 1).startswith('Tạm thời hơn')
    assert ag.verdict(-.01, [-.02, -.002], {17: -.01, 29: -.01, 43: -.01}, 3).startswith('ridge ext 4,0 HƠN')
    assert ag.verdict(.0, [-.01, .01], {17: .0, 29: .0, 43: .0}, 3).startswith('Không phân biệt')
    print('selftest R1: ĐẠT')


if __name__ == '__main__':
    main()
