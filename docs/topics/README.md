# Danh sách ý tưởng đề tài

> Mỗi đề tài có một thư mục con theo slug (chữ thường, không dấu, gạch ngang), với cấu trúc `01-idea/ … 06-experiments/` như mô tả trong [CLAUDE.md](../../CLAUDE.md). Tài liệu dùng chung cho mọi đề tài (nhật ký, tài nguyên, thông tin GVHD) nằm ở [docs/common/](../common/), không lặp lại ở đây.

> **Đang khảo sát (chưa có slug):** hai hướng GVHD gợi ý là aging và cancer. Bản đang dùng: [khảo sát sâu aging và cancer](../common/deep-research/reports/aging-cancer-deep-dive.md) (02/10/2026), thay thế [bản so sánh lần 1](../common/deep-research/reports/aging-vs-cancer-topic-comparison.md). Khi chốt được một bài toán thì tạo slug và thêm dòng vào bảng dưới.

| Slug | Tên đề tài | Lĩnh vực | Trạng thái | Tài liệu |
|---|---|---|---|---|
| `rtk-atp-applicability` | Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu | Tin sinh ứng dụng, PLM + CNN đa cửa sổ, kỹ nghệ phần mềm | **Coi như đã bỏ (02/10/2026, sau buổi gặp 1)** — RTK–ATP không bị từ chối nhưng GVHD khuyên tìm hướng khác; xem [biên bản lần 1](../meeting/session-01-minutes.md). Giữ tài liệu làm tham khảo | [biên bản GVHD lần 1](../meeting/session-01-minutes.md) · [04-proposal/topic-proposal.md](rtk-atp-applicability/04-proposal/topic-proposal.md) · [01-idea/topic-decision.md](rtk-atp-applicability/01-idea/topic-decision.md) · [02-survey/key-papers.md](rtk-atp-applicability/02-survey/key-papers.md) · [03-data/data-report.md](rtk-atp-applicability/03-data/data-report.md) |
| `tme-senescence-scrnaseq` | Phát hiện tế bào lão hóa trong vi môi trường khối u từ scRNA-seq (hướng 2 GVHD gợi ý) | Tin sinh ứng dụng, scRNA-seq, học máy | **Đang khảo sát (07/10/2026), chưa chốt** — sinh viên chốt dùng scRNA-seq thay vì ảnh hình thái nhân. Chưa có tài liệu `docs/topics/<slug>/`; chỉ có code khảo sát khả thi ở `ml/tme-senescence-scrnaseq/` | [phân tích 4 hướng](../common/deep-research/reports/advisor-4-directions-analysis.md) · [ml/.../preprocessing/README.md](../../ml/tme-senescence-scrnaseq/preprocessing/README.md) |
| `personal-expense-management` | Hệ thống quản lý chi tiêu cá nhân với bộ phân loại giao dịch tự thích nghi | Ứng dụng quản lý tài chính cá nhân, NLP/phân loại văn bản ngắn | **Tạm dừng** (01/10/2026) — đã có đề cương bản nháp và thí nghiệm thô; giữ nguyên để có thể quay lại | [01-idea/brainstorm.md](personal-expense-management/01-idea/brainstorm.md) |

## Hướng đã loại khỏi phạm vi

| Hướng | Lý do loại | Tài liệu giữ làm lịch sử |
|---|---|---|
| Peptide kích thích IL-6 | Dữ liệu công khai không có test độc lập; CONTRA-IL6 (2026) đã làm kiểm tra độc lập | [bioinformatics-topic-ideas-notion.md](../meeting/bioinformatics-topic-ideas-notion.md) |
| Phân loại họ protein efflux (dự phòng) | Bỏ sau khi chốt hướng ATP ngày 02/10/2026; lớp SMR có thể quá ít chuỗi để chia fold | [bioinformatics-topic-survey.md](../common/deep-research/reports/bioinformatics-topic-survey.md) |
| Hồ sơ bằng chứng protein bằng RAG · sàng lọc dataset GEO | Hai hướng đối chiếu trong bước khảo sát theo trọng tâm hệ thống; không chọn | [bioinformatics-application-topics.md](../common/deep-research/reports/bioinformatics-application-topics.md) · [bioinformatics-application-pitch.md](../meeting/bioinformatics-application-pitch.md) |

Khi một ý tưởng đủ cụ thể để cần ghi chép riêng: tạo `docs/topics/<slug>/01-idea/`, thêm dòng vào bảng trên, và cập nhật sơ đồ cấu trúc trong CLAUDE.md nếu cần.
