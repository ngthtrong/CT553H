# Giới thiệu đề tài và trao đổi tiến độ nghiên cứu

Mở **[index.html](index.html)** trực tiếp bằng Chrome hoặc Edge. Không cần mạng, backend hay cài Node để trình chiếu. Deck gồm **34 slide chính và 16 phụ lục**, tiếng Việt, phục vụ trao đổi với giảng viên.

## Điều khiển

| Thao tác | Phím / nút |
|---|---|
| Chuyển slide | Mũi tên, Space, Page Up/Down; vuốt trên màn hình cảm ứng |
| Mục lục và nhảy slide | `O` / Mục lục |
| Ghi chú và nguồn của slide hiện tại | `N` / Ghi chú |
| Tạm dừng hoặc tiếp tục hình động | `M` / Dừng chuyển động |
| Toàn màn hình | `F` / Toàn màn hình |
| Về đầu / về phần trao đổi | Home / End |

Tự tôn trọng thiết lập giảm chuyển động của hệ điều hành. GIF có poster tĩnh; sơ đồ chuyển động dừng khi slide ẩn hoặc người dùng bấm dừng. Có thể in bằng trình duyệt để có bản tĩnh; bản HTML giữ animation và biểu đồ tương tác ở phụ lục.

## Nội dung và thiết kế

- Slide 1–6: giới thiệu bài toán và ví dụ thực nghiệm.
- Slide 7–9: công trình liên quan, mục tiêu và câu hỏi nghiên cứu.
- Slide 10–15: dữ liệu, xử lý và thiết kế đánh giá.
- Slide 16–28: kết quả theo vấn đề nghiên cứu, tích hợp các bằng chứng liên quan.
- Slide 29–31: công cụ và trạng thái phát triển.
- Slide 32–34: tiến độ, hướng tiếp theo và trao đổi với giảng viên.
- Slide 35–50: phụ lục theo chủ đề, mở khi cần.

[Khảo sát template/style](design-research.md) được thực hiện trước khi dựng. Thiết kế tham khảo Assertion–Evidence/Penn State, Harvard Catalyst, Slidev Academic và hướng thị giác khoa học sự sống của EMBL. Màu và bố cục được dựng riêng cho đề tài, không dùng logo hay nhận diện chính thức của các tổ chức đó.

Tên cấu hình trên màn chiếu được viết bằng lời. Không có mã arm/phiên chạy hay footnote nguồn trên từng slide. Nguồn và điều kiện chi tiết nằm trong ghi chú, phụ lục, [slide-sources.json](slide-sources.json) và [evidence.json](evidence.json).

## Bằng chứng và phạm vi

Biểu đồ được sinh từ kết quả đã lưu, không huấn luyện hoặc đọc tập T để chọn model. Các population/metric khác nhau được ghi trong ghi chú; không gộp thành một đường tiến bộ theo thời gian. Snapshot Kaggle dùng cho phần full-PSI là `2026-11-01T11:18:07Z`. LoRA và các chức năng ứng dụng chưa hoàn tất được thể hiện đúng trạng thái.

Heatmap HIF1A là nhãn đo. GIF Fam188a chỉ minh họa cấu trúc protein. Ảnh giao diện là **prototype thiết kế đang dùng fixture tổng hợp**, không phải kết quả inference thật. Xem [nguồn tài sản](asset-notices.md).

## Tái dựng và kiểm tra

`prepare-assets.py` tạo các figure SVG độc lập bằng Matplotlib và bundle số liệu từ JSON nghiên cứu. Cần Python với numpy/Matplotlib. Các tài sản đã tải được dùng lại từ cache local; nếu thiếu thì script tải font/Chart.js từ nguồn công khai và ghi hash.

```powershell
python -I -X utf8 topics/degron-footprint/presentation/deck-research-overview-2026-11-02/prepare-assets.py
python -I -X utf8 topics/degron-footprint/presentation/deck-research-overview-2026-11-02/build-deck.py
```

`capture-prototype.cjs` và `validate-deck.cjs` dùng Playwright với Chrome headless. Có thể đặt `PLAYWRIGHT_MODULE` tới package Playwright sẵn có. Bản ghi tại [validation.json](validation.json); ảnh từng slide trong [previews/](previews/). Script kiểm đủ 50 slide, chữ tràn khung, ảnh và liên kết local, nhãn cấu hình, điều hướng, mục lục, notes, biểu đồ tương tác, tạm dừng và reduced-motion, cùng nhiều kích thước màn hình. Render cũng được xem bằng mắt; ảnh tổng quan giúp tra cứu bố cục.

Code tạo slide và tài sản nằm riêng trong thư mục này. Deck trước được giữ nguyên.
