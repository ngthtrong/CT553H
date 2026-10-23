#!/usr/bin/env python3
"""THĂM DÒ (không tiền đăng ký) — chiều ngược lại: học trên bão hòa, chấm trên peptide quét.

Nếu nhãn quét không giúp huấn luyện (run_merge.py), nó vẫn có thể là tập CHẤM điểm lớn: ~2.700 cụm
cov80 không chạm cụm bão hòa nào, so với 89–172 cụm của benchmark hiện tại. Script này đo:

  * ridge M3 học trên TOÀN BỘ bão hòa ext4.0 (176 peptide) -> AUROC trên peptide quét ở cụm rời;
  * cùng mô hình học NGAY TRÊN bộ quét (CV theo cụm, cùng tập peptide) làm mốc "cùng miền";
  * ridge M0 (chỉ thành phần) học trên bão hòa, để thấy ngữ cảnh ±3 có chuyển sang quét không.

Chỉ đo, không chọn gì dựa trên kết quả này. Mọi số mang nhãn "thăm dò".

  .venv/bin/python -I topics/degron-footprint/research/scan-sat-merge-2026-10-23/sat_to_scan_eval.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
import sys, json
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_merge as rm            # noqa: E402  (nạp rd, dr, rc, suff, solve_plain, lin, load_scan)
rd, dr, rc = rm.rd, rm.dr, rm.rc

ALPHAS = rm.ALPHAS
SEEDS = rm.SEEDS


def fit_alpha_cv(X, y, g, seed=17):
    """alpha theo MSE trên một lần chia nhóm 20%."""
    tr, va = next(GroupShuffleSplit(1, test_size=.2, random_state=seed).split(X, y, g))
    T, r = rm.suff(X[tr], y[tr])
    return min((rm.mse(rm.lin(rm.solve_plain(T, r, a), X[va]), y[va]), a) for a in ALPHAS)[1]


def per_peptide_auroc(scores, y, bounds):
    return [dr.auroc(scores[a:b], y[a:b] >= rd.RESCUE_DELTA) for a, b in bounds]


def boot(per, groups, n=5000, seed=20261023):
    ok = [i for i, v in enumerate(per) if v is not None]
    v = np.array([per[i] for i in ok]); g = np.asarray(groups)[ok]
    u = sorted(set(g)); idx = {c: np.where(g == c)[0] for c in u}
    rng = np.random.default_rng(seed)
    means = [float(np.concatenate([v[idx[c]] for c in rng.choice(u, len(u))]).mean()) for _ in range(n)]
    return {'mean': float(v.mean()), 'ci95': np.quantile(means, [.025, .975]).tolist(),
            'n_peptides': len(ok), 'n_clusters': len(u)}


def paired(per_a, per_b, groups):
    ok = [i for i in range(len(per_a)) if per_a[i] is not None and per_b[i] is not None]
    return rc.compare([per_a[i] for i in ok], [per_b[i] for i in ok], [groups[i] for i in ok])


def main():
    rep = rd.load_clusters()
    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(rm.EXT_PSI, f'ext{rm.EXT_PSI}')
    sat_clusters = set(rowgE)
    out = {'note': 'THĂM DÒ, không tiền đăng ký. Học trên toàn bộ bão hòa ext4.0 (176 peptide), chấm trên peptide quét '
                   'có cụm cov80 không thuộc bất kỳ cụm bão hòa ext4.0 nào. Nhãn quét: rep1, reads>=10, ΔPSI so với mut0.',
           'n_sat_train_peptides': len(pepsE), 'n_sat_train_clusters': len(sat_clusters), 'by_threshold': {}}

    for thr in (3.0, 4.0):
        sc = rm.load_scan(thr, rep)
        grp_pep = np.array([rep.get(rd.accession(p), rd.accession(p)) for p in sc['peps']])
        disjoint_pep = np.array([g not in sat_clusters for g in grp_pep])
        keep_rows = disjoint_pep[sc['pep_of_row']]
        Xs, ys = sc['X'][keep_rows], sc['y'][keep_rows]
        pep_of_row = sc['pep_of_row'][keep_rows]
        # chỉ mục peptide mới (liên tục sau khi lọc)
        uniq, start = np.unique(pep_of_row, return_index=True)
        bounds = [(s, e) for s, e in zip(start, list(start[1:]) + [len(pep_of_row)])]
        groups = [grp_pep[u] for u in uniq]
        block = {'n_scan_peptides_disjoint': len(uniq), 'n_cells': int(len(ys)),
                 'n_clusters': len(set(groups)), 'pos_rate': float(np.mean(ys >= rd.RESCUE_DELTA))}

        # --- (1) bão hòa -> quét ---
        for name, cols in (('M3_sat_to_scan', slice(0, 180)), ('M0_sat_to_scan', slice(0, 60))):
            a = fit_alpha_cv(XE[:, cols], yE, rowgE)
            T, r = rm.suff(XE[:, cols], yE)
            th = rm.solve_plain(T, r, a)
            s = rm.lin(th, Xs[:, cols])
            per = per_peptide_auroc(s, ys, bounds)
            block[name] = {**boot(per, groups), 'alpha': a}
            block[f'_per_{name}'] = per

        # --- (2) mốc cùng miền: M3 học trên quét, CV 5 fold theo cụm, cùng tập peptide ---
        g_rows = np.array([groups[np.searchsorted(uniq, p)] for p in pep_of_row])
        scores = np.full(len(ys), np.nan)
        for tr, te in GroupKFold(5).split(Xs, ys, g_rows):
            a = fit_alpha_cv(Xs[tr][:, :180], ys[tr], g_rows[tr])
            T, r = rm.suff(Xs[tr][:, :180], ys[tr])
            scores[te] = rm.lin(rm.solve_plain(T, r, a), Xs[te][:, :180])
        per_in = per_peptide_auroc(scores, ys, bounds)
        block['M3_scan_cv_same_peptides'] = boot(per_in, groups)
        block['_per_scan_cv'] = per_in

        # --- so sánh ghép cặp ---
        c1 = paired(block['_per_M3_sat_to_scan'], block['_per_M0_sat_to_scan'], groups)
        c2 = paired(block['_per_scan_cv'], block['_per_M3_sat_to_scan'], groups)
        block['paired_M3_minus_M0_both_trained_on_sat'] = {'delta': c1['delta'], 'ci95': c1['ci95']}
        block['paired_scanCV_minus_sat_to_scan'] = {'delta': c2['delta'], 'ci95': c2['ci95']}
        for k in [k for k in block if k.startswith('_per_')]:
            del block[k]
        out['by_threshold'][f'scan_psi_wt_le_{thr}'] = block
        print(thr, json.dumps({k: (v if not isinstance(v, dict) else {kk: (round(vv, 4) if isinstance(vv, float) else vv)
                                                                      for kk, vv in v.items() if kk != 'ci95'})
                               for k, v in block.items()}, indent=1), flush=True)

    (HERE / 'results-sat-to-scan.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
