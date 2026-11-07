---
title: ĐỀ CƯƠNG LUẬN VĂN
subtitle: |
  Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong nghiên cứu degron và xây dựng công cụ phân tích
lang: vi-VN
---

**Sinh viên thực hiện:** Nguyễn Thanh Trọng — MSSV: B2305615  
**Giáo viên hướng dẫn 1:** TS. Hồ Quang Thái — MSCB: [Bổ sung]  

**Mốc cập nhật: 03/11/2026.** Đề cương phản ánh các kết quả phát triển đã lưu và công việc còn lại; chưa xác nhận hoàn tất G2/G3 hoặc nghiệm thu ứng dụng. Snapshot campaign local được đọc ở mốc 10:17 (UTC+8), không phải trạng thái tiến trình trực tiếp.

# I. MỞ ĐẦU

## 1. Lý do chọn đề tài

Lượng protein trong tế bào chịu ảnh hưởng của cả quá trình tổng hợp và phân hủy. Trong hệ ubiquitin–proteasome, degron là tín hiệu liên quan đến việc nhận diện protein để phân hủy. Một thay đổi amino acid tại degron có thể làm thay đổi hoạt tính tín hiệu này. Vì vậy, xác định ảnh hưởng của từng phép thay thế có ý nghĩa đối với việc lựa chọn đột biến để kiểm chứng chức năng protein [1, 2].

Điểm hoạt tính của cả đoạn peptide chưa trực tiếp trả lời câu hỏi: thay amino acid nào, tại vị trí nào, sẽ làm tín hiệu degron mạnh lên hay yếu đi? Đo toàn bộ các phép thay thế bằng thực nghiệm cần nhiều nguồn lực. Mô hình dự đoán có thể hỗ trợ thu hẹp danh sách đột biến ưu tiên, với điều kiện được đánh giá trên nhãn phù hợp và kiểm soát sự tương đồng giữa dữ liệu huấn luyện và kiểm tra.

Zhang và cộng sự cung cấp dữ liệu đột biến quét và bão hòa làm cơ sở xây dựng nhãn thực nghiệm [1]. PAP và Degformer cung cấp các phương pháp đối chứng; trong đó Degformer đã hỗ trợ mô phỏng đột biến và xuất ma trận vị trí × amino acid [2, 3]. Do đó, đóng góp cần được kiểm chứng bằng hiệu quả dự đoán, độ ổn định và thiết kế đánh giá, thay vì chỉ dựa vào việc tạo ma trận hoặc xây dựng giao diện mới.

Các thí nghiệm đã cho thấy ridge vượt đối chứng chênh lệch điểm PAP; mở rộng miền nhãn và ngữ cảnh có thứ tự mang lại cải thiện ở những thiết kế được kiểm [8, 11, 17]. Nghiên cứu full-PSI mới bổ sung bằng chứng về train toàn dải và ESM đóng băng kết hợp CNN; đối chứng pointwise giúp kiểm tra phần đóng góp của trộn vị trí [18]. Tiền huấn luyện bằng nhãn mức tile chưa đem lại lợi ích trong thiết kế đã thử [12]. Đóng góp hiện tập trung vào dữ liệu, đánh giá có đối chứng và công cụ phân tích; chưa xác lập kiến trúc mới hoặc kiểm chứng ngoài độc lập.

## 2. Mục tiêu nghiên cứu

**Mục tiêu chung:** Nghiên cứu phương pháp dự đoán hiệu ứng của các phép thay thế amino acid trong degron từ dữ liệu thực nghiệm, đánh giá khả năng tổng quát hóa theo cụm protein và xây dựng công cụ hỗ trợ phân tích, ưu tiên đột biến.

**Mục tiêu cụ thể:**

- Xây dựng pipeline chuẩn hóa dữ liệu, ánh xạ tọa độ và tạo nhãn hiệu ứng đột biến có thể tái lập; giữ riêng các nguồn và điều kiện đo.
- Thiết lập các đối chứng thành phần amino acid, ridge, chênh lệch điểm PAP và kiến trúc Degformer trong những điều kiện so sánh được công bố rõ.
- Đánh giá vai trò của phạm vi PSI, ngữ cảnh có thứ tự và biểu diễn protein pretrained; so các đầu pointwise/CNN tương ứng, học chuyển tiếp và frozen–LoRA theo protocol, không mặc định mô hình phức tạp hơn sẽ tốt hơn.
- Đánh giá hiệu quả, độ ổn định qua nhiều seed, sai số và đóng góp từng thành phần bằng thí nghiệm loại bỏ thành phần.
- Xây dựng một ứng dụng local React/TypeScript và FastAPI: peptide đơn, lô peptide và chia cửa sổ toàn protein; chú giải ClinVar/nguồn tham chiếu; nhập dữ liệu đo để đối chiếu; lưu dự án/lịch sử và xuất kết quả có nguồn gốc.

## 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng:** Các peptide degron, phép thay thế đơn amino acid, chỉ số ổn định protein trong phép đo reporter và mô hình dự đoán hiệu ứng đột biến ở mức residue. Residue là một amino acid tại một vị trí cụ thể của chuỗi protein; footprint trong đề tài là bản đồ các vị trí hoặc phép thay thế ảnh hưởng đến hoạt tính degron theo hệ đo.

**Phạm vi:**

- Nguồn nhãn chính là dữ liệu peptide người của Zhang 2023. Benchmark lịch sử có 91 peptide, 89 cụm và 47.847 ô (PSI(WT) ≤ 3); mở rộng train tới PSI(WT) ≤ 4 dùng pool 176 peptide nhưng giữ outer-test lịch sử [8, 11]. Luồng full-PSI hiện hành bỏ lọc ngưỡng PSI sau QC kỹ thuật: 235 peptide, 122.412 ô saturation và 221 nhóm protein; bundle scanning hỗ trợ có 224.470 ô [18]. Đây là hai population/thiết kế đánh giá riêng, không ghép điểm thành một đường tiến bộ hoặc coi phần mở rộng là tập xác nhận độc lập.
- Đầu vào chính là trình tự tham chiếu (WT), vị trí và amino acid thay thế. Đầu ra là hiệu ứng dự đoán ΔPSI; có thể tổng hợp thành ma trận L × 20, với L là độ dài peptide thuộc miền mô hình hỗ trợ.
- Dữ liệu mức peptide của Voutsinos được xem xét cho học chuyển tiếp. Larsen chỉ phục vụ khảo sát chuyển miền ở mức tile khi điều kiện sử dụng được xác nhận; không được thay cho nhãn đột biến thực nghiệm [2, 4].
- Koren 2018 (Table S4, saturation mutagenesis đầu C, cùng đại lượng PSI nhưng thư viện 23-mer và 3 bin) đã được audit: chỉ 5 cụm cov80 mới, thấp hơn ngưỡng 20 đã chốt, nên chỉ làm tập kiểm chứng ngoài cho lớp degron đầu C, không nhập vào huấn luyện. Nguồn không có giấy phép mở, chỉ dùng nội bộ [15].
- Không đặt nhận diện E3 cụ thể làm nhiệm vụ chính. Chưa thực hiện thí nghiệm sinh học mới; kết quả phần mềm hỗ trợ hình thành giả thuyết, không suy ra quan hệ nhân quả gây bệnh hoặc hiệu quả điều trị.
- Một ứng dụng local duy nhất, không yêu cầu hosting công khai, tài khoản hay VPS. Mỗi dự đoán vẫn thuộc cửa sổ 28 residue; xử lý toàn protein không chứng minh hiệu ứng trên protein nguyên vẹn. Dữ liệu nhập chỉ phục vụ dự án/đối chiếu, không tự trở thành nhãn train; lịch sử đã lưu tồn tại đến khi người dùng xóa.

# II. CƠ SỞ LÝ THUYẾT

## 1. Degron và hệ ubiquitin–proteasome

- **Khái niệm và vai trò:** protein, amino acid, residue, degron, enzyme E3 ligase, ubiquitin và proteasome; quan hệ giữa tín hiệu degron và sự phân hủy có chọn lọc.
- **Bối cảnh sinh học:** hoạt tính của peptide tách rời có thể khác hoạt tính khi đoạn đó nằm trong protein nguyên vẹn; độ lộ bề mặt, cấu trúc và môi trường tế bào là những yếu tố cần cân nhắc.
- **Tài liệu tham khảo:** Zhang và cộng sự [1]; Voutsinos và cộng sự [2]; Larsen và cộng sự [4].

## 2. Đo hoạt tính degron và hiệu ứng đột biến

- **GPS và PSI:** Global Protein Stability profiling dùng reporter và phân loại tế bào theo tín hiệu huỳnh quang. Protein Stability Index (PSI) tóm tắt phân bố tín hiệu qua các bin. Trong dữ liệu Zhang, PSI thấp hơn tương ứng reporter kém bền hơn.
- **Định nghĩa hiệu ứng:** ΔPSI = PSI(mutant) − PSI(WT). Giá trị dương biểu thị reporter bền hơn theo phép đo; không tự chứng minh cơ chế nhận diện trực tiếp của E3.
- **Thiết kế đột biến:** scanning khảo sát phép thay thế quét tại các vị trí; saturation khảo sát nhiều amino acid thay thế tại từng vị trí. Các ô cùng peptide có liên hệ thống kê, không được coi là những mẫu độc lập hoàn toàn.
- **Nguồn nhiễu:** số đọc, khác biệt replicate và điều kiện đo. Pipeline phải mô tả cách tạo mốc WT, gộp replicate và xử lý giá trị thiếu. Mốc WT của bộ bão hòa lấy từ các ô đồng nghĩa trong cùng hệ đo; không lấy điều kiện BAG6 WT thay thế [8].
- **Tài liệu tham khảo:** Zhang và cộng sự [1], bộ dữ liệu Mendeley phiên bản 2 [6].

## 3. Học máy cho dự đoán hiệu ứng đột biến

- **Biểu diễn:** mã hóa amino acid tham chiếu và thay thế, thành phần peptide, ngữ cảnh có thứ tự và biểu diễn ESM2 pretrained [20]. Đóng băng backbone, train đầu dự đoán và thích nghi tham số LoRA là các chế độ khác nhau; LoRA học cập nhật hạng thấp cùng đầu tác vụ [21].
- **Mô hình:** hồi quy ridge làm đối chứng đơn giản; PAP dự đoán điểm cả peptide, từ đó tính ΔPAP = PAP(mutant) − PAP(WT); Degformer dùng transformer dự đoán PSI [2, 3]. Chiều điểm khi đánh giá phải thống nhất với nhãn đích.
- **Học chuyển tiếp:** tiền huấn luyện biểu diễn trên nhãn hoạt tính mức peptide rồi tinh chỉnh cho ΔPSI. Nhãn hai mức có ý nghĩa khác nhau nên cần đầu dự đoán hoặc phép biến đổi phù hợp; không đổi nhãn nhị phân motif thành ΔPSI.
- **Công cụ dự kiến:** Python, NumPy, pandas, scikit-learn, PyTorch và MMseqs2; chỉ chọn cấu hình đủ nguồn lực và ghi phiên bản khi thực nghiệm.
- **Tài liệu tham khảo:** PAP [2], Degformer [3], MetaDegron [5] để đối chiếu phạm vi dự đoán.

## 4. Đánh giá và khả năng tái lập

- Chia dữ liệu theo cụm protein tương đồng thay vì chia ngẫu nhiên từng ô. Quy ước cov80 hiện dùng là phân cụm MMseqs2 với ngưỡng đồng nhất 30% và độ phủ 80%; kiểm độ nhạy bằng độ phủ 50% khi phù hợp.
- Dùng tập validation theo cụm bên trong mỗi fold huấn luyện để chọn siêu tham số; mọi chuẩn hóa, chọn đặc trưng và tiền huấn luyện đều phải loại cụm kiểm tra ngoài.
- Benchmark lịch sử dùng AUROC mức ô macro theo peptide. Full-PSI dùng MAE macro theo peptide làm chỉ số chính; báo thêm Spearman và AUROC/AP cho ΔPSI ≥ 1 hoặc ΔPSI ≤ −1. AUROC/AP full-PSI cần ít nhất 3 ô mỗi lớp; phải ghi số peptide đủ điều kiện, không loại peptide khỏi hồi quy chỉ vì thiếu hai lớp.
- So sánh ghép cặp trên cùng peptide; bootstrap theo cụm protein để ước lượng khoảng tin cậy. Báo kết quả từng seed bên cạnh kết quả tổng hợp và phân biệt benchmark phát triển với kiểm chứng độc lập.

# III. PHƯƠNG PHÁP NGHIÊN CỨU

## 1. Phương pháp tiếp cận

Đề tài kết hợp khảo sát tài liệu, thực nghiệm có đối chứng và phát triển phần mềm. Các câu hỏi hiện hành là: (i) phạm vi nhãn PSI ảnh hưởng thế nào tới hồi quy và xếp hạng đột biến; (ii) ngữ cảnh có thứ tự và ESM kết hợp đầu trộn vị trí đóng góp gì so với đối chứng tương ứng; (iii) nguồn nhãn scanning và LoRA có tạo lợi ích so với học trực tiếp/frozen trong cùng điều kiện; (iv) đưa mô hình đã đánh giá vào công cụ local có nguồn gốc và miền áp dụng rõ ràng như thế nào?

Trước hết, khảo sát đường cong học theo số cụm huấn luyện để kiểm tra giả thuyết thiếu nhãn (đã thực hiện, kết quả bên dưới). Sau đó, so cùng một bộ mã hóa ở hai chế độ khởi tạo ngẫu nhiên và tiền huấn luyện, dùng chung fold, ngân sách nhãn đột biến và quy trình chọn siêu tham số (đã thực hiện một thiết kế, kết quả âm). Các nhánh mô hình còn lại là phương án dự kiến, được giữ lại theo bằng chứng; đề cương không mặc định một kiến trúc mới sẽ thắng đối chứng.

Các thực nghiệm dùng 5 outer fold theo nhóm protein, validation bên trong, seed 17/29/43 và 5.000 lần bootstrap theo nhóm. Full-PSI hợp nhóm từ cụm toàn proteome cov80, hits cov50 hai chiều và hợp trình tự trùng; đây vẫn là kiểm soát homology bằng heuristic. Scanning được chia development/nguồn giữ lại/nhóm chồng saturation trước fitting. Scaler/PCA và siêu tham số chỉ khớp trên phần train hợp lệ. Cấu hình hạn chế PSI vẫn dùng inner validation toàn dải, nên không hoàn toàn chưa thấy nhãn PSI cao trong lựa chọn mô hình [18].

Bằng chứng phát triển hiện có ghi nhận AUROC macro 0,8082 của ridge và 0,7693 của ΔPAP trên cùng bộ bão hòa [8]. Kết quả này chưa chứng minh tính mới kiến trúc. Các thử nghiệm tương tác và huấn luyện lại kiến trúc Degformer với ngân sách nhãn nhỏ cũng chưa cho lợi ích so với ridge [9]. Dữ liệu này định hướng giả thuyết tiếp theo, không thay thế một phép kiểm chứng xác nhận cuối cùng.

Các khảo sát ngày 22/10/2026 bổ sung năm kết quả, tất cả trên benchmark phát triển theo cụm (OOF), không phải kiểm chứng ngoài độc lập; nguồn số liệu ở mục [11–15]:

- **Đường cong học.** Với ridge, AUROC theo 25/50/75/100% số cụm huấn luyện là 0,7776 / 0,8044 / 0,8088 / 0,8082; chênh lệch 100% − 50% là +0,0038 với khoảng tin cậy 95% theo cụm [−0,0009; +0,0087], tức chưa đủ bằng chứng cho giả thuyết thiếu nhãn. Với mạng `gate_no_pap`, chênh lệch tương ứng là +0,0156 [+0,0060; +0,0256] và đường cong vẫn đi lên. Khoảng cách ridge − mạng thu hẹp nhưng chưa đảo chiều, nên kết quả này không phục hồi ứng viên kiến trúc nào đã bị loại [11].
- **Nới ngưỡng degron.** Thêm 85 peptide có PSI(WT) trong khoảng 3,0–4,0 vào phần huấn luyện, giữ nguyên outer-test, đưa AUROC của ridge từ 0,8082 lên 0,8208 (+0,0126; khoảng tin cậy [+0,0061; +0,0190]; dương ở cả ba seed). Lợi ích còn dương khi đổi ngưỡng sự kiện và phân hoạch protein [11, 13]. Điểm ước lượng đạt đỉnh quanh ngưỡng 4,0, nhưng các khoảng tin cậy chồng nhau; chưa chứng minh ngưỡng này hơn mọi ngưỡng khác. Kết luận thuộc benchmark lịch sử, không thay cho đánh giá full-PSI.
- **Diễn giải thận trọng.** Phần tách riêng (thêm một nửa số cụm mới so với mốc cụm vùng cũ) ủng hộ cách đọc "độ phủ phân bố" ở ridge nhưng không dứt khoát ở mạng, và tiêu chí hình dạng chốt trước không đạt; kết luận là chưa phân định, không được viết thành "lợi ích hoàn toàn do mở rộng phân bố". Chưa tách được "vùng PSI(WT) khác" khỏi "protein khác" [11].
- **Tiền huấn luyện nhãn mức tile (Voutsinos).** Tiền huấn luyện encoder trên 212.616 tile rồi tinh chỉnh ΔPSI cho AUROC 0,8098, thấp hơn khởi tạo ngẫu nhiên (0,8175; hiệu −0,0077, khoảng tin cậy [−0,0163; +0,0006]) và thấp hơn ridge (0,8208; hiệu −0,0110, khoảng tin cậy [−0,0197; −0,0024]). Kết quả âm này chỉ bác thiết kế "tiền huấn luyện trên nhãn mức peptide rồi tinh chỉnh toàn bộ" đã thử, không suy ra cho thiết kế khác [12].
- **Hiệu chuẩn.** Điểm thô của ridge kém hơn việc dùng tần suất nền (Brier 0,1272 so với 0,1139). Hiệu chuẩn Platt trong inner-train đưa Brier xuống 0,0925 (hiệu +0,0346; khoảng tin cậy [+0,0266; +0,0425]; dương ở cả ba seed), và top 10% phép thay thế mỗi peptide làm giàu ô dương 4,02 lần so với ngẫu nhiên. Xác suất sau hiệu chuẩn vẫn thiên thấp trên miền gốc (trung bình 0,115 so với 0,131 quan sát) [14].

**Kết quả tiếp nối quan trọng đến 03/11/2026.** R0 tái lập các mốc; Degformer sạch cụm R1 đã hoàn tất 3 seed × 5 fold, AUROC 0,8068 so với ridge 0,8208; vì vậy không còn ghi đối chứng này là chưa chạy [16]. R6 cho ridge ngữ cảnh ±5 đạt 0,8286 với CI điều chỉnh của mức tăng so ±3 là [+0,0021; +0,0139]. ESM2-35M+mCNN đạt 0,8305 nhưng phép xác nhận chính so ridge có CI chứa 0; chưa đủ cơ sở thay mô hình sản phẩm [17].

**Full-PSI trên Kaggle.** Cùng outer-test toàn dải, W5 train PSI≤4 đạt MAE 0,43358; train toàn dải đạt 0,40780 (giảm 5,94%), với CI điều chỉnh của chênh lệch [−0,03381; −0,01829]. ESM2-35M đóng băng + CNN đạt MAE 0,38435 so với 0,38969 của đầu pointwise tương ứng; CI95 mô tả của chênh lệch [−0,01017; −0,00090]. mCNN cân bằng strata đạt 0,38385 nhưng chỉ hơn CNN toàn dải khoảng 0,00051 PSI, chưa xác lập kiến trúc thắng. MAE dùng đủ 235 peptide; AUROC dương chỉ có 184 peptide đủ điều kiện. Tiền huấn luyện scanning cải thiện CNN one-hot từ 0,39361 xuống 0,38723; quality weighting làm ridge kém hơn. Đây là OOF development, protocol mở rộng sau khi biết kết quả cũ, không phải xác nhận độc lập [18].

**Campaign local và ranh giới kết luận.** Kế hoạch gồm 9 pLM; snapshot ghi 455/635 đơn vị công việc hoàn tất, trong đó 7 pLM xong 420 Ridge fold; ProtT5 và Ankh bị chặn ở tokenizer. Frozen ESM2-35M xong 10 fold của seed17 (hai arm); LoRA mới xong 1 fold, fold kế tiếp được ghi đang chạy. Status lưu không xác nhận worker hiện còn sống; chưa có tổng hợp OOF local, so LoRA–frozen đủ seed/fold, calibration hoặc locked-transfer hoàn tất. Runtime Windows khác Kaggle, nên không gộp hai output thành mẫu độc lập. Recipe W5 toàn dải đã chốt cho nguồn giữ lại; không dùng tập này chọn mọi pLM mới. Nguồn ngoài/cấu trúc vẫn thiếu đầu vào [19].

Đối với ứng viên mới, dấu chênh lệch phải đọc đúng chiều metric và vai trò phép so: MAE âm là tốt hơn, AUROC dương là tốt hơn. Hai phép so phạm vi PSI có hiệu chỉnh; các CI tiếp nối khác chỉ mô tả. Chưa tự đóng G2/G3 hoặc đổi serving model. CNN/LoRA/family cần final refit, hiệu chuẩn, miền áp dụng và export tương ứng trước khi phục vụ; calibration baseline cũ không tự chuyển sang model mới.

## 2. Quy trình thực hiện

| STT | Nội dung | Kết quả |
|:---:|:---|:---|
| 1 | Nghiên cứu sinh học degron, khảo sát PAP, Degformer, MetaDegron và nguồn nhãn | Tổng quan tài liệu; bảng so sánh bài toán, dữ liệu và giới hạn |
| 2 | Kiểm dữ liệu, tái tính PSI, ánh xạ tọa độ, phân cụm và thiết kế đánh giá | Bảng nhãn; sổ nguồn gốc; danh sách fold; protocol và đối chứng |
| 3 | Đo đường cong học; thiết kế, huấn luyện mô hình và ablation; xây dựng phần mềm | Runner tái lập; mô hình ứng viên; API, giao diện và chức năng xuất kết quả |
| 4 | Kiểm thử phần mềm và kiểm chéo thực nghiệm | Ca kiểm thử; đối chiếu điểm giao diện với runner; báo cáo rò rỉ, lỗi và kết quả từng seed |
| 5 | Đánh giá, phân tích sai số, viết báo cáo và hoàn thiện luận văn | Bảng so sánh có khoảng tin cậy; báo cáo đóng góp, giới hạn; mã nguồn và hướng dẫn |

**Tiến độ đến 03/11/2026.** Đã có pipeline dữ liệu, thí nghiệm lịch sử, kết quả Kaggle full-PSI và baseline React/FastAPI với ETL, suy luận và kiểm thử được ghi trước đây. Workspace UI mới là prototype tương tác bằng fixture tổng hợp và bộ nhớ tab, chưa nối backend. Luận văn cập nhật có chọn lọc kết quả quan trọng, đóng góp, giới hạn và công việc còn lại; đây chưa phải bản nghiệm thu cuối [16–19].

**Việc còn lại theo ưu tiên.** (a) Hoàn tất campaign và tổng hợp OOF, so paired frozen–LoRA và các ứng viên đủ điều kiện; (b) hiệu chuẩn, final refit/export và đánh giá recipe đã khóa trên nguồn giữ lại; (c) tích hợp đúng cổng R3 cho baseline, hoặc xác định miền mới nếu chọn model full-PSI; (d) triển khai/kiểm chứng lưu dự án, job peptide/protein, import/comparison và PostgreSQL local; (e) hoàn thiện nghiệm thu, hướng dẫn và các phần luận văn còn chờ. Nguồn ngoài mới chỉ khảo sát tiếp sau kiểm endpoint, homology và quyền sử dụng; không coi số benchmark hiện tại là external validation.

Tiến độ theo tuần và mốc nộp sẽ bổ sung sau khi có lịch học phần và thống nhất phạm vi với giảng viên hướng dẫn.

# IV. ỨNG DỤNG THỰC TẾ VÀ NGUỒN DỮ LIỆU

## 1. Ứng dụng thực tế

- Hỗ trợ người nghiên cứu lựa chọn vị trí và amino acid thay thế để làm thí nghiệm tiếp theo, kèm đột biến đối chứng.
- Trực quan hóa ma trận hiệu ứng, đối chiếu dự đoán với ô thực nghiệm đã có và truy xuất nguồn dữ liệu, phiên bản mô hình.
- Hỗ trợ giảng dạy và khảo sát mối liên hệ giữa trình tự peptide và tín hiệu phân hủy. Kết quả chỉ có ý nghĩa trong phạm vi hệ đo và miền dữ liệu được mô tả.

Luồng baseline đã có: nhập peptide hợp lệ hoặc chọn tile tham chiếu → sinh phép thay thế → tính điểm bằng mô hình cố định → hiển thị ma trận/xếp hạng → xuất CSV/JSON. Bản local đầu tiên còn yêu cầu jobs peptide/protein, chú giải ClinVar, nhập dữ liệu đo để đối chiếu và lưu dự án/lịch sử. Các luồng mở rộng chưa nghiệm thu; prototype mới không thay bằng chứng thực thi. Thiếu dữ liệu, sai tọa độ và miền unknown/borderline phải hiện rõ; không chuyển điểm thành xác suất bệnh [19].

## 2. Nguồn dữ liệu thử nghiệm

| Nguồn dữ liệu | Mô tả và vai trò | Link |
|:---|:---|:---|
| Zhang 2023 — Mendeley Data v2 | Nhãn chính: count/GPS, đột biến quét và bão hòa; dữ liệu CC BY 4.0 | [Mendeley v2](https://data.mendeley.com/datasets/32h94v2yv2/2) |
| Zhang — GEO GSE240610 | Đối chiếu nguồn peptidome; các bảng dự đoán sẵn không thay thế nhãn đo | [GSE240610](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610) |
| Voutsinos/PAP | Tile bào tương và mô hình PAP; đối chứng và nguồn nhãn mức peptide cho học chuyển tiếp | [Kho tác giả](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol) |
| Larsen — transcription factors | Tile trong bối cảnh nhân; khảo sát chuyển miền ở mức tile nếu quyền sử dụng được chốt | [Kho tác giả](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors) |
| Koren 2018 — Table S4 | Saturation mutagenesis đầu C, cùng đại lượng PSI nhưng thư viện 23-mer, 3 bin; chỉ kiểm chứng ngoài cho lớp degron đầu C, không nhập huấn luyện; nguồn không có giấy phép mở, chỉ dùng nội bộ | [DOI](https://doi.org/10.1016/j.cell.2018.04.028) |
| UniProtKB/Swiss-Prot | Trình tự, accession và tọa độ phục vụ ánh xạ và phân cụm protein | [UniProt](https://www.uniprot.org/) |
| MaveDB và ClinVar, bổ trợ | Khảo sát ca nghiên cứu nếu endpoint phù hợp; không gộp điểm abundance hay nhãn bệnh vào ΔPSI | [MaveDB](https://www.mavedb.org/); [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) |

Mỗi nguồn được ghim phiên bản hoặc ngày tải, checksum và điều kiện sử dụng. Nhãn khác assay được giữ riêng. MetaDegron chỉ dùng khảo sát/truy nguồn trong phạm vi hiện tại; việc nhập nhãn vào huấn luyện hoặc công khai còn phụ thuộc quyền sử dụng và thẩm định nguồn [10].

# V. CÁC DỰ ÁN LIÊN QUAN

| Dự án | Mô tả và quan hệ với đề tài | Link |
|:---|:---|:---|
| PAP | Dự đoán hoạt tính cả peptide; chênh điểm mutant–WT tạo đối chứng ΔPAP | [PAP và dữ liệu](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol) |
| Degformer | Transformer dự đoán PSI; đã hỗ trợ đột biến quét/bão hòa và ma trận 28 × 20; đối chứng gần nhất cần kiểm soát overlap | [Degformer](https://github.com/Alpine2048/Degformer) |
| MetaDegron | Dự đoán degron ở mức motif/đoạn; dùng so sánh phạm vi chức năng, loại nhãn và nguồn gốc dữ liệu | [Bài báo](https://doi.org/10.1093/bib/bbae519) |
| DEGRONOPEDIA | Công cụ phân tích degron; đối chiếu chức năng tra cứu và cách trình bày kết quả | [Tài liệu](https://degronopedia.com/degronopedia/documentation) |
| DegronMD | Tài nguyên degron và biến thể; đối chiếu thông tin chú giải, không mặc định dữ liệu dự đoán là nhãn thật | [Bài báo](https://doi.org/10.1093/molbev/msad253) |

Ma trận thay thế, xử lý theo lô hoặc giao diện web không được dùng riêng để khẳng định tính mới. Điểm khác biệt dự kiến nằm ở bằng chứng đánh giá theo cụm, kiểm soát nguồn nhãn và quy trình hỗ trợ ưu tiên đột biến có thể tái tính.

# VI. DỰ KIẾN KẾT QUẢ VÀ ĐÓNG GÓP

- **Dữ liệu và đánh giá:** pipeline tạo nhãn có nguồn gốc rõ ràng, bộ chia theo cụm và runner tái lập; báo cáo riêng độ chồng lặp, điều kiện assay và hạn chế của các đối chứng.
- **Kết quả nghiên cứu đã có:** bằng chứng về mở rộng miền nhãn, ngữ cảnh có thứ tự và ESM/CNN với đối chứng pointwise; giữ riêng kết quả âm của tile-label pre-training, weighting và các phép so chưa phân giải. Full-PSI giảm MAE W5 từ 0,43358 xuống 0,40780; ESM2-35M+CNN đạt 0,38435. Đóng góp thuộc benchmark/phương pháp đánh giá; chưa xác lập kiến trúc mới hoặc kiểm chứng ngoài [11–18].
- **Sản phẩm phần mềm đã có và còn thiếu:** baseline CLI và React/FastAPI dùng ridge/Platt, có ma trận/xếp hạng, chú giải, export và kiểm thử lịch sử; đường suy luận đã đối chiếu runner. Workspace mới dùng fixture tổng hợp. Lưu dự án/lịch sử, jobs peptide/protein, import/comparison, PostgreSQL và tích hợp R3 còn cần triển khai/kiểm chứng; chưa đổi serving model hoặc nghiệm thu bản đầu [14, 19].
- **Kiểm thử và tài liệu:** bộ ca kiểm thử đầu vào, tọa độ, chiều điểm và xuất dữ liệu; kết quả giao diện khớp runner trong sai số số học; tài liệu cài đặt, sử dụng và tái lập.
- **Luận văn:** tổng quan, thiết kế phương pháp, kết quả định lượng, phân tích sai số, giới hạn và hướng phát triển. Khả năng vượt đối chứng và tính mới kiến trúc là mục tiêu cần kiểm chứng, chưa phải kết quả đã đạt.

# VII. TÀI LIỆU THAM KHẢO

Quản lý tài liệu bằng **Zotero hoặc Mendeley** theo yêu cầu của mẫu. Danh mục dưới đây là danh mục khởi đầu; các báo cáo nội bộ [8–19] là hồ sơ tính toán chưa xuất bản, không thay thế công trình khoa học đã công bố. Truy vết tệp và hash giữ trong hồ sơ build, không in đường dẫn nội bộ làm dẫn chứng.

1. Zhang, Z. và cộng sự (2023). *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*. Molecular Cell, 83, 3377–3392.e6. DOI: <https://doi.org/10.1016/j.molcel.2023.08.022>.
2. Voutsinos, V. và cộng sự (2026). *A near-complete map of human cytosolic degrons and their relevance for disease*. Science Advances. DOI: <https://doi.org/10.1126/sciadv.adz3483>.
3. Alpine2048. *Degformer: Transformer model for internal and C-terminal degron prediction*. Mã nguồn, commit 49ee52459967. [GitHub](https://github.com/Alpine2048/Degformer/tree/49ee524599671f2b5e30d9cd052ce6baa55c06d8).
4. Larsen, F. B. và cộng sự (2025). *Comprehensive degron mapping in human transcription factors*. bioRxiv, bản tiền ấn phẩm. DOI: <https://doi.org/10.1101/2025.05.16.654404>.
5. Zheng, M. và cộng sự (2024). *MetaDegron: multimodal feature-integrated protein language model for predicting E3 ligase targeted degrons*. Briefings in Bioinformatics, 25(6), bbae519. DOI: <https://doi.org/10.1093/bib/bbae519>.
6. Zhang và cộng sự (2023). Bộ dữ liệu đi kèm nghiên cứu degron, *Mendeley Data*, phiên bản 2. DOI: <https://doi.org/10.17632/32h94v2yv2.2>.
7. NCBI. *GEO Series GSE240610*. [Trang dữ liệu](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610).
8. Nguyễn Thanh Trọng (18/10/2026). *G2 — học trực tiếp trên ma trận bão hòa*. Báo cáo thực nghiệm nội bộ, chưa xuất bản; đánh giá phát triển theo cụm protein.
9. Nguyễn Thanh Trọng (18/10/2026). *G2 — mở rộng: ba câu hỏi còn mở của báo cáo bão hòa*. Báo cáo thực nghiệm nội bộ, chưa xuất bản.
10. Nguyễn Thanh Trọng (21/10/2026). *Phân tích MetaDegron và đối chiếu đề tài hiện tại*. Audit nội bộ, chưa xuất bản.
11. Nguyễn Thanh Trọng (22/10/2026). *Đường cong học theo cụm và mở rộng phạm vi nhãn PSI*. Báo cáo thực nghiệm nội bộ, chưa xuất bản; benchmark phát triển OOF.
12. Nguyễn Thanh Trọng (22/10/2026). *Tiền huấn luyện nhãn mức tile rồi tinh chỉnh ΔPSI*. Báo cáo thực nghiệm nội bộ, chưa xuất bản; kết quả âm.
13. Nguyễn Thanh Trọng (22/10/2026). *Độ nhạy theo độ mịn phân cụm của lợi ích mở rộng nhãn*. Báo cáo thực nghiệm nội bộ, chưa xuất bản.
14. Nguyễn Thanh Trọng (22/10/2026). *Hiệu chuẩn điểm và nguyên mẫu dòng lệnh*. Báo cáo tính toán nội bộ, chưa xuất bản.
15. Nguyễn Thanh Trọng (22/10/2026). *Audit Koren 2018 Table S4*. Audit nội bộ, chưa xuất bản; nguồn gốc: Koren, I. và cộng sự (2018), Cell 173(7), 1622–1635.e14, DOI: <https://doi.org/10.1016/j.cell.2018.04.028>.
16. Nguyễn Thanh Trọng (22–23/10/2026). *Tái lập notebook, Degformer sạch cụm, ESM và cổng miền sử dụng*. Hồ sơ tính toán Kaggle nội bộ, chưa xuất bản.
17. Nguyễn Thanh Trọng (23/10/2026). *Đối chứng biểu diễn, đầu mạng, ngữ cảnh rộng và scanning*. Báo cáo thực nghiệm Kaggle nội bộ, chưa xuất bản.
18. Nguyễn Thanh Trọng (02/11/2026). *Phân tích kết quả full-PSI: phạm vi nhãn, ESM/CNN và học chuyển tiếp*. Báo cáo phát triển nội bộ, chưa xuất bản; output Kaggle cập nhật đến 01/11/2026.
19. Nguyễn Thanh Trọng (03/11/2026). *Snapshot campaign local và trạng thái tích hợp phần mềm*. Hồ sơ tiến độ nội bộ, chưa xuất bản; snapshot local 10:17 (UTC+8), không phải xác nhận worker trực tiếp.
20. Lin, Z. và cộng sự (2023). *Evolutionary-scale prediction of atomic-level protein structure with a language model*. Science, 379(6637), 1123–1130. DOI: <https://doi.org/10.1126/science.ade2574>.
21. Hu, E. J. và cộng sự (2022). *LoRA: Low-Rank Adaptation of Large Language Models*. International Conference on Learning Representations. [Bài báo](https://openreview.net/forum?id=nZeVKeeFYf9).
