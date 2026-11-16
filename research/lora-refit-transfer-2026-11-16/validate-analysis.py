"""Exercise calibration/aggregate/diagnostics/figures with synthetic local data.

All fixtures and outputs stay under local/. No real T outcomes are read and no
fixture is exported as an experiment result.
"""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
from pathlib import Path
from types import SimpleNamespace
import sys
import uuid
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').is_file())
V3=ROOT/'research/kaggle-roadmap-2026-10-31'
sys.path.insert(0,str(V3))
import numpy as np
import pandas as pd
from degron_v3 import local_refit as work
from degron_v3.common import atomic_json,sha256
from degron_v3.local_control import Control


def main():
    root=HERE/'local'/('analysis-validation-'+uuid.uuid4().hex);root.mkdir(parents=True)
    original=work.PROJECT;work.PROJECT=root/'published';work.PROJECT.mkdir()
    try:
        sat=pd.DataFrame(dict(cell_id=[f'w{i}' for i in range(10)],peptide_id=['w1']*5+['w2']*5,
            group_id=['wg1']*5+['wg2']*5,dpsi_mean=np.linspace(-2,2,10),psi_stratum=['le3']*10))
        n=12
        scan=pd.DataFrame(dict(cell_id=[f't{i}' for i in range(n)],peptide_id=['t1']*6+['t2']*6,
            group_id=['tg1']*6+['tg2']*6,wt_sequence=['A'*28]*n,mutant_sequence=['C'+'A'*27]*n,
            position_1based=[1]*n,wt_aa=['A']*n,mut_aa=['C']*n,partition=['scan_T']*n,
            dpsi_rep1=np.linspace(-2,2,n),dpsi_rep2=np.linspace(-1.8,2.2,n),
            dpsi_rep12_mean=np.linspace(-1.9,2.1,n),scan_pair=['A>C']*n))
        (root/'tables').mkdir();scan.to_parquet(root/'tables/scanning-cells.parquet',index=False)
        ds=SimpleNamespace(root=root,sat=sat,identity='fixture',
            peptides=pd.DataFrame(dict(peptide_id=['t1','t2'],psi_wt_scan_rep1=[2.,5.5])))
        config=dict(modes=['lora','frozen'],seeds=[17,29,43],expected_T=dict(cells=12,peptides=2,groups=2))
        lock=dict(folds=[])
        campaign=root/'fixture-campaign';(campaign/'jobs').mkdir(parents=True)
        atomic_json(campaign/'plan.json',dict(config=config))
        for mode in config['modes']:
            for seed in config['seeds']:
                for fold in range(5):
                    rows=sat.iloc[fold*2:fold*2+2].copy()
                    rows['prediction']=rows.dpsi_mean*.8
                    rows['seed']=seed;rows['recipe']=f'esm2_35m-{mode}-D';rows['data_identity']='fixture'
                    path=root/f'{mode}-{seed}-{fold}.parquet';rows.to_parquet(path,index=False)
                    lock['folds'].append(dict(mode=mode,seed=seed,oof=path.relative_to(ROOT).as_posix()))
                score=campaign/'jobs'/f'score-held-{mode}-D-{seed}';score.mkdir()
                np.save(score/'held.npy',scan.dpsi_rep1.to_numpy()*(.9 if mode=='lora' else .7))
                refit=campaign/'jobs'/f'refit-{mode}-D-{seed}';refit.mkdir()
                np.save(refit/'final-w.npy',sat.dpsi_mean.to_numpy()*.85)
            out=campaign/'jobs'/f'calibrate-final-{mode}-D';out.mkdir()
            work.calibrate(ds,dict(mode=mode),out,lock)
        baseline=scan[['cell_id','dpsi_rep1']].rename(columns={'dpsi_rep1':'dpsi_mean'})
        baseline['prediction']=baseline.dpsi_mean*.6
        baseline['p_minus']=.2;baseline['p_neutral']=.6;baseline['p_plus']=.2
        path=root/'baseline.parquet';baseline.to_parquet(path,index=False)
        lock['w5_baseline']=path.relative_to(ROOT).as_posix()
        out=campaign/'jobs/aggregate-refit';out.mkdir()
        control=Control(campaign,'aggregate')
        work.aggregate(ds,campaign,out,control,config,lock)
        results=work.read(out/'results.json')
        assert results['denominators']==config['expected_T']
        assert len(results['contrasts'])==2 and all(v['multiplicity']==2 for v in results['contrasts'].values())
        assert results['metrics']['esm2_35m-lora-D']['all']['mae']<results['metrics']['esm2_35m-frozen-D']['all']['mae']
        out=campaign/'jobs/analyze-errors';out.mkdir();work.errors(ds,campaign,out,control)
        out=campaign/'jobs/figure-export';out.mkdir();work.figures(campaign,out,control)
        assert len(list((work.PROJECT/'figures').glob('*.png')))==3
        atomic_json(HERE/'analysis-validation.json',dict(status='pass',scope='synthetic_software_fixture_not_scientific_results',
            real_T_outcomes_read=False,tests=['OOF_ensemble_calibrator','aggregate_seed_ensemble_and_baselines',
                'two_paired_group_contrasts','replicate_intersection','error_diagnostics','three_figure_exports'],
            synthetic_results_path=root.relative_to(ROOT).as_posix(),
            implementation_sha256=sha256(Path(work.__file__))))
        print('ANALYSIS VALIDATION PASS:',root)
    finally:
        work.PROJECT=original


if __name__=='__main__':main()
