# Lưu trữ — KHÔNG dùng để ra quyết định

> Mọi thứ trong `archive/` là **lịch sử**: đề tài đã đóng, khảo sát đã bị thay, bản nháp cũ. Câu "chốt / quyết định / khuyến nghị" ở đây **không còn hiệu lực**. Trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../DECISIONS.md). Giữ lại để tra cứu bằng chứng, số liệu đã đo và lý do loại, tránh khảo sát lại từ đầu.

## Đề tài đã đóng (`topics/`)

| Thư mục | Đề tài | Lý do đóng | Quyết định |
|---|---|---|---|
| [budgeted-microservice-rca/](topics/budgeted-microservice-rca/) | Lựa chọn bằng chứng RCA theo ngân sách truy vấn | Xem [D-021](../DECISIONS.md#d-021) | [D-021](../DECISIONS.md#d-021) |
| [plm-calibration-audit/](topics/plm-calibration-audit/) | A4 — audit calibration và miền áp dụng của PLM (từng là dự phòng) | Trọng chỉ giữ `degron-footprint`, xem [D-024](../DECISIONS.md#d-024) | [D-024](../DECISIONS.md#d-024) |
| [xai-fidelity-benchmark/](topics/xai-fidelity-benchmark/) | A2 — benchmark fidelity XAI | Như trên | [D-024](../DECISIONS.md#d-024) |
| [structure-sequence-leakage-audit/](topics/structure-sequence-leakage-audit/) | A3 — audit rò rỉ cấu trúc–trình tự | Như trên | [D-024](../DECISIONS.md#d-024) |
| [dark-kinome-zero-shot/](topics/dark-kinome-zero-shot/) | Dark kinome zero-shot trên DARKIN | Như trên (G2 yếu nhất, trụ tính mới đã sụp) | [D-024](../DECISIONS.md#d-024) |
| [budgeted-plm-variant-scoring/](topics/budgeted-plm-variant-scoring/) | Tối ưu chi phí chấm điểm biến thể protein bằng PLM | Như trên | [D-024](../DECISIONS.md#d-024) |
| [scalable-metagenomic-binning/](topics/scalable-metagenomic-binning/) | Tối ưu đồ thị cho binning metagenomics | Như trên | [D-024](../DECISIONS.md#d-024) |
| [rtk-atp-applicability/](topics/rtk-atp-applicability/) | Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng | GVHD khuyên đổi đề tài sau buổi gặp 1. Ý tưởng miền áp dụng sống lại ở [plm-calibration-audit](topics/plm-calibration-audit/README.md) | D-006 |
| [tme-senescence-scrnaseq/](topics/tme-senescence-scrnaseq/) | Tế bào lão hóa trong vi môi trường khối u từ scRNA-seq | Nhãn SenMayo do chính pipeline sinh ra | D-008 |
| [sirtuin-substrate/](topics/sirtuin-substrate/) | Cơ chất deacetyl hóa theo isoform SIRT1–7 | Nhãn in vitro gần như không chuyển được vào tế bào; đóng góp còn lại là kết quả âm | D-011 |
| [legal-qa-grounding/](topics/legal-qa-grounding/) | Hỏi–đáp pháp luật tiếng Việt có kiểm chứng trích dẫn | Không liên quan tin sinh học | D-019 |
| *(không còn file)* `personal-expense-management` | Quản lý chi tiêu cá nhân | Không liên quan tin sinh học; tài liệu đã gỡ khỏi repo từ trước, chỉ còn trong lịch sử git và [journal/2026-09.md](../journal/2026-09.md) | D-002, D-019 |

Mỗi thư mục đề tài có `log.md` (nhật ký tách từ nhật ký chung cũ), nếu có.

## Khảo sát cũ (`surveys/`)

| Tài liệu | Ngày | Ghi chú |
|---|---|---|
| [bioinformatics-topic-survey/](surveys/bioinformatics-topic-survey/bioinformatics-topic-survey.md) | 01/10 | Khoảng trống đánh giá trong nhóm GVHD; có kiểm chứng RAG-msCNN |
| [bioinformatics-application-topics.md](surveys/bioinformatics-application-topics.md) | 01/10 | Hướng ứng dụng/hệ thống; hai hướng không chọn |
| [rag-mcnn-topic-ideas/](surveys/rag-mcnn-topic-ideas/rag-mcnn-topic-ideas.md) | 01–02/10 | Không gian thiết kế RAG trong nhóm GVHD |
| [aging-cancer/](surveys/aging-cancer/aging-cancer-deep-dive.md) | 02/10 | Khảo sát aging và cancer (kèm bản so sánh lần 1) |
| [advisor-4-directions-analysis.md](surveys/advisor-4-directions-analysis.md) | 06/10 | 4 hướng giao thoa cancer–aging do GVHD gợi ý |
| [compute-novelty-directions.md](surveys/compute-novelty-directions.md) · [b-method-layer-draft.md](surveys/b-method-layer-draft.md) | 08/10 | Hướng tính mới ở phần tin học; bản phác B + nén mô hình + conformal |
| [topic-final-recommendation.md](surveys/topic-final-recommendation.md) | 08/10 | Khuyến nghị sirtuin làm chính (D-009, đã bị thay) |
| [criteria-only-recommendation.md](surveys/criteria-only-recommendation.md) | 10/10 | Khuyến nghị nếu chỉ xét năm tiêu chí (đã bị thay) |

## Biên bản/nháp cũ (`meetings/`)

Bản nguồn Notion và pitch trước buổi gặp 1: [bioinformatics-topic-ideas-notion.md](meetings/bioinformatics-topic-ideas-notion.md), [bioinformatics-proposal-notion.md](meetings/bioinformatics-proposal-notion.md), [bioinformatics-application-pitch.md](meetings/bioinformatics-application-pitch.md).
