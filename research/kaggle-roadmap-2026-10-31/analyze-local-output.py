"""Audit completed local artifacts and derive development results without loading models.

Writes only local-output-analysis.{json,md,png} beside this script. Imported and
inherited campaign artifacts, model checkpoints and the dataset stay read-only.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
import gc
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf8')

import numpy as np
import pandas as pd
from degron_v3.data import Dataset
from degron_v3.metrics import per_peptide, paired_ci

METRICS = ['mae','rmse','spearman','auroc_plus','auprc_plus','auroc_minus','auprc_minus']
META = ['peptide_id','group_id','outer_fold','psi_stratum','dpsi_mean']
SEEDS = [17,29,43]
PROBS = ['p_minus','p_neutral','p_plus']


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def summarize(pp):
    def one(rows):
        out = dict(peptides=len(rows),clusters=int(rows.group_id.nunique()),cells=int(rows.n.sum()))
        for key in METRICS:
            valid=rows[key].dropna()
            out[key]=float(valid.mean()) if len(valid) else None
            out[key+'_eligible_peptides']=len(valid)
        return out
    return dict(all=one(pp),strata={str(k):one(v) for k,v in pp.groupby('psi_stratum',observed=True)})


def assert_metrics(actual, expected):
    for key in METRICS:
        if expected[key] is None:
            assert actual[key] is None, key
        else:
            assert abs(actual[key]-expected[key])<1e-10,(key,actual[key],expected[key])


def class_labels(values):
    return np.where(np.asarray(values)<=-1,0,np.where(np.asarray(values)>=1,2,1))


class Analysis:
    def __init__(self, campaign):
        self.campaign=campaign.resolve()
        self.plan=read(campaign/'plan.json')
        self.state=read(campaign/'state.json')
        self.queue=read(campaign/'queue.json')
        self.dataset=Dataset(HERE.parents[1]/'data/processed/v3-fullpsi')
        assert self.dataset.identity==self.plan['data_identity']
        self.reference=self.dataset.sat.set_index('cell_id')[META].sort_index()
        assert len(self.reference)==122412
        assert self.reference.groupby('group_id').outer_fold.nunique().max()==1
        self.hashes={}
        self.pp={}
        self.predictions={}
        self.result=dict(generated_local=datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
            campaign=campaign.name,data_identity=self.dataset.identity,scientific_status='development_not_gate_closure',
            analysis_script_sha256=digest(__file__),source_files={})

    def source(self,path):
        path=Path(path).resolve()
        assert path.is_relative_to(HERE.resolve())
        key=path.relative_to(HERE).as_posix()
        if key not in self.result['source_files']:
            self.result['source_files'][key]=dict(bytes=path.stat().st_size,sha256=self.hash(path))
        return path

    def hash(self,path):
        path=Path(path).resolve()
        if path not in self.hashes:self.hashes[path]=(path.stat().st_size,digest(path))
        return self.hashes[path][1]

    def folder(self,job):
        record=self.state['jobs'][job]
        return Path(record.get('artifact_campaign',self.campaign))/'jobs'/job

    def integrity(self):
        assert {j['id'] for j in self.queue}==set(self.state['jobs'])
        counts=dict(Counter(v['status'] for v in self.state['jobs'].values()))
        assert counts==dict(complete=633,source_pending=1,structure_pending=1),counts
        references=0
        local_paths=set()
        for name,record in self.state['jobs'].items():
            if record['status']!='complete':continue
            origin=Path(record.get('artifact_campaign',self.campaign)).resolve()
            assert origin.parent==self.campaign.parent
            if origin!=self.campaign:
                assert self.hash(origin/'plan.json')==record['source_plan_sha256']
            for entry in record['files']:
                path=(origin/entry['path']).resolve()
                assert path.is_relative_to(origin)
                assert path.is_file() and path.stat().st_size==entry['bytes'],str(path)
                assert self.hash(path)==entry['sha256'],str(path)
                local_paths.add(path)
                references+=1
        lineage=read(self.source(self.campaign/'inheritance.json'))
        old=Path(lineage['source_campaign'])
        assert self.hash(old/'state.json')==lineage['source_state_sha256']
        kaggle=HERE/'output/official'/self.plan['source_campaign']
        manifest=read(self.source(kaggle/'pipeline-manifest.json'))
        kpaths=set()
        for task in manifest['tasks'].values():
            if task['status']!='complete':continue
            for e in task['files']:
                p=(kaggle/e['path']).resolve()
                assert p.is_relative_to(kaggle.resolve()) and p.stat().st_size==e['bytes']
                assert self.hash(p)==e['sha256'],str(p)
                kpaths.add(p)
        self.kaggle=kaggle
        self.old_analysis=read(self.source(HERE/'output-analysis.json'))
        assert self.old_analysis['source_manifest_sha256']==self.hash(kaggle/'pipeline-manifest.json')
        assert self.old_analysis['data_identity']==self.dataset.identity
        for name in ('plan.json','state.json','queue.json','session.json'):
            self.source(self.campaign/name)
        self.result['integrity']=dict(status='pass',local_complete_jobs=633,state_counts=counts,
            local_artifact_references=references,local_unique_artifacts=len(local_paths),
            local_bytes_checked=sum(self.hashes[p][0] for p in local_paths),
            inherited_source_state_unchanged=True,inherited_complete_jobs=lineage['inherited_complete'],
            kaggle_complete_files_checked=len(kpaths),kaggle_bytes_checked=sum(self.hashes[p][0] for p in kpaths),
            mismatches=[],note='Checks cover saved artifacts and recorded metadata, not a new homology or wet-lab audit.')
        print('PASS artifact hashes and source lineage',flush=True)

    def oof(self,path,key,reported=None,full_metrics_per_seed=False):
        path=self.source(path)
        frame=pd.read_parquet(path)
        assert set(frame['mode'])=={'official'} and set(frame.data_identity)=={self.dataset.identity}
        assert sorted(frame.seed.unique())==SEEDS
        assert not frame.duplicated(['seed','cell_id']).any() and np.isfinite(frame.prediction).all()
        seed_reports={}
        for seed,rows in frame.groupby('seed'):
            meta=rows.set_index('cell_id')[META].sort_index()
            pd.testing.assert_frame_equal(meta,self.reference,check_dtype=False,check_exact=True)
            mae=float(rows.assign(error=(rows.prediction-rows.dpsi_mean).abs()).groupby('peptide_id').error.mean().mean())
            if reported and 'per_seed' in reported:
                assert abs(mae-reported['per_seed'][str(seed)]['all']['mae'])<1e-10
            seed_reports[str(seed)]=dict(mae=mae)
            if full_metrics_per_seed:
                pp=per_peptide(rows,rows.prediction.to_numpy())
                seed_reports[str(seed)]=summarize(pp)['all']
                if reported and 'per_seed' in reported:
                    assert_metrics(seed_reports[str(seed)],reported['per_seed'][str(seed)]['all'])
        mean=frame.groupby('cell_id').prediction.mean().reindex(self.reference.index)
        pp=per_peptide(self.reference.reset_index(),mean.to_numpy())
        measured=summarize(pp)
        if reported:assert_metrics(measured['all'],reported['ensemble']['all'])
        self.pp[key]=pp
        self.predictions[key]=mean.to_numpy()
        return dict(seeds=SEEDS,oof_rows=len(frame),ensemble=measured,per_seed=seed_reports)

    def local_results(self):
        recipes={}
        for group in ('collect-family','collect-core'):
            folder=self.campaign/'jobs'/group
            collection=read(self.source(folder/'collection.json'))
            assert collection['data_identity']==self.dataset.identity and collection['mode']=='official'
            for recipe,reported in collection['reports'].items():
                key='local:'+recipe
                recipes[recipe]=self.oof(folder/(recipe+'-oof.parquet'),key,reported,group=='collect-core')
                recipes[recipe]['group']=group
                print(recipe,round(recipes[recipe]['ensemble']['all']['mae'],6),flush=True)
        assert len(recipes)==41
        family_summary=pd.read_csv(self.source(self.campaign/'jobs/collect-family/summary.csv'))
        core_summary=pd.read_csv(self.source(self.campaign/'jobs/collect-core/summary.csv'))
        benchmark=pd.read_csv(self.source(self.campaign/'jobs/report/benchmark.csv'))
        assert not benchmark.duplicated(['platform','recipe']).any()
        assert len(benchmark)==88
        for _,row in pd.concat([family_summary,core_summary]).iterrows():
            assert_metrics(recipes[row.recipe]['ensemble']['all'],row.to_dict())
            match=benchmark[(benchmark.platform=='local')&(benchmark.recipe==row.recipe)]
            assert len(match)==1
            assert_metrics(match.iloc[0].to_dict(),row.to_dict())
        # Verify nested choices against the actual saved inner MSE, not outer scores.
        collection=read(self.campaign/'jobs/collect-family/collection.json')
        choices=collection['reports']['nested-family-selection']['choices']
        selected=Counter()
        for choice in choices:
            options=[]
            for job in self.queue:
                if job['kind']=='ridge' and job['seed']==choice['seed'] and job['fold']==choice['fold']:
                    fit=read(self.folder(job['id'])/'fit.json')
                    options.append((fit['validation_mse'],fit['recipe']))
            best=min(options)
            assert (choice['validation_mse'],choice['recipe'])==best
            selected[choice['recipe']]+=1
        self.result['local_recipes']=recipes
        self.result['nested_selection']=dict(choices=choices,counts=dict(selected),inner_mse_argmin_verified=True)
        for recipe in ('ordered-w5-D','esm2_35m-cnn-D','esm2_35m-mcnn-E'):
            original=self.old_analysis['recipes'][recipe]
            paths=[self.kaggle/p for p in original['files']]
            frames=[pd.read_parquet(self.source(p)) for p in paths]
            # Kaggle stage05 artifacts can be one file per seed.
            frame=pd.concat(frames,ignore_index=True)
            assert sorted(frame.seed.unique())==SEEDS and not frame.duplicated(['seed','cell_id']).any()
            for _,rows in frame.groupby('seed'):
                pd.testing.assert_frame_equal(rows.set_index('cell_id')[META].sort_index(),self.reference,
                                               check_dtype=False,check_exact=True)
            mean=frame.groupby('cell_id').prediction.mean().reindex(self.reference.index).to_numpy()
            key='kaggle:'+recipe
            self.pp[key]=per_peptide(self.reference.reset_index(),mean)
            self.predictions[key]=mean
            assert_metrics(summarize(self.pp[key])['all'],original['ensemble']['all'])
        top=benchmark.sort_values('mae').head(15).astype(object)
        self.result['benchmark_top']=top.where(pd.notna(top),None).to_dict(orient='records')
        self.result['benchmark_rows']=dict(local=len(family_summary)+len(core_summary),kaggle=47,total=len(benchmark))

    def contrasts(self):
        result={}
        def compare(a,b,metric='mae',multiplicity=1,role='posthoc_development',stratum=None):
            left,right=self.pp[a],self.pp[b]
            if stratum:
                left=left[left.psi_stratum==stratum];right=right[right.psi_stratum==stratum]
            key=f'{a} minus {b}; {metric}'+(f'; {stratum}' if stratum else '')
            result[key]=dict(a=a,b=b,metric=metric,stratum=stratum,role=role,
                **paired_ci(left,right,metric,multiplicity=multiplicity))
            return result[key]
        original=read(self.source(self.campaign/'jobs/collect-core/comparisons.json'))
        for arm in 'BD':
            for metric in ('mae','auroc_plus'):
                measured=compare('local:esm2_35m-lora-'+arm,'local:esm2_35m-frozen-'+arm,metric,4,
                    'matched_local_contrast; adjusted CI is a conservative posthoc family of four')
                supplied=original[f'lora-frozen-{arm}-{metric}']
                assert abs(measured['delta']-supplied['delta'])<1e-12
                assert np.allclose(measured['ci95'],supplied['ci95'],atol=1e-12,rtol=0)
        for mode in ('frozen','lora'):
            compare(f'local:esm2_35m-{mode}-D',f'local:esm2_35m-{mode}-B')
        for arm in 'BD':
            for other in ('kaggle:ordered-w5-D','kaggle:esm2_35m-cnn-D','local:nested-family-selection'):
                compare('local:esm2_35m-lora-'+arm,other)
        compare('local:nested-family-selection','kaggle:ordered-w5-D')
        for model in self.plan['config']['models']:
            compare(f'local:{model}-context-D',f'local:{model}-only-D')
        for stratum in ('le3','gt3_le4','gt4_le5','gt5'):
            compare('local:esm2_35m-lora-D','local:esm2_35m-lora-B',stratum=stratum)
        self.result['contrasts']=result

    def calibration(self):
        results={}
        self.reliability={}
        for recipe in self.result['local_recipes']:
            if not recipe.startswith(('esm2_35m-frozen-','esm2_35m-lora-')):continue
            folder=self.campaign/'jobs/calibrate-core'/recipe
            card=read(self.source(folder/'model-card.json'))
            lock=read(self.source(folder/'selection-lock.json'))
            assert lock['recipe']==recipe and lock['data_identity']==self.dataset.identity
            assert lock['input_oof_sha256']==self.hash(self.campaign/'jobs/collect-core'/(recipe+'-oof.parquet'))
            raw=pd.read_parquet(self.source(folder/'calibrated-oof.parquet'))
            assert not raw.duplicated(['seed','cell_id']).any()
            priors=[]
            for (seed,fold),rows in raw.groupby(['seed','outer_fold']):
                inner=pd.read_parquet(self.campaign/'jobs/collect-core'/f'{recipe}-seed{seed}-fold{fold}-calibration.parquet')
                assert not set(inner.group_id)&set(rows.group_id)
                counts=np.bincount(class_labels(inner.dpsi_mean),minlength=3)
                prior=counts/counts.sum()
                null=rows[['cell_id']].copy()
                for i,p in enumerate(PROBS):null[p]=prior[i]
                priors.append(null)
            mean=raw.groupby('cell_id')[['prediction']+PROBS].mean().reindex(self.reference.index)
            assert np.allclose(mean.prediction,self.predictions['local:'+recipe],atol=0,rtol=0)
            probabilities=mean[PROBS].to_numpy()
            assert np.isfinite(probabilities).all() and (probabilities>=0).all() and (probabilities<=1).all()
            assert np.allclose(probabilities.sum(1),1,atol=1e-12)
            labels=class_labels(self.reference.dpsi_mean)
            targets=np.eye(3)[labels]
            brier=np.square(probabilities-targets).sum(1)
            assert abs(float(brier.mean())-card['multiclass_brier'])<1e-10
            null=pd.concat(priors).groupby('cell_id')[PROBS].mean().reindex(self.reference.index).to_numpy()
            null_brier=np.square(null-targets).sum(1)
            work=self.reference.reset_index()[['peptide_id','group_id']].copy()
            work['brier']=brier
            peptide=work.groupby(['peptide_id','group_id'],as_index=False).brier.mean()
            self.pp['calibration:'+recipe]=peptide
            bins=[]
            positive=(labels==2).astype(float)
            for i in range(10):
                mask=(probabilities[:,2]>=i/10)&(probabilities[:,2]<((i+1)/10) if i<9 else probabilities[:,2]<=1)
                if mask.any():bins.append(dict(bin=i,n=int(mask.sum()),mean_probability=float(probabilities[mask,2].mean()),observed_rate=float(positive[mask].mean())))
            self.reliability[recipe]=bins
            results[recipe]=dict(multiclass_brier_cell_micro=float(brier.mean()),multiclass_brier_peptide_macro=float(peptide.brier.mean()),
                inner_prior_brier_cell_micro=float(null_brier.mean()),positive_ece_cell_micro=sum(b['n']*abs(b['mean_probability']-b['observed_rate']) for b in bins)/len(labels),
                observed_positive_rate=float(positive.mean()),mean_positive_probability=float(probabilities[:,2].mean()),
                reliability_bins=bins,final_promotion_status=card['final_promotion_status'],model_ids=card['model_ids'])
        for arm in 'BD':
            a=self.pp['calibration:esm2_35m-lora-'+arm]
            b=self.pp['calibration:esm2_35m-frozen-'+arm]
            results['lora_minus_frozen_'+arm]=dict(role='posthoc_macro_Brier_comparison',**paired_ci(a,b,'brier'))
        self.result['calibration']=results

    def transfer(self):
        folder=self.campaign/'jobs/locked-transfer-w5/ordered-w5-D'
        card=read(self.source(folder/'model-card.json'))
        lock=read(self.source(folder/'selection-lock.json'))
        assert lock['recipe']=='ordered-w5-D' and lock['data_identity']==self.dataset.identity
        source_oof=self.kaggle/'tasks/01-78cc356ba4f4/ordered-w5-D-oof.parquet'
        assert lock['input_oof_sha256']==self.hash(source_oof)
        held=pd.read_parquet(self.source(folder/'held-scanning.parquet'))
        assert set(held.partition)=={'scan_T'} and not held.cell_id.duplicated().any()
        original=self.dataset.scanning(include_held=True)
        expected=original[(original.partition=='scan_T')&original.dpsi_rep1.notna()].set_index('cell_id')
        assert set(held.cell_id)==set(expected.index)
        assert np.array_equal(held.dpsi_mean.to_numpy(),expected.reindex(held.cell_id).dpsi_rep1.to_numpy())
        assert not set(held.group_id)&set(self.reference.group_id)
        assert not set(held.group_id)&set(original.loc[original.partition=='scan_dev','group_id'])
        model=per_peptide(held,held.prediction.to_numpy())
        zero=per_peptide(held,np.zeros(len(held)))
        assert_metrics(summarize(model)['all'],card['held']['all'])
        probabilities=held[PROBS].to_numpy()
        assert np.isfinite(probabilities).all() and np.allclose(probabilities.sum(1),1)
        y=class_labels(held.dpsi_mean)
        train_prior=np.bincount(class_labels(self.reference.dpsi_mean),minlength=3)/len(self.reference)
        self.result['transfer']=dict(recipe='ordered-w5-D',population=summarize(model),
            zero_baseline=summarize(zero),model_minus_zero_mae=paired_ci(model,zero,'mae'),
            substitutions=held.mut_aa.value_counts().to_dict(),no_group_overlap_with_W_or_scan_dev=True,
            multiclass_brier_cell_micro=float(np.square(probabilities-np.eye(3)[y]).sum(1).mean()),
            development_prior_brier_cell_micro=float(np.square(train_prior-np.eye(3)[y]).sum(1).mean()),
            observed_positive_rate=float((y==2).mean()),mean_positive_probability=float(probabilities[:,2].mean()),
            trained_cells=card['trained_cells'],final_alpha=card['final_alpha'],
            model_inference_seconds=card['inference_seconds'],lora_evaluated_on_T=False,
            limitation='Previously explored same-lab scanning, R/A/S substitutions, rep1 endpoint; not independent external or clinical validation.')

    def finish(self):
        self.result['limitations']=[
            'This is analysis of an already explored development benchmark; no automatic product selection or G2/G3 closure.',
            'Local/Kaggle share observations. Do not concatenate them as independent samples or average their reported metrics.',
            'Main matched frozen-LoRA results use the same local runtime, splits, seeds and head initialization.',
            'Four matched comparisons have nominal 95% CIs; additional Bonferroni intervals are posthoc and do not create a preregistration.',
            'B restricts training PSI, while validation/test cover the full PSI range.',
            'AUROC/AP use only peptides with >=3 observations in both classes; missing metrics are not zeros.',
            'The calibration card Brier is a three-class cell-micro score, unlike historical binary P6 Brier.',
            'Only W5-D has locked T evaluation/final refit here. LoRA/family/CNN final serving exports remain open.',
            'Model cards currently have an empty model_ids list; recipe/base revision/provenance must be completed before a serving release.',
            'source_pending and structure_pending remain unresolved; artifact integrity does not prove biological independence.',
            'Metric recomputation reuses reviewed runner per_peptide/paired_ci helpers; it is not an independently implemented metric library.',
        ]
        assert self.hash(self.campaign/'state.json')==digest(self.campaign/'state.json'),'Campaign changed during analysis'
        target=HERE/'local-output-analysis.json'
        target.write_text(json.dumps(self.result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
        write_report(self.result)
        plot(self.result,self.reliability)
        print('Saved local-output-analysis.json/.md/.png',flush=True)


def format_ci(row,adjusted=False):
    values=row['ci_adjusted' if adjusted else 'ci95']
    return f"{row['delta']:+.6f} [{values[0]:+.6f}; {values[1]:+.6f}]"


def write_report(r):
    rec=r['local_recipes'];contrasts=r['contrasts']
    lines=['# Phân tích campaign local hoàn tất — 06/11/2026','',
        '**[ĐO đã lưu và tái tính]** Campaign `'+r['campaign']+'` hoàn tất 633 job, còn `source_pending` và `structure_pending`. LoRA ESM2-35M cải thiện so với frozen trong phép so cùng runtime local; chưa có kiểm chứng T cho LoRA hoặc model LoRA cuối để phục vụ.',
        '', 'Nguồn số và phương pháp: [local-output-analysis.json](local-output-analysis.json); mã tái tạo: [analyze-local-output.py](analyze-local-output.py). Báo cáo chỉ đọc output/data, không huấn luyện lại hoặc sửa campaign. Các phép so mới mang vai trò development/hậu kiểm.',
        '', '## 1. Kiểm tra tính toàn vẹn và độ đầy đủ','',
        f"- [ĐO] Kiểm {r['integrity']['local_artifact_references']:,} artifact local và {r['integrity']['kaggle_complete_files_checked']:,} file Kaggle hoàn tất bằng size/SHA-256: không sai lệch; trạng thái nguồn kế thừa giữ nguyên.",
        '- [ĐO] 41 recipe local (36 pLM/Ridge + quy trình chọn nested + 4 frozen/LoRA), đủ seed 17/29/43. Mỗi seed có cùng 122.412 ô, 235 peptide, 221 nhóm; không trùng `(seed, cell_id)`, điểm hữu hạn, nhãn/fold khớp bundle. Metric ensemble được tái tính và khớp báo cáo gốc trong dung sai 1e-10.',
        '- [ĐO] Bảng chung có 88 hàng: 41 local + 47 Kaggle. Nguồn/platform được giữ riêng. Một số hàng Kaggle stage11 chỉ có seed 17, không được so như ensemble ba seed.',
        '', '## 2. Phép so frozen–LoRA cùng runtime','',
        'MAE macro theo peptide (thấp hơn tốt hơn); AUROC/AP dương dùng nhãn đo ΔPSI ≥ 1. MAE có 235 peptide, AUROC/AP dương có 184 peptide đủ điều kiện; AUROC âm có 110 peptide. B: train PSI≤4; D: train toàn dải; validation/test chung toàn dải.',
        '', '| Recipe | MAE | AUROC + | AP + | AUROC − |','|---|---:|---:|---:|---:|']
    for mode in ('frozen','lora'):
        for arm in 'BD':
            key=f'esm2_35m-{mode}-{arm}';v=rec[key]['ensemble']['all']
            lines.append(f"| {key} | {v['mae']:.6f} | {v['auroc_plus']:.6f} | {v['auprc_plus']:.6f} | {v['auroc_minus']:.6f} |")
    lines+=['','[ĐO] Chênh lệch **LoRA − frozen**, ensemble ba seed, bootstrap 5.000 lần theo nhóm protein. Dấu âm MAE và dấu dương AUROC là cải thiện. CI hiệu chỉnh 98,75% là Bonferroni hậu kiểm cho bốn phép so; CI gốc 95% được giữ riêng.','','| Điều kiện/chỉ số | Δ và CI 95% | Δ và CI hiệu chỉnh |','|---|---|---|']
    for arm in 'BD':
        for metric in ('mae','auroc_plus'):
            row=contrasts[f'local:esm2_35m-lora-{arm} minus local:esm2_35m-frozen-{arm}; {metric}']
            lines.append(f'| {arm} / {metric} | {format_ci(row)} | {format_ci(row,True)} |')
    lines+=['','[DIỄN GIẢI] Đây là bằng chứng development cho ích lợi của LoRA trong thiết kế đã thử. Mỗi seed cũng phải được đọc riêng; lợi ích ensemble không biến ba seed thành ba bộ dữ liệu độc lập.','','| Recipe | MAE seed 17 | MAE seed 29 | MAE seed 43 | MAE ensemble |','|---|---:|---:|---:|---:|']
    for key in ('esm2_35m-frozen-B','esm2_35m-frozen-D','esm2_35m-lora-B','esm2_35m-lora-D'):
        v=rec[key];lines.append('| '+key+' | '+' | '.join(f"{v['per_seed'][str(s)]['mae']:.6f}" for s in SEEDS)+f" | {v['ensemble']['all']['mae']:.6f} |")
    row=contrasts['local:esm2_35m-lora-D minus local:esm2_35m-lora-B; mae']
    lines+=['',f"[ĐO] LoRA D−B, MAE: {format_ci(row)}. Không chọn B chỉ từ vị trí đứng đầu bảng nếu CI ghép cặp chưa phân biệt được.",'','| Miền PSI(WT) test | n peptide | LoRA-B MAE | LoRA-D MAE |','|---|---:|---:|---:|']
    for s in ('le3','gt3_le4','gt4_le5','gt5'):
        a=rec['esm2_35m-lora-B']['ensemble']['strata'][s];b=rec['esm2_35m-lora-D']['ensemble']['strata'][s]
        lines.append(f"| {s} | {a['peptides']} | {a['mae']:.6f} | {b['mae']:.6f} |")
    lines+=['','[DIỄN GIẢI] B/D có đánh đổi theo miền PSI; miền >5 chỉ có 23 peptide và không có AUROC dương đủ điều kiện. MAE toàn W gần nhau không đồng nghĩa hành vi trên mọi miền giống nhau.','','## 3. Khảo sát pLM và so với kết quả Kaggle','','| pLM | MAE only-D | MAE context-D | AUROC + context-D |','|---|---:|---:|---:|']
    models=sorted({k.removesuffix('-context-D') for k in rec if k.endswith('-context-D')},key=lambda k:rec[k+'-context-D']['ensemble']['all']['mae'])
    for model in models:
        a=rec[model+'-only-D']['ensemble']['all'];b=rec[model+'-context-D']['ensemble']['all']
        lines.append(f"| {model} | {a['mae']:.6f} | {b['mae']:.6f} | {b['auroc_plus']:.6f} |")
    n=rec['nested-family-selection']['ensemble']['all']
    lines+=['',f"[ĐO] Nested selection: MAE {n['mae']:.6f}, AUROC dương {n['auroc_plus']:.6f}. Cả 15 lựa chọn seed/fold khớp argmin inner MSE từ artifact gốc; số lần chọn từng recipe nằm trong JSON. Đây là điểm của quy trình chọn, không phải một model cố định.",
        '', '[DIỄN GIẢI] Không có quan hệ đơn điệu giữa kích thước pLM và chất lượng trong bảng này. ProtT5/Ankh đã có kết quả thật; Ankh encoder FP32, feature lưu FP16, khác precision inference của các pLM FP16. Context/only có phép so ghép cặp ở JSON; không quy toàn bộ chênh lệch cho một cơ chế sinh học.',
        '', '| Phép so MAE (hậu kiểm development) | Δ và CI 95% |','|---|---|']
    for key in ('local:nested-family-selection minus kaggle:ordered-w5-D; mae',
                'local:esm2_35m-lora-B minus kaggle:ordered-w5-D; mae',
                'local:esm2_35m-lora-B minus kaggle:esm2_35m-cnn-D; mae'):
        lines.append(f'| {key.removesuffix("; mae")} | {format_ci(contrasts[key])} |')
    lines+=['','Các hàng Kaggle/local dùng cùng cohort và nhãn/fold đã đối chiếu, nhưng khác runtime và có thể khác kiến trúc/ngân sách. Đây không phải phép tách nhân quả chỉ riêng LoRA so với CNN; không cộng hai platform thành mẫu độc lập.','','## 4. Hiệu chuẩn xác suất','','Brier dưới đây là **ba lớp** (Δ≤−1, trung tính, Δ≥1), không so trực tiếp với Brier nhị phân P6 lịch sử. Card gốc báo cell-micro; macro theo peptide được ghi riêng. Baseline hằng chỉ học tần suất lớp ở inner-validation của đúng fold, rồi ensemble ba seed; không học nhãn outer-test.','','| Recipe | Brier cell-micro | Brier peptide-macro | Baseline inner-prior micro | ECE dương micro |','|---|---:|---:|---:|---:|']
    for key in ('esm2_35m-frozen-B','esm2_35m-frozen-D','esm2_35m-lora-B','esm2_35m-lora-D'):
        v=r['calibration'][key]
        lines.append(f"| {key} | {v['multiclass_brier_cell_micro']:.6f} | {v['multiclass_brier_peptide_macro']:.6f} | {v['inner_prior_brier_cell_micro']:.6f} | {v['positive_ece_cell_micro']:.6f} |")
    lines+=['','[DIỄN GIẢI] LoRA có Brier thấp hơn frozen, nhưng ECE dương theo cách chia bin này cao hơn frozen. Brier kết hợp chất lượng phân biệt và hiệu chuẩn; không kết luận mọi khía cạnh hiệu chuẩn của LoRA đều tốt hơn chỉ từ Brier.',
        '', '[ĐO/giới hạn] Xác suất hữu hạn, tổng ba lớp bằng 1; card Brier tái tính khớp. Nhóm inner calibration không giao outer-test. Đây là calibration CV, chưa có final LoRA/CNN/family model phục vụ. `model_ids` trong các card hiện đang rỗng, cần hoàn thiện provenance khi đóng gói model.','','## 5. Locked transfer W5-D trên scan_T','']
    t=r['transfer'];m=t['population']['all'];z=t['zero_baseline']['all']
    lines += [f"[ĐO] {m['cells']:,} ô / {m['peptides']:,} peptide / {m['clusters']} nhóm, chỉ phép thay R/A/S. Nhãn rep1; không giao group_id với W hoặc scan_dev. Recipe W5-D và input OOF khớp selection lock.",
        '', '| Chỉ số | Kết quả |','|---|---:|',f"| MAE W5-D | {m['mae']:.6f} |",f"| MAE dự đoán hằng 0 | {z['mae']:.6f} |",f"| W5-D − zero, MAE và CI 95% | {format_ci(t['model_minus_zero_mae'])} |",f"| AUROC dương / peptide đủ điều kiện | {m['auroc_plus']:.6f} / {m['auroc_plus_eligible_peptides']} |",f"| AUROC âm / peptide đủ điều kiện | {m['auroc_minus']:.6f} / {m['auroc_minus_eligible_peptides']} |",f"| Brier ba lớp cell-micro trên T | {t['multiclass_brier_cell_micro']:.6f} |",f"| Tần suất dương đo / xác suất dương trung bình | {t['observed_positive_rate']:.6f} / {t['mean_positive_probability']:.6f} |",
        '', '[DIỄN GIẢI] CI của ΔMAE so với zero cắt 0: chưa đủ bằng chứng W5-D giảm MAE trên T so với baseline này. AUROC âm gần 0,5 trên 85 peptide đủ điều kiện. Xác suất dương trung bình cũng cao hơn tần suất đo trên T, nên cần xem chuyển miền xác suất cùng khả năng xếp hạng.',
        '', 'T là scanning cùng phòng thí nghiệm, đã được khảo sát ở mức nguồn; khác thiết kế saturation 19 phép thay. Không gọi đây là external độc lập/kiểm chứng lâm sàng. **LoRA chưa được chấm trên T**; kết quả W5-D không chứng minh transfer của LoRA.',
        '', '## 6. Việc còn lại','',
        '1. [ĐỀ XUẤT] Giữ LoRA-B và LoRA-D là ứng viên development; chốt mục tiêu/miền sử dụng và quy tắc lựa chọn trước đánh giá tiếp. Bảng OOF không tự chọn model sản phẩm.',
        '2. [CHƯA LÀM] Final refit/export đúng kiến trúc cho model được chọn, đầy đủ revision/tokenizer/precision/calibrator/model card và kiểm suy luận độc lập.',
        '3. [CHƯA LÀM] Protocol đánh giá tiếp cho LoRA; không dùng T đã xem để chọn nhiều model rồi gọi là kiểm chứng độc lập.',
        '4. [PENDING] Nguồn ngoài và cấu trúc thật; không đổi nhãn hoặc giả dữ liệu để đóng hai trạng thái này.',
        '5. [ĐỀ XUẤT] Đưa kết quả đã kiểm vào luận văn khi yêu cầu cập nhật nội dung; giữ giới hạn development và kết quả âm. App baseline chưa thay model, G2/G3 chưa tự đóng.',
        '', '![Development results](local-output-analysis.png)','', '## Tái tạo','', '```powershell',
        '.\\.venv\\Scripts\\python.exe -I research/kaggle-roadmap-2026-10-31/analyze-local-output.py',
        '```','', 'Cần giữ output Kaggle, campaign local nguồn, successor và bundle dữ liệu. Script kiểm hash, đọc Parquet/JSON, ghi các file phân tích bên cạnh; không load checkpoint/model hoặc sửa output nguồn.']
    (HERE/'local-output-analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf8')


def plot(r,reliability):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(13,10),layout='constrained')
    rec=r['local_recipes'];keys=[f'esm2_35m-{m}-{a}' for m in ('frozen','lora') for a in 'BD']
    colors=['#7c8b99','#a0aab3','#127c80','#67a9a5']
    axes[0,0].bar(['Frozen B','Frozen D','LoRA B','LoRA D'],[rec[k]['ensemble']['all']['mae'] for k in keys],color=colors)
    axes[0,0].set(ylabel='Peptide-macro MAE (PSI)',ylim=(0,.45),title='A. Matched local, three-seed ensemble')
    for i,k in enumerate(keys):axes[0,0].text(i,rec[k]['ensemble']['all']['mae']+.004,f"{rec[k]['ensemble']['all']['mae']:.4f}",ha='center')
    ax=axes[0,1]
    for i,arm in enumerate('BD'):
        v=r['contrasts'][f'local:esm2_35m-lora-{arm} minus local:esm2_35m-frozen-{arm}; mae']
        lo,hi=v['ci_adjusted'];ax.errorbar(v['delta'],i,xerr=[[v['delta']-lo],[hi-v['delta']]],fmt='o',color='#127c80',capsize=5)
    ax.axvline(0,color='gray',linestyle='--');ax.set(yticks=[0,1],yticklabels=['B','D'],xlabel='Delta MAE: LoRA - frozen',title='B. Group bootstrap; posthoc 98.75% CIs')
    models=sorted({k.removesuffix('-context-D') for k in rec if k.endswith('-context-D')},key=lambda m:rec[m+'-context-D']['ensemble']['all']['mae'])
    ax=axes[1,0];ax.barh(models,[rec[m+'-context-D']['ensemble']['all']['mae'] for m in models],color='#899eae');ax.invert_yaxis();ax.set(xlabel='Peptide-macro MAE',title='C. Frozen pLM + context Ridge, arm D',xlim=(0,.45))
    ax=axes[1,1]
    for key in ('esm2_35m-lora-B','esm2_35m-lora-D'):
        bins=reliability[key];ax.plot([b['mean_probability'] for b in bins],[b['observed_rate'] for b in bins],'o-',label=key.removeprefix('esm2_35m-'))
    ax.plot([0,1],[0,1],'--',color='gray');ax.set(xlim=(0,1),ylim=(0,1),xlabel='Mean P(delta PSI >= 1)',ylabel='Observed fraction',title='D. CV reliability, cell-weighted bins');ax.legend()
    fig.suptitle('Degron-footprint: completed local development campaign (6 Nov 2026)',fontsize=15)
    fig.savefig(HERE/'local-output-analysis.png',dpi=160)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign',type=Path,default=HERE/'output/local/ef138c84579c842e')
    args=parser.parse_args()
    analysis=Analysis(args.campaign)
    analysis.integrity()
    analysis.local_results()
    analysis.contrasts()
    analysis.calibration()
    analysis.transfer()
    analysis.finish()


if __name__=='__main__':main()
