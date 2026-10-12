# Prior art: xử lý nhãn thiếu / không đầy đủ trong multi-label biological link prediction (PU learning) — đánh giá tính mới và mức rủi ro cho đóng góp đề xuất trên DARKIN

> Ngày khảo sát: 10/10/2026. Nhãn nguồn: **[SOURCE]** = có dẫn nguồn trực tiếp; **[ANALYSIS]** = suy luận của người khảo sát từ các nguồn đã dẫn; **[UNVERIFIED]** = chưa kiểm chứng được.
>
> **Đóng góp đang được xem xét:** một loss/ranking objective hoặc sampling scheme phân biệt annotated positive với unknown pair (positive-unlabeled learning hoặc missing-label-aware ranking), thay vì coi unknown là hard negative, đánh giá trên zero-shot kinase protocol của DARKIN.
>
> **Ba thất bại truy cập cần ghi rõ:** (1) `nature.com/articles/s41587-026-03239-5` (KinoPlex) **chuyển hướng sang trang đăng nhập IdP**, không đọc được full text/Methods/Supplement — mọi điều về cơ chế PU của KinoPlex dưới đây chỉ dựa trên **abstract trên PubMed** và một bài tin thứ cấp. (2) `pmc.ncbi.nlm.nih.gov/articles/PMC12579546` (DARKIN) trả về trang "Checking your browser", phải dùng bản PDF tự lưu trữ của Sabancı University thay thế. (3) `openaccess.thecvf.com` trả HTTP 403; đã lấy bản PDF tương đương từ mi.t.u-tokyo.ac.jp và trích text cục bộ.

## Câu hỏi 1 — Các phương pháp đã được thiết lập cho PU learning và multi-label learning với nhãn thiếu, áp dụng được cho ranking

### Takeaway

Hai dòng kỹ thuật đã rất chín: (a) **unbiased/non-negative PU risk estimators** (uPU của du Plessis, nnPU của Kiryo) cùng họ phương pháp **class-prior estimation**, và (b) **single-positive / missing-label multi-label learning** với một phổ chiến lược từ "assume negative" (AN) tới weighted, ignore, và pseudo-label. Quan trọng nhất cho đề tài: **đã tồn tại một bài đúng bài toán "multi-label ranking from positive and unlabeled data" (Kanehira & Harada, CVPR 2016)** — đây là precedent gần nhất về mặt phương pháp, và chính bài này báo cáo gain rất nhỏ trên dữ liệu thật.

### Cited Findings

**PU learning nền tảng**

- Bekker & Davis, *Learning from positive and unlabeled data: a survey* (Machine Learning, 2018, 746 citations) đặt bảy câu hỏi nghiên cứu cốt lõi của PU learning và là survey chuẩn để trích dẫn — "PU learning is the setting where a learner only has access to positive examples and unlabeled data" — [Consensus record](https://consensus.app/papers/details/f99936dac14c5e28919e4fe530bc1938/?utm_source=claude_code) [SOURCE]
- **nnPU (Kiryo, Niu, du Plessis, Sugiyama, NeurIPS 2017)**: vấn đề của unbiased PU risk estimator là "the unbiased risk estimators will give negative empirical risks, if the model being trained is very flexible"; non-negative risk estimator chặn risk không xuống dưới 0, nhờ đó "more robust against overfitting, and thus we are able to train very flexible models given limited P data" — [arXiv 1703.00593](https://arxiv.org/abs/1703.00593); code tại [github.com/kiryor/nnPUlearning](https://github.com/kiryor/nnPUlearning) [SOURCE]
- **nnPU phụ thuộc class prior và lệch bất đối xứng**: trong thí nghiệm các tác giả cố định β=0, và ghi nhận "under-misspecified π'_p hurt more than over-misspecified π'_p" (ước lượng prior **thấp hơn** thực tế gây hại nhiều hơn ước lượng cao hơn) — [arXiv 1703.00593](https://arxiv.org/abs/1703.00593) [SOURCE]
- Sansone et al., *Efficient Training for Positive Unlabeled Learning* (IEEE TPAMI, 2016, 75 citations): PU learning dùng khi "there is a need to learn a classifier for a class of interest from an unlabeled data set, which may contain anomalies as well as samples from unknown classes"; bài tập trung vào scalability — [Consensus record](https://consensus.app/papers/details/0c51f23c7e955c439bef3130814d7985/?utm_source=claude_code) [SOURCE]
- Khảo sát mới nhất về mặt thực nghiệm: *A Closer Look to Positive-Unlabeled Learning from Fine-grained Perspectives: An Empirical Study* (NeurIPS 2025) chia PU thành hai họ — **disambiguation-free empirical risks** (uPU, nnPU, DistPU) và **pseudo-labeling methods** — và đề xuất "risk-consistent set-aware empirical risk", kết hợp hai họ thành một framework mà tác giả nói "can be a practical benchmark in PU learning" — [NeurIPS 2025 poster 116712](https://neurips.cc/virtual/2025/poster/116712) [SOURCE]. Chỉ đọc được abstract, **không rút ra được con số so sánh PU vs baseline đơn giản** [UNVERIFIED]

**Class-prior estimation**

- du Plessis, Niu & Sugiyama, *Class-prior Estimation for Learning from Positive and Unlabeled Data* (Machine Learning): ước lượng class prior của unlabeled set chỉ bằng positive bổ sung, không cần labeled negative, qua **penalized divergences**; biến thể penalized L1-distance "gives a computationally efficient algorithm with an analytic solution" — [arXiv 1611.01586](https://arxiv.org/pdf/1611.01586) [SOURCE]
- du Plessis & Sugiyama (2014) có hai bài nền: *Class prior estimation from positive and unlabeled data* (IEICE Trans., 97(5):1358–1362) và *Semi-supervised learning of class balance under class-prior change by distribution matching* (Neural Networks, 50:110–119) — đây chính là hai reference [11], [12] mà Kanehira & Harada dùng để ước lượng prior — [bản text trích từ PDF Kanehira & Harada](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- **Giới hạn đã biết của CPE**: Yao, Liu et al. (ICLR 2020, "Rethinking Class-Prior Estimation for PU Learning") chỉ ra "existing distributional-assumption-free CPE methods often **overestimate the class prior** when the irreducibility assumption, regarding the support of positive and negative data distributions, is violated" — [liner.com review](https://liner.com/review/rethinking-classprior-estimation-for-positiveunlabeled-learning) [SOURCE, nguồn thứ cấp, nên xác nhận lại từ OpenReview]
- **Hướng tránh prior hoàn toàn**: Chang, Du & Zhang (IJCAI 2020, *Positive Unlabeled Learning with Class-Prior Approximation*) "formulate a convex problem that jointly solves the class-prior unknown problem and trains an accurate classifier with no need of any class-prior assumptions or additional negative samples" — [mlanthology record](https://mlanthology.org/ijcai/2020/chang2020ijcai-positive) [SOURCE]

**Multi-label với nhãn thiếu — và cụ thể là ranking**

- **Precedent gần nhất về mặt phương pháp**: Kanehira & Harada, *Multi-label Ranking from Positive and Unlabeled Data* (CVPR 2016). Bài nêu đúng vấn đề của đề tài: "conventional ranking methods regard unlabeled objects as negative", và chứng minh rằng với rank loss, "rank loss imposes a penalty not for (positive, negative) but for (assigned, not assigned) label pairs. However, these pairs contain (positive, positive) pairs, which should not be included in the penalty" — [PDF](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- Giả định của Kanehira & Harada: "we make the assumption that the deficit of a positive label is not biased on the sample space. This condition is represented as P(x|s_i=1)=P(x|y_i=1)" — tức **SCAR / Selected Completely At Random**, đúng giả định của Elkan & Noto — [PDF, dòng 316](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- Bài đưa ra **hai điều kiện** mà loss phải thỏa để label incompleteness không làm lệch ranking: condition 1 = *use of weighted loss function* (weight theo per-class prior P(y_i=1)), condition 2 = *use of symmetric loss function*; bốn phương pháp trong thí nghiệm là tổ hợp có/không hai điều kiện này — [PDF, Table 1](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- **Phổ chiến lược chuẩn cho single-positive / missing-label multi-label** (Cole et al., *Multi-Label Learning from Single Positive Labels*, CVPR 2021): BCE (full labels, upper bound), BCE-LS, IUN, **IU (ignore unobserved)**, **AN (assume negative — plain BCE)**, **AN-LS (assume negative + label smoothing)**, **WAN (weak assume negative, down-weight negative terms)**, **EPR (expected positive regularization)**, **ROLE (regularized online label estimation)**, mỗi cái có/không LinearInit — [ar5iv 2106.09708](https://ar5iv.labs.arxiv.org/html/2106.09708) [SOURCE]
- Cole et al. cảnh báo rằng **không thể chỉ bỏ unobserved label**: "simply dropping unobserved labels would lead to a degenerate solution that always predicts positive" — [arXiv 2106.09708](https://arxiv.org/pdf/2106.09708) [SOURCE]
- **Label-correlation-based imputation**: Wu et al., *Multi-label Learning with Missing Labels using Mixed Dependency Graphs* ([arXiv 1804.00117](https://arxiv.org/pdf/1804.00117)) dùng graph phụ thuộc hỗn hợp giữa instance và label để điền nhãn thiếu [SOURCE]. Hướng mới hơn: **IGNORE** (ECCV 2024) — "Information Gap-Based False Negative Loss Rejection for Single Positive Multi-Label Learning", phát hiện false negative khả năng cao và loại chúng khỏi loss — [mlanthology record](https://mlanthology.org/eccv/2024/song2024eccv-ignore) [SOURCE]
- Các biến thể SPML khác (2022–2023) đều quay quanh pseudo-label / label enhancement: *Acknowledging the Unknown for Multi-label Learning with Single Positive Labels* ([arXiv 2203.16219](https://arxiv.org/pdf/2203.16219)), *One Positive Label is Sufficient* ([arXiv 2206.00517](https://arxiv.org/pdf/2206.00517)), *Pseudo Labels for SPML* ([arXiv 2306.01034](https://arxiv.org/pdf/2306.01034)), *Vision-Language Pseudo-Labels for SPML* ([arXiv 2310.15985](https://arxiv.org/pdf/2310.15985)) [SOURCE]

### Inferences

- **[ANALYSIS]** Đóng góp đề xuất, nhìn ở mức phương pháp thuần, **không mới**: Kanehira & Harada (2016) đã làm đúng việc "multi-label ranking mà unknown không bị coi là negative", đã có cả chứng minh lý thuyết lẫn điều kiện trên loss. Cái có thể mới chỉ là **ngữ cảnh áp dụng** (zero-shot kinase, DARKIN), không phải cơ chế.
- **[ANALYSIS]** Condition 1 của Kanehira & Harada đòi **per-class prior P(y_i=1)**. Trên DARKIN, "class" = kinase, và test kinase chưa từng thấy trong training ⇒ prior cho chính những class cần đánh giá là **không ước lượng được từ nhãn training**. Đây là điểm đứt gãy kỹ thuật trung tâm, xem câu hỏi 3.
- **[ANALYSIS]** Nếu vẫn muốn làm, nhánh **prior-free** (Chang IJCAI 2020; PU-AUC ở câu hỏi 4) là nhánh duy nhất tương thích về mặt khái niệm với zero-shot.

### Gaps

- Không đọc được full text NeurIPS 2025 empirical study, nên không có bảng số "PU vs tuned baseline" cập nhật nhất.
- Elkan & Noto (2008) chỉ xuất hiện gián tiếp (qua giả định SCAR trong Kanehira & Harada); chưa đọc bản gốc.
- Chưa tìm được bài nào làm missing-label-aware ranking **trên giao thức zero-shot class-disjoint**.

## Câu hỏi 2 — PU / missing-label-aware learning đã được áp dụng cho kinase-substrate / phosphosite prediction chưa? KinoPlex có "pre-empt" đóng góp này không?

### Takeaway

**Có, và nhiều hơn mức mong đợi.** PU learning đã là công cụ tiêu chuẩn trong kinase-substrate prediction từ 2016 (Yang et al.), có phương pháp riêng (AdaSampling 2018, SnapKin 2023), và **KinoPlex (Nature Biotechnology, 29/07/2026) dùng "positive-unlabeled transfer learning" làm thành phần cốt lõi**. Tuy nhiên KinoPlex áp PU vào **một task khác**: quyết định residue nào *có khả năng bị phosphorylate nói chung* (phospho-competence), không phải gán kinase cho site. Do đó KinoPlex **không trực tiếp pre-empt** đóng góp đề xuất, nhưng nó **phá hủy phần lớn giá trị "novelty" của câu chuyện** "chưa ai dùng PU cho dữ liệu phosphosite".

### Cited Findings

- **KinoPlex, nguồn sơ cấp (abstract)**: Vanderwall, Huttlin, Mintseris, …, Cantley, Gygi, *An AI-enabled structural atlas decodes kinase specificity across the human proteome*, Nature Biotechnology, 29/07/2026. Abstract theo PubMed (PMID 42527527): "Using ~20,000 AlphaFold models and **positive-unlabeled transfer learning**, we identified ~567,000 residues as structurally **phospho-competent**. We intersected these with **kinase position-specific scoring matrices** to quantify motif specificity, yielding ~250,000 high-confidence candidates" — theo PubMed, [DOI](https://doi.org/10.1038/s41587-026-03239-5) [SOURCE]
- Abstract cũng nêu quy mô vấn đề nhãn thiếu, con số rất đáng dùng để mở bài: "Of the 1.8 million serine/threonine/tyrosine residues in the human proteome, **only 6% bear experimental validation of phosphorylation, and only 5% of these have been mapped to a kinase**" — theo PubMed, [DOI](https://doi.org/10.1038/s41587-026-03239-5) [SOURCE]
- **Vị trí của PU trong pipeline KinoPlex**: bản tin thứ cấp xác nhận PU chỉ ở bước structural phospho-competence, còn specificity kinase đến từ PSSM — "a positive-unlabeled transfer learning strategy to infer which residues are structurally competent for phosphorylation when direct labels are sparse", sau đó "intersected with kinase position-specific scoring matrices" — [bioengineer.org](https://bioengineer.org/ai-structural-atlas-reveals-kinase-specificity-across-the-human-proteome/) [SOURCE, nguồn thứ cấp]
- **PU cho kinase-substrate, tiền lệ sớm nhất**: Yang P, Humphrey SJ, James DE, Yang YH, *Positive-unlabeled ensemble learning for kinase substrate prediction from dynamic phosphoproteomics data*, Bioinformatics 32(2):252–9 — [escholarship record](https://escholarship.org/uc/item/5181r831) [SOURCE]. Năm công bố có xung đột giữa các nguồn index (2015 vs 2016) [UNVERIFIED]
- **AdaSampling** (IEEE Transactions on Cybernetics, 03/2018, DOI 10.1109/TCYB.2018.2816984): "iteratively estimates the class mislabeling probability with an adaptive sampling procedure", và một trong hai bioinformatics application chính thức của bài là "identifying kinase-substrates from mass spectrometry-based phosphoproteomics data" — [UTS OPUS record](https://opus.lib.uts.edu.au/handle/10453/132177), [PDF](https://opus.lib.uts.edu.au/bitstream/10453/132177/1/AdaSampling_v12.pdf) [SOURCE]
- **SnapKin** (2023): "a snapshot deep learning ensemble for kinase-substrate prediction from phosphoproteomics data", dùng **pseudo-positive learning strategy** để giảm vấn đề small sample size cộng resampling-based ensemble — [PMC10632189](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10632189/) [SOURCE]
- **Review tổng hợp**: Li F. et al., *Positive-unlabeled learning in bioinformatics and computational biology: a brief review* (Briefings in Bioinformatics, 2021, 78 citations) rà soát **29 ứng dụng PU learning trong tin sinh**, trong đó có "functional site characterization and interaction prediction" — [Consensus record](https://consensus.app/papers/details/d8c6213e312e5fd9aed9a364e4b45540/?utm_source=claude_code) [SOURCE]
- **DARKIN tự nhận vấn đề nhãn thiếu**: trong Discussion, các tác giả giải thích AP thấp bằng chính lý do này — "it could also be an issue of **data incompleteness**. While some kinase–phosphosite pairs are truly associated, they might not have been experimentally studied and therefore are not reported as associated pairs" — [DARKIN PDF, Sabancı mirror](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]

### Inferences

- **[ANALYSIS]** KinoPlex và đóng góp đề xuất **khác task một cách rõ ràng và có thể biện luận được**: KinoPlex = PU trên bài toán nhị phân một nhãn (site này có phosphorylatable không), đặc trưng cấu trúc; đề xuất = PU/missing-label-aware **ranking** trên bài toán multi-label gán kinase, zero-shot theo kinase. Nhưng khi ra hội đồng, câu "Nature Biotechnology 2026 đã dùng PU cho phosphoproteome rồi" là câu hỏi **chắc chắn sẽ bị hỏi**, và sinh viên phải trả lời bằng đúng sự phân biệt task này, có trích Methods.
- **[ANALYSIS]** Với ba tiền lệ PU trong kinase-substrate (Yang 2016, AdaSampling 2018, SnapKin 2023) cộng KinoPlex 2026, đóng góp này nên được đóng khung là **"chuyển một kỹ thuật đã biết vào một giao thức đánh giá mới"**, không phải đóng góp phương pháp. Đó là loại đóng góp hợp lệ cho luận văn đại học nhưng yếu nếu GVHD đòi tính mới ở mức phương pháp.
- **[ANALYSIS]** Lợi thế đi kèm: DARKIN authors tự viết "data incompleteness" vào Discussion ⇒ sinh viên có **motivation trích dẫn được từ chính bài benchmark**, không phải tự nghĩ ra. Đây là điểm mạnh nhất của đề xuất.

### Gaps

- **Không đọc được Methods/Supplementary của KinoPlex** (paywall/IdP redirect). Vì vậy: estimator PU cụ thể (uPU? nnPU? Elkan-Noto reweighting? bagging?), cách ước lượng class prior, và liệu có nhánh nào liên quan tới gán kinase hay không — **chưa xác định được**. Cần lấy full text qua thư viện trường trước khi viết đề cương.
- Chưa kiểm được bản gốc Yang et al. 2016 để biết họ dùng estimator nào và báo cáo gain bao nhiêu so với baseline.

## Câu hỏi 3 — PU learning đã từng kết hợp với zero-shot / unseen-class chưa? Giả định class-prior còn sống sót không?

### Takeaway

**Không tìm được tiền lệ nào kết hợp PU learning với zero-shot/unseen-class setting** qua các truy vấn đã thử — nhưng theo đúng yêu cầu, **không được suy ra tính mới từ việc không tìm thấy**. Quan trọng hơn: có lý do **lý thuyết** để nghi ngờ sự kết hợp này, vì mọi estimator PU chuẩn (uPU, nnPU, condition 1 của Kanehira) đều cần **per-class prior**, và trong zero-shot theo kinase thì prior của đúng những class cần dự đoán không ước lượng được từ nhãn training.

### Cited Findings

- Truy vấn "positive-unlabeled learning zero-shot unseen classes class prior" **không trả về công trình nào kết hợp PU với zero-shot/unseen classes**; chỉ trả về các bài class-prior estimation thuần [SOURCE: kết quả tìm kiếm, ghi nhận như một quan sát về độ phủ tìm kiếm, không phải bằng chứng về tính mới]
- Truy vấn trên Consensus "positive-unlabeled learning combined with zero-shot learning for unseen classes" trả về **không bài nào thực sự ở giao của hai lĩnh vực**: top-1 là Zero-VAE-GAN (ZSL thuần, không PU), top-2 là survey PU của Bekker & Davis, top-3 là Efficient Training for PU — [Consensus search](https://consensus.app/search/new?q=positive-unlabeled+learning+combined+with+zero-shot+learning+for+unseen+classes&utm_source=claude_code) [SOURCE, cùng cách đọc như trên]
- **Bằng chứng gián tiếp rằng prior-per-class là điểm vỡ**: Kanehira & Harada ghi nhận "the prior P(y_i=1) in (16) was given from fully labeled training samples" trong thí nghiệm synthetic optimal; khi phải **ước lượng** prior họ áp dụng du Plessis & Sugiyama distribution matching "for every class" — tức **một lần ước lượng cho mỗi class** — [PDF, dòng 557–576](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- **Và ước lượng prior per-class hỏng chính xác ở chế độ dữ liệu của DARKIN**: "If many labels were attached (8 labels out of 80 classes), the prior estimation failed and high accuracy could not be achieved… these results implied that **the rate of (the number of labels)/(the number of classes) in the data is a key to the success of our method** combined with prior estimation" — [PDF, dòng ~600](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- Kanehira & Harada cũng nêu một ngưỡng vận hành: "Our method works when the label deficit rate is greater than about 20%", và "the accuracy near a 0% deficit rate was low because the prior estimation method we used did not assume that the labels were complete" — [PDF](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- **Nhánh prior-shift gần nhất** (có thể dùng để lập luận, không phải tiền lệ trực tiếp): Mielniczuk, Rejchel & Teisseyre (preprint 2026) "study estimation of a class prior for unlabeled target samples which possibly differs from that of the source population", dùng distribution matching với kernel embeddings — [linstat2026 abstract](https://linstat2026.put.poznan.pl/abs/Rejchel.pdf) [SOURCE]
- **Nhánh prior-free cho link prediction** (xem thêm câu hỏi 4): Mao et al., *Boosting GNN-Based Link Prediction via PU-AUC Optimization* (IEEE TKDE 2025) nói thẳng rào cản: "the **unknown class prior** and data imbalance of networks impede the use of PU learning in link prediction", và phương pháp của họ "is **free of class prior estimation** and able to handle the data imbalance" — [Consensus record](https://consensus.app/papers/details/172f68cc8fb7534fbb6bea1f96173914/?utm_source=claude_code) [SOURCE]

### Inferences

- **[ANALYSIS]** Giả định class-prior **không sống sót nguyên vẹn** trong zero-shot theo kinase. Lý do cụ thể: π_k = P(site bị phosphorylate bởi kinase k) phụ thuộc mạnh vào từng kinase (DARKIN chia kinase theo số phosphosite liên kết, ngưỡng 15 và 10 — tức số positive mỗi kinase biến động hàng chục lần). Với test kinase chưa thấy, muốn biết π_k thì cần đúng cái nhãn mà ta đang cố dự đoán. Có ba lối ra, tất cả đều phải nói rõ là **giả định**, không phải ước lượng:
  1. **Prior-free**: PU-AUC (Mao et al. 2025) hoặc Chang IJCAI 2020. Tương thích nhất với zero-shot, nhưng phải tự cài, chi phí cao.
  2. **Prior chia sẻ theo kinase group/family**: giả định π_k xấp xỉ bằng π của nhóm kinase (DARKIN có 11 kinase groups, 129 families và đã stratify theo group) — đây là giả định sinh học **có thể biện luận** và là ý tưởng duy nhất mang hơi hướng "mới" mà tôi thấy được.
  3. **Prior như một hyperparameter**, sweep và báo cáo sensitivity curve. Trung thực nhất, và cộng với cảnh báo của nnPU ("under-misspecified π'_p hurt more") thì có thể biến thành **một phân tích sensitivity có giá trị học thuật ngay cả khi không có gain**.
- **[ANALYSIS]** Lối ra (3) là lối duy nhất mà sinh viên **chắc chắn có kết quả để viết** sau 8–9 tuần, dù PU thắng hay thua.
- **[ANALYSIS]** Cảnh báo của Kanehira & Harada về tỷ số (số label)/(số class) đi **ngược** chiều có lợi cho DARKIN: số nhãn mỗi site rất nhỏ so với số kinase class (phần lớn site chỉ có 1–2 kinase trên hàng trăm class), tức tỷ số này rất thấp — đây **có thể là** chế độ tốt cho ước lượng prior theo logic bài CVPR (họ nói prior estimation hỏng khi nhãn **nhiều**). Nhưng mặt khác, prior rất nhỏ ⇒ ước lượng từ ít positive sẽ có variance lớn. Hai hiệu ứng trái chiều, **không kết luận được từ nguồn hiện có** [UNVERIFIED].

### Gaps

- Chưa tìm được bài nào xử lý class-prior estimation **cho class chưa thấy**. Có thể bài toán này vô vọng về mặt lý thuyết (prior của class unseen là non-identifiable từ dữ liệu seen), nhưng tôi **không tìm được nguồn nào phát biểu điều đó một cách hình thức** — nên đây vẫn là phỏng đoán, không phải kết quả đã biết.
- Chưa kiểm được full text PU-AUC (TKDE 2025) để biết complexity thực tế và có code công khai hay không.

## Câu hỏi 4 — Trong drug–target và protein–protein interaction prediction: thực hành chuẩn là gì, và PU có thực sự thắng "assume negative" không? Có negative result nào không?

### Takeaway

Thực hành chuẩn trong DTI/PPI vẫn là **random negative sampling từ unlabeled pairs**, và literature đã cảnh báo mạnh rằng chính việc này gây **overoptimistic performance**. Các bài PU đều tự báo cáo thắng, nhưng **tôi không tìm được bài nào so PU objective với một baseline "assume negative" đã được tune cẩn thận**. Bằng chứng negative mạnh nhất không đến từ DTI/PPI mà từ **multi-label vision**: trên COCO, **label smoothing đơn thuần (AN-LS, 66.9 mAP) bằng hoặc hơn phương pháp phức tạp ROLE (66.3 mAP)**, trong khi AN trần là 64.1.

### Cited Findings

**Bằng chứng negative mạnh nhất: baseline đơn giản đã bắt kịp phương pháp phức tạp**

- Cole et al. (CVPR 2021), Table 1, test mAP (fine-tuned), MS-COCO / NUS-WIDE — [ar5iv 2106.09708](https://ar5iv.labs.arxiv.org/html/2106.09708) [SOURCE]:

  | Method | COCO (linear / FT) | NUS (linear / FT) |
  |---|---|---|
  | BCE (full labels, upper bound) | 70.0 / **75.8** | 50.7 / **52.6** |
  | **AN (plain assume-negative BCE)** | 62.3 / 64.1 | 46.2 / 42.0 |
  | **AN-LS (chỉ thêm label smoothing)** | 64.8 / **66.9** | 48.5 / 44.9 |
  | AN-LS + LinearInit | – / **69.2** | – / 50.5 |
  | ROLE (phương pháp đề xuất) | 66.3 / 66.3 | 49.5 / 43.1 |
  | ROLE + LinearInit | – / 69.0 | – / **51.0** |

  Đọc bảng: trên COCO fine-tuned, **AN-LS (66.9) > ROLE (66.3)**; AN-LS+LinearInit (69.2) > ROLE+LinearInit (69.0). Chỉ trên NUS-WIDE thì ROLE+LinearInit (51.0) hơn AN-LS+LinearInit (50.5) một chút. Toàn bộ gain của "phương pháp đúng về missing label" so với AN trần là **+2,8 đến +5,1 mAP trên COCO**, nhưng **phần lớn gain đó đến từ label smoothing, không từ cơ chế estimate-label**.
- Một bài SPML về sau mô tả label smoothing đúng như vậy: AN-LS "beats plain assume-negative", và AN là "a lower bound on performance"; label smoothing là **"a strong baseline"** — [tổng hợp từ các bài SPML, xem arXiv 2310.15985](https://arxiv.org/pdf/2310.15985) [SOURCE]
- Trong ablation của arXiv 2310.15985, label smoothing chỉ thêm **khoảng +0,3 đến +0,4 mAP** trên VOC/COCO/NUS/CUB [SOURCE, con số là phép trừ của tôi từ bảng ablation nên nên kiểm lại]. Lưu ý bài này dùng ε=0,9 rất cao nên không chuyển trực tiếp sang setting smoothing thông thường [ANALYSIS]

**Negative result từ chính bài PU multi-label ranking gần nhất**

- Kanehira & Harada, phần Discussion về dữ liệu thật (MSCOCO 82.783 train / 40.504 test, 80 class, trung bình 2,95 nhãn/ảnh; NUS-WIDE 161.789 train, 81 class, trung bình 1,76 nhãn/ảnh): "In both datasets, Method 3 with the estimated prior was able to **improve slightly** the accuracy in every deficit rate even though the prior estimation was naive" — [PDF](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- Và trong Conclusion: "Despite its simplicity, our method **slightly improved** the accuracy, but an efficient estimation algorithm is needed for more improvement when applied to large-scale data" — [PDF](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]. Lưu ý: họ **không đưa bảng số** cho MSCOCO/NUS-WIDE, chỉ có Fig. 7 và Fig. 8 (hình), nên không trích được con số gain cụ thể [UNVERIFIED]

**DTI / PPI: thực hành chuẩn và lời cảnh báo**

- Peng et al. (Scientific Reports, 08/2017), *Screening drug-target interactions with positive-unlabeled learning*: nêu rằng lấy negative ngẫu nhiên từ unlabeled pairs "results in overoptimistic classification results"; họ đề xuất NDTISE chọn strong negative bằng PU learning, nuôi một framework SVM gọi là PUDTI, và báo cáo NDTISE "is much better than random selection and **slightly outperforms** NCPIS" — [PMC5556112](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5556112/) [SOURCE]
- DDI-PULearn (BMC Bioinformatics, 12/2019): unlabeled drug pairs "may include a considerable number of real positive samples which can degrade the prediction performance"; dùng OCSVM + cosine-similarity KNN để seed reliable negative rồi iterative SVM; đánh giá trên **149.878 cặp khả năng giữa 548 drug**, so với 2 baseline và 5 phương pháp SOTA — [PMC6929327](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6929327/), [Springer](https://link.springer.com/doi/10.1186/s12859-019-3214-6) [SOURCE]
- **Negative sampling là nguồn overoptimism chính trong PPI** (bài 2025): Li, Shao, Zhao, Liu, *Negative sampling strategies impact the prediction of scale-free biomolecular network interactions with machine learning* (BMC Biology 2025): overestimated model performance xuất phát từ negative sampling procedures, và gắn với **degree bias** — model "can predict interaction probabilities primarily based on sample degrees instead of molecular features"; bài cũng ghi nhận các nghiên cứu gần đây **vẫn tiếp tục** báo cáo ước lượng quá lạc quan dù đã có cảnh báo trước đó — [BMC Biology 10.1186/s12915-025-02231-w](https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-025-02231-w) [SOURCE]
- Tiền lệ kinh điển: Park & Marcotte (Bioinformatics, 2011) chỉ ra "there are two fundamentally different types of subset sampling for negative PPIs", và pair-input methods "are significantly influenced by the paired nature of inputs" — [PMC3198576](https://pmc.ncbi.nlm.nih.gov/articles/PMC3198576) [SOURCE, qua kết quả tìm kiếm]
- Kesemen et al. (CIBB 2025), *Clustering-Based Negative Sampling Approaches for Protein-Protein Interaction Prediction*: so clustering-based negative sampling với random sampling trên 4 dataset, lập luận rằng random sampling "tends to introduce inaccurately labelled negative samples" — [GSU avesis record](https://avesis.gsu.edu.tr/yayin/626589d9-03f1-444a-acb8-1ac9a66ea2c7/clustering-based-negative-sampling-approaches-for-protein-protein-interaction-prediction) [SOURCE]
- **Nhánh PU hiện đại nhất cho link prediction**: PU-AUC (Mao et al., IEEE TKDE 2025) — model-agnostic, prior-free, tối ưu AUC dưới PU, có accelerated method "to reduce the operational complexity of PU-AUC optimization from quadratic to approximately linear"; báo cáo "boosting the performance of the state-of-the-art GNN-based link prediction models" — [Consensus record](https://consensus.app/papers/details/172f68cc8fb7534fbb6bea1f96173914/?utm_source=claude_code) [SOURCE]
- PU + transfer learning cho gene network reconstruction (Mignone et al., 2018): "we consider known existing links as positive labeled data and all the possible remaining links as unlabeled data", dùng source network (Mus Musculus) để cải thiện target (Homo Sapiens); hiệu quả "with respect to the considered baselines" — [Consensus record](https://consensus.app/papers/details/a24d8767392c5d23b82c3c256a4d66d4/?utm_source=claude_code) [SOURCE]

### Inferences

- **[ANALYSIS] Về negative evidence, nói thẳng:** tôi **không tìm được** bài nào trong DTI/PPI công bố rằng PU không giúp. Nhưng điều đó **không phải bằng chứng PU hữu dụng** — đây là publication bias điển hình: không ai công bố "PU learning của tôi không thắng BCE". Ba dấu hiệu gián tiếp cho thấy gain thực tế nhỏ: (1) từ ngữ của chính các tác giả PU khi so với phương án tốt nhất là **"slightly outperforms"** (Peng et al.) và **"slightly improved"** (Kanehira & Harada, hai lần); (2) bảng của Cole et al. cho thấy cơ chế "đúng về missing label" (ROLE) **không thắng được label smoothing** trên COCO; (3) literature PPI 2011–2025 cho thấy biến số thống trị là **negative sampling / degree bias**, không phải dạng của loss.
- **[ANALYSIS]** Hệ quả cho sinh viên: nếu đóng góp được đóng khung là "PU sẽ cải thiện AP", **xác suất thất bại cao**. Nếu đóng khung là "đo xem cách xử lý unknown ảnh hưởng thế nào tới AP, có ablation sạch và sensitivity theo prior", thì **thành công bất kể dấu của kết quả**. Đây là sự khác biệt quyết định giữa một đề tài an toàn và một đề tài rủi ro.

### Gaps

- Không có bài nào so trực tiếp "negative sampling strategy vs PU loss choice, cái nào quan trọng hơn". Chưa đọc full text BMC Biology 2025 để xem có bảng trả lời được câu đó không.
- Không có bảng số cho phần MSCOCO/NUS-WIDE của Kanehira & Harada (chỉ có hình).
- Chưa tra được PU learning áp dụng cho **kinase–phosphosite link prediction dạng multi-label ranking** cụ thể (khác với kinase-substrate binary classification kiểu AdaSampling/SnapKin).

## Câu hỏi 5 — Rủi ro thực tế: xác suất PU objective tạo ra cải thiện AP đo được trên DARKIN, và các baseline đơn giản phải kiểm soát trước

### Takeaway

**Rủi ro cao, và quan trọng hơn: rủi ro "không kết luận được" cao hơn rủi ro "PU thua".** Vì AP tuyệt đối trên DARKIN rất thấp (0,15–0,19 ở trục kinase) nhưng **biến động giữa các split lớn hơn gain kỳ vọng của PU**, một gain +0,005–0,01 AP sẽ **không phân biệt được với noise** nếu không chạy đủ split và seed. Trước khi quy công cho cơ chế PU, bắt buộc phải kiểm soát ít nhất: AN trần, AN + label smoothing, WAN (down-weight negative), tỉ lệ negative sampling, và prior-as-hyperparameter.

### Cited Findings

**Con số nền của DARKIN (để tính "gain bao nhiêu mới đáng tin")**

- Macro AP tốt nhất toàn bài: "The highest AP score achieved was **0.1911** using fine-tuning pLMs, which considerably outperforms **random guessing (0.03** by averaging AP over 1000 runs of randomly generated ranking of kinases for a given site), **but can be considered low overall**" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]
- Định nghĩa macro AP (trục kinase): "for each kinase, we rank the prediction probabilities made for all phosphosite samples… We calculate the AP score for each kinase and then take the mean across all kinase classes, hence calculating the **macro AP**" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]
- Xử lý multi-label hiện tại của benchmark là **rất lỏng**: "When multiple kinases can phosphorylate a phosphosite, we accept the predicted kinase as a true positive if it matches **any** of the true kinases associated with it" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]
- **Kết quả theo embedding (Table 2, chỉ dùng pLM embeddings, Split 1)** — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]: 3-NN tốt nhất là TAPE 0,1200; BZSM tốt nhất là ESM1v 0,1640 ±0,0028 và ESM1B 0,1631 ±0,0011; ProtT5-XL 0,1552 ±0,0011; SaProt (avg) 0,1466 ±0,0026. Baseline encoding: OneHot 0,0634 ±0,0034, Blosum62 0,0327, NLF 0,0419.
- **Biến động giữa 4 split (Table 4, BZSM với Family+Group+EC)** — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]:

  | Split | ESM1B (cls) AP | SaProt (cls) AP | Phospho-site AP (ESM1B / SaProt) | Family AP | Group AP |
  |---|---|---|---|---|---|
  | Split 1 | 0,1769 | 0,1800 | 0,2830 / 0,3053 | 0,2278 / 0,2384 | 0,3959 / 0,3903 |
  | Split 2 | 0,1536 | 0,1599 | 0,2747 / 0,2929 | 0,1989 / 0,2087 | 0,3689 / 0,3649 |
  | Split 3 | 0,1531 | 0,1627 | 0,2951 / 0,3142 | 0,1987 / 0,2104 | 0,3747 / 0,3663 |
  | Split 4 | 0,1652 | 0,1690 | 0,3118 / 0,3482 | 0,2142 / 0,2205 | 0,3969 / 0,4069 |

  ⇒ **Xác nhận hai trục AP mà đề bài nêu**: trục kinase (macro AP, ~0,15–0,18) và **"Phospho-site AP"** (~0,27–0,35). Nhưng cũng cho thấy **spread giữa split tới 0,024 AP** (0,1531 → 0,1769 cho cùng ESM1B), trong khi std giữa các run cùng split chỉ ~0,001–0,008.
- **Cấu trúc split zero-shot** (để hiểu vì sao prior per-kinase khó): "Kinases that are associated with fewer than 15 phosphosites are defined as train kinases. Later, kinases with at least 90% sequence identity are grouped and are randomly defined as entirely train or test kinases altogether"; validation ngưỡng 10 phosphosite; và benchmark **cố tình đảo vai light/dark kinase**: "we invert the roles of light and dark kinases in evaluation" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]
- Dữ liệu được chia theo **11 kinase groups và 129 kinase families**; stratify theo group vì "stratifying by kinase families is impractical due to the limited number of kinases per family" — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf) [SOURCE]
- Benchmark đã bị vượt bởi một bài khác: arXiv 2510.23492 (*Learning the PTM Code through a Coarse-to-Fine, Mechanism-Aware Framework*) báo cáo **mAP 0,2946 trên DARKIN**, tự nhận "substantially outperforms the highest reported score from the original study (0.1911) by 54%", và định nghĩa mAP của họ là "the ability to correctly **rank true kinases for each substrate**" — [arXiv 2510.23492](https://arxiv.org/pdf/2510.23492) [SOURCE]

**Rủi ro class-prior estimation, dạng đã có nguồn**

- nnPU: sai lệch prior theo hướng thấp gây hại nhiều hơn hướng cao ("under-misspecified π'_p hurt more than over-misspecified π'_p") — [arXiv 1703.00593](https://arxiv.org/abs/1703.00593) [SOURCE]
- CPE không giả định phân bố có xu hướng **overestimate** prior khi irreducibility bị vi phạm (ICLR 2020 ReCPE) — [review](https://liner.com/review/rethinking-classprior-estimation-for-positiveunlabeled-learning) [SOURCE, thứ cấp]
- Kanehira & Harada chọn ước lượng prior **naive** (tỉ lệ labeled sample mỗi class) cho dữ liệu thật vì "the computational costs of existing algorithms are high" — [PDF](https://www.mi.t.u-tokyo.ac.jp/assets/publication/Multi-label_Ranking_from_Positive_and_Unlabeled_Data.pdf) [SOURCE]
- Mao et al. gọi "unknown class prior and data imbalance of networks" là cái **cản trở việc dùng PU learning cho link prediction** — [Consensus record](https://consensus.app/papers/details/172f68cc8fb7534fbb6bea1f96173914/?utm_source=claude_code) [SOURCE]

### Inferences

- **[ANALYSIS] Ngưỡng gain phải vượt.** Vì spread giữa 4 split của DARKIN tới ~0,024 AP ở trục kinase, một cải thiện muốn tin được phải (a) đo trên **cả 4 split chính thức** × **ít nhất 3 seed**, và (b) có hiệu ứng nhất quán về dấu trên cả 4 split. Nếu gain ~0,005 chỉ xuất hiện ở 2/4 split, kết luận duy nhất hợp lệ là "không phân biệt được với noise". Đây là ràng buộc nặng nhưng **làm được trong 8–9 tuần** nếu dùng BZSM (bilinear) trên embedding đã trích sẵn thay vì fine-tune pLM.
- **[ANALYSIS] Xác suất PU tạo gain đo được: tôi đặt ở mức thấp, khoảng 25–35%**, dựa trên: Kanehira & Harada chỉ đạt "slightly improved" dù họ *thiết kế* loss cho đúng bài toán này; Cole et al. cho thấy ROLE không thắng label smoothing; và prior per-kinase ở DARKIN là **không ước lượng được** (unseen class) nên phải giả định. Đây là ước lượng chủ quan của tôi, không phải số liệu từ nguồn.
- **[ANALYSIS] Danh sách baseline phải kiểm soát trước khi quy công cho cơ chế PU** (xếp theo thứ tự bắt buộc):
  1. **AN trần** — BCE/ranking coi unknown = 0, đúng như benchmark hiện làm. Đây là baseline tham chiếu.
  2. **AN-LS** — chỉ thêm label smoothing. Theo bảng Cole et al. đây là baseline **mạnh nhất và rẻ nhất**, và là baseline mà nhiều paper PU thực chất không vượt được.
  3. **WAN** — down-weight toàn bộ negative term bằng một hằng số α; sweep α. Nếu PU chỉ ngang WAN thì "cơ chế PU" không phải thứ tạo gain, chỉ là reweighting.
  4. **Negative sampling rate** — sweep số negative lấy mỗi positive. Literature PPI (Park & Marcotte 2011; BMC Biology 2025) cho thấy đây là biến số thống trị, phải cố định/sweep có kiểm soát.
  5. **Prior-as-hyperparameter** — thay vì ước lượng π, sweep π và vẽ **AP vs π**. Nếu đường cong phẳng thì PU không có tác dụng; nếu có đỉnh ở π khác giá trị naive thì có phát hiện thật.
  6. **Giữ nguyên mọi thứ khác**: cùng embedding (ESM1B hoặc ESM1v cls — hai cái tốt nhất), cùng kiến trúc BZSM, cùng split, cùng seed. Chỉ đổi loss.
- **[ANALYSIS] Hai bẫy đo lường riêng của DARKIN:**
  - **Bẫy trộn trục.** Con số 0,1911 là macro AP **trục kinase**; "Phospho-site AP" là 0,27–0,35; còn arXiv 2510.23492 báo 0,2946 và mô tả metric của họ là "rank true kinases for each substrate" — tức **nghe giống trục site hơn trục kinase**, nhưng lại so với 0,1911. **Không được lặp lại so sánh này** mà chưa đọc kỹ cả hai bài; nếu sinh viên trích "+54%" của họ, rất dễ bị GVHD bắt lỗi so sai trục. [ANALYSIS, dựa trên [arXiv 2510.23492](https://arxiv.org/pdf/2510.23492) và [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf)]
  - **Bẫy "any match".** Quy ước "true positive if it matches any of the true kinases" của DARKIN đã làm nhẹ bớt vấn đề multi-label ngay trong metric. Tức **một phần tác hại của nhãn thiếu đã bị metric hấp thụ**, làm dư địa cải thiện cho PU hẹp hơn tưởng. Đây là một lập luận phản biện mạnh mà GVHD có thể nêu, sinh viên nên chuẩn bị trước.
- **[ANALYSIS] Khung đóng góp đề nghị, ít rủi ro nhất:** không bán "PU cải thiện AP", mà bán **"một nghiên cứu ablation về cách xử lý unknown pair dưới giao thức zero-shot theo kinase"** gồm: (a) đặt vấn đề bằng chính câu "data incompleteness" của tác giả DARKIN; (b) so AN / AN-LS / WAN / IU / PU (uPU hoặc nnPU, prior sweep) trên 4 split; (c) phân tích sensitivity theo π và theo tỉ lệ negative; (d) nếu PU không thắng, **đó là kết quả công bố được** vì chưa ai làm trên benchmark này. Rủi ro "không có gì để viết" gần như bằng 0; rủi ro "không có contribution phương pháp mới" thì chấp nhận ngay từ đầu.

### Gaps

- **Không xác minh được hai con số nền trong đề bài**: "~11.500 annotated training pairs" và "308 kinases". Trong bản PDF DARKIN, các số này nằm ở **Figure 2 (hình)** — "The number of kinases. (b) The number of unique phosphosites. (c) The number of kinase–phosphosite pairs in each train, validation, and test folds" — và ở Supplementary, nên **không trích text được** [UNVERIFIED]. Cần mở Figure 2 hoặc repo [tastanlab/darkin](https://github.com/tastanlab/darkin) để chốt số chính xác trước khi viết đề cương.
- Tỉ lệ multi-label chính xác (bao nhiêu % site có >1 kinase) nằm trong Supplementary Fig. 3, chưa đọc được. Bài chỉ nói "We quantified the multilabel nature of the task in Fig. 3, available as supplementary data" [UNVERIFIED]. Con số này **quan trọng trực tiếp** cho đóng góp: nếu tỉ lệ multi-label thấp, lợi ích tiềm năng của missing-label-aware ranking càng nhỏ.
- Chưa biết DARKIN/BZSM hiện dùng loss gì chính xác (cross-entropy trên toàn bộ kinase class? ranking loss?) — cần đọc code để biết baseline AN thực tế là gì. Bài có đề cập một kỹ thuật masking: loại các kinase ngoài group bằng cách "effectively setting them to negative infinity", tức benchmark **đã** có một dạng masking theo group — [DARKIN PDF](https://research.sabanciuniv.edu/53050/1/DARKIN.pdf). Đây có thể đã lấn vào ý tưởng "ignore unknown" ở mức group [ANALYSIS, cần xác nhận bằng code].
- Chi phí tính toán thực tế của nnPU/PU-AUC trên ma trận site × kinase của DARKIN chưa ước lượng được; PU-AUC là pairwise nên cần bản accelerated (xấp xỉ linear) mới khả thi trên Colab [ANALYSIS].
