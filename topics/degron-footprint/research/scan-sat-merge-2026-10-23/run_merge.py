#!/usr/bin/env python3
"""Phần B — trộn nhãn bộ quét vào huấn luyện trên bộ bão hòa. Tiêu chí chốt trước ở PROTOCOL.md.

Outer-test = đúng ô bộ 91 peptide của G2; peptide bão hòa `ext4.0` và mọi peptide quét chỉ vào
outer-train, và peptide quét thuộc cụm test (và, ở bước chọn siêu tham số, cụm validation) bị loại.

Chạy từ gốc repo (CPU, 2 thread):
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/scan-sat-merge-2026-10-23/run_merge.py [--no-neural]
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import residue_data as rd          # noqa: E402
import derisk as dr                # noqa: E402
import run_curve as rc             # noqa: E402

torch.set_num_threads(2)
SEEDS = [17, 29, 43]
ALPHAS = [1.0, 10.0, 100.0, 1000.0]
WEIGHTS = [0.05, 0.2, 1.0]
EXT_PSI = 4.0
SCAN_THR_MAIN, SCAN_THR_SENS = 4.0, 3.0
LR_MAIN, LR_ALT = 2e-3, 5e-4
MIN_PER_CLASS = 3


# ------------------------------------------------------------------ ridge theo thống kê đủ
def suff(X, y):
    """T = Z'Z, r = Z'y với Z = [1, X]."""
    Z = np.empty((len(y), X.shape[1] + 1))
    Z[:, 0] = 1.0
    Z[:, 1:] = X
    return Z.T @ Z, Z.T @ y


def solve_plain(T, r, alpha):
    D = np.full(T.shape[0], alpha); D[0] = 0.0
    return np.linalg.solve(T + np.diag(D), r)


def solve_s2(Ts, rs, Tc, rcv, w, alpha):
    """[1, X, 1{quét}·X]: trả khối chung [1, X] (hàng bão hòa có khối riêng = 0)."""
    p1 = Ts.shape[0]
    M = np.zeros((2 * p1 - 1, 2 * p1 - 1))
    M[:p1, :p1] = Ts + w * Tc
    M[:p1, p1:] = w * Tc[:, 1:]
    M[p1:, :p1] = w * Tc[1:, :]
    M[p1:, p1:] = w * Tc[1:, 1:]
    r = np.concatenate([rs + w * rcv, w * rcv[1:]])
    D = np.full(M.shape[0], alpha); D[0] = 0.0
    return np.linalg.solve(M + np.diag(D), r)[:p1]


def lin(theta, X):
    return theta[0] + X @ theta[1:]


def mse(a, b):
    return float(np.mean((a - b) ** 2))


# ------------------------------------------------------------------ mạng
def train_net(xx, yy, tr, va, lr, seed, init_state=None, max_epoch=60, patience=8):
    torch.manual_seed(seed)
    net = rc.Gate(gated=True, pap=False)
    if init_state is not None:
        net.load_state_dict(init_state)
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=.01)
    rng = np.random.default_rng(seed)
    best, state, eb = 1e99, None, 0
    for epoch in range(1, max_epoch + 1):
        net.train()
        for batch in np.array_split(rng.permutation(tr), max(1, len(tr) // 1024)):
            loss = ((net(xx[batch]) - yy[batch]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad():
            v = float(((net(xx[va]) - yy[va]) ** 2).mean())
        if v < best - 1e-6:
            best, state, eb = v, {k: t.detach().clone() for k, t in net.state_dict().items()}, epoch
        if epoch - eb >= patience:
            break
    net.load_state_dict(state); net.eval()
    return net, state, eb, best


def net_predict(net, xx, te):
    with torch.no_grad():
        return net(xx[te]).numpy()


# ------------------------------------------------------------------ dữ liệu quét
def load_scan(thr, rep):
    seqs, subs = rd.load_scan_csv()
    scan = rd.build_scanning(rd.load_psi('rep1'), seqs, subs, degron_psi_max=thr)
    peps, rows, y, idx = dr.rows_and_labels(scan, 'scan')
    X = dr.featurize(rows, {'pair', 'comp', 'ctx'})
    grp = np.array([rep.get(rd.accession(p), rd.accession(p)) for p in peps])
    rowg = np.concatenate([np.repeat(grp[i], b - a) for i, (a, b) in enumerate(idx)])
    pep_of_row = np.concatenate([np.repeat(i, b - a) for i, (a, b) in enumerate(idx)])
    return {'peps': peps, 'X': X, 'y': y, 'rowg': rowg, 'pep_of_row': pep_of_row,
            'n_peptides': len(peps), 'n_cells': len(y), 'n_clusters': len(set(grp))}


def pair_ids(X):
    return X[:, :20].argmax(1) * 20 + X[:, 20:40].argmax(1)


def macro_subset(scores, y, idx, mask, min_class=MIN_PER_CLASS):
    per = []
    for a, b in idx:
        m = mask[a:b]
        yy, ss = y[a:b][m] >= rd.RESCUE_DELTA, scores[a:b][m]
        if yy.sum() >= min_class and (~yy).sum() >= min_class:
            per.append(dr.auroc(ss, yy))
        else:
            per.append(None)
    return per


def main():
    run_neural = '--no-neural' not in sys.argv
    t0 = time.time()
    rep = rd.load_clusters()

    # ---- bộ bão hòa: đúng cách run_curve dựng pool ext ----
    peps0, X0, y0, idx0, rowg0, groups0, psiwt0 = rc.build(rd.DEGRON_PSI_MAX, 'base')
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'outer fold KHÔNG trùng G2 -> dừng'
    print('cổng tự kiểm: 5 fold trùng G2 [OK]', flush=True)

    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(EXT_PSI, f'ext{EXT_PSI}')
    new_peps = [p for p in pepsE if p not in set(peps0)]
    pos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[pos[p]]) for p in new_peps])
    Xc = np.vstack([X0, XE[new_rows]]); yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    base_n = len(y0)
    sat_clusters_all = set(rowgc)
    in_scan_pair_cache = {}

    results = {}
    meta = {'folds': [], 'scan': {}}

    def pools(fold, seed):
        te = folds[fold][1]
        test_clusters = set(fold_clusters[fold])
        tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
        extra = np.array([i for i in range(base_n, len(yc)) if rowgc[i] not in test_clusters], dtype=int)
        pool = np.concatenate([tr_base, extra])
        ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                      .split(pool, yc[pool], rowgc[pool]))
        return te, test_clusters, pool[ti], pool[vi]

    def record(arm, preds_by_seed, hyper):
        ens = np.mean(preds_by_seed, axis=0)
        m_ens, per = rc.macro(ens, y0, idx0)
        per_seed = [rc.macro(s, y0, idx0) for s in preds_by_seed]
        results[arm] = {'macro_auroc_ensemble': m_ens, 'per_peptide': per,
                        'macro_auroc_per_seed': [m for m, _ in per_seed],
                        'per_peptide_by_seed': [p for _, p in per_seed],
                        'hyper': hyper, '_ens': ens, '_seed_scores': preds_by_seed}
        print(f'  {arm:34s} ensemble {m_ens:.4f}  seeds {[round(m, 4) for m, _ in per_seed]}', flush=True)

    # ---- baseline A0 / A1 (sklearn, đúng run_curve) ----
    for arm, rows_fn in (('A1_sat_ext', 'ext'), ('A0_sat_base', 'base')):
        outs, hyp = [], []
        for seed in SEEDS:
            out = np.full(base_n, np.nan)
            for fold in range(5):
                te, test_clusters, train, val = pools(fold, seed)
                if rows_fn == 'base':
                    # đúng run_curve level 100%: pool chỉ từ bộ gốc
                    tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
                    ti, vi = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                                  .split(tr_base, yc[tr_base], rowgc[tr_base]))
                    train, val = tr_base[ti], tr_base[vi]
                pred, a = rc.ridge(Xc, yc, train, val, te)
                out[te] = pred; hyp.append({'seed': seed, 'fold': fold, 'alpha': a})
            outs.append(out)
        record(arm, outs, hyp)
    ref_a1 = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())
    ref_a1 = ref_a1['results']['ridge']['ext']['macro_auroc_ensemble']
    ref_a0 = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())
    ref_a0 = ref_a0['results']['ridge']['100']['macro_auroc_ensemble']
    assert abs(results['A1_sat_ext']['macro_auroc_ensemble'] - ref_a1) < 1e-9, 'A1 không tái lập P0'
    assert abs(results['A0_sat_base']['macro_auroc_ensemble'] - ref_a0) < 1e-9, 'A0 không tái lập 0,8082'
    print('cổng tái lập: A1 = %.4f, A0 = %.4f khớp P0/G2 [OK]' % (ref_a1, ref_a0), flush=True)

    # ---- phép tự kiểm bộ giải thống kê đủ so với sklearn trên A1 ----
    te, tc, train, val = pools(0, SEEDS[0])
    Tt, rt = suff(Xc[train][:, :180], yc[train])
    a_ref = [h['alpha'] for h in results['A1_sat_ext']['hyper'] if h['seed'] == SEEDS[0] and h['fold'] == 0][0]
    full = np.concatenate([train, val])
    Tf, rf = suff(Xc[full][:, :180], yc[full])
    mine = lin(solve_plain(Tf, rf, a_ref), Xc[te][:, :180])
    from sklearn.linear_model import Ridge
    sk = Ridge(alpha=a_ref).fit(Xc[full][:, :180], yc[full]).predict(Xc[te][:, :180])
    assert np.max(np.abs(mine - sk)) < 1e-6, f'bộ giải lệch sklearn: {np.max(np.abs(mine - sk))}'
    print('tự kiểm: bộ giải thống kê đủ khớp sklearn Ridge (max |Δ| %.2e) [OK]' % np.max(np.abs(mine - sk)), flush=True)

    sat_pairs_te = pair_ids(X0)

    # ---------------------------------------------------------------- các cấu hình ngưỡng quét
    for thr, tag in ((SCAN_THR_MAIN, 'thr4.0'), (SCAN_THR_SENS, 'thr3.0')):
        sc = load_scan(thr, rep)
        meta['scan'][tag] = {k: sc[k] for k in ('n_peptides', 'n_cells', 'n_clusters')}
        scan_pairs = set(pair_ids(sc['X']).tolist())
        meta['scan'][tag]['n_distinct_pairs'] = len(scan_pairs)
        in_pair = np.isin(sat_pairs_te, list(scan_pairs))
        meta['scan'][tag]['frac_sat_test_cells_in_scan_pairs'] = float(in_pair.mean())
        in_sat_cluster = np.isin(sc['rowg'], list(sat_clusters_all))
        meta['scan'][tag]['n_scan_cells_in_sat_clusters'] = int(in_sat_cluster.sum())
        print(f'\n=== ngưỡng quét {thr}: {sc["n_peptides"]} peptide, {sc["n_cells"]} ô, '
              f'{sc["n_clusters"]} cụm; {in_sat_cluster.sum()} ô thuộc cụm bão hòa ===  '
              f'({time.time() - t0:.0f}s)', flush=True)
        Xs, ys, gs = sc['X'], sc['y'], sc['rowg']

        arms = ['S0_scan_only', 'S1_pool_naive', 'S2_pool_source', 'S2d_pool_source_disjoint', 'S3_scan_prior']
        outs = {a: [np.full(base_n, np.nan) for _ in SEEDS] for a in arms}
        hyp = {a: [] for a in arms}
        excl = []
        for si, seed in enumerate(SEEDS):
            for fold in range(5):
                te, test_clusters, train, val = pools(fold, seed)
                full = np.concatenate([train, val])
                val_clusters = set(rowgc[val])
                keep_full = ~np.isin(gs, list(test_clusters))
                keep_in = keep_full & ~np.isin(gs, list(val_clusters))
                dis = ~in_sat_cluster
                if si == 0:
                    excl.append({'fold': fold, 'scan_cells_removed_test_clusters': int((~keep_full).sum()),
                                 'scan_peptides_removed_test_clusters': int(len(set(sc['pep_of_row'][~keep_full]))),
                                 'scan_cells_removed_also_val_clusters_seed17': int((keep_full & ~keep_in).sum())})
                Xtr, ytr = Xc[train][:, :180], yc[train]
                Xva, yva = Xc[val][:, :180], yc[val]
                Ts_in, rs_in = suff(Xtr, ytr)
                Ts_full, rs_full = suff(Xc[full][:, :180], yc[full])
                Xte = Xc[te][:, :180]

                # holdout cụm quét để chọn alpha của mô hình quét (S0/S3)
                rng = np.random.default_rng(seed * 1000 + fold + 7)
                uq = np.array(sorted(set(gs[keep_full])))
                ho = set(rng.permutation(uq)[:max(1, int(.2 * len(uq)))])
                ho_mask = np.isin(gs, list(ho)) & keep_full
                tr_mask = keep_full & ~ho_mask
                T_a, r_a = suff(Xs[tr_mask], ys[tr_mask])
                best_as = min((mse(lin(solve_plain(T_a, r_a, a), Xs[ho_mask]), ys[ho_mask]), a)
                              for a in ALPHAS)[1]

                def scan_stats(mask):
                    return suff(Xs[mask], ys[mask])

                for arm in ('S1_pool_naive', 'S2_pool_source', 'S2d_pool_source_disjoint'):
                    m_in = keep_in & (dis if arm.startswith('S2d') else True)
                    m_full = keep_full & (dis if arm.startswith('S2d') else True)
                    Tc_in, rc_in = scan_stats(m_in)
                    best = None
                    for w in WEIGHTS:
                        for a in ALPHAS:
                            if arm.startswith('S1'):
                                th = solve_plain(Ts_in + w * Tc_in, rs_in + w * rc_in, a)
                            else:
                                th = solve_s2(Ts_in, rs_in, Tc_in, rc_in, w, a)
                            v = mse(lin(th, Xva), yva)
                            if best is None or v < best[0]:
                                best = (v, w, a)
                    _, w, a = best
                    Tc_f, rc_f = scan_stats(m_full)
                    if arm.startswith('S1'):
                        th = solve_plain(Ts_full + w * Tc_f, rs_full + w * rc_f, a)
                    else:
                        th = solve_s2(Ts_full, rs_full, Tc_f, rc_f, w, a)
                    outs[arm][si][te] = lin(th, Xte)
                    hyp[arm].append({'seed': seed, 'fold': fold, 'w': w, 'alpha': a, 'val_mse': best[0]})

                # S0 / S3: mô hình quét → tiên nghiệm
                Tin, rin = scan_stats(keep_in)
                th0_in = solve_plain(Tin, rin, best_as)
                Tfu, rfu = scan_stats(keep_full)
                th0 = solve_plain(Tfu, rfu, best_as)
                outs['S0_scan_only'][si][te] = lin(th0, Xte)
                hyp['S0_scan_only'].append({'seed': seed, 'fold': fold, 'alpha': best_as})
                # S3: ridge bão hòa trên phần dư của mô hình quét (inner dùng mô hình không thấy cụm val)
                Zi = np.c_[np.ones(len(ytr)), Xtr]
                resid_in = ytr - Zi @ th0_in
                T_in, r_in = suff(Xtr, resid_in)
                best = min((mse(lin(solve_plain(T_in, r_in, a), Xva) + lin(th0_in, Xva), yva), a) for a in ALPHAS)
                a = best[1]
                Zf = np.c_[np.ones(len(full)), Xc[full][:, :180]]
                resid_f = yc[full] - Zf @ th0
                T_f, r_f = suff(Xc[full][:, :180], resid_f)
                outs['S3_scan_prior'][si][te] = lin(solve_plain(T_f, r_f, a), Xte) + lin(th0, Xte)
                hyp['S3_scan_prior'].append({'seed': seed, 'fold': fold, 'alpha': a, 'alpha_scan': best_as,
                                             'val_mse': best[0]})
            print(f'  seed {seed} xong ({time.time() - t0:.0f}s)', flush=True)
        meta['scan'][tag]['excluded_by_fold'] = excl
        for a in arms:
            assert not any(np.isnan(o).any() for o in outs[a])
            record(f'{a}@{tag}', outs[a], hyp[a])

        # ---- mạng, chỉ ở ngưỡng chính ----
        if run_neural and tag == 'thr4.0':
            print('\n--- mạng gate_no_pap ---', flush=True)
            xs_t = torch.tensor(np.c_[Xs, np.zeros(len(ys))], dtype=torch.float32)
            ys_t = torch.tensor(ys, dtype=torch.float32)
            xc_t = torch.tensor(np.c_[Xc, np.zeros(len(yc))], dtype=torch.float32)
            yc_t = torch.tensor(yc, dtype=torch.float32)
            n_arms = {'N1_rand': [np.full(base_n, np.nan) for _ in SEEDS],
                      f'N2_scan_pre_lr{LR_MAIN:g}': [np.full(base_n, np.nan) for _ in SEEDS],
                      f'N2_scan_pre_lr{LR_ALT:g}': [np.full(base_n, np.nan) for _ in SEEDS]}
            n_hyp = {k: [] for k in n_arms}
            for si, seed in enumerate(SEEDS):
                for fold in range(5):
                    te, test_clusters, train, val = pools(fold, seed)
                    val_clusters = set(rowgc[val])
                    keep_in = ~np.isin(gs, list(test_clusters | val_clusters))
                    rng = np.random.default_rng(seed * 1000 + fold + 11)
                    uq = np.array(sorted(set(gs[keep_in])))
                    ho = set(rng.permutation(uq)[:max(1, int(.2 * len(uq)))])
                    ho_m = np.isin(gs, list(ho)) & keep_in
                    pre_tr = np.where(keep_in & ~ho_m)[0]; pre_va = np.where(ho_m)[0]
                    pre_net, pre_state, pre_ep, pre_v = train_net(xs_t, ys_t, pre_tr, pre_va, LR_MAIN, seed)
                    net, _, ep, v = train_net(xc_t, yc_t, train, val, LR_MAIN, seed)
                    n_arms['N1_rand'][si][te] = net_predict(net, xc_t, te)
                    n_hyp['N1_rand'].append({'seed': seed, 'fold': fold, 'epoch': ep, 'val_mse': v})
                    for lr in (LR_MAIN, LR_ALT):
                        key = f'N2_scan_pre_lr{lr:g}'
                        net, _, ep, v = train_net(xc_t, yc_t, train, val, lr, seed, init_state=pre_state)
                        n_arms[key][si][te] = net_predict(net, xc_t, te)
                        n_hyp[key].append({'seed': seed, 'fold': fold, 'epoch': ep, 'val_mse': v,
                                           'pretrain_epoch': pre_ep, 'pretrain_val_mse': pre_v})
                    print(f'  seed {seed} fold {fold} ({time.time() - t0:.0f}s)', flush=True)
            for k in n_arms:
                assert not any(np.isnan(o).any() for o in n_arms[k])
                record(k, n_arms[k], n_hyp[k])

    # ---------------------------------------------------------------- so sánh chốt trước
    def cmp(a, b, name):
        c = rc.compare(results[a]['per_peptide'], results[b]['per_peptide'], groups0)
        ps = [rc.compare(results[a]['per_peptide_by_seed'][i], results[b]['per_peptide_by_seed'][i],
                         groups0)['delta'] for i in range(len(SEEDS))]
        rule = bool(c['ci95'][0] > 0 and all(d > 0 for d in ps))
        return {'a': a, 'b': b, 'delta': c['delta'], 'ci95': c['ci95'], 'delta_per_seed': ps,
                'n_clusters': c['n_clusters'], 'criterion_ci_above_zero': bool(c['ci95'][0] > 0),
                'criterion_all_seeds_positive': bool(all(d > 0 for d in ps)),
                'accepted_by_preregistered_rule': rule, 'ci_entirely_below_zero': bool(c['ci95'][1] < 0)}

    comparisons = {}
    for tag in ('thr4.0', 'thr3.0'):
        for arm in ('S1_pool_naive', 'S2_pool_source', 'S2d_pool_source_disjoint', 'S3_scan_prior', 'S0_scan_only'):
            comparisons[f'{arm}@{tag} - A1'] = cmp(f'{arm}@{tag}', 'A1_sat_ext', arm)
        comparisons[f'S2_pool_source@{tag} - A0'] = cmp(f'S2_pool_source@{tag}', 'A0_sat_base', 'S2')
    comparisons['A1 - A0 (P0 lặp lại)'] = cmp('A1_sat_ext', 'A0_sat_base', 'P0')
    if run_neural:
        comparisons['N2_lr2e-3 - N1'] = cmp(f'N2_scan_pre_lr{LR_MAIN:g}', 'N1_rand', 'N2')
        comparisons['N2_lr5e-4 - N1'] = cmp(f'N2_scan_pre_lr{LR_ALT:g}', 'N1_rand', 'N2b')
        comparisons['N1 - A1 (mạng so ridge)'] = cmp('N1_rand', 'A1_sat_ext', 'N1')

    # ---- chẩn đoán (iii): ô test thuộc 20 cặp của bộ quét vs còn lại ----
    diag = {}
    in_pair = np.isin(sat_pairs_te, list(set(pair_ids(load_scan(SCAN_THR_MAIN, rep)['X']).tolist())))
    # Mở rộng 23/10 (sau khi thấy kết quả chính, chỉ là báo cáo bổ sung, không đổi tiêu chí hay arm):
    # chẩn đoán cặp cho MỌI arm có dùng bộ quét, không chỉ S2 và N2 lr chính.
    diag['_fraction_test_cells_in_scan_pairs'] = float(in_pair.mean())
    for arm in [k for k in results if k.startswith(('S1_', 'S2_', 'S2d_', 'S3_', 'N2_'))]:
        base_key = 'N1_rand' if arm.startswith('N2') else 'A1_sat_ext'
        for name, mask in (('in_scan_pairs', in_pair), ('not_in_scan_pairs', ~in_pair)):
            a = macro_subset(results[arm]['_ens'], y0, idx0, mask)
            b = macro_subset(results[base_key]['_ens'], y0, idx0, mask)
            ok = [i for i in range(len(a)) if a[i] is not None and b[i] is not None]
            if len(ok) >= 5:
                c = rc.compare([a[i] for i in ok], [b[i] for i in ok], [groups0[i] for i in ok])
                diag[f'{arm} {name}'] = {'baseline': base_key, 'n_peptides_eligible': len(ok),
                                         'auroc_arm': float(np.mean([a[i] for i in ok])),
                                         'auroc_baseline': float(np.mean([b[i] for i in ok])),
                                         'delta': c['delta'], 'ci95': c['ci95']}
            else:
                diag[f'{arm} {name}'] = {'baseline': base_key, 'n_peptides_eligible': len(ok)}

    pub = {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_') and kk != 'per_peptide_by_seed'}
           for k, v in results.items()}
    out = {'protocol': 'PROTOCOL.md 23/10/2026; outer-test = ô bộ 91 peptide G2 (cổng tự kiểm trùng folds G2); '
                       'benchmark phát triển OOF, không phải kiểm chứng ngoài',
           'seeds': SEEDS, 'alphas': ALPHAS, 'scan_weights': WEIGHTS, 'ext_degron_psi_max': EXT_PSI,
           'reference': {'A1_P0_ridge_ext': ref_a1, 'A0_G2_ridge_base': ref_a0},
           'meta': meta, 'results': pub, 'comparisons': comparisons, 'diagnostic_pair_split': diag,
           'neural_run': run_neural, 'wall_seconds': round(time.time() - t0),
           'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'python': sys.version}}
    (HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print('\n=== so sánh ===')
    for k, c in comparisons.items():
        print(f"{k:42s} Δ={c['delta']:+.4f} CI=[{c['ci95'][0]:+.4f},{c['ci95'][1]:+.4f}] "
              f"seeds={[round(d, 4) for d in c['delta_per_seed']]} nhận={c['accepted_by_preregistered_rule']}")
    print('\nchẩn đoán cặp:'); print(json.dumps(diag, indent=1))
    print(f'\n-> {HERE / "results.json"}  ({time.time() - t0:.0f}s)')


if __name__ == '__main__':
    main()
