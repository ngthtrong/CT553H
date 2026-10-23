# R3 — Cổng miền áp dụng cho công cụ — 22/10/2026

**Trạng thái: ĐÃ CHẠY trên Kaggle (CPU, 22/10/2026, 29 giây) — CẢ HAI TẦNG ĐỀU "DÙNG ĐƯỢC" theo PROTOCOL.** [PROTOCOL.md](PROTOCOL.md) chốt trước; notebook [r3-domain-gate.ipynb](r3-domain-gate.ipynb); kết quả và trọng số cổng ở [run-kaggle-20261022/](run-kaggle-20261022/) (gốc: [r3-results.zip](r3-results.zip)). Không đổi trạng thái G2/G3.

**[ĐO] Kết quả một dòng của phân tích cục bộ.** Tile của sàng peptidome GPS **trùng định danh** với 235/235 peptide bão hòa và cho PSI tương quan tốt (Pearson 0,84), **nhưng hai thang PSI lệch nhau một hằng số ≈ 0,9**: ngưỡng `PSI(WT) ≤ 4,0` của mô hình ΔPSI **không** dùng thẳng trên PSI của sàng được (độ đặc hiệu chỉ 0,20). Cổng phải ánh xạ qua mô hình logistic học từ pool. Sàng phủ **72%** tile 28-mer của proteome.

## Kết quả `[ĐO]` — [results.json](run-kaggle-20261022/results.json), [gate-card.json](run-kaggle-20261022/gate-card.json), [gate-weights.npz](run-kaggle-20261022/gate-weights.npz)

347.780 tile hợp lệ của sàng (12.023 cụm cov80 toàn proteome); pool 235 peptide bão hòa (176 trong miền, **59 ngoài miền**). Đánh giá OOF theo cụm; chỉ số "ba seed" chỉ là ba seed bootstrap (ridge tất định nên CI trùng nhau).

| | Tầng (i): tra PSI sàng | Tầng (ii): dự đoán từ chuỗi |
|---|---:|---:|
| Spearman giai đoạn A (dự đoán PSI sàng) | — | 0,869 (Pearson 0,836; RMSE 0,699 so với 1,274 của "trung bình") |
| AUROC OOF (CI 95%) | 0,911 (0,86–0,95) | 0,815 (0,75–0,87) |
| Kỹ năng Brier (BSS) | 0,516 | 0,242 |
| Tỉ lệ peptide ngoài miền bị xếp "trong miền" (tiêu chí ≤ 0,25 / ≤ 0,35) | 0,169 (10/59) | 0,203 (12/59) |
| Độ chính xác khi xếp "trong miền" | 0,934 | 0,908 |
| Ngưỡng PSI tương ứng P ≥ 0,8 ("in") / P < 0,5 ("out") | x ≤ 2,687 / x ≥ 3,110 | x̂ ≤ 3,700 / x̂ ≥ 4,426 |
| Hàm logistic (a, b) | 10,187 ; −3,275 | 8,457 ; −1,911 |
| Kết luận theo PROTOCOL | **dùng được** | **dùng được** |

- `[ĐO]` Áp hai ngưỡng tầng (i) lên 360.724 tile của sàng có reads ≥ 10 ([proteome-domain-share.json](run-kaggle-20261022/proteome-domain-share.json), sinh bởi [domain_share.py](domain_share.py)): **khoảng 26% "in-domain", 9% "borderline", 65% "out-of-domain"**. Một công cụ từ chối mặc định ngoài miền sẽ từ chối khoảng hai phần ba tile tự chọn từ UniProt.
- `[DIỄN GIẢI]` Ngưỡng thô `PSI ≤ 4,0` **không** dùng được trên PSI sàng (độ đặc hiệu 0,20): phải đi qua hàm logistic. Hệ thống phải có trạng thái `borderline` cho cả hai tầng (P giữa 0,5 và 0,8).
- Giới hạn: chỉ 59 peptide ngoài miền nên tiêu chí tỉ lệ lọt "trong miền" là phép so điểm ước lượng (CI rộng); pool thiên về PSI sàng thấp (trung vị 2,39 so với 3,81 toàn sàng), nên ngoại suy cho tile PSI cao chưa kiểm trực tiếp; cổng chỉ nói tile giống miền huấn luyện đến đâu, không nói điểm ΔPSI chính xác.

## 1. Phân tích cục bộ (không huấn luyện) — [local_analysis.py](local_analysis.py) → [local-analysis.json](local-analysis.json)

| Câu hỏi | Kết quả `[ĐO]` |
|---|---|
| Q1. Tile của sàng có cùng định danh với 176/235 peptide bão hòa? | **Có.** 235/235 peptide của pool bão hòa (sau lọc kỹ thuật, kể cả 176 peptide huấn luyện) có mặt theo tên trong `gps-peptidome-rep1.tsv` và đều có PSI với `reads ≥ 10`. Trình tự thật của tile sàng **không có trong file** (chỉ có tên) nên quy tắc `(n−1)·23` chỉ được kiểm gián tiếp qua khớp tên + khớp PSI |
| Q2. Thang PSI trùng nhau không? | **Tương quan tốt nhưng lệch hằng số.** Pearson 0,840, Spearman 0,837 (n = 235); PSI sàng **thấp hơn** PSI(WT) nội tại trung bình **0,876**; độ dốc OLS 1,018, intercept 0,831; RMSE 1,016. So với PSI mốc WT của sàng quét (`_mut0`, n = 117): Pearson 0,609, lệch −0,879 (độ lệch ≈ 0,9 PSI là giữa **sàng peptidome** và hai nguồn còn lại; scanning `_mut0` và WT nội tại của bão hòa trùng nhau về trung bình, xem [cross-source-audit.json](../r6-ladder-scan-2026-10-23/cross-source-audit.json)) |
| Q2'. Dùng thẳng ngưỡng 4,0 trên PSI sàng? | **Không.** Ngưỡng 4,0: độ chính xác 0,800, độ nhạy 1,00, **độ đặc hiệu 0,203**, AUROC của PSI sàng cho "trong miền" 0,916. Ngưỡng 3,0: độ chính xác 0,634, độ đặc hiệu 0,403, AUROC 0,907. Gần như mọi tile bị xếp "trong miền" ở ngưỡng 4,0 thô |
| Q2''. Phụ thuộc số reads? | n = 12 (reads 10–30): r = 0,62; n = 123 (30–100): r = 0,85, RMSE 1,04; n = 100 (≥100): r = 0,86, RMSE 0,93 |
| Q3. Độ phủ proteome? | Snapshot 20.431 protein có **482.216** tile 28-mer đủ độ dài theo quy tắc. Sàng có **360.724** dòng PSI hợp lệ (`reads ≥ 10`), trong đó **347.806** khớp tile đủ độ dài ⇒ phủ **72,1%**; 18.536 protein có ≥ 1 tile đo được. Trên PSI sàng thô: 32,4% tile ≤ 3,0 và 54,6% tile ≤ 4,0 (trung vị PSI 3,81) |
| Q4. Độ lệch chọn của pool | PSI sàng của pool bão hòa có trung vị **2,39** (khoảng 1,21–5,22) so với 3,81 toàn sàng: pool thiên về tile PSI thấp. Mọi ngoại suy cho tile PSI cao dựa vào đuôi trên của logistic và **chưa kiểm trực tiếp** |

## 2. Phát hiện kỹ thuật phải sửa trước khi chốt

`[ĐO]` File cụm của G2 (`protein-id30-cov80_cluster.tsv`) chỉ có **6.573** protein (những protein có trong các thí nghiệm). Trong 18.753 accession của sàng chỉ **6.573** có cụm; số còn lại sẽ thành cụm riêng nếu dùng file này ⇒ paralog (olfactory, KRAB-ZNF…) rò rỉ qua fold và làm tầng (ii) lạc quan giả.

`[ĐO]` Đã chạy lại MMseqs2 (cùng cờ với bản gốc, `--threads 2`, ~9,5 phút) trên **toàn snapshot 20.431 protein** ⇒ **12.918 cụm**, cụm lớn nhất 430 protein. Script [build_proteome_clusters.py](build_proteome_clusters.py), SHA-256 đầu vào/đầu ra trong [proteome-cluster-manifest.json](proteome-cluster-manifest.json). Cụm này chỉ dùng cho R3; **không** thay các cụm của G2/P0/P1 và không sửa bảng cũ.

## 3. Điều tôi đã thấy trước khi chốt (nói thẳng)

- Các **phân tích Q1–Q4** ở trên được xem **trước** khi viết PROTOCOL, nên tiêu chí tầng (i) là ngưỡng chất lượng tối thiểu chứ không phải giả thuyết độc lập (PROTOCOL §0).
- Một lần chạy **smoke** (30.000 tile ngẫu nhiên + pool, kiểm hạ tầng) đã in Spearman giai đoạn A ≈ 0,87 và AUROC giai đoạn B ≈ 0,82 trên tập con đó. Kiểm đối chứng: xáo nhãn cho Spearman −0,019; hệ số ridge hợp lý sinh học (W, F, Y, I giảm PSI mạnh nhất; E, D, Q, P tăng). Con số smoke **không được dùng làm kết quả** và không dùng để chọn gì: mô hình, đặc trưng, lưới α và mọi ngưỡng của PROTOCOL được viết trước lần chạy đó. Kết quả thật là lần chạy đầy đủ trong notebook.

## 4. Thiết kế (tóm tắt, chi tiết ở PROTOCOL)

- **Tầng (i):** `P(trong miền | PSI sàng) = σ(a + b·PSI)` khớp trên pool 235 peptide (nhãn `PSI(WT) nội tại ≤ 4,0`), đánh giá bằng GroupKFold theo cụm proteome.
- **Tầng (ii):** ridge 420 đặc trưng (đếm 20 acid amin + 400 cặp liền kề) dự đoán PSI sàng từ trình tự trên ~3,5·10⁵ tile, nested CV theo cụm; rồi ánh xạ `σ(a₂ + b₂·PSI_dự đoán)`.
- **Ba trạng thái:** `in-domain` (P ≥ 0,80), `borderline`, `out-of-domain` (P < 0,50); tầng (ii) không dùng được ⇒ chuỗi tự gõ nhận `unknown`.
- **Đầu ra cho hệ thống:** `gate-weights.npz`, `gate-card.json`.

## 5. Dựng lại

```bash
.venv/bin/python -I topics/degron-footprint/research/r3-domain-gate-2026-10-22/local_analysis.py      # ~1 phút
.venv/bin/python -I topics/degron-footprint/research/r3-domain-gate-2026-10-22/build_proteome_clusters.py  # ~10 phút, MMseqs2
.venv/bin/python -I topics/degron-footprint/research/r3-domain-gate-2026-10-22/run_r3.py --smoke    # kiểm hạ tầng ~12 giây (không phải kết quả)
```

Bản đầy đủ chạy qua notebook (xem RUN.md). `local_analysis.py` ghi thêm `data/processed/r3-sat-wt-pool.tsv` (nhãn miền của 235 peptide; ghi trong `data/README.md`).

## 6. Giới hạn

- Cổng nói *tile giống miền huấn luyện đến đâu theo PSI(WT)*; nó **không** nói điểm ΔPSI chính xác ở đó (AUROC 0,8208 đo chỉ trong miền).
- Nhãn miền định nghĩa trên PSI(WT) **nội tại của thí nghiệm bão hòa**; hai thang PSI lệch ≈ 0,9, mọi ngưỡng ở thang sàng phải đi qua logistic.
- Sàng peptidome là một replicate (`Control Replicate 1`); độ nhiễu đo không được mô hình hóa riêng.
- Số liệu Q1–Q4 là phân tích mô tả trên cùng dữ liệu sẽ dùng để khớp cổng; chúng không phải kiểm chứng độc lập.
