import csv, gzip, sys, h5py, json
import numpy as np
from collections import defaultdict
full_gz, train_gz, holdout_txt, wdir = sys.argv[1:5]
AA='ACDEFGHIKLMNPQRSTVWY'; aa2i={a:i for i,a in enumerate(AA)}
def elu(x): return np.where(x>0, x, np.expm1(np.minimum(x,0)))
class PAP:
    def __init__(s,p):
        f=h5py.File(p,'r'); g=lambda n: np.array(f[n])
        s.Wc=g('int_cnn/int_cnn/kernel:0'); s.bc=g('int_cnn/int_cnn/bias:0'); s.k=s.Wc.shape[0]
        s.W2=g('int2/int2/kernel:0'); s.b2=g('int2/int2/bias:0')
        s.W3=g('int3/int3/kernel:0'); s.b3=g('int3/int3/bias:0')
        s.W4=g('latent_int/latent_int/kernel:0'); s.b4=g('latent_int/latent_int/bias:0')
        s.C1=g('ct1/ct1/kernel:0'); s.c1=g('ct1/ct1/bias:0')
        s.C2=g('ct2/ct2/kernel:0'); s.c2=g('ct2/ct2/bias:0')
        s.C3=g('ct3/ct3/kernel:0'); s.c3=g('ct3/ct3/bias:0')
        s.C4=g('latent_ct/latent_ct/kernel:0'); s.c4=g('latent_ct/latent_ct/bias:0')
    def internal(s,X):
        N,L,_=X.shape; k=s.k
        w=np.lib.stride_tricks.sliding_window_view(X,k,axis=1).transpose(0,1,3,2).reshape(N,L-k+1,k*20)
        h=elu(w@s.Wc.reshape(k*20,-1)+s.bc).mean(axis=1)
        h=elu(h@s.W2+s.b2); h=elu(h@s.W3+s.b3)
        return (h@s.W4+s.b4).ravel()
    def cterm(s,X):
        v=X.reshape(X.shape[0],-1)
        h=elu(v@s.C1+s.c1); h=elu(h@s.C2+s.c2); h=elu(h@s.C3+s.c3)
        return (h@s.C4+s.c4).ravel()
def oh(seqs):
    X=np.zeros((len(seqs),30,20),dtype=np.float32)
    for n,s in enumerate(seqs):
        for i,a in enumerate(s): X[n,i,aa2i[a]]=1.0
    return X
rows=[r for r in csv.DictReader(gzip.open(full_gz,'rt')) if '_tile' in r['name']]
tr={r['name'] for r in csv.DictReader(gzip.open(train_gz,'rt'))}
hold={l.strip() for l in open(holdout_txt) if l.strip()}
gene=lambda n:n.split('_tile')[0]
tg={gene(n) for n in tr}
maxt=defaultdict(int)
for r in rows: maxt[gene(r['name'])]=max(maxt[gene(r['name'])],int(r['name'].split('_tile')[1]))

m=PAP(f'{wdir}/cnn2w1_weights.h5')
def ev(sel, target, nmin=None, label=''):
    seqs=[];y=[];ct=[]
    for r in rows:
        g=gene(r['name'])
        if not sel(g,r): continue
        s=r['aa'].upper()
        if len(s)!=30 or any(c not in aa2i for c in s): continue
        v=r[target]
        if v in ('','NA','NaN'): continue
        if nmin is not None and float(r['n'])<nmin: continue
        seqs.append(s); y.append(float(v)); ct.append(int(r['name'].split('_tile')[1])==maxt[g])
    X=oh(seqs); y=np.array(y); ct=np.array(ct,dtype=bool)
    sc=m.internal(X)
    if ct.any(): sc=sc+np.where(ct, 0, 0); tmp=m.cterm(X[ct][:,25:30,:]); sc[ct]+=tmp
    rp=np.corrcoef(sc,y)[0,1]
    print(f'  {label:52} n={len(y):6}  Pearson={rp:.4f}')
    return rp

print('Muc tieu = abundance_score (cot 6, dung script dung):')
ev(lambda g,r: g in hold and g not in tg, 'abundance_score', None, 'holdout hieu dung 428 gene')
ev(lambda g,r: g in hold,                 'abundance_score', None, 'toan bo 527 gene trong danh sach')
ev(lambda g,r: g not in tg,               'abundance_score', None, 'moi gene KHONG co trong file train (728)')
ev(lambda g,r: True,                      'abundance_score', None, 'toan bo 212k tile')
ev(lambda g,r: g in hold and g not in tg, 'abundance_score', 3,    'holdout hieu dung, loc n>=3')
ev(lambda g,r: g in hold and g not in tg, 'abundance_score', 6,    'holdout hieu dung, loc n>=6')
print('Muc tieu = degron_score:')
ev(lambda g,r: g in hold and g not in tg, 'degron_score', None, 'holdout hieu dung 428 gene')
ev(lambda g,r: True,                      'degron_score', None, 'toan bo 212k tile')
