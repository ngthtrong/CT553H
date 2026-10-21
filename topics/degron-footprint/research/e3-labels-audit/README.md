# Audit nhãn E3 và nhãn theo residue của Zhang 2023

> **Cập nhật 12/10/2026:** đã tải lại hai ZIP scanning/saturation vào `topics/degron-footprint/data/raw/`, pin SHA-256 và chạy [audit thành phần–ngữ cảnh](../composition-context-audit.md). **2.046/2.624** footprint có vị trí cùng cặp thay thế nhưng chênh ΔPSI ≥1,0; cận kỳ vọng P@3 của score chỉ dựa thành phần là **0,6045**, oracle không ràng buộc là **0,7792**. Với cụm protein identity 30%, coverage hai chiều 50%, test khớp tham chiếu còn **221–301 footprint** qua 5 seed. Các nhận định cũ bên dưới rằng bất biến hoán vị khiến mô hình không thể dự đoán footprint **không đúng**; đọc báo cáo mới trước khi dùng lập luận đó. Gom theo cặp (WT, replacement), không chỉ WT, vì dữ liệu có ngoại lệ ở vị trí 25–27. 135.040 là số **định danh**, chưa phải số ΔPSI đã curate.

> Ngày: **11/10/2026**. Mục đích: qua **cổng chặn số 2** của đề tài [`degron-e3-specificity`](../topic-decision.md) — đếm nhãn E3/adaptor **thực sự dùng được** thay vì dẫn lại con số "16 E3" từ bài báo.
>
> Kết luận ngắn: **cổng 2 KHÔNG QUA** cho thành phần có điều kiện E3, nhưng **nhãn theo residue lớn hơn tài liệu trước của repo ghi rất nhiều**. Chi tiết ở mục 3 và 4.

## 1. Nguồn dữ liệu, và vì sao không lấy từ Supplementary của tạp chí

Bài: Zhang và cộng sự, *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*, **Molecular Cell** 2023, [doi:10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022) (PMC10594193; PMC10688572 là thông báo đính chính, không phải bài).

Table S1–S7 trên PMC **tải không được**: endpoint `/bin/NIHMS1932106-supplement-*.xlsx` trả về trang `Checking your browser - reCAPTCHA`. Europe PMC trả `Article with id PMC10594193 is not open access one`. Nguồn thay thế **dùng được** là Mendeley Data mà chính bài khai báo:

| Nguồn | Nội dung | Kích thước | SHA-256 (32 ký tự đầu) |
|---|---|---|---|
| [Mendeley 10.17632/32h94v2yv2.2](https://data.mendeley.com/datasets/32h94v2yv2/2), `Degron CRISPR Screens.zip` | MAGeCK + count của mọi screen CRISPR | 2.595.159 B | `b30d422d6b9a515a35b3092099314221` |
| cùng nguồn, `I28 CRL Saturation Mutagenesis.zip` | reads đột biến bão hòa, 12 mẫu | 5.224.902 B | `cbda58342265dd73b7946cd091c5b558` |
| cùng nguồn, `I28 Scanning Mutagenesis.zip` | reads + **CSV đã tính PSI** cho đột biến quét | 27.939.862 B | `a82bd1ee4bc7a2da69df06cb44dd34fe` |
| [Zenodo 8103915](https://doi.org/10.5281/zenodo.8103915) | mã DegronID | 148.330 B | `60cadd70023406a3fb90e7f6c30c0dc9` |

**Zenodo chỉ có mã, không có nhãn E3** — 15 file, trong đó dữ liệu duy nhất là `example_pssm.rds` và hai FASTA ví dụ. Không dùng được để đếm.

Còn một nguồn **chưa lấy được**: **Table S5** (peptide clone riêng theo DN CUL, cột 4–5 ghi *"the identity of the experimentally identified E3 ligase, either by CRISPR screen or by individual testing"*). Đây là bảng gán E3 do chính tác giả curate, và là trần trên thật của số nhãn. Nó chỉ có trong Supplementary của tạp chí, nên con số ở mục 3 là **giới hạn dưới tính từ dữ liệu CRISPR thô**.

## 2. Chạy lại

Tải ba file ZIP trên vào **ba thư mục rỗng riêng biệt**, giải nén, rồi chạy từ thư mục này:

```bash
MG="<giải nén CRISPR>/Degron CRISPR (new)/MAGEcK (Completed)"
SAT="<giải nén satmut>/I28 CRL Saturation (Completed)"
SCAN="<giải nén scanmut>/I28 Scanning (Completed)/Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv"

python3 -I count_e3_labels.py  "$MG"  e3-labels-audit.json      # hit thô từng screen
python3 -I assign_e3.py        "$MG"  e3-assignment.json        # gán adaptor, loại bộ máy chung
python3 -I sweep_thresholds.py "$MG"  e3-threshold-sweep.json   # 36 tổ hợp ngưỡng
python3 -I count_satmut.py     "$SAT" satmut-audit.json         # độ phủ đột biến bão hòa
python3 -I count_scanmut.py    "$SCAN" scanmut-audit.json       # độ phủ đột biến quét
python3 -I count_footprints.py "$SCAN" footprint-audit.json     # peptide CÓ footprint học được
python3 -I overlap.py "$MG" "$SAT" "$SCAN" overlap-audit.json   # chồng lấn ba bộ
```

Chỉ thư viện chuẩn Python, không cần cài gì. Mọi ngưỡng ghi tường minh trong file JSON kết quả.

## 3. Cổng chặn 2: nhãn E3 — **KHÔNG QUA**

### 3.1 Phương pháp gán

Tế bào được sort theo tỉ lệ GFP/DsRed **cao**, nên sgRNA làm peptide **bền hơn** sẽ giàu lên ở mẫu sort → dùng cột `pos|` của MAGeCK. Ngưỡng: `pos|fdr ≤ 0,10`, `pos|lfc ≥ 1,5`, `pos|goodsgrna ≥ 4`.

Bộ máy chung của con đường bị loại theo **danh sách tường minh** (proteasome `PSM*`, neddylation `NAE1`/`NEDD8`/`UBE2M`, scaffold `CUL*`/`RBX1`/`SKP1`/`DDB1`, `ARIH1/2`, COP9, `VCP`/`NPLOC4`, vài thành phần tái diễn như `UBL5`, `PSMG3`). **Không loại theo tần suất** — vì một adaptor thật có thể là hub nhận nhiều peptide, và KLHL15 đúng là như vậy trong chính bài báo. Lần chạy đầu dùng quy tắc tần suất đã **loại oan KLHL15 (13/31 screen)**; đã sửa.

Ghi chú: `APPBP2` xuất hiện ở ~17/31 screen nhưng `lfc` chỉ 0,8–1,6 nên tự rơi dưới ngưỡng. Bài báo cũng tự thừa nhận *"bench-top contamination of pre-cloned sgRNAs were observed"* ở một số lô.

### 3.2 Kết quả

| | Số đếm |
|---|---:|
| Screen CRISPR trong dữ liệu (trừ 3 control) | **31** |
| Gán được một adaptor | **27** |
| Gán được **rõ** (margin ≥ 0,5 và không có hit ngoài họ adaptor mạnh hơn) | **25** |
| Không gán được | 4 (`AGRN_82`, `CDC6_1`, `MDN1_196`, `NANOS3_5`) |
| **Số E3 khác nhau** | **10** |

Phân bố peptide trên mỗi E3 — **đây là con số giết thành phần có điều kiện E3**:

| E3 | Số peptide |
|---|---:|
| **KLHL15** | **13** |
| BAG6 | 4 |
| ASB7 | 2 |
| FEM1B | 2 |
| ASB3 (`GPR75-ASB3`), KLHL9, FBXW5, FBXO21, FBXO38, DCAF5 | **1 mỗi cái** |

Hai cờ cảnh báo: `ALAS2_8` → KLHL15 nhưng `TRPC4AP` mạnh hơn (3,79 so với 3,42); `HINFP_3` → FBXW5 nhưng `VAV2` mạnh hơn (2,47 so với 2,41).

### 3.3 Độ bền theo ngưỡng — 36 tổ hợp

Quét `fdr ∈ {0,05; 0,10; 0,25}` × `lfc ∈ {1,0; 1,5; 2,0; 2,5}` × `goodsgrna ∈ {3,4,5}`:

| Đại lượng | Biên độ trên 36 tổ hợp |
|---|---|
| Peptide gán được | **16–29** trên 31 |
| Số E3 khác nhau | **8–10** |
| **Số E3 có ≥ 5 peptide** | **luôn đúng bằng 1** |
| Số E3 có ≥ 10 peptide | 0 hoặc 1 |
| E3 có 1 peptide duy nhất | 4–6 |

**Kết luận.** Không có ngưỡng nào làm con số khá hơn. Chỉ có **một** lớp E3 đủ mẫu để huấn luyện, và 6 lớp có đúng một mẫu. Thành phần 3 của kiến trúc CMIL-E3 (vector điều kiện E3 sinh từ trình tự miền nhận cơ chất, điều biến kiểu FiLM) **không huấn luyện được trên bộ nhãn này**, và không khái quát được sang E3 mới vì chỉ có 10 E3 để học quan hệ trình tự–đặc hiệu.

Cách phát biểu đúng từ nay: **không nói "16 E3 có nhãn CRISPR" như thể đó là 16 lớp dùng được.** Con số cần nói là **số peptide trên mỗi E3**, và nó là 1–13.

## 4. Phát hiện ngoài dự kiến: nhãn theo residue lớn hơn tài liệu repo ghi

### 4.1 Đột biến quét (scanning) — nguồn chính

Từ `I28 Scanning Mutagenesis Replicate 1.csv`, 283.880 dòng, có cột PSI sẵn (thang 1–6, **thấp = bị phân hủy nhanh**):

| | Số đếm |
|---|---:|
| Dòng có PSI | 261.866 |
| Dòng có PSI **và** `Sum ≥ 10` | **256.711** |
| Peptide trong thư viện | 9.817 |
| Peptide có cả hoang dã và biến thể được chấm | **8.831** |
| Peptide có ≥ 24 trong 28 vị trí được chấm | 8.877 |
| Vị trí/peptide | min 1 · median **28** · mean 26,4 |

### 4.2 Bao nhiêu peptide **thực sự có footprint học được**

Định nghĩa tường minh: peptide là degron nếu PSI hoang dã ≤ 3,0; "có footprint" nếu tồn tại ≥ 1 vị trí mà đột biến làm PSI **tăng** ≥ 1,0 (phá degron thì peptide bền lên).

| | Số đếm |
|---|---:|
| Peptide có hoang dã + biến thể | 8.831 |
| Là degron (PSI hoang dã ≤ 3,0) | **3.439** |
| Degron **và** phủ ≥ 21 vị trí | 3.415 |
| **Degron, đủ phủ, và có footprint** | **2.624** |
| Trong đó footprint **khu trú** (≤ 6 vị trí quan trọng) | **2.402** |

Phân bố trong nhóm có footprint: số vị trí quan trọng median **3** (p25 = 2, p75 = 4); ΔPSI lớn nhất median 1,53; biên độ PSI trong peptide median 2,04.

Độ nhạy theo ngưỡng:

| PSI hoang dã ≤ | ΔPSI ≥ | Số degron | Số có footprint |
|---:|---:|---:|---:|
| 2,5 | 0,5 / 1,0 / 1,5 | 2.069 | 1.980 / 1.576 / 849 |
| 3,0 | 0,5 / 1,0 / 1,5 | 3.415 | 3.275 / **2.624** / 1.381 |
| 3,5 | 0,5 / 1,0 / 1,5 | 4.572 | 4.376 / 3.414 / 1.728 |

**Median 3 vị trí quan trọng trên 28** là con số quan trọng nhất của toàn bộ audit này: tín hiệu **khu trú thật**, trong khi mô hình tốt nhất hiện có bất biến hoán vị (Pearson gốc–đảo = 1,000000) nên về nguyên lý không biểu diễn được nó.

### 4.3 Đột biến bão hòa (saturation) — bản đồ đầy đủ 19 thay thế

| | Số đếm |
|---|---:|
| Peptide | **249** |
| Định danh biến thể | **135.040** |
| Biến thể/peptide | median **560** (= 28 vị trí × 20 ký hiệu) |
| Peptide có ≥ 27 vị trí, sau lọc reads ≥ 10 | **239** |
| Tổng reads | 121.498.124 |

Bài báo nói "219 footprint độ phân giải cao" — đó là tập do tác giả curate. Dữ liệu thô đỡ được **239–247** peptide với độ phủ gần đủ.

### 4.4 Chồng lấn ba bộ

| | Số đếm |
|---|---:|
| Peptide CRISPR có đột biến bão hòa | **27 / 31** |
| Peptide CRISPR có đột biến quét | 29 / 31 |
| Peptide CRISPR có **cả hai** | **25** |
| Peptide bão hòa có trong bộ quét | 130 / 248 |

Bốn peptide CRISPR không có đột biến bão hòa đúng là bốn peptide **BAG6** (`ANKRD27_23`, `CD68_8`, `CDHR4_23`, `CFB_17`) — khớp với việc BAG6 nằm ở screen riêng (Table S4), không phải CRL.

**Hệ quả dùng được:** có **23 peptide đồng thời được gán E3 và có bản đồ đột biến bão hòa**. Hai số 27 ở bảng trên là hai tập khác nhau: 4 peptide BAG6 được gán E3 nhưng không có bản đồ bão hòa; 4 peptide có bản đồ bão hòa (`AGRN_82`, `CDC6_1`, `MDN1_196`, `NANOS3_5`) không được gán E3. Đủ làm **ca nghiên cứu nhỏ**, không đủ làm tập huấn luyện mô hình có điều kiện.

Kiểm lại từ hai JSON audit đã lưu:

```bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path('topics/degron-footprint/research/e3-labels-audit')
assignments = json.loads((root / 'e3-assignment.json').read_text())['assignment']
overlap = json.loads((root / 'overlap-audit.json').read_text())
assigned = {name for name, value in assignments.items() if value['e3'] is not None}
saturated = set(overlap['crispr_with_satmut'])
print(len(assigned), len(saturated), len(assigned & saturated))  # 27 27 23
PY
```

## 5. Đọc công trình gần nhất có thể trùng ý tưởng

### 5.1 Zhang 2023 — chính bài cho dữ liệu, đã đọc toàn văn

Mô hình của họ: **SVM trên thành phần acid amin** (dự đoán PSI của toàn bộ ~260K peptidome làm tập kiểm tra), cộng **DegronID** — thuật toán **chấm độ giống motif bằng PSSM** dựng từ footprint, rồi gom cụm thứ bậc thành 40 nhóm. DegronID **không** dự đoán bản đồ đột biến từ trình tự; nó dùng footprint **đã đo** làm truy vấn để tìm peptide giống trong thư viện.

Tự nhận giới hạn, trích đúng: *"Thirty-one peptides were missed either because of low representation or because they possessed multiple degrons which cannot be easily disambiguated."*

Việc họ **chưa** làm: không có mô hình dự đoán độ nhạy đột biến theo từng residue từ trình tự; không dùng PLM; không có mô hình có điều kiện E3.

### 5.2 Bài transcription factor 05/2025 (cùng nhóm Copenhagen) — đã đọc toàn văn

Không mô hình hóa đặc hiệu E3, không kiến trúc mới, không XAI. Đột biến **thực nghiệm** của họ là **có đích, không bão hòa** (xóa đoạn ở ASCL1 23–40 và HSF1 198–217, đột biến điểm ZNF140 H323Y). Bản đồ thay thế đầy đủ của họ là **in silico** (ΔPAP), không phải đo.

### 5.3 Tra cứu tiền lệ cho bài toán đã tái định tâm

Không tìm được công trình nào dự đoán **bản đồ độ nhạy đột biến theo residue cho degron** từ trình tự. Các mô hình degron đã có đều ở mức peptide hoặc protein, và phần lớn dựa trên **thành phần**:

| Mô hình | Biểu diễn | Mức dự đoán |
|---|---|---|
| PAP (2026) | `Conv1D(kernel=1)` + gộp trung bình | peptide, điểm khối — **bất biến hoán vị** |
| Zhang SVM (2023) | 20 đặc trưng thành phần | peptide |
| QCDPred (nấm men) | hồi quy logistic trên thành phần | tile |
| Degpred (2022) | BERT + BiLSTM | peptide/protein |
| MetaDegron (2024) | SeqVec + BLSTM (D) và XGBoost 10 đặc trưng (X), hai route riêng | hit motif/cửa sổ, 21 lựa chọn E3 qua regex, **một** classifier dùng chung (đính chính 21/10, [audit](../metadegron-analysis-2026-10-21/README.md)) |
| deepDegron (2021) | mạng sâu trên trình tự | chỉ hai đầu chuỗi |

Tiền lệ gần nhất về **phương pháp luận** nằm ngoài bài toán degron: một khung học máy 2025 báo rằng **6 điểm thay thế mỗi residue là đủ để suy ra phần còn lại với độ chính xác ~90%** trên dữ liệu quét đột biến sâu nói chung. Phải trích bài này nếu đặt đóng góp ở trục "dự đoán bản đồ thay thế", vì nó là phản biện trực tiếp về tính mới của ý tưởng.

## 6. Hệ quả cho đề tài — và điều phải quyết

**Chết:** thành phần 3 (điều kiện E3 kiểu FiLM) và việc đặt "đặc hiệu E3" làm **thước đo chính**. Chỉ 1 lớp E3 đủ mẫu, 6 lớp có 1 mẫu.

**Sống, và mạnh hơn tưởng:** bài toán **dự đoán footprint theo residue** — 2.624 peptide có footprint học được (2.402 khu trú), 256.711 phép đo theo residue, cộng 249 bản đồ thay thế đầy đủ (135.040 phép đo) làm tập kiểm tra độ phân giải cao. Median 3 vị trí quan trọng trên 28 là lý do nguyên lý khiến mô hình bất biến hoán vị không làm được.

**Giữ được ở quy mô nhỏ:** 23 peptide có cả nhãn E3 và bản đồ đột biến bão hòa → ca nghiên cứu; cả 13 peptide được gán KLHL15 nằm trong giao này, là lớp duy nhất đạt ngưỡng 5. Vẫn cần lọc chất lượng nhãn và chia tập trước khi chấm điểm.

Quyết định thuộc về sinh viên, không phải của ghi chú này. Ba lựa chọn đã trình bày ở [nhật ký](../../../../journal/README.md).
