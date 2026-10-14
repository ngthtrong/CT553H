#!/usr/bin/env python3
"""Dựng ma trận ΔPSI vị trí × amino acid cho bộ bão hòa, và đo nó có dùng được không.

Bối cảnh: hướng "ma trận 28×20" là chỗ khác biệt khả thi duy nhất của đề tài so với
DEGRONOPEDIA / MetaDegron / PAP. Nhưng bộ bão hòa **không có phép đo hoang dã nào**
(0 định danh dạng _mut0), nên ΔPSI không tự tính được.

Đường ra: thư viện bão hòa thay mỗi vị trí bằng **cả 20** amino acid, nên ô mà amino acid
thay vào trùng residue hoang dã là một phép đo WT nội tại. Mỗi peptide có 28 ô như vậy.
Cần biết trình tự peptide để xác định ô nào.

Trình tự được suy từ quy tắc tile đã khớp trên bộ scanning: peptide <ACC>_<GENE>_<n> là
28-mer của protein ACC bắt đầu ở (n-1)*23. Quy tắc này được KIỂM hai lần:
  (a) so với trình tự thật của các peptide có cả trong bộ scanning;
  (b) so PSI của 28 ô WT-nội-tại với PSI hoang dã đo ở bộ scanning.
Peptide không qua kiểm thì bị loại, không đoán.
"""

import csv
import gzip
import json
import math
import re
import statistics
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())
PROC = TOPIC / "data/processed"
RAW = TOPIC / "data/raw"
SCAN_CSV = (TOPIC / "data/interim/zhang-scanning-unzip/I28 Scanning (Completed)"
            / "Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv")
SAT_PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)(?P<aa>[a-z])$")
SCAN_PAT = re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")

TILE_STEP = 23
TILE_LEN = 28
READ_MIN = 10
RESCUE_DELTA = 1.0


def load_psi(condition, read_min=READ_MIN):
    out = {}
    with (PROC / f"psi-{condition}.tsv").open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            psi, total = float(p[1]), float(p[2])
            if not math.isnan(psi) and total >= read_min:
                out[p[0]] = psi
    return out


def load_scan_wt_sequences():
    csv.field_size_limit(10 ** 7)
    seqs = {}
    with SCAN_CSV.open(newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            m = SCAN_PAT.match(r["Gene"])
            if m and int(m.group("pos")) == 0:
                seqs[m.group("pep")] = r["AA.Seq"]
    return seqs


def load_uniprot():
    up = {}
    with gzip.open(RAW / "human-reviewed-2026-10-12.fasta.gz", "rt") as fh:
        acc, buf = None, []
        for line in fh:
            if line.startswith(">"):
                if acc:
                    up[acc] = "".join(buf)
                acc = line.split("|")[1] if "|" in line else None
                buf = []
            else:
                buf.append(line.strip())
        if acc:
            up[acc] = "".join(buf)
    return up


def derive_sequence(pep, uniprot):
    parts = pep.split("_")
    try:
        n = int(parts[-1])
    except ValueError:
        return None
    protein = uniprot.get(parts[0])
    if not protein:
        return None
    start = (n - 1) * TILE_STEP
    seq = protein[start:start + TILE_LEN]
    return seq if len(seq) == TILE_LEN else None


def main():
    sat_a, sat_b = load_psi("sat_a"), load_psi("sat_b")
    scan_seqs = load_scan_wt_sequences()
    scan_psi = load_psi("rep1")
    uniprot = load_uniprot()

    def parse(table):
        cells = {}
        for name, psi in table.items():
            m = SAT_PAT.match(name)
            if m:
                cells.setdefault(m.group("pep"), {})[
                    (int(m.group("pos")), m.group("aa").upper())] = psi
        return cells

    cells_a, cells_b = parse(sat_a), parse(sat_b)
    peptides = sorted(set(cells_a) | set(cells_b))
    report = {"n_saturation_peptides": len(peptides),
              "tile_rule": {"step": TILE_STEP, "length": TILE_LEN,
                            "start_formula": "(n-1)*step"}}

    # --- kiểm (a): quy tắc tile so với trình tự thật
    checked = {"match": 0, "mismatch": 0, "no_truth": 0, "no_derivation": 0}
    sequences, mismatches = {}, []
    for pep in peptides:
        truth = scan_seqs.get(pep)
        derived = derive_sequence(pep, uniprot)
        if truth:
            t = truth.rstrip("*").upper()
            if derived and derived[:len(t)] == t:
                checked["match"] += 1
                sequences[pep] = t
            else:
                checked["mismatch"] += 1
                if len(mismatches) < 5:
                    mismatches.append({"peptide": pep, "truth": t, "derived": derived})
        elif derived:
            checked["no_truth"] += 1
            sequences[pep] = derived
        else:
            checked["no_derivation"] += 1
    report["tile_rule_check"] = {**checked, "examples_mismatch": mismatches,
                                 "n_sequences_available": len(sequences)}

    # --- kiểm (b): ô WT-nội-tại so với PSI hoang dã của bộ scanning
    internal, cross = [], []
    for pep, seq in sequences.items():
        vals = []
        for half in (cells_a, cells_b):
            d = half.get(pep)
            if not d:
                continue
            for i, residue in enumerate(seq, start=1):
                v = d.get((i, residue))
                if v is not None:
                    vals.append(v)
        if len(vals) >= 10:
            med = statistics.median(vals)
            sd = statistics.pstdev(vals)
            internal.append({"peptide": pep, "n_wt_identity_cells": len(vals),
                             "median_psi": med, "sd_psi": sd})
            ref = scan_psi.get(f"{pep}_mut0")
            if ref is not None:
                cross.append((med, ref))
    if internal:
        report["internal_wt_reference"] = {
            "n_peptides": len(internal),
            "median_cells_per_peptide": statistics.median(
                x["n_wt_identity_cells"] for x in internal),
            "median_within_peptide_sd": round(statistics.median(
                x["sd_psi"] for x in internal), 4),
        }
    if len(cross) >= 3:
        xs = [c[0] for c in cross]
        ys = [c[1] for c in cross]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxy = sum((x - mx) * (y - my) for x, y in cross)
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        diffs = [x - y for x, y in cross]
        md = sum(diffs) / n
        report["internal_wt_reference"]["cross_check_vs_scanning_wt"] = {
            "n_peptides": n,
            "pearson": round(sxy / math.sqrt(sxx * syy), 4) if sxx and syy else None,
            "mean_diff": round(md, 4),
            "sd_diff": round(math.sqrt(sum((d - md) ** 2 for d in diffs) / (n - 1)), 4),
            "meaning": ("Pearson cao và mean_diff nhỏ thì WT nội tại dùng được làm mốc, "
                        "nên tính được ΔPSI cho CẢ các peptide không có trong bộ scanning."),
        }

    # --- ma trận ΔPSI: độ phủ và độ lặp lại theo ô
    fills, pair_cells = [], []
    pos_a = pos_b = agree = 0
    for pep, seq in sequences.items():
        refs = {}
        for tag, half in (("a", cells_a), ("b", cells_b)):
            d = half.get(pep)
            if not d:
                continue
            vals = [d[(i, r)] for i, r in enumerate(seq, start=1) if (i, r) in d]
            if len(vals) >= 10:
                refs[tag] = statistics.median(vals)
        if len(refs) < 2:
            continue
        da = {k: cells_a[pep][k] - refs["a"] for k in cells_a.get(pep, {})}
        db = {k: cells_b[pep][k] - refs["b"] for k in cells_b.get(pep, {})}
        # ô thật sự là thay thế (loại ô WT-nội-tại)
        wt_cells = {(i, r) for i, r in enumerate(seq, start=1)}
        keys = (set(da) & set(db)) - wt_cells
        fills.append(len(keys) / (TILE_LEN * 19))
        for k in keys:
            pair_cells.append((da[k], db[k]))
            ia, ib = da[k] >= RESCUE_DELTA, db[k] >= RESCUE_DELTA
            pos_a += ia
            pos_b += ib
            agree += ia and ib
    if pair_cells:
        xs = [p[0] for p in pair_cells]
        ys = [p[1] for p in pair_cells]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxy = sum((x - mx) * (y - my) for x, y in pair_cells)
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        diffs = [x - y for x, y in pair_cells]
        md = sum(diffs) / n
        var_diff = sum((d - md) ** 2 for d in diffs) / (n - 1)
        alld = xs + ys
        ma = sum(alld) / len(alld)
        var_obs = sum((x - ma) ** 2 for x in alld) / (len(alld) - 1)
        report["dpsi_matrix"] = {
            "n_peptides_with_matrix": len(fills),
            "mean_fill_rate_of_28x19": round(sum(fills) / len(fills), 4),
            "n_substitution_cells_in_both_halves": n,
            "pearson_dpsi_between_halves": round(sxy / math.sqrt(sxx * syy), 4)
            if sxx and syy else None,
            "sd_noise_single_half": round(math.sqrt(var_diff / 2), 4),
            "noise_share_of_observed_variance": round(var_diff / 2 / var_obs, 4),
            "n_positive_cells_half_a": pos_a, "n_positive_cells_half_b": pos_b,
            "n_positive_in_both": agree,
            "jaccard_positive_cells": round(agree / (pos_a + pos_b - agree), 4)
            if (pos_a + pos_b - agree) else None,
            "note": ("jaccard_positive_cells là trần lặp lại khi gọi một Ô là dương. Mô hình "
                     "dự đoán ô không thể vượt mức này trên nhãn một-nửa."),
        }

    path = Path(__file__).parent / "saturation-matrix.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
