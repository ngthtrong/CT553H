---
title: ĐỀ CƯƠNG LUẬN VĂN
subtitle: |
  DỰ ĐOÁN HIỆU ỨNG ĐỘT BIẾN DEGRON Ở MỨC RESIDUE
  VÀ XÂY DỰNG CÔNG CỤ HỖ TRỢ PHÂN TÍCH
lang: vi-VN
---

**Sinh viên thực hiện:** Nguyễn Thanh Trọng — MSSV: B2305615  
**Giáo viên hướng dẫn 1:** TS. Hồ Quang Thái — MSCB: [Bổ sung]  

# I. MỞ ĐẦU

## 1. Lý do chọn đề tài

Lượng protein trong tế bào chịu ảnh hưởng của cả quá trình tổng hợp và phân hủy. Trong hệ ubiquitin–proteasome, degron là tín hiệu liên quan đến việc nhận diện protein để phân hủy. Một thay đổi amino acid tại degron có thể làm thay đổi hoạt tính tín hiệu này. Vì vậy, xác định ảnh hưởng của từng phép thay thế có ý nghĩa đối với việc lựa chọn đột biến để kiểm chứng chức năng protein [1, 2].

Điểm hoạt tính của cả đoạn peptide chưa trực tiếp trả lời câu hỏi: thay amino acid nào, tại vị trí nào, sẽ làm tín hiệu degron mạnh lên hay yếu đi? Đo toàn bộ các phép thay thế bằng thực nghiệm cần nhiều nguồn lực. Mô hình dự đoán có thể hỗ trợ thu hẹp danh sách đột biến ưu tiên, với điều kiện được đánh giá trên nhãn phù hợp và kiểm soát sự tương đồng giữa dữ liệu huấn luyện và kiểm tra.

Zhang và cộng sự cung cấp dữ liệu đột biến quét và bão hòa làm cơ sở xây dựng nhãn thực nghiệm [1]. PAP và Degformer cung cấp các phương pháp đối chứng; trong đó Degformer đã hỗ trợ mô phỏng đột biến và xuất ma trận vị trí × amino acid [2, 3]. Do đó, đóng góp cần được kiểm chứng bằng hiệu quả dự đoán, độ ổn định và thiết kế đánh giá, thay vì chỉ dựa vào việc tạo ma trận hoặc xây dựng giao diện mới.

Khảo sát thực nghiệm nội bộ bước đầu cho thấy mô hình ridge có thể vượt đối chứng chênh lệch điểm PAP trên bộ bão hòa, nhưng chưa xác lập được lợi ích ổn định của các thành phần kiến trúc phức tạp hơn [8]. Các khảo sát tiếp theo (22/10/2026) cho thấy phân bố của nhãn huấn luyện, chứ không riêng số lượng nhãn, là yếu tố đáng chú ý hơn, và tiền huấn luyện trên nhãn mức peptide theo thiết kế đã thử chưa đem lại lợi ích [11, 12]. Đề tài tiếp tục nghiên cứu vai trò của nguồn nhãn, biểu diễn trình tự và học chuyển tiếp; đồng thời xây dựng công cụ giúp truy xuất kết quả cùng nguồn gốc và giới hạn áp dụng.

## 2. Mục tiêu nghiên cứu

**Mục tiêu chung:** Nghiên cứu phương pháp dự đoán hiệu ứng của các phép thay thế amino acid trong degron từ dữ liệu thực nghiệm, đánh giá khả năng tổng quát hóa theo cụm protein và xây dựng công cụ hỗ trợ phân tích, ưu tiên đột biến.

**Mục tiêu cụ thể:**

- Xây dựng pipeline chuẩn hóa dữ liệu, ánh xạ tọa độ và tạo nhãn hiệu ứng đột biến có thể tái lập; giữ riêng các nguồn và điều kiện đo.
- Thiết lập các đối chứng thành phần amino acid, ridge, chênh lệch điểm PAP và kiến trúc Degformer trong những điều kiện so sánh được công bố rõ.
- Kiểm tra giả thuyết học biểu diễn từ nhãn mức peptide rồi tinh chỉnh trên nhãn đột biến có cải thiện dự đoán so với học trực tiếp hay không (một thiết kế đã thử, chưa có lợi ích; xem III.1); khảo sát đường cong học và vai trò của phân bố nhãn huấn luyện trước khi lựa chọn mô hình (đã thực hiện).
- Đánh giá hiệu quả, độ ổn định qua nhiều seed, sai số và đóng góp từng thành phần bằng thí nghiệm loại bỏ thành phần.
- Xây dựng nguyên mẫu phần mềm nhập peptide, hiển thị ma trận hiệu ứng dự đoán, xếp hạng đột biến và xuất kết quả kèm thông tin mô hình.

## 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng:** Các peptide degron, phép thay thế đơn amino acid, chỉ số ổn định protein trong phép đo reporter và mô hình dự đoán hiệu ứng đột biến ở mức residue. Residue là một amino acid tại một vị trí cụ thể của chuỗi protein; footprint trong đề tài là bản đồ các vị trí hoặc phép thay thế ảnh hưởng đến hoạt tính degron theo hệ đo.

**Phạm vi:**

- Nguồn nhãn chính là dữ liệu peptide người của Zhang 2023, gồm đột biến quét và bão hòa. Miền đánh giá là bộ bão hòa sau lọc gồm 91 peptide, 89 cụm protein và 47.847 ô phép thay thế (ngưỡng PSI(WT) ≤ 3,0) [8]; đây là số mẫu sau xử lý của đề tài và được giữ nguyên làm outer-test. Cấu hình huấn luyện chính có thể nới ngưỡng lên PSI(WT) ≤ 4,0, thêm 85 peptide (44.490 ô, 83 cụm cov80 mới) chỉ vào phần huấn luyện, tức 176 peptide huấn luyện [11]. Cấu hình này chỉ được nhận vì đã đạt tiêu chí chốt trước (xem III.1); ngưỡng 3,0 vẫn được báo song song.
- Đầu vào chính là trình tự tham chiếu (WT), vị trí và amino acid thay thế. Đầu ra là hiệu ứng dự đoán ΔPSI; có thể tổng hợp thành ma trận L × 20, với L là độ dài peptide thuộc miền mô hình hỗ trợ.
- Dữ liệu mức peptide của Voutsinos được xem xét cho học chuyển tiếp. Larsen chỉ phục vụ khảo sát chuyển miền ở mức tile khi điều kiện sử dụng được xác nhận; không được thay cho nhãn đột biến thực nghiệm [2, 4].
- Koren 2018 (Table S4, saturation mutagenesis đầu C, cùng đại lượng PSI nhưng thư viện 23-mer và 3 bin) đã được audit: chỉ 5 cụm cov80 mới, thấp hơn ngưỡng 20 đã chốt, nên chỉ làm tập kiểm chứng ngoài cho lớp degron đầu C, không nhập vào huấn luyện. Nguồn không có giấy phép mở, chỉ dùng nội bộ [15].
- Không đặt nhận diện E3 cụ thể làm nhiệm vụ chính. Chưa thực hiện thí nghiệm sinh học mới; kết quả phần mềm hỗ trợ hình thành giả thuyết, không suy ra quan hệ nhân quả gây bệnh hoặc hiệu quả điều trị.

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

- **Biểu diễn:** mã hóa amino acid tham chiếu và thay thế, thành phần peptide, cửa sổ ngữ cảnh quanh vị trí đột biến; xem xét biểu diễn học được từ dữ liệu mức peptide.
- **Mô hình:** hồi quy ridge làm đối chứng đơn giản; PAP dự đoán điểm cả peptide, từ đó tính ΔPAP = PAP(mutant) − PAP(WT); Degformer dùng transformer dự đoán PSI [2, 3]. Chiều điểm khi đánh giá phải thống nhất với nhãn đích.
- **Học chuyển tiếp:** tiền huấn luyện biểu diễn trên nhãn hoạt tính mức peptide rồi tinh chỉnh cho ΔPSI. Nhãn hai mức có ý nghĩa khác nhau nên cần đầu dự đoán hoặc phép biến đổi phù hợp; không đổi nhãn nhị phân motif thành ΔPSI.
- **Công cụ dự kiến:** Python, NumPy, pandas, scikit-learn, PyTorch và MMseqs2; chỉ chọn cấu hình đủ nguồn lực và ghi phiên bản khi thực nghiệm.
- **Tài liệu tham khảo:** PAP [2], Degformer [3], MetaDegron [5] để đối chiếu phạm vi dự đoán.

## 4. Đánh giá và khả năng tái lập

- Chia dữ liệu theo cụm protein tương đồng thay vì chia ngẫu nhiên từng ô. Quy ước cov80 hiện dùng là phân cụm MMseqs2 với ngưỡng đồng nhất 30% và độ phủ 80%; kiểm độ nhạy bằng độ phủ 50% khi phù hợp.
- Dùng tập validation theo cụm bên trong mỗi fold huấn luyện để chọn siêu tham số; mọi chuẩn hóa, chọn đặc trưng và tiền huấn luyện đều phải loại cụm kiểm tra ngoài.
- Chỉ số chính là AUROC mức ô, tính riêng trên peptide đủ hai lớp rồi lấy trung bình. Nhãn nhị phân, ngưỡng và chiều hiệu ứng phải được cố định trong protocol trước so sánh. Bổ sung tương quan Spearman hoặc MAE cho ΔPSI liên tục và phân tích footprint khi đủ nhãn.
- So sánh ghép cặp trên cùng peptide; bootstrap theo cụm protein để ước lượng khoảng tin cậy. Báo kết quả từng seed bên cạnh kết quả tổng hợp và phân biệt benchmark phát triển với kiểm chứng độc lập.

# III. PHƯƠNG PHÁP NGHIÊN CỨU

## 1. Phương pháp tiếp cận

Đề tài kết hợp khảo sát tài liệu, nghiên cứu thực nghiệm có đối chứng và phát triển nguyên mẫu phần mềm. Câu hỏi nghiên cứu chính là: với dữ liệu đột biến có hạn, học biểu diễn từ nhãn mức peptide có tạo ra lợi ích dự đoán ổn định so với ridge và ΔPAP khi kiểm soát tương đồng protein hay không?

Trước hết, khảo sát đường cong học theo số cụm huấn luyện để kiểm tra giả thuyết thiếu nhãn (đã thực hiện, kết quả bên dưới). Sau đó, so cùng một bộ mã hóa ở hai chế độ khởi tạo ngẫu nhiên và tiền huấn luyện, dùng chung fold, ngân sách nhãn đột biến và quy trình chọn siêu tham số (đã thực hiện một thiết kế, kết quả âm). Các nhánh mô hình còn lại là phương án dự kiến, được giữ lại theo bằng chứng; đề cương không mặc định một kiến trúc mới sẽ thắng đối chứng.

Thiết kế dự kiến kế thừa 5 outer fold theo cụm cov80, validation bên trong, seed 17/29/43 và 5.000 lần bootstrap theo cụm. Mỗi nguồn tiền huấn luyện phải được kiểm chồng cụm với outer-test trước khi học. Các checkpoint có sẵn chỉ đưa vào bảng so sánh tổng quát hóa khi đã xác minh điều kiện dữ liệu; huấn luyện lại kiến trúc Degformer cùng ngân sách nhãn phải được ghi riêng với việc tái lập đầy đủ chế độ huấn luyện của tác giả.

Bằng chứng phát triển hiện có ghi nhận AUROC macro 0,8082 của ridge và 0,7693 của ΔPAP trên cùng bộ bão hòa [8]. Kết quả này chưa chứng minh tính mới kiến trúc. Các thử nghiệm tương tác và huấn luyện lại kiến trúc Degformer với ngân sách nhãn nhỏ cũng chưa cho lợi ích so với ridge [9]. Dữ liệu này định hướng giả thuyết tiếp theo, không thay thế một phép kiểm chứng xác nhận cuối cùng.

Các khảo sát ngày 22/10/2026 bổ sung năm kết quả, tất cả trên benchmark phát triển theo cụm (OOF), không phải kiểm chứng ngoài độc lập; nguồn số liệu ở mục [11–15]:

- **Đường cong học.** Với ridge, AUROC theo 25/50/75/100% số cụm huấn luyện là 0,7776 / 0,8044 / 0,8088 / 0,8082; chênh lệch 100% − 50% là +0,0038 với khoảng tin cậy 95% theo cụm [−0,0009; +0,0087], tức chưa đủ bằng chứng cho giả thuyết thiếu nhãn. Với mạng `gate_no_pap`, chênh lệch tương ứng là +0,0156 [+0,0060; +0,0256] và đường cong vẫn đi lên. Khoảng cách ridge − mạng thu hẹp nhưng chưa đảo chiều, nên kết quả này không phục hồi ứng viên kiến trúc nào đã bị loại [11].
- **Nới ngưỡng degron.** Thêm 85 peptide có PSI(WT) trong khoảng 3,0–4,0 vào phần huấn luyện, giữ nguyên outer-test, đưa AUROC của ridge từ 0,8082 lên 0,8208 (+0,0126; khoảng tin cậy [+0,0061; +0,0190]; dương ở cả ba seed). Kết luận còn đứng vững khi đổi `RESCUE_DELTA` (0,5 và 1,5), khi chia lại fold, và khi đổi sang ba phân hoạch protein thật sự khác (theo accession, id 0,2/cov 0,5, id 0,1/cov 0,3: +0,0166, +0,0134, +0,0113, khoảng tin cậy đều trên 0) [11, 13]. Lợi ích đạt đỉnh quanh ngưỡng 4,0 rồi giảm ở các ngưỡng cao hơn; ngưỡng 4,0 được chốt trước khi thấy lưới này.
- **Diễn giải thận trọng.** Phần tách riêng (thêm một nửa số cụm mới so với mốc cụm vùng cũ) ủng hộ cách đọc "độ phủ phân bố" ở ridge nhưng không dứt khoát ở mạng, và tiêu chí hình dạng chốt trước không đạt; kết luận là chưa phân định, không được viết thành "lợi ích hoàn toàn do mở rộng phân bố". Chưa tách được "vùng PSI(WT) khác" khỏi "protein khác" [11].
- **Tiền huấn luyện nhãn mức tile (Voutsinos).** Tiền huấn luyện encoder trên 212.616 tile rồi tinh chỉnh ΔPSI cho AUROC 0,8098, thấp hơn khởi tạo ngẫu nhiên (0,8175; hiệu −0,0077, khoảng tin cậy [−0,0163; +0,0006]) và thấp hơn ridge (0,8208; hiệu −0,0110, khoảng tin cậy [−0,0197; −0,0024]). Kết quả âm này chỉ bác thiết kế "tiền huấn luyện trên nhãn mức peptide rồi tinh chỉnh toàn bộ" đã thử, không suy ra cho thiết kế khác [12].
- **Hiệu chuẩn.** Điểm thô của ridge kém hơn việc dùng tần suất nền (Brier 0,1272 so với 0,1139). Hiệu chuẩn Platt trong inner-train đưa Brier xuống 0,0925 (hiệu +0,0346; khoảng tin cậy [+0,0266; +0,0425]; dương ở cả ba seed), và top 10% phép thay thế mỗi peptide làm giàu ô dương 4,02 lần so với ngẫu nhiên. Xác suất sau hiệu chuẩn vẫn thiên thấp trên miền gốc (trung bình 0,115 so với 0,131 quan sát) [14].

Đối với ứng viên mới, chỉ xem là có bằng chứng cải thiện khi chênh lệch ghép cặp với đối chứng chính có khoảng tin cậy dương và kết quả nhất quán qua các seed theo tiêu chí chốt trước. Nếu chưa đạt, báo cáo kết quả âm, giới hạn và nguyên mẫu sử dụng mô hình đối chứng tốt nhất; không tự coi mục tiêu đóng góp phương pháp đã hoàn thành. Hiện nguyên mẫu dùng ridge với cấu hình huấn luyện nới ngưỡng 4,0 cùng hiệu chuẩn Platt; chưa có ứng viên kiến trúc hay tiền huấn luyện nào đạt tiêu chí này. Trạng thái G2 (lợi ích ổn định của thành phần kiến trúc, đối chứng Degformer sạch cụm) và G3 (công cụ) vẫn chưa hoàn tất.

## 2. Quy trình thực hiện

| STT | Nội dung | Kết quả |
|:---:|:---|:---|
| 1 | Nghiên cứu sinh học degron, khảo sát PAP, Degformer, MetaDegron và nguồn nhãn | Tổng quan tài liệu; bảng so sánh bài toán, dữ liệu và giới hạn |
| 2 | Kiểm dữ liệu, tái tính PSI, ánh xạ tọa độ, phân cụm và thiết kế đánh giá | Bảng nhãn; sổ nguồn gốc; danh sách fold; protocol và đối chứng |
| 3 | Đo đường cong học; thiết kế, huấn luyện mô hình và ablation; xây dựng phần mềm | Runner tái lập; mô hình ứng viên; API, giao diện và chức năng xuất kết quả |
| 4 | Kiểm thử phần mềm và kiểm chéo thực nghiệm | Ca kiểm thử; đối chiếu điểm giao diện với runner; báo cáo rò rỉ, lỗi và kết quả từng seed |
| 5 | Đánh giá, phân tích sai số, viết báo cáo và hoàn thiện luận văn | Bảng so sánh có khoảng tin cậy; báo cáo đóng góp, giới hạn; mã nguồn và hướng dẫn |

**Tiến độ đến 22/10/2026.** Bước 1–2 đã có phần lớn. Ở bước 3 đã đo đường cong học, nới ngưỡng degron, tiền huấn luyện nhãn tile (kết quả âm), hiệu chuẩn và nguyên mẫu dòng lệnh (chưa có API hay giao diện web) [11–14]; audit Koren 2018 chưa qua cổng nhập huấn luyện [15]. Bước 4–5 gần như chưa làm; Chương 4 luận văn mới viết phần thực nghiệm đã có.

**Việc còn lại.** (a) Tìm thêm nguồn nhãn khác Koren: Timms 2023 và tiền ấn phẩm về biến thể gây bệnh phá degron (cả hai chưa xác minh quyền sử dụng, có đột biến điểm hay không và endpoint); (b) tách "vùng PSI(WT)" khỏi "protein khác" nếu có cặp peptide cùng protein ở hai vùng ngưỡng; (c) đối chứng Degformer sạch cụm để hoàn tất G2; (d) API và giao diện web cho nguyên mẫu, cùng bộ ca kiểm thử; (e) viết luận văn.

Tiến độ theo tuần và mốc nộp sẽ bổ sung sau khi có lịch học phần và thống nhất phạm vi với giảng viên hướng dẫn.

# IV. ỨNG DỤNG THỰC TẾ VÀ NGUỒN DỮ LIỆU

## 1. Ứng dụng thực tế

- Hỗ trợ người nghiên cứu lựa chọn vị trí và amino acid thay thế để làm thí nghiệm tiếp theo, kèm đột biến đối chứng.
- Trực quan hóa ma trận hiệu ứng, đối chiếu dự đoán với ô thực nghiệm đã có và truy xuất nguồn dữ liệu, phiên bản mô hình.
- Hỗ trợ giảng dạy và khảo sát mối liên hệ giữa trình tự peptide và tín hiệu phân hủy. Kết quả chỉ có ý nghĩa trong phạm vi hệ đo và miền dữ liệu được mô tả.

Luồng phần mềm dự kiến: nhập peptide hợp lệ → sinh các phép thay thế → tính điểm bằng mô hình đã cố định → hiển thị ma trận và bảng xếp hạng → xuất CSV/JSON cùng provenance. Trường hợp thiếu dữ liệu, sai tọa độ hoặc nằm ngoài miền hỗ trợ phải được thể hiện rõ; không chuyển điểm chưa hiệu chuẩn thành xác suất bệnh.

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
- **Kết quả nghiên cứu:** bằng chứng về ảnh hưởng của lượng và phân bố nhãn, và hiệu quả học chuyển tiếp, đối với dự đoán ΔPSI. Đã có: nới ngưỡng degron cải thiện ridge (+0,0126) và bền qua các độ nhạy đã kiểm; tiền huấn luyện nhãn tile theo thiết kế đã thử chưa có lợi ích [11–13]. Nếu một ứng viên sau này cải thiện ổn định, xác định thành phần tạo lợi ích bằng ablation; nếu chưa có, báo cáo trung thực phạm vi thất bại và giới hạn kết luận. Mọi con số là benchmark phát triển, chưa phải kiểm chứng độc lập.
- **Sản phẩm phần mềm:** nguyên mẫu nhập peptide, tạo ma trận dự đoán, xếp hạng phép thay thế, đối chiếu dữ liệu đo và xuất kết quả kèm phiên bản mô hình, nguồn dữ liệu, miền áp dụng. Đã có bản dòng lệnh tối giản, xuất điểm đã hiệu chuẩn Platt và tái tính khớp runner (chênh dưới 1e-9) [14]; giao diện web, API và bộ ca kiểm thử còn lại.
- **Kiểm thử và tài liệu:** bộ ca kiểm thử đầu vào, tọa độ, chiều điểm và xuất dữ liệu; kết quả giao diện khớp runner trong sai số số học; tài liệu cài đặt, sử dụng và tái lập.
- **Luận văn:** tổng quan, thiết kế phương pháp, kết quả định lượng, phân tích sai số, giới hạn và hướng phát triển. Khả năng vượt đối chứng và tính mới kiến trúc là mục tiêu cần kiểm chứng, chưa phải kết quả đã đạt.

# VII. TÀI LIỆU THAM KHẢO

Quản lý tài liệu bằng **Zotero hoặc Mendeley** theo yêu cầu của mẫu. Danh mục dưới đây là danh mục khởi đầu; các báo cáo nội bộ [8–15] dùng để truy xuất bằng chứng tiền đề, không thay thế công trình khoa học đã công bố.

1. Zhang, Z. và cộng sự (2023). *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*. Molecular Cell, 83, 3377–3392.e6. DOI: <https://doi.org/10.1016/j.molcel.2023.08.022>.
2. Voutsinos, V. và cộng sự (2026). *A near-complete map of human cytosolic degrons and their relevance for disease*. Science Advances. DOI: <https://doi.org/10.1126/sciadv.adz3483>.
3. Alpine2048. *Degformer: Transformer model for internal and C-terminal degron prediction*. Mã nguồn, commit 49ee52459967. [GitHub](https://github.com/Alpine2048/Degformer/tree/49ee524599671f2b5e30d9cd052ce6baa55c06d8).
4. Larsen, F. B. và cộng sự (2025). *Comprehensive degron mapping in human transcription factors*. bioRxiv, bản tiền ấn phẩm. DOI: <https://doi.org/10.1101/2025.05.16.654404>.
5. Zheng, M. và cộng sự (2024). *MetaDegron: multimodal feature-integrated protein language model for predicting E3 ligase targeted degrons*. Briefings in Bioinformatics, 25(6), bbae519. DOI: <https://doi.org/10.1093/bib/bbae519>.
6. Zhang và cộng sự (2023). Bộ dữ liệu đi kèm nghiên cứu degron, *Mendeley Data*, phiên bản 2. DOI: <https://doi.org/10.17632/32h94v2yv2.2>.
7. NCBI. *GEO Series GSE240610*. [Trang dữ liệu](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610).
8. Nguyễn Thanh Trọng (18/10/2026). *G2 — học trực tiếp trên ma trận bão hòa*. Báo cáo nội bộ; số mẫu và AUROC từ `research/g2-saturation-2026-10-18/results.json`; khoảng tin cậy ridge từ `audit.json`.
9. Nguyễn Thanh Trọng (18/10/2026). *G2 — mở rộng: ba câu hỏi còn mở của báo cáo bão hòa*. Báo cáo nội bộ; kết quả tại `research/g2-extension-2026-10-18/`.
10. Nguyễn Thanh Trọng (21/10/2026). *Phân tích MetaDegron và đối chiếu đề tài hiện tại*. Báo cáo nội bộ tại `research/metadegron-analysis-2026-10-21/`; phần đề xuất chưa phải quyết định thực hiện.
11. Nguyễn Thanh Trọng (22/10/2026). *Đường cong học theo cụm (P1) và nới ngưỡng degron (P0)*. Báo cáo nội bộ; số liệu từ `research/learning-curve-2026-10-22/results.json`, `results-b.json`, `results-c.json`; benchmark phát triển OOF.
12. Nguyễn Thanh Trọng (22/10/2026). *P3 — tiền huấn luyện nhãn mức tile rồi tinh chỉnh ΔPSI*. Báo cáo nội bộ tại `research/pretrain-p3-2026-10-22/`; kết quả âm.
13. Nguyễn Thanh Trọng (22/10/2026). *Độ nhạy theo độ mịn phân cụm của lợi ích nới ngưỡng*. Báo cáo nội bộ tại `research/recluster-sensitivity-2026-10-22/`.
14. Nguyễn Thanh Trọng (22/10/2026). *P6 — hiệu chuẩn điểm và nguyên mẫu dòng lệnh*. Báo cáo nội bộ tại `research/calibration-p6-2026-10-22/`.
15. Nguyễn Thanh Trọng (22/10/2026). *Audit Koren 2018 Table S4 và cổng P2*. Báo cáo nội bộ tại `research/koren-s4-audit-2026-10-22/`; nguồn gốc: Koren, I. và cộng sự (2018), Cell 173(7), 1622–1635.e14, DOI: <https://doi.org/10.1016/j.cell.2018.04.028>.
