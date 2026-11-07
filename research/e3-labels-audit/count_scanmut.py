#!/usr/bin/env python3
"""Đếm tài nguyên đột biến quét (scanning mutagenesis) của Zhang 2023.

Dùng: python3 -I count_scanmut.py <file CSV replicate> <out.json>
Nguồn: Mendeley Data 10.17632/32h94v2yv2.2, "I28 Scanning Mutagenesis.zip",
       file "I28 Scanning Mutagenesis Replicate 1.csv".
Cột: Gene (ID dạng <peptide>_mut<pos>, mut0 = hoang dã), AA.Seq, b1..b6, nb1..nb6, Sum, PSI.
Chỉ thư viện chuẩn.
"""
import sys, csv, json, re, statistics
from collections import defaultdict

PAT=re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")
READ_MIN=10

def main():
    path,out=sys.argv[1],sys.argv[2]
    csv.field_size_limit(10**7)
    pos_all=defaultdict(set); pos_scored=defaultdict(set); pos_strong=defaultdict(set)
    wt_scored=set(); n=0; n_psi=0; n_strong=0; unparsed=0
    psi_vals=[]
    with open(path,newline="",encoding="utf-8",errors="replace") as fh:
        for r in csv.DictReader(fh):
            n+=1
            ident=r["Gene"]; m=PAT.match(ident)
            if not m: unparsed+=1; continue
            pep=m.group("pep"); p=int(m.group("pos"))
            pos_all[pep].add(p)
            try: s=float(r["Sum"])
            except (TypeError,ValueError): s=0.0
            psi=r["PSI"]
            has=psi not in ("NA","","NaN",None)
            if has:
                n_psi+=1; psi_vals.append(float(psi))
                if p==0: wt_scored.add(pep)
                else: pos_scored[pep].add(p)
                if s>=READ_MIN:
                    n_strong+=1
                    if p>0: pos_strong[pep].add(p)
    cov=lambda d,k: sum(1 for v in d.values() if len(v)>=k)
    sz=lambda d: [len(v) for v in d.values()] or [0]
    res=dict(
      source=dict(dataset="Mendeley Data 10.17632/32h94v2yv2.2",
                  file="I28 Scanning Mutagenesis.zip",
                  table="I28 Scanning Mutagenesis Replicate 1.csv",
                  read_filter=f"Sum >= {READ_MIN}"),
      rows=dict(total=n, with_psi=n_psi, with_psi_and_reads=n_strong, unparsed=unparsed),
      peptides=dict(
        in_library=len(pos_all),
        with_any_scored_mutant=len(pos_scored),
        with_scored_wildtype=len(wt_scored),
        with_wt_and_ge1_mutant=len(set(wt_scored)&set(pos_scored))),
      position_coverage_scored=dict(
        ge_1=cov(pos_scored,1), ge_7=cov(pos_scored,7), ge_14=cov(pos_scored,14),
        ge_21=cov(pos_scored,21), ge_24=cov(pos_scored,24), ge_27=cov(pos_scored,27)),
      position_coverage_after_read_filter=dict(
        ge_1=cov(pos_strong,1), ge_14=cov(pos_strong,14),
        ge_21=cov(pos_strong,21), ge_24=cov(pos_strong,24), ge_27=cov(pos_strong,27)),
      positions_per_peptide_scored=dict(
        min=min(sz(pos_scored)), median=statistics.median(sz(pos_scored)),
        mean=round(statistics.mean(sz(pos_scored)),1), max=max(sz(pos_scored))),
      psi_distribution=dict(
        n=len(psi_vals), min=round(min(psi_vals),4), max=round(max(psi_vals),4),
        mean=round(statistics.mean(psi_vals),4), sd=round(statistics.pstdev(psi_vals),4)) if psi_vals else {},
    )
    json.dump(res,open(out,"w"),indent=1,ensure_ascii=False)
    print(json.dumps(res,indent=1,ensure_ascii=False))

if __name__=="__main__": main()
