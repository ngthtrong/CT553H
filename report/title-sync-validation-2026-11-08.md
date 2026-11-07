# Đồng bộ tên đề tài và chuyển slide sang tiếng Anh — 08/11/2026

Tên do tác giả cung cấp ngày 07/11; hoàn tất kiểm tra sau khi chuyển sang ngày 08/11 (UTC+8).

- **Tiếng Việt:** Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong nghiên cứu degron và xây dựng công cụ phân tích
- **Tiếng Anh:** Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Assays and Development of an Analysis Tool

Nguồn tên chính: `report/config/metadata.tex` (`\ThesisTitle`, tiếng Anh) và
`proposal/proposal.md` (`subtitle`, tiếng Việt). Slide đọc trực tiếp hai nguồn
này; tên tiếng Việt nằm trong metadata và Notes bìa, nội dung trình chiếu bằng tiếng Anh.

## Tệp bàn giao và kết quả

| Tài liệu | Kết quả |
| --- | --- |
| [Slide PPTX](../presentation/Degron_Research_Report.pptx) / [PDF](../presentation/Degron_Research_Report.pdf) | 94 slide; nội dung và Notes tiếng Anh; 8 biểu đồ native giữ nguyên dữ liệu số |
| [Luận văn một mặt](build/content/content.pdf) / [hai mặt](build/content-twoside/content.pdf) | 121 trang mỗi bản; bìa, biểu mẫu, metadata PDF và đầu trang dùng tên mới |
| [Đề cương PDF](../proposal/proposal.pdf) / [DOCX](../proposal/proposal.docx) | PDF 10 trang; subtitle đúng tên tiếng Việt; thân đề cương giữ snapshot 03/11 |

PASS: build/check hai bản luận văn, gồm đối chiếu danh mục/nhãn/tham chiếu hình
bảng; build/check PDF và DOCX đề cương; 16 kiểm cấu trúc, 16 kiểm số liệu,
kiểm ngôn ngữ và text/layout slide; `git diff --check`.

Đối chiếu toàn bộ văn bản PDF sau chuẩn hóa khoảng trắng và loại đúng phần tên
đề tài/đầu trang cho thấy không có thay đổi nội dung còn lại: 121 trang ở mỗi
bản luận văn, 10 trang đề cương. Hash của **232 tệp nguồn nội dung khoa học**
không thay đổi; thân Markdown đề cương giữ nguyên. Thứ tự 94 slide, dữ liệu số
của 8 chart, 88 recipe v3 và 23 recipe R6 được giữ.

## Rà trực quan và phạm vi

Đã xem đủ 94 slide tiếng Anh qua 12 contact sheet; xem riêng bìa và các khung
chữ cần chỉnh. Hai trang có chỉnh câu chữ cuối (11/48) đã được xem riêng ở
1280×720; 92 trang còn lại có pixel hash trùng bộ ảnh đã rà.
Luận văn: xem bìa ngoài/trong, trang xác nhận, cam đoan và đầu trang ở cả hai
bản (trang vật lý 1/2/3/6/14). Đề cương: xem trang 1/2. Không mở ứng dụng
Microsoft PowerPoint/Word trong lượt này.

Validator đề cương trước đây đối chiếu tiến độ 03/11 với `state.json` đang
thay đổi, gây lỗi khi chỉ dựng lại tên. Đã giữ nguyên biên bản cũ từng byte tại
[validation-snapshot-2026-11-03.json](../proposal/validation-snapshot-2026-11-03.json)
và dùng biên bản này cho hai claim tiến độ lịch sử. Các metric khác tiếp tục
đối chiếu JSON nguồn. Đây là dùng lại kết quả kiểm đã lưu, không xác minh lại
các job tại mốc lịch sử hoặc cập nhật tiến độ hiện tại.

Không đổi số liệu, dữ liệu, campaign state, checkpoint, serving model hoặc
quyết định G2/G3. Template gốc giữ nguyên. Các deck overview bị xóa sẵn ngoài
phạm vi được giữ nguyên trạng; không commit/push. Build không đồng nghĩa
nghiệm thu nghiên cứu.

Hash và kiểm chi tiết: [JSON](title-sync-validation-2026-11-08.json),
[validation slide](../presentation/research-report/VALIDATION.md),
[validation đề cương](../proposal/validation.json).
