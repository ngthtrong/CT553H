"""Dựng bảng ô của bộ SCANNING (Zhang 2023, Replicate 1) cho R6: một dòng cho mỗi (peptide, vị trí) có nhãn.

Nhãn ΔPSI = PSI(ô đột biến) − PSI(WT đo trực tiếp `_mut0`), đúng `residue_data.build_scanning`; peptide giữ nếu
PSI(WT) ≤ 4,0 (cùng ngưỡng mở rộng của cấu hình chính), ≥ 21 vị trí đo được, reads ≥ 10. Thay thế của bộ quét chỉ
là R/A/S (quy tắc "opposite scanning"), mỗi vị trí đúng một acid amin.

Peptide có accession KHÔNG nằm trong `protein-id30-cov80_cluster.tsv` bị loại (nếu giữ, chúng thành "cụm riêng" và
có thể là paralog của protein test): số bị loại ghi vào bảng.

Đây là bước CHUẨN BỊ DỮ LIỆU (không huấn luyện). Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/r6-ladder-scan-2026-10-23/make_scantable.py
Đầu ra: data/processed/r6-scantable.npz (ghi vào data/README.md).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
import residue_data as rd          # noqa: E402

OUT = TOPIC / 'data/processed/r6-scantable.npz'
PSI_WT_MAX = 4.0


def main():
    d = rd.load_all(degron_psi_max=PSI_WT_MAX)
    scan, rep = d['scan'], d['clusters']
    peps, wt_seq, psi_wt, groups = [], [], [], []
    pep_of_row, pos, aa, mut_seq, y = [], [], [], [], []
    dropped_no_cluster = []
    for name in sorted(scan):
        v = scan[name]
        acc = rd.accession(name)
        if acc not in rep:
            dropped_no_cluster.append(name)
            continue
        assert len(v['seq']) == rd.TILE_LEN
        k = len(peps)
        peps.append(name); wt_seq.append(v['seq']); psi_wt.append(v['wt']); groups.append(rep[acc])
        for p, (a, dpsi) in sorted(v['cells'].items()):
            assert a in rd.AAS and v['seq'][p - 1] in rd.AAS and a != v['seq'][p - 1]
            pep_of_row.append(k); pos.append(p); aa.append(a)
            mut_seq.append(v['seq'][:p - 1] + a + v['seq'][p:]); y.append(dpsi)
    np.savez_compressed(
        OUT, peps=np.asarray(peps), wt_seq=np.asarray(wt_seq), psi_wt=np.asarray(psi_wt, dtype=np.float64),
        groups=np.asarray(groups), pep_of_row=np.asarray(pep_of_row, dtype=np.int32),
        pos=np.asarray(pos, dtype=np.int16), aa=np.asarray(aa), mut_seq=np.asarray(mut_seq),
        y=np.asarray(y, dtype=np.float64), psi_wt_max=np.asarray(PSI_WT_MAX),
        n_dropped_no_cluster=np.asarray(len(dropped_no_cluster)))
    y = np.asarray(y)
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    summary = {'n_peptides': len(peps), 'n_cells': int(len(y)), 'n_clusters': len(set(groups)),
               'n_peptides_le_3.0': int(sum(w <= 3.0 for w in psi_wt)),
               'n_cells_le_3.0': int(sum(psi_wt[k] <= 3.0 for k in pep_of_row)),
               'positive_rate': float((y >= rd.RESCUE_DELTA).mean()),
               'n_dropped_no_cluster': len(dropped_no_cluster),
               'sha256': sha}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    (HERE / 'scantable-summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
