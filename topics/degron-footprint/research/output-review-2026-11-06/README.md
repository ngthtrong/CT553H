# Rà soát toàn bộ output — 06/11/2026

[ĐO] Rà soát chỉ đọc; không huấn luyện lại, không sửa state/checkpoint.

- Kiểm lại SHA-256 của 76 nguồn chọn lọc trong phân tích OOF.
- Local: 633 complete, 1 source_pending, 1 structure_pending; 456 job được kế thừa và chỉ tính một lần.
- 88 cấu hình có OOF: 47 Kaggle + 41 local. Cùng dữ liệu W, không phải 88 bộ kiểm định độc lập.
- 540 fold ridge, 30 frozen và 30 LoRA; cả 30 LoRA có tensor adapter thay đổi.

## Kiểm kê vật lý

| Nhánh output | File | GiB |
|---|---:|---:|
| `code/302988f37d839f2f` | 30 | 0.000 |
| `local/e18d80b06ac90585` | 18 | 0.000 |
| `local/e7097449883a51d8` | 2,959 | 3.541 |
| `local/ef138c84579c842e` | 2,754 | 2.131 |
| `local/weights` | 63 | 14.110 |
| `official/369cb2fe6a1e31e0` | 2,990 | 2.859 |
| `weights/esm2_35m` | 8 | 0.127 |
| `support-metadata` | 5 | 0.000 |
| `transport-archive` | 1 | 17.542 |

[ĐO] `official.zip` có 8,827 member, 24,446,764,849 byte giải nén. Toàn bộ tên và size khớp cây output hiện có; 8,431 member ≤1 MiB đã kiểm CRC cả bản giải nén và payload ZIP. Không giải nén thêm, không kiểm lại CRC payload lớn; không khẳng định toàn ZIP không hỏng. Đây là bản đóng gói trùng dữ liệu, không phải campaign mới.

File vật lý có thể chứa cache/checkpoint trùng nội dung; không cộng với số artifact đã kiểm hash thành số quan sát khoa học.

## Kết quả và giới hạn

[ĐO] LoRA-B: MAE 0.363669, AUROC+ 0.855047; LoRA-D: 0.364996 / 0.853556. Cả hai tốt hơn frozen cùng runtime/arm; các CI điều chỉnh hậu kiểm cho bốn so sánh không cắt 0.

[DIỄN GIẢI] B và D gần nhau ở trung bình nhưng khác theo WT PSI. Không chọn B chỉ từ hạng MAE; D tốt hơn ở PSI >5. Không thấy xu hướng tăng kích thước pLM luôn tốt hơn.

[ĐO] Brier CV của LoRA giảm nhưng ECE+ tăng so với frozen. Đây là hai khía cạnh khác nhau; không kết luận xác suất đã được hiệu chuẩn tốt trong mọi miền.

[ĐO] W5-D trên T có ΔMAE so với đoán 0 = -0.003256, CI95 [-0.009249, 0.002760]. PSI >5 có MAE 0.442783 so với 0.346964 của đoán 0. Xác suất dương trung bình 0.089529 vượt tỷ lệ thực 0.051155.

[DIỄN GIẢI] AUROC+ tốt không chứng minh độ chính xác hồi quy hay hiệu chuẩn chuyển miền. T chỉ R/A/S, rep1, cùng phòng thí nghiệm và nguồn đã từng thăm dò; LoRA chưa được đánh giá trên T.

## Thời gian và epoch

Thời gian dưới đây là tổng duration ghi ở attempt hoàn tất; một job resume có thể thiếu các attempt trước. Không diễn giải là GPU-active hoặc tổng thời gian người dùng chờ.

| Nhóm | Job | Duration ghi nhận (giờ) |
|---|---:|---:|
| other | 15 | 3.069 |
| probe | 9 | 0.012 |
| extract | 9 | 0.964 |
| ridge | 540 | 1.422 |
| tune-frozen | 30 | 14.068 |
| tune-lora | 30 | 36.007 |

| Cấu hình | Fold | Epoch min / median / max |
|---|---:|---:|
| frozen-B | 15 | 1 / 1 / 3 |
| frozen-D | 15 | 1 / 1 / 3 |
| lora-B | 15 | 1 / 3 / 7 |
| lora-D | 15 | 1 / 2 / 4 |

## Tái tạo và nguồn

Từ gốc repo: `.venv/Scripts/python.exe topics/degron-footprint/research/output-review-2026-11-06/audit.py`.

Chạy `analyze-output.py` / `analyze-local-output.py` ở campaign nếu cần tính lại OOF; audit này tái kiểm hash 76 nguồn và xuất bảng từ các phân tích đã kiểm invariants. Không phải một thư viện metric độc lập.

Số chính xác, toàn bộ 88 cấu hình, seed, strata, CI, lựa chọn nested và nguồn hash: [results.json](results.json).

Chi tiết nền: [Kaggle](../kaggle-roadmap-2026-10-31/output-analysis.md), [Kaggle diagnostics](../kaggle-roadmap-2026-10-31/output-analysis-details.md), [Local](../kaggle-roadmap-2026-10-31/local-output-analysis.md).

Cần làm tiếp: final refit/export/calibrator/card theo kiến trúc, kiểm định nguồn ngoài/cấu trúc có dữ liệu hợp lệ, tích hợp và nghiệm thu phần mềm. Không tự thay model phục vụ từ leaderboard.

## Khôi phục metadata của bản giải nén

[ĐO] Phát hiện 120 JSON nhỏ bị toàn byte 0 trong bản giải nén. Đã lưu bản lỗi ngoài output và khôi phục từ ZIP: 80 artifact khớp SHA-256 trong state; 40 worker-result khớp toàn bộ nội dung job tương ứng trong state. Không sửa state/checkpoint/model và không huấn luyện lại. Bản ZIP là file nén lưu kết quả, không được tính như campaign thêm.

[Nhật ký trước/sau và bằng chứng](metadata-recovery.json), [đối chiếu trước khôi phục](archive-comparison.json), [tái kiểm toàn bộ artifact sau khôi phục](integrity-recheck.json). Tái kiểm mới đạt 4.278 artifact local và 2.986 Kaggle, không mismatch. Không suy đoán nguyên nhân các byte 0.
