# Tiền đăng ký — đường cong học theo cụm (P1) và nới ngưỡng degron (P0)

Chốt **trước khi chạy**, ngày 22/10/2026. Kế hoạch gốc: [next-steps-plan-2026-10-22](../next-steps-plan-2026-10-22/README.md) §2. Sau khi chạy, README chỉ **báo kết quả**, không sửa tiêu chí ở file này.

## 1. Hai câu hỏi

- **P1.** Ở bộ bão hòa hiện tại, AUROC có còn tăng theo số **cụm protein** huấn luyện không? Tức nút thắt mà [G2 mở rộng §3b](../g2-extension-2026-10-18/README.md) *diễn giải* là lượng nhãn có được một phép đo trực tiếp xác nhận hay không.
- **P0.** 144 peptide bị loại chỉ bởi ngưỡng `DEGRON_PSI_MAX = 3,0` ([phép đếm](../next-steps-plan-2026-10-22/sat-filter-dropoff.json)) có dùng được làm **nhãn huấn luyện thêm** không, khi miền đánh giá giữ nguyên?

## 2. Bất biến, giữ nguyên từ G2 để số liệu so được

- Nhãn: ΔPSI trung bình hai nửa `sat_a`/`sat_b`; ô dương khi ΔPSI ≥ `RESCUE_DELTA` = 1,0.
- Chỉ số: **AUROC mức ô, macro theo peptide**, chỉ tính trên peptide đủ hai lớp.
- Đặc trưng: **M3 180 chiều** (`pair` 40 + `comp` 20 + `ctx` ±3 có thứ tự 120), đúng `derisk.featurize`.
- Seed huấn luyện **17, 29, 43**. Bootstrap **5.000 lần theo cụm protein**, giữ mọi peptide của cụm được lấy mẫu.
- Mọi chọn siêu tham số chỉ trên inner validation **chia theo cụm** trong phần huấn luyện; không bao giờ xem outer-test.

## 3. Phép chia — điều kiện để so được với 0,8082

`[ĐỀ XUẤT]` Yêu cầu bắt buộc: **outer-test phải là đúng những ô của bộ 91 peptide** như benchmark G2, ở cả P1 và P0.

- 5 outer fold lấy bằng `GroupKFold(5)` trên **bộ 91 peptide gốc** theo cụm cov80 — đúng lệnh G2 đã chạy.
- **Cổng tự kiểm:** danh sách cụm test của 5 fold phải **trùng khớp** `folds` trong [results.json](../g2-saturation-2026-10-18/results.json) của G2. Không trùng → dừng, không báo kết quả.
- Peptide nới ngưỡng (P0) **chỉ vào outer-train**. Peptide nào thuộc cụm test của fold nào thì bị loại khỏi train của **đúng fold đó**; số bị loại từng fold phải được báo.
- Đường cong (P1) lấy **tập con lồng nhau theo cụm**: trộn thứ tự cụm của outer-train bằng seed, lấy tiền tố 25/50/75/100%. Lồng nhau nghĩa là tập 25% ⊂ 50% ⊂ 75% ⊂ 100% trong cùng seed và cùng fold.

## 4. Mô hình, chốt trước

Hai mô hình, không thêm:

- **ridge M3** — mô hình chính. Alpha chọn trong {1, 10, 100, 1000} bằng MSE trên inner validation, rồi khớp lại trên toàn bộ phần huấn luyện của mức đó.
- **`gate_no_pap`** — mô hình phụ, đúng class `Gate(gated=True, pap=False)` của [runner G2](../g2-saturation-2026-10-18/run.py), đúng lịch học (AdamW lr 0,002, weight decay 0,01, batch 1024, tối đa 60 epoch, patience 8). Chọn vì nó là ứng viên mạng tốt nhất của G2 (0,8015) **và** không cần nhánh ΔPAP, nên không phải tính lại PAP cho peptide mới.

`[ĐỀ XUẤT]` Lý do dùng hai mô hình khác sức chứa: nếu đường cong của ridge phẳng mà đường cong của mạng dốc, thì kết luận "thiếu nhãn" có nghĩa khác với khi cả hai đều phẳng. Một mô hình không phân biệt được hai tình huống đó.

**Không** tính ΔPAP cho peptide mới trong thí nghiệm này; mốc ΔPAP 0,7693 chỉ được **dẫn lại** từ G2 trên đúng bộ 91 peptide, không tính lại.

## 5. Tiêu chí kết luận, chốt trước

**P1 — đường cong học.** Gọi A(m) là AUROC macro của điểm OOF gộp ba seed ở mức m.

- **Hỗ trợ giả thuyết thiếu nhãn** khi *cả hai*: (a) CI95 ghép cặp theo cụm của A(100%) − A(50%) **nằm hoàn toàn > 0**; (b) dãy A(25%) ≤ A(50%) ≤ A(75%) ≤ A(100%) **tăng đơn điệu không giảm**.
- (a) đạt mà (b) không đạt → ghi "**hỗ trợ một phần**", nêu rõ chỗ không đơn điệu.
- (a) không đạt → ghi "**chưa đủ bằng chứng cho giả thuyết thiếu nhãn**". **Không** được diễn giải thành "đã chạm trần dữ liệu": thiết kế này không đo trần.

**P0 — nới ngưỡng.** Gọi A(ext) là AUROC trên cùng outer-test khi thêm peptide nới ngưỡng vào train.

- **Nhận** khi *cả hai*: (a) CI95 ghép cặp của A(ext) − A(100%) **> 0**; (b) delta **dương ở cả ba seed** tính riêng.
- Chỉ (a) đạt → "lợi ích chưa bền qua seed", không đưa vào cấu hình chính.
- (a) không đạt → kết luận âm: "nới miền degron không thêm tín hiệu học được ở thiết kế này"; giữ ngưỡng 3,0 làm cấu hình chính.

**Bắt buộc báo kèm, dù kết quả thế nào:** số peptide và số **cụm cov80 mới** mà P0 thêm vào; tỉ lệ ô dương (ΔPSI ≥ 1) của nhóm mới so với nhóm 91 peptide; phân bố ΔPSI và PSI(WT) của nhóm mới; số peptide mới bị loại từng fold do trùng cụm test.

## 6. Dự đoán đã ghi trước khi chạy

`[ĐỀ XUẤT]` Ghi để sau không đọc ngược kết quả thành điều đã biết:

1. **P1 có khả năng cao hỗ trợ**: ridge thắng mọi mô hình sức chứa lớn ở n = 89 cụm là dấu hiệu chế độ thiếu dữ liệu.
2. **P0 có khả năng cao thất bại, vì một lý do cụ thể**: peptide có PSI(WT) cao đã bền, nên "ô dương = ΔPSI ≥ 1 = reporter bền thêm" gần như không có chỗ để xảy ra — khả năng bị chặn trên. Nếu tỉ lệ ô dương của nhóm mới thấp hẳn so với nhóm 91, thì P0 thất bại vì **đổi nghĩa nhãn**, không phải vì "thêm nhãn không giúp". Hai cách đọc này phải được phân biệt trong README.
3. Nếu P1 hỗ trợ **và** P0 thất bại, kết luận ghép là: thiếu nhãn đúng là nút thắt, nhưng **không** tháo được bằng cách nới định nghĩa degron — phải tìm nhãn cùng hệ đo từ nguồn khác ([dataset-search §2](../next-steps-plan-2026-10-22/dataset-search.md)).

## 7. Việc không làm

- Không thêm mô hình thứ ba, không thử biến thể lớp mạng mới.
- Không đổi ngưỡng `RESCUE_DELTA`, không đổi chỉ số, không đổi cov80 sang cov50 cho kết quả chính.
- Không chạy lại với ngưỡng degron khác 4,0 rồi chọn số thuận lợi. Ngưỡng P0 **chốt ở 4,0** (thêm 85 peptide). Mức 3,5/4,5/5,0 chỉ được chạy nếu báo **toàn bộ** cùng lúc như phân tích độ nhạy, có nhãn rõ.
- Không sửa đề cương, slide, hay trạng thái G2/G3 trong phiên này.
