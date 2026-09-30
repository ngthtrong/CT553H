# RQ1, kiểm tra nhanh (bản thô): embedding zero-shot

> Ngày chạy: 29/09/2026 · Trạng thái: **bản thô, không dùng làm kết quả chính thức**

## Mục đích

Có một con số khởi điểm để mang tới buổi gặp GVHD: khi người dùng vừa tạo danh mục mà chưa có giao dịch nào, cách đơn giản nhất (không LLM, không dữ liệu tổng hợp) đạt đến đâu.

## Cách làm

- Tập dev: mẫu ngẫu nhiên 10% khoản chi có nhãn (503 giao dịch, seed 42), id ở [results/dev_ids.csv](results/dev_ids.csv).
- Mỗi ghi chú được gán vào danh mục có embedding gần nhất (cosine) với embedding của tên, hoặc tên + mô tả, danh mục. Không học gì từ dữ liệu thật.
- Mô hình: `multilingual-e5-small`, `multilingual-e5-base`, `bge-m3`, chạy CPU.
- Macro-F1 tính trên 19 danh mục có mặt trong dev, dù mô hình chọn trong cả 25.
- "Hay gặp" là ghi chú xuất hiện ít nhất 5 lần trong toàn bộ khoản chi (288/503 mẫu dev).

Chạy lại: `.venv/bin/python ml/personal-expense-management/experiments/rq1-quick-check/run.py` (từ thư mục gốc, cần `pip install -r ml/requirements.txt`).

## Kết quả ([results/summary.csv](results/summary.csv))

| Phương pháp | Biến thể | Accuracy | Macro-F1 | Top-3 |
|---|---|---:|---:|---:|
| Ngẫu nhiên | 1/25 | 2,6% | 1,6% | |
| Luôn đoán AC* | | 32,8% | 2,6% | |
| Khớp tên danh mục* | | 34,0% | 8,5% | |
| e5-small | chỉ tên | 16,9% | 19,5% | 23,3% |
| e5-small | tên + mô tả | 42,9% | **38,2%** | 64,2% |
| e5-base | tên + mô tả | 40,0% | 31,7% | 63,8% |
| bge-m3 | chỉ tên | 17,9% | 11,5% | 24,3% |
| bge-m3 | tên + mô tả | **50,1%** | 36,0% | 64,0% |

\* Cả hai baseline này đều dựa vào việc biết AC là nhãn phổ biến nhất (khớp tên không được thì đoán AC). Người dùng mới không có thông tin này.

## Nhận xét

1. **Chỉ có tên thì gần như vô dụng** (16–18%), thua cả việc luôn đoán AC. Tên viết tắt như AC, DC, AV, RL không mang nghĩa với mô hình.
2. **Thêm một câu mô tả thì accuracy tăng khoảng 2,5 lần** (lên 40–50%), và **top-3 đạt khoảng 64%**. Với giao diện gợi ý 3 danh mục, cứ 3 lần nhập thì khoảng 2 lần đã có đáp án đúng trong gợi ý.
3. **Danh mục lớn nhất lại yếu nhất:** AC (33% dữ liệu) chỉ đạt F1 0,28 với bge-m3, vì ranh giới giữa "ăn chính" và "ăn vặt" (AV) rất mờ đối với embedding. RL và Ngu đạt 0: đây là các danh mục theo ngữ cảnh (đi cùng ai, cảm xúc), không đọc được từ ghi chú.
4. Danh mục tên rõ nghĩa hoặc mô tả sát hành vi thì tốt: DC 0,95, Badmintion 0,93, Coffee 0,76, Study 0,71.
5. Kết quả nằm trong khoảng 40–85% mà kế hoạch đặt ra, nên **RQ2 (thích nghi theo phản hồi) còn nhiều chỗ để cải thiện**. Embedding zero-shot thường yếu hơn LLM zero-shot và mô hình học trên dữ liệu tổng hợp, nên đây là **cận dưới** của RQ1.

## Hạn chế của lần chạy này

- **Mô tả danh mục do Claude viết nháp sau khi đã xem dữ liệu** ([categories.json](categories.json)), nên có nguy cơ rò rỉ. Ví dụ mô tả DC có chữ "xăng", mà "xăng" chiếm phần lớn nhãn DC. Người làm đề tài cần tự viết lại mô tả, khóa và commit trước khi chạy thí nghiệm chính thức.
- Một lần chia dev duy nhất, chưa có khoảng tin cậy.
- Chưa có LLM zero-shot và dữ liệu tổng hợp, là hai phương pháp chính của RQ1.
