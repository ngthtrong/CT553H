# Công cụ audit calibration và miền áp dụng cho bộ dự đoán mCNN+PLM — ứng viên A4

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../../DECISIONS.md) — hiện là **đề tài dự phòng** theo [D-023](../../../DECISIONS.md#d-023). Cập nhật lần cuối: **12/10/2026**.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, tầng công cụ: độ tin cậy, conformal prediction, phát hiện ngoài miền (OOD) |
| Dữ liệu | Dùng lại mô hình và dữ liệu của GVHD (ATP-binding, efflux, FAD…); tự dựng tập kiểm tra cùng họ/khác họ theo UniProt/Pfam. Chưa tải |
| Giai đoạn | Mới khảo sát qua tóm tắt tìm kiếm; **chưa đọc toàn văn nguồn nào** |

## Bài toán
Mô hình mCNN+PLM của GVHD xuất điểm số được đọc như "độ tin cậy", nhưng chưa công trình nào trong danh mục GVHD kiểm tra xem điểm đó **có được hiệu chỉnh** (90% tin cậy có ứng với 90% đúng không), cũng như **mô hình có tự hạ độ tin cậy** khi protein nằm xa mọi họ đã học hay không.

- **Đầu vào:** mô hình mCNN+PLM đã huấn luyện, điểm dự đoán thô, embedding PLM, định nghĩa "họ đã huấn luyện".
- **Đầu ra:** chỉ số calibration (ECE, reliability diagram); cờ miền áp dụng cho từng dự đoán (trong miền / gần biên / ngoài miền); **bằng chứng cờ có ý nghĩa** (nhóm bị gắn cờ có tỉ lệ lỗi thật cao hơn); một thư viện dùng lại được.

## Cổng G1/G2/G3
| Cổng | Trạng thái | Ghi chú |
|---|---|---|
| G1 nhãn độc lập | Khả quan — dùng lại nhãn thực nghiệm của các bài toán GVHD | Chưa audit |
| G2 đóng góp dương | **Khả quan nhất trong nhóm A.** Mục tiêu là đo và gắn cờ, ít phụ thuộc kết quả "âm". Phải chứng minh cờ thật sự tách được lỗi | Chưa có số đo |
| G3 ứng dụng | **Tự nhiên:** lớp cảnh báo gắn vào web server dự đoán | — |

## Rủi ro chính
- Khoảng trống chỉ dựa trên tóm tắt tìm kiếm (chưa thấy tiền lệ trực tiếp áp conformal/OOD cho đúng lớp PLM-classifier). Cần kiểm kỹ, đặc biệt là bài Nature Methods 04/2026 về "hàng xóm lạ" trong embedding.
- Cần mã nguồn hoặc trọng số mô hình của GVHD; nếu không có thì phải tự huấn luyện lại baseline tương đương.
- ~~Dạng công cụ có thể không đáp ứng kỳ vọng "kiến trúc mới" của GVHD.~~ **Rủi ro này đã được gỡ:** GVHD chấp nhận đóng góp dạng công cụ ([D-022](../../../DECISIONS.md#d-022)). Vẫn nên xác nhận lại ở tuần 6 ([C-5](../../../DECISIONS.md)).
- **Rủi ro còn lại lớn nhất:** khoảng trống **hoàn toàn chưa kiểm** — chưa đọc toàn văn nguồn nào. Bài *Nature Methods* 04/2026 về "hàng xóm lạ" trong không gian embedding có thể đang chiếm đúng chỗ này.
- Đây là phiên bản tổng quát của ý tưởng "cảnh báo miền áp dụng" trong RTK–ATP cũ ([archive](../rtk-atp-applicability/)).

## Việc tiếp theo
1. Đọc toàn văn các nguồn về conformal/OOD cho PLM (bao gồm Nature Methods 04/2026).
2. Chọn 1 mô hình GVHD có mã công khai (ví dụ RTK_RAG, mCNN-GenEfflux) và thử đo ECE.

## Trong thư mục này
- [log.md](log.md) · [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md)
- Nguồn danh mục: [surveys/bioinformatics-tool-layer-candidates-2026-10-12.md](../../../surveys/bioinformatics-tool-layer-candidates-2026-10-12.md) (mục A4)
