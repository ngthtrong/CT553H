# Ghi chú người trình bày

## 1. Hiệu ứng đột biến degron ở mức residue

Buổi giới thiệu đề tài và trao đổi tiến độ; không phải bảo vệ hoàn tất. Hình mở đầu dùng ma trận nhãn đo HIF1A. Mục tiêu: người nghe hiểu bài toán, thấy bằng chứng và góp ý hướng tiếp theo.

Nguồn: slide-figures-2026-10-15/example-matrix.json

## 2. Degron tham gia quá trình phân hủy protein

Sơ đồ là nguyên lý đơn giản hóa UPS. GIF Fam188a của Nikolakhs, CC BY-SA 3.0, chỉ minh họa một protein gấp cuộn, không phải HIF1A/degron đã đo. Hoạt tính của đoạn peptide tách rời có thể khác trong protein nguyên vẹn.

Nguồn: 

## 3. Một phép thay tạo một ô trong bản đồ hiệu ứng

WT là trình tự tham chiếu. Ma trận hiển thị 28 vị trí và 20 amino acid; ô WT→WT được mask, có 532 phép thay thật khi đủ dữ liệu. Đây là sơ đồ đầu ra, không phải dự đoán mô hình.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 4. GPS chuyển tín hiệu reporter thành nhãn ΔPSI

Histogram là minh họa cách đo, không phải số liệu thực nghiệm. PSI của Zhang dùng sáu bin, thang 1–6; thấp là reporter kém bền. Không tự suy dấu ΔPSI thành cơ chế E3 hay khả năng gây bệnh.

Nguồn: full-data-audit/psi-build.json

## 5. Ví dụ HIF1A cho thấy hiệu ứng tập trung theo vị trí

Peptide Q16665_HIF1A_25, vị trí protein 553–580. WT nội tại PSI2.1865; 186 ô ΔPSI≥1. Ví dụ được chọn theo ≥500 ô, nhiều ô dương nhất, hòa lấy ID nhỏ nhất. Đối chiếu motif HIF1A/VHL là y văn, không phải phát hiện cơ chế mới. Ô WT và ô thiếu đều được mask.

Nguồn: slide-figures-2026-10-15/example-matrix.json

## 6. Giá trị sử dụng là ưu tiên đột biến để kiểm chứng

Không coi xếp hạng dự đoán là thay thế thực nghiệm. ClinVar là annotation và động lực nghiên cứu; liên hệ bệnh ở mức residue chưa thiết lập. Các ô trong hình chỉ mô tả lựa chọn, không phải điểm mô hình.

Nguồn: variant-coverage-2026-10-15/README.md

## 7. Công trình liên quan trả lời các câu hỏi khác nhau

Không nhận ma trận hoặc web là tính mới độc quyền. Khác endpoint thì không so trực tiếp AUROC. MetaDegron có một classifier dùng chung với lựa chọn motif/E3; không phải mọi menu là một lớp E3 học độc lập.

Nguồn: metadegron-analysis-2026-10-21/comparison-and-positioning.md

## 8. Ba mục tiêu nối nghiên cứu với công cụ

Không đặt dự đoán E3 hay chẩn đoán biến thể gây bệnh làm nhiệm vụ chính. Không có phép đo sinh học mới. Công cụ phục vụ hình thành giả thuyết và lựa chọn thí nghiệm.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 9. Các câu hỏi đang dẫn dắt hướng nghiên cứu

Sơ đồ là quan hệ nghiên cứu, không là lịch chạy. Các kết quả được tổ chức theo câu hỏi, không theo mã phiên hay thứ tự thời gian.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 10. Nguồn dữ liệu được dùng đúng vai trò

Core v3 chỉ chứa Zhang và UniProt, không chứa ClinVar/Koren/Larsen/MetaDegron hoặc weights. Larsen/MaveDB là nguồn khảo sát với endpoint khác. Phân biệt nguồn đã tải, đã audit và đã dùng fit.

Nguồn: kaggle-roadmap-2026-10-31/DATASET.md, full-data-audit/README.md

## 11. Hai thiết kế đột biến có độ phủ bổ sung

Scanning có phép thay là hàm của WT: hướng R/A/S, tổng20 cặp có hướng trong380 cặp không đồng nghĩa. Hình biểu thị thiết kế lý tưởng, không khẳng định mọi ô đều qua QC.

Nguồn: scan-sat-merge-2026-10-23/README.md

## 12. Mốc WT phải phù hợp với từng thí nghiệm

Saturation không có mut0; dùng trung vị ô đồng nghĩa từng nửa. Scanning dùng mut0 đúng replicate. Không lấy BAG6 WT làm mốc saturation. PSI dựng lại261865 giá trị khớp tác giả trong5e-7 khi mô phỏng điều kiện tái lập.

Nguồn: full-data-audit/psi-build.json, full-data-audit/saturation-matrix.json

## 13. Độ lặp lại của nhãn đặt giới hạn cho cách đọc kết quả

0.8335 là Pearson giữa hai nửa trên cohort saturation theo audit. Không so noise_share của tổng phương sai với noise_share của phần dư như cùng đại lượng. Replicate là mốc độ tin cậy của phép đo, không phải trần tuyệt đối cho mọi estimator.

Nguồn: full-data-audit/saturation-matrix.json, full-data-audit/replicate-audit.json

## 14. Chia theo nhóm protein để kiểm khả năng tổng quát hóa

Hai thiết kế có population, eligibility và preprocessing khác, không nối AUROC thành một đường tiến bộ. V3 dùng5outer folds và3seed inner-validation; các transform chỉ fit trong train, epoch chọn rồi khởi tạo lại refit. Nhóm có homology heuristic, không chứng minh độc lập sinh học tuyệt đối.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 15. Sai số, xếp hạng và ngân sách thí nghiệm là các mục tiêu riêng

V3 MAE có235 peptide; event dương Δ≥1 có184peptide đủ điều kiện, âm Δ≤−1 có110. Mỗi lớp phải có≥3ô. Bootstrap5000 theo nhóm, không theo122412ô. AUROC không là accuracy; AP cần đọc với tần suất event.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 16. Ngữ cảnh cục bộ bổ sung thông tin ngoài phép thay

M0 pair+composition0.8393; unordered0.8625; ordered±3 0.8682. Ordered−M0 +.0289 CI[.0264,.0313]. Trung bình AUROC các seed trong nguồn này, không gán là ensemble v3. Mô hình tuyến tính composition hằng trong peptide không tự đổi thứ hạng giữa vị trí có cùng phép thay.

Nguồn: residue-task-derisk-2026-10-15/model.json

## 17. Học toàn dải PSI giảm sai số hồi quy của Ridge

So sánh trên cùng 235 peptide và 221 nhóm protein. Học toàn dải giảm MAE 5,94% so với chỉ học PSI ≤ 4. Hai phép so chính dùng khoảng tin cậy 97,5% đã điều chỉnh; cận gần 0 chưa bảo đảm mức giảm tối thiểu 0,02 PSI. Nhánh train hẹp vẫn dùng validation toàn dải. PSI(WT) chỉ là metadata, không phải feature.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 18. Lợi ích toàn dải tập trung ở miền PSI cao

Bốn miền test có 91, 85, 36 và 23 peptide. Cân bằng dữ liệu giúp miền PSI cao nhưng có đánh đổi ở miền thấp. Miền PSI > 5 không có hiệu ứng dương ΔPSI ≥ 1, vì vậy AUROC dương không xác định. Guardrail của Ridge không tự chuyển sang CNN: so với CNN chỉ học PSI ≤ 4, CNN toàn dải tăng MAE miền PSI ≤ 3 khoảng 0,00870; khoảng tin cậy AUROC cũng chưa bảo đảm mức giảm dưới 0,01.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 19. ESM bổ sung tín hiệu cho baseline ngữ cảnh

Thêm ESM vào Ridge ngữ cảnh tăng AUROC dương khoảng 0,01255, với khoảng tin cậy 95% mô tả từ 0,00622 đến 0,01967. Quy trình chọn recipe bằng validation đạt MAE 0,397525; cải thiện AUROC của quy trình này còn chưa phân giải. Không lấy điểm của một fixed recipe thay cho kết quả nested selection. Benchmark toàn dải hiện chỉ có ESM2-35M.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 20. CNN cải thiện thêm sau representation ESM

Cùng representation và train toàn dải, CNN giảm MAE 0,00534 so với pointwise; khoảng tin cậy 95% mô tả từ −0,01017 đến −0,00090. AUROC dương tăng khoảng 0,01129. Pointwise và CNN có 36.833 và 57.185 tham số head, nên phép so chưa cô lập hoàn toàn tác động trộn vị trí khỏi sức chứa.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 21. Nhiều cửa sổ chưa chứng minh vượt một cửa sổ

Nhiều cửa sổ trên train cân bằng có MAE 0,383846, so với 0,384354 của CNN toàn dải. Chênh lệch −0,000508 có khoảng tin cậy 95% mô tả từ −0,003157 đến +0,002223. Đây còn là hai phân bố train khác nhau. Khi giữ cùng train toàn dải, nhiều cửa sổ cũng chưa chứng minh vượt CNN. CNN chỉ học PSI ≤ 4 vẫn đáng giữ nếu ưu tiên miền PSI thấp.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 22. Học tốt nhãn tile chưa bảo đảm chuyển sang mutation effect

Phép so dùng cùng encoder, cùng cách fine-tune và cùng miền đánh giá 91 peptide. Tiền huấn luyện trên 212.616 tile học tốt nhiệm vụ riêng (Pearson khoảng 0,864), nhưng sau fine-tune đạt AUROC 0,8098 so với 0,8175 của khởi tạo ngẫu nhiên. Chênh lệch có khoảng tin cậy còn chứa 0. Kết luận chỉ giới hạn thiết kế tiền huấn luyện nhãn tile đã thử, không áp cho mọi pLM hay mọi cách chuyển giao.

Nguồn: pretrain-p3-2026-10-22/results.json

## 23. Scanning pretrain có lợi cả ngoài các kiểu thay đã thấy

Đây là CNN đầu vào one-hot, không phải thí nghiệm kết hợp ESM với scanning. Nhóm 20 kiểu thay có 6.433 ô; 360 kiểu còn lại có 115.979 ô, cùng phủ 235 peptide và 221 nhóm. Cả hai khoảng tin cậy MAE đều ở phía cải thiện nhưng là phân tích hậu nghiệm mô tả. Mean của hai replicate chưa hơn rep1 rõ ràng; quality weighting làm MAE tăng khoảng 0,00401. Kết quả này là saturation OOF, chưa phải đánh giá trên tập T.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 24. Đối chiếu Degformer cần kiểm cả chồng mẫu và ngân sách nhãn

Checkpoint công bố có 42.163 trên 47.847 ô mutation và WT của cả 91 peptide trong train. Loại ô trùng chưa tạo một peptide holdout. Retrain sạch cụm đạt AUROC 0,806775 so với 0,820822 của Ridge mở rộng train. Khoảng tin cậy chênh lệch còn chứa 0. Không đọc chênh lệch checkpoint/retrain thành tác động nhân quả chỉ do leakage vì các điều kiện huấn luyện cũng thay đổi.

Nguồn: r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json

## 25. Xếp hạng giúp tập trung ngân sách vào đột biến đáng thử

Precision dương được tính macro trong 184 peptide đủ điều kiện. Top 5% đạt 58,24% với CNN và 51,89% với Ridge; top 10% tương ứng 49,04% và 44,29%. AP dương 0,50947 đi cùng tần suất dương macro 0,124697. Phía âm có AP 0,213667 trên 110 peptide, precision top 5% khoảng 16,77%. Đây là ranking utility, không là accuracy toàn tập hoặc xác suất đã calibration.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 26. Độ ổn định và chi phí cùng tham gia lựa chọn mô hình

CNN có MAE tốt hơn Ridge ở 156 trên 235 peptide và ở cả năm fold. Tổng thời gian task hoàn tất là 9,3265 giờ; hai task frozen stage11 chiếm 7,23 giờ. Nhánh frozen mới có seed17 và đủ năm fold; LoRA chưa có OOF hoàn chỉnh. Một trạng thái running trong snapshot không xác nhận tiến trình từ xa còn sống. Không gộp kết quả runtime local đang chuẩn bị vào snapshot Kaggle này.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, kaggle-roadmap-2026-10-31/output-analysis-details.json

## 27. Hiệu chuẩn nối điểm hồi quy với xác suất sự kiện

Bằng chứng trên slide thuộc Ridge đã hiệu chuẩn, đánh giá OOF trên 91 peptide. Brier của Platt khoảng 0,0925 so với 0,1139 của tần suất nền. Điểm hồi quy ΔPSI không tự là xác suất. Reliability còn thiên thấp do khác phân bố giữa pool calibration và miền test; chưa gọi là hiệu chuẩn hoàn hảo. CNN cần calibrator và quy trình đánh giá riêng.

Nguồn: calibration-p6-2026-10-22/results.json

## 28. Miền áp dụng cần được đánh giá cùng với dự đoán

Cổng được khảo sát cho miền train PSI ≤ 4. PSI của peptidome screen lệch WT nội tại khoảng 0,9 nên không áp ngưỡng thô 4 trực tiếp. Phân loại trong miền, giáp ranh, ngoài miền nói về sự phù hợp dữ liệu, không bảo đảm độ chính xác ΔPSI. Full-PSI cũng không tự chứng minh áp dụng được cho mọi protein. Tích hợp cổng này vào ứng dụng nền còn cần hoàn thiện.

Nguồn: r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json

## 29. Công cụ đưa ma trận và danh sách ưu tiên vào cùng một luồng

Ảnh chụp prototype Workspace UI v2 hiện hành, lấy đúng vùng ma trận và inspector. Mọi score và xác suất trong prototype là fixture tổng hợp; không có model inference hoặc backend. Mã React/FastAPI nền là một phần riêng. Ảnh dùng để giới thiệu luồng sử dụng, không phải nghiệm thu chức năng mở rộng.

Nguồn: ../system/design/workspace-ui-v2/README.md

## 30. Một ứng dụng local giữ kết quả cùng nguồn gốc

Stack đã chọn là React/TypeScript và FastAPI chạy local. SQLite đã dùng cho baseline; PostgreSQL và lưu workspace bền vững thuộc phạm vi cần triển khai, kiểm chứng. Không yêu cầu public hosting. Sơ đồ giới thiệu kiến trúc và provenance, không xác nhận mọi module đã hoàn tất.

Nguồn: ../system/README.md

## 31. Phần mềm có nền tảng để tiếp tục mở rộng

Các kiểm thử ghi trong tài liệu thuộc baseline và không được chạy lại trong phiên dựng slide. Project/history, durable batch jobs, whole-protein web flow và nhập dữ liệu đo vẫn cần triển khai theo phạm vi mở rộng. Domain gate mới chưa được tích hợp đúng trong baseline. Không coi endpoint đã thiết kế là chức năng đã nghiệm thu.

Nguồn: ../system/README.md

## 32. Những gì đã thực hiện tạo nền tảng cho hướng nghiên cứu

Tổng hợp những sản phẩm và hiểu biết đã có, gắn với ba mục tiêu đầu deck. Đóng góp đang phát triển gồm dữ liệu/benchmark, phương pháp thực nghiệm, đánh giá và phần mềm. Không cần khẳng định kiến trúc mới để trình bày giá trị của nghiên cứu. Đây vẫn là buổi trao đổi tiến độ, chưa kết luận hoàn tất đề tài.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, model-selection-pipeline-2026-10-24/README.md

## 33. Ưu tiên tiếp theo là khóa lựa chọn và kiểm chứng khả năng chuyển giao

Final promotion tự động hiện hỗ trợ Ridge ngữ cảnh; CNN cần final refit và export riêng. Khóa recipe và calibration trước khi đọc tập T. Scanning đã từng được thăm dò trong lịch sử, nên tập T cần mô tả đúng phạm vi held-source và lịch sử tiếp xúc. Nghiên cứu mô hình và hoàn thiện công cụ có thể tiến hành song song. LoRA không phải điều kiện bắt buộc để hoàn thiện benchmark lõi.

Nguồn: kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md

## 34. Trao đổi về hướng nghiên cứu và bước tiếp theo

Mời giảng viên góp ý mục tiêu và hướng ưu tiên. Đây là buổi giới thiệu/tiến độ, không phải nghiệm thu toàn bộ đề tài. Có thể mở overview hoặc phụ lục để trao đổi chi tiết.

Nguồn: 

## 35. Cách đọc các thuật ngữ trong bài toán

Residue: amino acid tại một vị trí. WT: trình tự tham chiếu. OOF: dự đoán ngoài fold.

Nguồn: model-selection-pipeline-2026-10-24/README.md

## 36. Chi tiết tạo nhãn và kiểm chất lượng

Đồng nghĩa dùng làm WT nội tại; ô thiếu được mask; điều kiện đo được giữ riêng.

Nguồn: full-data-audit/psi-build.json, full-data-audit/saturation-matrix.json

## 37. Độ tin cậy phụ thuộc mức phân tích

Pearson ΔPSI scanning là 0,7229; saturation là 0,8335. Jaccard scanning tính theo vị trí, còn saturation tính theo ô. Các cohort và mẫu số khác nhau, nên đây là mô tả độ tin cậy chứ không là phép so ghép cặp hai nguồn. Không so phần nhiễu trên phương sai dư với phần nhiễu trên tổng phương sai như cùng đại lượng.

Nguồn: full-data-audit/replicate-audit.json, full-data-audit/saturation-matrix.json

## 38. Mô hình composition không phân biệt mọi vị trí

Bất biến áp cho mô hình chỉ dựa thành phần trong cùng peptide và cùng cặp thay thế. Không gán nó cho toàn bộ PAP có kênh đầu C hoặc mô hình có ngữ cảnh. Baseline được gọi composition trong tài liệu thực tế còn có one-hot WT và mutant. Oracle đọc nhãn test chỉ mô tả giới hạn biểu diễn, không là hiệu năng test của mô hình học được.

Nguồn: composition-context-audit.md, residue-task-derisk-2026-10-15/model.json

## 39. Learning curve cần tách model đơn và ensemble

Độ nhạy phân cụm là phép kiểm riêng; không đếm phân hoạch trùng nhau như bằng chứng mới.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis-details.json, recluster-sensitivity-2026-10-22/results.json

## 40. Các thiết kế tương tác chưa vượt baseline ổn định

Đây là những thiết kế đã thử, không phải phủ định mọi tương tác phi tuyến.

Nguồn: g2-saturation-2026-10-18/results.json, g2-extension-2026-10-18/e2-candidates.json

## 41. Lọc trùng mức ô chưa loại được chồng mức peptide

Cần đánh giá theo peptide/nhóm protein được giữ riêng.

Nguồn: g2-saturation-2026-10-18/results.json, r1-degformer-clean-2026-10-22/run-kaggle-20261022/results.json

## 42. Khảo sát cỡ ESM thuộc các thiết kế riêng

Bảng dùng các Ridge bổ sung ESM trên thiết kế miền 91 peptide, không cùng population với benchmark toàn dải. Các cỡ ESM trong bảng đều chưa cho lợi ích phân giải được theo phép so đã định. Registry nhiều checkpoint không đồng nghĩa mọi checkpoint đã được đánh giá. Trong output toàn dải hiện chỉ ESM2-35M có kết quả.

Nguồn: r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json

## 43. Đọc nhiều tiêu chí trên cùng các ứng viên

Các điểm là ensemble dự đoán ba seed; vẫn là phân tích development.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

## 44. Scanning transfer: tách các kiểu thay thế để kiểm chuyển giao

Mỗi peptide chỉ tính các ô thuộc cohort đang xét. Nhóm 20 kiểu thay có 114 peptide đủ điều kiện AUROC dương; nhóm 360 có 184. Không so trực tiếp hai macro AUROC như cùng population. Hai khoảng tin cậy MAE trên hình là hậu nghiệm mô tả, lấy mẫu lại 5.000 lần theo nhóm protein.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis-details.json

## 45. ClinVar hỗ trợ động lực ở mức vùng, chưa xác nhận mức residue

Odds ratio Mantel–Haenszel theo protein khoảng 2,14783, khoảng tin cậy 95% từ 2,07193 đến 2,22651, trên 3.114 tầng có thông tin. Đây là liên hệ mức vùng, chưa là quan hệ nhân quả. Phân tích khớp đúng mutation ở saturation còn ít biến thể có phân loại và khoảng tin cậy AUC vẫn chứa 0,5. ClinVar không được dùng làm nhãn chọn model ΔPSI.

Nguồn: variant-coverage-2026-10-15/enrichment.json, variant-coverage-2026-10-15/README.md

## 46. Nhãn E3 chưa đủ cho nhiệm vụ có điều kiện E3

Chỉ một nhóm có ít nhất năm peptide; không dùng số E3 trong menu thay cho số lớp có thể học.

Nguồn: e3-labels-audit/README.md

## 47. Nguồn ngoài cần được đánh giá theo endpoint và khả năng sử dụng

Koren chưa có kết quả đánh giá model; dữ liệu khác thang, độ dài và chỉ có năm nhóm mới nên không đưa vào train. Larsen cung cấp nhãn tile, không có mutation ΔPSI đầy đủ. Phân tích cấu trúc trên MaveDB là thăm dò, còn vấn đề endpoint và cấu trúc dimer cần kiểm lại. SaProt true-3Di chưa có output; có weights không thay được mapping cấu trúc.

Nguồn: koren-s4-audit-2026-10-22/results.json, larsen-nuclear-and-risks-2026-10-15/README.md, architecture-check/README.md

## 48. Calibration và domain gate trả lời hai câu hỏi khác nhau

Cả hai cần được kiểm lại khi đổi model hoặc thay phạm vi dữ liệu.

Nguồn: calibration-p6-2026-10-22/results.json, r3-domain-gate-2026-10-22/run-kaggle-20261022/results.json

## 49. Tính tái lập nối dữ liệu, model và kết quả phục vụ

Đã kiểm hash và kích thước 2.986 file trong snapshot, gồm 83 OOF thuộc 47 recipe. Phân tích tính lại khớp số đã lưu. Các bằng chứng kiểm thử app nền trong tài liệu là lịch sử, không phải kết quả kiểm thử lại trong phiên tạo deck. Không gộp runtime local khác môi trường vào cùng kết quả Kaggle.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json, ../system/README.md

## 50. Tài liệu và bằng chứng có thể tra cứu theo chủ đề

Nguồn không đặt thành footnote trên từng slide theo yêu cầu. Có thể mở Ghi chú để xem nguồn và phạm vi của slide đang trình chiếu. Phụ lục, slide-sources.json và evidence.json giữ chuỗi truy vết. Các website được dùng khảo sát template/style, không bổ sung số hiệu năng mô hình.

Nguồn: kaggle-roadmap-2026-10-31/output-analysis.json

