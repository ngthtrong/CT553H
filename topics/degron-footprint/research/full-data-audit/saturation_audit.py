#!/usr/bin/env python3
"""Audit bộ đột biến bão hòa Zhang 2023: ma trận 28×20 đầy tới đâu, và có lặp lại được không.

Vì sao: hướng "ma trận thay thế vị trí × amino acid" là chỗ khác biệt khả thi duy nhất của
đề tài so với DEGRONOPEDIA / MetaDegron / PAP (xem thẻ đề tài, dòng G3). Repo trước chỉ đếm
135.040 **định danh** và ghi rõ đó chưa phải số ô có ΔPSI dùng được. Giờ đã dựng được PSI cho
cả hai nửa 6-bin nên đo được: độ phủ thật của ma trận, và độ lặp lại của từng ô.

Định danh: <peptide>_mut<vị trí><chữ thường> với chữ thường là amino acid THAY VÀO.
Giả định "hai nửa S1..S6 và S7..S12 là hai replicate" được KIỂM bằng tương quan, không tin sẵn.
"""

import json
import math
import re
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
PROC = TOPIC / "data/processed"
PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)(?P<aa>[a-z])?$")
AA = "ACDEFGHIKLMNPQRSTVWY"
READ_MIN = 10
RESCUE_DELTA = 1.0


def load(condition):
    out = {}
    with (PROC / f"psi-{condition}.tsv").open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            psi, total = float(p[1]), float(p[2])
            if not math.isnan(psi):
                out[p[0]] = (psi, total)
    return out


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")


def parse(table, read_min):
    """{peptide: {(pos, aa): psi}} cộng {peptide: psi_wt}."""
    cells, wt = {}, {}
    for name, (psi, total) in table.items():
        if total < read_min:
            continue
        m = PAT.match(name)
        if not m:
            continue
        pep, pos, aa = m.group("pep"), int(m.group("pos")), m.group("aa")
        if aa is None:
            wt[pep] = psi
        else:
            cells.setdefault(pep, {})[(pos, aa.upper())] = psi
    return cells, wt


def main():
    a_raw, b_raw = load("sat_a"), load("sat_b")
    report = {"thresholds": {"read_min": READ_MIN, "rescue_delta": RESCUE_DELTA}}

    # --- 0. kiểm giả định hai nửa là hai replicate
    shared_ids = [i for i in a_raw.keys() & b_raw.keys()
                  if a_raw[i][1] >= 100 and b_raw[i][1] >= 100]
    xs = [a_raw[i][0] for i in shared_ids]
    ys = [b_raw[i][0] for i in shared_ids]
    report["half_split_check"] = {
        "n_ids_reads_ge_100_both": len(shared_ids),
        "pearson_psi": round(pearson(xs, ys), 4),
        "verdict": ("Tương quan cao thì hai nửa đúng là hai replicate của cùng thiết kế 6 bin. "
                    "Thấp thì thứ tự bin đã giả định sai và mọi số dưới đây không dùng được."),
    }

    # --- 1. độ phủ ma trận
    for rmin, tag in ((READ_MIN, "read_min_10"), (50, "read_min_50"), (100, "read_min_100")):
        cells_a, wt_a = parse(a_raw, rmin)
        cells_b, wt_b = parse(b_raw, rmin)
        peps = sorted(set(cells_a) | set(cells_b))
        union_cells = {p: set(cells_a.get(p, {})) | set(cells_b.get(p, {})) for p in peps}
        both_cells = {p: set(cells_a.get(p, {})) & set(cells_b.get(p, {})) for p in peps}
        n_union = sum(len(v) for v in union_cells.values())
        n_both = sum(len(v) for v in both_cells.values())
        positions = {p: {pos for pos, _ in union_cells[p]} for p in peps}
        max_pos = max((max(v) for v in positions.values() if v), default=0)
        # ô có ΔPSI (cần WT cùng điều kiện)
        with_d_a = sum(1 for p in cells_a for _ in cells_a[p] if p in wt_a)
        with_d_b = sum(1 for p in cells_b for _ in cells_b[p] if p in wt_b)
        n_peps_with_wt = len(set(wt_a) | set(wt_b))
        report[f"matrix_coverage_{tag}"] = {
            "n_peptides": len(peps), "max_position_seen": max_pos,
            "n_cells_union_of_halves": n_union,
            "n_cells_measured_in_both_halves": n_both,
            "n_peptides_with_wt_reference": n_peps_with_wt,
            "n_cells_with_dpsi_half_a": with_d_a, "n_cells_with_dpsi_half_b": with_d_b,
            "theoretical_max_cells_28x20": len(peps) * 28 * 20,
            "fill_rate_union": round(n_union / (len(peps) * 28 * 20), 4) if peps else None,
            "fill_rate_both_halves": round(n_both / (len(peps) * 28 * 20), 4) if peps else None,
        }

    # --- 2. độ lặp lại của ΔPSI theo ô, và của việc gọi ô là "dương"
    cells_a, wt_a = parse(a_raw, READ_MIN)
    cells_b, wt_b = parse(b_raw, READ_MIN)
    pairs, pos_a, pos_b, agree = [], 0, 0, 0
    for pep in set(cells_a) & set(cells_b):
        if pep not in wt_a or pep not in wt_b:
            continue
        for key in set(cells_a[pep]) & set(cells_b[pep]):
            da = cells_a[pep][key] - wt_a[pep]
            db = cells_b[pep][key] - wt_b[pep]
            pairs.append((da, db))
            ia, ib = da >= RESCUE_DELTA, db >= RESCUE_DELTA
            pos_a += ia
            pos_b += ib
            agree += ia and ib
    if pairs:
        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]
        diffs = [x - y for x, y in pairs]
        n = len(diffs)
        md = sum(diffs) / n
        var_diff = sum((d - md) ** 2 for d in diffs) / (n - 1)
        alld = xs + ys
        ma = sum(alld) / len(alld)
        var_obs = sum((x - ma) ** 2 for x in alld) / (len(alld) - 1)
        report["cell_reproducibility"] = {
            "n_cells_compared": n, "pearson_dpsi": round(pearson(xs, ys), 4),
            "mean_diff": round(md, 4), "sd_noise_single_half": round(math.sqrt(var_diff / 2), 4),
            "var_observed_dpsi": round(var_obs, 4),
            "noise_share_of_observed_variance": round(var_diff / 2 / var_obs, 4),
            "n_positive_half_a": pos_a, "n_positive_half_b": pos_b,
            "n_positive_in_both": agree,
            "jaccard_positive_cells": round(agree / (pos_a + pos_b - agree), 4)
            if (pos_a + pos_b - agree) else None,
            "note": ("jaccard_positive_cells là mức trùng khớp khi gọi một Ô là dương giữa hai "
                     "nửa. Đây là trần cho bất kỳ mô hình dự đoán ô."),
        }

    # --- 3. chồng lấn với bộ scanning (peptide nào có cả hai nguồn nhãn)
    scan_peps = set()
    scan_path = PROC / "psi-rep1.tsv"
    if scan_path.exists():
        with scan_path.open(encoding="utf-8") as fh:
            next(fh)
            for line in fh:
                m = PAT.match(line.split("\t", 1)[0])
                if m:
                    scan_peps.add(m.group("pep"))
    sat_peps = set(cells_a) | set(cells_b)
    report["overlap_with_scanning"] = {
        "n_saturation_peptides": len(sat_peps),
        "n_also_in_scanning": len(sat_peps & scan_peps),
        "n_saturation_only": len(sat_peps - scan_peps),
        "implication": ("Peptide có cả hai nguồn phải nằm CÙNG phía train/test, nếu không thì "
                        "rò rỉ giữa hai nhiệm vụ. Nếu saturation được dùng để train thì không "
                        "được gọi 249 peptide là test độc lập."),
    }

    path = Path(__file__).parent / "saturation-audit.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
