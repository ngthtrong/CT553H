#!/usr/bin/env python3
"""Verify and import the pinned RTK_RAG archive; audit sequences without splitting.

Uses only Python's standard library. Original files stay unchanged under raw/.
No upstream code is executed and no model/embedding is downloaded.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
import statistics
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "DECISIONS.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())  # thư mục đề tài
SLUG = "rtk-atp-applicability"
COMMIT = "b7bd4c2347c7d44d24ae3d13e42082ba6cd62627"
URL = f"https://codeload.github.com/B1607/RTK_RAG/zip/{COMMIT}"
ARCHIVE_SHA256 = "a82015b5b8a23ef0634decc22bd27f00392e34fd40f4f3e10a21365f686287d4"
SETS = {
    "atp-549": ("ATP_549", "ATP_549", 549),
    "rtk-69": ("RTK_Test", "RTK", 69),
    "rag-244": ("RAG_Fasta", None, 244),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def dump_csv(path, rows, fields):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Use a previously downloaded archive (offline)")
    args = parser.parse_args()
    raw = TOPIC / "data" / "raw"
    processed = TOPIC / "data" / "processed"
    reports = TOPIC / "03-data"
    for directory in (raw, processed, reports):
        directory.mkdir(parents=True, exist_ok=True)
    archive_path = raw / f"rtk-rag-{COMMIT}.zip"
    if args.archive:
        content = args.archive.read_bytes()
    elif archive_path.exists():
        content = archive_path.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=120) as response:
            content = response.read()
    if digest(content) != ARCHIVE_SHA256:
        raise ValueError("Archive SHA-256 differs from the verified snapshot; inspect before importing")
    if not archive_path.exists():
        archive_path.write_bytes(content)
    elif digest(archive_path.read_bytes()) != ARCHIVE_SHA256:
        raise ValueError("Existing raw archive changed; refusing to overwrite")
    source = raw / "rtk-rag"
    files = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupted ZIP member")
        for member in archive.infolist():
            if member.is_dir():
                continue
            parts = Path(member.filename).parts
            if parts[0] != f"RTK_RAG-{COMMIT}" or ".." in parts:
                raise ValueError(f"Unexpected archive path: {member.filename}")
            relative = Path(*parts[1:])
            target = source / relative
            payload = archive.read(member)
            if target.exists() and target.read_bytes() != payload:
                raise ValueError(f"Raw file was modified: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(payload)
            files.append({"path": str(relative), "bytes": len(payload), "sha256": digest(payload)})
    records = []
    errors = []
    for name, (fasta_dir, label_dir, expected) in SETS.items():
        paths = sorted((source / "Data/Fasta" / fasta_dir).glob("*.fasta"))
        if len(paths) != expected:
            errors.append(f"{name}: expected {expected} FASTA, got {len(paths)}")
        if label_dir:
            labels = list((source / "Data/Label" / label_dir).glob("*.label"))
            if {p.stem for p in labels} != {p.stem for p in paths}:
                errors.append(f"{name}: FASTA/label identifiers differ")
        for path in paths:
            lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
            headers = [line for line in lines if line.startswith(">")]
            if len(headers) != 1 or not lines[0].startswith(">"):
                errors.append(f"{name}/{path.stem}: invalid single-record FASTA")
            sequence = "".join(line for line in lines if not line.startswith(">")).upper()
            if not sequence or not set(sequence) <= set("ACDEFGHIKLMNPQRSTVWYBXZJUO"):
                errors.append(f"{name}/{path.stem}: invalid amino acids")
            label = None
            if label_dir:
                label_path = source / "Data/Label" / label_dir / f"{path.stem}.label"
                label = "".join(label_path.read_text().split()) if label_path.exists() else ""
                if len(label) != len(sequence) or not set(label) <= {"0", "1"}:
                    errors.append(f"{name}/{path.stem}: invalid labels or length mismatch")
            records.append({"dataset": name, "protein_id": path.stem, "header": headers[0][1:] if headers else "",
                            "sequence": sequence, "labels": label, "length": len(sequence),
                            "positive": label.count("1") if label is not None else None,
                            "sequence_sha256": digest(sequence.encode())})
    if errors:
        dump_json(reports / "validation-errors.json", errors)
        raise ValueError(f"{len(errors)} validation errors; see validation-errors.json")
    summary = {}
    for name in SETS:
        subset = [r for r in records if r["dataset"] == name]
        lengths = [r["length"] for r in subset]
        positive = sum(r["positive"] for r in subset) if subset[0]["labels"] is not None else None
        total = sum(lengths)
        summary[name] = {"proteins": len(subset), "unique_sequences": len({r["sequence_sha256"] for r in subset}),
                         "residues": total, "positive": positive,
                         "negative": total - positive if positive is not None else None,
                         "positive_fraction": positive / total if positive is not None else None,
                         "min_length": min(lengths), "median_length": statistics.median(lengths),
                         "max_length": max(lengths), "over_1000_aa": sum(n > 1000 for n in lengths),
                         "noncanonical_residues": dict(Counter(a for r in subset for a in r["sequence"] if a not in "ACDEFGHIKLMNPQRSTVWY")),
                         "zero_positive_proteins": sum(r["positive"] == 0 for r in subset) if positive is not None else None}
        with (processed / f"{name}.fasta").open("w") as f:
            for row in subset:
                f.write(f'>{name}|{row["protein_id"]}\n{row["sequence"]}\n')
    by_sequence = defaultdict(list)
    for r in records:
        by_sequence[r["sequence_sha256"]].append(r)
    duplicate_groups, conflicts = [], []
    for key, group in by_sequence.items():
        if len(group) < 2:
            continue
        members = [f'{r["dataset"]}/{r["protein_id"]}' for r in group]
        duplicate_groups.append({"sequence_sha256": key, "members": members})
        if len({r["labels"] for r in group if r["labels"] is not None}) > 1:
            conflicts.append({"sequence_sha256": key, "members": members})
    overlaps = {}
    for a, b in itertools.combinations(SETS, 2):
        ra = [r for r in records if r["dataset"] == a]
        rb = [r for r in records if r["dataset"] == b]
        common = {r["sequence_sha256"] for r in ra} & {r["sequence_sha256"] for r in rb}
        overlaps[f"{a} vs {b}"] = {"exact_sequence_hashes": len(common),
                                    "shared_identifiers": sorted({r["protein_id"] for r in ra} & {r["protein_id"] for r in rb})}
    audit = {"source_commit": COMMIT, "datasets": summary, "unique_sequences_total": len(by_sequence),
             "exact_duplicate_groups": duplicate_groups, "conflicting_label_groups": conflicts,
             "cross_dataset_overlap": overlaps, "validation_errors": errors,
             "homology_alignment_performed": False, "train_validation_test_split_created": False}
    manifest = {"repository": "https://github.com/B1607/RTK_RAG", "commit": COMMIT, "archive_url": URL,
                "archive_sha256": digest(content), "archive_bytes": len(content),
                "verified_at_utc": datetime.now(timezone.utc).isoformat(), "files": files}
    dump_json(raw / "manifest.json", manifest)
    dump_json(reports / "source-manifest.json", manifest)
    dump_json(reports / "audit-summary.json", audit)
    dump_csv(reports / "dataset-summary.csv", [{"dataset": key, **{k: v for k, v in val.items() if k != "noncanonical_residues"}} for key, val in summary.items()],
             ["dataset"] + [k for k in next(iter(summary.values())) if k != "noncanonical_residues"])
    with (processed / "proteins.jsonl").open("w") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    fields = ["dataset", "protein_id", "header", "length", "positive", "sequence_sha256"]
    dump_csv(processed / "protein-index.csv", [{k: r[k] for k in fields} for r in records], fields)
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
