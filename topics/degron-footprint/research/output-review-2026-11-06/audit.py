"""Read-only campaign inventory and thesis evidence export; run from any directory.

Reuses the checked OOF analyses; does not train, deserialize model objects, or
rewrite campaign state. All derived numerical tables remain traceable to JSON.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
TOPIC = next(p for p in HERE.parents if (p / 'data/README.md').exists())
R = TOPIC / 'research/kaggle-roadmap-2026-10-31'
CAMPAIGN = R / 'output/local/ef138c84579c842e'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(2**20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    local = read(R / 'local-output-analysis.json')
    kaggle = read(R / 'output-analysis.json')
    details = read(R / 'output-analysis-details.json')
    assert local['integrity']['status'] == 'pass'
    assert not local['integrity']['mismatches']
    assert local['data_identity'] == kaggle['data_identity']
    source_checks = []
    for name, expected in local['source_files'].items():
        path = R / name
        assert path.stat().st_size == expected['bytes'], name
        assert digest(path) == expected['sha256'], name
        source_checks.append(name)

    inventory = {}
    # Count physical files, including partial/cache files; no deduplication claim.
    for parent in sorted((R / 'output').iterdir()):
        if not parent.is_dir():
            continue
        children = sorted(p for p in parent.iterdir() if p.is_dir())
        for child in children:
            files = [p for p in child.rglob('*') if p.is_file()]
            inventory[str(child.relative_to(R / 'output')).replace('\\', '/')] = {
                'physical_files': len(files),
                'physical_bytes': sum(p.stat().st_size for p in files),
                'extensions': dict(Counter(p.suffix or '[none]' for p in files)),
            }

    histories = {}
    for path in sorted((R / 'output/local').glob('*/state.json')):
        state = read(path)
        histories[path.parent.name] = {
            'state_sha256': digest(path),
            'counts': dict(Counter(j['status'] for j in state['jobs'].values())),
            'scientific_status': state.get('scientific_status'),
        }
    state = read(CAMPAIGN / 'state.json')
    timing = defaultdict(list)
    epochs = defaultdict(list)
    adapter_updates = []
    jobs = []
    for name, job in state['jobs'].items():
        if job['status'] != 'complete':
            continue
        source = Path(job.get('artifact_campaign', str(CAMPAIGN)))
        category = ('ridge' if name.startswith('ridge-') else
                    'tune-lora' if name.startswith('tune-lora-') else
                    'tune-frozen' if name.startswith('tune-frozen-') else
                    'extract' if name.startswith('extract-') else
                    'probe' if name.startswith('probe-') else 'other')
        if 'seconds' in job:
            timing[category].append(float(job['seconds']))
        fit = source / 'jobs' / name / 'fit.json'
        if category.startswith('tune-'):
            values = read(fit)
            epochs[values['mode'] + '-' + values['arm']].append(values['selected_epoch'])
            if values['mode'] == 'lora':
                changed = values['changed_parameters']
                adapter_updates.append({'job': name, 'changed_tensors': len(changed),
                                        'lora_tensors': sum('lora_' in s for s in changed)})
                assert any('lora_' in s for s in changed), name
        jobs.append({'name': name, 'category': category,
                     'inherited': source.resolve() != CAMPAIGN.resolve()})
    assert len(jobs) == 633
    assert len(adapter_updates) == 30
    timing_summary = {k: {'jobs': len(v), 'recorded_seconds_sum': sum(v),
                          'median_recorded_seconds': statistics.median(v),
                          'min_recorded_seconds': min(v), 'max_recorded_seconds': max(v)}
                      for k, v in timing.items()}
    epoch_summary = {k: {'folds': len(v), 'selected_epochs': v, 'min': min(v),
                         'max': max(v), 'median': statistics.median(v),
                         'counts': dict(Counter(v))} for k, v in epochs.items()}

    recipes = []
    for origin, analysis in [('Kaggle', kaggle), ('Local', local)]:
        for name, values in analysis.get('recipes', analysis.get('local_recipes')).items():
            recipes.append({'origin': origin, 'recipe': name, 'seeds': values['seeds'],
                            'ensemble': values['ensemble'], 'per_seed': values.get('per_seed'),
                            'oof_rows': values['oof_rows']})
    assert len(recipes) == 88
    assert all(len(r['seeds']) == 3 for r in recipes if r['origin'] == 'Local')
    assert all(r['ensemble']['all']['cells'] == 122412 for r in recipes)
    cross_runtime = []
    for name in sorted(set(local['local_recipes']) & set(kaggle['recipes'])):
        if name not in {f'esm2_35m-{view}-{arm}' for view in ['only','context'] for arm in ['B','D']}:
            continue  # The two nested selectors search different candidate families.
        l, k = local['local_recipes'][name], kaggle['recipes'][name]
        if len(k['seeds']) != 3:
            continue
        cross_runtime.append({'recipe': name,
                              'local_minus_kaggle_mae': l['ensemble']['all']['mae']-k['ensemble']['all']['mae'],
                              'local_minus_kaggle_auroc_plus': l['ensemble']['all']['auroc_plus']-k['ensemble']['all']['auroc_plus']})
    t = local['transfer']
    transfer_strata = []
    for key in ['le3', 'gt3_le4', 'gt4_le5', 'gt5']:
        m, z = t['population']['strata'][key], t['zero_baseline']['strata'][key]
        transfer_strata.append({'stratum': key, 'peptides': m['peptides'],
                               'model_mae': m['mae'], 'zero_mae': z['mae'],
                               'model_minus_zero_mae': m['mae']-z['mae'],
                               'positive_eligible_peptides': m['auroc_plus_eligible_peptides']})
    source_names = ['local-output-analysis.json', 'output-analysis.json', 'output-analysis-details.json']
    results = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'analysis_kind': 'read_only_inventory_and_evidence_export',
        'audit_script_sha256': digest(Path(__file__)),
        'sources': {n: {'sha256': digest(R / n), 'bytes': (R / n).stat().st_size} for n in source_names},
        'data_identity': local['data_identity'],
        'source_hashes_rechecked': len(source_checks),
        'inventory': inventory, 'local_history': histories, 'integrity': local['integrity'],
        'job_categories': dict(Counter(j['category'] for j in jobs)),
        'timing': timing_summary,
        'timing_limitation': 'Recorded worker attempt durations only; resumed jobs may omit prior attempts. Inherited jobs counted once. Neither GPU-active time nor elapsed campaign time.',
        'kaggle_complete_task_recorded_seconds': sum(kaggle['completed_task_seconds'].values()),
        'selected_epochs': epoch_summary, 'lora_updates': adapter_updates,
        'recipes': recipes, 'cross_runtime': cross_runtime,
        'nested_selection': local['nested_selection'], 'contrasts': local['contrasts'],
        'calibration': local['calibration'], 'transfer': t,
        'transfer_strata': transfer_strata,
        'kaggle_diagnostics': details,
        'limitations': local['limitations'],
    }
    (HERE / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    lines = ['# Rà soát toàn bộ output — 06/11/2026', '',
             '[ĐO] Rà soát chỉ đọc; không huấn luyện lại, không sửa state/checkpoint.', '',
             f"- Kiểm lại SHA-256 của {len(source_checks)} nguồn chọn lọc trong phân tích OOF.",
             '- Local: 633 complete, 1 source_pending, 1 structure_pending; 456 job được kế thừa và chỉ tính một lần.',
             '- 88 cấu hình có OOF: 47 Kaggle + 41 local. Cùng dữ liệu W, không phải 88 bộ kiểm định độc lập.',
             '- 540 fold ridge, 30 frozen và 30 LoRA; cả 30 LoRA có tensor adapter thay đổi.', '',
             '## Kiểm kê vật lý', '', '| Nhánh output | File | GiB |', '|---|---:|---:|']
    for name, v in inventory.items():
        lines.append(f"| `{name}` | {v['physical_files']:,} | {v['physical_bytes']/2**30:.3f} |")
    lines += ['', 'File vật lý có thể chứa cache/checkpoint trùng nội dung; không cộng với số artifact đã kiểm hash thành số quan sát khoa học.', '',
              '## Kết quả và giới hạn', '',
              '[ĐO] LoRA-B: MAE 0.363669, AUROC+ 0.855047; LoRA-D: 0.364996 / 0.853556. Cả hai tốt hơn frozen cùng runtime/arm; các CI điều chỉnh hậu kiểm cho bốn so sánh không cắt 0.', '',
              '[DIỄN GIẢI] B và D gần nhau ở trung bình nhưng khác theo WT PSI. Không chọn B chỉ từ hạng MAE; D tốt hơn ở PSI >5. Không thấy xu hướng tăng kích thước pLM luôn tốt hơn.', '',
              '[ĐO] Brier CV của LoRA giảm nhưng ECE+ tăng so với frozen. Đây là hai khía cạnh khác nhau; không kết luận xác suất đã được hiệu chuẩn tốt trong mọi miền.', '',
              '[ĐO] W5-D trên T có ΔMAE so với đoán 0 = -0.003256, CI95 [-0.009249, 0.002760]. PSI >5 có MAE 0.442783 so với 0.346964 của đoán 0. Xác suất dương trung bình 0.089529 vượt tỷ lệ thực 0.051155.', '',
              '[DIỄN GIẢI] AUROC+ tốt không chứng minh độ chính xác hồi quy hay hiệu chuẩn chuyển miền. T chỉ R/A/S, rep1, cùng phòng thí nghiệm và nguồn đã từng thăm dò; LoRA chưa được đánh giá trên T.', '',
              '## Thời gian và epoch', '',
              'Thời gian dưới đây là tổng duration ghi ở attempt hoàn tất; một job resume có thể thiếu các attempt trước. Không diễn giải là GPU-active hoặc tổng thời gian người dùng chờ.', '',
              '| Nhóm | Job | Duration ghi nhận (giờ) |', '|---|---:|---:|']
    for name, v in timing_summary.items():
        lines.append(f"| {name} | {v['jobs']} | {v['recorded_seconds_sum']/3600:.3f} |")
    lines += ['', '| Cấu hình | Fold | Epoch min / median / max |', '|---|---:|---:|']
    for name, v in epoch_summary.items():
        lines.append(f"| {name} | {v['folds']} | {v['min']} / {v['median']:g} / {v['max']} |")
    lines += ['', '## Tái tạo và nguồn', '',
              'Từ gốc repo: `.venv/Scripts/python.exe topics/degron-footprint/research/output-review-2026-11-06/audit.py`.', '',
              'Chạy `analyze-output.py` / `analyze-local-output.py` ở campaign nếu cần tính lại OOF; audit này tái kiểm hash 76 nguồn và xuất bảng từ các phân tích đã kiểm invariants. Không phải một thư viện metric độc lập.', '',
              'Số chính xác, toàn bộ 88 cấu hình, seed, strata, CI, lựa chọn nested và nguồn hash: [results.json](results.json).', '',
              'Chi tiết nền: [Kaggle](../kaggle-roadmap-2026-10-31/output-analysis.md), [Kaggle diagnostics](../kaggle-roadmap-2026-10-31/output-analysis-details.md), [Local](../kaggle-roadmap-2026-10-31/local-output-analysis.md).', '',
              'Cần làm tiếp: final refit/export/calibrator/card theo kiến trúc, kiểm định nguồn ngoài/cấu trúc có dữ liệu hợp lệ, tích hợp và nghiệm thu phần mềm. Không tự thay model phục vụ từ leaderboard.', '']
    (HERE / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'sources': len(source_checks), 'recipes': len(recipes), 'epochs': epoch_summary, 'timing': timing_summary}, indent=2))


if __name__ == '__main__':
    main()
