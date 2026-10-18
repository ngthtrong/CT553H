#!/usr/bin/env python3
"""Charts for the Notion summary page of 16 Oct 2026.

Built with matplotlib; no hand-placed SVG coordinates. Every value is read from a
result file under topics/degron-footprint/research/, except four milestones that are
locked by decision and passed in as named constants below (each with its source).

Run:   .venv/bin/python topics/degron-footprint/presentation/notion-2026-10-16/figures.py
Out:   png/*.png at 200 dpi on the project background.

Records no decision; see DECISIONS.md.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent


def repo_root(start: pathlib.Path) -> pathlib.Path:
    for p in [start, *start.parents]:
        if (p / "DECISIONS.md").is_file():
            return p
    raise SystemExit("DECISIONS.md not found")


ROOT = repo_root(HERE)
RES = ROOT / "topics/degron-footprint/research"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)

# Project palette, fixed in presentation/slide-content-2026-10-15.md
BG, INK, RED, TEAL, BLUE, GREY, AMBER = (
    "#FAFBFC", "#15323F", "#D1495B", "#2A9D8F", "#386FA4", "#8FA3AD", "#E9C46A")

for f in ("calibri.ttf", "calibrib.ttf"):
    p = pathlib.Path.home() / ".local/share/fonts/ms-office" / f
    if p.is_file():
        fm.fontManager.addfont(str(p))
plt.rcParams.update({
    "font.family": "Calibri" if any(f.name == "Calibri" for f in fm.fontManager.ttflist)
                   else "DejaVu Sans",
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": GREY,
    "xtick.color": GREY, "ytick.color": INK, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False,
})

# Milestones locked by decision (D-031, D-028); sources named in README.md
TARGET_AUROC = 0.7693       # dPAP cnn2w1, cell-level AUROC on the saturation matrix
CEILING_SAT = 0.9519        # measurement ceiling, saturation set
MDE = 0.0123                # minimum detectable effect, paired M3-M0
GAIN_VS_CNN2W7 = 0.0300     # M3 over dPAP cnn2w7 on the scanning set

enr = json.loads((RES / "variant-coverage-2026-10-15/enrichment.json").read_text())
mdl = json.loads((RES / "residue-task-derisk-2026-10-15/model.json").read_text())


def finish(fig, name, caption):
    fig.text(0.012, 0.012, caption, fontsize=7.4, color=GREY, style="italic", va="bottom")
    out = PNG / name
    fig.savefig(out, dpi=200, facecolor=BG)
    plt.close(fig)
    print(f"{name}  ({out.stat().st_size // 1024} KB)")


# ------------------------------------------------------------ 1. urgency forest
mh, cl = enr["mh_by_protein"], enr["mh_by_cluster_cov80"]
rows = [("Stratified by protein\n%s informative strata" % f"{mh['strata_informative']:,}", mh, RED),
        ("Stratified by cov80 cluster\n%s informative strata" % f"{cl['strata_informative']:,}", cl, BLUE)]

fig, ax = plt.subplots(figsize=(9.2, 3.0))
for i, (lab, d, col) in enumerate(rows):
    y = len(rows) - 1 - i
    a, b = d["ci95"]
    ax.plot([a, b], [y, y], color=col, lw=2.4, solid_capstyle="butt", zorder=3)
    for v in (a, b):
        ax.plot([v, v], [y - 0.1, y + 0.1], color=col, lw=2.4, zorder=3)
    ax.plot([d["or_mh"]], [y], "o", ms=11, color=col, mec=BG, mew=2, zorder=4)
    ax.annotate(f"{d['or_mh']:.3f}  [{a:.3f}, {b:.3f}]", (d["or_mh"], y),
                xytext=(0, 13), textcoords="offset points", ha="center",
                fontsize=11.5, fontweight="bold", color=col, zorder=5)
ax.axvline(1.0, color=GREY, ls="--", lw=1.2, zorder=2)
ax.annotate("OR = 1\nno difference", (1.0, 1.50), ha="center", va="bottom",
            fontsize=8.5, color=GREY)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([lab for lab, _, _ in rows][::-1], fontsize=10.5)
ax.set_ylim(-0.75, 1.9)
ax.set_xlim(0.92, 2.42)
ax.set_xlabel("Odds ratio, pathogenic vs benign  (Mantel–Haenszel)", fontsize=10)
ax.set_title("Measured degron regions are enriched for disease variants — at REGION level",
             fontsize=13.5, fontweight="bold", loc="left", pad=28)
ax.annotate("ClinVar of 12 Oct 2026 · 2.56 M missense variants mapped onto every peptide the GPS screen measured",
            (0, 1), xycoords="axes fraction", xytext=(0, 14), textcoords="offset points",
            fontsize=9.5, color=GREY)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout(rect=(0, 0.06, 1, 1))
finish(fig, "fig-01-urgency-forest.png",
       "Own measurement · research/variant-coverage-2026-10-15/enrichment.json · "
       "ClinVar (Landrum et al. 2018, PMID 29165669) — not for diagnostic use")

# ------------------------------------------------------- 2. scale decomposition
dec = mdl["scanning"]["paired_vs_M0"]
tot = dec["M3_plus_ordered_context"]["mean"]
seg = [("Composition of a ±3 window", dec["M2_plus_window_composition"]["mean"], BLUE),
       ("Order within that window", tot - dec["M2_plus_window_composition"]["mean"], TEAL),
       ("Absolute position in the peptide",
        dec["M4_context_and_position"]["mean"] - tot, RED)]

fig, ax = plt.subplots(figsize=(9.2, 2.5))
left = 0.0
for k, (lab, val, col) in enumerate(seg):
    ax.barh([0], [val], left=left, height=0.52, color=col, edgecolor=BG, linewidth=2.0)
    if val / tot > 0.35:
        ax.text(left + val / 2, 0, f"{lab}\n+{val:.4f}  ·  {val / tot * 100:.0f}% of the gain",
                ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    else:
        ax.annotate(f"{lab}: +{val:.4f}  ({val / tot * 100:.0f}%)", (left + val / 2, -0.26),
                    xytext=(0, -24 - 22 * (k - 1)), textcoords="offset points",
                    ha="center", va="center",
                    fontsize=9.5, color=col, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.2,
                                    connectionstyle="angle,angleA=0,angleB=90,rad=2"))
    left += val
ax.set_xlim(0, tot * 1.02)
ax.set_ylim(-1.35, 0.45)
ax.set_yticks([])
ax.set_xlabel("Cell-level AUROC gained over a composition-only model  "
              "(paired per peptide, bootstrap over 1,599 protein clusters)", fontsize=9.5)
ax.set_title("The signal sits at the ±3-neighbourhood scale, not at absolute position",
             fontsize=13.5, fontweight="bold", loc="left", pad=26)
ax.annotate(f"Total gain +{tot:.4f} AUROC  ·  2,288 peptides  ·  "
            "the right question is “composition at which scale”, not “composition or position”",
            (0, 1), xycoords="axes fraction", xytext=(0, 12), textcoords="offset points",
            fontsize=9.5, color=GREY)
ax.spines["left"].set_visible(False)
fig.tight_layout(rect=(0, 0.07, 1, 1))
finish(fig, "fig-02-scale-decomposition.png",
       "Own measurement · research/residue-task-derisk-2026-10-15/model.json")

# ------------------------------------------------------------ 3. the G2 target
sat = mdl["saturation_transfer"]["macro_auroc"]
bars = [("Measurement ceiling of the assay", CEILING_SAT, TEAL),
        ("ΔPAP cnn2w1 — published control, the TARGET", TARGET_AUROC, RED),
        ("M3, ±3 context — where this thesis is now", sat["M3_plus_ordered_context"]["value"], BLUE),
        ("M0, composition only — honest baseline", sat["M0_composition_only"]["value"], GREY)]

fig, ax = plt.subplots(figsize=(9.2, 3.2))
ys = range(len(bars))
ax.barh(list(ys), [v for _, v, _ in bars], height=0.6,
        color=[c for _, _, c in bars], edgecolor=BG, linewidth=2.0)
for y, (lab, v, col) in zip(ys, bars):
    ax.text(v + 0.004, y, f"{v:.4f}", va="center", ha="left",
            fontsize=11.5, fontweight="bold", color=col)
ax.axvline(0.5, color=GREY, lw=1.2, ls=":")
ax.annotate("0.5 = random", (0.5, len(bars) - 0.45), xytext=(4, 0), textcoords="offset points",
            fontsize=8.5, color=GREY, va="center")
ax.set_yticks(list(ys))
ax.set_yticklabels([lab for lab, _, _ in bars], fontsize=10.5)
ax.set_xlim(0.5, 1.0)
ax.set_xlabel("Cell-level AUROC on the saturation matrix, macro-averaged per peptide", fontsize=10)
ax.set_title("Gate G2 is a number, not a sentence: beat 0.7693, ceiling 0.9519",
             fontsize=13.5, fontweight="bold", loc="left", pad=26)
ax.annotate("91 peptides / 89 clusters / 47,847 cells · trained on the scanning set only, "
            "so the 19 substitutions are unseen",
            (0, 1), xycoords="axes fraction", xytext=(0, 12), textcoords="offset points",
            fontsize=9.5, color=GREY)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
gap = TARGET_AUROC - sat["M3_plus_ordered_context"]["value"]
ax.annotate(f"remaining gap −{gap:.4f}   (detection threshold {MDE:.4f})",
            (sat["M3_plus_ordered_context"]["value"] + gap / 2, 1.5),
            ha="center", va="center", fontsize=10, color=AMBER, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc=AMBER, ec=AMBER, alpha=0.25))
fig.tight_layout(rect=(0, 0.06, 1, 1))
finish(fig, "fig-03-g2-target.png",
       "Own measurement · research/residue-task-derisk-2026-10-15/model.json, ceiling.json · "
       "the ceiling is a measurement ceiling of the assay, not a learnable limit")

# ----------------------------------------------------------------- 4. roadmap
phases = [("Architecture search\nvariants A / B / C", 7, 3, BLUE),
          ("Hard checkpoint\npivot if the target is unmet", 10, 1, RED),
          ("Software\nprediction service + harness", 11, 3, AMBER),
          ("Write-up and defence", 14, 2, TEAL)]

fig, ax = plt.subplots(figsize=(9.2, 3.0))
for i, (lab, start_w, dur, col) in enumerate(phases):
    y = len(phases) - 1 - i
    ax.broken_barh([(start_w, dur)], (y - 0.28, 0.56), facecolors=col,
                   edgecolor=BG, linewidth=2.0)
    ax.text(start_w + dur / 2, y, f"W{start_w}\u2013{start_w + dur - 1}" if dur > 1 else f"W{start_w}",
            ha="center", va="center", color="white" if col != AMBER else INK,
            fontsize=10, fontweight="bold")
ax.axvline(7, color=GREY, lw=1.4, ls="--", zorder=1)
ax.annotate("now: end of week 6", (7, len(phases) - 0.42), xytext=(-7, 0),
            textcoords="offset points", ha="right", va="center", fontsize=9.5, color=GREY)
ax.set_xlim(6, 16)
ax.set_xticks(range(6, 17))
ax.set_xticklabels([f"W{w}" for w in range(6, 17)], fontsize=9.5)
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([lab for lab, _, _, _ in phases][::-1], fontsize=10.5)
ax.set_ylim(-0.7, len(phases) - 0.3)
ax.set_xlabel("Course week", fontsize=10)
ax.set_title("What is left: nine weeks, with a hard checkpoint in week 10",
             fontsize=13.5, fontweight="bold", loc="left", pad=26)
ax.annotate("G1 independent labels: MET   \u00b7   G2 positive contribution: PARTIAL   "
            "\u00b7   G3 application: DESIGNED, NOT BUILT",
            (0, 1), xycoords="axes fraction", xytext=(0, 12), textcoords="offset points",
            fontsize=9.5, color=GREY)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout(rect=(0, 0.07, 1, 1))
finish(fig, "fig-04-roadmap.png",
       "Derived from D-029 + D-031 + D-033 \u00b7 to be used as an authority it needs a decision entry of its own")
