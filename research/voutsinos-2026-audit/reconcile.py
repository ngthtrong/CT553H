import csv, gzip, sys, json, hashlib
from collections import defaultdict, Counter
full_gz, train_gz, holdout_txt, out = sys.argv[1:5]
print("sha256 degrons.csv.gz =", hashlib.sha256(open(full_gz,'rb').read()).hexdigest()[:32])

def gene(n): return n.split('_tile')[0]
full={}; gfull=defaultdict(int)
with gzip.open(full_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        full[r['name']]=r; gfull[gene(r['name'])]+=1
print(f"FULL table: tiles={len(full)} genes={len(gfull)}")

tr=set(); gtr=defaultdict(int)
with gzip.open(train_gz,'rt') as fh:
    for r in csv.DictReader(fh): tr.add(r['name']); gtr[gene(r['name'])]+=1
print(f"TRAIN file: tiles={len(tr)} genes={len(gtr)}")

hold={l.strip() for l in open(holdout_txt) if l.strip()}
not_train=set(full)-tr
print(f"tiles in FULL but not in TRAIN: {len(not_train)}  (= candidate holdout tiles)")
gnt=Counter(gene(n) for n in not_train)
print(f"genes covered by those tiles: {len(gnt)}")
print(f"  of which in holdout_selection.txt: {len(set(gnt)&hold)}")
print(f"  NOT in holdout_selection.txt: {len(set(gnt)-hold)}")

# the 99 genes: are they split tile-wise between train and holdout?
both=[g for g in hold if g in gtr]
print(f"\nholdout genes that ALSO have train tiles: {len(both)}")
rows=[]
for g in sorted(both)[:12]:
    rows.append({"gene":g,"tiles_total":gfull[g],"tiles_in_train":gtr[g],"tiles_held_out":gfull[g]-gtr[g]})
for r in rows: print("  ",r)
fully = sum(1 for g in both if gtr[g]==gfull[g])
part  = sum(1 for g in both if 0<gtr[g]<gfull[g])
print(f"  -> ALL tiles in train (gene not actually held out): {fully}")
print(f"  -> partially held out: {part}")

hold_eff=[g for g in hold if g not in gtr]
print(f"\nholdout genes with NO train tiles (effective holdout): {len(hold_eff)}")
ht=sum(gfull[g] for g in hold_eff)
print(f"  tiles in effective holdout: {ht}")
res={"full_tiles":len(full),"full_genes":len(gfull),"train_tiles":len(tr),"train_genes":len(gtr),
 "tiles_not_in_train":len(not_train),"genes_not_in_train":len(gnt),
 "holdout_list":len(hold),"holdout_genes_with_train_tiles":len(both),
 "holdout_fully_in_train":fully,"holdout_partially":part,
 "effective_holdout_genes":len(hold_eff),"effective_holdout_tiles":ht,"examples":rows}
json.dump(res,open(out,'w'),indent=1); print("\nwrote",out)
