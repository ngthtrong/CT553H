#!/usr/bin/env python3
"""Read recorded evidence. Never run experiments or collect partial local scores."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
ROOT = next(p for p in HERE.parents if (p / 'CLAUDE.md').exists())
RES = ROOT / 'topics/degron-footprint/research'
SOURCES = [
 ('NC-01', 'Dựng lại PSI và kiểm nhãn', 'full-data-audit/psi-build.json'),
 ('NC-02', 'Benchmark saturation ban đầu', 'g2-saturation-2026-10-18/results.json'),
 ('NC-03', 'Audit benchmark ban đầu', 'g2-saturation-2026-10-18/audit.json'),
 ('NC-04', 'Đường cong học và mở ngưỡng', 'learning-curve-2026-10-22/results.json'),
 ('NC-05', 'Phân tách lượng nhãn và phân bố', 'learning-curve-2026-10-22/results-b.json'),
 ('NC-06', 'Độ nhạy ngưỡng', 'learning-curve-2026-10-22/results-c.json'),
 ('NC-07', 'Tiền huấn luyện tile-label', 'pretrain-p3-2026-10-22/results.json'),
 ('NC-08', 'Hiệu chuẩn baseline', 'calibration-p6-2026-10-22/results.json'),
 ('NC-09', 'Kiểm khớp đường suy luận', 'calibration-p6-2026-10-22/verify.json'),
 ('NC-10', 'Tái lập notebook R0', 'r0-reproduce-notebook-2026-10-22/run-kaggle-20261022/results.json'),
 ('NC-11', 'Degformer sạch cụm', 'r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json'),
 ('NC-12', 'ESM và ridge', 'r2-esm-features-2026-10-22/run-kaggle-20261022/results.json'),
 ('NC-13', 'Cổng miền R3', 'r3-domain-gate-2026-10-22/run-kaggle-20261022/gate-card.json'),
 ('NC-14', 'Ngữ cảnh, biểu diễn và đầu mạng R6', 'r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json'),
 ('NC-15', 'Bundle full-PSI', 'kaggle-roadmap-2026-10-31/dataset-build.json'),
 ('NC-16', 'Phân tích Kaggle full-PSI', 'kaggle-roadmap-2026-10-31/output-analysis.json'),
 ('NC-17', 'Chẩn đoán full-PSI hậu nghiệm', 'kaggle-roadmap-2026-10-31/output-analysis-details.json'),
 ('NC-18', 'Nhãn đo HIF1A minh họa', 'slide-figures-2026-10-15/example-matrix.json'),
 ('NC-19', 'Audit Koren', 'koren-s4-audit-2026-10-22/results.json'),
 ('NC-20', 'Độ nhạy phân cụm', 'recluster-sensitivity-2026-10-22/results.json'),
 ('NC-21', 'Sổ nguồn dữ liệu và điều kiện dùng', '../data/README.md'),
 ('NC-22', 'Audit giới hạn nhãn E3', 'e3-labels-audit/README.md'),
 ('NC-23', 'Audit độ phủ và liên quan ClinVar', 'variant-coverage-2026-10-15/README.md'),
 ('NC-24', 'Đối chứng biểu diễn lịch sử', 'residue-task-derisk-2026-10-15/model.json'),
 ('NC-25', 'Trộn scanning–saturation', 'scan-sat-merge-2026-10-23/results.json'),
 ('KH-01', 'Kế hoạch local đã chốt', 'kaggle-roadmap-2026-10-31/local-plan.json'),
 ('KH-02', 'Protocol thực thi full-PSI', 'kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md'),
 ('KH-03', 'Kế hoạch/runtime local, không lấy metric', 'kaggle-roadmap-2026-10-31/output/local/e7097449883a51d8/plan.json'),
 ('PM-01', 'Phạm vi và trạng thái hệ thống hiện hành', '../system/README.md'),
 ('PM-02', 'Baseline ứng dụng và các kiểm tra lịch sử', '../system/app/README.md'),
 ('PM-03', 'Workspace UI v2: fixture và giới hạn review', '../system/design/workspace-ui-v2/README.md'),
]

def main():
    docs = {}
    records = []
    for sid, title, rel in SOURCES:
        path = RES / rel
        raw = path.read_bytes()
        records.append(dict(id=sid, title=title, path=str(path.relative_to(ROOT)),
                            sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)))
        if path.suffix == '.json':
            docs[sid] = json.loads(raw)
    g2, v3, dataset = docs['NC-02'], docs['NC-16'], docs['NC-15']
    assert (g2['n_peptides'], g2['n_clusters'], g2['n_cells']) == (91, 89, 47847)
    assert v3['scientific_status'] == 'development_not_gate_closure'
    assert docs['KH-03']['data_identity'] == v3['data_identity']
    vals = {
      'SAT_PEPTIDES': str(dataset['saturation_peptides']),
      'SAT_CELLS': f"{dataset['saturation_cells']:,}".replace(',', '.'),
      'SAT_GROUPS': str(dataset['saturation_groups']),
      'SCAN_CELLS': f"{dataset['scan_cells']:,}".replace(',', '.'),
      'BASE_AUC': f"{g2['macro_auroc']['ridge']:.4f}".replace('.', ','),
      'DPAP_AUC': f"{g2['macro_auroc']['DeltaPAP']:.4f}".replace('.', ','),
      'EXT_AUC': f"{docs['NC-04']['results']['ridge']['ext']['macro_auroc_ensemble']:.4f}".replace('.', ','),
      'R1_AUC': f"{docs['NC-11']['macro_auroc_ensemble']:.4f}".replace('.', ','),
      'R6_W5_AUC': f"{docs['NC-14']['summaries']['ridge_W5']['macro_auroc_ensemble']:.4f}".replace('.', ','),
      'R6_MCNN_AUC': f"{docs['NC-14']['summaries']['esm35_mcnn']['macro_auroc_ensemble']:.4f}".replace('.', ','),
    }
    selection = [('W5_B','ordered-w5-B'),('W5_D','ordered-w5-D'),('W5_E','ordered-w5-E'),
                 ('POINT_D','esm2_35m-pointwise-D'),('CNN_D','esm2_35m-cnn-D'),('MCNN_E','esm2_35m-mcnn-E'),
                 ('SCRATCH_D','cnn-transfer-scratch-D'),('SCAN_PRETRAIN_D','cnn-transfer-dpsi_rep1-D')]
    for key, recipe in selection:
        assert v3['recipes'][recipe]['seeds'] == [17,29,43]
        vals[key] = f"{v3['recipes'][recipe]['ensemble']['all']['mae']:.5f}".replace('.', ',')
    result = dict(date='2026-11-03', scope='Sequential learning; saved development evidence; local plan only',
                  sources=records, values=vals, data_identity=v3['data_identity'],
                  historical=dict(g2=g2['macro_auroc'],curve=docs['NC-04']['results'],
                                  r6=docs['NC-14']['summaries'],r6_contrasts=docs['NC-14']['contrasts']),
                  fullpsi=dict(recipes=v3['recipes'],contrasts=v3['contrasts'],dataset=dataset,
                               learning_curve=docs['NC-17']['learning_curve']),
                  calibration=docs['NC-08']['metrics'], hif=docs['NC-18'],
                  local_plan=dict(config=docs['KH-01'],training=docs['KH-03']['training'],
                                  features=docs['KH-03']['features'],selection=docs['KH-03']['selection']),
                  exclusions=['No local fit metrics or partial LoRA performance collected',
                              'No new training, live-worker check or scientific acceptance'])
    (HERE/'evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'Collected {len(records)} sources; local predictive results excluded')

if __name__ == '__main__':
    main()
