#!/usr/bin/env python3
"""Sinh ví dụ ma trận 28x20 cho **slide 16** của bộ slide buổi gặp 16/10/2026.

Việc số 2 trong "Việc phải làm trước khi dựng slide" của
`presentation/slide-content-2026-10-15.md`: chọn một peptide degron trong bộ bão hòa,
xuất **nhãn đo được** (không phải dự đoán của mô hình) thành:

  * `example-matrix.json` — số liệu + xuất xứ (SHA-256 của hai file đầu vào)
  * `--out-svg` (tuỳ chọn) — heatmap 28x20 + bar per-position, bảng màu của bộ slide

**Nhãn bằng chứng: tự đo.** Mọi giá trị sinh từ `data/processed/psi-sat_{a,b}.tsv`,
qua đúng bộ nạp dùng chung `residue-task-derisk-2026-10-15/residue_data.py`, nên các
ngưỡng (reads >= 10, degron nếu PSI WT <= 3,0, ô dương nếu dPSI >= 1,0) khớp với mọi
con số đã công bố nội bộ của đề tài.

**Về chuyện train/test.** Brief yêu cầu "chọn peptide trong tập train". Trong thiết kế
hiện hành (học trục ngữ cảnh trên bộ quét, xác nhận ma trận trên bộ bão hòa) thì **cả 91
peptide bão hòa đều nằm phía đánh giá** — không tồn tại peptide bão hòa "trong tập train".
Script vì vậy **ghi rõ trạng thái split** của peptide được chọn thay vì giả định một tập
train không có thật. Slide 16 chỉ hiện **nhãn đo được**, không có đầu ra mô hình, nên
không có rò rỉ nào xảy ra; caption phải nói đúng điều đó.

Quy tắc chọn peptide, cố định và tái lập được (không chọn tay):
  1. chỉ peptide degron của bộ bão hòa (PSI WT <= 3,0, đã lọc sẵn trong bộ nạp);
  2. phải đo đủ >= 500 ô trong tổng 28x19 ô khác WT;
  3. xếp theo **số ô dương** (dPSI >= 1,0) giảm dần, rồi theo id tăng dần;
  4. lấy phần tử đầu.

Chạy:
    .venv/bin/python topics/degron-footprint/research/slide-figures-2026-10-15/make_example_matrix.py \
        --out-svg topics/degron-footprint/presentation/deck-2026-10-16/figures/example-matrix.svg
"""

import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())
HERE = Path(__file__).resolve().parent
DERISK = TOPIC / "research/residue-task-derisk-2026-10-15"
sys.path.insert(0, str(DERISK))

import residue_data as rd  # noqa: E402  (phải chèn sys.path trước)

MIN_CELLS = 500
AAS = rd.AAS

# bảng màu của bộ slide (slide-content, mục "Phong cách thiết kế")
C_DEGRON = "#D1495B"    # dPSI < 0: đột biến làm peptide kém bền hơn
C_STABLE = "#2A9D8F"    # dPSI > 0: đột biến làm peptide bền hơn -> residue thuộc degron
C_INK = "#15323F"
C_MUTED = "#8FA3AD"
C_PAPER = "#FAFBFC"

# nhóm hoá tính của 20 acid amin, dùng cho trục x của heatmap
AA_GROUPS = [
    ("hydrophobic", "AVLIMFWP"),
    ("polar", "STNQCGY"),
    ("acidic", "DE"),
    ("basic", "KRH"),
]
AA_ORDER = "".join(aas for _, aas in AA_GROUPS)
assert sorted(AA_ORDER) == sorted(AAS), "thứ tự acid amin phải phủ đúng 20 loại"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pick_peptide(sat):
    """Quy tắc chọn cố định; trả về (peptide, thống kê)."""
    ranked = []
    for pep, v in sat.items():
        cells = v["cells"]
        if len(cells) < MIN_CELLS:
            continue
        mean = {k: (a + b) / 2 for k, (a, b) in cells.items()}
        n_pos = sum(1 for d in mean.values() if d >= rd.RESCUE_DELTA)
        ranked.append((-n_pos, pep))
    if not ranked:
        raise SystemExit("không peptide nào đạt ngưỡng số ô đo được")
    ranked.sort()
    return ranked[0][1]


def build_record(pep, v, clusters, scan_clusters):
    cells = {k: (a + b) / 2 for k, (a, b) in v["cells"].items()}
    seq = v["seq"]
    acc = rd.accession(pep)
    cluster = clusters.get(acc, acc)

    matrix = []          # [pos][aa] -> dPSI hoặc None
    for pos in range(1, rd.TILE_LEN + 1):
        row = {}
        for aa in AA_ORDER:
            if aa == seq[pos - 1]:
                row[aa] = None          # ô WT: không có thay thế
            else:
                d = cells.get((pos, aa))
                row[aa] = round(d, 4) if d is not None else None
        matrix.append(row)

    per_position = []
    for pos in range(1, rd.TILE_LEN + 1):
        vals = [d for aa, d in matrix[pos - 1].items() if d is not None]
        per_position.append({
            "pos": pos,
            "wt": seq[pos - 1],
            "n_measured": len(vals),
            "mean_dpsi": round(statistics.mean(vals), 4) if vals else None,
            "n_positive": sum(1 for d in vals if d >= rd.RESCUE_DELTA),
        })

    measured = [d for row in matrix for d in row.values() if d is not None]
    return {
        "peptide": pep,
        "accession": acc,
        "gene": pep.split("_")[1],
        "tile": int(pep.split("_")[-1]),
        "sequence": seq,
        "protein_cluster": cluster,
        "cluster_also_in_scanning_set": cluster in scan_clusters,
        "psi_wt_internal": round(v["psi_wt"], 4),
        "psi_wt_replicates": {k: round(x, 4) for k, x in v["wt_internal"].items()},
        "psi_wt_external_scan": (round(v["psi_wt_external"], 4)
                                 if v["psi_wt_external"] is not None else None),
        "n_cells_measured": len(measured),
        "n_cells_positive": sum(1 for d in measured if d >= rd.RESCUE_DELTA),
        "dpsi_min": round(min(measured), 4),
        "dpsi_max": round(max(measured), 4),
        "aa_order": AA_ORDER,
        "aa_groups": [{"name": n, "aas": a} for n, a in AA_GROUPS],
        "matrix": matrix,
        "per_position": per_position,
    }


# ------------------------------------------------------------------ vẽ SVG

def colour(d, vmax):
    """dPSI -> màu. dương = bền hơn = xanh mòng; âm = kém bền = đỏ san hô."""
    if d is None:
        return "none"
    t = max(-1.0, min(1.0, d / vmax))
    base = C_STABLE if t >= 0 else C_DEGRON
    r, g, b = (int(base[i:i + 2], 16) for i in (1, 3, 5))
    k = abs(t)
    # trộn về nền trắng ngà theo độ lớn
    pr, pg, pb = (int(C_PAPER[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (round(pr + (r - pr) * k),
                              round(pg + (g - pg) * k),
                              round(pb + (b - pb) * k))


def render_svg(rec):
    # ô rộng hơn cao: ma trận 28 hàng x 20 cột vốn gần vuông, nhưng slide 16:9 thì
    # thấp và rộng, nên giãn ngang để hình dùng hết khung mà không phải thu nhỏ chữ
    cell_w, cell_h = 24, 15
    left, top = 74, 104
    n_pos, n_aa = rd.TILE_LEN, len(AA_ORDER)
    grid_w, grid_h = n_aa * cell_w, n_pos * cell_h
    bar_x = left + grid_w + 44
    bar_w = 170
    width = bar_x + bar_w + 92
    height = top + grid_h + 112

    vmax = max(abs(rec["dpsi_min"]), abs(rec["dpsi_max"]))
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="Inter, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{C_PAPER}"/>',
        f'<text x="20" y="28" font-size="15" font-weight="700" fill="{C_INK}">'
        f'{rec["gene"]} tile {rec["tile"]} — measured &#916;PSI, 28 positions &#215; 20 amino acids</text>',
        f'<text x="20" y="48" font-size="11" fill="{C_MUTED}">'
        f'{rec["accession"]} &#183; wild-type PSI {rec["psi_wt_internal"]:.2f} '
        f'(low = degraded = degron) &#183; {rec["n_cells_measured"]} cells measured, '
        f'{rec["n_cells_positive"]} stabilising &#183; mean of two independent halves</text>',
        f'<text x="20" y="66" font-size="10" fill="{C_MUTED}" font-style="italic">'
        f'own measurement from Zhang et al. 2023 raw counts &#183; no model output on this slide</text>',
    ]

    # nhãn nhóm hoá tính trên trục x
    x = left
    for name, aas in AA_GROUPS:
        w = len(aas) * cell_w
        out.append(f'<line x1="{x}" y1="{top - 24}" x2="{x + w}" y2="{top - 24}" '
                   f'stroke="{C_MUTED}" stroke-width="1"/>')
        out.append(f'<text x="{x + w / 2}" y="{top - 29}" font-size="9" fill="{C_MUTED}" '
                   f'text-anchor="middle">{name}</text>')
        x += w
    for j, aa in enumerate(AA_ORDER):
        out.append(f'<text x="{left + j * cell_w + cell_w / 2}" y="{top - 7}" font-size="10" '
                   f'font-family="JetBrains Mono, monospace" fill="{C_INK}" '
                   f'text-anchor="middle">{aa}</text>')

    # ô ma trận
    for i, row in enumerate(rec["matrix"]):
        pos = i + 1
        wt = rec["sequence"][i]
        y = top + i * cell_h
        out.append(f'<text x="{left - 26}" y="{y + cell_h - 4}" font-size="9" fill="{C_MUTED}" '
                   f'text-anchor="end">{pos}</text>')
        out.append(f'<text x="{left - 10}" y="{y + cell_h - 4}" font-size="10" '
                   f'font-family="JetBrains Mono, monospace" font-weight="600" '
                   f'fill="{C_INK}" text-anchor="end">{wt}</text>')
        for j, aa in enumerate(AA_ORDER):
            d = row[aa]
            cx = left + j * cell_w
            if aa == wt:
                out.append(f'<rect x="{cx}" y="{y}" width="{cell_w}" height="{cell_h}" '
                           f'fill="none" stroke="{C_INK}" stroke-width="1.4"/>')
            elif d is None:
                out.append(f'<rect x="{cx}" y="{y}" width="{cell_w}" height="{cell_h}" '
                           f'fill="#FFFFFF" stroke="#E4E9EC" stroke-width=".5"/>')
                out.append(f'<line x1="{cx + 5}" y1="{y + cell_h - 3}" x2="{cx + cell_w - 5}" '
                           f'y2="{y + 3}" stroke="#D6DDE2" stroke-width="1"/>')
            else:
                out.append(f'<rect x="{cx}" y="{y}" width="{cell_w}" height="{cell_h}" '
                           f'fill="{colour(d, vmax)}" stroke="#FFFFFF" stroke-width=".5"/>')

    # bar per-position
    pos_vals = [p["mean_dpsi"] or 0.0 for p in rec["per_position"]]
    pmax = max(abs(min(pos_vals)), abs(max(pos_vals))) or 1.0
    zero = bar_x + bar_w * (0 - (-pmax)) / (2 * pmax)
    out.append(f'<text x="{bar_x}" y="{top - 7}" font-size="10" fill="{C_MUTED}">'
               f'mean &#916;PSI per position</text>')
    out.append(f'<line x1="{zero}" y1="{top}" x2="{zero}" y2="{top + grid_h}" '
               f'stroke="{C_MUTED}" stroke-width="1" stroke-dasharray="3 2"/>')
    for i, p in enumerate(rec["per_position"]):
        v = p["mean_dpsi"] or 0.0
        w = bar_w * abs(v) / (2 * pmax)
        y = top + i * cell_h + 2
        x0 = zero if v >= 0 else zero - w
        fill = C_STABLE if v >= 0 else C_DEGRON
        out.append(f'<rect x="{x0}" y="{y}" width="{max(w, 0.6)}" height="{cell_h - 4}" '
                   f'fill="{fill}" opacity="{0.95 if abs(v) >= 1.0 else 0.5}"/>')
        if abs(v) >= 1.0:
            out.append(f'<text x="{zero + bar_w / 2 + 10}" y="{y + cell_h - 4}" font-size="8.5" '
                       f'font-weight="700" fill="{C_INK}">{v:+.2f}</text>')

    # thang màu
    cb_y = top + grid_h + 30
    out.append(f'<text x="{left}" y="{cb_y - 8}" font-size="10" fill="{C_MUTED}">'
               f'&#916;PSI = PSI(substituted) &#8722; PSI(wild type)</text>')
    steps = 40
    for s in range(steps):
        t = -1 + 2 * s / (steps - 1)
        out.append(f'<rect x="{left + s * 6}" y="{cb_y}" width="6" height="11" '
                   f'fill="{colour(t * vmax, vmax)}"/>')
    out.append(f'<text x="{left}" y="{cb_y + 25}" font-size="9" fill="{C_DEGRON}">'
               f'&#8722;{vmax:.1f} destabilised</text>')
    out.append(f'<text x="{left + steps * 6}" y="{cb_y + 25}" font-size="9" fill="{C_STABLE}" '
               f'text-anchor="end">stabilised +{vmax:.1f}</text>')
    out.append(f'<text x="{left}" y="{cb_y + 42}" font-size="9.5" fill="{C_INK}">'
               f'a stabilising substitution means the wild-type residue '
               f'<tspan font-weight="700">was carrying</tspan> the degron</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-json", default=str(HERE / "example-matrix.json"))
    ap.add_argument("--out-svg", default=None)
    args = ap.parse_args()

    data = rd.load_all()
    sat, clusters = data["sat"], data["clusters"]
    scan_clusters = {clusters.get(rd.accession(p), rd.accession(p)) for p in data["scan"]}

    pep = pick_peptide(sat)
    rec = build_record(pep, sat[pep], clusters, scan_clusters)
    rec["provenance"] = {
        "generated_by": "research/slide-figures-2026-10-15/make_example_matrix.py",
        "loader": "research/residue-task-derisk-2026-10-15/residue_data.py",
        "inputs": {
            name: {"path": f"data/processed/psi-{name}.tsv",
                   "sha256": sha256(rd.PROC / f"psi-{name}.tsv")}
            for name in ("sat_a", "sat_b")
        },
        "thresholds": {"read_min": rd.READ_MIN, "degron_psi_max": rd.DEGRON_PSI_MAX,
                       "rescue_delta": rd.RESCUE_DELTA, "min_cells": MIN_CELLS},
        "selection_rule": ("peptide degron bão hòa, >= %d ô đo được, nhiều ô dương nhất, "
                           "hoà thì lấy id nhỏ nhất" % MIN_CELLS),
        "split_note": ("Cả 91 peptide bão hòa nằm phía đánh giá của thiết kế cross-source. "
                       "Slide 16 chỉ hiện nhãn đo được, không có đầu ra mô hình."),
        "n_saturation_peptides": len(sat),
    }

    Path(args.out_json).write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")
    print(f"ghi {args.out_json}")
    if args.out_svg:
        out = Path(args.out_svg)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_svg(rec), encoding="utf-8")
        print(f"ghi {args.out_svg}")

    print(f"peptide {rec['peptide']} · PSI WT {rec['psi_wt_internal']} · "
          f"{rec['n_cells_measured']} ô · {rec['n_cells_positive']} ô dương · "
          f"cụm {rec['protein_cluster']} (trong bộ quét: {rec['cluster_also_in_scanning_set']})")


if __name__ == "__main__":
    main()
