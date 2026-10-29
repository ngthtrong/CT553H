"""Tổng hợp bằng chứng đã lưu; không huấn luyện hay tái kiểm định."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data' / 'README.md').exists())
RESEARCH = TOPIC / 'research'
SOURCES = {
    'r6': 'r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json',
    'r6_posthoc': 'r6-ladder-scan-2026-10-23/posthoc-r6.json',
    'r2': 'r2-esm-features-2026-10-22/run-kaggle-20261022/results.json',
    'linear_history': 'residue-task-derisk-2026-10-15/model.json',
    'r6_protocol': 'r6-ladder-scan-2026-10-23/PROTOCOL.md',
    'r6_data': 'r6-ladder-scan-2026-10-23/r6data.py',
    'r6_nn': 'r6-ladder-scan-2026-10-23/r6nn.py',
    'r6_runner': 'r6-ladder-scan-2026-10-23/run_r6.py',
    'r2_common': 'r2-esm-features-2026-10-22/common.py',
    'linear_features': 'residue-task-derisk-2026-10-15/derisk.py',
}
CONFIGS = ('ridge_M3', 'ridge_W5', 'oh_cnn1', 'oh_mcnn',
           'ridge_esm35', 'esm35_cnn1', 'esm35_mcnn')
CONTRASTS = ('A_ridge_W5_vs_W3', 'P_esm35_mcnn_vs_ridge',
             'S1_esm35_mcnn_vs_oh_mcnn', 'S5_oh_mcnn_vs_oh_cnn1',
             'S6_esm35_mcnn_vs_esm35_cnn1', 'S7_esm35_mcnn_vs_ridge_W5')


def main():
    raw = {key: (RESEARCH / rel).read_bytes() for key, rel in SOURCES.items()}
    loaded = {k: json.loads(raw[k]) for k in ('r6', 'r6_posthoc', 'r2', 'linear_history')}
    r6, post, r2, old = (loaded[k] for k in ('r6', 'r6_posthoc', 'r2', 'linear_history'))
    summaries = {}
    for name in CONFIGS:
        value = r6['summaries'][name]
        seeds = value['macro_auroc_per_seed']
        assert set(seeds) == {'17', '29', '43'}, (name, seeds)
        summaries[name] = {
            'per_seed': seeds,
            'mean_seed_auroc': sum(seeds.values()) / len(seeds),
            'ensemble_auroc': value['macro_auroc_ensemble'],
        }
    contrasts = {key: r6['contrasts'][key] for key in CONTRASTS}
    for key, value in contrasts.items():
        assert (value['n_peptides'], value['n_clusters']) == (91, 89), key
        delta = summaries[value['a']]['ensemble_auroc'] - summaries[value['b']]['ensemble_auroc']
        assert abs(delta - value['delta']) < 1e-12, key
    report = {
        'schema_version': 1,
        'scope': 'Extraction of saved development results; no new training or bootstrap.',
        'sources': {key: {'path': '../' + rel, 'sha256': hashlib.sha256(raw[key]).hexdigest()}
                    for key, rel in SOURCES.items()},
        'r6': {'metric': 'cell AUROC, macro across peptides', 'summaries': summaries,
               'contrasts': contrasts},
        'r2': {key: r2[key] for key in ('model', 'pca_k', 'macro_auroc',
                                       'paired_M3+ESM_minus_M3', 'verdict')},
        'linear_history': old,
        'ensemble_posthoc': {name: post['ensemble_effect'][name] for name in CONFIGS},
        'scan_inventory_posthoc_cov80': post['scan_holdout'],
        'missing_matched_arms': ['pair-only ridge', 'pair+composition ridge',
                                'unordered-local-context ridge', 'ESM pointwise head matched to R6 CNN'],
    }
    lines = [
        '# Bảng bằng chứng đã có', '',
        'Sinh bằng `build_evidence.py`; số được trích từ JSON đã lưu, không phải lượt huấn luyện mới. '
        'Đường dẫn và SHA-256 nguồn: [evidence.json](evidence.json). '
        'Cách diễn giải và khoảng trống: [README.md](README.md).', '',
        '## R6: cùng outer-test 91 peptide / 89 cụm', '',
        'AUROC mức ô, macro theo peptide. `Mean seed` là trung bình AUROC từng seed; '
        '`Ensemble` là AUROC của điểm dự đoán trung bình ba seed.', '',
        '| Cấu hình | Seed 17 | Seed 29 | Seed 43 | Mean seed | Ensemble |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for name, value in summaries.items():
        numbers = [value['per_seed'][str(s)] for s in (17, 29, 43)]
        numbers += [value['mean_seed_auroc'], value['ensemble_auroc']]
        lines.append('| `' + name + '` | ' + ' | '.join(f'{v:.4f}' for v in numbers) + ' |')
    lines += ['', 'Nguồn: [results.json R6](../' + SOURCES['r6'] + ').', '',
              '## Phép so R6: giữ nguyên vai trò và kết luận nguồn', '',
              'P là phép xác nhận duy nhất của R6; S* là phép phụ/mô tả. '
              'CI dùng kết luận lấy `ci_adj` (bằng `ci95` khi m=1). '
              'Dấu từng seed lấy từ so hai seed tương ứng, không lấy từ hiệu ensemble.', '',
              '| Phép so | Vai trò | Δ ensemble | CI dùng kết luận | Δ seed 17/29/43 | Kết luận nguồn |',
              '|---|---|---:|---|---|---|']
    for name, value in contrasts.items():
        ci = value['ci_adj']
        ds = '/'.join(f'{value["seed_deltas"][str(s)]:+.4f}' for s in (17, 29, 43))
        lines.append(f'| `{name}` | {value["family"]}, m={value["m"]} | {value["delta"]:+.4f} '
                     f'| [{ci[0]:+.4f}; {ci[1]:+.4f}] | {ds} | {value["verdict"]} |')
    lines += ['', '## R2: ESM gộp + PCA + Ridge', '',
              'ESM-2 650M; PCA-64. Đây không phải đầu không CNN tương ứng hoàn toàn với R6.', '',
              '| Cấu hình nguồn | Ensemble AUROC |', '|---|---:|']
    for name, value in r2['macro_auroc'].items():
        lines.append(f'| `{name}` | {value["macro_auroc_ensemble"]:.4f} |')
    lines += ['', 'Nguồn: [results.json R2](../' + SOURCES['r2'] + ').', '',
              '## Đối chứng tuyến tính lịch sử: khác thiết kế R6', '',
              'Chỉ dùng để định vị bằng chứng. Không lấy chênh lệch giữa bảng này và R6 '
              'để quy tác động cho một thành phần. M0 chứa cặp thay thế và composition.', '',
              '| Cấu hình | Scanning CV, mean 5 seed | Học scanning → saturation |',
              '|---|---:|---:|']
    for name in ('M0_composition_only', 'M2_plus_window_composition', 'M3_plus_ordered_context'):
        a = old['scanning']['macro_auroc'][name]['mean']
        b = old['saturation_transfer']['macro_auroc'][name]['value']
        lines.append(f'| `{name}` | {a:.4f} | {b:.4f} |')
    lines += ['', 'Nguồn: [model.json lịch sử](../' + SOURCES['linear_history'] + ').', '',
              'Không có số mới cho pair-only hoặc ESM pointwise tương ứng CNN. '
              'Kiểm kê scanning ngoài cụm và hiệu ứng ensemble trong JSON là hậu kiểm đã có.', '']
    (HERE / 'evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'results.md').write_text('\n'.join(lines))
    print('Wrote evidence.json and results.md; source contrasts cross-checked; no training performed.')


if __name__ == '__main__':
    main()
