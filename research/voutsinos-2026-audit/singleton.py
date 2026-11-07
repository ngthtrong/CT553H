import sys
from collections import defaultdict
clust_tsv, holdout_txt = sys.argv[1:3]
members=defaultdict(set); g2c={}
for line in open(clust_tsv):
    p=line.rstrip('\n').split('\t')
    if len(p)>=2: g2c[p[1]]=p[0]; members[p[0]].add(p[1])
hold=[l.strip() for l in open(holdout_txt) if l.strip()]
sizes=[len(members[g2c[g]]) for g in hold if g in g2c]
from collections import Counter
print("holdout cluster-size distribution:", dict(sorted(Counter(sizes).items())))
print("holdout genes in singleton clusters:", sum(1 for s in sizes if s==1), "/", len(sizes))
allsz=Counter(len(v) for v in members.values())
print("ALL clusters size distribution (top):", dict(sorted(allsz.items())[:8]))
tot=sum(k*v for k,v in allsz.items())
print("total genes in cluster map:", tot, "| singleton clusters:", allsz.get(1,0), "| non-singleton:", sum(v for k,v in allsz.items() if k>1))
