# Nghiên cứu degron-footprint — chỉ mục hiện hành

Đồng bộ ngày **03/11/2026**. Bài toán là hồi quy `ΔPSI = PSI(mutant) − PSI(WT)` cho thay thế amino acid đơn; các benchmark, phạm vi PSI và phép chia dữ liệu khác nhau phải được trình bày riêng. Kết quả development chưa đóng G2/G3 và chưa thay mô hình `m3-ext4.0-platt-v1` trong ứng dụng.

## Luồng đang thực hiện: v3 full-PSI

| Nội dung | Điểm vào và bằng chứng |
| --- | --- |
| Dữ liệu | [DATASET.md](kaggle-roadmap-2026-10-31/DATASET.md), [dataset-build.json](kaggle-roadmap-2026-10-31/dataset-build.json): 235 peptide / 122.412 ô saturation, 224.470 ô scanning sau QC; 221 nhóm protein trong W. [Sổ nguồn gốc](../data/README.md). |
| Thiết kế thực thi | [README v3](kaggle-roadmap-2026-10-31/README.md), [EXECUTION-PROTOCOL.md](kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md). `PROTOCOL.md` giữ thiết kế ban đầu; không thay lựa chọn mà runner đang dùng. |
| Output Kaggle đã nhập | [output-analysis.md](kaggle-roadmap-2026-10-31/output-analysis.md), [output-analysis.json](kaggle-roadmap-2026-10-31/output-analysis.json), [phân tích chi tiết](kaggle-roadmap-2026-10-31/output-analysis-details.md). Snapshot campaign `369cb2fe6a1e31e0` cập nhật `2026-11-01T11:18:07Z`; phân tích tạo ngày 02/11. |
| Campaign Windows local | [local-plan.json](kaggle-roadmap-2026-10-31/local-plan.json), [hướng dẫn chạy/resume](kaggle-roadmap-2026-10-31/local-runner.md), [môi trường CUDA](kaggle-roadmap-2026-10-31/local-cuda.md); snapshot ở mục dưới. |
| Chạy lại trên Kaggle | [RUN.md](kaggle-roadmap-2026-10-31/RUN.md), [ALL-IN-ONE.md](kaggle-roadmap-2026-10-31/ALL-IN-ONE.md), [MULTI-SESSION.md](kaggle-roadmap-2026-10-31/MULTI-SESSION.md). |
| Kiểm chứng hạ tầng | [VALIDATION.md](kaggle-roadmap-2026-10-31/VALIDATION.md), `*-validation.json` và [readiness.json](kaggle-roadmap-2026-10-31/run-local-2026-11-02/readiness.json). Smoke/readiness và benchmark là các bằng chứng khác nhau. |

**[ĐO đã lưu]** Phân tích output Kaggle đã đọc 83 file OOF, gộp thành 47 recipe; kiểm kích thước/SHA của 2.986 artifact hoàn tất. Manifest ghi 35 task hoàn tất và một task đang dở, không phải toàn bộ pipeline đã xong. Các nhánh 00/01/02/03/04/05/06 và một phần 11 có kết quả. Frozen stage11 mới có seed 17; LoRA chưa đủ OOF. Các nguồn số và giới hạn nằm trong [output-analysis.json](kaggle-roadmap-2026-10-31/output-analysis.json).

**[DIỄN GIẢI đã lưu]** Kết quả development hỗ trợ khảo sát train toàn dải PSI và frozen ESM kết hợp CNN; thứ hạng trong snapshot chưa phải lựa chọn sản phẩm. Chưa có output Kaggle stage07 calibration/locked T, stage08 external, stage09 structure hoặc stage10 aggregate cuối trong snapshot đã phân tích. Cần refit/export riêng nếu chọn CNN/LoRA/family để phục vụ.

## Campaign local sau sửa tokenizer — 03/11/2026, 12:38 (UTC+8)

**[ĐO kiểm phần mềm]** ProtT5 đã nạp được SentencePiece sau khi thêm protobuf; Ankh dùng tokenizer JSON gốc và đầu vào tách residue. Hai model đạt alignment đủ 532 phép thay, preflight CUDA, batch 8 và lưu feature FP16 hữu hạn theo [tokenizer-repair-validation.json](kaggle-roadmap-2026-10-31/tokenizer-repair-validation.json). Ankh base dùng encoder FP32 sau khi FP16 không qua kiểm hữu hạn; ProtT5 giữ FP16. Chưa suy ra chất lượng benchmark từ các kiểm tra này.

Successor **`ef138c84579c842e`** được tạo với [plan.json](kaggle-roadmap-2026-10-31/output/local/ef138c84579c842e/plan.json), [state.json](kaggle-roadmap-2026-10-31/output/local/ef138c84579c842e/state.json) và [inheritance.json](kaggle-roadmap-2026-10-31/output/local/ef138c84579c842e/inheritance.json). Tại mốc tạo: **456 complete kế thừa, 178 pending, một checkpoint LoRA paused**, tổng 635 đơn vị. Các trạng thái blocked/skipped của ProtT5/Ankh ở nguồn được reset để chạy probe/extract/120 Ridge fold. Campaign nguồn giữ nguyên để truy vết; artifact complete nằm ở nguồn, checkpoint paused được sao chép và kiểm hash. Kiểm CUDA trên mẫu nhỏ xác nhận tiếp tục LoRA qua successor khớp lượt liên tục, sai lệch tham số tối đa 0.

Dùng các lệnh `.cmd` như trước; [local-runner.md](kaggle-roadmap-2026-10-31/local-runner.md) mô tả phạm vi kế thừa được phép và yêu cầu giữ cả hai thư mục output. Snapshot cũ bên dưới được giữ theo mốc ban đầu, không còn là hàng đợi hiện tại.

## Snapshot lịch sử — 03/11/2026, 10:17 (UTC+8)

**[ĐỌC TRẠNG THÁI]** Campaign `e7097449883a51d8`, theo [plan.json](kaggle-roadmap-2026-10-31/output/local/e7097449883a51d8/plan.json), [queue.json](kaggle-roadmap-2026-10-31/output/local/e7097449883a51d8/queue.json) và [state.json](kaggle-roadmap-2026-10-31/output/local/e7097449883a51d8/state.json) tại thời điểm đọc. Đây là ảnh chụp tiến độ, không phải bảng đánh giá mô hình; tiến trình có thể cập nhật file sau mốc này.

| Trạng thái | Số đơn vị công việc |
| --- | ---: |
| `complete` | 455 |
| `adapter_blocked` | 2 |
| `skipped_resource` do phụ thuộc bị chặn | 122 |
| `running` theo state | 1 |
| Chưa có entry trong state | 55 |
| Tổng DAG | 635 |

455 đơn vị hoàn tất gồm import Kaggle, 9 bước weights, 7 probe, 7 extract, 420 Ridge fold và 11 tune fold. Frozen ESM2-35M đã xong B/D, seed 17, năm fold mỗi arm; LoRA mới xong B/17/fold0, state ghi `tune-lora-B-17-1` đang chạy. Không coi status `running` riêng lẻ là xác nhận worker còn sống; dùng `status-local.cmd` để kiểm trạng thái mới nhất.

ProtT5 bị `adapter_blocked` ở probe với lỗi tokenizer yêu cầu `tiktoken`; Ankh base bị chặn vì tokenizer không trả đúng 28 residue token. Đây là lỗi khả năng thực thi trong runtime này, chưa phải kết quả chất lượng dự đoán. Weights tải xong không đồng nghĩa adapter hoặc phép đánh giá đã đạt.

Các bước `collect-family`, `collect-core`, `calibrate-core`, `locked-transfer-w5` và `report` chưa chạy trong snapshot. Vì vậy chưa có benchmark local tổng hợp, phép so LoRA−frozen đủ seed/fold hoặc đánh giá locked T của campaign này. External/structure vẫn thiếu đầu vào. Campaign cũ `e18d80b06ac90585` đã bị thay thế vì lỗi timer Windows; lý do được giữ trong [superseded.json](kaggle-roadmap-2026-10-31/output/local/e18d80b06ac90585/superseded.json).

Từ gốc repo dùng `run-local.cmd` để tiếp tục, `status-local.cmd` để xem và `pause-local.cmd` để yêu cầu dừng an toàn. Đọc hướng dẫn trước khi đổi dependency/code vì fingerprint thay đổi sẽ tạo campaign mới. Git chỉ giữ metadata được cho phép; checkpoint, feature, OOF và output Kaggle phải được lưu riêng để tái lập/resume.

## Bằng chứng và kế hoạch lịch sử

| Hồ sơ | Vai trò hiện tại |
| --- | --- |
| [G2 saturation](g2-saturation-2026-10-18/README.md), [extension](g2-extension-2026-10-18/README.md) | Benchmark gốc và mở rộng ngưỡng; khác population/split của W full-PSI v3. |
| [Next steps](next-steps-plan-2026-10-22/README.md), [next phase](next-phase-plan-2026-10-22/README.md) | Kế hoạch và kết quả tháng 10; không phải hàng đợi thực thi v3 hiện tại. |
| [R0](r0-reproduce-notebook-2026-10-22/README.md), [R1](r1-degformer-clean-2026-10-22/README.md), [R2](r2-esm-features-2026-10-22/README.md), [R3](r3-domain-gate-2026-10-22/README.md) | Tái lập, đối chứng Degformer, frozen ESM và cổng miền; kết quả/giới hạn giữ theo protocol gốc. |
| [R6](r6-ladder-scan-2026-10-23/README.md), [scan–sat merge](scan-sat-merge-2026-10-23/README.md) | Ngữ cảnh/scanning/ESM/CNN; phép xác nhận P của R6 chưa đạt, Ridge ±5 được nhận ở mức họ. |
| [Model selection 24/10](model-selection-pipeline-2026-10-24/README.md) | Lập luận và chỉ mục bằng chứng R2/R6; không phải kết quả lựa chọn mới của v3. |
| [Notebook-kit 22/10](notebook-kit-2026-10-22/RUN.md) | Dựng gói v1/v2 để tái lập các thí nghiệm lịch sử. |

Các README lịch sử giữ mốc đo và protocol gốc. Khi cập nhật trạng thái, dẫn tới bằng chứng mới thay vì sửa lại kết luận lịch sử hay gộp metric giữa các thiết kế.
