# Từ score tới xác suất và miền được phép dùng

## Ba câu hỏi khác nhau

1. **Effect regression:** mutation làm PSI đổi bao nhiêu?
2. **Event probability:** xác suất xảy ra ΔPSI ≥ 1 trong population xác định là bao nhiêu?
3. **Domain membership:** peptide có thuộc miền mà mô hình được đánh giá phù hợp không?

Ba đầu ra không thay nhau. Score ΔPSI=0,8 không phải xác suất 80%; xác suất sự kiện lớn cũng không đảm bảo peptide nằm trong miền đã kiểm chứng.

## Calibration làm gì?

**Calibration/hiệu chuẩn xác suất** kiểm việc nhóm các dự đoán xác suất gần p có thực sự xảy ra sự kiện với tần suất gần p không. Ví dụ tự đặt: trong 100 mutation được gán khoảng 0,7, kỳ vọng khoảng 70 ô dương nếu xác suất khớp tần suất ở population đó.

**Platt scaling** fit một logistic map $p=1/(1+e^{-(as+b)})$ từ score s. **Isotonic regression** học một hàm đơn điệu linh hoạt hơn. Cả hai phải học trên dữ liệu được phép; không fit rồi chấm trên cùng nhãn test. **Cross-fitting** tạo score ngoài mẫu trong train để fit bước hiệu chuẩn, còn outer-test vẫn được giữ riêng. [NC-08]

**Brier score** là trung bình $(p-y)^2$ cho y nhị phân; thấp hơn tốt hơn. **ECE** chia xác suất thành bin rồi gộp độ lệch giữa xác suất trung bình và tần suất thật; kết quả phụ thuộc cách chia bin. **Reliability diagram** trực quan hóa sự khớp đó. Đường chéo là mốc khớp lý tưởng, không phải đường AUROC.

![Hiệu chuẩn baseline lịch sử. Hình bên trái là reliability theo các bin đã lưu; hình bên phải so Brier với xác suất nền. Không dùng đây làm calibration của CNN full-PSI.](assets/figures/calibration.pdf){width=96%}

Ở P6 lịch sử, cắt score thô vào [0,1] có Brier khoảng 0,1272; dự đoán hằng theo tỉ lệ dương nền có Brier khoảng 0,1139; Platt khoảng 0,0925. ECE của Platt khoảng 0,0163, gần ECE hằng khoảng 0,0154. Một model hằng có ECE nhỏ vẫn không phân biệt được mutation: cần đọc đồng thời phân biệt, calibration và baseline. [NC-08]

::: {.limit title="Phạm vi của kết quả xác suất"}
P6 thuộc baseline và cohort lịch sử. Tỉ lệ dương, PSI và pipeline đã thay đổi trong full-PSI; không chuyển nguyên calibrator rồi tuyên bố xác suất CNN/LoRA đã được kiểm chứng. Hiệu chuẩn full-PSI và artifact cuối vẫn là việc cần hoàn tất theo protocol.
:::

## Domain gate giải quyết một rủi ro khác

**Domain shift** là dữ liệu sử dụng khác phân bố dữ liệu mà mô hình đã được đánh giá: assay, miền PSI, protein, trình tự hoặc điều kiện sinh học có thể khác. **Gate/cổng miền** có thể trả `in`, `borderline`, `out` hoặc `unknown`, thay vì ép mọi đầu vào thành dự đoán chắc chắn.

R3 thử hai nhánh: tra PSI đã đo khi có dữ liệu và ước lượng từ trình tự khi không có. PSI của màn sàng nguồn không được thay trực tiếp cho PSI saturation: có độ lệch thang đo, khoảng 0,88 điểm trong audit. Ngưỡng số giống nhau trên hai assay không đồng nghĩa cùng miền. [NC-13]

Thiết kế R3 dùng P_in=0,8 và P_out=0,5 để tạo vùng cần thận trọng. Đây là xác suất thuộc miền theo mô hình cổng; không phải xác suất mutation gây bệnh hoặc độ tin cậy cho từng ô. Cần ghi lý do `unknown` khi thiếu nguồn, không gán 0 như thể đã đo. [NC-13]

![Hai đường độc lập: dự đoán hiệu ứng/hiệu chuẩn và kiểm miền. Hộp vàng là hướng tích hợp cần hoàn tất; sơ đồ không xác nhận app hiện đã có đầy đủ hai đường.](assets/diagrams/calibration-and-domain.pdf){width=95%}

## Kết quả nghiên cứu chưa bằng tích hợp sản phẩm

R3 có artifact và phân tích riêng; app baseline hiện chưa tích hợp đúng cổng này. Đường tra screen PSI thô và bộ nạp gate chưa đủ để coi chức năng đã hoàn thành. Cần đồng bộ input, model card, lý do trạng thái miền và test qua backend thật trước khi mô tả là chức năng đã nghiệm thu. [PM-01; NC-13]

**Model card** là bản mô tả phiên bản model, dữ liệu, cách chia, mục đích, giới hạn, metric và điều kiện dùng. Người đọc cần biết probability từ model/calibrator nào, gate dựa vào dữ liệu nào. Dùng hai số từ hai artifact không khớp phiên bản có thể tạo một kết quả nhìn hợp lý nhưng sai provenance.

::: {.exercise title="Tự kiểm 13"}
1. Score 0,8 khác xác suất 0,8 thế nào?
2. Tại sao phải có baseline xác suất hằng khi đọc Brier/ECE?
3. Gate `in` có bảo đảm một mutation cụ thể được dự đoán đúng không?
4. Vì sao chưa thể dùng kết quả P6 để khẳng định xác suất của mọi mô hình full-PSI đã tốt?
:::
