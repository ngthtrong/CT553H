#!/usr/bin/env python3
"""Đếm peptide thực sự CÓ footprint học được trong bộ đột biến quét Zhang 2023.

Dùng: python3 -I count_footprints.py <CSV replicate> <out.json>
Nguồn: Mendeley Data 10.17632/32h94v2yv2.2, "I28 Scanning Mutagenesis.zip".

Định nghĩa dùng ở đây, ghi tường minh:
 - PSI thang 1–6, THẤP = peptide bị phân hủy nhanh (có degron mạnh).
 - "peptide là degron" nếu PSI hoang dã (mut0) <= DEGRON_PSI_MAX.
 - "có footprint" nếu tồn tại >= MIN_RESCUE vị trí mà đột biến làm PSI TĂNG
   >= RESCUE_DELTA so với hoang dã (tức phá degron thì peptide bền lên).
 - Chỉ tính biến thể có Sum >= READ_MIN.
Chỉ thư viện chuẩn.
"""
import sys, csv, json, re, statistics
from collections import defaultdict

PAT=re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)$")
READ_MIN=10
DEGRON_PSI_MAX=3.0
RESCUE_DELTA=1.0
MIN_RESCUE=1
MIN_POS_COVERED=21

def main():
    path,out=sys.argv[1],sys.argv[2]
    csv.field_size_limit(10**7)
    wt={}; mut=defaultdict(dict)
    with open(path,newline="",encoding="utf-8",errors="replace") as fh:
        for r in csv.DictReader(fh):
            m=PAT.match(r["Gene"])
            if not m: continue
            try: s=float(r["Sum"])
            except (TypeError,ValueError): continue
            p=r["PSI"]
            if p in ("NA","","NaN",None) or s<READ_MIN: continue
            pep=m.group("pep"); pos=int(m.group("pos")); psi=float(p)
            if pos==0: wt[pep]=psi
            else: mut[pep][pos]=psi

    rows=[]
    for pep,w in wt.items():
        d=mut.get(pep,{})
        if not d: continue
        deltas={k:v-w for k,v in d.items()}
        rescue=[k for k,x in deltas.items() if x>=RESCUE_DELTA]
        rows.append(dict(pep=pep, wt=w, n_pos=len(d),
                         n_rescue=len(rescue),
                         max_delta=max(deltas.values()),
                         rng=max(d.values())-min(d.values())))
    n_all=len(rows)
    degron=[r for r in rows if r["wt"]<=DEGRON_PSI_MAX]
    cov=[r for r in degron if r["n_pos"]>=MIN_POS_COVERED]
    fp=[r for r in cov if r["n_rescue"]>=MIN_RESCUE]
    sharp=[r for r in fp if r["n_rescue"]<=6]   # footprint khu trú, không dàn đều

    def dist(rs,key):
        v=sorted(x[key] for x in rs)
        if not v: return {}
        return dict(min=round(v[0],2), p25=round(v[len(v)//4],2),
                    median=round(statistics.median(v),2),
                    p75=round(v[3*len(v)//4],2), max=round(v[-1],2))
    res=dict(
      source=dict(dataset="Mendeley Data 10.17632/32h94v2yv2.2",
                  file="I28 Scanning Mutagenesis.zip",
                  table="I28 Scanning Mutagenesis Replicate 1.csv"),
      definitions=dict(read_min=READ_MIN, degron_psi_max=DEGRON_PSI_MAX,
                       rescue_delta=RESCUE_DELTA, min_rescue=MIN_RESCUE,
                       min_pos_covered=MIN_POS_COVERED,
                       note="PSI thang 1-6, thap = bi phan huy nhanh"),
      counts=dict(
        peptides_with_wt_and_mutants=n_all,
        is_degron_wt_psi_le_3=len(degron),
        degron_and_coverage_ge21=len(cov),
        degron_coverage_and_has_footprint=len(fp),
        footprint_localised_le6_positions=len(sharp)),
      distributions=dict(
        n_rescue_positions_among_footprints=dist(fp,"n_rescue"),
        max_delta_among_footprints=dist(fp,"max_delta"),
        psi_range_among_footprints=dist(fp,"rng"),
        wt_psi_all=dist(rows,"wt")),
      sensitivity=[],
    )
    for dmax in (2.5,3.0,3.5):
        for rd in (0.5,1.0,1.5):
            dd=[r for r in rows if r["wt"]<=dmax and r["n_pos"]>=MIN_POS_COVERED]
            ff=[r for r in dd if sum(1 for k,v in mut[r["pep"]].items() if v-r["wt"]>=rd)>=MIN_RESCUE]
            res["sensitivity"].append(dict(degron_psi_max=dmax, rescue_delta=rd,
                                           n_degron=len(dd), n_with_footprint=len(ff)))
    json.dump(res,open(out,"w"),indent=1,ensure_ascii=False)
    print(json.dumps({k:res[k] for k in ("counts","distributions")},indent=1,ensure_ascii=False))
    print("\nđộ nhạy theo ngưỡng:")
    print(f"{'PSI<=':>6} {'Δ>=':>5} {'#degron':>8} {'#có footprint':>14}")
    for s in res["sensitivity"]:
        print(f"{s['degron_psi_max']:>6} {s['rescue_delta']:>5} {s['n_degron']:>8} {s['n_with_footprint']:>14}")

if __name__=="__main__": main()
