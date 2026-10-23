"""Kiểm đường code của R2 bằng mô hình ESM GIẢ + đặc trưng giả (vài giây, CPU). KHÔNG chạy ESM-2 thật,
KHÔNG phải kết quả R2. Cũng kiểm rằng đường chia ridge M3 của common.py tái lập 0,8208 trên dữ liệu thật
(ridge, vài giây — đây là cổng của notebook, chạy được cục bộ vì chỉ là ridge M3 đã công bố ở P0).

  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/r2-esm-features-2026-10-22/selftest_r2.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as cm                                       # noqa: E402
import run_r2 as r2                                       # noqa: E402


def main():
    import torch
    data = cm.load_combined()
    st = data['seqtab']
    n = 700
    # --- chỉ mục token/vị trí: mô hình giả trả embedding one-hot của residue → Δ tại vị trí đột biến phải khác 0 đúng chỗ ---
    AA = 'ACDEFGHIKLMNPQRSTVWY'

    def embed(seqs):
        x = torch.zeros(len(seqs), 28, 20)
        for b, s in enumerate(seqs):
            for j, c in enumerate(s):
                x[b, j, AA.index(c)] = 1.0
        return x
    F = r2.extract_features(st, embed, 'cpu', batch=128, log=lambda *a: None, limit=n)
    assert F.shape == (n, 40) and F.dtype == np.float16
    for i in range(0, n, 97):
        pos = int(st['pos'][i])
        wt = st['wt_seq'][st['pep_of_row'][i]]
        site = F[i, :20].astype(float)
        want = np.zeros(20)
        want[AA.index(st['aa'][i])] += 1
        want[AA.index(wt[pos - 1])] -= 1
        assert np.allclose(site, want), (i, site, want)
        assert np.allclose(F[i, 20:].astype(float), want / 28, atol=2e-3)
    # --- cổng ridge M3: tái lập P0 ---
    from sklearn.decomposition import PCA                 # noqa: F401
    import derisk as dr
    import json
    rng = np.random.default_rng(0)
    Ffake = rng.normal(size=(len(data['yc']), 80)).astype(np.float16)
    oof, meta = r2.fit_all(data, Ffake, k=8, seeds=(17,), variants=('M3',), log=lambda *a: None)
    lc = json.loads(r2.LC_RESULTS.read_text())['results']['ridge']['ext']
    m = dr.macro_auroc(oof['M3'][17], data['y0'], data['idx0'])[0]
    print(f'ridge M3 seed 17 qua common.py: {m:.6f} (P0: {lc["macro_auroc_per_seed"][0]:.6f})')
    assert abs(m - lc['macro_auroc_per_seed'][0]) < 2e-4
    # --- quy tắc kết luận ---
    assert r2.verdict(.01, [.002, .02], [.01, .01, .01]).startswith('nhận')
    assert r2.verdict(.01, [.002, .02], [.01, -.01, .01]).startswith('lợi ích chưa bền')
    assert r2.verdict(-.01, [-.02, -.002], [-.01, -.01, -.01]).startswith('âm')
    assert r2.verdict(.0, [-.01, .01], [0., 0., 0.]).startswith('chưa đủ')
    print('selftest R2: ĐẠT')


if __name__ == '__main__':
    main()
