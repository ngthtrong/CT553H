# Biên bản kiểm tra báo cáo — 17/11/2026 (lượt C)

Trạng thái khoa học giữ `development_not_gate_closure`. **Build sạch không phải nghiệm thu nghiên cứu
và cũng không phải nghiệm thu phần mềm.** Không có con số nào trong báo cáo được tính lại ở lượt này;
mọi số mới được generator đọc từ file kết quả và ghi kèm hash nguồn.
Số liệu máy đọc: [review-validation-2026-11-17.json](review-validation-2026-11-17.json).

## 1. Lệnh đã chạy

| Lệnh | Kết quả |
| --- | --- |
| `make -C report all` | exit 0 |
| `make -C report check` | PASS — một mặt và hai mặt, **148 trang** mỗi bản, A4, phông nhúng |
| `python report/scripts/check_float_references.py` | PASS — **23 hình / 66 bảng**, hai biến thể khớp nhau |

- PDF một mặt: `960a32df520166a5969fad99b0580aedd0f6bf953b38f6f17ceeffb403f8cc95`
- PDF hai mặt: `2c12ce1492613e8f9596d52ae31d1cda2f710f3d6a1f094da5e097613b138806`
- Smoke (9 trang): `f82222c631ded47dc2889fabd28dcaa46a88e15858de8e5fae7538291b34ac06`

## 2. Rà bố cục

Trước lượt này: 12 hình / 58 bảng. Sau: **23 hình / 66 bảng**; riêng Chương 4 giảm 44 → 40 bảng,
Phụ lục B tăng 8 → 12.

**Cách đo khoảng trống:** render từng trang của **cả hai** bản ở 50 dpi, trong vùng nội dung đo
khoảng trống lớn nhất và khoảng trống cuối trang theo tỉ lệ chiều cao vùng; ngưỡng một phần ba.

Kết quả: **12/148 trang** vượt ngưỡng, **giống hệt nhau ở cả hai bản**. Tất cả đều là kết thúc có
chức năng, không phải lỗi bố cục:

| Trang | Lý do |
| --- | --- |
| 5, 6 | Lời cảm ơn và lời cam đoan — có ô ký tên |
| 10, 17, 21 | Cuối mục lục / danh mục bảng / danh mục |
| 73 | Cuối Chương 3 |
| 113 | Cuối một bảng nhiều trang |
| 125 | Cuối Chương 4 |
| 129 | Cuối phần Kết luận |
| 132 | Cuối danh mục tài liệu tham khảo |
| 136 | Cuối Phụ lục A |
| 148 | Trang cuối Phụ lục B |

Không trang hình/bảng nào, và không trang liền trước hay liền sau nào, bị gắn cờ.
Các trang chứa sáu sơ đồ mới đã được **xem ảnh render ở cỡ đọc được** và vẽ lại cho tới khi hết
chồng chữ.

## 3. Đã làm

- **3.1** — xoá đủ 5 dấu `[PENDING]`; `grep` trên `chapters/ frontmatter/ appendices/` trả về 0.
  Mỗi chỗ thay bằng nội dung thật: quy trình cài đặt và container **đã chạy**, lượt thao tác đã thực
  hiện kèm trỏ tới ảnh chụp, và mục nguồn mở/dữ liệu **không bịa đường dẫn kho**.
- **3.2** — mục mới *Software Acceptance of the First Release* trong Chương 4.
- **3.3** — mục mới *Final Refit and Held-Source Transfer*: kết quả T, đảo dấu ở strata PSI(WT) > 5
  **giữ nguyên là kết quả âm**, phép kiểm similarity, Koren dạng khảo sát, quyết định phạm vi và
  bảng giới hạn L1–L10. Kết luận, đánh giá RQ và trang trạng thái đã cập nhật.
- **3.4** — sáu sơ đồ dựng từ code: use case, kiến trúc/triển khai, sequence job, state job/item,
  sequence import–comparison, CDM.
- **3.5** — Chương 3 viết lại theo triển khai thật, gồm CDM → LDM → **PDM đọc từ ORM** và đối chiếu
  migration `0001`–`0004`.
- **3.8** — ba lệnh PASS trên cả hai bản.

## 4. Chưa làm

- **3.6 — một phần.** Vẫn 66 bảng. Không gộp thêm các bảng mỏng vì chúng thuộc các protocol khác
  nhau; gộp sẽ trộn các thiết kế mà hồ sơ nghiên cứu cố ý giữ riêng.
- **3.7 — bị chặn:** chưa chốt tên đề tài chính thức.
- Chạy lại bộ test PostgreSQL sau thay đổi 17/11; kiểm tay a11y; **ghi nhận của GVHD cho biên bản
  D-4 vẫn chưa có**.

## 5. Cách tái lập các số mới

```bash
.venv/bin/python report/assets/ch4/build_transfer_assets.py
system/app/.venv/bin/python -I report/assets/ch4/dump_app_schema.py
.venv/bin/python report/assets/ch4/build_app_assets.py
make -C report all && make -C report check
python report/scripts/check_float_references.py
```

`dump_app_schema.py` **dừng** nếu ORM và migration lệch nhau; `build_transfer_assets.py` **dừng**
nếu `scientific_status`, `serving_promotion` hoặc danh sách L1–L10 trong biên bản D-4 thay đổi.
Không commit/push trong lượt này.
