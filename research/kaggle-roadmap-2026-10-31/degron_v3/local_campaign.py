"""Persistent work queue and Windows-visible session orchestration."""
from collections import Counter
import csv
import gc
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import time
import traceback

import numpy as np
import pandas as pd
import torch

from .common import atomic_json, environment, sha256
from .data import Dataset
from .local_control import Control, Paused, fingerprint, process_lock, install_pause_handler
from . import local_jobs as work
from .metrics import summarize, per_peptide, paired_ci

HERE = work.HERE
ROOT = next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
TERMINAL = {'complete','resource_blocked','adapter_blocked','skipped_resource','source_pending','structure_pending'}
EXCLUDED = TERMINAL-{'complete'}
TOKENIZER_REPAIR_SOURCE = 'a794922b58f9c0792905b962b06a9f47444c5ca146232737662b58512ed14db0'


def implementation_hash():
    return hashlib.sha256(b''.join(p.read_bytes() for p in sorted((HERE/'degron_v3').glob('*.py')))+
                          (HERE/'local-runner.py').read_bytes()).hexdigest()


def window_title(value):
    if os.name=='nt':
        import ctypes
        setter=ctypes.windll.kernel32.SetConsoleTitleW
        setter.argtypes=[ctypes.c_wchar_p]
        setter(value)


def runtime_identity():
    result=environment()
    probe=subprocess.run(['nvidia-smi','--query-gpu=driver_version','--format=csv,noheader'],
                         capture_output=True,text=True,timeout=10,check=True)
    result['driver_version']=probe.stdout.strip()
    return result


def jobs(config):
    items = [dict(id='import-kaggle', kind='import', deps=[])]
    for model in config['models']:
        items += [dict(id=f'weights-{model}',kind='weights',model=model,deps=[]),
                  dict(id=f'probe-{model}',kind='probe',model=model,deps=[f'weights-{model}']),
                  dict(id=f'extract-{model}',kind='extract',model=model,deps=[f'probe-{model}'])]
        for arm in config['arms']:
            for context in [False,True]:
                for seed in config['seeds']:
                    for fold in range(5):
                        items.append(dict(id=f'ridge-{model}-{arm}-{int(context)}-{seed}-{fold}',kind='ridge',model=model,
                            arm=arm,context=context,seed=seed,fold=fold,deps=[f'extract-{model}']))
    for seed in config['seeds']:
        for mode in ['frozen','lora']:
            for arm in config['arms']:
                for fold in range(5):
                    items.append(dict(id=f'tune-{mode}-{arm}-{seed}-{fold}',kind='tune',mode=mode,arm=arm,
                        seed=seed,fold=fold,deps=['import-kaggle','probe-esm2_35m']))
    items += [dict(id='collect-family',kind='collect',group='ridge',deps=[j['id'] for j in items if j['kind']=='ridge']),
              dict(id='collect-core',kind='collect',group='tune',deps=[j['id'] for j in items if j['kind']=='tune'])]
    development = [j['id'] for j in items if j['kind'] in ['ridge','tune']]
    items += [dict(id='external-pending',kind='external',deps=[]),dict(id='structure-pending',kind='structure',deps=[]),
              dict(id='calibrate-core',kind='calibrate',deps=['collect-core']),
              dict(id='locked-transfer-w5',kind='transfer',deps=['import-kaggle','collect-family','collect-core']),
              dict(id='report',kind='report',deps=['calibrate-core','locked-transfer-w5'])]
    return items


def initialize(config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf8'))
    assert config['models'] and 'esm2_35m' in config['models'] and set(config['models']) <= set(work.MODELS)
    assert config['arms']==['B','D'] and config['seeds']==[17,29,43]
    ds = Dataset(ROOT/config['data'])
    runtime = runtime_identity()
    assert runtime.get('cuda'), 'Local GPU campaign requires CUDA; do not silently run heavy models on CPU'
    plan = dict(schema_version=1, config=config, data_identity=ds.identity,
        code_sha256=implementation_hash(),
        registry_sha256=sha256(HERE/'model-registry.json'),
        protocol_sha256=sha256(HERE/'EXECUTION-PROTOCOL.md'),runtime=runtime,
        scientific_status='development_expansion_after_Kaggle_results',
        training=dict(epochs=20,batch=8,dtype='float32',lr=.0001,patience=4,refit='selected_inner_epoch'),
        features=dict(dtype='float16',batch=8,view='delta_site_and_mean',pca=64,
                      encoder_dtypes=dict(work.INFERENCE_DTYPES)),
        selection='inner MSE only; no family selection from outer OOF; T locked to prespecified W5-D',
        source_campaign='369cb2fe6a1e31e0')
    source_name = config.get('inherit_completed_from')
    source = None
    if source_name:
        assert Path(source_name).name == source_name, 'Use a campaign ID, not a path'
        source = HERE/'output/local'/source_name
        plan['inheritance_source'] = dict(campaign=source_name,
            plan_sha256=sha256(source/'plan.json'), state_sha256=sha256(source/'state.json'),
            policy='tokenizer_repair_reuse_unaffected_complete_and_paused_esm35_v1')
    identity = fingerprint(plan)
    campaign = HERE/'output/local'/identity[:16]; campaign.mkdir(parents=True,exist_ok=True)
    if (campaign/'plan.json').exists():
        assert json.loads((campaign/'plan.json').read_text()) == plan
    else:
        atomic_json(campaign/'plan.json',plan); atomic_json(campaign/'queue.json',jobs(config))
        atomic_json(campaign/'state.json',dict(plan_id=identity,jobs={},scientific_status=plan['scientific_status']))
    if source is not None and (not (campaign/'inheritance.json').exists() or
                               not json.loads((campaign/'state.json').read_text())['jobs']):
        validation = json.loads((HERE/'tokenizer-repair-validation.json').read_text())
        inherit_unaffected(source, campaign, validation)
    atomic_json(campaign.parent/'latest.json',dict(campaign=str(campaign),plan_id=identity))
    return campaign


def latest():
    path=HERE/'output/local/latest.json'
    if not path.exists(): raise FileNotFoundError('No local campaign yet; run run-local.cmd first')
    return Path(json.loads(path.read_text())['campaign'])


def complete_valid(campaign, record):
    if record.get('status')!='complete': return False
    origin = Path(record.get('artifact_campaign', campaign)).resolve()
    if origin != Path(campaign).resolve():
        if origin.parent != Path(campaign).resolve().parent: return False
        if sha256(origin/'plan.json') != record['source_plan_sha256']: return False
    for entry in record.get('files',[]):
        path=(origin/entry['path']).resolve()
        if not path.is_relative_to(origin): return False
        if not path.exists() or path.stat().st_size!=entry['bytes'] or sha256(path)!=entry['sha256']: return False
    return bool(record.get('files'))


def inherit_unaffected(source, target, validation):
    """Narrow, audited repair migration; never overwrite the source campaign."""
    source, target = Path(source).resolve(), Path(target).resolve()
    assert source.parent == target.parent and source != target
    old = json.loads((source/'plan.json').read_text())
    new = json.loads((target/'plan.json').read_text())
    state = json.loads((source/'state.json').read_text())
    assert validation['status'] == 'pass' and validation['target_code_sha256'] == implementation_hash()
    assert old['code_sha256'] == TOKENIZER_REPAIR_SOURCE, 'Source code has not been reviewed for this repair'
    assert state['plan_id'] == fingerprint(old) and source.name == fingerprint(old)[:16]
    assert new['code_sha256'] == implementation_hash()
    assert new['inheritance_source']['plan_sha256'] == sha256(source/'plan.json')
    assert new['inheritance_source']['state_sha256'] == sha256(source/'state.json')
    assert not any(v['status']=='running' for v in state['jobs'].values()), 'Source must be stopped'
    for key in ('data_identity','registry_sha256','protocol_sha256','training','selection','source_campaign'):
        assert old[key] == new[key], f'Cannot inherit changed scientific setting: {key}'
    assert old['features'] == {k:v for k,v in new['features'].items() if k!='encoder_dtypes'}
    assert new['features']['encoder_dtypes'] == {'ankh_base':'float32'}
    assert old['config'] == {k:v for k,v in new['config'].items() if k!='inherit_completed_from'}
    previous_runtime = old['runtime']
    runtime = {**new['runtime'], 'versions': {k:v for k,v in new['runtime']['versions'].items() if k!='protobuf'}}
    assert previous_runtime == runtime, 'Only the added protobuf dependency may differ'
    assert new['runtime']['versions']['protobuf'] == '6.33.5'
    allowed = {j['id']: j for j in jobs(new['config'])}
    inherited, paused, copies = {}, {}, []
    for job_id, record in state['jobs'].items():
        job = allowed.get(job_id)
        if job is None: continue
        affected = job.get('model') in ('prott5_encoder','ankh_base') and job['kind']!='weights'
        if affected or job['kind'] not in ('import','weights','probe','extract','ridge','tune'): continue
        assert 'artifact_campaign' not in record, 'Chained inheritance needs a separate review'
        if record['status']=='complete':
            assert complete_valid(source, record), f'Changed completed artifact: {job_id}'
            inherited[job_id] = {**record, 'artifact_campaign': str(source),
                                 'source_plan_sha256': sha256(source/'plan.json')}
        elif record['status']=='paused' and job['kind']=='tune':
            # ESM35 numerical/training code is unchanged; preserve checkpoint
            # identity and RNG via explicit lineage, not by rewriting tensors.
            paused[job_id] = source.name
            for path in sorted((source/'jobs'/job_id).rglob('*')):
                if not path.is_file() or path.name=='worker-result.json' or path.name.endswith('.tmp'): continue
                copies.append(dict(path=path.relative_to(source).as_posix(), bytes=path.stat().st_size, sha256=sha256(path)))
            inherited[job_id] = dict(status='paused', reason='Audited ESM35 checkpoint inherited; source retained')
    target_state = json.loads((target/'state.json').read_text())
    assert not target_state['jobs'], 'Inheritance only initializes an empty successor'
    for entry in copies:
        src, dst = source/entry['path'], target/entry['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        assert not dst.exists() or sha256(dst)==entry['sha256']
        if not dst.exists(): shutil.copyfile(src,dst)
        assert sha256(dst)==entry['sha256']
    manifest = dict(source_campaign=str(source), source_plan_sha256=sha256(source/'plan.json'),
        source_state_sha256=sha256(source/'state.json'), source_code_sha256=old['code_sha256'],
        target_code_sha256=new['code_sha256'], validation_sha256=fingerprint(validation),
        inherited_complete=sum(v['status']=='complete' for v in inherited.values()),
        checkpoint_campaigns=paused, checkpoint_files=copies,
        reset_models=['prott5_encoder','ankh_base'], source_immutable=True)
    # Write lineage before state; a failure never marks unverified work complete.
    atomic_json(target/'inheritance.json', manifest)
    target_state['jobs']=inherited
    atomic_json(target/'state.json', target_state)


def collect(ds,campaign,out,control,group):
    planned=json.loads((campaign/'queue.json').read_text()); state=json.loads((campaign/'state.json').read_text())['jobs']
    buckets={}
    for item in planned:
        if item['kind']!=group or state.get(item['id'],{}).get('status')!='complete':continue
        folder=work.artifact_directory(campaign,item['id']); info=json.loads((folder/'fit.json').read_text())
        buckets.setdefault(info['recipe'],[]).append(folder)
    reports={}; tables=[]; pp={}
    for recipe,folders in buckets.items():
        control.check()
        frame=pd.concat([pd.read_parquet(p/'oof.parquet') for p in folders],ignore_index=True)
        assert set(frame.data_identity)=={ds.identity} and set(frame['mode'])=={'official'}
        assert not frame.duplicated(['seed','cell_id']).any()
        assert set(frame.seed)=={17,29,43}
        for seed,part in frame.groupby('seed'):
            assert set(part.cell_id)==set(ds.sat.cell_id) and len(part)==len(ds.sat)
            observed=part.set_index('cell_id').reindex(ds.sat.cell_id)
            assert np.array_equal(observed.dpsi_mean.to_numpy(),ds.sat.dpsi_mean.to_numpy())
            assert np.array_equal(observed.outer_fold.to_numpy(),ds.sat.outer_fold.to_numpy())
        frame.to_parquet(out/f'{recipe}-oof.parquet',index=False)
        for folder in folders:
            info=json.loads((folder/'fit.json').read_text()); dest=out/f'{recipe}-seed{info["seed"]}-fold{info["fold"]}-calibration.parquet'
            if not dest.exists(): shutil.copyfile(folder/'calibration.parquet',dest)
        mean=frame.groupby('cell_id').prediction.mean().reindex(ds.sat.cell_id).to_numpy()
        report=dict(ensemble=summarize(ds.sat,mean),per_seed={str(s):summarize(ds.sat,
            part.set_index('cell_id').prediction.reindex(ds.sat.cell_id).to_numpy()) for s,part in frame.groupby('seed')})
        atomic_json(out/f'{recipe}-results.json',report);reports[recipe]=report
        pp[recipe]=per_peptide(ds.sat,mean)
        tables.append(dict(recipe=recipe,platform='local',seeds='17,29,43',**report['ensemble']['all']))
        control.log(f'COLLECT {recipe} MAE={report["ensemble"]["all"]["mae"]:.6f}',force=True)
    if group=='ridge' and buckets:
        selected=[]; choices=[]
        for seed in [17,29,43]:
            for fold in range(5):
                options=[]
                for recipe,folders in buckets.items():
                    for folder in folders:
                        info=json.loads((folder/'fit.json').read_text())
                        if info['seed']==seed and info['fold']==fold:options.append((info['validation_mse'],recipe,folder))
                loss,recipe,folder=min(options,key=lambda v:(v[0],v[1]));rows=pd.read_parquet(folder/'oof.parquet')
                rows['selected_recipe']=recipe;rows['recipe']='nested-family-selection';selected.append(rows)
                choices.append(dict(seed=seed,fold=fold,recipe=recipe,validation_mse=loss))
        selected=pd.concat(selected);selected.to_parquet(out/'nested-family-selection-oof.parquet',index=False)
        mean=selected.groupby('cell_id').prediction.mean().reindex(ds.sat.cell_id).to_numpy()
        reports['nested-family-selection']=dict(ensemble=summarize(ds.sat,mean),choices=choices)
        tables.append(dict(recipe='nested-family-selection',platform='local',seeds='17,29,43',**reports['nested-family-selection']['ensemble']['all']))
    atomic_json(out/'collection.json',dict(data_identity=ds.identity,mode='official',reports=reports,
        eligibility={k:v['status'] for k,v in state.items() if k.startswith('probe-')},
        note='Development; resource/adapter exclusion occurs before task labels are scored.'))
    pd.DataFrame(tables).to_csv(out/'summary.csv',index=False)
    if group=='tune':
        comparisons={}
        for arm in ['B','D']:
            for metric in ['mae','auroc_plus']:
                comparisons[f'lora-frozen-{arm}-{metric}']=paired_ci(pp[f'esm2_35m-lora-{arm}'],pp[f'esm2_35m-frozen-{arm}'],metric)
        atomic_json(out/'comparisons.json',comparisons)


def dispatch(ds,job,campaign,out,control):
    kind=job['kind']
    if kind=='import':work.import_kaggle(ds,out,control)
    elif kind=='weights':work.weights(job['model'],campaign,out,control)
    elif kind=='probe':work.probe(job['model'],campaign,out,control)
    elif kind=='extract':work.extract(ds,job['model'],campaign,out,control)
    elif kind=='ridge':work.ridge_fold(ds,job,campaign,out,control)
    elif kind=='tune':work.finetune_fold(ds,job,campaign,out,control)
    elif kind=='collect':collect(ds,campaign,out,control,job['group'])
    elif kind in ['external','structure']:
        atomic_json(out/'pending.json',dict(status=kind+'_pending',reason='Reviewed external/3Di input not supplied'))
        raise work.Blocked('Reviewed input not supplied', 'source_pending' if kind=='external' else 'structure_pending')
    elif kind in ['calibrate','transfer']:
        from .stages import calibration_stage
        if kind=='transfer':
            source=work.SOURCE/'tasks/01-78cc356ba4f4';recipes=['ordered-w5-D']
        else:
            source=campaign/'jobs/collect-core';recipes=[f'esm2_35m-{mode}-{arm}' for mode in ['frozen','lora'] for arm in ['B','D']]
        for recipe in recipes:
            control.check();dest=out/recipe;dest.mkdir(exist_ok=True)
            calibration_stage(ds,dest,dict(training_output=str(source),selected_recipe=recipe,smoke=False))
    elif kind=='report':
        frames=[]
        for name in ['collect-family','collect-core']:
            frames.append(pd.read_csv(campaign/'jobs'/name/'summary.csv'))
        old=HERE/'output-analysis.json'
        if old.exists():
            reference=json.loads(old.read_text(encoding='utf8'))
            assert reference['source_manifest_sha256']==sha256(work.SOURCE/'pipeline-manifest.json')
            frames.append(pd.DataFrame([dict(recipe=k,platform='kaggle',seeds=','.join(map(str,v['seeds'])),**v['ensemble']['all']) for k,v in reference['recipes'].items()]))
        pd.concat(frames,ignore_index=True).to_csv(out/'benchmark.csv',index=False)
        atomic_json(out/'evidence.json',dict(data_identity=ds.identity,platforms=['kaggle','local'],
            claim='Development comparisons; frozen-LoRA main contrasts matched within local runtime.',
            pending=['External source','True structure mapping','Architecture-specific CNN/LoRA/family final promotion'],
            source_kaggle=str(work.SOURCE)))
    else:raise ValueError(kind)


def worker(campaign,job_id,deadline):
    with process_lock(Path(campaign).parent/'worker.lock'):
        return worker_locked(campaign,job_id,deadline)


def worker_locked(campaign,job_id,deadline):
    campaign=Path(campaign);plan=json.loads((campaign/'plan.json').read_text())
    job=next(j for j in json.loads((campaign/'queue.json').read_text()) if j['id']==job_id)
    control=Control(campaign,job_id,deadline);install_pause_handler(control)
    out=campaign/'jobs'/job_id;out.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(2)
    torch.cuda.set_per_process_memory_fraction(.75)
    result=dict(job=job_id,started_unix=time.time())
    try:
        control.check()
        assert implementation_hash()==plan['code_sha256'], 'Code changed during campaign; start a new campaign'
        assert sha256(HERE/'model-registry.json')==plan['registry_sha256']
        assert runtime_identity()==plan['runtime'], 'Runtime changed; start a new campaign'
        ds=Dataset(ROOT/plan['config']['data']);assert ds.identity==plan['data_identity']
        control.log('START '+json.dumps(job),force=True)
        dispatch(ds,job,campaign,out,control)
        result.update(status='complete',files=[dict(path=p.relative_to(campaign).as_posix(),bytes=p.stat().st_size,sha256=sha256(p))
            for p in sorted(out.rglob('*')) if p.is_file() and p.name!='worker-result.json' and not p.name.endswith(('.tmp','.previous'))])
        control.log('COMPLETE',force=True)
    except Paused as exc:result.update(status='paused',reason=str(exc));print('PAUSED:',exc,flush=True)
    except work.Blocked as exc:result.update(status=exc.kind,reason=str(exc));print(exc.kind,str(exc),flush=True)
    except Exception as exc:
        result.update(status='failed',reason=f'{type(exc).__name__}: {exc}',traceback=traceback.format_exc());traceback.print_exc()
    result['seconds']=time.time()-result['started_unix'];atomic_json(out/'worker-result.json',result)
    return 0 if result['status']=='complete' else 75 if result['status']=='paused' else 2


def status(campaign):
    campaign=Path(campaign);state=json.loads((campaign/'state.json').read_text());planned=json.loads((campaign/'queue.json').read_text())
    counts=Counter(state['jobs'].get(j['id'],{}).get('status','pending') for j in planned)
    print('Campaign:',campaign,'\nJobs:',dict(counts),'\nTotal:',len(planned),flush=True)
    if (campaign/'progress.json').exists():print('Last progress:',(campaign/'progress.json').read_text(),flush=True)
    return dict(counts)


def run(config,hours=2,profile='all',retry_failed=False,max_jobs=None):
    lock=HERE/'output/local/session.lock'
    with process_lock(lock):
        # An orphan worker must finish/pause before another supervisor can start GPU work.
        with process_lock(lock.with_name('worker.lock')):pass
        campaign=initialize(config);state=json.loads((campaign/'state.json').read_text());planned=json.loads((campaign/'queue.json').read_text())
        stop=campaign/'STOP'
        if stop.exists():stop.unlink()
        session=time.strftime('%Y%m%d-%H%M%S');logdir=campaign/'sessions';logdir.mkdir(exist_ok=True)
        deadline=time.time()+hours*3600 if hours else 0
        control=Control(campaign,'supervisor',deadline);install_pause_handler(control)
        atomic_json(campaign/'session.json',dict(pid=os.getpid(),session=session,deadline_unix=deadline,status='running',profile=profile))
        window_title('Degron CUDA | RUNNING | '+campaign.name)
        print('VISIBLE LOCAL SESSION',session,'\nCampaign:',campaign,'\nRuntime:',json.loads((campaign/'plan.json').read_text())['runtime'],flush=True)
        print('Ctrl+C requests a safe pause. Checkpoints every 120s during training. Close window = recover last committed checkpoint.',flush=True)
        for record in state['jobs'].values():
            if record['status']=='running':record['status']='paused'
        attempted=set();executed=0
        def save():atomic_json(campaign/'state.json',state)
        with (logdir/f'{session}.log').open('a',encoding='utf8',buffering=1) as log:
            log.write(f'SESSION {session} campaign={campaign} deadline={deadline} profile={profile}\n')
            for job in planned:
                if control.stopping() or (max_jobs is not None and executed>=max_jobs):break
                if profile=='models' and job['kind'] in ['tune','calibrate','transfer','report']:continue
                if profile=='core' and (job['kind'] in ['ridge','extract'] or (job.get('model') and job['model']!='esm2_35m') or job['id']=='collect-family'):continue
                record=state['jobs'].get(job['id'],{})
                if record.get('status')=='complete':
                    if complete_valid(campaign,record):continue
                    raise ValueError(f'Completed artifact changed: {job["id"]}; inspect before continuing')
                if record.get('status') in EXCLUDED:continue
                if record.get('status')=='failed' and not retry_failed:continue
                deps=[state['jobs'].get(d,{}).get('status','pending') for d in job['deps']]
                if any(s not in TERMINAL for s in deps):continue
                if any(s in EXCLUDED for s in deps) and job['kind']!='collect':
                    state['jobs'][job['id']]=dict(status='skipped_resource',reason='Dependency excluded before scoring');save();continue
                state['jobs'][job['id']]=dict(status='running',session=session);save()
                headline=f'\nRUN {job["id"]} | {executed+1} new work units this session\n'
                print(headline,end='',flush=True);log.write(headline)
                joblogs=campaign/'logs';joblogs.mkdir(exist_ok=True)
                joblog=(joblogs/f'{job["id"]}.log').open('a',encoding='utf8',buffering=1)
                args=[sys.executable,'-u','-I',str(HERE/'local-runner.py'),'worker','--campaign',str(campaign),'--job',job['id'],'--deadline',str(deadline)]
                launched=time.time()
                child=subprocess.Popen(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace',bufsize=1)
                lines=queue.Queue()
                def reader():
                    for line in child.stdout:lines.put(line)
                thread=threading.Thread(target=reader,daemon=True);thread.start()
                heartbeat=time.monotonic()
                while child.poll() is None or not lines.empty() or thread.is_alive():
                    if control.stopping():stop.touch(exist_ok=True)
                    try:
                        line=lines.get(timeout=1);print(line,end='',flush=True);log.write(line);joblog.write(line)
                    except queue.Empty:pass
                    if time.monotonic()-heartbeat>=30:
                        line=time.strftime('%H:%M:%S')+' heartbeat '+job['id']+'; worker active\n';print(line,end='',flush=True);log.write(line);joblog.write(line);heartbeat=time.monotonic()
                thread.join();child.wait()
                joblog.close()
                result_path=campaign/'jobs'/job['id']/'worker-result.json'
                if result_path.exists() and json.loads(result_path.read_text()).get('started_unix',0)>=launched:record=json.loads(result_path.read_text())
                else:record=dict(status='failed',reason=f'Worker exited {child.returncode} without a result')
                state['jobs'][job['id']]=record;save();executed+=1
                if record['status']=='paused':break
        atomic_json(campaign/'session.json',dict(pid=os.getpid(),session=session,status='paused' if control.stopping() else 'idle',executed=executed))
        status(campaign)
        print('SESSION ENDED. Run run-local.cmd again to continue. This window remains open.',flush=True)
        window_title('Degron CUDA | SESSION ENDED | '+campaign.name)
        return campaign
