"""R6 — dữ liệu, đặc trưng và chia fold. Dùng lại đường chia của R2 (`common.py`) để mọi so sánh ghép cặp
được trên cùng ô test, cùng train/val của từng (seed, fold).

Quy ước hàng: hàng 0..N_sat-1 là 92.337 ô bão hòa (47.847 ô bộ gốc đầu tiên, 44.490 ô nới ngưỡng sau);
hàng N_sat.. là ô bộ SCANNING (`r6-scantable.npz`), luôn nằm sau.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/r2-esm-features-2026-10-22'))
import common as cm                                            # noqa: E402  (nạp luôn derisk, learning-curve, nbkit vào sys.path)
import derisk as dr                                            # noqa: E402

AAS = 'ACDEFGHIKLMNPQRSTVWY'
assert ''.join(sorted(dr.AA2I, key=dr.AA2I.get)) == AAS, 'thứ tự acid amin của derisk đã đổi'
A2I = {a: i for i, a in enumerate(AAS)}
SEEDS = cm.SEEDS
SCANTAB = TOPIC / 'data/processed/r6-scantable.npz'
L = 28
HALF = 7                       # cửa sổ cắt quanh điểm đột biến: 2·HALF+1 = 15 vị trí
CROP = 2 * HALF + 1


# ------------------------------------------------------------------ nạp dữ liệu
def load_sat():
    """Bộ gộp 92.337 ô như R2 (đã assert khớp G2 và nhãn hai cache), kèm bảng trình tự dạng mảng thường."""
    data = cm.load_combined()
    st = data['seqtab']
    data['st'] = {k: st[k] for k in ('peps', 'groups', 'wt_seq', 'idx', 'pos', 'aa', 'mut_seq', 'pep_of_row', 'y')}
    return data


def load_scan(psi_wt_max=4.0):
    """Bảng scanning. psi_wt_max ≤ 4,0 chỉ lọc HÀNG (không đánh lại chỉ số peptide)."""
    z = np.load(SCANTAB)
    s = {k: z[k] for k in ('peps', 'wt_seq', 'psi_wt', 'groups', 'pep_of_row', 'pos', 'aa', 'mut_seq', 'y')}
    assert float(z['psi_wt_max']) >= psi_wt_max
    keep = s['psi_wt'][s['pep_of_row']] <= psi_wt_max
    s['keep'] = np.where(keep)[0]
    s['rowg'] = s['groups'][s['pep_of_row']]
    return s


def scan_train_rows(scan, test_clusters):
    """Hàng scanning (đã lọc theo ngưỡng) KHÔNG thuộc cụm outer-test của fold."""
    bad = np.isin(scan['rowg'][scan['keep']], np.asarray(sorted(test_clusters)))
    return scan['keep'][~bad]


# ------------------------------------------------------------------ đặc trưng
def seq_ints(seqs):
    return np.array([[A2I.get(c, -1) for c in s] for s in seqs], dtype=np.int8)


def cell_features(wt_int, pep_of_row, pos, aa, W=3):
    """pair(40) + comp(20) + ctx có thứ tự ±W (2W·20), đúng thứ tự cột và giá trị của `derisk.featurize`
    ({'pair','comp','ctx'}) khi W=3. float64 để bằng cache từng bit."""
    n = len(pos)
    pos0 = pos.astype(np.int64) - 1
    ar = np.arange(n)
    wt_row = wt_int[pep_of_row].astype(np.int64)
    X = np.zeros((n, 60 + 2 * W * 20))
    X[ar, wt_row[ar, pos0]] = 1.0
    X[ar, 20 + np.array([A2I[a] for a in aa])] = 1.0
    comp = np.zeros((len(wt_int), 20))
    for k in range(20):
        comp[:, k] = (wt_int == k).sum(1)
    X[:, 40:60] = comp[pep_of_row] / L
    for b, o in enumerate([o for o in range(-W, W + 1) if o != 0]):
        q = pos0 + o
        ok = (q >= 0) & (q < L)
        idx = wt_row[ar, np.clip(q, 0, L - 1)]
        ok &= idx >= 0
        X[ar[ok], 60 + b * 20 + idx[ok]] = 1.0
    return X


def crop_wt_idx(wt_int, pep_of_row, pos):
    """[n, CROP] chỉ số acid amin WT quanh điểm đột biến; 20 = ngoài trình tự."""
    n = len(pos)
    q = (pos.astype(np.int64) - 1)[:, None] + np.arange(-HALF, HALF + 1)[None, :]
    ok = (q >= 0) & (q < L)
    out = wt_int[pep_of_row][np.arange(n)[:, None], np.clip(q, 0, L - 1)].astype(np.int64)
    out = np.where(ok & (out >= 0), out, 20)
    return out.astype(np.int8)


def sat_view(data):
    st = data['st']
    wt_int = seq_ints(st['wt_seq'])
    return {'wt_int': wt_int, 'pep_of_row': st['pep_of_row'].astype(np.int64), 'pos': st['pos'].astype(np.int64),
            'aa': st['aa'], 'y': st['y'], 'rowg': data['rowgc']}


def scan_view(scan):
    return {'wt_int': seq_ints(scan['wt_seq']), 'pep_of_row': scan['pep_of_row'].astype(np.int64),
            'pos': scan['pos'].astype(np.int64), 'aa': scan['aa'], 'y': scan['y'], 'rowg': scan['rowg']}
