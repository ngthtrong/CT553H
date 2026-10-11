# Danh sách ý tưởng đề tài

> Mỗi đề tài có một thư mục con theo slug (chữ thường, không dấu, gạch ngang), với cấu trúc `01-idea/ … 06-experiments/` như mô tả trong [CLAUDE.md](../../CLAUDE.md). Tài liệu dùng chung cho mọi đề tài (nhật ký, tài nguyên, thông tin GVHD) nằm ở [docs/common/](../common/), không lặp lại ở đây.

> **Đang khảo sát (chưa có slug):** hai hướng GVHD gợi ý là aging và cancer. Bản đang dùng: [khảo sát sâu aging và cancer](../common/deep-research/reports/aging-cancer-deep-dive.md) (02/10/2026), thay thế [bản so sánh lần 1](../common/deep-research/reports/aging-vs-cancer-topic-comparison.md). Khi chốt được một bài toán thì tạo slug và thêm dòng vào bảng dưới.

> **Khuyến nghị đề tài chính (10/10/2026, chưa có slug, chưa trình GVHD): dark kinome trên DARKIN.** Bản đang dùng để quyết định: **[chốt đề tài chính](../common/deep-research/reports/main-topic-decision.md)** — tiêu chí và trọng số, bảng so sánh bốn ứng viên, **bốn lập luận bán đề tài phải gỡ bỏ**, lộ trình 8–9 tuần và **sáu phép kiểm trước khi chốt**. Nền kỹ thuật: [đánh giá chi tiết DARKIN](../common/deep-research/reports/dark-kinome-darkin-evaluation.md) (audit dữ liệu, tiền lệ, năm tiêu chí, protocol/XAI/conformal/website). Hai điều kiện bắt buộc dẫn tới khuyến nghị này đến từ câu trả lời của sinh viên ngày 10/10/2026 (kết quả âm không được chấp nhận; có GPU) — **chưa phải lời GVHD**.

> ## ✅ ĐỀ TÀI ĐÃ CHỐT (11/10/2026), TÁI ĐỊNH TÂM CÙNG NGÀY: `degron-e3-specificity`
>
> **Dự đoán footprint degron ở mức residue bằng học đa thể hiện với cổng phơi lộ cấu trúc, trên nhãn đột biến thực nghiệm.** Slug giữ nguyên để không vỡ liên kết, nhưng **trục đã đổi**. Quyết định của sinh viên; **chưa có phê duyệt GVHD**, cần báo cáo buổi tuần 6. Xem [hub học đề tài](degron-e3-specificity/learn/index.html) · [quyết định và phạm vi](degron-e3-specificity/01-idea/topic-decision.md) · [trang trình bày](degron-e3-specificity/01-idea/presentation.html) · [chuẩn bị buổi tuần 6](../meeting/session-02-prep.md).
>
> **Ba cổng chặn đã đóng hết (11/10/2026 khuya).** Cổng 1 qua: đọc toàn văn bài degron transcription factor — họ không làm đặc hiệu E3, không kiến trúc mới, không XAI. Cổng 3 có câu trả lời và **thu hẹp tuyên bố tính mới**: BioBlobs (10/2025) đã dùng MIL có cổng attention trên protein, OmniESI (2025) đã dùng điều biến có điều kiện → "mới ở chỗ ghép, không mới ở cơ chế". **Cổng 2 KHÔNG QUA và buộc đổi trục.**
>
> **Phép đếm nhãn E3 từ dữ liệu thô** ([7 script tái tạo](../common/deep-research/research_notes/degron-e3-labels/README.md)): 31 screen CRISPR → 27 gán được → **10 E3** → **chỉ 1 E3 (KLHL15, 13 peptide) có ≥5 peptide**, 6 E3 có đúng 1 peptide. Bền với 36 tổ hợp ngưỡng. → **bỏ thành phần điều kiện E3**, bỏ "đặc hiệu E3" khỏi vị trí thước đo chính.
>
> **Phần bù, lớn hơn tài liệu trước ghi nhiều:** nhãn theo residue có **256.711 phép đo** đột biến quét, **2.624 peptide có footprint học được** (2.402 khu trú), **median 3 vị trí quan trọng trên 28**, cộng **135.040 phép đo** trên 249 bản đồ thay thế đầy đủ. Đây là nguồn nhãn và thước đo chính của đề tài.
>
> **Quy ước ngôn từ:** không nói "16 E3 có nhãn CRISPR" — nói **số peptide trên mỗi E3** (1–13). Không gọi phần E3 là nhiệm vụ dự đoán, gọi là **ca nghiên cứu** trên 27 peptide. Không nói "chưa ai làm đặc hiệu E3" (MetaDegron đã làm cho 21 E3). Phải tự nói ra rằng khi có nhãn mức residue thì MIL không còn bắt buộc.

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
