"""Sinh r3-domain-gate.ipynb (sạch outputs). Chạy: python3 -I build_notebook.py ; rồi stamp_protocol.py."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'notebook-kit-2026-10-22'))
from nbbuild import md, code, write_notebook, BOOTSTRAP, validate   # noqa: E402

cells = [
    md('''# R3 — Cổng miền áp dụng cho công cụ

**Mục đích:** học hai tầng cổng trả lời *"tile này có thuộc miền `PSI(WT) ≤ 4,0` mà mô hình ΔPSI đã học không?"*:
tầng (i) ánh xạ PSI đo của sàng peptidome GPS → trạng thái miền; tầng (ii) ridge 420 đặc trưng từ trình tự → PSI → trạng thái miền.
Tiêu chí chốt trước: `research/r3-domain-gate-2026-10-22/PROTOCOL.md` (SHA-256 nhúng ở ô 1). Chỉ CPU (vài phút), **không cần GPU**.

**Trước khi chạy:** (1) R0 phải ĐẠT trong cùng loại môi trường (đặt `R0_CONFIRMED = True` ở ô 1); (2) gắn 2 dataset (`degron-code-*`, `degron-data-v1`).
Kết quả: `/kaggle/working/out/r3-results.zip` — giải nén vào `research/r3-domain-gate-2026-10-22/run-<nền-tảng>/` (xem `research/notebook-kit-2026-10-22/RUN.md`).'''),
    code('''# Ô 1 — tham số
PROTOCOL_SHA256 = "__STAMP__"
R0_CONFIRMED = False       # chỉ đặt True sau khi 00-reproduce.ipynb báo "R0 ĐẠT" ở môi trường này
SMOKE = False              # True = chạy thử nhanh trên 30.000 tile (chỉ kiểm hạ tầng, KHÔNG dùng làm kết quả)
assert R0_CONFIRMED or SMOKE, "Chạy R0 trước (PROTOCOL §4). Đặt R0_CONFIRMED = True sau khi R0 ĐẠT."'''),
    code(BOOTSTRAP),
    code('''# Ô 3 — ghép cây thư mục, kiểm SHA-256 dữ liệu, kiểm PROTOCOL
ctx = nbkit.setup('R3', protocol='research/r3-domain-gate-2026-10-22/PROTOCOL.md',
                  protocol_sha256=PROTOCOL_SHA256, needs=['R3'], threads=2)'''),
    code('''# Ô 4 — chạy (hàm nằm trong run_r3.py; notebook chỉ gọi). Vài phút CPU.
ctx.add_to_path('r3-domain-gate-2026-10-22')
import run_r3
res = run_r3.run(ctx, smoke=SMOKE)'''),
    code('''# Ô 5 — kết luận theo đúng PROTOCOL §2-§3 (không diễn giải thêm)
t1, ta, tb = res['tier1'], res['tier2_stage_A'], res['tier2_stage_B']
print('TẦNG (i)   :', 'DÙNG ĐƯỢC' if res['usable_tier1'] else 'KHÔNG ĐẠT', t1['verdict'])
print('TẦNG (ii)  :', 'DÙNG ĐƯỢC' if res['usable_tier2'] else 'KHÔNG ĐẠT', tb['verdict'])
print(f"  tầng (i)  AUROC OOF {t1['auroc_oof']:.4f}  BSS {t1['bss_oof']:.3f}  d0 lọt in-domain {t1['frac_d0_in_domain']:.3f}")
print(f"  tầng (ii) Spearman A {ta['spearman_point']:.3f}  AUROC B {tb['auroc_oof']:.4f}  BSS {tb['bss_oof']:.3f}  d0 lọt in-domain {tb['frac_d0_in_domain']:.3f}")
if SMOKE:
    print("\\n⚠ SMOKE = True: kết quả này chỉ kiểm hạ tầng, KHÔNG phải kết quả R3.")'''),
    code('''# Ô 6 — ghi gate-weights.npz, gate-card.json, results.json và nén để tải về
run_r3.write_outputs(res, ctx.out)
ctx.finalize()'''),
]
nb = write_notebook(HERE / 'r3-domain-gate.ipynb', cells, title='R3 domain gate')
print(nb, validate(nb))
