# Audit Koren 2018 Table S4 (+ S3) và cổng P2 — 22/10/2026

Tiêu chí chốt **trước khi tính số cổng** ở [PROTOCOL.md](PROTOCOL.md) (kèm mục §0 nói rõ đã xem gì trước khi chốt). Số liệu: [results.json](results.json), sinh bởi [audit.py](audit.py). Không đổi trạng thái G2/G3, không sửa đề cương hay slide, không nhập gì vào huấn luyện.

**[ĐO] Kết quả một dòng.** Dữ liệu **đọc được và đúng** (PSI tái tính khớp 1.827/1.827 dòng, chiều ΔPSI đúng sinh học), nhưng **cổng P2 KHÔNG đạt**: chỉ **5 cụm cov80 mới** (cần ≥ 20), và đây là giới hạn *cấu trúc* của nguồn (S4 chỉ có 9 substrate). Vai trò còn lại theo protocol: **tập kiểm chứng ngoài** cho lớp degron đầu C, không nhập huấn luyện.

## 1. Ánh xạ file → bảng `[ĐO]` (đã mở file)

Thay cho giả thuyết `[CHƯA XÁC MINH]` trước đó (suy từ kích thước). Mọi file là bản NIHMS của Koren et al. 2018 (PMC6003881), SHA-256 ở [data/README.md](../../data/README.md).

| File | Bảng | Nội dung đã xác nhận | Có PSI đột biến điểm? |
|---|---|---|---|
| `supplement-10.xlsx` | **S3A–E** | Thế **Ala** (Gly→Arg) từng vị trí trên 5 clone (#3 55-aa, #5 10-aa, #6 51-aa, #7 55-aa, #8 12-aa); có hàng WT mỗi sheet; 3 bin | Có (một thay thế/vị trí), 49+10+46+55+12 ô |
| **`supplement-11.xlsx`** | **S4A–I** | **Saturation mutagenesis**, 9 substrate, 3 bin | **Có**, 1.739 ô đột biến + 88 ô đồng nghĩa (1.827 dòng) |
| `supplement-12.xlsx` | S5A–B | Danh sách chuỗi substrate KLHDC3/APPBP2 | Không |
| `supplement-13.xlsx` | S6A–D | S6A = sàng thư viện G-end (~2.060 peptide 56-mer, 3 bin, PSI mỗi peptide); S6B–D = danh sách substrate | Không (mức peptide) |
| `supplement-14.xlsx` | S7A–F | S7A = sàng C-terminal 23-mer (**~22.560 peptide**, **4 bin**, PSI mỗi peptide); S7B = dự đoán motif; S7C–F = substrate Cul2/4A/4B | Không (mức peptide) |
| `supplement-15.xlsx` | S8A–G | Kết quả sàng CRISPR (MAGeCK) | Không |

`[ĐO]` Hai sheet của S4 mang nhãn nhầm `S5E`/`S5G` trong tên (CHGA, Peptide35) — lỗi gõ của tác giả, nội dung thuộc S4. `supplement-8`, `-9` (S1, S2) chưa tải, không cần cho P2.

## 2. Table S4 là gì `[ĐO]`

| Substrate | Dài WT | Vị trí đột biến | Ô đột biến | Ô đồng nghĩa (mốc WT) | WT nội tại (PSI) | ΔPSI trung vị | ΔPSI lớn nhất |
|---|---:|---|---:|---:|---:|---:|---:|
| Clone#8 | 12 | 1–12 | 228 | 10 (thiếu ô đồng nghĩa ở 2 vị trí) | 1,681 | 0,000 | 1,11 |
| EPHB2 | 23 | 14–23 | 190 | 10 | 1,722 | 0,038 | 1,21 |
| PDGFC | 23 | 14–23 | 190 | 10 | 1,718 | 0,074 | 1,21 |
| EMID1 | 23 | 14–23 | 190 | 10 | 1,761 | 0,021 | 1,14 |
| CHGA | 23 | 14–23 | 190 | 9 | 1,823 | −0,067 | 0,84 |
| XP_211896.1 | 23 | 14–23 | 190 | 10 | 1,780 | 0,064 | 0,97 |
| Peptide#35 | 23 | 14–23 | 190 | 9 | 1,788 | 0,024 | 0,44 |
| MAGEA3 | 23 | 14–23 | 181 | 10 | 1,738 | 0,059 | 0,67 |
| MSRB2 | 23 | 14–23 | 190 | 10 | 1,827 | −0,001 | 0,43 |

- `[ĐO]` **Thang đo:** cột `PSI` = Σ i·Binᵢ/ΣBinᵢ với **3 bin** → PSI ∈ [1;3] (quan sát 1,49–2,93). Nhãn chính của Zhang dùng **6 bin** → PSI ∈ [1;6]. Hai thang **không cộng được thô**.
- `[ĐO]` **Peptide:** 23-mer đầu C **có codon dừng `*`** (đầu C tự do, tức là degron *đầu C*), chỉ **10 vị trí cuối** được đột biến (Clone#8: cả 12). Nhãn chính của Zhang là 28-mer nội vùng, quét cả 28 vị trí.
- `[ĐO]` **Lớp degron:** Gly-end (Clone#8, EPHB2, PDGFC, EMID1…), RxxG/EE/R-3 (MAGEA3, MSRB2) — các lớp C-degron khác nhóm mà đề tài đang có.
- `[ĐO]` Mỗi substrate: tổng 200 ô = 10 vị trí × 20 acid amin (gồm ô đồng nghĩa), một vài ô thiếu (CHGA, Peptide#35: 199; MAGEA3: 191; Clone#8: 238/240).

### Footprint cực kỳ cục bộ `[ĐO]`

Trung vị ΔPSI theo vị trí (xem `median_dpsi_by_pos` trong results.json): hầu hết vị trí ≈ 0; tín hiệu nằm ở **1–3 vị trí cuối**.

| Substrate | Vị trí có trung vị ΔPSI > 0,25 |
|---|---|
| Clone#8 | 12 (Gly cuối): +1,04 |
| EPHB2 / PDGFC / EMID1 | −2 và −1: 22 (+0,42 / +0,44 / +0,33), 23 (+1,06 / +1,12 / +0,75) |
| CHGA | 23 (+0,38) |
| XP_211896.1 | 19 (+0,38), 22 (+0,63) |
| MSRB2 | 21 (+0,29) |

`[DIỄN GIẢI]` Đây là dạng nhãn khác hẳn nhãn Zhang: **9 substrate × ~1–2 vị trí quan trọng**, phần còn lại là nền nhiễu ≈ ±0,1. Với nhãn Zhang, tỉ lệ ô ΔPSI ≥ 1 là 13,1% (base) / 11,4% (nhóm nới ngưỡng); ở S4 là **3,0%** (và 0% ở 6 trong 9 substrate). Quy về cùng tỉ lệ biên độ (ΔPSI ≥ 0,4 trên thang rộng 2 tương đương ≥ 1 trên thang rộng 5) là **9,6%**, vẫn thấp hơn. Cả hai ngưỡng là *mô tả*, không phải tiêu chí.

## 3. Cổng P2 `[ĐO]`

| Mã | Tiêu chí (chốt trước) | Kết quả | Kết luận |
|---|---|---|---|
| **G1** | ≥ 20 cụm cov80 mới | **5** cụm mới | **Không đạt** |
| R1 | Tái tính PSI từ Bin1–3 khớp ≤ 1e-6, ≥ 99% dòng | 1.827/1.827 (sai lệch lớn nhất 5e-12) | Đạt |
| R2 | ≥ 8 ô đồng nghĩa ở ≥ 7/9 substrate | 9/9 (9–10 ô; SD của ô đồng nghĩa 0,05–0,11) | Đạt |
| R3 | Gly cuối Clone#8: trung vị ΔPSI ≥ +0,5, ≥ 90% dương | n = 19, trung vị **+1,04**, 100% dương | Đạt |

**Cổng = G1 ∧ R1 ∧ R2 ∧ R3 → KHÔNG đạt.** Theo PROTOCOL §4: nhãn ΔPSI **tái lập được và đúng chiều**, nhưng không đủ cụm → **vai trò: tập kiểm chứng ngoài, không nhập huấn luyện**.

### Chi tiết G1 `[ĐO]`

13 chuỗi WT có thể (9 của S4 + 4 clone S3 chưa trùng; Clone#8 trùng S4A) → ánh xạ vào Swiss-Prot người bằng hậu tố đầu C:

| Chuỗi | Kết quả ánh xạ |
|---|---|
| EPHB2 | P29323 — **chính EPHB2 là protein có peptide trong 176 peptide huấn luyện/kiểm** (accession này là một trong 9 accession bị loại khỏi `proteins-full.fasta`, nên được thêm lại ở lượt phân cụm liên hợp) → không mới |
| PDGFC · EMID1 · CHGA · MAGEA3 · MSRB2 | Q9NRA1 · Q96A84 · P10645 · P43357 · Q9Y3D2 → **5 cụm mới** (MAGEA3 là cụm 7 thành viên họ MAGE; bốn cái kia là cụm đơn) |
| Clone#8, XP_211896.1, Peptide#35 | **Không ánh xạ được** (không khớp hậu tố/đoạn nào của Swiss-Prot người; XP_211896.1 là mã RefSeq loài khác) |
| S3 Clone#3/#5/#6/#7 | **Không ánh xạ được** (clone cDNA, không khớp đoạn nào của Swiss-Prot người) |

Quy ước bảo thủ của protocol: không ánh xạ được = 0 cụm. Kể cả nếu cả 13 đều ánh xạ được và đều mới thì tối đa 13 < 20; vì vậy G1 **không thể đạt** với S4 ∪ S3, và protocol đã ghi trước điều này (§0). Phân cụm liên hợp: 6.573 protein Zhang + 5 protein Koren không có sẵn → 5.091 cụm; chạy riêng, **không ghi đè** `protein-id30-cov80_cluster.tsv`.

### Chẩn đoán R4 (không tham gia cổng) `[ĐO]`

Trên 12 ô Clone#8 có cả ở S3E (thế Ala/Arg) và S4A: Spearman **0,10** (n = 12). Ngoài ô G12R (ΔPSI +0,90 ở S3, +1,08 ở S4) thì phần còn lại của S3 dao động ±0,3–0,5 trong khi S4 ≈ 0 ± 0,1; mốc WT cũng lệch (S3: 1,584; S4: ô đồng nghĩa 1,681). `[DIỄN GIẢI]` S3 nhiễu hơn S4 đáng kể (ít read hơn); hai thí nghiệm đồng thuận ở hiệu ứng lớn nhưng **không** ở hiệu ứng nhỏ. Không dùng S3 làm nhãn; nếu dùng Koren thì chỉ S4. Đây là chỉ dấu về sàn nhiễu của hệ đo này, không phải bằng chứng cho hay chống cổng.

## 4. Hệ quả cho kế hoạch `[DIỄN GIẢI]`

1. **P2 → P4 → P5 không có nguồn nhãn ngoài từ Koren.** 5 cụm mới (≈ 900 ô, phần lớn ≈ nền) không thể làm dịch chuyển đường cong học; dùng làm huấn luyện còn mất vì khác thang (3 bin), khác thư viện (23-mer đầu C có stop, 10 vị trí), khác phân bố nhãn (3% ô dương).
2. **Giá trị còn lại là kiểm chứng ngoài, và là loại kiểm chứng có sức nặng:** lớp degron khác (C-degron), thư viện khác, nhóm tác giả khác. Phép kiểm khả thi và đúng thiết kế: mô hình Zhang-trained (ridge M3) cho điểm 1.739 ô → AUROC theo substrate với nhãn "ΔPSI ≥ 0,4" hoặc Spearman. Cảnh báo trước: footprint của S4 nằm ở 1–3 vị trí cuối, còn nhãn Zhang là degron nội vùng, nên **kết quả âm ở đây sẽ không phản bác mô hình** (khác lớp degron), còn kết quả dương mới có nghĩa. Chưa chạy; cần protocol riêng và duyệt.
3. **Nếu muốn vẫn đi tìm nhãn ngoài cùng thư viện:** hai ứng viên còn trong [dataset-search](../next-steps-plan-2026-10-22/dataset-search.md) (Shimshon 2024, Bekturova 2025) và con số "219 degron CRL saturation" cần đối chiếu với dữ liệu Zhang đã có. Chưa kiểm.
4. **Nguồn S7A (≈ 22.560 peptide 23-mer đầu C, 4 bin) và S6A (≈ 2.060, 3 bin) là tầng T2** (mức peptide, không đột biến điểm), khác thang. Không đánh giá ở đây; ghi nhận làm ứng viên giám sát yếu nếu P3 muốn thêm lớp đầu C.

## 5. Giới hạn và quyền sử dụng

- `[ĐO]` Chỉ 9 substrate (S4) / 13 chuỗi (kèm S3) — kết luận "5 cụm mới" là về **các substrate Koren chọn**, không về mọi tiềm năng của hệ GPS đầu C.
- `[ĐO]` Ánh xạ protein bằng khớp hậu tố đầu C trong Swiss-Prot hiện hành (2026_03), không phải trình tự lúc làm thí nghiệm; 6/13 chuỗi không ánh xạ được nên con số 5 có thể thấp hơn số thật vài đơn vị, nhưng không thể vượt 13 nên **kết luận không đạt cổng không đổi**.
- `[ĐO]` Quyền sử dụng: bản NIHMS, **không** thuộc PMC Open Access (`oa.fcgi` 404). Dùng nội bộ; `data/` đã gitignore. Không đưa bảng gốc lên git/phụ lục/nguyên mẫu công khai; chỉ trích số tổng hợp kèm ghi công. File `koren-2018-cells.tsv` (bảng ô chuẩn hóa) nằm ở `data/interim/`, cùng quy định.
- `[ĐO]` Benchmark mô tả; không phải kiểm chứng ngoài mô hình nào.

## 6. Dựng lại

```bash
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  topics/degron-footprint/research/koren-s4-audit-2026-10-22/audit.py
```

Cần `data/raw/koren-2018/NIHMS967427-supplement-{10,11}.xlsx`, `data/processed/proteins-full.fasta`, UniProt ghim, `mmseqs` trong PATH. Chạy ≈ 1–2 phút (MMseqs2 trên 6.578 protein). Sinh `results.json` (ở đây), `data/interim/koren-2018-cells.tsv` (cột: `table, substrate, pos, wt_aa, mut_aa, psi, dpsi, n_bins`; 1.911 dòng: 1.739 S4 + 172 S3) và `data/interim/koren-2018-cluster/`.
