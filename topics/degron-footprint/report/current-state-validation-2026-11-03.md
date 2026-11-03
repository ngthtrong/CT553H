# Cập nhật chọn lọc luận văn và đề cương — 03/11/2026

## Phạm vi và bằng chứng

Theo yêu cầu cập nhật trạng thái, lượt này đưa các kết quả quan trọng đã có vào tài liệu, không viết
lại toàn bộ luận văn. Không huấn luyện, chạy lại benchmark, khởi động/dừng campaign, sửa data/protocol,
đổi serving model hoặc đóng G2/G3.

- Luận văn: tóm tắt Anh/Việt, mục tiêu/phạm vi và đóng góp; bổ sung ngắn khái niệm ESM/LoRA và trạng
  thái tích hợp; thêm Chương 4 mục 4.2.3.12–13 về R1/R2/R6 và full-PSI; cập nhật thảo luận, phần còn
  thiếu và kết luận. Số liệu benchmark 91 peptide giữ nguyên.
- Đề cương: giữ bảy phần và ba bảng theo mẫu; đồng bộ câu hỏi nghiên cứu, hai population/metrics,
  kết quả quan trọng, tiến độ local và phạm vi ứng dụng đã chốt. Xuất lại PDF/DOCX từ Markdown.
- Cập nhật README/chỉ dẫn trạng thái liên quan để không tiếp tục mô tả hai tài liệu là bản trước v3.

Nguồn điều khiển: JSON R1/R2/R6 và model card R3; v3 `dataset-build.json`, `output-analysis.json`;
plan/queue/state của local `e7097449883a51d8`; tài liệu/mã ứng dụng và validation prototype. Snapshot
Kaggle cập nhật `2026-11-01T11:18:07Z`; phân tích ngày 02/11; local là snapshot lưu **03/11, 10:17
(UTC+8)**. Status `running` không xác nhận worker trực tiếp. Artifact local nặng/OOF không có trong
checkout này; số hiệu năng local mới không được suy ra từ inner-validation MSE.

Các nguồn và SHA-256 đầu vào/đầu ra được ghi ở
[current-state-validation-2026-11-03.json](current-state-validation-2026-11-03.json) và
[validation đề cương](../proposal/validation.json). Trong PDF, truy vết được trình bày bằng phương
pháp, bảng, diễn giải và trích dẫn học thuật; đường dẫn nội bộ chỉ nằm trong mã/comment/hồ sơ kiểm.

## Kết quả kiểm

- `make -C topics/degron-footprint/report doctor`: đủ môi trường/phông.
- Chạy generator Chương 4: số mới đọc từ JSON; hai bảng full-PSI thêm mới. Toàn bộ bảng/hình cũ không
  đổi; các macro số cũ không đổi.
- `make -C topics/degron-footprint/report all` và `check`: hai PDF **80 trang**, A4, phông nhúng,
  tham chiếu ổn định; không overfull box, thiếu glyph hoặc nhãn/tham chiếu lỗi.
- `make -C topics/degron-footprint/proposal` và `check`: PDF **10 trang**, Letter đúng mẫu; DOCX có
  đủ bảy phần và hình học Letter. Các số full-PSI, CI quan trọng và tiến độ local được đối chiếu với
  JSON nguồn ở cả PDF và DOCX. Builder dùng đúng mẫu ở `reportTemplate/guideline-thesis/` sau di chuyển repo.
- Trích văn bản PDF: khớp số mới; không có đường dẫn bằng chứng nội bộ; tóm tắt Anh/Việt mỗi bản một
  trang. Luận văn còn **7** vị trí `PENDING` tương ứng thông tin/tác vụ chưa hoàn tất, không xóa để tạo
  cảm giác hoàn thành.
- Đã xem ảnh render các trang sửa và hai bảng mới ở cả bản một mặt/hai mặt, toàn bộ đề cương; kiểm
  tiêu đề, font, khoảng cách, bảng, ngắt trang và trạng thái. Không thay đổi bố cục mẫu để giấu nội dung.
- `git diff --check`: đạt. Không commit hoặc push.

## Giới hạn giữ trong tài liệu

Kết quả là development OOF, chưa phải xác nhận ngoài độc lập. Hai tập 91 peptide và full-PSI có
population/metrics khác nhau. LoRA mới xong một fold; các nhánh calibration/locked transfer và final
CNN/LoRA/family export còn thiếu. Serving vẫn là ridge/Platt baseline. Workspace UI dùng fixture
tổng hợp; lưu dự án, jobs, import/comparison, PostgreSQL và tích hợp R3 chưa nghiệm thu.

Smoke PDF cũ chỉ được bộ kiểm định dạng đọc lại; không có lượt smoke nghiên cứu hoặc kiểm thử app
mới. DOCX được kiểm cấu trúc/nội dung, chưa kiểm render trực tiếp bằng Microsoft Word. Các mục cần
cá nhân hóa, khảo sát trong nước, hướng dẫn/nghiệm thu và metadata chưa biết vẫn để chờ xác minh.
