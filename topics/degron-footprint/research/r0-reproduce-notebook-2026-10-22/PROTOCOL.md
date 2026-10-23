# PROTOCOL — R0: tái lập mốc đã biết trong môi trường notebook — 22/10/2026

**Chốt trước khi chạy.** Tệp này được băm SHA-256 và nhúng vào `00-reproduce.ipynb` (ô tham số `PROTOCOL_SHA256`); `nbkit.check_protocol` dừng notebook nếu tệp đổi sau khi chốt. Không đổi trạng thái G2/G3, không sửa tiêu chí của thí nghiệm nào đã chốt.

## 1. Mục đích

`[ĐỀ XUẤT]` Mọi thí nghiệm huấn luyện tiếp theo (R1, R2, R3, R5) chạy trên Kaggle/Colab. R0 trả lời **một** câu: *môi trường notebook có tái lập đúng các con số đã đo trên máy cục bộ không?* Nếu không, **mọi kết quả notebook sau đó vô nghĩa** cho tới khi sửa môi trường. R0 **không huấn luyện mô hình mới** và không tạo kết luận khoa học nào.

## 2. Việc chạy (CPU, vài phút)

- **Cổng A.** Chạy lại đường ridge M3 của [learning-curve](../learning-curve-2026-10-22/run_curve.py): mức 100% (91 peptide) và mức nới ngưỡng 4,0 (176 peptide huấn luyện, outer-test vẫn 91 peptide), seed 17/29/43, 5 fold cov80 từ cache `learning-curve-sat-{base,ext4.0}.npz`. Kiểm 5 fold trùng `folds` trong `g2-saturation-2026-10-18/results.json`.
- **Cổng B.** Chạy `calibration-p6-2026-10-22/verify.py` nguyên trạng (nguyên mẫu `predict.py` khớp runner).
- **Tuỳ chọn C** (`RUN_FULL_CURVE = True`, ~10–20 phút CPU): chạy lại toàn bộ `run_curve.main()` gồm cả `gate_no_pap`. Chỉ để thông tin.

## 3. Tiêu chí chốt trước

Mốc lấy từ các file **đã commit** (`learning-curve-2026-10-22/results.json`, `calibration-p6-2026-10-22/verify.json`), đọc **trước** khi chạy bất cứ thứ gì có thể ghi đè chúng.

| Cổng | Đại lượng | Mốc | Dung sai | Nếu vi phạm |
|---|---|---|---|---|
| A1 | 5 fold outer trùng `folds` của G2 | trùng từng cụm | 0 | **Dừng.** Không báo gì khác |
| A2 | AUROC ridge, mức 100%, ensemble ba seed | 0,8081859… | \|Δ\| ≤ **1e-4** | Cổng hỏng |
| A3 | AUROC ridge, mức nới ngưỡng 4,0, ensemble | 0,8208224… | \|Δ\| ≤ **1e-4** | Cổng hỏng |
| A4 | AUROC ridge từng seed (6 giá trị) | theo `macro_auroc_per_seed` | \|Δ\| ≤ **1e-4** | Cổng hỏng |
| A5 | Δ(ext − 100%) và CI 95% bootstrap theo cụm | +0,0126; [+0,0061; +0,0190] | Δ: 1e-4; hai đầu CI: 5e-4 | Cổng hỏng |
| B | Mọi phép đối chiếu của `verify.py` (11 phép) | 0 | \|Δ\| < **1e-9** | Ghi hỏng; **không** dừng cổng A (B là độc lập) |
| C | (tuỳ chọn) AUROC từng mức của ridge / `gate_no_pap` | theo `results.json` | ridge 1e-4; `gate_no_pap` 5e-3 (chỉ thông tin) | `gate_no_pap` lệch chỉ ghi chú, **không** coi là hỏng cổng |

**Điều kiện "R0 đạt":** A1–A5 đều đạt **và** B đạt. R0 đạt ⇒ môi trường được phép dùng cho R1/R2/R3/R5. R0 hỏng ⇒ báo thẳng cổng nào, kèm `env.json` (phiên bản numpy/scikit-learn/torch), và **không** chạy các thí nghiệm sau.

`[DIỄN GIẢI]` Dung sai 1e-4 cho AUROC là chỗ chấp nhận khác biệt do BLAS/phiên bản scikit-learn giữa hai máy; nó **không** đủ rộng để che một lỗi chia fold hay lỗi dữ liệu. Dung sai của B giữ nguyên 1e-9 như `verify.py` vì phép đối chiếu đó chỉ là số học đặc trưng.

## 4. Đầu ra

`results.json` (kết quả cổng + số đo), `env.json` (môi trường), `gates.json` (từng cổng: quan sát/mốc/chênh/dung sai), `verify.json` (từ `verify.py`). Notebook in bảng cổng và **chỉ** câu "R0 ĐẠT" / "R0 HỎNG: <cổng>", không diễn giải thêm.

## 5. Giới hạn

- R0 chỉ chứng minh tái lập **số học** của đường đã có; nó không chứng minh mô hình đúng hay tổng quát.
- Cache `learning-curve-sat-*.npz` được dựng ở máy cục bộ; R0 không dựng lại cache từ dữ liệu thô (đường `rd.load_all` chỉ được kiểm gián tiếp qua cổng B).
- GPU không cần cho R0; kết quả neural (tuỳ chọn C) có thể khác nhau ở chữ số thập phân cuối giữa các phiên bản torch.
