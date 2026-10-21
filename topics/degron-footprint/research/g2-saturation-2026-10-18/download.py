"""Download pinned Degformer source/weights; never execute downloaded source."""
import json,hashlib,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
TOPIC=next(p for p in HERE.parents if (p/'data'/'README.md').exists())
out=TOPIC/'data/raw/degformer-isolated';out.mkdir(parents=True,exist_ok=True)
m=json.loads((HERE/'source-manifest.json').read_text())
for name,meta in m['files'].items():
    p=out/name
    b=p.read_bytes() if p.exists() else urllib.request.urlopen(meta['url']).read()
    assert hashlib.sha256(b).hexdigest()==meta['sha256'],name
    if not p.exists():p.write_bytes(b)
(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('All pinned source hashes verified:',m['commit'])
