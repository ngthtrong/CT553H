# Kết quả sáu phép kiểm trước khi chốt đề tài

Ngày chạy: **11/10/2026**. Thực hiện theo [mục 6 của báo cáo chốt đề tài](../main-topic-decision-2026-10-10.md).

Quy ước nhãn: **[ĐO]** tự chạy/tự đếm trong phiên này · **[NGUỒN]** trích nguyên văn từ bài · **[PHÂN TÍCH]** suy luận · **[CHƯA XÁC MINH]**.

## Thứ tự ưu tiên đã đổi theo câu trả lời của sinh viên (11/10/2026)

| Câu trả lời | Hệ quả lên sáu phép kiểm |
|---|---|
| **Ưu tiên tiêu chí: phương pháp** | **6.5 trở thành phép kiểm quyết định**, không còn là phép kiểm phụ — nó kiểm chính trục đóng góp |
| **Không cần quan tâm đề tài có liên quan nghiên cứu hiện tại của GVHD hay không** | **6.6 mất mục đích hoàn toàn** → đã bỏ. Ca nghiên cứu sirtuin tồn tại *chỉ* để nối sang SirtSAGE. Cũng làm **giảm** lợi thế của DARKIN so với các ứng viên khác (xem mục 7) |
| Thầy chưa có bài toán mở trong nhóm | Không nhận được bài toán sẵn → phải tự đề xuất vào một hướng đông đúc |
| Không nên chấp nhận kết quả âm | Giữ nguyên điều kiện bắt buộc G2 |
| Phạm vi website không quan trọng | ⚠️ Xung đột với [biên bản lần 1, mục 4](../../../../project/meetings/2026-10-02-session-01/minutes.md): GVHD nói tiêu chí 5 là **"không thể thiếu"**. Giữ website ở phạm vi tối thiểu, không bỏ |

## 6.1 — Trục đo của mAP 0,2946 (COMPASS-PTM): **ĐÃ CHỐT, cross-axis**

**[NGUỒN]** arXiv 2510.23492 = *Learning the PTM Code through a Coarse-to-Fine, Mechanism-Aware Framework* (Zhang, Cao, Gao, Wang, Li, Xu, Tan, Zhu, Hsieh, Gu, Heng). Abstract báo *"a 54% gain in zero-shot enzyme assignment"*; không nhắc DARKIN trong abstract.

**[NGUỒN]** Mục 2.2.4: mAP là *"the mean Average Precision (mAP), which assesses the ability to correctly rank **true kinases for each substrate**"*. Công thức (Eqs. 15–17, mục 6.2.2): `mAP = (1/N) Σ AP_i` với **N = số substrate**, và `AP_s = (1/|K_s⁺|) Σ P(k)·I(rank_k(s) ∈ K_s⁺)`.

**[NGUỒN]** Hai con số đều có trong bài: *"our model achieves the mAP of 0.2946"* và *"the highest reported score from the original study (0.1911)"*.

**Kết luận [PHÂN TÍCH]:** `mAP` của COMPASS-PTM là **trục site/substrate**, còn 0,1911 của DARKIN là **trục kinase** (xem 6.2). Phép so sánh "+54%" là **so chéo trục**. Không nói tác giả gian; nói đúng là **hai con số không cùng phép đo**.

**Chưa đóng:** Supplementary S.3.7 không có trong bản HTML arXiv; split/seed DARKIN và kích thước tập kinase ứng viên **không được nêu** ở main text (đẩy sang S.2.2). Site-AP phụ thuộc mạnh vào kích thước universe, nên **không kết luận** COMPASS-PTM kém hơn — chỉ kết luận phép so sánh đã công bố không hợp lệ.

## 6.2 — DARKIN Supplementary Fig. 4: **ĐÃ CHỐT, và đây là phát hiện nặng nhất**

Lấy được bản toàn văn mở của chính bài DARKIN qua **`research.sabanciuniv.edu/53050/1/DARKIN.pdf`** (vòng được paywall OUP), giải nén bằng `pdftotext -layout`.

### 6.2a Fig. 4 chỉ là **thống kê đếm**, không phải phân rã AP

**[NGUỒN]** *"Additionally, we report the sites unique to the test set or shared with the validation and training data in the Fig. 4."* → Fig. 4 đếm site, **không** báo AP theo tầng. **RQ2 vẫn còn nguyên khoảng trống.**

### 6.2b Lý lẽ của DARKIN là một phát biểu **có thể bác bỏ** và chưa ai kiểm

**[NGUỒN]** nguyên văn:

> *"While a site-based split of the train, validation, and test set is possible, it is difficult to obtain a balanced split based on all four criteria. **More importantly, it is not necessary**, as the aim is to predict the right kinases for a known phosphosite. Even when a phosphosite appears in both splits, the associated kinase labels are disjoint across training and test sets. The model is still required to generalize to unseen kinases. **It is indeed more challenging for the model**, as it has previously associated this site with a different kinase and now needs to predict its association with the unseen test kinase. Therefore, this strategy does not affect the integrity of the evaluation process."*

Tức DARKIN **chủ động khẳng định** site overlap làm bài toán **khó hơn**, không phải dễ hơn. Đây là một giả thuyết thực nghiệm, **chưa ai đo**, và phép đo 6.3 dưới đây làm được trực tiếp.

### 6.2c ⚠️ Phải RÚT một khẳng định trong báo cáo chốt đề tài

**[NGUỒN] Table 4 của chính bài DARKIN đã báo cáo CẢ HAI TRỤC trên CẢ BỐN SPLIT:**

| Split | Embedding | AP (trục kinase) | **Phospho-site AP** | Family AP | Group AP | Masked Group AP |
|---|---|---:|---:|---:|---:|---:|
| 1 | ESM1B (cls) | 0,1769 | **0,2830** | 0,2278 | 0,3959 | 0,4054 |
| 1 | SaProt (cls) | 0,1800 | **0,3053** | 0,2384 | 0,3903 | 0,3868 |
| 2 | ESM1B (cls) | 0,1536 | 0,2747 | 0,1989 | 0,3689 | 0,3644 |
| 2 | SaProt (cls) | 0,1599 | 0,2929 | 0,2087 | 0,3649 | 0,3702 |
| 3 | ESM1B (cls) | 0,1531 | 0,2951 | 0,1987 | 0,3747 | 0,3508 |
| 3 | SaProt (cls) | 0,1627 | 0,3142 | 0,2104 | 0,3663 | 0,3598 |
| 4 | ESM1B (cls) | 0,1652 | 0,3118 | 0,2142 | 0,3969 | 0,3563 |
| 4 | SaProt (cls) | 0,1690 | **0,3482** | 0,2205 | 0,4069 | 0,3674 |

**[NGUỒN]** Định nghĩa: *"family AP, where kinase predictions are aggregated by their families; group AP, where kinase predictions are aggregated by their groups; and **phosphosite AP, which evaluates precision for phosphosite-specific predictions**"*. Còn có **Masked Group AP** và **hit@k**.

Ba hệ quả:

1. **Khẳng định "chưa bài nào báo cáo nhất quán cả hai trục trên cả bốn split" là SAI.** Phải rút khỏi mục 5.2 của báo cáo chốt đề tài. Đây là trụ chính của tiêu chí 1 trong bản khuyến nghị — **nó sụp**.
2. **Baseline đã công bố của DARKIN trên trục site đạt 0,3053 (Split 1, SaProt) và 0,3482 (Split 4, SaProt) — đều CAO HƠN 0,2946 của COMPASS-PTM.** Nghĩa là kết luận 6.1 được xác nhận **bằng chính bài đã phản biện**, không cần dựa vào luận văn Pekey chưa qua phản biện nữa.
3. Bối cảnh metric đã dày hơn tưởng: 5 chỉ số × 4 split × 2 pLM đã có sẵn.

### 6.2d Đính chính ngưỡng chia kinase

**[NGUỒN]** *"Kinases that are associated with fewer than **15** phosphosites are defined as train kinases"*; ngưỡng cho validation là *"at least **10** phosphosites per kinase"*; kinase ≥ 90% sequence identity bị gom cùng một tập.

→ Sửa con số "< 10 site → train" trong [nhật ký 10/10](../../../../journal/README.md). Đúng là **< 15**. Chiều thì không đổi: kinase **giàu** chú giải nằm ở val/test.

## 6.3 — Ép substrate-protein-disjoint còn lại bao nhiêu: **ĐÃ CHỐT, [ĐO]**

Checkout `tastanlab/darkin` tại commit `498de014951f962f77ca1b96340fead3cc24c450`, split 1 / seed 12345 / ZSL. Script: `check63_bipartite.py` (chưa từng được commit vào repo). Train 8.559 dòng / 3.319 protein; test 1.414 dòng.

### 6.3a Phân rã ba tầng — **cân bằng gần như hoàn hảo, rất thuận cho RQ2**

| Tầng | Dòng test | % | Cặp có nhãn |
|---|---:|---:|---:|
| **T1** substrate protein **mới** | 491 | **34,7%** | 536 |
| **T2** protein đã thấy, **site mới** | 461 | **32,6%** | 502 |
| **T3** site key **đã có** trong train | 462 | **32,7%** | 577 |

**[ĐO]** Cửa sổ 15 aa trùng train: **462 dòng = đúng bằng T3**. Nghĩa là **không có** cửa sổ gần-trùng nào đến từ protein khác; overlap cửa sổ không thêm gì ngoài overlap site key. Sạch.

**[PHÂN TÍCH]** Ba tầng ~1/3 mỗi tầng là điều kiện tốt nhất có thể cho RQ2: mỗi tầng đủ dòng để tính AP, và cỡ tầng gần nhau nên so sánh không bị lệch bởi cỡ mẫu.

### 6.3b Tạo split cold-both thì **không khả thi** — xác nhận bằng số của chính DARKIN

**[ĐO]** Nếu chỉ giữ T1 làm tập test:

| Ngưỡng nhãn/kinase | Kinase còn lại (chỉ T1) | Kinase ở test đầy đủ |
|---|---:|---:|
| ≥ 1 | 36 | 38 |
| ≥ 5 | **25** | 38 |
| ≥ 10 | **15** | 38 |
| ≥ 12 | 12 | 38 |
| ≥ 14 | 11 | 38 |

Nhãn/kinase trong T1: min 1 · median 9 · max 68.

**[PHÂN TÍCH]** DARKIN cần **≥ 10 dương** cho lớp held-out để AP có nghĩa. Ép substrate-protein-disjoint làm tập kinase test tụt từ **38 xuống 15**, mất ~60% không gian nhãn. **Kết luận: không tạo split cold-both. Làm phân rã ba tầng ở 6.3a.** Đây đúng là khuyến nghị đã nêu, nay có số của chính DARKIN đỡ lưng thay vì chỉ dựa vào phát biểu của SAGEPhos.

### 6.3c Độ liên thông bipartite — đo trên DARKIN, không vay của SAGEPhos

**[ĐO]** Đồ thị bipartite kinase × site:

| Tập | Nút | Thành phần liên thông | Lớn nhất | % nút trong thành phần lớn nhất |
|---|---:|---:|---:|---:|
| train | 8.867 | 60 | 8.627 | **97,3%** |
| train + test | 9.857 | 56 | 9.661 | **98,0%** |

**[PHÂN TÍCH]** DARKIN liên thông **98,0%** — cùng bậc với con số 99,9% SAGEPhos báo trên dataset của họ. Vậy lý do cold-both bất khả thi **không phải đặc thù dataset SAGEPhos**; nó đúng với DARKIN, và giờ có phép đo riêng để trích.

## 6.4 — Pekey 0,2250 / 0,3321 đã thành bài báo chưa: **CHƯA**

**[NGUỒN]** Luận văn thạc sĩ Mert Pekey, *Zero/Few-Shot Dark Kinase-Phosphosite Association Prediction With Biologically Grounded Data Augmentation*, Sabancı University, **07/2025**, GVHD Öznur Taştan ([eprint 53625](https://research.sabanciuniv.edu/id/eprint/53625/)). Giới thiệu **DARKIN-FT** (fine-tune end-to-end phosphosite encoder) và **DARKIN-Interact** (binary classifier, joint attention trên cặp trình tự).

**[ĐO tra cứu]** Không tìm được bài báo riêng cho DARKIN-FT/DARKIN-Interact. Bài benchmark đã công bố là Sunar, Işık, **Pekey**, Cinbiş, Taştan, *Bioinformatics* 41(11) 2025 — Pekey là đồng tác giả, nhưng Table 4 của bài đó **không** chứa DARKIN-FT/Interact.

**[PHÂN TÍCH]** Hai mặt: (a) 0,2250/0,3321 **chưa qua phản biện**, nên "vượt mốc đã công bố" vẫn phát biểu được; (b) luận văn **công khai và cùng nhóm tác giả benchmark**, nên bỏ qua nó sẽ bị bắt lỗi chọn baseline yếu — và nhóm đó rất có thể công bố trước khi sinh viên bảo vệ (tuần 14–15).

**[NGUỒN]** Chi tiết dùng được: ProGen2 và KSSA weak labeling **làm giảm** hiệu năng; augmentation bằng **chuỗi đồng dạng cải thiện** Macro AP của DARKIN-Interact.

## 6.5 — Bộ mã hóa đa cửa sổ đã ai dùng chưa: **phép kiểm quyết định, và kết quả KHÔNG thuận**

### 6.5a SAGEPhos **không** phải GraphSAGE — rủi ro này không xảy ra

**[NGUỒN]** SAGEPhos (ICLR 2025, nhóm CUHK) dùng **ESM-2-650M** + **Substrate Structure Encoder là RGCN** (6 lớp, hidden 512) trên **đồ thị cấu trúc 3D của substrate**, predictor MLP 3 lớp dropout 0,2, fusion gated + residual. "SAGE" là *Sage Bio-Coupled and Augmented* fusion, **không phải GraphSAGE**, và **không phải** đồ thị bipartite kinase–site. Task là **phân loại nhị phân** kinase-specific, không phải xếp hạng multilabel như DARKIN.

### 6.5b Nhưng mCNN + PLM **đã có tiền lệ trực tiếp**, kể cả trong danh mục GVHD

**[NGUỒN]** **DeepPhos** đã dùng **nhiều cửa sổ 25, 33, 51** cho dự đoán phosphosite (densely connected CNN blocks). **MusiteDeep** dùng CNN + attention. Cả hai huấn luyện mô hình riêng cho từng họ kinase.

**[PHÂN TÍCH]** Cộng thêm một điều đã có trong repo: danh mục GVHD **đã có `msCNN-PLM-FAD` (2026)** — tức **multi-scale CNN trên embedding PLM** chính là phương pháp sẵn có của thầy. Vậy "mCNN trên embedding PLM cho DARKIN" là **ghép hai thứ đã biết và áp vào benchmark mới**. Đó đúng là điều [đánh giá DARKIN](../darkin-evaluation.md) đã cảnh báo ở tiêu chí 3: *"Không chỉ liệt kê PLM, LoRA, attention, conformal."*

**Không tìm được** tiền lệ đúng cho "mCNN trên PLM + xếp hạng theo cặp zero-shot trên DARKIN". Nhưng đây là **novelty mỏng**: mới ở chỗ ghép, không mới ở cơ chế.

### 6.5c Thử trục phương pháp thay thế: mục tiêu xếp hạng theo trục site

Lập luận định dùng: DARKIN huấn luyện bằng **cross-entropy softmax trên light kinase** (đã xác nhận [NGUỒN], Eq. 2), tức tối ưu theo kinase; còn chỉ số ứng dụng cần là **site-AP**. Một **listwise/margin ranking loss trên tập kinase ứng viên của từng site** sẽ khớp mục tiêu huấn luyện với trục đánh giá.

**[NGUỒN]** Các mảnh đều đã có: listwise LTR là chuẩn mực sẵn; multi-label ZSL đã ghi nhận đúng vấn đề điểm không so được giữa các ví dụ (*"scores in pairwise RankNet and hinge rank losses are unbounded, so they can vary across examples"*); margin-based ranking loss cho multi-label ZSL đã có (chest radiograph). **Không tìm được** công trình áp listwise loss cho tập kinase ứng viên trong kinase–substrate.

**[PHÂN TÍCH]** Mạnh hơn 6.5b vì có lập luận nguyên lý (lệch giữa mục tiêu huấn luyện và trục đánh giá) cộng một vấn đề đã được ghi nhận trong y văn MLZSL. Nhưng vẫn là **áp một loss đã biết vào task mới**. Và 6.2c vừa cho thấy DARKIN **đã báo cáo** site-AP, nên không thể nói "trục site bị bỏ quên".

### 6.5d Kết luận của phép kiểm quyết định

**Ba trục phương pháp đã thử, cả ba đều có tiền lệ trực tiếp:**

| Trục phương pháp | Tiền lệ | Mức còn lại |
|---|---|---|
| mCNN trên embedding PLM | DeepPhos (đa cửa sổ 25/33/51); `msCNN-PLM-FAD` 2026 của chính GVHD | Mỏng — ghép hai thứ đã biết |
| PU / nhãn thiếu | Kanehira & Harada CVPR 2016; chuẩn mực trong kinase-substrate từ 2016 | Loại (xem [ghi chú 03](03-missing-label-pu-prior-art.md)) |
| Listwise ranking theo trục site | Mảnh ghép đã có; chưa thấy áp cho kinase–substrate | Mỏng–trung bình; và trục site **không** bị bỏ quên (6.2c) |

**[PHÂN TÍCH]** Trong khi đó mặt cạnh tranh rất dày: DARKIN 2025 + Pekey 2025 + SAGEPhos ICLR 2025 + COMPASS-PTM 2026 *Nature Communications* + KinoPlex 2026 *Nature Biotechnology* + Prot2Token + ít nhất hai preprint autoregressive 2025. **Đây là một hướng đang nóng.**

## 6.6 — Gán kinase cho phosphosite sirtuin: **ĐÃ BỎ**

Sinh viên trả lời 11/10/2026: không cần quan tâm đề tài có liên quan nghiên cứu hiện tại của GVHD hay không. Ca nghiên cứu sirtuin tồn tại **chỉ** để nối sang SirtSAGE, nên phép kiểm này mất mục đích. Không chạy. Bằng chứng ở [ghi chú 04](04-dark-kinome-cancer-aging-framing.md) vẫn giữ nếu sau này cần.

## Tổng kết: còn lại gì sau sáu phép kiểm

**Đã chết (phải gỡ khỏi mọi tài liệu gửi GVHD):**

1. "Chưa ai báo cáo cả hai trục trên cả bốn split" — **sai**, Table 4 của DARKIN đã có (6.2c). *Đây là trụ tiêu chí 1 của bản khuyến nghị.*
2. "Audit phát hiện rò rỉ phía substrate bị bỏ qua" — sai, có Fig. 4 + lý lẽ tường minh (6.2a/6.2b).
3. "Holdout hai chiều là mới" — SAGEPhos đã đặt tên; và **không khả thi**, 38 → 15 kinase (6.3b).
4. "Vượt SOTA 0,2946" — so chéo trục; baseline đã công bố của DARKIN đạt 0,3053–0,3482 trên trục site (6.1 + 6.2c).
5. "mCNN + PLM là đóng góp phương pháp" — DeepPhos + `msCNN-PLM-FAD` của chính GVHD (6.5b).

**Còn sống:**

- **RQ2 là khoảng trống thật và rẻ.** DARKIN **khẳng định** site overlap *"does not affect the integrity"* và *"is indeed more challenging"*; Fig. 4 chỉ đếm, **không đo AP theo tầng**. Phân rã ba tầng 34,7/32,6/32,7 (6.3a) kiểm được trực tiếp. **Nhưng đây là đóng góp đánh giá/phản biện, không phải đóng góp phương pháp** — đúng thứ sinh viên vừa xếp ưu tiên thấp.
- Bộ số [ĐO] của 6.3 (ba tầng, 38→15, liên thông 98,0%) dùng được trong luận văn bất kể chọn hướng nào.

**Mâu thuẫn phải đưa sinh viên quyết:** ưu tiên là **phương pháp**, nhưng sau sáu phép kiểm thì **phương pháp là chỗ yếu nhất** của đề tài này, còn chỗ mạnh nhất lại là **đánh giá**. Thêm nữa, bỏ ràng buộc "khớp GVHD" đã **gỡ mất một trong hai lợi thế chính** của DARKIN (bài toán mức residue trên trình tự, đúng nhánh dày của thầy), nên điểm tương đối của nó trong [bảng so sánh](../main-topic-decision-2026-10-10.md) phải tính lại.
