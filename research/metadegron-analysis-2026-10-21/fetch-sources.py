"""Download inert source documents only; never import or execute third-party code."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import json
import urllib.request
import urllib.error
import sys

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
RAW = TOPIC / 'data' / 'raw' / 'metadegron'
SOURCES = {
    'paper.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11491831/fullTextXML',
    'paper.html': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/',
    'publisher.html': 'https://academic.oup.com/bib/article/25/6/bbae519/7828723',
    'pmc-oa.xml': 'https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC11491831',
    'web-home-http.html': 'http://modinfor.com/MetaDegron/',
    'web-home-https.html': 'https://modinfor.com/MetaDegron/',
    'web-download.html': 'http://modinfor.com/MetaDegron/Download.php',
    'web-tutorial.html': 'http://modinfor.com/MetaDegron/Tutorial.php',
    'web-statistics.html': 'http://modinfor.com/MetaDegron/Statistics.php',
    'web-terms.html': 'http://modinfor.com/MetaDegron/Terms.php',
    'seqvec-weights-access.txt': 'http://modinfor.com/MetaDegron/Download/weights.hdf5',
    'embedding-access.txt': 'http://modinfor.com/MetaDegron/Download/all_train_embedding.npy',
    'github-metadata.json': 'https://api.github.com/repos/BioDataStudy/MetaDegron',
}

def fetch(item):
    name, url = item
    dest = RAW / name
    row = {'url': url, 'path': str(dest.relative_to(ROOT)), 'client_date': '2026-10-21',
           'attempted_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'license': 'chưa xác nhận', 'downloaded': False}
    if dest.exists():
        data = dest.read_bytes()
        row.update(downloaded=True, cache=True, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        return row
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CT553H research audit contact via repository'})
        with urllib.request.urlopen(req, timeout=18) as response:
            data = response.read(20_000_001)
            row.update(status=response.status, final_url=response.url,
                       content_type=response.headers.get('Content-Type'))
        if len(data) > 20_000_000:
            row['error'] = 'Safety size limit 20 MB: no payload retained'
        else:
            dest.write_bytes(data)
            row.update(downloaded=True, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        row['error'] = f'{type(exc).__name__}: {exc}'
    return row

if __name__ == '__main__':
    output = 'source-access.json'
    if len(sys.argv) > 1:
        SOURCES = json.loads(Path(sys.argv[1]).read_text())
        output = Path(sys.argv[1]).stem + '-access.json'
    RAW.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, SOURCES.items()))
    (HERE / output).write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(json.dumps([{k: r.get(k) for k in ('path', 'status', 'downloaded', 'error')} for r in rows], ensure_ascii=False))
