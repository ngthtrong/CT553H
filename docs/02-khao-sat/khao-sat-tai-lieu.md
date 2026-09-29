# Khảo sát tài liệu và bằng chứng cho các khẳng định của đề tài

> Ngày tìm: 29/09/2026 · Người thực hiện: Claude (tìm và tóm tắt), người làm đề tài cần **tự đọc lại bản gốc** trước khi trích dẫn trong đề cương hay luận văn.
> Đi kèm: [de-tai-1-brainstorm.md](../01-y-tuong/de-tai-1-brainstorm.md), [de-cuong.tex](../04-de-cuong/de-cuong.tex).

---

## 1. Cách tìm

| Mục | Nội dung |
|---|---|
| Nguồn | Công cụ tìm kiếm web; trang arXiv, ACL Anthology, ACM Digital Library, Springer, trang tác giả |
| Từ khóa (tiếng Anh) | transaction categorization, user-defined categories, cold start, label names only, zero-shot text classification, LLM synthetic data, prequential evaluation, concept drift, email foldering, personal informatics, abandonment, semi-automated tracking, mental accounting, automation bias, noisy labels, quantification, conformal prediction time series, intermittent demand, hierarchical forecast reconciliation |
| Từ khóa (tiếng Việt) | phân loại chi tiêu cá nhân, ghi chú giao dịch, học máy tiếng Việt |
| Tiêu chí giữ lại | Công bố có bình duyệt, hoặc preprint arXiv có nội dung kỹ thuật rõ. Blog và trang quảng cáo chỉ ghi nhận là **tài liệu xám**, không dùng làm bằng chứng |
| Chưa làm | Tìm có hệ thống trên Google Scholar / Scopus; lần theo trích dẫn (snowballing) từ các bài gần nhất ở mục 4 |

**Giới hạn:** không thể chứng minh "chưa ai làm". Kết luận ở mục 5 chỉ có nghĩa là: *trong phạm vi tìm kiếm trên, chưa thấy*. Cần tìm lại trên Google Scholar trước khi nộp đề cương.

---

## 2. Bảng đối chiếu khẳng định và bằng chứng

Mức độ: **A** = nghiên cứu có bình duyệt · **B** = dữ liệu hoặc thí nghiệm của chính đề tài (chỉ một người) · **C** = tài liệu xám · **✗** = chưa có bằng chứng.

| # | Khẳng định trong đề tài | Bằng chứng | Mức | Việc cần làm |
|---|---|---|---|---|
| K1 | Ghi chép thủ công tốn công, dễ khiến người dùng ngừng ghi | Li và cộng sự (2010) xác định rào cản ở giai đoạn *thu thập* trong hệ thống personal informatics. Epstein và cộng sự (2015) mô tả việc quên ghi và bỏ dở như một phần tất yếu của tự theo dõi. Choe và cộng sự (2017) đề xuất theo dõi bán tự động để giảm gánh nặng nhập liệu | A (lĩnh vực tự theo dõi nói chung) | **Chưa có** nghiên cứu có bình duyệt riêng cho ghi chép chi tiêu. Các số liệu kiểu "82% bỏ app vì nhập tay" chỉ là tài liệu xám (C). → Khảo sát người dùng (mục 6) |
| K2 | Mỗi người tự đặt danh mục theo cách riêng | Lý thuyết kế toán tâm lý: người ta gom khoản chi vào các "tài khoản tâm lý" do mình tự định nghĩa (Thaler, 1999; Heath & Soll, 1996). QuickBooks cho doanh nghiệp tự đặt tên danh mục, và bài toán phân loại phải theo danh mục đó (Dong và cộng sự, 2025). Dữ liệu đề tài có 25 danh mục riêng như AC, RL, Ngu | A + B | Chưa có bằng chứng rằng **người dùng cá nhân Việt Nam** thực sự tạo danh mục riêng. → Khảo sát (mục 6) |
| K3 | Chọn danh mục là một phần đáng kể của công ghi chép | Choe và cộng sự (2017) nói chung về gánh nặng nhập liệu. Chưa tìm thấy nghiên cứu tách riêng phần công chọn danh mục | ✗ | Khảo sát; đo trực tiếp trong đánh giá người dùng (thời gian nhập có và không có gợi ý) |
| K4 | Gợi ý vài lựa chọn (top-k) giúp giảm công | MailCat gợi ý 3 thư mục cho mỗi email; khi gợi ý đúng, người dùng chỉ cần một cú nhấp (Segal & Kephart, 1999) | A (bài toán tương tự: xếp email) | Báo cáo top-3 trong thí nghiệm |
| K5 | Ghi chú tiếng Việt rất ngắn, viết tắt, thiếu dấu | Dữ liệu đề tài: trung vị 2 từ, nhiều biến thể viết ([bao-cao-du-lieu.md](../03-du-lieu/bao-cao-du-lieu.md)). Tài liệu về khôi phục dấu tiếng Việt cho thấy văn bản thiếu dấu phổ biến trên mạng xã hội | B; phần "phổ biến" chỉ ở mức C | Không suy rộng từ một người. Thu ghi chú của tình nguyện viên (RQ4) |
| K6 | Người dùng mới không có dữ liệu (cold start) | QuickBooks nêu cold start là thách thức chính của phân loại giao dịch (Dong và cộng sự, 2025). Thí nghiệm đề tài: chỉ nhớ lại thì 30 ngày đầu đạt 17,2% ([rq2-baseline-nho-lai](../../ml/experiments/rq2-baseline-nho-lai/README.md)) | A + B | — |
| K7 | LLM sinh dữ liệu huấn luyện được khi chưa có nhãn | ZeroGen (Ye và cộng sự, 2022); Schick & Schütze (2021); phân loại chỉ dùng tên nhãn (Meng và cộng sự, 2020). Dữ liệu tổng hợp cho giao dịch SME (Aluffi và cộng sự, 2025) | A | — |
| K8 | … nhưng dữ liệu tổng hợp yếu với danh mục mang tính chủ quan | Tính chủ quan của nhiệm vụ và của từng mẫu tương quan nghịch với hiệu quả của dữ liệu tổng hợp (Li và cộng sự, 2023) | A | **Rủi ro trực tiếp**: RL, Mental, Ngu mang tính chủ quan. Biến thành giả thuyết kiểm tra trong RQ1 |
| K9 | Dữ liệu thay đổi theo thời gian | Dữ liệu đề tài: 86,7% khi chia ngẫu nhiên, còn 78,2% khi chia theo thời gian; accuracy theo tháng giảm năm 2026. Tổng quan concept drift (Gama và cộng sự, 2014; Lu và cộng sự, 2019). Bài toán xếp email cũng phải đánh giá theo thời gian (Bekkerman và cộng sự, 2004) | A + B | — |
| K10 | Đánh giá prequential là giao thức phù hợp | Dawid (1984); Gama và cộng sự (2013) | A | — |
| K11 | "Nhớ lại" là baseline mạnh | Thí nghiệm đề tài: nhớ lại đúng 93,8% trên ghi chú đã gặp (61% luồng) | B | Tìm thêm tài liệu dùng láng giềng gần hoặc tra bảng làm baseline cho phân loại giao dịch |
| K12 | Người dùng không phải lúc nào cũng sửa khi gợi ý sai | Thiên kiến tự động hóa: con người có xu hướng chấp nhận gợi ý của máy mà không kiểm tra, nhất là khi bận (Parasuraman & Manzey, 2010). Nhãn nhiễu làm giảm chất lượng mô hình (Song và cộng sự, 2022) | A | TN5 (thí nghiệm nhỏ) |
| K13 | Sai số phân loại làm lệch tổng chi theo danh mục | "Phân loại rồi đếm" là ước lượng chệch của tỷ lệ và tổng chi phí mỗi lớp; có các phương pháp hiệu chỉnh (Forman, 2008) | A | RQ3 mở rộng |
| K14 | Chi tiêu cá nhân khó dự báo: chuỗi ngắn, nhiều nhiễu, nhiều kỳ bằng 0 | Brando và cộng sự (2018) dự báo giao dịch của khách hàng ngân hàng và phải lọc bớt các dự báo có độ tin cậy thấp. Phương pháp cho chuỗi thưa: Croston (1972), TSB (Teunter và cộng sự, 2011). Dữ liệu đề tài: trung bình lịch sử thắng các baseline khác | A + B | — |
| K15 | Cần khoảng dự báo thay vì một con số, và khoảng đó phải chịu được dữ liệu thay đổi | Conformal thích nghi (Gibbs & Candès, 2021); EnbPI (Xu & Xie, 2021) | A | RQ3 mở rộng |
| K16 | Dự báo theo danh mục phải khớp với tổng | Hòa giải dự báo phân cấp MinT (Wickramasuriya và cộng sự, 2019) | A | Tùy chọn trong RQ3 |
| K17 | Kiểm định: McNemar cho phân loại, Diebold–Mariano cho dự báo | Dietterich (1998); Diebold & Mariano (1995) | A | — |
| K18 | Ứng dụng quản lý chi tiêu chủ yếu hỗ trợ ghi chép, ít hỗ trợ lập ngân sách | Rà soát 45 ứng dụng lập ngân sách có điểm cao (Alenazi & Sas, 2023) | A | Dùng ở chương 2 |

---

## 3. Tài liệu theo mảng

### 3.1 Tự theo dõi và gánh nặng nhập liệu
- **Li, Dey & Forlizzi (2010).** *A stage-based model of personal informatics systems.* CHI, 557–566. Mô hình 5 giai đoạn; rào cản ở từng giai đoạn, trong đó có giai đoạn thu thập.
- **Epstein, Ping, Fogarty & Munson (2015).** *A lived informatics model of personal informatics.* UbiComp, 731–742. Phỏng vấn 22 người: chọn công cụ, quên ghi, bỏ dở rồi quay lại.
- **Choe và cộng sự (2017).** *Semi-automated tracking: a balanced approach for self-monitoring applications.* IEEE Pervasive Computing 16(1), 74–84. Kết hợp ghi tay với tự động để giảm gánh nặng mà vẫn giữ được nhận thức của người dùng. Hệ thống của đề tài (máy gợi ý, người xác nhận) đúng là dạng bán tự động này.
- **Kaye và cộng sự (2014).** *Money talks: tracking personal finances.* CHI, 521–530. Nghiên cứu định tính với 14 người về cách theo dõi tài chính, nhấn mạnh yếu tố cảm xúc. *(Chưa đọc được toàn văn.)*
- **Alenazi & Sas (2023).** *Evaluating budgeting apps: limited support for budgeting compared to tracking.* BCS HCI. Rà soát 45 ứng dụng từ 1.335 ứng dụng, dưới góc nhìn kế toán tâm lý.

### 3.2 Kế toán tâm lý (cơ sở cho danh mục tự đặt)
- **Thaler (1999).** *Mental accounting matters.* J. Behavioral Decision Making 12(3), 183–206. Người ta gán các khoản chi vào những tài khoản tâm lý.
- **Heath & Soll (1996).** *Mental budgeting and consumer decisions.* J. Consumer Research 23(1), 40–52. Người ta đặt ngân sách theo nhóm chi và theo dõi chi tiêu theo nhóm đó.

### 3.3 Phân loại giao dịch
- **Dong và cộng sự (2025).** *Transaction categorization with relational deep learning in QuickBooks.* arXiv:2506.09234. Doanh nghiệp tự đặt tên danh mục. Txn-Bert kết hợp GNN trên CSDL quan hệ; cold start được xử lý bằng dữ liệu của các doanh nghiệp khác. Top-1 68,67%, top-5 88,04%. Đánh giá trên tập kiểm tra tĩnh, **không có vòng phản hồi**.
- **Aluffi và cộng sự (2025).** *Categorising SME bank transactions with machine learning and synthetic data generation.* arXiv:2508.05425. Sinh dữ liệu tổng hợp để **bổ sung** cho dữ liệu có nhãn, dùng bộ danh mục cố định. Accuracy 73,49% (±5,09).
- **Moraes và cộng sự (2024).** arXiv:2401.06790. Dùng LLM zero-shot để xây và mở rộng cây chủ đề cho giao dịch ngân hàng bán lẻ.
- Scalable and weakly supervised bank transaction classification, arXiv:2305.18430. Giám sát yếu bằng luật và heuristic. *(Chưa đọc chi tiết.)*

### 3.4 Bài toán tương tự: xếp email vào thư mục do người dùng tạo
- **Segal & Kephart (1999).** *MailCat: an intelligent assistant for organizing e-mail.* AAAI. Gợi ý 3 thư mục, học theo thói quen của từng người. Bản tiếp theo, SwiftFile, học tăng dần (ICML 2000).
- **Bekkerman, McCallum & Huang (2004).** *Automatic categorization of email into folders: benchmark experiments on Enron and SRI corpora.* Chia dữ liệu tăng dần theo thời gian: huấn luyện trên các đoạn trước, kiểm tra trên đoạn sau.

→ Đây là **tiền lệ gần nhất về phương pháp**: danh mục do từng người tạo, gợi ý top-k, học tăng dần, đánh giá theo thời gian. Khác biệt: email là văn bản dài, và các công trình này ra đời trước LLM nên không giải quyết ngày đầu chưa có nhãn.

### 3.5 Phân loại khi không có dữ liệu gán nhãn
- **Meng và cộng sự (2020).** *Text classification using label names only* (LOTClass). EMNLP.
- **Schick & Schütze (2021).** *Generating datasets with pretrained language models.* EMNLP.
- **Ye và cộng sự (2022).** *ZeroGen: efficient zero-shot learning via dataset generation.* EMNLP. Sinh dữ liệu bằng mô hình lớn rồi huấn luyện một mô hình nhỏ, giống thiết kế của đề tài.
- **Li và cộng sự (2023).** *Synthetic data generation with LLMs for text classification: potential and limitations.* EMNLP. Tính chủ quan làm giảm hiệu quả của dữ liệu tổng hợp.
- Embedding đa ngữ: **Chen và cộng sự (2024)** BGE M3-Embedding, Findings of ACL; **Wang và cộng sự (2024)** Multilingual E5, arXiv:2402.05672. Tiếng Việt: **Nguyen & Nguyen (2020)** PhoBERT, Findings of EMNLP.

### 3.6 Học trực tuyến, dữ liệu thay đổi, phản hồi
- **Dawid (1984)**, phương pháp prequential. **Gama, Sebastião & Rodrigues (2013).** *On evaluating stream learning algorithms.* Machine Learning 90(3), 317–346.
- **Gama và cộng sự (2014)**, tổng quan thích nghi với concept drift, ACM Computing Surveys 46(4). **Lu và cộng sự (2019)**, *Learning under concept drift: a review*, IEEE TKDE 31(12).
- **Amershi và cộng sự (2014).** *Power to the people: the role of humans in interactive machine learning.* AI Magazine 35(4).
- **Parasuraman & Manzey (2010).** *Complacency and bias in human use of automation.* Human Factors 52(3).
- **Song và cộng sự (2022).** *Learning from noisy labels with deep neural networks: a survey.* IEEE TNNLS.

### 3.7 Dự báo và lượng hóa (RQ3)
- **Forman (2008).** *Quantifying counts and costs via classification.* Data Mining and Knowledge Discovery 17, 164–206.
- **Brando và cộng sự (2018).** *Uncertainty modelling in deep networks: forecasting short and noisy series.* ECML-PKDD (Applied Data Science).
- **Croston (1972)**; **Teunter, Syntetos & Babai (2011)**, EJOR 214(3). Dự báo chuỗi thưa.
- **Wickramasuriya, Athanasopoulos & Hyndman (2019).** MinT, JASA 114(526), 804–819.
- **Gibbs & Candès (2021).** *Adaptive conformal inference under distribution shift.* NeurIPS. **Xu & Xie (2021).** EnbPI, ICML.
- **Diebold & Mariano (1995)**, JBES. **Dietterich (1998)**, Neural Computation 10(7).

---

## 4. Các công trình gần nhất và khác biệt

| Công trình | Danh mục tự đặt | Ngày đầu, chưa có nhãn nào | Học từ phản hồi, đánh giá theo thời gian | Phản hồi thiếu | Ghi chú tự gõ tiếng Việt | Ảnh hưởng lên dự báo |
|---|---|---|---|---|---|---|
| MailCat / SwiftFile (1999–2000) | ✓ (thư mục) | ✗ | ✓ | ✗ | ✗ | ✗ |
| Bekkerman và cộng sự (2004) | ✓ (thư mục) | ✗ | ✓ (chia theo thời gian) | ✗ | ✗ | ✗ |
| QuickBooks Rel-Cat (2025) | ✓ | Một phần (dựa vào dữ liệu doanh nghiệp khác) | ✗ (tập kiểm tra tĩnh) | ✗ | ✗ | ✗ |
| SME + dữ liệu tổng hợp (2025) | ✗ | ✗ (bổ sung cho dữ liệu có nhãn) | ✗ | ✗ | ✗ | Gián tiếp (cho vay theo dòng tiền) |
| ZeroGen / LOTClass | ✗ (nhãn cố định của benchmark) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Đề tài** | ✓ | ✓ (chỉ từ tên, mô tả và LLM) | ✓ (prequential, tách đã gặp / chưa gặp) | ✓ (TN5) | ✓ | ✓ (RQ3) |

## 5. Kết luận về tính mới (có điều kiện)

Trong phạm vi tìm kiếm ở mục 1, **chưa thấy công trình nào kết hợp cùng lúc**:
1. danh mục do từng người tự định nghĩa, khi người đó **chưa có nhãn nào** và hệ thống **không dựa vào dữ liệu của người dùng khác**;
2. đánh giá prequential quá trình thích nghi theo phản hồi, **so với baseline nhớ lại** và tách riêng ghi chú đã gặp với chưa gặp;
3. phân tích độ nhạy khi phản hồi không đầy đủ;
4. ghi chú chi tiêu tiếng Việt tự gõ;
5. đo ảnh hưởng của lỗi phân loại lên dự báo và cảnh báo ngân sách theo danh mục.

Mỗi thành phần riêng lẻ đều **đã có** trong tài liệu. Đóng góp của đề tài nằm ở **tổ hợp và bối cảnh**, không ở một thuật toán mới. Cần trình bày trung thực như vậy trước hội đồng.

## 6. Những khẳng định chưa có bằng chứng: khảo sát người dùng

Các khẳng định K1 (phần riêng cho chi tiêu), K2 (người Việt tự tạo danh mục) và K3 cần một **khảo sát ngắn** (Google Form, ẩn danh, mục tiêu 30–50 người, làm ở tuần 1–2). Câu hỏi dự kiến:
1. Bạn đã từng ghi chép chi tiêu chưa? Bằng công cụ gì? Còn ghi không, và nếu đã ngừng thì sau bao lâu và vì sao? (chọn nhiều)
2. Bạn dùng danh mục có sẵn, sửa danh mục có sẵn, hay tự tạo danh mục riêng? Tự tạo bao nhiêu danh mục?
3. Trong một lần ghi, phần nào tốn công nhất: gõ nội dung, nhập số tiền, hay chọn danh mục? (thang Likert)
4. Nếu app gợi ý sẵn 3 danh mục, bạn có dùng không? Bạn có kiểm tra lại gợi ý không?
5. Cho 5 ghi chú mẫu, bạn sẽ xếp vào danh mục nào? (Dùng để thấy mỗi người xếp khác nhau, và để thu thêm ghi chú thật.)

Kết quả khảo sát thay thế cho các khẳng định hiện đang ở mức ✗ và C. **Nếu kết quả ngược với giả định** (ví dụ phần lớn không tự tạo danh mục), cần xem lại động cơ của đề tài.
