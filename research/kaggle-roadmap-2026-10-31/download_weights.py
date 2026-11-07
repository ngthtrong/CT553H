"""Download pinned official model assets without importing any model code.

Resumable files, SHA256 verification against HF LFS metadata, atomic status updates.
Only one PyTorch/safetensors format is retained, never duplicate TF/Flax weights.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import shutil
import threading
import time

import requests

HERE = Path(__file__).resolve().parent
TOPIC = next((p for p in HERE.parents if (p / 'data/README.md').exists()), None)
ROOT = next((p for p in HERE.parents if (p / 'CLAUDE.md').exists()), HERE)
DEFAULT = TOPIC / 'data/raw/plm-weights-v3' if TOPIC else Path('/kaggle/working/plm-weights-v3')
PRINT_LOCK = threading.Lock()
USE_HUB = False


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, path)


def emit(*args):
    with PRINT_LOCK:
        print(*args, flush=True)


def request(url, **kwargs):
    for attempt in range(6):
        try:
            r = requests.get(url, timeout=(30, 120), **kwargs)
            if r.status_code in (429, 500, 502, 503, 504):
                r.close()
                time.sleep(min(2 ** attempt, 20))
                continue
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt == 5:
                raise
            time.sleep(min(2 ** attempt, 20))
    raise RuntimeError('HTTP retry budget exhausted')


def select_files(siblings):
    names = {f['rfilename'] for f in siblings}
    if 'model.safetensors.index.json' in names:
        weights = {n for n in names if n.endswith('.safetensors')}
        weights.add('model.safetensors.index.json')
    elif 'model.safetensors' in names:
        weights = {'model.safetensors'}
    elif 'pytorch_model.bin.index.json' in names:
        weights = {n for n in names if n.endswith('.bin') and 'pytorch_model' in n}
        weights.add('pytorch_model.bin.index.json')
    elif 'pytorch_model.bin' in names:
        weights = {'pytorch_model.bin'}
    else:
        raise ValueError('No supported complete PyTorch/safetensors checkpoint')
    meta = {n for n in names if '/' not in n and (
        n.endswith(('.json', '.txt', '.model')) or n.lower().startswith(('readme', 'license', 'notice')))}
    # Remote .py code is deliberately not downloaded or executed.
    keep = weights | meta
    return [f for f in siblings if f['rfilename'] in keep]


def expected_sha(entry):
    return (entry.get('lfs') or {}).get('sha256')


def valid_file(path, entry):
    if not path.is_file() or path.stat().st_size != entry['size']:
        return False
    sha = expected_sha(entry)
    if sha:
        return digest(path) == sha
    # HF small-file blob ID is git SHA1, not plain SHA1.
    if entry.get('blobId'):
        h = hashlib.sha1(f'blob {entry["size"]}\0'.encode())
        h.update(path.read_bytes())
        return h.hexdigest() == entry['blobId']
    return True


def fetch_file(repo, revision, entry, folder, cache_root):
    relative = Path(entry['rfilename'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Unsafe remote path')
    target = folder / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if valid_file(target, entry):
        return dict(path=str(relative), bytes=target.stat().st_size,
                    sha256=digest(target), verified=True, reused=True)
    sha = expected_sha(entry)
    blob = cache_root / ('models--' + repo.replace('/', '--')) / 'blobs' / str(sha)
    if sha and valid_file(blob, entry):
        shutil.copyfile(blob, target)
    elif USE_HUB:
        from huggingface_hub import hf_hub_download
        hf_hub_download(repo_id=repo, filename=relative.as_posix(), revision=revision,
                        local_dir=folder, token=False)
        if not valid_file(target, entry):
            raise ValueError(f'Hub asset hash mismatch: {relative}')
    else:
        part = target.with_suffix(target.suffix + '.partial')
        for attempt in range(8):
            offset = part.stat().st_size if part.exists() else 0
            if offset == entry['size']:
                break
            if offset > entry['size']:
                raise ValueError('Partial asset is larger than expected')
            url = f'https://huggingface.co/{repo}/resolve/{revision}/{relative.as_posix()}'
            try:
                with request(url, stream=True, headers={'Range': f'bytes={offset}-'} if offset else {}) as r:
                    append = bool(offset and r.status_code == 206)
                    if append and not r.headers.get('Content-Range', '').startswith(f'bytes {offset}-'):
                        raise ValueError('Range response offset mismatch')
                    with part.open('ab' if append else 'wb') as f:
                        for chunk in r.iter_content(chunk_size=4 << 20):
                            if chunk:
                                f.write(chunk)
                if part.stat().st_size == entry['size']:
                    break
            except requests.RequestException:
                if attempt == 7:
                    raise
                time.sleep(min(2 ** attempt, 20))
        if not valid_file(part, entry):
            raise ValueError(f'Integrity mismatch: {relative}; partial retained for investigation')
        os.replace(part, target)
    return dict(path=str(relative), bytes=target.stat().st_size,
                sha256=digest(target), hf_lfs_sha256=sha, verified=True, reused=False)


def download_one(model, out, cache_root, metadata_only=False):
    key, repo = model['id'], model['checkpoint']
    report = dict(model_id=key, requested_repo=repo, status='resolving', files=[])
    try:
        previous_status = out / key / 'status.json'
        if metadata_only and previous_status.exists():
            previous = json.loads(previous_status.read_text())
            if previous.get('status') == 'complete':
                return previous
        pinned = model.get('checkpoint_revision')
        suffix = f'/revision/{pinned}' if pinned else ''
        meta = request(f'https://huggingface.co/api/models/{repo}{suffix}?blobs=true').json()
        repo, revision = meta['id'], meta['sha']
        selected = select_files(meta['siblings'])
        folder = out / key / revision
        folder.mkdir(parents=True, exist_ok=True)
        report.update(repo=repo, revision=revision, bytes_expected=sum(f['size'] for f in selected),
                      path=folder.relative_to(ROOT).as_posix() if folder.is_relative_to(ROOT) else str(folder),
                      license_metadata=(meta.get('cardData') or {}).get('license'),
                      remote_metadata=meta, status='metadata_ready')
        save(out / key / 'status.json', report)
        emit(key, revision[:12], f'{report["bytes_expected"]/2**30:.2f} GiB', 'metadata')
        if metadata_only:
            return report
        if shutil.disk_usage(out).free < report['bytes_expected'] + (10 << 30):
            raise OSError('Insufficient disk headroom for this model plus 10 GiB reserve')
        report['status'] = 'downloading'
        save(out / key / 'status.json', report)
        for entry in selected:
            result = fetch_file(repo, revision, entry, folder, cache_root)
            report['files'].append(result)
            save(out / key / 'status.json', report)
            if entry['size'] > (20 << 20):
                emit(key, entry['rfilename'], f'{entry["size"]/2**30:.2f} GiB', 'verified')
        report.update(status='complete', bytes_verified=sum(f['bytes'] for f in report['files']))
        (out / key / 'SOURCE.md').write_text(
            f'# {key}\n\nOfficial source: https://huggingface.co/{repo}\n\n'
            f'Pinned revision: `{revision}`. Files and SHA-256: status.json.\n'
            'Weights are data, not repository source. Remote Python code was not downloaded/executed.\n'
            'Terms and model card belong to the pinned snapshot; download does not select this model.\n')
        emit(key, 'COMPLETE')
    except Exception as exc:
        report.update(status='download_failed', error=f'{type(exc).__name__}: {exc}')
        emit(key, 'FAILED', report['error'][:250])
    save(out / key / 'status.json', report)
    return report


def main():
    global USE_HUB
    ap = argparse.ArgumentParser()
    ap.add_argument('--models', default='all')
    ap.add_argument('--out', type=Path, default=DEFAULT)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--metadata-only', action='store_true')
    ap.add_argument('--backend', choices=['http', 'hub'], default='http')
    ap.add_argument('--small-first', action='store_true', help='Prioritize complete smaller checkpoints before large ones')
    args = ap.parse_args()
    registry = json.loads((HERE / 'model-registry.json').read_text())
    models = registry['models']
    if args.models != 'all':
        chosen = set(args.models.split(','))
        models = [m for m in models if m['id'] in chosen]
        assert {m['id'] for m in models} == chosen, 'Unknown model ID'
    args.out.mkdir(parents=True, exist_ok=True)
    if args.small_first:
        def expected_size(m):
            status = args.out / m['id'] / 'status.json'
            return json.loads(status.read_text()).get('bytes_expected', float('inf')) if status.exists() else float('inf')
        models.sort(key=expected_size)
    USE_HUB = args.backend == 'hub'
    os.environ['HF_HOME'] = str(args.out / '.hf-home')
    os.environ['HF_XET_CACHE'] = str(args.out / '.xet')
    os.environ['HF_XET_HIGH_PERFORMANCE'] = '1'
    reports = []
    cache = Path.home() / '.cache/huggingface/hub'
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(download_one, m, args.out, cache, args.metadata_only) for m in models]
        for future in as_completed(futures):
            reports.append(future.result())
            save(args.out / 'download-summary.json', dict(schema_version=1, models=reports))
    save(args.out / 'weights-status.json', dict(schema_version=1, metadata_only=args.metadata_only,
         models=[{k: v for k, v in r.items() if k != 'remote_metadata'} for r in reports]))
    print('FINISHED', {s: sum(r['status'] == s for r in reports) for s in {r['status'] for r in reports}})


if __name__ == '__main__':
    main()
