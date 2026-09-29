# Khảo sát: các ứng dụng xử lý ghi chép chi tiêu đa tiền tệ như thế nào

> Ngày khảo sát: 24/09/2026 · Phục vụ: [de-tai-1-brainstorm.md](../01-y-tuong/de-tai-1-brainstorm.md) (mục 5, đặc biệt 5.3 và 5.7)
> **Cập nhật 27/09/2026:** đa tiền tệ đã được hạ xuống **tính năng phụ** của hệ thống, không còn câu hỏi nghiên cứu, bỏ case study ngoại tệ (xem brainstorm mục 0.1 và 5). Khảo sát này vẫn dùng cho thiết kế module Money/FX và bảng so sánh ở chương 2. Các mục trong brainstorm được nhắc tới dưới đây giữ nguyên số mục.
> Phương pháp: đọc tài liệu chính thức, help center, issue trên GitHub của từng ứng dụng. **Chưa dùng thử trực tiếp.** Những điểm lấy từ nguồn thứ ba hoặc chưa đọc được trang gốc được đánh dấu *(chưa kiểm chứng)*.

---

## 0. Tóm tắt

1. **Có 4 mô hình xử lý đa tiền tệ** trên thị trường, từ đơn giản đến chặt chẽ: (A) đơn tiền tệ, (B) ví theo tiền tệ + quy đổi khi hiển thị, (C) mỗi giao dịch mang tiền tệ riêng + tỷ giá lịch sử, (D) kế toán kép đa hàng hóa (GnuCash, Beancount, hledger). Thiết kế ở mục 5.3 của đề tài thuộc mô hình **C, có mượn ý tưởng của D**.
2. **Đổi tiền:** app tốt bắt người dùng **nhập số tiền cả hai bên** (Firefly III, GnuCash, Beancount `@@`). App phổ thông thường chỉ cho nhập một số tiền + tỷ giá. **Phí/chênh lệch tỷ giá gần như luôn bị "nuốt"**: không tách ra, hoặc chỉ được dung sai khi ghép cặp (Toshl cho lệch 5%).
3. **Giao dịch ngoại tệ:** app tốt lưu **cả tiền gốc lẫn tiền bị trừ** và quy đổi theo **tỷ giá ngày giao dịch** (Toshl, Lunch Money, PocketSmith). Một số app dùng **tỷ giá hiện tại** cho dữ liệu cũ, làm thống kê quá khứ thay đổi theo ngày (Wallet, Splitwise khi quy đổi). Ngay Firefly III cũng từng dính lỗi này (issue #12455).
4. **Ví:** mô hình phổ biến nhất là **mỗi ví một loại tiền**, ví đa tiền tệ (Wise, Revolut) tách thành nhiều ví con. Tổng tài sản = tổng số dư quy đổi theo **tỷ giá hiện tại**.
5. **Bức tranh tài chính:** hầu hết chỉ dừng ở "tổng quy đổi về tiền tệ báo cáo" + "tổng theo từng loại tiền". Ngân sách đa tiền tệ có 2 trường phái: **mỗi loại tiền một hạn mức** (Firefly III) hoặc **quy đổi về một hạn mức** (Toshl, PocketSmith). **Tách biến động tài sản do tỷ giá: không thấy ở app chi tiêu phổ thông, nhưng ĐÃ CÓ trong phần mềm kế toán kép** (trading accounts của GnuCash, `--gain`/`--valuechange` của hledger).
6. **Hàm ý quan trọng nhất cho đề tài:** câu *"phân rã biến động tổng tài sản: chưa thấy"* ở mục 5.7 **cần sửa**. Nên định vị lại: *đưa khái niệm lãi/lỗ tỷ giá của kế toán kép vào giao diện dành cho người không biết kế toán*, và dùng lý thuyết trading accounts của Selinger làm cơ sở. Chi tiết ở mục 7.

---

## 1. Các ứng dụng được khảo sát

| Nhóm | Ứng dụng | Vì sao chọn |
|---|---|---|
| App chi tiêu phổ thông | Money Lover, Sổ Thu Chi MISA, Spendee, Wallet (BudgetBakers) | Đối thủ trực tiếp, có người dùng Việt |
| App quản lý tài chính "nghiêm túc" | Toshl, PocketSmith, Lunch Money, Firefly III (mã nguồn mở) | Hỗ trợ đa tiền tệ tốt nhất, có tài liệu công khai |
| App **không** hỗ trợ đa tiền tệ | YNAB, Monarch Money, Actual Budget | Làm đối chứng: không hỗ trợ thì người dùng xoay xở ra sao |
| Kế toán kép cá nhân | GnuCash, Beancount, hledger | Cách làm "đúng chuẩn kế toán", là cơ sở lý thuyết |
| App du lịch / chia tiền | TravelSpend, Splitwise | Bài toán ngắn hạn, nhiều loại tiền |
| Ngân hàng số đa tiền tệ | Wise, Revolut | Là **nguồn dữ liệu** và là chuẩn về minh bạch phí, không phải app ghi chép |

---

## 2. Bốn mô hình xử lý đa tiền tệ

| Mô hình | Cách làm | Ứng dụng | Ưu | Nhược |
|---|---|---|---|---|
| **A. Đơn tiền tệ** | Cả hệ thống một loại tiền. Muốn dùng tiền khác thì tạo ngân sách riêng hoặc tự quy đổi tay | YNAB (khuyên tạo budget riêng cho mỗi loại tiền), Actual Budget (chỉ có tính năng hiển thị thử nghiệm từ 11/2025), Monarch | Đơn giản | Không có tổng tài sản. Monarch hiển thị giao dịch 1.000 JPY thành "$1,000" |
| **B. Ví theo tiền tệ, quy đổi khi hiển thị** | Mỗi ví một loại tiền. Tổng hợp thì quy đổi, thường theo **tỷ giá hiện tại** | Money Lover, Wallet, Spendee, MISA | Dễ hiểu với người dùng phổ thông | Thống kê quá khứ "trôi" theo tỷ giá; đổi tiền và phí xử lý sơ sài |
| **C. Giao dịch mang tiền tệ riêng, tỷ giá lịch sử** | Mỗi giao dịch lưu tiền gốc; quy đổi theo tỷ giá **ngày giao dịch**, cho sửa tỷ giá | Toshl, Lunch Money, PocketSmith, Firefly III (trường *foreign amount*), TravelSpend | Báo cáo cũ ổn định, phản ánh đúng số tiền thật đã trả | Không tự tách được phần tài sản thay đổi do tỷ giá |
| **D. Kế toán kép đa hàng hóa** | Mỗi tài khoản một "hàng hóa" (tiền tệ, cổ phiếu). Đổi tiền là một bút toán hai vế cân bằng; chênh lệch đi vào tài khoản trung gian (*trading* / *conversion*) | GnuCash, Beancount, hledger | Chặt chẽ nhất, **tính được lãi/lỗ tỷ giá** | Người không biết kế toán không dùng nổi |

**Nhận xét:** Mô hình C là "chuẩn ngành" cho app cá nhân tốt. Mô hình D là chuẩn kế toán. Đề tài đang đứng ở C và muốn làm thêm một phần việc của D (phân rã tỷ giá) mà vẫn giữ giao diện của C. Đây là định vị hợp lý, nhưng phải nói rõ phần "mượn" từ D.

---

## 3. Câu hỏi 1: Việc đổi tiền được xử lý như thế nào?

### 3.1 Bảng so sánh

| Ứng dụng | Cách ghi đổi tiền | Số tiền hai bên? | Phí / chênh lệch tỷ giá |
|---|---|---|---|
| **Firefly III** | Giao dịch loại *transfer* giữa hai tài khoản khác tiền | **Bắt buộc** nhập cả hai ("you must set the amount of the transfer in both currencies") | Không tách. Tỷ giá ngầm = số nhận / số gửi. UI từng lỗi mất trường *foreign amount* (issue #3909, #12855) |
| **GnuCash** | *Transfer Funds* + hộp thoại *Edit Exchange Rate*, nhập tỷ giá ngân hàng đưa | Có (nhập tỷ giá hoặc số tiền đích) | Nếu bật **trading accounts**, chênh lệch tự vào tài khoản `Trading:CURRENCY`. Nếu không, bán ngoại tệ phải tự tách bút toán lãi/lỗ |
| **Beancount / hledger** | `-10000000 VND` / `380 USD @@ 10000000 VND` hoặc cân bằng qua `equity:conversion` | Có | Cách `equity:conversion` ghi lại **toàn bộ lãi/lỗ tích lũy** từ các lần đổi |
| **Toshl** | Hai bút toán (chi ở ví A, thu ở ví B) được **ghép cặp** thành chuyển khoản | Có (hai bút toán riêng) | Ghép cặp tự động nếu cách nhau **≤ 4 ngày** và lệch **≤ 5%** sau khi quy đổi về tiền chính. **Phần lệch (chính là phí) bị bỏ qua**, không hiện thành dòng riêng |
| **Wallet (BudgetBakers)** | Chuyển khoản giữa hai tài khoản, có thể đặt tỷ giá tùy chỉnh cho lần chuyển | Qua tỷ giá *(chưa kiểm chứng trang gốc)* | Không tách |
| **Money Lover, Spendee, MISA** | Chuyển tiền giữa các ví | Thường chỉ một số tiền + tỷ giá *(chưa kiểm chứng)* | Không tách |
| **PocketSmith** | Hai giao dịch ở hai tài khoản, gắn danh mục *transfer* | Có | Không tách. Tài liệu ghi rõ: **chưa hỗ trợ quy đổi cho ngân sách chuyển khoản khác tiền**, phải tạo hai ngân sách riêng và tự quy đổi tay |
| **YNAB** (không có đa tiền tệ) | Người dùng tự ghi thành chi ở budget này, thu ở budget kia | Không | Không có khái niệm |
| **Wise, Revolut** | Đổi trong app | Có | **Hiển thị phí rõ ràng trước khi xác nhận**: Wise = mid-market + phí 0,35–2,85%; Revolut = tỷ giá liên ngân hàng ngày thường, cộng thêm ~0,5–1% cuối tuần tùy gói. **Chỉ minh bạch cho kênh của chính họ** |

### 3.2 Những gì rút ra

- **Nhập hai số tiền là cách đúng.** Tỷ giá thực tế chỉ là hệ quả. App cho nhập "một số tiền + tỷ giá" làm mất thông tin khi phí được thu riêng (phí cố định + spread).
- **Không app chi tiêu nào tự tính phí ẩn so với một tỷ giá tham chiếu.** Toshl còn **cố ý bỏ qua** chênh lệch bằng dung sai 5%, tức chấp nhận "mất" một khoản mà đề tài muốn làm lộ ra. Điều này **khẳng định khoảng trống** ở mục 5.7 của brainstorm.
- **Wise/Revolut là chuẩn tham chiếu về minh bạch phí**, nhưng họ chỉ minh bạch cho giao dịch của họ. Đề tài làm được việc họ không làm: so **mọi kênh** (ngân hàng, tiệm vàng, chợ đen, Wise…) trên cùng một thước đo mid-market.
- **Kỹ thuật ghép cặp của Toshl** (khung thời gian + dung sai sau quy đổi) là baseline tốt cho nhãn "Chuyển khoản nội bộ" trong TN1. Có thể so: *luật ghép cặp kiểu Toshl* vs *mô hình ML*.
- **Lỗi hay gặp** (Firefly III): giao diện tạo chuyển khoản khác tiền ẩn mất ô số tiền thứ hai. Module Money/FX cần test E2E cho đúng luồng này.

---

## 4. Câu hỏi 2: Giao dịch bằng các ngoại tệ khác nhau được xử lý như thế nào?

### 4.1 Hai tình huống cần phân biệt

| Tình huống | Ví dụ | Cần lưu gì |
|---|---|---|
| **Chi bằng tiền của ví** nhưng ví khác tiền báo cáo | Trả 3.000 JPY từ ví JPY, tiền báo cáo VND | Số tiền JPY + tỷ giá quy đổi về VND |
| **Chi bằng tiền khác tiền của ví** (quẹt thẻ nước ngoài) | Quẹt thẻ Visa VND ở Nhật: hóa đơn 3.000 JPY, thẻ bị trừ 540.000 VND | **Cả hai số** + tỷ giá báo cáo |

### 4.2 Cách các app xử lý

| Ứng dụng | Quẹt thẻ nước ngoài | Tỷ giá quy đổi về tiền báo cáo | Sửa tỷ giá |
|---|---|---|---|
| **Firefly III** | `amount` (tiền của tài khoản) + `foreign amount` (tiền gốc), bắt buộc nhập cả hai | Tỷ giá trong hệ thống. **Không tự tải tỷ giá lịch sử.** Từng lỗi dùng tỷ giá **hôm nay** thay vì ngày giao dịch khi tính lại (issue #12455, sửa ở v6.7.0) | Có (nhập *foreign amount* thì dùng số đó) |
| **Toshl** | Nhập ở bất kỳ tiền nào; màn hình hiện đồng thời tiền gốc, tiền của ví, tiền chính | **Tỷ giá ngày giao dịch**, dữ liệu từ 1999, cập nhật hằng giờ | Có, "custom rate that better reflects the price you paid" |
| **Lunch Money** | Giao dịch đồng bộ ngân hàng mang tiền của tài khoản; có tùy chọn ghi đè loại tiền khi Plaid trả sai | **Tỷ giá ngày giao dịch**; ngày không có tỷ giá thì lấy **ngày gần nhất** | Không thấy trong tài liệu |
| **PocketSmith** | Theo tiền của tài khoản | **Tỷ giá lưu theo từng ngày**; số dư quy đổi theo ngày số dư cuối | Không thấy |
| **Spendee** | Giao dịch khác tiền ví, hiển thị cả hai tiền | Tự cập nhật mỗi 24h; không nói rõ ngày nào | Có, và có thể "nhớ" tỷ giá cho lần sau |
| **Wallet** | Theo tài khoản | Tỷ giá cập nhật hằng đêm. Theo góp ý của người dùng trên trang feedback của hãng, **thống kê bị méo khi tỷ giá đổi** vì dùng tỷ giá hiện tại *(chưa kiểm chứng trang gốc)* | Có, có thể tắt tự cập nhật |
| **Money Manager Ex** | Theo tài khoản | Có tùy chọn **"Use historical currency rates"**, tắt thì dùng tỷ giá hiện tại | Có |
| **TravelSpend** | Nhập ở tiền địa phương, quy về tiền nhà | Tỷ giá trực tuyến, hoặc tỷ giá đã cache khi offline | Có |
| **Splitwise** | Mỗi chi phí một loại tiền, **số dư tách theo từng loại tiền** | Bản Pro: quy đổi **toàn bộ lịch sử theo tỷ giá hiện tại** | Không. Đổi loại tiền ở bản miễn phí **chỉ đổi nhãn, không quy đổi số** |

### 4.3 Những gì rút ra

- **Tỷ giá ngày giao dịch cho thu/chi** là lựa chọn của các app tốt, trùng với VAS 10 / IAS 21 mà đề tài đang dựa vào. Đây là điểm **đã phổ biến**, không phải điểm mới.
- **Luôn cho sửa tỷ giá.** Tỷ giá nguồn công khai chỉ là tham chiếu. Nếu người dùng nhập hai số tiền thì dùng hai số đó, như Firefly III.
- **Lưu tỷ giá đã dùng vào giao dịch** (cột `fx_rate_to_base` của đề tài) là bắt buộc. Lỗi #12455 của Firefly III cho thấy tính lại hàng loạt mà dùng nhầm ngày là hỏng toàn bộ báo cáo cũ. Đây là một ca unit test đáng có.
- **Chiến lược "ngày gần nhất" khi thiếu tỷ giá** (Lunch Money) giống mục 5.3-3 của brainstorm. Nên chọn rõ: "gần nhất **trước đó**" (không nhìn tương lai) và ghi vào tài liệu.
- **Không phân biệt nhãn tiền và quy đổi** là lỗi thiết kế có thật (Splitwise, Monarch). Giao diện đề tài cần chặn việc đổi loại tiền của ví đã có giao dịch (Spendee cũng chặn).

---

## 5. Câu hỏi 3: Ví tiền được quản lý ra sao?

| Khía cạnh | Cách làm phổ biến | Ví dụ |
|---|---|---|
| **Tiền tệ của ví** | Mỗi ví một loại tiền, chọn lúc tạo | Firefly III, Wallet, PocketSmith, Spendee, Money Lover, GnuCash |
| **Đổi loại tiền của ví** | Không cho đổi khi đã có giao dịch | Spendee |
| **Ví đa tiền tệ (Wise, Revolut)** | Tách thành nhiều ví con, mỗi ví một loại tiền | Wallet ("create a separate account for each currency"), PocketSmith, Firefly III |
| **Danh sách tiền tệ** | Chỉ bật những loại cần dùng; hỗ trợ tiền tự định nghĩa (crypto, vàng, điểm thưởng) | Firefly III (phải *enable* trước; 2–12 chữ số thập phân), GnuCash (tiền giả XTS/XXX), Toshl & PocketSmith (vàng, bạc, crypto), MISA (giá vàng cập nhật hằng ngày) |
| **Tổng tài sản** | Cộng số dư các ví sau khi quy đổi theo **tỷ giá hiện tại** | Tất cả app mô hình B, C, D |
| **Loại ví khỏi tổng** | Cờ "không tính vào tổng" | Money Lover ("exclude from total", nhóm "Total Wallet") |
| **Cây tài khoản** | Tài khoản cha/con được khác tiền; số dư cha quy đổi về tiền của cha | GnuCash |
| **Số dư nợ nhiều loại tiền** | Giữ riêng từng loại tiền, không tự cộng | Splitwise ("You owe $12.45 and you are owed £8.72") |

**Những gì rút ra:**
- Thiết kế "một ví một loại tiền, ví đa tiền tệ tách ví con" ở mục 5.3-2 **trùng với số đông**, là lựa chọn an toàn.
- Nên có **nhóm ví** (ví dụ "Wise" gồm Wise-USD, Wise-EUR, Wise-JPY) để giao diện không bị rối. Chưa thấy app phổ thông nào làm tốt điều này; GnuCash làm được nhờ cây tài khoản.
- Nên có cờ **"không tính vào tổng"** (ví tiết kiệm mục tiêu, ví hộ người khác) như Money Lover.
- Vàng là "loại tiền" rất phổ biến với người Việt (MISA có). Có thể coi là mở rộng rẻ vì mô hình dữ liệu đã hỗ trợ `minor_unit` và tỷ giá tùy chọn.

---

## 6. Câu hỏi 4: Bức tranh tài chính được trình bày như thế nào?

### 6.1 Các lớp thông tin mà app hiện có trình bày

| Lớp | Cách trình bày | Ứng dụng |
|---|---|---|
| **Tổng tài sản / net worth** | Một con số ở tiền tệ báo cáo, theo tỷ giá hiện tại | PocketSmith, Lunch Money, Toshl, Wallet, Money Lover |
| **Tiền gốc hay tiền quy đổi** | Công tắc: xem số dư và giao dịch theo **tiền gốc** hoặc **quy đổi**; tooltip hiện số còn lại | PocketSmith ("Show amounts in base currency instead of native where possible") |
| **Tổng theo từng loại tiền** | Khi xem tiền gốc, tổng mỗi loại tiền hiển thị riêng, không cộng | PocketSmith, Splitwise, Money Lover |
| **Thống kê chi tiêu** | Quy đổi về tiền chính (Toshl: mọi biểu đồ và tổng dùng tiền chính, đổi được bất cứ lúc nào) | Toshl, Spendee, Lunch Money |
| **Ngân sách** | (1) **Mỗi loại tiền một hạn mức**, giao dịch tiền khác không bị tính; (2) **một hạn mức**, giao dịch tiền nào cũng quy đổi rồi trừ vào | (1) Firefly III ("a budget of EUR 100 will not be influenced by transactions in USD"), PocketSmith (tiền ngân sách = tiền của tài khoản); (2) Toshl (ngân sách du lịch bằng tiền địa phương, "expenses in any currency can still count against it"), TravelSpend (ngân sách tổng chuyến / theo ngày) |
| **Dự báo dòng tiền** | Theo giao dịch định kỳ đã lập lịch, không dùng ML | PocketSmith |
| **Ảnh hưởng tỷ giá** | *Xem mục 6.2* | |

### 6.2 Ảnh hưởng của tỷ giá lên tài sản: ai làm được gì

| Mức độ | Ứng dụng | Cách làm |
|---|---|---|
| Không có | Money Lover, Spendee, Wallet, Lunch Money, Toshl, Firefly III | Tổng tài sản thay đổi nhưng không nói vì sao. Wallet còn làm **méo thống kê** vì tỷ giá |
| Có một phần, cho đầu tư | Wealthfolio | Lãi/lỗ tỷ giá chưa thực hiện của danh mục đầu tư |
| Có một phần, chưa rõ | PocketSmith | Brainstorm mục 5.7 ghi "xem thay đổi số dư do tỷ giá theo từng tài khoản". **Tài liệu multi-currency tôi đọc lần này không nhắc đến tính năng này.** Cần dùng thử để xác nhận trước khi đưa vào luận văn |
| **Có đầy đủ, chuẩn kế toán** | **GnuCash** (trading accounts, từ bản 2.3.14) | Mỗi lần đổi tiền, hai vế đi qua `Trading:USD`, `Trading:VND`. Số dư trading accounts **định giá theo tỷ giá hiện tại chính là lãi/lỗ tỷ giá** (đã và chưa thực hiện) |
| **Có đầy đủ, chuẩn kế toán** | **hledger** | Ghi đổi tiền qua `equity:conversion` để lưu lãi/lỗ tích lũy; hoặc dùng `--value`, `--valuechange`, `--gain` để tính thay đổi giá trị và lãi/lỗ chưa thực hiện |
| **Có đầy đủ, chuẩn kế toán** | **Beancount** (+ Fava) | Chỉ thị `price` để định giá lại; bút toán *Conversions* trong bảng cân đối |

**Cơ sở lý thuyết:** Peter Selinger, *Tutorial on multiple currency accounting*. Ý chính: cách "quy hết về một tiền tệ gốc" (cách của mô hình B/C) **phá vỡ phương trình kế toán** khi tỷ giá thay đổi, vì phần lãi/lỗ tỷ giá "không có chỗ để ghi". Trading account giữ một số dư đa tiền tệ như `USD 100 − CAD 120`; khi tỷ giá đổi, giá trị của nó quy ra CAD tự thay đổi, và đó chính là lãi/lỗ tỷ giá. Ví dụ trong bài: tỷ giá 1,20 → 1,30 → 1,15 CAD/USD thì trading account có giá trị 0 → +10 → −5 CAD, trong khi không có giao dịch nào.

### 6.3 Những gì rút ra
- **Công tắc "tiền gốc / quy đổi"** và **tổng theo từng loại tiền** của PocketSmith là mẫu giao diện đáng học, rẻ, hữu ích cho câu hỏi "tôi còn bao nhiêu JPY".
- **Ngân sách:** đề tài chọn "mỗi ngân sách một loại tiền, giao dịch tiền khác quy đổi vào" + phạm vi quốc gia. Đây là lai giữa Toshl và Firefly III, hợp lý. Nên nói rõ trong luận văn là đã xem xét cả hai trường phái và vì sao chọn.
- **Ảnh hưởng tỷ giá:** app phổ thông **chưa có**, phần mềm kế toán **đã có từ lâu** nhưng người thường không dùng được. Đây là khoảng trống thật, nhưng là khoảng trống **về trình bày và khả năng tiếp cận**, không phải về phương pháp tính.

---

## 7. Đối chiếu với đề tài: điều gì được xác nhận, điều gì cần sửa

### 7.1 Được xác nhận (giữ nguyên)

| Thiết kế trong brainstorm | Bằng chứng từ khảo sát |
|---|---|
| Lưu tiền gốc + loại tiền gốc | Mọi app mô hình C, D đều làm |
| Quy đổi thu/chi theo tỷ giá ngày giao dịch, lưu tỷ giá đã dùng | Toshl, Lunch Money, PocketSmith. Ngược lại Wallet, Splitwise, lỗi #12455 của Firefly III cho thấy hậu quả khi làm sai |
| Tổng tài sản theo tỷ giá hiện tại | Tất cả |
| Mỗi ví một loại tiền, ví đa tiền tệ tách ví con | Wallet, PocketSmith, Firefly III |
| Tách `TRANSFER` / `EXCHANGE` khỏi thu/chi | Firefly III, Toshl (ghép cặp), kế toán kép |
| Tự tính phí ẩn so với mid-market | **Không app ghi chép nào làm.** Toshl còn bỏ qua chênh lệch bằng dung sai 5% |
| Dự báo nhu cầu từng loại tiền bằng ML | Không thấy. PocketSmith chỉ dự báo theo lịch |

### 7.2 Cần sửa hoặc làm rõ

**(a) Sửa câu định vị "phân rã biến động tài sản: chưa thấy" ở mục 5.7.** Hội đồng có người biết kế toán sẽ chỉ ra GnuCash trading accounts hoặc hledger `--gain`. Đề xuất viết lại:

> *"Lãi/lỗ tỷ giá là khái niệm đã có trong kế toán kép (Selinger; GnuCash trading accounts; hledger). Tuy nhiên, trong các ứng dụng quản lý chi tiêu cá nhân phổ thông được khảo sát, chưa thấy ứng dụng nào tách biến động tổng tài sản thành phần do dòng tiền và phần do tỷ giá. Hệ thống đưa phép phân rã này vào giao diện dành cho người dùng không có kiến thức kế toán."*

Viết như vậy **mạnh hơn** chứ không yếu đi: có cơ sở lý thuyết để trích dẫn, và công thức của đề tài được kiểm chứng bằng cách so với kết quả của trading accounts trên cùng dữ liệu (một ca unit test rất thuyết phục).

**(b) Công thức phân rã ở 5.3-7 đúng về toán nhưng chưa khớp với cách lưu giao dịch.** Công thức hiện tại định giá dòng tiền theo tỷ giá **đầu kỳ** `r(c,t−1)`, trong khi giao dịch lại được lưu `amount_base` theo tỷ giá **ngày giao dịch**. Hệ quả:
- Cột "thu nhập" và "chi tiêu" trên biểu đồ waterfall (tổng `amount_base`) **sẽ không cộng ra đúng** phần "hiệu ứng dòng tiền" của công thức.
- Một lần đổi tiền trong kỳ sẽ làm thay đổi `B(VND)` và `B(USD)`, nên phần "dòng tiền" bị lẫn cả phí đổi tiền lẫn biến động tỷ giá trong kỳ.

Gợi ý sửa (cần tự kiểm tra lại): tách thành **3 phần** cho khớp với dữ liệu đã lưu:

```
ΔW = Σ amount_base(thu nhập)                       ← theo tỷ giá ngày giao dịch
   − Σ amount_base(chi tiêu, kể cả phí đổi tiền)   ← theo tỷ giá ngày giao dịch
   + hiệu ứng tỷ giá                               ← phần còn lại = ΔW − (thu − chi)
```

Phần còn lại này chính là thứ trading account của Selinger đo. Khi đó waterfall luôn khớp, phí đổi tiền nằm gọn trong "chi tiêu", và "hiệu ứng tỷ giá" có định nghĩa kế toán rõ ràng. Nếu vẫn muốn công thức đóng dạng như hiện tại thì cần nói rõ trong luận văn vì sao chọn tỷ giá đầu kỳ và chấp nhận sai lệch với waterfall.

**(c) Kiểm chứng lại dòng PocketSmith trong bảng 5.7** bằng bản dùng thử (đã có trong mục 11 của brainstorm), vì tài liệu hiện tại không xác nhận.

**(d) Bổ sung vào bảng so sánh chương 2** một dòng cho nhóm kế toán kép (GnuCash / hledger / Beancount) và một dòng cho Wise/Revolut. Hội đồng dễ hỏi "Wise đã hiện phí rồi, làm thêm để làm gì" và câu trả lời là mục 3.2 ở trên.

### 7.3 Ý tưởng nhỏ lấy được từ khảo sát (không bắt buộc)

| Ý tưởng | Lấy từ | Chi phí |
|---|---|---|
| Luật ghép cặp chuyển khoản (±4 ngày, ±5% sau quy đổi) làm **baseline** cho nhãn "Chuyển khoản nội bộ" trong TN1 | Toshl | Thấp, và cho RQ1 thêm một baseline có nguồn gốc |
| Khi ghép cặp xong một cặp khác tiền, **tự tính phí ẩn** của cặp đó | Kết hợp Toshl + mục 5.3-5 | Thấp; biến dung sai 5% mà Toshl bỏ qua thành thông tin |
| Công tắc xem tiền gốc / tiền quy đổi | PocketSmith | Thấp |
| Nhóm ví (Wise gồm nhiều ví con), cờ "không tính vào tổng" | GnuCash, Money Lover | Thấp |
| Vàng như một "loại tiền" | MISA, Toshl, PocketSmith | Thấp nếu nguồn giá vàng ổn |

---

## 8. Hạn chế của khảo sát này

- Chỉ dựa trên tài liệu công khai. Một số trang gốc (Wallet, Money Lover, Lunch Money trang tính năng) **bị chặn khi truy cập tự động**, thông tin về chúng lấy từ đoạn trích kết quả tìm kiếm hoặc bài review, đã đánh dấu *(chưa kiểm chứng)*.
- Nhiều bài so sánh đa tiền tệ trên mạng do **chính đối thủ viết** (Borderless Budget, Tallyroot, Finny, Budgero). Chỉ dùng chúng để tìm manh mối, không trích dẫn làm bằng chứng.
- Các con số phí của Wise/Revolut thay đổi theo thời gian và theo gói; chỉ dùng để minh họa.
- **Nên dùng thử** ít nhất Toshl, PocketSmith, Firefly III (demo), Money Lover, GnuCash (trading accounts) và chụp màn hình cho chương 2.

---

## 9. Nguồn

**Ứng dụng quản lý tài chính**
- Firefly III: [How to use currencies](https://docs.firefly-iii.org/how-to/firefly-iii/features/currencies/), [Manage multiple currencies](https://docs.firefly-iii.org/tutorials/finances/currencies/), [Exchange rates](https://docs.firefly-iii.org/explanation/financial-concepts/exchange-rates/), [Budgets](https://docs.firefly-iii.org/explanation/financial-concepts/budgets/), [Issue #12455: native_amount dùng now()](https://github.com/firefly-iii/firefly-iii/issues/12455), [Issue #3909](https://github.com/firefly-iii/firefly-iii/issues/3909), [Issue #12855](https://github.com/firefly-iii/firefly-iii/issues/12855)
- Toshl: [Currencies](https://toshl.com/currencies/), [Matching transfers between financial accounts](https://toshl.com/blog/matching-transfers-between-financial-accounts/)
- PocketSmith: [Multi-currency features](https://learn.pocketsmith.com/article/122-multi-currency-beta-features-in-pocketsmith), [Multi-currency](https://learn.pocketsmith.com/article/513-multi-currency), [Tour: multi-currency](https://www.pocketsmith.com/tour/multi-currency/)
- Lunch Money: [Knowledge base: Multicurrency](https://support.lunchmoney.app/settings/multicurrency), [Managing accounts](https://support.lunchmoney.app/setup/accounts/managing-accounts)
- Spendee: [How to set/change the currency and exchange rate](https://help.spendee.com/article/231-how-to-setchange-the-currency-and-exchange-rate)
- Wallet (BudgetBakers): [Multiple Currencies & Exchange Rates](https://support.budgetbakers.com/hc/en-us/articles/7149418777746-Multiple-Currencies-Exchange-Rates), [Feedback #81](https://feedback.budgetbakers.com/81)
- Money Lover: [Definition of wallets](https://moneylover.zendesk.com/hc/en-us/articles/34972671048985-Definition-of-wallets-in-MoneyLover)
- Sổ Thu Chi MISA: [Trang chủ](https://sothuchi.misa.vn/)
- Money Manager Ex: [Accounts & Currencies](https://moneymanagerex.org/docs/features/accounts/)
- YNAB: [Using multiple currencies](https://support.ynab.com/en_us/using-multiple-currencies-in-ynab-a-guide-SyBF6PHno)
- Actual Budget: [Multi-Currency docs](https://actualbudget.org/docs/budgeting/multi-currency/), [Issue #3351](https://github.com/actualbudget/actual/issues/3351)
- Monarch Money: [International Accounts and Currency](https://help.monarch.com/hc/en-us/articles/360048393552-International-Accounts-and-Currency)
- TravelSpend: [Can I enter custom rates?](https://help.travel-spend.com/currency-conversion-rates/tRj7gE8u4nhvErytPouJdg/can-i-enter-custom-rates/pzb4mwvbmiU6kwFCcQpU9C)
- Splitwise: [Managing a group with multiple currencies](https://kb.splitwise.com/balances-and-expenses/how-can-i-manage-a-friendship-or-group-with-multiple-currencies)

**Kế toán kép và cơ sở lý thuyết**
- Peter Selinger: [Tutorial on multiple currency accounting](https://www.mathstat.dal.ca/~selinger/accounting/tutorial.html), [Multiple currency accounting in GnuCash](https://www.mathstat.dal.ca/~selinger/accounting/gnucash.html)
- GnuCash: [Chapter 12: Multiple Currencies](https://gnucash.org/docs/v5/C/gnucash-guide/chapter_currency.html), [Trading Accounts (wiki)](https://wiki.gnucash.org/wiki/Trading_Accounts)
- hledger: [Currency conversion](https://hledger.org/currency-conversion.html), [Calculate unrealized gain](https://hledger.org/gain.html)
- Beancount: [Language syntax (price, @, @@)](https://beancount.github.io/docs/beancount_language_syntax/)

**Ngân hàng số**
- Wise: [Pricing](https://wise.com/us/pricing/)
- Revolut: [Fees for card payments in a foreign currency](https://help.revolut.com/en-US/help/card-payments-withdrawals/getting-started-with-card-payments/can-i-pay-in-a-specific-currency/)

**Bài so sánh của bên thứ ba (thiên vị, chỉ tham khảo)**
- [Finny: Best multi-currency expense tracking apps 2026](https://getfinny.app/blog/best-multi-currency-expense-tracking-apps-2026)
- [Tallyroot: Budget software for multiple currencies](https://tallyroot.com/blog/budget-software-multiple-currencies/)
- [Borderless Budget: Actual Budget multi-currency](https://borderlessbudget.com/blog/actual-budget-multi-currency)
