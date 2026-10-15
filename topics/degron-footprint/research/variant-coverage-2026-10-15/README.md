# Độ phủ biến thể ClinVar và tính cấp thiết của bài toán — 15/10/2026 (phiên 10)

> **Câu hỏi của phiên:** Trọng hỏi hai điều — *tập trung vào phần mềm thì có giải quyết được
> vấn đề ý nghĩa bài toán không*, và *degron có là một ngách quan trọng của tin sinh học
> không*. Câu trả lời cho câu đầu là **không** (hai trục độc lập). Phiên này đi đo câu thứ hai.
>
> **Việc đã làm:** tải ClinVar (2,56 triệu biến thể missense), đối chiếu với **bảy tầng** thư
> viện peptide, và đo xem biến thể gây bệnh có giàu lên trong vùng degron hay không.
>
> **Kết quả quyết định — tỉ số chênh gây bệnh/lành tính trong vùng degron là 2,15**, sống sót
> qua khử nhiễu gene (Mantel–Haenszel phân tầng theo protein, 3.114 tầng). Đây là **lập luận
> cấp thiết đầu tiên của đề tài dựa trên số đo**, không dựa trên khẳng định.
>
> **Hai kết quả âm phải nói kèm:** degron lái ung thư kinh điển **phần lớn không hiện ra**
> trong assay này (chỉ HIF1A), và biến thể ClinVar **không** giàu lên về *vị trí* trong degron.
>
> Quyết định: [D-033](../../../../DECISIONS.md#d-033). Script: [`coverage.py`](coverage.py),
> [`enrichment.py`](enrichment.py). Dữ liệu: [`clinvar/SOURCE.md`](../../data/raw/clinvar/SOURCE.md).
>
> ✅ **Đính chính sau khi viết (cùng ngày, cuối phiên 10).** Báo cáo này viết khi hai hệ quả còn là **đề xuất**;
> cả hai **nay đã thành quyết định**, nên đọc mục 7 và mục 10 theo đây: phạm vi **degron tự trị + biến thể
> dòng mầm** đã được chốt, và đối chứng ngoài `CTNNB1` đã chuyển sang **không dùng** — cả hai ở
> [D-035](../../../../DECISIONS.md#d-035) (Claude theo ủy quyền của Trọng). Ngoài ra GVHD đã xác nhận
> **trụ phần mềm là đóng góp** ([D-034](../../../../DECISIONS.md#d-034)). Số liệu trong báo cáo **không đổi**.

## Nhãn bằng chứng

`[đo]` tự chạy trong phiên này · `[nguồn]` số của tác giả khác · `[phân tích]` suy luận từ số
đã đo · `[đề xuất]` chưa được Trọng xác nhận · `[chưa xác minh]` chỉ thấy qua kiến thức nền
hoặc tóm tắt, **chưa** có trích dẫn trong repo.

---

## 1. Vì sao phải đo chuyện này

Đề tài đã có ba trụ: nhãn thực nghiệm (G1 mạnh nhất repo), một khoảng trống đo lường đã
chứng minh, và một con số dương +0,0289 trên trục ngữ cảnh ([D-031](../../../../DECISIONS.md#d-031)).
Nhưng [đánh giá trung thực 15/10](../contribution-assessment-2026-10-15.md) §4 đã chỉ ra chỗ
hở: nhóm được lợi nhất là "nhà nghiên cứu ML khác", và **nhóm đó nhỏ**. Không tài liệu nào
của đề tài trả lời được câu *"vì sao bài toán này đáng làm"* bằng một con số.

Thêm phần mềm **không** lấp chỗ hở đó. Ý nghĩa đến từ **ai bị chặn ở quyết định nào**, không
từ hình thức sản phẩm. API và lớp bất định chỉ đưa một đóng góp *đã có ý nghĩa* đến tay người
dùng. **[phân tích]**

Nên phiên này đi tìm một quyết định thật mà đề tài có thể nối vào: **diễn giải biến thể
missense chưa rõ ý nghĩa (VUS)**. Phá degron là một trong ít lớp cơ chế dự đoán được từ trình
tự, và nó dự đoán **hướng** (bền lên ⇒ có thể tăng chức năng), chứ không chỉ "có hại/không
hại" như đa số bộ dự đoán. Nếu lớp đó phủ đủ nhiều biến thể thật thì đề tài có lập luận cấp
thiết; nếu không thì phải bỏ mạch này. **[phân tích]**

**Điều kiện cam kết trước khi chạy:** nếu số biến thể chấm được chỉ ở mức *vài chục* thì lập
luận không đứng; *vài trăm* trở lên thì đứng. Ghi lại ở đây để không tự nới ngưỡng sau khi
thấy số.

## 2. Bảy tầng, và vì sao phải tách

Lỗi đọc số nghiêm trọng nhất của phép kiểm này là lẫn **thư viện chọn lọc** với **bản tile
đầy đủ**. Repo tới nay chỉ dùng loại thứ nhất. **[đo]**

| Tầng | Peptide | Protein | % tile proteome | Vai |
|---|---:|---:|---:|---|
| `sat` bão hòa | 91 | 91 | 0,0% | ma trận 19 thay thế **đầy đủ** |
| `scan` quét degron | 2.994 | 2.474 | 0,8% | nhãn mức vị trí, **một** thay thế mỗi vị trí |
| `lib` toàn thư viện quét | 9.817 | 6.582 | 2,7% | **chọn lọc**, ≈1,5 tile mỗi protein |
| `pepdome_degron_psi15` | 13.801 | 7.090 | 3,8% | tile PSI ≤ 1,5 |
| `pepdome_degron_psi20` | 45.999 | 13.248 | 12,8% | tile PSI ≤ 2,0 |
| **`pepdome_degron`** | **116.702** | **17.287** | **32,4%** | tile PSI ≤ 3,0 (ngưỡng [D-025](../../../../DECISIONS.md#d-025)) |
| `pepdome_all` | 360.724 | 18.536 | 100% | mọi tile đo được (reads ≥ 10) |

Ba tầng đầu **tái lập đúng** [D-031](../../../../DECISIONS.md#d-031) (91 / 2.994 peptide,
83.446 ô) vì dùng lại nguyên `residue_data.py` của phiên 8 — nên loader đáng tin.

Bốn tầng dưới đến từ **peptidome GPS** ([GEO GSE240610](../../data/README.md) Table S1,
475.506 tile, bước 23 trên toàn proteome người). Repo đã có file này từ 13/10 nhưng **chưa
bao giờ dùng nó làm miền áp dụng**. Bản rút gọn được cache ở
`data/interim/gps-peptidome-rep1.tsv`.

**Miền áp dụng phần lớn là protein chưa thấy [đo].** So với tập huấn luyện mức residue
(2.509 protein / 2.013 cụm cov80):

| | Protein | Cụm cov80 | Cụm **chưa thấy** |
|---|---:|---:|---:|
| `pepdome_degron` | 17.287 | 15.819 | **13.814 (87,3%)** |
| `pepdome_all` | 18.536 | 17.051 | 15.038 (88,2%) |

**67,9%** tile degron (79.195/116.702) nằm trên protein chưa thấy ⇒ công cụ chú giải được một
không gian **gấp ~7 lần** tập có nhãn, và mọi tuyên bố tổng quát hóa buộc phải dựa vào split
cụm — đúng cái repo đã làm.

## 3. Đường ống ClinVar, và phép kiểm chứng toạ độ

ClinVar `variant_summary.txt.gz`, bản `Last-Modified` 12/10/2026, SHA-256 ghi ở
[SOURCE.md](../../data/raw/clinvar/SOURCE.md). **[đo]**

| Bước | Số |
|---|---:|
| Biến thể missense, đã bỏ trùng `VariationID` | 2.564.486 |
| Gene có mặt trong ít nhất một tầng | 2.526.412 |
| **Khớp acid amin hoang dã với UniProt** | **2.349.511 (93,0%)** |
| Bị loại vì lệch toạ độ | 176.901 (7,0%) |

Phép kiểm chứng này **không được bỏ**: toạ độ ClinVar theo transcript RefSeq không đương
nhiên bằng toạ độ UniProt canonical. 7,0% lệch là các trường hợp isoform/transcript khác;
giữ chúng lại sẽ gán biến thể vào sai residue.

⚠ Bỏ trùng theo `VariationID` hơi mạnh nếu một `VariationID` ứng với nhiều `AlleleID`
(haplotype); với SNV missense đơn lẻ thì gần như 1:1. **[phân tích]**

## 4. Độ phủ — con số trả lời câu hỏi của mục 1

**[đo]** Biến thể đã kiểm toạ độ, rơi vào từng tầng:

| Tầng | Tổng | **VUS** | Gây bệnh | Lành tính |
|---|---:|---:|---:|---:|
| `sat` | 591 | 500 | 26 | 26 |
| `scan` | 18.691 | 15.653 | 699 | 938 |
| `lib` | 57.612 | 48.753 | 1.706 | 3.181 |
| `pepdome_degron_psi15` | 73.717 | 61.790 | 3.484 | 3.441 |
| `pepdome_degron_psi20` | 248.663 | 208.365 | 11.424 | 11.431 |
| **`pepdome_degron`** | **630.401** | **530.412** | 26.075 | 28.942 |
| `pepdome_all` | 1.885.334 | 1.583.772 | 59.214 | 105.996 |

**Nhưng "rơi vào peptide" không bằng "chấm được bằng ô đã đo".** Phân biệt này là chỗ dễ
thổi phồng nhất, nên đo riêng: **[đo]**

| Tầng | Trong peptide | Ở **vị trí** đã đo | Ở **đúng ô** đã đo (có cả acid amin) |
|---|---:|---:|---:|
| `sat` (ma trận đầy đủ) | 591 | 591 | **575** (486 VUS · 26 gây bệnh) |
| `scan` (một thay thế/vị trí) | 18.691 | 16.567 | **1.037** (871 VUS · 67 gây bệnh) |

Vì sao `scan` sụp từ 16.567 xuống 1.037: thư viện quét chỉ có **một** thay thế mỗi vị trí,
nên xác suất acid amin của ClinVar trùng đúng cái đó là ≈ 1/19. Bộ bão hòa có cả 19 nên gần
như không mất gì (591 → 575). **[phân tích]**

**⇒ Trả lời điều kiện cam kết trước ở mục 1:** số biến thể chấm được bằng **đúng ô thực
nghiệm** là **≈ 1.600** (575 + 1.037, có chồng lặp vì 61/89 cụm của bộ bão hòa cũng nằm
trong bộ quét), trong đó **≈ 1.350 là VUS**. Ngưỡng "vài trăm" **đã đạt**, vượt một bậc.

Và miền mà *câu hỏi có nghĩa* nhưng chưa có nhãn mức ô: **530.412 VUS** trong 116.702 tile đã
đo là degron.

## 5. Kết quả âm thứ nhất: không có giàu lên theo **vị trí**

**[đo]** Tỉ lệ biến thể nằm trong vùng degron **bằng đúng** tỉ lệ tile là degron, ở cả ba
ngưỡng:

| Ngưỡng degron | % tile của proteome | % biến thể ClinVar |
|---|---:|---:|
| PSI ≤ 3,0 | 32,4% | **33,4%** |
| PSI ≤ 2,0 | 12,8% | **13,2%** |
| PSI ≤ 1,5 | 3,8% | **3,9%** |

⇒ **Không được nói "degron là điểm nóng của biến thể gây bệnh".** Biến thể ClinVar phân bố
trong degron đúng theo tỉ lệ nền. Điều này hợp lý: ClinVar bị chi phối bởi gene nào được
giải trình tự nhiều, không bởi sinh học degron. **[phân tích]**

Thêm một điều phải nói: ngưỡng PSI ≤ 3,0 của [D-025](../../../../DECISIONS.md#d-025) cho
**32,4% tile của toàn proteome** là degron. Ngưỡng đó được chọn cho thư viện quét; **chưa ai
kiểm nó chặt đến đâu trên toàn peptidome**. Ở mức đó, câu "biến thể của bạn nằm trong một
degron" gần như **không mang thông tin**, vì một phần ba proteome thoả. Giá trị phải đến từ
dự đoán ΔPSI **theo từng residue**, không từ vị trí. **[phân tích]**

## 6. Kết quả quyết định: giàu lên theo **tính gây bệnh**, có khử nhiễu gene

Phép so đúng không phải "biến thể trong degron so với ngoài degron", mà **gây bệnh so với
lành tính, trong degron so với ngoài degron**. **[đo]**

Thô, trên mẫu số là tile đo được:

| | Gây bệnh | Lành tính | Tỉ lệ |
|---|---:|---:|---:|
| Trong tile degron | 26.078 | 28.940 | 0,901 |
| Tile đo được khác | 33.131 | 77.052 | 0,430 |

**Tỉ số chênh thô = 2,096** (CI 95% [2,052; 2,140]).

**Nhiễu loạn phải khử:** ClinVar bị vài trăm gene bệnh được giải trình tự rất sâu chiếm đa
số. Nếu đúng những gene đó tình cờ nhiều tile degron thì tỉ số lên cao mà không có ý nghĩa
nào ở mức residue. Đây đúng là lỗi repo đã ghi nhận một lần (*"đơn vị suy luận là cụm
protein, không phải peptide"*). Nên tính **Mantel–Haenszel phân tầng**, chỉ so degron với
không-degron **trong cùng một protein**: **[đo]**

| Phân tích | Tỉ số chênh | CI 95% | Tầng có thông tin |
|---|---:|---|---:|
| Thô | 2,096 | [2,052; 2,140] | — |
| **MH theo protein** | **2,148** | **[2,072; 2,227]** | 3.114 / 13.561 |
| MH theo cụm cov80 | 2,094 | [2,024; 2,167] | 2.903 / 12.390 |

⇒ **Giàu lên không phải tạo tác mức gene.** Trong cùng một protein, so vùng degron với vùng
không degron, biến thể gây bệnh nhiều hơn **2,15 lần** so với lành tính. Trên 3.114 protein.
CI rất chặt vì mẫu rất lớn.

Theo ngưỡng degron thì giàu lên **giữ nguyên, hơi giảm** khi siết: 2,10 (PSI ≤ 3,0) · 1,98
(≤ 2,0) · 1,86 (≤ 1,5). Nghĩa là tín hiệu **không** chỉ do nhóm degron mạnh nhất; nó rộng.
Tầng `lib` cho 0,959 [0,903; 1,018] — **không** giàu lên, đúng như kỳ vọng vì thư viện quét
được tác giả chọn theo tính chất degron, không theo liên quan bệnh. **[phân tích]**

**Giới hạn của kết luận này, phải nói kèm:**

1. **Là liên hệ, không phải nhân quả.** Vùng degron chồng lấn với các đặc trưng chức năng
   khác (vùng vô trật tự, vị trí PTM, motif tuyến tính ngắn). Chưa khử bảo tồn và độ vô trật
   tự ⇒ **chưa** nói được "gây bệnh *vì* phá degron". Đây là đối chứng còn thiếu, ghi ở mục 9.
2. **Nhãn "lành tính" của ClinVar cũng không phân bố ngẫu nhiên** — nó dồn vào gene được
   nghiên cứu nhiều và vùng chịu được biến dị. Thiết kế trong-cùng-protein khử phần mức gene,
   **không** khử phần này.
3. Phân loại là **dòng mầm**. Mạch soma xem mục 7.

## 7. Kết quả âm thứ hai: degron lái ung thư phần lớn không hiện ra

Đây là chỗ tôi (Claude) đã phát biểu **sai** ở đầu phiên, và phép đo bác bỏ. Mạch tôi đề xuất
ban đầu là *"diễn giải đột biến lái ung thư qua phá degron"*, lấy β-catenin, NRF2, MYC làm
ví dụ. Số đo nói mạch đó **không đứng được**. **[đo]**

| Degron kinh điển | Tile | reads rep1/rep2 | PSI rep1 / rep2 | Kết luận |
|---|---|---:|---|---|
| **CTNNB1** codon 31–48 (S33/S37/T41/S45) | 24–51 | 145 / 66 | **5,27 / 5,36** | **đo tốt, nhưng BỀN** — không phải degron |
| **MYC** T58/S62 (FBXW7) | 47–74 | **0 / 0** | NA | **vắng mặt khỏi thư viện** |
| **NFE2L2** ETGE 79–82 | 70–97 | 37 / 41 | **3,59 / 4,46** | không phải degron |
| **HIF1A** ODD P564 (VHL) | 553–580 | 189 / 532 | **1,86 / 1,51** | ✅ **degron mạnh, lặp lại** |
| TP53 vùng MDM2 15–29 | 1–28, 24–51 | 7 / — | 5,81 / 5,06 | không phải degron |

HIF1A còn có đối chứng cơ chế: dưới **MLN4924** (ức chế pan-Cullin) PSI tăng 1,51 → **2,45**,
đúng hướng kỳ vọng nếu phân hủy phụ thuộc CRL. **[đo]**

**Cách đọc đúng:** assay GPS phát hiện degron **tự trị** trong một 28-mer gắn GFP. Ba degron
lái ung thư nổi tiếng nhất đều **có điều kiện** — β-catenin cần GSK3β/CK1 mồi trong phức hủy
Axin/APC; MYC cần phosphoryl T58; NRF2 cần Keap1 bám đồng thời **cả hai** motif DLG và ETGE,
không thể xảy ra trong một 28-mer. HIF1A hiện ra vì prolyl-hydroxyl hóa tác động lên một motif
tuyến tính ngắn, **tự trị trong peptide**. **[chưa xác minh]** phần cơ chế — hợp với số đo
nhưng cần trích dẫn trước khi vào luận văn.

**Hai hệ quả bắt buộc:**

1. **Phạm vi phải gọi là "degron tự trị"**, không phải "degron" chung và tuyệt đối không phải
   "degron lái ung thư". Đây là giới hạn của **assay**, không của mô hình.
2. **[C-16](../../../../DECISIONS.md#c-16) bị phép đo này làm yếu đi nhiều.** Dữ liệu `CTNNB1`
   của Krishna 2026 nhắm đúng tile 24–51 — mà tile đó **có số đo tốt và nói không phải
   degron**. Dùng nó làm đối chứng hội tụ sẽ cho kết quả âm **vì lý do assay**, không vì mô
   hình sai, và sẽ không phân biệt được hai nguyên nhân. Đề xuất chuyển C-16 sang trạng thái
   **không dùng**. ⇒ **Đã thành quyết định cuối phiên:** [D-035](../../../../DECISIONS.md#d-035) qua
   [C-19](../../../../DECISIONS.md#c-19). ⚠ Giá phải trả: rủi ro “cả hai nguồn nhãn đều của Zhang 2023”
   **vẫn mở, chưa có ứng viên thay thế**.

**Mạch soma cũng không có dữ liệu.** Cột `Oncogenicity` của ClinVar rất thưa: toàn bộ 2,56
triệu biến thể missense chỉ có ~800 giá trị, trong đó **145** nằm trong tile degron (75
*Oncogenic* + 70 *Likely oncogenic*), **5** trong bộ quét, **0** trong bộ bão hòa. ⇒ Không
đủ cho bất kỳ tuyên bố nào về ung thư. **[đo]**

## 8. Degron có là ngách quan trọng của tin sinh học?

Tách hai mức, vì câu trả lời khác nhau. **[phân tích]**

**Mức sinh học — có, và nay có một con số của chính đề tài đỡ.** Vùng degron đo được giàu
biến thể gây bệnh **2,15 lần** so với lành tính, trong cùng protein, trên 3.114 protein và
2,5 triệu biến thể lâm sàng thật. Đây là phát biểu cấp thiết **mạnh nhất** đề tài từng có, và
nó không dựa vào uy tín của ngách mà dựa vào số đo. Bối cảnh nền (hệ ubiquitin–proteasome
phân hủy phần lớn protein nội bào; degron VHL–HIF1α là cơ chế cảm nhận oxy; thoái hóa protein
có đích là hướng thuốc đang rất sôi động) là **[chưa xác minh]** trong repo — phải trích dẫn
trước khi dùng, và **không** cần thiết nữa vì con số 2,15 đã tự đứng.

**Mức bài toán của luận văn — hẹp, và hẹp hơn mục 7 vừa chỉ ra.** Nhãn là peptide 28-mer gắn
đuôi GFP đo trong bào tương; phạm vi là degron **tự trị**; degron có điều kiện (phần lớn
degron lái ung thư nổi tiếng) nằm ngoài. Cộng thêm: lĩnh vực chỉ có ~5 công cụ và một nhúm
nhóm nghiên cứu — vừa là cơ hội (ít cạnh tranh) vừa là tín hiệu (cầu nhỏ). Và
[14 công trình của GVHD](../../../../project/advisor-publications/ho-quang-thai.md) **không
có bài nào về degron hay ubiquitin**, nên hội đồng không có tiên nghiệm về tầm quan trọng của
ngách này — lập luận cấp thiết phải tự dựng, và nay dựng được bằng mục 6.

**Phát biểu trung thực, dùng được trước hội đồng:**

> Vùng protein mà thực nghiệm đo được là degron giàu biến thể gây bệnh gấp 2,15 lần so với
> lành tính, so sánh trong cùng protein trên 2,5 triệu biến thể ClinVar. Trong vùng đó có
> 530.412 biến thể chưa rõ ý nghĩa mà hiện không có công cụ nào gán cơ chế. Đề tài dự đoán
> hiệu ứng đột biến **mức residue** trong vùng này, và chấm được ≈1.600 biến thể bằng đúng ô
> thực nghiệm đã đo. Phạm vi là degron **tự trị**; degron phụ thuộc phosphoryl hóa nằm ngoài
> tầm của assay, và điều đó đã được đo chứ không phải giả định.

## 8b. Mắt nối trụ 1 → trụ 2: đã đo ba lần, **chưa thiết lập được**

Trụ 1 nói *vùng* degron giàu biến thể gây bệnh. Trụ 2 dự đoán ở mức **residue**. Câu hỏi nối hai
trụ: **ở độ phân giải residue thì tín hiệu bệnh có còn không?** Đã đo ba cách. **[đo]**

**Phép 1 — nhị phân footprint / không footprint**, trong cùng peptide degron (ngưỡng ΔPSI ≥ 1,0
của repo; footprint chiếm **9,0%** ô đã đo):

| | Gây bệnh | Lành tính |
|---|---:|---:|
| Vị trí footprint | 45 | 76 |
| Vị trí không footprint | 650 | 853 |

**OR = 0,777**, CI 95% [0,530; 1,139] ⇒ **rỗng**. Mất lực: chỉ 121 biến thể có phân loại ở vị trí
footprint; phân tầng vô vọng (17–20 tầng có thông tin).

**Phép 2 và 3 — ΔPSI liên tục** ([`delta_psi_test.py`](delta_psi_test.py), seed 20261015, 2.000 lần
bootstrap **theo cụm cov80**). Thước đo **AUC = P(ΔPSI gây bệnh > ΔPSI lành tính)**, 0,5 là rỗng.
Hướng giả thuyết: phá degron ⇒ protein bền hơn ⇒ ΔPSI dương ⇒ AUC > 0,5.

| Tầng | Khớp | n gây bệnh / lành tính | Trung vị ΔPSI (bệnh / lành) | **AUC** | CI 95% |
|---|---|---:|---|---:|---|
| `scan_pos` | **vị trí** | 695 / 929 · 620 cụm | 0,150 / 0,130 | **0,5166** | [0,479; 0,554] |
| `scan_exact` | đúng acid amin | 67 / 36 · 73 cụm | 0,185 / 0,109 | 0,5195 | [0,400; 0,645] |
| `sat_exact` | **đúng ô**, nhãn sạch nhất | 26 / 25 · 24 cụm | **0,270 / 0,058** | **0,6738** | [0,489; 0,831] |

Ghép cặp **trong cùng peptide**, tầng có lực nhất (`scan_pos`, 82 peptide có cả hai nhóm): hiệu
trung bình **+0,033**, CI [−0,079; +0,141], **51,2%** peptide có hiệu dương — đúng bằng tung đồng xu.

**Cách đọc trung thực:**

1. **Ở độ phân giải residue, tín hiệu bệnh CHƯA được thiết lập.** Tầng duy nhất **có lực**
   (`scan_pos`, n = 1.624, 620 cụm) cho **0,5166** với CI khá chặt [0,479; 0,554] ⇒ nếu có hiệu ứng
   thì **nhỏ**, AUC không quá ≈ 0,55. Cả ba phép đều nhất quán với rỗng.
2. **Có một mạch đáng chú ý nhưng chưa đủ đỡ:** hiệu ứng **tăng dần** khi khớp chặt hơn và nhãn sạch
   hơn — 0,517 → 0,520 → **0,674**, và ở `sat_exact` trung vị ΔPSI của nhóm gây bệnh **gấp 4,6 lần**
   nhóm lành tính (0,270 so 0,058). Đó **đúng** là dạng mà người ta kỳ vọng nếu hiệu ứng thật đang bị
   (a) khớp-theo-vị-trí và (b) nhiễu nhãn làm suy giảm. **Nhưng** `sat_exact` có n = 51 và CI
   **[0,489; 0,831] vẫn chạm 0,5** ⇒ **không được gọi là dương**.
3. **Và phép sạch nhất KHÔNG thể tăng lực bằng dữ liệu hiện có.** Bộ bão hòa chỉ có 91 peptide; số
   biến thể ClinVar khớp đúng ô bị chặn ở **≈51 ca có phân loại**. ⇒ Mắt nối này **không đo được dứt
   điểm bằng dữ liệu đang có**; muốn đóng thì cần nguồn nhãn mức residue mới.
4. **Một phần lý do rỗng, đã đo:** phần lớn biến thể ClinVar rơi vào ô **bị nhiễu loạn yếu** — trung
   vị ΔPSI chỉ 0,13–0,27 so với ngưỡng footprint **1,0**. Biến thể ClinVar không tập trung vào ô
   footprint mạnh.

**Hệ quả cho khung đề tài — đã ghi thành [D-036](../../../../DECISIONS.md#d-036):** giữ trụ 1 ở
**mức vùng**; **không** được nói *"residue mà đề tài dự đoán là residue mang tín hiệu bệnh"*; và
**không** dùng ClinVar làm đích xác nhận cho mô hình. ClinVar chỉ dùng làm **động lực** (530.412 VUS
chưa ai gán cơ chế) chứ không làm nhãn đánh giá.

---

## 9. Việc còn thiếu, xếp theo mức đe doạ kết luận

1. **Đối chứng bảo tồn và độ vô trật tự** — việc quan trọng nhất. Nếu giàu lên 2,15 lần biến
   mất sau khi khử bảo tồn thì nó chỉ nói "degron nằm trong vùng chức năng", không nói gì
   riêng về degron. Cách làm: thêm bảo tồn (phyloP/ConSurf) và rASA/pLDDT (đã có sẵn cho một
   phần protein) làm tầng phân tầng thứ hai trong cùng khuôn Mantel–Haenszel.
2. **Ngưỡng degron phải chọn lại cho peptidome.** PSI ≤ 3,0 cho 32,4% proteome. Nên báo giàu
   lên như một **đường cong theo ngưỡng** (đã có ba điểm: 2,10 / 1,98 / 1,86) thay vì một số.
3. **Bản ClinVar ghim.** File tải về bị ghi đè mỗi tuần; muốn tái lập đúng số phải dùng
   `archive/variant_summary_2026-10.txt.gz`. Xem [SOURCE.md §5](../../data/raw/clinvar/SOURCE.md).
4. **Kiểm chồng lặp giữa 575 và 1.037** để có con số ≈1.600 chính xác (61/89 cụm bộ bão hòa
   nằm trong bộ quét).
5. Mở rộng phép kiểm điểm mục 7 sang đủ bộ degron lái ung thư đã công bố, để con số
   "1 trong 8" có nền thống kê thay vì là một ví dụ.

## 10. Những gì tài liệu này **không** làm

- **Không** quyết định *tại thời điểm viết*. Hai hệ quả ở mục 7 đã thành quyết định **cuối cùng ngày** qua
  [D-035](../../../../DECISIONS.md#d-035) — xem ghi chú đính chính ở đầu file.
- **Không** huấn luyện mô hình nào. Mục tiêu G2 (vượt AUROC 0,7693 trên ma trận bão hòa) **không
  đổi** và **chưa đạt**; [D-027](../../../../DECISIONS.md#d-027) vẫn đòi một kiến trúc mới.
- **Không** sửa `presentation/` — theo dặn dò của Trọng, chỉ sửa khi được yêu cầu.
- **Không** chứng minh biến thể nào gây bệnh vì phá degron; xem giới hạn ở mục 6.
