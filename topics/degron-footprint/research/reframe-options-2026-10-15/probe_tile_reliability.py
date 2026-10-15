import gzip, csv, math, statistics as st
F="/home/ngthtrong/CT553H/topics/degron-footprint/data/raw/voutsinos-2026/repo/score/degrons.csv.gz"
ds=[];ab=[];dstd=[];astd=[];ns=[];genes=set()
with gzip.open(F,'rt') as fh:
    for r in csv.DictReader(fh):
        try:
            d=float(r['degron_score']);a=float(r['abundance_score'])
            sd=float(r['degron_std']);sa=float(r['abundance_std']);n=int(r['n'])
        except (ValueError,TypeError):
            continue
        if any(math.isnan(x) for x in (d,a,sd,sa)): continue
        ds.append(d);ab.append(a);dstd.append(sd);astd.append(sa);ns.append(n)
        genes.add(r['name'].split('_tile')[0])
print(f"tiles usable        : {len(ds):,}")
print(f"genes               : {len(genes):,}")
print(f"median obs per tile : {st.median(ns)}  (min {min(ns)}, max {max(ns)})")
print(f"degron_score  sd across tiles : {st.pstdev(ds):.4f}   median per-tile std : {st.median(dstd):.4f}")
print(f"abundance_sc  sd across tiles : {st.pstdev(ab):.4f}   median per-tile std : {st.median(astd):.4f}")
def pear(x,y):
    mx=sum(x)/len(x);my=sum(y)/len(y)
    sx=math.sqrt(sum((v-mx)**2 for v in x));sy=math.sqrt(sum((v-my)**2 for v in y))
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(sx*sy)
print(f"\nPearson(degron_score, abundance_score) = {pear(ds,ab):.4f}")
# reliability = signal variance / total variance, per Spearman-Brown style attenuation
for nm,v,sd in (("degron",ds,dstd),("abundance",ab,astd)):
    tot=st.pvariance(v); err=sum(s*s for s in sd)/len(sd)
    rel=max(0.0,(tot-err)/tot)
    print(f"{nm:9s}: total var {tot:.4f}  mean err var {err:.4f}  reliability {rel:.4f}  ceiling r = {math.sqrt(rel):.4f}")
