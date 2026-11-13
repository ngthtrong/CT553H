# Kiểm chứng độ tin cậy và giới hạn chuyển miền — đợt CPU

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent.
- Origin Mode: validate; phân tích chẩn đoán và chuẩn bị đánh giá tiếp.
- Origin Date: 2026-11-08, Asia/Taipei.
- Verification Status: chưa thực thi tại thời điểm tạo protocol.
- Version Label: reliability_transfer_cpu_v1.

## 1. Phạm vi được phép

Người dùng yêu cầu bắt đầu thực hiện hướng kiểm chứng độ tin cậy và giới hạn
chuyển miền, **không chạy GPU trên môi trường hiện tại**. Đợt này chỉ đọc bảng
nhãn, split, OOF và xác suất đã lưu; không load checkpoint, không import
PyTorch/Transformers, không train/refit/inference, không tải dữ liệu hoặc weights.
Mọi output mới nằm trong thư mục nghiên cứu này. Giữ nguyên data, campaign,
state, manifest gốc, serving model, report, proposal và trạng thái G2/G3.

Protocol/config được lưu trước khi tính các chẩn đoán mới. Tuy nhiên MAE,
AUROC, prioritization và một số residual của W/T đã được xem trong các lượt
trước. Đây là **hậu kiểm development**, không phải preregistration độc lập.
Không dùng kết quả mới để chọn lại recipe hoặc ngưỡng thành công G2.

## 2. Câu hỏi và giả thuyết

1. Lợi ích matched LoRA–frozen có phụ thuộc seed, fold, WT PSI, mức tương đồng
   peptide với tập refit và mức bất đồng hai nửa assay không?
2. Hit ranking cố định có bền khi đổi ngưỡng hiệu ứng và yêu cầu cả hai nửa
   assay cùng xác nhận event không?
3. Regression, event ranking và calibration W5 thay đổi thế nào từ W sang T,
   khi mô tả riêng khác biệt substitution design và target replicate?
4. Bằng chứng nào vẫn thiếu để đánh giá LoRA trên T/nguồn mới?

Giả thuyết định hướng: ranking có thể bền hơn độ chính xác hồi quy; label
uncertainty, endpoint bounds và population shift có thể liên quan sai số.
Không thiết kế nhân quả để quy một nguyên nhân duy nhất. Kết quả âm hoặc
không phân giải được giữ nguyên. Đợt này không chứng minh lợi ích wet lab.

## 3. Input và kiểm tính đúng

- Bundle `data/processed/v3-fullpsi`, identity trong `config.json`.
- W: 122.412 mutation cell, 235 peptide, 221 nhóm; 5 outer fold, seed 17/29/43.
- Core local: frozen-B/D và LoRA-B/D từ campaign `ef138c84579c842e`.
- W5-D: OOF Kaggle đã được pin; calibration CV và T từ job locked-transfer-w5.
- T: prediction đã lưu cho rep1; không dùng lại để lựa chọn model.
- Nhãn saturation a/b là hai nửa assay theo pipeline nguồn; không tự xác nhận
  chúng là hai biological replicate độc lập.

Gate: kiểm SHA/size theo data manifest, campaign state/pipeline manifest và
input manifest prioritization hiện có; metadata/cell/label/fold phải khớp exact.
Không lấy intersection để che thiếu OOF hoặc seed. Xác suất hữu hạn, nằm [0,1],
tổng ba lớp bằng 1. Kiểm lại hash input sau thực thi. Không sửa hash kỳ vọng.

Kiểm group-disjoint và exact WT/mutant sequence trên hợp saturation/scanning.
Exact sequence trùng ở nhiều nhóm là lỗi grouping cần báo; exact sequence
trùng nhiều observation **trong cùng nhóm** là hợp lệ, không gộp nhãn.

## 4. Phân tích đã định

### 4.1. Độ bền development

Tái tính MAE/RMSE, AUROC/AP hai chiều (mỗi lớp ít nhất 3 cell), P@10
trong peptide, prevalence và zero MAE. Báo riêng từng seed và ensemble.
MAE/RMSE và P@10 là peptide-macro; cell-micro có tên riêng.

Matched contrasts: LoRA-B−frozen-B, LoRA-D−frozen-D; bổ sung LoRA-D−W5-D
nhưng ghi rõ cross-runtime, không cô lập riêng adaptation. Đối chiếu các CI
đã công bố; CI subgroup mới là mô tả 95%, không xác nhận superiority mới.
Phân tầng PSI cố định ≤3, (3,4], (4,5], >5; outer fold; bất đồng a/b
[0,.25), [.25,.5), [.5,1), [1,∞) PSI. Bất đồng là metadata nhãn hậu kiểm,
không phải feature hoặc điều kiện lọc deploy.

### 4.2. Tương đồng và leakage

Với mỗi peptide W, reference là peptide của các nhóm outer-train/refit;
arm B chỉ giữ WT PSI≤4, D giữ toàn dải. Với T, reference W5 là toàn W.
Tính max identity **cùng vị trí trên 28 AA, không alignment/gap**, và phần
5-mer duy nhất của query có mặt trong một reference peptide. Bins identity
[0,.25), [.25,.5), [.5,.75), [.75,1]. Không chọn cutoff theo performance.
Các đại lượng này là proxy cục bộ, không thay MMseqs2/remote-homology audit,
không bao gồm pretraining exposure và không chứng minh độc lập sinh học.
Không đổi group, split, train membership hoặc lọc model theo similarity.

### 4.3. Nhãn, ngưỡng và giới hạn assay

- Kiểm dpsi_mean=(a+b)/2, read support và reference riêng từng nửa.
- Báo Pearson a/b, MAE bất đồng, event agreement và prevalence cho threshold
  .75, 1, 1.25 ở cả hai chiều.
- Rank theo score OOF cố định; P@10 chấm nhãn mean, nửa a, nửa b và consensus
  cả hai nửa. Đây là **các target khác nhau**, không phải CI cho hit thật.
- Giữ no-hit peptide trong precision; random expectation là prevalence từng
  peptide. Không chọn threshold/seed tốt nhất hoặc thay primary E5.
- Bounds ΔPSI theo WT PSI chỉ là diagnostic; không clip prediction bằng WT
  PSI đo trên test. Bounds mean saturation được tính từ mean WT hai nửa.
- `reads_a/b` là tổng count đã chuẩn hóa từ pipeline, không được gọi là số
  raw sequencing reads. Chỉ mô tả sensitivity, không ước lượng variance chuẩn.

### 4.4. Chuyển miền đã có prediction

Đối chiếu W-full, W-mutant-R/A/S và W-exact-scanning-pairs (20 directed pairs
theo metadata scanning), đều giữ target mean a/b. Chấm **trong từng peptide**;
candidate pool và k thực tế đổi phải báo n, không coi là so cùng ngân sách E5.
Subset này không tái huấn luyện hoặc matching đầy đủ hai nguồn.

T giữ primary target rep1. Trên intersection có cả rep1/rep2, chấm cùng score
với rep1, rep2 và mean12 trên **cùng cell**; báo primary rep1 full riêng.
Đây là phân tích độ nhạy nhãn, không đổi target chính hoặc chọn model bằng T.
So W5−zero bằng paired protein-group bootstrap trên từng cohort/PSI stratum.
Chênh W–T chỉ là population contrast, không phải treatment effect.

Calibration: Brier 3 lớp, log loss với epsilon cố định chỉ để tính log,
ECE hai chiều với 10 bin equal-width, calibration-in-the-large và reliability
table kèm cell/peptide/group count. Báo micro và macro Brier riêng.
Không fit/recalibrate trên T. Không suy Brier giảm nghĩa mọi mặt calibration tốt.

## 5. Thống kê, ties và cách kết luận

- Cluster bootstrap 5.000 lần, seed 1729; lấy nhóm kèm toàn bộ peptide,
  estimand peptide-macro (không đổi thành group-macro khi nhóm có kích thước khác).
- So matched original MAE: CI98,75% cho family bốn contrast đã công bố;
  không coi family này hiệu chỉnh toàn bộ lịch sử thử model.
- CI mới/strata/threshold là mô tả 95%; không tạo p-value/threshold G2 mới.
- CI chứa 0: chưa phân giải, không kết luận tương đương hoặc bác bỏ mọi lợi ích.
- P@10 tie: SHA256([1729,peptide_id,cell_id]) giống E5; không dùng nhãn để phá tie.
- Giữ null có reason khi metric không xác định; không thay thiếu bằng 0.
- Không gọi 3 seed hoặc 5 fold là nghiên cứu/cohort độc lập.

## 6. Deliverable và acceptance đợt CPU

1. Config/protocol, runner CPU và dependency versions tái tạo được.
2. Input manifest có hash, lineage, kiểm trước/sau và giới hạn audit.
3. JSON kết quả, CSV subgroup/reliability/similarity/threshold và hình chẩn đoán.
4. Validator kiểm trực tiếp số liệu, edge case meaningful và source invariance.
5. README tiếng Việt: số đo, diễn giải, kết quả âm, limitations và bước tiếp.
6. Protocol tiếp theo cho LoRA transfer/new source; trạng thái **chưa chạy**.

Acceptance là tính đúng và đủ của phân tích, không yêu cầu hypothesis dương.
Gate thất bại phải dừng, không viết kết quả khoa học như đã đạt. Kiểm runtime
không import torch/transformers/cupy, không GPU; ghi wall/CPU/RSS và versions.
Không đổi serving, G2/G3 hoặc report trong đợt này.
