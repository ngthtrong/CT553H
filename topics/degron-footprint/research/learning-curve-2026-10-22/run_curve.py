"""Đường cong học theo cụm (P1) + nới ngưỡng degron (P0).

Tiêu chí chốt trước ở PROTOCOL.md. Chạy bằng python -I, CPU, 2 thread.
Outer-test ở MỌI mức là đúng những ô của bộ 91 peptide trong benchmark G2,
nên AUROC so trực tiếp được với 0,8082. Peptide nới ngưỡng chỉ vào outer-train.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/learning-curve-2026-10-22/run_curve.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib, statistics
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.linear_model import Ridge

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
import residue_data as rd
import derisk as dr
sys.path.insert(0, str(TOPIC / 'research/g2-saturation-2026-10-18'))

torch.set_num_threads(2)
SEEDS = [17, 29, 43]
LEVELS = [0.25, 0.50, 0.75, 1.00]
EXT_PSI_MAX = 4.0          # chốt trước, PROTOCOL §7
ALPHAS = [1, 10, 100, 1000]
N_BOOT = 5000
BOOT_SEED = 20261022

# ---- class Gate: dựng lại đúng kiến trúc gate_no_pap của runner G2 -------------
from torch import nn


class Gate(nn.Module):
    """Đúng class Gate của g2-saturation/run.py, dùng cấu hình gated=True, pap=False."""

    def __init__(self, gated=True, pap=False):
        super().__init__()
        self.gated = gated
        self.pap = pap
        self.pair = nn.Linear(40, 32)
        self.context = nn.Linear(140, 32)
        self.head = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x):
        pair = torch.relu(self.pair(x[:, :40]))
        ctx = torch.tanh(self.context(x[:, 40:180]))
        if self.gated:
            ctx = ctx * torch.sigmoid(self.pair(x[:, :40]))
        return self.head(torch.cat([pair, ctx], 1)).squeeze(1) + (x[:, 180] if self.pap else 0)


def neural(X, y, tr, va, te, seed):
    torch.manual_seed(seed)
    net = Gate(gated=True, pap=False)
    opt = torch.optim.AdamW(net.parameters(), lr=.002, weight_decay=.01)
    xx = torch.tensor(X, dtype=torch.float32)
    yy = torch.tensor(y, dtype=torch.float32)
    rng = np.random.default_rng(seed)
    best, state, epoch_best = 1e99, None, 0
    for epoch in range(1, 61):
        net.train()
        for batch in np.array_split(rng.permutation(tr), max(1, len(tr) // 1024)):
            loss = ((net(xx[batch]) - yy[batch]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad():
            v = float(((net(xx[va]) - yy[va]) ** 2).mean())
        if v < best - 1e-6:
            best = v
            state = {k: t.detach().clone() for k, t in net.state_dict().items()}
            epoch_best = epoch
        if epoch - epoch_best >= 8:
            break
    net.load_state_dict(state)
    net.eval()
    with torch.no_grad():
        return net(xx[te]).numpy(), epoch_best


def ridge(X, y, tr, va, te):
    best = min((np.mean((Ridge(alpha=a).fit(X[tr][:, :180], y[tr]).predict(X[va][:, :180])
                         - y[va]) ** 2), a) for a in ALPHAS)[1]
    full = np.concatenate([tr, va])
    return Ridge(alpha=best).fit(X[full][:, :180], y[full]).predict(X[te][:, :180]), best


# ---- dữ liệu -------------------------------------------------------------------
def build(psi_max, tag):
    """Trả về (peps, X180, y, idx, rowg, groups) cho bộ bão hòa ở ngưỡng psi_max."""
    cache = TOPIC / f'data/processed/learning-curve-sat-{tag}.npz'
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        return (list(z['peps']), z['X'], z['y'], z['idx'], z['rowg'], z['groups'],
                {k: float(v) for k, v in zip(z['wtkeys'], z['wtvals'])})
    d = rd.load_all(degron_psi_max=psi_max)
    peps, rows, y, idx = dr.rows_and_labels(d['sat'], 'sat')
    groups = np.array([d['clusters'].get(rd.accession(p), rd.accession(p)) for p in peps])
    rowg = np.concatenate([np.repeat(groups[i], b - a) for i, (a, b) in enumerate(idx)])
    X = dr.featurize(rows, {'pair', 'comp', 'ctx'})
    psiwt = {p: d['sat'][p]['psi_wt'] for p in peps}
    np.savez_compressed(cache, X=X, y=y, idx=np.asarray(idx), peps=np.asarray(peps),
                        groups=groups, rowg=rowg,
                        wtkeys=np.asarray(list(psiwt)), wtvals=np.asarray(list(psiwt.values())))
    return peps, X, y, np.asarray(idx), rowg, groups, psiwt


def macro(scores, y, idx):
    return dr.macro_auroc(scores, y, idx)


def per_peptide(scores, y, idx):
    return dr.macro_auroc(scores, y, idx)[1]


def compare(per_a, per_b, groups, rng_seed=BOOT_SEED):
    """Bootstrap ghép cặp theo cụm trên AUROC từng peptide."""
    keep = [i for i in range(len(per_a)) if per_a[i] is not None and per_b[i] is not None]
    delta = np.array([per_a[i] - per_b[i] for i in keep])
    g = np.asarray(groups)[keep]
    u = sorted(set(g))
    rng = np.random.default_rng(rng_seed)
    boot = [float(np.mean(np.concatenate([delta[g == c] for c in rng.choice(u, len(u), replace=True)])))
            for _ in range(N_BOOT)]
    return {'delta': float(delta.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist(),
            'n_peptides': len(keep), 'n_clusters': len(u)}


def main():
    # --- bộ gốc 91 peptide: định nghĩa outer-test, không bao giờ đổi ---
    peps0, X0, y0, idx0, rowg0, groups0, psiwt0 = build(rd.DEGRON_PSI_MAX, 'base')
    print(f'bộ gốc: {len(peps0)} peptide, {len(set(groups0))} cụm, {len(y0)} ô', flush=True)

    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]

    # cổng tự kiểm: phải trùng folds của G2
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    g2_clusters = [f['test_clusters'] for f in g2['folds']]
    assert fold_clusters == g2_clusters, 'phép chia outer KHÔNG trùng G2 -> dừng theo PROTOCOL §3'
    print('cổng tự kiểm: 5 fold trùng khớp folds của G2 [OK]', flush=True)

    # --- bộ nới ngưỡng ---
    pepsE, XE, yE, idxE, rowgE, groupsE, psiwtE = build(EXT_PSI_MAX, f'ext{EXT_PSI_MAX}')
    new_peps = [p for p in pepsE if p not in set(peps0)]
    new_pos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[new_pos[p]]) for p in new_peps])
    new_groups = {groupsE[new_pos[p]] for p in new_peps}
    print(f'bộ nới {EXT_PSI_MAX}: {len(pepsE)} peptide; thêm {len(new_peps)} peptide, '
          f'{len(new_rows)} ô, {len(new_groups - set(groups0))} cụm mới', flush=True)

    stats_new = {
        'n_new_peptides': len(new_peps),
        'n_new_cells': int(len(new_rows)),
        'n_new_clusters_not_in_base': len(new_groups - set(groups0)),
        'positive_rate_new': float(np.mean(yE[new_rows] >= rd.RESCUE_DELTA)),
        'positive_rate_base': float(np.mean(y0 >= rd.RESCUE_DELTA)),
        'dpsi_new': {'mean': float(yE[new_rows].mean()),
                     'median': float(np.median(yE[new_rows])),
                     'p95': float(np.quantile(yE[new_rows], .95))},
        'dpsi_base': {'mean': float(y0.mean()), 'median': float(np.median(y0)),
                      'p95': float(np.quantile(y0, .95))},
        'psi_wt_new': {'median': float(statistics.median([psiwtE[p] for p in new_peps])),
                       'min': float(min(psiwtE[p] for p in new_peps)),
                       'max': float(max(psiwtE[p] for p in new_peps))},
        'psi_wt_base': {'median': float(statistics.median(list(psiwt0.values())))},
    }
    print('  tỉ lệ ô dương: nhóm mới %.4f vs nhóm gốc %.4f'
          % (stats_new['positive_rate_new'], stats_new['positive_rate_base']), flush=True)

    # --- gộp: hàng của bộ gốc giữ nguyên chỉ số, hàng mới nối vào sau ---
    Xc = np.vstack([X0, XE[new_rows]])
    yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    base_n = len(y0)

    results = {}
    excluded = {}
    for model in ('ridge', 'gate_no_pap'):
        results[model] = {}
        for level in LEVELS + ['ext']:
            key = 'ext' if level == 'ext' else f'{int(level * 100)}'
            per_seed_scores, hyper = [], []
            for seed in SEEDS:
                out = np.full(base_n, np.nan)
                for fold, (_, te_idx) in enumerate(folds):
                    test_clusters = set(fold_clusters[fold])
                    te = te_idx                                   # chỉ số trong bộ gốc
                    tr_base = np.array([i for i in range(base_n)
                                        if rowg0[i] not in test_clusters])
                    tr_clusters = sorted(set(rowgc[tr_base]))
                    rng = np.random.default_rng(seed * 1000 + fold)
                    order = rng.permutation(tr_clusters)
                    if level == 'ext':
                        chosen = set(tr_clusters)                  # 100% cụm của bộ gốc
                        extra = np.array([i for i in range(base_n, len(yc))
                                          if rowgc[i] not in test_clusters], dtype=int)
                        excluded[f'fold{fold}'] = int(len(new_rows) - len(extra))
                        pool = np.concatenate([tr_base, extra])
                    else:
                        k = max(1, int(round(level * len(order))))
                        chosen = set(order[:k])
                        pool = np.array([i for i in tr_base if rowgc[i] in chosen], dtype=int)
                    gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                    ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
                    train, val = pool[ti], pool[vi]
                    assert not (set(rowgc[train]) & test_clusters)
                    assert not (set(rowgc[val]) & test_clusters)
                    if model == 'ridge':
                        pred, hp = ridge(Xc, yc, train, val, te)
                    else:
                        pred, hp = neural(np.c_[Xc, np.zeros(len(yc))], yc, train, val, te, seed)
                    out[te] = pred
                    hyper.append({'seed': seed, 'fold': fold, 'epoch_or_alpha': hp,
                                  'n_train_clusters': len(chosen) if level != 'ext'
                                  else len(set(rowgc[pool])),
                                  'n_train_cells': int(len(pool))})
                assert not np.isnan(out).any()
                per_seed_scores.append(out)
                print(f'  {model:12s} {key:>4s} seed {seed}: '
                      f'{macro(out, y0, idx0)[0]:.4f}', flush=True)
            ens = np.mean(per_seed_scores, axis=0)
            results[model][key] = {
                'macro_auroc_ensemble': macro(ens, y0, idx0)[0],
                'macro_auroc_per_seed': [macro(s, y0, idx0)[0] for s in per_seed_scores],
                'per_peptide': macro(ens, y0, idx0)[1],
                'per_peptide_by_seed': [macro(s, y0, idx0)[1] for s in per_seed_scores],
                'hyper': hyper,
            }

    # --- tiêu chí PROTOCOL §5 ---
    verdict = {}
    for model in results:
        r = results[model]
        curve = [r[f'{int(l * 100)}']['macro_auroc_ensemble'] for l in LEVELS]
        mono = all(curve[i] <= curve[i + 1] + 1e-12 for i in range(len(curve) - 1))
        c = compare(r['100']['per_peptide'], r['50']['per_peptide'], groups0)
        p1_a = c['ci95'][0] > 0
        ext = compare(r['ext']['per_peptide'], r['100']['per_peptide'], groups0)
        per_seed_ext = [compare(r['ext']['per_peptide_by_seed'][i],
                                r['100']['per_peptide_by_seed'][i], groups0)['delta']
                        for i in range(len(SEEDS))]
        verdict[model] = {
            'curve': curve,
            'P1_delta_100_minus_50': c,
            'P1_criterion_a_ci_above_zero': bool(p1_a),
            'P1_criterion_b_monotone': bool(mono),
            'P1_verdict': ('hỗ trợ' if (p1_a and mono) else
                           'hỗ trợ một phần' if p1_a else
                           'chưa đủ bằng chứng cho giả thuyết thiếu nhãn'),
            'P0_delta_ext_minus_100': ext,
            'P0_delta_per_seed': per_seed_ext,
            'P0_criterion_a_ci_above_zero': bool(ext['ci95'][0] > 0),
            'P0_criterion_b_all_seeds_positive': bool(all(d > 0 for d in per_seed_ext)),
            'P0_verdict': ('nhận' if (ext['ci95'][0] > 0 and all(d > 0 for d in per_seed_ext))
                           else 'lợi ích chưa bền qua seed' if ext['ci95'][0] > 0
                           else 'kết luận âm: nới miền degron không thêm tín hiệu học được'),
        }
        print(f"\n{model}: curve={[round(x, 4) for x in curve]}")
        print(f"  P1 {verdict[model]['P1_verdict']}: delta={c['delta']:+.4f} CI={c['ci95']}")
        print(f"  P0 {verdict[model]['P0_verdict']}: delta={ext['delta']:+.4f} CI={ext['ci95']}"
              f" per-seed={[round(d, 4) for d in per_seed_ext]}", flush=True)

    out = {
        'protocol': 'PROTOCOL.md 22/10/2026; outer-test = đúng ô của bộ 91 peptide G2; '
                    'peptide nới ngưỡng chỉ vào outer-train; benchmark phát triển OOF, '
                    'không phải kiểm chứng ngoài độc lập',
        'seeds': SEEDS, 'levels': LEVELS, 'ext_degron_psi_max': EXT_PSI_MAX,
        'rescue_delta': rd.RESCUE_DELTA, 'base_degron_psi_max': rd.DEGRON_PSI_MAX,
        'n_base_peptides': len(peps0), 'n_base_clusters': len(set(groups0)),
        'n_base_cells': int(len(y0)),
        'fold_check_matches_g2': True,
        'g2_reference_macro_auroc': g2['macro_auroc'],
        'new_group_stats': stats_new,
        'new_peptides_excluded_per_fold_due_to_test_cluster': excluded,
        'results': {m: {k: {kk: vv for kk, vv in v.items() if kk != 'per_peptide_by_seed'}
                        for k, v in results[m].items()} for m in results},
        'verdict': verdict,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'versions': {'numpy': np.__version__, 'torch': torch.__version__,
                     'python': sys.version},
    }
    (HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f"\n-> {HERE / 'results.json'}")


if __name__ == '__main__':
    main()
