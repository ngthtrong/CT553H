import csv, gzip, sys, h5py
import numpy as np
full_gz, train_gz, holdout_txt, wdir = sys.argv[1:5]
AA='ACDEFGHIKLMNPQRSTVWY'; aa2i={a:i for i,a in enumerate(AA)}
def elu(x): return np.where(x>0,x,np.expm1(np.minimum(x,0)))
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
        h=elu(h@s.W2+s.b2); h=elu(h@s.W3+s.b3); return (h@s.W4+s.b4).ravel()
    def cterm(s,X):
        v=X.reshape(X.shape[0],-1)
        h=elu(v@s.C1+s.c1); h=elu(h@s.C2+s.c2); h=elu(h@s.C3+s.c3); return (h@s.C4+s.c4).ravel()
rows=[r for r in csv.DictReader(gzip.open(full_gz,'rt')) if '_tile' in r['name']]
tr={r['name'].split('_tile')[0] for r in csv.DictReader(gzip.open(train_gz,'rt'))}
hold={l.strip() for l in open(holdout_txt) if l.strip()}
gene=lambda n:n.split('_tile')[0]
sets={'holdout hieu dung 428 gene': lambda g: g in hold and g not in tr,
      'toan bo 212k tile':          lambda g: True,
      'tap train':                  lambda g: g in tr}
for mn in ['cnn2w1','cnn2w7']:
    m=PAP(f'{wdir}/{mn}_weights.h5')
    print(f'===== {mn} (kernel {m.k}) — AP DUNG KENH C-TERM CHO MOI TILE =====')
    for lab,sel in sets.items():
        seqs=[];y=[]
        for r in rows:
            if not sel(gene(r['name'])): continue
            s=r['aa'].upper()
            if len(s)!=30 or any(c not in aa2i for c in s): continue
            v=r['abundance_score']
            if v in ('','NA','NaN'): continue
            seqs.append(s); y.append(float(v))
        X=np.zeros((len(seqs),30,20),dtype=np.float32)
        for n,s in enumerate(seqs):
            for i,a in enumerate(s): X[n,i,aa2i[a]]=1.0
        y=np.array(y)
        si=m.internal(X); sc=m.cterm(X[:,25:30,:]); full=si+sc
        print(f'  {lab:28} n={len(y):6}  int={np.corrcoef(si,y)[0,1]:.4f}  '
              f'ct-only={np.corrcoef(sc,y)[0,1]:.4f}  FULL={np.corrcoef(full,y)[0,1]:.4f}')
