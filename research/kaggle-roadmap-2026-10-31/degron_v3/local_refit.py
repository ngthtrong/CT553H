"""Final W refit and post-hoc held-source evaluation inside the local runner.

No supervisor here: scheduling, OS locks, deadline, STOP and checkpoint recovery
remain owned by local_campaign/local_control/local_training.
"""
from collections import Counter
import gc
import hashlib
import json
from pathlib import Path
import shutil
import time

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

from .common import atomic_json, sha256
from .data import Dataset
from .finetune import MutationRegressor, infer
from .local_control import Control, atomic_torch, fingerprint, load_torch
from .local_training import fit, predict, model_digest
from .metrics import paired_ci, per_peptide, summarize
from .plm import Encoder

V3 = Path(__file__).resolve().parents[1]
ROOT = next(p for p in V3.parents if (p/'CLAUDE.md').is_file())
PROJECT = ROOT/'research/lora-refit-transfer-2026-11-16'
LOCAL = V3/'output/local'
FEATURES = ['cell_id','peptide_id','group_id','wt_sequence','mutant_sequence',
            'position_1based','wt_aa','mut_aa']
STATUS = 'development_not_gate_closure'
CORE_KINDS = {'refit','score-held','calibrate-final','aggregate-refit'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def repo_path(value):
    path = (ROOT/value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f'Input outside repository: {value}')
    return path


def ids_hash(values):
    return fingerprint(sorted(map(str, values)))


def config_inputs(config):
    assert config['campaign_kind']=='refit_transfer_v1'
    assert config['models']==['esm2_35m'] and config['arms']==['D']
    assert config['modes']==['lora','frozen'] and config['seeds']==[17,29,43]
    assert config['expected_W']==dict(cells=122412,peptides=235,groups=221)
    assert config['expected_T']==dict(cells=39234,peptides=1410,groups=730)
    assert config['bootstrap']==dict(replicates=5000,seed=1729,multiplicity=2)
    lock = read(repo_path(config['source_lock']))
    assert lock['data_identity']==config['data_identity']
    assert lock['epochs']=={'lora':{'17':2,'29':2,'43':2},'frozen':{'17':1,'29':2,'43':2}}
    assert config['scope']=='core_and_available_completion'
    return lock


def verify_sources(lock):
    for entry in lock['files']:
        path = repo_path(entry['path'])
        if not path.is_file() or path.stat().st_size!=entry['bytes'] or sha256(path)!=entry['sha256']:
            raise ValueError(f'Pinned source changed/missing: {entry["path"]}')


def cohort(ds, expected=None, labels=False):
    # Filtering for rep1 availability is fixed in the protocol, never score based.
    columns = FEATURES+['partition','dpsi_rep1']
    if labels:
        columns += ['dpsi_rep2','dpsi_rep12_mean','scan_pair']
    frame = pd.read_parquet(ds.root/'tables/scanning-cells.parquet',columns=columns)
    frame = frame.loc[(frame.partition=='scan_T') & frame.dpsi_rep1.notna()].copy()
    assert not frame.cell_id.duplicated().any()
    assert not set(frame.group_id)&set(ds.sat.group_id), 'T groups entered W'
    if expected is not None:
        actual = dict(cells=len(frame),peptides=frame.peptide_id.nunique(),groups=frame.group_id.nunique())
        assert actual==expected, (actual,expected)
    if labels:
        frame['dpsi_mean']=frame.dpsi_rep1
        wt = frame.peptide_id.map(ds.peptides.set_index('peptide_id').psi_wt_scan_rep1)
        assert wt.notna().all()
        frame['psi_wt_scan_rep1']=wt
        frame['psi_stratum']=pd.cut(wt,[-np.inf,3,4,5,np.inf],labels=['le3','gt3_le4','gt4_le5','gt5']).astype(str)
        return frame.reset_index(drop=True)
    # Target columns do not leave this function on any model inference path.
    return frame[FEATURES].reset_index(drop=True)


def oof_ensemble(ds, lock, mode):
    values=[]
    for seed in [17,29,43]:
        rows=[]
        for entry in lock['folds']:
            if entry['mode']==mode and entry['seed']==seed:
                rows.append(pd.read_parquet(repo_path(entry['oof'])))
        assert len(rows)==5
        raw=pd.concat(rows,ignore_index=True)
        assert not raw.cell_id.duplicated().any()
        assert set(raw.cell_id)==set(ds.sat.cell_id)
        assert set(raw.seed)=={seed} and set(raw.recipe)=={f'esm2_35m-{mode}-D'}
        assert set(raw.data_identity)=={ds.identity}
        raw=raw.set_index('cell_id').loc[ds.sat.cell_id]
        assert np.allclose(raw.dpsi_mean.to_numpy(),ds.sat.dpsi_mean.to_numpy(),atol=0,rtol=0)
        assert np.isfinite(raw.prediction).all()
        values.append(raw.prediction.to_numpy())
    return np.mean(values,axis=0)


def jobs(config):
    config_inputs(config)
    items=[]
    for mode in config['modes']:
        for seed in config['seeds']:
            items.append(dict(id=f'refit-{mode}-D-{seed}',kind='refit',mode=mode,seed=seed,deps=[]))
    for mode in config['modes']:
        items.append(dict(id=f'calibrate-final-{mode}-D',kind='calibrate-final',mode=mode,deps=[]))
    for mode in config['modes']:
        for seed in config['seeds']:
            items.append(dict(id=f'score-held-{mode}-D-{seed}',kind='score-held',mode=mode,seed=seed,
                              deps=[f'refit-{mode}-D-{seed}']))
    items.append(dict(id='aggregate-refit',kind='aggregate-refit',deps=[j['id'] for j in items]))
    items += [dict(id='model-card-parity',kind='model-card-parity',phase='completion',deps=['aggregate-refit']),
              dict(id='analyze-errors',kind='analyze-errors',phase='completion',deps=['aggregate-refit']),
              dict(id='koren-rank-only',kind='koren-rank-only',phase='completion',deps=['aggregate-refit']),
              dict(id='figure-export',kind='figure-export',phase='completion',deps=['analyze-errors']),
              dict(id='finalize-branch1',kind='finalize-branch1',phase='completion',
                   deps=['model-card-parity','analyze-errors','figure-export'])]
    assert len(items)==20 and len({j['id'] for j in items})==20
    known=set()
    for job in items:
        assert set(job['deps'])<=known
        known.add(job['id'])
    return items


def preflight(config_path, gpu=True):
    from .local_campaign import implementation_hash, runtime_identity
    config=read(config_path);lock=config_inputs(config);verify_sources(lock)
    ds=Dataset(repo_path(config['data']))
    assert ds.identity==config['data_identity']
    actual=dict(cells=len(ds.sat),peptides=ds.sat.peptide_id.nunique(),groups=ds.sat.group_id.nunique())
    assert actual==config['expected_W']
    held=cohort(ds,config['expected_T'])
    assert ids_hash(held.cell_id)==lock['T_cell_ids_sha256']
    free=shutil.disk_usage(LOCAL).free
    used=sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file())
    assert free>=35*2**30 and used+5*2**30<=50*2**30, 'Disk reserve/budget exceeded'
    for mode in config['modes']:
        oof_ensemble(ds,lock,mode)
    record=dict(status='pass',observed_unix=time.time(),scope='core_and_available_completion',
        config_sha256=sha256(config_path),source_lock_sha256=sha256(repo_path(config['source_lock'])),
        protocol_sha256=sha256(repo_path(config['protocol'])),code_sha256=implementation_hash(),
        runtime=runtime_identity(),W=actual,T=config['expected_T'],T_cell_ids_sha256=ids_hash(held.cell_id),
        disk_free_bytes=free,local_used_bytes=used,koren_status='missing_input_pending',
        scientific_status=STATUS,gpu_forward_backward=False)
    assert record['runtime']['cuda'], 'CUDA required; CPU fallback is forbidden'
    if gpu:
        torch.set_num_threads(2);torch.cuda.set_per_process_memory_fraction(.75)
        tests=[]
        for mode in config['modes']:
            model=MutationRegressor(Encoder('esm2_35m',[V3/'output/weights',LOCAL/'weights'],'cuda','float32'),mode,17)
            frame=ds.sat.head(8)
            target=torch.as_tensor(frame.dpsi_mean.to_numpy(),dtype=torch.float32,device='cuda')
            loss=((model(frame[FEATURES])-target)**2).mean()
            assert torch.isfinite(loss)
            loss.backward()
            grads=[p.grad for p in model.parameters() if p.requires_grad and p.grad is not None]
            assert grads and all(torch.isfinite(g).all() for g in grads)
            tests.append(dict(mode=mode,finite_loss=float(loss.detach().cpu()),
                              peak_allocated_bytes=torch.cuda.max_memory_allocated()))
            del model,loss,target,grads;gc.collect();torch.cuda.empty_cache()
        record.update(gpu_forward_backward=True,gpu_tests=tests)
    atomic_json(PROJECT/'preflight.json',record)
    return record


def initialize(config_path):
    from .local_campaign import implementation_hash, runtime_identity
    config=read(config_path);lock=config_inputs(config);verify_sources(lock)
    check=read(PROJECT/'preflight.json')
    assert check['status']=='pass' and check['gpu_forward_backward'], 'Run GPU preflight first'
    assert check['config_sha256']==sha256(config_path)
    assert check['code_sha256']==implementation_hash() and check['runtime']==runtime_identity(), 'Rerun preflight after code/runtime changes'
    assert check['source_lock_sha256']==sha256(repo_path(config['source_lock']))
    assert check['protocol_sha256']==sha256(repo_path(config['protocol']))
    plan=dict(schema_version=2,config=config,data_identity=config['data_identity'],
        code_sha256=implementation_hash(),runtime=check['runtime'],
        protocol_sha256=check['protocol_sha256'],source_lock_sha256=check['source_lock_sha256'],
        registry_sha256=sha256(V3/'model-registry.json'),scientific_status=STATUS,
        source_campaign=lock['source_campaign'],training=dict(batch=8,dtype='float32',lr=.0001,
            weight_decay=.01,clip_grad=1.,refit=True,epochs=lock['epochs'],early_stopping=False))
    identity=fingerprint(plan);campaign=LOCAL/identity[:16]
    campaign.mkdir(parents=True,exist_ok=True)
    if (campaign/'plan.json').exists():
        assert read(campaign/'plan.json')==plan
        assert read(campaign/'queue.json')==jobs(config)
    else:
        atomic_json(campaign/'plan.json',plan);atomic_json(campaign/'queue.json',jobs(config))
        atomic_json(campaign/'state.json',dict(plan_id=identity,jobs={},scientific_status=STATUS))
    atomic_json(LOCAL/'latest.json',dict(campaign_id=campaign.name,campaign=str(campaign),plan_id=identity))
    return campaign


def load_model(campaign,mode,seed):
    path=campaign/'jobs'/f'refit-{mode}-D-{seed}'/'model.pt'
    saved=torch.load(path,map_location='cpu',weights_only=True)
    assert saved['campaign']==campaign.name and saved['mode']==mode and saved['seed']==seed
    model=MutationRegressor(Encoder('esm2_35m',[V3/'output/weights',LOCAL/'weights'],'cuda','float32'),mode,seed)
    assert model.encoder.lock['revision']==saved['base_revision']
    model.restore(saved['learned_state'])
    assert model_digest(model)==saved['learned_state_sha256']
    return model,saved


def probabilities(cal,prediction):
    out=np.zeros((len(prediction),3),dtype=float)
    out[:,cal.classes_.astype(int)]=cal.predict_proba(np.asarray(prediction).reshape(-1,1))
    assert np.isfinite(out).all() and np.allclose(out.sum(1),1)
    return out


def events(y):
    return np.where(np.asarray(y)<=-1,0,np.where(np.asarray(y)>=1,2,1))


def refit(ds,job,campaign,out,control,lock):
    mode,seed=job['mode'],job['seed'];epochs=lock['epochs'][mode][str(seed)]
    model=MutationRegressor(Encoder('esm2_35m',[V3/'output/weights',LOCAL/'weights'],'cuda','float32'),mode,seed)
    initial=model.learned_state()
    epoch,_=fit(model,ds.sat,ds.sat.iloc[:0],seed,out/'refit.pt',control,epochs=epochs,refit=True)
    assert epoch==epochs
    learned=model.learned_state()
    changed=[name for name in learned if not torch.equal(learned[name],initial[name])]
    assert changed and (mode!='lora' or any('lora_' in name for name in changed))
    model_id=f'esm2_35m-{mode}-D-seed{seed}-refit-{campaign.name}'
    model_path=out/'model.pt'
    metadata=dict(schema_version=1,model_id=model_id,model='esm2_35m',mode=mode,seed=seed,
        campaign=campaign.name,data_identity=ds.identity,base_revision=model.encoder.lock['revision'],
        epochs=epochs,train_cell_ids_sha256=ids_hash(ds.sat.cell_id),train_group_ids_sha256=ids_hash(ds.sat.group_id.unique()),
        learned_state_sha256=model_digest(model))
    if model_path.exists():
        previous=torch.load(model_path,map_location='cpu',weights_only=True)
        assert previous['learned_state_sha256']==metadata['learned_state_sha256']
    else:
        atomic_torch(model_path,dict(**metadata,learned_state=learned))
    atomic_json(out/'fit.json',dict(**metadata,train_cells=len(ds.sat),train_peptides=ds.sat.peptide_id.nunique(),
        train_groups=ds.sat.group_id.nunique(),validation_cells=0,T_fit_cells=0,
        epoch_policy='per_seed_median_of_five_source_selected_epochs',changed_parameters=changed))
    # In-sample W predictions are only for the score-shift diagnostic, never calibration.
    predict(model,ds.sat[FEATURES],out/'final-w.npy',control)


def calibrate(ds,job,out,lock):
    mode=job['mode'];p=oof_ensemble(ds,lock,mode)
    cal=LogisticRegression(C=1.,max_iter=1000).fit(p.reshape(-1,1),events(ds.sat.dpsi_mean))
    joblib.dump(cal,out/'final-calibrator.joblib')
    atomic_json(out/'calibration.json',dict(recipe=f'esm2_35m-{mode}-D',fit_population='ensemble_OOF_W',
        train_cells=len(ds.sat),train_cell_ids_sha256=ids_hash(ds.sat.cell_id),T_fit_cells=0,
        ensemble_order='mean_raw_three_seeds_then_calibrate',classes=cal.classes_.tolist(),
        prediction_sha256=hashlib.sha256(p.tobytes()).hexdigest(),
        warning='Final refit score shift is evaluated, not fitted away with T.'))


def score(ds,job,campaign,out,control,config,lock):
    frame=cohort(ds,config['expected_T']);assert ids_hash(frame.cell_id)==lock['T_cell_ids_sha256']
    model,saved=load_model(campaign,job['mode'],job['seed'])
    p=predict(model,frame,out/'held.npy',control)
    assert len(p)==config['expected_T']['cells'] and np.isfinite(p).all()
    atomic_json(out/'score.json',dict(model_id=saved['model_id'],cells=len(p),
        cell_ids_sha256=ids_hash(frame.cell_id),input_columns=list(frame.columns),target_columns_passed_to_model=[],
        prediction_sha256=sha256(out/'held.npy')))


def ranking(frame,prediction):
    rows=[]
    frame=frame.assign(prediction=prediction)
    for peptide,sub in frame.groupby('peptide_id',sort=True):
        y=sub.dpsi_mean.to_numpy();p=sub.prediction.to_numpy()
        tie=np.asarray([hashlib.sha256(json.dumps([1729,str(peptide),str(cell)],ensure_ascii=False,
                          separators=(',',':')).encode()).hexdigest() for cell in sub.cell_id])
        for direction,labels,scores in [('plus',y>=1,p),('minus',y<=-1,-p)]:
            k=min(10,len(sub));order=np.lexsort((tie,-scores));count=int(labels.sum())
            eligible=min(count,len(sub)-count)>=3
            rows.append(dict(peptide_id=peptide,group_id=sub.group_id.iloc[0],direction=direction,n=len(sub),
                k=k,hits=count,prevalence=float(labels.mean()),no_hit=count==0,
                precision_at_k=float(labels[order[:k]].mean()),
                auroc=float(roc_auc_score(labels,scores)) if eligible else None,
                ap=float(average_precision_score(labels,scores)) if eligible else None,
                null_reason=None if eligible else 'fewer_than_three_members_in_one_class'))
    return pd.DataFrame(rows)


def probability_metrics(y,probs):
    cls=events(y);result=dict(cells=len(y),brier_three_class=float(np.square(probs-np.eye(3)[cls]).sum(1).mean()))
    for name,index in [('minus',0),('plus',2)]:
        observed=(cls==index).astype(float);p=probs[:,index];bins=np.minimum((p*10).astype(int),9)
        ece=0.;counts=[]
        for b in range(10):
            mask=bins==b;n=int(mask.sum())
            counts.append(n)
            if n:ece+=n/len(y)*abs(float(p[mask].mean()-observed[mask].mean()))
        result[name]=dict(ece=ece,prevalence=float(observed.mean()),bins=counts)
    return result


def aggregate(ds,campaign,out,control,config,lock):
    held=cohort(ds,config['expected_T'],labels=True)
    baseline=pd.read_parquet(repo_path(lock['w5_baseline']))
    assert not baseline.cell_id.duplicated().any() and set(baseline.cell_id)==set(held.cell_id)
    baseline=baseline.set_index('cell_id').loc[held.cell_id]
    assert np.allclose(baseline.dpsi_mean.to_numpy(),held.dpsi_mean.to_numpy(),atol=0,rtol=0)
    predictions={'ordered-w5-D':baseline.prediction.to_numpy(),
                 'zero':np.zeros(len(held)),'constant-W-mean':np.full(len(held),ds.sat.dpsi_mean.mean())}
    prob={'ordered-w5-D':baseline[['p_minus','p_neutral','p_plus']].to_numpy()}
    seed_reports={};shift={}
    for mode in config['modes']:
        recipe=f'esm2_35m-{mode}-D';values=[];wv=[]
        seed_reports[recipe]={}
        for seed in config['seeds']:
            p=np.load(campaign/'jobs'/f'score-held-{mode}-D-{seed}'/'held.npy')
            values.append(p);wv.append(np.load(campaign/'jobs'/f'refit-{mode}-D-{seed}'/'final-w.npy'))
            control.check();seed_reports[recipe][str(seed)]=summarize(held,p)
        predictions[recipe]=np.mean(values,axis=0)
        cal=joblib.load(campaign/'jobs'/f'calibrate-final-{mode}-D'/'final-calibrator.joblib')
        prob[recipe]=probabilities(cal,predictions[recipe])
        oof=oof_ensemble(ds,lock,mode);finalw=np.mean(wv,axis=0)
        shift[recipe]=dict(OOF_W_mean=float(oof.mean()),final_W_in_sample_mean=float(finalw.mean()),
            T_mean=float(predictions[recipe].mean()),
            OOF_W_quantiles=np.quantile(oof,[.01,.1,.5,.9,.99]).tolist(),
            final_W_in_sample_quantiles=np.quantile(finalw,[.01,.1,.5,.9,.99]).tolist(),
            T_quantiles=np.quantile(predictions[recipe],[.01,.1,.5,.9,.99]).tolist(),
            warning='Final W predictions are in-sample; no score correction fitted.')
    pp={};reports={};ranks={};replicates={}
    local_ensemble=held[['cell_id','peptide_id','group_id']].copy()
    for recipe,p in predictions.items():
        control.check();assert len(p)==len(held) and np.isfinite(p).all()
        pp[recipe]=per_peptide(held,p);reports[recipe]=summarize(held,p)
        pp[recipe].to_csv(out/f'{recipe}-per-peptide.csv',index=False)
        ranks[recipe]=ranking(held,p)
        ranks[recipe].to_csv(out/f'{recipe}-ranking.csv',index=False)
        local_ensemble[recipe]=p
        available=held[['dpsi_rep1','dpsi_rep2']].notna().all(axis=1)
        replicates[recipe]={}
        for column in ['dpsi_rep1','dpsi_rep2','dpsi_rep12_mean']:
            sub=held.loc[available].copy();sub['dpsi_mean']=sub[column]
            replicates[recipe][column]=summarize(sub,p[available.to_numpy()])
    local_ensemble.to_parquet(out/'ensemble-held.parquet',index=False)
    contrasts={}
    for other in ['esm2_35m-frozen-D','ordered-w5-D']:
        control.check();name='esm2_35m-lora-D_minus_'+other;dest=out/(name+'-ci.json')
        if dest.exists():result=read(dest)
        else:
            result=paired_ci(pp['esm2_35m-lora-D'],pp[other],n_boot=5000,seed=1729,multiplicity=2)
            atomic_json(dest,result)
        contrasts[name]=result
    rank_summary={}
    for recipe,frame in ranks.items():
        rank_summary[recipe]={direction:dict(peptides=len(sub),no_hit_peptides=int(sub.no_hit.sum()),
            macro_precision_at_min10=float(sub.precision_at_k.mean()),macro_prevalence=float(sub.prevalence.mean()),
            auroc_eligible_peptides=int(sub.auroc.notna().sum()),ap_eligible_peptides=int(sub.ap.notna().sum()))
            for direction,sub in frame.groupby('direction')}
    result=dict(schema_version=1,campaign=campaign.name,scientific_status=STATUS,
        evaluation='posthoc_transfer_on_previously_examined_held_source',primary_endpoint='peptide_macro_MAE_T_rep1',
        denominators=config['expected_T'],metrics=reports,per_seed=seed_reports,contrasts=contrasts,
        probability_metrics={name:probability_metrics(held.dpsi_mean.to_numpy(),p) for name,p in prob.items()},
        ranking=rank_summary,replicate_intersection=replicates,score_shift=shift,
        constant_W_mean=float(ds.sat.dpsi_mean.mean()),
        limitations=['T was previously examined; not independent external validation.',
            'Bootstrap conditions on fitted predictions and does not include training/selection uncertainty.',
            'Secondary metrics, strata and diagnostics are exploratory; no global multiplicity correction.',
            'No automatic serving promotion or G2/G3 closure.'])
    atomic_json(out/'results.json',result)
    atomic_json(PROJECT/'results.json',result)


def parity(ds,campaign,out,control,config):
    fixture=ds.sat[FEATURES].head(32).copy();values=[];tests=[];models=[]
    for seed in config['seeds']:
        model,saved=load_model(campaign,'lora',seed)
        first=predict(model,fixture,out/f'seed{seed}.npy',control)
        del model;gc.collect();torch.cuda.empty_cache()
        reloaded,_=load_model(campaign,'lora',seed)
        second=infer(reloaded,fixture,batch=8)
        assert np.allclose(first,second,atol=1e-5,rtol=1e-5)
        tests.append(dict(seed=seed,max_absolute_difference=float(np.max(abs(first-second))),rows=len(fixture)))
        path=campaign/'jobs'/f'refit-lora-D-{seed}'/'model.pt'
        models.append(dict(model_id=saved['model_id'],seed=seed,epochs=saved['epochs'],
                           path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=sha256(path)))
        values.append(second);del reloaded;gc.collect();torch.cuda.empty_cache()
    calpath=campaign/'jobs/calibrate-final-lora-D/final-calibrator.joblib'
    cal=joblib.load(calpath);probs=probabilities(cal,np.mean(values,axis=0))
    assert np.isfinite(probs).all()
    report=dict(status='pass',tests=tests,scope='checkpoint reload, resumable predict vs finetune.infer on same runtime',
        atol=1e-5,rtol=1e-5,coordinate_contract='1-based residue; WT/mutant amino acids; exact 28-aa inputs',
        cross_runtime_parity='pending_on_primary_machine')
    atomic_json(out/'parity-results.json',report);atomic_json(PROJECT/'parity-results.json',report)
    card=dict(schema_version=1,campaign=campaign.name,scientific_status=STATUS,model_ids=[x['model_id'] for x in models],
        models=models,ensemble='mean raw predictions of seeds 17,29,43, then calibrate',
        base_model='facebook/esm2_t12_35M_UR50D',base_revision=read(V3/'output/weights/esm2_35m/status.json')['revision'],
        adapter=dict(rank=8,alpha=16,targets=['query','value']),dtype='float32',batch=8,
        features='delta-site embedding + delta-mean embedding + composition/pair 60',
        calibrator=dict(path=calpath.relative_to(ROOT).as_posix(),sha256=sha256(calpath),fit='ensemble OOF W only'),
        parity=report,claim_boundary='Reporter mutation effects; previously explored same-source transfer; not clinical validation.',
        serving_promotion='not_authorized_by_research_execution',G2_G3='not_closed')
    atomic_json(out/'model-card.json',card);atomic_json(PROJECT/'model-card.json',card)


def errors(ds,campaign,out,control):
    config=read(campaign/'plan.json')['config'];held=cohort(ds,config['expected_T'],labels=True)
    values=pd.read_parquet(campaign/'jobs/aggregate-refit/ensemble-held.parquet').set_index('cell_id').loc[held.cell_id]
    rows=[]
    for name in values.columns:
        if name in ['peptide_id','group_id']:continue
        p=values[name].to_numpy()
        for stratum,sub in held.groupby('psi_stratum',sort=True):
            control.check();idx=sub.index.to_numpy();e=p[idx]-sub.dpsi_mean.to_numpy()
            rows.append(dict(recipe=name,stratum=stratum,cells=len(sub),peptides=sub.peptide_id.nunique(),
                groups=sub.group_id.nunique(),signed_bias=float(e.mean()),cell_MAE=float(abs(e).mean()),
                target_mean=float(sub.dpsi_mean.mean()),prediction_mean=float(p[idx].mean()),
                positive_prevalence=float((sub.dpsi_mean>=1).mean()),negative_prevalence=float((sub.dpsi_mean<=-1).mean())))
    table=pd.DataFrame(rows);table.to_csv(out/'error-strata.csv',index=False)
    table.to_csv(PROJECT/'error-strata.csv',index=False)
    result=dict(status='descriptive_not_causal',strata=rows,
        hypotheses=dict(target_distribution='signed residual/prevalence table',
            score_shift='results.json score_shift; no T correction fitted',
            replicate_noise='results.json replicate_intersection; disagreement is not known measurement variance',
            similarity_construct='not_resolved_by_this_run; no new homology alignment performed'),
        conclusion='Associations only; mechanisms may remain unresolved.')
    atomic_json(out/'error-results.json',result);atomic_json(PROJECT/'error-results.json',result)


def figures(campaign,out,control):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    result=read(campaign/'jobs/aggregate-refit/results.json');paths=[]
    fig,ax=plt.subplots(figsize=(7,3.5));labels=[]
    for i,(name,record) in enumerate(result['contrasts'].items()):
        low,high=record['ci_adjusted'];value=record['delta']
        ax.errorbar(value,i,xerr=[[value-low],[high-value]],fmt='o',capsize=4)
        labels.append(name.replace('esm2_35m-','').replace('_minus_',' minus '))
    ax.set_yticks(range(len(labels)),labels);ax.axvline(0,color='grey',linestyle='--')
    ax.set_xlabel('Delta peptide-macro MAE; 97.5% paired group-bootstrap CI')
    ax.set_title('Development: post-hoc held-source transfer');fig.tight_layout()
    paths.append(('primary-contrasts.png',fig))
    fig,ax=plt.subplots(figsize=(7,4))
    for name,record in result['metrics'].items():
        strata=record['strata'];order=[s for s in ['le3','gt3_le4','gt4_le5','gt5'] if s in strata]
        ax.plot(order,[strata[s]['mae'] for s in order],marker='o',label=name.replace('esm2_35m-',''))
    ax.set_ylabel('Peptide-macro MAE');ax.set_xlabel('Measured scanning WT PSI stratum')
    ax.set_title('Development: all baselines retained');ax.legend(fontsize=8);fig.tight_layout()
    paths.append(('mae-by-psi.png',fig))
    fig,ax=plt.subplots(figsize=(7,4))
    for name,shift in result['score_shift'].items():
        for population,key in [('OOF W','OOF_W_quantiles'),('Final W (in-sample)','final_W_in_sample_quantiles'),('T','T_quantiles')]:
            ax.plot([.01,.1,.5,.9,.99],shift[key],marker='.',label=name.replace('esm2_35m-','')+' '+population)
    ax.set_xlabel('Prediction quantile');ax.set_ylabel('Raw score');ax.set_title('Development: final score shift, no correction')
    ax.legend(fontsize=7);fig.tight_layout();paths.append(('score-shift.png',fig))
    target=PROJECT/'figures';target.mkdir(exist_ok=True)
    for name,fig in paths:
        control.check();fig.savefig(out/name,dpi=160);plt.close(fig);shutil.copyfile(out/name,target/name)
    atomic_json(out/'figure-results.json',dict(files=[name for name,_ in paths],source_results_sha256=sha256(campaign/'jobs/aggregate-refit/results.json')))
    (PROJECT/'figure-captions.md').write_text(
        '# Figures\n\nAll results are development, post-hoc transfer on a previously examined held source.\n\n'
        '- primary-contrasts.png: LoRA-D minus frozen-D/W5-D peptide-macro MAE, paired group-bootstrap 97.5% intervals; negative favours LoRA.\n'
        '- mae-by-psi.png: Peptide-macro MAE by measured scanning WT PSI, retaining zero and W-derived constant baselines.\n'
        '- score-shift.png: OOF W, in-sample final W and held-source T prediction quantiles. Final W is not a generalization estimate.\n\n'
        'Numbers and denominators: results.json. No automatic serving promotion or gate closure.\n',encoding='utf8')


def finalize(campaign,out,config,lock):
    state=read(campaign/'state.json');planned=read(campaign/'queue.json')
    core=[j['id'] for j in planned if j['kind'] in CORE_KINDS]
    assert len(core)==15 and all(state['jobs'][name]['status']=='complete' for name in core)
    files=[]
    paths=[repo_path(x['path']) for x in lock['files'] if '/output/weights/esm2_35m/' in x['path']]
    for mode in config['modes']:
        paths.extend(campaign/'jobs'/f'refit-{mode}-D-{seed}'/'model.pt' for seed in config['seeds'])
        paths.append(campaign/'jobs'/f'calibrate-final-{mode}-D'/'final-calibrator.joblib')
    for path in paths:
        files.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=sha256(path),role='inference',transport='manual_copy_not_Git'))
    for path in (campaign/'jobs').rglob('*.npy'):
        files.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,sha256=sha256(path),role='reanalysis_or_resume',transport='manual_copy_not_Git'))
    summary=dict(campaign=campaign.name,status='core_complete_branch1_incomplete',core_jobs_complete=15,
        scientific_status=STATUS,koren=state['jobs'].get('koren-rank-only',{}).get('status','pending'),
        outstanding=['Koren S4 input and reviewed variable-length inference','Author/supervisor D-4 decision',
                     'Cross-runtime inference parity on primary machine','Full mechanism/similarity investigation if required'],
        G2_G3='not_closed',serving='unchanged')
    atomic_json(out/'acceptance-results.json',summary);atomic_json(PROJECT/'acceptance-results.json',summary)
    manifest=dict(schema_version=1,campaign=campaign.name,files=files,summary=summary,
        note='Verify hashes after manual copy. Do not copy .git or .venv; Git clone alone cannot resume training.')
    atomic_json(out/'handoff-manifest.json',manifest);atomic_json(PROJECT/'handoff-manifest.json',manifest)


def dispatch(ds,job,campaign,out,control):
    plan=read(campaign/'plan.json');config=plan['config'];lock=config_inputs(config)
    assert sha256(repo_path(config['protocol']))==plan['protocol_sha256']
    assert sha256(repo_path(config['source_lock']))==plan['source_lock_sha256']
    verify_sources(lock)
    if job['kind']=='refit':refit(ds,job,campaign,out,control,lock)
    elif job['kind']=='calibrate-final':calibrate(ds,job,out,lock)
    elif job['kind']=='score-held':score(ds,job,campaign,out,control,config,lock)
    elif job['kind']=='aggregate-refit':aggregate(ds,campaign,out,control,config,lock)
    elif job['kind']=='model-card-parity':parity(ds,campaign,out,control,config)
    elif job['kind']=='analyze-errors':errors(ds,campaign,out,control)
    elif job['kind']=='figure-export':figures(campaign,out,control)
    elif job['kind']=='finalize-branch1':finalize(campaign,out,config,lock)
    elif job['kind']=='koren-rank-only':
        from .local_jobs import Blocked
        atomic_json(out/'pending.json',dict(status='source_pending',reason='Koren S4 input absent; variable-length inference not validated.'))
        raise Blocked('Koren S4 missing; branch 1 remains incomplete. No synthetic padding/scaling.',kind='source_pending')
    else:raise ValueError(job['kind'])
