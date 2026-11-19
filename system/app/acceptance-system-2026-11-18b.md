# Biên bản nghiệm thu — plan-system đợt 1 (lượt 2) — 18/11/2026

Số liệu máy đọc: [acceptance-system-2026-11-18b.json](acceptance-system-2026-11-18b.json). Lượt 1:
[acceptance-system-2026-11-18.md](acceptance-system-2026-11-18.md) (giữ nguyên). Biên bản nghiệm thu **phần mềm**;
không đổi `scientific_status` (`development_not_gate_closure`), không đóng G3, không đổi model phục vụ.

Máy đo: WSL2 Ubuntu 24.04, AMD Ryzen 5 5500U (12 luồng), 7,4 GiB RAM, Docker Engine cùng VM. Code chưa commit.
Không có migration mới (head vẫn `0005`).

## 1. Kết quả kiểm thử `[ĐO]`

| Nhóm | Kết quả |
| --- | --- |
| Backend container, PostgreSQL 16 | **314 pass**, 18 skip (thêm 4 skip: test sao lưu chỉ chạy SQLite) |
| Backend container, SQLite | **332 pass** |
| Backend host nhanh (sau sửa CSP) | 317 pass, 1 skip, 14 deselected |
| Tĩnh | ruff (thêm `ops/`), mypy 50 tệp, contract, `tsc`, ESLint, `check:api`: sạch |
| Vitest | **194/194** (16 tệp) |
| Playwright mock | **34/34** (thêm VIZ-03 × 2 theme, VIZ-04 360 px, biểu đồ + axe trong UC-09) |
| E2E thật, LoRA-D mặc định | **13 pass**, 1 skip (NF-06 có chủ đích). Lần đầu `RPT real` hỏng: Chromium cảnh báo `frame-ancestors` bị bỏ qua trong `<meta>`; meta nay không có directive này (header HTTP vẫn giữ); chạy lại đạt |
| E2E thật, npz mặc định | **14/14** |

Sau lượt npz, stack trở lại cấu hình `.env` (LoRA-D, `default_model_source = setting`).

## 2. Theo mục

| Mục | Tiêu chí | Bằng chứng |
| --- | --- | --- |
| 2.1 Footprint protein | Giá trị = tính lại từ ô từng tile (< 1e-9); không trộn vùng chồng lấn; e2e + axe; 360 px không cuộn ngang | VIZ-01…04 |
| 2.3 Biểu đồ so sánh | Điểm khớp bảng matched; endpoint không tương thích không vẽ calibration và nêu lý do; axe | CMP-04/05; e2e UC-09 |
| 3.5 Báo cáo | Số khớp snapshot; đủ cảnh báo, ghi công, hash model; không tài nguyên ngoài | RPT-01…03; trang mở trong Chromium không vi phạm CSP, không request khác |
| 4.1 Sao lưu/khôi phục | Sao lưu → xoá volume → khôi phục khớp; manifest hỏng bị từ chối; không ghi đè khi chưa xác nhận; ghi thời gian/dung lượng | `tests/test_backup.py`; [backup-roundtrip.json](tests/results/backup-roundtrip.json): sao lưu 15,4 s, khôi phục 29,3 s, ≈ 63 MB, checksum CSDL và hash file giống hệt |

Vòng Docker của 4.1 làm trên project Compose tạm `df-ops01` khôi phục từ bản sao lưu stack thật; CSDL thật **không**
bị ghi đè. Bản sao lưu thật để lại ở `.data/backups/ops01-20261118T080221Z/` (chứa dữ liệu người dùng, ngoài git).

## 3. Chưa kiểm

- Kiểm tay accessibility (4.6).
- 4.3: biên bản phục vụ LoRA-D chờ Trọng xác nhận.
- In báo cáo ra PDF bằng tay trên từng trình duyệt (có CSS in, chưa xem bằng mắt).
- Khôi phục đè lên stack thật (cố ý chỉ làm trên project tạm).
