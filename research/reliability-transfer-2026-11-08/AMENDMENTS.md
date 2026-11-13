# Nhật ký triển khai và kiểm số học

## 08/11/2026 — thống nhất precision của ensemble trước lần xác nhận cuối

Lượt phân tích đầu đã chạy CPU. Validator trực tiếp từ OOF phát hiện chênh
khoảng 1e-10 ở MAE subset: một phép lấy trung bình giữ float32, phép khác dùng
reduction float32 theo thứ tự khác. Đã truy tới dtype của prediction gốc,
không phải mismatch cell, nhãn, split hoặc số candidate.

Runner và phép tái tính độc lập được thống nhất **cast prediction lưu sẵn sang
float64 trước khi ensemble**, như input adapter của replay 07/11. Ghi chênh
max với native groupby mean trong `results.json.numerical_precision`.
Đối chiếu MAE/CI cũ dùng tolerance 2e-8 phù hợp input float32; phép tái tính
độc lập của các bảng mới vẫn dùng 1e-10. Không sửa số, manifest, nhãn hay
checkpoint lịch sử. Các input gốc vẫn được kiểm SHA trước/sau.

Đồng thời hoàn thiện đầu ra contrast paired cho **toàn bộ** grid threshold,
hai hướng, bốn target nhãn và các matched baseline đã định trong protocol;
không chọn target/ngưỡng tốt nhất. Bổ sung null reason cho event metric không
đủ lớp, contrast từng seed và kiểm consensus CI độc lập. Đây là hoàn thiện
độ bao phủ kiểm chứng; các CI mới vẫn mô tả hậu kiểm, không tiền đăng ký mới.

Protocol/config khóa trước lượt đầu giữ nguyên. Lượt đầu chưa được validator
xác nhận và không được công bố là kết quả cuối. Không có GPU hoặc train mới.
