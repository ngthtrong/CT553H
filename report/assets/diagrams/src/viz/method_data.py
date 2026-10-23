"""Data for Fig 3.7 (method overview): the example peptide, its measured and OOF-predicted matrices,
the 6-bin read distributions, and the calibration numbers. Reads only repo files; trains nothing.

Run: .venv/bin/python -I report/assets/diagrams/src/viz/method_data.py   (prints the selection summary)
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr, pearsonr

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
TOPIC = ROOT / 'topics' / 'degron-footprint'
sys.path.insert(0, str(TOPIC / 'research' / 'residue-task-derisk-2026-10-15'))
import residue_data as rd   # repo module: label construction (read-only use)

AAS = rd.AAS
PROC = TOPIC / 'data' / 'processed'


def load():
    base = np.load(PROC / 'learning-curve-sat-base.npz', allow_pickle=False)
    oof = np.load(PROC / 'calibration-p6-oof.npz', allow_pickle=False)
    return base, oof


def per_peptide(base, oof):
    """Per-peptide Spearman/Pearson between OOF ridge score (mean of 3 seeds) and measured dPSI."""
    y = base['y']; idx = base['idx']; peps = base['peps']
    score = oof['score_by_seed'].mean(axis=0)
    assert np.allclose(oof['y'], y) and (oof['idx'] == idx).all(), 'OOF is not aligned with the base cache'
    rows = []
    for i, (a, b) in enumerate(idx):
        yy, ss = y[a:b], score[a:b]
        rows.append(dict(i=i, pep=str(peps[i]), n=int(b - a), ymax=float(yy.max()),
                         n_pos=int((yy >= 1.0).sum()),
                         sp=float(spearmanr(yy, ss).statistic), pr=float(pearsonr(yy, ss).statistic)))
    return rows, score


def pick_example(rows):
    """Pre-specified rule (not best-case): among peptides with a clear footprint (max dPSI >= 2 and >= 8
    cells with dPSI >= 1), take the one whose Spearman is closest to the median Spearman of that subset."""
    sub = [r for r in rows if r['ymax'] >= 2.0 and r['n_pos'] >= 8]
    med = float(np.median([r['sp'] for r in sub]))
    best = min(sub, key=lambda r: abs(r['sp'] - med))
    return best, med, len(sub)


def matrices(base, score, i):
    """Return (seq, WT-aware 28x20 measured matrix, predicted matrix) for base peptide i, in position order."""
    sat = _sat()
    pep = str(base['peps'][i])
    cells = sat[pep]['cells']                       # {(pos, aa): (da, db)}
    keys = sorted(cells)
    a, b = base['idx'][i]
    assert len(keys) == b - a, (len(keys), b - a)
    X = base['X'][a:b]
    mut_from_x = [AAS[j] for j in X[:, 20:40].argmax(1)]
    assert mut_from_x == [k[1] for k in keys], 'cell order differs from the cache'
    seq = sat[pep]['seq'][:28]
    meas = np.full((28, 20), np.nan); pred = np.full((28, 20), np.nan)
    for r, (pos, aa) in enumerate(keys):
        meas[pos - 1, AAS.index(aa)] = base['y'][a + r]
        pred[pos - 1, AAS.index(aa)] = score[a + r]
    return pep, seq, meas, pred, sat[pep]


_SAT = None
def _sat():
    global _SAT
    if _SAT is None:
        seqs, _subs = rd.load_scan_csv()
        up = rd.load_uniprot()
        _SAT = rd.build_saturation(rd.load_psi('sat_a'), rd.load_psi('sat_b'), seqs, up, degron_psi_max=3.0)
    return _SAT


def bin_distributions(pep, seq, info, meas):
    """Normalised reads per bin (replicate A) of (i) the median synonymous (WT-like) construct and
    (ii) the substitution with the largest dPSI, read from psi-sat_a.tsv."""
    import csv
    want = {}
    syn = {(i, r) for i, r in enumerate(seq, start=1)}
    with open(PROC / 'psi-sat_a.tsv', encoding='utf-8') as fh:
        rd_ = csv.reader(fh, delimiter='\t'); next(rd_)
        for row in rd_:
            m = rd.SAT_PAT.match(row[0])
            if m and m.group('pep') == pep:
                key = (int(m.group('pos')), m.group('aa').upper())
                want[key] = (float(row[1]), [float(v) for v in row[3:9]])
    syn_vals = sorted((v[0], k) for k, v in want.items() if k in syn)
    psi_syn, k_syn = syn_vals[len(syn_vals) // 2]
    pos, j = np.unravel_index(np.nanargmax(meas), meas.shape)
    k_mut = (int(pos) + 1, AAS[j])
    psi_mut = want[k_mut][0]
    def frac(k):
        nb = np.array(want[k][1]); return nb / nb.sum()
    return dict(syn=dict(key=k_syn, psi=psi_syn, frac=frac(k_syn).tolist()),
                mut=dict(key=k_mut, psi=psi_mut, frac=frac(k_mut).tolist(),
                         wt=seq[k_mut[0] - 1], dpsi=float(meas[pos, j])))


def calibration_numbers():
    r = json.load(open(TOPIC / 'research' / 'calibration-p6-2026-10-22' / 'results.json'))
    m = r['metrics']
    rel = lambda k: [(b['mean_pred'], b['obs_rate'], b['n_cells']) for b in m[k]['reliability']]
    return dict(brier_raw=m['raw']['brier'], brier_platt=m['platt']['brier'], brier_const=m['const']['brier'],
                ece_raw=m['raw']['ece'], ece_platt=m['platt']['ece'],
                auroc=m['platt']['macro_auroc_of_prob'], enrich10=r['utility']['top10pct']['enrichment']['mean'],
                enrich10_ci=r['utility']['top10pct']['enrichment']['ci95'],
                pos_rate=r['metrics']['observed_pos_rate'], rel_raw=rel('raw'), rel_platt=rel('platt'))


if __name__ == '__main__':
    base, oof = load()
    rows, score = per_peptide(base, oof)
    sp = np.array([r['sp'] for r in rows])
    print('peptides', len(rows), 'median Spearman (all 91) %.3f' % np.median(sp),
          'median Pearson %.3f' % np.median([r['pr'] for r in rows]))
    ex, med, n = pick_example(rows)
    print('footprint subset n=%d, median Spearman %.3f' % (n, med)); print('example', ex)
    pep, seq, meas, pred, info = matrices(base, score, ex['i'])
    print(pep, seq, 'psi_wt %.3f' % info['psi_wt'])
    print('meas range', np.nanmin(meas), np.nanmax(meas), 'pred range', np.nanmin(pred), np.nanmax(pred))
    print(bin_distributions(pep, seq, info, meas))
    c = calibration_numbers(); print({k: v for k, v in c.items() if not k.startswith('rel')})
    print('rel_raw', [(round(a,3), round(b,3), n) for a, b, n in c['rel_raw']])
    print('rel_platt', [(round(a,3), round(b,3), n) for a, b, n in c['rel_platt']])
