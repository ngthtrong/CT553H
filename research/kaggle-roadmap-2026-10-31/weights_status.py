"""Refresh a portable inventory of model downloads; partial bytes are never verified weights."""
import argparse
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8<<20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    root = TOPIC/'data/raw/plm-weights-v3'
    models = json.loads((HERE/'model-registry.json').read_text())['models']
    rows = []
    for spec in models:
        folder = root/spec['id']; path = folder/'status.json'
        status = json.loads(path.read_text()) if path.exists() else {'status': 'not_started'}
        record = dict(model_id=spec['id'], repo=spec['checkpoint'], revision=spec['checkpoint_revision'],
            source=f'https://huggingface.co/{spec["checkpoint"]}/tree/{spec["checkpoint_revision"]}',
            status=status['status'], bytes_expected=status.get('bytes_expected'),
            license_metadata=status.get('license_metadata'), files=status.get('files', []),
            partial_bytes=sum(p.stat().st_size for p in folder.rglob('*.partial')) if folder.exists() else 0)
        if record['status'] == 'complete':
            assert status['revision'] == spec['checkpoint_revision']
            for f in record['files']:
                asset = folder/status['revision']/f['path']
                assert asset.is_file() and asset.stat().st_size == f['bytes']
                if args.verify:
                    assert digest(asset) == f['sha256'], asset
            record['bytes_verified_complete'] = sum(f['bytes'] for f in record['files'])
            record['verification'] = 'sha256_rechecked' if args.verify else 'size_rechecked_downloader_hashes_recorded'
        rows.append(record)
    counts = {s: sum(r['status'] == s for r in rows) for s in sorted(set(r['status'] for r in rows))}
    result = dict(schema_version=2, snapshot_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        status_counts=counts, requested_models=len(rows),
        total_expected_bytes=sum(r.get('bytes_expected') or 0 for r in rows),
        verified_complete_bytes=sum(r.get('bytes_verified_complete', 0) for r in rows),
        partial_bytes=sum(r['partial_bytes'] for r in rows),
        note='Snapshot only. Only complete models can load. Metadata_ready means queued/resolved, not downloaded. '
             'Download log/job/status files live under data/raw/plm-weights-v3; rerun this script to refresh.',
        models=rows)
    (HERE/'weights-status.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(result['snapshot_utc'], counts, 'expected GiB', round(result['total_expected_bytes']/2**30, 2),
          'complete GiB', round(result['verified_complete_bytes']/2**30, 2), 'partial GiB', round(result['partial_bytes']/2**30, 2))


if __name__ == '__main__':
    main()
