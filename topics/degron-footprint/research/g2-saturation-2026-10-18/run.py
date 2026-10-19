"""CPU reproducible saturation benchmark; run with python -I, threads limited to 2.
Outer cov80 folds; inner cov80 validation selects epochs. No outer-label tuning.
Architecture candidate: mutation-conditioned local context gate + frozen DeltaPAP residual.
Novelty is a hypothesis, not a claim established by this experiment.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
os.environ['OMP_NUM_THREADS']='2'
import sys,json,hashlib,csv,ast
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import GroupKFold,GroupShuffleSplit
from sklearn.linear_model import Ridge
HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'log.md').exists())
sys.path.insert(0,str(TOPIC/'research/residue-task-derisk-2026-10-15'))
import residue_data as rd
import derisk as dr
sys.path.insert(0,str(TOPIC/'research/pap-baseline'))
from pap_baseline import PAP,WDIR

torch.set_num_threads(2)
SEEDS=[17,29,43]
class Gate(nn.Module):
    def __init__(self, gated=True, pap=True):
        super().__init__();self.gated=gated;self.pap=pap
        self.pair=nn.Linear(40,32);self.context=nn.Linear(140,32)
        self.head=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
    def forward(self,x):
        pair=torch.relu(self.pair(x[:,:40]));ctx=torch.tanh(self.context(x[:,40:180]))
        if self.gated:ctx=ctx*torch.sigmoid(self.pair(x[:,:40]))
        return self.head(torch.cat([pair,ctx],1)).squeeze(1)+(x[:,180] if self.pap else 0)

def neural(X,y,tr,va,te,seed,gated,pap,checkpoint):
    torch.manual_seed(seed);net=Gate(gated,pap);opt=torch.optim.AdamW(net.parameters(),lr=.002,weight_decay=.01)
    xx=torch.tensor(X,dtype=torch.float32);yy=torch.tensor(y,dtype=torch.float32)
    rng=np.random.default_rng(seed);best=1e99;state=None;epoch_best=0
    for epoch in range(1,61):
        net.train()
        for batch in np.array_split(rng.permutation(tr),max(1,len(tr)//1024)):
            loss=((net(xx[batch])-yy[batch])**2).mean();opt.zero_grad();loss.backward();opt.step()
        net.eval()
        with torch.no_grad():v=float(((net(xx[va])-yy[va])**2).mean())
        if v<best-1e-6:best=v;state={k:t.detach().clone() for k,t in net.state_dict().items()};epoch_best=epoch
        if epoch-epoch_best>=8:break
    net.load_state_dict(state)
    checkpoint.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':state,'seed':seed,'gated':gated,'pap':pap,'epoch':epoch_best,'train_indices':tr.tolist(),'validation_indices':va.tolist(),'test_indices':te.tolist()},checkpoint)
    with torch.no_grad():return net(xx[te]).numpy(),epoch_best

def main():
    cache=TOPIC/'data/processed/g2-saturation-input.npz'
    if not cache.exists():
        d=rd.load_all();peps,rows,y,idx=dr.rows_and_labels(d['sat'],'sat')
        groups=np.array([d['clusters'].get(rd.accession(p),rd.accession(p)) for p in peps])
        rowg=np.concatenate([np.repeat(groups[i],b-a) for i,(a,b) in enumerate(idx)])
        seqs=[s[:p-1]+aa+s[p:] for s,p,aa in rows];wt=[s for s,p,aa in rows]
        pap=PAP(WDIR/'cnn2w1_weights.h5')
        def score(s):return np.concatenate([pap.score(s[i:i+256]) for i in range(0,len(s),256)])
        dp=score(seqs)-score(wt) # Match the established PAP benchmark: mutant minus WT.
        X=dr.featurize(rows,{'pair','comp','ctx'})
        # featurize block order pair, comp, ctx is fixed.
        np.savez_compressed(cache,X=np.c_[X,dp],y=y,idx=idx,peps=peps,groups=groups,rowg=rowg,seqs=seqs,wt=wt)
    z=np.load(cache);X=z['X'];y=z['y'];idx=z['idx'];groups=z['groups'];rowg=z['rowg'];peps=z['peps']
    preds={'DeltaPAP':X[:,-1]};epochs={};splits=[]
    models={'ridge':None,'gate_pap':(True,True),'no_gate_pap':(False,True),'gate_no_pap':(True,False)}
    for name,cfg in models.items():
        allseed=[];epochs[name]=[]
        for seed in SEEDS:
            out=np.zeros(len(y))
            for fold,(tr,te) in enumerate(GroupKFold(5).split(X,y,rowg)):
                ti,vi=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=seed).split(X[tr],y[tr],rowg[tr]));train,val=tr[ti],tr[vi]
                assert not(set(rowg[train])&set(rowg[te])) and not(set(rowg[val])&set(rowg[te]))
                if cfg is None:
                    best=min((np.mean((Ridge(alpha=a).fit(X[train,:180],y[train]).predict(X[val,:180])-y[val])**2),a) for a in [1,10,100,1000])[1]
                    out[te]=Ridge(alpha=best).fit(X[tr,:180],y[tr]).predict(X[te,:180]);ep=best
                else:out[te],ep=neural(X,y,train,val,te,seed,*cfg,TOPIC/f'data/processed/g2-saturation-models/{name}-seed{seed}-fold{fold}.pt')
                epochs[name].append({'seed':seed,'fold':fold,'epoch_or_alpha':ep})
                if name=='ridge' and seed==SEEDS[0]:splits.append({'fold':fold,'test_clusters':sorted(set(rowg[te]))})
            allseed.append(out)
            print(name,seed,dr.macro_auroc(out,y,idx)[0],flush=True)
        preds[name]=np.mean(allseed,axis=0)
        np.savez_compressed(TOPIC/f'data/processed/g2-saturation-{name}-predictions.npz',seeds=SEEDS,predictions=allseed)
    # Reconstruct only the reviewed architecture, never execute downloaded script top level.
    raw=TOPIC/'data/raw/degformer-isolated'
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    for file,meta in manifest['files'].items():
        assert hashlib.sha256((raw/file).read_bytes()).hexdigest()==meta['sha256'],file
    tree=ast.parse((raw/'predict.py').read_text());node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PeptideTransformer')
    ns={'torch':torch,'nn':nn,'MAX_LEN':28};exec(compile(ast.Module(body=[node],type_ignores=[]),'reviewed-degformer-class','exec'),ns)
    ck=torch.load(raw/'peptide_model_epoch50.pt',map_location='cpu',weights_only=False)
    net=ns['PeptideTransformer'](21);net.load_state_dict(ck['model_state_dict']);net.eval()
    def dg(seqs):
        arr=[]
        with torch.no_grad():
            for i in range(0,len(seqs),128):
                t=torch.tensor([[rd.AAS.index(a) for a in s] for s in seqs[i:i+128]])
                arr.extend(net(t).numpy())
        return ck['control_scaler'].inverse_transform(np.array(arr).reshape(-1,1)).ravel()
    preds['Degformer']=dg(z['seqs'])-dg(z['wt'])
    training={r['sequence'] for r in csv.DictReader((raw/'training_data.csv').open())}
    overlap=[sum(s in training for s in z['seqs'][a:b]) for a,b in idx]
    per={k:dr.macro_auroc(v,y,idx)[1] for k,v in preds.items()}
    def compare(a,b):
        keep=[i for i in range(len(peps)) if per[a][i] is not None and per[b][i] is not None]
        delta=np.array([per[a][i]-per[b][i] for i in keep]);g=groups[keep];u=sorted(set(g));rng=np.random.default_rng(20261018)
        boot=[np.mean(np.concatenate([delta[g==c] for c in rng.choice(u,len(u),replace=True)])) for _ in range(5000)]
        return {'delta':float(delta.mean()),'ci95':np.quantile(boot,[.025,.975]).tolist(),'n_peptides':len(keep),'n_clusters':len(u)}
    result={'protocol':'5 outer cov80 folds, inner cov80 validation; 3 training seeds; no scan data used; exploratory development benchmark, not untouched external validation', 'seeds':SEEDS,'n_peptides':len(peps),'n_cells':len(y),'n_clusters':len(set(groups)),'macro_auroc':{k:dr.macro_auroc(v,y,idx)[0] for k,v in preds.items()},'comparisons':{b:compare('gate_pap',b) for b in preds if b!='gate_pap'},'degformer_overlap':{'mutant_cells_in_training':sum(overlap),'wt_peptides_in_training':sum(s in training for s in set(z['wt']))},'epochs':epochs,'folds':splits,'per_peptide':{str(p):{k:per[k][i] for k in per} for i,p in enumerate(peps)},'input_sha256':hashlib.sha256(cache.read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'versions':{'numpy':np.__version__,'torch':torch.__version__,'python':sys.version}}
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(TOPIC/'data/processed/g2-saturation-predictions.npz',**preds)
    print(json.dumps({k:v for k,v in result.items() if k in ['macro_auroc','comparisons','degformer_overlap']},indent=2),flush=True)
if __name__=='__main__':main()
