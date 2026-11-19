# Hoàn thiện nhánh 3 và cập nhật Chương 3/4 theo ứng dụng v0.2 — 18/11/2026

Lượt làm theo yêu cầu của Trọng ngày 17–18/11/2026: thực hiện các việc còn lại của nhánh 3
(trừ metadata ngày bảo vệ/hội đồng, chờ D-2), và đưa danh sách tính năng A–D vào Chương 3/4,
ảnh chụp từng tính năng vào Phụ lục A. Biên bản này **bổ sung**, không thay
[review-validation-2026-11-17.md](review-validation-2026-11-17.md) và
[title-sync-validation-2026-11-17.md](title-sync-validation-2026-11-17.md).

Trạng thái khoa học giữ `development_not_gate_closure`. Không chạy huấn luyện/suy luận nghiên cứu,
không sửa campaign, không đổi model phục vụ, không đóng G3, không commit/push. Build PDF không đồng
nghĩa nghiệm thu nghiên cứu.

## 1. Nội dung đã sửa

| Phần | Thay đổi |
| --- | --- |
| Abstract / Tóm tắt | Bỏ câu đã **sai** "LoRA has not been tested there" / "LoRA chưa được đánh giá ở đây" và "workflows remain incomplete"; thêm kết quả T của LoRA-D, kết quả âm ở miền PSI ổn định nhất, quyết định D-4 (GVHD chưa ghi nhận), ứng dụng đã nghiệm thu với LoRA-D tuỳ chọn. Mốc 07/11 → 17/11. Rút gọn để mỗi bản đúng **một trang** (bỏ ba câu phụ đã có trong Kết luận) |
| Chương 1 | Mục *Contributions Achieved and Still Expected*: mốc 17/11, thêm refit/T, D-4 với L1–L10, ứng dụng v0.2 |
| Chương 3 | §Functional Overview viết lại theo nhóm **A. Mutation analysis / B. Reference data and context / C. Workspace**, kèm **Bảng 3.1** ánh xạ tính năng ↔ UC ↔ FR (đối chiếu `system/srs.md`) và bốn giới hạn chung. §Method and Model Design: hai model phục vụ thay cho "refit/export còn thiếu". §Domain integration: R3 đã tích hợp (`gate-r3-v1`). §Local Execution View (`sec:local-execution`): 4 container + ETL, chỉ web mở cổng loopback, PG16/SQLite, hai model đổi bằng cấu hình, cấu hình mặc định LoRA-D của Trọng **không** phải quyết định phục vụ, bảo mật/riêng tư, giao diện. Sửa lỗi macro: "100 peptide" đang dùng nhầm số giây import 100.000 dòng (5,01 s) → 4,94 s |
| Chương 4 §Software Acceptance | Số liệu theo hai biên bản cùng ngày: backend 303 case (PG 290 pass/13 skip, SQLite 302 pass/1 skip trong container), LoRA parity 9/9, Vitest 172, e2e mock 28, e2e thật 12/12 (prod container); lượt chạy lại sau khi đặt LoRA-D mặc định 11 pass + 1 skip có chủ đích (ghi rõ chỉ có trong phần văn bản của biên bản). Bỏ câu "PostgreSQL chưa chạy lại". Thêm chi phí LoRA-D: p95 39,1 s/tile, image 1,77 GB so với 399 MB, API 514,5 MiB, parity 3,0e-6. Hợp đồng API: 10 baseline + 24 mới + 3 legacy, 0 planned |
| Chương 4 phần kế hoạch test | Bảng kịch bản nghiệm thu: bỏ "All are pending / no execution result claimed", thêm cột *Executed in*; sửa Functions Under Test, Approach, Deliverables, Test Activities, Risks, mục Future Work cho khớp việc đã chạy |
| Mục transfer-refit, Kết luận | Ghi cấu hình mặc định LoRA-D local của Trọng là cấu hình, chưa có biên bản phục vụ/GVHD; số test mới; bỏ "repeat of the PostgreSQL run remains outstanding" |
| Phụ lục A | Viết lại cài đặt (container và host, lệnh đã chạy), hướng dẫn sử dụng 7 bước, **5 hình mới A.1–A.5** (10 màn hình chưa có ở Chương 3). Sửa lỗi `\nolinkurl` làm mất dấu cách trong lệnh (cả lỗi cũ `./run-local.cmd--hours2`). Đoạn campaign đổi sang thì quá khứ và trỏ campaign refit riêng |
| Ảnh chụp | Chụp lại toàn bộ 14 màn hình × 2 theme bằng `e2e/screenshots.spec.ts` (font **Roboto**, thay bản Fira) trên **bản sao** `dev.db` ở scratchpad với model npz; DB thật và container không bị ghi. 14 ảnh light chép vào `report/assets/screenshots/` (4 hình Chương 3 cũng được thay) |
| 3.6 Cân bảng | Gộp 4 cặp bảng mỏng thành bảng hai phần (a)/(b), **không đổi dữ liệu sinh ra**: g2-paired + g2-seeds, cal-metrics + cal-verdict, partb + partb-verdict, campaign-core + campaign-paired. 67 → **63 bảng** |

Ghi chú khi đọc ảnh: dữ liệu import trong ảnh so sánh/dataset là **giá trị minh hoạ suy từ dự đoán**
(Spearman 1,000 là hệ quả) — chú thích Hình 3.x và A.5 ghi rõ. Trang Sources của app còn câu về share
link (FR-20 đã bỏ); chú thích A.4 ghi rõ, app chưa sửa.

## 2. Nguồn số liệu mới

`report/assets/ch4/build_app_assets.py` nay đọc thêm `system/app/docker-validation-2026-11-17.json`
(và kiểm `scientific_status`), đếm `x-implementation-status` trong `system/openapi.yaml` (dừng nếu còn
operation `planned`/không đánh dấu). Macro mới không chứa chữ số trong tên.

| Tệp | SHA-256 |
| --- | --- |
| `system/app/docker-validation-2026-11-17.json` | `78ff9329972d4f0a7324558c27133a13175281da9c140eea881b7081e2a22e5f` |
| `system/app/acceptance-2026-11-17.json` | `50df68bf2cb791afe00871b8e64de8255360c9827bf9472a737450232a38a682` |
| `report/assets/ch4/build_app_assets.py` | `17e184464fc28f8bcaf955db243121e6650b5091a6cf141de27b647894e861fe` |
| `report/assets/ch4/app-numbers.tex` | `b264685bfa386b48228f6946bbc3172974ced0f7eb7b7be88b522ffd8e1f0a89` |
| `report/assets/ch4/tab-app-tests.tex` | `5ca0496d5b7b0786dfef9913f0e67b1f04f43499f69b4de16f1d139b418bcbf9` |

## 3. Kiểm `[ĐO 18/11/2026]`

| Kiểm | Kết quả |
| --- | --- |
| `make -C report all` | PASS (exit 0), references resolved |
| `make -C report check` | PASS — 157 trang một mặt, 157 hai mặt, smoke 9; A4; phông nhúng |
| `scripts/check_float_references.py` | PASS — **28 hình, 63 bảng**, khớp cả hai bản |
| Abstract / Tóm tắt | mỗi bản đúng một trang (v, vi) |
| Khoảng trống (50 dpi, cả hai bản, ngưỡng 1/3 vùng nội dung) | 12/157 trang, giống hệt ở hai bản; đều là trang kết thúc có chức năng: 5–6 (cảm ơn/cam đoan), 10 (cuối trạng thái nghiên cứu), 17/19/22 (cuối mục lục/danh mục hình/bảng), 30 (cuối Phần 1), 77 (cuối Ch.3), 130 (cuối Ch.4), 134 (cuối Kết luận), 137 (cuối tài liệu tham khảo), 157 (trang cuối). Không trang hình/bảng nào bị gắn cờ |
| Xem ảnh render cỡ đọc được | Bảng 3.1 (lần đầu tràn chân trang → đổi `\footnotesize`, rút chữ, hết tràn), Bảng 4.33 kịch bản, 4 bảng gộp, Phụ lục A.1–A.5, trang Abstract |

| PDF | SHA-256 |
| --- | --- |
| `report/build/content/content.pdf` | `feee114949b5cf21a662070998b231189eae7637214150e7b9716dd52a7928f5` |
| `report/build/content-twoside/content.pdf` | `ab251f62829eb577c07218d1755f039e60222604fb36fae58be2657171e5d385` |

## 4. Còn mở

- **D-2:** `\ThesisDate`, `\DefenseDate`, tên hội đồng — bỏ qua theo yêu cầu đến khi có thông tin.
- **3.7:** slide chưa đồng bộ tên (nhánh 4).
- GVHD chưa ghi nhận D-4 và tên tiếng Việt mới.
- Kiểm tay bàn phím/trình đọc màn hình (A11Y) vẫn do người thực hiện.
- Câu share link trên trang Sources của app (nằm ngoài báo cáo).
