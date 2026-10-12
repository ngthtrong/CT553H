#!/usr/bin/env python3
"""Audit pinned RCAEval index and six raw cases; no model training or scoring.

Index labels and root_cause.txt are evaluation-only. Case names encode answers
and must never be predictor features. Download only the files needed by the audit.
"""

import argparse
import gc
import hashlib
import json
import platform
import time
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[3]
DATASET = "phamquiluan/RCAEval"
REVISION = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
INDEX_SHA256 = "c49a288920dbba2e8e724679a14636d5c7eb2b45426bba14007ef79a6c0ab1bb"


def download(path, destination, expected_sha=None, expected_size=None):
    url = f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/{path}"
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_suffix(destination.suffix + ".part")
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with partial.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    handle.write(chunk)
        actual_sha = hashlib.sha256(partial.read_bytes()).hexdigest()
        if expected_sha and actual_sha != expected_sha:
            raise ValueError(f"Downloaded checksum mismatch: {path}")
        if expected_size is not None and partial.stat().st_size != expected_size:
            raise ValueError(f"Downloaded size mismatch: {path}")
        partial.rename(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    if expected_sha and digest != expected_sha:
        raise ValueError(f"Cached checksum mismatch: {path}")
    if expected_size is not None and destination.stat().st_size != expected_size:
        raise ValueError(f"Cached size mismatch: {path}")
    return {"path": path, "bytes": destination.stat().st_size, "sha256": digest, "url": url}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path,
                        default=ROOT / "data/budgeted-microservice-rca/raw")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).parent / "results/data-audit.json")
    args = parser.parse_args()
    manifest = [download("cases.parquet", args.raw_dir / "cases.parquet", INDEX_SHA256)]
    index = pd.read_parquet(args.raw_dir / "cases.parquet")
    if len(index) != 735 or index["case"].duplicated().any():
        raise ValueError("Index count/uniqueness differs from pinned dataset")
    table = []
    for (dataset, suite, system), rows in index.groupby(["dataset", "suite", "system"]):
        table.append({"dataset": dataset, "suite": suite, "system": system,
                      "cases": len(rows), "root_services": int(rows.root_cause_service.nunique()),
                      "logs_available": int(rows.has_logs.sum()),
                      "traces_available": int(rows.has_traces.sum()),
                      "faults": rows.fault.value_counts().sort_index().to_dict(),
                      "metric_columns_min": int(rows.n_metrics.min()),
                      "metric_columns_max": int(rows.n_metrics.max())})
    samples = []
    for system in ("ob", "ss", "tt"):
        for suite in ("RE2", "RE3"):
            label = index[(index.system == system) & (index.suite == suite)].sort_values("case").iloc[0]
            case = label["case"]
            tree_url = f"https://huggingface.co/api/datasets/{DATASET}/tree/{REVISION}/{case}"
            response = requests.get(tree_url, timeout=60)
            response.raise_for_status()
            available = response.json()
            files = []
            sample = {"case": case, "dataset": label["dataset"],
                      "evaluation_only_root_service": label["root_cause_service"],
                      "evaluation_only_fault": label["fault"], "tables": {}}
            for entry in available:
                name = Path(entry["path"]).name
                if name not in ("inject_time.txt", "metrics.parquet", "logs.parquet", "traces.parquet"):
                    continue
                destination = args.raw_dir / entry["path"]
                record = download(entry["path"], destination,
                                  entry.get("lfs", {}).get("oid"), entry["size"])
                files.append(record)
                if name == "inject_time.txt":
                    if int(destination.read_text()) != int(label["inject_time"]):
                        raise ValueError(f"Injection timestamp differs from index: {case}")
                    continue
                started = time.perf_counter()
                frame = pd.read_parquet(destination)
                seconds = time.perf_counter() - started
                kind = name.removesuffix(".parquet")
                expected_rows = int(label[{"metrics": "n_timesteps", "logs": "n_logs",
                                           "traces": "n_traces"}[kind]])
                if len(frame) != expected_rows:
                    raise ValueError(f"Raw/index row count mismatch: {entry['path']}")
                sample["tables"][kind] = {
                    "rows": len(frame), "columns": len(frame.columns),
                    "schema_columns": frame.columns.tolist(),
                    "estimated_dataframe_bytes": int(frame.memory_usage(deep=True).sum()),
                    "parquet_bytes": record["bytes"], "local_read_seconds": seconds,
                }
                if kind == "metrics":
                    numeric = frame.drop(columns=["time"])
                    if numeric.shape[1] != int(label["n_metrics"]):
                        raise ValueError(f"Metric columns differ from index: {case}")
                    sample["tables"][kind]["null_fraction"] = float(numeric.isna().mean().mean())
                    before = frame.time < int(label["inject_time"])
                    sample["tables"][kind]["normal_rows"] = int(before.sum())
                    sample["tables"][kind]["faulty_rows"] = int((~before).sum())
                    if int(before.sum()) != int(label["normal_timesteps"]):
                        raise ValueError(f"Normal window differs from index: {case}")
                del frame
                gc.collect()
            manifest.extend(files)
            samples.append(sample)
            print(f"Verified {case}: {', '.join(sample['tables'])}", flush=True)
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    (args.raw_dir / "download-manifest.json").write_text(json.dumps({
        "dataset": DATASET, "revision": REVISION, "files": manifest,
    }, indent=2) + "\n")
    result = {
        "source": {"dataset": DATASET, "revision": REVISION, "license": "MIT",
                   "index_sha256": INDEX_SHA256},
        "audit_scope": "Complete index plus six deterministic representative raw cases; no training or accuracy results",
        "environment": {"python": platform.python_version(), "pandas": pd.__version__},
        "cases": len(index), "summary": table,
        "multi_source_cases": int(index.suite.isin(["RE2", "RE3"]).sum()),
        "cases_with_logs": int(index.has_logs.sum()),
        "cases_with_traces": int(index.has_traces.sum()),
        "evaluation_only_root_file_cases": int(index.has_root_cause_file.sum()),
        "samples": samples,
        "downloaded_bytes_including_index": sum(f["bytes"] for f in manifest),
        "warning": "Local read timings are feasibility observations, not a fair latency benchmark or production cost",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"cases": len(index), "sample_cases": len(samples),
                      "downloaded_bytes": result["downloaded_bytes_including_index"]}, indent=2))


if __name__ == "__main__":
    main()
