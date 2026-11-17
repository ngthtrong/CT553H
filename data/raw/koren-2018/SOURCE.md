# Koren 2018 — bản S4 tại máy Windows, 16/11/2026

Người dùng cung cấp lại `NIHMS967427-supplement-11.xlsx` tại
`data/raw/koren-2018-probe/`; sao sang thư mục này, giữ nguyên bản nguồn.

- Bài: Koren et al. 2018, DOI 10.1016/j.cell.2018.04.028, PMC6003881.
- Bảng: Table S4, saturation mutagenesis của 9 substrate.
- Kích thước: 169738 byte.
- SHA-256: c96973f2b2781b35a822527fa875e38df82f75da9ac327668d1d10114fdbcbeb.
- Khớp chính xác bản đã audit ngày 22/10; không tải lại qua mạng.
- Theo sổ nguồn repo: chỉ dùng nội bộ; không đưa bảng gốc/cell-level derivative
  lên Git, app công khai hoặc phụ lục. Chỉ xuất metric tổng hợp có ghi nguồn.
- Parser hiện tại dùng cached XML values, không chạy macro/công thức/mã nguồn.
- Phạm vi mới: rank-only, không nhập vào training/calibration của Zhang.

Chi tiết audit cũ: research/koren-s4-audit-2026-10-22/README.md.
Protocol bổ sung: research/lora-refit-transfer-2026-11-16/KOREN-PROTOCOL.md.
