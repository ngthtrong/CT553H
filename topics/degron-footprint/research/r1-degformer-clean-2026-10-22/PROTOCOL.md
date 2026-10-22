# R1 — Degformer sạch cụm: PROTOCOL chốt trước khi chạy

Chốt ngày 22/10/2026, **trước khi** huấn luyện bất kỳ mô hình R1 nào và trước khi thấy điểm nào của R1. Không sửa tiêu chí sau khi xem kết quả; nếu phải sửa thì thêm mục "sửa sau khi xem" kèm ngày và lý do, không ghi đè. SHA-256 của file này được nhúng vào notebook (`stamp_protocol.py`).

Thí nghiệm này chạy **điều kiện G2 còn thiếu** ("đối chứng Degformer sạch cụm") mà [E3 của G2 mở rộng](../g2-extension-2026-10-18/PREREGISTRATION.md) đã hoãn vì ~70 giờ CPU. Nó **không** tự động đổi trạng thái G2: kết quả đi vào báo cáo; việc ghi trạng thái là quyết định riêng của Trọng và GVHD.

## 1. Câu hỏi

Khi kiến trúc Degformer đã công bố được huấn luyện lại bằng đúng công thức của tác giả trên bảng huấn luyện 569.270 dòng **sau khi loại mọi hàng chạm cụm outer-test** của từng fold, nó hơn, ngang, hay kém ridge M3 (ext 4,0) trên cùng 47.847 ô outer-test của G2?

`[ĐO]` Mốc liên quan đã có: checkpoint công bố **bị rò** (88,12% ô trùng khít sequence với bảng huấn luyện của tác giả, 91/91 WT) cho macro AUROC 0,9248; kiến trúc huấn luyện từ đầu chỉ trên nhãn bão hòa (E3) cho 0,7500; ridge ext 4,0 cho 0,8208. R1 đo khoảng giữa hai cực đó khi dữ liệu huấn luyện lớn **và** sạch cụm.

## 2. Dữ liệu và luật loại hàng (chốt trước)

Bảng huấn luyện: `degformer-isolated/training_data.csv` (569.270 dòng, `sequence` 28-mer, `controlPSI`), SHA-256 `6d492962…46f2`. Với mỗi outer fold f (test = 47.847 ô của 91 peptide trong các cụm cov80 của fold, trùng G2), **loại khỏi huấn luyện** hợp của ba luật, dựng bởi [build_exclusion_r1.py](build_exclusion_r1.py) (đã chạy cục bộ; đây là chuẩn bị dữ liệu, không huấn luyện):

| Luật | Định nghĩa | Ý nghĩa |
|---|---|---|
| **E1** | `sequence` trùng khít một ô đột biến hoặc WT của peptide outer-test của fold | chặn rò trực tiếp |
| **E2** | khoảng cách Hamming ≤ 8 (identity ≥ 20/28) tới một WT outer-test của fold | chặn biến thể gần (kể cả đột biến quét nhiều vị trí) |
| **E3** | hàng chứa một 12-mer của protein P (UniProt người ghim 2026_03, 20.439 protein) mà (a) P thuộc cụm cov80 outer-test của fold, hoặc (b) P có hit MMseqs2 vào một thành viên cụm đó (id ≥ 0,30, e ≤ 1e-3, alnlen ≥ 50; `-s 7.5`) | chặn đồng dạng mức protein/paralog trong phạm vi UniProt đã ghim |

`[ĐO]` ([exclusion-summary.json](exclusion-summary.json)) 99,83% hàng ánh xạ được vào ít nhất một protein bằng 12-mer. Số hàng bị loại / còn lại theo fold:

| Fold | Loại (hợp E1∪E2∪E3) | Còn lại | Trong đó E3 (a)-chỉ-cụm | Protein bị loại |
|---:|---:|---:|---:|---:|
| 0 | 46.152 (8,11%) | 523.118 | 14.280 | 1.323 |
| 1 | 27.557 (4,84%) | 541.713 | 11.546 | 251 |
| 2 | 31.034 (5,45%) | 538.236 | 8.868 | 432 |
| 3 | 44.937 (7,89%) | 524.333 | 10.681 | 1.000 |
| 4 | 19.242 (3,38%) | 550.028 | 11.572 | 182 |

Cổng bắt buộc (runner `assert`): sau khi loại, **không còn** sequence nào của ô/WT outer-test trong tập huấn luyện của fold.

**Hai điều cần nói thẳng:**
- Luật loại **chặt hơn** cách ridge được kiểm soát (ridge chỉ tách theo cụm cov80). Cố ý: đối chứng "sạch" phải sạch hơn mức tối thiểu. Hệ quả là Degformer bị loại thêm họ gen mà ridge vẫn thấy lúc huấn luyện; nếu kết quả là "ridge hơn", phải đọc kèm điều này. Mặt nạ chỉ-cụm (E1∪E2∪E3a) *không* chạy trong lượt này; muốn chạy phải thêm PROTOCOL mới.
- "Sạch" chỉ nghĩa trong phạm vi E1–E3: 0,17% hàng không ánh xạ được vào UniProt đã ghim chỉ bị E1/E2 chặn, và paralog nằm ngoài UniProt đã ghim không bị phát hiện. 432 cửa sổ 12-mer bị bỏ vì lặp ở > 200 protein.

## 3. Huấn luyện (chốt trước)

**Kiến trúc:** `PeptideTransformer(vocab=21)` dựng từ AST của `predict.py` (SHA khớp manifest G2; AST trùng với class trong `train_v2.py`): d_model 128, 8 head, 4 lớp, feed-forward 256, dropout 0,1; **545.025 tham số** (cổng: bằng đúng số này).

**Siêu tham số từ `train_v2.py`** (runner đọc hằng số bằng AST, không gõ tay): `BATCH_SIZE = 512`, `LR = 1e-4`, `EPOCHS = 50`, Adam, MSE trên `controlPSI` chuẩn hóa z (thống kê train của fold), `ReduceLROnPlateau(factor 0,5, patience 2)`, AMP fp16 trên GPU.

**Độ lệch có chủ ý so với script tác giả** (ghi để không ai đọc nhầm là "tái lập nguyên văn"):

| Tác giả | R1 | Vì sao |
|---|---|---|
| validation 10% **ngẫu nhiên theo dòng** (`random_state=42`) | validation 10% **theo nhóm protein** (`GroupShuffleSplit`, `random_state=seed`; nhóm = protein đầu tiên ánh xạ được, dòng không ánh xạ được tự thành nhóm) | validation ngẫu nhiên rò đồng dạng vào chọn epoch |
| 50 epoch cố định, lưu mỗi epoch | tối đa 50 epoch, **dừng nếu 10 epoch liền không cải thiện val_mse**, chọn epoch val_mse thấp nhất | tiết kiệm giờ GPU; vẫn trong trần 50 của tác giả |
| tính thêm metric trên toàn tập train mỗi epoch | không tính | chỉ để in, không ảnh hưởng trọng số |
| `cudnn.benchmark = True` | tắt, bật cờ tất định của `nbkit.set_seeds` | tái lập tốt hơn; GPU vẫn có thể lệch ở chữ số thập phân cuối |
| 90% dữ liệu (10% giữ bí mật của tác giả) | 100% của bảng sau khi loại; 10% bí mật của tác giả **không có** trong repo | không thể làm khác |

**Điểm ô outer-test:** `score = (pred(mutant) − pred(WT)) × sd` (đơn vị PSI), từ checkpoint epoch tốt nhất; AUROC bất biến theo `sd`.

## 4. Seed và thứ tự ưu tiên (chốt trước)

Bắt buộc theo thứ tự: seed **17** (cả 5 fold) → seed **29** → seed **43**. Chạy tuần tự trong cùng phiên nếu hạn mức cho phép; nếu không, mỗi seed một phiên và gộp bằng [aggregate_r1.py](aggregate_r1.py). Mỗi (seed, fold) lưu điểm và checkpoint ngay khi xong; phiên bị ngắt chạy lại sẽ bỏ qua fold đã xong.

## 5. Chỉ số và so sánh (chốt trước)

AUROC mức ô, macro theo peptide (`derisk.macro_auroc`), nhãn dương ΔPSI ≥ 1,0. Điểm OOF **ensemble** = trung bình điểm các seed đã hoàn tất 5 fold. So sánh ghép cặp theo peptide, bootstrap 5.000 lần theo cụm (`run_curve.compare`):

| So sánh | Vai trò |
|---|---|
| **R1 − ridge ext 4,0** (per-peptide đã lưu ở `learning-curve-2026-10-22/results.json`, macro 0,8208) | **chính**, quyết định kết luận |
| R1 − ridge base (0,8082) | mô tả |
| R1 − ΔPAP `cnn2w1` (0,7693) | mô tả |
| R1 − checkpoint công bố bị rò (0,9248) | mô tả: đo mức rò đã thổi phồng điểm |

Từng seed được so với ridge ensemble ba seed đã lưu (chênh giữa ridge từng seed và ensemble ≤ 5e-4 theo `results.json`).

## 6. Tiêu chí kết luận (chốt trước)

Gọi Δ = A(R1 ensemble) − A(ridge ext 4,0), [lo, hi] là CI 95%, Δ_s là hiệu từng seed so với ridge ext 4,0:

| Điều kiện | Kết luận |
|---|---|
| lo > 0, mọi Δ_s > 0, **đủ ba seed** | Degformer sạch cụm **hơn** ridge ext 4,0 |
| hi < 0, đủ ba seed | ridge ext 4,0 **hơn** |
| còn lại, đủ ba seed | **không phân biệt được** (CI phủ 0 hoặc seed không đồng nhất) |
| chưa đủ ba seed | chỉ báo "tạm thời" hoặc "chưa kết luận"; **không** được dùng như kết luận R1 |

Hàm `aggregate_r1.verdict` cài đúng bảng này.

## 7. Cổng tự kiểm (dừng nếu hỏng)

1. Manifest dữ liệu khớp SHA-256; PROTOCOL khớp SHA nhúng.
2. 5 outer fold trùng `folds` của G2; bảng trình tự khớp nhãn cache.
3. Mặt nạ loại dựng cho đúng bảng này (SHA `training_data.csv` khớp) và không còn sequence test trong tập huấn luyện (§2).
4. Số tham số = 545.025; SHA `predict.py`, `train_v2.py`, `training_data.csv` khớp manifest G2.
5. Ridge ext 4,0 tham chiếu: macro per-peptide trung bình = 0,8208 (|Δ| ≤ 1e-9 so với `results.json`).

## 8. Điều không làm

- Không dùng checkpoint công bố của tác giả để khởi tạo (có thể rò); không nạp file `.pt` của họ (pickle sklearn).
- Không chọn lại seed, không chạy lại fold "cho đẹp", không đổi luật loại sau khi thấy điểm.
- Không tinh chỉnh siêu tham số ngoài các độ lệch ở §3.
- Không kết luận "Degformer tốt/kém" nói chung: chỉ trả lời câu hỏi ở §1 trên benchmark này.
- Không ghi G2 là hoàn tất.

## 9. Giới hạn ghi trước

- Benchmark **phát triển OOF**, không phải kiểm chứng ngoài; cùng 91 peptide đã khảo sát nhiều lần.
- Ngân sách nhãn **không** bằng nhau: Degformer thấy cả 260K peptide proteome (S1), quét (S4) và bão hòa (S7) của các peptide train; ridge chỉ thấy nhãn bão hòa. Đây là câu hỏi "công thức đã công bố, dữ liệu lớn và sạch", khác E3 ("cùng ngân sách nhãn").
- Thang nhãn: `controlPSI` của Degformer là PSI tuyệt đối của chuỗi, gộp ba bảng; ΔPSI suy ra bằng hiệu hai dự đoán.
- Một cách dừng sớm và validation theo nhóm là lựa chọn của R1, không phải của tác giả.

## 10. Dự đoán ghi trước

`[ĐỀ XUẤT]` (a) macro AUROC của R1 **thấp hơn rõ** 0,9248 của checkpoint bị rò (chênh ≥ 0,05); (b) R1 nằm trong khoảng 0,75–0,88; (c) kết luận "ridge hơn" hoặc "không phân biệt" nhiều khả năng hơn "R1 hơn". Nếu sai thì ghi rõ trong báo cáo.

## 11. Chi phí

`[ƯỚC LƯỢNG]`, chưa benchmark: ~490K–550K dòng huấn luyện, ~1.000 bước/epoch, mô hình 0,5 triệu tham số trên T4 với AMP: vài chục giây/epoch → ≤ ~25 phút/fold (không dừng sớm) → ~2 giờ/seed → ~6 giờ cho ba seed; dừng sớm giảm đáng kể. Ô benchmark ở đầu notebook in số đo thật và ước lượng giờ **trước** khi chạy thật; quyết định dừng nếu vượt hạn mức nằm ở Trọng. Tham chiếu cũ: E3 trên CPU ~17 phút/epoch.
