"""Audit a pinned DARKIN checkout without training or downloading models."""
import argparse
import csv
import hashlib
import json
import statistics
import subprocess
from collections import Counter
from pathlib import Path


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.checkout.resolve()
    base = root / "Darkin_Dataset"
    result = {
        "retrieval_date": "2026-10-10",
        "commit": subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "source": "https://github.com/tastanlab/darkin",
        "sha256": {},
        "splits": {},
    }
    properties = read_csv(base / "data_files/kinase_properties.csv")
    for relative in (
        "Darkin_Dataset/data_files/kinase_properties.csv",
        "baseline_scripts/aupr_zsl.py",
        "bilinear_zero_shot_model/scripts/evaluation/metrics.py",
    ):
        result["sha256"][relative] = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    matrix_path = base / "data_files/kinase_similarity_matrix.csv"
    similarity = {}
    with matrix_path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)[1:]
        for row in reader:
            similarity[row[0]] = dict(zip(header, map(float, row[1:])))
    result["sha256"][str(matrix_path.relative_to(root))] = hashlib.sha256(matrix_path.read_bytes()).hexdigest()
    result["kinase_properties"] = {
        "rows": len(properties),
        "unique_kinases": len({row["Kinase"] for row in properties}),
        "missing_domain": sum(not row["Kinase_Domain"] for row in properties),
    }
    for directory in sorted((base / "datasets").iterdir()):
        zsl = directory / "ZSL"
        if not zsl.exists():
            continue
        sets = {}
        report = {}
        for partition, pattern in (
            ("train", "train_data_*.csv"),
            ("validation", "ZSL_validation_data_*.csv"),
            ("test", "ZSL_test_data_*.csv"),
        ):
            path, = zsl.glob(pattern)
            rows = read_csv(path)
            result["sha256"][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
            counts = Counter(k.strip() for row in rows for k in row["KINASE_ACC_IDS"].split(",") if k.strip())
            keys = {(row["SUB_ACC_ID"], row["SUB_MOD_RSD"]) for row in rows}
            peptides = {row["SITE_+/-7_AA"].upper() for row in rows}
            proteins = {row["SUB_ACC_ID"] for row in rows}
            sets[partition] = {"kinases": set(counts), "keys": keys, "peptides": peptides, "proteins": proteins}
            report[partition] = {
                "rows": len(rows), "pairs": sum(counts.values()), "kinases": len(counts),
                "unique_site_keys": len(keys), "unique_uppercase_windows": len(peptides),
                "positive_sites_per_kinase": {"min": min(counts.values()), "median": statistics.median(counts.values()), "max": max(counts.values())},
                "per_kinase": dict(sorted(counts.items())),
                "non_15mer_rows": sum(len(row["SITE_+/-7_AA"]) != 15 for row in rows),
                "non_STY_center_rows": sum(row["SITE_+/-7_AA"][7].upper() not in "STY" for row in rows),
                "center_exceptions": [row for row in rows if row["SITE_+/-7_AA"][7].upper() not in "STY"],
            }
        report["overlaps"] = {}
        for left, right in (("train", "validation"), ("train", "test"), ("validation", "test")):
            report["overlaps"][f"{left}_{right}"] = {
                name: len(sets[left][name] & sets[right][name]) for name in sets[left]
            }
            cross = [(a, b, similarity[a][b]) for a in sets[left]["kinases"] for b in sets[right]["kinases"] if a in similarity and b in similarity[a]]
            report["overlaps"][f"{left}_{right}"]["domain_matrix_max_percent"] = max(value for _, _, value in cross)
            report["overlaps"][f"{left}_{right}"]["domain_matrix_pairs_ge90"] = sum(value >= 90 for _, _, value in cross)
            report["overlaps"][f"{left}_{right}"]["domain_matrix_pairs_checked"] = len(cross)
            report["overlaps"][f"{left}_{right}"]["domain_matrix_pairs_expected"] = len(sets[left]["kinases"]) * len(sets[right]["kinases"])
        report["test_rows_seen_train"] = {
            "site_key": sum((row["SUB_ACC_ID"], row["SUB_MOD_RSD"]) in sets["train"]["keys"] for row in read_csv(next(zsl.glob("ZSL_test_data_*.csv")))),
            "protein": sum(row["SUB_ACC_ID"] in sets["train"]["proteins"] for row in read_csv(next(zsl.glob("ZSL_test_data_*.csv")))),
        }
        result["splits"][directory.name] = report
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"commit": result["commit"], "properties": result["kinase_properties"], "split_count": len(result["splits"]), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
