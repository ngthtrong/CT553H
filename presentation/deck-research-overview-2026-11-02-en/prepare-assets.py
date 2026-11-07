"""Create standalone research figures and a hashed evidence bundle; no training/test-T access."""
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
HERE = Path(__file__).resolve().parent
TOPIC = next((p for p in HERE.parents if (p / 'data/README.md').exists()))
R = TOPIC / 'research'
ASSETS = HERE / 'assets'
ASSETS.mkdir(exist_ok=True)
VENDOR = HERE / 'vendor'
VENDOR.mkdir(exist_ok=True)
source_hashes = {}
downloads = []

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def read(name):
    p = R / name
    source_hashes[name] = digest(p)
    return json.loads(p.read_text(encoding='utf8'))

def download(url, name):
    p = VENDOR / name
    if not p.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            p.write_bytes(response.read())
    downloads.append(dict(path='vendor/' + name, url=url, sha256=digest(p)))
for weight in ['Regular', 'SemiBold']:
    download(f'https://raw.githubusercontent.com/google/fonts/main/ofl/bevietnampro/BeVietnamPro-{weight}.ttf', f'be-vietnam-pro-{weight.lower()}.ttf')
download('https://raw.githubusercontent.com/google/fonts/main/ofl/bevietnampro/OFL.txt', 'font-license.txt')
download('https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js', 'chart.umd.js')
download('https://cdn.jsdelivr.net/npm/chart.js@4.4.1/LICENSE.md', 'chart-license.md')
old = TOPIC / 'presentation/deck-2026-10-16/assets'
for name in ['fam188a.gif', 'fam188a-poster.png']:
    shutil.copy2(old / name, ASSETS / name)
    downloads.append(dict(path='assets/' + name, source=str((old / name).relative_to(TOPIC)), sha256=digest(ASSETS / name), attribution='Nikolakhs, I-TASSER predicted protein fold of Fam188a, Wikimedia Commons, CC BY-SA 3.0', url='https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif'))
for p in VENDOR.glob('*.ttf'):
    font_manager.fontManager.addfont(p)
plt.rcParams.update({'font.family': ['Be Vietnam Pro', 'DejaVu Sans'], 'font.size': 16, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.spines.left': False, 'axes.edgecolor': '#D6DFD3', 'text.color': '#193A2B', 'axes.labelcolor': '#617267', 'xtick.color': '#617267', 'ytick.color': '#193A2B', 'savefig.transparent': True, 'svg.fonttype': 'path', 'axes.titleweight': 'semibold', 'axes.grid': False, 'svg.hashsalt': 'degron-research-overview-2026-11-02'})
GREEN = '#18974C'
DARK = '#0A5032'
CORAL = '#C76242'
BLUE = '#477CA7'
MUTED = '#A9B7A8'
files = []

def save(fig, name):
    p = ASSETS / (name + '.svg')
    fig.savefig(p, bbox_inches='tight', pad_inches=0.16, metadata={'Date': None})
    plt.close(fig)
    p.write_text('\n'.join((line.rstrip() for line in p.read_text(encoding='utf8').splitlines())) + '\n', encoding='utf8')
    files.append(p.name)

def bars(name, labels, values, xlabel, colors=None, max_x=None, fmt='.3f'):
    fig, ax = plt.subplots(figsize=(11, 4.6))
    y = np.arange(len(labels))
    cols = colors or [GREEN] * len(labels)
    ax.barh(y, values, color=cols, height=0.48)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.tick_params(axis='y', length=0, pad=12)
    ax.set_xlabel(xlabel, loc='right', labelpad=12)
    ax.set_xlim(0, max_x or max(values) * 1.2)
    ax.xaxis.grid(True, color='#E3E8DF')
    ax.set_axisbelow(True)
    for i, v in enumerate(values):
        ax.text(v + ax.get_xlim()[1] * 0.018, i, format(v, fmt), va='center', weight='semibold', fontsize=17)
    fig.tight_layout()
    save(fig, name)

def forest(name, labels, deltas, cis, xlabel):
    fig, ax = plt.subplots(figsize=(10, 3.4 if len(labels) < 4 else 4.7))
    for i, (v, ci) in enumerate(zip(deltas, cis)):
        color = GREEN if ci[1] < 0 else BLUE if ci[0] > 0 else CORAL
        ax.errorbar(v, i, xerr=[[v - ci[0]], [ci[1] - v]], fmt='o', color=color, capsize=6, markersize=10, lw=3)
    ax.axvline(0, color=MUTED, lw=1.4, ls='--')
    ax.set_yticks(range(len(labels)), labels)
    ax.invert_yaxis()
    ax.tick_params(axis='y', length=0, pad=12)
    ax.set_xlabel(xlabel, labelpad=10)
    ax.xaxis.grid(True, color='#E3E8DF')
    fig.tight_layout()
    save(fig, name)
analysis = read('kaggle-roadmap-2026-10-31/output-analysis.json')
details = read('kaggle-roadmap-2026-10-31/output-analysis-details.json')
model = read('residue-task-derisk-2026-10-15/model.json')
g2 = read('g2-saturation-2026-10-18/results.json')
deg = read('r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json')
cal = read('calibration-p6-2026-10-22/results.json')
hif = read('slide-figures-2026-10-15/example-matrix.json')
replicate = read('full-data-audit/replicate-audit.json')
satquality = read('full-data-audit/saturation-matrix.json')
clinical = read('variant-coverage-2026-10-15/enrichment.json')
pre = read('pretrain-p3-2026-10-22/results.json')
curve = read('learning-curve-2026-10-22/results.json')
recluster = read('recluster-sensitivity-2026-10-22/results.json')
extra = read('r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json')
gate = read('r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json')

def metric(recipe, key='mae'):
    return analysis['recipes'][recipe]['ensemble']['all'][key]
context = model['scanning']['macro_auroc']
bars('context', ['Substitution + peptide composition', 'Add local composition', 'Add local order'], [context[k]['mean'] for k in ['M0_composition_only', 'M2_plus_window_composition', 'M3_plus_ordered_context']], 'Within-peptide AUROC · higher is better', [MUTED, BLUE, GREEN], 1)
arms = ['ordered-w5-' + x for x in 'ABCDE']
bars('training-range', ['PSI ≤ 3 only', 'PSI ≤ 4 only', 'PSI ≤ 5 only', 'Full PSI range', 'Full range, balanced'], [metric(k) for k in arms], 'MAE (PSI) · lower is better', [MUTED, BLUE, MUTED, GREEN, DARK], 0.56)
q1 = [analysis['contrasts'][f'ordered-w5-{x} minus ordered-w5-B; mae'] for x in 'DE']
forest('training-ci', ['Full range versus PSI ≤ 4 only', 'Balanced versus PSI ≤ 4 only'], [x['delta'] for x in q1], [x['ci_adjusted'] for x in q1], 'MAE difference · adjusted 97.5% CI')
fig, ax = plt.subplots(figsize=(10, 4.6))
for arm, label, color in [('B', 'PSI ≤ 4 only', BLUE), ('D', 'Full range', GREEN), ('E', 'Full range, balanced', CORAL)]:
    values = [analysis['recipes']['ordered-w5-' + arm]['ensemble']['strata'][s]['mae'] for s in ['le3', 'gt3_le4', 'gt4_le5', 'gt5']]
    ax.plot(range(4), values, 'o-', color=color, lw=3, ms=8, label=label)
ax.set_xticks(range(4), ['PSI ≤ 3', '3 < PSI ≤ 4', '4 < PSI ≤ 5', 'PSI > 5'])
ax.set_ylabel('MAE (PSI)')
ax.set_ylim(0.27, 0.55)
ax.yaxis.grid(True, color='#E3E8DF')
ax.legend(frameon=False, fontsize=13, loc='upper center', ncol=3)
fig.tight_layout()
save(fig, 'strata')
labels = ['Context Ridge', 'Ridge + ESM', 'Validation-based selection']
keys = ['ordered-w5-D', 'esm2_35m-context-D', 'nested-family-selection']
bars('esm-linear', labels, [metric(k, 'auroc_plus') for k in keys], 'Positive-event AUROC · full PSI range', [MUTED, GREEN, BLUE], 1)
bars('heads', ['One-hot + CNN', 'ESM + pointwise', 'ESM + CNN', 'ESM + multiple windows'], [metric(k) for k in ['onehot-cnn-D', 'esm2_35m-pointwise-D', 'esm2_35m-cnn-D', 'esm2_35m-mcnn-D']], 'MAE (PSI) · matched full-range training', [MUTED, BLUE, GREEN, DARK], 0.47, fmt='.4f')
c = analysis['contrasts']['esm2_35m-cnn-D minus esm2_35m-pointwise-D; mae']
forest('cnn-ci', ['CNN versus pointwise'], [c['delta']], [c['ci95']], 'MAE difference · descriptive 95% CI')
c = details['contrasts']['esm2_35m-mcnn-E minus esm2_35m-cnn-D; mae']
forest('mcnn-ci', ['Balanced multi-window model\nversus full-range CNN'], [c['delta']], [c['ci95']], 'MAE difference · descriptive 95% CI')
bars('transfer', ['CNN from scratch', 'Scanning-pretrained CNN', 'CNN pretrained on replicate means'], [metric(k) for k in ['cnn-transfer-scratch-D', 'cnn-transfer-dpsi_rep1-D', 'cnn-transfer-dpsi_rep12_mean-D']], 'MAE (PSI) · matched one-hot architecture', [MUTED, GREEN, BLUE], 0.46, fmt='.4f')
cc = [details['contrasts']['cnn-transfer-dpsi_rep1-D minus cnn-transfer-scratch-D; mae; ' + s] for s in ['scan20', 'other360']]
forest('transfer-pairs', ['20 types observed in scanning', '360 remaining types'], [v['delta'] for v in cc], [v['ci95'] for v in cc], 'MAE difference versus training from scratch · descriptive 95% CI')
refs = deg['references_macro_auroc']
bars('degformer', ['Ridge on the same test domain', 'Group-clean Degformer', 'ΔPAP'], [refs['ridge_ext4.0'], deg['macro_auroc_ensemble'], refs['DeltaPAP']], 'AUROC · evaluation on 91 peptides', [GREEN, BLUE, MUTED], 1)
fig, ax = plt.subplots(figsize=(9, 4.5))
xx = np.arange(3)
w = 0.32
for j, (key, label, color) in enumerate([('ordered-w5-D', 'Context Ridge', MUTED), ('esm2_35m-cnn-D', 'ESM + CNN', GREEN)]):
    vals = [metric(key, 'precision_plus_' + s + '_eligible_macro') * 100 for s in ['0.05', '0.1', '0.2']]
    ax.bar(xx + (j - 0.5) * w, vals, w, color=color, label=label)
    for x, v in zip(xx + (j - 0.5) * w, vals):
        ax.text(x, v + 1.5, f'{v:.1f}%', ha='center', fontsize=15)
ax.set_xticks(xx, ['Top 5%', 'Top 10%', 'Top 20%'])
ax.set_ylabel('Positive-event precision (%)')
ax.set_ylim(0, 75)
ax.legend(frameon=False, loc='upper right', fontsize=13)
ax.yaxis.grid(True, color='#E3E8DF')
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, 'utility')
fig, ax = plt.subplots(figsize=(9, 4.3))
for key, label, color in [('ordered-w5-D', 'Ridge', MUTED), ('esm2_35m-cnn-D', 'ESM + CNN', GREEN)]:
    vals = details['fold_mae'][key]
    ax.plot(range(1, 6), list(vals.values()), 'o-', label=label, lw=3, color=color, ms=9)
ax.set_xticks(range(1, 6))
ax.set_xlabel('Outer test groups')
ax.set_ylabel('MAE (PSI)')
ax.set_ylim(0.34, 0.45)
ax.legend(frameon=False)
ax.yaxis.grid(True, color='#E3E8DF')
fig.tight_layout()
save(fig, 'folds')
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot([0, 0.65], [0, 0.65], ls='--', color=MUTED, lw=1.5)
rr = cal['metrics']['platt']['reliability']
ax.plot([v['mean_pred'] for v in rr], [v['obs_rate'] for v in rr], 'o-', color=GREEN, lw=3, ms=7)
ax.set_xlim(0, 0.65)
ax.set_ylim(0, 0.65)
ax.set_xlabel('Predicted probability')
ax.set_ylabel('Observed frequency')
ax.grid(color='#E3E8DF')
fig.tight_layout()
save(fig, 'calibration')
aa = hif['aa_order']
matrix = np.array([[row.get(a, np.nan) if row.get(a) is not None else np.nan for row in hif['matrix']] for a in aa])
fig, ax = plt.subplots(figsize=(13, 5.3))
cmap = LinearSegmentedColormap.from_list('psi', ['#477CA7', '#F2F4EE', '#E9976B', '#AE432E'])
im = ax.imshow(matrix, aspect='auto', cmap=cmap, norm=TwoSlopeNorm(vmin=-0.6, vcenter=0, vmax=3.2), interpolation='nearest')
ax.set_xticks(range(28), list(hif['sequence']), fontsize=14)
ax.xaxis.tick_top()
ax.set_yticks(range(20), list(aa), fontsize=14)
ax.tick_params(length=0)
ax.set_xlabel('Position in the HIF1A peptide', labelpad=12)
ax.set_xticks(np.arange(-0.5, 28, 1), minor=True)
ax.set_yticks(np.arange(-0.5, 20, 1), minor=True)
ax.grid(which='minor', color='#F6F7F2', linewidth=1)
ax.add_patch(plt.Rectangle((8.5, -0.5), 5, 20, fill=False, edgecolor=DARK, lw=2.5))
cb = fig.colorbar(im, ax=ax, fraction=0.028, pad=0.03)
cb.set_label('Measured ΔPSI', fontsize=13)
cb.ax.tick_params(labelsize=11)
fig.tight_layout()
save(fig, 'hif-measured')
seeds = analysis['recipes']['esm2_35m-cnn-D']['seed_mae']
bars('seed-ensemble', ['Seed 17', 'Seed 29', 'Seed 43', 'Mean predictions'], list(seeds.values()) + [metric('esm2_35m-cnn-D')], 'MAE (PSI)', [MUTED, MUTED, MUTED, GREEN], 0.46, fmt='.4f')
bars('brier', ['Prevalence baseline', 'Calibrated Ridge'], [cal['metrics']['const']['brier'], cal['metrics']['platt']['brier']], 'Brier score · lower is better', [MUTED, GREEN], 0.15, fmt='.4f')
fig, ax = plt.subplots(figsize=(9, 4.3))
curves = details['learning_curve']
values = [curves[k]['mean_seed_mae'] for k in curves]
ax.plot([25, 50, 75, 100], values, 'o-', color=GREEN, lw=3, ms=9)
ax.set_xticks([25, 50, 75, 100])
ax.set_xlabel('% of training groups in a single fit')
ax.set_ylabel('Mean single-seed MAE')
ax.yaxis.grid(True, color='#E3E8DF')
fig.tight_layout()
save(fig, 'learning-curve')
fig, ax = plt.subplots(figsize=(11, 4.6))
labels = ['Context Ridge', 'ESM + pointwise', 'ESM + CNN', 'ESM + multiple windows', 'Scanning → CNN']
ks = ['ordered-w5-D', 'esm2_35m-pointwise-D', 'esm2_35m-cnn-D', 'esm2_35m-mcnn-E', 'cnn-transfer-dpsi_rep1-D']
for k, label, c in zip(ks, labels, [MUTED, BLUE, GREEN, DARK, CORAL]):
    x = metric(k)
    y = metric(k, 'auroc_plus')
    ax.scatter(x, y, s=160, color=c)
    ax.annotate(label, (x, y), xytext=(8, 8), textcoords='offset points', fontsize=13)
ax.set_xlabel('MAE (PSI) · lower is better')
ax.set_ylabel('Positive-event AUROC · higher is better')
ax.set_xlim(0.376, 0.43)
ax.set_ylim(0.819, 0.865)
ax.grid(color='#E3E8DF')
fig.tight_layout()
save(fig, 'tradeoff')
human_names = {'ordered-w5-D': 'Ridge · full range', 'ordered-w5-B': 'Ridge · PSI ≤ 4 only', 'ordered-w5-E': 'Ridge · balanced', 'esm2_35m-cnn-D': 'ESM + CNN · full range', 'esm2_35m-cnn-B': 'ESM + CNN · PSI ≤ 4 only', 'esm2_35m-mcnn-E': 'ESM + multiple windows · balanced', 'esm2_35m-pointwise-D': 'ESM + pointwise · full range', 'onehot-cnn-D': 'One-hot + CNN · full range', 'cnn-transfer-dpsi_rep1-D': 'Scanning → CNN · full range', 'esm2_35m-context-D': 'Ridge + ESM · full range', 'nested-family-selection': 'Validation-based selection'}
explorer = [dict(name=human_names[k], mae=metric(k), auroc=metric(k, 'auroc_plus'), ap=metric(k, 'auprc_plus')) for k in human_names]
(HERE / 'data.js').write_text('window.DECK_DATA=' + json.dumps(dict(explorer=explorer, hif=hif), ensure_ascii=False) + ';\n', encoding='utf8')
evidence = dict(source_hashes=source_hashes, assets=downloads, figures=files, figure_sha256={name: digest(ASSETS / name) for name in files}, prototype_sha256=digest(ASSETS / 'workspace-prototype.png') if (ASSETS / 'workspace-prototype.png').exists() else None, dataset_identity=analysis['data_identity'], source_manifest_sha256=analysis['source_manifest_sha256'], scientific_status='development; no automatic model promotion or gate closure', main_population=dict(peptides=235, protein_groups=221, cells=122412), chart_explorer=explorer, definitions=dict(mae='peptide macro, PSI units', plus='measured delta PSI >= 1', minus='measured delta PSI <= -1', ci='Q1 two contrasts: adjusted 97.5%; other added comparisons descriptive 95% protein-group bootstrap', plotting='standalone SVG figures generated with Matplotlib; no external test predictions computed'), generation_script_sha256=digest(Path(__file__)))
(HERE / 'evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
(HERE / 'asset-notices.md').write_text('# Asset notices\n\nFonts: Be Vietnam Pro, SIL OFL; see vendor/font-license.txt.\n\nChart.js 4.4.1, MIT; see vendor/chart-license.md.\n\nProtein GIF and its existing poster: Nikolakhs, I-TASSER predicted protein fold of Fam188a, Wikimedia Commons, CC BY-SA 3.0. https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif . Unmodified illustration of a protein fold, not HIF1A or a measured degron structure. The GIF remains under its original license.\n\nAll process diagrams are original schematic SVG/CSS. Research figures are generated from the local evidence sources listed in evidence.json.\n', encoding='utf8')
print(f'Prepared {len(files)} research figures; {len(source_hashes)} hashed result sources.')
