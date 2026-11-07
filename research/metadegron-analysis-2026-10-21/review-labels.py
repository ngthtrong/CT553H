"""Summarize a manually inspected 40-row source-trace review.

This is evidence tracing, not a claim of having rerun biological experiments.
Per-row source records are retained only in ignored raw/derived/.
"""
from pathlib import Path
import json
import math
import pandas as pd

HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
ROOT=next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
RAW=TOPIC/'data/raw/metadegron';DERIVED=RAW/'derived'

def wilson(k,n):
    z=1.959963984540054;p=k/n;c=(p+z*z/(2*n))/(1+z*z/n)
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return {'count':k,'n':n,'rate':p,'ci95':[c-h,c+h]}

def main():
    rows=json.loads((DERIVED/'label-sample-records.json').read_text())['rows'];reviews=[]
    for r in rows:
        f=RAW/f'elm-sample-{r["row"]}.tsv';d=pd.read_csv(f,sep='\t',comment='#')
        hit=d[(d.ELMIdentifier==r['class'])&(d.Start<=r['end'])&(d.End>=r['start'])]
        supported=not hit.empty and any(hit.InstanceLogic=='true positive')
        ubiq=any('ubiquitinase assay' in str(m) for m in hit.Methods)
        note='ELM hiện hành có true-positive cùng lớp và giao tọa độ; Methods/References đã đọc. Chưa truy đọc toàn bộ thí nghiệm gốc.' if supported else 'Không tìm thấy record cùng lớp/tọa độ trong truy vấn protein ELM hiện hành. PMID tổng hợp trong S2 không đủ xác nhận từng thí nghiệm; không coi đây là nhãn sai.'
        if r['class']=='DEG_APCC_TPR_1':note+=' Motif TPR có thể là chỗ gắn co-activator của APC/C; tương tác không tự chứng minh là tín hiệu làm hủy protein nguồn.'
        if r['row'] in [54,105]:note+=' BUB1B tham gia phức hợp checkpoint; cần tách nhận diện/tương tác APC/C khỏi phân hủy BUB1B.'
        reviews.append({**r,'elm_query_rows':len(d),'elm_matching_records':len(hit),
             'curation_supported':supported,'ubiquitination_assay_in_elm_metadata':ubiq,
             'biological_label':'not-fully-adjudicated','wrong_human_scope':r['species_suffix']!='HUMAN',
             'status':'curation-supported' if supported else 'unresolved-lineage','review_note':note,
             'matched_elm':hit[['Accession','Start','End','References','Methods','InstanceLogic']].fillna('').to_dict('records')})
    (DERIVED/'manual-label-review-records.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False))
    n=len(rows);supported=sum(r['curation_supported'] for r in reviews)
    out={'generator':'review-labels.py','sampling':'simple random without replacement, seed17','n':n,
       'curation_supported':wilson(supported,n),'unresolved_lineage':wilson(n-supported,n),
       'not_human_despite_s2_title':wilson(sum(r['wrong_human_scope'] for r in reviews),n),
       'ubiquitination_assay_in_elm_metadata':wilson(sum(r['ubiquitination_assay_in_elm_metadata'] for r in reviews),n),
       'all_source_coordinate_slices_contained_in_reported_peptide':all(r['reported_contains_core'] for r in rows),
       'biological_wrong_rate':None,'biological_ambiguity_rate':None,
       'why_null':'Source-trace review is complete for 40 rows, but direct primary experimental adjudication is incomplete; no defensible biological mislabel rate.',
       'details_path':str((DERIVED/'manual-label-review-records.json').relative_to(ROOT)),
       'scope_of_manual_read':'all 40 rows, source coordinates, S2 PMIDs, current ELM matching metadata; not all underlying experimental papers',
       'important_distinction':f'{n-supported} unresolved traces do not mean {n-supported} wrong degrons; ELM true-positive binding motif does not by itself prove degradation'}
    (HERE/'manual-label-review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
