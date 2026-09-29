# Brainstorm đề tài luận văn CT553H

> Cập nhật: 27/09/2026 · Trạng thái: **đã chọn hướng đề tài #1, đã đổi trọng tâm nghiên cứu (xem 0.1), đang hoàn thiện đề cương, chưa gặp GVHD**

---

## 0. Tóm tắt quyết định

- **Đề tài chọn:** Hệ thống quản lý chi tiêu cá nhân, trong đó **mỗi người dùng tự đặt danh mục chi tiêu của mình**. Bộ phân loại giao dịch **dùng được ngay từ ngày đầu** (nhờ LLM zero-shot và dữ liệu tổng hợp sinh riêng cho danh mục của từng người), rồi **tự thích nghi theo phản hồi sửa nhãn**. Có thêm dự báo chi tiêu.
- **Vai trò của bộ dữ liệu cá nhân (5.465 giao dịch thật, 25 nhãn tự đặt):** không dùng để huấn luyện mô hình ban đầu, mà dùng để **đánh giá hệ thống**. Bộ dữ liệu được **phát lại theo thời gian** như thể một người dùng mới dùng hệ thống từ 09/2022 với 25 danh mục tự tạo: hệ thống đoán nhãn trước, sau đó "người dùng" sửa theo nhãn thật, rồi hệ thống học tiếp (đánh giá kiểu *prequential*, kiểm tra trước, học sau).
- **Trọng tâm khoa học:**
  1. Khi người dùng vừa tạo danh mục riêng mà chưa có giao dịch nào, bộ phân loại đạt đến đâu (RQ1).
  2. Chiến lược thích nghi nào giảm số lần người dùng phải sửa nhãn nhanh nhất, kể cả khi dữ liệu thay đổi theo thời gian và có danh mục mới xuất hiện (RQ2).
  3. Dự báo chi tiêu (RQ3, phụ).
  4. Kiểm tra lại trên dữ liệu tình nguyện viên (RQ4, có điều kiện).
- **Kịch bản phụ:** 25 nhãn được gộp về 10–12 danh mục chuẩn, để so sánh ảnh hưởng của độ chi tiết danh mục.
- **Hội đồng thiên về kỹ thuật phần mềm** (rubric CT553H: 40% phát triển ứng dụng, 40% viết khoa học, 20% trình bày và thái độ): phần hệ thống và quy trình phải chắc chắn. Hướng mới giúp chuyện này tự nhiên hơn, vì **vòng phản hồi, pipeline sinh dữ liệu theo người dùng và pipeline thích nghi chính là đối tượng nghiên cứu**. Công cụ phát lại dữ liệu chạy qua API thật của hệ thống.
- **Đa tiền tệ:** hạ xuống **tính năng phụ của hệ thống**, bỏ khỏi tên đề tài, không còn RQ nào. MVP chỉ giữ mô hình dữ liệu đúng (ví theo loại tiền, tỷ giá lịch sử, đổi tiền) và tính phí đổi tiền ẩn. Người dùng nhiều loại tiền vẫn là **nhóm đối tượng phụ** (mục 4.2).

### 0.1 Thay đổi ngày 27/09/2026 và lý do

| Trước | Sau | Lý do |
|---|---|---|
| Huấn luyện và đánh giá trên cùng dữ liệu cá nhân (kiểm định chéo, chia theo thời gian) | Dữ liệu cá nhân chỉ để **đánh giá**, phát lại theo thời gian. Mô hình ban đầu là LLM zero-shot và mô hình học trên **dữ liệu tổng hợp** | Hệ thống nhiều người dùng phục vụ chủ yếu **người dùng mới chưa có dữ liệu**. Nghiên cứu trên một người có sẵn 4 năm dữ liệu thì không trả lời được bài toán đó |
| Gộp nhãn về 10–12 nhóm chuẩn làm bài toán chính | **Danh mục do người dùng tự tạo** (25 nhãn gốc) là kịch bản chính; danh mục chuẩn là kịch bản phụ | Người dùng thật muốn danh mục của riêng mình. Nhãn của dữ liệu vốn là danh mục cá nhân (AC, RL, Mental…). Đây là chỗ mô hình chung không đủ và lớp cá nhân phải chứng minh giá trị |
| Dữ liệu tổng hợp: không có | Dữ liệu tổng hợp **sinh theo danh mục của từng người dùng** (từ tên và mô tả danh mục) để huấn luyện mô hình riêng cho người đó | Là cách duy nhất để có dữ liệu huấn luyện cho danh mục tự tạo khi người dùng chưa có giao dịch nào |
| RQ1 nhấn mạnh "người bán chưa gặp", GroupKFold theo người bán | Bỏ khái niệm người bán | Dữ liệu là **ghi chú tự viết** (trung vị 2 từ), không phải sao kê ngân hàng ([bao-cao-du-lieu.md](../03-du-lieu/bao-cao-du-lieu.md), mục 7) |
| RQ2b "người dùng mới" phụ thuộc hoàn toàn vào tình nguyện viên | Bài toán người dùng mới được nghiên cứu ngay trên dữ liệu cá nhân (phát lại từ con số 0). Tình nguyện viên chỉ cần **100–200 ghi chú** gán theo danh mục của chính họ (RQ4) | Dữ liệu để đánh giá cần ít hơn nhiều so với dữ liệu để huấn luyện, và tình nguyện viên không phải học bộ danh mục của người khác |
| Đa tiền tệ nằm trong tên đề tài, có RQ3b, có case study giao dịch ngoại tệ thật | Tính năng phụ, bỏ RQ3b, **bỏ case study ngoại tệ** | Không có dữ liệu ngoại tệ thật. RQ3b gượng ép, kết quả gần như biết trước. Phạm vi quá lớn cho 14 tuần |
| Dự báo chi tiêu: RQ3a + RQ3b | RQ3 (phụ), chỉ dự báo, không có tỷ giá | Giữ theo quyết định của người làm đề tài; bỏ phần tỷ giá |

---

## 1. Bối cảnh

| Mục | Nội dung |
|---|---|
| Ngành | Kỹ thuật phần mềm |
| Yêu cầu học phần | Hệ thống phần mềm có hàm lượng khoa học tương đối. Rubric: A. Phát triển ứng dụng 40% · B. Kiến thức, viết khoa học 40% · C. Thái độ, trình bày 20% ([CT553H.pdf](../CT553H.pdf)) |
| Thời gian | 3.5 tháng (~14 tuần), làm một mình |
| Kỹ năng | Java, C, C++, React, Redis, MongoDB, PostgreSQL, Web, AI/ML |
| Sở thích | Thương mại điện tử, khởi nghiệp, hệ thống hoàn chỉnh, quy trình phát triển phần mềm, phần mềm quản lý thông minh, tự động hóa đời sống, tài chính cá nhân, chứng khoán |
| Định hướng | Xây dựng hệ thống kèm hàm lượng nghiên cứu |
| GVHD | Chuyên ngành tin sinh học, chấp nhận đề tài lĩnh vực khác |
| Hội đồng | Thường thiên về kỹ thuật phần mềm |
| Tài nguyên tính toán | Không có lab. Dùng máy cá nhân + Google Colab / Kaggle. API LLM thương mại để sinh dữ liệu tổng hợp |
| Dữ liệu tình nguyện viên | Không cần mẫu cam kết (vẫn ẩn danh hóa trước khi xử lý). Khả năng xin được: **chưa chắc** |

---

## 2. Các ý tưởng đã xem xét

| # | Đề tài | Phần nghiên cứu | Ghi chú |
|---|---|---|---|
| 1 | **Tài chính cá nhân: phân loại giao dịch + dự báo chi tiêu** | Phân loại theo danh mục tự tạo bằng LLM và dữ liệu tổng hợp + thích nghi theo phản hồi; dự báo chuỗi thời gian | **Đã chọn** |
| 2 | Trợ lý mua sắm RAG cho sàn thương mại điện tử | So sánh chiến lược truy xuất (BM25, dense, hybrid, rerank) | Dự phòng |
| 3 | Gợi ý sản phẩm theo phiên | Item-KNN, GRU4Rec, SASRec trên RetailRocket/Olist | Khá phổ biến |
| 4 | OCR hóa đơn, quản lý chi phí cửa hàng nhỏ | OCR + trích xuất thông tin trên MC-OCR 2021 | Có thể làm module mở rộng cho #1 |
| 5 | Quản lý kho thông minh cho SME | Dự báo nhu cầu (ARIMA, Prophet, LightGBM) | |
| 6 | Phân tích, backtest danh mục chứng khoán | Markowitz, Risk Parity, HRP | Phần khoa học dễ bị chất vấn |
| 7 | AI hỗ trợ quản lý dự án phần mềm | Ước lượng story point trên TAWOS | Khó thắng baseline |
| 8 | Phát hiện review giả | Phân loại dữ liệu mất cân bằng | Thiếu dữ liệu |

### So sánh 3 đề tài vào vòng cuối

| Tiêu chí | #1 Tài chính cá nhân | #6 Chứng khoán | #7 AI quản lý dự án |
|---|---|---|---|
| Tính mới | ★★★★ | ★★ | ★★★ |
| Khả thi 3.5 tháng | ★★★★ | ★★★ | ★★★ |
| Dữ liệu | ★★★★★ (có sẵn dữ liệu thật) | ★★★★ | ★★★★ |
| Rủi ro chính | Dữ liệu đánh giá chủ yếu của một người | Kết quả dễ bị bác bỏ, backtest dễ sai | Mô hình khó thắng baseline |
| Khả năng ghi điểm | ★★★★★ | ★★★ | ★★★★ |

**Lấy điểm mạnh của #7:** báo cáo thể hiện rõ quy trình phát triển phần mềm (Scrum, CI/CD, kiểm thử tự động).

---

## 3. Liên hệ với chuyên môn của GVHD

Theo danh sách công bố trong [cong-bo-gvhd.md](../02-khao-sat/cong-bo-gvhd.md), GVHD mạnh về **BERT/transformer, CNN, word embedding, SHAP, RAG**, và thường trình bày nghiên cứu theo **quy tắc 5 bước của Chou**. Đề tài chạm tới các mảng này ở: embedding (bộ nhớ kNN, embedding zero-shot), **RAG** (LLM few-shot lấy ví dụ từ lịch sử sửa nhãn của người dùng), PhoBERT (kịch bản phụ danh mục chuẩn).

Khung 5 bước chỉ là **cách trình bày gợi ý** để GVHD dễ hướng dẫn. Hội đồng thiên kỹ thuật phần mềm không đòi hỏi khung này, nên hỏi GVHD trước khi dùng.

| Bước (Chou's 5-step rule) | Áp dụng vào đề tài |
|---|---|
| 1. Xây dựng bộ dữ liệu chuẩn | (a) **Luồng đánh giá**: 5.028 khoản chi thật đã làm sạch, ẩn danh, sắp theo thời gian, nhãn là 25 danh mục tự đặt. (b) **Tập dev**: mẫu ngẫu nhiên ~10%, chỉ dùng để tinh chỉnh, không tính điểm. (c) **Tên và mô tả** của 25 danh mục, viết một lần trước thí nghiệm. (d) **Dữ liệu tổng hợp** sinh từ tên và mô tả danh mục. (e) Gán nhãn lại mù một mẫu, đo Cohen's kappa |
| 2. Biểu diễn mẫu | TF-IDF (n-gram từ và ký tự), embedding đa ngôn ngữ (bge-m3, multilingual-e5), PhoBERT (kịch bản phụ) |
| 3. Thuật toán | Mô hình ban đầu: LLM zero-shot, embedding zero-shot, mô hình nhẹ học trên dữ liệu tổng hợp của từng người. Chiến lược thích nghi: bộ nhớ tra cứu, kNN trực tuyến, huấn luyện lại định kỳ, LLM few-shot truy xuất (RAG) |
| 4. Kiểm định | **Phát lại theo thời gian** (prequential), không tính điểm trên tập dev. Kiểm tra độc lập trên dữ liệu tình nguyện viên (nếu có). McNemar, bootstrap, nhiều seed |
| 5. Web server | Chính là hệ thống hoàn chỉnh đã triển khai. Công cụ phát lại chạy qua API thật của hệ thống |

Giải thích dự đoán: với bộ nhớ kNN, lời giải thích có sẵn và dễ hiểu (*"giống giao dịch 'cf với [P03]' bạn đã xếp vào RL"*). SHAP chỉ là tùy chọn. Báo cáo thêm **MCC**, độ đo GVHD hay dùng.

---

## 4. Đề cương chi tiết

### 4.1 Tên đề tài (đề xuất, cần chốt với GVHD)

**Phương án chính**
- **Tiếng Việt:** Xây dựng hệ thống quản lý chi tiêu cá nhân với bộ phân loại giao dịch tự thích nghi theo phản hồi người dùng và dự báo chi tiêu
- **Tiếng Anh:** Building a Personal Expense Management System with a Feedback-Adaptive Transaction Classifier and Spending Forecasting

**Phương án khác**
- Nhấn vào danh mục tự tạo: *Xây dựng hệ thống quản lý chi tiêu cá nhân với phân loại giao dịch theo danh mục do người dùng định nghĩa, ứng dụng LLM và dữ liệu tổng hợp*.
- Ngắn gọn: *Hệ thống quản lý chi tiêu cá nhân thông minh: phân loại giao dịch thích nghi và dự báo chi tiêu*.

### 4.2 Lý do chọn đề tài và đối tượng người dùng

- Ghi chép chi tiêu thủ công tốn thời gian, người dùng hay bỏ cuộc. Mỗi lần ghi phải gõ nội dung **và** chọn danh mục.
- Ghi chú tiếng Việt do người dùng tự gõ rất ngắn, viết tắt, không dấu, sai chính tả ("cf", "cơm sờn", "xang").
- **Mỗi người có bộ danh mục riêng.** Các app ghi chép phổ biến đều cho người dùng tự tạo danh mục, và người dùng có thói quen riêng: cùng "cafe" có người xếp vào Ăn uống, có người xếp vào Gặp bạn bè. Một mô hình học trên bộ danh mục cố định thì không dùng được cho danh mục tự tạo.
- **Bài toán người dùng mới:** mô hình học máy thông thường cần hàng trăm giao dịch đã gán nhãn của chính người đó mới dùng được. Đúng lúc người dùng dễ bỏ cuộc nhất (những tuần đầu), hệ thống lại chưa giúp được gì.
- **Đối tượng chính:** người Việt tự ghi chép chi tiêu hằng ngày (sinh viên, người đi làm).
- **Đối tượng phụ:** người có thu nhập và chi tiêu bằng nhiều loại tiền (du học sinh, người làm việc ở nước ngoài, freelancer nhận ngoại tệ), được phục vụ bằng tính năng đa tiền tệ (mục 5).

### 4.3 Mục tiêu

**Tổng quát:** xây dựng hệ thống web hoàn chỉnh quản lý chi tiêu cá nhân, trong đó bộ phân loại giao dịch làm việc với danh mục do người dùng tự đặt, dùng được ngay từ ngày đầu và ngày càng chính xác hơn nhờ phản hồi của từng người.

**Cụ thể:**
1. Xây dựng và đánh giá bộ phân loại ban đầu cho danh mục tự tạo, không cần giao dịch nào của người dùng: LLM zero-shot và mô hình học trên dữ liệu tổng hợp sinh từ tên và mô tả danh mục.
2. Thiết kế và so sánh các chiến lược thích nghi theo phản hồi sửa nhãn, đánh giá bằng cách phát lại 4 năm dữ liệu thật theo thời gian.
3. So sánh các mô hình dự báo chi tiêu tuần với baseline đơn giản.
4. Xây dựng, kiểm thử, triển khai hệ thống theo quy trình Scrum và CI/CD. Tích hợp mô hình vào hệ thống có quản lý phiên bản và giám sát tỷ lệ sửa nhãn.
5. (Phụ) Mô hình dữ liệu đa tiền tệ đúng chuẩn, theo tinh thần VAS 10 / IAS 21.

### 4.4 Câu hỏi nghiên cứu

| RQ | Câu hỏi | Bắt buộc? |
|---|---|---|
| RQ1 | Khi người dùng **vừa tạo danh mục riêng** mà chưa có giao dịch nào, bộ phân loại ban đầu đạt đến đâu trên ghi chú chi tiêu thật? So sánh LLM zero-shot (local và API), embedding zero-shot, và mô hình nhẹ học trên **dữ liệu tổng hợp sinh riêng cho danh mục của người dùng**. Mô tả danh mục giúp được bao nhiêu so với chỉ có tên? Cần bao nhiêu ví dụ tổng hợp mỗi danh mục? | Có |
| RQ2 | Khi hệ thống học từ phản hồi sửa nhãn, **chiến lược thích nghi nào giảm số lần người dùng phải sửa nhanh nhất** với chi phí (độ trễ, tài nguyên) chấp nhận được? Sau bao nhiêu giao dịch thì vượt mô hình ban đầu? Khi dữ liệu thay đổi theo thời gian (**danh mục mới được tạo**, thói quen đổi), chiến lược nào chịu được tốt nhất? | Có |
| RQ3 | Mô hình dự báo chi tiêu tuần nào vượt được baseline "trung bình lịch sử", và chênh lệch có ý nghĩa thống kê không? | Có (phụ) |
| RQ4 | Kết luận của RQ1–RQ2 có lặp lại trên dữ liệu và danh mục của người dùng khác không? | Có điều kiện: cần tối thiểu 3 tình nguyện viên (mục 6, TN4) |

Kịch bản phụ **danh mục chuẩn** (25 nhãn gộp về 10–12 nhóm) được chạy trong TN1 và TN2 để so sánh, không phải RQ riêng.

### 4.5 Phạm vi

| MVP (bắt buộc) | Mở rộng (nếu kịp) | Ngoài phạm vi |
|---|---|---|
| Web responsive, nhiều người dùng | Phân rã biến động tài sản do chi tiêu / do tỷ giá (5.3-7) | App mobile native |
| CRUD giao dịch, import CSV | Ngân sách theo quốc gia (5.3-8) | Kết nối API ngân hàng |
| **Danh mục tự tạo** (tên + mô tả tùy chọn); bộ danh mục mặc định cho người không muốn tự tạo | Gợi ý lượng ngoại tệ cần đổi (5.3-11) | **Dự đoán tỷ giá**, tư vấn đầu tư |
| **Sinh dữ liệu tổng hợp theo danh mục** khi người dùng tạo danh mục, huấn luyện mô hình riêng chạy nền | So sánh chi tiêu theo PPP | Thuế thu nhập nhiều quốc gia |
| **Gợi ý danh mục khi nhập** + **vòng phản hồi** cập nhật lớp cá nhân | Phát hiện giao dịch bất thường, OCR hóa đơn | Thanh toán, chuyển tiền thật |
| Quản lý phiên bản mô hình, giám sát tỷ lệ sửa nhãn | | Phân loại giao dịch tiếng nước ngoài |
| Ngân sách, cảnh báo, dashboard, dự báo | | |
| Ví theo từng loại tiền, tỷ giá lịch sử, đổi tiền, **phí đổi tiền ẩn** (phụ) | | |

### 4.6 Chức năng chính

**Người dùng:**
- Đăng ký, đăng nhập (JWT), chọn tiền tệ báo cáo và múi giờ.
- **Quản lý danh mục:** dùng bộ mặc định hoặc tự tạo (tên, mô tả ngắn tùy chọn). Khi tạo, sửa hoặc xóa danh mục, hệ thống sinh lại dữ liệu tổng hợp và huấn luyện lại mô hình riêng ở chế độ nền.
- Quản lý ví (mỗi ví một loại tiền).
- CRUD giao dịch, import CSV/Excel.
- **Gợi ý danh mục khi gõ ghi chú**, kèm độ tin cậy và lời giải thích ("giống giao dịch X bạn đã xếp vào Y"). Khi người dùng sửa, lớp cá nhân được cập nhật ngay.
- Import hàng loạt: phân loại tự động cả file, người dùng duyệt các dòng có độ tin cậy thấp.
- Đổi tiền giữa ví: nhập số tiền hai bên, hệ thống tính phí ẩn so với tỷ giá thị trường.
- Ngân sách theo danh mục, cảnh báo khi sắp vượt.
- Dashboard chi tiêu, dự báo chi tiêu tuần tới.
- Xuất báo cáo PDF/Excel.

**Quản trị viên:** quản lý bộ danh mục mặc định, cấu hình bộ sinh dữ liệu (model, prompt, số ví dụ mỗi danh mục), quản lý phiên bản mô hình, theo dõi **tỷ lệ sửa nhãn theo tuần** trên toàn hệ thống (cùng độ đo với thí nghiệm offline), theo dõi chi phí gọi API.

### 4.7 Kiến trúc

```
┌─────────────┐      ┌──────────────────────────┐      ┌───────────────────────────────────┐
│  React SPA  │─────▶│   Spring Boot (Java)     │─────▶│  ML Service (FastAPI)             │
│  (Vite, TS) │ REST │  - Auth, Wallet, Txn     │ REST │  - /categories: sinh dữ liệu tổng │
└─────────────┘      │  - Category (tự tạo)     │      │    hợp + huấn luyện mô hình riêng │
                     │  - Budget, Alert         │      │  - /categorize: mô hình ban đầu   │
                     │  - Money/FX (phụ)        │      │    + lớp cá nhân theo user        │
                     │  - Scheduler (tỷ giá)    │      │  - /feedback: cập nhật ngay       │
                     └───┬──────────┬───────────┘      │  - /retrain (định kỳ), /forecast  │
                         │          │                  └──────┬─────────────────┬──────────┘
                  ┌──────▼───────┐ ┌▼──────────┐              │                 │
                  │ PostgreSQL   │ │ Redis     │◀─────────────┘          ┌──────▼────────┐
                  │ + pgvector   │ │ cache,    │  hàng đợi sinh dữ liệu  │ LLM API       │
                  │ (bộ nhớ kNN  │ │ hàng đợi  │  và huấn luyện nền      │ (chỉ nhận tên │
                  │  theo user)  │ └───────────┘                         │ + mô tả danh  │
                  └──────────────┘                                       │ mục)          │
        Công cụ phát lại (replay): đọc CSV → gọi API thật → ghi kết quả  └───────────────┘
        Docker Compose · GitHub Actions CI/CD · Triển khai VPS
```

- **PostgreSQL:** dữ liệu tài chính cần tính toàn vẹn (ACID), kiểu `NUMERIC` chính xác. **pgvector** lưu embedding của các giao dịch đã sửa nhãn theo từng người dùng, dùng cho kNN, nên không cần thêm vector DB riêng. *(Cần kiểm tra lại khi thiết kế.)*
- **Redis:** cache tỷ giá và dashboard; **hàng đợi** cho tác vụ sinh dữ liệu tổng hợp và huấn luyện lại (chạy nền, vì gọi LLM mất vài giây đến vài chục giây).
- **Sinh dữ liệu theo người dùng:** khi người dùng tạo danh mục, ML service gửi **tên và mô tả của toàn bộ danh mục** của người đó cho LLM (để ví dụ sinh ra phân biệt được các danh mục gần nhau như AC và AV), nhận về ví dụ tổng hợp, lưu lại, rồi huấn luyện mô hình nhẹ riêng cho người đó. **Không gửi ghi chú giao dịch** đi. Trong lúc chờ, hệ thống dùng LLM zero-shot hoặc embedding zero-shot.
- **LLM dùng để phân loại trong hệ thống** (local hay API, hay chỉ dùng mô hình học trên dữ liệu tổng hợp): **chưa quyết định, chờ kết quả RQ1** (độ chính xác, độ trễ, chi phí, quyền riêng tư). Ghi chú chi tiêu là dữ liệu nhạy cảm, nên đây là tiêu chí phải cân nhắc khi chọn.
- **ML service** chỉ nạp mô hình và mã đã xuất ra từ `ml/`. Lớp cá nhân (dữ liệu tổng hợp, mô hình riêng, bộ nhớ, kNN) được tạo trong lúc chạy và có số phiên bản.
- **Công cụ phát lại** vừa là công cụ thí nghiệm vừa là **kiểm thử tích hợp**: chạy luồng dữ liệu thật qua API của hệ thống đã triển khai, kể cả sự kiện "người dùng tạo danh mục mới". Số liệu cuối cùng trong luận văn là số của **chính hệ thống**, không chỉ của notebook.

---

## 5. Bài toán đa tiền tệ (tính năng phụ)

> **Trạng thái từ 27/09/2026:** không còn gánh phần khoa học, không có dữ liệu thật, không có RQ. Chỉ giữ trong MVP: **(1)–(4)** mô hình dữ liệu và **(5)** phí ẩn. Các mục khác chuyển sang "nếu kịp". Toàn bộ phần này là tính toán xác định, được kiểm chứng bằng **unit test với kịch bản tính tay**. Khảo sát chi tiết: [khao-sat-xu-ly-da-tien-te.md](../02-khao-sat/khao-sat-xu-ly-da-tien-te.md). Giữ nguyên số mục để các liên kết từ tài liệu khảo sát không bị lệch.

### 5.1 Tình huống minh họa (persona của nhóm đối tượng phụ)

> **Minh, du học sinh ở Nhật.** Gia đình chuyển VND hằng tháng, làm thêm nhận JPY, học phí và tiền nhà trả bằng JPY, thỉnh thoảng quẹt thẻ Visa VND ở Nhật, đổi tiền qua ngân hàng hoặc dịch vụ chuyển tiền.
>
> **Minh muốn biết:** tổng tài sản hiện tại? Mất bao nhiêu tiền cho phí đổi tiền?

### 5.2 Các vấn đề cần giải quyết

| # | Vấn đề | Nếu làm sai | Trạng thái |
|---|---|---|---|
| 1 | Lưu số tiền của nhiều loại tiền | Sai số làm tròn (dùng `float`), sai số chữ số thập phân (JPY 0, USD 2, KWD 3) | MVP |
| 2 | Quy đổi để báo cáo | Tổng hợp vô nghĩa khi cộng thẳng VND với JPY | MVP |
| 3 | Chọn tỷ giá nào, ngày nào | Báo cáo tháng cũ thay đổi mỗi ngày vì dùng tỷ giá hiện tại | MVP |
| 4 | Đổi tiền / chuyển giữa ví | Bị tính thành chi tiêu và thu nhập ảo | MVP |
| 5 | Phí đổi tiền ẩn trong tỷ giá | Người dùng không biết mình mất tiền | MVP |
| 6 | Quẹt thẻ ở nước ngoài | Hai số tiền (tiền gốc và tiền bị trừ) + phí giao dịch nước ngoài | MVP (chỉ lưu 2 số tiền) |
| 7 | Tài sản thay đổi do tỷ giá | Tưởng mình tiết kiệm được hoặc bị lỗ, thực ra là do tỷ giá | Nếu kịp |
| 8 | Ngân sách khi chi bằng nhiều loại tiền | Không biết đã tiêu bao nhiêu so với hạn mức | Nếu kịp (MVP chỉ quy đổi về tiền của ngân sách) |
| 9 | So sánh chi tiêu giữa các nước | Sức mua khác nhau | Nếu kịp |
| 10 | Múi giờ | Giao dịch lúc 23h ở nước khác bị tính sang ngày khác | MVP (lưu `timestamptz` + múi giờ) |
| 11 | Thiếu tiền ở một loại tiền | Tổng tài sản đủ nhưng không có JPY để trả tiền nhà | Nếu kịp |

### 5.3 Giải pháp

#### (1) Lưu trữ tiền
- **Luôn lưu số tiền gốc và loại tiền gốc** (mã ISO 4217). Không bao giờ chỉ lưu số đã quy đổi.
- PostgreSQL `NUMERIC(19,4)` hoặc `BIGINT` theo đơn vị nhỏ nhất. Java dùng `BigDecimal` hoặc Java Money API (JSR 354, Moneta). **Không dùng `double`/`float`.**
- Bảng `currencies` lưu `minor_unit`. Frontend hiển thị bằng `Intl.NumberFormat`.

#### (2) Ví theo tiền tệ và tiền tệ báo cáo
- Mỗi ví có **một** loại tiền cố định. Ví đa tiền tệ (Wise, Revolut) được mô hình hóa thành nhiều ví con.
- Mỗi người dùng chọn một **tiền tệ báo cáo**. Mọi thống kê tổng hợp quy về tiền tệ này.

#### (3) Tỷ giá: nguồn, loại, quy tắc tra cứu
- Bảng `exchange_rates` lưu lịch sử theo ngày. Job hằng ngày lấy tỷ giá, cache Redis, có nguồn dự phòng, cho phép nhập tay.
- Nguồn tham khảo (cần kiểm tra lại điều khoản): Vietcombank, tỷ giá trung tâm NHNN, open.er-api.com / exchangerate-api. **Frankfurter (ECB) không có VND.**
- Quy tắc (theo tinh thần VAS 10 / IAS 21): thu/chi quy đổi theo **tỷ giá ngày giao dịch** và lưu lại `fx_rate_to_base`; số dư và tổng tài sản quy đổi theo **tỷ giá lúc xem**; ngày không có tỷ giá thì dùng tỷ giá gần nhất **trước đó**; quy đổi chéo đi qua USD.

#### (4) Đổi tiền và chuyển giữa ví
- Loại giao dịch: `INCOME`, `EXPENSE`, `TRANSFER` (cùng tiền), `EXCHANGE` (khác tiền), `LOAN` (vay/cho vay, xem [bao-cao-du-lieu.md](../03-du-lieu/bao-cao-du-lieu.md) mục 4.4).
- `TRANSFER`, `EXCHANGE`, `LOAN` **không tính là thu nhập hay chi tiêu**. Hai vế liên kết bằng `transfer_group_id`.
- Dữ liệu cá nhân không có giao dịch chuyển khoản nội bộ, nên **không đưa nhãn này vào thí nghiệm phân loại**.

#### (5) Phí đổi tiền ẩn
Người dùng nhập số tiền **hai bên**. Hệ thống tính:

```
tỷ_giá_thực_tế     = số_tiền_nhận / số_tiền_gửi
giá_trị_thị_trường = số_tiền_gửi × tỷ_giá_mid_market(ngày đó)
phí_ẩn             = giá_trị_thị_trường − số_tiền_nhận
tỷ_lệ_phí          = phí_ẩn / giá_trị_thị_trường
```

*Ví dụ (giả định):* đổi 10.000.000 VND lấy 380 USD, tỷ giá thị trường 25.400 thì 10 triệu VND tương đương 393,7 USD, phí ẩn 13,7 USD (~3,5%).

- Chuẩn chính: tỷ giá **mid-market** (World Bank *Remittance Prices Worldwide*; Quy định EU 2019/518). *(Cần đọc văn bản gốc trước khi trích dẫn.)*
- Chỉ có tỷ giá theo ngày, nên chênh lệch nhỏ (khoảng dưới 0,3–0,5%) hiển thị là "không đáng kể". Nêu điểm này trong phần hạn chế.
- Phí ẩn ghi thành khoản chi thuộc danh mục "Phí đổi tiền". Dashboard thống kê theo tháng và theo kênh đổi.

#### (6) Quẹt thẻ ở nước ngoài
Lưu cả `original_amount` + `original_currency` và số tiền thực bị trừ trên thẻ. Chênh lệch so với tỷ giá thị trường là phí, ghi nhận như (5).

#### (7) Phân rã biến động tài sản *(nếu kịp)*
Tách biến động tổng tài sản thành phần do dòng tiền và phần do tỷ giá. **Lưu ý:** công thức cũ (định giá dòng tiền theo tỷ giá đầu kỳ) chưa khớp với cách lưu `amount_base` theo tỷ giá ngày giao dịch. Khi làm thì dùng cách 3 phần (thu − chi theo `amount_base`, phần còn lại là hiệu ứng tỷ giá), xem [khao-sat-xu-ly-da-tien-te.md](../02-khao-sat/khao-sat-xu-ly-da-tien-te.md) mục 7.2(b). Khái niệm này đã có trong kế toán kép (GnuCash trading accounts, hledger `--gain`), nên phải viết là "đưa vào giao diện cho người không biết kế toán", không viết là "mới".

#### (8) Ngân sách đa tiền tệ *(MVP tối thiểu)*
Mỗi ngân sách có một loại tiền. Khoản chi bằng loại tiền khác được quy đổi theo tỷ giá ngày giao dịch. Ngân sách theo quốc gia và tự nhận biết bối cảnh quốc gia là phần "nếu kịp".

#### (9) So sánh chi tiêu giữa các nước theo PPP *(nếu kịp)*

#### (10) Múi giờ
Lưu `timestamptz` (UTC) kèm múi giờ địa phương. Thống kê theo ngày dùng ngày địa phương.

#### (11) Gợi ý lượng ngoại tệ cần đổi *(nếu kịp)*
Dùng lại mô hình dự báo của RQ3 cho chuỗi chi tiêu từng loại tiền: `cần_đổi = max(0, dự_báo_P80 − số_dư_hiện_có)`. Không dự đoán thời điểm đổi. Không có dữ liệu để đánh giá nghiêm túc, nên nếu làm thì chỉ trình bày như một tính năng.

### 5.4 Thiết kế CSDL (phần liên quan)

```sql
currencies      (code CHAR(3) PK, name, symbol, minor_unit SMALLINT)
users           (id, email, base_currency → currencies, default_timezone)
wallets         (id, user_id, name, type, currency → currencies, archived)
exchange_rates  (rate_date, base, quote, rate NUMERIC(20,10), rate_type, source,
                 PK(rate_date, base, quote, rate_type, source))
categories      (id, user_id NULL,                  -- NULL = bộ danh mục mặc định
                 name, description NULL,            -- đầu vào của LLM zero-shot và bộ sinh dữ liệu
                 created_at, archived)
synthetic_examples (id, category_id, text, generator_model, generator_version, created_at)
transactions    (id, user_id, wallet_id,
                 type            -- INCOME | EXPENSE | TRANSFER | EXCHANGE | LOAN
                 amount NUMERIC(19,4), currency,
                 original_amount, original_currency,
                 fx_rate_to_base NUMERIC(20,10), amount_base NUMERIC(19,4),
                 occurred_at TIMESTAMPTZ, local_tz,
                 description, category_id,
                 category_source -- USER | MODEL
                 model_confidence, model_version,
                 transfer_group_id)
category_feedback (id, user_id, transaction_id, predicted_category, corrected_category,
                   model_version, created_at)       -- nguồn dữ liệu cho lớp cá nhân và giám sát
user_models     (user_id, version, kind, artifact_path, trained_at, metrics_json)
user_memory     (user_id, transaction_id, text_norm, embedding VECTOR(n), category_id)  -- pgvector
budgets         (id, user_id, category_id, currency, amount, period)
```

### 5.5 Những điều không làm, và lý do
- **Dự đoán tỷ giá / thời điểm đổi tiền tối ưu:** không đủ cơ sở khoa học, dễ bị chất vấn.
- **Thuế thu nhập nhiều quốc gia, kết nối ngân hàng nước ngoài:** ngoài phạm vi 14 tuần.
- **Thí nghiệm dự báo có tỷ giá (RQ3b cũ):** bỏ, vì phải giả lập người dùng không có thật và kết quả gần như biết trước.
- **Case study giao dịch ngoại tệ thật:** bỏ.

### 5.6 Dữ liệu
Bộ dữ liệu cá nhân chỉ có VND. Phần đa tiền tệ không cần dữ liệu huấn luyện, chỉ cần tỷ giá lịch sử công khai và unit test.

### 5.7 Khảo sát hiện trạng (tìm ngày 24/09/2026)

**Kết luận ngắn:** hỗ trợ đa tiền tệ cơ bản đã phổ biến. Tính phí đổi tiền ẩn cho từng giao dịch thì chưa thấy trong các app quản lý chi tiêu được khảo sát. Lãi/lỗ tỷ giá đã có trong phần mềm kế toán kép.

| Tính năng | Hiện trạng | Ví dụ |
|---|---|---|
| Ví theo loại tiền, tiền tệ báo cáo, tỷ giá tự động | **Đã phổ biến** | Toshl, PocketSmith, Firefly III, Lunch Money, Spendee, Wallet, MoneyWiz, Money Lover |
| Tỷ giá lịch sử theo ngày giao dịch | **Đã có** | Toshl, Firefly III, Lunch Money |
| Ngân sách theo loại tiền | **Đã có** | PocketSmith, Toshl, Firefly III |
| Dự báo dòng tiền | **Có, dạng lập lịch/quy tắc** | PocketSmith (không dùng ML) |
| Tách biến động tài sản do tỷ giá | **Có trong kế toán kép**, chưa thấy trong app chi tiêu phổ thông | GnuCash trading accounts, hledger `--gain` |
| **Tự tính phí đổi tiền ẩn** cho từng giao dịch | **Chưa thấy** trong app quản lý chi tiêu. Chỉ có công cụ so sánh nhà cung cấp chuyển tiền (Wise, Remitto) | |

**Khảo sát liên quan đến trọng tâm ML (cần làm, xem mục 11):**
- Phân loại giao dịch bằng ML đã được nghiên cứu nhiều với tiếng Anh: Txn-Bert (QuickBooks, arXiv 2506.09234), phân loại giao dịch SME **bằng dữ liệu tổng hợp** (arXiv 2508.05425, gần với hướng mới), TopoLedgerBERT (arXiv 2407.05175).
- Cần tìm thêm về: LLM zero-shot cho phân loại văn bản ngắn; phân loại với **nhãn do người dùng định nghĩa** (open-set, label-name-only classification); huấn luyện trên dữ liệu do LLM sinh (sim-to-real gap); học trực tuyến / học liên tục với phản hồi người dùng; cold-start cá nhân hóa; đánh giá prequential.
- Cần kiểm tra các app ghi chép (Money Lover, MISA, Spendee…) có gợi ý danh mục tự tạo bằng ML không, hay chỉ theo luật / lịch sử.
- Nên viết *"chưa tìm thấy trong các ứng dụng và công trình được khảo sát"*, **không** viết *"chưa ai làm"*.

**Nguồn:** [Toshl](https://toshl.com/currencies/) · [Firefly III](https://docs.firefly-iii.org/explanation/financial-concepts/exchange-rates/) · [PocketSmith multi-currency](https://www.pocketsmith.com/tour/multi-currency/) · [PocketSmith forecasts](https://www.pocketsmith.com/tour/cash-flow-forecasts/) · [Lunch Money](https://lunchmoney.app/features/multicurrency/) · [YNAB](https://support.ynab.com/en_us/using-multiple-currencies-in-ynab-a-guide-SyBF6PHno) · [Wealthfolio](https://wealthfolio.app/docs/concepts/market-data-and-fx/) · [Money Lover](https://moneylover.me/vi/) · [arXiv 2506.09234](https://arxiv.org/abs/2506.09234) · [arXiv 2508.05425](https://arxiv.org/abs/2508.05425) · [arXiv 2407.05175](https://arxiv.org/abs/2407.05175)

---

## 6. Thiết kế thí nghiệm

### Bước 0: Chuẩn bị dữ liệu

**0.1 Danh mục của người dùng giả lập (kịch bản chính)**
- 25 nhãn chi gốc được coi là **danh mục người dùng tự tạo**. Sửa lỗi chính tả tên nhãn (`Badmintion` → `Badminton`), nhưng không đổi nghĩa.
- Viết **mô tả ngắn một câu** cho mỗi danh mục, như một người dùng bình thường sẽ viết khi tạo danh mục (ví dụ *AC: "bữa ăn chính trong ngày"*, *RL: "ăn uống, đi chơi cùng bạn bè"*). Viết **một lần, trước khi chạy thí nghiệm**, lưu vào config và không sửa theo kết quả trên luồng đánh giá.
- Hai biến thể thông tin danh mục: **chỉ tên** và **tên + mô tả**. Với tên viết tắt như AC, DC, RL, biến thể chỉ tên sẽ rất thấp. Đó là một kết quả, không phải lỗi: nó trả lời câu hỏi "có nên khuyến khích người dùng viết mô tả không".
- **Thời điểm tạo danh mục:** một danh mục được coi là "vừa được tạo" ngay trước giao dịch đầu tiên mang nhãn đó trong luồng (5 nhãn chỉ xuất hiện từ 2025). Như vậy, tại mỗi thời điểm hệ thống chỉ biết các danh mục đã tồn tại, đúng như ngoài đời.
- `Cho vay` chuyển sang loại giao dịch `LOAN`, không nằm trong bài toán phân loại.

**0.2 Kịch bản phụ: danh mục chuẩn**
- Viết **bảng ánh xạ** 25 nhãn về 10–12 danh mục chuẩn (phương án gộp ở [bao-cao-du-lieu.md](../03-du-lieu/bao-cao-du-lieu.md), mục 8), kèm mô tả mỗi danh mục chuẩn. Viết **trước khi chạy thí nghiệm**, căn cứ vào định nghĩa nhãn chứ không căn cứ vào kết quả.
- Dùng chung khung phát lại và bộ sinh dữ liệu, chỉ khác danh sách danh mục đầu vào. Ở kịch bản này có thể sinh một tập tổng hợp lớn dùng chung (5.000–12.000 mẫu) và thử fine-tune PhoBERT.

**0.3 Tập dev và luồng đánh giá**
- **Tập dev** = mẫu ngẫu nhiên khoảng **10%** số khoản chi (~500 giao dịch, seed cố định). Mọi việc tinh chỉnh (prompt LLM, prompt sinh dữ liệu, số ví dụ mỗi danh mục, siêu tham số, ngưỡng tin cậy, cách kết hợp mô hình) chỉ được nhìn kết quả trên tập này.
- **Luồng đánh giá** = toàn bộ luồng theo thời gian. **Đề xuất:** giao dịch thuộc tập dev vẫn đi qua luồng như bình thường (hệ thống vẫn nhận phản hồi và học từ chúng, vì ngoài đời người dùng vẫn nhập các giao dịch này), nhưng **không được tính điểm**. Nhờ vậy luồng không bị thủng. *(Cần xác nhận lại với GVHD.)*
- **Khóa cấu hình** (ghi ra file config, commit) trước khi tính điểm trên luồng. Không quay lại sửa theo kết quả.
- **Thành thật về giới hạn:** người làm đề tài đã xem toàn bộ dữ liệu khi làm EDA, và tự viết mô tả danh mục. Dev và luồng đánh giá là của cùng một người, và vì dev lấy ngẫu nhiên nên trùng nội dung với luồng (ví dụ "xăng"). Nêu rõ những điều này trong luận văn. Kiểm tra trên tình nguyện viên (TN4) là cách giảm nghi ngờ.

**0.4 Làm sạch và chất lượng nhãn**
- Rà soát 154 giao dịch có nhãn thiểu số và 164 giao dịch có ngày bất thường (báo cáo dữ liệu, mục 4).
- **Đo độ nhất quán của nhãn:** lấy ngẫu nhiên 300 giao dịch, gán lại **theo 25 danh mục** mà không nhìn nhãn cũ, tính Cohen's kappa. Kappa của kịch bản danh mục chuẩn suy ra được qua bảng ánh xạ. Đây là **giới hạn trên của con người**.

**0.5 Bộ sinh dữ liệu tổng hợp**
- Sinh bằng **API LLM thương mại**. Đầu vào **chỉ gồm** tên và mô tả (nếu có) của **toàn bộ danh mục** của người dùng. Đưa cả danh sách vào một prompt để ví dụ sinh ra phân biệt được các danh mục gần nhau (AC và AV, Coffee và RL). **Không đưa ghi chú thật nào vào prompt**, kể cả làm ví dụ.
- Yêu cầu đa dạng: có dấu / không dấu, viết tắt, lỗi gõ, có / không có tên quán hay thương hiệu, độ dài 1–6 từ.
- Số ví dụ mỗi danh mục là một biến thí nghiệm: **10 / 30 / 100**. Khi có danh mục mới, sinh thêm cho danh mục đó (và có thể sinh lại cho các danh mục gần nó).
- **Lưu toàn bộ prompt, tên và phiên bản model, tham số, đầu ra** vào file để tái lập. Không sinh lại mỗi lần chạy thí nghiệm. Ghi lại chi phí và thời gian sinh (đây cũng là chi phí của hệ thống thật mỗi khi người dùng tạo danh mục).
- Báo cáo **tỷ lệ trùng** giữa dữ liệu tổng hợp và luồng đánh giá. Không xóa, chỉ báo cáo.

### Kiểm tra nhanh trước khi cam kết (tuần 2)
Trên **tập dev**, với 25 danh mục (tên + mô tả):
- Chạy LLM zero-shot local; sinh 30 ví dụ mỗi danh mục rồi huấn luyện TF-IDF + LR.
- Mục đích: kiểm tra toàn bộ đường ống và ước lượng mức khởi điểm.
- Nếu mức khởi điểm **dưới khoảng 40%**: xem lại prompt sinh và prompt phân loại (vẫn chỉ trên dev) trước khi đi tiếp.
- Nếu mức khởi điểm **đã trên khoảng 85%**: RQ2 còn ít chỗ để cải thiện. Khi đó trình bày biến thể "chỉ tên" và các giai đoạn có danh mục mới làm trọng tâm của RQ2.

### TN1: Bộ phân loại ban đầu, khi chưa có giao dịch nào (RQ1)

| Nhóm | Mô hình | Dùng được cho danh mục tự tạo? |
|---|---|---|
| Baseline | Khớp tên danh mục trong ghi chú; đoán ngẫu nhiên theo số danh mục | Có |
| LLM zero-shot | Model local (Qwen hoặc tương đương qua Ollama, bản lượng tử hóa) · model API. Prompt gồm tên (+ mô tả) danh mục; nhiệt độ 0 | Có |
| Embedding zero-shot | Độ tương đồng giữa embedding ghi chú và embedding tên (+ mô tả) danh mục (bge-m3 / multilingual-e5) | Có |
| Học trên dữ liệu tổng hợp theo người dùng | TF-IDF (n-gram từ + ký tự) + LR · embedding + LR, huấn luyện trên ví dụ sinh cho danh mục của người dùng | Có (mô hình nhẹ, huấn luyện trong vài giây) |
| *Kịch bản phụ* | Các mô hình trên + fine-tune PhoBERT trên tập tổng hợp lớn của danh mục chuẩn | Chỉ danh mục chuẩn |

- Đánh giá **không thích nghi** (chưa học từ phản hồi) trên toàn bộ luồng, trừ tập dev. Các biến thể: chỉ tên / tên + mô tả; 10 / 30 / 100 ví dụ tổng hợp mỗi danh mục.
- Báo cáo tách **ghi chú hay gặp / hiếm gặp**, và F1 từng danh mục (danh mục tên rõ nghĩa như Coffee so với tên viết tắt như AC).
- **Lưu cache câu trả lời của LLM** ra file để thí nghiệm tái lập được và không tốn phí khi chạy lại.
- Quyền riêng tư: chỉ gửi bản `*_anon.csv` lên API. Đọc chính sách lưu dữ liệu của nhà cung cấp trước khi gửi.

### TN2: Chiến lược thích nghi, phát lại theo thời gian (RQ2)

**Giao thức phát lại (prequential, kiểm tra trước, học sau):**
1. Sắp các khoản chi theo ngày (trong cùng ngày giữ thứ tự của file gốc).
2. Gặp nhãn lần đầu thì phát sự kiện "người dùng tạo danh mục": hệ thống sinh dữ liệu tổng hợp cho danh mục đó và cập nhật mô hình ban đầu.
3. Với mỗi giao dịch: hệ thống đoán nhãn bằng trạng thái hiện tại, ghi lại đúng/sai (bỏ qua tính điểm nếu thuộc tập dev), **sau đó** mới nhận nhãn thật như thể người dùng vừa xác nhận hoặc sửa.
4. Cập nhật lớp cá nhân: bộ nhớ và kNN cập nhật ngay; mô hình cá nhân huấn luyện lại theo lịch (tuần hoặc tháng).
5. Giả định **phản hồi đầy đủ** (người dùng luôn sửa khi sai). (Tùy chọn) phân tích độ nhạy khi chỉ 50% lần sai được sửa.

**Các chiến lược (đặt trên mô hình ban đầu tốt nhất của TN1):**

| Mã | Chiến lược | Ghi chú |
|---|---|---|
| A0 | Không thích nghi | Mốc so sánh |
| A1 | Bộ nhớ tra cứu: ghi chú đã chuẩn hóa → nhãn gần nhất; không có thì dùng mô hình ban đầu | Rẻ nhất; trên dữ liệu cũ đã đúng ~92% với ghi chú đã gặp |
| A2 | kNN trực tuyến trên embedding các giao dịch đã sửa, kết hợp với mô hình ban đầu theo khoảng cách hoặc độ tin cậy | Cập nhật tức thì, có lời giải thích tự nhiên |
| A3 | Huấn luyện lại định kỳ mô hình cá nhân (TF-IDF + LR) trên lịch sử phản hồi **trộn với dữ liệu tổng hợp** (tỷ lệ tổng hợp giảm dần khi có nhiều dữ liệu thật). Biến thể chống trôi: toàn bộ lịch sử · cửa sổ trượt N tháng · trọng số theo thời gian | Gần với kết quả sơ bộ 78% ở báo cáo dữ liệu |
| A4 | LLM few-shot truy xuất (RAG): lấy k giao dịch đã sửa giống nhất đưa vào prompt | Gần chuyên môn GVHD; đắt và chậm nhất |

**Độ đo:**
- **Số lần người dùng phải sửa mỗi tháng** (độ đo chính, hướng người dùng) và accuracy / Macro-F1 theo từng tháng.
- **Điểm hòa vốn:** số giao dịch phản hồi cần để chiến lược vượt A0, và để đạt ngưỡng 80%.
- **Danh mục mới:** độ chính xác trong N giao dịch đầu tiên của mỗi danh mục vừa tạo.
- Tách ghi chú **đã gặp / chưa gặp** tại thời điểm đoán.
- MCC, confusion matrix, độ trễ (ms/giao dịch), bộ nhớ, chi phí API.
- Mốc tham chiếu: Cohen's kappa (giới hạn trên của con người) và "mô hình học trên toàn bộ dữ liệu quá khứ" của thí nghiệm sơ bộ (78% khi chia theo thời gian, cùng 25 nhãn).

**Kịch bản phụ:** chạy lại A0–A3 với danh mục chuẩn, so sánh để thấy ảnh hưởng của độ chi tiết danh mục.

**So sánh thống kê:** các chiến lược cùng đoán trên một luồng nên dùng **kiểm định McNemar** theo cặp. Khoảng tin cậy bằng **bootstrap theo tháng**. Phần có yếu tố ngẫu nhiên (lấy mẫu dữ liệu tổng hợp, PhoBERT) chạy 3–5 seed.

**Chạy qua hệ thống thật:** các chiến lược được so sánh trong `ml/experiments/` cho nhanh. **Cấu hình được chọn** thì chạy lại bằng công cụ phát lại qua API của hệ thống đã triển khai, kể cả sự kiện tạo danh mục, và hai kết quả phải khớp. Việc này đồng thời là một bài kiểm thử tích hợp.

### TN3: Dự báo chi tiêu (RQ3, phụ)
- **Chuỗi:** tổng chi **thường ngày** theo tuần (bỏ các khoản `Special`, học phí luân chuyển, vay), 211 tuần.
- **Trước tiên xử lý vấn đề mật độ ghi chép giảm** (tỷ lệ ngày không có khoản chi tăng từ 7% năm 2022 lên 32% năm 2026, báo cáo dữ liệu mục 4.7). Nếu không, mô hình có thể đang dự báo *thói quen ghi chép* chứ không phải chi tiêu. Ít nhất phải nêu rõ, tốt nhất là tách được hai yếu tố.
- **Mô hình:** Naive, Seasonal Naive, trung bình lịch sử và trung bình trượt (baseline, hiện đang thắng), ETS / SARIMA, Prophet (ngày lễ Việt Nam), LightGBM (lag, rolling, lịch).
- **Đánh giá:** rolling-origin backtest, dự báo trước 1 tuần và 4 tuần. Cách đánh giá này cũng theo tinh thần "chỉ dùng quá khứ", thống nhất với TN2.
- **Độ đo:** MAE, RMSE, sMAPE (không dùng MAPE vì có tuần chi bằng 0). **Kiểm định Diebold–Mariano** giữa các cặp.
- Kết quả "không mô hình nào thắng trung bình lịch sử" vẫn là kết quả hợp lệ. Phân tích vì sao (chi tiêu thường ngày ổn định, hệ số biến thiên 0,40).

### TN4: Kiểm tra trên người dùng khác (RQ4, có điều kiện)
- Mỗi tình nguyện viên: tự đặt **danh mục của mình** (tên + mô tả ngắn), cung cấp **100–200 ghi chú chi tiêu thật có ngày** và gán nhãn theo danh mục đó. Khoảng 1–2 giờ mỗi người. Ẩn danh trước khi xử lý. Vì dùng danh mục của chính họ, tình nguyện viên không phải học bộ danh mục của người khác.
- Chạy lại TN1 và TN2 (rút gọn vì luồng ngắn) với **cấu hình đã khóa**, không tinh chỉnh thêm.
- **Ngưỡng:** đủ **3 người** trở lên thì báo cáo là RQ4. Có 1–2 người thì trình bày như nghiên cứu tình huống. Không có ai thì đưa vào hạn chế và hướng phát triển.
- **Liên hệ tình nguyện viên từ tuần 1.** Họ cần vài tuần để ghi chép nếu chưa có sẵn.

### Hạn chế cần nêu trước hội đồng
- Luồng đánh giá chính là của một người; dev và luồng đánh giá cùng một người; người làm đề tài đã xem dữ liệu khi làm EDA và tự viết mô tả danh mục.
- Giả định phản hồi đầy đủ (người dùng luôn sửa khi sai) lạc quan hơn thực tế.
- Nhãn do một người gán, có nhiễu, đã đo bằng Cohen's kappa.
- Dữ liệu tổng hợp phụ thuộc vào LLM dùng để sinh. Kết quả có thể khác nếu dùng LLM khác.
- Ghi chú tự gõ khác với nội dung sao kê / SMS ngân hàng, nên kết quả không suy rộng sang bài toán phân loại sao kê.

---

## 7. Kiểm thử và quy trình
- **Quy trình:** Scrum, sprint 1 tuần, backlog trên GitHub Projects.
- **Kiểm thử:**
  - unit test (JUnit, pytest). Module Money/FX phủ test cao: làm tròn, quy đổi chéo, ngày không có tỷ giá, phí ẩn.
  - **kiểm thử ML service:** hợp đồng API; tính xác định (cùng đầu vào + cùng phiên bản mô hình thì cho cùng đầu ra); lớp cá nhân và danh mục của người A không ảnh hưởng người B; rollback phiên bản mô hình; xử lý khi API LLM lỗi hoặc chậm (dùng mô hình dự phòng); bộ sinh dữ liệu được kiểm thử với LLM giả lập (mock).
  - integration test (Testcontainers cho PostgreSQL + pgvector, Redis). **Công cụ phát lại** chạy một đoạn luồng dữ liệu qua API như một bài kiểm thử hồi quy của chất lượng mô hình.
  - E2E (Playwright), load test (k6) cho `/categorize`.
- **CI/CD:** GitHub Actions chạy build, test (kể cả đoạn phát lại ngắn với dữ liệu tổng hợp đã lưu sẵn, không gọi API), rồi deploy.
- **Giám sát:** tỷ lệ sửa nhãn theo tuần trên từng phiên bản mô hình (cùng độ đo với TN2), chi phí gọi API.
- **Đánh giá người dùng:** 5–10 người dùng thử, thang **SUS**. Có thể gộp với tình nguyện viên của TN4.

---

## 8. Kế hoạch 14 tuần

| Tuần | Công việc | Kết quả |
|---|---|---|
| 1 | Viết tên + mô tả 25 danh mục; bảng ánh xạ về danh mục chuẩn; rà nhãn thiểu số và ngày bất thường; tách tập dev; **liên hệ tình nguyện viên**; đọc tài liệu | Đề cương, config danh mục, dữ liệu đã chia |
| 2 | Gán nhãn lại mù 300 mẫu (kappa); viết bộ sinh dữ liệu và khung phát lại; **kiểm tra nhanh trên dev**; phân tích yêu cầu, thiết kế CSDL, kiến trúc; tạo repo, Docker, CI | Kappa, dữ liệu tổng hợp, skeleton project |
| 3 | TN1: baseline, LLM zero-shot (local, API), embedding zero-shot, mô hình học trên dữ liệu tổng hợp; các biến thể chỉ tên / có mô tả, số ví dụ; kịch bản phụ | Bảng kết quả RQ1, chốt mô hình ban đầu |
| 4 | TN2: chiến lược A0–A4, biến thể chống trôi, danh mục mới, kiểm định thống kê | **Chốt cấu hình thích nghi** |
| 5 | Backend: auth, ví, giao dịch, **danh mục tự tạo**, module Money (có unit test), import CSV | API core |
| 6 | ML service: `/categories` (sinh dữ liệu + huấn luyện nền qua hàng đợi), `/categorize`, `/feedback`, lớp cá nhân (pgvector), quản lý phiên bản; dịch vụ tỷ giá, phí ẩn | Luồng tạo danh mục → phân loại → phản hồi chạy được qua API |
| 7 | Frontend core: quản lý danh mục, nhập nhanh với gợi ý danh mục, sửa nhãn, import hàng loạt | Tạo danh mục → nhập → gợi ý → sửa trên UI |
| 8 | TN3: dự báo chi tiêu, backtest, Diebold–Mariano | **Báo cáo giữa kỳ với GVHD** |
| 9 | `/forecast`; ngân sách, cảnh báo, dashboard; huấn luyện lại định kỳ; giám sát tỷ lệ sửa nhãn và chi phí API | Đủ chức năng chính |
| 10 | Chạy **phát lại qua hệ thống thật**; TN4 nếu có dữ liệu tình nguyện viên; phần mở rộng nếu còn thời gian | Kết quả cuối khớp giữa notebook và hệ thống |
| 11 | Kiểm thử unit, integration, E2E, load; sửa lỗi | Báo cáo kiểm thử |
| 12 | Deploy VPS, hoàn thiện UI, người dùng thử, SUS | Bản chạy online |
| 13 | Hoàn thiện báo cáo, biểu đồ kết quả | Bản thảo luận văn |
| 14 | Chỉnh sửa, slide, tập demo, **thời gian dự phòng** | Bản nộp cuối |

> Viết báo cáo dần từng tuần. Thứ tự cắt khi trễ (đề xuất): phần mở rộng đa tiền tệ → A4 (RAG) → PhoBERT ở kịch bản phụ → kịch bản phụ danh mục chuẩn → TN4.

---

## 9. Rủi ro và cách giảm

| Rủi ro | Mức | Cách giảm |
|---|---|---|
| **Rò rỉ khi tinh chỉnh**: nhìn kết quả trên luồng đánh giá rồi sửa prompt / mô tả danh mục | **Cao** | Chỉ tinh chỉnh trên dev; viết mô tả danh mục trước; khóa và commit config trước khi tính điểm; ghi nhật ký mọi lần chạy |
| Phạm vi phình to | Cao | Phân tầng MVP / mở rộng (4.5), thứ tự cắt ở mục 8 |
| Danh mục cá nhân khó hiểu (AC, RL, Mental, Ngu) khiến dữ liệu tổng hợp và LLM zero-shot rất yếu ở ngày đầu | Trung bình | Biến thể có mô tả; đây cũng là lý do cần lớp cá nhân. Báo cáo F1 từng danh mục để thấy rõ |
| Dữ liệu tổng hợp khác xa ghi chú thật | Trung bình | Đa dạng hóa prompt (kiểm tra trên dev). Khoảng cách này tự nó là một kết quả của RQ1 |
| Sinh dữ liệu khi tạo danh mục chậm hoặc tốn phí trong hệ thống thật | Trung bình | Chạy nền qua hàng đợi, dùng zero-shot trong lúc chờ, cache; đo chi phí thật trong TN1 |
| LLM không tất định, API đổi phiên bản | Trung bình | Nhiệt độ 0, ghi tên và phiên bản model, cache toàn bộ câu trả lời và dữ liệu sinh ra |
| Danh mục hiếm (English 4 mẫu) làm Macro-F1 nhiễu | Trung bình | Báo cáo F1 từng danh mục và số mẫu; báo cáo thêm accuracy và số lần sửa |
| Không đủ tình nguyện viên | Trung bình | Liên hệ từ tuần 1; ngưỡng 3 người; có phương án lùi (TN4) |
| Mật độ ghi chép giảm làm sai lệch dự báo | Trung bình | Phân tích trước khi dự báo (TN3), nêu rõ trong hạn chế |
| Nhãn cũ không nhất quán | Trung bình | Rà soát, đo kappa |
| Hội đồng (thiên KTPM) đánh giá thấp nếu phần hệ thống yếu | Trung bình | Kiểm thử ML service, quản lý phiên bản, phát lại qua hệ thống thật, CI/CD |
| Máy cá nhân không chạy nổi LLM local | Thấp | Bản lượng tử hóa nhỏ, hoặc chạy trên Colab / Kaggle |
| API tỷ giá ngừng hoạt động | Thấp | Lưu lịch sử vào CSDL, nguồn dự phòng, nhập tay |

---

## 10. Câu hỏi hội đồng có thể hỏi

1. **Dữ liệu huấn luyện do LLM sinh thì có khách quan không?** *(Tập đánh giá là dữ liệu thật và không dùng khi sinh dữ liệu. Prompt sinh chỉ chứa tên và mô tả danh mục. Có báo cáo tỷ lệ trùng.)*
2. **Sao không huấn luyện luôn trên dữ liệu của em cho cao?** *(Người dùng mới không có dữ liệu. Học từ dữ liệu người dùng là chiến lược A3 trong phát lại, và được đo đúng trình tự thời gian.)*
3. **Sao không dùng một bộ danh mục cố định cho đơn giản?** *(Người dùng muốn danh mục riêng; có kịch bản phụ danh mục chuẩn để so sánh.)*
4. Dữ liệu đánh giá chủ yếu của một người thì kết quả có tổng quát không? *(TN4 và phần hạn chế.)*
5. Em có tinh chỉnh trên chính tập đánh giá không? Mô tả danh mục do em viết có thiên vị không? *(Tách dev, viết mô tả trước, khóa config.)*
6. Tại sao mô hình không đạt 100%? *(Cohen's kappa; nhãn phụ thuộc ngữ cảnh.)*
7. Người dùng thật có sửa hết các lần sai không? *(Giả định phản hồi đầy đủ, phân tích độ nhạy, nêu trong hạn chế.)*
8. Ghi chú chi tiêu là dữ liệu nhạy cảm, có gửi ra LLM bên ngoài không? *(Bộ sinh dữ liệu chỉ gửi tên và mô tả danh mục. Việc dùng LLM nào để phân loại được quyết định dựa trên RQ1, có tính đến quyền riêng tư. Thí nghiệm chỉ gửi bản đã ẩn danh.)*
9. Mô hình ML được tích hợp, quản lý phiên bản và kiểm thử trong hệ thống thế nào? Số liệu trong luận văn có phải của hệ thống thật không? *(Công cụ phát lại qua API.)*
10. Chênh lệch giữa các chiến lược có ý nghĩa thống kê không?
11. Hệ thống khác gì Money Lover, MISA, các app ghi chép khác?
12. Tại sao không dùng `double` để lưu tiền? Phí đổi tiền tính thế nào?

---

## 11. Việc cần làm tiếp

**Trước buổi gặp GVHD** (xem [buoi-01-chuan-bi.md](../meeting/buoi-01-chuan-bi.md))
- [ ] In [tom-tat-de-tai.pdf](tom-tat-de-tai.pdf) hoặc chuẩn bị 5–6 slide theo hướng mới
- [ ] Hỏi khoa mẫu đề cương / báo cáo của CT553H

**Dữ liệu**
- [x] Xác nhận các cột và nguồn dữ liệu: ghi chép tay trên Notion, xem báo cáo dữ liệu
- [x] EDA cơ bản, thử nghiệm sơ bộ phân loại và dự báo
- [ ] Viết tên + mô tả 25 danh mục; bảng ánh xạ về danh mục chuẩn (sau khi có ý kiến GVHD)
- [ ] Rà soát nhãn thiểu số và ngày bất thường
- [ ] Tách tập dev ngẫu nhiên ~10%; gán nhãn lại mù 300 mẫu, tính kappa
- [ ] Phân tích mật độ ghi chép giảm (ảnh hưởng tới TN3)
- [ ] **Liên hệ 3–5 tình nguyện viên ngay**

**Thí nghiệm**
- [ ] Chọn API LLM để sinh dữ liệu, đọc chính sách dữ liệu và ước tính chi phí
- [ ] Kiểm tra máy cá nhân có chạy được LLM local (Ollama) không; kiểm tra hạn mức GPU Colab / Kaggle
- [ ] Kiểm tra pgvector phù hợp cho bộ nhớ kNN theo người dùng

**Tài liệu cần tìm**
- [ ] LLM zero-shot cho phân loại văn bản ngắn; phân loại chỉ dựa vào tên nhãn (label-name-only); huấn luyện trên dữ liệu do LLM sinh
- [ ] Học trực tuyến / học liên tục, concept drift, đánh giá prequential
- [ ] Cá nhân hóa và cold-start trong phân loại
- [ ] Phân loại giao dịch (Txn-Bert, arXiv 2508.05425, TopoLedgerBERT); PhoBERT
- [ ] Cohen's kappa, McNemar, Diebold–Mariano
- [ ] (Phụ) VAS 10 / IAS 21, World Bank *Remittance Prices Worldwide*, Quy định EU 2019/518

**Khác**
- [ ] Tự dùng thử Toshl, PocketSmith, Firefly III, Money Lover để chụp màn hình cho chương 2; xem các app gợi ý danh mục tự tạo thế nào
- [x] ~~Ghi chép giao dịch ngoại tệ của bản thân~~ (đã bỏ, 27/09/2026)
