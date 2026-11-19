# Plan-report §8b: trực quan hoá và bố cục — 18/11/2026

Thực hiện mục **V-1 … V-6** của [plan-report.md](../plan-report.md) theo phản hồi của Trọng ngày 18/11/2026.
Không đổi số liệu, kết quả hay giới hạn bằng chứng; không chạy huấn luyện/suy luận; không commit/push.

## 1. Đã làm

| Mục | Thay đổi |
| --- | --- |
| V-1 | Bộ biểu tượng TikZ dùng chung (`style.tex`: dữ liệu, bin, cụm, lớp model, khoảng tin cậy, khoá, refit, bia, thẻ model, màn hình, thay đổi/cố định). (a) Hình 2.5: khối *Bounds* → trục PSI 1–6 có PSI(WT) và hai mũi tên giới hạn. (b) Hình 2.9: khối *Thousands of cells…* → minh hoạ 3 nhóm và một mẫu bootstrap theo nhóm (có lặp). (c) Hình 3.1: biểu tượng cho 10 bước. (d) Hình 3.2: vẽ lại thành **ma trận câu hỏi × yếu tố** với ký hiệu "thay đổi / giữ cố định" |
| V-2 | Hình 3.3 vẽ lại bằng TikZ (`nested-evaluation.tex`), thay PDF ngày 06/11 vốn ghi "No LoRA evaluation on T"; thêm nhánh refit LoRA-D/frozen-D chấm T một lần; nhãn `fig:campaign-nested` giữ nguyên; chú thích cập nhật |
| V-3 | Hình 3.6 kiến trúc chi tiết (ngoại lệ Q-6 theo yêu cầu): ranh giới máy/Docker/mạng `internal`, trình duyệt, web (nginx), api (router + gói suy luận: registry ridge/LoRA-D, calibrator, cổng R3), worker, db (PostgreSQL/SQLite), 3 volume, ETL và thư mục nghiên cứu; **11 logo** (React, TypeScript, Vite, nginx, FastAPI, Python, NumPy, PyTorch, PostgreSQL, SQLite, Docker) từ Simple Icons 13.21.0 (CC0), chuyển sang path tuyệt đối với cung đổi thành Bézier để TikZ vẽ được (`logos.tex`, ghi hash SVG nguồn); chú thích ghi logo là nhãn hiệu của chủ sở hữu. Profile `vps` (chưa kiểm) không vẽ |
| V-4 | Các sơ đồ TikZ cũ của Part B tách ra `assets/figures/` và vẽ lại: **use case** (UML, tác nhân ngoài ranh giới, đường nối vào cạnh trong, quan hệ «uses»), **sequence job** và **sequence import** (style chung `seq-style.tex`, nhãn nền trắng), **trạng thái job/item** (Hình 3.8, nhánh vuông góc, nhãn không chồng), **CDM** (sửa quan hệ sai `model_version → project` theo khoá ngoại thật: job, analysis, tile; câu văn đi kèm sửa theo). Đầu mũi tên chung 2,3 mm |
| V-5 | Kiểm tự động float cắt đoạn bằng `pdftotext -bbox-layout`; sửa bằng cách đặt khai báo float sau đoạn bị cắt (lặp đến 0), chuyển Bảng 3.2 sang `longtable` (không phải float) với tiêu đề nhóm dính hàng (`\\*`), đặt `bottomnumber=0` trong `report/template/typography.tex`; kiểm lại thứ tự số hình theo lần dẫn đầu (sửa 2 chỗ bị đảo) |
| V-6 | Bảng 4.29 chuyển sang `tabularx`. Generator `build_app_assets.py` không còn đọc `system/openapi.yaml` đang thay đổi theo plan-system (đã 29 path/39 operation lúc 15:56) mà đọc ảnh số liệu lúc nghiệm thu `contract-at-acceptance.json` (27/37; 10/24/3), có ghi hash nguồn |

## 2. Kiểm `[ĐO 18/11/2026]`

| Kiểm | Kết quả |
| --- | --- |
| Xem trước từng hình mới/vẽ lại (`preview_figure.py`) | không overfull; đã xem ảnh từng hình đến khi hết chồng chữ |
| `make -C report all` / `make -C report check` | PASS — 168 trang một mặt, 168 hai mặt, smoke 9 |
| `check_float_references.py` | PASS — 41 hình, 64 bảng, khớp cả hai bản |
| Mực ngoài vùng chữ (lề 3,5/2 cm, 50 dpi) | chỉ trang 1–2 (khung bìa có chủ đích), cả hai bản |
| Float cắt đoạn | 0, cả hai bản. Chỗ duy nhất máy còn báo (trang 71) là phần tiếp của `longtable` Bảng 3.2 có lặp đầu bảng, không phải float |
| Thứ tự hình theo lần dẫn đầu | khớp; ngoại lệ có chủ đích: dẫn trước tới `tab:question-assessment`, `fig:transfer-strata` (từ chú thích bảng trước) và các bảng Phụ lục B |
| Khoảng cách float – lần dẫn đầu | mọi float trong 1 trang, trừ 5 bảng lệch 2–4 trang (Bảng 1.1 không đổi; 3.4, 3.5 ở mục thiết kế dữ liệu dài; 4.2, 4.6) |
| Khoảng trống > 1/3 | 13/168 trang, giống hệt hai bản; đều là trang kết thúc có chức năng |
| Abstract / Tóm tắt | mỗi bản một trang |

| PDF | SHA-256 |
| --- | --- |
| `report/build/content/content.pdf` | `ff979e80c04977f38b79c003867804d3f067481b155f9741a8f956d137a4bbda` |
| `report/build/content-twoside/content.pdf` | `bf6cfbcc6f1b0a6e80110f260de8111241fe5c2264efb33ef31333609f35d1a3` |

## 3. Ghi chú

- Script kiểm (tràn lề, float cắt đoạn, thứ tự) nằm ở scratchpad phiên làm việc, không thêm vào repo.
- `bottomnumber=0` đổi chính sách float của bản làm việc `report/` (template gốc `reportTemplate/` không đổi).
- Sơ đồ kiến trúc vẫn cần cập nhật lại khi plan-system thêm thành phần (plan-report 6.2).
