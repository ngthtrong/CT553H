import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch

BLUE, BLUE_F = "#386FA4", "#DCE9F5"
AMB, AMB_F = "#C77D0A", "#FFF4E0"
TEAL, TEAL_F = "#2A9D8F", "#D8F0EC"
GREY, GREY_F = "#5B6770", "#EEF1F4"
INK = "#1F2933"

fig, ax = plt.subplots(figsize=(12, 5.2), dpi=200)
ax.set_xlim(0, 120); ax.set_ylim(0, 52); ax.axis("off")

def box(x, y, w, h, text, fc, ec, lw=1.4, ls="-", bold=False, fs=10):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.6",
                       fc=fc, ec=ec, lw=lw, ls=ls)
    ax.add_patch(p)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
            color=INK, fontweight="bold" if bold else "normal", linespacing=1.3)

def arrow(a, b, ls="-", color=GREY, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, lw=1.3,
                                 ls=ls, color=color, connectionstyle=f"arc3,rad={rad}"))

def tag(x, y, s):
    ax.text(x, y, s, fontsize=9, fontweight="bold", color=AMB, ha="right", va="center")

# 1 input
box(1, 20, 17, 12, "Input\n28-residue peptide\n+ one substitution", GREY_F, GREY, fs=9.5)

# 2 feature blocks
ax.text(41, 47.8, "Feature blocks", ha="center", fontsize=10, color=GREY, style="italic")
ys = [37, 24, 7]
box(29, ys[0], 24, 8, "Substitution\n(position, from → to)", BLUE_F, BLUE)
box(29, ys[1], 24, 8, "±3 neighbourhood\ncomposition", BLUE_F, BLUE, lw=2.8, bold=True)
box(29, ys[2], 24, 8, "Whole-peptide\ncomposition", BLUE_F, BLUE)
ax.text(41, 22.4, "≈80% of the gain over\nwhole-peptide composition", ha="center", va="top",
        fontsize=8.5, color=BLUE, linespacing=1.25)
for y in ys:
    arrow((19.2, 26), (28.4, y + 4))

# 3 ablation
box(62, 20, 17, 12, "Ablation:\nwhich block helps?", BLUE_F, BLUE, fs=9.5)
for y in ys:
    arrow((53.6, y + 4), (61.4, 26))
ax.text(70.5, 18.6, "ridge on M3 blocks:\nAUROC 0.8082", ha="center", va="top", fontsize=8.5, color=BLUE, linespacing=1.25)

# 4 architectural component (open)
box(84, 20, 15.5, 12, "Architectural\ncomponent with\na stable benefit", AMB_F, AMB, ls="--", fs=9)
tag(99, 34, "open")
arrow((79.6, 26), (83.4, 26))

# 5 output
box(106, 26, 13.5, 8, "ΔPSI per\nsubstitution", TEAL_F, TEAL, bold=True, fs=9.5)
box(106, 11, 13.5, 8, "Per-prediction\nuncertainty", AMB_F, AMB, ls="--", fs=9)
tag(119.3, 20.6, "open")
arrow((99.9, 28.5), (105.4, 30), color=TEAL)
arrow((99.9, 22.5), (105.4, 15.5), ls="--", color=AMB)

# 6 whole-peptide labels (open)
box(60, 1, 40, 9, "Whole-peptide labels (far more numerous)\npossible auxiliary support for the\nresidue-level output — to be tested",
    AMB_F, AMB, ls="--", fs=8.5)
tag(99.5, 11.8, "open")
arrow((88, 10.7), (88, 19.4), ls="--", color=AMB)

# legend
ax.legend(handles=[Patch(fc=BLUE_F, ec=BLUE, label="preliminary evidence"),
                   Patch(fc=AMB_F, ec=AMB, ls="--", label="open, untested")],
          loc="upper right", bbox_to_anchor=(1.0, 1.02), frameon=False, fontsize=9, ncol=2)

# overflow check
fig.canvas.draw()
r = fig.canvas.get_renderer()
inv = ax.transData.inverted()
for t in ax.texts:
    bb = t.get_window_extent(r)
    x0, y0 = inv.transform((bb.x0, bb.y0)); x1, y1 = inv.transform((bb.x1, bb.y1))
    if x0 < 0 or x1 > 120 or y0 < 0 or y1 > 52:
        print("CLIPPED:", repr(t.get_text()), x0, x1, y0, y1)
import pathlib; fig.savefig(pathlib.Path(__file__).parent / "png" / "fig-method.png", bbox_inches="tight", facecolor="white")
print("saved")
