# Kiểm tra template luận văn — 21/10/2026

Template được dựng lại từ template báo cáo NCKH (kiểm ngày 09/10/2026) theo
`guideline-thesis/` và ba luận văn mẫu trong `resources/reference-theses/`.
Ô trong ngoặc vuông là placeholder chủ ý.

## PDF đã tạo

| Tệp | Số trang |
| --- | ---: |
| `build/content/content.pdf` | 25 |
| `build/content-twoside/content.pdf` | 25 |
| `build/smoke/smoke.pdf` | 9 |

Bản trống gồm 2 bìa, 11 trang đầu (La Mã i–xiii), Phần 1 (1 trang), Phần 2
(bốn chương), Phần 3, References và hai phụ lục. Khung chương và phụ lục có 87
tiêu đề chương/mục (template NCKH cũ: 130).

## Lệnh tái tạo

```bash
make -C reportTemplate doctor
make -C reportTemplate clean all smoke
make -C reportTemplate check
make -C reportTemplate content smoke BIBLIOGRAPHY=bibtex   # nhánh natbib/BibTeX
make -C reportTemplate check
```

## Kết quả

- Cả ba PDF đều A4, Times New Roman nhúng đủ phông; `make check` đạt ở cả
  nhánh biblatex/Biber và nhánh BibTeX.
- Log cuối không có lỗi LaTeX, tràn khung, tham chiếu/trích dẫn chưa giải
  quyết, nhãn lặp hay thiếu ký tự. `make check` xác nhận có đủ các tiêu đề:
  Thesis Revision Confirmation, Comments of the Advisor, Acknowledgements,
  Commitment to Results, Abstract, Tóm tắt, Table of Contents, List of
  Figures/Tables, Glossary and Abbreviations, Part 1/2/3, Chương 1 và 4,
  References, Appendix A; và không còn chữ của báo cáo NCKH.
- Đã xem trực quan: hai bìa, trang xác nhận chỉnh sửa, nhận xét GVHD, mục
  lục (chương, mục, mục con), danh mục bảng, thuật ngữ, Phần 1, chương 1
  (nhãn PART 2 phía trên chương, bảng đặc tả use case), phụ lục, và trong
  `smoke.pdf` hình, bảng, công thức, trích dẫn `[1]`, References. Chân trang
  và đầu trang có đường kẻ ở phần thân; trang trước mục lục chỉ có số trang.
- Đã build thử một bản sao có tên luận văn dài, tên phụ, hai GVHD và tên có
  dấu tiếng Việt: bìa, trang xác nhận và đầu/chân trang không tràn; bản hai
  mặt giữ vị trí đầu/chân trang như bản một mặt.
- Rà soát nguồn: không còn tham chiếu tới `deliverables/`, `config/members`,
  `\PendingField`, hay tệp `.bib` tách loại.

## Chưa kiểm tra / khác biệt đã biết

- Chưa đối chiếu PDF với bản Word từng pixel: lề, cỡ chữ và dàn ý theo mẫu của
  Khoa, nhưng mẫu Word là khổ Letter, template dùng A4.
- Header/footer theo mẫu của Khoa; ba luận văn mẫu chỉ in số trang ở giữa
  (cách chuyển ghi trong `README.md`).
- Chữ cố định là tiếng Anh; chưa có phiên bản tiếng Việt.
- Nội dung các chương chỉ là khung tiêu đề và comment hướng dẫn, chưa kiểm
  tra với văn bản dài thật (hình lớn, bảng nhiều trang ngoài use case).

## Danh sách tệp nguồn

Đường dẫn tương đối với `reportTemplate/`; ngoài danh sách này có ba PDF trong
`build/` (tệp phụ và log bị Git bỏ qua) và thư mục `guideline-thesis/` (tài
liệu hướng dẫn của Khoa, đặt ngoài template).

```text
.gitignore
Makefile
README.md
VALIDATION.md
appendices/a-installation-user-guide.tex
appendices/b-supplementary-materials.tex
assets/README.md
assets/diagrams/.gitkeep
assets/figures/.gitkeep
bibliography/references.bib
chapters/01-problem-description.tex
chapters/02-theoretical-background.tex
chapters/03-solution-design.tex
chapters/04-testing-evaluation.tex
chapters/conclusion.tex
chapters/introduction.tex
config/metadata.tex
examples/formatting.tex
examples/references.bib
frontmatter/abstract-vi.tex
frontmatter/abstract.tex
frontmatter/acknowledgements.tex
frontmatter/advisor-comments.tex
frontmatter/commitment.tex
frontmatter/cover.tex
frontmatter/glossary.tex
frontmatter/revision-confirmation.tex
frontmatter/title-page.tex
logo-ctu.png
main.tex
scripts/build.py
scripts/check_template.py
scripts/doctor.py
template/bibliography.tex
template/commands.tex
template/ctu-thesis.cls
template/packages.tex
template/typography.tex
```
