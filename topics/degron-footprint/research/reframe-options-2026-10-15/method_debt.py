"""Dọn hai món nợ phương pháp trước khi chốt các đề xuất C.

NỢ 1 — Phát hiện 2 ("split cụm cov80 không mua được gì") có thật, hay chỉ là tạo tác của
        ridge tuyến tính quá đơn giản để ghi nhớ định danh protein?
        Kiểm bằng BA mô hình có khả năng khai thác đồng dạng tăng dần:
          (1) ridge tuyến tính          — đã đo ở cascade_and_offset.py
          (2) gradient boosting         — mô hình mạnh, phi tuyến
          (3) 1-NN theo đồng nhất vị trí — khai thác đồng dạng TỐI ĐA ⇒ chặn trên của hiệu ứng cụm
        Nếu cả (3) cũng không thấy hiệu ứng cụm thì Phát hiện 2 vững.

NỢ 2 — Rủi ro LeBlanc: trọng số THEO VỊ TRÍ có tái lập được không, hay chỉ tổng theo
        acid amin mới tái lập? Bootstrap theo khuôn LeBlanc, đo tái lập nửa-nửa.

Chạy:  .venv/bin/python3 -I topics/degron-footprint/research/reframe-options-2026-10-15/method_debt.py
Chỉ đọc; không ghi gì vào data/.
"""
import csv, gzip, math, sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT = Path(__file__).resolve()
while not (ROOT / "CLAUDE.md").exists():
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
SEED = 20261015
NSEED = 3
NBOOT = 40


def fnum(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def rankdata(v):
    v = np.asarray(v, float)
    o = v.argsort(kind="mergesort")
    r = np.empty(len(v))
    r[o] = np.arange(len(v), dtype=float)
    s = v[o]
    i = 0
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
    """[0:560] kenh theo vi tri · [560:580] thanh phan · [580] bias"""
    X = np.zeros((len(seqs), L * NA + NA + 1), dtype=np.float32)
    for n, s in enumerate(seqs):
        for p, c in enumerate(s):
            k = AIDX.get(c)
            if k is not None:
                X[n, p * NA + k] = 1.0
                X[n, L * NA + k] += 1.0
    X[:, -1] = 1.0
    return X


def ridge_fit(X, y, lam=10.0):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d)
    A[-1, -1] -= lam
    return np.linalg.solve(A, X.T @ y)


def nn1_predict(Xte_pos, Xtr_pos, ytr, chunk=512):
    """1-NN theo so vi tri trung khop (tich vo huong cua one-hot vi tri)."""
    out = np.empty(len(Xte_pos))
    for i in range(0, len(Xte_pos), chunk):
        sim = Xte_pos[i:i + chunk] @ Xtr_pos.T           # = so (vi tri, aa) trung khop
        out[i:i + chunk] = ytr[np.asarray(sim.argmax(1)).ravel()]
    return out


# ---------------- nap du lieu ----------------
print("nap GPS ...", flush=True)
gps = {}
with open(GPS, newline="", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("AA.Seq") or "").strip().upper()
        if len(aa) != L or any(c not in AIDX for c in aa):
            continue
        psi = fnum(row.get("Observed.PSI"))
        if psi is not None:
            gps[aa] = (psi, (row.get("Gene") or "").split("_")[0])

print("nap tile ...", flush=True)
tscore = {}
with gzip.open(TILE, "rt", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("aa") or "").strip().upper()
        d = fnum(row.get("degron_score"))
        if d is None or len(aa) < L:
            continue
        for off in range(len(aa) - L + 1):
            tscore.setdefault(aa[off:off + L], d)

clu = {}
with open(CLUST, newline="", encoding="utf-8") as fh:
    for line in fh:
        p = line.split()
        if len(p) == 2:
            clu[p[1]] = p[0]

matched = sorted(set(gps) & set(tscore))
seq_clu = {s: clu.get(gps[s][1], gps[s][1]) for s in matched}
clusters = sorted(set(seq_clu.values()))
print(f"GPS {len(gps):,} · trinh tu dung chung {len(matched):,} · cum {len(clusters):,}\n")

# ===================== NO 1 =====================
print("=" * 78)
print("NO 1 — Phat hien 2 co phai tao tac cua ridge tuyen tinh?")
print("=" * 78)
res = {}
for rep in range(NSEED):
    rng = np.random.default_rng(SEED + rep)
    perm = rng.permutation(len(clusters))
    test_cl = {clusters[i] for i in perm[:len(clusters) // 2]}
    train_cl = {clusters[i] for i in perm[len(clusters) // 2:]}
    m_tr = [s for s in matched if seq_clu[s] in train_cl]
    m_te = [s for s in matched if seq_clu[s] in test_cl]
    rng.shuffle(m_tr)
    held = sorted(m_tr[:len(m_tr) // 2])
    tr = [s for s, (p_, a_) in gps.items()
          if clu.get(a_, a_) in train_cl and s not in set(held)]
    ytr = np.array([gps[s][0] for s in tr])
    Xtr, Xh, Xt = feats(tr), feats(held), feats(m_te)

    preds = {}
    w = ridge_fit(Xtr.astype(np.float64), ytr)
    preds["ridge"] = (Xh.astype(np.float64) @ w, Xt.astype(np.float64) @ w)

    gb = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.1,
                                       max_leaf_nodes=63, random_state=SEED + rep)
    gb.fit(Xtr[:, :-1], ytr)
    preds["gboost"] = (gb.predict(Xh[:, :-1]), gb.predict(Xt[:, :-1]))

    preds["1nn-dongdang"] = (nn1_predict(Xh[:, :L * NA], Xtr[:, :L * NA], ytr),
                             nn1_predict(Xt[:, :L * NA], Xtr[:, :L * NA], ytr))

    for mname, (ph, pt) in preds.items():
        a_h = np.array([gps[s][0] for s in held]); b_h = np.array([tscore[s] for s in held])
        a_t = np.array([gps[s][0] for s in m_te])
        res.setdefault(mname, []).append((
            abs(spearman(ph, a_h)),     # cung cum, assay A
            abs(spearman(pt, a_t)),     # khac cum, assay A
            abs(spearman(ph, b_h))))    # cung cum, assay B
    print(f"  seed {rep+1}/{NSEED} xong (train {len(tr):,})", flush=True)

print(f"\n{'mo hinh':<16} {'rho cung cum':>14} {'rho khac cum':>14} "
      f"{'dich CUM':>12} {'dich ASSAY':>12} {'ty le':>7}")
print("-" * 80)
for mname, v in res.items():
    arr = np.array(v); mu, sd = arr.mean(0), arr.std(0, ddof=1)
    d_cl, d_as = mu[0] - mu[1], mu[0] - mu[2]
    print(f"{mname:<16} {mu[0]:>8.4f}±{sd[0]:.4f} {mu[1]:>8.4f}±{sd[1]:.4f} "
          f"{d_cl:>+12.4f} {d_as:>+12.4f} {abs(d_as)/max(abs(d_cl),1e-4):>6.0f}x")

print("\n=> Doc: neu '1nn-dongdang' (khai thac dong dang toi da) co 'dich CUM' LON")
print("   thi split cum CO tac dung va Phat hien 2 chi dung cho mo hinh yeu.")

# ===================== NO 2 =====================
print("\n" + "=" * 78)
print(f"NO 2 — Trong so THEO VI TRI co tai lap? (bootstrap x{NBOOT}, khuon LeBlanc)")
print("=" * 78)
rng = np.random.default_rng(SEED)
perm = rng.permutation(len(clusters))
train_cl = {clusters[i] for i in perm[len(clusters) // 2:]}
tr = [s for s, (p_, a_) in gps.items() if clu.get(a_, a_) in train_cl]
ytr = np.array([gps[s][0] for s in tr]); Xtr = feats(tr).astype(np.float64)
print(f"tap bootstrap: {len(tr):,} peptide")

W = np.empty((NBOOT, Xtr.shape[1]))
for b in range(NBOOT):
    idx = rng.integers(0, len(tr), len(tr))
    W[b] = ridge_fit(Xtr[idx], ytr[idx])
    if (b + 1) % 10 == 0:
        print(f"  bootstrap {b+1}/{NBOOT}", flush=True)

pos = W[:, :L * NA]                                  # 560 o (vi tri, aa)
comp = W[:, L * NA:L * NA + NA]                      # 20 thanh phan
pos_agg = pos.reshape(NBOOT, L, NA).sum(axis=1)      # tong theo aa, gop 28 vi tri

print("\n--- Tai lap nua-nua (Spearman giua trung binh hai nua bootstrap) ---")
h = NBOOT // 2
for nm, M in (("o (vi tri, aa)  560 chieu", pos),
              ("tong theo aa     20 chieu", pos_agg),
              ("kenh thanh phan  20 chieu", comp)):
    print(f"  {nm:<28} {spearman(M[:h].mean(0), M[h:].mean(0)):+.4f}")

print("\n--- On dinh tung he so: |trung binh| / SD ---")
for nm, M in (("o (vi tri, aa)", pos), ("tong theo aa", pos_agg), ("thanh phan", comp)):
    r = np.abs(M.mean(0)) / (M.std(0, ddof=1) + 1e-12)
    sign = np.mean(np.abs(np.sign(M).mean(0)))
    print(f"  {nm:<16} trung vi {np.median(r):>7.2f} · "
          f"ty le he so co |mu|/SD > 2: {np.mean(r > 2):.3f} · dong thuan dau {sign:.3f}")

print("\n=> Doc: neu 'tong theo aa' tai lap cao ma 'o (vi tri, aa)' tai lap thap")
print("   thi 'thanh phan > vi tri' DUNG o muc tham so, va rui ro LeBlanc la that.")
