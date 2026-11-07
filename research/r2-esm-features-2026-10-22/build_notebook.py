"""Sinh r2-esm.ipynb (sạch outputs). Chạy:
  python3 -I build_notebook.py && python3 -I ../notebook-kit-2026-10-22/stamp_protocol.py r2-esm.ipynb PROTOCOL.md
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'notebook-kit-2026-10-22'))
from nbbuild import md, code, write_notebook, BOOTSTRAP, validate   # noqa: E402

cells = [
    md('''# R2 — Đặc trưng ESM-2 đóng băng cộng vào ridge M3

Giai đoạn 1 (**GPU**): trích Δ embedding (mutant − WT) của `facebook/esm2_t33_650M_UR50D` cho 92.337 ô. Giai đoạn 2 (**CPU**): PCA(64) chỉ trên outer-train từng fold,
ridge trên M3 ∪ PCA, so ghép cặp theo cụm với ridge M3 (cùng chia train/val), 3 seed. Tiêu chí chốt trước:
`research/r2-esm-features-2026-10-22/PROTOCOL.md` (SHA-256 nhúng ở ô 1).

**Cách chạy (Kaggle):**
1. Import notebook; gắn 2 dataset riêng tư `degron-code-*` và `degron-data-v1` (xem `research/notebook-kit-2026-10-22/RUN.md`).
2. *Settings → Accelerator → GPU T4/P100*.
3. **Internet: bật** để tải trọng số từ Hugging Face (cần tài khoản đã xác minh điện thoại). Nếu không bật được: thêm ESM-2 650M làm dataset/model và gắn vào notebook — ô 5 tự dò thư mục chứa `config.json` có tên `esm2_t33_650M`.
4. *Run All*. Cache đặc trưng (~0,5 GB) ghi ở `/kaggle/working/out/r2-cache/` — **ngoài** gói kết quả; phiên ngắt giữa chừng thì chạy lại và ô 5 dùng cache.
5. Tải `/kaggle/working/out/r2-results.zip`, giải nén vào `research/r2-esm-features-2026-10-22/run-<phiên>/`.

`SMOKE = True` chỉ trích 2.048 ô để kiểm đường code và dừng trước giai đoạn 2; **không** dùng kết quả SMOKE.'''),
    code('''# Ô 1 — tham số (đừng sửa PROTOCOL_SHA256 bằng tay; dùng stamp_protocol.py)
PROTOCOL_SHA256 = "__STAMP__"
SMOKE = False
BATCH = 256                # chỉ giảm nếu hết bộ nhớ GPU; KHÔNG đổi mô hình (PROTOCOL §5)'''),
    code(BOOTSTRAP),
    code('''# Ô 3 — ghép cây thư mục, kiểm SHA-256 dữ liệu, kiểm PROTOCOL, kiểm GPU
ctx = nbkit.setup('R2', protocol='research/r2-esm-features-2026-10-22/PROTOCOL.md',
                  protocol_sha256=PROTOCOL_SHA256, needs=['R2'], threads=4, seeds=[17], require_gpu=True)
try:
    import transformers
except ImportError:
    nbkit.pip_install('transformers')'''),
    code('''# Ô 4 — nạp mã R2 và bảng trình tự (cổng: khớp nhãn, 5 fold trùng G2)
ctx.add_to_path('r2-esm-features-2026-10-22')
import time, hashlib, json
import numpy as np, torch
import common as cm, run_r2
data = cm.load_combined()
st = data['seqtab']
assert len(st['mut_seq']) == 92337
print('ô:', len(st['mut_seq']), '· peptide:', len(st['wt_seq']))'''),
    code('''# Ô 5 — GIAI ĐOẠN 1 (GPU): trích đặc trưng ESM-2, dùng cache nếu đã có
cache_dir = ctx.out.parent / 'r2-cache'; cache_dir.mkdir(exist_ok=True)
fpath = cache_dir / ('r2-esm-features-smoke.npy' if SMOKE else 'r2-esm-features.npy')
dev = 'cuda'
t0 = time.time()
if fpath.exists():
    F = np.load(fpath); source = 'cache'; print('dùng cache', fpath)
else:
    embed = run_r2.make_hf_embed_fn(dev)
    source = embed.source; print('nguồn trọng số:', source)
    F = run_r2.extract_features(st, embed, dev, batch=BATCH, limit=2048 if SMOKE else None)
    np.save(fpath, F)
    # cổng tất định: trích lại 128 ô đầu phải cho cùng giá trị (dung sai fp16)
    F2 = run_r2.extract_features(st, embed, dev, batch=BATCH, limit=128, log=lambda *a: None)
    a, b = F[:128].astype(np.float32), F2.astype(np.float32)
    ctx.gates.check('embedding_determinism_relmax', float(np.abs(a - b).max() / np.abs(a).max()), 0.0, 1e-2)   # fp16, batch khác cỡ
n_expect = 2048 if SMOKE else 92337
ctx.gates.check('n_cells', F.shape[0], n_expect, 0)
ctx.gates.check('finite', float(np.isfinite(F).all()), 1.0, 0)
print('F:', F.shape, F.dtype, f'{time.time()-t0:.0f}s')
ctx.save('r2-stage1.json', {'source': str(source), 'shape': list(F.shape), 'seconds': time.time()-t0,
                            'features_sha256': hashlib.sha256(F.tobytes()).hexdigest(), 'model': run_r2.MODEL_ID})'''),
    code('''# Ô 6 — GIAI ĐOẠN 2 (CPU): PCA + ridge từng fold/seed, cổng tái lập M3 = 0,8208, so ghép cặp theo cụm
if SMOKE:
    print('SMOKE: dừng trước giai đoạn 2.')
else:
    t0 = time.time()
    oof, meta = run_r2.fit_all(data, F)
    run_r2.save_oof(ctx.out / 'r2-oof.npz', oof)
    res = run_r2.summarize(oof, data, gates=ctx.gates)
    res['meta'] = meta; res['seconds_stage2'] = time.time() - t0
    res['runner_sha256'] = hashlib.sha256(open(run_r2.__file__, 'rb').read()).hexdigest()
    ctx.gates.assert_all()
    ctx.save('results.json', res)
    print('\\nKẾT LUẬN THEO PROTOCOL §3:', res['verdict'])'''),
    code('''# Ô 7 — nén kết quả để tải về
ctx.finalize()'''),
]
nb = write_notebook(HERE / 'r2-esm.ipynb', cells, title='R2 ESM-2 features')
print(nb, validate(nb))
