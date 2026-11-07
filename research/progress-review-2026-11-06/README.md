# Rà soát và cập nhật báo cáo tiến độ Degron — 06/11/2026

## Sản phẩm chính

Đã cập nhật **báo cáo hiện có**, giữ tiếng Anh và Tóm tắt tiếng Việt theo quy ước repository. Mốc được trình bày là **báo cáo tiến độ**, không phải xác nhận hoàn tất luận văn hay nghiệm thu nghiên cứu/phần mềm.

- [Báo cáo và hướng dẫn build](../../report/README.md).
- [PDF một mặt](../../report/build/content/content.pdf) · [PDF hai mặt](../../report/build/content-twoside/content.pdf).
- [Lịch sử thí nghiệm](experiment-history.md), [audit dữ liệu/phương pháp](data-method-audit.md), [so sánh kết quả theo protocol](result-comparison.md).
- [Audit local độc lập](local-audit.md), [JSON](local-audit.json), [script chỉ đọc](local-audit.py), [nguồn đã đọc và hash](source-inventory.json).
- [Kiểm chứng tài liệu khoa học](literature-audit.md).
- [Kiểm kê bằng chứng thiếu](missing-evidence.md), [nhật ký sửa báo cáo](report-changes.md), [kiểm chứng báo cáo/PDF](../../report/progress-validation-2026-11-06.md).

## Trạng thái repository và phạm vi truy cập

[ĐO] Bắt đầu từ working tree sạch, nhánh `main`, commit `64c3c337a3823e2575720ad89156d78e06cf8921` (06/11/2026 11:05:07 +08). Lệnh chỉ đọc `git ls-remote --heads origin` trả về:

| Branch trên remote tại lúc kiểm | Commit |
|---|---|
| `main` | `64c3c337a3823e2575720ad89156d78e06cf8921` |
| `report` | `0c75af1ae28aa6a68a88464e3ca05be5c456e541` |

Các local ref `backup-before-clean`, `clean` và `report` cũng có mặt. Một remote-tracking ref trong checkout không tự chứng minh branch đó còn tồn tại trên GitHub; lịch sử cũ được dùng để truy quyết định, không thay bằng chứng artifact mới. Không checkout nhánh, reset, commit hay push trong lượt này.

[ĐO] Phân tích trực tiếp bản dữ liệu và output local đã đồng bộ trong checkout Linux, gồm Parquet OOF; **không quan sát trực tiếp tiến trình Windows đang chạy**. “Mới nhất” ở đây là snapshot mới nhất tìm được và kiểm chứng trong các tài nguyên đã truy cập. Session/plan/campaign identity được ghi trong JSON audit. Không tự khởi chạy/resume training để cập nhật tài liệu.

## Cách đọc bằng chứng

- **Đã xác minh:** tái tính được từ dự đoán/dữ liệu hoặc xác nhận trực tiếp từ mã/artifact; lý thuyết dựa trên nguồn gốc đã kiểm.
- **Suy luận có cơ sở:** giải thích hợp lý từ kết quả, chưa có thiết kế cô lập nguyên nhân.
- **Giả thuyết/đề xuất:** cần thí nghiệm mới; không có metric được điền thay thế.

Các số cũ được giữ trong nhóm protocol riêng. Benchmark ban đầu 91 peptide, full-PSI W 235 peptide, và transfer T 1.410 peptide không được xếp thành cùng một leaderboard. Scanning mutation-label pre-training và Voutsinos tile-label pre-training là hai can thiệp khác nhau.

## Kết luận trọng tâm trong phạm vi bằng chứng

[ĐO] Local snapshot có 633 job complete và hai job chờ đầu vào. Matched ESM2-35M LoRA đạt MAE 0,363669 (B) và 0,364996 (D), cải thiện so với frozen cùng runtime/arm. Các kết quả này thuộc ensemble ba seed và development W; không gán cho một checkpoint đơn hay cho protein tự nhiên.

[DIỄN GIẢI] Chưa có một kiến trúc tối ưu chung: B/D đánh đổi theo WT PSI, mCNN không có lợi thế chắc chắn so với single CNN trong so sánh đã nêu, kích thước pLM không tăng hiệu năng đơn điệu. LoRA có chi phí attempt đã ghi cao hơn và chưa được đánh giá trên T. Không đổi serving model từ leaderboard.

[ĐO] W5-D trên T có MAE 0,399147 so với 0,402403 của dự đoán 0; CI95 cho chênh lệch bao phủ 0. AUROC+ tốt không thay bằng chứng hiệu ứng hồi quy hay xác suất được hiệu chuẩn tốt. T cùng phòng thí nghiệm, R/A/S, rep1, nguồn đã được thăm dò trước; chưa phải kiểm định ngoài độc lập.

## Tái tạo

Từ gốc repository, dùng môi trường phân tích Linux hiện có (không cài đè môi trường Windows/CUDA):

```bash
.venv/bin/python -I research/progress-review-2026-11-06/local-audit.py
.venv/bin/python report/assets/ch4/build_progress_assets.py
make -C report all
make -C report check
.venv/bin/python report/scripts/validate_progress_report.py
git diff --check
```

Script audit chỉ ghi hồ sơ review tại đây; không sửa state/manifest/checkpoint/dataset và không load model. Byte khác do newline phải được đối chiếu đúng phép tái tạo hash đã pin, không sửa expected hash để ép dữ liệu hợp lệ. Bản audit/hash/PDF của phiên cập nhật trước được giữ nguyên làm lịch sử; hồ sơ `progress-validation-*` ghi riêng các kiểm tra mới.
