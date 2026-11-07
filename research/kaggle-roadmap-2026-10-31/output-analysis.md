# Phân tích output Kaggle v3 — 02/11/2026

**[DIỄN GIẢI] Kết quả development ủng hộ mở tập train ra toàn dải PSI và dùng frozen ESM2 kết hợp CNN. Chưa đủ bằng chứng kết luận LoRA, chuyển nguồn trên T hoặc hoàn tất G2/G3.** mCNN-E có MAE thấp nhất trong snapshot; CNN-D là ứng viên hợp lý để khóa và đánh giá tiếp vì MAE gần tương đương và khả năng xếp hạng hiệu ứng dương tốt hơn.

Nguồn chính là [pipeline-manifest.json](output/official/369cb2fe6a1e31e0/pipeline-manifest.json), không phải trạng thái cũ “chưa chạy” trong README. Snapshot được cập nhật lần cuối `2026-11-01T11:18:07Z`. Các phép tính dẫn xuất, đường dẫn OOF, seed và CI nằm trong [output-analysis.json](output-analysis.json); [analyze-output.py](analyze-output.py) tái tạo số liệu từ output mà không load checkpoint. Chạy script với `python -I` trong môi trường đã có numpy/pandas/pyarrow/scipy/scikit-learn.

**[ĐO] Tính toàn vẹn và phạm vi dữ liệu.** Đã kiểm SHA-256 và kích thước của **2.986 file / 3.065.290.891 byte** thuộc các task hoàn tất: không sai lệch. Đã đọc **83 file OOF, gộp thành 47 recipe**; không trùng cặp `(seed, cell_id)`, dự đoán hữu hạn, mode đều là official và data identity thống nhất. Tất cả recipe/seed có cùng **122.412 ô, 235 peptide, 221 nhóm protein**, cùng nhãn và fold metadata. Một nhóm protein chỉ thuộc một outer fold. Đây là kiểm tra artifact và OOF; không phải một audit homology mới hay chứng minh độc lập sinh học.

Stage00 tái lập số lịch sử thành công: AUROC base **0,808185904**, ext4 **0,820822359** ([legacy-reproduction.json](output/official/369cb2fe6a1e31e0/tasks/00-78cc356ba4f4/legacy-reproduction.json)). Không so trực tiếp chênh lệch với bảng W mới vì population/eligibility/split đã khác.

**Cách đọc các bảng.** MAE là trung bình sai số tuyệt đối theo peptide, đơn vị PSI; thấp hơn tốt hơn. AUROC/AP dương dùng `ΔPSI≥1`, âm dùng `ΔPSI≤−1`; cao hơn tốt hơn. MAE có 235 peptide, metric dương có 184 peptide đủ điều kiện, metric âm có 110. B là train PSI≤4; D là train toàn dải; E là toàn dải cân bằng stratum rồi peptide. W5 là baseline Ridge có ngữ cảnh có thứ tự ±5 residue. Test W luôn giữ nguyên giữa các arm. Inner validation dùng toàn dải ngay cả với B.

Trừ hai model stage11 frozen chỉ có seed17, bảng dưới dùng **dự đoán ensemble của seed17/29/43**: lấy trung bình dự đoán từng ô rồi mới tính metric. Các task stage05 được tách theo seed nên không thể dùng trung bình các `stage-summary.csv` thay cho ensemble.

| Recipe | MAE ↓ | AUROC dương ↑ | AP dương ↑ | AUROC âm ↑ |
|---|---:|---:|---:|---:|
| Dự đoán hằng 0, đối chứng mô tả | 0,436916 | 0,500000 | 0,124697 | 0,500000 |
| Ridge W5-B | 0,433577 | 0,831179 | 0,463183 | 0,674538 |
| Ridge W5-D | 0,407803 | 0,831933 | 0,461413 | 0,693120 |
| Ridge W5-E | 0,403613 | 0,827521 | 0,449854 | 0,710871 |
| Ridge ESM-only-D | 0,400760 | 0,813072 | 0,433978 | 0,786762 |
| Ridge W5+ESM-D | 0,402252 | 0,844480 | 0,495354 | 0,730115 |
| Nested selection stage04 | 0,397525 | 0,836694 | 0,478757 | 0,757802 |
| One-hot CNN-D | 0,393611 | 0,829131 | 0,459661 | 0,709770 |
| ESM pointwise-D | 0,389693 | 0,837527 | 0,473879 | 0,751469 |
| **ESM CNN-D** | **0,384354** | **0,848816** | **0,509470** | **0,755034** |
| ESM mCNN-D | 0,384992 | 0,846323 | 0,504215 | 0,756996 |
| **ESM mCNN-E** | **0,383846** | **0,847004** | **0,506416** | **0,759130** |
| ESM CNN-B | 0,387965 | 0,850629 | 0,509656 | 0,748445 |
| CNN scanning-pretrain rep1-D, one-hot | 0,387226 | 0,842494 | 0,502367 | 0,713237 |

**[ĐO] Mở toàn dải PSI cải thiện hồi quy, chủ yếu ở miền PSI cao.** Với cùng W5, MAE A/B/C/D lần lượt **0,471133 / 0,433577 / 0,417743 / 0,407803**. D giảm **0,025774 PSI (5,94%)** so B; E giảm **0,029963 PSI (6,91%)**. Bootstrap 5.000 lần theo 221 nhóm protein cho hai phép so chính:

| Phép so | ΔMAE | CI 97,5%, Bonferroni hai phép so |
|---|---:|---|
| D−B | −0,025774 | [−0,033806; −0,018286] |
| E−B | −0,029963 | [−0,041656; −0,018817] |

Các CI tính lại khớp [comparisons.json](output/official/369cb2fe6a1e31e0/tasks/01-78cc356ba4f4/comparisons.json). Cả hai hỗ trợ cải thiện MAE. Tuy vậy, cận gần 0 vẫn lớn hơn −0,02, nên chưa chứng minh mức cải thiện tối thiểu 0,02 PSI ở toàn bộ CI đã điều chỉnh.

| PSI(WT) của test | Số peptide | MAE B | MAE D | MAE E |
|---|---:|---:|---:|---:|
| ≤3 | 91 | 0,422700 | 0,421506 | 0,426944 |
| (3;4] | 85 | 0,435020 | 0,421457 | 0,423019 |
| (4;5] | 36 | 0,409195 | 0,363918 | 0,351808 |
| >5 | 23 | 0,509439 | 0,371812 | 0,320672 |

**[DIỄN GIẢI] D là lựa chọn cân bằng hơn E ở baseline Ridge.** Miền≤3, AUROC dương D−B là **−0,000572**, CI95 **[−0,002967; +0,001807]**; chưa thấy giảm quá guardrail 0,01. E−B là **−0,005715**, CI95 **[−0,010121; −0,001370]**, hơi vượt ngưỡng −0,01 ở cận dưới. Vì thế không nên gọi E đã chắc chắn bảo toàn miền cũ. Hai guardrail CI là mô tả, chưa điều chỉnh đa kiểm định. Chúng dùng 89 peptide đủ điều kiện trong 87 nhóm. Nhóm PSI>5 không có AUROC dương hợp lệ; giá trị null là đúng.

**[ĐO] ESM2 cung cấp thông tin bổ sung, nhưng output mới khảo sát một checkpoint.** W5+ESM-D cải thiện AUROC dương so W5-D **+0,012548**, CI95 mô tả **[+0,006216; +0,019670]**; MAE giảm **0,005550**. ESM-only-D giảm MAE nhưng giảm AUROC dương, đồng thời AUROC âm tăng mạnh. Không có một recipe Ridge tốt nhất cho mọi mục tiêu. Quy trình nested selection theo inner MSE đạt MAE **0,397525**, Δ so W5-D **−0,010278**, CI95 **[−0,015013; −0,005772]**; cải thiện AUROC dương của quy trình này còn chưa phân giải, CI **[−0,003052; +0,013091]**. Không được lấy mức tăng của fixed W5+ESM-D thay cho kết quả nested selection. Chỉ ESM2-35M được chạy; chưa có kết luận về họ/cỡ pLM khác.

**[ĐO] CNN trên ESM có giá trị thêm so với pointwise.** Cùng arm D, ensemble CNN−pointwise giảm MAE **0,005339**, CI95 **[−0,010173; −0,000899]**, và tăng AUROC dương **0,011289**, CI95 **[+0,003434; +0,019133]**. Ở B, giảm MAE là **0,012472**. Với one-hot-D, CNN−pointwise có CI MAE **[−0,006704; +0,003009]**, chưa phân giải. Đây là bằng chứng development rằng trộn vị trí giúp khi dùng representation ESM, không chứng minh CNN luôn thắng với mọi đầu vào; số tham số giữa các head cũng không hoàn toàn bằng nhau.

CNN-D trên ESM giảm MAE **5,75%** và tăng AUROC dương **0,016883** so Ridge W5-D. mCNN-E đứng đầu MAE nhưng chỉ hơn CNN-D **0,000508 PSI**. Ở cùng D, mCNN−CNN có ΔMAE **+0,000639**, CI95 **[−0,001710; +0,003065]**. Chưa có cơ sở nói mCNN vượt CNN; CI ở D cũng không phải phép so trực tiếp mCNN-E với CNN-D. Tất cả CI ngoài Q1 là mô tả, không hiệu chỉnh cho toàn bộ quá trình xem nhiều recipe.

**[ĐO] Hiệu quả chọn đột biến và giới hạn sự kiện hiếm.** Với ESM CNN-D, chọn top5% dự đoán dương trong từng peptide đủ điều kiện đạt precision macro **58,24%**, so W5-D **51,89%**; top10% đạt **49,04%**, so **44,29%**. AP dương **0,509470**, tần suất dương macro cùng cohort **0,124697**. AP âm **0,213667**, tần suất âm macro cùng cohort **0,027336**; precision top5% phía âm **16,77%**. Các số này cho thấy khả năng ưu tiên thí nghiệm, không phải accuracy toàn tập hay xác suất đã calibration. Baseline hằng 0 có score bằng nhau nên top-k phụ thuộc thứ tự phá hòa; không dùng top-k của nó làm kỳ vọng random.

**[ĐO] Scanning transfer có lợi vừa phải; quality weighting hiện gây hại.** Nguồn [replicate-audit.json](output/official/369cb2fe6a1e31e0/tasks/06-78cc356ba4f4/replicate-audit.json) ghi 152.004 ô scan_dev có cả hai replicate, tương quan Pearson **0,707430**. Đây là subset dùng train transfer, không phải toàn bộ 224.470 ô scanning.

| Phép so cùng mô hình/đầu vào phù hợp | ΔMAE | CI95 mô tả |
|---|---:|---|
| Ridge quality−sat-only | +0,004010 | [+0,002965; +0,005173] |
| Ridge thêm scan rep1−sat-only | −0,003072 | [−0,003847; −0,002289] |
| CNN pretrain rep1−CNN scratch | −0,006385 | [−0,009929; −0,003013] |
| CNN pretrain mean12−CNN scratch | −0,006326 | [−0,009905; −0,002890] |
| CNN pretrain mean12−rep1 | +0,000059 | [−0,002124; +0,002183] |

**[DIỄN GIẢI]** Recipe quality weighting hiện tại nên được ghi nhận là kết quả âm; điều này không chứng minh mọi cách dùng chất lượng replicate đều vô ích. Hai cách pretrain đều cải thiện so scratch, chưa thấy mean12 vượt rep1. CNN scratch stage06 khớp metric one-hot CNN-D stage05, là đối chứng nhất quán giữa hai stage. CNN transfer one-hot không phải ESM+scanning; chưa có thí nghiệm kết hợp hai nguồn tín hiệu đó. So với ESM CNN-D, transfer rep1 có ΔMAE **+0,002872**, CI95 **[−0,001682; +0,007555]**; chưa phân giải. Chẩn đoán riêng 20/360 cặp substitution vẫn cần làm.

**[ĐO] Chi phí và phần chưa hoàn tất.** Có **35 task complete, một task running theo manifest**. Stage00–06 đã có artifact; stage11 mới hoàn tất frozen-B và frozen-D của seed17, đủ năm fold. MAE của hai nhánh là **0,407145 / 0,391931**, chỉ head được học; chưa có kết quả LoRA. Task `11-lora-B-s17` mới có checkpoint inner của fold0, thiếu OOF/results/status hoàn tất. Trạng thái running trong snapshot không xác nhận tiến trình từ xa hiện còn sống, và output không đủ để kết luận nguyên nhân dừng là lỗi, timeout hay người dùng ngắt.

Tổng thời gian các task hoàn tất là **9,33 giờ**; riêng hai task frozen stage11 chiếm **7,23 giờ**. Đây là tổng thời gian task được ghi, chưa gồm phần LoRA đang dở. Mã stage11 chạy lại backbone cho từng batch WT/mutant trong mỗi epoch kể cả frozen, giải thích một nguồn chi phí có thể tối ưu bằng cache nếu giữ đúng feature/dtype và giao thức so sánh. GPU ghi nhận hai Tesla T4; runtime hiện không tự cộng VRAM hoặc tự phân phối huấn luyện qua hai card. Chưa benchmark để khẳng định tốc độ sau tối ưu.

Không có output stage07 calibration/locked T, stage08 external, stage09 structure hay stage10 aggregate cuối. Không gọi nguồn ngoài/cấu trúc đã chạy; không có bằng chứng calibration, external validity hoặc hiệu năng LoRA. Không dùng các ô mutation như 122.412 mẫu thống kê độc lập; CI ở đây resample nhóm protein. Protocol thực thi cũng là thiết kế development sau khi biết dữ liệu/lịch sử.

**[ĐỀ XUẤT] Thứ tự tiếp theo dựa trên snapshot này:**

1. Giữ Ridge W5-D làm mốc; ưu tiên ESM CNN-D làm ứng viên khóa tiếp, giữ mCNN-E là đối chứng nhạy cảm. Đánh giá trực tiếp chênh lệch giữa hai ứng viên nếu cần chọn, thay vì lấy thứ hạng MAE làm xác nhận.
2. Hoàn thiện model-specific final refit/export và calibration cho CNN trước đánh giá trên T. Stage07 hiện tự promotion W5; chỉ đổi tên `selected_recipe` chưa đủ để có final CNN hợp lệ. T chưa được dùng ở phân tích này.
3. Tách hoàn tất benchmark lõi khỏi nhánh LoRA tốn giờ; nếu tiếp tục LoRA, resume đúng code/data/protocol/seed, giữ run identity và hoàn thành đủ OOF để so với frozen cùng seed. Không đổi cấu hình trong cùng run để tiết kiệm giờ rồi gộp chung.
4. Hoàn thiện 20/360 pair diagnostics và kiểm nguồn/assay cho T. Nếu mở rộng pLM families hoặc ESM+scanning, lập rõ phép so trước lượt chạy tiếp theo; output này chưa hỗ trợ các kết luận đó.

Các đề xuất trên chưa được thực thi. Không sửa output nhập từ Kaggle, mô hình hay các notebook trong phiên phân tích này.
