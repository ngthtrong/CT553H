# Đề tài đang đào sâu

> Danh sách đề tài và vị trí của từng đề tài (chính / dự phòng / thứ tự tiềm năng) **chỉ ghi ở [DECISIONS.md](../DECISIONS.md)**. File này chỉ mô tả khuôn thư mục.

## Khuôn một thư mục đề tài

Mỗi đề tài gói gọn trong một thư mục, tên mô tả bằng tiếng Anh, chữ thường, nối bằng gạch ngang. **Số đầu tên thư mục** (ví dụ `1-plm-calibration-audit`) thể hiện mức tiềm năng; số này do Trọng tự đặt. Khi đổi tên, chạy `python3 tools/rename_topic.py <tên-cũ> <tên-mới>` để `git mv` và sửa toàn bộ link trỏ tới.

```text
topics/<ten-de-tai>/
├── README.md        Thẻ trạng thái nghiên cứu: bài toán, I/O, G1/G2/G3, rủi ro, việc tiếp theo. Sửa đè khi có tiến triển
├── log.md           Nhật ký nghiên cứu riêng đề tài, mới nhất ở trên
├── research/        Khảo sát tài liệu, audit dữ liệu, báo cáo (script audit đi cùng ghi chú của nó)
├── code/            Script tiền xử lý / thí nghiệm (tạo khi có)
├── presentation/    Slide, trang HTML trình bày, bản chuẩn bị buổi gặp (tạo khi có)
├── proposal/        Đề cương LaTeX (tạo khi có)
└── data/            Dữ liệu thật: raw/ (gốc, không sửa tay), interim/ (cache), processed/ (đầu ra script). KHÔNG lên git
```

`data/` bị `.gitignore` chặn (`topics/*/data/`, `archive/topics/*/data/`). Script tìm thư mục đề tài qua file `log.md` và thư mục gốc repo qua `DECISIONS.md`, nên vẫn chạy được sau khi đổi tên hay chuyển thư mục; `git mv` mang theo cả `data/`.

## Thêm hoặc đóng một đề tài

- **Thêm:** tạo thư mục theo khuôn trên, viết `README.md` + `log.md`, rồi ghi quyết định vào `DECISIONS.md`.
- **Đóng:** ghi quyết định vào `DECISIONS.md`, `git mv` thư mục sang `archive/topics/`, thêm một dòng vào [archive/README.md](../archive/README.md).
