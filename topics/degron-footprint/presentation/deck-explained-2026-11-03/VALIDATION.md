# Kiểm tra deck — 03/11/2026

**PASS:** 31 slide chính và 5 phụ lục, HTML chạy offline và PDF 36 trang. Kết quả chi tiết trong `validation.json`.

## Nội dung và nguồn

- Hai annotation đã áp dụng: không có slide lộ trình học sáu buổi; phần dữ liệu không trình bày các phiên bản hoặc so sánh số liệu theo phiên bản.
- Số đếm saturation/scanning đọc từ `dataset-build.json`; metric, seed/fold và CI đọc từ `output-analysis.json` / `output-analysis-details.json`.
- Hash các nguồn số liệu và tài sản khớp khi kiểm tra. Các file của deck ngày 02/11 giữ nguyên theo `reuse-manifest.json`.
- Không chạy huấn luyện, đọc locked T, thay campaign hoặc đổi model phục vụ. Đây là kiểm tra artifact trình bày.

## Trình duyệt và tương tác

- Không lỗi JavaScript, không ảnh/đường dẫn local hỏng, không yêu cầu HTTP khi trình chiếu offline.
- Toàn bộ 36 slide được render và kiểm hình học; không phát hiện chữ/hình vượt vùng nội dung.
- Điều hướng từng bước, chuyển thẳng slide, mục lục 36 mục, mở notes, đổi MAE/AUROC/AP đều đạt.
- Video MP4 giải mã đủ 1820×1080, dài 12,32 giây; thời gian phát thực tăng trong kiểm tra. Dừng khi chuyển slide hoặc tạm dừng chuyển động.
- Một yêu cầu range của video bị Chromium hủy khi đổi slide được ghi riêng trong `cancelled_media_requests`; movie đã được kiểm phát thành công, không có lỗi tải còn lại.
- Giảm chuyển động dùng poster cho GIF/video; CSS animation dừng khi tạm dừng.
- Khung deck nằm trong viewport ở 1280×720, 1920×1080, 390×844 và 844×390; không tràn ngang tài liệu. Trên điện thoại deck giữ tỷ lệ 16:9.

## PDF và kiểm tra bằng mắt

- PDF có đúng 36 trang tỷ lệ 16:9, không có trang trắng; trang ít chữ nhất có 185 ký tự trích xuất được.
- `pdffonts` xác nhận mọi font được nhúng; có mapping Unicode.
- Bản in hiển thị toàn bộ fragment, poster video/GIF và biểu đồ SVG thay canvas; canvas tương tác được ẩn hoàn toàn khi in.
- Đã xem contact sheet của toàn bộ slide chính/phụ lục và render PDF các trang 3, 13, 20, 23, 27, 30, 36. Đã sửa nhãn fold chồng nhau, kích thước sơ đồ công việc, phần giải thích CI, cách hiển thị screenshot và biểu đồ trùng khi in.
- Ảnh từng slide và contact sheet nằm trong `previews/`. Font/ảnh/video/đồ thị có nguồn trong `asset-notices.md`, `media-sources.json` và `evidence.json`.

`git diff --check` và kiểm tra whitespace riêng cho các file mới đạt. Thay đổi chỉ nằm trong thư mục deck mới; không commit.

## Cập nhật tên đề tài

Ngày 04/11/2026: bộ dựng đọc tên trực tiếp từ trường `subtitle` của đề cương, giữ nguyên cách viết trong tài liệu. Tiêu đề trang mở đầu, tab trình duyệt và PDF được dựng lại từ cùng nguồn tên này.

Theo yêu cầu đổi tên cả hai bản slide, tiêu đề được đồng bộ với tên trong `proposal/proposal.md`: “Dự đoán hiệu ứng đột biến degron ở mức residue và xây dựng công cụ hỗ trợ phân tích”. Trang mở đầu, tiêu đề trình duyệt/PDF, mục đầu của mục lục và ghi chú dùng cùng tên. Cỡ chữ trang mở đầu được căn lại cho tiêu đề đầy đủ. HTML/PDF và ảnh preview đã được dựng lại; các slide từ 2 đến 36, tài sản và số liệu được đối chiếu với bản trước khi đổi tên.
