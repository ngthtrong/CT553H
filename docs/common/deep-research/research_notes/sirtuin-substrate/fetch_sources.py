"""Download public research sources; never train a model or alter raw inputs."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile
import io
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
CACHE = ROOT / "data/sirtuin-substrate/raw"
MANIFEST = Path(__file__).with_name("download-manifest.json")
SOURCES = {
    "ridgeway.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12594832/fullTextXML",
    "weinert.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4641529/fullTextXML",
    "sirt3-2011.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3042044/fullTextXML",
    "rauh.html": "https://www.nature.com/articles/ncomms3327",
    "github-tree.json": "https://api.github.com/repos/nashirag/ML-Hybrid_Ensemble_Method/git/trees/main?recursive=1",
}
for accession in ["PXD021357", "PXD023479", "PXD019763", "PXD012796"]:
    SOURCES[f"{accession}.json"] = f"https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{accession}"
    SOURCES[f"{accession}-files.json"] = f"https://www.ebi.ac.uk/pride/ws/archive/v2/files/byProject?accession={accession}&pageSize=1000&page=0"


def fetch(item):
    name, url = item
    path = CACHE / name
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "CT553H research audit"})
        with urllib.request.urlopen(request, timeout=180) as response:
            body = response.read()
            record = {"file": name, "url": url, "status": response.status,
                      "content_type": response.headers.get("Content-Type"),
                      "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                      "uniprot_release": response.headers.get("X-UniProt-Release")}
        valid = (not name.endswith((".xlsx", ".docx", ".zip")) or body.startswith(b"PK"))
        valid = valid and (not name.endswith(".pdf") or body.startswith(b"%PDF"))
        record["valid_file_signature"] = valid
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != body:
            path = path.with_name(path.name + "." + record["sha256"][:12] + ".response")
            record["saved_as"] = path.name
        elif not valid:
            path = path.with_name(path.name + ".response")
            record["saved_as"] = path.name
        path.write_bytes(body)
        if name == "weinert-supp.zip" and valid:
            with zipfile.ZipFile(io.BytesIO(body)) as archive:
                for member in archive.namelist():
                    basename = Path(member).name
                    if basename.startswith("embj0034-") and basename.endswith((".xlsx", ".pdf")):
                        target = CACHE / ("weinert-zip-" + basename)
                        if not target.exists():
                            target.write_bytes(archive.read(member))
    except Exception as error:
        record = {"file": name, "url": url, "error": str(error)}
    record["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(record, ensure_ascii=False), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, help="JSON mapping filename to URL")
    args = parser.parse_args()
    source_list = Path(__file__).with_name("sources.json")
    sources = json.loads(args.sources.read_text()) if args.sources else (
        json.loads(source_list.read_text()) if source_list.exists() else SOURCES)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, sources.items()))
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    MANIFEST.write_text(json.dumps(old + records, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
