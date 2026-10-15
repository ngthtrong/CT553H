# CLAUDE.md

Repo luận văn tốt nghiệp CT553H (Kỹ thuật phần mềm, ĐH Cần Thơ) của **Nguyễn Thế Trọng**, GVHD **TS. Hồ Quang Thái**. Hiện ở **giai đoạn chọn đề tài**: nhiều đề tài được đào sâu song song, chưa đề tài nào được GVHD duyệt, chưa huấn luyện mô hình hay xây ứng dụng.

## Đầu phiên: đọc theo thứ tự này

1. **[DECISIONS.md](DECISIONS.md)**, phần A (hiện hành) và phần C (đang chờ xác nhận). Đây là **nguồn duy nhất** cho các câu hỏi: đề tài nào chính, dự phòng, đang đào sâu, đã loại; định hướng chọn đề tài; quy ước đang áp dụng.
2. `README.md` (thẻ trạng thái) và `log.md` của đề tài sắp làm, trong `topics/<ten-de-tai>/`.
3. Mục mới nhất của nhật ký chung [journal/](journal/README.md), nếu cần bối cảnh liên đề tài.

Nếu một tài liệu khác (báo cáo, nhật ký, trang HTML, file trong `archive/`) nói điều gì **trái với `DECISIONS.md`**, tin `DECISIONS.md` và báo lại cho Trọng chỗ mâu thuẫn. Không hành động theo câu "đã chốt" trong tài liệu cũ.

## Quy tắc ghi quyết định

- **Chỉ `DECISIONS.md` được ghi quyết định.** Tài liệu khác chỉ dẫn link `DECISIONS.md#d-0xx`, không viết lại nội dung quyết định.
- Khi Trọng quyết một điều mới: thêm mục `D-0xx` lên đầu phần B (ngày, ai quyết, nội dung, lý do). Sửa đè phần A cho khớp. Đổi trạng thái mục cũ thành `Bị thay bởi D-0xx`, **không xoá**.
- **Đề xuất của Claude không phải quyết định.** Ghi đề xuất vào phần C và chờ Trọng xác nhận. Chỉ khi Trọng nói rõ "Claude tự quyết" thì mới ghi thẳng vào phần B, với "Ai quyết: Claude (ủy quyền)".
- Lời GVHD là thông tin thô: ghi vào biên bản ở `project/meetings/` hoặc [project/people.md](project/people.md). Hệ quả của lời đó cho việc chọn đề tài thì ghi vào `DECISIONS.md`.

## Cấu trúc thư mục

```text
CT553H/
├── DECISIONS.md            ★ Nơi duy nhất ghi quyết định (hiện hành + sổ quyết định + đề xuất chờ duyệt)
├── README.md               Bản đồ repo 1 trang
├── CLAUDE.md / AGENTS.md   Quy ước làm việc (AGENTS.md chỉ trỏ về đây)
├── project/                Thông tin thô về dự án và con người
│   ├── people.md               Sinh viên, GVHD, người liên quan, những điều GVHD đã nói
│   ├── course.md               Mốc thời gian, năm tiêu chí GVHD, cổng G1/G2/G3
│   ├── advisor-research.md     Các nhánh nghiên cứu của GVHD (dùng để đánh giá tính mới)
│   ├── advisor-publications/   Danh mục công bố đã scrape (ho-quang-thai.md, yu-yen-ou.md)
│   └── meetings/               Mỗi buổi gặp một thư mục YYYY-MM-DD-session-NN/: prep.md, minutes.md, slides/
├── topics/                 Mỗi đề tài đang đào sâu một thư mục, gói gọn tài liệu + code
│   └── <ten-de-tai>/           README.md (thẻ trạng thái) · log.md · research/ · code/ · presentation/ · proposal/ · data/ (không lên git, trừ data/README.md)
├── surveys/                Khảo sát diện rộng chưa gắn với một đề tài (danh mục ứng viên)
├── resources/              ★ Mọi tài nguyên: README.md (chỉ mục + artifact/Notion/dữ liệu/môi trường), papers/, reference-theses/, course/
├── lectures/               Mọi bài giảng tự học (HTML mở bằng file://, CS535, lộ trình sinh học, hub học degron)
├── journal/                Nhật ký chung theo tháng (YYYY-MM.md), mới nhất ở trên
├── archive/                Đề tài đã đóng, khảo sát cũ — KHÔNG dùng để ra quyết định
├── tools/                  check_links.py (kiểm link), rename_topic.py (đổi tên thư mục đề tài + sửa link)
└── requirements.txt        Cài vào .venv/ ở thư mục gốc
```

Khuôn của một thư mục đề tài và cách thêm/đóng đề tài: xem [topics/README.md](topics/README.md). Chỉ đề tài được chốt cuối cùng mới có thêm `backend/`, `frontend/`, `ml-service/`, `thesis/` ở thư mục gốc. Các thư mục này chưa tồn tại.

@resources/README.md

## Quy ước

- **Tên file/thư mục:** chữ thường, không dấu, tiếng Anh, nối bằng gạch ngang. Thư mục đề tài có thể có **số đầu tên** (`1-ten-de-tai`) thể hiện mức tiềm năng; số này **do Trọng tự đặt**, Claude không tự đổi.
- **Liên kết** giữa các tài liệu dùng đường dẫn tương đối. Sau khi di chuyển hay đổi tên file, chạy `python3 tools/check_links.py` và sửa đến khi không còn link hỏng. Đổi tên thư mục đề tài thì dùng `python3 tools/rename_topic.py <cũ> <mới>`.
- **Script** tìm thư mục gốc repo qua file `DECISIONS.md` (không dùng `parents[N]`), để vẫn chạy được sau khi chuyển thư mục.
- **Dữ liệu** nằm trong chính thư mục đề tài: `topics/<ten-de-tai>/data/{raw,interim,processed}/`. Nội dung thư mục này bị `.gitignore` chặn; không bao giờ commit dữ liệu, tên thật hay file chưa ẩn danh. Mọi file trong `data/processed/` phải sinh lại được bằng script trong `code/` hoặc `research/` của đề tài. Script tìm thư mục đề tài qua file `log.md` (`TOPIC`), nên `data/` đi theo khi đổi tên hay chuyển thư mục đề tài.
- **Sổ nguồn gốc dữ liệu:** mỗi `data/` có một `data/README.md`, và mỗi bộ dữ liệu tải về có thêm một `SOURCE.md` cạnh nó (hai loại file duy nhất trong `data/` được lên git, nhờ ngoại lệ `!**/data/README.md` và `!**/data/**/SOURCE.md`). `SOURCE.md` giữ **thông báo giấy phép nguyên văn** và xuất xứ ghim của riêng bộ đó; `data/README.md` giữ bản tổng hợp. Nó ghi: (1) **nguồn gốc** từng bộ dữ liệu: URL/DOI/accession, phiên bản hoặc commit ghim, giấy phép, ngày tải, manifest/SHA-256; (2) **danh mục từng file** trong `raw/`, `interim/`, `processed/`: script nào tạo ra, từ đầu vào nào, đã kiểm gì; (3) **giải thích các trường** của tập dữ liệu dùng để huấn luyện/đánh giá: cấu trúc định danh, ý nghĩa, đơn vị và chiều của từng cột, nhãn suy ra thế nào; (4) **nhật ký xử lý** theo ngày, mới nhất ở trên; (5) lệnh **dựng lại từ đầu**. Mỗi lần tải thêm, xử lý lại hay xoá file trong `data/` thì cập nhật README này **trong cùng phiên**. File không rõ script tạo ra thì ghi rõ "không có script" thay vì đoán. Mẫu: [topics/degron-footprint/data/README.md](topics/degron-footprint/data/README.md).
- **Thí nghiệm tái lập được:** cố định seed; ghi config và kết quả nhỏ ra file trong thư mục đề tài. Số liệu đưa vào tài liệu phải trỏ tới file kết quả tương ứng.
- **Nhãn bằng chứng** khi viết khảo sát: phân biệt rõ đã tự đo, nguồn tác giả, phân tích, đề xuất, và chưa xác minh (chỉ thấy qua tóm tắt tìm kiếm). Không nói "chưa ai làm" khi mới tra qua tóm tắt.
- **Khi soạn slide/báo cáo:** đọc [gợi ý trình bày từ sáu bài của nhóm GVHD](project/advisor-presentation-guide.md) để tham khảo mạch dẫn nhập, workflow, bảng đối chứng/ablation và giới hạn lập luận. Đây là gợi ý theo yêu cầu của Trọng, không phải yêu cầu bắt buộc của GVHD; mẫu học phần và trạng thái trong `DECISIONS.md` vẫn là căn cứ.
- **Trang HTML** tạo trực tiếp trong repo, mở bằng `file://`, không publish artifact ([D-013](DECISIONS.md#d-013)).
- **Repo private** ([D-004](DECISIONS.md#d-004)): được chứa PDF bài báo và phân tích về bài của nhóm GVHD. Nếu đổi sang public hoặc chia sẻ repo (kể cả cho GVHD) thì phải gỡ các phần này trước, kể cả khỏi lịch sử git.

## Cuối phiên có thay đổi đáng kể

1. Việc làm cho một đề tài: thêm mục lên đầu `topics/<ten-de-tai>/log.md` và sửa đè thẻ `README.md` của đề tài (G1/G2/G3, việc tiếp theo, ngày cập nhật).
2. Việc chung: thêm 3–5 dòng lên đầu `journal/YYYY-MM.md`.
3. Có quyết định mới: cập nhật `DECISIONS.md` (phần B, rồi phần A).
4. Có tài nguyên mới hoặc đổi trạng thái tài nguyên: cập nhật [resources/README.md](resources/README.md).
5. Có tải, xử lý hay xoá dữ liệu: cập nhật `topics/<ten-de-tai>/data/README.md` (nguồn gốc, danh mục file, các trường, nhật ký xử lý).
