# Quy trình đưa model lên phục vụ (serving policy)

Tạo ngày **18/11/2026**, mục 4.3 của [plan-system.md](../plan-system.md). Áp dụng cho mọi thay đổi model **mặc định**
của ứng dụng local (`system/app/`), dù đổi bằng cờ `is_default` trong registry hay bằng biến `DF_DEFAULT_MODEL_ID`.

> **Nguyên tắc (R-8):** thứ hạng development, quyết định đóng G2 (D-4) hay một kết quả dương trên T **không tự cho
> phép** đổi model phục vụ. Model chỉ thành mặc định khi có một biên bản phục vụ ở `system/app/serving-decision-<ngày>.md`
> được Trọng ghi nhận; ghi nhận của GVHD được ghi riêng (có hoặc "chưa có"). Trạng thái khoa học vẫn
> `development_not_gate_closure`; biên bản phục vụ không đóng G3.

## 1. Các bước

| # | Bước | Bằng chứng tối thiểu | Ai |
| --- | --- | --- | --- |
| 1 | **Candidate**: model đã đóng băng (`status = frozen`), có model card, hash trọng số, lineage | `model_version` có `weights_sha256`; model card hiển thị ở `/model/<id>` | Claude/Trọng |
| 2 | **Parity**: triển khai phục vụ tái tạo triển khai nghiên cứu | Tệp kết quả parity (ví dụ `tests/results/lora-bundle.json`): sai khác tối đa và ngưỡng đã chốt trước | Claude |
| 3 | **Đo vận hành**: latency p50/p95 mỗi tile, RAM, kích thước image trên cùng máy | Tệp đo (ví dụ `tests/results/latency-lora.json`); ghi rõ ngưỡng NFR nào **không đạt** | Claude |
| 4 | **Đối chiếu giới hạn claim**: liệt kê giới hạn khoa học phải hiển thị cùng model (ví dụ L1–L10 của biên bản D-4) | Bảng giới hạn trong biên bản; model card và nhãn giao diện không nói vượt các giới hạn đó | Claude soạn, Trọng duyệt |
| 5 | **Quyết định**: ký/ghi nhận | Biên bản `serving-decision-<ngày>.md` theo mẫu §3, có tên, ngày, phương án chọn | **Trọng**; GVHD ghi nhận riêng |
| 6 | **Đổi mặc định** | Sửa `.env`/registry **sau** bước 5; `/healthz` trả `default_model_id`, `default_model_source`, `default_model_sha256` khớp biên bản; log khởi động có dòng `default model: …` | Trọng/Claude |
| 7 | **Kiểm sau đổi** | `make docker-test` (PG + SQLite), `make docker-e2e` với model mới làm mặc định; số case thực tế ghi vào biên bản nghiệm thu đợt | Claude |

Quay về model trước (rollback) cũng là một thay đổi mặc định: ghi một dòng vào biên bản đang hiệu lực (ngày, lý do,
model quay về) hoặc lập biên bản mới. Không cần lặp lại bước 2–3 nếu model quay về đã có biên bản.

## 2. Kiểm tra máy đọc được

- Khi khởi động, API và worker ghi một dòng log:
  `default model: <model_id> source=<registry|setting|fallback> kind=<kind> weights_sha256=<hash>`.
- `GET /healthz` trả cùng ba thông tin (`default_model_id`, `default_model_source`, `default_model_sha256`).
- `source=fallback` nghĩa là không có cờ mặc định dùng được và `DF_DEFAULT_MODEL_ID` không trỏ tới model đang phục vụ;
  trạng thái này **không** được coi là có biên bản.
- Một mặc định "khớp hồ sơ" khi `default_model_id` và `default_model_sha256` trùng với biên bản phục vụ còn hiệu lực
  mới nhất. Model registry mặc định của ETL (`m3-ext4.0-platt-v1`, baseline v0.2 đã nghiệm thu) là mặc định lịch sử,
  không cần biên bản mới khi quay về.

## 3. Mẫu biên bản `system/app/serving-decision-<ngày>.md`

```markdown
# Biên bản phục vụ model — <ngày>

| Mục | Nội dung |
| --- | --- |
| Model | `<model_id>` (kind `<kind>`) |
| Hash trọng số đăng ký | `<weights_sha256>` |
| Thay cho | `<model_id cũ>` |
| Cách bật | `DF_DEFAULT_MODEL_ID=<model_id>` trong `system/app/.env` / cờ `is_default` (chọn một) |
| Phạm vi | Cài đặt local của Trọng / bản trình bày bảo vệ / … |

## Bằng chứng
| Bước | Tệp | Kết quả |
| --- | --- | --- |
| Parity | `…json` | sai khác tối đa …; ngưỡng … |
| Latency/RAM/image | `…json` | p95 … s/tile; RAM …; image …; NFR-01 đạt/không đạt |
| Test sau đổi | `acceptance-system-<ngày>.json` | … |

## Giới hạn phải đi kèm
(liệt kê; ví dụ L1–L10 của `research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md`)

## Quyết định
- Phương án: <bật làm mặc định / chỉ tuỳ chọn / quay về>
- Người quyết định: Nguyễn Thanh Trọng — ngày …
- Ghi nhận của GVHD (TS. Hồ Quang Thái): <có, ngày … / chưa có>
- Không thay đổi: `scientific_status = development_not_gate_closure`; G3 chưa đóng.
```

## 4. Trạng thái tại ngày lập (18/11/2026)

> **Cập nhật 18/11/2026:** đã có biên bản [serving-decision-2026-11-18.md](app/serving-decision-2026-11-18.md) cho
> LoRA-D (Trọng xác nhận; GVHD đã ghi nhận theo Trọng). Đoạn dưới giữ làm lịch sử.

Cài đặt local của Trọng đang bật `DF_DEFAULT_MODEL_ID=esm2-35m-lora-d-aa4fc2b7` trong `system/app/.env` (nhật ký
[plan.md](../plan.md) ngày 17/11) nhưng **chưa có biên bản phục vụ**. Theo tiêu chí nghiệm thu 4.3, cần **một** trong
hai: (a) Trọng lập biên bản `serving-decision-<ngày>.md` cho LoRA-D theo mẫu §3, hoặc (b) quay về npz bằng cách xoá
`DF_DEFAULT_MODEL_ID` khỏi `.env`. Bằng chứng sẵn có cho (a): parity `tests/results/lora-bundle.json`, đo
`tests/results/latency-lora.json` (p95 39,1 s/tile, NFR-01 không đạt), giới hạn L1–L10 của biên bản D-4.
