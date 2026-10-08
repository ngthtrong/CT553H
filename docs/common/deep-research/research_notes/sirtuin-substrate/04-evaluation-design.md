# Thiết kế đánh giá cho đề tài dự đoán cơ chất SIRT1–7: phản biện và đề xuất giao thức

> Phạm vi: chỉ xét **phần đánh giá** (metric, cách chia tập, baseline, so sánh với bài 2025). Không huấn luyện mô hình nào, không đề xuất kiến trúc mới ngoài những gì cần để đặt ablation.
>
> **Nhãn bằng chứng dùng xuyên suốt:**
> - `[tác giả báo cáo]` — câu trong bài báo gốc hoặc trong báo cáo nội bộ, trích nguyên ý, chưa phán xét đúng/sai.
> - `[tự kiểm]` — tôi tự đọc đúng đoạn văn/Methods đó trong phiên này, hoặc tự tính lại số bằng máy.
> - `[suy luận]` — kết luận của tôi từ các dữ kiện đã dẫn, không có trong nguồn nào.
> - `[chưa kiểm]` — chưa đọc được nguồn gốc (phụ lục bị chặn, DOI chưa tra lại), nêu ra để sinh viên kiểm.
>
> Tài liệu nền trong repo: [topic-final-recommendation.md](../../reports/topic-final-recommendation.md) · [compute-novelty-directions.md](../../reports/compute-novelty-directions.md). Mọi số trong hai tài liệu đó, khi được nhắc lại ở đây, đều mang nhãn `[tác giả báo cáo]` cho tới khi tôi kiểm lại được.
>
> Toàn văn Ridgeway et al. 2025 lấy qua **PubMed Central** (PMC12594832), DOI [10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6). Theo PubMed, bài này là *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem 2025.

---

## 1. Con số 43,0% của Ridgeway 2025 được tính thế nào, và đại lượng nào đo được trên tập chỉ-có-dương

### Takeaway

Phép tính **đúng là 64/149** như báo cáo nội bộ đoán, nhưng **cái tên "precision" của nó là sai**: với tập chỉ có 149 vị trí dương đã biết, 64/149 là **recall (sensitivity, hit rate)**, không phải precision. Chính bài báo, ở phần SET8, định nghĩa `precision = TP/(TP+FP)` và `recall = TP/(TP+FN)`, nên cách dùng chữ trong phần SIRT là **không nhất quán nội bộ**. Trên tập chỉ-có-dương, **precision, MCC, AUROC, AUPRC đều không đo được**; chỉ recall-ở-một-ngưỡng, enrichment so với một background, và thứ hạng (ranking) là đo được.

### Cited Findings

- Nguyên văn phần Results, mục *Employment of the ML-hybrid ensemble method to the SIRT1-7 family*: “Our SIRT2 ML-hybrid ensemble model … **was able to successfully reconfirm 64 of 149 previously confirmed SIRT2 substrates** (Supplementary Data), indicating an **precision rate of 43.0%**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/), DOI [10.1038/s42004-025-01717-6](https://doi.org/10.1038/s42004-025-01717-6) `[tự kiểm — đọc đúng câu này trong toàn văn]`.
- Tôi tính lại: `64/149 = 0,42953…` → làm tròn **42,95% ≈ 43,0%**. Vậy **phép tính khớp**: con số 43,0% chính là `64/149`, không phải lấy từ một bảng nào khác `[tự kiểm — tự tính]`.
- Cùng bài, phần SET8, định nghĩa rõ hai đại lượng: “a method precision rate (i.e., **[True Positive] / [True Positive + False Positive]**)” và “recall of 0.31 (**[True Positive] / [True Positive + False Negative]**)”, cộng “specificity of 0.83 ([True Negative] / [False Positive + True Negative])” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.
- Bài có **một** con số thực sự là precision, nhưng là của SET8 chứ không phải SIRT: 2.367 vị trí được mô hình dự đoán dương, **885** trong đó được xác nhận có hoạt tính methyl hóa in vitro → “a validated precision of **37.4%**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`. Tôi tính lại `885/2367 = 0,37389 → 37,4%` `[tự kiểm]`. Đây là precision **đúng nghĩa**: mẫu số là *số dự đoán dương*, và mọi dự đoán dương đều được đem đi thử.
- Phần Discussion gộp hai con số này lại: “These models achieve experimentally validated **precision rates of 37−43%**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.
- Nguồn của 149 vị trí: phần Methods, mục *Mass spectrometry*, câu cuối: “The **MS-verified sites for SIRT2 were obtained from the dataset provided in Zhang et al., 2022**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`. Tức tập này **không phải** thí nghiệm của chính Ridgeway; nó là dữ liệu ngoài.
- Bài Zhang 2022 là *Quantitative proteomic analysis of the lysine acetylome reveals diverse SIRT2 substrates*, Sci Rep — [PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/). Theo phần Results mục *Proteome-wide identification of lysine acetylation changes*: **2.846 vị trí acetyl hóa duy nhất trên 1.414 protein** được định lượng; **896** vị trí tăng khi knockdown SIRT2; **509** vị trí giảm khi overexpression; ngưỡng gọi là **> 1,5 lần** và phải **ngược chiều giữa KD và OE** (Methods, mục *Differential expression (DEX)*); FDR < 1% chỉ áp cho bước *identification*, **không có p-value riêng cho việc gọi vị trí phụ thuộc SIRT2** `[tự kiểm qua WebFetch toàn văn PMC8907344]`.
- Vẫn trong Zhang 2022, mục *Venn diagrams*: giao của hai tiêu chí ở mức vị trí là **134 peptide chứa 152 vị trí** (Fig. S4a) `[tự kiểm]`. Danh sách đầy đủ 2.846 vị trí nằm ở **Supplementary Table S1** `[tự kiểm — bài dẫn Table S1 cho tập 2.846; chưa mở được file để xác nhận có cột fold-change cho từng vị trí]`.
- Báo cáo nội bộ nói tập 149 vị trí là “SIRT2 quá biểu hiện (OE) và knockdown (KD)”, “cả 149 vị trí đều có log2(FC) < 0 ở OE và > 0 ở KD”, và “Mô hình của bài 2025 dự đoán dương 64/149, **đúng mức precision 43,0%** họ báo” — [topic-final-recommendation.md §2.2](../../reports/topic-final-recommendation.md) `[tác giả báo cáo]`.
- Ridgeway lại mô tả bối cảnh tế bào là “HCT116 cells over-expressing FLAG-SIRT2-WT or **catalytically inactive FLAG-SIRT2-H187Y**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`, trong khi Zhang 2022 mô tả thiết kế là **knockdown và overexpression** `[tự kiểm]`. Hai mô tả không trùng nhau.

### Inferences

- **Kết luận về câu hỏi chính:** báo cáo nội bộ **đúng về phép tính, sai về đại lượng**. `64/149` có mẫu số là *số vị trí dương đã biết*, nên nó là `TP/(TP+FN)` = **recall**. Muốn nó là precision thì mẫu số phải là *số vị trí mô hình gọi dương*, và tập phải chứa cả những vị trí mô hình gọi dương mà thực ra không phải cơ chất — tập 149 không có thứ đó `[suy luận]`.
- Sự khác biệt này không phải chuyện câu chữ. **Recall một mình thì "cải thiện" được bằng cách hạ ngưỡng**: một mô hình gọi *mọi* lysine là dương đạt recall 100% trên tập 149, trong khi precision thật của nó gần 0. Vì vậy câu "mô hình của em đạt 55% so với 43,0% của bài 2025" **không nói lên điều gì** nếu hai mô hình gọi dương với tỉ lệ khác nhau `[suy luận]`.
- Việc Discussion gộp SET8 (37,4% = precision thật) với SIRT2 (43,0% = recall) thành “precision rates of 37−43%” là **trộn hai đại lượng khác nhau về bản chất**. Đây là một điểm phản biện sạch, có thể nêu với GVHD, và nó **không đòi hỏi mình phải chạy mô hình nào** `[suy luận]`.
- **Đại lượng nào đo được trên tập chỉ-có-dương, và vì sao:** mọi metric cần đếm **FP** hoặc **TN** đều không tính được, vì muốn có FP/TN phải có mẫu âm.
  - **Recall / sensitivity ở một ngưỡng** — đo được. Chỉ cần `TP` và `TP+FN = 149`.
  - **Hit rate trên danh sách đã xếp hạng (recall@k)** — đo được, với điều kiện k được định nghĩa trên một tập nền chung (ví dụ k = 1% của 145.461 vị trí toàn proteome), không phải trên 149.
  - **Enrichment so với một background** — đo được, nhưng **phải khai báo background là gì**. Không có background thì không có phép so.
  - **Precision = TP/(TP+FP)** — **không** đo được: không có vị trí nào trong tập được biết là âm, nên FP không đếm được.
  - **MCC** — **không** đo được: công thức cần cả bốn ô của ma trận nhầm lẫn; ở đây hai ô (FP, TN) bằng 0 theo cấu tạo tập, nên MCC không xác định (mẫu số có nhân tử bằng 0).
  - **AUROC** — **không** đo được: trục x là FPR = FP/(FP+TN), cần **phân bố điểm của lớp âm**.
  - **AUPRC** — **không** đo được: trục y là precision tại mỗi mức recall, lại cần FP.
  - `[suy luận, dựa trên định nghĩa trong chính Ridgeway 2025 và trong Chicco & Jurman 2020 dẫn ở mục 4]`
- **Nhưng điều này sửa được**, và đây là phát hiện quan trọng nhất của tài liệu này: Zhang 2022 **định lượng 2.846 vị trí**, trong đó chỉ **152** đạt tiêu chí phụ thuộc SIRT2. Phần còn lại — tôi tính `2846 − 152 = **2.694** vị trí` — là **"được đo trong cùng thí nghiệm nhưng không đổi"**, đúng định nghĩa nhãn âm mà báo cáo nội bộ §2.3 đã đề xuất. Nếu lấy được Table S1 kèm fold-change, **tập trong tế bào thôi "chỉ-có-dương"**, và precision/MCC/AUPRC **trở thành đo được** `[suy luận]`.
- Khi đó tỉ lệ dương của tập trong tế bào là `152/2846 ≈ 5,3%` `[tự kiểm — tự tính]`, tức vẫn rất lệch, nên metric phải là AUPRC + MCC chứ không phải accuracy (xem mục 4).
- **Enrichment minh họa (không phải kết quả, chỉ là cách tính):** nếu lấy tỉ lệ dương của SIRT2 trong tập mảng (`1901/6801 = 27,95%` theo báo cáo nội bộ `[tác giả báo cáo]`) làm background, thì một bộ dự đoán ngẫu nhiên gọi dương với cùng tỉ lệ sẽ trúng kỳ vọng `149 × 0,2795 = 41,6` vị trí; quan sát 64 cho z ≈ 4,08, p nhị thức một phía ≈ `6,2e-5`, enrichment ≈ **1,54×** `[tự kiểm — tự tính, với giả định background nêu trên]`. **Cảnh báo:** background **đúng** phải là *tỉ lệ mô hình gọi dương trên tập nền*, không phải tỉ lệ nhãn dương trong tập huấn luyện. Con số 1,54× ở trên vì vậy **chỉ là minh họa cách làm**, không được trích như kết quả `[suy luận]`.

### Gaps

- **Chưa đọc được Supplementary Materials S1 và S3 của Ridgeway.** S1 chứa “data allocation”, K-fold, hyperparameter tuning và **cách chọn ngưỡng quyết định**; S3 chứa bảng mô hình tốt nhất của từng SIRT và con số “41.2% precision determined by the testing set” cho SIRT2. Không đọc S1 thì **không biết ngưỡng áp cho tập 149 là ngưỡng nào** (ngưỡng tối ưu F-score trên holdout? hay ngưỡng khác?). Đây là việc phải làm: tải PDF Supplementary Materials từ trang Nature Communications Chemistry `[chưa kiểm]`.
- **Chưa xác nhận Ridgeway có loại các vị trí trùng với tập huấn luyện ra khỏi 149 hay không.** Methods, mục *Experimental dataset generation and evaluation*, nói rõ “any duplicated sequences or sequences found within the training dataset were dropped” — nhưng câu đó nằm ở đoạn nói về **tập surface-exposed proteome**, không phải đoạn nói về 149 vị trí `[tự kiểm — đọc đúng đoạn này]`. Báo cáo nội bộ nói **46/149 vị trí (30,9%) nằm trong 6.801 vị trí của mảng** `[tác giả báo cáo]`. Nếu đúng và nếu Ridgeway không loại chúng, thì gần 1/3 "tập test" là mẫu huấn luyện → **43,0% bị thổi lên bởi memorization** `[suy luận, cần kiểm]`.
- **149 vs 152.** Zhang báo 152 vị trí giao hai tiêu chí; Ridgeway dùng 149. Chênh 3 vị trí chưa rõ do đâu (trùng peptide? không map được sang UniProt? lọc độ dài?) `[chưa kiểm]`.
- **Định nghĩa nhãn dương của mảng.** Ridgeway Methods, mục *Training dataset generation*, viết: “Peptides which produced a **signal ratio score of 1 or greater** were classified as positive” `[tự kiểm]`. Báo cáo nội bộ lại đếm theo cột **`substrate category = 1`** `[tác giả báo cáo]`. Hai cột này khác nhau trong file Rauh. Nếu Ridgeway thật sự ngưỡng trên `signal ratio` thì **toàn bộ bảng số dương theo isoform trong báo cáo nội bộ (176 / 1.901 / … ) có thể không phải nhãn mà Ridgeway dùng**. Phải mở lại `All_Sirts_Feature_Y_labels.csv` và đối chiếu với `Supplementary Data 1` của Rauh `[chưa kiểm — việc tuần 1]`.
- **Mô tả thiết kế tế bào không khớp** giữa Ridgeway (WT vs H187Y bất hoạt xúc tác) và Zhang (KD và OE). Chưa mở được Methods của Zhang đủ sâu để biết có nhánh H187Y hay không `[chưa kiểm]`.

---

## 2. Cách đánh giá đúng thống kê trên tập chỉ-có-dương

### Takeaway

Có ba họ phương pháp chính đáng: **(a)** báo recall tại *ngân sách dự đoán cố định* kèm enrichment so với background **cùng cấu tạo**; **(b)** metric xếp hạng kiểu "nhận dạng sớm" (EF, BEDROC) vay từ sàng lọc ảo trong hoá tin; **(c)** hiệu chỉnh PU — khôi phục metric thật từ metric PU bằng class prior. Nhưng **giải pháp tốt nhất cho đúng đề tài này không phải PU learning mà là dựng nhãn âm thật** từ 2.694 vị trí "được định lượng nhưng không đổi" của Zhang.

### Cited Findings

- **Khung lý thuyết PU:** Bekker & Davis (2020), *Learning from positive and unlabeled data: a survey*, Machine Learning 109:719–760, DOI [10.1007/s10994-020-05877-5](https://doi.org/10.1007/s10994-020-05877-5), bản tiền in [arXiv:1811.04820](https://arxiv.org/abs/1811.04820). Survey tổ chức quanh bảy câu hỏi nghiên cứu của lĩnh vực; đặt vấn đề là learner chỉ có mẫu dương cộng mẫu chưa gán nhãn, và tập chưa gán nhãn chứa cả dương lẫn âm `[tự kiểm qua tìm kiếm — đọc tóm tắt và thông tin xuất bản, chưa đọc toàn văn]`.
- **Giả định SCAR có thể sai:** cùng nhóm tác giả, Bekker, Robberechts & Davis (ECML PKDD 2019), *Beyond the Selected Completely At Random Assumption for Learning from Positive and Unlabeled Data*, [arXiv:1809.03207](https://arxiv.org/abs/1809.03207) — “most positive and unlabeled data is subject to selection biases” `[tự kiểm — tóm tắt]`.
- **Hiệu chỉnh metric bằng class prior:** Jain, White & Radivojac (AAAI 2017), *Recovering True Classifier Performance in Positive-Unlabeled Learning*, [arXiv:1702.00518](https://arxiv.org/abs/1702.00518), [bản AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/10937). Kết quả: đường ROC và precision–recall tính trên dữ liệu PU **có thể hiệu chỉnh được nếu biết class prior**; mở rộng được cho trường hợp nhãn dương có nhiễu, khi đó cần thêm tỉ lệ nhiễu; metric PU thô **đánh giá thấp** hiệu năng thật; tác giả khuyên **báo cả bản thô và bản đã hiệu chỉnh** `[tự kiểm — tóm tắt và phần kết luận qua tìm kiếm]`.
- **Hiệu chỉnh cho bài toán y–sinh, có cả MCC:** Ramola, Jain & Radivojac (PSB 2019), [PDF](https://www.ccs.neu.edu/home/radivojac/papers/ramola_psb_2019.pdf) — metric PU không hiệu chỉnh có thể sai rất nhiều, tuỳ tỉ lệ dương trong tập chưa gán nhãn và tỉ lệ âm bị gán sai; bài đưa cách hiệu chỉnh cho **bốn metric, trong đó có Matthews correlation** `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **Metric nhận dạng sớm trên danh sách xếp hạng:** Truchon & Bayly (2007), *Evaluating Virtual Screening Methods: Good and Bad Metrics for the "Early Recognition" Problem*, J Chem Inf Model 47(2):488–508. So sánh AUROC, AUAC, average rank, enrichment factor (EF), RIE; kết luận **AUROC/AUAC/average rank đều không phù hợp** khi mục tiêu là đẩy mẫu dương lên đầu danh sách, **EF không nhạy với thứ hạng trước và sau điểm cắt**, và đề xuất **BEDROC** `[tự kiểm — tóm tắt qua tìm kiếm; chưa đọc toàn văn nên chưa xác nhận công thức và tham số α khuyến nghị]`.
- **Khung thống kê cho các metric đó:** White và cộng sự (BMC Bioinformatics 2009), [PMC2722655](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2722655/) — BEDROC và RIE là **hai metric tương đương về mặt thống kê**; có "seesaw effect": nhấn nhận-dạng-sớm quá mạnh làm **giảm power** của metric `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **Hiệu năng tự báo thường cao hơn hiệu năng thật trên tập độc lập, đúng trong PTM:** benchmark 7 bộ dự đoán hydroxyl hóa, PLOS Comput Biol — “self-reported performance is found to widely overestimate the real accuracy measured on independent datasets”, và trên tập độc lập mới dựng **không bộ nào tốt hơn ngẫu nhiên** — [PMC7332089](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7332089/) `[tự kiểm — tóm tắt qua tìm kiếm; chưa đọc toàn văn]`.

### Inferences

- **Thứ tự ưu tiên tôi khuyến nghị, không phải PU trước:**
  1. **Dựng nhãn âm thật** từ Zhang Table S1 (2.846 định lượng − 152 phụ thuộc SIRT2 = 2.694 âm-trong-tế-bào). Khi có cả hai lớp, mọi metric bình thường (AUPRC, MCC) dùng được, và không phải nhờ tới hiệu chỉnh PU vốn **phụ thuộc vào một class prior mà mình không biết** `[suy luận]`.
  2. Nếu bước 1 thất bại (không lấy được Table S1 kèm fold-change), **mới** rơi về chế độ chỉ-có-dương, và khi đó dùng: recall ở ngân sách cố định + enrichment + BEDROC/EF, **kèm khoảng tin cậy bootstrap**.
  3. Hiệu chỉnh PU kiểu Jain 2017 **chỉ nên là một phân tích độ nhạy**: trình bày metric thật như một *hàm của class prior π* trên một dải π hợp lý, chứ không chốt một con số. Lý do: π ở đây là "tỉ lệ lysine trong proteome thật sự là cơ chất SIRT2 trong tế bào" — không ai biết, và mọi con số đơn lẻ sẽ là bịa `[suy luận]`.
- **Background phải "matched", nghĩa là gì ở đây.** 149 vị trí dương của Zhang không phải lysine ngẫu nhiên: chúng là lysine (i) **acetyl hóa thật** trong HCT116, (ii) **phát hiện được bằng khối phổ** (nên thuộc protein biểu hiện cao, và nằm trong peptide tryptic có độ dài/ái lực thuận lợi), (iii) **định lượng được ở cả hai điều kiện**. Nếu lấy background là toàn bộ 145.461 vị trí proteome, enrichment sẽ bị thổi lên bởi ba thiên lệch đó, chứ không phải bởi chất lượng mô hình. **Background đúng là chính 2.694 vị trí còn lại của Zhang** — cùng dòng tế bào, cùng phương pháp đo, cùng bộ lọc phát hiện `[suy luận]`.
- **So sánh hai mô hình trên tập chỉ-có-dương chỉ công bằng khi khớp ngân sách.** Cụ thể: buộc cả hai mô hình gọi dương **đúng cùng số lượng** vị trí trên một tập nền chung (ví dụ cùng 5% của 2.846 vị trí Zhang, hoặc cùng 5% của 145.461 vị trí Supplementary Data 13), rồi mới so recall trên 149. Đây chính là `recall@k`, và nó loại bỏ mánh hạ ngưỡng `[suy luận]`.
- Kinh nghiệm từ benchmark hydroxyl hóa ([PMC7332089](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7332089/)) nói rằng **kỳ vọng hợp lý cho đề tài này là kết quả âm hoặc gần-ngẫu-nhiên khi chuyển miền**. Nên đặt điều đó vào đề cương như một **kết quả được phép xảy ra**, không phải thất bại — khớp với câu hỏi số 2 dành cho GVHD trong báo cáo nội bộ `[suy luận]`.

### Gaps

- Chưa kiểm được Zhang Table S1 có cột fold-change **theo từng vị trí** cho cả hai điều kiện, hay chỉ có danh sách vị trí đã định lượng. Nếu chỉ có danh sách, vẫn dựng được nhãn âm nhị phân (2.694 vị trí "định lượng mà không vào danh sách 152") nhưng **không dựng được nhãn thứ tự trong tế bào** `[chưa kiểm]`.
- Chưa tìm được bài phương pháp nào **áp dụng PU-correction cụ thể cho dự đoán vị trí PTM**; các nguồn trên đều là phương pháp tổng quát hoặc y–sinh nói chung `[chưa kiểm sâu]`.
- Chưa xác nhận công thức và tham số α của BEDROC từ toàn văn Truchon & Bayly 2007. Nếu dùng, **phải khai báo α và lý do**, vì α quyết định "sớm" nghĩa là bao nhiêu phần trăm đầu danh sách `[chưa kiểm]`.

---

## 3. Chia tập có kiểm soát rò rỉ: theo protein VÀ theo đồng dạng trình tự

### Takeaway

Chia theo protein là **chưa đủ** và chia theo đồng dạng của chính peptide 13 aa là **vô nghĩa về mặt kỹ thuật**. Cách đúng: gom cụm **chuỗi protein mẹ đầy đủ** bằng MMseqs2 ở ngưỡng **30% identity** (ngưỡng này có căn cứ từ Rost 1999), gán **cả cụm** vào một phân vùng (thuật toán GraphPart), rồi **thêm** một bước khử trùng lặp ở mức cửa sổ 13-mer mà ngưỡng phải **suy ra từ phân bố dữ liệu**, không chọn tay.

### Cited Findings

- **Ngưỡng 30% có căn cứ, không phải chọn tuỳ ý:** Rost (1999), *Twilight zone of protein sequence alignments*, Protein Eng 12(2):85–94 — phân tích hơn một triệu alignment của các cặp đã biết cấu trúc; **trên ngưỡng khoảng 30% identity, 90% các cặp là homolog; dưới 25% thì dưới 10% là homolog**; vùng 20–35% là "twilight zone"; và **kết luận phụ thuộc mạnh vào độ dài alignment** — ví dụ 10 residue giống nhau trong alignment dài 16 (>60%) **không** cho suy ra tương đồng cấu trúc. [Bản PDF](https://www.biostat.wisc.edu/~kbroman/teaching/statgen/2004/refs/rost1.pdf), [bản ghi thư mục](https://portal.fis.tum.de/en/publications/twilight-zone-of-protein-sequence-alignments/) `[tự kiểm — tóm tắt qua tìm kiếm; chưa đọc toàn văn PDF]`.
- **Lý do không nên chỉ "lọc bớt cho hết trùng":** GraphPart — Teufel và cộng sự (2023), *GraphPart: homology partitioning for biological sequence analysis*, NAR Genomics and Bioinformatics 5(4):lqad088, [PMC10578201](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10578201/), [mã nguồn](https://github.com/graph-part/graph-part). Đặt vấn đề: nếu chuỗi họ hàng gần bị chia hai bên train/test thì **"performance of prediction methods will tend to be overestimated"**; cách cũ là *xoá* chuỗi cho tới khi không còn cặp gần, GraphPart thì **giữ chuỗi và gán cụm vào cùng một phân vùng**, nhờ vậy giữ được nhiều mẫu hơn với mức tách đồng dạng tương đương. Hỗ trợ `needleall` (EMBOSS) và **MMseqs2**, có chế độ precomputed `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **Công cụ gom cụm:** MMseqs2 — Steinegger & Söding (2017), Nat Biotechnol, DOI [10.1038/nbt.3988](https://doi.org/10.1038/nbt.3988) `[chưa kiểm — DOI từ kiến thức nền, phải tra lại]`. CD-HIT — Fu và cộng sự (2012), Bioinformatics 28(23):3150–3152, DOI [10.1093/bioinformatics/bts565](https://doi.org/10.1093/bioinformatics/bts565) `[chưa kiểm — DOI từ kiến thức nền, phải tra lại]`.
- **Thực tế trong lĩnh vực PTM lysine:** dbPTM công bố “non-homologous benchmark datasets to evaluate the predictive power for PTM sites prediction tools” — [trang tải dbPTM](https://biomics.lab.nycu.edu.tw/dbPTM/download.php); và có tiền lệ dùng **CD-HIT ngưỡng 40% identity** để dựng tập không dư thừa cho PTM lysine — [IJBS v14 p0946 supplementary](https://ijbs.com/v14/p0946/ijbsv14p0946s1.pdf) `[tự kiểm — qua tìm kiếm, chưa đọc toàn văn; không có bằng chứng ngưỡng 40% được *hiệu chuẩn* để chống rò rỉ, chỉ là tiền lệ sử dụng]`.
- **Cái mà Ridgeway 2025 thực sự làm:** Methods, *Experimental dataset generation and evaluation* — “Additionally, **any duplicated sequences or sequences found within the training dataset were dropped**”. Không có câu nào nói tới gom cụm đồng dạng, CD-HIT, MMseqs2, hay chia theo protein — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.
- **Cách chia của Ridgeway cho họ SIRT:** “As it was available, a holdout set from the MethylSight investigation was employed … for the SET8 model. **No holdout set was obtained for MuSiteDeep, therefore the associated investigations employed the use of a holdout set representative of 10% of the experimental data.**” Và ngưỡng quyết định: “An **m-threshold analysis was then performed using the holdout set** of never-seen data to effectively assess the effect of the decision threshold on performance” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.

### Inferences

- **Vì sao không gom cụm trên chính peptide 13 aa.** Với chuỗi dài 13, một mismatch đổi identity đi `1/13 ≈ 7,7%`, và hai 13-mer ngẫu nhiên đã có identity kỳ vọng khoảng 5–6% chỉ do trùng ngẫu nhiên trong 20 chữ cái. Rost 1999 nói thẳng rằng ở alignment ngắn, identity cao **không** suy ra được quan hệ. Thêm nữa CD-HIT/MMseqs2 dựa trên k-mer seeding nên **mất độ nhạy trên chuỗi rất ngắn**. Kết luận: ngưỡng % identity áp lên 13-mer là con số không có nghĩa `[suy luận, dựa trên Rost 1999]`.
- **Đơn vị gom cụm đúng là protein mẹ.** Rò rỉ trong bài toán này đi qua hai đường: (i) **cùng protein** — hai lysine khác nhau của cùng protein có ngữ cảnh chung và cùng thuộc tính sinh học; (ii) **protein đồng dạng** — paralog/ortholog có motif gần y hệt, ví dụ các histone, các tubulin, các enzyme đường phân. Chia theo protein chỉ chặn đường (i) `[suy luận]`.
- **Hệ quả cho đề tài:** báo cáo nội bộ nói 6.801 vị trí thuộc **2.999 protein** `[tác giả báo cáo]`, tức trung bình 2,3 vị trí/protein → chia theo protein là bắt buộc nhưng rẻ. Còn số cụm ở 30% identity thì **chưa biết**, và con số đó quyết định bài toán có đủ dữ liệu để chia 5 phần hay không. **Đây là phép đo đầu tiên phải làm, trước cả khi chọn kiến trúc** `[suy luận]`.

### Đề xuất giao thức chia tập (cụ thể, đủ để viết vào đề cương)

Năm phân vùng, **không bốn**, vì conformal cần tập hiệu chỉnh riêng và chuyển miền cần tập trong tế bào riêng.

| Phân vùng | Nguồn | Dùng để | Đo **in-domain** hay **chuyển miền** |
|---|---|---|---|
| `TRAIN` | mảng Rauh, ~70% số cụm | huấn luyện tham số | — |
| `VAL` | mảng Rauh, ~10% số cụm | chọn mô hình, hyperparameter, early stopping | in-domain |
| `CALIB` | mảng Rauh, ~10% số cụm | **chỉ** chọn ngưỡng quyết định và hiệu chỉnh conformal. Không bao giờ dùng để chọn mô hình | — (tập công cụ) |
| `TEST-IN` | mảng Rauh, ~10% số cụm, **niêm phong** | báo cáo hiệu năng in-domain, mở đúng một lần | **in-domain** |
| `TEST-OUT` | Zhang 2022: 152 dương + 2.694 âm-trong-tế-bào | báo cáo **chuyển miền** in vitro → trong tế bào | **chuyển miền** |

Quy tắc kèm theo:

1. **Gom cụm theo chuỗi protein mẹ đầy đủ** (lấy từ UniProt theo accession của 2.999 protein), MMseqs2 `easy-cluster` với `--min-seq-id 0.3 -c 0.8`, rồi gán **toàn bộ cụm** vào một phân vùng. Ngưỡng 0,3 lấy theo Rost 1999 (trên ~30% thì 90% cặp là homolog). Nếu dùng GraphPart thay cho gom cụm thủ công thì tốt hơn vì giữ được nhiều mẫu hơn ([PMC10578201](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10578201/)).
2. **Báo cáo độ nhạy theo ngưỡng.** Chạy lại toàn bộ ở **0,3 và 0,5**, báo cả hai bảng kết quả. Nếu khoảng cách giữa hai bảng lớn, đó **chính là** một kết quả đáng viết (đo được mức rò rỉ đồng dạng), không phải rắc rối. Không được chọn ngưỡng nào cho ra số đẹp hơn.
3. **Bước khử trùng lặp thứ hai ở mức 13-mer.** Trước khi niêm phong `TEST-IN`, tính khoảng cách Hamming từ mỗi 13-mer trong `TEST-IN` tới 13-mer gần nhất trong `TRAIN`. **Không chọn ngưỡng tay.** Thay vào đó: (a) vẽ phân bố khoảng cách này và phân bố tương ứng cho cặp 13-mer ngẫu nhiên; (b) loại các cặp nằm ở đuôi mà phân bố thật tách rõ khỏi phân bố ngẫu nhiên; (c) **báo cáo hiệu năng phân tầng theo khoảng cách này** (ví dụ các dải Hamming 0–2, 3–5, 6+). Cách (c) mạnh hơn cách (b) vì nó biến rò rỉ thành đại lượng đo được, đúng tinh thần phép đo khoảng cách Levenshtein tới mẫu train gần nhất trong [PepSpecBench](https://arxiv.org/pdf/2605.01945) `[tự kiểm — qua tìm kiếm, là preprint, nhãn chất lượng thấp hơn]`.
4. **`TEST-OUT` phải được lọc chống rò rỉ theo cả hai chiều.** Loại khỏi `TRAIN/VAL/CALIB` mọi protein thuộc cùng cụm 30% với protein nào xuất hiện trong `TEST-OUT`. Nếu không làm, 108/149 vị trí thuộc protein đã có trong mảng (`[tác giả báo cáo]`) sẽ biến phép đo chuyển miền thành phép đo memorization.
5. **Phải báo hai phiên bản của `TEST-OUT`:** (a) **loại** 46 vị trí trùng hẳn với mảng; (b) giữ. Chênh lệch giữa (a) và (b) là **ước lượng trực tiếp phần đóng góp của memorization vào con số 43,0% của Ridgeway**. Đây là một đóng góp đo được, rẻ, và **không ai đã làm** `[suy luận]`.
6. **Ngưỡng cho `TEST-OUT` phải lấy từ `CALIB` (miền mảng), không từ `TEST-OUT`.** Nếu muốn báo thêm phiên bản hiệu chỉnh lại theo miền tế bào, thì **chia `TEST-OUT` làm hai nửa theo cụm protein**: một nửa hiệu chỉnh, một nửa báo cáo. Báo cả hai con số và nói rõ cái nào là chuyển miền *không* hiệu chỉnh (đây mới là câu hỏi nghiên cứu) và cái nào là chuyển miền *có* hiệu chỉnh (đây là giới hạn trên).
7. **Niêm phong.** Ghi hash của file phân vùng vào repo trước khi chạy thí nghiệm đầu tiên; `TEST-IN` và `TEST-OUT` mở đúng một lần ở cuối. Đây là cách trả lời "cổng dữ liệu" mà GVHD nêu từ buổi 1.

### Gaps

- **Chưa biết số cụm ở 30% identity**, nên chưa biết tỉ lệ 70/10/10/10 có khả thi hay không. Nếu số cụm nhỏ (ví dụ dưới ~300), phải chuyển sang **nested CV theo cụm** thay vì chia một lần, và `CALIB` phải lấy bằng cross-conformal `[chưa kiểm — phép đo tuần 1]`.
- Chưa tra lại DOI của MMseqs2 và CD-HIT từ nguồn gốc `[chưa kiểm]`.
- Chưa tìm được bài **đo định lượng** mức thổi phồng do rò rỉ đồng dạng **riêng cho dự đoán vị trí PTM** (khác với benchmark hydroxyl hóa [PMC7332089](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7332089/) vốn đo "tự báo vs độc lập" nói chung). Nếu thật không có, thì chính đề tài này **đo được nó lần đầu cho họ sirtuin**, và đó là một đóng góp phương pháp đáng kể hơn là một dòng ablation `[chưa kiểm sâu + suy luận]`.

---

## 4. Metric theo từng tình huống

### Takeaway

Bốn tình huống, bốn bộ metric. Nguyên tắc chung: **accuracy và AUROC bị cấm làm metric chính** ở đây (SIRT1 đạt 97,4% accuracy bằng cách luôn trả lời "không"); AUPRC + MCC làm trụ cho nhãn nhị phân; macro (không micro) cho đa nhãn 7 isoform vì lượng enzyme khác nhau giữa các isoform; và tập trong tế bào dùng recall-ở-ngân-sách + enrichment nếu không có nhãn âm, AUPRC + MCC nếu có.

### Cited Findings

- **MCC thay cho accuracy và F1:** Chicco & Jurman (2020), *The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation*, BMC Genomics 21:6, DOI [10.1186/s12864-019-6413-7](https://doi.org/10.1186/s12864-019-6413-7), [PMC6941312](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6941312/). Luận điểm: accuracy và F1 “can dangerously show over-optimistic inflated results, especially on imbalanced datasets”; MCC “produces a high score only if the prediction obtained good results in **all of the four confusion matrix categories**”; F1 **phụ thuộc vào việc lớp nào được gọi là dương**, MCC thì không `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **PR thay cho ROC khi lệch lớp:** Saito & Rehmsmeier (2015), *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*, PLoS ONE 10(3):e0118432, DOI [10.1371/journal.pone.0118432](https://doi.org/10.1371/journal.pone.0118432), [PMC4349800](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4349800/). Luận điểm: “the visual interpretability of ROC plots in the context of imbalanced datasets can be **deceptive** … owing to an intuitive but **wrong interpretation of specificity**”; PR “can provide the viewer with an accurate prediction of future classification performance due to the fact that they evaluate the fraction of true positives among positive predictions”; bài viết nhắm thẳng vào tin sinh `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **AUROC cũng không phù hợp cho mục tiêu "nhận dạng sớm":** Truchon & Bayly (2007), J Chem Inf Model 47(2):488–508 — ROC/AUAC/average rank “have the same inappropriate behaviors that make them poor metrics for judging methods meant to rank actives early” `[tự kiểm — tóm tắt qua tìm kiếm]`.
- **Chính Ridgeway cũng chọn F-score vì lệch lớp**, và nói rõ specificity bị thổi: “The F-score was selected as the best measurement … considering the imbalanced representation of positives”; “rather than using specificity, **which is falsely inflated by the large proportion of negative identifications**” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`. Nhưng bài **không** báo MCC hay AUPRC ở đâu cả; chỉ có F-score, precision, recall, specificity, và các đường PR/ROC cho SET8 `[tự kiểm]`.
- **Số liệu lệch lớp của đề tài:** SIRT1 có **176 dương / 6.801**, SIRT5 có **2.614 / 6.801** — [topic-final-recommendation.md §2.1](../../reports/topic-final-recommendation.md) `[tác giả báo cáo]`. Tôi tính: SIRT1 tỉ lệ dương `2,59%`, nên **accuracy của bộ dự đoán "luôn trả lời âm" là 97,41%**; SIRT5 tỉ lệ dương `38,44%` `[tự kiểm — tự tính]`.
- **Lượng enzyme khác nhau giữa các isoform** nên tín hiệu không so trực tiếp được giữa các isoform — [topic-final-recommendation.md §2.1 điểm 2](../../reports/topic-final-recommendation.md), dẫn từ Rauh 2013 `[tác giả báo cáo]`.
- **Metric đa nhãn:** Zhang & Zhou (2014), *A Review on Multi-Label Learning Algorithms*, IEEE TKDE 26(8):1819–1837 `[chưa kiểm — từ kiến thức nền, phải tra DOI]`. Wu & Zhou (2017), *A Unified View of Multi-Label Performance Measures*, ICML `[chưa kiểm]`. Sechidis, Tsoumakas & Vlahavas (2011), *On the stratification of multi-label data*, ECML PKDD — phân tầng cho dữ liệu đa nhãn `[chưa kiểm]`.

### Đề xuất metric theo tình huống

**(a) Nhãn nhị phân, một isoform, in-domain (`TEST-IN`)**

- **Chính:** **AUPRC** (đường cong, kèm giá trị baseline = tỉ lệ dương, vì AUPRC của bộ ngẫu nhiên **bằng tỉ lệ dương**, nên AUPRC 0,30 là tốt cho SIRT1 nhưng tệ cho SIRT5) + **MCC tại ngưỡng đã chốt trên `CALIB`**.
- **Kèm:** precision và recall tại đúng ngưỡng đó; **khoảng tin cậy bootstrap theo cụm protein** (resample cụm, không resample vị trí — nếu resample vị trí thì CI quá hẹp vì các vị trí cùng protein tương quan).
- **Cấm làm metric chính:** accuracy (lý do: 97,41% cho SIRT1 `[tự kiểm]`), specificity một mình (chính Ridgeway nói nó bị thổi `[tự kiểm]`), AUROC (Saito & Rehmsmeier; Truchon & Bayly).
- **AUROC vẫn nên báo nhưng ở cột phụ**, vì nhiều bài cùng nhánh (kể cả NAD_MCNN AUC 0,9733 trong báo cáo nội bộ `[tác giả báo cáo]`) báo AUC, nên cần nó để nối với tài liệu — kèm một câu giải thích vì sao nó không phải metric quyết định.

**(b) Nhãn liên tục / thứ tự (`signal ratio`, `efficiency`, có `ratio error`)**

- **Spearman ρ** và **Kendall τ** giữa điểm dự đoán và `signal ratio` quan sát, tính **trong từng isoform riêng** (vì không so được giữa isoform).
- **Trọng số theo `1/ratio error²`** trong cả loss và metric; báo cả bản có trọng số và không trọng số. Lý do có căn cứ: sai số trung vị của SIRT1 là 0,37 so với 0,21–0,27 của các isoform khác `[tác giả báo cáo]`, nên bỏ qua sai số là thiên vị SIRT1.
- Nếu đóng khung thành hồi quy thứ tự (ordinal): **quadratic weighted kappa** cho các bin, cộng một phép kiểm tính đơn điệu (điểm dự đoán có tăng theo bin hay không).
- **Không dùng** Pearson r hay RMSE làm metric chính: `signal ratio` là tỉ lệ, phân bố lệch, và chính Rauh từ chối diễn giải chi tiết giá trị tỉ lệ `[tác giả báo cáo]`.

**(c) Đa nhãn, 7 isoform**

| Kiểu trung bình | Có nên dùng | Lý do |
|---|---|---|
| **Per-label** (7 bảng riêng: AUPRC, MCC) | **Bắt buộc, là bảng chính** | Mỗi isoform có tỉ lệ dương khác nhau (2,59% → 38,44% `[tự kiểm]`), nên một con số gộp che mất SIRT1 |
| **Macro-average** (bình quân 7 giá trị per-label) | **Nên, làm số tổng hợp** | Mỗi isoform đóng góp bằng nhau, nên SIRT1 không bị SIRT5 nuốt |
| **Micro-average** (gộp hết ô confusion rồi tính) | **Không nên làm số chính** | Bị SIRT5 và SIRT2 chi phối; nặng hơn nữa, nó **cộng dồn các nhãn mà bản thân Rauh nói không so được với nhau** vì lượng enzyme khác nhau `[suy luận, dựa trên dữ kiện lượng enzyme]` |
| **Example-based** (Hamming loss, subset accuracy) | Chỉ làm phụ, và phải kèm baseline | Hamming loss bị lệch lớp làm cho "đoán toàn âm" trông tốt; subset accuracy (khớp đúng cả 7 nhãn) quá nghiêm, và với phân bố 1.107 vị trí âm-với-cả-7 trên 6.801 `[tác giả báo cáo]` thì "đoán toàn âm" đã đạt subset accuracy ~16,3% `[tự kiểm — tự tính]` |

- Thêm một metric **đúng với sản phẩm đầu ra**: nếu website trả về *tập* isoform, thì phải báo **F1 theo mẫu (example-based F1)** và, nếu có conformal, **độ phủ thực tế theo từng isoform (Mondrian) cộng kích thước tập trung bình**. Độ phủ gộp chung 7 isoform che mất chuyện SIRT1 không đạt phủ.
- Chia tập đa nhãn phải **phân tầng theo đa nhãn**, không phân tầng theo một nhãn (Sechidis 2011 `[chưa kiểm]`) — nhưng **ràng buộc cụm protein thắng ràng buộc phân tầng** khi hai cái xung đột. Báo cáo tỉ lệ dương của từng isoform trong từng phân vùng để người đọc thấy mức mất cân.

**(d) Tập chỉ-có-dương trong tế bào**

- Nếu **không có** nhãn âm: **recall tại ngân sách cố định** (cùng tỉ lệ gọi dương cho mọi mô hình so sánh) + **enrichment so với background matched** kèm **kiểm định nhị thức/hypergeometric** + **BEDROC/EF** cho phần xếp hạng + CI bootstrap. **Tuyệt đối không gọi nó là precision.**
- Nếu **có** nhãn âm (2.694 vị trí Zhang): dùng đúng bộ (a), tức **AUPRC + MCC**, với baseline AUPRC = `152/2846 ≈ 5,3%` `[tự kiểm]`.
- Trong cả hai trường hợp: báo **phân tầng theo khoảng cách đồng dạng tới tập huấn luyện** và theo "có/không nằm trong 6.801 vị trí mảng".

### Inferences

- Việc Ridgeway **không báo MCC hay AUPRC ở bất kỳ đâu** `[tự kiểm]`, chỉ báo F-score/precision/recall tại ngưỡng tự chọn, có nghĩa là **không có số nào của họ dùng lại trực tiếp được** làm mốc so sánh cho một bảng MCC/AUPRC. Muốn có mốc, **phải chạy lại mô hình của họ** từ repo [ML-Hybrid_Ensemble_Method](https://github.com/nashirag/ML-Hybrid_Ensemble_Method) `[suy luận]`.
- Cổng dừng tuần 4 trong báo cáo nội bộ ("MCC ≥ baseline cho ≥ 4/7 isoform" `[tác giả báo cáo]`) **không dùng được như đang viết**: với 176 dương, MCC của SIRT1 có CI rộng tới mức "≥" hay "<" là chuyện may rủi. Phải sửa thành so sánh **có CI bootstrap theo cụm** và/hoặc **kiểm định bắt cặp** (ví dụ bootstrap hiệu MCC trên cùng các cụm test) `[suy luận]`.

### Gaps

- Chưa tra lại DOI của Zhang & Zhou 2014, Wu & Zhou 2017, Sechidis 2011 `[chưa kiểm]`.
- Chưa tìm được bài phương pháp nói riêng về **chọn kiểu trung bình đa nhãn khi các nhãn được đo ở thang không so sánh được** (ở đây: lượng enzyme khác nhau). Lập luận "không dùng micro" của tôi là `[suy luận]` từ dữ kiện sinh học, chưa có nguồn phương pháp hậu thuẫn.

---

## 5. Bậc thang baseline và ablation: mỗi bậc tách được điều gì

### Takeaway

Bậc thang trong báo cáo nội bộ (6 bậc) **thiếu hai bậc quan trọng** (bộ dự đoán hằng/ngẫu nhiên có khai báo tỉ lệ dương, và MusiteDeep đứng một mình) và **gộp nhiều biến thay đổi trong một bậc** (bậc 4→5 đổi cả fine-tuning lẫn không gì khác thì được, nhưng bậc 3→4 đổi đồng thời biểu diễn **và** kiến trúc **và** số đầu ra). Dưới đây là bậc thang đã tách biến, kèm phát biểu rõ **mỗi bậc cô lập cái gì**.

### Đề xuất bậc thang (mỗi bậc đổi **đúng một** thứ so với bậc trước)

| # | Mô hình | Đổi gì so với bậc trước | **Cô lập được điều gì** |
|---|---|---|---|
| **B0** | Hằng số: luôn trả lời âm; và ngẫu nhiên gọi dương đúng tỉ lệ dương của isoform | — | **Sàn tuyệt đối.** Buộc phải có, vì nó cho con số accuracy 97,41% của SIRT1 `[tự kiểm]` và AUPRC baseline của từng isoform. Ridgeway có dùng dummy classifier `[tự kiểm]`, nên bỏ bậc này là đi lùi |
| **B1** | PSSM / scoring matrix trên cửa sổ 13 aa, 7 ma trận riêng | thêm thông tin vị trí–amino acid | Phần hiệu năng giải thích được **chỉ bằng ưu tiên từng vị trí độc lập** (motif tuyến tính). Đây đúng là phương pháp "permutation array motif" mà Ridgeway đo được precision 2% `[tự kiểm]` |
| **B2** | k-mer / gapped k-mer + SVM (hoặc logistic regression) | thêm tương tác giữa các vị trí | Phần hiệu năng do **tương tác bậc cao giữa các vị trí**, mà PSSM không bắt được |
| **B3** | MusiteDeep (N6-acetyl-lysine) **đứng một mình** | bỏ phần đặc hiệu isoform | **Bao nhiêu phần của "đặc hiệu isoform" thật ra chỉ là "vị trí này có acetyl hóa hay không".** Bậc này là bắt buộc: Ridgeway dùng MusiteDeep làm bộ dự đoán phụ trong ensemble `[tự kiểm]`, nên nếu MusiteDeep một mình đã đạt gần bằng cả ensemble thì "đặc hiệu isoform" chưa được chứng minh |
| **B4** | 443 đặc trưng làm tay + LDA/decision tree, **chạy lại trên cách chia của mình** | tái dựng baseline của bài 2025 | **Mốc so sánh hợp lệ duy nhất** với Ridgeway 2025. Không chạy lại thì không có mốc MCC/AUPRC nào (xem §4) |
| **B5** | one-hot 13×20 + CNN một cửa sổ, 7 mô hình rời | đổi *bộ học* sang mạng neural, giữ biểu diễn thô | Phần lợi do **mạng neural** so với mô hình tuyến tính/cây, **không lẫn** với lợi do PLM |
| **B6** | **ESM-2 đóng băng** + CNN một cửa sổ, 7 mô hình rời | đổi *biểu diễn* one-hot → PLM | **Đóng góp riêng của PLM.** Đây là phép so mà GVHD hỏi ở tiêu chí 3 ("có gì mới hơn PLM không") — phải có để trả lời |
| **B7** | ESM-2 đóng băng + **mCNN nhiều cửa sổ**, 7 mô hình rời | đổi *đầu* một cửa sổ → nhiều cửa sổ | **Đóng góp riêng của mCNN**, tách khỏi đóng góp của PLM. Nếu B7 ≈ B6, thì mCNN không đáng và phải nói thẳng — kể cả khi mCNN là khung quen của GVHD |
| **B8** | ESM-2 đóng băng + mCNN, **một mô hình 7 đầu ra** | đổi 7 mô hình rời → một mô hình chia sẻ | **Lợi của chia sẻ tham số giữa các isoform.** Có cơ sở dữ liệu: 2.087 vị trí dương với đúng 2 isoform `[tác giả báo cáo]`. **Isoform nào được lợi và isoform nào bị hại** là câu trả lời quan trọng nhất ở đây — kỳ vọng SIRT1 (176 dương) được lợi nhiều nhất `[suy luận]` |
| **B9** | ESM-2 + **LoRA** + mCNN, 7 đầu ra | fine-tune thay vì đóng băng | Đóng góp riêng của fine-tuning, trên đúng kiến trúc và cách chia đã cố định |
| **B10** | B9 + **nhãn thứ tự có trọng số sai số** thay nhãn nhị phân | đổi *mục tiêu học* | **Đóng góp của nhãn liên tục.** Đây là một trong hai điểm mới tin học mà đề tài tự nhận; nếu không tách thành một bậc riêng thì không chứng minh được |
| **B11** | B10 + **error-weighted loss** riêng biệt | tách trọng số ra khỏi việc chuyển sang thang thứ tự | Phân biệt "dùng thang liên tục" với "cân theo độ tin cậy của phép đo". Hai cái này hay bị gộp |
| **B12** | B10/B11 + **ngữ cảnh sinh học thêm** (cửa sổ rộng hơn, khu trú dưới tế bào, cấu trúc/disorder) | thêm đặc trưng ngoài cửa sổ 13 aa | Đóng góp của ngữ cảnh. **Phải ablate từng loại ngữ cảnh một**, vì khu trú dưới tế bào là đặc trưng **mức protein** và rất dễ gây rò rỉ: nếu chia theo protein không nghiêm, mô hình chỉ cần học "protein này ở ty thể" là xong `[suy luận]` |
| **B13** | B12 + **hiệu chỉnh ngưỡng theo từng isoform** trên `CALIB` | đổi cách chọn ngưỡng | Tách "mô hình tốt hơn" khỏi "ngưỡng đặt khéo hơn". Bắt buộc, vì lượng enzyme khác nhau giữa isoform `[tác giả báo cáo]` |
| **B14** | B13 + **conformal theo isoform (Mondrian)** | thêm lớp bảo đảm | Không đổi thứ hạng dự đoán, nên **không được báo như "tăng hiệu năng"**; chỉ báo độ phủ và kích thước tập |

**Hai ablation thuộc về phần đánh giá, không phải phần mô hình, nhưng quan trọng hơn vài bậc trên:**

- **L1 — ablation rò rỉ:** chạy lại bậc tốt nhất ở ba cách chia (ngẫu nhiên theo vị trí / theo protein / theo cụm 30%). Cô lập **mức thổi phồng do rò rỉ**. Dự đoán: khoảng cách giữa "ngẫu nhiên theo vị trí" và "theo cụm 30%" sẽ lớn hơn mọi khoảng cách giữa các bậc B5→B13 `[suy luận]`. Nếu đúng, đó là thông điệp chính của luận văn.
- **L2 — ablation memorization trên `TEST-OUT`:** báo recall/AUPRC riêng cho (a) 46 vị trí có trong mảng, (b) 103 vị trí không có, (c) phân tầng theo khoảng cách đồng dạng. Cô lập **phần của con số chuyển miền đến từ việc đã thấy mẫu đó**.

### Inferences

- Bậc thang trong báo cáo nội bộ đi thẳng từ "đặc trưng làm tay + LDA" (bậc 3) sang "ESM-2 đóng băng + mCNN" (bậc 4) `[tác giả báo cáo]`. Bước đó đổi **ba thứ cùng lúc** (biểu diễn, kiến trúc, số đầu ra), nên **nếu có cải thiện thì không gán được cho nguyên nhân nào** — đúng điều GVHD đòi ở tiêu chí 2 `[suy luận]`.
- **B3 (MusiteDeep một mình) là bậc dễ bị bỏ nhất và nguy hiểm nhất nếu bỏ.** Ridgeway dùng MusiteDeep làm thành phần thứ hai của ensemble SIRT `[tự kiểm]`. Nếu phần lớn hiệu năng trên tập Zhang đến từ "vị trí này acetyl hóa trong tế bào" (mà MusiteDeep bắt được) chứ từ "SIRT2 deacetyl hóa nó", thì cả con số 43,0% lẫn con số của mình đều không nói gì về **đặc hiệu isoform** — và lưu ý tập Zhang **toàn là vị trí acetyl hóa thật**, nên lợi thế này càng lớn `[suy luận]`.
- Số bậc như trên là 15, quá nhiều cho 8–9 tuần nếu chạy đủ 7 isoform × 2 ngưỡng đồng dạng × bootstrap. **Đề xuất rút:** chạy đủ bậc thang trên **2 isoform** (SIRT2 vì có `TEST-OUT`, và SIRT1 vì là trường hợp xấu nhất), rồi chỉ chạy B0, B4, B8, B13 cho 5 isoform còn lại. Nói rõ lựa chọn này trong đề cương thay vì âm thầm bỏ bậc `[suy luận]`.

### Gaps

- Chưa kiểm được repo [ML-Hybrid_Ensemble_Method](https://github.com/nashirag/ML-Hybrid_Ensemble_Method) có đủ mã để chạy lại 7 mô hình SIRT (bậc B4) hay chỉ có mã SET8, và có kèm random seed / cách chia hay không `[chưa kiểm — việc tuần 1, quan trọng vì B4 là mốc so sánh duy nhất]`.
- Chưa biết MusiteDeep bản nào Ridgeway dùng và có chạy lại được không (bậc B3) `[chưa kiểm]`.

---

## 6. So với điểm số đã công bố (Supplementary Data 13) khác gì so với chạy lại mô hình của họ

### Takeaway

Hai phép so cho hai loại kết luận **khác hẳn nhau**. So với điểm số đã công bố chỉ chứng minh được **"xếp hạng của tôi khác/tốt hơn xếp hạng của họ trên tập này"** — một phát biểu mô tả, không phải phát biểu nhân quả về phương pháp. Chỉ **chạy lại mô hình của họ trên cách chia của mình** mới cho phát biểu "phương pháp của tôi tốt hơn phương pháp của họ". Cả hai đều nên làm, nhưng **không được trình bày như một**.

### Cited Findings

- Báo cáo nội bộ: `Supplementary Data 13` là “dự đoán cho toàn bộ proteome: **145.461 vị trí × 7 isoform, có cả điểm số liên tục**”, và kết luận “baseline của bài 2025 **có sẵn dự đoán để so trực tiếp từng vị trí, không cần chạy lại mô hình của họ**” — [topic-final-recommendation.md §2.2](../../reports/topic-final-recommendation.md) `[tác giả báo cáo]`.
- Mã và nhãn của Ridgeway công khai: [github.com/nashirag/ML-Hybrid_Ensemble_Method](https://github.com/nashirag/ML-Hybrid_Ensemble_Method) `[tác giả báo cáo — tôi chưa mở repo trong phiên này]`.
- Tập mà Supplementary Data 13 phủ được dựng từ **surface-exposed lysine proteome**, với bộ lọc NetSurfP1.0 ở ngưỡng 0,2, và **đã loại bỏ** “any duplicated sequences or sequences found within the training dataset” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/), Methods *Experimental dataset generation and evaluation* `[tự kiểm]`.
- Ngưỡng của họ được chọn bằng “m-threshold analysis … using the holdout set”, và holdout của SIRT là “10% of the experimental data” — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.
- Họ còn báo “41.2% precision determined by the testing set (Supplementary Materials S3.)” cho SIRT2, cạnh con số 43,0% — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự kiểm]`.

### Phát biểu nào hợp lệ, phát biểu nào không

| Phép so | Phát biểu **hợp lệ** | Phát biểu **không** hợp lệ |
|---|---|---|
| **A. Điểm số liên tục của họ (Supp. Data 13) vs điểm của tôi, trên cùng tập, so bằng metric xếp hạng** | "Trên tập X, điểm số của mô hình tôi xếp 152 vị trí phụ thuộc SIRT2 lên cao hơn điểm số đã công bố của Ridgeway 2025, với AUPRC/BEDROC là …, CI …" | "Mô hình tôi tốt hơn phương pháp của Ridgeway" — không, vì điểm của họ sinh ra từ **tập huấn luyện khác và cách chia khác** |
| **B. Nhãn nhị phân đã công bố của họ (ngưỡng của họ) vs nhãn của tôi (ngưỡng của tôi)** | *Không có phát biểu nào hợp lệ* về chất lượng tương đối | Mọi so sánh recall/precision ở hai ngưỡng khác nhau. Đây là lỗi dễ mắc nhất |
| **C. Chạy lại mã của họ trên `TRAIN` của tôi, báo trên `TEST-IN`/`TEST-OUT` của tôi** | "Với cùng dữ liệu huấn luyện, cùng cách chia kiểm soát đồng dạng, cùng ngưỡng chọn trên `CALIB`, phương pháp của tôi đạt MCC … so với … của phương pháp 443-đặc-trưng + LDA/cây" | "Tôi tái tạo được kết quả công bố của họ" — chỉ nói được điều đó nếu chạy lại trên **cách chia của họ** |
| **D. Chạy lại mã của họ trên cách chia của *họ*** | "Tôi tái tạo được / không tái tạo được con số công bố" — đây là kiểm chứng tính tái lập, có giá trị riêng | Không dùng con số này làm mốc so sánh cho mô hình mới của mình |

### Những cái bẫy cụ thể của phép so A

1. **Ngưỡng khác nhau.** Supplementary Data 13 có điểm liên tục, nên bẫy này **tránh được** bằng cách chỉ so metric xếp hạng (AUPRC, BEDROC) hoặc so ở **ngân sách khớp nhau**. Nếu dùng nhãn nhị phân của họ thì không tránh được `[suy luận]`.
2. **Dữ liệu huấn luyện của họ chồng lên tập test của tôi.** Điểm trong Supp. Data 13 do mô hình học trên 6.801 vị trí mảng sinh ra; `TEST-OUT` của tôi (152 vị trí Zhang) có ~46 vị trí nằm trong 6.801 đó `[tác giả báo cáo]`. Với 46 vị trí này, **điểm của họ là điểm trên mẫu huấn luyện của chính họ**. Phải báo riêng hai nhóm (trùng / không trùng) `[suy luận]`.
3. **Không có cách chia của họ.** Họ chỉ nói "holdout 10% of the experimental data" `[tự kiểm]`, không công bố danh sách. Nên **không thể** dựng một `TEST-IN` mà vừa sạch với mô hình của tôi vừa sạch với mô hình của họ. Hệ quả: phép so A **chỉ nên làm trên `TEST-OUT`** (dữ liệu Zhang, nguồn độc lập với cả hai), không nên làm trên tập mảng `[suy luận]`.
4. **Supp. Data 13 đã bị lọc.** Nó chỉ phủ lysine có surface accessibility > 0,2 theo NetSurfP1.0, và **đã loại** các chuỗi trùng tập huấn luyện `[tự kiểm]`. Nên có thể **thiếu** một phần trong 152 vị trí Zhang. Phải đếm phần phủ trước khi so; nếu phủ thấp, phép so A mất giá trị. **Đây là phép đếm phải làm trước tiên** `[suy luận]`.
5. **Ngưỡng của họ được chọn trên holdout rồi báo cáo trên cùng holdout** (m-threshold analysis dùng holdout set `[tự kiểm]`), nên con số "41,2% precision trên testing set" của họ **đã lạc quan**. Không được dùng nó làm mốc `[suy luận]`.
6. **Một điểm nhầm trong báo cáo nội bộ:** câu "không cần chạy lại mô hình của họ" `[tác giả báo cáo]` chỉ đúng cho phép so A. Vì họ **không báo MCC/AUPRC ở đâu cả** `[tự kiểm]`, và vì tiêu chí 2 của GVHD đòi so trên cùng cách chia, **việc chạy lại (phép so C) là bắt buộc, không phải tuỳ chọn**. Việc 2 trong §6 của báo cáo nội bộ ("chạy lại baseline của bài 2025") nói đúng điều này, nhưng §2.2 lại nói ngược — hai mục tự mâu thuẫn `[suy luận]`.

### Gaps

- Chưa đếm được **bao nhiêu trong 152 vị trí Zhang có mặt trong Supplementary Data 13**. Nếu con số này nhỏ, toàn bộ phép so A thu hẹp lại rất nhiều `[chưa kiểm — phép đếm quan trọng nhất của tuần 1]`.
- Chưa biết Supp. Data 13 có kèm **ngưỡng nhị phân của họ** cho từng isoform hay chỉ có điểm `[chưa kiểm]`.
- Chưa mở repo của họ nên chưa biết phép so C có khả thi về mặt mã nguồn hay không `[chưa kiểm]`.

---

## 7. Những phát biểu trong báo cáo nội bộ nên sửa, và sửa thành gì

### Takeaway

Chín phát biểu. Hai cái sai về bản chất (nhãn metric, và "precision đo được / MCC không đo được"), ba cái sai về dữ kiện (OE/KD, 149 vs 152, cột nhãn), ba cái overclaim về phương pháp, một cái tự mâu thuẫn.

### Bảng sửa

| # | Phát biểu hiện tại `[tác giả báo cáo]` | Vấn đề | Thay bằng |
|---|---|---|---|
| **1** | "Mô hình của bài 2025 dự đoán dương 64/149, **đúng mức precision 43,0%** họ báo" (§2.2) | Phép tính đúng, **tên đại lượng sai**. 64/149 là recall/hit rate, không phải precision `[tự kiểm]` | "Ridgeway 2025 báo `64/149 = 43,0%` và **gọi đó là precision**; nhưng vì cả 149 vị trí đều là dương đã biết, đại lượng này thực chất là **recall (hit rate) ở ngưỡng quyết định của họ**. Chính bài, ở phần SET8, định nghĩa precision = TP/(TP+FP), nên cách dùng chữ trong phần SIRT không nhất quán nội bộ" |
| **2** | "Với 149 vị trí dương, **đo được precision** (so trực tiếp 43,0%) nhưng **chưa đo được MCC/AUPRC**" (§2.2) | **Ngược hoàn toàn.** Precision là thứ *không* đo được (không có FP); recall là thứ đo được. Và MCC/AUPRC **trở thành đo được** nếu dùng 2.694 vị trí "định lượng mà không đổi" của Zhang làm nhãn âm `[suy luận, dựa trên 2.846 và 152 `[tự kiểm]`]` | "Trên tập chỉ-có-dương, đo được: recall ở ngưỡng, recall ở ngân sách khớp, enrichment so với background matched, metric xếp hạng kiểu BEDROC. **Không** đo được: precision, MCC, AUROC, AUPRC — vì cả bốn đều cần đếm FP hoặc TN. Nhưng Zhang 2022 định lượng **2.846** vị trí trong khi chỉ **152** đạt tiêu chí phụ thuộc SIRT2, nên **2.694** vị trí còn lại là nhãn âm-trong-tế-bào dùng được; khi đó AUPRC và MCC đo được, với tỉ lệ dương nền ≈ 5,3%" |
| **3** | "149 vị trí … đo bằng khối phổ với SIRT2 quá biểu hiện (OE) và knockdown (KD)" (§2.2) | Ridgeway mô tả bối cảnh là **WT vs H187Y bất hoạt xúc tác** `[tự kiểm]`; Zhang mô tả **KD và OE** `[tự kiểm]`. Báo cáo gộp hai mô tả | "Tập 149 vị trí **không phải thí nghiệm của Ridgeway**; Methods của họ nói rõ lấy từ **Zhang et al. 2022** ([PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)). Thiết kế của Zhang là knockdown + overexpression trong HCT116; Ridgeway lại mô tả WT vs H187Y. **Sự khác biệt này phải làm rõ trước khi dùng tập** vì nó quyết định nhãn âm được định nghĩa thế nào" |
| **4** | "**149** vị trí" (§2.2) | Zhang báo **152** vị trí (134 peptide) giao hai tiêu chí, Fig. S4a `[tự kiểm]` | "Zhang 2022 báo 134 peptide / **152 vị trí**; Ridgeway dùng **149**. Chênh 3 chưa giải thích được — phải đối chiếu Supp. Data 14 của Ridgeway với Table S1/S4 của Zhang" |
| **5** | "Nhãn nhị phân mà bài 2025 dùng (**`category ≥ 1`**)" và bảng số dương 176/1.901/… (§2.1) | Ridgeway Methods viết là “**signal ratio score of 1 or greater**” `[tự kiểm]`, không phải cột `substrate category` | "Ridgeway phát biểu ngưỡng trên **`signal ratio` ≥ 1**. Báo cáo này đếm theo cột `substrate category`. **Hai cột khác nhau**, nên bảng số dương theo isoform phải được xác nhận lại bằng cách đối chiếu `All_Sirts_Feature_Y_labels.csv` với `Supplementary Data 1` của Rauh trước khi dùng làm số liệu đề cương" |
| **6** | "RQ2 … So với **43,0%** của bài 2025 trên **đúng 149 vị trí đó**" (§4.2) | So recall ở hai ngưỡng khác nhau là **không hợp lệ**: hạ ngưỡng là tăng được recall. Và 46/149 là mẫu huấn luyện của chính họ `[tác giả báo cáo]` | "RQ2 so **recall ở ngân sách gọi-dương khớp nhau** (cả hai mô hình gọi dương cùng tỉ lệ trên cùng tập nền), cộng enrichment so với 2.694 vị trí âm-trong-tế-bào, cộng AUPRC/MCC nếu nhãn âm dựng được. Báo riêng cho nhóm vị trí **trùng** và **không trùng** tập mảng" |
| **7** | "`Supplementary Data 13` … có sẵn dự đoán để so trực tiếp từng vị trí, **không cần chạy lại mô hình của họ**" (§2.2) | Mâu thuẫn với chính §6 việc 2 của cùng tài liệu; và Ridgeway **không báo MCC/AUPRC ở đâu cả** `[tự kiểm]`, nên không có mốc để so | "Supp. Data 13 cho phép **một** phép so: so **xếp hạng** điểm số trên tập Zhang. Nó **không** thay được việc chạy lại mô hình của họ trên cách chia của mình, vì (a) họ không báo MCC/AUPRC, (b) cách chia của họ không công khai, (c) ngưỡng của họ chọn trên holdout rồi báo trên cùng holdout. Cả hai phép so đều phải làm và trình bày tách biệt" |
| **8** | Cổng dừng tuần 4: "ESM-2 + mCNN đa nhãn **≥ baseline** … (MCC) cho **≥ 4/7 isoform**" (§4.3) | "≥" không có CI thì với SIRT1 (176 dương) là may rủi; và so đa nhãn với baseline 7-mô-hình-rời đổi nhiều biến cùng lúc | "Cổng: MCC của bậc B8 cao hơn bậc B4 **ngoài khoảng tin cậy bootstrap 95% theo cụm protein** cho ≥ 4/7 isoform, trên cùng `TEST-IN` và ngưỡng chọn trên `CALIB`. SIRT1 báo riêng, không tính vào cổng" |
| **9** | Bậc thang RQ1: "(3) đặc trưng làm tay + LDA/cây → (4) **ESM-2 đóng băng + mCNN**" (§4.2) | Bước này đổi **ba** thứ cùng lúc (biểu diễn, kiến trúc, số đầu ra) nên không gán được nguyên nhân | Dùng bậc thang 15 bậc ở §5 của tài liệu này, trong đó mỗi bậc đổi **đúng một** thứ; thêm **B0** (dummy) và **B3** (MusiteDeep một mình), và thêm hai ablation đánh giá **L1** (rò rỉ) và **L2** (memorization) |

### Hai phát biểu nên **giữ**, vì kiểm lại thấy đứng vững

- "Tập test độc lập nguồn **tồn tại và tải được**, nhưng thiếu nhãn âm" (§2.2) — đúng về tồn tại và về nguồn độc lập (Zhang 2022, không phải thí nghiệm của Ridgeway `[tự kiểm]`). Phần "thiếu nhãn âm" chỉ đúng với Supp. Data 14 của Ridgeway, **không** đúng với dữ liệu gốc của Zhang.
- "Nhãn âm định nghĩa được một cách sạch: vị trí được định lượng trong cùng thí nghiệm KO/KD nhưng không đổi là âm trong tế bào" (§2.3) — đúng, và **Zhang 2022 chính là trường hợp đó**, với 2.846 vị trí định lượng `[tự kiểm]`. Báo cáo nội bộ đặt ý này ở mục "nguồn có, chưa xác nhận file" và đi tìm bộ PRIDE khác, trong khi **nguồn cần tìm nằm ngay trong bài đã dùng** `[suy luận]`. Đây là phát hiện có giá trị thực hành cao nhất của tài liệu này.

### Cảnh báo về chất lượng nhãn "vàng" của `TEST-OUT`

Nhãn dương của Zhang được gọi bằng **ngưỡng > 1,5 lần** và điều kiện **ngược chiều giữa KD và OE**, và **không có p-value hay FDR cho bước gọi vị trí** (chỉ có FDR < 1% cho bước identification) `[tự kiểm qua toàn văn PMC8907344]`. Hệ quả cho đề cương:

- Tập 152 vị trí là **kết quả của một ngưỡng**, không phải chân lý. Phải báo độ nhạy của mọi kết luận theo ngưỡng đó (ví dụ chạy lại với > 1,3 và > 2,0 lần nếu Table S1 có fold-change).
- Vì không có kiểm định thống kê ở bước gọi vị trí, **một phần của 152 là dương giả**, nên recall thật của bất kỳ mô hình nào đều bị chặn trên dưới 100%. Phải nói điều này trước khi báo con số, không phải sau.
- Đây cũng là một câu hỏi tốt cho GVHD, bổ sung vào năm câu trong báo cáo nội bộ: *"Thầy có coi tập 152 vị trí gọi bằng ngưỡng fold-change 1,5 mà không có FDR là nhãn vàng đủ tiêu chuẩn cho một tập test, hay em phải dựng lại từ dữ liệu thô?"* `[suy luận]`

### Gaps

- Chưa mở được Supplementary Table S1 của Zhang 2022 để xác nhận có fold-change theo từng vị trí → **cổng dữ liệu tuần 1 vẫn mở**, nhưng nay nó là một việc rất cụ thể (một file, một bài, một bảng) thay vì "đi tìm bộ PRIDE nào đó".
- Chưa đọc Supplementary Materials S1 và S3 của Ridgeway 2025 → chưa biết chính xác ngưỡng áp cho tập 149, và chưa kiểm được con số 41,2%.
- Chưa tra lại DOI của MMseqs2, CD-HIT, Zhang & Zhou 2014, Wu & Zhou 2017, Sechidis 2011; chưa đọc toàn văn Rost 1999, Truchon & Bayly 2007, Saito & Rehmsmeier 2015, Chicco & Jurman 2020, Jain 2017 (chỉ đọc tóm tắt và thông tin xuất bản).
- Không kiểm chứng được bất kỳ con số nào trong `[tác giả báo cáo]` thuộc báo cáo nội bộ (176 dương, 46/149, 108/149, 145.461 × 7) vì không mở file dữ liệu trong phiên này; mọi suy luận dựa trên chúng kế thừa độ bất định đó.
