# Kiểm chứng cập nhật kết quả ưu tiên mutation — 07/11/2026

Phạm vi là cập nhật luận văn từ [replay OOF đã đo](../research/oof-prioritization-2026-11-07/README.md),
không chạy lại mô hình, mở tập T hay làm wet lab. [Biên bản JSON](prioritization-validation-2026-11-07.json)
ghi hash nguồn/tài sản/PDF, số trang, trạng thái kiểm và giới hạn.

## Nội dung đã đồng bộ

- Chương 3, mục **Equal-Budget Retrospective Prioritisation**: candidate pool,
  hai chiều hit, năm chính sách, ngân sách cố định/tỷ lệ, tie, kỳ vọng random,
  denominator, budget-to-recall và bootstrap nhóm protein.
- Chương 4, mục **Equal-Budget Retrospective Mutation Prioritisation**:
  Precision@10 dương 53,62%/46,26%/9,78% của LoRA-D/W5-D/random kỳ vọng;
  1.260/1.087/229,86 hit với cùng 2.350 lựa chọn; hai CI Bonferroni 97,5%.
  Báo cả các đối chứng phụ, chiều âm, recall, lựa chọn để đạt recall và PSI.
- Phụ lục B thêm từng seed/ensemble và sáu ngân sách. Tổng cộng **6 bảng,
  1 đồ thị** mới; macro số và tài sản được sinh từ nguồn đã kiểm hash.
- Hai tóm tắt, trạng thái tiến độ, mở đầu, đánh giá RQ và kết luận giữ đúng
  phạm vi bằng chứng mới. Những câu “chỉ so random” được giới hạn lại cho
  benchmark lịch sử 91 peptide; không đổi số liệu hoặc protocol cũ.

## Kiểm số và truy vết

[Generator](assets/ch4/build_prioritization_assets.py) kiểm SHA-256 của các
JSON/CSV trước khi sinh tài sản. [Manifest](assets/ch4/priority-assets.json)
ghi chín output và hash generator. [Script kiểm](scripts/validate_prioritization_report.py)
đối chiếu **toàn bộ ô của sáu bảng** với nguồn, xác nhận denominator, ngân sách
và hai contrast chính; giữ đủ **88 hàng cấu hình OOF** của bảng campaign cũ.
Nguồn replay đã có kiểm số học bằng triển khai riêng; việc tích hợp luận văn
không tạo thêm một nghiên cứu độc lập hoặc một phép kiểm wet lab.

Provenance nội bộ nằm trong mã, comment LaTeX và biên bản; PDF không in tên
file/đường dẫn nội bộ để làm dẫn chứng. Không thêm tài liệu học thuật hoặc
thay bibliography trong lượt này.

## Build và PDF

```bash
.venv/bin/python -I report/assets/ch4/build_prioritization_assets.py
make -C report all
make -C report check
.venv/bin/python -I report/scripts/validate_prioritization_report.py --visual-reviewed
git diff --check
```

`--visual-reviewed` ghi nhận việc session chính đã thực sự xem ảnh render,
không tự suy ra từ kiểm tự động hoặc gán thành người dùng đã duyệt.
Receipt của lượt build cuối được lưu trong thư mục review ở `build/` và
được chép vào biên bản JSON.

- [PDF một mặt](build/content/content.pdf) và [PDF hai mặt](build/content-twoside/content.pdf):
  **130 trang/bản**, khổ A4, phông nhúng, tham chiếu đã giải quyết.
- Không còn overfull box, thiếu ký tự hoặc lỗi citation/reference trong log.
  Hai tóm tắt vẫn mỗi ngôn ngữ một trang, tại trang PDF 7 và 8.
- Đã xem contact sheet của 22 trang liên quan ở mỗi bản và các trang chi tiết
  tóm tắt, công thức, bảng chính/CI, đồ thị, phụ lục seed/ngân sách.
  Đã sửa công thức tràn ngang, nới bảng ngân sách và tránh float chen giữa câu.
- Đã kiểm annotation và nội dung PDF; không có annotation đánh dấu nhận xét
  trong hai PDF. Không dùng byte equality để suy hai layout giống nhau.
- Các tệp render/contact sheet ở `build/review-prioritization-2026-11-07/`,
  được Git ignore. Năm marker `[PENDING]` của nội dung hiện tại vẫn giữ nguyên.

Kiểm acronym là advisory trên bản trích các phần được cập nhật: **partial**,
không hỗ trợ tóm tắt tiếng Việt và không chứa glossary/phần định nghĩa trước
đó. Các báo thiếu định nghĩa trong body được đối chiếu phạm vi; WT/LoRA bị
checker hạn chế nhận dạng cách viết. Tóm tắt Anh đã ghi đầy đủ WT và AUROC.
Không coi kiểm này là chứng nhận toàn luận văn không có lỗi thuật ngữ.

## Giới hạn và phần giữ nguyên

Kết quả được trình bày là **hồi cứu development**. Precision dùng cả 235 peptide;
recall/enrichment/budget-to-recall dương dùng 198 peptide có hit, không bỏ
37 peptide không hit khỏi Precision. Random là kỳ vọng, không phải campaign
wet lab đã chạy. Lựa chọn tránh được trong replay không chuyển thành số giờ
hoặc tiền tiết kiệm; tổng hit dùng cho recall chỉ biết khi chấm hồi cứu.

LoRA-D vẫn là policy chính dù LoRA-B có point estimate hơi cao hơn. Phép so
LoRA–W5 giữa runtime khác nhau không cô lập riêng tác động adaptation. Không
thay mô hình phục vụ hoặc tự đóng G2/G3. Các hồ sơ kiểm ngày 03/11 và 06/11
giữ nguyên phạm vi/hash lịch sử; đề cương và template sạch không sửa.

Worker native đã hoàn tất một lượt rà câu chữ và phạm vi trước tích hợp;
lượt rà bản viết cuối của worker không chạy được vì hạn mức. Session chính
thực hiện kiểm cuối bằng source, script, PDF text và ảnh render. Không tuyên
bố có peer review độc lập hay cross-model review cho bản cập nhật này.
