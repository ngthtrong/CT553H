# Báo cáo phân tích bộ dữ liệu chi tiêu cá nhân

> Đề tài: *Xây dựng hệ thống quản lý chi tiêu cá nhân với bộ phân loại giao dịch tự thích nghi theo phản hồi người dùng và dự báo chi tiêu* (tên dự kiến, xem [brainstorm.md](../01-y-tuong/brainstorm.md))
> Ngày: 24/09/2026 · Mục đích: báo cáo hiện trạng dữ liệu, kết quả thử nghiệm sơ bộ và xin ý kiến GVHD về hướng xử lý.

---

## Tóm tắt

- Bộ dữ liệu gồm **5.465 giao dịch thật** (5.029 khoản chi, 436 khoản thu) do em tự ghi chép trên Notion từ **01/09/2022 đến 23/09/2026** (49 tháng, liên tục, không có tháng trống).
- Toàn bộ giao dịch đã được **gán nhãn thủ công**: 25 nhãn chi, 8 nhãn thu. Dữ liệu sạch về định dạng: không có lỗi ngày, số tiền khớp hoàn toàn với cột kiểm tra.
- Thử nghiệm sơ bộ với TF-IDF + Logistic Regression/SVM đạt **~86% accuracy** khi kiểm định chéo ngẫu nhiên nhưng giảm còn **~78%** khi huấn luyện trên dữ liệu cũ và kiểm thử trên dữ liệu mới. Như vậy, **dữ liệu có hiện tượng thay đổi theo thời gian rõ rệt**, đúng với câu hỏi nghiên cứu RQ2.
- **Vai trò của bộ dữ liệu (cập nhật 27/09/2026):** không dùng để huấn luyện mô hình ban đầu, mà dùng để **đánh giá hệ thống** bằng cách phát lại theo thời gian như một người dùng mới với 25 nhãn được coi là danh mục người dùng tự tạo; tập dev là mẫu ngẫu nhiên ~10%, không tính điểm. Các thử nghiệm sơ bộ ở mục 6 học trên chính dữ liệu này, nên chỉ còn là **mốc tham chiếu**.
- Có 5 khác biệt so với giả định ban đầu của đề cương cần điều chỉnh (mục 7), quan trọng nhất: nội dung giao dịch là **ghi chú tự viết rất ngắn** (trung vị 2 từ), không phải nội dung SMS ngân hàng.

---

## 1. Tổng quan

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | Tự ghi chép hằng ngày, xuất CSV từ Notion |
| Số giao dịch | 5.465 (chi 5.029 · thu 436) |
| Khoảng thời gian | 01/09/2022 – 23/09/2026 (1.484 ngày) |
| Loại tiền | Chỉ VND |
| Tổng chi | 394,7 triệu VND |
| Tổng thu | 430,6 triệu VND (trong đó 149,2 triệu là **tiền vay** vốn sinh viên, xem 4.4) |
| Số tiền mỗi giao dịch | Trung vị 25.000 VND · 75% giao dịch ≤ 46.000 VND · lớn nhất 48 triệu VND |

**Số giao dịch theo năm:** 2022 (4 tháng): 540 · 2023: 1.568 · 2024: 1.521 · 2025: 1.048 · 2026 (9 tháng): 788.

### Các cột dữ liệu

| Cột gốc | Ý nghĩa | Ghi chú |
|---|---|---|
| `Title` | Nội dung giao dịch, tự viết | Trung vị 2 từ / 9 ký tự, ví dụ: "xăng", "cơm sườn trứng", "4g monthly" |
| `Cost` | Số tiền | Dạng chuỗi "₫745,000", đã chuyển thành số nguyên |
| `Date` | Ngày giao dịch | Chỉ có ngày, **không có giờ** |
| `Type Expenses` | Nhãn khoản chi | 25 nhãn |
| `Ex/In` | Chi / thu | |
| `Special` | Đánh dấu khoản đặc biệt | `Monthly` (định kỳ tháng), `BigM` (lớn trong tháng), `BigY` (lớn trong năm), `Vay`, `Annual` |
| `Type In come` | Nhãn khoản thu | 8 nhãn |
| `Budget` | Số tiền có dấu (chi âm, thu dương) | Trùng lặp với `Cost`, đã kiểm tra khớp 100% |
| `Created time` | Thời điểm tạo bản ghi trên Notion | Dùng để đánh giá độ trễ ghi chép |

---

## 2. Phân bố nhãn

### 2.1 Nhãn khoản chi (25 nhãn)

| Nhãn | Số GD | Tỷ lệ | Tổng tiền (triệu) | Nội dung điển hình |
|---|---:|---:|---:|---|
| AC | 1.695 | 33,7% | 50,3 | bánh mì, hủ tiếu, cơm sườn (bữa ăn chính) |
| DC | 508 | 10,1% | 19,8 | xăng (di chuyển) |
| Bida | 419 | 8,3% | 15,0 | bida |
| AV | 379 | 7,5% | 5,8 | nước mía, nước cam, tàu hủ (ăn vặt, đồ uống) |
| Badmintion | 368 | 7,3% | 14,3 | cầu lông, sân cầu, quấn cán |
| Utility | 367 | 7,3% | 23,7 | phí rút tiền, iCloud, 4G, card điện thoại |
| Study | 346 | 6,9% | 166,4 | gửi xe ở trường, photo, **học phí** |
| Coffee | 257 | 5,1% | 5,1 | cafe |
| RL | 208 | 4,1% | 6,8 | ăn uống, giải trí cùng bạn bè |
| Home | 154 | 3,1% | 39,8 | ký túc xá, điện nước, đồ gia dụng |
| 15 nhãn còn lại | 327 | 6,5% | 40,1 | Body, G, CL, Accident, Entertainment, Mental, Smoking, Ngu, Swimming, Family, Gym, Sport, NET, English, Cho vay |

- **Mất cân bằng mạnh:** nhãn lớn nhất chiếm 33,7%, **9 nhãn có dưới 20 mẫu** (English 4, Cho vay 3). Do đó cần dùng **Macro-F1** làm độ đo chính.
- **94,4% số giao dịch là chi tiêu thường ngày nhưng chỉ chiếm 35,3% tổng tiền.** 64,7% tổng tiền nằm ở các khoản được đánh dấu `Special` (học phí, tiền nhà, mua sắm lớn).

### 2.2 Nhãn khoản thu (8 nhãn)

Family 294 GD (227,9 triệu) · Salary 67 (38,7 triệu) · Anh em 28 · Clan 24 · Sell old things 8 · **Cho vay 7 (149,2 triệu)** · Invest 4 · Luck 4.

---

## 3. Đặc điểm nổi bật của dữ liệu

1. **Văn bản rất ngắn, nhiều biến thể viết.** Cùng một nội dung có nhiều cách viết: "cafe / cf / caffe / coffe / cà phê", "cầu lông / cầu long / cầu", "cơm sườn / cơm sờn / cờm sườn / cơn sườn". Có viết tắt, sai chính tả, có dấu và không dấu lẫn lộn.
2. **Lặp lại nhiều:** 5.028 khoản chi có nhãn chỉ có 1.973 nội dung khác nhau. Riêng "xăng" xuất hiện 444 lần.
3. **Nhãn phụ thuộc ngữ cảnh, không chỉ nội dung.** Nhãn thể hiện *mục đích* và *đi cùng ai*, không chỉ *mua gì*. Ví dụ "nước mía" thường là AV nhưng là RL khi đi cùng bạn; "cafe" có thể là Coffee, RL hoặc Mental. Điều này đặt ra giới hạn trên cho mọi mô hình chỉ dùng văn bản.
4. **Có tên người trong nội dung** (bạn bè, người thân), ví dụ mẫu "bida với [tên]". Đây là tín hiệu phân loại hữu ích nhưng là **thông tin nhạy cảm**, cần ẩn danh (mục 5).
5. **Ghi chép khá kịp thời:** với 1.566 giao dịch được nhập trực tiếp (không nhập hàng loạt), 92,9% được ghi trong ngày hoặc ngày hôm sau.

---

## 4. Các vấn đề chất lượng dữ liệu

| # | Vấn đề | Quy mô | Cách xử lý |
|---|---|---|---|
| 4.1 | **Nhãn không nhất quán**: cùng một nội dung nhưng gán nhãn khác nhau | 82 nội dung, 154 giao dịch (3,1%) mang nhãn thiểu số. Ví dụ: "xăng" 444 lần DC, 2 lần AC | Đã đánh dấu `flag_label_minority`. Cần rà soát thủ công trước khi huấn luyện |
| 4.2 | **Bản ghi điều chỉnh**, không phải giao dịch thật ("cân bằng số liệu", "điều chỉnh chênh lệch…") | 2 dòng (1 dòng 7,7 triệu, không có nhãn) | Loại khỏi tập huấn luyện và thống kê |
| 4.3 | **Nghi trùng lặp**: trùng nội dung, số tiền, ngày, nhãn | 23 nhóm, 47 dòng | Chỉ đánh dấu, **không xóa tự động**, vì có thể là giao dịch thật (ví dụ mua 3 phần cơm cùng giá trong một ngày) |
| 4.4 | **Tiền vay và cho vay ghi thành thu/chi** | 10 dòng; riêng vay vốn sinh viên 128 triệu | Tách thành loại giao dịch riêng (không phải thu nhập), đúng với thiết kế `TRANSFER` trong đề cương |
| 4.5 | **Học phí luân chuyển**: gia đình gửi tiền (ghi là thu Family), sau đó đóng học phí (ghi là chi Study) | ~19 dòng, mỗi dòng 3–22 triệu | Loại khỏi chuỗi dự báo chi tiêu thường ngày |
| 4.6 | **Chuyến đi nước ngoài ghi thành một khoản tổng** (Malaysia 12/2025: 4,1 triệu; Đài Loan 09–11/2026: 14,2 triệu) | 2 dòng | Đánh dấu. Loại khỏi thí nghiệm phân loại và chuỗi dự báo chi tiêu thường ngày |
| 4.7 | **Mật độ ghi chép giảm dần** | Trung bình 120 GD/tháng (2022–2024) còn 81 GD/tháng (2025–2026). Tỷ lệ ngày không có khoản chi nào tăng từ 7% (2022) lên 32% (2026) | Cần xác định do chi ít đi, do gộp nhiều khoản, hay do bỏ sót. Ảnh hưởng trực tiếp đến dự báo |
| 4.8 | **Ngày giao dịch sau ngày nhập liệu** | 164 dòng | Phần lớn là khoản ghi trước (kế hoạch) hoặc nhập nhầm năm. Cần rà soát |
| 4.9 | Nội dung có xuống dòng, khoảng trắng đặc biệt | 5 dòng | Đã chuẩn hóa (Unicode NFC, gộp khoảng trắng) |
| 4.10 | Lỗi chính tả tên nhãn (`Badmintion`) | | Chuẩn hóa khi chốt bộ nhãn mới |

---

## 5. Xử lý đã thực hiện

Script `ml/quan-ly-chi-tieu-ca-nhan/preprocessing/clean_data.py` (file gốc giữ nguyên, có thể chạy lại):

1. Chuyển số tiền sang số nguyên, ngày sang kiểu ngày, chuẩn hóa văn bản.
2. Tách cột `Special` thành các cờ `is_monthly`, `is_bigm`, `is_bigy`, `is_vay`, `is_annual`, `is_regular`.
3. Thêm các cờ chất lượng: `flag_adjustment`, `flag_loan_flow`, `flag_trip_lump_sum`, `flag_missing_label`, `flag_possible_duplicate`, `flag_label_minority`.
4. Đánh dấu các bản ghi nhập hàng loạt (`is_backfilled`) và tính độ trễ ghi chép (`entry_lag_days`).
5. **Ẩn danh:** thay 39 tên người bằng mã cố định `[P01]`, `[P02]`… (611 dòng bị thay đổi). Mã hóa nhất quán nên mô hình vẫn học được tín hiệu "đi cùng ai". Bỏ cột thời điểm nhập liệu.

| File đầu ra | Nội dung | Phạm vi sử dụng |
|---|---|---|
| `data/quan-ly-chi-tieu-ca-nhan/processed/transactions_clean.csv` | Đầy đủ, chưa ẩn danh | Chỉ dùng cá nhân |
| `data/quan-ly-chi-tieu-ca-nhan/processed/transactions_anon.csv` | Đã ẩn danh tên người | Gửi GVHD, đưa vào phụ lục |

> Bản ẩn danh vẫn còn tên địa điểm (trường, quán, đường). Nếu công bố dữ liệu công khai thì cần ẩn danh thêm mức này.

---

## 6. Thử nghiệm sơ bộ

### 6.1 Phân loại khoản chi (mốc tham chiếu cho RQ2)

Thiết lập: 5.028 khoản chi có nhãn, 25 nhãn, chỉ dùng nội dung văn bản. Đặc trưng TF-IDF kết hợp n-gram từ (1–2) và n-gram ký tự (2–5).

| Mô hình | Kiểm định chéo 5-fold (phân tầng) | | Chia theo thời gian (train 2022–2024, test 2025–2026) | |
|---|---:|---:|---:|---:|
| | Accuracy | Macro-F1 | Accuracy | Macro-F1 |
| Nhãn phổ biến nhất | 33,7% | 0,02 | 27,5% | 0,02 |
| Tra cứu nội dung đã gặp | 74,0% | 0,44 | 62,0% | 0,28 |
| TF-IDF + Logistic Regression | 85,7% | 0,66 | 78,0% | 0,46 |
| TF-IDF + Linear SVM | **86,7%** | **0,66** | **78,2%** | 0,45 |

**Nhận xét:**

- **Dữ liệu thay đổi theo thời gian là vấn đề thật, đo được.** Khi chia theo thời gian, accuracy giảm ~9 điểm, Macro-F1 giảm ~0,2. Nguyên nhân:
  - Tỷ lệ nội dung **chưa từng gặp** trong tập test tăng từ 34% lên 53%.
  - **5 nhãn mới** chỉ xuất hiện từ 2025 (Swimming, Sport, NET, English, Cho vay).
  - Phân bố nhãn thay đổi theo thói quen: Bida từ 3,8% lên 17,4%, cầu lông từ 9,8% xuống 2,4%.
- **Nội dung đã gặp** phân loại đúng ~92%. **Nội dung mới** chỉ đúng 65–72%. Đây là chỗ mô hình ngữ nghĩa (PhoBERT, LLM) có thể tạo khác biệt.
- **Learning curve** (lấy N giao dịch đầu tiên theo thời gian, test trên 2025–2026): 50 mẫu 40% · 200 mẫu 50% · 1.000 mẫu 56% · 2.000 mẫu 73% · 3.348 mẫu 78%. Đường cong này lẫn cả ảnh hưởng của số mẫu và của thay đổi theo thời gian, cần thiết kế lại để tách hai yếu tố.
- **Lỗi thường gặp:** RL, G (nhãn phụ thuộc ngữ cảnh "đi cùng ai") và các nhãn ít mẫu.

### 6.2 Dự báo chi tiêu (RQ3)

Chuỗi: tổng chi **thường ngày** theo tuần (bỏ các khoản `Special`), 211 tuần. Trung bình 646.000 VND/tuần, hệ số biến thiên 0,40.

Backtest rolling-origin, dự báo trước 1 tuần, 52 tuần gần nhất:

| Mô hình | MAE (VND) | sMAPE |
|---|---:|---:|
| Naive (bằng tuần trước) | 240.192 | 31,6% |
| Trung bình 4 tuần | 193.510 | 25,3% |
| Trung bình 8 tuần | 193.990 | 26,1% |
| Trung bình toàn bộ lịch sử | **183.837** | **24,5%** |

**Nhận xét:** chi tiêu thường ngày khá ổn định nên baseline đơn giản đã khó vượt. Mô hình phức tạp (SARIMA, Prophet, LightGBM) cần được so sánh công bằng với baseline này. Các khoản lớn (`BigM`, `BigY`) chiếm 65% tổng tiền nhưng thưa và không đều, nên được xử lý riêng (lịch định kỳ hoặc loại khỏi dự báo).

---

## 7. So sánh với giả định trong đề cương

| Giả định ban đầu | Thực tế dữ liệu | Hướng điều chỉnh đề xuất |
|---|---|---|
| Nội dung giao dịch giống SMS/sao kê ngân hàng | Ghi chú tự viết, trung vị 2 từ, nhiều viết tắt | Bài toán là *phân loại ghi chú chi tiêu ngắn tiếng Việt*. Nếu muốn giữ tính năng "dán thông báo ngân hàng" thì cần thu thập thêm dữ liệu SMS |
| Có đặc trưng giờ giao dịch | Chỉ có ngày | Bỏ đặc trưng giờ. Dùng thứ trong tuần, ngày trong tháng, số tiền |
| Có ví/tài khoản và nhãn "Chuyển khoản nội bộ" | Không có cột ví, không có giao dịch chuyển khoản nội bộ | Thiết kế ví vẫn giữ trong hệ thống, nhưng không có dữ liệu huấn luyện cho nhãn này |
| Không có dữ liệu ngoại tệ | Có 2 chuyến đi nước ngoài, bị ghi thành một khoản tổng bằng VND | Đa tiền tệ đã hạ xuống tính năng phụ, không cần dữ liệu ngoại tệ (quyết định 27/09/2026) |
| Bộ nhãn 10–15 nhãn | 25 nhãn, nhiều nhãn rất ít mẫu | Gộp nhãn (phương án ở mục 8) |

---

## 8. Nội dung xin ý kiến GVHD

1. **Bộ nhãn:** 25 nhãn gốc được coi là **danh mục do người dùng tự tạo** và là kịch bản chính. Kịch bản phụ gộp về 10–12 danh mục chuẩn để so sánh. Một phương án gộp (bảng ánh xạ chính thức sẽ viết trước khi chạy thí nghiệm):

   | Nhóm đề xuất | Nhãn gốc |
   |---|---|
   | Ăn uống | AC, AV, Coffee |
   | Di chuyển | DC |
   | Học tập | Study, English |
   | Nhà ở | Home |
   | Hóa đơn, tiện ích | Utility |
   | Thể thao | Badmintion, Swimming, Gym, Sport |
   | Giải trí | Bida, NET, Entertainment |
   | Quan hệ xã hội | RL, G, Family |
   | Cá nhân, mua sắm | Body, CL |
   | Chi phát sinh, khác | Accident, Ngu, Mental, Smoking |
   | *(không phải chi tiêu)* | Cho vay: chuyển sang loại giao dịch riêng |

2. **Cách đánh giá chính:** phát lại dữ liệu theo thời gian (đoán trước, học sau) thay cho kiểm định chéo. Tinh chỉnh chỉ trên tập dev (mẫu ngẫu nhiên ~10%, vẫn đi qua luồng để hệ thống học nhưng không tính điểm). Cách này có thuyết phục không?
3. **Nhãn phụ thuộc ngữ cảnh** (RL, G): mô hình tổng quát gần như không đoán được nhóm này. Dự kiến để lớp cá nhân học (ví dụ từ mã người `[P03]`), và xem đây là chỗ chứng minh giá trị của thích nghi. Có hợp lý không?
4. **Tình nguyện viên:** mỗi người tự đặt danh mục, cung cấp 100–200 ghi chú đã gán nhãn, chỉ để đánh giá. Cần tối thiểu bao nhiêu người?

---

## 9. Bước tiếp theo

- [ ] Rà soát 154 giao dịch có nhãn không nhất quán và 164 giao dịch có ngày bất thường.
- [ ] Viết mô tả một câu cho 25 danh mục (trước khi chạy thí nghiệm); viết bảng ánh xạ về danh mục chuẩn cho kịch bản phụ.
- [ ] Tách tập dev ngẫu nhiên ~10% (seed cố định) trong script tiền xử lý.
- [ ] Gán nhãn lại mù 300 mẫu theo 25 danh mục, tính Cohen's kappa.
- [ ] Phân tích nguyên nhân mật độ ghi chép giảm (mục 4.7) trước khi làm thí nghiệm dự báo.
- [x] ~~Ghi chép chi tiết giao dịch ngoại tệ~~ (đã bỏ, 27/09/2026).
