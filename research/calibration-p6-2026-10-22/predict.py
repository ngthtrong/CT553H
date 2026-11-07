"""Nguyên mẫu G3 tối giản (offline): điểm ΔPSI và xác suất hiệu chuẩn cho mọi thay thế trên tile 28-mer.

Đặc trưng M3 (180 chiều) được dựng ĐỘC LẬP với derisk.featurize để verify.py có phép đối chiếu thật:
  [0:20] one-hot acid amin hoang dã · [20:40] one-hot acid amin thay vào ·
  [40:60] thành phần acid amin cả tile · [60:180] one-hot ngữ cảnh vị trí -3,-2,-1,+1,+2,+3.
Chỉ cần numpy; mô hình đọc từ data/processed/calibration-p6-model.npz (sinh bằng build_model.py).

Ví dụ:
  .venv/bin/python -I predict.py --uniprot P60484 --tile 3 --out pten-tile3.csv
  .venv/bin/python -I predict.py --uniprot P60484 --all-tiles --out pten.csv
  .venv/bin/python -I predict.py --seq <28 acid amin> --out x.csv
"""
import argparse
import csv
import gzip
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
MODEL = TOPIC / 'data/processed/calibration-p6-model.npz'
FASTA = TOPIC / 'data/raw/human-reviewed-2026-10-12.fasta.gz'
AAS = 'ACDEFGHIKLMNPQRSTVWY'
AA2I = {a: i for i, a in enumerate(AAS)}
TILE_LEN, TILE_STEP, WINDOW = 28, 23, 3
OFFSETS = [o for o in range(-WINDOW, WINDOW + 1) if o != 0]

WARNING = (
    'CẢNH BÁO: mô hình học trên Zhang 2023 (GPS, tile 28-mer nội vùng, thang PSI 1..6) và chỉ trên '
    'peptide có PSI(WT) <= 4,0. Xác suất là P(ΔPSI >= 1,0) CHO MIỀN ĐÓ; không dùng cho tile bền, '
    'cho hệ đo khác, hay như kiểm chứng ngoài. Benchmark phát triển, OOF AUROC ~0,82. '
    'Không dùng nhãn Koren 2018 hay nguồn chưa có quyền.')


def featurize(seq, pos, aa):
    """Một ô (vị trí 1-based, acid amin thay) -> vector 180 chiều."""
    x = np.zeros(180)
    x[AA2I[seq[pos - 1]]] = 1.0
    x[20 + AA2I[aa]] = 1.0
    for c in seq:
        if c in AA2I:
            x[40 + AA2I[c]] += 1.0 / len(seq)
    for b, o in enumerate(OFFSETS):
        i = pos - 1 + o
        if 0 <= i < len(seq) and seq[i] in AA2I:
            x[60 + b * 20 + AA2I[seq[i]]] = 1.0
    return x


def cells_of(seq):
    return [(pos, aa) for pos in range(1, len(seq) + 1) for aa in AAS if aa != seq[pos - 1]]


def load_model(path=MODEL):
    z = np.load(path, allow_pickle=False)
    return {k: z[k] for k in z.files}


def calibrate(model, score, which=None):
    which = which or str(model['calibrator'])
    if which == 'platt':
        return 1.0 / (1.0 + np.exp(-(model['platt_coef'][0] * score + model['platt_intercept'][0])))
    if which == 'iso':
        return np.interp(score, model['iso_x'], model['iso_y'])
    raise ValueError(which)


def score_cells(model, seq, cells):
    X = np.array([featurize(seq, p, a) for p, a in cells])
    return X @ model['coef'] + float(model['intercept'][0])


def predict_tile(model, seq, which=None):
    cells = cells_of(seq)
    s = score_cells(model, seq, cells)
    p = calibrate(model, s, which)
    order = np.argsort(-s, kind='stable')
    rank = np.empty(len(s), dtype=int)
    rank[order] = np.arange(1, len(s) + 1)
    return cells, s, p, rank


def load_uniprot(path=FASTA):
    up, acc, buf = {}, None, []
    with gzip.open(path, 'rt') as fh:
        for line in fh:
            if line.startswith('>'):
                if acc:
                    up[acc] = ''.join(buf)
                acc = line.split('|')[1] if '|' in line else None
                buf = []
            else:
                buf.append(line.strip())
    if acc:
        up[acc] = ''.join(buf)
    return up


def tile_seq(protein, n):
    s = protein[(n - 1) * TILE_STEP:(n - 1) * TILE_STEP + TILE_LEN]
    return s if len(s) == TILE_LEN else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--seq', help='tile 28 acid amin')
    src.add_argument('--uniprot', help='accession UniProt trong snapshot 2026-10-12')
    ap.add_argument('--tile', type=int, help='chỉ số tile 1-based: (n-1)*23 .. +28')
    ap.add_argument('--all-tiles', action='store_true')
    ap.add_argument('--out', help='ghi CSV (mặc định stdout)')
    ap.add_argument('--calibrator', choices=['platt', 'iso'], help='mặc định theo mô hình đã build')
    a = ap.parse_args(argv)

    if not MODEL.exists():
        sys.exit(f'chưa có {MODEL}; chạy build_model.py trước')
    model = load_model()
    print(WARNING, file=sys.stderr)

    tiles = []   # (peptide_id, tile, seq)
    if a.seq:
        s = a.seq.strip().upper()
        if len(s) != TILE_LEN or any(c not in AA2I for c in s):
            sys.exit(f'--seq phải là {TILE_LEN} acid amin chuẩn')
        tiles.append(('user_seq', 0, s))
    else:
        prot = load_uniprot().get(a.uniprot)
        if not prot:
            sys.exit(f'không có {a.uniprot} trong snapshot UniProt cache')
        ns = (range(1, (len(prot) - TILE_LEN) // TILE_STEP + 2) if a.all_tiles
              else [a.tile] if a.tile else sys.exit('cần --tile N hoặc --all-tiles'))
        for n in ns:
            s = tile_seq(prot, n)
            if s is None:
                print(f'tile {n}: ngoài phạm vi protein ({len(prot)} aa), bỏ qua', file=sys.stderr)
            elif any(c not in AA2I for c in s):
                print(f'tile {n}: có acid amin không chuẩn, bỏ qua', file=sys.stderr)
            else:
                tiles.append((f'{a.uniprot}_{n}', n, s))
    if not tiles:
        sys.exit('không có tile hợp lệ')

    fh = open(a.out, 'w', newline='', encoding='utf-8') if a.out else sys.stdout
    w = csv.writer(fh)
    w.writerow(['peptide', 'tile', 'position', 'wt_aa', 'mut_aa', 'score_dpsi_raw',
                'p_dpsi_ge_1_calibrated', 'rank_in_tile', 'top10pct_in_tile'])
    for pid, n, seq in tiles:
        cells, s, p, rank = predict_tile(model, seq, a.calibrator)
        cut = int(np.ceil(0.10 * len(cells)))
        for (pos, aa), si, pi, ri in zip(cells, s, p, rank):
            w.writerow([pid, n, pos, seq[pos - 1], aa, f'{si:.10g}', f'{pi:.10g}', int(ri), int(ri <= cut)])
    if a.out:
        fh.close()


if __name__ == '__main__':
    main()
