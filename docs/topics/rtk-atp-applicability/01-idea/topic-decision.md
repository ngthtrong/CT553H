# Quyết định đề tài — 01/10/2026

Người thực hiện đã chốt hướng nghiên cứu và yêu cầu chuẩn bị trình bày ngày **02/10/2026**. Đây là quyết định của sinh viên; chưa ghi nhận phê duyệt của GVHD.

**Tên đề tài:** Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, sử dụng PLM–MCNN và truy hồi, được đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu.

**Tên ngắn trên slide:** Dự đoán vị trí gắn ATP ở RTK với cảnh báo miền áp dụng.

**Tên tiếng Anh:** An Applicability-Aware System for ATP-Binding Site Prediction in Receptor Tyrosine Kinases Using Protein Language Models, Multi-Window CNNs, and Retrieval under a Leakage-Controlled Evaluation Protocol.

- Nguồn lực: một người, 14 tuần; có phần nghiên cứu và sản phẩm phần mềm.
- RQ1: truy hồi cải thiện dự đoán bao nhiêu khi kiểm soát đồng dạng và giữ nguyên bộ phân loại?
- RQ2: sequence identity với dữ liệu tham chiếu có giúp xác định vùng mô hình hoạt động tốt hay không?
- Dùng ProtT5 đóng băng và MCNN; không mở rộng sang chatbot, docking, thiết kế thuốc hoặc fine-tuning nhiều PLM.
- “Kiểm soát rò rỉ” là phạm vi của giao thức downstream; không bảo đảm loại hết ảnh hưởng dữ liệu tiền huấn luyện.
- Kết quả âm vẫn có giá trị: retrieval không tốt hơn baseline, hoặc identity chưa đủ để cảnh báo, phải được báo cáo trung thực.

Tài liệu chính: [thuyết minh chi tiết](../04-proposal/topic-proposal.md), [bài báo liên quan](../02-survey/key-papers.md), [dữ liệu đã tải và kiểm tra](../03-data/data-report.md), [dàn ý trình bày](../../../meeting/2026-10-02-rtk-atp-slide-outline.md).

Bản ngoài repo: [slide 13 trang](https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT) (mã nguồn [session-01-slides/](../../../meeting/session-01-slides/)) · [trang Notion](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880). Xem [resources.md](../../../common/resources.md) để biết cách sửa lại ở phiên sau.
