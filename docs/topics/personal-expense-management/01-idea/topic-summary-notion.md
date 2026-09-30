# Hệ thống quản lý chi tiêu cá nhân với bộ phân loại giao dịch tự thích nghi

> Bản tóm tắt để nhập vào Notion. Cập nhật 29/09/2026. Trạng thái: **đề tài chưa chốt, chưa gặp GVHD**. Chi tiết: [de-tai-1-brainstorm.md](de-tai-1-brainstorm.md).

**Tên tiếng Anh (đề xuất):** Building a Personal Expense Management System with a Feedback-Adaptive Transaction Classifier and Spending Forecasting

---

## Vấn đề

- Ghi chép chi tiêu bằng tay tốn công: mỗi lần phải gõ nội dung **và** chọn danh mục, nên người dùng hay bỏ cuộc.
- Ghi chú tiếng Việt tự gõ rất ngắn, viết tắt, không dấu, sai chính tả ("cf", "cơm sờn", "xăng").
- **Mỗi người tự đặt danh mục riêng.** Mô hình học trên một bộ danh mục cố định không dùng được cho danh mục tự tạo.
- **Người dùng mới chưa có dữ liệu.** Mô hình học máy thông thường cần hàng trăm giao dịch đã gán nhãn mới giúp được, trong khi những tuần đầu lại là lúc người dùng dễ bỏ cuộc nhất.

## Ý tưởng chính

1. Khi người dùng tạo danh mục (tên + một câu mô tả tùy chọn), hệ thống dùng **LLM zero-shot** và **sinh dữ liệu tổng hợp cho riêng bộ danh mục đó** để huấn luyện một mô hình nhẹ. Nhờ vậy bộ phân loại **dùng được ngay từ ngày đầu**.
2. Mỗi lần người dùng sửa gợi ý, hệ thống **học từ phản hồi** và ngày càng đoán đúng hơn.
3. **Dữ liệu thật chỉ dùng để đánh giá, không dùng để huấn luyện.** 4 năm ghi chép được phát lại theo thời gian như một người dùng mới: hệ thống đoán trước, "người dùng" sửa theo nhãn thật, rồi hệ thống học tiếp.

## Dữ liệu

| Mục | Giá trị |
|---|---|
| Nguồn | Tự ghi chép trên Notion, 09/2022 → 09/2026 (49 tháng liên tục) |
| Quy mô | 5.465 giao dịch, 1.973 nội dung khác nhau, ghi chú trung vị 2 từ |
| Nhãn | 25 danh mục tự đặt, gán tay |
| Xử lý | Đã làm sạch và ẩn danh bằng script; tên người được thay bằng mã |

## Câu hỏi nghiên cứu

| RQ | Câu hỏi |
|---|---|
| **RQ1** | Khi người dùng vừa tạo danh mục mà chưa có giao dịch nào, bộ phân loại ban đầu (LLM zero-shot, embedding, mô hình học trên dữ liệu tổng hợp) đạt đến đâu? |
| **RQ2** | Các chiến lược học từ phản hồi cải thiện được bao nhiêu so với baseline "nhớ lại", đặc biệt trên **ghi chú chưa từng gặp**? |
| **RQ3** | Dự báo khoảng chi tiêu theo tuần có đáng tin không, và **lỗi phân loại làm lệch dự báo, cảnh báo ngân sách** tới mức nào? |
| RQ4 | *(Có điều kiện)* Kết luận có lặp lại trên dữ liệu của người khác không? Cần ít nhất 3 tình nguyện viên |
| TN5 | Kết quả thay đổi thế nào khi người dùng không sửa hết các gợi ý sai? |

## Kết quả sơ bộ

| Thử nghiệm | Kết quả | Ý nghĩa |
|---|---|---|
| TF-IDF + SVM | 86,7% (chia ngẫu nhiên) → **78,2%** (chia theo thời gian) | Đánh giá ngẫu nhiên quá lạc quan; phải đánh giá theo thời gian |
| Embedding zero-shot, không học gì từ dữ liệu thật | 17,9% (chỉ tên danh mục) → **50,1%** (thêm một câu mô tả) | Mô tả danh mục giúp rất nhiều ở ngày đầu |
| Baseline "nhớ lại + zero-shot" (B1) | 71,5% tổng thể, nhưng chỉ **37,0%** trên ghi chú chưa gặp | 87% số lần phải sửa tay nằm ở ghi chú chưa gặp; đây là chỗ RQ2 phải cải thiện |

## Hệ thống

- **Kiến trúc:** React · Spring Boot · FastAPI (ML service) · PostgreSQL + pgvector · Redis · Docker Compose · GitHub Actions CI/CD.
- **Chức năng chính:** danh mục tự tạo; gợi ý danh mục khi gõ ghi chú, kèm độ tin cậy và lời giải thích; sửa nhãn và học ngay; import hàng loạt; ngân sách và cảnh báo; dashboard và dự báo chi tiêu. Đa tiền tệ là tính năng phụ.
- **Điểm kỹ thuật:** công cụ phát lại dữ liệu chạy qua **API thật** của hệ thống, nên số liệu trong luận văn là của chính hệ thống, không chỉ của notebook. Mô hình có quản lý phiên bản và giám sát tỷ lệ sửa nhãn.
- **Quy trình:** Scrum (sprint 1 tuần); unit, integration, E2E và load test; người dùng thử đánh giá bằng thang SUS.

## Kế hoạch 14 tuần

| Tuần | Giai đoạn |
|---|---|
| 1–2 | Chuẩn bị dữ liệu, khảo sát người dùng, phân tích yêu cầu, thiết kế, dựng khung dự án |
| 3–4 | Thí nghiệm RQ1, RQ2, TN5; chốt mô hình ban đầu và chiến lược thích nghi |
| 5–7 | Backend, ML service, frontend core |
| 8–10 | RQ3; ngân sách, dashboard; phát lại qua hệ thống thật; RQ4 nếu có dữ liệu |
| 11–12 | Kiểm thử, triển khai, người dùng thử |
| 13–14 | Viết luận văn, slide, dự phòng |

## Hạn chế đã biết

- Luồng đánh giá chính là dữ liệu của một người; nhãn do một người gán.
- Kết quả phụ thuộc vào LLM dùng để sinh dữ liệu tổng hợp.
- Ghi chú tự gõ khác với sao kê ngân hàng, nên kết quả không suy rộng sang bài toán phân loại sao kê.
