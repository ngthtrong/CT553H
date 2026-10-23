"""Phần C: độ nhạy ngưỡng degron (3,5/4,0/4,5/5,0), cov50 và RESCUE_DELTA.

Tiêu chí ở PROTOCOL-C.md. Cả bốn ngưỡng chạy trong MỘT lượt và báo đầy đủ;
cấu hình chính của đề tài vẫn là 4,0 theo phần A, lưới này chỉ là phân tích độ nhạy.

Outer-test ở mọi mức = đúng ô của bộ 91 peptide (miền ngưỡng 3,0).
Peptide nới ngưỡng chỉ vào outer-train.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/learning-curve-2026-10-22/run_sensitivity.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib, statistics
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_curve as A

TOPIC = A.TOPIC
rd, dr = A.rd, A.dr
SEEDS = A.SEEDS
THRESHOLDS = [3.5, 4.0, 4.5, 5.0]
DELTAS = [0.5, 1.0, 1.5]          # RESCUE_DELTA khi đánh giá
MAIN_DELTA = 1.0
PREREG_THRESHOLD = 4.0            # cấu hình đã tiền đăng ký ở phần A
N_BOOT = A.N_BOOT
BOOT_SEED = A.BOOT_SEED


def load_cov50():
    rep = {}
    with (TOPIC / 'data/interim/protein-id30-cov50_cluster.tsv').open(encoding='utf-8') as fh:
        for line in fh:
            r, m = line.rstrip('\n').split('\t')[:2]
            rep[m] = r
    return rep


def macro_at(scores, y, idx, delta):
    """AUROC macro theo peptide, ô dương khi y >= delta."""
    per = []
    for a, b in idx:
        per.append(dr.auroc(scores[a:b], y[a:b] >= delta))
    ok = [v for v in per if v is not None]
    return (statistics.mean(ok) if ok else None), per


def compare_per(per_a, per_b, groups):
    keep = [i for i in range(len(per_a)) if per_a[i] is not None and per_b[i] is not None]
    delta = np.array([per_a[i] - per_b[i] for i in keep])
    g = np.asarray(groups)[keep]
    u = sorted(set(g))
    rng = np.random.default_rng(BOOT_SEED)
    boot = [float(np.mean(np.concatenate([delta[g == c] for c in rng.choice(u, len(u), replace=True)])))
            for _ in range(N_BOOT)]
    return {'delta': float(delta.mean()), 'ci95': np.quantile(boot, [.025, .975]).tolist(),
            'n_peptides': len(keep), 'n_clusters': len(u)}


def oof(Xc, yc, rowgc, base_n, folds, fold_clusters, rowg_base, model, seed, extra_all):
    """Một lượt OOF trên miền base. extra_all=None -> chỉ dùng nhãn base."""
    out = np.full(base_n, np.nan)
    excl = {}
    for fold, (_, te) in enumerate(folds):
        tc = set(fold_clusters[fold])
        tr_base = np.array([i for i in range(base_n) if rowg_base[i] not in tc])
        if extra_all is None:
            pool = tr_base
        else:
            extra = np.array([i for i in extra_all if rowgc[i] not in tc], dtype=int)
            excl[f'fold{fold}'] = int(len(extra_all) - len(extra))
            pool = np.concatenate([tr_base, extra])
        gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
        ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
        train, val = pool[ti], pool[vi]
        assert not (set(rowgc[train]) & tc) and not (set(rowgc[val]) & tc)
        if model == 'ridge':
            pred, _ = A.ridge(Xc, yc, train, val, te)
        else:
            pred, _ = A.neural(np.c_[Xc, np.zeros(len(yc))], yc, train, val, te, seed)
        out[te] = pred
    assert not np.isnan(out).any()
    return out, excl


def main():
    peps0, X0, y0, idx0, rowg0_cov80, groups0_cov80, psiwt0 = A.build(rd.DEGRON_PSI_MAX, 'base')
    base_n = len(y0)
    cov50 = load_cov50()
    groups0_cov50 = np.array([cov50.get(rd.accession(p), rd.accession(p)) for p in peps0])
    rowg0_cov50 = np.concatenate([np.repeat(groups0_cov50[i], b - a)
                                  for i, (a, b) in enumerate(idx0)])
    print(f'bộ base: {len(peps0)} peptide · cov80 {len(set(groups0_cov80))} cụm · '
          f'cov50 {len(set(groups0_cov50))} cụm · {base_n} ô', flush=True)

    # --- dữ liệu thêm theo từng ngưỡng ---
    ext = {}
    for t in THRESHOLDS:
        pe, Xe, ye, idxe, _, ge, psiwte = A.build(t, f'ext{t}')
        new = [p for p in pe if p not in set(peps0)]
        pos = {p: i for i, p in enumerate(pe)}
        rows = np.concatenate([np.arange(*idxe[pos[p]]) for p in new])
        ext[t] = {
            'X': Xe[rows], 'y': ye[rows],
            'g80': np.concatenate([np.repeat(ge[pos[p]], idxe[pos[p]][1] - idxe[pos[p]][0])
                                   for p in new]),
            'g50': np.concatenate([np.repeat(cov50.get(rd.accession(p), rd.accession(p)),
                                             idxe[pos[p]][1] - idxe[pos[p]][0]) for p in new]),
            'stats': {
                'n_new_peptides': len(new), 'n_new_cells': int(len(rows)),
                'n_new_clusters_cov80_not_in_base': len(set(ge[pos[p]] for p in new)
                                                        - set(groups0_cov80)),
                'positive_rate_at_delta1': float(np.mean(ye[rows] >= MAIN_DELTA)),
                'psi_wt_median': float(statistics.median([psiwte[p] for p in new])),
            },
        }
        print(f"  ngưỡng {t}: +{len(new)} peptide, {len(rows)} ô, "
              f"{ext[t]['stats']['n_new_clusters_cov80_not_in_base']} cụm cov80 mới, "
              f"ô dương {ext[t]['stats']['positive_rate_at_delta1']:.4f}", flush=True)

    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())

    runs = {}        # (clustering, model, level) -> {delta: (macro, per_peptide)}
    exclusions = {}
    for clustering in ('cov80', 'cov50'):
        rowg_base = rowg0_cov80 if clustering == 'cov80' else rowg0_cov50
        groups_base = groups0_cov80 if clustering == 'cov80' else groups0_cov50
        folds = list(GroupKFold(5).split(X0, y0, rowg_base))
        fold_clusters = [sorted(set(rowg_base[te])) for _, te in folds]
        if clustering == 'cov80':
            assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'fold lệch G2'
            print('cổng tự kiểm cov80: 5 fold trùng khớp folds của G2 [OK]', flush=True)
        else:
            print(f'cov50: {len(set(rowg_base))} cụm, fold sizes '
                  f'{[len(c) for c in fold_clusters]}', flush=True)
        models = ('ridge', 'gate_no_pap') if clustering == 'cov80' else ('ridge',)
        for model in models:
            for level in ['base'] + THRESHOLDS:
                if level == 'base':
                    Xc, yc, rowgc, extra_all = X0, y0, rowg_base, None
                else:
                    e = ext[level]
                    Xc = np.vstack([X0, e['X']])
                    yc = np.concatenate([y0, e['y']])
                    rowgc = np.concatenate([rowg_base,
                                            e['g80'] if clustering == 'cov80' else e['g50']])
                    extra_all = np.arange(base_n, len(yc))
                per_seed = []
                for seed in SEEDS:
                    o, excl = oof(Xc, yc, rowgc, base_n, folds, fold_clusters,
                                  rowg_base, model, seed, extra_all)
                    per_seed.append(o)
                    if level != 'base' and clustering == 'cov80' and model == 'ridge':
                        exclusions[str(level)] = excl
                ens = np.mean(per_seed, axis=0)
                key = (clustering, model, str(level))
                runs[key] = {
                    'ensemble': {str(d): macro_at(ens, y0, idx0, d) for d in DELTAS},
                    'per_seed_macro': {str(d): [macro_at(s, y0, idx0, d)[0] for s in per_seed]
                                       for d in DELTAS},
                    'per_seed_per_peptide': {str(d): [macro_at(s, y0, idx0, d)[1]
                                                      for s in per_seed] for d in DELTAS},
                    'groups_base': groups_base,
                }
                print(f"  {clustering} {model:12s} {str(level):>4s}: " +
                      ' '.join(f"d{d}={runs[key]['ensemble'][str(d)][0]:.4f}" for d in DELTAS),
                      flush=True)

    # ---------------- tiêu chí ----------------
    def deltas_for(clustering, model, d):
        base = runs[(clustering, model, 'base')]
        out = {}
        for t in THRESHOLDS:
            r = runs[(clustering, model, str(t))]
            c = compare_per(r['ensemble'][str(d)][1], base['ensemble'][str(d)][1],
                            base['groups_base'])
            per_seed = [compare_per(r['per_seed_per_peptide'][str(d)][i],
                                    base['per_seed_per_peptide'][str(d)][i],
                                    base['groups_base'])['delta']
                        for i in range(len(SEEDS))]
            c['per_seed_delta'] = per_seed
            c['all_seeds_positive'] = bool(all(x > 0 for x in per_seed))
            c['auroc_ext'] = r['ensemble'][str(d)][0]
            out[str(t)] = c
        out['_base_auroc'] = base['ensemble'][str(d)][0]
        return out

    main_grid = deltas_for('cov80', 'ridge', MAIN_DELTA)
    dd = [main_grid[str(t)]['delta'] for t in THRESHOLDS]
    all_pos = all(main_grid[str(t)]['ci95'][0] > 0 for t in THRESHOLDS)
    mono = all(dd[i] <= dd[i + 1] + 1e-12 for i in range(len(dd) - 1))
    best_i = int(np.argmax(dd))
    sat = all(dd[j] <= dd[best_i] + 0.002 for j in range(best_i, len(dd)))
    decline = [str(THRESHOLDS[j]) for j in range(len(dd))
               if dd[j] < dd[best_i] - 0.002 and j > best_i]
    if mono and all_pos:
        c1 = 'lợi ích còn tăng theo ngưỡng'
    elif decline:
        c1 = f'suy giảm sau {THRESHOLDS[best_i]}'
    elif sat:
        c1 = f'bão hòa tại {THRESHOLDS[best_i]}'
    else:
        c1 = 'không thuộc ba dạng chốt trước; xem mô tả'

    # C2: độ bền của ngưỡng 4,0
    c2_conds = {}
    for d in DELTAS:
        g = deltas_for('cov80', 'ridge', d)
        c2_conds[f'cov80_delta{d}'] = g[str(PREREG_THRESHOLD)]
    g50 = deltas_for('cov50', 'ridge', MAIN_DELTA)
    c2_conds[f'cov50_delta{MAIN_DELTA}'] = g50[str(PREREG_THRESHOLD)]
    failed = [k for k, v in c2_conds.items() if not v['ci95'][0] > 0]
    c2 = 'bền' if not failed else f"bền có điều kiện; không đạt: {', '.join(failed)}"

    # C3: nhất quán hai mô hình
    net_grid = deltas_for('cov80', 'gate_no_pap', MAIN_DELTA)
    dn = [net_grid[str(t)]['delta'] for t in THRESHOLDS]
    same_sign = all((a > 0) == (b > 0) for a, b in zip(dd, dn))
    same_order = int(np.argmax(dd)) == int(np.argmax(dn))
    c3 = ('hai mô hình đồng thuận về hình dạng' if (same_sign and same_order)
          else 'lệch giữa hai mô hình')

    print(f'\nC1 {c1}')
    print(f'   ridge cov80 d1.0: ' +
          ' '.join(f'Δ({t})={main_grid[str(t)]["delta"]:+.4f}' for t in THRESHOLDS))
    print(f'C2 {c2}')
    print(f'C3 {c3}: net ' +
          ' '.join(f'Δ({t})={net_grid[str(t)]["delta"]:+.4f}' for t in THRESHOLDS), flush=True)

    out = {
        'protocol': 'PROTOCOL-C.md; bốn ngưỡng chạy một lượt và báo đầy đủ; cấu hình chính '
                    'của đề tài vẫn là 4,0 theo phần A; lưới này là phân tích độ nhạy, '
                    'KHÔNG dùng để chọn cấu hình',
        'seeds': SEEDS, 'thresholds': THRESHOLDS, 'rescue_deltas': DELTAS,
        'main_rescue_delta': MAIN_DELTA, 'prereg_threshold': PREREG_THRESHOLD,
        'base_degron_psi_max': rd.DEGRON_PSI_MAX,
        'n_base_peptides': len(peps0), 'n_base_cells': base_n,
        'n_base_clusters': {'cov80': len(set(groups0_cov80)), 'cov50': len(set(groups0_cov50))},
        'fold_check_cov80_matches_g2': True,
        'added_data_stats': {str(t): ext[t]['stats'] for t in THRESHOLDS},
        'excluded_cells_per_fold_cov80': exclusions,
        'absolute_auroc': {f'{c}|{m}|{l}': {str(d): runs[(c, m, l)]['ensemble'][str(d)][0]
                                            for d in DELTAS}
                           for (c, m, l) in runs},
        'per_seed_macro': {f'{c}|{m}|{l}': runs[(c, m, l)]['per_seed_macro']
                           for (c, m, l) in runs},
        'grid_ridge_cov80': {str(d): {k: v for k, v in deltas_for('cov80', 'ridge', d).items()}
                             for d in DELTAS},
        'grid_ridge_cov50_main_delta': g50,
        'grid_net_cov80_main_delta': net_grid,
        'verdict': {'C1_shape': c1, 'C1_monotone': bool(mono), 'C1_all_ci_above_zero': bool(all_pos),
                    'C1_argmax_threshold': THRESHOLDS[best_i],
                    'C2_robustness': c2, 'C2_failed_conditions': failed,
                    'C3_model_agreement': c3},
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'versions': {'numpy': np.__version__, 'torch': torch.__version__},
    }
    (HERE / 'results-c.json').write_text(json.dumps(out, indent=2, ensure_ascii=False,
                                                    default=float) + '\n')
    print(f"\n-> {HERE / 'results-c.json'}")


if __name__ == '__main__':
    main()
