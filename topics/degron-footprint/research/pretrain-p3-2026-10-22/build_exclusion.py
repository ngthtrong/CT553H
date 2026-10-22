"""Dựng bảng gene Voutsinos -> protein thuộc cụm outer-test (chống rò rỉ cho P3).

Theo PROTOCOL.md §3. Ba luật, hợp của chúng là tập bị loại:
  1. MMseqs2 easy-search (id >= 0,30, e <= 1e-3, alnlen >= 50) giữa trình tự gene dựng
     từ tile liền kề và các protein thành viên của 89 cụm cov80 của bộ 91 peptide gốc;
  2. trùng 12-mer giữa tile 30-mer và các protein đó;
  3. trùng tên gene (biomart `Gene name` <-> UniProt `GN=`).

Bảng này KHÔNG phụ thuộc fold: nó chỉ ghi gene nào chạm protein nào. Runner suy ra
fold nào loại gene nào bằng cụm test của fold đó.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/pretrain-p3-2026-10-22/build_exclusion.py
"""
import csv
import gzip
import json
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
RAW = TOPIC / 'data/raw'
PROC = TOPIC / 'data/processed'
TILES = RAW / 'voutsinos-2026/repo/score/degrons.csv.gz'
BIOMART = RAW / 'voutsinos-2026/repo/library/biomart_cytosol.csv.gz'
UNIPROT = RAW / 'human-reviewed-2026-10-12.fasta.gz'
CLUSTERS = TOPIC / 'data/interim/protein-id30-cov80_cluster.tsv'
BASE_CACHE = PROC / 'learning-curve-sat-base.npz'
OUT = PROC / 'p3-tile-exclusion.json'
TILE_RE = re.compile(r'^(ENSG\d+)_tile(\d+)$')
STD = set('ACDEFGHIKLMNPQRSTVWY')
KMER = 12
MIN_ID, MAX_E, MIN_ALN = 0.30, '1e-3', 50

csv.field_size_limit(10 ** 7)


def load_tiles():
    tiles = defaultdict(list)                 # gene -> [(tile_no, aa)]
    n_all = n_drop = 0
    with gzip.open(TILES, 'rt', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            n_all += 1
            m = TILE_RE.match(r['name'])
            aa = r['aa']
            if not m or len(aa) != 30 or set(aa) - STD:
                n_drop += 1
                continue
            tiles[m.group(1)].append((int(m.group(2)), aa))
    for g in tiles:
        tiles[g].sort()
    return tiles, n_all, n_drop


def assemble(tl):
    """Ghép các tile liền kề (chồng 15 aa) thành đoạn; đứt chỗ thiếu tile/lệch chồng lấn."""
    frags, cur, last = [], None, None
    for no, aa in tl:
        if cur is not None and no == last + 1 and cur[-15:] == aa[:15]:
            cur += aa[15:]
        else:
            if cur:
                frags.append(cur)
            cur = aa
        last = no
    if cur:
        frags.append(cur)
    return frags


def load_uniprot():
    seq, gn = {}, {}
    with gzip.open(UNIPROT, 'rt') as fh:
        acc, buf = None, []
        for line in fh:
            if line.startswith('>'):
                if acc:
                    seq[acc] = ''.join(buf)
                acc = line.split('|')[1]
                m = re.search(r' GN=(\S+)', line)
                gn[acc] = m.group(1).upper() if m else None
                buf = []
            else:
                buf.append(line.strip())
        if acc:
            seq[acc] = ''.join(buf)
    return seq, gn


def main():
    z = np.load(BASE_CACHE, allow_pickle=True)
    base_clusters = set(z['groups'].tolist())
    rep_of = {}
    with CLUSTERS.open() as fh:
        for line in fh:
            r, m = line.rstrip('\n').split('\t')[:2]
            rep_of[m] = r
    targets = {m: r for m, r in rep_of.items() if r in base_clusters}
    useq, ugn = load_uniprot()
    targets = {a: r for a, r in targets.items() if a in useq}
    print(f'{len(base_clusters)} cụm test (gốc) -> {len(targets)} protein thành viên', flush=True)

    tiles, n_all, n_drop = load_tiles()
    print(f'tile: {n_all} dòng, bỏ {n_drop} (điều khiển/ký tự lạ); {len(tiles)} gene', flush=True)

    # ---- luật 1: MMseqs2 ----
    mm = shutil.which('mmseqs')
    assert mm, 'không thấy mmseqs'
    hits = defaultdict(set)                   # gene -> {target accession}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        with (td / 'q.fa').open('w') as fq:
            for g, tl in tiles.items():
                for i, f in enumerate(assemble(tl)):
                    if len(f) >= 30:
                        fq.write(f'>{g}|{i}\n{f}\n')
        with (td / 't.fa').open('w') as ft:
            for a in targets:
                ft.write(f'>{a}\n{useq[a]}\n')
        subprocess.run([mm, 'easy-search', str(td / 'q.fa'), str(td / 't.fa'), str(td / 'o.tsv'),
                        str(td / 'tmp'), '--min-seq-id', str(MIN_ID), '-e', MAX_E,
                        '--threads', '2', '-s', '7.5',
                        '--format-output', 'query,target,fident,alnlen,evalue'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for line in (td / 'o.tsv').read_text().splitlines():
            q, t, fid, aln, ev = line.split('\t')
            if float(fid) >= MIN_ID and int(aln) >= MIN_ALN:
                hits[q.split('|')[0]].add(t)
    print(f'luật 1 (MMseqs2): {len(hits)} gene chạm protein cụm test', flush=True)

    # ---- luật 2: 12-mer ----
    kidx = defaultdict(set)
    for a in targets:
        s = useq[a]
        for i in range(len(s) - KMER + 1):
            kidx[s[i:i + KMER]].add(a)
    kmer_hits = defaultdict(set)
    for g, tl in tiles.items():
        for _, aa in tl:
            for i in range(len(aa) - KMER + 1):
                k = aa[i:i + KMER]
                if k in kidx:
                    kmer_hits[g] |= kidx[k]
    print(f'luật 2 (12-mer): {len(kmer_hits)} gene', flush=True)

    # ---- luật 3: tên gene ----
    name2acc = defaultdict(set)
    for a in targets:
        if ugn.get(a):
            name2acc[ugn[a]].add(a)
    ens2name = defaultdict(set)
    with gzip.open(BIOMART, 'rt') as fh:
        for r in csv.DictReader(fh):
            if r['Gene name']:
                ens2name[r['Gene stable ID']].add(r['Gene name'].upper())
    name_hits = {}
    for g in tiles:
        s = set()
        for nm in ens2name.get(g, ()):
            s |= name2acc.get(nm, set())
        if s:
            name_hits[g] = s
    print(f'luật 3 (tên gene): {len(name_hits)} gene', flush=True)

    out = {
        'rules': {'mmseqs': {'min_seq_id': MIN_ID, 'evalue': MAX_E, 'min_alnlen': MIN_ALN},
                  'kmer': KMER, 'gene_name': 'biomart Gene name == UniProt GN'},
        'n_tile_rows': n_all, 'n_tile_dropped_controls_or_nonstandard': n_drop,
        'n_genes': len(tiles), 'n_tiles_kept': sum(len(v) for v in tiles.values()),
        'n_test_clusters': len(base_clusters), 'n_target_proteins': len(targets),
        'target_cluster': targets,
        'hits': {'mmseqs': {g: sorted(v) for g, v in hits.items()},
                 'kmer': {g: sorted(v) for g, v in kmer_hits.items()},
                 'gene_name': {g: sorted(v) for g, v in name_hits.items()}},
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False))
    union = set(hits) | set(kmer_hits) | set(name_hits)
    summary = {k: out[k] for k in out if k not in ('hits', 'target_cluster')}
    summary.update({'n_genes_hit_mmseqs': len(hits), 'n_genes_hit_kmer': len(kmer_hits),
                    'n_genes_hit_gene_name': len(name_hits), 'n_genes_hit_union': len(union),
                    'n_tiles_in_hit_genes_union': sum(len(tiles[g]) for g in union)})
    (HERE / 'exclusion-summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    print(f'hợp ba luật: {len(union)} gene / {summary["n_tiles_in_hit_genes_union"]} tile '
          f'(trên tất cả cụm test của cả 5 fold)')


if __name__ == '__main__':
    main()
