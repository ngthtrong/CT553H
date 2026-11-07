"""Inert-file audit. Run from repository root using .venv/bin/python -I.

No import, eval, model deserialization, notebook execution or pickle loading
from the downloaded project. Derived third-party records stay below raw/.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import ast
import csv
import hashlib
import gzip
import json
import re
import statistics
import subprocess
import time
import zipfile
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import StratifiedGroupKFold, train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
RAW = TOPIC / 'data/raw/metadegron'
REPO = RAW / 'repo'
DERIVED = RAW / 'derived'
AA = 'ACDEFGHIKLMNPQRSTVWY'
SEEDS = [17, 29, 43]

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False, default=lambda x: x.item() if isinstance(x, np.generic) else str(x)))

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def fasta(path):
    out, key = {}, None
    for line in path.read_text().splitlines():
        if line.startswith('>'):
            key = line[1:].split()[0]; out[key] = ''
        elif key:
            out[key] += line.strip()
    return out

def tables():
    pos = pd.read_csv(REPO / 'data/degron_data.txt', sep='\t')
    props = pd.read_csv(REPO / 'data/annotated_degrons_properties.tsv', sep='\t')
    neg = pd.read_csv(REPO / 'data/simulated_degrons.tsv.gz', sep='\t')
    up = pd.read_csv(REPO / 'supporting_file/uniprot_seq.tsv')
    return pos, props, neg, up

def e3_map():
    tree = ast.parse((REPO / 'Webserver/Degron_prediction.py').read_text())
    emap = next(ast.literal_eval(x.value) for x in tree.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'dict_E3_degrons' for t in x.targets))
    elm = pd.read_csv(REPO / 'supporting_file/elm_class_202309.txt', sep='\t')
    motif_to_class = dict(zip(elm.Motif, elm.ELMIdentifier))
    manual = {'CBL APS motif': 'CBL', 'CBL MET motif': 'CBL', 'CBL PTK motif': 'CBL',
              'ITCH motif': 'ITCH', 'FBX031 motif': 'SCF_FBXO31'}
    return emap, {e: sorted({manual.get(m, motif_to_class.get(m, 'UNMAPPED:' + m)) for m in motifs}) for e, motifs in emap.items()}

def profile():
    DERIVED.mkdir(exist_ok=True)
    with zipfile.ZipFile(RAW / 'supplementary-files.zip') as z:
        dest = RAW / 'supplementary'; dest.mkdir(exist_ok=True)
        for n in z.namelist():
            if n.endswith('.xlsx') and Path(n).name == n and not (dest / n).exists():
                (dest / n).write_bytes(z.read(n))
    pos, props, neg, up = tables()
    schemas = {}
    candidates = [x for x in REPO.rglob('*') if x.is_file() and '.git' not in x.parts and
                  (x.suffix in ['.csv', '.tsv', '.txt'] or x.name.endswith('.tsv.gz'))]
    for f in sorted(candidates):
        try:
            sep = ',' if f.suffix == '.csv' or f.name == 'uniprot_seq.tsv' else '\t'
            d = pd.read_csv(f, sep=sep)
            schemas[str(f.relative_to(RAW))] = {'rows': len(d), 'columns': list(d.columns),
                'dtypes': d.dtypes.astype(str).to_dict(), 'missing': d.isna().sum().to_dict(),
                'exact_duplicate_rows': int(d.duplicated().sum())}
        except Exception as e:
            schemas[str(f.relative_to(RAW))] = {'error': str(e)}
    for f in sorted((RAW / 'supplementary').glob('*.xlsx')):
        for sheet in pd.ExcelFile(f).sheet_names:
            d = pd.read_excel(f, sheet_name=sheet, header=0 if sheet == 'All' else 1)
            schemas[f'supplementary/{f.name}#{sheet}'] = {'rows': len(d), 'columns': list(d.columns),
                'dtypes': d.dtypes.astype(str).to_dict(), 'missing': d.isna().sum().to_dict(),
                'exact_duplicate_rows': int(d.duplicated().sum())}
    s2 = pd.read_excel(RAW / 'supplementary/supplementary_table_s2_bbae519.xlsx', header=1)
    # Source protein sequences, not short motifs, define homology groups.
    proteins = {}; records = []
    for i, r in pos.iterrows():
        seq = str(r['protein seq']); acc = str(r.Entry)
        token = 'md-' + acc + '-' + hashlib.sha256(seq.encode()).hexdigest()[:10]
        proteins[token] = seq
        start, end = int(r.START), int(r.END)
        core = seq[start-1:end]
        records.append({'row': i, 'protein': token, 'entry': acc, 'entry_name': r['Entry name'],
            'start': start, 'end': end, 'class': r['class'], 'source': r.source,
            'species_suffix': r['Entry name'].rsplit('_', 1)[-1], 'seq': str(r.deg_seq),
            'core': core, 'core_matches_reported': core == str(r.deg_seq),
            'reported_contains_core': core in str(r.deg_seq),
            'pmid': str(s2.iloc[i]['PudMed ID']), 'upstream_cluster': int(r.cluster)})
    dump(DERIVED / 'positive-records.json', records)
    upseq = dict(zip(up.Entry_Isoform, up.Sequence)); seq_lookup = dict(upseq)
    for _, r in pos.iterrows(): seq_lookup[str(r.Entry)] = str(r['protein seq'])
    samples = []
    for label, df in [(1, props), (0, neg[(neg.CONS_SCORE > 0)].dropna())]:
        for i, r in df.iterrows():
            acc = str(r.Entry_Isoform); seq = seq_lookup.get(acc)
            if not isinstance(seq, str): continue
            start, end = int(r.START), int(r.END)
            if not 1 <= start <= end <= len(seq): continue
            token = 'bg-' + acc + '-' + hashlib.sha256(seq.encode()).hexdigest()[:10]
            proteins[token] = seq
            # Translate both sources with exactly the same slicing convention.
            core = seq[start-1:end]; center = (start - 1 + end - 1) // 2
            context = ''.join(seq[j] if 0 <= j < len(seq) else '-' for j in range(center-14, center+15))
            samples.append({'label': label, 'table_row': int(i), 'entry': acc, 'protein': token,
                            'start': start, 'end': end, 'core': core, 'context': context})
    dump(DERIVED / 'classification-records.json', samples)
    topic_prot = fasta(TOPIC / 'data/processed/proteins-full.fasta')
    combined = {'tp-' + k: v for k, v in topic_prot.items()}; combined.update(proteins)
    (DERIVED / 'combined-proteins.fasta').write_text(''.join(f'>{k}\n{v}\n' for k, v in sorted(combined.items())))
    positive_proteins = {r['protein']: proteins[r['protein']] for r in records}
    (DERIVED / 'positive-proteins.fasta').write_text(''.join(f'>{k}\n{v}\n' for k, v in sorted(positive_proteins.items())))
    emap, eclasses = e3_map()
    counts = {e: {'motif_compatible_rows': sum(r['class'] in cs for r in records), 'mapped_classes': cs}
              for e, cs in eclasses.items()}
    join_keys = set(zip(pos.Entry, pos.START, pos.END))
    sample_idx = sorted(np.random.default_rng(17).choice(len(pos), 40, replace=False).tolist())
    manual_rows = [{k: v for k, v in records[i].items() if k not in ['seq', 'core']} for i in sample_idx]
    dump(DERIVED / 'label-sample-records.json', {'seed': 17, 'sampling': 'simple random 40/302', 'rows': manual_rows})
    dump(HERE / 'label-sample.json', {'generator':'audit_dataset.py --stage profile','seed':17,
         'sampling':'simple random 40/302','row_indices':sample_idx,
         'records_path':str((DERIVED/'label-sample-records.json').relative_to(ROOT)),
         'reason':'source records retained under ignored raw/; no raw data redistributed'})
    out = {'generator': 'audit_dataset.py --stage profile', 'script_sha256': sha(Path(__file__)),
           'positive': {'rows': len(pos), 'proteins_by_accession': pos.Entry.nunique(),
            'protein_sequences': pos['protein seq'].nunique(), 'unique_motif_sequences': pos.deg_seq.nunique(),
            'unique_entry_coordinates': len(join_keys), 'classes': pos['class'].value_counts().to_dict(),
            'sources': pos.source.value_counts().to_dict(), 'species_suffix': Counter(r['species_suffix'] for r in records),
            'pmids': s2['PudMed ID'].astype(str).value_counts().to_dict(),
            'reported_length_counts': pos.deg_seq.str.len().value_counts().sort_index().to_dict(),
            'coordinate_length_counts': (pos.END-pos.START+1).value_counts().sort_index().to_dict(),
            'core_matches_reported': sum(r['core_matches_reported'] for r in records),
            'reported_contains_core': sum(r['reported_contains_core'] for r in records),
            's2_matches_repository_identifiers': bool((s2['UniProt ID'].astype(str).values == pos.Entry.values).all()),
            's2_matches_repository_sequences': bool((s2['Degron instance'].astype(str).values == pos.deg_seq.values).all()),
            'topic_accession_overlap': len(set(pos.Entry) & set(topic_prot)),
            'topic_exact_protein_sequence_overlap': len(set(pos['protein seq']) & set(topic_prot.values())),
            'upstream_cluster_values': pos.cluster.value_counts().to_dict()},
           'properties': {'positive_rows': len(props), 'proteins': props.Entry.nunique(),
              'coordinate_join_to_302': sum((r.Entry,r.START,r.END) in join_keys for _, r in props.iterrows())},
           'negative': {'rows': len(neg), 'proteins': neg.Entry.nunique(),
              'coordinate_length_counts': (neg.END-neg.START+1).value_counts().sort_index().to_dict(),
              'filtered_rows': len(neg[neg.CONS_SCORE > 0].dropna()),
              'positive_protein_overlap': len(set(pos.Entry) & set(neg.Entry)),
              'exact_positive_coordinate_overlap': sum((r.Entry,r.START,r.END) in join_keys for _, r in neg.iterrows())},
           'web_e3_count': len(emap), 'e3_motif_mapping': counts,
           'classification': {'rows': len(samples), 'positive': sum(r['label'] for r in samples),
                              'negative': sum(not r['label'] for r in samples)}, 'schemas': schemas}
    out['negative']['length_histogram_equals_5x_positive_coordinate_length_plus_one'] = Counter((neg.END-neg.START+1).astype(int)) == Counter({int(k)+1:int(v)*5 for k,v in Counter((pos.END-pos.START+1).astype(int)).items()})
    out['classification']['excluded_negative_rows_for_missing_or_invalid_sequence'] = len(neg[neg.CONS_SCORE > 0].dropna()) - sum(not r['label'] for r in samples)
    dump(HERE / 'dataset-audit.json', out)
    print(json.dumps({k:v for k,v in out.items() if k not in ['schemas', 'positive', 'e3_motif_mapping']}, ensure_ascii=False))

def cluster():
    results = {'generator': 'audit_dataset.py --stage cluster', 'version': subprocess.check_output(['mmseqs', 'version'], text=True).strip()}
    for pop in ['positive', 'combined']:
        results[pop] = {}
        for cov in [50, 80]:
            prefix = DERIVED / f'{pop}-cov{cov}'
            cmd = ['mmseqs', 'easy-cluster', str(DERIVED / f'{pop}-proteins.fasta'), str(prefix), str(prefix)+'-tmp',
                   '--min-seq-id', '0.3', '-c', str(cov/100), '--cov-mode', '0', '--seq-id-mode', '0',
                   '--alignment-mode', '3', '--cluster-mode', '1', '--single-step-clustering', '1',
                   '-s', '7.5', '--max-seqs', '10000', '--split-memory-limit', '2G', '--threads', '4']
            started = time.time(); cached = Path(str(prefix)+'_cluster.tsv').exists()
            if not cached:
                with (DERIVED / f'{pop}-cov{cov}.log').open('w') as log:
                    subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True, cwd=ROOT)
            pairs = [line.split('\t')[:2] for line in Path(str(prefix)+'_cluster.tsv').read_text().splitlines()]
            results[pop][str(cov)] = {'proteins':len(pairs), 'clusters':len({p[0] for p in pairs}),
                'command':cmd, 'cached':cached, 'seconds':round(time.time()-started,2),
                'tsv_sha256':sha(Path(str(prefix)+'_cluster.tsv'))}
            dump(HERE / 'clusters.json', results)
            print(pop, cov, results[pop][str(cov)]['clusters'], flush=True)

def groups(cov, pop='combined'):
    gm={m:r for r,m in (line.split('\t')[:2] for line in (DERIVED / f'{pop}-cov{cov}_cluster.tsv').read_text().splitlines())}
    if pop!='combined':return gm
    # Preserve ALL original protein groups when extending the population. A greedy
    # rerun with added sequences may otherwise fragment an old group.
    parent={v:v for v in gm.values()}
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    original=TOPIC/f'data/interim/protein-id30-cov{cov}_cluster.tsv'
    old=defaultdict(set)
    for line in original.read_text().splitlines():
        rep,member=line.split('\t')[:2]
        if 'tp-'+member in gm:old[rep].add(gm['tp-'+member])
    for values in old.values():
        values=sorted(values)
        for v in values[1:]:union(values[0],v)
    frozen={m:find(r) for m,r in gm.items()}
    (DERIVED/f'frozen-combined-cov{cov}_cluster.tsv').write_text(''.join(f'{r}\t{m}\n' for m,r in sorted(frozen.items())))
    output=HERE/'frozen-group-reuse.json'
    info=json.loads(output.read_text()) if output.exists() else {'generator':'audit_dataset.py groups()','meaning':'new union clusters additionally constrained to preserve every original topic cluster'}
    info[str(cov)]={'original_tsv':str(original.relative_to(ROOT)),'original_sha256':sha(original),
        'original_groups_represented':len(old),'old_groups_fragmented_before_constraint':sum(len(v)>1 for v in old.values()),
        'union_cluster_count':len(set(gm.values())),'effective_frozen_extended_cluster_count':len(set(frozen.values())),
        'all_original_groups_preserved':all(len({find(v) for v in values})==1 for values in old.values())}
    dump(output,info)
    return frozen

def boot_auc(y, pred, g, seed, n=5000):
    # Cluster multiplicities are weights; no resampling of individual cells.
    unique = np.unique(g); lookup = {v:i for i,v in enumerate(unique)}; gi = np.array([lookup[v] for v in g])
    rng = np.random.default_rng(seed); values = []
    for _ in range(n):
        w = np.bincount(rng.integers(0,len(unique),len(unique)), minlength=len(unique))[gi]
        if np.any(w[y==0]) and np.any(w[y==1]): values.append(roc_auc_score(y,pred,sample_weight=w))
    return {'ci95':np.quantile(values,[.025,.975]).tolist(), 'replicates':len(values), 'clusters':len(unique)}

def models():
    records = json.loads((DERIVED / 'classification-records.json').read_text())
    y = np.array([r['label'] for r in records]); entries = np.array([r['entry'] for r in records])
    out = {'generator':'audit_dataset.py --stage models', 'seeds':SEEDS, 'definition':'reconstructed properties population; not published D training population', 'results':[]}
    for cov in [80,50]:
        gm = groups(cov); g = np.array([gm[r['protein']] for r in records])
        for view in ['length','core-frequency','core-count-length','context29-frequency']:
            seqs = [r['context' if view.startswith('context') else 'core'] for r in records]
            if view == 'length': X = np.array([[len(s)] for s in seqs],dtype=float)
            else:
                X = np.array([[s.count(a) for a in AA] for s in seqs], dtype=float)
                if 'frequency' in view: X /= np.maximum(X.sum(axis=1,keepdims=True),1)
                if 'count-length' in view: X = np.column_stack([X,[len(s) for s in seqs]])
            for seed in SEEDS:
                model = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0,max_iter=2000,random_state=seed))
                tr, te = train_test_split(np.arange(len(y)),test_size=.1,stratify=y,random_state=seed)
                clf = model().fit(X[tr],y[tr]); pred = clf.predict_proba(X[te])[:,1]
                random_result = {'auroc':roc_auc_score(y[te],pred), 'auprc':average_precision_score(y[te],pred),
                    'n_test':len(te), 'test_rows_shared_cluster':int(np.isin(g[te],g[tr]).sum())}
                oof = np.zeros(len(y)); folds=[]
                for tr,te in StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=seed).split(X,y,g):
                    assert not set(g[tr]) & set(g[te])
                    clf = model().fit(X[tr],y[tr]); oof[te] = clf.predict_proba(X[te])[:,1]
                    folds.append({'n_test':len(te),'n_positive':int(y[te].sum()),'auroc':roc_auc_score(y[te],oof[te])})
                row = {'cov':cov,'features':view,'seed':seed,'random_holdout':random_result,
                    'group_oof':{'auroc':roc_auc_score(y,oof),'auprc':average_precision_score(y,oof),'folds':folds}}
                # One primary CI per representation and coverage; all seeds still measured.
                if seed == 17: row['group_oof']['bootstrap'] = boot_auc(y,oof,g,seed)
                out['results'].append(row); dump(HERE / 'composition-baseline.json',out)
                print(cov,view,seed,round(row['group_oof']['auroc'],4),flush=True)
    sampling(out)

def sampling(out=None):
    if out is None: out=json.loads((HERE/'composition-baseline.json').read_text())
    pos,props,neg,up=tables(); nf=neg[neg.CONS_SCORE>0].dropna()
    sampled=nf.sample(n=5*len(props),replace=True,random_state=2024509)
    features=['ASA_SCORE','DSS_SCORE','FCONS_SCORE','COIL','ANCHOR_SCORE','nflanking_ptms','nflanking_ub_lysines','HELIX','RIG_SCORE','Domain_pfam']
    keep=['Entry','START','END']+features
    data=pd.concat([props[keep].assign(label=1),sampled[keep].assign(label=0)])
    data=data.dropna(); data=data.sample(frac=1,random_state=42).reset_index(drop=True)
    cv=StratifiedKFold(5,shuffle=True,random_state=np.random.RandomState(527)); leak=[]
    for tr,te in cv.split(data,data.label):
        keys=lambda ix:set(zip(data.iloc[ix].label,data.iloc[ix].Entry,data.iloc[ix].START,data.iloc[ix].END))
        shared=keys(tr)&keys(te)
        leak.append({'test_rows':len(te),'shared_coordinate_keys':len(shared),
          'test_rows_with_identical_coordinate_in_train':sum((r.label,r.Entry,r.START,r.END) in shared for _,r in data.iloc[te].iterrows())})
    out['author_x_sampling']={'positive':int(data.label.sum()),'negative':int((data.label==0).sum()),
        'sampled_negative_unique_rows':int(sampled.index.nunique()),'fold_leakage':leak,
        'definition':'matches Training_MetaDegron-X.py row sampling/splitting; does not execute their code'}
    cr=json.loads((DERIVED/'classification-records.json').read_text())
    key_to_protein={(r['label'],r['entry'],r['start'],r['end']):r['protein'] for r in cr}
    out['author_x_sampling']['homology_by_cov']={}
    for cov in [80,50]:
        gm=groups(cov)
        group=[gm.get(key_to_protein.get((r.label,r.Entry,r.START,r.END),'UNMAPPED')) for _,r in data.iterrows()]
        fold_rows=[]
        for tr,te in StratifiedKFold(5,shuffle=True,random_state=np.random.RandomState(527)).split(data,data.label):
            tg=[group[i] for i in tr if group[i] is not None];vg=[group[i] for i in te if group[i] is not None]
            tc=Counter(tg);vc=Counter(vg);cross=sum(tc[k]*vc[k] for k in tc.keys()&vc.keys())
            fold_rows.append({'train_mapped':len(tg),'test_mapped':len(vg),'test_mapped_shared_cluster':sum(v in tc for v in vg),
                 'cross_split_same_cluster_pairs':cross,'cross_split_mapped_pairs':len(tg)*len(vg),
                 'pair_fraction_mapped':cross/(len(tg)*len(vg))})
        out['author_x_sampling']['homology_by_cov'][str(cov)]={'mapped_rows':sum(v is not None for v in group),'total_rows':len(group),'folds':fold_rows}
    d=pd.read_csv(REPO/'supporting_file/Degpred_result.csv');aucs={k:roc_auc_score(t.true_labels,t.predicted_probs) for k,t in d.groupby('symbol')}
    out['published_baseline_recalculation']={'Degpred_per_repeat':aucs,'mean':statistics.mean(aucs.values()),'published':.9540,
        'difference':statistics.mean(aucs.values())-.9540,'not_model_reexecution':True}
    dump(HERE/'composition-baseline.json',out)

def overlaps():
    records=json.loads((DERIVED/'positive-records.json').read_text());pos,props,neg,up=tables()
    proteins={r['protein']:str(pos.iloc[r['row']]['protein seq']) for r in records}
    csv.field_size_limit(10**7)
    path=TOPIC/'data/interim/zhang-scanning-unzip/I28 Scanning (Completed)/Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv'
    wt,mut,seqs={},{},{}
    for r in csv.DictReader(path.open()):
        m=re.match(r'(.+)_mut(\d+)$',r['Gene'])
        if not m:continue
        pep,p=m[1],int(m[2])
        if p==0:seqs[pep]=r['AA.Seq'].rstrip('*').upper()
        try:reads=float(r['Sum']);psi=float(r['PSI'])
        except (ValueError,TypeError):continue
        if reads<10 or not np.isfinite(psi):continue
        if p==0:wt[pep]=psi
        else:mut.setdefault(pep,{})[p]=psi
    fp={p for p,w in wt.items() if w<=3 and len(mut.get(p,{}))>=21 and any(v-w>=1 for v in mut.get(p,{}).values())}
    sat=set()
    for line in (TOPIC/'data/processed/psi-sat_a.tsv').read_text().splitlines()[1:]:
        m=re.match(r'(.+)_mut\d+[a-zA-Z]$',line.split('\t')[0])
        if m:sat.add(m[1])
    assignments=json.loads((TOPIC/'research/e3-labels-audit/e3-assignment.json').read_text())['assignment']
    # The historical clustering reference covers scanning proteins, not every saturation-only protein.
    # Read the already pinned full human snapshot; no download or reference-cluster rewrite.
    full_seq={};gene_to_acc=defaultdict(set);acc=None
    with gzip.open(TOPIC/'data/raw/human-reviewed-2026-10-12.fasta.gz','rt') as fh:
        for line in fh:
            if line.startswith('>'):
                acc=line.split('|')[1];full_seq[acc]=''
                gene=re.search(r'\bGN=(\S+)',line)
                if gene:gene_to_acc[gene[1]].add(acc)
            elif acc:full_seq[acc]+=line.strip()
    for f in (TOPIC/'data/raw/uniprot-additional').glob('*.fasta'):
        for key,value in fasta(f).items():full_seq[key.split('|')[1] if '|' in key else key]=value
    topic_prot=fasta(TOPIC/'data/processed/proteins-full.fasta');full_seq.update(topic_prot)
    crispr=set()
    for p in assignments:
        candidates=[q for q in seqs if q==p or q.endswith('_'+p)]
        if len(candidates)==1:crispr.add(candidates[0])
        else:
            gene=p.rsplit('_',1)[0];accs=gene_to_acc.get(gene,set())
            crispr.add(next(iter(accs))+'_'+p if len(accs)==1 else p)
    n=np.load(TOPIC/'data/processed/g2-saturation-input.npz',allow_pickle=False)
    g2=set(n['peps'].tolist()); g2_seq={p:str(n['wt'][int(ab[0])]) for p,ab in zip(n['peps'],n['idx'])}
    def pep_seq(p):
        if p in seqs:return seqs[p]
        if p in g2_seq:return g2_seq[p]
        a=p.split('_')[0]
        try:start=(int(p.rsplit('_',1)[1])-1)*23
        except ValueError:return ''
        return full_seq.get(a,'')[start:start+28]
    sat_halves=[]
    for tag in ['sat_a','sat_b']:
        half=defaultdict(dict)
        for line in (TOPIC/f'data/processed/psi-{tag}.tsv').read_text().splitlines()[1:]:
            columns=line.split('\t');m=re.match(r'(.+)_mut(\d+)([a-z])$',columns[0])
            if not m:continue
            value,reads=float(columns[1]),float(columns[2])
            if np.isfinite(value) and reads>=10:half[m[1]][(int(m[2]),m[3].upper())]=value
        sat_halves.append(half)
    sat_wt={};sat_important={}
    for p in sat|g2:
        seq=pep_seq(p);refs=[]
        for half in sat_halves:
            vals=[half[p][(i,a)] for i,a in enumerate(seq,1) if (i,a) in half[p]]
            refs.append(statistics.median(vals) if len(vals)>=10 else None)
        if all(r is not None for r in refs):
            sat_wt[p]=statistics.mean(refs)
            keys=set(sat_halves[0][p])&set(sat_halves[1][p])
            sat_important[p]={i for i,a in keys if 1<=i<=len(seq) and a!=seq[i-1] and
                statistics.mean([sat_halves[j][p][(i,a)]-refs[j] for j in [0,1]])>=1}
    datasets={name:{p:{'seq':pep_seq(p),'psi':(sat_wt if name in ['saturation','g2'] else wt).get(p)} for p in ps} for name,ps in [('footprint',fp),('saturation',sat),('crispr',crispr),('g2',g2)]}
    out={'generator':'audit_dataset.py --stage overlap','definitions':{'footprint':'same CSV/thresholds as count_footprints.py; verified exact denominator',
          'regional_overlap':'exact tile sequence located in source protein, annotated coordinate interval intersects tile; no free short-motif search across unrelated proteins',
          'label_agreement':'PSI <=3; scanning CSV WT for footprint/CRISPR, native-AA median refs each half (>=10) for saturation/G2; not E3 agreement',
          'tile_agreement':'degron_score >=0.5 operational cutoff, exploratory; not PSI conversion'}, 'datasets':{}}
    regional_positive=set()
    for name,ds in datasets.items():
        matches=[];shared=set();peptides=set()
        for r in records:
            source=proteins[r['protein']]
            for p,d in ds.items():
                if p.split('_')[0]==r['entry']:shared.add(r['row'])
                tile=d['seq']
                if len(tile)<20:continue
                starts=[m.start() for m in re.finditer('(?='+re.escape(tile)+')',source)]
                for a in starts:
                    overlap=set(range(max(a+1,r['start']),min(a+len(tile),r['end'])+1))
                    if not overlap:continue
                    important=({a+j for j in sat_important.get(p,set())} if name in ['saturation','g2'] else
                               {a+j for j,v in mut.get(p,{}).items() if p in wt and v-wt[p]>=1})
                    hits=len(overlap&important)
                    matches.append({'positive_row':r['row'],'peptide':p,'entry':r['entry'],'psi':d['psi'],
                        'shared_important_positions':hits,'n_overlap_residues':len(overlap),
                        'footprint_available':p in sat_important if name in ['saturation','g2'] else p in wt and p in mut})
                    regional_positive.add(r['row']);peptides.add(p)
        out['datasets'][name]={'denominator':len(ds),'peptides_with_mapped_sequence':sum(len(r['seq'])>=20 for r in ds.values()),
           'same_accession_positive_rows':len(shared),
           'regional_positive_rows':len({r['positive_row'] for r in matches}),'regional_peptides':len(peptides),
           'available_psi_pairs':sum(r['psi'] is not None for r in matches),
           'psi_low_pairs':sum(r['psi'] is not None and r['psi']<=3 for r in matches),
           'psi_high_pairs':sum(r['psi'] is not None and r['psi']>3 for r in matches),
           'pairs_with_measured_important_position':sum(r['shared_important_positions']>0 for r in matches),'pairs':matches}
    for name,path in [('voutsinos',TOPIC/'data/raw/voutsinos-2026/repo/score/degrons.csv.gz'),
                      ('larsen',TOPIC/'data/raw/larsen-2025/transfac_tiles.csv.gz')]:
        d=pd.read_csv(path); tile_map=defaultdict(list)
        for _,r in d.iterrows():
            score=float(r.degron_score)
            tile_map[str(r.aa)].append((str(r['name']),score if np.isfinite(score) else None))
        matches=[]; represented=set()
        for r in records:
            seq=proteins[r['protein']]
            for a in range(max(0,r['start']-30), min(len(seq)-29,r['end'])):
                for tile,score in tile_map.get(seq[a:a+30],[]):
                    matches.append({'positive_row':r['row'],'tile':tile,'degron_score':score,'source_start':a+1})
                    regional_positive.add(r['row'])
            if any(seq[a:a+30] in tile_map for a in range(len(seq)-29)):represented.add(r['protein'])
        out['datasets'][name]={'denominator':len(d),'regional_positive_rows':len({r['positive_row'] for r in matches}),
            'regional_tiles':len({r['tile'] for r in matches}),'source_proteins_represented_by_exact_tile':len(represented),
            'pairs_score_missing':sum(r['degron_score'] is None for r in matches),
            'pairs_score_ge_point5':sum(r['degron_score'] is not None and r['degron_score']>=.5 for r in matches),
            'pairs_score_lt_point5':sum(r['degron_score'] is not None and r['degron_score']<.5 for r in matches),'pairs':matches}
    out['e3_after_filter']={}
    emap,eclasses=e3_map()
    for cov in [80,50]:
        gm=groups(cov);topic_group={gm['tp-'+a] for a in topic_prot}
        g2_clusters={gm['tp-'+p.split('_')[0]] for p in g2 if 'tp-'+p.split('_')[0] in gm}
        counts={};human_counts={};regional_counts={};g2_counts={};strict_counts={};row_remaining=[]
        for e,cs in eclasses.items():
            matched=[r for r in records if r['class'] in cs]
            unique={(r['entry'],r['start'],r['end']) for r in matched}
            human={ (r['entry'],r['start'],r['end']) for r in matched if r['species_suffix']=='HUMAN' }
            filtered=[r for r in matched if r['species_suffix']=='HUMAN' and gm[r['protein']] not in topic_group and r['row'] not in regional_positive]
            regional_counts[e]=len({(r['entry'],r['start'],r['end']) for r in matched if r['species_suffix']=='HUMAN' and r['row'] not in regional_positive})
            g2_counts[e]=len({(r['entry'],r['start'],r['end']) for r in matched if r['species_suffix']=='HUMAN' and r['row'] not in regional_positive and gm[r['protein']] not in g2_clusters})
            counts[e]=len(unique);human_counts[e]=len(human);strict_counts[e]=len({(r['entry'],r['start'],r['end']) for r in filtered})
            row_remaining+=filtered
        out['e3_after_filter'][str(cov)]={'motif_mapped_unique':counts,'human_unique':human_counts,
              'human_no_regional_overlap':regional_counts,'human_no_g2_clusters_no_regional_overlap':g2_counts,
              'human_no_topic_cluster_no_regional_overlap':strict_counts,
              'e3_ge5_before':sum(v>=5 for v in counts.values()),'e3_ge5_human':sum(v>=5 for v in human_counts.values()),
              'e3_ge5_no_region':sum(v>=5 for v in regional_counts.values()),'e3_ge5_no_g2_cluster_no_region':sum(v>=5 for v in g2_counts.values()),
              'e3_ge5_strict':sum(v>=5 for v in strict_counts.values()),
              'strict_rows_union':len({r['row'] for r in row_remaining}),
              'warning':'motif-compatible assignment, NOT 21 independently experimentally verified E3 classes'}
        pg=groups(cov,'positive');labels=np.array([r['class'] for r in records]);g=np.array([pg[r['protein']] for r in records])
        fractions=[]
        for seed in SEEDS:
            tr,te=train_test_split(np.arange(len(records)),test_size=.1,random_state=seed)
            cross=sum(g[a]==g[b] for a in tr for b in te)
            fractions.append({'seed':seed,'train':len(tr),'test':len(te),'test_rows_with_train_homolog':int(np.isin(g[te],g[tr]).sum()),
                 'cross_split_positive_row_pairs_same_cluster':cross,'all_cross_split_pairs':len(tr)*len(te),'pair_fraction':cross/(len(tr)*len(te))})
        out.setdefault('internal_positive_homology',{})[str(cov)]={'clusters':len(set(g)),'random90_10_sensitivity':fractions,
                 'author_actual_dl_partition':'not identifiable without object-NPY row order and labels; this simulation is NOT the published split'}
    dump(HERE/'overlap-audit.json',out)
    print(json.dumps({k:{x:y for x,y in v.items() if x!='pairs'} for k,v in out['datasets'].items()},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['profile','cluster','models','sampling','overlap','all'],default='all');args=parser.parse_args()
    for stage,fn in [('profile',profile),('cluster',cluster),('models',models),('sampling',sampling),('overlap',overlaps)]:
        if args.stage in [stage,'all']:fn()
