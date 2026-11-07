#!/usr/bin/env python3
"""Đếm nhãn E3/adaptor thực sự dùng được từ CRISPR screen của Zhang 2023.

Dùng: python3 -I count_e3_labels.py <thư-mục-MAGeCK> <out.json>
Nguồn dữ liệu: Mendeley Data 10.17632/32h94v2yv2.2, file "Degron CRISPR Screens.zip".
Chỉ thư viện chuẩn.
"""
import sys, os, json, csv

# Thành phần chung của con đường CRL/UPS — xuất hiện ở mọi screen, KHÔNG phải adaptor đặc hiệu.
CORE = {
    "ARIH1","ARIH2","NEDD8","NAE1","UBA3","UBE2M","UBE2F","RBX1","RNF7",
    "CUL1","CUL2","CUL3","CUL4A","CUL4B","CUL5","RNF114",
    "SKP1","ELOB","ELOC","TCEB1","TCEB2","RBX2",
    "VCP","NFE2L1","NGLY1","DDI2","SEM1","PSMD14","UCHL5",
    "UBA1","UBE2D1","UBE2D2","UBE2D3","UBE2R2","CDC34",
    "DDB1","DCUN1D1","COPS2","COPS3","COPS4","COPS5","COPS6","COPS7A","COPS8","GPS1",
}
def is_proteasome(g):
    return g.startswith(("PSMA","PSMB","PSMC","PSMD","PSME","POMP"))

def top_pos(path, fdr_max=0.25, nmax=25):
    rows=[]
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            try:
                rank=int(r["pos|rank"]); fdr=float(r["pos|fdr"])
                lfc=float(r["pos|lfc"]); good=int(r["pos|goodsgrna"])
                sc=float(r["pos|score"])
            except (KeyError,ValueError):
                continue
            rows.append(dict(gene=r["id"],rank=rank,fdr=fdr,lfc=lfc,good=good,score=sc))
    rows.sort(key=lambda x:x["rank"])
    return [x for x in rows[:nmax] if x["fdr"]<=fdr_max]

def main():
    d, out = sys.argv[1], sys.argv[2]
    res={}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"): continue
        pep=fn[:-4]
        if pep.lower().startswith("control"): continue
        hits=top_pos(os.path.join(d,fn))
        cand=[h for h in hits
              if h["gene"] not in CORE and not is_proteasome(h["gene"])]
        res[pep]=dict(
            n_hits_fdr25=len(hits),
            top10_all=[(h["gene"],round(h["fdr"],4),round(h["lfc"],2),h["good"]) for h in hits[:10]],
            candidate_adaptors=[(h["gene"],round(h["fdr"],4),round(h["lfc"],2),h["good"]) for h in cand[:6]],
        )
    summary=dict(
        n_screens=len(res),
        n_screens_with_any_hit=sum(1 for v in res.values() if v["n_hits_fdr25"]>0),
        n_screens_with_candidate=sum(1 for v in res.values() if v["candidate_adaptors"]),
    )
    json.dump(dict(summary=summary,screens=res), open(out,"w"), indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1))
    for p,v in res.items():
        c=v["candidate_adaptors"]
        print(f"{p:<14} hits={v['n_hits_fdr25']:>3}  ứng viên adaptor: "
              + (", ".join(f"{g}(fdr={f},lfc={l},sg={s})" for g,f,l,s in c[:3]) if c else "— KHÔNG CÓ"))

if __name__=="__main__":
    main()
