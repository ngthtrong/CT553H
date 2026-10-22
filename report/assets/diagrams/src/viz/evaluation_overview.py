"""Biểu đồ cho hình V4 (fig-4-2-evaluation-overview): đọc kết quả có sẵn, KHÔNG tính lại thí nghiệm.

Chạy:  .venv/bin/python -I report/assets/diagrams/src/viz/evaluation_overview.py
Ghi:   report/assets/diagrams/src/viz/inputs/ev-{learning-curve,threshold,reliability,forest}.png
       report/assets/diagrams/src/viz/inputs/ev-numbers.json   (mọi số dùng trong hình, kèm file nguồn)

Quy ước kích thước (DESIGN-SPEC §2, §5): ảnh được đặt vào frame 1600 px với 100 px tương ứng 1 inch,
nên cỡ chữ 17,5 pt ≈ 24 px sau khi đặt. PNG xuất ở dpi 200 (gấp đôi kích thước đặt).
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
TOPIC = ROOT / 'topics' / 'degron-footprint'   # script nằm trong report/, không dưới topics/
RES = TOPIC / 'research'
OUT = HERE / 'inputs'
OUT.mkdir(exist_ok=True)

INK, MUTED, LINE = '#1E1E1E', '#4A5563', '#7A8594'
BLUE, ORANGE, VERM, GREEN, SKY, PINK = '#0072B2', '#E69F00', '#D55E00', '#009E73', '#56B4E9', '#CC79A7'
FS = 17.5            # pt; 100 px = 1 in when placed  ->  ~24 px
DPI = 200

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': FS, 'axes.labelsize': FS, 'xtick.labelsize': FS,
    'ytick.labelsize': FS, 'legend.fontsize': FS, 'text.color': INK, 'axes.labelcolor': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.edgecolor': LINE, 'axes.linewidth': 1.2,
    'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': 'white',
    'axes.facecolor': 'white', 'savefig.facecolor': 'white',
})

numbers = {}


def load(rel):
    p = RES / rel
    numbers.setdefault('_sources', []).append(str(p.relative_to(ROOT)))
    return json.loads(p.read_text(encoding='utf-8'))


def finish(fig, name):
    fig.savefig(OUT / name, dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- (a) learning curve
lc = load('learning-curve-2026-10-22/results.json')
v = lc['verdict']
x = np.arange(5)
ridge = v['ridge']['curve'] + [lc['results']['ridge']['ext']['macro_auroc_ensemble']]
net = v['gate_no_pap']['curve'] + [lc['results']['gate_no_pap']['ext']['macro_auroc_ensemble']]
numbers['learning_curve'] = {
    'levels': ['25%', '50%', '75%', '100%', '100% + extra'],
    'ridge_M3': ridge, 'gate_no_pap': net,
    'ridge_P1_delta_100_minus_50': v['ridge']['P1_delta_100_minus_50'],
    'ridge_P0_delta_ext_minus_100': v['ridge']['P0_delta_ext_minus_100'],
    'net_P1_delta_100_minus_50': v['gate_no_pap']['P1_delta_100_minus_50'],
    'net_P0_delta_ext_minus_100': v['gate_no_pap']['P0_delta_ext_minus_100'],
}
fig, ax = plt.subplots(figsize=(4.8, 3.5))
ax.axvline(3.5, color=LINE, lw=1.2, ls=(0, (4, 3)))
ax.plot(x, ridge, '-o', color=BLUE, lw=2.4, ms=8, mec='white', mew=1.5, label='Ridge')
ax.plot(x, net, '-s', color=ORANGE, lw=2.4, ms=8, mec=INK, mew=1.1, label='Gated net')
ax.set_xticks(x)
ax.set_xticklabels(['25', '50', '75', '100', '+extra'])
ax.set_xlabel('Training clusters (%)')
ax.set_ylabel('Macro AUROC')
ax.set_ylim(0.745, 0.83)
ax.set_yticks([0.75, 0.78, 0.81])
ax.legend(frameon=False, loc='lower right', bbox_to_anchor=(0.76, 0.0), handlelength=1.4, borderaxespad=0.1)
ax.grid(axis='y', color='#E4E8EE', lw=1)
ax.set_axisbelow(True)
fig.tight_layout(pad=0.4)
finish(fig, 'ev-learning-curve.png')

# ---------------------------------------------------------------- (b) threshold sensitivity
c = load('learning-curve-2026-10-22/results-c.json')
thr = ['3.5', '4.0', '4.5', '5.0']
rg = c['grid_ridge_cov80']['1.0']
nt = c['grid_net_cov80_main_delta']
numbers['threshold'] = {
    'thresholds': thr,
    'ridge_delta': {t: [rg[t]['delta'], *rg[t]['ci95']] for t in thr},
    'net_delta': {t: [nt[t]['delta'], *nt[t]['ci95']] for t in thr},
    'main_threshold_preregistered': c['prereg_threshold'], 'rescue_delta': c['main_rescue_delta'],
}
fig, ax = plt.subplots(figsize=(4.8, 3.5))
xs = np.arange(4)
for off, d, col, mk, lab, mec in ((-0.11, rg, BLUE, 'o', 'Ridge', 'white'), (0.11, nt, ORANGE, 's', 'Gated net', INK)):
    y = np.array([d[t]['delta'] for t in thr])
    lo = y - np.array([d[t]['ci95'][0] for t in thr])
    hi = np.array([d[t]['ci95'][1] for t in thr]) - y
    ax.errorbar(xs + off, y, yerr=[lo, hi], fmt=mk, color=col, ms=8, mec=mec, mew=1.3, elinewidth=2.2, capsize=0, label=lab)
ax.axhline(0, color=LINE, lw=1.2)
ax.axvspan(0.5, 1.5, color='#E1EFF8', zorder=0)
ax.text(1, -0.0033, 'main', ha='center', va='bottom', color=BLUE, fontsize=FS, fontweight='bold')
ax.set_xticks(xs)
ax.set_xticklabels(thr)
ax.set_xlabel('Max PSI of wild type')
ax.set_ylabel('Δ AUROC vs 3.0')
ax.set_ylim(-0.004, 0.034)
ax.set_yticks([0, 0.01, 0.02])
ax.legend(frameon=False, loc='upper right', handlelength=0.8, borderaxespad=0.1, ncol=2, columnspacing=0.8, handletextpad=0.5)
ax.grid(axis='y', color='#E4E8EE', lw=1)
ax.set_axisbelow(True)
fig.tight_layout(pad=0.4)
finish(fig, 'ev-threshold.png')

# ---------------------------------------------------------------- (c) reliability
cal = load('calibration-p6-2026-10-22/results.json')
m = cal['metrics']
fig, ax = plt.subplots(figsize=(4.8, 3.5))
ax.plot([0, 1], [0, 1], color=LINE, lw=1.4, ls=(0, (4, 3)))
rel_numbers = {}
for key, col, mk, lab, mec in (('raw', VERM, 's', 'Raw', INK), ('platt', BLUE, 'o', 'Platt', 'white')):
    rb = [b for b in m[key]['reliability'] if b['n_cells'] > 0]
    xp = np.array([b['mean_pred'] for b in rb])
    yo = np.array([b['obs_rate'] for b in rb])
    lo = yo - np.array([b['obs_rate_ci95'][0] for b in rb])
    hi = np.array([b['obs_rate_ci95'][1] for b in rb]) - yo
    ax.errorbar(xp, yo, yerr=[lo, hi], fmt='-' + mk, color=col, ms=7, mec=mec, mew=1.2, lw=2.0, elinewidth=1.6, capsize=0, label=lab)
    rel_numbers[key] = {'brier': m[key]['brier'], 'brier_ci95': m[key]['brier_ci95'], 'ece': m[key]['ece'],
                        'bins': [{'mean_pred': b['mean_pred'], 'obs_rate': b['obs_rate'], 'ci95': b['obs_rate_ci95'], 'n_cells': b['n_cells']} for b in rb]}
numbers['reliability'] = {**rel_numbers, 'raw_minus_platt_brier': cal['comparisons']['raw_minus_platt'],
                          'observed_positive_rate': m['observed_pos_rate'],
                          'event': 'delta PSI >= 1.0', 'n_test_cells': cal['n_test_cells'], 'n_test_peptides': cal['n_test_peptides']}
ax.set_xlim(-0.02, 1.0)
ax.set_ylim(-0.02, 1.0)
ax.set_xticks([0, 0.5, 1])
ax.set_yticks([0, 0.5, 1])
ax.set_xlabel('Predicted P(ΔPSI ≥ 1)')
ax.set_ylabel('Observed rate')
ax.legend(frameon=False, loc='upper left', handlelength=1.4, borderaxespad=0.1)
ax.grid(color='#E4E8EE', lw=1)
ax.set_axisbelow(True)
fig.tight_layout(pad=0.4)
finish(fig, 'ev-reliability.png')

# ---------------------------------------------------------------- (d) negative results (forest plot)
g2 = load('g2-saturation-2026-10-18/results.json')['comparisons']['ridge']              # gate_pap - ridge
e2 = load('g2-extension-2026-10-18/e2-candidates.json')['comparisons']
e3 = load('g2-extension-2026-10-18/e3-degformer-arch.json')['comparisons']['degformer_arch_minus_ridge']
p3 = load('pretrain-p3-2026-10-22/results.json')['verdict']['ext']['A_pre_minus_rand']
rows = [
    ('Sigmoid gate', g2, 'vs ridge'),
    ('FiLM', e2['film']['minus_ridge'], 'vs ridge'),
    ('Bilinear, rank 8', e2['bilinear']['minus_ridge'], 'vs ridge'),
    ('Cross-ridge', e2['cross_ridge']['minus_ridge'], 'vs ridge'),
    ('Degformer, retrained', e3, 'vs ridge'),
    ('Tile pre-training', p3, 'vs random init'),
]
numbers['negative_results'] = [{'design': r[0], 'reference': r[2], 'delta': r[1]['delta'], 'ci95': r[1]['ci95']} for r in rows]
fig, ax = plt.subplots(figsize=(14.24, 3.05))
ys = np.arange(len(rows))[::-1]
ax.axvline(0, color=LINE, lw=1.4)
for yv, (lab, r, ref) in zip(ys, rows):
    d, (lo, hi) = r['delta'], r['ci95']
    straddle = lo < 0 < hi
    col = ORANGE if straddle else VERM
    ax.plot([lo, hi], [yv, yv], color=col, lw=3.2, solid_capstyle='butt')
    ax.plot([d], [yv], 'o' if not straddle else 's', color=col, ms=9, mec=INK if straddle else 'white', mew=1.2, zorder=3)
    ax.text(1.02, yv, f'{d:+.3f}  [{lo:+.3f}, {hi:+.3f}]', va='center', ha='left', fontsize=FS, color=INK, transform=ax.get_yaxis_transform())
ax.set_yticks(ys)
ax.set_yticklabels([f'{r[0]}  ({r[2]})' for r in rows], fontsize=FS, color=INK)
ax.set_xlim(-0.078, 0.012)
ax.set_xticks([-0.06, -0.04, -0.02, 0])
ax.set_xlabel('Δ macro AUROC (paired, cluster-bootstrap 95% CI)', loc='left')
ax.tick_params(axis='y', length=0)
ax.grid(axis='x', color='#E4E8EE', lw=1)
ax.set_axisbelow(True)
fig.subplots_adjust(left=0.300, right=0.770, top=0.98, bottom=0.235)
finish(fig, 'ev-forest.png')

# ---------------------------------------------------------------- numbers for the Figma frame
folds = load('g2-saturation-2026-10-18/results.json')['folds']
numbers['protocol'] = {
    'seeds': lc['seeds'], 'n_base_peptides': lc['n_base_peptides'], 'n_base_clusters': lc['n_base_clusters'],
    'n_base_cells': lc['n_base_cells'], 'n_extra_peptides': lc['new_group_stats']['n_new_peptides'],
    'n_extra_clusters_not_in_base': lc['new_group_stats']['n_new_clusters_not_in_base'],
    'test_clusters_per_fold': [len(f['test_clusters']) for f in folds],
    'extra_cells_excluded_per_fold': lc['new_peptides_excluded_per_fold_due_to_test_cluster'],
    'n_boot': cal['n_boot'],
}
numbers['_sources'] = sorted(set(numbers['_sources']))
(OUT / 'ev-numbers.json').write_text(json.dumps(numbers, indent=1, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k: numbers[k] for k in ('protocol',)}, indent=1))
print('ok', sorted(p.name for p in OUT.glob('ev-*')))
