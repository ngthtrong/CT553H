"""Supplemental rank-only inference; no new trainer, scheduler or core edits."""
import os
for key,value in [('OMP_NUM_THREADS','2'),('OPENBLAS_NUM_THREADS','2'),('CUBLAS_WORKSPACE_CONFIG',':4096:8'),
                   ('HF_HUB_OFFLINE','1'),('TRANSFORMERS_OFFLINE','1')]:
    os.environ.setdefault(key,value)
from pathlib import Path
import gc
import hashlib
import json
import posixpath
import re
import statistics
import sys
import time
import xml.etree.ElementTree as ET
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
V3=ROOT/'research/kaggle-roadmap-2026-10-31'
sys.path.insert(0,str(V3))
import numpy as np
import pandas as pd
import torch
from scipy.stats import spearmanr
from degron_v3.common import AA_INDEX,atomic_json,sha256
from degron_v3.data import Dataset
from degron_v3.features import features
from degron_v3.finetune import infer
from degron_v3.local_control import Control,Paused,fingerprint,process_lock,install_pause_handler
from degron_v3.local_training import predict
from degron_v3.local_refit import load_model,read,FEATURES
from degron_v3.local_campaign import complete_valid,window_title

RAW=ROOT/'data/raw/koren-2018/NIHMS967427-supplement-11.xlsx'
RAW_HASH='c96973f2b2781b35a822527fa875e38df82f75da9ac327668d1d10114fdbcbeb'
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def xlsx_sheets(path):
    with zipfile.ZipFile(path) as archive:
        assert sum(x.file_size for x in archive.infolist())<50*2**20
        strings=[]
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings=[''.join(t.text or '' for t in item.findall('.//s:t',NS))
                     for item in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(archive.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
            rel=sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target=rels[rel]
            target=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl',target))
            assert target.startswith('xl/') and '..' not in target.split('/')
            rows=[]
            for row in ET.fromstring(archive.read(target)).findall('s:sheetData/s:row',NS):
                values={}
                for cell in row.findall('s:c',NS):
                    column=re.match(r'[A-Z]+',cell.attrib['r']).group()
                    value=cell.find('s:v',NS);kind=cell.attrib.get('t')
                    if kind=='inlineStr':result=''.join(x.text or '' for x in cell.findall('.//s:t',NS))
                    elif value is None:result=None
                    elif kind=='s':result=strings[int(value.text)]
                    elif kind in ['str','e']:result=value.text
                    else:result=float(value.text)
                    values[column]=result
                rows.append(values)
            header=next(row for row in rows if row.get('A')=='Oligo ID')
            start=rows.index(header)+1
            yield sheet.attrib['name'],[{str(name):row.get(column) for column,name in header.items() if name is not None}
                                         for row in rows[start:] if row.get('A') is not None]


def parse_source():
    assert RAW.is_file() and sha256(RAW)==RAW_HASH,'Missing/changed Koren S4'
    output=[];qc=[]
    for sheet,rows in xlsx_sheets(RAW):
        substrate=sheet.split('. ',1)[1].strip();parsed=[]
        for index,row in enumerate(rows):
            match=re.fullmatch(r'([A-Z])(\d+)([A-Z])',str(row.get('Substitution','')).strip())
            if match is None:continue
            wt,pos,mut=match.group(1),int(match.group(2)),match.group(3)
            text=str(row['Amino acid sequence']);assert text.endswith('*')
            seq=text[:-1];assert set(seq)<=set(AA_INDEX) and len(seq) in [12,23]
            bins=np.asarray([row[f'Bin{i}'] for i in [1,2,3]],dtype=float)
            assert np.isfinite(bins).all() and bins.sum()>0
            measured=float(row['PSI']);error=abs(float(np.dot(bins,[1,2,3])/bins.sum())-measured)
            assert error<=1e-6
            parsed.append(dict(cell_id='koren-'+fingerprint([sheet,index,wt,pos,mut])[:20],
                peptide_id=substrate,group_id=substrate,position_1based=pos,wt_aa=wt,mut_aa=mut,
                mutant_sequence=seq,psi=measured,psi_error=error))
        reference=next(row for row in parsed if row['wt_aa']!=row['mut_aa'])
        chars=list(reference['mutant_sequence']);chars[reference['position_1based']-1]=reference['wt_aa']
        wtseq=''.join(chars)
        identities=[row['psi'] for row in parsed if row['wt_aa']==row['mut_aa']]
        assert identities
        for row in parsed:
            pos=row['position_1based']-1;seq=row['mutant_sequence']
            assert len(seq)==len(wtseq) and wtseq[pos]==row['wt_aa'] and seq[pos]==row['mut_aa']
            assert sum(a!=b for a,b in zip(seq,wtseq))==int(row['wt_aa']!=row['mut_aa'])
            row['wt_sequence']=wtseq;row['dpsi_mean']=row['psi']-statistics.median(identities)
            if row['wt_aa']!=row['mut_aa']:output.append(row)
        qc.append(dict(substrate=substrate,rows=len(parsed),identity_rows=len(identities),
                       mutants=sum(row['wt_aa']!=row['mut_aa'] for row in parsed),
                       length=len(wtseq),max_psi_error=max(row['psi_error'] for row in parsed)))
    assert len(qc)==9 and sum(x['rows'] for x in qc)==1827 and len(output)==1739
    frame=pd.DataFrame(output).sort_values(['peptide_id','cell_id']).reset_index(drop=True)
    assert not frame.cell_id.duplicated().any()
    return frame,qc


def variable_aux(frame):
    pair=np.zeros((len(frame),40),dtype=np.float32);composition=np.zeros((len(frame),20),dtype=np.float32)
    for i,(seq,pos,mut) in enumerate(zip(frame.wt_sequence,frame.position_1based,frame.mut_aa)):
        pos=int(pos)-1;assert 0<=pos<len(seq) and seq[pos]!=mut
        pair[i,AA_INDEX[seq[pos]]]=1;pair[i,20+AA_INDEX[mut]]=1
        for aa in seq:composition[i,AA_INDEX[aa]]+=1/len(seq)
    return np.concatenate([pair,composition],axis=1)


def variable_tensor(encoder,sequences):
    length=len(sequences[0]);assert all(len(s)==length for s in sequences)
    encoded=encoder.tokenizer(list(sequences),return_tensors='pt',padding=True,
                              return_special_tokens_mask=True,truncation=False)
    mask=encoded['attention_mask'].bool() & ~encoded.pop('special_tokens_mask').bool()
    assert torch.all(mask.sum(1)==length)
    encoded={k:v.to(encoder.device) for k,v in encoded.items()}
    hidden=encoder.model(**encoded).last_hidden_state
    result=hidden[mask.to(encoder.device)].reshape(len(sequences),length,-1)
    assert torch.isfinite(result).all()
    return result


class VariableLength(torch.nn.Module):
    def __init__(self,base):
        super().__init__();self.base=base

    def learned_state(self):return self.base.learned_state()

    def forward(self,frame):
        self.base.backbone.eval();frame=frame.reset_index(drop=True)
        result=torch.empty(len(frame),device=self.base.encoder.device)
        lengths=frame.wt_sequence.str.len().to_numpy()
        for length in sorted(set(lengths)):
            rows=np.flatnonzero(lengths==length);sub=frame.iloc[rows]
            wt=variable_tensor(self.base.encoder,sub.wt_sequence.tolist())
            mutant=variable_tensor(self.base.encoder,sub.mutant_sequence.tolist());delta=mutant-wt
            position=torch.as_tensor(sub.position_1based.to_numpy()-1,device=wt.device)
            pooled=torch.cat([delta[torch.arange(len(sub),device=wt.device),position],delta.mean(1)],dim=1)
            aux=torch.as_tensor(variable_aux(sub),device=wt.device)
            result[torch.as_tensor(rows,device=wt.device)]=self.base.head(torch.cat([pooled.float(),aux],1)).squeeze(-1)
        return result


def rho(y,p):
    if np.ptp(y)==0 or np.ptp(p)==0:return None
    value=float(spearmanr(y,p).statistic)
    return value if np.isfinite(value) else None


def run(campaign,deadline=0):
    campaign=Path(campaign);state=read(campaign/'state.json')
    for mode in ['lora','frozen']:
        for seed in [17,29,43]:
            if not complete_valid(campaign,state['jobs'].get(f'refit-{mode}-D-{seed}',{})):
                print('Koren waits for all six final refit models.',flush=True);return 0
    model_pins=[]
    for mode in ['lora','frozen']:
        for seed in [17,29,43]:
            path=campaign/'jobs'/f'refit-{mode}-D-{seed}'/'model.pt'
            model_pins.append(dict(mode=mode,seed=seed,path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))
    plan=dict(schema_version=1,source_campaign=campaign.name,source_plan_sha256=sha256(campaign/'plan.json'),
        raw_sha256=sha256(RAW),script_sha256=sha256(Path(__file__)),protocol_sha256=sha256(HERE/'KOREN-PROTOCOL.md'),models=model_pins)
    identity=fingerprint(plan);out=HERE/'local'/('koren-'+identity[:16]);out.mkdir(parents=True,exist_ok=True)
    atomic_json(out/'plan.json',plan)
    if (out/'results.json').exists():
        atomic_json(HERE/'koren-results.json',read(out/'results.json'))
        atomic_json(HERE/'koren-run-status.json',dict(status='complete',source_campaign=campaign.name,identity=identity))
        print('Koren supplemental evaluation already complete.',flush=True);return 0
    control=Control(campaign,'koren-supplement',deadline);control.identity_campaign=identity;install_pause_handler(control)
    statuspath=HERE/'koren-run-status.json'
    atomic_json(statuspath,dict(status='running',source_campaign=campaign.name,identity=identity,started_unix=time.time()))
    window_title('Degron CUDA | KOREN SUPPLEMENT | '+campaign.name)
    try:
        control.check();frame,qc=parse_source();frame.to_parquet(out/'source-cells.parquet',index=False)
        ds=Dataset(ROOT/'data/processed/degron-data-v3-fullpsi');fixture=ds.sat[FEATURES].head(16)
        predictions={};parities=[]
        for mode in ['lora','frozen']:
            values=[]
            for seed in [17,29,43]:
                control.check();model,_=load_model(campaign,mode,seed)
                reference=infer(model,fixture,batch=8);adapter=VariableLength(model)
                assert np.array_equal(variable_aux(fixture),features(fixture,'composition'))
                actual=infer(adapter,fixture,batch=8)
                assert np.allclose(reference,actual,atol=1e-5,rtol=1e-5)
                parities.append(dict(mode=mode,seed=seed,max_abs_difference=float(abs(reference-actual).max())))
                control.job=f'koren-{mode}-D-{seed}'
                values.append(predict(adapter,frame[FEATURES],out/f'{mode}-{seed}.npy',control))
                del model,adapter;gc.collect();torch.cuda.empty_cache()
            predictions[mode]=values
        rows=[]
        for substrate,sub in frame.groupby('peptide_id',sort=True):
            idx=sub.index.to_numpy();row=dict(substrate=substrate,mutants=len(sub),length=len(sub.wt_sequence.iloc[0]))
            for mode,values in predictions.items():
                row[mode]=dict(ensemble_spearman=rho(sub.dpsi_mean.to_numpy(),np.mean(values,axis=0)[idx]),
                    per_seed={str(seed):rho(sub.dpsi_mean.to_numpy(),p[idx]) for seed,p in zip([17,29,43],values)})
            rows.append(row)
        result=dict(status='complete',identity=identity,source_campaign=campaign.name,scientific_status='development_not_gate_closure',
            evaluation='rank_only_adjacent_source_previously_audited',substrates=rows,QC=qc,parity_28aa=parities,
            macro_spearman={mode:(float(np.mean(eligible)) if eligible else None)
                for mode in predictions for eligible in [[r[mode]['ensemble_spearman'] for r in rows if r[mode]['ensemble_spearman'] is not None]]},
            eligible_substrates={mode:sum(r[mode]['ensemble_spearman'] is not None for r in rows) for mode in predictions},
            denominator=dict(substrates=9,mutants=1739),provenance=plan,
            limitations=['Length/construct extrapolation; not independent untouched validation.',
                'No PSI rescaling, calibration, MAE comparison with Zhang, cell-level p-values or automatic gate closure.',
                'Original core queue/source_pending history is unchanged; this is a supplemental evaluation.'])
        atomic_json(out/'results.json',result);atomic_json(HERE/'koren-results.json',result)
        atomic_json(statuspath,dict(status='complete',source_campaign=campaign.name,identity=identity,finished_unix=time.time()))
        atomic_json(HERE/'koren-handoff-manifest.json',dict(identity=identity,source_campaign=campaign.name,
            artifacts=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha256(p),transport='internal_manual_copy_not_Git') for p in out.glob('*.npy')],
            raw_source_policy='internal_only_not_Git',core_state_unchanged=True))
        print('KOREN COMPLETE: 9 substrates, 1739 mutants; rank-only results exported.',flush=True)
        return 0
    except Paused as exc:
        atomic_json(statuspath,dict(status='paused',source_campaign=campaign.name,identity=identity,reason=str(exc)))
        print('Koren PAUSED; run-local.cmd resumes committed prefixes.',flush=True);return 0
    except Exception as exc:
        atomic_json(statuspath,dict(status='failed',source_campaign=campaign.name,identity=identity,reason=f'{type(exc).__name__}: {exc}'))
        raise


def after_core(campaign,deadline=0):
    base=Path(campaign).parent
    with process_lock(base/'session.lock'):
        with process_lock(base/'worker.lock'):
            torch.set_num_threads(2);torch.cuda.set_per_process_memory_fraction(.75)
            return run(campaign,deadline)
