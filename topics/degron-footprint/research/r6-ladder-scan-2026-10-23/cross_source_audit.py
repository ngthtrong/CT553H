"""Kiểm chéo MÔ TẢ scanning vs bão hòa trên CÙNG ô (peptide, vị trí, acid amin thay) — PROTOCOL R6 §0 / README mục 1.

Không phải tiêu chí và không phải thí nghiệm mô hình. Với mỗi ngưỡng PSI(WT) (3,0 / 4,0 / không ngưỡng): các peptide có mặt ở cả
hai bộ với trình tự giống nhau; ô nào bộ scanning đo (chỉ thay bằng R/A/S) và bộ bão hòa cũng đo thì so ΔPSI:
Pearson/Spearman, độ dốc OLS, κ nhị phân (ΔPSI ≥ 1), AUROC gộp của ΔPSI scanning cho ô dương bão hòa, tham chiếu "nửa A bão hòa → nhãn nửa B"
trên đúng các ô đó, và chênh PSI(WT) giữa hai nguồn.

Chạy từ gốc repo:
  OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
    topics/degron-footprint/research/r6-ladder-scan-2026-10-23/cross_source_audit.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import pearsonr, spearmanr

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
import residue_data as rd          # noqa: E402
import derisk as dr                # noqa: E402


def main():
    out = {}
    for thr in (3.0, 4.0, 99.0):
        d = rd.load_all(degron_psi_max=thr)
        scan, sat = d['scan'], d['sat']
        shared = sorted(set(scan) & set(sat))
        rows, wt_pairs = [], []
        for p in shared:
            s, t = scan[p], sat[p]
            if s['seq'] != t['seq']:
                continue
            wt_pairs.append((s['wt'], t['psi_wt']))
            for pos, (aa, dpsi) in s['cells'].items():
                if (pos, aa) in t['cells']:
                    a, b = t['cells'][(pos, aa)]
                    rows.append((aa, dpsi, (a + b) / 2, a, b))
        sc = np.array([r[1] for r in rows]); st = np.array([r[2] for r in rows])
        sa = np.array([r[3] for r in rows]); sb = np.array([r[4] for r in rows])
        wt = np.array(wt_pairs)
        ps, pt = sc >= rd.RESCUE_DELTA, st >= rd.RESCUE_DELTA
        po = float((ps == pt).mean())
        pe = ps.mean() * pt.mean() + (1 - ps.mean()) * (1 - pt.mean())
        out['no_threshold' if thr > 90 else f'wt_le_{thr}'] = {
            'n_shared_peptides': len(shared), 'n_cells': int(len(rows)),
            'substitution_counts': {a: int(sum(1 for r in rows if r[0] == a)) for a in sorted({r[0] for r in rows})},
            'positive_rate_scan': float(ps.mean()), 'positive_rate_sat': float(pt.mean()),
            'pearson': float(pearsonr(sc, st)[0]), 'spearman': float(spearmanr(sc, st).statistic),
            'ols_slope_sat_on_scan': float(np.polyfit(sc, st, 1)[0]),
            'mean_dpsi_scan': float(sc.mean()), 'mean_dpsi_sat': float(st.mean()),
            'binary_agreement': po, 'cohen_kappa': float((po - pe) / (1 - pe)),
            'auroc_scan_dpsi_for_sat_positive_pooled': dr.auroc(list(sc), list(pt)),
            'reference_auroc_satA_for_satB_positive_same_cells': dr.auroc(list(sa), list(sb >= rd.RESCUE_DELTA)),
            'wt_psi_mean_scan_mut0': float(wt[:, 0].mean()), 'wt_psi_mean_sat_internal': float(wt[:, 1].mean()),
            'wt_psi_diff_sat_minus_scan': float((wt[:, 1] - wt[:, 0]).mean()),
            'wt_psi_pearson': float(pearsonr(wt[:, 0], wt[:, 1])[0]),
        }
    (HERE / 'cross-source-audit.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: {kk: round(vv, 4) for kk, vv in v.items() if isinstance(vv, float)} for k, v in out.items()},
                     indent=1))


if __name__ == '__main__':
    main()
