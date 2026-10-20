# Quyết định và phạm vi đề tài: footprint degron ở mức residue

> **Đề tài chốt ngày 11/10/2026, tái định tâm cùng ngày (khuya)** sau khi qua cổng chặn số 2. Slug giữ nguyên `degron-e3-specificity` để không vỡ liên kết, nhưng **trục đề tài đã đổi** — xem mục 1 và mục 2.1. Chưa có phê duyệt chính thức của GVHD; cần báo cáo ở buổi tuần 6.

> **Audit 12/10/2026:** [báo cáo thành phần–ngữ cảnh](composition-context-audit.md) đã lượng hóa giới hạn của score thành phần: cận kỳ vọng precision@3 **0,6045**, oracle không ràng buộc **0,7792**; 2.046/2.624 footprint có cùng cặp thay thế nhưng chênh ΔPSI ≥1. Test thử theo cụm protein identity 30%, coverage hai chiều 50%, chỉ giữ peptide khớp tham chiếu còn **221–301 footprint** qua 5 seed. Phương án ma trận thay thế trong báo cáo là **đề xuất đang khảo sát**, chưa thay kiến trúc hoặc tên đề tài ở tài liệu này. Các trang trình bày cũ chưa được đồng bộ toàn bộ với audit mới.

## 1. Tên đề tài

**Dự đoán footprint degron ở mức residue bằng học đa thể hiện với cổng phơi lộ cấu trúc, trên nhãn đột biến thực nghiệm.**

Tên cũ — *"Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc"* — **đã bỏ ngày 11/10/2026 (khuya)**, vì phép đếm nhãn ở mục 2.1 cho thấy chỉ có **một** lớp E3 đủ mẫu để huấn luyện.

- Trang trình bày (mở bằng `file://`): [presentation.html](../presentation/presentation.html)
- Báo cáo kiểm chứng chi tiết: [../../../common/deep-research/reports/degron-topic-report/index.html](topic-report/index.html)
- Audit bản đồ tile và mô hình PAP: [../../../common/deep-research/research_notes/degron/](voutsinos-2026-audit/)
- **Audit nhãn E3 và nhãn theo residue** (vòng quyết định việc tái định tâm): [../../../common/deep-research/research_notes/degron-e3-labels/](e3-labels-audit/README.md)

## 2. Vì sao đề tài có hình dạng này

Mọi con số dưới đây là **tự đếm từ dữ liệu thô**, không dẫn lại từ bài báo.

1. **Kênh nội PAP cnn2w1 không dùng thứ tự residue.** Đảo thứ tự cho Pearson(gốc, đảo) = **1,000000**. Đây là tính chất của kênh nội dựa thành phần, không phải toàn bộ PAP có kênh C-terminal. PAP đầy đủ được tái lập ở Pearson 0,869. ΔPAP vẫn dự đoán được ảnh hưởng thay thế; trong cùng peptide, mô hình thành phần chỉ bắt buộc cho cùng giá trị ở các vị trí có cùng cặp (WT, replacement).
2. **Lợi ích của bản đối chứng bắt motif nhỏ trên điểm toàn đoạn.** `cnn2w7` chỉ hơn **+0,0032 Pearson** trong cấu hình đã tái lập. Điều này chưa chứng minh thang đo bão hòa hoặc mọi kiến trúc có ngữ cảnh đều không thể cải thiện.
3. **Nhãn khu trú có phần vượt biểu diễn thành phần.** Có **2.624 footprint**, **2.402 khu trú**, median 3 vị trí quan trọng. Audit mới cho thấy **2.046** peptide có vị trí cùng cặp thay thế nhưng chênh ΔPSI ≥1. Đây là khác biệt nhãn quan sát, chưa tách phần ngữ cảnh có thể học khỏi nhiễu thực nghiệm.
4. **Nguồn nhãn theo vị trí:** **256.711 dòng** có PSI và reads ≥10 từ quét, cộng **135.040 định danh** trong thư viện bão hòa của 249 peptide. Bão hòa còn cần tính/curate score; không gọi mọi định danh là một ΔPSI đã xác nhận.

### 2.1 Cổng chặn 2 đã đóng, và nó buộc đổi trục

Đếm từ MAGeCK thô ([ghi chú và 7 script](e3-labels-audit/README.md)):

|                                   |                        Số đếm |
| --------------------------------- | -------------------------------: |
| Screen CRISPR                     |                     **31** |
| Gán được adaptor              |      27 (gán **rõ**: 25) |
| **Số E3 khác nhau**       |                     **10** |
| **Số E3 có ≥ 5 peptide** | **1** (KLHL15, 13 peptide) |
| Số E3 có đúng 1 peptide       |                                6 |

Bền với **36 tổ hợp ngưỡng**: gán được 16–29, số E3 8–10, và số E3 có ≥ 5 peptide **luôn đúng bằng 1**.

**Hệ quả:** bỏ thành phần điều kiện E3 khỏi kiến trúc, và bỏ "đặc hiệu E3" khỏi vị trí thước đo chính. E3 còn lại ở vai trò **ca nghiên cứu** trên 23 peptide có cả nhãn E3 và bản đồ đột biến bão hòa (giao của hai tập 27 peptide, không phải 27 peptide đồng thời).

## 3. Phạm vi

**Trong phạm vi:** protein người, trọng tâm bào tương và peptide của sàng lọc GPS; dự đoán **bản đồ độ nhạy đột biến theo từng residue** của một đoạn peptide; huấn luyện và đánh giá trên nhãn đột biến thực nghiệm; một ứng dụng web; một ca nghiên cứu E3 ở quy mô nhỏ.

**Ngoài phạm vi, phải nói rõ trong luận văn:**

- Không dự đoán protein có thực sự bị phân hủy nhanh trong một tế bào cụ thể (còn phụ thuộc E3 nào được biểu hiện, chaperone, định vị dưới tế bào).
- **Không dự đoán E3 nào nhận ra degron.** Chỉ có 10 E3 có nhãn và 6 trong số đó có đúng một peptide, nên đây là ca nghiên cứu, không phải nhiệm vụ dự đoán.
- Không thay thế mô hình dự đoán độc tính biến thể; chỉ bổ sung cơ chế.
- Nhãn là peptide **tách rời**, không phải protein nguyên vẹn.

## 4. Bộ dữ liệu, đã tải và tự đếm

|                       | Bộ 1 — bản đồ bào tương                          | Bộ 2 — đột biến quét                                 | Bộ 3 — đột biến bão hòa                                           | Bộ 4 — biến thể protein nguyên vẹn |
| --------------------- | -------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| Nguồn                | Voutsinos 2026, *Sci Adv*                              | Zhang 2023, Mendeley `32h94v2yv2`                        | cùng nguồn                                                             | MaveDB (API)                             |
| Vai trò              | **Nhãn yếu, mức đoạn** (nhiệm vụ phụ trợ) | **Nhãn mạnh, mức residue** — huấn luyện chính | **Kiểm tra độ phân giải cao sau xử lý score và chia tập** | Kiểm tra trên protein nguyên vẹn     |
| Số phép đo         | 212.658 đoạn                                           | **256.711** (PSI, reads ≥ 10)                       | **135.040 định danh; chưa phải số score đạt lọc**          | 69.209 biến thể duy nhất              |
| Đơn vị nhãn       | một điểm cho cả đoạn                               | ΔPSI theo **từng vị trí**                        | ΔPSI theo **vị trí × 19 thay thế**                            | độ dồi dào protein                   |
| Peptide dùng được | 5.327 gene                                               | **2.624** có footprint (2.402 khu trú)             | **249** (239 phủ ≥ 27 vị trí)                                  | 9 gene                                   |
| Thang đo             | Điểm liên tục 0–1                                   | PSI 1–6                                                   | PSI 1–6                                                                 | Độ dồi dào                           |
| Giấy phép           | MIT                                                      | Mendeley công khai                                        | Mendeley công khai                                                      | CC0                                      |

Tập kiểm tra của bộ 1: **428 gene hiệu dụng / 15.820 tile**, tính từ dữ liệu — **không** dùng danh sách 527 gene công bố, vì 96 gene trong đó thực ra nằm hết ở tập huấn luyện.

Chồng lấn: **27/31 peptide CRISPR** có bản đồ đột biến bão hòa; 4 peptide thiếu là 4 peptide BAG6. Trong 27 peptide CRISPR **được gán E3**, chỉ **23** có bản đồ bão hòa: 4 peptide không gán E3 nhưng vẫn có bản đồ. Xem phép giao hai JSON trong [ghi chú audit](e3-labels-audit/README.md). 130/248 peptide bão hòa có mặt trong bộ quét.

## 5. Kiến trúc đề xuất: MIL-Degron

GVHD **kỳ vọng một kiến trúc chưa ai dùng** (thông tin ngày 11/10/2026). Năm thành phần; thành phần điều kiện E3 của bản trước **đã bỏ**.

| # | Thành phần                                                                                                                 | Phép đo buộc phải có nó                                                                                                                             |
| - | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Mỗi vị trí sinh một cửa sổ ứng viên motif; peptide là một "túi" cửa sổ                                          | Mô hình hiện có bất biến hoán vị (Pearson gốc–đảo = 1,000000), còn footprint thật khu trú ở median 3/28 vị trí                          |
| 2 | Embedding PLM **mức residue**, không gộp trước                                                                    | Mọi mô hình degron đã công bố đều gộp trung bình hoặc dùng thành phần                                                                      |
| 3 | **Attention có cổng** trên các thể hiện, thay global average pooling                                             | Cấu trúc túi là chỗ nối **nhãn yếu mức đoạn** (212.658) với **nhãn mạnh mức residue** (256.711) trong **một** mô hình |
| 4 | **Cổng phơi lộ**: rASA và pLDDT nhân vào logit attention                                                         | Tác giả đo điểm chỉ tương quan độ dồi dào ở rASA > 0,7, nhưng chỉ dùng cấu trúc để phân tích sau                                    |
| 5 | Hai đầu ra, huấn luyện đa nhiệm: điểm khối (phụ trợ) và **bản đồ độ nhạy theo residue** (mục tiêu) | Nhãn đoạn nhiều; nhãn residue là thứ cần đo. Lợi ích nhãn phụ chưa được thực nghiệm                                                    |

**Hai điểm mới, phát biểu hẹp đúng mức:**

- **Cổng phơi lộ đặt ở chỗ gộp, không phải đầu vào.** Dự đoán trên peptide tách rời thì đặt cổng "phơi lộ hoàn toàn"; trên protein nguyên vẹn thì đặt rASA thật. Cùng một mô hình giải thích cả hai chế độ, tức khoảng cách tile-so-với-protein trở thành một tham số của mô hình.
- **Attention có thể được giám sát bằng nhãn đột biến theo residue**, nhưng trọng số attention và ảnh hưởng đột biến là hai đối tượng khác nhau. Không gọi nhãn đột biến là ground truth trực tiếp của attention hoặc coi đây tự nó là phương pháp mới; cần đối chứng và kiểm giá trị của cách nối hai đối tượng.

**Phải tự nói ra giới hạn của lập luận MIL.** Khi đã có nhãn ở mức residue thì một đầu hồi quy theo từng vị trí là mô hình tự nhiên, và MIL không còn bắt buộc. Lý do giữ cấu trúc túi là **để dùng được cả hai bộ nhãn trong một mô hình**: đầu khối gộp các thể hiện, đầu residue đọc thẳng từng thể hiện. Nếu phép thử cho thấy đầu hồi quy theo vị trí đơn thuần đã đủ, thì đó là kết quả phải báo, không phải thất bại cần che.

## 6. Thước đo

Thước đo chính **không phải** Pearson trên thang điểm khối. Ba bậc, khó dần:

1. **Tái lập baseline trên thang điểm khối.** 428 gene holdout hiệu dụng; PAP chạy lại đã đạt Pearson 0,8690. Bậc này để chứng minh chạy lại được, **không** để đặt đóng góp.
2. **Dự đoán bản đồ độ nhạy theo residue — thước đo chính.** Chia **theo peptide**, trên 2.624 peptide có footprint. Chỉ số: Spearman theo từng peptide giữa vector 28 chiều dự đoán và đo được; và **precision@3** — mô hình có đặt độ nhạy cao nhất đúng vào các vị trí quan trọng thật không (median 3 trên 28).
3. **Chuyển sang bản đồ thay thế đầy đủ.** 249 peptide bão hòa thô, cần xử lý score và mask ô không hợp lệ; không mặc định mọi peptide có đủ 28×19 nhãn. Có 130/248 peptide đạt reads trùng bộ quét nên cần giữ peptide/protein/cụm cùng phía trước khi gọi là tập kiểm tra. Nếu đề xuất ma trận dùng một phần bão hòa để train, phải chốt protocol mới và giữ riêng phần test.

**Đối chứng bắt buộc:** ΔPAP tính trên đúng thay thế thực nghiệm, mô hình thành phần và đầu hồi quy theo vị trí không MIL. Bản đồ của mô hình thành phần không bắt buộc phẳng; ràng buộc đúng là score trùng nhau ở các vị trí cùng cặp thay thế trong cùng peptide. Các oracle/cận ở audit 12/10 dùng nhãn đánh giá, không phải performance đã đo của các baseline này.

**Ca nghiên cứu E3, không phải thước đo:** 23 peptide có cả nhãn E3 và bản đồ bão hòa. Câu hỏi: footprint dự đoán có khớp motif của E3 đã biết không? Cả 13 peptide KLHL15 nằm trong giao này; vẫn cần lọc chất lượng nhãn và chia tập trước khi chấm ca nghiên cứu.

> **Vẫn phải thống nhất thước đo với GVHD trước khi bắt đầu.** Đổi gộp trung bình sang max trên **cùng trọng số đã học cho gộp trung bình** làm Pearson sụt **0,824 → 0,344**. Đây không phải so sánh công bằng với max pooling được huấn luyện lại, nên không suy ra kiến trúc khu trú sẽ thua hoặc không thể cải thiện điểm toàn đoạn. Thước đo chính đề xuất vẫn là bậc 2 và bậc 3 vì khớp câu hỏi footprint.

## 7. Ba cổng chặn — trạng thái cập nhật 11/10/2026 (cuối phiên)

1. **Đọc toàn văn bài degron transcription factor** (Larsen và cộng sự, [bioRxiv 05/2025](https://doi.org/10.1101/2025.05.16.654404)) — **ĐÃ QUA, theo hướng thuận.** Họ **không** mô hình hóa đặc hiệu E3, **không** đề xuất kiến trúc mới, **không** dùng nhãn E3 hay CRISPR, **không** có phần giải thích mô hình. PAP cùng ESM-1b chỉ dùng để so biến thể CRX; phần nhắc CRL4-DCAF12 và FEM1b nằm ở Thảo luận, là suy đoán theo y văn. Trục của đề tài còn trống.
   - **Hai điều chỉnh bắt buộc từ cùng bài:** họ đã tính rASA và pLDDT từ AlphaFold2 kèm DSSP, và đã làm bản đồ thay thế *in silico* ΔPAP cho mọi đột biến điểm trong một vùng của HSF1 → "dùng cấu trúc" và "giải thích biến thể" không còn là phần mới của đề tài.
   - **Bộ dữ liệu thứ tư, chưa tải:** thư viện nhân **58.781 đoạn có điểm / 1.626 TF**, cộng **8.645 đoạn / 234 protein** chồng lấn với thư viện bào tương. Là lựa chọn rẻ hơn cho bậc 2 (cùng assay, khác khoang tế bào). Tiền ấn CC BY-NC-ND nên phải kiểm điều kiện dùng dữ liệu trước khi đưa vào kế hoạch.
2. **Đếm nhãn E3 dùng được** — **ĐÃ QUA, và kết quả buộc tái định tâm đề tài.** Table S1–S7 trên PMC chặn bằng reCAPTCHA và Europe PMC trả *"not open access"*, nên lấy dữ liệu **thô** từ Mendeley Data `10.17632/32h94v2yv2.2` mà chính bài khai báo. Đếm từ MAGeCK: **31 screen → 27 gán được → 10 E3 → chỉ 1 E3 có ≥ 5 peptide**, bền với 36 tổ hợp ngưỡng. Thành phần điều kiện E3 **đã bỏ**; chi tiết ở mục 2.1 và [ghi chú audit](e3-labels-audit/README.md).
   - **Bù lại, phát hiện nhãn theo residue lớn hơn tài liệu trước ghi rất nhiều:** 256.711 phép đo đột biến quét, 2.624 peptide có footprint học được, 135.040 phép đo trên 249 bản đồ thay thế đầy đủ. Đây là nguồn nhãn của đề tài sau khi tái định tâm.
   - **Chưa lấy được Table S5** (gán E3 do tác giả curate, gồm cả "individual testing"), nên 10 E3 là **giới hạn dưới**. Không đổi kết luận: Table S5 chỉ thêm peptide, không đổi được việc 6 lớp có một mẫu.
3. **Tra tính mới của kiến trúc** — **ĐÃ CÓ CÂU TRẢ LỜI, và nó thu hẹp tuyên bố.** Chưa thấy ai dùng học đa thể hiện cho degron, phần đó giữ được. Nhưng [BioBlobs](https://arxiv.org/abs/2510.01632) (10/2025) đã dùng đúng attention-based MIL kiểu Ilse 2018 trên protein — túi là protein, thể hiện là cấu trúc con học được, có cổng attention — cho dự đoán chức năng; và [OmniESI](https://arxiv.org/abs/2506.17963) (2025) đã dùng điều biến có điều kiện hai chiều enzyme–cơ chất, cùng ý tưởng với FiLM. **Phát biểu đúng: mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, chưa thấy áp cho degron; không mới ở cơ chế.** Còn lại: tra danh sách trích dẫn bài 2026 và nội bộ MetaDegron.

### 7.1 Ba cổng bắt buộc G1/G2/G3, áp lại cho đề tài này

Ba điều kiện này đến từ [báo cáo chốt đề tài chính](../../../archive/topics/dark-kinome-zero-shot/research/main-topic-decision-2026-10-10.md). Lúc chốt degron ban đầu chúng chưa được áp; bảng dưới là lần áp lại sau đó. G2 vẫn cần kết quả mô hình footprint trên peptide chưa gặp mới xác lập được.

| Cổng                                                        | Kết quả                               | Căn cứ                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **G1** nhãn thực nghiệm hoặc chú giải độc lập | **ĐẠT, mạnh nhất trong repo** | Điểm tile từ reporter assay, PSI từ sàng lọc, 219 footprint từ đột biến bão hòa. Không nhãn nào do pipeline của đề tài sinh ra. So sánh: hướng senescence scRNA-seq trượt cổng này                                                                                             |
| **G2** đóng góp dương đo được                 | **CHƯA XÁC LẬP**               | Phần bằng chứng đã có (bất biến hoán vị, +0,0032, 0,824 → 0,344) là kết quả phê phán về baseline. Đóng góp dương mới phải đến từ dự đoán footprint mức residue trên peptide chưa gặp, vượt đối chứng hồi quy theo vị trí không MIL; mô hình ấy chưa chạy |
| **G3** ứng dụng hoặc website khả thi               | **ĐẠT, nhưng yếu nhất**      | **Ba** sản phẩm đã tồn tại, không phải hai: DEGRONOPEDIA (*NAR* 2024), máy chủ web MetaDegron, Colab của tác giả PAP                                                                                                                                                                |

### 7.2 Hai đối thủ, chưa có trong các tài liệu trước

- **MetaDegron** (*Briefings in Bioinformatics* 2024, [doi:10.1093/bib/bbae519](https://doi.org/10.1093/bib/bbae519)) — **đã dự đoán degron theo từng E3 cho 21 E3 ligase**, có máy chủ web với cây chọn E3, hiển thị cấu trúc và mạng tương tác. Nhưng huấn luyện trên khoảng **300 degron đã curate** từ ELM và y văn, âm tính là **peptide ngẫu nhiên**, chia 90/10, AUC 0,87–0,90, không kiểm soát đồng dạng. Kiến trúc: SeqVec kèm BLSTM và conv-pooling, cộng XGBoost trên 10 đặc trưng — trong đó **có** độ phơi lộ với dung môi và độ vô trật tự, nhưng ở **đầu vào**, không ở bước gộp.
- **ELITE** ([bioRxiv 11/2025](https://doi.org/10.1101/2025.11.05.686884)) và **E3TargetPred** — xếp hạng E3 cho một substrate ở **mức cặp protein–protein**, ProtBERT kiểu Siamese, Integrated Gradients. Nhãn dương từ mạng tương tác tổ chức theo mô, nhãn âm từ Negatome; đánh giá bằng kiểm chứng chéo, không có tập kiểm tra kiểm soát đồng dạng. Khác đơn vị dự đoán và khác loại nhãn so với đề tài, nên **không** phải baseline cùng thang — nhưng chiếm cùng **khung ứng dụng** và phải nằm trong bảng khảo sát.

## 8. Quy ước ngôn từ riêng của đề tài

- **Không dùng chữ "đầu tiên"** cho bất kỳ phần nào. Đã có ít nhất 5 công cụ dự đoán degron trước, và MetaDegron dùng PLM từ 2024.
- Phân biệt rõ **"thang điểm khối"** (bulk score, nhiệm vụ phụ) và **"bản đồ độ nhạy đột biến theo residue"** (bài toán chính). E3 là ca nghiên cứu, không trộn thành một con số chung.
- Khi nói về kiểm soát đồng dạng của tác giả: nói **"tốt nhưng không hoàn hảo"** — tự đo được 14/428 gene (3,3%) vẫn có họ hàng trong train ở identity ≥30%, và một gene trùng 100% trên 77 residue với TRIM5.
- Nhận xét mã nguồn PAP luôn kèm: **script công bố trỏ vào cột DNA thay vì cột acid amin**, nên không chạy lại mã của họ mà tự dựng pipeline.
- Gọi 219 footprint là **"chuẩn thực nghiệm theo residue"**, không gọi là "ground truth tuyệt đối".
- **Không nói "chưa ai làm đặc hiệu E3".** MetaDegron (2024) đã làm cho 21 E3 và có máy chủ web. Đề tài hiện khác ở **nguồn nhãn đột biến thực nghiệm mức residue** và **đơn vị dự đoán** (bản đồ vị trí thay vì điểm cả đoạn); nhánh dự đoán E3 đã bỏ, nên không dùng nhãn CRISPR làm tuyên bố đóng góp chính.
- **Không nói "kiến trúc chưa ai dùng" cho toàn bộ MIL-Degron.** Nói: *mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, không mới ở cơ chế* — BioBlobs đã dùng MIL có cổng attention trên protein, OmniESI đã dùng điều biến có điều kiện enzyme–cơ chất.
- **Không nói "16 E3 có nhãn CRISPR"** như thể đó là 16 lớp dùng được. Con số phải nói là **số peptide trên mỗi E3**: KLHL15 13, BAG6 4, ASB7 2, FEM1B 2, và sáu E3 có **đúng một** peptide. Tổng 27 peptide gán được trên 10 E3.
- **Không gọi phần E3 là "nhiệm vụ dự đoán".** Gọi đúng là **ca nghiên cứu** trên 23 peptide có cả nhãn E3 được gán và bản đồ bão hòa (27 là số peptide được gán E3 trước khi lấy giao).
- Gọi 219 footprint là **"chuẩn thực nghiệm theo residue"**; và khi nói về quy mô thì dùng số tự đếm — **2.624 peptide có footprint học được**, không nói "hơn 5.000 degron" vì con số đó là của tác giả và không phải số peptide học được.
- **Phải tự nói ra** rằng khi đã có nhãn mức residue thì MIL không còn bắt buộc, và lý do giữ cấu trúc túi là để dùng được cả nhãn yếu mức đoạn lẫn nhãn mạnh mức residue trong một mô hình.
- Khi nói về cấu trúc: **không nói "chưa ai dùng cấu trúc"**. Bài TF 05/2025 đã tính rASA và pLDDT từ AlphaFold2, và MetaDegron đã dùng độ phơi lộ làm đặc trưng. Cái khác là **chỗ đặt**: ở bước gộp thay vì ở đầu vào.

## 9. Tài nguyên tính toán — đã đo

Máy: AMD Ryzen 5 5500U, 12 luồng, 7 GB RAM, không GPU.

|                      | Thông lượng | Toàn bộ 212.658 tile | Cache mức residue                   |
| -------------------- | -------------- | ---------------------- | ------------------------------------ |
| ESM-2 **35M**  | 64,6 tile/s    | **~55 phút**    | 12,2 GB fp32                         |
| ESM-2 **650M** | 5,3 tile/s     | **~11 giờ**     | **32,7 GB fp32** — vượt RAM |

Kết luận: dùng **35M để lặp thí nghiệm**, 650M chỉ một lượt cuối chạy qua đêm theo luồng. Kiến trúc cần embedding mức residue nên **đây là lý do cụ thể để xin GPU**.
