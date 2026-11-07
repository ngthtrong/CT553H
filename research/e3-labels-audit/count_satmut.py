#!/usr/bin/env python3
"""Đếm tài nguyên đột biến bão hòa (219 footprint) của Zhang 2023.

Dùng: python3 -I count_satmut.py <thư-mục-đếm-reads> <out.json>
Nguồn: Mendeley Data 10.17632/32h94v2yv2.2, "I28 CRL Saturation Mutagenesis.zip".
Định dạng mỗi file: <peptideID>[_mut<pos><aa>]\t<reads>, một file cho mỗi bin/mẫu.
Chỉ thư viện chuẩn.
"""
import sys, os, json, re
from collections import defaultdict

PAT=re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)(?P<aa>[A-Za-z])$")

def main():
    d,out=sys.argv[1],sys.argv[2]
    files=sorted(f for f in os.listdir(d) if f.endswith(".txt"))
    reads=defaultdict(int)          # id -> tổng reads trên mọi mẫu
    present=defaultdict(int)        # id -> số mẫu có mặt
    for fn in files:
        with open(os.path.join(d,fn),encoding="utf-8",errors="replace") as fh:
            for line in fh:
                parts=line.rstrip("\n").split("\t")
                if len(parts)<2: continue
                try: c=int(parts[1])
                except ValueError: continue
                reads[parts[0]]+=c
                if c>0: present[parts[0]]+=1

    pep_pos=defaultdict(set); pep_mut=defaultdict(set); wt=set(); unparsed=set()
    for ident in reads:
        m=PAT.match(ident)
        if m:
            p=m.group("pep"); pep_pos[p].add(int(m.group("pos")))
            pep_mut[p].add((int(m.group("pos")),m.group("aa").upper()))
        else:
            wt.add(ident); unparsed.add(ident)

    all_peps=set(pep_pos)|wt
    # độ phủ: bao nhiêu peptide có >=27 trong 28 vị trí được đột biến
    cov=lambda k: sum(1 for p,s in pep_pos.items() if len(s)>=k)
    # ngưỡng reads: chỉ giữ biến thể có tổng reads >= 10 trên toàn bộ mẫu
    strong=defaultdict(set)
    for ident,c in reads.items():
        if c>=10:
            m=PAT.match(ident)
            if m: strong[m.group("pep")].add(int(m.group("pos")))

    res=dict(
      source=dict(dataset="Mendeley Data 10.17632/32h94v2yv2.2",
                  file="I28 CRL Saturation Mutagenesis.zip", n_sample_files=len(files)),
      totals=dict(
        n_identifiers=len(reads), n_mutant_identifiers=sum(len(v) for v in pep_mut.values()),
        n_wildtype_identifiers=len(wt), n_distinct_peptides=len(all_peps),
        total_reads=sum(reads.values())),
      position_coverage=dict(
        peptides_with_ge_1_pos=cov(1), peptides_with_ge_14_pos=cov(14),
        peptides_with_ge_24_pos=cov(24), peptides_with_ge_27_pos=cov(27),
        peptides_with_ge_28_pos=cov(28)),
      after_read_filter_ge10=dict(
        peptides=len(strong),
        peptides_with_ge_24_pos=sum(1 for s in strong.values() if len(s)>=24),
        peptides_with_ge_27_pos=sum(1 for s in strong.values() if len(s)>=27)),
      mutants_per_peptide=dict(
        min=min((len(v) for v in pep_mut.values()),default=0),
        median=sorted(len(v) for v in pep_mut.values())[len(pep_mut)//2] if pep_mut else 0,
        max=max((len(v) for v in pep_mut.values()),default=0)),
      example_peptides=sorted(all_peps)[:5],
      unparsed_examples=sorted(unparsed)[:5],
    )
    json.dump(res,open(out,"w"),indent=1,ensure_ascii=False)
    print(json.dumps(res,indent=1,ensure_ascii=False))

if __name__=="__main__": main()
