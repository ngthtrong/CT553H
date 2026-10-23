"""R3 — cổng miền áp dụng: tầng (i) tra cứu PSI đo -> trạng thái miền; tầng (ii) ridge trình tự -> PSI -> trạng thái.

Tiêu chí chốt trước ở PROTOCOL.md (SHA-256 nhúng trong notebook). CPU, numpy + scikit-learn (GroupKFold) + scipy (rankdata).
Hàm `run(ctx, smoke=False)` được notebook gọi; chạy độc lập:  python -I run_r3.py [--smoke]

Ridge giải bằng phương trình chuẩn từ thống kê gộp theo fold (tất định, ít RAM): với mỗi fold giữ
n, Σx, Σy, XᵀX, Xᵀy, Σy². Nested CV chọn α trên các fold còn lại.
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/notebook-kit-2026-10-22'))
import residue_data as rd      # noqa: E402

PROTEOME_CLUSTERS = TOPIC / 'data/interim/protein-id30-cov80-proteome_cluster.tsv'

AAS = rd.AAS
AA2I = {a: i for i, a in enumerate(AAS)}
NF = 20 + 400
ALPHAS = [1, 10, 100, 1000, 10000]
READ_MIN = rd.READ_MIN
SEEDS = [17, 29, 43]
N_BOOT = 5000
P_IN, P_OUT = 0.80, 0.50
DOMAIN_PSI = 4.0
# tiêu chí PROTOCOL §2 và §3
CRIT1 = {'auroc_lo': 0.80, 'bss_lo': 0.0, 'frac_d0_in_max': 0.25}
CRIT2 = {'spearman_min': 0.30, 'auroc_lo': 0.70, 'bss_lo': 0.0, 'frac_d0_in_max': 0.35}


# ------------------------------------------------------------------ dữ liệu
def load_proteome_clusters():
    """accession -> đại diện cụm (id30 cov80) phủ TOÀN proteome (build_proteome_clusters.py).
    Không dùng rd.load_clusters(): file đó chỉ có 6.573 protein (xem README, local-analysis)."""
    rep = {}
    for line in PROTEOME_CLUSTERS.read_text(encoding='utf-8').splitlines():
        r, m = line.split('\t')[:2]
        rep[m] = r
    return rep


def load_tiles(smoke=False, pool_names=()):
    """-> names, seq_int (N,28) int8, psi (N,), group (N,) cho tile hợp lệ của sàng."""
    uniprot = rd.load_uniprot()
    clusters = load_proteome_clusters()
    names, seqs, psis = [], [], []
    dropped = {'psi_na_or_low_reads': 0, 'acc_not_in_uniprot': 0, 'not_full_tile': 0, 'nonstandard_aa': 0}
    with (TOPIC / 'data/interim/gps-peptidome-rep1.tsv').open(encoding='utf-8') as fh:
        next(fh)
        for line in fh:
            name, reads, psi = line.rstrip('\n').split('\t')
            if psi == 'NA' or float(reads) < READ_MIN:
                dropped['psi_na_or_low_reads'] += 1
                continue
            if name.split('_')[0] not in uniprot:
                dropped['acc_not_in_uniprot'] += 1
                continue
            seq = rd.derive_sequence(name, uniprot)
            if seq is None:
                dropped['not_full_tile'] += 1
                continue
            if any(c not in AA2I for c in seq):
                dropped['nonstandard_aa'] += 1
                continue
            names.append(name)
            seqs.append(seq)
            psis.append(float(psi))
    if smoke:                                    # kiểm hạ tầng: pool + tập con ngẫu nhiên
        rng = np.random.default_rng(0)
        keep = set(pool_names) | set(rng.choice(names, 30000, replace=False))
        sel = [i for i, n in enumerate(names) if n in keep]
        names, seqs, psis = [names[i] for i in sel], [seqs[i] for i in sel], [psis[i] for i in sel]
    S = np.array([[AA2I[c] for c in s] for s in seqs], dtype=np.int8)
    group = np.array([clusters.get(rd.accession(n), rd.accession(n)) for n in names])
    return names, S, np.asarray(psis), group, dropped


def feats(S):
    """(N,28) int8 -> (N,420) float64: đếm 20 acid amin + đếm 400 cặp liền kề."""
    N = len(S)
    X = np.zeros((N, NF))
    for a in range(20):
        X[:, a] = (S == a).sum(1)
    P = S[:, :-1].astype(np.int64) * 20 + S[:, 1:]
    rows = np.repeat(np.arange(N), P.shape[1])
    np.add.at(X, (rows, 20 + P.ravel()), 1.0)
    return X


def blocks(idx, size=20000):
    for i in range(0, len(idx), size):
        yield idx[i:i + size]


# ------------------------------------------------------------------ ridge từ thống kê gộp
def fold_stats(S, y, idx):
    st = {'n': 0, 'sx': np.zeros(NF), 'sy': 0.0, 'xtx': np.zeros((NF, NF)), 'xty': np.zeros(NF), 'yty': 0.0}
    for b in blocks(idx):
        X = feats(S[b])
        yb = y[b]
        st['n'] += len(b)
        st['sx'] += X.sum(0)
        st['sy'] += yb.sum()
        st['xtx'] += X.T @ X
        st['xty'] += X.T @ yb
        st['yty'] += float(yb @ yb)
    return st


def combine(sts):
    return {k: sum(s[k] for s in sts) for k in sts[0]}


def fit(st, alpha):
    n = st['n']
    mx, my = st['sx'] / n, st['sy'] / n
    xtx = st['xtx'] - n * np.outer(mx, mx)
    xty = st['xty'] - n * mx * my
    coef = np.linalg.solve(xtx + alpha * np.eye(NF), xty)
    return coef, my - mx @ coef


def mse(st, coef, b):
    n = st['n']
    sse = (st['yty'] - 2 * (coef @ st['xty'] + b * st['sy']) + coef @ st['xtx'] @ coef
           + 2 * b * (coef @ st['sx']) + n * b * b)
    return sse / n


# ------------------------------------------------------------------ logistic 2 tham số + chỉ số
def logistic_fit(x, d, iters=60, ridge=1e-8):
    A = np.c_[np.ones(len(x)), x]
    w = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-A @ w))
        W = p * (1 - p) + 1e-12
        H = A.T @ (A * W[:, None]) + ridge * np.eye(2)
        step = np.linalg.solve(H, A.T @ (d - p))
        w += step
        if np.abs(step).max() < 1e-10:
            break
    return w


def sigmoid(a, b, x):
    return 1 / (1 + np.exp(-(a + b * x)))


def auroc(score, label):
    from scipy.stats import rankdata
    label = np.asarray(label, bool)
    n1, n0 = int(label.sum()), int((~label).sum())
    if n1 == 0 or n0 == 0:
        return float('nan')
    r = rankdata(score)
    return float((r[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def pool_cv(x, d, groups, n_splits=5):
    """Xác suất OOF của logistic theo GroupKFold trên pool + Brier nền theo từng train fold."""
    from nbkit import StableGroupKFold as GroupKFold   # cùng fold với bản đo trên mọi bản sklearn
    oof = np.zeros(len(x))
    base = np.zeros(len(x))
    for tr, te in GroupKFold(n_splits).split(x, d, groups):
        a, b = logistic_fit(x[tr], d[tr])
        oof[te] = sigmoid(a, b, x[te])
        base[te] = d[tr].mean()
    return oof, base


def cluster_boot_metrics(oof, base, d, groups, seed):
    """Bootstrap theo cụm: AUROC và BSS (1 - Brier/Brier_nền)."""
    rng = np.random.default_rng(seed)
    uniq, inv = np.unique(groups, return_inverse=True)
    members = [np.where(inv == k)[0] for k in range(len(uniq))]
    aur, bss = [], []
    for _ in range(N_BOOT):
        take = np.concatenate([members[k] for k in rng.integers(0, len(uniq), len(uniq))])
        aur.append(auroc(oof[take], d[take]))
        b1 = np.mean((oof[take] - d[take]) ** 2)
        b0 = np.mean((base[take] - d[take]) ** 2)
        bss.append(1 - b1 / b0)
    q = lambda v: [float(np.nanquantile(v, .025)), float(np.nanquantile(v, .975))]       # noqa: E731
    return {'auroc_ci95': q(aur), 'bss_ci95': q(bss)}


def evaluate_map(x, d, groups, tag):
    """Đánh giá tầng: OOF, AUROC, BSS (CI từng seed), ba mức trạng thái, rò rỉ nguy hiểm."""
    oof, base = pool_cv(x, d, groups)
    a, b = logistic_fit(x, d)
    out = {'tag': tag, 'n': int(len(x)), 'n_clusters': int(len(set(groups))), 'base_rate': float(d.mean()),
           'auroc_oof': auroc(oof, d), 'brier_oof': float(np.mean((oof - d) ** 2)),
           'brier_base': float(np.mean((base - d) ** 2)), 'logistic_final': {'a': float(a), 'b': float(b)}}
    out['bss_oof'] = 1 - out['brier_oof'] / out['brier_base']
    out['bootstrap_by_seed'] = {str(s): cluster_boot_metrics(oof, base, d, groups, s) for s in SEEDS}
    status = np.where(oof >= P_IN, 'in', np.where(oof < P_OUT, 'out', 'borderline'))
    out['status_share'] = {k: float((status == k).mean()) for k in ('in', 'borderline', 'out')}
    n_in = max(1, int((status == 'in').sum()))
    out['precision_in_domain'] = float(((status == 'in') & (d == 1)).sum() / n_in)
    out['frac_d0_in_domain'] = float(((status == 'in') & (d == 0)).sum() / max(1, int((d == 0).sum())))
    out['recall_d1_in_domain'] = float(((status == 'in') & (d == 1)).sum() / max(1, int((d == 1).sum())))
    inv = lambda p: float((np.log(p / (1 - p)) - a) / b)                                  # noqa: E731
    out['x_cut_for_P_in'] = inv(P_IN)
    out['x_cut_for_P_out'] = inv(P_OUT)
    return out


def verdict(ev, crit, spearman=None):
    ok = {}
    seeds = list(ev['bootstrap_by_seed'].values())
    ok['auroc_ci_lo_all_seeds'] = bool(all(s['auroc_ci95'][0] >= crit['auroc_lo'] for s in seeds))
    ok['bss_ci_lo_all_seeds'] = bool(all(s['bss_ci95'][0] > crit['bss_lo'] for s in seeds))
    ok['frac_d0_in_domain'] = bool(ev['frac_d0_in_domain'] <= crit['frac_d0_in_max'])
    if spearman is not None:
        ok['spearman_point'] = bool(spearman >= crit['spearman_min'])
    ok['usable'] = bool(all(ok.values()))
    return ok


# ------------------------------------------------------------------ giai đoạn A (tầng ii)
def stage_a(S, y, group, names):
    from nbkit import StableGroupKFold as GroupKFold   # cùng fold với bản đo trên mọi bản sklearn
    folds = list(GroupKFold(5).split(np.zeros(len(y)), y, group))
    sts = [fold_stats(S, y, te) for _, te in folds]
    oof = np.zeros(len(y))
    chosen = []
    for k, (tr, te) in enumerate(folds):
        inner = {}
        for a in ALPHAS:
            errs = []
            for j in range(5):
                if j == k:
                    continue
                train = combine([sts[m] for m in range(5) if m not in (k, j)])
                coef, b = fit(train, a)
                errs.append(mse(sts[j], coef, b))
            inner[a] = float(np.mean(errs))
        best = min(inner, key=inner.get)
        chosen.append({'fold': k, 'alpha': best, 'inner_mse': inner})
        coef, b = fit(combine([sts[m] for m in range(5) if m != k]), best)
        for blk in blocks(te):
            oof[blk] = feats(S[blk]) @ coef + b
    # final: chọn α theo MSE trung bình 5 fold (huấn luyện trên 4), khớp trên toàn bộ
    cv = {a: float(np.mean([mse(sts[j], *fit(combine([sts[m] for m in range(5) if m != j]), a))
                            for j in range(5)])) for a in ALPHAS}
    best_final = min(cv, key=cv.get)
    coef_f, b_f = fit(combine(sts), best_final)
    return oof, folds, chosen, {'alpha': best_final, 'cv_mse': cv}, coef_f, b_f


def cluster_corr_boot(y, p, group, seed, rank=False):
    """Pearson (hoặc Spearman nếu rank=True) với bootstrap theo cụm bằng thống kê đủ từng cụm."""
    if rank:
        from scipy.stats import rankdata
        y, p = rankdata(y), rankdata(p)
    uniq, inv = np.unique(group, return_inverse=True)
    C = len(uniq)
    S = np.c_[np.bincount(inv), np.bincount(inv, y), np.bincount(inv, p), np.bincount(inv, y * y),
              np.bincount(inv, p * p), np.bincount(inv, y * p), np.bincount(inv, (y - p) ** 2)]

    def stat(tot):
        n, sy, sp, syy, spp, syp, sse = tot
        cov = syp / n - sy * sp / n ** 2
        return cov / np.sqrt((syy / n - (sy / n) ** 2) * (spp / n - (sp / n) ** 2)), np.sqrt(sse / n)
    est = stat(S.sum(0))
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(N_BOOT):
        w = np.bincount(rng.integers(0, C, C), minlength=C)
        vals.append(stat(w @ S))
    r = np.array([v[0] for v in vals])
    e = np.array([v[1] for v in vals])
    return {'corr': float(est[0]), 'corr_ci95': [float(np.quantile(r, .025)), float(np.quantile(r, .975))],
            'rmse': float(est[1]), 'rmse_ci95': [float(np.quantile(e, .025)), float(np.quantile(e, .975))]}


# ------------------------------------------------------------------ chạy
def run(ctx=None, smoke=False):
    t0 = time.time()
    res = {'protocol': 'PROTOCOL.md 22/10/2026', 'smoke': bool(smoke), 'P_in': P_IN, 'P_out': P_OUT,
           'criteria': {'tier1': CRIT1, 'tier2': CRIT2}, 'alphas': ALPHAS}
    pool = [l.rstrip('\n').split('\t') for l in
            (TOPIC / 'data/processed/r3-sat-wt-pool.tsv').read_text(encoding='utf-8').splitlines()[1:]]
    pool_names = [r[0] for r in pool]
    psi_wt = np.array([float(r[1]) for r in pool])
    d = (psi_wt <= DOMAIN_PSI).astype(float)
    pc = load_proteome_clusters()
    pgroup = np.array([pc.get(r[3], r[3]) for r in pool])      # cụm theo phân cụm TOÀN proteome

    names, S, psi, group, dropped = load_tiles(smoke, pool_names)
    res['tiles'] = {'n_valid': int(len(names)), 'dropped': dropped, 'n_clusters': int(len(set(group))),
                    'psi_quantiles': {str(q): float(np.quantile(psi, q)) for q in (.05, .25, .5, .75, .95)}}
    print(f"tile hợp lệ: {len(names):,} · cụm: {len(set(group)):,} · bỏ: {dropped}", flush=True)
    pos = {n: i for i, n in enumerate(names)}
    missing = [n for n in pool_names if n not in pos]
    assert not missing, f'{len(missing)} peptide pool không có trong tile hợp lệ: {missing[:3]}'
    x_meas = psi[[pos[n] for n in pool_names]]
    res['pool'] = {'n': len(pool), 'n_d1': int(d.sum()), 'n_clusters': int(len(set(pgroup))),
                   'pool_psi_quantiles': {str(q): float(np.quantile(x_meas, q)) for q in (.05, .25, .5, .75, .95)}}

    # ---- tầng (i)
    print('Tầng (i): M1 trên PSI đo', flush=True)
    ev1 = evaluate_map(x_meas, d, pgroup, 'tier1_lookup')
    ev1['verdict'] = verdict(ev1, CRIT1)
    res['tier1'] = ev1
    print(f"  AUROC OOF {ev1['auroc_oof']:.4f} · BSS {ev1['bss_oof']:.3f} · d0 lọt in-domain "
          f"{ev1['frac_d0_in_domain']:.3f} · dùng được: {ev1['verdict']['usable']}", flush=True)

    # ---- tầng (ii): giai đoạn A
    print('Tầng (ii) giai đoạn A: ridge 420 đặc trưng, nested CV theo cụm', flush=True)
    oof, folds, chosen, final, coef, b = stage_a(S, psi, group, names)
    base_pred = np.zeros(len(psi))
    for tr, te in folds:
        base_pred[te] = psi[tr].mean()
    base_rmse_ref = float(np.sqrt(np.mean((psi - base_pred) ** 2)))
    a_stage = {'alpha_per_outer_fold': chosen, 'alpha_final': final,
               'reference_rmse_train_mean': base_rmse_ref,
               'by_seed': {str(s): {'pearson': cluster_corr_boot(psi, oof, group, s, False),
                                    'spearman': cluster_corr_boot(psi, oof, group, s, True)} for s in SEEDS}}
    sp = a_stage['by_seed']['17']['spearman']['corr']
    a_stage['spearman_point'] = sp
    res['tier2_stage_A'] = a_stage
    print(f"  Spearman OOF {sp:.3f} · Pearson {a_stage['by_seed']['17']['pearson']['corr']:.3f} · "
          f"RMSE {a_stage['by_seed']['17']['pearson']['rmse']:.3f} (tham chiếu ≈ {base_rmse_ref:.3f}) · "
          f"α={final['alpha']}", flush=True)

    # ---- giai đoạn B
    x_pred = oof[[pos[n] for n in pool_names]]
    ev2 = evaluate_map(x_pred, d, pgroup, 'tier2_sequence')
    ev2['verdict'] = verdict(ev2, CRIT2, spearman=sp)
    res['tier2_stage_B'] = ev2
    print(f"Giai đoạn B: AUROC OOF {ev2['auroc_oof']:.4f} · BSS {ev2['bss_oof']:.3f} · d0 lọt in-domain "
          f"{ev2['frac_d0_in_domain']:.3f} · dùng được: {ev2['verdict']['usable']}", flush=True)

    res['usable_tier1'] = ev1['verdict']['usable']
    res['usable_tier2'] = ev2['verdict']['usable']
    res['seconds'] = round(time.time() - t0, 1)

    # ---- đầu ra cho hệ thống
    weights = {'tier2_coef': coef, 'tier2_intercept': np.array([b]), 'tier2_alpha': np.array([final['alpha']]),
               'feature_spec': np.array('20 aa counts (ACDEFGHIKLMNPQRSTVWY) + 400 adjacent-pair counts (index a*20+b)'),
               'm1': np.array([ev1['logistic_final']['a'], ev1['logistic_final']['b']]),
               'm2': np.array([ev2['logistic_final']['a'], ev2['logistic_final']['b']]),
               'p_in': np.array([P_IN]), 'p_out': np.array([P_OUT]),
               'x_cuts_measured': np.array([ev1['x_cut_for_P_in'], ev1['x_cut_for_P_out']]),
               'x_cuts_predicted': np.array([ev2['x_cut_for_P_in'], ev2['x_cut_for_P_out']]),
               'usable_tier1': np.array([res['usable_tier1']]), 'usable_tier2': np.array([res['usable_tier2']])}
    card = {'name': 'degron-domain-gate-r3', 'protocol': 'research/r3-domain-gate-2026-10-22/PROTOCOL.md',
            'smoke': bool(smoke),
            'domain_definition': 'PSI(WT) nội tại (trung vị ô đồng nghĩa, thí nghiệm bão hòa Zhang 2023) <= 4,0',
            'tier1': {k: ev1[k] for k in ('auroc_oof', 'bss_oof', 'frac_d0_in_domain', 'precision_in_domain',
                                          'status_share', 'x_cut_for_P_in', 'x_cut_for_P_out')},
            'tier2': {'spearman_stage_A': sp, **{k: ev2[k] for k in ('auroc_oof', 'bss_oof', 'frac_d0_in_domain',
                                                                     'precision_in_domain', 'status_share',
                                                                     'x_cut_for_P_in', 'x_cut_for_P_out')}},
            'usable_tier1': res['usable_tier1'], 'usable_tier2': res['usable_tier2'],
            'status_levels': {'in-domain': f'P>={P_IN}', 'borderline': f'{P_OUT}<=P<{P_IN}',
                              'out-of-domain': f'P<{P_OUT}', 'unknown': 'tầng (ii) không dùng được'},
            'limits': ['cổng chỉ nói tile giống miền huấn luyện đến đâu; không nói điểm ΔPSI chính xác',
                       'hai thang PSI (sàng vs bão hòa) lệch ≈ 0,9; ngưỡng thô 4,0 trên PSI sàng bị cấm',
                       'pool 235 peptide thiên về PSI sàng thấp; ngoại suy cho PSI cao chưa kiểm trực tiếp'],
            'sources': ['Zhang et al. 2023 GEO GSE240610 (Control Replicate 1) — citation bắt buộc',
                        'Zhang et al. 2023 Mendeley Data 10.17632/32h94v2yv2.2 (CC BY 4.0)',
                        'UniProtKB/Swiss-Prot 2026_03 (CC BY 4.0)']}
    res['_weights'] = weights
    res['_card'] = card
    return res


def write_outputs(res, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    weights, card = res.pop('_weights'), res.pop('_card')
    np.savez(out_dir / 'gate-weights.npz', **weights)
    (out_dir / 'gate-card.json').write_text(json.dumps(card, indent=2, ensure_ascii=False) + '\n')
    (out_dir / 'results.json').write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float) + '\n')
    res['_weights'], res['_card'] = weights, card
    return out_dir


if __name__ == '__main__':
    smoke = '--smoke' in sys.argv
    r = run(None, smoke=smoke)
    target = HERE / ('smoke-out' if smoke else 'local-out')
    write_outputs(r, target)
    print('->', target)
