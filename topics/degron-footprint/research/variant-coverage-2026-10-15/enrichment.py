#!/usr/bin/env python3
"""Biến thể gây bệnh có giàu lên trong vùng degron đo được hay không — có khử nhiễu gene.

`coverage.py` cho tỉ số chênh thô **2,095** (gây bệnh so với lành tính, tile degron so với
tile không degron). Con số thô đó **không dùng được một mình**, vì ClinVar bị một nhóm nhỏ
gene bệnh được giải trình tự rất sâu chiếm đa số: nếu đúng những gene đó tình cờ có nhiều
tile degron thì tỉ số chênh lên cao mà không mang ý nghĩa nào ở mức residue. Đây đúng là
lỗi mà đề tài đã ghi nhận một lần (xem rủi ro "đơn vị suy luận là cụm protein").

Nên script này tính **Mantel–Haenszel phân tầng theo protein**: chỉ so tile degron với tile
không degron **trong cùng một protein**, rồi gộp các tầng. Mọi khác biệt giữa gene (bao nhiêu
biến thể được nộp, gene có phải gene bệnh hay không) bị khử theo thiết kế.

Báo thêm bản phân tầng theo **cụm cov80** để khớp đơn vị suy luận mà D-031 đã chốt.

Mẫu số luôn là tile **đo được** (reads >= 10): so degron với không-degron trong cùng miền
đo được, không so với vùng không có số liệu.

Chạy từ thư mục gốc repo:
    .venv/bin/python -I topics/degron-footprint/research/variant-coverage-2026-10-15/enrichment.py
"""

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import coverage as cov                      # noqa: E402

OUT = HERE / "enrichment.json"


def mantel_haenszel(strata):
    """strata: [(a, b, c, d)] với a=degron&patho, b=degron&benign, c=khác&patho, d=khác&benign.

    Trả OR_MH kèm CI 95% theo Robins–Breslow–Greenland.
    """
    num = den = 0.0
    rbg_p = rbg_q = rbg_pq = 0.0
    used = 0
    for a, b, c, d in strata:
        n = a + b + c + d
        if n == 0:
            continue
        # tầng chỉ thông tin khi có cả hai chiều
        if (a + b) == 0 or (c + d) == 0 or (a + c) == 0 or (b + d) == 0:
            continue
        used += 1
        num += a * d / n
        den += b * c / n
        p = (a + d) / n
        q = (b + c) / n
        r = a * d / n
        s = b * c / n
        rbg_p += p * r
        rbg_q += p * s + q * r
        rbg_pq += q * s
    if den == 0 or num == 0:
        return None
    or_mh = num / den
    var = (rbg_p / (2 * num ** 2)
           + rbg_q / (2 * num * den)
           + rbg_pq / (2 * den ** 2))
    se = math.sqrt(var)
    return {
        "or_mh": or_mh,
        "ci95": [math.exp(math.log(or_mh) - 1.96 * se),
                 math.exp(math.log(or_mh) + 1.96 * se)],
        "strata_informative": used,
        "strata_total": len(strata),
    }


def main():
    data = cov.rd.load_all()
    spans, sizes = cov.build_spans(data)
    uniprot = data["uniprot"]
    rep = data["clusters"]
    acc2gene, _ = cov.uniprot_genes()

    lib_accs = set()
    for tag in cov.TIERS:
        lib_accs |= set(spans[tag])
    lib_genes = defaultdict(set)
    for acc in lib_accs:
        g = acc2gene.get(acc)
        if g:
            lib_genes[g].add(acc)

    # Tra cứu nhanh: accession -> danh sách span, cho hai tầng cần so.
    def spanlist(tag, acc):
        return spans[tag].get(acc, ())

    # per-protein và per-cluster: [degron_patho, degron_benign, other_patho, other_benign]
    by_protein = defaultdict(lambda: [0, 0, 0, 0])
    by_cluster = defaultdict(lambda: [0, 0, 0, 0])
    totals = Counter()

    for gene, ref1, pos, alt1, bucket, vid, onc in cov.stream_clinvar():
        if bucket not in ("pathogenic", "benign"):
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

        in_all = any(s <= pos <= e for s, e, _ in spanlist("pepdome_all", ok_acc))
        if not in_all:
            totals["outside_measured"] += 1
            continue            # mẫu số là tile đo được
        in_deg = any(s <= pos <= e for s, e, _ in spanlist("pepdome_degron", ok_acc))

        idx = (0 if bucket == "pathogenic" else 1) + (0 if in_deg else 2)
        by_protein[ok_acc][idx] += 1
        by_cluster[rep.get(ok_acc, ok_acc)][idx] += 1
        totals[f"{'degron' if in_deg else 'other'}_{bucket}"] += 1

    crude_a = totals["degron_pathogenic"]
    crude_b = totals["degron_benign"]
    crude_c = totals["other_pathogenic"]
    crude_d = totals["other_benign"]
    crude_or = (crude_a * crude_d) / (crude_b * crude_c)
    se = math.sqrt(1 / crude_a + 1 / crude_b + 1 / crude_c + 1 / crude_d)

    result = {
        "counts": dict(totals),
        "crude": {
            "table": {"degron_patho": crude_a, "degron_benign": crude_b,
                      "other_patho": crude_c, "other_benign": crude_d},
            "or": crude_or,
            "ci95": [math.exp(math.log(crude_or) - 1.96 * se),
                     math.exp(math.log(crude_or) + 1.96 * se)],
        },
        "mh_by_protein": mantel_haenszel(list(by_protein.values())),
        "mh_by_cluster_cov80": mantel_haenszel(list(by_cluster.values())),
        "n_proteins": len(by_protein),
        "n_clusters": len(by_cluster),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
