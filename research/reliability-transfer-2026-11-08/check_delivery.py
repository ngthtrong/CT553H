"""Check the finished CPU package and inventory its reviewable artifacts."""
import ast
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/"CLAUDE.md").exists())


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    required = ["PROTOCOL.md", "config.json", "analyze.py", "validate.py", "plot.py", "write_report.py",
                "requirements-analysis.txt", "input-manifest.json", "results.json", "runtime.json", "validation.json",
                "README.md", "NEXT-EVALUATION.md", "AMENDMENTS.md", "diagnostics.png", "figure-manifest.json", "visual-review.json"]
    for name in required:
        assert (HERE/name).is_file() and (HERE/name).stat().st_size > 0, name
    for p in HERE.glob("*.py"):
        ast.parse(p.read_text())
    validation = json.loads((HERE/"validation.json").read_text())
    results = json.loads((HERE/"results.json").read_text())
    runtime = json.loads((HERE/"runtime.json").read_text())
    inputs = json.loads((HERE/"input-manifest.json").read_text())
    figure = json.loads((HERE/"figure-manifest.json").read_text())
    visual = json.loads((HERE/"visual-review.json").read_text())
    assert validation["status"] == "pass"
    assert validation["validator_sha256"] == sha(HERE/"validate.py")
    assert validation["result_sha256"] == sha(HERE/"results.json")
    for name, record in validation["output_hashes"].items():
        assert sha(HERE/name) == record["sha256"], name
    for name, record in inputs["files"].items():
        assert (ROOT/name).stat().st_size == record["bytes"] and sha(ROOT/name) == record["sha256"], name
    assert figure["generator_sha256"] == sha(HERE/"plot.py")
    for name, expected in figure["sources"].items():
        assert sha(HERE/name) == expected, name
    assert sha(HERE/figure["output"]["path"]) == figure["output"]["sha256"]
    assert visual["figure_sha256"] == sha(HERE/"diagnostics.png") and visual["status"] == "pass"
    assert runtime["gpu_execution"] is False and runtime["forbidden_model_runtimes_imported"] == []
    assert results["pending"]["lora_T"] == "not_evaluated_no_saved_predictions"
    links = 0
    for p in [*HERE.glob("*.md"), ROOT/"research/README.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            if re.match(r"[a-z]+://", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            assert (p.parent/target).exists(), (str(p), target)
            links += 1
    # Whitespace check includes new files, which git diff --check alone omits.
    for p in [*HERE.glob("*.py"), *HERE.glob("*.md"), *HERE.glob("*.json"), HERE/"requirements-analysis.txt"]:
        assert all(line == line.rstrip() for line in p.read_text().splitlines()), p
    # Package entries preserve large local analysis detail via an explicit ignore.
    ignored = subprocess.run(["git", "check-ignore", "--no-index", str(HERE/"local/threshold-per-peptide.csv")],
                             cwd=ROOT, text=True, capture_output=True)
    assert ignored.returncode == 0, "Large local threshold detail is not ignored"
    record = dict(status="pass", checked_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
                  required_artifacts=required, numerical_validation_groups=len(validation["checks"]),
                  upstream_input_files_rehashed=len(inputs["files"]), relative_links_checked=links,
                  new_source_syntax_and_whitespace="pass", figure="source_hashes_and_session_visual_review_match",
                  figure_visual_inspection_note="See visual-review.json; this checker does not perform a visual review.",
                  gpu_execution=False, training=False, model_inference=False, local_detail_ignored=True,
                  scope="CPU diagnostic deliverables; LoRA T, external validation and serving remain explicitly pending.")
    (HERE/"delivery-validation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n")
    files = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(HERE.iterdir())
             if p.is_file() and p.name != "artifact-manifest.json"}
    (HERE/"artifact-manifest.json").write_text(json.dumps(dict(files=files,
                 excluded=["artifact-manifest.json (self)", "local/", "__pycache__/"],
                 scope="CPU diagnostic source, protocol and reviewable outputs; no upstream artifact copied or modified."), indent=2)+"\n")
    print(f"PASS delivery: {len(files)} artifacts, {links} local links, {len(inputs['files'])} unchanged source files")


if __name__ == "__main__":
    main()
