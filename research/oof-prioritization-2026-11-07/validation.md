## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-11-07
- Verification Status: VERIFIED trong phạm vi kiểm số học trực tiếp; CAUTION về suy rộng khoa học
- Version Label: oof_priority_validation_v1

# Kiểm chứng và giới hạn

Input audit, scorer edge cases và kiểm độc lập primary/CI đều PASS, xem
[input-manifest.json](input-manifest.json), [validation.json](validation.json)
và [independent-validation.json](independent-validation.json).
Lượt đầu và lượt cuối giữ nguyên bảng per-peptide, summary và hai primary
contrast (bản đầu được lưu local); chỉ mở rộng độ bao phủ tie/CI phân tầng.
Các kiểm này không chứng nhận pipeline huấn luyện từ đầu hoặc wet lab.

Hai contrast chính dùng CI97,5 Bonferroni; không tính p-value mới hoặc
gán mức hiệu quả thực tiễn chưa được đối tác wet lab định nghĩa. Tất cả
secondary contrast/CI và phân tầng là mô tả trên development.

## Fallacy scan — 11/11 loại được xét trong phạm vi báo cáo

| Loại | Trạng thái | Quan sát/giới hạn |
| --- | --- | --- |
| Simpson | NOTE | Đối chiếu PSI và fold: không quan sát đảo dấu so W5; mức lợi ích không đồng nhất. Không kết luận cho các phân tầng chưa xét. |
| Ecological fallacy | NOTE | Estimand peptide-macro; không suy mọi mutation/protein đều tốt hơn. |
| Berkson / selection | CAUTION | W là cohort đã chọn/QC, không phải mọi peptide tự nhiên; không tái lập QC hay khảo sát missingness nguồn. |
| Collider bias | NOTE | Primary không điều kiện thêm vào nhãn; phân tầng số hit là mô tả hậu kiểm, không suy quan hệ nhân quả. |
| Base rate neglect | NOTE | Random là prevalence theo peptide; no-hit giữ trong Precision; denominator Recall khác được công bố. |
| Regression to mean | NOTE | Không có pre/post trên nhóm cực trị; không suy cải thiện thực nghiệm từ replay. |
| Survivorship | NOTE | Giữ toàn bộ 235 peptide, cả 37 không hit dương và 84 không hit âm; nguồn sau QC vẫn có giới hạn chọn mẫu. |
| Look elsewhere | CAUTION | Hiệu chỉnh hai contrast chính; toàn bộ ngân sách/hướng/recipe phụ được báo, CI phụ chỉ mô tả. |
| Forking paths | CAUTION | Khóa config trước utility nhưng dữ liệu/model development đã được xem; amendment được giữ, không phải preregistration. |
| Correlation / causation | CAUTION | Không diễn giải ưu thế replay thành tác động nhân quả lên wet lab hoặc tiết kiệm thực tế. |
| Reverse causality | NOTE | Prediction OOF được lưu trước replay; không đặt kết luận cơ chế nhân quả hay clinical từ điểm dự đoán. |

## Kiểm artifact

- Figure đã được mở kiểm trực quan: hai hướng, trục log, label/legend/dải CI
  hiện đầy đủ; CSV tách conditional random band khỏi cluster CI.
- README giữ denominator và kết quả không thuận lợi/không phân giải.
- Không có train/refit/inference mới, `.pt`/pickle load, nguồn ngoài mới,
  model phục vụ mới, hoặc dữ liệu gửi tới dịch vụ mô hình ngoài.
- Nguồn raw/campaign/output phân tích cũ được đối chiếu hash; không sửa manifest
  để ép identity. Không có commit hoặc push.
