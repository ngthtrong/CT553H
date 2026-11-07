# Tài nguyên trình bày

`../logo-ctu.png` là logo dùng chung trên hai trang bìa, giữ nguyên byte từ
bộ template gốc.

Đặt hình của luận văn vào `figures/`, sơ đồ vào `diagrams/`; hai thư mục đã
được cấu hình trong `template/packages.tex`. Hình PDF/PNG/JPG dùng được
trực tiếp với XeLaTeX. Xuất SVG hoặc draw.io sang PDF trước khi chèn.

Tài sản bổ sung 06/11/2026:

- [Campaign diagrams](diagrams/campaign-2026-11-06/README.md): 2 sơ đồ `.drawio` chỉnh sửa được, PDF vector có nhúng nguồn và PNG.
- [Generator kết quả campaign](ch4/build_campaign_assets.py): 12 bảng, 3 đồ thị PDF/PNG và macro số từ JSON audit; không fit lại mô hình.
- [Nguồn audit](../../research/output-review-2026-11-06/README.md) và [hồ sơ kiểm PDF](../current-state-validation-2026-11-06.md).

Tài sản bổ sung 07/11/2026:

- [Generator ưu tiên mutation](ch4/build_prioritization_assets.py): 6 bảng, macro số và đồ thị budget/recall PDF vector + PNG từ replay OOF đã kiểm; không tính lại model hoặc bootstrap.
- [Manifest tài sản](ch4/priority-assets.json) pin SHA-256 input/output; provenance trong comment LaTeX, không in đường dẫn làm dẫn chứng.
- [Nguồn kết quả](../../research/oof-prioritization-2026-11-07/README.md) và [kiểm PDF](../prioritization-validation-2026-11-07.md).
