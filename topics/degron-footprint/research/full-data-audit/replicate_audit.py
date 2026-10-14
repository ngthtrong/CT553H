#!/usr/bin/env python3
"""Đo độ lặp lại của nhãn degron giữa Replicate 1, Replicate 2 và mẫu BAG6 WT.

Vì sao: audit 12/10 chốt rằng 35,0% phương sai ΔPSI còn lại sau oracle thành phần *có thể*
là ngữ cảnh học được, nhưng cũng *có thể* là nhiễu đo, và không tách được vì chỉ dùng một
replicate. Giờ đã dựng được PSI cho Replicate 2 từ read thô, nên tách được.

Các phép đo:
  1. Tương quan PSI giữa các điều kiện, theo ngưỡng read.
  2. Độ lệch chuẩn nhiễu đo của ΔPSI, suy từ chênh lệch giữa hai replicate.
  3. Tỉ lệ footprint gọi lại được ở replicate độc lập (cùng định nghĩa, cùng ngưỡng).
  4. Phần 35,0% phương sai dư: bao nhiêu giải thích được bằng nhiễu đo.
  5. So BAG6 WT với hai replicate BAG6-chưa-rõ, để trả lời câu genotype còn treo.

Ngưỡng giữ nguyên audit trước: reads >= 10, PSI WT <= 3,0, >= 21 vị trí, dương nếu dPSI >= 1,0.
Chỉ đọc bảng trong data/processed/psi-*.tsv do build_psi.py sinh ra.
"""

import json
import math
import re
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())
PROC = TOPIC / "data/processed"
PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")

READ_MIN = 10
DEGRON_PSI_MAX = 3.0
RESCUE_DELTA = 1.0
MIN_POS = 21


def load(condition):
    """{id: (psi, sum)} cho các id có Sum >= READ_MIN và PSI hợp lệ."""
    out = {}
    path = PROC / f"psi-{condition}.tsv"
    with path.open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            psi, total = float(parts[1]), float(parts[2])
            if math.isnan(psi) or total < READ_MIN:
                continue
            out[parts[0]] = (psi, total)
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


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    return pearson(rank(xs), rank(ys))


def footprints(table):
    """{peptide: {pos: dpsi}} cho các peptide đạt lọc degron + độ phủ, kèm WT."""
    wt, mut = {}, {}
    for name, (psi, _) in table.items():
        m = PAT.match(name)
        if not m:
            continue
        pep, pos = m.group("pep"), int(m.group("pos"))
        if pos == 0:
            wt[pep] = psi
        else:
            mut.setdefault(pep, {})[pos] = psi
    out = {}
    for pep, w in wt.items():
        d = mut.get(pep)
        if not d or w > DEGRON_PSI_MAX or len(d) < MIN_POS:
            continue
        out[pep] = {"wt": w, "d": {p: v - w for p, v in d.items()}}
    return out


def main():
    tables = {c: load(c) for c in ("rep1", "rep2", "wt")}
    report = {"thresholds": {"read_min": READ_MIN, "degron_psi_max": DEGRON_PSI_MAX,
                             "rescue_delta": RESCUE_DELTA, "min_pos": MIN_POS},
              "n_ids_passing_reads": {c: len(t) for c, t in tables.items()}}

    # 1. tương quan PSI từng cặp điều kiện, theo ngưỡng read
    report["psi_agreement"] = {}
    for a, b in (("rep1", "rep2"), ("rep1", "wt"), ("rep2", "wt")):
        shared = tables[a].keys() & tables[b].keys()
        entry = {}
        for rmin in (10, 50, 100, 500):
            pairs = [(tables[a][i][0], tables[b][i][0]) for i in shared
                     if tables[a][i][1] >= rmin and tables[b][i][1] >= rmin]
            if len(pairs) < 10:
                continue
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            diffs = [x - y for x, y in pairs]
            n = len(diffs)
            md = sum(diffs) / n
            sd = math.sqrt(sum((d - md) ** 2 for d in diffs) / (n - 1))
            entry[f"reads_ge_{rmin}"] = {
                "n": n, "pearson": round(pearson(xs, ys), 4),
                "spearman": round(spearman(xs, ys), 4),
                "mean_diff": round(md, 4), "sd_diff": round(sd, 4),
                "mad": round(sorted(abs(d - md) for d in diffs)[n // 2], 4),
            }
        report["psi_agreement"][f"{a}_vs_{b}"] = entry

    # 2+4. nhiễu đo của dPSI và phần phương sai dư nó giải thích
    f1, f2 = footprints(tables["rep1"]), footprints(tables["rep2"])
    shared_pep = f1.keys() & f2.keys()
    pair_d = []
    for pep in shared_pep:
        for pos, d1 in f1[pep]["d"].items():
            d2 = f2[pep]["d"].get(pos)
            if d2 is not None:
                pair_d.append((d1, d2))
    n = len(pair_d)
    if n > 2:
        diffs = [a - b for a, b in pair_d]
        md = sum(diffs) / n
        var_diff = sum((d - md) ** 2 for d in diffs) / (n - 1)
        # dPSI = tín hiệu + nhiễu, hai replicate độc lập cùng phương sai nhiễu:
        # Var(d1 - d2) = 2 * Var(nhiễu)  =>  sd nhiễu một replicate:
        sd_noise = math.sqrt(var_diff / 2)
        alld = [x for p in pair_d for x in p]
        ma = sum(alld) / len(alld)
        var_obs = sum((x - ma) ** 2 for x in alld) / (len(alld) - 1)
        xs = [p[0] for p in pair_d]
        ys = [p[1] for p in pair_d]
        report["dpsi_noise"] = {
            "n_position_pairs": n, "n_peptides": len(shared_pep),
            "pearson": round(pearson(xs, ys), 4), "spearman": round(spearman(xs, ys), 4),
            "var_observed_dpsi": round(var_obs, 4),
            "sd_noise_single_replicate": round(sd_noise, 4),
            "var_noise_single_replicate": round(sd_noise ** 2, 4),
            "noise_share_of_observed_variance": round(sd_noise ** 2 / var_obs, 4),
            "residual_after_composition_oracle_rep1": 0.350,
            "noise_share_of_that_residual": round(sd_noise ** 2 / var_obs / 0.350, 4),
            "interpretation": ("Nếu tỉ lệ nhiễu trên phương sai dư gần 1 thì phần 35,0% "
                               "chủ yếu là nhiễu đo, không phải ngữ cảnh học được."),
        }

    # 3. footprint có gọi lại được ở replicate độc lập không
    def positives(f):
        return {pep: {p for p, d in v["d"].items() if d >= RESCUE_DELTA} for pep, v in f.items()}

    p1, p2 = positives(f1), positives(f2)
    fp1 = {pep for pep, s in p1.items() if s}
    fp2 = {pep for pep, s in p2.items() if s}
    both_cov = f1.keys() & f2.keys()
    jac, recovered, exact = [], 0, 0
    for pep in fp1 & both_cov:
        a, b = p1[pep], p2.get(pep, set())
        if b:
            recovered += 1
        if a == b:
            exact += 1
        union = a | b
        if union:
            jac.append(len(a & b) / len(union))
    report["footprint_reproducibility"] = {
        "n_footprint_rep1": len(fp1), "n_footprint_rep2": len(fp2),
        "n_peptides_covered_in_both": len(both_cov),
        "n_footprint_rep1_also_covered_in_rep2": len(fp1 & both_cov),
        "n_recovered_as_footprint_in_rep2": recovered,
        "recovery_rate": round(recovered / len(fp1 & both_cov), 4) if fp1 & both_cov else None,
        "n_identical_positive_set": exact,
        "mean_jaccard_of_positive_positions": round(sum(jac) / len(jac), 4) if jac else None,
        "note": ("recovery_rate là tỉ lệ peptide được gọi là footprint ở rep1 mà cũng được "
                 "gọi ở rep2 với cùng ngưỡng. Jaccard đo trùng khớp ở mức VỊ TRÍ, "
                 "là thứ mô hình phải dự đoán."),
    }

    # 5. BAG6: WT so với hai replicate chưa rõ genotype
    fw = footprints(tables["wt"])
    for other, label in ((f1, "rep1"), (f2, "rep2")):
        shared = fw.keys() & other.keys()
        pd = [(other[pep]["d"][pos], fw[pep]["d"][pos])
              for pep in shared for pos in other[pep]["d"] if pos in fw[pep]["d"]]
        if len(pd) > 2:
            xs = [p[0] for p in pd]
            ys = [p[1] for p in pd]
            report.setdefault("bag6_wt_comparison", {})[f"wt_vs_{label}"] = {
                "n_position_pairs": len(pd), "n_peptides": len(shared),
                "pearson_dpsi": round(pearson(xs, ys), 4),
                "spearman_dpsi": round(spearman(xs, ys), 4),
            }

    path = Path(__file__).parent / "replicate-audit.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
