#!/usr/bin/env python3
"""Khử trùng lặp các score set MaveDB đã tải, cho 9 gene của bài Voutsinos 2026.

Audit 11/10 đã đếm 69.209 biến thể duy nhất qua API nhưng chỉ dựa metadata. Giờ đã tải
toàn bộ bảng điểm nên đếm được trên dữ liệu thật, và tách rõ: số bản ghi, số biến thể duy
nhất theo gene, và mức chồng lấn giữa các score set trong cùng một gene.
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())
MAVE = TOPIC / "data/raw/mavedb"


def main():
    sets = json.loads((MAVE / "score-sets.json").read_text())
    by_urn = {s["urn"]: s for s in sets}
    per_gene = defaultdict(lambda: {"variants": set(), "rows": 0, "scored": 0, "sets": []})
    per_set = {}

    for path in sorted(MAVE.glob("*.scores.csv")):
        urn = path.stem.replace("_", ":", 2).replace(".scores", "")
        urn = urn.rsplit(".scores", 1)[0]
        meta = by_urn.get(urn.replace("urn:mavedb:", "urn:mavedb:"))
        if meta is None:
            # tên file thay ':' bằng '_'; dựng lại bằng cách so khớp hậu tố
            stem = path.name.split(".scores.csv")[0]
            for candidate in by_urn:
                if candidate.replace(":", "_") == stem:
                    meta = by_urn[candidate]
                    urn = candidate
                    break
        if meta is None:
            continue
        gene = meta["gene"]
        rows = scored = 0
        variants = set()
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            key = None
            for name in ("hgvs_pro", "hgvs_nt", "hgvs_splice", "accession"):
                if reader.fieldnames and name in reader.fieldnames:
                    key = name
                    break
            for row in reader:
                rows += 1
                value = (row.get("score") or "").strip()
                if value in ("", "NA", "NaN", "None"):
                    continue
                scored += 1
                variant = (row.get(key) or "").strip() if key else ""
                if variant and variant not in ("NA", "_wt", "_sy"):
                    variants.add(variant)
        per_set[urn] = {"gene": gene, "title": meta["title"], "rows": rows,
                        "rows_with_score": scored, "unique_variants": len(variants),
                        "declared_numVariants": meta.get("numVariants"),
                        "license": meta.get("license")}
        g = per_gene[gene]
        g["rows"] += rows
        g["scored"] += scored
        g["variants"] |= variants
        g["sets"].append(urn)

    genes = {}
    for gene, g in sorted(per_gene.items()):
        sum_per_set = sum(per_set[u]["unique_variants"] for u in g["sets"])
        genes[gene] = {
            "n_score_sets": len(g["sets"]), "rows": g["rows"], "rows_with_score": g["scored"],
            "unique_variants_after_dedup": len(g["variants"]),
            "sum_of_per_set_unique": sum_per_set,
            "duplication_collapsed": sum_per_set - len(g["variants"]),
        }

    report = {
        "n_score_sets_downloaded": len(per_set),
        "per_gene": genes,
        "total_unique_variants_after_dedup": sum(v["unique_variants_after_dedup"]
                                                 for v in genes.values()),
        "total_rows": sum(v["rows"] for v in genes.values()),
        "per_score_set": per_set,
        "note": ("Khử trùng lặp theo khóa HGVS trong từng gene. Các score set cùng gene chồng "
                 "nhau nên tổng theo từng set lớn hơn số duy nhất. Biến thể _wt và _sy bị loại."),
    }
    path = Path(__file__).parent / "mavedb-audit.json"
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in
                      ("n_score_sets_downloaded", "per_gene",
                       "total_unique_variants_after_dedup", "total_rows")},
                     indent=1, ensure_ascii=False))
    print("\nghi:", path.name)


if __name__ == "__main__":
    main()
