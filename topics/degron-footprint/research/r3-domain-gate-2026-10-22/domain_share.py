"""Tỉ lệ tile của sàng peptidome rơi vào từng trạng thái miền của tầng (i) R3 (mô tả, không phải tiêu chí).

Dùng đúng hai ngưỡng `x_cuts_measured` trong run-kaggle-20261022/gate-weights.npz áp lên PSI sàng của mọi tile có
reads ≥ 10. Ghi run-kaggle-20261022/proteome-domain-share.json.  Chạy từ gốc repo:
  .venv/bin/python -I topics/degron-footprint/research/r3-domain-gate-2026-10-22/domain_share.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
RUN = HERE / 'run-kaggle-20261022'


def main():
    w = np.load(RUN / 'gate-weights.npz', allow_pickle=False)
    c_in, c_out = [float(x) for x in w['x_cuts_measured']]
    df = pd.read_csv(TOPIC / 'data/interim/gps-peptidome-rep1.tsv', sep='\t')
    x = pd.to_numeric(df.loc[df['reads'] >= 10, 'psi'], errors='coerce').dropna().to_numpy()
    p_in, p_out = float((x <= c_in).mean()), float((x >= c_out).mean())
    out = {'n_tiles_reads_ge_10': int(len(x)), 'x_cut_in': c_in, 'x_cut_out': c_out,
           'share_in_domain': p_in, 'share_borderline': 1 - p_in - p_out, 'share_out_of_domain': p_out,
           'note': 'tile của sàng peptidome (mọi độ dài), PSI sàng thô; mô tả, không phải kết quả mô hình'}
    (RUN / 'proteome-domain-share.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
