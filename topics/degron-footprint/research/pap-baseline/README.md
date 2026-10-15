# Baseline PAP, kiểm lại và chấm trên nhãn footprint

> Ngày **14/10/2026**. Script: [pap_baseline.py](pap_baseline.py) → [pap-baseline.json](pap-baseline.json).
> Phần A trả lời việc còn thiếu ghi ở [full-data-audit §12](../full-data-audit/README.md) ("chưa chạy lại
> baseline PAP sau khi tải lại repo"). Phần B và C là **đối chứng bắt buộc** mà
> [topic-decision §6](../topic-decision.md) yêu cầu nhưng chưa ai chạy: ΔPAP trên đúng thay thế thực nghiệm.
> **Không huấn luyện mô hình nào** — PAP dùng trọng số đã công bố của tác giả.

## Nhãn bằng chứng

- **[đo]** tự chạy trong phiên này, số có trong `pap-baseline.json`.
- **[phân tích]** suy luận của Claude từ các số đó.
- Quy ước ngôn từ của đề tài giữ nguyên: không nói "PAP không dự đoán được footprint", không nói bản đồ
  mô hình thành phần phải phẳng, không gọi ΔPAP là ma trận hạng 1.

## Chạy lại

```bash
tar -xzf topics/degron-footprint/data/raw/voutsinos-2026/repo/models/pap_weights.tgz \
    -C topics/degron-footprint/data/interim/pap-weights
.venv/bin/python topics/degron-footprint/research/pap-baseline/pap_baseline.py
```

Cần `h5py`, `numpy`, `scipy`. Seed 0 cho mọi phép phá tie và bootstrap.

## A. Tái lập PAP: khớp đúng số của phiên 11/10 và của bài báo

Trên **428 gene holdout hiệu dụng / 15.818 tile** (không dùng danh sách 527 gene công bố, vì 96 gene
trong đó nằm hết ở tập train — xem [voutsinos-2026-audit](../voutsinos-2026-audit/README.md)):

| Cấu hình | Phiên này | Phiên 11/10 | Bài báo |
|---|---:|---:|---:|
| `cnn2w1`, chỉ kênh nội | **0,8239** | 0,8239 | 0,82 |
| `cnn2w1`, đầy đủ (kênh C-term cho **mọi** tile) | **0,8690** | 0,8690 | 0,87 |
| `cnn2w7`, đầy đủ | **0,8722** | 0,8722 | — |

**[đo]** Trùng đến bốn chữ số thập phân sau khi tải lại repo @`9b3eafa6`. Bản tái lập bằng numpy dùng
được, và **cả hai con số công bố đều khớp**. Điều này đóng việc còn thiếu của audit 13/10.

## B. ΔPAP trên nhãn footprint của bộ quét — **đối chứng này yếu hơn baseline thành phần**

ΔPAP = PAP(peptide đột biến) − PAP(peptide hoang dã), tính trên **đúng** thay thế có trong CSV của
Zhang 2023, rồi chấm bằng precision@3 với cùng ngưỡng và cùng tập peptide như
[label_ceiling.py](../full-data-audit/label_ceiling.py). Nhãn là replicate 2, điểm thành phần ước lượng từ
replicate 1 (không đọc nhãn test). 2.403 peptide.

| Mốc | precision@3 | Spearman theo peptide |
|---|---:|---:|
| Ngẫu nhiên | 0,1232 | — |
| **ΔPAP `cnn2w1`** | **0,2959** | 0,4128 |
| **ΔPAP `cnn2w7`** | **0,4270** | 0,4337 |
| Baseline thành phần (ước lượng trung thực) | 0,4884 | — |
| Trần thực nghiệm (rep1 chấm trên nhãn rep2) | 0,6514 | — |

**[đo]** Kiểm ghép cặp trên cùng peptide:

| So sánh | Chênh trung bình | Bootstrap 95% | Wilcoxon |
|---|---:|---|---:|
| ΔPAP `cnn2w7` − thành phần | **−0,0615** | [−0,073; −0,049] | 6,3 × 10⁻¹⁹ |
| ΔPAP `cnn2w7` − trần nhãn | −0,2244 | [−0,236; −0,213] | 2,9 × 10⁻²⁰⁷ |
| ΔPAP `cnn2w1` − thành phần | −0,1925 | [−0,204; −0,181] | 1,9 × 10⁻¹⁵⁶ |

**[phân tích] Ba hệ quả cho thiết kế đề tài:**

1. **Mốc G2 ở [D-025](../../../../DECISIONS.md#d-025) được xác nhận là mốc khó hơn ΔPAP.** Baseline thành
   phần 0,4884 **cao hơn** ΔPAP `cnn2w7` (0,4270) với p ≈ 6 × 10⁻¹⁹. Nên 0,4897 là mốc đúng để cam kết,
   không phải ΔPAP. Vẫn phải báo ΔPAP trong bảng kết quả vì đây là đối chứng mà
   [topic-decision §6](../topic-decision.md) yêu cầu, và vì nó là mô hình degron công bố gần nhất.
2. **Khoảng cách cnn2w1 → cnn2w7 lớn hơn nhiều ở nhiệm vụ residue.** Trên thang điểm khối, cửa sổ 7 chỉ
   hơn +0,0032 Pearson (0,8690 → 0,8722) — chính tác giả đã đo. Trên nhiệm vụ footprint, nó hơn
   **+0,1311** precision@3 (0,2959 → 0,4270). **[phân tích]** Đây là **bằng chứng dương đầu tiên trong
   repo** cho hướng "thêm năng lực bắt ngữ cảnh cục bộ": trần "+0,0032" đo trên thang điểm khối **không
   áp được** cho nhiệm vụ mức residue. Không suy ra kiến trúc nào sẽ thắng; chỉ nói trục này chưa bão hòa
   ở thang đo của đề tài.
3. **Không có rò rỉ từ tập train của PAP.** Tách theo việc protein của peptide có nằm trong gene train của
   PAP hay không: `cnn2w7` cho 0,4268 (656 peptide, có) so với 0,4270 (1.747 peptide, không). Chênh lệch
   bằng không. Nên ΔPAP dùng được làm đối chứng trên toàn bộ tập test.

Nhãn **trung bình hai replicate** (theo D-025 đề xuất 3) cho cùng bức tranh, Spearman cao hơn chút:
ΔPAP `cnn2w7` precision@3 0,4364, Spearman 0,4747 trên 2.265 peptide. **[đo]**

0 đột biến nào là codon stop trong vùng được chấm, nên quy tắc cắt tại stop không ảnh hưởng kết quả.

## C. ΔPAP trên ma trận bão hòa — nguồn nhãn chính theo D-025

Nhãn ô = trung bình hai nửa, WT nội tại là trung vị các ô đồng nghĩa (xem
[full-data-audit §6](../full-data-audit/README.md)). Lọc thêm **PSI WT ≤ 3,0** cho đúng định nghĩa peptide
degron như bộ quét → **91 peptide** trong 235 peptide có ma trận.

| Phép đo (trung bình theo peptide) | Giá trị |
|---|---:|
| Trần: nửa A chấm trên nhãn nửa B, Spearman mức ô | **0,6989** |
| Trần: nửa A chấm trên nhãn nửa B, AUROC gọi ô dương | **0,9519** |
| ΔPAP `cnn2w1`, Spearman mức ô | 0,3553 |
| ΔPAP `cnn2w7`, Spearman mức ô | 0,3527 |
| ΔPAP `cnn2w1`, AUROC | **0,7692** |
| ΔPAP `cnn2w7`, AUROC | 0,7646 |
| ΔPAP `cnn2w1`, Spearman mức **vị trí** (gộp 19 thay thế) | 0,4130 |

**[đo]**

**[phân tích] Bốn điều quan trọng cho thiết kế:**

1. **Lọc PSI WT ≤ 3,0 cắt bộ bão hòa từ 235 xuống 91 peptide.** Đây là **con số chưa ai nêu** và nó đổi
   bài toán lực thống kê: D-025 đề xuất 2 đã kèm điều kiện "tính lại lực cho 235 peptide", nhưng cỡ mẫu
   thật của peptide degron chỉ là **91**. Phân bố: 9 peptide có PSI WT < 2, 82 peptide 2–3, rồi 50 peptide
   3–3,5 và 35 peptide 3,5–4 nằm ngoài ngưỡng. **Việc chặn mới của đề tài là tính lực trên n = 91**, không
   phải 235. Nếu lực không đủ, hai đường ra: nới ngưỡng PSI WT (3,5 cho 141 peptide) và phải biện minh,
   hoặc chấm ở **mức ô** (91 × ~500 ô) thay vì mức peptide — nhưng ô trong cùng peptide không độc lập.
2. **AUROC là thước đo nên dùng cho ma trận, không phải Spearman.** Trần Spearman mức ô chỉ 0,6989, trong
   khi trần AUROC đạt 0,9519: việc **xếp hạng** mọi ô khó hơn hẳn việc **tách ô dương khỏi ô âm**, và
   nhiệm vụ của đề tài là cái sau. ΔPAP đạt AUROC 0,7692 nên dư địa còn **0,1827**.
3. **Ở nguồn nhãn này, `cnn2w1` và `cnn2w7` bằng nhau** (0,7692 so với 0,7646), khác hẳn bộ quét. **[phân
   tích]** Không kết luận được vì sao; một khả năng là n = 91 chưa đủ phân biệt. Phải nhắc khi so hai nguồn.
4. **Gộp 19 thay thế lên mức vị trí làm Spearman tăng** (0,3553 → 0,4130), đúng như kỳ vọng nếu nhiễu mức
   ô bị triệt tiêu khi gộp. Nên bản đồ mức vị trí vẫn là cách trình bày chắc hơn trong ứng dụng.

## Đã kiểm những gì

- Tái lập PAP trùng bốn chữ số với phiên 11/10 **và** hai con số của bài báo (0,82 / 0,87) — xác nhận
  bản numpy đúng và repo tải lại không khác.
- precision@3 dùng đúng hàm của [label_ceiling.py](../full-data-audit/label_ceiling.py) (import trực
  tiếp, không viết lại), cùng ngưỡng reads ≥ 10, PSI WT ≤ 3,0, ΔPSI ≥ 1,0, ≥ 21 vị trí, seed 0.
- Baseline thành phần tái lập 0,4884 trên 2.403 peptide, khớp 0,4897 của
  [power_analysis.py](../full-data-audit/power_analysis.py) trên tập peptide hơi khác (chênh do
  power_analysis không đòi ΔPAP tính được cho mọi vị trí).
- Mọi so sánh dùng **kiểm ghép cặp** trên cùng peptide, kèm bootstrap 2.000 lần và Wilcoxon.
- Tách rò rỉ: ánh xạ ENSG → UniProt từ `library/cytosol_genes.csv.gz` của repo Voutsinos.

## Những gì **không** làm

- **Không huấn luyện mô hình nào.** PAP dùng trọng số công bố; baseline thành phần là trung bình nhóm, không
  phải mô hình học được. **G2 vẫn chưa xác lập.**
- Không chạy lại `train_cnn2w.py` của tác giả — script đó trỏ vào **cột DNA** thay vì cột acid amin
  (lỗi đã ghi ở [voutsinos-2026-audit](../voutsinos-2026-audit/README.md)), nên không dùng được.
- Không dùng split theo cụm protein cov80 ở đây: các số trên là **trên toàn bộ peptide dùng được**, để so
  với trần nhãn và baseline thành phần trên cùng cơ sở. Khi benchmark chính thức dựng xong thì phải báo
  lại ΔPAP **trên đúng tập test** đó.
