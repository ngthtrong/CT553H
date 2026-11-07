# Nhật ký triển khai

## 07/11/2026 — bổ sung độ bao phủ kiểm tra sau lượt chấm đầu

Lượt đầu kết thúc lúc 17:08 (+08:00), có kết quả utility. Rà mã độc lập phát
hiện phân tích 100 tie seed mới bao phủ ngân sách chính k10 và phân tầng chỉ
có point estimate/denominator. Lượt cuối mở rộng kiểm tie sang cả sáu ngân
sách đã khóa và thêm CI95 mô tả cho phân tầng bằng cùng bootstrap 5.000 lần.

Không thay cohort, nhãn, điểm, recipe, ngân sách, seed, chính sách rank,
estimand, hai contrast chính hoặc quy tắc kết luận. Đây là bổ sung độ bao phủ
triển khai, không phải đổi giả thuyết hoặc lựa chọn sau khi xem kết quả.
Cấu hình khóa giữ nguyên. Bản mã và toàn bộ đầu ra lượt đầu được bảo tồn ở
`local/initial-run/` (không đưa Git); lượt cuối phải kiểm primary contrast
và bảng per-peptide giống lượt đầu trước khi công bố kết quả.
