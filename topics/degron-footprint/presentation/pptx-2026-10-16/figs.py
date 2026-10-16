"""Generate raster figures used by the PPTX (data-derived heatmap, gradient, schematic grid)."""
import json, hashlib, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
SRC = os.path.join(HERE, "..", "deck-external-2026-10-16", "assets", "measured-example.json")
for f in ("calibri.ttf", "calibrib.ttf"):
    fm.fontManager.addfont(os.path.expanduser("~/.local/share/fonts/ms-office/" + f))
plt.rcParams["font.family"] = "Calibri"
CORAL, TEAL, INK, BG, GREY = "#D1495B", "#2A9D8F", "#15323F", "#FAFBFC", "#8FA3AD"
cmap = LinearSegmentedColormap.from_list("dpsi", [CORAL, BG, TEAL])

d = json.load(open(SRC))
seq, order = d["sequence"], d["aa_order"]
M = np.full((len(seq), 20), np.nan)
for c in d["cells"]:
    M[c["position"] - 1, order.index(c["aa"])] = c["mean_delta"]
lim = float(np.nanmax(np.abs(M)))
pos_mean = np.nanmean(M, axis=1)

# ---- heatmap + per-position bar ----
fig = plt.figure(figsize=(7.2, 5.5), dpi=220)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0.09, 0.17, 0.64, 0.77])
ax2 = fig.add_axes([0.76, 0.17, 0.21, 0.77])
im = ax.imshow(M, cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
for i, ch in enumerate(seq):
    j = order.index(ch)
    ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=True, fc="#E3E8EB", ec=INK, lw=.8))
ax.set_xticks(range(20)); ax.set_xticklabels(list(order), fontsize=8.5, color=INK)
ax.set_yticks(range(28)); ax.set_yticklabels([f"{i+1} {c}" for i, c in enumerate(seq)], fontsize=7.4, color=INK, family="DejaVu Sans Mono")
ax.xaxis.tick_top(); ax.tick_params(length=0)
for x in (4.5, 7.5, 12.5, 14.5, 17.5):   # hydrophobic | aromatic | polar | charged | special groups
    ax.axvline(x, color=BG, lw=2)
ax.set_xlabel("")
for s in ax.spines.values(): s.set_visible(False)
ax2.barh(range(28), pos_mean, color=[TEAL if v > 0 else CORAL for v in pos_mean], height=.72)
ax2.set_ylim(27.5, -.5); ax2.axvline(0, color=INK, lw=.8)
ax2.set_yticks([]); ax2.tick_params(labelsize=8, colors=INK)
ax2.set_xlabel("mean ΔPSI\nper position", fontsize=8.5, color=INK)
for s in ("top", "right", "left"): ax2.spines[s].set_visible(False)
ax2.set_facecolor(BG)
cax = fig.add_axes([0.09, 0.085, 0.45, 0.022])
cb = fig.colorbar(im, cax=cax, orientation="horizontal"); cb.ax.tick_params(labelsize=8, colors=INK)
cb.set_label("ΔPSI = PSI(substituted) − PSI(wild type)    ← less stable | more stable →", fontsize=8.5, color=INK)
cb.outline.set_visible(False)
fig.savefig(f"{OUT}/example-heatmap.png", facecolor=BG)
plt.close(fig)

# ---- schematic empty 28x20 grid (slide 15, no numbers) ----
fig, ax = plt.subplots(figsize=(3.3, 3.2), dpi=220)
fig.patch.set_facecolor(BG)
rng = np.random.RandomState(0)
G = np.zeros((28, 20))
ax.imshow(G, cmap=LinearSegmentedColormap.from_list("g", ["#E9EEF0", "#E9EEF0"]), aspect="auto")
ax.set_xticks(np.arange(-.5, 20), minor=True); ax.set_yticks(np.arange(-.5, 28), minor=True)
ax.grid(which="minor", color=BG, lw=1.2); ax.tick_params(which="both", length=0, labelleft=False, labelbottom=False)
for s in ax.spines.values(): s.set_visible(False)
for (r, c) in [(8, 3), (9, 3), (10, 3), (10, 11), (11, 3), (11, 7), (12, 3), (13, 3)]:
    ax.add_patch(plt.Rectangle((c-.5, r-.5), 1, 1, fc=TEAL, ec=BG, lw=1.2))
fig.savefig(f"{OUT}/grid-schematic.png", facecolor=BG, bbox_inches="tight", pad_inches=.02)
plt.close(fig)

# ---- diverging colour bar legend (slide 15) ----
w, h = 1200, 90
arr = (cmap(np.linspace(0, 1, w))[:, :3] * 255).astype("uint8")
Image.fromarray(np.repeat(arr[None], h, 0)).save(f"{OUT}/dpsi-colorbar.png")

# ---- PSI gradient bar (coral -> teal) ----
w, h = 1200, 90
arr = np.zeros((h, w, 3), dtype=np.uint8)
c0, c1 = np.array([0xD1, 0x49, 0x5B]), np.array([0x2A, 0x9D, 0x8F])
for x in range(w):
    arr[:, x] = (c0 + (c1 - c0) * x / (w - 1)).astype(np.uint8)
Image.fromarray(arr).save(f"{OUT}/psi-gradient.png")

meta = {"heatmap_source": "deck-external-2026-10-16/assets/measured-example.json", "sha256_source": hashlib.sha256(open(SRC, "rb").read()).hexdigest(),
        "peptide": d["peptide"], "wt_psi": d["wt_psi"], "cells": int(np.sum(~np.isnan(M))), "color_limit": lim}
json.dump(meta, open(f"{OUT}/figs-meta.json", "w"), indent=1)
print(meta)
