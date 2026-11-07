"""Independent count/metric readbacks and workspace-scope checks for this audit."""
from pathlib import Path
import ast
import csv
import hashlib
import json
import re
import subprocess
import numpy as np
import pandas as pd
import openpyxl
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedGroupKFold

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
RAW=TOPIC/'data/raw/metadegron';checks=[]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((HERE/n).read_text())
def check(name,passed,detail=None):
    checks.append({'check':name,'passed':bool(passed),'detail':detail})
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)

def main():
    d=load('dataset-audit.json');o=load('overlap-audit.json');b=load('composition-baseline.json');x=load('safe-x-reproduction.json')
    with (RAW/'repo/data/degron_data.txt').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    check('positive-count-csv-vs-pandas',len(rows)==d['positive']['rows']==302)
    check('accessions-two-counts',len({r['Entry'] for r in rows})==d['positive']['proteins_by_accession']==240)
    check('human-count-independent',sum(r['Entry name'].endswith('_HUMAN') for r in rows)==227)
    workbook=openpyxl.load_workbook(RAW/'supplementary/supplementary_table_s2_bbae519.xlsx',read_only=True,data_only=True)
    excel=list(workbook.active.iter_rows(min_row=3,values_only=True));excel=[r for r in excel if r[0] is not None]
    check('s2-independent-openpyxl',len(excel)==len(rows) and all(str(a[0])==r['Entry'] and str(a[4])==r['deg_seq'] for a,r in zip(excel,rows)))
    check('footprint-old-vs-new-denominator',o['datasets']['footprint']['denominator']==2624)
    check('saturation-and-crispr-denominators',o['datasets']['saturation']['denominator']==249 and o['datasets']['crispr']['denominator']==31)
    # Current G2 scores independently recomputed from stored predictions, not copied JSON alone.
    n=np.load(TOPIC/'data/processed/g2-saturation-input.npz',allow_pickle=False)
    pred=np.load(TOPIC/'data/processed/g2-saturation-predictions.npz',allow_pickle=False)
    check('g2-shape-groups',len(n['peps'])==91 and len(set(n['groups']))==89 and len(n['y'])==47847)
    measured={}
    old=json.loads((TOPIC/'research/g2-saturation-2026-10-18/results.json').read_text())
    for name in ['DeltaPAP','ridge']:
        vals=[roc_auc_score(n['y'][a:z]>=1,pred[name][a:z]) for a,z in n['idx']]
        measured[name]=float(np.mean(vals));check('g2-recompute-'+name,abs(measured[name]-old['macro_auroc'][name])<1e-12,measured[name])
    dp=np.load(TOPIC/'data/processed/g2-ext-degformer_arch-predictions.npz',allow_pickle=False)
    measured['Degformer_retrained']=float(np.mean([roc_auc_score(n['y'][a:z]>=1,dp['predictions'][a:z]) for a,z in n['idx']]))
    ext=json.loads((TOPIC/'research/g2-extension-2026-10-18/e3-degformer-arch.json').read_text())
    check('degformer-retrain-independent-metric',abs(measured['Degformer_retrained']-ext['macro_auroc']['degformer_arch_cov80'])<1e-12,measured['Degformer_retrained'])
    # Independent HIF1A position readback from NPZ mutation sequences, not PSI parser.
    pair=o['datasets']['g2']['pairs'][0];j=list(n['peps']).index(pair['peptide']);start,end=map(int,n['idx'][j])
    records=json.loads((RAW/'derived/positive-records.json').read_text());r=records[pair['positive_row']]
    native=str(n['wt'][start]);source=rows[r['row']]['protein seq'];offset=source.index(native)
    rescued=set()
    for k in range(start,end):
        if n['y'][k]<1:continue
        diffs=[i for i,(a,z) in enumerate(zip(str(n['seqs'][k]),native)) if a!=z]
        if len(diffs)==1:rescued.add(offset+diffs[0]+1)
    regional={v for v in rescued if r['start']<=v<=r['end']}
    check('hif1a-13-rescue-positions-from-npz',len(regional)==pair['shared_important_positions']==13,{'positions':len(regional)})
    # Reconstruct seed29 context baseline from literal sequence records and saved cluster map.
    rr=json.loads((RAW/'derived/classification-records.json').read_text());gm={m:r for r,m in (l.split('\t')[:2] for l in (RAW/'derived/frozen-combined-cov80_cluster.tsv').read_text().splitlines())}
    X=np.array([[r['context'].count(a) for a in 'ACDEFGHIKLMNPQRSTVWY'] for r in rr],dtype=float);X/=X.sum(1,keepdims=True)
    y=np.array([r['label'] for r in rr]);g=np.array([gm[r['protein']] for r in rr]);p=np.zeros(len(rr));split_clean=True
    for tr,te in StratifiedGroupKFold(5,shuffle=True,random_state=29).split(X,y,g):
        split_clean &= not bool(set(g[tr])&set(g[te]))
        model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=2000,random_state=29)).fit(X[tr],y[tr]);p[te]=model.predict_proba(X[te])[:,1]
    target=next(r['group_oof']['auroc'] for r in b['results'] if r['cov']==80 and r['seed']==29 and r['features']=='context29-frequency')
    check('composition-independent-seed29-readback',split_clean and abs(roc_auc_score(y,p)-target)<1e-12,{'auroc':roc_auc_score(y,p),'groups_disjoint':split_clean})
    check('all-preregistered-seeds-coverages',len(b['results'])==24 and {r['seed'] for r in b['results']}=={17,29,43} and {r['cov'] for r in b['results']}=={50,80})
    frozen=load('frozen-group-reuse.json')
    check('existing-topic-cov50-cov80-groups-preserved',all(frozen[str(c)]['all_original_groups_preserved'] for c in [50,80]))
    # Direct comparison to each published supplementary metric, not only their mean.
    s5=pd.read_excel(RAW/'supplementary/supplementary_table_s5_bbae519.xlsx',sheet_name='All')
    s5=s5[(s5.Tools=='MetaDegron-X')&(s5.Metrics=='auc')]
    expected={int(str(r.Times).split('_')[-1]):float(r.Values) for _,r in s5.iterrows()}
    err=max(abs(r['auroc']-expected[r['seed']]) for r in x['results'][:10])
    check('safe-x-all-ten-repeats-vs-s5',err<1e-12,{'max_abs_error':err,'mean':x['recalculated_author_seed_mean']})
    check('safe-x-no-pickle-execution',x['executed_opcodes']==0 and x['model_param']['num_feature']=='10' and x['trees']==300)
    # Cross-check test overlap by a dataframe join, separate from the set-key counter.
    pp=pd.read_csv(RAW/'repo/data/test_properties.tsv',sep='\t').rename(columns={'Start':'START','End':'END'})
    props=pd.read_csv(RAW/'repo/data/annotated_degrons_properties.tsv',sep='\t')
    overlap=len(pp.merge(props[['Entry','START','END']],on=['Entry','START','END']))
    check('beta-trcp-overlap-two-methods',overlap==x['test_positive_coordinates_in_properties']==8)
    s=b['author_x_sampling'];check('author-x-sampling-population',s['positive']==212 and s['negative']==1060 and s['sampled_negative_unique_rows']==748)
    check('duplicate-leakage-present-all-folds',all(r['test_rows_with_identical_coordinate_in_train']>0 for r in s['fold_leakage']))
    # All README measured headlines have explicit JSON-backed values.
    ledger={
      '302':('dataset-audit.json','positive.rows',d['positive']['rows']),
      '240':('dataset-audit.json','positive.proteins_by_accession',d['positive']['proteins_by_accession']),
      '227':('dataset-audit.json','positive.species_suffix.HUMAN',d['positive']['species_suffix']['HUMAN']),
      '212':('dataset-audit.json','properties.positive_rows',d['properties']['positive_rows']),
      '0,8082':('validation.json','g2_recomputed.ridge',round(measured['ridge'],4)),
      '0,7693':('validation.json','g2_recomputed.DeltaPAP',round(measured['DeltaPAP'],4)),
      '0,7500':('validation.json','g2_recomputed.Degformer_retrained',round(measured['Degformer_retrained'],4)),
      '0,9670':('safe-x-reproduction.json','recalculated_author_seed_mean',round(x['recalculated_author_seed_mean'],4)),
      '8/20':('safe-x-reproduction.json','test_positive_coordinates_in_properties / positive_rows',f"{overlap}/{x['positive_rows']}"),
      '91–111':('composition-baseline.json','author_x_sampling.fold_leakage.test_rows_with_identical_coordinate_in_train',[min(r['test_rows_with_identical_coordinate_in_train'] for r in s['fold_leakage']),max(r['test_rows_with_identical_coordinate_in_train'] for r in s['fold_leakage'])]),
      '2 peptide':('overlap-audit.json','datasets.footprint.regional_peptides',o['datasets']['footprint']['regional_peptides'])}
    readme=(HERE/'README.md').read_text()
    check('readme-headline-ledger',all(token in readme for token in ledger))
    check('readme-measured-lines-link-json',all('.json' in line for line in readme.splitlines() if '[ĐO]' in line))
    check('readme-no-unqualified-priority-claims',not re.search(r'chưa ai làm|đầu tiên|vượt trội',readme,re.I))
    # Structural checking of source code does not execute it.
    for path in HERE.glob('*.py'):ast.parse(path.read_text())
    check('own-scripts-parse',True)
    base=load('baseline-worktree.json');untouched=[]
    for item in base['files']:
        pth=ROOT/item['path'];untouched.append(pth.is_file() and sha(pth)==item['sha256'])
    check('all-preexisting-dirty-files-preserved',all(untouched),{'files':len(untouched)})
    check('root-head-unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['head'])
    status=subprocess.check_output(['git','status','--porcelain','-z'],cwd=ROOT,text=True).split('\0')
    before={r['path'] for r in base['files']};new=[]
    for entry in status:
        if not entry:continue
        path=entry[3:]
        if path not in before:new.append(path)
    allowed=[str(HERE.relative_to(ROOT))+'/',str((TOPIC/'data/README.md').relative_to(ROOT))]
    check('new-status-paths-within-scope',all(any(p==a or p.startswith(a) for a in allowed) for p in new),new)
    raw_ignored=subprocess.run(['git','check-ignore',str((RAW/'repo/data/degron_data.txt').relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
    check('third-party-data-remains-ignored',raw_ignored.returncode==0)
    output={'generator':'validate.py','checks':checks,'g2_recomputed':measured,'readme_number_ledger':ledger,
        'limitations':['No MetaDegron-D GPS transfer or mutant-map score produced','No full primary-experiment biological error rate','No remote prediction submitted'],
        'scope':{'new_git_status_paths':new,'preexisting_untouched':all(untouched)}}
    (HERE/'validation.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    broken=[]
    for path in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('http:','https:','#','mailto:')):continue
            f=target.split('#',1)[0]
            if f and not (path.parent/f).exists():broken.append([path.name,target])
    check('local-report-links',not broken,broken)
    manifest=load('source-manifest.json');bad=[]
    for f in manifest['files']:
        if sha(ROOT/f['path'])!=f['sha256']:bad.append(f['path'])
    check('downloaded-and-derived-sha256',not bad,{'files_checked':len(manifest['files']),'mismatch':bad})
    output['checks']=checks;output['passed']=all(c['passed'] for c in checks)
    (HERE/'validation.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
    if not output['passed']:raise SystemExit('validation failed')

if __name__=='__main__':main()
