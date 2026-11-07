Phân tích bổ sung output Kaggle v3, ngày 02/11/2026.

**[DIỄN GIẢI] Snapshot ủng hộ full-PSI ở Ridge, representation ESM2-35M và CNN trên ESM. Việc chọn arm B hay D cho CNN vẫn cần cân nhắc mục tiêu; mCNN-E chưa chứng minh vượt CNN-D.** Phân tích bổ sung còn cho thấy lợi ích scanning pretrain xuất hiện trên cả 360 kiểu thay thế ngoài 20 kiểu của scanning.

Nguồn tổng quát: [output-analysis.json](output-analysis.json), [phân tích ban đầu](output-analysis.md), [manifest chính thức](output/official/369cb2fe6a1e31e0/pipeline-manifest.json). Các số mới trong tài liệu này được lưu ở [output-analysis-details.json](output-analysis-details.json), sinh bằng [analyze-output-details.py](analyze-output-details.py). Đây là phân tích hậu nghiệm development; CI95 mô tả, 5.000 paired bootstrap theo nhóm protein, seed1729, không điều chỉnh đa kiểm định. Dự đoán lấy trung bình từng ô của seed17/29/43 trước khi tính metric theo peptide. Không đọc nhãn scan_T hoặc checkpoint.

**[ĐO] Đối chiếu toàn bộ phân tích ban đầu.** Chạy lại `analyze-output.py` trên bản output nhập về: 2.986 file, 3.065.290.891 byte khớp SHA-256/kích thước trong manifest; đủ 83 OOF/47 recipe. JSON tính lại có toàn bộ số trùng chính xác với `output-analysis.json`, chỉ khác thời điểm tạo. Manifest có 35 task complete, một task `11-lora-B-s17` running; snapshot cập nhật `2026-11-01T11:18:07Z`, tức 19:18:07 ngày 01/11/2026 ở UTC+8. Trạng thái này không chứng minh tiến trình Kaggle hiện còn chạy. README/PROTOCOL có câu “chưa chạy” là trạng thái tài liệu cũ.

**[ĐO] So trực tiếp hai ứng viên dẫn đầu.** MAE mCNN-E là 0,383846196; CNN-D là 0,384353827. Chênh mCNN-E−CNN-D = −0,000507631, CI95 [−0,003157473; +0,002223427]. AUROC dương chênh −0,001812120, CI95 [−0,006372735; +0,002738648]. Hai CI đều chứa 0. Thứ hạng điểm không đủ để chọn mCNN như một cải tiến đã xác nhận; CI chứa 0 cũng không chứng minh hai model tương đương.

**[ĐO] Không chuyển kết luận full-PSI của Ridge sang mọi head.** CNN-D giảm MAE toàn W 0,003610846 so CNN-B, nhưng CI95 [−0,007738662; +0,000420131] còn chứa 0. Riêng PSI≤3, CNN-D tăng MAE 0,008700411, CI95 [+0,003292820; +0,014106553]. AUROC dương trong miền này giảm 0,006407098, CI95 [−0,013334076; +0,000759729]; cận dưới vượt mức giảm 0,01. Vì vậy guardrail chưa được bảo đảm cho CNN-D so CNN-B. Đây là phép so thêm sau khi thấy output, khác họ Q1 định trước dùng Ridge W5.

| Miền test | Số peptide | MAE CNN-B | MAE CNN-D | MAE mCNN-E |
|---|---:|---:|---:|---:|
| PSI≤3 | 91 | 0,403567 | 0,412267 | 0,413154 |
| 3<PSI≤4 | 85 | 0,403716 | 0,399328 | 0,401730 |
| 4<PSI≤5 | 36 | 0,345256 | 0,332657 | 0,329647 |
| PSI>5 | 23 | 0,334872 | 0,299491 | 0,286631 |

Nguồn bảng strata: `recipes/<recipe>/ensemble/strata` trong [output-analysis.json](output-analysis.json). [DIỄN GIẢI] CNN-D là ứng viên hợp lý cho mục tiêu hồi quy toàn dải; CNN-B vẫn là đối chứng cần giữ nếu ưu tiên miền PSI thấp hoặc event dương. Chưa khóa lựa chọn bằng thứ hạng development.

**[ĐO] CNN-D cải thiện rộng qua fold và peptide so Ridge W5-D.**

| Outer fold | MAE Ridge W5-D | MAE ESM CNN-D |
|---|---:|---:|
| 0 | 0,419272 | 0,399917 |
| 1 | 0,409007 | 0,379794 |
| 2 | 0,425174 | 0,404757 |
| 3 | 0,397517 | 0,367561 |
| 4 | 0,388043 | 0,369740 |

CNN-D có MAE thấp hơn ở 156/235 peptide và 150/221 nhóm (delta mỗi nhóm lấy trung bình các peptide của nhóm). [DIỄN GIẢI] Lợi ích không chỉ đến từ một fold. Không dùng năm fold hay ba seed như các mẫu thống kê độc lập; các tập train có giao nhau.

**[ĐO] Scanning pretrain có lợi cả ngoài các kiểu thay thế đã quan sát trong scanning.** Tách saturation theo cặp amino acid có hướng WT→mutant: 20 kiểu scanning có 6.433 ô, 360 kiểu còn lại có 115.979 ô; mỗi cohort đều phủ 235 peptide/221 nhóm. Metric dưới là peptide-macro MAE, mỗi peptide chỉ lấy ô thuộc cohort đang xét.

| Kiểu thay thế trên saturation | CNN one-hot scratch | CNN pretrain rep1 | ΔMAE pretrain−scratch | CI95 mô tả |
|---|---:|---:|---:|---|
| 20 kiểu scanning | 0,399065 | 0,391342 | −0,007723 | [−0,012104; −0,003399] |
| 360 kiểu còn lại | 0,393296 | 0,386985 | −0,006311 | [−0,009841; −0,002942] |

[DIỄN GIẢI] Lợi ích quan sát được không bị giới hạn ở 20 kiểu thay thế của scanning. Đây vẫn là OOF trên saturation development, chưa phải bằng chứng transfer trên T hay một assay độc lập. Hai cohort khác nhau về số ô/phân bố; không đọc chênh MAE giữa cohort như độ khó nội tại của từng loại. AUROC dương chỉ có 114 peptide đủ điều kiện ở cohort20, so 184 ở cohort360; không so trực tiếp hai macro AUROC như cùng population.

**[ĐO] Learning curve cần tách mean seed khỏi ensemble.**

| Fraction nhóm train của Ridge W5-D | MAE trung bình ba seed | MAE ensemble |
|---|---:|---:|
| 25% | 0,441319 | 0,415403 |
| 50% | 0,418874 | 0,411335 |
| 75% | 0,410696 | 0,408327 |
| 100% | 0,407803 | 0,407803 |

Từng seed dùng subset train khác nhau ở fraction<1; vì vậy hợp dữ liệu của ensemble có thể vượt fraction ghi ở mỗi thành viên. [DIỄN GIẢI] Dùng cột mean seed để đọc độ nhạy với lượng dữ liệu của một lượt fit; không diễn giải ensemble25% là một model chỉ thấy đúng25% tổng dữ liệu. Curve hiện mới có Ridge, không đủ để ngoại suy lợi ích tăng dữ liệu cho CNN/pLM.

**[ĐO] Epoch được chọn thường sớm.** ESM pointwise-D và CNN-D đều chọn epoch1 trong 9/15 lượt seed×fold, median1; CNN-D có epoch tốt nhất tối đa7. mCNN-D median3, tối đa5. [DIỄN GIẢI] Chưa có bằng chứng rằng tăng trần epoch sẽ cải thiện; việc giải thích nguyên nhân cần learning curves train/validation chi tiết. Số tham số head pointwise/CNN lần lượt 36.833/57.185, nên phép so chưa cô lập hoàn toàn ảnh hưởng trộn vị trí khỏi dung lượng head.

**[ĐO] Chi phí hoàn tất là 9,3265 giờ task, trong đó stage11 frozen chiếm 77,52%.** Hai task frozen-B/D mới có seed17, đủ năm fold, MAE 0,407145/0,391931. Chỉ head thay đổi; không có OOF LoRA. Mã stage11 chạy backbone WT/mutant mỗi batch/epoch kể cả frozen, trong khi stage05 dùng feature cache. [DIỄN GIẢI] Chi phí lớn này chưa phải bằng chứng LoRA kém hiệu quả; nhánh LoRA còn thiếu kết quả. Cache cho comparator frozen là hướng tối ưu cần kiểm parity/precision, không thay recipe trong cùng run rồi gộp kết quả.

**[ĐỀ XUẤT] Ưu tiên hoàn tất đánh giá lõi.** Giữ Ridge W5-D làm mốc, CNN-D/CNN-B và mCNN-E làm các ứng viên cần lựa chọn theo mục tiêu đã ghi rõ. Khóa lựa chọn development, triển khai final refit/export riêng cho kiến trúc chọn, hiệu chuẩn đúng model rồi đánh giá T theo protocol. Stage07 hiện tự promotion W5; đổi tên recipe không tạo final CNN hợp lệ. Các stage07–10 và LoRA chưa có kết quả hoàn tất, nên chưa có bằng chứng calibration, external/structure hay hoàn tất G2/G3. Không cần chờ LoRA để hoàn thiện benchmark lõi.
