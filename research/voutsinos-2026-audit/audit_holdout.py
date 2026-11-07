import csv, gzip, sys, json
from collections import Counter, defaultdict
train_gz, clust_tsv, holdout_txt, out = sys.argv[1:5]

train_genes=set()
with gzip.open(train_gz,'rt') as fh:
    for r in csv.DictReader(fh): train_genes.add(r['name'].split('_tile')[0])
hold=[l.strip() for l in open(holdout_txt) if l.strip()]
hold_genes=set(hold)
print(f"train genes={len(train_genes)}  holdout genes={len(hold_genes)} (file lines={len(hold)})")

g2c={}; members=defaultdict(set)
with open(clust_tsv) as fh:
    for line in fh:
        p=line.rstrip('\n').split('\t')
        if len(p)>=2: g2c[p[1]]=p[0]; members[p[0]].add(p[1])

print("DIRECT gene overlap train∩holdout:", len(train_genes & hold_genes))
tc={g2c[g] for g in train_genes if g in g2c}
hc={g2c[g] for g in hold_genes if g in g2c}
print(f"train genes mapped to clusters: {len([g for g in train_genes if g in g2c])}/{len(train_genes)}")
print(f"holdout genes mapped to clusters: {len([g for g in hold_genes if g in g2c])}/{len(hold_genes)}")
shared=tc & hc
print(f"clusters in train: {len(tc)} | clusters in holdout: {len(hc)} | SHARED CLUSTERS: {len(shared)}")

leaky_hold=[g for g in hold_genes if g in g2c and g2c[g] in tc]
print(f"HOLDOUT genes whose homology cluster also contains a TRAIN gene: {len(leaky_hold)}/{len(hold_genes)} = {len(leaky_hold)/len(hold_genes):.1%}")
ex=[]
for g in sorted(leaky_hold)[:10]:
    rep=g2c[g]; sibs=sorted(members[rep]&train_genes)[:4]
    ex.append({"holdout_gene":g,"cluster_rep":rep,"cluster_size":len(members[rep]),"train_siblings":sibs})
for e in ex: print("  ", e)
res={"train_genes":len(train_genes),"holdout_genes":len(hold_genes),
     "direct_gene_overlap":len(train_genes&hold_genes),
     "clusters_train":len(tc),"clusters_holdout":len(hc),"shared_clusters":len(shared),
     "holdout_genes_with_train_homolog":len(leaky_hold),
     "holdout_leak_fraction":round(len(leaky_hold)/len(hold_genes),4),"examples":ex}
json.dump(res,open(out,'w'),indent=1); print("\nwrote",out)
