#!/usr/bin/env python3
"""Kiểm lại baseline PAP (Voutsinos 2026) và chạy ΔPAP trên nhãn footprint của Zhang 2023.

Ba phần:
  A. Tái lập Pearson công bố của PAP trên holdout hiệu dụng (428 gene), từ repo đã tải lại
     ngày 13/10 (@9b3eafa6). Số cũ (11/10): kênh nội 0,8239; đầy đủ, C-term cho mọi tile 0,8690.
  B. Đối chứng bắt buộc của đề tài (topic-decision §6): ΔPAP = PAP(đột biến) − PAP(hoang dã)
     tính trên ĐÚNG thay thế thực nghiệm của bộ quét, chấm bằng precision@3 với cùng ngưỡng,
     cùng tập peptide như label_ceiling.py / power_analysis.py. So với baseline thành phần
     0,4897 và trần nhãn 0,6514 bằng kiểm ghép cặp trên cùng peptide.
  C. ΔPAP trên ma trận bão hòa (nguồn nhãn chính theo D-025): Spearman và AUROC theo peptide
     ở mức ô, so với trần nửa-chấm-nửa.

PAP dương = bền hơn; ΔPSI dương = đột biến làm bền (footprint). Nên điểm footprint = ΔPAP.
Codon stop trong đột biến quét: cắt peptide tại stop rồi chấm, vì đầu C mới là một phần thật
của construct (GPS gắn peptide vào đầu C của GFP).

Chạy: .venv/bin/python topics/degron-footprint/research/pap-baseline/pap_baseline.py
Cần: data/interim/pap-weights/pap_weights/*.h5 (giải nén models/pap_weights.tgz của repo Voutsinos).
"""

import csv
import gzip
import json
import math
import random
import statistics
import sys
from pathlib import Path

import h5py
import numpy as np
from scipy.stats import spearmanr, rankdata, wilcoxon

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / "data" / "README.md").exists())
sys.path.insert(0, str(TOPIC / "research/full-data-audit"))
import label_ceiling as lc            # noqa: E402  load_psi, load_sequences, build_peptides
import saturation_matrix as sm       # noqa: E402  derive_sequence, load_uniprot, SAT_PAT

REPO = TOPIC / "data/raw/voutsinos-2026/repo"
WDIR = TOPIC / "data/interim/pap-weights/pap_weights"
AA = "ACDEFGHIKLMNPQRSTVWY"
AA2I = {a: i for i, a in enumerate(AA)}
SEED = 0
N_BOOT = 2000


def elu(x):
    return np.where(x > 0, x, np.expm1(np.minimum(x, 0)))


class PAP:
    """Dựng lại PAP chỉ bằng numpy, giống voutsinos-2026-audit/test_allct.py."""

    def __init__(self, path):
        f = h5py.File(path, "r")
        g = lambda n: np.array(f[n])  # noqa: E731
        self.Wc, self.bc = g("int_cnn/int_cnn/kernel:0"), g("int_cnn/int_cnn/bias:0")
        self.k = self.Wc.shape[0]
        self.W2, self.b2 = g("int2/int2/kernel:0"), g("int2/int2/bias:0")
        self.W3, self.b3 = g("int3/int3/kernel:0"), g("int3/int3/bias:0")
        self.W4, self.b4 = g("latent_int/latent_int/kernel:0"), g("latent_int/latent_int/bias:0")
        self.C = [(g(f"ct{i}/ct{i}/kernel:0"), g(f"ct{i}/ct{i}/bias:0")) for i in (1, 2, 3)]
        self.C4, self.c4 = g("latent_ct/latent_ct/kernel:0"), g("latent_ct/latent_ct/bias:0")

    def internal(self, X):
        n, L, _ = X.shape
        k = self.k
        w = np.lib.stride_tricks.sliding_window_view(X, k, axis=1)
        w = w.transpose(0, 1, 3, 2).reshape(n, L - k + 1, k * 20)
        h = elu(w @ self.Wc.reshape(k * 20, -1) + self.bc).mean(axis=1)
        h = elu(h @ self.W2 + self.b2)
        h = elu(h @ self.W3 + self.b3)
        return (h @ self.W4 + self.b4).ravel()

    def cterm(self, X5):
        h = X5.reshape(X5.shape[0], -1)
        for W, b in self.C:
            h = elu(h @ W + b)
        return (h @ self.C4 + self.c4).ravel()

    def score(self, seqs):
        """Điểm đầy đủ cho danh sách chuỗi; gom theo độ dài vì GAP phụ thuộc độ dài."""
        out = np.full(len(seqs), np.nan)
        by_len = {}
        for i, s in enumerate(seqs):
            if s is not None and len(s) >= max(self.k, 5):
                by_len.setdefault(len(s), []).append(i)
        for L, idx in by_len.items():
            X = np.zeros((len(idx), L, 20), dtype=np.float32)
            for r, i in enumerate(idx):
                for j, a in enumerate(seqs[i]):
                    X[r, j, AA2I[a]] = 1.0
            out[idx] = self.internal(X) + self.cterm(X[:, -5:, :])
        return out


def clean(seq):
    """Chữ hoa, cắt tại stop đầu tiên; None nếu có ký tự lạ."""
    s = seq.upper().split("*")[0]
    return s if s and all(c in AA2I for c in s) else None


# ---------------------------------------------------------------- A. Voutsinos
def part_a(models):
    rows = [r for r in csv.DictReader(gzip.open(REPO / "score/degrons.csv.gz", "rt"))
            if "_tile" in r["name"]]
    gene = lambda n: n.split("_tile")[0]  # noqa: E731
    train = {gene(r["name"]) for r in csv.DictReader(gzip.open(REPO / "models/degron_train.csv.gz", "rt"))}
    hold = {l.strip() for l in open(REPO / "library/holdout_selection.txt") if l.strip()}
    seqs, y = [], []
    for r in rows:
        g, s, v = gene(r["name"]), r["aa"].upper(), r["abundance_score"]
        if g in hold and g not in train and len(s) == 30 and all(c in AA2I for c in s) \
                and v not in ("", "NA", "NaN"):
            seqs.append(s)
            y.append(float(v))
    y = np.array(y)
    X = np.zeros((len(seqs), 30, 20), dtype=np.float32)
    for n, s in enumerate(seqs):
        for i, a in enumerate(s):
            X[n, i, AA2I[a]] = 1.0
    out = {"n_tiles": len(y), "n_genes": len({g for g in hold if g not in train})}
    for name, m in models.items():
        si, sc = m.internal(X), m.cterm(X[:, 25:30, :])
        out[name] = {"pearson_internal_only": round(float(np.corrcoef(si, y)[0, 1]), 4),
                     "pearson_full_cterm_all_tiles": round(float(np.corrcoef(si + sc, y)[0, 1]), 4)}
    out["published"] = {"internal_only": 0.82, "full": 0.87}
    out["previous_rerun_2026_10_11"] = {"cnn2w1_internal_only": 0.8239, "cnn2w1_full": 0.8690,
                                        "cnn2w7_full": 0.8722}
    return out, train


# ---------------------------------------------------------------- B. bộ quét
def p_at_k(scores, labels, rng, k=lc.TOP_K):
    return lc.precision_at_k(scores, labels, k=k, rng=rng)


def boot_ci(diffs, rng):
    n = len(diffs)
    means = sorted(sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(N_BOOT))
    return [round(means[int(0.025 * N_BOOT)], 4), round(means[int(0.975 * N_BOOT)], 4)]


def part_b(models, train_genes):
    rng = random.Random(SEED)
    seqs, subs = lc.load_sequences()
    f1, f2 = lc.build_peptides(lc.load_psi("rep1")), lc.build_peptides(lc.load_psi("rep2"))
    shared = sorted(f1.keys() & f2.keys())

    # ΔPAP cho mọi (peptide, vị trí) có trong nhãn
    keys, wt_seqs, mut_seqs = [], [], []
    n_stop = 0
    for pep in shared:
        w = clean(seqs.get(pep, ""))
        if w is None:
            continue
        for pos in set(f1[pep]) | set(f2[pep]):
            m = subs.get((pep, pos))
            if m is None:
                continue
            n_stop += "*" in m.rstrip("*")[: len(w)]
            keys.append((pep, pos))
            wt_seqs.append(w)
            mut_seqs.append(clean(m))
    dpap = {}
    for name, m in models.items():
        uniq = sorted({s for s in wt_seqs + mut_seqs if s})
        sc = dict(zip(uniq, m.score(uniq)))
        d = {}
        for (pep, pos), w, mu in zip(keys, wt_seqs, mut_seqs):
            if mu is not None and not math.isnan(sc.get(mu, math.nan)):
                d.setdefault(pep, {})[pos] = sc[mu] - sc[w]
        dpap[name] = d

    # map UniProt -> có nằm trong gene train của PAP không (rò rỉ tiềm năng)
    ens2up = {}
    for r in csv.DictReader(gzip.open(REPO / "library/cytosol_genes.csv.gz", "rt")):
        ens2up.setdefault(r["gene"], set()).update(x for x in (r["uniprot"], r.get("uniprot2", "")) if x)
    up_in_train = set().union(*(ens2up.get(g, set()) for g in train_genes))

    def composition(pep):
        groups = {}
        for pos in f1[pep]:
            s, m = seqs.get(pep), subs.get((pep, pos))
            if not s or not m or pos > len(s) or pos > len(m):
                return None
            groups.setdefault((s[pos - 1], m[pos - 1]), []).append(pos)
        comp = {}
        for members in groups.values():
            gm = sum(f1[pep][p] for p in members) / len(members)
            comp.update({p: gm for p in members})
        return comp

    out = {"n_shared_peptides": len(shared), "n_stop_mutants_scored_truncated": n_stop}
    for label_name in ("rep2", "mean_rep1_rep2"):
        res = {}
        rows = []
        for pep in shared:
            if label_name == "rep2":
                labels = f2[pep]
            else:
                labels = {p: (f1[pep][p] + f2[pep][p]) / 2 for p in f1[pep] if p in f2[pep]}
            if not any(v >= lc.RESCUE_DELTA for v in labels.values()):
                continue
            comp = composition(pep)
            if comp is None:
                continue
            r = {"pep": pep, "in_pap_train": pep.split("_")[0] in up_in_train,
                 "ceiling": p_at_k(f1[pep], labels, rng) if label_name == "rep2" else None,
                 "composition": p_at_k(comp, labels, rng) if label_name == "rep2" else None}
            for name in models:
                d = dpap[name].get(pep, {})
                r[name] = p_at_k(d, labels, rng)
                common = [p for p in d if p in labels]
                r[name + "_spearman"] = (spearmanr([d[p] for p in common],
                                                   [labels[p] for p in common]).statistic
                                         if len(common) >= 5 else None)
            pos_set = {p for p, v in labels.items() if v >= lc.RESCUE_DELTA}
            r["random"] = len(pos_set) / len(labels)
            rows.append(r)
        keep = [r for r in rows if all(r[n] is not None for n in models)
                and (label_name != "rep2" or (r["ceiling"] is not None and r["composition"] is not None))]
        res["n_peptides_scored"] = len(keep)
        mean = lambda xs: round(sum(xs) / len(xs), 4) if xs else None  # noqa: E731
        res["precision_at_3"] = {"random": mean([r["random"] for r in keep])}
        for name in models:
            res["precision_at_3"]["dPAP_" + name] = mean([r[name] for r in keep])
            sp = [r[name + "_spearman"] for r in keep
                  if r[name + "_spearman"] is not None and not math.isnan(r[name + "_spearman"])]
            res.setdefault("spearman_per_peptide_mean", {})["dPAP_" + name] = mean(sp)
        if label_name == "rep2":
            res["precision_at_3"]["composition_from_rep1"] = mean([r["composition"] for r in keep])
            res["precision_at_3"]["ceiling_rep1"] = mean([r["ceiling"] for r in keep])
            brng = random.Random(SEED + 1)
            for name in models:
                for ref in ("composition", "ceiling"):
                    diffs = [r[name] - r[ref] for r in keep]
                    st = wilcoxon([r[name] for r in keep], [r[ref] for r in keep], zero_method="zsplit")
                    res.setdefault("paired", {})[f"dPAP_{name}_minus_{ref}"] = {
                        "mean_diff": mean(diffs), "bootstrap95": boot_ci(diffs, brng),
                        "wilcoxon_p": float(f"{st.pvalue:.3g}")}
        # tách theo việc protein có trong tập train của PAP hay không
        for flag in (True, False):
            sub = [r for r in keep if r["in_pap_train"] == flag]
            res.setdefault("by_pap_train_overlap", {})[
                "protein_in_pap_train" if flag else "protein_not_in_pap_train"] = {
                "n": len(sub), **{"dPAP_" + n: mean([r[n] for r in sub]) for n in models}}
        out["labels_" + label_name] = res
    return out


# ---------------------------------------------------------------- C. bộ bão hòa
def part_c(models):
    sat_a, sat_b = sm.load_psi("sat_a"), sm.load_psi("sat_b")
    scan_seqs = sm.load_scan_wt_sequences()
    uniprot = sm.load_uniprot()

    def parse(t):
        cells = {}
        for name, psi in t.items():
            m = sm.SAT_PAT.match(name)
            if m:
                cells.setdefault(m.group("pep"), {})[(int(m.group("pos")), m.group("aa").upper())] = psi
        return cells

    ca, cb = parse(sat_a), parse(sat_b)
    peps = []
    for pep in sorted(set(ca) | set(cb)):
        truth = scan_seqs.get(pep)
        derived = sm.derive_sequence(pep, uniprot)
        if truth:
            t = truth.rstrip("*").upper()
            seq = t if derived and derived[: len(t)] == t else None
        else:
            seq = derived
        if seq and all(c in AA2I for c in seq):
            peps.append((pep, seq))

    def dmatrix(cells, seq):
        vals = [cells[(i, r)] for i, r in enumerate(seq, 1) if (i, r) in cells]
        if len(vals) < 10:
            return None, None
        ref = statistics.median(vals)
        wt = {(i, r) for i, r in enumerate(seq, 1)}
        return {k: v - ref for k, v in cells.items() if k not in wt}, ref

    # điểm ΔPAP cho mọi ô
    jobs = {}
    for pep, seq in peps:
        jobs[(pep, 0, "")] = seq
        for i in range(1, len(seq) + 1):
            for b in AA:
                if b != seq[i - 1]:
                    jobs[(pep, i, b)] = seq[: i - 1] + b + seq[i:]
    seq_list = sorted(set(jobs.values()))
    out = {"n_peptides_with_sequence": len(peps)}
    preds = {}
    for name, m in models.items():
        sc = dict(zip(seq_list, m.score(seq_list)))
        preds[name] = {k: sc[s] for k, s in jobs.items()}

    def auroc(score, pos):
        if not any(pos) or all(pos):
            return None
        r = rankdata(score)
        npos = sum(pos)
        return (sum(rv for rv, p in zip(r, pos) if p) - npos * (npos + 1) / 2) / (npos * (len(pos) - npos))

    rows = []
    for pep, seq in peps:
        da, ra = dmatrix(ca.get(pep, {}), seq)
        db, rb = dmatrix(cb.get(pep, {}), seq)
        if da is None or db is None:
            continue
        cells = sorted(set(da) & set(db))
        avg = {k: (da[k] + db[k]) / 2 for k in cells}
        wt_psi = (ra + rb) / 2
        if wt_psi > lc.DEGRON_PSI_MAX:
            continue                                   # cùng ngưỡng degron như bộ quét
        lab = [avg[k] for k in cells]
        pos = [v >= lc.RESCUE_DELTA for v in lab]
        r = {"pep": pep, "n_cells": len(cells), "n_pos": sum(pos),
             "ceiling_spearman": spearmanr([da[k] for k in cells], [db[k] for k in cells]).statistic,
             "ceiling_auroc": auroc([da[k] for k in cells], [db[k] >= lc.RESCUE_DELTA for k in cells])}
        for name in models:
            s = [preds[name][(pep, i, b)] - preds[name][(pep, 0, "")] for i, b in cells]
            r[name + "_spearman"] = spearmanr(s, lab).statistic
            r[name + "_auroc"] = auroc(s, pos)
            # mức vị trí: độ nhạy = trung bình ΔPSI trên 19 thay thế
            pos_lab, pos_s = {}, {}
            for (i, b), v, sv in zip(cells, lab, s):
                pos_lab.setdefault(i, []).append(v)
                pos_s.setdefault(i, []).append(sv)
            pl = [statistics.mean(pos_lab[i]) for i in sorted(pos_lab)]
            ps = [statistics.mean(pos_s[i]) for i in sorted(pos_lab)]
            r[name + "_position_spearman"] = spearmanr(ps, pl).statistic
        rows.append(r)

    def m(key):
        xs = [r[key] for r in rows if r[key] is not None and not math.isnan(r[key])]
        return {"mean": round(sum(xs) / len(xs), 4), "n": len(xs)} if xs else None

    out["n_degron_peptides_wt_psi_le_3"] = len(rows)
    out["cell_level"] = {"ceiling_half_a_vs_half_b_spearman": m("ceiling_spearman"),
                         "ceiling_half_a_scores_half_b_labels_auroc": m("ceiling_auroc")}
    for name in models:
        out["cell_level"]["dPAP_" + name + "_spearman"] = m(name + "_spearman")
        out["cell_level"]["dPAP_" + name + "_auroc"] = m(name + "_auroc")
        out.setdefault("position_level", {})["dPAP_" + name + "_spearman"] = m(name + "_position_spearman")
    out["note"] = ("Nhãn ô = trung bình hai nửa (S1–S6, S7–S12), WT nội tại là trung vị các ô đồng "
                   "nghĩa. Trần dùng nhãn một nửa nên thấp hơn trần thật của nhãn trung bình hai nửa.")
    return out


def main():
    models = {n: PAP(WDIR / f"{n}_weights.h5") for n in ("cnn2w1", "cnn2w7")}
    report = {"seed": SEED, "voutsinos_repo_commit": "9b3eafa6"}
    report["A_voutsinos_holdout"], train_genes = part_a(models)
    print(json.dumps(report["A_voutsinos_holdout"], indent=1))
    report["B_scanning_footprint"] = part_b(models, train_genes)
    print(json.dumps(report["B_scanning_footprint"], indent=1, ensure_ascii=False))
    report["C_saturation_matrix"] = part_c(models)
    print(json.dumps(report["C_saturation_matrix"], indent=1, ensure_ascii=False))
    (HERE / "pap-baseline.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                            encoding="utf-8")
    print("ghi: pap-baseline.json")


if __name__ == "__main__":
    main()
