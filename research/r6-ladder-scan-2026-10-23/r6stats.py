"""R6 — thống kê: AUROC macro, so sánh ghép cặp theo cụm (bootstrap), CI hiệu chỉnh Bonferroni, quy tắc kết luận.

`compare` lặp đúng vòng bootstrap của `run_curve.compare` (cùng seed 20261022, cùng thứ tự rút cụm), nên với m=1
cho đúng CI 95% của R1/R2/P0.
"""
import numpy as np

import r6data as r6          # noqa: F401  (nạp sys.path của derisk, run_curve)
import derisk as dr

N_BOOT = 5000
BOOT_SEED = 20261022
EQUIV_MARGIN = 0.01          # biên "tương đương" chỉ để MÔ TẢ (PROTOCOL §6)


def summarize_oof(oof, y0, idx0):
    """oof: {seed: điểm OOF [base_n]} -> macro AUROC từng seed + ensemble + per-peptide."""
    seeds = sorted(oof)
    per_seed = {s: dr.macro_auroc(oof[s], y0, idx0) for s in seeds}
    ens = np.mean([oof[s] for s in seeds], axis=0)
    em, epp = dr.macro_auroc(ens, y0, idx0)
    return {'seeds': seeds,
            'macro_auroc_per_seed': {str(s): per_seed[s][0] for s in seeds},
            'macro_auroc_ensemble': em, 'per_peptide_ensemble': epp,
            '_per_seed_pp': {s: per_seed[s][1] for s in seeds}}


def compare(per_a, per_b, groups, m=1, n_boot=N_BOOT, seed=BOOT_SEED):
    """Δ = A − B ghép cặp theo peptide, bootstrap theo CỤM. m = số phép so trong họ (Bonferroni: CI 1−0,05/m)."""
    keep = [i for i in range(len(per_a)) if per_a[i] is not None and per_b[i] is not None]
    delta = np.array([per_a[i] - per_b[i] for i in keep])
    g = np.asarray(groups)[keep]
    u = sorted(set(g))
    by = {c: delta[g == c] for c in u}
    rng = np.random.default_rng(seed)
    boot = [float(np.mean(np.concatenate([by[c] for c in rng.choice(u, len(u), replace=True)])))
            for _ in range(n_boot)]
    q95 = np.quantile(boot, [.025, .975]).tolist()
    qadj = np.quantile(boot, [.025 / m, 1 - .025 / m]).tolist() if m > 1 else q95
    return {'delta': float(delta.mean()), 'ci95': q95, 'ci_adj': qadj, 'm': m,
            'n_peptides': len(keep), 'n_clusters': len(u)}


def seed_deltas(sum_a, sum_b):
    return {str(s): float(np.mean([a - b for a, b in zip(sum_a['_per_seed_pp'][s], sum_b['_per_seed_pp'][s])
                                   if a is not None and b is not None]))
            for s in sum_a['seeds']}


def contrast(sum_a, sum_b, groups, m=1):
    """Một phép so đầy đủ: ensemble, từng seed, CI, kết luận theo PROTOCOL §6."""
    c = compare(sum_a['per_peptide_ensemble'], sum_b['per_peptide_ensemble'], groups, m=m)
    sd = seed_deltas(sum_a, sum_b)
    c['seed_deltas'] = sd
    c['verdict'] = verdict(c['ci_adj'], list(sd.values()))
    c['equivalent_within_0.01'] = bool(c['ci95'][0] > -EQUIV_MARGIN and c['ci95'][1] < EQUIV_MARGIN)
    return c


def verdict(ci, deltas):
    """PROTOCOL §6. ci: CI dùng để kết luận (đã hiệu chỉnh nếu thuộc họ nhiều phép)."""
    if ci[0] > 0 and len(deltas) == 3 and all(d > 0 for d in deltas):
        return 'nhận'
    if ci[1] < 0:
        return 'âm'
    if ci[0] > 0:
        return 'lợi ích chưa bền qua seed'
    return 'chưa đủ bằng chứng (CI phủ 0)'
