"""G2 extension, 18 Oct 2026. Three experiments fixed in PREREGISTRATION.md before any run.

Subcommands: overlap (E1), candidates (E2), degformer_arch (E3).
Splits, labels and metric reuse g2-saturation-2026-10-18 exactly; nothing is retuned here.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
os.environ.setdefault('OMP_NUM_THREADS','4')
import sys,json,csv,ast,hashlib,time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import GroupKFold,GroupShuffleSplit
from sklearn.linear_model import Ridge
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'g2-saturation-2026-10-18'
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
sys.path.insert(0,str(TOPIC/'research/residue-task-derisk-2026-10-15'))
import residue_data as rd
import derisk as dr
torch.set_num_threads(4)
SEEDS=[17,29,43]
CACHE=TOPIC/'data/processed/g2-saturation-input.npz'
PRED=TOPIC/'data/processed/g2-saturation-predictions.npz'
RAW=TOPIC/'data/raw/degformer-isolated'
BOOT=5000

def load():
    z=np.load(CACHE)
    return z['X'],z['y'],z['idx'],z['peps'],z['groups'],z['rowg'],z['seqs'],z['wt']

def macro(scores,y,idx,mask=None):
    """Macro AUROC by peptide; mask restricts the cells that count, peptide kept only if both classes survive."""
    per=[]
    for a,b in idx:
        s=scores[a:b];t=y[a:b]>=rd.RESCUE_DELTA
        if mask is not None:
            m=mask[a:b];s=s[m];t=t[m]
        per.append(dr.auroc(s,t) if len(t) else None)
    ok=[v for v in per if v is not None]
    return (float(np.mean(ok)) if ok else None),per

def paired(pa,pb,groups,rng_seed=20261018):
    keep=[i for i in range(len(pa)) if pa[i] is not None and pb[i] is not None]
    if not keep:return None
    d=np.array([pa[i]-pb[i] for i in keep]);g=np.array(groups)[keep];u=sorted(set(g))
    rng=np.random.default_rng(rng_seed)
    boot=[np.mean(np.concatenate([d[g==c] for c in rng.choice(u,len(u),replace=True)])) for _ in range(BOOT)]
    return {'delta':float(d.mean()),'ci95':np.quantile(boot,[.025,.975]).tolist(),
            'n_peptides':len(keep),'n_clusters':len(u),'n_positive_peptides':int((d>0).sum())}

def folds(X,y,rowg,seed):
    for fold,(tr,te) in enumerate(GroupKFold(5).split(X,y,rowg)):
        ti,vi=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=seed).split(X[tr],y[tr],rowg[tr]))
        train,val=tr[ti],tr[vi]
        assert not(set(rowg[train])&set(rowg[te])) and not(set(rowg[val])&set(rowg[te]))
        yield fold,train,val,te

# ----------------------------------------------------------------- E1
def cmd_overlap():
    X,y,idx,peps,groups,rowg,seqs,wt=load()
    training={r['sequence'] for r in csv.DictReader((RAW/'training_data.csv').open())}
    seen=np.array([s in training for s in seqs])
    mask=~seen
    pred=np.load(PRED)
    out={'n_cells':int(len(y)),'n_cells_overlapping':int(seen.sum()),'n_cells_held':int(mask.sum()),
         'fraction_overlapping':float(seen.mean()),'wt_in_training':int(sum(s in training for s in set(wt))),
         'n_wt_peptides':int(len(set(wt))),'full':{},'nonoverlap':{},'per_peptide_nonoverlap_cells':{}}
    perf,pern={},{}
    for k in pred.files:
        out['full'][k],perf[k]=macro(pred[k],y,idx)
        out['nonoverlap'][k],pern[k]=macro(pred[k],y,idx,mask)
    kept=[i for i in range(len(peps)) if pern['ridge'][i] is not None]
    out['n_peptides_scored_nonoverlap']=len(kept)
    for i,p in enumerate(peps):
        a,b=idx[i];out['per_peptide_nonoverlap_cells'][str(p)]=int(mask[a:b].sum())
    out['paired_nonoverlap']={f'Degformer_minus_{b}':paired(pern['Degformer'],pern[b],groups) for b in ['ridge','DeltaPAP','gate_pap']}
    out['paired_nonoverlap']['ridge_minus_DeltaPAP']=paired(pern['ridge'],pern['DeltaPAP'],groups)
    out['shift_full_to_nonoverlap']={k:(None if out['nonoverlap'][k] is None or out['full'][k] is None
                                        else out['nonoverlap'][k]-out['full'][k]) for k in pred.files}
    (HERE/'e1-overlap.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['n_cells_held','fraction_overlapping','full','nonoverlap','paired_nonoverlap']},indent=2))

# ----------------------------------------------------------------- E2
class Interact(nn.Module):
    """Pre-registered interaction candidates. No DeltaPAP branch, so the head carries the interaction alone."""
    def __init__(self,kind):
        super().__init__();self.kind=kind
        self.pair=nn.Linear(40,32);self.context=nn.Linear(140,32)
        if kind=='bilinear':
            self.up=nn.Linear(32,8,bias=False);self.uc=nn.Linear(32,8,bias=False)
            self.head=nn.Sequential(nn.Linear(72,32),nn.ReLU(),nn.Linear(32,1))
        else:
            self.scale=nn.Linear(40,32);self.shift=nn.Linear(40,32)
            self.head=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
    def forward(self,x):
        pair=torch.relu(self.pair(x[:,:40]));ctx=torch.tanh(self.context(x[:,40:180]))
        if self.kind=='bilinear':
            h=torch.cat([pair,ctx,self.up(pair)*self.uc(ctx)],1)
        else:
            h=torch.cat([pair,ctx*self.scale(x[:,:40])+self.shift(x[:,:40])],1)
        return self.head(h).squeeze(1)

def train_net(kind,X,y,tr,va,te,seed,checkpoint):
    torch.manual_seed(seed);net=Interact(kind)
    opt=torch.optim.AdamW(net.parameters(),lr=.002,weight_decay=.01)
    xx=torch.tensor(X,dtype=torch.float32);yy=torch.tensor(y,dtype=torch.float32)
    rng=np.random.default_rng(seed);best=1e99;state=None;ep_best=0
    for epoch in range(1,61):
        net.train()
        for batch in np.array_split(rng.permutation(tr),max(1,len(tr)//1024)):
            loss=((net(xx[batch])-yy[batch])**2).mean();opt.zero_grad();loss.backward();opt.step()
        net.eval()
        with torch.no_grad():v=float(((net(xx[va])-yy[va])**2).mean())
        if v<best-1e-6:best=v;state={k:t.detach().clone() for k,t in net.state_dict().items()};ep_best=epoch
        if epoch-ep_best>=8:break
    net.load_state_dict(state);checkpoint.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':state,'kind':kind,'seed':seed,'epoch':ep_best,
                'train_indices':tr.tolist(),'validation_indices':va.tolist(),'test_indices':te.tolist()},checkpoint)
    with torch.no_grad():return net(xx[te]).numpy(),ep_best

def cross_features(X):
    """Explicit cross product of the substituted amino acid (20) with ordered +-3 context (120)."""
    mut=X[:,20:40];ctx=X[:,60:180]
    return (mut[:,:,None]*ctx[:,None,:]).reshape(len(X),-1).astype(np.float32)

def gram_ridge(Xtr,ytr,Xva,yva,Xte,alphas=(1,10,100,1000),chunk=4000):
    p=Xtr.shape[1];G=np.zeros((p,p));b=np.zeros(p)
    for a in range(0,len(Xtr),chunk):
        blk=Xtr[a:a+chunk].astype(np.float64);G+=blk.T@blk;b+=blk.T@ytr[a:a+chunk]
    def solve(al):return np.linalg.solve(G+al*np.eye(p),b)
    best=min(((np.mean((Xva.astype(np.float64)@solve(al)-yva)**2),al) for al in alphas))
    w=solve(best[1])
    return Xte.astype(np.float64)@w,best[1]

def cmd_candidates():
    X,y,idx,peps,groups,rowg,seqs,wt=load()
    base=np.load(PRED);ref={'ridge':base['ridge'],'DeltaPAP':base['DeltaPAP']}
    out={'preregistered':['bilinear','film','cross_ridge'],'seeds':SEEDS,'macro_auroc':{},
         'per_seed':{},'epochs':{},'comparisons':{},'success_criterion':
         'positive paired delta against ridge in all three seeds AND cluster bootstrap CI excluding zero AND the same against frozen DeltaPAP'}
    perref={k:macro(v,y,idx)[1] for k,v in ref.items()}
    preds={}
    for kind in ['bilinear','film']:
        allseed=[];out['epochs'][kind]=[]
        for seed in SEEDS:
            o=np.zeros(len(y))
            for fold,tr,va,te in folds(X,y,rowg,seed):
                o[te],ep=train_net(kind,X[:,:180],y,tr,va,te,seed,
                    TOPIC/f'data/processed/g2-ext-models/{kind}-seed{seed}-fold{fold}.pt')
                out['epochs'][kind].append({'seed':seed,'fold':fold,'epoch':ep})
            allseed.append(o);print(kind,seed,macro(o,y,idx)[0],flush=True)
        np.savez_compressed(TOPIC/f'data/processed/g2-ext-{kind}-predictions.npz',seeds=SEEDS,predictions=allseed)
        preds[kind]=np.mean(allseed,axis=0);out['per_seed'][kind]=[macro(o,y,idx)[0] for o in allseed]
    # cross_ridge is deterministic, so one pass is the ensemble and the per seed entry repeats it.
    Xc=np.hstack([X[:,:180].astype(np.float32),cross_features(X)])
    out['cross_ridge_features']=int(Xc.shape[1])
    o=np.zeros(len(y));alphas=[]
    for fold,tr,va,te in folds(X,y,rowg,SEEDS[0]):
        o[te],al=gram_ridge(Xc[tr],y[tr],Xc[va],y[va],Xc[te]);alphas.append({'fold':fold,'alpha':al})
    preds['cross_ridge']=o;out['per_seed']['cross_ridge']=[macro(o,y,idx)[0]]*3;out['epochs']['cross_ridge']=alphas
    print('cross_ridge',macro(o,y,idx)[0],flush=True)
    np.savez_compressed(TOPIC/'data/processed/g2-ext-cross_ridge-predictions.npz',predictions=o)
    for k,v in preds.items():
        out['macro_auroc'][k]=macro(v,y,idx)[0]
        per=macro(v,y,idx)[1]
        out['comparisons'][k]={f'minus_{r}':paired(per,perref[r],groups) for r in perref}
        if k in ['bilinear','film']:
            ps=np.load(TOPIC/f'data/processed/g2-ext-{k}-predictions.npz')['predictions']
            out['comparisons'][k]['per_seed_minus_ridge']=[paired(macro(s,y,idx)[1],perref['ridge'],groups) for s in ps]
        else:
            out['comparisons'][k]['per_seed_minus_ridge']=[out['comparisons'][k]['minus_ridge']]
    out['macro_auroc']['ridge_reference']=macro(ref['ridge'],y,idx)[0]
    out['macro_auroc']['DeltaPAP_reference']=macro(ref['DeltaPAP'],y,idx)[0]
    for k in preds:
        c=out['comparisons'][k];seedpos=all(s['delta']>0 for s in c['per_seed_minus_ridge'])
        ci_r=c['minus_ridge']['ci95'];ci_p=c['minus_DeltaPAP']['ci95']
        c['meets_preregistered_criterion']=bool(seedpos and ci_r[0]>0 and ci_p[0]>0)
    out['runner_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out['versions']={'numpy':np.__version__,'torch':torch.__version__,'python':sys.version}
    (HERE/'e2-candidates.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'macro_auroc':out['macro_auroc'],'criterion':{k:out['comparisons'][k]['meets_preregistered_criterion'] for k in preds}},indent=2))

# ----------------------------------------------------------------- E3
def degformer_class():
    m=json.loads((BASE/'source-manifest.json').read_text())
    for f,meta in m['files'].items():
        assert hashlib.sha256((RAW/f).read_bytes()).hexdigest()==meta['sha256'],f
    tree=ast.parse((RAW/'predict.py').read_text())
    node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PeptideTransformer')
    ns={'torch':torch,'nn':nn,'MAX_LEN':28}
    exec(compile(ast.Module(body=[node],type_ignores=[]),'reviewed-degformer-class','exec'),ns)
    return ns['PeptideTransformer']

def cmd_degformer_arch(max_epochs=30,patience=6,seed=17):
    X,y,idx,peps,groups,rowg,seqs,wt=load()
    d=rd.load_all();psi={p:d['sat'][p]['psi_wt'] for p in peps}
    wtpsi=np.array([psi[p] for p in peps])
    pep_of=np.concatenate([np.repeat(i,b-a) for i,(a,b) in enumerate(idx)])
    y_abs=y+wtpsi[pep_of]
    enc=lambda s:[rd.AAS.index(c) for c in s]
    Em=torch.tensor([enc(s) for s in seqs]);Ew=torch.tensor([enc(s) for s in wt])
    uniq=sorted({(str(w),i) for w,i in zip(wt,pep_of)},key=lambda t:t[1])
    wt_rows=torch.tensor([enc(s) for s,_ in uniq]);wt_pep=np.array([i for _,i in uniq])
    Net=degformer_class();out={'seed':seed,'max_epochs':max_epochs,'patience':patience,'folds':[],
        'hyperparameters':'author published: Adam lr 1e-4, batch 512, d_model 128, 4 layers, 8 heads, ff 256, dropout 0.1',
        'target':'absolute PSI of the sequence, z scored on outer train; cell score is pred(mutant) minus pred(wild type)'}
    pred=np.zeros(len(y))
    for fold,tr,va,te in folds(X,y,rowg,seed):
        wtr=np.where(np.isin(wt_pep,np.unique(pep_of[tr])))[0]
        wva=np.where(np.isin(wt_pep,np.unique(pep_of[va])))[0]
        xt=torch.cat([Em[tr],wt_rows[wtr]]);yt=np.concatenate([y_abs[tr],wtpsi[wt_pep[wtr]]])
        mu,sd=float(yt.mean()),float(yt.std())
        yt=torch.tensor((yt-mu)/sd,dtype=torch.float32)
        xv=torch.cat([Em[va],wt_rows[wva]])
        yv=torch.tensor((np.concatenate([y_abs[va],wtpsi[wt_pep[wva]]])-mu)/sd,dtype=torch.float32)
        torch.manual_seed(seed);net=Net(21);opt=torch.optim.Adam(net.parameters(),lr=1e-4)
        rng=np.random.default_rng(seed);best=1e99;state=None;ep_best=0;curve=[]
        for epoch in range(1,max_epochs+1):
            t0=time.time();net.train()
            for b in np.array_split(rng.permutation(len(xt)),max(1,len(xt)//512)):
                loss=((net(xt[b])-yt[b])**2).mean();opt.zero_grad();loss.backward();opt.step()
            net.eval()
            with torch.no_grad():
                tot=0.0
                for a in range(0,len(xv),512):tot+=float(((net(xv[a:a+512])-yv[a:a+512])**2).sum())
                v=tot/len(xv)
            curve.append({'epoch':epoch,'val_mse':v,'seconds':round(time.time()-t0,1)})
            print(f'fold{fold} epoch{epoch} val{v:.5f} {curve[-1]["seconds"]}s',flush=True)
            if v<best-1e-6:best=v;state={k:t.detach().clone() for k,t in net.state_dict().items()};ep_best=epoch
            if epoch-ep_best>=patience:break
        net.load_state_dict(state);net.eval()
        def run(t):
            o=[]
            with torch.no_grad():
                for a in range(0,len(t),512):o.extend(net(t[a:a+512]).numpy())
            return np.array(o)
        pred[te]=(run(Em[te])-run(Ew[te]))*sd
        ck=TOPIC/f'data/processed/g2-ext-models/degformer_arch-seed{seed}-fold{fold}.pt'
        ck.parent.mkdir(parents=True,exist_ok=True)
        torch.save({'state_dict':state,'seed':seed,'fold':fold,'epoch':ep_best,'target_mean':mu,'target_sd':sd,
                    'train_indices':tr.tolist(),'validation_indices':va.tolist(),'test_indices':te.tolist()},ck)
        out['folds'].append({'fold':fold,'best_epoch':ep_best,'best_val_mse':best,
                             'stopped_at_cap':ep_best==max_epochs or epoch==max_epochs,'curve':curve})
    base=np.load(PRED)
    per={'degformer_arch':macro(pred,y,idx)[1],'ridge':macro(base['ridge'],y,idx)[1],
         'DeltaPAP':macro(base['DeltaPAP'],y,idx)[1],'Degformer_checkpoint':macro(base['Degformer'],y,idx)[1]}
    out['macro_auroc']={'degformer_arch_cov80':macro(pred,y,idx)[0],
        'ridge':macro(base['ridge'],y,idx)[0],'DeltaPAP':macro(base['DeltaPAP'],y,idx)[0],
        'Degformer_official_checkpoint_leaky':macro(base['Degformer'],y,idx)[0]}
    out['comparisons']={f'degformer_arch_minus_{k}':paired(per['degformer_arch'],per[k],groups) for k in ['ridge','DeltaPAP']}
    out['runner_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    np.savez_compressed(TOPIC/'data/processed/g2-ext-degformer_arch-predictions.npz',predictions=pred,seed=seed)
    (HERE/'e3-degformer-arch.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'macro_auroc':out['macro_auroc'],'comparisons':out['comparisons']},indent=2))

if __name__=='__main__':
    {'overlap':cmd_overlap,'candidates':cmd_candidates,'degformer_arch':cmd_degformer_arch}[sys.argv[1]]()
