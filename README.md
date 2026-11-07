# Luận văn tốt nghiệp CT553H

Kho nghiên cứu và báo cáo luận văn của **Nguyễn Thanh Trọng** (B2305615), GVHD **TS. Hồ Quang Thái**, ngành Kỹ thuật phần mềm, Đại học Cần Thơ.

Đề tài **degron-footprint** tập trung dự đoán hiệu ứng đột biến ở từng vị trí amino acid trên nhãn thực nghiệm, kèm công cụ phân tích. Kết quả và giới hạn của từng thí nghiệm nằm trong README và tệp kết quả tương ứng.

## Trạng thái ngày 07/11/2026

| Mảng | Hiện trạng và điểm vào |
| --- | --- |
| Nghiên cứu / G2 | **v3 full-PSI** hoàn tất 633 job local, nguồn ngoài/cấu trúc pending. [Phân tích local](research/kaggle-roadmap-2026-10-31/local-output-analysis.md) có bằng chứng LoRA cải thiện so frozen. [Hồ sơ rà nghiệm thu G2](research/g2-acceptance-2026-11-07/README.md): đã có cải thiện định lượng trong development, đủ hồ sơ để rà nghiệm thu; chưa ghi nhận quyết định đóng G2. [Kaggle](research/kaggle-roadmap-2026-10-31/output-analysis.md) giữ mốc riêng; mô hình sản phẩm chưa đổi. |
| Bằng chứng wet lab / nguồn lực | [Kết quả tra cứu theo ARS](research/wet-lab-evidence-plan-2026-11-07/findings.md): có tiền lệ validation sinh học từ nghiên cứu ngoài; số liệu nguồn lực lân cận gồm đo thực tế, ước lượng và simulation cần tách riêng. Chưa có kiểm chứng trực tiếp CT553H tiết kiệm wet lab. |
| Dữ liệu | Bundle v3 giữ saturation toàn dải PSI và scanning sau QC; nguồn, giấy phép, hash và nhật ký nằm trong [sổ dữ liệu](data/README.md), quy tắc dựng bundle ở [DATASET.md](research/kaggle-roadmap-2026-10-31/DATASET.md). Dữ liệu và artifact nặng nằm local. |
| Ứng dụng | [Baseline FastAPI + React](system/app/README.md) có mã và kiểm thử lịch sử, dùng `m3-ext4.0-platt-v1`. [Phạm vi v0.2](system/README.md) gồm dự án/lịch sử, jobs peptide/protein, import/comparison; các phần mở rộng chưa được nghiệm thu. |
| Giao diện | [Workspace UI v2](system/design/workspace-ui-v2/README.md) là prototype tương tác hiện hành; dữ liệu minh hoạ, lưu trong bộ nhớ tab, chưa nối backend. |
| Luận văn / đề cương | [Luận văn](report/README.md) cập nhật campaign hoàn tất ngày 06/11: phương pháp, 88 cấu hình OOF, LoRA/calibration/T, sơ đồ và phụ lục; [audit tổng hợp](research/output-review-2026-11-06/README.md). [Đề cương](proposal/README.md) giữ bản 03/11. Còn `[PENDING]`; cập nhật tài liệu không phải nghiệm thu G2/G3. |

Trạng thái nghiệm thu được đối chiếu ngày 07/11 từ output/audit đã lưu ngày 06/11; không có lượt huấn luyện hoặc kiểm lại test phần mềm mới. G2 ghi nhận bằng chứng nghiên cứu riêng với nghiệm thu G3 và claim lợi ích wet lab. Các snapshot tiến độ cũ giữ mốc riêng trong chỉ mục nghiên cứu.

## Cấu trúc hiện tại

| Thư mục | Nội dung |
| --- | --- |
| [research/](research/README.md) | Chỉ mục hiện hành, thí nghiệm, audit, script và kết quả nhỏ; v3 và bằng chứng lịch sử được dẫn riêng. |
| [data/](data/README.md) | Nguồn gốc và hướng dẫn dữ liệu; dữ liệu thô/trung gian/đã xử lý không đưa lên Git. |
| [report/](report/README.md) | Bản luận văn đang viết, nằm trực tiếp ở gốc repo. |
| [proposal/](proposal/README.md) | Đề cương và hướng dẫn dựng PDF/DOCX. |
| [system/](system/README.md) | Thiết kế và ứng dụng FastAPI + React. |
| [presentation/](presentation) | Slide và tài liệu trình bày. |
| [resources/](resources/) | [Thông tin người tham gia](resources/people.md), [đề cương học phần](resources/CT553H.pdf), [hướng dẫn dữ liệu](resources/dataset-guide.md), [luận văn tham khảo](resources/reference-theses/). |
| [resources/papers/](resources/papers/) | [Ghi chép phân tích bài báo](resources/papers/analyzed-papers/README.md), [PDF degron](resources/papers/degron/README.md), [hướng nghiên cứu GVHD](resources/papers/advisor-research.md), công bố của [Hồ Quang Thái](resources/papers/ho-quang-thai/ho-quang-thai.md) và [Yu-Yen Ou](resources/papers/yu-yen-ou/yu-yen-ou.md). |
| [reportTemplate/](reportTemplate/README.md) | Template LaTeX gốc sạch, tách khỏi bản luận văn đang viết. |

Ngày 07/11/2026, các thư mục đề tài được chuyển từ `topics/degron-footprint/` ra gốc repo: `research/`, `data/`, `report/`, `proposal/`, `system/` và `presentation/`. Ghi chép trước đây ở `lectures/`, `project/` đã được gom vào `resources/`. Manifest, hash và bản ghi kết quả lịch sử giữ đường dẫn tại thời điểm tạo. Gói ZIP notebook-kit v1/v2 giữ cây `topics/degron-footprint/` bên trong để tương thích với các notebook lịch sử.

## Bắt đầu

Chạy lệnh từ gốc repository. Hướng dẫn nghiên cứu và quy tắc đóng góp nằm trong [CLAUDE.md](CLAUDE.md), được [AGENTS.md](AGENTS.md) dẫn chiếu.

Trên máy Windows hiện tại, `.venv` ở gốc đã được chuẩn bị cho CUDA. Xem [local-runner.md](research/kaggle-roadmap-2026-10-31/local-runner.md) rồi dùng PowerShell:

```powershell
.\run-local.cmd --hours 2   # mở phiên chạy/tiếp tục trong terminal riêng
.\status-local.cmd         # xem trạng thái
.\pause-local.cmd          # yêu cầu dừng an toàn
```

Khi cần dựng môi trường CUDA lại, theo [local-cuda.md](research/kaggle-roadmap-2026-10-31/local-cuda.md) và requirements ghim của v3. `requirements.txt` ở gốc phục vụ script nghiên cứu cũ; dùng môi trường riêng để không ghi đè runtime campaign.

Huấn luyện trên Kaggle v3: [RUN.md](research/kaggle-roadmap-2026-10-31/RUN.md), [notebook tổng](research/kaggle-roadmap-2026-10-31/ALL-IN-ONE.md) và [resume nhiều phiên](research/kaggle-roadmap-2026-10-31/MULTI-SESSION.md). [Notebook-kit 22/10](research/notebook-kit-2026-10-22/RUN.md) dành cho tái lập R0–R6 lịch sử.

Chạy ứng dụng baseline theo [README của app](system/app/README.md). Makefile ứng dụng dùng Bash và đường dẫn môi trường Linux/WSL; frontend có thể cài/chạy bằng npm theo README riêng. Prototype Workspace UI v2 mở trực tiếp bằng trình duyệt theo hướng dẫn của nó.

Biên dịch luận văn cần GNU Make, XeLaTeX, Biber/BibTeX, Poppler và Times New Roman:

```bash
make -C report doctor
make -C report content
make -C report check
```

PDF nằm tại `report/build/content/content.pdf`. Template sạch dùng cùng lệnh với `-C reportTemplate`.

## Tệp đưa lên Git

Giữ mã nguồn, tài liệu, kết quả nhỏ và tài sản hình/sơ đồ. Bỏ qua dữ liệu nghiên cứu (ngoại trừ sổ nguồn gốc `README.md` và `SOURCE.md`), checkpoint, môi trường ảo, cache, CSDL ứng dụng, bí mật và tệp biên dịch trung gian. Hai bản LaTeX cho phép giữ ba PDF chính trong `build/{content,content-twoside,smoke}/` theo `.gitignore` riêng.

Output v3 có ngoại lệ cụ thể cho metadata/báo cáo nhỏ của campaign local và nguồn weights; xem [quy tắc lưu output](research/kaggle-roadmap-2026-10-31/local-runner.md). Output Kaggle, tensor, feature và OOF nặng không đi cùng clone Git; cần bản sao riêng để resume/tính lại metric.
