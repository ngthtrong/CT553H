"""Lần thử G2 thật đầu tiên: chuyển giao qua assay có giúp được gì không?

Câu hỏi quyết định hướng đóng góp ([D-030](../../../../DECISIONS.md#d-030) mục 1):
  mô hình dùng NHÃN GPS có đánh bại mô hình chỉ dùng nhãn tile, trên chính nhiệm vụ tile?
Nếu CÓ  -> "chuyển giao qua assay" là đóng góp dương đo được, và kiến trúc có việc rõ ràng.
Nếu KHÔNG -> khoảng cách 0,1061 là hàng rào chứ không phải cơ hội; phải đổi hướng.

Ba mô hình, cùng đặc trưng, cùng ngân sách, cùng split cụm cov80, 5 seed:
  (A) chi-GPS     — huan luyen tren PSI cua GPS (nhieu du lieu, sai assay)
  (B) chi-tile    — huan luyen tren degron_score cua tile (it du lieu, dung assay)
  (C) ghep-2-dau  — bieu dien dung chung + MOT dau rieng cho moi assay  <- de xuat kien truc
  (D) B + dac trung tu A — dung du doan cua (A) lam mot dac trung cho (B)  <- stacking

Danh gia: tat ca cham tren nhan TILE o cum TEST. Tran nhieu cua tile = 0,9903.

Chay: .venv/bin/python3 -I topics/degron-footprint/research/cross-assay-model-2026-10-15/transfer_experiment.py
Chi doc; khong ghi gi vao data/.
"""
import csv, gzip, math, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve()
while not (ROOT / "DECISIONS.md").exists():
    if ROOT.parent == ROOT:
        sys.exit("khong tim thay goc repo")
    ROOT = ROOT.parent
DATA = ROOT / "topics/degron-footprint/data"
GPS = DATA / ("interim/zhang-gps-unzip/I28 Initial MLN4924 SVM (Completed)/"
              "Machine Learning Prediction of I28 Peptidome PSI (Complete Coverage & 10% Training).csv")
TILE = DATA / "raw/voutsinos-2026/repo/score/degrons.csv.gz"
CLUST = DATA / "interim/protein-id30-cov80_cluster.tsv"

csv.field_size_limit(10 ** 7)
AA = "ACDEFGHIKLMNPQRSTVWY"
AIDX = {c: i for i, c in enumerate(AA)}
L, NA = 28, 20
SEED, NSEED, LAM = 20261015, 5, 10.0
CEIL = 0.9903          # tran nhieu cua degron_score tile (probe_tile_reliability.py)


def fnum(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def rankdata(v):
    v = np.asarray(v, float)
    o = v.argsort(kind="mergesort")
    r = np.empty(len(v)); r[o] = np.arange(len(v), dtype=float)
    s = v[o]; i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[o[i:j + 1]] = (i + j) / 2
        i = j + 1
    return r


def spearman(x, y):
    a, b = rankdata(x), rankdata(y)
    a = a - a.mean(); b = b - b.mean()
    d = math.sqrt((a @ a) * (b @ b))
    return float(a @ b / d) if d else float("nan")


def feats(seqs):
    X = np.zeros((len(seqs), L * NA + NA + 1), dtype=np.float32)
    for n, s in enumerate(seqs):
        for p, c in enumerate(s):
            k = AIDX.get(c)
            if k is not None:
                X[n, p * NA + k] = 1.0
                X[n, L * NA + k] += 1.0
    X[:, -1] = 1.0
    return X


def ridge(X, y, lam=LAM):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d)
    A[-1, -1] -= lam
    return np.linalg.solve(A, X.T @ y)


def z(v):
    v = np.asarray(v, float)
    sd = v.std()
    return (v - v.mean()) / (sd if sd else 1.0)


# ---------------- nap ----------------
print("nap du lieu ...", flush=True)
gps = {}
with open(GPS, newline="", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("AA.Seq") or "").strip().upper()
        if len(aa) != L or any(c not in AIDX for c in aa):
            continue
        psi = fnum(row.get("Observed.PSI"))
        if psi is not None:
            gps[aa] = (psi, (row.get("Gene") or "").split("_")[0])

tile = {}
with gzip.open(TILE, "rt", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("aa") or "").strip().upper()
        d = fnum(row.get("degron_score"))
        if d is None or len(aa) < L:
            continue
        for off in range(len(aa) - L + 1):
            tile.setdefault(aa[off:off + L], d)

clu = {}
with open(CLUST, newline="", encoding="utf-8") as fh:
    for line in fh:
        p = line.split()
        if len(p) == 2:
            clu[p[1]] = p[0]

matched = sorted(set(gps) & set(tile))
seq_clu = {s: clu.get(gps[s][1], gps[s][1]) for s in matched}
clusters = sorted(set(seq_clu.values()))
print(f"GPS {len(gps):,} · trinh tu dung chung {len(matched):,} · cum {len(clusters):,}\n")

names = ["A chi-GPS", "B chi-tile", "C ghep-2-dau", "D stacking"]
out = {n: [] for n in names}

for rep in range(NSEED):
    rng = np.random.default_rng(SEED + rep)
    perm = rng.permutation(len(clusters))
    test_cl = {clusters[i] for i in perm[:len(clusters) // 2]}
    train_cl = {clusters[i] for i in perm[len(clusters) // 2:]}

    m_tr = [s for s in matched if seq_clu[s] in train_cl]     # co CA hai nhan
    m_te = [s for s in matched if seq_clu[s] in test_cl]
    g_tr = [s for s, (p_, a_) in gps.items()
            if clu.get(a_, a_) in train_cl and s not in set(m_te)]

    Xg, Xm, Xt = feats(g_tr).astype(np.float64), feats(m_tr).astype(np.float64), feats(m_te).astype(np.float64)
    yg = np.array([gps[s][0] for s in g_tr])                  # nhan assay A
    ym = np.array([tile[s] for s in m_tr])                    # nhan assay B
    yte = np.array([tile[s] for s in m_te])                   # su that (assay B)

    # (A) chi GPS
    wA = ridge(Xg, yg)
    pA_te, pA_tr = Xt @ wA, Xm @ wA
    out["A chi-GPS"].append(abs(spearman(pA_te, yte)))

    # (B) chi tile
    wB = ridge(Xm, ym)
    out["B chi-tile"].append(abs(spearman(Xt @ wB, yte)))

    # (C) bieu dien dung chung + mot dau rieng moi assay:
    #     hoc dong thoi tren hai nhan da chuan hoa, roi tinh chinh dau cho assay B
    Xboth = np.vstack([Xg, Xm])
    yboth = np.concatenate([z(yg) * -1.0, z(ym)])   # dao dau GPS: PSI cao = BEN = nguoc degron
    wSh = ridge(Xboth, yboth)
    # dau rieng cho assay B: hoi quy nhan B that len (dac trung dung chung + du doan chung)
    hSh_tr, hSh_te = Xm @ wSh, Xt @ wSh
    Hb_tr = np.column_stack([hSh_tr, Xm[:, L * NA:]])         # du doan chung + thanh phan
    Hb_te = np.column_stack([hSh_te, Xt[:, L * NA:]])
    wHead = ridge(Hb_tr, ym, lam=1.0)
    out["C ghep-2-dau"].append(abs(spearman(Hb_te @ wHead, yte)))

    # (D) stacking: du doan cua (A) lam MOT dac trung cho mo hinh tren nhan B
    Ds_tr = np.column_stack([pA_tr, Xm])
    Ds_te = np.column_stack([pA_te, Xt])
    wD = ridge(Ds_tr, ym)
    out["D stacking"].append(abs(spearman(Ds_te @ wD, yte)))

    print(f"  seed {rep+1}/{NSEED} (GPS {len(g_tr):,} · tile-train {len(m_tr):,} · test {len(m_te):,})",
          flush=True)

print(f"\n{'mo hinh':<16} {'rho vs nhan TILE o cum TEST':>30} {'% cua tran':>12}")
print("-" * 62)
mu = {}
for n in names:
    a = np.array(out[n]); mu[n] = a.mean()
    print(f"{n:<16} {a.mean():>18.4f} ± {a.std(ddof=1):.4f} {a.mean()/CEIL:>11.1%}")
print(f"{'tran nhieu tile':<16} {CEIL:>18.4f}")

print("\n--- Phep so quyet dinh huong ---")
d_ct = mu["C ghep-2-dau"] - mu["B chi-tile"]
d_dt = mu["D stacking"] - mu["B chi-tile"]
d_ba = mu["B chi-tile"] - mu["A chi-GPS"]
print(f"  B chi-tile  -  A chi-GPS   = {d_ba:+.4f}   (dung assay co hon nhieu du lieu?)")
print(f"  C ghep-2-dau - B chi-tile  = {d_ct:+.4f}   <- CHUYEN GIAO co giup?")
print(f"  D stacking   - B chi-tile  = {d_dt:+.4f}   <- stacking co giup?")
best = max(names, key=lambda n: mu[n])
print(f"\n  tot nhat: {best} = {mu[best]:.4f}  (du dia con lai den tran: {CEIL-mu[best]:.4f})")
# kiem ghep cap tung seed cho hai phep so quan trong
for nm, other in (("C ghep-2-dau", "B chi-tile"), ("D stacking", "B chi-tile")):
    d = np.array(out[nm]) - np.array(out[other])
    print(f"  ghep cap {nm} vs {other}: trung binh {d.mean():+.4f}, "
          f"SD {d.std(ddof=1):.4f}, thang {int((d>0).sum())}/{NSEED} seed")
