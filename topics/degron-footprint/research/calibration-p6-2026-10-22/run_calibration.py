"""P6 — hiệu chuẩn điểm ridge M3 (mức ext 4,0) và tiện ích xếp hạng top-k%.

Tiêu chí chốt trước ở PROTOCOL.md. Chạy bằng python -I, CPU, 2 thread.
Tái dùng NGUYÊN run_curve.build/run_curve.ridge nên điểm thô trùng results.json của P0.

  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/calibration-p6-2026-10-22/run_calibration.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.isotonic import IsotonicRegression

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import run_curve as rc          # noqa: E402  (đồng thời nạp residue_data, derisk)
rd, dr = rc.rd, rc.dr

SEEDS = rc.SEEDS
N_BOOT = 5000
BOOT_SEED = 20261022
N_INNER = 5
KS = [0.05, 0.10, 0.20]
N_BINS = 10
METHODS = ['raw', 'platt', 'iso', 'const']


# ---------------------------------------------------------------- hiệu chuẩn
def raw_prob(score):
    return np.clip(score / rd.RESCUE_DELTA, 0.0, 1.0)


def fit_platt(s, y):
    return LogisticRegression(C=1e4, max_iter=1000).fit(s[:, None], y)


def fit_iso(s, y):
    return IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds='clip').fit(s, y)


def apply_platt(m, s):
    return m.predict_proba(s[:, None])[:, 1]


def crossfit_oof(Xc, yc, rowgc, pool, alpha, seed, fold):
    """Điểm OOF của pool: 5 inner fold theo cụm, alpha cố định từ bước chính."""
    clusters = sorted(set(rowgc[pool]))
    rng = np.random.default_rng(seed * 1000 + fold + 7)
    perm = rng.permutation(clusters)
    assign = {c: i % N_INNER for i, c in enumerate(perm)}
    f = np.array([assign[g] for g in rowgc[pool]])
    oof = np.zeros(len(pool))
    for k in range(N_INNER):
        trk, tek = pool[f != k], pool[f == k]
        m = Ridge(alpha=alpha).fit(Xc[trk][:, :180], yc[trk])
        oof[f == k] = m.predict(Xc[tek][:, :180])
    return oof


# ---------------------------------------------------------------- bootstrap theo cụm
class ClusterBoot:
    def __init__(self, cl_idx, n_clusters):
        self.ci = cl_idx
        self.nc = n_clusters
        rng = np.random.default_rng(BOOT_SEED)
        self.W = rng.multinomial(n_clusters, np.full(n_clusters, 1.0 / n_clusters),
                                 size=N_BOOT).astype(float)

    def per_cluster(self, v):
        return np.bincount(self.ci, weights=v, minlength=self.nc)

    def mean_ci(self, v):
        """CI của trung bình ô (gộp) khi bootstrap cụm."""
        S, N = self.per_cluster(v), np.bincount(self.ci, minlength=self.nc).astype(float)
        point = float(S.sum() / N.sum())
        boot = (self.W @ S) / (self.W @ N)
        return point, np.quantile(boot, [.025, .975]).tolist(), boot


def brier_cells(p, y):
    return (p - y) ** 2


def ece_pack(p, y, boot, nb=N_BINS):
    edges = np.unique(np.quantile(p, np.linspace(0, 1, nb + 1)))
    k = max(len(edges) - 1, 1)
    b = np.clip(np.searchsorted(edges[1:-1], p, side='right'), 0, k - 1)
    nc = boot.nc
    flat = boot.ci * k + b
    n = np.bincount(flat, minlength=nc * k).reshape(nc, k).astype(float)
    sp = np.bincount(flat, weights=p, minlength=nc * k).reshape(nc, k)
    sy = np.bincount(flat, weights=y, minlength=nc * k).reshape(nc, k)
    tot = n.sum()
    ece = float(np.abs(sy.sum(0) - sp.sum(0)).sum() / tot)
    Wn = boot.W @ n
    ece_b = np.abs(boot.W @ sy - boot.W @ sp).sum(1) / Wn.sum(1)
    with np.errstate(invalid='ignore', divide='ignore'):
        obs_b = (boot.W @ sy) / Wn
    rel = []
    for j in range(k):
        lo, hi = np.nanquantile(obs_b[:, j], [.025, .975])
        rel.append({'bin': j, 'n_cells': int(n[:, j].sum()),
                    'n_clusters': int((n[:, j] > 0).sum()),
                    'mean_pred': float(sp[:, j].sum() / n[:, j].sum()),
                    'obs_rate': float(sy[:, j].sum() / n[:, j].sum()),
                    'obs_rate_ci95': [float(lo), float(hi)]})
    return {'ece': ece, 'ece_ci95': np.quantile(ece_b, [.025, .975]).tolist(), 'reliability': rel}


def recal_line(p, y):
    z = np.log(np.clip(p, 1e-4, 1 - 1e-4) / (1 - np.clip(p, 1e-4, 1 - 1e-4)))
    m = LogisticRegression(C=1e6, max_iter=2000).fit(z[:, None], y)
    return {'intercept': float(m.intercept_[0]), 'slope': float(m.coef_[0, 0])}


def diff_ci(boot, v_a, v_b):
    """CI của Brier(a) − Brier(b) (a,b là vector bình phương sai số theo ô)."""
    Sa, Sb = boot.per_cluster(v_a), boot.per_cluster(v_b)
    N = np.bincount(boot.ci, minlength=boot.nc).astype(float)
    point = float((Sa.sum() - Sb.sum()) / N.sum())
    d = (boot.W @ (Sa - Sb)) / (boot.W @ N)
    return {'delta': point, 'ci95': np.quantile(d, [.025, .975]).tolist()}


# ---------------------------------------------------------------- tiện ích top-k%
def topk_stats(score, y, idx, frac):
    out = []
    for a, b in idx:
        yy = y[a:b] >= rd.RESCUE_DELTA
        n = b - a
        npos = int(yy.sum())
        if npos == 0 or npos == n:
            out.append(None)
            continue
        k = max(1, int(np.ceil(frac * n)))
        order = np.argsort(-score[a:b], kind='stable')[:k]
        hit = int(yy[order].sum())
        prec = hit / k
        out.append({'precision': prec, 'recall': hit / npos, 'enrichment': prec / (npos / n)})
    return out


def macro_ci(vals, groups_pep, key):
    keep = [i for i, v in enumerate(vals) if v is not None]
    v = np.array([vals[i][key] for i in keep])
    g = np.asarray(groups_pep)[keep]
    u = sorted(set(g))
    rng = np.random.default_rng(BOOT_SEED)
    boot = [float(np.concatenate([v[g == c] for c in rng.choice(u, len(u), replace=True)]).mean())
            for _ in range(N_BOOT)]
    return {'mean': float(v.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist(),
            'n_peptides': len(keep), 'n_clusters': len(u)}


# ---------------------------------------------------------------- chính
def main():
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'folds không trùng G2'
    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    new_peps = [p for p in pepsE if p not in set(peps0)]
    pos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[pos[p]]) for p in new_peps])
    Xc = np.vstack([X0, XE[new_rows]])
    yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    base_n = len(y0)
    yb = (y0 >= rd.RESCUE_DELTA).astype(float)

    lc = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())
    ref_auroc = lc['results']['ridge']['ext']['macro_auroc_per_seed']

    S = {m: [] for m in ['score', 'platt', 'iso', 'platt_dom', 'iso_dom', 'const']}
    detail, coefs = [], {}
    for seed in SEEDS:
        sc = np.full(base_n, np.nan)
        P = {m: np.full(base_n, np.nan) for m in ['platt', 'iso', 'platt_dom', 'iso_dom', 'const']}
        for fold, (_, te) in enumerate(folds):
            test_clusters = set(fold_clusters[fold])
            tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
            extra = np.array([i for i in range(base_n, len(yc))
                              if rowgc[i] not in test_clusters], dtype=int)
            pool = np.concatenate([tr_base, extra])
            gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
            ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
            train, val = pool[ti], pool[vi]
            pred, alpha = rc.ridge(Xc, yc, train, val, te)
            full = np.concatenate([train, val])
            mdl = Ridge(alpha=alpha).fit(Xc[full][:, :180], yc[full])
            chk = mdl.predict(X0[te][:, :180])
            assert np.abs(chk - pred).max() < 1e-9
            coefs[f'{seed}_{fold}'] = (mdl.coef_.copy(), float(mdl.intercept_), float(alpha))
            sc[te] = pred
            # --- cross-fit trong outer-train (pool = train + val)
            oof = crossfit_oof(Xc, yc, rowgc, pool, alpha, seed, fold)
            ypool = (yc[pool] >= rd.RESCUE_DELTA).astype(float)
            pl, io = fit_platt(oof, ypool), fit_iso(oof, ypool)
            P['platt'][te], P['iso'][te] = apply_platt(pl, pred), io.predict(pred)
            dom = pool < base_n
            pld, iod = fit_platt(oof[dom], ypool[dom]), fit_iso(oof[dom], ypool[dom])
            P['platt_dom'][te], P['iso_dom'][te] = apply_platt(pld, pred), iod.predict(pred)
            P['const'][te] = ypool.mean()
            detail.append({'seed': seed, 'fold': fold, 'alpha': float(alpha),
                           'n_pool_cells': int(len(pool)), 'pool_pos_rate': float(ypool.mean()),
                           'oof_auroc_cell_pooled': dr.auroc(oof, ypool > 0),
                           'platt': {'coef': float(pl.coef_[0, 0]), 'intercept': float(pl.intercept_[0])}})
        assert not np.isnan(sc).any() and all(not np.isnan(v).any() for v in P.values())
        a = dr.macro_auroc(sc, y0, idx0)[0]
        assert abs(a - ref_auroc[SEEDS.index(seed)]) < 1e-9, (seed, a)
        print(f'seed {seed}: macro-AUROC thô {a:.4f} khớp results.json [OK]', flush=True)
        S['score'].append(sc)
        for m in P:
            S[m].append(P[m])

    # ---- ensemble và theo seed
    ens_score = np.mean(S['score'], axis=0)
    assert abs(dr.macro_auroc(ens_score, y0, idx0)[0] - lc['results']['ridge']['ext']['macro_auroc_ensemble']) < 1e-9
    prob = {'raw': raw_prob(ens_score)}
    for m in ['platt', 'iso', 'platt_dom', 'iso_dom', 'const']:
        prob[m] = np.mean(S[m], axis=0)
    prob_seed = [{'raw': raw_prob(S['score'][i]), **{m: S[m][i] for m in
                  ['platt', 'iso', 'const']}} for i in range(len(SEEDS))]

    clusters = sorted(set(rowg0))
    cmap = {c: i for i, c in enumerate(clusters)}
    ci = np.array([cmap[c] for c in rowg0])
    boot = ClusterBoot(ci, len(clusters))

    metrics = {}
    for m in ['raw', 'platt', 'iso', 'const', 'platt_dom', 'iso_dom']:
        br, brci, _ = boot.mean_ci(brier_cells(prob[m], yb))
        metrics[m] = {'brier': br, 'brier_ci95': brci,
                      **ece_pack(prob[m], yb, boot), 'recalibration_line': recal_line(prob[m], yb),
                      'mean_pred': float(prob[m].mean()),
                      'macro_auroc_of_prob': dr.macro_auroc(prob[m], y0, idx0)[0] if m != 'const' else None}
    bc = brier_cells(prob['const'], yb)
    for m in ['raw', 'platt', 'iso', 'platt_dom', 'iso_dom']:
        metrics[m]['bss_vs_const'] = 1 - metrics[m]['brier'] / metrics['const']['brier']
    metrics['observed_pos_rate'] = float(yb.mean())

    comp = {}
    for c in ['platt', 'iso']:
        comp[f'raw_minus_{c}'] = diff_ci(boot, brier_cells(prob['raw'], yb), brier_cells(prob[c], yb))
        comp[f'raw_minus_{c}']['per_seed'] = [
            float(np.mean(brier_cells(prob_seed[i]['raw'], yb)) - np.mean(brier_cells(prob_seed[i][c], yb)))
            for i in range(len(SEEDS))]
        comp[f'const_minus_{c}'] = diff_ci(boot, bc, brier_cells(prob[c], yb))
        comp[f'const_minus_{c}']['per_seed'] = [
            float(np.mean(brier_cells(prob_seed[i]['const'], yb)) - np.mean(brier_cells(prob_seed[i][c], yb)))
            for i in range(len(SEEDS))]
    comp['platt_minus_iso'] = diff_ci(boot, brier_cells(prob['platt'], yb), brier_cells(prob['iso'], yb))
    for c in ['platt_dom', 'iso_dom']:
        comp[f'raw_minus_{c}'] = diff_ci(boot, brier_cells(prob['raw'], yb), brier_cells(prob[c], yb))
    comp['raw_minus_const'] = diff_ci(boot, brier_cells(prob['raw'], yb), bc)

    verdict = {}
    for c in ['platt', 'iso']:
        a = comp[f'raw_minus_{c}']
        ok_a = a['ci95'][0] > 0
        ok_b = all(d > 0 for d in a['per_seed'])
        b = comp[f'const_minus_{c}']
        verdict[c] = {
            'calibrated_criterion_a_ci_above_zero': bool(ok_a),
            'calibrated_criterion_b_all_seeds_positive': bool(ok_b),
            'calibrated_verdict': 'đã hiệu chuẩn' if (ok_a and ok_b)
                                  else 'chưa đủ bằng chứng là đã hiệu chuẩn',
            'skill_vs_base_rate_ci_above_zero': bool(b['ci95'][0] > 0),
            'skill_verdict': ('xác suất có kỹ năng hơn tần suất nền' if b['ci95'][0] > 0
                              else 'hiệu chuẩn nhưng không có kỹ năng hơn tần suất nền'),
        }
    use_iso = comp['platt_minus_iso']['ci95'][0] > 0
    verdict['prototype_calibrator'] = 'iso' if use_iso else 'platt'

    # ---- tiện ích xếp hạng (điểm thô ensemble) + từng seed
    grp_pep = np.asarray(groups0)
    util = {}
    for frac in KS:
        key = f'top{int(round(frac * 100))}pct'
        st = topk_stats(ens_score, y0, idx0, frac)
        util[key] = {k: macro_ci(st, grp_pep, k) for k in ['precision', 'recall', 'enrichment']}
        util[key]['enrichment_per_seed'] = [
            float(np.mean([v['enrichment'] for v in topk_stats(S['score'][i], y0, idx0, frac) if v]))
            for i in range(len(SEEDS))]
        util[key]['k_cells_typical'] = int(np.ceil(frac * np.median([b - a for a, b in idx0])))
        util[key]['random_enrichment'] = 1.0
    util['verdict_enrichment_top10_ci_above_1'] = bool(util['top10pct']['enrichment']['ci95'][0] > 1)

    out = {
        'protocol': 'PROTOCOL.md 22/10/2026; ridge M3 mức ext 4,0; OOF trên benchmark phát triển, '
                    'không phải kiểm chứng ngoài độc lập',
        'seeds': SEEDS, 'n_boot': N_BOOT, 'boot_seed': BOOT_SEED,
        'n_test_cells': int(len(y0)), 'n_test_peptides': len(peps0),
        'n_test_clusters': len(clusters),
        'gate_raw_auroc_matches_results_json': True,
        'metrics': metrics, 'comparisons': comp, 'verdict': verdict, 'utility': util,
        'folds_detail': detail,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    np.savez_compressed(TOPIC / 'data/processed/calibration-p6-oof.npz',
                        score_by_seed=np.array(S['score']), platt_by_seed=np.array(S['platt']),
                        iso_by_seed=np.array(S['iso']), y=y0, idx=np.asarray(idx0),
                        coef=np.array([coefs[f'{s}_{f}'][0] for s in SEEDS for f in range(5)]),
                        intercept=np.array([coefs[f'{s}_{f}'][1] for s in SEEDS for f in range(5)]),
                        alpha=np.array([coefs[f'{s}_{f}'][2] for s in SEEDS for f in range(5)]),
                        test_rows=np.concatenate([folds[f][1] for f in range(5)]),
                        test_fold_sizes=np.array([len(folds[f][1]) for f in range(5)]))
    for m in ['raw', 'platt', 'iso', 'const']:
        r = metrics[m]
        print(f"{m:6s} Brier {r['brier']:.5f} CI {np.round(r['brier_ci95'], 5).tolist()} "
              f"ECE {r['ece']:.4f}", flush=True)
    for k, v in comp.items():
        print(f'  {k}: {v["delta"]:+.5f} CI {np.round(v["ci95"], 5).tolist()}')
    print(json.dumps(verdict, ensure_ascii=False, indent=1))
    for k in ['top5pct', 'top10pct', 'top20pct']:
        print(k, {a: round(util[k][a]['mean'], 3) for a in ['precision', 'recall', 'enrichment']},
              util[k]['enrichment']['ci95'])


if __name__ == '__main__':
    main()
