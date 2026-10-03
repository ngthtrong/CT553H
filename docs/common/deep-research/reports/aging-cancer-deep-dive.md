# Chọn dự đoán vị trí deacetyl hóa theo từng SIRT

**Khảo sát sâu, ngày 02/10/2026.** Tài liệu quyết định cho mốc **báo cáo lại đề tài ở tuần 6** (hiện tuần 4), với khoảng **8–9 tuần thực hiện** sau đó và một **ứng dụng/website bắt buộc**. Thay thế [bản so sánh lần 1](aging-vs-cancer-topic-comparison.md) — bản đó có một số khẳng định đã bị khảo sát mới này đảo lại, xem mục 2.

> **Mức kiểm chứng** — mọi con số trong tài liệu này đều kèm một dấu:
> `[toàn văn]` đã đọc toàn văn bài báo hoặc chính file dữ liệu · `[abstract]` chỉ đọc abstract/metadata chính thức · `[đã thử link]` tự gửi HTTP request ngày 02/10/2026 và ghi đúng mã trả về · `[tự đo]` tự tải dữ liệu về và tự tính con số · `[chưa kiểm]` chỉ có từ search snippet hoặc nguồn thứ cấp, **chưa xác nhận ở nguồn gốc**.
> Chỗ nào khảo sát không tìm được số thì ghi **"không tìm được"** — không thay bằng con số phỏng đoán.

---

## 1. Khuyến nghị: hai ứng viên gần như ngang nhau, chọn theo một câu hỏi duy nhất cho GVHD

**Khuyến nghị chính — Ứng viên A: dự đoán vị trí lysine bị deacetyl hóa bởi từng isoform SIRT1–SIRT7 (mức residue), thay bộ mô tả thủ công bằng PLM + multi-window CNN đa nhãn, đánh giá bằng split gom nhóm theo protein cộng một tập test MS độc lập nguồn.** Lý do duy nhất, nói trong một câu: đây là bài toán **chính tác giả gốc đã ghi là future work** ("protein language models such as ESM-2 and ProtBERT") và hiện **chỉ có LDA/decision tree trên 443 bộ mô tả** giải, trong khi toàn bộ bảng huấn luyện **6.801 site × ~444 đặc trưng × 7 nhãn SIRT đã tải về được và kiểm được hôm nay** `[tự đo]` ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/), [file nhãn trên GitHub](https://raw.githubusercontent.com/nashirag/ML-Hybrid_Ensemble_Method/HEAD/SIRT1-7_Investigation/ML_Components/All_Sirts_Feature_Y_labels.csv)).

**Đồng hạng — Ứng viên B: dự đoán vị trí phosphoryl hóa theo từng nhóm kinase gây ung thư, dùng benchmark non-homologous của dbPTM.** Lý do duy nhất: đây là ứng viên **duy nhất có sẵn tập đánh giá non-homologous do chính cơ sở dữ liệu công bố để so sánh chéo giữa các công cụ**, tách theo từng nhóm kinase (CDK, MAPK, AKT, PKC, CK2, GSK…), và dữ liệu **phát hành đã cắt cửa sổ ±10 residue sẵn** `[toàn văn]` ([dbPTM download](https://biomics.lab.nycu.edu.tw/dbPTM/download.php)).

**Hạng ba — Ứng viên C: dự đoán vị trí carbonyl hóa protein (K/R/P/T).** Lý do duy nhất: có tập test độc lập đã công bố (K 323 / P 114 / R 145 / T 124) và framing aging trung thực nhất (oxidative damage), nhưng **toàn bộ lập luận "còn nhiều khoảng trống" dựa trên một con số MCC mà chính bài báo nguồn tự mâu thuẫn** — xem mục 5.

### Vì sao hai ứng viên đầu ngang nhau, và điều gì quyết định

A và B **kéo về hai phía ngược nhau trên đúng hai tiêu chí quan trọng nhất**:

| | **A. Vị trí substrate SIRT** | **B. Vị trí phospho theo nhóm kinase** |
|---|---|---|
| **Dữ liệu + tập test độc lập** | Dữ liệu **đã tải về và đếm được** `[tự đo]`, nhưng split công bố chỉ là **10% holdout cùng một microarray** — **không phải tập test độc lập nguồn** `[toàn văn]` | **dbPTM tự công bố benchmark non-homologous** đúng để so sánh chéo công cụ `[toàn văn]` |
| **Mức khớp GVHD** | **Cao nhất**: cùng chủ đề aging/sirtuin với công trình mới nhất của GVHD, nhưng **khác bài toán và khác mức phân giải** | Cao về *phương pháp* (đúng lane residue-window của GVHD), **GVHD chưa có bài PTM nào** — vừa là tính mới vừa là khoảng trống về hướng dẫn sinh học |
| **Khoảng trống đóng góp** | **Rất lớn** — chưa từng có mô hình neural nào trên bộ dữ liệu này | Lớn — chỉ **14 bài deep learning 2024–2026** `[toàn văn]`, đối thủ gần nhất là preprint bioRxiv |
| **Khả thi 8–9 tuần** | Rất cao — 6.801 × 444, vài MB, train trên CPU được | Cao nhất — dữ liệu đã cắt cửa sổ sẵn, file nhỏ, không cần cấu trúc |

Nói thẳng: **A thắng về mức khớp GVHD và dư địa đóng góp; B thắng về cổng dữ liệu.** Quyết định treo vào **một câu hỏi phải hỏi GVHD ở tuần 6**: *thầy có coi một split gom nhóm theo protein mà sinh viên tự dựng, cộng một tập MS độc lập nguồn, là "tập test độc lập" đủ chuẩn hay không?* Nếu có → chọn A. Nếu thầy đòi một benchmark cộng đồng đã tồn tại sẵn → chọn B. Nếu thầy nói rõ muốn hướng **cancer** → chọn B (B có framing ung thư qua các kinase gây ung thư, A thì không).

### Hai ứng viên này **ghép được với nhau**, và đó là nước đi mạnh nhất

A và B cùng là bài toán **phân loại cửa sổ quanh một residue, nhãn nhị phân, mất cân bằng nặng** — tức là một encoder PLM dùng chung với hai đầu ra (một đầu "vị trí này có bị SIRT*i* deacetyl hóa không", một đầu "vị trí này có bị kinase nhóm *g* phosphoryl hóa không") là **multi-task learning**, bản thân nó đã là một đóng góp phương pháp cho tiêu chí 2, và đã có tiền lệ cùng dạng trong field (ESM-NBR dùng multi-task cho residue gắn nucleic acid `[chưa kiểm]` — [arXiv 2312.00842](https://arxiv.org/pdf/2312.00842)).

Có một cách ghép **chặt hơn và rẻ hơn**, và đây là nước đi tôi khuyên: **lấy dữ liệu acetylation tổng quát (không phân biệt enzyme) làm task phụ cho A**. dbPTM có **138.169 site acetylation thực nghiệm** cộng một bộ benchmark dựng sẵn **5.646 protein / 14.407 site dương / 8.704 site âm** `[toàn văn]` ([dbPTM download](https://biomics.lab.nycu.edu.tw/dbPTM/download.php)); CPLM 4.0 thì **file `Acetylation.zip` 31.806.865 byte tải về thật, HTTP 200** `[đã thử link]` ([CPLM](http://cplm.biocuckoo.cn/Download/Acetylation.zip)). Ghép như vậy giải đúng điểm yếu duy nhất của A: nó **mang một benchmark bên ngoài vào bài toán SIRT**, biến câu chuyện thành "từ acetyl-lysine tổng quát → phân giải theo enzyme", đúng dạng pretraining/multi-task mà reviewer tin.

---

## 2. ĐÍNH CHÍNH BẮT BUỘC — sáu khẳng định sai phải sửa trước khi nói với GVHD

Những điểm dưới đây có trong [bản khảo sát lần 1](aging-vs-cancer-topic-comparison.md) hoặc trong các trao đổi trước. Khảo sát mới đã đảo lại. **Đọc kỹ sáu mục này trước khi soạn slide tuần 6** — nói lại con số sai trước mặt GVHD là rủi ro lớn nhất và rẻ nhất để tránh.

### 2.1. Số liệu DeepSIRT: accuracy 76,69% / MCC 0,49 / AUC 0,833 là **sai**

**Khẳng định cũ:** DeepSIRT đạt accuracy 76,69%, MCC 0,49, AUC 0,833, nên "còn khoảng trống rất rộng về số liệu".

**Thực tế:** abstract chính thức trên PubMed báo **"an average of up to 85,77% sensitivity, 97,32% specificity, and 0,82 MCC for seven members of the sirtuin family"** `[abstract]` ([PubMed 34058657](https://pubmed.ncbi.nlm.nih.gov/34058657/), [DOI 10.1016/j.compbiolchem.2021.107514](https://doi.org/10.1016/j.compbiolchem.2021.107514)). Bộ số 76,69% / 0,49 / 0,833 **không tìm được ở bất kỳ nguồn nào** — không có trong abstract, và toàn văn bị chắn (ScienceDirect trả **HTTP 403** `[đã thử link]`).

**Giải thích khả dĩ nhất theo khảo sát:** đó là số của **người khác đánh giá lại DeepSIRT như một baseline**, rất có thể là một bảng bên trong SirtSAGE, nơi bài toán được đặt lại thành **một bài multi-class "unified" duy nhất** thay vì bảy bài nhị phân riêng theo từng isoform của DeepSIRT — tức là một setting khó hơn hẳn. Abstract SirtSAGE nói đúng điều đó: nó "outperforms state-of-the-art 1D-CNN baselines… **despite operating under a substantially more stringent unified multi-class setting**" `[toàn văn của abstract]` ([Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1142/S2737416527400011?fields=abstract)).

**Hệ quả hành động:** **không được gán 76,69% / 0,49 / 0,833 cho DeepSIRT** khi chưa thấy bảng nguồn. Và vì MCC thật của DeepSIRT là **0,82**, lập luận "nhánh sirtuin classification còn nhiều chỗ cải thiện về số liệu" **sụp** — đây là một lý do nữa để không chọn bài toán phân loại họ sirtuin.

### 2.2. SenSeqNet: giả thuyết "tác giả không gom cụm đồng dạng" là **sai**

**Khẳng định cũ:** nghi vấn rằng tác giả SenSeqNet không chạy clustering theo identity, nên con số 86,43% là lạc quan.

**Thực tế:** họ **có làm**. Bản preprint dùng **CD-HIT ngưỡng 0,4**; bản công bố 2026 dùng **MMseqs2 ngưỡng 0,3** kèm câu tuyên bố chống rò rỉ nguyên văn: *"Only these representative sequences were used for subsequent model training and validation **to avoid data leakage**"* `[toàn văn]` ([PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/)).

**Khuyết điểm thật, đã kiểm chứng, phải thay giả thuyết cũ bằng ba điểm này:**

1. **Rò rỉ ở mức gene (group leakage) trong split chính.** Gom cụm ở 30–40% identity bỏ được *cặp gần trùng* nhưng **không bỏ được tư cách thành viên họ gene**. Notebook v2 import `train_test_split` và `KFold`, **không bao giờ dùng `GroupKFold`/`StratifiedGroupKFold`**, dù header FASTA v2 có sẵn trường `gene=` mà notebook trích đặc trưng tự parse `[tự đo]` ([All_code_v2/SenSeqNet.ipynb](https://github.com/HanliJiang13/SenSeqNet/blob/HEAD/All_code_v2/SenSeqNet.ipynb)).
2. **Nửa âm của tập "external validation" v1 là bản sao của tập huấn luyện.** Đếm trực tiếp: **6.110 chuỗi trùng byte-identical = 94,83% trong số 6.443 external negatives**, và **26/26 gene symbol của external negatives đều đã có trong tập negative huấn luyện** `[tự đo]`. Đây là phát hiện cứng nhất và dễ kiểm nhất trong toàn bộ khảo sát.
3. **Gom cụm bất đối xứng theo lớp, cộng external test chỉ có một lớp ở bản v2.** Notebook đọc `reps_30_rep_seq_pos.fasta` và `reps_30_rep_seq_neg.fasta` riêng — gom cụm từng lớp độc lập thì **không ngăn được một chuỗi dương và một chuỗi âm gần trùng nhau**, và thực tế v1 có **16 cặp trùng tuyệt đối mang cả hai nhãn** `[tự đo]`. External validation của v2 chỉ báo **true positive rate 77,55% (40.502/52.227)** từ 26 gene, **không có negatives → không có specificity, không có MCC, không có AUC** `[toàn văn]` ([PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/)).

Thêm một khuyết điểm thứ tư về **độ tập trung**: **5 gene chiếm 56,0% toàn bộ chuỗi dương huấn luyện** (CKB 4.894; SYK 3.482; AAK1 2.294; DAO 1.784; TOM1 1.494), và **2 gene chiếm 97,1% external positives** (BIN1 12.135; HBP1 3.909) `[tự đo]`.

### 2.3. Con số dataset SenSeqNet: 238.634 / 217.696 là của **bản preprint**, không phải bản công bố

Phải tách hai bản ra ở mọi chỗ:

| | **v1 — preprint bioRxiv** `10.1101/2024.10.28.620702` | **v2 — Aging Cell 2026** `10.1111/acel.70344` |
|---|---|---|
| Gom cụm | **CD-HIT 0,4** | **MMseqs2 0,3** |
| Thô | **238.634 dương / 217.696 âm** | **292.759 dương / 373.098 âm** |
| Sau gom cụm | **24.914 / 28.752** | **43.381 / 32.673** |
| Accuracy | **83,55%**, AUC 0,92 | **86,43%**, AUC 0,94, MCC 0,7221 |

Nguồn: `[toàn văn]` ([bioRxiv v2](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full)) và `[toàn văn]` ([PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/)). Hai con số 24.914 / 28.752 **khớp chính xác** với số chuỗi đếm được trong file FASTA v1 trên GitHub `[tự đo]`.

Có một **bất nhất số học giữa hai bản, đáng nêu với GVHD**: v1 gom cụm ở ngưỡng *lỏng hơn* (0,4) và giữ 24.914/238.634 = **10,4%**; v2 gom cụm ở ngưỡng *chặt hơn* (0,3) mà giữ 43.381/292.759 = **14,8%** — ngưỡng chặt hơn lại giữ nhiều đại diện hơn 1,74 lần là bất khả trên cùng dữ liệu, trừ khi tham số coverage khác nhau mạnh (MMseqs2 `easy-cluster` mặc định `-c 0.8`, nên mảnh lệch chiều dài tự tạo cụm riêng) `[tự đo, suy luận]`.

### 2.4. TransNRank: đã bị **rút khỏi arXiv**, không được coi là cạnh tranh đang sống

**Khẳng định cũ:** TransNRank (2026) là một đối thủ Transformer mới trong nhánh neoantigen.

**Thực tế:** trang arXiv ghi nguyên văn *"This paper has been withdrawn by Yuenan Hou"*, kèm tuyên bố của chính nhóm rằng *"the final authorship has not been determined and this version has not been polished"*, và **không có PDF** `[toàn văn của trang abstract]` ([arXiv:2608.01924](https://arxiv.org/abs/2608.01924)).

**Hệ quả:** **không trích TransNRank như công trình cạnh tranh**, và không dùng con số "top-20 recall 46,9% → 53,1%" của nó. Nó chỉ còn một giá trị: bằng chứng rằng **các nhóm khác đang tấn công đúng benchmark NCI/TESLA/HiTIDE trong năm 2026**.

### 2.5. RTK_RAG: **GVHD không phải tác giả**

Tra PubMed trực tiếp: RTK_RAG (*J Chem Inf Model* 65(13):7277, 2025-07-14) có tác giả **Wei SS, Jhang WE, Liu YC, Chuang CC, Ou YY** — **QT Ho không có trong danh sách tác giả** `[toàn văn metadata]`. Tức là **đề tài RTK–ATP mà sinh viên vừa bỏ được dựng trên một bài báo mà chính GVHD không viết.**

**Hệ quả, phải đổi cách nói:** từ nay không được gọi RTK_RAG, DeepNeoAG, NeoGen-BC, RAG_MCNNIL6, NAD_MCNN là "công trình của nhóm GVHD". Đó là nhóm **Prof Ou** tại Yuan Ze University, một đồng tác giả thường xuyên nhưng **không phải người hướng dẫn**. Danh mục đồng tác giả thật của GVHD với Prof Ou là **17 bài trên PubMed** `[toàn văn metadata]`, và trong đó **không có bài nào về ung thư** — mục duy nhất có chữ "tumour" là TNFPred (tumour necrosis factors, một họ cytokine, không phải cancer genomics). Lưu ý thêm: chuỗi `Ho QT[Author]` trả **71 bản ghi** trên PubMed vì trùng chữ viết tắt với nhiều tác giả khác, nên **không được khẳng định "GVHD có 9 bài về cancer"** `[chưa kiểm — không phân giải được định danh tác giả]`.

### 2.6. Prof Ou và aging: kết quả tìm kiếm cũ là **false positive**

Lần quét keyword trước tưởng như có một bài aging trong danh mục Prof Ou. **Sai: nó khớp chữ "le*verag*ing" trong tiêu đề RTK_RAG** `[toàn văn — file local]`. **Prof Ou không có bài nào về aging.**

Quét lại cả hai danh mục (`docs/common/advisor/Prof Ho/research.md`, 14 công trình; và `Prof Ou/research.md`) với các từ khóa sirtuin|aging|ageing|senescen|autophag|telomer|longevity|lifespan: **trên toàn bộ hai danh mục chỉ có đúng MỘT bài thuộc địa hạt aging — SirtSAGE của GVHD** `[toàn văn — file local]`. Không có autophagy, không có carbonylation, không có glycation, không có aggregation, không có telomere, không có aging clock, không có peptide chống lão hóa.

**Hệ quả kép, phải nói cả hai mặt:** (a) **tiêu chí 1 rất dễ lập luận** ở hầu hết mọi nhánh aging, vì GVHD chưa công bố gì ở đó; (b) **GVHD chỉ hướng dẫn được phần sinh học của sirtuin**. Với carbonylation, glycation, autophagy hay aggregation, **sinh viên là người phải mang phần sinh học tới** — chấp nhận được ở mức luận văn, nhưng phải chuẩn bị một trang brief sinh học cho buổi tuần 6 để GVHD không phải đánh giá sinh học lạ trong tình trạng không có chuẩn bị.

---

## 3. Ứng viên A — vị trí lysine bị deacetyl hóa bởi từng isoform SIRT1–SIRT7

### Bài toán chính xác

**Vào:** một chuỗi protein (hoặc một accession UniProt) cộng một vị trí lysine đã acetyl hóa. **Ra:** bảy điểm số, mỗi điểm cho một isoform SIRT1–SIRT7, trả lời "lysine này có bị isoform đó deacetyl hóa không". Đây là **bài toán đa nhãn, không phải đa lớp** — một lysine có thể là substrate của nhiều SIRT cùng lúc; hàng dữ liệu thật có dạng `P05141_163_c0,1,1,0,1,0,1,1` (UniProt P05141, vị trí 163, dương với 5 trong 7 isoform) `[tự đo]`.

### Vì sao quan trọng về mặt sinh học, và vì sao cấp thiết

Sirtuin là họ deacylase phụ thuộc NAD+ điều hòa biểu hiện gene, sửa chữa DNA, cân bằng chuyển hóa, đáp ứng stress, apoptosis và các con đường liên quan lão hóa `[toàn văn của abstract]` ([SirtSAGE abstract](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1142/S2737416527400011?fields=abstract)). Biết **SIRT nào tác động lên lysine nào** là điều kiện để nói một thuốc nhắm SIRT sẽ thay đổi protein nào — khác hẳn với việc chỉ biết "lysine này có acetyl hóa".

Tính cấp thiết thì có một con số rất mạnh: phương pháp thực nghiệm truyền thống, permutation array, đạt **precision 2,0%**; pipeline ML 2025 đẩy lên **43,0% cho SIRT2** (xác nhận lại 64/149 substrate đã biết) `[toàn văn]` ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/), [trang Nature](https://www.nature.com/articles/s42004-025-01717-6)). Tức là ngay cả sau khi có ML, **hơn một nửa dự đoán vẫn sai** — đây là bài toán còn mở thật, không phải bài toán đã bão hòa.

### Công trình trước, **phân nhóm theo họ phương pháp**

| Nhóm phương pháp | Công trình tiêu biểu | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. Thực nghiệm peptide microarray (không ML)** | Rauh et al. 2013, *Nat Commun* 4:2327 — microarray **6.802 vị trí acetylation người** đo song song với cả bảy sirtuin `[chưa kiểm]` ([ncomms3327](https://www.nature.com/articles/ncomms3327)) | Là **nguồn nhãn gốc** duy nhất phân giải theo enzyme ở quy mô lớn; đo trực tiếp | Peptide ngắn, không phải protein đủ dài; tín hiệu in vitro; không mở rộng được ngoài những site đã có trên array |
| **2. ML cổ điển trên bộ mô tả thủ công, một mô hình cho một isoform** | Ridgeway et al. 2025, *Commun Chem* 8(1):340 — bảy mô hình ensemble riêng, mỗi base model là **LDA hoặc decision tree**, SMOTE/oversampling cho mất cân bằng, stack với điểm acetyl-lysine tổng quát của MuSiteDeep; đặc trưng = one-hot + MACCS Keys (166 fingerprint) + ProtDCal `[toàn văn]` ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)) | **Dữ liệu và code công khai, tải được**; có xác nhận MS tiến cứu (64 site SIRT2 mới); định nghĩa bài toán rõ ràng | **Không có baseline neural nào**; bảy mô hình độc lập nên **không khai thác được tương quan giữa các isoform**; cửa sổ chỉ 13 aa — chính tác giả nêu đó là hạn chế; split là **stratified K-fold + holdout 10% cùng một microarray** |
| **3. Phương pháp đặc thù một isoform, trước 2020** | SIRT1 substrate bằng SVM tích hợp nhiều nguồn, *Sci Rep* 2017 `[chưa kiểm]` ([s41598-017-04847-7](https://www.nature.com/articles/s41598-017-04847-7)); SIRT3 substrate specificity bằng peptide array + ML `[chưa kiểm]`; QSAR cho substrate SIRT1 trong đái tháo đường, *J Bioinform Comput Biol* 2022 `[chưa kiểm]` ([S0219720022500081](https://www.worldscientific.com/doi/10.1142/S0219720022500081)) | Tiền lệ cho thấy "đặc hiệu theo isoform" là bài toán được chấp nhận | Chỉ một isoform; dữ liệu nhỏ; **công cụ web SIRT1 2017 đã chết** — `http://bioinfo.bjmu.edu.cn/huac/` trả **HTTP 000 sau 8,1 s** `[đã thử link]` |
| **4. Dự đoán site acetylation tổng quát, không phân giải enzyme (PLM hiện đại)** | PLMGraph-Ace 2026 (PLM + sequence-distance graph) `[chưa kiểm]` ([S1389202926000188](https://www.sciencedirect.com/science/article/pii/S1389202926000188)); PBertKla 2025 cho lactylation, **AUC > 0,880** trên validation độc lập `[chưa kiểm]` ([BMC Biol](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-025-02202-1)); tổng quan cả họ task trong *Brief Bioinform* 25(6):bbae469 `[chưa kiểm]` | Dùng đúng công nghệ hiện đại; dữ liệu rất lớn | **Không biết enzyme nào gây ra modification** — mất đúng phần thông tin có giá trị sinh học; và nhánh này **đã đông** |
| **5. Phân loại chính protein sirtuin (không phải site)** | DeepSIRT 2021 (1D-CNN + PSSM/AAC, **sens 85,77% / spec 97,32% / MCC 0,82**) `[abstract]`; SirtSAGE 2026 (ESM-2 → GATv2 có cổng pLDDT + lớp KAN) `[toàn văn của abstract]` | Là lane của chính GVHD | **Đã bị chiếm, bởi chính GVHD, trong năm nay.** Coi phân loại họ/isoform sirtuin là đóng. Dữ liệu DeepSIRT cũng **mất** — `http://140.138.155.216/deepsirt/` trả **HTTP 000 sau 25,0 s** `[đã thử link]` |

### Khoảng trống cụ thể

Ba điểm, xếp theo độ chắc:

1. **Chưa có PLM nào được áp dụng cho bài toán substrate SIRT phân giải theo isoform.** Chỉ có LDA/decision tree trên 443 bộ mô tả, và **chính tác giả ghi ESM-2/ProtBERT là bước tiếp theo nhưng không làm** `[toàn văn]`.
2. **Chưa có mô hình đa nhãn nào trên cả bảy SIRT cùng lúc.** Công trình 2025 fit bảy mô hình độc lập, nên về mặt kiến trúc **không thể** khai thác việc một lysine thường là substrate của nhiều isoform.
3. **Cửa sổ 13 aa là hạn chế do chính tác giả thừa nhận** ("abbreviated peptide sequences, which may not effectively represent full-length enzyme-substrate interactions") `[toàn văn]` — đây là lời mời trực tiếp dùng ngữ cảnh toàn chuỗi của PLM, và đúng là setting multi-window CNN của GVHD.

### Dữ liệu — kích cỡ và trạng thái truy cập **đã thử**

| File / nguồn | Kích cỡ đo được | Trạng thái |
|---|---|---|
| `https://github.com/nashirag/ML-Hybrid_Ensemble_Method` | — | **HTTP 200** `[đã thử link]` |
| `All_Sirts_Feature_Y_labels.csv` | **224.234 byte, 6.802 dòng = 1 header + 6.801 site có nhãn**, 7 cột nhãn `SIRT_1..7_EXPERIMENTALLY_ACTIVE` | **HTTP 200, tải về và đếm được** `[tự đo]` |
| `sirt_training_feature_set.csv` | **7.395.733 byte, 6.802 dòng, header có 445 trường** (trường đầu là `uid_pos`) | **HTTP 200, tải về và đếm được** `[tự đo]` |
| Zenodo DOI 10.5281/zenodo.17082245 | không tìm được nội dung | `[chưa kiểm]` |
| MS data, PeptideAtlas PASS05848 | không tìm được kích cỡ | `[chưa kiểm]` |
| Bộ proteome-wide (lysine lộ bề mặt) | quá lớn cho GitHub, nằm trên Google Drive | link có trong README nhưng **nội dung chưa kiểm** `[chưa kiểm]` |
| dbPTM benchmark Acetylation (làm task phụ) | **5.646 protein / 14.407 site dương / 8.704 site âm** | **trang download HTTP 200** `[toàn văn + đã thử link]` |
| CPLM 4.0 `Acetylation.zip` (task phụ) | **31.806.865 byte, content-type application/zip** | **HTTP 200, tải thật** `[đã thử link]` |

**Một lệch nhỏ phải khai báo trung thực:** bài báo ghi "443 descriptive features", nhưng header file công bố có **445 trường tính cả `uid_pos`, tức 444 cột không phải ID** `[tự đo]`. Báo cáo 443 là *con số bài báo tuyên bố* và 444/445 là *cái file thật chứa*.

### Trần hiệu năng trung thực

**Precision xác nhận bằng MS: 37–43%** — cụ thể **SIRT2 đạt 43,0%** (64/149) và SET8 (một methyltransferase, cùng framework) đạt **37,4%** trên 2.367 site dự đoán `[toàn văn]`. **Per-isoform AUC/MCC/accuracy cho SIRT1 và SIRT3–SIRT7: không tìm được** — bài báo chỉ báo chi tiết cho SIRT2 và SET8. Nghĩa là **sinh viên có thể phải tự chạy lại `SIRT_ALL_RUNS.ipynb` để dựng baseline** — rẻ (LDA/decision tree trên 6.801×444) nhưng là công việc **ngoài kế hoạch**, phải tính vào tuần 7.

### Điểm theo năm tiêu chí GVHD

| Tiêu chí | Đánh giá | Căn cứ |
|---|---|---|
| **1. Tính mới** | **Cao** | Chưa có PLM nào trên bài toán này; chưa có mô hình đa nhãn 7 isoform nào. Và **khác bài toán, khác mức phân giải so với SirtSAGE** — SirtSAGE phân loại *chính protein sirtuin* ở mức toàn chuỗi, A dự đoán *vị trí substrate* ở mức residue. Không phải chạy lại SirtSAGE |
| **2. Cải tiến phương pháp** | **Cao** | Bộ mô tả → ESM-2/ProtT5 + multi-window CNN; cửa sổ 13 aa → ngữ cảnh toàn chuỗi; 7 mô hình rời → một đầu msCNN đa nhãn. Nằm đúng trong họ mCNN/msCNN của GVHD |
| **3. Phương pháp mới (xa hơn PLM)** | **Trung bình–cao, cần chọn cẩn thận** | Lựa chọn an toàn nhất: thay embedding ProtT5 đông lạnh bằng **PLM nhận biết cấu trúc (ProstT5/SaProt)**, hoặc **LoRA/PEFT thay vì đông lạnh**, hoặc **đầu KAN**. **Cảnh báo:** cổng cấu trúc + graph attention là **đúng nước đi của SirtSAGE**, nên nếu dùng thì phải đóng khung là *chuyển sang một bài toán mới (mức residue)*, không phải phát minh |
| **4. XAI** | **Rất cao — mạnh nhất trong tất cả ứng viên** | Attribution theo từng vị trí trên cửa sổ 13 aa cho ra trực tiếp một **sequence logo đặc hiệu theo isoform**, đối chiếu được với đặc hiệu đã biết thực nghiệm từ Rauh 2013. Đây là **giải thích kiểm chứng được**, không phải một đồ thị SHAP trang trí |
| **5. Web app** | **Cao, và là khác biệt thật** | Mô hình nhỏ, input nhỏ (dán chuỗi hoặc UniProt ID → điểm theo từng lysine cho cả 7 isoform). Quan trọng: **hiện không tồn tại web tool sống nào cho substrate sirtuin hay target sirtuin** — bài 2025 không có web server `[toàn văn]`, công cụ SIRT1 2017 chết `[đã thử link]`, và host `140.138.155.216` của DeepSIRT/NAD_MCNN **time out cả hai đường** `[đã thử link]` |

### Rủi ro cụ thể và cổng dừng

**Rủi ro 1 — split 10% holdout cùng nguồn.** Đây là **đúng khuyết điểm đã làm đề tài trước yếu**. Phải tự định nghĩa split chặt hơn: gom nhóm theo protein (hold out cả UniProt entry, không phải từng site), hoặc CD-HIT trên các 13-mer. Và phải có một **tập test độc lập nguồn**: 64 site SIRT2 xác nhận MS (PeptideAtlas PASS05848), cộng một nghiên cứu proteomics acetylome SIRT2 độc lập `[chưa kiểm]` ([PMC8907344](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8907344/)). **Cổng dừng: nếu đến hết tuần 7 không dựng được tập test độc lập nguồn với cả hai lớp, chuyển sang Ứng viên B.**

**Rủi ro 2 — nhãn là hoạt tính peptide array in vitro, không phải sự thật trong tế bào.** Cách nói trung thực bắt buộc: *"dự đoán hoạt tính deacetyl hóa mức peptide của từng isoform SIRT, đo bằng acetylome microarray"*, dùng site MS làm kiểm tra trực giao. Nói "dự đoán substrate in vivo" là đòn tấn công hiển nhiên nhất của reviewer.

**Rủi ro 3 — mất cân bằng nặng theo từng isoform** (bài 2025 phải dùng SMOTE/oversampling ở mức > 20:80). **Báo MCC và AUPRC, không báo accuracy.**

**Rủi ro 4 — bốn công trình 2026 lân cận.** SirtSAGE (phân loại sirtuin, của chính GVHD), PLMGraph-Ace (site acetylation tổng quát, PLM+graph), AcetylBench (benchmarking), và một bài sàng lọc chất ức chế SIRT2 trên *Sci Rep* `[chưa kiểm]` ([s41598-026-52371-4](https://www.nature.com/articles/s41598-026-52371-4)). **Không có cái nào làm substrate SIRT phân giải theo isoform.** Nêu cả bốn với GVHD để thầy thấy sinh viên đã tra.

**Rủi ro 5 — AcetylBench 2026 vừa là lý lẽ vừa là lời cảnh báo.** Bài này báo rằng ba nguồn lạm phát chỉ số (sequence redundancy, test set không độc lập, giảm chiều bị khóa theo phân phối) **kéo accuracy biểu kiến 99,38% xuống AUC cross-database 0,523, không phân biệt được với ngẫu nhiên**; và AUC cross-validation nội bộ **0,815–0,867 sụp xuống 0,582–0,607** trên một benchmark thực sự độc lập `[chưa kiểm — mọi đường vào toàn văn đều bị chắn]` ([Springer](https://link.springer.com/article/10.1186/s12859-026-06593-y)). Đây là **lý lẽ sẵn có để biện minh cho giao thức kiểm soát rò rỉ** — và đồng thời là cảnh báo rằng **mọi số acetylation mới phải báo cross-database, nếu không sẽ không ai tin**. **Nhưng: không tìm được URL tải file của AcetylBench**, nên "đánh giá trên AcetylBench" hiện là **ý định, không phải lựa chọn đã xác minh**.

---

## 4. Ứng viên B — vị trí phosphoryl hóa theo từng nhóm kinase gây ung thư

### Bài toán chính xác

**Vào:** chuỗi protein + một vị trí S/T/Y. **Ra:** nhãn nhị phân theo từng nhóm kinase — "vị trí này có bị kinase nhóm *g* phosphoryl hóa không", với *g* ∈ {CDK, MAPK, PKA, PKC, CK2, AKT, GSK, RSK, PDK1, SGK, …}. Dương = residue đã được xác nhận phosphoryl hóa bởi nhóm đó; âm = residue cùng loại amino acid nhưng không bị modify.

### Vì sao quan trọng, và vì sao cấp thiết

Các nhóm kinase trong benchmark **chính là trục tín hiệu gây ung thư**: CDK (chu kỳ tế bào), MAPK (RAS–MAPK), AKT/PDK1/SGK (PI3K–AKT–mTOR), PKC, CK2, GSK3, RSK. Liên kết với ung thư có số lượng hóa: ActiveDriverDB dùng **hơn 260.000 site PTM thực nghiệm** và báo rằng **16–21% các thay thế amino acid đã biết tác động đến site PTM**, trên cả ba nhóm đột biến gây bệnh, đột biến somatic ung thư và biến thể germline của dân số `[chưa kiểm]` ([NAR 46(D1):D901](https://academic.oup.com/nar/article/46/D1/D901/4566599)).

### Công trình trước, **phân nhóm theo họ phương pháp**

| Nhóm phương pháp | Công trình tiêu biểu | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. CNN trên đặc trưng chuỗi** | DeepPhos — CNN, tốt hơn các kiến trúc DL khác trên site S/T và Y `[chưa kiểm]` | Kiến trúc đơn giản, rẻ, đã được chấp nhận | Không có ngữ cảnh toàn chuỗi; không phân giải theo kinase ở mức nhóm |
| **2. RNN/LSTM xếp tầng** | DeepPPSite — stacked LSTM `[chưa kiểm]` ([S0003269720304875](https://www.sciencedirect.com/science/article/abs/pii/S0003269720304875)) | Bắt được phụ thuộc trong cửa sổ | Chậm hơn CNN mà không thắng rõ; không có PLM |
| **3. Attention-CNN + Transformer** | DeepPhosPPI — dùng **bộ Betts (306 bản ghi)** và **Dset_308 (308 bản ghi)** làm benchmark độc lập `[chưa kiểm]` ([bbaf462](https://academic.oup.com/bib/article/26/5/bbaf462/8248860)) | Có benchmark độc lập được công bố | Benchmark **rất nhỏ** (vài trăm bản ghi) |
| **4. PLM + Transformer tự hồi quy, phân giải theo kinase** | Preprint bioRxiv 2025 — **ESM-2 650M**, 5.385 substrate huấn luyện / 969 validation, ba tập test trong đó có một **"Rare-Group Test Set" 14 mẫu từ hai nhóm kinase bị loại hoàn toàn khỏi huấn luyện** `[chưa kiểm]` ([bioRxiv 2025.03.12.642740](https://www.biorxiv.org/content/10.1101/2025.03.12.642740v1.full)) | **Đối thủ gần nhất, và dùng đúng nguyên liệu của sinh viên**; thiết kế tập test theo nhóm bị giữ hoàn toàn ra ngoài là một ý tưởng đánh giá tốt để học | Vẫn là **preprint**, chưa qua peer review → **không gian chưa đóng**; tập test chỉ **14 mẫu** |
| **5. Đầu KAN trên PLM cho site phospho** | CaLMPhosKAN — hợp nhất embedding nhận biết codon và nhận biết amino acid với **đầu KAN dựa trên wavelet** `[chưa kiểm]` ([btaf124](https://academic.oup.com/bioinformatics/article/41/4/btaf124/8090024)) | Chứng minh **đầu KAN công bố được trong đúng niche PTM-site** | Không phân giải theo nhóm kinase |

**Mức đông đúc đo được:** PubMed `((phosphorylation site[TIAB] OR ubiquitination site[TIAB] OR acetylation site[TIAB]) AND prediction[TIAB] AND deep learning[TIAB]) AND 2024:2026[dp]` → **14 bản ghi** `[toàn văn — tự chạy truy vấn]`. **Ít đông nhất trong mọi task có benchmark thật** mà khảo sát tìm được. Lưu ý: đếm theo TIAB phrase **hệ thống đếm thiếu**, nên 14 là so sánh tương đối, không phải tổng điều tra.

### Dữ liệu — kích cỡ và trạng thái truy cập **đã thử**

Mirror đang sống của dbPTM là **`https://biomics.lab.nycu.edu.tw/dbPTM/` → HTTP 200, 0,10 s**; trang download → **HTTP 200** `[đã thử link]`. Host cũ `https://awi.cuhk.edu.cn/dbPTM/` trả **HTTP 403** và `http://dbptm.mbc.nctu.edu.tw/` không kết nối được `[đã thử link]` — **phải dùng host NYCU**.

Số site thực nghiệm, đọc trực tiếp từ trang download `[toàn văn]`:

| Loại PTM | Site thực nghiệm | Số literature |
|---|---|---|
| Phosphorylation | **1.615.054** | 44.986 |
| Ubiquitination | **348.307** | 669 |
| Acetylation | **138.169** | 19.451 |
| Dephosphorylation | **133** | 95 |

Và **đây là phần quyết định**: dbPTM tuyên bố rõ rằng vì số liệu cross-validation không so sánh được giữa các công cụ, bản cập nhật này *"compiles **non-homologous benchmark datasets** to evaluate the predictive power for PTM site prediction tools"*, kèm hướng dẫn cho các điểm hoạt động high-Sn / high-Sp / cân bằng `[toàn văn]`. Benchmark **tách theo nhóm kinase**, với ba cột số mỗi dòng:

| Kinase | col1 | col2 | col3 | Kinase | col1 | col2 | col3 |
|---|---|---|---|---|---|---|---|
| CDK | 1.020 | 1.503 | 29.823 | CK1 | 174 | 339 | 5.808 |
| MAPK | 857 | 1.270 | 22.436 | RSK | 221 | 215 | 6.985 |
| PKA | 905 | 1.209 | 29.813 | GRK | 77 | 147 | 2.310 |
| PKC | 691 | 943 | 24.207 | PKG | 126 | 145 | 7.311 |
| CK2 | 511 | 819 | 15.387 | DYRK | 109 | 142 | 3.470 |
| CAMKL | 454 | 556 | 20.129 | MAPKAPK | 100 | 125 | 3.096 |
| GSK | 291 | 397 | 10.328 | DMPK | 99 | 109 | 3.533 |
| AKT | 351 | 380 | 14.617 | PKD | 88 | 97 | 3.401 |
| CAMK2 | 254 | 366 | 12.575 | PDK1 | 77 | 93 | 2.274 |
| | | | | SGK | 63 | 77 | 3.057 |

**Cảnh báo bắt buộc:** **header của bảng này không được lấy về trong lần scrape, nên ý nghĩa ba cột là suy luận, không phải xác nhận** — *có thể* là protein / site dương / site âm `[chưa kiểm]`. **Phải xác nhận trước tuần 6**, vì toàn bộ lập luận về cổng dữ liệu của B dựa vào bảng này.

Định dạng: mỗi bản ghi có UniProt ID, vị trí modify, loại PTM, và **chuỗi gồm 10 amino acid phía trên và 10 phía dưới** (dùng dấu gạch ở đầu/cuối protein); site không align được chính xác vào chuỗi UniProt thì bị loại; tích hợp 41 cơ sở dữ liệu PTM `[toàn văn]`.

### Trần hiệu năng trung thực

**Không tìm được** một số SOTA nào cho đúng bài toán "phospho-site theo nhóm kinase trên benchmark dbPTM" — các công trình trên đều dùng benchmark riêng. Nghĩa là: **dư địa chắc chắn có nhưng không định lượng được trước**, và sinh viên sẽ phải **tự dựng baseline** trên split của dbPTM. Đây là một điểm yếu thật so với Ứng viên C, nơi tập test độc lập kèm luôn các con số đối thủ.

### Điểm theo năm tiêu chí

| Tiêu chí | Đánh giá | Căn cứ |
|---|---|---|
| **1. Tính mới** | **Trung bình–cao** | **GVHD chưa có bài PTM nào** trong 17 bài đồng tác giả `[toàn văn metadata]` → mới so với chính danh mục của thầy. Nhưng đối thủ gần nhất (preprint bioRxiv 2025) dùng đúng ESM-2 → phải phân biệt bằng *phân giải theo nhóm* và *giao thức đánh giá*, không bằng kiến trúc |
| **2. Cải tiến phương pháp** | **Cao** | Dữ liệu đã cắt cửa sổ ±10 sẵn nên port pipeline là rẻ nhất; cải tiến là msCNN đa cửa sổ + đầu đa nhãn theo nhóm kinase |
| **3. Phương pháp mới** | **Trung bình–cao** | Giống A: ProstT5/SaProt, LoRA, hoặc đầu KAN — và **CaLMPhosKAN chứng minh đầu KAN công bố được đúng trong niche này** `[chưa kiểm]` |
| **4. XAI** | **Cao** | Motif kinase là kiến thức sinh học có sẵn và rất cụ thể (ví dụ CK2 ưa acid ở +1/+3), nên attribution theo vị trí đối chiếu được với motif đã biết |
| **5. Web app** | **Cao** | "Dán chuỗi → highlight các site dự đoán theo từng kinase" — tương tự trực tiếp app RTK–ATP sinh viên đã thiết kế |

### Rủi ro cụ thể và cổng dừng

**Rủi ro 1 — cửa sổ ±10 có thể quá hẹp cho multi-window CNN.** Các bài của GVHD thường scan nhiều độ rộng tới ±(15–25). Nếu file phát hành bị cap ở 21 residue thì phải **trích lại cửa sổ từ chuỗi UniProt dùng vị trí của dbPTM** `[chưa kiểm]`. **Đây là rủi ro cụ thể, kiểm được, phải giải quyết trước tuần 6** — mất một buổi.

**Rủi ro 2 — ý nghĩa ba cột trong bảng benchmark chưa xác nhận.** Cùng mức ưu tiên như trên.

**Rủi ro 3 — framing ung thư là một bước gián tiếp.** "Kinase này gây ung thư, nên dự đoán site của nó liên quan ung thư" là đúng nhưng cần một câu diễn giải cẩn thận. Con số 16–21% của ActiveDriverDB là câu chống đỡ tốt nhất `[chưa kiểm]`.

**Cổng dừng:** nếu đến hết tuần 7 mà (a) không xác nhận được ý nghĩa cột và (b) không trích lại được cửa sổ rộng hơn, thì B mất lợi thế duy nhất của nó (cổng dữ liệu) → chuyển về A.

---

## 5. Ứng viên C — vị trí carbonyl hóa protein (K/R/P/T)

### Bài toán chính xác

**Vào:** chuỗi protein + một vị trí là K, R, P hoặc T. **Ra:** nhị phân, residue này có bị carbonyl hóa không. Quy ước của field là **bốn mô hình riêng, một cho mỗi loại residue**.

### Vì sao quan trọng

Carbonyl hóa protein là **modification oxy hóa không hồi phục kinh điển**; mất proteostasis và tổn thương oxy hóa đều là hallmark của lão hóa. Framing trung thực nhưng cần đúng một câu cẩn thận: **carbonyl hóa là một dấu hiệu tổn thương, không phải một aging clock**.

### Công trình trước, phân nhóm theo họ phương pháp

| Nhóm | Công trình | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. Đặc trưng thủ công + ML cổ điển** | CarSitePred, iCarPS — iCarPS đạt **AUROC 0,627–0,629** `[toàn văn]` | Đơn giản, baseline rõ | Hiệu năng thấp rõ rệt |
| **2. Deep learning + xử lý mất cân bằng** | PreCar_Deep 2021 — Borderline-SMOTE + deep learning `[chưa kiểm]` ([S0169743921001969](https://www.sciencedirect.com/science/article/abs/pii/S0169743921001969)) | Xử lý mất cân bằng tử tế | Không dùng PLM |
| **3. Attention + transfer learning** | SCANS 2025, *Advanced Science* 12(23):2500581 — AUROC **K 0,823 / P 0,885 / R 0,900 / T 0,881** trên tập test độc lập `[toàn văn]` | SOTA hiện tại, có GitHub và benchmark công bố | **Không dùng PLM + mCNN**, không dùng retrieval, không có SHAP → cả ba chỗ còn trống |

**Mức đông đúc:** khoảng **bốn predictor** trong cả dòng (CarSitePred → iCarPS → PreCar_Deep 2021 → SCANS 2025). Truy vấn PubMed `carbonylation site prediction` 2021–2026 trả **71 bản ghi** nhưng **bị lạm phát mạnh** vì "carbonylation" nở ra thành phản ứng carbonyl hóa trong hóa hữu cơ `[toàn văn — tự chạy]`.

### Dữ liệu — trạng thái truy cập đã thử

**CarbonylDB** `http://carbonyldb.missouri.edu/CarbonylDB/` → **HTTP 200** `[đã thử link]`; chứa **1.495 protein carbonyl hóa đã xác nhận thực nghiệm và 3.781 site carbonyl hóa** `[toàn văn]`. Residue âm/decoy trong SOTA lấy từ **BioLiP2 (29.992 protein có tương tác ligand)** `[toàn văn]`.

**Tập test độc lập: CÓ, đã công bố.** Site huấn luyện SCANS: **K 654, P 242, R 293, T 259**; site test độc lập: **K 323, P 114, R 145, T 124**. Repo `https://github.com/jianzhang-xynu/SCANS` → **HTTP 200** `[đã thử link]` ([PMC12199415](https://pmc.ncbi.nlm.nih.gov/articles/PMC12199415)).

### Trần hiệu năng — **và mâu thuẫn phải nêu rõ**

Đây là lý do C xuống hạng ba chứ không phải hạng một.

- **Bảng so sánh trích được từ bài báo** cho MCC trên **thang phần trăm: 17,612 / 16,980 / 27,644 / 23,403** tức **0,176–0,276**; F1 **10,924 / 10,903 / 14,627 / 13,156**; AUCPC **0,118 / 0,067 / 0,055 / 0,060**; đối thủ đứng đầu được nêu là **iCarPS** `[toàn văn]`.
- **Cùng bài báo, ở phần abstract/thân bài**, lại nói SCANS "records maximum **MCC values ranging from 0,712 to 0,779**" và cải thiện **2,8%–5,8%** so với phương pháp nhì là **CarSitePred** `[chưa kiểm]`.

Hai bộ số gần như chắc chắn là **hai setting đánh giá khác nhau** (cross-validated benchmark so với independent test có decoy từ ligand site), nhưng **không xác nhận được cái nào là cái nào**. **Không được trích một con số MCC duy nhất cho SCANS mà không nói rõ setting.** Và quan trọng hơn: **nếu bộ 0,712–0,779 là bộ của tập test độc lập, thì dư địa của C co lại rất nhiều.** Đây là **sự thật chưa kiểm có ảnh hưởng quyết định lớn nhất trong toàn bộ khảo sát** — phải giải quyết từ supplementary material hoặc GitHub của SCANS **trước buổi tuần 6**.

### Điểm theo năm tiêu chí

**Đạt cả 5/5 trên giấy:** (1) chưa có PLM+mCNN cho carbonylation; (2) cải tiến trực tiếp bằng mCNN/msCNN; (3) lớp retrieval chuyển trực tiếp được từ RAG-msCNN; (4) SCANS chỉ làm ablation + phân tích motif, còn chỗ cho SHAP/attribution, và BERT-Promoter là tiền lệ nội bộ; (5) web app rõ ràng. **Khả thi cao** — hàng trăm đến vài nghìn cửa sổ mỗi loại residue, embedding trên Colab free tính bằng phút đến giờ.

### Rủi ro và cổng dừng

**Cổng dừng duy nhất, và phải mở trước tuần 6: giải quyết mâu thuẫn MCC.** Nếu MCC thật trên tập test độc lập là 0,712–0,779 → **C rớt xuống dưới B**, vì khi đó bài toán đã gần bão hòa và sinh viên sẽ phải cạnh tranh với một SOTA mạnh mà không có lợi thế nào. Nếu là 0,176–0,276 → **C lên ngang A và B**, vì khi đó nó có cả tập test độc lập công bố, cả dư địa định lượng, cả framing aging trung thực.

**Rủi ro thứ hai:** chưa kiểm được repo SCANS **có thật chứa file benchmark hay không** — chỉ biết trang repo trả 200 `[đã thử link]`.

---

## 6. Ứng viên D — vị trí glycation lysine (dự phòng cho C)

Giữ đúng vai trò **dự phòng**: cùng hình dạng bài toán, cùng mức tái dùng code, và khoảng trống **sạch hơn** (không tìm được bất kỳ predictor glycation nào dùng ProtT5/ESM-2 + multi-window CNN), nhưng framing aging yếu hơn vì văn liệu thường đóng khung glycation là **đái tháo đường** nhiều như là **lão hóa**.

**Vào:** chuỗi + một vị trí lysine. **Ra:** nhị phân, có bị glycation không. Glycation sinh ra advanced glycation end products (AGEs), một cơ chế lão hóa và biến chứng đái tháo đường kinh điển.

**Dữ liệu:** CPLM `http://cplm.biocuckoo.cn/` → **HTTP 200** `[đã thử link]`. Nhiều tập test độc lập đã công bố: Glypre dùng **20 protein với 37 site glycation lysine** từ PLMD; BERT-Kgly dùng bộ **3.969 dương / 82.270 âm**, huấn luyện trên ~**3.573 dương cộng số âm tương đương**, với **tập test độc lập 200 dương + 200 âm**; một phương pháp RNN 2025 chia **4.830 huấn luyện / 1.000 validation nội bộ / 1.000 test độc lập** — tất cả `[chưa kiểm]` ([Glypre](https://doi.org/10.3390/molecules22111891), [BERT-Kgly PMC9580886](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9580886/), [PMC12436683](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436683/)).

**Trần hiệu năng:** PredGly (*Bioinformatics* 35(16):2749, 2019) báo **sensitivity 0,887 / specificity 0,899 / accuracy 0,893 / MCC 0,785** `[chưa kiểm]` ([Bioinformatics](https://academic.oup.com/bioinformatics/article/35/16/2749/5259189)). **Số của tập test độc lập của BERT-Kgly: không tìm được. Số của bài RNN 2025: không tìm được.** MCC 0,785 nghĩa là trần đã khá cao — đây là điểm yếu của D.

**Mức đông đúc:** thấp–trung bình, **năm predictor trong chín năm** (Gly-PseAAC 2016, Glypre 2017, PredGly 2019, BERT-Kgly 2022, RNN 2025).

**XAI có một lợi thế cụ thể:** tín hiệu theo vị trí đã biết — "abundance of alanine, valine, glycine, methionine upstream và downstream, trong khi lysine và arginine bị depleted ở các vị trí +1 đến +4" `[chưa kiểm]` — tức là đúng một câu chuyện window-feature mà mCNN khai thác được và SHAP giải thích được.

**Cách dùng:** nếu GVHD phản bác "carbonyl hóa có thật là aging không?", **D là món đổi, không phải thiết kế lại**.

---

## 7. Ứng viên E — benchmark senescence đã sửa (SenBench): mạnh nhất về bằng chứng, nguy hiểm nhất về định vị

Ứng viên này có **bằng chứng đã tự đo mạnh nhất trong toàn bộ khảo sát** và đồng thời là **cái bẫy lớn nhất**. Phải đọc cả hai mặt.

### Bài toán và công trình trước

SenSeqNet là bộ phân loại nhị phân mức toàn chuỗi (protein liên quan senescence hay không), dùng embedding `ESM-2_t33` (33 lớp, 650M tham số, 1280 chiều) mean-pool, đưa vào BiLSTM → CNN `[toàn văn]`. Bộ chỉ số công bố đầy đủ: **Accuracy 86,43%, Sensitivity 90,51%, Specificity 81,01%, F1 88,38%, MCC 0,7221, AUC 0,94** `[toàn văn]` ([PMC12724000](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724000/)).

Phân nhóm theo phương pháp cho nhánh này: **(1) dự đoán gene lão hóa bằng đặc trưng annotation/network** — Kerepesi et al. 2018 dùng **304 protein liên quan lão hóa từ GenAge (bản 18)** so với **19.879 protein không lão hóa từ Swiss-Prot**, rút ~21.000 đặc trưng xuống **36 đặc trưng nhị phân**, báo **AUC 0,9322**, accuracy 98,39% tại ngưỡng 0,24, **F1 0,46458, MCC 0,45641**, chỉ 5-fold CV lặp 20 lần **không có tập test riêng** `[toàn văn]` ([PMC5840292](https://pmc.ncbi.nlm.nih.gov/articles/PMC5840292/)) — **ưu điểm** là mạnh, **nhược điểm** là đặc trưng mạnh nhất lại là GO/pathway, tức **vòng tròn luận lý** đối với một task chỉ dùng chuỗi; **(2) PLM fine-tune cho protein lão hóa** — một chapter Springer 2026 fine-tune ESM2-t33 bằng LoRA trên **320 chuỗi GenAge + 320 chuỗi không lão hóa = 640**, sau tiền xử lý còn **160+160 huấn luyện và 34+30 test**, báo **accuracy 0,625, F1 0,700, ROC-AUC 0,743** `[chưa kiểm — trang 303-redirect về IdP Springer]` ([Springer chapter](https://link.springer.com/chapter/10.1007/978-3-032-13048-8_26)) — **đây là dấu hiệu cảnh báo rõ nhất trong toàn bộ khảo sát**: không phải chưa ai thử, mà là **tín hiệu chuỗi cho "protein này có liên quan lão hóa không" dường như yếu**; **(3) PLM + LSTM-CNN mức chuỗi** — chính SenSeqNet, không có đối thủ nào khác và **không tìm được bài nào trích dẫn nó** tính đến 02/10/2026.

### Bằng chứng tự đo — rất mạnh

Cơ chế biến vài trăm gene thành ~290.000 chuỗi đã được xác định: **truy vấn theo từng tên gene vào UniParc, không phải UniProtKB.** Header FASTA trong repo ghi nguyên văn `>Seq_uniparc_PEX19.xlsx_2`, `>Seq_TUBB4A共207条.xlsx_33`, `>Sequence_56_uniparc_CDK5R1_AND_database_facet_100_2024_11_26` `[tự đo]`. Grep `OS=` và `GN=` cho **không khớp nào** ở cả hai file v1 — provenance duy nhất còn lại là tên gene trong tên file và một chỉ số dòng `[tự đo]`. Bài báo công bố nói "UniProtKB" và **không bao giờ nhắc UniParc** `[toàn văn]`.

Số học chốt lại phê bình: CellAge Build 3 chỉ có **866 gene** từ genetic manipulation, trong đó chỉ **417 dòng / 370 gene riêng biệt là "Induces"** `[tự đo — tải `cellAge.zip` 21.540 byte, HTTP 200, đếm 949 dòng dữ liệu]`. SenSeqNet dùng **163 gene CellAge + 47 gene khác = 210 gene**. **292.759 chuỗi dương / 210 gene ≈ 1.394 chuỗi mỗi gene** `[tự đo]` — không gene người nào có 1.394 isoform. Mở rộng nhất thiết là ortholog xuyên loài và các mảnh từ UniParc.

Tập âm cũng có vấn đề: **không có cơ sở dữ liệu nguồn nào được nêu tên** — không HRT Atlas, không danh sách Eisenberg–Levanon, không trích dẫn nào `[toàn văn]`. 82 gene symbol thu hồi được từ FASTA là protein cấu trúc và tiết: VIM 4.694; TF 4.588; **IGH 4.520** (immunoglobulin heavy chain, 15,7% toàn bộ negatives); GH1 2.481; BPI 2.083; LEP 1.999; TNF 1.991 `[tự đo]`. Hai lớp khác nhau **theo họ protein**, không theo trạng thái senescence — dương bị chi phối bởi kinase và protein chu kỳ tế bào/DNA damage (SYK, AAK1, ATR, CDK5R1, CDC6, HIPK2, MOS, E2F7), âm bởi filament cytoskeleton, immunoglobulin, hormone tiết và protein ribosome. **ESM-2 tách hai nhóm đó gần như theo cấu tạo.**

Và một mâu thuẫn nhãn trực tiếp: **`ARPC1B` là gene dương trong tập huấn luyện và đồng thời là gene trong tập external negative** `[tự đo]`.

### Dữ liệu — trạng thái truy cập đã thử

Repo `https://github.com/HanliJiang13/SenSeqNet` → HTTP 200, public, repo id 877516477, `"private": false` `[tự đo]`. Bốn file v1 tải được **không cần đăng ký, không cần LFS**: `positive_0.4.fasta` 12.403.805 B / **24.914 chuỗi**; `negative_0.4.fasta` 13.355.846 B / **28.752 chuỗi**; `clustered_external_positive.fasta` 6.103.151 B / **16.524**; `clustered_external_negative.fasta` 2.230.618 B / **6.443** `[tự đo]`. Tổng khoảng **34 MB, tải trong vài giây**.

**Nhưng:** `Data_v2/Data_v2.zip` là **Git LFS pointer, kích cỡ khai báo 1.414.069.895 byte ≈ 1,41 GB**; `Data/Original_data/positive.zip` và `negative.zip` cũng là LFS pointer; embedding 150M và 650M (tức đúng mô hình bài báo báo cáo) cũng là LFS pointer `[tự đo]`. **Và repo không có LICENSE nào cả** — API license của GitHub trả **HTTP 404** `[tự đo]`, nghĩa là mặc định "all rights reserved". Nếu phân phối lại một bộ dữ liệu đã sửa thì **chỉ nên phát hành danh sách accession cộng script, không phát hành chuỗi**.

CellAge và GenAge thì sạch sẽ: `cellAge.zip` 21.540 B / **866 gene**; `human_genes.zip` 9.465 B / **307 gene người**; `models_genes.zip` 48.796 B / **2.205 gene sinh vật mô hình** — tất cả HTTP 200, không đăng ký `[tự đo]`. Giấy phép: "free but subject to the conditions of the Human Ageing Genomic Resources"; **tên giấy phép cụ thể: không tìm được** `[toàn văn phần release note, nhưng `legal.html` không trích được hết]`.

### Vì sao E nguy hiểm — ba cảnh báo, giữ nguyên, không làm nhẹ

**Cảnh báo 1 — đây chính là cái bẫy đã làm đề tài trước yếu.** Đóng góp dạng "chỉ ra giao thức đánh giá của bài trước có vấn đề" là **đúng trục đã khiến RTK–ATP mất tiêu chí 1–3**. Nếu chọn E thì **phần kiểm toán phải gói trong một chương, một bảng**, và **tên đề tài phải gọi tên phương pháp hoặc benchmark, không gọi tên việc kiểm toán**.

**Cảnh báo 2 — các con số trung thực sẽ ĐI XUỐNG.** Trên một split gom nhóm theo gene với hard negatives, accuracy có thể **rơi từ 86% xuống khoảng 60–70%**. Luận văn phải được đóng khung sao cho **một con số thấp hơn nhưng đáng tin là KẾT QUẢ, không phải thất bại** — và **phải thống nhất cách đóng khung này với GVHD TRƯỚC khi cam kết**. Một GVHD kỳ vọng "beat SOTA" sẽ không vui.

**Cảnh báo 3 — tín hiệu có thể thực sự yếu.** Văn liệu gene lão hóa cho thấy đặc trưng annotation/network chi phối, chuỗi đóng góp ít; chapter ESM2+LoRA đạt **accuracy 0,625 / AUC 0,743 trên một tập test 64 protein** `[chưa kiểm]`. Nếu AUC trên split gom nhóm đáp xuống gần 0,6 thì luận văn trở thành "chuỗi một mình không đủ cho dự đoán senescence, và đây là bằng chứng cộng một predictor có hiệu chuẩn và nhận biết miền áp dụng" — trung thực ở mức công bố được, **nhưng cần một GVHD chấp nhận kết quả âm**.

**Cổng dừng đã định lượng:** **nếu đến tuần 9 mà AUC trên split gom nhóm < 0,65, chuyển trọng tâm sang benchmark + web tool + XAI và bỏ hẳn khẳng định "cải thiện SOTA".**

**Một cảnh báo thêm về phạm vi bằng chứng:** mọi đo đạc rò rỉ ở trên là **chỉ trên bản v1**. Bộ v2 nằm sau một LFS object 1,41 GB chưa pull. **Không được tuyên bố trong buổi pitch rằng benchmark đã công bố bị rò rỉ**; chỉ được nói rằng **bản v1 phát hành chứng minh được là rò rỉ**, rằng **bản v2 chưa được kiểm**, và rằng **kiểm nó là việc ngày đầu tiên**. Rủi ro truy cập duy nhất là **quota bandwidth của Git LFS trên tài khoản GitHub miễn phí** — **thử `git lfs pull` trong giờ đầu tiên** `[chưa kiểm]`.

### Điểm theo năm tiêu chí

Hai tiêu chí là **lãnh địa chưa ai chiếm** trên benchmark này: SenSeqNet **không có XAI** (hạn chế do chính tác giả viết: *"a key limitation of this study is the model's interpretability, particularly in identifying biologically significant motifs within protein sequences"*) và **không có web application** — repo chỉ có package PyPI, một CLI và một notebook Colab `[toàn văn]`. Tiêu chí 2 có đường rõ: SenSeqNet **mean-pool thành một vector duy nhất rồi mới cho qua BiLSTM/CNN**, tức là **đã bỏ hết thông tin vị trí** — mCNN trên embedding theo từng residue là cải tiến hiển nhiên và GVHD sẽ nhận ra ngay. Tiêu chí 2 còn một đường mạnh hơn và **được chính khuyết điểm phát hiện ra thúc đẩy**: **huấn luyện bất biến theo họ gene** (một discriminator họ gene/Pfam với gradient-reversal layer, hoặc contrastive loss cân bằng theo họ), tức "benchmark cũ cho mô hình gian lận bằng cách nhận ra họ protein; đây là một mô hình bị cấm làm điều đó". Tiêu chí 1 thì **yếu một cách nghịch lý**: niche này có **đúng một người chiếm và không có bài nào trích dẫn** — vừa là cơ hội vừa là rủi ro, vì "tôi cải thiện SOTA" thành một so sánh một-bài, và GVHD có thể đọc một field một-bài là mỏng.

---

## 8. Ứng viên F — vị trí gắn nucleotide trên một họ protein liên quan ung thư

Giữ lại vì nó có **con số dư địa trung thực nhất trong cả báo cáo**, nhưng rủi ro định vị cao.

**Bài toán:** chuỗi + một vị trí → residue này có gắn ATP/GTP không. **SOTA PFDCNN** (*Sci Rep* 2025) dùng đặc trưng ESM-2, huấn luyện trên ATP-227 / ATP-388 / PATP-1930, test độc lập trên **ATP-17** và **ATP-41**: ATP-17 **AUC 0,965, Accuracy 0,990, Sensitivity 0,391, Specificity 0,997, Precision 0,642, MCC 0,497**; ATP-41 **AUC 0,941, Accuracy 0,984, Sensitivity 0,194, Specificity 0,999, Precision 0,857, MCC 0,403** `[toàn văn]` ([PMC12647579](https://pmc.ncbi.nlm.nih.gov/articles/PMC12647579/), code [PFDCNN](https://github.com/Yswangustb/PFDCNN)).

**Đọc kỹ sensitivity.** 0,391 và 0,194 nghĩa là **SOTA đã công bố bỏ sót 61–81% residue gắn ATP thật**. "Accuracy 0,990" là tiếng nói của mất cân bằng lớp, không phải của chất lượng. **Đây là một khoảng trống lớn, trung thực, định lượng được**, và nó phục vụ trực tiếp tiêu chí 2: một đề tài có mục tiêu công bố là "thu lại những dương tính mà SOTA bỏ sót, đo bằng MCC và recall thay vì accuracy" có một đích ngắm sẵn.

**Rủi ro định vị:** slice **RTK đã bị lấy** bởi RTK_RAG (nhóm Prof Ou, 2025) — nên phải chọn slice khác. Khảo sát chỉ ra công thức khớp nhất là **vị trí gắn GTP/GDP trong superfamily RAS, với KRAS/HRAS/NRAS làm móc ung thư**, vì GVHD đã có **hai bài về site GTP trên Rab GTPase (2019)** và **RAS cùng superfamily với Rab** `[toàn văn metadata]`. **Nhưng khảo sát KHÔNG tra được liệu đã có predictor site GTP/GDP nào cho superfamily RAS hay chưa** — đây là **việc tra cứu có giá trị cao nhất còn lại**, và chưa làm được.

**Đối thủ gần nhất chưa đọc được:** "Residue-Level Multiview Deep Learning for ATP Binding Site Prediction and Applications in Kinase Inhibitors" (PMID 39690486) — **chỉ xác nhận được tiêu đề/PMID, PubMed trả cookie wall** `[chưa kiểm]` ([PubMed 39690486](https://pubmed.ncbi.nlm.nih.gov/39690486/)). Tiêu đề của nó đồng thời chứng minh framing "ATP site → kinase inhibitor → ung thư" đã được field chấp nhận. **Đây là bài quan trọng nhất phải đọc nếu chọn F.**

**Một bài học từ ứng viên bị loại có điều kiện, phải nói ra:** phân loại họ efflux ABC đa kháng thuốc là **mức khớp GVHD cao nhất của mọi thứ trong báo cáo** — mCNN-GenEfflux (12/2025, *Comput Biol Chem*) **đúng là làm việc đó** `[toàn văn metadata]`, và ABCB1/ABCC1/ABCG2 là ba bơm efflux chính gây đa kháng thuốc ở tế bào ung thư `[chưa kiểm]`. Nhưng **không tìm được tập test độc lập nào cho bài toán phân loại họ ABC ở mức chuỗi**, và **chỉ có 49 protein ABC ở người** `[chưa kiểm]` — nên nó **rớt cổng dữ liệu**. Điều này cho một bài học chung đáng nói với GVHD: **"mức khớp GVHD tối đa" và "có benchmark cộng đồng" kéo về hai phía ngược nhau trong field này**, vì chính các bài của GVHD tự dựng split CD-HIT riêng thay vì dùng benchmark cộng đồng. Sinh viên phải biện minh cổng dữ liệu bằng **uy tín của dbPTM hoặc của ATP-17/ATP-41**, không bằng tiền lệ của GVHD.

---

## 9. Bảng so sánh toàn bộ ứng viên còn sống

| | **A. Site substrate SIRT** | **B. Site phospho theo nhóm kinase** | **C. Site carbonyl hóa** | **D. Site glycation** | **E. SenBench (senescence)** | **F. Site nucleotide, họ liên quan ung thư** |
|---|---|---|---|---|---|---|
| **Hướng** | aging | cancer | aging | aging (yếu hơn) | aging | cancer |
| **Mức residue?** | **Có** | **Có** | **Có** | **Có** | Không (toàn chuỗi) | **Có** |
| **Dữ liệu tải được hôm nay** | **Có, tự tải và đếm** `[tự đo]` | **Có** `[đã thử link]` | **Có** `[đã thử link]` | **Có** `[đã thử link]` | **Có, 34 MB v1** `[tự đo]`; v2 sau LFS 1,41 GB | **Có** `[đã thử link]` |
| **Tập test độc lập có sẵn** | **Không** — holdout 10% cùng microarray | **Có** — benchmark non-homologous theo nhóm kinase của dbPTM | **Có** — K 323 / P 114 / R 145 / T 124 | **Có** — 200+200; 1.000 | **Không** — external v2 chỉ một lớp; external v1 trùng 94,8% | **Có** — ATP-17, ATP-41 |
| **Trần SOTA trung thực** | **Precision MS 37–43%** | **Không tìm được** cho đúng setting này | **Mâu thuẫn: MCC 0,176–0,276 hay 0,712–0,779** | MCC 0,785 (PredGly 2019) | Acc 86,43%, nhưng **sẽ xuống 60–70% khi sửa split** | **Sn 0,391 / 0,194** — SOTA bỏ sót 61–81% |
| **Mức đông đúc** | Rất thấp (1 bài 2025, không có baseline neural) | **Thấp nhất** — 14 bài DL 2024–26 | Thấp — ~4 predictor | Thấp–TB — 5 predictor/9 năm | **Cực thấp nhưng nguy hiểm** — 1 bài, 0 trích dẫn | Rất thấp — 6 bài 2024–26 |
| **Khớp GVHD — phương pháp** | Cao | **Rất cao** | Cao | Cao | Cao | **Rất cao** (FAD ×2, ATP, GTP-Rab) |
| **Khớp GVHD — sinh học** | **Cao nhất** (sirtuin = lane duy nhất của thầy) | Không có bài | Không có bài | Không có bài | Gần aging nhưng khác task | Không có bài cancer |
| **Khả thi 8–9 tuần** | **Rất cao** | **Cao nhất** | Cao | Cao | Cao | Cao |
| **Tiêu chí đạt** | 1,2,3,4,5 — **XAI mạnh nhất** | 1,2,3,4,5 | 1,2,3,4,5 | 1,2,3,4,5 | 2,4,5 mạnh; **1 yếu, 3 trung bình** | 1,2,3,4,5 |
| **Web tool đối thủ** | **Không tồn tại cái nào sống** `[đã thử link]` | Có nhưng không theo nhóm kinase | SCANS có GitHub | AagingPEPred sống nhưng khác task | **Không có web app** | PFDCNN có GitHub |
| **Rủi ro lớn nhất** | Phải tự dựng tập test độc lập | Ý nghĩa cột benchmark + cửa sổ ±10 | **Mâu thuẫn MCC chưa giải** | Trần đã cao | **Bẫy kiểm toán + số đi xuống + tín hiệu có thể yếu** | Slice RTK đã mất; chưa tra RAS |

---

## 10. Danh sách loại bỏ, mỗi dòng một lý do

**Loại to tiếng — aging clock (DNA-methylation, proteomic, transcriptomic).** Phải nói rõ ràng chuyện này với GVHD, vì đây là thứ dễ được gợi ý nhất ("aging clock đang nóng"), và lý do nó rớt **không phải độ khó mà là hình dạng đầu vào**: clock ăn **một vector đo lường trên mỗi người** (beta value CpG, abundance protein huyết tương, transcript count) và nhãn là **tuổi thời gian của người đó** — **không có amino acid sequence nào ở đâu cả**. Toàn bộ lineage PLM → mCNN → RAG của GVHD **không áp dụng được về mặt kiến trúc**, nên **tiêu chí 2 và 3 không thể đạt**. Dữ liệu thì là cohort data sau đơn xin: DeepStrataAge huấn luyện trên **12.234 CpG site từ 29.167 người**; proteomic clock theo cơ quan dựng trên **UK Biobank n = 43.616** và validate ở Trung Quốc (n = 3.977) và Mỹ (n = 800) `[chưa kiểm]` ([npj Aging](https://www.nature.com/articles/s41514-026-00358-w), [Nature Aging](https://www.nature.com/articles/s43587-025-01016-8)). UK Biobank cần đơn được duyệt kèm phí và quá trình xét hàng tháng — **không thể nằm trong cửa sổ 8–9 tuần**. Cách dùng duy nhất đúng của clock trong luận văn này là **làm framing ở phần mở đầu** ("lão hóa đo được; đây là phía tổn thương phân tử của nó"), không phải làm task.

**Loại — nhánh neoantigen, và lý do khớp kém không phải vì khó.** Cổng dữ liệu thì **qua được, nhưng chỉ qua một cửa duy nhất**: ma trận harmonized của Immunity 2023 trên figshare (ba link đều trả **HTTP 202, resolve, không cần login**) cộng các file TrainingSet/TestingSet của Gartner `[đã thử link]`. Nhưng bốn cổng khác thì rớt:
- **Cổng định vị.** Nước đi kiến trúc hiển nhiên — PLM + multi-window scanning CNN cho neoantigen — **đã được chính nhóm Prof Ou công bố**: DeepNeoAG (2024, *Int J Biol Macromol*, **12 trích dẫn**, trong đó **11 là review hoặc không liên quan**) và NeoGen-BC (**công bố 09/09/2026, 0 trích dẫn, closed access, không có code công khai**) `[đã thử link — Semantic Scholar API]`. Pitch một đề tài neoantigen trong họ phương pháp này vào tháng 10/2026 là **đọc lại abstract của NeoGen-BC cho một giáo sư đồng tác giả thường xuyên với tác giả cuối của NeoGen-BC**.
- **Cổng hướng dẫn.** GVHD **không có bài cancer/tumour/neoantigen nào**. Sinh học MHC class I/II, nhận diện tế bào T, và điều gì làm một nhãn immunogenicity đáng tin — đó đúng là chỗ sinh viên cần người hướng dẫn nhất, và đúng là chỗ GVHD không cung cấp được.
- **Cổng đóng góp giao thức — đã bị chiếm hoàn toàn.** Immunity 2023 (Müller et al.) đã **reprocess WES/RNA-seq từ 120 bệnh nhân ngoài cộng 11 bệnh nhân nội bộ = 131 người**, xác định **46.017 đột biến SNV somatic và 1.781.445 neo-peptide, trong đó 212 đột biến và 178 neo-peptide là immunogenic**, rồi phát hành ma trận mở với mục đích tự tuyên bố là *"homogenized datasets valuable for developing and benchmarking companion algorithms"* `[abstract]` ([PubMed 37816353](https://pubmed.ncbi.nlm.nih.gov/37816353/)). Một pitch "harmonize dữ liệu và so sánh phương pháp công bằng" ở đây sẽ bị đọc là **chạy lại `bash train_classifier.sh`**.
- **Cổng chỉ số.** Trên benchmark sạch ITSNdb, **bảy predictor đã công bố có ROC AUC từ 0,52 đến 0,60**, với **chỉ 7 neoantigen được cả bảy phương pháp cùng dự đoán là immunogenic**, và phương pháp xếp hạng tốt nhất theo average rank (DeepHLApan) **tạo ra 100% (297) false positive trên TESLA** `[toàn văn]` ([Front Immunol 1094236](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1094236/full)). Trong khi đó các bài tự curate báo 0,81–0,905. **Sinh viên không thể biết mình đang cạnh tranh với con số nào, và reviewer cũng không.** Mọi framing "beat SOTA" ở đây là bẫy.

Có **đúng một chỗ còn mở** trong nhánh này, nói ra để công bằng: các negative ở mọi dataset là "chưa được chứng minh là immunogenic", không phải "đã được chứng minh là không immunogenic" (chính tập validation của ITSNdb có **113 trong 120 negative thiếu xác nhận binding**) `[toàn văn]`, tức là bài toán **positive-unlabelled learning mà cả field đang xử lý như phân loại nhị phân có giám sát** — và khảo sát **không tìm được bài nào trong nhánh này đóng khung nó là PU learning**. Đó là một ý tưởng thật, nhưng nó không cứu được bốn cổng trên.

**Phần còn lại, mỗi dòng một lý do:**

| Bị loại | Lý do một dòng |
|---|---|
| Phân loại họ/isoform sirtuin | **Đã bị chiếm bởi chính GVHD trong năm nay** (SirtSAGE), và dữ liệu DeepSIRT mất (host `140.138.155.216` time out cả hai đường `[đã thử link]`) |
| Dự đoán site gắn NAD+ | Nhóm Prof Ou đã làm, **AUC 0,9733 cho sirtuin người và 0,9701 cho enzyme deacylation khác** `[abstract]` — gần bão hòa, và server down nên không so sánh công bằng được |
| Phân loại protein autophagy | **Không còn dư địa** — PLM-ATG đạt **Acc 99,5%, MCC 0,990, AUC 0,9998** trên tập test 100+100 `[toàn văn]`, và nó **đã dùng ESM-2 cộng SHAP**, tức đã chiếm luôn tiêu chí 3 và 4. Chỉ còn đường "kiểm toán rò rỉ" — **đúng cái bẫy cũ** |
| Peptide chống lão hóa | **AUC độc lập đã 0,99** trên **40 chuỗi** `[toàn văn]`; peptide 2–80 aa nên **không có bài toán cửa sổ nào để giải** |
| Vùng dễ kết tụ / amyloidogenic | **Đông nhất trong các lựa chọn mức residue** — ≥6 bài 2025–2026, và **AggrescanAI đã dùng đúng ProtT5 ở mức residue** `[chưa kiểm]` |
| Motif LIR/AIM (autophagy) | Hấp dẫn về trí tuệ nhưng **không có tập test độc lập**, positive chỉ vài trăm motif, và baseline trung thực là AF2-Multimer — **không chạy được ở quy mô trên Colab free** |
| Định vị dưới mitochondria | Bị siết từ hai phía: Mito-Mixer 2026 **đã là multi-scale trên ESM-2 đông lạnh** (GCC 0,6945 trên M983) `[chưa kiểm]`, và nhóm Prof Ou đã có MCNN_MC (PLM+CNN, mitochondrial carriers, JCIM 2024) `[toàn văn metadata]` |
| Dự đoán gene/protein lão hóa (GenAge) | **Không có split nào trong bất kỳ archive HAGR nào** `[tự đo]`, và kết quả chuỉ-dùng-chuỗi tốt nhất là **accuracy 0,625 / AUC 0,743 trên tập test 64 protein** `[chưa kiểm]` — rủi ro kết quả âm không công bố được hoặc kết quả vòng tròn luận lý |
| Senolytic / CR mimetic (phân tử nhỏ) | **Loại vì khớp phương pháp, không vì chất lượng** — SMILES/cheminformatics, không có PLM, không có mCNN → **chỉ đạt tiêu chí 1 và 5** |
| SASP | **Không tồn tại benchmark mức chuỗi nào** — mọi nguồn SASP là proteomic hoặc transcriptomic |
| Telomere / telomerase | Không có benchmark; công trình sequence-ML duy nhất là từ **2008** |
| Klotho / mTOR / AMPK / IGF1 | Không có benchmark chuỗi riêng; "protein này có trong pathway mTOR không" sụp thành dự đoán chức năng tổng quát |
| Protein sửa chữa DNA | Chỉ có network-based; task lân cận có benchmark (DNA-binding protein, PDB14189/PDB2272/PDB186) là **sinh học khác và đã bão hòa** |
| Progeria / laminopathy | **Không tìm được** benchmark nào — nhưng **đã tra rất nông**, độ tin cậy thấp |
| TCR–pMHC binding | Benchmark IMMREP22/23 tuyệt vời, nhưng **kết luận công bố của chính field là mô hình không tổng quát hóa cho peptide chưa thấy**, và các entry tốt nhất ở IMMREP23 cần modelling cấu trúc — **vượt ngân sách compute** |
| MHC class II presentation | Khả thi về dữ liệu (IEDB export HTTP 200 `[đã thử link]`) nhưng **đó là lane neoantigen của Prof Ou**, chính chỗ sinh viên đang muốn rời |
| Driver vs passenger gene; oncogene vs TSG | **Các danh sách gold-standard CHÍNH LÀ nhãn** → không có tập test độc lập; N chỉ vài trăm gene; TP53 là "oncogene in disguise" → nhiễu nhãn nội tại `[chưa kiểm]` |
| ΔΔG nhiễu loạn PPI | SKEMPI 2.0 **khóa theo cấu trúc**; làm từ chuỗi thì bỏ mất tín hiệu, làm với cấu trúc thì vượt compute; và là regression chứ không phải phân loại cửa sổ |
| Synthetic lethality | Link prediction trên đồ thị cặp gene, không tái dùng được gì ở mức residue, và **9.322 trong 35.913 positive của SynLethDB 2.0 tự là dự đoán tính toán** `[chưa kiểm]` |
| Phân loại subtype ung thư | Sai modality (bulk omics), và các tầng có giá trị lâm sàng là controlled-access |
| DTI / drug response trong oncology | **240 bản ghi PubMed 2024–2026** `[toàn văn — tự chạy]` — đông nhất trong mọi task; và URL bulk download của GDSC trả **HTTP 410 Gone** `[đã thử link]` |
| Kinase inhibitor selectivity | Tín hiệu nằm trong **phân tử**, không trong chuỗi protein; rời hẳn họ phương pháp của GVHD |
| Variant effect / ProteinGym clinical | **Benchmark độc lập tốt nhất trong cả báo cáo** (clinical zip 123 MB) nhưng **khớp GVHD thấp nhất** — thầy không có bài variant effect nào, output head khác, và nó **bỏ đi phần lớn tài sản giao thức kiểm soát rò rỉ** sinh viên đã có |
| Phân loại họ efflux ABC | **Khớp GVHD cao nhất của mọi thứ** (mCNN-GenEfflux đúng là việc này) nhưng **không tìm được tập test độc lập** và chỉ có **49 protein ABC ở người** — giữ làm case study trong web app, **không làm benchmark chính** |

**Một mẫu hình xuyên suốt, đáng nói với GVHD trong một câu:** những nhánh aging mà sinh học là **một trạng thái tế bào hoặc tư cách thành viên pathway** (SASP, senescence, protein pathway, gene longevity) **không cho ra task chuỗi tốt**, vì nhãn không được mã hóa trong chuỗi. Những nhánh mà sinh học là **một sự kiện tổn thương hoặc gắn kết phân tử** (carbonylation, glycation, aggregation, gắn ATP/NAD, deacetyl hóa bởi một enzyme cụ thể) **thì có**, vì nhãn là hóa học cục bộ. Pipeline cửa sổ-residue sẵn có của sinh viên khớp với nhóm thứ hai, không khớp nhóm thứ nhất.

---

## 11. Hướng dẫn xuyên suốt cho tiêu chí 3, 4 và 5

Phần này độc lập với việc chọn ứng viên nào — áp dụng cho A, B, C, D, F như nhau.

### 11.1. Tiêu chí 3 — "xa hơn PLM": bốn lựa chọn an toàn, và một lựa chọn phải tránh

Tính mới ở đây là **tương đối so với nhóm này**, và nhóm đã lấy hai nước đi hiển nhiên nhất: **graph attention trên cấu trúc AlphaFold có cổng pLDDT** (SirtSAGE, 2026) và **retrieval augmentation** (RAG-msCNN, RTK_RAG). Đề xuất một trong hai làm "phương pháp mới" ở tuần 6 sẽ nhận câu trả lời "chúng tôi đã làm rồi".

**Xếp theo tỉ lệ (mới-cho-nhóm-này ÷ công sức), tốt nhất trước:**

1. **Thay embedding ProtT5 đông lạnh bằng PLM nhận biết cấu trúc (ProstT5 hoặc SaProt).** Đây là **đúng bước tiếp theo trong chính lập luận lịch sử của GVHD** (PSSM → PLM → ?). SaProt huấn luyện trên "approximately 40 million protein sequences and structures" với **từ vựng nhận biết cấu trúc kết hợp token residue với token 3Di từ Foldseek**, công bố ICLR 2024 `[chưa kiểm]` ([ICLR 2024 PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/1c42513b8895ab11fbbb5b7e8e6b6b02-Paper-Conference.pdf), [code](https://github.com/westlake-repl/SaProt)). ProstT5 là "a bilingual language model for protein sequences and structures" dịch được giữa chuỗi amino acid 1-D và chuỗi 3Di 1-D `[chưa kiểm]`. **Độ khó kỹ năng ≈ 0** — chỉ là một lời gọi `AutoModel` khác đưa vào đúng window-CNN cũ. **Rủi ro chính là nó không cải thiện chỉ số** — và điều đó **vẫn ổn, thậm chí tốt**: với giao thức kiểm soát rò rỉ của sinh viên, một kết quả âm được thực hiện tử tế ("token nhận biết cấu trúc không giúp gì khi đã kiểm soát đồng dạng") là một đóng góp khoa học bảo vệ được.
   **CẢNH BÁO CHƯA GIẢI, phải kiểm trước tuần 6:** **SaProt có cần một cấu trúc 3D ở thời điểm inference hay không** (token 3Di của Foldseek được dẫn XUẤT TỪ một cấu trúc). Nếu có, nó thừa hưởng đúng vấn đề triển khai của đường GNN, còn hướng dịch chuỗi→3Di của ProstT5 thì có thể không. **Đây là điểm quyết định xem khuyến nghị này có đứng được hay không** `[chưa kiểm]`.
2. **Đầu KAN thay đầu dense của mCNN.** Rẻ (`pykan`/`efficient-kan`, vài trăm dòng), **đã chứng minh công bố được đúng trong niche PTM-site** (CaLMPhosKAN, đầu KAN dựa trên wavelet, *Bioinformatics* 41(4):btaf124) `[chưa kiểm]`, và **đồng thời cung cấp luôn tiêu chí 4** qua phân tích hàm cơ sở ký hiệu. IKANbind làm đúng điều đó: dùng các hàm ký hiệu **sin(πx), cos(πx), tanh(πx), x, x²** thay B-spline mờ đục, cho phép "basis function weight analysis"; và nó đạt **AUC 0,916 so với 0,906 của ATMGBs trên DNA-180-Test, AUPR 0,526 so với 0,491, F1 0,508 so với 0,489** `[toàn văn]` ([btag433](https://academic.oup.com/bioinformatics/article/42/7/btag433/8712719), [code](https://github.com/yangfengzhuguet/IKANBind)). **Lưu ý chiến lược:** KAN cũng là thành phần XAI của chính SirtSAGE, nên phải đóng khung là *chuyển sang một bài toán mức residue*, không phải phát minh.
3. **Conformal prediction cho cổng miền áp dụng có bảo đảm hình thức.** Chuyển "identity làm tín hiệu miền áp dụng" — ý tưởng tốt duy nhất mang được từ đề tài RTK–ATP cũ — thành một phương pháp **có bảo đảm**: conformal prediction cho một cách data-driven để tìm ngưỡng sao cho **false discovery rate trên dữ liệu test thấp hơn một giới hạn trên do người dùng chỉ định** `[chưa kiểm]` ([Nat Commun](https://www.nature.com/articles/s41467-024-55676-y), [PMC11164347](https://pmc.ncbi.nlm.nih.gov/articles/PMC11164347/)). Split-conformal calibration là khoảng **50 dòng**, không có deep learning mới, compute không đáng kể — và nó **cấp nguồn trực tiếp cho banner cảnh báo của web app**, tức tiêu chí 3 và 5 cùng lúc.
4. **LoRA/PEFT thay vì embedding đông lạnh.** Mới so với nhóm này (họ đông lạnh). Có biện minh ở tầm *Nature Communications* ("Fine-tuning protein language models boosts predictions across diverse tasks") và **một ví dụ tham chiếu đúng cho binding-site prediction** `[chưa kiểm]` ([bioRxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full.pdf), [s41467-024-51844-2](https://www.nature.com/articles/s41467-024-51844-2)). Khả thi trên T4 free với checkpoint 35M/150M; checkpoint 650M với LoRA là **biên giới trên 16 GB** và cần gradient checkpointing cùng batch nhỏ. Dự trù **1–2 tuần** `[tự ước lượng]`.

**TRÁNH làm phương pháp chính — GNN trên cấu trúc AlphaFold.** Ba lý do cộng lại: (a) đó là **phương pháp mới nhất của chính nhóm**, nên không mới với họ; (b) đó là **khoảng trống kỹ năng lớn nhất của sinh viên** — với người chưa từng train GNN, dự trù **2–3 trong 8–9 tuần** chỉ để đạt một baseline đáng tin (ngữ nghĩa batching của PyTorch Geometric, quy ước `edge_index`, readout mức node so với mức graph, mất cân bằng lớp ở mức residue) `[tự ước lượng]`; (c) **nó phá web app**: nếu mô hình cần cấu trúc thì app **không nhận được FASTA dán tùy ý** — hoặc chỉ tra được protein đã biết trong AlphaFold DB, hoặc phải chạy ESMFold (quá nặng cho hosting miễn phí), hoặc tụt xuống "chỉ nhận accession". **Đây là xung đột trực tiếp với tiêu chí 5 và phải nêu với GVHD ở tuần 6.** Giữ GNN làm **nhánh so sánh dự phòng** nếu còn thời gian, và **nhắc nó ở tuần 6 để cho thấy mình biết SirtSAGE**.

Nếu vẫn muốn một nhánh cấu trúc: **tải cấu trúc, đừng dự đoán.** AlphaFold DB cho bulk download qua FTP `ftp://ftp.ebi.ac.uk/pub/databases/alphafold`, một REST API cho từng accession, và một bucket Google Cloud **khoảng 23 TiB** (CC-BY-4.0, `gs://public-datasets-deepmind-alphafold-v4`); pLDDT là **một số 0–100 cho mỗi residue**, nằm trong field B-factor của mmCIF/PDB hoặc trong `confidence_v4.json` `[chưa kiểm]` ([NAR 50(D1):D439](https://academic.oup.com/nar/article/50/D1/D439/6430488), [afdb README](https://github.com/google-deepmind/alphafold/blob/main/afdb/README.md)). **Không tải bucket 23 TiB** — với vài nghìn accession, lấy từng file: **khoảng vài GB và vài giờ tải tuần tự lịch sự** `[tự ước lượng]`. Và phải **báo cáo tỉ lệ coverage** — không phải accession nào cũng có entry AlphaFold (isoform, protein rất dài, chuỗi không thuộc reference) — đây đúng là thứ nhóm GVHD sẽ kiểm.

**Tránh hẳn:** Mamba/Hyena, mixture-of-experts, EGNN, sparse autoencoder làm phương pháp chính — tiền lệ mỏng hoặc không có trong niche này, learning curve cao nhất, và không tái dùng được tài sản nào của sinh viên. Riêng **mixture-of-experts và Hyena trong dự đoán mức residue của protein: không tìm được bài nào.**

### 11.2. Tiêu chí 4 — XAI: một đóng góp XAI đáng tin trông như thế nào, cụ thể

**Trước hết, một tin tốt về chính tiền lệ của GVHD.** BERT-Promoter (2022) dùng SHAP **như một bước chọn đặc trưng, không phải để giải thích sinh học**. Abstract nói nguyên văn: SHAP *"served as a feature selection step to look at the top-rank BERT encodings"*, rồi "different machine learning classifiers were implemented to learn the top features" `[abstract — metadata PubMed nguyên văn]` ([DOI 10.1016/j.compbiolchem.2022.107732](https://doi.org/10.1016/j.compbiolchem.2022.107732)). Hiệu năng báo cáo: **accuracy 85,5% và 76,9%** cho hai tầng (promoter vs non-promoter; strong vs weak). **Nghĩa là: sinh viên vượt được tiền lệ của chính GVHD chỉ bằng cách làm giải thích hậu nghiệm có xác nhận sinh học** — vì tiền lệ không làm điều đó. Đây là cách an toàn về mặt chính trị để đạt tiêu chí 4 mà không hàm ý công trình của thầy thiếu sót. Ngược lại, **chạy lại "SHAP để chọn đặc trưng" sẽ bị thầy đọc ngay là lặp lại**.

**Ba nước đi đáng tin, xếp theo tỉ lệ (sức nặng ÷ chi phí):**

**Nước đi 1 — attribution đối chiếu định lượng với annotation độc lập.** Đây là nước đi rẻ nhất và đáng tin nhất. Copy đúng động tác của ESM2_AMP nhưng ở mức residue: tính attribution theo từng residue (integrated gradients hoặc SHAP GradientExplainer) trên tập test, rồi **đo mức làm giàu (enrichment) của các vị trí attribution cao bên trong các feature chức năng do UniProt annotate (Domain, Region, Motif, Active site, Binding site, Compositional bias)** so với một baseline ngẫu nhiên khớp vị trí. Đầu ra là **một con số cộng một đường cong**, chi phí gần như bằng không, và **so sánh trực tiếp được với con số đã có trong văn liệu**: ESM2_AMP báo rằng "higher attention weights were observed for end segments" và **ba segment có attention cao nhất bao phủ khoảng 54,78% vùng amino acid chức năng (Domain, Region, Compositional bias, Repeat, Motif) trong các ca true-positive** `[toàn văn]` ([bbaf434](https://academic.oup.com/bib/article/26/4/bbaf434/8242608)). Điều làm nó thành **bằng chứng chứ không phải lập luận vòng tròn** là annotation **độc lập với nhãn huấn luyện**.

**Nước đi 2 — dùng attribution để biện minh một quyết định thiết kế.** Đây là mẫu LMCrot, và nó **biến XAI từ trang trí thành một đóng góp phương pháp**, tức nuôi luôn tiêu chí 2. LMCrot (ProtT5-XL-UniRef50 + ensemble CNN/BiLSTM cho site crotonylation) dùng **attention weight chuẩn hóa từ block cuối của encoder ProtT5, lấy trung bình trên các head**, vẽ heatmap; với protein **O00244** nó cho thấy attention đáng kể vào các residue **xa nhau trên chuỗi nhưng cách nhau 7,83 Å trong không gian**, và tác giả dùng đúng điều đó để **biện minh việc đưa toàn chuỗi vào thay vì chỉ một cửa sổ peptide**; kết luận sinh học được phát biểu là *"relying exclusively on peptide sequences might fail to capture the association of distant residues affecting the site"* `[toàn văn]` ([btae290](https://academic.oup.com/bioinformatics/article/40/5/btae290/7658304)). Hiệu năng của nó, để tham chiếu: trên HeLa dataset **MCC 0,699, AUROC 0,922**, so với DeepCap-Kcr **MCC 0,650, AUROC 0,906** (cải thiện MCC ~7,6%); trên protein không phải histone **cải thiện MCC 14,8% so với CapsNh-Kcr** `[toàn văn]`. **Phiên bản của sinh viên:** "khối lượng attribution nằm ngoài cửa sổ ±w là X%, do đó thiết kế multi-window với cửa sổ ngoài rộng hơn là chính đáng".

**Nước đi 3 — giải thích chính các ca thất bại và miền áp dụng.** Đây là nước đi riêng của sinh viên này, vì nó dựa trên chuyên môn kiểm soát rò rỉ đã có: **so sánh pattern attribution trên protein test có identity cao so với identity thấp**. Nếu attribution của mô hình sụp xuống vài vị trí khi gặp protein identity thấp, đó là một **lời giải thích cơ chế trung thực, công bố được, cho VÌ SAO hiệu năng giảm khi kiểm soát rò rỉ**. **Khảo sát không tìm được bài nào làm đúng điều này** — vừa là cơ hội vừa là rủi ro: hãy coi đó là **tính mới chưa xác nhận** và tra lại trước khi tuyên bố.

**Chi phí tính toán — thứ tự quan trọng hơn con số.** Với embedding đã đông lạnh và nằm trên disk (đúng setup hiện tại của sinh viên), SHAP GradientExplainer hoặc Captum integrated gradients trên một window-CNN nhỏ là việc **tính bằng phút** cho vài trăm cửa sổ test trên một T4, vì mỗi bước attribution chỉ chạm vào đầu CNN, không chạm vào PLM 650M tham số `[tự ước lượng]`. Attribution **xuyên qua PLM** (tức gán cho amino acid thay vì cho chiều embedding) cần gradient qua ProtT5/ESM-2, khoảng (số bước tích phân, thường 20–50) × (một forward+backward của PLM) cho mỗi chuỗi — khả thi cho **hàng chục đến trăm chuỗi**, không khả thi cho cả dataset; **hãy lên kế hoạch một tập case study, không phải chạy toàn bộ tập test** `[tự ước lượng]`. Saturation mutagenesis đầy đủ là **19 × L forward** cho mỗi protein; với L=400 là **7.600 forward cho MỘT protein** — **đừng làm điều này xuyên PLM trên free tier**; giới hạn vào cửa sổ ±15 quanh site dự đoán (≈ 19 × 31 ≈ **589 forward mỗi site**) hoặc làm mutagenesis chỉ trên đầu CNN bằng thay thế trong không gian embedding `[tự ước lượng]`. **Tránh hẳn KernelExplainer** — nó là biến thể SHAP duy nhất thực sự nguy hiểm với một deadline ("computes approximate values in exponential time"), và không có gì trong subfield này đòi nó; bài tiền lệ LMCrot dùng GradientExplainer `[chưa kiểm]`.

**Ba kiểm tra phòng vệ, mỗi cái tốn giờ chứ không tốn ngày, biến "chúng tôi vẽ một đồ thị SHAP" thành một mục XAI bảo vệ được** `[tự ước lượng]`: (1) **kiểm tra sanity bằng ngẫu nhiên hóa mô hình** — tính lại attribution với trọng số khởi tạo ngẫu nhiên; nếu pattern vẫn sống thì phương pháp đang đọc input chứ không đọc mô hình; báo độ tương tự; (2) **sự đồng thuận giữa hai phương pháp độc lập** (integrated gradients so với SHAP GradientExplainer so với occlusion/ISM) — báo rank correlation của điểm theo residue; **bất đồng tự nó là một phát hiện trung thực đáng báo**; (3) **đường cong faithfulness deletion/insertion** — mask k residue attribution cao nhất và đo mức tụt dự đoán so với mask residue ngẫu nhiên.

**Kỷ luật ngôn từ, bắt buộc.** Có một văn liệu đáng kể cho thấy attribution map có thể **trông hợp lý mà không trung thực**: "certain saliency methods may produce visually plausible explanations even when model parameters are randomized" `[chưa kiểm]` ([PMC10831517](https://pmc.ncbi.nlm.nih.gov/articles/PMC10831517/)); "Saliency maps do not necessarily indicate the true causes of predictions" `[chưa kiểm]` ([arXiv 2008.02766](https://arxiv.org/pdf/2008.02766)); và sự tương đương filter↔motif thì yếu — "Only several best-recovered motifs can be equated to true motifs, as most kernels act during training to increase generalization ability, with such auxiliary kernels producing noise" `[chưa kiểm]`. Nên: **nói** "các vị trí attribution cao được làm giàu trong vùng chức năng đã annotate (X% so với baseline Y%)"; **không nói** "mô hình đã phát hiện ra motif gắn kết" hay "mô hình đã học được cơ chế".

### 11.3. Tiêu chí 5 — web app: thay đổi chính sách 2026 của Hugging Face và số học bộ nhớ của PLM

**Thay đổi chính sách phải biết trước, không phải phát hiện ở tuần 14.** Tài liệu chính thức của Hugging Face ghi nguyên văn: *"Static Spaces are free for everyone. **Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organizations.** Free personal accounts in good standing can still host up to **2 Gradio Spaces running on ZeroGPU**."* `[toàn văn]` ([HF Spaces overview](https://huggingface.co/docs/hub/en/spaces-overview)). Cùng trang: mỗi môi trường Space mặc định giới hạn **16 GB RAM, 2 CPU core và 50 GB disk KHÔNG bền vững**; hardware **CPU Basic 2 vCPU / 16 GB là FREE**; CPU Upgrade 8 vCPU / 32 GB **$0,03/giờ**; T4-small **$0,40/giờ**; L4 **$0,80**; A10G-small **$1,00**; A100-large **$2,50**. Trên hardware miễn phí Space sẽ **"go to sleep"** sau một thời gian không dùng. Networking chỉ mở port 80, 443 và 8080. Có thể **xin community GPU grant** từ tab Settings `[toàn văn]`. *(Nhiều nguồn thứ cấp vẫn nói Spaces đơn giản là miễn phí, và con số "sleep sau 48 giờ" chỉ xuất hiện ở nguồn thứ ba — **tài liệu chính thức mới là nguồn có thẩm quyền về yêu cầu paid plan, và con số 48 giờ là chưa xác nhận** `[chưa kiểm]`.)*

**Số học bộ nhớ, nói thẳng ra để không phải phát hiện muộn** `[tự ước lượng]`:

| Mô hình | Trọng số ở fp32 | Vừa Streamlit Community Cloud? | Vừa HF Spaces CPU Basic (16 GB)? |
|---|---|---|---|
| ESM-2 **8M** (embed 320) | ~32 MB | Vừa | Vừa |
| ESM-2 **35M** (embed 480) | **≈ 140 MB** | **Vừa** | Vừa |
| ESM-2 **150M** (embed 640) | **≈ 600 MB** | **Vừa, sát** | Vừa |
| ESM-2 **650M** (embed 1280) | **≈ 2,6 GB** (650M × 4 byte) + activation | **VƯỢT hẳn** | Vừa nhưng phải cẩn thận, và chạy chậm trên CPU |
| **ProtT5-XL (~3B)** | — | **Không** | **Không servable trên bất kỳ free tier nào ở fp32** |

Trần của Streamlit Community Cloud được báo là **CPU 0,078–2 core, bộ nhớ 690 MB–2,7 GB, storage tối đa 50 GB** `[chưa kiểm — từ tóm tắt thứ cấp của docs Streamlit, phải tự xác minh]`. Nghĩa là: **ESM-2 650M và ProtT5-XL không thể serve trên Streamlit Community Cloud.**

**Một điều đáng khích lệ, để việc chọn checkpoint nhỏ không thành một sự nhượng bộ khoa học:** có báo cáo rằng **"The ESM-2 model with 150M parameters performs better than the ESM-1b model with 650M parameters"** `[chưa kiểm]` ([bioRxiv 2022.07.20.500902](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v1.full.pdf)).

**Yêu cầu của một web tool dự đoán đáng tin — dùng editorial của NAR Web Server Issue làm tài liệu đặc tả.** Số 2025 là số thường niên thứ 23, *Nucleic Acids Research* 53(W1), 07/07/2025, gồm **72 server**. Yêu cầu minh thị `[toàn văn]` ([NAR 53(W1):W1](https://academic.oup.com/nar/article/53/W1/W1/8176964)): server phải **"free and open-access"**, từ chối việc yêu cầu thanh toán hoặc đăng ký thẻ; *"[cloud servers] usually require users to log in—and that is something that we do not allow"*; tài liệu là **bắt buộc** và phải nói về "the underlying data and, most importantly, **the limitations of the system**"; mục tiêu cốt lõi là phục vụ "researchers who do not want to use the command line"; từ chối server đòi tiền xử lý nặng phía người dùng hoặc trả ra "plain text outputs without contextual information"; kết quả phải có **filtering và sorting** cùng link ra ngoài; và tác giả được kỳ vọng **tiếp tục bảo trì server lâu sau khi công bố**. Editorial **không quy định framework nào** — nên React + FastAPI của sinh viên là chính đáng, và với một khoa Kỹ thuật phần mềm **có thể còn ăn điểm hơn một trang Gradio**.

**Thứ tự build, để nếu dừng sớm vẫn còn thứ demo được** `[tự ước lượng]`: (1) dán FASTA + **một nút Example** (tính năng giá trị cao nhất khi demo trước GVHD hoặc hội đồng); (2) chạy → bảng điểm theo residue, **sort và filter được**; (3) một hình: track/lollipop điểm theo residue dọc chuỗi, highlight site dự đoán; (4) **tải CSV và JSON**; (5) **banner miền áp dụng**: hiện max sequence identity của query so với tập huấn luyện cộng mức risk đã hiệu chuẩn bằng conformal, kèm chữ nói rõ dự đoán ngoài miền áp dụng là không đáng tin; (6) upload file FASTA + batch mode; (7) **panel XAI**: attribution theo residue overlay lên track điểm, cộng hình enrichment attribution-vs-annotation — **đây là chỗ tiêu chí 4 trở thành tính năng người dùng thấy được chứ không nằm chôn trong báo cáo**; (8) **trang Limitations**.

**Ước lượng thời gian build** `[tự ước lượng — không có nguồn]`: Gradio một file `app.py` trên HF Spaces **1–2 ngày** (nhanh nhất, nhưng bị chặn trừ khi ngoại lệ ZeroGPU áp dụng); Streamlit trên Community Cloud **2–4 ngày** (thật sự miễn phí nhưng buộc dùng mô hình ≤150M hoặc embedding tính trước); FastAPI + HTML/JS tối giản **4–7 ngày**; **FastAPI + React (stack khai báo của sinh viên) 1,5–2,5 tuần**; Spring Boot + React + ml-service FastAPI riêng (kiến trúc repo đã dự tính) **2,5–4 tuần** — ấn tượng nhất về mặt SE và cũng rủi ro tiến độ nhất.

**Kế hoạch bảo vệ được:** dựng bản **Gradio hoặc Streamlit trước, ở khoảng tuần 10, làm bảo hiểm** (1–2 ngày, luôn có một demo chạy được), rồi nâng lên **FastAPI + React ở tuần 12–13** nếu thí nghiệm đã xong. **Tuyệt đối không để app đến tuần cuối.**

**Chế độ thất bại kinh điển và cách sửa trung thực.** App không chạy nổi PLM trong giới hạn hosting miễn phí, nên âm thầm serve kết quả tính trước cho một danh sách protein cố định và hỏng với mọi chuỗi mới. Cách sửa, theo thứ tự ưu tiên: (1) **chủ động huấn luyện mô hình cuối trên một checkpoint PLM nhỏ** — dùng ESM-2 **35M hoặc 150M** cho mô hình triển khai, và báo số của ProtT5-XL / ESM-2 650M như giới hạn trên mức nghiên cứu trong một bảng; **đóng khung đây là một nghiên cứu accuracy-vs-deployability biến ràng buộc thành đóng góp** thay vì một lời thú nhận, và nó phục vụ trực tiếp sự quan tâm của khoa SE về trade-off kỹ thuật; (2) **job queue**: submit chuỗi → job id → poll kết quả, phần embedding nặng chạy ở worker (kiến trúc đúng và là một deliverable SE tốt, nhưng **nó chỉ che latency, không tạo ra bộ nhớ không có**); (3) **cache embedding cho tập đánh giá và các example input** — và vì **disk 50 GB của HF KHÔNG bền vững**, phải **ship cache trong repo hoặc trong một HF Dataset**, không build lúc runtime; (4) **cap độ dài chuỗi và cap batch** trên app công khai, nói rõ trong UI — chuẩn mực thông thường và nó ngăn cái OOM sẽ giết demo đúng lúc bảo vệ; (5) **phương án cuối, làm trung thực**: một static Space / trình duyệt kết quả tính trước, với banner nổi bật nói rõ nó serve dự đoán tính trước cho N protein, cộng link Colab notebook và một Docker image để chạy trên chuỗi mới — **đây không phải thất bại nếu được DÁN NHÃN; thất bại là giả vờ ngược lại**; (6) **xin GVHD một server của Đại học Cần Thơ ở tuần 6** — không mất gì khi hỏi và nó xóa toàn bộ ràng buộc; đồng thời xin community GPU grant của HF, docs mời làm việc đó. **Anti-pattern phải tránh:** gọi một inference API thuê ngoài cho PLM lúc có request — nó mang vào một key, một quota, một chi phí và một phụ thuộc mà sinh viên không bảo đảm được trong suốt đời luận văn.

**Một quan sát có giá trị chiến lược:** cả **BERT-Promoter của GVHD ship CODE ONLY** ("freely available at https://github.com/khanhlee/bert-promoter", **không phải một web server được host**) `[abstract nguyên văn]`, và **LMCrot 2024 cũng chỉ trỏ vào một repo** ("Code & Web Server: https://github.com/KCLabMTU/LMCrot") `[toàn văn]`. Nghĩa là **một web app chạy thật, deploy thật là chỗ sinh viên vượt được tiền lệ một cách thấy được** — quan trọng cho tiêu chí 5 và cho yêu cầu bắt buộc của khoa Kỹ thuật phần mềm. Và cộng thêm sự thật rằng **mọi web tool của tiền lệ trong nhánh sirtuin đều đã chết** (`140.138.155.216` time out hai đường, `bioinfo.bjmu.edu.cn/huac` không kết nối, bài 2025 không có server) `[đã thử link]`, cộng với **`cciwyy.top` của PLM-ATG không kết nối** và **`124.222.115.164` của Antiaging-FL không kết nối** `[đã thử link]` — "công cụ của field không còn dùng được hoặc yếu; tôi đã dựng một cái chạy được và có tài liệu" là một đóng góp tiêu chí 5 thật và một động cơ nghiên cứu đáng tin. **Nhưng tự nó chỉ là một đóng góp phần mềm, không phải một đóng góp nghiên cứu** — không được để nó làm trục chính.

---

## 12. Kế hoạch tuần 4 đến tuần 15

Giả định: tuần 4 là hiện tại; tuần 6 báo cáo lại đề tài; tuần 14–15 báo cáo cuối. **Mọi tuần đều có một điều kiện dừng/chuyển.**

**Tuần 4 (còn lại) — mở ba cổng chặn, theo đúng thứ tự này.** Ba việc này rẻ nhưng quyết định nhiều nhất:
1. **Giải mâu thuẫn MCC của SCANS** từ supplementary material hoặc GitHub — đây là sự thật chưa kiểm có ảnh hưởng quyết định lớn nhất, và nó định vị Ứng viên C.
2. **Xác nhận ý nghĩa ba cột của bảng benchmark dbPTM** và **kiểm cửa sổ ±10 có đủ rộng hay phải trích lại từ UniProt** — định vị Ứng viên B.
3. **Kiểm SaProt/ProstT5 có cần cấu trúc 3D ở inference hay không** — định vị toàn bộ khuyến nghị tiêu chí 3.
Song song: **xin GVHD bản PDF của SirtSAGE** (mọi đường tự lấy đều thất bại: publisher trả **HTTP 403**, Semantic Scholar báo `openAccessPdf.status: "CLOSED"`, không có index ở PubMed/bioRxiv/ResearchGate `[đã thử link]`) — đây cũng là một cách mở đầu cuộc trò chuyện tự nhiên ở tuần 6.

**Tuần 5 — dựng pipeline tối thiểu cho ứng viên dẫn đầu, và dựng history research.** Tải lại dữ liệu A (hai file CSV), dựng split gom nhóm theo protein, chạy một baseline LDA/decision tree để **tự có con số baseline per-isoform** (bài báo không công bố). Song song viết **bảng khảo sát phân nhóm theo phương pháp** đúng yêu cầu mục 3 của biên bản — dùng các bảng ở mục 3 và 4 của báo cáo này làm bộ xương.

**Tuần 6 — BÁO CÁO LẠI ĐỀ TÀI.** Trình bày theo đúng ba câu hỏi GVHD nhấn mạnh: bài toán là gì (input→output), vì sao cần làm (tính cấp thiết, có số), nghiên cứu giải quyết phần nào. Mang theo: bảng phân nhóm phương pháp, bảng so sánh ứng viên ở mục 9, danh sách loại bỏ ở mục 10 (để thấy đã tra rộng), và danh sách câu hỏi ở mục 13. **Đưa cả sáu đính chính ở mục 2 vào phần nói, không chờ bị hỏi.**

**Tuần 7 — chốt dữ liệu và chốt giao thức đánh giá.** Hoàn thành tập test độc lập (với A: split gom nhóm theo protein + tập MS trực giao). **Cổng dừng: nếu hết tuần 7 không có tập test độc lập hai lớp, chuyển sang ứng viên B.**

**Tuần 8 — baseline PLM.** Trích embedding (ProtT5 hoặc ESM-2 150M; **đo thời gian một batch 1.000 chuỗi trước khi cam kết với 650M**), train mCNN đa nhãn, báo MCC/AUPRC trên cả split cũ và split mới. **Đây là bảng số đầu tiên của luận văn.**

**Tuần 9 — "xa hơn PLM", nhánh một.** Thực hiện một trong bốn lựa chọn ở mục 11.1, ưu tiên embedding nhận biết cấu trúc nếu tuần 4 xác nhận nó không cần cấu trúc ở inference; nếu không thì LoRA hoặc đầu KAN. **Cổng dừng (riêng cho E nếu chọn E): nếu AUC trên split gom nhóm < 0,65, bỏ khẳng định "cải thiện SOTA" và chuyển trọng tâm sang benchmark + web tool + XAI.**

**Tuần 10 — web app bản bảo hiểm, 1–2 ngày.** Gradio hoặc Streamlit, một checkpoint nhỏ, dán FASTA → bảng + một hình + tải CSV. **Từ đây trở đi luôn có một demo chạy được.** Phần còn lại của tuần: nhánh hai của tiêu chí 3, hoặc conformal calibration.

**Tuần 11 — XAI.** Nước đi 1 (enrichment attribution vs annotation UniProt) là bắt buộc; nước đi 2 (attribution biện minh thiết kế multi-window) nếu còn thời gian. Cộng ba kiểm tra phòng vệ ở mục 11.2.

**Tuần 12–13 — nâng web app lên FastAPI + React**, thêm banner miền áp dụng, panel XAI, trang Limitations. **Chỉ làm bước này nếu thí nghiệm đã xong ở tuần 11; nếu chưa, giữ bản Gradio/Streamlit và dành thời gian cho số liệu.**

**Tuần 14–15 — viết và báo cáo.** Dự trù ablation còn thiếu và bảng cuối ở tuần 14; tuần 15 chỉ cho việc viết, slide và tập nói.

---

## 13. Câu hỏi đặt cho GVHD ở tuần 6

Xếp theo mức ảnh hưởng tới quyết định, cao nhất trước. Năm câu đầu là loại **phải có câu trả lời mới làm tiếp được**.

1. **Thầy coi một split gom nhóm theo protein mà em tự dựng, cộng một tập test MS độc lập nguồn, là "tập test độc lập" đủ chuẩn hay không — hay thầy đòi một benchmark cộng đồng đã tồn tại sẵn?** Đây là câu quyết định giữa Ứng viên A và Ứng viên B. (Bối cảnh cần nói kèm: trong field này, **"mức khớp với công trình của thầy" và "có benchmark cộng đồng" kéo về hai phía ngược nhau**, vì chính các bài của thầy tự dựng split CD-HIT riêng.)
2. **Thầy muốn em đi hướng aging hay hướng cancer?** Nếu cancer thì B hoặc F; nếu aging thì A hoặc C.
3. **Thầy có bài toán hoặc bộ dữ liệu nào đang mở trong nhóm muốn giao không, đặc biệt trong nhánh sirtuin?** Nếu thầy có dữ liệu SirtSAGE và có bài toán con, lựa chọn thay đổi lập tức. **Và xin thầy bản PDF của SirtSAGE** — mọi đường tự lấy đều bị chắn.
4. **Thứ tự ưu tiên giữa năm tiêu chí nếu không đạt hết trong 8–9 tuần là gì?** Biên bản ghi "càng đạt nhiều càng tốt" và tiêu chí 5 là không thể thiếu, nhưng không có trọng số.
5. **Nếu các con số trung thực ĐI XUỐNG so với số đã công bố — vì split chặt hơn và negative khó hơn — thầy có chấp nhận đó là KẾT QUẢ hay thầy kỳ vọng "beat SOTA"?** Phải thống nhất cách đóng khung này **trước** khi cam kết, đặc biệt nếu chọn Ứng viên E.
6. **Nguồn GPU em có thể dùng là gì, và có server của trường để host web app không?** Hugging Face đã đổi chính sách: tạo Gradio/Docker Space nay cần **paid plan**; một server của trường xóa toàn bộ ràng buộc bộ nhớ.
7. **Phạm vi tối thiểu của ứng dụng/website là gì** — một trang demo chạy được là đủ, hay thầy kỳ vọng kiến trúc ba tầng kiểu Spring Boot + React + ml-service?
8. **Hình thức và mức chi tiết của báo cáo tuần 6** (slide, văn bản, hay đề cương sơ bộ)?
9. **Thầy nghĩ gì về việc đóng góp XAI là "attribution đối chiếu định lượng với annotation UniProt độc lập" thay vì SHAP để chọn đặc trưng như BERT-Promoter?** Câu này cho thấy sinh viên đã đọc tiền lệ của chính thầy và biết vượt nó ở đâu.
10. **Em có được tính "một kết quả âm được thực hiện tử tế" là đóng góp không** — ví dụ "token nhận biết cấu trúc không giúp gì khi đã kiểm soát đồng dạng"?

---

## 14. Những điều báo cáo này **CHƯA** kiểm chứng

Liệt kê đầy đủ mọi khoảng trống mà khảo sát tự đánh dấu. Đây là danh sách phải mang theo khi nói với GVHD — không được để một trong các mục này bị phát hiện trước khi tự nói ra.

**Có ảnh hưởng quyết định nhất, phải giải trước tuần 6:**
- **MCC của SCANS trên tập test độc lập**: bài báo cho hai bộ số không tương thích (0,176–0,276 từ bảng so sánh trích được, so với 0,712–0,779 từ abstract/thân bài), và **không xác nhận được bộ nào ứng với setting nào**. Nếu bộ cao là bộ của test độc lập, dư địa của Ứng viên C co lại rất nhiều.
- **Ý nghĩa ba cột số trong bảng benchmark theo nhóm kinase của dbPTM**: header không lấy được trong lần scrape; "protein / site dương / site âm" là **suy luận**.
- **Cửa sổ ±10 của dbPTM có đủ cho multi-window CNN hay phải trích lại từ UniProt**: chưa kiểm.
- **SaProt/ProstT5 có cần cấu trúc 3D ở thời điểm inference hay không**: chưa kiểm. Đây là điểm quyết định xem khuyến nghị tiêu chí 3 có đứng được hay không.
- **URL figshare của Gartner et al. 2021** (nếu quay lại nhánh neoantigen): README của NeoRanking chỉ nói "the figshare links provided by Gartner et al." mà **không in URL** — chưa thử được.

**Về SirtSAGE — hầu như không biết gì về số liệu:**
- **Accuracy, MCC, AUC, F1 per-class: không tìm được.** Abstract không có số nào, toàn văn bị chắn (**HTTP 403** cả hai đường, `openAccessPdf.status: "CLOSED"`, không index ở PubMed/bioRxiv/ResearchGate) `[đã thử link]`.
- **Nguồn dữ liệu, kích cỡ dataset, số lớp trong "unified multi-class setting"** (7 isoform? 4 lớp phylogenetic? isoform × localization?): **không tìm được**.
- **Có công bố code/data hay không: không tìm được.**
- **Tập test độc lập là một benchmark đã công bố hay một split riêng: không tìm được.**
- **Phần limitations / future work: không tìm được** (nằm trong Discussion sau tường 403).

**Về DeepSIRT:**
- **Thành phần dataset chính xác** (bao nhiêu protein target mỗi SIRT, bao nhiêu mỗi localization, database nào, ngưỡng đồng dạng nào): **không tìm được**.
- **Số lớp: không tìm được.**
- **Accuracy và AUC do chính tác giả báo cáo: không tìm được** (abstract chỉ có sensitivity, specificity, MCC).

**Về Ứng viên A:**
- **Per-isoform AUC/MCC/accuracy cho SIRT1 và SIRT3–SIRT7: không tìm được** — chỉ có SIRT2 (precision 43,0%) và SET8 (37,4%). Sinh viên có thể phải tự chạy lại notebook để dựng baseline (công việc ngoài kế hoạch).
- **File proteome-wide trên Google Drive có còn resolve hay không: chưa kiểm.**
- **Nội dung Zenodo record 10.5281/zenodo.17082245: chưa kiểm.**
- **URL tải file của AcetylBench, ngưỡng dedup chính xác, và nó đánh giá lại những predictor nào: không tìm được** — mọi đường vào toàn văn đều bị chắn. "Đánh giá trên AcetylBench" hiện là **ý định, không phải lựa chọn đã xác minh**.
- **Có nguồn công khai nào gán nhãn site acetyl-lysine theo enzyme deacetylase chịu trách nhiệm ở quy mô lớn, ngoài microarray Rauh: không tìm được** — dường như thật sự không tồn tại, và đó chính là lý do bộ Rauh/Biggar là lựa chọn duy nhất.
- **PhosphoSitePlus có đòi đăng ký hôm nay hay không, và số dòng acetylation chính xác ở đó: chưa kiểm.**
- **URL download thật và số đếm acetylation của iPTMnet: chưa kiểm.**

**Về Ứng viên E (senescence):**
- **Bộ dữ liệu v2 chưa được kiểm** — nằm sau một Git LFS object 1,41 GB chưa pull. **Không được tuyên bố benchmark đã công bố bị rò rỉ**; chỉ được nói bản v1 chứng minh được là rò rỉ và v2 chưa kiểm.
- **Dòng lệnh MMseqs2 chính xác** (coverage `-c`, `--cov-mode`, `--cluster-mode`): **không tìm được** — nó quyết định liệu các mảnh có thoát được clustering.
- **Truy vấn UniParc/UniProt chính xác: không tìm được.**
- **Table S3, danh sách 148 gene âm chính thức: chưa lấy được** (Wiley 403; PMC không expose supplement). 82+27 symbol thu hồi được là **tái dựng một phần**, không phải danh sách chính thức.
- **Tác giả định dùng HRT Atlas v1.0 hay danh sách Eisenberg–Levanon: không tìm được** — cả hai bản đều không trích dẫn nguồn housekeeping gene nào.
- **Git LFS object có tải được ẩn danh hay không: chưa kiểm** (quota bandwidth trên tài khoản GitHub miễn phí có thể làm `git lfs pull` thất bại). **Đây là rủi ro truy cập dữ liệu thật duy nhất — thử trong giờ đầu tiên.**
- **Thời gian Colab thực tế để embed ~76.000 chuỗi bằng ESM-2 650M: chưa đo.** Dấu hiệu gián tiếp: tác giả ship embedding 8M và 35M làm file thật nhưng để 150M và 650M là LFS object. **Đo một batch 1.000 chuỗi trước khi cam kết với 650M.**
- **Số liệu của chapter ESM-2+LoRA cho protein lão hóa: chưa kiểm** (Springer 303-redirect về IdP) — kích cỡ dataset, chỉ số, và có gom nhóm theo gene hay không đều không biết.
- **Tên giấy phép cụ thể của HAGR: không tìm được** — chỉ biết "free use subject to HAGR conditions".
- **Package PyPI `senseqnet` và notebook Colab demo: chưa chạy thử.**
- **Số trích dẫn của SenSeqNet: không lấy được** — báo là "không tìm được bài nào trích dẫn tính đến 02/10/2026", **không phải "0 trích dẫn"**.

**Về các ứng viên khác và các nhánh bị loại:**
- **Repo SCANS và repo PLM-ATG có thật chứa file benchmark hay không: chưa kiểm** (chỉ biết trang repo trả 200).
- **Số liệu của StackAPP (autophagy 2025): không tìm được** — phải kiểm trước khi nói PLM-ATG là SOTA.
- **Số liệu tập test độc lập của BERT-Kgly: không tìm được.** Số liệu của bài RNN glycation 2025: **không tìm được.**
- **Tác giả của Mito-Mixer: không xác định được** (MDPI trả 403) — quan trọng vì không loại trừ được khả năng đó là bài của nhóm Prof Ou. **Kiểm trước khi xét bất kỳ đề tài mitochondrial nào.**
- **Kích cỡ chính xác của SubMitoPred / M983: không tìm được.**
- **Đã có predictor site GTP/GDP nào cho superfamily RAS hay chưa: chưa tra.** **Đây là việc tra cứu có giá trị cao nhất còn lại** — nó quyết định giữa các biến thể của Ứng viên F.
- **Multiview-ATPBind (PMID 39690486): chỉ xác nhận được tiêu đề/PMID** (PubMed cookie wall) — đây là đối thủ trực tiếp nhất của Ứng viên F.
- **Số record chính xác của LIRcentral và download có resolve hay không: chưa kiểm.**
- **Progeria/laminopathy và dự đoán chaperone-client: tra rất nông hoặc không tra.**
- **Có tồn tại tập test độc lập (non-homologous, định sẵn) cho bất kỳ task phân loại họ transporter hoặc receptor liên quan ung thư nào: chưa xác định.**
- **Toàn văn Immunity 2023: không đọc được** (Cell.com **HTTP 403** cả `/fulltext/` và `/pdfExtended/`; Europe PMC **403**) — nên phần Limitations/Discussion, AUC/PR theo từng dataset, kích cỡ split NCI-train/NCI-test chính xác, và danh sách baseline đầy đủ đều **chưa kiểm**.
- **Dataset, kích cỡ, split và thành phần "independent test set" đứng sau AUC 0,9053 của NeoGen-BC: không tìm được từ nguồn bên ngoài** — phải lấy từ bản PDF có sẵn trong repo. **Code của NeoGen-BC và DeepNeoAG: không tìm được repo nào.**
- **Số liệu hiệu năng của NeoTImmuML (AUC, accuracy, precision/recall): không tìm được** (endpoint toàn văn Frontiers trả body bị cắt).
- **Hiệu năng của predictor neoantigen phân tầng theo allele HLA Đông Nam Á/Việt Nam: không tìm được.** (Bối cảnh: **HLA-A\*02:01 chiếm 80/199 = 40,2%** ITSNdb `[toàn văn]` — cao hơn hẳn tần suất của allele đó ở bất kỳ dân số nào, và nó lệch về tổ tiên châu Âu.)
- **Hai bài review 2025 có thể hợp nhất các số liệu nhánh neoantigen: cả hai đều bị 303-redirect về trang login.**

**Về công cụ và hạ tầng:**
- **Không tìm được số wall-clock đo thật** cho SHAP hay integrated gradients áp trên ProtT5/ESM-2 trên T4; **không bài nào báo runtime của XAI**. Mọi con số thời gian trong mục 11.2 là **ước lượng tự gán nhãn**.
- **Không tìm được số GPU-hour đo thật** cho việc train một GATv2/GraphSAGE trên vài nghìn residue graph.
- **Không kiểm module `explain` hiện tại của PyTorch Geometric.**
- **Không tìm được bài protein-sequence nào dùng TCAV / concept activation vector hoặc layer-wise relevance propagation.** LIME, DeepLIFT thuần và LRP **không xuất hiện** ở bất kỳ bài protein-sequence 2024–2026 nào trong khảo sát.
- **Không tìm được benchmark so sánh trực tiếp các phương pháp XAI trên các predictor mức residue của protein.**
- **Không tìm được bài nào dùng XAI để giải thích riêng khoảng cách hiệu năng giữa split có và không kiểm soát redundancy** — đây là cơ hội của Nước đi 3, nhưng là **tính mới chưa xác nhận**, phải tra lại.
- **Không tìm được bài protein-specific tương đương với việc hiệu chỉnh "attribution noise từ one-hot encoding" trong genomics**; liệu artefact đó có áp dụng cho input là embedding PLM (không phải one-hot) hay không: **không tìm được**.
- **Toàn văn BERT-Promoter: không đọc được** (ScienceDirect 403, PubMed cookie wall, EuropePMC 403, trang tác giả → 404) — nên **biến thể SHAP cụ thể (KernelExplainer hay TreeExplainer), số đặc trưng giữ lại sau xếp hạng SHAP, danh sách classifier đầy đủ, và các giá trị MCC/AUC đều KHÔNG TÌM ĐƯỢC.** Sinh viên có quyền truy cập thư viện trường và nên lấy PDF — đây là thứ đầu tiên GVHD kiểm được.
- **Không kiểm được free tier hiện tại của Render hoặc Fly.io** (RAM, sleep, có còn free tier hay không) — cả hai đã đổi nhiều lần.
- **Không tìm được cold-start latency đo thật** cho một Space hoặc app Streamlit nạp một checkpoint ESM-2.
- **Không kiểm chi tiết điều kiện của free tier ZeroGPU** ngoài một câu trong docs chính thức; **"in good standing" không được định nghĩa**, và đây là điểm thất bại đơn lẻ của phương án hosting ưu tiên.
- **ZeroGPU có giữ được một mô hình ESM-2 650M trong GPU memory hay không và trong bao lâu mỗi request: không tìm được.**
- **Trần bộ nhớ 690 MB–2,7 GB của Streamlit Community Cloud: chưa kiểm ở nguồn gốc** (từ tóm tắt thứ cấp của docs Streamlit).
- **Không tìm được nguồn nào khảo sát framework triển khai (Flask/FastAPI/Streamlit/Gradio) của các web server bioinformatics gần đây** — các bài gần như không nói. Nên **mọi khẳng định về phân bố framework trong báo cáo này là không có cơ sở**, và báo cáo không đưa ra khẳng định nào như vậy.
- **Không tìm được bài báo hay bài viết nào mô tả thẳng thắn một web app dự đoán mức luận văn thất bại theo kiểu đó** — chế độ thất bại ở mục 11.3 là **rủi ro suy luận từ giới hạn bộ nhớ đã công bố cộng kích cỡ mô hình**, không phải một hiện tượng được trích dẫn.
- **ESM-3 có tải trọng số tự do được với điều khoản sinh viên dùng được hay không: không tìm được** — và điều này quan trọng vì ESM-3 thường bị gate.
- **Một nguồn phải KHÔNG được trích:** tỉ lệ "Kernel SHAP chậm hơn TreeSHAP 30–500 lần" đến từ một trang hướng dẫn của vendor thứ ba, chất lượng thấp — **không đưa vào luận văn mà chưa xác minh lại**. Tương tự, con số "SaProt 77,16% so với ESM-2 39,16% cho long-range contact" không gán được về một bài cụ thể nào — **không trích**. Và con số "Naïve Bayes dựa trên network đạt 92,5% cho tumour suppressor và 94,2% cho oncogene" **không truy được về bài gốc — không trích**.

**Về danh mục công bố của GVHD:**
- Cả hai danh mục đều là **bản scrape Google Scholar cục bộ** (14 công trình cho Prof Ho; file Prof Ou dài hơn và chưa đếm). **"Không có bài aging nào ngoài SirtSAGE" nghĩa là "không có trong các bản scrape này", không phải một điều chắc chắn.**
- **Chữ viết tắt `Ho QT[Author]` trùng nhiều tác giả trên PubMed** (71 bản ghi cho dạng viết tắt) và không phân giải được bằng ORCID hay affiliation trong thời gian có. **Các công trình đơn tác giả hoặc với cộng tác viên khác của thầy có thể còn những mục chưa thấy.**
- **SirtSAGE không xuất hiện trong các truy vấn PubMed** — có thể *J Comput Biophys Chem* không được index ở PubMed; phần về nó dựa vào bản ghi của repo và metadata Semantic Scholar.
- **Việc GVHD có CHẤP NHẬN một đề tài cancer dù thầy không có công bố nào ở đó hay không là một câu hỏi về con người mà khảo sát không trả lời được từ văn liệu.** Phải hỏi ở tuần 6.
