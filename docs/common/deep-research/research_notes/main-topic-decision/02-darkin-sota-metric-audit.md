# Audit SOTA và trục đo trên benchmark DARKIN (zero-shot kinase–phosphosite link prediction)

> Ngày audit: 10/10/2026. Quy ước nhãn: **[SOURCE]** = tác giả tự báo cáo, có dẫn nguồn · **[ANALYSIS]** = suy luận của tôi · **[UNVERIFIED]** = không truy cập được.
>
> **Kết luận một dòng, đặt lên đầu vì đây là output hữu ích nhất:** **0,2946 của COMPASS-PTM và 0,1911 của DARKIN gần như chắc chắn KHÔNG đo trên cùng một trục.** 0,1911 là `macro AP` trung bình **theo kinase** (xếp hạng phosphosite cho một kinase cho trước); COMPASS-PTM tự định nghĩa mAP là "rank true kinases for each substrate", tức trục **phosphosite** — chính là chỉ số DARKIN gọi là `Phosphosite AP`. Trên trục phosphosite, baseline BZSM của chính DARKIN đã đạt ~0,288 và bản fine-tune (DARKIN-FT) đạt 0,3321 — **cao hơn 0,2946**. Nghĩa là con số "+54%" của COMPASS-PTM chưa được xác nhận là một cải tiến thật trên cùng trục; nhưng **cũng chưa được xác nhận là sai**, vì Supplementary S.3.7 (nơi chứa định nghĩa chi tiết) không truy cập được.

## (a) Mỗi con số được báo cáo trên trục AP nào?

### Takeaway

Hai trục tồn tại thật và có tên riêng trong hệ sinh thái DARKIN: `macro AP` (trục kinase, **chỉ số chính**) và `Phosphosite AP` (trục site, chỉ số phụ). DARKIN và luận văn Pekey báo cáo cả hai; COMPASS-PTM chỉ báo cáo một số duy nhất, và cách diễn giải bằng lời của nó khớp với **trục site**.

### Cited Findings

- [SOURCE] DARKIN (bioRxiv preprint của bài Bioinformatics btaf480): "We evaluate our methods using the macro Average Precision (AP) score" và "we calculate the AP score for each kinase and then take the mean across all kinase classes, hence calculating the macro AP" — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] DARKIN dùng đồng thời các chỉ số: `macro AP` (chính), `Family AP`, `Group AP`, `Phosphosite AP`, `hit@k accuracy`, `Masked Group AP` — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] DARKIN mô tả `Phosphosite AP` rất ngắn: "Phosphosite AP, which evaluates precision for phosphosite-specific predictions". Giá trị số của nó nằm ở Table 4, không trích xuất được từ bản full-text HTML — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] Luận văn Pekey định nghĩa rõ ràng hai trục, nguyên văn:
  - `Macro-AP`: "Macro-AP is the principal metric. For each kinase class, we rank all test phosphosites, compute the Average Precision (AP) for that class, and then take the unweighted mean across classes."
  - `Phosphosite AP`: "Phosphosite AP is computed analogously to Macro-AP but in the opposite direction: for each phosphosite, we rank all candidate kinases, compute the AP, and average the resulting APs. This metric captures how accurately the model ranks kinases for a given phosphosite, aligning closely with the retrieval experience of an end user."
  — [Pekey MSc thesis, Sabanci University 2025](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf) (tr. 22, mục 3.4 Evaluation Metrics)
- [SOURCE] Pekey nêu lý do **không** lấy trục site làm chỉ số chính: "we do not report Phosphosite AP as the primary evaluation metric because the kinase label space in the test set is relatively small. In such settings, site-level AP can be disproportionately affected by the number of true labels per phosphosite or the frequency of certain kinases, which can lead to misleading impressions of model performance." — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] Mã nguồn DARKIN xác nhận hai trục cùng tồn tại trong một hàm. Trong `bilinear_zero_shot_model/scripts/evaluation/metrics.py`, hàm `calculate_aupr` tính cả:
  - `class_aupr = average_precision_score(self.labels[:, kin_class_idx], scores_to_use[:, kin_class_idx])` → gộp thành biến `macro_aupr` (trục **cột = kinase**)
  - `row_aupr = average_precision_score(self.labels[row_idx, :], scores_to_use[row_idx, :])` → gộp thành biến `macro_row_aupr` (trục **hàng = phosphosite**)
  Các hàm khác (`calculate_aupr_per_class`, `calculate_aupr_per_kinase_class_and_group`, `calculate_group_masked_ap`, `_calculate_property_ap`) đều chỉ dùng trục cột. Không có biến nào tên `phosphosite` trong file. — [metrics.py trên tastanlab/darkin](https://raw.githubusercontent.com/tastanlab/darkin/main/bilinear_zero_shot_model/scripts/evaluation/metrics.py)
- [SOURCE] COMPASS-PTM định nghĩa mAP bằng một câu duy nhất: "the mean Average Precision (mAP), which assesses the ability to correctly rank true kinases for each substrate" — [COMPASS-PTM, PMC13377107](https://pmc.ncbi.nlm.nih.gov/articles/PMC13377107/)
- [SOURCE] COMPASS-PTM báo cáo: "Following the benchmark's protocol, our model achieves an mAP of 0.2946" và "This result substantially outperforms the highest reported score from the original study (0.1911) by 54%", kèm ghi chú "this score was obtained using an ESM2-150M backbone". Bài **không nêu tên phương pháp** đã đạt 0,1911. — [COMPASS-PTM, PMC13377107](https://pmc.ncbi.nlm.nih.gov/articles/PMC13377107/)
- [SOURCE] COMPASS-PTM **không in công thức mAP** trong thân bài; nó trỏ sang Supplementary Information S.3.7 cho chi tiết protocol và tập kinase ứng viên — [COMPASS-PTM, PMC13377107](https://pmc.ncbi.nlm.nih.gov/articles/PMC13377107/); xác nhận lại trên bản arXiv HTML: mục 2.2.4 "Zero-shot Generalization to Unseen Kinases" chỉ tóm tắt rồi trỏ sang supplement — [arXiv 2510.23492 HTML](https://arxiv.org/html/2510.23492v1)
- [SOURCE] 0,1911 trong DARKIN là `macro AP` của **ESM1b fine-tune**, cụ thể "achieved by reinitializing the final two layers of both the phosphosite and kinase encoders using the full set of kinase features"; bài gọi đây là "marginal improvement" so với cấu hình khác và "at a notable computational cost". Không fine-tune, BZSM tốt nhất chỉ hơn 0,16 (ESM1B và ESM1v, CLS token). — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] Mốc random guessing của `macro AP` trên DARKIN là **~0,03** (trung bình 1000 lần xếp hạng ngẫu nhiên); DARKIN tự nhận 0,1911 "can be considered low overall" — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)

### Inferences

- [ANALYSIS] Chuỗi suy luận về trục của COMPASS-PTM: DARKIN gọi trục site là `Phosphosite AP` và định nghĩa nó là "for each phosphosite, we rank all candidate kinases"; COMPASS-PTM định nghĩa mAP là "correctly rank true kinases for each substrate". Hai câu này mô tả **cùng một phép toán**. Vậy mAP của COMPASS-PTM khớp với `Phosphosite AP` / `macro_row_aupr`, **không** khớp với `macro AP` của 0,1911.
- [ANALYSIS] Hệ quả định lượng: đặt cạnh 0,2946 thì `Phosphosite AP` của chính baseline DARKIN (bản Pekey tái dựng, ESM1B BZSM) = **0,2879**, và DARKIN-FT = **0,3321** (xem mục (c)). Nếu COMPASS-PTM đo trục site thật thì 0,2946 chỉ **nhích hơn baseline không fine-tune ~0,007** và **thấp hơn SOTA trục site ~0,038**. "+54%" sẽ biến mất hoàn toàn.
- [ANALYSIS] Có một cách đọc khác, không loại trừ được: chữ "mAP" có thể là tên thương mại của `macro AP` còn câu giải thích chỉ viết lỏng tay theo hướng "use case người dùng" (DARKIN cũng diễn giải bài toán là "assign phosphosites to dark kinases"). Nếu vậy 0,2946 là đúng trục và là SOTA thật, vượt 0,1911 một cách hợp lệ. **Không có bằng chứng nào trong tay phân định được hai cách đọc này**, vì công thức nằm ở S.3.7.
- [ANALYSIS] Việc COMPASS-PTM đạt điểm cao nhất bằng backbone **ESM2-150M**, trong khi DARKIN cho thấy ESM2-150M là backbone *yếu nhất* trong 4 pLM (BZSM macro AP 0,1325 — thấp nhất bảng), làm tăng thêm nghi vấn về tính so sánh được: hoặc kiến trúc COMPASS-PTM thật sự bù được khoảng cách backbone, hoặc chỉ số đang đo thứ khác.

### Gaps

- [UNVERIFIED] **Supplementary Information S.3.7 của COMPASS-PTM không truy cập được.** nature.com chuyển hướng qua `idp.nature.com` (paywall/SSO); bản arXiv PDF vượt giới hạn 10 MB của WebFetch; bản arXiv HTML và PMC đều bị cắt trước phần supplement. Đây là tài liệu duy nhất có thể chốt dứt điểm câu hỏi trục. **Người làm đề tài nên tải PDF arXiv 2510.23492 (47 trang) bằng tay và đọc S.3.7** — đó là việc 15 phút và giải quyết toàn bộ nghi vấn.
- [UNVERIFIED] Giá trị `Phosphosite AP` **do chính bài DARKIN báo cáo** (Table 4) chưa lấy được. Tôi chỉ có số của bản tái dựng trong luận văn Pekey (cùng nhóm, cùng Split 1).

## (b) Có cùng split, seed và tập kinase ứng viên không?

### Takeaway

DARKIN và Pekey đều dùng **Split 1, 3 seed, lấy trung bình** — hoàn toàn so sánh được với nhau. COMPASS-PTM chỉ nói "following the benchmark's protocol" mà **không nêu split nào, seed nào, hay tập kinase ứng viên nào**; tất cả bị đẩy sang S.3.7. Vì vậy tính so sánh được của 0,2946 **không xác nhận được ở cả ba chiều này**, không chỉ ở chiều trục đo.

### Cited Findings

- [SOURCE] DARKIN có **4 split**, sinh ra bằng cách đổi random seed; thí nghiệm mặc định dùng **Split 1**; mỗi cấu hình BZSM được train **3 lần**, báo cáo mean và std; tỉ lệ train/val/test = **80/10/10** trên các cặp kinase–phosphosite — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] Sau tiền xử lý, DARKIN có **392 kinase**, **11 kinase group**, **129 kinase family** — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)
- [SOURCE] Pekey: "Each model was run with three different random seeds, and the average results were reported. All results are based on the DARKIN Split 1 unless otherwise noted." — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] Kích thước Split 1 (Pekey): **8.560 train / 1.485 validation / 1.415 test** mẫu (cặp kinase–phosphosite) — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] Ba ràng buộc sinh split của DARKIN (Pekey trình bày lại rõ hơn bài báo):
  1. *Minimum support*: mọi kinase ở val/test phải có **≥ 10 phosphosite** được chú giải, để AP per-class đáng tin;
  2. *Stratified groups*: phân bố 11 kinase group được giữ nguyên qua train/val/test;
  3. *Sequence identity exclusivity*: các kinase có **≥ 90% identity** trong kinase domain bị đưa vào **cùng một split**, "prevents knowledge leakage through highly similar sequences and avoids inflating performance via trivial transfer".
  — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] **Chiều held-out bị hiểu ngược trong nhiều bản mô tả thứ cấp.** Pekey nói rõ: "In the DARKIN dataset, kinases with abundant phosphosite annotations are assigned to the validation and test splits, while understudied 'dark' kinases are reserved for the training split... Kinases with fewer than ten associated phosphosites are always placed in the training set, whereas those with richer annotation are preferentially used in validation and testing." Lý do: cần đủ positive để tính AP trên lớp held-out. — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] COMPASS-PTM về split: "This benchmark is designed to identify 'dark kinases' for a given phosphosite, enforcing strictly disjoint kinase sets between the training and testing splits" — không nêu kích thước split; về seed, chỉ có ghi chú chung cho các hình là "n = 3 independent training runs with different random seeds", **không gắn riêng cho DARKIN**; tập kinase ứng viên: không nêu, trỏ S.3.7 — [COMPASS-PTM, PMC13377107](https://pmc.ncbi.nlm.nih.gov/articles/PMC13377107/)
- [SOURCE] Repo COMPASS-PTM (`ZhangJJ26/COMPASS-PTM`, default branch `master`, tạo 17/10/2025, cập nhật 12/08/2026, 9 star) có **22 file, 5 thư mục, và KHÔNG có file nào tên liên quan tới evaluation, metrics, DARKIN hay downstream task**. Toàn bộ cây: `README.md`, `environment.yaml`, `COMPASS_PTM_main.jpg`, `data/{aa2selfies_embeddings.pt, kinase_embeddings_150m.npz, kinases_dict.json, matrix.pt, stage1_mini/train_data.csv, stage2_mini/train_data.csv}`, `models/{config_pep.py, dataset.py, inference.ipynb, loss.py, model.py, train.py, ptm_probabilities.csv, preprocess/preprocess_kinase.py, preprocess/preprocess_matrix.py}`. Listing không bị truncate. — [GitHub API tree](https://api.github.com/repos/ZhangJJ26/COMPASS-PTM/git/trees/HEAD?recursive=1), [GitHub API repo](https://api.github.com/repos/ZhangJJ26/COMPASS-PTM)

### Inferences

- [ANALYSIS] **Không thể kiểm chứng 0,2946 từ mã nguồn.** Repo chỉ có `train.py` + `inference.ipynb` + dữ liệu "mini" (`stage1_mini`, `stage2_mini`), không có script DARKIN, không có hàm AP, không có kết quả. Đây là điểm yếu tái lập quan trọng và nên nói thẳng với GVHD: con số DARKIN của COMPASS-PTM hiện là **author-reported, không reproducible từ repo**.
- [ANALYSIS] Về **label leakage**: COMPASS-PTM là framework PTM đa nhiệm được huấn luyện trước trên dữ liệu PTM/enzyme–substrate; bản arXiv HTML cho biết data availability liệt kê "the PTM and enzyme-substrate datasets" nhưng đó là dữ liệu **fine-tuning**, không phải pretraining corpus, và corpus pretraining **không được mô tả**. Nếu bất kỳ nguồn nào trong đó chứa cặp kinase–site của các kinase thuộc test split DARKIN (PhosphoSitePlus là nguồn gốc của DARKIN, nên rủi ro này không nhỏ), thì "zero-shot" bị phá vỡ ở mức corpus. **Tôi không xác nhận được có leakage; tôi xác nhận được rằng bài không cung cấp đủ thông tin để loại trừ nó.**
- [ANALYSIS] Một rủi ro leakage **nội tại của chính DARKIN**, ít ai nói tới, và nó đánh đúng vào trục site: Pekey ghi "unlike the zero-shot design in DARKIN, which ensures kinase classes are split across training and test sets, **the same phosphosite sequences can appear in both training and testing sets** due to the dataset's multilabel nature" ([Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)). Zero-shot ở đây là zero-shot **theo kinase**, không phải theo phosphosite. Pekey phải tự loại các sequence trùng khi huấn luyện ProGen2 vì lý do này.

### Gaps

- [UNVERIFIED] Số **kinase test** cụ thể của Split 1 (tức kích thước label space / tập ứng viên) không lấy được: bài DARKIN đặt con số này trong Figure 2, Pekey chỉ cho số **mẫu** (1.415 test) chứ không cho số **lớp**. Đây là tham số then chốt: `Phosphosite AP` phụ thuộc mạnh vào kích thước tập ứng viên, nên nếu COMPASS-PTM dùng tập ứng viên khác (ví dụ toàn bộ 392 kinase thay vì chỉ kinase test) thì con số càng không so sánh được.
- [UNVERIFIED] Corpus pretraining của COMPASS-PTM (danh sách database cụ thể) — nằm trong supplementary không truy cập được.
- [UNVERIFIED] COMPASS-PTM dùng Split 1 hay tự chia lại — không xác định được.

## (c) SOTA thật theo từng protocol, và luận văn Pekey báo cáo gì

### Takeaway

Theo **trục kinase (macro AP, chỉ số chính)**, SOTA công khai xác nhận được là **0,2386** (DARKIN-FT + ESM1B, few-shot 5-shot) và **0,2250** (DARKIN-FT + ESM1B, strict zero-shot), đều từ luận văn Pekey — không phải 0,1911 của bài DARKIN. Theo **trục site (Phosphosite AP)**, SOTA xác nhận được là **0,3321** (DARKIN-FT + ESM1B zero-shot), cao hơn 0,2946 của COMPASS-PTM.

### Cited Findings — bảng zero-shot của Pekey (Table 4.1, Split 1, 3 seed)

Tất cả từ [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), Table 4.1. `BZSM` = bilinear zero-shot model, tức chính baseline của DARKIN.

| Model | Method | Macro AP (trục kinase) | Top-1 | Top-3 | Top-5 | Phosphosite AP (trục site) |
|---|---|---|---|---|---|---|
| ESM1B | BZSM (DARKIN baseline) | 0,1746 | 0,1320 | 0,3314 | 0,4698 | **0,2879** |
| ESM1B | **DARKIN-FT** | **0,2250** | 0,1751 | 0,3977 | 0,5228 | **0,3321** |
| ESM1B | DARKIN-FT–PT | 0,1822 | 0,1648 | 0,3819 | 0,5177 | 0,3191 |
| ProtT5XL | BZSM | 0,1673 | 0,1339 | 0,2953 | 0,4394 | 0,2790 |
| ProtT5XL | DARKIN-FT | 0,1710 | 0,1376 | 0,2720 | 0,3936 | 0,2631 |
| ESM2-650M | BZSM | 0,1659 | 0,1280 | 0,3128 | 0,4429 | 0,2744 |
| ESM2-650M | DARKIN-FT | 0,1966 | 0,1673 | 0,3717 | 0,4868 | 0,3113 |
| ESM2-150M | BZSM | 0,1325 | 0,1058 | 0,3177 | 0,4448 | 0,2629 |
| ESM2-150M | DARKIN-FT | 0,1862 | 0,1416 | 0,3465 | 0,4835 | 0,2915 |

### Cited Findings — few-shot (5-shot), Table 4.2

- [SOURCE] ESM1B + DARKIN-FT: Macro AP **0,2386**, Phosphosite AP **0,3465** (cao nhất toàn luận văn). ESM1B + BFSM (baseline few-shot): 0,1894 / 0,2965. ESM2-650M + DARKIN-FT: 0,2272 / 0,3330. — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), Table 4.2
- [ANALYSIS] **Few-shot KHÔNG phải strict zero-shot** — mô hình được thấy 5 site của mỗi kinase test. Không được đem 0,2386 so với 0,1911 hay 0,2946.

### Cited Findings — các cấu hình còn lại của Pekey

- [SOURCE] **DARKIN-Interact** (biến thể binary classification, phosphosite–kinase interact): zero-shot Macro AP **0,2078**, Phosphosite AP 0,3109 — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), Table 4.16 (dòng không augmentation)
- [SOURCE] **LoRA**: dùng để fine-tune các pLM encoder cho cả DARKIN-FT và DARKIN-Interact; luận văn có loạt bảng so sánh "fine-tuning N encoder layers versus LoRA on DARKIN-Interact" (Table 4.5–4.6 và phụ lục A). Đây là biến thể huấn luyện, **vẫn strict zero-shot** — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), mục lục bảng
- [SOURCE] **Ba chiến lược data augmentation** và kết quả: (i) sinh phosphosite có điều kiện kinase bằng ProGen2 fine-tune (ProGen2–Phospho) → **giảm** hiệu năng; (ii) weak supervision bằng dự đoán của **Kinase Substrate Specificity Atlas (KSSA, Johnson et al. 2023)** → **giảm** hiệu năng; (iii) **homologous sequences** (sinh biến thể từ multiple sequence alignment) → **cải thiện Macro AP cho DARKIN-Interact** — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), abstract + mục 4.5
- [SOURCE] Chi tiết Table 4.16 (augmentation bằng homologous sequence, chỉ thêm vào **train**):
  - DARKIN-FT: 0,2250 → **0,2060** Macro AP; Phosphosite AP 0,3321 → **0,2687** (xấu đi)
  - DARKIN-Interact: 0,2078 → **0,2131** Macro AP (tốt hơn); Phosphosite AP 0,3109 → **0,2901** (xấu đi)
  Pekey tự nhận xét: "kinase-level performance metrics improved, we observed a drop in phosphosite-level accuracy and AP scores, suggesting that the model became better at distinguishing among kinase classes but struggled more in retrieving the correct kinase for a given phosphosite" — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] So sánh với **KSSA làm predictor trực tiếp** trên subset đã lọc (Table 4.14, **không so sánh được với bảng chính** vì chạy trên DARKIN-KL-ST / DARKIN-KL-Y đã lọc):
  - S/T: DARKIN-FT 0,2240 Macro AP / 0,3101 Phosphosite AP; DARKIN-Interact 0,2073 / 0,3097; **KSSA 0,1600 / 0,3870**
  - Y: DARKIN-FT 0,3810 / 0,4915; DARKIN-Interact 0,3389 / 0,4259; **KSSA 0,1259 / 0,6338**
  — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf), Table 4.14
- [SOURCE] Spectral Norm regularization "slightly outperformed the baseline in both Macro AP" — một cải tiến nhỏ, rẻ — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] Kết luận của Pekey về giới hạn: "all models still struggle to distinguish between kinases from the same family or group since their sequences are often very similar. This suggests that sequence data alone might not be enough to solve this problem completely." — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)

### Inferences — cấu hình nào strict zero-shot, cấu hình nào dùng side information

- [ANALYSIS] **Strict zero-shot** (không dùng thông tin ngoài về kinase test, ngoài sequence + family/group/EC mà DARKIN đã cho phép): BZSM, DARKIN-FT, DARKIN-FT–PT, DARKIN-Interact, các biến thể LoRA và regularization. Lưu ý: **mọi** cấu hình trong luận văn đều dùng kinase family/group/EC trong biểu diễn kinase ("these attributes are included in the kinase representations for all models in this study") — DARKIN gốc cũng vậy, nên đây là phần của protocol, không phải side information thêm.
- [ANALYSIS] **Dùng side information về kinase test, không còn là zero-shot thuần**: (1) **KSSA / atlas motif** — KSSA là dữ liệu thực nghiệm đo *đặc hiệu cơ chất* của chính các kinase đó, tức là đúng thứ thông tin mà zero-shot lẽ ra phải suy ra; dùng nó vừa làm weak label vừa làm predictor đều là rò rỉ thông tin về lớp held-out. (2) **Homologous-sequence augmentation** — trường hợp này nhẹ hơn và **có thể bảo toàn zero-shot**: augmentation chỉ thêm vào tập train (cột "Kinase Set = Train" trong Table 4.16), nên không chạm vào kinase test. [ANALYSIS] Tôi đánh giá (2) là hợp lệ, (1) là không hợp lệ nếu muốn so với 0,1911.
- [ANALYSIS] **Fine-grained cluster (F.grain) và clustered evaluation**: Pekey thêm một lớp phân cụm kinase dẫn từ cây phả hệ KinBase (2024) rồi báo cáo thêm bộ bảng "evaluated with clustered..." ở phụ lục. Đây là **trục đo thứ ba** (AP ở mức thuộc tính kinase, không phải mức kinase riêng lẻ), dễ hơn trục kinase. Khi đọc bất kỳ con số DARKIN nào, phải xác định nó thuộc một trong **bốn** họ chỉ số: macro AP (kinase), Phosphosite AP (site), Family/Group/F.grain AP (thuộc tính), Masked Group AP.

### Gaps

- [UNVERIFIED] Giá trị tuyệt đối của các bảng LoRA (Table 4.5–4.6) chưa trích ra; chỉ xác nhận được sự tồn tại và vai trò của chúng.
- [UNVERIFIED] Luận văn Pekey (2025) có được công bố thành bài báo peer-reviewed chưa — chưa kiểm. Nếu chưa, thì "SOTA trục kinase = 0,2250/0,2386" là **SOTA chỉ tồn tại trong một luận văn thạc sĩ của chính nhóm tác giả benchmark**, chưa qua phản biện.

## (d) Còn công trình 2025–2026 nào khác trên DARKIN? Và sinh viên thực tế phải vượt cái gì?

### Takeaway

Hai nghi vấn mà khảo sát trước nêu đều **giải quyết xong và đều là âm tính**: bioRxiv 2025.03.12.642740 **không** đánh giá trên DARKIN; "Improving DeepKinZero with PLMs and transductive learning" **không phải đối thủ** mà chính là luận văn tiền thân đã sinh ra benchmark DARKIN. Ngoài DARKIN, COMPASS-PTM và Pekey, tôi không tìm thấy công trình thứ tư nào báo cáo số trên DARKIN.

### Cited Findings

- [SOURCE] bioRxiv 2025.03.12.642740 có tiêu đề thật là **"Predicting Kinase-Substrate Phosphorylation Site Using Autoregressive Transformer"** (Pourmirzaei, Esmaili, Pourmirzaei, Rezaei, Dong Xu; đăng 14/03/2025). Nó làm 3 task (site prediction là chính, cộng kinase group classification và substrate–kinase interaction prediction làm phụ) và **không nhắc tới DARKIN, không báo cáo AP/mAP trên DARKIN** — [bioRxiv 2025.03.12.642740](https://www.biorxiv.org/content/10.1101/2025.03.12.642740v1)
- [SOURCE] "Improving DeepKinZero with Protein Language Models and Transductive Learning" là **luận văn 2024 của Emine Ayşe Sunar (Sabanci University)** — chính là tác giả đầu của bài DARKIN. Ba đóng góp của nó: (1) tạo ra setup đánh giá DARKIN với các split tính tới điều kiện zero-shot, kinase group và sequence similarity; (2) đánh giá nhiều pLM với 2 zero-shot model (k-NN và bilinear); (3) dùng kinase active site cho kết quả tương đương kinase domain. — [Sabanci repository, eprint 51540](https://research.sabanciuniv.edu/id/eprint/51540/)
- [SOURCE] Pekey tự định vị công trình của mình là mở rộng của DeepKinZero (Deznabi et al. 2020) và DARKIN (Sunar et al. 2024) — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] DARKIN bản OpenReview có tiêu đề khác ("DARKIN: A zero-shot classification benchmark and an evaluation of protein language models") — cùng công trình, khác bản — [OpenReview a4x5tbYRYV](https://openreview.net/forum?id=a4x5tbYRYV)
- [SOURCE] Dữ liệu và script sinh split của DARKIN công khai tại [tastanlab/darkin](https://github.com/tastanlab/darkin); bản Bioinformatics là [btaf480](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017), PubMed [41160492](https://pubmed.ncbi.nlm.nih.gov/41160492/), bản preprint mở tại [bioRxiv 2025.08.27.672558](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1).
- [SOURCE] Về chi phí huấn luyện phía Pekey: DARKIN-FT train **100 epoch**, DARKIN-Interact **50 epoch**, ProGen2–Phospho **5000 step** (bản cuối giảm còn 2000 step vì hiệu năng suy giảm sau đó); chọn checkpoint theo validation tốt nhất; sau khi chọn hyperparameter thì gộp train+val và train lại cùng số epoch — [Pekey thesis](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf)
- [SOURCE] COMPASS-PTM: repo **không nêu checkpoint/weights**; phần code availability chỉ trỏ GitHub cho "custom code" — [arXiv 2510.23492 HTML](https://arxiv.org/html/2510.23492v1); repo size 8.799 KB (~8,6 MB), dữ liệu kèm theo chỉ là `*_mini` — [GitHub API repo](https://api.github.com/repos/ZhangJJ26/COMPASS-PTM)
- [SOURCE] DARKIN tự nhận fine-tune ESM1b (cấu hình cho 0,1911) là "at a notable computational cost" — [DARKIN bioRxiv full text](https://www.biorxiv.org/content/10.1101/2025.08.27.672558v1.full)

### Inferences — tính khả thi với 1 GPU hạng Colab và 8–9 tuần

- [ANALYSIS] **Tái lập baseline DARKIN: khả thi, và đây là việc nên làm đầu tiên.** Lý do: dataset cực nhỏ (Split 1 chỉ 8.560 cặp train / 1.415 test), repo công khai đầy đủ cả split lẫn `metrics.py`, và cấu hình BZSM **đóng băng embedding pLM** — nghĩa là chỉ cần trích embedding một lần (có thể cache) rồi học một ma trận bilinear W, việc này chạy được trên CPU. Phần tốn kém duy nhất là trích embedding ESM1b/ProtT5-XL cho ~11.500 peptide + 392 kinase domain, vài giờ GPU T4 là xong, và chỉ làm một lần.
- [ANALYSIS] **Tái lập DARKIN-FT (0,2250): khả thi nhưng căng.** Fine-tune end-to-end ESM1b (~650M tham số) 100 epoch trên T4 16 GB là biên giới khả thi — cần gradient checkpointing, batch nhỏ, mixed precision. Đường tránh rủi ro: dùng **ESM2-150M** (Pekey đạt 0,1862 zero-shot với nó, vẫn trên 0,1746 của BZSM-ESM1B) hoặc **LoRA** thay vì full fine-tune. Pekey đã chứng minh LoRA là đường khả thi.
- [ANALYSIS] **Tái lập COMPASS-PTM: KHÔNG khả thi trong 8–9 tuần.** Ba lý do cộng dồn: (1) không có checkpoint công bố, nên phải pretrain lại một framework PTM coarse-to-fine đa nhiệm từ đầu; (2) repo không có script DARKIN, không có code metric, nên dù pretrain xong cũng phải tự viết lại toàn bộ phần đánh giá và sẽ không biết mình có khớp protocol của tác giả hay không; (3) chỉ có dữ liệu `*_mini`. [ANALYSIS] Khuyến nghị: **đừng coi 0,2946 là mục tiêu phải vượt.** Coi nó là một con số trong literature mà đề tài sẽ *audit*, không phải *beat*.
- [ANALYSIS] **Sinh viên thực tế phải vượt cái gì**, xếp theo độ chắc chắn:
  1. **Bắt buộc, trục kinase:** `macro AP` 0,1911 (DARKIN, ESM1b fine-tune, Split 1) — đây là số peer-reviewed duy nhất trên trục chính. Mốc random là 0,03.
  2. **Thực tế hơn, trục kinase:** `macro AP` **0,2250** (DARKIN-FT, Pekey, strict zero-shot). Nếu không nhắc tới số này mà chỉ so với 0,1911 thì hội đồng/GVHD có thể bắt lỗi "chọn baseline yếu", vì luận văn Pekey công khai và cùng nhóm.
  3. **Nếu chọn báo cáo trục site:** `Phosphosite AP` **0,3321** (DARKIN-FT, Pekey) là mốc cần vượt, **không phải** 0,2946.
  4. **Không cần vượt:** 0,2386 (few-shot, khác protocol), các số KSSA ở Table 4.14 (subset đã lọc, khác tập đánh giá).
- [ANALYSIS] **Cơ hội đề tài nằm ngay trong audit này, không nằm ở việc đẩy số.** Khoảng trống rõ rệt: hiện không có bài nào (a) báo cáo *cả hai* trục một cách nhất quán trên *cả bốn* split, (b) kiểm chứng liệu các con số liên-bài có cùng trục hay không, (c) kiểm tra rò rỉ ở mức corpus pretraining cho các mô hình PLM/PTM lớn khi đánh giá trên DARKIN. Một luận văn làm "đánh giá lại chuẩn hóa + báo cáo song trục + kiểm soát rò rỉ" trên DARKIN có đóng góp phương pháp thật, không phụ thuộc vào việc có vượt được SOTA hay không — và chi phí tính toán nằm trọn trong một GPU Colab. [ANALYSIS] Điều này cũng khớp với quy ước ngôn từ mà người làm đề tài đã dùng ở hướng cũ (nói "kiểm soát rò rỉ", không tuyên bố "vượt SOTA").
- [ANALYSIS] Rủi ro cần nói trước với GVHD: trọng tâm "audit chỉ số" phụ thuộc vào việc **đọc được S.3.7 của COMPASS-PTM**. Nếu S.3.7 hóa ra định nghĩa mAP đúng là trục kinase, thì luận điểm "không so sánh được" sụp một nửa (vẫn còn các vấn đề split/seed/tập ứng viên/leakage/không reproducible). Nên đọc S.3.7 **trước** khi chốt đề tài, không phải sau.

### Gaps

- [UNVERIFIED] Chưa chạy một lượt tra citation đầy đủ (Semantic Scholar / Google Scholar citing-articles) cho btaf480 — bài mới xuất bản 11/2025 nên số bài trích dẫn còn ít, nhưng tôi không loại trừ được một preprint rất mới nào đó. Nguồn cần kiểm thêm: danh sách "cited by" của btaf480 trên OUP và Semantic Scholar.
- [UNVERIFIED] Thời gian huấn luyện thực tế (giờ GPU) và loại GPU: **không bài nào trong ba công trình công bố**. Pekey chỉ cho số epoch/step; DARKIN chỉ nói "notable computational cost"; COMPASS-PTM không nêu. Mọi ước lượng thời gian ở trên là [ANALYSIS] của tôi dựa trên kích thước dataset và model, không phải số do tác giả báo cáo.
- [UNVERIFIED] Có checkpoint COMPASS-PTM trên Hugging Face hay không — sidebar arXiv có mục Hugging Face nhưng đó là menu mặc định của arXiv, không phải xác nhận.
