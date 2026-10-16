# Slide PowerPoint cho buổi gặp 16/10/2026 (`.pptx`)

**[degron-footprint-2026-10-16.pptx](degron-footprint-2026-10-16.pptx)** · **26 slide chính + 2 phụ lục** (A1 tài liệu tham khảo, A2 định dạng bản ghi), 16:9, tiếng Anh, **ghi chú người nói** ở mọi slide (tiếng Việt: câu cấm, nhãn bằng chứng, câu trả lời chuẩn bị sẵn). Dựng ngày 15/10/2026 theo yêu cầu của Trọng: *"tạo slide pptx, không phải deck html"* ([D-037](../../../../DECISIONS.md#d-037)).

Nội dung: [brief 26 slide](../slide-content-2026-10-15.md), mọi con số trích từ brief hoặc từ file kết quả của repo. Trạng thái là [DECISIONS.md](../../../../DECISIONS.md#hien-hanh). Đây là **bản thứ ba** cho cùng buổi gặp, cạnh [deck-2026-10-16](../deck-2026-10-16/README.md) và [deck-external-2026-10-16](../deck-external-2026-10-16/README.md); ba bản **không đồng bộ tự động**, chọn một hoặc gộp là việc của Trọng.

## Mở và trình chiếu

Mở bằng PowerPoint (hoặc Keynote / LibreOffice Impress), chế độ **Slide Show**. Chuyển slide bằng hiệu ứng *fade*. **21 slide có animation bấm chuột** (hiện dần từng bước: chuỗi residue → gập → đột biến, E3 → ubiquitin → proteasome, phễu dữ liệu, cột đo 0,7–0,96 …). **Ba GIF chạy ở chế độ Slide Show** (slide 2, 4, 7). Ở chế độ soạn thảo GIF đứng yên ở khung đầu.

## Những gì cần biết trước khi dùng

| Việc | Trạng thái |
|---|---|
| **Q1 và Q4 ở slide 26** | **Trọng tự viết** (việc 9 của brief). Hai ô viền nét đứt hổ phách là chỗ giữ chỗ, **phải thay trước buổi gặp** |
| **Slide 18, ô giấy phép Larsen** | Ghi *"MIT in repo; coverage of the data file awaiting author reply"* thay cho "MIT": [C-11a](../../../../DECISIONS.md#c-11a) vẫn chờ. Lệch nhẹ khỏi brief (brief cố ý không đưa chỗ mơ hồ này lên slide); đổi lại nếu Trọng muốn |
| **Slide 16** | Ma trận ΔPSI thật của `O00468_AGRN_82` (532 ô). Đây là **minh họa nhãn đo**: peptide bão hòa nằm phía đánh giá của split, **không phải ví dụ huấn luyện** (khác giả định của brief) |
| **Slide 25** | G1/G2/G3 gọi là *readiness check nội bộ*, không phải cổng của học phần; bảng tuần là suy ra từ D-029 + D-031, chưa phải quyết định ghi sổ |
| **Kiểm tra** | `validate.py` của skill pptx: **PASSED** (schema, quan hệ, timing). **Chưa mở bằng PowerPoint thật và chưa phát thử animation**: máy này không có LibreOffice. Bố cục kiểm bằng bộ xem trước tự viết ([render_preview.py](render_preview.py), vẽ lại hình khối + bố trí chữ bằng font Calibri thật) và bộ đo tràn chữ trong [lib.py](lib.py). Nên mở file một lần, bấm qua 26 slide, trước khi mang đi |

## Thiết kế

Bảng màu theo brief (nền `#FAFBFC`, chữ `#15323F`, san hô = degron / PSI thấp, xanh mòng = bền, xanh thép = mô hình, hổ phách = chưa đo). **Mẫu bên ngoài đã tra và nguyên tắc vận dụng**, GIF và giấy phép nằm ở [SOURCES.md](SOURCES.md). Motif lặp lại: hàng **ô residue** (dải 28 ô ở slide 1, hàng ô tiến độ mười phần ở chân mỗi slide). Mỗi slide một câu khẳng định làm tiêu đề, phần dưới là bằng chứng (hướng assertion–evidence).

## Dựng lại

```bash
cd topics/degron-footprint/presentation/deck-pptx-2026-10-16
../../../../.venv/bin/python figs.py     # heatmap slide 16, lưới, thang màu → assets/
../../../../.venv/bin/python build.py    # → degron-footprint-2026-10-16.pptx (in cảnh báo tràn chữ nếu có)
../../../../.venv/bin/python render_preview.py degron-footprint-2026-10-16.pptx /đường/dẫn/ra   # PNG xem nhanh bố cục
```

Cần `python-pptx`, `pillow`, `matplotlib`, `numpy` (đã có trong `.venv`) và font Calibri ở `~/.local/share/fonts/ms-office/` cho bộ đo chữ. `figs.py` đọc [measured-example.json](../deck-external-2026-10-16/assets/measured-example.json) (do script [export_example.py](../../research/slide-example-2026-10-15/export_example.py) sinh; chỉ **đọc**, không sửa thư mục đó).

| Tệp | Nội dung |
|---|---|
| [lib.py](lib.py), [comp.py](comp.py) | Theme, khối chữ có đo tràn, bảng, animation XML (fade theo bấm chuột), chuyển slide |
| [part1.py](part1.py) … [part5.py](part5.py) | Slide 1–5, 6–9, 10–14, 15–18, 19–22, 23–28 |
| [figs.py](figs.py) | Hình sinh từ dữ liệu / sơ đồ raster |
| [assets/](assets/) | 3 GIF (kèm [SOURCES.md](SOURCES.md)), heatmap, lưới, thang màu, `figs-meta.json` (SHA-256 đầu vào) |
