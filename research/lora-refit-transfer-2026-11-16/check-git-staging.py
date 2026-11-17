"""Check staged Git blobs without changing the index, hooks, config or history.

Policy for new work: <=10 MiB per file, <=25 MiB per staged set, no raw data,
weights/checkpoints/prediction arrays/archives in the branch-1 experiment.
Existing unchanged historical files are not inspected as new additions.
"""
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'CLAUDE.md').is_file())
EXPERIMENT = 'research/lora-refit-transfer-2026-11-16/'
OUTPUT = 'research/kaggle-roadmap-2026-10-31/output/'
BINARY_SUFFIXES = {'.pt', '.pth', '.pkl', '.pickle', '.joblib', '.safetensors', '.ckpt',
                   '.npy', '.npz', '.parquet', '.arrow', '.bin', '.db', '.sqlite', '.sqlite3',
                   '.zip', '.tar', '.gz', '.7z', '.xlsx'}


def git(*args, input_bytes=None):
    return subprocess.check_output(['git', *args], cwd=ROOT, input=input_bytes)


def inspect():
    unresolved = git('ls-files', '--unmerged', '-z')
    if unresolved:
        return dict(status='fail', reasons=['Unresolved index entries'], files=[], bytes=0)
    changed = [x.decode('utf8') for x in git('diff', '--cached', '--name-only',
               '--diff-filter=ACMRT', '-z', '--no-renames').split(b'\0') if x]
    entries = {}
    for row in filter(None, git('ls-files', '--stage', '-z').split(b'\0')):
        metadata, raw_path = row.split(b'\t', 1)
        mode, oid, stage = metadata.decode().split()
        if stage == '0':
            entries[raw_path.decode('utf8')] = (mode, oid)
    objects = [entries[name][1] for name in changed]
    sizes = {}
    if objects:
        raw = git('cat-file', '--batch-check=%(objectname) %(objectsize)',
                  input_bytes=('\n'.join(objects) + '\n').encode())
        sizes = {row.split()[0]: int(row.split()[1]) for row in raw.decode().splitlines()}
    files, reasons = [], []
    for name in changed:
        mode, oid = entries[name]
        size = sizes[oid]
        files.append(dict(path=name, bytes=size))
        path = PurePosixPath(name)
        suffixes = {suffix.lower() for suffix in path.suffixes}
        if size > 10 * 2**20:
            reasons.append(f'File exceeds 10 MiB: {name}')
        if mode == '160000':
            reasons.append(f'Nested Git repository: {name}')
        if 'data' in path.parts and path.name not in {'README.md', 'SOURCE.md'}:
            reasons.append(f'Data payload: {name}')
        if suffixes & {'.pt', '.pth', '.pkl', '.pickle', '.joblib', '.safetensors', '.ckpt'}:
            reasons.append(f'Model/checkpoint: {name}')
        if name.startswith((EXPERIMENT, OUTPUT)) and suffixes & BINARY_SUFFIXES:
            reasons.append(f'Heavy experiment payload: {name}')
        if name.startswith(EXPERIMENT + 'local/'):
            reasons.append(f'Local-only branch-1 artifact: {name}')
        if any(part in {'.venv', '__pycache__', '.data'} for part in path.parts):
            reasons.append(f'Runtime/cache directory: {name}')
        if name.startswith(OUTPUT) and path.name in {'STOP', 'session.json', 'progress.json', 'latest.json'}:
            # Historical per-job progress is allowed; mutable campaign progress is not.
            if path.name != 'progress.json' or 'jobs' not in path.parts:
                reasons.append(f'Mutable campaign control file: {name}')
    total = sum(item['bytes'] for item in files)
    if total > 25 * 2**20:
        reasons.append('Staged set exceeds 25 MiB')
    return dict(status='fail' if reasons else 'pass', files=files, bytes=total, reasons=reasons,
                scope='changed index blobs only; no history, remote or licensing audit')


if __name__ == '__main__':
    result = inspect()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'pass' else 1)
