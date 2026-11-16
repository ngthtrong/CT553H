"""Meaningful CPU and real CUDA pause/resume checks on isolated W-only fixtures."""
import os
for name,value in [('OMP_NUM_THREADS','2'),('OPENBLAS_NUM_THREADS','2'),
                   ('CUBLAS_WORKSPACE_CONFIG',':4096:8'),('HF_HUB_OFFLINE','1'),('TRANSFORMERS_OFFLINE','1')]:
    os.environ.setdefault(name,value)
from pathlib import Path
import gc
import json
import sys
import uuid
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
V3=ROOT/'research/kaggle-roadmap-2026-10-31'
sys.path.insert(0,str(V3))
import numpy as np
import pandas as pd
import torch
from degron_v3.common import atomic_json
from degron_v3.data import Dataset
from degron_v3.finetune import MutationRegressor
from degron_v3.plm import Encoder
from degron_v3.local_control import Control,Paused,atomic_torch,load_torch,process_lock
from degron_v3.local_training import fit,predict
from degron_v3.local_campaign import jobs,resolve_campaign,pause,implementation_hash
from degron_v3.local_refit import read,FEATURES,ranking
from degron_v3.metrics import paired_ci


def main():
    tests=[];config=read(HERE/'refit-plan.json');planned=jobs(config)
    assert len(planned)==20 and sum(j['kind']=='refit' for j in planned)==6
    assert sum(j['kind']=='score-held' for j in planned)==6
    tests.append(dict(test='DAG_15_core_plus_5_completion_topological',status='pass'))
    origin=resolve_campaign('D:\\old\\topics\\degron-footprint\\research\\kaggle-roadmap-2026-10-31\\output\\local\\ef138c84579c842e')
    assert origin==V3/'output/local/ef138c84579c842e'
    try:resolve_campaign('../../outside')
    except ValueError:pass
    else:raise AssertionError('Unsafe selector accepted')
    tests.append(dict(test='legacy_path_relocated_and_outside_selector_rejected',status='pass'))
    a=pd.DataFrame(dict(peptide_id=['a','b','c','d'],group_id=['g1','g1','g1','g2'],mae=[1.,1.,4.,1.]))
    b=a.assign(mae=1.)
    stat=paired_ci(a,b,n_boot=5000,seed=1729,multiplicity=2)
    assert stat['delta']==.75 and stat['multiplicity']==2 and stat['clusters']==2
    assert stat['ci_adjusted']==[0.,1.]
    tests.append(dict(test='paired_group_bootstrap_preserves_peptide_weights',status='pass'))
    fixture=pd.DataFrame(dict(cell_id=['c','a','b'],peptide_id=['p']*3,group_id=['g']*3,dpsi_mean=[0.,0.,0.]))
    ranks=ranking(fixture,np.zeros(3))
    assert ranks.no_hit.all() and ranks.auroc.isna().all() and (ranks.k==3).all()
    tests.append(dict(test='no_hit_and_missing_classes_have_explicit_nulls',status='pass'))
    root=HERE/'local'/('validation-'+uuid.uuid4().hex);root.mkdir(parents=True)
    target=root/'pause-target';target.mkdir()
    atomic_json(target/'state.json',dict(jobs={}))
    with process_lock(root/'worker.lock'):
        assert pause(target,wait=True,timeout=0)==2
    assert pause(target,wait=True,timeout=1)==0
    tests.append(dict(test='pause_wait_does_not_claim_success_while_worker_locked',status='pass'))
    path=root/'fallback.pt';atomic_torch(path,dict(identity='fixed',value=1));atomic_torch(path,dict(identity='fixed',value=2))
    path.write_bytes(b'interrupted write');assert load_torch(path,'fixed')['value']==1
    try:load_torch(path,'changed')
    except ValueError:pass
    else:raise AssertionError('Checkpoint identity bypassed')
    tests.append(dict(test='corrupt_checkpoint_fallback_and_identity_mismatch_rejection',status='pass'))
    ds=Dataset(ROOT/config['data']);train=ds.sat.head(32).copy()
    torch.set_num_threads(2);torch.cuda.set_per_process_memory_fraction(.75)
    for mode in ['frozen','lora']:
        states=[]
        for interrupted in [False,True]:
            campaign=root/(mode+str(interrupted));campaign.mkdir()
            control=Control(campaign,'fixed-refit',checkpoint_seconds=99999,log_seconds=99999)
            if interrupted:control.pause_after_steps=3
            model=MutationRegressor(Encoder('esm2_8m',[V3/'output/local/weights',V3/'output/weights'],'cuda','float32'),mode,17)
            try:fit(model,train,train.iloc[:0],17,campaign/'refit.pt',control,epochs=2,refit=True)
            except Paused:
                saved=load_torch(campaign/'refit.pt');assert saved['cursor']==24
                del model;gc.collect();torch.cuda.empty_cache()
                model=MutationRegressor(Encoder('esm2_8m',[V3/'output/local/weights',V3/'output/weights'],'cuda','float32'),mode,17)
                fit(model,train,train.iloc[:0],17,campaign/'refit.pt',Control(campaign,'fixed-refit'),epochs=2,refit=True)
            assert load_torch(campaign/'refit.pt')['finished']
            check=Control(campaign,'fixed-refit')
            fit(model,train,train.iloc[:0],17,campaign/'refit.pt',check,epochs=2,refit=True);assert check.steps==0
            states.append(model.learned_state());del model;gc.collect();torch.cuda.empty_cache()
        difference=max(float((states[0][key]-states[1][key]).abs().max()) for key in states[0])
        assert difference==0,(mode,difference)
        tests.append(dict(test='real_CUDA_fixed_epoch_refit_resume_'+mode,status='pass',max_parameter_difference=difference))
    campaign=root/'prediction';campaign.mkdir()
    model=MutationRegressor(Encoder('esm2_8m',[V3/'output/local/weights',V3/'output/weights'],'cuda','float32'),'lora',17)
    continuous=predict(model,train[FEATURES],campaign/'full.npy',Control(campaign,'score'))
    class StopAt16(Control):
        def log(self,message,force=False,**progress):
            if progress.get('rows',0)>=16:self.requested=True
    try:predict(model,train[FEATURES],campaign/'resumed.npy',StopAt16(campaign,'score'))
    except Paused:pass
    assert read(campaign/'resumed.json')['completed']==16
    resumed=predict(model,train[FEATURES],campaign/'resumed.npy',Control(campaign,'score'))
    assert np.array_equal(continuous,resumed)
    tests.append(dict(test='real_CUDA_prediction_prefix_resume',status='pass',rows=32))
    del model;gc.collect();torch.cuda.empty_cache()
    atomic_json(HERE/'refit-validation.json',dict(status='pass',scope='software_only_W_fixture_not_benchmark',
        code_sha256=implementation_hash(),tests=tests,cuda_device=torch.cuda.get_device_name(0),
        temporary_artifacts=root.relative_to(ROOT).as_posix(),T_outcomes_read=False))
    print(json.dumps(tests,indent=2))


if __name__=='__main__':
    base=V3/'output/local'
    with process_lock(base/'session.lock'):
        with process_lock(base/'worker.lock'):
            main()
