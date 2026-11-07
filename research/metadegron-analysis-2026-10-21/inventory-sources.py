"""Produce source hashes, dependency/architecture inventory and access receipts."""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
import ast
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import zipfile
import h5py

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
RAW=TOPIC/'data/raw/metadegron'; REPO=RAW/'repo'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def save(name,d):
    (HERE/name).write_text(json.dumps(d,indent=2,ensure_ascii=False,default=str))

def main():
    commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    commit_date=subprocess.check_output(['git','-C',str(REPO),'show','-s','--format=%cI',commit],text=True).strip()
    tracked=subprocess.check_output(['git','-C',str(REPO),'ls-files','-z'],text=True).split('\0');tracked=[p for p in tracked if p]
    licenses=[p for p in tracked if re.search(r'license|copying|copyright',Path(p).name,re.I)]
    accesses=[]
    for p in sorted(HERE.glob('*access.json')):
        for r in json.loads(p.read_text()):
            f=ROOT/r['path'];r['accessible']=r['downloaded'];r['receipt_file']=p.name
            if f.exists() and f.suffix=='.xlsx' and not zipfile.is_zipfile(f):
                r['accessible']=False;r['content_validation']='HTML challenge, not XLSX; HTTP 200 is not data access'
            if f.exists() and f.name=='review-2017-table.html' and 'restricted to ELTEnet' in f.read_text():
                r['accessible']=False;r['content_validation']='HTTP 200 access-denial page: restricted to ELTEnet'
            if 'elm-' in f.name:r['license']='ELM academic license; noncommercial/internal academic scope; no redistribution assumed'
            if f.name.startswith('paper.') or f.name.startswith('supplementary-files'):
                r['license']='article CC BY 4.0; underlying imported dataset permissions separately unresolved'
            accesses.append(r)
    access_by_path={r['path']:r for r in accesses}
    files=[]
    for p in sorted(RAW.rglob('*')):
        if not p.is_file() or '.git' in p.relative_to(RAW).parts or '-tmp' in str(p.relative_to(RAW)):continue
        rel=str(p.relative_to(ROOT));r={'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'download_date':'2026-10-21'}
        if REPO in p.parents:
            tail=p.relative_to(REPO).as_posix();r.update(url=f'https://github.com/BioDataStudy/MetaDegron/blob/{commit}/{tail}',license='chưa xác nhận: no LICENSE in pinned repository')
        elif rel in access_by_path:
            r.update(url=access_by_path[rel]['url'],license=access_by_path[rel]['license'],accessible=access_by_path[rel]['accessible'])
        elif (RAW/'supplementary') in p.parents:
            r.update(url='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11491831/supplementaryFiles',license='article CC BY 4.0; upstream data rights checked separately',container_sha256=sha(RAW/'supplementary-files.zip'))
        else:r.update(url=None,license='derived audit; source rights retained',generator='audit_dataset.py')
        files.append(r)
    root=ET.parse(RAW/'paper.xml').getroot();lic=root.find('.//license')
    env={m:bool(importlib.util.find_spec(m)) for m in ['numpy','pandas','scipy','sklearn','h5py','torch','tensorflow','keras','allennlp','xgboost']}
    env.update(python=platform.python_version(),platform=platform.platform())
    existing_inputs=[]
    for rel in ['data/processed/proteins-full.fasta','data/raw/human-reviewed-2026-10-12.fasta.gz',
                'data/interim/protein-id30-cov50_cluster.tsv','data/interim/protein-id30-cov80_cluster.tsv',
                'data/processed/g2-saturation-input.npz','data/processed/psi-sat_a.tsv','data/processed/psi-sat_b.tsv',
                'data/raw/larsen-2025/transfac_tiles.csv.gz','data/raw/voutsinos-2026/repo/score/degrons.csv.gz',
                'data/interim/zhang-scanning-unzip/I28 Scanning (Completed)/Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv']:
        p=TOPIC/rel;existing_inputs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'read_only_existing_source':True})
    save('source-manifest.json',{'generator':'inventory-sources.py','client_date':'2026-10-21','existing_topic_inputs':existing_inputs,
        'repository':{'url':'https://github.com/BioDataStudy/MetaDegron','commit':commit,'commit_date':commit_date,'license_files':licenses,
          'license':'chưa xác nhận; absent LICENSE is not permission','tracked_files':len(tracked)},
        'article':{'doi':'10.1093/bib/bbae519','pmcid':'PMC11491831','license_verbatim':''.join(lic.itertext()),'license':'CC BY 4.0'},
        'network_attempts':accesses,'files':files,'environment':env,
        'safety':{'third_party_code_executed':False,'pickle_loaded':False,'torch_checkpoint_loaded':False,
          'object_npy_loaded':False,'hdf5_numeric_metadata_only':True,'remote_prediction_submissions':0,
          'web_terms':'Terms.php 404; linked UTHealth policies 403; no prediction submitted',
          'large_remote_files':'reachable HTTP 200; audit fetch capped at 20 MB, payload not retained; not missing weights claim'}})
    notebooks={};imports=set();code_refs={}
    for p in REPO.rglob('*'):
        if not p.is_file() or '.git' in p.parts:continue
        if p.suffix=='.py':sources=[(None,p.read_text())]
        elif p.suffix=='.ipynb':
            cells=json.loads(p.read_text()).get('cells',[])
            sources=[(i,''.join(c['source'])) for i,c in enumerate(cells) if c['cell_type']=='code']
            notebooks[p.name]={'code_cells':len(sources),'all_cells':len(cells),'executed_by_audit':False}
        else:continue
        for cell,s in sources:
            try:
                tree=ast.parse(s)
                for node in ast.walk(tree):
                    if isinstance(node,ast.Import):imports.update(a.name.split('.')[0] for a in node.names)
                    elif isinstance(node,ast.ImportFrom) and node.module:imports.add(node.module.split('.')[0])
            except SyntaxError:pass
            hits=[]
            for i,line in enumerate(s.splitlines(),1):
                if any(k in line for k in ['pickle.load','allow_pickle','train_test_split','StratifiedKFold','feature_name','covariates','validation_data','EarlyStopping','shift, slicesize','dict_E3_degrons']):
                    hits.append({'line':i,'kind':next(k for k in ['pickle.load','allow_pickle','train_test_split','StratifiedKFold','feature_name','covariates','validation_data','EarlyStopping','shift, slicesize','dict_E3_degrons'] if k in line)})
            if hits:code_refs[str(p.relative_to(REPO))+(f'#cell-{cell}' if cell is not None else '')]=hits
    arch=json.loads((REPO/'models/degron_DL.json').read_text());layers=[]
    for layer in arch['config']['layers']:
        c=layer['config'];r={'class':layer['class_name'],'name':c['name']}
        for k in ['batch_input_shape','units','activation','filters','kernel_size','pool_size','input_dim','output_dim','alpha','padding','strides','axis']:
            if k in c:r[k]=c[k]
        if 'layer' in c:r['wrapped_layer']={k:v for k,v in c['layer']['config'].items() if k in ['units','activation','recurrent_activation','return_sequences','dropout','recurrent_dropout']}
        layers.append(r)
    arrays=[]
    with h5py.File(REPO/'models/degron_DL.h5','r') as f:
        h5meta={k:(v.tolist() if hasattr(v,'tolist') else str(v)) for k,v in f.attrs.items() if k!='layer_names'}
        f.visititems(lambda n,x:arrays.append({'name':n,'shape':list(x.shape),'dtype':str(x.dtype)}) if isinstance(x,h5py.Dataset) else None)
    save('code-audit.json',{'generator':'inventory-sources.py','imports':sorted(imports),'notebooks':notebooks,
        'code_reference_locations':code_refs,'serialized_architecture_layers':layers,'hdf5':{'attributes':h5meta,'arrays':arrays},
        'framework_reproduction_blockers':['TensorFlow 1.15 / Keras 2.3.1 / allennlp 0.9.0 unavailable in current Python environment',
            'Object-NPY and XGBoost pickle are not safely loaded by original scripts; no unrestricted deserialization performed',
            'Webserver source constructs 49-residue windows; bundled architecture has 29 residues; notebook uses 29',
            'Webserver X uses 11 columns including STRAND, training X uses 10, plus missing precomputed per-protein feature files'],
        'external_evaluation':{'x_precomputed_properties':'completed by safe-predict-x.py without unpickling; see safe-x-reproduction.json',
          'zero_shot':'blocked: D runtime not reconstructed; X protein-feature assets missing; no GPS scores generated',
          'mutation_map':'blocked: same plus fixed-motif-window implementation required','remote_submissions':0}})
    tree='\n'.join(f'{p} ({(REPO/p).stat().st_size:,} bytes)' for p in tracked)
    languages=Counter(Path(p).suffix or '(no suffix)' for p in tracked)
    total=sum((REPO/p).stat().st_size for p in tracked)
    save('repository-inventory.json',{'generator':'inventory-sources.py','commit':commit,'commit_date':commit_date,'file_count':len(tracked),'bytes':total,
        'extension_file_counts':dict(languages),'license_files':licenses,'notebook_count':len(notebooks),
        'weights':[r for r in files if r['path'].endswith(('.h5','.pickle','.npy'))],
        'readme':'repo/README.md','dependency_manifest_files':[p for p in tracked if Path(p).name in ['requirements.txt','environment.yml','pyproject.toml','setup.py','Pipfile']],
        'imports':sorted(imports)})
    (HERE/'repository-tree.md').write_text('# Cây repo ghim\n\n[ĐO] Sinh bởi `inventory-sources.py`; số byte và kiểm kê trong [repository-inventory.json](repository-inventory.json). Cây giữ nguyên tên file upstream.\n\n```text\n'+tree+'\n```\n')
    # Snapshot relevant current-topic numbers with exact source hashes; no rerunning old experiments.
    inputs={}
    for rel in ['g2-saturation-2026-10-18/results.json','g2-saturation-2026-10-18/audit.json','g2-extension-2026-10-18/e3-degformer-arch.json',
                'g2-extension-2026-10-18/e2-candidates.json','e3-labels-audit/e3-assignment.json','e3-labels-audit/footprint-audit.json','e3-labels-audit/satmut-audit.json']:
        p=TOPIC/'research'/rel
        inputs[rel]={'path':str(p.relative_to(ROOT)),'sha256':sha(p),'data':json.loads(p.read_text())}
    save('current-topic-evidence.json',{'generator':'inventory-sources.py','meaning':'readback of existing measured JSON, not new model runs','inputs':inputs})
    print(json.dumps({'commit':commit,'file_count':len(tracked),'bytes':total,'license_files':licenses,'environment':env},ensure_ascii=False))

if __name__=='__main__':main()
