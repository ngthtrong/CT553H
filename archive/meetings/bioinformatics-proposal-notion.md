# Đề tài tin sinh: một đề xuất chính và một dự phòng

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../DECISIONS.md).

> **Trạng thái:** bản chuẩn bị cho buổi gặp GVHD sáng 02/10/2026. Đề tài **chưa chốt**.
> Trang này thay cho [bản so sánh ba hướng](bioinformatics-topic-ideas-notion.md) trước đó: hướng IL-6 đã bị loại, và hai hướng còn lại đã được viết lại cho rõ phần đóng góp.
> Chi tiết đầy đủ kèm câu hỏi cho GVHD: [session-01-prep.md](../../project/meetings/2026-10-02-session-01/prep.md).

## Quyết định đã làm và lý do

Ba hướng trong bản trước thật ra chia nhau **một** câu hỏi nghiên cứu ("truy hồi giúp bao nhiêu, và lợi ích có phụ thuộc độ tương đồng láng giềng không") áp lên ba bộ dữ liệu khác nhau. Vì vậy việc cần quyết không phải là chọn bài toán sinh học, mà là chọn nơi đặt đóng góp và chọn bộ dữ liệu cho câu hỏi đó chạy rẻ nhất.

- **Nơi đặt đóng góp:** chất lượng đánh giá, không phải kiến trúc mới. Với một người, nền sinh học cơ bản và GPU miễn phí, đây là chỗ rẻ nhất để làm tốt.
- **Bộ dữ liệu:** ATP ở receptor tyrosine kinase. Dữ liệu có sẵn, có giấy phép, và đầu ra theo từng residue cho một sản phẩm trực quan.
- **Loại bỏ IL-6:** dữ liệu công khai không có tập test độc lập, và [CONTRA-IL6 (2026)](https://pubmed.ncbi.nlm.nih.gov/42281397/) đã báo cáo kiểm tra trên bộ độc lập, nên tính mới mỏng nhất trong ba hướng.

## Đề xuất chính: vị trí gắn ATP dưới giao thức chống rò rỉ

**Tên làm việc:** Truy hồi cho dự đoán residue gắn ATP dưới giao thức chống rò rỉ — ngưỡng chọn trên validation, AUPRC, và quy tắc từ chối dự đoán theo độ tương đồng láng giềng.

### Vấn đề sinh học

ATP là phân tử mang năng lượng tham gia nhiều phản ứng của protein. Dự đoán residue nào trong protein kinase gắn ATP giúp nghiên cứu chức năng protein và khảo sát vùng đích của thuốc. Hướng hẹp ở đây là họ receptor tyrosine kinase (RTK). Phần sinh học đã được mã hóa sẵn trong benchmark: nhãn "gắn / không gắn" cho từng residue đã có trong bộ dữ liệu, nên công việc chính là học máy và phương pháp đánh giá.

### Vì sao còn chỗ cho đóng góp

Ba điểm dưới đây là **nhận xét phương pháp**, không phải cáo buộc, và đều kiểm chứng được từ tài liệu công khai. Chưa có kết luận nào về việc đây có phải phiên bản tạo ra số liệu trong bài báo hay không.

1. **Ngưỡng quyết định chọn trên chính tập đang chấm.** Hàm `model_test` trong notebook công khai của RTK_RAG dùng `roc_curve` trên `y_test`, lấy `argmax` của G-mean, rồi tính MCC và F1 trên cùng nhãn đó. Cách chuẩn là chọn ngưỡng trên validation rồi khóa lại trước khi chấm test.
2. **Chỉ số không phù hợp với dữ liệu mất cân bằng.** Tập test RTK có 711 residue gắn trên 73.270 residue không gắn, tức khoảng 0,96% dương. Ở mức đó, accuracy và specificity trên 0,98 đạt được gần như tầm thường, và AUC sát trần không còn phân biệt được các mô hình. [LMetalSite](https://academic.oup.com/bib/article/23/6/bbac444/6770088) chọn AUPR làm chỉ số chính đúng vì lý do này.
3. **Lọc đồng dạng lỏng và kho truy hồi cùng một họ.** CD-HIT 40% lỏng hơn chuẩn 25–30% thường dùng trong lĩnh vực, và kho truy hồi gồm 244 protein đều thuộc họ RTK. Câu hỏi "một RTK mới có luôn tìm được láng giềng đủ gần hay không" chưa được trả lời.

### Ba câu hỏi nghiên cứu

| | Câu hỏi | Cách đo |
|---|---|---|
| **RQ1** | Dưới giao thức sạch (kho truy hồi tách khỏi test ở ≤30% identity, ngưỡng chọn trên validation, test giữ tỉ lệ dương tự nhiên), truy hồi còn đóng góp bao nhiêu so với cùng PLM và mCNN không truy hồi? | ΔAUPRC và ΔMCC, khoảng tin cậy 95% bootstrap **theo protein**, ít nhất 5 seed |
| **RQ2** | Mỗi lựa chọn đánh giá đóng góp bao nhiêu điểm vào chỉ số: (a) ngưỡng chọn trên test thay vì validation, (b) CD-HIT 40% so với 30%, (c) kho truy hồi cùng họ RTK so với kho đa dạng hơn? | (a) Giữ nguyên điểm dự đoán và chỉ đổi ngưỡng: chỉ MCC, F1 và G-mean thay đổi, AUPRC và AUROC không đổi. (b) và (c) có thiết kế so sánh riêng |
| **RQ3** | **Phần mới.** Chỉ dự đoán khi identity của láng giềng gần nhất đạt ngưỡng *t*: quy tắc từ chối dự đoán này có cải thiện độ tin cậy trên protein không có láng giềng gần? | Đường coverage–AUPRC khi quét *t*, so với dự đoán toàn phần |

RQ3 vừa là phần thiết kế mới, vừa là phần sinh ra sản phẩm. Nếu phải cắt vì thời gian thì cắt nhánh (b) của RQ2 trước, không cắt RQ3.

### Dữ liệu và baseline

- **Dữ liệu:** 549 protein huấn luyện, 69 protein RTK làm test độc lập, kho truy hồi 244 protein — từ [repo RTK_RAG](https://github.com/B1607/RTK_RAG), repo duy nhất của nhóm có giấy phép (Academic Free License v3.0). **Cộng thêm** bộ ATP-388 / ATP-41 / ATP-17 làm tập ngoài nhóm, để chữa điểm yếu lớn nhất của bộ gốc: với 69 protein và 711 residue dương thì khoảng tin cậy sẽ rất rộng.
- **Baseline:** (1) ProtTrans + mCNN không truy hồi; (2) truy hồi trộn trung bình α = 0,7 như bản của nhóm; (3) **bộ phân loại k-NN thuần trên embedding** — baseline quan trọng nhất, vì nếu k-NN thuần gần bằng mô hình đầy đủ thì phần lớn tín hiệu chỉ là tương đồng chuỗi; (4) số công bố của RTK_RAG làm mốc tham chiếu.
- **Chỉ số:** AUPRC là chính; MCC và F1 tại ngưỡng chọn trên validation; AUROC để đối chiếu với bài gốc.
- **Tính toán:** embedding ProtTrans cho khoảng 900–1.300 protein dưới 2 giờ GPU; mỗi lần huấn luyện mCNN vài phút; toàn bộ trong khoảng 30–60 giờ GPU. Nút thắt là dung lượng đĩa, nên lưu embedding theo residue một lần rồi cắt cửa sổ trong lúc huấn luyện.

### Sản phẩm

Trang web nhận chuỗi FASTA, kiểm tra định dạng, rồi trả về:

- chuỗi axit amin tô màu theo điểm dự đoán của từng residue;
- identity của láng giềng gần nhất trong kho truy hồi, kèm cờ **"ngoài vùng tin cậy"** khi identity dưới ngưỡng *t* của RQ3;
- bảng điểm theo residue tải xuống được, kèm vài chuỗi tham chiếu gần nhất.

Cờ tin cậy là RQ3 hiện ra thành tính năng, không phải giao diện trang trí. Chưa có công cụ nào trong dòng bài này báo tín hiệu đó cho người dùng. Không dựng mô hình 3D.

### Kế hoạch và cổng dừng

| Giai đoạn | Việc chính | Cổng quyết định |
|---|---|---|
| G1 · 20% thời gian | Kiểm tra dữ liệu, nhãn, giấy phép; đo thời gian embedding thật; dựng baseline không truy hồi | Tái lập baseline trong ±0,05 MCC. Không đạt thì chuyển sang hướng dự phòng |
| G2 · 25% | Khóa phép chia, dựng giao thức sạch, chạy RQ1 | ΔAUPRC có vượt dao động giữa các seed hay không |
| G3 · 25% | RQ2 ablation và RQ3 quy tắc từ chối dự đoán | RQ3 không có tín hiệu thì thu hẹp thành benchmark và giao thức |
| G4 · 20% | Xây công cụ web từ mô hình đã huấn luyện | Chạy được từ đầu đến cuối trên một chuỗi mới |
| G5 · 10% | Viết báo cáo, slide, ghi rõ giới hạn | — |

Số tuần thực tế chờ GVHD xác nhận mốc nộp, nên các mốc trên ghi theo phần trăm thời gian.

### Rủi ro và kết quả xấu nhất

- **Rủi ro số một:** repo RTK_RAG không chứa mã dựng đặc trưng RAG (`rag_prottrans_GPU.py` nằm trong một tệp zip trên server không phản hồi). Nếu không xin được từ GVHD thì vẫn làm được, nhưng mất khả năng so trực tiếp với số trong bài.
- **Rủi ro thứ hai:** tập test nhỏ và rất lệch, nên khoảng tin cậy có thể rộng. Giảm nhẹ bằng bootstrap theo protein và bằng tập ATP ngoài nhóm.
- **Kết quả xấu nhất vẫn bảo vệ được:** nếu truy hồi không còn giúp dưới giao thức sạch, luận văn vẫn có một giao thức đánh giá chống rò rỉ, một kết quả âm có kiểm soát kèm khoảng tin cậy, và một công cụ báo tín hiệu tin cậy. Điều này chỉ đúng nếu GVHD và hội đồng chấp nhận dạng luận văn đó — nên đó là câu hỏi phải hỏi ngay buổi đầu.

## Đề xuất dự phòng: phân loại họ protein efflux

**Tên làm việc:** Tăng cường dữ liệu bằng chuỗi sinh so với các cách xử lý mất cân bằng rẻ hơn, cho phân loại siêu họ protein efflux — một so sánh có kiểm soát rò rỉ.

Protein efflux giúp tế bào đưa một số chất ra ngoài; một số hệ vận chuyển liên quan đến khả năng kháng thuốc của vi khuẩn. Hướng này so sánh tăng cường dữ liệu bằng chuỗi ProtGPT2 với class weighting, focal loss, SMOTE trên embedding và mixup, dưới phép chia theo cụm MMseqs2 30%, và báo cáo chất lượng theo từng họ hiếm thay vì chỉ độ chính xác chung.

Đây là phần mở rộng đúng hai hạn chế mà bài [mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595) tự nêu, nên là hướng an toàn nhất về quan hệ thầy–trò. Một đối chứng âm đáng làm: [Shen et al. 2021](https://www.biorxiv.org/content/10.1101/2021.02.18.431877v1.full) cho thấy ngay cả chuỗi bị xáo trộn đôi khi vẫn làm tăng chỉ số, nên mức tăng từ chuỗi sinh tự nó chưa chứng minh chuỗi đó hợp lý về sinh học.

**Hai điều phải nói thật:** chưa tìm được bảng công khai xác nhận số chuỗi mỗi họ — [DeepEfflux](https://academic.oup.com/bioinformatics/article/34/18/3111/4970514) ghi lớp SMR chỉ 15 chuỗi, nên lớp hiếm có thể không đủ cụm để chia fold; và chi phí fine-tune ProtGPT2 chưa đo được. Vì vậy hướng này chỉ chốt được nếu GVHD chia sẻ bộ dữ liệu và cách chia tập của GenEfflux.

## So sánh hai hướng

| | Chính — ATP | Dự phòng — efflux |
|---|---|---|
| Bài toán | Dự đoán residue gắn ATP ở protein kinase | Phân loại protein efflux theo siêu họ |
| Đóng góp đề xuất | Giao thức đánh giá chống rò rỉ + quy tắc từ chối dự đoán | So sánh có kiểm soát giữa tăng cường sinh và xử lý mất cân bằng rẻ |
| Dữ liệu | Có sẵn và có giấy phép, cộng tập ATP ngoài nhóm | Phụ thuộc GVHD chia sẻ, hoặc dựng lại từ TCDB |
| GPU | Thấp nhất, khoảng 30–60 giờ | Trung bình đến cao, 80–150 giờ, chưa đo |
| Sản phẩm | Bản đồ residue kèm cờ tin cậy | FASTA → điểm theo họ, kèm cảnh báo khi không phân biệt được |
| Rủi ro chính | Repo không chứa mã dựng đặc trưng RAG | Lớp hiếm quá nhỏ, khoảng tin cậy rất rộng |
| Mở ra bằng | Xin mã và trọng số RTK_RAG | Đúng một câu hỏi về bộ GenEfflux |

## Cần GVHD trả lời

1. Hai hướng này, hướng nào gần chuyên môn và lịch hướng dẫn hơn?
2. Nếu đóng góp là **giao thức đánh giá và một quy tắc từ chối dự đoán**, chứ không phải một kiến trúc mới, như vậy đã đủ cho luận văn chưa, hay hội đồng sẽ đòi thêm một thành phần mô hình mới?
3. Nếu kết quả cuối là "truy hồi không giúp dưới giao thức chặt" — một kết quả âm có kiểm soát — thầy và hội đồng có chấp nhận không?
4. Có mã dựng đặc trưng RAG, trọng số mô hình, hoặc embedding đã trích của RTK_RAG không?
5. Có chia sẻ được bộ dữ liệu và cách chia tập của GenEfflux không?
6. Tỷ lệ nghiên cứu so với hệ thống của học phần; lớp hệ thống cần dày tới đâu để hội đồng chấp nhận?
7. Số tuần thực tế, mốc nộp, và nguồn GPU có thể dùng?

## Nguồn

- **ATP / RTK:** [bài RTK_RAG trên PubMed](https://pubmed.ncbi.nlm.nih.gov/40531492/) · [repo và README dữ liệu](https://github.com/B1607/RTK_RAG) · [bộ ATP-388/41/17](https://pmc.ncbi.nlm.nih.gov/articles/PMC13073818/)
- **Chỉ số cho dữ liệu mất cân bằng:** [LMetalSite, Brief Bioinform 2022](https://academic.oup.com/bib/article/23/6/bbac444/6770088)
- **Efflux:** [mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595) · [DeepEfflux](https://academic.oup.com/bioinformatics/article/34/18/3111/4970514) · [Shen et al. 2021](https://www.biorxiv.org/content/10.1101/2021.02.18.431877v1.full)
- **Rò rỉ dữ liệu trong ML:** [Kapoor & Narayanan, Patterns 2023](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9) · [Bernett et al. 2024](https://academic.oup.com/bib/article/25/2/bbae076/7621029)
- Khảo sát nội bộ đầy đủ: `archive/surveys/bioinformatics-topic-survey/bioinformatics-topic-survey.md`
