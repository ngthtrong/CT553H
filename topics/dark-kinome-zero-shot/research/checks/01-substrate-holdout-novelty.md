# Substrate-side generalization trong kinase–phosphosite link prediction: đã ai làm chưa?

> Ghi chú khảo sát, 10/10/2026. Nhãn nguồn: **[SOURCE]** = tác giả tự công bố, **[ANALYSIS]** = suy luận của tôi từ nguồn, **[UNVERIFIED]** = không truy cập được.
> Bối cảnh: audit split mặc định của DARKIN cho thấy kinase hoàn toàn disjoint (0 overlap) nhưng 923/1414 = 65,3% dòng test thuộc substrate protein đã xuất hiện trong train, và 462/1414 = 32,7% dòng test dùng chung site key (accession, residue) với train.

---

## Câu hỏi 1: Đã có công trình nào evaluate protocol giữ lại ĐỒNG THỜI novel kinase VÀ novel substrate protein/site chưa?

### Takeaway

Khái niệm **không mới**: SAGEPhos (ICLR 2025) đã đặt tên và cài đặt riêng rẽ cả *kinase-cold-start* và *substrate-cold-start*, và **nói thẳng rằng setting hai chiều đồng thời là "not feasible"** trên dataset của họ. Nhưng tôi **không tìm thấy** công trình nào thực sự *evaluate* setting hai chiều, và **không công trình nào làm điều đó trên DARKIN**. Quan trọng hơn: nhóm DARKIN **đã nhìn thấy vấn đề site overlap và chủ động gạt bỏ nó bằng lý lẽ**, chứ không phải vô tình bỏ sót — nên khung "phát hiện lỗi bị bỏ qua" là **không đúng sự thật**, phải đổi sang khung "kiểm chứng thực nghiệm một lập luận chưa được kiểm chứng".

### Cited Findings

**DARKIN đã biết và đã chủ động từ chối site-based split (bằng chứng mạnh nhất, trích nguyên văn):**

- [SOURCE] "Note that a single phosphosite can be targeted by multiple kinases, which may result in the same phosphosite appearing in both the training and test sets with different kinase labels." — [DARKIN, Bioinformatics 41(11) btaf480, bản PDF tác giả](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] "While a site-based split of the train, validation, and test set is possible, it is difficult to obtain a balanced split based on all four criteria. **More importantly, it is not necessary, as the aim is to predict the right kinases for a known phosphosite.** Even when a phosphosite appears in both splits, the associated kinase labels are disjoint across training and test sets. The model is still required to generalize to unseen kinases. It is indeed more challenging for the model, as it has previously associated this site with a different kinase and now needs to predict its association with the unseen test kinase. **Therefore, this strategy does not affect the integrity of the evaluation process.**" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] DARKIN **đã đo** tỉ lệ site mới/site trùng trong test: "we report the sites unique to the test set or shared with the validation and training data in the Fig. 4, available as supplementary data" và "seen and novel sites in the test dataset (Fig. 4...)". Tức là con số của tôi (65,3% / 32,7%) trùng ý với một hình phụ lục đã có. — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] Ràng buộc tương tự **chỉ áp cho kinase, không áp cho substrate**: "kinases with sequence similarity are grouped and assigned exclusively to the same set (train, validation, or test)... Sequence similarity is determined by sequence identity calculated after pairwise global alignment"; ngưỡng là "kinases with at least 90% sequence identity are grouped and are randomly defined as entirely train or test kinases altogether". — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] Và ngay ở bước curation, DARKIN nói rõ không lọc substrate: "Kinase–phosphosite associations, which are related to non-human kinases, are removed. **We did not apply the same restriction to substrates**, as substrates from the model organisms are used to probe the interactions." — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] DARKIN có cả một đoạn discussion về data leakage, dẫn tới drug–target prediction (Chatterjee et al. 2023), drug synergy (2025), genomics (Whalen et al. 2022), link prediction (Brière et al. 2025), Bernett et al. 2024 — tức là nhóm này **ý thức rất rõ về văn hoá leakage audit**, nhưng áp dụng nó chỉ ở trục kinase. — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)

**SAGEPhos: đã có substrate-cold-start, và đã tuyên bố two-sided là bất khả thi:**

- [SOURCE] "we modified the split methods to simulate a cold-start scenario (Zhu et al., 2021), introducing entirely new kinase or substrate sequences in the test set, denoted respectively as **Kinase-cold-start** and **Substrate-cold-start**." — [SAGEPhos, ICLR 2025 proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Footnote then-and-there: "**Due to the high interconnectivity (99.9%) in our dataset, with most sites linked to multiple kinases and vice versa, creating a truly cold-start test set with completely unseen kinases and substrates was not feasible.**" — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Cách cài đặt substrate-cold-start của SAGEPhos: "for substrate cold-start, dataset splitting was based on **substrate 11-mer sequence identity**. All data points with identical substrate sequences were assigned to the same set to avoid sequence overlap". — [SAGEPhos ICLR PDF, Appendix A](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)

**Không tìm thấy công trình nào khác làm two-sided:**

- [SOURCE] Trong các công trình kinase–substrate autoregressive 2025, framing vẫn là unseen-kinase: Esmaili et al. "can predict substrates for a kinase in case of no known substrates", redundancy reduction bằng CD-HIT 0.7, negative pairs sinh theo Euclidean distance trong sequence space + hard negatives theo ESM-2 kinase embedding; **snippet không nêu split scheme theo substrate**. — [Kinase-substrate prediction using an autoregressive model, PMC11968300](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11968300/)
- [SOURCE] Tiền lệ cũ gần nhất là Predikin: chia site thành test 10% / train 90% và "omitted those sites in the training set linked to the same kinase" khi scoring — đây là guard theo kinase, không phải theo substrate protein. — [kết quả tìm kiếm dẫn tới Predikin](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2912303/)
- [SOURCE] SnapKin báo cáo 5-fold cross-validation nhưng không nêu fold chia theo substrate hay không. — [SnapKin, PMC10632189](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10632189/)

### Inferences

- [ANALYSIS] **Claim "lần đầu tiên đề xuất two-sided holdout cho kinase–substrate" là KHÔNG bảo vệ được.** SAGEPhos đã đặt tên hai trục cold-start và đã công khai bàn tới setting hợp nhất. Nếu nói "chưa ai nghĩ tới", GVHD hoặc reviewer chỉ cần mở footnote SAGEPhos là bác được.
- [ANALYSIS] Claim **vẫn bảo vệ được** nếu đổi sang: (a) **chưa ai lượng hoá** mức tụt performance do substrate overlap **trên DARKIN**; (b) lập luận của DARKIN ("does not affect the integrity of the evaluation process") là một **giả định chưa được kiểm chứng bằng thực nghiệm** — DARKIN đưa ra lý lẽ chứ không đưa ra ablation; (c) tuyên bố "not feasible" của SAGEPhos là một **claim có thể bác được bằng thực nghiệm** (ví dụ bằng bipartite-component / greedy protein-level partition, chấp nhận hy sinh một phần dữ liệu).
- [ANALYSIS] Substrate-cold-start của SAGEPhos **yếu hơn hẳn** điều cần kiểm: nó chỉ loại trùng **11-mer window giống hệt**, không phải loại trùng **substrate protein**. Một site S473 và một site S481 của cùng protein vẫn nằm hai bên split. Nên "leave-protein-out" ở mức accession **vẫn là khoảng trống thật**, chặt hơn mọi thứ đã có trong literature kinase.
- [ANALYSIS] Thiết kế dễ bảo vệ nhất cho luận văn: giữ nguyên trục kinase của DARKIN (không sửa), chỉ thêm **một trục thứ hai** và báo cáo AP phân rã theo 3 tầng test rows: (i) substrate protein mới, (ii) protein cũ nhưng site mới, (iii) site đã thấy trong train. Đây là phân tích *bổ sung*, không phải *phủ định* DARKIN — ít gây xung đột với nhóm tác giả, và vẫn là đóng góp đo đếm được.

### Gaps

- Supplementary Fig. 4 của DARKIN ("seen and novel sites in the test dataset") **[UNVERIFIED]** — tôi không tải được file supplementary (nằm sau academic.oup.com). Không biết họ chỉ đếm, hay có báo cáo AP phân rã theo seen/novel. **Đây là việc bắt buộc phải kiểm trước khi chốt claim novelty**, vì nếu Fig. 4 đã có AP phân rã thì đóng góp bị thu hẹp rất nhiều.
- Không khẳng định được "không ai từng làm two-sided". Tôi đã tìm với các cụm: "leave-protein-out", "substrate holdout", "unseen kinase unseen substrate", "both-cold", "held-out substrate proteins" — **đã tìm và không thấy instance nào**, nhưng *không* phải *confirmed absent*. Chưa quét: Google Scholar full-text, các bài phosphoproteomics clinical 2026.

---

## Câu hỏi 2: SAGEPhos — task, dataset, split, metrics, có dùng DARKIN không?

### Takeaway

SAGEPhos là **kinase-specific phosphosite binary classification** (có/không phosphorylate), **không phải** multilabel ranking kinase như DARKIN; dataset tự xây 18.360 positive từ Phospho.ELM + PhosphoNetworks + PhosphoSitePlus + AlphaFoldDB; **không dùng DARKIN, không so với DeepKinZero**. Cảnh báo: **bản arXiv đã bị tác giả rút (withdrawn)** vì "significant disagreements" trong nhóm, dù bản ICLR 2025 vẫn còn trên proceedings.

### Cited Findings

- [SOURCE] Task: "Structure-aware kinAse-substrate bio-coupled and bio-auGmented nEtwork for **Phosphorylation site prediction**", nhắm vào "individual kinase-based approaches [that] focus solely on sequence inputs, neglecting crucial structural information". Hàm học là `f : p'_i → y_i`, với kinase info được broadcast vào n-mer segment → **binary, kinase-conditioned**. — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Dataset: Phospho.ELM (Dinkel 2010) + PhosphoNetworks (Hu 2014) + PhosphoSitePlus (Hornbeck 2012), structure từ AlphaFoldDB; "final dataset comprises **18,360 positive samples**"; chỉ giữ human sites, chỉ giữ entry có structure trong AlphaFoldDB. — [SAGEPhos ICLR PDF, Appendix A](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Negatives: "(1) known phosphorylation sites that are validated substrates of other kinases, and (2) experimentally verified phosphorylatable sites lacking reported kinase associations, resulting in a **balanced 1:1 ratio**". — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Split: tỉ lệ 8:1:1; ba partition — **Warm-start** (random), **Kinase-cold-start** (chia theo kinase identity, không overlap kinase), **Substrate-cold-start** (chia theo 11-mer substrate sequence identity). — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Metrics: Accuracy, AUC-ROC, AUC-PRC, FPR. Warm-start: SAGEPhos **80,6 Acc / 88,3 AUC-ROC / 86,2 AUC-PRC / 21,7 FPR**; baseline tốt nhất MusiteDeep 73,5 / 78,5 / 7,3 / 26,4 và Phosformer-ST 64,7 / 78,9 / 79,0 / 95,6. Claim headline: "almost 10% and 12% improvements in prediction accuracy and AUC-ROC". — [SAGEPhos ICLR PDF, Table 1](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Kết quả cold-start (Table 2) có baselines: Kinase-cold-start MusiteDeep 68,3 Acc / 73,8 AUC-ROC / 6,4 AUC-PRC; Phosformer-ST 61,0 / 72,7 / 73,3. Substrate-cold-start MusiteDeep 67,5 / 22,2 / 0,8; Phosformer-ST 63,5 / 79,3 / 79,7. Tác giả nhận xét: "compared to warm start data, **substrate cold start dataset hardly affected performance**, indicating our model's [robustness]". — [SAGEPhos ICLR PDF, Table 2](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Zero-shot phụ: thử CDK17 (kinase unseen) với substrate từ Johnson et al. 2023, cộng 4 kinase unseen khác; so với MusiteDeep, SAGEPhos đạt 91,6 ở một chỉ số trong Table A2. — [SAGEPhos ICLR PDF, Appendix C](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] **DARKIN không được nhắc tới một lần nào** trong toàn văn SAGEPhos (grep "DARKIN", "DeepKinZero" = 0 hit). — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] Code: https://github.com/ZhangJJ26/SAGEPhos. Tác giả từ CUHK và Zhejiang University. — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] **Bản arXiv v2 đã bị RÚT**: trang arXiv:2502.07384 ghi tác giả rút vì "significant disagreements" trong nhóm và cần "further verification". — [arXiv:2502.07384](https://arxiv.org/abs/2502.07384)

### Inferences

- [ANALYSIS] SAGEPhos **không phải competitor trực tiếp** của DARKIN: khác task (binary classification vs multilabel kinase ranking), khác metric (AUC-ROC vs macro AP), khác dataset, negatives tự sinh 1:1. Không thể so số giữa hai bên.
- [ANALYSIS] Số của SAGEPhos nên dùng **rất thận trọng** trong đề cương: arXiv version bị rút vì nội bộ nhóm không đồng thuận là một cờ đỏ về độ tin cậy của kết quả. Nên trích SAGEPhos **cho phần thiết kế protocol (khái niệm cold-start hai trục)** chứ không trích làm mốc SOTA.
- [ANALYSIS] Nhận xét "substrate cold start hardly affected performance" của SAGEPhos là **lập luận thuận lợi cho đề tài**, không phải bất lợi: nó cho thấy một kết luận đã được công bố mà **chưa ai kiểm lại trên benchmark khác**, và nó đạt được dưới định nghĩa substrate-cold-start yếu (11-mer exact match). Luận văn có thể kiểm lại cùng câu hỏi dưới định nghĩa chặt hơn (protein-level) trên DARKIN và xem kết luận còn đứng không.
- [ANALYSIS] FPR 95,6% của Phosformer-ST ở warm-start và AUC-PRC 0,8 của MusiteDeep ở substrate-cold-start cho thấy bảng baseline của SAGEPhos có khả năng baseline bị cấu hình kém (under-tuned). Cẩn thận khi dẫn.

### Gaps

- **[UNVERIFIED]** Dòng SAGEPhos trong Table 2 (cold-start) không extract được sạch khỏi PDF — tôi có số của baselines nhưng **không có số cold-start của chính SAGEPhos**. Phải mở lại PDF/Table 2 bằng mắt nếu cần trích.
- **[UNVERIFIED]** Trang OpenReview của SAGEPhos (review scores, phản biện của reviewer về split) không tìm được qua search. Đáng tìm lại bằng openreview.net trực tiếp — review có thể chứa chính xác câu hỏi về substrate leakage.

---

## Câu hỏi 3: DeepKinZero — zero-shot setting là gì, có kiểm soát substrate overlap không?

### Takeaway

DeepKinZero (Bioinformatics 36(12):3652–3661, 2020; cùng nhóm Taştan với DARKIN) là **tiền thân trực tiếp** của DARKIN. Zero-shot của nó chia kinase theo *số lượng site* (kinase nhiều site → train, kinase ít site → test), và **hoàn toàn không có bất kỳ kiểm soát nào về substrate protein hay phosphosite overlap** — kể cả không có sequence-similarity split ở trục nào.

### Cited Findings

- [SOURCE] Dataset: PhosphoSitePlus tải 03/2018, loại isoform và fusion kinase, còn **13.426 sites / 343 kinases**. — [DeepKinZero bioRxiv full text](https://www.biorxiv.org/content/10.1101/670638.full)
- [SOURCE] Split: "Kinases with more than 5 sites are considered as training classes" → 124 train kinases / 12.901 sites; validation = 17 kinase có đúng 5 sites / 80 sites; test (zero-shot) = 112 kinase còn lại, mỗi kinase <5 sites / 237 sites. — [DeepKinZero bioRxiv](https://www.biorxiv.org/content/10.1101/670638.full)
- [SOURCE] Kinase separation: theo Xian et al., "keep[s] the zero-shot kinases well apart from the rest of the classes in learning the models and parameter tuning"; "the sets of common and rare kinases are disjoint". — [DeepKinZero bioRxiv](https://www.biorxiv.org/content/10.1101/670638.full)
- [SOURCE] Substrate: bài **không bàn tới substrate protein overlap**; **không có protein-level hay sequence-similarity split** nào; chỉ ghi nhận "a phosphosite occasionally can indeed be phosphorylated by more than one kinase". — [DeepKinZero bioRxiv](https://www.biorxiv.org/content/10.1101/670638.full)
- [SOURCE] Bộ test ngoài (Phospho.ELM): tác giả "removed all the kinases and their associated phosphosites that were in our training and validation set" — tức là xử lý overlap ở trục kinase, **không kiểm site overlap**. — [DeepKinZero bioRxiv](https://www.biorxiv.org/content/10.1101/670638.full)
- [SOURCE] DARKIN tự phê bình split của DeepKinZero: "While this splitting strategy closely mirrors the real-world scenario of the deployed model, **the limited number of examples for each class in the test set complicates the reliable estimation of evaluation performance**" → lý do DARKIN đảo vai light/dark kinase. — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)
- [SOURCE] Có bản mở rộng: "Improving DeepKinZero with protein language models and transductive learning" (Sabancı). **[UNVERIFIED]** nội dung — chưa đọc. — [research.sabanciuniv.edu/51540](https://research.sabanciuniv.edu/id/eprint/51540/)

### Inferences

- [ANALYSIS] **Bất khớp số liệu trong bản bioRxiv DeepKinZero**: 12.901 + 80 + 237 = 13.218 ≠ 13.426; và trong test 215 + 16 + 2 = 233 ≠ 237. Có thể là sai sót biên tập của bản preprint, cần đối chiếu bản Bioinformatics chính thức trước khi trích con số.
- [ANALYSIS] Cả dòng DeepKinZero → DARKIN đều **chỉ tiến bộ ở trục kinase** (DeepKinZero: không ràng buộc similarity → DARKIN: thêm 90% identity grouping + group stratification). Trục substrate **không được chạm vào ở cả hai thế hệ**. Đây là mạch kể (narrative) thuyết phục cho đề cương: lỗ hổng có hệ thống trong một dòng nghiên cứu 6 năm, chứ không phải nitpick một bài lẻ.
- [ANALYSIS] Vì DARKIN được xây đúng lên trên DeepKinZero của cùng nhóm, phản biện "sao nhóm tác giả không làm" có câu trả lời tự nhiên: ưu tiên thiết kế của họ là *đảm bảo đủ mẫu mỗi kinase class trong test*, và site-based split xung đột với mục tiêu đó (họ nói rõ: "difficult to obtain a balanced split based on all four criteria").

### Gaps

- Bản Bioinformatics chính thức của DeepKinZero (có thể khác bản bioRxiv về số liệu) **[UNVERIFIED]** — paywalled, chưa đọc.
- Phiên bản "Improving DeepKinZero with pLMs and transductive learning" **[UNVERIFIED]** — có khả năng là transductive (dùng test phosphosites không nhãn khi train), nếu đúng thì đáng chú ý vì transductive learning *làm trầm trọng* vấn đề substrate overlap. Cần đọc.

---

## Câu hỏi 4: Prot2Token — có bao gồm kinase–substrate linkage không, split thế nào?

### Takeaway

**Có.** Prot2Token (arXiv:2505.20589, bioRxiv 2024.05.31.596915) có task "Kinase phosphorylation" và "Kinase group classification". Điểm quan trọng: Prot2Token **đã dùng CD-HIT 70% trên substrate sequence** và chia train/val **theo unique substrate**, nhưng test held-out lại theo **kinase group hiếm** chứ không phải kinase disjoint hoàn toàn. Nó **không dùng DARKIN**.

### Cited Findings

- [SOURCE] Danh sách task gồm "Kinase phosphorylation" (nhóm Other/PTM) và "Kinase group classification" (nhóm Classification), cạnh EC, GO, Fold, Human PPI, DeepLoc 2.0, binding site, structure prediction, TargetP 2.0, v.v. Bài dùng cụm "substrate-kinase phosphorylation prediction", **không** dùng "kinase-substrate interaction". — [Prot2Token arXiv HTML, Table 11](https://arxiv.org/html/2505.20589v2)
- [SOURCE] Dataset kinase phosphorylation: **GPS 6.0**, 24.160 phosphorylation sites; sau ID mapping còn 13.374 sequences có kinase info; cuối cùng **386 kinase types thuộc 12 groups**. — [Prot2Token arXiv HTML, Appendix A.3.4](https://arxiv.org/html/2505.20589v2)
- [SOURCE] Redundancy: "CD-HIT at a **70% similarity threshold** clusters **substrate** sequences. One representative is kept per cluster, and pairs are selected both across clusters and within clusters (one pair per cluster)." Train/val: "Random split by **unique substrates**: 5.382 training và 969 validation." — [Prot2Token arXiv HTML](https://arxiv.org/html/2505.20589v2)
- [SOURCE] Hai test held-out: **Rare-Group** (14 samples từ group RGC và PKL, loại hoàn toàn khỏi train) và **GPS-Test** (146 samples, toàn bộ từ group CMGC, lấy từ nghiên cứu GPS). — [Prot2Token arXiv HTML](https://arxiv.org/html/2505.20589v2)
- [SOURCE] F1 (positive khi score > 0,7), Table 9: KinasePhos3 0,0747 (val) / 0,0421 (GPS test) / 0,3178 (rare groups); GPS 6.0 0,3076 / 0,2398 / 0,4000; **Prot2Token-C 0,4966 / 0,4059 / 0,4242**. — [Prot2Token arXiv HTML, Table 9](https://arxiv.org/html/2505.20589v2)
- [SOURCE] Tác giả tự nêu hai hạn chế: "The paper does not state whether the GPS-Test proteins are cluster-disjoint from training" và "GPS 6.0's training split is unavailable, so its scores may reflect memorization". — [Prot2Token arXiv HTML](https://arxiv.org/html/2505.20589v2)
- [SOURCE] Có bản bioRxiv riêng về chủ đề này: "Predicting Kinase-Specific Phosphorylation Sites with Pretrained Protein Language Models" (2025), adapt Prot2Token cho 3 task: kinase group classification, kinase-substrate interaction prediction, site prediction; ESM-2 encoder + autoregressive decoder + self-supervised decoder pretraining. **[UNVERIFIED]** split protocol. — [bioRxiv 2025.03.12.642740](https://www.biorxiv.org/content/10.1101/2025.03.12.642740.full.pdf)

### Inferences

- [ANALYSIS] **Prot2Token là competitor đáng lo nhất về mặt novelty**, nhưng theo chiều ngược: nó **đã** kiểm soát substrate-side (CD-HIT 70% trên substrate + split theo unique substrate) mà **chưa** kiểm soát kinase-side đủ mạnh (test chia theo group, không phải kinase disjoint + 90% identity grouping như DARKIN). Nên trong landscape hiện tại: DARKIN = kinase-side chặt / substrate-side lỏng; Prot2Token = substrate-side chặt / kinase-side lỏng. **Chưa bên nào chặt cả hai.** Đây là framing mạnh nhất tôi tìm được cho đề cương.
- [ANALYSIS] Tuy nhiên điều này cũng có nghĩa: "substrate-side control cho kinase-phosphosite" **không phải ý tưởng mới** — nó đã tồn tại trong Prot2Token và SAGEPhos. Đóng góp phải nằm ở chỗ **hợp nhất hai trục trên một benchmark và đo được cái giá**, không phải ở chỗ "nghĩ ra trục substrate".
- [ANALYSIS] Rare-Group test chỉ có **14 samples** — quá nhỏ để kết luận gì; con số F1 0,4242 trên 14 mẫu không có ý nghĩa thống kê. Nếu GVHD hỏi "Prot2Token đã làm rồi?", đây là câu trả lời.
- [ANALYSIS] Prot2Token dùng F1 với ngưỡng cố định 0,7, DARKIN dùng macro AP. **Không so sánh chéo được**; nếu luận văn muốn đặt cả hai vào một bảng thì phải tự re-implement, đó là chi phí lớn — không nên làm trong 8–9 tuần.

### Gaps

- bioRxiv 2024.05.31.596915 (bản Prot2Token mà đề bài nêu) **trả HTTP 403** khi fetch. Tôi chỉ đọc được bản arXiv:2505.20589 v2 (12/2025). **[UNVERIFIED]** liệu bản bioRxiv tháng 5/2024 có task kinase phosphorylation hay không — khả năng cao là bản sau mới thêm, nhưng không xác nhận được.
- bioRxiv 2025.03.12.642740 (adapt Prot2Token riêng cho kinase) **[UNVERIFIED]** — chưa đọc methods, đây là ứng viên competitor gần nhất, **nên đọc trước buổi gặp GVHD**.

---

## Câu hỏi 5: Thuật ngữ và thực hành chuẩn cho "cold start hai chiều" trong recsys / link prediction

### Takeaway

Không có một tên chuẩn duy nhất. Phổ biến nhất trong literature drug–target là **"both-cold"** hoặc **"cold-both"**; biến thể một chiều là **cold-drug / cold-protein** hoặc **cold-source / cold-target**; đối lập là **warm start**. Gốc khái niệm là cold start của recommender systems.

### Cited Findings

- [SOURCE] Định nghĩa both-cold: "a 'both-cold' scenario where drugs and targets in the test set are both missing from training". — [DTIAM, arXiv:2312.15252](https://arxiv.org/pdf/2312.15252)
- [SOURCE] Một nghiên cứu trên Davis kinase inhibitor dataset dùng nhãn **"cold-both"** cùng với "cold-drug" và "cold-protein": "evaluated on the Davis kinase inhibitor dataset using four settings: random split, cold-drug, cold-protein, and cold-both". — [kết quả tìm kiếm DTI](https://arxiv.org/pdf/2404.03516)
- [SOURCE] MOTIVE nói rõ gốc gác: splits "based on the random split and cold start split originally defined for **recommendation systems**", đặt tên một chiều là **cold-source / cold-target**, "Cold-target split is symmetrical to cold-source split", và định nghĩa cold start là trường hợp "at least one node was not present during training". — [MOTIVE, arXiv:2406.08649](https://arxiv.org/pdf/2406.08649)
- [SOURCE] SAGEPhos dẫn Zhu et al. 2021 làm nguồn khái niệm cold-start cho bài toán phosphorylation. — [SAGEPhos ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/49d9839ede3649bd2ac2d7804ad6931a-Paper-Conference.pdf)
- [SOURCE] DARKIN dẫn chính xác dòng literature này khi bàn leakage: drug-target prediction (Chatterjee et al. 2023), drug synergy (2025), genomics (Whalen et al. 2022), link prediction (Brière et al. 2025), Bernett et al. 2024. — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)

### Inferences

- [ANALYSIS] Khuyến nghị framing cho luận văn: **dùng từ vựng cold-start của recsys/DTI**, vì (a) nó đã có tiền lệ in ấn, (b) nó đặt đề tài vào dòng "rigorous evaluation of biological link prediction" mà chính DARKIN đã dẫn, (c) nó cho phép nói "DARKIN hiện là **cold-kinase** split; luận văn bổ sung **cold-substrate** và **cold-both**" — câu này ngắn, chính xác, và không tuyên bố "đầu tiên".
- [ANALYSIS] Vì tên gọi không thống nhất, trong đề cương nên **định nghĩa lại rõ ràng ngay tại chỗ** (cold-kinase / cold-substrate / cold-both ở mức accession) và nói rõ mình dùng nghĩa nào, kèm một câu ghi nhận SAGEPhos dùng cùng từ nhưng ở mức 11-mer.
- [ANALYSIS] Về tính khả thi: SAGEPhos nói cold-both "not feasible" vì bipartite graph quá dày (99,9% interconnectivity). Đây là **rủi ro kỹ thuật thật** cho đề tài, cần kiểm sớm: nếu bipartite kinase×substrate của DARKIN cũng là một giant connected component thì cold-both sẽ còn rất ít test rows. **Việc nên làm đầu tiên:** đếm connected components và kích thước component lớn nhất trên bipartite graph của DARKIN, và đếm xem nếu ép substrate-protein-disjoint thì còn bao nhiêu test rows với bao nhiêu kinase còn đủ ≥5 sites. Nếu còn quá ít → phải chuyển sang báo cáo *phân rã AP theo 3 tầng* (như gợi ý ở Câu hỏi 1) thay vì tạo split cold-both.

### Gaps

- Chưa đọc Bernett et al. 2024 và Brière et al. 2025 (hai nguồn chính DARKIN dẫn về rigorous evaluation) **[UNVERIFIED]**. Brière et al. 2025 về link prediction leakage có thể chứa đúng khung lý thuyết cho đề tài — **nên đọc**.
- Chưa xác định được Zhu et al. 2021 mà SAGEPhos dẫn là bài nào cụ thể **[UNVERIFIED]**.
