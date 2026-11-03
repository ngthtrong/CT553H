"""Tokenizer, CUDA and audited campaign-inheritance checks; no efficacy claims."""
import json
import gc
import os
from pathlib import Path
import subprocess
import sys
import tempfile

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
HERE = Path(__file__).resolve().parent
BASELINE_COMMIT = '907175572a5b344861e83eb4620bf440c893946e'
sys.path.insert(0, str(HERE))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf8')

import numpy as np
import torch
from tokenizers import Tokenizer
import sentencepiece as spm
from degron_v3.common import atomic_json, sha256
from degron_v3.plm import Encoder, load_tokenizer, specification, resolve_snapshot
from degron_v3.local_control import Control, fingerprint, process_lock, load_torch
from degron_v3 import local_campaign as campaign
from degron_v3.local_jobs import probe, artifact_directory
from degron_v3.local_control import Paused
from degron_v3.local_training import fit
from degron_v3.data import Dataset
from degron_v3.finetune import MutationRegressor


def tokenizer_checks(model):
    snapshot, _ = resolve_snapshot(model, [HERE/'output/local/weights'])
    encoder = Encoder.__new__(Encoder)
    encoder.spec = specification(model)
    encoder.device = torch.device('cpu')
    encoder.tokenizer = load_tokenizer(encoder.spec, snapshot)
    aas = 'ACDEFGHIKLMNPQRSTVWY'
    wt = (aas*2)[:28]
    mutants = [(i, wt[:i]+aa+wt[i+1:]) for i in range(28) for aa in aas if aa!=wt[i]]
    inputs, mask = encoder.encode_input([wt])
    base = inputs['input_ids'][mask].tolist()
    if model == 'prott5_encoder':
        reference = spm.SentencePieceProcessor(model_file=str(snapshot/'spiece.model'))
        expected = reference.encode(' '.join(wt), out_type=int)
    else:
        reference = Tokenizer.from_file(str(snapshot/'tokenizer.json'))
        encoded = reference.encode(list(wt), is_pretokenized=True)
        expected = [v for v,m in zip(encoded.ids, encoded.special_tokens_mask) if not m]
    assert base==expected and len(base)==28
    for start in range(0,len(mutants),8):
        batch=mutants[start:start+8]
        inputs, mask=encoder.encode_input([s for _,s in batch])
        ids=inputs['input_ids'][mask].reshape(len(batch),28).tolist()
        for (position,_), values in zip(batch,ids):
            assert [j for j,(a,b) in enumerate(zip(base,values)) if a!=b]==[position]
    for length in (27,29):
        try: encoder.encode_input([(aas*2)[:length]])
        except AssertionError: pass
        else: raise AssertionError('Invalid residue length accepted')
    return dict(test='tokenizer_'+model, status='pass', substitutions=len(mutants),
                residue_tokens=28, unknown_tokens=0, original_artifact_ids_equal=True,
                invalid_lengths_rejected=True)


def inheritance_checks():
    with tempfile.TemporaryDirectory(prefix='tokenizer-inheritance-') as temporary:
        root=Path(temporary)
        config=dict(models=['esm2_35m'],arms=['B','D'],seeds=[17,29,43],data='fixed')
        old=dict(config=config,code_sha256=campaign.TOKENIZER_REPAIR_SOURCE,
                 runtime=dict(versions=dict(torch='fixed')), data_identity='fixed',
                 registry_sha256='fixed',protocol_sha256='fixed',training={},features={},
                 selection='fixed',source_campaign='fixed')
        source=root/fingerprint(old)[:16];source.mkdir()
        atomic_json(source/'plan.json',old)
        job='extract-esm2_35m';p=source/'jobs'/job/'pool.npy';p.parent.mkdir(parents=True)
        np.save(p,np.arange(8,dtype=np.float32))
        paused='tune-lora-B-17-2';ck=source/'jobs'/paused/'inner.pt';ck.parent.mkdir(parents=True)
        torch.save(dict(identity='unchanged-checkpoint',cursor=24),ck)
        state=dict(plan_id=fingerprint(old),jobs={job:dict(status='complete',files=[dict(
            path=p.relative_to(source).as_posix(),bytes=p.stat().st_size,sha256=sha256(p))]),
            paused:dict(status='paused')})
        atomic_json(source/'state.json',state)
        before=sha256(source/'state.json')
        new={**old,'code_sha256':campaign.implementation_hash(),
             'features':dict(encoder_dtypes={'ankh_base':'float32'}),
             'config':{**config,'inherit_completed_from':source.name},
             'runtime':dict(versions=dict(torch='fixed',protobuf='6.33.5')),
             'inheritance_source':dict(plan_sha256=sha256(source/'plan.json'),state_sha256=before)}
        validation=dict(status='pass',target_code_sha256=campaign.implementation_hash())
        def target(name,plan):
            dst=root/name;dst.mkdir();atomic_json(dst/'plan.json',plan)
            atomic_json(dst/'state.json',dict(plan_id=fingerprint(plan),jobs={}))
            return dst
        dst=target('successor',new)
        campaign.inherit_unaffected(source,dst,validation)
        result=json.loads((dst/'state.json').read_text())['jobs'][job]
        assert campaign.complete_valid(dst,result)
        assert artifact_directory(dst,job)==p.parent
        assert Control(dst,paused).identity_campaign==source.name
        assert load_torch(dst/'jobs'/paused/'inner.pt','unchanged-checkpoint')['cursor']==24
        assert sha256(ck)==sha256(dst/'jobs'/paused/'inner.pt')
        assert sha256(source/'state.json')==before
        for field in ('data_identity','protocol_sha256','training'):
            wrong={**new,field:'changed'}
            try:campaign.inherit_unaffected(source,target('bad-'+field,wrong),validation)
            except AssertionError:pass
            else:raise AssertionError('Changed scientific setting accepted')
        p.write_bytes(b'corrupt')
        assert not campaign.complete_valid(dst,result)
        try:campaign.inherit_unaffected(source,target('corrupt',new),validation)
        except AssertionError:pass
        else:raise AssertionError('Corrupt completed artifact accepted')
    return dict(test='audited_inheritance',status='pass',source_unchanged=True,
                checkpoint_bytes_and_identity_preserved=True,changed_science_and_corrupt_artifact_rejected=True)


def unchanged_training_check():
    root=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
    name=(HERE/'degron_v3/local_training.py').relative_to(root).as_posix()
    baseline=subprocess.check_output(['git','show',BASELINE_COMMIT+':'+name],cwd=root).decode('utf8').replace('\r\n','\n')
    current=(HERE/'degron_v3/local_training.py').read_text(encoding='utf8')
    assert current.replace('control.identity_campaign','control.campaign.name')==baseline
    # All numerical components used for the inherited ESM35/Ridge results are unchanged.
    for filename in ('data.py','features.py','finetune.py','learning.py','metrics.py','neural.py','stages.py'):
        path=HERE/'degron_v3'/filename
        prior=subprocess.check_output(['git','show',BASELINE_COMMIT+':'+path.relative_to(root).as_posix()],cwd=root)
        assert path.read_bytes().replace(b'\r\n',b'\n')==prior.replace(b'\r\n',b'\n')
    return dict(test='inherited_numerical_code_unchanged',status='pass')


def cross_campaign_resume(ds, root):
    import shutil
    role=ds.role(ds.sat,0,17)
    train=ds.sat.loc[(role=='train')&(ds.sat.psi_wt_sat<=4)].head(32).copy()
    validation=ds.sat.loc[role=='validation'].head(16).copy()
    states=[]
    for interrupted in (False,True):
        source=root/('paused' if interrupted else 'continuous');source.mkdir()
        control=Control(source,'matched-lora',log_seconds=999999)
        if interrupted:control.pause_after_steps=2
        model=MutationRegressor(Encoder('esm2_35m',[HERE/'output/weights'],'cuda','float32'),'lora',17)
        try:result=fit(model,train,validation,17,source/'fit.pt',control,epochs=2)
        except Paused:
            target=root/'successor-checkpoint';target.mkdir()
            shutil.copytree(source,target,dirs_exist_ok=True)
            atomic_json(target/'inheritance.json',dict(checkpoint_campaigns={'matched-lora':source.name}))
            del model;gc.collect();torch.cuda.empty_cache()
            model=MutationRegressor(Encoder('esm2_35m',[HERE/'output/weights'],'cuda','float32'),'lora',17)
            result=fit(model,train,validation,17,target/'fit.pt',Control(target,'matched-lora'),epochs=2)
        states.append((model.learned_state(),result))
        del model;gc.collect();torch.cuda.empty_cache()
    difference=max(float((states[0][0][k]-states[1][0][k]).abs().max()) for k in states[0][0])
    assert difference==0 and states[0][1]==states[1][1]
    return dict(test='real_cuda_lora_checkpoint_successor_resume',status='pass',max_abs_parameter_difference=difference)


def main():
    results=[]
    with process_lock(HERE/'output/local/session.lock'), process_lock(HERE/'output/local/worker.lock'):
        torch.set_num_threads(2)
        torch.cuda.set_per_process_memory_fraction(.75)
        results.append(unchanged_training_check())
        results.extend(tokenizer_checks(m) for m in ('prott5_encoder','ankh_base'))
        results.append(inheritance_checks())
        ds=Dataset(HERE.parents[1]/'data/processed/degron-data-v3-fullpsi')
        with tempfile.TemporaryDirectory(prefix='tokenizer-cuda-') as temporary:
            results.append(cross_campaign_resume(ds,Path(temporary)))
            for model in ('prott5_encoder','ankh_base'):
                out=Path(temporary)/model;out.mkdir()
                probe(model,HERE/'output/local/validation-placeholder',out,Control(Path(temporary),model))
                report=json.loads((out/'preflight.json').read_text())['models'][0]
                results.append(dict(test='cuda_preflight_'+model,status='pass',report=report))
                torch.cuda.reset_peak_memory_stats()
                encoder=Encoder(model,[HERE/'output/local/weights'],'cuda','float16')
                frame=ds.sat.head(8)
                delta=encoder(frame.mutant_sequence.tolist())-encoder(frame.wt_sequence.tolist())
                assert delta.shape[:2]==(8,28) and np.isfinite(delta.astype('float16')).all()
                assert torch.cuda.max_memory_allocated()<=6*2**30
                results.append(dict(test='cuda_batch8_delta_'+model,status='pass',
                    encoder_dtype=str(encoder.dtype),float16_storage_finite=True,
                    peak_vram_bytes=torch.cuda.max_memory_allocated()))
                del encoder;gc.collect();torch.cuda.empty_cache()
    atomic_json(HERE/'tokenizer-repair-validation.json',dict(status='pass',
        scope='tokenizer_and_cuda_and_reuse_safety_not_benchmark_efficacy',
        target_code_sha256=campaign.implementation_hash(),script_sha256=sha256(__file__),tests=results))
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
