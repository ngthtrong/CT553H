"""Đo khoảng cách qua assay giữa GPS (Zhang 2023) và tile sort-seq (Voutsinos 2026).

Mô phỏng "within-target cross-lab cascade" của arXiv 2605.11764: giữ nguyên *trình tự*
(tương đương "identical compounds") rồi đổi assay, để tách phương sai đo khỏi dịch chuyển miền.

Chạy:  .venv/bin/python3 -I topics/degron-footprint/research/reframe-options-2026-10-15/cross_assay_gap.py
Chỉ đọc; không ghi gì vào data/.
"""
import csv, gzip, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / "DECISIONS.md").exists():          # tìm gốc repo qua DECISIONS.md
    if ROOT.parent == ROOT:
        sys.exit("khong tim thay goc repo")
    ROOT = ROOT.parent
DATA = ROOT / "topics/degron-footprint/data"
GPS = DATA / ("interim/zhang-gps-unzip/I28 Initial MLN4924 SVM (Completed)/"
              "Machine Learning Prediction of I28 Peptidome PSI (Complete Coverage & 10% Training).csv")
TILE = DATA / "raw/voutsinos-2026/repo/score/degrons.csv.gz"

csv.field_size_limit(10 ** 7)


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    return pearson(rank(x), rank(y))


def fnum(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


# ---------- 1. GPS: trình tự 28-mer, PSI hai replicate ----------
gps = {}            # aa28 -> (psi_mean, psi_rep_x, psi_rep_y, gene)
with open(GPS, newline="", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("AA.Seq") or "").strip().upper()
        if len(aa) != 28 or "*" in aa:
            continue
        obs, px, py = fnum(row.get("Observed.PSI")), fnum(row.get("PSI.x")), fnum(row.get("PSI.y"))
        if obs is None:
            continue
        gps[aa] = (obs, px, py, (row.get("Gene") or "").split("_")[0])

rep_pairs = [(v[1], v[2]) for v in gps.values() if v[1] is not None and v[2] is not None]
print(f"GPS: {len(gps):,} peptide 28-mer duy nhat; {len(rep_pairs):,} co ca hai replicate")
rel_gps = pearson([p[0] for p in rep_pairs], [p[1] for p in rep_pairs])
# do tin cay cua TRUNG BINH hai replicate (Spearman-Brown)
rel_gps_mean = 2 * rel_gps / (1 + rel_gps)
print(f"GPS  r(rep1,rep2)            = {rel_gps:.4f}   -> reliability cua trung binh = {rel_gps_mean:.4f}")

# ---------- 2. Tile: trình tự 30-mer -> ba 28-mer con ----------
tile = {}           # aa28 -> (degron_score, degron_std, gene)
n_tile = 0
with gzip.open(TILE, "rt", encoding="utf-8", errors="replace") as fh:
    for row in csv.DictReader(fh):
        aa = (row.get("aa") or "").strip().upper()
        d, sd = fnum(row.get("degron_score")), fnum(row.get("degron_std"))
        if d is None or sd is None or len(aa) < 28:
            continue
        n_tile += 1
        gene = (row.get("name") or "").split("_tile")[0]
        for off in range(len(aa) - 27):
            tile.setdefault(aa[off:off + 28], (d, sd, gene))

_mean_t = sum(v[0] for v in tile.values()) / len(tile)
var_t = sum((v[0] - _mean_t) ** 2 for v in tile.values()) / len(tile)
err_t = sum(v[1] ** 2 for v in tile.values()) / len(tile)
rel_tile = max(0.0, (var_t - err_t) / var_t)
print(f"Tile: {n_tile:,} tile -> {len(tile):,} khoa 28-mer")
print(f"Tile reliability (tu sai so tung tile) = {rel_tile:.4f}")

# ---------- 3. Giao: cùng trình tự, hai assay ----------
shared = sorted(set(gps) & set(tile))
print(f"\n=== Trinh tu 28-mer co mat trong CA HAI assay: {len(shared):,} ===")
if len(shared) < 30:
    sys.exit("qua it de ket luan")

a = [gps[s][0] for s in shared]          # GPS PSI  (cao = BEN)
b = [tile[s][0] for s in shared]         # degron_score (cao = DEGRON)
genes = {tile[s][2] for s in shared}
r_obs, rho_obs = pearson(a, b), spearman(a, b)
print(f"so gene (ENSG) trong phan giao : {len(genes):,}")
print(f"Pearson (GPS PSI vs degron_score)  = {r_obs:+.4f}")
print(f"Spearman                           = {rho_obs:+.4f}")

# chỉnh suy giảm do nhiễu hai phía: r_true = r_obs / sqrt(rel_A * rel_B)
denom = math.sqrt(max(rel_gps_mean, 1e-9) * max(rel_tile, 1e-9))
r_dis = r_obs / denom
print(f"\n--- Tach nhieu do khoi khac biet that ---")
print(f"tran do nhieu hai assay            = {denom:+.4f}   (= sqrt(rel_GPS * rel_tile))")
print(f"|r| quan sat                        = {abs(r_obs):.4f}")
print(f"|r| sau chinh suy giam              = {min(abs(r_dis),1.0):.4f}")
print(f"KHOANG CACH QUA ASSAY (|r|)         = {denom - abs(r_obs):.4f} tong,"
      f" trong do {max(0.0, 1 - min(abs(r_dis),1.0)):.4f} KHONG do nhieu")

# ---------- 4. Bậc thang trên nhãn nhị phân (AUROC), giống cascade của bài PROTAC ----------
def auroc(score, label):
    pair = sorted(zip(score, label))
    pos = sum(label); neg = len(label) - pos
    if pos == 0 or neg == 0:
        return float("nan")
    # rank-sum, xử lý đồng hạng bằng hạng trung bình
    ranks = [0.0] * len(pair); i = 0
    while i < len(pair):
        j = i
        while j + 1 < len(pair) and pair[j + 1][0] == pair[i][0]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    s = sum(r for r, (_, lb) in zip(ranks, pair) if lb)
    return (s - pos * (pos + 1) / 2) / (pos * neg)

# nhãn degron theo ngưỡng của Zhang: PSI <= 3.0 la peptide degron
lab = [1 if v <= 3.0 else 0 for v in a]
print(f"\n--- Nhan nhi phan: degron = (GPS PSI <= 3.0) ---")
print(f"ty le duong = {sum(lab)/len(lab):.4f}  ({sum(lab):,}/{len(lab):,})")
# degron_score cao => la degron => dung truc tiep lam diem xep hang
auc_cross = auroc(b, lab)
inside = [s for s in shared if gps[s][1] is not None and gps[s][2] is not None]
lab1 = [1 if gps[s][1] <= 3.0 else 0 for s in inside]
auc_within = auroc([-gps[s][2] for s in inside], lab1)      # PSI thap = degron => dao dau
print(f"AUROC(replicate GPS -> nhan GPS)   = {auc_within:.4f}   (TRAN TRONG assay, n={len(inside):,})")
print(f"AUROC(degron_score  -> nhan GPS)   = {auc_cross:.4f}   (QUA assay)")
print(f"=> KHOANG CACH QUA ASSAY (AUROC)   = {auc_within - auc_cross:.4f}")

# ---------- 5. Don vi suy luan: cum protein cov80 ----------
clu = {}
with open(ROOT / "topics/degron-footprint/data/interim/protein-id30-cov80_cluster.tsv",
          newline="", encoding="utf-8") as fh:
    for line in fh:
        parts = line.split()
        if len(parts) == 2:
            clu[parts[1]] = parts[0]
accs = {gps[s][3] for s in shared}
cl = {clu.get(a, a) for a in accs}
print(f"\n--- Don vi suy luan ---")
print(f"accession UniProt trong phan giao  : {len(accs):,}")
print(f"CUM protein cov80                  : {len(cl):,}")

# ---------- 6. Bat dong y o cac ca TU TIN ----------
# GPS: degron manh PSI<=2.0 / khong degron PSI>=4.0 ; tile: nguong tai trung vi
med = sorted(v[0] for v in tile.values())[len(tile) // 2]
conf = [(gps[s][0], tile[s][0]) for s in shared if gps[s][0] <= 2.0 or gps[s][0] >= 4.0]
disag = sum(1 for p, d in conf if (p <= 2.0) != (d > med))
print(f"\n--- Bat dong y tren ca tu tin (GPS PSI<=2.0 hoac >=4.0; tile so voi trung vi {med:.3f}) ---")
print(f"so ca tu tin                       : {len(conf):,}")
print(f"bat dong y hoan toan               : {disag:,}  ({disag/len(conf):.4f})")

# ---------- 7. Dai kho: bo hai duoi cua GPS ----------
hard = [s for s in shared if 2.0 < gps[s][0] < 4.0]
if len(hard) >= 100:
    hl = [1 if gps[s][0] <= 3.0 else 0 for s in hard]
    print(f"\n--- Chi tren dai kho 2.0 < PSI < 4.0 (n={len(hard):,}, duong {sum(hl)/len(hl):.3f}) ---")
    print(f"AUROC qua assay tren dai kho       = {auroc([tile[s][0] for s in hard], hl):.4f}")
    print(f"|Pearson| qua assay tren dai kho   = {abs(pearson([gps[s][0] for s in hard],[tile[s][0] for s in hard])):.4f}")
