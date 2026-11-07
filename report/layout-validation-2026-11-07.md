# Kiểm tra bố cục và tham chiếu — 07/11/2026

Đã sửa ba nhóm nhận xét: khoảng trắng/ngắt trang, số và tên hình/tham chiếu,
và tính nhất quán của định dạng. Phạm vi là bản làm việc `report/`;
không sửa `reportTemplate/`, số liệu nghiên cứu hoặc các biên bản validation cũ.
Kết quả máy đọc, hash và danh mục hình/bảng:
[layout-validation-2026-11-07.json](layout-validation-2026-11-07.json).

## Kết quả

| Hạng mục | Trước | Sau |
| --- | ---: | ---: |
| Tổng số trang, mỗi bản một mặt/hai mặt | 130 | 121 |
| Danh mục hình | 2 trang | 1 trang |
| Danh mục bảng | 5 trang | 3 trang |
| Thuật ngữ | 2 trang | 1 trang |
| Trang hình trong thân bài có đuôi trống trên 1/3 vùng nội dung | 3 | 0 |

Chỉ số đuôi trống đo từ dòng chữ cuối trong vùng nội dung tới đáy vùng đó,
ngưỡng 224 pt; đây là chỉ báo rà soát, không thay thế kiểm tra bằng mắt.
Các trang hình bị đánh dấu trước sửa là trang PDF 58, 78 và 97.

## Thay đổi

- Điều chỉnh khoảng cách quanh float, số hình/bảng được phép cùng trang và
  tỷ lệ tối thiểu của trang chỉ chứa float; giữ lề, Times New Roman 13 bp
  và giãn dòng thân bài 1,3. Dùng `raggedbottom` để tránh kéo giãn khoảng cách
  dọc trong bản hai mặt.
- Thêm 49 tên ngắn cho danh mục; giữ nguyên toàn bộ chú thích đầy đủ, kể cả
  trích dẫn và giới hạn bằng chứng. Mở rộng ô số trang của mục lục/danh mục
  để số La Mã dài không tràn khung. Thu gọn bảng thuật ngữ về cùng một trang.
- Chuyển bảng lịch sử nghiên cứu sang `longtable`, lặp tiêu đề cột/chú thích
  khi tiếp bảng. Bổ sung chú thích tiếp bảng cho đặc tả use case và bảng RQ.
- Bỏ ba lệnh `clearpage` ở phụ lục B; giữ tiêu đề với nội dung theo sau và
  dùng `FloatBarrier` tại hai ranh giới mục để bảng không trôi sang mục kế tiếp.
- Bổ sung hai lượt dẫn hình còn thiếu: kết quả adaptation và đường cong
  ngân sách. Mọi hình đều được dẫn bằng nhãn; không gõ số hoặc chỉnh bộ đếm.
- Ghi quy tắc dùng tiếp tại [CLAUDE.md](../CLAUDE.md), dẫn chiếu từ
  [README.md](README.md). Thêm [check_float_references.py](scripts/check_float_references.py)
  vào `make check` để đối chiếu danh mục, nhãn và PDF.

## Kiểm chứng

Các lệnh sau đã chạy thành công:

```bash
make -C report all
make -C report smoke
make -C report check
git diff --check
```

- Hai PDF chính: 121 trang A4 mỗi bản; PDF smoke: 9 trang. Phông nhúng;
  không có overfull box, thiếu ký tự, nhãn trùng, citation/reference chưa giải quyết.
- 12 hình: 2.1–2.2, 3.1–3.3, 4.1–4.7. 58 bảng: 1.1–1.10,
  3.1–3.3, 4.1–4.37, B.1–B.8. Đối chiếu số liên tục, thứ tự chương,
  tên danh mục/nhãn, chú thích in trên đúng trang và named destination trong PDF.
- 461 vùng liên kết mỗi bản nằm trong trang; đích liên kết nội bộ hợp lệ.
  Kiểm tra bằng lỗi cố ý trong bản sao tạm đã bắt được sai số hình, sai tên,
  sai đích PDF và thiếu lượt dẫn hình trong nội dung.
- Xem ảnh tổng quan toàn bộ bản một mặt, xem kỹ đủ 12 trang hình, danh mục,
  bảng tiếp trang và chuyển mục phụ lục; đối chiếu bản hai mặt tại các trang
  định dạng tương ứng. Có 51 ảnh trang ở kích thước đọc được cho mỗi bản tại
  `build/review-layout-2026-11-07/`. Đối chiếu raster tất cả trang giữa hai bản
  không phát hiện khác biệt tại độ phân giải kiểm tra.
- 205 tệp tài sản đã có giữ nguyên byte so với khi bắt đầu. Kiểm riêng xác nhận
  mọi chú thích đầy đủ vẫn được giữ; không sửa số liệu, biểu đồ hay bảng kết quả.

Khoảng trống ở bìa, trang ký/nhận xét và cuối chương, tài liệu tham khảo,
phụ lục vẫn được giữ theo chức năng. Trang danh mục cuối không bị ép ghép
với phần kế tiếp; trang cuối bảng 88 cấu hình dành chỗ cho các hàng hoàn chỉnh.
Đây là kiểm chứng định dạng của bản đang viết, không xác nhận hoàn tất các mục
`[PENDING]` hoặc nghiệm thu nghiên cứu/phần mềm.

## PDF

- [Bản một mặt](build/content/content.pdf) — SHA-256:
  `7c3581207e67240586eb3a75e1ffa745313adafdc7320e20cf1acd745fd2fd8e`.
- [Bản hai mặt](build/content-twoside/content.pdf) — SHA-256:
  `ace7c37ee370537c7b24b066d2240dadafa7fe5f5bf5efc035cd188ac10312fb`.
