# Audit đầy đủ các bộ dữ liệu degron — 13/10/2026

> **Phạm vi:** tải đủ bốn nguồn dữ liệu của đề tài, dựng lại PSI từ read thô cho mọi điều kiện,
> và đo những thứ trước đây chưa đo được. **Không huấn luyện mô hình nào.** Mọi số trong tài liệu
> này trỏ tới file JSON kết quả cùng thư mục.
>
> Vị trí đề tài chỉ ghi ở [DECISIONS.md](../../../../DECISIONS.md). Tài liệu này là **bằng chứng**,
> không phải quyết định. Các đề xuất nêu ở mục 8 chờ Trọng xác nhận.

## Nhãn bằng chứng dùng trong tài liệu

| Nhãn | Nghĩa |
|---|---|
| **[đo]** | Tự chạy script trong thư mục này trên dữ liệu đã tải, có file JSON kết quả |
| **[nguồn]** | Số do tác giả bài báo công bố hoặc ghi trong dữ liệu của họ |
| **[phân tích]** | Suy luận từ các số **[đo]**, nêu rõ giả định |
| **[đề xuất]** | Kiến nghị của Claude, **chưa được duyệt** |

---

## 1. Đã tải những gì

Manifest đầy đủ kèm SHA-256 từng file: `data/raw/full-download-manifest.json`. Script: [fetch_all.py](fetch_all.py).

| Nguồn | Nội dung | Kích thước | Trạng thái trước 13/10 |
|---|---|---:|---|
| [Mendeley 10.17632/32h94v2yv2.2](https://data.mendeley.com/datasets/32h94v2yv2/2) | **cả 5 file**, SHA-256 khớp checksum Mendeley công bố | ~430 MB | chỉ có 2/5 file |
| [GEO GSE240610](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610) | Table S1 (475.507 dòng × 3 sheet) + `RAW.tar` + filelist | 75 MB | chưa tải |
| [KULL-Centre/_2025_Voutsinos_degron_cytosol](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol) @ `9b3eafa6` | 50 file, MIT | 180 MB | **đã mất khỏi máy**, chỉ còn ghi chú audit |
| MaveDB API | 26 score set của 9 gene, CC0 | 24 MB | chỉ có số từ metadata |

Zenodo `16925278` trả **403 Forbidden** từ mạng này ("unusual traffic from your network"); repo GitHub cùng tác giả, cùng giấy phép MIT là bản thay thế. **[đo]**

**Ba file Mendeley lần đầu có trên máy**, trong đó quan trọng nhất là
`I28 GPS Peptidome Screen and MLN4924 and SVM.zip` (393 MB) — xem mục 6.

## 2. Dựng lại PSI cho mọi điều kiện

Script: [build_psi.py](build_psi.py) → `data/processed/psi-{rep1,rep2,wt,sat_a,sat_b}.tsv`,
báo cáo [psi-build.json](psi-build.json).

Trước đây repo chỉ dùng được `I28 Scanning Mutagenesis Replicate 1.csv` — file duy nhất tác giả
đã tính sẵn PSI. Nhưng ZIP còn chứa read thô của **Replicate 2**, của **mẫu BAG6 WT**, và 12 mẫu
**bão hòa**. Công thức PSI được suy ra và kiểm:

```
factor_i = (Σ_rows b_1) / (Σ_rows b_i)     # bin 1 làm chuẩn
nb_i     = b_i × factor_i
PSI      = (Σ_i i × nb_i) / (Σ_i nb_i)     # thang 1..6, THẤP = bị phân hủy nhanh
```

**Cổng kiểm đã đạt:** dựng lại PSI của Replicate 1 từ 6 file read thô và so với cột PSI của tác giả
trên **261.865** giá trị — lệch lớn nhất **5,0 × 10⁻⁷**, đúng bằng nửa đơn vị làm tròn của số tác giả
in ra. **[đo]**

| Bảng mới | Số định danh |
|---|---:|
| `psi-rep1.tsv` (đối chứng) | 261.868 |
| `psi-rep2.tsv` | 261.999 |
| `psi-wt.tsv` (BAG6 WT) | 264.036 |
| `psi-sat_a.tsv` | 134.608 |
| `psi-sat_b.tsv` | 134.563 |

### 2.1 Lỗi trong pipeline đã công bố của Zhang 2023

Script gộp của tác giả đọc 6 file count với `header=TRUE` trên file **không có header**, nên **dòng dữ
liệu đầu tiên của mỗi file bị ăn mất**. Dòng đầu: S1 = `mut10`, S2 = `mut17`, S3–S6 đều = `mut24`. Hệ quả
trong CSV công bố: `mut10` và `mut17` bị ghi `Sum=0, PSI=NA` dù có read; `mut24` mất bin 3–6 nên PSI của
nó lệch **0,62**. Lỗi còn lan vào **hệ số chuẩn hóa**, vì tác giả tính hệ số trên chính cột `b_i` đã
thiếu dòng. **[đo]**

Ảnh hưởng thực tế **nhỏ** (3 định danh trên 261.868, không peptide nào trong số đó là footprint), nhưng
phải biết để tái lập: `build_psi.py --validate` mô phỏng đúng lỗi này để khớp số tác giả, còn bảng xuất
ra dùng dữ liệu **đã sửa**. Cùng loại với lỗi đọc nhầm cột DNA trong mã Voutsinos đã ghi ở
[voutsinos-2026-audit](../voutsinos-2026-audit/README.md).

## 3. Độ lặp lại — rủi ro số hai của đề tài, nay đã đo được

Script: [replicate_audit.py](replicate_audit.py) → [replicate-audit.json](replicate-audit.json).
Ngưỡng giữ nguyên audit 12/10: reads ≥ 10, PSI WT ≤ 3,0, ≥ 21 vị trí, dương nếu ΔPSI ≥ 1,0.

| Phép đo | Kết quả |
|---|---:|
| PSI rep1 vs rep2, Pearson (reads ≥ 10 / ≥ 100 / ≥ 500) | 0,9239 / 0,9394 / 0,9672 |
| ΔPSI rep1 vs rep2, Pearson · Spearman (85.518 cặp vị trí) | **0,7229** · 0,6485 |
| Độ lệch chuẩn nhiễu đo của ΔPSI, một replicate | **0,2974** |
| Footprint gọi lại được ở rep2, mức **peptide** | **2.104 / 2.356 = 89,3%** |
| Trùng khớp mức **vị trí**, Jaccard trung bình | **0,4965** |
| Peptide có tập vị trí dương **giống hệt** nhau | **377 / 2.356 = 16,0%** |

**[đo]** Đồng thời, script tái lập đúng **2.624** footprint ở Replicate 1 — khớp con số đã biết của repo —
và cho **2.639** ở Replicate 2 một cách độc lập.

**[phân tích] Hệ quả quan trọng nhất:** peptide nào *có* footprint thì lặp lại tốt (89,3%), nhưng
*residue nào* là footprint chỉ lặp lại khoảng một nửa (Jaccard 0,4965). Đề tài dự đoán ở **mức residue**,
nên đây chính là đại lượng mà nhãn phải đáng tin — và nó chỉ đáng tin ở mức trung bình.

### 3.1 Phân rã phương sai, cùng cơ sở với con số 35,0%

Audit 12/10 ghi "35,0% phương sai ΔPSI còn lại sau oracle thành phần" và để mở câu hỏi phần đó là ngữ
cảnh học được hay nhiễu đo. Tính lại trên **cùng cơ sở trung bình macro theo peptide**, với nhãn là
trung bình hai replicate (nên phương sai nhiễu của nhãn là `Var(d1−d2)/4`):

| Thành phần | Tỉ lệ |
|---|---:|
| Dư sau oracle theo cặp thay thế | 0,3612 |
| Trong đó là **nhiễu đo** | **75,9%** |
| **Ngữ cảnh học được, cận trên** | **0,0872** |

**[đo]** [label-ceiling.json](label-ceiling.json). Tức phần có thể học thêm nhờ ngữ cảnh là khoảng **8,7%**
phương sai ΔPSI, **không phải 35%**.

### 3.2 Nhiễu không phải do ngưỡng reads quá thoáng

Giả thuyết ban đầu của Claude: nhiễu lớn chỉ vì ngưỡng reads ≥ 10 quá thoáng. **Giả thuyết này sai.**
Script [read_depth_sweep.py](read_depth_sweep.py) → [read-depth-sweep.json](read-depth-sweep.json):

| reads ≥ | footprint còn lại | nhiễu / dư | ngữ cảnh ≤ | trần P@3 | baseline thành phần |
|---:|---:|---:|---:|---:|---:|
| 10 | 2.624 | 0,759 | 0,0872 | 0,6511 | 0,4892 |
| 50 | 2.474 | 0,750 | 0,0880 | 0,6568 | 0,4930 |
| 100 | 2.175 | 0,720 | 0,0954 | 0,6696 | 0,4964 |
| 200 | 1.309 | 0,766 | 0,0757 | 0,6614 | 0,5061 |
| 400 | 128 | 1,005 | 0,0000 | 0,5990 | 0,4844 |

**[đo]** Tỉ lệ nhiễu giữ nguyên 0,72–0,77 suốt từ reads ≥ 10 đến ≥ 200; ở ≥ 400 thì mẫu sụp còn 64 peptide
chấm được. **[phân tích]** Nhiễu là tính chất của assay quét, không phải tạo tác của ngưỡng. Điểm tốt nhất
là reads ≥ 100 (ngữ cảnh ≤ 0,0954 với 2.175 footprint), nhưng cải thiện nhỏ.

## 4. Trần thực nghiệm do chính nhãn đặt ra

Script: [label_ceiling.py](label_ceiling.py) → [label-ceiling.json](label-ceiling.json).

Ý tưởng: coi ΔPSI của một replicate như "một mô hình biết đúng sinh học nhưng có nhiễu đo", rồi chấm nó
trên nhãn của replicate kia bằng đúng precision@3 mà đề tài dùng. Không mô hình học được nào biết nhiều
hơn một phép đo lặp của cùng đại lượng, trừ khi nó khử được nhiễu.

| Mốc | precision@3 |
|---|---:|
| Ngẫu nhiên | 0,1204 |
| **Baseline thành phần, ước lượng trung thực** (học nhóm cùng cặp trên rep1, chấm trên nhãn rep2) | **0,4897** |
| Cận oracle của lớp thành phần (audit 12/10, **chọn được nhờ nhìn nhãn test**) | 0,6045 |
| **Trần thực nghiệm: rep1 chấm trên nhãn rep2** | **0,6514** |
| cùng thế, chiều ngược lại | 0,6488 |
| Oracle không ràng buộc (audit 12/10, **cũng nhìn nhãn test**) | 0,7792 |

**[đo]** 2.403 peptide được chấm.

**[phân tích] Ba điều chỉnh với cách đọc cũ:**

1. **0,7792 không phải dư địa.** Nó là oracle đọc chính nhãn test nên không mô hình nào đạt. Do đó
   "dư địa 0,1747" và "+28,9% tương đối" ghi ở thẻ đề tài **không còn đúng** như cách diễn giải cũ.
2. **0,6045 cũng là oracle**, chỉ là oracle của một lớp mô hình hẹp hơn. Baseline thành phần *thật*,
   khi phải ước lượng từ dữ liệu khác, chỉ đạt **0,4897**.
3. **Dư địa thật** giữa trần thực nghiệm và baseline trung thực là **0,1617** — vẫn lớn, và lớn hơn
   dư địa so với mốc 0,6045 (chỉ 0,0469).

Nói cách khác: đề tài **vẫn có khoảng trống đáng kể để chứng minh đóng góp dương**, nhưng phải phát biểu
mốc cho đúng. Mốc nên là baseline thành phần được huấn luyện và đánh giá công bằng, kèm **báo cả trần
nhãn 0,65** để người đọc biết giới hạn trên.

## 5. Lực thống kê — việc chặn của đề tài, đã trả lời

Script: [power_analysis.py](power_analysis.py) → [power-analysis.json](power-analysis.json).
Kiểm ghép cặp theo peptide (cùng peptide được chấm bởi cả hai phương pháp), hai phía, α = 0,05.
Độ lệch chuẩn của chênh lệch **đo từ dữ liệu thật**: 0,2416; effect size d_z = 0,669.

| Mốc so sánh | Dư địa | n cần cho lực 0,80 | Lực ở n = 221 | n = 271 | n = 301 | n = 322 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline thành phần trung thực (0,4897) | 0,1617 | **18** | ≈1,00 | ≈1,00 | ≈1,00 | ≈1,00 |
| Cận oracle 0,6045 | 0,0469 | **209** | 0,8228 | 0,8917 | 0,9204 | 0,9362 |

MDE ở lực 0,80: **0,0455** (n=221) → **0,0377** (n=322). **[đo]**

**[phân tích] Kết luận:** tập test 221–322 footprint chia theo cụm protein **đủ lực**. So với baseline
thành phần trung thực thì dư thừa lực. So với mốc 0,6045 thì vẫn đạt nhưng **sát biên ở split cov50**
(lực 0,82 tại n=221), nên **nên dùng split coverage 80%** (271–322 footprint, lực 0,92–0,94).

**Giới hạn:** độ lệch chuẩn 0,2416 đo trên cặp (replicate đầy đủ, baseline thành phần). Một mô hình học
được so với baseline có thể cho độ lệch chuẩn khác; khi có mô hình thật **phải tính lại lực** bằng độ lệch
chuẩn của chính cặp đó.

### 5.1 Độ bền với cách xử lý tie

Baseline thành phần gán **điểm bằng nhau** cho mọi vị trí trong một nhóm cùng cặp thay thế, nên nó sinh
rất nhiều tie và kết quả phụ thuộc cách phá tie. Đo cả ba cách, trên cùng 2.403 peptide: **[đo]**

| Phá tie | Trần replicate | Baseline thành phần | Dư địa | SD | MDE ở n=221 |
|---|---:|---:|---:|---:|---:|
| Ngẫu nhiên đều (quy ước đang dùng) | 0,6514 | 0,4897 | 0,1617 | 0,2416 | 0,0455 |
| Bất lợi nhất cho baseline | 0,6514 | 0,4066 | 0,2448 | 0,2707 | 0,0510 |
| **Có lợi nhất cho baseline** | 0,6514 | **0,5754** | **0,0760** | 0,2137 | 0,0403 |

**[phân tích]** Hai điều:

1. **Trần 0,6514 không đổi** ở cả ba cách, vì ΔPSI thật gần như không có tie. Con số trần vững.
2. **Kết luận "tập test đủ lực" đứng vững ở cả ba cách:** ngay trong trường hợp có lợi nhất cho baseline,
   dư địa 0,0760 vẫn lớn hơn MDE 0,0403 tại n = 221.

Phá tie "có lợi nhất cho baseline" **không hợp lệ** cho một mô hình thật, vì nó phải đọc nhãn mới xếp
được như vậy; quy ước đúng là ngẫu nhiên đều, cùng quy ước với audit 12/10. Ghi cả dải để không ai lấy một
con số lẻ ra dùng mà không biết độ nhạy này.

## 6. Bộ bão hòa: chất lượng tốt hơn bộ quét rõ rệt

Script: [saturation_audit.py](saturation_audit.py), [saturation_matrix.py](saturation_matrix.py)
→ [saturation-audit.json](saturation-audit.json), [saturation-matrix.json](saturation-matrix.json).

Định danh bão hòa là `<peptide>_mut<vị trí><chữ thường>`, chữ thường là **amino acid thay vào**; đủ cả
20 chữ, vị trí 1–28, **249 peptide**. Hai nửa S1–S6 và S7–S12 là hai replicate: PSI tương quan
**0,9544** trên 110.544 định danh (reads ≥ 100), nên giả định thứ tự bin được xác nhận. **[đo]**

### 6.1 Bộ bão hòa không có phép đo hoang dã nào

**0 trên 134.608** định danh có dạng `_mut0`. Nên ΔPSI **không tự tính được** từ bộ này. **[đo]**

Đường ra, đã kiểm hai lần: vì mỗi vị trí được thay bằng **cả 20** amino acid, ô mà amino acid thay vào
trùng residue hoang dã là một **construct đồng nghĩa** (đổi codon, giữ nguyên protein) — tức một phép đo
WT nội tại. Mỗi peptide có 28 ô như vậy.

- Quy tắc tile suy từ bộ quét: 28-mer, bước **23**, bắt đầu ở `(n-1)×23`. Khớp **128/130** peptide có
  trình tự thật; 2 ca lệch bị **loại**, không đoán. **[đo]**
- 28 ô WT-nội-tại của một peptide: mỗi ô ~1.600 reads, PSI lệch nhau **SD 0,031**. Trung vị SD trong
  peptide trên toàn bộ: **0,0576**. **[đo]**
- Đối chiếu chéo WT nội tại với PSI hoang dã của bộ quét (117 peptide có cả hai): Pearson **0,7882**,
  chênh trung bình **−0,0132** (gần như không lệch hệ thống), SD chênh 0,5795. **[đo]**

### 6.2 Ma trận ΔPSI vị trí × amino acid

| Phép đo | Kết quả |
|---|---:|
| Peptide dựng được ma trận | **235** |
| Độ phủ trung bình của 28×19 | **97,9%** |
| Ô thay thế đo được ở **cả hai** nửa | **122.412** |
| ΔPSI giữa hai nửa, Pearson | **0,8335** |
| Nhiễu đo, một nửa | 0,2645 |
| **Tỉ lệ nhiễu trên phương sai quan sát** | **16,7%** |
| **Jaccard khi gọi một Ô là dương** | **0,6596** |
| Peptide có cả trong bộ quét | **130 / 248** |

**[đo]**

**[phân tích]** So với bộ quét (ΔPSI Pearson 0,7229; nhiễu chiếm 75,9% phần dư; Jaccard mức vị trí
0,4965), bộ bão hòa **tốt hơn trên mọi trục**: tương quan cao hơn, nhiễu thấp hơn nhiều, nhãn lặp lại
tốt hơn. Nó cũng là nguồn duy nhất cho **ma trận 28×20**, tức chỗ khác biệt G3 mà thẻ đề tài đã nêu.
Giá phải trả là **chỉ 235–248 peptide** thay vì 2.624.

**Cảnh báo chia tập:** 130 peptide có **cả hai** nguồn nhãn. Chúng phải nằm **cùng một phía**
train/test, nếu không thì rò rỉ giữa hai nhiệm vụ. Nếu bộ bão hòa được dùng để huấn luyện thì
**không được** tiếp tục gọi 249 peptide đó là test độc lập.

## 7. Sàng peptidome GPS, và **mô hình học máy của chính tác giả**

Script: [gps_peptidome_audit.py](gps_peptidome_audit.py) → [gps-peptidome-audit.json](gps-peptidome-audit.json).

File Mendeley 393 MB lần đầu có trên máy chứa, ngoài 18 file count và bảng PSI đầy đủ của ba điều kiện,
hai file **dự đoán PSI toàn peptidome bằng học máy do chính nhóm Zhang làm**, huấn luyện trên 5% và 10%
dữ liệu, phủ hoàn toàn.

| Phép đo | Kết quả |
|---|---:|
| SVM tác giả, 10% train: Pearson · RMSE (260.989 peptide) | **0,8955** · 0,563 |
| SVM tác giả, 5% train: Pearson · RMSE | 0,8916 · 0,5708 |
| Cột `replicate.error` của tác giả: trung vị \|sai số\| | 0,239 **[nguồn]** |
| Control rep1 vs rep2: Pearson · SD nhiễu một replicate (343.236 peptide) | 0,9304 · **0,3357** |
| MLN4924: peptide bền lên ≥ 1 PSI khi chặn CRL | **1.978 / 260.989 = 0,76%** |

**[đo]** trừ dòng ghi **[nguồn]**.

**[phân tích] Ba hệ quả:**

1. **Thẻ đề tài đánh giá G3 chưa đầy đủ.** Nó liệt kê DEGRONOPEDIA, MetaDegron, Colab của nhóm PAP, nhưng
   **không biết** Zhang 2023 đã kèm mô hình dự đoán PSI trên chính bộ dữ liệu đề tài dùng. Phải nêu
   baseline này. Lưu ý **phạm vi khác nhau**: nó dự đoán PSI mức **peptide**, còn đề tài nhắm footprint và
   hiệu ứng đột biến mức **residue** — khác nhiệm vụ, nên không phải đối thủ trực tiếp, nhưng không được
   bỏ qua khi phát biểu tính mới.
2. **Nhiễu ~0,30–0,34 được xác nhận lần thứ ba, độc lập.** Bộ quét cho 0,2974, bộ bão hòa 0,2645,
   peptidome 0,3357, và chính tác giả ghi 0,239. Bốn con số cùng cỡ ⇒ đây là tính chất của assay GPS.
3. **RMSE của SVM (0,563) lớn hơn nhiễu replicate (0,336)** ⇒ ở mức peptide vẫn còn dư địa, nhưng mô hình
   tác giả đã khá sát trần nhãn.

## 8. MaveDB

Script: [mavedb_audit.py](mavedb_audit.py) → [mavedb-audit.json](mavedb-audit.json).

26 score set của 9 gene, 160.491 dòng, **76.194 biến thể duy nhất** sau khử trùng lặp theo khóa HGVS
trong từng gene (loại `_wt`, `_sy`). **[đo]** Con số 69.209 ở audit 11/10 tính từ metadata API trên tập
score set nhỏ hơn; con số mới tính trên bảng điểm thật đã tải. Trùng lặp dồn ở LDLR (23.856 dòng bị gộp),
GCK (17.330) và PTEN (16.090).

## 9. Đề xuất — **chờ Trọng xác nhận**, chưa phải quyết định

**[đề xuất]**

1. **Sửa cách phát biểu mục tiêu G2 ở thẻ đề tài.** Thay "vượt 0,6045, +28,9% tương đối nếu đạt trần"
   bằng: baseline thành phần huấn luyện công bằng **0,4897**, mục tiêu vượt mốc đó, và **báo kèm trần
   nhãn 0,6514** để người đọc biết giới hạn trên. Lý do: 0,7792 và 0,6045 đều là oracle đọc nhãn test.
2. **Chuyển trọng tâm nhãn sang bộ bão hòa**, dùng bộ quét làm nguồn phụ và để mở rộng độ phủ. Lý do:
   nhiễu 16,7% so với 75,9%, Jaccard 0,66 so với 0,50, và ma trận 28×19 phủ 97,9%. Rủi ro phải nhận:
   chỉ 235 peptide, nên tập test nhỏ — cần tính lại lực riêng cho thiết kế này **trước khi** cam kết.
3. **Dùng nhãn trung bình hai replicate** thay vì một replicate, và **báo trần nhãn** trong mọi bảng kết
   quả. Lấy trung bình giảm phương sai nhiễu bốn lần so với một phép đo đơn.
4. **Chọn split theo cụm protein coverage 80%** (271–322 footprint) thay vì 50%, để lực đạt 0,92–0,94.
5. **Giữ 130 peptide có cả hai nguồn nhãn cùng một phía** train/test, và ghi rõ điều này trong thiết kế
   benchmark.
6. **Nêu SVM của Zhang 2023 trong phần G3 và trong đề cương**, kèm làm rõ khác biệt phạm vi
   peptide/residue.
7. **Không dùng mẫu BAG6 WT trộn với hai replicate kia.** ΔPSI của nó chỉ tương quan 0,56–0,58 với hai
   replicate (so với 0,72 giữa hai replicate đó), và lệch hệ thống −0,11 PSI. Nếu dùng, phải coi là điều
   kiện riêng.

## 10. Chạy lại

Từ thư mục gốc repo, môi trường `.venv` đã cài `requests` (các script phân tích chỉ dùng thư viện chuẩn):

```bash
.venv/bin/python topics/degron-footprint/research/full-data-audit/fetch_all.py
cd topics/degron-footprint/data && mkdir -p interim/zhang-scanning-unzip interim/zhang-saturation-unzip interim/zhang-gps-unzip
unzip -oq "raw/I28 Scanning Mutagenesis.zip" -d interim/zhang-scanning-unzip
unzip -oq "raw/I28 CRL Saturation Mutagenesis.zip" -d interim/zhang-saturation-unzip
unzip -oq "raw/I28 GPS Peptidome Screen and MLN4924 and SVM.zip" -x "*.xlsx" -d interim/zhang-gps-unzip
cd ../../..
.venv/bin/python topics/degron-footprint/research/full-data-audit/build_psi.py --condition all --validate
.venv/bin/python topics/degron-footprint/research/full-data-audit/replicate_audit.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/label_ceiling.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/power_analysis.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/read_depth_sweep.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/saturation_audit.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/saturation_matrix.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/gps_peptidome_audit.py
.venv/bin/python topics/degron-footprint/research/full-data-audit/mavedb_audit.py
```

Mọi script cố định seed 0 ở chỗ có ngẫu nhiên (phá tie trong precision@3). Dữ liệu thô và bảng dẫn xuất
nằm trong `topics/degron-footprint/data/`, bị `.gitignore` chặn; chỉ file JSON kết quả nhỏ lên git.

## 11. Đã kiểm những gì

- Tái lập PSI của tác giả trên 261.865 giá trị, lệch ≤ 5,0 × 10⁻⁷; truy nguyên đủ ba định danh lệch về
  một nguyên nhân duy nhất (lỗi header) và kiểm bằng cách mô phỏng lại đúng lỗi đó.
- Tái lập đúng **2.624** footprint ở Replicate 1, khớp số đã biết của repo.
- Kiểm giả định "hai nửa bão hòa là hai replicate" bằng tương quan 0,9544 trước khi dùng.
- Kiểm quy tắc tile hai lần: so trình tự thật (128/130) và so PSI của ô WT-nội-tại với WT bộ quét.
- SHA-256 mọi file Mendeley khớp checksum do Mendeley công bố; commit Voutsinos khớp hash đã ghim.
- **Không huấn luyện mô hình nào.** Mọi "trần" và "oracle" đều là đại lượng tính từ nhãn, đã nói rõ.

## 12. Những gì vẫn chưa làm

- Chưa dùng `GSE240610_RAW.tar` và 18 file count của sàng peptidome để dựng lại PSI từ read thô
  (đã có bảng PSI của tác giả nên chưa cần).
- Chưa tải read giải trình tự thô (SRA `PRJNA1277273`, FASTQ của Zhang).
- Chưa chạy lại baseline PAP của Voutsinos sau khi tải lại repo; các số ở
  [voutsinos-2026-audit](../voutsinos-2026-audit/README.md) là từ phiên 11/10, chưa kiểm lại.
- Chưa phân tích `Degron CRISPR Screens.zip` lần này — đã làm ở [e3-labels-audit](../e3-labels-audit/README.md) 11/10.
- Chưa huấn luyện mô hình nào, nên **G2 vẫn chưa xác lập**.
