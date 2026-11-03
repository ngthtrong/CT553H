# Kiểm tra tài liệu học — 03/11/2026

**PASS.** PDF cuối: `study-guide.pdf`, **62 trang A4, 19 chương, 22 hình**
(12 sơ đồ Draw.io + 8 hình từ số liệu đã lưu + 1 ví dụ tự đặt + 1 ảnh giao diện fixture).
Các chương 1–16 trình bày kiến thức và tiến trình; 17–19 là thực hành, từ điển và nguồn.

## Nội dung và nguồn

- Đối chiếu 31 nguồn nội bộ; lưu SHA-256, vai trò NC/KH/PM và 5 tài liệu nền bên ngoài.
- Kiểm lại các giá trị chính được đưa vào bản học: 235 peptide, 221 nhóm, 122.412 ô saturation;
  Ridge W5-D MAE 0,40780, CNN-D 0,38435, mCNN-E 0,38385. Phạm vi là development.
- Phân biệt cohort lịch sử 91 peptide, pool train 176 và full-PSI 235; không ghép metric
  khác population thành một bảng so trực tiếp.
- Sửa rõ M3 đã có ordered context ±3; W5 mở tới ±5. Không mô tả phép so này như unordered→ordered.
- **Chương local chỉ có hướng đi/lý do**, không dùng fit score, checkpoint score, tiến độ từng
  task hoặc thứ hạng pLM chưa đủ. Trong PDF, chương này ở trang vật lý **46–48**
  (trang in 39–41); không khởi chạy/dừng/sửa campaign.
- R3, baseline app và UI fixture giữ phạm vi riêng; test lịch sử không được gọi là nghiệm thu mới.

## PDF và sơ đồ

- XeLaTeX lặp đến khi tham chiếu ổn định; không overfull box, thiếu glyph, nhãn trùng hoặc
  tham chiếu chưa giải quyết. Font nhúng và có Unicode mapping; mọi trang A4.
- Kiểm 279 liên kết PDF và các bookmark chương/phần; liên kết nội bộ có đích hợp lệ.
- Cả 12 bản `.drawio` qua kiểm cấu trúc, không lỗi/cảnh báo. Render bằng native Draw.io 32.6.1.
- Native PDF phải dùng `--crop`; đã sửa lỗi xuất mặc định Letter cắt cạnh phải.
  Kiểm tự động xác nhận **toàn bộ nhãn node của từng sơ đồ** còn đầy đủ trong PDF xuất.
- Đã xem contact sheet của **toàn bộ 62 trang** ở bản cuối. Xem thêm ảnh lớn các trang
  có công thức, ma trận, bảng/CI và local plan; kiểm vị trí caption, dấu tiếng Việt, ký hiệu,
  bảng nhỏ cùng trang và nhãn đo/minh họa/fixture/kế hoạch.
- Preview sinh ở `previews/` (ngoài Git); nguồn Markdown, script, PNG/PDF và `.drawio` được giữ.

## Tái lập và phạm vi kiểm tra

Đã chạy `make` và `make previews` với môi trường Python riêng, không đổi môi trường CUDA.
`validation.json` giữ hash PDF và hash các nguồn tạo artifact. `source-map.md` giữ bản đồ nguồn.
Lệnh dựng lại được ghi trong README.

Các kiểm tra trên xác nhận artifact học tập và tính khớp nguồn trong phạm vi đã xét;
không phải lượt train mới, nghiệm thu ứng dụng, external validation hoặc xác nhận G2/G3.
