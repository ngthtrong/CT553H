# Chốt đề tài chính: khuyến nghị và cơ sở

Ngày: **10/10/2026**. Trạng thái: **khuyến nghị có điều kiện, chưa phải đề tài đã duyệt**. Mốc chặn: **tuần 6 báo cáo lại đề tài với GVHD** (hiện tuần 4).

> ⚠️ **CẬP NHẬT 11/10/2026 — đã chạy sáu phép kiểm ở mục 6, và kết quả đổi phán quyết của mục 5.2.** Đọc **[kết quả sáu phép kiểm](../research_notes/main-topic-decision/05-six-checks-results.md)** trước khi dùng bản này. Tóm tắt: trụ tiêu chí 1 **sụp** (Table 4 của chính bài DARKIN đã báo cả hai trục trên cả bốn split); cả ba trục phương pháp đã thử **đều có tiền lệ trực tiếp**; nhưng **RQ2 còn nguyên khoảng trống** và phép đo ba tầng 34,7/32,6/32,7 rất thuận. Sinh viên đã xếp **phương pháp** là ưu tiên và bỏ ràng buộc khớp GVHD — hai điều này làm điểm tương đối của đề tài trong mục 3 **phải tính lại**.

> Tài liệu này chọn **một đề tài chính và một phương án dự phòng**, theo yêu cầu của sinh viên. Bốn ghi chú khảo sát nền nằm ở [research_notes/main-topic-decision/](../research_notes/main-topic-decision/). Nhãn bằng chứng dùng lại quy ước của [báo cáo DARKIN](dark-kinome-darkin-evaluation.md): **[ĐO]** tự chạy/tự đếm, **[NGUỒN]** tác giả công bố, **[PHÂN TÍCH]** suy luận, **[ĐỀ XUẤT]** chưa thực nghiệm, **[CHƯA XÁC MINH]** chưa truy cập được.

## 0. Hai thông tin sinh viên cung cấp ngày 10/10/2026, và chúng loại được gì

| Thông tin                                                                                                       | Nguồn                          | Hệ quả trực tiếp                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GVHD không chấp nhận kết quả âm làm đóng góp chính** (sinh viên đánh giá là rủi ro cao) | Sinh viên trả lời 10/10/2026 | **Loại hướng sirtuin in-vitro** khỏi vị trí đề tài chính. Phán quyết của [khảo sát sâu sirtuin](sirtuin-substrate-deep-research.md) là THU HẸP và *đổi lời hứa sang "một phép đo có kiểm soát về mức độ KHÔNG chuyển được của nhãn"* — đó đúng là một kết quả âm |
| **Có GPU ổn định hơn Colab/Kaggle miễn phí**                                                        | Sinh viên trả lời 10/10/2026 | Mở lại fine-tuning và LoRA. Gỡ đúng ràng buộc mà[đính chính số 9](dark-kinome-darkin-evaluation.md) của báo cáo DARKIN đã nói là *không* quyết định novelty nhưng có quyết định phạm vi thực nghiệm                                                                                      |

Hai câu trả lời này thu hẹp cuộc so sánh về **hai ứng viên**, và cần nói rõ: chúng **không** phải là lời GVHD. Mục 7 còn ghi cả câu cần hỏi lại GVHD.

## 1. Khuyến nghị

### Đề tài chính

> **Dự đoán kinase cho phosphosite ở các kinase ít được nghiên cứu (dark kinome): biểu diễn PLM với bộ mã hóa đa cửa sổ, đánh giá song trục có kiểm soát rò rỉ, và ca nghiên cứu trên họ sirtuin.**

Nền dữ liệu: **DARKIN** ([Bioinformatics 2025, btaf480](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017), repo `tastanlab/darkin`, đã audit tại [research_notes/dark-kinome/](../research_notes/dark-kinome/)).

**Độ tin cậy: trung bình.** Đề tài khả thi và bảo vệ được, nhưng **tiêu chí 1 (tính mới) là tiêu chí yếu nhất** và phụ thuộc sáu phép kiểm ở mục 6 — ba trong số đó làm được trong vài giờ và phải làm **trước** buổi gặp tuần 6.

### Phương án dự phòng

> **Đánh giá lại chuẩn hóa benchmark DARKIN: báo cáo song trục trên cả bốn split, kiểm tính so sánh được của các con số đã công bố, và kiểm soát rò rỉ ở mức site/protein/corpus.**

Dự phòng này **dùng chung toàn bộ hạ tầng** với đề tài chính: cùng dữ liệu, cùng code trích embedding, cùng baseline, cùng website. Nếu phần phương pháp ở đề tài chính không tạo được cải thiện đo được, phần đã làm **không mất**, chỉ đổi trọng tâm đóng góp. Đây là lý do chọn cặp này thay vì hai đề tài rời nhau.

## 2. Tiêu chí, trọng số và điều kiện bắt buộc

Trọng số dưới đây do tôi đặt, phản ánh hai câu trả lời ở mục 0; GVHD **chưa** công bố trọng số nào ([biên bản lần 1, mục 4](../../meeting/session-01-minutes.md) ghi rõ "càng đạt nhiều tiêu chí càng tốt" và tiêu chí 5 là không thể thiếu).

**Ba điều kiện bắt buộc — trượt là loại, không bù bằng điểm cao ở chỗ khác:**

| #            | Điều kiện                                                                                                                            | Lý do                                                              |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **G1** | Nhãn phải là**nhãn thực nghiệm hoặc chú giải độc lập**, không phải điểm do chính pipeline của đề tài sinh ra | Mô hình học trên nhãn tự sinh chỉ học lại bộ chấm điểm |
| **G2** | Phải cho phép một**đóng góp dương đo được**                                                                           | Câu trả lời của sinh viên ở mục 0                            |
| **G3** | Phải có**ứng dụng/website** khả thi trong thời gian còn lại                                                               | Tiêu chí 5 của GVHD, "không thể thiếu"                        |

| Tiêu chí                                                                 | Trọng số | Vì sao trọng số này                                                                                         |
| -------------------------------------------------------------------------- | ---------: | --------------------------------------------------------------------------------------------------------------- |
| Khả năng có đóng góp dương đo được (tiêu chí 2–3 của GVHD) |        25% | Cao nhất vì G2                                                                                                |
| Dữ liệu và nhãn hợp lệ, cách đánh giá đứng được             |        20% | Quyết định đề tài có đo được gì không                                                              |
| Khớp GVHD: lĩnh vực, phương pháp, năm tiêu chí                    |        20% | Người duyệt đề tài                                                                                        |
| Khả thi 8–9 tuần, 1 GPU, kèm website                                   |        15% | [Biên bản, mục 5](../../meeting/session-01-minutes.md)                                                        |
| Tính mới và mức độ đông đúc của hướng                         |        10% | Thấp**không** vì ít quan trọng mà vì cả bốn ứng viên đều đã có tiền lệ dày; xem mục 4 |
| Rủi ro rò rỉ và tái lập                                              |         5% | Đã có công cụ kiểm soát                                                                                  |
| Tận dụng việc đã có                                                  |         5% | Cố ý để thấp, tránh chi phí đã bỏ ra chi phối                                                        |

## 3. Bảng so sánh bốn ứng viên

Điểm 1–5. Ô ghi `G?` nghĩa là trượt điều kiện bắt buộc.

| Tiêu chí                      | Trọng số | **A. DARKIN dark kinome** |  B. Senescence scRNA-seq | C. Sirtuin in-vitro (thu hẹp) |    D. RTK–ATP |
| ------------------------------- | ---------: | ------------------------------: | -----------------------: | -----------------------------: | -------------: |
| Đóng góp dương đo được |        25% |                     **3** |                        2 |       **1 (G2 trượt)** |              3 |
| Dữ liệu và nhãn hợp lệ    |        20% |                     **4** | **1 (G1 trượt)** |                              3 |              4 |
| Khớp GVHD                      |        20% |                     **4** |                        3 |                              4 |              2 |
| Khả thi 8–9 tuần             |        15% |                     **3** |                        2 |                              3 |              3 |
| Tính mới                      |        10% |                     **2** |                        3 |                              2 |              2 |
| Rủi ro rò rỉ/tái lập       |         5% |                     **4** |                        2 |                              3 |              4 |
| Tận dụng việc đã có       |         5% |                     **3** |                        4 |                              5 |              5 |
| **Tổng có trọng số**  |            |                  **3,40** |           **2,15** |                 **2,55** | **3,00** |

**Tổng điểm không phải lý do chọn A.** Lý do là B và C **trượt điều kiện bắt buộc**, và D đã bị GVHD khuyên thay. Bảng này chỉ để thấy A không thắng nhờ một ô lệch.

### 3.1 Vì sao B trượt G1 — và đây là trở ngại mang tính quyết định

`ml/tme-senescence-scrnaseq/preprocessing/README.md` tự ghi, ở [dòng 97](../../../ml/tme-senescence-scrnaseq/preprocessing/README.md):

> Điểm SenMayo là **điểm biểu hiện của một chữ ký gene, không phải nhãn thực nghiệm**. Senescence không có chuẩn vàng ở mức tế bào trong mô, nên mọi mô hình có giám sát huấn luyện trên nhãn dẫn từ điểm này **đang học lại chính bộ chấm điểm đó**.

Cộng thêm ba phép đo **[ĐO]** đã có trên GSE103322: trượt điều kiện đi/dừng `patients_with_ge20_positives` (7 so với ngưỡng ≥ 8); 70% tế bào "dương" là fibroblast còn T cell và B cell bằng 0, nên chênh lệch giữa bệnh nhân phần lớn là chênh lệch **thành phần loại tế bào**; và khi đặt lại ngưỡng trong từng loại tế bào thì dataset **trượt rõ**. Các ngưỡng này được đặt **trước** khi có số thật, nên không thể nới.

Dataset lớn hơn (GSE131907) có thể sửa điều kiện số bệnh nhân, nhưng README đã nói thẳng là **không sửa được** việc điểm đi theo loại tế bào — và càng không sửa được G1. Hướng này vẫn còn giá trị như một bài toán *không giám sát* hoặc một phân tích giới hạn của chữ ký, nhưng không phải đề tài có đóng góp dương trong 8–9 tuần.

### 3.2 Vì sao C trượt G2

[Khảo sát sâu sirtuin](sirtuin-substrate-deep-research.md) đã đo hai lần, độc lập nhau, và cả hai lần đều cho cùng kết luận: nhãn mảng peptide in vitro gần như không chuyển được vào tế bào — MCC **+0,047…+0,080** (Sol 2012, n = 1.417) và **−0,007** trên tập chồng lấn chặt; độ giàu **1,17×, p = 0,291** trên 103 vị trí curated giao với mảng Rauh. Thêm vào đó, **Deep-PLA (2020) đã phủ SIRT1, 2, 3, 6, 7 ở mức residue**, tức phần đáng làm nhất đã có tiền lệ.

Đây là công việc tốt và bằng chứng vững. Nhưng đóng góp còn lại **là một kết quả âm**, và theo mục 0 thì đó là rủi ro cao. Giữ lại làm nguồn ca nghiên cứu, xem mục 5.4.

## 4. Những gì khảo sát ngày 10/10 **gỡ bỏ** khỏi hồ sơ đề tài chính

Phần này quan trọng hơn phần ủng hộ: bốn lập luận bán đề tài trông hấp dẫn và **đều không dùng được**. Ghi lại để không ai mang chúng vào slide tuần 6.

| Lập luận định dùng                                                                            | Vì sao phải bỏ                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Nguồn                                                                      |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| "Audit phát hiện DARKIN rò rỉ ở phía substrate (65,3% dòng test thuộc protein đã thấy)" | **DARKIN đã thấy và chủ động gạt bỏ bằng lý lẽ**, nguyên văn: *"While a site-based split… is possible… More importantly, **it is not necessary**… this strategy does not affect the integrity of the evaluation process."* Họ còn **đã đếm** seen vs novel site trong test (Supplementary Fig. 4). Khung "phát hiện lỗi bị bỏ qua" là **sai sự thật** và sẽ bị bác ngay                                                                                                                                                                                                                                                                                                           | [01](../research_notes/main-topic-decision/01-substrate-holdout-novelty.md)  |
| "Lần đầu đề xuất holdout hai chiều (kinase mới**và** substrate mới)"               | **SAGEPhos (ICLR 2025) đã đặt tên** cả Kinase-cold-start và Substrate-cold-start, và tuyên bố thẳng cold-both *"was **not feasible**"* vì đồ thị bipartite liên thông 99,9%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | [01](../research_notes/main-topic-decision/01-substrate-holdout-novelty.md)  |
| "Vượt SOTA 0,2946 của COMPASS-PTM"                                                              | **0,2946 và 0,1911 gần như chắc chắn không cùng trục đo.** DARKIN: *"AP score for each kinase… hence macro AP"* → **trục kinase**. COMPASS-PTM: *"rank true kinases for each substrate"* → **trục site**. Trên trục site, baseline BZSM của chính DARKIN đã đạt **0,2879** và DARKIN-FT **0,3321**, tức **cao hơn** 0,2946. Thêm nữa: repo COMPASS-PTM **không có code evaluation nào** (đã liệt kê toàn bộ 22 file qua GitHub API), không checkpoint → **0,2946 không tái lập được**                                                                                                                                                          | [02](../research_notes/main-topic-decision/02-darkin-sota-metric-audit.md)   |
| "Đóng góp phương pháp là xử lý nhãn thiếu bằng PU learning"                            | **Không mới và rủi ro cao.** Kanehira & Harada, *Multi-label Ranking from Positive and Unlabeled Data* (CVPR 2016) làm đúng việc này, và tự kết luận *"slightly improved"*. PU đã là công cụ tiêu chuẩn trong kinase-substrate từ 2016 (Yang et al.), AdaSampling 2018, SnapKin 2023, KinoPlex 2026. **Điểm vỡ kỹ thuật:** mọi estimator cần class prior π_k, mà zero-shot theo kinase thì π_k của đúng các kinase cần dự đoán **không ước lượng được**; Mao et al. (TKDE 2025) nói thẳng điều này *"impede the use of PU learning in link prediction"*. Và Cole et al. (CVPR 2021): **label smoothing đơn thuần (66,9) thắng ROLE (66,3)** trên COCO | [03](../research_notes/main-topic-decision/03-missing-label-pu-prior-art.md) |

Thêm hai đính chính phải nhớ:

- **[NGUỒN]** DARKIN đặt kinase **giàu chú giải** vào val/test và kinase dark (< 10 site) vào **train** — ngược với nhiều bản mô tả thứ cấp. Lý do: lớp held-out cần ≥ 10 dương để tính AP được. Đừng nói "test là dark kinase".
- **[NGUỒN]** DARKIN tính đúng là *"we accept the predicted kinase as a true positive if it matches **any** of the true kinases"* → metric **đã hấp thụ một phần** tác hại của nhãn thiếu, nên dư địa cho mọi cải tiến kiểu "xử lý nhãn thiếu" hẹp hơn tưởng. Đây là phản biện mạnh GVHD có thể nêu.

## 5. Đề tài chính, chi tiết

### 5.1 Bài toán, phạm vi, câu hỏi nghiên cứu

**Đầu vào:** một phosphosite (accession + vị trí residue, cửa sổ trình tự quanh nó) và một tập kinase ứng viên công bố rõ, mỗi kinase biểu diễn bằng trình tự miền kinase.
**Đầu ra:** thứ hạng các kinase ứng viên cho phosphosite đó, kèm trạng thái ngoài miền áp dụng và provenance của bằng chứng.
**Phạm vi:** kinase ở tập test **chưa xuất hiện trong huấn luyện** (zero-shot theo lớp kinase). Không hứa hẹn gì về việc kinase đó có thật sự tác động trong một tế bào cụ thể.

Ba câu hỏi nghiên cứu:

- **RQ1 — phương pháp.** Bộ mã hóa đa cửa sổ trên embedding PLM, huấn luyện bằng mục tiêu xếp hạng **theo trục site**, có cải thiện site-AP so với baseline bilinear và fine-tuning của DARKIN, trên cả bốn split chính thức, không? *Chỉ số chính: site-AP. Chỉ số phải báo kèm: kinase-AP.*
- **RQ2 — đánh giá.** Hiệu năng suy giảm	 bao nhiêu khi phân rã tập test theo ba tầng: substrate protein mới / protein đã thấy nhưng site mới / site đã thấy? Đây là **lượng hóa một giả định mà DARKIN phát biểu nhưng chưa chứng minh** (*"does not affect the integrity"*).
- **RQ3 — XAI.** Phần attribution của mô hình có trùng với motif đặc hiệu đo được độc lập không, và trùng tới đâu khi motif **không** được dùng để huấn luyện?

### 5.2 Vì sao đây là đóng góp, theo năm tiêu chí của GVHD

| Tiêu chí                             | Đóng góp dự kiến                                                                                                                                                                                                                                                                                                                                      | Mức tin cậy                            |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **1. Tính mới**                | ~~Trục site là trục ứng dụng cần nhưng ít được báo cáo; chưa bài nào báo cáo nhất quán cả hai trục trên cả bốn split~~ → **ĐÃ RÚT 11/10/2026.** **Table 4 của chính bài DARKIN đã báo cáo cả hai trục trên cả bốn split** (kinase AP 0,1531–0,1800 và Phospho-site AP 0,2747–0,3482), cộng Family AP, Group AP, Masked Group AP và hit@k. Xem [kết quả phép kiểm 6.2c](../research_notes/main-topic-decision/05-six-checks-results.md). Còn lại: **RQ2** (phân rã AP theo ba tầng substrate) là khoảng trống thật — Fig. 4 chỉ **đếm** site, không đo AP theo tầng | **Đã sụp trụ chính.** Xem mục 6 (đã chạy) |
| **2. Cải tiến phương pháp** | Bộ mã hóa**đa cửa sổ** trên embedding PLM cho bài toán theo cặp, cộng mục tiêu xếp hạng theo trục site. Đúng ví dụ GVHD nêu ("CNN sang mCNN hoặc tiếp tục cải tiến mCNN") và đúng nhánh dày nhất trong [danh mục của thầy](../../advisor/README.md)                                                                | Khá, nếu kiểm 6.5 đạt               |
| **3. Phương pháp mới**       | PLM thay cho đặc trưng thủ công — đúng ví dụ GVHD nêu (PSSM → PLM)                                                                                                                                                                                                                                                                             | Khá                                     |
| **4. XAI**                       | Attribution trên cửa sổ peptide và miền kinase,**kiểm fidelity riêng** (occlusion, randomization theo [Adebayo 2018](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html)) và đối chiếu motif atlas **trên phần không dùng để train**. GVHD đã có tiền lệ XAI: BERT-Promoter dùng SHAP | Khá                                     |
| **5. Ứng dụng/website**        | Hai luồng ở mục 5.5                                                                                                                                                                                                                                                                                                                                     | Đạt, nếu giữ phạm vi ở mục 5.5    |

### 5.3 Vì sao khớp GVHD — và chỗ phải trung thực

**Khớp về phương pháp, rất rõ.** Đây là bài toán **mức residue trên trình tự protein**, đúng dạng với nhánh dày nhất trong danh mục GVHD (ATP-binding sites, msCNN-PLM-FAD, mCNN-GenEfflux, MFPS_CNN). GVHD **chấp nhận đầu vào không phải trình tự** ([biên bản, mục 1, bổ sung 07/10](../../meeting/session-01-minutes.md)), nhưng cũng chính biên bản đó ghi: thang đóng góp cho đầu vào **không** phải trình tự là phần sinh viên phải tự lập luận, vì hai luận văn thầy đã hướng dẫn đều là bài toán trên trình tự. Đề tài này **không phải chịu gánh nặng đó** — đó là một lợi thế thật của A so với B.

**Khớp về lĩnh vực: phải phát biểu cẩn thận.** Danh mục GVHD **không có công trình nào về cancer** ([advisor/README.md, mục 3](../../advisor/README.md)); aging có điểm neo ở SirtSAGE. Khảo sát [04](../research_notes/main-topic-decision/04-dark-kinome-cancer-aging-framing.md) cho kết quả rõ:

- **Khung dark kinome mạnh và định lượng được.** NIH IDG đứng sau; **151/634 ≈ 23,8% kinase người là understudied** (Essegian et al., *Cell Reports Medicine* 2020, [PMC7659504](https://pmc.ncbi.nlm.nih.gov/articles/PMC7659504/)); độ lệch chú ý: **EGFR ~90.000 bài so với HIPK4 9 bài**.
- **Liên hệ cancer: thật, nhưng ở mức gene.** Essegian 2020 trên 17 ung thư solid TCGA: biểu hiện của understudied kinase **tiên lượng kết cục xấu**; PKMYT1 overexpressed ở 17/20 ung thư. **Chưa** có bằng chứng nối dự đoán cặp kinase–site với kết cục lâm sàng.
- **Liên hệ aging: yếu.** Không tìm được bằng chứng nào nối dark kinome cụ thể với aging. **Không bán đề tài này như đề tài aging.**
- **Động lực mạnh nhất, và sát đề tài nhất:** Johnson et al., *Nature* 2023 ([PMC9876800](https://pmc.ncbi.nlm.nih.gov/articles/PMC9876800/)) — kinase thượng nguồn chỉ được biết cho **dưới 4%** phosphosite; atlas profile 303 kinase, trong đó **83 là dark kinase**. benchmarKIN ([PMC12098709](https://pmc.ncbi.nlm.nih.gov/articles/PMC12098709/)): thư viện kinase–substrate **thay đổi mạnh** hoạt tính suy ra, và tutorial chạy trực tiếp dữ liệu CPTAC khối u.

Chuỗi lập luận nên dùng, mỗi mắt có nguồn: *phosphoproteomics khối u → suy hoạt tính kinase → phụ thuộc thư viện kinase–substrate → thư viện phủ dưới 4% phosphosite và lệch về kinase well-studied → dark kinase vô hình trong mọi phân tích.* Đây cũng là lý do **phương pháp luận** khiến zero-shot là setting đúng, không chỉ là một chiêu novelty.

**Không nói:** "đây là đề tài ung thư", "góp phần điều trị ung thư", "đây là đề tài aging", hay bất kỳ chữ "đầu tiên" nào.

### 5.4 Cầu nối sang hướng của GVHD: ca nghiên cứu sirtuin

Đây là phần làm đề tài này khớp GVHD hơn hẳn một đề tài kinase thuần, và nó **rẻ**.

**[NGUỒN]** Sirtuin **là** cơ chất của kinase, có cặp cụ thể và có thể trích dẫn:

- **JAK1 → SIRT1 tại Tyr280 và Tyr301**, nằm **trong catalytic domain**, cần cho tương tác SIRT1–STAT3, có trục IL-6/ung thư — Wang et al., *JBC* 2018, [10.1074/jbc.RA117.001387](https://doi.org/10.1074/jbc.RA117.001387). Đây là cặp mạnh nhất: nối sirtuin, kinase và ung thư trong một bài.
- JNK → SIRT1 Ser27/Ser47/Thr530; mTOR → SIRT1 Ser47; CycB/CDK1 → SIRT1 Thr530 + Ser540; CK2 → SIRT1; CDK1/2/4/5 → SIRT2 Ser368; AMPK → SIRT2 Thr101 ([10.1074/jbc.M113.537266](https://doi.org/10.1074/jbc.M113.537266)). Phần lớn trích **qua review** Flick & Lüscher, *Front Pharmacol* 2012 ([PMC3289391](https://pmc.ncbi.nlm.nih.gov/articles/PMC3289391/)) — **phải mở bài gốc trước khi đưa vào đề cương**.

**Khoảng trống là chỗ mạnh, không phải độ dày bằng chứng:** SIRT3 có 6 phosphoserine (101–118), SIRT4 (S255/261/262), SIRT6 (Y294/S303) **phát hiện bằng MS nhưng chưa gán được kinase nào**; SIRT7 chưa map được site nào; SIRT1 có 13 phosphosite MS nhưng chỉ khoảng 4 có kinase đã biết.

**Ca nghiên cứu [ĐỀ XUẤT]:** chạy mô hình trên các phosphosite của SIRT1–7, kiểm xem nó có **recover** được các cặp đã biết (JNK, CDK1, CK2, JAK1) — đây là một phép kiểm độ đúng độc lập với benchmark — rồi **sinh giả thuyết** cho các site chưa gán kinase. Gọi đúng tên: **danh sách ưu tiên để kiểm tra**, không phải cơ chất đã xác nhận. Một mục trong luận văn, một trang trong website, và nó nói trực tiếp tới công trình mới nhất của GVHD.

### 5.5 MVP và chuỗi bài toán → bằng chứng → luận văn

| Bước | Việc                                                                            | Bằng chứng sinh ra                                           | Vào mục nào của luận văn                   |
| ------ | -------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------ |
| 1      | Pin snapshot DARKIN, trích embedding PLM một lần, cache                       | SHA-256, bảng đếm                                           | Dữ liệu và phương pháp                     |
| 2      | Tái lập baseline bilinear/BZSM,**báo cả hai trục**, 4 split × 3 seed | Bảng mốc tái lập có CI                                    | Kết quả, mục baseline                         |
| 3      | Bộ mã hóa đa cửa sổ + mục tiêu xếp hạng trục site                     | Bảng so sánh cùng ngân sách + ablation từng thành phần | Kết quả, mục đóng góp phương pháp (RQ1) |
| 4      | Phân rã test theo ba tầng substrate                                           | Đường suy giảm AP theo tầng                               | Kết quả (RQ2)                                  |
| 5      | XAI: occlusion + randomization + đối chiếu motif giữ riêng                  | Bảng fidelity + bảng trùng motif                            | Kết quả (RQ3)                                  |
| 6      | Ca nghiên cứu sirtuin                                                          | Bảng recover cặp đã biết + danh sách giả thuyết        | Thảo luận                                      |
| 7      | Website hai luồng                                                               | Nhật ký tác vụ, độ chính xác mapping                   | Sản phẩm                                       |

**MVP tối thiểu đủ bảo vệ** (nếu mọi thứ chậm): bước 1, 2, 4 và 7. Tức **đúng phương án dự phòng** — và nó vẫn là một luận văn.

**Website, phạm vi đã cắt cho vừa 8–9 tuần.** Không làm Spring Boot + React + FastAPI ba lớp như sơ đồ trong CLAUDE.md. Một dịch vụ FastAPI phục vụ mô hình đã xuất, cộng một giao diện mỏng, hai luồng:

- **Một site:** nhập accession/vị trí hoặc peptide, chọn tập kinase ứng viên → thứ hạng kinase, attribution, provenance, cảnh báo ngoài miền.
- **Một thí nghiệm:** tải bảng phosphosite → thứ hạng theo lô, tải kết quả về.

Phải phân biệt rõ trên giao diện: liên kết **curated** / **dự đoán** / **unknown**. Không hiển thị score chưa calibrate như xác suất. Không gọi kết quả là "cơ chất đã xác nhận".

### 5.6 Lộ trình 8–9 tuần

| Tuần                     | Việc                                                                                   | Cổng                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Trước tuần 6** | Sáu phép kiểm ở mục 6                                                              | **Ba phép kiểm nhanh phải đạt, nếu không thì đổi khung đóng góp**      |
| 6                         | Báo cáo GVHD: bài toán, động cơ, khảo sát đã phân nhóm theo phương pháp | Chốt đề tài                                                                           |
| 1–2                      | Pin dữ liệu, trích embedding, tái lập baseline hai trục                           | Khớp số công bố trong sai số seed                                                    |
| 3–4                      | Bộ mã hóa đa cửa sổ + mục tiêu xếp hạng, ablation                             | **Cổng quyết định: có cải thiện nhất quán dấu trên cả 4 split không?** |
| 5                         | Phân rã ba tầng; XAI                                                                 |                                                                                           |
| 6–7                      | Website hai luồng; ca nghiên cứu sirtuin                                             |                                                                                           |
| 8–9                      | Viết, dự phòng trượt tiến độ                                                    |                                                                                           |

**Cổng ở tuần 4 là cổng thật.** Khảo sát [03](../research_notes/main-topic-decision/03-missing-label-pu-prior-art.md) đã đo: spread giữa 4 split là **~0,024 AP**, trong khi std giữa các seed chỉ **0,001–0,008**. Nghĩa là một cải thiện chỉ thấy trên một split **không phải bằng chứng**. Nếu tới hết tuần 4 chưa có cải thiện nhất quán dấu trên cả bốn split, **chuyển sang phương án dự phòng** và dùng tuần 5–7 làm cho phần đánh giá lại thật kỹ, thay vì đuổi theo một cải thiện không tới.

### 5.7 Rủi ro lớn nhất và cách xử lý

| Rủi ro                                                                                                                           | Dấu hiệu nhận biết                                                            | Xử lý                                                                                                                                                                                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tiêu chí 1 không đủ với GVHD** — hướng đông đúc (Pekey 2025, COMPASS-PTM 2026, KinoPlex 2026, SAGEPhos 2025) | GVHD hỏi "khác gì mấy bài kia" mà không trả lời được bằng một bảng | **Rủi ro số một.** Chuẩn bị sẵn **bảng khác biệt theo nhóm phương pháp** đúng format [mục 3 của biên bản](../../meeting/session-01-minutes.md); dựa novelty vào **trục site + phân rã ba tầng + kiểm rò rỉ corpus**, không dựa vào "mô hình mới" |
| Phương pháp không tạo cải thiện                                                                                            | Cổng tuần 4                                                                     | Phương án dự phòng, chia sẻ toàn bộ hạ tầng                                                                                                                                                                                                                                               |
| **Chọn baseline yếu**                                                                                                     | So với 0,1911 mà không nhắc 0,2250                                            | Phải nêu**cả** 0,2250 (kinase) và **0,3321** (site) của Pekey. Luận văn đó công khai và cùng nhóm tác giả benchmark — bỏ qua sẽ bị bắt lỗi                                                                                                                         |
| Trộn hai trục AP                                                                                                                | Trích "+54%" của COMPASS-PTM                                                    | Mọi bảng ghi rõ trục. Đọc S.3.7 trước (mục 6.1)                                                                                                                                                                                                                                            |
| Website ngốn hết thời gian                                                                                                     | Hết tuần 7 chưa có luồng nào chạy                                          | Phạm vi đã cắt ở 5.5; làm luồng "một site" trước, luồng lô là tùy chọn                                                                                                                                                                                                               |
| COMPASS-PTM không tái lập được                                                                                              | Đã biết: không có code eval, không checkpoint                               | **Không đặt 0,2946 làm mục tiêu phải vượt.** Coi là con số cần audit                                                                                                                                                                                                              |

## 6. Sáu phép kiểm trước khi chốt chính thức

Ba phép đầu làm được trong vài giờ và **phải xong trước buổi gặp tuần 6**. Mỗi phép có thể đổi quyết định.

| #             | Phép kiểm                                                                                                                                                                                        | Vì sao đổi được quyết định                                                                                                                          | Chi phí                 |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| **6.1** | Tải tay**arXiv 2510.23492** và đọc **Supplementary S.3.7** của COMPASS-PTM: công thức mAP                                                                                       | Nếu 0,2946 là trục kinase thì nó thật sự là SOTA và bối cảnh đổi hẳn. Nếu là trục site thì nó**dưới** baseline của chính DARKIN | ~15 phút                |
| **6.2** | Lấy**DARKIN Supplementary Fig. 4** (seen vs novel site trong test)                                                                                                                          | Nếu Fig. 4**đã** phân rã AP theo seen/novel thì **RQ2 bị thu hẹp rất nhiều**                                                           | Cần quyền thư viện   |
| **6.3** | Đếm trên checkout DARKIN: nếu ép substrate-protein-disjoint thì còn**bao nhiêu dòng test** và bao nhiêu kinase còn ≥ 5 site                                                     | SAGEPhos nói cold-both bất khả thi vì bipartite liên thông 99,9%. Nếu DARKIN cũng vậy thì**không tạo split mới**, chỉ phân rã ba tầng | ~1 giờ, script đã có |
| 6.4           | Kiểm Pekey 0,2250/0,3321 đã thành bài báo chưa                                                                                                                                              | Hiện chỉ tồn tại trong một**luận văn thạc sĩ chưa qua phản biện**                                                                          | ~20 phút                |
| 6.5           | Tra xem**bộ mã hóa đa cửa sổ** đã được áp dụng cho DARKIN hoặc kinase–substrate theo cặp chưa. ⚠️ **SAGEPhos** nghe như GraphSAGE — kiểm kiến trúc nó trước | Đây là trục tiêu chí 2. Nếu đã có tiền lệ trực tiếp thì phải đổi                                                                           | ~1 giờ                  |
| 6.6           | Chạy lại một vòng tìm 2012–2026 về gán kinase cho phosphosite sirtuin, trước khi nói "bằng chứng thưa"                                                                               | Các cặp ở 5.4 trích qua review**2012**, đã 14 năm                                                                                               | ~1 giờ                  |

## 7. Những gì còn thiếu, có thể đổi quyết định

**Thông tin từ GVHD — quan trọng hơn mọi phép kiểm ở trên.** Câu hỏi đã có sẵn ở [mục 7 biên bản lần 1](../../meeting/session-01-minutes.md), nay thêm trọng tâm:

1. **Thứ tự ưu tiên giữa năm tiêu chí** nếu không đạt hết trong 8–9 tuần. Câu này quyết định nên dồn sức vào phương pháp hay vào đánh giá + sản phẩm. => phương pháp
2. **"Cancer" của thầy là nhánh nào?** Danh mục thầy không có công trình cancer. Nếu thầy có một nhánh cụ thể trong đầu, đề tài này có thể lệch. => không cần quan tâm đến việc có liên quan đến các nghiên cứu hiện tại của giảng viên hay không!
3. **Thầy có bài toán nào đang mở trong nhóm** mà sinh viên có thể nhận? Nhận một bài toán của nhóm gần như chắc chắn khớp tiêu chí 1 hơn là tự đề xuất vào một hướng đông đúc. => chưa có.
4. **Kết quả âm có được chấp nhận ở mức nào?** Mục 0 ghi đây là *đánh giá của sinh viên*, chưa phải lời thầy. Nếu thầy chấp nhận, hướng C quay lại cuộc đua ngay — bằng chứng của nó là thứ vững nhất trong cả repo. => không nên chấp nhận kết quả âm
5. **Phạm vi tối thiểu của website. => không quan trọng**

**Thông tin kỹ thuật còn thiếu:** Methods/Supplement của **KinoPlex** (paywall, nature.com redirect sang IdP login); corpus pretraining của COMPASS-PTM (không được mô tả → không loại trừ được leakage từ PhosphoSitePlus); tỉ lệ multi-label chính xác của DARKIN (Supplementary Fig. 3 — **quyết định trực tiếp dư địa đóng góp**); loss thực tế của BZSM baseline; trang OpenReview của SAGEPhos (review có thể chứa đúng câu hỏi về substrate leakage). Lưu ý **bản arXiv v2 của SAGEPhos đã bị tác giả rút** vì *"significant disagreements"* trong nhóm → chỉ trích cho phần **khái niệm protocol**, không trích làm mốc SOTA.

## 8. Giới hạn của chính báo cáo này

Chưa chạy baseline, chưa huấn luyện mô hình, chưa triển khai gì. Mọi con số của người khác đều **chưa tái lập**. Trọng số ở mục 2 do tôi đặt, không phải của GVHD. Ba điều kiện bắt buộc cũng do tôi đặt, dựa trên hai câu trả lời của sinh viên ngày 10/10/2026 — và một trong hai (kết quả âm không được chấp nhận) là **đánh giá của sinh viên về GVHD**, chưa phải lời GVHD. Nếu điều đó sai, mục 3.2 phải tính lại.

Ghi chú nền: [01 substrate holdout](../research_notes/main-topic-decision/01-substrate-holdout-novelty.md) · [02 audit SOTA và trục đo](../research_notes/main-topic-decision/02-darkin-sota-metric-audit.md) · [03 tiền lệ nhãn thiếu/PU](../research_notes/main-topic-decision/03-missing-label-pu-prior-art.md) · [04 khung cancer/aging](../research_notes/main-topic-decision/04-dark-kinome-cancer-aging-framing.md)
