"""Real ESM35 CUDA equivalence tests for pause/resume, not efficacy measurements."""
import os
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
from pathlib import Path
import sys
import tempfile
import json
import gc
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

import numpy as np
import torch
from degron_v3.common import atomic_json
from degron_v3.data import Dataset
from degron_v3.finetune import MutationRegressor
from degron_v3.plm import Encoder
from degron_v3.local_control import Control, Paused, atomic_torch, load_torch, process_lock
from degron_v3.local_training import fit
from degron_v3.local_jobs import extract
from degron_v3.local_campaign import jobs


def main():
    torch.set_num_threads(2)
    ds=Dataset(HERE.parents[1]/'data/processed/v3-fullpsi')
    role=ds.role(ds.sat,0,17)
    train=ds.sat.loc[(role=='train')&(ds.sat.psi_wt_sat<=4)].head(32).copy()
    validation=ds.sat.loc[role=='validation'].head(16).copy()
    results=[]
    with tempfile.TemporaryDirectory(prefix='degron-local-validation-') as temporary:
        root=Path(temporary)
        for mode in ['frozen','lora']:
            states=[]
            for interrupted in [False,True]:
                campaign=root/(mode+str(interrupted));campaign.mkdir()
                control=Control(campaign,'matched-test',checkpoint_seconds=999999,log_seconds=999999)
                if interrupted:control.pause_after_steps=3
                model=MutationRegressor(Encoder('esm2_35m',[HERE/'output/weights'],'cuda','float32'),mode,17)
                try:epoch,loss=fit(model,train,validation,17,campaign/'fit.pt',control,epochs=2)
                except Paused:
                    saved=load_torch(campaign/'fit.pt');assert saved['cursor']==24 and saved['epoch']==1
                    del model;gc.collect();torch.cuda.empty_cache()
                    model=MutationRegressor(Encoder('esm2_35m',[HERE/'output/weights'],'cuda','float32'),mode,17)
                    epoch,loss=fit(model,train,validation,17,campaign/'fit.pt',Control(campaign,'matched-test'),epochs=2)
                states.append((model.learned_state(),epoch,loss))
                saved=load_torch(campaign/'fit.pt');assert saved['finished']
                # A finished checkpoint must return without performing any more optimizer steps.
                check=Control(campaign,'matched-test');fit(model,train,validation,17,campaign/'fit.pt',check,epochs=2)
                assert check.steps==0
                del model;gc.collect();torch.cuda.empty_cache()
            difference=max(float((states[0][0][k]-states[1][0][k]).abs().max()) for k in states[0][0])
            assert difference==0 and states[0][1:]==states[1][1:],(mode,difference)
            results.append(dict(test='real_cuda_pause_resume_'+mode,status='pass',max_abs_parameter_difference=difference,
                                same_best_epoch_and_validation_loss=True))
        path=root/'recover.pt';atomic_torch(path,{'identity':'test','value':1});atomic_torch(path,{'identity':'test','value':2})
        path.write_bytes(b'incomplete write')
        assert load_torch(path,'test')['value']==1
        results.append(dict(test='corrupt_latest_checkpoint_falls_back_to_previous',status='pass'))
        with process_lock(root/'lock'):
            try:
                with process_lock(root/'lock'):raise AssertionError('Duplicate lock succeeded')
            except RuntimeError:pass
        with process_lock(root/'lock'):pass
        results.append(dict(test='duplicate_session_rejected_and_lock_released',status='pass'))
        class StopAt16(Control):
            def log(self,message,force=False,**progress):
                if progress.get('rows',0)>=16:self.requested=True
        campaign=root/'extract';campaign.mkdir();atomic_json(campaign/'plan.json',dict(runtime='fixed-test'))
        # weights resolve against HERE/output/weights, so no download or source changes.
        for name in ['full','resumed']:(campaign/name).mkdir()
        frame=ds.sat.head(32)
        extract(ds,'esm2_35m',campaign,campaign/'full',Control(campaign,'extract'),frame=frame)
        try:extract(ds,'esm2_35m',campaign,campaign/'resumed',StopAt16(campaign,'extract'),frame=frame)
        except Paused:pass
        assert json.loads((campaign/'resumed/progress.json').read_text())['completed']==16
        extract(ds,'esm2_35m',campaign,campaign/'resumed',Control(campaign,'extract'),frame=frame)
        assert np.array_equal(np.load(campaign/'full/pool.npy'),np.load(campaign/'resumed/pool.npy'))
        results.append(dict(test='real_cuda_feature_prefix_resume',status='pass',rows=32))
        config=json.loads((HERE/'local-plan.json').read_text());planned=jobs(config)
        assert len({j['id'] for j in planned})==len(planned)
        known=set()
        for job in planned:assert set(job['deps'])<=known;known.add(job['id'])
        assert sum(j['kind']=='tune' for j in planned)==60
        assert sum(j['kind']=='ridge' for j in planned)==540
        results.append(dict(test='queue_complete_unique_and_topologically_ordered',status='pass',work_units=len(planned)))
    atomic_json(HERE/'local-runner-validation.json',dict(status='pass',scope='software_and_real_GPU_resume_not_scientific_results',
        torch=torch.__version__,cuda=torch.version.cuda,device=torch.cuda.get_device_name(0),tests=results))
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
