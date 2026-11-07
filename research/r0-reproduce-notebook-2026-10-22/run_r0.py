"""R0 — tái lập mốc đã biết trong môi trường notebook (Kaggle/Colab). Chỉ CPU, vài phút.

Không huấn luyện mô hình mới: chỉ chạy lại đường ridge M3 của learning-curve (mức 100% và mức nới ngưỡng 4,0),
kiểm 5 fold trùng G2, và (tuỳ chọn) chạy `calibration-p6/verify.py` để kiểm nguyên mẫu `predict.py` khớp runner.
Tiêu chí ở PROTOCOL.md (chốt SHA-256 nhúng trong notebook). Hàm `run(ctx)` được notebook gọi.

Phần vòng lặp ridge bám đúng `learning-curve-2026-10-22/run_curve.py::main` (nhánh model == 'ridge',
level == 100% và 'ext'); mọi hàm khác (`build`, `ridge`, `macro`, `compare`) được IMPORT từ run_curve.
"""
import contextlib
import io
import json
import sys
import time
import traceback

import numpy as np

SEEDS = [17, 29, 43]
TOL_AUROC = 1e-4          # PROTOCOL §3
TOL_CI = 5e-4
TOL_VERIFY = 1e-9
TOL_NEURAL_INFO = 5e-3    # chỉ thông tin (khác nền tảng/phiên bản torch)


def ridge_levels(rc, rd, GroupKFold, GroupShuffleSplit, topic):
    """Trả về (per-seed AUROC, ensemble AUROC, per-peptide ensemble) cho mức '100' và 'ext' của ridge."""
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((topic / 'research/g2-saturation-2026-10-18/results.json').read_text())
    same_folds = fold_clusters == [f['test_clusters'] for f in g2['folds']]

    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(rc.EXT_PSI_MAX, f'ext{rc.EXT_PSI_MAX}')
    in_base = set(peps0)
    new_pos = {p: i for i, p in enumerate(pepsE)}
    new_peps = [p for p in pepsE if p not in in_base]
    new_rows = np.concatenate([np.arange(*idxE[new_pos[p]]) for p in new_peps])
    Xc = np.vstack([X0, XE[new_rows]])
    yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    base_n = len(y0)

    out = {'same_folds_as_g2': bool(same_folds), 'n_base_peptides': len(peps0),
           'n_new_peptides': len(new_peps), 'n_cells_base': int(base_n)}
    for key in ('100', 'ext'):
        per_seed, scores = [], []
        for seed in SEEDS:
            pred_all = np.full(base_n, np.nan)
            for fold, (_, te) in enumerate(folds):
                test_clusters = set(fold_clusters[fold])
                tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
                if key == 'ext':
                    extra = np.array([i for i in range(base_n, len(yc)) if rowgc[i] not in test_clusters],
                                     dtype=int)
                    pool = np.concatenate([tr_base, extra])
                else:
                    pool = tr_base
                gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
                pred, _alpha = rc.ridge(Xc, yc, pool[ti], pool[vi], te)
                pred_all[te] = pred
            assert not np.isnan(pred_all).any()
            scores.append(pred_all)
            per_seed.append(rc.macro(pred_all, y0, idx0)[0])
        ens = np.mean(scores, axis=0)
        macro, per_pep = rc.macro(ens, y0, idx0)
        out[key] = {'macro_auroc_ensemble': macro, 'macro_auroc_per_seed': per_seed,
                    'per_peptide': per_pep}
    out['groups0'] = [str(g) for g in groups0]
    return out


def run(ctx, run_verify=True, run_full_curve=False):
    t0 = time.time()
    ctx.add_to_path('learning-curve-2026-10-22', 'residue-task-derisk-2026-10-15',
                    'g2-saturation-2026-10-18', 'calibration-p6-2026-10-22')
    # mốc đã commit: đọc TRƯỚC khi chạy bất cứ thứ gì có thể ghi đè results.json
    committed = json.loads((ctx.research / 'learning-curve-2026-10-22/results.json').read_text())
    import run_curve as rc
    import residue_data as rd
    from sklearn.model_selection import GroupShuffleSplit
    from nbkit import StableGroupKFold
    GroupKFold = rc.GroupKFold = StableGroupKFold       # cả run_curve.main() (cổng C) cũng dùng cách chia này
    g = ctx.gates
    res = {'tolerances': {'auroc': TOL_AUROC, 'ci': TOL_CI, 'verify': TOL_VERIFY}}

    # ---- Cổng A: ridge M3 ----
    print('Cổng A — ridge M3 (mức 100% và nới ngưỡng 4,0)')
    ra = ridge_levels(rc, rd, GroupKFold, GroupShuffleSplit, ctx.topic)
    assert ra['same_folds_as_g2'], '5 fold không trùng G2 -> dừng theo PROTOCOL §3'
    print('  5 fold trùng G2 [OK]')
    ref = committed['results']['ridge']
    for key, label in (('100', 'ridge_base_ensemble'), ('ext', 'ridge_ext4.0_ensemble')):
        g.check(label, ra[key]['macro_auroc_ensemble'], ref[key]['macro_auroc_ensemble'], TOL_AUROC)
        for s, (a, b) in enumerate(zip(ra[key]['macro_auroc_per_seed'], ref[key]['macro_auroc_per_seed'])):
            g.check(f'{label}_seed{SEEDS[s]}', a, b, TOL_AUROC)
    # delta P0 + CI bootstrap theo cụm (tất định theo BOOT_SEED trong run_curve)
    cmp_ = rc.compare(ra['ext']['per_peptide'], ra['100']['per_peptide'], np.asarray(ra['groups0']))
    ref_cmp = committed['verdict']['ridge']['P0_delta_ext_minus_100']
    g.check('P0_delta_ext_minus_100', cmp_['delta'], ref_cmp['delta'], TOL_AUROC)
    g.check('P0_ci_low', cmp_['ci95'][0], ref_cmp['ci95'][0], TOL_CI)
    g.check('P0_ci_high', cmp_['ci95'][1], ref_cmp['ci95'][1], TOL_CI)
    res['gate_A'] = {k: {kk: vv for kk, vv in v.items() if kk != 'per_peptide'} if isinstance(v, dict) else v
                     for k, v in ra.items() if k != 'groups0'}
    res['gate_A']['P0_compare'] = cmp_

    # ---- Cổng B: nguyên mẫu predict.py khớp runner ----
    if run_verify:
        print('\nCổng B — calibration-p6/verify.py (predict.py khớp runner)')
        import verify
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                verify.main()
            ok = True
            err = None
        except BaseException as e:                      # noqa: BLE001 — ghi lại, không nuốt
            ok, err = False, ''.join(traceback.format_exception_only(type(e), e)).strip()
        print(buf.getvalue()[-1800:])
        rep = verify.report
        diffs = [v['max_abs_diff'] for v in rep.values() if isinstance(v, dict) and 'max_abs_diff' in v]
        mx = max(diffs) if diffs else float('nan')
        g.check('verify_max_abs_diff', mx if diffs else 1.0, 0.0, TOL_VERIFY, strict=False)
        res['gate_B'] = {'completed_without_assertion': ok, 'error': err, 'n_checks': len(diffs),
                         'max_abs_diff': mx, 'report': rep}
    else:
        res['gate_B'] = {'skipped': True}

    # ---- Tuỳ chọn: chạy lại nguyên run_curve.main() (ridge + gate_no_pap, ~10-20 phút CPU) ----
    if run_full_curve:
        print('\nTuỳ chọn — chạy lại toàn bộ run_curve.main() (thông tin, dung sai nới do khác phiên bản torch)')
        with contextlib.redirect_stdout(io.StringIO()):
            rc.main()
        new = json.loads((ctx.research / 'learning-curve-2026-10-22/results.json').read_text())
        for m in ('ridge', 'gate_no_pap'):
            for k in ('25', '50', '75', '100', 'ext'):
                tol = TOL_AUROC if m == 'ridge' else TOL_NEURAL_INFO
                g.check(f'full_{m}_{k}', new['results'][m][k]['macro_auroc_ensemble'],
                        committed['results'][m][k]['macro_auroc_ensemble'], tol, strict=(m == 'ridge'))
        res['full_curve'] = {m: {k: new['results'][m][k]['macro_auroc_ensemble']
                                 for k in new['results'][m]} for m in new['results']}

    res['all_gates_pass'] = bool(g.to_dict()['all_pass'])
    res['seconds'] = round(time.time() - t0, 1)
    res['versions'] = {'numpy': np.__version__}
    return res
