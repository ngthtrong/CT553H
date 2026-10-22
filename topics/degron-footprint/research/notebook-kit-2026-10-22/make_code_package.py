#!/usr/bin/env python3
"""Dựng gói mã `degron-code-<commit>[-dirty].zip` cho notebook — từ WORKING TREE (không phải git archive),
vì nhiều thay đổi chưa commit. Ghi SHA-256 từng file, git commit, cờ dirty vào CODE_MANIFEST.json;
SHA-256 của chính file zip ghi ra file cạnh nó (`.sha256`).

Chạy từ gốc repo (python -I):
  python3 -I topics/degron-footprint/research/notebook-kit-2026-10-22/make_code_package.py
  python3 -I .../make_code_package.py --list            # chỉ in danh sách + kích thước, không ghi gì
  python3 -I .../make_code_package.py --extra "topics/degron-footprint/research/xyz"

Gói chỉ chứa mã/PROTOCOL/kết quả nhỏ của đề tài (bộ cho phép ở INCLUDE_GLOBS). KHÔNG bao giờ chứa
Koren, MetaDegron, Larsen, ClinVar. Không upload gì — chỉ ghi file vào data/processed/packages/.
"""
import argparse
import fnmatch
import hashlib
import json
import subprocess
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
TOPIC_REL = TOPIC.relative_to(ROOT).as_posix()
OUT_DIR = TOPIC / 'data/processed/packages'

# thư mục con của research/ được đưa vào gói (glob theo tên thư mục)
INCLUDE_GLOBS = ['residue-task-derisk-*', 'g2-saturation-*', 'g2-extension-*', 'pap-baseline',
                 'learning-curve-*', 'calibration-p6-*', 'pretrain-p3-*', 'recluster-sensitivity-*',
                 'notebook-kit-*', 'r[0-9]-*']
ALLOW_EXT = {'.py', '.md', '.json', '.ipynb', '.txt', '.sh', '.yaml', '.yml', '.csv', '.tsv'}
MAX_FILE = 3 * 1024 * 1024
DENY = ('koren', 'metadegron', 'larsen', 'clinvar', '__pycache__', '.pyc', '.log', '.pt', '.pkl',
        'packages/')
# Hai marker CHỈ là stub: CLAUDE.md thật chứa thông tin cá nhân/GVHD, data/README.md thật là sổ nguồn gốc
# đầy đủ — không cần và không nên đưa lên dịch vụ ngoài.
STUBS = {'CLAUDE.md': '# Workspace tạm cho notebook (stub). Marker để script tìm ROOT.\n',
         f'{TOPIC_REL}/data/README.md': '# Workspace tạm cho notebook (stub). Marker để script tìm TOPIC;\n'
                                       'sổ nguồn gốc thật nằm ở repo, không đi cùng gói.\n'}


def git(*args):
    try:
        return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True,
                              check=True).stdout.strip()
    except Exception:
        return ''


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def collect(extra):
    files = []
    research = TOPIC / 'research'
    dirs = [d for d in sorted(research.iterdir())
            if d.is_dir() and any(fnmatch.fnmatch(d.name, g) for g in INCLUDE_GLOBS)]
    for e in extra:
        d = (ROOT / e).resolve()
        if d.is_dir():
            dirs.append(d)
        elif d.is_file():
            files.append(d)
    for d in dirs:
        for p in sorted(d.rglob('*')):
            if not p.is_file():
                continue
            low = p.relative_to(ROOT).as_posix().lower()
            if any(w in low for w in DENY) or p.suffix not in ALLOW_EXT or p.stat().st_size > MAX_FILE:
                continue
            files.append(p)
    seen, out = set(), []
    for p in files:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true', help='chỉ in danh sách, không ghi gói')
    ap.add_argument('--extra', action='append', default=[], help='thư mục/file thêm (tương đối gốc repo)')
    a = ap.parse_args(argv)

    files = collect(a.extra)
    for p in files:                       # chốt chặn cuối
        low = p.relative_to(ROOT).as_posix().lower()
        assert not any(w in low for w in ('koren', 'metadegron', 'larsen', 'clinvar')), low
    total = sum(p.stat().st_size for p in files)
    if a.list:
        for p in files:
            print(f'{p.stat().st_size:>9,d}  {p.relative_to(ROOT).as_posix()}')
        print(f'--- {len(files)} file, {total/1024:.0f} KB')
        return 0

    commit = git('rev-parse', 'HEAD')
    dirty_files = [l[3:] for l in git('status', '--porcelain').splitlines()]
    dirty = bool(dirty_files)
    manifest = {'package': 'degron-code', 'stubs': sorted(STUBS), 'created': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'git_commit': commit, 'dirty': dirty, 'n_dirty_files': len(dirty_files),
                'dirty_files_sample': dirty_files[:30], 'topic_rel': TOPIC_REL,
                'files': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha256(p),
                           'bytes': p.stat().st_size} for p in files]}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    name = f'degron-code-{commit[:12] or "nogit"}{"-dirty" if dirty else ""}.zip'
    zp = OUT_DIR / name
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('CODE_MANIFEST.json', json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
        for rel, text in STUBS.items():
            z.writestr(rel, text)
        for p in files:
            z.write(p, p.relative_to(ROOT).as_posix())
    digest = sha256(zp)
    (OUT_DIR / (name + '.sha256')).write_text(f'{digest}  {name}\n')
    print(f'✔ {zp.relative_to(ROOT)}  {zp.stat().st_size/1024:.0f} KB  {len(files)} file')
    print(f'  sha256={digest}\n  git={commit[:12]} dirty={dirty} ({len(dirty_files)} file chưa commit)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
