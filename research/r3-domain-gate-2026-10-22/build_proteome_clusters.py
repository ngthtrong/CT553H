"""Phân cụm protein TOÀN PROTEOME (snapshot UniProt 20.431 protein) bằng MMseqs2, cùng cờ với bản gốc.

Lý do (local_analysis, 22/10/2026): file cụm của G2 (`protein-id30-cov80_cluster.tsv`) chỉ có 6.573 protein
(những protein có trong các thí nghiệm), nên với sàng peptidome (18.753 protein) phần lớn accession KHÔNG có cụm
và sẽ thành cụm riêng -> họ gen paralog (olfactory, KRAB-ZNF...) rò rỉ qua fold. R3 cần cụm phủ cả proteome.

Cờ y hệt `e3-labels-audit/prepare_protein_clusters.py`: --min-seq-id 0.3 -c 0.8 --cov-mode 0 --seq-id-mode 0
--alignment-mode 3 --cluster-mode 1 --single-step-clustering 1 -s 7.5 --max-seqs 10000.
Ghi: data/interim/protein-id30-cov80-proteome_cluster.tsv (rep<TAB>member, id = accession) + manifest SHA-256.
Chạy:  .venv/bin/python -I .../build_proteome_clusters.py  [--threads 2]   (khoảng vài phút CPU)
"""
import argparse
import gzip
import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
FASTA_GZ = TOPIC / 'data/raw/human-reviewed-2026-10-12.fasta.gz'
OUT = TOPIC / 'data/interim/protein-id30-cov80-proteome_cluster.tsv'
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--threads', type=int, default=2)
    a = ap.parse_args()
    seqs, acc, buf = {}, None, []
    with gzip.open(FASTA_GZ, 'rt') as fh:
        for line in fh:
            if line.startswith('>'):
                if acc:
                    seqs[acc] = ''.join(buf)
                acc, buf = line.split('|')[1], []
            else:
                buf.append(line.strip())
        if acc:
            seqs[acc] = ''.join(buf)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        fa = td / 'proteome.fasta'
        fa.write_text(''.join(f'>{k}\n{seqs[k]}\n' for k in sorted(seqs)))
        prefix = td / 'cl'
        cmd = ['mmseqs', 'easy-cluster', str(fa), str(prefix), str(td / 'tmp'), '--min-seq-id', '0.3', '-c', '0.8',
               '--cov-mode', '0', '--seq-id-mode', '0', '--alignment-mode', '3', '--cluster-mode', '1',
               '--single-step-clustering', '1', '-s', '7.5', '--max-seqs', '10000', '--split-memory-limit', '2G',
               '--threads', str(a.threads)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        text = Path(str(prefix) + '_cluster.tsv').read_text()
        fasta_sha = sha(fa.read_bytes())
    rows = [l.split('\t') for l in text.splitlines()]
    members = {m for _, m in rows}
    assert members == set(seqs), 'thành viên cụm khác tập protein đầu vào'
    OUT.write_text(text)
    sizes = Counter(r for r, _ in rows)
    man = {'input': FASTA_GZ.name, 'input_fasta_sha256': fasta_sha, 'n_proteins': len(seqs),
           'n_clusters': len(sizes), 'largest_cluster': sizes.most_common(1)[0][1],
           'cluster_file_sha256': sha(OUT.read_bytes()), 'command': ' '.join(cmd[:1] + cmd[1:2] + ['<fasta>']
                                                                            + cmd[4:]),
           'mmseqs_version': subprocess.run(['mmseqs', 'version'], capture_output=True, text=True).stdout.strip()}
    (HERE / 'proteome-cluster-manifest.json').write_text(json.dumps(man, indent=2) + '\n')
    print(json.dumps(man, indent=2))


if __name__ == '__main__':
    main()
