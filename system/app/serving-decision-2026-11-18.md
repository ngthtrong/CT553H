# Biên bản phục vụ model — 18/11/2026

> **Có hiệu lực từ 18/11/2026.** Soạn theo [serving-policy.md](../serving-policy.md) §3, mục 4.3 của
> [plan-system.md](../../plan-system.md); Trọng ghi tên và ngày xác nhận ở mục *Quyết định* ngày 18/11/2026. Không
> thay đổi trạng thái khoa học.

| Mục                       | Nội dung                                                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model                      | `esm2-35m-lora-d-aa4fc2b7` (kind `torch_lora`; ESM-2 35M + LoRA rank 8, ensemble 3 seed 17/29/43)                                                                                       |
| Hash trọng số đăng ký | `d6729faf0bc4fa781239fba2945362ae72273901afdde5d35138e2b35401303f` (manifest `data/processed/lora-d-serving-v1/esm2-35m-lora-d-v1.json`)                                                |
| Thay cho                   | `m3-ext4.0-platt-v1` (ridge npz, mặc định của registry, baseline v0.2)                                                                                                                |
| Cách bật                 | `DF_DEFAULT_MODEL_ID=esm2-35m-lora-d-aa4fc2b7` trong `system/app/.env` (cờ `is_default` trong registry **không** đổi; `/healthz` báo `default_model_source = setting`) |
| Phạm vi                   | Cài đặt Docker local trên máy của Trọng và bản trình bày bảo vệ. Không áp dụng cho bản cài của người khác, không có bản công khai                                 |
| Model còn lại            | npz vẫn phục vụ, chọn được trên giao diện (plan-system 1.1)                                                                                                                        |

## Bằng chứng

| Bước                           | Tệp                                                                                                                            | Kết quả `[ĐO]`                                                                                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Candidate                        | `/v1/models/esm2-35m-lora-d-aa4fc2b7` (model card); `research/lora-refit-transfer-2026-11-16/model-card.json`               | `status = frozen` (16/11), 3 model_id + sha256, calibrator logistic 3 lớp học chỉ trên OOF W (`T_fit_cells = 0`)                                  |
| Parity phục vụ ↔ nghiên cứu | `tests/results/lora-bundle.json` → `serving_parity`                                                                        | Hai tile đủ 532 ô, CPU: sai khác tối đa **0,0** (điểm từng seed, điểm ensemble, xác suất)                                              |
| Parity khác runtime             | `tests/results/lora-bundle.json` → `cross_runtime_parity`                                                                  | CUDA (Windows, RTX 5060) ↔ CPU, 32 hàng W × 3 seed: tối đa **3,0 × 10⁻⁶**                                                                   |
| Latency / RAM / image            | `tests/results/latency-lora.json` (17/11, Docker, 4 luồng CPU)                                                               | p50 37,7 s, p95 **39,1 s/tile** (npz: p95 20,2 ms); RSS container API 514,5 MiB; image 1,77 GB (npz 399 MB). **NFR-01 (300 ms) không đạt** |
| Cache (plan-system 1.2) | `tests/test_cache.py`; `tests/results/cache-lora.json` | Lần đầu ≥ 33,1 s; mở/xuất lại cùng tile ≤ 30,2 ms; kết quả bằng nhau |
| Test sau khi bật | `acceptance-system-2026-11-18.md`, `acceptance-system-2026-11-18b.md` | Container PG 314 pass / 18 skip, SQLite 332 pass; e2e thật LoRA-D mặc định 13 pass + 1 skip (NF-06), npz mặc định 14/14 (lượt 2) |

## Giới hạn phải đi kèm

Model card và nhãn giao diện hiển thị `development benchmark (post-hoc transfer, previously examined held-out source), not external validation`. Các giới hạn L1–L10 của
[biên bản D-4](../../research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md) áp dụng nguyên văn, đặc biệt:

- **L1** T đã từng được xem; đánh giá chuyển miền hậu kiểm, không phải validation độc lập.
- **L3** Ở tầng PSI(WT) > 5, baseline zero có MAE thấp hơn LoRA-D (0,3470 so với 0,3622). Cổng miền R3 vẫn áp dụng cho
  LoRA-D như cho npz (DEVIATIONS §12); nới cổng là quyết định riêng (plan-system 1.6).
- **L5** ECE lớp plus của LoRA-D (0,0523) kém W5-D (0,0384).
- **L6** Chiều minus yếu (AUROC− 0,5932, 85 peptide).
- **L10** Chưa chứng minh lợi ích wet lab hay tiết kiệm nguồn lực.
- Vận hành: ≈ 40 s mỗi tile trên CPU; protein dài (ví dụ 382 tile) mất nhiều giờ. Giao diện báo ước lượng và hỏi xác
  nhận trước khi chạy (plan-system 1.1, 1.7).
- `TRAINING_PEPTIDE` của LoRA-D theo 235 tile W (DEVIATIONS §12), khác 176 peptide của npz.

## Quyết định

- Phương án: bật LoRA-D làm model mặc định cho phạm vi ở bảng trên; npz giữ làm model tuỳ chọn và là phương án quay về.
- Người quyết định: Nguyễn Thanh Trọng — đã xác nhận ngày 18/11/2026 (ghi trong tệp: "Trọng - 18/11/2026").
- Ghi nhận của GVHD (TS. Hồ Quang Thái): đã ghi nhận (theo Trọng ghi ngày 18/11/2026).
- Không thay đổi: `scientific_status = development_not_gate_closure`; G3 chưa đóng; biên bản này không phải nghiệm thu
  khoa học và không suy ra từ thứ hạng development (R-8).

## Quay về

Xoá `DF_DEFAULT_MODEL_ID` khỏi `system/app/.env`, `docker compose up -d api worker`; `/healthz` phải trả
`default_model_id = m3-ext4.0-platt-v1`, `default_model_source = registry`. Ghi một dòng ngày và lý do vào biên bản này.
