"""Kiểm đường code R6 — KHÔNG phải thí nghiệm, KHÔNG in AUROC của bất kỳ biến thể nào ngoài mốc ridge M3 đã biết.

Chạy từ gốc repo (CPU, vài phút):
  OPENBLAS_NUM_THREADS=2 R6_ESM8_PATH=<thư-mục-esm2_t6_8M> .venv/bin/python -I \
    topics/degron-footprint/research/r6-ladder-scan-2026-10-23/selftest_r6.py
Nếu không đặt R6_ESM8_PATH, phần dùng mô hình thật cố tải `facebook/esm2_t6_8M_UR50D` từ Hugging Face.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r6data as r6                                         # noqa: E402
import r6stats as st                                        # noqa: E402
import r6esm                                                # noqa: E402
import r6nn                                                 # noqa: E402
import run_r6 as run                                        # noqa: E402
import nbkit                                                # noqa: E402

ok = []


def passed(msg):
    ok.append(msg)
    print('  ✔', msg)


t0 = time.time()
print('[1] nạp dữ liệu')
data = r6.load_sat()
scan = r6.load_scan(4.0)
n_sat, base_n = len(data['yc']), data['base_n']
assert n_sat == 92337 and base_n == 47847
passed(f'bão hòa {n_sat} ô, scanning {len(scan["keep"])} ô / {len(set(scan["groups"]))} cụm')

print('[2] đặc trưng: dựng lại M3 bằng cell_features(W=3) phải bằng cache từng bit')
sv = r6.sat_view(data)
Xw = r6.cell_features(sv['wt_int'], sv['pep_of_row'], sv['pos'], sv['aa'], 3)
assert np.array_equal(Xw, data['Xc'][:, :180]), 'đặc trưng dựng lại khác cache'
passed('cell_features(W=3) == cache M3 trên 92.337 ô')
for W in run.WIDTHS:
    XW = r6.cell_features(sv['wt_int'], sv['pep_of_row'], sv['pos'], sv['aa'], W)
    assert XW.shape == (n_sat, 60 + 2 * W * 20) and np.array_equal(XW[:, :60], Xw[:, :60])
    assert np.array_equal(XW[:, :180][:, :60], Xw[:, :60])
passed(f'đặc trưng ngữ cảnh rộng ±{run.WIDTHS}: đúng kích thước, khối pair/comp trùng M3')
cw = r6.crop_wt_idx(sv['wt_int'], sv['pep_of_row'], sv['pos'])
rows = np.where(sv['pos'] == 1)[0][:5]
assert (cw[rows, :r6.HALF] == 20).all() and (cw[rows, r6.HALF] == sv['wt_int'][sv['pep_of_row'][rows], 0]).all()
rows = np.where(sv['pos'] == 28)[0][:5]
assert (cw[rows, r6.HALF + 1:] == 20).all()
passed('crop_wt_idx: biên đầu/cuối trình tự đúng, trung tâm là WT tại điểm đột biến')

print('[3] mốc ridge M3 ext 4,0 qua đường chia của R6 (đã biết 0,8208)')
gates = nbkit.Gates()
oof_m3, _ = run.ridge_sat(data, data['Xc'][:, :180])
info = run.run_gates(data, scan, oof_m3, gates)
gates.assert_all()
passed(f'cổng: {len(gates.items)} cổng đạt; M3 ensemble = {info["summary_M3"]["macro_auroc_ensemble"]:.6f}')

print('[4] ridge + scanning: chỉ kiểm bất biến (hữu hạn, không rò cụm test), KHÔNG in AUROC')
for mode in ('pool', 'prior'):
    o, a = run.ridge_scan(data, scan, mode, seeds=(17,), folds=(0,))
    te0 = data['folds_te'][0]
    assert np.isfinite(o[17][te0]).all() and np.isnan(np.delete(o[17], te0)).all()
passed('ridge_scan pool/prior chạy, chỉ ghi vào ô test của fold 0, hữu hạn')
o, _ = run.ridge_sat(data, r6.cell_features(sv['wt_int'], sv['pep_of_row'], sv['pos'], sv['aa'], 5),
                     seeds=(17,), folds=(0,))
assert np.isfinite(o[17][data['folds_te'][0]]).all()
passed('ridge_sat với đặc trưng W=5 chạy')

print('[5] thống kê: compare m=1 phải trùng run_curve.compare; Bonferroni làm CI rộng hơn; quy tắc kết luận')
import run_curve as rc
sA = st.summarize_oof(oof_m3, data['y0'], data['idx0'])
rng = np.random.default_rng(0)
fake = {s: oof_m3[s] + rng.normal(0, .15, base_n) for s in oof_m3}
sB = st.summarize_oof(fake, data['y0'], data['idx0'])
c1 = st.compare(sB['per_peptide_ensemble'], sA['per_peptide_ensemble'], data['groups0'], m=1)
ref = rc.compare(sB['per_peptide_ensemble'], sA['per_peptide_ensemble'], data['groups0'])
assert abs(c1['delta'] - ref['delta']) < 1e-12 and np.allclose(c1['ci95'], ref['ci95'])
c4 = st.compare(sB['per_peptide_ensemble'], sA['per_peptide_ensemble'], data['groups0'], m=4)
assert c4['ci_adj'][0] < c1['ci95'][0] and c4['ci_adj'][1] > c1['ci95'][1]
assert st.verdict([0.001, 0.01], [1, 1, 1]) == 'nhận'
assert st.verdict([0.001, 0.01], [1, -1, 1]).startswith('lợi ích chưa bền')
assert st.verdict([-0.02, -0.001], [-1, -1, -1]) == 'âm'
assert st.verdict([-0.01, 0.01], [1, 1, 1]).startswith('chưa đủ')
passed('compare trùng run_curve.compare; Bonferroni rộng hơn; bốn nhánh kết luận đúng')
agg = run.aggregate({'ridge_M3': oof_m3, 'esm35_mcnn': fake}, data)
assert 'P_esm35_mcnn_vs_ridge' in agg['contrasts']
passed('aggregate dựng được phép so chính từ OOF')

print('[6] cross_source_audit chạy và cho số hữu hạn')
au = run.cross_source_audit(data, scan)
assert au['all_shared_wt_le_4.0']['n_cells'] > 1000 and np.isfinite(au['all_shared_wt_le_4.0']['pearson'])
passed(f'kiểm chéo nguồn: {au["all_shared_wt_le_4.0"]["n_cells"]} ô trùng')

print('[7] mạng trên one-hot: SMOKE (2 epoch, tập con) — chỉ kiểm cơ học')
import torch
r6nn.HP['max_epochs'] = 2
dev = 'cpu'
torch.set_num_threads(2)
pack = run.build_pack('onehot', data, scan, dev, None, with_scan=True)
assert pack.wt_idx.shape[0] == n_sat + len(scan['y']) and pack.src.sum() == len(scan['y'])
sub = {'tr': np.arange(0, 3000), 'va': np.arange(3000, 3600), 'te': np.arange(3600, 4200), 'n_scan': 2000}
tmp = Path(tempfile.mkdtemp())
for mode in (None, 'scan_pool', 'scan_ft'):
    o, meta = run.run_nn('oh_mcnn', 'onehot', (3, 5, 7), 32, pack, data, scan, mode=mode, seeds=(17,), folds=(0,),
                         out_dir=tmp, subsample=sub, log=lambda *a: None)
    assert np.isfinite(o[17][sub['te']]).all()
passed('run_nn: scratch / scan_pool / scan_ft chạy và cho điểm hữu hạn')
o1, _ = run.run_nn('oh_cnn1', 'onehot', (5,), 96, pack, data, scan, mode=None, seeds=(17,), folds=(0,),
                   subsample=sub, log=lambda *a: None)
o2, _ = run.run_nn('oh_cnn1', 'onehot', (5,), 96, pack, data, scan, mode=None, seeds=(17,), folds=(0,),
                   subsample=sub, log=lambda *a: None)
assert np.array_equal(o1[17][sub['te']], o2[17][sub['te']])
passed('tất định theo seed trên CPU (hai lần chạy cho cùng điểm)')
n_before = len(json.loads((tmp / 'r6-oof-oh_mcnn.meta.json').read_text()))
run.run_nn('oh_mcnn', 'onehot', (3, 5, 7), 32, pack, data, scan, mode=None, seeds=(17,), folds=(0,),
           out_dir=tmp, subsample=sub, log=lambda *a: None)
assert len(json.loads((tmp / 'r6-oof-oh_mcnn.meta.json').read_text())) == n_before
passed('tiếp tục được: chạy lại không huấn luyện lại fold đã xong')

print('[8] ESM-2 8M thật trên CPU: kiểm cắt cửa sổ, biên, và đường nạp vào mạng')
src8 = os.environ.get('R6_ESM8_PATH')
try:
    embed = r6esm.make_embed_fn('esm8', 'cpu', source=src8)
except Exception as e:                                           # noqa: BLE001
    embed = None
    print('  ⚠ bỏ qua phần ESM thật (không có trọng số 8M):', str(e)[:120])
if embed is not None:
    s = data['st']
    pick = np.concatenate([np.where(s['pos'] == p)[0][:3] for p in (1, 2, 14, 27, 28)])
    tmpd = Path(tempfile.mkdtemp())
    wt_seq, mut_seq = s['wt_seq'], s['mut_seq'][pick]
    r6esm.extract('esm8', wt_seq, mut_seq, s['pos'][pick], s['pep_of_row'][pick], embed, 'cpu',
                  tmpd / 'crop.npy', tmpd / 'pool.npy', batch=8, log=lambda *a: None)
    crop = np.load(tmpd / 'crop.npy').astype(np.float32)
    pool = np.load(tmpd / 'pool.npy').astype(np.float32)
    D = r6esm.MODELS['esm8'][1]
    assert crop.shape == (len(pick), r6.CROP, D) and pool.shape == (len(pick), 2 * D)
    for r in range(len(pick)):                                   # đối chiếu độc lập từng ô
        i = pick[r]
        hm = embed([s['mut_seq'][i]])[0].numpy()
        hw = embed([s['wt_seq'][s['pep_of_row'][i]]])[0].numpy()
        delta = hm - hw
        p0 = int(s['pos'][i]) - 1
        for k, o in enumerate(range(-r6.HALF, r6.HALF + 1)):
            q = p0 + o
            ref = delta[q] if 0 <= q < r6.L else np.zeros(D)
            assert np.allclose(crop[r, k], ref, atol=2e-3), (r, k)
        assert np.allclose(pool[r], np.concatenate([delta[p0], delta.mean(0)]), atol=2e-3)
        assert np.abs(delta[p0]).sum() > 0
    passed('crop/pool khớp tính tay ở vị trí 1, 2, 14, 27, 28 (kể cả biên)')
    # nạp vào mạng ESM bằng pack nhỏ và chạy 2 epoch
    n_small = 600
    extract_rows = np.arange(n_small)
    r6esm.extract('esm8', data['st']['wt_seq'], data['st']['mut_seq'][:n_small], data['st']['pos'][:n_small],
                  data['st']['pep_of_row'][:n_small], embed, 'cpu', tmpd / 'c2.npy', batch=64, log=lambda *a: None)
    crop_t = r6esm.load_to_device(tmpd / 'c2.npy', 'cpu')
    pk = r6nn.Pack('cpu', run.r6.crop_wt_idx(sv['wt_int'], sv['pep_of_row'], sv['pos'])[:n_small],
                   data['Xc'][:n_small, :60], data['yc'][:n_small], crop=crop_t)
    assert pk.D == D
    sub2 = {'tr': np.arange(0, 400), 'va': np.arange(400, 500), 'te': np.arange(500, 600)}
    o, meta = run.run_nn('esm8_mcnn', 'esm8', (3, 5, 7), 32, pk, data, scan, mode=None, seeds=(17,), folds=(0,),
                         subsample=sub2, log=lambda *a: None)
    assert np.isfinite(o[17][sub2['te']]).all()
    passed('mạng ESM (8M thật, 600 ô) huấn luyện 2 epoch và dự đoán hữu hạn')

print(f'\nTẤT CẢ {len(ok)} KIỂM ĐẠT ({time.time() - t0:.0f}s). Đây là kiểm đường code, không phải kết quả R6.')
