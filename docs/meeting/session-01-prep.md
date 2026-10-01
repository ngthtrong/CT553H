# Chuẩn bị buổi gặp GVHD lần 1 — hướng tin sinh học

> **Lưu ý cập nhật sau:** người dùng đã xác nhận một người/14 tuần và muốn ưu tiên phát triển ứng dụng/hệ thống. Xem [bản trao đổi mới](bioinformatics-application-pitch.md) và [khảo sát mới](../common/deep-research/reports/bioinformatics-application-topics.md). Nội dung ATP bên dưới là phương án trước đó, chưa được chốt.

> Cập nhật: 01/10/2026. Buổi gặp: **sáng 02/10/2026**. Đề tài **chưa chốt**.
> Mang **hai** hướng: đề xuất chính (ATP + giao thức đánh giá) và dự phòng (efflux). Đi với tâm thế để thầy phản biện và chọn.
> Nguồn: [khảo sát sâu](../common/deep-research/reports/bioinformatics-topic-survey.md) · [trang so sánh ba hướng](bioinformatics-topic-ideas-notion.md) · [kiểm chứng RAG-msCNN](../common/deep-research/reports/rag-mscnn-verification.md)
>
> **Không nêu trong buổi này:** phát hiện ở mục 3.1 của bản khảo sát (kịch bản RAG-msCNN bản 07/2025 chỉ áp truy hồi cho residue có nhãn dương). Hai lý do: bản thân chưa tự đọc hết bằng chứng, và buổi gặp đầu tiên không phải chỗ đặt vấn đề tái lập bài của thầy. Nếu sau này muốn nêu, làm theo mục 3.3 của bản khảo sát: nói riêng, dạng câu hỏi tái lập.

## Mục tiêu buổi gặp

1. Thầy chọn hoặc điều chỉnh giữa hai hướng; biết hướng nào gần chuyên môn và lịch của thầy hơn.
2. Biết kỳ vọng của học phần: tỷ lệ nghiên cứu so với hệ thống, và **luận văn dạng “giao thức đánh giá + kết quả có thể âm” có được chấp nhận hay không**. Đây là câu hỏi quyết định của cả hai hướng.
3. Mở ba nút chặn tài nguyên: mã dựng đặc trưng RAG của RTK_RAG, bộ dữ liệu GenEfflux, và nguồn GPU thực tế.
4. Thống nhất cách làm việc: tần suất gặp, kênh liên lạc, mốc nộp.

## Làm trước buổi gặp (tối nay, khoảng 45 phút)

- [x] Trợ lý đã tải và đọc notebook RTK_RAG: xác nhận `model_test` chọn ngưỡng G-mean bằng nhãn của chính tập đang chấm. [Bằng chứng, vị trí mã và giới hạn](../common/deep-research/reports/rtk-rag-threshold-verification.md).
- [ ] **Người trình bày tự mở lại** [notebook tại commit đã kiểm](https://github.com/B1607/RTK_RAG/blob/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627/CODE/MCNN_npy.ipynb), tìm `def model_test` ở ô thứ 10 (`In [6]`), đọc `roc_curve(y_test...)` → `np.argmax(gmeans)` → `confusion_matrix(y_test...)`. Bằng chứng này hỗ trợ nhánh (a) của RQ2; chưa chứng minh cách tạo mọi số liệu trong bài báo.
- [ ] Đọc README RTK_RAG, xác nhận lại các số sẽ nói: 549 protein train, 69 protein RTK test độc lập, 244 protein trong kho truy hồi, 711 residue dương / 73.270 âm (≈0,96%).
- [ ] Xem banner quota trong tài khoản Kaggle (30 h/tuần hay khác) — để trả lời được khi thầy hỏi về GPU.
- [ ] Thử tải bộ ATP-388/ATP-41/ATP-17 ([PMC13073818](https://pmc.ncbi.nlm.nih.gov/articles/PMC13073818/)). Nếu tải được, tập test ngoài nhóm là chắc chắn; nếu không, nói rõ đây là việc của tuần 1.
- [ ] In một trang: bảng “Hai hướng mang ra trao đổi” + ba RQ của hướng chính.

## Hai hướng mang ra trao đổi

| | **Chính — ATP** | **Dự phòng — efflux** |
|---|---|---|
| Bài toán | Dự đoán residue gắn ATP ở protein kinase | Phân loại protein efflux theo siêu họ |
| Đóng góp đề xuất | Giao thức đánh giá chống rò rỉ + quy tắc từ chối dự đoán theo độ tương đồng | So sánh có kiểm soát: tăng cường bằng chuỗi sinh so với các cách xử lý mất cân bằng rẻ |
| Dữ liệu | Có sẵn và **có giấy phép** (RTK_RAG, AFL v3.0) + tập ATP ngoài nhóm | **Phụ thuộc thầy** chia sẻ bộ GenEfflux, hoặc phải dựng lại từ TCDB |
| GPU | Thấp nhất (<2 giờ embedding, train vài phút/lần) | Trung bình–cao, chi phí fine-tune ProtGPT2 chưa đo |
| Sản phẩm | Bản đồ residue + cờ tin cậy — trực quan nhất | FASTA → điểm theo họ + cảnh báo khi không phân biệt được |
| Rủi ro chính | Repo không chứa mã dựng đặc trưng RAG | Lớp SMR chỉ 15–18 chuỗi, khoảng tin cậy rất rộng |
| Mở ra bằng | Xin mã/trọng số RTK_RAG | **Đúng một câu hỏi**: thầy chia sẻ được bộ GenEfflux không |

Hướng IL-6 peptide đã bỏ khỏi danh sách: dữ liệu công khai không có tập test độc lập, và [CONTRA-IL6 (2026)](https://pubmed.ncbi.nlm.nih.gov/42281397/) đã báo cáo kiểm tra trên bộ độc lập nên tính mới mỏng nhất trong ba hướng. Nếu thầy hỏi, trả lời đúng như vậy.

## Đề xuất chính: ATP + giao thức đánh giá chống rò rỉ

**Tên làm việc:** Truy hồi cho dự đoán residue gắn ATP dưới giao thức chống rò rỉ: ngưỡng chọn trên validation, AUPRC, và quy tắc từ chối dự đoán theo độ tương đồng láng giềng.

### Vì sao còn chỗ cho đóng góp (ba điểm tự kiểm chứng được, không phải cáo buộc)

1. **Hàm đánh giá công khai chọn ngưỡng trên chính tập đang chấm.** Đã đọc trực tiếp `model_test` trong notebook RTK_RAG: `roc_curve` dùng `y_test`, chọn `argmax(gmeans)`, rồi tính MCC/F1 trên cùng nhãn đó. Nhánh cross dùng fold giữ lại; nhánh independent có cùng lời gọi nhưng không lưu output. Mã/output có điểm không đồng bộ và thiếu module nạp dữ liệu, nên chưa kết luận đây là phiên bản tạo số liệu bài báo. Đề xuất chọn ngưỡng trên validation rồi khóa trước khi chấm test. [Vị trí mã, giới hạn và câu trả lời khi thầy hỏi](../common/deep-research/reports/rtk-rag-threshold-verification.md).
2. **Chỉ số không phù hợp với dữ liệu mất cân bằng.** Tập test RTK chỉ có ≈0,96% residue dương. Ở mức đó, accuracy và specificity ≥0,98 đạt được gần như tầm thường, và AUC sát trần không còn phân biệt được các mô hình. [LMetalSite](https://academic.oup.com/bib/article/23/6/bbac444/6770088) chọn AUPR làm chỉ số chính đúng vì lý do này.
3. **Lọc đồng dạng lỏng và kho truy hồi cùng họ.** CD-HIT 40% chạy chung một lần lỏng hơn chuẩn 25–30% thường dùng, và kho truy hồi gồm 244 protein cùng họ RTK. Câu hỏi “một RTK mới có luôn tìm được láng giềng đủ gần hay không” chưa được trả lời.

### Ba câu hỏi nghiên cứu

| | Nội dung | Cách đo |
|---|---|---|
| **RQ1** | Dưới giao thức sạch (kho truy hồi tách khỏi test ở ≤30% identity, ngưỡng chọn trên validation, test giữ tỉ lệ dương tự nhiên), truy hồi còn đóng góp bao nhiêu so với cùng PLM + mCNN không truy hồi? | ΔAUPRC và ΔMCC, khoảng tin cậy 95% **bootstrap theo protein** (không coi mỗi residue là một quan sát độc lập), ≥5 seed |
| **RQ2** | Mỗi lựa chọn đánh giá đóng góp bao nhiêu điểm vào chỉ số: (a) chọn ngưỡng trên test thay vì validation, (b) CD-HIT 40% so với 30%, (c) kho truy hồi cùng họ RTK so với kho đa dạng hơn? | (a) Giữ nguyên điểm dự đoán, đo ΔMCC/ΔF1/G-mean; AUPRC và AUROC không đổi khi chỉ đổi ngưỡng. (b)/(c) Đo ΔAUPRC/ΔMCC với thiết kế so sánh riêng. Xáo nhãn kho chỉ là đối chứng có tác dụng nếu phương pháp thực sự dùng nhãn kho; với trộn embedding không nhãn, dùng kho ngẫu nhiên cùng kích thước để kiểm tra vai trò chọn láng giềng. |
| **RQ3** | Quy tắc **từ chối dự đoán**: chỉ dự đoán khi identity của láng giềng gần nhất ≥ *t*. Quy tắc này có cải thiện độ tin cậy trên protein không có láng giềng gần không? | Đường coverage–AUPRC khi quét *t*; so với dự đoán toàn phần |

RQ3 là phần thiết kế mới và cũng là phần sinh ra sản phẩm. Nếu phải cắt vì thời gian, cắt nhánh (b) của RQ2 trước, **không** cắt RQ3.

### Dữ liệu, baseline, chỉ số

- **Dữ liệu:** ATP-549 (train) + 69 protein RTK test độc lập + kho truy hồi 244 protein, từ [RTK_RAG](https://github.com/B1607/RTK_RAG) — repo duy nhất của nhóm có giấy phép (AFL v3.0). **Cộng thêm** ATP-388/ATP-41/ATP-17 làm tập ngoài nhóm. Phần cộng này chữa đúng điểm yếu lớn nhất của bộ gốc: chỉ 69 protein và 711 residue dương thì khoảng tin cậy sẽ rất rộng.
- **Baseline:** (1) ProtTrans + mCNN không truy hồi; (2) truy hồi trộn trung bình α = 0,7 như bản của nhóm; (3) **bộ phân loại k-NN thuần trên embedding** — baseline này quan trọng nhất: nếu k-NN thuần gần bằng mô hình đầy đủ, nghĩa là phần lớn tín hiệu chỉ là tương đồng chuỗi; (4) số công bố của RTK_RAG làm mốc tham chiếu.
- **Chỉ số:** AUPRC là chính; MCC và F1 tại ngưỡng chọn trên validation; AUROC để đối chiếu với bài gốc; trung bình ± độ lệch chuẩn qua seed.
- **Tính toán:** embedding ProtTrans cho khoảng 900–1.300 protein dưới 2 giờ GPU; mỗi lần huấn luyện mCNN vài phút. Toàn bộ trong khoảng 30–60 giờ GPU. Nút thắt là dung lượng đĩa, nên lưu embedding theo residue một lần rồi cắt cửa sổ trong dataloader, không lưu sẵn tensor cửa sổ.

### Sản phẩm (học phần bắt buộc có hệ thống)

Trang web nhận một hoặc nhiều chuỗi FASTA, kiểm tra định dạng, rồi trả về:

- chuỗi axit amin tô màu theo điểm dự đoán từng residue;
- **identity của láng giềng gần nhất trong kho truy hồi, và cờ “ngoài vùng tin cậy”** khi identity dưới ngưỡng *t* của RQ3;
- bảng kết quả tải xuống được, kèm vài chuỗi tham chiếu gần nhất.

Điểm bán được của sản phẩm: cờ tin cậy là hiện thân trực tiếp của RQ3, không phải giao diện trang trí. Không công cụ nào trong dòng bài này hiện báo tín hiệu đó cho người dùng. Không dựng mô hình 3D. Kiến trúc tối thiểu là FastAPI phục vụ mô hình đã xuất + React; **cần hỏi thầy** lớp hệ thống phải dày tới đâu để hội đồng chấp nhận.

### Lịch và cổng quyết định

| Giai đoạn | Việc chính | Cổng quyết định |
|---|---|---|
| G1 (≈20% thời gian) | Kiểm tra dữ liệu/nhãn/giấy phép; đo thời gian embedding thật trên một phiên Kaggle; dựng baseline không truy hồi | **Tái lập được baseline trong ±0,05 MCC so với số của bài.** Không đạt thì dừng, chuyển sang efflux |
| G2 (≈25%) | Khóa phép chia, dựng giao thức sạch, chạy RQ1 | ΔAUPRC có vượt dao động giữa các seed không |
| G3 (≈25%) | RQ2 ablation + RQ3 quy tắc từ chối | Nếu RQ3 không có tín hiệu, thu hẹp thành benchmark + giao thức |
| G4 (≈20%) | Xây công cụ web từ mô hình đã huấn luyện | Chạy được end-to-end trên chuỗi mới |
| G5 (≈10%) | Viết báo cáo, slide, ghi giới hạn | |

> **Cần điền số tuần thực tế.** Hai bản tài liệu hiện ghi khác nhau (14 tuần ở trang so sánh, 20 tuần ở bản khảo sát). Hỏi thầy mốc nộp rồi quy đổi các phần trăm trên thành tuần cụ thể.

### Kết quả xấu nhất vẫn bảo vệ được

Nếu truy hồi không còn giúp dưới giao thức sạch, luận văn vẫn có ba thứ: một giao thức đánh giá chống rò rỉ cho bài toán này, một kết quả âm **có kiểm soát** (kèm đối chứng âm và khoảng tin cậy), và một công cụ báo tín hiệu tin cậy. Nhưng điều này chỉ đúng **nếu thầy và hội đồng chấp nhận dạng luận văn đó** — nên đây là câu hỏi số 2 trong danh sách dưới.

## Đề xuất dự phòng: efflux (nêu ngắn, 2 phút)

Tăng cường dữ liệu bằng chuỗi ProtGPT2 so với các cách xử lý mất cân bằng rẻ (class weighting, focal loss, SMOTE trên embedding, mixup) cho phân loại siêu họ efflux, dưới phép chia theo cụm MMseqs2 30%. Đây là phần mở rộng đúng hai hạn chế mà [mCNN-GenEfflux](https://doi.org/10.1016/j.compbiolchem.2025.108595) tự nêu, nên là hướng an toàn nhất về quan hệ.

Hai điểm phải nói thật: (1) chưa tìm được bảng công khai xác nhận số chuỗi mỗi họ — [DeepEfflux](https://academic.oup.com/bioinformatics/article/34/18/3111/4970514) ghi SMR chỉ 15 chuỗi, nên lớp hiếm có thể không đủ cụm để chia fold; (2) chi phí fine-tune ProtGPT2 chưa đo. Vì vậy hướng này **chỉ chốt được nếu thầy chia sẻ bộ dữ liệu và cách chia của GenEfflux**.

Một đối chứng âm đáng nêu nếu thầy hỏi sâu: [Shen et al. 2021](https://www.biorxiv.org/content/10.1101/2021.02.18.431877v1.full) cho thấy ngay cả chuỗi bị xáo trộn đôi khi vẫn làm tăng chỉ số. Nên mức tăng từ chuỗi sinh tự nó chưa chứng minh chuỗi đó hợp lý về sinh học.

## Trình bày (khoảng 10 phút)

| # | Nội dung | Thông điệp chính |
|---|---|---|
| 1 | Bối cảnh | Em muốn làm trong hướng PLM + mCNN của nhóm thầy. Nền sinh học của em còn cơ bản, nên em chọn bài toán mà phần sinh học đã được mã hóa trong benchmark |
| 2 | Đơn vị đóng góp | Em không đề xuất kiến trúc mới. Em đề xuất **chất lượng đánh giá** làm trục: tách tập theo đồng dạng, chọn ngưỡng trên validation, AUPRC thay AUC trên dữ liệu ≈1% dương |
| 3 | Hướng chính | ATP ở RTK: ba điểm có thể cải thiện trong giao thức (mục “Vì sao còn chỗ”), dẫn tới ba RQ |
| 4 | Điểm mới thật sự | RQ3: quy tắc từ chối dự đoán theo identity láng giềng, kèm đường coverage–AUPRC. Đây cũng là thứ sinh ra sản phẩm |
| 5 | Sản phẩm | Bản đồ residue + cờ “ngoài vùng tin cậy”. Công cụ đầu tiên trong dòng này báo tín hiệu tin cậy cho người dùng |
| 6 | Dự phòng | Efflux, mở ra nếu thầy chia sẻ được bộ GenEfflux |
| 7 | Cần thầy hỗ trợ | Mã/trọng số RTK_RAG, GPU, và xác nhận dạng luận văn |

**Không** trình bày: chi tiết kiến trúc mCNN, so sánh PLM, hay danh sách xu hướng 2024–2026. Giữ trọng tâm ở “đánh giá trước, mô hình sau”.

## Câu hỏi cho GVHD

**Phạm vi và kỳ vọng** *(hỏi trước, quan trọng nhất)*

1. Hai hướng trên, hướng nào gần chuyên môn và lịch hướng dẫn của thầy hơn?
2. Nhóm thầy đổi mới chủ yếu bằng cách thêm một module mới vào pipeline. Nếu đóng góp của em là **giao thức đánh giá và một quy tắc từ chối dự đoán**, chứ không phải một kiến trúc mới, thầy thấy đủ cho luận văn chưa, hay hội đồng sẽ đòi thêm một thành phần mô hình mới?
3. Nếu kết quả cuối là “truy hồi không giúp dưới giao thức chặt” — tức một kết quả âm có kiểm soát — thầy và hội đồng có chấp nhận không?
4. Tỷ lệ nghiên cứu so với hệ thống của CT553H là bao nhiêu? Lớp hệ thống cần dày tới đâu (chỉ FastAPI phục vụ mô hình, hay cần backend đầy đủ, lưu lịch sử, tài khoản)?
5. Mốc nộp và số tuần thực tế là bao nhiêu?

**Dữ liệu và tài nguyên**

6. Repo RTK_RAG không chứa mã dựng đặc trưng RAG (`rag_prottrans_GPU.py` nằm trong một tệp zip trên server không phản hồi). Thầy có bản đó, trọng số mô hình, hoặc embedding đã trích không ạ? *(Nút chặn số một của hướng chính.)*
7. Thầy có thể chia sẻ bộ dữ liệu và cách chia tập của GenEfflux không? *(Nút chặn duy nhất của hướng dự phòng.)*
8. Có benchmark ngoài hoặc tập test độc lập nào khác cho ATP mà nhóm đang dùng không? Em dùng thêm bộ ATP ngoài nhóm (ATP-388/41/17) để kiểm chứng được chứ ạ?
9. Nguồn GPU thực tế em có thể dùng: máy phòng lab, hay chỉ Colab Pro + Kaggle? Em đang tính khoảng 30–60 giờ GPU cho hướng chính.

**Phương pháp**

10. Phép chia theo đồng dạng: em nên dùng ngưỡng nào cho đúng chuẩn lĩnh vực — giữ CD-HIT 40% để so được với bài gốc, hay siết về 30% và chấp nhận số không so trực tiếp được?
11. Thầy muốn phần trọng tâm nghiêng về phép truy hồi, kiểm soát rò rỉ/mất cân bằng, hay khả năng giải thích đầu ra?

**Hành chính và cơ hội**

12. Mẫu đề cương, lịch nộp đề cương, tần suất gặp và kênh liên lạc?
13. Nếu kết quả tốt, thầy có muốn hướng tới một bài hội nghị không ạ?

## GVHD có thể hỏi lại

| Câu hỏi | Trả lời ngắn |
|---|---|
| Em thêm gì so với RTK_RAG? | Ba thứ: giao thức sạch (ngưỡng trên validation, kho truy hồi tách khỏi test, AUPRC), một tập ATP ngoài nhóm, và quy tắc từ chối dự đoán theo identity láng giềng. Không thay kiến trúc |
| Chỉ đo lại thì có đủ làm luận văn? | Phần đo lại là nền. Phần mới là RQ3 và công cụ báo tín hiệu tin cậy — chưa có công cụ nào trong dòng này làm |
| Sao không dùng ESM-2, vốn cho MCC cao hơn? | Bài gốc chọn ProtTrans để tiết kiệm tính toán. Em giữ ProtTrans để so sánh công bằng với số đã công bố; ESM-2 là một nhánh nếu còn ngân sách GPU |
| Tại sao AUPRC chứ không AUC? | Tập test chỉ ≈0,96% residue dương. Ở mức đó AUC sát trần và không phân biệt được mô hình |
| Vì sao bootstrap theo protein? | 69 protein nhưng hơn 73.000 residue. Các residue trong cùng protein tương quan mạnh, nên coi mỗi residue là một quan sát độc lập sẽ cho khoảng tin cậy hẹp giả tạo |
| Nếu truy hồi vẫn giúp rõ thì sao? | Vẫn là kết quả tốt: một khẳng định có kiểm soát, cộng đường coverage cho biết nó giúp ở đâu và hết tác dụng ở đâu |
| k-NN thuần để làm gì? | Để biết phần nào của kết quả chỉ là tương đồng chuỗi. Nếu k-NN thuần gần bằng mô hình đầy đủ thì đó là phát hiện đáng báo cáo |
| Nền sinh học của em có đủ không? | Nhãn residue gắn đã có trong benchmark. Phần sinh học cần đọc là motif Walker A / P-loop, trong tầm tự học |
| GPU ở đâu? | Colab Pro + Kaggle. Embedding dưới 2 giờ, mỗi lần huấn luyện vài phút |
| Tiêu chí dừng? | Cổng G1: không tái lập được baseline trong ±0,05 MCC thì chuyển hướng. Cổng G3: RQ3 không có tín hiệu thì thu hẹp phạm vi |

## Những điểm chưa kiểm chứng — nói thẳng nếu bị hỏi

- Chưa tự mở bộ ATP-388/41/17; khả năng tải và tính tương thích nhãn là việc của tuần 1.
- Chưa biết repo RTK_RAG có bản mã dựng đặc trưng RAG ở đâu khác không.
- Quota Kaggle: tài liệu ghi khoảng 30 giờ/tuần, một nguồn thứ cấp ghi 50 giờ. Chưa xem banner trong tài khoản.
- Số chuỗi mỗi họ efflux: hai nguồn ghi khác nhau (ABC 2394/SMR 18 so với ABC 1670/SMR 15).
- Mọi ước lượng giờ GPU trong tài liệu này là suy luận từ mốc đo của người khác, chưa tự đo.
