# Thực hiện C-15: giảm rủi ro nhiệm vụ mức residue, và con số dương đầu tiên

> Ngày **15/10/2026 (phiên 8)**. Chạy theo yêu cầu của Trọng: *tiến hành thực hiện đề xuất C-15,
> nghiên cứu thêm để giảm thiểu rủi ro và trình bày được đóng góp rõ ràng*.
> Quyết định chấp nhận C-15 ghi ở D-031.
>
> Script: [residue_data.py](residue_data.py) (nạp nhãn) · [derisk.py](derisk.py) (sáu lệnh con).
> Kết quả: [ladder.json](ladder.json) · [identify.json](identify.json) · [model.json](model.json) ·
> [ceiling.json](ceiling.json) · [power.json](power.json) · [headline.json](headline.json).

## Nhãn bằng chứng
**[đo]** tự chạy phiên này, có lệnh tái lập · **[nguồn]** số của tác giả · **[phân tích]** suy luận ·
**[đề xuất]** chờ Trọng xác nhận · **[chưa xác minh]** chỉ thấy qua tóm tắt tìm kiếm.

---

## 0. Kết luận một màn hình

| Việc C-15 đặt ra | Trạng thái sau phiên này |
|---|---|
| **Việc chặn: lực trên n = 91 + đếm cụm** | ✅ **Xong, và rủi ro nhỏ hơn đã tưởng nhiều.** 91 peptide = **89 cụm** cov80; mức chênh nhỏ nhất phát hiện được là **0,0123** AUROC (không phải 0,071), lực tại delta đo được là **0,995** |
| **Rủi ro LeBlanc "thành phần > vị trí"** | ✅ **Đã khoanh bằng số.** Đổi nhãn từ mức peptide sang hiệu ứng đột biến đưa tỉ lệ hệ số ngữ cảnh tách được khỏi 0 từ **28,9% → 53,3%**, đồng thuận dấu **0,684 → 0,90**, và tỉ lệ áp đảo của thành phần từ **≈ 56× → 2,2×** |
| **Con số dương cho G2** | ✅ **Có.** Ngữ cảnh cục bộ đáng **+0,0289** AUROC so với lớp mô hình chỉ-thành-phần (CI [0,0264; 0,0313]) và **+0,0300** so với **ΔPAP `cnn2w7`** — mô hình degron công bố gần nhất (CI [0,0234; 0,0366], 2.064 peptide, 1.471 cụm) |
| **Việc của kiến trúc** | ⚠ **Định nghĩa lại, hẹp hơn và kiểm được.** Trên **ma trận bão hòa**, mô hình của repo **vẫn thua ΔPAP −0,0420** (CI [−0,0580; −0,0256]). Đây là mục tiêu G2 cụ thể, thay cho phát biểu "MIL so với đầu theo vị trí" chưa có lý do |

**Một điều phải nói kèm mọi lần dùng con số +0,0300:** ΔPAP là mô hình huấn luyện cho **độ dồi dào của
tile 30-mer**, nên ở đây nó **bị dùng ngoài mục đích**. Thắng nó **không** phải thắng một mô hình được
huấn luyện cho nhiệm vụ này — **không có** mô hình nào như thế, và đó chính là khoảng trống đề tài tuyên bố.
Mốc M0 chỉ-thành-phần **hoà** ΔPAP `cnn2w7` (+0,0008, CI [−0,0057; 0,0074]) cho thấy rào này **thấp**.

---

## 1. Thiết kế: hai nguồn nhãn mức residue, không phải một

D-028 mục 5 nói bộ bão hòa là nguồn **duy nhất** đỡ được mức residue.
Phép đo phiên này cho thấy phát biểu đó cần **nói chính xác hơn**: có **hai** nguồn nhãn **hiệu ứng đột
biến**, và chúng có hai vai khác nhau. **[đo]**

| | **Bộ quét** (scanning) | **Bộ bão hòa** (saturation) |
|---|---|---|
| Nhãn | ΔPSI so với PSI hoang dã đo trực tiếp | ΔPSI so với WT nội tại (trung vị ô đồng nghĩa), hai nửa độc lập |
| Thiết kế thay thế | **1 thay thế mỗi vị trí**, gần như toàn bộ là **→R** (20 cặp (WT, đột biến) khác nhau) | **19 thay thế mỗi vị trí** — ma trận đầy |
| Peptide degron (PSI WT ≤ 3,0) | **2.994** | **91** |
| Cụm protein cov80 | **1.985** | **89** |
| Ô | **83.446** | **47.847** |
| Tỉ lệ ô dương | 0,0895 | 0,1310 |
| Trần **đo lường**, AUROC mức ô | **0,9458** (rep1 chấm nhãn rep2) | **0,9519** (nửa A chấm nhãn nửa B) |
| Vai | **cỡ mẫu và trục ngữ cảnh** | **ma trận thay thế** và xác nhận chuyển nguồn |

Chồng lặp: **61/89 cụm** của bộ bão hòa cũng có trong bộ quét (42 peptide trùng tên), nên mọi phép chuyển
nguồn phải **loại cụm trùng khỏi tập huấn luyện** — đã làm.

**[phân tích] Hệ quả cho cách viết:** câu "n = 91 là cỡ mẫu của phần mức residue" **không đúng**. Cỡ mẫu
của **trục ngữ cảnh** là 1.985 cụm; n = 91 chỉ là cỡ mẫu của **phần ma trận 19 thay thế**.

---

## 2. Việc chặn thứ nhất: đơn vị suy luận và lực trên n = 91 **[đo]**

### 2.1 Đơn vị suy luận hầu như không phạt gì

Cảnh báo phiên trước: *"đơn vị suy luận là cụm protein, không phải peptide; bỏ qua lồng nhau cho tỉ lệ dương
giả trên 45%"*. Đếm thật:

| Ngưỡng PSI WT | Peptide | Protein | **Cụm cov80** | Ô | Trần AUROC |
|---:|---:|---:|---:|---:|---:|
| ≤ 2,5 | 9 | 9 | 9 | 4.531 | 0,9471 |
| **≤ 3,0** | **91** | **91** | **89** | **47.847** | **0,9519** |
| ≤ 3,5 | 141 | 141 | 137 | 74.081 | 0,9504 |
| ≤ 4,0 | 176 | 176 | 172 | 92.337 | 0,9501 |
| không ngưỡng | 235 | 233 | 227 | 122.412 | 0,9500 |

91 peptide nằm trên **91 protein khác nhau** và **89 cụm** — thư viện bão hòa chọn mỗi protein một peptide,
nên **lồng nhau ở mức protein gần như không tồn tại**. Phạt thật nằm ở **ô lồng trong peptide**:
ICC = **0,0625**, cỡ cụm trung bình 526 ⇒ hệ số thiết kế **33,79**, tức **≈ 1.416 ô độc lập hiệu dụng**,
không phải 47.847 — và cũng không phải 91.

### 2.2 Lực: mức chênh nhỏ nhất phát hiện được là **0,0123**, không phải 0,071

SD lấy từ **chính chênh lệch ghép cặp giữa hai mô hình thật** (không phải SD của nhãn), bootstrap **theo
cụm**, 4.000 lần, 89 cụm:

| Phép so trên bộ bão hòa | Delta đo được | CI 95% | SE theo cụm | **MDE ở lực 80%** | Lực tại delta đo được |
|---|---:|---|---:|---:|---:|
| M1 (chỉ số vị trí) − M0 | +0,0123 | [0,0046; 0,0199] | 0,0040 | **0,0112** | 0,868 |
| M2 (thành phần cửa sổ) − M0 | +0,0170 | [0,0087; 0,0255] | 0,0042 | **0,0118** | 0,982 |
| **M3 (ngữ cảnh có thứ tự) − M0** | **+0,0201** | [0,0117; 0,0285] | 0,0044 | **0,0123** | **0,995** |

Phép so **không** ghép cặp cần ≈ √2 lần lớn hơn: MDE **0,0491**. Vẫn **dưới** 0,071.

**[phân tích] Con số 0,071 của phiên trước sai ở đâu.** Nó là MDE suy từ **phương sai mức peptide không ghép
cặp**. Nhưng thiết kế thật là **ghép cặp**: mỗi peptide cho một AUROC từ ~526 ô, nên phương sai của *chênh
lệch* nhỏ hơn phương sai của *mức* rất nhiều. ⇒ **Cam kết trước được**: ablation **≥ 0,012** phân biệt được
trên n = 91; ablation **dưới 0,012** thì **không**, và phải nói trước điều đó thay vì báo p-value sau.

Bộ quét để so: 1.599 cụm ⇒ SE 0,0009–0,0013, **MDE 0,0025–0,0036**.

---

## 3. Việc chặn thứ hai: rủi ro LeBlanc, đo trên **đúng loại nhãn** **[đo]**

reframe §11.2 đã xác nhận rủi ro LeBlanc **là thật** — nhưng trên
nhãn **PSI mức peptide**. Phiên này chạy **đúng khuôn đó** (bootstrap theo cụm, |μ|/SD từng hệ số, đồng
thuận dấu) trên nhãn **hiệu ứng đột biến**, với véc-tơ trọng số **ngữ cảnh cục bộ** (6 lệch vị trí × 20 acid
amin, cửa sổ ±3).

| Nhãn | Véc-tơ | |μ|/SD trung vị | % hệ số > 2 | Đồng thuận dấu | Tái lập nửa–nửa |
|---|---|---:|---:|---:|---:|
| **PSI mức peptide** (§11.2, 43.635 peptide) | 560 ô (vị trí, acid amin) | 1,24 | **0,289** | **0,684** | 0,9801 |
| | tổng theo acid amin | 69,02 | 1,000 | 1,000 | 1,0000 |
| **Hiệu ứng đột biến, bộ quét** (2.994 peptide / 1.985 cụm) | 120 ô **ngữ cảnh** | **2,31** | **0,533** | **0,900** | 0,9943 |
| | tổng theo acid amin | 5,13 | 0,850 | 0,988 | 0,9994 |
| | cặp thay thế (40) | 8,72 | 0,550 | 0,817 | 1,0000 |
| **Hiệu ứng đột biến, bộ bão hòa** (91 peptide / 89 cụm) | 120 ô **ngữ cảnh** | 1,25 | 0,250 | **0,840** | 0,9703 |
| | cặp thay thế (40) | 6,36 | **0,925** | 0,976 | 0,9983 |

**[phân tích] Ba điều đọc được, và cả ba đều đổi thế của đề tài:**

1. **Đổi nhãn làm tham số vị trí nhận diện được rõ hơn.** 28,9% → **53,3%** ô tách khỏi 0; đồng thuận dấu
   0,684 → **0,90**. Trên nhãn mức peptide, thành phần ổn định hơn vị trí **≈ 56 lần** (69,02 / 1,24); trên
   nhãn hiệu ứng đột biến tỉ lệ đó còn **2,2 lần** (5,13 / 2,31). **Đây là lý lẽ bằng số cho C-15**, không
   phải niềm tin.
2. **Kết luận của LeBlanc 2026 không bị bác, nó bị khoanh lại.** *"Thành phần quan trọng hơn từng vị trí"*
   vẫn đúng ở mức tham số, trên **nhãn mức peptide/tile**. Phát biểu đúng mức của đề tài:
   *"đúng với nhãn mức tile; với nhãn hiệu ứng đột biến, tỉ lệ áp đảo giảm từ ≈ 56× xuống 2,2× — đã đo"*.
3. **Bộ bão hòa một mình thiếu lực cho tham số ngữ cảnh** (25% ô, 89 cụm) nhưng **rất đủ cho ma trận thay
   thế** (92,5% hệ số cặp tách khỏi 0, cao nhất bảng). ⇒ Thiết kế bắt buộc: **học trục ngữ cảnh trên bộ
   quét, xác nhận ma trận trên bộ bão hòa.** Không phải chọn một trong hai.

---

## 4. Con số dương đầu tiên trên nhiệm vụ mức residue **[đo]**

Năm mô hình, cùng ridge (alpha chọn bằng PRESS/LOO giải tích), cùng đặc trưng nền, chia **theo cụm protein
cov80**, 5 fold × 5 seed, chấm bằng **AUROC mức ô trung bình macro theo peptide**.

| | Khối đặc trưng thêm vào | Cột | AUROC bộ quét | SD qua seed |
|---|---|---:|---:|---:|
| **M0** | *chỉ thành phần*: one-hot WT + one-hot đột biến + thành phần peptide | 60 | **0,8393** | 0,0002 |
| M1 | + chỉ số vị trí 1…28 | 88 | 0,8445 | 0,0002 |
| M2 | + **thành phần cửa sổ ±3 (không thứ tự)** | 80 | 0,8625 | 0,0002 |
| **M3** | + **ngữ cảnh ±3 có thứ tự** | 180 | **0,8682** | 0,0003 |
| M4 | + ngữ cảnh ±3 **và** chỉ số vị trí | 208 | 0,8684 | 0,0001 |
| | *trần **đo lường** (rep1 chấm nhãn rep2)* | | *0,9458* | |

Ghép cặp theo peptide, bootstrap theo cụm (1.599 cụm, 2.288 peptide):

| Phép so | Delta | CI 95% | Tỉ lệ thắng | Wilcoxon |
|---|---:|---|---:|---:|
| M1 − M0 | +0,0052 | [0,0035; 0,0070] | 0,563 | 8 × 10⁻²⁰ |
| **M2 − M0** | **+0,0232** | [0,0211; 0,0251] | 0,712 | 5 × 10⁻¹²³ |
| **M3 − M0** | **+0,0289** | [0,0264; 0,0313] | 0,725 | 8 × 10⁻¹²⁹ |
| M4 − M0 | +0,0291 | [0,0266; 0,0317] | 0,728 | 2 × 10⁻¹²⁹ |

### 4.1 Khoảng trống chứng minh bằng toán nay **cũng đã được đo**

Trụ 89,7% nói lớp mô hình chỉ-thành-phần **không thể** tách các vị trí có **cùng cặp thay thế** trong một
peptide. Trên bộ quét, **68,9%** peptide có một nhóm cùng cặp bị chia dương/không-dương **[đo]**. Phiên này
đo **giá** của điều đó: **+0,0289 AUROC**, trên 1.599 cụm, CI không chứa 0. ⇒ Khoảng trống không còn chỉ là
chứng minh; nó có **một con số**.

### 4.2 Nhưng nó là **ngữ cảnh cục bộ**, không phải "vị trí" — và đây là chỗ nên nói thật

**[phân tích]** Phân rã delta cho một kết luận không đoán trước được:

| Thành phần của delta | Giá trị |
|---|---:|
| chỉ số vị trí tuyệt đối, một mình (M1 − M0) | +0,0052 |
| **thành phần cửa sổ ±3, không thứ tự** (M2 − M0) | **+0,0232** — chiếm **80%** của tổng |
| thêm thứ tự trong cửa sổ (M3 − M2) | +0,0057 |
| thêm chỉ số vị trí lên trên ngữ cảnh (M4 − M3) | **+0,0002** — bằng 0 |

⇒ Cái mua được hiệu năng là **lân cận cục bộ**, và **phần lớn là thành phần của lân cận**, không phải thứ
tự, và **không** phải vị trí tuyệt đối trong peptide. **[phân tích]** Điều này **không** chống LeBlanc 2026
mà **tinh chỉnh** nó: câu hỏi đúng không phải *"thành phần hay vị trí"* mà *"thành phần ở thang nào — cả
peptide hay lân cận ±3"*. Đề tài nên phát biểu đúng như thế; nói "mô hình vị trí thắng mô hình thành phần"
là **sai bản chất** của chính phép đo này.

### 4.3 So với mô hình degron công bố gần nhất, ghép cặp đúng tập peptide

2.064 peptide cả ba đều chấm được, 1.471 cụm:

| Phép so trên **bộ quét** | Delta | CI 95% | Tỉ lệ thắng |
|---|---:|---|---:|
| M0 − ΔPAP `cnn2w1` | +0,0421 | [0,0366; 0,0480] | 0,677 |
| **M3 − ΔPAP `cnn2w1`** | **+0,0714** | [0,0652; 0,0775] | 0,792 |
| M0 − ΔPAP `cnn2w7` | **+0,0008** | [−0,0057; 0,0074] | 0,396 |
| **M3 − ΔPAP `cnn2w7`** | **+0,0300** | [0,0234; 0,0366] | 0,576 |

ΔPAP trong cùng thước đo: `cnn2w1` **0,7943**, `cnn2w7` **0,8357** (2.064 peptide).
Trên bộ bão hòa, ΔPAP `cnn2w1` cho **0,7693** — **tái lập mốc 0,7692** của
[pap-baseline §C](../pap-baseline/README.md) ngày 14/10, và trần 0,9519 trùng tuyệt đối. Đây là phép kiểm
chéo cho thấy đường ống phiên này nối đúng với các phiên trước.

---

## 5. Chỗ mô hình của repo **vẫn thua**, và đó là mục tiêu G2 cụ thể **[đo]**

Huấn luyện **chỉ trên bộ quét** (2.849 peptide sau khi loại 145 peptide có cụm trùng), chấm trên bộ bão hòa
— tức chuyển sang **19 thay thế chưa thấy** và **cụm protein chưa thấy**:

| | AUROC mức ô trên bộ bão hòa | Spearman mức vị trí |
|---|---:|---:|
| M0 chỉ thành phần | 0,7071 | 0,4368 |
| M3 ngữ cảnh | **0,7273** | 0,4440 |
| **ΔPAP `cnn2w1`** | **0,7693** | 0,3553 **[nguồn 14/10]** |
| *trần đo lường* | *0,9519* | *0,6989* |

| Phép so, 89 cụm | Delta | CI 95% |
|---|---:|---|
| M3 − ΔPAP `cnn2w1` | **−0,0420** | [−0,0580; −0,0256] |
| M3 − ΔPAP `cnn2w7` | −0,0373 | [−0,0575; −0,0148] |

**[phân tích] Đọc đúng kết quả âm này.** Nó **không** nói hướng mức residue sai; nó nói **ba** điều cụ thể:

1. Mô hình tuyến tính học từ **một loại thay thế (→R)** không chuyển sang **19 thay thế** được tốt bằng một
   CNN học từ nhãn độ dồi dào quy mô lớn. Hợp lý, và đã lường trước.
2. Trên **thang mức vị trí** thì thứ tự **đảo**: M3 cho Spearman **0,4440** so với ΔPAP **0,3553**. Nên tuyên
   bố phải ghi rõ **theo từng thước đo**, không gộp.
3. ⇒ **Mục tiêu G2 nay là một con số, không phải một câu:** vượt **0,7693** AUROC mức ô trên bộ bão hòa,
   với trần đo lường 0,9519, và mức chênh **≥ 0,0123** là ngưỡng phát hiện được đã tính trước. Đây là phát
   biểu kiểm được, thay cho "MIL so với đầu theo vị trí" — vốn chưa có lý do.

### 5.1 Và lý do cho việc của kiến trúc nay đã có, khác lý do cũ

**[phân tích]** Tra y văn phiên này **[chưa xác minh — chỉ qua tóm tắt tìm kiếm, 15/10/2026]**: không tìm
thấy phép so trực tiếp **MIL so với đầu theo từng residue** trên cùng một nhiệm vụ mức residue; mô típ
chung trong y văn là **đầu theo residue khi có nhãn mức residue**, còn **MIL khi chỉ có nhãn mức túi**.
⇒ Đặt "MIL so với đầu theo vị trí" làm **tính mới** là **yếu**: với nhãn mức ô đã có, đầu theo vị trí là
lựa chọn tiêu chuẩn, còn MIL là lựa chọn **kém tự nhiên**.

Nhưng phép đo phiên này cho nó **một lý do thật**, và lý do đó là chuyện khác:

| Thang nhãn | Cỡ | Nhận diện được tham số vị trí? |
|---|---:|---|
| mức peptide / tile (GPS 260k, tile 212k) | **rất lớn** | **Không** (28,9%, §11.2) |
| hiệu ứng đột biến, bộ quét | 83.446 ô / 1.985 cụm | **Có** (53,3%) |
| hiệu ứng đột biến, ma trận bão hòa | 47.847 ô / **89 cụm** | cặp thay thế: có (92,5%); ngữ cảnh: yếu (25%) |

⇒ Câu hỏi kiến trúc đúng là: **nhãn mức túi (peptide/tile) dồi dào có giúp được đầu ra mức residue không,
khi đi qua một cầu nối MIL/attention — và có thắng được đầu theo vị trí huấn luyện trên nhãn mức ô ít hơn?**
Đây là **giám sát yếu**, đúng chỗ MIL sinh ra để dùng, và **câu trả lời âm cũng là kết quả dùng được** vì
§11.2 đã cho biết trước nên bi quan. Trước phiên này, phát biểu "MIL so với đầu theo vị trí" không có lý do;
nay nó có, và đi kèm một dự đoán kiểm được.

---

## 6. **[đề xuất]** Câu đóng góp, viết lại theo đúng những gì đã đo

> Chưa có mô hình nào được huấn luyện cho nhiệm vụ **hiệu ứng đột biến degron ở mức residue**: năm sản phẩm
> đã có đều xuất điểm ở mức peptide, tile hoặc motif. Em dựng **benchmark đầu tiên cho nhiệm vụ đó** — hai
> nguồn nhãn hiệu ứng đột biến với hai vai, trần **đo lường** đo được (0,9458 bộ quét / 0,9519 bộ bão hòa),
> split theo cụm protein, đối chứng là mô hình degron công bố gần nhất (ΔPAP), và **phân tích lực tính
> trước** (MDE 0,0123 ở n = 91 / 0,0036 ở 1.985 cụm) — rồi **phân rã** xem thông tin nằm ở thang nào:
> thành phần cả peptide, **lân cận ±3** (chỗ chứa 80% của +0,0289), thứ tự trong lân cận, hay vị trí tuyệt
> đối (bằng 0). Trên trục đó mô hình của em **vượt ΔPAP `cnn2w7` +0,0300** ở bộ quét, nhưng **còn thua
> 0,0420** trên ma trận bão hòa — và chính khoảng đó là việc của kiến trúc, với mục tiêu số đã ghi trước.

**Vì sao câu này mạnh hơn bản 14/10:** mọi mệnh đề đều có một con số **và** một khoảng tin cậy **và** một
ngưỡng phát hiện tính trước; chỗ chưa thắng được **nói ra** thay vì để trống; và không chỗ nào dùng
"dư địa đến trần" — trần ở đây luôn gọi là **trần đo lường**.

---

## 7. Rủi ro: trạng thái sau phiên này

| Rủi ro | Trước | Sau |
|---|---|---|
| Lực trên n = 91 | **việc chặn** | ✅ **Giải quyết.** MDE 0,0123; 89 cụm; 1.416 ô độc lập hiệu dụng |
| Đơn vị suy luận là cụm | cảnh báo "dương giả > 45%" | ✅ Ở bộ bão hòa hầu như **không phạt** (91 → 89) |
| LeBlanc "thành phần > vị trí" | **rủi ro số một, đã xác nhận là thật** | ⚠ **Khoanh được**: thật trên nhãn peptide, giảm từ 56× xuống 2,2× trên nhãn đột biến |
| Nhãn residue chỉ lặp lại ~một nửa | Jaccard 0,4965 (bộ quét) | Giữ nguyên, nhưng trần **AUROC** là 0,9458/0,9519, và đó là thước đo đã chốt (D-028 mục 2) |
| **Mới: thua ΔPAP trên ma trận bão hòa** | chưa biết | ⚠ **−0,0420.** Thành mục tiêu G2 có số |
| **Mới: "MIL so với đầu theo vị trí" là lý lẽ yếu** | ghi là "chưa tìm thấy tiền lệ" | ⚠ Phải đổi lý do sang **giám sát yếu từ nhãn mức túi** (§5.1) |
| Nguồn nhãn mức residue chỉ có một nhóm tác giả | chưa nêu | ⚠ **Mới.** Cả bộ quét và bộ bão hòa đều của Zhang 2023. Xem C-16 |

---

## 8. **[đề xuất]** → C-16: một nguồn nhãn mức residue **độc lập** đã tìm được

**[chưa xác minh — đọc PDF bản Edinburgh, chưa tải dữ liệu]** Krishna và cộng sự, *Nature Genetics* 58:366–375
(02/2026), DOI [10.1038/s41588-025-02496-5](https://doi.org/10.1038/s41588-025-02496-5): **saturation genome
editing** tại **locus nội sinh** của `CTNNB1`, đo **cả 342 đột biến missense** trên **codon 31–48** của
degron β-catenin.

Vì sao đáng giá cho đề tài **[phân tích]**:

- **Độc lập theo cả ba trục:** nhóm tác giả khác, **assay khác** (SGE nội sinh + reporter huỳnh quang, không
  phải GPS peptide), và **protein chưa thấy** — đã kiểm: `P35222` **không có** trong bảng PSI của bộ
  quét/bão hòa, và **không có** trong thư viện TF của Larsen 2025 **[đo]**.
- **Khớp đúng khuôn dữ liệu của đề tài:** codon 31–48 nằm **trọn** trong tile 2 của `P35222` (residue 24–51
  theo quy tắc `(n−1)·23`, dài 28) **[đo]** — nên dự đoán được bằng đúng mô hình 28-mer hiện có, không cần
  đổi gì.
- Và nó có **sức nặng lâm sàng**: bài dùng điểm đó tách hai phân nhóm ung thư gan.

Ba điều phải kiểm **trước** khi coi là việc:

1. **Kiểu hình khác:** readout là **tín hiệu Wnt**, không phải độ dồi dào/độ bền. Quan hệ là *gián tiếp*
   (đột biến phá degron → thoát phân hủy → tăng tín hiệu). Phải gọi đúng là **đối chứng hội tụ**, không phải
   nhãn cùng loại.
2. **Giấy phép chưa rõ.** Điểm từng biến thể nằm ở *Source data* / Supplementary của Nature Genetics; phần
   deposit công khai (GEO `GSE299075`, EGA `EGAS00001005364`) là **RNA-seq**, không phải bảng điểm. Code ở
   Zenodo `10.5281/zenodo.17940132` — ⚠ và resources §4 ghi **Zenodo trả
   403 từ mạng này**.
3. **Cỡ nhỏ:** 342 ô trên **một** degron, 18 vị trí ⇒ đủ làm **đối chứng ngoài**, **không** đủ huấn luyện.

---

## 8b. Mâu thuẫn với file slide viết cùng ngày — **đã ghi, chưa sửa**

Trong lúc phiên này chạy, một phiên khác viết
`presentation/slide-content-2026-10-15.md` (13:54). File đó
viết **trước khi** phiên này đo xong, nên có **năm chỗ** nay sai. Claude **không sửa** file trình bày khi chưa
được yêu cầu; danh sách đầy đủ nằm ở mục A của DECISIONS.md.

Chỗ **nghiêm trọng nhất**: file đó "cam kết trước" rằng MDE ở n = 91 là **≈ 0,071** và vì thế *"phần lớn
ablation sẽ không phân biệt được"*. Số đo thật là **0,0123** — nếu đem bản đó trình bày thì đề tài **tự hạ
thiết kế của mình xuống khoảng 6 lần**, và tự loại bỏ chính những ablation mà nó **có** lực để chạy.

---

## 9. Những gì phiên này **không** làm

- **Không** sửa `presentation/` (Trọng đã dặn: chỉ sửa khi được yêu cầu) — kể cả file slide viết cùng ngày
  mà §8b vừa nêu năm chỗ sai.
- **Không** huấn luyện bất kỳ mô hình phi tuyến, PLM, hay MIL nào — chỉ ridge, để delta **quy được** cho
  khối đặc trưng chứ không cho năng lực mô hình.
- **Không** huấn luyện trên ma trận bão hòa (chỉ chuyển sang nó) — đó là việc tiếp theo, và nay có mục tiêu
  số 0,7693.
- **Không** tải dữ liệu CTNNB1 (§8 là đề xuất, giấy phép chưa rõ).
- **Không** ghi gì vào `data/` — mọi lệnh phiên này **chỉ đọc**.

---

## 10. Tái lập

```bash
cd /home/ngthtrong/CT553H
.venv/bin/python -I topics/degron-footprint/research/residue-task-derisk-2026-10-15/derisk.py all
```

Sáu lệnh con chạy riêng được: `ladder`, `identify`, `model`, `ceiling`, `power`, `headline`
(`power` cần `model` chạy trước; `headline` cần cả `model` và `ceiling`). Seed 0 ở mọi chỗ.
Cần `data/interim/pap-weights/pap_weights/*.h5` cho `ceiling` — lệnh giải nén ở
[pap-baseline](../pap-baseline/README.md).

Kiểm đã làm:

- `ridge_fit` (phân rã Gram thay SVD, nhanh hơn ≈ 15 lần) khớp `sklearn.linear_model.Ridge` tới
  **7 × 10⁻¹⁴** trên ma trận có cột phụ thuộc tuyến tính **[đo]**.
- n = 91 và trần 0,9519 **tái lập đúng** [pap-baseline §C](../pap-baseline/README.md); ΔPAP `cnn2w1` trên
  bộ bão hòa cho 0,7693 so với 0,7692 đã ghi (lệch do làm tròn) **[đo]**.
- Peptide nào suy trình tự theo quy tắc tile mà **không khớp** trình tự thật trong bộ quét thì **bị loại**,
  không đoán — giữ đúng kiểm (a) của [saturation_matrix.py](../full-data-audit/saturation_matrix.py).
