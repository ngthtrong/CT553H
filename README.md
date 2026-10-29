# Luận văn tốt nghiệp CT553H

Kho nghiên cứu và báo cáo luận văn của **Nguyễn Thanh Trọng** (B2305615), GVHD **TS. Hồ Quang Thái**, ngành Kỹ thuật phần mềm, Đại học Cần Thơ.

Đề tài **degron-footprint** tập trung dự đoán hiệu ứng đột biến ở từng vị trí amino acid trên nhãn thực nghiệm, kèm công cụ phân tích. Kết quả và giới hạn của từng thí nghiệm nằm trong README và tệp kết quả tương ứng.

## Cấu trúc hiện tại

| Thư mục | Nội dung |
| --- | --- |
| [topics/degron-footprint/research/](topics/degron-footprint/research/) | Thí nghiệm, audit, script và kết quả nhỏ; xem [tổng hợp lựa chọn mô hình](topics/degron-footprint/research/model-selection-pipeline-2026-10-24/README.md). |
| [topics/degron-footprint/data/](topics/degron-footprint/data/README.md) | Nguồn gốc và hướng dẫn dữ liệu; dữ liệu thô/trung gian/đã xử lý không đưa lên Git. |
| [topics/degron-footprint/report/](topics/degron-footprint/report/README.md) | Bản luận văn đang viết, đã chuyển từ `report/` ở gốc. |
| [topics/degron-footprint/proposal/](topics/degron-footprint/proposal/README.md) | Đề cương và hướng dẫn dựng PDF/DOCX. |
| [topics/degron-footprint/system/](topics/degron-footprint/system/README.md) | Thiết kế và ứng dụng FastAPI + React. |
| [topics/degron-footprint/presentation/](topics/degron-footprint/presentation/) | Slide và tài liệu trình bày. |
| [resources/](resources/) | [Thông tin người tham gia](resources/people.md), [đề cương học phần](resources/CT553H.pdf), [hướng dẫn dữ liệu](resources/dataset-guide.md), [luận văn tham khảo](resources/reference-theses/). |
| [resources/papers/](resources/papers/) | [Ghi chép phân tích bài báo](resources/papers/analyzed-papers/README.md), [PDF degron](resources/papers/degron/README.md), [hướng nghiên cứu GVHD](resources/papers/advisor-research.md), công bố của [Hồ Quang Thái](resources/papers/ho-quang-thai/ho-quang-thai.md) và [Yu-Yen Ou](resources/papers/yu-yen-ou/yu-yen-ou.md). |
| [reportTemplate/](reportTemplate/README.md) | Template LaTeX gốc sạch, tách khỏi bản luận văn đang viết. |

Ghi chép và hồ sơ trước đây ở `lectures/`, `project/` đã được gom vào `resources/`. Các đường dẫn trong bản ghi thí nghiệm lịch sử có thể vẫn phản ánh bố cục cũ.

## Bắt đầu

Chạy lệnh từ gốc repository. Hướng dẫn nghiên cứu và quy tắc đóng góp nằm trong [CLAUDE.md](CLAUDE.md), được [AGENTS.md](AGENTS.md) dẫn chiếu.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Huấn luyện trên Kaggle: xem [RUN.md](topics/degron-footprint/research/notebook-kit-2026-10-22/RUN.md) để chuẩn bị gói và mang kết quả về. Cài đặt ứng dụng theo [README của app](topics/degron-footprint/system/app/README.md).

Biên dịch luận văn cần GNU Make, XeLaTeX, Biber/BibTeX, Poppler và Times New Roman:

```bash
make -C topics/degron-footprint/report doctor
make -C topics/degron-footprint/report content
make -C topics/degron-footprint/report check
```

PDF nằm tại `topics/degron-footprint/report/build/content/content.pdf`. Template sạch dùng cùng lệnh với `-C reportTemplate`.

## Tệp đưa lên Git

Giữ mã nguồn, tài liệu, kết quả nhỏ và tài sản hình/sơ đồ. Bỏ qua dữ liệu nghiên cứu (ngoại trừ sổ nguồn gốc `README.md` và `SOURCE.md`), checkpoint, môi trường ảo, cache, CSDL ứng dụng, bí mật và tệp biên dịch trung gian. Hai bản LaTeX cho phép giữ ba PDF chính trong `build/{content,content-twoside,smoke}/` theo `.gitignore` riêng.
