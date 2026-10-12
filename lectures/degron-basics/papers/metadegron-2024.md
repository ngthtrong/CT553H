[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# MetaDegron 2024 — đối thủ trực tiếp nhất

| | |
|---|---|
| **Nơi công bố** | *Briefings in Bioinformatics*, 2024 |
| **DOI** | <https://doi.org/10.1093/bib/bbae519> |
| **Giấy phép** | mở, nhưng **chưa kiểm từng bài** → chỉ dẫn link, chưa sao chép hình |
| **Mức kiểm** | **[NGUỒN]** — đọc tóm tắt và mô tả trên trang gốc |

---

## Bài này làm gì

Dự đoán degron **theo từng E3 ligase**, cho **21 E3**. Có **máy chủ web** với cây chọn E3, hiển thị cấu trúc và mạng tương tác.

## Vì sao đây là đối thủ đáng lo nhất

Hai lý do:

1. Nó làm đúng cái trục mà đề tài **đã phải bỏ** (đặc hiệu E3) — và nó làm được cho **21 E3**, trong khi đề tài chỉ đếm được **10 E3 có nhãn, 1 E3 đủ mẫu** ([Zhang 2023](zhang-2023.md)).
2. Nó **đã có máy chủ web**, nên chiếm cùng khung ứng dụng — ảnh hưởng trực tiếp tới cổng **G3** của đề tài.

## Nhưng cách nó làm có điểm yếu rõ

| Khía cạnh | MetaDegron | Đề tài |
|---|---|---|
| **Nhãn** | ~**300 degron đã curate** từ ELM và y văn | **256.711 phép đo thực nghiệm** |
| **Nhãn âm** | **peptide ngẫu nhiên** | vị trí đo được nhưng ΔPSI thấp |
| **Chia tập** | 90/10, **không kiểm soát đồng dạng** | theo cụm protein MMseqs2, identity ≥ 30% |
| **Thước đo** | AUC 0,87–0,90 | precision@3 mức residue |
| **Đơn vị dự đoán** | peptide có phải degron không | **residue nào trong degron quan trọng** |

Ba chỗ này là điểm yếu thật:

- **Nhãn âm là peptide ngẫu nhiên.** Peptide ngẫu nhiên dễ phân biệt hơn peptide thật không phải degron rất nhiều. AUC 0,87–0,90 trên nhãn âm ngẫu nhiên **không so sánh được** với chỉ số trên nhãn âm thật.
- **Không kiểm soát đồng dạng.** Chia 90/10 ngẫu nhiên trên 300 degron thì gần như chắc chắn có rò rỉ do họ hàng. Xem [bài giảng về rò rỉ](../../09-leakage-and-homology.html).
- **Đơn vị dự đoán khác.** MetaDegron trả lời "peptide này có phải degron" — đề tài trả lời "**residue nào** trong degron quan trọng". Hai câu hỏi khác nhau, nên **không phải baseline cùng thang**.

## Kiến trúc của nó

SeqVec + BLSTM + conv-pooling, cộng XGBoost trên 10 đặc trưng.

Đáng chú ý: trong 10 đặc trưng **có** độ phơi lộ với dung môi và độ vô trật tự — nhưng ở **đầu vào**, không ở bước gộp. Đây chính là chỗ đề tài định khác: đặt cổng phơi lộ **tại bước gộp** ([bài 6](../06-proposed-solution.md)).

## Việc còn chưa làm

**Tra nội bộ MetaDegron** — nằm trong danh sách việc chưa xong của cổng chặn 3 ([topic-decision.md mục 7](../../../topics/degron-footprint/research/topic-decision.md)). Có thể còn phát hiện làm hẹp thêm tuyên bố tính mới.

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
