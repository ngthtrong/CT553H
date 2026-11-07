# Thay đổi báo cáo và lý do — 06/11/2026

## Phạm vi

Cập nhật `topics/degron-footprint/report/` từ bản đang có tại commit `64c3c33`; không tạo báo cáo nghiên cứu tách rời thay thế. Giữ tiếng Anh, Tóm tắt tiếng Việt, tên đề tài chính thức và template Khoa. Không điền thông tin bảo vệ/hội đồng, không sửa đề cương, slide, template gốc, dataset, campaign state/checkpoint hoặc serving bundle. Không train, resume, commit hay push.

## Nội dung giữ, sửa, bổ sung và loại bỏ

| Phần | Xử lý | Nội dung và lý do |
|---|---|---|
| Front matter | Bổ sung | Trang **Research Progress Status**, mốc 06/11/2026, trạng thái bằng chứng và cách đọc các population. Làm rõ tài liệu chưa phải báo cáo cuối/nghiệm thu. |
| Abstract / Tóm tắt | Sửa | Định danh là báo cáo tiến độ, giữ số đã đo và giới hạn development/transfer. Không biến 633 job thành nghiệm thu khoa học. |
| Mở đầu | Viết lại | Protein → proteostasis → degradation/degron → mutation → assay/giới hạn → mô hình → câu hỏi cụ thể ΔPSI. Lập luận cấp thiết có nguồn, không bắt đầu từ kiến trúc. |
| Related work / gap | Sửa, loại khẳng định quá rộng | PAP đã dùng ΔPAP và khảo sát biến thể, nên bỏ cách nói các công trình trước chỉ dừng ở motif/peptide. Gap được giới hạn vào endpoint, training range, representation/head và grouped evaluation có đối chứng. Không claim “đầu tiên” hay novelty từ ESM+CNN. |
| Mục tiêu / câu hỏi / đóng góp | Sửa | Năm RQ gắn trực tiếp với thiết kế đã chạy và câu hỏi còn mở. Tách đóng góp workflow/dữ liệu/đánh giá có bằng chứng khỏi kiến trúc mới, triển khai đầy đủ và hiệu quả wet-lab chưa xác lập. |
| Cơ sở lý thuyết | Mở rộng | Amino acid/peptide/protein, proteostasis/turnover/half-life/thermodynamic stability, E1/E2/E3/proteasome, ngữ cảnh degron, WT/mutant, GPS/PSI/ΔPSI, scanning/saturation, QC và đơn vị quan sát. Thêm lý thuyết ML đúng recipe: Ridge/one-hot, pLM, CNN/mCNN, frozen/LoRA, transfer, splitting/leakage, loss/metric/CI/calibration. |
| Sơ đồ lý thuyết | Bổ sung | Hai sơ đồ TikZ tự vẽ: tuyến UPS điển hình và đường prediction so với measurement. Chú thích là khái niệm, không phải thí nghiệm hay cơ chế CT553H đã xác nhận. |
| Chương 1 | Sửa | Giữ 532 substitution/peptide; chuyển lợi ích phần mềm thành mục tiêu dự kiến, bỏ khẳng định ngân sách/cost chưa đo. Giữ phần yêu cầu đã chốt với trạng thái planned. |
| Chương 3 | Bổ sung | Lịch sử quyết định và data evolution: vì sao đổi hướng từ peptide score/scan transfer sang saturation, mở WT PSI, thử representation/head và matched adaptation. Nhắc hạn chế hồi cứu, không viết lại lịch sử như toàn bộ được preregistered. |
| Feature / adaptation description | Làm rõ | “pLM-only” còn 60 feature WT/mutant/composition; PSI không là feature effect model. Matched LoRA dùng pooled/pointwise MLP, không CNN/mCNN; full fine-tuning có code option nhưng không có arm đã đánh giá trong campaign. |
| Chương 4, lịch sử | Sửa diễn giải | Không coi replicate agreement là trần toán học. Đổi giải thích variance/label shortage thành suy luận có giới hạn. Chọn threshold4 chỉ thuộc study lịch sử; full-PSI là population khác. Làm rõ multiplicity riêng G2/R6/full-PSI/local. |
| R6 transfer control | Bổ sung kết quả bị bỏ sót | JSON còn ghi nhận one-hot mCNN scanning fine-tuning +0,014661 AUROC, CIadj [0,002720;0,027593]. Giữ primary ESM-mCNN chưa đạt; không sửa lịch sử JSON/README cũ để tạo thành công. |
| Kiểm chứng local | Mở rộng bằng chứng | Tái tính 41 recipe MAE, bốn core metric/calibration, W5-D/T; kiểm 32 file dữ liệu, 4.278 artifact local, 2.986 Kaggle, split roles và lựa chọn nested. Phân biệt 75 hash nguồn exact và một trường hợp newline được giải thích chính xác. Không claim đã quan sát Windows live hay load tensor. |
| Phân tích sai số | Bổ sung | Hình scatter hai arm giữ đủ235 peptide, bảng effect-class/large effects và ba cell sai nhất; fold/group/strata/substitution diagnostics trong JSON. Giữ case kém hơn frozen và nhắc subgroup chưa có kiểm định mới. |
| RQ và nghiên cứu tiếp | Bổ sung | Bảng nối năm RQ với bằng chứng/giới hạn. Ưu tiên validation mới, nguồn/overlap/endpoint, residual/calibration và model-specific serving artifacts, thay vì tiếp tục tối ưu leaderboard bằng T đã xem. |
| Kết luận | Sửa mức khẳng định | “Provisional Findings at the Progress Cutoff” và ưu tiên giai đoạn tiếp; chưa chọn mô hình tối ưu hay kết luận final. |
| Bibliography | Sửa và bổ sung | 22 mục có DOI/URL và audit mức kiểm. Sửa Zhiqian Zhang, Fia B. Larsen, Mengqiu Zheng; thay mục TO VERIFY bằng nguồn xác minh được; giữ Larsen preprint và Degformer software. Không giả định mở full text thành công khi 403/reCAPTCHA. |
| Chỉ mục/rules | Đồng bộ tối thiểu | README report/research dẫn dossier mới. CLAUDE sửa thông tin local/remote branch đã cũ và chỉ điểm validation mới; không thay protocol hoặc quyết định mô hình. |

## Kết luận thay đổi và kết luận giữ lại

- **Giữ:** LoRA cải thiện so matched frozen trên W, nhưng B/D đánh đổi theo PSI; không chọn B bằng hạng MAE. T chỉ kiểm W5-D, chưa LoRA. Lợi thế MAE T so zero chưa xác lập. Development chưa phải external validity.
- **Làm rõ:** Lợi ích LoRA xuất hiện ở nhiều peptide/group nhưng không đồng đều. LoRA-B tốt hơn ở184/235 peptide, D164/235; vẫn có51 và71 peptide kém hơn. Bỏ một group bất kỳ không đảo dấu mean contrast là robustness mô tả, không thay external validation.
- **Bổ sung giới hạn:** Sai số lớn trên |ΔPSI|≥1 và các sign reversal cho thấy MAE trung bình chưa đủ diễn giải mutation có tác động mạnh. Số support trong subgroup khác điều kiện eligibility AUROC.
- **Điều chỉnh lịch sử:** Có control scanning→one-hot mCNN dương; không khẳng định transfer luôn thất bại, cũng không dùng nó để tuyên bố primary architecture đã được xác nhận.
- **Loại bỏ mức khẳng định vượt bằng chứng:** Không chứng minh kiến trúc mới, thiếu nhãn là nguyên nhân duy nhất, không còn leakage, tiết kiệm wet-lab, protein tự nhiên hoặc lâm sàng.

## Hồ sơ kiểm chứng

- [Local audit](local-audit.md): phương pháp, source/data hash, bảng số, residual và giới hạn.
- [Literature audit](literature-audit.md): nguồn hỗ trợ từng lập luận, DOI/URL, mức truy cập và missingness.
- [Lịch sử](experiment-history.md), [data/method](data-method-audit.md), [result comparison](result-comparison.md): không gộp protocol để xếp hạng.
- [Missing evidence](missing-evidence.md): trạng thái, ảnh hưởng, nguồn đã kiểm, cách bổ sung và ưu tiên.
- [Validation mới](../../report/progress-validation-2026-11-06.md): build/PDF, bảng88 dòng, source binding, link/annotation, các kiểm tra đã làm và giới hạn.

Hồ sơ output-review/current-state-validation ngày06/11 trước lượt này giữ nguyên làm bằng chứng lịch sử. PDF ở đường dẫn làm việc được dựng lại, vì vậy đọc hash mới từ `progress-validation-2026-11-06.json` thay vì gán hash PDF cũ cho bản mới.
