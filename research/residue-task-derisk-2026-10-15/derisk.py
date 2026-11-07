#!/usr/bin/env python3
"""Giảm rủi ro cho nhiệm vụ MỨC RESIDUE và đo đóng góp của trục vị trí — 15/10/2026.

Bốn lệnh con, mỗi lệnh ghi một file JSON cạnh script:

  ladder   Đơn vị suy luận và cỡ mẫu thật: bậc thang ngưỡng peptide degron × (số peptide,
           số cụm protein cov80, số ô, tỉ lệ ô dương, trần nhãn), và hệ số thiết kế do ô
           lồng trong peptide.
  identify Rủi ro LeBlanc trên ĐÚNG loại nhãn: bootstrap theo cụm, đo độ ổn định của trọng
           số NGỮ CẢNH CỤC BỘ trên nhãn hiệu ứng đột biến, đối chiếu với trọng số thành
           phần. So sánh trực tiếp được với bảng ở reframe §11.2 (nhãn mức peptide).
  model    Thành phần so với vị trí/ngữ cảnh: M0 chỉ-thành-phần (cái mà chứng minh 89,7%
           nói là KHÔNG THỂ), M1 + chỉ số vị trí, M2 + thành phần cửa sổ (không thứ tự),
           M3 + ngữ cảnh có thứ tự. Chia theo cụm protein, 5 fold × 5 seed, chấm bằng
           AUROC mức ô trung bình theo peptide. Rồi chuyển sang bộ bão hòa, đã loại cụm
           trùng khỏi tập huấn luyện.
  power    Lực thống kê THẬT: lấy SD của chênh lệch ghép cặp từ chính các mô hình ở `model`,
           bootstrap theo cụm, rồi suy mức chênh nhỏ nhất phát hiện được ở n = 91.

Seed cố định. Ngưỡng giữ nguyên như mọi phiên trước (reads >= 10, PSI WT <= 3,0, ô dương
nếu ΔPSI >= 1,0) để số so sánh được với pap-baseline và full-data-audit.
"""

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr, wilcoxon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))      # chạy được cả với python -I
import residue_data as rd          # noqa: E402
SEED = 0
AAS = rd.AAS
AA2I = {a: i for i, a in enumerate(AAS)}
WINDOW = 3


# ------------------------------------------------------------------ thước đo

def auroc(score, positive):
    pos = np.asarray(positive, dtype=bool)
    npos = int(pos.sum())
    n = len(pos)
    if npos == 0 or npos == n:
        return None
    r = rankdata(score)
    return float((r[pos].sum() - npos * (npos + 1) / 2) / (npos * (n - npos)))


def design_effect(groups_sizes, icc):
    """Hệ số thiết kế Kish cho dữ liệu lồng: 1 + (m-1)*ICC với m là cỡ cụm bình quân."""
    m = statistics.mean(groups_sizes)
    return 1 + (m - 1) * icc


def icc_oneway(values_by_group):
    """ICC(1) một chiều từ phân rã phương sai giữa/trong peptide."""
    groups = [np.asarray(v, dtype=float) for v in values_by_group if len(v) >= 2]
    k = len(groups)
    if k < 2:
        return None
    n_i = np.array([len(g) for g in groups], dtype=float)
    means = np.array([g.mean() for g in groups])
    grand = np.concatenate(groups).mean()
    ms_between = (n_i * (means - grand) ** 2).sum() / (k - 1)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)
    df_within = n_i.sum() - k
    ms_within = ss_within / df_within if df_within > 0 else float("nan")
    m0 = (n_i.sum() - (n_i ** 2).sum() / n_i.sum()) / (k - 1)
    var_b = (ms_between - ms_within) / m0
    total = var_b + ms_within
    return float(var_b / total) if total > 0 else None


# ------------------------------------------------------------------ lệnh: ladder

def cmd_ladder(data):
    rep = data["clusters"]
    seqs, uniprot = data["seqs"], data["uniprot"]
    sat_a, sat_b = rd.load_psi("sat_a"), rd.load_psi("sat_b")
    out = {"note": "Ngưỡng áp trên WT nội tại (trung vị ô đồng nghĩa, trung bình hai nửa),"
                   " đúng cách pap_baseline.py phần C đã làm.",
           "levels": []}
    for thr in (2.5, 3.0, 3.5, 4.0, 99.0):
        sat = rd.build_saturation(sat_a, sat_b, seqs, uniprot, degron_psi_max=thr)
        accs = {rd.accession(p) for p in sat}
        clusters = {rep.get(a, a) for a in accs}
        cells, pos, ceil_auroc, ceil_sp, sizes, labels_by_pep = [], [], [], [], [], []
        for v in sat.values():
            ks = sorted(v["cells"])
            da = [v["cells"][k][0] for k in ks]
            db = [v["cells"][k][1] for k in ks]
            avg = [(x + y) / 2 for x, y in zip(da, db)]
            p = [x >= rd.RESCUE_DELTA for x in avg]
            cells.append(len(ks))
            pos.append(sum(p))
            sizes.append(len(ks))
            labels_by_pep.append(avg)
            a = auroc(da, [y >= rd.RESCUE_DELTA for y in db])
            if a is not None:
                ceil_auroc.append(a)
            s = spearmanr(da, db).statistic
            if not math.isnan(s):
                ceil_sp.append(s)
        icc = icc_oneway(labels_by_pep)
        row = {
            "psi_wt_max": thr if thr < 99 else None,
            "n_peptides": len(sat),
            "n_proteins": len(accs),
            "n_clusters_cov80": len(clusters),
            "n_cells": sum(cells),
            "median_cells_per_peptide": statistics.median(cells) if cells else None,
            "positive_cell_rate": round(sum(pos) / sum(cells), 4) if cells else None,
            "ceiling_auroc_half_vs_half": round(statistics.mean(ceil_auroc), 4)
            if ceil_auroc else None,
            "ceiling_spearman_half_vs_half": round(statistics.mean(ceil_sp), 4)
            if ceil_sp else None,
            "icc_cells_within_peptide": round(icc, 4) if icc else None,
            "design_effect": round(design_effect(sizes, icc), 2) if icc and sizes else None,
        }
        if row["design_effect"]:
            row["effective_n_cells"] = round(row["n_cells"] / row["design_effect"], 1)
        out["levels"].append(row)

    # bộ quét, cùng bậc thang, để so cỡ mẫu
    psi, subs = data["psi_rep1"], data["subs"]
    scan_rows = []
    for thr in (3.0, 99.0):
        scan = rd.build_scanning(psi, seqs, subs, degron_psi_max=thr)
        accs = {rd.accession(p) for p in scan}
        n_cells = sum(len(v["cells"]) for v in scan.values())
        scan_rows.append({
            "psi_wt_max": thr if thr < 99 else None,
            "n_peptides": len(scan), "n_proteins": len(accs),
            "n_clusters_cov80": len({rep.get(a, a) for a in accs}),
            "n_cells": n_cells,
            "positive_cell_rate": round(statistics.mean(
                dp >= rd.RESCUE_DELTA for v in scan.values()
                for (_, dp) in v["cells"].values()), 4),
        })
    out["scanning"] = scan_rows

    # chồng lặp cụm giữa hai nguồn
    sat3 = rd.build_saturation(sat_a, sat_b, seqs, uniprot, degron_psi_max=3.0)
    scan3 = rd.build_scanning(psi, seqs, subs, degron_psi_max=3.0)
    cs = {rep.get(rd.accession(p), rd.accession(p)) for p in sat3}
    cq = {rep.get(rd.accession(p), rd.accession(p)) for p in scan3}
    out["overlap_cov80_clusters"] = {
        "saturation_clusters": len(cs), "scanning_clusters": len(cq),
        "shared": len(cs & cq), "saturation_only": len(cs - cq),
        "shared_peptide_names": len(set(sat3) & set(scan3)),
    }
    return out


# ------------------------------------------------------------------ đặc trưng

def featurize(rows, blocks):
    """rows: (seq, pos, mut_aa). blocks: tập con của {pair, comp, posidx, winComp, ctx}."""
    parts = []
    n = len(rows)
    if "pair" in blocks:
        wt = np.zeros((n, 20)); mu = np.zeros((n, 20))
        for j, (seq, pos, aa) in enumerate(rows):
            wt[j, AA2I[seq[pos - 1]]] = 1.0
            mu[j, AA2I[aa]] = 1.0
        parts += [wt, mu]
    if "comp" in blocks:
        comp = np.zeros((n, 20))
        cache = {}
        for j, (seq, pos, aa) in enumerate(rows):
            v = cache.get(seq)
            if v is None:
                v = np.zeros(20)
                for c in seq:
                    if c in AA2I:
                        v[AA2I[c]] += 1
                v /= len(seq)
                cache[seq] = v
            comp[j] = v
        parts.append(comp)
    if "posidx" in blocks:
        p = np.zeros((n, rd.TILE_LEN))
        for j, (seq, pos, aa) in enumerate(rows):
            if 1 <= pos <= rd.TILE_LEN:
                p[j, pos - 1] = 1.0
        parts.append(p)
    if "winComp" in blocks:
        w = np.zeros((n, 20))
        for j, (seq, pos, aa) in enumerate(rows):
            for o in range(-WINDOW, WINDOW + 1):
                if o == 0:
                    continue
                i = pos - 1 + o
                if 0 <= i < len(seq) and seq[i] in AA2I:
                    w[j, AA2I[seq[i]]] += 1.0
            parts_sum = w[j].sum()
            if parts_sum:
                w[j] /= parts_sum
        parts.append(w)
    if "ctx" in blocks:
        offs = [o for o in range(-WINDOW, WINDOW + 1) if o != 0]
        c = np.zeros((n, len(offs) * 20))
        for j, (seq, pos, aa) in enumerate(rows):
            for b, o in enumerate(offs):
                i = pos - 1 + o
                if 0 <= i < len(seq) and seq[i] in AA2I:
                    c[j, b * 20 + AA2I[seq[i]]] = 1.0
        parts.append(c)
    return np.hstack(parts)


MODELS = {
    "M0_composition_only": {"pair", "comp"},
    "M1_plus_position_index": {"pair", "comp", "posidx"},
    "M2_plus_window_composition": {"pair", "comp", "winComp"},
    "M3_plus_ordered_context": {"pair", "comp", "ctx"},
    "M4_context_and_position": {"pair", "comp", "ctx", "posidx"},
}


def ridge_fit(X, y, alphas=(0.1, 1.0, 10.0, 100.0, 1000.0)):
    """Ridge với alpha chọn bằng PRESS (LOO giải tích).

    Dùng phân rã riêng của ma trận Gram `Xc' Xc` (p × p, p <= 228) thay cho SVD của
    `Xc` (n × p, n tới 8 × 10^4): cùng nghiệm, nhanh hơn khoảng một bậc. Giá trị riêng
    rất nhỏ bị cắt, nên nghiệm vẫn xác định khi các cột one-hot phụ thuộc tuyến tính.
    """
    Xm = X.mean(0); ym = y.mean()
    Xc = X - Xm; yc = y - ym
    G = Xc.T @ Xc
    evals, V = np.linalg.eigh(G)
    keep = evals > 1e-9 * max(evals.max(), 1.0)
    evals, V = evals[keep], V[:, keep]
    s = np.sqrt(evals)
    U = (Xc @ V) / s
    Vt = V.T
    Uty = U.T @ yc
    best = None
    for a in alphas:
        d = s ** 2 / (s ** 2 + a)
        resid = yc - U @ (d * Uty)
        h = (U ** 2 * d).sum(1)
        press = float(((resid / np.maximum(1 - h, 1e-8)) ** 2).sum())
        if best is None or press < best[0]:
            best = (press, a, d)
    _, alpha, d = best
    w = Vt.T @ (d * Uty / s)
    return w, float(ym - Xm @ w), alpha


def rows_and_labels(dataset, kind):
    """-> peptides list, rows, y, pep_index"""
    rows, y, idx, peps = [], [], [], []
    for pep, v in sorted(dataset.items()):
        seq = v["seq"]
        start = len(rows)
        if kind == "scan":
            for pos in sorted(v["cells"]):
                aa, dp = v["cells"][pos]
                rows.append((seq, pos, aa)); y.append(dp)
        else:
            for (pos, aa) in sorted(v["cells"]):
                da, db = v["cells"][(pos, aa)]
                rows.append((seq, pos, aa)); y.append((da + db) / 2)
        if len(rows) > start:
            peps.append(pep)
            idx.append((start, len(rows)))
    return peps, rows, np.asarray(y, dtype=float), idx


def macro_auroc(scores, y, idx):
    per = []
    for a, b in idx:
        v = auroc(scores[a:b], y[a:b] >= rd.RESCUE_DELTA)
        if v is not None:
            per.append(v)
        else:
            per.append(None)
    ok = [v for v in per if v is not None]
    return (statistics.mean(ok) if ok else None), per


# ------------------------------------------------------------------ lệnh: model

def cmd_model(data, n_seeds=5, n_folds=5):
    rep = data["clusters"]
    rng_master = np.random.default_rng(SEED)
    out = {"window": WINDOW, "n_seeds": n_seeds, "n_folds": n_folds,
           "metric": "AUROC mức ô, trung bình macro theo peptide", "scanning": {},
           "saturation_transfer": {}}

    # ---------- (1) nội bộ bộ quét, chia theo cụm
    peps, rows, y, idx = rows_and_labels(data["scan"], "scan")
    groups = np.array([rep.get(rd.accession(p), rd.accession(p)) for p in peps])
    feats = {name: featurize(rows, blocks) for name, blocks in MODELS.items()}
    out["scanning"]["n_peptides"] = len(peps)
    out["scanning"]["n_cells"] = len(rows)
    out["scanning"]["n_clusters"] = len(set(groups))
    out["scanning"]["n_features"] = {k: int(v.shape[1]) for k, v in feats.items()}

    per_pep = {name: {} for name in MODELS}      # pep -> list AUROC theo seed
    seed_macro = {name: [] for name in MODELS}
    uniq = np.array(sorted(set(groups)))
    for seed in range(n_seeds):
        rng = np.random.default_rng(rng_master.integers(1 << 30))
        order = rng.permutation(len(uniq))
        fold_of = {uniq[g]: i % n_folds for i, g in enumerate(order)}
        pep_fold = np.array([fold_of[g] for g in groups])
        macro = {name: [] for name in MODELS}
        for f in range(n_folds):
            te_pep = np.where(pep_fold == f)[0]
            tr_pep = np.where(pep_fold != f)[0]
            tr_mask = np.zeros(len(rows), dtype=bool)
            for i in tr_pep:
                a, b = idx[i]; tr_mask[a:b] = True
            te_mask = ~tr_mask
            for name in MODELS:
                X = feats[name]
                w, b0, _ = ridge_fit(X[tr_mask], y[tr_mask])
                s_all = X @ w + b0
                for i in te_pep:
                    a, b = idx[i]
                    v = auroc(s_all[a:b], y[a:b] >= rd.RESCUE_DELTA)
                    if v is not None:
                        per_pep[name].setdefault(peps[i], []).append(v)
                        macro[name].append(v)
        for name in MODELS:
            seed_macro[name].append(statistics.mean(macro[name]))

    out["scanning"]["macro_auroc"] = {
        name: {"mean": round(statistics.mean(v), 4),
               "sd_across_seeds": round(statistics.pstdev(v), 4)}
        for name, v in seed_macro.items()}

    # phép so ghép cặp theo peptide (trung bình các seed), bootstrap theo CỤM
    pep_mean = {name: {p: statistics.mean(v) for p, v in d.items()}
                for name, d in per_pep.items()}
    pep_group = {p: rep.get(rd.accession(p), rd.accession(p)) for p in peps}
    out["scanning"]["paired_vs_M0"] = {}
    for name in MODELS:
        if name == "M0_composition_only":
            continue
        common = sorted(set(pep_mean[name]) & set(pep_mean["M0_composition_only"]))
        diffs = np.array([pep_mean[name][p] - pep_mean["M0_composition_only"][p]
                          for p in common])
        gl = [pep_group[p] for p in common]
        out["scanning"]["paired_vs_M0"][name] = cluster_bootstrap(diffs, gl)
        out["scanning"]["paired_vs_M0"][name]["wilcoxon_p"] = (
            float(wilcoxon(diffs).pvalue) if np.any(diffs != 0) else 1.0)
        out["scanning"]["paired_vs_M0"][name]["n_peptides"] = len(common)
        out["scanning"]["paired_vs_M0"][name]["win_rate"] = round(
            float((diffs > 0).mean()), 4)

    # ---------- (2) chuyển sang bộ bão hòa (cụm trùng bị loại khỏi train)
    s_peps, s_rows, s_y, s_idx = rows_and_labels(data["sat"], "sat")
    s_groups = set(rep.get(rd.accession(p), rd.accession(p)) for p in s_peps)
    keep = np.array([g not in s_groups for g in groups])
    tr_mask = np.zeros(len(rows), dtype=bool)
    for i in np.where(keep)[0]:
        a, b = idx[i]; tr_mask[a:b] = True
    out["saturation_transfer"]["n_scanning_peptides_kept_for_training"] = int(keep.sum())
    out["saturation_transfer"]["n_scanning_peptides_dropped_cluster_overlap"] = int(
        (~keep).sum())
    out["saturation_transfer"]["n_saturation_peptides"] = len(s_peps)
    out["saturation_transfer"]["n_saturation_cells"] = len(s_rows)
    out["saturation_transfer"]["note"] = (
        "Huấn luyện CHỈ trên bộ quét, chấm trên bộ bão hòa. Mọi peptide quét có cụm protein"
        " cov80 trùng với bộ bão hòa đã bị loại khỏi tập huấn luyện. Thay thế của bộ quét"
        " gần như toàn bộ là ->R, nên đây là phép chuyển sang 19 thay thế CHƯA THẤY.")
    s_feats = {name: featurize(s_rows, blocks) for name, blocks in MODELS.items()}
    sat_pep_auroc = {}
    for name, blocks in MODELS.items():
        X = feats[name]
        w, b0, alpha = ridge_fit(X[tr_mask], y[tr_mask])
        s = s_feats[name] @ w + b0
        m, per = macro_auroc(s, s_y, s_idx)
        sat_pep_auroc[name] = {p: v for p, v in zip(s_peps, per) if v is not None}
        # mức vị trí: gộp 19 thay thế
        pos_sp = []
        for (a, b), pep in zip(s_idx, s_peps):
            lab, sc = {}, {}
            for (seq, pos, aa), yy, ss in zip(s_rows[a:b], s_y[a:b], s[a:b]):
                lab.setdefault(pos, []).append(yy); sc.setdefault(pos, []).append(ss)
            ks = sorted(lab)
            if len(ks) >= 5:
                r = spearmanr([statistics.mean(sc[k]) for k in ks],
                              [statistics.mean(lab[k]) for k in ks]).statistic
                if not math.isnan(r):
                    pos_sp.append(r)
        out["saturation_transfer"].setdefault("macro_auroc", {})[name] = {
            "value": round(m, 4) if m else None, "alpha": alpha,
            "position_level_spearman": round(statistics.mean(pos_sp), 4) if pos_sp else None,
        }
    out["saturation_transfer"]["paired_vs_M0"] = {}
    base = sat_pep_auroc["M0_composition_only"]
    s_pep_group = {p: rep.get(rd.accession(p), rd.accession(p)) for p in s_peps}
    for name in MODELS:
        if name == "M0_composition_only":
            continue
        common = sorted(set(sat_pep_auroc[name]) & set(base))
        diffs = np.array([sat_pep_auroc[name][p] - base[p] for p in common])
        r = cluster_bootstrap(diffs, [s_pep_group[p] for p in common])
        r["n_peptides"] = len(common)
        r["win_rate"] = round(float((diffs > 0).mean()), 4)
        r["wilcoxon_p"] = float(wilcoxon(diffs).pvalue) if np.any(diffs != 0) else 1.0
        out["saturation_transfer"]["paired_vs_M0"][name] = r

    # lưu để lệnh power dùng lại
    (HERE / "paired-diffs.json").write_text(json.dumps({
        "scanning": {n: {p: pep_mean[n][p] for p in pep_mean[n]} for n in MODELS},
        "scanning_group": pep_group,
        "saturation": {n: sat_pep_auroc[n] for n in MODELS},
        "saturation_group": s_pep_group,
    }) + "\n", encoding="utf-8")
    return out


def cluster_bootstrap(diffs, group_labels, n_boot=4000, seed=SEED):
    """Bootstrap theo CỤM (đơn vị suy luận), trả trung bình + CI 95% + SD."""
    diffs = np.asarray(diffs, dtype=float)
    by = {}
    for d, g in zip(diffs, group_labels):
        by.setdefault(g, []).append(d)
    keys = list(by)
    arrs = [np.asarray(by[k]) for k in keys]
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    k = len(keys)
    for i in range(n_boot):
        pick = rng.integers(0, k, k)
        boots[i] = np.concatenate([arrs[j] for j in pick]).mean()
    return {"mean": round(float(diffs.mean()), 4),
            "ci95": [round(float(np.quantile(boots, 0.025)), 4),
                     round(float(np.quantile(boots, 0.975)), 4)],
            "sd_cluster_bootstrap": round(float(boots.std(ddof=1)), 4),
            "n_clusters": k}


# ------------------------------------------------------------------ lệnh: identify

def cmd_identify(data, n_boot=40):
    """Rủi ro LeBlanc trên nhãn hiệu ứng đột biến, theo đúng khuôn reframe §11.2."""
    rep = data["clusters"]
    out = {"n_bootstrap": n_boot, "window": WINDOW,
           "framework": ("Bootstrap theo CỤM protein. Với mỗi véc-tơ trọng số: |mu|/SD theo"
                         " từng hệ số, tỉ lệ hệ số có |mu|/SD > 2, đồng thuận dấu, và tái"
                         " lập nửa–nửa. So trực tiếp được với bảng reframe §11.2, nơi nhãn"
                         " là PSI MỨC PEPTIDE và chỉ 28,9% ô vị trí tách khỏi 0."),
           "sources": {}}

    for tag, kind in (("scanning_mutation_effect", "scan"),
                      ("saturation_mutation_effect", "sat")):
        peps, rows, y, idx = rows_and_labels(data[kind], kind)
        groups = np.array([rep.get(rd.accession(p), rd.accession(p)) for p in peps])
        X = featurize(rows, {"pair", "comp", "ctx"})
        offs = [o for o in range(-WINDOW, WINDOW + 1) if o != 0]
        n_ctx = len(offs) * 20
        ctx_slice = slice(X.shape[1] - n_ctx, X.shape[1])
        pair_slice = slice(0, 40)

        uniq = np.array(sorted(set(groups)))
        g2p = {}
        for i, g in enumerate(groups):
            g2p.setdefault(g, []).append(i)
        rng = np.random.default_rng(SEED)
        W = []
        for _ in range(n_boot):
            pick = rng.integers(0, len(uniq), len(uniq))
            sel = []
            for j in pick:
                for i in g2p[uniq[j]]:
                    a, b = idx[i]
                    sel.append(np.arange(a, b))
            sel = np.concatenate(sel)
            w, _, _ = ridge_fit(X[sel], y[sel])
            W.append(w)
        W = np.array(W)

        def stability(block, label, collapse=None):
            Wb = W[:, block]
            if collapse == "offset":
                Wb = Wb.reshape(Wb.shape[0], len(offs), 20).sum(1)
            mu, sd = Wb.mean(0), Wb.std(0, ddof=1)
            t = np.abs(mu) / np.maximum(sd, 1e-12)
            sign = np.maximum((W[:, block].reshape(W.shape[0], -1) > 0).mean(0),
                              1 - (W[:, block].reshape(W.shape[0], -1) > 0).mean(0)) \
                if collapse is None else np.maximum((Wb > 0).mean(0), 1 - (Wb > 0).mean(0))
            half = W.shape[0] // 2
            A = Wb[:half].mean(0); B = Wb[half:].mean(0)
            r = float(np.corrcoef(A, B)[0, 1]) if Wb.shape[1] > 2 else None
            return {"label": label, "n_coefficients": int(Wb.shape[1]),
                    "median_abs_mu_over_sd": round(float(np.median(t)), 2),
                    "share_abs_mu_over_sd_gt2": round(float((t > 2).mean()), 3),
                    "sign_consensus": round(float(np.mean(sign)), 3),
                    "half_half_reproducibility": round(r, 4) if r is not None else None}

        rowsout = [
            stability(ctx_slice, f"{len(offs)*20} ô (lệch vị trí, acid amin) — NGỮ CẢNH"),
            stability(ctx_slice, "tổng theo acid amin của ngữ cảnh (20 chiều)",
                      collapse="offset"),
            stability(pair_slice, "cặp thay thế (WT, đột biến) — 40 chiều"),
        ]
        out["sources"][tag] = {
            "n_peptides": len(peps), "n_cells": len(rows),
            "n_clusters": len(set(groups)), "vectors": rowsout}
    return out


# ------------------------------------------------------------------ lệnh: power

def cmd_power(data):
    path = HERE / "paired-diffs.json"
    if not path.exists():
        raise SystemExit("chạy `model` trước: cần paired-diffs.json")
    d = json.loads(path.read_text(encoding="utf-8"))
    out = {"note": ("Lực tính trên SD THẬT của chênh lệch ghép cặp giữa hai mô hình, không"
                    " phải SD của nhãn. Đơn vị bootstrap là CỤM protein cov80."),
           "alpha": 0.05, "target_power": 0.80, "sources": {}}
    z_a, z_b = 1.959964, 0.8416212
    for src, gkey in (("saturation", "saturation_group"), ("scanning", "scanning_group")):
        groups = d[gkey]
        base = d[src]["M0_composition_only"]
        rows = {}
        for name, vals in d[src].items():
            if name == "M0_composition_only":
                continue
            common = sorted(set(vals) & set(base))
            diffs = np.array([vals[p] - base[p] for p in common])
            gl = [groups[p] for p in common]
            cb = cluster_bootstrap(diffs, gl)
            se = cb["sd_cluster_bootstrap"]
            mde = (z_a + z_b) * se
            rows[name] = {
                "observed_delta": cb["mean"], "ci95": cb["ci95"],
                "se_cluster": se, "n_clusters": cb["n_clusters"],
                "mde_80pct_power": round(float(mde), 4),
                "power_at_observed": round(float(
                    normal_power(abs(cb["mean"]), se)), 3) if se > 0 else None,
            }
        # SD nhãn-mức-peptide dùng cho MDE tổng quát (không phụ thuộc mô hình nào)
        all_names = sorted(set(base))
        per_pep = np.array([base[p] for p in all_names])
        gl = [groups[p] for p in all_names]
        cb0 = cluster_bootstrap(per_pep - per_pep.mean(), gl)
        rows["_unpaired_reference"] = {
            "se_of_mean_auroc_cluster_bootstrap": cb0["sd_cluster_bootstrap"],
            "mde_80pct_power_unpaired_two_sample": round(
                float((z_a + z_b) * cb0["sd_cluster_bootstrap"] * math.sqrt(2)), 4),
            "meaning": ("Phép so KHÔNG ghép cặp cần mức chênh lớn hơn ≈ sqrt(2) lần. Ghép"
                        " cặp theo peptide là lý do lực đủ ở n nhỏ."),
        }
        out["sources"][src] = rows
    return out


# ------------------------------------------------------------------ lệnh: ceiling

def cmd_ceiling(data):
    """Đặt mọi con số vào CÙNG một thước đo: AUROC mức ô, trung bình macro theo peptide.

    Bốn mốc trên mỗi nguồn: trần đo lường (replicate / nửa–nửa), ΔPAP (mô hình degron công
    bố gần nhất), và hai mô hình của repo. Mục đích là tránh lặp lại lỗi D-025 mục 1: trần
    ở đây là **trần ĐO LƯỜNG**, không phải mức học được.
    """
    sys.path.insert(0, str(rd.TOPIC / "research/pap-baseline"))
    import pap_baseline as pb        # noqa: E402

    models = {n: pb.PAP(pb.WDIR / f"{n}_weights.h5") for n in ("cnn2w1", "cnn2w7")}
    out = {"metric": "AUROC mức ô, trung bình macro theo peptide", "scanning": {},
           "saturation": {}}

    # ---------- bộ quét: trần replicate + ΔPAP
    seqs, subs = data["seqs"], data["subs"]
    scan1 = data["scan"]
    scan2 = rd.build_scanning(rd.load_psi("rep2"), seqs, subs)
    shared = sorted(set(scan1) & set(scan2))
    jobs, per_rep, per_pap = {}, [], {n: [] for n in models}
    for pep in shared:
        s = scan1[pep]["seq"]
        jobs[(pep, 0, "")] = pb.clean(s)
        for pos, (aa, _) in scan1[pep]["cells"].items():
            jobs[(pep, pos, aa)] = pb.clean(s[:pos - 1] + aa + s[pos:])
    seq_list = sorted({v for v in jobs.values() if v})
    pap_score = {}
    for name, m in models.items():
        sc = dict(zip(seq_list, m.score(seq_list)))
        pap_score[name] = {k: sc.get(v) for k, v in jobs.items()}
    for pep in shared:
        ks = sorted(set(scan1[pep]["cells"]) & set(scan2[pep]["cells"]))
        if len(ks) < 10:
            continue
        lab2 = [scan2[pep]["cells"][k][1] >= rd.RESCUE_DELTA for k in ks]
        v = auroc([scan1[pep]["cells"][k][1] for k in ks], lab2)
        if v is not None:
            per_rep.append(v)
        for name in models:
            base = pap_score[name].get((pep, 0, ""))
            if base is None:
                continue
            sc = [pap_score[name].get((pep, k, scan1[pep]["cells"][k][0]))
                  for k in ks]
            if any(x is None or (isinstance(x, float) and math.isnan(x)) for x in sc):
                continue
            lab = [scan1[pep]["cells"][k][1] >= rd.RESCUE_DELTA for k in ks]
            a = auroc([x - base for x in sc], lab)
            if a is not None:
                per_pap[name].append(a)
    per_pep_pap = {"scanning": {n: {} for n in models},
                   "saturation": {n: {} for n in models}}
    for pep in shared:
        ks = sorted(set(scan1[pep]["cells"]) & set(scan2[pep]["cells"]))
        if len(ks) < 10:
            continue
        for name in models:
            base = pap_score[name].get((pep, 0, ""))
            if base is None:
                continue
            sc = [pap_score[name].get((pep, k, scan1[pep]["cells"][k][0])) for k in ks]
            if any(x is None or math.isnan(x) for x in sc):
                continue
            a = auroc([x - base for x in sc],
                      [scan1[pep]["cells"][k][1] >= rd.RESCUE_DELTA for k in ks])
            if a is not None:
                per_pep_pap["scanning"][name][pep] = a

    out["scanning"] = {
        "n_peptides_both_replicates": len(shared),
        "measurement_ceiling_rep1_scores_rep2_labels": round(
            statistics.mean(per_rep), 4) if per_rep else None,
        "n_peptides_in_ceiling": len(per_rep),
        "delta_pap": {n: {"macro_auroc": round(statistics.mean(v), 4),
                          "n_peptides": len(v)} for n, v in per_pap.items()},
        "note": ("Trần là trần ĐO LƯỜNG (một replicate chấm trên replicate kia), KHÔNG phải"
                 " mức dự đoán được từ trình tự."),
    }

    # ---------- bộ bão hòa: trần nửa–nửa + ΔPAP, trên ĐÚNG tập ô của thư mục này
    sat = data["sat"]
    jobs = {}
    for pep, v in sat.items():
        jobs[(pep, 0, "")] = pb.clean(v["seq"])
        for (pos, aa) in v["cells"]:
            jobs[(pep, pos, aa)] = pb.clean(v["seq"][:pos - 1] + aa + v["seq"][pos:])
    seq_list = sorted({x for x in jobs.values() if x})
    pap_score = {}
    for name, m in models.items():
        sc = dict(zip(seq_list, m.score(seq_list)))
        pap_score[name] = {k: sc.get(x) for k, x in jobs.items()}
    ceil, pap_m = [], {n: [] for n in models}
    for pep, v in sat.items():
        ks = sorted(v["cells"])
        da = [v["cells"][k][0] for k in ks]
        db = [v["cells"][k][1] for k in ks]
        avg = [(x + y) / 2 for x, y in zip(da, db)]
        a = auroc(da, [y >= rd.RESCUE_DELTA for y in db])
        if a is not None:
            ceil.append(a)
        lab = [x >= rd.RESCUE_DELTA for x in avg]
        for name in models:
            base = pap_score[name].get((pep, 0, ""))
            sc = [pap_score[name].get((pep,) + k) for k in ks]
            if base is None or any(x is None or math.isnan(x) for x in sc):
                continue
            aa_ = auroc([x - base for x in sc], lab)
            if aa_ is not None:
                pap_m[name].append(aa_)
                per_pep_pap["saturation"][name][pep] = aa_
    out["saturation"] = {
        "n_peptides": len(sat),
        "measurement_ceiling_half_vs_half": round(statistics.mean(ceil), 4) if ceil else None,
        "delta_pap": {n: {"macro_auroc": round(statistics.mean(v), 4),
                          "n_peptides": len(v)} for n, v in pap_m.items()},
        "cross_check_vs_pap_baseline_2026_10_14": {
            "expected_ceiling": 0.9519, "expected_delta_pap_cnn2w1": 0.7692},
    }
    (HERE / "pap-per-peptide.json").write_text(
        json.dumps(per_pep_pap) + "\n", encoding="utf-8")
    return out


# ------------------------------------------------------------------ lệnh: headline

def cmd_headline(data=None):
    """Câu đóng góp, ghép cặp đúng tập peptide dùng chung, bootstrap theo cụm.

    So M3 (có ngữ cảnh) và M0 (chỉ thành phần) với **ΔPAP cnn2w7** — mô hình degron công
    bố gần nhất — trên ĐÚNG những peptide cả ba đều chấm được, rồi đặt cạnh trần đo lường.
    """
    pd_path, pap_path = HERE / "paired-diffs.json", HERE / "pap-per-peptide.json"
    if not (pd_path.exists() and pap_path.exists()):
        raise SystemExit("chạy `model` và `ceiling` trước")
    mine = json.loads(pd_path.read_text(encoding="utf-8"))
    pap = json.loads(pap_path.read_text(encoding="utf-8"))
    ceil = json.loads((HERE / "ceiling.json").read_text(encoding="utf-8"))
    out = {"metric": "AUROC mức ô, trung bình macro theo peptide",
           "note": ("Mọi phép so GHÉP CẶP trên cùng peptide, bootstrap theo CỤM protein"
                    " cov80. Trần là trần ĐO LƯỜNG, không phải mức học được."),
           "sources": {}}
    for src, gkey, ceil_key in (("scanning", "scanning_group",
                                 "measurement_ceiling_rep1_scores_rep2_labels"),
                                ("saturation", "saturation_group",
                                 "measurement_ceiling_half_vs_half")):
        groups = mine[gkey]
        row = {"ceiling_measurement": ceil[src][ceil_key], "comparisons": {}}
        for ref_name in ("cnn2w1", "cnn2w7"):
            ref = pap[src][ref_name]
            for mod in ("M0_composition_only", "M3_plus_ordered_context"):
                common = sorted(set(mine[src][mod]) & set(ref))
                if len(common) < 10:
                    continue
                diffs = np.array([mine[src][mod][p] - ref[p] for p in common])
                cb = cluster_bootstrap(diffs, [groups[p] for p in common])
                cb["n_peptides"] = len(common)
                cb["win_rate"] = round(float((diffs > 0).mean()), 4)
                cb["wilcoxon_p"] = float(wilcoxon(diffs).pvalue)
                cb["mean_model"] = round(float(np.mean(
                    [mine[src][mod][p] for p in common])), 4)
                cb["mean_delta_pap"] = round(float(np.mean([ref[p] for p in common])), 4)
                row["comparisons"][f"{mod}_vs_dPAP_{ref_name}"] = cb
        out["sources"][src] = row
    return out


def normal_power(delta, se, alpha=0.05):
    from scipy.stats import norm
    z = norm.ppf(1 - alpha / 2)
    return float(norm.cdf(delta / se - z) + norm.cdf(-delta / se - z))


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command",
                    choices=["ladder", "identify", "model", "ceiling", "power",
                             "headline", "all"])
    args = ap.parse_args()
    cmds = ["ladder", "identify", "model", "ceiling", "power", "headline"] \
        if args.command == "all" else [args.command]
    data = None
    for c in cmds:
        if data is None and c not in ("power", "headline"):
            data = rd.load_all()
        if c == "ladder":
            res = cmd_ladder(data)
        elif c == "identify":
            res = cmd_identify(data)
        elif c == "model":
            res = cmd_model(data)
        elif c == "ceiling":
            res = cmd_ceiling(data)
        elif c == "headline":
            res = cmd_headline()
        else:
            res = cmd_power(data)
        path = HERE / f"{c}.json"
        path.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"=== {c} -> {path.name}")
        print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
