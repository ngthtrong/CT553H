import csv, gzip, sys, json, time
from collections import defaultdict
import parasail

seqfile, train_gz, holdout_txt, out = sys.argv[1:5]

CODON = {}
bases='TCAG'
aas='FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
i=0
for b1 in bases:
    for b2 in bases:
        for b3 in bases:
            CODON[b1+b2+b3]=aas[i]; i+=1
def translate(dna):
    p=[]
    for i in range(0,len(dna)-2,3):
        a=CODON.get(dna[i:i+3].upper(),'X')
        if a=='*': break
        p.append(a)
    return ''.join(p)

prot={}
with gzip.open(seqfile,'rt') as fh:
    for line in fh:
        parts=line.rstrip('\n').split('\t')
        if len(parts)<2: parts=line.rstrip('\n').split()
        if len(parts)<2: continue
        ensg=parts[0].split('|')[0]
        p=translate(parts[-1])
        if len(p)>len(prot.get(ensg,'')): prot[ensg]=p   # giu transcript dai nhat
print(f"protein dich duoc: {len(prot)} gene, do dai trung vi ~{sorted(len(v) for v in prot.values())[len(prot)//2]}")

train_genes={r['name'].split('_tile')[0] for r in csv.DictReader(gzip.open(train_gz,'rt')) if '_tile' in r['name']}
hold={l.strip() for l in open(holdout_txt) if l.strip()}
eff=[g for g in hold if g not in train_genes]
tr=[g for g in train_genes if g in prot]
eff=[g for g in eff if g in prot]
print(f"holdout hieu dung co protein: {len(eff)} | train co protein: {len(tr)}")

# --- sang loc bang 6-mer
K=6
idx=defaultdict(set)
for g in tr:
    s=prot[g]
    for i in range(len(s)-K+1): idx[s[i:i+K]].add(g)
print(f"so 6-mer trong index: {len(idx)}")

t0=time.time()
cands={}
for g in eff:
    s=prot[g]; cnt=defaultdict(int)
    for i in range(len(s)-K+1):
        for h in idx.get(s[i:i+K],()): cnt[h]+=1
    top=sorted(cnt.items(), key=lambda x:-x[1])[:25]
    cands[g]=[h for h,c in top if c>=3]
n_pairs=sum(len(v) for v in cands.values())
print(f"sang loc 6-mer xong trong {time.time()-t0:.0f}s -> {n_pairs} cap ung vien can align")

# --- Smith-Waterman tren ung vien
mat=parasail.blosum62
t0=time.time(); results=[]
for g,hs in cands.items():
    a=prot[g]
    for h in hs:
        b=prot[h]
        r=parasail.sw_trace_striped_16(a,b,11,1,mat)
        tr_=r.traceback
        alen=len(tr_.comp) if tr_ else 0
        nid=sum(1 for c in tr_.comp if c=='|') if tr_ else 0
        if alen>0:
            # identity tren vung align, va coverage tren chuoi holdout
            pid=100.0*nid/alen
            cov=100.0*alen/len(a)
            results.append((g,h,round(pid,1),round(cov,1),alen,nid))
print(f"align xong {len(results)} cap trong {time.time()-t0:.0f}s")

results.sort(key=lambda x:-x[2])
print("\n== cap co identity cao nhat (holdout vs train) ==")
print(f"{'holdout':18} {'train':18} {'%id':>6} {'%cov':>6} {'alen':>6}")
for r in results[:15]: print(f"{r[0]:18} {r[1]:18} {r[2]:6} {r[3]:6} {r[4]:6}")

def worst(th_id, th_cov):
    hit={r[0] for r in results if r[2]>=th_id and r[3]>=th_cov}
    return len(hit)
print()
summary={}
for ti,tc in [(30,50),(40,50),(50,50),(60,50),(25,80),(30,80),(40,30),(60,30),(90,10)]:
    n=worst(ti,tc); summary[f"id>={ti}_cov>={tc}"]=n
    print(f"  gene holdout co ho hang trong train voi identity>={ti}% va coverage>={tc}%: {n}/{len(eff)} ({100*n/len(eff):.1f}%)")
mx=max((r[2] for r in results), default=0)
print(f"\nidentity cao nhat quan sat duoc giua holdout va train: {mx}%")
json.dump({"n_eff_holdout":len(eff),"n_train":len(tr),"n_pairs_aligned":len(results),
  "max_identity_pct":mx,"thresholds":summary,
  "top_pairs":[{"holdout":r[0],"train":r[1],"pct_id":r[2],"pct_cov_of_holdout":r[3],"aln_len":r[4]} for r in results[:25]]},
  open(out,'w'), indent=1)
print("wrote", out)
