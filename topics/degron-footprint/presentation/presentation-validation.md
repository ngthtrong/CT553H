# Kiểm tra trang trình bày — 11/10/2026

> **Lịch sử quyết định:** các câu "chốt / quyết định / khuyến nghị" trong file này phản ánh thời điểm viết, có thể đã bị thay. Trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

Phạm vi: hoàn thiện phần giao diện còn dở trong phiên Claude, tại [presentation.html](presentation.html). Đây là kiểm tra tài liệu HTML; không chạy thêm thí nghiệm ML hoặc xác minh lại toàn bộ y văn.

## Phần đã hoàn thiện

- Gắn hoạt ảnh vào sơ đồ UPS, hai đầu ra kênh nội, khả năng tiếp cận degron, tín hiệu motif và luồng cấu trúc vào kiến trúc đề xuất (khi đó tên là CMIL-E3).
- Thêm ba ô số liệu nền với liên kết audit; biểu đồ gộp trung bình/max lấy từ [pool-test.json](../research/voutsinos-2026-audit/pool-test.json), trục Pearson đầy đủ 0–1, có bảng tương đương và giới hạn phép thử cùng trọng số.
- Thêm minh họa tương tác đổi bối cảnh peptide/protein và độ phơi lộ giả định. Thanh hiển thị không phải xác suất hoặc kết quả mô hình.
- Điều khiển sáng/tối/theo hệ thống, dừng hoạt ảnh, tôn trọng `prefers-reduced-motion`, khung SVG cuộn ngang trên điện thoại, CSS in tĩnh.
- Sơ đồ tự vẽ có nhãn minh họa; bỏ điểm ví dụ 0,7213 để tránh nhầm với số đo. Giới hạn giải thích bất biến hoán vị ở kênh nội cnn2w1; kênh C-term có thông tin vị trí.

## Kiểm tra đã chạy

Chromium headless qua Playwright; chặn yêu cầu HTTPS để kiểm tra khả năng đọc ngoại tuyến bằng font dự phòng.

| Trường hợp | Kết quả |
|---|---|
| Desktop 1440 px, sáng và tối | Không tràn trang; không lỗi JavaScript |
| Điện thoại 390 px, sáng và tối | Không tràn trang; sơ đồ cuộn trong khung |
| Giảm chuyển động | Hoạt ảnh tắt; nút bật chuyển động bị vô hiệu theo cài đặt hệ thống |
| Điều khiển giao diện và dừng hoạt ảnh | Hoạt động |
| Chuyển peptide/protein, thanh rASA | Hoạt động; peptide mở thanh 100%, trở lại protein giữ giá trị người đọc chọn |
| Bảng số liệu mở/đóng | Hoạt động |
| ID, anchor, đường dẫn file nội bộ | Không ID trùng; anchor và file đích tồn tại |
| Tắt JavaScript | Nội dung, sáu hình và bảng vẫn đọc được; điều khiển tương tác ẩn |
| Báo cáo kiểm chứng chi tiết | Mục tài liệu tham khảo hiện diện; không sửa file |
| Chế độ in A4 | Nền trắng theo CSS in kể cả hệ thống tối; hoạt ảnh tắt; xuất được PDF kiểm tra |
| Cấu trúc HTML | Thẻ lồng khớp; caption nằm trong table |

Đã xem ảnh chụp phần đầu desktop, biểu đồ sáng, sơ đồ phơi lộ tối và minh họa tương tác trên điện thoại. Palette hai màu đã chạy lại validator Python của phiên Claude: đạt các cổng lightness/chroma/CVD/normal separation/contrast ở cả hai chế độ, trên surface thực của trang. `git diff --check` đạt.

Ảnh chụp và kết quả kiểm tra tạm: `/tmp/ct553h-presentation-preview/` (không đưa vào Git, có thể bị dọn sau phiên). Công cụ kiểm tra cài tại `/tmp/ct553h-presentation-tools/`, không thay dependency của repository.

## Giới hạn và công việc nghiên cứu còn lại

- Chưa xác minh lại DOI hay đọc thêm bài báo trong lần chỉnh giao diện này; liên kết ngoài được giữ từ phiên Claude.
- Ba cổng nghiên cứu trong [topic-decision.md](../research/topic-decision.md) vẫn còn: bài transcription factor, nhãn E3 thực dùng được và tiền lệ kiến trúc MIL.
- Kiến trúc vẫn là đề xuất; hoạt ảnh và thanh phơi lộ không phải bằng chứng cho hiệu năng hay khả năng chuyển miền.

## Cập nhật 11/10/2026 (khuya) — nội dung đã đổi sau lần kiểm này

Đề tài **tái định tâm** sang bản đồ độ nhạy theo residue; kiến trúc đổi tên **CMIL-E3 → MIL-Degron** và còn 5 thành phần. Trang đã sửa nhiều mục (tiêu đề, đầu vào/đầu ra, phạm vi, bảng kiến trúc, bảng dữ liệu, ba bậc thước đo, bảng năm tiêu chí, mục cổng chặn, tài liệu tham khảo).

**Đã kiểm lại sau khi sửa:** cấu trúc thẻ HTML khớp, không ID trùng, số thứ tự tài liệu tham khảo 1–18 không trùng, mọi liên kết nội bộ tồn tại.

**Chưa kiểm lại:** ảnh chụp, chế độ in, giao diện điện thoại, sáng/tối, giảm chuyển động — các phép kiểm trong bảng trên chạy trước khi sửa nội dung. **Việc còn lại:** sơ đồ SVG luồng dữ liệu vẫn vẽ nhánh *điều kiện E3* đã bỏ; hiện chỉ ghi chú bằng chữ trong `figcaption`, **chưa vẽ lại hình**.
