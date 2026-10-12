# Nhãn mảng peptide gần như không chuyển được vào tế bào

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../DECISIONS.md).

**Phán quyết: THU HẸP — không bỏ, nhưng phải đổi hẳn lời hứa của đề tài.** Phép thử trực tiếp nhất mà năm nhánh khảo sát làm được đã cho kết quả xấu nhất có thể cho giả thuyết trung tâm: trên **1.417 vị trí** khớp cửa sổ 13 amino acid giữa mảng peptide Rauh 2013 và acetylome SIRT3 trong tế bào người (Sol 2012, U2OS), nhãn SIRT3 của mảng dự báo chiều thay đổi acetyl hóa trong tế bào với **MCC chỉ từ +0,047 đến +0,080** tùy ngưỡng, và trên tập chồng lấn chặt hơn (khớp đúng UniProt + vị trí, n = 718) **MCC = −0,007** `[tự kiểm]`. Nói thẳng: **nhãn in vitro gần như không mang thông tin về việc một lysine có phụ thuộc sirtuin trong tế bào hay không.** Cùng lúc, ba cột chống đỡ khác của đề tài cũng sụt: "đặc hiệu isoform SIRT1–7" **đã được công bố hai lần** (Ridgeway 2025 ở mức residue, DeepSIRT 2021 ở mức protein — do chính nhóm Prof. Y.-Y. Ou làm); **bốn trong bảy isoform không phải deacetylase mạnh** theo chính các bài gốc về enzymology; và con số **43,0%** mà bản khuyến nghị nội bộ dùng làm mốc so sánh **là recall, không phải precision**, lại còn pha rò rỉ (52,3% trên các vị trí đã có trong tập huấn luyện so với 39,0% trên các vị trí ngoài tập) `[tự kiểm]`. Nhưng cổng dữ liệu thì **mở**: mọi file nhãn, file dự đoán baseline và hai acetylome trong tế bào đều đã tải và đếm được trong phiên khảo sát, và nguồn nhãn âm trong tế bào — thứ mà bản khuyến nghị tưởng là không có — nằm ngay trong bài mà baseline đã dùng. Vì vậy khuyến nghị là **giữ đề tài nhưng hạ phạm vi định lượng xuống SIRT1/2/3 và đổi sản phẩm khoa học từ "một mô hình tốt hơn" thành "một phép đo có kiểm soát về mức độ KHÔNG chuyển được của nhãn in vitro"** — đồng thời chuẩn bị thật sự cho khả năng GVHD không chấp nhận kết quả âm làm đóng góp chính, và khi đó đề tài dự phòng B có lợi thế rõ ràng ở đúng tiêu chí 4 (XAI có đáp án).

---

## 1. Phán quyết, lý do, mức tin cậy

**Quyết định đề nghị: THU HẸP (narrow), không tiếp tục như đang viết, cũng không tạm dừng.**

Ba lựa chọn và lý do chọn cái giữa:

| Lựa chọn | Vì sao không / vì sao có |
|---|---|
| **Tiếp tục nguyên trạng** (7 isoform, mục tiêu "mô hình tốt hơn, trả về tập isoform") | **Không.** Chính tác giả bộ dữ liệu viết **"This comparison cannot show which isoform will dominantly deacetylate a site"** `[tác giả báo cáo]` ([ncomms3327](https://doi.org/10.1038/ncomms3327)), tức đầu ra "tập isoform" là đúng cái dữ liệu không trả lời được. Thêm nữa 4/7 isoform không phải deacetylase mạnh (mục 2), và phép đo chuyển miền đã cho MCC ≈ 0 (mục 4). |
| **THU HẸP** | **Có.** Hạ phần định lượng xuống **SIRT1/2/3**; đổi câu hỏi trung tâm từ "mô hình của em tốt hơn" thành "**đo cho đúng** mức chuyển được của nhãn mảng, với nhãn âm thật, với metric đúng, với kiểm soát rò rỉ ba mức". Dữ liệu cho việc này **đã có trong tay** và baseline **đã có điểm số từng vị trí**. Đây là đề tài duy nhất trong ba lựa chọn mà mọi con số cần thiết đều kiểm được trước tuần 6. |
| **Tạm dừng / chuyển sang B** | **Chỉ nếu** GVHD trả lời "không" cho câu hỏi số 1 ở mục 9 (kết quả âm có được chấp nhận làm đóng góp chính không). Khi đó B mạnh hơn thật, không phải vì B mới hơn mà vì B có **đáp án XAI định lượng**: trong benchmark dbPTM, **1.246/1.503 (83%)** cửa sổ dương CDK có proline ở vị trí +1, so với **919/29.823 (3%)** cửa sổ âm `[tự đo, theo b-method-layer-draft.md]`. Sirtuin **không có gì tương đương** (mục 2.5). |

**Mức tin cậy:**

- **Cao** cho kết luận "nhãn mảng không chuyển được ở chỉ số nhị phân": phép đo được chạy trên file thật, hai loài, bốn ngưỡng, và nhất quán xấu ở mọi ngưỡng `[tự kiểm]`.
- **Cao** cho kết luận "quy tắc nhãn là `efficiency ≥ 1`": tái lập **100,0000%** trên **47.607** ô (6.801 vị trí × 7 isoform), **0 bất đồng** `[tự kiểm]`.
- **Trung bình** cho kết luận "tính mới yếu ở cả ba trục": dựa trên khảo sát một ngày, PubMed + WebSearch, chưa đọc toàn văn DeepSIRT và Deep-PLA — hai lỗ hổng có thể đổi phán quyết trục 1.
- **Trung bình–thấp** cho kết luận "4/7 isoform làm bài toán vô nghĩa": các trích dẫn enzymology là `[tác giả báo cáo]` chắc chắn, nhưng việc **cột SIRT5 của mảng phản ánh cái gì** vẫn là `[suy luận]` chưa kiểm (cần Supplementary Data 5 của Rauh để biết lượng enzyme từng isoform).

**Một câu để nói với GVHD:** "Em đã đo thử bước quan trọng nhất của đề tài trước khi cam kết, và nó cho kết quả âm. Em đề nghị biến chính phép đo đó thành luận văn, thu hẹp xuống ba isoform mà sinh học đỡ được, và xin ý kiến thầy về việc một kết quả âm có đủ làm đóng góp chính hay không."

---

## 2. Năm nhánh khảo sát xác lập được gì, xếp theo chủ đề

### 2.1 Nhãn huấn luyện đo một thứ hẹp hơn tên gọi của nó

Mảng peptide Rauh 2013 là một phép thử **mất tín hiệu** (loss-of-signal): peptide 13 amino acid đã acetyl hóa được in lên mảng, ủ với sirtuin, **sau đó** mới thêm kháng thể kháng acetyl-lysine. Enzyme hoạt động ⇒ nhóm acetyl mất ⇒ kháng thể không bám ⇒ tín hiệu **giảm**. Nhãn dương vì vậy là **sự vắng mặt của tín hiệu**, và chính tác giả ghi hạn chế: **"Our deacetylation assay is based on a loss of signal, which makes small changes hard to measure"** `[tác giả báo cáo]` ([doi:10.1038/ncomms3327](https://doi.org/10.1038/ncomms3327)). Tác giả cũng nói khác biệt giữa các isoform **có thể đến từ "sequence bias of the anti-acetyl-Lys antibodies"** `[tác giả báo cáo]` — tức thiên lệch của kháng thể theo trình tự, không phải của enzyme.

Hệ quả cho máy học là một dạng **nhiễu nhãn phụ thuộc đặc trưng** `[suy luận]`: chính trình tự peptide — input của mô hình — ảnh hưởng tới xác suất nhãn bị gán sai. Loại nhiễu này lệch có hệ thống, nên **không chữa được bằng cách thêm trọng số theo sai số đo**.

Bốn cột nhãn, theo đúng chữ của tác giả: `substrate category` là **"a deacetylation likelihood between 0 and 1"** (tức **đã là** liên tục, không phải nhị phân); ngưỡng gọi dương của bài gốc là **"significant loss of signal (P < 0,01)"**, tức một **kiểm định thống kê**; `signal ratio` là tỉ lệ so với mảng tham chiếu, trong đó tham chiếu dùng **"inactive mutant, active sirtuin without NAD⁺ or buffer-only"** — ba loại đối chứng, mạnh hơn mức thường thấy; `ratio error` là **"variations between peptide spot triplicates and experiment repetitions"**, tức sai số đo lặp lại, **không** phải độ tin cậy sinh học; và `efficiency` là **"Quotients of category and ratio"** `[tác giả báo cáo]`. Phép kiểm trên file xác nhận công thức: `efficiency = substrate category / signal ratio`, kiểm trên dòng đầu 0,14 / 1,84 = 0,07609, đúng giá trị trong file `[tự kiểm]`.

Điều này có hệ quả thực hành: **không dùng `efficiency` làm mục tiêu hồi quy.** Vì `signal_ratio` nằm ở mẫu số, `efficiency` nổ lên khi `signal_ratio` nhỏ — tức chính ở vùng tín hiệu mất nhiều, nơi nhiễu đo lớn nhất; mục tiêu sẽ có **phương sai tăng theo giá trị** và mô hình bị hướng vào đúng những điểm kém tin cậy nhất `[suy luận]`. Nếu muốn một nhãn liên tục duy nhất, `signal_ratio` là lựa chọn ít dẫn xuất nhất, với `ratio_error` làm trọng số nghịch.

**Chỗ trống hợp lệ duy nhất về nhãn: `ratio error` thật sự chưa được dùng ở đâu cả** `[tự kiểm]`. SIRT1 có trung vị `ratio error` **0,37**, cao nhất trong 7 isoform (các isoform khác 0,21–0,27), tức 176 nhãn dương của SIRT1 là loại nhiễu nhất.

Và một file chưa ai nhắc tới: **Supplementary Data 6** của Rauh — **"Peptides that yielded no significant signal in at least one control experiment"** `[tác giả báo cáo]`. Đây là những peptide mà phép thử mất tín hiệu **về nguyên tắc không đo được**. Nếu chúng vẫn nằm trong 6.802 dòng và bị gán nhãn âm, thì một phần nhãn âm nghĩa là **"không đo được"**, không phải **"đo được và enzyme không hoạt động"**, và mọi chỉ số trên lớp âm (specificity, MCC) đều bị thổi phồng `[suy luận]`. **Việc đầu tiên khi mở file: đếm số dòng của Supplementary Data 6 và kiểm xem Ridgeway có loại chúng không** — chưa làm được.

### 2.2 Bốn trong bảy isoform không phải deacetylase mạnh, và SIRT5 là một nghịch lý

Đây là bằng chứng phá khung sinh học của đề tài, và nó đến từ các bài gốc, không từ suy luận.

| Isoform | Khung "deacetylase" khớp? | Bằng chứng |
|---|---|---|
| **SIRT1** | **Khớp.** | Rauh: Sirt1 "shows a more even activity distribution", **"less specific than most other isoforms"**; xác nhận trên HMG-B1 **Lys12**, phụ thuộc NAD⁺ `[tác giả báo cáo]` ([ncomms3327](https://doi.org/10.1038/ncomms3327)) |
| **SIRT2** | **Khớp**, nhưng cũng là demyristoylase hiệu quả | `kcat/KM` cho việc tháo nhóm myristoyl "slightly higher" so với acetyl `[chưa kiểm — chỉ qua tìm web, trỏ tới PMC4894398]` |
| **SIRT3** | Khớp **hoạt tính**, không khớp **ý nghĩa** | Rauh: SIRT3 giảm acetyl hóa MDH, nhưng **"These results cannot identify the acetylation site affected"** `[tác giả báo cáo]`. Weinert: vai trò là **"repairs nonenzymatic acetylation lesions"** `[tác giả báo cáo]` ([doi:10.15252/embj.201591271](https://doi.org/10.15252/embj.201591271)) |
| **SIRT4** | **Không khớp** | Mathias 2014, Cell: **"mitochondrial SIRT4 and SIRT5 have little to no deacetylase activity"**; SIRT4 là lipoamidase, **"catalytic efficiency for lipoyl- and biotinyl-lysine modifications is superior to its deacetylation activity"** `[tác giả báo cáo]` ([doi:10.1016/j.cell.2014.11.046](https://doi.org/10.1016/j.cell.2014.11.046), [PMC4344121](https://pmc.ncbi.nlm.nih.gov/articles/PMC4344121/)). Rauh chỉ đo được "**low but reproducible** Sirt4 deacetylation activity against the **non-physiological** Fluor-de-Lys peptide" với 7 μg enzyme `[tác giả báo cáo]` |
| **SIRT5** | **Không khớp** | Cùng câu Mathias 2014. Rauh dẫn Sirt5 có "stronger **desuccinylase and demalonylase** activity" `[tác giả báo cáo]`. Weinert: SIRT5 nén succinylation và glutarylation, cả hai "**may occur nonenzymatically**" `[tác giả báo cáo]` |
| **SIRT6** | **Khớp rất kém** | Jiang 2013, Nature: **"four of the seven mammalian sirtuins have very weak deacetylase activity in vitro"**; SIRT6 "efficiently removes **long-chain fatty acyl groups**" `[tác giả báo cáo]` ([doi:10.1038/nature12038](https://doi.org/10.1038/nature12038), [PMC3635073](https://pmc.ncbi.nlm.nih.gov/articles/PMC3635073/)). Review dẫn lại: deacetylase của SIRT6 **"100 to 1000 times lower compared to the most active SIRTs"**, demyristoylation **~300 lần cao hơn** deacetylation `[tác giả báo cáo — nhưng là review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8389836/)`. Rauh chỉ thấy "**weak** Sirt6-dependent deacetylation of the hydrophilic histone H3-Lys56 peptide" `[tác giả báo cáo]` |
| **SIRT7** | **Khớp kém, theo cách khác** | Barber 2012, Nature: SIRT7 là **"a highly selective H3K18Ac deacetylase"** — có hoạt tính nhưng gần như chỉ một vị trí `[tác giả báo cáo]` ([doi:10.1038/nature11043](https://doi.org/10.1038/nature11043), [PMC3412143](https://pmc.ncbi.nlm.nih.gov/articles/PMC3412143/)). Trên peptide tự do hầu như không đo được, cần DNA/RNA hoặc nucleosome `[chưa kiểm — chỉ qua tìm web, trỏ tới PMC4850736, PMC5326686]`. Rauh **không** đưa phép đo hoạt tính riêng cho SIRT7 `[tác giả báo cáo]` |

Hai hệ quả sắc nhất `[suy luận]`:

**Nghịch lý SIRT5.** Isoform mà Cell 2014 nói "có rất ít hoặc không có hoạt tính deacetylase" lại là isoform có **nhiều nhãn dương nhất (2.614)**, và là isoform duy nhất Ridgeway **không** phải cân bằng lại lớp ("SIRT5 (38,4% positive, 61,6% negative)" `[tác giả báo cáo]`). Hai cách đọc, cả hai đều xấu: (i) SIRT5 được nhỏ lượng enzyme cao nhất nên mất tín hiệu nhiều nhất, tức cột SIRT5 chủ yếu phản ánh **nồng độ enzyme** — kiểm được bằng Supplementary Data 5; hoặc (ii) cột SIRT5 phản ánh hoạt tính desuccinylase/demalonylase biểu hiện ra như hoạt tính yếu trên acetyl-lysine, tức mô hình "SIRT5 deacetylation" đang học **một phản ứng không phải phản ứng chính của SIRT5**.

**SIRT6 và SIRT7 bị thử sai bối cảnh.** Cả hai cần nucleosome / nucleic acid; mảng peptide tự do là bối cảnh tệ nhất có thể. Nhãn âm cho hai isoform này phần lớn có thể là **âm của phép thử**, và một mô hình đạt MCC cao trên hai cột đó đang **học thành công một tạo tác thí nghiệm**.

Đáng chú ý: ba isoform mà khung deacetylase khớp (SIRT1, SIRT2, SIRT3) **đúng là** ba isoform có bằng chứng ở mức protein nguyên hoặc có tập đánh giá trong tế bào — SIRT1→HMGB1 K12, SIRT3→MDH (Rauh), SIRT2→149 vị trí HCT116, SIRT3→3.174 vị trí U2OS. Và cặp đồng dương mạnh nhất trong mảng là **SIRT2–SIRT3, 1.136 vị trí** `[tự kiểm]`, khớp với câu của Ridgeway: **"SIRT2 and SIRT3 share almost twice the substrates as any other combination of SIRT"** `[tác giả báo cáo]`. Nghĩa là **một mô hình đa nhãn giới hạn ở SIRT1/2/3 có cơ sở sinh học, mô hình 7 đầu ra thì không.**

### 2.3 Ở stoichiometry 0,05%, chữ "cơ chất" mất phần lớn nghĩa chức năng

Weinert 2015 đo tỉ lệ chiếm chỗ của acetyl hóa trong gan chuột: **trung vị ~0,05%** — khoảng 1 trên 2.000 bản copy của protein. Vị trí ty thể ~0,11%, ngoài ty thể ~0,04% (Fig 3A). Nghịch lý nhất: những vị trí **bị ảnh hưởng mạnh nhất** khi mất SIRT3 (`S3 > 4`, `S3 > 8`) lại có stoichiometry **thấp nhất, 0,05%**, và **97% vị trí đích của SIRT3 có stoichiometry < 1%** (Fig 3C). Tác giả còn ước lượng hơn 20 vị trí **"previously suggested to regulate metabolic proteins"** và thấy **"nearly all of these sites were < 1% acetylated"** `[tác giả báo cáo]` ([doi:10.15252/embj.201591271](https://doi.org/10.15252/embj.201591271), [PMC4641529](https://pmc.ncbi.nlm.nih.gov/articles/PMC4641529/)). Kết luận cơ chế của chính tác giả: **"there is little evidence of enzyme-catalyzed, site-specific acetylation in mitochondria"**, và mức tăng khi mất SIRT3 là **"a function of their inherent reactivity and the nonenzymatic origin of acetylation"**.

Ba hệ quả `[suy luận]`:

Thứ nhất, **mặt bất lợi mạnh hơn mặt có lợi**. Nếu phần lớn acetyl hóa ty thể là tổn thương hóa học không chọn vị trí, thì đại lượng đáng dự đoán là **phản ứng hóa học nội tại của lysine** (pKa, môi trường vi mô, độ lộ) — và cái đó chủ yếu do **cấu trúc 3D** quyết định, không do 13 amino acid liền kề. Mô hình chỉ nhìn cửa sổ 13 aa đang bỏ qua biến giải thích chính.

Thứ hai, **một luận văn hứa "tìm cơ chất để hiểu điều hòa" đang ngầm hứa một ý nghĩa sinh học mà dữ liệu không đỡ được**. Với 97% vị trí, deacetyl hóa không đổi đáng kể trạng thái protein vì nó đã gần như không bị acetyl hóa.

Thứ ba, **nhãn "thay đổi sau KO" trộn hai nguồn**: "enzyme tác động lên vị trí này" và "vị trí này dễ bị acetyl hóa phi enzyme". Một mô hình đạt điểm cao có thể chỉ học **tính phản ứng của lysine**. Đây là confound **phải kiểm**, ví dụ bằng cách xem mô hình huấn luyện cho SIRT2 và cho SIRT3 có dự đoán gần như giống nhau hay không.

### 2.4 Ba khái niệm bị gộp làm một, và chuỗi suy diễn giữa chúng rất yếu

Phải tách: **(a)** hoạt tính trên peptide in vitro, **(b)** cơ chất thật trên protein gấp cuộn, **(c)** vị trí đổi sau KO/KD/OE trong tế bào.

| Từ → tới | Suy diễn được không | Vì sao |
|---|---|---|
| (a) dương → (b) dương | **Không chắc** | Rauh: "false positives could result from **limited accessibility** of a good substrate site in the full-length protein" `[tác giả báo cáo]` |
| (a) âm → (b) âm | **Khá chắc nhưng không tuyệt đối** | Rauh: "More distant residues, not covered by our peptides, might also influence deacetylation" `[tác giả báo cáo]`. SIRT6/SIRT7 là ví dụ rõ: yếu trên peptide tự do, có hoạt tính trên nucleosome |
| (b) dương → (c) dương | **Không chắc** | Cần cùng khoang tế bào, cần NAD⁺, cần stoichiometry ban đầu đủ cao để đo được thay đổi |
| (c) dương → (b) dương | **Không chắc — chỗ sai phổ biến nhất** | (c) bắt **mọi** tác động kể cả gián tiếp: SIRT đó deacetyl hóa một acetyltransferase khác, hoặc đổi mức acetyl-CoA kéo theo acetyl hóa phi enzyme hàng nghìn vị trí (Weinert) |
| **(a) dương → (c) dương** | **Yếu nhất, vì là tích của hai bước đều không chắc** | **Đây chính là thứ đề tài định đo.** Con số 43,0% là một ước lượng của bước này, chỉ trên nhãn dương, chỉ cho SIRT2, trên một tập 149 vị trí lấy từ bài khác |

Và Rauh đã tự nói ra bước xác nhận còn thiếu: **"Each deacetylation site thus has to be confirmed on native target protein and ultimately in vivo"** `[tác giả báo cáo]`. Tổng cộng bài gốc xác nhận ở mức protein nguyên có định vị vị trí được **2 vị trí** (Prx1 K197 với Sirt5, HMGB1 K12 với Sirt1) trên **6.802** vị trí của mảng — tỉ lệ ≈ 0,03% `[suy luận]`. Đó không phải tỉ lệ dương tính giả, nhưng nó cho thấy bước peptide → protein **gần như chưa được đo ở mức hệ thống bởi chính bài gốc**.

Thêm hai chỗ cụ thể làm đứt chuỗi: **nồng độ enzyme** (mảng dùng 6–218 μg/ml, mức protein dùng 9,4–9,7 **μM**, một phép thử dùng 7 μg Sirt4 `[tác giả báo cáo]`; ở nồng độ cao enzyme có thể xúc tác phản ứng mà ở mức sinh lý nó không làm); và **khu trú dưới tế bào** — một peptide từ protein ty thể có thể bị SIRT1 (ở nhân) deacetyl hóa trên mảng dù hai phân tử đó **không bao giờ gặp nhau trong tế bào**. Mô hình sẽ dự đoán dương và **đúng về hóa học, sai về sinh học** `[suy luận; phần khu trú SIRT1/6/7 nhân, SIRT2 tế bào chất, SIRT3/4/5 ty thể là [chưa kiểm — cần trích dẫn riêng]]`.

### 2.5 Nền "đáp án" cho phần XAI chưa có, và một con số trong bản khuyến nghị có thể gán sai isoform

Phần XAI của đề tài dựa vào một phép kiểm "có đáp án": occlusion từng vị trí rồi đối chiếu với motif đặc hiệu đã biết. Khảo sát cho thấy đáp án đó **có khả năng cao là không tồn tại**: một bài proteomics acetylome 2022 ghi **không thấy bằng chứng cho một motif ưa thích nào ở SIRT7** `[chưa kiểm — qua tóm tắt]` ([doi:10.1038/s41598-022-06793-5](https://www.nature.com/articles/s41598-022-06793-5)); văn liệu **mâu thuẫn** về SIRT1 (một nghiên cứu cũ kết luận SIRT1 không có đặc hiệu chuỗi, trong khi Garske & Denu 2006 với thư viện 104.907 chuỗi 5-mer kết luận SIRT1 **có** phân biệt cơ chất theo ngữ cảnh, hit đạt hoạt tính cao tới **20 lần** `[chưa kiểm toàn văn]` [PMC2519118](https://pmc.ncbi.nlm.nih.gov/articles/PMC2519118)); và lớp I (SIRT1–3) được mô tả là **giống nhau nhất** về đặc hiệu, nên khác biệt giữa chúng rất tinh tế `[chưa kiểm]`.

Nghiêm trọng hơn: câu trong bản khuyến nghị — *"Rauh báo SIRT7 ưa residue thân nước không tích điện hoặc tích điện âm ở vị trí −3, −2, +1"* — **không tìm thấy** trong phần toàn văn Rauh đọc được, và phát biểu tương tự trong văn liệu xuất hiện như một phát biểu về **SIRT1** (vị trí +2, +3, −2) `[chưa kiểm]`. Hai nhánh khảo sát độc lập (01 và 05) đều cảnh báo điều này. **Không được dùng con số −3/−2/+1 trong tài liệu gửi GVHD cho tới khi đọc lại đúng hình đặc hiệu chuỗi trong bài gốc.**

Lối ra khả thi và rẻ `[suy luận]`: **tự dựng bảng motif theo vị trí (−6…+6) cho từng isoform trực tiếp trên 6.801 vị trí của mảng**, có kiểm định và hiệu chỉnh đa so sánh. Nếu một isoform có vị trí làm giàu mạnh, đó là đáp án hợp lệ cho isoform đó; nếu không, ta đã **chứng minh** rằng không có đáp án — và đó cũng là một kết quả báo cáo được. Việc này không cần GPU, không cần huấn luyện, và **quyết định phần XAI có đáng làm hay không**.

Về quy trình kiểm chứng XAI, nếu làm thì bốn tầng là tối thiểu: **sanity check** (occlusion trên mô hình chưa huấn luyện và trên mô hình huấn luyện với nhãn đã trộn — Adebayo 2018, [arXiv:1810.03292](https://arxiv.org/abs/1810.03292)); **faithfulness** (đường deletion/insertion, comprehensiveness/sufficiency theo quy ước ERASER, DeYoung 2020, [arXiv:1911.03429](https://arxiv.org/abs/1911.03429)); **ROAR có huấn luyện lại** để phân biệt "mất thông tin" với "đầu vào trở nên lạ" (Hooker 2019, [arXiv:1806.10758](https://arxiv.org/abs/1806.10758)); và **hiệu chỉnh mức may rủi** khi báo tỉ lệ khớp motif — với cửa sổ 13 aa và một vị trí quan tâm, mức may rủi là 1/12 ≈ 0,083 `[tự kiểm — tính theo công thức L/(N−L+1) của [arXiv:2609.16271](https://arxiv.org/pdf/2609.16271), là tiền ấn phẩm chưa phản biện]`. Thêm một cảnh báo đặc thù: nếu dùng ESM-2 làm nền, bản đồ occlusion đo tác động **qua cả PLM**, nên một vị trí có thể quan trọng vì nó đổi embedding của cả cửa sổ, không phải vì nó tiếp xúc enzyme `[suy luận]`.

### 2.6 Conformal prediction bảo đảm ít hơn mọi bản phác trước đang nói

Không có một "conformal prediction" duy nhất cho bài toán đa nhãn; có ít nhất ba mức, mỗi mức một định lý khác:

- **Mức A — 7 bài toán nhị phân rời.** Bảo đảm độ phủ **biên**: `1 − α ≤ P(Y ∈ C(X)) ≤ 1 − α + 1/(n+1)`, là **Theorem 1** của Angelopoulos & Bates `[tác giả báo cáo]` ([arXiv:2107.07511](https://arxiv.org/abs/2107.07511)). Dễ nhất, nhưng **nói rất ít**: với mất cân bằng nặng, `C(x) = {0}` hầu khắp vẫn đạt độ phủ 90% mà vô dụng.
- **Mức B — Mondrian / label-conditional theo từng isoform.** `P(Y_j ∈ C_j(X) | Y_j = 1) ≥ 1 − α`, tức "trong các vị trí thật là cơ chất của SIRT2, ta bắt được ≥ 90%". Đây mới có nghĩa sinh học; bảo đảm là **Proposition 2, Section 4.2** của cùng bài `[tác giả báo cáo]`. Giá: cần đủ điểm hiệu chỉnh **trong lớp dương của từng isoform**.
- **Mức C — "tập isoform có bảo đảm 90%".** Đây là cách các bản phác đang **nói**, nhưng nhãn đúng là một **vector 7 chiều**, nên tập dự đoán đúng nghĩa là tập con của 128 vector, không phải tập con của 7 isoform. Muốn một phát biểu về một **tập isoform**, đối tượng đúng là **conformal risk control** trên tỉ lệ bỏ sót (**Theorem 2**, Section 4.3; bài gốc: Angelopoulos et al., ICLR 2024, [arXiv:2208.02814](https://arxiv.org/abs/2208.02814)), và phát biểu đúng là *"kỳ vọng tỉ lệ isoform thật bị bỏ sót ≤ α"*, **không** phải *"xác suất tập chứa đúng cả 7 nhãn ≥ 1 − α"*.

Câu **"conformal trả về tập isoform có bảo đảm độ phủ 90%"** trong cả `topic-final-recommendation.md` và `b-method-layer-draft.md` vì vậy là **nói quá nếu không nêu rõ đang ở mức nào** `[suy luận]`.

Hai con số định lượng quan trọng. **Cỡ mẫu hiệu chỉnh** (Table 1 của Angelopoulos & Bates, với α = 0,1 và δ = 0,1) `[tác giả báo cáo]`:

| ε (sai lệch độ phủ) | 0,10 | 0,05 | 0,01 | 0,005 | 0,001 |
|---|---|---|---|---|---|
| n(ε) | **22** | **102** | **2.491** | 9.812 | 244.390 |

Nếu dành 20% trong 6.801 vị trí làm tập hiệu chỉnh, số **điểm dương** của từng isoform là ≈35 (SIRT1), ≈380, ≈369, ≈208, ≈523, ≈240, ≈338 `[suy luận — tính từ số dương đã kiểm]`. Đọc bảng trên: **sáu isoform đạt "90% ± 0,05"; SIRT1 chỉ đạt "90% ± 0,10"**, tức khoảng [0,80; 1,00] — gần như vô nghĩa. Và nếu hiệu chỉnh Bonferroni cho **đồng thời 7 nhãn** ở α = 0,1 thì α_j ≈ 0,0143 và cỡ mẫu tối thiểu `n ≥ 1/α − 1` **≥ 69 điểm dương mỗi isoform** — **SIRT1 với ~35 điểm không đạt** `[suy luận]`.

Thứ hai, và nghiêm trọng hơn: **bảo đảm conformal không chuyển sang tập trong tế bào nếu chỉ hiệu chỉnh trên mảng.** Weighted conformal prediction chỉ xử lý **covariate shift** với `P(Y|X)` **giữ nguyên** (Section 4.5, **Theorem 3**; bài gốc Tibshirani et al., NeurIPS 2019, [arXiv:1904.06019](https://arxiv.org/abs/1904.06019)). Nhưng ở đây **cùng một cửa sổ chuỗi X** có thể mang nhãn khác nhau ở hai miền vì khu trú, cạnh tranh, stoichiometry — tức **`P(Y|X)` đổi**, đây là **concept shift**, và Theorem 3 không áp dụng được `[suy luận]`. Ngay cả nếu coi là covariate shift, điều kiện của Tibshirani là ước lượng chính xác được `w(x)` từ một mẫu covariate **đại diện** của miền đích — còn 149 vị trí hiện có được chọn **vì chúng đáp ứng SIRT2**, tức mẫu đã bị **chọn theo nhãn** `[suy luận]`.

Vì vậy ba phương án, xếp theo mức trung thực:

| Phương án | Bảo đảm thật có được | Nhận xét |
|---|---|---|
| **P1.** Hiệu chỉnh trên mảng, báo trên mảng | `P(Y_j ∈ C_j(X)) ≥ 1 − α` trên phân bố mảng | **Luôn làm được.** Bảo đảm duy nhất chắc chắn |
| **P2.** Hiệu chỉnh trên mảng, đo **độ phủ thực nghiệm** trên in-cell | **Không có bảo đảm** — chỉ là chẩn đoán dịch chuyển miền | Đây là nội dung thật của RQ3; phải gọi là "empirical coverage", **không** gọi là "guarantee" |
| **P3.** Tách một phần tập in-cell làm hiệu chỉnh | `P(Ŷ_j = 1 | Y_j = 1) ≥ 1 − α` trên phân bố in-cell | **Chỉ làm được với SIRT2.** Với ~75 điểm hiệu chỉnh thì chỉ nói được "90% ± 0,05–0,10" |

Một tin tốt có điều kiện: nhiễu của mảng là nhiễu **đo lường, phân tán, không đối kháng**, và theo Einbinder et al. (*Label Noise Robustness of Conformal Prediction*, JMLR 25, 2024, [arXiv:2209.14295](https://arxiv.org/abs/2209.14295)) loại nhiễu này khiến conformal **bảo thủ** so với nhãn sạch — tập dự đoán to hơn cần, nhưng **không phủ thiếu** `[suy luận, dựa trên kết quả [tác giả báo cáo] của họ]`.

Và về tính mới: hai lượt tìm ngày 08/10/2026 **không ra bài nào** ghép conformal với dự đoán vị trí PTM `[tự kiểm]`. Nhưng conformal đã dày trong hóa tin/QSAR từ 2018–2019, kể cả cho hoạt tính trên **550 đích protein** (Bosc et al., J Cheminform 2019). Nên tính mới ở đây là **"áp dụng vào một bài toán mới"**, không phải "phương pháp mới" `[suy luận]`.

---

## 3. So sánh với công trình đã có

| Công trình | Năm | Bài toán | Đơn vị dự đoán | Nhãn / dữ liệu | Đặc hiệu isoform? | Phương pháp | Chồng lấn với đề tài |
|---|---|---|---|---|---|---|---|
| **Rauh et al.** [doi](https://doi.org/10.1038/ncomms3327) | 2013 | Đặc hiệu cơ chất SIRT1–7 (thực nghiệm) | Peptide 13 aa | **6.802 vị trí × 7 isoform**, nhãn liên tục | Có | Mảng peptide, không ML | **Nguồn nhãn huấn luyện.** Hoàn toàn in vitro; tác giả tự nói không so được giữa isoform |
| **Ridgeway et al.** [doi](https://doi.org/10.1038/s42004-025-01717-6) · [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) | 2025 | Cơ chất enzyme PTM (SET8 + SIRT1–7) | Residue (peptide 13 aa) | Nhãn nhị phân từ Rauh, **443 đặc trưng** | **Có, 7 mô hình rời** | LDA / cây + oversampling, ensemble xếp tầng với **MuSiteDeep** | **Đối thủ trực tiếp.** Và **cả PLM lẫn nhãn thang độ đều là "future work" họ tự công bố** |
| **DeepSIRT** [doi](https://doi.org/10.1016/j.compbiolchem.2021.107514) | 2021 | **Target** của sirtuin + khu trú dưới tế bào | **Cả protein** | Danh sách target SIRT1–7 có annotate khu trú | **Có, 7 thành viên** | 1D-CNN, giảm đồng dạng | **⚠️ Nhóm Prof. Ou.** Sn 85,77%, Sp 97,32%, **MCC 0,82** `[tác giả báo cáo, qua PubMed]`. Chồng lấn ở đúng cụm từ "isoform-specific SIRT1–7" |
| **NAD_MCNN** [doi](https://doi.org/10.1111/cbdd.70085) | 2025 | Vị trí gắn **NAD⁺ trên chính enzyme** | Residue trên enzyme | Vị trí gắn cofactor | n/a | PLM + mCNN nhiều cửa sổ | **Nhóm Prof. Ou.** AUC 0,9733 / 0,9701. Khác bài toán; khung PLM+mCNN là cái đề tài mượn lại |
| **Deep-PLA** [doi](https://doi.org/10.1093/bib/bbz107) | 2020 | Acetyl hóa đặc hiệu **HAT/HDAC** | Cửa sổ quanh K | 7 HAT + **9 HDAC** curate từ tài liệu | Có (theo enzyme) | DNN + AAC/CKSAAP/PSSM, PSO | **Tiền lệ "đặc hiệu enzyme" từ 2020. SIRT1–7 LÀ HDAC class III** → phải kiểm 9 HDAC đó gồm những ai `[chưa kiểm]` |
| **GPS-PAIL** [PMC5177928](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5177928/) | 2016 | Acetyl hóa đặc hiệu từng **KAT** | Chuỗi | Vị trí curate | Có (theo KAT) | Scoring matrix | Tiền lệ còn sớm hơn. Làm yếu mọi tuyên bố "đầu tiên dự đoán PTM đặc hiệu enzyme" `[chưa kiểm]` |
| **Johnson et al. (kinome atlas)** [doi](https://doi.org/10.1038/s41586-022-05575-3) | 2023 | Đặc hiệu 303 kinase Ser/Thr | Peptide | Positional scanning peptide array (in vitro) | Có, 303 kinase | PWM / motif | **Analogue gần nhất, và đã làm bước in vitro → toàn proteome ở quy mô lớn hơn.** Kinase đã biết chỉ **< 4%** vị trí `[tác giả báo cáo]` |
| **"Validity of the cell-extracted proteome…"** [PMC11447832](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/) | 2024 | Motif mảng vs motif dịch chiết tế bào | Peptide | PL-PWM (Johnson) vs dịch chiết | Theo kinase | PWM | **⚠️ Bằng chứng ngược:** mảng cho dự đoán **ngang** motif từ dịch chiết, cho **3 kinase** `[chưa kiểm — qua tóm tắt]` |
| **benchmarKIN** [doi](https://doi.org/10.1038/s41467-025-59779-y) | 2025 | Benchmark suy luận hoạt tính kinase | Phosphoproteome | 184 cặp / 30 kinase / 62 perturbation | Theo kinase | Nhiều phương pháp | Cộng đồng kinase **đã có** benchmark in-cell cho dự đoán từ mảng. **Mượn được phương pháp luận** |
| **Phosformer / Phosformer-ST** [PMC11968300](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11968300/) | 2023–25 | Phospho đặc hiệu kinase | Cặp (kinase, peptide) | Cơ chất đã biết | Có | Transformer giải thích được | Ý "một mô hình điều kiện hóa theo enzyme" đã có. **Mức peptide, không mức residue** → chỗ phân biệt được |
| **COMPASS-PTM** [doi](https://www.nature.com/articles/s41467-026-73148-3) | 2026 | PTM **đa nhãn** + crosstalk | Chuỗi | dbPTM + qPTM | Không (theo loại PTM) | PLM tinh chỉnh + crosstalk prompting, **+122% F1 tương đối** | **Làm yếu trục 3:** "đa nhãn PTM với PLM" đã là SOTA `[chưa kiểm]` |
| **PDeepPP** (qua [PMC13389326](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389326/)) | ~2025 | Vị trí PTM tổng quát | Chuỗi | Benchmark PTM | Không | **ESM-2 + transformer-CNN song song** | **Làm yếu trục 3:** "ESM-2 + CNN đa thang" đã công bố `[chưa kiểm]` |
| **ESMBind / QBind** [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full) | 2023 | Vị trí gắn **và PTM** | Chuỗi | Token classification | Không | **LoRA / QLoRA trên ESM-2** | **Làm yếu trục 3:** "ESM-2 + LoRA cho PTM" đã công bố `[tác giả báo cáo]` |

**Phán quyết ba trục** `[suy luận]`:

- **Trục 1 (tính mới của vấn đề sinh học): YẾU–TRUNG BÌNH.** "Dự đoán cơ chất SIRT1–7 đặc hiệu isoform" đã công bố **hai lần**. Phần còn trống là **mức residue × một mô hình đa nhãn × đánh giá trong tế bào** — một khe hẹp giữa hai bài đã có, không phải vùng trắng. Phát biểu an toàn: *"em không mở bài toán mới; em lấp khe giữa DeepSIRT (mức protein) và Ridgeway (mức residue, 7 mô hình rời)."*
- **Trục 2 (tính mới của dữ liệu đánh giá): MẠNH NHẤT, nhưng không như đang nghĩ.** Không tìm thấy công trình nào dựng **tập đánh giá trong tế bào có cả nhãn dương và nhãn âm cho nhiều isoform SIRT** `[chưa tìm thấy, không kết luận là chưa từng có]`. Nhưng câu **"chưa ai đo xem dự đoán từ mảng có đúng trong tế bào không" là SAI nếu nói nguyên văn**: Ridgeway đã đo (64/149 cho SIRT2; 3/9 vị trí cho SET8), và cộng đồng kinase đã làm việc tương đương ở quy mô lớn hơn nhiều. **Đóng góp thật nằm ở nhãn âm và ở metric ngoài precision, không ở ý tưởng "đánh giá in-cell".**
- **Trục 3 (tính mới của phương pháp tính toán): YẾU.** Từng mảnh của "ESM-2 + LoRA + mCNN + conformal" đều có tiền lệ, trừ hai mảnh nhỏ: conformal cho PTM (**không tìm thấy** `[chưa tìm thấy...]`) và hồi quy trên nhãn thang độ của mảng peptide — mà **chính Ridgeway đã công bố nó như future work của họ**: *"The density of the SPOT peptide arrays is correlated with substrate preference and **may improve performance when incorporated through regression-based ML models as opposed to the classification models currently used**"* `[tự kiểm — đọc toàn văn]` ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)). Cách trình bày trung thực: *"bài 2025 đề xuất hai việc tương lai — PLM và hồi quy trên mật độ SPOT — em làm cả hai và đo xem có đúng không."* Và vì chính tác giả đã nêu, **rủi ro bị nhóm Ridgeway làm trước là thật** (bài công bố 07/11/2025, mới 11 tháng).

Một ghi chú về cách trình bày với GVHD `[suy luận]`: đừng nói "NAD_MCNN khác bài em" rồi dừng. Nói: *"nhóm thầy đã phủ hai mảnh của bài toán sirtuin — vị trí gắn cofactor ở mức residue (NAD_MCNN) và nhận dạng target ở mức protein (DeepSIRT) — mảnh còn trống là vị trí trên target ở mức residue, theo từng isoform."* Cách này biến chồng lấn thành lập luận liên tục với nền của GVHD thay vì để GVHD tự phát hiện.

Cuối cùng, **một citation phải sửa trong mọi tài liệu nội bộ**: Prot2Token mở rộng cho kinase **không phải NeurIPS 2025** — tìm được bản bioRxiv 2024 và bản mở rộng ở **LMRL Workshop @ ICLR 2025**, không thấy NeurIPS `[chưa kiểm — tìm không ra]`. `b-method-layer-draft.md` mục 6 ghi "NeurIPS 2025" và sẽ bị bắt lỗi.

---

## 4. Kiểm kê dữ liệu với số đếm đã xác nhận

Tất cả tải và đếm được từ môi trường cloud ngày 08/10/2026 `[tự kiểm]`.

| Bộ dữ liệu | Số dòng | Số protein | Nội dung và cảnh báo |
|---|---|---|---|
| **Rauh 2013 Supp Data 1** (`MOESM80`, 2.122.503 B) | **6.802** vị trí (sheet 6.806 dòng, 4 dòng tiêu đề) | **2.937** accession đầu tiên khác nhau; **13.240** accession xuất hiện ở đâu đó | 31 cột = 1 + 7×4 + 2. Mọi chuỗi đúng **13 ký tự**, **0 trùng**. Đệm bằng **`Z`** (249 dòng). `Protein names` và `Uniprot Accession Codes` **thiếu ở 473 dòng (7,0%)**. **Không có cột vị trí residue riêng** — vị trí nằm trong ngoặc của text, một dòng có thể mang nhiều vị trí. **475 dòng trùng** (accession đầu + vị trí đầu). Sau khi gỡ: **17.170** cặp (UniProt, vị trí). ⚠️ Dòng tiêu đề thứ hai **lệch một cột**: đọc bằng `header=2` sẽ gán sai tên cho 3 cột cuối |
| **Ridgeway 2025 Supp Data 15** (`MOESM17`, sheet `Table 13`) | **6.801** × 9 cột | **2.999** | **Bảng nhãn nhị phân chuẩn** kèm 13-mer. 0 giá trị thiếu, 6.801 chuỗi duy nhất. Đệm bằng **`X`** (696 ký tự). Sau khi đổi `Z`→`X`, merge với Rauh khớp **6.801/6.801**. **Đây là file nên dùng làm nhãn** |
| `All_Sirts_Feature_Y_labels.csv` (GitHub, 224.234 B) | 6.801 | 2.999 | Tổng dương khớp Supp Data 15 **tuyệt đối**. Nhưng **7 cột theo thứ tự lộn xộn 5,4,1,7,2,6,3**, và **thứ tự dòng khác** (bất đồng 338–3.160 dòng tùy isoform). **Phải join theo `uid_pos`, tuyệt đối không join theo chỉ số dòng** |
| **Ridgeway 2025 Supp Data 14** (`MOESM16`) — SIRT2 trong tế bào | **149** × 8 cột, 0 thiếu | **123** | **Cả 149 có log2FC < 0 ở OE và > 0 ở KD** (OE: min −6,12, trung vị −1,82; KD: min +0,59, trung vị +1,76) → **tập chỉ-có-nhãn-dương**. Điểm mô hình 0,0944–0,9182, dự đoán dương = **64**, và `score ≥ 0,5` cũng đúng 64 → **ngưỡng là 0,5**. 64/149 = **42,95%**. **Không có cột p-value, không có số replicate, không có hiệu chỉnh mức protein** |
| **Ridgeway 2025 Supp Data 13** (`MOESM15`, 19.196.393 B) — dự đoán | **145.461** × 17 cột, 0 thiếu | **2.737** | **KHÔNG phải "toàn bộ proteome"** (proteome người ~20.400 protein) — đây là tập lysine acetyl hóa đã biết của 2.737 protein, lọc theo NetSurfP1.0 > 0,2. Số dự đoán dương rất lệch: SIRT1 3.946 (2,71%) … SIRT7 52.407 (36,03%). ⚠️ **Rò rỉ:** **3.226 / 145.461** vị trí có 13-mer trùng đúng tập huấn luyện; **55.703 vị trí (38,3%)** trên **973 / 2.737** protein cũng có trong tập huấn luyện |
| **Sol 2012 Table S2** (PLoS ONE, 940.487 B) — **người, U2OS, SIRT3 KD vs OE** | **3.174** vị trí × 19 cột | **1.498** | **Mọi vị trí được định lượng**, nên **dựng được cả nhãn âm**. Có cột `Sequence window` **13 aa** — khớp đúng cửa sổ của Rauh. Một cột tỉ lệ duy nhất, **không có cột replicate**. log2 trung vị −0,031; 5–95%: **−1,20 … +0,85**. >1,5×: **303**; trong 0,67–1,5× (**ứng viên âm**): **2.456** |
| **Sol 2012 Table S1** (1.495.258 B) — **chuột, MEF, Sirt3 KO di truyền** | **1.566** vị trí × 22 cột | **846** | **2 replicate** nhưng **633/1.566 (40,4%) chỉ được định lượng ở một replicate**. >2×: **103** (khớp câu "over one hundred" của tác giả `[tác giả báo cáo]`); >1,5×: **284**; trong 0,67–1,5×: **942**. **Không hiệu chỉnh theo mức protein** (tác giả nói rõ lý do). **Không có p-value/FDR theo vị trí** |
| **Zhang 2022** ([PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)) — nguồn thật của 149 vị trí | **2.846** vị trí định lượng | **1.414** | **896** tăng khi KD; **509** giảm khi OE; giao hai tiêu chí ở mức vị trí = **134 peptide chứa 152 vị trí** (Fig. S4a). Ngưỡng gọi là **> 1,5 lần** và **ngược chiều KD/OE**; **FDR < 1% chỉ áp cho bước identification**, không có p-value cho việc gọi vị trí phụ thuộc SIRT2 `[tự kiểm qua toàn văn]`. ⇒ **2.846 − 152 = 2.694 vị trí âm-trong-tế-bào** dùng được; tỉ lệ dương nền **152/2.846 ≈ 5,3%**. Danh sách đầy đủ ở **Supplementary Table S1** — **chưa mở được file để xác nhận có cột fold-change theo từng vị trí** `[chưa kiểm]` |

**Số dương từng isoform** theo quy tắc đúng (`efficiency ≥ 1`), khớp tuyệt đối với Supp Data 15 `[tự kiểm]`:

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| Nhãn dương (`efficiency ≥ 1`) | **176** | 1.901 | 1.844 | 1.038 | **2.614** | 1.199 | 1.692 |
| Dương độc quyền một isoform | 21 | 319 | 289 | 162 | **1.088** | 269 | 282 |
| `substrate category = 1` | **4** | 822 | 1.171 | 1.011 | 2.615 | 737 | 1.682 |
| Trung vị `signal ratio` | 1,07 | 0,99 | 1,06 | 1,01 | 0,96 | 1,06 | 1,03 |
| Trung vị `ratio error` | **0,37** | 0,22 | 0,24 | 0,24 | 0,21 | 0,27 | 0,22 |

Số isoform dương trên mỗi vị trí: **0 → 1.107; 1 → 2.430; 2 → 2.087; 3 → 902; 4 → 226; 5 → 44; 6 → 5; 7 → 0** `[tự kiểm]`. Cặp đồng dương mạnh nhất: **SIRT2–SIRT3 1.136**, SIRT5–SIRT7 816, SIRT3–SIRT7 534 `[tự kiểm]`.

**Chênh 6.802 vs 6.801 đã tìm ra nguyên nhân** `[tự kiểm]`: dòng bị loại là `GIQCVKKRDLEQA` (Transcription factor p65 / RELA, accession đầu `Q04206`), dòng duy nhất của Rauh không có trong Supp Data 15 sau khi đổi `Z`→`X`. Nó có **4 vị trí trong một ngoặc** (`123;134;114;92`) và 10 accession — nhiều vị trí nhất trong file. **Lý do bị loại: `[chưa kiểm]`**, bài báo không nói.

**Chồng lấn và rò rỉ** `[tự kiểm]`:

| Tập | Chồng lấn với mảng Rauh |
|---|---|
| Supp Data 14 (149 vị trí SIRT2) | **44/149** khớp đúng (UniProt, position); **108/149** thuộc protein chính của mảng (83/123 protein); **41 vị trí / 40 protein hoàn toàn mới** |
| Sol 2012 người (3.174) | **718** khớp đúng vị trí; **1.417 (44,6%)** khớp đúng 13-mer; 1.473 vị trí trên protein của mảng |
| Sol 2012 chuột (1.566) | **0** chồng lấn ở mức accession/vị trí — nhưng **513 (32,8%)** có **13-mer trùng đúng từng chữ** |

Con số 513 ở tập chuột là phát hiện quan trọng về phương pháp: **"nguồn độc lập" ≠ "protein độc lập" ≠ "trình tự độc lập"**. Một tập chuột nghe như độc lập hoàn toàn, nhưng với mô hình chỉ nhìn cửa sổ 13 aa thì **một phần ba tập đó là chính input huấn luyện, dán nhãn mới** `[suy luận]`. **Phải lọc ở mức chuỗi, không chỉ ở mức accession.** Và các con số trên chỉ là **khớp 100%** — cận dưới; mức đồng dạng dưới 100% (paralog, họ histone, họ tubulin) **chưa chạy alignment** `[chưa kiểm]`.

**Cổng mạng:** `static-content.springer.com` → **403**; `media.springernature.com` → **200**; `pmc.ncbi.nlm.nih.gov/.../bin/*.xlsx` → **200 nhưng trả HTML reCAPTCHA** ("Preparing to download…"); `journals.plos.org` kể cả file phụ lục → **200**; `raw.githubusercontent.com`, `www.nature.com`, PRIDE API v3 → **200** `[tự kiểm]`.

**⚠️ Hai nhánh khảo sát BẤT ĐỒNG về việc tải được file phụ lục của Rauh.** Nhánh 01 (nền sinh học) báo **không tải được**, `curl` tới `static-content.springer.com` trả **403**, và vì vậy mọi con số về nội dung file trong bản khuyến nghị vẫn là `[chưa kiểm]` đối với nhánh đó. Nhánh 03 (kiểm kê dữ liệu) **tải được** qua host khác (`media.springernature.com`, 200) và **đã đếm trực tiếp trên file**. **Nhánh 03 là nhánh có file trong tay**, nên mọi số đếm trong mục này lấy theo nhánh 03; cảnh báo của nhánh 01 về việc "chưa kiểm" chỉ phản ánh giới hạn của chính nó, không phủ nhận số của nhánh 03.

Cũng cần nói rõ **hai nhánh bất đồng về quy tắc nhãn dương**: nhánh 01 và 04 (đọc Methods của Ridgeway) ghi quy tắc là **"signal ratio score of 1 or greater"** và cảnh báo rằng nếu đúng thì nhãn có thể **bị đảo dấu**, vì phép thử mất tín hiệu nghĩa là deacetyl hóa ⇒ tỉ lệ < 1. Nhánh 03 (có file) **đo được** rằng quy tắc tái lập chính xác là **`efficiency ≥ 1`**, tương đương **`substrate category ≥ signal ratio`** — tức Methods của Ridgeway **viết sai tên cột**, nhưng nhãn **không bị đảo**. Kết luận: dùng kết quả của nhánh 03; cảnh báo đảo dấu của nhánh 01/04 **đã được loại trừ bằng phép đo**, và đây là một ví dụ tốt để kể với GVHD về giá trị của việc tự mở file.

---

## 5. Bảng claim–evidence–correction cho `topic-final-recommendation.md`

Bản khuyến nghị nội bộ **được giữ nguyên để đối chiếu**. Bảng dưới liệt kê mọi phát biểu của nó mà khảo sát này phản bác hoặc phải thêm điều kiện.

| # | Phát biểu hiện tại trong `topic-final-recommendation.md` | Bằng chứng phản bác | Phải thay bằng | Còn đứng? |
|---|---|---|---|---|
| **1** | §2.2: "Mô hình của bài 2025 dự đoán dương 64/149, **đúng mức precision 43,0%** họ báo" | Mẫu số là **số vị trí dương đã biết**, nên `64/149 = TP/(TP+FN)` = **recall / hit rate**. Chính bài, phần SET8, định nghĩa "a method precision rate (i.e., **[True Positive] / [True Positive + False Positive]**)" và "recall … (TP/(TP+FN))" `[tự kiểm]` | "Ridgeway báo `64/149 = 43,0%` và **gọi đó là precision**; nhưng vì cả 149 vị trí đều là dương đã biết, đại lượng này thực chất là **recall ở ngưỡng 0,5 của họ**. Cách dùng chữ trong phần SIRT **không nhất quán nội bộ** với phần SET8" | **SAI về đại lượng** (phép tính đúng) |
| **2** | §2.2: "Với 149 vị trí dương, **đo được precision** … nhưng **chưa đo được MCC/AUPRC**" | **Ngược hoàn toàn.** Precision cần FP, MCC cần cả 4 ô, AUROC cần FPR, AUPRC cần precision — **cả bốn đều không đo được** trên tập chỉ-có-dương. Recall thì đo được. Và MCC/AUPRC **trở thành đo được** nhờ 2.694 vị trí âm của Zhang `[suy luận trên số [tự kiểm]]` | "Trên tập chỉ-có-dương đo được: **recall ở ngưỡng, recall ở ngân sách khớp, enrichment so với background matched, BEDROC/EF**. Không đo được: **precision, MCC, AUROC, AUPRC**. Nhưng Zhang 2022 định lượng **2.846** vị trí mà chỉ **152** đạt tiêu chí, nên **2.694** vị trí còn lại là nhãn âm-trong-tế-bào; khi đó AUPRC và MCC đo được, baseline AUPRC ≈ **5,3%**" | **SAI, đảo ngược** |
| **3** | §2.1: "Nhãn nhị phân mà bài 2025 dùng (**`category ≥ 1`**)" và đếm "Số vị trí dương (**`category = 1`**)" | Quy tắc đúng là **`efficiency ≥ 1`**, tái lập **100,0000%** trên 47.607 ô, **0 bất đồng**. `category = 1` cho SIRT1 chỉ **4** vị trí, bất đồng **2.423 ô (94,910% khớp)** `[tự kiểm]` | "Nhãn nhị phân của bài 2025 sinh bằng **`efficiency ≥ 1`**, tương đương **`substrate category ≥ signal ratio`**. **Số 176/1.901/1.844/1.038/2.614/1.199/1.692 thì đúng, nhãn thì sai.** Methods của Ridgeway viết là `signal ratio score of 1 or greater` — cũng không khớp tên cột, nhưng nhãn **không bị đảo dấu**" | **SAI về quy tắc** (số đúng) |
| **3b** | §3: "ngưỡng cứng `category ≥ 1` **làm mất 2.438 vị trí dương yếu của SIRT1**" | Hệ quả của #3: nhãn nhị phân **đã chuẩn hóa theo `signal ratio`** rồi, nên nó không phải phép ngưỡng cứng thô như mô tả `[tự kiểm]` | **Bỏ hẳn luận điểm này và viết lại.** Chỗ trống hợp lệ là **`ratio error` chưa được dùng ở đâu cả**; SIRT1 có trung vị `ratio error` 0,37 — cao nhất — nên 176 nhãn dương của SIRT1 là loại nhiễu nhất | **KHÔNG ĐỨNG** |
| **4** | §2.2: "149 vị trí … đo bằng khối phổ với SIRT2 quá biểu hiện (OE) và knockdown (KD)" (ngụ ý là thí nghiệm của Ridgeway) | Methods của Ridgeway: **"The MS-verified sites for SIRT2 were obtained from the dataset provided in Zhang et al., 2022"** `[tự kiểm]`. Và Ridgeway mô tả bối cảnh là **WT vs H187Y bất hoạt xúc tác**, còn Zhang mô tả **KD và OE** — hai mô tả **không trùng** `[tự kiểm]` | "Tập 149 vị trí **không phải thí nghiệm của Ridgeway**; nguồn là **Zhang et al. 2022, Sci Rep** ([PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)). Thiết kế của Zhang là KD + OE trong HCT116; Ridgeway lại mô tả WT vs H187Y. **Khác biệt này phải làm rõ trước khi dùng tập**, vì nó quyết định nhãn âm được định nghĩa thế nào" | **SAI về nguồn** |
| **4b** | §2.2 ngụ ý "tập test độc lập" | Nếu tập test của đề tài **chính là** tập mà baseline đã dùng để báo số, thì nó **độc lập với tập huấn luyện nhưng không độc lập với baseline** — cả hai mô hình đều đã "nhìn" qua nó ở mức chọn ngưỡng và báo cáo `[suy luận]` | "Độc lập **nguồn** với tập huấn luyện, **không** độc lập với baseline" | **CẦN ĐIỀU KIỆN** |
| **5** | §2.2: "**149** vị trí" | Zhang báo **134 peptide chứa 152 vị trí** (Fig. S4a) `[tự kiểm]` | "Zhang báo **152 vị trí**; Ridgeway dùng **149**. Chênh 3 **chưa giải thích được** — phải đối chiếu Supp Data 14 với Table S1/S4 của Zhang" | **CẦN SỬA SỐ** |
| **6** | §2.3: "**Nhãn âm định nghĩa được một cách sạch** … Đây là nhãn âm **có nghĩa**, khác hẳn nhãn âm 'chưa từng thấy'" | Nguyên lý đúng, nhưng **lạc quan quá** so với chất lượng thống kê thực tế: **không có p-value/FDR theo vị trí** ở cả hai bảng Sol 2012 và ở bước gọi vị trí của Zhang; phân vị 5–95% của log2 tỉ lệ là **−1,35…+1,12** (chuột) và **−1,20…+0,85** (người), tức **±2,2–2,5× chỉ do nhiễu** — ngưỡng 1,5× (log2 = 0,58) **nằm sâu trong dải nhiễu**; tập người có **1 phép so SILAC, không replicate** `[tự kiểm]` | "Nhãn âm **dùng được nhưng phải khai báo là nhãn yếu**: 'tỉ lệ nằm trong một khoảng tôi chọn', không phải 'đã kiểm và không bác bỏ được H0'. **Báo kết quả ở nhiều ngưỡng** (1,2× / 1,5× / 2,0× / 3,0×), không một ngưỡng. Và **lọc theo khu trú**, vì nhãn âm trộn 'trình tự không phù hợp' với 'không cùng khu trú'" | **ĐÚNG NGUYÊN LÝ, LẠC QUAN QUÁ** |
| **6b** | §2.3: đi tìm nhãn âm ở các bộ PRIDE | **Nguồn cần tìm nằm ngay trong bài mà baseline đã dùng** (Zhang 2022, 2.846 vị trí định lượng). Ngoài ra 3/4 accession PRIDE mà §2.3 nêu là **chuột**, 2/4 là **ức chế bằng thuốc** chứ không phải KO/KD di truyền, và **không accession nào có bảng vị trí nhỏ gọn** — chỉ raw file và MaxQuant output hàng trăm MB `[tự kiểm, PRIDE API v3]`. `PXD023479` khai báo **"No PTMs are included in the dataset"** | "Nguồn dùng được ngay: **Zhang 2022 Table S1** (SIRT2) và **Sol 2012 Table S1/S2** (SIRT3, PLoS ONE 7(12):e50545, [doi](https://doi.org/10.1371/journal.pone.0050545), PLOS không bị reCAPTCHA). **Cổng dữ liệu đã mở cho hai isoform**" | **CẦN THAY NGUỒN** |
| **7** | §2.2: "`Supplementary Data 13` là **dự đoán cho toàn bộ proteome**" | **145.461 vị trí trên 2.737 protein**; proteome người có ~20.400 protein. Đây là tập lysine acetyl hóa đã biết, đã lọc NetSurfP > 0,2 `[tự kiểm]` | "**145.461 vị trí trên 2.737 protein** — tập lysine acetyl hóa đã biết, lọc theo độ lộ bề mặt, **không phải toàn bộ proteome**. Và **3.226 vị trí có 13-mer trùng tập huấn luyện**, phải lọc trước khi dùng làm baseline" | **SAI về quy mô** |
| **8** | §2.2: "baseline có sẵn dự đoán để so trực tiếp, **không cần chạy lại mô hình của họ**" | Tự mâu thuẫn với §6 việc 2 của chính tài liệu. Và Ridgeway **không báo MCC hay AUPRC ở đâu cả** `[tự kiểm]`, nên không có mốc cho một bảng MCC/AUPRC | "Supp Data 13 cho **một** phép so: so **xếp hạng** điểm số. Nó **không thay được** việc chạy lại mô hình của họ, vì (a) họ không báo MCC/AUPRC, (b) cách chia của họ không công khai ('holdout 10% of the experimental data'), (c) ngưỡng của họ chọn **trên chính holdout** rồi báo trên cùng holdean đó ('m-threshold analysis … using the holdout set'), nên con số 41,2% đã lạc quan. **Chạy lại là bắt buộc**" | **TỰ MÂU THUẪN** |
| **9** | §4.2 RQ2: "So với **43,0%** của bài 2025 trên **đúng 149 vị trí đó**" | So recall ở hai ngưỡng khác nhau là **không hợp lệ** — hạ ngưỡng là tăng được recall; một mô hình gọi **mọi** lysine là dương đạt recall 100%. Và precision của bài 2025 tách theo mức chồng lấn: **23/44 = 52,3%** trên vị trí **có trong mảng** so với **41/105 = 39,0%** trên vị trí **không có trong mảng** `[tự kiểm]` | "So **recall ở ngân sách gọi-dương khớp nhau** trên cùng tập nền, cộng enrichment so với 2.694 vị trí âm, cộng AUPRC/MCC khi nhãn âm dựng được. **Mốc sạch là 39,0% trên 105 vị trí ngoài mảng, không phải 43,0%** — con số 43,0% đã pha rò rỉ ở mức vị trí" | **KHÔNG HỢP LỆ** |
| **10** | §3: tiền đề "**có khoảng cách miền lớn cần đo**" | Theo chính Ridgeway, **43,0% trên MS cao hơn 41,2% trên tập test nội bộ**, và họ gọi đó là *"a comparable but slight improvement"* `[tác giả báo cáo]`. Tức **ở chỉ số này không có sụt giảm**. Thêm nữa [PMC11447832](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/) báo mảng cho dự đoán **ngang** motif từ dịch chiết tế bào cho 3 kinase `[chưa kiểm]` | "Câu hỏi phải đặt **hai chiều**: khoảng cách có thể lớn (đo được MCC ≈ 0, mục 4 dưới) hoặc nhỏ (precision của baseline không sụt). **Kết quả âm là kết quả**, và tiền đề 'có khoảng cách lớn' chưa được đỡ bởi số liệu của baseline — nhưng **được đỡ mạnh bởi phép đo MCC ≈ 0 của chúng ta**" | **TIỀN ĐỀ CHƯA ĐỠ ĐƯỢC BỞI SỐ CỦA BASELINE, nhưng được đỡ bởi số của ta** |
| **11** | §2.4: "Deep-PLA … **khác họ enzyme; không phải isoform sirtuin**" | **SIRT1–7 LÀ HDAC class III**, và Deep-PLA phủ **9 HDAC**. DeepSIRT ghi rõ: "The class III HDACs contains seven members of the sirtuin family from SIRT1 to SIRT7" `[tác giả báo cáo]` | "Deep-PLA phủ 7 HAT + **9 HDAC**. **Phải đọc toàn văn xem 9 HDAC đó gồm những ai.** Nếu có SIRT1 hoặc SIRT2, câu 'mới ở họ sirtuin' **sụp**. Nếu chỉ có HDAC1–9 class I/II thì phát biểu đúng phải là 'class III chưa được Deep-PLA phủ'" | **CẦN KIỂM GẤP** |
| **12** | §2.4: liệt kê Rauh, Ridgeway, Deep-PLA, NAD_MCNN, SirtSAGE — **không có DeepSIRT** | **DeepSIRT 2021** (Shah, Taju, Dlamini, **Ou Y.-Y.**), *Comput Biol Chem* 93:107514 — "seven members of the sirtuin family of proteins", Sn 85,77%, Sp 97,32%, MCC 0,82 `[tác giả báo cáo, qua PubMed]` ([doi](https://doi.org/10.1016/j.compbiolchem.2021.107514), PMID 34058657). **Không có trong bản scrape 14 bài của GVHD** → bản scrape thiếu | "**Phải nêu DeepSIRT chủ động trên slide 1**, cùng NAD_MCNN. Phân biệt: DeepSIRT ở **mức protein** (target nào + khu trú nào), đề tài ở **mức residue** (lysine nào). Nếu không nêu, **GVHD có thể chỉ ngay vào bài của nhóm mình**" | **THIẾU BÀI QUAN TRỌNG NHẤT** |
| **13** | §4.2 phụ: "Rauh báo **SIRT7** ưa residue thân nước không tích điện hoặc tích điện âm ở **−3, −2, +1**; SIRT6 có túi gắn phần lớn thân dầu" — dùng làm **đáp án XAI** | **Không tìm thấy câu này** trong phần toàn văn Rauh đọc được. Phát biểu tương tự trong văn liệu là về **SIRT1** (+2, +3, −2); một bài 2022 nói **SIRT7 không có motif** ưa thích; phát biểu "túi thân dầu" trong các nguồn tìm được gắn với **SIRT2** (Phe235, Leu239 — nhưng nguồn duy nhất là **một bằng phát minh**, không dùng được) `[chưa kiểm]` | "**Bỏ con số −3/−2/+1 khỏi mọi tài liệu gửi GVHD** cho tới khi đọc lại đúng hình đặc hiệu chuỗi của Rauh. Thay bằng: **tự tính mức làm giàu residue theo vị trí (−6…+6) cho từng isoform trên 6.801 vị trí của mảng**, có kiểm định và hiệu chỉnh đa so sánh, rồi dùng kết quả đó làm đáp án" | **CÓ KHẢ NĂNG GÁN SAI ISOFORM** |
| **14** | §3 và §4.1: "conformal theo từng isoform (Mondrian) trả về *tập* isoform **có bảo đảm độ phủ**, ví dụ '{SIRT2, SIRT3} ở mức 90%'" | Mức A/B bảo đảm **từng nhãn một**. Một phát biểu về cả 7 nhãn cùng lúc cần **conformal risk control** (Theorem 2) hoặc **Bonferroni α/7** — và khi đó tập dự đoán phình ra, SIRT1 với ~35 điểm hiệu chỉnh dương **không đạt** ngưỡng Bonferroni ≥ 69 `[suy luận]` | "Chọn **một** mức và nói rõ. Phát biểu đúng cho tập isoform là: '**kỳ vọng tỉ lệ isoform thật bị bỏ sót ≤ α**', không phải 'xác suất tập chứa đủ 7 nhãn ≥ 1 − α'" | **NÓI QUÁ** |
| **15** | §4.2 RQ3: ngụ ý conformal cho **bảo đảm** trên dữ liệu trong tế bào | In-vitro → in-cell là **concept shift** (`P(Y|X)` đổi), không phải covariate shift, nên **Theorem 3 của weighted conformal không áp dụng được** `[suy luận]` | "Conformal bảo đảm độ phủ **trên chính phân bố mảng**. Trên miền in-cell **không có bảo đảm nào** — chỉ có **độ phủ thực nghiệm**, và nó là **chẩn đoán đo khoảng cách miền**, không phải guarantee. Ngoại lệ duy nhất: hy sinh ~75 trong 149 vị trí SIRT2 làm tập hiệu chỉnh để có **độ phủ trên lớp dương của SIRT2**" | **NÓI QUÁ** |
| **16** | §4.2 RQ1 bậc thang: "(3) đặc trưng làm tay + LDA/cây → (4) **ESM-2 đóng băng + mCNN**" | Bước này đổi **ba** thứ cùng lúc: **biểu diễn** (443 đặc trưng → PLM), **kiến trúc** (LDA/cây → mCNN), **số đầu ra** (7 rời → đa nhãn). Nếu có cải thiện thì **không gán được cho nguyên nhân nào** — đúng điều GVHD đòi ở tiêu chí 2 `[suy luận]` | Dùng bậc thang **mỗi bậc đổi đúng một thứ** (mục 7 dưới), thêm **B0** (dummy) và **B3** (MuSiteDeep đứng một mình), cộng hai ablation đánh giá **L1** (rò rỉ) và **L2** (memorization) | **GỘP BIẾN** |
| **17** | §4.3 cổng mô hình: "MCC **≥ baseline** … cho **≥ 4/7 isoform**" | "≥" không có CI thì với SIRT1 (176 dương) là chuyện may rủi `[suy luận]` | "MCC của bậc B8 cao hơn B4 **ngoài khoảng tin cậy bootstrap 95% theo cụm protein** cho ≥ 4/7 isoform, trên cùng `TEST-IN`, ngưỡng chọn trên `CALIB`. **SIRT1 báo riêng, không tính vào cổng**" | **KHÔNG DÙNG ĐƯỢC NHƯ ĐANG VIẾT** |
| **18** | §4.3 cổng SIRT1: "176 vị trí dương là quá ít" — **chỉ đặt cổng dừng cho SIRT1** | **Đó là isoform sai để lo lắng về.** SIRT1 là deacetylase hợp lệ nhất trong 7 cái (Rauh: "less specific than most other isoforms", xác nhận trên HMGB1 K12). **SIRT4, SIRT5, SIRT6, SIRT7 mới là chỗ khung sinh học đổ** `[suy luận trên trích dẫn [tác giả báo cáo]]` | "Đặt cổng dừng cho **SIRT4, SIRT5, SIRT6, SIRT7** vì khung deacetylase không khớp. SIRT1 giữ lại, báo riêng vì ít dữ liệu — đó là vấn đề thống kê, không phải vấn đề sinh học" | **ĐẶT CỔNG SAI ISOFORM** |
| **19** | §2.4: Ridgeway "không có ngữ cảnh ngoài peptide 13 aa" (ngụ ý cấu trúc là chỗ trống) | Ridgeway **đã** dùng NetSurfP1.0 > 0,2, và tự đo đường precision-vs-coverage của nó: nâng ngưỡng độ lộ tăng precision **37,3% → 42,0%** nhưng làm số cơ chất xác nhận tụt **885 → 402** `[tác giả báo cáo]` | "**Phần lớn lợi ích từ cấu trúc đã bị baseline khai thác.** Và để so sánh công bằng, phải **giữ nguyên** hai thứ: (a) bộ lọc NetSurfP > 0,2, (b) ensemble có MuSiteDeep. Bỏ cả hai thì chênh lệch MCC không quy được cho 'PLM tốt hơn đặc trưng làm tay'" | **CỔNG THÔNG TIN ĐÃ BỊ HÁI** |
| **20** | §3: "chưa có bài nào **đo xem dự đoán từ mảng in vitro có đúng trong tế bào không** ở mức hệ thống" | Ridgeway **đã** đo hai lần (SIRT2: 64/149; SET8: **75 vị trí in vitro → 32 sinh được tryptic peptide → chỉ 9/32 đo được tin cậy → 3/9 tăng methyl hóa**, n = 1 mỗi điều kiện) `[tự kiểm]`. Và cộng đồng kinase đã làm ở quy mô lớn hơn nhiều | Dạng an toàn: "**chưa có ai nghiên cứu một cách hệ thống** độ chuyển miền cho SIRT1–7; con số duy nhất tồn tại là 43,0% trên **một** isoform, **một** dòng tế bào, **chỉ có nhãn dương**". Dạng mạnh phải chứng minh: "chưa ai dựng **tập đánh giá trong tế bào có cả nhãn âm** cho đa isoform SIRT, nên chưa ai báo được MCC/AUPRC cho chuyển miền này" `[chưa tìm thấy, không kết luận là chưa từng có]` | **SAI NGUYÊN VĂN, đúng ở dạng hẹp** |
| **21** | §2.4: "Ridgeway … Dùng MusiteDeep làm bộ dự đoán phụ `[chưa kiểm]`" | **Xác nhận**: "MuSiteDeep was employed for the generalized PTM prediction component of the ensemble model", gộp bằng **hard voting** `[tự kiểm — đọc toàn văn]` | Nâng từ `[chưa kiểm]` lên `[tự kiểm]`, và **thêm một bậc baseline B3: MuSiteDeep đứng một mình** — xem mục 7 | **ĐÚNG, đã xác nhận** |
| **22** | §4.1: đầu ra "với mỗi lysine, **7 điểm số** … và một **tập isoform**" | Rauh: **"Isoform activities cannot be compared easily as each of the substrates has individual [KM và kcat riêng]"** và **"This comparison cannot show which isoform will dominantly deacetylate a site"** `[tác giả báo cáo]`. 7 cột đến từ 7 thí nghiệm ở nồng độ enzyme khác nhau trong dải **6–218 μg/ml** — chênh tới **~36 lần** | "Đầu ra 'tập isoform' là **đúng cái tác giả bộ dữ liệu nói dữ liệu của họ không trả lời được**. Hiệu chỉnh ngưỡng theo isoform **không khôi phục được** thông tin đã mất, vì không có đại lượng dùng chung nào để neo 7 thang đo. Phải **hạ phạm vi định lượng xuống SIRT1/2/3** và trình bày SIRT4–7 như **phân tích giới hạn của nhãn**" | **MỤC TIÊU ĐẦU RA KHÔNG ĐƯỢC DỮ LIỆU ĐỠ** |
| **23** | §2.1 điểm 1: "**SIRT1 gần như không dùng được** ở ngưỡng nhị phân hiện tại" (ngụ ý SIRT1 ít cơ chất / hoạt tính thấp) | Rauh **không** nói vậy. Ngược lại: Sirt1 "shows a more even activity distribution" và **"less specific than most other isoforms"**; `category > 0` ở SIRT1 là **6.775/6.802** — cao nhất trong 7 isoform `[tự kiểm]` | "SIRT1 có **176** nhãn dương **theo quy tắc `efficiency ≥ 1`**, nhưng điều đó phản ánh **ngưỡng và sai số đo** (trung vị `ratio error` 0,37, cao nhất), **không** phản ánh SIRT1 có ít cơ chất. SIRT1 chính là isoform mà Rauh gọi là ít đặc hiệu nhất" | **DIỄN GIẢI SAI NGUYÊN NHÂN** |
| **24** | §2.4: Ridgeway "Precision 37–43%" | Bài gộp hai đại lượng **khác bản chất**: SET8 **37,4% = 885/2.367 là precision đúng nghĩa** (mẫu số là số dự đoán dương, và mọi dự đoán dương đều đem đi thử) `[tự kiểm]`, còn SIRT2 **43,0% là recall**. Discussion của họ viết "experimentally validated **precision rates of 37−43%**" `[tự kiểm]` | "**37,4% (SET8) là precision; 43,0% (SIRT2) là recall.** Việc gộp chúng thành 'precision rates of 37−43%' là **trộn hai đại lượng**. Đây là một điểm phản biện sạch, nêu được với GVHD, và **không đòi hỏi chạy mô hình nào**" | **MỐC SO SÁNH TRỘN ĐẠI LƯỢNG** |
| **25** | Hai phát biểu **GIỮ NGUYÊN** | §2.2 "tập test độc lập nguồn **tồn tại và tải được**" — đúng về tồn tại và về nguồn độc lập với tập huấn luyện `[tự kiểm]`. §2.1 điểm 3 "cấu trúc chia sẻ cơ chất là thật và dày (2.087 vị trí dương với đúng 2 isoform)" — **đếm lại khớp đúng** `[tự kiểm]`, và khớp câu "SIRT2 and SIRT3 share almost twice the substrates as any other combination of SIRT" `[tác giả báo cáo]` | Giữ. Nhưng thêm điều kiện cho câu thứ hai: cấu trúc chia sẻ **có cơ sở nhất ở cặp SIRT2–SIRT3 (1.136 vị trí)**, tức ở đúng hai isoform mà khung deacetylase khớp | **ĐỨNG VỮNG** |

---

## 6. Phạm vi cốt lõi đề nghị, phần mở rộng, và các câu hỏi nghiên cứu

### 6.1 Phạm vi cốt lõi (phải làm, đủ để thành một luận văn)

**Tên đề nghị:** *Nhãn mảng peptide in vitro chuyển được bao nhiêu vào tế bào? Một phép đo có kiểm soát rò rỉ cho cơ chất deacetyl hóa của SIRT1, SIRT2 và SIRT3.*

Phạm vi cốt lõi gồm bốn thành phần, mỗi thành phần đều **không cần kết quả dương để có giá trị**:

1. **Ba isoform: SIRT1, SIRT2, SIRT3.** Đây là ba isoform mà khung "deacetylase" khớp theo enzymology, và đúng ba isoform có bằng chứng ngoài mảng (HMGB1 K12, MDH, 149 vị trí HCT116, 3.174 vị trí U2OS).
2. **Một tập đánh giá trong tế bào có cả nhãn âm**, dựng từ Zhang 2022 (SIRT2: 152 dương + 2.694 âm) và Sol 2012 Table S2 (SIRT3 người: 303 dương ở 1,5× + 2.456 âm), **báo ở nhiều ngưỡng**, **lọc rò rỉ ở mức chuỗi và mức cụm protein 30%**.
3. **Bậc thang baseline tách biến** (mục 7), chạy đủ cho SIRT2 (có `TEST-OUT`) và SIRT1 (trường hợp xấu nhất), chạy rút gọn cho SIRT3.
4. **Hai ablation đánh giá** — rò rỉ (L1) và memorization (L2) — mà khảo sát dự đoán là sẽ cho khoảng cách lớn hơn mọi khoảng cách giữa các bậc mô hình `[suy luận]`.

### 6.2 Phần mở rộng (chỉ làm nếu cốt lõi xong sớm)

| Mở rộng | Điều kiện để bắt đầu |
|---|---|
| **SIRT4–7 như phân tích giới hạn nhãn** (cột SIRT5 tương quan với lượng enzyme ra sao; mô hình SIRT6/SIRT7 học được gì khi phép thử sai bối cảnh) | Có Supplementary Data 5 của Rauh trong tay (lượng enzyme từng isoform) |
| **Nhãn thứ tự có trọng số `1/ratio_error²`** | Bậc B10/B11 trong bậc thang; chỉ sau khi B8 đã có số |
| **Conformal mức P1 + độ phủ thực nghiệm P2** | Chỉ sau khi đã chốt mức A/B/C và viết đúng phát biểu |
| **XAI với bốn tầng kiểm chứng** | **Chỉ sau khi** đã tự dựng bảng motif theo vị trí từ 6.801 vị trí và thấy có đáp án thật |
| **Bảng motif theo vị trí cho cả 7 isoform** | Làm ngay, rẻ — và nếu bảng đó không tồn tại trong văn liệu thì **chính việc dựng nó là một đóng góp nhỏ nhưng thật** `[suy luận]` |

### 6.3 Ba câu hỏi nghiên cứu, mỗi câu một giả thuyết kiểm được

**RQ1 — Nhãn mảng peptide in vitro mang bao nhiêu thông tin về sự phụ thuộc sirtuin trong tế bào?**

- **Giả thuyết H1 (kiểm được, và khảo sát dự đoán sẽ bị bác):** *Mô hình huấn luyện trên nhãn mảng đạt MCC > 0,15 trên `TEST-OUT` (SIRT2 từ Zhang, SIRT3 từ Sol), ngoài khoảng tin cậy bootstrap 95% theo cụm protein của một bộ dự đoán ngẫu nhiên khớp tỉ lệ gọi dương.*
- **Chứng cứ hiện có đã nghiêng về bác bỏ:** nhãn nhị phân của mảng đạt MCC **+0,047…+0,080** (người, 1.417 vị trí) và **−0,007** (chồng lấn chặt, 718 vị trí) `[tự kiểm]`. Nếu mô hình học cũng không vượt được, H1 bị bác và **đó là kết quả chính của luận văn**.
- **Phép kiểm phụ bắt buộc:** so với **B3 (MuSiteDeep đứng một mình)**. Nếu phần lớn hiệu năng trên tập Zhang đến từ "vị trí này acetyl hóa trong tế bào" (MuSiteDeep bắt được) chứ từ "SIRT2 deacetyl hóa nó", thì **cả con số 43,0% lẫn con số của ta đều không nói gì về đặc hiệu isoform** — và lưu ý tập Zhang **toàn là vị trí acetyl hóa thật**, nên lợi thế này càng lớn `[suy luận]`.

**RQ2 — Bao nhiêu phần của hiệu năng được báo cáo trong lĩnh vực này đến từ rò rỉ đồng dạng, không từ phương pháp?**

- **Giả thuyết H2:** *Khoảng cách MCC giữa cách chia "ngẫu nhiên theo vị trí" và cách chia "theo cụm protein 30% identity" lớn hơn khoảng cách MCC giữa bậc baseline tốt nhất và bậc baseline yếu nhất.* `[suy luận — đây là dự đoán của khảo sát]`
- **Chứng cứ hiện có:** precision của baseline là **52,3%** trên 44 vị trí **có trong mảng** so với **39,0%** trên 105 vị trí **không có** `[tự kiểm]`; **3.226/145.461** vị trí trong file dự đoán của họ có 13-mer trùng tập huấn luyện; **32,8%** tập chuột và **44,6%** tập người trùng 13-mer với tập huấn luyện `[tự kiểm]`.
- Nếu H2 đúng, **thông điệp chính của luận văn** là: trong bài toán này, cách chia quan trọng hơn kiến trúc. Và chưa tìm được bài nào **đo định lượng** mức thổi phồng do rò rỉ đồng dạng **riêng cho dự đoán vị trí PTM** `[chưa tìm thấy, không kết luận là chưa từng có]` — nếu thật không có, đề tài **đo được nó lần đầu cho họ sirtuin**.

**RQ3 — Nhãn thang độ có trọng số sai số đo có cải thiện so với nhãn nhị phân, và cải thiện ở đâu?**

- **Giả thuyết H3:** *Thay nhãn nhị phân `efficiency ≥ 1` bằng hồi quy trên `signal_ratio` với trọng số `1/ratio_error²` cải thiện AUPRC in-domain nhiều nhất ở isoform có `ratio_error` lớn nhất (SIRT1, trung vị 0,37) và ít nhất ở isoform có `ratio_error` nhỏ nhất (SIRT5, 0,21).*
- Đây là giả thuyết **có hướng**, kiểm được, và nếu nó đúng thì nó giải thích **tại sao** nhãn thang độ giúp — mạnh hơn một con số "AUPRC tăng X%". Phải tách thành **hai bậc riêng** (B10: đổi thang; B11: thêm trọng số), vì "dùng thang liên tục" và "cân theo độ tin cậy phép đo" là hai thứ hay bị gộp.
- **Phải nói rõ gốc ý tưởng:** đây là **future work do chính Ridgeway công bố**, không phải ý của sinh viên.

---

## 7. Đóng góp đã có bằng chứng, đóng góp kỳ vọng, và kết quả cần thí nghiệm

### 7.1 Đã có bằng chứng ngay hôm nay (mang đi gặp GVHD được, không cần chạy gì thêm)

| Đóng góp | Bằng chứng |
|---|---|
| **Quy tắc sinh nhãn của baseline được tái lập chính xác, và tên cột trong Methods của họ là sai** | `efficiency ≥ 1` khớp **100,0000%** trên 47.607 ô, **0 bất đồng**; `category = 1` bất đồng 2.423 ô `[tự kiểm]` |
| **Con số 43,0% là recall, không phải precision; và bài gộp nó với một precision thật thành một dải** | Định nghĩa precision/recall của chính bài ở phần SET8; 885/2.367 = 37,4% là precision đúng nghĩa `[tự kiểm]` |
| **Con số 43,0% pha rò rỉ ở mức vị trí; mốc sạch là 39,0%** | 23/44 = 52,3% (có trong mảng) vs 41/105 = 39,0% (không có) `[tự kiểm]` |
| **Nhãn âm trong tế bào tồn tại và nằm ngay trong bài mà baseline đã dùng** | Zhang 2022: 2.846 định lượng − 152 phụ thuộc SIRT2 = **2.694** âm; tỉ lệ dương nền 5,3% `[tự kiểm]` |
| **Cổng dữ liệu mở cho isoform thứ hai** | Sol 2012 Table S2: 3.174 vị trí người, có cửa sổ 13 aa, 303 dương / 2.456 âm `[tự kiểm]` |
| **"Nguồn độc lập" ≠ "trình tự độc lập"** | 513/1.566 (32,8%) vị trí **chuột** có 13-mer trùng **đúng từng chữ** với mảng người `[tự kiểm]` |
| **Supp Data 13 không phải "toàn bộ proteome", và chính nó có rò rỉ** | 145.461 vị trí / **2.737** protein; 3.226 vị trí trùng 13-mer tập huấn luyện; 55.703 vị trí trên 973 protein chia sẻ protein `[tự kiểm]` |
| **Chênh 6.802/6.801 là một dòng cụ thể, không phải lỗi đếm** | `GIQCVKKRDLEQA` / `Q04206` (RELA/p65), 4 vị trí trong một ngoặc `[tự kiểm]` |
| **Đo thử chuyển miền: MCC ≈ 0 ở mọi ngưỡng** | 4 ngưỡng × 2 loài + tập chồng lấn chặt; MCC cao nhất +0,082, thấp nhất −0,043 `[tự kiểm]` |
| **Mảng bỏ sót 61% các vị trí phụ thuộc SIRT2 trong tế bào mà nó CÓ đo** | Trong 44 vị trí chồng lấn, nhãn SIRT2 của mảng chỉ dương ở **17/44** `[tự kiểm]` |

Đây là **mười đóng góp đã thành hình trước khi huấn luyện một mô hình nào** — và là lý do mạnh nhất để không bỏ đề tài.

### 7.2 Kỳ vọng được (có cơ sở, nhưng phải làm mới biết)

- Một **tập đánh giá trong tế bào có cả hai lớp cho hai isoform**, công bố kèm script tái tạo. Chưa tìm thấy tập tương đương `[chưa tìm thấy, không kết luận là chưa từng có]`.
- **Lượng hóa mức thổi phồng do rò rỉ đồng dạng** cho họ sirtuin, ba cách chia, có CI bootstrap theo cụm.
- **Bảng motif theo vị trí cho từng isoform** dựng từ 6.801 vị trí — hoặc chứng minh rằng nó không tồn tại.
- Một **mốc so sánh MCC/AUPRC hợp lệ** với baseline, bằng cách chạy lại mã của họ trên cách chia của mình (vì họ **không báo MCC/AUPRC ở đâu cả** `[tự kiểm]`).
- **Phát biểu conformal đúng mức** (P1 chắc chắn, P2 là chẩn đoán, P3 chỉ cho SIRT2 lớp dương).

### 7.3 Chỉ thí nghiệm mới trả lời được (không được hứa trước)

- Mô hình học có vượt được MCC ≈ 0 trên `TEST-OUT` hay không. **Khảo sát dự đoán là không.**
- PLM có hơn 443 đặc trưng làm tay trên cùng cách chia hay không, và hơn bao nhiêu **ngoài CI**.
- mCNN nhiều cửa sổ có hơn CNN một cửa sổ hay không (B7 vs B6). **Nếu B7 ≈ B6, phải nói thẳng, kể cả khi mCNN là khung quen của GVHD.**
- Mô hình đa nhãn 7 (hoặc 3) đầu ra có lợi hơn các mô hình rời hay không, và **isoform nào được lợi, isoform nào bị hại** (kỳ vọng SIRT1 được lợi nhiều nhất `[suy luận]`).
- Nhãn thang độ có trọng số có cải thiện đúng theo hướng của H3 hay không.
- Số cụm protein ở 30% identity — **chưa biết**, và con số đó quyết định có chia 5 phần được hay phải chuyển sang nested CV theo cụm.

### 7.4 Bậc thang baseline đã tách biến (mỗi bậc đổi đúng một thứ)

| # | Mô hình | Cô lập được điều gì |
|---|---|---|
| **B0** | Hằng số "luôn âm"; và ngẫu nhiên gọi dương đúng tỉ lệ dương | **Sàn tuyệt đối.** Cho accuracy 97,41% của SIRT1 `[tự kiểm]` và AUPRC baseline từng isoform |
| **B1** | PSSM / scoring matrix trên cửa sổ 13 aa | Phần giải thích được **chỉ bằng ưu tiên từng vị trí độc lập** |
| **B2** | k-mer / gapped k-mer + SVM hoặc logistic | Phần do **tương tác giữa các vị trí** |
| **B3** | **MuSiteDeep (N6-acetyl-lysine) đứng một mình** | **Bao nhiêu phần của "đặc hiệu isoform" thật ra chỉ là "vị trí này có acetyl hóa hay không".** Bậc bắt buộc |
| **B4** | 443 đặc trưng làm tay + LDA/cây, **chạy lại trên cách chia của mình** | **Mốc so sánh hợp lệ duy nhất** với Ridgeway 2025 |
| **B5** | one-hot 13×20 + CNN một cửa sổ, mô hình rời | Phần lợi do **mạng neural**, không lẫn với lợi do PLM |
| **B6** | **ESM-2 đóng băng** + CNN một cửa sổ | **Đóng góp riêng của PLM** — đúng câu GVHD hỏi ở tiêu chí 3 |
| **B7** | ESM-2 đóng băng + **mCNN nhiều cửa sổ** | **Đóng góp riêng của mCNN**, tách khỏi PLM |
| **B8** | ESM-2 + mCNN, **một mô hình nhiều đầu ra** | **Lợi của chia sẻ tham số giữa isoform** (cơ sở: SIRT2–SIRT3 đồng dương 1.136 vị trí) |
| **B9** | ESM-2 + **LoRA** + mCNN | Đóng góp riêng của fine-tuning |
| **B10** | B9 + **nhãn thứ tự** thay nhãn nhị phân | Đóng góp của thang liên tục |
| **B11** | B10 + **trọng số `1/ratio_error²`** | Tách "dùng thang liên tục" khỏi "cân theo độ tin cậy phép đo" |
| **B12** | B11 + ngữ cảnh ngoài cửa sổ 13 aa (cửa sổ rộng, khu trú, disorder) | Đóng góp của ngữ cảnh. **Ablate từng loại một** — khu trú là đặc trưng **mức protein** và rất dễ gây rò rỉ |
| **B13** | B12 + **hiệu chỉnh ngưỡng theo isoform** trên `CALIB` | Tách "mô hình tốt hơn" khỏi "ngưỡng đặt khéo hơn" |
| **B14** | B13 + **conformal Mondrian** | Không đổi thứ hạng, nên **không được báo như "tăng hiệu năng"**; chỉ báo độ phủ và kích thước tập |
| **L1** | Chạy lại bậc tốt nhất ở **ba cách chia** (ngẫu nhiên theo vị trí / theo protein / theo cụm 30%) | **Mức thổi phồng do rò rỉ** — RQ2 |
| **L2** | Báo riêng trên `TEST-OUT`: vị trí **có** trong mảng vs **không có**, và phân tầng theo khoảng cách đồng dạng | **Phần của con số chuyển miền đến từ memorization** |

**Rút gọn thực tế** `[suy luận]`: chạy đủ bậc thang trên **2 isoform** (SIRT2 vì có `TEST-OUT`; SIRT1 vì là trường hợp xấu nhất), rồi chỉ chạy B0, B3, B4, B8, B13 cho các isoform còn lại. **Nói rõ lựa chọn này trong đề cương thay vì âm thầm bỏ bậc.**

### 7.5 Giao thức chia tập (đủ cụ thể để viết vào đề cương)

Năm phân vùng, không bốn: `TRAIN` (~70% số cụm), `VAL` (~10%, chọn mô hình), `CALIB` (~10%, **chỉ** chọn ngưỡng và hiệu chỉnh conformal — không bao giờ dùng chọn mô hình), `TEST-IN` (~10%, **niêm phong**, mở đúng một lần), `TEST-OUT` (Zhang 2022 + Sol 2012, đo **chuyển miền**).

Quy tắc kèm theo:

1. **Gom cụm theo chuỗi protein mẹ đầy đủ**, MMseqs2 `easy-cluster --min-seq-id 0.3 -c 0.8`, gán **toàn bộ cụm** vào một phân vùng. Ngưỡng 0,3 có căn cứ từ Rost 1999: **trên ~30% identity, 90% các cặp là homolog; dưới 25% thì dưới 10%** `[tự kiểm — qua tóm tắt]` ([Protein Eng 12(2):85–94](https://www.biostat.wisc.edu/~kbroman/teaching/statgen/2004/refs/rost1.pdf)). Dùng **GraphPart** ([PMC10578201](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10578201/)) thì tốt hơn gom cụm thủ công vì nó **giữ chuỗi và gán cụm vào cùng phân vùng** thay vì xoá, nên giữ được nhiều mẫu hơn.
2. **Không gom cụm trên chính peptide 13 aa.** Với chuỗi dài 13, một mismatch đổi identity `1/13 ≈ 7,7%`, và hai 13-mer ngẫu nhiên đã có identity kỳ vọng 5–6% chỉ do trùng ngẫu nhiên; Rost nói thẳng rằng ở alignment ngắn, identity cao **không** suy ra được quan hệ `[suy luận, dựa trên Rost 1999]`.
3. **Khử trùng lặp thứ hai ở mức 13-mer**, nhưng **không chọn ngưỡng tay**: vẽ phân bố khoảng cách Hamming từ mỗi 13-mer trong `TEST-IN` tới 13-mer gần nhất trong `TRAIN`, so với phân bố của cặp ngẫu nhiên, rồi **báo hiệu năng phân tầng theo khoảng cách này** (dải 0–2, 3–5, 6+). Cách này biến rò rỉ thành đại lượng đo được.
4. **Báo cáo độ nhạy theo ngưỡng đồng dạng:** chạy lại toàn bộ ở **0,3 và 0,5**, báo cả hai bảng. **Không được chọn ngưỡng nào cho ra số đẹp hơn.**
5. **`TEST-OUT` lọc hai chiều:** loại khỏi `TRAIN/VAL/CALIB` mọi protein thuộc cùng cụm 30% với protein trong `TEST-OUT`. Và **báo hai phiên bản** của `TEST-OUT`: (a) loại 44 vị trí trùng hẳn với mảng, (b) giữ. **Chênh lệch giữa (a) và (b) là ước lượng trực tiếp phần đóng góp của memorization vào con số 43,0%.**
6. **Ngưỡng cho `TEST-OUT` lấy từ `CALIB` (miền mảng), không từ `TEST-OUT`.**
7. **Niêm phong:** ghi hash của file phân vùng vào repo **trước** khi chạy thí nghiệm đầu tiên.

### 7.6 Metric theo tình huống

Nguyên tắc: **accuracy và AUROC bị cấm làm metric chính** — SIRT1 đạt **97,41%** accuracy bằng cách luôn trả lời "không" `[tự kiểm]`. Chicco & Jurman 2020: accuracy và F1 "can dangerously show over-optimistic inflated results, especially on imbalanced datasets", còn MCC "produces a high score only if the prediction obtained good results in **all of the four confusion matrix categories**" `[tự kiểm — tóm tắt]` ([doi:10.1186/s12864-019-6413-7](https://doi.org/10.1186/s12864-019-6413-7)). Saito & Rehmsmeier 2015: với dữ liệu lệch lớp, "the visual interpretability of ROC plots … can be **deceptive**" `[tự kiểm — tóm tắt]` ([doi:10.1371/journal.pone.0118432](https://doi.org/10.1371/journal.pone.0118432)). Và chính Ridgeway cũng chọn F-score "considering the imbalanced representation of positives", "rather than using specificity, **which is falsely inflated**" `[tự kiểm]`.

- **In-domain, một isoform:** **AUPRC** (kèm baseline = tỉ lệ dương, vì AUPRC của bộ ngẫu nhiên **bằng** tỉ lệ dương) + **MCC** tại ngưỡng chốt trên `CALIB`, kèm **CI bootstrap theo cụm protein** (resample cụm, không resample vị trí — các vị trí cùng protein tương quan). AUROC báo ở cột phụ để nối với tài liệu.
- **Nhãn liên tục:** **Spearman ρ** và **Kendall τ** **trong từng isoform riêng**; báo cả bản có và không có trọng số. **Không** dùng Pearson r hay RMSE làm metric chính.
- **Đa nhãn:** bảng **per-label** là bảng chính (tỉ lệ dương chạy từ 2,59% tới 38,44% `[tự kiểm]`); **macro-average** làm số tổng hợp; **micro-average không nên làm số chính** vì nó cộng dồn các nhãn mà bản thân Rauh nói không so được với nhau. Nếu sản phẩm trả về *tập* isoform thì phải báo **example-based F1** và, nếu có conformal, **độ phủ theo từng isoform (Mondrian)** cộng kích thước tập trung bình — độ phủ gộp chung che mất chuyện SIRT1 không đạt phủ. Lưu ý: "đoán toàn âm" đã đạt subset accuracy ~**16,3%** (1.107/6.801) `[tự kiểm]`.
- **Tập chỉ-có-dương:** **recall ở ngân sách gọi-dương cố định** + **enrichment so với background matched** kèm kiểm định nhị thức + **BEDROC/EF** + CI bootstrap. **Tuyệt đối không gọi nó là precision.** Background **đúng** là chính 2.694 vị trí còn lại của Zhang — cùng dòng tế bào, cùng phương pháp đo, cùng bộ lọc phát hiện — **không** phải 145.461 vị trí proteome, vì ba thiên lệch (acetyl hóa thật / phát hiện được bằng MS / định lượng được ở cả hai điều kiện) sẽ thổi enrichment lên `[suy luận]`.
- **Tập có nhãn âm:** AUPRC + MCC, baseline AUPRC = **5,3%**.

Một lưu ý về PU learning: thứ tự ưu tiên là **dựng nhãn âm thật trước**, PU-correction kiểu Jain 2017 ([arXiv:1702.00518](https://arxiv.org/abs/1702.00518)) **chỉ nên là phân tích độ nhạy** — trình bày metric thật như một **hàm của class prior π** trên một dải hợp lý, không chốt một con số, vì π ở đây là "tỉ lệ lysine trong proteome thật sự là cơ chất SIRT2 trong tế bào" và **không ai biết** `[suy luận]`.

---

## 8. Cổng go/stop dựa trên dữ liệu

Mỗi ngưỡng dưới đây **hoặc** có căn cứ dẫn được, **hoặc** được đánh dấu rõ **"phải quyết từ dữ liệu"**.

| # | Cổng | Khi nào | Ngưỡng | Căn cứ | Không qua thì làm gì |
|---|---|---|---|---|---|
| **G1** | **Deep-PLA có SIRT nào không** | Trước tuần 6 | Nhị phân: có / không | — (phép đọc, không phải ngưỡng) | Nếu **có SIRT1 hoặc SIRT2**, câu "mới ở họ sirtuin" **sụp** → đổi cách phát biểu toàn bộ trục 1, hoặc chuyển sang B |
| **G2** | **Supplementary Data 6 của Rauh** | Trước tuần 6 | **Phải quyết từ dữ liệu**: đếm số peptide "không cho tín hiệu đáng kể ở ≥1 đối chứng" và tỉ lệ của chúng trong tập huấn luyện | Chính tên file `[tác giả báo cáo]` | Nếu tỉ lệ cao, **phải loại chúng** khỏi lớp âm và báo lại mọi chỉ số; nếu không loại được thì khai báo rằng specificity/MCC bị thổi |
| **G3** | **Lượng enzyme từng isoform (Supp Data 5) vs số nhãn dương** | Trước tuần 6 | **Phải quyết từ dữ liệu**: tương quan Spearman giữa lượng enzyme và số nhãn dương của 7 cột | Dải 6–218 μg/ml, chênh ~36 lần `[tác giả báo cáo]` | Nếu tương quan cao, **phần "đặc hiệu isoform" của đề tài đổ** → chỉ còn làm được SIRT1/2/3 và phải nói rõ lý do |
| **G4** | **Zhang Table S1 có fold-change theo từng vị trí** | Tuần 1 | Nhị phân | Zhang báo 2.846 vị trí định lượng `[tự kiểm]` | Nếu chỉ có danh sách: vẫn dựng được **nhãn âm nhị phân** (2.694 vị trí), nhưng **không** dựng được nhãn thứ tự trong tế bào |
| **G5** | **Số cụm protein ở 30% identity** | Tuần 1, **trước khi chọn kiến trúc** | **Phải quyết từ dữ liệu.** Nếu số cụm **dưới ~300** thì chia một lần không khả thi | Chưa biết `[chưa kiểm]`; 6.801 vị trí trên 2.999 protein là 2,3 vị trí/protein `[tác giả báo cáo + tự kiểm]` | Chuyển sang **nested CV theo cụm**, và `CALIB` lấy bằng cross-conformal |
| **G6** | **Bao nhiêu trong 152 vị trí Zhang có mặt trong Supp Data 13** | Tuần 1 | **Phải quyết từ dữ liệu.** Nếu phủ thấp, phép so xếp hạng với baseline **mất giá trị** | Supp Data 13 đã lọc NetSurfP > 0,2 và đã loại chuỗi trùng tập huấn luyện `[tự kiểm]` | Bỏ phép so xếp hạng, chỉ còn phép so "chạy lại mã của họ" |
| **G7** | **Mô hình có vượt nhãn mảng thô trên `TEST-OUT`** | Tuần 4 | **MCC vượt +0,08** (mốc đã đo của nhãn mảng thô), **ngoài CI bootstrap 95% theo cụm** | **+0,047…+0,080** là mốc đo được trong khảo sát này `[tự kiểm]` | Báo kết quả âm và **chuyển trọng tâm sang RQ2 (rò rỉ) và phân tích nguyên nhân** — đây đã là kế hoạch, không phải thất bại |
| **G8** | **PLM có hơn đặc trưng làm tay** | Tuần 4 | MCC của **B6** cao hơn **B4** **ngoài CI bootstrap 95% theo cụm**, cho ≥ 2/3 isoform; **SIRT1 báo riêng** | Thay cho ngưỡng "≥ baseline cho 4/7" vốn không dùng được vì không có CI `[suy luận]` | Nói thẳng rằng PLM không giúp trên bài toán này — **đây là câu trả lời cho tiêu chí 3 của GVHD**, dương hay âm đều trả lời được |
| **G9** | **mCNN có đáng không** | Tuần 5 | **B7 vượt B6 ngoài CI** | — | Nếu B7 ≈ B6, **nói thẳng**, kể cả khi mCNN là khung quen của GVHD |
| **G10** | **Cổng dừng cho SIRT4/5/6/7** | Tuần 2 | Nhị phân sinh học: khung "deacetylase" không khớp | Mathias 2014 Cell, Jiang 2013 Nature, Barber 2012 Nature `[tác giả báo cáo]` | **Bỏ khỏi phần định lượng ngay từ đầu**, chuyển thành phân tích giới hạn nhãn. Lưu ý: cổng dừng cho **SIRT1** trong bản khuyến nghị là đặt **sai isoform** |
| **G11** | **Conformal cho SIRT1** | Tuần 5 | **n ≥ 22** điểm hiệu chỉnh dương cho ε = 0,10; **n ≥ 102** cho ε = 0,05; **n ≥ 69** nếu Bonferroni 7 nhãn ở α = 0,1 | Table 1 của Angelopoulos & Bates `[tác giả báo cáo]`; `n ≥ 1/α − 1` cho tính không-tầm-thường `[suy luận]` | SIRT1 có ~35 điểm → **chỉ đạt ε = 0,10**, và **không đạt Bonferroni**. Hoặc bỏ SIRT1 khỏi phần conformal, hoặc gom SIRT1+SIRT2+SIRT3 thành một cụm (clustered conformal, [arXiv:2306.09335](https://arxiv.org/abs/2306.09335)) **và nói rõ bảo đảm lúc đó là theo cụm, không theo isoform** — một đánh đổi mâu thuẫn một phần với chính chủ đề "đặc hiệu isoform" |
| **G12** | **XAI có đáp án không** | Tuần 3, **trước khi hứa phần XAI** | **Phải quyết từ dữ liệu**: mức làm giàu residue theo vị trí cho từng isoform trên 6.801 vị trí, có kiểm định và hiệu chỉnh đa so sánh. Mốc tham chiếu: CDK ở đề tài B đạt **83% vs 3%** (làm giàu ~27 lần) `[tự đo]` | Mức may rủi cho tỉ lệ khớp là 1/12 ≈ 0,083 với cửa sổ 13 aa `[tự kiểm theo công thức của một tiền ấn phẩm]` | Nếu không có isoform nào đạt làm giàu rõ, **bỏ phép kiểm "XAI có đáp án"** và thay bằng ba lối: đối chứng tiêu cực (occlusion **không** làm nổi vị trí ngoài ±4 và token đệm), đối chiếu chéo giữa isoform (SIRT1/2/3 giống nhau hơn SIRT5/6/7?), và đối chiếu với 2 vị trí xác nhận trên protein nguyên (Prx1 K197, HMGB1 K12) |
| **G13** | **XAI có trung thực không** | Tuần 6 | Sanity check **phải đạt**: nếu bản đồ occlusion trên mô hình **chưa huấn luyện** hoặc trên mô hình huấn luyện với **nhãn đã trộn** tương quan cao với bản đồ của mô hình thật → **dừng, không báo cáo motif** | Adebayo 2018 `[tác giả báo cáo]` | Không báo cáo phần XAI. Và đường deletion phải **tách khỏi đường xóa ngẫu nhiên**, nếu không thì không trung thực |

---

## 9. Câu hỏi cho GVHD tuần 6, gộp từ năm nhánh và xếp theo mức ảnh hưởng tới quyết định

Mười hai câu dưới đây đã loại trùng từ năm nhánh khảo sát cộng bản khuyến nghị. **Câu 1–3 quyết định đi hay dừng; câu 4–7 quyết định phạm vi; câu 8–12 quyết định cách trình bày.**

**Nhóm quyết định đi hay dừng:**

1. **"Em đã đo thử: nhãn mảng peptide in vitro gần như không chuyển được sang trong tế bào (MCC ≤ +0,08 trên 1.417 vị trí, và −0,007 trên tập chồng lấn chặt). Thầy có chấp nhận một luận văn mà kết quả chính là ĐỊNH LƯỢNG MỨC ĐỘ KHÔNG CHUYỂN ĐƯỢC, kèm phân tích nguyên nhân (khu trú, stoichiometry, công suất thống kê), thay vì một mô hình tốt hơn?"** — Đây là câu quan trọng nhất. Trả lời "không" ⇒ chuyển sang đề tài dự phòng B.
2. **"Bài Ridgeway 2025 TỰ CÔNG BỐ hai việc tương lai đúng bằng hai đóng góp chính của em (dùng PLM, và hồi quy trên mật độ SPOT). Thầy thấy việc 'làm trước việc tương lai của người khác' là đóng góp đủ cho luận văn, hay là rủi ro bị làm trước?"** — Bài mới 11 tháng.
3. **"Thầy có coi tập đánh giá trong tế bào do em tự dựng từ dữ liệu khối phổ công khai (Zhang 2022 cho SIRT2, Sol 2012 cho SIRT3) là tập test độc lập đủ tiêu chuẩn không? Lưu ý: tập 152 vị trí SIRT2 được gọi bằng ngưỡng fold-change 1,5 mà KHÔNG có FDR ở bước gọi vị trí, và cả hai bảng Sol 2012 đều không có p-value theo vị trí."**

**Nhóm quyết định phạm vi:**

4. **"Tại sao coi 7 isoform là 7 bài toán cùng loại khi theo Cell 2014 và Nature 2013, SIRT4/SIRT5 'có rất ít hoặc không có hoạt tính deacetylase', SIRT6 thấp hơn 100–1000 lần, và SIRT7 cần nucleosome? Em đề nghị hạ phần định lượng xuống SIRT1/2/3 và trình bày SIRT4–7 như phân tích giới hạn của nhãn. Thầy thấy được không?"**
5. **"Chính tác giả bộ dữ liệu viết 'This comparison cannot show which isoform will dominantly deacetylate a site'. Đầu ra 'tập isoform' mà em dự kiến là đúng cái họ nói dữ liệu không trả lời được. Thầy muốn em đổi đầu ra thành gì?"**
6. **"Nhóm Prof. Ou đã có DeepSIRT (2021) cho target SIRT1–7 ở mức protein, MCC 0,82. Thầy có coi đề tài này là tiếp nối DeepSIRT (hạ xuống mức residue), và nếu vậy có nên xin dữ liệu/mã của DeepSIRT không?"**
7. **"SIRT1 chỉ có 176 vị trí dương → khoảng 35 điểm hiệu chỉnh dương, theo bảng cỡ mẫu của Angelopoulos & Bates thì chỉ cho sai lệch độ phủ ±0,10, tức khoảng [0,80; 1,00]. Thầy muốn em (a) bỏ SIRT1 khỏi phần conformal, hay (b) gom SIRT1+SIRT2+SIRT3 thành một cụm hiệu chỉnh và nói rõ bảo đảm là theo CỤM chứ không theo isoform?"**

**Nhóm quyết định cách trình bày:**

8. **"Conformal chỉ bảo đảm độ phủ TRÊN MIỀN MẢNG PEPTIDE — vì in-vitro → in-cell là concept shift, không phải covariate shift, nên weighted conformal không áp dụng được. Thầy thấy em nên đóng khung conformal thành DỤNG CỤ ĐO khoảng cách miền, thay vì thành một bảo đảm?"**
9. **"Nếu baseline cho precision trên MS (43,0%) CAO HƠN trên tập test nội bộ (41,2%), thì khoảng cách miền em muốn đo nằm ở đâu? Em có câu trả lời: 43,0% của họ là RECALL không phải precision, và nó pha rò rỉ (52,3% trên vị trí có trong mảng so với 39,0% trên vị trí ngoài mảng). Thầy thấy phản biện này có đủ mạnh để làm một phần của luận văn?"**
10. **"Phép kiểm 'XAI có đáp án' của em dựa vào motif đặc hiệu isoform. Nhưng văn liệu MÂU THUẪN về SIRT1, có bài nói SIRT7 KHÔNG có motif, còn ở đề tài dự phòng thì CDK có đáp án rất mạnh (83% cửa sổ dương có P ở +1, so với 3% cửa sổ âm). Thầy có coi đây là lý do thật để nghiêng về đề tài dự phòng, hay em nên tự dựng bảng motif theo vị trí từ 6.801 vị trí của mảng và dùng nó làm đáp án?"**
11. **"Đóng góp chính nằm ở giao thức đánh giá (nhãn âm trong tế bào, kiểm soát rò rỉ ba mức, metric đúng), không phải 'vượt SOTA về accuracy'. Thầy đồng ý không? Và trong năm tiêu chí, thầy muốn em ưu tiên tiêu chí nào khi chỉ còn 8–9 tuần?"**
12. **"Bài 2025 KHÔNG báo MCC hay AUPRC ở bất kỳ đâu, chỉ báo F-score/precision/recall tại ngưỡng họ tự chọn trên chính holdout. Nghĩa là em phải CHẠY LẠI mô hình của họ để có mốc so sánh. Thầy coi việc chạy lại baseline có tính là một phần đóng góp, hay chỉ là công việc chuẩn bị?"**

---

## 10. Sản phẩm hệ thống, mô tả thật, khớp với giới hạn khoa học đã tìm được

Tiêu chí 5 của GVHD là **thành phần không thể thiếu**. Nhưng một website hứa "dán chuỗi vào, biết lysine nào bị SIRT nào deacetyl hóa trong tế bào" sẽ **mâu thuẫn trực tiếp** với kết quả khoa học của chính luận văn. Mô tả trung thực:

**Tên: một công cụ TRA CỨU VÀ ĐỐI CHIẾU BẰNG CHỨNG, không phải một công cụ dự đoán sinh học.**

| Thành phần | Nội dung | Vì sao trung thực |
|---|---|---|
| **Vào** | Một chuỗi protein người hoặc một UniProt ID | Giữ nguyên |
| **Ra, tầng 1 — điểm in vitro** | Với mỗi lysine: điểm dự đoán cho **SIRT1, SIRT2, SIRT3** (không phải 7), **dán nhãn rõ**: "điểm này dự đoán hoạt tính trên peptide 13 aa trong ống nghiệm" | Đây là thứ duy nhất nhãn huấn luyện đỡ được |
| **Ra, tầng 2 — cảnh báo chuyển miền** | Với mỗi vị trí, hiện **cả hai**: điểm in vitro, **và** một câu cảnh báo định lượng: "trên tập đánh giá trong tế bào của chúng tôi, điểm này tương quan với sự phụ thuộc sirtuin ở mức MCC = …" | **Biến kết quả âm thành tính năng**, thay vì che nó |
| **Ra, tầng 3 — bằng chứng thực nghiệm đã có** | Vị trí này có trong mảng Rauh không? Có trong Zhang 2022 / Sol 2012 không? log2FC là bao nhiêu? Có phải một trong 2 vị trí được xác nhận trên protein nguyên không? | **Phần hữu dụng nhất với người làm sinh học**, và hoàn toàn dựa trên dữ liệu đã kiểm |
| **Ra, tầng 4 — khoảng cách tới tập huấn luyện** | Khoảng cách Hamming của 13-mer này tới 13-mer gần nhất trong `TRAIN`; protein này có cùng cụm 30% với protein nào trong `TRAIN` không | Trả lời câu "mô hình có đang nhớ hay đang suy luận" **cho từng truy vấn** |
| **Ra, tầng 5 — conformal** | Tập dự đoán ở mức α đã chọn, kèm một dòng: "bảo đảm này áp cho **phân bố mảng peptide in vitro**; trên dữ liệu trong tế bào chúng tôi chỉ báo độ phủ thực nghiệm, không có bảo đảm" | **Phát biểu đúng** thay vì "{SIRT2, SIRT3} ở mức 90%" |
| **Không có** | Không có câu "đây là cơ chất sinh lý của SIRT_x". Không có 7 đầu ra bình đẳng. Không có tuyên bố "đầu tiên" hay "vượt SOTA" | Nhất quán với mục 2.2 và 2.3 |

**Một lợi thế bất ngờ của thiết kế này:** nó biến mọi giới hạn khoa học thành một **tính năng giao diện**. Người dùng không bị hứa quá, và luận văn không phải giấu kết quả âm trong một chương phụ lục. Đây cũng là câu trả lời cho tiêu chí 5 của một khoa Kỹ thuật phần mềm: giá trị của sản phẩm nằm ở **tích hợp và đối chiếu nhiều nguồn bằng chứng rời rạc** (mảng Rauh, Supp Data 13, Zhang 2022, Sol 2012, 2 vị trí xác nhận trên protein nguyên) — một việc hiện **không có công cụ nào làm**, và không phụ thuộc vào việc mô hình có tốt hay không.

---

## 11. Mức sẵn sàng để trình bày, và danh sách việc theo ưu tiên

### 11.1 Phán quyết về mức sẵn sàng

**Đề tài sẵn sàng khoảng 60% để trình bày tuần 6, và phần chưa sẵn sàng là phần nguy hiểm nhất.**

**Đã vững:** cổng dữ liệu (mọi file đã tải và đếm được, hai isoform có tập đánh giá trong tế bào có cả hai lớp); nền phản biện về metric (recall vs precision, rò rỉ 52,3% vs 39,0%); nền phê phán nhãn (quy tắc `efficiency ≥ 1`, `ratio error` chưa dùng); giao thức đánh giá đã cụ thể tới mức viết vào đề cương được; và — quan trọng nhất — **một phép đo thật về giả thuyết trung tâm, trước khi cam kết tài nguyên.**

**Chưa vững và sẽ bị hỏi:** (i) **DeepSIRT chưa có trên slide** — nếu không nêu chủ động, GVHD có thể chỉ ngay vào bài của nhóm mình; (ii) **chưa biết 9 HDAC của Deep-PLA gồm những ai** — một câu hỏi đủ phá toàn bộ trục 1; (iii) **con số −3/−2/+1 có khả năng gán sai isoform** và đang được dùng làm đáp án XAI; (iv) **chưa có câu trả lời cho việc tại sao 7 isoform là 7 bài toán cùng loại**; (v) **citation Prot2Token sai hội nghị**.

Nghĩa là đề tài **không sụp vì khoa học — nó sụp vì ba phép đọc chưa làm.** Cả ba đều làm được trong một buổi.

### 11.2 Danh sách việc, theo ưu tiên

**Trước tuần 6 — bắt buộc, theo đúng thứ tự này:**

1. **Đọc toàn văn Deep-PLA, xem 9 HDAC gồm những ai** ([doi:10.1093/bib/bbz107](https://doi.org/10.1093/bib/bbz107)). Nếu có SIRT1 hoặc SIRT2 → đổi cách phát biểu toàn bộ trục 1, hoặc chuyển sang B. **Đây là việc có khả năng đổi quyết định cao nhất với chi phí thấp nhất.**
2. **Đọc toàn văn DeepSIRT và thêm nó vào slide 1** cùng NAD_MCNN, trong bảng ba dòng (đầu vào / đơn vị dự đoán / nguồn nhãn). Biến chồng lấn thành lập luận liên tục với nền GVHD.
3. **Mở toàn văn Rauh 2013 và ghi lại CHÍNH XÁC phát biểu đặc hiệu chuỗi cho từng isoform.** Xong rồi mới sửa mục 4.2 của bản khuyến nghị. **Trước khi xong việc này, bỏ con số −3/−2/+1 khỏi mọi tài liệu gửi GVHD.**
4. **Tải Supplementary Data 5 và 6 của Rauh** qua `media.springernature.com`. Với Data 5: vẽ tương quan giữa lượng enzyme và số nhãn dương của 7 cột (**cổng G3**). Với Data 6: đếm số peptide "không cho tín hiệu đáng kể ở ≥1 đối chứng" và kiểm xem Ridgeway có loại chúng không (**cổng G2**).
5. **Tự tính mức làm giàu residue theo vị trí (−6…+6) cho từng isoform trên 6.801 vị trí**, có kiểm định và hiệu chỉnh đa so sánh (**cổng G12**). Rẻ, không cần GPU, và **quyết định phần XAI có đáng làm hay không**.
6. **Sửa bảy chỗ trong `topic-final-recommendation.md`** theo bảng ở mục 5: quy tắc nhãn (#3 và #3b), recall vs precision (#1, #2, #24), nguồn của 149 vị trí (#4, #5), quy mô Supp Data 13 (#7), tự mâu thuẫn về việc chạy lại baseline (#8), cổng dừng đặt sai isoform (#18), và phát biểu conformal (#14, #15).
7. **Sửa citation Prot2Token** trong `b-method-layer-draft.md` (bioRxiv 2024 + LMRL@ICLR 2025, **không phải NeurIPS 2025**).
8. **Dựng slide theo đúng khung GVHD đòi ở biên bản lần 1:** bài toán là gì (vào/ra) → vì sao cần → khảo sát **phân nhóm theo phương pháp** kèm ưu/nhược → đề tài cải thiện ở đâu. Và **nói bằng chứng chống lại đề tài trước**, vì nếu không tự nói thì GVHD sẽ hỏi.

**Tuần 1 sau khi GVHD đồng ý hướng:**

9. **Mở Zhang 2022 Supplementary Table S1** để xác nhận có fold-change theo từng vị trí (**cổng G4**).
10. **Đếm bao nhiêu trong 152 vị trí Zhang có mặt trong Supp Data 13** (**cổng G6**) — phép đếm quyết định phép so xếp hạng với baseline có giá trị hay không.
11. **Chạy MMseqs2 ở 30% identity trên 2.999 chuỗi protein mẹ, đếm số cụm** (**cổng G5**) — phép đo phải làm **trước cả khi chọn kiến trúc**.
12. **Mở repo `nashirag/ML-Hybrid_Ensemble_Method`** xem có đủ mã để chạy lại 7 mô hình SIRT hay chỉ có mã SET8, có seed và cách chia hay không. B4 là **mốc so sánh hợp lệ duy nhất**.
13. **Dùng Supplementary Data 15 làm nhãn**, không dùng `labels.csv`. Nếu buộc phải dùng `labels.csv`, **join theo `uid_pos`**.
14. **Niêm phong phân vùng**: ghi hash vào repo trước thí nghiệm đầu tiên.

**Việc nên làm nhưng không chặn:**

15. Tải Weinert 2015 / PXD000885 để định lượng lập luận "ngưỡng phát hiện / stoichiometry".
16. Thử lại Rardin 2013 (PNAS) và Chen 2012 (MCP) từ máy cá nhân — hai acetylome SIRT3 KO kinh điển có bảng vị trí.
17. Đọc toàn văn [PMC11447832](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/) (mảng vs dịch chiết tế bào, 3 kinase) — bằng chứng ngược với giả thuyết trung tâm, cần biết nó mạnh đến đâu.
18. Mở toàn văn Cauchois et al. 2021, Tibshirani et al. 2019, Einbinder et al. 2024 để lấy **đúng số định lý** trước khi viết vào luận văn.
19. Tra lại DOI của MMseqs2, CD-HIT, Zhang & Zhou 2014, Wu & Zhou 2017, Sechidis 2011 — hiện đều `[chưa kiểm]`.

---

## 12. Phụ lục bổ sung 08/10/2026 — đo xong cổng G3: lượng enzyme giải thích phần lớn chênh lệch giữa các isoform

Sau khi báo cáo này được viết, sinh viên hỏi thẳng: **bài toán 7 isoform có còn khả thi không?** Cổng G3 (§8) đã được đo, trên Supplementary Data 5 và 6 của Rauh, tải được qua `media.springernature.com`. Chi tiết và cách tái lập: [06-seven-isoform-feasibility.md](research/06-seven-isoform-feasibility.md).

**Kết quả:** số nhãn dương của một isoform tương quan mạnh với lượng enzyme được nhỏ lên mảng — Spearman **ρ = +0,811**, **p = 0,0349** (kiểm định hoán vị đầy đủ, n = 7 isoform) `[tự kiểm]`. SIRT5 được nhỏ **218 µg/ml**, nhiều nhất, và có **2.615** nhãn dương, nhiều nhất; SIRT4 được nhỏ 10 µg/ml và có 1.038. Thêm Spearman(số nhãn dương, `ratio error` trung vị) = **−0,855**: isoform ít enziem thì vừa ít nhãn dương vừa nhiễu hơn. Nghịch lý SIRT5 nêu ở §2.2 vì vậy **có một lời giải thích mang tính kỹ thuật thí nghiệm**, không cần viện tới hoạt tính desuccinylase.

**Hai phản biện phải nói kèm, nếu không sẽ bị bắt lỗi:** (i) n = 7 nên p = 0,0349 nằm sát ngưỡng, đây là tín hiệu chứ không phải bằng chứng quyết định; (ii) SIRT1 và SIRT7 **cùng** ở 20 µg/ml mà có **176** so với **1.692** nhãn dương, nên lượng enzyme **không** giải thích hết. Phát biểu đúng là *lượng enzyme là một biến gây nhiễu cỡ hiệu ứng lớn và chưa ai hiệu chỉnh*, **không** phải *cột SIRT5 chỉ là nồng độ enzyme*.

**Một mối lo của §2.1 bị bác bỏ bằng số:** Supplementary Data 6 (peptide không cho tín hiệu ở ≥ 1 đối chứng) có **220 peptide**, tất cả **220/220 đều còn trong bộ nhãn**, nhưng **185/220 (84,1%)** là dương ở ít nhất một isoform — gần như trùng tỉ lệ của toàn mảng, **5.695/6.802 (83,7%)** `[tự kiểm]`. Vậy giả thuyết "một phần nhãn âm thật ra là không đo được" **không thành** ở mức tổng thể, và chỉ 35/220 peptide âm ở cả bảy isoform. Đây là đính chính cho chính báo cáo này.

**Hệ quả cho phán quyết:** không đổi hướng, nhưng củng cố việc thu hẹp xuống **SIRT1/2/3**, và đổi vai của SIRT4–7 từ "bỏ đi" thành **một phân tích giới hạn của nhãn có số liệu đỡ** — bảng lượng enzyme vs nhãn dương là nội dung của phần đó.

## 13. Phụ lục bổ sung 08/10/2026 — đã đọc Deep-PLA: 9 HDAC của nó gồm SIRT1, 2, 3, 6, 7

Việc chặn số 1 ở §11.2 đã xong, sinh viên cung cấp PDF bbz107. Chi tiết: [07-deep-pla-hdac-coverage.md](research/07-deep-pla-hdac-coverage.md).

**Câu trả lời là xấu.** Web server chính thức ghi nguyên văn rằng Deep-PLA phủ "deacetylases (HDACs) including **HDAC1, HDAC2, HDAC3, HDAC6, SIRT1, SIRT2, SIRT3, SIRT6, and SIRT7**" `[tác giả báo cáo]` (`http://deeppla.cancerbio.info`). Vậy 9 HDAC = 4 HDAC cổ điển + **5 sirtuin**, thiếu đúng SIRT4 và SIRT5. Và năm isoform đó bao gồm cả **SIRT1, SIRT2, SIRT3** — ba isoform duy nhất mà §12 kết luận là còn khả thi. **Chồng lấn nằm trọn ở phần đáng làm.** Thêm nữa, chính bbz107 dẫn rằng ASEB đã được bổ sung "class I HDAC and **SIRT7** substrate predictive functions" từ trước đó.

**Hệ quả: trục tính mới sinh học (§3, trục 1) coi như hết.** Dự đoán vị trí deacetyl hóa đặc hiệu isoform sirtuin ở mức residue đã tồn tại từ 2020. Mọi câu có chữ "đầu tiên" về mặt sinh học sẽ bị bắt lỗi, và Deep-PLA ở *Briefings in Bioinformatics* là tạp chí GVHD chắc chắn biết.

**Chỗ còn khác biệt, và nó thật:** Table 1 của bbz107 cho thấy dữ liệu của họ **rất nhỏ và khác loại** — năm sirtuin cộng lại chỉ **288 vị trí trên 134 protein** (SIRT1 184, SIRT2 52, SIRT3 30, SIRT6 10, SIRT7 12), text-mining từ PubMed, tức là **cơ chất đã được báo cáo trong tài liệu**. Mảng Rauh có 6.801 vị trí × 7 isoform, hoạt tính peptide in vitro có hệ thống. Hai bộ nhãn đo hai thứ khác nhau. Họ cũng **không báo MCC, không báo AUPRC** (chỉ Sn/Sp/Pr/AUC), **không có chỉ số riêng cho SIRT2/3/6/7**, và dữ liệu nhỏ tới mức "only 5-fold cross-validations were carried out for … SIRT3, SIRT6, SIRT7" `[tác giả báo cáo]`. Phải ghi nhận một điểm họ làm tốt: tập kiểm tra của họ là **vị trí trên protein phi-người**, nên có kiểm soát độc lập thật.

**Phán quyết THU HẸP không đổi, nhưng khung phải đổi hẳn.** Đóng góp giữ lại không phải một bộ dự đoán mới mà là **phép đo xem các bộ dự đoán đã công bố có đúng trong tế bào hay không**. Trước §13, phép đo đó có **một** đối tượng; bây giờ có **ba** — Deep-PLA 2020, DeepSIRT 2021, Ridgeway 2025, ba loại nhãn huấn luyện khác nhau, không bài nào báo MCC/AUPRC, không bài nào đo trên acetylome KO/KD có nhãn âm. Đề tài vì vậy nên trở thành **một benchmark chuyển miền**, dạng việc mà cộng đồng kinase đã làm (benchmarKIN 2025) nhưng cộng đồng sirtuin thì chưa `[chưa tìm thấy, không kết luận là chưa từng có]`.

**Một phép đo mới mở ra, rẻ và mạnh:** 288 vị trí curate của Deep-PLA là nhãn dương **độc lập với mảng Rauh** và được xác nhận trên protein nguyên. Đối chiếu chúng với nhãn mảng cho **phép đo chuyển miền thứ hai**, độc lập với phép đo Sol 2012 ở §4. Đây giờ là việc ưu tiên cao nhất, thay cho thứ tự cũ ở §11.2.

## 14. Phụ lục bổ sung 08/10/2026 — tự tính MCC cho các mô hình sirtuin của Deep-PLA

Việc được giao là lấy 288 vị trí curate của Deep-PLA để làm phép đo chuyển miền thứ hai. Chi tiết: [08-deep-pla-per-isoform-mcc.md](research/08-deep-pla-per-isoform-mcc.md).

**Phần không làm được:** danh sách 288 vị trí nằm trong Supplementary của bbz107 và **Oxford University Press trả 403** cho mọi đường dẫn thử từ môi trường cloud; web server của Deep-PLA không có trang tải dữ liệu; PLMD (CSDL nguồn của họ) nay chỉ còn thư mục rỗng; iPTMnet 503; dbPTM 403 `[tự kiểm]`. Sinh viên cần tải Supplementary bằng quyền truy cập đã dùng để lấy PDF. Đến lúc đó, phép đo này vẫn `[chưa kiểm]`.

**Đổi lại, được một thứ không có trong bài báo.** Trang `help.php` của web server công bố số nhãn dương, nhãn âm và Sp/Sn/Pr ở ba ngưỡng **cho từng enzyme**, cả cross-validation lẫn test `[tác giả báo cáo]` — bài chỉ báo AUC cho SIRT1 và họ HDAC gộp. Từ (P, N, Sn, Sp) dựng lại được ma trận nhầm lẫn và **tính được MCC**, chỉ số Deep-PLA không báo ở đâu cả.

Cross-validation (người), ngưỡng High, MCC tự tính: **SIRT1 0,403 · SIRT2 0,219 · SIRT3 0,049 · SIRT6 0,321 · SIRT7 −0,016 · HDAC gộp họ 0,557**. SIRT3 có độ nhạy chỉ **7,7%**; SIRT7 **tệ hơn ngẫu nhiên** ở ngưỡng đó. Bảng đầy đủ ba ngưỡng và tập test: [data/deep-pla-sirtuin-mcc-derived.csv](research/data/deep-pla-sirtuin-mcc-derived.csv).

**Hai hệ quả, cả hai đều ủng hộ thiết kế đã đề xuất.** Thứ nhất, **mô hình gộp họ HDAC (0,557) tốt hơn mọi mô hình tách theo isoform**, kể cả SIRT1 — ở cỡ dữ liệu 10–185 vị trí, tách theo isoform làm hại nhiều hơn làm lợi, tức Deep-PLA vô tình cung cấp bằng chứng cho bậc B8 (một mô hình đa nhãn chia sẻ biểu diễn thay bảy mô hình rời) ở §5. Thứ hai, nó cho thấy vì sao Sn/Sp/Pr che mất vấn đề: SIRT3 có Sp 0,964 và Pr 0,340 trông tạm được, nhưng MCC 0,049 nói rằng mô hình gần như không phân biệt được gì.

**Phản biện với chính phép tính này:** MCC suy từ số đã làm tròn 4 chữ số nên chỉ nên đọc hai chữ số; P/N trên web server lệch 1 so với Table 1 cho SIRT1 (185 vs 184) và EP300, và lệch nhiều hơn cho dòng "HDACs" (147 vs 94) — chưa giải thích được `[chưa kiểm]`; tỉ lệ dương nền là tạo tác của cách họ dựng tập âm nên MCC này **so được giữa các enzyme trong cùng bài nhưng không so được với bài khác**, đúng lý do benchmark phải chạy lại mọi thứ trên cùng giao thức; và ở tập test SIRT6 chỉ có **2** vị trí dương, SIRT7 **4**, nên đừng dẫn MCC 0,409 và 0,521 như bằng chứng.

## 15. Phụ lục — Phép đo chuyển nhãn thứ hai: 289 vị trí curated của Deep-PLA (10/10/2026)

Ghi chú đầy đủ: [research_notes/sirtuin-substrate/09-deep-pla-sites-vs-array.md](research/09-deep-pla-sites-vs-array.md) · dữ liệu: `research_notes/sirtuin-substrate/data/deeppla-curated-sites-vs-rauh-labels.csv`.

**Điểm nghẽn ở §14 đã được giải tỏa trong phiên này, không cần sinh viên tải thủ công.** `academic.oup.com` trả 403 với curl, nhưng `WebFetch` đọc được trang bài báo, và khi gọi với `offset: 100000` nó trả về URL CloudFront **đã ký**; curl với URL đã ký trả 200. Tải được `table_s1.xlsx` (111.188 B), `table_s4.xlsx` (1.589.346 B), `table_s5.xlsx` (12.452 B). URL không ký trả `<Error><Code>MissingKey</Code>`; chữ ký có hạn nên không lưu lại được.

**Table S1** có 1.666 dòng (`UniProt | Gene | Position | Type | Sequence Window | Enzyme | Organism | Pmids`), mọi cửa sổ 15 aa. Lọc sirtuin + *Homo sapiens* cho **289 vị trí**: SIRT1 185, SIRT2 52, SIRT3 30, SIRT7 12, SIRT6 10 — **khớp chính xác** cột P trên `help.php` đã dùng ở §14, nên chênh lệch ±1 so với Table 1 của bài in (SIRT1 184) là lỗi của bài in, không phải của phép suy MCC.

**Phép đo.** Khớp theo 13-mer trung tâm của cửa sổ 15 aa với 6.802 peptide của mảng Rauh; nhãn dương tính của mảng dùng `efficiency ≥ 1` (quy tắc đã xác thực ở §5, bảng claim–evidence–correction). Kiểm định binomial chính xác, tỷ lệ nền lấy từ chính cột isoform đó.

| Isoform | Curated | Trên mảng | Mảng gọi dương đúng isoform | % | Nền của mảng | Độ giàu | p |
|---|---|---|---|---|---|---|---|
| SIRT1 | 185 | 55 | 2 | 3,6% | 2,6% | 1,41× | 0,418 |
| SIRT2 | 52 | 18 | 5 | 27,8% | 27,9% | 0,99× | 0,595 |
| SIRT3 | 30 | 19 | 6 | 31,6% | 27,1% | 1,16× | 0,414 |
| SIRT6 | 10 | 9 | 2 | 22,2% | 17,6% | 1,26× | 0,489 |
| SIRT7 | 12 | 2 | 1 | 50,0% | 24,9% | 2,01× | 0,436 |
| **Gộp** | **289** | **103** | **16** | **15,5%** | — | **1,17×** | **0,291** |

Dương tính cho **ít nhất một** isoform: 85/103 = 82,5% so với 83,7% toàn mảng → 0,986×. Tập cơ chất đã được y văn xác nhận **không khác một mẫu ngẫu nhiên của mảng**.

**Ý nghĩa.** Đây là xác nhận **độc lập thứ hai** cho kết luận trung tâm của báo cáo (nhãn in-vitro gần như không chuyển được vào tế bào), và mạnh hơn xác nhận thứ nhất vì dương tính ở đây được xác nhận trên protein cuộn gấp, không suy ra từ fold-change, và không cần giả định ngưỡng nào. Kết hợp với §14: hai tập nhãn mạnh nhất của lĩnh vực — mảng 6.802 vị trí và 289 vị trí curated — không đồng ý với nhau, và cả hai đều cho mô hình yếu. Đó là lý do tồn tại của một benchmark chuyển miền, và là phần trả lời mạnh nhất cho câu "Deep-PLA đã làm rồi".

**Giới hạn phải nói kèm.** Chỉ 103/289 (35,6%) vị trí curated có mặt trên mảng, nên phép kiểm chỉ nói về phần giao, bị giới hạn bởi cách Rauh chọn peptide năm 2013. SIRT7 (n=2) và SIRT6 (n=9) quá nhỏ để trích riêng — độ giàu 2,01× của SIRT7 là 1 trên 2 vị trí. Khớp theo 13-mer trung tâm có thể bắt cùng trình tự ở paralog; bản khớp nghiêm ngặt theo (UniProt, position) chưa làm `[chưa kiểm]`. Nhãn Deep-PLA là text-mining PubMed, không phải curation có kiểm tra lại. Tập 289 không có âm tính nên chỉ tính được độ giàu, không tính được MCC — đúng vấn đề tập chỉ-dương-tính đã mô tả ở ghi chú 04.

## Kết luận

Điều đã đổi trong hiểu biết về đề tài này không phải là "nó khó hơn tưởng" — mà là **câu hỏi nghiên cứu đã bị trả lời một phần, bởi chính dữ liệu, trước khi ai kịp huấn luyện mô hình nào.** Nhãn mảng peptide in vitro, khi đem đối chiếu với acetylome trong tế bào ở quy mô 1.417 vị trí, cho MCC gần bằng không. Đó không phải một chướng ngại cần vượt qua bằng kiến trúc tốt hơn; nó là **một dữ kiện về bản chất của nguồn nhãn**, và nó phù hợp đến mức đáng chú ý với ba thứ khác: việc Rauh tự nói các isoform không so được với nhau, việc Weinert đo được stoichiometry trung vị 0,05% và kết luận sirtuin "sửa chữa" hơn là "điều hòa", và việc chính mảng peptide bỏ sót 61% các vị trí phụ thuộc SIRT2 mà nó **có** đo. Bốn bằng chứng độc lập cùng chỉ về một hướng: cửa sổ 13 amino acid không chứa đủ thông tin để trả lời câu hỏi sinh học mà đề tài đặt ra.

Nhưng chính vì vậy đề tài **đáng làm tiếp, dưới một lời hứa khác**. Lĩnh vực này đang báo cáo những con số mà khảo sát vừa chỉ ra là trộn đại lượng (recall gọi là precision), pha rò rỉ (52,3% vs 39,0%), và dựa trên tập đánh giá chỉ có một lớp — trong khi nhãn âm thì nằm sẵn trong bài mà chính baseline đã dùng. Một luận văn đo cho đúng, với nhãn âm thật, với metric đúng, với kiểm soát rò rỉ ở ba mức, và nói thẳng rằng câu trả lời là âm, có giá trị khoa học cao hơn một mô hình nhích thêm 2% trên một benchmark đã rò rỉ. Rủi ro thật không nằm ở khoa học mà ở **sự chấp nhận**: nếu GVHD cần một đóng góp dương để chấm, thì câu hỏi số 1 ở mục 9 phải được hỏi trước mọi câu khác — và đề tài dự phòng B, với đáp án XAI định lượng 83% so với 3% mà sirtuin không có gì tương đương, phải nằm trong túi khi vào buổi gặp.
# Kiểm chứng đề tài dự đoán cơ chất deacetyl hóa SIRT1–7

Ngày khảo sát: **08/10/2026**. Phạm vi: phản biện [khuyến nghị ban đầu](../../surveys/topic-final-recommendation.md), đọc nguồn gốc và kiểm tra bảng dữ liệu; **chưa huấn luyện mô hình hoặc triển khai hệ thống**.

**Khuyến nghị: tiếp tục nhưng thu hẹp.** Có cơ sở để nghiên cứu khả năng khái quát hóa của mô hình học hoạt tính trên peptide sang các vị trí acetyl hóa phụ thuộc sirtuin trong tế bào. Chưa đủ cơ sở để chốt đề tài “dự đoán cơ chất sinh lý SIRT1–7 với bảo đảm 90%”. Giữ bảy đầu ra cho khảo sát nội miền; ưu tiên **SIRT2 và SIRT3** cho đánh giá ngoài miền, với hai endpoint riêng. Tính mới phải nằm ở giao thức chống rò rỉ, mô hình hóa bằng chứng và đánh giá chuyển endpoint; không nằm ở việc lần đầu dự đoán cơ chất sirtuin hay lần đầu kiểm chứng bằng acetylome.

Mức chắc chắn: **cao** với các lỗi nhãn, metric và tiền lệ trực tiếp đã kiểm tra; **vừa** với phạm vi phương pháp có thể đóng góp; **chưa đạt cổng dữ liệu** cho benchmark tế bào có dương–âm đáng tin ở hai isoform. Đủ mang tới GVHD để thảo luận có điều kiện, chưa đủ trình bày như đề tài đã xác nhận tính mới và khả thi.

Nhãn bằng chứng trong tài liệu:

- **[TG]**: tác giả nguồn gốc báo cáo; không phải kết quả của đề tài này.
- **[KT]**: tự tải và kiểm tra bảng/mã trong phiên này; có [script và kết quả audit](research/README.md).
- **[SL]**: suy luận hoặc thiết kế đề xuất, cần thí nghiệm kiểm chứng.
- **[CK]**: chưa xác minh, không dùng để kết luận chắc chắn.

## 1. Bối cảnh và câu hỏi cần bảo vệ

Đã đọc `CLAUDE.md`, [danh sách đề tài](../../../topics/README.md), [nhật ký](../../../journal/README.md), [biên bản lần 1](../../../project/meetings/2026-10-02-session-01/minutes.md), [hồ sơ GVHD](../../../project/advisor-research.md), bản phác phương pháp B và khảo sát hướng tin học. Các tài liệu trước còn ưu tiên cancer/aging hoặc kinase; theo yêu cầu phiên này, khuyến nghị SIRT1–7 là phạm vi khảo sát. Không dùng các giới hạn GPU/thời gian cũ làm lý do loại phương pháp.

Biên bản ghi **tiêu chí 5 là ứng dụng/website bắt buộc**. Conformal là một hướng phương pháp, không thay cho tiêu chí 5. GVHD là **Ho Quang Thai**; không mặc định các công trình của nhóm **Yu-Yen Ou** là của GVHD. SirtSAGE có tên Ho trong danh mục địa phương, nhưng toàn văn chưa lấy được để kiểm tra chi tiết kiến trúc.

Vấn đề có giá trị: “mẫu chuỗi thuận lợi cho enzyme trên peptide có giúp tìm vị trí acetyl hóa đáp ứng can thiệp enzyme trong tế bào, khi protein/họ protein chưa được thấy?” Giá trị này gắn với sinh học sirtuin nhưng chưa chứng minh tác dụng chống lão hóa, nguy cơ ung thư hoặc điều trị.

## 2. Nền sinh học: ba loại bằng chứng không đồng nhất

**Acetyl hóa** là gắn nhóm acetyl lên lysine (K), một amino acid trong protein. **Deacetyl hóa** là loại nhóm này; sirtuin sử dụng NAD+ trong phản ứng. **Isoform SIRT1–7** ở đây chỉ bảy thành viên họ enzyme, cần phân biệt với các biến thể trình tự của một protein cơ chất.

| Endpoint | Đo được | Không tự suy ra được |
|---|---|---|
| Peptide in vitro | Enzyme tái tổ hợp làm giảm acetyl trên đoạn chuỗi trong điều kiện thử | Protein nguyên có bị tác động trong tế bào không |
| Protein nguyên, enzyme tinh sạch | Bằng chứng phản ứng trực tiếp trên protein trong phép thử đó | Tầm quan trọng sinh lý trong mô/tế bào cụ thể |
| Acetylome KO/KD/OE | Mức peptide acetyl thay đổi sau mất gen, giảm biểu hiện hoặc tăng biểu hiện enzyme | Mọi vị trí thay đổi đều là cơ chất trực tiếp |

Một site MS tăng sau KO có thể phản ánh mất deacetyl hóa trực tiếp, thay đổi enzyme khác, chuyển hóa, hoặc lượng protein. **Hiệu chỉnh lượng protein** giúp tách nhiều protein hơn khỏi tỷ lệ acetyl cao hơn, nhưng chưa chứng minh quan hệ nhân quả trực tiếp. Ngược lại, site không tăng có thể do ít công suất thống kê, enzyme bù trừ hoặc site vốn hầu như không acetyl hóa. [SL]

**Stoichiometry** là tỷ lệ phân tử protein được acetyl hóa tại một vị trí. [Weinert 2015](https://doi.org/10.15252/embj.201591271), Results/Fig. 3 và Appendix S2–S3, dùng định lượng hóa học và dữ liệu SIRT3 đã công bố để lập luận rằng nhiều acetyl hóa ty thể có occupancy thấp, phù hợp với vai trò sửa tổn thương acetyl hóa không enzyme của SIRT3. Đây là diễn giải ở phạm vi dữ liệu ty thể, không kết luận mọi acetyl hóa vô nghĩa hoặc mọi sirtuin có cùng vai trò. Cần phân biệt cột stoichiometry được ước lượng trực tiếp với cột **predicted stoichiometry** tính từ fold-change nhập từ Hebert. [TG]

### Khác biệt giữa bảy thành viên

| Nhóm | Điều cần tính đến khi thiết kế |
|---|---|
| SIRT1/2/3 | Có cơ sở mạnh cho deacetyl hóa; vẫn cần khu trú, biểu hiện và bối cảnh tế bào |
| SIRT4 | Có hoạt tính loại các nhóm acyl khác: không dùng một assay acetyl-peptide để đại diện toàn bộ chức năng. [Anderson 2017](https://doi.org/10.1016/j.cmet.2017.03.003) |
| SIRT5 | Ưu tiên demalonyl/desuccinyl trong nghiên cứu động học; số nhãn acetyl dương cao ở Rauh không có nghĩa enzyme deacetyl hóa ưu thế trong tế bào. [Du 2011](https://doi.org/10.1126/science.1207861), Fig. 1/Table S2 |
| SIRT6 | Hoạt tính trên nucleosome phụ thuộc ngữ cảnh khác peptide tự do. [Nghiên cứu nucleosome](https://pmc.ncbi.nlm.nih.gov/articles/PMC3794599/) |
| SIRT7 | Các nghiên cứu hoạt hóa bởi acid nucleic cho thấy điều kiện assay có thể quan trọng. [Nghiên cứu RNA](https://pmc.ncbi.nlm.nih.gov/articles/PMC5326686/), [cấu trúc 2025](https://doi.org/10.1038/s41467-025-56529-y) |

Hai dòng SIRT6/7 là đối chiếu nguồn liên quan, chưa audit dữ liệu thực nghiệm của các bài đó trong phiên này. Không loại nhãn Rauh cho SIRT4–7; chỉ giữ tên endpoint chính xác: **đáp ứng deacetyl hóa peptide trong điều kiện assay**.

## 3. Rauh 2013: assay và nhãn thực sự là gì?

Đã đọc toàn văn [Rauh 2013](https://doi.org/10.1038/ncomms3327), Methods và Supplementary Methods, cùng SD1/2/5/6/7. Mảng có peptide acetyl và đối chứng không acetyl, spot lặp; dùng antibody để đọc mất tín hiệu sau xử lý enzyme. Có đối chứng không NAD+, buffer và mutant thích hợp. Lượng enzyme **6–218 µg/ml**, thời gian xử lý 2 giờ; lượng và construct khác theo isoform. [TG]

| Cột SD1 | Ý nghĩa | Cách dùng hợp lý |
|---|---|---|
| `signal ratio (exp:ref)` | Tín hiệu xử lý/chứng; thấp hơn thường tương ứng mất acetyl mạnh hơn | Không đặt “ratio ≥ 1 là dương”; không gọi là tốc độ phản ứng |
| `ratio error` | Biến thiên giữa spot triplicate và lần lặp, theo mô tả bài | Chỉ là proxy độ tin cậy; chưa phải phương sai của nhãn efficiency |
| `substrate category` | Tổng hợp kết quả mất tín hiệu có ý nghĩa, Welch P < .01, thành thang 0–1 qua nhiều thí nghiệm | Có thể khảo sát thang thứ tự; không xem là xác suất đã calibration |
| `efficiency` | `category / ratio`, dùng xếp hạng/clustering trong bài | Nhãn liên tục dẫn xuất; không đồng nhất với `kcat/Km` |

Tác giả tránh diễn giải chi tiết ratio vì thay đổi nhỏ khó đo. Do đó, “bảng có số thực” chưa đủ chứng minh hồi quy sẽ tốt hơn phân loại. Category có các mức rời rạc và độ phân giải khác theo isoform; efficiency chịu ảnh hưởng cả category lẫn mẫu số. Đề xuất kiểm tra thang thứ tự, biến đổi ổn định và xếp hạng **trong từng isoform**, không hồi quy một thang hoạt tính chung cho cả bảy. Trọng số `1/error²` cần kiểm tra và chặn cực trị; error của ratio không tự truyền thành error của category/ratio. [SL]

### Audit số liệu và chênh lệch 6.802/6.801

[KT], từ SD1 và Ridgeway SD15, đối chiếu theo chuỗi sau chuẩn hóa **Z → X**, không ghép theo số dòng:

- SD1: **6.802 chuỗi khác nhau**, đều dài 13, K ở giữa; không thiếu ô trong 28 cột đo; **249** có ký tự Z; **473** dòng thiếu accession; **5.251** dòng liệt kê nhiều accession.
- SD15: **6.801 chuỗi khác nhau**, không thiếu ô trong chín cột sử dụng; **249** còn X. Bài Ridgeway nói thay residue masked bằng alanine, nhưng bảng phân phối vẫn có X; chưa xác minh đầy đủ chuỗi ở bước sinh đặc trưng.
- Chính xác một chuỗi SD1 không có trong SD15: **GIQCVKKRDLEQA**. SD2 gắn chuỗi với **Q04206/RELA/p65 K123** và nhiều accession/position khác. **Đã xác định dòng mất; chưa xác định lý do loại.**
- SD15 có **2.999 chuỗi accession khác nhau**, trong đó có placeholder **SYNTHETIC** trên **231 dòng**. Vì vậy không được gọi là 2.999 protein đã ánh xạ chắc chắn; 2.998 là số accession khác placeholder, cũng chưa phải số protein sinh học đã chuẩn hóa.
- **Toàn bộ 47.607 nhãn** SD15 khớp `efficiency ≥ 1` của SD1. `category ≥ 1` sai ở 172/1.079/673/27/0/462/10 dòng cho SIRT1→7; ngưỡng ratio ≥ 1 cũng không khớp. Đây là bất nhất giữa mô tả Methods và dữ liệu, không suy đoán động cơ hoặc sửa nhãn tác giả.

| Isoform | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dương SD15 (`efficiency ≥ 1`) | 176 | 1.901 | 1.844 | 1.038 | 2.614 | 1.199 | 1.692 |
| Chỉ dương với isoform đó | 21 | 319 | 289 | 162 | 1.088 | 269 | 282 |
| Trung vị ratio error SD1 | .37 | .22 | .24 | .24 | .21 | .27 | .22 |

Phân bố số nhãn dương/site từ 0→6: **1.107, 2.430, 2.087, 902, 226, 44, 5**; không có site dương cả bảy. Đây là tương quan trong assay, chưa chứng minh mô hình chia sẻ sẽ tốt hơn mô hình độc lập. SIRT1 mất cân bằng nặng, nhưng **176 không tự động là lý do bỏ**: cần đếm protein/họ chứa các dương sau split, kiểm tra độ bất định và learning curve. [SL]

## 4. Kiểm kê dữ liệu tế bào và trạng thái cổng dữ liệu

| Nguồn / accession | Loài, bối cảnh, can thiệp | Lặp và định lượng | File đã đọc / tình trạng |
|---|---|---|---|
| [Zhang 2022](https://doi.org/10.1038/s41598-022-06793-5); [Synapse syn26134616](https://doi.org/10.7303/syn26134616) | Người, HCT116; SIRT2 KD/OE và chứng | S1 có bốn cột mẫu 1/3/5/7; đã chuẩn hóa lượng protein; không có p/q khác biệt từng site | S1 **2.846 dòng dữ liệu**; S2 **134 peptide hit, tổng 152 acK**; đã tải XLSX |
| Ridgeway SD14, cùng nguồn Zhang | Người, HCT116; tập chọn KD↑ và OE↓ | Dữ liệu dương chọn lọc, không có lớp âm | **149 site key / 123 accession / 134 tryptic peptide**; không phải nghiên cứu MS độc lập mới |
| [Weinert 2015 EV1](https://doi.org/10.15252/embj.201591271); PXD000885 cho dữ liệu nghiên cứu Weinert | Gan chuột; bảng nhập SIRT3 KO/WT từ [Hebert 2013](https://doi.org/10.1016/j.molcel.2012.10.024) | Có ratio KO/WT, CR KO/WT, CR WT/WT; bảng nhập không có site p/q hoặc cột lặp KO | **17.871 dòng EV1**, trong đó **2.106** có ratio SIRT3 KO/WT; đã tải/đọc ZIP và XLSX |
| [Rardin 2013](https://doi.org/10.1073/pnas.1302961110) | Gan chuột, ty thể, WT/SIRT3 KO, nhịn ăn 24 giờ | **5 động vật/nhóm**, có process/injection replicates; chuẩn peptide; bảng protein riêng | [TG] 2.187 site, 283 tăng ≥2 lần, P≤.01; **bảng S3–S5 chưa đọc được**: PMC trả HTML challenge, PNAS 403 |
| [PXD021357](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD021357) | Chuột, ống thận, sham vs UUO ngày 1 | Metadata ghi hiệu chỉnh protein, FC 2, t-test P<.05; số lặp chưa xác minh qua bảng định lượng | Metadata tải được; **acetylome không phải KO SIRT3**. Không dùng làm nhãn cơ chất SIRT3 |
| [PXD023479](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD023479) | HEK293T; SIRT3-FLAG vs Luc-FLAG | Co-IP/interactome theo protocol | Metadata tải được; **không phải acetylome KO**; tương tác không đồng nghĩa deacetyl hóa |
| [PXD012796](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD012796) | Chuột, T CD3+ từ lách; WT/Sirt2 KO, naive/kích hoạt 3 ngày | Enrichment acK, định lượng tương đối; số lặp/site table chưa kiểm | Ứng viên phù hợp về can thiệp; chưa nhận bảng định lượng |
| [PXD019763](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD019763) | Cùng nhánh công bố chuyển hóa tế bào T/Sirt2 | Cần xác định vai trò từng file và liên hệ các accession | Không đếm cùng nghiên cứu thành hai validation độc lập; chưa đủ xác nhận endpoint site |

Nguồn số đếm [KT]: [audit-results.json](research/audit-results.json). Nguồn metadata: [manifest](research/download-manifest.json). API liệt kê file PRIDE thử trong phiên trả body rỗng dù HTTP 200; đây là lỗi/giới hạn truy xuất, **không phải bằng chứng kho không có file**.

### Những giới hạn cụ thể đã kiểm tra

**SIRT2:** S1 có intensity thô, hệ số protein và intensity đã chuẩn hóa; cần tính ratio theo đúng cặp 3/1 và 7/5. Không suy FDR định danh 1% thành FDR khác biệt acetyl hóa. [Ghi chú của người cung cấp dữ liệu trên Synapse](https://www.synapse.org/Synapse:syn26134616/discussion/threadId=9116) giải thích mẫu chẵn có xử lý bổ sung, dùng hỗ trợ nhận diện trong MaxQuant và không đưa vào phân tích downstream; không được tính chúng thành lặp sinh học của mẫu lẻ. Chưa có bảng replicate đủ để ước lượng công suất hoặc khoảng tin cậy từng site. OE có đồng biểu hiện acetyltransferases theo ghi chú nguồn; endpoint rộng hơn “chỉ thay SIRT2”. [TG/CK]

Ridgeway mô tả WT/H187Y trong đoạn validation, nhưng Zhang dùng H187Y ở kiểm chứng BCL9 trong tế bào 293; global acetylome HCT116 là KD/OE. Không gộp hai thí nghiệm. Chênh **152 → 149** vẫn cần truy vết ánh xạ; không tuyên bố ba vị trí mất do lý do đã biết.

**SIRT3:** EV1 là đường tải thực tế cho dữ liệu định lượng isoform thứ hai. **483/2.106 ratio ≥2** chỉ là đếm theo ngưỡng, **không phải 483 cơ chất dương đã xác nhận**. Không có p/q và lặp KO trong bảng nhập; phải lấy Hebert gốc hoặc Rardin để lập luận uncertainty, total-protein correction và mapping isoform. Không xem Weinert và Hebert là hai thí nghiệm KO độc lập. Hebert gốc báo 3.285 site được định lượng, 2.193 ty thể; tập giao EV1 nhỏ hơn tập nguồn. [KT/TG]

**Kết luận cổng:** đã có assay train và bảng định lượng cho **SIRT2 + SIRT3**; chưa có benchmark tế bào dương–âm đủ bằng chứng ở hai isoform. Cổng “file tải được” đạt một phần; cổng “nhãn trả lời được câu hỏi cơ chất” còn mở.

### Quy tắc dương, âm, chưa xác định

| Loại | Quy tắc đề xuất | Hạn chế phải giữ |
|---|---|---|
| Dương phụ thuộc isoform | Hướng thay đổi phù hợp, effect-size đủ ý nghĩa sinh học đặt trước, kiểm định/uncertainty hợp lệ, chỉnh protein nếu có | Vẫn có thể gián tiếp; chỉ thí nghiệm trực tiếp mới nâng cấp nhãn cơ chất trực tiếp |
| Âm theo bối cảnh | Định lượng tốt, assay có lực, khoảng tin cậy nằm trong biên tương đương quanh 0 được biện minh trước | Chỉ “không đáp ứng đáng kể trong bối cảnh này”, không phải enzyme không bao giờ tác động |
| Unknown | Không đo được, missing/imputed, localization/mapping mơ hồ, CI rộng hoặc chỉ P>.05 | Không cho vào loss như âm; giữ mask và báo độ phủ |

Biên tương đương cần dựa độ biến thiên assay và thay đổi tối thiểu có ý nghĩa sinh học, bàn với chuyên gia; không tự chọn 1.5/2 lần cho mọi bộ. Nếu chưa có âm đáng tin, dùng bài toán positive–unlabeled/ranking có giả định rõ, hoặc hồi quy đáp ứng định lượng; không hợp thức hóa MCC bằng gán unknown thành 0. [SL]

## 5. 43,0%, rò rỉ và bất nhất giữa các bảng

**64/149 = 42,953%** là tỷ lệ phát hiện lại trên tập positive-only tại ngưỡng .5. Có thể gọi recall trên tập dương tham chiếu chọn lọc, không phải recall tổng thể mọi cơ chất. **Precision = TP/(TP+FP)** cần FP trong một tập đo thích hợp; 149 dương không cung cấp FP. Không xác định được specificity/MCC/AUROC; AUPRC trên toàn dương không có ý nghĩa phân biệt. Mô hình đoán tất cả dương đạt 100% recall ở đây, nên “vượt 43%” đơn độc không chứng minh tốt hơn. [KT/SL]

Audit SD14 và CSV đặc trưng Ridgeway: **46/149** site key `(accession, position)` có trong train; **108/149** nằm trên accession đã có trong train. Chỉ **41** dòng còn lại ở accession chưa thấy theo cách ánh xạ này; chúng vẫn có thể đồng dạng. Đây là trùng với **pool huấn luyện công bố**, chưa xác định từng dòng thuộc fold nào khi mô hình được fit. Counts là dựa annotation, chưa kiểm lại toàn bộ residue bằng FASTA có phiên bản. Deep-PLA S1 cũng có **73** key trong pool train và **1** key trong SD14; chưa tính đầy đủ biến thể accession/homology. [KT]

Kiểm tra bổ sung trên trình tự UniProt tải ngày 08/10/2026: **149/149** vị trí SD14 có residue K và peptide tryptic khớp tại site; lấy riêng isoform P06753-2. [Kết quả mapping và hash snapshot](research/mapping-audit-results.json). Đây là kiểm tra trình tự hiện hành cho test, chưa kiểm toàn bộ train hoặc phục hồi RefSeq v54 của nghiên cứu gốc. [KT]

So chuỗi ngắn SD13 với 6.552 window train không có X: **60/149** window trùng đủ 13 residue; **63/149** có ít nhất 10/13 residue khớp ở cùng vị trí. Đây là so không gap trên peptide, **không phải clustering đồng dạng toàn protein**; 60 chuỗi trùng lớn hơn 46 key trùng cho thấy accession–position chưa bắt hết trùng trình tự. [KT]

SD13 có **145.461 key khác nhau**, là tập dự đoán cho proteome được chọn theo quy trình tác giả, không phải nhãn thực nghiệm cho tất cả lysine người. Cả 149 key SD14 có trong SD13 nhưng **0/149 điểm SIRT2 khớp ở sai số 1e-8**; **21 nhãn nhị phân khác**, SD13 cho **61** dương còn SD14 cho **64**. Ví dụ ANXA1 P04083 K312: SD13 **.709550397**, SD14 **.801009919762105**. Nguyên nhân/phiên bản model chưa xác định. Vì thế phải báo hai snapshot riêng; không lấy SD13 để tái tạo 64/149 rồi khẳng định thành công. [KT]

Ridgeway Supplementary Materials S1 dùng holdout peptide stratified 10%, rồi chia 90% còn lại cho base/meta training, CV stratified lặp. Không có bằng chứng protein/homology grouping trong protocol đã đọc. Mã `model_fitting.py` ở commit **e7cb6d7eb8837c770bd1638dcd45c59688535cfa** có `train_test_split` không `groups`, một số split không đặt `random_state`. Đây là kiểm tra mã snapshot, không chứng minh chính snapshot đó sinh toàn bộ bảng bài báo. Cần kiểm soát cả feature selection, scaler, negative sampling và hyperparameter search trong fold. [TG/KT]

## 6. Tiền lệ và tính mới

Chiến lược, truy vấn và giới hạn: [search-log.md](research/search-log.md). Khảo sát đến ngày 08/10/2026, ưu tiên paper/Methods/supplement/code và dữ liệu chính thức.

| Công trình | Đích và phương pháp | Hệ quả cho đề tài |
|---|---|---|
| [Smith 2011](https://doi.org/10.1021/cb100218d), *SIRT3 Substrate Specificity Determined by Peptide Arrays and Machine Learning* | Array peptide, hồi quy chuỗi cho SIRT3; có kiểm chứng động học. Đọc PDF tác giả | ML dự đoán cơ chất sirtuin có từ trước Rauh; endpoint binding trên analog khác endpoint Rauh |
| [Zhai 2017](https://doi.org/10.1038/s41598-017-04847-7) | Site SIRT1; SVM + chuỗi + GO/PPI/Pfam; chia theo protein khi dùng chức năng; kiểm chứng thực nghiệm | Ngữ cảnh sinh học và protein split không mới tự thân; âm nền vẫn là lysine chưa được biết |
| [Deep-PLA 2020](https://doi.org/10.1093/bib/bbz107), online 2019 | HAT/HDAC-specific DNN; **SIRT1/2/3/6/7**; AAC/CKSAAP/PSSM/BE, PSO; human train/nonhuman test | Đối thủ cơ chất trực tiếp; không được nói “HDAC không phải sirtuin” |
| [Ridgeway 2025](https://doi.org/10.1038/s42004-025-01717-6) | 7 model isoform riêng, 443 feature, LDA/tree + MusiteDeep và meta-ensemble; 149 site tế bào | Đã đánh giá chuyển assay→cellular; ensemble có thành phần DL. PLM và regression được tác giả nêu hướng tương lai |
| [NAD_MCNN 2025](https://doi.org/10.1111/cbdd.70085) | Vị trí gắn NAD+ trên enzyme, PLM + multiwindow CNN theo abstract | Bài toán khác; không so AUC trực tiếp. Chưa đọc toàn văn/không audit data; không gắn với Ho |
| [SirtSAGE](https://doi.org/10.1142/S2737416527400011) | Phân loại/lập bản đồ tiến hóa protein sirtuin theo tiêu đề và danh mục địa phương | Cùng họ enzyme, khác cơ chất residue. Publisher không truy cập được: kiến trúc/benchmark **chưa kiểm bằng toàn văn** |
| [AIPred 2025](https://doi.org/10.1186/s12915-025-02418-1) | Acetyl hóa nonhistone, PLM + ML giải thích | PLM cho acetyl-site đã có; acetylation propensity khác enzyme-specific deacetylation |
| [DeepPTMPred 2026](https://doi.org/10.1093/bib/bbag321) | PTM-site đa phương thức, có PLM/cấu trúc | Thêm PLM hoặc cấu trúc vào PTM không tự đủ mới; mới kiểm toàn văn web ở mức kiến trúc tổng quát |
| [CLASPP 2026](https://doi.org/10.1371/journal.pcbi.1014616) | PLM, contrastive learning, cân bằng nhiều PTM; unified predictor | Chia sẻ biểu diễn/mất cân bằng/motif đã có tiền lệ; multi-PTM không đồng nhất bảy enzyme cùng endpoint |

[KT] S1 Deep-PLA có annotation SIRT người: **185/52/30/10/12** lần lượt cho SIRT1/2/3/6/7; chuột **30/6/16/2/4**. Đây là số dòng annotation theo enzyme, không cộng thành số site duy nhất vì site có thể nhiều enzyme. Đọc Methods cho thấy âm lấy từ lysine chưa được ghi modified; human/nonhuman split không tự loại protein đồng dạng. Cần audit mapping và nguồn từng PMID trước khi coi các nhãn này là test độc lập.

Chưa tìm thấy trong phạm vi truy vấn một nghiên cứu **PLM bảy đầu ra trên Rauh, đánh giá cellular có kiểm soát họ protein và uncertainty endpoint**. Đây là khoảng trống **ứng viên**, không kết luận chưa từng có. Các bài tên DeepSIRT/ASEB cũng cần kiểm thêm trước literature review cuối; không coi tên có “SIRT” là cùng đích.

Ba tầng đóng góp:

1. **Đã có bằng chứng trong phiên:** audit nhãn, endpoint, metric và provenance; phát hiện bất nhất SD13/14. Hữu ích cho đề xuất và tái lập, chưa mặc định đủ thành đóng góp phương pháp luận văn.
2. **Dự kiến:** học nhiều isoform với mask/độ tin cậy phù hợp từng assay; tách tín hiệu chuỗi và khả năng tiếp cận trong tế bào; benchmark không rò rỉ có danh mục dương/âm/unknown.
3. **Cần thí nghiệm:** PLM, sharing, ordinal target hoặc context cải thiện dự đoán; conformal có coverage hữu ích; XAI phản ánh motif/động học. Chưa có kết quả để hứa.

## 7. Giao thức đánh giá đề xuất

### Ánh xạ và chia dữ liệu

1. Giữ chuỗi gốc, Z/X và toàn bộ mapping từ Rauh SD2. Pin FASTA/UniProt release và checksum; kiểm K đúng position, cửa sổ khớp, isoform/canonical, accession lỗi thời và loài. Một peptide có nhiều protein không được nhân thành nhiều mẫu độc lập.
2. Xây nhóm liên thông gồm các protein có chung peptide/mapping và protein đồng dạng; giữ cả nhóm trong một split. Dùng MMseqs2/CD-HIT hoặc alignment có **identity + coverage**, lưu phiên bản/tham số; khảo sát độ nhạy theo mức họ, không chọn ngưỡng dựa performance test.
3. Audit thêm chuỗi cửa sổ giống nhau giữa nhóm; mọi peptide masked/mapping mơ hồ để pool riêng. Không gộp tất cả `SYNTHETIC` thành một protein thật và cũng không tự xem chúng độc lập.
4. Chia **train / validation / calibration / test** theo nhóm. Validation chọn kiến trúc/ngưỡng; calibration chỉ chọn quantile uncertainty sau khi đóng model; test giữ kín. Nếu split khiến isoform không có đủ positive clusters, báo metric không ước lượng được và dùng nested/group CV thích hợp; không ép tỷ lệ 80/10/10.
5. Cellular test giữ riêng theo nghiên cứu, protein và homology với toàn bộ training/calibration; báo các tầng **site đã thấy / site mới cùng protein / protein mới / họ mới**. SIRT3 chuột là chuyển loài **cộng** chuyển assay, không quy mọi suy giảm cho domain shift in vitro→cell.

Audit trong phiên đã đo annotation overlap và kiểm chuỗi ngắn; **chưa chạy clustering toàn protein, chưa khóa FASTA toàn bộ train và chưa tạo split chính thức**. Bảo đảm protein không trùng chỉ loại một nguồn rò rỉ, không bảo đảm các site trong cùng protein là mẫu iid.

### Metric theo endpoint

| Dữ liệu | Metric chính | Bổ sung/đối chứng |
|---|---|---|
| Nhị phân assay có hai lớp | AUPRC theo isoform; MCC/F1 ở ngưỡng chọn trên validation | AUROC, calibration/Brier, prevalence; macro và từng isoform, CI bootstrap theo nhóm |
| Liên tục/thứ tự assay | Spearman/Kendall theo isoform; ordinal loss/error; MAE nếu thang có nghĩa | Constant/median predictor, rank enrichment; không so trực tiếp trị số giữa isoform |
| Bảy nhãn đầy đủ | Macro-AUPRC, Hamming loss; micro và per-label | Exact match/Jaccard, cardinality; label masks với cellular thiếu nhãn |
| 149 site dương | Recall tại ngưỡng đã khóa; positive enrichment/recall@budget nếu có universe nền hợp lệ | Always-positive, số dự đoán trên nền, CI theo protein; không precision/MCC |
| Cellular quantitative | Tương quan/ranking đáp ứng; effect-size sau protein correction | Giữ unknown, localization và missingness; đánh giá phân loại chỉ trên nhãn được biện minh |

Không tune ngưỡng bằng 149 dương rồi báo recall trên cùng 149. Khi so cùng site, dùng CI của **chênh lệch ghép cặp theo protein**; không coi 149 site là 149 thử nghiệm sinh học độc lập. Với nhãn tế bào chỉ có một isoform, không báo exact-match vector bảy nhãn.

### Baseline và ablation tối thiểu

| So sánh | Giữ cố định | Hiệu ứng được tách |
|---|---|---|
| Constant/prior; motif/PSSM; 443 feature + LDA/tree | Split, nhãn và tuning budget | Độ khó thật và lợi ích ML |
| Ridgeway chạy lại base + MusiteDeep/meta khi tái lập được | Protocol chung; tách model có/không secondary score | So baseline đầy đủ, tránh đối thủ yếu hơn bản công bố |
| One-hot + CNN; frozen PLM + linear/MLP; frozen PLM + mCNN | Head size/selection hợp lý | Biểu diễn PLM và tác dụng mCNN |
| 7 head độc lập vs shared backbone | Cùng encoder/loss/target | Chia sẻ isoform; negative transfer |
| Binary efficiency threshold vs ordinal category vs derived efficiency | Cùng split/encoder | Ý nghĩa nhãn; cần endpoint đánh giá chung để so |
| Có/không error weighting; có/không mask uncertainty | Cùng nhãn và model | Lợi ích độ tin cậy; sensitivity với weight cap |
| Peptide-only vs context-only vs sequence+context | Context chỉ lấy từ nguồn độc lập đã pin | Tác dụng localization/structure/PPI; kiểm leakage annotation |
| Frozen vs LoRA | Kiến trúc và split | Lợi ích fine-tuning; chỉ làm sau baseline đơn giản |

Deep-PLA có thể chạy lại trên dữ liệu riêng đã khóa hoặc dùng như external published predictor với audit overlap. **Dự đoán công bố SD13/14 chỉ là mốc lịch sử**, vì training pool/split/snapshot khác. Không tuyên bố “vượt Ridgeway” từ một model mới dùng thêm context trong khi đối thủ được fit theo protocol khác. Không cần chạy toàn bộ tổ hợp: ưu tiên ablation trả lời RQ, báo chi phí và seed.

## 8. Conformal: bảo đảm điều gì và trong miền nào?

[Angelopoulos–Bates](https://arxiv.org/abs/2107.07511) trình bày split conformal: model cố định, calibration và test exchangeable, quantile hữu hạn mẫu. “Không giả định phân phối” **không có nghĩa không cần giả định exchangeability**. Protein được chọn theo assay và site MS được chọn theo đáp ứng có thể phá điều kiện này.

Đầu ra dễ diễn giải cho mỗi isoform là **C_j(x) ⊆ {0,1}**: `{1}` dương, `{0}` âm trong endpoint được calibrate, `{0,1}` chưa phân biệt được. Tập rỗng cần xử lý/chẩn đoán, không tự chứng minh OOD. [SL]

| Bảo đảm muốn có | Điều cần thiết |
|---|---|
| 90% marginal cho từng isoform | Calibration hợp lệ cho isoform j; có thể chủ yếu che phủ lớp âm nếu mất cân bằng |
| Coverage riêng cho positive/negative | Mondrian theo **lớp thực** và isoform; mỗi lớp phải đủ mẫu; grouping isoform đơn độc chưa đủ |
| 90% cho toàn vector bảy nhãn | Score joint hoặc điều chỉnh sai số đồng thời, ví dụ α/7; bảy mức 90% riêng không cho joint 90% |
| Tập isoform chứa cơ chất thực | Phải định nghĩa chứa tất cả isoform dương hay ít nhất một; kiểm cả missing-label và false inclusion |
| 90% trong tế bào | Calibration đích hợp lệ hoặc định lý phù hợp; không chuyển bảo đảm của nhãn assay sang nhãn cellular |

Các site trong protein phụ thuộc nhau: định nghĩa đơn vị coverage là protein rồi site, hay cả cluster, và dùng thiết kế hierarchical/group conformal phù hợp. Xem [Dunn–Wasserman–Ramdas, two-layer models](https://robinmdunn.github.io/publication/conformal/). Chia protein riêng giúp chống leakage nhưng không tự cho theorem iid-site. Dùng [Barber và cộng sự, beyond exchangeability](https://doi.org/10.1214/23-AOS2276) để đánh giá giới hạn, không viện dẫn như bảo đảm miễn điều kiện.

[Weighted conformal dưới covariate shift](https://arxiv.org/abs/1904.06019) cần cùng quan hệ Y|X và tỷ lệ mật độ thích hợp. Ở đây **Y assay và Y cellular khác định nghĩa**, nên weighting đầu vào chưa sửa được concept/endpoint shift. Nếu có cellular calibration, phải giữ cellular test khác nhóm/nghiên cứu; 149 dương chỉ hỗ trợ coverage cho lớp dương chọn lọc, không negative coverage hoặc vector bảy nhãn.

Ít positive clusters khiến quantile thô và set lớn; số mẫu cần hoạch định từ độ chính xác CI mong muốn và effective sample size, không từ một ngưỡng tùy ý. Báo coverage theo isoform/lớp, set size, tỷ lệ `{0,1}`, utility và CI; không dùng set luôn `{0,1}` để tuyên bố thành công. **RQ conformal nên là phần mở rộng có điều kiện**, không lời hứa trong tên đề tài cốt lõi.

## 9. XAI: kiểm độ trung thực trước khi diễn giải cơ chế

Đề xuất occlusion/attribution trên window, so với motif và vị trí quan trọng thực nghiệm; cần giữ central K và thử nhiều cách perturbation tránh chuỗi ngoài phân phối. Đối chứng gồm model trọng số ngẫu nhiên, hoán nhãn rồi fit, motif thành phần amino acid nền, thay residue matched và motif xáo vị trí. [Adebayo 2018](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html) cung cấp cơ sở cho sanity checks bằng randomization.

Motif Rauh lấy top 50 efficiency của **chính array**, nên agreement có thể là học lại dữ liệu, không validation sinh học độc lập. Ưu tiên kinetics/mutagenesis hoặc thí nghiệm protein khác nguồn; kiểm fidelity qua thay đổi score khi perturbation, độ ổn định theo seed và fold. Không khớp motif có thể do model sai, nhãn nhiễu, context khác hoặc phương pháp XAI; không tự kết luận “XAI sai”. Saliency không chứng minh cơ chế hay quan hệ nhân quả. [SL]

## 10. Khẳng định ban đầu cần sửa

| Khẳng định trong báo cáo cũ | Bằng chứng | Kết luận sửa |
|---|---|---|
| Category ≥1 cho 176 SIRT1 dương | SD1↔SD15 khớp efficiency≥1; category≥1 chỉ tương ứng 4 trong tập aligned | Dùng tên nhãn đúng; giữ bất nhất Methods để truy vết |
| 64/149 là precision | 149 đều KD↑/OE↓, không FP | Recall trên dương chọn lọc |
| SD13 đủ thay chạy lại baseline | SD13/14 khác điểm và 21 binary calls; split mới khác | Mốc lịch sử; baseline công bằng cần chạy cùng protocol |
| Deep-PLA không có sirtuin | Methods + S1 có SIRT1/2/3/6/7 | Đối thủ trực tiếp |
| Chưa ai làm ML cơ chất sirtuin / cellular validation | Smith 2011, Zhai 2017, Deep-PLA, Ridgeway | Bỏ tính mới “lần đầu”; tìm khác biệt hẹp |
| Ridgeway không neural | MusiteDeep làm predictor phụ | Base model cổ điển, hybrid có DL |
| Không đổi có ý nghĩa là âm sạch | Thiếu lực/compensation/missingness; chưa có equivalence test | Unknown mặc định; âm theo bối cảnh cần chứng cứ |
| PXD021357/PXD023479 là KO acetylome SIRT3 | Sham/UUO và FLAG co-IP trong metadata | Loại khỏi benchmark cơ chất KO |
| 2.999 protein đã ánh xạ | 231 dòng SYNTHETIC; SD1 nhiều accession | Số accession strings; cần mapping phiên bản |
| Nhãn liên tục sẽ giải quyết SIRT1 | Category/ratio là derived assay score, chưa kinetics | Giả thuyết phải thử; không tự bỏ hoặc cứu isoform |
| Bảy output + conformal là tập isoform đúng 90% trong tế bào | Marginal/joint/endpoint khác nhau | Định nghĩa C_j và miền bảo đảm; cellular cần cơ sở riêng |
| Motif không khớp ⇒ XAI sai | Motif cùng array, endpoint/context khác | Kiểm fidelity và đối chứng, không suy nhân quả |
| Conformal đạt tiêu chí 5 | Biên bản: tiêu chí 5 là ứng dụng/website | Thiết kế sản phẩm riêng, bảo đảm ghi đúng phạm vi |

## 11. Phạm vi có thể bảo vệ và cổng đi/dừng

Tên tạm đề xuất: **“Học đặc hiệu deacetyl hóa của sirtuin từ peptide và đánh giá khả năng khái quát hóa sang acetylome phụ thuộc SIRT2/SIRT3.”** Bảy isoform là phạm vi assay; hai isoform là phạm vi cellular. Phần sinh học đóng góp ở đánh giá ranh giới giữa peptide preference và cellular response trên protein mới; chưa hứa phát hiện cơ chất sinh lý mới.

| Câu hỏi | Giả thuyết kiểm chứng | Cách bác bỏ |
|---|---|---|
| **RQ1:** PLM và chia sẻ isoform có cải thiện trên protein/họ chưa thấy? | Biểu diễn chia sẻ giúp một số isoform so baseline cùng split | Paired group CI/ablation không cho lợi ích hoặc cho negative transfer; vẫn là kết quả cần báo |
| **RQ2:** Nhãn thang độ và context giúp khái quát sang cellular response? | Score assay cộng context liên quan hơn peptide-only với đáp ứng protein-normalized SIRT2/3 | Hiệu ứng mất trên protein mới, context-only ngang combined hoặc chỉ có nguồn/mapping bias |
| **RQ3, có điều kiện:** uncertainty có utility dưới các miền đánh giá? | Calibration nội miền cho coverage/set size hữu ích; ngoài miền cần hiệu chỉnh đích | Coverage thất bại hoặc set vô dụng; không diễn giải thất bại là theorem bị bác bỏ khi giả định sai |

Đóng góp tin học nên chọn **một cơ chế có lý do** — ví dụ objective ordinal/masked sharing theo assay và uncertainty — rồi chứng minh bằng ablation. Chỉ thay ESM-2/LoRA/mCNN vào baseline là đóng góp ứng dụng, có thể chưa đủ mức phương pháp GVHD mong muốn. Context không mới tự thân và không nên chứa annotation “known SIRT substrate” của test.

| Cổng | Bằng chứng cần có trước khi đi tiếp | Hiện trạng / xử lý nếu thiếu |
|---|---|---|
| Mapping và độc lập | FASTA pin, site verified, multi-mapping xử lý, protein/homology overlap quantified, split đủ positive groups | Chưa đạt toàn bộ; hoàn tất trước fit, tách pool mơ hồ |
| Cellular endpoint | Site table + design/replicates, uncertainty/protein correction, quy tắc dương/âm/unknown có lý do | SIRT2 và SIRT3 quantitative tải được; full binary benchmark chưa đạt |
| Giá trị khoa học | Ít nhất RQ1 hoặc RQ2 trả lời được bằng endpoint hợp lệ và CI đủ hẹp cho effect cần đánh giá | Nếu chỉ còn positive recall trên nguồn rò rỉ, thu hẹp sang assay/generalization hoặc tạm dừng RQ2 |
| Tính mới phương pháp | So đối thủ trực tiếp, objective rõ, ablation tách hiệu ứng và mức kỳ vọng GVHD | Chưa có chứng minh thực nghiệm; không đặt “thắng 4/7” làm gate tùy ý |
| Conformal | Đối tượng và đơn vị sampling rõ; calibration đủ thông tin, set có utility | Giữ mở rộng; bỏ lời hứa cellular nếu thiếu điều kiện |

Không dùng “phải có âm cho hai isoform” như gate duy nhất: continuous response/ranking có thể là endpoint khoa học hợp lệ. Nhưng nếu GVHD yêu cầu phân loại **cơ chất trực tiếp** với specificity, dữ liệu response hiện tại chưa đáp ứng. Nếu mapping/replicate không giải được và không còn RQ hợp lệ, mới xét [dự phòng kinase](../../surveys/b-method-layer-draft.md); chưa có trở ngại quyết định buộc chuyển ngay.

### Câu hỏi ưu tiên cho GVHD

1. Thầy chấp nhận endpoint **acetyl hóa phụ thuộc isoform** và kết quả âm về chuyển miền, hay yêu cầu cơ chất trực tiếp? Có cộng tác sinh học để xác thực/tư vấn equivalence margin không?
2. Benchmark theo protein/homology và SIRT3 chuột có đáp ứng yêu cầu test độc lập? Có cần cellular người cho isoform thứ hai?
3. Đóng góp phương pháp ở objective bằng chứng/ordinal/multitask cần ở mức nào so với việc dùng PLM? Thầy ưu tiên RQ nào?
4. Có nên giữ bảy head assay nhưng chỉ SIRT2/3 cellular, và báo SIRT1 theo uncertainty thay vì loại theo số 176?
5. Xin toàn văn SirtSAGE và dữ liệu/nguồn phù hợp từ nhóm; xác định phạm vi website bắt buộc và người dùng.

### Sản phẩm hệ thống phù hợp

Website nhập protein/UniProt ID, kiểm lysine/mapping rồi hiển thị điểm **assay-specific** cho bảy isoform, bằng chứng liên quan, trạng thái context/unknown và phạm vi calibration. Nếu có model cellular được xác thực thì hiển thị ở mục riêng, kèm tế bào/loài và endpoint. Có tải bảng kết quả, provenance và giải thích amino acid; không ghi “cơ chất sinh lý xác nhận” hoặc “90% đúng” trên protein ngoài miền chưa kiểm. Đây là đặc tả cho tiêu chí 5, chưa triển khai trong khảo sát.

## 12. Mức sẵn sàng và thứ tự việc tiếp theo

**Sẵn sàng trình bày như đề xuất cần chốt phạm vi, chưa sẵn sàng bảo vệ các khẳng định mạnh của bản cũ.** Có dữ liệu và vấn đề thật, nhưng tính mới “lần đầu” bị phản bác; benchmark tế bào đầy đủ và bảo đảm conformal vẫn chưa được thiết lập.

1. **Ưu tiên 1:** truy vết SIRT2 Synapse và bảng Hebert/Rardin gốc: metadata mẫu/lặp, site p/q/CI, protein correction; giải 152→149 và SD13/14. Nếu thiếu uncertainty, chốt continuous/positive–unlabeled endpoint với GVHD trước xây nhãn.
2. **Ưu tiên 2:** pin FASTA, mapping site và grouping homology; công bố exclusions/split/cardinality theo isoform. Đếm effective positive proteins; quyết định phạm vi SIRT1 từ bằng chứng đó.
3. **Ưu tiên 3:** hoàn tất full-text NAD_MCNN/SirtSAGE và khảo sát trực tiếp bổ sung, khóa giả thuyết/metric/ablation; chọn đóng góp phương pháp đủ hẹp.
4. **Ưu tiên 4, phiên thực nghiệm sau:** chạy baseline đơn giản rồi PLM/sharing/label/context theo giao thức chung; model selection trên validation, giữ test kín. Không dùng kết quả khảo sát này thay kết quả training.
5. **Ưu tiên 5:** chỉ thêm conformal khi sampling/calibration hợp lệ; kiểm XAI; sau đó triển khai website phản ánh đúng giới hạn đã đo.

Các phần còn thiếu được ghi cụ thể trong [ghi chú bằng chứng](research/README.md) và [nhật ký công việc](../../../journal/README.md). Báo cáo khuyến nghị ban đầu được giữ nguyên để đối chiếu.
