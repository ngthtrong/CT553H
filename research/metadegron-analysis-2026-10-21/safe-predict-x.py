"""Static literal extraction from pickle; never invoke pickle.load/REDUCE.

UBJSON is parsed as bounded primitive data. No Python object or model class
from the input is instantiated. The numeric-tree interpreter is local code.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import pickletools
import struct
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
REPO=TOPIC/'data/raw/metadegron/repo'
DERIVED=TOPIC/'data/raw/metadegron/derived'
FEATURES=['ASA_SCORE','DSS_SCORE','FCONS_SCORE','COIL','ANCHOR_SCORE','nflanking_ptms','nflanking_ub_lysines','HELIX','RIG_SCORE','Domain_pfam']

class UBJSON:
    def __init__(self,data):self.data=data;self.i=0;self.items=0
    def take(self,n):
        if n<0 or n>10_000_000 or self.i+n>len(self.data):raise ValueError('invalid length')
        d=self.data[self.i:self.i+n];self.i+=n;return d
    def integer(self,t):
        fmt={'U':'>B','i':'>b','I':'>h','l':'>i','L':'>q'}[t]
        return struct.unpack(fmt,self.take(struct.calcsize(fmt)))[0]
    def value(self,t=None,depth=0):
        self.items+=1
        if depth>60 or self.items>5_000_000:raise ValueError('parser bound')
        if t is None:t=self.take(1).decode('ascii')
        if t in 'UiIlL':return self.integer(t)
        if t in 'dD':return struct.unpack('>f' if t=='d' else '>d',self.take(4 if t=='d' else 8))[0]
        if t=='S':return self.take(self.value(depth=depth+1)).decode('utf-8')
        if t=='C':return self.take(1).decode('ascii')
        if t=='T':return True
        if t=='F':return False
        if t=='Z':return None
        if t in '{[':
            typed=None;count=None
            if self.data[self.i:self.i+1]==b'$':self.take(1);typed=self.take(1).decode('ascii')
            if self.data[self.i:self.i+1]==b'#':self.take(1);count=self.value(depth=depth+1)
            if count is not None and not 0<=count<=2_000_000:raise ValueError('container bound')
            result={} if t=='{' else [];end=b'}' if t=='{' else b']';n=0
            while (count is not None and n<count) or (count is None and self.data[self.i:self.i+1]!=end):
                if t=='{':
                    length=self.value(depth=depth+1);key=self.take(length).decode('utf-8')
                    if key in result:raise ValueError('duplicate object key')
                    result[key]=self.value(typed,depth+1)
                else:result.append(self.value(typed,depth+1))
                n+=1
            if count is None:self.take(1)
            return result
        raise ValueError(f'Unsupported UBJSON marker {t!r} at {self.i}')

def extract():
    p=REPO/'models/classifier_XGBoost.pickle';data=p.read_bytes()
    if len(data)>10_000_000:raise ValueError('pickle static scan bound')
    candidates=[];opcounts={}
    for op,arg,position in pickletools.genops(data):
        opcounts[op.name]=opcounts.get(op.name,0)+1
        if op.name in ['BINBYTES','BINBYTES8','BYTEARRAY8'] and isinstance(arg,(bytes,bytearray)) and bytes(arg).startswith(b'{'):
            candidates.append(bytes(arg))
    if len(candidates)!=1:raise ValueError('expected one literal UBJSON booster')
    parser=UBJSON(candidates[0]);state=parser.value()
    if parser.i!=len(candidates[0]):raise ValueError('unconsumed input')
    (DERIVED/'xgboost-literal-state.json').write_text(json.dumps(state))
    model=state['Model']['learner'];param=model['learner_model_param'];booster=model['gradient_booster']
    if booster['name']!='gbtree' or model['objective']['name']!='binary:logistic':raise ValueError('unsupported model family')
    if int(param['num_feature'])!=len(FEATURES):raise ValueError('feature count mismatch')
    ts=booster['model']['trees']
    for t in ts:
        if any(int(v)!=0 for v in t.get('split_type',[])):raise ValueError('categorical tree unsupported')
        nn=int(t['tree_param']['num_nodes'])
        for k in ['left_children','right_children','split_indices','split_conditions','default_left']:
            if len(t[k])!=nn:raise ValueError('inconsistent tree arrays')
    info={'checkpoint_sha256':hashlib.sha256(data).hexdigest(),'literal_sha256':hashlib.sha256(candidates[0]).hexdigest(),
          'pickle_opcodes':opcounts,'executed_opcodes':0,'trees':len(ts),'model_param':param,
          'objective':model['objective'],'feature_order':FEATURES,'feature_names':model.get('feature_names'),
          'parser_bytes_consumed':parser.i}
    return model,info

def predict(model,X):
    # XGBoost uses float32 comparisons. split_conditions at leaves already include eta.
    X=np.asarray(X,dtype=np.float32);base=float(model['learner_model_param']['base_score'])
    margin=np.full(len(X),math.log(base/(1-base)),dtype=np.float32)
    for t in model['gradient_booster']['model']['trees']:
        for i,row in enumerate(X):
            node=0
            for step in range(len(t['left_children'])+1):
                left=t['left_children'][node];right=t['right_children'][node]
                if left==-1:
                    margin[i]+=np.float32(t['split_conditions'][node]);break
                x=row[t['split_indices'][node]]
                node=left if (t['default_left'][node] if np.isnan(x) else x<np.float32(t['split_conditions'][node])) else right
                if node<0 or node>=len(t['left_children']):raise ValueError('invalid child')
            else:raise ValueError('cyclic tree')
    return 1/(1+np.exp(-margin))

def main(inspect_only=False):
    model,info=extract()
    if inspect_only:
        print(json.dumps(info,indent=2));return
    positive=pd.read_csv(REPO/'data/test_properties.tsv',sep='\t')
    rename={'solvent_accessibility':'ASA_SCORE','disorder':'DSS_SCORE','conservative_score':'FCONS_SCORE','coiled_coil':'COIL',
            'anchoring_score':'ANCHOR_SCORE','flanking_ptms':'nflanking_ptms','flanking_ub_lysine':'nflanking_ub_lysines',
            'a_helix':'HELIX','flexibility':'RIG_SCORE','structured_domain':'Domain_pfam'}
    positive=positive.rename(columns=rename)
    negative=pd.read_csv(REPO/'supporting_file/simulated_degron2.csv')
    ppos=predict(model,positive[FEATURES]);pneg=predict(model,negative[FEATURES])
    indices=np.arange(len(negative));res=[]
    for seed in list(range(1,11))+[17,29,43]:
        selected=pd.Series(indices).sample(n=len(positive),random_state=seed).to_numpy()
        y=np.r_[np.ones(len(ppos)),np.zeros(len(selected))];pred=np.r_[ppos,pneg[selected]]
        res.append({'seed':seed,'auroc':roc_auc_score(y,pred)})
    raw=pd.read_csv(REPO/'data/degron_data.txt',sep='\t');props=pd.read_csv(REPO/'data/annotated_degrons_properties.tsv',sep='\t')
    tkeys={(r.Entry,int(r.Start),int(r.End)) for _,r in positive.iterrows()}
    ckeys={(r.Entry,int(r.START),int(r.END)) for _,r in raw.iterrows()};pkeys={(r.Entry,int(r.START),int(r.END)) for _,r in props.iterrows()}
    mean=float(np.mean([r['auroc'] for r in res[:10]]))
    info.update(generator='safe-predict-x.py',method='static literal data plus independently authored numerical tree inference',
       positive_rows=len(positive),negative_pool=len(negative),results=res,published_mean=.9670,
       recalculated_author_seed_mean=mean,difference=mean-.9670,
       test_positive_coordinates_in_curated=len(tkeys&ckeys),test_positive_coordinates_in_properties=len(tkeys&pkeys),
       audit_seed_mean=float(np.mean([r['auroc'] for r in res[10:]])),
       limitation='same prepared property tables and stored weights; not original feature generation, independent experiment, or GPS transfer')
    (HERE/'safe-x-reproduction.json').write_text(json.dumps(info,indent=2))
    print(json.dumps({k:info[k] for k in ['trees','positive_rows','negative_pool','recalculated_author_seed_mean','difference','audit_seed_mean','test_positive_coordinates_in_curated','test_positive_coordinates_in_properties']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inspect-only',action='store_true');a=p.parse_args();main(a.inspect_only)
