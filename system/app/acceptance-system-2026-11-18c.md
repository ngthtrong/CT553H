# Biên bản nghiệm thu — đóng đợt 1, đợt 2, đầu đợt 3 — 18/11/2026

Số liệu máy đọc: [acceptance-system-2026-11-18c.json](acceptance-system-2026-11-18c.json). Biên bản trước giữ nguyên
([lượt 1](acceptance-system-2026-11-18.md), [lượt 2](acceptance-system-2026-11-18b.md)). Nghiệm thu **phần mềm**; không
đổi `scientific_status`, không đóng G3. Code chưa commit. Migration mới `0006`–`0008`, mỗi lần nâng có sao lưu trước bằng
`make backup`.

## 1. Kết quả kiểm thử `[ĐO]`

| Nhóm | Kết quả |
| --- | --- |
| Backend container, PostgreSQL 16 | **344 pass**, 19 skip |
| Backend container, SQLite | **363 pass** |
| Backend host nhanh | 347 pass, 1 skip, 15 deselected |
| Tĩnh | ruff, mypy (58 tệp), contract, `tsc`, ESLint, `check:api`: sạch |
| Vitest | **211/211** (24 tệp) |
| Playwright mock | 40/41 ở lượt đầy đủ; ca hỏng (UX-01 tối 360 px) do thanh tiêu đề dính khi chụp toàn trang → cố định tĩnh lúc chụp, tạo lại 24 ảnh chuẩn, 4/4 hai lần liên tiếp |
| E2E thật, LoRA-D mặc định | **14 pass**, 1 skip (NF-06) |
| E2E thật, npz mặc định | **15/15** |

## 2. Theo mục

| Mục | Kết quả |
| --- | --- |
| 4.3 | Biên bản phục vụ LoRA-D có hiệu lực (Trọng xác nhận 18/11; GVHD đã ghi nhận theo Trọng) |
| 4.6 | UX-01 hồi quy ảnh (24 ảnh), chụp lại `docs/screenshots/` (+ 3 màn mới), mẫu kiểm tay `a11y-manual-2026-11-18.md`; **kiểm tay chưa làm** |
| 1.4 | Docker PERF-01: p95 LoRA-D 39,1 s → **28,1 s/tile** (6 luồng + gộp LoRA, sai khác ≤ 5,0e-6); mục tiêu ≤ 15 s **không đạt**. Lần đo đầu (p50 23,5 ms) vô hiệu vì script đo trúng cache — đã sửa script và đo lại |
| 2.2 | So sánh hai model: CMP-01…03, e2e mock + axe + 360 px, e2e thật |
| 2.6 | Ứng viên kiểm chứng: SUG-01…03 |
| 3.3 | Nhiều protein một job: BATCH-10 |
| 3.4 | CLI, client, notebook: CLI-01…03 |
| 4.2 | Trang Admin + heartbeat: OPS-04…06; hoạt động qua nginx trên Docker |
| 4.5 | Ưu tiên + giới hạn item chạy: BATCH-11; 3 container worker thật: 36 item, 15/13/8, không trùng |
| 5.1 / 5.4 | Chú giải + hướng dẫn lần đầu (UX-03/04); chế độ trình bày (UX-10) |
| 1.6 | Biên bản đề xuất chính sách cổng (khuyến nghị giữ R3); **chờ quyết định**, không triển khai |
| 4.4 | Đồng thuận theo thời gian: CMP-06/07 |
| 5.2 | Phím tắt có công tắc tắt, ghim, nhớ bộ lọc theo id: UX-05/06 |

## 3. Chưa kiểm

- Kiểm tay accessibility; quyết định 1.6; các mục đợt 3 còn lại (2.4, 2.5, 3.1, 3.2, 3.6, 5.3).
- 1.4 bước c/d (tuỳ chọn); `.env` vẫn 4 luồng, không gộp LoRA.
- Ảnh trong `report/assets/screenshots/` chưa cập nhật các màn mới (nhánh 3).
