"""Hinh cho trang Notion lo trinh 19/10/2026.

Moi con so doc truc tiep tu file ket qua trong research/; khong co so viet tay
ngoai bon moc bi khoa boi quyet dinh (ghi ro o HANG_SO ben duoi).

Chay:  .venv/bin/python topics/degron-footprint/presentation/notion-2026-10-19/figures.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# --- thu muc goc repo tim qua DECISIONS.md (quy uoc repo) ---
ROOT = Path(__file__).resolve()
while not (ROOT / "DECISIONS.md").exists():
    ROOT = ROOT.parent
RES = ROOT / "topics/degron-footprint/research"
OUT = Path(__file__).resolve().parent / "png"
OUT.mkdir(exist_ok=True)

# Hang so bi khoa boi quyet dinh (D-031): tran do luong cua bo bao hoa.
CEILING = 0.9519  # research/residue-task-derisk-2026-10-15/ceiling.json

sat = json.loads((RES / "g2-saturation-2026-10-18/results.json").read_text())
aud = json.loads((RES / "g2-saturation-2026-10-18/audit.json").read_text())
ext2 = json.loads((RES / "g2-extension-2026-10-18/e2-candidates.json").read_text())
ext3 = json.loads((RES / "g2-extension-2026-10-18/e3-degformer-arch.json").read_text())
ov = json.loads((RES / "g2-extension-2026-10-18/e1-overlap.json").read_text())

def vn(n):
    """Dinh dang so kieu Viet: dau cham phan nghin."""
    return f"{n:,}".replace(",", ".")


C = {
    "bg": "#FAFBFC", "ink": "#15323F", "degron": "#D1495B",
    "stable": "#2A9D8F", "model": "#386FA4", "mute": "#8FA3AD", "warn": "#E9C46A",
}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "figure.facecolor": C["bg"],
    "axes.facecolor": C["bg"], "text.color": C["ink"],
    "axes.labelcolor": C["ink"], "xtick.color": C["ink"], "ytick.color": C["ink"],
})

# ---------------------------------------------------------------- fig 1
rows = [
    ("Trần đo lường của assay\n(một nửa replicate chấm trên nửa kia)", CEILING, C["stable"], "tran"),
    ("Ridge M3 học trực tiếp trên bão hoà\n— MÔ HÌNH HIỆN TẠI", sat["macro_auroc"]["ridge"], C["model"], "ta"),
    ("FiLM  (tiền đăng ký)", ext2["macro_auroc"]["film"], C["mute"], "loai"),
    ("Bilinear  (tiền đăng ký)", ext2["macro_auroc"]["bilinear"], C["mute"], "loai"),
    ("Ridge tích chéo  (tiền đăng ký)", ext2["macro_auroc"]["cross_ridge"], C["mute"], "loai"),
    ("ΔPAP cnn2w1 — ĐỐI CHỨNG CÔNG BỐ,\nĐÍCH PHẢI VƯỢT", sat["macro_auroc"]["DeltaPAP"], C["degron"], "dich"),
    ("Kiến trúc Degformer huấn luyện lại\ndưới cov80", ext3["macro_auroc"]["degformer_arch_cov80"], C["mute"], "loai"),
]
fig, ax = plt.subplots(figsize=(12.4, 5.6))
fig.subplots_adjust(left=0.33, right=0.97, top=0.76, bottom=0.20)
ys = range(len(rows))[::-1]
for y, (lab, val, col, kind) in zip(ys, rows):
    ax.barh(y, val - 0.70, left=0.70, color=col, height=0.62,
            alpha=1.0 if kind in ("ta", "dich", "tran") else 0.55,
            edgecolor=C["bg"], linewidth=1.5)
    ax.text(val + 0.004, y, f"{val:.4f}", va="center", ha="left",
            fontsize=11.5, fontweight="bold", color=col)
ax.set_yticks(list(ys))
ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.axvline(sat["macro_auroc"]["DeltaPAP"], color=C["degron"], ls=":", lw=1.4, zorder=0)
ax.set_xlim(0.70, 0.99)
ax.set_xlabel("AUROC mức ô trên ma trận bão hoà, trung bình macro theo peptide", fontsize=11)
d = aud["ridge_vs_DeltaPAP"]
fig.text(0.015, 0.94, "Mốc số của G2 đã vượt; điều kiện kiến trúc thì chưa",
         fontsize=16, fontweight="bold", color=C["ink"])
fig.text(0.015, 0.875,
         f"ridge M3 vượt ΔPAP +{d['delta']:.4f} (CI 95% [{d['ci95'][0]:.4f}; {d['ci95'][1]:.4f}])"
         f"  ·  năm thiết kế nhiều sức chứa hơn đều thua",
         fontsize=11, color=C["mute"])
fig.text(0.015, 0.825,
         f"{sat['n_peptides']} peptide  /  {sat['n_clusters']} cụm  /  {vn(sat['n_cells'])} ô  ·  5 fold cov80, 3 seed",
         fontsize=11, color=C["mute"])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.text(0.015, 0.035, "Đo tự do · research/g2-saturation-2026-10-18/ + g2-extension-2026-10-18/",
         fontsize=9, color=C["mute"])
fig.text(0.015, 0.005, "Trần là TRẦN ĐO LƯỜNG của phép đo, không phải mức học được từ trình tự",
         fontsize=9, color=C["mute"])
fig.savefig(OUT / "fig-benchmark.png", dpi=170, facecolor=C["bg"])
plt.close(fig)

# ---------------------------------------------------------------- fig 2
fig, ax = plt.subplots(figsize=(12.4, 4.2))
fig.subplots_adjust(left=0.33, right=0.97, top=0.72, bottom=0.22)
full = ov["full"]["Degformer"]
non = ov["nonoverlap"]["Degformer"]
bars = [
    ("Degformer, checkpoint tác giả\ntrên TOÀN BỘ 47.847 ô", full, C["warn"]),
    (f"Degformer, checkpoint tác giả\ntrên {vn(ov['n_cells_held'])} ô KHÔNG trùng train", non, C["warn"]),
    ("Kiến trúc Degformer, tự huấn luyện\ndưới split cụm cov80", ext3["macro_auroc"]["degformer_arch_cov80"], C["mute"]),
    ("Ridge M3 của đề tài", sat["macro_auroc"]["ridge"], C["model"]),
]
ys = range(len(bars))[::-1]
for y, (lab, val, col) in zip(ys, bars):
    ax.barh(y, val - 0.70, left=0.70, color=col, height=0.6, edgecolor=C["bg"], linewidth=1.5)
    ax.text(val + 0.004, y, f"{val:.4f}", va="center", fontsize=11.5, fontweight="bold", color=col)
ax.set_yticks(list(ys)); ax.set_yticklabels([b[0] for b in bars], fontsize=9.5)
ax.set_xlim(0.70, 0.99)
ax.set_xlabel("AUROC mức ô, trung bình macro theo peptide", fontsize=11)
fig.text(0.015, 0.93, "Sức mạnh của Degformer nằm ở 569k dòng tiền huấn luyện, không ở kiến trúc",
         fontsize=15, fontweight="bold", color=C["ink"])
fig.text(0.015, 0.855,
         f"{ov['fraction_overlapping']*100:.2f}%".replace('.', ',') + f" ô test trùng train của nó, và cả {ov['wt_in_training']}/{ov['n_wt_peptides']} peptide WT nằm trong train.",
         fontsize=11, color=C["mute"])
fig.text(0.015, 0.795,
         "Bỏ hết ô trùng nó vẫn giữ điểm; nhưng kiến trúc đó tự học thì thua cả ΔPAP.",
         fontsize=11, color=C["mute"])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.savefig(OUT / "fig-degformer.png", dpi=170, facecolor=C["bg"])
plt.close(fig)

print("OK ->", OUT)
for p in sorted(OUT.glob("*.png")):
    print(" ", p.name, p.stat().st_size)
