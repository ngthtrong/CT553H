#!/usr/bin/env python3
"""Biến thể gây bệnh có nằm ở ô bị phá degron mạnh hơn biến thể lành tính không?

Đây là phép đo **mắt nối trụ 1 → trụ 2** của khung đề tài. Trụ 1 nói *vùng* degron giàu
biến thể gây bệnh (tỉ số chênh 2,148, [enrichment.py](enrichment.py)). Trụ 2 dự đoán ở mức
**residue**. Câu hỏi còn trống: ở độ phân giải residue thì tín hiệu bệnh có còn không?

Phép nhị phân footprint/không-footprint đã chạy và cho **kết quả rỗng** (OR 0,777,
CI [0,530; 1,139]) nhưng **mất lực** vì chỉ 121 biến thể có phân loại nằm ở vị trí footprint.
Script này thay bằng **ΔPSI liên tục**, dùng được toàn bộ ~1.600 biến thể có phân loại.

**Hướng giả thuyết có nghĩa sinh học:** phá degron ⇒ protein thoát phân hủy ⇒ **bền hơn**
⇒ ΔPSI **dương**. Nên nếu biến thể gây bệnh phá degron thì ΔPSI của chúng phải **lớn hơn**
của biến thể lành tính. Thước đo: **AUC = P(ΔPSI gây bệnh > ΔPSI lành tính)**, 0,5 là rỗng —
cùng họ thước đo với phần còn lại của đề tài.

Ba phép, từ nhiều lực/khớp lỏng đến ít lực/khớp chặt:

  * **scan_pos**  — bộ quét, khớp **vị trí**. Nhiều lực nhất. ⚠ Acid amin thay vào trong thư
                    viện quét là **lựa chọn của tác giả**, không phải alt của ClinVar ⇒ đo
                    *độ nhạy của vị trí*, không phải hiệu ứng của chính biến thể đó.
  * **scan_exact** — bộ quét, khớp **đúng acid amin** của ClinVar. Khớp chặt, ít lực hơn.
  * **sat_exact**  — bộ bão hòa, khớp **đúng ô** trong ma trận 19 thay thế. Khớp chặt nhất,
                    nhãn sạch nhất (nhiễu 16,7%), nhưng **ít lực nhất**.

Đơn vị bootstrap là **cụm protein cov80**, theo đúng đơn vị suy luận của D-031 — không phải
biến thể, vì biến thể trong cùng protein không độc lập. Thêm một phép **ghép cặp trong cùng
peptide** để khử hẳn khác biệt giữa peptide.

Chạy từ thư mục gốc repo:
    .venv/bin/python -I topics/degron-footprint/research/variant-coverage-2026-10-15/delta_psi_test.py
"""

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import coverage as cov                      # noqa: E402

OUT = HERE / "delta-psi-test.json"
SEED = 20261015
N_BOOT = 2000


def auc_gt(xs, ys):
    """P(x > y) + 0.5 P(x == y) — thống kê Mann–Whitney chuẩn hoá. 0,5 là rỗng."""
    if not xs or not ys:
        return None
    merged = sorted([(v, 0) for v in xs] + [(v, 1) for v in ys])
    # xếp hạng có xử lý đồng hạng
    ranks = {}
    i = 0
    while i < len(merged):
        j = i
        while j + 1 < len(merged) and merged[j + 1][0] == merged[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    r_x = sum(ranks[k] for k, (_, g) in enumerate(merged) if g == 0)
    n1, n2 = len(xs), len(ys)
    u = r_x - n1 * (n1 + 1) / 2
    return u / (n1 * n2)


def boot_auc(by_cluster, rng, n_boot=N_BOOT):
    """CI của AUC, bootstrap **theo cụm protein**. by_cluster: {cl: ([patho], [benign])}."""
    clusters = list(by_cluster)
    if len(clusters) < 3:
        return None
    out = []
    for _ in range(n_boot):
        xs, ys = [], []
        for cl in rng.choices(clusters, k=len(clusters)):
            p, b = by_cluster[cl]
            xs.extend(p)
            ys.extend(b)
        a = auc_gt(xs, ys)
        if a is not None:
            out.append(a)
    if len(out) < 100:
        return None
    out.sort()
    return [out[int(0.025 * len(out))], out[int(0.975 * len(out))]]


def paired_within_peptide(by_pep, rng, n_boot=N_BOOT):
    """Hiệu trung bình ΔPSI(gây bệnh) − ΔPSI(lành tính), ghép cặp trong cùng peptide."""
    diffs = []
    for pep, (p, b) in by_pep.items():
        if p and b:
            diffs.append(statistics.fmean(p) - statistics.fmean(b))
    if len(diffs) < 3:
        return {"n_peptides": len(diffs), "note": "quá ít peptide có cả hai nhóm"}
    boots = []
    for _ in range(n_boot):
        s = rng.choices(diffs, k=len(diffs))
        boots.append(statistics.fmean(s))
    boots.sort()
    pos = sum(1 for d in diffs if d > 0)
    return {
        "n_peptides": len(diffs),
        "mean_diff": statistics.fmean(diffs),
        "median_diff": statistics.median(diffs),
        "ci95": [boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots))]],
        "n_positive": pos,
        "frac_positive": pos / len(diffs),
    }


def summarise(tag, rec, rng):
    """rec: {"by_cluster": {...}, "by_pep": {...}, "vus": [...]}"""
    xs = [v for p, _ in rec["by_cluster"].values() for v in p]
    ys = [v for _, b in rec["by_cluster"].values() for v in b]
    auc = auc_gt(xs, ys)
    out = {
        "n_pathogenic": len(xs),
        "n_benign": len(ys),
        "n_vus": len(rec["vus"]),
        "n_clusters": len(rec["by_cluster"]),
        "median_dpsi_pathogenic": statistics.median(xs) if xs else None,
        "median_dpsi_benign": statistics.median(ys) if ys else None,
        "median_dpsi_vus": statistics.median(rec["vus"]) if rec["vus"] else None,
        "auc_patho_gt_benign": auc,
        "auc_ci95_bootstrap_by_cluster": boot_auc(rec["by_cluster"], rng),
        "paired_within_peptide": paired_within_peptide(rec["by_pep"], rng),
    }
    # phiên bản |ΔPSI|: nhiễu loạn theo chiều nào cũng tính
    abs_bc = {cl: ([abs(v) for v in p], [abs(v) for v in b])
              for cl, (p, b) in rec["by_cluster"].items()}
    out["auc_abs_dpsi"] = auc_gt([abs(v) for v in xs], [abs(v) for v in ys])
    out["auc_abs_ci95"] = boot_auc(abs_bc, rng)
    return out


def main():
    rng = random.Random(SEED)
    data = cov.rd.load_all()
    spans, _ = cov.build_spans(data)
    uniprot = data["uniprot"]
    rep = data["clusters"]
    acc2gene, _ = cov.uniprot_genes()

    scan, sat = data["scan"], data["sat"]
    # tra cứu nhanh
    scan_cells = {pep: rec["cells"] for pep, rec in scan.items()}
    sat_cells = {pep: rec["cells"] for pep, rec in sat.items()}

    lib_accs = set()
    for tag in cov.TIERS:
        lib_accs |= set(spans[tag])
    lib_genes = defaultdict(set)
    for acc in lib_accs:
        g = acc2gene.get(acc)
        if g:
            lib_genes[g].add(acc)

    tiers = {t: {"by_cluster": defaultdict(lambda: ([], [])),
                 "by_pep": defaultdict(lambda: ([], [])),
                 "vus": []}
             for t in ("scan_pos", "scan_exact", "sat_exact")}
    stats = Counter()

    def record(tier, cl, pep, bucket, value):
        d = tiers[tier]
        if bucket == "vus":
            d["vus"].append(value)
            return
        idx = 0 if bucket == "pathogenic" else 1
        d["by_cluster"][cl][idx].append(value)
        d["by_pep"][pep][idx].append(value)

    for gene, ref1, pos, alt1, bucket, vid, onc in cov.stream_clinvar():
        if bucket not in ("pathogenic", "benign", "vus"):
            continue
        accs = lib_genes.get(gene)
        if not accs:
            continue
        ok_acc = None
        for acc in accs:
            seq = uniprot.get(acc)
            if seq and pos <= len(seq) and seq[pos - 1] == ref1:
                ok_acc = acc
                break
        if not ok_acc:
            continue
        cl = rep.get(ok_acc, ok_acc)

        # --- bộ quét
        for start, end, pep in spans["scan"].get(ok_acc, ()):
            if not (start <= pos <= end):
                continue
            off = pos - start + 1
            cell = scan_cells.get(pep, {}).get(off)
            if cell is None:
                break
            aa_mut, dpsi = cell[0], cell[1]
            record("scan_pos", cl, pep, bucket, dpsi)
            stats[f"scan_pos_{bucket}"] += 1
            if aa_mut and aa_mut.upper() == alt1:
                record("scan_exact", cl, pep, bucket, dpsi)
                stats[f"scan_exact_{bucket}"] += 1
            break

        # --- bộ bão hòa, khớp đúng ô (trung bình hai replicate theo D-025.3)
        for start, end, pep in spans["sat"].get(ok_acc, ()):
            if not (start <= pos <= end):
                continue
            off = pos - start + 1
            cell = sat_cells.get(pep, {}).get((off, alt1))
            if cell is not None:
                da, db = cell
                record("sat_exact", cl, pep, bucket, (da + db) / 2)
                stats[f"sat_exact_{bucket}"] += 1
            break

    result = {
        "seed": SEED, "n_bootstrap": N_BOOT,
        "hypothesis": ("phá degron => protein bền hơn => ΔPSI dương; "
                       "nên AUC P(ΔPSI gây bệnh > ΔPSI lành tính) > 0,5 nếu có tín hiệu"),
        "counts": dict(stats),
        "tiers": {t: summarise(t, rec, rng) for t, rec in tiers.items()},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
