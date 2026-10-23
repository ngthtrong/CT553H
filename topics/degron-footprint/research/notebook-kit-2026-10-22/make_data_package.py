#!/usr/bin/env python3
"""Dựng gói dữ liệu `degron-data-v1.zip` cho notebook — CHỈ nguồn được phép phân phối lại.

Được phép: Zhang 2023 (CC BY 4.0) và cache dẫn xuất, Voutsinos 2026 (MIT), UniProt/AlphaFold (CC BY 4.0),
Degformer (Apache-2.0). TUYỆT ĐỐI KHÔNG: Koren 2018, MetaDegron, Larsen 2025, ClinVar thô — script
từ chối cứng theo tên đường dẫn và theo giấy phép khai báo.

Nguồn danh sách file:
  1. REGISTRY dưới đây (R0, R3, dùng chung);
  2. mọi file `research/*/data-needs.json` của từng thí nghiệm (R1, R2, ...), dạng
       {"experiment": "R1", "files": [{"path": "data/raw/...", "license": "Apache-2.0", "source": "..."}]}
     `path` tương đối từ topics/degron-footprint/. Thêm thí nghiệm mới KHÔNG cần sửa file này.

Chạy từ gốc repo (python -I):
  python3 -I .../make_data_package.py --list              # in danh sách + kích thước + giấy phép, KHÔNG ghi gì
  python3 -I .../make_data_package.py                     # ghi data/processed/packages/degron-data-v1.zip
  python3 -I .../make_data_package.py --only R0,R3        # gói con
Script không upload gì lên dịch vụ ngoài.
"""
import argparse
import hashlib
import json
import sys
import time
import zipfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
OUT_DIR = TOPIC / 'data/processed/packages'

ALLOWED_LICENSES = {'GEO public data (cite Zhang 2023)', 'CC BY 4.0', 'MIT', 'Apache-2.0', 'CC BY 4.0 (derived)', 'MIT (derived)',
                    'Apache-2.0 (derived)', 'CC BY 4.0 + MIT (derived)'}
DENY = ('koren', 'metadegron', 'larsen', 'clinvar', 'koren-2018', 'mendeley-files')

Z = 'Zhang et al. 2023, Mol Cell — Mendeley Data 10.17632/32h94v2yv2.2'
ZS = 'cache dẫn xuất từ Zhang 2023 (research/learning-curve, calibration-p6)'
UP = 'UniProtKB/Swiss-Prot người, release 2026_03'
SCAN = ('data/interim/zhang-scanning-unzip/I28 Scanning (Completed)/'
        'Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv')

# (đường dẫn tương đối topic, giấy phép, nguồn, thí nghiệm cần)
REGISTRY = [
    ('data/processed/learning-curve-sat-base.npz', 'CC BY 4.0 (derived)', ZS, ['R0', 'R1', 'R2', 'R5']),
    ('data/processed/learning-curve-sat-ext4.0.npz', 'CC BY 4.0 (derived)', ZS, ['R0', 'R1', 'R2', 'R5']),
    ('data/processed/calibration-p6-model.npz', 'CC BY 4.0 (derived)', ZS, ['R0', 'R5']),
    ('data/processed/calibration-p6-trainpath.npz', 'CC BY 4.0 (derived)', ZS, ['R0']),
    ('data/processed/calibration-p6-oof.npz', 'CC BY 4.0 (derived)', ZS, ['R0']),
    ('data/processed/psi-rep1.tsv', 'CC BY 4.0', Z, ['R0']),
    ('data/processed/r3-sat-wt-pool.tsv', 'CC BY 4.0 (derived)',
     'nhãn miền PSI(WT) nội tại của 235 peptide bão hòa (Zhang 2023); do r3-domain-gate/local_analysis.py dựng',
     ['R3']),
    ('data/processed/psi-sat_a.tsv', 'CC BY 4.0', Z, ['R0']),
    ('data/processed/psi-sat_b.tsv', 'CC BY 4.0', Z, ['R0']),
    (SCAN, 'CC BY 4.0', Z, ['R0']),
    ('data/interim/protein-id30-cov80_cluster.tsv', 'CC BY 4.0 (derived)',
     'MMseqs2 id30 cov80 trên UniProt (CC BY 4.0)', ['R0', 'R1', 'R2', 'R3', 'R5']),
    ('data/interim/protein-id30-cov80-proteome_cluster.tsv', 'CC BY 4.0 (derived)',
     'MMseqs2 id30 cov80 trên toàn snapshot UniProt (build_proteome_clusters.py)', ['R3']),
    ('data/interim/gps-peptidome-rep1.tsv', 'GEO public data (cite Zhang 2023)',
     'NCBI GEO GSE240610 Table S1, sheet I28 Control Replicate 1 (sàng peptidome GPS, Zhang 2023)', ['R3']),
    ('data/raw/human-reviewed-2026-10-12.fasta.gz', 'CC BY 4.0', UP, ['R0', 'R1', 'R2', 'R3', 'R5']),
    ('data/raw/human-reviewed-2026-10-12.fasta.manifest.json', 'CC BY 4.0', UP, ['R0', 'R3']),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def gather():
    ent = defaultdict(lambda: {'experiments': set()})
    for path, lic, src, exps in REGISTRY:
        e = ent[path]
        e.update(license=lic, source=src)
        e['experiments'] |= set(exps)
    for dn in sorted((TOPIC / 'research').glob('*/data-needs.json')):
        spec = json.loads(dn.read_text())
        for f in spec['files']:
            e = ent[f['path']]
            e.update(license=f['license'], source=f.get('source', str(dn.parent.name)))
            e['experiments'].add(spec['experiment'])
    problems = []
    for path, e in ent.items():
        low = path.lower()
        if any(w in low for w in DENY):
            problems.append(f'CẤM theo tên: {path}')
        if e['license'] not in ALLOWED_LICENSES:
            problems.append(f'giấy phép không được phép ({e["license"]}): {path}')
        if not (TOPIC / path).is_file():
            problems.append(f'thiếu file: {path}')
        if not path.startswith('data/'):
            problems.append(f'chỉ nhận file dưới data/: {path}')
    return ent, problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--only', default='', help='R0,R3 — chỉ file của các thí nghiệm này')
    ap.add_argument('--version', default='v1')
    a = ap.parse_args(argv)
    ent, problems = gather()
    if a.only:
        keep = set(a.only.split(','))
        ent = {p: e for p, e in ent.items() if e['experiments'] & keep}
    if problems:
        print('\n'.join('✘ ' + x for x in problems))
        return 1
    total = 0
    print(f'{"bytes":>12}  {"giấy phép":24} {"thí nghiệm":14} đường dẫn')
    for path in sorted(ent):
        e = ent[path]
        sz = (TOPIC / path).stat().st_size
        total += sz
        print(f'{sz:>12,d}  {e["license"]:24} {",".join(sorted(e["experiments"])):14} {path}')
    print(f'--- {len(ent)} file, {total/2**20:.1f} MB chưa nén · TUYỆT ĐỐI không có Koren/MetaDegron/Larsen/ClinVar')
    if a.list:
        return 0

    files = []
    for path in sorted(ent):
        p = TOPIC / path
        files.append({'path': path, 'sha256': sha256(p), 'bytes': p.stat().st_size,
                      'license': ent[path]['license'], 'source': ent[path]['source'],
                      'experiments': sorted(ent[path]['experiments'])})
    by_exp = defaultdict(list)
    for f in files:
        for x in f['experiments']:
            by_exp[x].append(f['path'])
    manifest = {'package': f'degron-data-{a.version}', 'version': a.version,
                'created': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'note': 'Chỉ nguồn được phép phân phối lại; xem data/README.md. Không upload khi chưa duyệt.',
                'files': files, 'experiments': dict(by_exp)}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    name = f'degron-data-{a.version}.zip'
    zp = OUT_DIR / name
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr('DATA_MANIFEST.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
        for f in files:
            z.write(TOPIC / f['path'], f'topics/degron-footprint/{f["path"]}')
    digest = sha256(zp)
    (OUT_DIR / (name + '.sha256')).write_text(f'{digest}  {name}\n')
    print(f'✔ {zp.relative_to(TOPIC)}  {zp.stat().st_size/2**20:.1f} MB nén  sha256={digest}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
