#!/usr/bin/env python3
"""Quét ngưỡng: số peptide gán được E3 và số E3 khác nhau phụ thuộc ngưỡng thế nào.
Dùng: python3 -I sweep_thresholds.py <thư-mục-MAGeCK> <out.json>
"""
import sys, os, json, csv
from collections import defaultdict
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from assign_e3 import is_core, is_adaptor, read

def count(screens, fdr_max, lfc_min, sg_min):
    per=defaultdict(list); unass=0
    for pep,rows in screens.items():
        cand=[r for r in rows if r["fdr"]<=fdr_max and r["lfc"]>=lfc_min
              and r["good"]>=sg_min and is_adaptor(r["gene"]) and not is_core(r["gene"])]
        if cand:
            per[max(cand,key=lambda x:x["lfc"])["gene"]].append(pep)
        else: unass+=1
    sizes=sorted((len(v) for v in per.values()),reverse=True)
    return dict(assigned=sum(len(v) for v in per.values()), unassigned=unass,
                n_e3=len(per), sizes=sizes,
                n_e3_ge5=sum(1 for s in sizes if s>=5),
                n_e3_ge10=sum(1 for s in sizes if s>=10),
                n_singleton=sum(1 for s in sizes if s==1),
                top=max(sizes) if sizes else 0)

def main():
    d,out=sys.argv[1],sys.argv[2]
    screens={fn[:-4]:read(os.path.join(d,fn)) for fn in sorted(os.listdir(d))
             if fn.endswith(".txt") and not fn.lower().startswith("control")}
    grid=[]
    print(f"{'fdr':>5} {'lfc':>5} {'sg':>3} | {'gán':>4} {'ko gán':>6} {'#E3':>4} {'E3>=5':>6} {'E3>=10':>7} {'1 mẫu':>6} {'lớn nhất':>8}")
    for fdr in (0.05,0.10,0.25):
        for lfc in (1.0,1.5,2.0,2.5):
            for sg in (3,4,5):
                c=count(screens,fdr,lfc,sg)
                grid.append(dict(fdr=fdr,lfc=lfc,sg=sg,**c))
                print(f"{fdr:>5} {lfc:>5} {sg:>3} | {c['assigned']:>4} {c['unassigned']:>6} "
                      f"{c['n_e3']:>4} {c['n_e3_ge5']:>6} {c['n_e3_ge10']:>7} {c['n_singleton']:>6} {c['top']:>8}")
    json.dump(dict(n_screens=len(screens),grid=grid),open(out,"w"),indent=1)
    a=[g['assigned'] for g in grid]; e=[g['n_e3'] for g in grid]
    print(f"\nbiên độ: gán được {min(a)}–{max(a)} trên {len(screens)} screen; số E3 {min(e)}–{max(e)}")
    print(f"số E3 có >=5 peptide: {sorted({g['n_e3_ge5'] for g in grid})}")
    print(f"số E3 có >=10 peptide: {sorted({g['n_e3_ge10'] for g in grid})}")

if __name__=="__main__": main()
