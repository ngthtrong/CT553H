#!/usr/bin/env python3
"""Phần A — nhãn của bộ quét và bộ bão hòa có CÙNG THANG không? Chỉ đọc, không huấn luyện.

Hai bộ chia sẻ một số peptide (cùng tên `<acc>_<gene>_<tile>`). Với peptide chung, bộ quét
thay vị trí `pos` bằng MỘT acid amin `aa`; bộ bão hòa có ô `(pos, aa)` đúng acid amin đó.
Vậy có những **đột biến giống hệt nhau được đo hai lần, ở hai thí nghiệm** — cho phép đo
trực tiếp "nhãn so với nhãn", không cần mô hình.

Chạy từ gốc repo:
  .venv/bin/python -I topics/degron-footprint/research/scan-sat-merge-2026-10-23/audit_labels.py
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / "data" / "README.md").exists())
sys.path.insert(0, str(TOPIC / "research/residue-task-derisk-2026-10-15"))
import residue_data as rd  # noqa: E402

RESCUE = rd.RESCUE_DELTA


def auroc(score, label):
    score, label = np.asarray(score, float), np.asarray(label, bool)
    n1, n0 = int(label.sum()), int((~label).sum())
    if n1 == 0 or n0 == 0:
        return None
    r = rankdata(score)
    return float((r[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def kappa(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    po = float((a == b).mean())
    pe = float(a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()))
    return None if pe == 1 else (po - pe) / (1 - pe)


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1])


def pair_stats(x, y, label_x=None, label_y=None):
    """x = nhãn nguồn 1, y = nhãn nguồn 2 trên cùng ô."""
    slope = float(np.polyfit(x, y, 1)[0])
    out = {"n": int(len(x)), "pearson": pearson(x, y), "spearman": float(spearmanr(x, y).statistic),
           "mean_x": float(np.mean(x)), "mean_y": float(np.mean(y)),
           "mean_diff_y_minus_x": float(np.mean(y) - np.mean(x)),
           "sd_x": float(np.std(x)), "sd_y": float(np.std(y)),
           "ols_slope_y_on_x": slope,
           "pos_rate_x": float((x >= RESCUE).mean()), "pos_rate_y": float((y >= RESCUE).mean()),
           "kappa_binary": kappa(x >= RESCUE, y >= RESCUE),
           "auroc_x_predicts_y_label": auroc(x, y >= RESCUE),
           "auroc_y_predicts_x_label": auroc(y, x >= RESCUE)}
    return out


def main():
    seqs, subs = rd.load_scan_csv()
    uniprot = rd.load_uniprot()
    cond = {c: rd.load_psi(c) for c in ("rep1", "rep2", "wt")}
    sat_a, sat_b = rd.load_psi("sat_a"), rd.load_psi("sat_b")
    # bão hòa SAU lọc kỹ thuật, KHÔNG áp ngưỡng degron (235 peptide)
    sat_all = rd.build_saturation(sat_a, sat_b, seqs, uniprot, degron_psi_max=99.0)
    rep = rd.load_clusters()

    out = {"note": "Phần A: so nhãn quét với nhãn bão hòa trên CÙNG đột biến (peptide, vị trí, acid amin). "
                   "Đọc từ psi-{rep1,rep2,wt,sat_a,sat_b}.tsv; không huấn luyện."}

    # ---------------------------------------------------------- 1. peptide chung
    scan_has_wt = {p[:-5] for p in cond["rep1"] if p.endswith("_mut0")}
    shared = sorted(set(sat_all) & scan_has_wt)
    out["overlap"] = {
        "saturation_after_technical_filter": len(sat_all),
        "scanning_peptides_with_wt_in_rep1": len(scan_has_wt),
        "shared_peptides": len(shared),
        "shared_clusters_cov80": len({rep.get(rd.accession(p), rd.accession(p)) for p in shared}),
        "saturation_clusters_cov80": len({rep.get(rd.accession(p), rd.accession(p)) for p in sat_all}),
    }

    # ---------------------------------------------------------- 2. ô trùng nhau
    cells = []  # mỗi ô: dict
    for pep in shared:
        sat = sat_all[pep]
        seq = sat["seq"]
        wt_rep = {c: cond[c].get(f"{pep}_mut0") for c in cond}
        for pos in range(1, rd.TILE_LEN + 1):
            mut_seq = subs.get((pep, pos))
            if not mut_seq or len(mut_seq) < pos:
                continue
            aa = mut_seq[pos - 1]
            key = (pos, aa)
            if aa not in rd.AAS or key not in sat["cells"] or seq[pos - 1] == aa:
                continue
            row = {"pep": pep, "pos": pos, "wt_aa": seq[pos - 1], "aa": aa,
                   "psi_wt_sat": sat["psi_wt"],
                   "sat_a": sat["cells"][key][0], "sat_b": sat["cells"][key][1]}
            for c in cond:
                v, w = cond[c].get(f"{pep}_mut{pos}"), wt_rep[c]
                row[f"scan_{c}"] = None if (v is None or w is None) else v - w
            cells.append(row)
    out["shared_cells"] = {"n_cells_with_both_assays_any_condition": len(cells),
                           "mutant_aa_in_scanning": dict(Counter(r["aa"] for r in cells).most_common())}

    def sel(rows, *keys):
        rows = [r for r in rows if all(r[k] is not None for k in keys)]
        return rows, [np.array([r[k] for r in rows], float) for k in keys]

    out["agreement"] = {}
    for tag, wt_max in (("all_shared", 99.0), ("degron_psi_wt_le_4.0", 4.0), ("degron_psi_wt_le_3.0", 3.0)):
        sub = [r for r in cells if r["psi_wt_sat"] <= wt_max]
        block = {"n_peptides": len({r["pep"] for r in sub}), "n_cells": len(sub)}
        for c in ("rep1", "rep2", "wt"):
            rows, (s, a, b) = sel(sub, f"scan_{c}", "sat_a", "sat_b")
            if len(rows) < 30:
                block[f"scan_{c}_vs_sat"] = {"n": len(rows)}
                continue
            sat = (a + b) / 2
            block[f"scan_{c}_vs_sat"] = pair_stats(s, sat)
            # theo peptide: tương quan trong peptide, trung bình
            per = []
            for pep in sorted({r["pep"] for r in rows}):
                idx = [i for i, r in enumerate(rows) if r["pep"] == pep]
                if len(idx) >= 8:
                    v = spearmanr(s[idx], sat[idx]).statistic
                    if not math.isnan(v):
                        per.append(float(v))
            block[f"scan_{c}_vs_sat"]["within_peptide_spearman_mean"] = (
                float(np.mean(per)) if per else None)
            block[f"scan_{c}_vs_sat"]["n_peptides_with_ge8_cells"] = len(per)
        rows, (s1, s2) = sel(sub, "scan_rep1", "scan_rep2")
        if len(rows) >= 30:
            block["ceiling_scan_rep1_vs_rep2"] = pair_stats(s1, s2)
        rows, (a, b) = sel(sub, "sat_a", "sat_b")
        block["ceiling_sat_half_a_vs_half_b"] = pair_stats(a, b)
        out["agreement"][tag] = block

    # ---------------------------------------------------------- 3. mốc WT: nội tại vs đo trực tiếp
    wt_rows = []
    for pep in shared:
        w = {c: cond[c].get(f"{pep}_mut0") for c in cond}
        wt_rows.append((pep, sat_all[pep]["psi_wt"], w))
    out["wt_reference"] = {}
    for c in cond:
        ok = [(a, w[c]) for _, a, w in wt_rows if w[c] is not None]
        a = np.array([x for x, _ in ok]); b = np.array([y for _, y in ok])
        out["wt_reference"][f"sat_internal_median_vs_scan_{c}_mut0"] = {
            "n_peptides": len(ok), "pearson": pearson(a, b),
            "spearman": float(spearmanr(a, b).statistic),
            "mean_diff_scan_minus_sat": float(np.mean(b) - np.mean(a)),
            "sd_diff": float(np.std(b - a)),
            "frac_abs_diff_gt_0.5": float((np.abs(b - a) > 0.5).mean())}

    # ---------------------------------------------------------- 4. thiết kế thay thế của bộ quét
    out["scanning_design"] = {}
    for thr in (3.0, 4.0):
        scan = rd.build_scanning(cond["rep1"], seqs, subs, degron_psi_max=thr)
        cnt = Counter(aa for v in scan.values() for (aa, _) in v["cells"].values())
        pairs = Counter((v["seq"][pos - 1], aa) for v in scan.values()
                        for pos, (aa, _) in v["cells"].items())
        n = sum(cnt.values())
        pos_rate_R = None
        top_aa, top_n = cnt.most_common(1)[0]
        out["scanning_design"][f"psi_wt_le_{thr}"] = {
            "n_peptides": len(scan), "n_cells": n,
            "n_clusters_cov80": len({rep.get(rd.accession(p), rd.accession(p)) for p in scan}),
            "top_mutant_aa": top_aa, "top_mutant_aa_fraction": top_n / n,
            "mutant_aa_counts": dict(cnt.most_common()),
            "distinct_wt_mut_pairs_observed": len(pairs),
            "distinct_pairs_possible_in_saturation": 380,
        }

    # ---------------------------------------------------------- 5. tỉ lệ ô dương: cùng peptide, cùng loại thay thế
    sat3 = {p: v for p, v in sat_all.items() if v["psi_wt"] <= 3.0}
    all_cells = [(a + b) / 2 for v in sat3.values() for (a, b) in v["cells"].values()]
    r_cells = [(a + b) / 2 for v in sat3.values() for (pos, aa), (a, b) in v["cells"].items() if aa == "R"]
    out["positive_rate_decomposition"] = {
        "saturation_psi_wt_le_3.0_all_19_substitutions": {"n": len(all_cells), "pos_rate": float(np.mean(np.array(all_cells) >= RESCUE))},
        "saturation_psi_wt_le_3.0_only_to_R": {"n": len(r_cells), "pos_rate": float(np.mean(np.array(r_cells) >= RESCUE))},
        "scanning_psi_wt_le_3.0": {"pos_rate": 0.0895, "source": "ladder.json"},
    }

    (HERE / "audit-labels.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out["overlap"], indent=1))
    for k, v in out["agreement"].items():
        r1 = v.get("scan_rep1_vs_sat", {})
        print(k, v["n_peptides"], v["n_cells"], {kk: (round(vv, 4) if isinstance(vv, float) else vv)
                                                  for kk, vv in r1.items() if kk in ("n", "pearson", "spearman", "ols_slope_y_on_x", "mean_diff_y_minus_x", "kappa_binary", "auroc_x_predicts_y_label")})
    print(json.dumps(out["wt_reference"], indent=1))


if __name__ == "__main__":
    main()
