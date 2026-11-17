# Protocol refit/transfer v1 — 16/11/2026

Khoá trước prediction LoRA/frozen refit mới trên T. Trọng đã yêu cầu triển khai
runner và chạy GPU trong phiên ngày 16/11. T từng được xem qua W5 và diagnostic
08/11; đây là đánh giá chuyển miền hậu kiểm trên held-source đã khảo sát, không
phải independent external validation. Giữ `development_not_gate_closure`.

## 1. Nguồn và phạm vi

- Nguồn development: `ef138c84579c842e`, có tham chiếu artifact hoàn tất từ
  `e7097449883a51d8`. Giữ nguyên mọi plan/state/checkpoint nguồn.
- `source-lock.json` pin plan/state nguồn, 30 cặp fit/OOF D, base weights,
  baseline W5, data manifest và cohort IDs; path tương đối, bytes/SHA-256.
- Campaign mới dùng `refit_transfer_v1`, fingerprint riêng bao gồm byte code,
  config/protocol/source-lock/runtime. Không kế thừa checkpoint training cũ.
- 15 core job và 5 completion job trong cùng runner. Koren thiếu nguồn/adapter
  được ghi `source_pending`; không coi toàn nhánh hoàn thành. D-4 vẫn pending.

## 2. Fit policy cố định

Base ESM2-35M `facebook/esm2_t12_35M_UR50D`, revision
`6fbf070e65b0b7291e7bbcd451118c216cff79d8`. Giữ tokenizer/head/feature từ v3:
delta-site và delta-mean embedding + pair/composition 60 chiều. WT 28 aa,
coordinate 1-based. PSI/reads/label/group/fold không là input model.

Frozen-D và LoRA-D cùng seed 17/29/43, khởi tạo mới từ base và head đúng seed.
LoRA rank 8, alpha 16, attention query/value; FP32, batch 8, AdamW lr 1e-4,
weight decay .01, gradient clip 1. Toàn W 122.412 cell/235 peptide/221 nhóm;
không scan_dev/T, không early stopping. Validation frame rỗng. Median epoch
riêng từng seed từ 5 fold development: LoRA 2/2/2, frozen 1/2/2.

Không train tiếp outer model, không ghép 15 outer models làm final ensemble.
Không đổi precision/batch/LR/threshold theo kết quả hay tự fallback CPU.
Checkpoint khoảng 120 s, model/optimizer/RNG/cursor và 2 thế hệ; resume chỉ
khi campaign identity khớp. Runtime/code/config thay đổi phải tạo campaign mới.

## 3. Calibration và prediction

Calibrator logistic multinomial C=1, max_iter=1000, event labels minus <=-1,
neutral (-1,1), plus >=1. Fit từ **raw ensemble OOF W của đúng recipe**:
trung bình raw prediction ba seed trước fit. Không dùng final in-sample W hoặc
T để fit calibrator/correction. Final ensemble cũng mean raw ba seed rồi áp
calibrator một lần. Lưu score shift OOF W/final W/T; final W chỉ diagnostic.

Score primary T rep1 đúng 39.234 cell/1.410 peptide/730 nhóm; QC là rep1 finite
và partition scan_T đã pin, không lọc theo prediction. Assert ID/hash/finite và
W/T group disjoint. Frame inference chỉ chứa sequence, substitution, coordinate
và identifiers; nhãn T được tách và chỉ ghép trong aggregate.

## 4. Endpoint và thống kê

Primary endpoint: mean MAE trên peptide (peptide-macro), T rep1 toàn cohort.
Hai contrast LoRA-D minus frozen-D và LoRA-D minus W5-D; delta âm tốt hơn.
Paired bootstrap 5.000 lần theo group, RNG seed 1729; cùng resample cho hai
model, giữ peptide weights trong group. CI 97,5% hai phía mỗi contrast của
family 2 bằng Bonferroni, percentile 1,25%/98,75%. CI cắt 0 là chưa phân giải,
không đồng nghĩa tương đương. Không có ngưỡng lợi ích thực dụng do tác giả chốt;
không dùng kết quả để tự promotion hoặc đóng gate.

Giữ baseline zero, W5-D đã pin và constant = mean dpsi_mean toàn W. Không chọn
lại constant/recipe bằng T. Báo từng seed và ensemble; seed không là replicate
sinh học. Bootstrap conditional trên predictions, không bao trùm training hay
model-selection uncertainty.

Secondary: peptide-macro RMSE, Spearman, AUROC/AP hai chiều ±1 (mỗi lớp >=3
thành viên/peptide), P@min(10,N), prevalence/no-hit, Brier ba lớp, ECE 10 bin hai
chiều, strata theo scanning WT PSI. Ranking tie dùng hash seed 1729, peptide và
cell ID, như diagnostic 08/11. Metric không đủ lớp ghi null kèm lý do/count,
không điền 0. Replicate intersection chấm rep1/rep2/mean12 trên cùng giao tập;
rep1 toàn cohort vẫn primary. Secondary/strata là exploratory.

Directed pair và similarity/mechanism chưa được triển khai đầy đủ phải ghi
missing coverage, không gọi diagnostic mô tả là giải thích cơ chế hoặc toàn bộ
nhánh đã xong. Giữ mọi kết quả âm, kể cả tệ hơn zero/W5 ở PSI cao.

## 5. Completion và bàn giao

Model card ghi đủ 3 model ID/seed/epoch/adapter-head hash/base revision,
calibrator lineage và AA/coordinate contract. Parity: reload checkpoint và so
resumable predict với finetune.infer trên cùng 32 W cells, atol/rtol=1e-5.
Đây là kiểm cùng runtime; máy chính phải kiểm lại sau copy, không giả là đã có
triển khai backend độc lập. Không đổi model phục vụ từ lượt research này.

Koren S4 thiếu nguồn XLSX/hash và adapter chiều dài 12/23 aa được review: ghi
pending, không pad giả hay scale 3-bin thành 6-bin, không đóng source_pending.
Error diagnostics chỉ mô tả distribution/residual/score shift/replicate;
similarity/causal mechanism có thể chưa phân giải. Xuất 3 hình đầu tiên từ JSON,
không sửa report/app/slide trên máy này. D-4 chỉ tác giả/GVHD quyết định.

Checkpoint/prediction/calibrator/weights và logs ở output local ignored; chỉ
code/protocol/metadata/metrics/figures chọn lọc lên Git. Không tự stage/commit/
push. Manifest copy thủ công có relative path/bytes/SHA; không copy .git/.venv.
