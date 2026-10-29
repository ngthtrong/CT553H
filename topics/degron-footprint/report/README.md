# Luận văn degron-footprint

Bản luận văn đang viết của **Nguyễn Thanh Trọng** (B2305615), GVHD **TS. Hồ Quang Thái**. Thư mục này đã chuyển từ `report/` ở gốc vào `topics/degron-footprint/report/`, cạnh mã nghiên cứu và ứng dụng của đề tài.

Bản làm việc được tạo từ [template sạch](../../../reportTemplate/README.md), đã điền metadata và nội dung đề tài. Các mục `[PENDING]` hoặc ô trong ngoặc vuông còn lại cần được hoàn thiện; không dùng thư mục template gốc để viết luận văn.

- [main.tex](main.tex): điểm vào LaTeX.
- [config/metadata.tex](config/metadata.tex): thông tin bìa, sinh viên và GVHD.
- [assets/README.md](assets/README.md): hình, sơ đồ và tài sản trình bày.
- [VALIDATION.md](VALIDATION.md): bản ghi kiểm tra trước đây; không phải xác nhận đã build lại sau khi di chuyển.
- Mẫu của Khoa nằm trong `guideline-thesis/`; luận văn tham khảo nằm ở [resources/reference-theses/](../../../resources/reference-theses/).

Các hướng dẫn định dạng bên dưới kế thừa từ template.

## Quyết định thiết kế

| Nội dung | Chọn | Lý do |
| --- | --- | --- |
| Ngôn ngữ | Tiếng Anh; trang Tóm tắt tiếng Việt | Cả ba luận văn mẫu viết tiếng Anh, Khánh thêm Tóm tắt; mẫu của Khoa có cả TÓM TẮT và ABSTRACT. Chữ cố định (tiêu đề chương, tên hình/bảng) nằm ở `template/commands.tex` và `frontmatter/`; chuyển sang tiếng Việt cần sửa các tệp đó và dòng `\setdefaultlanguage` trong `template/typography.tex`. |
| Khổ giấy | A4 | Hai trong ba luận văn mẫu dùng A4 (mẫu Word của Khoa là Letter). |
| Cỡ chữ/giãn dòng | Times New Roman 13 bp, giãn 1,3, thụt dòng đầu 1,27 cm | Mẫu của Khoa dùng 13 pt, giãn khoảng 1,25. |
| Lề | Trái 3,5 cm, phải 2 cm, trên/dưới 3 cm | Theo mẫu của Khoa (Khánh cũng dùng). |
| Đầu/chân trang | Tên luận văn ở đầu trang; họ tên + MSSV bên trái chân trang, số trang bên phải | Theo mẫu của Khoa. Ba luận văn mẫu chỉ in số trang ở giữa; muốn như vậy, đổi `\pagestyle{thesis}` thành `thesisplain` trong `main.tex` và `\chapterpagestyle` trong `template/ctu-thesis.cls`. |
| Tài liệu tham khảo | IEEE, đánh số theo thứ tự trích dẫn, một tệp `bibliography/references.bib` | Cả ba luận văn mẫu dùng số thứ tự. |

## Cấu trúc tài liệu

Trang bìa không đánh số; phần đầu dùng số La Mã bắt đầu từ trang xác nhận
chỉnh sửa; phần thân dùng số Ả Rập bắt đầu từ 1.

| Thứ tự | Nội dung | Tệp |
| --- | --- | --- |
| 1–2 | Bìa chính, bìa phụ | `frontmatter/cover.tex`, `title-page.tex` |
| 3 | Thesis Revision Confirmation (xác nhận chỉnh sửa theo hội đồng) | `frontmatter/revision-confirmation.tex` |
| 4 | Comments of the Advisor (chừa dòng chấm để GVHD viết) | `frontmatter/advisor-comments.tex` |
| 5 | Acknowledgements | `frontmatter/acknowledgements.tex` |
| 6 | Commitment to Results | `frontmatter/commitment.tex` |
| 7–8 | Abstract, Tóm tắt | `frontmatter/abstract.tex`, `abstract-vi.tex` |
| 9 | Table of Contents, List of Figures, List of Tables | tự sinh |
| 10 | Glossary and Abbreviations | `frontmatter/glossary.tex` |
| 11 | **Part 1. Introduction** (mục 1.–7., mục con 3.1…) | `chapters/introduction.tex` |
| 12 | **Part 2. Content**: Chương 1 Problem Description, 2 Theoretical Background, 3 Solution Design and Implementation, 4 Testing and Evaluation | `chapters/01-…` đến `04-…` |
| 13 | **Part 3. Conclusion** (mục 1.–3.) | `chapters/conclusion.tex` |
| 14 | References | tự sinh |
| 15 | Appendix A (cài đặt, hướng dẫn sử dụng), Appendix B (tư liệu bổ sung) | `appendices/` |

Chương 1–4 giữ đúng dàn ý của Khoa (mô tả bài toán và đặc tả use case → cơ
sở lý thuyết → thiết kế và cài đặt → kiểm thử và đánh giá), có bổ sung mục
dữ liệu/phương pháp/mô hình và đánh giá thực nghiệm vì đề tài tin sinh có
phần nghiên cứu mô hình. Hai luận văn của Nhi và Bảo tách thành năm chương
(Giới thiệu, Cơ sở lý thuyết, Phương pháp, Kết quả, Triển khai và kết luận);
muốn theo kiểu đó, thêm/bớt tệp trong `chapters/` và các dòng `\include` trong
`main.tex`.

**Đã bỏ so với template NCKH:** bìa/bìa phụ "Báo cáo tổng kết", danh sách thành
viên và đơn vị phối hợp, thông tin kết quả nghiên cứu (tiếng Việt, tiếng Anh),
thông tin sinh viên chủ nhiệm, nhận xét của người hướng dẫn trong biểu mẫu
NCKH, bản tin và báo cáo tóm tắt (4 PDF), `config/members.tex`, hướng dẫn
nghiệm thu `HD.pdf` và `HinhThucBC.pdf`, bốn tệp `.bib` tách theo loại
(văn bản pháp quy/sách/bài báo), 130 tiêu đề chương/mục khái quát, hai phụ lục
tái lập NCKH, gói `pdfpages` và lệnh `\PendingField`. Nguồn gốc nằm trong lịch
sử Git (commit `30c20ef`).

Không đưa vào: trang "Comments of the Reviewers" (chỉ một luận văn mẫu có,
mẫu của Khoa không có). Cần thì thêm vào `main.tex` sau nhận xét GVHD một tệp
như `advisor-comments.tex` với `\FrontChapter{COMMENTS OF THE REVIEWERS}`.

## Cài đặt

Yêu cầu Python **3.9+**, GNU Make, XeLaTeX và Poppler. Python chỉ dùng thư viện
chuẩn; không cần môi trường ảo, pip hay latexmk.

```bash
sudo apt update
sudo apt install make python3 texlive-xetex texlive-latex-extra \
  texlive-lang-other texlive-fonts-recommended texlive-bibtex-extra \
  biber poppler-utils fontconfig
```

Cần Times New Roman đủ bốn kiểu Regular/Bold/Italic/Bold Italic. Cài phông có
quyền sử dụng rồi chạy `fc-cache -f`. Trên WSL, template cũng nhận bốn tệp
`times.ttf`, `timesbd.ttf`, `timesi.ttf`, `timesbi.ttf` tại
`/mnt/c/Windows/Fonts/`; dùng vị trí khác thì chỉnh `template/typography.tex`.
Template báo lỗi khi không tìm thấy phông, không tự thay bằng phông khác.
Chạy `make doctor` để kiểm tra thực tế.

## Biên dịch

Từ gốc repository dùng `make -C topics/degron-footprint/report <lệnh>`, hoặc vào
`topics/degron-footprint/report/` và dùng trực tiếp các lệnh dưới đây.

| Lệnh | PDF |
| --- | --- |
| `make content` | `build/content/content.pdf` — một mặt |
| `make content-twoside` | `build/content-twoside/content.pdf` — hai mặt (giữ lề trái 3,5 cm/phải 2 cm trên mọi trang, không ép chương mở ở trang lẻ) |
| `make smoke` | `build/smoke/smoke.pdf` — minh họa hình, bảng, công thức, trích dẫn, use case |
| `make all` | hai bản luận văn |
| `make check` | kiểm PDF, log, A4, phông nhúng, tiêu đề bắt buộc, không còn chữ của báo cáo NCKH |
| `make doctor` | kiểm môi trường |
| `make clean` | xóa `build/` |

Luôn build qua Make/`scripts/build.py` (tự lặp đến khi tham chiếu ổn định,
tự phát hiện `\citep`, `\cite`, `\nocite`); một lượt XeLaTeX trực tiếp không
đủ. Build dừng khi có lỗi LaTeX, tràn khung, thiếu ký tự, nhãn trùng hoặc
tham chiếu chưa giải quyết. Mặc định dùng biblatex-ieee/Biber, thiếu thì dùng
natbib/BibTeX (`make content BIBLIOGRAPHY=bibtex` để ép). Log nằm cạnh PDF.
Xem PDF bằng mắt sau khi thay nội dung: log không phát hiện được chữ đè logo
hay tiêu đề đầu trang quá dài.

## Điền thông tin

1. `config/metadata.tex`: tên luận văn (**viết hoa**, như bìa các luận văn
   mẫu), tên rút gọn cho đầu trang `\ThesisRunningTitle` (một dòng), sinh
   viên, MSSV, niên khóa, mã lớp, GVHD (hai GVHD thì điền `\AdvisorTwoName`),
   ngày bảo vệ, ba thành viên hội đồng, ngày ký. Thông tin Trường/Khoa cuối
   tệp.
2. Viết nội dung trong `frontmatter/` (Abstract, Tóm tắt, Lời cảm ơn, Thuật
   ngữ) và `chapters/`, `appendices/`. Dòng bắt đầu bằng `%` là hướng dẫn.
3. Tiêu đề **chương/phần/phụ lục viết hoa ngay trong nguồn**
   (`\chapter{PROBLEM DESCRIPTION}`); tiêu đề mục (`\section`, `\subsection`)
   viết hoa chữ đầu từ chính. Mục lục lấy nguyên văn tiêu đề.
4. Phần 1 và Phần 3 đánh số mục 1., 2., 3.1. (`\ThesisFlatNumbering`); các
   chương của Phần 2 và phụ lục đánh số 1.1., 1.1.1. (`\ThesisChapterNumbering`).
   Hình/bảng đánh số theo chương (`Figure 2.1.`); hình trong Phần 1 là `0.1`.
5. `\ThesisPart{PART 2. CONTENT}` đặt ngay trước `\chapter` đầu tiên: in nhãn
   phía trên tiêu đề chương và thêm dòng riêng trong mục lục.
6. Thêm thuật ngữ: bỏ comment dòng mẫu trong `frontmatter/glossary.tex`.
   Nếu đổi tên tệp, cập nhật `\input`/`\include` trong `main.tex`.

## Hình, bảng, công thức, use case

Đặt hình vào `assets/figures/` hoặc `assets/diagrams/`.

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=.8\textwidth]{ten-hinh.pdf}
  \caption{Figure title}\label{fig:ten-hinh}
\end{figure}

\begin{table}[htbp]
  \centering
  \caption{Table title}\label{tab:ten-bang}
  \begin{tabularx}{\textwidth}{|l|X|}
    \hline \textbf{Field} & \textbf{Description} \\ \hline
    ... & ... \\ \hline
  \end{tabularx}
\end{table}
```

Chú thích hình đặt dưới, chú thích bảng đặt trên; `\label` sau `\caption`.
Bảng dài dùng `longtable`. Công thức dùng `equation` (đánh số theo chương).
Gói tùy chọn (`listings`, `algorithm`, `siunitx`, `pdflscape`) bật ở cuối
`template/packages.tex` khi cần.

Bảng đặc tả use case của Khoa là môi trường `usecasespec` (xem
`chapters/01-problem-description.tex`): `\ucname`, `\ucactor`, `\ucfull`.
Xuống dòng trong ô dùng `\newline`, không dùng `\\`.

## Tài liệu tham khảo

Thêm bản ghi vào `bibliography/references.bib`, trích dẫn bằng
`\citep{khoa-tai-lieu}`. Dùng khóa duy nhất và bảo vệ tên riêng bằng `{...}`
trong tiêu đề.

```bibtex
@article{khoa-tai-lieu,
  author  = {[Last, First]},
  title   = {{[Article title]}},
  journal = {[Journal]},
  year    = {[Year]},
  volume  = {[Volume]},
  pages   = {[Pages]},
  doi     = {[DOI]}
}
```

`examples/references.bib` chỉ phục vụ `make smoke`, không dùng cho luận văn.
Kết quả kiểm tra của phiên bản này ghi tại `VALIDATION.md`.
