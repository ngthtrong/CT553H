#!/usr/bin/env python3
"""Fetch pinned Mendeley scanning/saturation archives; keep raw files outside Git."""

import argparse
import hashlib
import json
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[5]
BASE = "https://data.mendeley.com"
DATASET = "32h94v2yv2"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
PINNED = {
    "I28 Scanning Mutagenesis.zip": "a82bd1ee4bc7a2da69df06cb44dd34fe8480c6fd799340684f5058d02223df50",
    "I28 CRL Saturation Mutagenesis.zip": "cbda58342265dd73b7946cd091c5b558eed6e615bbcb97921e37bd50fbb5ee60",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path,
                        default=ROOT / "data/degron-e3-specificity/raw")
    args = parser.parse_args()
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(
        f"{BASE}/public-api/datasets/{DATASET}/files",
        params={"folder_id": "root", "version": 2}, headers=HEADERS, timeout=60,
    )
    response.raise_for_status()
    entries = response.json()
    records = []
    for entry in entries:
        name = entry["filename"]
        if name not in PINNED:
            continue
        expected = PINNED[name]
        details = entry["content_details"]
        if details["sha256_hash"] != expected:
            raise ValueError(f"Upstream checksum changed: {name}")
        dest = args.raw_dir / name
        if not dest.exists():
            temporary = dest.with_suffix(".part")
            with requests.get(details["download_url"], headers=HEADERS,
                              stream=True, timeout=60) as download:
                download.raise_for_status()
                with temporary.open("wb") as handle:
                    for chunk in download.iter_content(1024 * 1024):
                        handle.write(chunk)
            if hashlib.sha256(temporary.read_bytes()).hexdigest() != expected:
                raise ValueError(f"Downloaded checksum mismatch: {name}")
            temporary.rename(dest)
        actual = hashlib.sha256(dest.read_bytes()).hexdigest()
        if actual != expected or dest.stat().st_size != details["size"]:
            raise ValueError(f"Local file does not match source: {name}")
        records.append({"filename": name, "bytes": dest.stat().st_size,
                        "sha256": actual, "download_url": details["download_url"]})
        print(f"Verified {name}: {dest.stat().st_size} bytes", flush=True)
    if len(records) != len(PINNED):
        raise ValueError("One or more pinned archives are absent from version 2")
    (args.raw_dir / "download-manifest.json").write_text(
        json.dumps({"dataset": "10.17632/32h94v2yv2.2", "files": records}, indent=2)
        + "\n", encoding="utf-8",
    )


if __name__ == "__main__":
    main()
