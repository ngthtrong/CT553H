# Draft protocol — full-PSI và khảo sát pLM

**Trạng thái: thiết kế 31/10/2026, CHƯA KHÓA, CHƯA CHẠY.** Các kết quả cũ và kiểm kê nhãn đã được xem. Không gọi tài liệu này là preregistration độc lập với dữ liệu đã biết. Trước triển khai cần đóng các lựa chọn còn ghi draft, băm protocol/config/splits rồi nhúng vào notebook.

## 1. Câu hỏi nghiên cứu

| Mã | Câu hỏi | Phép so chính dự kiến |
|---|---|---|
| Q1 | Bỏ ngưỡng PSI của tập fit giúp gì cho hồi quy toàn dải, và có giữ được chất lượng miền cũ? | Train-full và full-balanced so train≤4, cùng W outer-test, Ridge W5 |
| Q2 | Họ/cỡ pLM nào cung cấp thông tin bổ sung ngoài baseline ngữ cảnh? | Frozen representation + cùng đầu Ridge/PCA so W5; chọn recipe trong inner CV |
| Q3 | Học trộn các vị trí có thêm giá trị sau khi có pLM? | ESM35 pointwise so CNN k5; mCNN là phép phụ |
| Q4 | Replicate/source-aware transfer có giúp trong điều kiện scanning chỉ có 20 cặp? | Recipe chỉ saturation so recipe dùng scan_dev; tách 20/360 cặp trên saturation |
| Q5 | Kết quả có chuyển sang peptide/assay khác và xác suất có ích không? | Các recipe đã khóa trên cùng T, calibration chỉ fit trên development |
| Q6 | Thông tin cấu trúc có thêm giá trị trong cohort map được? | SaProt cùng checkpoint true-3Di so masked-3Di, kèm sequence baseline cùng cohort |

Đóng góp benchmark/phương pháp/đánh giá là đủ; Q3/Q6 không bắt buộc dương. Q6 và nguồn mới không phải đường găng của lõi.

## 2. Phân biệt đánh giá lịch sử và đánh giá mới

- **L-reproduce:** nguyên nhãn, 91 peptide, 47.847 ô, folds/metric của G2/P0. Kiểm M3 base 0,808186 và ext4.0 0,820822 trong dung sai AUROC 1e-4; verify inference theo dung sai lịch sử. Cổng này là tái lập số học, không phải kiểm độc lập.
- **L-new:** áp arm train mới, giữ population test L nhưng kiểm cụm và preprocessing theo protocol mới. Nếu một quy tắc chống leakage/final-fit làm đổi tập fit, báo là thiết kế mới; không ép khớp số cũ hoặc dùng delta giữa hai thiết kế như tác động riêng của full-PSI.
- **W:** nested grouped CV trên 235 peptide qua QC; folds mới sau audit group. Dùng cùng W outer/inner assignment cho các arm/model. Tập đã biết vẫn là development; số fold tăng không tạo dataset độc lập.
- **T-scan:** đánh giá chuyển nguồn trên phần đã giữ riêng và khai báo lịch sử thăm dò. Source khác assay chỉ được coi độc lập trong phạm vi overlap/history audit xác nhận, không vì khác tên file.

Tái lập L cũ không cấp quyền bỏ qua một cross-split hit phát hiện trong W. Bảng legacy và bảng W luôn tách.

## 3. Ma trận dữ liệu và ngân sách

### 3.1 Các arm của Q1

| Arm | Tập fit có giám sát | Trọng số | Vai trò |
|---|---|---|---|
| A | PSI(WT)≤3 | theo ô như baseline | Mốc hẹp |
| B | PSI(WT)≤4 | theo ô | Mốc chính có bằng chứng lịch sử |
| C | PSI(WT)≤5 | theo ô | Độ nhạy |
| D | Toàn bộ qua QC | theo ô | Giả thuyết bỏ ngưỡng |
| E | Toàn bộ qua QC | cân bằng stratum, peptide trong train | Giả thuyết phân bố che lợi ích |

Chạy đủ năm arm với **Ridge W5** trên W; M3 B và L-reproduce làm neo. Đối chứng tuyến tính pair-only/composition/window-unordered/ordered chạy trên B và D để tránh tích Descartes mọi view×mọi feature. Khi 05 kiểm mạng, chỉ B/D/E và số model/head hữu hạn; A/C không tự nhân sang mọi pLM.

Quality weighting là họ kiểm định riêng trong 06, không cộng vào Q1 sau khi thấy D/E. Learning curve theo số cụm trên full pool là thí nghiệm phụ của 01, chỉ W5 và một mạng đã định trước, fractions 25/50/75/100; subsets lồng nhau, outer-test không đổi. Không ngoại suy curve vượt số cụm hiện có như bằng chứng mạng chắc chắn sẽ thắng.

### 3.2 Inner validation và ngưỡng fit

W dùng common inner validation toàn dải để chọn regularization cho mục tiêu toàn dải. Ngưỡng A/B/C chỉ lọc **hàng dùng khớp hệ số**, không lọc outer-test. Vì validation có PSI cao, không mô tả A/B là hoàn toàn chưa từng sử dụng thông tin nhãn ở PSI cao trong mọi bước chọn model.

Mỗi inner split: fit scaler/PCA trên `inner_train ∩ arm_filter`; chọn α/epoch bằng common inner-validation; final fit scaler/PCA/model trên `outer_train ∩ arm_filter` theo recipe đã định. Nếu refit mạng, số epoch chọn từ inner-validation rồi fit lại trên outer-train hợp lệ; không early-stop bằng outer-test. Có thể chọn không refit cho cả hai họ, nhưng phải khóa một quy tắc chung trước chạy.

Luồng L dùng quy tắc historical riêng cho tái lập; bảng mới ghi rõ quy tắc final-fit. Không trộn ensemble mạng với trung bình metric seed và coi là cùng đại lượng.

## 4. Chọn model nhiều họ mà không mở số thử vô hạn

- Danh sách checkpoint ở `model-registry.json`; model cùng checkpoint khác precision/quantization là cấu hình khác, không thay lén sau OOM.
- Bước 02 quyết định **khả thi tài nguyên**, dựa trên probe không nhãn, không dùng AUROC/MAE test để bỏ model.
- Bước 03 trích một lần WT/Δ pooled, không lưu attention/all-layers hoặc crop của mọi model.
- Bước 04 dùng recipe cố định: W5, ESM features-only, W5+ESM features. Chính là W5+PCA64(Δsite; mean Δ), PCA/scaler chỉ học trong train; tên recipe đổi theo họ, không ngầm dùng ESM cho mọi pLM.
- Shortlist head ở 05: ESM35 là anchor, thêm **tối đa một họ khác được chọn trong inner validation**. Nếu shortlist thay đổi qua outer fold, đó là đánh giá một quy trình chọn model; không ghép các fold rồi nói một checkpoint cố định đã thắng.
- Không chọn một họ/cỡ từ toàn bộ W outer OOF rồi báo chính OOF đó là ước lượng xác nhận không chệch. Có thể báo bảng development đầy đủ, khóa final recipe và đánh giá T sau.
- ESM-1v: checkpoint `_1` là đối chứng riêng đã định; ensemble `_1…_5` là một recipe khác có chi phí năm checkpoint, không phải năm dataset độc lập.
- Không fine-tune toàn bộ mọi pLM. PEFT/LoRA chỉ là nhánh sau khi frozen probe đủ khả thi và protocol riêng có ngân sách; không cần cho completion lõi.

## 5. Metrics và population

### 5.1 Hồi quy

**Chỉ số chính W: MAE macro theo peptide**, ô hợp lệ trong peptide được lấy trung bình trước, rồi trung bình các peptide. Báo thêm RMSE macro, pooled RMSE có nhãn rõ, Spearman trong peptide, bốn PSI strata và n peptide/cụm/ô. MAE macro coi peptide có số ô khác nhau có vai trò tương đương; không dùng sample weighting train để đổi metric test.

Baseline luôn có constant/mean train và W5. Một mô hình đoán gần 0 có thể đạt MAE dễ nhìn do nhiều hiệu ứng nhỏ; vì vậy phải đọc cùng metric dấu/hiệu ứng mạnh và cải thiện so baseline. Không dùng PSI(WT) thật của test để clip dự đoán vào giới hạn có điều kiện.

### 5.2 Hiệu ứng dương và âm

- Dương: `ΔPSI≥1`; âm: `ΔPSI≤−1`; neutral: ở giữa. Học target liên tục, không gán nhãn motif/gain-of-degron sinh học từ dấu một cách tự động.
- Báo AUROC/AUPRC trong peptide khi có ≥3 ô mỗi lớp của event được xét; ghi n đủ điều kiện và n bị loại. AUPRC đi cùng tần suất event. Khi không có đủ hai lớp, metric = null/undefined có reason, không điền 0/0,5.
- Metric W dùng eligibility trên **nhãn đo**, không trên dự đoán; cùng cohort cho paired contrast. L-reproduce dùng đúng eligibility lịch sử để khớp số, không so thẳng metric W đã thay rule với 0,8208.
- Nhóm >5 không có dương≥1; dùng MAE/RMSE, metric event âm và false-positive rate của event dương tại ngưỡng xác suất được chọn trong train/validation. Không dùng AUROC dương để chấm nhóm này.
- Top-k budget cố định 5/10/20%; thêm baseline pair/hydrophobicity hoặc W5 cùng population, không chỉ random. Không gọi enrichment là phần trăm đúng toàn bộ mẫu.
- Nếu xuất residue score, khóa phép gộp (ví dụ mean hiệu ứng 19 phép thay) và mask trước lượt chạy; không chọn mean/max sau khi xem kết quả. Giữ ma trận substitution là đầu ra gốc.

## 6. CI, tiêu chí và selection

- Seed training 17/29/43; cùng outer assignment. Report từng seed, mean seed metric và metric trên mean prediction riêng. Seed không phải đơn vị thống kê độc lập.
- Paired bootstrap **5.000 lần theo group protein sau kiểm leakage**, giữ các peptide/ô đi cùng group. Metric strata báo n group và số bootstrap hợp lệ; không đếm mutation cells như mẫu độc lập.
- Họ chính Q1 gồm D−B và E−B theo MAE macro; báo CI Bonferroni cho hai contrast (mức từng CI 97,5%) và CI95 mô tả. Hướng có lợi là delta MAE âm. Không lấy một guardrail AUROC âm/dương làm kết luận thay primary MAE.
- Ngưỡng thực dụng là **draft cần chốt trước chạy**: giảm MAE tối thiểu 0,02 PSI; miền ≤3 không giảm AUROC quá 0,01. CI chứa cả cải thiện và suy giảm → chưa phân giải; CI phủ 0 không chứng minh tương đương. Không nới ngưỡng sau khi thấy kết quả.
- Q2: đánh giá nested selection recipe so W5 là một contrast chính; bảng từng họ là development, không 18 phép primary độc lập. Nếu muốn kết luận từng họ, khóa family multiplicity trước chạy và báo tất cả.
- Q3: pointwise vs CNN k5 là primary; mCNN vs CNN/pointwise là phụ; ghi số tham số/FLOPs/budget. Q4/Q6 là họ riêng, không dùng kết quả phụ để cứu Q1/Q2.
- Giới hạn tài nguyên và missing runs phải xuất hiện trong bảng; không cho missing arm giá trị dự đoán hoặc gộp smoke vào chính thức.

## 7. Calibration và quyết định cuối

- Cross-fit calibration trên development OOF cùng target domain. Nếu dùng ba class (âm/neutral/dương), dùng một mô hình xác suất nhất quán hoặc kiểm `p_plus+p_minus≤1`; không trưng hai xác suất độc lập mâu thuẫn như phân bố ba class.
- Report Brier/reliability/ECE và tần suất nền theo miền; sample count/CI cho event âm. Không mang nguyên bộ Platt M3 sang W5 hoặc model khác.
- Hiệu chuẩn trên source/stratum nào chỉ có bằng chứng ở đó. Không refit calibration trên T rồi gọi score calibrated là đánh giá transfer nguyên trạng.
- Model được chọn bằng quy tắc ghi trước kết hợp MAE/event utility/độ ổn định/chi phí, không có yêu cầu mạng thắng. Đóng băng model/calibrator/data/feature/extractor versions và benchmark inference CPU/GPU thực.
- Nếu W phát triển hỗ trợ full-PSI, phải có model card phạm vi mới; không tự bỏ gate của model cũ chỉ vì đã thêm train. W là thư viện được chọn, không chứng minh phục vụ mọi peptide/protein.

## 8. Điều kiện dừng

Hash/nhãn/fold lệch; group/sequence xuyên split; thiếu map bị giả singleton; tokenizer không 1 residue↔1 representation; NaN/Inf; mask sai; PCA/weights thấy test; T lọt scan_dev; chưa đủ tài nguyên/tải weights: dừng nhánh liên quan, ghi `failed_gate`, `resource_blocked` hoặc `source_pending`. Không thay checkpoint/precision/target sau khi lỗi mà vẫn giữ cùng run ID.

Mỗi notebook có `SMOKE=True` riêng. Smoke chỉ kiểm đường code/tài nguyên; kết quả ghi rõ mode và không được vào bảng scientific results. Kết quả chính phải có manifests, data/split/protocol/checkpoint hashes, OOF row IDs và env.
