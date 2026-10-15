# Nhật ký đề tài `degron-footprint`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../DECISIONS.md).

---

## 15/10/2026 (chiều) — bộ nhân Larsen: giấy phép đã qua, nhưng nó không cứu nhãn residue; và một tiền lệ thứ năm

Tài liệu: [research/larsen-nuclear-and-risks-2026-10-15/](research/larsen-nuclear-and-risks-2026-10-15/README.md), kèm sáu file ghi chép trong `notes/`. **Không huấn luyện mô hình nào.** Hai đề xuất mới ghi vào [DECISIONS.md phần C](../../DECISIONS.md): C-10, C-11.

- **Giấy phép bộ nhân Larsen: cổng chặn đã qua, và đường tải sạch hơn mong đợi.** Điểm mức tile **không** nằm sau CC BY-NC-ND của bài báo mà nằm trong repo GitHub `KULL-Centre/_2025_Larsen_degron_transcriptionfactors` dưới **giấy phép MIT** — một file `annotations/transfac_tiles.csv.gz` **5,77 MB** đã chú giải sẵn **PAP, ADPred, rASA, pLDDT**. Zenodo (cũng MIT) trả **403** từ mạng này; archive ERDA 120,79 GB **không có giấy phép nào** và không cần tới. **Không có deposit GEO/figshare** — đừng đi tìm mã GSE nữa. Chỗ mơ hồ duy nhất còn lại: MIT nominally là giấy phép phần mềm (đề xuất **C-11**: gửi một email xác nhận).
- **Nhưng nội dung bộ nhân bác bỏ kỳ vọng lớn nhất đặt vào nó.** Nó **không phải GPS** mà là sort-seq abundance reporter, tile **30-aa bước 15**, 4 cổng, thang PSI **đảo chiều** và chuẩn hoá lại (bảng GPS của đề tài có 6 bin). Nhãn **chỉ ở mức tile, chỉ trên trình tự hoang dã**: không bão hòa, không alanine scan, **không một nhãn mức residue nào**, và bài **không có một con số mức residue nào**. Reproducibility của nó (Pearson 0,97 giữa replicate) là **mức tile trên toàn dải động**, **không so được** với Jaccard 0,4965 mức residue của đề tài.
- **Và nó không phải test ngoại độc lập về trình tự: 1.583/1.626 (97,4%) TF của Larsen đã có trong peptidome GPS I28 của Zhang 2023**, còn **230/242** protein dùng chung với thư viện bào tương nằm trong **tập train của PAP** (tự đo, giao theo ký hiệu gene nên là **chặn trên**). Phải gọi đúng là **test chuyển assay / chuyển ngăn ở mức tile**. Rò rỉ thực tế thấp hơn con số đó gợi ý, vì nhãn footprint chỉ nằm trên bộ quét và bão hòa — ở đó chỉ **31,2%** TF có mặt, và HSF1, CRX, ZNF140, YBX1, NFE2L1 (ví dụ chính của Larsen) **không có**.
- **⚠ Hệ quả phải sửa: đường thoát ghi ở [bài 9](../../lectures/degron-basics/09-risks.md) rủi ro 1 không tồn tại.** Câu "bổ sung bộ nhân của Larsen 2025 nếu nhãn residue sụp" **đã sai** và đã sửa. Nó không nâng n, không cải thiện Jaccard, không thay mốc ΔPAP mức residue.
- **Nó vẫn giúp ba việc rẻ:** (1) test chuyển assay/chuyển ngăn mức tile với chú giải đã tính sẵn, mốc **PAP Pearson 0,79 / Spearman 0,80** do chính tác giả đo (so 0,87 trên holdout bào tương — ước lượng "chi phí chuyển ngăn"); (2) **chỗ duy nhất rASA/pLDDT có phương sai** (32% tile degron rASA > 0,7; 40% pLDDT < 70) ⇒ nơi kiểm được cổng phơi lộ ở mức tile, biến C-8 từ khẳng định thành số đo được; (3) hai phép so chưa tìm thấy ai làm — QCDPred ↔ thư viện nhân, và PAP tính lại trên ≈ 50.136 tile không chồng (đề xuất **C-10**).
- **⚠ Con số 58.781 không nhất quán trong chính bài báo** (các chỗ khác in 62.992 / 63.230 / 63.011 / 58.992). Đừng trích như con số dứt khoát; phải đếm dòng trong CSV.
- **TIỀN LỆ THỨ NĂM, và nó giết một claim: [Degformer](../../lectures/degron-basics/papers/degformer-2026.md)** (repo GitHub Apache-2.0, tạo 24/03/2026, **không bài báo**) huấn luyện trên **đúng** bảng S1+S4+S7 của Zhang, `MAX_LEN = 28`, và ship script xuất **ΔPSI trên 28 vị trí × 20 acid amin**. ⇒ Câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20" **phải bị xoá khỏi mọi tài liệu**. **Nhưng nó yếu ở đúng chỗ đề tài mạnh** (đọc toàn bộ mã nguồn + tự đo trên CSV nó ship): split `train_test_split(random_state=42)` **ngẫu nhiên thuần** với **4,09% rò rỉ trình tự y hệt** (2.330/56.927 dòng validation), **9.443** trình tự trùng mang **nhãn trái nhau**, đầu đọc **CLS token** (không có đầu mức residue; heatmap là 532 lượt forward), không cấu trúc, không trần nhãn, **tập blind vắng mặt** ⇒ con số headline **không tái lập được từ repo**, và ρ của nó rất có thể là **Pearson** (hàm duy nhất trong repo là `scipy.stats.pearsonr`), không phải Spearman. ⇒ **Cơ hội, không phải án tử**: baseline nên đánh bại dưới cov80.
- **Thêm hai tiền lệ nữa phải tính:** **DegronMD** (*MBE* 2023) là tiền lệ **đã công bố** có module đột biến mà repo bỏ sót; và **[LeBlanc 2026](../../lectures/degron-basics/papers/leblanc-2026.md)** (*Cell Systems* 17(9):101701) hạ **ba lập luận hỗ trợ** xuống "thực hành chuẩn" (tách abundance/function trên thư viện tile, split cụm protein phân cấp, đối chiếu trần replicate bằng số 0,555 so 0,568). **Và hai câu trong tài liệu repo sai:** MetaDegron và DegronMD **đều có batch submission** nên "batch" không phải điểm khác biệt G3.
- **Rủi ro khoa học mới từ LeBlanc 2026:** với 30 seed × 200 bootstrap họ kết luận *"composition is more important than individual positions"* và filter *"not picking up on specific protein motifs"*. Nếu đúng cho tile degron thì mô hình mức residue có thể đang **khớp nhiễu vị trí**. Họ cho luôn khuôn kiểm: báo độ ổn định trọng số theo vị trí qua seed/bootstrap.
- **Kết quả âm "siết read 10 → 200" nay là phát hiện có trích dẫn.** **DiMSum** (*Genome Biol* 2020) phân rã phương sai thành hai số hạng `m/N` **cộng một số hạng `a` không phụ thuộc số đọc**, và viết thẳng *"increasing sequencing coverage will not lead to reductions in the measurement errors"*, thuốc chữa là *"increasing the number of replicate experiments"*. **Enrich2** (*Genome Biol* 2017) cho mũi độc lập mạnh hơn vì là kết quả thực nghiệm: trên domain C2, lọc theo input count cho điểm **tương đồng *xấu hơn*** tập không lọc. ⇒ Đừng thử lại hướng ngưỡng read; muốn giảm nhiễu thì thêm replicate.
- **Phép tính Spearman–Brown lượng hoá "nhãn lặp một nửa":** độ tin cậy một replicate `ρ₁ ≈ 0,241`, trung bình hai replicate `ρ₂ ≈ 0,388` ⇒ trần Pearson của phần ngữ cảnh học được là **0,295** so với một replicate và **0,374** so với trung bình hai (**+27% tương đối**). Nhưng (a) đó là **bộ quét**; trên bộ bão hòa (nhiễu 16,7%) lợi ích chỉ **≈ +4,5%**, và (b) việc dùng trung bình hai replicate **đã chốt** ở [D-025](../../DECISIONS.md#d-025) mục 3 ⇒ con số này để **biện luận**, không phải để quyết.
- **Đơn vị suy luận là cụm protein, không phải peptide.** Bỏ qua lồng nhau cho tỉ lệ dương giả **trên 45%** ở mức danh nghĩa 5% (Saravanan, Berman & Sober) ⇒ con số cần báo ở bộ bão hòa là **số cụm**, không phải 91; và mức chênh tối thiểu phát hiện được ở n = 91 là **≈ 0,071**, nên **phần lớn ablation (0,02–0,05) sẽ không phân biệt được** — nên cam kết trước điều đó.
- **Tính mới của cổng phơi lộ co lại thành một ablation bắt buộc.** Yang và cộng sự (*PLOS Comput Biol* 22(8):e1014552, 2026) dùng **rASA làm đặc trưng node đầu vào** cộng **attention pooling với vector truy vấn học được** — không phải cổng theo độ lộ, **nhưng** pooling học được trên node đã chứa rASA là **tập mẹ** của cổng đặt tay. ⇒ Không được dựa vào "chưa ai đặt độ lộ gần bước gộp"; phải chạy **ablation ô chéo** (pooling học được ± rASA × cổng tường minh ± rASA) — đúng ô mà chính họ để trống.
- **Tín hiệu thời điểm tốt nhất của phiên:** **không tìm thấy công cụ dự đoán degron mới nào công bố 2025–2026** — PubMed 41 bản ghi, Europe PMC 100 + 127 hit, đọc tiêu đề từng cái; và trong **19 bài trích** Larsen 2025 (9) + Voutsinos 2026 (11), **không bài nào** là mô hình dự đoán degron hay footprint mức residue. Phải viết đúng dạng "đã chạy truy vấn X ngày 15/10, không tìm thấy".
- **Hub học `degron-basics/` đã cập nhật:** [bài 9](../../lectures/degron-basics/09-risks.md) (cả bảy rủi ro, mỗi rủi ro thêm phần "mới 15/10" + cách xử lý xếp theo chi phí + "điều vẫn có thể giết nó"; bảng nợ kỹ thuật từ 5 lên 12 dòng), [papers/larsen-2025.md](../../lectures/degron-basics/papers/larsen-2025.md) (viết lại phần dữ liệu + giấy phép), hai file mới [degformer-2026.md](../../lectures/degron-basics/papers/degformer-2026.md) và [leblanc-2026.md](../../lectures/degron-basics/papers/leblanc-2026.md), [papers/README.md](../../lectures/degron-basics/papers/README.md) (13 → 15 công trình, bảng giấy phép tách "bài báo" khỏi "dữ liệu"), README hub (khối cập nhật mới, danh sách "đừng nói sai" từ 5 lên 8 mục).
- **Chỗ chưa kiểm được, không được dùng để lập luận:** toàn văn Wang & Zheng (*Nat Chem Biol* 2025-11, "degrons beyond short linear motifs") **bị paywall** — chỉ đọc được tóm tắt, và nó là **rủi ro phạm vi** cho khung 28-mer; chồng lặp ở **mức trình tự** (tile 30-mer chứa trọn peptide 23-mer) **chưa đo**; ~60.600 ký tự cuối của toàn văn Larsen chưa đọc; mức xuất ra của **DegPred** vẫn chưa xác minh.

---

## 15/10/2026 — lập luận lại đề tài, và một lỗi lập luận bị phát hiện

Tài liệu: [research/topic-argument-2026-10-15.md](research/topic-argument-2026-10-15.md), thay mạch cũ ở [topic-decision.md](research/topic-decision.md) (11/10). **Không huấn luyện mô hình nào.** Ba đề xuất ghi vào [DECISIONS.md phần C](../../DECISIONS.md): C-7, C-8, C-9.

- **Lỗi lập luận quan trọng nhất, tự phát hiện: cổng phơi lộ không huấn luyện được trên nhiệm vụ chính.** Toàn bộ nhãn huấn luyện là **peptide 28-mer tách rời gắn vào đầu C của GFP**, nên **mọi peptide phơi lộ như nhau** và rASA/pLDDT **không có phương sai** — tham số của cổng **không nhận diện được** từ dữ liệu. Ba báo cáo trước đều không thấy điều này. Hệ quả: thành phần 4 hạ xuống **cơ chế chuyển giao**, ra khỏi đường găng của G2, và **không dành tuần 7–8 cho nó** (đề xuất **C-8**).
- **Lý lẽ kỹ thuật chính đổi sang ngữ cảnh vị trí**, nơi có bằng chứng đo được: đổi kernel 1 → 7 cho **+0,1311** precision@3 mức residue so với chỉ **+0,0032** Pearson trên điểm đoạn — **gấp ~41 lần**. Trần "+0,0032" mà chính tác giả đo **không chuyển sang** nhiệm vụ mức residue. Đây là bằng chứng dương đầu tiên của repo cho hướng mô hình có ngữ cảnh.
- **Cách kể chuyện về PAP được sửa cho đúng.** ΔPAP thua baseline thành phần không phải vì PAP tồi mà vì nó **được huấn luyện cho điểm cả đoạn**, không cho ảnh hưởng đột biến theo vị trí. Câu dẫn nhập đúng và mạnh hơn: **chưa có mô hình nào được huấn luyện cho đúng nhiệm vụ này**. Bốn tiền lệ đều xuất ở mức peptide/motif — đã kiểm, kể cả MetaDegron-D chỉ dùng trình tự.
- **Đề xuất chuyển chỗ đặt đóng góp** từ "kiến trúc mới" sang "**benchmark mức residue đầu tiên** + mô hình thắng trên nó" (**C-7**). Lý do: [D-022](../../DECISIONS.md#d-022) đã cho phép đóng góp dạng công cụ; tính mới kiến trúc đã bị thu hẹp **bốn lần**; còn bộ trần nhãn + baseline + đối chứng + lực + split thì **đã đo xong** và không bài nào trong sáu bài đã đọc có. Rủi ro nhận kèm: [D-012](../../DECISIONS.md#d-012) vẫn đòi đóng góp dương, nên mô hình vượt 0,4897 **vẫn bắt buộc**.
- **Đề xuất đổi thước đo ma trận từ Spearman sang AUROC mức ô** (**C-9**): trần nhãn Spearman chỉ 0,6989 còn trần AUROC đạt 0,9519, và nhiệm vụ của đề tài là tách ô dương chứ không phải xếp hạng mọi ô. Dư địa AUROC **0,1827** lớn hơn dư địa bộ quét (0,1617) trên nhãn ít nhiễu hơn nhiều.
- **Hub học `degron-basics/` đã viết lại theo mạch mới:** bài 5 (bảng mốc mới + hai mục 5.1/5.2 mới), bài 6 (mục 3 viết lại hoàn toàn để hạ cổng phơi lộ), bài 7 (bậc 3 thành bậc chính, AUROC, n = 91), bài 8 (câu đóng góp mới + lý do chuyển tính mới), bài 9 (rủi ro 4c mới, bảng thu hẹp tính mới thêm 3 dòng), README (5 thay đổi lớn, bảng mốc mới, danh sách "đừng nói sai" từ 3 lên 5 mục).
- **Mốc tuần 6 là 16/10** (buổi gặp 1 là 02/10, tuần 4) — tính ra ngày mai, và buổi gặp **chưa định ngày**. Tài liệu trình bày vẫn **chưa sửa** theo yêu cầu của Trọng ngày 14/10.

---

## 14/10/2026 — kiểm lại baseline PAP, chạy đối chứng ΔPAP, kiểm tiền đề cổng phơi lộ

Báo cáo: [research/pap-baseline/](research/pap-baseline/README.md) và
[research/architecture-check/](research/architecture-check/README.md). **Không huấn luyện mô hình nào.**

- **Trọng xác nhận C-6** (bảy đề xuất audit 13/10) → [D-025](../../DECISIONS.md#d-025), và **chấp nhận không có đề tài dự phòng** → [D-026](../../DECISIONS.md#d-026). Mốc G2 từ nay là baseline thành phần **0,4897** kèm trần nhãn **0,6514**; nguồn nhãn chính là **bộ bão hòa**.
- **Tái lập PAP khớp tuyệt đối** sau khi tải lại repo @`9b3eafa6`: kênh nội 0,8239, đầy đủ 0,8690, `cnn2w7` 0,8722 — trùng bốn chữ số với phiên 11/10 **và** khớp hai số công bố (0,82 / 0,87). Đóng việc còn thiếu của audit 13/10.
- **Đối chứng ΔPAP, chưa ai chạy trước đây:** trên nhãn footprint bộ quét, ΔPAP `cnn2w7` đạt precision@3 **0,4270**, `cnn2w1` 0,2959 — **thấp hơn baseline thành phần 0,4884**, kiểm ghép cặp p ≈ 6 × 10⁻¹⁹. Nên mốc 0,4897 của D-025 là mốc khó hơn ΔPAP và đúng để cam kết.
- **Bằng chứng dương đầu tiên cho trục "thêm ngữ cảnh cục bộ":** `cnn2w1` → `cnn2w7` chỉ +0,0032 Pearson trên thang điểm khối (chính tác giả đo), nhưng **+0,1311** precision@3 trên nhiệm vụ residue. Trần "+0,0032" **không áp được** cho thang đo của đề tài.
- **Không có rò rỉ từ tập train PAP:** 0,4268 (protein có trong train) so với 0,4270 (không có). Nên ΔPAP dùng được làm đối chứng toàn tập test.
- **Việc chặn mới, phát hiện ngoài dự tính:** bộ bão hòa sau khi áp đúng ngưỡng peptide degron (PSI WT ≤ 3,0) chỉ còn **91 peptide**, không phải 235. D-025 đề xuất 2 kèm điều kiện tính lại lực; cỡ mẫu thật để tính là **91**. Đường ra nếu thiếu lực: nới ngưỡng lên 3,5 (141 peptide) hoặc chấm mức ô.
- **Thước đo cho ma trận nên là AUROC, không phải Spearman:** trần nửa-chấm-nửa là Spearman 0,6989 so với **AUROC 0,9519**; ΔPAP đạt AUROC 0,7692 nên dư địa 0,1827. Gộp 19 thay thế lên mức vị trí làm Spearman tăng 0,3553 → 0,4130.
- **Tiền đề cổng phơi lộ đúng, hiệu ứng mạnh.** Trên 33.718 biến thể missense của 6 protein bào tương MaveDB kèm AlphaFold v6: Spearman(ΔPAP, độ dồi dào) đi từ **−0,1928** ở residue chôn lên **+0,3733** ở phơi lộ ≥ 0,7; theo pLDDT còn mạnh hơn (−0,1642 ở ≥ 90 lên **+0,3973** ở < 50). Hệ số tương tác ΔPAP × rASA **+0,6625**, bootstrap [0,627; 0,700]. Bỏ PRKN ra vẫn còn **+0,5990** [0,546; 0,648].
- **ΔPAP đổi dấu ở residue chôn** — mô hình degron không có cấu trúc sai dấu ở 47% residue. Cổng phơi lộ không chỉ tăng điểm, nó sửa một lỗi hệ thống. **pLDDT phân tách mạnh hơn rASA** nên nếu chỉ chọn một thì chọn pLDDT (cũng rẻ hơn).
- **Ràng buộc thiết kế mới cho nhiệm vụ phụ:** PSI hoang dã Zhang so với điểm tile Voutsinos cho Spearman 0,7333 toàn cục nhưng chỉ **0,2921** trong nhóm peptide degron → nhãn đoạn phân biệt "có degron hay không" tốt, phân biệt **mức độ** kém. Nhiệm vụ phụ nên là **phân loại**, không phải hồi quy ngang hàng.
- **Rò rỉ chéo nhiệm vụ phải ghi vào benchmark:** 725/770 peptide footprint có tile trong tập train của PAP (dù đo ra không có lợi thế nào).
- Hai tiền đề kiến trúc **vẫn chưa kiểm được** vì cần huấn luyện: cấu trúc túi so với đầu hồi quy theo vị trí, và PLM mức residue so với one-hot.
- Phát hiện vận hành: **AlphaFold DB trả 403 nếu không có User-Agent**; thêm `-A "Mozilla/5.0"` thì tải được. 8 cấu trúc kèm SHA-256 ở `data/raw/alphafold/manifest.txt`.
- **Tra y văn cho cổng phơi lộ (cùng ngày, sau phép đo) — và nó sửa lại kết luận:** [prior-art-exposure-gate.md](research/architecture-check/prior-art-exposure-gate.md). **Tiền đề không mới**: Voutsinos 2026 (ρ = −0,47; Kruskal–Wallis P = 5,4 × 10⁻⁶), Larsen 2025 (\|r\| 0,41 với rASA), QCDPred, DEGRONOPEDIA, JoGo đều đã báo. **Hiện tượng đổi dấu cũng đã có người tìm ra**: Larsen 2025 báo ΔPAP Pearson **0,54** ở IDR của CRX so với **−0,19** ở homeodomain đã gấp. Phép đo của repo là xác nhận lại ở quy mô lớn hơn trên nhãn độ dồi dào, **không phải phát hiện** — đã sửa câu nói quá trong báo cáo và thẻ đề tài.
- **Tìm được tiền lệ phương pháp sát nhất, và nó là baseline bắt buộc:** [Schulze & Lindorff-Larsen, *eLife* 2026](https://doi.org/10.7554/eLife.103721) (cùng nhóm Voutsinos), gộp **6 thí nghiệm VAMP-seq / 31.614 biến thể** trên **đúng 6 protein** mà repo dùng, tách chôn/phơi lộ ở ngưỡng rASA **0,1**, dựng ma trận thay thế theo lớp, đối chứng ThermoMPNN ΔΔG. **rASA một mình cho Spearman 0,45** — mạnh hơn ΔPAP ở khoảng phơi lộ nhất (0,3733). Ghi chú: [schulze-2026.md](../../lectures/degron-basics/papers/schulze-2026.md).
- **Bài đó phát hiện hai lỗi phương pháp của phép đo 14/10:** (a) bộ **GCK** dùng trong tập đo bằng **DHFR-PCA**, không phải VAMP-seq — trộn hai phenotype; (b) **NUDT15 và ASPA là homodimer**, rASA tính trên AlphaFold monomer phân loại sai residue ở mặt tiếp xúc. **Con số hệ số tương tác +0,6625 chưa dùng được** cho tới khi chạy lại.
- **Nhưng Schulze 2026 tự nêu khoảng trống đúng là hướng đề tài:** framework cấu trúc của họ không bắt được **neo-degron ở vị trí phơi lộ**, và họ mời đưa vào "đặc trưng sinh hóa phức tạp hơn". Kèm ca cụ thể **PRKN S109** — residue phơi lộ có profile thay thế giống residue chôn. Dùng làm dẫn nhập.
- **Nơi đặt cổng vẫn chưa tìm thấy tiền lệ:** PAP dùng cấu trúc chỉ để phân tích sau; **MetaDegron-D chỉ dùng trình tự** (khả năng tiếp cận dung môi từ Spider2 chỉ vào nhánh XGBoost, không có attention, chỉ max-pooling); DEGRONOPEDIA dùng ở bước annotation; Schulze 2026 dùng để chia lớp. Ghi là **chưa tìm thấy**, không phải "chưa ai làm", và tính mới của đề tài **không nên** dựa chính vào điểm này.
- Sửa mâu thuẫn trong thẻ đề tài: nhãn mức residue được gọi là "rủi ro số hai" ở một chỗ và "nay là rủi ro số một" ở chỗ khác.

---

## 13/10/2026 — tải đủ bốn nguồn dữ liệu; dựng PSI cho mọi điều kiện; **đo được trần nhãn và lực thống kê**

Báo cáo đầy đủ: [research/full-data-audit/](research/full-data-audit/README.md). Không huấn luyện mô hình nào.

- **Tải đủ:** Mendeley cả **5/5** file (trước có 2), GEO GSE240610, repo Voutsinos @ `9b3eafa6` (trước **đã mất khỏi máy**), 26 score set MaveDB. SHA-256 khớp checksum Mendeley công bố. Zenodo `16925278` trả 403 từ mạng này. Manifest: `data/raw/full-download-manifest.json`.
- **Dựng PSI từ read thô cho mọi điều kiện**, thứ repo chưa từng có: Replicate 2, mẫu BAG6 WT, và cả hai nửa bão hòa. Công thức suy ra và kiểm trên **261.865** giá trị của Replicate 1, lệch ≤ **5,0 × 10⁻⁷**. Tái lập đúng **2.624** footprint.
- **Lỗi trong pipeline công bố của Zhang 2023:** script gộp đọc `header=TRUE` trên file count không có header nên **ăn mất dòng đầu của cả 6 file**; lan cả vào hệ số chuẩn hóa. Ảnh hưởng nhỏ (3 định danh, không có footprint nào) nhưng phải mô phỏng lại mới khớp số tác giả.
- **Rủi ro số hai đã đo được.** ΔPSI rep1 vs rep2 Pearson **0,7229**; nhiễu một replicate SD **0,2974**. Footprint lặp lại ở mức peptide **89,3%**, nhưng **mức vị trí Jaccard chỉ 0,4965** — tức *residue nào* là footprint chỉ lặp lại khoảng một nửa, và đó chính là thứ đề tài dự đoán. Phân rã lại cùng cơ sở macro: dư sau oracle 0,3612, **75,9% là nhiễu**, ngữ cảnh học được cận trên chỉ **0,0872** (không phải 35%). Quét ngưỡng reads 10→200 cho thấy **nhiễu không phải tạo tác của ngưỡng**.
- **Trần thực nghiệm do nhãn đặt ra:** rep1 chấm trên nhãn rep2 cho precision@3 **0,6514**. Baseline thành phần **ước lượng trung thực** chỉ **0,4897**, không phải 0,6045 — cả 0,6045 và 0,7792 đều là oracle đọc nhãn test. Dư địa thật **0,1617**, không phải 0,1747 theo cách đọc cũ.
- **Việc chặn đã trả lời: tập test đủ lực.** Kiểm ghép cặp, SD đo thật 0,2416, d_z 0,669. So baseline trung thực: cần **18** peptide, lực ≈1,00. So mốc 0,6045: cần **209**, lực **0,82–0,94** ở n = 221–322 — đạt nhưng sát biên ở cov50, nên **nên dùng split cov80**.
- **Bộ bão hòa tốt hơn bộ quét trên mọi trục**, và là nguồn duy nhất cho ma trận 28×20: nhiễu chiếm **16,7%** (so 75,9%), ΔPSI giữa hai nửa Pearson **0,8335**, Jaccard ô dương **0,6596**, ma trận phủ **97,9%** của 28×19 trên **235** peptide. Nhưng bộ này **không có phép đo hoang dã nào** — giải bằng ô đồng nghĩa (amino acid thay vào trùng WT) làm WT nội tại, 28 ô/peptide, SD trong peptide 0,031; quy tắc tile (28-mer, bước 23) khớp **128/130** trình tự thật. **130/248** peptide có cả hai nguồn nhãn nên phải cùng phía train/test.
- **Phát hiện ảnh hưởng tới G3:** file Mendeley 393 MB lần đầu tải chứa **mô hình học máy của chính nhóm Zhang** dự đoán PSI toàn peptidome (Pearson **0,8955** ở 10% train, RMSE 0,563 trên 260.989 peptide). Thẻ đề tài trước chỉ biết DEGRONOPEDIA, MetaDegron, PAP. Khác phạm vi (peptide so với residue) nên không phải đối thủ trực tiếp, nhưng phải nêu.
- Nhiễu ~0,30 được xác nhận **bốn lần độc lập**: quét 0,2974, bão hòa 0,2645, peptidome 0,3357, và chính tác giả ghi 0,239 ⇒ tính chất của assay GPS. MLN4924: chỉ **0,76%** peptide bền lên ≥1 PSI khi chặn CRL. MaveDB: **76.194** biến thể duy nhất (ước lượng cũ từ metadata 69.209).
- **Mẫu BAG6 WT không trộn được** với hai replicate kia: ΔPSI chỉ tương quan 0,56–0,58 (so 0,72 giữa hai replicate) và lệch hệ thống −0,11 PSI.
- Bảy đề xuất ghi vào [DECISIONS.md](../../DECISIONS.md) phần C (C-6), **chờ Trọng xác nhận** — gồm sửa cách phát biểu mục tiêu G2 và chuyển trọng tâm nhãn sang bộ bão hòa.
- **Hub học đã đồng bộ:** thêm [bài 10 "Dữ liệu thật trông như thế nào"](../../lectures/degron-basics/10-data-up-close.md) (mô tả dữ liệu dễ hiểu: một dòng gồm gì, PSI tính ra sao, dữ liệu tốt đến đâu) kèm 2 sơ đồ mới. Đồng thời chèn ghi chú cập nhật vào bài 4, 5, 7, 9 và thẻ README của hub, vì các bài đó đang ghi mốc 0,6045 / dư địa 0,1747 và "rủi ro số một là lực thống kê" — nay đều đã lỗi.

---

## 12/10/2026 (tiếp) — tạo hub markdown đơn giản giải thích đề tài

- **Yêu cầu của Trọng:** đọc lại hub HTML ở [lectures/degron-footprint/](../../lectures/degron-footprint/index.html) thấy quá khó hiểu và phức tạp. Cần một hub markdown đơn giản, từ khái niệm cơ bản nhất đến đóng góp, mỗi phần quan trọng có hình, mỗi bài báo một file riêng, trích dẫn dẫn link ngay tại chỗ liên quan.
- Tạo [lectures/degron-basics/](../../lectures/degron-basics/README.md): **9 bài** (khái niệm → cách đo → bài toán → dữ liệu → khoảng trống → giải pháp → đánh giá → đóng góp → rủi ro), **14 sơ đồ tự dựng** dạng SVG, **12 file bài báo** + chỉ mục. Tổng 38 file. Hub HTML cũ giữ nguyên, hai bản trỏ lẫn nhau.
- Nội dung không viết mới mà **rút từ các báo cáo audit đã có**; mỗi con số dẫn link về nguồn gốc trong `research/`. Giữ nguyên nhãn bằng chứng và toàn bộ quy ước ngôn từ của đề tài (không nói "chưa ai dùng MIL", không nói "dùng cấu trúc là phần mới", không nói bản đồ mô hình thành phần phải phẳng, không hứa cải thiện 0,1747).
- Mỗi sơ đồ mang nhãn `SƠ ĐỒ TỰ DỰNG` ở góc trên phải theo quy ước trong [NOTICE.md](../../lectures/degron-footprint/assets/figures/NOTICE.md), để không lẫn với hình của tác giả bài báo. Sơ đồ kiến trúc MIL-Degron mang thêm nhãn `ĐỀ XUẤT, CHƯA KIỂM CHỨNG`.
- Thêm một dòng trỏ tới hub mới trong [lectures/index.html](../../lectures/index.html). Kiểm: 14 SVG hợp lệ XML, mọi hình được tham chiếu đều tồn tại và mọi hình đều được dùng, `check_links.py` không sinh link hỏng mới.

---

## 12/10/2026 (tiếp) — degron được chốt làm **đề tài chính** ([D-023](../../DECISIONS.md#d-023))

- Trọng chốt: degron là đề tài chính, [`plm-calibration-audit`](../../archive/topics/plm-calibration-audit/README.md) (A4) là dự phòng. Kèm thông tin mới: **GVHD vẫn chấp nhận đóng góp dạng công cụ** ([D-022](../../DECISIONS.md#d-022)), nên rào cản C-3 với nhóm A được gỡ.
- Căn cứ chọn degron, tóm từ [khảo sát 7 ứng viên](../../surveys/seven-candidates-comparison-2026-10-12.md): degron là ứng viên **duy nhất có khoảng trống đã chứng minh** chứ không phải "chưa kiểm" — 89,7% peptide (2.353/2.624) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần bị **chứng minh** không tách được. Thêm: G1 mạnh nhất repo; TC4 (XAI) thỏa mãn bởi chính bài toán vì đầu ra là điểm quan trọng theo residue; có kiến trúc để đề xuất (mục 6 của audit); dữ liệu đã trên máy nên khả thi trong 8–9 tuần.
- **Sửa thẻ trạng thái:** dòng G2 trước đây viết "dư địa chỉ 0,1747" làm đề tài trông yếu hơn mức bằng chứng cho phép. Đã viết lại theo đúng số của [audit](research/composition-context-audit.md): cận chính xác 0,6045 cho lớp mô hình thành phần, oracle không ràng buộc 0,7792, ngẫu nhiên 0,1204, tức +28,9% tương đối nếu đạt trần. Câu "G2 chưa xác lập" **giữ nguyên** vì chưa huấn luyện mô hình nào.
- Dòng G3 cũng được sửa cho đúng: **ba** sản phẩm đã tồn tại (DEGRONOPEDIA, máy chủ web MetaDegron, Colab nhóm PAP), không phải hai. Ứng dụng phải khác biệt được; chỗ khác biệt khả thi là ma trận 28×20 trên nhãn thực nghiệm.
- **Việc chặn gần nhất:** tính lực thống kê trên tập test 221–322 footprint trước khi cam kết huấn luyện. Chưa chạy.

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
