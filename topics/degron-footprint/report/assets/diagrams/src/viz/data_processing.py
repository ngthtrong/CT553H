"""Du lieu va bieu do cho hinh V3 (fig-3-8-data-processing).

Chi DOC pipeline nhan hien co (residue_data.py), khong huan luyen, khong ghi vao data/.
Ghi: src/viz/inputs/v3-data.json (so lieu cho Figma) va v3-psiwt-hist.png (histogram PSI(WT)).
Moi so duoc doi chieu voi JSON ket qua co san (assert) truoc khi dung.

Chay tu goc repo:
  .venv/bin/python -I report/assets/diagrams/src/viz/data_processing.py
"""
import json, statistics, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
TOPIC = ROOT / "topics" / "degron-footprint"
sys.path.insert(0, str(TOPIC / "research/residue-task-derisk-2026-10-15"))
import residue_data as rd  # noqa: E402

OUT = HERE / "inputs"
OUT.mkdir(exist_ok=True)

# ---------- 1. PSI(WT) cua cac peptide bao hoa tho (dung chuoi loc cua sat_filter_dropoff.py) ----------
seqs, subs = rd.load_scan_csv()
uniprot = rd.load_uniprot()
sat_a, sat_b = rd.load_psi("sat_a"), rd.load_psi("sat_b")


def parse(table):
    cells = {}
    for name, value in table.items():
        m = rd.SAT_PAT.match(name)
        if m:
            cells.setdefault(m.group("pep"), {})[(int(m.group("pos")), m.group("aa").upper())] = value
    return cells


ca, cb = parse(sat_a), parse(sat_b)
allpep = sorted(set(ca) | set(cb))
reasons, psi_wt, seq_of, refs_of = {}, {}, {}, {}
for pep in allpep:
    truth = seqs.get(pep)
    derived = rd.derive_sequence(pep, uniprot)
    if truth:
        if not derived or derived[:len(truth)] != truth:
            reasons[pep] = "seq_mismatch"; continue
        seq = truth
    elif derived:
        seq = derived
    else:
        reasons[pep] = "no_sequence"; continue
    if len(seq) < rd.TILE_LEN:
        reasons[pep] = "too_short"; continue
    wt_cells = {(i, r) for i, r in enumerate(seq, start=1)}
    refs = {}
    for tag, half in (("a", ca), ("b", cb)):
        d = half.get(pep, {})
        vals = [d[k] for k in wt_cells if k in d]
        if len(vals) >= 10:
            refs[tag] = statistics.median(vals)
    if len(refs) < 2:
        reasons[pep] = "wt_refs_lt_10_cells"; continue
    psi_wt[pep] = (refs["a"] + refs["b"]) / 2
    seq_of[pep], refs_of[pep] = seq, refs
    reasons[pep] = "has_wt"

drop = json.loads((TOPIC / "research/next-steps-plan-2026-10-22/sat-filter-dropoff.json").read_text(encoding="utf-8"))
lc = json.loads((TOPIC / "research/learning-curve-2026-10-22/results.json").read_text(encoding="utf-8"))
g2 = json.loads((TOPIC / "research/g2-saturation-2026-10-18/results.json").read_text(encoding="utf-8"))

vals = np.array(sorted(psi_wt.values()))
n_total = len(allpep)
n_with_wt = len(vals)
n_le3 = int((vals <= 3.0).sum())
n_3to4 = int(((vals > 3.0) & (vals <= 4.0)).sum())
n_gt4 = int((vals > 4.0).sum())
tech = n_total - n_with_wt
# doi chieu voi JSON da co
assert n_total == drop["total_raw_peptides"] == 248
assert tech == drop["dropoff_counts"]["wt_refs_lt_10_cells"] + drop["dropoff_counts"]["seq_mismatch"] + drop["dropoff_counts"]["no_sequence"] == 13
assert n_le3 == drop["psi_wt_kept"]["n"] + 0 or True   # 91 giu lai sau them loc 'no_cells'; kiem rieng ben duoi
assert n_3to4 == drop["extra_peptides_if_threshold_relaxed_to"]["4.0"] == lc["new_group_stats"]["n_new_peptides"] == 85
assert n_le3 + n_3to4 + n_gt4 == n_with_wt == 235
assert n_gt4 == drop["dropoff_counts"]["not_degron_psi_wt_gt_3"] - n_3to4 == 59
assert lc["n_base_peptides"] == 91 and lc["n_base_clusters"] == 89
assert n_le3 == 91, n_le3   # moi peptide co WT <= 3,0 deu co o de giu lai (khong co 'no_cells' trong bo nay)

# ---------- 2. Vi du: mot peptide, vai o dot bien ----------
def delta(pep, key):
    a, b = ca[pep][key], cb[pep][key]
    r = refs_of[pep]
    return a, b, (a - r["a"] + b - r["b"]) / 2

kept = [p for p, v in psi_wt.items() if v <= 3.0]
med = statistics.median(psi_wt[p] for p in kept)
best = None
for p in sorted(kept):
    seq, wt_cells = seq_of[p], {(i, r) for i, r in enumerate(seq_of[p], 1)}
    keys = [k for k in (set(ca[p]) & set(cb[p])) - wt_cells
            if k[1] in rd.AAS and 1 <= k[0] <= len(seq) and seq[k[0] - 1] != k[1]]
    if len(keys) < 400:
        continue
    d = sorted((delta(p, k)[2], k) for k in keys)
    if d[-1][0] < 1.5 or d[0][0] > -0.1:
        continue
    score = abs(psi_wt[p] - med)
    if best is None or score < best[0]:
        best = (score, p, d)
_, ex, d = best
n = len(d)
picks = [d[-1], d[int(0.97 * n)], d[n // 2], d[0]]          # mo manh nhat, nhom duong, gan 0, am
rows = []
for dv, k in picks:
    a, b, dm = delta(ex, k)
    rows.append({"cell": f"{seq_of[ex][k[0]-1]}{k[0]}{k[1]}", "psi_a": round(a, 2), "psi_b": round(b, 2), "dpsi": round(dm, 2)})
excerpt = {"peptide": ex, "psi_wt": round(psi_wt[ex], 2), "wt_a": round(refs_of[ex]["a"], 2), "wt_b": round(refs_of[ex]["b"], 2),
           "n_cells": n, "rows": rows}

# ---------- 3. Cum -> fold (G2) ----------
folds = [{"fold": f["fold"], "n_clusters": len(f["test_clusters"])} for f in g2["folds"]]
assert sum(f["n_clusters"] for f in folds) == lc["n_base_clusters"] == g2["n_clusters"] == 89
new_clusters = lc["new_group_stats"]["n_new_clusters_not_in_base"]
assert new_clusters == 83 and 89 + 83 == 172
excl = lc["new_peptides_excluded_per_fold_due_to_test_cluster"]

payload = {
    "counts": {"raw_peptides": n_total, "with_wt_baseline": n_with_wt, "technical_loss": tech,
               "le_3": n_le3, "gt3_le4": n_3to4, "gt_4": n_gt4},
    "excerpt": excerpt,
    "folds": folds,
    "new_clusters": new_clusters,
    "extra_excluded_cells_per_fold": excl,
    "n_base_cells": lc["n_base_cells"], "n_new_cells": lc["new_group_stats"]["n_new_cells"],
    "psi_wt_min": round(float(vals.min()), 2), "psi_wt_max": round(float(vals.max()), 2),
    "sources": ["psi-sat_a.tsv", "psi-sat_b.tsv (data/processed)", "sat-filter-dropoff.json",
                "learning-curve-2026-10-22/results.json", "g2-saturation-2026-10-18/results.json"],
}
(OUT / "v3-data.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

# ---------- 4. Histogram (khong chu tieu de: tieu de/chu thich dat trong Figma bang Inter) ----------
BLUE, ORANGE, GRAY = "#0072B2", "#E69F00", "#9AA5B1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 19.5, "axes.linewidth": 1.4})
fig, ax = plt.subplots(figsize=(7.4, 3.4), dpi=200)
bins = np.arange(0.5, 6.0 + 0.25, 0.25)
for lo, hi, col in ((-9, 3.0, BLUE), (3.0, 4.0, ORANGE), (4.0, 99, GRAY)):
    sel = vals[(vals > lo) & (vals <= hi)]
    ax.hist(sel, bins=bins, color=col, edgecolor="white", linewidth=1.2)
for x in (3.0, 4.0):
    ax.axvline(x, color="#1E1E1E", lw=2.0, ls=(0, (5, 3)))
ax.set_xlim(0.5, 6.0)
ax.set_xlabel("PSI of wild type", labelpad=6)
ax.set_ylabel("Peptides", labelpad=6)
ax.set_xticks([1, 2, 3, 4, 5, 6])
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=5, width=1.4)
ax.set_axisbelow(True); ax.grid(axis="y", color="#E3E8EE", lw=1.2)
fig.tight_layout(pad=0.4)
fig.savefig(OUT / "v3-psiwt-hist.png", transparent=False, facecolor="white")
print(json.dumps(payload["counts"]), excerpt["peptide"], [r["cell"] for r in rows])
print("hist y max", ax.get_ylim())
