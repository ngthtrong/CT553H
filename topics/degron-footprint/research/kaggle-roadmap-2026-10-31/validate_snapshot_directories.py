"""Regression check: Kaggle expands snapshot ZIPs, then users resume the directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'CLAUDE.md').exists())
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


CHILD = '''import hashlib,json,sys,zipfile
from pathlib import Path
import nbformat
notebook, source, output, report = map(Path, sys.argv[1:])
nb=nbformat.read(notebook,as_version=4)
ns={"__name__":"__main__","display":lambda frame:None}
exec(nb.cells[2].source,ns)
ns.update(INSTALL_DEPENDENCIES=False,AUTO_DOWNLOAD=False,SMOKE=True,
    OUTPUT_ROOT=str(output),DATA_DIR=str(Path.cwd()/"topics/degron-footprint/data/processed/v3-fullpsi"),
    OVERRIDES={"00":{"reproduce_legacy":True}},RESUME_FROM=str(source))
exec(nb.cells[4].source,ns)
exec(nb.cells[6].source,ns)
p=ns["pipeline"]
assert not (p.root/"SNAPSHOT.json").exists()
assert list((p.root/"resume-indexes").glob("*.json"))
assert p.executed==0 and len(p.state["tasks"])==11
assert all(t["status"]=="complete" for t in p.state["tasks"].values())
assert p.task_path("03-esm2_8m") is not None
export=p.export(include_features=True)
assert export["status"]=="exported"
with zipfile.ZipFile(export["archive"]) as z:
    assert z.namelist().count("SNAPSHOT.json")==1
    index=json.loads(z.read("SNAPSHOT.json"))
    assert any(f["path"].endswith("pool.npy") for f in index["files"])
    assert any(f["path"].endswith("crop.npy") for f in index["files"])
    for f in index["files"]:
        assert hashlib.sha256(z.read(f["path"])).hexdigest()==f["sha256"]
Path(report).write_text(json.dumps(dict(plan_id=p.plan_id,archive=export["archive"],
    single_fresh_snapshot_index=True,feature_arrays_retained=True,tasks_retained=11,training_jobs_executed=0)))
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, default=TOPIC/'data/processed/v3-validation/snapshot-directories')
    args = ap.parse_args(); args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    source = args.out/'input-1'
    assert not source.exists(), 'Use a fresh regression output folder'
    shutil.copytree(args.source.resolve(), source)
    manifest = json.loads((source/'pipeline-manifest.json').read_text())
    files = [p for p in sorted(source.rglob('*')) if p.is_file() and p.name != 'SNAPSHOT.json']
    (source/'SNAPSHOT.json').write_text(json.dumps(dict(plan_id=manifest['plan_id'],include_features=True,
        files=[dict(path=p.relative_to(source).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files])))
    checks = []
    for round_id in (1, 2):
        result_path = args.out/f'round-{round_id}.json'
        result = subprocess.run([sys.executable, '-I', '-c', CHILD,
            str(HERE/'notebooks/12-all-in-one.ipynb'), str(source), str(args.out/f'working-{round_id}'), str(result_path)],
            cwd=ROOT, env=dict(os.environ, OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', HF_HUB_OFFLINE='1'),
            capture_output=True, text=True, timeout=120)
        print('round', round_id, 'exit', result.returncode, flush=True)
        if result.returncode:
            print(result.stdout[-3000:]); print(result.stderr[-5000:]); raise SystemExit(1)
        report = json.loads(result_path.read_text())
        assert report['plan_id'] == manifest['plan_id'], 'Original campaign ID changed'
        checks.append({k:v for k,v in report.items() if k!='archive'})
        if round_id == 1:
            source = args.out/'input-2'
            with zipfile.ZipFile(report['archive']) as z: z.extractall(source)
    output = dict(status='pass', original_campaign_id=manifest['plan_id'],
        notebook_sha256=sha(HERE/'notebooks/12-all-in-one.ipynb'),rounds=checks,
        note='Actual notebook bootstrap tested with extracted snapshot directories; no retraining required.')
    (HERE/'multi-session-validation.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__': main()
