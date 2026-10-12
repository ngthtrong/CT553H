# Phân tích hai luận văn tin sinh để tham khảo

Ngày đọc: **05/10/2026**. Mục đích: học cách xác định đóng góp, thiết kế thực nghiệm và xây dựng ứng dụng cho hướng **aging/cancer đang khảo sát**, chưa chọn đề tài thay người làm luận văn.

## 1. Kết luận để sử dụng ngay

**Bài peptide là mẫu tốt hơn cho phần nghiên cứu mô hình; BioFlow-Scope là mẫu tốt hơn cho phần kỹ nghệ phần mềm.** Với định hướng hiện tại, nên tham khảo cách tổ chức thực nghiệm của bài thứ nhất và chọn một số chức năng truy vết, quản lý kết quả, kiểm thử của bài thứ hai. Ghép nguyên hai phạm vi sẽ quá rộng so với khoảng 8–9 tuần thực hiện đã ghi trong [biên bản GVHD](../../project/meetings/2026-10-02-session-01/minutes.md).

Hai bài cho thấy hai cách làm luận văn tin sinh trong ngành Kỹ thuật phần mềm: phát triển bộ dự đoán có ứng dụng, hoặc phát triển nền tảng tích hợp công cụ. Chúng **không chứng minh** rằng chỉ cần dùng PLM, thêm XAI và làm website là đủ đóng góp cho đề tài của mình.

### Tài liệu và giới hạn bằng chứng

- **[T1 — Hybrid Cascade](b2203539-ho-quoc-bao-hybrid-cascade-plm-mscnn.pdf)**: *A Hybrid Cascade Framework Integrating Protein Language Models and Multi-scale CNNs for Peptide Screening and Toxicity Prediction*, 08/2026, 96 trang PDF.
- **[T2 — BioFlow-Scope](b2205944-nguyen-duy-khanh-thesis.pdf)**: *Design and Implementation of BioFlow-Scope — An AI-Assisted Web Platform for Reproducible Bioinformatics Pipelines*, 08/2026, 212 trang PDF.
- Cả hai bìa ghi GVHD **Ho Quang Thai (TS. Hồ Quang Thái)**, **cùng GVHD của người làm đề tài trong repo**, theo xác nhận lại của người dùng ngày 05/10/2026. Hai bài vì vậy là tiền lệ cùng GVHD đáng tham khảo; vẫn cần căn cứ góp ý trực tiếp để xác định phạm vi và yêu cầu đánh giá của đề tài hiện tại.
- Số trang bên dưới là **trang PDF, tính từ 1**; khi cần có thêm số trang in. Đã đọc phần bài toán, phương pháp, thiết kế, kết quả, giới hạn; đối chiếu trực quan bảng kết quả chính và hình XAI. Đây là phân tích báo cáo, **chưa kiểm toán mã nguồn, chạy phần mềm hoặc tái lập thực nghiệm**. Các số đo đều là số tác giả báo cáo, trừ phép tính được ghi rõ.
- Phân biệt **nội dung báo cáo**, **nhận xét từ bằng chứng** và **đề xuất cho đề tài của mình**. Không coi lời khẳng định trong luận văn là kết quả đã được xác minh độc lập.

## 2. So sánh tổng quan

| Khía cạnh | T1 — Hybrid Cascade | T2 — BioFlow-Scope |
|---|---|---|
| Vấn đề trung tâm | Sàng lọc peptide có hoạt tính kháng khuẩn rồi đánh giá khả năng gây tan máu | Quản lý và thực thi quy trình tin sinh có truy vết, hỗ trợ tìm kiếm protein và AI Agent |
| Đầu vào → đầu ra | Chuỗi peptide → điểm AMP, điểm tan máu, vùng nhạy cảm và kết quả sàng lọc | Dữ liệu + pipeline + tham số → lần chạy, log, artifact, provenance; câu hỏi/chuỗi → kết quả truy hồi |
| Đơn vị nghiên cứu | Chuỗi peptide; hai bài toán phân loại nhị phân | Pipeline, lần chạy, dữ liệu, người dùng và thao tác Agent |
| Trọng tâm đóng góp | So sánh biểu diễn/mô hình, xử lý lệch dữ liệu, lựa chọn hiệu năng–chi phí, XAI | Thiết kế và tích hợp hệ thống, quản lý vòng đời thực thi, tái lập và kiểm soát AI |
| AI sử dụng | ESM-2 + CNN/mCNN; occlusion XAI | ESM-2 cho protein search; embedding văn bản, RAG, LLM và tool calling |
| Ứng dụng | FastAPI + Streamlit; cài cục bộ hoặc Docker | Spring Boot + Next.js + PostgreSQL + Redis + Qdrant + FastAPI + Docker |
| Bằng chứng mạnh hơn | Bảng thực nghiệm mô hình và dữ liệu | Đặc tả, kiến trúc, kiểm thử chức năng/backend/E2E |
| Khoảng trống đánh giá | Độc lập đồng dạng, nhãn âm, ablation có kiểm soát, kiểm chứng XAI và toàn cascade | Chất lượng truy hồi, chất lượng LLM, tải lớn và tái chạy trên môi trường độc lập |
| Độ gần với hướng aging/cancer | Gần về PLM–mCNN và dự đoán từ chuỗi; khác mục tiêu sinh học | Gần về sản phẩm nghiên cứu tin sinh; không cung cấp predictor aging/cancer |

Không so số trang hoặc số tính năng để kết luận bài nào “tốt hơn”; hai bài đặt trọng tâm khác nhau.

## 3. T1 — Hybrid Cascade: nên học gì và cần phản biện gì?

### 3.1. Bài toán và phương pháp

Luồng chính gồm hai mô hình: **AMP Gatekeeper** phân biệt AMP/non-AMP, sau đó **Toxicity Assessor** đánh giá tan máu cho chuỗi qua cổng đầu. Phần triển khai bổ sung đối chiếu 55 motif và XAI bằng che lần lượt từng residue. Vì vậy, “hai tầng” là hai bộ dự đoán; sơ đồ ba bước có thêm bước diễn giải/khuyến nghị, không nhất thiết là ba mô hình học máy. [T1, PDF 41–45]

Phương pháp được triển khai thành một chuỗi so sánh:

1. AAC/DPC/one-hot với RF hoặc SVM làm mốc.
2. CNN một cửa sổ và mCNN nhiều cửa sổ.
3. ESM-2 ở các cỡ 8M, 35M, 150M, 650M; khảo sát frozen embedding và fine-tuning.
4. Sàng lọc cấu hình trên 5.000 mẫu train và 1.000 mẫu validation, seed 42, giới hạn 3 epoch; sau đó huấn luyện các ứng viên trên dữ liệu đầy đủ.
5. Cấu hình được ưu tiên khi triển khai là **ESM-2 35M frozen + mCNN (3, 5, 7)**. Nhánh 650M dùng cửa sổ (5, 7, 9). Bài toán độc tính dùng Focal Loss. [T1, PDF 46–51, 73, 78]

Điểm có thể học là **mỗi bước thêm độ phức tạp đều có đối chứng**, rồi chọn cấu hình theo cả kết quả và tài nguyên. Tuy nhiên, proxy 3 epoch chỉ dùng để sàng lọc sớm; nó không bảo đảm thứ hạng khi huấn luyện hội tụ hoặc sau khi thay đổi phân bố dữ liệu.

### 3.2. Dữ liệu và kết quả chính

Tác giả tổng hợp HemoPI-1/2/3, RNN-Hem, HLPpred-Fuse và Viri. Nhánh độc tính chỉ giữ một số nguồn âm để giảm nhầm lẫn giữa “không phải AMP” và “AMP ít/không gây tan máu”. Đây là ý tưởng đáng học về **định nghĩa nhãn theo đúng câu hỏi sinh học**; tính đúng đắn của từng phép gán nhãn vẫn cần dữ liệu gốc để kiểm tra. [T1, PDF 44–45]

| Dữ liệu | Tổng | Train | Validation | Test |
|---|---:|---:|---:|---:|
| AMP | 96.529 | 77.223 | 9.653 | 9.653 |
| Tan máu | 3.146 | 2.516 | 315 | 315 |

Nguồn: Bảng 4.3–4.4, PDF 56. Toàn bộ dữ liệu tan máu gồm **2.379 toxic và 767 safe**; lớp toxic là lớp đa số.

Kết quả cuối ở Bảng 4.13, PDF 79 (trang in 56):

| Bài toán | Cấu hình | Accuracy | Recall | Specificity | F1 | ROC-AUC |
|---|---|---:|---:|---:|---:|---:|
| AMP | 35M + mCNN (3,5,7) | 91,88% | 81,91% | 96,56% | 86,57% | 0,9739 |
| AMP | 650M + mCNN (5,7,9) | 91,69% | 79,45% | 97,44% | 85,94% | 0,9801 |
| Tan máu | 35M + mCNN + Focal | 77,78% | 75,21% | 85,71% | 83,64% | 0,8950 |
| Tan máu | 650M + mCNN + Focal | 74,92% | 71,43% | 85,71% | 81,15% | 0,8870 |

**Diễn giải vừa đủ:** cấu hình 35M có F1/recall tốt hơn trong các phép so sánh này; riêng AMP, 650M có ROC-AUC cao hơn. Không có cơ sở gọi 35M thắng trên mọi tiêu chí hoặc kết luận mọi PLM lớn đều kém cho peptide.

### 3.3. Bốn điểm đáng tham khảo

- **Động cơ dẫn tới luồng sản phẩm:** tìm ứng viên có hoạt tính rồi đánh giá thêm một thuộc tính bất lợi, thay vì chỉ trả một nhãn. Điều này làm ứng dụng gắn với thao tác nghiên cứu cụ thể. [PDF 24–28, 41–42]
- **Quan tâm chất lượng dữ liệu:** tác giả phát hiện độ dài trung bình AMP khoảng 22 aa, âm khoảng 44 aa; thực hiện cắt chuỗi âm để khớp phân bố độ dài. Đây là ví dụ tốt về việc kiểm tra mô hình có thể học tín hiệu ngoài mục tiêu hay không. [PDF 74–76]
- **Chọn mô hình có tính tới triển khai:** có phân tích thời gian huấn luyện và cấu hình nhỏ để phục vụ cục bộ. Nên học cách đặt câu hỏi hiệu năng–chi phí, còn kết luận chạy tốt trên máy của mình phải đo lại. [PDF 71–73, 85–88]
- **XAI nối trực tiếp với giao diện:** che residue, đo thay đổi đầu ra, hiển thị vùng nhạy cảm và đối chiếu motif. Đây là mẫu luồng tương tác có thể chuyển sang dự đoán site. [PDF 51–52, 82–86]

### 3.4. Các điểm chưa đủ bằng chứng hoặc chưa nhất quán

**A. Loại trùng hoàn toàn chưa kiểm soát được đồng dạng giữa các tập.** PDF 45 mô tả `drop_duplicates` rồi chia ngẫu nhiên 80/10/10. PDF 27 nói các nguồn có tiền xử lý đồng dạng, nhưng điều này chưa xác lập độc lập sau khi hợp nhất nhiều nguồn. Vì vậy, “independent” ở Bảng 4.13 nên hiểu là **holdout theo mô tả của bài**, chưa phải test độc lập nguồn hoặc không có chuỗi gần giống train. Đây là thiếu bằng chứng về giao thức, chưa phải kết luận đã đo được rò rỉ. CD-HIT có cơ chế gom cụm theo ngưỡng identity và tham số coverage; thao tác đó khác loại chuỗi trùng hoàn toàn. [Hướng dẫn chính thức CD-HIT](https://github.com/weizhongli/cdhit/blob/master/doc/cdhit-user-guide.wiki)

**B. Nhãn AMP và nhãn tan máu cần được kiểm riêng.** PDF 44 gán AMP dương từ nhiều nguồn hemolysis, còn PDF 45 gom các mẫu độc thành toxic AMP. Cần bảng bằng chứng hoạt tính AMP theo nguồn/mẫu; dữ kiện tan máu tự nó chưa đủ chứng minh nhãn AMP trong pipeline này. Tác giả cũng thừa nhận chuỗi con cắt từ nguồn non-AMP **chưa được xác nhận thực nghiệm là âm**. [PDF 75, 89]

**C. Diễn giải Focal Loss mâu thuẫn với số lượng lớp.** PDF 78 gọi toxic là lớp hiếm, trong khi Bảng 4.3–4.4 cho thấy toxic là đa số. Chưa xem code nên không kết luận loss được cài sai; cần kiểm quy ước lớp dương, cách áp dụng α=0,26 và đối chứng BCE so với Focal trên cùng dữ liệu.

**D. F1 cao chưa đủ chứng minh khả năng sàng lọc độc tính.** Test có 238 toxic/77 safe. Bộ dự đoán luôn trả toxic sẽ đạt F1 lớp toxic khoảng **86,08%**, tính bằng `2 × 238 / (2 × 238 + 77)`, nhưng specificity bằng 0. F1 của mô hình 35M là 83,64%, đồng thời specificity đạt 85,71% và ROC-AUC 0,8950. Điều này không khiến mô hình vô dụng; nó cho thấy cần đọc F1 cùng confusion matrix, chỉ số cân bằng hai lớp và chi phí sai. Recall 75,21% tương ứng bỏ sót khoảng **24,79% mẫu toxic** ở ngưỡng báo cáo, nên không thể diễn giải đầu ra là bảo đảm an toàn. [Bảng 4.4 và 4.13; các tỷ lệ dẫn xuất do người đọc tính]

**E. Chưa tách được nguyên nhân của hiện tượng 650M kém hơn.** Hai cấu hình cuối thay đổi đồng thời cỡ PLM, chiều embedding và bộ kernel. Cần giữ head hoặc thiết kế đối chứng phù hợp, chạy nhiều seed và báo độ biến thiên để quy kết tác động. PDF 82 có câu thận trọng coi giải thích là giả thuyết, nhưng PDF 88 lại dùng diễn đạt mạnh về sai sót của scaling laws. Chỉ nên giữ kết luận thực nghiệm trong phạm vi đã đo.

**F. Chưa đủ kết quả cho toàn bộ cascade.** Bảng 4.13 đánh giá hai nhiệm vụ riêng. Còn cần tập có nhãn phù hợp để đo cả luồng: bao nhiêu AMP hữu ích bị loại ở cổng đầu, bao nhiêu ứng viên qua cả hai cổng thực sự thuộc nhóm mong muốn, và thời gian tiết kiệm bao nhiêu. Không nhân trực tiếp hai recall từ hai tập test khác nhau để suy ra hiệu năng toàn hệ thống.

**G. Heatmap chưa xác nhận cơ chế sinh học.** Báo cáo mô tả che token bằng MASK hoặc PAD, nhưng hai lựa chọn cần được xác định và kiểm tra riêng. Hình 4.9–4.10 cho thấy ví dụ minh họa, chưa phải đánh giá có hệ thống độ trung thực hay ổn định của giải thích. Cần lưu cả attribution có dấu trước chuẩn hóa, so sánh che vị trí quan trọng với vị trí ngẫu nhiên, và dùng motif thực nghiệm độc lập khi có. Nghiên cứu về sanity checks cũng cho thấy xem hình đẹp là chưa đủ để đánh giá saliency. [T1, PDF 51–52, 83–84; Adebayo et al., 2018](https://arxiv.org/abs/1810.03292)

**H. Phạm vi chiều dài và bằng chứng triển khai cần thống nhất.** PDF 27 giới hạn ≤30 aa, PDF 54–55 mô tả dữ liệu đến 100 aa và đầu vào 128; PDF 78 ghi tối đa 128 token. Cần phân biệt residue với token và xác định miền dữ liệu thật. Yêu cầu RAM 4 GB ở PDF 87 cũng chưa thay thế được benchmark CPU/RAM và độ trễ, nhất là khi bật XAI.

**Bài học:** học cấu trúc lập luận và hệ thống đối chứng; không sao chép các từ như “unbiased”, “universal paradox”, “safe” hoặc “chứng minh cơ chế” khi bằng chứng chưa tương ứng.

## 4. T2 — BioFlow-Scope: nên học gì và cần phản biện gì?

### 4.1. Đóng góp thực chất

Đây là luận văn **xây dựng nền tảng nghiên cứu**, không phải đề xuất mô hình protein mới. Phần mềm gom các thao tác vốn rời rạc vào một quy trình: thiết kế pipeline bằng canvas/YAML, kiểm tra DAG, chạy công cụ bằng Docker, quản lý dataset/artifact, theo dõi log và lưu provenance. AI hỗ trợ tìm kiếm và điều phối thao tác. [T2, PDF 20–25]

Kiến trúc được báo cáo gồm Spring Boot modular monolith, Next.js, PostgreSQL, Redis, Qdrant và FastAPI sidecar. Điểm đáng học là **phân công trách nhiệm**, không phải số lượng công nghệ.

Hai luồng embedding được tách rõ:

| Luồng | Biểu diễn được báo cáo | Công dụng |
|---|---|---|
| Protein | ESM-2 35M, mean pooling, 480 chiều | Tìm protein gần trong không gian embedding rồi bổ sung metadata |
| Văn bản | all-MiniLM-L6-v2, 384 chiều | Tìm đoạn tài liệu cho RAG/Agent |

Nguồn: Bảng 2.8, PDF 97. Không so trực tiếp vector của hai không gian; protein search cũng không tự trở thành XAI hay xác nhận chức năng sinh học. Bài giải thích khá rõ điểm similarity không phải xác suất hoặc E-value. [PDF 99–100]

### 4.2. Các phần nên lấy làm mẫu

- **Quản lý một lần chạy như một đối tượng nghiên cứu:** liên kết phiên bản pipeline, tham số, đầu vào, log, đầu ra và checksum. Với đề tài predictor, có thể thu gọn thành phiên bản model, dữ liệu đầu vào, ngưỡng, cấu hình XAI và kết quả xuất. [PDF 90–94, 117]
- **Luồng công việc có trạng thái:** chạy, theo dõi, hủy, tiếp tục, so sánh; xử lý lỗi là một phần sản phẩm. [PDF 194–195]
- **Tách quyền thao tác, phê duyệt và bằng chứng:** Agent đề xuất hành động nhưng hệ thống vẫn kiểm quyền, lưu quyết định và liên kết kết luận với nguồn. Chỉ cần học phần này nếu sản phẩm thật sự có Agent. [PDF 150–154]
- **Đặc tả dẫn tới kiểm thử:** báo cáo có dữ liệu/thao tác/kết quả mong đợi và kết quả kiểm thử; phần kiểm thử không chỉ là ảnh chụp giao diện. [PDF 189–199]
- **Nói rõ giới hạn:** bài tự phân biệt kiểm thử phần mềm với benchmark khoa học, giúp người đọc biết đã và chưa chứng minh điều gì. [PDF 199]

### 4.3. Kết quả được báo cáo và cách hiểu

| Hạng mục | Báo cáo | Giới hạn suy luận |
|---|---|---|
| Chức năng | 47/47 PASS | Đúng trong các kịch bản đã kiểm |
| Backend | 1.134 test: 1.133 PASS, 1 SKIP do Docker daemon, 0 FAIL | Không nên rút gọn thành tất cả test đều chạy thành công |
| Coverage | Instruction 51,70%; Class 57,28%; Branch 42,24% | Chỉ số bao phủ mã, không phải độ chính xác sinh học |
| Frontend | 35 Playwright E2E PASS; TypeScript 0 lỗi | Bằng chứng cho giao diện/luồng và kiểm tra kiểu |
| Tìm protein | Trường hợp PETase: tổng 982 ms | Chưa phải phân bố latency trên nhiều truy vấn và tải |
| Tái lập | Bundle được verifier xác nhận | Cần xem verifier kiểm điều gì; chưa tự suy ra tái chạy độc lập cho kết quả tương đương |

Nguồn: Bảng 4.18, PDF 198–199 (trang in 179–180). Chưa có log/mã nguồn trong phạm vi đọc để xác nhận lại các số này.

### 4.4. Các giới hạn quan trọng

**A. Chất lượng AI chưa được đánh giá như một kết quả nghiên cứu.** PDF 199 nói rõ chưa có benchmark precision/recall cho Semantic Protein Search hoặc khung chấm chất lượng LLM. Trả kết quả nhanh, có citation và gọi đúng API chưa chứng minh protein tìm được có chức năng phù hợp hoặc câu trả lời được nguồn hỗ trợ.

**B. Ảnh giao diện không phải bằng chứng tích hợp đang chạy.** PDF 141 (trang in 122) ghi rõ hình ở §3.3–3.4 chụp frontend dùng **mock API vì backend trả HTTP 503** khi chụp. Điều này không phủ định các test được báo cáo ở thời điểm khác, nhưng không dùng chính các ảnh đó để xác nhận luồng backend/AI hoạt động.

**C. Phạm vi nhập và phạm vi mô hình nhìn thấy khác nhau.** API nhận chuỗi 10–5.000 ký tự, trong khi tokenizer được cấu hình mặc định 1.024 token. [PDF 97] Nếu tham khảo cách làm này, phải thông báo phần bị cắt hoặc thiết kế cách xử lý chuỗi dài; nếu không, người dùng dễ hiểu kết quả đại diện cho toàn protein.

**D. Tái lập cần nhiều mức bằng chứng.** Bài đã phân biệt các mức kiểm chứng ở PDF 90–94. Tuy nhiên, kiểm checksum của bundle chủ yếu xác nhận tính toàn vẹn artifact; đánh giá tái lập tính toán còn cần tái chạy trên môi trường sạch, xác định phiên bản dữ liệu/công cụ và tiêu chí đầu ra tương đương. Tên trạng thái `VERIFIED_REPRODUCIBLE` trong test không tự thay thế giao thức này.

**E. Phạm vi lớn và chứng minh nhu cầu còn có thể làm sâu hơn.** Pipeline editor, worker, viewer đa định dạng, workspace, quota, search, Agent và publication là nhiều sản phẩm con. Trong các phần kết quả đã đọc, bằng chứng mạnh nhất là triển khai/kiểm thử; chưa có nghiên cứu người dùng định lượng về thời gian hoàn thành công việc, số lỗi hoặc lợi ích so với cách làm trước. Khi mượn ý tưởng, nên chọn một quy trình cụ thể để đo.

**F. Có lỗi biên tập cần tránh.** PDF 3 ghi tên đề tài về mạng xã hội cho sinh viên, không khớp BioFlow-Scope ở bìa. Đây là lỗi nhất quán tài liệu, không phải bằng chứng rằng phần mềm hoặc toàn bộ kết quả sai.

## 5. Đối chiếu với năm tiêu chí của GVHD hiện tại

Đây là **nhận xét của người đọc**, không phải chấm điểm của GVHD. Tiêu chí lấy từ [biên bản lần 1](../../project/meetings/2026-10-02-session-01/minutes.md).

| Tiêu chí | Bài học từ T1 | Bài học từ T2 | Điều cần chứng minh trong đề tài của mình |
|---|---|---|---|
| Tính mới của hướng | Một vấn đề sinh học có đầu vào/đầu ra rõ | Một khó khăn trong quy trình nghiên cứu | Khoảng trống của đúng bài toán aging/cancer; không chỉ đổi tên dữ liệu |
| Cải tiến phương pháp | So sánh CNN/mCNN và xử lý dữ liệu | Cải tiến quy trình và tích hợp hệ thống | Đối chứng tách tác động của phần cải tiến; thống nhất với GVHD loại đóng góp được kỳ vọng |
| Sử dụng phương pháp mới | Thử PLM thay biểu diễn thủ công | Tích hợp embedding, RAG và Agent | Chỉ ra phương pháp giải quyết hạn chế nào; độ mới phải khảo sát riêng |
| XAI | Có occlusion và ví dụ heatmap, còn thiếu đánh giá sâu | Provenance/citation hỗ trợ truy vết, không thay thế XAI predictor | Đánh giá lời giải thích bằng perturbation, ổn định và bằng chứng độc lập nếu có |
| Ứng dụng/website | Predictor chuyên biệt, phạm vi gọn | Thiết kế và kiểm thử hệ thống phong phú | Luồng sử dụng hoàn chỉnh, kết quả lưu/xuất được, kiểm thử lỗi và tài nguyên |

## 6. Áp dụng cho hai hướng đang khảo sát

### 6.1. Phần có thể chuyển giao

Theo [khảo sát aging/cancer hiện có](../../archive/surveys/aging-cancer/aging-cancer-deep-dive.md), hai ứng viên đầu là site deacetyl hóa theo SIRT và site phosphoryl hóa theo nhóm kinase. Đây là **ngữ cảnh của repo**, không phải đánh giá mới về tính mới hay độ sẵn sàng của dữ liệu.

- Từ T1: học ma trận baseline → biểu diễn → head → ablation; kiểm tra lệch dữ liệu; đo chi phí; trình bày XAI trên chuỗi.
- Từ T2: học cách lưu mỗi lần phân tích với phiên bản model, input hash, cấu hình, kết quả và log; xuất báo cáo để người dùng kiểm lại.
- **Phải thay đổi đầu ra:** hai hướng site cần xác định protein, vị trí residue và loại nhãn; không dùng nguyên bộ phân loại cả chuỗi peptide rồi coi là predictor site.
- **Phải thiết kế lại split:** giữ các site/cửa sổ từ cùng protein trong cùng nhóm, kiểm tra đồng dạng phù hợp, dựng dữ liệu trước khi tối ưu mô hình. Ngưỡng và cách kiểm tra phải phù hợp dữ liệu thực tế.
- **Không chuyển kết luận sinh học:** predictor AMP/tan máu không xác nhận peptide chống ung thư; predictor PTM trên protein liên quan aging/cancer cũng không trực tiếp dự đoán bệnh hay hiệu quả điều trị.

### 6.2. Phạm vi sản phẩm đề xuất để cân nhắc

Một website chuyên biệt có thể gồm: nhập FASTA → kiểm tra chuỗi → dự đoán site → xem điểm và giải thích theo vị trí → đối chiếu metadata/nguồn → lưu và xuất kết quả. Chức năng chạy lô, trạng thái công việc và phiên bản model tạo chiều sâu kỹ nghệ phần mềm mà không cần xây một nền tảng pipeline tổng quát.

Phần nghiên cứu nên chọn một giả thuyết chính để kiểm, chẳng hạn lợi ích của mCNN so với head đơn giản trên cùng embedding, hoặc độ hữu ích của XAI trong xác định vùng mô hình dựa vào. Chưa thêm Agent/RAG nếu chưa có tác vụ cần nó và giao thức đánh giá tương ứng. Đây là **đề xuất phạm vi**, chưa phải quyết định chọn đề tài hoặc triển khai.

### 6.3. Các nhóm bằng chứng nên chuẩn bị

| Nhóm | Bằng chứng tối thiểu hữu ích |
|---|---|
| Dữ liệu | Nguồn và ý nghĩa nhãn, số protein/site, nhóm chia tập, kiểm trùng/đồng dạng, giới hạn mẫu âm |
| Mô hình | Baseline đơn giản và PLM + head đơn giản; ablation trên cùng split; nhiều seed khi khả thi; ngưỡng chọn trên validation |
| Đánh giá | Chỉ số theo lớp/nhãn, confusion matrix, PR-AUC/MCC phù hợp bài toán, phân tích lỗi; test được giữ riêng |
| XAI | So che vị trí quan trọng với vị trí ngẫu nhiên, độ ổn định và ca thất bại; phân biệt giải thích mô hình với cơ chế sinh học |
| Phần mềm | Luồng nhập–chạy–xem–xuất, input lỗi/chuỗi dài, thất bại/hủy tác vụ, latency theo độ dài/lô, RAM/VRAM thực đo |
| Tái lập | Cấu hình/seed/split/model version, môi trường chạy, log và một lần tái chạy có tiêu chí so sánh |

## 7. Thứ tự đọc để tiết kiệm thời gian

| Mục tiêu | Trang nên đọc |
|---|---|
| Hiểu bài toán T1 | PDF 24–28: động cơ, câu hỏi và phạm vi |
| Học tổ chức mô hình và dữ liệu | T1 PDF 41–52: cascade, nhãn, proxy, ablation và XAI |
| Học phân tích kết quả, kiểm tra phát biểu | T1 PDF 73–84: lệch độ dài, bảng kết quả, giới hạn giải thích |
| Học triển khai predictor | T1 PDF 85–89 |
| Hiểu đóng góp T2 | PDF 20–25 |
| Phân biệt provenance, search và giải thích | T2 PDF 90–104 |
| Học đặc tả AI, nhận diện giới hạn ảnh giao diện | T2 PDF 140–154 |
| Học cách báo cáo kiểm thử có giới hạn rõ | T2 PDF 189–201 |

Trước khi dựa vào hai bài làm tiền lệ cho đề xuất, nên làm rõ với GVHD: phạm vi ứng dụng chuyên biệt cần sâu tới đâu, cải tiến mô hình/XAI cần bằng chứng gì, và có thể xin mã nguồn/cấu hình/split của bài tham khảo để kiểm lại hay không. Chưa có căn cứ từ hai PDF để xác nhận điểm số, mức đánh giá của hội đồng hoặc khả năng tái sử dụng mã.
