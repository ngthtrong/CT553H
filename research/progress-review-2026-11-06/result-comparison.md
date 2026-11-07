# So sánh kết quả theo protocol — 06/11/2026

[ĐỐI CHIẾU JSON] Các số dưới được trích từ JSON đã lưu; không huấn luyện lại, không coi đây là kết quả tái lập độc lập. Mỗi nhóm giữ nguyên population, endpoint và quy tắc ensemble. Bảng không tạo một leaderboard chung giữa scanning, saturation, full-PSI và domain gate. Danh sách đủ 88 recipe current, seed/strata và chi phí nằm trong phụ lục báo cáo và [output-review/results.json](../output-review-2026-11-06/results.json); kiểm campaign hiện tại ở [local-audit.md](local-audit.md).

## 1. H-scan và H-transfer: cùng biểu diễn, khác population

Nguồn: [model.json](../residue-task-derisk-2026-10-15/model.json). Cột scanning là **trung bình metric qua seed**; không thay nó bằng AUROC của ensemble saturation. Scanning có 2.994 peptide trước eligibility AUROC; H-transfer chấm 91 peptide saturation sau chặn scanning cùng cụm test.

| Biểu diễn | H-scan AUROC trung bình seed | H-transfer AUROC (`value` đã lưu) |
|---|---:|---:|
| M0_composition_only | 0.839300 | 0.707100 |
| M1_plus_position_index | 0.844500 | 0.719400 |
| M2_plus_window_composition | 0.862500 | 0.724100 |
| M3_plus_ordered_context | 0.868200 | 0.727300 |
| M4_context_and_position | 0.868400 | 0.725300 |

Chênh giữa hai cột không phải treatment effect: đã đổi dữ liệu train/test và phân phối phép thay. Baseline M0 gồm 40 one-hot WT/mutant và 20 composition; không phải chỉ composition.

## 2. H-sat: G2 và P0 giữ cùng 91 peptide/89 nhóm/47.847 ô test

Nguồn G2: [results.json](../g2-saturation-2026-10-18/results.json). Tất cả là macro AUROC trong peptide; hướng sự kiện ΔPSI≥1. Điểm Degformer public được giữ để minh họa overlap, không phải đối chứng tổng quát hóa sạch.

| G2 model | Ensemble/frozen AUROC | Trạng thái |
|---|---:|---|
| DeltaPAP | 0.769284 | Đã đo theo G2; development |
| ridge | 0.808186 | Đã đo theo G2; development |
| gate_pap | 0.800225 | Đã đo theo G2; development |
| no_gate_pap | 0.793727 | Đã đo theo G2; development |
| gate_no_pap | 0.801510 | Đã đo theo G2; development |
| Degformer | 0.924814 | Overlapping checkpoint: 42.163/47.847 mutant cells và WT cả 91 peptide trong training |

P0 Ridge train≤4: **0,820822** trên cùng H-sat test; so train≤3 0,808186: Δ 0.012636, CI95 [+0.006122, +0.018994]. Nguồn: [learning-curve/results.json](../learning-curve-2026-10-22/results.json). R0 tái lập các số này, không cung cấp bộ test mới. P1 Ridge 100%−50% CI95 [-0.000935, +0.008656]; không đủ bằng chứng cho giả thuyết thiếu nhãn theo tiêu chí P1.

## 3. H-sat: transfer, cleaned training exposure và PLM

Cùng test H-sat nhưng từng recipe có nguồn/fit policy khác. Chỉ suy đóng góp thành phần từ đối chứng tương ứng trong protocol, không từ việc so hàng khác nghiên cứu.

| Nhánh | AUROC ensemble | Đối chứng/diễn giải | Nguồn |
|---|---:|---|---|
| P3 ext / ridge | 0.820822 | Đối chứng cùng protocol P3 | [P3 JSON](../pretrain-p3-2026-10-22/results.json) |
| P3 ext / rand | 0.817488 | Đối chứng cùng protocol P3 | [P3 JSON](../pretrain-p3-2026-10-22/results.json) |
| P3 ext / pre | 0.809819 | Pretraining Voutsinos không thiết lập lợi ích | [P3 JSON](../pretrain-p3-2026-10-22/results.json) |
| R1 cleaned Degformer | 0.806775 | So Ridge ext4 ΔCI95 [-0.028298, +0.000974]; chưa chứng minh superiority/equivalence | [R1 JSON](../r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json) |
| R2 / M3 | 0.820822 | PCA64/Ridge, ESM2-650M; không cùng head CNN R6 | [R2 JSON](../r2-esm-features-2026-10-22/run-kaggle-20261022/results.json) |
| R2 / M3+ESM | 0.823039 | PCA64/Ridge, ESM2-650M; không cùng head CNN R6 | [R2 JSON](../r2-esm-features-2026-10-22/run-kaggle-20261022/results.json) |
| R2 / ESM | 0.785347 | PCA64/Ridge, ESM2-650M; không cùng head CNN R6 | [R2 JSON](../r2-esm-features-2026-10-22/run-kaggle-20261022/results.json) |
| Merge / A1_sat_ext | 0.820822 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / S0_scan_only@thr4.0 | 0.727690 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / S1_pool_naive@thr4.0 | 0.818922 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / S2_pool_source@thr4.0 | 0.820344 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / S3_scan_prior@thr4.0 | 0.819749 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / N1_rand | 0.815373 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |
| Merge / N2_scan_pre_lr0.002 | 0.816830 | Ridge pooling chưa tốt hơn A1; neural recipe là đối chứng riêng | [Merge JSON](../scan-sat-merge-2026-10-23/results.json) |

## 4. H-sat: R6 đối chứng biểu diễn/head và ngữ cảnh

Nguồn: [R6 results.json](../r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json). Seed 17/29/43, fixed legacy folds; bảng điểm ensemble không thay trung bình metric từng seed.

| Recipe | Ensemble AUROC |
|---|---:|
| esm150_mcnn | 0.821244 |
| esm35_cnn1 | 0.826394 |
| esm35_mcnn | 0.830490 |
| esm35_mcnn+scan_ft | 0.829874 |
| esm35_mcnn+scan_pool | 0.836670 |
| esm650_mcnn | 0.824286 |
| esm8_mcnn | 0.826500 |
| oh_cnn1 | 0.812747 |
| oh_mcnn | 0.816805 |
| oh_mcnn+scan_ft | 0.831466 |
| oh_mcnn+scan_pool | 0.824152 |
| ridge_M3 | 0.820822 |
| ridge_W10 | 0.818231 |
| ridge_W5 | 0.828637 |
| ridge_W7 | 0.825471 |
| ridge_esm150 | 0.820682 |
| ridge_esm35 | 0.823387 |
| ridge_esm650 | 0.823038 |
| ridge_esm8 | 0.821393 |
| ridge_scan_pool | 0.813758 |
| ridge_scan_pool_t3 | 0.817291 |
| ridge_scan_prior | 0.819041 |
| ridge_scan_prior_t3 | 0.819173 |

| Contrast | Δ AUROC | CI dùng kết luận | Phạm vi | Kết luận JSON |
|---|---:|---|---|---|
| P_esm35_mcnn_vs_ridge | 0.009668 | [-0.002516, +0.023258] | primary, m=1 | chưa đủ bằng chứng (CI phủ 0) |
| A_ridge_W5_vs_W3 | 0.007814 | [+0.002116, +0.013917] | A, m=3 | nhận |
| S1_esm35_mcnn_vs_oh_mcnn | 0.013685 | [+0.002526, +0.026172] | secondary, m=1 | nhận |
| S6_esm35_mcnn_vs_esm35_cnn1 | 0.004096 | [-0.000504, +0.008679] | secondary, m=1 | chưa đủ bằng chứng (CI phủ 0) |
| S7_esm35_mcnn_vs_ridge_W5 | 0.001854 | [-0.011533, +0.016449] | secondary, m=1 | chưa đủ bằng chứng (CI phủ 0) |
| G_oh_mcnn_scan_ft_vs_scratch | 0.014661 | [+0.002720, +0.027593] | G, m=4 | nhận |
| G_esm35_mcnn_scan_pool_vs_scratch | 0.006180 | [-0.008582, +0.021095] | G, m=4 | chưa đủ bằng chứng (CI phủ 0) |

Primary P chưa đạt; nhận một contrast họ G không thay phán quyết P. Các secondary contrasts không có một global family adjustment chung; trình bày theo đúng gia đình ghi trong JSON, không gọi mọi contrast là xác nhận độc lập.

## 5. Calibration H-sat và Domain-R3 là endpoint riêng

P6 calibration: [results.json](../calibration-p6-2026-10-22/results.json), event nhị phân ΔPSI≥1. Brier nhị phân này không cùng chuẩn với tổng squared error ba lớp của v3.

| Calibrator | Binary Brier | ECE |
|---|---:|---:|
| raw | 0.127165 | 0.143658 |
| const | 0.113939 | 0.015357 |
| platt | 0.092541 | 0.016314 |
| iso | 0.092523 | 0.016422 |

R3: [results.json](../r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json), 235 peptide/222 nhóm, nhãn domain = intrinsic WT PSI≤4; không phải mutation-effect AUROC.

| Gate | Domain AUROC OOF | Binary Brier |
|---|---:|---:|
| tier1 | 0.911113 | 0.091524 |
| tier2_stage_B | 0.815389 | 0.143406 |

## 6. Full-PSI W và locked-transfer T

Các dòng dưới đều là ensemble dự đoán ba seed trên W (235 peptide/221 nhóm/122.412 cell), MAE macro theo peptide và AUROC+ trên 184 peptide đủ điều kiện. Chúng được chia theo runtime; chỉ các contrast matched mới cô lập tương đối rõ can thiệp tương ứng. Không dùng thứ tự dòng để suy một thang tăng tiến qua các protocol.

| Kaggle recipe | MAE | AUROC+ |
|---|---:|---:|
| W5-B | 0.433577 | 0.831179 |
| W5-D | 0.407803 | 0.831933 |
| W5-E | 0.403613 | 0.827521 |
| ESM2-35M CNN-D | 0.384354 | 0.848816 |
| ESM2-35M mCNN-E | 0.383846 | 0.847004 |
| One-hot CNN scratch-D | 0.393611 | 0.829131 |
| One-hot CNN scanning rep1-D | 0.387226 | 0.842494 |

| Local recipe | MAE | AUROC+ |
|---|---:|---:|
| Nested family selector | 0.394454 | 0.840882 |
| ESM2-35M frozen-B | 0.403385 | 0.826268 |
| ESM2-35M LoRA-B | 0.363669 | 0.855047 |
| ESM2-35M frozen-D | 0.390382 | 0.824625 |
| ESM2-35M LoRA-D | 0.364996 | 0.853556 |

Matched local LoRA giảm MAE so frozen cùng arm; mCNN-E/CNN-D khác cả training arm nên không cô lập riêng multi-scale. T là population khác: W5-D MAE 0.399147 so zero 0.402403, ΔMAE −0.003256, CI95 [−0.009249,+0.002760]; AUROC+ 0.840546 dùng 338 peptide eligible trên tổng 1.410 peptide. Không có LoRA T để điền thêm hàng.

Các bảng đầy đủ current được giữ tại [output-review results](../output-review-2026-11-06/results.json), [Kaggle analysis JSON](../kaggle-roadmap-2026-10-31/output-analysis.json) và [local analysis JSON](../kaggle-roadmap-2026-10-31/local-output-analysis.json). Bảng trong báo cáo/phụ lục chứa đủ 47 recipe Kaggle và 41 local; 88 recipe cùng dùng W, không phải 88 test cohorts.

- So current với lịch sử phải giữ W=235/221/122.412 và legacy test=91/89/47.847 riêng; AUROC eligibility không luôn bằng tổng peptide MAE.
- So frozen/LoRA phải dùng cùng local runtime; frozen Kaggle seed17 chỉ là snapshot riêng.
- T chỉ W5-D; không có LoRA T. Một AUROC tốt không thay MAE/zero baseline hay calibration chuyển miền.
- Epoch/duration là log của các fit/attempt đã ghi; không tự gọi là GPU-active time, energy hoặc wet-lab cost.

Xem [experiment-history.md](experiment-history.md) cho quyết định nghiên cứu và [data-method-audit.md](data-method-audit.md) cho QC, units, missingness và giới hạn công bằng.
