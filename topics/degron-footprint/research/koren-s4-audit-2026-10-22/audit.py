#!/usr/bin/env python3
"""Audit Koren 2018 Table S4 (+ S3) và cổng P2 — tiêu chí chốt ở PROTOCOL.md.

Chạy từ thư mục gốc repo:
    OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/koren-s4-audit-2026-10-22/audit.py

Đọc xlsx bằng openpyxl (data_only, read_only): không chạy macro/mã trong file.
Ghi: results.json (cạnh script), data/interim/koren-2018-cells.tsv, data/interim/koren-2018-cluster/.
"""

import gzip
import json
import re
import statistics
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import openpyxl

warnings.simplefilter("ignore")

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / "data" / "README.md").exists())
sys.path.insert(0, str(TOPIC / "research/residue-task-derisk-2026-10-15"))
import residue_data as rd  # noqa: E402

RAW = TOPIC / "data/raw/koren-2018"
INTERIM = TOPIC / "data/interim"
CLU = INTERIM / "koren-2018-cluster"
S3, S4 = RAW / "NIHMS967427-supplement-10.xlsx", RAW / "NIHMS967427-supplement-11.xlsx"
SUBST = re.compile(r"^([A-Z])(\d+)([A-Z])$")
THRESH = {"G1_min_new_clusters": 20, "R1_tol": 1e-6, "R1_frac": 0.99, "R2_min_identity": 8,
          "R2_min_substrates": 7, "R3_median": 0.5, "R3_frac_pos": 0.9}


def read_sheet(ws):
    rows = list(ws.iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Oligo ID")
    head = [str(c) for c in rows[h]]
    out = []
    for r in rows[h + 1:]:
        if not r or r[0] is None:
            continue
        d = dict(zip(head, r))
        d["bins"] = [float(d[f"Bin{i}"]) for i in (1, 2, 3)]
        d["psi_reported"] = float(d["PSI"])
        d["seq"] = str(d["Amino acid sequence"])
        out.append(d)
    return out


def load(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return {ws.title: read_sheet(ws) for ws in wb.worksheets}


def psi_from_bins(b):
    t = sum(b)
    return sum((i + 1) * x for i, x in enumerate(b)) / t if t > 0 else float("nan")


def substrate_name(title):
    return title.split(". ", 1)[1].strip()


def spearman(x, y):
    def rank(a):
        o = np.argsort(a, kind="mergesort")
        r = np.empty(len(a))
        r[o] = np.arange(len(a))
        for v in set(a):  # trung bình hạng khi hòa
            idx = [i for i, t in enumerate(a) if t == v]
            if len(idx) > 1:
                r[idx] = np.mean(r[idx])
        return r
    return float(np.corrcoef(rank(list(x)), rank(list(y)))[0, 1])


def describe(v):
    v = np.asarray(v, float)
    return {"n": int(len(v)), "median": float(np.median(v)), "p05": float(np.percentile(v, 5)),
            "p95": float(np.percentile(v, 95)), "min": float(v.min()), "max": float(v.max())}


# ------------------------------------------------------------------ S4
def audit_s4(sheets):
    out, cells, wt_seqs = {}, [], {}
    all_diff, n_rows, n_ok = [], 0, 0
    for title, rows in sheets.items():
        sub = substrate_name(title)
        parsed = []
        for r in rows:
            m = SUBST.match(str(r["Substitution"]).strip())
            if not m:
                continue
            wt_aa, pos, mut_aa = m.group(1), int(m.group(2)), m.group(3)
            re_psi = psi_from_bins(r["bins"])
            diff = abs(re_psi - r["psi_reported"])
            all_diff.append(diff)
            n_rows += 1
            n_ok += diff <= THRESH["R1_tol"]
            parsed.append({"pos": pos, "wt": wt_aa, "mut": mut_aa, "psi": r["psi_reported"],
                           "seq": r["seq"].rstrip("*"), "term": r["seq"].endswith("*")})
        # trình tự WT: hoàn nguyên một dòng không đồng nghĩa
        ref = next(p for p in parsed if p["wt"] != p["mut"])
        seq_l = list(ref["seq"])
        seq_l[ref["pos"] - 1] = ref["wt"]
        wt_seq = "".join(seq_l)
        # kiểm nhất quán: mọi dòng chỉ khác WT ở đúng 1 vị trí
        bad = sum(1 for p in parsed
                  if sum(a != b for a, b in zip(wt_seq, p["seq"])) != (0 if p["wt"] == p["mut"] else 1)
                  or wt_seq[p["pos"] - 1] != p["wt"])
        ident = [p["psi"] for p in parsed if p["wt"] == p["mut"]]
        wt_psi = statistics.median(ident) if len(ident) >= 1 else float("nan")
        for p in parsed:
            p["substrate"] = sub
            p["dpsi"] = p["psi"] - wt_psi
            cells.append(p)
        mut = [p for p in parsed if p["wt"] != p["mut"]]
        wt_seqs[sub] = wt_seq
        out[sub] = {
            "sheet": title, "n_rows": len(parsed), "n_identity": len(ident),
            "n_mutant_cells": len(mut), "positions": [min(p["pos"] for p in parsed), max(p["pos"] for p in parsed)],
            "wt_seq": wt_seq, "wt_len": len(wt_seq), "has_stop": all(p["term"] for p in parsed),
            "wt_psi_internal": wt_psi, "identity_psi_sd": float(np.std(ident)) if ident else None,
            "inconsistent_rows": bad,
            "dpsi": describe([p["dpsi"] for p in mut]),
            "frac_pos_ge1.0": float(np.mean([p["dpsi"] >= 1.0 for p in mut])),
            "frac_pos_ge0.4_range_equiv": float(np.mean([p["dpsi"] >= 0.4 for p in mut])),
            "max_dpsi": float(max(p["dpsi"] for p in mut)),
            "median_dpsi_by_pos": {str(pos): round(float(np.median([p["dpsi"] for p in mut if p["pos"] == pos])), 3)
                                   for pos in sorted({p["pos"] for p in mut})},
        }
    r1 = {"n_rows": n_rows, "n_within_tol": int(n_ok), "frac": n_ok / n_rows,
          "max_abs_diff": float(max(all_diff)), "pass": bool(n_ok / n_rows >= THRESH["R1_frac"])}
    return out, cells, wt_seqs, r1


# ------------------------------------------------------------------ S3
def audit_s3(sheets):
    out, cells = {}, []
    for title, rows in sheets.items():
        name = substrate_name(title)
        wt = rows[0]
        ok = sum(abs(psi_from_bins(r["bins"]) - r["psi_reported"]) <= 1e-6 for r in rows)
        muts = []
        for r in rows[1:]:
            if len(r["seq"]) != len(wt["seq"]):
                continue
            d = [(i, a, b) for i, (a, b) in enumerate(zip(wt["seq"], r["seq"]), 1) if a != b]
            if len(d) == 1:
                i, a, b = d[0]
                muts.append({"pos": i, "wt": a, "mut": b, "psi": r["psi_reported"]})
        out[name] = {"wt_oligo": wt["Oligo ID"], "wt_seq": wt["seq"], "wt_len": len(wt["seq"]),
                     "wt_psi": wt["psi_reported"], "n_mutants": len(muts), "n_rows": len(rows),
                     "psi_recompute_ok": f"{ok}/{len(rows)}"}
        for m in muts:
            m["substrate"], m["dpsi"] = name, m["psi"] - wt["psi_reported"]
            cells.append(m)
    return out, cells


# ------------------------------------------------------------------ ánh xạ + cụm
def map_to_uniprot(wt_seqs):
    up = rd.load_uniprot()
    res = {}
    for sub, seq in wt_seqs.items():
        suffix = [a for a, s in up.items() if s.endswith(seq)]
        anywhere = [a for a, s in up.items() if seq in s] if not suffix else []
        res[sub] = {"seq": seq, "len": len(seq), "c_terminal_match": sorted(suffix),
                    "internal_match": sorted(anywhere)[:10], "n_internal": len(anywhere)}
    return res, up


def cluster_joint(mapping, up, train_accs):
    prot = {}
    for line in (TOPIC / "data/processed/proteins-full.fasta").read_text().splitlines():
        if line.startswith(">"):
            acc = line[1:].strip()
            prot[acc] = []
        else:
            prot[acc].append(line.strip())
    prot = {a: "".join(s) for a, s in prot.items()}
    koren_accs = sorted({a for m in mapping.values() for a in (m["c_terminal_match"] or m["internal_match"])})
    added = [a for a in koren_accs if a not in prot]
    for a in added:
        prot[a] = up[a]
    CLU.mkdir(parents=True, exist_ok=True)
    fasta = CLU / "joint.fasta"
    fasta.write_text("".join(f">{a}\n{s}\n" for a, s in sorted(prot.items())))
    prefix = CLU / "joint-id30-cov80"
    cmd = ["mmseqs", "easy-cluster", str(fasta), str(prefix), str(prefix) + "-tmp",
           "--min-seq-id", "0.3", "-c", "0.8", "--cov-mode", "0", "--seq-id-mode", "0",
           "--alignment-mode", "3", "--cluster-mode", "1", "--single-step-clustering", "1",
           "-s", "7.5", "--max-seqs", "10000", "--split-memory-limit", "2G", "--threads", "2"]
    tsv = Path(str(prefix) + "_cluster.tsv")
    if not tsv.exists():
        with (CLU / "mmseqs.log").open("w") as fh:
            subprocess.run(cmd, check=True, stdout=fh, stderr=subprocess.STDOUT)
    members = {}
    for line in tsv.read_text().splitlines():
        r, m = line.split("\t")[:2]
        members.setdefault(r, set()).add(m)
    rep_of = {m: r for r, ms in members.items() for m in ms}
    per_sub, new_clusters = {}, set()
    for sub, m in mapping.items():
        accs = m["c_terminal_match"] or m["internal_match"]
        info = []
        for a in accs:
            rep = rep_of[a]
            overlap = sorted(members[rep] & train_accs)
            info.append({"accession": a, "in_zhang_6573": a not in added, "cluster_rep": rep,
                         "cluster_size": len(members[rep]), "overlap_with_176_peptides": overlap})
        is_new = bool(info) and all(not i["overlap_with_176_peptides"] for i in info)
        per_sub[sub] = {"accessions": info, "mapped": bool(info), "new_cluster": is_new}
        if is_new:
            new_clusters.update(i["cluster_rep"] for i in info)
    return per_sub, new_clusters, {"n_zhang_proteins": len(prot) - len(added), "n_added_koren": len(added),
                                   "n_clusters_joint": len(members)}


def main():
    s4 = load(S4)
    s3 = load(S3)
    sub4, cells4, wt_seqs, r1 = audit_s4(s4)
    sub3, cells3 = audit_s3(s3)

    # R2: ô đồng nghĩa
    r2_n = sum(v["n_identity"] >= THRESH["R2_min_identity"] for v in sub4.values())
    r2 = {"n_substrates_ge8_identity": int(r2_n), "of": len(sub4),
          "pass": bool(r2_n >= THRESH["R2_min_substrates"])}

    # R3: Gly cuối của Clone#8
    g = [c["dpsi"] for c in cells4 if c["substrate"] == "Clone#8" and c["pos"] == 12 and c["wt"] == "G" and c["mut"] != "G"]
    r3 = {"n": len(g), "median_dpsi": float(np.median(g)), "frac_positive": float(np.mean([x > 0 for x in g])),
          "pass": bool(np.median(g) >= THRESH["R3_median"] and np.mean([x > 0 for x in g]) >= THRESH["R3_frac_pos"])}

    # R4 (chẩn đoán): S3E (Clone#8) vs S4A trên ô trùng
    s4key = {(c["pos"], c["mut"]): c["dpsi"] for c in cells4 if c["substrate"] == "Clone#8" and c["wt"] != c["mut"]}
    pairs = [(c["dpsi"], s4key[(c["pos"], c["mut"])]) for c in cells3
             if c["substrate"] == "Clone#8" and (c["pos"], c["mut"]) in s4key]
    wt_s3 = sub3["Clone#8"]["wt_psi"]
    r4 = {"n_overlap": len(pairs), "wt_s3_row": wt_s3, "wt_s4_identity_median": sub4["Clone#8"]["wt_psi_internal"],
          "spearman": spearman([a for a, _ in pairs], [b for _, b in pairs]) if len(pairs) >= 3 else None,
          "pairs_s3_s4": [[round(a, 3), round(b, 3)] for a, b in pairs]}

    # Ánh xạ + cụm
    all_wt = dict(wt_seqs)
    for name, v in sub3.items():
        if name != "Clone#8":
            all_wt[f"S3:{name}"] = v["wt_seq"]
    mapping, up = map_to_uniprot(all_wt)
    d = rd.load_all(degron_psi_max=4.0)
    train_accs = {rd.accession(p) for p in d["sat"]}
    del d
    per_sub, new_clusters, clu_meta = cluster_joint(mapping, up, train_accs)
    g1 = {"n_substrates_s4": len(sub4), "n_substrates_s4_s3_dedup": len(all_wt),
          "n_mapped": sum(v["mapped"] for v in per_sub.values()),
          "n_new_clusters": len(new_clusters), "n_train_accessions_176": len(train_accs),
          "pass": bool(len(new_clusters) >= THRESH["G1_min_new_clusters"])}

    # So với Zhang (mô tả)
    mut4 = [c for c in cells4 if c["wt"] != c["mut"]]
    desc = {"s4_all_mutant_cells": len(mut4),
            "dpsi": describe([c["dpsi"] for c in mut4]),
            "frac_pos_ge1.0": float(np.mean([c["dpsi"] >= 1.0 for c in mut4])),
            "frac_pos_ge0.4_range_equiv": float(np.mean([c["dpsi"] >= 0.4 for c in mut4])),
            "psi_range_observed": [float(min(c["psi"] for c in cells4)), float(max(c["psi"] for c in cells4))],
            "zhang_reference": {"frac_pos_ge1.0_base91": 0.1310, "frac_pos_ge1.0_new85": 0.1140,
                                "psi_bins": 6, "koren_s4_bins": 3,
                                "source": "learning-curve-2026-10-22/README.md §3"}}

    gate = bool(g1["pass"] and r1["pass"] and r2["pass"] and r3["pass"])
    role = ("P4_import_with_source_indicator" if gate else
            "external_validation_only" if (r1["pass"] and r2["pass"] and r3["pass"]) else "unusable_until_explained")
    result = {"thresholds": THRESH, "G1": g1, "R1": r1, "R2": r2, "R3": r3, "R4_diagnostic": r4,
              "gate_pass": gate, "role": role, "s4_substrates": sub4, "s3_substrates": sub3,
              "mapping": {k: {**v, **per_sub[k]} for k, v in mapping.items()},
              "clustering": clu_meta, "description": desc}
    (HERE / "results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))

    # bảng ô chuẩn hóa (interim, không lên git)
    with (INTERIM / "koren-2018-cells.tsv").open("w") as fh:
        fh.write("table\tsubstrate\tpos\twt_aa\tmut_aa\tpsi\tdpsi\tn_bins\n")
        for c in cells4:
            if c["wt"] != c["mut"]:
                fh.write(f"S4\t{c['substrate']}\t{c['pos']}\t{c['wt']}\t{c['mut']}\t{c['psi']:.6f}\t{c['dpsi']:.6f}\t3\n")
        for c in cells3:
            fh.write(f"S3\t{c['substrate']}\t{c['pos']}\t{c['wt']}\t{c['mut']}\t{c['psi']:.6f}\t{c['dpsi']:.6f}\t3\n")

    print(json.dumps({"G1": g1, "R1": r1, "R2": r2, "R3": r3, "R4": {k: v for k, v in r4.items() if k != 'pairs_s3_s4'},
                      "gate_pass": gate, "role": role, "desc": desc}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
