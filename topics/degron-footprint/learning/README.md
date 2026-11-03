# Học tuần tự đề tài degron-footprint

Tài liệu học tiếng Việt cho người có nền tảng kỹ thuật phần mềm, mốc bằng chứng **03/11/2026**.
Mục tiêu là hiểu quá trình đã thực hiện, khái niệm, lý do lựa chọn và giới hạn của từng kết luận.
Đây là tài liệu học riêng, không thay luận văn hoặc protocol nghiên cứu.

Đầu ra: **[study-guide.pdf](study-guide.pdf)**, 62 trang, 19 chương tiếng Việt (mốc 03/11/2026). Nguồn ở `chapters/`, hình/sơ đồ ở `assets/`; 12 sơ đồ có bản `.drawio`
chỉnh sửa được. `evidence.json` giữ số liệu và SHA-256 nguồn; không dùng số minh họa như kết quả đo.
Các phần local đang dở chỉ mô tả **kế hoạch và lý do**, không công bố thứ hạng/metric từ kết quả chưa đủ.

## Lộ trình

1. Cách đọc bằng chứng và bản đồ bài toán.
2. Sinh học nền, phép đo GPS, PSI và ΔPSI.
3. Nguồn dữ liệu, dựng nhãn, QC, trình tự và tọa độ.
4. Chia tập, mô hình đối chứng, cách đọc metric/CI.
5. Các thực nghiệm lịch sử, mở rộng nhãn, ESM/CNN và full-PSI.
6. Calibration, domain gate, kế hoạch train local và bằng chứng còn thiếu.
7. Phần mềm, quy trình tái lập, câu hỏi tự kiểm và hướng đi tiếp theo.

## Kỹ năng được áp dụng

- [Notion research documentation](/home/ngthtrong/.codex/plugins/cache/openai-curated-remote/notion/3.0.3/skills/notion-research-documentation/SKILL.md): tổng hợp nguồn, phân biệt đo/diễn giải/kế hoạch và kiểm chứng đầu ra. Đầu ra theo yêu cầu là PDF local; không ghi vào Notion.
- [Draw.io skill](../../../.agents/skills/drawio-skill/SKILL.md), bản ghim tại [SOURCE.md](../../../.agents/skills/drawio-skill/SOURCE.md): sơ đồ XML chỉnh sửa được, kiểm cấu trúc, render và xem ảnh.

Không phục hồi hồ sơ đánh giá học tập cũ đã vắng trong checkout; câu hỏi trong sách là bài tự kiểm mới,
không phải câu trả lời hoặc đánh giá năng lực đã được ghi nhận của người học.

## Bắt đầu đọc

Đọc chương 1–8 trước để hiểu sinh học, phép đo, nhãn và đánh giá; chương 9–13 giải thích
các thực nghiệm và bằng chứng Kaggle; chương 14 chỉ nói kế hoạch local; chương 15–16 nối
nghiên cứu với phần mềm và các việc còn thiếu. Chương 17 có bài thực hành/gợi ý đáp án,
chương 18 là từ điển, chương 19 là danh mục nguồn có liên kết trong PDF.

Đừng dùng tài liệu này thay hướng dẫn chạy campaign. Không chạy lại train, thay dependency
CUDA, đọc kết quả fit local đang dở hoặc tự đóng scientific gate khi build sách.

## Nguồn và mức bằng chứng

- [source-map.md](source-map.md): 31 nguồn nội bộ đã đối chiếu, đường dẫn và hash.
- [evidence.json](evidence.json): số liệu chọn lọc và danh mục nguồn; local chỉ đọc plan.
- [figure-manifest.json](figure-manifest.json): 8 biểu đồ/heatmap từ kết quả đã lưu, 1 ví dụ tự đặt,
  1 ảnh giao diện fixture; tổng 10 hình ngoài sơ đồ.
- [diagram-manifest.json](diagram-manifest.json): 12 sơ đồ; kiểm cấu trúc không lỗi/cảnh báo.
- [validation.json](validation.json) và [validation.md](validation.md): kiểm PDF, nguồn, font,
  tính đầy đủ nhãn sơ đồ và phạm vi nội dung.

Các kết quả lịch sử, full-PSI và các nguồn dữ liệu khác endpoint được trình bày riêng.
Tài liệu không báo cáo metric local hoặc chứng nhận phần mềm chưa được nghiệm thu.

## Dựng lại trong môi trường riêng

Cần Pandoc, XeLaTeX, Poppler (`pdfinfo`, `pdffonts`, `pdftotext`) và font DejaVu.
Ví dụ Linux/WSL, chạy từ gốc repository; môi trường đặt ở `/tmp` để tách khỏi CUDA campaign:

```bash
python3 -m venv /tmp/ct553h-learning-venv
/tmp/ct553h-learning-venv/bin/python -m pip install \
  -r topics/degron-footprint/learning/requirements.txt
make -C topics/degron-footprint/learning \
  PYTHON=/tmp/ct553h-learning-venv/bin/python
make -C topics/degron-footprint/learning previews \
  PYTHON=/tmp/ct553h-learning-venv/bin/python
```

Build đọc lại 31 nguồn nhỏ, sinh lại biểu đồ và PDF, lặp XeLaTeX tới khi tham chiếu ổn định,
rồi chạy kiểm tra. Không cần raw ZIP, GPU hay weights để dựng sách từ kết quả đã lưu.
Giữ `build/` và `previews/` ngoài Git; PDF chính, nguồn, ảnh và `.drawio` được lưu cùng tài liệu.

## Sửa và xuất lại sơ đồ

Mở `assets/diagrams/*.drawio` bằng diagrams.net/Draw.io. PNG là preview, PDF vector dùng trong sách.
Muốn sinh lại bằng script cần **Draw.io Desktop native CLI**. Bản đã dùng: 32.6.1 từ
[release chính thức](https://github.com/jgraph/drawio-desktop/releases/tag/v32.6.1), có Xvfb trên Linux headless.
Không đóng gói executable hoặc môi trường Python vào repository.

```bash
DRAWIO_BINARY=/path/to/drawio \
  /tmp/ct553h-learning-venv/bin/python -I \
  topics/degron-footprint/learning/scripts/generate_diagrams.py
```

Trên Linux headless có thể chạy trong `xvfb-run -a`, hoặc đặt `XVFB_BINARY` tới Xvfb để script
tạo display tạm. Nếu giải nén thư viện hệ thống vào thư mục riêng, đặt `LD_LIBRARY_PATH` phù hợp.
Script dùng `--crop` khi xuất PDF; nếu thiếu cờ này, native export có thể cắt sơ đồ theo trang Letter.
Kiểm tra đọc toàn bộ nhãn trong PDF sơ đồ giúp bắt lỗi đó, ngoài việc xem PNG.

Sau khi sửa nội dung/sơ đồ, build lại, chạy `make check`, xem contact sheet của **mọi trang**
và ảnh lớn các trang chứa bảng, công thức, hình hoặc đổi bố cục. Kiểm tự động không xác nhận
nội dung khoa học mới; phần mới vẫn phải truy nguyên về source, cohort và protocol.
