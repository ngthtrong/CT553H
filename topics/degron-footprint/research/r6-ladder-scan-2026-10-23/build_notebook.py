"""Sinh r6-ladder-scan.ipynb (sạch outputs). Chạy:
  python3 -I build_notebook.py && python3 -I ../notebook-kit-2026-10-22/stamp_protocol.py r6-ladder-scan.ipynb PROTOCOL.md
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'notebook-kit-2026-10-22'))
from nbbuild import md, code, write_notebook, BOOTSTRAP, validate   # noqa: E402

cells = [
    md(r'''# R6 — Chuỗi đối chứng: ngữ cảnh rộng · scanning · ESM-2 bốn cỡ · CNN/mCNN (một notebook)

Chạy **toàn bộ** các hướng đề xuất ngày 23/10/2026 trên cùng benchmark bão hòa (ext 4,0; outer-test 91 peptide), theo tiêu chí chốt trước ở
`research/r6-ladder-scan-2026-10-23/PROTOCOL.md` (SHA-256 nhúng ở ô 1; notebook dừng nếu file đổi).

| GĐ | Việc | Thiết bị |
|---|---|---|
| 0 | cổng tái lập (ridge M3 = 0,8208) + kiểm chéo nguồn scanning/bão hòa (mô tả) | CPU |
| A | ridge với ngữ cảnh ±5/±7/±10 | CPU |
| B | ridge + bộ scanning (`pool`, `prior`) | CPU |
| C | trích Δ embedding ESM-2 8M/35M/150M/650M | **GPU, Internet** |
| D | ridge + ESM theo cỡ | CPU |
| E | one-hot CNN/mCNN và ESM-35M CNN/mCNN (**phép chính: ESM-35M + mCNN so với ridge**) | **GPU** |
| F | mCNN với ESM 8M/150M/650M | **GPU** |
| G | mạng + scanning (`scan_pool`, `scan_ft`) — chạy cuối vì kỳ vọng thấp nhất (xem PROTOCOL §0) | **GPU** |

**Cách chạy (Kaggle)** — xem `research/notebook-kit-2026-10-22/RUN.md`:
1. Dựng lại **cả hai gói** (có file dữ liệu mới `r6-scantable.npz`): `make_data_package.py` rồi `make_code_package.py`; trên Kaggle tạo **version mới** của dataset `degron-data-v1` và `degron-code`; gắn cả hai vào notebook.
2. *Settings → Accelerator → GPU T4*; **Internet: bật** (tải trọng số ESM-2 từ Hugging Face; hoặc gắn sẵn bốn bản ESM-2 làm dataset/model — ô 7 tự dò thư mục chứa `config.json` có tên `esm2_t6_8M`, `esm2_t12_35M`, `esm2_t30_150M`, `esm2_t33_650M`).
3. **Lần đầu đặt `SMOKE = True`** (≈ 5 phút): kiểm GPU, Internet, trọng số ESM-2 và đường huấn luyện mạng; **không phải kết quả**. Sau đó đặt `SMOKE = False` và *Run All*.
4. Ô benchmark (trước GĐ E) in giờ GPU ước lượng theo số đo thật; nếu vượt hạn mức, bỏ bớt `STAGES` (ví dụ bỏ `'G'` trước, rồi `'F'`) — **báo giai đoạn chưa chạy là chưa chạy, không phải âm**.
5. Mỗi (cấu hình, seed, fold) lưu OOF ngay khi xong (`r6-oof-*.npz`). Phiên bị ngắt: chạy lại, ô 4 tiếp tục từ OOF đã lưu (nếu đã tải gói OOF cũ lên làm dataset và gắn vào, ô 4 tự chép về).
6. Tải `/kaggle/working/out/r6-results.zip`, giải nén vào `research/r6-ladder-scan-2026-10-23/run-<phiên>/`. Cache embedding (nhiều GB) ghi ở `/kaggle/temp` (nếu có) — **ngoài** gói kết quả.

Đọc kết quả bằng đúng bảng ở PROTOCOL §6. Chỉ phép **P** (ESM-35M + mCNN so với ridge) được gọi là "xác nhận".'''),
    code(r'''# Ô 1 — tham số (đừng sửa PROTOCOL_SHA256 bằng tay; dùng stamp_protocol.py)
PROTOCOL_SHA256 = "__STAMP__"
SMOKE = False                                   # True: kiểm hạ tầng ~5 phút, KHÔNG phải kết quả
STAGES = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G']   # bỏ bớt nếu hết hạn mức; thứ tự chạy cố định theo danh sách này
BATCH_EXTRACT = 256                             # chỉ giảm nếu hết bộ nhớ GPU; KHÔNG đổi mô hình (PROTOCOL §8)'''),
    code(BOOTSTRAP),
    code(r'''# Ô 3 — ghép cây thư mục, kiểm SHA-256 dữ liệu, kiểm PROTOCOL, kiểm GPU
if SMOKE:
    STAGES = ['smoke']
needs_gpu = SMOKE or any(s in STAGES for s in ('C', 'E', 'G', 'F'))
ctx = nbkit.setup('R6', protocol='research/r6-ladder-scan-2026-10-23/PROTOCOL.md',
                  protocol_sha256=PROTOCOL_SHA256, needs=['R6'], threads=4, seeds=[17], require_gpu=needs_gpu)
try:
    import transformers
except ImportError:
    nbkit.pip_install('transformers')'''),
    code(r'''# Ô 4 — nạp mã R6 và dữ liệu; tiếp tục từ OOF cũ nếu có
import os, glob, shutil, json, time, hashlib
from pathlib import Path
import numpy as np, torch
ctx.add_to_path('r2-esm-features-2026-10-22', 'r6-ladder-scan-2026-10-23')
import r6data as r6, r6stats, r6esm, r6nn, run_r6 as run, run_r2
for f in glob.glob('/kaggle/input/**/r6-oof-*', recursive=True) + glob.glob('/content/**/r6-oof-*', recursive=True):
    dst = ctx.out / Path(f).name
    if not dst.exists():
        shutil.copy2(f, dst); print('tiếp tục từ', Path(f).name)
data = r6.load_sat()
scan = r6.load_scan(4.0)
scan3 = r6.load_scan(3.0)
sv = r6.sat_view(data)
CACHE = None                                    # cache embedding (~10,5 GB): ưu tiên /kaggle/temp (không vào gói kết quả)
for cand in (Path('/kaggle/temp'), ctx.out.parent):
    try:
        cand.mkdir(parents=True, exist_ok=True); (cand / '.w').write_text('x'); (cand / '.w').unlink()
        CACHE = cand / 'r6-cache'; CACHE.mkdir(exist_ok=True); break
    except OSError:
        continue
free_gb = shutil.disk_usage(CACHE).free / 2**30
print(f'cache: {CACHE} · trống {free_gb:.0f} GB (cần ≈ 11 GB cho GĐ C)')
if 'C' in STAGES and free_gb < 12:
    print('⚠ ĐĨA TRỐNG KHÔNG ĐỦ cho cache embedding; bỏ cỡ 650M khỏi r6esm.MODELS hoặc dọn đĩa trước khi chạy GĐ C')
have = lambda name: run.have_oof(ctx.out, name)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
print('ô bão hòa:', len(data['yc']), '· ô scanning (≤4,0):', len(scan['keep']), '· cụm scanning:', len(set(scan['rowg'][scan['keep']])),
      '· cache:', CACHE, '· thiết bị:', dev)'''),
    code(r'''# Ô 5 — GĐ 0: cổng tái lập (ridge M3 = 0,8208) + kiểm chéo nguồn (mô tả)
if '0' in STAGES or 'smoke' in STAGES:
    t0 = time.time()
    if not have('ridge_M3'):
        o, al = run.ridge_sat(data, data['Xc'][:, :180]); run.save_oof(ctx.out, 'ridge_M3', o)
    oof_m3 = run.load_one_oof(ctx.out, 'ridge_M3')
    info = run.run_gates(data, scan, oof_m3, ctx.gates)
    ctx.gates.assert_all()
    audit = run.cross_source_audit(data, scan)
    ctx.save('r6-stage0.json', {'gates_info': info, 'cross_source_audit_descriptive': audit, 'seconds': time.time() - t0})
    print(json.dumps(audit, indent=1, ensure_ascii=False))'''),
    code(r'''# Ô 6 — GĐ A (ridge ngữ cảnh rộng) và GĐ B (ridge + scanning), CPU
if 'A' in STAGES:
    for W in run.WIDTHS:
        nm = f'ridge_W{W}'
        if not have(nm):
            X = r6.cell_features(sv['wt_int'], sv['pep_of_row'], sv['pos'], sv['aa'], W)
            o, al = run.ridge_sat(data, X); run.save_oof(ctx.out, nm, o); print('xong', nm)
if 'B' in STAGES:
    for tag, sc in (('', scan), ('_t3', scan3)):
        for mode in ('pool', 'prior'):
            nm = f'ridge_scan_{mode}{tag}'
            if not have(nm):
                o, al = run.ridge_scan(data, sc, mode); run.save_oof(ctx.out, nm, o); print('xong', nm)'''),
    code(r'''# Ô 7 — GĐ C (GPU): trích Δ embedding (crop + pool) cho bốn cỡ; crop 35M cho ô scanning
def _ok(path, n, D, crop=True):
    if not path.exists():
        return False
    s = np.load(path, mmap_mode='r').shape
    return s == ((n, r6.CROP, D) if crop else (n, 2 * D))

if 'C' in STAGES:
    s = data['st']; n_sat = len(s['mut_seq']); stage_c = {}
    for key, (mid, D) in r6esm.MODELS.items():
        t0 = time.time()
        f_crop, f_pool = CACHE / f'crop-{key}-sat.npy', CACHE / f'pool-{key}-sat.npy'
        f_scan = CACHE / f'crop-{key}-scan.npy'
        need_scan = key == 'esm35'
        if _ok(f_crop, n_sat, D) and _ok(f_pool, n_sat, D, False) and (not need_scan or _ok(f_scan, len(scan['y']), D)):
            print(key, ': dùng cache'); continue
        embed = r6esm.make_embed_fn(key, 'cuda')
        print(key, '· nguồn trọng số:', embed.source)
        r6esm.extract(key, s['wt_seq'], s['mut_seq'], s['pos'], s['pep_of_row'], embed, 'cuda', f_crop, f_pool,
                      batch=BATCH_EXTRACT)
        tmp = CACHE / f'_det-{key}.npy'
        r6esm.extract(key, s['wt_seq'], s['mut_seq'], s['pos'], s['pep_of_row'], embed, 'cuda', tmp, None,
                      batch=64, limit=128, log=lambda *a: None)
        a = np.load(f_crop, mmap_mode='r')[:128].astype(np.float32); b = np.load(tmp).astype(np.float32)
        rel = float(np.abs(a - b).max() / max(np.abs(a).max(), 1e-9))
        ctx.gates.check(f'embedding_determinism_relmax_{key}', rel, 0.0, 1e-2, strict=False)
        tmp.unlink()
        if need_scan:
            r6esm.extract(key, scan['wt_seq'], scan['mut_seq'], scan['pos'], scan['pep_of_row'], embed, 'cuda',
                          f_scan, None, batch=BATCH_EXTRACT)
        stage_c[key] = {'model': mid, 'source': str(embed.source), 'seconds': time.time() - t0}
        del embed; torch.cuda.empty_cache()
        print(key, f'xong · {time.time() - t0:.0f}s')
    ctx.save('r6-stage-c.json', stage_c)'''),
    code(r'''# Ô 8 — GĐ D (CPU): ridge + ESM (PCA-64) theo cỡ, đúng công thức R2
if 'D' in STAGES:
    R2_650 = 0.8230390437782314                   # M3+ESM của R2 (results.json)
    for key in r6esm.MODELS:
        nm = f'ridge_{key}'
        if have(nm):
            continue
        F = np.load(CACHE / f'pool-{key}-sat.npy')
        o, meta = run_r2.fit_all(data, F, variants=('M3+ESM',), log=lambda *a: None)
        run.save_oof(ctx.out, nm, o['M3+ESM']); print('xong', nm)
        if key == 'esm650':
            from r6stats import summarize_oof
            sm = summarize_oof(o['M3+ESM'], data['y0'], data['idx0'])
            ctx.gates.check('ridge_esm650_vs_R2', sm['macro_auroc_ensemble'], R2_650, 1e-3, strict=False)
        del F'''),
    code(r'''# Ô 9 — benchmark (GPU): đo giây/epoch THẬT rồi ước lượng giờ cho GĐ E, G, F — đọc trước khi để chạy hết
PACKS = {}
def get_pack(rep, with_scan):
    k = (rep, with_scan)
    if k not in PACKS:
        PACKS[k] = run.build_pack(rep, data, scan, dev, CACHE, with_scan=with_scan)
    return PACKS[k]

if any(s in STAGES for s in ('E', 'G', 'F')):
    est = {}
    tr, va, te, _ = r6.cm.pool_split(data, 17, 0)
    for name in ('oh_mcnn', 'esm35_mcnn'):
        rep, ks, F_ = run.NN_SPECS[name]
        pk = get_pack(rep, True)
        torch.cuda.synchronize() if dev == 'cuda' else None
        t0 = time.time()
        r6nn.fit(pk, tr, va, {'ks': ks, 'F': F_}, 1, max_epochs=2)
        if dev == 'cuda': torch.cuda.synchronize()
        est[name] = (time.time() - t0) / 2
    per_epoch = max(est.values())
    # ~20 epoch/lượt (trung bình R1: 5–50), 15 lượt/cấu hình; scan_pool ≈ 2,6× số hàng, scan_ft ≈ 1,4× + tiền huấn luyện
    hours = {'E (4 cấu hình)': 4 * 15 * 20 * per_epoch / 3600,
             'G (4 cấu hình scanning)': 15 * 20 * per_epoch * 2 * (2.6 + 1.4 + 1.0) / 3600,
             'F (3 cấu hình, cỡ lớn hơn)': 3 * 15 * 20 * per_epoch * 1.5 / 3600}
    print('giây/epoch đo được:', {k: round(v, 2) for k, v in est.items()})
    print('ƯỚC LƯỢNG giờ GPU (thô, chưa tính tải dữ liệu):', {k: round(v, 2) for k, v in hours.items()},
          '· tổng ≈', round(sum(hours.values()), 1), 'giờ')
    ctx.save('r6-benchmark.json', {'seconds_per_epoch': est, 'est_hours': hours})'''),
    code(r'''# Ô 10 — GĐ E (GPU): one-hot CNN/mCNN và ESM-35M CNN/mCNN; phép CHÍNH = esm35_mcnn − ridge
def run_cfg(name, mode=None, with_scan=False):
    rep, ks, F_ = run.NN_SPECS[name]
    key = name if mode is None else f'{name}+{mode}'
    if have(key):
        print('đã có', key); return
    pk = get_pack(rep, with_scan)
    run.run_nn(name, rep, ks, F_, pk, data, scan, mode=mode, out_dir=ctx.out, log=print)

if 'E' in STAGES:
    for name in ('oh_mcnn', 'esm35_mcnn', 'oh_cnn1', 'esm35_cnn1'):
        run_cfg(name, with_scan='G' in STAGES)'''),
    code(r'''# Ô 11 — GĐ F (GPU): mCNN với ESM 8M / 150M / 650M (không dùng scanning)
if 'F' in STAGES:
    for name in ('esm8_mcnn', 'esm150_mcnn', 'esm650_mcnn'):
        run_cfg(name, with_scan=False)
        PACKS.pop((run.NN_SPECS[name][0], False), None); torch.cuda.empty_cache()'''),
    code(r'''# Ô 12 — GĐ G (GPU): mạng + scanning (hàng scanning thuộc cụm outer-test bị loại; kỳ vọng thấp nhất, chạy cuối)
if 'G' in STAGES:
    for name in ('oh_mcnn', 'esm35_mcnn'):
        for mode in run.SCAN_MODES:
            run_cfg(name, mode=mode, with_scan=True)
    PACKS.clear(); torch.cuda.empty_cache()'''),
    code(r'''# Ô 13 — SMOKE (chỉ khi SMOKE = True): kiểm GPU + Internet + trọng số 8M + vòng huấn luyện; KHÔNG phải kết quả
if 'smoke' in STAGES:
    import tempfile
    embed = r6esm.make_embed_fn('esm8', 'cuda'); print('nguồn trọng số:', embed.source)
    s = data['st']; n_small = 600; d8 = r6esm.MODELS['esm8'][1]
    tmpd = Path(tempfile.mkdtemp())
    r6esm.extract('esm8', s['wt_seq'], s['mut_seq'][:n_small], s['pos'][:n_small], s['pep_of_row'][:n_small], embed,
                  'cuda', tmpd / 'c.npy', tmpd / 'p.npy', batch=64, log=lambda *a: None)
    crop = r6esm.load_to_device(tmpd / 'c.npy', 'cuda')
    pk = r6nn.Pack('cuda', r6.crop_wt_idx(sv['wt_int'], sv['pep_of_row'], sv['pos'])[:n_small], data['Xc'][:n_small, :60],
                   data['yc'][:n_small], crop=crop)
    r6nn.HP['max_epochs'] = 2
    sub = {'tr': np.arange(0, 400), 'va': np.arange(400, 500), 'te': np.arange(500, 600)}
    o, _ = run.run_nn('esm8_mcnn', 'esm8', (3, 5, 7), 32, pk, data, scan, mode=None, seeds=(17,), folds=(0,),
                      subsample=sub, log=lambda *a: None)
    assert np.isfinite(o[17][sub['te']]).all()
    print('SMOKE ĐẠT: GPU', torch.cuda.get_device_name(0), '· ESM-2 8M · huấn luyện mạng ESM chạy được. Đặt SMOKE = False.')'''),
    code(r'''# Ô 14 — TỔNG HỢP theo PROTOCOL §5–§6 (đọc mọi OOF đã lưu; giai đoạn chưa chạy thì phép so tương ứng vắng mặt)
if 'smoke' not in STAGES:
    t0 = time.time()
    allo = run.load_all_oof(ctx.out)
    agg = run.aggregate(allo, data)
    agg['stages_requested'] = STAGES
    agg['configs_present'] = sorted(allo)
    agg['configs_missing_from_protocol'] = sorted(set(
        ['ridge_M3'] + [f'ridge_W{w}' for w in run.WIDTHS] + ['ridge_scan_pool', 'ridge_scan_prior'] +
        [f'ridge_{k}' for k in r6esm.MODELS] + list(run.NN_SPECS) +
        [f'{b}+{m}' for b in ('oh_mcnn', 'esm35_mcnn') for m in run.SCAN_MODES]) - set(allo))
    agg['sha256'] = {f: hashlib.sha256(open(getattr(m, '__file__'), 'rb').read()).hexdigest()
                     for f, m in (('run_r6', run), ('r6nn', r6nn), ('r6esm', r6esm), ('r6data', r6), ('r6stats', r6stats))}
    agg['seconds_aggregate'] = time.time() - t0
    run.print_table(agg)
    ctx.save('results.json', agg)
    P = agg['contrasts'].get('P_esm35_mcnn_vs_ridge')
    print('\nKẾT LUẬN THEO PROTOCOL §6 — phép CHÍNH (ESM-35M + mCNN so với ridge M3):',
          P['verdict'] if P else 'CHƯA CHẠY (thiếu esm35_mcnn)')
    print('Giai đoạn/cấu hình chưa chạy (KHÔNG phải kết quả âm):', agg['configs_missing_from_protocol'])'''),
    code(r'''# Ô 15 — nén kết quả để tải về
ctx.finalize()'''),
]
nb = write_notebook(HERE / 'r6-ladder-scan.ipynb', cells, title='R6 ladder + scanning')
print(nb, validate(nb))
