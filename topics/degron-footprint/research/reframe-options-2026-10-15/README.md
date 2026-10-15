# Tìm hướng đóng góp lớn hơn, rõ hơn, dễ đánh giá hơn — 15/10/2026 (tối)

> ⚠ **ĐÍNH CHÍNH (phiên 7 và 8, cùng ngày) — đọc trước khi dùng bất kỳ con số nào ở §10 và §11.**
> Tài liệu này **giữ nguyên làm lịch sử**; ba chỗ của nó đã bị phép đo sau bác bỏ hoặc sửa:
>
> 1. **Con số +0,1061 ở §10.2 và §10.4 bị nhiễu lẫn và quy sai nguyên nhân.** Giá thật của việc dùng sai
>    assay chỉ là **0,0169**; phần còn lại là *nhãn tile vốn khó dự đoán hơn nhãn GPS*. Xem
>    [cross-assay-model §3.2](../cross-assay-model-2026-10-15/README.md).
> 2. **Mọi chỗ viết "dư địa đến trần" (ví dụ "dư địa 0,1992") phải đọc là trần ĐO LƯỜNG, không phải mức
>    học được.** Ba lớp mô hình đều dừng ở 0,78–0,80. Xem
>    [cross-assay-model §3.3](../cross-assay-model-2026-10-15/README.md).
> 3. **Kết luận §11.2 ("rủi ro LeBlanc là thật") vẫn đúng, nhưng chỉ cho nhãn mức peptide.** Trên nhãn
>    **hiệu ứng đột biến**, tỉ lệ áp đảo của thành phần giảm từ ≈ 56× xuống **2,2×**. Xem
>    [residue-task-derisk §3](../residue-task-derisk-2026-10-15/README.md).
>
> Hướng H1 mà §4–§6 khuyến nghị **đã bị hạ** xuống một chương đo lường theo
> [D-031](../../../../DECISIONS.md#d-031).

> **Tài liệu phân tích, không phải quyết định.** Đề nghị ở §6 đã ghi thành [C-13](../../../../DECISIONS.md)
> và **chờ Trọng xác nhận**. Viết tiếp [đánh giá mức đóng góp](../contribution-assessment-2026-10-15.md)
> (cùng ngày, đã thành [C-12](../../../../DECISIONS.md)) theo yêu cầu của Trọng: đánh giá lại toàn bộ trạng
> thái, tra bên ngoài, và gợi ý hướng đi có đóng góp **lớn hơn, rõ ràng hơn, dễ đánh giá hơn**, phát biểu
> được trơn tru theo mạch ở [hướng dẫn trình bày](../../../../project/advisor-presentation-guide.md).

## Nhãn bằng chứng

**[đo]** tự đo trong phiên này, có lệnh tái lập · **[nguồn]** số của tác giả, đã đọc ·
**[phân tích]** suy luận · **[đề xuất]** chờ xác nhận · **[chưa xác minh]** chỉ thấy qua tóm tắt tìm kiếm.

---

## 1. Phép đo mới trong phiên này đã đổi bài toán

Phép đo quan trọng nhất không phải từ tra y văn mà từ **dữ liệu đã nằm trên máy từ 13/10 mà chưa ai mở ra
đúng cách**: bảng tile của Voutsinos 2026,
`data/raw/voutsinos-2026/repo/score/degrons.csv.gz`. **[đo]**

| Đại lượng | Giá trị |
|---|---:|
| Số tile dùng được | **212.658** |
| Số gene | **5.327** |
| Số lần đo trung vị mỗi tile | 6 (từ 2 đến 30) |
| Độ tin cậy (reliability) của `degron_score` | **0,9807** → **trần tương quan r = 0,9903** |
| Độ tin cậy của `abundance_score` | **0,8549** → **trần tương quan r = 0,9246** |
| Pearson(`degron_score`, `abundance_score`) | **−0,9558** |

Cách tính: bảng **có sẵn cột sai số từng tile** (`degron_std`, `abundance_std`), nên
reliability = (phương sai tổng − phương sai sai số trung bình)/phương sai tổng, và trần tương quan là căn của
nó. Lệnh tái lập ở [§8](#8-tái-lập).

**Ba hệ quả, và chúng quan trọng hơn mọi thứ tra được từ bên ngoài. [phân tích]**

1. **Bài toán hết nghèo dữ liệu.** Đề tài đang bị chặn ở **n = 91** peptide với trần nhãn 0,6514. Ngay trong
   repo đã có **212.658 tile / 5.327 gene** với trần **0,99**. Chênh lệch này không phải cải thiện dần — nó
   đổi hẳn loại kết luận thống kê có thể phát biểu. Mức chênh tối thiểu phát hiện được đi từ ≈ 0,071 xuống
   cỡ 10⁻³.
2. **Trần nhãn tính được *chính xác*, không phải chặn trên.** Vì có sai số từng tile, không cần ước lượng
   trần qua hai replicate như bộ của Zhang. Đây là **tài sản phương pháp** mà hầu hết bộ DMS không có.
3. **Nhưng `degron_score` và `abundance_score` gần như cùng một lượng** (r = −0,96) ⇒ **không** được dùng
   chúng như hai assay độc lập. Em đã định đề xuất hướng đó và phép đo này **loại nó**. Ghi lại để không ai
   đề xuất lại.

**Giới hạn phải nói kèm:** `degron_std` là **sai số của trung bình** trên ≈ 6 lần đo, nên 0,98 là độ tin cậy
của **giá trị tile đã lấy trung bình** — đúng đại lượng cần dự đoán, nhưng lạc quan hơn độ tin cậy của một
lần đo đơn. Khi báo phải viết đúng là *"trần cho nhiệm vụ dự đoán trung bình tile"*.

---

## 2. Trạng thái đề tài hiện tại, đọc lại một lượt

Không có gì ở đây là mới; đây là bản gom để so với các hướng ở §4.

| Tài sản | Trạng thái |
|---|---|
| Khoảng trống chứng minh được (89,7%) | **Vững**, không hướng nào làm mất nó |
| Trần nhãn, baseline trung thực, đối chứng ΔPAP, split cov80, lực | **Đã đo xong**, có file |
| ΔPAP (0,4270) thua baseline thành phần (0,4884), p ≈ 6 × 10⁻¹⁹ | **Đã đo**, là phát hiện thật |
| Mô hình vượt baseline | **Chưa có gì** |
| Cổng phơi lộ | **Mất vai** — rASA không có phương sai trên nhãn peptide tách rời ([C-8](../../../../DECISIONS.md)) |
| Tính mới kiến trúc | **Gần 0** — Degformer đã xuất đúng ma trận 28×20; Yang 2026 là tập mẹ của cổng phơi lộ |
| n của nhiệm vụ chính | **91 peptide**, đơn vị thật là số cụm protein (< 91) |
| Rủi ro "thành phần > vị trí" (LeBlanc 2026) | **Chưa kiểm**, có thể làm mất cơ sở nhiệm vụ residue |

**Chẩn đoán một câu. [phân tích]** Đề tài đang đặt toàn bộ phần tính điểm lên **tập dữ liệu nhỏ nhất và
nhiễu nhất** trong bốn tập đã tải, và đặt toàn bộ tính mới lên **thành phần dễ bị bắt lỗi nhất** (kiến trúc).
Cả hai lựa chọn đều có thể đảo mà **không mất** tài sản nào.

---

## 3. Tra bên ngoài: hình dạng đóng góp đang được nhận trong năm 2026

Tra ngày **15/10/2026** trên web, PubMed và Consensus. Phát hiện chính: **"khoa học đánh giá"
(evaluation science) đang là một dạng đóng góp được nhận và công bố trong chính năm nay** — nhưng chưa ai làm
cho degron.

| Công trình | Làm gì | Vì sao liên quan |
|---|---|---|
| **Decomposing the Generalization Gap in PROTAC Activity Prediction** ([arXiv 2605.11764](https://arxiv.org/abs/2605.11764), 05/2026) | Random split AUROC 0,85–0,91 nhưng **leave-one-target-out chỉ ≈ 0,67**. Phân rã khoảng cách: **chặn 0,124 AUROC do phương sai đo giữa phòng thí nghiệm**, 0,05 do chọn ngưỡng. 8 kiến trúc + ESM-2 tới 3B + 2.000 lượt tinh chỉnh **không phá được trần**. Cấu hình rank-1 một seed **tụt 0,161** khi kiểm nhiều seed. Phần dương: few-shot k = 5 nâng 0,668 → **0,7050**. Platt scaling đưa về ngưỡng hiệu chuẩn 0,05 | **Đây là khuôn mẫu gần nhất với tài sản thật của repo.** Nó chứng minh dạng đóng góp *"đo trần, phân rã khoảng cách, chỉ ra kiến trúc không phá được, rồi đưa một can thiệp có delta dương"* **được nhận**, và nó làm cho **phát hiện âm trở thành đóng góp dương** `[nguồn]` |
| **Identifying and Addressing Systematic Data Leakage in Protein-Ligand Affinity Benchmarks** ([bioRxiv 2026.06.29.735309](https://www.biorxiv.org/content/10.64898/2026.06.29.735309v1), 06/2026) | Cùng hình dạng, cho docking: benchmark hiện tại méo vì rò rỉ; dựng benchmark kiểm soát rò rỉ; tầng khó nhất có baseline chỉ-ligand làm mốc | Hình dạng thứ hai, cùng năm, lĩnh vực khác `[chưa xác minh — đọc qua tóm tắt]` |
| **ProteinGym** ([NeurIPS 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723403/)) | Phần giới hạn **tự nói** nhiễu đo là vấn đề chưa giải quyết, một số assay có tương quan replicate kém nên *"không thể kỳ vọng tương quan hoàn hảo giữa thực nghiệm và mô hình"*; và cảnh báo **lấy trung bình Spearman qua các protein có thể gây hiểu sai** vì nhiễu và dải động khác nhau giữa protein | Benchmark lớn nhất của lĩnh vực **nêu đúng vấn đề mà repo đã đo được**, nhưng **không** đưa trần dựa trên replicate cũng **không** chuẩn hóa theo nó `[nguồn]` |
| **A natural upper bound to the accuracy of predicting protein stability changes** ([arXiv 1809.10389](https://arxiv.org/pdf/1809.10389)) | Từ đo lặp, trần Pearson cho ΔΔG là **0,73–0,83** tùy bộ | **Tiền lệ của ý tưởng trần** trong protein ML. Phải trích; **không được** nói trần nhãn là ý tưởng mới `[chưa xác minh]` |
| **FLIGHTED** ([PMC10996587](https://pmc.ncbi.nlm.nih.gov/articles/PMC10996587/)) | Lập luận FLIP và ProteinGym **cần hiệu chỉnh theo nhiễu**; và dữ liệu, không phải cỡ mô hình, đang là chỗ giới hạn | Nỗ lực gần nhất với chuẩn hóa theo nhiễu `[chưa xác minh]` |
| **Voutsinos 2026**, *Science Advances* 12(6):eadz3483 ([10.1126/sciadv.adz3483](https://www.science.org/doi/10.1126/sciadv.adz3483)) | > 200.000 tile 30-aa, > 5.000 protein bào tương, phủ 99,7%. 19% degron mạnh / 30% trung gian / 51% không. **Phần lớn degron nằm ở vùng bị chôn** ⇒ chỉ hoạt động khi protein mở/gấp sai. Mô hình của họ đạt **Pearson 0,82 và 0,87** so với độ dồi dào đo được **trên tile giữ lại** | Vừa là **nguồn dữ liệu lớn** (§1) vừa là **baseline cứng** phải trích đúng. Con số 0,82/0,87 là **mức tile**, không phải mức protein nguyên vẹn `[nguồn]` |
| Cùng bài, phần chuyển giao | Tương quan giữa **điểm tile trung bình** và **độ dồi dào protein nguyên vẹn** là **kém**; tốt hơn ở vị trí **phơi lộ và vô định hình** | **Đây là một kết quả âm đã công bố** trên đúng nhiệm vụ chuyển giao — biến nó thành bài toán mở có mốc, chứ không phải đất trống `[nguồn]` |
| **Calibrated VEP at the Residue Level** ([bioRxiv 2025.11.24.690189](https://www.biorxiv.org/content/10.1101/2025.11.24.690189.full.pdf)) và **Gene- and domain-aware calibration** ([bioRxiv 02/2026](https://www.biorxiv.org/content/10.64898/2026.02.17.706269v1)) | Hiệu chuẩn mức residue và theo gene/domain cho VEP | **Cảnh báo:** nhánh "hiệu chuẩn" đã đông trong 2025–2026. Nếu đặt đóng góp thuần ở hiệu chuẩn thì sẽ phải đua với hai bài rất mới `[chưa xác minh]` |

### 3.1 Chỗ **chưa tìm thấy tiền lệ**, sau một lần tra

Phát biểu đúng mức: **đã chạy các truy vấn trên web, PubMed và Consensus ngày 15/10/2026 và không tìm thấy**
— không phải "chưa ai làm". **[phân tích]**

| Điều | Bằng chứng ngược đã kiểm |
|---|---|
| **Phân rã khoảng cách tổng quát hóa cho dự đoán degron** (trong assay so với qua assay/qua ngăn tế bào) | Có cho PROTAC (2026) và protein–ligand (2026); **không** cho degron hay độ bền mức residue |
| **Chuẩn hóa hiệu năng mô hình theo trần nhãn từ replicate, rồi cho thấy *thứ hạng mô hình đổi*** | Chuẩn hóa theo trần là **chuẩn mực trong khoa học thần kinh** (brain encoding, trần từ lần trình bày lặp lại); trong DMS tương quan replicate chỉ dùng **làm phép kiểm lành mạnh**. ProteinGym nêu vấn đề nhưng không chuẩn hóa; FLIGHTED gần nhất |
| **Benchmark chuyển assay cho bộ dự đoán degron** (GPS ↔ VAMP-seq ↔ tile nhân) | Không tìm thấy. Có bằng chứng gián tiếp mạnh: một bài *Protein Science* 2023 thấy **biến thiên lớn nhất đến từ bộ dữ liệu, không từ bộ dự đoán** |

---

## 4. Bốn hướng, chấm theo bốn tiêu chí Trọng nêu

Chấm: **lớn** (tầm đóng góp) · **rõ** (phát biểu được trong một câu) · **dễ đánh giá** (có một con số đầu
bảng, không cần thắng SOTA) · **khả thi 8 tuần**.

### H1 — Phân rã khoảng cách tổng quát hóa của dự đoán degron ⭐ **khuyến nghị**

**Câu đóng góp:** *Mọi con số degron đã công bố đều đo trong một assay, trên split ngẫu nhiên hoặc theo gene.
Em đo xem còn lại bao nhiêu khi **đổi assay và đổi ngăn tế bào**, phân rã khoảng cách đó thành phần do nhiễu
đo, phần do rò rỉ tương đồng và phần do dịch chuyển miền, cho thấy phần nào **không** đóng được bằng kiến
trúc, rồi đưa một can thiệp có delta dương và một công cụ trả kết quả kèm trần.*

| | |
|---|---|
| **Lớn** | **Cao.** Kết luận áp cho **cả lĩnh vực degron**, không cho một mô hình. Dùng cả bốn nguồn đã tải |
| **Rõ** | **Cao.** Một con số đầu bảng: `AUROC trong assay − AUROC qua assay`, kèm bảng phân rã |
| **Dễ đánh giá** | **Cao nhất trong bốn hướng.** Không cần thắng SOTA; deliverable là **phân rã** + một delta dương từ can thiệp (theo đúng khuôn PROTAC: 0,668 → 0,705) |
| **Khả thi** | **Cao.** Dữ liệu đã trên máy; cụm MMseqs2 cov80 đã dựng; trần tính được chính xác từ cột sai số |
| **Rủi ro** | Khuôn này **mới 5 tháng tuổi** trong PROTAC ⇒ **phải trích và nói rõ là vận dụng sang lĩnh vực khác**. Và nếu GVHD giữ kỳ vọng "kiến trúc chưa ai dùng" thì hướng này **không đáp** |

**Vì sao nó cứu đúng ba chỗ đang hỏng. [phân tích]** (a) n = 91 → 212.658 tile; (b) không cần "mô hình
thắng baseline" làm điều kiện sống còn, nên [D-026](../../../../DECISIONS.md#d-026) (không dự phòng) bớt nguy
hiểm; (c) phát hiện âm ΔPAP **đổi vai từ gánh nặng thành bằng chứng trung tâm** — nó chính là một mục của
bảng phân rã.

### H2 — Chuẩn hóa đánh giá theo trần nhãn, nhập từ khoa học thần kinh

**Câu đóng góp:** *Trong DMS, tương quan replicate chỉ được dùng làm phép kiểm lành mạnh. Trong khoa học thần
kinh nó được dùng làm **mẫu số**. Em mang cách đó sang, định nghĩa thước đo chuẩn hóa theo trần, và cho thấy
**thứ hạng mô hình đổi** khi chuẩn hóa — tức các bảng xếp hạng hiện có đang xếp hạng một phần là nhiễu.*

| | |
|---|---|
| **Lớn** | **Cao nhất về tầm** — áp cho mọi benchmark DMS, không riêng degron. Đúng tầng công cụ của [D-022](../../../../DECISIONS.md#d-022) |
| **Rõ** | **Cao.** "Thứ hạng có đổi hay không" là câu hỏi nhị phân, định lượng được bằng Kendall tau trước/sau |
| **Dễ đánh giá** | **Cao**, nhưng kết quả có thể là *"thứ hạng không đổi"* ⇒ **kết quả âm**, mà [D-012](../../../../DECISIONS.md#d-012) không nhận |
| **Khả thi** | Trung bình — cần nhiều bộ có replicate; MaveDB 26 score set đã có, ProteinGym phải tải |
| **Rủi ro** | **Ý tưởng trần nhãn có tiền lệ** (arXiv 1809.10389 cho ΔΔG; FLIGHTED). Đóng góp chỉ còn là **hệ thống hóa + kết quả đổi thứ hạng** ⇒ **không được** nói là phát minh. Và ít "sinh học" nhất ⇒ TC1 yếu nhất |

**[phân tích]** H2 **không nên** đứng một mình, nhưng nó là **chương phương pháp hoàn hảo cho H1**: H1 cần
trần cho từng assay để phân rã; H2 là cách tính trần đó. Ghép lại thành một mạch liền.

### H3 — Chuyển giao peptide → protein nguyên vẹn, có điều kiện phơi lộ

**Câu đóng góp:** *Voutsinos 2026 báo rằng điểm tile trung bình **tương quan kém** với độ dồi dào protein
nguyên vẹn, và tốt hơn ở vị trí phơi lộ/vô định hình. Em biến quan sát đó thành một **hàm gộp học được có
điều kiện phơi lộ**, đánh giá trên nhãn độ dồi dào protein nguyên vẹn của MaveDB.*

| | |
|---|---|
| **Lớn** | **Cao về mặt khoa học** — đây là bài toán lĩnh vực thật sự muốn giải |
| **Rõ** | Cao: dự đoán độ dồi dào protein nguyên vẹn từ tile |
| **Dễ đánh giá** | **Trung bình** |
| **Khả thi** | **Trung bình–thấp** |
| **Rủi ro** | **Rơi lại đúng cái bẫy n nhỏ:** đơn vị suy luận là **protein**, và MaveDB chỉ có ít protein độ dồi dào ⇒ lực lại thành vấn đề. Và Voutsinos **đã làm một phiên bản** của nó |

**[phân tích]** H3 **cứu được cổng phơi lộ** (đặt nó ở chỗ rASA *có* phương sai) nên rất hấp dẫn về mặt kể
chuyện. Nhưng nó mua lại đúng rủi ro vừa chẩn đoán. ⇒ Nên là **chương chuyển giao của H1**, không phải đề tài.

### H4 — Giữ nguyên đề tài, chuyển đơn vị dự đoán từ residue sang tile

Hết vấn đề lực. Nhưng **Voutsinos đã đạt Pearson 0,82/0,87** trên đúng nhiệm vụ đó, và PAP là mô hình của
chính họ ⇒ phải thắng tác giả của bộ dữ liệu trên sân của họ. **Mỏng. Không khuyến nghị đứng một mình.**

---

## 5. Mạch trình bày cho H1, theo khuôn sáu bài của nhóm GVHD

Theo mẫu tổng hợp ở [hướng dẫn §1](../../../../project/advisor-presentation-guide.md): bối cảnh sinh học →
bài toán → giới hạn cách hiện có → dữ liệu/nhãn → workflow → bằng chứng từng thành phần → so sánh → giải
thích → giới hạn. Điền bằng số **đã đo**; ô chưa đo ghi "chưa đo".

| Trang | Thông điệp | Nội dung đã có |
|---|---|---|
| 1. Bài toán | Dự đoán đoạn nào của protein là tín hiệu phân hủy, và dự đoán đó còn đúng khi đổi điều kiện đo hay không | — |
| 2. Bối cảnh sinh học | Degron → ubiquitin → proteasome; biến thể tạo degron mới gây bệnh | Hình một tầng, nhãn tiếng Việt |
| 3. Đầu vào/đầu ra/nhãn | Vào: đoạn trình tự (+ cấu trúc). Ra: điểm degron + **bất định**. Nhãn: PSI từ GPS, điểm tile, độ dồi dào | 4 nguồn, số mẫu thật |
| 4. Tiền lệ và khoảng trống | Mọi con số công bố là **trong một assay**; chưa ai đo phần còn lại khi đổi assay/ngăn | Bảng 5 công cụ đã kiểm từng tính năng |
| 5. Dữ liệu và tính khả thi | **212.658 tile / 5.327 gene**, trần r = **0,9903**; bộ bão hòa 91 peptide, trần 0,6514 | **[đo]** §1 + audit 13/10 |
| 6. Ý tưởng | Giữ cố định biểu diễn và ngân sách, **chỉ đổi phép chia**: trong assay → qua assay → qua ngăn | Workflow 5 khối |
| 7. Thành phần trọng tâm | Trần nhãn là **mẫu số**, không phải chú thích | H2 |
| 8. Đánh giá và ablation | Phép đo nào **bác bỏ** được giả thuyết: nếu khoảng cách qua assay ≈ 0 thì đề tài sai | Bảng kế hoạch, ô "chưa đo" |
| 9. Bằng chứng hiện có | ΔPAP 0,4270 **thua** baseline 0,4884 (p ≈ 6 × 10⁻¹⁹); kernel 1→7 cho **+0,1311**; nhiễu 75,9% không chữa được bằng ngưỡng read (DiMSum, Enrich2) | Bốn báo cáo đã có |
| 10. Ứng dụng, giới hạn | API trả điểm **kèm trần và cờ ngăn tế bào**; giới hạn: peptide không chứng minh tác động trên protein nguyên vẹn | Bốn tính năng đã kiểm |

**Mẫu câu điền theo [hướng dẫn §2](../../../../project/advisor-presentation-guide.md):**

> *Trong dự đoán degron, người dùng cần biết đoạn nào gây phân hủy **và tin được đến đâu**, để chọn vị trí
> đột biến đáng thử. Các mô hình gần nhất (PAP, MetaDegron, DegronMD, Degformer) báo kết quả **trong một
> assay bào tương, trên split ngẫu nhiên hoặc theo gene**, và chưa báo trần nhãn. Nghiên cứu này **đo và phân
> rã** phần hiệu năng mất đi khi đổi assay và đổi ngăn tế bào, được đánh giá bằng **so sánh ghép cặp cùng
> biểu diễn, cùng ngân sách, trên split cụm protein cov80**, với trần nhãn tính từ sai số từng tile.*

Một câu, không có chữ "chưa ai làm", mỗi mệnh đề gắn một phép đo. Đây là chỗ H1 hơn mạch hiện tại rõ nhất.

---

## 6. **[đề xuất]** → [C-13](../../../../DECISIONS.md)

1. **Nhận H1 làm mạch chính**, với **H2 làm chương phương pháp** và **H3 làm chương chuyển giao**. Giữ nguyên
   tên đề tài và trụ khoảng trống 89,7%; đổi **đơn vị đánh giá** và **chỗ đặt đóng góp**.
2. **Chuyển nhãn chính từ bộ bão hòa (n = 91) sang tile Voutsinos (212.658 / 5.327 gene)** cho phần benchmark,
   giữ bộ bão hòa cho **nhiệm vụ ma trận 28×20** như sản phẩm ứng dụng. Việc này **sửa một phần
   [D-025](../../../../DECISIONS.md#d-025) đề xuất 2** nên cần Trọng quyết.
3. **Việc chặn đổi:** không còn là "tính lực trên n = 91" mà là **dựng được phép chia qua assay** và **đếm số
   cụm protein độc lập ở từng assay**.
4. **Hỏi GVHD một câu dứt khoát** cùng [C-5](../../../../DECISIONS.md) và [C-7](../../../../DECISIONS.md):
   *đóng góp dạng "đo và phân rã trần của một lớp bài toán" có được nhận, hay bắt buộc phải có kiến trúc mới?*
   Ba đề xuất C-7, C-12, C-13 đều treo vào câu trả lời này.

**Rủi ro của chính §6, phải nhận. [phân tích]** (a) H1 **vẫn** cần một delta dương để thỏa
[D-012](../../../../DECISIONS.md#d-012); khuôn PROTAC cho thấy nó có thể đến từ **can thiệp hiệu chuẩn/few-shot**
thay vì từ kiến trúc, nhưng nó **không miễn**. (b) Nếu khoảng cách qua assay hóa ra **nhỏ**, H1 mất thông
điệp — nên **đo nó trước tiên**, trên một cặp assay, trước khi cam kết. (c) Chuyển nhãn chính nghĩa là một
phần công của ba đợt audit chuyển sang vai phụ; không mất, nhưng phải viết lại.

---

## 7. Những gì tài liệu này **không** làm

- **Không** quyết định; §6 là đề xuất, đã ghi [C-13](../../../../DECISIONS.md).
- **Không** huấn luyện mô hình nào. Phép đo duy nhất mới là reliability ở §1.
- **Không** đọc toàn văn arXiv 2605.11764, bioRxiv 735309, FLIGHTED, arXiv 1809.10389 — tất cả **[chưa xác
  minh]** ngoài phần tóm tắt đã trích. **Phải đọc toàn văn arXiv 2605.11764 trước khi dùng nó làm khuôn.**
- **Không** tải thêm dữ liệu; H1 dùng cái đã có, cộng tùy chọn [C-10](../../../../DECISIONS.md) (Larsen, 5,77 MB).
- **Không** sửa `presentation/`.

## 8. Tái lập

Phép đo ở §1 (chạy ngoài thư mục dữ liệu, với `python3 -I`):

```bash
# script: topics/degron-footprint/research/reframe-options-2026-10-15/probe_tile_reliability.py
.venv/bin/python3 -I topics/degron-footprint/research/reframe-options-2026-10-15/probe_tile_reliability.py
```

Đầu vào: `topics/degron-footprint/data/raw/voutsinos-2026/repo/score/degrons.csv.gz` (chỉ đọc, không sinh
file trong `data/`). Nguồn gốc file đã ghi ở [data/README.md](../../data/README.md).

---

## 9. Đã đọc toàn văn arXiv 2605.11764, và đã đo khoảng cách qua assay — **H1 có thông điệp**

Thêm 15/10/2026 (tối, phiên 2), sau khi Trọng yêu cầu làm việc (2) ở §6.

### 9.1 Phương pháp thật của bài PROTAC, đọc từ toàn văn

Klamt, Nejdl, Tang — arXiv:2605.11764v1, nộp 12/05/2026, cs.LG + q-bio.BM, 32 trang, **preprint chưa qua
phản biện**, CC BY 4.0, dữ liệu CC-BY-4.0, mã MIT. **[nguồn]**

**Cái cần học là *bậc thang* (cascade), không phải con số.** Họ đo ba mức trên **cùng một cohort 36 target,
ghép cặp n = 35**:

| Mức | AUROC | Đổi gì so với mức trên |
|---|---:|---|
| random-CV | **0,802** | — |
| **cross-lab** (giữ nguyên target, bỏ ra các mục của *một công bố*) | **0,678** | chỉ đổi **phòng đo** ⇒ hiệu 0,124 là **phương sai đo** |
| LOTO (bỏ hẳn target) | **0,653** | thêm **dịch chuyển miền** ⇒ hiệu 0,025 |

**Mấu chốt phương pháp:** mức giữa **giữ nguyên định danh target** để **dịch chuyển cấu trúc bị loại bỏ**,
nên hiệu số cô lập được đúng một nguyên nhân. Đây là thứ chuyển sang được.

Neo phụ: 3,7 lần thay đổi DC50 trung vị trên **cùng hợp chất** qua các công bố (28 phép so, 12 target).
Bốn chặn triangulation: 0,124 (phòng đo) · 0,05 (ngưỡng nhị phân hóa) · 0,008 (xung đột cross-DOI) ·
0,02–0,03 (dịch chuyển còn lại). Phân tích **chính** của họ không phải bậc thang mà là **ω² = 0,256**
(hiệu chỉnh chệch, CI [0,110; 0,421]). Kết luận: phương sia đo giữa phòng chiếm **0,117 trong 0,149**
(≈ 81%). Phần dương: few-shot k = 5 cho **+0,0306**, CI [+0,015; +0,051] — **yếu tố duy nhất** có đóng góp
biên tách khỏi 0 trong thiết kế factorial 2⁴.

**Ba điều về mức độ trung thực của bài, nên bắt chước. [phân tích]** (a) Họ báo ω² **không chệch** làm chính
và nói rõ eta² bị chệch lên ở n nhỏ; (b) họ viết thẳng *"partially-overlapping bounds rather than a strict
additive identity"* — bốn chặn **không** cộng thành một đẳng thức; (c) phần giới hạn tự hạ một kết quả đầu
đề của chính mình: hiệu ứng warhead **+0,042** co lại dưới sai số seed khi phân rã đúng cách. Và họ tự báo
dedup làm trần 0,668 tụt còn **0,617**.

### 9.2 Phép đo: bậc thang hai mức cho degron **[đo]**

Chuyển "cùng hợp chất, hai phòng" thành **"cùng trình tự, hai assay"**. Script:
[cross_assay_gap.py](cross_assay_gap.py). Hai assay đều **bào tương**, nên đây là
**dịch chuyển định dạng assay**, chưa phải chuyển ngăn tế bào.

- Assay A — **GPS** (Zhang 2023): peptide 28-mer gắn đầu C của GFP, PSI 6 bin. 252.502 peptide 28-mer.
- Assay B — **tile sort-seq** (Voutsinos 2026): tile 30-aa, 4 cổng, `degron_score`. 212.634 tile.
- Ghép: 28-mer của A là **chuỗi con đúng** của 30-mer của B ⇒ **17.820 trình tự dùng chung**,
  **4.610 accession UniProt**, **4.308 cụm protein cov80**.

| Đại lượng | Giá trị |
|---|---:|
| Độ tin cậy GPS (r hai replicate 0,9510 → trung bình) | **0,9749** |
| Độ tin cậy tile (từ sai số từng tile) | **0,9807** |
| **Trần AUROC trong assay** (replicate GPS → nhãn GPS) | **0,9813** |
| **AUROC qua assay** (`degron_score` → nhãn GPS) | **0,9041** |
| **⇒ Khoảng cách qua assay** | **0,0773** |
| Pearson(PSI, `degron_score`) | **−0,7680** |
| Trần tương quan do nhiễu = √(0,9749 × 0,9807) | 0,9778 |
| **\|r\| sau chỉnh suy giảm hai phía** | **0,7854** |

### 9.3 Kết luận, và nó **đảo** kết luận của bài PROTAC

**[phân tích]** Ba điều, xếp theo mức quan trọng:

1. **Khoảng cách qua assay gần như KHÔNG do nhiễu đo.** Hai assay đều rất tin cậy (0,975 và 0,981), nên
   trần nhiễu là 0,9778 — nhưng tương quan **thật** (sau khi gỡ nhiễu cả hai phía) chỉ **0,7854**. Tức
   **≈ 0,215 của tương quan còn thiếu là hệ thống**, không phải nhiễu. Ở bài PROTAC, phương sai đo chiếm
   **81%** khoảng cách; ở đây nó chiếm **gần như 0%**. Đây là một **kết quả trái chiều, không phải lặp lại** —
   và nó mạnh hơn cho đề tài, vì nó nói **có thứ thật để mô hình hóa**.
2. **Khoảng cách tập trung đúng ở chỗ cần dự đoán.** Trên **dải khó** 2,0 < PSI < 4,0 (n = 7.601, tỉ lệ
   dương 0,432): AUROC qua assay rơi **0,9041 → 0,7839**, và |r| rơi **0,768 → 0,5291**. Con số toàn dải
   0,904 **được làm đẹp bởi hai đuôi dễ**. Thêm nữa, trên 10.219 ca **tự tin** (PSI ≤ 2,0 hoặc ≥ 4,0) vẫn có
   **19,10% bất đồng ý hoàn toàn**.
3. **Cỡ mẫu hết là vấn đề.** **4.308 cụm protein cov80**, so với **n = 91** của nhiệm vụ hiện tại.

⇒ **H1 có thông điệp**, và thông điệp đó đồng thời **định nghĩa nhiệm vụ cho kiến trúc mới** mà
[D-027](../../../../DECISIONS.md#d-027) đòi: *xử lý dịch chuyển định dạng assay, chấm trên dải khó.*
Đây là một mục tiêu kiến trúc **hẹp, đo được, và có mốc sẵn** — khác hẳn "một cơ chế chưa ai dùng".

### 9.4 Năm giới hạn của chính phép đo này, phải nói kèm **[phân tích]**

1. **Trình tự ghép không phải construct giống nhau.** 28-mer là chuỗi con của 30-mer ⇒ tile mang thêm tới
   **2 residue ngữ cảnh**. Một phần của 0,215 là **khác ngữ cảnh trình tự**, không phải khác assay. **Đối
   chứng bắt buộc:** so ba nhóm offset (0/1/2) và nhóm 28-mer nằm giữa tile; nếu khoảng cách không đổi theo
   offset thì ngữ cảnh không phải nguyên nhân.
2. **Hai assay khác nhau ở nhiều trục cùng lúc** — reporter, số bin (6 so với 4), chiều dài tile, chuẩn hóa,
   thư viện. Phép đo **không** tách được các trục đó; nó chỉ chặn **tổng**. Bài PROTAC tách được vì họ giữ
   nguyên target; ở đây muốn tách phải thiết kế thêm.
3. **Độ tin cậy GPS là tái lập kỹ thuật** trên cùng thư viện, cùng assay — nó **không** bao gồm phương sai
   construct, nên trần 0,9813 **lạc quan**.
4. `tile.setdefault` **giữ tile đầu tiên** khớp một khóa 28-mer; nếu nhiều tile chứa cùng 28-mer thì các tile
   sau bị bỏ. Ảnh hưởng nhỏ nhưng chưa định lượng.
5. **Chưa phải chuyển ngăn tế bào.** Cả hai đều bào tương. Mức thứ ba của bậc thang cần bộ nhân Larsen
   ([C-10](../../../../DECISIONS.md)).

### 9.5 Bậc thang đầy đủ nên dựng (ba mức đã có, hai mức cần thêm)

| Mức | Đổi gì | Trạng thái |
|---|---|---|
| 1. Trong assay, trong cụm | — | **0,9813** `[đo]` |
| 2. **Qua assay**, cùng trình tự | định dạng assay | **0,9041** `[đo]` |
| 3. Qua assay, **dải khó** | + độ khó của ca | **0,7839** `[đo]` |
| 4. Qua assay + **qua cụm protein cov80** | + dịch chuyển trình tự | **chưa đo** — cần huấn luyện |
| 5. **Qua ngăn tế bào** (bộ nhân Larsen) | + ngăn tế bào | **chưa đo** — cần [C-10](../../../../DECISIONS.md) |

Mức 4 là mức **phải có** để phát biểu đóng góp; mức 5 là phần mở rộng.

---

## 10. (a) Đối chứng offset và (b) bậc thang 2×2 — **đã chạy, và kết quả đổi chỗ đặt đóng góp lần nữa**

Thêm 15/10/2026 (tối, phiên 3), theo yêu cầu của Trọng. Script:
[cascade_and_offset.py](cascade_and_offset.py). **[đo]**

### 10.1 (a) Đối chứng offset — **giới hạn số 1 ở §9.4 đã được đóng**

17.680/17.820 trình tự khớp **đúng một** tile (chỉ 140 ca nhập nhằng).

| offset của 28-mer trong tile 30-mer | n | \|Pearson\| | AUROC |
|---|---:|---:|---:|
| 0 (thêm 2 residue ở đầu C) | 6.485 | 0,7735 | 0,9069 |
| 1 (thêm 1 mỗi đầu) | 5.724 | 0,7611 | 0,9026 |
| 2 (thêm 2 residue ở đầu N) | 5.471 | 0,7700 | 0,9040 |
| **biến thiên theo offset** | | **0,0125** | **0,0044** |

**Kết luận:** biến thiên theo offset là **0,0044 AUROC**, so với khoảng cách qua assay **0,0773** ⇒ ngữ cảnh
2 residue giải thích **nhiều nhất ≈ 6%** khoảng cách. **Ngữ cảnh trình tự không phải nguyên nhân.** Con số
0,0773 dùng được trước GVHD.

### 10.2 (b) Bậc thang 2×2, 5 seed, **cả hai ô đều ngoài mẫu**

Sửa hai lỗi của bản nháp: ô "cùng cụm" trước đó là **trong mẫu** (nay dùng peptide giữ lại khỏi huấn luyện),
và trước đó chỉ **một** split (nay 5 seed — đúng bài học của chính bài PROTAC, nơi cấu hình rank-1 một seed
tụt 0,161).

Mô hình: ridge trên one-hot 28×20 + thành phần, λ = 10, huấn luyện trên PSI của GPS ở các cụm train
(≈ 37–39 nghìn peptide). Giữ **nguyên trình tự, nguyên cụm, nguyên mô hình**, chỉ đổi **một** thứ mỗi lần.

| Mô hình | Cụm | n | ρ vs A (GPS) | ρ vs B (tile) | AUROC vs A |
|---|---|---:|---:|---:|---:|
| đầy đủ (vị trí + thành phần) | cùng | 4.602 | 0,8848 ± 0,0028 | 0,7786 ± 0,0065 | 0,9387 ± 0,0041 |
| đầy đủ | khác | 8.615 | 0,8887 ± 0,0016 | 0,7803 ± 0,0029 | 0,9412 ± 0,0014 |
| chỉ thành phần | cùng | 4.602 | 0,8820 ± 0,0025 | 0,7826 ± 0,0070 | 0,9349 ± 0,0038 |
| chỉ thành phần | khác | 8.615 | 0,8857 ± 0,0017 | 0,7844 ± 0,0032 | 0,9379 ± 0,0017 |

**Phân rã (Spearman, mô hình đầy đủ):**

| Đổi gì | Hiệu |
|---|---:|
| **dịch chuyển CỤM protein** (cùng assay) | **−0,0039** |
| **dịch chuyển ASSAY** (cùng cụm) | **+0,1061** |
| cả hai | +0,1045 |
| **tỉ lệ ASSAY / CỤM** | **27×** |

Mô hình chỉ-thành-phần cho đúng cùng hình: cụm −0,0037, assay +0,0993, tỉ lệ **27×**.

### 10.3 Ba phát hiện, và cả ba đều đổi điều gì đó trong repo **[phân tích]**

**Phát hiện 1 — Toàn bộ khoảng cách tổng quát hóa là dịch chuyển assay; trình tự lạ đóng góp bằng 0.**
0,1061 so với −0,0039. Dấu của dịch chuyển cụm là **âm** (cụm chưa thấy lại *hơi tốt hơn*) và **ổn định qua
cả 5 seed** (SD 0,0016–0,0028), nên đây không phải nhiễu. Cộng với §9: dịch chuyển assay **không phải nhiễu
đo** (hai assay tin cậy 0,975 và 0,981). ⇒ Khoảng cách này là một loại **thứ ba** mà cả bài PROTAC lẫn y văn
degron đều chưa đặt tên: **thiên lệch hệ thống giữa định dạng assay**, không phải nhiễu, không phải trình tự lạ.

**Phát hiện 2 — Split cụm protein cov80 không mua được gì trên nhiệm vụ này.** Đây là
**mâu thuẫn với [D-025](../../../../DECISIONS.md#d-025) đề xuất 4** của chính repo, và với cả phần phân tích
lực vốn chọn cov80 thay cov50 vì lực. Precaution đó **thật** cho nhiệm vụ khác, nhưng ở đây nó **đo đúng số
0**. Đề xuất [C-14](../../../../DECISIONS.md).

⚠ **Giới hạn quan trọng nhất của phát hiện 2:** mô hình là **ridge tuyến tính trên one-hot**, có thể **quá
đơn giản để ghi nhớ định danh protein**. Một PLM có thể overfit cụm và khi đó split cụm sẽ có tác dụng. Phát
biểu đúng mức: *"với mô hình tuyến tính thành phần/vị trí trên nhãn peptide GPS, split cụm cov80 không thay
đổi kết quả"* — **không** phải *"split cụm không bao giờ cần"*. Phải chạy lại khi có mô hình mạnh.

**Phát hiện 3 — Kênh theo vị trí chỉ thêm +0,0028 đến +0,0030 so với chỉ thành phần.** Đây là **xác nhận độc
lập cho LeBlanc 2026** (*"composition is more important than individual positions"*), trên assay khác, 5 seed.
Rủi ro số một ở [C-12](../../../../DECISIONS.md) **nay đã được đo, và nó là thật** — ở **mức peptide**.

**Nhưng nó KHÔNG bác bỏ trụ thứ nhất của đề tài, và chỗ này phải nói cho đúng:** repo đã **chứng minh bằng
toán** rằng mô hình chỉ-thành-phần **không thể** định vị residue nào (89,7% peptide bị ràng buộc). Hai điều
cùng đúng: *thành phần đủ để chấm điểm cả đoạn, nhưng bị chứng minh không thể định vị bên trong đoạn.* ⇒ Luận
văn **không được** nói "vị trí giúp chấm điểm peptide"; lý lẽ về vị trí chỉ sống **ở mức residue**.

### 10.4 Chỗ đặt đóng góp sau ba phiên, và mục tiêu số cho kiến trúc mới

Nhiệm vụ của kiến trúc mới theo [D-027](../../../../DECISIONS.md#d-027) nay **hẹp lại ba lần** nhờ loại trừ:

| Ứng viên cho "việc của kiến trúc" | Đo được | Kết luận |
|---|---:|---|
| Xử lý trình tự/cụm protein chưa thấy | −0,0039 | **miễn phí ⇒ không phải việc của kiến trúc** |
| Thêm ngữ cảnh vị trí cho điểm peptide | +0,0030 | **gần cạn ⇒ không phải** |
| Cổng phơi lộ trên nhiệm vụ chính | không nhận diện được ([C-8](../../../../DECISIONS.md)) | **không phải** |
| **Xử lý dịch chuyển định dạng assay** | **+0,1061**, hệ thống | ✅ **đây** |
| **Định vị mức residue** | bị chứng minh bất khả thi cho mô hình thành phần | ✅ **và đây** |

**Mục tiêu số, phát biểu được:** cross-assay Spearman hiện **0,7786 ± 0,0065**, trần nhiễu **0,9778** ⇒ dư
địa **0,1992** trên **4.308 cụm protein**. So với mốc cũ (vượt 0,4897, trần 0,6514, dư địa 0,1617, **n = 91**):
dư địa **lớn hơn**, cỡ mẫu **lớn hơn 47 lần**, và baseline **không phải oracle**.

---

## 11. Dọn hai món nợ phương pháp — Phát hiện 2 **vững**, rủi ro LeBlanc **là thật**

Thêm 15/10/2026 (tối, phiên 5), theo lựa chọn của Trọng: dọn nợ trước khi chốt các đề xuất C.
Script: [method_debt.py](method_debt.py). **[đo]**

### 11.1 Nợ 1 — Phát hiện 2 **không** phải tạo tác của mô hình yếu

Ba mô hình, khả năng khai thác đồng dạng tăng dần, 3 seed, cả hai ô ngoài mẫu:

| Mô hình | ρ cùng cụm | ρ khác cụm | **dịch chuyển CỤM** | dịch chuyển ASSAY | tỉ lệ |
|---|---:|---:|---:|---:|---:|
| ridge tuyến tính | 0,8858 ± 0,0034 | 0,8889 ± 0,0014 | **−0,0032** | +0,1041 | 33× |
| **gradient boosting** | 0,8813 ± 0,0031 | 0,8827 ± 0,0023 | **−0,0014** | +0,1043 | **77×** |
| **1-NN theo đồng nhất vị trí** | 0,3074 ± 0,0153 | 0,3168 ± 0,0041 | **−0,0094** | +0,0341 | 4× |

**Ba điều, và điều thứ ba là quan trọng nhất. [phân tích]**

1. **Gradient boosting cho dịch chuyển cụm −0,0014** — *nhỏ hơn cả* ridge. Lời giải thích "mô hình quá đơn
   giản để ghi nhớ định danh protein" ở [§10.3](#103-ba-phát-hiện) **bị bác bỏ**. Giới hạn chính của Phát
   hiện 2 đã được dọn.
2. **1-NN đồng dạng — phép kiểm chặn trên — cũng cho dịch chuyển cụm âm (−0,0094).** Ngay cả mô hình *chỉ*
   sống bằng việc tra peptide giống nhất cũng **không** được lợi từ việc test nằm trong cụm đã huấn luyện.
3. **Và đây là cơ chế: 1-NN đồng dạng chỉ đạt ρ ≈ 0,31, so với 0,89 của ridge.** Tra cứu theo đồng dạng trình
   tự **gần như vô dụng** cho nhiệm vụ này. ⇒ Split cụm protein không mua được gì **vì không có tín hiệu đồng
   dạng nào để rò rỉ**: tín hiệu dự đoán ở đây là **thành phần**, không phải họ hàng trình tự.

Thêm một quan sát: **gradient boosting (0,8813) không thắng ridge tuyến tính (0,8858)**. Mô hình phi tuyến
mạnh không ăn được gì — lại một dấu hiệu nữa rằng tín hiệu ở mức peptide là **đơn giản và cộng tính**.

⇒ **[C-14](../../../../DECISIONS.md) nay đã đủ bằng chứng**, điều kiện "phải chạy lại với mô hình mạnh" đã
thực hiện. Phát biểu được: *với ba lớp mô hình khác hẳn nhau — tuyến tính, boosting, và tra cứu đồng dạng —
split cụm cov80 đều không thay đổi kết quả, vì nhiệm vụ không có tín hiệu đồng dạng để rò rỉ.*

### 11.2 Nợ 2 — rủi ro LeBlanc **là thật**, ở mức tham số

40 bootstrap trên 43.635 peptide, theo khuôn LeBlanc.

| Véc-tơ trọng số | Tái lập nửa–nửa | \|μ\|/SD trung vị | % hệ số có \|μ\|/SD > 2 | Đồng thuận dấu |
|---|---:|---:|---:|---:|
| **560 ô (vị trí, acid amin)** | +0,9801 | **1,24** | **0,289** | **0,684** |
| tổng theo acid amin (20 chiều) | +1,0000 | **69,02** | 1,000 | 1,000 |
| kênh thành phần (20 chiều) | +1,0000 | 69,02 | 1,000 | 1,000 |

**Đọc cho đúng, vì hai dòng đầu tiên nhìn như mâu thuẫn. [phân tích]** Véc-tơ 560 chiều **xét như một
tổng thể** thì tái lập cao (0,9801) — nhưng đó là vì nó **thừa hưởng** thành phần mức acid amin, thứ tái lập
hoàn hảo. Phép kiểm phân biệt được là **từng hệ số**: chỉ **28,9%** ô vị trí tách được khỏi 0, đồng thuận dấu
chỉ **0,684**, và độ ổn định của tổng theo acid amin **cao hơn ≈ 56 lần**.

⇒ *"Thành phần quan trọng hơn từng vị trí"* của LeBlanc 2026 **đúng ở mức tham số**, không chỉ ở mức hiệu
năng. Rủi ro số một của [C-12](../../../../DECISIONS.md) được xác nhận.

### 11.3 Hệ quả buộc phải sửa [C-13](../../../../DECISIONS.md) — và nó cứu lại bộ bão hòa

**[phân tích]** Đây là chỗ hai món nợ gặp nhau và sinh ra một kết luận mà không phiên nào trước thấy.

Nhãn mà §11.2 dùng là **PSI của cả peptide 28-mer** — nhãn **mức peptide**. Và kết quả là: nhãn mức peptide
**không nhận diện được tham số theo vị trí**. Tile Voutsinos cũng là nhãn **mức tile**, tức cùng loại.

⇒ **Tile không thể đỡ phần lập luận mức residue của đề tài.** C-13 đề nghị chuyển nhãn chính sang tile; nay
phải nói chính xác hơn:

| Nguồn nhãn | Đỡ được phần nào | Không đỡ được |
|---|---|---|
| **Tile Voutsinos** (212.658 / 5.327 gene) | benchmark, **phân rã khoảng cách qua assay**, cỡ mẫu, trần nhãn chính xác | **mọi tuyên bố mức residue** |
| **Bộ bão hòa** (n = 91) | **duy nhất** đỡ được mức residue — vì nhãn là **hiệu ứng đột biến**, đo trực tiếp từng vị trí | cỡ mẫu, lực |

Và điều này **không** mâu thuẫn trụ 89,7%, mà **giải thích** nó: nhãn mức peptide không định vị được bên
trong peptide, nên muốn nói về residue thì **buộc** phải có nhãn đột biến. Chứng minh 89,7% nói mô hình thành
phần *không thể*; §11.2 nói nhãn peptide *cũng không đủ để học*. Hai việc khác nhau, cùng chỉ về một chỗ.

⇒ **Sửa C-13: tile và bộ bão hòa có hai vai riêng, không thay thế nhau.** Hệ quả: **việc chặn "lực trên
n = 91" KHÔNG mất đi** như §6 và §10 đã nói — nó chỉ **thu hẹp** vào chương mức residue. Phần benchmark và
phân rã thì hết lo cỡ mẫu.
