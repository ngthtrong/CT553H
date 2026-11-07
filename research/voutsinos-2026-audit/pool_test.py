import csv, gzip, sys, h5py, json
import numpy as np
full_gz, train_gz, holdout_txt, wdir, out = sys.argv[1:6]
AA='ACDEFGHIKLMNPQRSTVWY'; aa2i={a:i for i,a in enumerate(AA)}
def elu(x): return np.where(x>0,x,np.expm1(np.minimum(x,0)))
def load(p):
    f=h5py.File(p,'r'); g=lambda n: np.array(f[n])
    return dict(Wc=g('int_cnn/int_cnn/kernel:0'), bc=g('int_cnn/int_cnn/bias:0'),
        W2=g('int2/int2/kernel:0'), b2=g('int2/int2/bias:0'),
        W3=g('int3/int3/kernel:0'), b3=g('int3/int3/bias:0'),
        W4=g('latent_int/latent_int/kernel:0'), b4=g('latent_int/latent_int/bias:0'))
def head(h,w):
    h=elu(h@w['W2']+w['b2']); h=elu(h@w['W3']+w['b3']); return (h@w['W4']+w['b4']).ravel()
def conv(X,w):
    k=w['Wc'].shape[0]; N,L,_=X.shape
    win=np.lib.stride_tricks.sliding_window_view(X,k,axis=1).transpose(0,1,3,2).reshape(N,L-k+1,k*20)
    return elu(win@w['Wc'].reshape(k*20,-1)+w['bc'])     # (N, L-k+1, nf)

rows=[r for r in csv.DictReader(gzip.open(full_gz,'rt')) if '_tile' in r['name']]
tr={r['name'].split('_tile')[0] for r in csv.DictReader(gzip.open(train_gz,'rt')) if '_tile' in r['name']}
hold={l.strip() for l in open(holdout_txt) if l.strip()}
seqs=[];y=[]
for r in rows:
    g=r['name'].split('_tile')[0]
    if not (g in hold and g not in tr): continue
    s=r['aa'].upper()
    if len(s)!=30 or any(c not in aa2i for c in s): continue
    v=r['abundance_score']
    if v in ('','NA','NaN'): continue
    seqs.append(s); y.append(float(v))
X=np.zeros((len(seqs),30,20),dtype=np.float32)
for n,s in enumerate(seqs):
    for i,a in enumerate(s): X[n,i,aa2i[a]]=1.0
y=np.array(y)
print(f"holdout hieu dung: {len(y)} tile\n")
res={}
for mn in ['cnn2w1','cnn2w7']:
    w=load(f'{wdir}/{mn}_weights.h5'); A=conv(X,w); k=w['Wc'].shape[0]
    out_={}
    for pool,fn in [('average (nhu tac gia)',lambda a:a.mean(axis=1)),
                    ('max',lambda a:a.max(axis=1)),
                    ('top-3 mean',lambda a:np.sort(a,axis=1)[:,-3:,:].mean(axis=1))]:
        p=head(fn(A),w); rp=abs(np.corrcoef(p,y)[0,1])
        out_[pool]=round(float(rp),4)
        print(f"  {mn} (cua so {k}) + {pool:22} -> |Pearson| = {rp:.4f}")
    res[mn]=out_
    # do do "tap trung" cua tin hieu theo vi tri
    act=A.max(axis=2)                              # (N, L-k+1) hoat do manh nhat moi vi tri
    sh=act/np.maximum(act.sum(axis=1,keepdims=True),1e-9)
    ent=-(sh*np.log(sh+1e-12)).sum(axis=1)
    print(f"  {mn}: entropy phan bo hoat do theo vi tri = {ent.mean():.3f} / max {np.log(act.shape[1]):.3f}"
          f"  -> tin hieu {'TAP TRUNG' if ent.mean()<0.9*np.log(act.shape[1]) else 'DAN DEU'}\n")
    res[mn]['position_entropy']=round(float(ent.mean()),3)
    res[mn]['position_entropy_max']=round(float(np.log(act.shape[1])),3)
json.dump(res,open(out,'w'),indent=1); print("wrote",out)
