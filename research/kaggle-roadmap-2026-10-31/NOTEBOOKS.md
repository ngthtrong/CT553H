# Các notebook đã triển khai

12 notebook đơn và1 notebook tổng thật trong [notebooks/](notebooks/); logic ở `degron_v3/`, entry CLI `run_stage.py`. Tất cả mặc định SMOKE=True; chạy official cần SMOKE=False. Stage có học đều lưu model/checkpoint mới, OOF, config/data/code/protocol identity và môi trường.

| Stage | Công việc và model mới | Input thêm | Output chính |
|---|---|---|---|
| 00 | Audit schema/nhãn/split; tái lập Ridge lịch sử ở official | Core v3 | gates, data-summary, legacy-reproduction |
| 01 | Ridge A–E, pair/composition/unordered/W3/W5; curve W5-D 25/50/75/100% nhóm | Core v3 | model.joblib từng seed/fold, calibration predictions, OOF, paired CI |
| 02 | Probe pLM/tokenizer/tài nguyên; không fit nhãn | Complete pinned weights | preflight.json, model locks, blocked reasons |
| 03 | Trích Δsite/meanΔ, optional crop±7 theo model/scope/shard | Weights + preflight; T cần selection lock | pool.npy, crop.npy, rows, progress, feature-manifest |
| 04 | Fit Ridge/PCA64 pLM-only và W5+pLM, B/D; nested family selection | Complete pooled features stage03 | heads.joblib, OOF, nested-selection |
| 05 | Train pointwise k1/CNN k5/mCNN k3/5/7 với one-hot và frozen ESM35, B/D/E | Complete ESM35 crop | model.pt + optimizer checkpoints, OOF, calibration predictions |
| 06 | Fit sat/quality/source-aware Ridge; scratch CNN so scanning-pretrain→saturation-fine-tune | Core scan_dev rep1/rep2 | replicate audit, new CNN/Ridge, OOF |
| 07 | Fit 3-class calibration, W5 final model refit/export và chấm held scanning | Training output + selected recipe | selection-lock, calibrated OOF, W5 final-model, held results, model-card |
| 08 | Audit nguồn ngoài: endpoint/units/sequence/exact overlap | Reviewed external_table | source_pending hoặc audit; chưa automatic external prediction |
| 09 | Audit cấu trúc; opt-in train cùng cohort W5/SaProt true/masked 3Di | Reviewed structure_table + SaProt weights/preflight | structure_pending hoặc audited mapping, feature/head/OOF |
| 10 | Tổng hợp OOF đúng data identity/mode, giữ kết quả âm | Các stage outputs | evidence.json/CSV |
| 11 | Train frozen head, LoRA attention Q/V+head; optional full tuning8M/35M, B/D | Complete weights; GPU official | adapter/head-model.pt mới, optimizer, changed_parameters, OOF |

Thứ tự lõi: **00 → 01**, **02 → 03 → 04 → 05**, sau đó **07 → 10**; **06** và **11** là nhánh train bổ sung trên cùng W, chạy trước quyết định ứng viên. Stage08/09 có cổng dữ liệu riêng. Không mở T để chọn model rồi gọi T là xác nhận độc lập.

Các thư mục result phải được gắn bằng đường dẫn cụ thể, không dùng `next(glob)` để đoán. Family/scale screening cần tạo feature từng model; notebook không tải/chạy tất cả model lớn trong một phiên mặc định. ESM1v 5 member được giữ như các candidate; ensemble5 chuyên biệt chưa tự động gộp.

Smoke04/05 dùng fixture ngẫu nhiên để kiểm luồng/head; smoke03 dùng weights thật, smoke11 dùng ESM2-8M thật + ΔPSI thật. Smoke08/09 kiểm nhánh pending. Đọc [RUN.md](RUN.md) để cấu hình chính xác và chuyển official.

**Notebook tổng:** [12-all-in-one.ipynb](notebooks/12-all-in-one.ipynb) tự điều phối toàn bộ route trên, với code embedded, download khi cần và task cache/resume. Xem [ALL-IN-ONE.md](ALL-IN-ONE.md).
