# Biên bản nghiệm thu — plan-system đợt 1 (lượt 1) — 18/11/2026

Số liệu máy đọc: [acceptance-system-2026-11-18.json](acceptance-system-2026-11-18.json). Biên bản này nghiệm thu
**phần mềm** cho các mục đã làm của đợt 1 trong [plan-system.md](../../plan-system.md); không xác nhận mô hình, không
đóng G3, không đổi `scientific_status` (`development_not_gate_closure`). Biên bản 17/11 giữ nguyên.

Máy đo: WSL2 Ubuntu 24.04, AMD Ryzen 5 5500U (12 luồng), 7,4 GiB RAM, Docker Engine cùng VM. Code chưa commit.

## 1. Kết quả kiểm thử `[ĐO]`

| Nhóm | Lệnh | Kết quả |
| --- | --- | --- |
| Backend, container, PostgreSQL 16 | `make docker-test` | **306 pass**, 14 skip, 0 fail |
| Backend, container, SQLite | `make docker-test DF_TEST_BACKEND=sqlite` | **320 pass**, 0 fail |
| Backend, host (nhanh) | `make test-fast` | 305 pass, 1 skip, 14 deselected |
| Tĩnh | ruff, mypy, `make contract`, `tsc`, ESLint, `check:api` | đều sạch |
| Frontend | `npx vitest run` | **186/186** (14 tệp) |
| E2E mock | `npx playwright test` | **31/31** (gồm MSEL-02 mock, UNC-04 × 2 theme) |
| E2E backend thật, LoRA-D mặc định | `make docker-e2e` | **12 pass**, 1 skip (NF-06 bỏ qua có chủ đích khi model mặc định chậm) |
| E2E backend thật, npz mặc định | `DF_DEFAULT_MODEL_ID= docker compose up -d api worker` rồi `make docker-e2e` | **13/13**. Lần đầu MSEL-04 gặp giới hạn tần suất của chính dịch vụ (429) sau NF-06; spec nay chờ `Retry-After`, chạy lại 13/13 |

Sau lượt npz, stack đã trở lại cấu hình `.env` (LoRA-D mặc định, `default_model_source = setting`).

## 2. Theo mục `[ĐO]`

| Mục | Tiêu chí nghiệm thu | Bằng chứng |
| --- | --- | --- |
| 1.1 | Một tile chấm bằng cả hai model từ giao diện, không sửa `.env`; snapshot lưu đúng model đã chọn | MSEL-04 pass với **cả hai** model mặc định; MSEL-01…03 |
| 1.2 | Mở/xuất lại cùng tile LoRA-D lần hai < 1 s | `tests/results/cache-lora.json`: lần đầu ≥ 33,1 s, lần hai và export ≤ **30,2 ms**, kết quả bằng nhau; CACHE-01…04 |
| 1.3 | Snapshot cũ (không có SD) vẫn mở được (FR-22) | Phân tích lưu 17/11 (`d3042938…`) trên CSDL Docker: GET 200, export CSV 200, không có trường SD; UNC-01…04 |
| 1.5 | Cảnh báo `TRAINING_PEPTIDE` cho chuỗi gõ tay với cả hai model | DOM-02 trong cả hai backend container |
| 1.7 | ETA hợp lệ; thông báo chỉ khi người dùng cho phép; nội dung không chứa chuỗi | BATCH-08, BATCH-09 |
| 4.3 | Cấu hình hiện tại có **một** biên bản tương ứng | Log khởi động và `/healthz` có nguồn + hash (OPS-07). Biên bản [serving-decision-2026-11-18.md](serving-decision-2026-11-18.md) là **nháp chờ Trọng xác nhận** ⇒ 4.3 chưa đạt |

## 3. Migration `0005` trên dữ liệu thật

- CSDL PostgreSQL của Docker: sao lưu `pg_dump -Fc` trước khi nâng (`.data/backup/docker-pg-2026-11-18-pre0005.dump`,
  sha256 `5fb47049…`, 20 bảng dữ liệu), sau đó API áp `0005` lúc khởi động.
- `.data/dev.db` (dùng bởi `make dev-api`): sao lưu `.data/backup/dev-2026-11-18-pre0005.db` (sha256 `be7c5f88…`),
  nâng lên `0005`, `PRAGMA integrity_check = ok`.
- Lỗi phát hiện: `test_whole_protein_windows_match_the_reference_tiles` dùng bản sao `dev.db` mà không migrate (lộ ra
  trong container vì test `slow` bị bỏ qua ở `test-fast`). Đã sửa test để nâng bản sao lên head trước.

## 4. Chưa kiểm

- Kiểm tay accessibility (4.6); các mục 2.1, 2.3, 3.5, 4.1, 4.6 chưa bắt đầu.
- Quyết định phục vụ LoRA-D: chờ Trọng ghi tên/ngày; GVHD chưa ghi nhận.
- Latency chỉ đo trên máy tác giả; ETA giả định một worker.
