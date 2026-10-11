#!/usr/bin/env python3
"""Gán adaptor E3 cho từng peptide degron từ CRISPR screen của Zhang 2023.

Dùng: python3 -I assign_e3.py <thư-mục-MAGeCK> <out.json>
Nguồn: Mendeley Data 10.17632/32h94v2yv2.2, "Degron CRISPR Screens.zip",
       thư mục "Degron CRISPR (new)/MAGEcK (Completed)".
Chỉ thư viện chuẩn. Mọi ngưỡng ghi tường minh trong file JSON kết quả.

Logic: tế bào được sort theo GFP/DsRed CAO, nên sgRNA làm peptide BỀN hơn sẽ
giàu lên trong mẫu sort -> dùng cột pos| của MAGeCK. Loại bộ máy chung của
con đường (proteasome, neddylation, cullin scaffold, E2) theo danh sách tường
minh — KHÔNG loại theo tần suất, vì một adaptor thật có thể là hub nhận nhiều
peptide (KLHL15 là ví dụ trong chính bài báo).
"""
import sys, os, json, csv
from collections import defaultdict

CORE_EXACT = {
    # neddylation, scaffold, RBR/E2, COP9, p97, deubiquitinase chung
    "NAE1","UBA3","NEDD8","UBE2M","UBE2F","DCUN1D1","DCUN1D5",
    "CUL1","CUL2","CUL3","CUL4A","CUL4B","CUL5","CUL7","CUL9",
    "RBX1","RNF7","SKP1","ELOB","ELOC","TCEB1","TCEB2","DDB1","DDA1",
    "ARIH1","ARIH2","UBE2L3","UBE2D1","UBE2D2","UBE2D3","UBE2R2","CDC34",
    "UBA1","UBE2Q1","UBE2V1","TMEM189-UBE2V1",
    "COPS2","COPS3","COPS4","COPS5","COPS6","COPS7A","COPS7B","COPS8","GPS1",
    "VCP","NPLOC4","UFD1","UFD1L","NFE2L1","NGLY1","DDI2","SEM1","UCHL5",
    "POMP","PSMG1","PSMG2","PSMG3","PSMG4","ADRM1","PAAF1",
    "UBL5","PHF5A","PPIL2","RNF113A",  # thành phần spliceosome/khác, tái diễn
}
def is_core(g):
    return g in CORE_EXACT or g.startswith(("PSMA","PSMB","PSMC","PSMD","PSME","PSMF"))

ADAPTOR_PREFIX = ("FBXW","FBXO","FBXL","KLHL","KBTBD","KCTD","BTBD","DCAF","ASB",
                  "SOCS","WSB","SPSB","RAB40","FEM1","ZYG11","KLHDC","LRR1")
ADAPTOR_EXACT = {"BTRC","SKP2","SPOP","KEAP1","ENC1","VPRBP","DTL","DDB2","CRBN",
                 "AMBRA1","PHIP","ZER1","PRAME","ELOA","APPBP2","GPR75-ASB3","BAG6"}
def is_adaptor(g):
    return g in ADAPTOR_EXACT or g.startswith(ADAPTOR_PREFIX)

FDR_MAX, LFC_MIN, SG_MIN, MARGIN_MIN = 0.10, 1.5, 4, 0.5

def read(p):
    out=[]
    with open(p,newline="",encoding="utf-8",errors="replace") as fh:
        for r in csv.DictReader(fh,delimiter="\t"):
            try: out.append(dict(gene=r["id"],fdr=float(r["pos|fdr"]),
                                 lfc=float(r["pos|lfc"]),good=int(r["pos|goodsgrna"])))
            except (KeyError,ValueError): pass
    return out

def main():
    d,out=sys.argv[1],sys.argv[2]
    screens={fn[:-4]:read(os.path.join(d,fn)) for fn in sorted(os.listdir(d))
             if fn.endswith(".txt") and not fn.lower().startswith("control")}
    n=len(screens)
    freq=defaultdict(int)
    for rows in screens.values():
        for r in rows:
            if r["fdr"]<=FDR_MAX and r["lfc"]>=LFC_MIN and r["good"]>=SG_MIN:
                freq[r["gene"]]+=1

    assign={}; per_e3=defaultdict(list)
    for pep,rows in screens.items():
        passing=[r for r in rows if r["fdr"]<=FDR_MAX and r["lfc"]>=LFC_MIN and r["good"]>=SG_MIN]
        cand=[r for r in passing if is_adaptor(r["gene"]) and not is_core(r["gene"])]
        cand.sort(key=lambda x:-x["lfc"])
        noncore=[r for r in passing if not is_core(r["gene"])]
        noncore.sort(key=lambda x:-x["lfc"])
        if cand:
            top=cand[0]; second=cand[1]["lfc"] if len(cand)>1 else 0.0
            # đối thủ ngoài họ adaptor nhưng mạnh hơn -> cờ cảnh báo
            stronger=[(r["gene"],round(r["lfc"],2)) for r in noncore
                      if r["lfc"]>top["lfc"] and r["gene"]!=top["gene"]][:3]
            assign[pep]=dict(e3=top["gene"],lfc=round(top["lfc"],2),fdr=round(top["fdr"],6),
                             sg=top["good"],margin=round(top["lfc"]-second,2),
                             n_adaptor_candidates=len(cand),
                             other_adaptors=[(c["gene"],round(c["lfc"],2)) for c in cand[1:4]],
                             stronger_nonadaptor=stronger)
            per_e3[top["gene"]].append(pep)
        else:
            assign[pep]=dict(e3=None,n_adaptor_candidates=0,
                             best_noncore=[(r["gene"],round(r["lfc"],2),round(r["fdr"],4))
                                           for r in noncore[:4]])
    clear={p:v for p,v in assign.items()
           if v["e3"] and v["margin"]>=MARGIN_MIN and not v["stronger_nonadaptor"]}
    res=dict(
      source=dict(dataset="Mendeley Data 10.17632/32h94v2yv2.2",
                  file="Degron CRISPR Screens.zip",
                  subdir="Degron CRISPR (new)/MAGEcK (Completed)"),
      thresholds=dict(column="pos|",fdr_max=FDR_MAX,lfc_min=LFC_MIN,
                      good_sgrna_min=SG_MIN,margin_min=MARGIN_MIN,
                      core_excluded_by="danh sách tường minh, không theo tần suất"),
      summary=dict(n_screens=n,
        n_assigned=sum(1 for v in assign.values() if v["e3"]),
        n_unassigned=sum(1 for v in assign.values() if not v["e3"]),
        n_assigned_clear=len(clear),
        n_distinct_e3=len(per_e3),
        peptides_per_e3={k:len(v) for k,v in sorted(per_e3.items(),key=lambda x:-len(x[1]))}),
      adaptor_frequency_across_screens={g:c for g,c in sorted(freq.items(),key=lambda x:-x[1])
                                        if is_adaptor(g) and not is_core(g)},
      assignment=assign,
      e3_to_peptides={k:sorted(v) for k,v in sorted(per_e3.items(),key=lambda x:-len(x[1]))})
    json.dump(res,open(out,"w"),indent=1,ensure_ascii=False)
    s=res["summary"]
    print(f"screen CRISPR: {s['n_screens']}")
    print(f"gán được adaptor: {s['n_assigned']}   không gán được: {s['n_unassigned']}   gán RÕ: {s['n_assigned_clear']}")
    print(f"số E3 khác nhau: {s['n_distinct_e3']}\n")
    print("peptide trên mỗi E3:")
    for k,v in s["peptides_per_e3"].items(): print(f"  {k:<13} {v:>2}  {', '.join(res['e3_to_peptides'][k])}")
    print("\nkhông gán được:")
    for p,v in sorted(assign.items()):
        if not v["e3"]: print(f"  {p:<14} hit mạnh nhất ngoài bộ máy chung: {v['best_noncore']}")
    print("\ncờ cảnh báo (có hit ngoài họ adaptor mạnh hơn):")
    for p,v in sorted(assign.items()):
        if v["e3"] and v["stronger_nonadaptor"]: print(f"  {p:<14} -> {v['e3']}, nhưng mạnh hơn: {v['stronger_nonadaptor']}")

if __name__=="__main__": main()
