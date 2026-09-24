# Brainstorm đề tài luận văn CT553H

> Cập nhật: 24/09/2026 · Trạng thái: **đã chọn hướng đề tài #1, đang hoàn thiện đề cương**

---

## 0. Tóm tắt quyết định

- **Đề tài chọn:** Hệ thống quản lý tài chính cá nhân thông minh, **đa tiền tệ**, ứng dụng học máy để phân loại giao dịch và dự báo chi tiêu.
- **Lý do chính:** có sẵn **hơn 5.000 giao dịch thật từ 2022 đến nay**, khả thi trong 3.5 tháng, dễ ghi điểm khi bảo vệ, hợp sở thích (tài chính cá nhân, khởi nghiệp, tự động hóa).
- **Trọng tâm: học máy.** Đa tiền tệ là **điểm cộng của hệ thống**, không gánh phần hàm lượng khoa học.
- **Đóng góp chính (hàm lượng khoa học):** so sánh phương pháp phân loại giao dịch tiếng Việt **trên người bán chưa gặp** (có loại trùng lặp để tránh rò rỉ dữ liệu), đo mức nhất quán của chính nhãn người dùng, đo ảnh hưởng của dữ liệu thay đổi theo thời gian, khảo sát bài toán người dùng mới (cold-start), so sánh mô hình dự báo chi tiêu (kèm phân tích phụ về ảnh hưởng của biến động tỷ giá).
- **Hội đồng thiên về kỹ thuật phần mềm:** ML là trọng tâm khoa học, nhưng phần hệ thống và quy trình (kiến trúc, kiểm thử, CI/CD, tích hợp mô hình vào hệ thống) phải chắc chắn, vì đó là phần hội đồng chấm kỹ nhất.
- **Điểm khác biệt của hệ thống:** không phải "hỗ trợ đa tiền tệ", vì nhiều ứng dụng đã có (xem mục 5.7). Điểm khác biệt là **phân tích chi phí và rủi ro đa tiền tệ**:
  1. tự phát hiện **phí đổi tiền ẩn** (định nghĩa theo tỷ giá mid-market, xem 5.3-5),
  2. **tách biến động tài sản** thành phần do chi tiêu và phần do tỷ giá,
  3. **dự báo nhu cầu theo từng loại tiền** và gợi ý lượng cần đổi theo dự báo phân vị (xem 5.3-11).

---

## 1. Bối cảnh

| Mục | Nội dung |
|---|---|
| Ngành | Kỹ thuật phần mềm |
| Yêu cầu học phần | Hệ thống phần mềm có hàm lượng khoa học tương đối |
| Thời gian | 3.5 tháng (~14 tuần), làm một mình |
| Kỹ năng | Java, C, C++, React, Redis, MongoDB, PostgreSQL, Web, AI/ML |
| Sở thích | Thương mại điện tử, khởi nghiệp, hệ thống hoàn chỉnh, quy trình phát triển phần mềm, phần mềm quản lý thông minh, tự động hóa đời sống, tài chính cá nhân, chứng khoán |
| Định hướng | Xây dựng hệ thống kèm hàm lượng nghiên cứu |
| GVHD | Chuyên ngành tin sinh học, chấp nhận đề tài lĩnh vực khác |
| Hội đồng | Thường thiên về kỹ thuật phần mềm |
| Tài nguyên tính toán | Không có lab. Dùng máy cá nhân + Google Colab / Kaggle |
| Dữ liệu tình nguyện viên | Không cần mẫu cam kết (vẫn ẩn danh hóa trước khi xử lý) |

---

## 2. Các ý tưởng đã xem xét

| # | Đề tài | Phần nghiên cứu | Ghi chú |
|---|---|---|---|
| 1 | **Tài chính cá nhân: phân loại giao dịch + dự báo chi tiêu** | So sánh TF-IDF, PhoBERT, LLM; dự báo chuỗi thời gian | **Đã chọn** |
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
| Khả thi 3.5 tháng | ★★★★★ | ★★★ | ★★★ |
| Dữ liệu | ★★★★★ (có sẵn dữ liệu thật) | ★★★★ | ★★★★ |
| Rủi ro chính | Dữ liệu một người | Kết quả dễ bị bác bỏ, backtest dễ sai | Mô hình khó thắng baseline |
| Khả năng ghi điểm | ★★★★★ | ★★★ | ★★★★ |

**Lấy điểm mạnh của #7:** báo cáo thể hiện rõ quy trình phát triển phần mềm (Scrum, CI/CD, kiểm thử tự động).

---

## 3. Liên hệ với chuyên môn của GVHD

Theo danh sách công bố trong `draft.md`, GVHD mạnh về **BERT/transformer, CNN, word embedding, SHAP, RAG**, và thường trình bày nghiên cứu theo **quy tắc 5 bước của Chou**. Có thể trình bày phần nghiên cứu theo đúng khung này để GVHD dễ hướng dẫn:

| Bước (Chou's 5-step rule) | Áp dụng vào đề tài |
|---|---|
| 1. Xây dựng bộ dữ liệu chuẩn (benchmark) | Làm sạch, ẩn danh hóa hơn 5.000 giao dịch. **Loại trùng lặp giữa train/test theo nhóm người bán** (tương tự dùng CD-HIT loại chuỗi quá giống nhau). **Gán nhãn lại mù một mẫu, đo Cohen's kappa** |
| 2. Biểu diễn mẫu | TF-IDF (từ và n-gram ký tự), word embedding (fastText), embedding đa ngôn ngữ (bge-m3, multilingual-e5), embedding PhoBERT, đặc trưng số tiền/thời gian/tiền tệ |
| 3. Thuật toán | Logistic Regression, SVM, fine-tune PhoBERT, (tùy chọn) PhoBERT + CNN head, LLM few-shot |
| 4. Kiểm định chéo | GroupKFold theo người bán; **tập kiểm tra độc lập** = dữ liệu 2025–2026 (chia theo thời gian); nhiều seed; learning curve |
| 5. Web server | Chính là hệ thống quản lý tài chính hoàn chỉnh đã triển khai |

Thêm **SHAP** để giải thích vì sao mô hình phân loại một giao dịch vào một danh mục. Tính năng này vừa hữu ích cho người dùng, vừa quen thuộc với GVHD. Báo cáo thêm **MCC**, độ đo GVHD hay dùng trong các bài báo.

---

## 4. Đề cương chi tiết

### 4.1 Tên đề tài

**Tiếng Việt:** Xây dựng hệ thống quản lý tài chính cá nhân đa tiền tệ ứng dụng học máy trong phân loại giao dịch và dự báo chi tiêu

**Tiếng Anh:** Building a Multi-Currency Personal Finance Management System Using Machine Learning for Transaction Categorization and Spending Forecasting

### 4.2 Lý do chọn đề tài và đối tượng người dùng

- Ghi chép chi tiêu thủ công tốn thời gian, người dùng hay bỏ cuộc.
- Các ứng dụng phổ biến phân loại dựa trên quy tắc, chưa hiểu tốt nội dung giao dịch tiếng Việt.
- Ngày càng nhiều người Việt có **thu nhập và chi tiêu bằng nhiều loại tiền**:
  - du học sinh (nhận tiền nhà bằng VND, làm thêm, trả học phí bằng ngoại tệ),
  - người lao động ở nước ngoài gửi tiền về,
  - freelancer/remote nhận lương USD, EUR,
  - người thường xuyên đi lại giữa hai nước (digital nomad, công tác).
- Nhóm này thường gặp các vấn đề: không biết tổng tài sản thật, không biết tiêu bao nhiêu ở mỗi nước, **mất tiền vì phí đổi tiền "ẩn"**, không phân biệt được tài sản giảm vì tiêu hay vì tỷ giá.

### 4.3 Mục tiêu

**Tổng quát:** xây dựng hệ thống web hoàn chỉnh quản lý tài chính cá nhân đa tiền tệ, tự động hóa khâu phân loại giao dịch và hỗ trợ ra quyết định bằng dự báo.

**Cụ thể:**
1. So sánh các phương pháp phân loại giao dịch tiếng Việt, từ cổ điển đến transformer và LLM.
2. Khảo sát số mẫu gán nhãn tối thiểu cho người dùng mới, và hiệu quả của huấn luyện lại định kỳ khi dữ liệu thay đổi theo thời gian.
3. So sánh các mô hình dự báo chi tiêu, đánh giá ảnh hưởng của biến động tỷ giá lên dự báo.
4. Thiết kế mô hình dữ liệu và nghiệp vụ **đa tiền tệ đúng chuẩn**, dựa trên nguyên tắc của chuẩn mực kế toán VAS 10 / IAS 21.
5. Xây dựng, kiểm thử, triển khai hệ thống theo quy trình Scrum và CI/CD.

### 4.4 Câu hỏi nghiên cứu

| RQ | Câu hỏi | Bắt buộc? |
|---|---|---|
| RQ1 | Phương pháp nào phân loại giao dịch tiếng Việt tốt nhất khi cân bằng độ chính xác, tốc độ và chi phí? | Có |
| RQ2 | Dữ liệu thay đổi theo thời gian làm độ chính xác giảm bao nhiêu? Huấn luyện lại định kỳ cải thiện bao nhiêu? Người dùng mới cần gán nhãn bao nhiêu giao dịch? | Có |
| RQ3a | Mô hình nào dự báo chi tiêu tốt nhất? | Có |
| RQ3b | Với người dùng có tiền tệ báo cáo khác tiền tệ chi tiêu, nên dự báo theo tiền gốc rồi quy đổi, hay dự báo trực tiếp trên chuỗi đã quy đổi? Mức ảnh hưởng thay đổi thế nào theo độ biến động của tỷ giá? | Có (phân tích phụ) |
| RQ4 | Mô hình đa ngôn ngữ có phân loại tốt giao dịch có nội dung tiếng nước ngoài không? | Chỉ khi có dữ liệu (xem 5.6) |

### 4.5 Phạm vi

| MVP (bắt buộc) | Mở rộng (nếu kịp) | Ngoài phạm vi |
|---|---|---|
| Web responsive, nhiều người dùng | Kế hoạch đổi tiền, cảnh báo thiếu hụt ngoại tệ | App mobile native |
| Ví theo từng loại tiền, tiền tệ báo cáo | Lãi/lỗ tỷ giá đã thực hiện | Kết nối API ngân hàng |
| Tỷ giá lịch sử tự động cập nhật | So sánh chi tiêu giữa các nước theo PPP | **Dự đoán tỷ giá**, tư vấn đầu tư |
| Đổi tiền/chuyển khoản giữa ví, ghi nhận phí đổi tiền | Phân loại đa ngôn ngữ (RQ4) | Thuế thu nhập nhiều quốc gia |
| Phân loại tự động + vòng lặp phản hồi | Phát hiện giao dịch bất thường | Thanh toán, chuyển tiền thật |
| Ngân sách, cảnh báo, dashboard, dự báo | OCR hóa đơn (đề tài #4) | |
| Phân rã biến động tài sản (do tiêu hay do tỷ giá) | | |

### 4.6 Chức năng chính

**Người dùng:**
- Đăng ký, đăng nhập (JWT), chọn **tiền tệ báo cáo** và múi giờ mặc định.
- Quản lý ví: mỗi ví có một loại tiền (ví tiền mặt VND, tài khoản ngân hàng JPY, thẻ Visa VND, ví Wise USD…).
- CRUD giao dịch, import CSV/Excel, dán nội dung thông báo ngân hàng.
- **Tự động phân loại** kèm độ tin cậy và giải thích (SHAP). Người dùng sửa nhãn thì hệ thống ghi nhận để huấn luyện lại.
- **Đổi tiền / chuyển giữa ví**: nhập số tiền hai bên, hệ thống tự tính tỷ giá thực tế và phí so với tỷ giá thị trường.
- Ngân sách theo danh mục, theo tiền tệ hoặc theo quốc gia; cảnh báo khi sắp vượt.
- Dashboard: tổng tài sản quy đổi, cơ cấu theo tiền tệ, chi tiêu theo quốc gia, **phân rã biến động tài sản**.
- Dự báo chi tiêu tuần/tháng tới.
- Xuất báo cáo PDF/Excel.

**Quản trị viên:** quản lý danh mục chuẩn, danh sách tiền tệ, nguồn tỷ giá; theo dõi chỉ số mô hình; kích hoạt huấn luyện lại.

### 4.7 Kiến trúc

```
┌─────────────┐      ┌──────────────────────────┐      ┌─────────────────────┐
│  React SPA  │─────▶│   Spring Boot (Java)     │─────▶│  ML Service         │
│  (Vite, TS) │ REST │  - Auth, Wallet, Txn     │ REST │  (Python FastAPI)   │
└─────────────┘      │  - Money/FX module       │      │  - /categorize      │
                     │  - Budget, Alert         │      │  - /forecast        │
                     │  - Scheduler (tỷ giá)    │      │  - /retrain         │
                     └───┬──────────┬─────┬─────┘      └─────────┬───────────┘
                         │          │     │                      │
                  ┌──────▼───┐ ┌────▼───┐ │ fetch hằng ngày ┌────▼───────────┐
                  │PostgreSQL│ │ Redis  │ └───────────────▶ │ Nguồn tỷ giá   │
                  │          │ │ cache, │                   │ (API ngoài)    │
                  └──────────┘ │ queue  │                   └────────────────┘
                               └────────┘
        Docker Compose · GitHub Actions CI/CD · Triển khai VPS
```

- **PostgreSQL:** dữ liệu tài chính cần tính toàn vẹn (ACID), kiểu `NUMERIC` chính xác.
- **Redis:** cache tỷ giá của ngày và dashboard, hàng đợi tác vụ huấn luyện lại.
- **Module Money/FX** tách riêng trong backend, có unit test kỹ vì đây là nơi dễ sai nhất.
- Không dùng MongoDB, vì không có lý do rõ ràng để dùng.

---

## 5. Bài toán đa tiền tệ

### 5.1 Tình huống minh họa (persona)

> **Minh, du học sinh ở Nhật.**
> - Mỗi tháng gia đình chuyển 15 triệu VND vào tài khoản Vietcombank.
> - Làm thêm ở Nhật, nhận lương bằng JPY vào tài khoản ngân hàng Nhật.
> - Học phí, tiền nhà trả bằng JPY. Thỉnh thoảng quẹt thẻ Visa VND ở Nhật.
> - Mỗi hè về Việt Nam 2 tháng, tiêu bằng VND.
> - Đổi tiền qua ngân hàng hoặc dịch vụ chuyển tiền.
>
> **Minh muốn biết:** tổng tài sản hiện tại? Mỗi tháng tiêu bao nhiêu ở Nhật, bao nhiêu ở Việt Nam? Mất bao nhiêu tiền cho phí đổi tiền? Tháng sau cần bao nhiêu JPY, có cần đổi thêm không?

### 5.2 Các vấn đề cần giải quyết

| # | Vấn đề | Nếu làm sai |
|---|---|---|
| 1 | Lưu số tiền của nhiều loại tiền | Sai số làm tròn (dùng `float`), sai số chữ số thập phân (JPY 0, USD 2, KWD 3) |
| 2 | Quy đổi để báo cáo | Tổng hợp vô nghĩa khi cộng thẳng VND với JPY |
| 3 | Chọn tỷ giá nào, ngày nào | Báo cáo tháng cũ thay đổi mỗi ngày vì dùng tỷ giá hiện tại |
| 4 | Đổi tiền / chuyển giữa ví | Bị tính thành chi tiêu và thu nhập ảo, thống kê sai gấp đôi |
| 5 | Phí đổi tiền ẩn trong tỷ giá | Người dùng không biết mình mất tiền |
| 6 | Quẹt thẻ ở nước ngoài | Hai số tiền (tiền gốc và tiền bị trừ) + phí giao dịch nước ngoài |
| 7 | Tài sản thay đổi do tỷ giá | Tưởng mình tiết kiệm được hoặc bị lỗ, thực ra là do tỷ giá |
| 8 | Ngân sách khi chi bằng nhiều loại tiền | Không biết đã tiêu bao nhiêu so với hạn mức |
| 9 | So sánh chi tiêu giữa các nước | 1 triệu VND ở Việt Nam và 1 triệu VND quy đổi ra ở Nhật có sức mua rất khác nhau |
| 10 | Múi giờ | Giao dịch lúc 23h ở Nhật bị tính sang ngày khác, sai thống kê ngày |
| 11 | Thiếu tiền ở một loại tiền | Tổng tài sản đủ nhưng không có JPY để trả tiền nhà |

### 5.3 Giải pháp

#### (1) Lưu trữ tiền
- **Luôn lưu số tiền gốc và loại tiền gốc** (mã ISO 4217: VND, JPY, USD…). Không bao giờ chỉ lưu số đã quy đổi.
- Kiểu dữ liệu: PostgreSQL `NUMERIC(19,4)` hoặc `BIGINT` theo đơn vị nhỏ nhất. Java dùng `BigDecimal` hoặc **Java Money API (JSR 354, thư viện Moneta)**. **Tuyệt đối không dùng `double`/`float`.**
- Bảng `currencies` lưu số chữ số thập phân (`minor_unit`) của từng loại tiền. Frontend hiển thị bằng `Intl.NumberFormat`.

#### (2) Ví theo tiền tệ và tiền tệ báo cáo
- Mỗi ví có **một** loại tiền cố định. Ví đa tiền tệ (Wise, Revolut) được mô hình hóa thành nhiều ví con.
- Mỗi người dùng chọn một **tiền tệ báo cáo** (base currency), có thể đổi bất cứ lúc nào. Mọi thống kê tổng hợp đều quy về tiền tệ này.

#### (3) Tỷ giá: nguồn, loại, quy tắc tra cứu
- **Bảng `exchange_rates` lưu lịch sử** tỷ giá theo ngày: `(rate_date, base, quote, rate, rate_type, source)`.
- Job chạy hằng ngày lấy tỷ giá và cache vào Redis. Nếu nguồn chính lỗi thì chuyển sang nguồn dự phòng.
- **Nguồn tham khảo** (cần kiểm tra lại tình trạng và điều khoản):
  - Tỷ giá công bố của Vietcombank (có giá mua tiền mặt, mua chuyển khoản, bán),
  - tỷ giá trung tâm của Ngân hàng Nhà nước,
  - các API tỷ giá miễn phí (ví dụ open.er-api.com, exchangerate-api). **Lưu ý:** API dựa trên tỷ giá ECB như Frankfurter không có VND.
- **Quy tắc quy đổi** (theo tinh thần VAS 10 / IAS 21):
  - Giao dịch thu/chi quy đổi theo **tỷ giá ngày giao dịch**. Lưu lại tỷ giá đã dùng (`fx_rate_to_base`) để báo cáo cũ không thay đổi.
  - **Số dư, tổng tài sản** quy đổi theo **tỷ giá tại thời điểm xem**.
  - Ngày không có tỷ giá (cuối tuần, lễ) thì dùng tỷ giá gần nhất trước đó.
  - Quy đổi chéo (JPY → VND khi nguồn chỉ có USD) đi qua đồng trung gian: `JPY→VND = (USD→VND) / (USD→JPY)`.
- Khi người dùng đổi tiền tệ báo cáo, hệ thống tính lại `amount_base` từ bảng tỷ giá lịch sử (chạy nền).

#### (4) Đổi tiền và chuyển giữa ví
- Tách riêng loại giao dịch: `INCOME`, `EXPENSE`, `TRANSFER` (cùng tiền), `EXCHANGE` (khác tiền).
- `TRANSFER` và `EXCHANGE` **không tính là thu nhập hay chi tiêu**. Hai vế được liên kết bằng `transfer_group_id`.
- **Mô hình ML cần nhận diện giao dịch chuyển khoản nội bộ** để tự gợi ý ghép cặp. Đây là một nhãn quan trọng trong bài toán phân loại.

#### (5) Phí đổi tiền ẩn
Khi đổi tiền, người dùng nhập số tiền **hai bên**. Hệ thống tính:

```
tỷ_giá_thực_tế  = số_tiền_nhận / số_tiền_gửi
giá_trị_thị_trường = số_tiền_gửi × tỷ_giá_trung_bình_thị_trường(ngày đó)
phí_ẩn          = giá_trị_thị_trường − số_tiền_nhận
tỷ_lệ_phí       = phí_ẩn / giá_trị_thị_trường
```

*Ví dụ (số liệu giả định):* đổi 10.000.000 VND lấy 380 USD. Nếu tỷ giá thị trường hôm đó là 1 USD = 25.400 VND, thì 10 triệu VND tương đương 393,7 USD. Phí ẩn là 13,7 USD (~3,5%).

**Chọn tỷ giá nào làm chuẩn:**
- **Chuẩn chính: tỷ giá mid-market** (trung bình mua–bán liên ngân hàng). Căn cứ: World Bank *Remittance Prices Worldwide* đo biên lợi nhuận tỷ giá so với tỷ giá liên ngân hàng; Quy định EU 2019/518 yêu cầu công bố phí quy đổi dưới dạng % chênh lệch so với tỷ giá tham chiếu của ECB. *(Cần kiểm tra văn bản gốc trước khi trích dẫn.)*
- **Chuẩn phụ để hiển thị:** so với tỷ giá bán của Vietcombank hoặc tỷ giá trung tâm của Ngân hàng Nhà nước, để trả lời câu hỏi "đổi ở kênh này có rẻ hơn đổi ở ngân hàng không?".
- **Ngưỡng sai số:** hệ thống chỉ có tỷ giá theo ngày, trong khi tỷ giá biến động trong ngày. Chênh lệch nhỏ (khoảng dưới 0,3–0,5%, cần hiệu chỉnh) hiển thị là "không đáng kể". Nêu điểm này trong phần hạn chế.
- **Kiểm chứng:** đối chiếu với biên lai thật (mục 5.8) và với phí Wise công bố so với mid-market.

Phí ẩn được ghi thành một khoản chi thuộc danh mục **"Phí đổi tiền"**. Dashboard thống kê tổng phí đổi tiền theo tháng, theo kênh đổi, giúp người dùng chọn kênh rẻ hơn. Đây là tính năng có giá trị thực tế cao, dễ gây ấn tượng khi demo.

#### (6) Quẹt thẻ ở nước ngoài
- Lưu cả `original_amount` + `original_currency` (ví dụ 3.000 JPY) **và** số tiền thực bị trừ trên thẻ (ví dụ 540.000 VND).
- Chênh lệch so với tỷ giá thị trường là phí giao dịch nước ngoài, ghi nhận như (5).
- Thống kê "chi ở Nhật" dùng số tiền gốc JPY, thống kê "ví thẻ VND" dùng số tiền bị trừ.

#### (7) Phân rã biến động tài sản: do tiêu hay do tỷ giá
Gọi `B(c,t)` là số dư loại tiền `c` tại thời điểm `t`, `r(c,t)` là tỷ giá quy về tiền tệ báo cáo. Tổng tài sản `W(t) = Σ_c B(c,t) · r(c,t)`. Biến động giữa hai kỳ được tách **chính xác** thành hai phần:

```
W(t) − W(t−1) =  Σ_c [B(c,t) − B(c,t−1)] · r(c,t−1)     ← hiệu ứng dòng tiền (thu nhập, chi tiêu)
               + Σ_c  B(c,t) · [r(c,t) − r(c,t−1)]       ← hiệu ứng tỷ giá
```

*Ví dụ:* giữ 1.000 USD, không tiêu gì, tỷ giá tăng từ 25.000 lên 26.000. Tài sản quy ra VND tăng 1.000.000, **toàn bộ là hiệu ứng tỷ giá**, không phải tiết kiệm.

Dashboard hiển thị biểu đồ waterfall: tài sản đầu kỳ → + thu nhập → − chi tiêu → ± tỷ giá → tài sản cuối kỳ.

#### (8) Ngân sách đa tiền tệ
- Mỗi ngân sách có **loại tiền riêng** và có thể gắn **phạm vi quốc gia** (ví dụ: "Ăn uống ở Nhật: 40.000 JPY/tháng", "Ăn uống ở Việt Nam: 3 triệu VND/tháng").
- Khoản chi bằng loại tiền khác được quy đổi sang tiền của ngân sách theo tỷ giá ngày giao dịch.
- Hệ thống tự nhận biết **bối cảnh quốc gia** hiện tại từ loại tiền và ví của các giao dịch gần nhất, rồi gợi ý ngân sách phù hợp.

#### (9) So sánh chi tiêu giữa các nước (mở rộng)
- Quy đổi theo tỷ giá thị trường **không phản ánh sức mua**. Có thể thêm chế độ xem theo **PPP** (hệ số ngang giá sức mua của World Bank).
- Ví dụ câu hỏi trả lời được: "Chi phí sinh hoạt thực tế của tôi ở Nhật cao gấp mấy lần ở Việt Nam?"

#### (10) Múi giờ
- Lưu thời điểm giao dịch bằng `timestamptz` (UTC) **kèm múi giờ địa phương** lúc giao dịch.
- Thống kê theo ngày dùng **ngày địa phương**, tỷ giá tra theo ngày địa phương.

#### (11) Kế hoạch thanh khoản ngoại tệ (mở rộng, dùng kết quả dự báo)
Kết hợp 3 tầng:

| Tầng | Nội dung |
|---|---|
| **Tính năng** | Dùng lại mô hình dự báo thắng ở TN2 cho chuỗi chi tiêu của từng loại tiền, so với số dư hiện có của loại tiền đó |
| **Phương pháp** | Gợi ý theo **dự báo phân vị** thay vì một con số: `cần_đổi = max(0, dự_báo_P80 − số_dư_hiện_có)`. Đổi dư một chút tốt hơn thiếu tiền trả tiền nhà |
| **Đánh giá** | Trên dữ liệu bán mô phỏng, đặt trong **chương đánh giá hệ thống** (mục "Đánh giá tính năng gợi ý đổi tiền"), **không phải RQ** để giữ ML làm trọng tâm |

- Cảnh báo sớm: "Tháng sau dự kiến chi 120.000 JPY (P80: 135.000), số dư JPY hiện có 80.000. Nên đổi thêm khoảng 55.000 JPY."
- **Chỉ gợi ý số lượng cần đổi, không dự đoán thời điểm đổi tốt nhất.** Dự đoán tỷ giá thuộc loại bài toán như dự đoán giá cổ phiếu, kết quả khó thuyết phục hội đồng.

**Cách đánh giá (bán mô phỏng):**
- Lấy chuỗi chi tiêu VND thật, chọn các giai đoạn giả định "đang ở nước ngoài" (ví dụ: 10 tháng ở Nhật, 2 tháng hè về Việt Nam), quy đổi phần chi ở nước ngoài sang JPY theo tỷ giá lịch sử thật. Kết quả là các chuỗi chi tiêu **ngắt quãng** theo từng loại tiền, giống thực tế người đi lại giữa hai nước.
- Mô phỏng theo thời gian: mỗi tháng, hệ thống gợi ý lượng cần đổi, rồi so với chi tiêu thực tế tháng đó.
- **Độ đo:** tỷ lệ tháng bị thiếu tiền, số tiền đổi dư trung bình. Chạy với P50 / P80 / P90 để vẽ **đường đánh đổi** giữa thiếu tiền và đổi dư.
- (Tùy chọn) Thử thêm phương pháp **Croston** cho chuỗi ngắt quãng (intermittent demand).
- **Nghiên cứu tình huống:** chạy trên dữ liệu ngoại tệ tự ghi chép (mục 5.8), dù ngắn.
- **Hạn chế cần nêu rõ:** đây là *kiểm chứng cơ chế gợi ý trên dữ liệu bán mô phỏng*, không phải hành vi chi tiêu thật ở nước ngoài (cơ cấu chi tiêu và giá cả khác nhau). Phần quy đổi tỷ giá trùng một phần với RQ3b; phần mới là chuỗi ngắt quãng và đánh giá quyết định đổi tiền.

### 5.4 Thiết kế CSDL (phần liên quan đa tiền tệ)

```sql
currencies      (code CHAR(3) PK, name, symbol, minor_unit SMALLINT)
users           (id, email, base_currency → currencies, default_timezone)
wallets         (id, user_id, name, type, currency → currencies, archived)
exchange_rates  (rate_date, base, quote, rate NUMERIC(20,10), rate_type, source,
                 PK(rate_date, base, quote, rate_type, source))
transactions    (id, user_id, wallet_id,
                 type            -- INCOME | EXPENSE | TRANSFER | EXCHANGE
                 amount NUMERIC(19,4), currency,          -- số tiền theo tiền của ví
                 original_amount, original_currency,      -- tiền gốc (quẹt thẻ nước ngoài)
                 fx_rate_to_base NUMERIC(20,10), amount_base NUMERIC(19,4),
                 occurred_at TIMESTAMPTZ, local_tz, country_code,
                 description, category_id,
                 category_source -- USER | MODEL
                 model_confidence, model_version,
                 transfer_group_id)
budgets         (id, user_id, category_id, currency, amount, period, country_code NULL)
category_feedback (id, transaction_id, predicted_category, corrected_category, created_at)
```

### 5.5 Những điều không làm, và lý do
- **Dự đoán tỷ giá / thời điểm đổi tiền tối ưu:** không đủ cơ sở khoa học trong phạm vi luận văn, dễ bị chất vấn.
- **Thuế thu nhập nhiều quốc gia:** quy định phức tạp, ngoài chuyên môn.
- **Kết nối trực tiếp ngân hàng nước ngoài:** mỗi nước một chuẩn, không khả thi trong 14 tuần.

### 5.6 Nếu dữ liệu hiện có chỉ có VND
Phần đa tiền tệ vẫn làm được:
- **Nghiệp vụ và hệ thống** (mục 5.3) không cần dữ liệu huấn luyện, chỉ cần tỷ giá lịch sử (công khai).
- **RQ3b (dự báo có tỷ giá)** vẫn làm được: lấy chuỗi chi tiêu VND thật, kết hợp tỷ giá lịch sử VND/USD thật, mô phỏng người dùng có tiền tệ báo cáo là USD.
- **RQ4 (đa ngôn ngữ)** chỉ làm nếu thu thập được dữ liệu thật từ tình nguyện viên ở nước ngoài (vài trăm giao dịch). Nếu không có thì đưa vào hướng phát triển. **Không nên dựa hoàn toàn vào dữ liệu do LLM sinh ra**, vì hội đồng sẽ nghi ngờ tính khách quan.

### 5.7 Khảo sát hiện trạng: đã có ai làm chưa? (tìm ngày 24/09/2026)

**Kết luận ngắn:** hỗ trợ đa tiền tệ **cơ bản đã phổ biến**. Các tính năng **phân tích** đa tiền tệ thì **chưa thấy** hoặc chỉ có một phần trong các ứng dụng được khảo sát. Về học thuật, chưa tìm thấy công trình nào về quản lý tài chính cá nhân đa tiền tệ, và chưa thấy công trình phân loại giao dịch **tiếng Việt**.

| Tính năng | Hiện trạng | Ví dụ |
|---|---|---|
| Ví theo loại tiền, tiền tệ báo cáo, tỷ giá tự động | **Đã phổ biến** | Toshl, PocketSmith, Firefly III, Lunch Money, Spendee, Wallet (BudgetBakers), MoneyWiz, Money Lover |
| Tỷ giá lịch sử theo ngày giao dịch, nhập tỷ giá tùy chỉnh | **Đã có** | Toshl (dữ liệu từ 1999, cho nhập tỷ giá thực trả), Firefly III (trường foreign amount), Lunch Money |
| Ngân sách theo loại tiền | **Đã có** | PocketSmith (ngân sách theo tiền tệ của tài khoản), Toshl |
| Dự báo dòng tiền đa tiền tệ | **Có, dạng lập lịch/quy tắc** | PocketSmith (dự báo số dư theo giao dịch định kỳ, không dùng ML) |
| Thấy ảnh hưởng của tỷ giá | **Có một phần** | PocketSmith (xem thay đổi số dư do tỷ giá theo từng tài khoản), Wealthfolio (lãi/lỗ tỷ giá chưa thực hiện, cho **đầu tư**), Borderless Budget (quảng cáo "xem tỷ giá ảnh hưởng thế nào", không công bố phương pháp) |
| **Phân rã biến động tổng tài sản: dòng tiền và tỷ giá** (công thức 5.3-7) | **Chưa thấy** công bố rõ cho chi tiêu cá nhân | |
| **Tự tính phí đổi tiền ẩn** cho từng giao dịch, thống kê theo kênh | **Chưa thấy** trong app quản lý chi tiêu. Chỉ có công cụ **so sánh** nhà cung cấp chuyển tiền (Wise, Remitto) | |
| **Dự báo nhu cầu từng loại tiền bằng ML** + gợi ý lượng cần đổi | **Chưa thấy** | |
| Phân loại giao dịch bằng ML | **Nghiên cứu nhiều với tiếng Anh** (Txn-Bert của QuickBooks 2025, phân loại giao dịch SME 2025, TopoLedgerBERT 2024). **Chưa thấy công trình tiếng Việt** | |

**Lưu ý khi viết vào luận văn:**
- Khảo sát dựa trên tài liệu công khai và bài review. Ứng dụng thương mại có thể có tính năng không công bố.
- Bài so sánh của Borderless Budget nói "không app nào có" các tính năng phân tích, nhưng đây là **bài của đối thủ cạnh tranh**, cần xem là nguồn thiên vị.
- Nên viết: *"chưa tìm thấy trong các ứng dụng và công trình được khảo sát"*, **không** viết *"chưa ai làm"*.
- Chương 2 của luận văn nên có một **bảng so sánh tính năng** giữa hệ thống của mình và Toshl, PocketSmith, Firefly III, Money Lover. Hội đồng gần như chắc chắn sẽ hỏi "khác gì app X".

**Định vị tính năng key:** *"Từ ghi chép đa tiền tệ đến phân tích đa tiền tệ"*. Các app hiện có trả lời câu hỏi "tôi có bao nhiêu tiền", hệ thống này trả lời thêm "tôi **mất bao nhiêu** vì đổi tiền", "tài sản thay đổi **vì đâu**", "tháng sau **cần bao nhiêu** tiền nào".

**Nguồn:**
- [Toshl: currencies](https://toshl.com/currencies/)
- [Firefly III: exchange rates](https://docs.firefly-iii.org/explanation/financial-concepts/exchange-rates/)
- [PocketSmith: multi-currency](https://www.pocketsmith.com/tour/multi-currency/), [PocketSmith: cash flow forecasts](https://www.pocketsmith.com/tour/cash-flow-forecasts/)
- [Lunch Money: multicurrency](https://lunchmoney.app/features/multicurrency/)
- [Borderless Budget: best multi-currency budgeting apps](https://borderlessbudget.com/blog/best-multi-currency-budgeting-apps)
- [YNAB: using multiple currencies](https://support.ynab.com/en_us/using-multiple-currencies-in-ynab-a-guide-SyBF6PHno)
- [Wealthfolio: market data & FX](https://wealthfolio.app/docs/concepts/market-data-and-fx/)
- [Money Lover](https://moneylover.me/vi/)
- [Transaction Categorization with Relational Deep Learning in QuickBooks (arXiv 2506.09234)](https://arxiv.org/abs/2506.09234)
- [Categorising SME Bank Transactions with ML and Synthetic Data (arXiv 2508.05425)](https://arxiv.org/abs/2508.05425)
- [TopoLedgerBERT (arXiv 2407.05175)](https://arxiv.org/abs/2407.05175)

### 5.8 Vấn đề dữ liệu cho tính năng key
Bộ 5.000 giao dịch **không có ngoại tệ**. Cách xử lý:
- **Bắt đầu ghi chép ngay từ bây giờ** mọi giao dịch ngoại tệ của bản thân: số tiền hai bên khi đổi, tiền gốc và tiền bị trừ khi quẹt thẻ, kênh đổi, biên lai. Đến tuần 12 sẽ có khoảng 3 tháng dữ liệu thật để demo và kiểm chứng.
- **Kiểm chứng phí ẩn:** đối chiếu phí hệ thống tính ra với biên lai/sao kê thật. Tỷ giá thị trường lấy từ nguồn công khai.
- **Tình nguyện viên:** du học sinh, người đi làm ở nước ngoài, xin dữ liệu ẩn danh vài tháng.
- **Thí nghiệm dự báo có tỷ giá** (TN2) chỉ cần chuỗi VND thật và tỷ giá lịch sử thật, không phụ thuộc dữ liệu ngoại tệ cá nhân.
- **Phân rã tài sản và phí ẩn** là bài toán tính toán xác định: kiểm chứng bằng **unit test với các kịch bản tính tay**, không cần dữ liệu huấn luyện.

---

## 6. Thiết kế thí nghiệm

### Bước 0: Chuẩn bị dữ liệu
- Làm sạch, **ẩn danh hóa** (số tài khoản, tên người nhận), chuẩn hóa văn bản (có dấu/không dấu, viết tắt).
- Chốt bộ danh mục **10–15 nhãn**, trong đó có nhãn **"Chuyển khoản nội bộ"**. Kiểm tra tính nhất quán của nhãn cũ.
- EDA: phân bố nhãn, số tiền, tính mùa vụ (Tết, ngày nhận lương).
- Thu thập tỷ giá lịch sử 2022 đến nay (VND, USD, JPY, EUR…).

### TN1: Phân loại giao dịch (RQ1, RQ2)

| Nhóm | Mô hình |
|---|---|
| Baseline | Rule-based theo từ khóa |
| Cổ điển | TF-IDF + Logistic Regression / Linear SVM, fastText |
| Transformer | Fine-tune PhoBERT; (tùy chọn) PhoBERT embedding + CNN head |
| LLM | Zero-shot / few-shot, model local (Qwen qua Ollama) so với API |

- **Đặc trưng:** nội dung giao dịch, số tiền (log), giờ, thứ trong tuần, loại tiền, loại ví.
- **Cách chia dữ liệu:** (a) stratified 5-fold CV; (b) theo thời gian: huấn luyện trên 2022–2024, kiểm thử trên 2025–2026.
- **Learning curve:** F1 theo số mẫu huấn luyện 50 / 100 / 200 / 500 / 1000 / toàn bộ.
- **Mô phỏng vòng lặp phản hồi:** duyệt giao dịch theo thời gian, huấn luyện lại hằng tháng, so với không huấn luyện lại.
- **Giải thích:** SHAP cho mô hình tốt nhất.
- **Độ đo:** Accuracy, **Macro-F1**, F1 từng lớp, confusion matrix, độ trễ suy luận (ms), kích thước mô hình.
- **Góc nhìn bảo mật:** dữ liệu tài chính nhạy cảm, nên so sánh model chạy local với API bên ngoài.

### TN2: Dự báo chi tiêu (RQ3a, RQ3b)
- **Mục tiêu dự báo:** tổng chi theo tuần, và chi theo tháng cho các danh mục chính.
- **Mô hình:** Naive / Seasonal Naive (baseline bắt buộc), Moving Average, SARIMA, Prophet (khai báo ngày lễ Việt Nam), LightGBM (đặc trưng lag, rolling, lịch).
- **Đánh giá:** rolling-origin backtest, dự báo trước 1 tuần và 4 tuần.
- **Độ đo:** MAE, RMSE, sMAPE. Không dùng MAPE vì có những ngày chi tiêu bằng 0.
- **So sánh có ý nghĩa thống kê:** dùng **kiểm định Diebold–Mariano** giữa các cặp phương pháp dự báo.
- **Phân tích phụ về tỷ giá (RQ3b):** mô phỏng tiền tệ báo cáo khác VND, so sánh:
  - (A) dự báo trực tiếp trên chuỗi đã quy đổi,
  - (B) dự báo trên chuỗi VND gốc rồi quy đổi bằng tỷ giá gần nhất.

  Lặp lại với **nhiều cặp tiền có độ biến động khác nhau**: USD (ổn định), EUR (trung bình), JPY (mất giá mạnh 2022–2024), có thể thêm KRW, THB. Vẽ **chênh lệch sai số (A − B) theo độ biến động của tỷ giá** và kiểm định Diebold–Mariano cho từng cặp.

  Kết luận mong đợi có dạng: *"với cặp tiền biến động dưới X%, hai cách tương đương; trên X%, nên dự báo theo tiền gốc"*. Kết quả "không khác biệt" ở cặp USD vẫn là một điểm dữ liệu có giá trị.

### TN3 (tùy chọn): Phân loại đa ngôn ngữ (RQ4)
PhoBERT so với XLM-R / multilingual embedding và LLM, trên tập giao dịch tiếng nước ngoài của tình nguyện viên.

### Hạn chế cần nêu trước hội đồng
- Dữ liệu chủ yếu của một người: bổ sung dữ liệu từ 3–5 tình nguyện viên để kiểm tra khả năng tổng quát hóa.
- Tỷ giá từ nguồn công khai là tỷ giá tham khảo, có thể khác tỷ giá thực tế của từng kênh đổi tiền.

---

## 7. Kiểm thử và quy trình
- **Quy trình:** Scrum, sprint 1 tuần, backlog trên GitHub Projects.
- **Kiểm thử:**
  - unit test (JUnit, pytest). **Module Money/FX cần phủ test gần như 100%**: làm tròn, quy đổi chéo, ngày không có tỷ giá, đổi tiền tệ báo cáo, phân rã tài sản.
  - integration test (Testcontainers cho PostgreSQL, Redis).
  - E2E (Playwright), load test (k6).
- **CI/CD:** GitHub Actions chạy build, test rồi deploy.
- **Đánh giá tính năng gợi ý đổi tiền:** mô phỏng trên dữ liệu bán mô phỏng + nghiên cứu tình huống, xem 5.3-11.
- **Đánh giá người dùng:** 5–10 người dùng thử, ưu tiên người có dùng nhiều loại tiền. Đo bằng thang **SUS**.

---

## 8. Kế hoạch 14 tuần

| Tuần | Công việc | Kết quả |
|---|---|---|
| 1 | Đọc tài liệu, EDA, làm sạch và ẩn danh dữ liệu, chốt danh mục, thu thập tỷ giá lịch sử | Đề cương, notebook EDA |
| 2 | Phân tích yêu cầu, use case, **thiết kế CSDL đa tiền tệ**, kiến trúc; tạo repo, Docker, CI | Tài liệu thiết kế, skeleton project |
| 3 | TN1: baseline, TF-IDF + LR/SVM, fastText | Bảng kết quả đợt 1 |
| 4 | TN1: PhoBERT, LLM, learning curve, chia theo thời gian, SHAP | **Chốt mô hình phân loại** |
| 5 | Backend: auth, ví, giao dịch, **module Money** (có unit test), import CSV | API core |
| 6 | **Dịch vụ tỷ giá** (job, cache Redis, dự phòng), đổi tiền, phí ẩn, quy đổi; ML service `/categorize` | Luồng đa tiền tệ chạy được |
| 7 | Frontend core, vòng lặp phản hồi | Nhập → phân loại → sửa nhãn trên UI |
| 8 | TN2: các mô hình dự báo, backtest, thí nghiệm tỷ giá | **Báo cáo giữa kỳ với GVHD** |
| 9 | Tích hợp `/forecast`; ngân sách đa tiền tệ, cảnh báo, dashboard, **phân rã tài sản** | Đủ chức năng chính |
| 10 | Pipeline huấn luyện lại; mở rộng: kế hoạch đổi tiền, TN3 nếu có dữ liệu | Tính năng mở rộng |
| 11 | Kiểm thử unit, integration, E2E, load; sửa lỗi | Báo cáo kiểm thử |
| 12 | Deploy VPS, hoàn thiện UI, người dùng thử, khảo sát SUS | Bản chạy online |
| 13 | Hoàn thiện báo cáo, biểu đồ kết quả | Bản thảo luận văn |
| 14 | Chỉnh sửa, slide, tập demo, **thời gian dự phòng** | Bản nộp cuối |

> Viết báo cáo dần từng tuần. Phát hiện giao dịch bất thường và LSTM đã được **bỏ khỏi kế hoạch chính** để có thời gian cho phần đa tiền tệ. Nếu còn thời gian thì làm, không thì đưa vào hướng phát triển.

---

## 9. Rủi ro và cách giảm

| Rủi ro | Mức | Cách giảm |
|---|---|---|
| Phạm vi phình to vì thêm đa tiền tệ | Cao | Phân tầng MVP / mở rộng (mục 4.5), cắt TN3 và anomaly trước |
| Nhãn cũ không nhất quán | Trung bình | Tuần 1 rà soát, gộp nhãn, ghi lại quy tắc gán nhãn |
| Mô hình phức tạp không thắng baseline | Trung bình | Chấp nhận, phân tích nguyên nhân. Đây vẫn là kết quả khoa học |
| API tỷ giá ngừng hoạt động / giới hạn | Trung bình | Lưu lịch sử vào CSDL, có nguồn dự phòng, cho phép nhập tỷ giá thủ công |
| Dữ liệu một người | Trung bình | Tình nguyện viên, nêu rõ trong phần hạn chế |
| Fine-tune PhoBERT thiếu GPU | Thấp | Google Colab / Kaggle, dữ liệu 5.000 mẫu nhỏ |

---

## 10. Câu hỏi hội đồng có thể hỏi

1. Dữ liệu chỉ của một người thì kết quả có tổng quát không?
2. Tại sao không dùng `double` để lưu tiền?
3. Quy đổi theo tỷ giá ngày giao dịch hay ngày hiện tại? Căn cứ vào đâu?
4. Phí đổi tiền được tính thế nào, tỷ giá thị trường lấy từ đâu?
5. Vì sao chọn Macro-F1 mà không chỉ dùng Accuracy?
6. Mô hình tốt nhất hơn baseline bao nhiêu? Có đáng với chi phí tính toán không?
7. Dữ liệu tài chính nhạy cảm, hệ thống bảo mật thế nào? Có gửi dữ liệu cho LLM bên ngoài không?
8. Hệ thống khác gì Money Lover, Misa, Wise?

---

## 11. Việc cần làm tiếp

- [ ] Xác nhận các cột trong bộ dữ liệu (ngày giờ, số tiền, nội dung, danh mục, ví)
- [x] Dữ liệu có giao dịch ngoại tệ không? **Không**. Bài toán mới gặp gần đây, xem mục 5.8
- [ ] **Bắt đầu ghi chép giao dịch ngoại tệ của bản thân ngay** (số tiền hai bên, kênh đổi, biên lai)
- [x] Khảo sát hiện trạng đa tiền tệ, xem mục 5.7
- [ ] Tự dùng thử Toshl, PocketSmith (bản dùng thử), Firefly III (bản demo) để kiểm chứng bảng 5.7 và chụp màn hình cho chương 2
- [ ] Hỏi khoa mẫu đề cương / báo cáo của CT553H
- [ ] Trao đổi với GVHD: hướng đề tài, khung 5 bước của Chou, phạm vi đa tiền tệ
- [ ] Làm EDA trên dữ liệu thật
- [ ] Tìm tài liệu liên quan: transaction categorization, personal finance ML, PhoBERT, forecasting cá nhân, VAS 10 / IAS 21
- [ ] Kiểm tra nguồn tỷ giá có VND, điều khoản sử dụng, dữ liệu lịch sử (cần cả USD, EUR, JPY, KRW, THB cho RQ3b)
- [ ] Đọc văn bản gốc World Bank *Remittance Prices Worldwide* (phương pháp tính) và Quy định EU 2019/518 để trích dẫn định nghĩa phí ẩn
- [ ] Tìm tài liệu về kiểm định Diebold–Mariano
- [x] Chốt cách xử lý vấn đề "dự báo nhu cầu từng loại tiền khó kiểm chứng": kết hợp tính năng + dự báo phân vị + đánh giá bán mô phỏng trong chương hệ thống (5.3-11)
- [ ] Tìm tài liệu về dự báo phân vị (quantile forecasting) và phương pháp Croston cho chuỗi ngắt quãng
