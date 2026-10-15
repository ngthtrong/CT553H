"""(a) Đối chứng offset và (b) bậc thang 2x2 {cùng/khác cụm} x {cùng/khác assay}.

(a) 28-mer của GPS là chuỗi con của 30-mer Voutsinos ⇒ tile mang thêm tới 2 residue ngữ cảnh.
    Nếu ngữ cảnh là nguyên nhân của khoảng cách qua assay thì khoảng cách phải đổi theo offset.

(b) Mô phỏng thủ thuật của arXiv 2605.11764: giữ nguyên *định danh* rồi chỉ đổi một thứ.
    Ở đây giữ nguyên **trình tự, cụm protein và mô hình**, chỉ đổi **nguồn nhãn** ⇒ cô lập dịch chuyển assay.

Chạy:  .venv/bin/python3 -I topics/degron-footprint/research/reframe-options-2026-10-15/cascade_and_offset.py
Chỉ đọc; không ghi gì vào data/.
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
SEED = 20261015


def fnum(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    def rk(v):
        o = v.argsort(kind="mergesort"); r = np.empty(len(v)); r[o] = np.arange(len(v))
        # hang trung binh cho dong hang
        s = v[o]; i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and s[j + 1] == s[i]:
                j += 1
            if j > i:
                r[o[i:j + 1]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y)
    a -= a.mean(); b -= b.mean()
    d = math.sqrt((a @ a) * (b @ b))
    return float(a @ b / d) if d else float("nan")


def auroc(score, label):
    score = np.asarray(score, float); label = np.asarray(label, int)
    pos, neg = int(label.sum()), int((1 - label).sum())
    if pos == 0 or neg == 0:
        return float("nan")
    o = score.argsort(kind="mergesort"); s = score[o]
    r = np.empty(len(s)); r[:] = np.arange(1, len(s) + 1)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[i:j + 1] = (i + j) / 2 + 1
        i = j + 1
    return float((r[label[o] == 1].sum() - pos * (pos + 1) / 2) / (pos * neg))


def onehot(seqs):
    X = np.zeros((len(seqs), L * NA + NA + 1), dtype=np.float32)
    for n, s in enumerate(seqs):
        for p, c in enumerate(s):
            k = AIDX.get(c)
            if k is not None:
                X[n, p * NA + k] = 1.0
                X[n, L * NA + k] += 1.0
    X[:, -1] = 1.0
    return X


def comp_only(X):
    """chi giu thanh phan + bias (bo kenh theo vi tri)."""
    Y = X.copy(); Y[:, :L * NA] = 0.0
    return Y


def ridge_fit(X, y, lam):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d, dtype=np.float64)
    A[-1, -1] -= lam                      # khong phat bias
    return np.linalg.solve(A, X.T @ y)


# ---------------- nap du lieu ----------------
print("nap GPS ...", flush=True)
gps = {}
with open(GPS, newline="", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("AA.Seq") or "").strip().upper()
        if len(aa) != L or any(c not in AIDX for c in aa):
            continue
        psi = fnum(row.get("Observed.PSI"))
        if psi is None:
            continue
        gps[aa] = (psi, (row.get("Gene") or "").split("_")[0])
print(f"GPS: {len(gps):,} peptide 28-mer sach", flush=True)

print("nap tile ...", flush=True)
tmatch = {}          # aa28 -> list[(degron_score, offset)]
with gzip.open(TILE, "rt", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("aa") or "").strip().upper()
        d = fnum(row.get("degron_score"))
        if d is None or len(aa) < L:
            continue
        for off in range(len(aa) - L + 1):
            tmatch.setdefault(aa[off:off + L], []).append((d, off))

clu = {}
with open(CLUST, newline="", encoding="utf-8") as fh:
    for line in fh:
        p = line.split()
        if len(p) == 2:
            clu[p[1]] = p[0]

matched = sorted(set(gps) & set(tmatch))
print(f"\n=== trinh tu dung chung: {len(matched):,} ===")

# ===================== (a) DOI CHUNG OFFSET =====================
print("\n" + "=" * 70)
print("(a) DOI CHUNG OFFSET  —  ngu canh 2 residue co phai nguyen nhan?")
print("=" * 70)
uniq = [s for s in matched if len(tmatch[s]) == 1]
print(f"trinh tu khop DUNG MOT tile: {len(uniq):,} / {len(matched):,}"
      f"  (khop nhieu tile: {len(matched)-len(uniq):,})")

print(f"\n{'offset':>8} {'n':>8} {'|Pearson|':>10} {'|Spearman|':>11} {'AUROC':>8}")
print("-" * 50)
rows = []
for off in (0, 1, 2):
    sub = [s for s in uniq if tmatch[s][0][1] == off]
    if len(sub) < 200:
        print(f"{off:>8} {len(sub):>8}   (qua it)")
        continue
    a = np.array([gps[s][0] for s in sub])
    b = np.array([tmatch[s][0][0] for s in sub])
    lab = (a <= 3.0).astype(int)
    pr = abs(float(np.corrcoef(a, b)[0, 1]))
    sp = abs(spearman(a, b))
    au = auroc(b, lab)
    rows.append((off, len(sub), pr, sp, au))
    print(f"{off:>8} {len(sub):>8} {pr:>10.4f} {sp:>11.4f} {au:>8.4f}")

if len(rows) >= 2:
    print(f"\nbien thien theo offset: |Pearson| {max(r[2] for r in rows)-min(r[2] for r in rows):.4f}"
          f" · AUROC {max(r[4] for r in rows)-min(r[4] for r in rows):.4f}")
    print("=> Neu bien thien nay NHO so voi khoang cach 0.0773 thi ngu canh 2 residue"
          " KHONG phai nguyen nhan chinh.")

# ===================== (b) BAC THANG 2x2 =====================
print("\n" + "=" * 70)
print("(b) BAC THANG 2x2  —  {cung/khac cum protein} x {cung/khac assay}")
print("=" * 70)

seq_clu = {s: clu.get(gps[s][1], gps[s][1]) for s in matched}
clusters = sorted(set(seq_clu.values()))
med_b = float(np.median([tmatch[s][0][0] for s in matched]))
print(f"cum cov80 trong phan giao: {len(clusters):,}")
print("QUAN TRONG: o 'cung cum' dung peptide GIU LAI khoi huan luyen (ngoai mau),"
      " nen ca hai o deu la ngoai mau.\n")

NSEED = 5
acc = {k: [] for k in (("full", "cung"), ("full", "khac"), ("comp", "cung"), ("comp", "khac"))}
for rep in range(NSEED):
    rng = np.random.default_rng(SEED + rep)
    perm = rng.permutation(len(clusters))
    test_cl = {clusters[i] for i in perm[:len(clusters) // 2]}
    train_cl = {clusters[i] for i in perm[len(clusters) // 2:]}

    m_tr = [s for s in matched if seq_clu[s] in train_cl]
    m_te = [s for s in matched if seq_clu[s] in test_cl]
    # giu lai mot nua peptide khop trong cum train -> o "cung cum" ngoai mau
    rng.shuffle(m_tr)
    held = set(m_tr[:len(m_tr) // 2])
    tr_seqs = [s for s, (psi, a_) in gps.items()
               if clu.get(a_, a_) in train_cl and s not in held]
    ytr = np.array([gps[s][0] for s in tr_seqs], dtype=np.float64)
    Xtr_full = onehot(tr_seqs).astype(np.float64)
    Xtr_comp = comp_only(onehot(tr_seqs)).astype(np.float64)

    for tag, Xt in (("full", Xtr_full), ("comp", Xtr_comp)):
        w = ridge_fit(Xt, ytr, lam=10.0)
        for cl_name, subset in (("cung", sorted(held)), ("khac", m_te)):
            Xs = onehot(subset)
            Xs = (Xs if tag == "full" else comp_only(Xs)).astype(np.float64)
            pred = Xs @ w
            a = np.array([gps[s][0] for s in subset])
            b = np.array([tmatch[s][0][0] for s in subset])
            acc[(tag, cl_name)].append((
                abs(spearman(pred, a)), abs(spearman(pred, b)),
                auroc(-pred, (a <= 3.0).astype(int)),
                auroc(-pred, (b > med_b).astype(int)), len(subset)))
    print(f"  seed {rep+1}/{NSEED} xong (train {len(tr_seqs):,} · cung-cum {len(held):,}"
          f" · khac-cum {len(m_te):,})", flush=True)

NAME = {"full": "day du (vi tri + thanh phan)", "comp": "chi thanh phan"}
print(f"\n{'mo hinh':<30} {'cum':<6} {'n':>7} {'rho vs A':>16} {'rho vs B':>16} {'AUROC A':>15}")
print("-" * 95)
mean = {}
for k, v in acc.items():
    arr = np.array([r[:4] for r in v])
    mu, sd = arr.mean(0), arr.std(0, ddof=1)
    mean[k] = mu
    print(f"{NAME[k[0]]:<30} {k[1]:<6} {v[0][4]:>7} "
          f"{mu[0]:>9.4f}±{sd[0]:.4f} {mu[1]:>9.4f}±{sd[1]:.4f} {mu[2]:>8.4f}±{sd[2]:.4f}")

print(f"\n--- Phan ra (trung binh {NSEED} seed, moi hieu so chi doi MOT thu) ---")
for tag in ("full", "comp"):
    ra_tr, rb_tr = mean[(tag, "cung")][0], mean[(tag, "cung")][1]
    ra_te, rb_te = mean[(tag, "khac")][0], mean[(tag, "khac")][1]
    a_tr, a_te = mean[(tag, "cung")][2], mean[(tag, "khac")][2]
    print(f"\n[{NAME[tag]}]  (Spearman)")
    print(f"  dich chuyen CUM   (cung assay A): {ra_tr:.4f} -> {ra_te:.4f}   hieu {ra_tr-ra_te:+.4f}")
    print(f"  dich chuyen ASSAY (cung cum)    : {ra_tr:.4f} -> {rb_tr:.4f}   hieu {ra_tr-rb_tr:+.4f}")
    print(f"  CA HAI                          : {ra_tr:.4f} -> {rb_te:.4f}   hieu {ra_tr-rb_te:+.4f}")
    print(f"  ty le ASSAY / CUM               : {abs(ra_tr-rb_tr)/max(abs(ra_tr-ra_te),1e-4):.0f}x")
    print(f"  (AUROC vs A: cung cum {a_tr:.4f} -> khac cum {a_te:.4f}, hieu {a_tr-a_te:+.4f})")

print("\n--- Gia tri cua kenh theo vi tri (chi so LeBlanc 'thanh phan vs vi tri') ---")
for cl_name in ("cung", "khac"):
    d = mean[("full", cl_name)][0] - mean[("comp", cl_name)][0]
    print(f"  {cl_name:<5} cum: rho day du - rho chi-thanh-phan = {d:+.4f}")
