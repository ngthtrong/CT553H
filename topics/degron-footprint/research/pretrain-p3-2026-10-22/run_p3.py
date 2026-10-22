"""P3 — tiền huấn luyện nhãn tile (Voutsinos) rồi tinh chỉnh ΔPSI. Tiêu chí ở PROTOCOL.md.

Hai pha: (1) nền `ridge` + `rand` (khởi tạo ngẫu nhiên, hai lr) và cổng tái lập;
(2) tiền huấn luyện từng (fold, seed) rồi tinh chỉnh `pre` (hai lr). Có tiến độ lưu ở
data/processed/p3-progress.pkl nên chạy lại sẽ tiếp tục.

Chạy từ gốc repo (cần build_exclusion.py chạy trước):
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/pretrain-p3-2026-10-22/run_p3.py
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '2'
os.environ['OMP_NUM_THREADS'] = '2'
import sys, json, gzip, csv, hashlib, pickle, time, re
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(HERE))
import run_curve as rc                      # build, ridge, compare, Gate, macro
import residue_data as rd
import derisk as dr

torch.set_num_threads(4)
SEEDS = rc.SEEDS
LRS = [2e-3, 5e-4]
CONFIGS = [('ext', 4.0), ('base', 3.0)]    # (tên, ngưỡng); ext là cấu hình chính
PROG = TOPIC / 'data/processed/p3-progress.pkl'
MODELDIR = TOPIC / 'data/processed/p3-pretrained'
TILES = TOPIC / 'data/raw/voutsinos-2026/repo/score/degrons.csv.gz'
EXCL = TOPIC / 'data/processed/p3-tile-exclusion.json'
TILE_RE = re.compile(r'^(ENSG\d+)_tile(\d+)$')
PT_MAX_EPOCH, PT_PATIENCE, PT_BATCH, PT_LR = 10, 2, 256, 2e-3
OFFS = [o for o in range(-dr.WINDOW, dr.WINDOW + 1) if o != 0]


# ---------------------------------------------------------------- tiền huấn luyện
def tile_feats(A):
    """A: (B, L) long -> (B*L, 180) float32, chế độ chỉ-hoang-dã, đúng bố cục derisk.featurize."""
    B, L = A.shape
    oh = F.one_hot(A, 20).float()
    comp = oh.mean(1, keepdim=True).expand(-1, L, -1)
    w = dr.WINDOW
    pad = F.pad(oh, (0, 0, w, w))
    ctx = [pad[:, w + o:w + o + L, :] for o in OFFS]
    x = torch.cat([oh, torch.zeros_like(oh), comp] + ctx, -1)
    return x.reshape(B * L, -1)


def selftest_feats():
    """tile_feats phải khớp featurize (trừ khối mut) trên một chuỗi 28-mer bất kỳ."""
    rng = np.random.default_rng(0)
    seq = ''.join(rng.choice(list(rd.AAS), 28))
    rows = [(seq, p, 'A') for p in range(1, 29)]
    ref = dr.featurize(rows, {'pair', 'comp', 'ctx'})
    A = torch.tensor([[dr.AA2I[c] for c in seq]])
    mine = tile_feats(A).numpy()
    keep = np.r_[0:20, 40:180]
    assert np.allclose(ref[:, keep], mine[:, keep]), 'tile_feats khác featurize'
    assert np.allclose(mine[:, 20:40], 0)


def load_tiles():
    genes, aas, ys = [], [], []
    with gzip.open(TILES, 'rt', encoding='utf-8') as fh:
        csv.field_size_limit(10 ** 7)
        for r in csv.DictReader(fh):
            m = TILE_RE.match(r['name'])
            aa = r['aa']
            if not m or len(aa) != 30 or set(aa) - set(rd.AAS):
                continue
            genes.append(m.group(1)); aas.append([dr.AA2I[c] for c in aa])
            ys.append(-float(r['degron_score']))
    return np.array(genes), np.array(aas, dtype=np.int64), np.array(ys, dtype=np.float32)


def pretrain(seed, fold, genes, A, y, excluded_genes):
    """Tiền huấn luyện Gate trên tile của gene không bị loại. Trả (state, thống kê)."""
    keep = ~np.isin(genes, list(excluded_genes))
    g_keep = np.unique(genes[keep])
    rng = np.random.default_rng(seed * 7919 + fold)
    val_genes = set(rng.choice(g_keep, max(1, len(g_keep) // 10), replace=False))
    is_val = np.array([g in val_genes for g in genes]) & keep
    tr = np.where(keep & ~is_val)[0]; va = np.where(is_val)[0]
    assert not (set(genes[tr]) & set(excluded_genes)) and not (set(genes[va]) & set(excluded_genes))
    mu, sd = float(y[tr].mean()), float(y[tr].std())
    yz = torch.tensor((y - mu) / sd)
    At = torch.tensor(A)
    torch.manual_seed(seed)
    net = rc.Gate(gated=True, pap=False)
    w0 = {k: v.detach().clone() for k, v in net.state_dict().items()}
    opt = torch.optim.AdamW(net.parameters(), lr=PT_LR, weight_decay=.01)

    def predict(ids):
        out = []
        net.eval()
        with torch.no_grad():
            for b in np.array_split(ids, max(1, len(ids) // 2048)):
                out.append(net(tile_feats(At[b])).reshape(len(b), -1).mean(1))
        return torch.cat(out)

    best, state, eb = 1e99, None, 0
    brng = np.random.default_rng(seed * 104729 + fold)
    for epoch in range(1, PT_MAX_EPOCH + 1):
        net.train()
        for b in np.array_split(brng.permutation(tr), max(1, len(tr) // PT_BATCH)):
            pred = net(tile_feats(At[b])).reshape(len(b), -1).mean(1)
            loss = ((pred - yz[b]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        v = float(((predict(va) - yz[va]) ** 2).mean())
        if v < best - 1e-6:
            best, eb = v, epoch
            state = {k: t.detach().clone() for k, t in net.state_dict().items()}
        if epoch - eb >= PT_PATIENCE:
            break
    net.load_state_dict(state)
    pv = predict(va).numpy()
    pear = float(np.corrcoef(pv, yz[va].numpy())[0, 1])
    # cột mut của lớp pair không nhận gradient -> khôi phục về khởi tạo của seed
    state['pair.weight'][:, 20:40] = w0['pair.weight'][:, 20:40]
    stats = {'seed': seed, 'fold': fold, 'n_tiles_train': int(len(tr)), 'n_tiles_val': int(len(va)),
             'n_genes_excluded': len(excluded_genes), 'n_tiles_excluded': int((~keep).sum()),
             'best_epoch': eb, 'epochs_run': epoch, 'val_mse_z': best, 'val_pearson': pear}
    return state, stats


# ---------------------------------------------------------------- tinh chỉnh
def finetune(xx, yy, tr, va, te, seed, lr, init_state=None):
    """Đúng rc.neural, thêm lr và trạng thái đầu; trả (dự đoán, epoch tốt nhất, MSE val tốt nhất)."""
    torch.manual_seed(seed)
    net = rc.Gate(gated=True, pap=False)
    if init_state is not None:
        net.load_state_dict(init_state)
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=.01)
    rng = np.random.default_rng(seed)
    best, state, eb = 1e99, None, 0
    for epoch in range(1, 61):
        net.train()
        for batch in np.array_split(rng.permutation(tr), max(1, len(tr) // 1024)):
            loss = ((net(xx[batch]) - yy[batch]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad():
            v = float(((net(xx[va]) - yy[va]) ** 2).mean())
        if v < best - 1e-6:
            best, eb = v, epoch
            state = {k: t.detach().clone() for k, t in net.state_dict().items()}
        if epoch - eb >= 8:
            break
    net.load_state_dict(state); net.eval()
    with torch.no_grad():
        return net(xx[te]).numpy(), eb, best


def main():
    t0 = time.time()
    selftest_feats()
    print('selftest tile_feats == featurize [OK]', flush=True)

    # ---- bộ gốc + bộ nới (giống run_curve) ----
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    folds = list(GroupKFold(5).split(X0, y0, rowg0))
    fold_clusters = [sorted(set(rowg0[te])) for _, te in folds]
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    assert fold_clusters == [f['test_clusters'] for f in g2['folds']], 'folds khác G2'
    print('cổng 1: folds trùng G2 [OK]', flush=True)
    pepsE, XE, yE, idxE, rowgE, groupsE, _ = rc.build(4.0, 'ext4.0')
    new_peps = [p for p in pepsE if p not in set(peps0)]
    npos = {p: i for i, p in enumerate(pepsE)}
    new_rows = np.concatenate([np.arange(*idxE[npos[p]]) for p in new_peps])
    Xc = np.vstack([X0, XE[new_rows]]); yc = np.concatenate([y0, yE[new_rows]])
    rowgc = np.concatenate([rowg0, rowgE[new_rows]]); base_n = len(y0)
    xx = torch.tensor(np.c_[Xc, np.zeros(len(yc))], dtype=torch.float32)
    yy = torch.tensor(yc, dtype=torch.float32)

    def pool_split(cfg, fold, seed):
        test_clusters = set(fold_clusters[fold])
        tr_base = np.array([i for i in range(base_n) if rowg0[i] not in test_clusters])
        pool = tr_base
        if cfg == 'ext':
            extra = np.array([i for i in range(base_n, len(yc))
                              if rowgc[i] not in test_clusters], dtype=int)
            pool = np.concatenate([tr_base, extra])
        gsp = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=seed)
        ti, vi = next(gsp.split(pool, yc[pool], rowgc[pool]))
        train, val = pool[ti], pool[vi]
        assert not (set(rowgc[train]) & test_clusters) and not (set(rowgc[val]) & test_clusters)
        return train, val, folds[fold][1]

    prog = pickle.loads(PROG.read_bytes()) if PROG.exists() else {}

    def save():
        PROG.write_bytes(pickle.dumps(prog))

    # ---- pha 1: ridge + rand ----
    for seed in SEEDS:
        for fold in range(5):
            for cfg, _ in CONFIGS:
                train, val, te = pool_split(cfg, fold, seed)
                k = ('ridge', cfg, seed, fold)
                if k not in prog:
                    pred, a = rc.ridge(Xc, yc, train, val, te)
                    prog[k] = (pred, a, 0.0)
                for lr in LRS:
                    k = ('rand', cfg, seed, fold, lr)
                    if k not in prog:
                        prog[k] = finetune(xx, yy, train, val, te, seed, lr)
            save()
            print(f'  pha 1 seed {seed} fold {fold} xong ({time.time() - t0:.0f}s)', flush=True)

    def assemble(arm, cfg, seed, lr=None):
        out = np.full(base_n, np.nan)
        for fold in range(5):
            te = folds[fold][1]
            if arm == 'ridge':
                out[te] = prog[('ridge', cfg, seed, fold)][0]
            elif lr is not None:
                out[te] = prog[(arm, cfg, seed, fold, lr)][0]
            else:        # chọn lr theo MSE val trong
                cand = [prog[(arm, cfg, seed, fold, l)] for l in LRS]
                out[te] = min(cand, key=lambda c: c[2])[0]
        assert not np.isnan(out).any()
        return out

    # ---- cổng 2: tái lập 0,8082/0,8015 (base) và 0,8208/0,8154 (ext) ----
    lc = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())['results']
    gate = {}
    for cfg, ref_key in (('base', '100'), ('ext', 'ext')):
        r_ens = np.mean([assemble('ridge', cfg, s) for s in SEEDS], axis=0)
        n_ens = np.mean([assemble('rand', cfg, s, lr=2e-3) for s in SEEDS], axis=0)
        got = {'ridge': rc.macro(r_ens, y0, idx0)[0], 'gate_no_pap': rc.macro(n_ens, y0, idx0)[0]}
        ref = {'ridge': lc['ridge'][ref_key]['macro_auroc_ensemble'],
               'gate_no_pap': lc['gate_no_pap'][ref_key]['macro_auroc_ensemble']}
        gate[cfg] = {'got': got, 'ref': ref}
        print(f'cổng 2 [{cfg}]: ridge {got["ridge"]:.4f} (ref {ref["ridge"]:.4f}) · '
              f'rand lr2e-3 {got["gate_no_pap"]:.4f} (ref {ref["gate_no_pap"]:.4f})', flush=True)
        for m in got:
            assert abs(got[m] - ref[m]) <= 5e-4, f'cổng tái lập trượt: {cfg} {m}'
    print('cổng 2: tái lập [OK]', flush=True)

    # ---- pha 2: tiền huấn luyện + tinh chỉnh ----
    genes, A, ytile = load_tiles()
    ex = json.loads(EXCL.read_text())
    tcl = ex['target_cluster']
    hits = {}
    for rule in ('mmseqs', 'kmer', 'gene_name'):
        for g, accs in ex['hits'][rule].items():
            hits.setdefault(g, set()).update(accs)
    print(f'tile giữ lại: {len(ytile)} / {len(set(genes))} gene', flush=True)
    MODELDIR.mkdir(exist_ok=True)
    pt_stats, excl_stats = [], []
    for seed in SEEDS:
        for fold in range(5):
            test_cl = set(fold_clusters[fold])
            excluded = {g for g, accs in hits.items() if any(tcl[a] in test_cl for a in accs)}
            kpre = ('pretrain', seed, fold)
            if kpre not in prog:
                state, st = pretrain(seed, fold, genes, A, ytile, excluded)
                torch.save(state, MODELDIR / f'p3-pre-seed{seed}-fold{fold}.pt')
                prog[kpre] = st
                save()
            else:
                state = torch.load(MODELDIR / f'p3-pre-seed{seed}-fold{fold}.pt')
            st = prog[kpre]
            print(f'  pretrain seed {seed} fold {fold}: loại {st["n_genes_excluded"]} gene/'
                  f'{st["n_tiles_excluded"]} tile; train {st["n_tiles_train"]}; epoch {st["best_epoch"]}; '
                  f'Pearson val {st["val_pearson"]:.3f} ({time.time() - t0:.0f}s)', flush=True)
            for cfg, _ in CONFIGS:
                train, val, te = pool_split(cfg, fold, seed)
                for lr in LRS:
                    k = ('pre', cfg, seed, fold, lr)
                    if k not in prog:
                        prog[k] = finetune(xx, yy, train, val, te, seed, lr, init_state=state)
            save()

    # ---- tiêu chí PROTOCOL §6 ----
    results, verdict = {}, {}
    for cfg, _ in CONFIGS:
        results[cfg] = {}
        per_seed_scores = {}
        for arm in ('ridge', 'rand', 'pre'):
            per_seed_scores[arm] = [assemble(arm, cfg, s) for s in SEEDS]
            ens = np.mean(per_seed_scores[arm], axis=0)
            hyper = [{'seed': s, 'fold': f,
                      'lr': (None if arm == 'ridge' else min(
                          LRS, key=lambda l: prog[(arm, cfg, s, f, l)][2])),
                      'epoch_or_alpha': (prog[('ridge', cfg, s, f)][1] if arm == 'ridge' else
                                         min((prog[(arm, cfg, s, f, l)] for l in LRS),
                                             key=lambda c: c[2])[1])}
                     for s in SEEDS for f in range(5)]
            results[cfg][arm] = {
                'macro_auroc_ensemble': rc.macro(ens, y0, idx0)[0],
                'macro_auroc_per_seed': [rc.macro(s, y0, idx0)[0] for s in per_seed_scores[arm]],
                'per_peptide': rc.macro(ens, y0, idx0)[1], 'hyper': hyper}
            if arm != 'ridge':
                results[cfg][arm]['macro_auroc_per_lr_fixed'] = {
                    str(lr): rc.macro(np.mean([assemble(arm, cfg, s, lr=lr) for s in SEEDS], axis=0),
                                      y0, idx0)[0] for lr in LRS}
        v = {}
        for name, a, b in (('A_pre_minus_rand', 'pre', 'rand'), ('B_pre_minus_ridge', 'pre', 'ridge')):
            c = rc.compare(results[cfg][a]['per_peptide'], results[cfg][b]['per_peptide'], groups0)
            per_seed = [rc.compare(rc.macro(per_seed_scores[a][i], y0, idx0)[1],
                                   rc.macro(per_seed_scores[b][i], y0, idx0)[1], groups0)['delta']
                        for i in range(len(SEEDS))]
            v[name] = {'delta': c['delta'], 'ci95': c['ci95'], 'delta_per_seed': per_seed,
                       'criterion_ci_above_zero': bool(c['ci95'][0] > 0),
                       'criterion_all_seeds_positive': bool(all(d > 0 for d in per_seed)),
                       'passes': bool(c['ci95'][0] > 0 and all(d > 0 for d in per_seed))}
        A_ok, B_ok = v['A_pre_minus_rand']['passes'], v['B_pre_minus_ridge']['passes']
        v['conclusion'] = ('Nhận' if A_ok and B_ok else
                           'Giúp mạng nhưng chưa vượt M3' if A_ok else
                           'Chưa đủ bằng chứng cho lợi ích của tiền huấn luyện')
        verdict[cfg] = v
        print(f'\n[{cfg}] ridge {results[cfg]["ridge"]["macro_auroc_ensemble"]:.4f} · '
              f'rand {results[cfg]["rand"]["macro_auroc_ensemble"]:.4f} · '
              f'pre {results[cfg]["pre"]["macro_auroc_ensemble"]:.4f}')
        for n in ('A_pre_minus_rand', 'B_pre_minus_ridge'):
            print(f'  {n}: {v[n]["delta"]:+.4f} CI {v[n]["ci95"]} seeds {v[n]["delta_per_seed"]} '
                  f'-> {"đạt" if v[n]["passes"] else "không đạt"}')
        print(f'  => {v["conclusion"]}', flush=True)

    out = {
        'protocol': 'PROTOCOL.md 22/10/2026; benchmark phát triển OOF; outer-test = 91 peptide gốc',
        'seeds': SEEDS, 'lr_grid': LRS, 'primary_config': 'ext (ngưỡng 4,0)',
        'pretrain': {'max_epoch': PT_MAX_EPOCH, 'patience': PT_PATIENCE, 'batch_tiles': PT_BATCH,
                     'lr': PT_LR, 'target': '-degron_score (z-score trên tập tiền huấn luyện)'},
        'reproduction_gate': gate,
        'pretrain_stats': [prog[('pretrain', s, f)] for s in SEEDS for f in range(5)],
        'results': results, 'verdict': verdict,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'python': sys.version},
        'wall_seconds': time.time() - t0,
    }
    (HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f'\n-> {HERE / "results.json"}  ({time.time() - t0:.0f}s)')


if __name__ == '__main__':
    main()
