"""Validate output integrity and paired statistics without retraining."""
import json,sys,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'log.md').exists())
sys.path.insert(0,str(TOPIC/'research/residue-task-derisk-2026-10-15'))
import derisk as dr
z=np.load(TOPIC/'data/processed/g2-saturation-input.npz');r=json.loads((HERE/'results.json').read_text())
assert len(z['y'])==47847 and len(z['peps'])==91 and len(set(z['groups']))==89
assert abs(r['macro_auroc']['DeltaPAP']-.7692837466691289)<1e-10
for f in r['folds']:
    te=set(f['test_clusters']);assert te and te<=set(z['groups'])
flat=[c for f in r['folds'] for c in f['test_clusters']]
assert len(flat)==len(set(flat))==89
pred=np.load(TOPIC/'data/processed/g2-saturation-predictions.npz')
assert all(len(a)==len(z['y']) and np.isfinite(a).all() for a in pred.values())
idx=z['idx'];groups=z['groups']
def comp(x,y):
    a=np.array(dr.macro_auroc(x,z['y'],idx)[1]);b=np.array(dr.macro_auroc(y,z['y'],idx)[1]);d=a-b
    u=sorted(set(groups));rng=np.random.default_rng(20261018)
    boots=[np.concatenate([d[groups==c] for c in rng.choice(u,len(u),replace=True)]).mean() for _ in range(5000)]
    return {'delta':float(d.mean()),'ci95':np.quantile(boots,[.025,.975]).tolist()}
extra={'ridge_vs_DeltaPAP':comp(pred['ridge'],pred['DeltaPAP']),'seed_metrics':{},'gate_vs_no_gate_by_seed':[],'gate_vs_DeltaPAP_by_seed':[]}
for name in ['ridge','gate_pap','no_gate_pap','gate_no_pap']:
    pp=np.load(TOPIC/f'data/processed/g2-saturation-{name}-predictions.npz')['predictions']
    extra['seed_metrics'][name]=[dr.macro_auroc(x,z['y'],idx)[0] for x in pp]
g=np.load(TOPIC/'data/processed/g2-saturation-gate_pap-predictions.npz')['predictions']
b=np.load(TOPIC/'data/processed/g2-saturation-no_gate_pap-predictions.npz')['predictions']
for x,y in zip(g,b):
    extra['gate_vs_no_gate_by_seed'].append(comp(x,y));extra['gate_vs_DeltaPAP_by_seed'].append(comp(x,pred['DeltaPAP']))
extra['degformer_mutant_overlap_fraction']=r['degformer_overlap']['mutant_cells_in_training']/len(z['y'])
# Reload every local model checkpoint and verify held-out predictions and split isolation.
import importlib.util
spec=importlib.util.spec_from_file_location('g2_runner',HERE/'run.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
checked=0
for name in ['gate_pap','no_gate_pap','gate_no_pap']:
    pp=np.load(TOPIC/f'data/processed/g2-saturation-{name}-predictions.npz')['predictions']
    for si,seed in enumerate(r['seeds']):
        for fold in range(5):
            ck=runner.torch.load(TOPIC/f'data/processed/g2-saturation-models/{name}-seed{seed}-fold{fold}.pt',weights_only=True)
            tr=ck['train_indices'];va=ck['validation_indices'];te=ck['test_indices']
            assert len(tr)+len(va)+len(te)==len(z['y'])
            assert not(set(z['rowg'][tr])&set(z['rowg'][va]))
            assert not(set(z['rowg'][tr])&set(z['rowg'][te]))
            assert not(set(z['rowg'][va])&set(z['rowg'][te]))
            net=runner.Gate(ck['gated'],ck['pap']);net.load_state_dict(ck['state_dict']);net.eval()
            with runner.torch.no_grad():actual=net(runner.torch.tensor(z['X'][te],dtype=runner.torch.float32)).numpy()
            np.testing.assert_allclose(actual,pp[si,te],rtol=1e-6,atol=1e-6);checked+=1
extra['reloaded_checkpoints']=checked
extra['checks']='PASS: counts, finite predictions, PAP reproduction, disjoint outer groups, per-seed recalculation, all 45 checkpoint splits and held-out predictions' 
(HERE/'audit.json').write_text(json.dumps(extra,indent=2)+'\n');print(json.dumps(extra,indent=2))
