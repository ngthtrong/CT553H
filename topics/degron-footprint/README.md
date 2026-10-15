# Dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm

> **Mạch lập luận hiện hành: [topic-argument-2026-10-15.md](research/topic-argument-2026-10-15.md)** (thay [topic-decision.md](research/topic-decision.md) 11/10). Ba đề xuất đi kèm đang chờ Trọng: [C-7, C-8, C-9](../../DECISIONS.md).
>
> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md) — hiện là **đề tài chính** theo [D-023](../../DECISIONS.md#d-023). Cập nhật lần cuối: **15/10/2026**. Slug cũ là `degron-e3-specificity`; trục "đặc hiệu E3" đã bỏ từ 11/10/2026.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, protein, học máy (dạng dự đoán mức residue) |
| Dữ liệu | **Đã tải đủ bốn nguồn** (13/10): Zhang 2023 Mendeley cả 5/5 file, GEO GSE240610, repo Voutsinos 2026, 26 score set MaveDB → `topics/degron-footprint/data/`. PSI đã dựng từ read thô cho **mọi** điều kiện: quét rep1/rep2/BAG6 WT, bão hòa hai nửa. Xem [audit đầy đủ](research/full-data-audit/README.md) |
| Giai đoạn | Đã tải đủ, audit nhãn, **đo trần nhãn và lực thống kê**, **chạy xong đối chứng ΔPAP và kiểm tiền đề kiến trúc**; chưa huấn luyện mô hình nào |

## Bài toán
Degron là đoạn trình tự khiến protein bị đánh dấu để phân hủy. Câu hỏi: **residue nào trong degron quyết định độ bền**, và đột biến ở đó làm độ bền thay đổi bao nhiêu? Đầu vào là peptide/protein (kèm cấu trúc nếu có). Đầu ra là điểm quan trọng theo residue và dự đoán hiệu ứng đột biến (ΔPSI).

## Cổng G1/G2/G3
| Cổng | Trạng thái | Bằng chứng |
|---|---|---|
| G1 nhãn độc lập | **Đạt, mạnh nhất repo** — toàn bộ là nhãn thực nghiệm | [e3-labels-audit/](research/e3-labels-audit/README.md) |
| G2 đóng góp dương | **Chưa xác lập** (chưa huấn luyện mô hình nào), nhưng **khoảng trống đã chứng minh, đã định lượng đúng mốc, và nay đã có đối chứng thật**. Mốc theo [D-025](../../DECISIONS.md#d-025): baseline thành phần **0,4897**, trần nhãn **0,6514**, ngẫu nhiên 0,1204. **Mới 14/10:** ΔPAP của PAP (mô hình degron công bố gần nhất) chỉ đạt precision@3 **0,4270** trên cùng tập — **thấp hơn** baseline thành phần (p ≈ 6 × 10⁻¹⁹), nên mốc 0,4897 là mốc khó hơn và đúng để cam kết. Trên bộ bão hòa, thước đo nên là **AUROC mức ô**: ΔPAP 0,7692, trần 0,9519. **Lưu ý:** 0,6045 và 0,7792 là oracle đọc nhãn test, không dùng nữa | [pap-baseline/](research/pap-baseline/README.md) · [full-data-audit §4](research/full-data-audit/README.md) · [composition-context-audit.md](research/composition-context-audit.md) |
| G3 ứng dụng | **Yếu nhất trong các ứng viên.** Đã có **bốn** tiền lệ: DEGRONOPEDIA (*NAR* 2024), máy chủ web MetaDegron, Colab của nhóm PAP, và **mô hình học máy của chính nhóm Zhang 2023** dự đoán PSI toàn peptidome (Pearson 0,8955, RMSE 0,563 trên 260.989 peptide) — cái cuối mới phát hiện 13/10, **khác phạm vi** (peptide, không phải residue) nên không phải đối thủ trực tiếp, nhưng phải nêu. Chỗ khác biệt **đã kiểm 14–15/10**: cả bốn đều xuất ở mức **peptide/motif** (MetaDegron-D chỉ dùng trình tự, không attention), nên ma trận 28×20 trên nhãn đột biến thực nghiệm là chỗ khác biệt duy nhất;  nay đã xác nhận ma trận này **phủ 97,9% trên 235 peptide** từ bộ bão hòa | [full-data-audit §6–7](research/full-data-audit/README.md) · [topic-decision.md §7](research/topic-decision.md) |

## Rủi ro chính
- ~~**Lực thống kê — rủi ro số một.**~~ **Đã giải quyết 13/10: tập test đủ lực.** Kiểm ghép cặp với SD đo thật 0,2416: so baseline thành phần trung thực cần **18** peptide (lực ≈1,00); so mốc 0,6045 cần **209**, cho lực **0,82–0,94** ở n = 221–322. Hệ quả: **dùng split cov80** (271–322, lực 0,92–0,94), không dùng cov50 (n=221 chỉ cho lực 0,82). Khi có mô hình thật phải tính lại lực bằng SD của chính cặp đó. [Chi tiết](research/full-data-audit/README.md)
- **Nhãn mức residue chỉ lặp lại khoảng một nửa — rủi ro số một của bộ quét.** Peptide *có* footprint lặp lại tốt (89,3%), nhưng *residue nào* là footprint chỉ trùng ở mức Jaccard **0,4965**, và chỉ 16,0% peptide có tập vị trí dương giống hệt nhau giữa hai replicate. Đề tài dự đoán đúng ở mức residue này.
- ~~**Nhiễu đo chưa tách khỏi tín hiệu ngữ cảnh.**~~ **Đã tách 13/10.** Dư sau oracle thành phần là 0,3612, trong đó **75,9% là nhiễu đo**; ngữ cảnh học được cận trên chỉ **0,0872** phương sai, **không phải 35,0%**. Nhiễu **không** phải tạo tác của ngưỡng reads (giữ 0,72–0,77 từ reads≥10 đến ≥200) và được xác nhận bốn lần độc lập (~0,24–0,34) ⇒ tính chất của assay GPS.
- **Bộ bão hòa tốt hơn nhưng nhỏ hơn mức đã tưởng — nay là việc chặn.** Nhiễu chỉ 16,7%, Jaccard ô dương 0,6596, ma trận phủ 97,9%. Nhưng sau khi áp **đúng** ngưỡng peptide degron (PSI WT ≤ 3,0) thì chỉ còn **91 peptide**, không phải 235 ([pap-baseline §C](research/pap-baseline/README.md)). **Phải tính lực trên n = 91** trước khi cam kết thiết kế theo [D-025](../../DECISIONS.md#d-025) đề xuất 2. Bộ này không có phép đo hoang dã; phải dùng ô đồng nghĩa làm WT nội tại. **130/248** peptide trùng với bộ quét nên phải cùng phía train/test.
- Kiến trúc MIL/cổng cấu trúc: **tiền đề của hai trong năm thành phần đã được kiểm 14/10, theo hướng thuận** ([architecture-check/](research/architecture-check/README.md)) — nhưng [tra y văn cùng ngày](research/architecture-check/prior-art-exposure-gate.md) cho thấy **tiền đề cổng phơi lộ không mới** (Voutsinos 2026, Larsen 2025, QCDPred, DEGRONOPEDIA, JoGo) và **hiện tượng ΔPAP đổi dấu đã được Larsen 2025 tìm ra trên CRX** (0,54 ở IDR so với −0,19 ở vùng gấp). Phép đo của repo là xác nhận lại ở quy mô lớn hơn trên nhãn độ dồi dào, **không phải phát hiện**. Con số hệ số tương tác **+0,6625 chưa dùng được** cho tới khi chạy lại không có GCK và dùng cấu trúc homodimer cho NUDT15/ASPA. Nối hai nhãn: Spearman 0,7333 toàn cục nhưng chỉ **0,2921** trong nhóm degron, nên nhiệm vụ phụ nên là phân loại. **Vẫn chưa kiểm**: cấu trúc túi so với đầu hồi quy theo vị trí, và PLM so với one-hot — cả hai cần huấn luyện. **Chưa tìm thấy** tiền lệ đặt cổng phơi lộ **bên trong** mô hình học được tại bước gộp: PAP dùng cấu trúc chỉ để phân tích sau, MetaDegron-D chỉ dùng trình tự (cấu trúc chỉ vào nhánh XGBoost, không có attention), Schulze 2026 dùng cấu trúc để chia lớp. Tiền lệ khác: BioBlobs, OmniESI, Ilse 2018. Phát biểu đúng mức: **mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, không mới ở cơ chế**.
- Larsen 2025 đã tính rASA/pLDDT từ AlphaFold2 và đã làm bản đồ ΔPAP *in silico*, nên **"dùng cấu trúc" và "giải thích biến thể" không còn là phần mới**.
- Quy ước ngôn từ: không nói "16 E3 có nhãn CRISPR"; không nói "chưa ai làm đặc hiệu E3"; không nói "chưa ai làm ma trận thay thế cho degron"; không hứa cải thiện 0,1747 như điều chắc chắn.

## Việc tiếp theo

Thứ tự theo **chỗ có bằng chứng đo được**, xem [lập luận lại §7.4](research/topic-argument-2026-10-15.md).

1. **Tính lực thống kê trên n = 91** (peptide bão hòa đạt PSI WT ≤ 3,0) — **việc chặn duy nhất**. Nếu không đủ: nới ngưỡng lên 3,5 (141 peptide, phải biện minh) hoặc chấm mức ô kèm xử lý phụ thuộc trong peptide.
2. **Trọng xác nhận [C-7, C-8, C-9](../../DECISIONS.md)** — chỗ đặt đóng góp, vai của cổng phơi lộ, thước đo ma trận.
3. **Chốt thiết kế benchmark** theo [D-025](../../DECISIONS.md#d-025): split cụm protein cov80, nhãn trung bình hai replicate, 130 peptide hai nguồn cùng phía, bỏ BAG6 WT, báo kèm trần nhãn. Ghi rõ 725/770 peptide footprint có tile trong tập train của PAP.
4. **Huấn luyện baseline thành phần thật**, rồi **mô hình ngữ cảnh vị trí** — đây là chỗ có bằng chứng dương (+0,1311), không phải cổng phơi lộ.
5. **Ablation** `B → B + hạng 1 → B + hạng r` trên ma trận bão hòa, thước đo **AUROC mức ô** (ΔPAP 0,7692, trần 0,9519).
6. **Ứng dụng** xuất ma trận 28×20 **và** bản đồ mức vị trí (gộp 19 thay thế cho Spearman cao hơn: 0,3553 → 0,4130).
7. **Ngoài đường găng:** chạy lại phần cổng phơi lộ (bỏ GCK, homodimer cho NUDT15/ASPA, thêm ngưỡng rASA 0,1) và thêm hai đối chứng cho nhãn độ dồi dào — ma trận theo lớp phơi lộ của [Schulze 2026](https://doi.org/10.7554/eLife.103721) và ThermoMPNN ΔΔG.
8. Hai tiền đề kiến trúc còn lại (túi so với hồi quy theo vị trí; PLM so với one-hot) nằm trong chính việc huấn luyện ở mục 4–5.

## Trong thư mục này
- [log.md](log.md) — nhật ký nghiên cứu (11–12/10/2026).
- research/: **[topic-argument-2026-10-15.md](research/topic-argument-2026-10-15.md) (mạch lập luận hiện hành)** · [pap-baseline/](research/pap-baseline/README.md) và [architecture-check/](research/architecture-check/README.md) (14/10 — đối chứng ΔPAP, tiền đề cổng phơi lộ)** · [full-data-audit/](research/full-data-audit/README.md) (13/10 — tải đủ dữ liệu, trần nhãn, lực thống kê) · [topic-decision.md](research/topic-decision.md) (phạm vi 11/10, có phần lịch sử) · [composition-context-audit.md](research/composition-context-audit.md) · [e3-labels-audit/](research/e3-labels-audit/README.md) · [voutsinos-2026-audit/](research/voutsinos-2026-audit/README.md) · [topic-report/index.html](research/topic-report/index.html)
- presentation/: [presentation.html](presentation/presentation.html) · [presentation-validation.md](presentation/presentation-validation.md) · [session-02-prep.md](presentation/session-02-prep.md) (bản 11/10, đã lạc hậu)
- Hub học của đề tài: [lectures/degron-footprint/](../../lectures/degron-footprint/index.html)
