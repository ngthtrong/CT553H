"""R1 — gộp điểm các seed đã tải về, tính AUROC macro + so sánh ghép cặp theo cụm với ridge ext 4,0.

Chạy được cục bộ (CPU, vài giây, KHÔNG huấn luyện): đọc các file `r1-preds-seed*.npz` từ một hoặc nhiều
thư mục kết quả (mỗi phiên notebook một thư mục), rồi ghi `results.json` cạnh script này.

  .venv/bin/python -I topics/degron-footprint/research/r1-degformer-clean-2026-10-22/aggregate_r1.py \
      [thư-mục-kết-quả ...]        # mặc định: thư mục chứa script

Quy tắc kết luận (PROTOCOL §6) được cài thẳng trong hàm `verdict()`; không thêm kết luận nào khác.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
sys.path.insert(0, str(TOPIC / 'research/residue-task-derisk-2026-10-15'))
sys.path.insert(0, str(TOPIC / 'research/learning-curve-2026-10-22'))

SEEDS_REQUIRED = (17, 29, 43)


def verdict(delta_ens, ci, seed_deltas, n_seeds):
    """PROTOCOL §6. 'hơn' cần CI dưới > 0 VÀ mọi seed đã chạy dương VÀ đủ ba seed."""
    if ci[0] > 0 and all(d > 0 for d in seed_deltas.values()):
        if n_seeds >= 3:
            return 'Degformer sạch cụm HƠN ridge ext 4,0 (đạt tiêu chí ba seed)'
        return f'Tạm thời hơn, nhưng mới {n_seeds}/3 seed — chưa đạt tiêu chí'
    if ci[1] < 0:
        return ('ridge ext 4,0 HƠN Degformer sạch cụm' if n_seeds >= 3
                else f'Tạm thời ridge hơn ({n_seeds}/3 seed)')
    return ('Không phân biệt được (CI phủ 0 hoặc seed không đồng nhất)' if n_seeds >= 3
            else f'Chưa kết luận ({n_seeds}/3 seed, CI phủ 0 hoặc seed không đồng nhất)')


def load_seed_files(dirs):
    best = {}
    for d in dirs:
        for f in sorted(Path(d).glob('r1-preds-seed*.npz')):
            seed = int(f.stem.split('seed')[1])
            z = np.load(f)
            if bool(z['smoke']):
                print(f'bỏ {f}: chạy SMOKE')
                continue
            n = int(z['done'].sum())
            if seed not in best or n > best[seed][0]:
                best[seed] = (n, z['scores'], z['done'], str(f))
    return best


def main(dirs, out_path=None):
    import residue_data as rd
    import run_curve as rc
    import derisk as dr
    peps0, X0, y0, idx0, rowg0, groups0, _ = rc.build(rd.DEGRON_PSI_MAX, 'base')
    lc = json.loads((TOPIC / 'research/learning-curve-2026-10-22/results.json').read_text())
    g2 = json.loads((TOPIC / 'research/g2-saturation-2026-10-18/results.json').read_text())
    e3 = json.loads((TOPIC / 'research/g2-extension-2026-10-18/e3-degformer-arch.json').read_text())
    ridge_ext = lc['results']['ridge']['ext']['per_peptide']
    ridge_base = lc['results']['ridge']['100']['per_peptide']
    dpap = [g2['per_peptide'][p]['DeltaPAP'] for p in peps0]
    leaky = [g2['per_peptide'][p]['Degformer'] for p in peps0]
    mean = lambda v: float(np.mean([x for x in v if x is not None]))
    assert abs(mean(ridge_ext) - 0.8208223589063638) < 1e-9 and abs(mean(ridge_base) - 0.8081859035239344) < 1e-9

    seeds = load_seed_files(dirs or [HERE])
    complete = {s: v for s, v in seeds.items() if v[0] == 5}
    incomplete = {s: v[0] for s, v in seeds.items() if v[0] != 5}
    out = {'protocol': 'PROTOCOL.md (R1) — benchmark phát triển OOF, KHÔNG phải kiểm chứng ngoài; không đổi trạng thái G2',
           'seeds_complete': sorted(complete), 'seeds_incomplete_folds_done': incomplete,
           'references_macro_auroc': {'ridge_ext4.0': mean(ridge_ext), 'ridge_base': mean(ridge_base),
                                      'DeltaPAP': mean(dpap), 'Degformer_checkpoint_leaky': mean(leaky),
                                      'E3_degformer_arch_91_labels_only': e3['macro_auroc']['degformer_arch_cov80']},
           'source_files': {str(s): v[3] for s, v in seeds.items()}}
    if not complete:
        out['verdict'] = 'Chưa có seed nào hoàn tất 5 fold — chưa có kết luận'
        Path(out_path or HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    per_seed = {s: dr.macro_auroc(v[1], y0, idx0) for s, v in complete.items()}
    ens = np.mean([complete[s][1] for s in sorted(complete)], axis=0)
    ens_m, ens_pp = dr.macro_auroc(ens, y0, idx0)
    out['macro_auroc_per_seed'] = {str(s): per_seed[s][0] for s in sorted(per_seed)}
    out['macro_auroc_ensemble'] = ens_m
    out['per_peptide_ensemble'] = ens_pp
    cmp = lambda a, b: rc.compare(a, b, groups0)
    out['paired'] = {
        'primary_vs_ridge_ext4.0': cmp(ens_pp, ridge_ext),
        'vs_ridge_base': cmp(ens_pp, ridge_base),
        'vs_DeltaPAP': cmp(ens_pp, dpap),
        'vs_Degformer_checkpoint_leaky': cmp(ens_pp, leaky),
    }
    seed_d = {s: cmp(per_seed[s][1], ridge_ext)['delta'] for s in sorted(per_seed)}
    out['seed_deltas_vs_ridge_ext4.0'] = {str(s): d for s, d in seed_d.items()}
    prim = out['paired']['primary_vs_ridge_ext4.0']
    out['verdict'] = verdict(prim['delta'], prim['ci95'], seed_d, len(complete))
    out['leakage_effect'] = {'checkpoint_leaky_minus_clean_macro_auroc':
                             mean(leaky) - ens_m}
    out['note'] = ('So seed đơn với ridge ensemble ba seed (per_peptide đã lưu ở learning-curve/results.json); '
                   'chênh giữa ridge từng seed và ensemble ≤ 5e-4 (PROTOCOL §6).')
    out['aggregate_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(out_path or HERE / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: out[k] for k in ('macro_auroc_per_seed', 'macro_auroc_ensemble', 'paired',
                                          'seed_deltas_vs_ridge_ext4.0', 'verdict', 'leakage_effect')},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1:])
