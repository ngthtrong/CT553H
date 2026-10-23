# R1 — Degformer sạch cụm (điều kiện G2 còn thiếu) — 22/10/2026

**Trạng thái: CHƯA CHẠY.** Đã dựng xong dữ liệu, mã, PROTOCOL chốt trước và notebook; huấn luyện do Trọng chạy trên Kaggle/Colab rồi tải kết quả về. Tới khi có `results.json` từ lượt chạy thật, **không có con số R1 nào** trong repo, và README này không nêu kết quả nào.

Tiêu chí, luật loại hàng, độ lệch so với script tác giả và dự đoán ghi trước: [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Kế hoạch gốc: [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md). Không đổi trạng thái G2: kết quả chỉ đi vào báo cáo.

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

## Việc Trọng làm tay

1. Dựng gói bằng `notebook-kit-2026-10-22/make_data_package.py` và `make_code_package.py`, xem danh sách, **tự upload** làm hai dataset riêng tư (`degron-data-v1`, `degron-code-*`) — hướng dẫn: `notebook-kit-2026-10-22/RUN.md`.
2. Import `r1-degformer-clean.ipynb`, bật GPU, gắn hai dataset, *Run All*. Đọc dòng **benchmark** ở ô 5 (giờ GPU ước lượng theo số đo thật) **trước** khi để chạy hết; quá hạn mức thì đặt `SEEDS = [17]` và chạy seed khác ở phiên sau.
3. Tải `r1-results.zip` (có ngay sau fold đầu tiên), giải nén vào `run-<phiên>/` cạnh README này.
4. `python -I aggregate_r1.py run-*/...` (hoặc dùng `results.json` do ô 5 ghi), rồi mới cập nhật README với kết quả, nhãn `[ĐO]`/`[DIỄN GIẢI]`, và báo trung thực kể cả khi âm.

## Chi phí `[ƯỚC LƯỢNG]`, chưa benchmark

Vài chục giây/epoch trên T4 với AMP, ≤ 50 epoch/fold (dừng sớm sau 10 epoch không cải thiện): ≲ 2 giờ/seed, ≲ 6 giờ cho ba seed. Ô benchmark thay ước lượng này bằng số đo trước khi chạy thật. So với E3 trên CPU (~17 phút/epoch), đây là lý do E3 từng hoãn R1.

## Giới hạn (chi tiết ở PROTOCOL §9)

Benchmark phát triển OOF, không phải kiểm chứng ngoài; luật loại **chặt hơn** cách ridge được kiểm soát; ngân sách nhãn của Degformer lớn hơn của ridge (260K peptide proteome + quét + bão hòa); "sạch" chỉ trong phạm vi E1–E3 và UniProt đã ghim.
