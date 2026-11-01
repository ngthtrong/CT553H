# Protocol thực thi v3.1 — 01/11/2026

Đây là protocol triển khai sau khi đã biết dữ liệu và kết quả lịch sử, không phải
preregistration độc lập. `PROTOCOL.md` giữ thiết kế ban đầu. File này mô tả chính
xác các lựa chọn dùng trong runner; hash được nhúng trong notebook và run manifest.
Không có kết quả official mới được công bố cùng bộ notebook này.

## Dữ liệu và phạm vi suy luận

- Nhãn: hồi quy ΔPSI của đột biến đơn trong reporter peptide 28 AA của Zhang 2023.
  Saturation giữ QC kỹ thuật gốc, bỏ điều kiện lọc PSI: 235 peptide, 122.412 ô.
- PSI(WT), read count, replicate disagreement, stratum, group/fold là metadata.
  PSI/read/fold không được đưa vào feature. Disagreement chỉ dùng để tính trọng
  số train trong phép so riêng của stage06.
- A/B/C: train với PSI(WT)≤3/4/5; D: full; E: full cân bằng stratum rồi peptide.
  Inner validation dùng chung toàn dải cho mọi arm; test không bị lọc theo arm.
  Vì vậy A/B có dùng nhãn PSI cao để chọn hyperparameter.
- Giới hạn vật lý: 1−PSI(WT) ≤ ΔPSI ≤ 6−PSI(WT). Không ép clipping dự đoán bằng
  PSI(WT). AUROC thiếu hai lớp ghi null; peptide PSI>5 vẫn có ích cho hồi quy/âm.

## Splits và fit

- View L tái lập riêng số cũ, dùng NPZ/fold lịch sử, raw Ridge, seeds 17/29/43,
  α=1/10/100/1000. Dung sai macro AUROC 1e-4 so .808185975 và .820822359.
- View W: 5 outer folds dùng 221 nhóm saturation, được hợp từ cov80 toàn proteome,
  hits MMseqs2 identity≥.30, bidirectional cov≥.50, alnlen≥50 và exact-sequence
  unions. Đây là kiểm soát homology bằng heuristic, không phải chứng minh độc lập.
  Fold được cân bằng theo stratum/số peptide; nhãn ΔPSI không dùng để chia.
- Inner validation khoảng 20% nhóm saturation còn lại, common assignments cho
  seeds 17/29/43. Scaler/PCA chỉ fit inner-train, sau đó refit outer-train hợp lệ.
  Epoch mạng chọn bằng inner MSE rồi khởi tạo lại, fit outer-train đủ epoch đã chọn.
- scan_dev và scan_T được tách theo nhóm trước fitting, không giao với saturation.
  Scan cùng nhóm saturation giữ trong `sat_overlap`, không dùng làm train transfer
  trong implementation này. T đã từng được khảo sát ở mức nguồn trong lịch sử;
  gọi là held-source trong protocol này, không gọi external độc lập hoàn toàn.
- Ridge chọn α∈{.1,1,10,100,1000} bằng inner MSE. Frozen pLM: PCA64 chỉ trên block
  Δsite + meanΔ, context W5 được giữ riêng. PCA randomized, tối đa 20.000 hàng
  train bằng seed cố định để giới hạn RAM; scaler vẫn fit toàn train hợp lệ.
- Curve của stage01 dùng 25/50/75/100% nhóm train theo thứ tự hash(seed, group),
  subsets lồng nhau trong từng tập fit; common validation/test không đổi. Chỉ W5-D
  được triển khai curve; curve mạng là việc bổ sung sau khi khóa ứng viên.

## Các model được huấn luyện mới

1. Stage01: Ridge mới cho A–E và pair/composition/unordered/ordered controls.
2. Stage04: Ridge/PCA mới trên từng family/scale, có/không context. Chọn recipe
   trong từng outer fold/seed bằng inner MSE; nested OOF đánh giá quy trình chọn.
   Không tuyên bố một fixed family thắng trên dữ liệu độc lập từ bảng development.
3. Stage05: pointwise k1, CNN k5, mCNN k3/5/7, one-hot và ESM35 crop ±7.
   Kênh center và input pair+composition giống nhau; projection pLM32, filters96
   cho pointwise/CNN và 32 mỗi nhánh mCNN; dropout .3; AdamW lr.001,
   weight_decay .01, batch256, tối đa40 epoch, patience6. Số tham số thực được lưu;
   k1/k5 là phép so khả năng trộn vị trí, không khẳng định bằng tuyệt đối số tham số.
4. Stage06: Ridge sat-only/quality/source-aware, cùng intersection rep1/rep2.
   Quality scale median train, cap [.1,1]; scanning source weight .1. CNN được
   pretrain5 epoch cố định trên scan_dev rep1 hoặc mean12, rồi fine-tune saturation;
   CNN scratch cùng architecture/seed là đối chứng. scan_T không được dùng pretrain.
5. Stage11: học regression head mới với frozen pLM và **LoRA attention Q/V + head**.
   Default ESM2-35M, arms B/D; rank8, alpha16, head64/ReLU/dropout.2;
   AdamW lr1e-4, weight_decay.01, batch8, clip1, tối đa20 epoch, patience4.
   Backbone dùng eval dropout policy ở cả hai nhánh nhưng gradient LoRA vẫn bật.
   Head initialization và splits giống nhau. Checkpoint lưu adapter/head mới,
   optimizer, base revision; runner xác nhận LoRA thực sự thay đổi tham số.
   `finetune_modes=['frozen','full']` hỗ trợ full tuning ESM2-8M/35M.
   Chưa khẳng định fine-tuning model lớn khả thi; cần preflight riêng trước mở rộng.

Đây là fine-tuning model pretrained cho nhãn mới, không pretrain pLM từ đầu.
Không cần kiến trúc mới để đóng góp benchmark/phương pháp/đánh giá/phần mềm.

## Weights, feature và tài nguyên

- Registry gồm 20 checkpoint của 7 họ, đã pin revision theo metadata chính thức.
  Trạng thái tải và SHA từng file độc lập với việc adapter/GPU đã được kiểm.
  Không chạy remote Python của model repo; Transformers builtin/T5EncoderModel.
- Stage02 probe tokenizer, 28 residue tokens, finite/repeated forward, throughput,
  peak VRAM. Không tự thay quantization hoặc sharding sau OOM. Stage03 chỉ chạy
  model đã qua preflight trên runtime tương ứng. 3B/6B/15B có thể resource-blocked;
  GPU nhiều card không tự cộng bộ nhớ. Implementation hiện chưa có dispatch/offload.
- Feature chính là Δhidden(site) + meanΔ; crop chỉ trích cho head shortlist.
  Shard giữ row IDs/progress/prefix hash; merge kiểm disjoint, revision/dtype/data.
  Extraction cho T yêu cầu selection lock. Không gửi sequence qua hosted API.
- Checkpoint/data/code bundle được tách. Weights gốc không được nhân bản trong
  mỗi result ZIP. Bản package chỉ chứa file đã được kiểm hash; partial không được load.

## Đánh giá và cổng

- Chính: peptide-macro MAE toàn W và từng stratum. Báo thêm RMSE, Spearman,
  AUROC/AP dương Δ≥1 và âm Δ≤−1, precision/enrichment top5/10/20%.
  AUROC/AP yêu cầu mỗi lớp≥3; số peptide đủ điều kiện được ghi riêng.
- Report mỗi seed và ensemble prediction khi có; không tráo metric trung bình
  seed với metric của ensemble. CI paired bootstrap5.000 lần theo nhóm protein,
  chênh MAE D−B/E−B, CI95% và Bonferroni cho hai phép so chính. Dấu âm tốt hơn.
  Ngưỡng thực dụng trước official: giảm MAE tối thiểu .02 PSI; miền≤3 không giảm
  AUROC dương quá .01. Đây là quy tắc diễn giải, runner không tự đóng scientific gate.
- Stage07 khóa recipe trước khi đọc T. Calibrator3 lớp chỉ fit inner-validation
  predictions của chính fold, không dùng một global OOF split gây rò nhãn chéo.
  Final calibrator fit ensemble OOF development. W5 có final refit/export và T-score;
  family/CNN/LoRA hiện có calibration CV nhưng chưa có final promotion tự động.
- Stage08 không có nguồn mới thì ghi source_pending; nguồn có endpoint/độ dài khác
  chỉ được audit, không padding hay đổi thành ΔPSI. Nhập nguồn mới vào train cần
  protocol nguồn và homology/assay audit riêng. Không tải nguồn mới trong builder lõi.
- Stage09 không có cấu trúc/mapping thật thì structure_pending. Có bảng reviewed,
  `run_saprot=True` chạy cùng cohort W5/SaProt true/masked 3Di. Giữ WT3Di cho mutant
  là giả định tĩnh, không khẳng định cấu trúc mutant được đo. Mapping/coverage phải báo.
- Stage10 chỉ tổng hợp đúng data identity/mode; official OOF thiếu bị từ chối.
  Dữ liệu cấu trúc chỉ phủ cohort con được báo riêng, không trộn với bảng full W.

## Smoke và kết quả official

SMOKE=True là default an toàn: seed17, cohort nhỏ, epoch1; stage05/04 có fixture
ngẫu nhiên ghi rõ tên `synthetic_smoke`. Stage11 dùng **weights ESM2-8M thật và
nhãn ΔPSI thật**, kiểm update/lưu model. Mọi output smoke có mode riêng và không
được dùng làm bằng chứng hiệu năng. Stage08/09 pending là trạng thái đúng khi thiếu
đầu vào, không phải thí nghiệm đã chạy. Chạy official trên Kaggle, giữ cả OOM/kết quả âm.

Software local smoke không thay cho kiểm CUDA/GPU, full folds hoặc external validity.
G2/G3 không được tự đóng khi chỉ tạo notebook, trích feature hoặc chạy smoke.
