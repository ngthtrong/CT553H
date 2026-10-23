# R1 — Degformer sạch cụm (điều kiện G2 còn thiếu) — 22/10/2026

**Trạng thái: ĐÃ CHẠY trên Kaggle (2×T4, 22–23/10/2026), đủ ba seed × năm fold.** Tiêu chí, luật loại hàng và dự đoán ghi trước ở [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Kết quả: [run-kaggle-20261022/](run-kaggle-20261022/) (gốc: [r1-results.zip](r1-results.zip), gồm cả điểm dự đoán từng seed). Kế hoạch gốc: [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md). Không đổi trạng thái G2: ghi trạng thái là quyết định của Trọng và GVHD.

Tiêu chí, luật loại hàng, độ lệch so với script tác giả và dự đoán ghi trước: [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Kế hoạch gốc: [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md). Không đổi trạng thái G2: kết quả chỉ đi vào báo cáo.

## Kết quả `[ĐO]` — [results.json](run-kaggle-20261022/results.json)

Degformer sạch cụm (PeptideTransformer 545.025 tham số; bảng huấn luyện 569.270 dòng, mỗi fold loại 3,4–8,1% dòng chạm cụm outer-test), AUROC mức ô, macro theo peptide, outer-test 47.847 ô của G2:

| Mô hình | AUROC |
|---|---:|
| **R1, ensemble ba seed** (từng seed 0,8012 · 0,8054 · 0,8004) | **0,8068** |
| ridge M3 ext 4,0 (đối chiếu chính) | 0,8208 |
| ridge base | 0,8082 |
| ΔPAP `cnn2w1` | 0,7693 |
| Degformer huấn luyện chỉ trên nhãn bão hòa (E3) | 0,7500 |
| checkpoint công bố (bị rò) | 0,9248 |

| So sánh ghép cặp theo cụm | Δ | CI 95% |
|---|---:|---|
| **R1 − ridge ext 4,0 (CHÍNH)** | **−0,0140** | [−0,0283; +0,0010] |
| R1 − ridge base | −0,0014 | [−0,0192; +0,0161] |
| R1 − ΔPAP | +0,0375 | [+0,0249; +0,0507] |
| R1 − checkpoint bị rò | −0,1180 | [−0,1387; −0,0979] |

Δ từng seed so với ridge ext: −0,0196 · −0,0154 · −0,0204. **Kết luận theo PROTOCOL §6: "không phân biệt được"** (CI phủ 0). Cả ba dự đoán ghi trước (§10) đều đúng: chênh với checkpoint rò ≥ 0,05 (thực tế 0,118); R1 nằm trong 0,75–0,88; kết luận không phải "R1 hơn".

- `[DIỄN GIẢI]` Rò rỉ làm phồng AUROC của checkpoint công bố 0,118; 0,9248 bằng 97% trần nhãn (0,9519), phù hợp với việc đã thuộc lòng ma trận từng peptide.
- `[DIỄN GIẢI]` Thêm 569K dòng tiền huấn luyện nâng transformer từ 0,7500 (E3) lên 0,8068 nhưng **không vượt** ridge chỉ học từ 92K ô. Cả ba seed đều âm so với ridge ext, CI chỉ chạm 0 từ phía dưới: nghiêng về "ridge ≥ Degformer" dù quy tắc không cho kết luận chắc hơn.
- `[ĐO]` Từng peptide (từ `per_peptide_ensemble`): R1 thắng ridge ext ở 43/91 peptide; tương quan AUROC từng peptide giữa R1 và ridge r = 0,82, tức các peptide khó là chung.
- Ghi chú huấn luyện: ~28–31 giây/epoch trên T4; epoch tốt nhất từ 5 đến 50; **một lượt (seed 29, fold 0) chạm trần 50 epoch** ([r1-train-log-seed29.json](run-kaggle-20261022/r1-train-log-seed29.json)). Mặt nạ loại hàng loại 3,4–8,1% dòng mỗi fold ([r1-exclusion-check.json](run-kaggle-20261022/r1-exclusion-check.json)).

## Câu hỏi

Kiến trúc Degformer đã công bố, huấn luyện lại bằng công thức của tác giả trên 569.270 dòng **đã loại các hàng chạm cụm outer-test**, hơn/ngang/kém ridge M3 ext 4,0 (0,8208) trên 47.847 ô outer-test của G2? Hai mốc đã đo để đặt cạnh: checkpoint công bố bị rò 0,9248 và Degformer chỉ trên nhãn bão hòa (E3) 0,7500.

## Đã chuẩn bị `[ĐO]` (cục bộ, không huấn luyện)

| Việc | Kết quả |
|---|---|
| [build_exclusion_r1.py](build_exclusion_r1.py) → `data/processed/r1-row-exclusion.npz`, [exclusion-summary.json](exclusion-summary.json) | Mỗi fold loại 3,38–8,11% dòng (19.242–46.152); 99,83% dòng ánh xạ được vào UniProt người; cổng "không còn sequence test trong tập huấn luyện" qua ở cả 5 fold. Đây là dữ liệu chuẩn bị, không phải kết quả R1 |
| Class `PeptideTransformer` dựng từ AST `predict.py` | 545.025 tham số; AST trùng với `train_v2.py`; SHA khớp manifest G2 |
| [selftest_r1.py](selftest_r1.py) (dữ liệu giả 3.000 dòng, 2 epoch CPU) | Đạt: đầu ra hữu hạn, tất định theo seed trên CPU, quy tắc kết luận `aggregate_r1.verdict` cho đúng bốn nhánh. **Không phải huấn luyện R1** |
| Chạy `load_inputs` + cổng rò trên một cây thư mục tối thiểu (chỉ file có trong gói mã + gói dữ liệu) | Đạt trong 3,4 giây: nên notebook không phụ thuộc file nào ngoài hai gói |

## File

| File | Vai trò |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước |
| [build_exclusion_r1.py](build_exclusion_r1.py) | Dựng mặt nạ loại hàng (cục bộ, MMseqs2 ≤ 2 luồng) |
| [run_r1.py](run_r1.py) | Huấn luyện từng (seed, fold), lưu điểm + checkpoint, tiếp tục được khi phiên ngắt |
| [aggregate_r1.py](aggregate_r1.py) | Gộp seed đã tải về, bootstrap theo cụm, kết luận theo PROTOCOL §6 (CPU, vài giây) |
| [r1-degformer-clean.ipynb](r1-degformer-clean.ipynb) | Notebook sạch outputs, đã stamp SHA-256 PROTOCOL |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook (sau đó chạy `stamp_protocol.py`) |
| [data-needs.json](data-needs.json) | File dữ liệu notebook cần, cho `make_data_package.py` |
| [selftest_r1.py](selftest_r1.py) | Kiểm đường code, không phải thí nghiệm |

## Cách chạy lại (đã làm một lần ngày 22/10/2026)

1. Dựng gói bằng `notebook-kit-2026-10-22/make_data_package.py` và `make_code_package.py`, xem danh sách, **tự upload** làm hai dataset riêng tư (`degron-data-v1`, `degron-code-*`) — hướng dẫn: `notebook-kit-2026-10-22/RUN.md`.
2. Import `r1-degformer-clean.ipynb`, bật GPU, gắn hai dataset, *Run All*. Đọc dòng **benchmark** ở ô 5 (giờ GPU ước lượng theo số đo thật) **trước** khi để chạy hết; quá hạn mức thì đặt `SEEDS = [17]` và chạy seed khác ở phiên sau.
3. Tải `r1-results.zip` (có ngay sau fold đầu tiên), giải nén vào `run-<phiên>/` cạnh README này.
4. `python -I aggregate_r1.py run-*/...` (hoặc dùng `results.json` do ô 5 ghi), rồi mới cập nhật README với kết quả, nhãn `[ĐO]`/`[DIỄN GIẢI]`, và báo trung thực kể cả khi âm.

## Chi phí (ước lượng ban đầu; số đo thật ở mục Kết quả)

Vài chục giây/epoch trên T4 với AMP, ≤ 50 epoch/fold (dừng sớm sau 10 epoch không cải thiện): ≲ 2 giờ/seed, ≲ 6 giờ cho ba seed. Ô benchmark thay ước lượng này bằng số đo trước khi chạy thật. So với E3 trên CPU (~17 phút/epoch), đây là lý do E3 từng hoãn R1.

## Giới hạn (chi tiết ở PROTOCOL §9)

Benchmark phát triển OOF, không phải kiểm chứng ngoài; luật loại **chặt hơn** cách ridge được kiểm soát; ngân sách nhãn của Degformer lớn hơn của ridge (260K peptide proteome + quét + bão hòa); "sạch" chỉ trong phạm vi E1–E3 và UniProt đã ghim.
