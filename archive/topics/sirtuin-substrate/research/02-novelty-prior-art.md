# Kiểm chứng tính mới: dự đoán cơ chất deacetyl hóa đặc hiệu isoform SIRT1–7 bằng PLM

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Ngày tìm kiếm: **08/10/2026**. Người thực hiện: Claude (subagent khảo sát prior art).

**Nhãn bằng chứng dùng trong tài liệu này**
- `[tác giả báo cáo]` — con số hoặc nhận định do chính tác giả bài báo viết, tôi chỉ chép lại.
- `[tự kiểm]` — tôi tự đọc toàn văn / metadata trong phiên này và xác nhận.
- `[suy luận]` — kết luận của tôi từ các bằng chứng trên, không có nguồn nào nói thẳng.
- `[chưa kiểm]` — chỉ thấy qua snippet tìm kiếm hoặc tóm tắt bên thứ ba, chưa đọc nguồn gốc.
- `[chưa tìm thấy, không kết luận là chưa từng có]` — tôi tìm không ra; **không** được đọc thành "chưa ai làm".

> **Cảnh báo đọc trước:** tài liệu này tìm ra **ba bằng chứng chống lại** tính mới của đề tài, mạnh hơn tôi dự kiến trước khi tìm. Chúng nằm ở mục 1 (DeepSIRT, cùng nhóm Prof. Ou) và mục 6 (Ridgeway 2025 đã tự tuyên bố PLM + nhãn liên tục là "future work" của chính họ, và đã tự làm một phần đánh giá in-cell). Đọc mục 7 (phán quyết ba trục) trước khi dùng tài liệu này để làm slide.

---

## Chiến lược tìm kiếm và giới hạn phủ

### Công cụ và truy vấn đã dùng (08/10/2026)

| Công cụ | Truy vấn | Kết quả đáng chú ý |
|---|---|---|
| PubMed (MCP `search_articles`) | `sirtuin substrate prediction machine learning deacetylation` | **1** kết quả duy nhất trên toàn PubMed `[tự kiểm]` |
| PubMed | `(sirtuin OR SIRT1 OR SIRT2 OR SIRT3) AND (prediction OR predictor) AND (acetylation site OR substrate) AND (deep learning OR neural network OR language model)` | **1** kết quả: DeepSIRT (PMID 34058657) `[tự kiểm]` |
| PubMed | `enzyme-specific post-translational modification site prediction deep learning kinase-specific` | 0 kết quả (truy vấn quá hẹp do PubMed dịch cụm có gạch nối thành `[All Fields]`) `[tự kiểm]` |
| PubMed | `protein language model ESM-2 post-translational modification site prediction` | 6 kết quả `[tự kiểm]` |
| PubMed (`get_full_text_article`) | PMC12594832 (Ridgeway 2025) | **Đọc toàn văn 58.205 ký tự** `[tự kiểm]` |
| PubMed (`get_article_metadata`) | PMID 34058657, 40183480, 41203923 | abstract + tác giả + affiliation đầy đủ `[tự kiểm]` |
| WebSearch (extended) | `in vitro peptide array kinase motif transfer to in-cell phosphoproteome prediction generalization` | Tìm được bài so PL-PWM (Johnson) vs motif từ dịch chiết tế bào |
| WebSearch (extended) | `Johnson 2023 kinome atlas peptide specificity predicts cellular phosphosites limitations` | Nature 2023 atlas, PMC9876800 |
| WebSearch (extended) | `multi-label PTM site prediction protein language model noisy labels` | COMPASS-PTM, MTPrompt-PTM, AstraPTM, MIND-S, PTMGPT2 |
| WebSearch (extended) | `conformal prediction PTM phosphorylation site prediction protein language model` | **Không ra bài nào** ghép conformal với PTM |
| WebSearch (extended) | `PhosformerST kinase-specific phosphosite prediction protein language model zero-shot` | Phosformer, Phosformer-ST, DARKIN, DeepKinZero |
| WebSearch (extended) | `Deep-PLA HAT HDAC specific lysine acetylation deacetylation prediction` | Deep-PLA (bbz107), GPS-PAIL |
| WebSearch (extended) | `in vitro specificity model generalization to in vivo substrates domain shift enzyme substrate prediction` | OmniESI, VIPER, low-homology shift |
| WebSearch (extended) | `benchmarking kinase substrate predictions against perturbation phosphoproteomics cellular validation Kinase Library` | benchmarKIN (Nat Commun 2025) |
| WebSearch (extended) | `Prot2Token multi-task protein language model PTM phosphorylation NeurIPS 2025` | Prot2Token (bioRxiv 2024), Extending Prot2Token (LMRL@ICLR 2025) |
| WebSearch (extended) | `NAD_MCNN sirtuin NAD+ binding site prediction multiwindow CNN protein language model` | NAD_MCNN, ATP_mCNN, repo `B1607/SirtuinNAD` |
| WebSearch (extended) | `positive-unlabeled learning PTM site prediction label noise acetylation benchmark` | EPuL, PU-glycosylation, TransPTM, DeepMVP |
| WebSearch (extended) | `LoRA fine-tuned ESM-2 multi-window CNN PTM site prediction conformal uncertainty combination` | ESMBind/QBind, PDeepPP, SeqProFT |

### Giới hạn phủ — phải nói với GVHD

1. **Chưa truy cập được Semantic Scholar / Consensus / bioRxiv API trực tiếp**; mọi thông tin về preprint đến qua WebSearch, nên có thể **bỏ sót preprint mới (2026)** chưa được index tốt `[tự kiểm về giới hạn]`.
2. **Chưa đọc toàn văn** bất kỳ bài nào ngoài Ridgeway 2025. Deep-PLA, NAD_MCNN, DeepSIRT, Johnson 2023, COMPASS-PTM chỉ đọc abstract hoặc snippet → phần lớn mang nhãn `[chưa kiểm]`.
3. **Không tra được kỷ yếu hội nghị trực tiếp** (NeurIPS/ICLR/ISMB/RECOMB OpenReview, proceedings). Thông tin "Prot2Token ở NeurIPS 2025" trong tài liệu nội bộ của sinh viên **không xác nhận được**: tìm ra bản bioRxiv 2024 và bản mở rộng ở **LMRL Workshop @ ICLR 2025**, không thấy NeurIPS `[chưa kiểm]` → **phải sửa lại citation này trong đề cương**, nếu không sẽ bị GVHD bắt lỗi.
4. **PubMed không index arXiv/ICLR/NeurIPS**, nên phần phương pháp máy học thuần (label-noise, conformal, multi-label) bị phủ kém nhất trong ba trục.
5. Chưa đối chiếu với **danh mục công bố đầy đủ của TS. Hồ Quang Thái**; bản scrape trong repo chỉ có 14 bài (ghi trong `project/advisor-research.md`). DeepSIRT tìm được ở đây **không có trong bản scrape đó** — dấu hiệu bản scrape thiếu.
6. Mỗi truy vấn chỉ chạy **một lần**; không có kiểm tra liên-công-cụ (cross-engine) cho phần lớn nhận định.

---

## 1. Công trình nào đã dự đoán cơ chất sirtuin hoặc vị trí acetyl hóa do sirtuin điều hòa? Có bài nào đặc hiệu isoform SIRT1–7 không?

### Takeaway

Chỉ tìm được **hai** công trình nhắm trực tiếp vào "cơ chất sirtuin" — **Ridgeway 2025** (mức residue, đúng SIRT1–7, có cả nhãn mảng peptide và xác nhận MS) và **DeepSIRT 2021** (mức protein, bảy isoform, **do chính nhóm Prof. Y.-Y. Ou làm**). Nghĩa là **đặc hiệu-isoform-SIRT1–7 đã được làm hai lần**, một lần ở mức residue và một lần ở mức protein, và lần ở mức protein là của nhóm GVHD.

### Cited Findings

- **Ridgeway et al. 2025** (*Commun Chem* 8:340, công bố 07/11/2025) dựng mô hình ensemble ML-hybrid cho **cả bảy SIRT1–7**, tập huấn luyện 6.801 peptide 13 aa đại diện acetyl-lysine proteome, sinh **443 đặc trưng**; "The number of deacetylation sites (i.e., positive and negative ratio) differed for each SIRT, as well as the best-fit model and meta-model" `[tác giả báo cáo]` — [DOI 10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6), [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- Ridgeway dùng **MuSiteDeep** làm thành phần "dự đoán PTM tổng quát" trong ensemble cho nhánh SIRT (và MethylSight cho nhánh SET8): "MuSiteDeep was employed for the generalized PTM prediction component of the ensemble model" `[tự kiểm — đọc toàn văn]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- Ridgeway **đã có phân tích chia sẻ cơ chất giữa isoform**: Circos plot + UpSet plot, và báo "SIRT2 and SIRT3 share almost twice the substrates as any other combination of SIRT", cặp lớn thứ hai là SIRT5–SIRT7 `[tác giả báo cáo]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- **⚠️ DeepSIRT (2021)**: Shah, Taju, Dlamini, **Ou Y.-Y.** (Yuan Ze University), *Comput Biol Chem* 93:107514 — "a deep neural network approach using one-dimensional Convolutional Neural Networks (CNN)… to accurately identify the outcome of the sirtuin protein by targeting their subcellular localizations", cho **"seven members of the sirtuin family of proteins"**, báo sensitivity 85,77%, specificity 97,32%, MCC 0,82 trên hai tập độc lập `[tác giả báo cáo, qua PubMed metadata]` — [DOI 10.1016/j.compbiolchem.2021.107514](https://doi.org/10.1016/j.compbiolchem.2021.107514), PMID 34058657
- DeepSIRT nói rõ về khoảng cách isoform: "The seven members of the sirtuin family have various substrates and are present in nearly all subcellular localizations including the nucleus, cytoplasm, and mitochondria" và "the function and localization of sirtuin targets were analyzed and annotated to compartmentalize into distinct subcellular localizations" `[tác giả báo cáo]` — PMID 34058657
- **GPS-PAIL** (2016) dự đoán vị trí acetyl hóa **đặc hiệu từng KAT** (lysine acetyltransferase) từ trình tự — tiền lệ "đặc hiệu enzyme" trong họ acetyl hóa từ 2016 `[chưa kiểm]` — [PMC5177928](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5177928/)
- **TransPTM** (2024, *Brief Bioinform* 25(3):bbae219) dựng benchmark **NHAC** cho acetyl hóa non-histone: 1.100 dương / 11.784 âm từ chuỗi đầy đủ, âm = lysine không được annotate `[chưa kiểm]` — [bbae219](https://academic.oup.com/bib/article/25/3/bbae219/7667560)

### Inferences

- `[suy luận]` **DeepSIRT là bằng chứng chống novelty nguy hiểm nhất ở trục 1**, vì (a) cùng nhóm nghiên cứu của đồng tác giả thường xuyên của GVHD, (b) cũng là "bảy isoform SIRT", (c) cũng dùng CNN. Nếu sinh viên lên slide nói "chưa ai làm đặc hiệu isoform SIRT1–7", GVHD **có thể chỉ ngay vào bài của nhóm mình**. Phải chủ động nêu DeepSIRT trước, rồi phân biệt: DeepSIRT phân loại **protein nào là target của SIRT nào và ở ngăn tế bào nào** (mức protein, đa lớp theo khu trú), còn đề tài này dự đoán **lysine nào trong protein đó** (mức residue, đa nhãn 7 đầu ra).
- `[suy luận]` "Đặc hiệu isoform" **không còn là tính mới đứng một mình**. Phần còn mới ở trục 1 chỉ còn là: mức residue × đa nhãn **một mô hình 7 đầu ra** (Ridgeway dùng 7 mô hình rời) × đánh giá trong tế bào có hệ thống.
- `[suy luận]` Bảng Circos/UpSet của Ridgeway đã chiếm trước phần "phân tích cấu trúc chia sẻ cơ chất giữa các isoform". Đề tài không nên bán điểm này như phát hiện mới, chỉ nên bán phần "mô hình đa nhãn khai thác cấu trúc đó để dự đoán tốt hơn" — đây mới là phần Ridgeway bỏ trống.

### Gaps

- Chưa đọc toàn văn DeepSIRT → **chưa biết tập dữ liệu của nó là gì** (danh sách protein target theo isoform lấy từ đâu), nên chưa khẳng định được chắc chắn rằng nó không có nhãn mức residue. **Việc tuần 1 bắt buộc: đọc DeepSIRT toàn văn.**
- Chưa tìm được công trình nào dùng chính dữ liệu Rauh 2013 trước Ridgeway 2025 `[chưa tìm thấy, không kết luận là chưa từng có]`.
- Không tra được công bố tiếng Trung / kỷ yếu khu vực, nơi nhóm Yuan Ze thường công bố thêm.

---

## 2. Công trình dự đoán PTM đặc hiệu enzyme / isoform nói chung — ý tưởng nào làm phương pháp đề xuất thành dẫn xuất?

### Takeaway

Toàn bộ các "thành phần ý tưởng" của đề tài — đặc hiệu enzyme, ensemble với bộ dự đoán PTM tổng quát, PLM cho kinase-specific, zero-shot cho enzyme chưa có dữ liệu — **đã có tiền lệ công bố**, nhiều cái từ 2016–2020. Ý tưởng khiến đề tài dễ bị gọi là dẫn xuất nhất là **ensemble "mô hình đặc hiệu enzyme × bộ dự đoán PTM tổng quát"** (Ridgeway, Deep-PLA) và **kinase-specific PLM** (Phosformer, Prot2Token).

### Cited Findings

- **Deep-PLA (2020)**, Yu K. và cộng sự, *Brief Bioinform* 21(5):1798–1805: dự đoán acetyl hóa **đặc hiệu từng HAT/HDAC** cho **7 HAT và 9 HDAC**, đặc trưng AAC + CKSAAP + PSSM + binary encoding, mạng neural sâu, tối ưu siêu tham số bằng **PSO**; có kiểm chứng trên tập độc lập HAT phi-người, có web server `[chưa kiểm — qua snippet + trang tạp chí]` — [DOI 10.1093/bib/bbz107](https://doi.org/10.1093/bib/bbz107)
- Deep-PLA đã làm cả phần "mạng enzyme–cơ chất" và phần "đột biến missense trong TCGA ảnh hưởng acetyl hóa và sống còn bệnh nhân" `[chưa kiểm]` — [bbz107](https://academic.oup.com/bib/article/21/5/1798/5612158)
- **Quan trọng:** HDAC class III **chính là SIRT1–7**. DeepSIRT ghi: "Sirtuins are protein deacetylases and include in the class III family of histone deacetylase enzymes (HDACs). The class III HDACs contains seven members of the sirtuin family from SIRT1 to SIRT7" `[tác giả báo cáo]` — PMID 34058657
- **MusiteDeep** được chính Ridgeway gọi là "a notable progression forward" cho dự đoán PTM tổng quát, và họ dùng nó làm chân thứ hai của ensemble `[tự kiểm]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- **Phosformer** là Transformer giải thích được cho dự đoán phospho đặc hiệu kinase, tự nhận có thể dự đoán cơ chất cho kinase **không có cơ chất nào đã biết** `[chưa kiểm]` — [ResearchGate listing](https://www.researchgate.net/publication/367389686_Phosformer_An_explainable_Transformer_model_for_protein_kinase-specific_phosphorylation_predictions)
- **Phosformer-ST** tồn tại và được dùng làm baseline; một bài 2025 báo Phosformer-ST đạt F1 0,62, AUC 0,56, **MCC 0,05** trên benchmark của họ, và lưu ý Phosformer-ST cùng GPS 6.0 "generate predictions at the peptide level, not per residue" `[chưa kiểm — số liệu là của bài cạnh tranh, không phải của tác giả Phosformer-ST]` — [Kinase-substrate prediction using an autoregressive model, PMC11968300](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11968300/)
- **"Predicting Kinase-Specific Phosphorylation Sites with Pretrained Protein Language Models"** (bioRxiv 2025.03.12.642740 v2): ghép decoder transformer tự hồi quy với **ESM-2**, hai giai đoạn, mở rộng **Prot2Token** để hỗ trợ đồng thời ba nhiệm vụ gồm phân loại nhóm kinase và dự đoán vị trí phospho đặc hiệu kinase; **tự nhận là bằng chứng đầu tiên về zero-shot generalization** cho chuỗi kinase chưa từng thấy `[tác giả báo cáo, qua snippet]` — [bioRxiv 2025.03.12.642740](https://www.biorxiv.org/content/10.1101/2025.03.12.642740v2)
- **DARKIN** (*Bioinformatics* 2025, 41(11):btaf480): benchmark **zero-shot** gán phosphosite cho "dark kinase", so các PLM bằng k-NN không cần huấn luyện và bằng bilinear classifier; báo các mô hình **ESM** tốt nhất `[chưa kiểm]` — [btaf480](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017), [PMC12579546](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12579546/)
- **DeepKinZero** (*Bioinformatics* 2020): zero-shot cho kinase ít dữ liệu bằng RNN hai chiều trên cửa sổ trình tự `[chưa kiểm]` — [bioRxiv 670638](https://www.biorxiv.org/content/10.1101/670638.full.pdf)
- **LinkPhinder**: `[chưa tìm thấy, không kết luận là chưa từng có]` — truy vấn của tôi không ra bài này; chưa kiểm được nội dung.

### Inferences

- `[suy luận]` **Deep-PLA là vấn đề lớn hơn tài liệu nội bộ của sinh viên ghi.** Tài liệu `topic-final-recommendation.md` viết Deep-PLA "khác họ enzyme; không phải isoform sirtuin". Nhưng SIRT1–7 **là** HDAC class III, và Deep-PLA đã phủ **9 HDAC**. Việc tuần 1 bắt buộc: đọc toàn văn Deep-PLA xem **9 HDAC đó có SIRT nào không**. Nếu có SIRT1 hoặc SIRT2, câu "mới ở họ sirtuin" sụp. Nếu chỉ có HDAC1–9 class I/II, câu đó vẫn đứng nhưng phải nói chính xác là "class III chưa được Deep-PLA phủ".
- `[suy luận]` Phần "đa nhãn 7 đầu ra một mô hình thay cho 7 mô hình rời" **không** dẫn xuất từ Phosformer/Prot2Token theo nghĩa kiến trúc, nhưng ý "một mô hình chung học biểu diễn enzyme rồi điều kiện hóa theo enzyme" chính là ý trung tâm của Phosformer và DeepKinZero. Nên **đề tài không được bán "đa nhãn/đa enzyme" như ý tưởng mới**, chỉ bán nó như "lần đầu áp cho SIRT1–7 ở mức residue" `[chưa tìm thấy bài nào làm việc đó, không kết luận là chưa từng có]`.
- `[suy luận]` Một hệ quả tích cực: Phosformer-ST và GPS 6.0 dự đoán ở **mức peptide**, không phải mức residue trên chuỗi đầy đủ. Nếu đề tài làm mức residue trên chuỗi protein nguyên (tức dùng ngữ cảnh ngoài cửa sổ 13 aa), đó là điểm phân biệt kỹ thuật có thể đo được.

### Gaps

- Chưa biết 9 HDAC của Deep-PLA là những enzyme nào — **lỗ hổng quan trọng nhất của mục này**.
- Chưa xác nhận được LinkPhinder và chưa tra MusiteDeep/DeepPhos trực tiếp (chỉ thấy qua trích dẫn của bài khác).
- Chưa tìm được bài nào dùng ensemble "mô hình đặc hiệu enzyme × bộ dự đoán PTM tổng quát" **với PLM thay cho đặc trưng làm tay** `[chưa tìm thấy, không kết luận là chưa từng có]`.

---

## 3. PLM (ESM-2, ESM-3, ProtT5, ProstT5, Ankh, SaProt) cho dự đoán vị trí PTM — SOTA hiện nay là gì?

### Takeaway

PLM cho PTM là một lĩnh vực **đã rất đông** tính đến 2026: có mô hình đa nhãn (COMPASS-PTM, MTPrompt-PTM, AstraPTM, MIND-S, UniPTM), mô hình sinh nhãn kiểu GPT (PTMGPT2), mô hình PLM nhận biết PTM (PTM-Mamba), và mô hình có cấu trúc (SAPP, SE(3)-equivariant). **"Dùng PLM cho PTM" năm 2026 không còn là tính mới dưới bất kỳ cách đóng khung nào.**

### Cited Findings

- **COMPASS-PTM** / "Learning the PTM code through a coarse-to-fine mechanism-aware framework" (*Nat Commun*, có bản arXiv 2510.23492): hai giai đoạn, giai đoạn 1 là **Multi-label Site Profiling Network** tinh chỉnh một PLM rồi ghép với mô tả lý-hóa qua dual-modal encoder; có **crosstalk-aware prompting module** biến tri thức "các PTM hay đồng xuất hiện" thành attention bias học được; báo **tăng F1 tương đối tới 122%** trên benchmark đa nhãn; dữ liệu từ **dbPTM và qPTM**, tác giả gọi vấn đề là "dual long-tail" `[tác giả báo cáo, qua snippet]` — [Nat Commun s41467-026-73148-3](https://www.nature.com/articles/s41467-026-73148-3), [arXiv 2510.23492](https://arxiv.org/pdf/2510.23492)
- **MTPrompt-PTM** (*PMC12190693*): prompt tuning trên PLM **biết cấu trúc**, cho **13 loại PTM**, một mô hình đa nhiệm với lớp trích đặc trưng chia sẻ + đầu phân loại riêng từng nhiệm vụ, **cộng chưng cất tri thức (knowledge distillation)** `[tác giả báo cáo, qua snippet]` — [PMC12190693](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190693/)
- **AstraPTM** (bioRxiv 2025.02.20.639276): embedding **ESM2**, ghép mô hình nhị phân "residue này có bị modify không" với mô hình đa nhãn "loại nào"; lập luận là mô hình nhị phân học được dù PTM cụ thể rất hiếm `[tác giả báo cáo, qua snippet]` — [bioRxiv 2025.02.20.639276](https://www.biorxiv.org/content/10.1101/2025.02.20.639276.full.pdf)
- **MIND-S** (*Cell Rep Methods* 2023): huấn luyện một mô hình trên nhiều loại PTM để loại ít dữ liệu "borrow knowledge" từ loại nhiều dữ liệu `[chưa kiểm]` — [S2667237523000450](https://www.sciencedirect.com/science/article/pii/S2667237523000450)
- **PTMGPT2** (*Nat Commun* 2024, s41467-024-51071-9): tinh chỉnh theo prompt một PLM kiểu GPT-2, đổi bài toán phân loại thành **sinh nhãn dạng text** `[chưa kiểm]` — [s41467-024-51071-9](https://www.nature.com/articles/s41467-024-51071-9), [GitHub PTMGPT2](https://github.com/pallucs/PTMGPT2)
- **PDeepPP**: "state-of-the-art approach based on ESM-2, which uses a parallel transformer-CNN architecture to capture both global and local sequence determinants" — tức **ESM-2 + CNN song song đã là SOTA được công bố** cho PTM `[chưa kiểm — qua snippet]` — xuất hiện trong [PMC13389326](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389326/)
- **ESMBind / QBind** (bioRxiv 2023.11.13.566930): **LoRA và QLoRA trên ESM-2** cho vị trí gắn **và PTM**, dạng binary token classification; tác giả báo LoRA/QLoRA tốt hơn full fine-tuning và giảm overfitting; cũng cảnh báo benchmark của họ có thể gây nhầm "due to things such as sequence similarity" `[tác giả báo cáo, qua snippet]` — [bioRxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full)
- **SE(3)-equivariant dynamic multi-modal engine** (*Commun Chem* 2026, s42004-026-02062-y): đi từ dự đoán vị trí PTM tới hiểu mạng PTM `[chưa kiểm]` — [s42004-026-02062-y](https://www.nature.com/articles/s42004-026-02062-y)
- **SAPP: Structure Aware PTM Prediction** (*Comput Biol Med*) và **DeepPTMPred** (*Brief Bioinform* 2026, bbag321) đều là mô hình đa phương thức PLM + cấu trúc `[chưa kiểm]` — [SAPP](https://www.sciencedirect.com/science/article/pii/S0010482525015227), [bbag321](https://academic.oup.com/bib/article/27/3/bbag321/8709888)
- **PhosF3C**, **CaLMPhosKAN**, **LMPhosSite**, **GPS-pPLM**, **PTM-Mamba** — ít nhất năm bộ dự đoán phospho dựa PLM nữa, 2024–2025 `[chưa kiểm]` — [PhosF3C](https://www.biorxiv.org/content/10.1101/2024.12.25.630296.full.pdf), [CaLMPhosKAN PMC11972116](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11972116/), [PTM-Mamba PMC10925343](https://pmc.ncbi.nlm.nih.gov/articles/PMC10925343/)

### Inferences

- `[suy luận]` **Không tìm thấy bài nào dùng PLM cho dự đoán cơ chất đặc hiệu isoform sirtuin** `[chưa tìm thấy, không kết luận là chưa từng có]`. Đây là khoảng trống thật, nhưng là khoảng trống hẹp kiểu "chưa ai cắm ổ này vào ổ cắm kia", không phải khoảng trống phương pháp.
- `[suy luận]` Vì PDeepPP (ESM-2 + CNN song song) và ESMBind (LoRA + ESM-2 token classification) đã công bố, **"ESM-2 + LoRA + mCNN" phải được trình bày là baseline mạnh mượn từ SOTA, không phải đóng góp**. Nếu sinh viên bán nó như đóng góp, GVHD hoặc hội đồng sẽ chỉ ra ngay hai bài này.
- `[suy luận]` Phần ngữ cảnh: mCNN nhiều cửa sổ của nhóm GVHD (ATP_mCNN, NAD_MCNN, DeepPLM_mCNN) **về bản chất cùng loại** với CNN song song đa thang của PDeepPP. Nên "mCNN" chỉ là chọn kiến trúc quen tay, không là tính mới.

### Gaps

- Chưa so sánh được **số liệu SOTA cụ thể** giữa các bộ dự đoán (mỗi bài dùng benchmark riêng; chưa có bảng chung). Không tìm được một bài khảo sát/benchmark trung lập 2026 cho PTM-PLM `[chưa tìm thấy, không kết luận là chưa từng có]`.
- Chưa kiểm được ESM-3, Ankh, SaProt có được dùng cho PTM chưa (truy vấn của tôi không đi tới) `[chưa tìm thấy, không kết luận là chưa từng có]`.

---

## 4. Dự đoán PTM đa nhãn, học từ nhãn có thang độ / nhiễu, học nhận biết nhiễu nhãn trong proteomics

### Takeaway

Đa nhãn PTM: **đã làm nhiều** (mục 3). Học từ **nhãn có thang độ liên tục của mảng peptide**: **không tìm thấy bài nào** — đây là phần có cơ sở nhất để gọi là mới ở trục 3, và chính Ridgeway đã nêu nó như việc tương lai của họ. PU-learning cho PTM: có, nhưng cho glycosyl hóa và pupylation, **không phải acetyl hóa đặc hiệu enzyme**.

### Cited Findings

- **EPuL** (*PMC6151806*): thuật toán positive-unlabeled learning cho vị trí pupylation, coi các lysine chưa được annotate là tập unlabeled; tác giả lưu ý cách dựng mẫu âm "can affect the performance of the final predictor dramatically if done poorly" `[tác giả báo cáo, qua snippet]` — [PMC6151806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6151806/)
- **PU learning cho glycosyl hóa** (*PMC6404354*): tác giả đề xuất "this PU learning schema may also be effectively employed for other PTM and functional site problems" `[tác giả báo cáo, qua snippet]` — [PMC6404354](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6404354/)
- **MTPrompt-PTM** dùng **nhãn mềm từ mô hình thầy**, tác giả lập luận nhãn mềm "capture subtle patterns and uncertainties often missed by traditional hard labels" — đây là cách xử lý bất định nhãn bằng chưng cất, **không** phải phương pháp sửa nhiễu tường minh `[tác giả báo cáo, qua snippet]` — [PMC12190693](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190693/)
- COMPASS-PTM gọi vấn đề của benchmark đa nhãn PTM là **"dual long-tail"** (phân bố loại PTM lệch + tỉ lệ dương/âm lệch) `[tác giả báo cáo, qua snippet]` — [arXiv 2510.23492](https://arxiv.org/pdf/2510.23492)
- **TransPTM/NHAC** benchmark acetyl hóa non-histone coi lysine không annotate là **âm** (1.100 dương / 11.784 âm) — tức thiết lập mà PU-learning được tạo ra để tránh `[chưa kiểm]` — [bbae219](https://academic.oup.com/bib/article/25/3/bbae219/7667560)
- **🔴 Ridgeway tự nêu đúng ý tưởng "nhãn thang độ"**: "The density of the SPOT peptide arrays is correlated with substrate preference and **may improve performance when incorporated through regression-based ML models as opposed to the classification models currently used**. Alternatively, the incorporation of the density as a feature within the current framework will also be investigated." `[tự kiểm — đọc toàn văn]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- **Correcting Noisy Multilabel Predictions** (arXiv 2502.14281): sửa hậu kỳ dự đoán của bộ phân loại học trên nhãn nhiễu, **không chuyên PTM** `[chưa kiểm]` — [arXiv 2502.14281](https://arxiv.org/pdf/2502.14281)

### Inferences

- `[suy luận]` Ý "dùng `signal ratio` và `ratio error` của Rauh làm nhãn thứ tự / trọng số thay cho ngưỡng cứng `category ≥ 1`" **không phải ý của sinh viên — nó là việc tương lai do chính Ridgeway công bố**. Điều này không làm nó vô giá trị (đây là bước tiếp hợp lý và chưa ai làm `[chưa tìm thấy, không kết luận là chưa từng có]`), nhưng **cấm trình bày nó như ý tưởng mới**. Cách trình bày trung thực: "bài 2025 đề xuất hai việc tương lai — PLM và mô hình hồi quy trên mật độ SPOT — em làm cả hai và đo xem có đúng không."
- `[suy luận]` Vì chính tác giả đã nêu, **rủi ro bị nhóm Ridgeway làm trước là thật**. Bài công bố 07/11/2025, tức mới 11 tháng. Phải hỏi GVHD về rủi ro này.

### Gaps

- Không tìm được bài nào học PTM từ nhãn **liên tục/thứ tự có sai số đo** của mảng peptide `[chưa tìm thấy, không kết luận là chưa từng có]`.
- Không tra được tài liệu label-noise ở arXiv/NeurIPS một cách hệ thống (PubMed không index).

---

## 5. Công trình nào nghiên cứu tường minh dịch chuyển miền in vitro → trong tế bào (peptide → protein) cho dự đoán enzyme–cơ chất? Tính mới cốt lõi này thật sự độc đáo tới đâu?

### Takeaway

**Đây vẫn là trục mạnh nhất của đề tài, nhưng yếu hơn tài liệu nội bộ của sinh viên đang giả định.** Lý do: (a) Johnson 2023 đã chuyển motif mảng peptide sang gán kinase cho **toàn bộ** phosphoproteome người và được benchmark lại bởi bên thứ ba (benchmarKIN); (b) một bài 2024 đã **so trực tiếp** motif từ mảng peptide ngẫu nhiên (PL-PWM của Johnson) với motif từ dịch chiết tế bào; (c) **Ridgeway đã tự làm một phần đánh giá in-cell** cho cả SET8 và SIRT2. Phần còn thật mới là: **đóng khung chính nó làm câu hỏi nghiên cứu, với nhãn âm trong tế bào và chỉ số ngoài precision**.

### Cited Findings

- **🔴 Ridgeway đã làm đánh giá in-cell, hai lần, không chỉ một.**
  - SET8: 75 vị trí xác nhận in vitro → 32 vị trí sinh được tryptic peptide → theo dõi MS trong **HCT116 quá biểu hiện SET8**; **chỉ 9/32 vị trí đo được tin cậy**, và **3/9 (33%)** tăng mono-methyl hóa (SETD1B-K41, KAT6A-K314, PRDM12-K269), `n = 1` mỗi điều kiện trên 3 mẫu sinh học gộp `[tự kiểm — đọc toàn văn]`
  - SIRT2: mô hình "reconfirm 64 of 149 previously confirmed SIRT2 substrates… indicating an precision rate of **43,0%**", so với **41,2%** trên tập test in vitro của họ; tác giả gọi đây là "comparable but slight improvement" `[tự kiểm]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- **Ridgeway đã tự nêu đúng vấn đề dịch chuyển miền:** "our method uses abbreviated peptide sequences, which may not effectively represent full-length enzyme-substrate interactions, especially when considering that the folded structure may prevent access to the residues that present potential PTM activity" `[tự kiểm]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- Ridgeway cũng nêu thiên lệch nhãn: "the datasets of known modified sites used to generate the data for our method carry bias due to research-driven interest and experimental methods that often target known motifs" `[tự kiểm]` — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)
- **Johnson et al. 2023** (*Nature*, atlas Ser/Thr kinome, 303 kinase bằng positional scanning peptide array) đã **gán kinase cho mọi vị trí phospho Ser/Thr đã báo cáo ở người**; với nhóm nhỏ vị trí đã biết kinase thì dự đoán "in excellent agreement"; nhưng **kinase phụ trách chỉ được báo cáo cho dưới 4% các vị trí**, nên phần lớn dự đoán không kiểm được bằng tài liệu `[tác giả báo cáo, qua snippet]` — [DOI 10.1038/s41586-022-05575-3](https://doi.org/10.1038/s41586-022-05575-3), [PMC9876800](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876800/)
- Bài tyrosine kinome tiếp sau ghi **99%** vị trí phosphoproteome Ser/Thr khớp tốt với ít nhất một kinase Ser/Thr — tức match trình tự gần như không phân biệt được gì `[chưa kiểm]` — [s41586-024-07407-y](https://www.nature.com/articles/s41586-024-07407-y)
- **🔴 Bài so trực tiếp mảng peptide vs dịch chiết tế bào (2024)**: thử motif từ mảng peptide trình tự ngẫu nhiên (**PL-PWM, Johnson et al. 2023**) so với motif lấy từ dịch chiết tế bào; **mảng cho dự đoán chất lượng tương đương motif từ dịch chiết cho ba kinase**; cũng báo dự đoán cơ chất bằng PWM không bị ảnh hưởng bởi khác biệt độ dồi dào cơ chất in vitro giữa các dòng tế bào `[chưa kiểm — qua tóm tắt WebSearch, số kinase chỉ là 3]` — ["Validity of the cell-extracted proteome as a substrate pool for exploring phosphorylation motifs of kinases", PMC11447832](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/)
- **benchmarKIN** (*Nat Commun* 2025, s41467-025-59779-y): benchmark suy luận hoạt tính kinase từ phosphoproteomics, ghép thí nghiệm perturbation kinh điển (gold standard **184 cặp / 30 kinase / 62 perturbation**) với benchmark trên khối u; kết luận: phần lớn phương pháp tính toán cho kết quả tương tự nhau, nhưng **chọn thư viện cơ chất ảnh hưởng mạnh**, và thư viện do người curate thắng; **đã thử cả Kinase Library (Johnson) và Phosformer** làm nguồn cơ chất dự đoán `[tác giả báo cáo + repo, qua snippet]` — [s41467-025-59779-y](https://www.nature.com/articles/s41467-025-59779-y), [PMC12098709](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12098709/), [GitHub saezlab/kinase_benchmark](https://github.com/saezlab/kinase_benchmark)
- benchmarKIN là **hồi cứu**: nó chấm việc hồi phục kinase bị perturb, **không** kiểm chứng tiền cứu từng cạnh kinase–cơ chất `[chưa kiểm — nhận định từ tóm tắt]` — [PMC12098709](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12098709/)
- Benchmark Bioinformatics 2017 cho hoạt tính kinase đã **tách riêng bằng chứng cơ chất in vivo / in vitro / in silico** khi đánh giá `[chưa kiểm]` — [Bioinformatics 33(12):1845](https://academic.oup.com/bioinformatics/article/33/12/1845/2991427)
- Dịch chuyển miền trong dự đoán enzyme–cơ chất nói chung đã có: **OmniESI** (điều kiện hóa đặc trưng theo cặp enzyme–substrate), **VIPER** (báo tổng quát hóa OOD tốt hơn, gắn với minima phẳng + cross-attention; là preprint), và một preprint 2026 về ESI dưới **low-homology shift** `[chưa kiểm]` — [OmniESI arXiv 2506.17963](https://arxiv.org/html/2506.17963v1), [VIPER bioRxiv](https://www.biorxiv.org/content/10.1101/2024.06.21.599972.full.pdf), [arXiv 2606.22823](https://arxiv.org/pdf/2606.22823)
- Review ML cho biocatalysis ghi dự đoán động học thường **lệch nhau giữa in vitro và in vivo** do nồng độ chất chuyển hóa nội bào, mức biểu hiện enzyme và điều hòa tế bào; một nghiên cứu được dẫn báo mạng neural dự đoán **k_cat in vivo tốt hơn in vitro** `[chưa kiểm]` — [S0734975025001843](https://www.sciencedirect.com/science/article/pii/S0734975025001843)

### Inferences

- `[suy luận]` **Câu "chưa ai đo xem dự đoán từ mảng in vitro có đúng trong tế bào không" là sai nếu nói nguyên văn.** Ridgeway đã đo (43,0% cho SIRT2; 3/9 cho SET8), và cộng đồng kinase đã làm việc tương đương ở quy mô lớn hơn nhiều (Johnson 2023 + benchmarKIN + bài PMC11447832). Phải sửa cách phát biểu thành một trong hai dạng hẹp hơn:
  - *dạng an toàn:* "chưa có ai **nghiên cứu một cách hệ thống** độ chuyển miền in vitro → trong tế bào cho SIRT1–7: con số duy nhất tồn tại là precision 43,0% trên một isoform, một dòng tế bào, chỉ có nhãn dương" `[tự kiểm, đúng với bằng chứng]`
  - *dạng mạnh nhưng phải chứng minh:* "chưa có ai dựng **tập đánh giá trong tế bào có cả nhãn âm** cho đa isoform SIRT, nên chưa ai báo được MCC/AUPRC cho chuyển miền này" `[chưa tìm thấy, không kết luận là chưa từng có]`
- `[suy luận]` **Phần analogue kinase là cả bất lợi và lợi thế.** Bất lợi: nó cho thấy ý tưởng không mới về nguyên lý. Lợi thế: nó cho **phương pháp luận có sẵn, đã được bình duyệt** để mượn — cách chia benchmark của benchmarKIN, cách tách bằng chứng in vivo/in vitro/in silico của Bioinformatics 2017, và phát hiện "99% vị trí khớp ≥1 kinase" làm cảnh báo mẫu âm. Một đề cương dẫn rõ ba nguồn này sẽ **mạnh hơn** một đề cương tuyên bố mình đầu tiên.
- `[suy luận]` Phát hiện PMC11447832 (mảng cho dự đoán ngang motif từ dịch chiết, cho 3 kinase) là **bằng chứng ngược với giả thuyết trung tâm** của đề tài: nó gợi ý khoảng cách in vitro → trong tế bào **có thể nhỏ hơn** sinh viên đang giả định. Phải đọc toàn văn bài này; nếu nó đúng cho kinase, câu hỏi "có khoảng cách không" trở thành câu hỏi thật sự hai chiều — điều này **tốt cho tính khoa học** (kết quả âm vẫn có ý nghĩa) nhưng **xấu cho pitch** nếu sinh viên bán khoảng cách như điều đã biết.

### Gaps

- Chưa đọc toàn văn PMC11447832 → chưa biết "ba kinase" là kinase nào, chỉ số nào được dùng, và kết luận có tổng quát được không. **Việc tuần 1 ưu tiên cao.**
- Chưa tìm được bài nào **huấn luyện** mô hình trên nhãn mảng peptide rồi **đánh giá có nhãn âm** trên phosphoproteome/acetylome trong tế bào, cho bất kỳ họ enzyme nào `[chưa tìm thấy, không kết luận là chưa từng có]` — đây là câu phát biểu tính mới an toàn nhất mà tôi tìm được.
- Chưa tra được tài liệu domain adaptation (DANN, importance weighting, test-time adaptation) áp cho PTM `[chưa tìm thấy, không kết luận là chưa từng có]`.

---

## 6. Phân biệt NAD_MCNN (vị trí gắn NAD+) với dự đoán cơ chất — để vẽ đúng ranh giới trên slide 1

### Takeaway

Ranh giới **rõ ràng và dễ bảo vệ**: NAD_MCNN dự đoán **residue nào trên chính phân tử enzyme sirtuin** gắn cofactor NAD+; đề tài dự đoán **residue nào trên một protein khác** bị enzyme sirtuin tác động. Hai bài toán khác nhau về đối tượng đầu vào, đầu ra, và nguồn nhãn. Nhưng **DeepSIRT (cùng nhóm Ou) khó phân biệt hơn nhiều** và phải nêu cùng lúc.

### Cited Findings

- **NAD_MCNN** (Le V.-T., Liu, Chang, Lee, Lin, Malik, **Ou Y.-Y.**, Yuan Ze University; *Chem Biol Drug Des* 105(4):e70085, 04/2025): "Their interaction with NAD+ at the catalytic site is crucial for function, but experimental methods to map **NAD+ binding sites** are time consuming"; ghép PLM với mCNN; **AUC 0,9733** cho sirtuin người, **0,9701** cho enzyme deacyl hóa phụ thuộc NAD khác `[tác giả báo cáo, qua PubMed metadata]` — [DOI 10.1111/cbdd.70085](https://doi.org/10.1111/cbdd.70085), PMID 40183480
- Từ khóa chính thức của NAD_MCNN: "NAD-dependent deacetylation proteins", "convolutional neural networks", "multiple windows scanning", "pretrained language model", "sirtuins"; MeSH gồm **Binding Sites** `[tự kiểm — PubMed metadata]` — PMID 40183480
- Mã và dữ liệu NAD_MCNN ở **GitHub `B1607/SirtuinNAD`** `[chưa kiểm — chưa mở repo]` — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/cbdd.70085?af=R)
- Cùng khung kiến trúc xuất hiện ở **ATP_mCNN** (vị trí gắn ATP, AUC 0,95) và **DeepPLM_mCNN** (ion channel/transporter) — tức mCNN + PLM là **khung dùng lại** của nhóm cho họ bài toán "vị trí gắn ligand trên protein" `[chưa kiểm]` — [ATP_mCNN](https://www.sciencedirect.com/science/article/abs/pii/S0010482524016263), [DeepPLM_mCNN](https://sciencedirect.com/science/article/abs/pii/S1476927124000434)

### Inferences — câu để nói trên slide

`[suy luận]` Bảng ba dòng này là cách phân biệt sạch nhất, mỗi dòng có citation:

| | NAD_MCNN 2025 | DeepSIRT 2021 | Đề tài đề xuất |
|---|---|---|---|
| Đầu vào | Chuỗi của **chính enzyme** sirtuin | Chuỗi của **protein target** | Chuỗi của **protein target** |
| Đơn vị dự đoán | **Residue trên enzyme** | **Cả protein** (+ khu trú dưới tế bào) | **Residue (lysine) trên target** |
| Câu hỏi sinh học | NAD+ gắn ở đâu trong túi xúc tác? | Protein này có là target của SIRT nào, ở ngăn nào? | Lysine nào bị SIRT nào deacetyl hóa? |
| Nhãn | Vị trí gắn từ cấu trúc/annotation | Danh sách target + khu trú | Hoạt tính mảng peptide (in vitro) + MS (trong tế bào) |
| Nguồn | [cbdd.70085](https://doi.org/10.1111/cbdd.70085) | [107514](https://doi.org/10.1016/j.compbiolchem.2021.107514) | — |

`[suy luận]` **Khuyến nghị cách nói:** không nói "NAD_MCNN khác bài em" rồi dừng. Nói: "nhóm thầy đã phủ **hai** mảnh của bài toán sirtuin — vị trí gắn cofactor ở mức residue (NAD_MCNN), và nhận dạng target ở mức protein (DeepSIRT) — mảnh còn trống là **vị trí trên target ở mức residue, theo từng isoform**." Cách này biến chồng lấn thành lập luận liên tục với nền của GVHD, thay vì để GVHD tự phát hiện ra chồng lấn.

### Gaps

- Chưa mở repo `B1607/SirtuinNAD` → chưa biết tập dữ liệu NAD_MCNN có dùng cơ chất nào không.
- Chưa tìm được bài nào của nhóm GVHD về **cơ chất** (substrate) PTM ở mức residue `[chưa tìm thấy, không kết luận là chưa từng có]` — nhưng bản scrape danh mục GVHD chỉ có 14 bài và **đã chứng tỏ thiếu** (DeepSIRT không có trong đó), nên **không được dùng làm bằng chứng**.
- Chưa tra được **SirtSAGE** và **RAG-msCNN** trong lần tìm này (chỉ có mô tả nội bộ trong repo).

---

## 7. Bảng so sánh tổng hợp và phán quyết ba trục

### Bảng so sánh

| Công trình | Năm | Bài toán | Đầu vào | Nhãn / Dữ liệu | Đặc hiệu isoform? | Phương pháp | Đánh giá | Chồng lấn / khác với đề xuất |
|---|---|---|---|---|---|---|---|---|
| **Ridgeway et al.** [DOI](https://doi.org/10.1038/s42004-025-01717-6) | 2025 | Cơ chất của enzyme PTM (SET8 + SIRT1–7) | Peptide 13 aa (SIRT) / 15 aa (SET8) | Mảng peptide Rauh 2013, 6.801 peptide, 443 đặc trưng; nhãn **nhị phân** | **Có, 7 mô hình rời** | LDA/cây + oversampling, ensemble xếp tầng với **MuSiteDeep** | F-score/precision trên holdout; **MS in-cell: SIRT2 64/149 = 43,0%; SET8 3/9** | **Đối thủ trực tiếp.** Đề xuất khác ở: PLM thay 443 đặc trưng, 1 mô hình 7 đầu ra thay 7 mô hình rời, nhãn thang độ thay nhị phân, in-cell thành RQ thay một con số. **Nhưng cả PLM và nhãn thang độ đều là "future work" họ tự công bố** |
| **DeepSIRT** [DOI](https://doi.org/10.1016/j.compbiolchem.2021.107514) | 2021 | **Target** của sirtuin + khu trú dưới tế bào | Chuỗi protein target | Danh sách target SIRT1–7 có annotate khu trú | **Có, 7 thành viên** | 1D-CNN, 3 phương pháp trích đặc trưng, giảm đồng dạng | 2 tập độc lập; Sn 85,77%, Sp 97,32%, MCC 0,82 | **⚠️ Nhóm Prof. Ou.** Mức **protein**, không phải residue. Chồng lấn ở từ "isoform-specific SIRT1–7" → phải nêu chủ động |
| **NAD_MCNN** [DOI](https://doi.org/10.1111/cbdd.70085) | 2025 | Vị trí gắn **NAD+ trên chính enzyme** | Chuỗi enzyme sirtuin | Vị trí gắn cofactor | n/a (enzyme là đầu vào) | PLM + mCNN nhiều cửa sổ | AUC 0,9733 / 0,9701 | **Nhóm Prof. Ou.** Khác bài toán hoàn toàn (cofactor vs cơ chất). Khung PLM+mCNN là cái đề tài mượn lại |
| **Deep-PLA** [DOI](https://doi.org/10.1093/bib/bbz107) | 2020 | Acetyl hóa đặc hiệu **HAT/HDAC** | Cửa sổ chuỗi quanh K | Cơ chất curate từ tài liệu, 7 HAT + **9 HDAC** | Có (theo enzyme) | DNN + AAC/CKSAAP/PSSM/BE, PSO | CV 5/10-fold + tập độc lập HAT phi-người | **Tiền lệ "đặc hiệu enzyme" từ 2020.** SIRT1–7 **là HDAC class III** → phải kiểm 9 HDAC đó gồm những ai |
| **GPS-PAIL** [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5177928/) | 2016 | Acetyl hóa đặc hiệu từng **KAT** | Chuỗi | Vị trí curate | Có (theo KAT) | Scoring matrix | CV | Tiền lệ còn sớm hơn. Làm yếu mọi tuyên bố "đầu tiên dự đoán PTM đặc hiệu enzyme" |
| **Johnson et al. (kinome atlas)** [DOI](https://doi.org/10.1038/s41586-022-05575-3) | 2023 | Đặc hiệu cơ chất 303 kinase Ser/Thr | Peptide (PSPA) | **Positional scanning peptide array** (in vitro) | Có, 303 kinase | PWM / motif | Gán kinase cho **toàn bộ** phosphoproteome Ser/Thr người; kinase đã biết chỉ **<4%** vị trí | **Analogue gần nhất, và nó đã làm bước in vitro → toàn proteome ở quy mô lớn hơn.** Khác: PWM không học sâu, không có nhãn âm trong tế bào |
| **"Validity of cell-extracted proteome…"** [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/) | 2024 | Motif mảng vs motif dịch chiết tế bào | Peptide | PL-PWM (Johnson) vs dịch chiết tế bào | Theo kinase | PWM | So chất lượng dự đoán, **3 kinase** | **⚠️ Bằng chứng ngược:** mảng cho dự đoán **ngang** motif từ dịch chiết → khoảng cách in vitro–trong tế bào có thể nhỏ hơn giả định |
| **benchmarKIN** [DOI](https://doi.org/10.1038/s41467-025-59779-y) | 2025 | Benchmark suy luận hoạt tính kinase | Phosphoproteome | 184 cặp / 30 kinase / 62 perturbation + khối u | Theo kinase | Nhiều phương pháp | AUROC trên perturbation; **đã thử Kinase Library và Phosformer** | Cho thấy cộng đồng kinase **đã có** benchmark in-cell cho dự đoán từ mảng. Mượn được phương pháp luận |
| **Phosformer / Phosformer-ST** [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11968300/) | 2023–25 | Phospho đặc hiệu kinase | Cặp (kinase, peptide) | Cơ chất đã biết | Có | Transformer; giải thích được | Benchmark peptide-level; bài khác báo MCC 0,05 | Ý "một mô hình điều kiện hóa theo enzyme" đã có. **Mức peptide, không mức residue** → chỗ đề tài phân biệt được |
| **Prot2Token + bản mở rộng** [bioRxiv](https://www.biorxiv.org/content/10.1101/2025.03.12.642740v2) | 2024–25 | Đa nhiệm protein; phospho đặc hiệu kinase | Chuỗi | 6 PTM + kinase | Có (kinase) | ESM-2 + decoder tự hồi quy; **tự nhận zero-shot đầu tiên** | Benchmark chuẩn | Đối thủ của **đề tài dự phòng B**. ⚠️ **Không phải NeurIPS 2025** — là bioRxiv + LMRL@ICLR 2025, phải sửa citation |
| **DARKIN** [DOI](https://doi.org/10.1093/bioinformatics/btaf480) | 2025 | Benchmark zero-shot phosphosite–dark kinase | Chuỗi | Vị trí đã biết | Có | So nhiều PLM, k-NN + bilinear | Zero-shot splits; ESM tốt nhất | Cho thấy benchmark zero-shot theo enzyme đã chuẩn hóa ở phía kinase |
| **COMPASS-PTM** [DOI](https://www.nature.com/articles/s41467-026-73148-3) | 2026 | PTM **đa nhãn** + crosstalk | Chuỗi | dbPTM + qPTM, "dual long-tail" | Không (theo loại PTM) | PLM tinh chỉnh + dual-modal + crosstalk prompting | Benchmark đa nhãn, **+122% F1 tương đối** | **Làm yếu trục 3:** "đa nhãn PTM với PLM" đã là SOTA. Khác: nhãn của nó là *loại PTM*, không phải *isoform enzyme* |
| **MTPrompt-PTM** [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190693/) | 2025 | 13 loại PTM, đa nhiệm | Chuỗi | dbPTM-kiểu | Không | Prompt tuning PLM biết cấu trúc + **nhãn mềm/KD** | Multi-task | Tiền lệ cho "một mô hình nhiều đầu ra + nhãn mềm xử lý bất định" |
| **PDeepPP** (qua [PMC13389326](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389326/)) | ~2025 | Vị trí PTM tổng quát | Chuỗi | Benchmark PTM | Không | **ESM-2 + transformer-CNN song song** | SOTA được dẫn | **Làm yếu trục 3:** "ESM-2 + CNN đa thang" đã công bố |
| **ESMBind / QBind** [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full) | 2023 | Vị trí gắn **và PTM** | Chuỗi | Token classification | Không | **LoRA / QLoRA trên ESM-2** | So full fine-tuning | **Làm yếu trục 3:** "ESM-2 + LoRA cho PTM" đã công bố |
| **EPuL / PU-glycosylation** [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6151806/) | 2017–19 | PU learning cho vị trí PTM | Chuỗi | Dương + unlabeled | Không | PU learning | CV | Tiền lệ xử lý nhãn âm không đáng tin. Chưa áp cho acetyl hóa đặc hiệu enzyme |
| **Rauh et al.** [URL](https://www.nature.com/articles/ncomms3327) | 2013 | Đặc hiệu cơ chất SIRT1–7 (thực nghiệm) | Peptide 13 aa | **6.802 vị trí × 7 isoform**, nhãn liên tục | Có | Mảng peptide (không ML) | Xác nhận 3 protein nguyên | Nguồn nhãn huấn luyện. Hoàn toàn in vitro |

### Phán quyết ba trục

**Trục 1 — tính mới của vấn đề sinh học: YẾU–TRUNG BÌNH.** `[suy luận]`
"Dự đoán cơ chất SIRT1–7 đặc hiệu isoform" **đã được công bố hai lần**: Ridgeway 2025 ở mức residue với đúng bảy isoform, và DeepSIRT 2021 ở mức protein với đúng bảy isoform **bởi nhóm của đồng tác giả thường xuyên của GVHD**. Phần còn trống là **mức residue × một mô hình đa nhãn × đánh giá trong tế bào**, tức một khe hẹp giữa hai bài đã có, không phải một vùng trắng. Phát biểu an toàn: "em không mở bài toán mới; em lấp khe giữa DeepSIRT (mức protein) và Ridgeway (mức residue, 7 mô hình rời)."

**Trục 2 — tính mới của dữ liệu đánh giá / benchmark: MẠNH NHẤT, nhưng không như đang nghĩ.** `[suy luận]`
Không tìm thấy công trình nào dựng **tập đánh giá trong tế bào có cả nhãn dương và nhãn âm, cho nhiều isoform SIRT** `[chưa tìm thấy, không kết luận là chưa từng có]`. Đây là tuyên bố tính mới **duy nhất** tôi tìm được mà chưa bị bài nào chiếm. Nhưng nó hẹp hơn tuyên bố trong `topic-final-recommendation.md`: Ridgeway **đã** đánh giá in-cell (43,0% cho SIRT2, 3/9 cho SET8), và cộng đồng kinase đã có cả atlas in vitro quy mô lớn (Johnson 2023) lẫn benchmark in-cell được bình duyệt (benchmarKIN 2025) lẫn một bài so trực tiếp mảng vs dịch chiết tế bào (PMC11447832). **Đóng góp thật nằm ở nhãn âm và ở chỉ số ngoài precision (MCC/AUPRC), không ở ý tưởng "đánh giá in-cell".**

**Trục 3 — tính mới của phương pháp tính toán: YẾU.** `[suy luận]`
Theo yêu cầu, tôi đã kiểm riêng từng mảnh của "ESM-2 + LoRA + mCNN + conformal":
- ESM-2 + CNN đa thang cho PTM: **đã công bố** (PDeepPP) `[chưa kiểm]`
- LoRA trên ESM-2 cho PTM: **đã công bố** (ESMBind/QBind) `[tác giả báo cáo]`
- Đa nhãn PTM với PLM: **đã công bố nhiều lần** (COMPASS-PTM, MTPrompt-PTM, AstraPTM, MIND-S) `[chưa kiểm]`
- Nhãn mềm / bất định nhãn trong PTM: **đã công bố** (MTPrompt-PTM, KD) `[chưa kiểm]`
- Conformal prediction cho PTM: **không tìm thấy** `[chưa tìm thấy, không kết luận là chưa từng có]` — xác nhận lại kết quả của `compute-novelty-directions.md` mục C4
- Hồi quy trên nhãn thang độ của mảng peptide: **không tìm thấy bài đã làm**, nhưng **chính Ridgeway đã công bố nó như future work của họ** `[tự kiểm]`

Kết luận trục 3: **tổ hợp này không phải tính mới.** Hai mảnh còn chưa ai làm (conformal cho PTM; nhãn thang độ mảng peptide) đều nhỏ, và mảnh thứ hai đã bị tác giả gốc công bố ý định làm. Đề tài nên trình bày trục 3 là **"thực hiện và đo một cách kiểm soát hai hướng mà bài 2025 tự nêu, cộng một thành phần chưa thấy ở PTM (conformal)"**, không phải "phương pháp mới".

### Ba việc phải làm trước khi lên slide `[suy luận]`

1. **Đọc toàn văn Deep-PLA** để biết 9 HDAC là ai. Nếu có SIRT → phải đổi cách phát biểu toàn bộ trục 1.
2. **Đọc toàn văn DeepSIRT** và thêm nó vào slide 1 một cách chủ động, cùng NAD_MCNN, trong bảng ba dòng ở mục 6.
3. **Sửa citation Prot2Token** (bioRxiv 2024 + LMRL@ICLR 2025, **không phải NeurIPS 2025**) trong mọi tài liệu nội bộ.

### Câu hỏi thêm cho GVHD tuần 6 `[suy luận]`

- Bài Ridgeway 2025 **tự công bố** hai việc tương lai đúng bằng hai đóng góp chính của em (PLM, và hồi quy trên mật độ SPOT). Thầy thấy việc "làm trước việc tương lai của người khác" là đóng góp đủ cho luận văn, hay là rủi ro bị làm trước?
- Nhóm Prof. Ou đã có **DeepSIRT (2021)** cho target SIRT1–7 ở mức protein. Thầy có coi đề tài này là tiếp nối DeepSIRT (hạ xuống mức residue), và nếu vậy có nên xin dữ liệu/mã của DeepSIRT không?

---

## 8. Nguồn (gom lại)

- Ridgeway N.H., Chopra A., Lukinović V., Feldman M., Charih F., Levy D., Green J.R., Biggar K.K. (2025), *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem 8:340 — [DOI 10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6) · [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) · mã: https://github.com/nashirag/ML-Hybrid_Ensemble_Method
- Shah S.M.A., Taju S.W., Dlamini B.B., Ou Y.-Y. (2021), *DeepSIRT: A deep neural network for identification of sirtuin targets and their subcellular localizations*, Comput Biol Chem 93:107514 — [DOI 10.1016/j.compbiolchem.2021.107514](https://doi.org/10.1016/j.compbiolchem.2021.107514)
- Le V.-T., Liu Y.-C., Chang Y.-Y., Lee Y.-C., Lin Y.-J., Malik M.-S., Ou Y.-Y. (2025), *NAD_MCNN*, Chem Biol Drug Des 105(4):e70085 — [DOI 10.1111/cbdd.70085](https://doi.org/10.1111/cbdd.70085)
- Yu K. và cộng sự (2020), *Deep learning based prediction of reversible HAT/HDAC-specific lysine acetylation*, Brief Bioinform 21(5):1798 — [DOI 10.1093/bib/bbz107](https://doi.org/10.1093/bib/bbz107)
- Johnson J.L. và cộng sự (2023), *An atlas of substrate specificities for the human serine/threonine kinome*, Nature — [DOI 10.1038/s41586-022-05575-3](https://doi.org/10.1038/s41586-022-05575-3) · [PMC9876800](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876800/)
- *The intrinsic substrate specificity of the human tyrosine kinome* (2024), Nature — [s41586-024-07407-y](https://www.nature.com/articles/s41586-024-07407-y)
- *Validity of the cell-extracted proteome as a substrate pool for exploring phosphorylation motifs of kinases* (2024) — [PMC11447832](https://pmc.ncbi.nlm.nih.gov/articles/PMC11447832/)
- *Comprehensive evaluation of phosphoproteomic-based kinase activity inference* (benchmarKIN, 2025), Nat Commun — [DOI 10.1038/s41467-025-59779-y](https://doi.org/10.1038/s41467-025-59779-y) · [PMC12098709](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12098709/) · [GitHub](https://github.com/saezlab/kinase_benchmark)
- *Benchmarking substrate-based kinase activity inference using phosphoproteomic data* (2017), Bioinformatics 33(12):1845 — [link](https://academic.oup.com/bioinformatics/article/33/12/1845/2991427)
- *Predicting Kinase-Specific Phosphorylation Sites with Pretrained Protein Language Models* — [bioRxiv 2025.03.12.642740v2](https://www.biorxiv.org/content/10.1101/2025.03.12.642740v2)
- Prot2Token — [bioRxiv 2024.05.31.596915](https://www.biorxiv.org/content/10.1101/2024.05.31.596915.full.pdf) · *Extending Prot2Token* (LMRL@ICLR 2025) — [bioRxiv 2025.03.03.641065](https://www.biorxiv.org/content/10.1101/2025.03.03.641065v1.full) · [GitHub](https://github.com/mahdip72/prot2token)
- *Kinase-substrate prediction using an autoregressive model* (2025) — [PMC11968300](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11968300/)
- DARKIN (2025), Bioinformatics 41(11):btaf480 — [link](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017) · [PMC12579546](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12579546/)
- DeepKinZero — [bioRxiv 670638](https://www.biorxiv.org/content/10.1101/670638.full.pdf)
- COMPASS-PTM / *Learning the PTM code…* — [Nat Commun s41467-026-73148-3](https://www.nature.com/articles/s41467-026-73148-3) · [arXiv 2510.23492](https://arxiv.org/pdf/2510.23492)
- MTPrompt-PTM — [PMC12190693](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190693/)
- AstraPTM — [bioRxiv 2025.02.20.639276](https://www.biorxiv.org/content/10.1101/2025.02.20.639276.full.pdf)
- MIND-S — [S2667237523000450](https://www.sciencedirect.com/science/article/pii/S2667237523000450)
- PTMGPT2 — [Nat Commun s41467-024-51071-9](https://www.nature.com/articles/s41467-024-51071-9) · [GitHub](https://github.com/pallucs/PTMGPT2)
- ESMBind / QBind — [bioRxiv 2023.11.13.566930](https://www.biorxiv.org/content/10.1101/2023.11.13.566930v1.full)
- SE(3)-equivariant multi-modal PTM engine (2026), Commun Chem — [s42004-026-02062-y](https://www.nature.com/articles/s42004-026-02062-y) · [PMC13389326](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389326/)
- SAPP — [S0010482525015227](https://www.sciencedirect.com/science/article/pii/S0010482525015227) · DeepPTMPred — [bbag321](https://academic.oup.com/bib/article/27/3/bbag321/8709888)
- TransPTM (2024), Brief Bioinform 25(3):bbae219 — [link](https://academic.oup.com/bib/article/25/3/bbae219/7667560)
- GPS-PAIL — [PMC5177928](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5177928/)
- EPuL — [PMC6151806](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6151806/) · PU-learning glycosylation — [PMC6404354](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6404354/)
- OmniESI — [arXiv 2506.17963](https://arxiv.org/html/2506.17963v1) · VIPER — [bioRxiv 2024.06.21.599972](https://www.biorxiv.org/content/10.1101/2024.06.21.599972.full.pdf) · ESI low-homology shift — [arXiv 2606.22823](https://arxiv.org/pdf/2606.22823)
- ATP_mCNN — [S0010482524016263](https://www.sciencedirect.com/science/article/abs/pii/S0010482524016263) · DeepPLM_mCNN — [S1476927124000434](https://sciencedirect.com/science/article/abs/pii/S1476927124000434)
- Rauh D. và cộng sự (2013), Nat Commun 4:2327 — https://www.nature.com/articles/ncomms3327

> Thông tin từ PubMed: các mục Ridgeway 2025, DeepSIRT 2021 và NAD_MCNN 2025 ở trên được truy xuất từ PubMed/PubMed Central trong phiên này; DOI đã dẫn kèm theo từng mục.
