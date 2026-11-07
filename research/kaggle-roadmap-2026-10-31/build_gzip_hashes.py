"""Pin expanded gzip bytes from the checksum-verified existing core ZIP.

Does not rewrite the core data, archive or DATA_MANIFEST.json.
"""
import gzip
import hashlib
import json
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p/'data/README.md').exists())
sys.path.insert(0, str(HERE))
from degron_v3.common import sha256, atomic_json


def main():
    build = json.loads((HERE/'dataset-build.json').read_text())
    archive = TOPIC/'data/processed/packages/degron-data-v3-fullpsi.zip'
    assert sha256(archive) == build['sha256'], 'Original core ZIP checksum mismatch'
    files = []
    with zipfile.ZipFile(archive) as z:
        prefix = 'degron-data-v3-fullpsi/'
        manifest_bytes = z.read(prefix+'DATA_MANIFEST.json')
        manifest = json.loads(manifest_bytes)
        for entry in manifest['files']:
            if not entry['path'].endswith('.gz'):
                continue
            compressed = z.read(prefix+entry['path'])
            assert hashlib.sha256(compressed).hexdigest() == entry['sha256']
            content = gzip.decompress(compressed)
            files.append(dict(path=entry['path'], gzip_sha256=entry['sha256'],
                content_bytes=len(content), content_sha256=hashlib.sha256(content).hexdigest()))
    atomic_json(HERE/'degron_v3/gzip-content-hashes.json', dict(schema_version=1,
        source_archive_sha256=build['sha256'],
        data_manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(), files=files))
    print(f'Pinned decompressed SHA-256 for {len(files)} gzip members; core bundle unchanged')


if __name__ == '__main__':
    main()
