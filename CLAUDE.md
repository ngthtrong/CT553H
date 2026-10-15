# CLAUDE.md

Repo luận văn tốt nghiệp CT553H (Kỹ thuật phần mềm, ĐH Cần Thơ) của **Nguyễn Thế Trọng**, GVHD **TS. Hồ Quang Thái**. Trạng thái đề tài và phê duyệt đọc ở [DECISIONS.md phần A](DECISIONS.md#hien-hanh); tiến độ thực nghiệm đọc ở README/log đề tài. Không giữ một bản trạng thái thứ hai trong file quy ước này.

## Đầu phiên: đọc theo thứ tự này

1. **[DECISIONS.md](DECISIONS.md)**: [A — hiện hành](DECISIONS.md#hien-hanh), [C — chờ xác nhận](DECISIONS.md#cho-xac-nhan), [D — theo dõi](DECISIONS.md#theo-doi). Tra [B1](DECISIONS.md#nghien-cuu-degron) cho ràng buộc nghiên cứu, [B2](DECISIONS.md#quy-uoc-repo) cho quy ước repo. [B3](DECISIONS.md#lich-su) là lịch sử/bối cảnh thu gọn, không phải kế hoạch đang thực hiện.
2. `README.md` (thẻ trạng thái) và `log.md` của đề tài sắp làm, trong `topics/<ten-de-tai>/`.
3. Mục mới nhất của nhật ký chung [journal/](journal/README.md), nếu cần bối cảnh liên đề tài.

Nếu một tài liệu khác (báo cáo, nhật ký, trang HTML, file trong `archive/`) nói điều gì **trái với `DECISIONS.md`**, tin `DECISIONS.md` và báo lại cho Trọng chỗ mâu thuẫn. Không hành động theo câu "đã chốt" trong tài liệu cũ.

## Quy tắc ghi quyết định

- **Chỉ `DECISIONS.md` được ghi quyết định.** Tài liệu khác chỉ dẫn link `DECISIONS.md#d-0xx`, không viết lại nội dung quyết định.
- Khi Trọng quyết một điều mới: lấy mã `D-0xx` kế tiếp theo **mã lớn nhất toàn sổ**, thêm vào đầu **nhóm phù hợp**: B1 (nghiên cứu) hoặc B2 (quy ước repo). Mỗi nhóm xếp mã mới nhất ở trên. Ghi ngày, người quyết/nguồn thẩm quyền, nội dung, căn cứ và khoản nào bị thay; sửa đè A nếu trạng thái hiện hành đổi. Không tạo lại một quyết định chỉ vì chuyển nhóm.
- **Hiệu lực theo khoản:** quyết định nhiều nội dung chỉ bị thay một phần thì ghi rõ `Còn áp dụng` và `Bị thay bởi D-0xx` cho từng khoản; giữ số khoản cũ để các trích dẫn vẫn đúng. Tách hiệu lực quyết định khỏi tiến độ thực hiện. Ví dụ, việc chọn đề tài đã làm xong nhưng quyết định vẫn áp dụng; email đã gửi nhưng phản hồi vẫn đang chờ.
- **Không xoá hay đánh lại mã** quyết định cũ. Mục hết liên quan đưa vào B3; lịch sử/bối cảnh không đồng nghĩa bãi bỏ. Khi rút gọn một bản ghi, giữ nguyên văn hồ sơ trước biên tập trong `<details>` và ghi hiệu lực hiện hành bên ngoài. Câu cũ trong khối nguyên văn không được dùng để phục hồi kế hoạch đã bị thay.
- **Đề xuất của Claude không phải quyết định.** Ghi đề xuất vào phần C và chờ Trọng xác nhận. Chỉ khi Trọng nói rõ "Claude tự quyết" thì mới ghi thẳng vào phần B, với "Ai quyết: Claude (ủy quyền)".
- **C chỉ chứa lựa chọn chưa xác nhận:** nêu câu hỏi cần quyết, khuyến nghị, ảnh hưởng và điều kiện còn thiếu; dẫn chi tiết sang báo cáo. Việc đã giao/chờ thực hiện hoặc chờ phản hồi ngoài đưa vào D; backlog kỹ thuật vẫn ở README/log đề tài. Khi C được giải quyết, giữ anchor `c-xx` trỏ tới quyết định tương ứng; nếu hồ sơ vừa ghi đã yêu cầu vừa ghi chờ xác nhận, nêu xung đột, không tự đóng đề xuất.
- **A là bản đọc nhanh**, khoảng 8 dòng trạng thái / một màn hình; không cộng dồn CI, phân rã delta, danh sách hướng đã loại hoặc bản đính chính. Kết quả đo nằm ở `research/` với nhãn bằng chứng. Không biến trần đo lường thành dư địa cải thiện, MDE của một phép so thành ngưỡng nghiệm thu chung, hay một kết quả dương cục bộ thành hoàn tất G2.
- Lời GVHD là thông tin thô: ghi vào biên bản ở `project/meetings/` hoặc [project/people.md](project/people.md). Hệ quả của lời đó cho việc chọn đề tài thì ghi vào `DECISIONS.md`.
- Dùng anchor cố định `hien-hanh`, `nghien-cuu-degron`, `quy-uoc-repo`, `lich-su`, `cho-xac-nhan`, `theo-doi` và `d-0xx` / `c-xx`; không tạo liên kết trạng thái dựa vào ngày trong tiêu đề. Khi tổ chức lại phải kiểm cả file đích lẫn fragment và giữ điểm chuyển tiếp cho mã cũ. Căn cứ thay đổi cấu trúc: [D-032](DECISIONS.md#d-032).

## Cấu trúc thư mục

```text
CT553H/
├── DECISIONS.md            ★ A hiện hành · B1/B2 sổ còn áp dụng · B3 lịch sử · C chờ xác nhận · D theo dõi
├── README.md               Bản đồ repo 1 trang
├── CLAUDE.md / AGENTS.md   Quy ước làm việc (AGENTS.md chỉ trỏ về đây)
├── project/                Thông tin thô về dự án và con người
│   ├── people.md               Sinh viên, GVHD, người liên quan, những điều GVHD đã nói
│   ├── course.md               Mốc thời gian, năm tiêu chí GVHD, cổng G1/G2/G3
│   ├── advisor-research.md     Các nhánh nghiên cứu của GVHD (dùng để đánh giá tính mới)
│   ├── advisor-publications/   Danh mục công bố đã scrape (ho-quang-thai.md, yu-yen-ou.md)
│   └── meetings/               Mỗi buổi gặp một thư mục YYYY-MM-DD-session-NN/: prep.md, minutes.md, slides/
├── topics/                 Mỗi đề tài đang đào sâu một thư mục, gói gọn tài liệu + code
│   └── <ten-de-tai>/           README.md · log.md · research/ · code/ · presentation/ · proposal/ · data/ (chỉ data/README.md và SOURCE.md lên git)
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
3. Có quyết định mới: cập nhật nhóm B1/B2 phù hợp trong `DECISIONS.md`, hiệu lực từng khoản cũ, phần A và điểm chuyển tiếp C liên quan. Nếu chỉ có tiến độ hoặc phản hồi mới thì cập nhật D và README/log tương ứng; không tạo D mới trừ khi thật sự đổi quyết định.
4. Có tài nguyên mới hoặc đổi trạng thái tài nguyên: cập nhật [resources/README.md](resources/README.md).
5. Có tải, xử lý hay xoá dữ liệu: cập nhật `topics/<ten-de-tai>/data/README.md` (nguồn gốc, danh mục file, các trường, nhật ký xử lý).
