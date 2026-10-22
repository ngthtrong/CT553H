"""Sinh 00-reproduce.ipynb (đã sạch outputs). Chạy: python3 -I build_notebook.py ; rồi stamp_protocol.py."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'notebook-kit-2026-10-22'))
from nbbuild import md, code, write_notebook, BOOTSTRAP, validate   # noqa: E402

EXP = 'r0-reproduce-notebook-2026-10-22'
cells = [
    md('''# R0 — Tái lập mốc đã biết trong môi trường notebook

**Mục đích:** kiểm môi trường Kaggle/Colab tái lập đúng các con số đã đo cục bộ (ridge M3 0,8082 / 0,8208; `predict.py` khớp runner < 1e-9).
Không huấn luyện mô hình mới. Tiêu chí chốt trước: `research/r0-reproduce-notebook-2026-10-22/PROTOCOL.md` (SHA-256 nhúng ở ô 1).

**Cách chạy:** xem `research/notebook-kit-2026-10-22/RUN.md`. Gắn 2 dataset (`degron-code-*`, `degron-data-v1`), **không cần GPU**, Internet tắt cũng được. Chọn *Run All*.
Kết quả: `/kaggle/working/out/r0-results.zip` (tải về, giải nén vào `research/r0-reproduce-notebook-2026-10-22/run-<nền-tảng>/`).'''),
    code('''# Ô 1 — tham số (đừng sửa PROTOCOL_SHA256 bằng tay; dùng stamp_protocol.py)
PROTOCOL_SHA256 = "__STAMP__"
RUN_VERIFY = True          # cổng B: calibration-p6/verify.py (cần ~1-2 phút CPU)
RUN_FULL_CURVE = False     # tuỳ chọn C: chạy lại toàn bộ run_curve.main() (~10-20 phút CPU)'''),
    code(BOOTSTRAP),
    code('''# Ô 3 — ghép cây thư mục, kiểm SHA-256 dữ liệu, kiểm PROTOCOL, ghi môi trường
ctx = nbkit.setup('R0', protocol='research/r0-reproduce-notebook-2026-10-22/PROTOCOL.md',
                  protocol_sha256=PROTOCOL_SHA256, needs=['R0'], threads=2, seeds=[17])
import json; print(json.dumps(ctx.env['packages'], indent=1))'''),
    code('''# Ô 4 — chạy các cổng (hàm nằm trong run_r0.py; notebook chỉ gọi)
ctx.add_to_path('r0-reproduce-notebook-2026-10-22')
import run_r0
res = run_r0.run(ctx, run_verify=RUN_VERIFY, run_full_curve=RUN_FULL_CURVE)'''),
    code('''# Ô 5 — bảng cổng và kết luận theo đúng PROTOCOL §3 (không diễn giải thêm)
gd = ctx.gates.to_dict()
for g in gd['gates']:
    print(f"{'ĐẠT ' if g['pass'] else 'HỎNG'}  {g['name']:34s} quan sát {g['observed']:.6f}  mốc {g['expected']:.6f}  |Δ|={g['abs_diff']:.2e}  (≤ {g['tol']:g})")
core = [g for g in gd['gates'] if not g['name'].startswith('full_gate_no_pap')]
print()
print('R0 ĐẠT' if all(g['pass'] for g in core) else 'R0 HỎNG: ' + ', '.join(g['name'] for g in core if not g['pass']))'''),
    code('''# Ô 6 — ghi kết quả và nén để tải về
ctx.save('results.json', res)
ctx.finalize(files=['research/calibration-p6-2026-10-22/verify.json'])'''),
]
nb = write_notebook(HERE / '00-reproduce.ipynb', cells, title='R0 reproduce')
print(nb, validate(nb))
