# R0 — Tái lập mốc đã biết trong môi trường notebook — 22/10/2026

**Trạng thái:** [PROTOCOL.md](PROTOCOL.md) đã chốt; notebook [00-reproduce.ipynb](00-reproduce.ipynb) đã dựng và **kiểm cục bộ**; **chưa chạy trên Kaggle/Colab** (Trọng tự chạy, xem [RUN.md](../notebook-kit-2026-10-22/RUN.md)). Đây là bước đầu tiên bắt buộc: R0 đỏ ⇒ không chạy R1/R2/R3.

**[ĐO] Kiểm hạ tầng cục bộ (22/10/2026, ~35 giây CPU, cùng máy với mốc nên chênh bằng 0).** Chạy từng ô của notebook qua gói mã + gói dữ liệu vừa dựng, trong cây thư mục ghép: 5 fold trùng G2; ridge mức 100% **0,808186** và nới ngưỡng 4,0 **0,820822** khớp mốc `learning-curve-2026-10-22/results.json` (|Δ| = 0); Δ(ext − 100%) 0,012636 và CI [0,006122; 0,018994] khớp; `verify.py` (11 phép) max |Δ| = 4,4·10⁻¹⁰ < 1e-9. `[DIỄN GIẢI]` Đây chỉ chứng minh **hạ tầng đóng gói đúng** (gói đủ file, SHA khớp, đường dẫn ghép đúng). Giá trị kiểm môi trường thật chỉ có khi chạy trên nền tảng khác — việc của Trọng.

## Gồm

| File | Việc |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước (dung sai 1e-4 cho AUROC, 1e-9 cho `verify.py`) |
| [run_r0.py](run_r0.py) | `run(ctx)`: import hàm từ `run_curve.py`, chạy cổng A (ridge), cổng B (`verify.py`), tuỳ chọn C (`run_curve.main()`) |
| [00-reproduce.ipynb](00-reproduce.ipynb) | Notebook mỏng (stamp SHA-256 của PROTOCOL) |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook từ mã |

## Đầu ra khi chạy thật

`results.json`, `env.json`, `gates.json`, `verify.json` (nén trong `r0-results.zip`). Đặt vào `run-<nền-tảng>-<ngày>/` cạnh README này.

## Giới hạn

R0 chỉ kiểm tái lập số học của đường ridge và nguyên mẫu; không dựng lại cache `learning-curve-sat-*.npz` từ dữ liệu thô và không chứng minh mô hình đúng.
