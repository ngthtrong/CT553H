import csv, gzip, sys, json
import numpy as np
from collections import defaultdict
full_gz, train_gz, holdout_txt, out = sys.argv[1:5]
gene=lambda n:n.split('_tile')[0]
full=defaultdict(list); 
for r in csv.DictReader(gzip.open(full_gz,'rt')):
    if '_tile' in r['name']: full[gene(r['name'])].append(r)
trn=defaultdict(set)
for r in csv.DictReader(gzip.open(train_gz,'rt')):
    if '_tile' in r['name']: trn[gene(r['name'])].add(r['name'])
hold={l.strip() for l in open(holdout_txt) if l.strip()}

g96=[g for g in hold if g in trn and len(trn[g])==len(full[g])]
g428=[g for g in hold if g not in trn]
g297=[g for g in full if g not in hold and len(trn.get(g,set()))<len(full[g])]
print(f"96-group (trong danh sach holdout nhung toan bo tile o train): {len(g96)}")
print(f"428-group (holdout hieu dung): {len(g428)}")
print(f"297-group (co tile ngoai train nhung KHONG trong danh sach holdout): {len(g297)}")

def stats(gs, lab):
    nt=[len(full[g]) for g in gs]
    reps=[float(r['n']) for g in gs for r in full[g] if r['n'] not in ('','NA')]
    miss=[1-len(trn.get(g,set()))/len(full[g]) for g in gs]
    print(f"\n{lab}: n_gene={len(gs)}")
    print(f"  tile/gene: trung binh {np.mean(nt):.1f} trung vi {np.median(nt):.0f} min {min(nt)} max {max(nt)}")
    print(f"  so lan do (n): trung binh {np.mean(reps):.2f} trung vi {np.median(reps):.0f}")
    print(f"  ti le tile BI THIEU khoi train: trung binh {np.mean(miss)*100:.1f}%  (0% = khong thieu gi)")
    return {"n_gene":len(gs),"tiles_mean":round(float(np.mean(nt)),1),"reps_mean":round(float(np.mean(reps)),2),
            "frac_tiles_missing_mean":round(float(np.mean(miss)),4)}
res={"g96":stats(g96,"NHOM 96"),"g428":stats(g428,"NHOM 428 (holdout hieu dung)"),"g297":stats(g297,"NHOM 297")}

# 297-group: thieu toan bo hay thieu mot phan?
whole=[g for g in g297 if g not in trn]
part=[g for g in g297 if g in trn]
print(f"\nNHOM 297 phan ra: thieu TOAN BO tile = {len(whole)} gene | thieu MOT PHAN = {len(part)} gene")
res["g297_all_missing"]=len(whole); res["g297_partial"]=len(part)
if part:
    fr=[1-len(trn[g])/len(full[g]) for g in part]
    print(f"  nhom thieu mot phan: ti le thieu trung binh {np.mean(fr)*100:.1f}%, trung vi {np.median(fr)*100:.1f}%")
# tong kiem ke
print(f"\nKIEM KE: 428 + 297(toan bo {len(whole)}) = {len(g428)+len(whole)} gene khong co tile nao o train")
print(f"Tong gene trong bang day du: {len(full)} | co tile o train: {len(trn)}")
json.dump(res, open(out,'w'), indent=1); print("\nwrote", out)
