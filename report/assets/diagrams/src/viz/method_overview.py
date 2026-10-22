"""Charts for Fig 3.7 (method overview). Real data only (see method_data.py); nothing is trained here.

Writes 2x PNGs to src/viz/inputs/: v2-bins.png, v2-heat-measured.png, v2-heat-predicted.png, v2-reliability.png
and v2-summary.json (every number printed in the figure, with its source).
Run: .venv/bin/python -I report/assets/diagrams/src/viz/method_overview.py
Sizes are planned placed sizes in Figma px; figure inches = px/100, dpi = 200, so 24 px text = 17.3 pt.
"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import method_data as md

OUT = HERE / 'inputs'
INK, MUTED, LINE = '#1E1E1E', '#4A5563', '#7A8594'
BLUE, VERM, SKY, GREEN = '#0072B2', '#D55E00', '#56B4E9', '#009E73'
FS = 17.3          # = 24 px at 100 px/in
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': FS, 'axes.edgecolor': LINE, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK, 'axes.linewidth': 1.2})
DPI = 200
AAS = md.AAS


def fig_px(w, h):
    return plt.figure(figsize=(w / 100, h / 100), dpi=DPI)


def ax_px(fig, w, h, left, bottom, width, height):
    return fig.add_axes([left / w, bottom / h, width / w, height / h])


def bins_chart(d):
    W, H = 440, 350
    fig = fig_px(W, H)
    ax = ax_px(fig, W, H, 92, 66, 330, 190)
    x = np.arange(1, 7)
    s, m = d['syn'], d['mut']
    ax.bar(x - 0.2, s['frac'], 0.38, color=BLUE, label=f"silent {s['key'][1]}{s['key'][0]}: PSI {s['psi']:.1f}")
    ax.bar(x + 0.2, m['frac'], 0.38, color=VERM, label=f"{m['wt']}{m['key'][0]}{m['key'][1]}: PSI {m['psi']:.1f}")
    ax.set_xticks(x); ax.set_xlim(0.4, 6.6); ax.set_ylim(0, 0.62); ax.set_yticks([0, 0.25, 0.5])
    ax.set_yticklabels(['0', '.25', '.5'])
    ax.set_xlabel('bin  (1 unstable, 6 stable)'); ax.set_ylabel('share of reads', labelpad=6)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.yaxis.grid(True, color='#E3E7EC', lw=1); ax.set_axisbelow(True)
    ax.legend(loc='lower left', bbox_to_anchor=(-0.28, 1.02), frameon=False, handlelength=1.0, handletextpad=0.5,
              labelspacing=0.15, borderaxespad=0)
    fig.savefig(OUT / 'v2-bins.png', transparent=False, facecolor='white'); plt.close(fig)


CMAP = LinearSegmentedColormap.from_list('div', [BLUE, '#FFFFFF', VERM])
CMAP.set_bad('#D5DBE3')


def heat(mat, name, vmax):
    W, H = 440, 416
    fig = fig_px(W, H)
    ax = ax_px(fig, W, H, 40, H - 6 - 308, 400, 308)          # 20 columns x 20 px, 28 rows x 11 px
    im = ax.imshow(np.ma.masked_invalid(mat), cmap=CMAP, vmin=-vmax, vmax=vmax, aspect='auto', interpolation='nearest')
    ax.set_xticks(range(20)); ax.set_xticklabels(list(AAS))
    for t in ax.get_xticklabels():
        t.set_fontfamily('DejaVu Sans Condensed')
    ax.xaxis.tick_bottom(); ax.tick_params(axis='x', length=0, pad=3)
    ax.set_yticks([0, 6, 13, 20, 27]); ax.set_yticklabels(['1', '7', '14', '21', '28'])
    ax.tick_params(axis='y', length=3, pad=3)
    for sp in ax.spines.values(): sp.set_visible(False)
    cax = ax_px(fig, W, H, 40 + 96, 38, 250, 14)
    cb = fig.colorbar(im, cax=cax, orientation='horizontal')
    cb.set_ticks([-2, 0, 2]); cb.set_ticklabels(['\u22122', '0', '+2']); cb.outline.set_visible(False)
    cax.tick_params(length=0, pad=3)
    fig.text(40 / W, 38 / H, '\u0394PSI', ha='left', va='bottom')
    fig.savefig(OUT / name, facecolor='white'); plt.close(fig)


def reliability(c):
    W, H = 440, 470
    fig = fig_px(W, H)
    ax = ax_px(fig, W, H, 92, 74, 330, 380)
    ax.plot([0, 1], [0, 1], ls='--', color=LINE, lw=1.6, label='ideal')
    for key, col, lab in (('rel_raw', VERM, 'raw score'), ('rel_platt', BLUE, 'after Platt')):
        pts = c[key]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], '-o', color=col, lw=2.4, ms=8,
                markeredgecolor='white', markeredgewidth=1.5, label=lab)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
    ax.set_xticklabels(['0', '.5', '1']); ax.set_yticklabels(['0', '.5', '1'])
    ax.set_xlabel('predicted probability'); ax.set_ylabel('observed share', labelpad=6)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.grid(True, color='#E3E7EC', lw=1); ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, handlelength=1.6, labelspacing=0.2, borderaxespad=0.1)
    fig.savefig(OUT / 'v2-reliability.png', facecolor='white'); plt.close(fig)


def main():
    base, oof = md.load()
    rows, score = md.per_peptide(base, oof)
    ex, med_sub, n_sub = md.pick_example(rows)
    pep, seq, meas, pred, info = md.matrices(base, score, ex['i'])
    d = md.bin_distributions(pep, seq, info, meas)
    c = md.calibration_numbers()
    vmax = 2.5
    assert np.nanmax(meas) <= vmax + 1e-9 and np.nanmin(meas) >= -vmax
    bins_chart(d); heat(meas, 'v2-heat-measured.png', vmax); heat(pred, 'v2-heat-predicted.png', vmax); reliability(c)
    sp_all = np.array([r['sp'] for r in rows])
    summary = dict(
        example=dict(peptide=pep, sequence=seq, psi_wt_internal=float(info['psi_wt']), n_cells=ex['n'],
                     spearman_oof=ex['sp'], pearson_oof=ex['pr'], max_dpsi=ex['ymax'],
                     selection_rule='among peptides with max dPSI>=2 and >=8 cells with dPSI>=1 (n=%d), the one whose Spearman is closest to that subset median (%.3f); not best-case' % (n_sub, med_sub)),
        all_peptides=dict(n=len(rows), median_spearman=float(np.median(sp_all)),
                          median_pearson=float(np.median([r['pr'] for r in rows]))),
        bins=d,
        calibration={k: v for k, v in c.items() if not k.startswith('rel')},
        sources=['data/processed/learning-curve-sat-base.npz', 'data/processed/calibration-p6-oof.npz',
                 'data/processed/psi-sat_a.tsv', 'research/calibration-p6-2026-10-22/results.json'],
        scale=dict(heatmap_vmax=vmax, note='same colour scale for measured and predicted'))
    (OUT / 'v2-summary.json').write_text(json.dumps(summary, indent=2, default=float), encoding='utf-8')
    print(json.dumps({k: summary[k] for k in ('example', 'all_peptides')}, indent=1, default=float))


if __name__ == '__main__':
    main()
