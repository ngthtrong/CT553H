# Docker và LoRA-D — biên bản kiểm 17/11/2026

Phạm vi: chuyển toàn bộ frontend/backend sang Docker theo yêu cầu ngày 17/11 và mục 2.12 (WP10) của
[plan.md](../../plan.md). Số liệu máy đọc được ở [docker-validation-2026-11-17.json](docker-validation-2026-11-17.json).
Trạng thái khoa học giữ `development_not_gate_closure`; **model phục vụ mặc định không đổi** (`m3-ext4.0-platt-v1`).
Biên bản này không thay [acceptance-2026-11-17.md](acceptance-2026-11-17.md).

Máy: WSL2 Ubuntu 24.04, Ryzen 5 5500U (12 luồng), 7,4 GB RAM, Docker Engine 29.8.1, Compose 5.5.1.

## 1. Kiến trúc container

| Container | Image | Vai trò |
| --- | --- | --- |
| `db` | `postgres:16-alpine` | CSDL, volume `dbdata`, không mở cổng ra host |
| `api` | `degron-footprint/backend:<WITH_LORA>` (target `runtime`, 399 MB / 1,77 GB khi có torch) | FastAPI, migrate khi khởi động |
| `worker` | cùng image, `python -m api.worker` | hàng đợi job bền (A-2) |
| `web` | `degron-footprint/web` (nginx-unprivileged, 77 MB) | giao diện đã build, `127.0.0.1:8080`, proxy `/v1`, `/healthz` |
| `etl` (profile `tools`) | image backend | nạp dữ liệu từ checkout gắn chỉ-đọc ở `/topic` |
| dev: `api`/`worker`/`web-dev`/`test` | target `dev` | mã nguồn bind-mount, Vite `:5173`, API `--reload` `:8000`, PG `:55433` |

Lệnh: `make docker-env`, `make docker-etl`, `make docker-up`, `make docker-dev`, `make docker-test`, `make docker-e2e`
(chi tiết [INSTALL.md](INSTALL.md) §0).

## 2. Kết quả `[ĐO]`

| Kiểm | Kết quả |
| --- | --- |
| ETL trong Docker, ClinVar `in-tiles` | 552,3 s; 2.933.851 dòng tham chiếu; 2.338.863 biến thể ClinVar; LoRA-D đăng ký frozen, không mặc định |
| Suite backend trong container dev, PostgreSQL 16 | **290 pass, 13 skip, 0 fail** (182,9 s) — đóng mục "chạy lại PG" của 2.9 |
| Suite backend trong container dev, SQLite + realdata | **302 pass, 1 skip** (parity LoRA cần torch) |
| Test LoRA với PyTorch (`.venv-lora`) | **9/9** (lượt chạy lại đầu trượt vì giả định sai trong test: chuỗi e2e "typed" cũng thuộc W; đã sửa assertion) |
| Vitest / tsc / eslint (host) | 172/172, sạch, sạch |
| E2E backend thật qua `web` :8080 | **12/12** (hai lượt) |
| E2E backend thật qua Vite dev :5173 | lượt đầu 11/12 (lỗi quyền volume, §4) → sửa → **12/12** |
| Hot reload API dev | `WatchFiles detected changes … Reloading` |
| Header bảo mật qua nginx | CSP, nosniff, Referrer-Policy, X-Frame-Options có mặt |
| Ghi cross-site | Origin lạ → 403; Origin `:8080` → 201 |
| Giới hạn body | multipart 2,3 MB tới được API; 12 MB → 413 tại nginx |
| RAM khi rảnh | api 84,6 MiB, worker 61,0, web 12,0, db 74,9 |

## 3. LoRA-D (mục 2.12) `[ĐO]`

| Kiểm | Kết quả | File |
| --- | --- | --- |
| Parity khác runtime: cài đặt nghiên cứu, 32 dòng W, CUDA (Windows) → CPU (WSL) | lệch tối đa **3,0e-6** (atol 1e-5) | `tests/results/lora-bundle.json` |
| Serving (`degron_footprint/lora.py`) ↔ nghiên cứu (`degron_v3`), 2 tile × 532 | **0,0** (raw từng seed, ensemble, xác suất) | như trên |
| API trong container `WITH_LORA=1` qua nginx ↔ fixture nghiên cứu | **0,0** | `tests/results/latency-lora.json` |
| Latency mỗi tile (10 tile, tuần tự, 4 luồng CPU) | LoRA-D p50 37,7 s / p95 **39,1 s**; npz p95 20 ms | như trên |
| NFR-01 (300 ms p95, đề xuất) | LoRA-D **không đạt**; npz đạt | như trên |
| RAM container api sau khi chạy LoRA-D | 514,5 MiB | như trên |
| Không có torch | LoRA-D báo không nạp, `/healthz` vẫn `ok`, mặc định npz | log api |
| `DF_DEFAULT_MODEL_ID` | chuyển qua lại LoRA-D ↔ npz; `/healthz`, `/v1/models` báo đúng mặc định thực tế | — |
| `calibrator: iso` với LoRA-D | 422 `INVALID_REQUEST`, field `calibrator` | `tests/test_lora.py` |

`[DIỄN GIẢI]` Cả hai tile của fixture đều là peptide W (đã train). Parity chứng minh hai cài đặt cho cùng số, không nói
gì về độ chính xác. Bằng chứng độ chính xác của
LoRA-D vẫn là đánh giá hồi cứu trên nguồn T đã từng xem (`research/lora-refit-transfer-2026-11-16/results.json`), trong
đó ở tầng PSI(WT) > 5 dự đoán zero tốt hơn. Với ~39 s/tile trên CPU, LoRA-D phù hợp chấm tile đơn hoặc job nhỏ, không
phù hợp quét protein dài.

## 4. Lỗi phát hiện khi chạy thật và đã sửa

1. `web` publish cổng 80 của container trong khi nginx-unprivileged nghe 8080.
2. nginx gửi `Host` không kèm cổng (`$host`) → kiểm tra same-origin (SEC-03) sẽ chặn ghi từ `:8080`; đổi `$http_host`.
3. `client_max_body_size 8k` cho mọi `/v1/` → chặn lưu phân tích (256 KiB) và import (10 MiB); nay 320 KiB và 11 MiB riêng cho upload.
4. Thiếu service `worker` → job không bao giờ chạy trong Docker.
5. Thiếu volume cho file import (`workspace`).
6. `Settings` tự đọc `.env` trong thư mục hiện hành; `.env` giờ là file của Compose (`DF_TRUST_PROXY=true`) → rò vào tiến trình chạy trên host, làm trượt test SEC-03. Bỏ đọc ngầm.
7. Container dev (uid host) không ghi được volume do user runtime (10001) tạo → nhóm 0 + setgid + umask 002.
8. Cảnh báo `TRAINING_PEPTIDE` dùng 176 peptide train của model npz cho mọi model → LoRA-D mang danh sách 235 tile W riêng.

## 5. Chưa kiểm

- Kiểm tay bàn phím/trình đọc màn hình (A11Y) — cần người thực hiện.
- Profile `vps` (Caddy/TLS); Docker Desktop trên Windows/macOS (chỉ chạy Docker Engine trong WSL2).
- Quyết định phục vụ LoRA-D làm mặc định — việc riêng của Trọng/GVHD. D-4 đã chốt 17/11 (phương án A, [biên bản](../../research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md)) và ghi rõ không đổi model phục vụ; biên bản này giữ đúng điều đó.

## 6. Lượt kiểm tối 17/11: LoRA-D làm mặc định và giao diện Roboto `[ĐO]`

Trọng đổi `.env` của máy này sang `WITH_LORA=1`, `DF_DEFAULT_MODEL_ID=esm2-35m-lora-d-aa4fc2b7`. Đây là cấu hình triển
khai local do Trọng chọn; chưa có biên bản quyết định phục vụ/ghi nhận GVHD, `scientific_status` không đổi. Đặt lại
`DF_DEFAULT_MODEL_ID=` (rỗng) và `make docker-up` để quay về model npz.

| Kiểm | Kết quả |
| --- | --- |
| `/healthz`, `/v1/models`, trang Model | mặc định `esm2-35m-lora-d-aa4fc2b7` (`torch_lora`); `api`/`worker` chạy `backend:1`, log không lỗi |
| Predict không ghi `model_id` (như giao diện) | LoRA-D; ~41 s; 532 ô; khớp fixture nghiên cứu 0,0; cảnh báo `TRAINING_PEPTIDE` cho tile W |
| Tile ngoài miền (A6NMZ7/7) | 422 `OUT_OF_DOMAIN` |
| Model npz chọn tường minh / `calibrator: iso` | 200 / 422 |
| Job 2 peptide qua `worker` | `completed`, 2/2, 73,7 s |
| Giao diện Chromium | màn "Scoring…" có Cancel khi chờ ~34 s, rồi ma trận 28×20, provenance và nhãn bằng chứng của LoRA-D |
| E2E real (`make docker-e2e`) | **11 pass, 1 skip** (NF-06 bỏ qua có chủ đích khi mặc định là LoRA-D, để không ghi đè số đo npz). Lượt đầu 10 pass/1 fail do test ghi cứng nhãn bằng chứng của npz → test nay đọc nhãn từ model card |

Lỗi tìm thêm và đã sửa: bản build nhúng vài subset font thành `data:` URI bị CSP chặn (4 lỗi console) →
`build.assetsInlineLimit: 0`; sau sửa 0 lỗi. Giao diện được rà và đổi sang Roboto/Roboto Mono cùng ngày:
[`../design/ui-ux-pro-max-2026-11-17/README.md`](../design/ui-ux-pro-max-2026-11-17/README.md) (Vitest 172/172, e2e mock
28/28 gồm axe 4 độ rộng × 2 theme).
