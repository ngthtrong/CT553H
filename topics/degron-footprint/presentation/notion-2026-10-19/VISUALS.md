# Hình minh họa trên Notion — 19/10/2026

[Trang chính](https://app.notion.com/p/3fe4c97ef69581ed968df52b445de084) và ba trang con được bổ sung hình theo yêu cầu của Trọng. Không có thí nghiệm hoặc quyết định mới.

| Hình | Loại và nguồn | Vị trí |
|---|---|---|
| `visuals/biology.png` | Sơ đồ giáo dục tự dựng bằng `visuals.py`: minh họa một con đường ubiquitin–proteasome, không khẳng định cơ chế của peptide cụ thể | Trang chính §1 |
| `visuals/mutation-map.gif` | GIF tự dựng, 4 khung; ví dụ A4V và ΔPSI +1,0 hoàn toàn giả định. Ma trận rút gọn 7 × 5 để đọc được | Trang chính §3; trang con residue |
| `visuals/assay.png` | Sơ đồ giáo dục tự dựng từ quy trình GPS trong hồ sơ Zhang; màu sáu nhóm không phải cường độ đo | Trang chính §6; trang con dataset |
| `../pptx-2026-10-16/assets/example-heatmap.png` | Hình đã có: dữ liệu AGRN `O00468_AGRN_82`, WT PSI 2,8782551625. Nguồn số: `../deck-2026-10-16/assets/measured-example.json`; metadata ảnh: `../pptx-2026-10-16/assets/figs-meta.json` | Trang chính §5; trang con residue |
| `png/fig-benchmark.png` | Hình đã có từ `figures.py`, số từ hai báo cáo G2 18/10. Caption bổ sung: trục bắt đầu 0,70; Degformer học lại chỉ một seed; trần đo lường không phải điểm cam kết | Trang con kết quả |

Ba sơ đồ mới là tài sản tự dựng cho dự án, không dùng hình tạo sinh. Heatmap/benchmark giữ nguồn dữ liệu trong hồ sơ hiện có. GIF tổng hợp protein Commons đã có từ trước được giữ nguyên cùng ghi công và CC BY-SA 3.0.

Các hình mới được upload vào Notion thành file ảnh/GIF, không trỏ tới đường dẫn máy cục bộ. Hai sơ đồ Mermaid bổ sung mô tả nguồn thông tin của mô hình và cách chia tập theo cụm; không khẳng định kiến trúc mới hay phép chia cụ thể nào ngoài giao thức hiện có.

## Dựng lại và kiểm tra

```bash
.venv/bin/python topics/degron-footprint/presentation/notion-2026-10-19/visuals.py
```

- Đã xem preview ba sơ đồ mới và hai ảnh dùng lại; sửa tiêu đề dài vượt khung ở hình sinh học.
- GIF mới có 4 khung, 1400 × 690 px; kiểm bằng Pillow trong `.venv`.
- Đã fetch lại cả bốn trang: trang chính có 6 ảnh và 2 Mermaid, giữ đủ 3 child-page block; trang con residue có 2 ảnh, dataset có 1 ảnh và 2 Mermaid, kết quả có 1 ảnh.
- Chưa kiểm bằng giao diện Notion thực tế; readback xác nhận block ảnh/GIF và sơ đồ, không xác nhận GIF phát trong trình duyệt.
- `visual-page-0.md` đến `visual-page-3.md` giữ nội dung readback sau cập nhật; `advisor-overview.md` là bản trước khi bổ sung hình.
