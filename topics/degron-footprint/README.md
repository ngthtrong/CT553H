# Dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026**. Slug cũ là `degron-e3-specificity`; trục "đặc hiệu E3" đã bỏ từ 11/10/2026.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, protein, học máy (dạng dự đoán mức residue) |
| Dữ liệu | Quét đột biến Zhang 2023 (256.711 phép đo, 2.624 peptide có footprint) + bản đồ thay thế đầy đủ (135.040 phép đo trên 249 bản đồ); Voutsinos 2026 → `topics/degron-footprint/data/` |
| Giai đoạn | Đã tải dữ liệu, audit nhãn, thành phần amino acid và cụm protein; chưa huấn luyện |

## Bài toán
Degron là đoạn trình tự khiến protein bị đánh dấu để phân hủy. Câu hỏi: **residue nào trong degron quyết định độ bền**, và đột biến ở đó làm độ bền thay đổi bao nhiêu? Đầu vào là peptide/protein (kèm cấu trúc nếu có). Đầu ra là điểm quan trọng theo residue và dự đoán hiệu ứng đột biến (ΔPSI).

## Cổng G1/G2/G3
| Cổng | Trạng thái | Bằng chứng |
|---|---|---|
| G1 nhãn độc lập | **Đạt, mạnh nhất repo** — toàn bộ là nhãn thực nghiệm | [e3-labels-audit/](research/e3-labels-audit/README.md) |
| G2 đóng góp dương | **Chưa xác lập.** Mô hình chỉ dùng thành phần amino acid đã đạt precision@3 tới 0,6045; trần không ràng buộc là 0,7792, nên dư địa chỉ 0,1747 | [composition-context-audit.md](research/composition-context-audit.md) |
| G3 ứng dụng | **Yếu nhất trong các ứng viên** | [topic-decision.md §7](research/topic-decision.md) |

## Rủi ro chính
- Khi chia test theo cụm protein (identity 30%, coverage 50%), chỉ còn **221–301 footprint**, tập test nhỏ.
- Kiến trúc MIL/cổng cấu trúc trong các trang cũ **chưa được kiểm chứng**. Đã có tiền lệ: BioBlobs (MIL trên protein), MetaDegron (21 E3).
- Quy ước ngôn từ: không nói "16 E3 có nhãn CRISPR"; không nói "chưa ai làm đặc hiệu E3".

## Việc tiếp theo
- Nếu được kích hoạt: thử hướng ma trận thay thế (mục 6 của audit), sau khi sửa phép phân rã; đặt baseline thành phần làm mốc G2.

## Trong thư mục này
- [log.md](log.md) — nhật ký nghiên cứu (11–12/10/2026).
- research/: [topic-decision.md](research/topic-decision.md) (phạm vi 11/10, có phần lịch sử) · [composition-context-audit.md](research/composition-context-audit.md) · [e3-labels-audit/](research/e3-labels-audit/README.md) · [voutsinos-2026-audit/](research/voutsinos-2026-audit/README.md) · [topic-report/index.html](research/topic-report/index.html)
- presentation/: [presentation.html](presentation/presentation.html) · [presentation-validation.md](presentation/presentation-validation.md) · [session-02-prep.md](presentation/session-02-prep.md) (bản 11/10, đã lạc hậu)
- Hub học của đề tài: [lectures/degron-footprint/](../../lectures/degron-footprint/index.html)
