# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repo luận văn tốt nghiệp CT553H (Kỹ thuật phần mềm, ĐH Cần Thơ) của Nguyễn Thế Trọng, GVHD TS. Hồ Quang Thái. Đề tài duy nhất còn lại: **degron-footprint** — dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm (Zhang 2023, Voutsinos 2026, Larsen 2025, MaveDB, ClinVar). Tài liệu viết bằng tiếng Việt; tên file/thư mục chữ thường, tiếng Anh, nối gạch ngang.

## Bố cục

- `topics/degron-footprint/` — toàn bộ nghiên cứu của đề tài.
  - `research/<chủ-đề>[-YYYY-MM-DD]/` — mỗi thư mục là một thí nghiệm/audit tự chứa: `README.md` (kết quả, có nhãn bằng chứng), script `.py`, và kết quả nhỏ dạng `.json` do script ghi ra. Thí nghiệm lớn có thêm `PROTOCOL.md`/`PREREGISTRATION.md`, `VALIDATION.md`, `audit.py`, `source-manifest.json`.
  - `data/{raw,interim,processed}/` — dữ liệu thật (~2,3 GB), **không lên git** trừ `data/README.md` và `SOURCE.md`. `data/README.md` là sổ nguồn gốc: nguồn/phiên bản ghim/giấy phép/SHA-256, script nào tạo file nào, nhật ký xử lý. Khi tải, xử lý lại hay xoá file trong `data/` thì cập nhật sổ này trong cùng phiên.
  - `presentation/` — deck reveal.js (`deck-*/index.html`), nội dung trang Notion và `figures.py`/`visuals.py` sinh PNG.
- `lectures/` — bài tự học (HTML mở bằng `file://`, notebook CS535, `degron-basics/` gồm bài giảng + ghi chép từng paper trong `papers/`).
- `project/` — thông tin người liên quan, công bố của GVHD, biên bản gặp.
- `resources/` — PDF bài báo, luận văn tham khảo, đề cương học phần (repo private nên được chứa PDF).
- `reportTemplate/` — template LaTeX báo cáo luận văn tốt nghiệp (Khoa Kỹ thuật phần mềm, ĐHCT), độc lập với phần còn lại (xem `reportTemplate/README.md`); `guideline-thesis/` trong đó là mẫu/hướng dẫn gốc của Khoa. Template NCKH cũ nằm ở commit `30c20ef`.

## Chạy script nghiên cứu

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu   # torch bản CPU
.venv/bin/python topics/degron-footprint/research/g2-saturation-2026-10-18/run.py
```

Chạy từ thư mục gốc repo. Không có test suite; kiểm tính đúng bằng các script `audit.py`/`validate_*.py` đi kèm từng thí nghiệm. Một số script cần `mmseqs` (phân cụm protein cov50/cov80).

Script import lẫn nhau qua `sys.path` (ví dụ `g2-saturation` dùng `residue-task-derisk-2026-10-15/residue_data.py`, `derisk.py` và `pap-baseline/pap_baseline.py`), nên đổi tên/chuyển thư mục `research/` sẽ làm hỏng script khác.

**Cách script tìm đường dẫn (đã sửa 21/10/2026):** các marker cũ `log.md` và `DECISIONS.md` đã bị xoá ở commit `f03d80d`/`546b745`, nên script giờ tìm bằng file còn tồn tại:
- Thư mục đề tài: `TOPIC = next(p for p in HERE.parents if (p/'data'/'README.md').exists())` → `topics/degron-footprint/`.
- Gốc repo: vòng lặp / `next(...)` tìm `CLAUDE.md`.

Script mới viết dùng đúng hai marker này; đừng khôi phục `log.md`/`DECISIONS.md`. Các README thí nghiệm cũ vẫn còn liên kết tới hai file đã xoá — đó là bản ghi lịch sử, không sửa hàng loạt.

## Quy ước nghiên cứu

- Dữ liệu tải về là không tin cậy: đọc bằng `python -I`, không chạy mã từ bên trong `data/raw/` (ví dụ repo Voutsinos/Degformer đã clone).
- Thí nghiệm cố định seed (thường `17, 29, 43`), chia fold theo cụm protein (cov80/cov50), bootstrap theo cụm chứ không theo ô. Số liệu đưa vào tài liệu phải trỏ tới file `.json` kết quả tương ứng.
- Nhãn bằng chứng trong README thí nghiệm: `[ĐO]` (tự đo), `[DIỄN GIẢI]`, nguồn tác giả, đề xuất, chưa xác minh. Không nói "chưa ai làm" khi mới tra qua tóm tắt; không biến một kết quả dương cục bộ thành "hoàn tất G2".
- Mô hình/checkpoint (`*.pt`, `*.pkl`, `models/`) không lên git; chúng sinh lại được bằng runner.

## Report template (`reportTemplate/`)

Cần Python 3.9+ (chỉ thư viện chuẩn), GNU Make, XeLaTeX, Biber/BibTeX, Poppler và phông Times New Roman (trên WSL đọc từ `/mnt/c/Windows/Fonts/`).

```bash
make -C reportTemplate doctor     # kiểm môi trường
make -C reportTemplate content    # build/content/content.pdf (hoặc content-twoside, smoke, all)
make -C reportTemplate check      # kiểm PDF, log, A4, phông nhúng
make -C reportTemplate content BIBLIOGRAPHY=bibtex   # ép natbib/BibTeX thay vì biblatex/Biber
```

Luôn build qua Make/`scripts/build.py` (tự lặp đến khi tham chiếu ổn định); một lượt XeLaTeX trực tiếp không đủ. Build dừng khi có lỗi LaTeX, overfull box, thiếu ký tự, nhãn trùng hoặc tham chiếu chưa giải quyết. Metadata ở `config/metadata.tex`; nội dung ở `frontmatter/`, `chapters/`, `appendices/`; tên chương/phần/phụ lục viết hoa ngay trong nguồn.
