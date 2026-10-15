# Sàng lọc biến thể protein nhiều tầng theo ngân sách tính toán, dùng PLM

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026** (mới mở hồ sơ).

| | |
|---|---|
| Lĩnh vực | Tin sinh học, protein, mô hình ngôn ngữ protein (PLM); tầng hệ thống/thuật toán suy luận |
| Dữ liệu | ProteinGym substitutions (217 assay DMS, ~2,5 triệu biến thể) + điểm các mô hình đã công bố. Chưa tải |
| Giai đoạn | Mới khảo sát tiền lệ qua tóm tắt tìm kiếm; **chưa đọc toàn văn bài nào**, chưa tải dữ liệu |

## Bài toán

Cho một protein và một thư viện biến thể, dùng PLM huấn luyện sẵn chấm điểm zero-shot rồi xếp hạng để chọn ứng viên đem thử nghiệm. Nhãn DMS chỉ dùng để **đánh giá**. Câu hỏi tính toán: dưới một ngân sách tính toán cố định, phân bổ thế nào giữa bộ chấm rẻ và bộ chấm đắt để thu hồi được nhiều biến thể tốt nhất.

- **Đầu vào:** trình tự gốc (FASTA); thư viện biến thể; danh sách bộ chấm kèm chi phí đo được; ngân sách B (GPU-giây hoặc bộ nhớ).
- **Đầu ra:** top-K biến thể; đường cong recall@K theo ngân sách; tỉ lệ bỏ sót ở tầng sàng đầu tiên.

**Định vị lại so với bản mô tả gốc:** phải chuyển trọng tâm sang **thư viện tổ hợp** (nơi pseudo-likelihood tốn N·L lượt chạy), không phải biến thể đơn — xem [deep-dive §2.1](research/deep-dive-2026-10-12.md).

## Cổng G1/G2/G3

| Cổng | Trạng thái | Ghi chú |
|---|---|---|
| G1 nhãn độc lập | **Đạt** — nhãn DMS thực nghiệm, chỉ dùng để đánh giá | Chưa audit assay cụ thể |
| G2 đóng góp dương | **Chưa rõ, rủi ro cao.** Phần tốc độ/bộ nhớ đã có tiền lệ gần trùng (ESME, Shao 2026). Phần còn trống (cascade theo ngân sách) chỉ có nghĩa nếu bộ chấm đắt thật sự tốt hơn bộ rẻ — bằng chứng hiện có nói chênh lệch **nhỏ** | Chưa có số đo |
| G3 ứng dụng | **Tốt**: web nhập FASTA + danh sách biến thể + ngân sách → bảng xếp hạng | Chưa thiết kế |

## Rủi ro chính

- **Lý do cần nghiên cứu yếu với biến thể đơn.** Toàn bộ ~450 triệu biến thể missense của người đã được tính sẵn và công khai (ESM1b — Brandes *Nat Genet* 2023; AlphaMissense; VespaG). Không được trình bày đề tài như thể việc chấm biến thể đơn còn đắt.
- **Ba hướng B, C và phần "mô hình nhỏ" đã có tiền lệ gần trùng:** ESME (*iScience* 2025), Shao 2026 (bioRxiv), OFS (2024), VespaG (2024), VESM (*Nat Methods* 2026).
- **Chất lượng đạt đỉnh quanh 650M.** Ba nguồn độc lập đều cho thấy lên 3B/15B gần như không tăng chất lượng. Nếu đúng thì tầng 2 của cascade vô nghĩa.
- **Không đáp ứng kỳ vọng "kiến trúc chưa ai dùng"** của GVHD nêu ngày 11/10 ([people.md](../../../project/people.md)) — cùng rủi ro với [C-3](../../../DECISIONS.md).
- Khớp GVHD chỉ ở mức trung bình: đúng protein + PLM, nhưng danh mục GVHD là phân loại có giám sát, không có bài nào về dự đoán hiệu ứng đột biến.
- Quy ước ngôn từ: **không nói "chưa ai làm cascade theo ngân sách"** — mới tra 2 lượt qua tóm tắt.

## Việc tiếp theo

1. **Kiểm G2 trước mọi thứ khác:** tải điểm các mô hình đã công bố trên ProteinGym, đo xem bộ chấm đắt (3B/15B, ensemble) có thật tốt hơn bộ rẻ (650M, VespaG) không. Làm được trên CPU trong 1–2 ngày. Nếu chênh lệch nhỏ thì đóng hướng này.
2. Đọc toàn văn Shao 2026 và ESME để xác định phần nào của hướng B/C đã bị chiếm.
3. Đếm số assay tổ hợp (nhiều đột biến) trong ProteinGym — quyết định xem trọng tâm tổ hợp có đủ dữ liệu không.

## Trong thư mục này

- [log.md](log.md) — nhật ký nghiên cứu
- [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md) — kiểm từng giả định của bản mô tả gốc, bảng tiền lệ
