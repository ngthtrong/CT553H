# Rà soát hồ sơ nghiệm thu G2 — 07/11/2026

**[DIỄN GIẢI TỪ KẾT QUẢ ĐÃ LƯU] G2 đã có bằng chứng cải thiện định lượng trong
benchmark development và hồ sơ đủ để rà soát nghiệm thu theo phạm vi đóng góp
hiện hành; chưa ghi nhận quyết định đóng G2 trong các hồ sơ đã đối chiếu.**

Lượt này cập nhật cách mô tả trạng thái, không phải biên bản nghiệm thu của
Trọng/GVHD. Không chạy train, suy luận, bootstrap hoặc audit artifact lớn.
[evidence.json](evidence.json) giữ số trích trực tiếp, JSON path và SHA-256 nguồn.
Các audit ngày 06/11 là bằng chứng đã lưu, không phải kiểm lại hôm nay.

## 1. Phạm vi đóng góp hiện hành

[Protocol thực thi v3](../kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md), mục
“Các model được huấn luyện mới”, ghi rõ: **“Không cần kiến trúc mới để đóng góp
benchmark/phương pháp/đánh giá/phần mềm.”** Chưa chứng minh kiến trúc gate/PAP
cũ không phải lý do duy nhất phủ nhận bằng chứng v3. Đồng thời, thay đổi phạm
vi nghiên cứu không tự tạo quyết định nghiệm thu.

Bằng chứng hiện có thuộc dự đoán ΔPSI của mutation đơn trong peptide-reporter,
đánh giá theo nhóm protein, so biểu diễn/head/phạm vi train, adaptation,
calibration và giới hạn chuyển miền. Không nhận đây là bằng chứng E3 cụ thể,
half-life, lâm sàng hoặc hiệu quả kinh tế của CT553H.

## 2. Bằng chứng định lượng hiện có

Nguồn chính: [local-output-analysis.json](../kaggle-roadmap-2026-10-31/local-output-analysis.json),
trường `local_recipes`, `contrasts`, `integrity`, `transfer`, `scientific_status`;
cách đọc ở [báo cáo phân tích](../kaggle-roadmap-2026-10-31/local-output-analysis.md).

| Nội dung | Kết quả đã lưu |
| --- | --- |
| Độ đầy đủ | 633 job complete; 41 recipe local đủ seed 17/29/43, 5 outer fold. Mỗi seed có 122.412 ô, 235 peptide, 221 nhóm protein. |
| Matched LoRA–frozen | Cùng runtime local, arm, split, MLP head và khởi tạo head. Chênh Kaggle CNN–local LoRA không cô lập riêng tác động LoRA. |
| LoRA-B | MAE 0,363669 so frozen-B 0,403385; AUROC+ 0,855047 so 0,826268. |
| LoRA-D | MAE 0,364996 so frozen-D 0,390382; AUROC+ 0,853556 so 0,824625. |
| Qua seed | Cả ba seed giảm MAE và tăng AUROC+ ở mỗi arm B/D. Chúng chung outer folds, không phải ba bộ dữ liệu độc lập. |
| Audit có sẵn | [Audit 06/11](../progress-review-2026-11-06/local-audit.md) đối chiếu OOF/nhãn/fold, metric và artifact; không chứng minh loại hết remote homology. |

MAE macro theo 235 peptide; AUROC+ macro dùng 184 peptide đủ điều kiện, event
ΔPSI≥1. Ensemble lấy trung bình prediction ba seed trước khi tính metric.

| Phép so LoRA − frozen | Δ | CI hiệu chỉnh 98,75% |
| --- | ---: | --- |
| B / MAE | −0,039716 | [−0,048959; −0,030630] |
| B / AUROC+ | +0,028779 | [+0,018798; +0,038893] |
| D / MAE | −0,025386 | [−0,033903; −0,017477] |
| D / AUROC+ | +0,028931 | [+0,019177; +0,038686] |

Paired bootstrap 5.000 lần theo nhóm protein; Bonferroni **hậu kiểm** cho bốn
phép so. CI hỗ trợ cải thiện development, không biến chúng thành kiểm định
tiền đăng ký hoặc xác nhận ngoài nguồn. Không chọn B chỉ vì đứng đầu bảng:
LoRA D−B có ΔMAE +0,001328, CI95 [−0,002947; +0,005537], chưa phân giải toàn W.

## 3. Những tiêu chí không được trộn

| Hồ sơ/tiêu chí | Cách áp dụng đúng |
| --- | --- |
| [G2 saturation 18/10](../g2-saturation-2026-10-18/README.md) | Ridge đã vượt mốc ΔPAP 0,7693 trên H-sat. Phán quyết gate/novelty tại mốc đó giữ nguyên, không dùng nguyên trạng làm phán quyết LoRA/v3. |
| [E2 lịch sử](../g2-extension-2026-10-18/PREREGISTRATION.md) | Tiêu chí ổn định kiến trúc áp cho các ứng viên E2 đã định, không tự thành yêu cầu kiến trúc mới của mọi đóng góp. |
| [R1 Degformer loại overlap](../r1-degformer-clean-2026-10-22/README.md) | Đã chạy 3 seed × 5 fold. AUROC 0,8068 so Ridge ext4 0,8208; CI chênh còn phủ 0. Không liệt kê là việc chưa chạy hoặc kết luận hai model tương đương. |
| V3: giảm MAE 0,02 PSI, guardrail AUROC miền≤3 là 0,01 | [Protocol thực thi](../kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md), mục “Đánh giá và cổng”, đặt trong họ D−B/E−B của training arm. Không tự dùng làm threshold nghiệm thu chung cho LoRA. |
| Phán quyết Q1 đã lưu | [Phân tích Kaggle](../kaggle-roadmap-2026-10-31/output-analysis.md) hỗ trợ giảm MAE; CI điều chỉnh D−B/E−B chưa nằm hoàn toàn dưới −0,02. Guardrail E còn chạm vùng giảm quá 0,01. Thành công LoRA không thay phán quyết Q1. |
| Nguồn ngoài/cấu trúc | Chờ reviewed input; giới hạn claim mở rộng. Không tự coi mọi nhánh pending là điều kiện bắt buộc để ghi nhận đóng góp development. |

Không đặt threshold G2 mới, không đổi threshold sau khi xem kết quả và không
sửa protocol/manifest để khớp phán quyết mong muốn.

## 4. Điều đã có và điều còn chờ

| Thành phần | Trạng thái |
| --- | --- |
| Cải thiện định lượng development có đối chứng | **Đã có**, đặc biệt matched LoRA–frozen B/D và CI theo nhóm. |
| Hồ sơ tái lập/kiểm toán | **Đã có** code/protocol, split, per-seed/OOF và audit; artifact nặng cần bản sao ngoài Git. |
| Quyết định đóng G2 theo phạm vi hiện hành | **Chưa được ghi nhận trong hồ sơ đối chiếu**. R1 README xác định việc ghi trạng thái là quyết định của Trọng/GVHD; không suy ra đã có đồng ý. |
| Tổng quát hóa LoRA ngoài nguồn | **Chưa có**; LoRA chưa chấm trên T. T cùng nguồn/phòng thí nghiệm và chỉ có W5-D. |
| MAE W5-D trên T tốt hơn zero | **Chưa xác nhận**: ΔMAE −0,003256, CI95 [−0,009249; +0,002760]. |
| Lợi ích wet lab/tiết kiệm nguồn lực CT553H | **Chưa kiểm chứng trực tiếp**; [tra cứu bằng chứng](../wet-lab-evidence-plan-2026-11-07/findings.md) đã tìm tiền lệ ngoài và số liệu nguồn lực lân cận, chưa xác nhận utility/tiết kiệm của CT553H. |
| Model mới phục vụ và G3 | **Chưa hoàn tất**; thuộc refit/export/tích hợp và acceptance phần mềm, không tự gộp với ghi nhận kết quả G2. |

Không thấy protocol thực thi quy mọi mục nguồn ngoài, wet lab hoặc export thành
điều kiện bắt buộc chung để ghi nhận đóng góp development. Nếu yêu cầu nghiệm
thu đã được tác giả/GVHD chốt rộng hơn, phải dẫn chính yêu cầu đó và đối chiếu;
không suy ra từ mong muốn ứng dụng.

Trình tự tiếp: (1) đối chiếu và xác nhận phạm vi/tiêu chí G2 đang dùng; (2) đọc
bằng chứng, giới hạn và kết quả âm tương ứng; (3) ghi quyết định của Trọng/GVHD,
ngày, phạm vi chấp nhận và điều kiện còn treo nếu có. Đây không phải yêu cầu tự
động train thêm hoặc làm wet lab. Thay model sản phẩm theo quy trình serving riêng.

## 5. Phạm vi cập nhật và provenance

Các chỉ mục hiện hành dẫn tới hồ sơ này. Hồ sơ thí nghiệm cũ, luận văn, đề cương,
slide, nhãn, checkpoint và JSON kết quả gốc giữ nguyên. `scientific_status` gốc
vẫn là `development_not_gate_closure`; bản trích không thay campaign.

**AI disclosure:** Codex hỗ trợ đối chiếu và soạn hồ sơ; một worker native
`gpt-6-astra` kiểm tiêu chí ở chế độ chỉ đọc, không web và không chạy model.
Đây không phải hội đồng nghiệm thu, phản biện mù hoặc xác minh cross-model.
