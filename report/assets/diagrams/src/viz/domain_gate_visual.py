"""V6 - 'The domain gate in practice': histogram of measured tile PSI and three real UI crops.

Reads (python -I): topics/degron-footprint/data/interim/gps-peptidome-rep1.tsv  (peptide, reads, psi)
Writes (src/viz/inputs/): v6-psi-hist.png, v6-card-{in,unknown,out}.png, v6-data.json
Run from the repository root:  .venv/bin/python -I report/assets/diagrams/src/viz/domain_gate_visual.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
TSV = ROOT / 'topics/degron-footprint/data/interim/gps-peptidome-rep1.tsv'
INP = HERE / 'inputs'

GREEN, VERM, INK, MUTED, LINE = '#009E73', '#D55E00', '#1E1E1E', '#4A5563', '#7A8594'
MIN_READS = 10          # same rule as research/r3-domain-gate-2026-10-22/local_analysis.py
THRESH = 4.0            # training-domain limit on PSI(WT)
EXAMPLES = {'A6NMZ7_COL6A6_28': 'tile 28', 'A6NMZ7_COL6A6_7': 'tile 7'}

# ---------------------------------------------------------------- data
df = pd.read_csv(TSV, sep='\t', usecols=['peptide', 'reads', 'psi'], na_values=['NA'])
df = df.dropna(subset=['reads', 'psi'])
df = df[df['reads'] >= MIN_READS]
psi = df['psi'].to_numpy(dtype=float)
n = len(psi)
share_in = float((psi <= THRESH).mean())
ex = {k: float(df.loc[df['peptide'] == k, 'psi'].iloc[0]) for k in EXAMPLES}

# ---------------------------------------------------------------- histogram
W_IN, H_IN, DPI = 14.72, 4.0, 200          # placed 1472 px wide -> PNG 2944 px (2x)
BIN = 0.05
edges = np.arange(1.0, 6.0 + BIN / 2, BIN)
counts, _ = np.histogram(np.clip(psi, 1.0, 6.0), bins=edges)
ctr = (edges[:-1] + edges[1:]) / 2
cols = [GREEN if c <= THRESH else VERM for c in ctr]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor='white')
ax = fig.add_axes([0.075, 0.22, 0.915, 0.74])
ax.bar(ctr, counts / 1000, width=BIN, color=cols, edgecolor='none')
ymax = counts.max() / 1000 * 2.0
ax.set_xlim(1.0, 6.0)
ax.set_ylim(0, ymax)
ax.axvline(THRESH, color=INK, lw=2.2, ls=(0, (6, 4)))
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_color(LINE)
ax.tick_params(colors=MUTED, labelsize=18, length=6, width=1.2)
ax.set_xlabel('Measured tile PSI (GPS screen, replicate 1)', fontsize=19, color=INK, labelpad=6)
ax.set_ylabel('Tiles (thousands)', fontsize=19, color=INK, labelpad=8)
ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5, integer=True, prune='upper'))

# zone labels (ink text; zone identity is carried by bar colour + these labels + the dashed line)
ax.text(THRESH - 0.08, ymax * 0.94, f'measured_in_domain\nPSI ≤ {THRESH:.1f}: {share_in * 100:.1f}% of tiles',
        ha='right', va='top', fontsize=18, color=INK, linespacing=1.25)
ax.text(THRESH + 0.08, ymax * 0.94, f'measured_out_of_domain\nPSI > {THRESH:.1f}: {(1 - share_in) * 100:.1f}% of tiles',
        ha='left', va='top', fontsize=18, color=INK, linespacing=1.25)

# example tiles: down-pointing markers just above their bar
marks = {}
for key, label in EXAMPLES.items():
    v = ex[key]
    i = int(np.clip((v - 1.0) // BIN, 0, len(counts) - 1))
    y = counts[i] / 1000 + ymax * 0.07
    ax.plot([v], [y], marker='v', ms=13, mfc=INK, mec='white', mew=2, zorder=5, ls='none')
    ax.text(v, y + ymax * 0.05, f'A6NMZ7 {label} \u00b7 PSI {v:.2f}', ha='center', va='bottom', fontsize=18, color=INK,
            zorder=5)
    px, py = ax.transData.transform((v, y))
    marks[key] = {'x_px': float(px), 'y_px_from_top': float(H_IN * DPI - py)}

fig.savefig(INP / 'v6-psi-hist.png', dpi=DPI, facecolor='white')
plt.close(fig)

# ---------------------------------------------------------------- UI crops (real screenshots from V0)
CARD_W, CARD_H = 2170, 1570           # crop box in the 2x screenshots (aspect 1.38)
X0 = 190
crops = {
    'in': ('ui-result-in-domain.png', 130),
    'unknown': ('ui-result-unknown.png', 130),
    'out': ('ui-result-out-of-domain.png', 60),
}
for k, (fn, y0) in crops.items():
    im = Image.open(INP / fn).convert('RGB')
    im.crop((X0, y0, X0 + CARD_W, y0 + CARD_H)).save(INP / f'v6-card-{k}.png', optimize=True)

# highlight boxes (in crop pixels, 2x) measured on the screenshots: status block of each card
boxes = {
    'in': [190, 396 - 130, 2350, 546 - 130],
    'unknown': [190, 396 - 130, 2350, 543 - 130],
    'out': [200, 261 - 60, 2340, 747 - 60],
}
box_json = {k: [b[0] - X0, b[1], b[2] - X0, b[3]] for k, b in boxes.items()}

json.dump({
    'source': str(TSV.relative_to(ROOT)),
    'min_reads': MIN_READS,
    'n_tiles': n,
    'threshold': THRESH,
    'share_psi_le_4': share_in,
    'median_psi': float(np.median(psi)),
    'example_psi': ex,
    'marker_px_in_hist_png_2x': marks,
    'hist_png_size': [int(W_IN * DPI), int(H_IN * DPI)],
    'card_crop_size_2x': [CARD_W, CARD_H],
    'highlight_boxes_in_card_2x': box_json,
}, open(INP / 'v6-data.json', 'w'), indent=2)
print(n, round(share_in, 4), ex, marks)
