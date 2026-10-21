#!/usr/bin/env python3
"""Cache full-length UniProt sequences and cluster scanning-library proteins.

Current reference sequences are not the original library's historical snapshot.
Empty/retired entries remain missing; redirects are recorded and clustered together.
"""

import argparse
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "CLAUDE.md").exists())
TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "data" / "README.md").exists())  # thư mục đề tài
HEADERS = {"User-Agent": "CT553H-research-audit/1.0"}


def read_fasta(lines):
    records, accession, pieces = {}, None, []
    for line in lines:
        if line.startswith(">"):
            if accession is not None:
                records[accession] = "".join(pieces)
            accession = line.split("|")[1]
            pieces = []
        else:
            pieces.append(line.strip())
    if accession is not None:
        records[accession] = "".join(pieces)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="2026-10-12", help="Local snapshot/cache label")
    parser.add_argument("--coverage", type=float, default=.8)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    base = TOPIC / "data"
    raw, processed, interim = (base / name for name in ("raw", "processed", "interim"))
    interim.mkdir(parents=True, exist_ok=True)
    wanted = set((processed / "protein-accessions.txt").read_text().split())
    snapshot = raw / f"human-reviewed-{args.date}.fasta.gz"
    manifest = snapshot.with_suffix(".manifest.json")
    if not snapshot.exists():
        with requests.get("https://rest.uniprot.org/uniprotkb/stream",
                          params={"compressed": "true", "format": "fasta",
                                  "query": "(organism_id:9606) AND (reviewed:true)"},
                          headers=HEADERS, stream=True, timeout=60) as response:
            response.raise_for_status()
            partial = snapshot.with_suffix(".part")
            with partial.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    handle.write(chunk)
            partial.rename(snapshot)
            manifest.write_text(json.dumps({
                "url": response.url, "uniprot_release": response.headers.get("X-UniProt-Release"),
                "bytes": snapshot.stat().st_size,
                "sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            }, indent=2))
    recorded = json.loads(manifest.read_text())
    if hashlib.sha256(snapshot.read_bytes()).hexdigest() != recorded["sha256"]:
        raise ValueError("Cached UniProt snapshot checksum mismatch")
    with gzip.open(snapshot, "rt") as handle:
        sequences = read_fasta(handle)
    selected = {a: sequences[a] for a in wanted if a in sequences}
    additional = raw / "uniprot-additional"
    additional.mkdir(exist_ok=True)
    records_file = additional / "manifest.json"
    records = json.loads(records_file.read_text()) if records_file.exists() else []
    seen = {record["requested"] for record in records}

    def fetch(accession):
        response = requests.get(f"https://rest.uniprot.org/uniprotkb/{accession}.fasta",
                                headers=HEADERS, timeout=60)
        response.raise_for_status()
        (additional / f"{accession}.fasta").write_bytes(response.content)
        return {"requested": accession, "status": response.status_code, "url": response.url,
                "firstline": response.text.splitlines()[0] if response.text else "",
                "sha256": hashlib.sha256(response.content).hexdigest()}

    with ThreadPoolExecutor(args.threads) as executor:
        records.extend(executor.map(fetch, sorted(wanted - selected.keys() - seen)))
    records_file.write_text(json.dumps(records, indent=2) + "\n")
    for record in records:
        path = additional / (record["requested"] + ".fasta")
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"Additional sequence checksum mismatch: {path.name}")
        if record["status"] == 200 and record["firstline"].startswith(">"):
            entries = read_fasta(path.read_text().splitlines())
            if len(entries) != 1:
                raise ValueError(f"Expected one sequence for {record['requested']}")
            selected[record["requested"]] = next(iter(entries.values()))
    fasta = processed / "proteins-full.fasta"
    fasta.write_text("".join(f">{a}\n{selected[a]}\n" for a in sorted(selected)))
    prefix = interim / f"protein-id30-cov{int(args.coverage * 100)}"
    command = ["mmseqs", "easy-cluster", str(fasta), str(prefix), str(prefix) + "-tmp",
               "--min-seq-id", "0.3", "-c", str(args.coverage), "--cov-mode", "0",
               "--seq-id-mode", "0", "--alignment-mode", "3", "--cluster-mode", "1",
               "--single-step-clustering", "1", "-s", "7.5", "--max-seqs", "10000",
               "--split-memory-limit", "2G", "--threads", str(args.threads)]
    clusters = Path(str(prefix) + "_cluster.tsv")
    reused = clusters.exists()
    out = Path(__file__).with_name(f"protein-clusters-cov{int(args.coverage * 100)}.json")
    if reused and out.exists():
        prior = json.loads(out.read_text())
        if (prior["full_fasta_sha256"] != hashlib.sha256(fasta.read_bytes()).hexdigest()
                or prior["bidirectional_coverage"] != args.coverage):
            raise ValueError("Cached clusters have different inputs; use a fresh clustering cache")
    if not reused:
        with (raw / f"mmseqs-id30-cov{int(args.coverage * 100)}.log").open("w") as handle:
            subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT, check=True)
    cluster_records = [line.split("\t") for line in clusters.read_text().splitlines()]
    members = {member for _, member in cluster_records}
    if members != selected.keys():
        raise ValueError("Cluster members differ from the retrieved sequence set")
    sizes = Counter(representative for representative, _ in cluster_records)
    result = {
        "date": args.date, "uniprot_snapshot": recorded,
        "wanted_accessions": len(wanted), "retrieved_accessions": len(selected),
        "missing_accessions": sorted(wanted - selected.keys()),
        "full_fasta_sha256": hashlib.sha256(fasta.read_bytes()).hexdigest(),
        "mmseqs_version": subprocess.check_output(["mmseqs", "version"], text=True).strip(),
        "reproduction_command": command, "cached_clusters_reused": reused,
        "minimum_identity": .3, "bidirectional_coverage": args.coverage,
        "cluster_mode": "connected component", "clusters": len(sizes),
        "largest_cluster_proteins": max(sizes.values()),
        "cluster_tsv_sha256": hashlib.sha256(clusters.read_bytes()).hexdigest(),
        "limitation": "Current-reference and heuristic alignment clusters, not proof of zero homology leakage",
    }
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("retrieved_accessions", "missing_accessions",
                                            "clusters", "largest_cluster_proteins")}, indent=2))


if __name__ == "__main__":
    main()
