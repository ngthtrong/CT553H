#!/usr/bin/env python3
"""Tải đầy đủ các bộ dữ liệu của đề tài degron vào data/raw/, kiểm SHA-256, ghi manifest.

Nguồn:
  1. Mendeley 10.17632/32h94v2yv2.2 (Zhang 2023): cả 5 file, checksum do Mendeley công bố.
  2. GEO GSE240610 (Zhang 2023, GPS peptidome): Table S1 + RAW.tar.
  3. GitHub KULL-Centre/_2025_Voutsinos_degron_cytosol (Voutsinos 2026), ghim commit.
  4. MaveDB (CC0): mọi score set của 9 gene trong bài Voutsinos.

Không tải read giải trình tự (SRA PRJNA1277273, các FASTQ của Zhang): dữ liệu đã tính
PSI/score có sẵn ở trên. Zenodo 16925278 trả 403 từ mạng này; repo GitHub là bản cùng tác giả.

Chạy lại: .venv/bin/python fetch_all.py [--only mendeley,geo,voutsinos,mavedb]
"""

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import requests

TOPIC = next(p for p in Path(__file__).resolve().parents if (p / "log.md").exists())
RAW = TOPIC / "data/raw"
UA = {"User-Agent": "Mozilla/5.0 (CT553H thesis data audit)"}

MENDELEY_DATASET = "32h94v2yv2"
GEO_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE240nnn/GSE240610/suppl/"
GEO_FILES = [
    "GSE240610_Supplementary_Table_1_Raw_data_of_GPS_peptidome_screens__Control_+_MLN4924_.xlsx",
    "GSE240610_RAW.tar",
    "filelist.txt",
]
VOUTSINOS_REPO = "https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol.git"
VOUTSINOS_COMMIT = "9b3eafa6bd9730c558cd018063fa0180edf9db1a"  # main, 06/03/2026
MAVE_GENES = ["PTEN", "TPMT", "NUDT15", "CYP2C9", "CYP2C19", "ASPA", "PRKN", "GCK", "LDLR"]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest, expected_sha=None, expected_size=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        part = dest.with_name(dest.name + ".part")
        for attempt in range(3):
            try:
                with requests.get(url, headers=UA, stream=True, timeout=120) as r:
                    r.raise_for_status()
                    with part.open("wb") as fh:
                        for chunk in r.iter_content(1 << 20):
                            fh.write(chunk)
                break
            except requests.RequestException:
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))
        part.rename(dest)
    digest = sha256(dest)
    if expected_sha and digest != expected_sha:
        raise ValueError(f"SHA-256 không khớp: {dest.name}")
    if expected_size is not None and dest.stat().st_size != expected_size:
        raise ValueError(f"Kích thước không khớp: {dest.name}")
    print(f"OK {dest.relative_to(TOPIC)} {dest.stat().st_size} B", flush=True)
    return {"path": str(dest.relative_to(TOPIC)), "bytes": dest.stat().st_size,
            "sha256": digest, "url": url}


def fetch_mendeley():
    r = requests.get(f"https://data.mendeley.com/public-api/datasets/{MENDELEY_DATASET}/files",
                     params={"folder_id": "root", "version": 2},
                     headers={**UA, "Accept": "application/json"}, timeout=60)
    r.raise_for_status()
    out = []
    for e in r.json():
        d = e["content_details"]
        out.append(download(d["download_url"], RAW / e["filename"], d["sha256_hash"], d["size"]))
    return {"source": "Mendeley Data 10.17632/32h94v2yv2.2 (Zhang et al. 2023, CC BY 4.0)",
            "checksum": "khớp sha256 do Mendeley công bố", "files": out}


def fetch_geo():
    out = [download(GEO_BASE + name, RAW / "geo-gse240610" / name) for name in GEO_FILES]
    return {"source": "NCBI GEO GSE240610 (Zhang et al. 2023)",
            "checksum": "GEO không công bố checksum; sha256 ghi lại tại thời điểm tải", "files": out}


def fetch_voutsinos():
    dest = RAW / "voutsinos-2026" / "repo"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", VOUTSINOS_REPO, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", VOUTSINOS_COMMIT], check=True)
    head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()
    if head != VOUTSINOS_COMMIT:
        raise ValueError("Commit Voutsinos không khớp")
    files = []
    for p in sorted(dest.rglob("*")):
        if p.is_file() and ".git" not in p.relative_to(dest).parts:
            files.append({"path": str(p.relative_to(TOPIC)), "bytes": p.stat().st_size,
                          "sha256": sha256(p)})
    print(f"OK voutsinos repo @ {head[:10]}, {len(files)} file", flush=True)
    return {"source": f"{VOUTSINOS_REPO} @ {VOUTSINOS_COMMIT} (MIT)", "files": files}


def fetch_mavedb():
    base = "https://api.mavedb.org/api/v1"
    out, sets = [], []
    for gene in MAVE_GENES:
        r = requests.post(f"{base}/score-sets/search", json={"targets": [gene]},
                          headers=UA, timeout=60)
        r.raise_for_status()
        for s in r.json()["scoreSets"]:
            urn = s["urn"]
            safe = urn.replace(":", "_")
            sets.append({"gene": gene, "urn": urn, "title": s["title"],
                         "numVariants": s.get("numVariants"),
                         "license": (s.get("license") or {}).get("shortName")})
            out.append(download(f"{base}/score-sets/{urn}/scores",
                                RAW / "mavedb" / f"{safe}.scores.csv"))
            meta = RAW / "mavedb" / f"{safe}.json"
            if not meta.exists():
                m = requests.get(f"{base}/score-sets/{urn}", headers=UA, timeout=60)
                m.raise_for_status()
                meta.write_text(json.dumps(m.json(), indent=1), encoding="utf-8")
    (RAW / "mavedb" / "score-sets.json").write_text(json.dumps(sets, indent=1), encoding="utf-8")
    return {"source": "MaveDB api.mavedb.org (CC0 theo từng score set)",
            "checksum": "MaveDB có thể cập nhật; sha256 ghi lại tại thời điểm tải",
            "score_sets": sets, "files": out}


SOURCES = {"mendeley": fetch_mendeley, "geo": fetch_geo,
           "voutsinos": fetch_voutsinos, "mavedb": fetch_mavedb}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default=",".join(SOURCES))
    args = ap.parse_args()
    manifest_path = RAW / "full-download-manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for name in args.only.split(","):
        manifest[name] = SOURCES[name]()
        manifest[name]["fetched"] = time.strftime("%Y-%m-%d")
        manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    print("manifest:", manifest_path.relative_to(TOPIC))


if __name__ == "__main__":
    main()
