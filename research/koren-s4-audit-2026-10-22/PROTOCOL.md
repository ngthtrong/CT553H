# PROTOCOL — audit Koren 2018 Table S4 và cổng P2 (chốt trước khi tính số cổng)

Chốt ngày 22/10/2026, **trước** khi chạy `audit.py`. Không sửa sau khi thấy số; nếu phải đổi thì viết phần phụ lục ghi rõ "đổi sau khi thấy kết quả".

## 0. Những gì đã xem *trước* khi chốt (để người đọc biết mức "mù" của protocol)

`[ĐO]` Khi mở file để ánh xạ bảng, đã thấy: tên sheet, dòng tiêu đề, vài dòng đầu/cuối, số dòng của từng sheet, và danh sách ký hiệu thay thế "đồng nghĩa" (ví dụ `K14K`). Chưa tính bất kỳ thống kê nào: chưa tính ΔPSI, tỉ lệ ô dương, tái tính PSI, ánh xạ protein, hay phân cụm. Từ cấu trúc đó **đã biết** Table S4 chỉ có **9 sheet = 9 substrate** và S3 thêm 5 clone (Clone#8 trùng S4A), nên tối đa **13 peptide / ≤ 13 cụm** — thấp hơn ngưỡng 20 của cổng. Tiêu chí G1 vẫn giữ **đúng ngưỡng của kế hoạch** (`next-steps-plan` P2: ≥ 20 cụm cov80 mới) thay vì hạ xuống cho vừa số; kết quả "không đạt" là dự đoán gần như chắc chắn và được báo là kết quả.

`[ĐO]` Cũng đã biết từ bài báo (Methods): thư viện bão hòa của Koren chia **3 bin** (PSI ∈ [1;3]), còn Zhang 2023 chia **6 bin** (PSI ∈ [1;6]). Đây là sự khác thang đo, **không** phải tiêu chí cổng (xem §4).

## 1. Phạm vi nguồn đủ điều kiện

| Bảng | Nội dung | Đủ điều kiện nhãn ΔPSI mức residue? |
|---|---|---|
| S4 (`supplement-11.xlsx`, 9 sheet) | Saturation mutagenesis, mỗi vị trí → mọi acid amin, 10 vị trí cuối (23-mer) hoặc 12 vị trí (Clone#8) | **Có** |
| S3 (`supplement-10.xlsx`, 5 sheet) | Thế alanine (Gly→Arg) từng vị trí trên 5 clone, có hàng WT | **Có**, phụ (một thay thế/vị trí) |
| S5, S6B–D, S7C–F, S8 | Danh sách chuỗi substrate, kết quả CRISPR | Không (không có PSI đột biến) |
| S6A, S7A | Sàng thư viện peptidome (PSI mỗi peptide, không đột biến điểm) | Không cho cổng P2. Chỉ là nguồn tầng T2 (mức tile); ghi nhận, không đánh giá ở đây |

## 2. Quy ước tính

- **PSI tái tính** = Σ i·Binᵢ / Σ Binᵢ, i = 1..3 (công thức trong Methods của bài).
- **WT nội tại mỗi substrate** = trung vị PSI của các ô "đồng nghĩa" (acid amin thế = acid amin gốc, ví dụ `K14K`) — cách tương đương với mốc WT của Zhang (trung vị ô đồng nghĩa). **ΔPSI** = PSI(mutant) − WT nội tại; dương = ổn định hơn WT (cùng chiều với nhãn chính).
- **Trình tự WT** của mỗi substrate = trình tự mutant với vị trí đột biến hoàn nguyên về acid amin gốc (cột `Substitution`), bỏ ký tự `*`.
- **Ánh xạ protein:** trình tự WT (23-mer, hoặc 12-mer của Clone#8) phải khớp **hậu tố đầu C** của một protein trong `human-reviewed-2026-10-12.fasta.gz`; nếu không có thì khớp chuỗi con bất kỳ; nếu vẫn không thì **không ánh xạ được** và đếm là 0 cụm (bảo thủ). Nhiều accession cùng khớp → giữ tất cả, đếm theo cụm nên không cộng đôi.
- **Phân cụm:** MMseqs2 `easy-cluster` đúng bộ tham số của `prepare_protein_clusters.py` (id 0,3 · cov 0,8 · `--cov-mode 0` · cluster-mode 1 · single-step · `-s 7.5`), chạy **riêng** trên `proteins-full.fasta` (6.573 protein của Zhang) ∪ các protein Koren ánh xạ được. Không ghi đè cụm hiện có. Cụm "mới" = cụm liên hợp **không chứa accession nào** của 176 peptide huấn luyện/kiểm (91 gốc + 85 nới ngưỡng 4,0).

## 3. Cổng P2 (tiêu chí chốt trước)

Cổng đạt khi **đồng thời**:

| Mã | Tiêu chí | Ngưỡng |
|---|---|---|
| **G1** | Số cụm cov80 *mới* (S4 ∪ S3, sau ánh xạ) | **≥ 20** |
| **R1** | Tái tính PSI từ Bin1–3 khớp cột PSI của tác giả | \|Δ\| ≤ 1e-6 ở ≥ 99% dòng của S4 |
| **R2** | Mốc WT nội tại dựng được từ ≥ 8 ô đồng nghĩa | ≥ 7/9 substrate S4 |
| **R3** | Chiều ΔPSI đúng sinh học (kiểm với kết luận của bài: Gly cuối là thiết yếu cho substrate KLHDC2/3) | Clone#8, vị trí 12 (Gly cuối): trung vị ΔPSI của các thế ≠ G ≥ **+0,5** và ≥ 90% thế có ΔPSI > 0 |

"ΔPSI tái lập được" của kế hoạch = R1 ∧ R2 ∧ R3. Cổng = G1 ∧ R1 ∧ R2 ∧ R3.

**Chẩn đoán, không tham gia cổng:** R4 — tương hợp giữa S3 và S4 trên các ô trùng cả chuỗi lẫn vị trí của Clone#8 (Spearman, báo kèm n); độ phủ ánh xạ; tỉ lệ ô dương ở hai định nghĩa ngưỡng (xem §4); so sánh phân bố ΔPSI với nhãn Zhang.

## 4. Hệ quả chốt trước theo kết quả

- **Cổng đạt:** vẫn **không** trộn thô vào huấn luyện. Phải có chỉ báo nguồn/thư viện (23-mer đầu C có codon dừng, 3 bin, ≠ 28-mer, 6 bin của Zhang), và nhãn quy về cùng thang (đề xuất: ΔPSI chia biên độ lý thuyết `B−1`, B = số bin) hoặc head riêng — đúng điều kiện (a) của P4.
- **G1 không đạt, R1–R3 đạt:** Koren S4 **chỉ làm tập kiểm chứng ngoài** (lớp degron đầu C, khác thư viện). Không nhập huấn luyện. P4/P5 không được coi là có nguồn nhãn ngoài từ Koren.
- **R1–R3 không đạt:** không dùng ở bất kỳ vai trò nào cho tới khi hiểu được vì sao.
- Mọi trường hợp: nguồn **không có giấy phép mở** (PMC `oa.fcgi` 404); dùng nội bộ, không đưa bảng gốc lên git/phụ lục/nguyên mẫu công khai.

## 5. Bất biến

Đọc xlsx bằng `python -I` + `openpyxl` (`data_only=True`, `read_only=True`), không chạy macro/mã trong file. Không sửa `raw/`. Kết quả nhỏ ghi `results.json` ở thư mục này.
