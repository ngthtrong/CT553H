"""R2 — đặc trưng ESM-2 đóng băng cộng vào ridge M3.

Hai giai đoạn (PROTOCOL §3–§5):
  1. `extract_features`  (GPU): Δ embedding mutant − WT cho 92.337 ô → F[92337, 2·d] float16, lưu cache;
  2. `fit_all` + `summarize` (CPU): PCA(64) khớp chỉ trên outer-train từng fold, ridge trên M3 ∪ PCA,
     so ghép cặp theo cụm với ridge M3 (cùng chia train/val), 3 seed, bootstrap 5.000 lần theo cụm.
Notebook chỉ gọi các hàm ở đây. Kiểm cục bộ chỉ bằng `selftest_r2.py` (mô hình giả, dữ liệu giả).
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as cm                                       # noqa: E402

MODEL_ID = 'facebook/esm2_t33_650M_UR50D'                 # chốt ở PROTOCOL §2, không đổi sau khi thấy số
PCA_K = 64
PCA_SEED = 17
BATCH = 256
LC_RESULTS = cm.TOPIC / 'research/learning-curve-2026-10-22/results.json'


# --------------------------------------------------------------------------- giai đoạn 1
def resolve_model_source(roots=('/kaggle/input', '/content')):
    """Ưu tiên bản ESM-2 đã gắn làm dataset/model (không cần Internet); nếu không có thì dùng HF hub."""
    for r in roots:
        rp = Path(r)
        if not rp.exists():
            continue
        for cfg in rp.rglob('config.json'):
            if 'esm2_t33_650m' in str(cfg.parent).lower().replace('-', '_'):
                return str(cfg.parent)
    return MODEL_ID


def make_hf_embed_fn(dev, source=None):
    import torch
    from transformers import AutoTokenizer, EsmModel
    src = source or resolve_model_source()
    tok = AutoTokenizer.from_pretrained(src)
    model = EsmModel.from_pretrained(src, add_pooling_layer=False)
    model = (model.half() if dev == 'cuda' else model).to(dev).eval()

    def embed(seqs):
        enc = tok(list(seqs), return_tensors='pt', padding=False)
        assert enc['input_ids'].shape[1] == 30, 'cần <cls> + 28 residue + <eos>'
        enc = {k: v.to(dev) for k, v in enc.items()}
        with torch.no_grad():
            h = model(**enc).last_hidden_state
        return h[:, 1:29, :].float()
    embed.source = src
    return embed


def extract_features(st, embed_fn, dev, batch=BATCH, log=print, limit=None):
    """F[i] = [ h_mut(pos) − h_wt(pos) ; mean_j (h_mut(j) − h_wt(j)) ] của ô i, float16."""
    import torch
    wt = st['wt_seq'].tolist()
    mut = st['mut_seq']
    pos = st['pos'].astype(np.int64)
    pep = st['pep_of_row'].astype(np.int64)
    n = len(mut) if limit is None else limit
    wt_h = torch.cat([embed_fn(wt[i:i + 64]) for i in range(0, len(wt), 64)]).to(dev)    # [P, 28, d]
    d = wt_h.shape[2]
    F = np.zeros((n, 2 * d), dtype=np.float16)
    t0 = time.time()
    for i in range(0, n, batch):
        j = min(n, i + batch)
        h = embed_fn(mut[i:j].tolist())
        delta = h - wt_h[torch.from_numpy(pep[i:j]).to(dev)]
        site = delta[torch.arange(j - i, device=dev), torch.from_numpy(pos[i:j] - 1).to(dev)]
        F[i:j] = torch.cat([site, delta.mean(1)], 1).cpu().numpy().astype(np.float16)
        if (i // batch) % 40 == 0:
            log(f'  {j}/{n} ô · {time.time() - t0:.0f}s')
    assert np.isfinite(F).all(), 'đặc trưng có NaN/Inf (tràn fp16?)'
    return F


# --------------------------------------------------------------------------- giai đoạn 2
def fit_all(data, F, k=PCA_K, seeds=cm.SEEDS, variants=('M3', 'M3+ESM', 'ESM'), log=print):
    from sklearn.decomposition import PCA
    base_n = data['base_n']
    Xc, yc = data['Xc'], data['yc']
    out = {v: {s: np.full(base_n, np.nan) for s in seeds} for v in variants}
    meta = {'pca_explained_variance_ratio_sum': [], 'alphas': {v: {} for v in variants}}
    for fold in range(5):
        _, _, _, pool = cm.pool_split(data, seeds[0], fold)          # pool chỉ phụ thuộc fold
        pca = PCA(n_components=k, svd_solver='randomized', random_state=PCA_SEED)
        pca.fit(F[pool].astype(np.float32))
        Z = np.concatenate([pca.transform(F[i:i + 20000].astype(np.float32))
                            for i in range(0, len(F), 20000)])
        mu, sd = Z[pool].mean(0), Z[pool].std(0)
        Z = (Z - mu) / np.where(sd > 0, sd, 1.0)
        meta['pca_explained_variance_ratio_sum'].append(float(pca.explained_variance_ratio_.sum()))
        blocks = {'M3': Xc[:, :180], 'M3+ESM': np.hstack([Xc[:, :180], Z]), 'ESM': Z}
        for seed in seeds:
            tr, va, te, _ = cm.pool_split(data, seed, fold)
            for v in variants:
                pred, alpha = cm.ridge_full(blocks[v], yc, tr, va, te)
                out[v][seed][te] = pred
                meta['alphas'][v][f'seed{seed}-fold{fold}'] = alpha
        log(f'  fold {fold}: PCA{k} giữ {meta["pca_explained_variance_ratio_sum"][-1]:.3f} phương sai')
    for v in variants:
        for s in seeds:
            assert not np.isnan(out[v][s]).any()
    return out, meta


def verdict(delta_ens, ci, seed_deltas):
    """PROTOCOL §6: 'nhận' cần CI dưới > 0 VÀ cả ba seed dương."""
    if ci[0] > 0 and len(seed_deltas) == 3 and all(d > 0 for d in seed_deltas):
        return 'nhận: đặc trưng ESM-2 cải thiện ridge M3 (đạt tiêu chí)'
    if ci[1] < 0:
        return 'âm: thêm đặc trưng ESM-2 làm ridge M3 kém đi'
    if ci[0] > 0:
        return 'lợi ích chưa bền qua seed (CI > 0 nhưng không đủ ba seed dương)'
    return 'chưa đủ bằng chứng (CI phủ 0)'


def summarize(oof, data, gates=None, log=print):
    import derisk as dr
    import run_curve as rc
    y0, idx0, groups0 = data['y0'], data['idx0'], data['groups0']
    seeds = list(next(iter(oof.values())).keys())
    res = {}
    for v, per_seed in oof.items():
        ps = {s: dr.macro_auroc(per_seed[s], y0, idx0) for s in seeds}
        ens = np.mean([per_seed[s] for s in seeds], axis=0)
        em, epp = dr.macro_auroc(ens, y0, idx0)
        res[v] = {'macro_auroc_per_seed': {str(s): ps[s][0] for s in seeds}, 'macro_auroc_ensemble': em,
                  'per_peptide_ensemble': epp, '_per_seed_pp': {s: ps[s][1] for s in seeds}}
    lc = json.loads(LC_RESULTS.read_text())['results']['ridge']['ext']
    if gates is not None:
        gates.check('M3_ensemble_vs_P0', res['M3']['macro_auroc_ensemble'], lc['macro_auroc_ensemble'], 1e-4)
        for s, ref in zip(seeds, lc['macro_auroc_per_seed']):
            gates.check(f'M3_seed{s}_vs_P0', res['M3']['macro_auroc_per_seed'][str(s)], ref, 2e-4)
    cmp = lambda a, b: rc.compare(a, b, groups0)
    primary = cmp(res['M3+ESM']['per_peptide_ensemble'], res['M3']['per_peptide_ensemble'])
    seed_d = [cmp(res['M3+ESM']['_per_seed_pp'][s], res['M3']['_per_seed_pp'][s])['delta'] for s in seeds]
    out = {'model': MODEL_ID, 'pca_k': PCA_K, 'seeds': seeds,
           'macro_auroc': {v: {k: res[v][k] for k in ('macro_auroc_per_seed', 'macro_auroc_ensemble')}
                           for v in res},
           'paired_M3+ESM_minus_M3': primary,
           'seed_deltas_M3+ESM_minus_M3': dict(zip(map(str, seeds), seed_d)),
           'descriptive_ESM_only_minus_M3': cmp(res['ESM']['per_peptide_ensemble'],
                                                 res['M3']['per_peptide_ensemble']),
           'verdict': verdict(primary['delta'], primary['ci95'], seed_d),
           'per_peptide_ensemble': {v: res[v]['per_peptide_ensemble'] for v in res}}
    log(json.dumps({k: out[k] for k in ('macro_auroc', 'paired_M3+ESM_minus_M3',
                                        'seed_deltas_M3+ESM_minus_M3', 'verdict')}, indent=2, ensure_ascii=False))
    return out


def save_oof(path, oof):
    np.savez_compressed(path, **{f'{v}__{s}': a for v, d in oof.items() for s, a in d.items()})


def load_oof(path):
    z = np.load(path)
    oof = {}
    for k in z.files:
        v, s = k.rsplit('__', 1)
        oof.setdefault(v, {})[int(s)] = z[k]
    return oof


if __name__ == '__main__':                      # chạy lại giai đoạn tổng hợp cục bộ từ r2-oof.npz đã tải về
    d = Path(sys.argv[1])
    data = cm.load_combined()
    res = summarize(load_oof(d / 'r2-oof.npz'), data)
    res['runner_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / 'results.json').write_text(json.dumps(res, indent=2, ensure_ascii=False) + '\n')
    print('->', HERE / 'results.json')
