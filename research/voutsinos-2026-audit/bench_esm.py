import time, sys, gzip, csv, json
import numpy as np, torch
from transformers import AutoTokenizer, AutoModel
torch.set_num_threads(12)
full_gz, out = sys.argv[1:3]
seqs=[]
with gzip.open(full_gz,'rt') as fh:
    for r in csv.DictReader(fh):
        if '_tile' in r['name'] and len(r['aa'])==30: seqs.append(r['aa'].upper())
        if len(seqs)>=1024: break
N_TOTAL=212658
res={}
for mid, label in [("facebook/esm2_t12_35M_UR50D","ESM-2 35M"),("facebook/esm2_t33_650M_UR50D","ESM-2 650M")]:
    try:
        t0=time.time(); tok=AutoTokenizer.from_pretrained(mid); mdl=AutoModel.from_pretrained(mid); mdl.eval()
        tload=time.time()-t0
        npar=sum(p.numel() for p in mdl.parameters())
        with torch.no_grad():
            b=torch.tensor(tok(seqs[:16],padding=True)['input_ids']); mdl(b)   # warmup
            for bs in [32,128]:
                n=min(512,len(seqs)); t0=time.time(); done=0
                for i in range(0,n,bs):
                    chunk=seqs[i:i+bs]
                    enc=tok(chunk,padding=True,return_tensors='pt')
                    o=mdl(**enc).last_hidden_state
                    done+=len(chunk)
                dt=time.time()-t0; rate=done/dt
                est=N_TOTAL/rate
                print(f"{label:12} params={npar/1e6:6.1f}M  batch={bs:4}  {rate:7.1f} tile/s  "
                      f"-> 212.658 tile trong {est/60:6.1f} phut  (hidden={o.shape[-1]})")
                res[f"{label}_bs{bs}"]={"params_M":round(npar/1e6,1),"tiles_per_sec":round(rate,1),
                    "minutes_for_212658":round(est/60,1),"hidden_dim":int(o.shape[-1]),"load_sec":round(tload,1)}
        del mdl
    except Exception as e:
        print(f"{label}: THAT BAI -> {type(e).__name__}: {str(e)[:150]}")
        res[label]={"error":f"{type(e).__name__}: {str(e)[:200]}"}
# kich co cache embedding
for d,lab in [(480,'35M'),(1280,'650M')]:
    gb=N_TOTAL*30*d*4/1e9
    print(f"Cache embedding mUc residue, {lab} (dim {d}): {gb:.1f} GB fp32 / {gb/2:.1f} GB fp16")
    res[f"cache_{lab}_GB_fp32"]=round(gb,1)
json.dump(res,open(out,'w'),indent=1); print("\nwrote",out)
