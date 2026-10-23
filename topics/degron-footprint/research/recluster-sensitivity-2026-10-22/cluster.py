"""Dựng các phân hoạch protein mới (L3–L6) của PROTOCOL.md bằng MMseqs2.

Cùng đầu vào và cùng cờ với bản gốc (prepare_protein_clusters.py); chỉ đổi --min-seq-id và -c.
Kết quả: data/interim/recluster-sensitivity/protein-idXX-covYY_cluster.tsv (đại diện<TAB>thành viên).

Chạy từ gốc repo:
  .venv/bin/python -I topics/degron-footprint/research/recluster-sensitivity-2026-10-22/cluster.py
"""
import subprocess, shutil, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
FASTA = TOPIC / 'data/processed/proteins-full.fasta'
OUT = TOPIC / 'data/interim/recluster-sensitivity'
MMSEQS = str(Path.home() / '.local/bin/mmseqs')
GRID = {'L3': (0.2, 0.5), 'L4': (0.1, 0.5), 'L5': (0.1, 0.3), 'L6': (0.0, 0.3)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'fasta_sha256': hashlib.sha256(FASTA.read_bytes()).hexdigest(), 'runs': {}}
    for tag, (ident, cov) in GRID.items():
        stem = f'protein-id{int(ident * 100):02d}-cov{int(cov * 100):02d}'
        tmp = OUT / f'{stem}-tmp'
        prefix = OUT / stem
        shutil.rmtree(tmp, ignore_errors=True)
        cmd = [MMSEQS, 'easy-cluster', str(FASTA), str(prefix), str(tmp),
               '--min-seq-id', str(ident), '-c', str(cov), '--cov-mode', '0',
               '--seq-id-mode', '0', '--alignment-mode', '3', '--cluster-mode', '1',
               '--single-step-clustering', '1', '-s', '7.5', '--max-seqs', '10000',
               '--split-memory-limit', '1500M', '--threads', '2']
        with (OUT / f'{stem}.log').open('w') as lg:
            subprocess.run(cmd, check=True, stdout=lg, stderr=subprocess.STDOUT)
        shutil.rmtree(tmp, ignore_errors=True)
        tsv = Path(f'{prefix}_cluster.tsv')
        reps = {l.split('\t')[0] for l in tsv.read_text().splitlines()}
        manifest['runs'][tag] = {'min_seq_id': ident, 'cov': cov, 'tsv': tsv.name,
                                 'n_rows': sum(1 for _ in tsv.open()), 'n_clusters_all_proteome': len(reps),
                                 'tsv_sha256': hashlib.sha256(tsv.read_bytes()).hexdigest(),
                                 'cmd': ' '.join(cmd)}
        print(tag, ident, cov, '->', len(reps), 'cụm / proteome', flush=True)
    (HERE / 'cluster-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
