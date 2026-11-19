# Biên bản nghiệm thu nhánh 2 — ứng dụng v0.2 local

Ngày **17/11/2026**. WP11.12 của [kế hoạch triển khai](../implementation-plan-2026-11-16.md). Số liệu máy đọc:
[acceptance-2026-11-17.json](acceptance-2026-11-17.json); mọi con số dưới đây trỏ tới một file trong
[tests/results/](tests/results/). Trạng thái khoa học giữ `development_not_gate_closure`: biên bản này nghiệm thu
**phần mềm**, không xác nhận mô hình, không đóng G2/G3 và không gọi so sánh với dữ liệu import là kiểm chứng độc lập.

Máy đo: WSL2 Ubuntu 24.04, AMD Ryzen 5 5500U (12 luồng), 7,4 GiB RAM, Python 3.12.3, Node 24.22.3, Playwright 1.64.1.
Code chưa commit tại thời điểm đo.

## 1. Kết quả kiểm thử `[ĐO]`

| Nhóm | Lệnh | Kết quả |
| --- | --- | --- |
| Backend (SQLite) | `make test` | **292 pass**, 1 skip (test PG khi không có `DF_TEST_PG_URL`); coverage **96%** (mục tiêu đề xuất ≥ 85%) |
| Backend (PostgreSQL 16) | `make test-pg` | 273 pass, 12 skip (`sqlite_only`/`realdata`) — **chạy ngày 16/11, trước** migration 0004, chặn SEC-03 và sửa race worker ngày 17/11; cần chạy lại khi bật Docker |
| Contract | `make contract` + schemathesis | Hợp lệ; 24/24 operation `implemented`, 0 `planned` |
| Frontend | `npm run typecheck lint check:api test build` | Vitest **171/171**; các bước khác pass |
| E2E mock | `npm run e2e` | **28/28** — luồng baseline, 360 px, hệ thiết kế (axe 2 theme × 4 độ rộng), luồng workspace UC-01/03/05/08/09/10 + bàn phím + axe, ma trận Chromium/Firefox/WebKit × 360/768/1280/1440 |
| E2E backend thật | `E2E_REAL=1` (dev-api + worker nhúng) | **14/14**, gồm luồng workspace đầy đủ; NF-06 chạy riêng (pass) |

## 2. Phi chức năng `[ĐO]` (ngưỡng SRS là đề xuất)

| ID | Đo được | Ngưỡng đề xuất | Nguồn |
| --- | --- | --- | --- |
| NF-01 | p95 9,48 ms (chuỗi gõ) / 11,95 ms (tile UniProt) | ≤ 300 ms | `tests/results/latency.json` |
| NF-02 | p95 9,72 ms (protein 1.028 aa) | ≤ 200 ms | như trên |
| NF-03 | RSS API 111,9 MB sau tải | ≤ 512 MB | như trên |
| NF-06 | click → heatmap p95 628 ms (Chromium, backend thật, 20 lần) | ≤ 1,5 s | `tests/results/nf06-real.json` |
| NF-07 | 100 peptide 4,94 s; protein Q8NF91 8.797 aa = 382 tile 20,73 s (54,3 ms/tile); export manifest 41,3 MB trong 3,25 s; trang 200 item 21,4 ms; huỷ 0,11 s; import 100.000 dòng xem trước 5,01 s; DB tăng 96,4 MB; RSS API+worker 437 MB | ghi nhận | `tests/results/workspace-performance.json` |

## 3. Triển khai và phục hồi `[ĐO]`

- **DEP-01** — cài sạch từ cây làm việc (340 file) vào thư mục rỗng: venv mới 35 s, migrate 2 s, ETL `degron-only` 108 s,
  `npm ci` 20 s, build 10 s, tổng 179 s; `healthz` ok; UC-01/03/04/05/06/07/08/09/10 chạy qua HTTP
  (`tests/results/dep01-clean-install.json`). Giới hạn: thư mục dữ liệu nghiên cứu (`data/`, ngoài git) đọc từ checkout này.
- **DEP-02** — `SIGKILL` API + worker khi job protein đang ở 60/382 tile, khởi động lại sau 1,44 s: job hoàn tất
  382/382, đúng 382 analysis không trùng, analysis đã lưu trước đó mở lại y hệt (`tests/results/dep02-restart.json`).

## 4. Bảo mật

- SEC-01: canary không xuất hiện trong log/URL/lỗi (test); log API của lượt e2e thật có 0 chuỗi sinh học.
- SEC-02: fuzz trường, chuỗi truy vấn, đường dẫn workspace (UUID chuẩn, chặn symlink), công thức CSV bị vô hiệu khi export.
- SEC-03: bind `127.0.0.1`; header CSP/nosniff/referrer; **ghi từ site khác → 403**, body không phải JSON → 415 (mới 17/11).
- SEC-05: `npm audit` production 0; dev 7 moderate (minimatch qua typescript-eslint); `pip-audit` runtime 0.

## 5. Lỗi phát hiện trong nghiệm thu và đã sửa

1. `max(clinvar_file_date)` quét 2,34 triệu dòng mỗi tile → migration `0004` (324 → 54 ms/tile).
2. Race worker/huỷ trên SQLite làm job thành `partial` thay vì `cancelled` → test tái hiện (đỏ 3/3 trên code cũ) và sửa.
3. API nhận lệnh ghi từ site khác (CSRF với dịch vụ local) → chặn 403/415.
4. Trang Model tràn ngang ở 360 px; bảng ẩn của footprint gây tràn; dialog đặt focus vào nút đóng.
5. `offset` cực lớn gây HTTP 500; contract thiếu mã 400 (do schemathesis phát hiện).

## 6. Còn mở

- A11Y-03: kiểm tay bằng bàn phím và trình đọc màn hình do **người** thực hiện (đã có luồng bàn phím tự động).
- Chạy lại bộ test PostgreSQL sau thay đổi 17/11 (cần Docker Desktop bật WSL integration).
- WP10 (LoRA-D phục vụ) chờ nhánh 1 mục 1.13; WP12 (ảnh chụp, kịch bản demo, hướng dẫn cài).
- NF-01…07 đo trên máy tác giả, chưa đo trên máy tham chiếu.
