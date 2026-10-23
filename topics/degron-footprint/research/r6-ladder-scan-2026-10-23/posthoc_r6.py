"""R6 — phân tích HẬU KIỂM (mô tả; không thuộc tiêu chí chốt trước của PROTOCOL).

Chạy từ gốc repo, với thư mục chứa các `r6-oof-*.npz` đã giải nén từ `r6-results.zip`:
    .venv/bin/python -I topics/degron-footprint/research/r6-ladder-scan-2026-10-23/posthoc_r6.py <thư-mục-OOF>
Ghi `posthoc-r6.json` cạnh script. Gồm: (1) tái tổng hợp từ OOF so với `results.json`; (2) hiệu ứng ensemble ba seed;
(3) Δ theo peptide; (4) trung bình điểm ridge + mạng (hai phép, nêu rõ cách chọn); (5) lượt đơn so ridge_W5;
(6) đếm peptide scanning nằm ngoài mọi cụm bão hòa (độ phủ của một kiểm chứng ngoài mức peptide, chưa chạy).
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_r6 as rr                                       # noqa: E402
import r6stats as st                                      # noqa: E402

d = Path(sys.argv[1])
data = rr.r6.load_sat()
y0, idx0, groups0 = data['y0'], data['idx0'], data['groups0']
oof = rr.load_all_oof(d)
S = {k: st.summarize_oof(v, y0, idx0) for k, v in oof.items()}
ref = json.load(open(HERE / 'run-kaggle-20261023/results.json'))
out = {}

# 1. tái tổng hợp từ OOF
out['reaggregate_max_abs_diff'] = max(abs(S[k]['macro_auroc_ensemble'] - ref['summaries'][k]['macro_auroc_ensemble']) for k in S)

# 2. hiệu ứng ensemble: AUROC trung bình từng seed so với ensemble
out['ensemble_effect'] = {}
for k, v in S.items():
    ms = float(np.mean(list(v['macro_auroc_per_seed'].values())))
    out['ensemble_effect'][k] = {'mean_seed': ms, 'ensemble': v['macro_auroc_ensemble'], 'gain': v['macro_auroc_ensemble'] - ms}


# 3. Δ theo peptide (ensemble)
def pp_delta(a, b):
    return np.array([x - y for x, y in zip(S[a]['per_peptide_ensemble'], S[b]['per_peptide_ensemble'])
                     if x is not None and y is not None])


out['per_peptide'] = {}
for a, b in [('esm35_mcnn', 'ridge_M3'), ('esm35_mcnn', 'ridge_W5'), ('ridge_W5', 'ridge_M3'),
             ('esm35_mcnn+scan_pool', 'ridge_W5'), ('oh_mcnn+scan_ft', 'ridge_W5'),
             ('esm35_mcnn+scan_pool', 'esm35_mcnn'), ('oh_mcnn+scan_ft', 'oh_mcnn'), ('esm35_mcnn', 'oh_mcnn')]:
    x = pp_delta(a, b)
    s = np.sort(x)
    out['per_peptide'][f'{a} - {b}'] = {
        'n': len(x), 'mean': float(x.mean()), 'median': float(np.median(x)), 'frac_positive': float((x > 0).mean()),
        'top5_contrib_to_mean': float(s[-5:].sum() / len(x)), 'bottom5_contrib_to_mean': float(s[:5].sum() / len(x)),
        'mean_without_top5': float(s[:-5].mean())}


# 4. trung bình điểm ridge + mạng (hậu kiểm). Phép 1 = ridge_W5 + mạng CHÍNH của PROTOCOL; phép 2 = ridge_W5 + cấu hình
#    có AUROC ensemble cao nhất bảng => CHỌN THEO KẾT QUẢ nên chệch lạc quan (winner's curse), chỉ để mô tả.
def blend(a, b):
    return {s: .5 * oof[a][s] + .5 * oof[b][s] for s in rr.SEEDS}


out['blend_posthoc'] = {}
for name, (a, b) in {'W5+esm35_mcnn': ('ridge_W5', 'esm35_mcnn'),
                     'W5+esm35_mcnn+scan_pool': ('ridge_W5', 'esm35_mcnn+scan_pool')}.items():
    Sb = st.summarize_oof(blend(a, b), y0, idx0)
    row = {'ensemble_auroc': Sb['macro_auroc_ensemble'], 'vs': {}}
    for r in ('ridge_W5', b):
        c = st.contrast(Sb, S[r], groups0, m=1)
        row['vs'][r] = {k: c[k] for k in ('delta', 'ci95', 'seed_deltas')}
    out['blend_posthoc'][name] = row

# 5. lượt đơn (không ensemble) so ridge_W5: trung bình ba seed theo peptide, bootstrap theo cụm
out['single_runs_vs_ridge_W5'] = {}
sd = S['ridge_W5']['_per_seed_pp']
for cfg in ('esm35_mcnn', 'esm35_mcnn+scan_pool', 'oh_mcnn+scan_ft', 'esm35_mcnn+scan_ft'):
    sa = S[cfg]['_per_seed_pp']
    per_seed = {str(s): float(np.mean([x - y for x, y in zip(sa[s], sd[s]) if x is not None and y is not None]))
                for s in rr.SEEDS}
    n = len(sd[rr.SEEDS[0]])
    pa = [None if sa[rr.SEEDS[0]][i] is None else float(np.mean([sa[s][i] for s in rr.SEEDS])) for i in range(n)]
    pb = [None if sd[rr.SEEDS[0]][i] is None else float(np.mean([sd[s][i] for s in rr.SEEDS])) for i in range(n)]
    c = st.compare(pa, pb, groups0, m=1)
    out['single_runs_vs_ridge_W5'][cfg] = {'per_seed': per_seed, 'mean_of_seeds_delta': c['delta'], 'ci95': c['ci95']}

# 6. scanning ngoài mọi cụm bão hòa (cov80)
sat_groups = np.asarray(sorted(set(np.asarray(data['st']['groups']).tolist())))
sc = rr.r6.load_scan(4.0)
keep = sc['keep']
rowg, y, aa, pep = sc['rowg'][keep], sc['y'][keep], sc['aa'][keep], sc['pep_of_row'][keep]
dis = ~np.isin(rowg, sat_groups)
yd, pd_ = y[dis], pep[dis]
both = sum(1 for p in set(pd_.tolist()) if (yd[pd_ == p] >= 1).any() and (yd[pd_ == p] < 1).any())
out['scan_holdout'] = {
    'sat_peptides': int(len(data['st']['peps'])), 'sat_clusters': int(len(sat_groups)),
    'scan_cells': int(len(keep)), 'scan_peptides': int(len(set(pep.tolist()))), 'scan_clusters': int(len(set(rowg.tolist()))),
    'cells_in_sat_clusters': int((~dis).sum()),
    'disjoint_cells': int(dis.sum()), 'disjoint_peptides': int(len(set(pd_.tolist()))),
    'disjoint_clusters': int(len(set(rowg[dis].tolist()))),
    'disjoint_peptides_both_classes': int(both),
    'positive_rate_dpsi_ge_1': float((yd >= 1).mean()),
    'aa_counts': {a: int((aa[dis] == a).sum()) for a in 'RAS'}}

(HERE / 'posthoc-r6.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: out[k] for k in ('reaggregate_max_abs_diff', 'scan_holdout')}, indent=1, ensure_ascii=False))
