# Chuẩn bị buổi gặp GVHD

> Cập nhật: 29/09/2026. Chi tiết đề tài: [brainstorm.md](../topics/personal-expense-management/01-idea/brainstorm.md). Dữ liệu: [data-report.md](../topics/personal-expense-management/03-data/data-report.md). Tài liệu phát tay: [topic-summary.pdf](../topics/personal-expense-management/01-idea/topic-summary.pdf).
> Đề tài **chưa chốt**: đi với tâm thế lắng nghe, mang theo đề tài dự phòng #2 (trợ lý mua sắm RAG).

## Mục tiêu buổi gặp

1. GVHD đồng ý hoặc điều chỉnh hướng đề tài, đặc biệt là cách dùng dữ liệu cá nhân **để đánh giá** thay vì để huấn luyện.
2. Hiểu rõ GVHD kỳ vọng gì: tỷ lệ nghiên cứu so với hệ thống, mức độ chặt chẽ.
3. Thống nhất cách làm việc: lịch gặp, kênh liên lạc, các mốc.

## Làm trước buổi gặp

- [x] Xác định nguồn dữ liệu: tự ghi chép trên Notion, 5.465 giao dịch, 09/2022 → 09/2026
- [x] EDA và thử nghiệm sơ bộ (số liệu ở mục Trình bày)
- [x] Chép dòng mẫu **đã ẩn danh** từ `transactions_anon.csv` để minh họa (mục Dữ liệu mẫu)
- [ ] In [topic-summary.pdf](../topics/personal-expense-management/01-idea/topic-summary.pdf) (2 trang A4), hoặc chuẩn bị 5–6 slide theo khung dưới
- [ ] Duyệt và sửa mô tả 25 danh mục trong [categories.json](../../ml/personal-expense-management/experiments/rq1-quick-check/categories.json) (bản nháp, 4 mục đánh dấu `uncertain`)

## Dữ liệu mẫu (đã ẩn danh)

| id | Ngày | Ghi chú | Số tiền (VND) | Nhãn | Minh họa điều gì |
|---:|---|---|---:|---|---|
| 4807 | 2026-09-18 | xăng | 30.000 | DC | Lặp lại rất nhiều (443 lần) |
| 1622 | 2026-09-16 | cf | 10.000 | Coffee | Viết tắt |
| 2057 | 2024-02-28 | cơm sờn | 25.000 | AC | Sai chính tả ("cơm sườn") |
| 573 | 2024-11-07 | bida với [P36] | 16.000 | Bida | Tên người đã được thay bằng mã |
| 3680 | 2026-06-21 | nước mía | 10.000 | AV | Cùng ghi chú… |
| 3690 | 2024-05-01 | nước mía | 10.000 | RL | …nhưng khác nhãn, vì nhãn phụ thuộc ngữ cảnh (đi cùng ai) |

## Trình bày (khoảng 10 phút)

| # | Nội dung | Thông điệp chính |
|---|---|---|
| 1 | Vấn đề | Ghi chép chi tiêu tay tốn công. Ghi chú tiếng Việt ngắn, viết tắt, không dấu. **Mỗi người tự đặt danh mục riêng**, nên mô hình học trên bộ danh mục cố định không dùng được. **Người dùng mới không có dữ liệu**, nên mô hình học máy thông thường chưa giúp được gì trong những tuần đầu, đúng lúc người dùng dễ bỏ cuộc nhất |
| 2 | Dữ liệu | 5.465 giao dịch thật, 49 tháng liên tục, 25 nhãn gán tay, 1.973 nội dung khác nhau, ghi chú trung vị 2 từ. Nguồn: tự ghi chép trên Notion. Đã làm sạch và ẩn danh bằng script |
| 3 | Kết quả sơ bộ | TF-IDF + SVM: 86,7% (kiểm định chéo ngẫu nhiên) nhưng chỉ 78,2% khi chia theo thời gian. Nội dung chưa gặp trong tập kiểm tra tăng từ 34% lên 53%, và có 5 nhãn mới. Dự báo: trung bình lịch sử (sMAPE 24,5%) thắng các baseline khác. **Kiểm tra nhanh hướng mới** (embedding zero-shot, dev 503 mẫu, không học gì từ dữ liệu thật): chỉ có tên danh mục đạt 16–18%; thêm một câu mô tả đạt 40–50%, top-3 khoảng 64% ([kết quả](../../ml/personal-expense-management/experiments/rq1-quick-check/README.md)) |
| 4 | **Ý tưởng chính** | Không dùng dữ liệu cá nhân để huấn luyện. Khi người dùng tạo danh mục (tên + mô tả tùy chọn), hệ thống dùng **LLM zero-shot** và **sinh dữ liệu tổng hợp cho riêng danh mục của người đó** để huấn luyện mô hình nhẹ. Dữ liệu 4 năm với 25 danh mục tự đặt được **phát lại theo thời gian** như một người dùng mới: hệ thống đoán trước, người dùng sửa sau, hệ thống học tiếp |
| 5 | Câu hỏi nghiên cứu | **RQ1** bộ phân loại ban đầu đạt đến đâu khi người dùng vừa tạo danh mục mà chưa có giao dịch nào · **RQ2** các chiến lược học từ phản hồi cải thiện được bao nhiêu **so với baseline nhớ lại**, trên **ghi chú chưa gặp** (nhớ lại + zero-shot đã đạt 71,5%, nhưng chỉ 37% trên ghi chú chưa gặp, nơi tập trung 87% số lần phải sửa) · **RQ3** dự báo khoảng theo danh mục và **ảnh hưởng của lỗi phân loại lên dự báo, cảnh báo ngân sách** · **RQ4** (nếu có tình nguyện viên) kiểm tra trên người khác · **TN5** độ nhạy khi người dùng không sửa hết |
| 6 | Hệ thống, kế hoạch | React · Spring Boot · FastAPI ML service · PostgreSQL + pgvector · Redis. Công cụ phát lại chạy qua API thật nên số liệu là của chính hệ thống. Đa tiền tệ chỉ còn là tính năng phụ. 14 tuần, mốc giữa kỳ tuần 8 |

**Không** trình bày chi tiết đa tiền tệ, CSDL, hay các biến thể của từng chiến lược. Giữ trọng tâm ở ý tưởng "đánh giá bằng phát lại".

## Câu hỏi cho GVHD

**Phạm vi và kỳ vọng** *(quan trọng nhất, hỏi trước)*
1. "Hàm lượng khoa học tương đối" của CT553H cụ thể là mức nào? Tỷ lệ nghiên cứu và hệ thống bao nhiêu là hợp lý?
2. Phạm vi hiện tại đã vừa với 14 tuần làm một mình chưa? Nếu cần cắt thì nên cắt phần nào? (Em đang định cắt theo thứ tự: mở rộng đa tiền tệ → LLM few-shot truy xuất → PhoBERT → kịch bản danh mục chuẩn → tình nguyện viên.)
3. Hội đồng thường thiên về kỹ thuật phần mềm. Thầy/cô khuyên phân bổ báo cáo giữa phần hệ thống và phần thí nghiệm thế nào?

**Phương pháp**
4. Dùng dữ liệu cá nhân chỉ để đánh giá (phát lại theo thời gian), còn huấn luyện bằng dữ liệu tổng hợp do LLM sinh theo danh mục của từng người: thầy/cô thấy cách này có thuyết phục không? Hội đồng có dễ nghi ngờ dữ liệu tổng hợp không?
5. Lấy 25 nhãn gốc làm "danh mục do người dùng tự tạo" (kịch bản chính), gộp về 10–12 danh mục chuẩn làm kịch bản phụ: có hợp lý không? Mô tả danh mục do chính em viết có bị xem là thiên vị không?
6. Dữ liệu đánh giá chủ yếu của một người: cần tối thiểu bao nhiêu tình nguyện viên? Mỗi người tự đặt danh mục và cung cấp 100–200 ghi chú có đủ không? (Em dự định tìm tình nguyện viên ngay sau khi đề tài được chốt.)
6b. Một số khẳng định về nhu cầu người dùng (người Việt có tự tạo danh mục không, chọn danh mục có tốn công không) chưa có nghiên cứu nào xác nhận. Em định làm khảo sát ngắn 30–50 người ở tuần 1–2: như vậy có đủ không? ([literature-survey.md](../topics/personal-expense-management/02-survey/literature-survey.md))
6c. RQ3 được mở rộng thành dự báo khoảng và lan truyền lỗi phân loại sang cảnh báo ngân sách: thầy/cô thấy phạm vi này có quá nặng không?
7. Ngoài Macro-F1 và số lần sửa mỗi tháng, có nên báo cáo MCC không? Thầy/cô yêu cầu kiểm định thống kê nào?
8. Khung 5 bước của Chou có phù hợp, hay thầy/cô muốn khung trình bày khác?
9. Hướng mới nghiêng về LLM (zero-shot, sinh dữ liệu tổng hợp), học trực tuyến và cold-start, ít dùng BERT/CNN hơn hướng cũ. Thầy/cô có thấy ổn khi hướng dẫn mảng này không, hay nên tăng phần embedding / PhoBERT cho gần chuyên môn của thầy/cô hơn?

**Hành chính**
10. Mẫu đề cương và báo cáo, lịch nộp, mốc giữa kỳ?
11. Tần suất gặp, kênh liên lạc (email, Zalo, gặp trực tiếp)?
12. Repo GitHub của em đang public. Em có được để tài liệu môn CS535 thầy/cô gửi trong repo không, hay nên để riêng tư?

**Cơ hội**
13. Nếu kết quả tốt, thầy/cô có muốn hướng tới một bài hội nghị không? (Bộ dữ liệu tổng hợp ghi chú chi tiêu tiếng Việt có thể công bố.)

## GVHD có thể hỏi lại

| Câu hỏi | Trả lời ngắn |
|---|---|
| Phát lại theo thời gian là gì? | Duyệt giao dịch theo đúng thứ tự ngày. Mỗi giao dịch: hệ thống đoán trước bằng những gì đã biết, rồi mới nhận nhãn thật để học tiếp. Không có thông tin tương lai nào lọt vào |
| Sao không huấn luyện trên dữ liệu của em luôn? | Người dùng mới không có dữ liệu. Học từ dữ liệu người dùng vẫn có, nhưng là một chiến lược trong phát lại, được đo đúng trình tự thời gian |
| Dữ liệu tổng hợp có khách quan không? | Prompt chỉ gồm tên và mô tả danh mục, không có ghi chú thật. Tập đánh giá hoàn toàn là dữ liệu thật. Có báo cáo tỷ lệ trùng |
| Có tinh chỉnh trên tập đánh giá không? | Tinh chỉnh trên tập dev (mẫu ngẫu nhiên ~10%, không tính điểm), viết mô tả danh mục trước, khóa cấu hình rồi mới tính điểm trên luồng |
| Danh mục như AC, RL thì LLM hiểu sao được? | Có hai biến thể: chỉ tên và tên + mô tả một câu. Mức thấp ở ngày đầu chính là lý do cần lớp cá nhân học từ phản hồi |
| Nhãn có đáng tin không? | Gán lại mù 300 mẫu, đo Cohen's kappa (dự kiến tuần 2) |
| Nếu mô hình ban đầu đã rất cao? | Kiểm tra trên dev ở tuần 2. Nếu vậy, lấy biến thể "chỉ tên" và các giai đoạn có danh mục mới làm trọng tâm của RQ2 |
| GPU ở đâu? | Colab / Kaggle, dữ liệu nhỏ; chỉ đưa bản đã ẩn danh lên cloud và API |

## Sau buổi gặp

- [ ] Ghi biên bản vào `session-01-minutes.md` ngay sau buổi gặp
- [ ] Cập nhật [brainstorm.md](../topics/personal-expense-management/01-idea/brainstorm.md) theo góp ý
- [ ] Nếu GVHD đề xuất đổi hướng: cùng Claude so sánh lại với đề tài dự phòng
