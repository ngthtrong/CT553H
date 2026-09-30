# RQ2: baseline "nhớ lại" và thí nghiệm nhỏ về phản hồi thiếu (bản thô)

> Ngày chạy: 29/09/2026 · Trạng thái: **bản thô**, mô tả danh mục vẫn là bản nháp của Claude ([categories.json](../rq1-kiem-tra-nhanh/categories.json))

## Mục đích

1. Đặt **mốc bắt buộc** cho RQ2: mọi chiến lược thích nghi phải được so với việc chỉ nhớ lại nhãn cũ.
2. Chạy thử **thí nghiệm nhỏ về phản hồi thiếu (TN5)**: người dùng không phải lúc nào cũng sửa khi hệ thống gợi ý sai.

## Cách làm

- Phát lại 5.028 khoản chi có nhãn theo thứ tự ngày, kiểm tra trước rồi học sau. Tính điểm trên 4.525 giao dịch; tập dev của RQ1 vẫn được phát lại nhưng không tính điểm.
- Danh mục được "tạo" vào ngày nó được dùng lần đầu. Zero-shot chỉ chọn trong những danh mục đã tồn tại tới thời điểm đó.
- **B0, nhớ lại:** ghi chú đã gặp thì lấy nhãn lần gần nhất; ghi chú chưa gặp thì không gợi ý, người dùng tự chọn.
- **B1, nhớ lại + zero-shot:** giống B0, nhưng ghi chú chưa gặp được gợi ý bằng embedding zero-shot (bge-m3, tên + mô tả).
- Hai cách chuẩn hóa ghi chú: `key` (chữ thường, gộp khoảng trắng) và `key_noacc` (bỏ thêm dấu tiếng Việt).
- **Phản hồi thiếu:** khi gợi ý sai, người dùng sửa với xác suất p ∈ {1,0; 0,9; 0,7; 0,5}. Nếu không sửa, nhãn sai được lưu vào bộ nhớ. Mỗi mức p chạy 5 seed.
- "Số lần thao tác tay mỗi tháng" gồm số lần gợi ý sai cộng số lần không có gợi ý.

Chạy lại: `.venv/bin/python ml/experiments/rq2-baseline-nho-lai/run.py`. Embedding được cache ở `data/interim/` (không lên git).

## Kết quả, phản hồi đầy đủ ([results/summary.csv](results/summary.csv))

| | B0 nhớ lại | B1 nhớ lại + ZS |
|---|---:|---:|
| Tỷ lệ ghi chú đã gặp | 60,7% | 60,7% |
| Accuracy toàn luồng | 56,9% | **71,5%** |
| Accuracy trên ghi chú đã gặp | 93,8% | 93,8% |
| Accuracy trên ghi chú **chưa gặp** | 0% (không gợi ý) | **37,0%** |
| Accuracy 30 ngày đầu | 17,2% | 49,1% |
| Thao tác tay / tháng | 39,8 | 26,3 |
| … trong đó do ghi chú chưa gặp | 36,3 | **22,9 (87%)** |

Bỏ dấu khi so khớp chỉ giúp thêm khoảng 0,7–0,9 điểm (B1 đạt 72,2%).

## Kết quả, phản hồi thiếu (B1, `key`, trung bình 5 seed)

| Xác suất sửa p | 1,0 | 0,9 | 0,7 | 0,5 |
|---|---:|---:|---:|---:|
| Accuracy | 71,5% | 71,1% | 70,1% | 68,7% |
| Accuracy trên ghi chú đã gặp | 93,8% | 93,1% | 91,5% | 89,2% |
| Thao tác tay / tháng | 26,3 | 26,7 | 27,6 | 28,9 |

## Nhận xét

1. **Nhớ lại gần như đã giải xong phần ghi chú lặp lại** (93,8%). Bất kỳ chiến lược nào cũng không còn nhiều chỗ để cải thiện trên 61% luồng này.
2. **Chỗ cần nghiên cứu là ghi chú chưa gặp:** chúng chiếm 39% luồng nhưng gây ra 87% số lần phải thao tác tay, và accuracy trên nhóm này chỉ 37%. Đây là căn cứ để đặt lại RQ2.
3. **Phản hồi thiếu làm bộ nhớ bị "nhiễm" nhãn sai:** khi chỉ sửa 50% số lần sai, accuracy trên ghi chú đã gặp giảm 4,6 điểm, vì nhãn sai được nhớ lại và lặp lại. Accuracy trên ghi chú chưa gặp không đổi, vì zero-shot không học từ bộ nhớ. Các chiến lược học từ phản hồi ở RQ2 (kNN, huấn luyện lại) sẽ bị ảnh hưởng mạnh hơn, và TN5 sẽ đo điều đó.
4. Accuracy theo tháng giảm trong năm 2026, xuống khoảng 60–68% ([results/monthly_accuracy.csv](results/monthly_accuracy.csv)), vì có nhiều ghi chú mới hơn. Đây là dấu hiệu dữ liệu thay đổi theo thời gian.

## Hạn chế

- Mô tả danh mục là bản nháp có nguy cơ rò rỉ (xem RQ1).
- Mô hình phản hồi thiếu quá đơn giản: mỗi lần sai được sửa độc lập với cùng xác suất. Thực tế, xác suất sửa có thể phụ thuộc vào độ tự tin của gợi ý và vào tải nhận thức của người dùng (Parasuraman & Manzey, 2010).
