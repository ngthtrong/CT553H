# Nhật ký làm việc

> Mỗi phiên làm việc có thay đổi đáng kể thì thêm **một mục lên đầu** (mới nhất ở trên). Ghi ngắn: đã làm gì, quyết định gì, còn dở gì. Chi tiết nằm trong các tài liệu được liên kết, không chép lại ở đây. Đầu phiên mới, đọc mục mới nhất để nắm tình hình.

---

## 29/09/2026

**Đã làm**
- Báo cáo trạng thái brainstorm; phản biện 7 điểm thiếu sót của đề tài.
- Bổ sung dòng mẫu ẩn danh và câu hỏi cho GVHD trong [buoi-01-chuan-bi.md](../meeting/buoi-01-chuan-bi.md). Làm slide 8 trang ([tai-nguyen.md](tai-nguyen.md)).
- Thí nghiệm thô [rq1-kiem-tra-nhanh](../../ml/quan-ly-chi-tieu-ca-nhan/experiments/rq1-kiem-tra-nhanh/README.md): embedding zero-shot trên dev đạt 50,1% với tên + mô tả, 17,9% nếu chỉ có tên.
- Thí nghiệm thô [rq2-baseline-nho-lai](../../ml/quan-ly-chi-tieu-ca-nhan/experiments/rq2-baseline-nho-lai/README.md): B1 đạt 71,5%, riêng ghi chú chưa gặp chỉ 37,0%; bản thô của TN5.
- Khảo sát tài liệu, đối chiếu 18 khẳng định với bằng chứng: [khao-sat-tai-lieu.md](../de-tai/quan-ly-chi-tieu-ca-nhan/02-khao-sat/khao-sat-tai-lieu.md).
- Đề cương bản nháp 1 bằng LaTeX: [de-cuong.tex](../de-tai/quan-ly-chi-tieu-ca-nhan/04-de-cuong/de-cuong.tex).
- Tạo cơ chế lưu thông tin giữa các phiên: file này và [tai-nguyen.md](tai-nguyen.md).

**Quyết định** (chi tiết ở [brainstorm.md](../de-tai/quan-ly-chi-tieu-ca-nhan/01-y-tuong/brainstorm.md), mục 0.2)
- B0/B1 (nhớ lại) là mốc bắt buộc. RQ2 đo mức cải thiện so với B1 trên ghi chú chưa gặp.
- RQ3 mở rộng thành dự báo khoảng và lan truyền lỗi phân loại (phương án 1 + 3).
- Thêm biến thể đặc trưng ngữ cảnh (+ctx). Chốt TN5 về phản hồi thiếu.
- Tìm tình nguyện viên sau buổi gặp GVHD, nếu đề tài được chốt.

**Còn dở**
- Người làm đề tài tự viết lại mô tả 25 danh mục. Bản hiện tại là nháp của Claude, có nguy cơ rò rỉ.
- Điền thông tin cá nhân và kiểm tra tên đơn vị trên trang bìa đề cương.
- Tìm lại tài liệu trên Google Scholar; tự đọc toàn văn các bài chính; đối chiếu `refs.bib`.
- Soạn và phát khảo sát người dùng.
- Buổi gặp GVHD lần 1: chưa diễn ra. Sau buổi gặp: viết `buoi-01-bien-ban.md`.

## 27/09/2026
- Đổi trọng tâm: dữ liệu cá nhân chỉ dùng để đánh giá bằng phát lại; mô hình ban đầu dùng LLM zero-shot và dữ liệu tổng hợp; đa tiền tệ hạ xuống tính năng phụ. Làm bản tóm tắt 2 trang ([tom-tat-de-tai.pdf](../de-tai/quan-ly-chi-tieu-ca-nhan/01-y-tuong/tom-tat-de-tai.pdf)).

## 24/09/2026
- Khởi tạo repo; báo cáo dữ liệu ([bao-cao-du-lieu.md](../de-tai/quan-ly-chi-tieu-ca-nhan/03-du-lieu/bao-cao-du-lieu.md)) và script làm sạch, ẩn danh.
