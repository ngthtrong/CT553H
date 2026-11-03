# Đề cương luận văn degron-footprint

Bản dự thảo ngày **21/10/2026**, soạn theo mẫu tiếng Việt của học phần. Tên đề tài là đề xuất cho bản thảo này, chưa phải tên được GVHD phê duyệt.

**Cập nhật chọn lọc 03/11/2026:** Markdown, PDF và DOCX đã phản ánh benchmark lịch sử, các kết quả quan trọng của v3 full-PSI, snapshot local 10:17 (UTC+8) và phạm vi ứng dụng local đã chốt. Đây là bản đề cương làm việc, chưa phải nghiệm thu G2/G3. Luồng nghiên cứu ở [research/README.md](../research/README.md); trạng thái triển khai ở [system/README.md](../system/README.md).

- [proposal.docx](proposal.docx): bản Word chỉnh sửa được, dùng DOCX đi kèm mẫu làm reference.
- [proposal.pdf](proposal.pdf): bản xem trước được biên dịch bằng XeLaTeX từ cùng nội dung Markdown. Ngắt trang có thể khác Word; chưa kiểm trực quan bằng Microsoft Word.
- [proposal.md](proposal.md): nguồn nội dung chung.
- [references.bib](references.bib): danh mục khởi đầu để nhập vào Zotero/Mendeley, giữ DOI và đường dẫn; cần đồng bộ lại trích dẫn nếu biên tập trực tiếp trong Word. Tác giả dài được rút gọn bằng `and others`; không phải thư viện trích dẫn đã được quản lý qua ứng dụng.
- [validation.json](validation.json): số trang, các kiểm tra tự động và SHA-256 của đầu vào/đầu ra.

## Bám mẫu

Mẫu gốc: [Đề cương LV Mau.pdf](../../../reportTemplate/guideline-thesis/Đề%20cương%20LV%20Mau.pdf) và [DOCX đi kèm](../../../reportTemplate/guideline-thesis/Đề%20cương%20LV%20Mau%20%281%29.docx).
Giữ 7 phần I–VII, các mục con và ba bảng quy trình/nguồn dữ liệu/dự án. Nội dung mở rộng theo bài toán sinh học và đánh giá mô hình nên dài hơn mẫu trống. Giữ khổ **Letter 612 × 792 pt**, lề 1 inch theo chính mẫu (không suy khổ A4 từ template báo cáo NCKH), phông Times New Roman.

Thông tin sinh viên/GVHD lấy từ [resources/people.md](../../../resources/people.md): Nguyễn Thanh Trọng, B2305615, TS. Hồ Quang Thái; thống nhất với `CLAUDE.md` hiện tại. Chỗ cần điền: MSCB của GVHD; lịch tuần chưa tự đặt khi chưa có lịch học phần.

## Bằng chứng và giới hạn

Nguồn số gồm JSON G2/P0/P3/P6, các lượt R0–R3/R6, [dataset-build.json](../research/kaggle-roadmap-2026-10-31/dataset-build.json), [output-analysis.json](../research/kaggle-roadmap-2026-10-31/output-analysis.json) và plan/queue/state của campaign local `e7097449883a51d8`. Hồ sơ SHA nguồn và đầu ra được ghi trong [validation.json](validation.json). Đường dẫn nội bộ giữ trong hồ sơ build, không in làm dẫn chứng trong đề cương. Không dùng hoặc khôi phục DECISIONS.md/log.md đã xóa.

Benchmark lịch sử giữ 91 peptide/89 cụm/47.847 ô; v3 full-PSI là 235 peptide/221 nhóm/122.412 ô, khác population và metric chính. Degformer sạch cụm đã chạy; LoRA local chưa đủ seed/fold. Nguồn giữ lại, calibration v3, final refit/export và nghiệm thu phần mềm còn dở. Baseline React/FastAPI tồn tại; workspace mới dùng fixture tổng hợp, chưa tích hợp. Không đổi mô hình phục vụ hoặc tự đóng G2/G3 từ thứ hạng development.

Tên chính thức của bài Zhang và MetaDegron được kiểm qua Crossref DOI API ngày 21/10/2026; tên Voutsinos lấy từ ghi chép bài đã lưu. Một số trang DOI/PMC/GEO không truy cập được qua công cụ web (500/CAPTCHA), nên không xem đó là kiểm chứng lại toàn văn. Trang GitHub Degformer đọc được; các mô tả sâu dựa trên audit ghim trong repository.

## Nội dung cập nhật 03/11/2026

Giữ các kết quả lịch sử có giá trị, bổ sung ngữ cảnh ±5, đối chứng ESM pointwise/CNN, lợi ích train toàn dải và scanning pre-training, kết quả âm của quality weighting. Cập nhật câu hỏi nghiên cứu, population/metrics, tiến độ và công việc còn lại; mở rộng phần mềm đúng phạm vi đã chốt. Hai nguồn phương pháp ESM2/LoRA được đối chiếu bằng bài báo gốc/metadata xuất bản. Các hồ sơ tính toán nội bộ được ghi là chưa xuất bản.

Builder đã sửa đường dẫn mẫu sau khi chuyển thư mục. `validate()` đối chiếu các số liệu mới và tiến độ local với JSON nguồn trong cả PDF/DOCX, kiểm không in đường dẫn bằng chứng nội bộ, khổ Letter, phông nhúng và lỗi LaTeX. Ngày tài liệu và thời điểm build được ghi riêng. Bản ghi kiểm trực quan và các giới hạn ở [validation cập nhật luận văn/đề cương](../report/current-state-validation-2026-11-03.md).

## Dựng và kiểm

```bash
make -C topics/degron-footprint/proposal
make -C topics/degron-footprint/proposal check
```

Cần Python 3 (thư viện chuẩn), Pandoc, XeLaTeX, Poppler và bộ Times New Roman trong `/mnt/c/Windows/Fonts/`. Build lặp XeLaTeX đến khi file aux ổn định; dừng nếu thiếu glyph, tràn khung hoặc tham chiếu lỗi. Kiểm đủ bảy phần trong cả Word/PDF, khổ giấy, font nhúng và số liệu. File trung gian nằm trong `build/` và bị gitignore. PDF xem trước cần kiểm trực quan sau mỗi thay đổi bố cục.
