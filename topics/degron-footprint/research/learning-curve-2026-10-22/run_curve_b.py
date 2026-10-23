"""Phần B: tách "thêm cụm" khỏi "mở rộng phân bố". Tiêu chí ở PROTOCOL-B.md.

Phần cũ (cụm vùng PSI(WT) <= 3,0) luôn giữ 100%; chỉ thay đổi tỉ lệ cụm MỚI
(vùng 3,0-4,0) thêm vào train. Outer-test, fold, nhãn, mô hình, seed: y nguyên phần A.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/learning-curve-2026-10-22/run_curve_b.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib
from pathlib import Path
import numpy as np
import torch
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_curve as A   # dùng lại build/ridge/neural/compare, không chép lại

TOPIC = A.TOPIC
rd, dr = A.rd, A.dr
SEEDS = A.SEEDS
NEW_FRACTIONS = [0.25, 0.50, 0.75, 1.00]
BASE_MARGINAL = 0.0038   # giá trị biên 36 cụm vùng cũ, đo ở phần A (PROTOCOL-B §4)


def main():
    peps0, X0, y0, idx0, rowg0, groups0, psiwt0 = A.build(rd.DEGRON_PSI_MAX, 'base')
    pepsE, XE, yE, idxE, rowgE, groupsE, psiwtE = A.build(A.EXT_PSI_MAX, f'ext{A.EXT_PSI_MAX}')

    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'fold lệch G2 -> dừng'
    print('cổng tự kiểm: 5 fold trùng khớp folds của G2 [OK]', flush=True)

    new_peps = [p for p in pepsE if p not in set(peps0)]
    pos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[pos[p]]) for p in new_peps])

    Xc = np.vstack([X0, XE[new_rows]])
    yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]])
    base_n = len(y0)
    new_cluster_pool = sorted(set(rowgc[base_n:]))
    print(f'cụm mới khả dụng: {len(new_cluster_pool)}', flush=True)

    results = {}
    for model in ('ridge', 'gate_no_pap'):
        results[model] = {}
        for frac in NEW_FRACTIONS:
            key = f'new{int(frac * 100)}'
            per_seed, hyper = [], []
            for seed in SEEDS:
                out = np.full(base_n, np.nan)
                for fold, (_, te) in enumerate(folds):
                    test_clusters = set(fold_clusters[fold])
                    tr_base = np.array([i for i in range(base_n)
                                        if rowg0[i] not in test_clusters])
                    avail = [c for c in new_cluster_pool if c not in test_clusters]
                    rng = np.random.default_rng(seed * 1000 + fold)
                    order = rng.permutation(avail)
                    k = max(1, int(round(frac * len(order))))
                    chosen_new = set(order[:k])
                    extra = np.array([i for i in range(base_n, len(yc))
                                      if rowgc[i] in chosen_new], dtype=int)
                    pool = np.concatenate([tr_base, extra])
                    gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                    ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
                    train, val = pool[ti], pool[vi]
                    assert not (set(rowgc[train]) & test_clusters)
                    assert not (set(rowgc[val]) & test_clusters)
                    if model == 'ridge':
                        pred, hp = A.ridge(Xc, yc, train, val, te)
                    else:
                        pred, hp = A.neural(np.c_[Xc, np.zeros(len(yc))], yc,
                                            train, val, te, seed)
                    out[te] = pred
                    hyper.append({'seed': seed, 'fold': fold, 'epoch_or_alpha': hp,
                                  'n_new_clusters_added': len(chosen_new),
                                  'n_train_clusters': len(set(rowgc[pool])),
                                  'n_train_cells': int(len(pool))})
                assert not np.isnan(out).any()
                per_seed.append(out)
                print(f'  {model:12s} {key:>7s} seed {seed}: '
                      f'{A.macro(out, y0, idx0)[0]:.4f}', flush=True)
            ens = np.mean(per_seed, axis=0)
            results[model][key] = {
                'macro_auroc_ensemble': A.macro(ens, y0, idx0)[0],
                'macro_auroc_per_seed': [A.macro(s, y0, idx0)[0] for s in per_seed],
                'per_peptide': A.macro(ens, y0, idx0)[1],
                'mean_new_clusters_added': float(np.mean([h['n_new_clusters_added']
                                                          for h in hyper])),
                'hyper': hyper,
            }

    # --- B(0) = mức 100% của phần A, đọc lại không chạy lại ---
    a = json.loads((HERE / 'results.json').read_text())
    verdict = {}
    for model in results:
        b0_per_pep = a['results'][model]['100']['per_peptide']
        b0 = a['results'][model]['100']['macro_auroc_ensemble']
        r = results[model]
        gains = {k: r[k]['macro_auroc_ensemble'] - b0 for k in r}
        c50 = A.compare(r['new50']['per_peptide'], b0_per_pep, groups0)
        total = gains['new100']
        frac25 = (gains['new25'] / total) if total > 0 else None
        main_v = ('ủng hộ mở rộng phân bố' if c50['ci95'][0] > BASE_MARGINAL else
                  'có giá trị nhưng chưa hơn cụm vùng cũ' if c50['ci95'][0] > 0 else
                  'chưa đủ bằng chứng')
        shape_v = ('bão hòa sớm' if (frac25 is not None and frac25 >= 0.60)
                   else 'tỉ lệ theo số cụm')
        verdict[model] = {
            'B0_macro_auroc_from_part_A': b0,
            'curve': {k: r[k]['macro_auroc_ensemble'] for k in r},
            'gains_over_B0': gains,
            'mean_new_clusters_added': {k: r[k]['mean_new_clusters_added'] for k in r},
            'B50_minus_B0': c50,
            'base_marginal_reference': BASE_MARGINAL,
            'criterion_main': main_v,
            'fraction_of_total_gain_at_25pct': frac25,
            'criterion_shape': shape_v,
            'agree': main_v == 'ủng hộ mở rộng phân bố' and shape_v == 'bão hòa sớm',
        }
        print(f'\n{model}: B0={b0:.4f} -> ' +
              ' '.join(f'{k}={r[k]["macro_auroc_ensemble"]:.4f}' for k in r))
        print(f'  B(50%)−B(0) = {c50["delta"]:+.4f} CI={c50["ci95"]} '
              f'(mốc cụm vùng cũ {BASE_MARGINAL:+.4f}) -> {main_v}')
        print(f'  lợi ích tại 25% chiếm {frac25 if frac25 is None else round(frac25,3)} '
              f'tổng lợi ích -> {shape_v}', flush=True)

    out = {
        'protocol': 'PROTOCOL-B.md; phần cũ giữ 100%, chỉ thay tỉ lệ cụm MỚI; '
                    'outer-test = đúng ô của bộ 91 peptide G2; benchmark phát triển OOF',
        'seeds': SEEDS, 'new_fractions': NEW_FRACTIONS,
        'ext_degron_psi_max': A.EXT_PSI_MAX,
        'n_new_clusters_available': len(new_cluster_pool),
        'fold_check_matches_g2': True,
        'results': {m: {k: {kk: vv for kk, vv in v.items() if kk != 'per_peptide'}
                        for k, v in results[m].items()} for m in results},
        'verdict': verdict,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'versions': {'numpy': np.__version__, 'torch': torch.__version__},
    }
    (HERE / 'results-b.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f"\n-> {HERE / 'results-b.json'}")


if __name__ == '__main__':
    main()
