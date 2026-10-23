"""Sinh r1-degformer-clean.ipynb (sạch outputs). Chạy:
  python3 -I build_notebook.py && python3 -I ../notebook-kit-2026-10-22/stamp_protocol.py r1-degformer-clean.ipynb PROTOCOL.md
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'notebook-kit-2026-10-22'))
from nbbuild import md, code, write_notebook, BOOTSTRAP, validate   # noqa: E402

EXP = 'r1-degformer-clean-2026-10-22'
cells = [
    md('''# R1 — Degformer sạch cụm (điều kiện G2 còn thiếu)

Huấn luyện lại kiến trúc Degformer đã công bố trên bảng 569.270 dòng **sau khi loại các hàng chạm cụm outer-test** của từng fold,
rồi chấm ΔPSI = pred(mutant) − pred(WT) trên 47.847 ô outer-test của G2 và so ghép cặp với ridge M3 (ext 4,0).
Tiêu chí chốt trước: `research/r1-degformer-clean-2026-10-22/PROTOCOL.md` (SHA-256 nhúng ở ô 1; notebook dừng nếu file đổi).

**Cách chạy (Kaggle):**
1. New Notebook → *File → Import* file này; gắn 2 dataset riêng tư: `degron-code-*` và `degron-data-v1` (xem `research/notebook-kit-2026-10-22/RUN.md`).
2. *Settings → Accelerator → GPU T4 ×2 hoặc P100*; Internet có thể tắt (không cần tải gì).
3. Ô 1: giữ `SEEDS = [17, 29, 43]`. Trước khi chạy hết, đọc dòng **benchmark** ở ô 5 (ước lượng giờ GPU); nếu vượt hạn mức tuần thì dừng, chạy `SEEDS = [17]` rồi các seed còn lại ở phiên khác.
4. *Run All*. Mỗi (seed, fold) xong là lưu điểm + checkpoint, và nén `/kaggle/working/out/r1-results.zip` — tải được ngay cả khi phiên bị ngắt.
5. Giải nén vào `research/r1-degformer-clean-2026-10-22/run-<phiên>/`; gộp nhiều phiên bằng `aggregate_r1.py` (CPU, vài giây).

`SMOKE = True` chỉ chạy 1 epoch trên 20.000 dòng để kiểm đường code; **không** dùng kết quả SMOKE.'''),
    code('''# Ô 1 — tham số (đừng sửa PROTOCOL_SHA256 bằng tay; dùng stamp_protocol.py)
PROTOCOL_SHA256 = "__STAMP__"
SEEDS = [17, 29, 43]       # thứ tự ưu tiên chốt ở PROTOCOL §4
FOLDS = [0, 1, 2, 3, 4]
SMOKE = False'''),
    code(BOOTSTRAP),
    code('''# Ô 3 — ghép cây thư mục, kiểm SHA-256 dữ liệu, kiểm PROTOCOL, kiểm GPU
ctx = nbkit.setup('R1', protocol='research/r1-degformer-clean-2026-10-22/PROTOCOL.md',
                  protocol_sha256=PROTOCOL_SHA256, needs=['R1'], threads=2, seeds=[SEEDS[0]],
                  require_gpu=not SMOKE)
import json; print(json.dumps({k: ctx.env.get(k) for k in ('gpus', 'cuda', 'mem_gb')}, indent=1))'''),
    code('''# Ô 4 — chạy R1: cổng tự kiểm → benchmark → huấn luyện từng (seed, fold). Logic nằm ở run_r1.py.
ctx.add_to_path('r1-degformer-clean-2026-10-22')
import run_r1
inp = run_r1.run(ctx, seeds=SEEDS, folds=FOLDS, smoke=SMOKE)'''),
    code('''# Ô 5 — gộp seed đã xong, so ghép cặp theo cụm với ridge ext 4,0, in kết luận theo PROTOCOL §6
import aggregate_r1
if SMOKE:
    print('SMOKE: bỏ qua tổng hợp (kết quả SMOKE không dùng được).')
else:
    aggregate_r1.main([ctx.out], out_path=ctx.out / 'results.json')'''),
    code('''# Ô 6 — nén kết quả để tải về
ctx.finalize()'''),
]
nb = write_notebook(HERE / 'r1-degformer-clean.ipynb', cells, title='R1 Degformer sạch cụm')
print(nb, validate(nb))
