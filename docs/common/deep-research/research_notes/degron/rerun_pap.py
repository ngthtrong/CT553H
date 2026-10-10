import csv, gzip, sys, json, h5py
import numpy as np
from collections import defaultdict

full_gz, train_gz, holdout_txt, wdir, out = sys.argv[1:6]
AA = 'ACDEFGHIKLMNPQRSTVWY'; aa2i = {a:i for i,a in enumerate(AA)}

def elu(x): return np.where(x > 0, x, np.expm1(np.minimum(x, 0)))

class PAP:
    def __init__(self, path):
        f = h5py.File(path, 'r')
        g = lambda n: np.array(f[n])
        self.Wc = g('int_cnn/int_cnn/kernel:0'); self.bc = g('int_cnn/int_cnn/bias:0')
        self.k = self.Wc.shape[0]
        self.W2 = g('int2/int2/kernel:0'); self.b2 = g('int2/int2/bias:0')
        self.W3 = g('int3/int3/kernel:0'); self.b3 = g('int3/int3/bias:0')
        self.W4 = g('latent_int/latent_int/kernel:0'); self.b4 = g('latent_int/latent_int/bias:0')
        self.C1 = g('ct1/ct1/kernel:0'); self.c1 = g('ct1/ct1/bias:0')
        self.C2 = g('ct2/ct2/kernel:0'); self.c2 = g('ct2/ct2/bias:0')
        self.C3 = g('ct3/ct3/kernel:0'); self.c3 = g('ct3/ct3/bias:0')
        self.C4 = g('latent_ct/latent_ct/kernel:0'); self.c4 = g('latent_ct/latent_ct/bias:0')
    def internal(self, X):                      # X: (N,L,20)
        N, L, _ = X.shape; k = self.k
        Wf = self.Wc.reshape(k*20, -1)          # (k*20, nf)
        win = np.lib.stride_tricks.sliding_window_view(X, k, axis=1)   # (N, L-k+1, 20, k)
        win = win.transpose(0,1,3,2).reshape(N, L-k+1, k*20)
        h = elu(win @ Wf + self.bc).mean(axis=1)                       # GAP -> (N,nf)
        h = elu(h @ self.W2 + self.b2); h = elu(h @ self.W3 + self.b3)
        return (h @ self.W4 + self.b4).ravel()
    def cterm(self, X):                         # X: (N,5,20)
        v = X.reshape(X.shape[0], -1)
        h = elu(v @ self.C1 + self.c1); h = elu(h @ self.C2 + self.c2); h = elu(h @ self.C3 + self.c3)
        return (h @ self.C4 + self.c4).ravel()

def onehot(seqs):
    X = np.zeros((len(seqs), len(seqs[0]), 20), dtype=np.float32)
    for n, s in enumerate(seqs):
        for i, a in enumerate(s): X[n, i, aa2i[a]] = 1.0
    return X

# ---- load data
rows = []
with gzip.open(full_gz, 'rt') as fh:
    for r in csv.DictReader(fh): rows.append(r)
train_names = set()
with gzip.open(train_gz, 'rt') as fh:
    for r in csv.DictReader(fh): train_names.add(r['name'])
hold = {l.strip() for l in open(holdout_txt) if l.strip()}
def gene(n): return n.split('_tile')[0]

train_genes = {gene(n) for n in train_names}
eff_hold = {g for g in hold if g not in train_genes}

# last tile index per gene = C-terminal tile
maxtile = defaultdict(int)
rows = [r for r in rows if '_tile' in r['name']]
for r in rows:
    g = gene(r['name']); idx = int(r['name'].split('_tile')[1]); maxtile[g] = max(maxtile[g], idx)

def subset(pred):
    seqs, y, isct = [], [], []
    for r in rows:
        if not pred(gene(r['name'])): continue
        s = r['aa'].upper()
        if len(s) != 30 or any(c not in aa2i for c in s): continue
        v = r['abundance_score']
        if v in ('', 'NA', 'NaN'): continue
        seqs.append(s); y.append(float(v))
        isct.append(int(r['name'].split('_tile')[1]) == maxtile[gene(r['name'])])
    return seqs, np.array(y), np.array(isct, dtype=bool)

sets = {
    'holdout_hieu_dung_428gene': subset(lambda g: g in eff_hold),
    'train': subset(lambda g: g in train_genes),
}

res = {}
rng = np.random.default_rng(12345)
for mname in ['cnn2w1', 'cnn2w7']:
    m = PAP(f'{wdir}/{mname}_weights.h5')
    res[mname] = {'cnn_kernel': int(m.k)}
    print(f'\n===== {mname}  (cnn kernel = {m.k}) =====')
    for sname, (seqs, y, isct) in sets.items():
        X = onehot(seqs)
        si = m.internal(X)
        sc = np.zeros(len(seqs))
        if isct.any(): sc[isct] = m.cterm(X[isct][:, 25:30, :])
        full = si + sc
        rp_full = np.corrcoef(full, y)[0,1]; rp_int = np.corrcoef(si, y)[0,1]
        from scipy.stats import spearmanr
        sp = spearmanr(full, y).statistic
        print(f'  {sname:28} n={len(y):6}  Pearson(full)={rp_full:.4f}  Pearson(int only)={rp_int:.4f}  Spearman={sp:.4f}  (C-term tiles: {int(isct.sum())})')
        res[mname][sname] = {'n': len(y), 'pearson_full': round(float(rp_full),4),
                             'pearson_internal_only': round(float(rp_int),4),
                             'spearman_full': round(float(sp),4), 'n_cterm_tiles': int(isct.sum())}
    # ---- permutation test on holdout
    seqs, y, isct = sets['holdout_hieu_dung_428gene']
    X = onehot(seqs)
    base = m.internal(X)
    Xs = X.copy()
    for n in range(Xs.shape[0]): Xs[n] = Xs[n][rng.permutation(30)]
    perm = m.internal(Xs)
    d = np.abs(base - perm)
    print(f'  PHEP THU DAO THU TU residue (chi kenh noi):')
    print(f'    max |delta| = {d.max():.3e}   mean |delta| = {d.mean():.3e}   Pearson(base,perm) = {np.corrcoef(base,perm)[0,1]:.6f}')
    res[mname]['permutation_test'] = {'max_abs_delta': float(f'{d.max():.6g}'),
        'mean_abs_delta': float(f'{d.mean():.6g}'),
        'pearson_base_vs_permuted': round(float(np.corrcoef(base,perm)[0,1]),6)}

json.dump(res, open(out,'w'), indent=1)
print('\nwrote', out)
