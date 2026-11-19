# Kịch bản demo 3–5 phút (bảo vệ luận văn)

Dùng app thật trên máy tác giả (`DF_EMBEDDED_WORKER=1 make dev-api` + `npm run dev`, theme sáng, cửa sổ 1440×900).
Không có clip dự phòng (bỏ theo yêu cầu 17/11); nếu app không chạy được khi bảo vệ, dùng ảnh từng màn hình ở
[docs/screenshots/](docs/screenshots/). Nói rõ ngay đầu: đây là công cụ phần
mềm trên một benchmark development, **không** phải kiểm chứng sinh học.

| Phút | Thao tác | Điều cần nói |
| --- | --- | --- |
| 0:00–0:40 | `/protein/A6NMZ7` → chọn tile 28 | Tile 28 aa bước 23; mỗi ô của bản đồ tile có nhãn miền theo cổng R3 (đo / dự đoán / borderline), không chỉ màu |
| 0:40–1:40 | Màn kết quả: banner miền → cảnh báo → nhãn bằng chứng → heatmap → footprint → top 10 | Thứ tự cảnh báo trước điểm số là cố ý; Viridis đảo cho xác suất, PuOr cho raw; footprint là trung bình 19 thế mỗi vị trí, tính lại từ cùng 532 ô; top 10 có nhãn "hồi cứu, development" đứng trước số |
| 1:40–2:20 | "Save to project" → analysis đã lưu → tab ClinVar | Lưu là hành động chủ động; snapshot giữ model, cổng và chú giải của ngày lưu, không tính lại; bốn trạng thái "không có gì để hiện" được tách riêng |
| 2:20–3:30 | New analysis → Whole protein → PTEN → xem trước → Submit | 17 cửa sổ, đoạn 397–403 không được phủ; job bền: worker riêng, có thể tắt máy giữa chừng và chạy tiếp (DEP-02); job ra `partial` vì cổng từ chối 2 tile ngoài miền |
| 3:30–4:20 | Trang project (History · Jobs · Datasets) → Import (nếu còn thời gian) | Import chỉ để so sánh, không retrain; lỗi chặn commit, cảnh báo phải xác nhận; mỗi file là một revision bất biến |
| 4:20–5:00 | Model & evidence | Model `m3-ext4.0-platt-v1`, cổng `gate-r3-v1`; số liệu đều đọc từ registry; giới hạn bằng chứng |

Câu hỏi hay gặp:

- *Vì sao một số peptide huấn luyện bị từ chối?* — cổng R3 xếp 11/176 tile huấn luyện vào "ngoài miền" theo PSI của sàng;
  đó là hệ quả của cổng (độ chính xác in-domain 0,934), không phải lỗi (`DEVIATIONS.md` §7).
- *Số đo hiệu năng?* — p95 một tile ≈ 10 ms, click → heatmap p95 ≈ 0,63 s, protein 8.797 aa ≈ 21 s trên máy tác giả
  (`acceptance-2026-11-17.md` §2).
