# Nền sinh học và ngữ nghĩa nhãn của dữ liệu cơ chất deacetyl hóa sirtuin (SIRT1–7)

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Ghi chú nghiên cứu, ngày **08/10/2026**. Mục đích: xác định **nhãn thật sự đo cái gì** và **khung sinh học có đứng được không**, trước khi chốt đề tài "dự đoán cơ chất deacetyl hóa đặc hiệu isoform SIRT1–7".
>
> **Nhãn bằng chứng dùng trong tài liệu này:**
> - `[tác giả báo cáo]` — chính tác giả bài báo nói vậy (có trích dẫn)
> - `[tự kiểm]` — Claude tự tải file / tự chạy lệnh và thấy trong phiên này
> - `[suy luận]` — suy luận của Claude từ các bằng chứng trên
> - `[chưa kiểm]` — chỉ thấy qua tóm tắt, tìm web, hoặc chưa xác nhận được nguồn gốc
>
> Tài liệu này **phản biện** [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md), không xác nhận nó. Có **hai chỗ mâu thuẫn trực tiếp** với bản khuyến nghị đó, nằm ở mục 2.4 và 2.5 — đọc hai mục đó trước khi mang đề tài đi gặp GVHD.
>
> **Giới hạn của phiên này:** không tải được `Supplementary Data 1` của Rauh 2013. Lệnh `curl` tới `static-content.springer.com` trả **403** (`[tự kiểm]`, 08/10/2026). Nghĩa là **mọi con số trong bản khuyến nghị dán nhãn `[tự đo]` về nội dung file nhãn đều KHÔNG được xác nhận lại trong phiên này.** Rauh 2013 không có bản trên PubMed Central (`[tự kiểm]`: `convert_article_ids` cho PMID 23995836 trả về **không có PMCID**), nên toàn văn chỉ lấy được từ nature.com.

---

## 0. Từ vựng sinh học, giải thích cho sinh viên CNTT

Đọc mục này trước, các mục sau sẽ dùng lại không giải thích nữa.

| Thuật ngữ | Giải thích |
|---|---|
| **Lysine (K)** | Một trong 20 amino acid. Đầu mạch nhánh có nhóm `-NH₂` tích điện dương. Đây là chỗ bị gắn thêm nhóm hóa học. |
| **Acetylation (acetyl hóa)** | Gắn nhóm acetyl (`CH₃CO-`) vào `-NH₂` của lysine. Làm mất điện tích dương → đổi tương tác của protein với DNA, với protein khác, hoặc đổi hoạt tính enzyme. Đây là một **PTM** (post-translational modification: biến đổi sau dịch mã). |
| **Deacetylation (deacetyl hóa)** | Phản ứng ngược: tháo nhóm acetyl ra. Sirtuin làm việc này. |
| **Sirtuin (SIRT1–7)** | 7 enzyme ở người, cùng họ với Sir2 của nấm men. Dùng **NAD⁺** làm đồng chất phản ứng (cofactor), nên hoạt tính của chúng gắn với trạng thái chuyển hóa của tế bào → liên quan tới lão hóa và ung thư. |
| **Isoform** | Ở đây nghĩa là 7 thành viên SIRT1…SIRT7. Chúng khác nhau về **vị trí trong tế bào** và về **loại phản ứng** chúng xúc tác (xem mục 5). |
| **Substrate (cơ chất)** | Phân tử mà enzyme tác động lên. "Cơ chất của SIRT2" = protein/vị trí lysine mà SIRT2 deacetyl hóa. |
| **Peptide** | Đoạn chuỗi amino acid ngắn, ở đây dài 13 aa. **Không có cấu trúc không gian** — chỉ là một sợi mềm. Khác hẳn protein gấp cuộn. |
| **Peptide microarray** | Tấm kính in hàng nghìn peptide thành các điểm nhỏ (spot). Nhỏ enzyme lên, rồi đo tín hiệu ở từng điểm. |
| **Mass spectrometry (MS, khối phổ)** | Đo khối lượng peptide để biết vị trí nào bị acetyl hóa và **nhiều hay ít**, trên mẫu tế bào thật. |
| **Acetylome** | Toàn bộ danh mục vị trí acetyl hóa đo được trong một mẫu. |
| **Stoichiometry (tỉ lệ chiếm chỗ)** | Trong số các bản copy của một protein trong tế bào, **bao nhiêu phần trăm** bị acetyl hóa ở đúng vị trí đó. Khác với "có phát hiện được hay không". |
| **KO / KD / OE** | Knockout (xóa gene), knockdown (giảm biểu hiện), overexpression (tăng biểu hiện). Cách gây nhiễu để xem vị trí nào phụ thuộc enziyme đó. |
| **kcat / KM, catalytic efficiency** | `kcat` = tốc độ xúc tác tối đa; `KM` = nồng độ cơ chất cần để đạt nửa tốc độ đó; `kcat/KM` = **hiệu suất xúc tác**, dùng để so hai cơ chất với nhau. |
| **Nucleosome** | DNA cuộn quanh một lõi 8 protein histone. Histone là cơ chất acetyl hóa quan trọng nhất trong nhân. |

---

## 1. Rauh et al. 2013 — phép thử mảng peptide đo chính xác cái gì

Nguồn toàn văn: Rauh D. et al., *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, **Nat Commun 4:2327** — [doi:10.1038/ncomms3327](https://doi.org/10.1038/ncomms3327) · PMID 23995836 (theo PubMed). Mọi câu trong mục 1 lấy từ phần Methods/Results của bản toàn văn trên nature.com, đọc trong phiên này.

### 1.1 Cơ chế đo: đây là phép thử **mất tín hiệu** (loss-of-signal)

- Quy trình: in peptide 13 aa đã acetyl hóa lên mảng → ủ với sirtuin → **sau đó** mới thêm kháng thể kháng acetyl-lysine → đo huỳnh quang. "For deacetylation assays, microarrays were treated with the sirtuin of interest before adding antibodies." `[tác giả báo cáo]` ([Methods, ncomms3327](https://doi.org/10.1038/ncomms3327))
- Enzyme hoạt động ⇒ nhóm acetyl mất ⇒ kháng thể **không bám được** ⇒ tín hiệu **giảm**. Tức là **nhãn dương = tín hiệu bị mất đi**, không phải tín hiệu xuất hiện.
- Chính tác giả ghi hạn chế: **"Our deacetylation assay is based on a loss of signal, which makes small changes hard to measure."** `[tác giả báo cáo]` ([ncomms3327](https://doi.org/10.1038/ncomms3327))
- Phát hiện dùng **hỗn hợp ba kháng thể** kháng acetyl-Lys, rồi hai kháng thể thứ cấp huỳnh quang. `[tác giả báo cáo]`
- Tác giả cũng nêu rằng khác biệt giữa các isoform **có thể đến từ "sequence bias of the anti-acetyl-Lys antibodies"** — tức là thiên lệch của kháng thể theo trình tự, không phải của enzyme. `[tác giả báo cáo]`

> **Ý nghĩa cho máy học** `[suy luận]`: nhãn là **hiệu số của một đại lượng bị chặn trên**. Một peptide mà kháng thể vốn bám yếu thì tín hiệu gốc đã thấp, nên "mất tín hiệu" khó đo → dễ bị gán âm **vì lý do kỹ thuật, không phải vì enzyme không hoạt động**. Đây là một dạng **nhiễu nhãn phụ thuộc đặc trưng** (feature-dependent label noise): chính trình tự peptide — tức là input của mô hình — ảnh hưởng tới xác suất nhãn bị gán sai. Loại nhiễu này **không** được xử lý bằng cách thêm trọng số theo sai số, vì nó lệch có hệ thống, không phải nhiễu ngẫu nhiên.

### 1.2 Bốn cột nhãn nghĩa là gì, theo đúng chữ của tác giả

| Cột | Định nghĩa của tác giả | Ghi chú |
|---|---|---|
| **substrate category** | "...which represents **a deacetylation likelihood between 0 and 1**" `[tác giả báo cáo]` | Đây là một **khả năng liên tục trong [0, 1]**, KHÔNG phải một nhãn phân loại rời rạc. Xem mâu thuẫn ở 2.4. |
| ngưỡng gọi dương | "Peptides with **significant loss of signal (P < 0.01)** were categorized as potential substrates." `[tác giả báo cáo]` | Ngưỡng dương là **kiểm định thống kê**, không phải ngưỡng trên giá trị `category`. |
| **signal ratio** | Tỉ lệ tín hiệu mảng đã xử lý so với **mảng tham chiếu**, trong đó tham chiếu là "a reference microarray treated with **inactive mutant, active sirtuin without NAD⁺ or buffer-only**" `[tác giả báo cáo]` | Bản toàn văn **không dùng** nhãn `exp:ref`; tên cột đó là của file phụ lục. `[tự kiểm: không tải được file để xác nhận]` |
| **ratio error** | "errors represent **variations between peptide spot triplicates and experiment repetitions**" `[tác giả báo cáo]` | Là **sai số đo lặp lại** (3 spot × nhiều lần chạy), không phải độ tin cậy sinh học. |
| **efficiency** | "**Quotients of category and ratio** (efficiency) were used for cluster analysis and heat map preparation." `[tác giả báo cáo]` | **`efficiency` là đại lượng dẫn xuất = category / ratio.** Không phải phép đo độc lập. Xem 2.2. |

### 1.3 Lượng enzyme khác nhau theo isoform — và tác giả nói gì về việc so sánh

- Dải nồng độ dùng trên mảng: **"6–218 μg ml⁻¹ sirtuin in reaction buffer"** `[tác giả báo cáo]`. Chi tiết từng isoform nằm ở **Supplementary Data 5** ("Experimental details for microarray runs and antibodies used") `[tác giả báo cáo, chưa tải được file]`.
- Lý do: **"different enzyme amounts had to be used due to different intrinsic activities."** `[tác giả báo cáo]`
- **Hai câu then chốt, chính tác giả tự giới hạn phạm vi diễn giải:**
  - **"Isoform activities cannot be compared easily as each of the substrates has individual"** (KM và kcat riêng) `[tác giả báo cáo]`
  - **"This comparison cannot show which isoform will dominantly deacetylate a site."** `[tác giả báo cáo]`

> **Đây là bằng chứng mạnh nhất chống lại phần "đặc hiệu isoform" của đề tài** `[suy luận]`. Mục tiêu đầu ra mà bản khuyến nghị mô tả — "với mỗi lysine, 7 điểm số, trả về **tập isoform**" — là **đúng cái mà tác giả bộ dữ liệu nói dữ liệu của họ không trả lời được**. Nếu mô hình học 7 đầu ra từ 7 lần thí nghiệm ở 7 nồng độ enzyme khác nhau, thì cột nào nhiều nhãn dương hơn **có thể chỉ phản ánh enzyme được nhỏ nhiều hơn**, không phản ánh enzyme ưa cơ chất đó hơn. Chuẩn hóa sau (per-isoform threshold calibration) **không khôi phục được** thông tin đã mất, vì không có đại lượng dùng chung nào để neo 7 thang đo lại với nhau.

### 1.4 Tác giả tự nêu bốn hạn chế khác

1. Cửa sổ peptide là hữu hạn: **"More distant residues, not covered by our peptides, might also influence deacetylation."** `[tác giả báo cáo]`
2. Dương tính giả vì cấu trúc: **"false positives could result from limited accessibility of a good substrate site in the full-length protein."** `[tác giả báo cáo]`
3. Bắt buộc phải xác nhận lại: **"Each deacetylation site thus has to be confirmed on native target protein and ultimately in vivo."** `[tác giả báo cáo]`
4. Thiên lệch kháng thể (xem 1.1).

### 1.5 Xác nhận trên protein nguyên: chỉ 3 trường hợp, và một trường hợp không định vị được vị trí

- **MDH + Sirt3 (ELISA):** "Sirt3 reduced MDH acetylation levels, and the effect was impeded by adding the sirtuin inhibitor nicotinamide." Nhưng tác giả ghi thêm: **"These results cannot identify the acetylation site affected."** `[tác giả báo cáo]`
- **Prx1 + Sirt5 (khối phổ):** "Sirt5 catalysed the time-dependent deacetylation of Prx1 protein at **Lys197**", không có phản ứng khi thiếu NAD⁺. `[tác giả báo cáo]`
- **HMG-B1 + Sirt1:** "Sirt1 catalysed the NAD⁺-dependent deacetylation of recombinant, acetylated HMG-B1 protein at **Lys12**." `[tác giả báo cáo]`
- Nồng độ enzyme dùng ở mức protein: **"9.4 μM Sirt5 (Prx1) or 9.7 μM Sirt1 (HMG-B1)"** `[tác giả báo cáo]` — tức là **micromol**, cao hơn nhiều mức sinh lý `[suy luận; chưa kiểm nồng độ sirtuin nội bào thật]`.

> `[suy luận]` Tổng cộng **2 vị trí** (Prx1 K197, HMGB1 K12) được xác nhận ở mức protein nguyên có định vị vị trí, trên **6.802** vị trí của mảng. Tỉ lệ xác nhận ≈ 0,03%. Đây **không phải** tỉ lệ dương tính giả (vì họ chỉ chọn vài ca để thử), nhưng nó cho thấy bước peptide → protein **gần như chưa được đo ở mức hệ thống bởi chính bài gốc**.

### 1.6 Tác giả nói gì về từng isoform trong bài này

- **SIRT1:** bài **không** nói SIRT1 có ít cơ chất hoặc hoạt tính thấp. Ngược lại: Sirt1 "shows a more even activity distribution" và có vẻ **"less specific than most other isoforms"**. `[tác giả báo cáo]`
- **SIRT4:** "we detected **low but reproducible** Sirt4 deacetylation activity **against the non-physiological Fluor-de-Lys peptide**" — dùng **7 μg Sirt4** trong phép thử đó. `[tác giả báo cáo]`
- **SIRT5:** bài dẫn công trình trước rằng Sirt5 "was found to display **stronger desuccinylase and demalonylase activity**". `[tác giả báo cáo]`
- **SIRT6:** "we observed **weak** Sirt6-dependent deacetylation of the hydrophilic histone H3-Lys56 peptide". `[tác giả báo cáo]`
- **SIRT7:** bài **không** đưa phép đo hoạt tính riêng cho SIRT7. Chỉ nói "Nuclear Sirt6 and Sirt7 ... show overlapping preference for a small set of peptides". `[tác giả báo cáo]`

> **Mâu thuẫn với bản khuyến nghị** `[tự kiểm]`: bản [topic-final-recommendation.md](../../../surveys/topic-final-recommendation.md) mục 4.2 viết *"Rauh báo SIRT7 ưa residue thân nước không tích điện hoặc tích điện âm ở vị trí −3, −2, +1"* và dùng câu đó làm **đáp án để kiểm XAI**. Trong phiên này **không tìm thấy câu đó** trong phần toàn văn đọc được (bản fetch trả về rằng phần cuối bài chỉ còn danh mục tài liệu và mô tả file phụ lục, không có phát biểu về vị trí −3/−2/+1). **Đừng dùng con số −3/−2/+1 trong tài liệu gửi GVHD cho tới khi đọc lại đúng đoạn trong Results/Figure của bài gốc.** `[chưa kiểm]`

### 1.7 Danh mục file phụ lục, theo đúng tên tác giả đặt

`[tác giả báo cáo]` (lấy từ phần Supplementary Information của trang nature.com):

| File | Nội dung theo tác giả |
|---|---|
| Supplementary Data 1 | "Annotated microarray peptides and their deacetylation by human Sirt1-Sirt7." |
| Supplementary Data 2 | "Annotation for all peptides sorted by protein." |
| Supplementary Data 3 | "Normed experimental data from all microarrays." |
| Supplementary Data 4 | "p-values and detectability of all substrates on microarrays with 3 different antibodies and antibody mix." |
| **Supplementary Data 5** | **"Experimental details for microarray runs and antibodies used."** ← lượng enzyme từng isoform nằm ở đây |
| Supplementary Data 6 | "Peptides that yielded no significant signal in at least one control experiment." |
| Supplementary Data 7 | "Top12 substrates by deacetylation efficiency co-localized with the 7 human sirtuins." |

> `[suy luận]` **Supplementary Data 6 là file quan trọng nhất mà bản khuyến nghị chưa nhắc tới.** Những peptide "không cho tín hiệu đáng kể ở ít nhất một thí nghiệm đối chứng" là những peptide mà **phép thử mất tín hiệu về nguyên tắc không đo được**. Nếu chúng vẫn nằm trong 6.802 dòng và bị gán nhãn âm, thì một phần nhãn âm là **"không đo được"**, không phải **"đo được và enzyme không hoạt động"**. Việc đầu tiên khi có file: đếm xem Supplementary Data 6 có bao nhiêu dòng và chúng có bị loại khỏi tập huấn luyện của Ridgeway 2025 hay không. **Chưa làm được trong phiên này vì 403.**

---

## 2. Bốn cột đó dùng làm nhãn liên tục hay thứ tự được không

### 2.1 Takeaway

Dùng được về mặt kỹ thuật, nhưng **không phải theo cách bản khuyến nghị mô tả**. `signal ratio` và `ratio error` là đại lượng **trong một isoform, ở một nồng độ enzyme cụ thể**; `efficiency` là **tỉ số dẫn xuất từ hai cột kia**, không phải phép đo mới; và `substrate category` **đã là** một giá trị liên tục [0,1] theo chính định nghĩa của tác giả, nên câu chuyện "chuyển từ nhị phân sang liên tục" không hoàn toàn là một cải tiến mới — nó là **sửa một lỗi diễn giải nhãn** của bài 2025.

### 2.2 `efficiency` không phải nhãn độc lập

- Theo Methods: **"Quotients of category and ratio (efficiency)"** `[tác giả báo cáo]`.
- `[suy luận]` Nghĩa là `efficiency ≈ category / signal_ratio`. Nếu đưa cả 4 cột vào làm 4 nhãn hoặc 4 trọng số, mô hình đang học **một đại lượng đếm hai lần**. Và vì `signal_ratio` nằm ở **mẫu số**, `efficiency` **nổ lên** khi `signal_ratio` nhỏ — tức là chính ở vùng tín hiệu mất nhiều, nơi nhiễu đo lớn nhất. Dùng `efficiency` làm nhãn hồi quy mà không chặn trên sẽ cho một mục tiêu có **phương sai tăng theo giá trị** (heteroscedastic), hướng mô hình tối ưu vào đúng những điểm kém tin cậy nhất.
- `[suy luận]` Nếu muốn một nhãn liên tục duy nhất, `signal_ratio` là lựa chọn ít dẫn xuất nhất, với `ratio_error` làm trọng số nghịch (`1/σ²`). **Không** dùng `efficiency` làm mục tiêu.

### 2.3 Cái gì bị mất khi chuyển sang nhãn thứ tự giữa các isoform

`[suy luận]`, dựa trên 1.3:

1. **Thang đo không chung gốc.** 7 cột `signal_ratio` đến từ 7 thí nghiệm ở nồng độ enzyme khác nhau trong dải 6–218 μg/ml, tức chênh **tới ~36 lần**. Một nhãn thứ tự chung cho 7 isoform đang xếp hạng **tích của (độ ưa cơ chất) × (lượng enzyme được dùng)**.
2. **`ratio error` chỉ nói về độ lặp lại kỹ thuật**, không nói peptide đó có đáng tin về mặt sinh học. Trọng số theo `1/ratio_error²` làm mô hình **tin hơn** vào các spot ổn định về mặt máy đo; nó **không** làm mô hình tin hơn vào các vị trí thật là cơ chất trong tế bào.
3. **Nền bị chặn (floor effect).** Phép thử mất tín hiệu có một mức sàn: khi tín hiệu gốc thấp thì `signal_ratio` gần 1 bất kể enzyme làm gì. Hồi quy trên `signal_ratio` sẽ học phần lớn **mức tín hiệu nền của từng peptide**, một đại lượng phụ thuộc kháng thể.
4. **Nhãn âm lẫn hai loại:** "đo được, enzyme không hoạt động" và "không đo được" (Supplementary Data 6). Không tách được hai loại này thì mọi chỉ số trên lớp âm (specificity, MCC) đều bị thổi phồng.

### 2.4 ⚠️ Mâu thuẫn chưa giải quyết về ngưỡng của Ridgeway 2025

Đây là phát hiện quan trọng nhất của mục này.

- **Bản khuyến nghị trong repo** viết: *"Nhãn nhị phân mà bài 2025 dùng (`category ≥ 1`)"* và đếm *"Số vị trí dương (`category = 1`)"* `[chưa kiểm — không tải được file để kiểm lại]`.
- **Methods của Ridgeway 2025 viết khác:** **"Peptides which produced a *signal ratio score* of 1 or greater were classified as positive, and positions with masked AA residues were replaced with alanine."** `[tác giả báo cáo]` — Ridgeway et al. 2025, Commun Chem, [doi:10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6), [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/), mục Methods "peptide substrate dataset for the sirtuin family was adapted from Rauh et al., 2013" (theo PubMed; PMID 41203923).
- `[suy luận]` Hai cách đọc này **không tương đương**, và một trong hai phải sai:
  - Nếu ngưỡng thật là trên **`substrate category`**: theo Rauh, `category` là "deacetylation likelihood between 0 and 1", nên `≥ 1` nghĩa là **chỉ lấy những vị trí có likelihood đúng bằng 1** — tức là tập dương **cực kỳ bảo thủ**. Điều này **giải thích được** vì sao SIRT1 chỉ còn rất ít vị trí dương.
  - Nếu ngưỡng thật là trên **`signal ratio`**: phép thử là **mất tín hiệu**, nên deacetyl hóa ⇒ tỉ lệ (xử lý : tham chiếu) **< 1**. Gọi dương khi tỉ lệ **≥ 1** thì **ngược dấu** — sẽ gán dương cho đúng những peptide **không** bị deacetyl hóa. Trừ khi cột trong file được định nghĩa theo chiều nghịch (ref : exp) hoặc là log của chiều nghịch.
- **Hệ quả cho đề tài** `[suy luận]`: nếu khả năng thứ hai đúng, **nhãn huấn luyện của bài 2025 bị đảo**, và con số "precision 43,0% trên 149 vị trí SIRT2" trở thành một kết quả rất khó diễn giải. Nếu khả năng thứ nhất đúng thì bản khuyến nghị đúng nhưng Methods của bài 2025 viết sai tên cột.
- **Việc phải làm, trước khi hứa gì với GVHD:** mở `Supplementary Data 1` của Rauh, đọc **tên cột và chiều của `signal ratio`** (xem giá trị của các vị trí đã xác nhận bằng thực nghiệm như Prx1 K197 và HMGB1 K12 là lớn hơn hay nhỏ hơn 1), rồi đối chiếu với file `All_Sirts_Feature_Y_labels.csv` trong [repo của bài 2025](https://github.com/nashirag/ML-Hybrid_Ensemble_Method). **Đây là một phép kiểm 30 phút quyết định toàn bộ RQ1 và RQ2 có nghĩa hay không.**

### 2.5 ⚠️ Nguồn thật của 149 vị trí SIRT2 không phải bài 2025

- **Methods của Ridgeway 2025:** **"The MS-verified sites for SIRT2 were obtained from the dataset provided in Zhang et [al.]"** `[tác giả báo cáo]` ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)). Phần Results cũng viết họ "looked at the performance ... to **confirm reported** SIRT2 cellular substrates from HCT116 cells over-expressing FLAG-SIRT2-WT or catalytically inactive FLAG-SIRT2-H187Y **as previously identified** by tandem MS", và **"Conditions of SIRT2 overexpression in HCT116 cells are described previously."** `[tác giả báo cáo]`
- `[suy luận]` Vậy **149 vị trí đó là dữ liệu của một bài khác (Zhang et al.)**, Ridgeway chỉ dùng lại. Bản khuyến nghị trong repo trình bày chúng như "đo bằng khối phổ với SIRT2 quá biểu hiện (OE) và knockdown (KD)" của bài 2025 — **cần sửa**. Và quan trọng hơn: nếu "tập test độc lập" của đề tài chính là tập test mà baseline đã dùng để báo precision, thì **nó không còn độc lập với baseline**; nó độc lập với *tập huấn luyện*, nhưng cả hai mô hình đều đã được "nhìn" qua nó ở mức chọn ngưỡng và báo cáo. `[suy luận]`
- `[chưa kiểm]` Chưa xác định được Zhang et al. là bài nào (phần tài liệu tham khảo bị cắt số trong bản full-text lấy qua PubMed Central). **Phải tra đúng DOI của Zhang et al. trước khi gọi 149 vị trí này là tập đánh giá.**
- Ngoài ra: Ridgeway tự ghi SIRT2 có **precision 43,0% trên dữ liệu MS**, so với **41,2% trên tập test nội bộ** — tác giả gọi đó là *"a comparable but slight improvement"* `[tác giả báo cáo]`. `[suy luận]` Nghĩa là **theo chính số liệu của họ, không có sụt giảm hiệu năng khi chuyển từ peptide sang tế bào.** Đây là bằng chứng **chống lại** tiền đề trung tâm của đề tài ("có một khoảng cách miền lớn cần đo"): nếu khoảng cách đó không thể hiện ra trong chỉ số, thì RQ2 có nguy cơ đo một hiệu ứng không tồn tại, hoặc đo một hiệu ứng bị che bởi việc tập đánh giá **chỉ có nhãn dương** (precision không thể phát hiện việc mô hình gán dương cho mọi thứ).

### 2.6 Chi tiết khác về nhãn của Ridgeway 2025, cần biết để so sánh công bằng

`[tác giả báo cáo]`, tất cả từ [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/):

- Đặc trưng: one-hot (260 chiều cho sirtuin) + MACCS keys + ProtDCal → **443 đặc trưng cho sirtuin** (483 cho SET8).
- Mô hình: **LDA** cho SET8 và SIRT2; **decision tree** cho một số thành viên SIRT khác. "The number of deacetylation sites (i.e., positive and negative ratio) differed for each SIRT, as well as the best-fit model and meta-model."
- Mất cân bằng: xử lý bằng oversampling/undersampling cho **mọi** isoform **trừ SIRT5** — "SIRT5 (38,4% positive, 61,6% negative)".
- Bộ dự đoán phụ trong ensemble cho họ sirtuin: **MusiteDeep**, gộp bằng **hard voting**.
- Tập thí nghiệm được lọc theo **độ lộ bề mặt**: "Lysine residues with a relevant surface accessibility value of over 0.2 were selected (the NetSurfP1.0 threshold for surface exposure)", cửa sổ ±7 hoặc ±6 quanh lysine trung tâm.
- Chia sẻ cơ chất: **"SIRT2 and SIRT3 share almost twice the substrates as any other combination of SIRT."**
- Về lớp âm, họ tự ghi: **"The accurate classification of negatives is particularly challenging as many PTMs dynamically change over time due to various molecular events within the cell."**

> `[suy luận]` Hai chỗ **bắt buộc phải giữ nguyên nếu muốn so sánh công bằng với baseline:** (a) bộ lọc độ lộ bề mặt NetSurfP > 0,2, (b) ensemble có MusiteDeep. Nếu đề tài mới bỏ cả hai thì chênh lệch MCC/precision không còn quy được cho "PLM tốt hơn đặc trưng làm tay".

---

## 3. Weinert et al. 2015 — vì sao "cơ chất SIRT" trong tế bào là một khái niệm trơn trượt

Nguồn: Weinert B.T. et al., *Analysis of acetylation stoichiometry suggests that SIRT3 repairs nonenzymatic acetylation lesions*, **EMBO J** — [doi:10.15252/embj.201591271](https://doi.org/10.15252/embj.201591271), [PMC4641529](https://pmc.ncbi.nlm.nih.gov/articles/PMC4641529/) (theo PubMed; PMID 26358839). Toàn văn đọc được trong phiên này, mọi số dưới đây là `[tác giả báo cáo]`.

### 3.1 Takeaway

Trong gan chuột, **đa số vị trí acetyl hóa bị chiếm chỗ ở mức ~0,05%** — tức là khoảng 1 trên 2.000 bản copy của protein. Tác giả kết luận SIRT3 chủ yếu **"sửa chữa tổn thương acetyl hóa không do enzyme"**, chứ không điều hòa. Nếu đúng, thì cụm từ "cơ chất sinh lý của SIRT3" mang nghĩa rất khác với "cơ chất của một kinase".

### 3.2 Những con số then chốt

- **Stoichiometry trung vị toàn bộ: ~0,05%.** "We calculated a median stoichiometry of acetylation that was ~0.05%."
- Vị trí ty thể **~0,11%**, vị trí ngoài ty thể **~0,04%** (Fig 3A) — phù hợp với việc có hai bể acetyl-CoA riêng (dẫn Wellen et al.).
- Vị trí đích của SIRT3 (`S3 > 2`) trung vị **0,08%**, thấp hơn vị trí ty thể **không** phải đích của SIRT3 (`S3 < 2`, **0,11%**); và những vị trí **bị ảnh hưởng mạnh nhất** khi mất SIRT3 (`S3 > 4`, `S3 > 8`) lại có stoichiometry **thấp nhất: 0,05%** (Fig 3A).
- **97% vị trí đích của SIRT3 có stoichiometry < 1%** (Fig 3C).
- "We also estimated acetylation stoichiometry at more than 20 sites that were **previously suggested to regulate metabolic proteins**, and found that **nearly all of these sites were < 1% acetylated**."
- Trong chuột SIRT3 KO, dự đoán stoichiometry tại `S3 > 2` tăng **trung vị 4 lần**; tại `S3 > 8` tăng **~11 lần** (và ~20 lần khi kết hợp calorie restriction) (Fig 3D). Tổng cộng chỉ **48 vị trí** đích của SIRT3 được dự đoán vượt 1% trong SIRT3 KO.
- Một vị trí điều hòa trong **nhân** thì khác hẳn: SMC3 K106 **4%** acetyl hóa.
- Các vị trí stoichiometry cao thường nằm trên **enzyme xử lý nhóm acetyl**: AACS K391 **13%**, NAA30 K235 **8%**, NAA50 K34 **5%**, ACSM1 K200 **5%**, KEG1 K128 **4%**, GLYAT K127 **1,5%**.
- Trong **4.322** vị trí có ước lượng stoichiometry: **344** trên protein gắn nhãn UniProt "nucleus", **1.532** trên protein "mitochondrion".
- Kết luận của tác giả về cơ chế: "**there is little evidence of enzyme-catalyzed, site-specific acetylation in mitochondria**, and several studies suggest that most mitochondrial acetylation occurs **nonenzymatically**"; và "increased acetylation at these sites in the absence of SIRT3 is **a function of their inherent reactivity and the nonenzymatic origin of acetylation**".
- Mở rộng sang SIRT5: "The mitochondrial sirtuin deacylase SIRT5 suppresses both succinylation and glutarylation in mitochondria ... both of these modifications **may occur nonenzymatically**, suggesting that sirtuin deacylases may have a **general role in protecting mitochondrial proteins from reactive acyl-CoA metabolites**."
- Tác giả tự giới hạn: "our data and their implications are **global in nature**"; "SIRT3 **may** have a general function in suppressing nonenzymatic acetylation ... **and also** have specific functions in regulating individual sites, as suggested in previous studies."
- Và tự nêu nguồn sai số: "we cannot account for additional modifications at these positions, the presence of which would cause us to **overestimate** acetylation stoichiometry"; so sánh với Zhao et al. thì "Our results **differ** from a previous study that reported high stoichiometry acetylation on EHHADH and MDH2" — khác biệt được quy cho việc Zhao dùng protein biểu hiện ngoại sinh trong tế bào nuôi, còn Weinert đo protein nội sinh trong mô gan.

### 3.3 Hệ quả cho đề tài

`[suy luận]`

1. **Hai mặt, và mặt bất lợi mạnh hơn.** Nếu phần lớn acetyl hóa ty thể là **tổn thương hóa học không chọn vị trí**, thì "đặc hiệu trình tự" ở những vị trí đó phần lớn là đặc hiệu của **sirtuin khi tháo ra**, chứ không phải của một enzyme khi gắn vào. Điều này **ủng hộ** việc có một tín hiệu trình tự học được. Nhưng nó cũng nói rằng **đại lượng sinh học đáng dự đoán** có lẽ là **phản ứng hóa học nội tại của lysine** (pKa, môi trường vi mô, độ lộ) — và cái đó **chủ yếu do cấu trúc 3D quyết định**, không do 13 amino acid liền kề. Mô hình chỉ nhìn cửa sổ 13 aa đang bỏ qua biến giải thích chính.
2. **Ở stoichiometry 0,05%, "cơ chất" không có nghĩa chức năng.** Một đề tài hứa "tìm cơ chất deacetyl hóa của SIRT trong tế bào" nên nói rõ: với 97% vị trí thì việc deacetyl hóa **không thay đổi đáng kể trạng thái của protein đó**, vì nó đã gần như không bị acetyl hóa. Nếu không nói rõ, luận văn đang **ngầm hứa một ý nghĩa sinh học mà dữ liệu không đỡ được**.
3. **Nhãn "thay đổi sau KO" bị trộn hai nguồn.** Theo chính Weinert, mức tăng acetyl hóa khi mất SIRT3 tỉ lệ với **tính phản ứng nội tại** của vị trí đó. Nên "vị trí phụ thuộc SIRT2/SIRT3" vừa mã hóa *enzyme có tác động lên vị trí này* vừa mã hóa *vị trí này dễ bị acetyl hóa phi enzyme*. Một mô hình đạt điểm cao trên nhãn đó **có thể chỉ học được tính phản ứng của lysine**, không học được đặc hiệu enzyme. Đây là một **confound phải kiểm**, ví dụ bằng cách xem mô hình huấn luyện cho SIRT2 và cho SIRT3 có dự đoán gần như giống nhau hay không.

---

## 4. Ba khái niệm phải phân biệt: (a) peptide in vitro, (b) cơ chất thật trên protein gấp cuộn, (c) vị trí đổi sau KO/KD/OE

### 4.1 Takeaway

Ba thứ này là **ba đại lượng khác nhau**, và chuỗi suy diễn giữa chúng **một chiều và yếu**. Chỉ có một suy diễn gần như an toàn: (a) âm ⇒ (b) khả năng âm cao. Mọi suy diễn còn lại đều cần giả định thêm.

### 4.2 Bảng suy diễn

| Từ → tới | Suy diễn được không | Vì sao |
|---|---|---|
| (a) dương → (b) dương | **Không chắc.** Rauh: "false positives could result from **limited accessibility** of a good substrate site in the full-length protein" `[tác giả báo cáo]` | Peptide tự do không có cấu trúc; vị trí lysine đó trên protein thật có thể bị chôn trong lõi hoặc nằm trong giao diện tương tác. |
| (a) âm → (b) âm | **Khá chắc, nhưng không tuyệt đối.** Rauh: "More distant residues, not covered by our peptides, might also influence deacetylation" `[tác giả báo cáo]` | Enzyme có thể cần phần nhận diện ngoài cửa sổ 13 aa. SIRT7 và SIRT6 là ví dụ rõ: hoạt tính trên **peptide tự do rất yếu hoặc không đo được**, nhưng trên **nucleosome** thì có (mục 5). Tức là (a) âm có thể là **dương tính giả của phép thử**, không phải âm sinh học. |
| (b) dương → (c) dương | **Không chắc.** | Cần enzyme và cơ chất **ở cùng khoang tế bào**, cần enzyme hoạt động (NAD⁺ đủ), và cần stoichiometry ban đầu đủ cao để đo được thay đổi. |
| (c) dương → (b) dương | **Không chắc — đây là chỗ sai phổ biến nhất.** | (c) bắt được **mọi** tác động, kể cả gián tiếp: SIRT đó deacetyl hóa một **acetyltransferase** khác; SIRT đó đổi dòng chuyển hóa làm thay đổi mức **acetyl-CoA**, kéo theo acetyl hóa phi enzyme ở hàng nghìn vị trí; KO gây stress chung làm đổi tỉ lệ sống/chết của tế bào. Weinert: acetyl hóa ty thể phần lớn **phi enzyme**, mức tăng tỉ lệ với **tính phản ứng nội tại** của vị trí `[tác giả báo cáo]` → một phần lớn tín hiệu "phụ thuộc SIRT3" là **hệ quả gián tiếp của mức acetyl-CoA và tính phản ứng**, không phải "enzyme bám vào vị trí này". |
| (a) dương → (c) dương | **Yếu nhất trong tất cả**, vì nó là tích của hai bước đều không chắc. | **Đây chính là thứ đề tài định đo.** Precision 43% mà bài 2025 báo là một ước lượng của bước này, nhưng chỉ trên nhãn dương, chỉ cho SIRT2, và trên một tập 149 vị trí lấy từ bài khác. |

### 4.3 Những thứ cụ thể làm đứt chuỗi peptide → protein → tế bào

`[suy luận]` trừ chỗ có ghi nguồn:

1. **Nồng độ enzyme.** Rauh dùng 6–218 μg/ml trên mảng, 9,4–9,7 **μM** ở mức protein, 7 μg Sirt4 cho một phép thử `[tác giả báo cáo]`. Ở nồng độ cao, enzyme có thể xúc tác những phản ứng mà ở mức sinh lý nó không làm. Đây là lý do SIRT4 "có hoạt tính deacetylase thấp nhưng lặp lại được" trên một peptide **phi sinh lý** (Fluor-de-Lys) `[tác giả báo cáo]` — tức là một dương tính *in vitro* mà ý nghĩa sinh học rất đáng ngờ.
2. **Cấu trúc bậc ba.** Bước (a)→(b). Bài 2025 có dùng NetSurfP > 0,2 để lọc độ lộ `[tác giả báo cáo]` — tức là họ **đã** nhận ra vấn đề này, và chính họ đo được rằng nâng ngưỡng độ lộ tăng precision **37,3% → 42,0%** nhưng làm số cơ chất xác nhận được **tụt 885 → 402** `[tác giả báo cáo]`. Đây là một **cổng thông tin cứng**: phần lớn lợi ích từ cấu trúc đã bị baseline khai thác.
3. **Khu trú dưới tế bào.** SIRT1/SIRT6/SIRT7 ở nhân, SIRT2 chủ yếu tế bào chất, SIRT3/4/5 ở ty thể `[chưa kiểm — cần trích dẫn riêng]`. Một peptide từ protein ty thể có thể bị SIRT1 deacetyl hóa trên mảng mà **hai phân tử đó không bao giờ gặp nhau trong tế bào**. Mô hình học từ mảng sẽ dự đoán dương, và nó **đúng về hóa học, sai về sinh học**. Khu trú là một đặc trưng **rẻ** cần thêm vào, nhưng thêm nó vào thì mô hình đang học một thứ không có trong nhãn huấn luyện → mất tính nhất quán giữa train và test.
4. **Stoichiometry.** Trung vị ~0,05% `[tác giả báo cáo, Weinert]`. Khối phổ chỉ phát hiện được thay đổi ở những vị trí đủ nhiều để định lượng được. Nên nhãn (c) **thiên lệch về phía vị trí có stoichiometry cao** — một tập con rất nhỏ và không đại diện.
5. **Tác động gián tiếp.** Xem 4.2. Không có cách nào tách ra bằng dữ liệu KO/KD đơn lẻ; cần thí nghiệm có đối chứng xúc tác (ví dụ so SIRT2-WT với đột biến mất hoạt tính H187Y — đúng loại đối chứng mà tập 149 vị trí dùng `[tác giả báo cáo]`, nên tập đó về mặt thiết kế là **tốt**; điểm yếu của nó là kích thước và việc chỉ có nhãn dương).
6. **NAD⁺ và chất ức chế nội sinh.** Hoạt tính sirtuin phụ thuộc NAD⁺; nicotinamide ức chế (Rauh dùng chính điều này làm đối chứng cho MDH `[tác giả báo cáo]`). Mô hình chỉ ăn trình tự thì **không có biến nào** đại diện cho trạng thái chuyển hóa.
7. **Cạnh tranh giữa 7 isoform + 11 HDAC cổ điển.** Rauh: "This comparison **cannot show which isoform will dominantly deacetylate a site**" `[tác giả báo cáo]`. Đầu ra "tập isoform có bảo đảm độ phủ" mà bản khuyến nghị đề xuất đang ngụ ý một bài toán phân công isoform mà **dữ liệu không chứa thông tin để phân công**.

---

## 5. Từng isoform: khung "deacetylase" khớp đến đâu

### 5.1 Takeaway

Trong 7 isoform, **chỉ SIRT1, SIRT2 và SIRT3** là deacetylase theo đúng nghĩa có hoạt tính mạnh trên lysine acetyl hóa. **SIRT4 và SIRT5 gần như không phải deacetylase.** **SIRT6 là deacetylase rất yếu** và là defatty-acylase mạnh. **SIRT7 hầu như không có hoạt tính trên peptide tự do** mà cần nucleic acid/nucleosome. Nghĩa là **một bài toán "dự đoán cơ chất deacetyl hóa" với 7 đầu ra bình đẳng là sai về mặt enzymology cho 4 trong 7 đầu ra.**

### 5.2 Bảng theo isoform

| Isoform | Khung "deacetylase" khớp? | Bằng chứng |
|---|---|---|
| **SIRT1** | **Khớp.** | Rauh: Sirt1 "shows a more even activity distribution", "less specific than most other isoforms"; xác nhận trên HMG-B1 K12, phụ thuộc NAD⁺ `[tác giả báo cáo]` ([ncomms3327](https://doi.org/10.1038/ncomms3327)) |
| **SIRT2** | **Khớp**, nhưng cũng là demyristoylase hiệu quả. | Hoạt tính deacetylase rõ; ngoài ra `kcat/KM` cho việc tháo nhóm **myristoyl** "slightly higher" so với nhóm acetyl `[chưa kiểm — qua tìm web, dẫn tới PMC4894398 "Efficient Demyristoylase Activity of SIRT2 Revealed by Kinetic and Structural Studies"]` |
| **SIRT3** | **Khớp** về hoạt tính, nhưng **không khớp về ý nghĩa**. | Rauh xác nhận SIRT3 giảm acetyl hóa MDH (nhưng "cannot identify the acetylation site affected") `[tác giả báo cáo]`. Weinert: SIRT3 nén acetyl hóa xuống **~0,05–0,08%**, kết luận vai trò là **"repairs nonenzymatic acetylation lesions"** chứ không điều hòa `[tác giả báo cáo]` ([doi:10.15252/embj.201591271](https://doi.org/10.15252/embj.201591271)) |
| **SIRT4** | **Không khớp.** | Mathias et al. 2014, Cell: **"mitochondrial SIRT4 and SIRT5 have little to no deacetylase activity, and a robust catalytic activity for SIRT4 has been elusive"**; SIRT4 là **lipoamidase** và **"SIRT4 catalytic efficiency for lipoyl- and biotinyl-lysine modifications is superior to its deacetylation activity"** `[tác giả báo cáo]` ([doi:10.1016/j.cell.2014.11.046](https://doi.org/10.1016/j.cell.2014.11.046), [PMC4344121](https://pmc.ncbi.nlm.nih.gov/articles/PMC4344121/), theo PubMed). Trước đó Haigis et al. 2006, Cell: SIRT4 **ADP-ribosyl hóa** glutamate dehydrogenase `[tác giả báo cáo]` ([doi:10.1016/j.cell.2006.06.057](https://doi.org/10.1016/j.cell.2006.06.057), theo PubMed). Rauh chỉ đo được "**low but reproducible** Sirt4 deacetylation activity against the **non-physiological** Fluor-de-Lys peptide" với 7 μg enzyme `[tác giả báo cáo]` |
| **SIRT5** | **Không khớp.** | Cùng câu của Mathias et al. ở trên `[tác giả báo cáo]`. Rauh dẫn rằng Sirt5 có "stronger **desuccinylase and demalonylase** activity" `[tác giả báo cáo]`. Weinert: SIRT5 nén **succinylation và glutarylation** ở ty thể, và cả hai biến đổi này "**may occur nonenzymatically**" `[tác giả báo cáo]`. Tìm web cho con số "trên trăm lần cao hơn cho lysine succinyl/glutaryl so với acetyl" `[chưa kiểm — chưa đọc bài gốc Du et al. 2011 Science]` |
| **SIRT6** | **Khớp rất kém.** | Jiang et al. 2013, Nature: **"four of the seven mammalian sirtuins have very weak deacetylase activity in vitro"**; SIRT6 "efficiently removes **long-chain fatty acyl groups**, such as myristoyl"; cấu trúc cho thấy "a large **hydrophobic pocket**" `[tác giả báo cáo]` ([doi:10.1038/nature12038](https://doi.org/10.1038/nature12038), [PMC3635073](https://pmc.ncbi.nlm.nih.gov/articles/PMC3635073/), theo PubMed). Một review tổng hợp: hoạt tính deacetylase của SIRT6 **"100 to 1000 times lower compared to the most active SIRTs"**, và **"in vitro demyristoylation activity is roughly 300 times higher than deacetylation"** `[tác giả báo cáo — nhưng là review, dẫn lại Jiang et al.]` ([PMC8389836](https://pmc.ncbi.nlm.nih.gov/articles/PMC8389836/)). Cùng review: hoạt tính SIRT6 "depends on histone packaging, thereby being **lower when tested in vitro using free histones**" `[tác giả báo cáo]`. Rauh chỉ thấy "**weak** Sirt6-dependent deacetylation of the hydrophilic histone H3-Lys56 peptide" `[tác giả báo cáo]`. SIRT6 còn **mono-ADP-ribosyl hóa** PARP1 ở K521 (Mao et al. 2011, Science, [doi:10.1126/science.1202723](https://doi.org/10.1126/science.1202723), theo PubMed) `[tác giả báo cáo]` |
| **SIRT7** | **Khớp kém, và theo một cách khác.** | Barber et al. 2012, Nature: SIRT7 là **"a highly selective H3K18Ac deacetylase"** — tức là có hoạt tính deacetylase, nhưng **cực kỳ chọn lọc, gần như chỉ một vị trí** `[tác giả báo cáo]` ([doi:10.1038/nature11043](https://doi.org/10.1038/nature11043), [PMC3412143](https://pmc.ncbi.nlm.nih.gov/articles/PMC3412143/), theo PubMed). Trên **peptide tự do** thì hoạt tính hầu như không đo được; cần **DNA hoặc RNA** (tRNA là chất kích hoạt mạnh nhất) hoặc **nucleosome** mới có hoạt tính `[chưa kiểm — chỉ qua tìm web, chưa đọc bài gốc; các nguồn web trỏ tới PMC4850736, PMC5326686]`. Rauh **không** đưa phép đo hoạt tính riêng cho SIRT7 `[tác giả báo cáo]` |

### 5.3 Hệ quả: isoform nào làm bài toán trở nên đáng ngờ

`[suy luận]`

- **SIRT4 và SIRT5: đáng ngờ nhất.** Chính tác giả bài Cell 2014 nói hai isoform này "có rất ít hoặc không có hoạt tính deacetylase". Nhưng theo chính số liệu được báo trong bản khuyến nghị, **SIRT5 lại là isoform có NHIỀU nhãn dương nhất (2.614)** và là isoform duy nhất **không** cần cân bằng lại lớp (38,4% dương, theo Methods của Ridgeway `[tác giả báo cáo]`). **Đây là một nghịch lý phải giải thích trước khi làm.** Hai cách đọc, cả hai đều xấu cho đề tài:
  1. SIRT5 được nhỏ **lượng enzyme cao nhất** trên mảng, nên mất tín hiệu nhiều nhất → cột SIRT5 chủ yếu phản ánh **nồng độ enzyme**. (Kiểm được bằng Supplementary Data 5.)
  2. Hoặc cột SIRT5 phản ánh hoạt tính thật nhưng là hoạt tính **desuccinylase/demalonylase** thể hiện ra như hoạt tính yếu trên lysine acetyl — nghĩa là mô hình "SIRT5 deacetylation" đang học **một phản ứng mà sinh học bảo không phải phản ứng chính của SIRT5**.
- **SIRT6 và SIRT7: đáng ngờ vì phép thử sai bối cảnh.** Cả hai cần **nucleosome / nucleic acid** để hoạt động. Mảng peptide tự do là **bối cảnh tệ nhất có thể** cho hai enzyme này. Nhãn âm cho SIRT6/SIRT7 trên mảng phần lớn có thể là **âm của phép thử**, không phải âm sinh học. Một mô hình đạt MCC cao trên hai cột này đang **học thành công một tạo tác thí nghiệm**.
- **SIRT1, SIRT2, SIRT3: dùng được.** Và đáng chú ý, đây đúng là ba isoform mà Rauh xác nhận được ở mức protein (SIRT1→HMGB1, SIRT3→MDH) hoặc có tập đánh giá trong tế bào (SIRT2, 149 vị trí).
- **Khuyến nghị thẳng** `[suy luận]`: nếu vẫn làm đề tài này, **hạ phạm vi định lượng xuống SIRT1/2/3**, và trình bày SIRT4–7 như một **phân tích phụ về giới hạn của nhãn** (ví dụ: "cột SIRT5 tương quan với lượng enzyme ra sao", "mô hình SIRT6/SIRT7 học được gì khi phép thử sai bối cảnh"). Phân tích đó **có giá trị khoa học thật** và trung thực hơn một mô hình 7 đầu ra trông đẹp. Bản khuyến nghị hiện tại chỉ đặt cổng dừng cho **SIRT1** (vì ít nhãn dương) — **đó là isoform sai để lo lắng về**. SIRT1 là deacetylase hợp lệ nhất trong 7 cái; SIRT4, SIRT5, SIRT6, SIRT7 mới là chỗ khung sinh học đổ.

---

## 6. Bằng chứng CHỐNG lại đề tài, gom một chỗ

`[suy luận]` trên nền các trích dẫn ở trên. Mục này viết để mang đi gặp GVHD, vì nếu không tự nói ra thì GVHD sẽ hỏi.

1. **Tác giả bộ dữ liệu đã nói trước rằng không dùng được cho mục đích này.** "Isoform activities cannot be compared easily"; "This comparison cannot show which isoform will dominantly deacetylate a site." Đề tài đặt tên là *"đặc hiệu isoform"* và đầu ra là *tập isoform*. Phải có câu trả lời cho việc này, không chỉ là "chúng em hiệu chỉnh ngưỡng theo isoform".
2. **4 trong 7 isoform không phải deacetylase mạnh.** SIRT4/SIRT5 "little to no deacetylase activity" (Cell 2014); SIRT6 thấp hơn 100–1000 lần; SIRT7 cần nucleic acid. Một mô hình đa nhãn 7 đầu ra ngụ ý 7 bài toán cùng loại — không đúng.
3. **Tiền đề "có khoảng cách miền lớn" chưa được số liệu đỡ.** Theo chính Ridgeway, precision trên MS (**43,0%**) **cao hơn** precision trên tập test nội bộ (**41,2%**). Nếu RQ2 là "đo khoảng cách in vitro → trong tế bào", thì baseline đã cho thấy khoảng cách đó **xấp xỉ bằng không ở chỉ số này**. RQ2 có nguy cơ không có hiệu ứng để đo.
4. **Tập đánh giá "độc lập" không độc lập như mô tả.** 149 vị trí là của **Zhang et al.**, baseline đã dùng chúng để báo cáo; và chúng **chỉ có nhãn dương**, nên chỉ đo được precision — một chỉ số mà mô hình đoán dương cho mọi thứ vẫn có thể thắng.
5. **Ngữ nghĩa nhãn chưa được xác định.** Mâu thuẫn `substrate category` vs `signal ratio` ở mục 2.4 chưa giải quyết, và `substrate category` theo định nghĩa của tác giả **đã là** liên tục [0,1], nên "đóng góp dùng nhãn liên tục" có thể chỉ là **sửa một lỗi đọc nhãn**, không phải một đóng góp phương pháp.
6. **Phần lợi ích từ cấu trúc đã bị baseline hái.** Ridgeway đã dùng NetSurfP > 0,2 và tự đo được đường cong precision-vs-coverage của nó (37,3% → 42,0%, nhưng 885 → 402 vị trí).
7. **Ý nghĩa sinh học ở stoichiometry 0,05% là mỏng.** 97% vị trí đích của SIRT3 dưới 1% acetyl hóa; "nearly all" trong 20+ vị trí "được cho là điều hòa protein chuyển hóa" cũng dưới 1%. Câu "tìm cơ chất để hiểu điều hòa" cần đổi thành câu khác, trung thực hơn.
8. **Nhãn (c) trộn tác động trực tiếp và gián tiếp, và mức tăng tỉ lệ với tính phản ứng nội tại của lysine** (Weinert). Mô hình có thể đạt điểm cao bằng cách học tính phản ứng của lysine, không học đặc hiệu enzyme. Phải có phép kiểm cho confound này.

### 6.1 Bằng chứng ỦNG HỘ, để công bằng

1. **Phép thử có đối chứng tốt.** Mảng tham chiếu dùng **đột biến mất hoạt tính, hoặc enzyme hoạt động nhưng thiếu NAD⁺, hoặc chỉ buffer** `[tác giả báo cáo]` — ba loại đối chứng, mạnh hơn mức thường thấy. Và sai số là sai số lặp lại thật (3 spot × nhiều lần chạy).
2. **Tập đánh giá trong tế bào có đối chứng xúc tác.** 149 vị trí đến từ so sánh **FLAG-SIRT2-WT với đột biến mất hoạt tính H187Y** `[tác giả báo cáo]`. Đây đúng là thiết kế loại bỏ được phần lớn tác động gián tiếp — tốt hơn một KO trần.
3. **Cấu trúc chia sẻ cơ chất giữa isoform là thật theo chính bài 2025:** "SIRT2 and SIRT3 share almost twice the substrates as any other combination of SIRT" `[tác giả báo cáo]`. Và SIRT2/SIRT3 đúng là hai isoform mà khung deacetylase khớp. Một mô hình đa nhãn **giới hạn ở SIRT1/2/3** có cơ sở sinh học.
4. **Bài 2025 tự để ngỏ đúng chỗ đề tài muốn làm** (PLM thay đặc trưng làm tay) `[chưa kiểm — câu này lấy từ bản khuyến nghị, chưa tự đọc đoạn "future work" của bài 2025]`.
5. **Phép kiểm XAI có đáp án là ý tưởng tốt**, nhưng đáp án phải là đáp án **thật** — xem cảnh báo ở 1.6 về con số −3/−2/+1 chưa xác nhận được.

---

## 7. Việc phải làm, theo thứ tự, trước khi trình bày

`[suy luận]`

1. **Tải `Supplementary Data 1` và `5` của Rauh** (từ máy sinh viên, vì cloud bị 403). Kiểm ba điều: (a) tên và **chiều** của cột `signal ratio`; (b) **lượng enzyme từng isoform** trong Data 5, và vẽ tương quan giữa lượng enzyme và số nhãn dương của 7 cột — nếu tương quan cao thì phần "đặc hiệu isoform" của đề tài đổ; (c) **Supplementary Data 6** có bao nhiêu peptide "không cho tín hiệu đáng kể ở đối chứng", và chúng có bị loại khỏi tập của Ridgeway hay không.
2. **Giải quyết mâu thuẫn ngưỡng ở 2.4** bằng cách đối chiếu `All_Sirts_Feature_Y_labels.csv` trong [repo bài 2025](https://github.com/nashirag/ML-Hybrid_Ensemble_Method) với file gốc của Rauh, dùng Prx1 K197 và HMGB1 K12 làm mốc đã biết là dương.
3. **Tra DOI của Zhang et al.** — nguồn thật của 149 vị trí SIRT2 — và đọc cách họ định nghĩa "cơ chất SIRT2".
4. **Thu hẹp phạm vi xuống SIRT1/2/3** cho phần định lượng, chuyển SIRT4–7 thành phân tích giới hạn nhãn. Sửa cổng dừng: hiện đang đặt cho SIRT1, nên đặt cho **SIRT4, SIRT5, SIRT6, SIRT7**.
5. **Bỏ hoặc xác nhận lại** con số "SIRT7 ưa residue ở −3/−2/+1" trước khi dùng làm đáp án XAI.
6. **Chuẩn bị câu trả lời cho hai câu GVHD sẽ hỏi:** "tại sao coi 7 isoform là 7 bài toán cùng loại khi 4 cái không phải deacetylase?" và "nếu baseline đã cho precision trên MS cao hơn trên test nội bộ, thì khoảng cách miền em muốn đo nằm ở đâu?"

---

## 8. Điều ghi chú này KHÔNG làm được

- **Không tải được `Supplementary Data 1` của Rauh** (403 từ `static-content.springer.com`, `[tự kiểm]` 08/10/2026). Nên **không kiểm lại được bất kỳ con số nào** mà bản khuyến nghị dán nhãn `[tự đo]`: 6.802 vị trí, số nhãn dương từng isoform (176/1.901/1.844/1.038/2.614/1.199/1.692), sai số trung vị, phân bố số isoform dương. Chúng vẫn là `[chưa kiểm]` đối với phiên này.
- **Không đọc được lượng enzyme cụ thể của từng isoform** (nằm trong Supplementary Data 5). Chỉ có dải **6–218 μg/ml** từ Methods. Nên không thể nói chính xác isoform nào bị thiên lệch nhiều nhất.
- **Không đọc được phần Results/Figure giữa bài của Rauh** về đặc hiệu trình tự từng isoform. Bản fetch đọc được Methods và phần cuối (danh mục phụ lục), nhưng phần mô tả motif theo vị trí (−3, −2, +1) **không thấy** trong những đoạn lấy về.
- **Không xác định được Zhang et al. là bài nào** — danh mục tài liệu trong bản full-text qua PubMed Central bị cắt số trích dẫn.
- **Không đọc toàn văn** Du et al. 2011 (Science, SIRT5 desuccinylase), Feldman et al. (SIRT6 activation bởi acid béo), các bài SIRT7 cần DNA/RNA, và bài demyristoylase của SIRT2. Các số từ những nguồn này đều dán `[chưa kiểm]`.
- **Không kiểm được nồng độ sirtuin sinh lý thật trong tế bào**, nên nhận xét "9,4 μM cao hơn mức sinh lý" là `[suy luận]`, chưa có số đối chiếu.
- **Không chạy mô hình, không huấn luyện gì** (theo đúng phạm vi được giao).

---

## 9. Nguồn

Theo PubMed và các trang nhà xuất bản, truy cập 08/10/2026:

- Rauh D. et al. (2013), *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327 — [doi:10.1038/ncomms3327](https://doi.org/10.1038/ncomms3327) · PMID 23995836 · **không có bản PMC**
- Ridgeway N. et al. (2025), *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem — [doi:10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6) · [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) · PMID 41203923 · mã và nhãn: https://github.com/nashirag/ML-Hybrid_Ensemble_Method
- Weinert B.T. et al. (2015), *Analysis of acetylation stoichiometry suggests that SIRT3 repairs nonenzymatic acetylation lesions*, EMBO J — [doi:10.15252/embj.201591271](https://doi.org/10.15252/embj.201591271) · [PMC4641529](https://pmc.ncbi.nlm.nih.gov/articles/PMC4641529/) · PMID 26358839
- Mathias R.A. et al. (2014), *Sirtuin 4 is a lipoamidase regulating pyruvate dehydrogenase complex activity*, Cell 159(7):1615–25 — [doi:10.1016/j.cell.2014.11.046](https://doi.org/10.1016/j.cell.2014.11.046) · [PMC4344121](https://pmc.ncbi.nlm.nih.gov/articles/PMC4344121/) · PMID 25525879
- Haigis M.C. et al. (2006), *SIRT4 inhibits glutamate dehydrogenase and opposes the effects of calorie restriction in pancreatic beta cells*, Cell 126(5):941–54 — [doi:10.1016/j.cell.2006.06.057](https://doi.org/10.1016/j.cell.2006.06.057) · PMID 16959573
- Jiang H. et al. (2013), *SIRT6 regulates TNF-α secretion through hydrolysis of long-chain fatty acyl lysine*, Nature 496(7443):110–3 — [doi:10.1038/nature12038](https://doi.org/10.1038/nature12038) · [PMC3635073](https://pmc.ncbi.nlm.nih.gov/articles/PMC3635073/) · PMID 23552949
- Barber M.F. et al. (2012), *SIRT7 links H3K18 deacetylation to maintenance of oncogenic transformation*, Nature 487(7405):114–8 — [doi:10.1038/nature11043](https://doi.org/10.1038/nature11043) · [PMC3412143](https://pmc.ncbi.nlm.nih.gov/articles/PMC3412143/) · PMID 22722849
- Mao Z. et al. (2011), *SIRT6 promotes DNA repair under stress by activating PARP1*, Science 332(6036):1443–6 — [doi:10.1126/science.1202723](https://doi.org/10.1126/science.1202723) · [PMC5472447](https://pmc.ncbi.nlm.nih.gov/articles/PMC5472447/) · PMID 21680843
- Review về SIRT6 (dùng cho các con số 100–1000 lần và ~300 lần, **là review dẫn lại**): *Emerging Therapeutic Potential of SIRT6 Modulators* — [PMC8389836](https://pmc.ncbi.nlm.nih.gov/articles/PMC8389836/)
- `[chưa kiểm]` các nguồn chỉ thấy qua tìm web, chưa đọc toàn văn: PMC4894398 (SIRT2 demyristoylase), PMC4850736 và PMC5326686 (SIRT7 cần DNA/RNA)
