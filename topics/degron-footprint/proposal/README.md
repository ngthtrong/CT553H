# Đề cương luận văn degron-footprint

Bản dự thảo ngày **21/10/2026**, soạn theo mẫu tiếng Việt của học phần. Tên đề tài là đề xuất cho bản thảo này, chưa phải tên được GVHD phê duyệt.

- [proposal.docx](proposal.docx): bản Word chỉnh sửa được, dùng DOCX đi kèm mẫu làm reference.
- [proposal.pdf](proposal.pdf): bản xem trước được biên dịch bằng XeLaTeX từ cùng nội dung Markdown. Ngắt trang có thể khác Word; chưa kiểm trực quan bằng Microsoft Word.
- [proposal.md](proposal.md): nguồn nội dung chung.
- [references.bib](references.bib): danh mục khởi đầu để nhập vào Zotero/Mendeley, giữ DOI và đường dẫn; cần đồng bộ lại trích dẫn nếu biên tập trực tiếp trong Word. Tác giả dài được rút gọn bằng `and others`; không phải thư viện trích dẫn đã được quản lý qua ứng dụng.
- [validation.json](validation.json): số trang, các kiểm tra tự động và SHA-256 của đầu vào/đầu ra.

## Bám mẫu

Mẫu gốc: [Đề cương LV Mau.pdf](../../../reportTemplate/guideline-thesis/Đề%20cương%20LV%20Mau.pdf) và [DOCX đi kèm](../../../reportTemplate/guideline-thesis/Đề%20cương%20LV%20Mau%20(1).docx).
Giữ 7 phần I–VII, các mục con và ba bảng quy trình/nguồn dữ liệu/dự án. Nội dung mở rộng theo bài toán sinh học và đánh giá mô hình nên dài hơn mẫu trống. Giữ khổ **Letter 612 × 792 pt**, lề 1 inch theo chính mẫu (không suy khổ A4 từ template báo cáo NCKH), phông Times New Roman.

Thông tin sinh viên/GVHD lấy từ [project/people.md](../../../project/people.md): Nguyễn Thanh Trọng, B2305615, TS. Hồ Quang Thái. File này có tên sinh viên khác phần tóm tắt CLAUDE.md; bản thảo dùng hồ sơ người tham gia có MSSV cụ thể. Chỗ cần điền: MSCB của GVHD; lịch tuần chưa tự đặt khi chưa có lịch học phần.

## Bằng chứng và giới hạn

Nguồn hiện hành được đọc trực tiếp: CLAUDE.md; data/README.md; báo cáo G2 saturation và extension 18/10; phân tích/khuyến nghị MetaDegron 21/10; ghi chép bài báo trong lectures/papers/. Không dùng DECISIONS.md hay log.md đã bị xoá, không khôi phục chúng.

Số mẫu 91/89/47.847 và AUROC 0,8082/0,7693 khớp [results.json](../research/g2-saturation-2026-10-18/results.json). Đối chứng Degformer huấn luyện lại cùng ngân sách nhãn đã có ở extension; bản có đầy đủ tiền huấn luyện nhưng loại cụm test vẫn là việc khác chưa hoàn tất. Không ghi G2 hoàn tất, không tự chốt kiến trúc; học chuyển tiếp/đường cong học là phương án đề xuất. MetaDegron đã được audit mã nguồn ngày 21/10; không dùng trạng thái cũ “chưa audit”.

Tên chính thức của bài Zhang và MetaDegron được kiểm qua Crossref DOI API ngày 21/10/2026; tên Voutsinos lấy từ ghi chép bài đã lưu. Một số trang DOI/PMC/GEO không truy cập được qua công cụ web (500/CAPTCHA), nên không xem đó là kiểm chứng lại toàn văn. Trang GitHub Degformer đọc được; các mô tả sâu dựa trên audit ghim trong repository.

## Cập nhật 22/10/2026

Một lần sửa sau các thí nghiệm ngày 22/10: nới ngưỡng degron (176 peptide huấn luyện, miền đánh giá vẫn 91), đường cong học, độ bền theo phân cụm lại, P3 tiền huấn luyện (âm), hiệu chuẩn P6, audit Koren (cổng P2 không đạt), kèm tiến độ và việc còn lại; thêm tài liệu nội bộ [11–15]. Mọi số lấy từ các `results.json` tương ứng; đều là benchmark phát triển OOF, không phải kiểm chứng ngoài. Không đổi trạng thái G2/G3. `validate()` vẫn chỉ kiểm 91/89/47.847 và 0,8082/0,7693 từ `g2-saturation`; các số mới chưa có kiểm tự động. `validation.json` (ngày `2026-10-21` cố định trong `build.py`) được ghi lại bởi lần build này.

## Dựng và kiểm

```bash
make -C topics/degron-footprint/proposal
make -C topics/degron-footprint/proposal check
```

Cần Python 3 (thư viện chuẩn), Pandoc, XeLaTeX, Poppler và bộ Times New Roman trong `/mnt/c/Windows/Fonts/`. Build lặp XeLaTeX đến khi file aux ổn định; dừng nếu thiếu glyph, tràn khung hoặc tham chiếu lỗi. Kiểm đủ bảy phần trong cả Word/PDF, khổ giấy, font nhúng và số liệu. File trung gian nằm trong `build/` và bị gitignore. PDF xem trước cần kiểm trực quan sau mỗi thay đổi bố cục.
