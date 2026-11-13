"""Render the already-computed CPU diagnostics; does not fit or score models."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result = json.loads((HERE/"results.json").read_text())
    thresholds = pd.read_csv(HERE/"threshold-sensitivity.csv")
    reliability = pd.read_csv(HERE/"reliability-bins.csv")
    agreement = pd.read_csv(HERE/"label-agreement.csv")
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.8), constrained_layout=True)
    ax = axes[0, 0]
    cohorts = ["W-full", "W-scanning-pairs", "T-rep1-full", "T-intersection-mean12"]
    labels = ["W / all substitutions", "W / scanning's 20 pairs", "T / replicate 1", "T / mean of replicates*"]
    for y, (cohort, label) in enumerate(zip(cohorts, labels)):
        row = next(x for x in result["transfer_vs_zero"] if x["cohort"] == cohort and x["axis"] == "all")
        lo, hi = row["ci95"]
        ax.errorbar(row["delta"], y, xerr=[[row["delta"]-lo], [hi-row["delta"]]],
                    fmt="o", color="#185d89" if cohort.startswith("W") else "#bb5027", capsize=4)
    ax.axvline(0, color="#555", linestyle="--", linewidth=1)
    ax.set(yticks=range(4), yticklabels=labels, xlabel="W5 minus zero MAE (PSI); 95% group CI",
           title="A. Regression benefit changes across populations")
    ax.invert_yaxis()
    ax.text(0, -.29, "*Both-replicate intersection; changed target, diagnostic only.", transform=ax.transAxes, fontsize=8)

    ax = axes[0, 1]
    recipes = ["esm2_35m-lora-D", "esm2_35m-frozen-D", "ordered-w5-D"]
    x = np.arange(3)
    for target, offset, color, label in [("mean", -.18, "#185d89", "Mean label >= 1"),
                                         ("both_halves", .18, "#b48320", "Both halves >= 1")]:
        vals = [thresholds[(thresholds.recipe == recipe) & (thresholds.threshold == 1)
                           & (thresholds.direction == "plus") & (thresholds.target == target)].iloc[0].delta*100
                for recipe in recipes]
        bars = ax.bar(x+offset, vals, .34, color=color, label=label)
        ax.bar_label(bars, fmt="%.1f", fontsize=9, padding=3)
    ax.set(xticks=x, xticklabels=["LoRA-D", "Frozen-D", "W5-D"], ylim=(0, 65),
           ylabel="Positive Precision@10 (%)", title="B. Fixed rankings under stricter hit labels")
    ax.legend(frameon=False, fontsize=9)
    ax.text(0, -.2, "Same 235 peptides and 2,350 choices; label targets differ.", transform=ax.transAxes, fontsize=8)

    ax = axes[1, 0]
    ax.plot([0, 1], [0, 1], "--", color="#777", linewidth=1)
    for cohort, color, label in [("W-full", "#185d89", "W / OOF"), ("T-rep1-full", "#bb5027", "T / final W5")]:
        f = reliability[(reliability.recipe == "ordered-w5-D") & (reliability.cohort == cohort)
                        & (reliability.axis == "all") & (reliability.direction == "plus") & (reliability.cells > 0)]
        ax.plot(f.mean_probability, f.observed_rate, "o-", color=color, label=label, markersize=5)
        for row in f[f.cells < 20].itertuples():
            offset = (-38, 12) if row.observed_rate == 0 else (5, 8)
            ax.annotate(f"n={int(row.cells)}", (row.mean_probability, row.observed_rate),
                        xytext=offset, textcoords="offset points", fontsize=8, color=color)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Mean predicted P(delta PSI >= 1)", ylabel="Observed positive rate",
           title="C. Positive-event reliability of W5")
    ax.legend(frameon=False)
    ax.text(0, -.2, "Sparse bins are labelled; all denominators: reliability-bins.csv.", transform=ax.transAxes, fontsize=8)

    ax = axes[1, 1]
    strata = ["le3", "gt3_le4", "gt4_le5", "gt5"]
    for direction, offset, color, label in [("plus", -.18, "#185d89", "Positive event"),
                                            ("minus", .18, "#bb5027", "Negative event")]:
        vals = []
        for s in strata:
            row = agreement[(agreement.threshold == 1) & (agreement.direction == direction) & (agreement.psi_stratum == s)].iloc[0]
            vals.append(row.event_jaccard)
        bars = ax.bar(np.arange(4)+offset, vals, .34, color=color, label=label)
        ax.bar_label(bars, fmt="%.2f", fontsize=9, padding=3)
    ax.annotate("No positive events", (3-.18, .02), xytext=(1.65, .22), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="#777"))
    ax.set(xticks=range(4), xticklabels=["<=3", "(3,4]", "(4,5]", ">5"], ylim=(0, .85),
           xlabel="Measured WT PSI", ylabel="Jaccard of events in halves a/b",
           title="D. Label agreement depends on effect and PSI")
    ax.legend(frameon=False, fontsize=9)
    fig.suptitle("Stored-prediction diagnostics / CPU only / posthoc development", fontsize=15)
    fig.savefig(HERE/"diagnostics.png", dpi=180)
    plt.close(fig)
    sources = ["results.json", "threshold-sensitivity.csv", "reliability-bins.csv", "label-agreement.csv"]
    (HERE/"figure-manifest.json").write_text(json.dumps(dict(generator_sha256=sha(Path(__file__)),
                sources={p: sha(HERE/p) for p in sources}, output=dict(path="diagnostics.png", sha256=sha(HERE/"diagnostics.png")),
                scope="Rendered stored metrics; no fitting, inference or new statistical comparison."), indent=2)+"\n")
    print("PASS diagnostic figure rendered")


if __name__ == "__main__":
    main()
