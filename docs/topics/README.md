# Danh sách ý tưởng đề tài

> Mỗi đề tài có một thư mục con theo slug (chữ thường, không dấu, gạch ngang), với cấu trúc `01-idea/ … 06-experiments/` như mô tả trong [CLAUDE.md](../../CLAUDE.md). Tài liệu dùng chung cho mọi đề tài (nhật ký, tài nguyên, thông tin GVHD) nằm ở [docs/common/](../common/), không lặp lại ở đây.

> **Đang khảo sát (chưa có slug):** hai hướng GVHD gợi ý là aging và cancer. Bản đang dùng: [khảo sát sâu aging và cancer](../common/deep-research/reports/aging-cancer-deep-dive.md) (02/10/2026), thay thế [bản so sánh lần 1](../common/deep-research/reports/aging-vs-cancer-topic-comparison.md). Khi chốt được một bài toán thì tạo slug và thêm dòng vào bảng dưới.

> **Khuyến nghị đề tài chính (10/10/2026, chưa có slug, chưa trình GVHD): dark kinome trên DARKIN.** Bản đang dùng để quyết định: **[chốt đề tài chính](../common/deep-research/reports/main-topic-decision.md)** — tiêu chí và trọng số, bảng so sánh bốn ứng viên, **bốn lập luận bán đề tài phải gỡ bỏ**, lộ trình 8–9 tuần và **sáu phép kiểm trước khi chốt**. Nền kỹ thuật: [đánh giá chi tiết DARKIN](../common/deep-research/reports/dark-kinome-darkin-evaluation.md) (audit dữ liệu, tiền lệ, năm tiêu chí, protocol/XAI/conformal/website). Hai điều kiện bắt buộc dẫn tới khuyến nghị này đến từ câu trả lời của sinh viên ngày 10/10/2026 (kết quả âm không được chấp nhận; có GPU) — **chưa phải lời GVHD**.

> ## ✅ ĐỀ TÀI ĐÃ CHỐT (11/10/2026): `degron-e3-specificity`
>
> **Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc.** Quyết định của sinh viên ngày 11/10/2026; **chưa có phê duyệt GVHD**, cần báo cáo buổi tuần 6. Xem [quyết định và phạm vi](degron-e3-specificity/01-idea/topic-decision.md) · [trang trình bày](degron-e3-specificity/01-idea/presentation.html) · [báo cáo kiểm chứng chi tiết](../common/deep-research/reports/degron-topic-report/index.html).
>
> **GVHD kỳ vọng một kiến trúc chưa ai dùng** (thông tin 11/10/2026) → kiến trúc đề xuất **CMIL-E3**, sáu thành phần, mỗi thành phần gắn với một phép đo tự thực hiện.
>
> **Ba cổng chặn chưa qua:** (1) đọc toàn văn bài degron transcription factor của cùng nhóm; (2) đếm nhãn E3 dùng được trong Table S3/S4/S6/S7 của Zhang 2023; (3) tra hệ thống tính mới của kiến trúc. Chi tiết ở mục 7 của [topic-decision.md](degron-e3-specificity/01-idea/topic-decision.md).

| Slug | Tên đề tài | Lĩnh vực | Trạng thái | Tài liệu |
|---|---|---|---|---|
| `rtk-atp-applicability` | Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu | Tin sinh ứng dụng, PLM + CNN đa cửa sổ, kỹ nghệ phần mềm | **Coi như đã bỏ (02/10/2026, sau buổi gặp 1)** — RTK–ATP không bị từ chối nhưng GVHD khuyên tìm hướng khác; xem [biên bản lần 1](../meeting/session-01-minutes.md). Giữ tài liệu làm tham khảo | [biên bản GVHD lần 1](../meeting/session-01-minutes.md) · [04-proposal/topic-proposal.md](rtk-atp-applicability/04-proposal/topic-proposal.md) · [01-idea/topic-decision.md](rtk-atp-applicability/01-idea/topic-decision.md) · [02-survey/key-papers.md](rtk-atp-applicability/02-survey/key-papers.md) · [03-data/data-report.md](rtk-atp-applicability/03-data/data-report.md) |
| `tme-senescence-scrnaseq` | Phát hiện tế bào lão hóa trong vi môi trường khối u từ scRNA-seq (hướng 2 GVHD gợi ý) | Tin sinh ứng dụng, scRNA-seq, học máy | **Không chọn làm đề tài chính (10/10/2026)** — trượt điều kiện bắt buộc về nhãn: điểm SenMayo là điểm chữ ký do chính pipeline sinh ra, nên mô hình có giám sát **học lại bộ chấm điểm** (xem [README của hướng](../../ml/tme-senescence-scrnaseq/preprocessing/README.md), dòng 97). Cộng với trượt ngưỡng đi/dừng đã đặt trước (7 so với ≥ 8 bệnh nhân) và điểm đi theo loại tế bào (70% tế bào dương là fibroblast). Giữ lại như bài toán **không giám sát** hoặc phân tích giới hạn của chữ ký | [chốt đề tài](../common/deep-research/reports/main-topic-decision.md) (mục 3.1) · [phân tích 4 hướng](../common/deep-research/reports/advisor-4-directions-analysis.md) · [ml/.../preprocessing/README.md](../../ml/tme-senescence-scrnaseq/preprocessing/README.md) |
| `personal-expense-management` | Hệ thống quản lý chi tiêu cá nhân với bộ phân loại giao dịch tự thích nghi | Ứng dụng quản lý tài chính cá nhân, NLP/phân loại văn bản ngắn | **Tạm dừng** (01/10/2026) — đã có đề cương bản nháp và thí nghiệm thô; giữ nguyên để có thể quay lại | [01-idea/brainstorm.md](personal-expense-management/01-idea/brainstorm.md) |

## Hướng đã loại khỏi phạm vi

| Hướng | Lý do loại | Tài liệu giữ làm lịch sử |
|---|---|---|
| Sửa lỗi phần mềm có kiểm chứng | Sinh viên yêu cầu loại ngày 10/10/2026; không tiếp tục khảo sát | Quyết định trong [nhật ký](../common/work-log.md) |
| Peptide kích thích IL-6 | Dữ liệu công khai không có test độc lập; CONTRA-IL6 (2026) đã làm kiểm tra độc lập | [bioinformatics-topic-ideas-notion.md](../meeting/bioinformatics-topic-ideas-notion.md) |
| Phân loại họ protein efflux (dự phòng) | Bỏ sau khi chốt hướng ATP ngày 02/10/2026; lớp SMR có thể quá ít chuỗi để chia fold | [bioinformatics-topic-survey.md](../common/deep-research/reports/bioinformatics-topic-survey.md) |
| Hồ sơ bằng chứng protein bằng RAG · sàng lọc dataset GEO | Hai hướng đối chiếu trong bước khảo sát theo trọng tâm hệ thống; không chọn | [bioinformatics-application-topics.md](../common/deep-research/reports/bioinformatics-application-topics.md) · [bioinformatics-application-pitch.md](../meeting/bioinformatics-application-pitch.md) |

Khi một ý tưởng đủ cụ thể để cần ghi chép riêng: tạo `docs/topics/<slug>/01-idea/`, thêm dòng vào bảng trên, và cập nhật sơ đồ cấu trúc trong CLAUDE.md nếu cần.
