"""Lợi ích P0 (ridge M3, nới ngưỡng 4,0) qua 7 mức phân hoạch protein.

Tiêu chí chốt trước ở PROTOCOL.md. Tái dùng build/ridge/compare/macro của
learning-curve-2026-10-22/run_curve.py. Outer-test luôn là 47.847 ô của 91 peptide gốc;
fold = GroupKFold(5) theo nhóm của MỨC đang xét.

Chạy từ gốc repo (sau cluster.py):
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/recluster-sensitivity-2026-10-22/run.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, hashlib
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
import run_curve as A

rd = A.rd
SEEDS = A.SEEDS
EXT = A.EXT_PSI_MAX
RECLUSTER = TOPIC / 'data/interim/recluster-sensitivity'
GATE_BASE, GATE_EXT, GATE_TOL = 0.8082, 0.8208, 1e-4
LEVELS = {                       # mã -> (mô tả, tệp tsv hoặc None)
    'L0': ('accession (không phân cụm)', None),
    'L1': ('id 0,3 · cov 0,8 (tham chiếu)', rd.CLUSTER_TSV),
    'L2': ('id 0,3 · cov 0,5', TOPIC / 'data/interim/protein-id30-cov50_cluster.tsv'),
    'L3': ('id 0,2 · cov 0,5', RECLUSTER / 'protein-id20-cov50_cluster.tsv'),
    'L4': ('id 0,1 · cov 0,5', RECLUSTER / 'protein-id10-cov50_cluster.tsv'),
    'L5': ('id 0,1 · cov 0,3', RECLUSTER / 'protein-id10-cov30_cluster.tsv'),
    'L6': ('id 0,0 · cov 0,3', RECLUSTER / 'protein-id00-cov30_cluster.tsv'),
}


def load_map(tsv):
    if tsv is None:
        return {}
    rep = {}
    with Path(tsv).open(encoding='utf-8') as fh:
        for line in fh:
            r, m = line.rstrip('\n').split('\t')[:2]
            rep[m] = r
    return rep


def run_level(code, cmap, peps0, X0, y0, idx0, pepsN, XN, yN, idxN):
    grp = lambda p: cmap.get(rd.accession(p), rd.accession(p))   # noqa: E731
    g0 = np.array([grp(p) for p in peps0])
    gN = np.array([grp(p) for p in pepsN])
    rowg0 = np.concatenate([np.repeat(g0[i], b - a) for i, (a, b) in enumerate(idx0)])
    rowgN = np.concatenate([np.repeat(gN[i], b - a) for i, (a, b) in enumerate(idxN)])
    base_n = len(y0)
    Xc, yc = np.vstack([X0, XN]), np.concatenate([y0, yN])
    rowgc = np.concatenate([rowg0, rowgN])
    ext_rows = np.arange(base_n, len(yc))

    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]

    leak = {}
    for f, (_, te) in enumerate(folds):
        tg = set(fold_clusters[f])
        mask = np.array([rowgc[i] in tg for i in ext_rows])
        pep_hit = [p for p, g in zip(pepsN, gN) if g in tg]
        leak[f'fold{f}'] = {'ext_cells_excluded': int(mask.sum()),
                            'ext_cells_total': int(len(ext_rows)),
                            'ext_peptides_excluded': len(pep_hit)}
    frac = float(np.mean([v['ext_cells_excluded'] / v['ext_cells_total'] for v in leak.values()]))

    arms = {}
    for arm in ('base', 'ext'):
        scores, hyper = [], []
        for seed in SEEDS:
            out = np.full(base_n, np.nan)
            for f, (_, te) in enumerate(folds):
                tg = set(fold_clusters[f])
                tr_base = np.array([i for i in range(base_n) if rowg0[i] not in tg])
                if arm == 'ext':
                    extra = np.array([i for i in ext_rows if rowgc[i] not in tg], dtype=int)
                    pool = np.concatenate([tr_base, extra])
                else:
                    pool = tr_base
                gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
                ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
                train, val = pool[ti], pool[vi]
                assert not (set(rowgc[train]) & tg) and not (set(rowgc[val]) & tg)
                pred, alpha = A.ridge(Xc, yc, train, val, te)
                out[te] = pred
                hyper.append({'seed': seed, 'fold': f, 'alpha': alpha,
                              'n_train_cells': int(len(pool)),
                              'n_train_groups': int(len(set(rowgc[pool])))})
            assert not np.isnan(out).any()
            scores.append(out)
        ens = np.mean(scores, axis=0)
        arms[arm] = {'ens': A.macro(ens, y0, idx0), 'seed_scores': scores, 'hyper': hyper}
        print(f'  {code} {arm:4s} ens={arms[arm]["ens"][0]:.4f} '
              f'seeds={[round(A.macro(s, y0, idx0)[0], 4) for s in scores]}', flush=True)

    cmp = A.compare(arms['ext']['ens'][1], arms['base']['ens'][1], g0)
    per_seed = [A.compare(A.macro(arms['ext']['seed_scores'][i], y0, idx0)[1],
                          A.macro(arms['base']['seed_scores'][i], y0, idx0)[1], g0)['delta']
                for i in range(len(SEEDS))]
    all_pep = list(peps0) + list(pepsN)
    all_g = list(g0) + list(gN)
    partition = frozenset(frozenset(p for p, g in zip(all_pep, all_g) if g == c) for c in set(all_g))
    shared = sum(1 for g in gN if g in set(g0))
    return {
        'n_groups_base': int(len(set(g0))), 'n_groups_union': int(len(set(all_g))),
        'macro_auroc_base': arms['base']['ens'][0], 'macro_auroc_ext': arms['ext']['ens'][0],
        'delta': cmp, 'delta_per_seed': per_seed,
        'ext_peptides_sharing_group_with_a_base_peptide': int(shared),
        'leak_per_fold': leak, 'ext_cells_excluded_fraction_mean': frac,
        'informative': bool(frac < .5),
        'fold_clusters': fold_clusters,
        'hyper_alpha': {a: [h['alpha'] for h in arms[a]['hyper']] for a in arms},
    }, partition


def main():
    peps0, X0, y0, idx0, *_ = A.build(rd.DEGRON_PSI_MAX, 'base')
    pepsE, XE, yE, idxE, *_ = A.build(EXT, f'ext{EXT}')
    base_set = set(peps0)
    pos = {p: i for i, p in enumerate(pepsE)}
    new = [p for p in pepsE if p not in base_set]
    rowsN = np.concatenate([np.arange(*idxE[pos[p]]) for p in new])
    XN, yN = XE[rowsN], yE[rowsN]
    idxN, off = [], 0
    for p in new:
        n = idxE[pos[p]][1] - idxE[pos[p]][0]
        idxN.append((off, off + n)); off += n
    idxN = np.asarray(idxN)
    # idxN tính theo chỉ số trong XN; run_level cần chỉ số tương đối của mảng ext
    print(f'base {len(peps0)} peptide / {len(y0)} ô; ext thêm {len(new)} peptide / {len(yN)} ô', flush=True)

    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    g2_clusters = [f['test_clusters'] for f in g2['folds']]

    results, partitions = {}, {}
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else None     # chỉ để thử nhanh; không ghi results.json
    for code, (desc, tsv) in LEVELS.items():
        if only and code not in only:
            continue
        if tsv is not None and not Path(tsv).exists():
            raise SystemExit(f'thiếu {tsv}; chạy cluster.py trước')
        print(f'\n== {code}: {desc}', flush=True)
        r, part = run_level(code, load_map(tsv), peps0, X0, y0, idx0, new, XN, yN, idxN)
        r['description'] = desc
        results[code], partitions[code] = r, part
        print(f'  nhóm base/union = {r["n_groups_base"]}/{r["n_groups_union"]} · '
              f'delta {r["delta"]["delta"]:+.4f} CI {[round(x, 4) for x in r["delta"]["ci95"]]} '
              f'per-seed {[round(d, 4) for d in r["delta_per_seed"]]} · '
              f'loại {r["ext_cells_excluded_fraction_mean"]:.1%} ô ext', flush=True)
        if code == 'L1':                    # cổng tự kiểm
            ok_fold = r['fold_clusters'] == g2_clusters
            ok_base = abs(r['macro_auroc_base'] - GATE_BASE) <= GATE_TOL
            ok_ext = abs(r['macro_auroc_ext'] - GATE_EXT) <= GATE_TOL
            print(f'  cổng L1: fold={ok_fold} base={ok_base} ext={ok_ext}', flush=True)
            if not (ok_fold and ok_base and ok_ext):
                raise SystemExit('cổng tự kiểm L1 KHÔNG đạt -> dừng theo PROTOCOL §4')

    if only:
        return
    ref = partitions['L1']
    for code, r in results.items():
        r['identical_to_L1_on_176_peptides'] = bool(partitions[code] == ref)

    # ---- tiêu chí PROTOCOL §5 ----
    real = [c for c, r in results.items() if c != 'L1' and not r['identical_to_L1_on_176_peptides']]
    judged = [c for c in real if results[c]['informative']]
    def ok(c):
        r = results[c]
        return bool(r['delta']['ci95'][0] > 0 and all(d > 0 for d in r['delta_per_seed']))
    fails = [c for c in judged if not ok(c)]
    if not judged:
        verdict = 'không có mức khác thật và còn thông tin để kết luận'
    elif not fails:
        verdict = 'Lợi ích P0 bền theo độ mịn'
    elif len(fails) == len(judged):
        verdict = 'Không bền'
    else:
        verdict = 'Bền một phần'
    summary = {'levels_different_from_L1': real,
               'levels_different_and_informative': judged,
               'levels_failing': fails,
               'levels_passing': [c for c in judged if c not in fails],
               'levels_uninformative': [c for c in real if c not in judged],
               'verdict': verdict}
    print('\nKẾT LUẬN theo PROTOCOL §5:', verdict, summary, flush=True)

    out = {
        'protocol': 'PROTOCOL.md 22/10/2026; ridge M3; benchmark phát triển OOF, không phải kiểm chứng ngoài',
        'seeds': SEEDS, 'ext_degron_psi_max': EXT, 'rescue_delta': rd.RESCUE_DELTA,
        'n_boot': A.N_BOOT, 'boot_seed': A.BOOT_SEED,
        'n_base_peptides': len(peps0), 'n_ext_new_peptides': len(new),
        'gate': {'base': GATE_BASE, 'ext': GATE_EXT, 'tol': GATE_TOL},
        'levels': results, 'summary': summary,
        'cluster_manifest': json.loads((HERE / 'cluster-manifest.json').read_text()),
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print('->', HERE / 'results.json')


if __name__ == '__main__':
    main()
