# Benchmark độ trung thực (fidelity) của XAI trên mô hình protein/điều hòa gen — ứng viên A2

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026**.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, tầng công cụ/benchmark, XAI |
| Dữ liệu | Dùng lại nhãn độc lập sẵn có: vị trí gắn ligand (PDB, UniProt "binding site"), motif điều hòa (JASPAR, ChIP-seq). Chưa tải |
| Giai đoạn | Mới khảo sát qua tóm tắt tìm kiếm; **chưa đọc toàn văn nguồn nào** |

## Bài toán
Các bài báo (kể cả BERT-Promoter của GVHD, dùng SHAP) coi điểm quan trọng do SHAP/attention/IG sinh ra là "giải thích sinh học", nhưng hầu như không kiểm. Đề tài đo xem **các vị trí được chấm điểm cao có trùng với vị trí đã biết từ cấu trúc/thực nghiệm độc lập hay không**.

- **Đầu vào:** mô hình đã huấn luyện (ví dụ mCNN+PLM cho ATP-binding, bộ phân loại promoter), phương pháp attribution, ground truth độc lập.
- **Đầu ra:** điểm fidelity cho từng cặp (mô hình, attribution), ví dụ AUPRC hay precision@k so với vị trí thật; độ nhất quán giữa các phương pháp; báo cáo phương pháp nào đáng tin.

## Cổng G1/G2/G3
| Cổng | Trạng thái | Ghi chú |
|---|---|---|
| G1 nhãn độc lập | Khả quan — ground truth cấu trúc/motif độc lập với mô hình | Chưa audit dữ liệu cụ thể |
| G2 đóng góp dương | **Chưa rõ.** Kết quả có thể "âm" (SHAP không đáng tin trên mô hình của GVHD) | Rủi ro: GVHD không nhận kết quả âm làm đóng góp chính |
| G3 ứng dụng | Khả thi: công cụ/thư viện đánh giá XAI | Chưa thiết kế |

## Rủi ro chính
- Có hai công trình liền kề cần đọc kỹ trước khi tin là còn trống: **TPCAV** (concept attribution cho genomics) và **benchmark bioRxiv 01/2025** về mô hình sequence-function diễn giải được.
- Dạng benchmark/audit có thể không đáp ứng kỳ vọng "kiến trúc mới" của GVHD ([C-3](../../DECISIONS.md)).

## Việc tiếp theo
1. Đọc toàn văn TPCAV, benchmark 01/2025 và position paper ICML 2026.
2. Chọn 1 mô hình + 1 bộ ground truth cụ thể, tự tải và audit.

## Trong thư mục này
- [log.md](log.md) · [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md)
- Nguồn danh mục: [surveys/bioinformatics-tool-layer-candidates-2026-10-12.md](../../surveys/bioinformatics-tool-layer-candidates-2026-10-12.md) (mục A2)
