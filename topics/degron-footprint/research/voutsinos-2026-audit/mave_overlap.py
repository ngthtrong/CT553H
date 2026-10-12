import csv, gzip, sys, json
from collections import defaultdict
biomart_gz, train_gz, full_gz, out = sys.argv[1:5]
genes = ["PTEN","TPMT","NUDT15","CYP2C9","CYP2C19","ASPA","PRKN","GCK","LDLR"]
sym2ensg = defaultdict(set)
with gzip.open(biomart_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        sym2ensg[r['Gene name']].add(r['Gene stable ID'])
tiles_train = defaultdict(int); tiles_all = defaultdict(int)
with gzip.open(train_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        if '_tile' in r['name']: tiles_train[r['name'].split('_tile')[0]] += 1
with gzip.open(full_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        if '_tile' in r['name']: tiles_all[r['name'].split('_tile')[0]] += 1
print(f"{'gene':9} {'ENSG':18} {'trong lib?':11} {'tile tong':>9} {'tile train':>10}")
res={}
for g in genes:
    ids = sorted(sym2ensg.get(g,[]))
    if not ids:
        print(f"{g:9} {'(khong co)':18} {'KHONG':11} {0:9} {0:10}")
        res[g]={"in_library":False,"ensg":None,"tiles_total":0,"tiles_in_train":0}; continue
    for e in ids:
        ta, tt = tiles_all.get(e,0), tiles_train.get(e,0)
        mark = 'CO' if ta>0 else 'co ENSG, 0 tile'
        print(f"{g:9} {e:18} {mark:11} {ta:9} {tt:10}")
        res.setdefault(g,{"in_library":ta>0,"ensg":e,"tiles_total":ta,"tiles_in_train":tt})
n_lib=sum(1 for v in res.values() if v["in_library"])
n_train=sum(1 for v in res.values() if v["tiles_in_train"]>0)
print(f"\n=> {n_lib}/9 gene co tile trong thu vien; {n_train}/9 gene co tile trong TAP TRAIN")
print("=> gene KHONG co trong thu vien:", [g for g,v in res.items() if not v["in_library"]])
json.dump(res, open(out,'w'), indent=1); print("wrote", out)
