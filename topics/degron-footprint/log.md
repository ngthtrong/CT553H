# Nhật ký đề tài `degron-footprint`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../DECISIONS.md).

---

## 12/10/2026 — `degron-e3-specificity`: đo giới hạn thành phần và quy mô test theo protein

- Theo đề xuất của sinh viên, tải lại scanning và saturation từ Mendeley v2 vào `topics/degron-footprint/data/raw/`, kiểm đầy đủ SHA-256; script cũ tái lập chính xác 8.831 peptide đạt lọc và 2.624 footprint. Báo cáo: [audit thành phần–ngữ cảnh](research/composition-context-audit.md); script/JSON tại [ghi chú audit](research/e3-labels-audit/README.md).
- **Đo:** 2.046/2.624 footprint có cùng cặp thay thế nhưng khoảng chênh ΔPSI ≥1; oracle trung bình theo cặp P@3 **0,5481**, cận kỳ vọng chính xác **0,6045**, oracle không ràng buộc **0,7792**. Cận Spearman do nới lỏng **0,7931**. Nhãn đánh giá được dùng để tính oracle; chưa là performance mô hình học được và chưa tách nhiễu đo.
- **Protein:** 9.817 peptide / 6.582 accession; footprint trên 2.232 accession, tối đa 7/protein. UniProt hiện tại cung cấp 6.573 accession; có 2.602 footprint khớp trình tự sau bỏ stop cuối. Chia thử 80/10/10 theo cụm full protein, identity 30%: test khớp tham chiếu **271–322** footprint (coverage hai chiều 80%), **221–301** (50%) qua 5 seed. Chưa là benchmark chính thức hoặc bằng chứng không rò rỉ đồng dạng.
- **Đính chính đề xuất:** scanning là ô quan sát từng hàng, không phải marginal; ΔPAP không phải hạng 1 nói chung (mô hình thành phần tuyến tính đã có thể hạng 2). Phương án ma trận đề xuất dùng nhánh thành phần cộng hiệu chỉnh ngữ cảnh hạng thấp, mask WT→WT/stop/nhãn thiếu. Đã sửa các lập luận PAP/phẳng, pooling và nhãn saturation trong [topic-decision.md](research/topic-decision.md), giữ tên và kiến trúc ở trạng thái cũ; phương án ma trận vẫn là đề xuất. Cần xử lý score saturation và chia cả hai nguồn trước khi train.
- **Kiểm:** 200 đối chiếu exhaustive P@3, 4.000 kiểm cận rank, đối chiếu Spearman có tie với SciPy; checksum, tái lập pipeline counts và compile script đạt. Không huấn luyện mô hình. Thay đổi `CLAUDE.md` xuất hiện đồng thời từ ngoài công việc này được giữ nguyên.

---

## 11/10/2026 — hoàn thiện hub học `degron-e3-specificity` sau phiên Claude bị ngắt

- Hoàn thiện [hub năm chặng](../../lectures/degron-footprint/index.html) và [ghi chú vận hành](../../lectures/degron-footprint/README.md): 22 trang HTML gồm 6 bài nền, danh mục/chín trang bài báo và 5 trang đào sâu đề tài. Nối từng phần của [presentation.html](presentation/presentation.html) tới bài đọc sâu; thêm đường về hub từ báo cáo kiểm chứng và danh sách đề tài.
- Đồng bộ phần dạy đề tài với quyết định tái định tâm cùng ngày: footprint theo residue là mục tiêu chính; nhãn toàn đoạn là phụ trợ; E3 là ca nghiên cứu. Viết lại các trang dữ liệu, kiến trúc, đánh giá, câu hỏi mở, Zhang 2023, Larsen 2025, MetaDegron 2024 và phần giải thích vì sao bỏ điều kiện hóa E3. Bổ sung tiền lệ BioBlobs, OmniESI, ELITE ngoài danh mục chín bài chính; sửa tác giả MetaDegron và tên BioBlobs trong trình bày.
- Kiểm [liên kết và nhãn ảnh](../../lectures/degron-footprint/check_links.py): 22 trang, 360 tham chiếu tương đối, không file/anchor hỏng; `git diff --check` đạt. Đã xem ảnh chụp Chrome của hub, hai trang trọng tâm và hình gốc Voutsinos ở độ rộng 500 px, hub ở 780 px: chữ, điều hướng và chú thích đọc được; hình lớn cuộn trong khung. Không chạy thí nghiệm hoặc huấn luyện mô hình.
- **Còn thiếu:** Table S5 do tác giả curate chưa truy được; chưa kiểm toàn bộ tiền lệ mới, chưa dùng thử DEGRONOPEDIA; chưa có kết quả mô hình footprint. Các trang ghi rõ đây là giới hạn, không suy ra kết quả còn thiếu.
- **Đính chính audit:** hai số 27 peptide (được gán E3; có bản đồ bão hòa) không chỉ cùng một tập. Giao của `e3-assignment.json` và `overlap-audit.json` là **23 peptide**; đã sửa [ghi chú audit](research/e3-labels-audit/README.md), quyết định đề tài, presentation và hub. Mục cũ bên dưới ghi “27 có cả hai” là sai theo hai JSON đã lưu.

---

## 11/10/2026 (khuya) — **CỔNG CHẶN 2 KHÔNG QUA**: chỉ 1 E3 đủ mẫu; nhưng nhãn theo residue lớn gấp nhiều lần tài liệu ghi

- **Yêu cầu của sinh viên:** đếm nhãn E3/adaptor thực sự dùng được, và đọc đầy đủ công trình gần nhất có thể trùng ý tưởng.
- **Vòng được paywall:** Table S1–S7 trên PMC trả `Checking your browser - reCAPTCHA`; Europe PMC trả *"not open access"*. Lấy được dữ liệu thô từ **Mendeley Data 10.17632/32h94v2yv2.2** mà chính bài khai báo (3 file ZIP, có SHA-256 trong ghi chú). Zenodo 8103915 chỉ có mã DegronID, không có nhãn.
- **Ghi chú và 7 script tái tạo:** [research_notes/degron-e3-labels/](research/e3-labels-audit/README.md).

### Cổng chặn 2 — kết quả: KHÔNG QUA cho thành phần có điều kiện E3

- **31 screen CRISPR** trong dữ liệu (trừ 3 control) → **27 gán được adaptor**, **25 gán rõ**, **10 E3 khác nhau**.
- **Phân bố giết thiết kế:** KLHL15 **13** peptide · BAG6 **4** · ASB7 **2** · FEM1B **2** · ASB3, KLHL9, FBXW5, FBXO21, FBXO38, DCAF5 **1 mỗi cái**.
- **Bền với ngưỡng:** quét 36 tổ hợp (fdr × lfc × goodsgrna) → gán được 16–29, số E3 8–10, và **số E3 có ≥5 peptide LUÔN đúng bằng 1**. Không ngưỡng nào cứu được.
- **Hệ quả:** thành phần 3 của CMIL-E3 (điều kiện E3 kiểu FiLM) **không huấn luyện được**, và không khái quát sang E3 mới vì chỉ có 10 E3 để học quan hệ trình tự–đặc hiệu. **Không được nói "16 E3 có nhãn CRISPR" như thể đó là 16 lớp dùng được** — con số phải nói là số peptide trên mỗi E3, tức 1–13.
- Một sai sót đã tự sửa trong phiên: lần chạy đầu loại hit theo **tần suất** nên **loại oan KLHL15** (13/31 screen); đã đổi sang loại bộ máy chung theo danh sách tường minh. `APPBP2` xuất hiện ~17/31 screen nhưng lfc 0,8–1,6 nên tự rơi dưới ngưỡng; bài báo cũng tự thừa nhận có nhiễm sgRNA ở một số lô.
- **Chưa lấy được Table S5** (gán E3 do tác giả curate, gồm cả "individual testing") → con số trên là **giới hạn dưới**.

### Phát hiện ngoài dự kiến: nhãn theo residue lớn hơn repo ghi rất nhiều

- **Đột biến quét:** 9.817 peptide trong thư viện, **8.831** có cả hoang dã và biến thể được chấm, **256.711 phép đo** có PSI và reads ≥10, median **28/28 vị trí** mỗi peptide.
- **Peptide thực sự CÓ footprint học được: 2.624** (degron PSI≤3, phủ ≥21 vị trí, có ≥1 vị trí mà đột biến làm PSI tăng ≥1,0); trong đó **2.402 khu trú** (≤6 vị trí quan trọng). **Median 3 vị trí quan trọng trên 28.**
- **Đột biến bão hòa:** **249 peptide × median 560 biến thể = 135.040** định danh, 239 peptide phủ ≥27 vị trí sau lọc reads. Bài báo nói "219 footprint" — đó là tập tác giả curate; dữ liệu thô đỡ được 239–247.
- **Chồng lấn:** **27/31** peptide CRISPR có bản đồ đột biến bão hòa; 25 có cả hai. Bốn peptide thiếu đúng là bốn peptide BAG6 (screen riêng, không phải CRL).
- **Median 3 vị trí quan trọng trên 28** là con số quan trọng nhất của vòng audit: tín hiệu **khu trú thật**, trong khi PAP bất biến hoán vị (Pearson gốc–đảo = 1,000000) nên về nguyên lý không biểu diễn được nó.

### Đọc công trình gần nhất

- **Zhang 2023, toàn văn.** Mô hình của họ là **SVM trên 20 đặc trưng thành phần**, cộng **DegronID** — chấm độ giống motif bằng PSSM dựng từ footprint **đã đo**, rồi gom cụm thứ bậc 40 nhóm. **Không** dự đoán bản đồ đột biến từ trình tự, **không** dùng PLM, **không** có mô hình có điều kiện E3.
- **Bài transcription factor 05/2025, toàn văn.** Đột biến thực nghiệm của họ **có đích, không bão hòa** (xóa đoạn ASCL1 23–40, HSF1 198–217; điểm ZNF140 H323Y); bản đồ thay thế đầy đủ là **in silico** ΔPAP, không phải đo.
- **Tra tiền lệ cho bài toán tái định tâm:** không tìm được ai dự đoán bản đồ độ nhạy đột biến theo residue cho degron. Mọi mô hình degron đã có đều ở mức peptide/protein và phần lớn dựa trên thành phần (PAP kernel=1, SVM-20, QCDPred hồi quy logistic, Degpred BERT, MetaDegron SeqVec, deepDegron chỉ hai đầu chuỗi). **Phản biện phải trích:** một khung học máy 2025 báo rằng 6 điểm thay thế mỗi residue đủ suy ra phần còn lại với ~90% độ chính xác trên dữ liệu quét đột biến sâu nói chung.

### Quyết định của sinh viên: TÁI ĐỊNH TÂM — đã thực hiện xong trong phiên

**Tên mới:** *Dự đoán footprint degron ở mức residue bằng học đa thể hiện với cổng phơi lộ cấu trúc, trên nhãn đột biến thực nghiệm.* Slug giữ `degron-e3-specificity` để không vỡ liên kết.

- **Kiến trúc đổi tên CMIL-E3 → MIL-Degron, 6 thành phần → 5.** Bỏ thành phần điều kiện E3. Lý do giữ cấu trúc túi đổi hẳn: không còn là "nhãn chỉ ở mức peptide" mà là **nối nhãn yếu mức đoạn (212.658) với nhãn mạnh mức residue (256.711) trong một mô hình**. Attention giờ **được giám sát trực tiếp** bằng nhãn đột biến, không chỉ dùng để diễn giải.
- **Thước đo chính mới:** Spearman theo từng peptide trên vector 28 chiều, cộng **precision@3** (chọn 3 vì median số vị trí quan trọng là 3/28), chia **theo peptide** trên 2.624 footprint. Tập kiểm tra khác thư viện: 249 bản đồ thay thế đầy đủ. Đối chứng âm có sẵn: mô hình bất biến hoán vị phải cho bản đồ phẳng.
- **Đối chứng bắt buộc tự đặt ra:** đầu hồi quy theo vị trí **không có MIL**. Khi đã có nhãn mức residue thì MIL không còn bắt buộc — phải tự nói ra điều này, và nếu đối chứng đủ tốt thì báo đúng như vậy.
- **E3 còn lại ở vai trò ca nghiên cứu** trên 27 peptide có cả nhãn E3 và bản đồ đột biến đầy đủ; KLHL15 (13 peptide) là lớp duy nhất đủ thử một đầu ra theo E3.
- **Đã cập nhật:** [topic-decision.md](research/topic-decision.md) (viết lại mục 1–6, thêm 2.1 và 7.1–7.2, thêm 4 quy ước ngôn từ), [presentation.html](presentation/presentation.html) (đổi tiêu đề, bảng đầu vào/đầu ra, phạm vi, bảng kiến trúc 5 thành phần, hộp giới hạn lập luận MIL, bảng dữ liệu + hộp số liệu tự đếm, ba bậc thước đo, bảng năm tiêu chí, mục cổng chặn, thêm tài liệu 14 và đánh số lại 15–18 — kiểm cấu trúc HTML và ID: không lỗi, không trùng), [session-02-prep.md](presentation/session-02-prep.md), [topics/README.md](../README.md), [CLAUDE.md](../../CLAUDE.md).
- **Còn dở:** chưa lấy được Table S5 (gán E3 do tác giả curate — chỉ thêm peptide, không đổi kết luận); sơ đồ SVG luồng dữ liệu vẫn vẽ nhánh điều kiện E3 đã bỏ, hiện chỉ ghi chú bằng chữ trong figcaption, **chưa vẽ lại**; chưa chạy phép đảo thứ tự residue trên sàng lọc 2; chưa chạy baseline, chưa huấn luyện, chưa xây website.

---

## 11/10/2026 (cuối phiên) — khảo sát lại đề tài một cách trung thực; **cổng chặn 1 đã qua**, hai tuyên bố bị thu hẹp

- **Yêu cầu của sinh viên:** khảo sát và đánh giá trung thực lại `degron-e3-specificity` so với các ứng viên còn lại trong repo. Sau đó sinh viên chọn **chuẩn bị slide tuần 6 luôn**, không đếm nhãn E3 trước.
- **Phát hiện về quy trình:** quyết định chốt đề tài ngày 11/10 **không có phép so sánh nào**. `grep` xác nhận tài liệu degron không nhắc DARKIN, và `main-topic-decision.md` cùng bốn ghi chú nền không nhắc degron. Ba cổng bắt buộc G1/G2/G3 chưa từng được áp cho degron. Đã áp lại trong phiên này.
- **Kết quả áp lại ba cổng cho degron:** **G1 (nhãn) đạt, mạnh nhất cả repo** — mọi nhãn là nhãn thực nghiệm. **G2 (đóng góp dương) chưa xác lập** — phụ thuộc số nhãn E3 chưa đếm, và phần bằng chứng vững nhất lại là một kết quả phê phán, đúng loại đã dùng để loại hướng sirtuin. **G3 (website) đạt nhưng yếu nhất** — ba sản phẩm đã tồn tại, không phải hai.
- **CỔNG CHẶN 1 ĐÃ QUA, theo hướng thuận.** Đọc được toàn văn bài degron transcription factor (Larsen và cộng sự, bioRxiv 05/2025): **không** mô hình hóa đặc hiệu E3, **không** kiến trúc mới, **không** nhãn E3 hay CRISPR, **không** có XAI. PAP cùng ESM-1b chỉ dùng so biến thể CRX. Trục của đề tài còn trống.
- **Nhưng cùng bài đó buộc sửa hai chỗ:** họ đã tính rASA và pLDDT từ AlphaFold2 kèm DSSP, và đã làm bản đồ thay thế in-silico ΔPAP → "dùng cấu trúc" và "giải thích biến thể" không còn là phần mới. Và có **bộ dữ liệu thứ tư**: thư viện nhân **58.781 đoạn / 1.626 TF**, cộng **8.645 đoạn / 234 protein** chồng lấn với thư viện bào tương — lựa chọn rẻ hơn cho bậc 2 (cùng assay, khác khoang).
- **PHẢI THU HẸP tuyên bố về nhãn E3.** Đọc toàn văn MetaDegron (*Brief Bioinform* 2024): **đã dự đoán degron theo từng E3 cho 21 E3 ligase**, có máy chủ web với cây chọn E3. Nên không nói "chưa ai làm đặc hiệu E3". Phát biểu đúng: chưa ai huấn luyện trên nhãn adaptor CRL theo CRISPR ở quy mô sàng lọc. Chỗ đó thật sự còn trống — MetaDegron huấn luyện trên **~300 degron curate**, âm tính là **peptide ngẫu nhiên**, chia 90/10, AUC 0,87–0,90, không kiểm soát đồng dạng. Nó cũng đã dùng độ phơi lộ nhưng ở **đầu vào**, không ở bước gộp.
- **PHẢI THU HẸP tuyên bố tính mới kiến trúc (cổng chặn 3).** Chưa thấy ai dùng MIL cho degron — phần đó giữ. Nhưng **BioBlobs** (arXiv 2510.01632, 10/2025) đã dùng đúng attention-based MIL kiểu Ilse 2018 trên protein, và **OmniESI** (arXiv 2506.17963, 2025) đã dùng điều biến có điều kiện enzyme–cơ chất. Kết luận: **mới ở chỗ ghép và chỗ đặt cổng phơi lộ, không mới ở cơ chế** — đúng mức novelty đã dùng để hạ dark kinome ở phép kiểm 6.5b.
- **Hai đối thủ mới chưa có trong repo:** **ELITE** (bioRxiv 11/2025, ProtBERT Siamese xếp hạng E3 cho substrate, Integrated Gradients, âm tính từ Negatome) và **E3TargetPred**. Ở mức cặp protein–protein, không mức residue → không giết đề tài, nhưng chiếm khung và phải vào bảng khảo sát.
- **Phán quyết:** degron **vẫn đứng đầu** các ứng viên trong repo, nhưng vì **G1 và tiêu chí 4**, không vì kiến trúc. Bài bán đề tài đang sai trọng tâm và đã được sửa.
- **Đã làm:** sửa [presentation.html](presentation/presentation.html) — đóng cổng 1, thêm nhóm G vào bảng khảo sát (giờ bảy nhóm A–G), số thật của MetaDegron, hộp giới hạn tuyên bố tính mới, bộ dữ liệu thứ tư, sửa ba ô trong bảng năm tiêu chí, viết lại mục 6.1, thêm bốn tài liệu tham khảo (14–17). Kiểm cấu trúc HTML và ID: không lỗi, không trùng. Thêm [session-02-prep.md](presentation/session-02-prep.md) — kịch bản nói, cây quyết định theo câu trả lời của GVHD, danh sách điều phải tự nói ra.
- **Còn dở:** **đếm nhãn E3 trong Table S3/S4/S6/S7 của Zhang 2023** — giờ là cổng duy nhất còn lại và là con số quyết định G2. Chưa thống nhất tình trạng GPU (10/10 ghi có GPU; mục 9 của topic-decision.md ghi máy không có GPU). Chưa tra danh sách trích dẫn bài 2026 và nội bộ MetaDegron. Chưa huấn luyện mô hình, chưa xây website.

---

## 11/10/2026 — tiếp tục phiên Claude: hoàn thiện giao diện `degron-e3-specificity`

- Hoàn thiện [presentation.html](presentation/presentation.html): hoạt ảnh trên sơ đồ, ô số liệu có nguồn audit, biểu đồ pooling có bảng và giới hạn phép thử, minh họa tương tác peptide/protein, sáng/tối, dừng chuyển động, cuộn hình trên điện thoại và chế độ in.
- Phân biệt hình minh họa với số đo; làm rõ bất biến hoán vị chỉ áp dụng kênh nội cnn2w1, không khái quát sang kênh C-term của PAP.
- Kiểm tra Chromium desktop/điện thoại, sáng/tối, giảm chuyển động, ngoại tuyến/tắt JavaScript, nút tương tác và liên kết nội bộ đều đạt; có kiểm tra ảnh chụp. Chi tiết: [presentation-validation.md](presentation/presentation-validation.md).
- Không thêm thí nghiệm ML. Ba cổng nghiên cứu trong [quyết định đề tài](research/topic-decision.md) vẫn còn; lần này hoàn tất phần trình bày còn dở.

---

## 11/10/2026 (muộn) — **CHỐT ĐỀ TÀI `degron-e3-specificity`**; kiểm chứng xong 10 điểm; GVHD kỳ vọng kiến trúc mới

- **Sinh viên chốt đề tài:** *Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc.* Tài liệu: [topic-decision.md](research/topic-decision.md), [presentation.html](presentation/presentation.html) (bố cục 6 mục, mở bằng `file://`), [báo cáo chi tiết bản 3](research/topic-report/index.html). **Chưa có phê duyệt GVHD.**
- **Thông tin mới từ GVHD: thầy kỳ vọng một kiến trúc chưa ai dùng**, không chấp nhận chỉ một bảng đối chứng có kỷ luật. → đề xuất kiến trúc **CMIL-E3** (học đa thể hiện có điều kiện E3 + cổng phơi lộ ở chỗ gộp), sáu thành phần, **mỗi thành phần gắn với một phép đo tự thực hiện**.
- **Theo yêu cầu: HTML tạo trực tiếp trên hệ thống, không dùng artifact.** Artifact bản 1 (`XAXzVcA6ot1eVVk4927suc`) giờ **lạc hậu**, file trong repo là bản chuẩn.

### Kết quả kiểm chứng 10 điểm — bốn điểm đi ngược bản 1

- **Tái lập được số của bài báo.** Tự dựng PAP bằng numpy từ trọng số công bố: kênh nội **0,8239** (bài: 0,82), đầy đủ **0,8690** (bài: 0,87) trên holdout hiệu dụng 428 gene. Chênh lệch 0,82–0,87 là do kênh C-term phải áp cho **mọi** tile (trong assay mọi tile đều gắn vào đầu C của GFP).
- **Phép đo quan trọng nhất:** đảo ngẫu nhiên thứ tự residue → điểm cnn2w1 **không đổi**, Pearson(gốc, đảo) = **1,000000**. PAP mặc định **bất biến hoán vị**, không biểu diễn được motif nào, vẫn đạt 0,869.
- **BÁC BỎ đóng góp phương pháp của bản 1:** repo có sẵn `cnn2w7` (cửa sổ 7, bắt được motif). Tự chạy: **0,8722 so với 0,8690 = +0,0032**. Trần của trục "thêm năng lực bắt motif" đã do chính tác giả đo.
- **Thêm:** thay gộp trung bình bằng gộp max làm sụt **0,824 → 0,344**; entropy theo vị trí 3,294/3,401 → tín hiệu thang điểm khối **dàn đều, không khu trú**. Hệ quả: kiến trúc khu trú **sẽ không thắng** trên thang điểm khối — phải chốt thước đo với GVHD trước.
- **CỔNG CHẶN ĐÃ MỞ:** GEO **GSE240610** tải được. Table S1 = 52,9 MB, 3 sheet × **475.507 dòng** kèm PSI; thêm RAW.tar 21 MB.
- **BÁC BỎ "chưa ai dùng PLM trên bộ này":** cùng nhóm có bài tiếp theo — degron trên **1.620 (chính xác 1.626) transcription factor**, tiền ấn bioRxiv 17/05/2025, **dùng PAP cùng ESM-1b**, và đã chỉ ra tác động biến thể tương quan độ mạnh degron. Ăn vào một phần đóng góp "giải thích biến thể theo cơ chế".
- **SỬA SỐ MaveDB:** 100.514 → **69.209 biến thể duy nhất** (bản 1 đếm cả dòng không có điểm; trùng lặp dồn ở PRKN và PTEN).
- **Rò rỉ bậc 3 đã định lượng:** 6/9 gene MaveDB có tile, **toàn bộ ở tập train**, nhưng chỉ **132 tile = 0,07%** → sửa gần như miễn phí. 3 gene còn lại (CYP2C9, CYP2C19, LDLR) không thuộc bào tương.
- **Chênh lệch 96 gene đã đặc tả:** phân vùng thật giữ lại **473 gene**; danh sách 527 = 428 đúng + 96 sai + 3 một phần; **45 gene bị giữ lại mà không có trong danh sách**. Nhóm 96 có nhiều tile hơn rõ rệt (64,3 so với 37,0 tile/gene) → suy luận: danh sách là tập tiền tuyển, gene lớn được trả về train.
- **Alignment độc lập làm giảm tuyên bố bản 1:** Smith-Waterman thật (parasail, sàng 6-mer) → **14/428 (3,3%)** gene holdout có họ hàng trong train ở identity ≥30%/coverage ≥50%; **1 ca trùng 100% trên 77 residue** (`AC104389.5` so với **TRIM5**). Bản 1 nói "không có paralog nào" là quá mạnh.
- **Lỗi tái lập trong mã công bố:** `train_cnn2w.py` dùng `ci_aa=1` → trỏ vào cột **DNA**, và A/C/G/T đều là ký hiệu acid amin hợp lệ nên bộ lọc không loại. Chạy mã công bố trên dữ liệu công bố sẽ huấn luyện trên chuỗi DNA.
- **Tài nguyên đã đo:** ESM-2 **35M** 64,6 tile/s → **~55 phút** toàn bộ; **650M** 5,3 tile/s → **~11 giờ**; cache mức residue 650M **32,7 GB** vượt RAM 7 GB. Hugging Face truy cập được.
- **Giấy phép:** repo và Zenodo **MIT**, MaveDB **CC0**, DegronID other-open, hai bản tiền ấn **CC BY-NC-ND**.
- **Còn dở — ba cổng chặn:** (1) đọc toàn văn bài degron TF (`biorxiv.org` bị chặn với WebFetch, chỉ lấy được tóm tắt qua API); (2) mở Table S3/S4/S6/S7 của Zhang 2023 để đếm nhãn E3 dùng được; (3) tra hệ thống tính mới của kiến trúc MIL. Chưa huấn luyện mô hình, chưa xây website.

---

## 11/10/2026 — ứng viên mới: dự đoán degron có bối cảnh cấu trúc; audit bản đồ tile 2026

- **Yêu cầu của sinh viên:** tìm hướng mới hơn, đóng góp rõ hơn, Claude tự quyết; vòng này **bỏ ràng buộc lĩnh vực và độ khớp GVHD**, nhắm **dữ liệu mới cộng trục phương pháp gắn lên nó** (sinh viên chọn qua câu hỏi trắc nghiệm).
- Sản phẩm: [báo cáo HTML](research/topic-report/index.html) — publish tại https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc. Thêm dòng vào [resources.md](../../resources/README.md) và [topics/README.md](../README.md).
- **Hướng đề xuất:** dự đoán degron (tín hiệu phân hủy protein) có tính tới trạng thái phơi lộ cấu trúc. Đóng góp chính là **thang đánh giá ba bậc**: (1) trong cùng sàng lọc, holdout kiểm soát đồng dạng; (2) chuyển giữa hai sàng lọc khác assay; (3) từ peptide tách rời sang protein nguyên vẹn. Bậc 2 và 3 **chưa ai đo**.
- **Tự audit bản đồ tile Voutsinos 2026** (repo `KULL-Centre/_2025_Voutsinos_degron_cytosol`, MIT, có SHA-256): 212.658 tile / 5.327 gene; train 195.629 tile / 4.830 gene; nhãn liên tục −0,144…1,132 (hồi quy thật, không phải phân loại mất cân bằng).
- **Hai giả thuyết của tôi đã sai, ghi lại để không lặp:** holdout chia **theo gene**, và **cả 527 gene holdout đều là cụm đồng dạng đơn lẻ**; tập validation early stopping cũng rời hẳn theo gene (0 gene trùng). **Không được lấy "sửa giao thức đánh giá" làm đóng góp.**
- **Phát hiện audit thật:** 96/527 gene trong `holdout_selection.txt` có **toàn bộ** tile nằm ở tập train, 3 gene giữ một phần → holdout **hiệu dụng 428 gene / 15.820 tile**. Nguyên nhân chưa xác định. Phải dùng số này khi so với Pearson 0,87 của tác giả.
- **Ba tầng dữ liệu:** bộ chính đã tải; bộ thứ hai (Zhang 2023, GPS-peptidome, GEO **GSE240610**, có 219 footprint saturation và residue quan trọng cho >5.000 degron → **ground truth XAI thực nghiệm**) **chưa tải**; bộ thứ ba MaveDB **100.514 phép đo độ dồi dào trên 9 gene** (đã truy vấn API; các bộ trong cùng gene chồng nhau, chưa khử trùng lặp).
- **Tiền lệ:** không được nói "đầu tiên" — đã có deepDegron, Degpred (BERT 2022), MetaDegron (PLM 2024), DegML, và **DEGRONOPEDIA (NAR 2024) là đối thủ trực tiếp ở tiêu chí 5**. Không tìm thấy ai dùng PLM trên bản đồ tile 2026 (chỉ vài lượt tìm web, chưa khảo sát hệ thống).
- **Còn dở:** (1) **cổng chặn** — thử tải GEO GSE240610, nếu không được thì bậc 2 và XAI sụp; (2) kiểm 9 gene MaveDB có nằm trong thư viện tile không; (3) chạy lại baseline PAP trên 428 gene holdout; (4) đọc toàn văn Methods bài 2026. Chưa chốt đề tài, chưa so với dark kinome và SIRT.
