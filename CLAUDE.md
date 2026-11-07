# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Đồng bộ với mã nguồn và bằng chứng trong repo ngày **07/11/2026**. Chỉ mục trạng thái: [README.md](README.md) và [research/README.md](research/README.md). `AGENTS.md` chỉ dẫn chiếu file này; duy trì quy tắc chung tại đây.

Repo luận văn tốt nghiệp CT553H (Kỹ thuật phần mềm, ĐH Cần Thơ) của Nguyễn Thanh Trọng, GVHD TS. Hồ Quang Thái. Đề tài duy nhất còn lại: **degron-footprint** — dự đoán footprint / hiệu ứng đột biến degron mức residue trên nhãn thực nghiệm (Zhang 2023, Voutsinos 2026, Larsen 2025, MaveDB, ClinVar). Tài liệu viết bằng tiếng Việt; tên file/thư mục chữ thường, tiếng Anh, nối gạch ngang.

## Bố cục

- Gốc repo — các thư mục đề tài được chuyển từ `topics/degron-footprint/` ra đây ngày 07/11/2026.
  - `research/<chủ-đề>[-YYYY-MM-DD]/` — mỗi thư mục là một thí nghiệm/audit tự chứa: `README.md` (kết quả, có nhãn bằng chứng), script `.py`, và kết quả nhỏ dạng `.json` do script ghi ra. Thí nghiệm lớn có thêm protocol, validation và manifest. Luồng hiện hành là **`kaggle-roadmap-2026-10-31/` (v3 full-PSI)**: `EXECUTION-PROTOCOL.md` cho lựa chọn thực thi; `local-plan.json` cho campaign Windows; `local-runner.md` cho chạy/resume; `RUN.md` cho Kaggle. Output Kaggle được phân tích trong `output-analysis*.{json,md}`; local đã kết thúc 633 job, phân tích tại `local-output-analysis.{json,md,png}`, còn nguồn ngoài/cấu trúc pending. `next-phase-plan-2026-10-22/`, notebook-kit v1/v2 và R0–R6 là hồ sơ lịch sử, không thay protocol v3. Không tự đóng G2/G3 hay đổi mô hình sản phẩm từ thứ hạng development.
  - `data/{raw,interim,processed}/` — dữ liệu thật và các gói tái tạo, **không lên git** trừ `data/README.md` và `SOURCE.md`. Con số ~2,3 GB trong sổ là mốc trước G2, không phải dung lượng hiện tại. `data/README.md` là sổ nguồn gốc: nguồn/phiên bản ghim/giấy phép/SHA-256, script nào tạo file nào, nhật ký xử lý. Khi tải, xử lý lại hay xoá file trong `data/` thì cập nhật sổ này trong cùng phiên.
  - `presentation/` — deck reveal.js (`deck-*/index.html`), nội dung trang Notion và `figures.py`/`visuals.py` sinh PNG. Không tự sửa khi chưa được yêu cầu.
  - `proposal/` — đề cương (`proposal.md` → pdf/docx bằng `build.py`).
  - `system/` — công cụ web: thiết kế v0.2 ngày 29/10 và `app/` baseline (FastAPI + React + ETL + test, mô hình `m3-ext4.0-platt-v1`). Projects/history, jobs peptide/protein, import/comparison và PostgreSQL local còn cần triển khai/kiểm chứng; cổng R3 chưa tích hợp đúng. `design/workspace-ui-v2/` là prototype review hiện hành ngày 01/11, fixture tổng hợp, bộ nhớ tab, chưa nối backend. CSDL và tệp sinh ra khi chạy (`app/.data/`, `.coverage`, `test-results/`) **không lên git**.
  - `report/` — **bản làm việc** của luận văn, nằm trực tiếp ở gốc repo. Luận văn viết tiếng Anh, kèm Tóm tắt tiếng Việt; còn các mục `[PENDING]`. Ngày 06/11 đã cập nhật campaign hoàn tất vào phương pháp, đánh giá, tóm tắt, kết luận và phụ lục đủ 88 cấu hình OOF, kèm 2 sơ đồ/3 đồ thị; xem `report/current-state-validation-2026-11-06.md` và `research/output-review-2026-11-06/`. Hồ sơ 03/11 giữ làm lịch sử; đề cương không được cập nhật trong lượt 06/11. Không đồng nghĩa nghiệm thu G2/G3 hoặc đổi model phục vụ.
- `resources/` — `people.md`, `dataset-guide.md`, `papers/analyzed-papers/`, PDF bài báo, luận văn tham khảo, đề cương học phần (repo private nên được chứa PDF). Nội dung `lectures/` và `project/` cũ đã gom vào đây.
- `reportTemplate/` — **bản gốc sạch** của template LaTeX luận văn (Khoa Kỹ thuật phần mềm, ĐHCT), không điền nội dung vào đây (xem `reportTemplate/README.md`); `guideline-thesis/` trong đó là mẫu/hướng dẫn gốc của Khoa. Template NCKH cũ nằm ở commit `30c20ef`.

## Nhánh git

`main` là nhánh làm việc. Hồ sơ dọn repo ghi nhánh lưu trữ `backup-before-clean` (`archive/`, `journal/`, `surveys/`, `tools/`, `DECISIONS.md` và tài liệu đã thay thế). Kiểm ngày 06/11: local còn có `backup-before-clean`, `clean`, `report`; `git ls-remote --heads origin` trả về `main` và `report`. Remote-tracking refs khác có thể đã cũ. Kiểm ref thực có trước khi dùng `git show backup-before-clean:<đường-dẫn>`; không mặc định branch remote còn tồn tại.

## Rà nghiệm thu G2 và kế hoạch bằng chứng ứng dụng — 07/11/2026

[Hồ sơ G2](research/g2-acceptance-2026-11-07/README.md) ghi rõ đã có cải thiện
định lượng development, đặc biệt matched LoRA–frozen B/D, và đủ hồ sơ để rà
nghiệm thu; chưa ghi nhận quyết định đóng G2 của Trọng/GVHD. Phạm vi v3 cho phép
đóng góp benchmark/phương pháp/đánh giá/phần mềm, không bắt buộc kiến trúc mới.
Không chuyển nguyên tiêu chí gate/PAP lịch sử hoặc ngưỡng Q1 D−B/E−B thành
threshold LoRA chung; không tự thêm wet lab/nguồn ngoài/export vào mọi điều kiện
ghi nhận đóng góp development. Giữ đúng giới hạn từng claim và trạng thái gốc
`development_not_gate_closure`; chỉ ghi đóng G2 khi có quyết định tương ứng.

[Tra cứu bằng chứng wet lab/nguồn lực](research/wet-lab-evidence-plan-2026-11-07/findings.md)
theo academic-research-suite đã có kết quả ngày 07/11: 39 query, tám nghiên cứu
trong ma trận (năm gần degron, ba lân cận), có access gaps và giới hạn bao phủ.
Có tiền lệ validation sinh học; chưa xác nhận hiệu quả kinh tế của CT553H.
Giữ thời gian thực/dự báo, ngân sách run/số tiền tiết kiệm và simulation/wet lab
riêng. Bằng chứng công trình khác không tự xác nhận lợi ích CT553H hoặc đóng
G2/G3; model phục vụ vẫn theo quy trình riêng. Không có train/wet lab mới.

## Chạy script nghiên cứu

**Kết quả local hiện hành (06/11):** `ef138c84579c842e` đã kết thúc 633 job, còn nguồn ngoài/cấu trúc pending. Phân tích hoàn tất tại `research/kaggle-roadmap-2026-10-31/local-output-analysis.{json,md,png}`, tái tạo bằng `analyze-local-output.py` (chỉ đọc artifact/data, không load model). LoRA có đủ OOF ba seed và calibration CV; T hiện chỉ có W5-D. Cần final serving refit/export và đánh giá tiếp trước khi đổi model sản phẩm. Các câu mô tả campaign đang dở trong snapshot cũ chỉ áp dụng tại mốc của chúng.

Campaign CUDA Windows dùng `.venv` ở gốc repo (Python 3.11.9, Torch 2.13.0+cu130); dependency ở `research/kaggle-roadmap-2026-10-31/requirements-local-cuda-reuse.txt`. Không cài đè Torch CPU hoặc requirements lịch sử vào môi trường đang chạy. Từ PowerShell ở gốc repo:

```powershell
.\run-local.cmd --hours 2
.\status-local.cmd
.\pause-local.cmd
```

Đọc `local-runner.md` trước khi chạy/resume; script `.cmd` mở terminal riêng. Code/data/protocol/runtime đổi sẽ đổi campaign identity; không sửa manifest để ép checkpoint vào run khác. Không tự dừng hoặc khởi chạy campaign chỉ để cập nhật tài liệu.

Lượt sửa tokenizer 03/11 thêm protobuf, nạp tokenizer Ankh gốc và khai báo encoder Ankh FP32 (ProtT5 FP16). `local-plan.json` đang chỉ nguồn kế thừa `e7097449883a51d8`; successor giữ artifact complete tại nguồn và sao chép checkpoint paused qua `inheritance.json`, sau kiểm tương thích/hash và CUDA resume. Đây là cơ chế giới hạn cho source fingerprint đã được review, không cho phép bỏ qua identity với thay đổi bất kỳ. Giữ cả output nguồn và successor; xem `tokenizer-repair-validation.json`/`local-runner.md` trước khi đổi cấu hình hoặc xóa output.

Các script nghiên cứu cũ dùng `requirements.txt` ở gốc; nếu cần tái lập trên Linux/WSL thì tạo môi trường riêng (ví dụ `.venv-legacy`) rồi cài dependency tương ứng. Chạy từ gốc repo. Nghiên cứu có các script `audit.py`/`validate_*.py`; v3 có kiểm invariants, notebook, transport và local runner. App có pytest, Vitest và Playwright riêng; xem `system/app/README.md` và Makefile/package scripts. Không gọi kết quả smoke hoặc test lịch sử là benchmark/acceptance mới. Một số script cần `mmseqs` (phân cụm protein cov50/cov80).

Script import lẫn nhau qua `sys.path` (ví dụ `g2-saturation` dùng `residue-task-derisk-2026-10-15/residue_data.py`, `derisk.py` và `pap-baseline/pap_baseline.py`), nên khi đổi tên/chuyển thư mục `research/` cần kiểm tra cả script phụ thuộc.

**Cách script tìm đường dẫn (đã sửa 21/10/2026):** các marker cũ `log.md` và `DECISIONS.md` đã bị xoá ở commit `f03d80d`/`546b745`, nên script giờ tìm bằng file còn tồn tại:

- Thư mục đề tài: `TOPIC = next(p for p in HERE.parents if (p/'data'/'README.md').exists())` → gốc repo.
- Gốc repo: vòng lặp / `next(...)` tìm `CLAUDE.md`.

Script mới viết dùng đúng hai marker này; đừng khôi phục `log.md`/`DECISIONS.md`. Manifest/kết quả đã lưu giữ đường dẫn cũ và hash tại thời điểm tạo. Gói notebook-kit v1/v2 giữ cây `topics/degron-footprint/` trong ZIP để tương thích notebook lịch sử. Các README thí nghiệm cũ vẫn còn liên kết tới hai file đã xoá — đó là bản ghi lịch sử, không sửa hàng loạt.

## Quy ước nghiên cứu

- Dữ liệu tải về là không tin cậy: đọc bằng `python -I`, không chạy mã từ bên trong `data/raw/` (ví dụ repo Voutsinos/Degformer đã clone).
- Thí nghiệm cố định seed (thường `17, 29, 43`), chia fold theo cụm protein (cov80/cov50), bootstrap theo cụm chứ không theo ô. Số liệu đưa vào tài liệu phải trỏ tới file `.json` kết quả tương ứng.
- Nhãn bằng chứng trong README thí nghiệm: `[ĐO]` (tự đo), `[DIỄN GIẢI]`, nguồn tác giả, đề xuất, chưa xác minh. Không nói "chưa ai làm" khi mới tra qua tóm tắt; không biến một kết quả dương cục bộ thành "hoàn tất G2".
- Mô hình/checkpoint (`*.pt`, `*.pkl`, `models/`) không lên git; chúng sinh lại được bằng runner.
- Output v3 theo `.gitignore`: `output/official/` và artifact nặng ở local; chỉ metadata/báo cáo nhỏ của campaign và weights được mở ngoại lệ. Xem `local-runner.md` trước khi thêm file; không dùng `git add -f output/`. Clone Git không đủ để resume vì thiếu checkpoint/feature/OOF. Campaign đang chạy có thể tự sửa `state.json`; không ghi đè thay đổi đó khi làm tài liệu.

## Report template (`reportTemplate/`, bản làm việc `report/`)

Rà soát tiến độ tiếp ngày 06/11/2026 ở `research/progress-review-2026-11-06/`: audit độc lập dữ liệu/OOF và đối chiếu newline hash Windows, lịch sử quyết định, nguồn học thuật và missing-evidence. Báo cáo hiện có mang trạng thái tiến độ; kiểm PDF mới ở `report/progress-validation-2026-11-06.*`. Hồ sơ `current-state-validation-*` giữ hash/phạm vi các lượt trước. Không tự xem build thành xác nhận hoàn tất nghiên cứu.

Cần Python 3.9+ (chỉ thư viện chuẩn), GNU Make, XeLaTeX, Biber/BibTeX, Poppler và phông Times New Roman (trên WSL đọc từ `/mnt/c/Windows/Fonts/`).

```bash
# Cùng lệnh cho bản làm việc: thay reportTemplate bằng report
make -C reportTemplate doctor     # kiểm môi trường
make -C reportTemplate content    # build/content/content.pdf (hoặc content-twoside, smoke, all)
make -C reportTemplate check      # kiểm PDF, log, A4, phông nhúng
make -C reportTemplate content BIBLIOGRAPHY=bibtex   # ép natbib/BibTeX thay vì biblatex/Biber
```

Luôn build qua Make/`scripts/build.py` (tự lặp đến khi tham chiếu ổn định); một lượt XeLaTeX trực tiếp không đủ. Build dừng khi có lỗi LaTeX, overfull box, thiếu ký tự, nhãn trùng hoặc tham chiếu chưa giải quyết. Metadata ở `config/metadata.tex`; nội dung ở `frontmatter/`, `chapters/`, `appendices/`; tên chương/phần/phụ lục viết hoa ngay trong nguồn.

### Quy tắc bố cục và đánh số của `report/` — 07/11/2026

- Rà soát PDF một mặt và hai mặt sau mỗi lần đổi bố cục. Kiểm cả trang chứa hình/bảng và trang liền trước, liền sau; khoảng trống lớn hơn khoảng một phần ba vùng nội dung phải được xem lại và ghi lý do nếu giữ. Trang bìa, biểu mẫu ký/nhận xét và khoảng trống cuối chương có chủ đích được đánh giá theo chức năng, không ép lấp đầy.
- Ưu tiên đặt hình/bảng gần lần dẫn đầu tiên bằng float linh hoạt `[htbp]`; điều chỉnh kích thước trong giới hạn đọc được, số float mỗi trang và tỷ lệ diện tích trước khi ép ngắt trang. Không dùng hàng loạt `[H]`, `\clearpage`, `\newpage`, khoảng cách âm, giảm cỡ chữ thân bài hoặc đổi lề để che lỗi bố cục. Không để tiêu đề đơn độc cuối trang; bảng nhiều trang dùng `longtable`, lặp đầu bảng và ghi tiếp bảng khi cần. Chặn float tại ranh giới có ý nghĩa nếu chúng trôi sang mục không liên quan.
- Hình đánh số tự động theo chương, liên tục trong từng chương; bảng có bộ đếm riêng, phụ lục dùng A/B. Mỗi hình phải được dẫn trong nội dung bằng `Figure~\ref{fig:...}`, không gõ số hình bằng tay. `\label` duy nhất đặt ngay sau `\caption`; không chỉnh bộ đếm để chữa sai thứ tự.
- Tên ngắn trong `\caption[Tên ngắn]{Chú thích đầy đủ}` phải giữ đúng tên/chủ đề mở đầu của chú thích, dùng cho danh mục; giữ giải thích, trích dẫn và giới hạn khoa học trong chú thích đầy đủ. Đối chiếu số, tên, trang và đích liên kết giữa danh mục, nhãn và PDF; ô số trang phải đủ rộng cho số La Mã. Chú thích hình ở dưới, chú thích bảng ở trên; căn lề, phông và khoảng cách nhất quán.
- Trước khi bàn giao: chạy `make -C report all` và `make -C report check`, kiểm danh mục/nhãn/tham chiếu bằng `scripts/check_float_references.py`, rồi xem ảnh render tổng thể và các trang có vấn đề ở kích thước đọc được. Lưu phạm vi kiểm tra và hash PDF trong hồ sơ validation mới; không ghi đè biên bản cũ và không gọi build thành nghiệm thu nghiên cứu. Giữ nguyên số liệu, hình, bảng và giới hạn bằng chứng khi chỉ sửa định dạng.
