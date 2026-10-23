# Tiền đăng ký — trộn nhãn bộ quét vào huấn luyện trên bộ bão hòa (phần B)

Chốt **trước khi chạy** [run_merge.py](run_merge.py), 23/10/2026. Phần A ([audit_labels.py](audit_labels.py), chỉ đọc) đã chạy trước và **được phép ảnh hưởng thiết kế dưới đây** (mục 2); phần B chưa chạy. Sau khi chạy, README chỉ báo kết quả, không sửa tiêu chí ở file này.

## 1. Câu hỏi

Thêm nhãn **bộ quét** (Zhang 2023, đột biến 1 acid amin/vị trí, ≈ 2.994–4.809 peptide) vào huấn luyện có làm tăng AUROC trên **đúng outer-test của G2** (91 peptide / 89 cụm / 47.847 ô) so với chỉ học bão hòa không? Và nếu có, cách trộn nào?

## 2. Điều phần A buộc thiết kế phải tính đến `[ĐO]`

Từ [audit-labels.json](audit-labels.json), 117 peptide chung hai bộ, 3.228 ô là **cùng một đột biến đo hai lần**:

- Tương quan quét-rep1 ↔ bão hòa: Pearson **0,70–0,72**, kappa nhị phân 0,65, AUROC (nhãn quét dự đoán nhãn bão hòa) 0,90. Trần trong từng bộ: Pearson 0,82 (quét rep1↔rep2) và 0,85 (bão hòa nửa A↔B). Tức hai bộ **cùng tín hiệu nhưng đồng thuận từng ô thấp hơn trần**; mốc WT (một phép đo `mut0` so với trung vị ô đồng nghĩa) lệch > 0,5 PSI ở 31% peptide. *(Bản gốc của dòng này viết "không cùng thang" và dẫn độ dốc OLS 0,70–0,73; đó là diễn giải sai — SD hai bộ gần bằng nhau, độ dốc chỉ là r · SD_y/SD_x. Sửa 23/10 sau khi chạy, chỉ sửa lời diễn giải, không đổi tiêu chí hay thiết kế.)*
- Điều kiện quét "BAG6 WT" lệch **−1,13 PSI** so với bão hòa → **không dùng**, đúng D-028.
- Thiết kế thay thế của bộ quét là **ánh xạ tất định** WT→đột biến: 10 loại WT → R, 6 → A, 4 → S; chỉ **20/380** cặp (WT, đột biến). Nên bộ quét không dạy gì về ma trận thay thế ngoài 20 cặp đó.

Hệ quả thiết kế: trộn mù (S1) có nguy cơ hại; cần **nhận diện nguồn** (S2) hoặc dùng làm **tiên nghiệm** (S3, N2); và phải có arm tách "peptide mới" khỏi "đo lại cùng đột biến" (S2d).

## 3. Bất biến (giữ từ P0/P1 để so được)

- Outer-test = đúng ô bộ 91 peptide; 5 fold `GroupKFold(5)` theo cụm cov80; **cổng tự kiểm**: cụm test của 5 fold phải trùng `folds` trong [results.json của G2](../g2-saturation-2026-10-18/results.json), không trùng → dừng.
- Nhãn bão hòa: ΔPSI trung bình hai nửa. Nhãn quét: ΔPSI = PSI(mutant) − PSI(`mut0`) của **replicate 1**, reads ≥ 10 (đúng `residue_data.build_scanning`). Không dùng điều kiện BAG6 WT.
- Chỉ số: AUROC mức ô macro theo peptide (ô dương ΔPSI ≥ 1,0). Bootstrap 5.000 lần theo cụm, ghép cặp. Seed 17/29/43. Đặc trưng M3 180 chiều.
- Phần bão hòa của huấn luyện = cấu hình P0 (`ext4.0`: 176 peptide, peptide thêm chỉ vào outer-train). Nên mốc so chính là **A1 = ridge `ext4.0` = 0,8208**, không phải 0,8082.
- Ngưỡng degron của bộ quét: **chính 4,0** (khớp A1); 3,0 chạy như độ nhạy, báo đủ.
- **Chống rò rỉ, chốt trước:** ở mỗi fold, mọi peptide quét có cụm cov80 thuộc cụm test của fold đó bị loại. **Ở bước chọn siêu tham số** (inner), peptide quét thuộc cụm của tập validation cũng bị loại — nếu không, validation thưởng cho độ trùng cụm mà test thật không có và kéo trọng số quét lên cao. Khi khớp lại cuối cùng (train+val) chỉ loại cụm test.

## 4. Các arm

Mô hình chính **ridge M3**, mô hình phụ `gate_no_pap` (đúng class và lịch của run_curve). Không thêm mô hình khác, không PLM/mCNN trong phiên này.

| Arm | Mô tả | Siêu tham số chọn trên inner validation (MSE, hàng bão hòa) |
|---|---|---|
| **A1** | chỉ bão hòa `ext4.0` | α ∈ {1,10,100,1000} |
| A0 | chỉ bão hòa 91 peptide (cổng tái lập 0,8082) | α |
| S0 | chỉ quét, dự đoán bão hòa (tham chiếu) | α |
| S1 | gộp hàng quét + bão hòa, **không** nhận diện nguồn, trọng số hàng quét w | α, w ∈ {0,05; 0,2; 1} |
| **S2 (CHÍNH)** | gộp, đặc trưng `[X, X·1{quét}]` (khối chung + khối riêng nguồn quét), hàng test bão hòa dùng khối chung | α, w |
| S2d | như S2 nhưng chỉ giữ peptide quét có cụm **không** nằm trong bất kỳ cụm bão hòa `ext4.0` nào | α, w |
| S3 | tiên nghiệm: khớp ridge trên quét → w₀; ridge bão hòa trên phần dư `y − X·w₀` (tương đương phạt `‖w − w₀‖²`) | α quét theo holdout cụm quét; α bão hòa |
| N1 | `gate_no_pap` khởi tạo ngẫu nhiên, `ext4.0` (mốc mạng) | epoch (early stop) |
| N2 | `gate_no_pap` tiền huấn luyện trên hàng quét (early stop theo holdout cụm quét) rồi tinh chỉnh `ext4.0`, **lr = 2e-3 (chính)**; lr = 5e-4 báo kèm, không chọn sau | epoch |

## 5. Tiêu chí kết luận, chốt trước

- **Chính:** S2 − A1 (ridge, ngưỡng quét 4,0). **Nhận "nhãn quét thêm giá trị cho ridge"** khi *cả hai*: CI95 ghép cặp theo cụm **> 0** và delta **dương ở cả ba seed**. Chỉ CI > 0 → "chưa bền qua seed". Không đạt → "không có bằng chứng quét giúp ridge ở thiết kế này".
- **Hại của trộn mù:** nếu S1 − A1 có CI95 **hoàn toàn < 0** thì ghi "trộn mù làm hại" (đây là câu trả lời trực tiếp cho "có trộn thẳng được không").
- **Phụ (mạng):** N2 − N1 theo cùng luật nhận (CI > 0 và ba seed dương). Nếu N2 đạt mà S2 không → "quét chỉ giúp mô hình sức chứa lớn"; nếu cả hai không → hướng trộn quét đóng lại ở mức nhãn ΔPSI.
- S1, S2d, S3, độ nhạy ngưỡng 3,0, S2 − A0: **thăm dò**, báo đủ, không dùng để thay kết luận chính.
- MDE tham chiếu từ [derisk](../residue-task-derisk-2026-10-15/README.md): 0,0123 ở 89 cụm. Delta nhỏ hơn mức này không được đọc là "có lợi" dù CI hẹp.
- **Chẩn đoán bắt buộc báo:** (i) trọng số w và α được chọn từng fold/seed; (ii) số peptide quét bị loại từng fold; (iii) delta S2 − A1 tách theo ô test thuộc 20 cặp (WT, đột biến) của bộ quét vs ô còn lại (AUROC macro trên peptide có ≥ 3 ô mỗi lớp trong nhóm con, kèm số peptide đủ điều kiện).

## 6. Dự đoán ghi trước khi chạy

`[ĐỀ XUẤT]` Ghi để sau không đọc ngược kết quả:

1. **S1 ≲ A1** (trộn mù hại hoặc hòa): phần A cho thấy lệch thang (độ dốc ~0,7), lệch mốc WT, và 80% hàng quét chỉ là 3 loại thay thế.
2. **S2 − A1 nhỏ, quanh 0 đến +0,01.** Ridge phẳng từ ~50% số cụm ([P1](../learning-curve-2026-10-22/README.md)): tham số tuyến tính của 180 đặc trưng đã gần ước lượng xong từ 89–172 cụm, nên thêm ~2.900 cụm quét ít có chỗ để cải thiện. Xác suất tôi gán cho "S2 đạt tiêu chí chính": **~30%**.
3. **N2 − N1 có khả năng dương hơn S2 − A1**, vì mạng `gate_no_pap` là mô hình duy nhất còn dốc theo số cụm ở P1. Xác suất "N2 đạt": **~35%**. [P3](../pretrain-p3-2026-10-22/README.md) (tiền huấn luyện tile → tinh chỉnh) âm, nên không kỳ vọng cao.
4. **Lợi ích nếu có sẽ tập trung ở ô test thuộc 20 cặp của bộ quét**, không ở phần ma trận thay thế còn lại.

## 7. Việc không làm

- Không dùng nhãn quét làm **test**; không đụng outer-test.
- Không thêm arm sau khi thấy kết quả; không chỉnh w ngoài lưới {0,05; 0,2; 1}.
- Không dùng trung bình rep1/rep2 cho nhãn quét (giảm nhiễu nhãn quét là hướng tiếp theo, ghi ở README, không làm ở đây).
- Không ghi file vào `data/` (đặc trưng quét tính trong bộ nhớ mỗi lần chạy).
- Không sửa `presentation/`, đề cương, trạng thái G2/G3.
