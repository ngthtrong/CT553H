# Bảng bằng chứng đã có

Sinh bằng `build_evidence.py`; số được trích từ JSON đã lưu, không phải lượt huấn luyện mới. Đường dẫn và SHA-256 nguồn: [evidence.json](evidence.json). Cách diễn giải và khoảng trống: [README.md](README.md).

## R6: cùng outer-test 91 peptide / 89 cụm

AUROC mức ô, macro theo peptide. `Mean seed` là trung bình AUROC từng seed; `Ensemble` là AUROC của điểm dự đoán trung bình ba seed.

| Cấu hình | Seed 17 | Seed 29 | Seed 43 | Mean seed | Ensemble |
|---|---:|---:|---:|---:|---:|
| `ridge_M3` | 0.8204 | 0.8210 | 0.8209 | 0.8208 | 0.8208 |
| `ridge_W5` | 0.8276 | 0.8288 | 0.8291 | 0.8285 | 0.8286 |
| `oh_cnn1` | 0.8102 | 0.8015 | 0.8036 | 0.8051 | 0.8127 |
| `oh_mcnn` | 0.8117 | 0.8058 | 0.8083 | 0.8086 | 0.8168 |
| `ridge_esm35` | 0.8234 | 0.8226 | 0.8240 | 0.8233 | 0.8234 |
| `esm35_cnn1` | 0.8239 | 0.8181 | 0.8125 | 0.8181 | 0.8264 |
| `esm35_mcnn` | 0.8280 | 0.8202 | 0.8183 | 0.8222 | 0.8305 |

Nguồn: [results.json R6](../r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json).

## Phép so R6: giữ nguyên vai trò và kết luận nguồn

P là phép xác nhận duy nhất của R6; S* là phép phụ/mô tả. CI dùng kết luận lấy `ci_adj` (bằng `ci95` khi m=1). Dấu từng seed lấy từ so hai seed tương ứng, không lấy từ hiệu ensemble.

| Phép so | Vai trò | Δ ensemble | CI dùng kết luận | Δ seed 17/29/43 | Kết luận nguồn |
|---|---|---:|---|---|---|
| `A_ridge_W5_vs_W3` | A, m=3 | +0.0078 | [+0.0021; +0.0139] | +0.0072/+0.0078/+0.0081 | nhận |
| `P_esm35_mcnn_vs_ridge` | primary, m=1 | +0.0097 | [-0.0025; +0.0233] | +0.0076/-0.0008/-0.0026 | chưa đủ bằng chứng (CI phủ 0) |
| `S1_esm35_mcnn_vs_oh_mcnn` | secondary, m=1 | +0.0137 | [+0.0025; +0.0262] | +0.0163/+0.0144/+0.0100 | nhận |
| `S5_oh_mcnn_vs_oh_cnn1` | secondary, m=1 | +0.0041 | [-0.0031; +0.0109] | +0.0015/+0.0044/+0.0047 | chưa đủ bằng chứng (CI phủ 0) |
| `S6_esm35_mcnn_vs_esm35_cnn1` | secondary, m=1 | +0.0041 | [-0.0005; +0.0087] | +0.0041/+0.0022/+0.0058 | chưa đủ bằng chứng (CI phủ 0) |
| `S7_esm35_mcnn_vs_ridge_W5` | secondary, m=1 | +0.0019 | [-0.0115; +0.0164] | +0.0004/-0.0085/-0.0108 | chưa đủ bằng chứng (CI phủ 0) |

## R2: ESM gộp + PCA + Ridge

ESM-2 650M; PCA-64. Đây không phải đầu không CNN tương ứng hoàn toàn với R6.

| Cấu hình nguồn | Ensemble AUROC |
|---|---:|
| `M3` | 0.8208 |
| `M3+ESM` | 0.8230 |
| `ESM` | 0.7853 |

Nguồn: [results.json R2](../r2-esm-features-2026-10-22/run-kaggle-20261022/results.json).

## Đối chứng tuyến tính lịch sử: khác thiết kế R6

Chỉ dùng để định vị bằng chứng. Không lấy chênh lệch giữa bảng này và R6 để quy tác động cho một thành phần. M0 chứa cặp thay thế và composition.

| Cấu hình | Scanning CV, mean 5 seed | Học scanning → saturation |
|---|---:|---:|
| `M0_composition_only` | 0.8393 | 0.7071 |
| `M2_plus_window_composition` | 0.8625 | 0.7241 |
| `M3_plus_ordered_context` | 0.8682 | 0.7273 |

Nguồn: [model.json lịch sử](../residue-task-derisk-2026-10-15/model.json).

Không có số mới cho pair-only hoặc ESM pointwise tương ứng CNN. Kiểm kê scanning ngoài cụm và hiệu ứng ensemble trong JSON là hậu kiểm đã có.
