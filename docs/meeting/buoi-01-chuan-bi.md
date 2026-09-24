# Chuẩn bị buổi gặp GVHD

> Chi tiết đề tài: [de-tai-1-brainstorm.md](../01-y-tuong/de-tai-1-brainstorm.md). Đề tài **chưa chốt**: đi với tâm thế lắng nghe, mang theo đề tài dự phòng #2 (trợ lý mua sắm RAG).

## Mục tiêu buổi gặp

1. GVHD đồng ý hoặc điều chỉnh hướng đề tài.
2. Hiểu rõ GVHD kỳ vọng gì: tỷ lệ nghiên cứu so với hệ thống, mức độ chặt chẽ.
3. Thống nhất cách làm việc: lịch gặp, kênh liên lạc, các mốc.

## Làm trước buổi gặp

- [ ] Xác định nguồn dữ liệu (app ghi chép tay hay sao kê ngân hàng), chép 3–5 dòng mẫu **đã ẩn danh**
- [ ] EDA nhanh để có số thật điền vào slide 2 (các chỗ `___` bên dưới)
- [ ] Kiểm tra nhanh: TF-IDF + Logistic Regression với GroupKFold theo người bán → Macro-F1 = `___`
- [ ] In hoặc chuẩn bị 5–6 slide (hoặc 1–2 trang A4) theo khung dưới

## Trình bày (khoảng 10 phút)

| # | Nội dung | Thông điệp chính |
|---|---|---|
| 1 | Vấn đề | Ghi chép chi tiêu thủ công tốn công; app hiện có phân loại theo quy tắc, chưa hiểu tốt giao dịch tiếng Việt. Chưa thấy công trình phân loại giao dịch tiếng Việt |
| 2 | Dữ liệu | `___` giao dịch thật (2022 → nay), `___` danh mục, `___` mô tả khác nhau, `___` người bán. Nguồn: `___` |
| 3 | Nghiên cứu theo **5 bước của Chou** | (1) Benchmark: ẩn danh, **loại trùng theo người bán (như CD-HIT)**, đo Cohen's kappa của nhãn · (2) Biểu diễn: TF-IDF, fastText, embedding đa ngôn ngữ, PhoBERT · (3) Thuật toán: LR/SVM → PhoBERT → LLM · (4) GroupKFold + tập kiểm tra độc lập 2025–2026, 5 seed, McNemar, MCC, SHAP · (5) Web server = hệ thống hoàn chỉnh |
| 4 | Câu hỏi nghiên cứu | **RQ1** phân loại (nhấn mạnh người bán chưa gặp) · **RQ2a** dữ liệu thay đổi theo thời gian, chiến lược huấn luyện lại · **RQ2b** người dùng mới (dữ liệu tình nguyện viên) · **RQ3a/b** dự báo chi tiêu, ảnh hưởng tỷ giá |
| 5 | Hệ thống | 1 hình kiến trúc (React · Spring Boot · FastAPI ML service · PostgreSQL · Redis). **Đa tiền tệ chỉ 1 slide**: phí đổi tiền ẩn, tách biến động tài sản, gợi ý lượng cần đổi |
| 6 | Kế hoạch và rủi ro | 14 tuần, mốc giữa kỳ tuần 8. Rủi ro chính: bài toán quá dễ do mô tả lặp lại, nhãn nhiễu, dữ liệu một người → đã có cách xử lý |

**Không** trình bày 11 vấn đề đa tiền tệ hay chi tiết CSDL. Giữ trọng tâm ở ML.

## Câu hỏi cho GVHD

**Phạm vi và kỳ vọng** *(quan trọng nhất, hỏi trước)*
1. "Hàm lượng khoa học tương đối" của CT553H cụ thể là mức nào? Tỷ lệ nghiên cứu và hệ thống bao nhiêu là hợp lý?
2. Theo thầy/cô, phạm vi hiện tại đã vừa với 14 tuần làm một mình chưa? Nếu cần cắt thì nên cắt phần nào?
3. Hội đồng thường thiên về kỹ thuật phần mềm. Thầy/cô khuyên phân bổ báo cáo giữa phần hệ thống và phần thí nghiệm thế nào?

**Phương pháp**
4. Trình bày theo khung 5 bước của Chou có phù hợp không, hay thầy/cô muốn khung khác?
5. Dữ liệu chủ yếu của một người có chấp nhận được không? Cần tối thiểu bao nhiêu tình nguyện viên?
6. Ngoài Macro-F1, có nên báo cáo MCC không? Thầy/cô có yêu cầu độ đo hay kiểm định thống kê nào khác?

**Hành chính**
7. Mẫu đề cương và báo cáo, lịch nộp, mốc giữa kỳ?
8. Tần suất gặp, kênh liên lạc (email, Zalo, gặp trực tiếp)?

**Cơ hội**
9. Nếu kết quả phân loại giao dịch tiếng Việt tốt, thầy/cô có muốn hướng tới một bài hội nghị không?

## GVHD có thể hỏi lại

| Câu hỏi | Trả lời ngắn |
|---|---|
| Tập kiểm tra độc lập là gì? | Dữ liệu 2025–2026, chia theo thời gian, không dùng khi huấn luyện |
| Loại dữ liệu trùng thế nào? | Chuẩn hóa mô tả thành nhóm người bán, GroupKFold theo nhóm; báo cáo tách người bán đã gặp / chưa gặp |
| Kết quả có ổn định không? | 5 seed, trung bình ± độ lệch chuẩn, kiểm định McNemar |
| Nhãn có đáng tin không? | Gán lại mù 300–500 mẫu, Cohen's kappa = `___` (hoặc "sẽ đo ở tuần 2") |
| Nếu PhoBERT không thắng TF-IDF? | Vẫn là kết quả: phân tích vì sao (mô tả ngắn, không dấu, lặp lại), so sánh chi phí và độ trễ |
| GPU ở đâu? | Colab / Kaggle, dữ liệu nhỏ; chỉ đưa dữ liệu đã ẩn danh lên cloud |

## Sau buổi gặp

- [ ] Ghi lại ngay các góp ý và quyết định của GVHD
- [ ] Cập nhật [de-tai-1-brainstorm.md](../01-y-tuong/de-tai-1-brainstorm.md) theo góp ý
- [ ] Nếu GVHD đề xuất đổi hướng: cùng Claude so sánh lại với đề tài dự phòng
