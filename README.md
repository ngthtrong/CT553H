# Luận văn tốt nghiệp CT553H

Kho nghiên cứu và báo cáo luận văn của **Nguyễn Thanh Trọng** (B2305615), GVHD **TS. Hồ Quang Thái**, ngành Kỹ thuật phần mềm, Đại học Cần Thơ.

Đề tài **degron-footprint** tập trung dự đoán hiệu ứng đột biến ở từng vị trí amino acid trên nhãn thực nghiệm, kèm công cụ phân tích. Kết quả và giới hạn của từng thí nghiệm nằm trong README và tệp kết quả tương ứng.

## Trạng thái ngày 06/11/2026

| Mảng | Hiện trạng và điểm vào |
| --- | --- |
| Nghiên cứu | **v3 full-PSI** đã hoàn tất phần tính toán local: 633 job complete, nguồn ngoài/cấu trúc pending. [Phân tích local hoàn tất](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/local-output-analysis.md) kiểm artifact, OOF, frozen–LoRA, hiệu chuẩn và T; [phân tích Kaggle](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/output-analysis.md) giữ mốc riêng. Chưa đóng G2/G3 hoặc chọn lại mô hình sản phẩm. |
| Dữ liệu | Bundle v3 giữ saturation toàn dải PSI và scanning sau QC; nguồn, giấy phép, hash và nhật ký nằm trong [sổ dữ liệu](topics/degron-footprint/data/README.md), quy tắc dựng bundle ở [DATASET.md](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/DATASET.md). Dữ liệu và artifact nặng nằm local. |
| Ứng dụng | [Baseline FastAPI + React](topics/degron-footprint/system/app/README.md) có mã và kiểm thử lịch sử, dùng `m3-ext4.0-platt-v1`. [Phạm vi v0.2](topics/degron-footprint/system/README.md) gồm dự án/lịch sử, jobs peptide/protein, import/comparison; các phần mở rộng chưa được nghiệm thu. |
| Giao diện | [Workspace UI v2](topics/degron-footprint/system/design/workspace-ui-v2/README.md) là prototype tương tác hiện hành; dữ liệu minh hoạ, lưu trong bộ nhớ tab, chưa nối backend. |
| Luận văn / đề cương | [Luận văn](topics/degron-footprint/report/README.md) cập nhật campaign hoàn tất ngày 06/11: phương pháp, 88 cấu hình OOF, LoRA/calibration/T, sơ đồ và phụ lục; [audit tổng hợp](topics/degron-footprint/research/output-review-2026-11-06/README.md). [Đề cương](topics/degron-footprint/proposal/README.md) giữ bản 03/11. Còn `[PENDING]`; cập nhật tài liệu không phải nghiệm thu G2/G3. |

Trạng thái nghiên cứu đã đối chiếu output hoàn tất ngày 06/11; số test phần mềm lịch sử không phải kết quả kiểm lại hôm nay. Các snapshot tiến độ cũ giữ mốc riêng trong chỉ mục nghiên cứu.

## Cấu trúc hiện tại

| Thư mục | Nội dung |
| --- | --- |
| [topics/degron-footprint/research/](topics/degron-footprint/research/README.md) | Chỉ mục hiện hành, thí nghiệm, audit, script và kết quả nhỏ; v3 và bằng chứng lịch sử được dẫn riêng. |
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

Trên máy Windows hiện tại, `.venv` ở gốc đã được chuẩn bị cho CUDA. Xem [local-runner.md](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/local-runner.md) rồi dùng PowerShell:

```powershell
.\run-local.cmd --hours 2   # mở phiên chạy/tiếp tục trong terminal riêng
.\status-local.cmd         # xem trạng thái
.\pause-local.cmd          # yêu cầu dừng an toàn
```

Khi cần dựng môi trường CUDA lại, theo [local-cuda.md](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/local-cuda.md) và requirements ghim của v3. `requirements.txt` ở gốc phục vụ script nghiên cứu cũ; dùng môi trường riêng để không ghi đè runtime campaign.

Huấn luyện trên Kaggle v3: [RUN.md](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/RUN.md), [notebook tổng](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/ALL-IN-ONE.md) và [resume nhiều phiên](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/MULTI-SESSION.md). [Notebook-kit 22/10](topics/degron-footprint/research/notebook-kit-2026-10-22/RUN.md) dành cho tái lập R0–R6 lịch sử.

Chạy ứng dụng baseline theo [README của app](topics/degron-footprint/system/app/README.md). Makefile ứng dụng dùng Bash và đường dẫn môi trường Linux/WSL; frontend có thể cài/chạy bằng npm theo README riêng. Prototype Workspace UI v2 mở trực tiếp bằng trình duyệt theo hướng dẫn của nó.

Biên dịch luận văn cần GNU Make, XeLaTeX, Biber/BibTeX, Poppler và Times New Roman:

```bash
make -C topics/degron-footprint/report doctor
make -C topics/degron-footprint/report content
make -C topics/degron-footprint/report check
```

PDF nằm tại `topics/degron-footprint/report/build/content/content.pdf`. Template sạch dùng cùng lệnh với `-C reportTemplate`.

## Tệp đưa lên Git

Giữ mã nguồn, tài liệu, kết quả nhỏ và tài sản hình/sơ đồ. Bỏ qua dữ liệu nghiên cứu (ngoại trừ sổ nguồn gốc `README.md` và `SOURCE.md`), checkpoint, môi trường ảo, cache, CSDL ứng dụng, bí mật và tệp biên dịch trung gian. Hai bản LaTeX cho phép giữ ba PDF chính trong `build/{content,content-twoside,smoke}/` theo `.gitignore` riêng.

Output v3 có ngoại lệ cụ thể cho metadata/báo cáo nhỏ của campaign local và nguồn weights; xem [quy tắc lưu output](topics/degron-footprint/research/kaggle-roadmap-2026-10-31/local-runner.md). Output Kaggle, tensor, feature và OOF nặng không đi cùng clone Git; cần bản sao riêng để resume/tính lại metric.
