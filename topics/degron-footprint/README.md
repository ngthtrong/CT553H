# Dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md) — hiện là **đề tài chính** theo [D-023](../../DECISIONS.md#d-023). Cập nhật lần cuối: **13/10/2026**. Slug cũ là `degron-e3-specificity`; trục "đặc hiệu E3" đã bỏ từ 11/10/2026.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, protein, học máy (dạng dự đoán mức residue) |
| Dữ liệu | **Đã tải đủ bốn nguồn** (13/10): Zhang 2023 Mendeley cả 5/5 file, GEO GSE240610, repo Voutsinos 2026, 26 score set MaveDB → `topics/degron-footprint/data/`. PSI đã dựng từ read thô cho **mọi** điều kiện: quét rep1/rep2/BAG6 WT, bão hòa hai nửa. Xem [audit đầy đủ](research/full-data-audit/README.md) |
| Giai đoạn | Đã tải đủ, audit nhãn, **đo trần nhãn và lực thống kê**; chưa huấn luyện |

## Bài toán
Degron là đoạn trình tự khiến protein bị đánh dấu để phân hủy. Câu hỏi: **residue nào trong degron quyết định độ bền**, và đột biến ở đó làm độ bền thay đổi bao nhiêu? Đầu vào là peptide/protein (kèm cấu trúc nếu có). Đầu ra là điểm quan trọng theo residue và dự đoán hiệu ứng đột biến (ΔPSI).

## Cổng G1/G2/G3
| Cổng | Trạng thái | Bằng chứng |
|---|---|---|
| G1 nhãn độc lập | **Đạt, mạnh nhất repo** — toàn bộ là nhãn thực nghiệm | [e3-labels-audit/](research/e3-labels-audit/README.md) |
| G2 đóng góp dương | **Chưa xác lập** (chưa huấn luyện mô hình nào), nhưng **khoảng trống đã được chứng minh và nay đã định lượng đúng mốc**. 2.353/2.624 peptide (**89,7%**) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần **bị chứng minh không tách được**. Mốc đúng để so: baseline thành phần **ước lượng trung thực 0,4897**; **trần nhãn thực nghiệm 0,6514** (một replicate chấm trên nhãn replicate kia); ngẫu nhiên 0,1204. Dư địa thật **0,1617**. **Lưu ý:** 0,6045 và 0,7792 là **oracle đọc nhãn test**, không mô hình nào đạt — cách đọc "dư địa 0,1747 / +28,9%" trước đây **không còn dùng** | [full-data-audit §4](research/full-data-audit/README.md) · [composition-context-audit.md](research/composition-context-audit.md) |
| G3 ứng dụng | **Yếu nhất trong các ứng viên.** Đã có **bốn** tiền lệ: DEGRONOPEDIA (*NAR* 2024), máy chủ web MetaDegron, Colab của nhóm PAP, và **mô hình học máy của chính nhóm Zhang 2023** dự đoán PSI toàn peptidome (Pearson 0,8955, RMSE 0,563 trên 260.989 peptide) — cái cuối mới phát hiện 13/10, **khác phạm vi** (peptide, không phải residue) nên không phải đối thủ trực tiếp, nhưng phải nêu. Chỗ khác biệt khả thi: ma trận 28×20 (vị trí × amino acid thay vào) trên nhãn đột biến thực nghiệm, thứ cả bốn không xuất ra; nay đã xác nhận ma trận này **phủ 97,9% trên 235 peptide** từ bộ bão hòa | [full-data-audit §6–7](research/full-data-audit/README.md) · [topic-decision.md §7](research/topic-decision.md) |

## Rủi ro chính
- ~~**Lực thống kê — rủi ro số một.**~~ **Đã giải quyết 13/10: tập test đủ lực.** Kiểm ghép cặp với SD đo thật 0,2416: so baseline thành phần trung thực cần **18** peptide (lực ≈1,00); so mốc 0,6045 cần **209**, cho lực **0,82–0,94** ở n = 221–322. Hệ quả: **dùng split cov80** (271–322, lực 0,92–0,94), không dùng cov50 (n=221 chỉ cho lực 0,82). Khi có mô hình thật phải tính lại lực bằng SD của chính cặp đó. [Chi tiết](research/full-data-audit/README.md)
- **Nhãn mức residue chỉ lặp lại khoảng một nửa — nay là rủi ro số một.** Peptide *có* footprint lặp lại tốt (89,3%), nhưng *residue nào* là footprint chỉ trùng ở mức Jaccard **0,4965**, và chỉ 16,0% peptide có tập vị trí dương giống hệt nhau giữa hai replicate. Đề tài dự đoán đúng ở mức residue này.
- ~~**Nhiễu đo chưa tách khỏi tín hiệu ngữ cảnh.**~~ **Đã tách 13/10.** Dư sau oracle thành phần là 0,3612, trong đó **75,9% là nhiễu đo**; ngữ cảnh học được cận trên chỉ **0,0872** phương sai, **không phải 35,0%**. Nhiễu **không** phải tạo tác của ngưỡng reads (giữ 0,72–0,77 từ reads≥10 đến ≥200) và được xác nhận bốn lần độc lập (~0,24–0,34) ⇒ tính chất của assay GPS.
- **Bộ bão hòa tốt hơn nhưng nhỏ.** Nhiễu chỉ 16,7%, Jaccard ô dương 0,6596, ma trận phủ 97,9% — nhưng chỉ **235 peptide**, nên nếu chuyển trọng tâm sang nguồn này thì **phải tính lại lực cho thiết kế mới trước khi cam kết**. Bộ này không có phép đo hoang dã; phải dùng ô đồng nghĩa làm WT nội tại. **130/248** peptide trùng với bộ quét nên phải cùng phía train/test.
- Kiến trúc MIL/cổng cấu trúc trong các trang cũ **chưa được kiểm chứng**. Đã có tiền lệ: BioBlobs (attention-MIL trên protein, 10/2025), OmniESI (điều biến có điều kiện hai chiều), MetaDegron (21 E3). Phát biểu đúng mức: **mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, không mới ở cơ chế**.
- Larsen 2025 đã tính rASA/pLDDT từ AlphaFold2 và đã làm bản đồ ΔPAP *in silico*, nên **"dùng cấu trúc" và "giải thích biến thể" không còn là phần mới**.
- Quy ước ngôn từ: không nói "16 E3 có nhãn CRISPR"; không nói "chưa ai làm đặc hiệu E3"; không nói "chưa ai làm ma trận thay thế cho degron"; không hứa cải thiện 0,1747 như điều chắc chắn.

## Việc tiếp theo
1. **Trọng xác nhận C-6** ở [DECISIONS.md](../../DECISIONS.md) — bảy đề xuất từ audit 13/10, quan trọng nhất là sửa cách phát biểu mục tiêu G2 và có chuyển trọng tâm nhãn sang bộ bão hòa hay không. Những việc dưới đây phụ thuộc câu trả lời đó.
2. **Chốt thiết kế benchmark**: split theo cụm protein cov80, nhãn là trung bình hai replicate, giữ 130 peptide hai nguồn cùng phía, báo kèm trần nhãn 0,6514 trong mọi bảng.
3. **Huấn luyện baseline thành phần thật** rồi mới tới mô hình có ngữ cảnh — đây là bước đầu tiên xác lập G2, chưa làm.
4. Thử hướng ma trận thay thế trên bộ bão hòa (235 peptide, phủ 97,9%); chạy thang ablation `B → B + hạng 1 → B + hạng r` cùng split và ngân sách. Tính lực riêng cho cỡ mẫu nhỏ này trước.
5. Thiết kế ứng dụng đủ khác **bốn** tiền lệ đã có (xem dòng G3), trong đó có SVM của chính nhóm Zhang.

## Trong thư mục này
- [log.md](log.md) — nhật ký nghiên cứu (11–12/10/2026).
- research/: **[full-data-audit/](research/full-data-audit/README.md) (mới nhất, 13/10 — tải đủ dữ liệu, trần nhãn, lực thống kê)** · [topic-decision.md](research/topic-decision.md) (phạm vi 11/10, có phần lịch sử) · [composition-context-audit.md](research/composition-context-audit.md) · [e3-labels-audit/](research/e3-labels-audit/README.md) · [voutsinos-2026-audit/](research/voutsinos-2026-audit/README.md) · [topic-report/index.html](research/topic-report/index.html)
- presentation/: [presentation.html](presentation/presentation.html) · [presentation-validation.md](presentation/presentation-validation.md) · [session-02-prep.md](presentation/session-02-prep.md) (bản 11/10, đã lạc hậu)
- Hub học của đề tài: [lectures/degron-footprint/](../../lectures/degron-footprint/index.html)
