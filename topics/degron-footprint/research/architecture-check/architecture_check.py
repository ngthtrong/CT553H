#!/usr/bin/env python3
"""Kiểm tiền đề của kiến trúc MIL-Degron (topic-decision §5) bằng dữ liệu đã có, không huấn luyện.

Hai tiền đề kiểm được ngay:
  1. CỔNG PHƠI LỘ (thành phần 4): tín hiệu degron chỉ biểu hiện ở vùng phơi lộ của protein nguyên vẹn.
     Nếu đúng, tương quan giữa ΔPAP (mô hình degron, không biết cấu trúc) và độ dồi dào đo bằng
     MaveDB phải cao hơn rõ ở residue phơi lộ / pLDDT thấp, và hồi quy phải có hệ số tương tác
     ΔPAP × rASA dương. Cấu trúc: AlphaFold DB v6, rASA tính bằng Shrake–Rupley (Biopython),
     chuẩn hóa theo max ASA lý thuyết Tien 2013; pLDDT đọc từ cột B-factor.
  2. NỐI NHÃN ĐOẠN VỚI NHÃN RESIDUE (thành phần 3, 5): hai assay đo cùng một đại lượng thì mới
     học đa nhiệm được. Đo tương quan giữa PSI hoang dã của peptide Zhang 2023 và điểm của tile
     Voutsinos 2026 chồng ≥ 20 residue, và độ phủ của tile Voutsinos trên peptide có footprint.

Chạy: .venv/bin/python topics/degron-footprint/research/architecture-check/architecture_check.py
Cần: biopython; data/raw/alphafold/AF-<acc>-F1-model_v6.pdb (xem README); pap-weights đã giải nén.
"""

import csv
import gzip
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / "log.md").exists())
sys.path.insert(0, str(TOPIC / "research/full-data-audit"))
sys.path.insert(0, str(TOPIC / "research/pap-baseline"))
import label_ceiling as lc  # noqa: E402
from pap_baseline import PAP, AA, AA2I, WDIR  # noqa: E402

RAW = TOPIC / "data/raw"
SEED = 0
N_BOOT = 1000
WIN = 30
# max ASA lý thuyết, Tien et al. 2013
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "Q": 225, "E": 223, "G": 104,
           "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155,
           "T": 172, "W": 285, "Y": 263, "V": 174}
THREE = {"Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q", "Glu": "E",
         "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F",
         "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V"}
ONE_FROM_PDB = {k.upper(): v for k, v in THREE.items()}
HGVS = re.compile(r"^p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|Ter|\*)$")

# một bộ điểm độ dồi dào cho mỗi gene; CYP2C9/2C19 là protein màng ER, báo riêng
ABUNDANCE_SETS = {
    "PTEN": ("urn_mavedb_00000013-a-1", "P60484", "cytosol"),
    "TPMT": ("urn_mavedb_00000013-b-1", "P51580", "cytosol"),
    "NUDT15": ("urn_mavedb_00000055-a-1", "Q9NV35", "cytosol"),
    "ASPA": ("urn_mavedb_00000657-a-1", "P45381", "cytosol"),
    "PRKN": ("urn_mavedb_00000114-a-1", "O60260", "cytosol"),
    "GCK": ("urn_mavedb_00000096-b-1", "P35557", "cytosol"),
    "CYP2C9": ("urn_mavedb_00000095-b-1", "P11712", "er_membrane"),
    "CYP2C19": ("urn_mavedb_00000062-b-1", "P33261", "er_membrane"),
}
RASA_BINS = [(0, 0.2, "buried <0.2"), (0.2, 0.5, "0.2–0.5"), (0.5, 0.7, "0.5–0.7"), (0.7, 9, "exposed ≥0.7")]
PLDDT_BINS = [(0, 50, "<50"), (50, 70, "50–70"), (70, 90, "70–90"), (90, 101, "≥90")]


def structure(acc):
    s = PDBParser(QUIET=True).get_structure(acc, RAW / f"alphafold/AF-{acc}-F1-model_v6.pdb")
    ShrakeRupley().compute(s[0], level="R")
    seq, rasa, plddt = [], [], []
    for res in s[0]["A"]:
        aa = ONE_FROM_PDB.get(res.get_resname().capitalize().upper())
        if aa is None:
            continue
        seq.append(aa)
        rasa.append(min(1.0, res.sasa / MAX_ASA[aa]))
        plddt.append(next(iter(res)).get_bfactor())
    return "".join(seq), rasa, plddt


def load_variants(urn):
    out = {"missense": [], "nonsense": [], "synonymous": []}
    with open(RAW / f"mavedb/{urn}.scores.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                score = float(r["score"])
            except (TypeError, ValueError):
                continue
            if math.isnan(score):
                continue
            h = r["hgvs_pro"]
            if h in ("p.=", "_wt", "_sy") or h.endswith("="):
                out["synonymous"].append(score)
                continue
            m = HGVS.match(h)
            if not m:
                continue
            wt, pos, mt = THREE.get(m.group(1)), int(m.group(2)), m.group(3)
            if mt in ("Ter", "*"):
                out["nonsense"].append(score)
            elif wt and mt in THREE:
                out["missense"].append((pos, wt, THREE[mt], score))
    return out


def window(seq, i):
    start = max(0, min(i - WIN // 2, len(seq) - WIN))
    return start, seq[start:start + WIN]


def pap_delta(model, seq, variants):
    """ΔPAP trên cửa sổ 30 residue quanh biến thể. Protein nguyên vẹn không có đầu C tự do, nên
    chỉ dùng kênh nội, trừ cửa sổ chạm đầu C thật thì cộng kênh C-term."""
    wts, muts, cterm = [], [], []
    for pos, wt, mt, _ in variants:
        start, w = window(seq, pos - 1)
        k = pos - 1 - start
        wts.append(w)
        muts.append(w[:k] + mt + w[k + 1:])
        cterm.append(start + WIN >= len(seq))

    def onehot(xs):
        X = np.zeros((len(xs), WIN, 20), dtype=np.float32)
        for n, s in enumerate(xs):
            for j, a in enumerate(s):
                X[n, j, AA2I[a]] = 1.0
        return X

    Xw, Xm = onehot(wts), onehot(muts)
    d = model.internal(Xm) - model.internal(Xw)
    ct = np.array(cterm)
    if ct.any():
        d[ct] += model.cterm(Xm[ct][:, -5:, :]) - model.cterm(Xw[ct][:, -5:, :])
    return d


def ranknorm(x):
    r = np.argsort(np.argsort(x))
    return (r + 0.5) / len(x)


def part_gate(model):
    rows, per_gene = [], {}
    for gene, (urn, acc, loc) in ABUNDANCE_SETS.items():
        seq, rasa, plddt = structure(acc)
        v = load_variants(urn)
        ok = [x for x in v["missense"] if x[0] <= len(seq) and seq[x[0] - 1] == x[1]]
        info = {"location": loc, "n_missense": len(v["missense"]), "n_wt_match_af": len(ok),
                "median_missense": round(statistics.median(x[3] for x in v["missense"]), 3),
                "median_nonsense": round(statistics.median(v["nonsense"]), 3) if v["nonsense"] else None,
                "median_synonymous": round(statistics.median(v["synonymous"]), 3) if v["synonymous"] else None}
        if len(ok) < 50 or len(seq) < WIN:
            per_gene[gene] = info
            continue
        d = pap_delta(model, seq, ok)
        y = np.array([x[3] for x in ok])
        info["spearman_all"] = round(float(spearmanr(d, y).statistic), 4)
        for lo, hi, lab in RASA_BINS:
            msk = np.array([lo <= rasa[x[0] - 1] < hi for x in ok])
            if msk.sum() >= 30:
                info.setdefault("spearman_by_rasa", {})[lab] = [round(float(spearmanr(d[msk], y[msk]).statistic), 4), int(msk.sum())]
        per_gene[gene] = info
        dn, yn = ranknorm(d), ranknorm(y)
        for (pos, *_), a, b in zip(ok, dn, yn):
            rows.append((gene, loc, a, b, rasa[pos - 1], plddt[pos - 1]))

    def pooled(sel):
        xs = [(r[2], r[3]) for r in rows if sel(r)]
        if len(xs) < 30:
            return None
        return [round(float(spearmanr([a for a, _ in xs], [b for _, b in xs]).statistic), 4), len(xs)]

    out = {"per_gene": per_gene}
    scopes = (("cytosol", lambda r: r[1] == "cytosol"), ("all", lambda r: True),
              # độ nhạy: PRKN chiếm gần một nửa số residue phơi lộ
              ("cytosol_without_PRKN", lambda r: r[1] == "cytosol" and r[0] != "PRKN"))
    for scope, keep in scopes:
        res = {"all": pooled(keep)}
        for lo, hi, lab in RASA_BINS:
            res.setdefault("by_rasa", {})[lab] = pooled(lambda r, lo=lo, hi=hi: keep(r) and lo <= r[4] < hi)
        for lo, hi, lab in PLDDT_BINS:
            res.setdefault("by_plddt", {})[lab] = pooled(lambda r, lo=lo, hi=hi: keep(r) and lo <= r[5] < hi)
        # hồi quy trên hạng đã chuẩn hóa theo gene: y ~ ΔPAP + rASA + ΔPAP×rASA (+ hằng số theo gene)
        sub = [r for r in rows if keep(r)]
        genes = sorted({r[0] for r in sub})

        def fit(data):
            X = np.array([[r[2] - 0.5, r[4], (r[2] - 0.5) * r[4]] + [float(r[0] == g) for g in genes] for r in data])
            yv = np.array([r[3] for r in data])
            return np.linalg.lstsq(X, yv, rcond=None)[0][:3]

        coef = fit(sub)
        rng = random.Random(SEED)
        boots = sorted(fit([sub[rng.randrange(len(sub))] for _ in range(len(sub))])[2] for _ in range(N_BOOT))
        res["regression_rank_scale"] = {
            "n": len(sub), "beta_dPAP": round(float(coef[0]), 4), "beta_rASA": round(float(coef[1]), 4),
            "beta_dPAP_x_rASA": round(float(coef[2]), 4),
            "beta_dPAP_x_rASA_bootstrap95": [round(float(boots[int(0.025 * N_BOOT)]), 4),
                                             round(float(boots[int(0.975 * N_BOOT)]), 4)]}
        out[scope] = res
    return out


def part_cross_assay():
    # PSI hoang dã của peptide Zhang (rep1, reads ≥ 10)
    psi = lc.load_psi("rep1")
    seqs, _ = lc.load_sequences()
    zhang = {pep: (psi[pep + "_mut0"], seqs[pep].rstrip("*").upper())
             for pep in seqs if pep + "_mut0" in psi}
    footprint = set(lc.build_peptides(psi))           # peptide degron (WT PSI ≤ 3, ≥ 21 vị trí)
    f1 = lc.build_peptides(psi)
    fp = {p for p, d in f1.items() if any(v >= lc.RESCUE_DELTA for v in d.values())}

    repo = RAW / "voutsinos-2026/repo"
    train = {r["name"] for r in csv.DictReader(gzip.open(repo / "models/degron_train.csv.gz", "rt"))}
    idx, tiles = {}, {}
    for r in csv.DictReader(gzip.open(repo / "score/degrons.csv.gz", "rt")):
        s, v, dv = r["aa"].upper(), r["abundance_score"], r["degron_score"]
        if v in ("", "NA", "NaN"):
            continue
        tiles[r["name"]] = (float(v), float(dv) if dv not in ("", "NA", "NaN") else None, r["name"] in train)
        for j in range(len(s) - 19):
            idx.setdefault(s[j:j + 20], set()).add(r["name"])
    pairs, cov_fp, cov_fp_train = [], 0, 0
    for pep, (w, s) in zhang.items():
        hit = set()
        for j in range(len(s) - 19):
            hit |= idx.get(s[j:j + 20], set())
        if pep in fp:
            cov_fp += bool(hit)
            cov_fp_train += any(tiles[t][2] for t in hit)
        if hit:
            pairs.append((w, statistics.mean(tiles[t][0] for t in hit), pep in footprint))
    x, y = [p[0] for p in pairs], [p[1] for p in pairs]
    xd = [p[0] for p in pairs if p[2]]
    yd = [p[1] for p in pairs if p[2]]
    return {
        "n_zhang_peptides_with_wt_psi": len(zhang),
        "n_with_overlapping_voutsinos_tile_ge20aa": len(pairs),
        "spearman_zhang_wt_psi_vs_voutsinos_abundance": round(float(spearmanr(x, y).statistic), 4),
        "spearman_within_degron_peptides_wt_psi_le_3": [round(float(spearmanr(xd, yd).statistic), 4), len(xd)],
        "n_footprint_peptides": len(fp),
        "footprint_peptides_with_voutsinos_tile": cov_fp,
        "footprint_peptides_with_tile_in_pap_train": cov_fp_train,
        "note": ("Cả hai đều là điểm độ bền của peptide tách rời gắn vào đầu C của GFP; Spearman cao thì "
                 "nhãn đoạn và nhãn residue có thể dùng chung một biểu diễn. Peptide có tile trùng ở tập "
                 "train của bất kỳ mô hình nào phải được tính vào thiết kế split (rò rỉ chéo nhiệm vụ)."),
    }


def main():
    model = PAP(WDIR / "cnn2w7_weights.h5")
    report = {"seed": SEED, "pap_model": "cnn2w7", "window": WIN,
              "alphafold": "AlphaFold DB v6, tải 14/10/2026, xem data/raw/alphafold/manifest.txt"}
    report["gate_premise_mavedb"] = part_gate(model)
    print(json.dumps(report["gate_premise_mavedb"], indent=1, ensure_ascii=False))
    report["cross_assay_zhang_vs_voutsinos"] = part_cross_assay()
    print(json.dumps(report["cross_assay_zhang_vs_voutsinos"], indent=1, ensure_ascii=False))
    (HERE / "architecture-check.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                                  encoding="utf-8")
    print("ghi: architecture-check.json")


if __name__ == "__main__":
    main()
