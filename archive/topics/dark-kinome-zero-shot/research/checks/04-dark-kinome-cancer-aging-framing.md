# Khung động lực sinh - y học cho đề tài dark kinome / kinase–phosphosite: khung "cancer" và khung "aging" mạnh đến đâu

> Ghi chú khảo sát, 10/10/2026. Nhãn: **[SOURCE]** = số/claim có nguồn trực tiếp · **[ANALYSIS]** = suy luận của người khảo sát · **[UNVERIFIED]** = chưa kiểm chứng được.
> Mục tiêu: để sinh viên tự đánh giá có thể trình bày đề tài zero-shot kinase–phosphosite link prediction (DARKIN) như một đề tài **cancer** hay **aging** một cách trung thực, không overclaim trước GVHD.

## Kết luận ngắn gọn trước khi vào chi tiết [ANALYSIS]

- Khung **"dark kinome / understudied kinome"** là khung mạnh nhất và chắc chắn nhất: có chương trình NIH (IDG) đứng sau, có con số cụ thể, có cơ sở dữ liệu riêng (Pharos, Dark Kinase Knowledgebase), có chuỗi bài trên *Nature Reviews Drug Discovery*. Đây nên là khung chính.
- Khung **"cancer"** là **thật và citable ở mức pan-cancer bioinformatics**, không phải khung generic: có bài *Cell Reports Medicine* 2020 (Clinical Kinase Index) và *Cancers* 2021 (pan-cancer kinome methylation) định lượng rõ "understudied kinase nào tiên lượng xấu ở ung thư nào". **Tuy nhiên**: đó là liên hệ **mức gene/protein (kinase nào quan trọng trong ung thư)**, chứ **không phải** liên hệ mức **phosphosite** (site nào bị kinase nào phosphoryl hóa trong ung thư). Đề tài dự đoán cặp kinase–site chỉ là **công cụ nền (enabling tool)** cho các nghiên cứu ung thư, không phải nghiên cứu ung thư trực tiếp. Phải nói đúng như vậy.
- Khung **"aging"** **yếu hơn hẳn**. Liên hệ chung (mTOR, AMPK, IGF-1 đều là kinase và đều nằm trong hallmark "deregulated nutrient sensing") là đúng nhưng generic tới mức gần như vô nghĩa về mặt tính mới.
- Cầu nối **sirtuin ↔ kinase** (nối với SirtSAGE 2026 của GVHD) là **thật, có citable primary literature**, nhưng **bằng chứng thưa và phần lớn là từ 2007–2018**. Chi tiết ở câu hỏi 3 — đọc kỹ phần đó trước khi dùng trong slide.

---

## 1. Vấn đề "dark kinome / understudied kinome" được đóng khung thế nào, ai khởi xướng, số liệu đầu bài là gì

### Takeaway
"Dark kinome" là một khung do **NIH Illuminating the Druggable Genome (IDG)** chính thức hóa, với một danh sách kinase cụ thể (162 kinase trong bản 2019 của Kinase DRGC), hệ thống phân loại Tclin/Tchem/Tbio/Tdark trên Pharos, và một cơ sở dữ liệu riêng (Dark Kinase Knowledgebase, darkkinome.org). Con số thường trích: ~634 kinase người (tính cả pseudokinase), ~24% understudied, và khoảng **1/3 kinome gần như chưa được nghiên cứu sâu**.

### Cited Findings
- Dark Kinase Knowledgebase (DKK) bao phủ **162 kinase** mà NIH xác định là "poorly studied hoặc 'dark' kinases", được chọn qua chương trình IDG — Berginski ME, Moret N, Liu C, Goldfarb D, Sorger PK, Gomez SM, "The Dark Kinase Knowledgebase: an online compendium of knowledge and experimental results of understudied kinases", *Nucleic Acids Res* 2021;49(D1):D529–D535 — [PMC7778917](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7778917/), [DOI 10.1093/nar/gkaa853](https://doi.org/10.1093/nar/gkaa853)
- Cùng bài: kinome người có "well over 500 members"; **"nearly one-third of kinases is largely unknown"** (abstract), dẫn Fedorov et al. (2010) — [PMC7778917](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7778917/)
- DKK **không** chứa dữ liệu kinase–substrate / phosphoproteomics; nội dung proteomics của nó giới hạn ở peptide PRM để định lượng và dữ liệu biểu hiện (GTEx, Human Proteome Map), cộng với mạng tương tác protein từ AP-MS và miniTurbo, reagent NanoBRET, tool compound cho ~30 kinase — [PMC7778917](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7778917/) [SOURCE]
- Essegian D, Khurana R, Stathias V, Schürer SC, "The Clinical Kinase Index: A Method to Prioritize Understudied Kinases as Drug Targets for the Treatment of Cancer", *Cell Reports Medicine* 2020: **"The human genome encodes about 634 kinases (pseudokinases included)"**, trong đó **151/634 (23,8%, làm tròn 24%) được xếp loại understudied** — [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504), [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2020.02.14.943886.full.pdf)
- Độ lệch chú ý nghiên cứu tính theo số bài báo: **EGFR ~90.000 bài, SRC ~30.000 bài, STK35 15 bài, HIPK4 9 bài** — trang giới thiệu chuỗi "Kinase Target Watch" của ĐH Eastern Finland (Christopher Asquith), chuỗi gồm 13 bài highlight trên *Nature Reviews Drug Discovery* — [UEF](https://www.uef.fi/en/article/kinase-target-watch-article-series-highlights-therapeutic-opportunities-within-the-understudied)
- Understudied kinase tập trung ở các nhóm **CMGC, CAMK và "other"**; nhóm tyrosine kinase (TK) đã được khai thác rất nhiều — tổng hợp từ kết quả tìm kiếm trích Pharos (xem Gaps về nguồn gốc chính xác)
- Johnson JL et al., "An atlas of substrate specificities for the human serine/threonine kinome", *Nature* 2023;613(7945):759–766: bộ profiling bao gồm **83 understudied "dark" kinases** — [PMC9876800](https://pmc.ncbi.nlm.nih.gov/articles/PMC9876800/), [DOI 10.1038/s41586-022-05575-3](https://doi.org/10.1038/s41586-022-05575-3)

### Inferences
- [ANALYSIS] Khung "dark kinome" có đủ ba thứ mà một slide "tính cấp thiết" cần: (1) một cơ quan tài trợ công khai đặt tên vấn đề (NIH IDG), (2) một danh sách mục tiêu cụ thể (162 kinase IDG, hoặc 151 understudied theo Pharos), (3) số liệu độ lệch chú ý cực kỳ ấn tượng và dễ hiểu (90.000 bài vs 9 bài). Đây là khung an toàn nhất về mặt "không bị bắt lỗi overclaim".
- [ANALYSIS] Vì DKK **không** có dữ liệu kinase–substrate, nên một đề tài sinh ra dự đoán kinase–phosphosite cho dark kinase lấp đúng một khoảng trống mà chính resource của IDG để trống. Đây là lập luận tốt, nhưng phải nói ở mức "bổ sung một loại dữ liệu mà DKK chưa có", không phải "đầu tiên".

### Gaps
- Số lượng dark kinase **không nhất quán giữa các nguồn**: 162 (DKK/Kinase DRGC, bản 2019), 151 (Pharos, theo Essegian 2020), và một trang SGC-UNC nói **134** IDG dark kinases. Tổng số kinome cũng khác nhau: ~535 (Manning-style, protein kinase thật) vs 634 (có pseudokinase). **Phải chọn một nguồn và trích nguyên văn kèm năm**, đừng trộn. [SOURCE conflict]
- Chưa kiểm được con số Pharos **hiện tại** (10/2026) trên pharos.nih.gov — số 151/634 là bản 2020. [UNVERIFIED cho hiện tại]
- Không tìm được con số định lượng về **phân bổ kinh phí NIH** theo kinase (kiểu "x% grant đổ vào y kinase"). DKK không đưa số này. Nếu cần số về funding, phải tìm thêm (Oprea et al. 2018 *Nat Rev Drug Discov* "Unexplored therapeutic opportunities in the human genome" là ứng viên, nhưng **tôi chưa đọc được bản full và chưa xác minh con số nào trong đó** — [UNVERIFIED]).

---

## 2. Liên hệ với CANCER mạnh đến đâu

### Takeaway
Liên hệ cancer là **thật và định lượng được**, không generic: có ít nhất hai bài pan-cancer chỉ rõ tên những understudied/dark kinase mà biểu hiện cao tương quan với sống còn kém, và một bài *Cell Reports Medicine* xây hẳn chỉ số ưu tiên mục tiêu ung thư cho understudied kinase. **Nhưng** toàn bộ bằng chứng này ở mức **gene/protein**, không ở mức **phosphosite**; và là tương quan TCGA, tác giả tự nói cần thí nghiệm xác thực thêm.

### Cited Findings
- Essegian et al. 2020 (*Cell Reports Medicine*): xây **Clinical Kinase Index** từ differential gene expression, tham số bệnh học, overall survival và mutational hotspot trên **17 loại ung thư solid của TCGA**; highlight nói thẳng **"Expression of understudied kinases in tumors is prognostic of poor outcomes"** — [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504)
- Cùng bài, các con số cụ thể: biểu hiện tăng của **15 Tdark kinase** tương quan với overall survival giảm ở nhiều loại ung thư; **ADCK5** là marker tiên lượng xấu ở KIRC, LIHC, UCEC, UVM; ở BRCA, biểu hiện cao của **ALPK3, CSNK1A1L, CSNK2A3, NRK, POMK, PSKH1** liên quan OS giảm; **PKMYT1** (Tchem) là understudied kinase điểm cao nhất, overexpressed ở 17/20 ung thư, và là biomarker tiên lượng/dự báo ở KIRC và KIRP; **TRIB3** tương quan di căn ở 5 cohort; **DYRK1B** đột biến ở 4,3% mẫu UCEC với OS xấu hơn (p < 0,05); **CAMKV** overexpressed ở 14 cohort — [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504)
- Southekal S, Mishra NK, Guda C, "Pan-Cancer Analysis of Human Kinome Gene Expression and Promoter DNA Methylation Identifies Dark Kinase Biomarkers in Multiple Cancers", *Cancers* 2021;13(6):1189: phân tích 32 loại ung thư TCGA, xác định các dark kinase **PKMYT1, PNCK, BRSK2, ERN2, STK31, STK32A, MAPK4** có vai trò ý nghĩa trong sống còn bệnh nhân — [DOI 10.3390/cancers13061189](https://doi.org/10.3390/cancers13061189) (PMID 33801837, PMC8001681)
- Có hẳn một dòng nghiên cứu "dark kinase family review + survival correlation" dành riêng cho ung thư, nhóm Burow/Drewry (Tulane + UNC Lineberger): NEK family (*Cancers* 2023, [DOI 10.3390/cancers15072067](https://doi.org/10.3390/cancers15072067)), MAP3K family (*Front Biosci* 2022, [DOI 10.31083/j.fbl2705167](https://doi.org/10.31083/j.fbl2705167)), MAP3K19 (*Front Biosci* 2022, [DOI 10.31083/j.fbl2706196](https://doi.org/10.31083/j.fbl2706196)) — tất cả đều dùng keyword "dark kinome", "understudied kinase", "Illuminating the Druggable Genome"
- Ví dụ dark kinase thành target thực nghiệm trong ung thư: kinome profiling ở **uveal melanoma** xác định **MARK3** và **STK10** (thuộc "dark kinome") là target tiềm năng; knockdown giảm tăng trưởng tế bào — Baqai U et al., *J Biol Chem* 2023;299(12):105418, [DOI 10.1016/j.jbc.2023.105418](https://doi.org/10.1016/j.jbc.2023.105418)
- Chất ức chế chọn lọc cho dark kinase gắn trực tiếp với ung thư: **HIPK4** được mô tả là "understudied member of the dark kinome", knockout gợi ý liên quan **cutaneous squamous cell carcinoma**; probe AZ137 (IC50 11 nM) mới ra 2026 — Zerva A et al., *J Med Chem* 2026;69(17):20616–20638, [DOI 10.1021/acs.jmedchem.6c01320](https://doi.org/10.1021/acs.jmedchem.6c01320). **CDK16/PCTAIRE**: dysregulation liên quan breast, prostate, cervical cancer — Amrhein JA et al., *Int J Mol Sci* 2022;23(23):14834, [DOI 10.3390/ijms232314834](https://doi.org/10.3390/ijms232314834)
- DKK có sẵn một tool **"Clinical Kinase Index"** cho "kinase targets in cancer" và heatmap TCGA (đột biến, CNV, mRNA) theo loại ung thư — [PMC7778917](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7778917/)

### Inferences
- [ANALYSIS] Câu an toàn và đúng để nói với GVHD: *"Understudied kinase đã được chứng minh có giá trị tiên lượng ở nhiều loại ung thư (Essegian 2020, Southekal 2021), nhưng để chuyển từ tương quan biểu hiện sang hiểu cơ chế thì cần biết chúng phosphoryl hóa cái gì — và đó chính là chỗ gần như trắng."* Đây là chuỗi lập luận hợp lệ, có nguồn ở cả hai đầu.
- [ANALYSIS] Câu **không** được nói: "đề tài này giúp điều trị ung thư" hoặc "dự đoán kinase–phosphosite là đề tài ung thư". Không có bằng chứng nào nối trực tiếp dự đoán cặp kinase–site với một kết cục lâm sàng ung thư.
- [ANALYSIS] Lưu ý tự phản biện: Essegian et al. tự nói kết quả là **tương quan TCGA** và "target validation requires further experiments". Nếu GVHD hỏi "bằng chứng mạnh cỡ nào", trả lời trung thực là: mức tương quan omics pan-cancer + một số case thực nghiệm lẻ (MARK3/STK10 ở uveal melanoma, HIPK4 ở cSCC), chưa có dark kinase nào thành thuốc ung thư được phê duyệt.

### Gaps
- **Không kiểm chứng được bằng chứng DepMap/cancer dependency map cụ thể về understudied kinase.** Essegian et al. chỉ *gợi ý* DepMap "may serve to be an important resource to help prioritize" — tức là forward-looking, không phải một kết quả DepMap đã công bố. Nếu cần số liệu DepMap (ví dụ "x dark kinase là selective dependency ở y dòng tế bào"), **phải tìm riêng; tôi không có số nào** — [UNVERIFIED]
- Không tìm được tỉ lệ cụ thể "bao nhiêu % dark kinase bị đột biến trong ung thư" trên toàn bộ danh sách IDG. Các bài trên chỉ nêu từng kinase.
- Con số FDA-approved target trong Essegian et al. **tự mâu thuẫn trong bài** (xem câu hỏi 4).
- Chưa đọc được LINCS-specific evidence về dark kinase trong ung thư. [UNVERIFIED]

---

## 3. Liên hệ với AGING, và đặc biệt cầu nối kinase ↔ sirtuin (điểm neo của GVHD)

### Takeaway
Liên hệ aging ở mức "kinase signalling là một phần của hallmarks of aging" là **đúng nhưng generic** (mTOR, AMPK, insulin/IGF-1 đều là kinase). Cầu nối **sirtuin là substrate của kinase** thì **có thật và có primary literature định danh được kinase + residue cụ thể**, nhưng bằng chứng **thưa, cũ (phần lớn 2007–2011), và phần lớn phosphosite trên sirtuin vẫn chưa biết kinase nào** — chính điều đó mới là lập luận hay, chứ không phải độ dày của bằng chứng.

### Cited Findings — các cặp kinase → sirtuin + residue cụ thể

Nguồn tổng hợp chính: Flick F, Lüscher B, "Regulation of sirtuin function by posttranslational modifications", *Front Pharmacol* 2012;3:29 — [PMC3289391](https://pmc.ncbi.nlm.nih.gov/articles/PMC3289391), [DOI 10.3389/fphar.2012.00029](https://doi.org/10.3389/fphar.2012.00029). Các primary reference ghi trong bảng của review đó:

| Sirtuin | Residue | Kinase | Hệ quả chức năng | Primary ref (theo review) |
|---|---|---|---|---|
| SIRT1 | Ser27, Ser47, Thr530 | **JNK** | Tăng khu trú nhân và hoạt tính trên histone H3 (không trên p53) | Nasrin et al. 2009 |
| SIRT1 | Ser47 | **mTOR** | **Ức chế** hoạt tính deacetylase | Back et al. 2011 |
| SIRT1 | Thr530, Ser540 | **CycB/CDK1** | Cần cho tiến triển chu kỳ tế bào bình thường; thể đột biến không cứu được tế bào Sirt1-knockout | Sasaki et al. 2008 |
| SIRT1 (murine) | Ser154, Ser649, Ser651, Ser683 | **CK2** | Được đề xuất là làm tăng hoạt tính xúc tác và tương tác với p53 | Kang et al. 2009 |
| SIRT1 (human) | Ser659, Ser661 | **CK2** | Có thể điều biến motif ESA và gắn DBC1 — **chưa kiểm chứng đầy đủ** | Zschoernig & Mahlknecht 2009 |
| SIRT2 | Ser368 (Ser331 ở variant 2) | **CycB/CDK1, CycE/CDK2, CycA/CDK2, CycD3/CDK4, p35/CDK5** | Giảm deacetylation histone và α-tubulin; đối kháng tác động của SIRT2 lên neurite outgrowth | North & Verdin 2007b; Pandithage et al. 2008 |

Ngoài review 2012, hai primary paper mới hơn tôi xác minh trực tiếp qua PubMed:

- **JAK1 phosphoryl hóa SIRT1 tại Tyr280 và Tyr301** — hai residue bảo tồn cao, **nằm trong chính catalytic deacetylase domain** của SIRT1. IL-6 làm tăng tương tác JAK1–SIRT1 và mức phosphoryl hóa. Phosphoryl hóa này **không** đổi hoạt tính xúc tác, nhưng **cần thiết** cho SIRT1 tương tác với STAT3, qua đó SIRT1 ức chế acetylation và hoạt tính phiên mã của STAT3 — Wang W et al., "JAK1-mediated Sirt1 phosphorylation functions as a negative feedback of the JAK1-STAT3 pathway", *J Biol Chem* 2018;293(28):11067–11075, [DOI 10.1074/jbc.RA117.001387](https://doi.org/10.1074/jbc.RA117.001387) (PMID 29789426). **Đây là bài tốt nhất cho cầu nối: tyrosine kinase, residue chính xác, trong catalytic domain, và có trục ung thư (IL-6/STAT3, bảo vệ tế bào ung thư khỏi apoptosis do thuốc).**
- **AMPK-dependent phosphoryl hóa SIRT2 tại Thr101** (SIRT2 là AKT binding partner cần cho hoạt hóa AKT bởi insulin) — Ramakrishnan G et al., "Sirt2 deacetylase is a novel AKT binding partner critical for AKT activation by insulin", *J Biol Chem* 2014;289(9):6054–6066, [DOI 10.1074/jbc.M113.537266](https://doi.org/10.1074/jbc.M113.537266) (PMID 24446434)

### Cited Findings — phần "chưa biết kinase nào" (lập luận mạnh nhất cho đề tài)
- Flick & Lüscher 2012 liệt kê các phosphosite **không gán được kinase và không rõ chức năng**: SIRT1 Ser14, Ser26, Ser172, Ser173, Ser719, Ser747 (Sasaki et al. 2008); SIRT2 Ser372/Ser335 (Nahhas et al. 2007); **SIRT3**: 6 phosphoserine ở vị trí 101, 103, 105, 114, 117, 118 (Olsen et al. 2010) — không biết kinase, chưa test chức năng; **SIRT4**: Ser255, Ser261, Ser262 (Yu et al. 2007) — không biết kinase; **SIRT5**: review không nêu phosphosite nào; **SIRT6**: Tyr294 và Ser303 (Dephoure et al. 2008) — không biết kinase, không rõ chức năng; **SIRT7**: chỉ có bằng chứng gián tiếp về phosphoryl hóa bởi một CDK complex trong mitosis (Grob et al. 2009), **chưa map được site nào** — [PMC3289391](https://pmc.ncbi.nlm.nih.gov/articles/PMC3289391)
- Cùng review: MS xác định 13 phosphosite trên SIRT1 (Sasaki et al. 2008), trong đó chỉ khoảng **4 site (Ser27, Ser47, Thr530, Ser540) có kinase đã biết** — [PMC3289391](https://pmc.ncbi.nlm.nih.gov/articles/PMC3289391). ⚠️ Lưu ý: bảng trong review và con số 13 không khớp hoàn toàn với nhau (bản WebFetch đọc được chỉ liệt kê ~10 site của Sasaki) — nếu dùng con số này, **phải đọc bản full và đếm lại**.
- Review đó cũng nói phần N- và C-terminal extension của sirtuin là đích chính của PTM, còn **catalytic core thì ít được nghiên cứu hơn nhiều** — [PMC3289391](https://pmc.ncbi.nlm.nih.gov/articles/PMC3289391)
- Zhao & Zhou 2020 (*Genome Instability & Disease*, review về nuclear sirtuins SIRT1/6/7): "little is known about how [sirtuins] themselves are regulated, with even less information on their post-translational modifications" — [bản tóm tắt](https://med.szu.edu.cn/kxyj/gjqk/latestarticles/content_2717) [SOURCE, nhưng chỉ đọc được snippet]

### Cited Findings — liên hệ aging ở mức hallmark (generic)
- Hallmark "deregulated nutrient sensing" của aging gồm 4 đường chính: **insulin/IGF-1 signalling, mTOR, sirtuins, AMPK** — trong đó 3/4 là kinase hoặc trục kinase. Nguồn tôi tìm được chỉ là trang phổ thông (lifespan.io) trích lại framework López-Otín; **tôi không đọc được bài López-Otín gốc** — [lifespan.io](https://lifespan.io/topic/deregulated-nutrient-sensing) [SOURCE yếu]
- Khả năng hoạt hóa AMPK **giảm theo tuổi**, làm suy yếu duy trì homeostasis tế bào và thúc đẩy quá trình lão hóa; AMPK signalling điều phối healthspan/lifespan qua FoxO, mTOR/ULK1, CRCT-1/CREB và **SIRT1** — Salminen A, Kaarniranta K, Kauppinen A, "Age-related changes in AMPK activation: Role for AMPK phosphatases and inhibitory phosphorylation by upstream signaling pathways", *Ageing Res Rev* 2016;28:15–26, [DOI 10.1016/j.arr.2016.04.003](https://doi.org/10.1016/j.arr.2016.04.003) (PMID 27060201). **Đây là nguồn aging tốt nhất tôi tìm được: nó nối trực tiếp aging ↔ phosphoryl hóa (cả activating lẫn inhibitory, kèm residue Thr172 của AMPKα) ↔ SIRT1.**
- SIRT1 và AMPK cùng chi phối tim trưởng thành khỏe mạnh (thúc đẩy β-oxidation), đối lập với trục mTOR/HIF-1α của tim thai — Packer M, *Eur J Heart Fail* 2023;25(8):1199–1212, [DOI 10.1002/ejhf.2972](https://doi.org/10.1002/ejhf.2972). Bài này cũng nêu điểm hữu ích về mặt framing: phosphoryl hóa cũng tác động lên Ser/Thr như O-GlcNAcylation, nhưng **"phosphorylation is regulated by hundreds of specific kinases and phosphatases"**, còn O-GlcNAcylation chỉ có 2 enzyme — tức độ phức tạp tổ hợp của bài toán gán kinase là nội tại.

### Inferences
- [ANALYSIS] **Cầu nối sirtuin–kinase là thật và dùng được, nhưng phải phát biểu đúng chiều.** Phát biểu đúng: *"Sirtuin không chỉ là enzyme xóa acetyl — bản thân chúng là substrate của kinase. SIRT1 có ít nhất 5 kinase đã được định danh (JNK, mTOR, CDK1, CK2, JAK1) phosphoryl hóa ở các residue cụ thể, và JAK1 phosphoryl hóa ngay trong catalytic domain (Y280/Y301). Nhưng với SIRT3–SIRT7, phần lớn phosphosite phát hiện bằng MS vẫn chưa biết kinase nào. Mô hình dự đoán kinase–phosphosite đúng là loại công cụ sinh giả thuyết cho khoảng trống đó."* Phát biểu **sai/overclaim**: "đề tài này nghiên cứu sirtuin" hoặc "dự đoán kinase của sirtuin là mục tiêu chính".
- [ANALYSIS] Điểm cộng chiến lược: cầu nối này cho phép đề tài **đứng cạnh** SirtSAGE 2026 mà không cạnh tranh với nó. SirtSAGE phân loại họ sirtuin từ sequence; đề tài này dự đoán ai phosphoryl hóa sirtuin — cùng một đối tượng protein, hai bài toán khác nhau, cùng một paradigm (sequence-based + deep learning). Nếu muốn, có thể làm một **case study nhỏ**: chạy mô hình trên các phosphosite đã biết của SIRT1–SIRT7 và xem nó có recover được JNK/CDK1/CK2/JAK1 không, rồi sinh giả thuyết cho các site chưa biết kinase (SIRT3 S101–S118, SIRT4 S255/S261/S262, SIRT6 Y294/S303). Đó là một mục đánh giá **nhỏ, rẻ, và cực kỳ khớp với GVHD**.
- [ANALYSIS] Cảnh báo trung thực: nếu GVHD muốn một đề tài **về aging**, thì đề tài kinase–phosphosite **không phải** đề tài aging. Khung aging ở đây chỉ đủ làm **một đoạn motivation và một case study**, không đủ làm trục chính. Đừng bán nó như trục chính.

### Gaps
- **Chưa đọc được primary paper nào trong các reference của Flick & Lüscher 2012** (Nasrin 2009, Back 2011, Sasaki 2008, Kang 2009, North & Verdin 2007, Pandithage 2008). Các cặp kinase–residue ở bảng trên là **trích qua review**, không phải kiểm chứng trực tiếp. Trước khi đưa vào slide/đề cương, nên mở ít nhất Sasaki 2008 và Nasrin 2009 để xác nhận residue. [cần verify]
- Review Flick & Lüscher là **2012** — có 14 năm bằng chứng mới chưa được quét. Hai bài tôi tìm thêm (JAK1→SIRT1 2018, AMPK→SIRT2 2014) gợi ý còn nhiều nữa. **Nên chạy một vòng tìm kiếm riêng cho 2012–2026** ("SIRT6 phosphorylation kinase", "SIRT3 phosphorylation site kinase", v.v.) trước khi tuyên bố "bằng chứng thưa". [chưa làm, hết budget]
- Không tìm được review **nào** tổng hợp đầy đủ kinase–site cho cả SIRT1→SIRT7 ở thời điểm hiện tại. Đây có thể là một quan sát hữu ích (khoảng trống thật) nhưng cũng có thể do tôi tìm chưa tới. [UNVERIFIED]
- **Không đọc được López-Otín et al. "Hallmarks of Aging" gốc** (2013 hoặc bản 2023 "Hallmarks of aging: An expanding universe"). Nguồn duy nhất cho danh sách 4 đường nutrient sensing là trang phổ thông. Nếu dùng trong đề cương, **phải trích bài gốc**, không trích lifespan.io.
- Không tìm được bằng chứng rằng bất kỳ **dark/understudied kinase** nào (danh sách IDG) có liên hệ với aging hay với sirtuin. Nghĩa là: aging link có cho kinase **nói chung**, nhưng **không** có cho dark kinome cụ thể. [ANALYSIS + gap] Đây là điểm yếu quan trọng phải nói thẳng.

---

## 4. Bao nhiêu kinase là đích thuốc đã phê duyệt, và độ tập trung nỗ lực được định lượng thế nào

### Takeaway
Con số hay dùng nhất: **49/634 kinase (8%)** là primary target của thuốc phân tử nhỏ chống ung thư đã được FDA phê duyệt, ~70% trong số đó thuộc nhóm tyrosine kinase. Tổng số thuốc ức chế kinase đã phê duyệt (mọi chỉ định) là **"over 100"**.

### Cited Findings
- **49 kinase (8%)** là primary target của thuốc phân tử nhỏ chống ung thư FDA-approved; ~70% trong số đó thuộc nhóm tyrosine kinase — Essegian et al. 2020, [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504)
- Cùng bài, các số đo độ tập trung nỗ lực rất dùng được cho slide: **chỉ 3 trong 39 thuốc được phê duyệt năm 2018 nhắm vào target kinase mới**; **không quá 20 IDG target chuyển từ Tbio sang Tchem mỗi năm** (trên toàn bộ các lớp target); **không có thuốc phân tử nhỏ nào có một kinase nhóm CaMK, CK1 hay AGC làm primary target**; tác giả kêu gọi dỡ bỏ "biases against understudied targets... particularly in grant funding" — [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504)
- **"over 100 clinically approved drugs"** là kinase inhibitor (mọi chỉ định) — [UEF Kinase Target Watch](https://www.uef.fi/en/article/kinase-target-watch-article-series-highlights-therapeutic-opportunities-within-the-understudied)
- Kinase là "one of the most successfully targeted protein families in drug development" — [UEF](https://www.uef.fi/en/article/kinase-target-watch-article-series-highlights-therapeutic-opportunities-within-the-understudied)
- Độ tập trung chú ý nghiên cứu, dạng số bài báo: EGFR ~90.000 / SRC ~30.000 / STK35 15 / HIPK4 9 — [UEF](https://www.uef.fi/en/article/kinase-target-watch-article-series-highlights-therapeutic-opportunities-within-the-understudied)

### Inferences
- [ANALYSIS] Cặp số mạnh nhất cho một slide "vì sao việc này quan trọng": **8% kinome là đích thuốc ung thư đã phê duyệt** + **90.000 bài về EGFR vs 9 bài về HIPK4**. Hai con số này, cùng nhau, nói trọn câu chuyện mà không cần overclaim gì cả.

### Gaps
- ⚠️ **Essegian et al. tự mâu thuẫn**: phần introduction nói 49 kinase (8%), còn phần summary nói "over 48 additional" approved inhibitors. Bản WebFetch ghi rõ "the counts are not fully consistent". **Khi trích, trích số 49/8% kèm "theo phần mở đầu của Essegian et al. 2020"**, đừng trích phần summary. [SOURCE conflict]
- Không xác minh được số kinase mà "over 100 approved drugs" của UEF nhắm tới, và UEF là trang tin đại học (secondary source). Nếu cần số chắc hơn, nên trích Roskoski (bản cập nhật hằng năm về FDA-approved protein kinase inhibitors) — **tôi chưa đọc bản nào của Roskoski, không có số** [UNVERIFIED].
- Không có số về tổng chi phí R&D hay phân bổ kinh phí theo kinase. [UNVERIFIED]

---

## 5. Phosphoproteomics / kinase activity inference trong nghiên cứu ung thư: có tạo ra nhu cầu thật cho thư viện kinase–substrate tốt hơn không?

### Takeaway
**Có, và đây là lập luận động lực mạnh nhất, định lượng nhất, và sát đề tài nhất.** Con số đinh: **chỉ dưới 4%** phosphosite Ser/Thr của người có kinase thượng nguồn đã biết (Johnson et al., *Nature* 2023). Và nghiên cứu benchmark 2024/2025 cho thấy **kết quả suy luận hoạt tính kinase phụ thuộc mạnh vào thư viện kinase–substrate**, tức chất lượng thư viện là yếu tố giới hạn thật.

### Cited Findings
- Johnson JL et al., *Nature* 2023;613:759–766: **"90,000 sites of serine and threonine phosphorylation have so far been identified"** (abstract); phần introduction nói kinase chịu trách nhiệm chỉ được biết cho **"less than 4% of these sites"**; kinome người có **"more than 300 protein Ser/Thr kinases"**; nghiên cứu profile **303 kinase (>84% số được dự đoán là active)**, trong đó có **83 dark kinase**; annotation phủ 82.735 site MS high-throughput + 7.017 site low-throughput = **89.752 site**; **"few, if any, substrates have been identified for the majority of the approximately 300 human protein Ser/Thr kinases"** — [PMC9876800](https://pmc.ncbi.nlm.nih.gov/articles/PMC9876800/), [DOI 10.1038/s41586-022-05575-3](https://doi.org/10.1038/s41586-022-05575-3)
  - ⚠️ **Mâu thuẫn nội bộ trong chính bài này**: abstract nói 90.000 site, introduction nói "over 200,000 Ser and Thr phosphorylation sites on human proteins" đã được báo cáo trong các bộ MS. Khi trích, **nói rõ trích từ đâu**. [SOURCE conflict]
- Validation của Johnson et al. dựa trên **969 site** có kinase thượng nguồn đã được xác nhận bởi ít nhất 3 báo cáo độc lập, bao phủ "over one third of the kinome" — [PMC9876800](https://pmc.ncbi.nlm.nih.gov/articles/PMC9876800/). [ANALYSIS] 969 site / ~90.000 site ≈ **1,1%** là phần có bằng chứng kinase **chắc chắn** — con số này còn khắt khe hơn "dưới 4%".
- benchmarKIN (đánh giá toàn diện kinase activity inference từ phosphoproteomics): rất ít phosphosite đo được truy được về kinase thượng nguồn trong các thư viện hiện có, giới hạn phạm vi của activity inference; **phần lớn thuật toán inference cho kết quả tương đương nhau, nhưng thư viện kinase–substrate thay đổi mạnh hoạt tính suy ra**; thư viện curate thủ công (đặc biệt **PhosphoSitePlus**) cho kết quả tốt nhất; **thêm target dự đoán từ NetworKIN cải thiện hiệu năng** trong bối cảnh benchmark trên khối u — [PMC12098709](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12098709/), [bioRxiv 2024.06.27.601117](https://www.biorxiv.org/content/10.1101/2024.06.27.601117.full.pdf)
- benchmarKIN dùng dữ liệu đa omics khối u để benchmark, xác định kinase hoạt tính cao/thấp theo từng loại ung thư; tutorial của nó chạy trực tiếp **dữ liệu phosphoproteomics CPTAC** qua z-score kinase activity estimation (RoKAI) với thư viện curate, theo từng loại ung thư — [benchmarKIN docs](https://benchmarkin.readthedocs.io/en/latest/notebooks/tumorBench.html)
- Bối cảnh cũ hơn: các resource curate như PhosphoSitePlus chỉ bao phủ một tập giới hạn các tương tác, và các liên kết kinase–substrate dự đoán từ motif **rất ít khi được xác thực thực nghiệm** — Phosphoproteomics-based profiling of kinase activities in cancer cells, [PMC6126574](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6126574/)

### Inferences
- [ANALYSIS] **Đây là động lực thật, không phải động lực vay mượn.** Chuỗi lập luận đầy đủ, mỗi khâu có nguồn: (1) phosphoproteomics khối u đã là dữ liệu lâm sàng/translational thường quy (CPTAC); (2) để đọc được dữ liệu đó người ta suy hoạt tính kinase; (3) suy hoạt tính kinase phụ thuộc vào thư viện kinase–substrate (benchmarKIN); (4) thư viện đó phủ **<4%** site (Johnson 2023) và lệch nặng về kinase well-studied; (5) do đó dark kinase **không thể** được suy hoạt tính — chúng vô hình trong mọi phân tích phosphoproteomics khối u. ⇒ Mô hình dự đoán cặp kinase–site với khả năng **zero-shot cho kinase chưa có substrate nào** là đúng cái đang thiếu.
- [ANALYSIS] Điểm này còn giúp giải thích vì sao **zero-shot** (chứ không phải prediction thường) là setting đúng: đúng những kinase quan trọng nhất về mặt khoa học lại là những kinase không có dữ liệu huấn luyện. Đây là một lập luận methodological-necessity, không chỉ là novelty.
- [ANALYSIS] Việc benchmarKIN thấy "thêm target dự đoán từ NetworKIN cải thiện hiệu năng" là bằng chứng gián tiếp nhưng cụ thể rằng **dự đoán in-silico đã có giá trị thực dụng đo được** trong pipeline khối u. Đây là câu trả lời tốt nếu GVHD hỏi "dự đoán của em thì ai dùng".

### Gaps
- **Không tìm được một bài CPTAC nào tự nói rằng thiếu annotation kinase–substrate là giới hạn của họ.** Bằng chứng nối CPTAC với vấn đề này là qua benchmarKIN (bài phương pháp) và tutorial của nó, chứ không từ chính các flagship paper của CPTAC. Nếu muốn trích CPTAC trực tiếp, **phải tìm thêm** — [UNVERIFIED]
- Chưa xác minh được số liệu hiện tại của PhosphoSitePlus (bao nhiêu cặp kinase–substrate đã curate, bao nhiêu kinase có ≥1 substrate đã biết). Đây là con số rất đáng có cho slide; nên lấy trực tiếp từ phosphosite.org. [chưa làm]
- Không kiểm chứng được mối liên hệ giữa DARKIN benchmark và các số liệu trên — tôi **không** khảo sát DARKIN trong vòng này (đã có ghi chú khác về nó trong cùng thư mục: `01-substrate-holdout-novelty.md`, `02-darkin-sota-metric-audit.md`, `03-missing-label-pu-prior-art.md`).

---

## Gợi ý cách phát biểu trung thực (dùng trực tiếp được) [ANALYSIS]

**Nên nói:**
- "Đề tài thuộc khung **understudied kinome** của NIH IDG, với ứng dụng rõ nhất ở phân tích phosphoproteomics khối u."
- "Understudied kinase **có** giá trị tiên lượng ở nhiều loại ung thư (Essegian 2020; Southekal 2021), nhưng chưa biết chúng phosphoryl hóa cái gì nên không thể đưa vào pipeline suy hoạt tính kinase."
- "Dưới 4% phosphosite Ser/Thr của người có kinase thượng nguồn đã biết (Johnson et al., Nature 2023)."
- "Sirtuin, ngoài vai trò enzyme, bản thân là substrate của kinase; phần lớn phosphosite trên SIRT3–SIRT7 chưa gán được kinase — đây có thể là một case study nối với hướng sirtuin của thầy."

**Không nên nói:**
- "Đây là đề tài ung thư" / "đề tài góp phần điều trị ung thư". Không có bằng chứng nối trực tiếp.
- "Đây là đề tài aging." Khung aging quá generic; và **không** tìm được bằng chứng nào nối dark kinome với aging.
- "Đầu tiên" cho bất cứ thứ gì (quy ước ngôn từ của repo).
- Bất kỳ số nào trong mục Gaps ở trên.
