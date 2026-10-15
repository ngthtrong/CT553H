# Đánh giá đề tài dark kinome trên DARKIN

Ngày đánh giá: **10/10/2026**. Trạng thái: **ứng viên đang khảo sát, chưa chốt đề tài, chưa huấn luyện mô hình**.

Theo yêu cầu của sinh viên, đánh giá này bỏ ràng buộc thời gian, lĩnh vực, mức liên quan tới GVHD và tài nguyên CPU/GPU. Ý tưởng sửa lỗi phần mềm có kiểm chứng đã được sinh viên loại; báo cáo tập trung vào dark kinome. Điều này chưa có nghĩa sinh viên đã bỏ SIRT hoặc GVHD đã duyệt hướng mới.

## 1. Kết luận đánh giá

**Đáng tiếp tục khảo sát, nhưng cần đổi trọng tâm đóng góp so với bản khuyến nghị ban đầu.** DARKIN cung cấp một nền thực nghiệm cụ thể. Tuy nhiên, PLM theo cặp, attention, fine-tuning, motif và đánh giá hạ nguồn đều có tiền lệ. Không thể coi việc ghép các thành phần này là bằng chứng đạt cả năm tiêu chí.

Hướng ưu tiên đề xuất:

> **Dự đoán liên kết kinase–phosphosite cho kinase chưa thấy, với cơ chế lựa chọn và đặt trọng số quan hệ dự đoán nhằm cải thiện suy luận hoạt tính kinase khi thư viện cơ chất thiếu chú giải.**

Giả thuyết trung tâm: chất lượng xếp hạng ở mức liên kết và chất lượng suy luận hoạt tính không nhất thiết tăng cùng nhau; bổ sung chọn lọc có thể hữu ích hơn bổ sung hàng loạt. Đây là **giả thuyết đề xuất**, chưa có kết quả của dự án và chưa được chứng minh là khoảng trống hoàn toàn mới.

Ưu tiên thứ hai, nếu benchmark hạ nguồn không phủ đủ kinase ít chú giải: **học thứ hạng trong điều kiện thiếu nhãn và khái quát sang kinase/nhóm đồng dạng mới**. Conformal là mở rộng có điều kiện; không đưa lời hứa phủ 90% vào tên đề tài lúc này.

### Quy ước bằng chứng

| Nhãn | Ý nghĩa |
|---|---|
| **[ĐO]** | Script trong phiên này đọc CSV/mã từ checkout DARKIN đã pin commit; có artifact tái tạo |
| **[NGUỒN]** | Tác giả công bố trong bài, repo hoặc luận văn; không phải kết quả tự tái lập |
| **[PHÂN TÍCH]** | Nhận xét suy ra từ bằng chứng, có thể cần kiểm tra thêm |
| **[ĐỀ XUẤT]** | Thiết kế nghiên cứu hoặc giả thuyết chưa thực nghiệm |
| **[CHƯA XÁC MINH]** | Chưa đọc đủ, chưa tải/chạy, hoặc chưa có dữ liệu để kết luận |

Nguồn nội bộ: [năm tiêu chí của GVHD](../../../project/meetings/2026-10-02-session-01/minutes.md), [bản khuyến nghị ban đầu](../../../archive/surveys/criteria-only-recommendation.md). Bằng chứng tự kiểm: [ghi chú audit](darkin-audit/README.md), [audit-results.json](darkin-audit/audit-results.json). Chỉ khảo sát và audit dữ liệu/mã; chưa chạy baseline hoặc model mới.

## 2. Bài toán, ý nghĩa và giới hạn đầu ra

### 2.1 Giải thích cho sinh viên CNTT

Phosphorylation là việc gắn nhóm phosphate lên một vị trí của protein. Kinase là enzyme thực hiện việc đó. Phosphoproteomics có thể tìm vị trí được phosphoryl hóa nhưng việc biết **kinase nào tác động lên vị trí nào** là nhiệm vụ riêng. Một vị trí có thể liên quan nhiều kinase, tùy điều kiện sinh học.

Trong bài toán này, phosphosite đã được xác định; mô hình xếp hạng kinase ứng viên dựa trên cửa sổ trình tự và thông tin kinase. “Dark” nói tới mức thiếu kiến thức/chú giải, không phải một họ kinase riêng.

Không đồng nhất ba câu hỏi: (a) residue có thể bị phosphoryl hóa; (b) kinase có tương thích với trình tự quanh residue; (c) kinase thực sự tác động trong một tế bào cụ thể. Mô hình trình tự chủ yếu hỗ trợ (b); dữ liệu nguồn và kiểm chứng quyết định có thể nói tới (c) đến đâu. **[PHÂN TÍCH]**

### 2.2 Đặc tả nhiệm vụ

- **Đầu vào:** phosphosite với accession/vị trí, cửa sổ 15 aa; trình tự miền kinase ứng viên; các thuộc tính được phép sử dụng và có provenance.
- **Đầu ra cơ bản:** score `s(x, k)` và thứ hạng trong một tập kinase ứng viên công bố rõ.
- **Đầu ra mở rộng:** quan hệ được lựa chọn, trọng số và trạng thái ngoài miền; tùy dữ liệu có thể đánh giá hoạt tính kinase từ phosphoproteomics.
- **Đơn vị nhãn:** liên kết vị trí–kinase được chú giải. Không tự coi mọi cặp chưa được chú giải là âm sinh học.
- **Zero-shot nghiêm ngặt:** không dùng nhãn liên kết của kinase test để huấn luyện/chọn model. Dùng motif đã đo cho chính kinase test là một chế độ có thông tin phụ, phải báo riêng.

Ví dụ minh họa: nhập vị trí S123 và danh sách kinase ứng viên; hệ thống trả các kinase có score cao cùng giới hạn mô hình. Đây là **danh sách ưu tiên để kiểm tra**, chưa phải danh sách cơ chất sinh lý xác nhận. Vị trí minh họa không phải kết quả nghiên cứu.

## 3. DARKIN: dữ liệu đã kiểm trực tiếp

### 3.1 Snapshot và tái tạo

**[ĐO]** Checkout `tastanlab/darkin` tại commit `498de014951f962f77ca1b96340fead3cc24c450`, tải ngày 10/10/2026. Script audit dùng thư viện chuẩn Python; SHA-256 từng CSV split được lưu trong JSON. Không đưa bản clone hoặc embedding lên Git.

```bash
python3 topics/dark-kinome-zero-shot/research/darkin-audit/audit_data.py \
  --checkout /path/to/darkin \
  --output topics/dark-kinome-zero-shot/research/darkin-audit/audit-results.json
```

### 3.2 Split mặc định, ZSL seed 12345

| Tập | Dòng phosphosite | Cặp có nhãn | Kinase | Nhãn/kinase: min · median · max |
|---|---:|---:|---:|---|
| Train | 8.559 | 11.473 | 308 | 1 · 6 · 949 |
| Validation | 1.484 | 1.628 | 46 | 10 · 14,5 · 486 |
| Test | 1.414 | 1.615 | 38 | 14 · 26,5 · 213 |

**[ĐO]** Median chính xác là **14,5** và **26,5**, thay vì số làm tròn 15 và 27 trong bản khuyến nghị. `kinase_properties.csv` có 392 kinase duy nhất, không thiếu miền kinase.

### 3.3 Độc lập theo kinase có, độc lập theo substrate chưa có

| Train so với test mặc định | Kết quả audit |
|---|---:|
| Kinase trùng | 0 |
| Key `(SUB_ACC_ID, SUB_MOD_RSD)` trùng | 462 |
| Cửa sổ 15 aa trùng sau chuẩn hóa chữ hoa | 462 |
| Accession substrate trùng | 436 |
| Dòng test thuộc protein có trong train | 923/1.414 ≈ 65,3% |
| Dòng test có cùng key vị trí trong train | 462/1.414 ≈ 32,7% |
| Similarity miền lớn nhất, theo ma trận đi kèm | 89,29% |
| Cặp miền train–test ≥90%, theo ma trận đi kèm | 0 |

**[ĐO]** Đây là overlap của đầu vào substrate, không phải overlap cùng cặp nhãn kinase–vị trí. Không gọi nó là bằng chứng benchmark sai: protocol đang đo kinase mới trên các vị trí có thể đã thấy. Tuy nhiên, không dùng kết quả đó để tuyên bố khái quát đồng thời sang **kinase mới và protein mới**. **[PHÂN TÍCH]**

Audit similarity dùng ma trận tác giả cung cấp, chưa chạy alignment độc lập. Ngưỡng 90% vẫn cho phép quan hệ rất gần dưới ngưỡng; không tương đương phép thử leave-family-out hoặc leave-group-out.

### 3.4 Năm snapshot split trong checkout

| Seed | Dòng test | Cặp test | Kinase test | Min nhãn/kinase test | Key test trùng train |
|---|---:|---:|---:|---:|---:|
| 0 | 1.409 | 1.614 | 40 | 12 | 448 |
| 42 | 1.332 | 1.578 | 40 | 12 | 386 |
| 87 | 1.431 | 1.612 | 39 | 12 | 453 |
| 1001 | 1.111 | 1.266 | 38 | 15 | 376 |
| 12345 | 1.414 | 1.615 | 38 | 14 | 462 |

**[ĐO]** Cả năm có kinase rời nhau giữa train/validation/test. Đây là số thư mục trong checkout, không mặc định trùng số split của mọi bản bài báo/Zenodo. Nhiều split dùng lại dữ liệu và kinase, nên độ lệch chuẩn qua split là mô tả độ nhạy; không tự là CI trên năm nghiên cứu độc lập.

### 3.5 Các dòng cần truy vết

**[ĐO]** Split mặc định có bốn dòng train và một dòng validation có residue trung tâm ngoài S/T/Y:

| Tập | Accession | Vị trí |
|---|---|---|
| Train | P27708 | H1856 |
| Train | P68433 | K14 |
| Train | P04637 | R249 |
| Train | Q15858-3 | I848 |
| Validation | Q02156 | K534 |

Một số seed khác đưa ngoại lệ vào test. Chưa kết luận đây là lỗi: có thể là metadata, mapping hoặc phản ứng khác phạm vi Ser/Thr/Tyr. Phải truy vết dữ liệu gốc. **[ĐỀ XUẤT]** Giữ nguyên snapshot cho tái lập chính thức; làm sensitivity analysis với tiêu chí loại rõ ràng, không sửa raw hoặc âm thầm thay benchmark.

Các kiểm tra chưa thực hiện: mapping toàn bộ site sang FASTA pin, provenance assay từng liên kết, đồng dạng substrate, tỷ lệ kinase thật sự ít nghiên cứu ở benchmark hạ nguồn, quyền phân phối dữ liệu dẫn xuất. Repo công khai không tự chứng minh mọi dữ liệu nguồn có thể tái phân phối.

## 4. Khảo sát nghiên cứu trước theo nhóm phương pháp

### 4.1 Nền benchmark và baseline

**[NGUỒN]** DARKIN dùng cửa sổ 15 aa, dữ liệu liên kết từ PhosphoSitePlus, classifier k-NN/BZSM, và split theo kinase. Test mô phỏng chưa thấy bằng cách giữ lại cả kinase đủ dữ liệu. Bài còn thử fine-tuning, không chỉ frozen embedding. Mốc cao nhất tác giả báo là **0,1911 AP**. [DARKIN, Methods và Results](https://academic.oup.com/bioinformatics/article/41/11/btaf480/8306017).

**[PHÂN TÍCH]** DARKIN vừa là nền dữ liệu vừa là baseline cần so; không thể nói “không phải đối thủ”. Chỉ vượt một cấu hình frozen yếu chưa chứng minh vượt phương pháp đầy đủ.

### 4.2 Mô hình tương tác theo cặp

**[NGUỒN]** Phosformer-ST đã nghiên cứu giải thích và dự đoán kinase ngoài tập assay. Luận văn Pekey 2025 đã có DARKIN-FT, DARKIN-Interact, LoRA và tăng cường bằng atlas/homology. Đã đọc các phần liên quan của luận văn, gồm Chương 3–4 và bảng kết quả; chưa tái lập. [Phosformer-ST](https://pmc.ncbi.nlm.nih.gov/articles/PMC10868336/), [luận văn Pekey, PDF](https://research.sabanciuniv.edu/id/eprint/53625/1/10733682.pdf).

**[PHÂN TÍCH]** Cross-attention/joint attention, fine-tune encoder, thêm motif hoặc tăng dữ liệu đồng dạng đều cần baseline trực tiếp. Luận văn cũng có các thí nghiệm dùng thông tin sinh tổng hợp cho nhiều tập kinase; từng cấu hình phải phân loại theo nguồn thông tin, không gọi tất cả là zero-shot nghiêm ngặt.

### 4.3 Đối thủ mới: COMPASS-PTM

**[NGUỒN]** Bài ngày 15/05/2026 kết hợp dự đoán PTM và gán enzyme, báo **mAP 0,2946** trên DARKIN so với 0,1911 của nghiên cứu gốc; có mã nguồn. Đây là kết quả tác giả, chưa phải mốc tái lập của dự án. [COMPASS-PTM](https://www.nature.com/articles/s41467-026-73148-3), [code](https://github.com/ZhangJJ26/COMPASS-PTM).

**[PHÂN TÍCH]** Bài mô tả mAP theo xếp hạng kinase cho substrate, trong khi audit code gốc cho thấy có AP theo kinase lẫn theo site. Phải kiểm Supplementary S.3.7/code/split trước coi 0,2946 và 0,1911 là hai số đã bảo đảm cùng phép đo. Không kết luận tác giả sai từ khác biệt cách diễn đạt này.

### 4.4 Motif, cấu trúc và context

**[NGUỒN]** Atlas Ser/Thr có 303 kinase; atlas Tyr gồm 78 conventional Tyr kinase và 15 kinase khác có hoạt tính Tyr. Đây là phép đo đặc hiệu peptide, không phải nhãn cơ chế cho mọi liên kết trong tế bào. [Johnson 2023](https://www.nature.com/articles/s41586-022-05575-3), [Yaron-Barir 2024](https://www.nature.com/articles/s41586-024-07407-y).

**[NGUỒN]** KinoPlex, công bố 29/07/2026, đã kết hợp cấu trúc dự đoán, motif và positive-unlabeled learning, có kiểm chứng phosphoproteomics và portal. [KinoPlex](https://www.nature.com/articles/s41587-026-03239-5).

**[PHÂN TÍCH]** “Thêm cấu trúc vào motif” không còn là khác biệt đủ rõ. Cần kiểm hiệu ứng ngoài độ tiếp cận/disorder, nguồn nhãn và phạm vi kinase; thêm annotation có thể mang đáp án test vào model.

### 4.5 Suy luận hoạt tính kinase

**[NGUỒN]** benchmarKIN đã thử thêm quan hệ dự đoán từ Kinase Library và Phosformer; hai cấu hình làm giảm hiệu năng. Mốc AUROC tác giả báo cho thư viện bổ sung lần lượt: Kinase Library 0,58 tumor/0,65 perturbation; Phosformer 0,57/0,65. Không suy ra mọi cách bổ sung đều thất bại. [benchmarKIN, Results và Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12098709/).

**[PHÂN TÍCH]** Khoảng trống cần khảo sát là **khi nào, cho kinase nào và bằng cơ chế nào** nên thêm quan hệ, chứ không phải việc đánh giá hạ nguồn lần đầu. So thư viện phải giữ chung universe kinase và số cơ chất khi thích hợp, để tách lợi ích coverage khỏi lợi ích chất lượng.

### 4.6 Bảng đối thủ và yêu cầu so sánh

| Nhóm | Đối thủ tối thiểu | Ưu điểm | Hạn chế cần kiểm / yêu cầu cho đề tài |
|---|---|---|---|
| Biểu diễn + compatibility | DARKIN k-NN, BZSM, fine-tuned | Protocol công khai, nhiều biểu diễn | Chạy cấu hình đầy đủ, khóa metric và split |
| Tương tác theo cặp | DARKIN-FT/Interact, Phosformer-ST | Học quan hệ giữa kinase và peptide | Audit train overlap, nguồn motif, ứng viên và zero-shot |
| Học PTM rồi gán enzyme | COMPASS-PTM | Đối thủ trực tiếp mới, có kết quả DARKIN | Kiểm nguồn pretraining có nhãn và phép tính AP |
| Motif/cấu trúc | Kinase Library, KinoPlex | Đối chiếu sinh học, thêm context | Phân biệt motif đo của kinase test với dự đoán từ sequence |
| Thư viện + activity inference | benchmarKIN và thư viện curated | Giá trị sử dụng có phép đo | Kiểm phủ kinase ít chú giải, inhibitor specificity, universe chung |

**[CHƯA XÁC MINH]** Chưa đọc đủ SAGEPhos/DeepKinZero/Prot2Token và mọi nghiên cứu 2026; không tuyên bố khảo sát đầy đủ hoặc “chưa ai làm” bất kỳ nhánh nào. SAGEPhos nằm trong danh sách phải đọc; OpenReview trả challenge trong phiên này.

## 5. Đánh giá theo năm tiêu chí của GVHD

Không có trọng số/điểm chuẩn chính thức. Bảng này đánh giá tiềm năng và điều kiện đạt, không chấm thành tích chưa làm.

| Tiêu chí | Đánh giá hiện tại | Đóng góp có thể bảo vệ | Bằng chứng còn cần |
|---|---|---|---|
| 1. Tính mới | **Có tiềm năng, chưa xác lập** | Cơ chế thêm quan hệ khi thiếu chú giải, tách coverage/chất lượng/nhiễu | Survey trực tiếp và khác biệt so Pekey, COMPASS, benchmarKIN |
| 2. Cải tiến phương pháp | **Khá, có điều kiện** | Selection/weighting nhận biết chất lượng và độ dư thừa của quan hệ | Đối chứng cùng ngân sách, ablation, CI và failure analysis |
| 3. Phương pháp mới | **Nền kỹ thuật tốt; novelty chưa chứng minh** | Objective hoặc cơ chế học nhằm giải quyết vấn đề cụ thể | Không chỉ liệt kê PLM, LoRA, attention, conformal |
| 4. XAI | **Thuận lợi hơn đề tài thiếu chuẩn đối chiếu** | Fidelity của attribution và đối chiếu motif độc lập | Không dùng cùng motif để vừa train vừa xác nhận giải thích |
| 5. Ứng dụng/website | **Rõ nhu cầu sử dụng dự kiến** | Ưu tiên kinase/thư viện, provenance, phân tích kết quả | Xác minh nhu cầu người dùng, usability và giới hạn ngoài miền |

Ý nghĩa sinh học chưa giải quyết không tự chứng minh tính mới tin học. Một website có chức năng hợp lý chưa chứng minh đã có người dùng thật. Không kết luận “đạt cả năm mà không cần cược”.

## 6. Ba phương án đóng góp để sinh viên lựa chọn

### A — Ưu tiên: bổ sung thư viện có kiểm soát nhiễu

**[ĐỀ XUẤT]** Model cặp sinh score; module lựa chọn/đặt trọng số cạnh dựa trên độ ổn định qua model, mức mới so thư viện curated và độ dư thừa cơ chất. Module phải học/chọn tham số trên dữ liệu phát triển, không tối ưu trên thí nghiệm hạ nguồn test.

Lý do: thêm quá nhiều cạnh có thể pha loãng tín hiệu, tạo độ chồng lấn thư viện và làm mất khả năng phân biệt kinase. Cần đối chứng ngưỡng score, top-k và cap số cơ chất trước khi dùng module phức tạp.

- **RQ1:** cải tiến model có tăng macro-AP và thứ hạng kinase trên ZSL/GZSL cùng protocol không?
- **RQ2:** lựa chọn/đặt trọng số cạnh có cải thiện nhận diện kinase bị can thiệp so với thêm top-k, ngưỡng score hoặc cạnh ngẫu nhiên không?
- **RQ3:** lợi ích thay đổi thế nào theo mức thiếu chú giải, độ tương đồng kinase và độ dư thừa cơ chất?

Điều kiện chọn A: có đủ kinase/thí nghiệm giao giữa DARKIN, model và benchmark hạ nguồn. Nếu gold standard chỉ phủ kinase phổ biến, chỉ kết luận về **kinase được giả lập thiếu chú giải**. Giấu bớt cạnh của kinase well-studied là thí nghiệm stress test, không thay thế validation dark kinase thật.

### B — Thiếu nhãn và khái quát hai phía

**[ĐỀ XUẤT]** Phân biệt cặp đã chú giải với cặp unknown; nghiên cứu loss/ranking hoặc sampling giảm phạt false negative tiềm ẩn. Đánh giá trên kinase mới, substrate mới và cả hai phía mới.

Điểm mạnh: trả lời trực tiếp nhãn thiếu và độ độc lập. Điểm khó: class prior/giả định chọn dương trong PU khó kiểm; không tự viện dẫn lý thuyết PU như bảo đảm nhãn đúng. KinoPlex là tiền lệ PU cần đối chiếu, dù task khác.

RQ đề xuất: objective mới có cải thiện xếp hạng trên các protocol khó hơn mà không chỉ hưởng lợi từ cặp unknown dễ phân biệt? Khóa sampling và báo sensitivity với false negative, không tạo âm từ thiếu chú giải rồi gọi đó là âm thực nghiệm.

### C — Calibration và tập ứng viên trên kinase mới

**[ĐỀ XUẤT]** Nghiên cứu uncertainty dưới dịch chuyển lớp kinase, đo trade-off coverage/set size và khả năng ưu tiên thí nghiệm.

Điểm mạnh: đóng góp thống kê rõ nếu giải được sampling/coverage. Điểm khó: calibration từ kinase khác không mặc nhiên exchangeable với test; target multi-label thiếu nhãn. Chọn C làm trục chính chỉ khi chốt được đối tượng bảo đảm và nền lý thuyết phù hợp. Hiện chưa đủ cơ sở hứa bảo đảm dark-kinase 90%.

**Khuyến nghị:** chọn một trục chính A hoặc B; XAI và website đi cùng trục đó. C là mở rộng nếu điều kiện hợp lệ. Không gom cả ba thành một đề tài khổng lồ chỉ để mỗi tiêu chí có một tên kỹ thuật.

## 7. Giao thức đánh giá đề xuất

### 7.1 Các mức khái quát

| Protocol | Câu hỏi được đo | Cách sử dụng |
|---|---|---|
| ZSL gốc DARKIN | Kinase mới trong tập ứng viên unseen | Tái lập và so công bố |
| GZSL | Chọn giữa kinase seen lẫn unseen | Gần việc dùng thực tế hơn; tách hai nhóm |
| ZSL + site/protein holdout | Kinase mới và substrate mới | Protocol bổ sung; không so số thẳng với split gốc |
| Leave-family/group-out | Khái quát xa trong không gian kinase | Stress test, đo mất bao nhiêu kinase/site |
| Study/time holdout hạ nguồn | Hoạt tính trên thí nghiệm mới | Kiểm giá trị sử dụng, giữ test khỏi việc chọn thư viện |

Chia theo nhóm sinh học trước fit, công bố số dương còn lại. Báo fold suy giảm coverage, không bỏ fold khó vì score thấp. Đối chứng tái lập giữ raw split, protocol bổ sung pin version riêng.

### 7.2 Hai chiều AP phải tách riêng

**[ĐO MÃ]** `baseline_scripts/aupr_zsl.py` tính AP cho từng kinase trên các site rồi lấy trung bình. `bilinear_zero_shot_model/scripts/evaluation/metrics.py` có cả AP theo kinase và theo row.

Với `Y` kích thước site × kinase và score `S`:

```text
macro_AP_kinase = mean_k AP(Y[:, k], S[:, k])
macro_AP_site   = mean_i AP(Y[i, :], S[i, :])
```

Phép thứ nhất hỏi model xếp các vị trí cho một kinase thế nào; phép thứ hai hỏi model xếp kinase cho một vị trí thế nào. Hai số không thay nhau. Cũng không mặc định AP bằng diện tích PR tính bằng quy tắc hình thang.

**[ĐỀ XUẤT]** Metric chính cho tái lập là đúng AP của code/protocol gốc; sản phẩm nhập site cần thêm site-AP, recall@k/hit@k, nDCG và độ lớn universe. Khi cặp unknown được mã hóa 0 để tính benchmark, gọi là đánh giá so **chú giải hiện có**, không precision sinh học của mọi dự đoán.

### 7.3 Thang baseline và ablation

| Bậc | Cấu hình | Hiệu ứng cần tách |
|---|---|---|
| B0 | Prior, motif/PSSM khi được phép, transfer theo similarity kinase | Độ khó và lợi ích thông tin phụ |
| B1 | k-NN/BZSM gốc + cấu hình fine-tuned | Mốc tái lập đầy đủ |
| B2 | Frozen PLM + đầu đơn giản | Lợi ích biểu diễn |
| B3 | DARKIN-FT/Interact; COMPASS khi tái lập được | Đối thủ trực tiếp mạnh |
| B4 | Cùng model, ngưỡng/top-k/cap cạnh | Lợi ích selection đơn giản |
| B5 | Cơ chế mới, thêm từng thành phần | Cải tiến phương pháp thật |

Hạ nguồn cần curated-only, curated + random edges khớp số lượng, curated + top-k, curated + threshold, curated + selection mới; đối chứng cạnh giữ phân bố bậc khi thích hợp. So model cùng tập ứng viên và nguồn dữ liệu được phép, không dùng atlas của test cho một phía rồi gọi chênh lệch là cải tiến encoder.

### 7.4 Kiểm soát nguồn thông tin

- Tách pretraining không nhãn trình tự khỏi pretraining có nhãn liên kết/PTM có thể chứa test.
- Khóa danh sách kinase, enzyme annotations, PPI và motif theo nguồn/version; audit external overlap.
- Chọn model/ngưỡng/module cạnh trên validation; mọi tuning activity inference dùng study phát triển riêng.
- Kiểm casing trong peptide: các chữ thường có thể mang thông tin PTM khác; công bố giữ hay chuẩn hóa và ablation.
- Cặp mới, kinase mới, site mới, protein mới và nguồn thực nghiệm mới là các mức độc lập khác nhau.

### 7.5 Metric hạ nguồn và độ bất định

**[ĐỀ XUẤT]** Dùng rank kinase bị can thiệp, hit@k, AUROC/AP chỉ khi nhãn nền và universe có căn cứ. Báo số kinase/thí nghiệm phủ được, kết quả trên universe giao chung và kết quả coverage mở rộng riêng. Tách can thiệp gene khỏi inhibitor đa đích; thí nghiệm inhibitor không tự xác nhận liên kết trực tiếp.

Bootstrap ghép cặp theo thí nghiệm/nghiên cứu cho hạ nguồn; theo protein/kinase thích hợp cho site-level. Báo phân bố qua split và seed fit riêng. Không coi hàng nghìn site là hàng nghìn lần lặp sinh học độc lập. Không chọn ngưỡng hiệu ứng “đạt” sau khi nhìn test; xác định effect size và độ chính xác CI trước thí nghiệm chính.

## 8. XAI: kiểm cả fidelity và ý nghĩa sinh học

**[ĐỀ XUẤT]** Attribution/occlusion trên peptide và residue miền kinase, với các kiểm tra sau:

1. Giữ vị trí trung tâm phù hợp task; perturbation có nền matched, tránh chỉ dùng mask ngoài phân phối.
2. Đo thay đổi score/thứ hạng khi bỏ/thay residue được giải thích là quan trọng; so residue ngẫu nhiên.
3. Randomize trọng số/nhãn rồi kiểm giải thích có đổi; kiểm độ ổn định theo seed/fold.
4. Đối chiếu motif atlas trên phần **không dùng để train/tune**, hoặc kinetics/mutagenesis độc lập khi có.
5. So với baseline PSSM để biết model chỉ học lại motif hay có thông tin bổ sung.

Khớp motif hỗ trợ plausibility sinh học; thay score theo attribution hỗ trợ fidelity model. Cả hai chưa chứng minh nguyên nhân trong tế bào. Attention map không tự là lời giải thích trung thực. Cơ sở sanity check: [Adebayo và cộng sự, 2018](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html).

Nếu dùng toàn bộ atlas làm auxiliary target, không trình bày agreement trên cùng atlas là validation độc lập. Motif tự dựng từ train là mô tả dữ liệu, không thay thế ground truth ngoài.

## 9. Conformal: định nghĩa trước lời hứa

Conformal cần điều kiện sampling/calibration; zero-shot của encoder không tự cho bảo đảm trên các lớp kinase mới. [Conformal beyond exchangeability](https://arxiv.org/abs/2202.13415). Nghiên cứu conformal cho zero-shot model như CLIP là tiền lệ kỹ thuật, không phải định lý sẵn cho split lớp và nhãn thiếu của DARKIN. [Silva-Rodríguez và cộng sự, CVPR 2025](https://arxiv.org/abs/2505.24693).

| Mục tiêu | Điều cần xác định |
|---|---|
| Chứa ≥1 kinase được chú giải | Cách lấy nhãn/site, candidate universe, nonconformity score |
| Chứa mọi kinase được chú giải | Coverage toàn tập multi-label; không đồng nhất với mục trên |
| Chứa mọi kinase thực sự tác động | Chưa có ground truth đầy đủ để kiểm |
| Coverage cho kinase đích | Calibration đích hoặc lý thuyết chuyển phù hợp; có thể đổi chế độ zero-shot |
| Coverage qua quần thể kinase mới | Mô hình sampling kinase và xử lý phụ thuộc site; cần nền thống kê riêng |

**[ĐỀ XUẤT]** Nếu chưa thiết lập điều kiện, chỉ báo empirical coverage với CI, set size, tỷ lệ set vô dụng và failure theo nhóm. Không gọi coverage đã đo là bảo đảm phân phối. Tập chứa tất cả kinase trivially có coverage cao nhưng không giúp thiết kế thí nghiệm; kiểm utility là bắt buộc.

Calibration bằng nhãn của kinase test có thể giữ model frozen nhưng không còn chế độ “không dùng nhãn đích” của toàn hệ thống. Báo riêng few-label target calibration. 90% coverage biên không có nghĩa mỗi gợi ý kinase đúng 90% hoặc mọi kinase có cùng coverage.

## 10. Website và giá trị sử dụng

**[ĐỀ XUẤT]** Người dùng dự kiến là nhà nghiên cứu cần ưu tiên kinase để kiểm tra hoặc phân tích phosphoproteomics. Chưa phỏng vấn hoặc xác nhận nhu cầu người dùng trong phiên này.

Hai luồng sản phẩm:

- **Một site:** nhập accession/vị trí hoặc peptide, chọn kinase universe; xem thứ hạng, motif/attribution, provenance và trạng thái ngoài miền.
- **Một thí nghiệm:** tải bảng phosphosite và log-fold-change; chọn thư viện curated/predicted, xem thay đổi rank hoạt tính và độ phủ cơ chất, tải kết quả.

Ứng dụng phải phân biệt liên kết curated, dự đoán, unknown và kết quả activity inference. Không hiển thị score chưa calibrate như xác suất; không gọi kết quả “cơ chất xác nhận”. Protein input cần mapping/version và residue check. Không suy rằng một kinase có score thấp là không tác động trong mọi bối cảnh.

Đánh giá sản phẩm: độ chính xác mapping và tái tạo kết quả batch, thời gian/tỷ lệ hoàn thành tác vụ, khả năng người dùng hiểu giới hạn và truy nguyên bằng chứng. Website là tiêu chí riêng; giao diện đẹp chưa chứng minh đóng góp phương pháp.

## 11. Đính chính bản khuyến nghị ban đầu

| Phát biểu cũ | Kết luận cập nhật |
|---|---|
| Baseline chỉ k-NN/bilinear đơn giản | Bài DARKIN còn có fine-tuning; có DARKIN-Interact và COMPASS |
| Attention theo cặp/motif là khoảng trống rõ | Đã có tiền lệ trực tiếp; cần khác biệt cụ thể |
| Kiểm chứng thư viện dự đoán hạ nguồn chưa ai làm | benchmarKIN đã thử; nhánh zero-shot riêng cần kiểm thêm |
| Motif là ground truth của XAI | Là đối chiếu đặc hiệu assay; fidelity cần kiểm riêng |
| Tập ứng viên bảo đảm 90% cho dark kinase | Chưa có thiết kế calibration/định lý hỗ trợ lời hứa |
| Benchmark đã kiểm soát đồng dạng nên độc lập đầy đủ | Có cutoff phía kinase; site/protein overlap còn lớn |
| Năm split cho CI độc lập | Là các phép chia dữ liệu liên quan; cần inference theo đơn vị phù hợp |
| Tối thiểu 14 site nên chỉ số từng kinase vững | Chỉ đúng min split mặc định; các split khác min 12; vẫn cần CI |
| Phải có GPU mới có cải tiến phương pháp | Frozen encoder vẫn có thể có objective/selection mới; tài nguyên không quyết định novelty |
| Đạt cả năm tiêu chí không cần cược | Mới là tiềm năng; tính mới và hiệu quả chưa chứng minh |

## 12. Cổng quyết định và việc tiếp theo

| Cổng | Bằng chứng cần có | Trạng thái hiện tại |
|---|---|---|
| Dữ liệu nền | Snapshot, count, disjoint kinase, overlap, ngoại lệ | **Đạt audit sơ bộ**, chưa mapping/provenance đầy đủ |
| Đối thủ | Full method, metric/split và nguồn nhãn của đối thủ gần nhất | **Một phần**; thêm SAGEPhos, Supplementary COMPASS và code cần đọc |
| Tính mới | Bảng khác biệt cụ thể và giả thuyết có thể bác bỏ | **Chưa chốt**; A/B là phương án đề xuất |
| Hạ nguồn | Giao kinase/thí nghiệm đủ thông tin, gold standard có giới hạn rõ | **Chưa audit file trực tiếp** |
| Baseline | Tái lập metric/code và score trên split pin | **Chưa chạy** |
| XAI | Thiết kế fidelity và đối chiếu độc lập | **Có thiết kế**, chưa thực nghiệm |
| Conformal | Đối tượng coverage, sampling/calibration và utility | **Chưa đạt**, không cam kết |
| Sản phẩm | Tác vụ, người dùng, provenance và validation | **Có đặc tả dự kiến**, chưa triển khai |

Thứ tự thực hiện đề xuất, không gán thời hạn:

1. Audit metric/split của DARKIN-Interact và COMPASS, nguồn pretraining/atlas và license dữ liệu.
2. Tải/kiểm benchmark hạ nguồn: đếm kinase giao, nghiên cứu độc lập, mức thiếu chú giải; chọn A nếu câu hỏi trả lời được, nếu không xem B.
3. Pin mapping/FASTA và xử lý ngoại lệ; khóa protocol gốc và protocol bổ sung, nguồn dữ liệu được phép.
4. Sau khi sinh viên yêu cầu thực nghiệm: tái lập baseline; kiểm khoảng trống định lượng; khóa RQ/objective/ablation.
5. Chạy đối chứng, phân tích thất bại và XAI; chỉ thêm conformal khi cổng tương ứng đạt.
6. Triển khai website từ endpoint đã xác minh, đánh giá tác vụ sử dụng.

Tên đề tài chưa gắn kiến trúc, để tránh chốt kỹ thuật trước bằng chứng: **“Dự đoán liên kết kinase–phosphosite cho kinase chưa thấy và đánh giá giá trị bổ sung thư viện cơ chất trong suy luận hoạt tính kinase.”** Nếu chọn A và thực nghiệm hỗ trợ, bổ sung cụm “với cơ chế kiểm soát nhiễu”; nếu chọn B, đổi tên quanh nhãn thiếu/khái quát hóa. Chưa có đề tài được duyệt hoặc kết quả vượt baseline.

## 13. Hồ sơ nguồn và giới hạn khảo sát

Nguồn trực tiếp đã truy cập: DARKIN bài/repo, luận văn Pekey (các phần liên quan), benchmarKIN, COMPASS-PTM, atlas kinase và trang KinoPlex. Phosformer-ST có đoạn nguồn tìm kiếm nhưng PMC trả challenge khi mở; SAGEPhos/OpenReview trả challenge. Ghi rõ đây là hạn chế truy cập, không là bằng chứng nghiên cứu không tồn tại.

Các số công bố chưa chạy lại. Audit CSV/mã gốc không phải thực nghiệm model, assay sinh học hoặc validation cellular. [Hồ sơ nguồn, commit, đường dẫn mã và lệnh tái tạo](darkin-audit/README.md) phân biệt bằng chứng nội bộ với kết quả tác giả. Bản khuyến nghị ban đầu được giữ làm lịch sử, có cảnh báo dẫn tới báo cáo này.
