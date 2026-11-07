#!/usr/bin/env python3
"""Chồng lấn giữa ba bộ: screen CRISPR (31 peptide), đột biến bão hòa (249), đột biến quét.
Dùng: python3 -I overlap.py <MAGeCK_dir> <satmut_dir> <scanmut_csv> <out.json>
"""
import sys, os, json, csv, re
PAT=re.compile(r"^(?P<pep>.+?)_mut(?P<pos>\d+)")

def norm(name):
    """CRISPR đặt tên GENE_NUM; bộ mutagenesis đặt ACC_GENE_NUM -> chuẩn hóa về GENE_NUM."""
    p=name.split("_")
    return "_".join(p[-2:]) if len(p)>=2 else name

def main():
    mg,sat,scan,out=sys.argv[1:5]
    crispr={f[:-4] for f in os.listdir(mg) if f.endswith(".txt") and not f.lower().startswith("control")}
    satp=set()
    for fn in os.listdir(sat):
        if not fn.endswith(".txt"): continue
        with open(os.path.join(sat,fn),encoding="utf-8",errors="replace") as fh:
            for line in fh:
                m=PAT.match(line.split("\t")[0])
                if m: satp.add(m.group("pep"))
        break  # một file đủ: thư viện giống nhau giữa các bin
    csv.field_size_limit(10**7)
    scanp=set()
    with open(scan,newline="",encoding="utf-8",errors="replace") as fh:
        for r in csv.DictReader(fh):
            m=PAT.match(r["Gene"])
            if m: scanp.add(m.group("pep"))
    cn, sn, scn = {norm(x) for x in crispr}, {norm(x) for x in satp}, {norm(x) for x in scanp}
    res=dict(
      sizes=dict(crispr=len(crispr), satmut=len(satp), scanmut=len(scanp)),
      normalised_sizes=dict(crispr=len(cn), satmut=len(sn), scanmut=len(scn)),
      overlap=dict(
        crispr_in_satmut=len(cn&sn), crispr_in_scanmut=len(cn&scn),
        satmut_in_scanmut=len(sn&scn),
        crispr_in_both=len(cn&sn&scn)),
      crispr_with_satmut=sorted(cn&sn),
      crispr_without_satmut=sorted(cn-sn),
    )
    json.dump(res,open(out,"w"),indent=1,ensure_ascii=False)
    print(json.dumps(res,indent=1,ensure_ascii=False))

if __name__=="__main__": main()
