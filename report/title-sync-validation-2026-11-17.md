# Chốt tên đề tài (D-1/D-3) — 17/11/2026

Tác giả chọn tên cuối ngày 17/11/2026. Xuất phát từ phương án 3 (bản gọn) trong
phiên phân tích tên, **bỏ cụm `Across the Full PSI Range`**. So với tên 16/11,
tên mới bỏ `Sequence-Based`, đổi `an Analysis Tool` thành `a Web Application`
vì phần mềm đã thành ứng dụng web v0.2 đầy đủ (nhánh 2 trong `plan.md`).

- **Tiếng Anh (mới):** Predicting Single-Residue Mutation Effects on PSI in Degron Reporter Assays and Development of a Web Application
- **Tiếng Anh (cũ, 16/11):** Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Reporter Assays and Development of an Analysis Tool
- **Tiếng Việt (mới):** Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong assay reporter degron và xây dựng ứng dụng web
- **Tiếng Việt (cũ, bản đăng ký):** Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong nghiên cứu degron và xây dựng công cụ phân tích

Tên tiếng Việt mới **khác bản đã đăng ký** trong đề cương (git `788851c`). Đóng
D-3 về phía tác giả; **GVHD chưa ghi nhận**.

## Tệp đã sửa

| Tệp | Thay đổi | SHA-256 sau sửa |
| --- | --- | --- |
| `report/config/metadata.tex` | `\ThesisTitle`, `\ThesisTitleVI`, chú thích nguồn tên | `08d7b8c75fcf75c8b3e1ff5258f5b357cb55e4043a8ab8ca03806b2868c3e182` |
| `report/frontmatter/abstract.tex` | `a local analysis tool` → `a web application` | `a9f84f6d004d9c3100cc0f1baccf2df573866eb2be46c18a68e52ff24fc2ac12` |
| `report/frontmatter/abstract-vi.tex` | `công cụ phân tích local` → `ứng dụng web` | `3a697cde9a08ee3fcfce65efab4e6e41be277df5a3f62905e52391ae5f1edc97` |
| `report/build/content/content.pdf` | dựng lại | `0930485bb35cb8a6fe056bf97ec671a25de6bbb1e7d4a3f67d19efbd5972285c` |
| `report/build/content-twoside/content.pdf` | dựng lại | `69f7f422f1b2f3699c50cd39d1ef388bf2cfca82fe9672037ad32cd050d15bbf` |

Ngoài ra: `report/README.md` (tên hiện hành) và `plan.md` (D-1, D-3, nhật ký).
Đầu trang `SINGLE-RESIDUE MUTATION EFFECTS ON PSI` vẫn khớp tên mới, không đổi.

## Kết quả kiểm [ĐO 17/11/2026]

| Kiểm | Kết quả |
| --- | --- |
| `make -C report all` | PASS (exit 0), references resolved |
| `make -C report check` | PASS — 148 trang một mặt, 148 trang hai mặt, smoke 9 trang; A4; phông nhúng |
| `scripts/check_float_references.py` | PASS — 23 hình, 66 bảng, khớp cả hai bản |
| Metadata PDF (`pdfinfo` Title) | khớp từng ký tự `\ThesisTitle` |
| Bìa ngoài, trang 1, render 60 dpi | tên ngắt hai dòng cân đối, không tràn khung |

Số trang không đổi so với lượt 17/11 trước (148/148).

## Chưa làm

- **Slide** (`presentation/research-report/`) chưa dựng lại, vẫn mang tên cũ;
  việc này gộp vào lượt dựng deck bảo vệ (nhánh 4).
- Các README/biên bản cũ (08/11, 16/11) giữ nguyên làm lịch sử.

## Phạm vi

Chỉ đổi tên và cụm mô tả phần mềm trong Abstract/Tóm tắt. Không đổi số liệu,
hình, bảng, giới hạn bằng chứng; không chạy campaign; không đóng G3; không
commit/push. Build PDF không đồng nghĩa nghiệm thu nghiên cứu.
