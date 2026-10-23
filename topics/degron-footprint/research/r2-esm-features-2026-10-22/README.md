# R2 — Đặc trưng ESM-2 đóng băng cộng vào ridge M3 — 22/10/2026

**Trạng thái: ĐÃ CHẠY trên Kaggle (2×T4, 22/10/2026).** Tiêu chí và dự đoán ghi trước ở [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Kết quả: [run-kaggle-20261022/](run-kaggle-20261022/) (gốc: [r2-results.zip](r2-results.zip), gồm điểm OOF). Kế hoạch gốc: [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md). Tiếp nối ở [R6](../r6-ladder-scan-2026-10-23/README.md) (đổi cỡ ESM-2, đưa ESM vào CNN/mCNN).

Tiêu chí, công thức đặc trưng và dự đoán ghi trước: [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Kế hoạch gốc: [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md).

## Kết quả `[ĐO]` — [results.json](run-kaggle-20261022/results.json), [r2-stage1.json](run-kaggle-20261022/r2-stage1.json)

ESM-2 650M đóng băng, Δ embedding PCA-64 (khớp chỉ trên outer-train), ridge, ba seed:

| Biến thể | AUROC ensemble | Từng seed |
|---|---:|---|
| M3 (đối chứng, tái lập 0,8208) | 0,8208 | 0,8204 · 0,8210 · 0,8209 |
| **M3 + ESM** | **0,8230** | 0,8228 · 0,8231 · 0,8233 |
| ESM-only (chỉ mô tả) | 0,7853 | 0,7853 · 0,7853 · 0,7853 |

**M3+ESM − M3 = +0,0022, CI 95% [−0,0033; +0,0082]**, Δ từng seed +0,0024 · +0,0021 · +0,0024. **Kết luận theo PROTOCOL §3: "chưa đủ bằng chứng (CI phủ 0)".** ESM-only − M3 = −0,0355 [−0,0495; −0,0211] (mô tả). Cả ba dự đoán ghi trước (§7) đều đúng.

- `[ĐO]` Từ `per_peptide_ensemble`: M3+ESM thắng M3 ở 44/91 peptide (thua 47), trung vị Δ −0,0011; **bỏ hai peptide hưởng lợi nhiều nhất thì Δ trung bình = −0,0004**. Nên "ba seed đều dương" không phải bằng chứng độc lập: ba seed dùng chung dữ liệu và fold, ridge gần như tất định.
- `[DIỄN GIẢI]` ESM-only đạt 0,7853 chỉ với 64 chiều tuyến tính (cao hơn ΔPAP 0,7693 và E3 0,7500), nhưng thêm vào M3 hầu như không đổi: ở mức tuyến tính, thông tin pLM phần lớn trùng với one-hot cộng ngữ cảnh. Trần lợi ích tuyến tính của ESM-650M khoảng +0,008.
- Chi phí đo thật: giai đoạn 1 (trích 92.337 ô × 2.560 chiều) 384 giây trên T4; giai đoạn 2 (PCA + ridge, 15 lượt × 3 biến thể) 95 giây. PCA-64 giữ ~80% phương sai. α của ESM-only luôn nằm ở biên lưới (1 hoặc 1000), nên con số ESM-only chỉ để mô tả.

## Câu hỏi

Δ embedding từ `facebook/esm2_t33_650M_UR50D` đóng băng (PCA 64 chiều, khớp chỉ trên outer-train) có làm ridge M3 ext 4,0 (0,8208) tốt hơn không? Đây là đổi **biểu diễn đầu vào**, không phải thiết kế tương tác mới.

## Đã chuẩn bị `[ĐO]` (cục bộ, không chạy ESM-2, không huấn luyện)

| Việc | Kết quả |
|---|---|
| [make_seqtable.py](make_seqtable.py) → `data/processed/r12-seqtable.npz` (dùng chung với R1) | 176 peptide, 92.337 ô = 47.847 (gốc) + 44.490 (nới ngưỡng) theo đúng thứ tự gộp của `run_curve.py`; nhãn khớp hai cache; 600 hàng đặc trưng dựng lại khớp cache |
| [selftest_r2.py](selftest_r2.py) | Đạt: (1) chỉ mục token/vị trí của `extract_features` đúng trên mô hình giả (Δ tại điểm đột biến khác 0 đúng chỗ, trung bình Δ = Δ/28); (2) **cổng tái lập**: ridge M3 qua `common.py` seed 17 cho 0,820421, đúng bằng `learning-curve-2026-10-22/results.json`; (3) bốn nhánh của quy tắc kết luận. **Không phải kết quả R2** |
| Chạy `load_combined` trên một cây thư mục tối thiểu (chỉ file có trong gói mã + gói dữ liệu) | Đạt: notebook không phụ thuộc file nào ngoài hai gói |

## File

| File | Vai trò |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước |
| [make_seqtable.py](make_seqtable.py) | Bảng trình tự 92.337 ô (cục bộ, dùng chung R1/R2) |
| [common.py](common.py) | Nạp tập gộp và chia (seed, fold) sao nguyên `run_curve.py`; ridge dùng toàn bộ cột |
| [run_r2.py](run_r2.py) | Giai đoạn 1 (trích đặc trưng, GPU) và giai đoạn 2 (PCA + ridge + so sánh, CPU); chạy lại phần tổng hợp cục bộ: `python -I run_r2.py <thư-mục-chứa-r2-oof.npz>` |
| [r2-esm.ipynb](r2-esm.ipynb) | Notebook sạch outputs, đã stamp SHA-256 PROTOCOL |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook (sau đó chạy `stamp_protocol.py`) |
| [data-needs.json](data-needs.json) | File dữ liệu notebook cần |
| [selftest_r2.py](selftest_r2.py) | Kiểm đường code, không phải thí nghiệm |

## Cách chạy lại (đã làm một lần ngày 22/10/2026)

1. Dựng và upload hai gói như R1 (xem `notebook-kit-2026-10-22/RUN.md`).
2. Import `r2-esm.ipynb`, bật GPU. **Bật Internet** để tải trọng số ESM-2 từ Hugging Face (Kaggle đòi tài khoản xác minh điện thoại); nếu không bật được, thêm ESM-2 650M làm dataset/model — ô 5 tự dò thư mục chứa `config.json` có tên `esm2_t33_650M`.
3. *Run All*. Cache đặc trưng (~0,5 GB) nằm ngoài gói kết quả. Tải `r2-results.zip`, giải nén vào `run-<phiên>/` cạnh README này.
4. Cập nhật README với kết quả sau khi có `results.json`, báo trung thực kể cả khi âm; kiểm lại ngày đọc giấy phép trọng số trong `r2-stage1.json`.

## Chi phí (ước lượng ban đầu; số đo thật ở mục Kết quả)

Giai đoạn 1 (T4, fp16): 10–30 phút. Giai đoạn 2 (CPU): 10–20 phút. Ít hơn nhiều so với R1.

## Giới hạn (chi tiết ở PROTOCOL §6)

Benchmark phát triển OOF, không phải kiểm chứng ngoài; ESM-2 đã được tiền huấn luyện trên UniRef nên các protein này có thể đã "được thấy"; một cỡ mô hình, một công thức; Δ dương không tách "thông tin pLM" khỏi "thêm chiều"; nếu nhận, suy luận trong sản phẩm cần ESM-2 (~1,3 GB) — chi phí cần cân ở R5.
