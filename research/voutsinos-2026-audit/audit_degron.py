import csv, gzip, sys, json, hashlib, statistics as st
from collections import Counter, defaultdict

train_gz, clust_tsv, holdout_txt, out_json = sys.argv[1:5]

print("sha256 degron_train.csv.gz =", hashlib.sha256(open(train_gz,'rb').read()).hexdigest()[:32])

rows=[]
with gzip.open(train_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        rows.append(r)
print("tiles total:", len(rows))

def gene(name): return name.split('_tile')[0]
sets = Counter(r['set'] for r in rows)
print("set counts:", dict(sets))

genes_by_set = defaultdict(set)
for r in rows: genes_by_set[r['set']].add(gene(r['name']))
for s,g in genes_by_set.items(): print(f"  genes in '{s}':", len(g))

ss = sorted(genes_by_set)
res = {"tiles_total": len(rows), "set_counts": dict(sets),
       "genes_per_set": {s: len(genes_by_set[s]) for s in ss}}

# 1) gene-level overlap between sets
for i in range(len(ss)):
    for j in range(i+1, len(ss)):
        ov = genes_by_set[ss[i]] & genes_by_set[ss[j]]
        print(f"GENE overlap {ss[i]} vs {ss[j]}: {len(ov)}")
        res[f"gene_overlap_{ss[i]}_{ss[j]}"] = len(ov)

# 2) homology-cluster overlap
g2c = {}
with open(clust_tsv) as fh:
    for line in fh:
        p = line.rstrip('\n').split('\t')
        if len(p) >= 2: g2c[p[1]] = p[0]          # member -> representative
print("cluster map entries:", len(g2c), "| distinct representatives:", len(set(g2c.values())))
res["cluster_map_entries"] = len(g2c); res["cluster_representatives"] = len(set(g2c.values()))
sizes = Counter(g2c.values())
multi = {k:v for k,v in sizes.items() if v>1}
print("clusters with >1 member:", len(multi), "| largest cluster:", max(sizes.values()) if sizes else 0)
res["clusters_multi_member"] = len(multi); res["largest_cluster"] = max(sizes.values()) if sizes else 0

clust_by_set = {s: {g2c.get(g, 'UNMAPPED:'+g) for g in genes_by_set[s]} for s in ss}
for i in range(len(ss)):
    for j in range(i+1, len(ss)):
        ov = clust_by_set[ss[i]] & clust_by_set[ss[j]]
        print(f"CLUSTER overlap {ss[i]} vs {ss[j]}: {len(ov)}  -> {sorted(ov)[:8]}")
        res[f"cluster_overlap_{ss[i]}_{ss[j]}"] = len(ov)
        res[f"cluster_overlap_examples_{ss[i]}_{ss[j]}"] = sorted(ov)[:20]
    unmapped = sum(1 for g in genes_by_set[ss[i]] if g not in g2c)
    print(f"  genes in '{ss[i]}' not in cluster map: {unmapped}")
    res[f"unmapped_genes_{ss[i]}"] = unmapped

# 3) sequence-level overlap: exact 30-mer and shared 15-mers across sets
if len(ss) >= 2:
    a, b = ss[0], ss[-1]
    seqa = {r['aa'].upper() for r in rows if r['set']==a}
    seqb = {r['aa'].upper() for r in rows if r['set']==b}
    exact = seqa & seqb
    print(f"EXACT 30-mer tile overlap {a} vs {b}: {len(exact)}")
    res[f"exact_tile_overlap_{a}_{b}"] = len(exact)
    K=15
    ka = set(); 
    for s_ in seqa:
        for p in range(len(s_)-K+1): ka.add(s_[p:p+K])
    hit=0; tot=0
    for r in rows:
        if r['set']!=b: continue
        s_=r['aa'].upper(); tot+=1
        if any(s_[p:p+K] in ka for p in range(len(s_)-K+1)): hit+=1
    print(f"{b} tiles sharing a {K}-mer with any {a} tile: {hit}/{tot} = {hit/tot:.1%}")
    res[f"kmer{K}_shared_{b}_vs_{a}"] = {"hit":hit,"total":tot,"frac":round(hit/tot,4)}

# 4) label distribution
for s in ss:
    v=[float(r['degron_score']) for r in rows if r['set']==s and r['degron_score'] not in ('','NA')]
    if v: print(f"degron_score '{s}': n={len(v)} mean={st.mean(v):.3f} sd={st.pstdev(v):.3f} min={min(v):.3f} max={max(v):.3f}")
    res[f"label_{s}"]={"n":len(v),"mean":round(st.mean(v),4) if v else None}

json.dump(res, open(out_json,'w'), indent=1)
print("\nwrote", out_json)
