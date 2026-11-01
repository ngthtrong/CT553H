"""Build a portable, allow-listed v3 code ZIP, without local data/weights/paths."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    names = ['README.md', 'RUN.md', 'ALL-IN-ONE.md', 'MULTI-SESSION.md', 'DATASET.md', 'NOTEBOOKS.md', 'EXECUTION-PROTOCOL.md',
        'PROTOCOL.md', 'MODEL-CATALOG.md', 'VALIDATION.md', 'requirements-kaggle.txt',
        'model-registry.json', 'package-spec.json', 'coverage.csv', 'run_stage.py',
        'download_weights.py', 'make_notebooks.py', 'make_all_in_one.py', 'merge_features.py', 'package_code.py',
        'build_gzip_hashes.py', 'validate_data_transport.py', 'data-transport-validation.json',
        'degron_v3/gzip-content-hashes.json',
        'dataset-build.json', 'notebook-validation.json', 'training-smoke.json',
        'invariant-validation.json', 'weights-status.json', 'weights-build.json', 'all-in-one-validation.json',
        'multi-session-validation.json', 'session-plan-example.json']
    files = [HERE/n for n in names]+sorted((HERE/'degron_v3').glob('*.py'))+sorted((HERE/'notebooks').glob('*.ipynb'))
    virtual = {'code-build.json': (json.dumps(dict(status='checksum_is_outside_archive',
        note='For the archive checksum read the accompanying .zip.sha256; CODE_MANIFEST verifies extracted files.'), indent=2)+'\n').encode()}
    manifest = dict(schema_version=3, bundle_id='degron-code-v3', role='trusted_code',
        protocol_sha256=sha(HERE/'EXECUTION-PROTOCOL.md'),
        files=[dict(path=p.relative_to(HERE).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    manifest['files'] += [dict(path=name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
                          for name, content in virtual.items()]
    content = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
    identity = hashlib.sha256(content).hexdigest()
    out = TOPIC/'data/processed/packages'; out.mkdir(exist_ok=True)
    target = out/f'degron-code-v3-{identity[:12]}.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('degron-code-v3/CODE_MANIFEST.json', content)
        for p in files:
            z.write(p, 'degron-code-v3/'+p.relative_to(HERE).as_posix())
        for name, value in virtual.items():
            z.writestr('degron-code-v3/'+name, value)
    target.with_suffix('.zip.sha256').write_text(f'{sha(target)}  {target.name}\n')
    (HERE/'code-build.json').write_text(json.dumps(dict(zip=str(target.relative_to(TOPIC.parent.parent)),
        bytes=target.stat().st_size, sha256=sha(target), manifest_sha256=identity,
        protocol_sha256=manifest['protocol_sha256'], files=len(manifest['files'])), indent=2)+'\n')
    print(target, target.stat().st_size)


if __name__ == '__main__':
    main()
