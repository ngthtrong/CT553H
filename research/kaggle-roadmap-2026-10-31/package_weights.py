"""Package only verified complete pretrained weights as a separate Kaggle input."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(8<<20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--models', default='esm2_8m,esm2_35m,esm2_650m')
    args = ap.parse_args(); root = TOPIC/'data/raw/plm-weights-v3'
    files, locks = [], []
    for key in args.models.split(','):
        p = root/key/'status.json'; d = json.loads(p.read_text())
        assert d['status'] == 'complete', f'{key}: incomplete assets cannot be packaged'
        files.append(p); locks.append(dict(model_id=key, revision=d['revision'], status_sha256=sha(p)))
        for f in d['files']:
            asset = p.parent/d['revision']/f['path']
            assert asset.stat().st_size == f['bytes'] and sha(asset) == f['sha256'], asset
            files.append(asset)
        if (p.parent/'SOURCE.md').exists(): files.append(p.parent/'SOURCE.md')
    identity = hashlib.sha256(json.dumps(locks, sort_keys=True).encode()).hexdigest()[:12]
    out = TOPIC/'data/processed/packages'/f'degron-weights-v3-{identity}.zip'
    # Weights are already dense binary; STORE avoids CPU-heavy duplicate compression.
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
        for p in files:
            z.write(p, 'plm-weights-v3/'+p.relative_to(root).as_posix())
    checksum = sha(out)
    out.with_suffix('.zip.sha256').write_text(f'{checksum}  {out.name}\n')
    (HERE/'weights-build.json').write_text(json.dumps(dict(zip=str(out.relative_to(TOPIC.parent.parent)),
        bytes=out.stat().st_size, sha256=checksum, models=locks), indent=2)+'\n')
    print(out, out.stat().st_size)


if __name__ == '__main__':
    main()
