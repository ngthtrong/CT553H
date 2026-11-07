# PROTOCOL — R3: cổng miền áp dụng cho công cụ — 22/10/2026

**Chốt trước khi chạy `r3-domain-gate.ipynb`.** Tệp này được băm SHA-256 và nhúng vào notebook (`PROTOCOL_SHA256`); `nbkit.check_protocol` dừng notebook nếu tệp đổi sau khi chốt. R3 không đổi trạng thái G2/G3 và không đụng tới mô hình ΔPSI.

## 0. Biết trước khi chốt (phải nói thẳng)

Phân tích cục bộ nhẹ [local-analysis.json](local-analysis.json) / [README](README.md) **đã được xem trước khi viết tệp này**. Hệ quả cho tính "chốt trước":

- **Tầng (i) (tra cứu PSI đo):** các ngưỡng của tiêu chí (i) được đặt **sau khi thấy** AUROC điểm ước lượng ≈ 0,92 trên 235 peptide. Tiêu chí (i) vì vậy là một **ngưỡng chất lượng tối thiểu để dùng**, không phải một giả thuyết kiểm định độc lập.
- **Tầng (ii) (dự đoán từ trình tự):** mô hình, đặc trưng, lưới siêu tham số và ngưỡng đều chốt dưới đây **trước khi** chạy bản đầy đủ. **Nhưng** một lần chạy kiểm hạ tầng (`run_r3.py --smoke`: chỉ 30.000 tile ngẫu nhiên + pool, không phải dữ liệu đầy đủ) đã in ra Spearman giai đoạn A ≈ 0,87 và AUROC giai đoạn B ≈ 0,82 trên tập con đó. Kiểm đối chứng sau đó: xáo nhãn cho Spearman −0,02 (không rò rỉ trong pipeline), hệ số ridge hợp lý sinh học (thơm/kỵ nước hạ PSI, acid tăng PSI). Các con số smoke **không** được dùng để chọn gì; mô hình và ngưỡng ở dưới được viết trước lần chạy đó và **không đổi sau khi thấy số**.
- **Một sửa đổi kỹ thuật làm trước khi chốt (không phải đổi tiêu chí):** file cụm của G2 chỉ có 6.573 protein nên không dùng được cho sàng 18.753 protein (protein không có trong file sẽ thành cụm riêng, paralog rò rỉ qua fold). R3 dùng phân cụm MMseqs2 id30 cov80 **toàn proteome** (`build_proteome_clusters.py`, cùng cờ với bản gốc; 20.431 protein → 12.918 cụm). Chi tiết ở [README](README.md).

## 1. Câu hỏi và định nghĩa

Mô hình ΔPSI (ridge M3 + Platt) học trên peptide có **`PSI(WT)` nội tại ≤ 4,0** (trung vị ô đồng nghĩa của bộ bão hòa). Công cụ cần nói với người dùng: *tile này có thuộc miền đó không?*

- **Nhãn miền** `d(p) = 1` nếu `PSI(WT) nội tại ≤ 4,0`, với `p` thuộc **pool bão hòa** 235 peptide (sau lọc kỹ thuật, không áp ngưỡng degron; trong đó 176 có `d = 1`). Nhãn nằm trong [`data/processed/r3-sat-wt-pool.tsv`](../../data/README.md) do `local_analysis.py` dựng.
- **PSI đo của tile** `x(p)`: PSI của tile `ACC_GENE_n` trong sàng peptidome GPS (`gps-peptidome-rep1.tsv`; tile hợp lệ nếu có PSI, `reads ≥ 10`, accession có trong snapshot UniProt, tile 28-mer đủ độ dài theo quy tắc `(n−1)·23`).
- `[ĐO]` (local-analysis) **hai thang PSI lệch nhau một hằng số ≈ 0,9** (PSI của sàng thấp hơn PSI(WT) nội tại ≈ 0,88 trung bình, Pearson 0,84, độ dốc ≈ 1,02). Vì vậy **không dùng ngưỡng 4,0 thô trên PSI của sàng**; phải ánh xạ qua mô hình logistic dưới đây.

## 2. Tầng (i): tra cứu PSI đo → trạng thái miền

- **Mô hình M1** (chốt): hồi quy logistic `P(d=1 | x) = σ(a + b·x)`, không phạt, IRLS, khớp trên pool.
- **Đánh giá:** `GroupKFold(5)` trên pool theo cụm cov80 của protein (accession → đại diện cụm trong `protein-id30-cov80-proteome_cluster.tsv`) → xác suất OOF. Báo: AUROC OOF; Brier OOF so với Brier của tần suất nền (tính trong train fold); **kỹ năng Brier** `BSS = 1 − Brier/Brier_nền`. Bootstrap 5.000 lần **theo cụm**, seed 17, 29, 43 (báo cả ba).
- **Trạng thái ba mức** (chốt, là chính sách chứ không phải tham số tinh chỉnh): `in-domain` nếu `P ≥ 0,80`; `out-of-domain` nếu `P < 0,50`; còn lại `borderline`. Báo `x` tương ứng (đảo hàm logistic), và trên OOF: độ chính xác (`P(d=1 | in-domain)`), tỉ lệ `d=0` lọt vào `in-domain`, và tỉ lệ pool rơi vào mỗi mức.
- **Tiêu chí "tầng (i) dùng được"** (cả ba): (a) AUROC OOF có cận dưới CI 95% **≥ 0,80 ở cả ba seed**; (b) BSS có cận dưới CI 95% **> 0 ở cả ba seed**; (c) trên OOF, tỉ lệ pool `d=0` được xếp `in-domain` **≤ 0,25** (cổng an toàn: lỗi nguy hiểm là gắn nhãn tile ngoài miền là trong miền).
- Không đạt ⇒ tầng (i) **không** dùng trạng thái miền định lượng; công cụ chỉ hiển thị PSI đo kèm cảnh báo định tính.

## 3. Tầng (ii): dự đoán PSI của tile ngoài sàng từ trình tự

Dùng cho chuỗi người dùng gõ và tile không có trong sàng.

- **Mô hình G** (chốt, **một** mô hình, không chọn lại sau khi thấy số): hồi quy ridge trên **420 đặc trưng** = đếm 20 acid amin (tổng 28) + đếm 400 cặp liền kề (tổng 27) của tile 28-mer. Không chuẩn hóa thêm; tâm hóa bằng thống kê train. Mục tiêu: `x` (PSI đo của sàng, thang sàng).
- **Dữ liệu huấn luyện:** mọi tile hợp lệ ở mục 1 (kỳ vọng ≈ 3,5·10⁵), loại tile chứa ký tự ngoài `ACDEFGHIKLMNPQRSTVWY`.
- **Chia fold:** `GroupKFold(5)` theo cụm cov80 **toàn proteome** của protein (`data/interim/protein-id30-cov80-proteome_cluster.tsv`) trên **toàn bộ tile** (không chia theo tile; mọi tile của cùng cụm cùng fold).
- **Siêu tham số:** `α ∈ {1, 10, 100, 1000, 10000}`, chọn **lồng**: với mỗi outer fold k, chọn α theo MSE trung bình trên 4 inner-val (mỗi fold còn lại lần lượt làm val, huấn luyện trên 3 fold còn lại); sau đó khớp lại trên 4 fold và dự đoán fold k. Khớp bằng phương trình chuẩn từ thống kê gộp (tất định; không dùng seed).
- **Giai đoạn A (chất lượng dự đoán PSI):** trên OOF toàn bộ tile: Pearson, Spearman (Pearson trên hạng toàn cục), RMSE so với RMSE của tham chiếu "trung bình train" . Bootstrap theo cụm 5.000 lần, seed 17/29/43.
- **Giai đoạn B (ra trạng thái miền):** với pool, lấy dự đoán OOF `x̂(p)` của giai đoạn A (đã ở fold giữ-cụm-ra), **mô hình M2** `P(d=1 | x̂) = σ(a₂ + b₂·x̂)` khớp trên pool, đánh giá bằng đúng quy trình mục 2 (OOF theo cụm pool, AUROC/BSS/ba mức).
- **Tiêu chí "tầng (ii) dùng được"** (cả bốn): (a) Spearman giai đoạn A (ước lượng điểm) **≥ 0,30**; (b) AUROC giai đoạn B, cận dưới CI 95% **≥ 0,70 ở cả ba seed**; (c) BSS giai đoạn B, cận dưới CI 95% **> 0 ở cả ba seed**; (d) tỉ lệ `d=0` lọt vào `in-domain` **≤ 0,35** trên OOF.
- Không đạt ⇒ **tầng (ii) không được triển khai**: chuỗi người dùng gõ nhận trạng thái `unknown` kèm cảnh báo, và công cụ chỉ chấm trạng thái miền cho tile **có trong sàng**. Đây là kết quả hợp lệ và sẽ được ghi vào thẻ cổng, không bị che.

## 4. Đầu ra

- `results.json`: mọi số ở mục 2–3 (kèm CI từng seed), kết luận theo tiêu chí, kích thước dữ liệu, số tile bị loại.
- `gate-weights.npz` (hệ thống nạp): hệ số ridge (420), intercept, α, mô tả đặc trưng, `a,b` của M1 và M2, các ngưỡng `P` (0,80; 0,50) và `x`/`x̂` tương ứng, hai cờ `usable_tier1`, `usable_tier2`.
- `gate-card.json`: tóm tắt kết quả, phạm vi, giới hạn, giấy phép nguồn, SHA-256 gói dữ liệu/mã. `env.json`, `gates.json`.
- **Điều kiện tiên quyết:** R0 đã ĐẠT trong cùng môi trường. Nếu chưa, notebook dừng.

## 5. Điều cổng này KHÔNG nói

- Cổng chỉ nói *tile giống miền huấn luyện đến mức nào theo PSI(WT)*. Nó **không** nói điểm ΔPSI chính xác ở đó: AUROC 0,8208 là benchmark phát triển, đo **chỉ trong miền**.
- `d` được định nghĩa trên **PSI(WT) nội tại của thí nghiệm bão hòa**, không trên PSI của sàng. Hai thang lệch ≈ 0,9 (mục 1); mọi ngưỡng ở thang sàng đều qua M1/M2.
- Pool 235 peptide được chọn để làm thí nghiệm bão hòa (nên thiên về tile có PSI sàng thấp: trung vị 2,39 so với 3,81 toàn sàng). Ngoại suy cho tile PSI cao dựa vào đuôi trên của logistic và **chưa được kiểm trực tiếp**.
- Không dùng nhãn của Koren 2018, MetaDegron, Larsen 2025 hay ClinVar. Không khẳng định gì về bệnh.

## 6. Môi trường và chi phí

CPU là đủ (ước lượng 2–6 phút, **chưa benchmark**); không cần GPU. Seed bootstrap 17/29/43; ridge tất định.
