# Kiểm chứng bản báo cáo tiến độ — 06/11/2026

Hồ sơ này thuộc lượt rà soát tiến độ sau `current-state-validation-2026-11-06.*`. Bản ghi trước giữ nguyên phạm vi/hash lịch sử; hai PDF tại đường dẫn làm việc được dựng lại từ nguồn hiện tại.

## Phạm vi

Cập nhật báo cáo hiện có, giữ tên đề tài/ngôn ngữ/template, chưa hoàn tất luận văn và chưa nghiệm thu nghiên cứu hay phần mềm. Không huấn luyện lại, resume, tải lại/biến đổi dataset, sửa state/checkpoint/manifest, đổi serving model, commit hoặc push. Sửa chỉ mục/rules ở mức dẫn hồ sơ mới và sửa thông tin branch đã cũ.

- [Dossier](../research/progress-review-2026-11-06/README.md), [thay đổi](../research/progress-review-2026-11-06/report-changes.md), [missing evidence](../research/progress-review-2026-11-06/missing-evidence.md).
- [Local audit mới](../research/progress-review-2026-11-06/local-audit.md), [JSON](../research/progress-review-2026-11-06/local-audit.json), [mã/registry/protocol](../research/progress-review-2026-11-06/source-inventory.code.json).
- [Nguồn học thuật](../research/progress-review-2026-11-06/literature-audit.md).

## Kiểm chứng khoa học và truy vết

Audit riêng đọc dữ liệu/OOF trong checkout Linux, không quan sát tiến trình Windows live. Đã kiểm 32 file dữ liệu của manifest, 4.278 artifact local và 2.986 Kaggle, không thiếu/hash sai trong tập kiểm. Tái tính 41 recipe local MAE/per-seed, bốn core metrics, Brier ba lớp và locked W5-D/T từ dự đoán lưu; metric so với số đã lưu khớp trong tolerance 1e-10. Kiểm 15 inner-role sets, 15 lựa chọn nested và 60 fit metadata. Fit metadata là bằng chứng khai báo adapter thay đổi; không reload model tensor trong audit mới.

Trong 76 nguồn phân tích được ghim: 75 match byte và một JSON được đối chiếu đúng phép LF→CRLF tái tạo chính xác hash/size Windows. Aggregate code, protocol và registry cũng tái tạo đúng hash pin theo newline từng file. Không sửa expected hash hoặc nguồn để ép PASS. Kiểm này xác nhận danh tính snapshot, không chứng minh loại hết homology/motif leakage.

Các diagnostic mới là mô tả hậu kiểm: 235 peptide, 221 group, 122.412 cell của W. Có counts tốt/xấu, leave-one-group-out mean contrast, fold/strata/substitution/effect class và failure cases. Không tạo CI/p-value mới cho subgroup. Các CI trong báo cáo kế thừa đúng paired bootstrap và family adjustment của thí nghiệm tương ứng.

## Dựng và kiểm báo cáo

Môi trường Linux hiện có đủ GNU Make, XeLaTeX, Biber/BibTeX, Poppler và bốn mặt Times New Roman đọc từ thư mục Windows. Không cài đè môi trường CUDA. Hai bản được dựng qua Make/`scripts/build.py` với **biblatex/IEEE + Biber**, đủ lượt ổn định tham chiếu. Tên đề tài chính thức giữ trong metadata/PDF.

Kết quả kiểm máy và hash PDF hiện tại được lưu tại [progress-validation-2026-11-06.json](progress-validation-2026-11-06.json); script: [validate_progress_report.py](scripts/validate_progress_report.py). Ảnh QA lưu ở `build/review-progress-2026-11-06/` bị Git ignore.

- `make doctor`, `make all`, `make check` đạt. Hai PDF **121 trang/bản**, A4, mọi font nhúng, không còn overfull, missing character, duplicate label hoặc tham chiếu chưa giải quyết. `make check` cũng kiểm bản smoke 9 trang đã có; không xem đó là chạy lại benchmark hay nghiệm thu phần mềm.
- Script mới đối chiếu **88 dòng** bảng campaign với JSON gốc, metric/seed của từng dòng; binding hash và số của bảng sai số mới; **22 khóa bibliography** duy nhất và citation hợp lệ; **100 liên kết local** của hồ sơ review không hỏng. Kiểm các đích liên kết GoTo trong PDF hợp lệ.
- Hai tóm tắt giữ một trang mỗi bản (PDF 7 và 8); trạng thái tiến độ ở trang 9. Còn **5 marker `[PENDING]`** trong mỗi PDF, kèm placeholder hành chính được giữ có chủ ý.
- Đã xem contact sheets **toàn bộ 121 trang bản một mặt**. Xem chi tiết ở cả hai bản: mở đầu/RQ (24–27), lý thuyết và hai sơ đồ khái niệm (40–43), uncertainty (48), hình/bảng sai số (90–92), bảng đánh giá RQ (96–97); thêm tóm tắt, trạng thái, history và mục lục/danh mục hình. Không thấy nội dung mất, chữ đè/cắt, sai thang hình hay trang trắng bất thường. Bảng RQ tiếp trang lặp header đúng.
- Hình scatter dùng cùng thang, đường equality và đủ 235 điểm/arm; bảng error ghi đúng số cell/peptide/group, không hiển thị subgroup CI giả. Các bảng failure giữ cả sign reversal và case LoRA kém frozen. Đã sửa label sơ đồ/header bảng gây overfull và ngăn ngắt từ “saturation” qua float lịch sử.
- `git diff --check` đạt; không có thay đổi dataset/output/checkpoint hoặc tài liệu ngoài phạm vi nêu trên.

## Giới hạn

- Build/PDF đúng hình thức không thay bằng chứng khoa học, validation nguồn độc lập hay nghiệm thu ứng dụng.
- Source authority/DOI được rà có mục tiêu, không phải systematic review hoặc chứng minh tính mới tuyệt đối. GEO live có reCAPTCHA, Larsen v1 có403; audit phân biệt metadata với toàn văn.
- Administrative placeholders và các mục chưa thực hiện được giữ, không tự tạo thông tin để hoàn chỉnh hình thức.
- Chưa kiểm CRC toàn payload lớn trong ZIP; audit working artifacts riêng không đồng nghĩa chứng nhận toàn bộ archive.
