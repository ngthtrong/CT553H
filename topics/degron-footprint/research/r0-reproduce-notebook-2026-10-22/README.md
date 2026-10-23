# R0 — Tái lập mốc đã biết trong môi trường notebook — 22/10/2026

**Trạng thái: ĐÃ CHẠY trên Kaggle (CPU, 22/10/2026) — ĐẠT 12/12 cổng.** [PROTOCOL.md](PROTOCOL.md) chốt trước; notebook [00-reproduce.ipynb](00-reproduce.ipynb); kết quả ở [run-kaggle-20261022/](run-kaggle-20261022/) (gốc: [r0-results.zip](r0-results.zip)). Đây là bước đầu tiên bắt buộc: R0 đỏ ⇒ không chạy R1/R2/R3 (đã đỏ không xảy ra).

**[ĐO] Kiểm hạ tầng cục bộ (22/10/2026, ~35 giây CPU, cùng máy với mốc nên chênh bằng 0).** Chạy từng ô của notebook qua gói mã + gói dữ liệu vừa dựng, trong cây thư mục ghép: 5 fold trùng G2; ridge mức 100% **0,808186** và nới ngưỡng 4,0 **0,820822** khớp mốc `learning-curve-2026-10-22/results.json` (|Δ| = 0); Δ(ext − 100%) 0,012636 và CI [0,006122; 0,018994] khớp; `verify.py` (11 phép) max |Δ| = 4,4·10⁻¹⁰ < 1e-9. `[DIỄN GIẢI]` Đây chỉ chứng minh **hạ tầng đóng gói đúng** (gói đủ file, SHA khớp, đường dẫn ghép đúng). Giá trị kiểm môi trường thật chỉ có khi chạy trên nền tảng khác — việc của Trọng.

## Kết quả `[ĐO]` (Kaggle, 22/10/2026) — [results.json](run-kaggle-20261022/results.json), [gates.json](run-kaggle-20261022/gates.json), [verify.json](run-kaggle-20261022/verify.json), [env.json](run-kaggle-20261022/env.json)

Môi trường: Python 3.13.15, numpy 2.1.3, scikit-learn 1.6.1, 4 CPU, 44 giây; gói mã commit `7ab4502614ec` (cây **dirty**), gói dữ liệu `degron-data-v1`.

| Cổng | Quan sát | Mốc | \|Δ\| |
|---|---:|---:|---:|
| ridge base (100%), ensemble | 0,808186 | 0,808186 | 0 |
| ridge base, từng seed 17/29/43 | 0,806245 · 0,806818 · 0,808076 | như mốc | 0 |
| ridge ext 4,0, ensemble | 0,820822 | 0,820822 | 0 |
| ridge ext 4,0, từng seed | 0,820421 · 0,820982 · 0,820924 | như mốc | 0 |
| Δ(ext − 100%) và CI P0 | +0,012636 · [0,006122; 0,018994] | như mốc | 0 |
| `verify.py` (11 phép đối chiếu predict ↔ runner) | max 4,4·10⁻¹⁰ | < 1e-9 | đạt |

`[DIỄN GIẢI]` Ridge và nguyên mẫu `predict.py` **tái lập bit-bit trên nền tảng khác** (khác phiên bản Python, numpy và scikit-learn so với máy phát triển). Giới hạn: gói mã dựng từ cây làm việc chưa commit; R0 chỉ kiểm số học, không chứng minh mô hình đúng.

## Gồm

| File | Việc |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước (dung sai 1e-4 cho AUROC, 1e-9 cho `verify.py`) |
| [run_r0.py](run_r0.py) | `run(ctx)`: import hàm từ `run_curve.py`, chạy cổng A (ridge), cổng B (`verify.py`), tuỳ chọn C (`run_curve.main()`) |
| [00-reproduce.ipynb](00-reproduce.ipynb) | Notebook mỏng (stamp SHA-256 của PROTOCOL) |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook từ mã |

## Đầu ra khi chạy

`results.json`, `env.json`, `gates.json`, `verify.json` (nén trong `r0-results.zip`). Đặt vào `run-<nền-tảng>-<ngày>/` cạnh README này.

## Giới hạn

R0 chỉ kiểm tái lập số học của đường ridge và nguyên mẫu; không dựng lại cache `learning-curve-sat-*.npz` từ dữ liệu thô và không chứng minh mô hình đúng.
