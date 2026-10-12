# Nhật ký đề tài `budgeted-plm-variant-scoring`

> Mới nhất ở trên. Trạng thái hiện hành chỉ ghi ở [DECISIONS.md](../../DECISIONS.md).

---

## 12/10/2026 — mở hồ sơ, kiểm tiền lệ của bản mô tả gốc

- Nguồn: Trọng dán bản mô tả "Lựa chọn 1" vào phiên làm việc, yêu cầu xem xét và nghiên cứu thêm. Bản mô tả không rõ nguồn gốc (link có `utm_source=chatgpt.com`); mọi đóng góp trong đó là **giả thuyết cần kiểm chứng**, chính bản mô tả cũng nói vậy.
- Tra 6 lượt. Kết quả ghi ở [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md). **Ba phát hiện làm thay đổi đề tài:**
  1. **Hướng B gần trùng hoàn toàn với ESME** (Çelik & Xie, *iScience* 2025): FlashAttention + sequence packing + batch theo số token + lượng tử, nhanh hơn 4–9×, bộ nhớ giảm 3–14×, có repo công khai.
  2. **Hướng C trùng gần hết với Shao 2026** (bioRxiv): 6 cấu hình số học × 3 cỡ ESM-2 trên toàn bộ ProteinGym; chỉ 3/18 tổ hợp Pareto-tối ưu và **cả ba đều là 650M**.
  3. **"ESMIN 2026" trong bản mô tả không tra được.** Nhiều khả năng là VESM (*Nat Methods* 2026). Phải sửa hoặc bỏ trước khi đưa vào đề cương.
- Vấn đề với lý do cần nghiên cứu: với **biến thể đơn**, điểm cho toàn bộ ~450 triệu biến thể missense của người đã công khai (ESM1b — Brandes *Nat Genet* 2023; VespaG chạy cả proteome < 30 phút trên laptop). Phải chuyển trọng tâm sang **thư viện tổ hợp** mới có lý do.
- Phần còn trống (tra 2 lượt, **[CHƯA KIỂM]**): hướng A — sàng nhiều tầng dưới ngân sách tính toán cố định, đo top-K recall. Gần nhất là TopVIP (*Cell Systems* 2024) nhưng nó phân bổ ngân sách **thí nghiệm ướt**, không phải tính toán.
- **Rủi ro G2 lớn nhất:** ba nguồn độc lập (Shao 2026, ESME, VESM) đều nói chất lượng đạt đỉnh quanh 650M. Nếu bộ chấm đắt không hơn bộ rẻ thì tầng 2 của cascade vô nghĩa. Thí nghiệm kiểm giả định này làm được trên CPU trong 1–2 ngày, ghi ở mục 7 của deep-dive.
- Chưa đọc toàn văn bài nào, chưa tải dữ liệu, chưa chạy mô hình.
