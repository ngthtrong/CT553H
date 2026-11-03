# Ghi chú người trình bày

## 1. Dự đoán hiệu ứng đột biến degron ở mức residue và xây dựng công cụ hỗ trợ phân tích

Đây là deck giải thích đề tài từ nền tảng sinh học tới nghiên cứu học máy và phần mềm. Ma trận mở đầu minh họa thiết kế, không là kết quả inference. Mục tiêu là dự đoán hiệu ứng một thay thế amino acid đơn trên độ bền reporter.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/README.md

## 2. Protein được tạo từ một chuỗi amino acid

GIF là mô hình dự đoán cấu trúc Fam188a của Nikolakhs, CC BY-SA 3.0. Không phải HIF1A hoặc cấu trúc degron đang khảo sát. Chuỗi tám AA là ví dụ giả định. Peptide trong nhiệm vụ chính dài 28 residue.

Nguồn: https://commons.wikimedia.org/wiki/File:I-TASSER_predicted_protein_fold_of_Fam188a.gif

## 3. Degron tham gia quá trình phân hủy protein

Sơ đồ đơn giản hóa hệ ubiquitin–proteasome, không mô tả mọi cơ chế phân hủy. E3 cùng các thành phần phù hợp góp phần nhận diện cơ chất. Video NIGMS 3764 của Andreas Martin/HHMI mô phỏng cơ chất gắn chuỗi ubiquitin, được máy AAA+ kéo mở; ubiquitin được tách trước khi cơ chất bị cắt. Video không là quan sát của dataset Zhang. Màu phân tử trong video theo tác giả, khác quy ước màu của sơ đồ.

Nguồn: https://www.nigms.nih.gov/image-gallery/3764, https://www.nigms.nih.gov/image-gallery, https://pubmed.ncbi.nlm.nih.gov/37738965/

## 4. Một phép thay có thể làm thay đổi tín hiệu

Ví dụ giả định MAGLSKVT thành MAGPSKVT, L4P. Thay thế có thể làm thay đổi hoạt động degron, song cũng có thể tác động qua cơ chế khác hoặc không có ảnh hưởng đáng kể. Không gán sự thay L/P này cho một degron đã được đo.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/

## 5. 532 phép thay tạo nhu cầu ưu tiên thí nghiệm

28 vị trí nhân 19 amino acid khác WT là 532 thay thế đơn tối đa. Ma trận có 20 hàng AA; ô WT→WT bị mask. Một peptide chỉ có dưới hoặc bằng 532 ô đo hợp lệ sau QC. Hình là sơ đồ thiết kế, không là dự đoán hay nhãn thực nghiệm.

Nguồn: research/kaggle-roadmap-2026-10-31/dataset-build.json

## 6. GPS chuyển tín hiệu huỳnh quang thành PSI

GFP được gắn peptide; DsRed làm tín hiệu tham chiếu. Tế bào được phân sáu bin theo tỷ lệ GFP/DsRed, rồi giải trình tự để đếm construct. PSI là trung bình có trọng số theo các bin sau chuẩn hóa. Thang Zhang 1–6. Không đọc chiều cao histogram minh họa như số đo thật.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/full-data-audit/psi-build.json

## 7. ΔPSI là hiệu ứng mà mô hình cần dự đoán

ΔPSI=PSI(mutant)−PSI(WT). Giá trị dương cho thấy reporter mutant bền hơn trong assay này; có thể phù hợp với degron bị suy yếu nhưng chưa xác định cơ chế. Không suy ra half-life định lượng, tác động trên protein nguyên vẹn hoặc gây bệnh. Ví dụ 2,5 và 3,8 không phải số liệu repo.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/

## 8. Saturation và scanning có độ phủ bổ sung

Scanning dùng replacement phụ thuộc WT, theo các hướng R/A/S; trên alphabet tạo 20 kiểu WT→mutant trong 380 kiểu có hướng không đồng nghĩa. Saturation khảo sát 19 AA thay thế mỗi vị trí khi đủ dữ liệu. Không giả định mọi ô trong thiết kế đều qua QC.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/scan-sat-merge-2026-10-23/README.md

## 9. Mỗi ô đột biến trở thành một bản ghi có nhãn

Mutation cell là khóa peptide/vị trí/WT/mutant, không là một protein độc lập. Scanning dùng mut0 đúng replicate. Saturation không có mut0; WT nội tại lấy trung vị các ô đồng nghĩa hợp lệ của từng nửa thí nghiệm. Không dùng BAG6 WT như replicate hoặc mốc saturation.

Nguồn: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/full-data-audit/saturation-matrix.json

## 10. Dữ liệu sau QC giữ toàn dải PSI

Số liệu được đọc từ dataset-build.json: saturation_cells 122412, saturation_peptides 235, saturation_groups 221, scan_cells 224470. Số scanning là toàn bộ sau QC, không phải số ô đều được dùng pretrain: scan_dev, scan_T và sat_overlap có vai trò riêng. Theo chỉnh sửa của người dùng, không trình bày các phiên bản dữ liệu hoặc so sánh tiến trình phiên bản.

Nguồn: research/kaggle-roadmap-2026-10-31/dataset-build.json

## 11. Pipeline nối dữ liệu, mô hình và công cụ

Sơ đồ định hướng nội dung. Các mô hình và so sánh ở benchmark development không tự chuyển thành model sản phẩm. Việc khóa cấu hình, calibration, tập T và kiểm chứng ngoài vẫn chưa hoàn tất theo snapshot tài liệu.

Nguồn: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/README.md

## 12. Trình tự là đầu vào; PSI dùng để tạo nhãn

Input chính chỉ có WT sequence, vị trí và mutant AA. Không đưa PSI WT/mutant, read count, group/fold hoặc stratum vào feature. Tính ΔPSI từ hai phép đo là chuẩn bị nhãn; không phải cung cấp sẵn nhãn khi inference.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/features.py, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 13. Giữ cùng nhóm protein khi chia dữ liệu

Chia theo nhóm tương đồng, chặn trùng sequence xuyên scanning/saturation. Trong mỗi outer fold, tuning và preprocessing chỉ dùng inner train/validation; sau đó refit trên outer train rồi đo outer test. Seed 17/29/43. 221 nhóm là đơn vị lấy mẫu lại cho CI. Các nhóm heuristic không chứng minh độc lập sinh học tuyệt đối.

Nguồn: research/kaggle-roadmap-2026-10-31/dataset-build.json, research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 14. Ridge là đối chứng cho giá trị của ngữ cảnh

Ordered radius=5 tạo 40 feature WT/mutant, 20 composition và 200 ordered-neighbour features, tổng 260. Vị trí đột biến không đưa vào một cột số độc lập; dùng để lấy ngữ cảnh. Ridge regularization hạn chế trọng số lớn. Không khẳng định deep learning mặc nhiên hơn Ridge.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/features.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 15. One-hot CNN học các mẫu trình tự cục bộ

Head thực dùng crop 15 vị trí, 20 one-hot channels cộng chỉ báo trung tâm và 60 feature phép thay/thành phần. CNN kernel=5; đây là đối chứng cùng họ head khi không có delta ESM. Hình chỉ thể hiện nguyên lý.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/degron_v3/features.py

## 16. ESM2 biến trình tự thành biểu diễn số

WT và mutant qua cùng ESM2 pretrained; ΔH=H_mutant−H_WT. Ở head CNN, dùng crop quanh site và projection, kết hợp one-hot WT, center indicator và 60 feature phụ. Không mô tả các chiều embedding như đại lượng sinh học đo trực tiếp. Benchmark đang trình bày chỉ có ESM2-35M.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 17. Pointwise và CNN khác cách trộn vị trí

Pointwise dùng Conv1D kernel1; CNN dùng kernel5. Head còn max-pooling và center pooling, nên pointwise không đồng nghĩa toàn mô hình bỏ qua mọi vị trí khác. Số tham số head khác nhau; so sánh không cô lập hoàn toàn tác động trộn vị trí khỏi sức chứa. Cả hai giữ đầu vào phụ nhất quán.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 18. mCNN khảo sát nhiều độ rộng ngữ cảnh

Mỗi nhánh có convolution, activation, max-pooling và center pooling. Các đặc trưng nhánh nối với feature phụ trước regression head. Đây là thiết kế đang được so sánh, không là bằng chứng nhiều kernel vượt một kernel.

Nguồn: research/kaggle-roadmap-2026-10-31/degron_v3/neural.py

## 19. Frozen và LoRA học những tham số khác nhau

Frozen chỉ cập nhật head. LoRA giữ weights backbone nền và học adapter tham số hạng thấp cùng head. Đây là nhánh fine-tuning riêng, không đồng nhất trực tiếp với CNN trên feature cache. Trong snapshot Kaggle chỉ frozen seed17 hoàn thành, LoRA chưa đủ OOF; chưa có phép so LoRA/frozen đầy đủ.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/README.md

## 20. Sai số, xếp hạng và CI trả lời các câu hỏi riêng

MAE tính macro theo 235 peptide. AUROC/AP dương dùng 184 peptide đủ ≥3 ô mỗi lớp; không là accuracy. AP phụ thuộc tỷ lệ event. Bootstrap 5000 theo 221 nhóm protein, không resample 122412 ô như độc lập. MAE là metric chính cho hồi quy; AUROC đánh giá xếp hạng sự kiện phụ. Phần uncertainty đặt ở CI chênh lệch, không là xác suất từng mutation.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 21. Thí nghiệm A: nên học trên phạm vi PSI nào?

Các cấu hình trong protocol gọi A/B/C/D/E, nhưng màn chiếu dùng tên phạm vi dễ đọc. Test W giữ 235 peptide cùng 221 nhóm. PSI≤3/4/5 không là nhãn degron/non-degron tuyệt đối. Balanced thay trọng số trong train, không đổi population test.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 22. Học toàn dải giúp Ridge giảm sai số hồi quy

Hai biểu đồ tái sử dụng từ deck trước; số liệu và hash nguồn được kiểm lại. D−B có CI97,5% điều chỉnh cho hai phép so chính, hỗ trợ cải thiện nhưng chưa chứng minh giảm ít nhất 0,02 PSI trên toàn CI. Cân bằng tốt hơn ở PSI cao, có đánh đổi ở miền thấp. Stratum PSI>5 không có event Δ≥1 hợp lệ; AUROC dương không xác định.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 23. Thí nghiệm B: ESM2 và CNN có ích đến đâu?

Bảng chính khớp bản paste: MAE Ridge 0,4078; pointwise 0,3897; CNN 0,3844; mCNN 0,3850; mCNN balanced 0,3838. Bốn dòng đầu cùng train toàn dải, dòng cuối đổi weighting. AUROC dương lần lượt khoảng 0,8319/0,8375/0,8488/0,8463/0,8470. Các nút đổi metric; PDF dùng bản MAE tĩnh. Chưa là kết quả locked T hoặc mô hình sản phẩm.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json

## 24. Chênh lệch nhỏ cần được đọc cùng khoảng tin cậy

Phép so trực tiếp mCNN-E minus CNN-D: delta=-0.0005076313196522603; CI95 mô tả=[-0.003157472974124294, 0.0022234273088492414], 5000 bootstrap theo nhóm. Đây là so sánh cả kiến trúc và train weighting; cùng train D, mCNN−CNN cũng chưa phân giải. CI ngoài phép so phạm vi train chính là mô tả, không hiệu chỉnh toàn bộ chọn recipe.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis-details.json, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 25. Thí nghiệm C: chuyển giao còn những câu hỏi mở

CNN transfer rep1 giảm MAE khoảng 0,006385 so scratch, CI95 mô tả [-0,009929;-0,003013]. Đây là one-hot CNN và saturation OOF, không là ESM+scanning hay kiểm chứng locked T. Mean12 chưa vượt rep1; quality weighting hiện có kết quả âm. Snapshot LoRA chưa đầy đủ. Không gộp chi phí/runtime hoặc kết quả local đang mở vào benchmark Kaggle.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/output-analysis-details.json

## 26. Ma trận hỗ trợ lựa chọn đột biến để kiểm chứng

Các ô và thanh trên hình minh họa luồng; không phải điểm inference. Công cụ cần giữ model/source version và miền áp dụng. Không đọc ΔPSI như xác suất bệnh hoặc kết luận cơ chế E3. Nếu có xác suất sự kiện, calibrator phải được đánh giá riêng cho model.

Nguồn: system/README.md

## 27. Phân biệt baseline phục vụ và prototype giao diện

Screenshot tái sử dụng của Workspace UI v2, không là ứng dụng React baseline hoặc inference thật. PostgreSQL, persistent projects/history, batch jobs, protein tiling web flow, import/comparison còn phải triển khai/kiểm chứng. Model serving vẫn m3-ext4.0-platt-v1. Các test baseline ghi trong tài liệu là lịch sử, không được chạy lại trong phiên tạo deck.

Nguồn: system/README.md, system/design/workspace-ui-v2/README.md

## 28. Những phần đã có và những phần cần hoàn thiện

Snapshot Kaggle cập nhật 01/11 11:18:07Z, phân tích ngày 02/11. Bản ghi local 03/11 12:38 UTC+8 ghi 456 job complete kế thừa, 178 pending, một checkpoint LoRA paused: ảnh chụp tiến độ, không xác nhận worker đang sống hoặc 635 thí nghiệm độc lập. Không dùng trạng thái job thay benchmark. Chưa đóng G2/G3.

Nguồn: research/README.md, system/README.md

## 29. Đóng góp gắn với các bằng chứng có thể kiểm tra

Đây là các trục đóng góp đang phát triển. Đã có dữ liệu/benchmark và kết quả development, nhưng kiểm chứng cuối cùng và phần mềm mở rộng chưa hoàn tất. Không tuyên bố một kiến trúc mới, mọi protein đều tổng quát hóa tốt hoặc website là tính mới độc quyền.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, system/README.md

## 30. Khóa lựa chọn rồi kiểm chứng trước khi tích hợp

Stage final promotion hiện hỗ trợ Ridge ngữ cảnh; CNN cần final refit/export riêng. Cần khóa cấu hình/calibration trước đọc T. T của các thiết kế có lịch sử tiếp xúc khác nhau; mô tả đúng held-source thay vì mặc định hoàn toàn độc lập. Nguồn ngoài phải kiểm endpoint/provenance. Nghiên cứu model và phần mềm có thể làm song song.

Nguồn: research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md, system/README.md

## 31. Từ trình tự đến một giả thuyết có thể kiểm chứng

Kết nối sinh học, nhãn thực nghiệm, đầu vào sequence-only, benchmark theo nhóm và công cụ. Bằng chứng đang có ủng hộ khảo sát ESM2 với CNN, nhưng chưa là kiểm chứng độc lập trên mọi nguồn hay hoàn tất sản phẩm. Slide lộ trình học sáu buổi đã được bỏ theo annotation của người dùng.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, system/README.md

## 32. Các thuật ngữ dùng trong deck

Các định nghĩa chỉ phục vụ đọc deck. CI metric không là uncertainty interval cho từng dự đoán. PSI không là thời gian bán hủy; ΔPSI không là xác suất gây bệnh.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/kaggle-roadmap-2026-10-31/output-analysis.json

## 33. Từ read counts đến ΔPSI cần đúng mốc WT

Không dùng trực tiếp raw bin counts chưa chuẩn hóa vào công thức. PSI nguồn có bước chuẩn hóa theo bin/điều kiện; kiểm tái dựng 261865 giá trị khớp tác giả trong 5e-7 theo audit. Saturation reads≥10, ≥10 ô đồng nghĩa mỗi nửa và mutation cell có cả hai nửa hợp lệ. Mốc WT khác giữa saturation và scanning; BAG6 WT là điều kiện khác. Chỉ mô tả audit đã có, không tính lại dữ liệu thô trong phiên này.

Nguồn: research/full-data-audit/psi-build.json, research/full-data-audit/saturation-matrix.json, research/kaggle-roadmap-2026-10-31/dataset-build.json

## 34. Ví dụ HIF1A: đọc ma trận nhãn thực nghiệm

Q16665_HIF1A_25, tọa độ protein 553–580, WT PSI nội tại 2,1865. Có 529 ô đo, 186 ô ΔPSI≥1. Chọn ví dụ theo ≥500 ô và số ô dương lớn nhất, tie ID. Hình đo được tái sử dụng, không là inference mới hoặc phát hiện cơ chế HIF1A/VHL. Ô WT và thiếu được mask; không gán zero cho ô thiếu.

Nguồn: research/slide-figures-2026-10-15/example-matrix.json

## 35. Bảng kết quả và đơn vị đánh giá

Các metric tính macro theo peptide, event dương Δ≥1, mỗi peptide ≥3 ô mỗi lớp. Đây là OOF development. AUROC khác cohort không so trực tiếp. MAE mCNN cân bằng−CNN toàn dải CI95 [-0,003157;+0,002223]. Chênh lệch CNN−pointwise CI95 [-0,010173;-0,000899], nhưng head capacity khác nhau.

Nguồn: research/kaggle-roadmap-2026-10-31/output-analysis.json, research/kaggle-roadmap-2026-10-31/output-analysis-details.json

## 36. Nguồn và bằng chứng có thể tra cứu theo chủ đề

Nhãn tác giả, nhãn đo, minh họa, fixture và đề xuất được phân biệt. Hình/gif/video và mọi figure có nguồn, hash trong evidence.json. Các audit baseline PAP/Degformer và R0–R6 là lịch sử, khác population/protocol; không nối thành một đường tiến bộ hoặc so AUROC trực tiếp với W. Tài liệu bài báo có erratum Figure2A, DOI10.1016/j.molcel.2023.10.021; deck không dùng Figure2A. Không hiển thị các phiên bản dữ liệu trên màn chiếu.

Nguồn: https://pubmed.ncbi.nlm.nih.gov/37738965/, research/README.md, asset-notices.md
