# Kiểm chứng độc lập bản lưu local — 06/11/2026

**[ĐO]** Kiểm tra trực tiếp dữ liệu, state, manifest và Parquet OOF trong checkout Linux; không huấn luyện, không nạp model/checkpoint vào Torch, không sửa state hoặc dữ liệu. Bằng chứng là **bản lưu campaign Windows có thể truy cập**, không phải quan sát trực tiếp một tiến trình Windows đang chạy. Chỉ mục kết quả máy đọc được: [local-audit.json](local-audit.json); mọi nguồn trực tiếp đã đọc được ghi size/SHA-256 trong [source-inventory.json](source-inventory.json).

## Phạm vi, phiên và độ toàn vẹn

- HEAD khi kiểm: `64c3c33`; hash đầy đủ được ghi tự động trong JSON. Git commit không thay thế identity riêng của campaign.
- Phiên lưu mới nhất: campaign `ef138c84579c842e`, session `20261106-075837`, `idle`, `executed=0` ở phiên session này. Con số 0 không có nghĩa toàn campaign chưa thực thi.
- State mới nhất có **633 complete, 1 source_pending, 1 structure_pending**. Hai pending ghi lý do `Reviewed input not supplied`; không có job `running` trong state này.
- Job có `started_unix` gần nhất trong successor là **06/11/2026 03:50:23 +08:00**. Mtime của bản sao khoảng 10:19 không được dùng như thời gian chạy. Snapshot nguồn `e709...` kết thúc ở 456 complete, 2 adapter_blocked, 122 skipped_resource, 1 paused; successor kế thừa đúng 456 job, tính một lần.
- Kiểm lại **4.278 artifact local** và **2.986 artifact Kaggle** hoàn tất: size và SHA-256 khớp state/manifest; không sửa bất kỳ manifest nào để đạt khớp.
- Bundle đang có tên thư mục Linux `v3-fullpsi`, nhưng hash `DATA_MANIFEST.json` đúng identity `b0376e05d690d991c95143d6122b5418e457318394da032928d0d1e53f914738`. Cả **32 file trong manifest** khớp size/SHA; không suy từ tên thư mục rằng đây là dataset khác.
- Kiểm 15 bảng role theo seed/fold: mỗi group có một role trong outer fold; test groups khớp W; role có cả `held_source`. Không chạy lại MMseqs2, vì vậy đây là xác minh split lưu sẵn, không chứng minh heuristic homology đã bắt hết mọi tương đồng sinh học.

### Khác byte do newline đã giải thích được

**[ĐO]** Trong 76 nguồn đã pin bởi phân tích local trước, **75 nguồn khớp byte trực tiếp**, một nguồn cần đối chiếu newline:

| Nguồn | Bản đang có | Bản pin ở Windows | Kiểm giải thích |
|---|---|---|---|
| `output-analysis.json` | 570.381 byte, SHA `ecd7f61b...` | 583.016 byte, SHA `7285f50f...` | Chuyển 12.635 LF thành CRLF trong bộ nhớ tái tạo đúng size và SHA pin |

Không diễn giải điều này thành artifact hỏng hoặc nội dung metric đã thay đổi. Ngược lại, không gọi cả 76 nguồn là khớp byte trực tiếp trên Linux. Đã giữ nguyên nguồn gốc và hash gốc.

**[ĐO]** [source-inventory.py](source-inventory.py) còn tái tạo chính xác hash code tổng hợp `b401f465...` trong plan bằng cùng thứ tự nối file của runner, xét hai cách LF/CRLF cho mỗi file. Tìm thấy đúng một cấu hình newline khớp: các module gốc dùng CRLF, nhóm `local_*.py` và `local-runner.py` dùng LF. Protocol và registry cũng tái tạo đúng hash pin khi dùng CRLF. [source-inventory.code.json](source-inventory.code.json) giữ toàn bộ ánh xạ và hash. Kiểm này xác nhận cùng văn bản nguồn; không chứng nhận môi trường Linux có thể resume GPU Windows.

## Kết quả OOF đã tái tính

**[ĐO]** Tất cả **41 recipe local** đủ seed 17/29/43, mỗi seed 122.412 cell/235 peptide/221 group/5 fold. Không trùng `(seed,cell_id)`; dự đoán hữu hạn; nhãn, group, stratum và outer-fold khớp bundle từng cell. MAE ensemble và từng seed khớp số đã lưu trong dung sai `1e-10`. Bốn core recipe còn được tái tính RMSE, Spearman, AUROC và AP bằng script kiểm độc lập với helper metric nghiên cứu. Nested selector có đủ 15 lựa chọn, tất cả khớp argmin inner-validation MSE từ 540 `fit.json`.

MAE là trung bình MAE từng peptide, **không phải cell-micro**. AUROC/AP dương dùng nhãn đo ΔPSI≥1 và cần ít nhất ba event, ba non-event/peptide; 184 peptide đủ điều kiện dương, 110 đủ điều kiện âm. Ensemble là trung bình dự đoán ba seed trước khi chấm metric.

| Recipe local | MAE W | AUROC+ | AP+ | AUROC− |
|---|---:|---:|---:|---:|
| frozen-B | 0.403385 | 0.826268 | 0.455411 | 0.754078 |
| frozen-D | 0.390382 | 0.824625 | 0.454438 | 0.766693 |
| LoRA-B | 0.363669 | 0.855047 | 0.551682 | 0.792134 |
| LoRA-D | 0.364996 | 0.853556 | 0.547416 | 0.802777 |

**[DIỄN GIẢI]** Matched frozen–LoRA có cùng runtime local và head, nên đây là đối chứng phù hợp hơn việc quy toàn bộ chênh lệch Kaggle CNN–local LoRA cho riêng LoRA. CI cluster-bootstrap trước đây còn được giữ nguyên ở phân tích nguồn, đã kiểm hash; audit này không tự tạo CI mới cho subgroup residual.

### Kiến trúc thực sự và cấu hình

**[ĐO từ code]** `MutationRegressor` dùng delta embedding WT→mutant tại residue thay thế, mean delta trên peptide và 60 đặc trưng WT/mutant/composition; head là Linear(2d+60,64), ReLU, Dropout(0,2), Linear(64,1). Đây là **MLP matched head**, khác các CNN/mCNN trên crop embedding ở Kaggle.

LoRA rank 8, alpha 16 cập nhật attention query/value; backbone còn lại frozen. Encoder cùng chính sách eval/dropout; head được reset seed để có cùng khởi tạo. Local: batch 8, tối đa 20 epoch, AdamW learning rate `1e-4`, weight decay `0.01`, gradient clipping 1, patience 4. Inner-validation MSE chọn epoch; sau đó khôi phục khởi tạo và refit train+validation đúng epoch đã chọn trước khi dự đoán outer-test. MSE chọn epoch là cell-micro, khác metric báo cáo MAE peptide-macro; đây là lựa chọn mục tiêu có thể khảo sát tiếp, chưa phải lỗi leakage.

B chỉ giới hạn dữ liệu **train/refit PSI(WT)≤4**, D dùng toàn dải; validation/test chung toàn dải. PSI(WT) dùng để chia miền/arm; không được đưa trực tiếp vào head như đặc trưng. WT và mutant sequence là input của encoder; nhãn ΔPSI là target. Code có tùy chọn `full`, nhưng **queue campaign chỉ frozen và LoRA**: chưa có kết quả full fine-tuning trong campaign này.

**[ĐO có giới hạn]** 60 fit metadata tồn tại, 30 LoRA khai báo tensor `lora_` đã thay đổi; không nạp tensor checkpoint để kiểm lại phép so tensor trong lượt này. Vì vậy phải phân biệt xác minh metadata/hash với thực thi lại phép học.

## Residual, fold và peptide khó

Các bảng dưới đây là **[ĐO hậu kiểm mô tả]**, không phải giả thuyết preregistered hay kiểm định trên tập độc lập mới. Không loại case có kết quả bất lợi. JSON có đầy đủ 235 hàng cho từng core recipe, 380 loại phép thay WT→mutant khi đủ dữ liệu, nhóm theo amino acid đích, fold, PSI và effect class; mỗi subgroup ghi denominator.

| Matched arm | Peptide MAE giảm/tăng | Group MAE giảm/tăng | Khoảng ΔMAE khi bỏ lần lượt một group |
|---|---:|---:|---:|
| LoRA-B − frozen-B | 184 / 51 | 176 / 45 | [−0.040371; −0.038878] |
| LoRA-D − frozen-D | 164 / 71 | 155 / 66 | [−0.026108; −0.024663] |

Group MAE ở phép đếm là trung bình MAE các peptide thuộc group. Khoảng leave-one-group-out trên đây là min/max từ việc bỏ từng group, **không phải confidence interval**. Lợi ích trung bình không đổi dấu khi bỏ bất kỳ một group nào; quan sát này giảm lo ngại kết quả bị một group duy nhất chi phối, nhưng không loại trừ overfitting, confounding hay sai sót homology chưa phát hiện.

| Fold | LoRA-B MAE | LoRA-D MAE |
|---|---:|---:|
| 0 | 0.386229 | 0.388193 |
| 1 | 0.360922 | 0.366613 |
| 2 | 0.379260 | 0.382512 |
| 3 | 0.353532 | 0.344535 |
| 4 | 0.338400 | 0.343128 |

Không xem năm fold như năm thí nghiệm độc lập; fold khác thành phần peptide/PSI và chia sẻ nhiều dữ liệu train.

### Hiệu ứng lớn và dấu sai số

MAE dưới đây là macro trên peptide **sau khi chỉ lấy cell thuộc subgroup**, do đó không trộn với MAE toàn W. Denominator dương/âm ở đây không áp điều kiện đủ ba event/non-event như AUROC.

| Nhãn đo | Cell / peptide / group | Zero MAE | LoRA-B MAE | LoRA-D MAE |
|---|---:|---:|---:|---:|
| ΔPSI≤−1 | 1.577 / 151 / 144 | 1.232016 | 1.038523 | 0.950972 |
| −1<ΔPSI<1 | 108.782 / 235 / 221 | 0.303095 | 0.287942 | 0.284277 |
| ΔPSI≥1 | 12.053 / 198 / 190 | 1.415517 | 0.799666 | 0.847877 |
| \|ΔPSI\|≥1 | 13.630 / 232 / 218 | 1.412737 | 0.896984 | 0.908419 |

**[DIỄN GIẢI]** LoRA cải thiện so với zero cả trên event lớn, nhưng sai số tuyệt đối vẫn lớn hơn rõ rệt so với cell trung tính. Với `prediction−observed`, signed error cell-micro của LoRA-B là +1.044940 ở event âm và −0.950420 ở event dương; LoRA-D tương ứng +0.937995 và −1.031367. Đây là dấu hiệu dự đoán co về vùng trung tâm; chưa có phân tích nhân quả để quy hiện tượng cho riêng loss, noise, mất cân bằng hay kiến trúc.

**[Case bất lợi giữ nguyên]** `Q96LX7_CCDC17_9` (524 cell, fold 2, PSI≤3) có MAE frozen-B 0.848604, LoRA-B **0.903467**; frozen-D 0.878782, LoRA-D **0.933562**. `Q16665_HIF1A_25` là một peptide khó khác (529 cell, fold 0); LoRA-B/D MAE 0.819259/0.907209. Tên protein giúp truy tìm trường hợp để kiểm noise/sequence, không chứng minh cơ chế E3 hay tính bệnh học của các mutation.

## Calibration và chuyển miền

**[ĐO]** Tái tính Brier ba lớp từ calibrated OOF và kiểm xác suất hữu hạn, tổng bằng 1: frozen-B/D **0.178879/0.179495**, LoRA-B/D **0.163071/0.165899**. Đây là cell-micro Brier ba lớp; không so trực tiếp với Brier nhị phân của P6 lịch sử. Saved ECE+ của LoRA cao hơn frozen, nên Brier giảm không chứng minh mọi mặt calibration đều tốt hơn.

**[ĐO]** Tái chấm trực tiếp `held-scanning.parquet`: 39.234 cell/1.410 peptide/730 group, chỉ mutant R/A/S, nhãn đúng rep1; group không giao W hay scan_dev. W5-D MAE **0.399147**, zero **0.402403**, AUROC+ **0.840546** (338 peptide đủ điều kiện), AUROC− **0.517600** (85 peptide). CI95 ghép cặp đã lưu của ΔMAE W5-D−zero là [−0.009249;+0.002760], cắt 0. Chưa đủ bằng chứng W5-D giảm MAE trên T so với zero.

T vẫn là scanning cùng nguồn/phòng thí nghiệm, đã từng khảo sát ở mức nguồn, khác saturation 19 mutant/residue. Không gọi là external validation độc lập; **LoRA chưa được chấm trên T**. Không lấy kết quả W5-D để suy ra transfer của LoRA.

## Các giới hạn chưa được giải quyết

| Nội dung | Trạng thái đúng | Ảnh hưởng và bước tiếp |
|---|---|---|
| Trạng thái Windows sau snapshot lưu | Không thể truy cập trực tiếp | Chỉ kết luận từ session/state đã lưu; cần snapshot/log mới nếu có lần chạy khác |
| External source/cấu trúc thật | Chưa được thực hiện trong campaign; explicit pending | Chưa chốt generalization ngoài nguồn; cần dữ liệu có provenance, mapping và protocol |
| LoRA trên miền chuyển tiếp | Chưa có kết quả trong campaign | Định nghĩa recipe và protocol đánh giá tiếp trước khi xem nhãn mới; T đã xem không còn hoàn toàn untouched |
| Final refit/export và provenance calibrator | Chưa hoàn thành | Card calibration có `model_ids=[]`; cần artifact kiến trúc đúng, tokenizer/revision/precision và inference độc lập |
| Overfit theo loss/noise | Không đầy đủ | OOF/leave-one-group-out không đủ; cần learning curves train/validation chuẩn hóa, repeat uncertainty và kiểm source grouping |
| Bản analyzer cũ chạy nguyên trạng trên Linux | Không tương thích đường dẫn | Hardcode tên dataset và Windows artifact path; dùng audit chỉ đọc này để map bản sao có hash đúng, không đổi manifest hay ép resume |

Không đóng G2/G3, không tuyên bố kiến trúc mới tối ưu và không thay serving model từ audit này.

## Tái tạo

Từ gốc repository, trong môi trường phân tích có NumPy/Pandas/SciPy/scikit-learn/PyArrow:

```bash
.venv/bin/python -I topics/degron-footprint/research/progress-review-2026-11-06/local-audit.py
python3 -I topics/degron-footprint/research/progress-review-2026-11-06/source-inventory.py
```

Hai script ghi kết quả dẫn xuất bên cạnh chính nó. Script thứ nhất cần các artifact local/Kaggle và bundle đã đồng bộ; clone Git đơn thuần chưa đủ. Không cài hoặc thay Torch, không cần GPU.
