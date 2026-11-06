# Kiểm chứng cập nhật kết quả campaign — 06/11/2026

## Phạm vi và nguồn

[ĐO] Phân tích toàn bộ cây output, cập nhật luận văn tiếng Anh và Tóm tắt tiếng Việt. Script audit chỉ đọc. Trong quá trình kiểm bản giải nén, đã khôi phục metadata bị toàn byte 0 từ bản nén có bằng chứng đối chiếu. Không huấn luyện lại, đổi serving model, sửa bundle/checkpoint/state, chạy nghiệm thu ứng dụng, sửa đề cương/presentation hoặc `reportTemplate/`.

- [Audit tổng hợp](../research/output-review-2026-11-06/README.md), [script](../research/output-review-2026-11-06/audit.py), [JSON đầy đủ](../research/output-review-2026-11-06/results.json).
- [Phân tích OOF local](../research/kaggle-roadmap-2026-10-31/local-output-analysis.json), [Kaggle](../research/kaggle-roadmap-2026-10-31/output-analysis.json) và [diagnostics](../research/kaggle-roadmap-2026-10-31/output-analysis-details.json).
- Phân tích OOF nền kiểm 4.278 artifact local / 5.774.277.284 byte và 2.986 artifact Kaggle / 3.065.290.891 byte, không mismatch. Audit mới tái kiểm **76 hash nguồn chọn lọc**, giữ nguyên state nguồn kế thừa, kiểm đủ 30 fit LoRA có tensor adapter thay đổi. Hash mã `analyze-local-output.py` khớp hash ghi trong kết quả. Không gọi đây là một thư viện metric độc lập.
- 633 job complete, 1 source_pending, 1 structure_pending; 456 job kế thừa tính một lần. 41 cấu hình local có đủ ba seed; 47 cấu hình Kaggle có hai control frozen chỉ một seed. Tất cả dùng W 235 peptide / 221 nhóm / 122.412 ô; 88 dòng không phải 88 bộ kiểm định độc lập.

`official.zip` là **file nén lưu kết quả**. Có 8.827 member, tên/size khớp cây giải nén; không tính thành campaign hoặc phép đo mới. Kiểm CRC 8.431 member ≤1 MiB phát hiện 120 JSON trong bản giải nén bị toàn byte 0. Đã giữ bản lỗi tại thư mục portable ngoài repo rồi khôi phục 80 file theo SHA-256 artifact trong state và 40 worker-result theo nội dung JSON khớp hoàn toàn job state. Sau khôi phục, tái kiểm mới toàn bộ 4.278 artifact local + 2.986 Kaggle đạt PASS. [Nhật ký khôi phục](../research/output-review-2026-11-06/metadata-recovery.json), [tái kiểm](../research/output-review-2026-11-06/integrity-recheck.json). Không kiểm CRC mọi payload lớn trong ZIP và không suy đoán nguyên nhân hỏng bản giải nén.

## Nội dung đã cập nhật

| Phần | Nội dung |
|---|---|
| Abstract / Tóm tắt / mở đầu / kết luận | Campaign hoàn tất, LoRA, hiệu chuẩn và giới hạn transfer; bỏ mô tả tokenizer/LoRA còn bị chặn |
| Chương 3 | Identity/kế thừa/checkpoint, nested group split, 9 pLM, 540 ridge + 60 tuning fit, precision và sửa tokenizer, calibration CV/T |
| Chương 4 | Integrity, family grid, đối chứng frozen–LoRA, CI hậu kiểm điều chỉnh, từng seed/ensemble, phân tầng PSI, calibration/T, các control âm và learning curve |
| Phụ lục A | Quy trình nghiên cứu local, pause/resume, ý nghĩa session executed=0 và 2 job chờ đầu vào; tách khỏi API/worker ứng dụng |
| Phụ lục B | Toàn bộ 88 cấu hình, seed, epoch, nested choices, duration và kiểm kê vật lý |
| Chú giải | pLM, LoRA, OOF, MAE/MSE, AP, ECE |

Đã kiểm mã feature để làm rõ: `pair-w5` là hai block one-hot WT/replacement, không phải tương tác và không có vị trí W5. Ridge bổ sung scanning và CNN pre-training là hai can thiệp riêng. Số liệu lịch sử được giữ, không trộn population hay runtime thành các lần lặp độc lập.

## Kết luận số liệu được giữ đúng phạm vi

- LoRA-B MAE **0,363669**, AUROC+ **0,855047**; LoRA-D **0,364996 / 0,853556**. Giảm MAE 9,8% / 6,5% so với frozen cùng arm/runtime. CI protein-group 98,75% cho bốn contrast hậu kiểm đều giữ chiều có lợi; không gọi là xác nhận đăng ký trước độc lập.
- D−B LoRA MAE +0,001328, CI95 [−0,002947; 0,005537]. Có đánh đổi theo WT PSI; không chọn B chỉ vì hạng trung bình.
- LoRA giảm Brier nhưng tăng ECE+ so với frozen. Calibrator CV và card `model_ids: []` chưa phải final serving artifact.
- T chỉ có W5-D: 1.410 peptide, 730 nhóm, 39.234 ô R/A/S, rep1. MAE 0,399147 so với zero 0,402403; ΔMAE −0,003256, CI95 [−0,009249; 0,002760]. AUROC+ 0,840546 không chứng minh lợi thế hồi quy hay hiệu chuẩn. Chưa có LoRA trên T; nguồn cùng phòng thí nghiệm từng được thăm dò, không phải kiểm định ngoài độc lập.
- Thời gian job là duration của attempt hoàn tất; không gán thành tổng thời gian GPU hoặc thời gian chờ của campaign bị ngắt/resume.

## Tài sản và kiểm PDF

[Generator](assets/ch4/build_campaign_assets.py) đọc JSON audit, sinh **12 bảng, macro số, 3 đồ thị khoa học PDF/PNG và 2 sơ đồ draw.io**. Bình luận nguồn và hash ở file sinh, không in đường dẫn nội bộ làm bằng chứng trong PDF. Các đường dẫn trong phụ lục A chỉ phục vụ lệnh thao tác.

- [Sơ đồ campaign](assets/diagrams/campaign-2026-11-06/campaign-lineage.pdf), [nested evaluation](assets/diagrams/campaign-2026-11-06/nested-evaluation.pdf); có `.drawio` chỉnh sửa được và PDF vector nhúng nguồn. Native export draw.io Desktop 32.6.10, kiểm cấu trúc mỗi sơ đồ: 0 error / 0 warning / score 0.
- [PDF một mặt](build/content/content.pdf) và [hai mặt](build/content-twoside/content.pdf): **103 trang/bản**, A4, Times New Roman nhúng; 10 tên font được kiểm nhúng trên mỗi bản. Hai tóm tắt đều một trang; không lỗi overfull, ký tự thiếu, nhãn trùng hay tham chiếu chưa giải quyết.
- Dựng bằng `scripts/build.py` qua đủ lượt XeLaTeX + BibTeX/IEEE; chạy `scripts/check_template.py` đạt PASS. Formatting smoke dựng lại 9 trang, đạt kiểm hình thức; không phải kiểm phần mềm nghiên cứu/ứng dụng.
- [Script kiểm riêng](scripts/validate_campaign_report.py) đối chiếu đủ 88 dòng bảng với JSON, số seed và bốn cột metric; kiểm hash nguồn, nội dung số chính, A4, mọi font nhúng, 6 dấu `[PENDING]` và 5 hình mới. Kết quả máy đọc và hash PDF: [JSON kiểm chứng](current-state-validation-2026-11-06.json).
- Đã xem contact sheet toàn bộ trang, PNG sơ đồ và các trang chi tiết: tóm tắt, lineage/nested, family, bảng/đồ thị LoRA, reliability/transfer và phụ lục. Ảnh QA ở thư mục bị ignore `build/review-2026-11-06/`.

Môi trường Windows ban đầu thiếu XeLaTeX/Poppler/draw.io. Đã chuẩn bị bộ portable ngoài repo tại `%LOCALAPPDATA%/CT553H-report-tools/`: TinyTeX 2026.11 (XeTeX TeX Live 2026), Poppler 26.09.0, draw.io 32.6.10 và PyMuPDF 1.26.7. Không cài đè dependency của `.venv` nghiên cứu.

## Tái tạo

Từ gốc repo, với môi trường phân tích đã có:

```powershell
.venv/Scripts/python.exe topics/degron-footprint/research/output-review-2026-11-06/audit.py
.venv/Scripts/python.exe topics/degron-footprint/report/assets/ch4/build_campaign_assets.py
```

Export hai sơ đồ theo [hướng dẫn](assets/diagrams/campaign-2026-11-06/README.md), rồi dựng qua `scripts/build.py`, không dùng một lượt XeLaTeX đơn lẻ. Với bộ portable của phiên này:

```powershell
$reportTools = Join-Path $env:LOCALAPPDATA 'CT553H-report-tools'
$env:Path = "$reportTools/tex-portable/TinyTeX/bin/windows;$reportTools/poppler/poppler-26.09.0/Library/bin;$env:Path"
$env:PYTHONUTF8 = '1'
Push-Location topics/degron-footprint/report
python scripts/build.py content --bibliography bibtex
python scripts/build.py content --twoside --bibliography bibtex
python scripts/build.py smoke --bibliography bibtex
python scripts/check_template.py
Pop-Location
$env:PYTHONPATH = Join-Path $reportTools 'pdf-renderer'
.venv/Scripts/python.exe topics/degron-footprint/report/scripts/validate_campaign_report.py
```

## Còn lại

Luận văn vẫn có **6 dấu `[PENDING]`**, các placeholder hành chính và các chú thích thư mục tham khảo `TO VERIFY` lịch sử. Hồ sơ này không xác nhận hoàn thiện học thuật toàn văn hoặc nghiệm thu G2/G3. Phần tính toán hiện tại đã xong; nguồn ngoài/cấu trúc hợp lệ, kiểm định mới, final refit/calibration lineage/export và phần mềm mở rộng vẫn là công việc tiếp theo. [Hồ sơ 03/11](current-state-validation-2026-11-03.md) được giữ nguyên.
