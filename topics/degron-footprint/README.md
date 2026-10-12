# Dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md) — hiện là **đề tài chính** theo [D-023](../../DECISIONS.md#d-023). Cập nhật lần cuối: **12/10/2026**. Slug cũ là `degron-e3-specificity`; trục "đặc hiệu E3" đã bỏ từ 11/10/2026.

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
| G2 đóng góp dương | **Chưa xác lập** (chưa huấn luyện mô hình nào), nhưng **khoảng trống đã được chứng minh** — mạnh nhất repo. 2.353/2.624 peptide (**89,7%**) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần **bị chứng minh không tách được**. Cận trên chính xác của lớp đó: precision@3 **0,6045**; oracle không ràng buộc **0,7792**; ngẫu nhiên 0,1204. Mục tiêu định lượng: vượt 0,6045 (**+28,9% tương đối** nếu đạt trần) | [composition-context-audit.md](research/composition-context-audit.md) |
| G3 ứng dụng | **Yếu nhất trong các ứng viên.** Đã có **ba** sản phẩm: DEGRONOPEDIA (*NAR* 2024), máy chủ web MetaDegron, Colab của nhóm PAP — nên ứng dụng phải **khác biệt được**, không chỉ tồn tại. Chỗ khác biệt khả thi: ma trận 28×20 (vị trí × amino acid thay vào) trên nhãn đột biến thực nghiệm, thứ cả ba sản phẩm kia không xuất ra | [topic-decision.md §7](research/topic-decision.md) |

## Rủi ro chính
- **Lực thống kê — rủi ro số một.** Chia test theo cụm protein chỉ còn **221–322 footprint** (cov50: 221–301; cov80: 271–322). Chưa biết n này có đủ để phát hiện một cải thiện precision@3 so với mốc 0,6045 hay không, khi chỉ số là trung bình macro theo peptide.
- **Nhiễu đo chưa tách khỏi tín hiệu ngữ cảnh.** Dữ liệu một replicate, reads tối thiểu thấp, genotype BAG6 của replicate chưa rõ. Một phần của 35,0% phương sai dư có thể là nhiễu, không phải ngữ cảnh học được.
- Kiến trúc MIL/cổng cấu trúc trong các trang cũ **chưa được kiểm chứng**. Đã có tiền lệ: BioBlobs (attention-MIL trên protein, 10/2025), OmniESI (điều biến có điều kiện hai chiều), MetaDegron (21 E3). Phát biểu đúng mức: **mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, không mới ở cơ chế**.
- Larsen 2025 đã tính rASA/pLDDT từ AlphaFold2 và đã làm bản đồ ΔPAP *in silico*, nên **"dùng cấu trúc" và "giải thích biến thể" không còn là phần mới**.
- Quy ước ngôn từ: không nói "16 E3 có nhãn CRISPR"; không nói "chưa ai làm đặc hiệu E3"; không nói "chưa ai làm ma trận thay thế cho degron"; không hứa cải thiện 0,1747 như điều chắc chắn.

## Việc tiếp theo
1. **Tính lực thống kê** trên tập test 221–322 footprint, **trước khi cam kết huấn luyện**. Dữ liệu đã có trên máy, không cần tải thêm. Đây là phép kiểm quyết định đề tài đứng hay sụp ở G2.
2. Đặt **baseline thành phần** làm mốc G2 (mốc đã biết: cận 0,6045).
3. Thử hướng ma trận thay thế theo mục 6 của audit, sau khi sửa phép phân rã; chạy thang ablation `B → B + hạng 1 → B + hạng r` với cùng split và ngân sách.
4. Kiểm lặp lại, độ sâu reads và tính ổn định để tách phần ngữ cảnh học được khỏi nhiễu đo.
5. Thiết kế ứng dụng đủ khác ba sản phẩm đã có (xem dòng G3).

## Trong thư mục này
- [log.md](log.md) — nhật ký nghiên cứu (11–12/10/2026).
- research/: [topic-decision.md](research/topic-decision.md) (phạm vi 11/10, có phần lịch sử) · [composition-context-audit.md](research/composition-context-audit.md) · [e3-labels-audit/](research/e3-labels-audit/README.md) · [voutsinos-2026-audit/](research/voutsinos-2026-audit/README.md) · [topic-report/index.html](research/topic-report/index.html)
- presentation/: [presentation.html](presentation/presentation.html) · [presentation-validation.md](presentation/presentation-validation.md) · [session-02-prep.md](presentation/session-02-prep.md) (bản 11/10, đã lạc hậu)
- Hub học của đề tài: [lectures/degron-footprint/](../../lectures/degron-footprint/index.html)
