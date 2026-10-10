# Chốt đề tài trước buổi gặp tuần 6: một đề tài chính, một dự phòng

Ngày: **08/10/2026**. Yêu cầu của sinh viên: chốt **một** đề tài hiểu rõ trước buổi gặp tuần 6, cộng **một** dự phòng; ưu tiên đề tài có tính mới **cả phần sinh học lẫn phần tin học**; **không còn ràng buộc GPU và thời gian**; tiêu chí quyết định là **ý nghĩa và giá trị khoa học thật**.

Nhãn bằng chứng: `[tự đo]` = số Claude tự tải file và đếm trong phiên này; `[chưa kiểm]` = chỉ thấy qua tóm tắt hoặc suy luận.

> **Đã đính chính 10/10/2026.** Bản gốc 08/10/2026 được giữ nguyên trong lịch sử git (xem commit trước commit đính chính này) để đối chiếu với [báo cáo khảo sát sâu](sirtuin-substrate-deep-research.md), vốn kiểm chứng tài liệu này như một **giả thuyết**, không phải kết luận. Những chỗ đã sửa trong bản này: quy tắc nhãn dương là `efficiency ≥ 1` (không phải `category ≥ 1`); **43,0% là recall, không phải precision**; nhãn âm trong tế bào **đã có sẵn** (Zhang 2022); **Deep-PLA 2020 đã phủ SIRT1/2/3/6/7** nên tính mới sinh học không còn; cổng dữ liệu và cổng SIRT1 được viết lại; Prot2Token không phải NeurIPS 2025; bỏ một câu về đặc hiệu SIRT7 không truy được nguồn. Bảng đính chính đầy đủ 25 dòng ở mục 5 của báo cáo khảo sát sâu.

Tài liệu nền: [compute-novelty-directions.md](compute-novelty-directions.md) · [b-method-layer-draft.md](b-method-layer-draft.md) · [advisor-4-directions-analysis.md](advisor-4-directions-analysis.md) · candidates-a-b-explained.md (chỉ có trong thư mục dự án, không nằm trong repo)

---

## 1. Kết luận: khuyến nghị gì

**Đề tài chính (khuyến nghị): dự đoán cơ chất deacetyl hóa theo từng isoform SIRT1–7, với câu hỏi trung tâm là chuyển từ nhãn in vitro sang dự đoán trong tế bào.**

Tên đề tài tạm: *Dự đoán cơ chất deacetyl hóa đặc hiệu isoform của SIRT1–7 bằng PLM–mCNN đa nhãn, học từ dữ liệu mảng peptide in vitro và đánh giá trên dữ liệu khối phổ trong tế bào, kèm dự đoán có bảo đảm thống kê.*

> **Khung đã đổi hai lần, chốt ngày 10/10/2026 là: THU HẸP, không bỏ.** Phần định lượng chỉ còn **SIRT1/2/3**. Lời hứa của đề tài **không phải "một mô hình tốt hơn"** mà là **một benchmark chuyển miền**: lấy ba bộ dự đoán cơ chất sirtuin đã công bố (Deep-PLA 2020, DeepSIRT 2021, Ridgeway 2025 — ba chế độ nhãn huấn luyện khác nhau, **không bộ nào báo MCC hay AUPRC**, không bộ nào được đánh giá trên acetylome KO/KD có nhãn âm thật) và **đo lại tất cả trên một tập đánh giá trong tế bào duy nhất**, với chỉ số chịu được mất cân bằng, kiểm soát rò rỉ ở mức protein cộng mức đồng dạng. Lĩnh vực kinase đã có đúng hình dạng này (benchmarKIN 2025); lĩnh vực sirtuin thì chưa `[chưa tìm thấy, không kết luận là chưa từng có]`.
>
> Chuyển sang đề tài dự phòng **chỉ khi** GVHD không chấp nhận một **kết quả âm** — một phép đo cho thấy nhãn in vitro không chuyển được — làm đóng góp chính. Đó là câu hỏi quyết định của buổi tuần 6.

**Đề tài dự phòng: B + lớp cải tiến tin học** — dự đoán vị trí phospho theo nhóm kinase, mô hình thầy ESM-2+LoRA+mCNN chưng cất thành mô hình nhỏ chạy CPU, kèm conformal. Bản phác đã có: [b-method-layer-draft.md](b-method-layer-draft.md) (PR #8).

Khác biệt quan trọng so với bản phác trước: đề tài chính **không còn là "A + thêm vài kỹ thuật tin học"**. Điểm yếu lớn nhất của A trước đây — *không có tập test độc lập* — được chuyển thành **chính câu hỏi nghiên cứu**. Lý do ở mục 3.

---

## 2. Số liệu tự đo trong phiên này

Tất cả tải được từ môi trường cloud ngày 08/10/2026.

### 2.1 Nhãn huấn luyện: mảng peptide Rauh 2013

File `Supplementary Data 1` của [Rauh et al. 2013, Nat Commun 4:2327](https://www.nature.com/articles/ncomms3327) (2,1 MB, tải trực tiếp từ Springer, mã 200) `[tự đo]`:

- **6.802 vị trí acetyl hóa**, mỗi vị trí là một peptide 13 amino acid (6 residue mỗi bên).
- Mỗi vị trí có **4 cột cho mỗi isoform**: `substrate category`, `signal ratio (exp:ref)`, `ratio error`, `efficiency`. Tức là **nhãn liên tục**, không chỉ nhị phân.
- Nhãn nhị phân mà bài 2025 dùng là **`efficiency ≥ 1`** (tương đương `substrate category ≥ signal ratio`), **không phải `category ≥ 1`** như bản gốc của tài liệu này ghi. Quy tắc `efficiency ≥ 1` tái tạo Supplementary Data 15 của họ ở mức 100,0000% (0 trên 47.607 ô lệch) `[tự đo]`; quy tắc `category = 1` chỉ cho 4 vị trí dương cho SIRT1, không phải 176. Số dương rất lệch nhau giữa các isoform:

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| Số vị trí dương (`efficiency ≥ 1`) | **176** | 1.901 | 1.844 | 1.038 | 2.614 | 1.199 | 1.692 |
| Trong đó chỉ dương với một isoform | 21 | 319 | 289 | 162 | **1.088** | 269 | 282 |
| Sai số trung vị của tỉ lệ tín hiệu | **0,37** | 0,22 | 0,24 | 0,24 | 0,21 | 0,27 | 0,22 |

(Hai dòng đầu đếm từ file nhãn của bài 2025, `All_Sirts_Feature_Y_labels.csv`, 6.801 dòng, 2.999 protein. Dòng thứ ba đếm từ file gốc của Rauh.) `[tự đo]`

- Phân bố số isoform dương trên mỗi vị trí: 1.107 vị trí âm với cả 7; 2.430 dương đúng 1 isoform; 2.087 dương 2; 902 dương 3; 226 dương 4; 44 dương 5; 5 dương 6 `[tự đo]`.

**Ba điều số liệu này nói ra:**

1. **SIRT1 gần như không dùng được ở ngưỡng nhị phân hiện tại** (176 dương trên 6.801, và sai số lớn nhất). Chính bài Rauh ghi rằng phép thử dựa trên **mất tín hiệu** nên thay đổi nhỏ khó đo, và các tác giả **từ chối diễn giải chi tiết tỉ lệ tín hiệu**. Dùng nhãn liên tục (hồi quy thứ tự) thay vì nhị phân là một cải tiến có lý do, không phải để cho khác.
2. **Lượng enzyme dùng cho mỗi isoform khác nhau** (bài ghi rõ, vì hoạt tính nội tại khác nhau), nên **không so trực tiếp được giữa các isoform**. Mô hình đa nhãn phải xử lý chuyện này, nếu không sẽ học ra "SIRT5 ăn tất".
3. Cấu trúc chia sẻ cơ chất giữa các isoform là thật và dày (2.087 vị trí dương với đúng 2 isoform), nên **một mô hình 7 đầu ra có cơ sở** để tốt hơn 7 mô hình rời — đúng chỗ bài 2025 bỏ trống.

### 2.2 Tập đánh giá độc lập nguồn: có, nhưng chỉ một lớp

`Supplementary Data 14` của [Ridgeway et al. 2025, Commun Chem](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) `[tự đo]`:

- **149 vị trí** acetyl hóa trong tế bào HCT116, đo bằng khối phổ với SIRT2 quá biểu hiện (OE) và knockdown (KD).
- **Cả 149 vị trí đều có log2(FC) < 0 ở OE và > 0 ở KD** — tức toàn bộ là vị trí **phụ thuộc SIRT2**: đây là tập **chỉ có nhãn dương**.
- Chỉ **46 trong 149 vị trí** nằm trong 6.801 vị trí của mảng; **123 protein**, trong đó 108 vị trí thuộc protein đã từng xuất hiện ở mảng `[tự đo]`.
- Mô hình của bài 2025 dự đoán dương **64/149**, tức **43,0%**. Vì cả 149 vị trí đều là dương tính đã biết, mẫu số là TP+FN, nên **43,0% là recall, không phải precision** `[tự đo]` — bản gốc của tài liệu này gọi sai. Tách theo rò rỉ: **52,3%** trên 44 vị trí cũng nằm trong mảng huấn luyện so với **39,0%** trên 105 vị trí ngoài mảng; **39,0% mới là mốc sạch**. (Con số SET8 37,4% = 885/2.367 của họ *đúng là* precision, nên cụm "37–43%" trong bài trộn hai đại lượng khác nhau.)

`Supplementary Data 13` là **dự đoán cho toàn bộ proteome: 145.461 vị trí × 7 isoform, có cả điểm số liên tục** `[tự đo]`. Nghĩa là baseline của bài 2025 **có sẵn dự đoán để so trực tiếp từng vị trí**, không cần chạy lại mô hình của họ. Đây là lợi thế lớn cho tiêu chí 2 của GVHD.

**Ý nghĩa:** tập test độc lập nguồn **tồn tại và tải được**. Trên riêng 149 vị trí này, chỉ đo được recall và độ giàu so với nền (không đo được precision, MCC hay AUPRC, vì không có âm tính). Nhưng xem 2.3: **nhãn âm trong tế bào đã có sẵn ở nguồn khác**, nên MCC và AUPRC trong tế bào vẫn đo được.

### 2.3 Nhãn âm trong tế bào: **đã có sẵn**, không còn là điểm nghẽn

- **Nhãn âm trong tế bào đã có sẵn, nằm trong chính bài mà baseline dùng** `[tự đo]`. Zhang 2022 (*Sci Rep*, [PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)) định lượng **2.846 vị trí trên 1.414 protein**, trong đó chỉ **152 vị trí phụ thuộc SIRT2** → **2.694 nhãn âm trong tế bào**, tỉ lệ nền dương ~5,3%. Nghĩa là **AUPRC và MCC trong tế bào đo được**, trái với điều bản gốc của tài liệu này kết luận. Thêm SIRT3: Sol 2012 (*PLoS ONE* 7:e50545) cho **3.174 vị trí người** (U2OS, KD so với OE, kèm cửa sổ 13 aa) và **1.566 vị trí chuột** (Sirt3 KO so với WT, 2 lần lặp). Cả hai đều **không có p-value từng vị trí và không chuẩn hóa theo lượng protein** — đó là giới hạn phải nói, không phải lý do để bỏ.
- PRIDE có hàng chục bộ acetylome liên quan sirtuin: tìm theo từ khóa, **SIRT1 23 bộ, SIRT2 15, SIRT3 24, SIRT5 9, SIRT6 9, SIRT7 7** có nhắc acetyl/succinyl/acyl trong tiêu đề hoặc mô tả `[tự đo, qua API PRIDE]`. Trong đó có đúng loại cần: ví dụ `PXD021357` (SIRT3 điều hòa acetyl hóa ty thể), `PXD023479` (SIRT3 nhân, lão hóa tế bào gốc), `PXD019763`/`PXD012796` (ức chế SIRT2, acetylome).
- **Nhãn âm định nghĩa được một cách sạch:** vị trí **được định lượng trong cùng thí nghiệm KO/KD nhưng không đổi** là âm trong tế bào cho isoform đó. Đây là nhãn âm có nghĩa, khác hẳn nhãn âm "chưa từng thấy" vẫn dùng trong các bài PTM.
- Bốn mã PRIDE nêu ở trên **phần lớn là chuột hoặc thí nghiệm ức chế bằng thuốc, và không mã nào cho bảng mức vị trí gọn** `[tự đo]`, nên đừng dựa vào chúng. Hai nguồn ở dòng đầu mục này mới là nguồn dùng được.
- Chưa lấy được bảng vị trí kèm fold-change từ các bài SIRT3 KO kinh điển (Rardin 2013 PNAS và Chen 2012 MCP bị reCAPTCHA chặn khi tải phụ lục từ PMC; bản mở trên Europe PMC không có). Một bài SIRT3-deficiency mở (`PMC9741511`) tải được phụ lục nhưng chỉ có hình, không có bảng vị trí `[tự đo]`. Không còn là việc chặn, vì Sol 2012 đã cho SIRT3 và Zhang 2022 đã cho SIRT2.

### 2.4 Người khác đã làm tới đâu

| Công trình | Làm gì | Chỗ còn trống |
|---|---|---|
| **Rauh 2013** (Nat Commun) | Mảng peptide, 6.802 vị trí × 7 isoform. Xác nhận lại trên **protein nguyên** cho 3 trường hợp (MDH với Sirt3; Prx1 với Sirt5; HMG-B1 với Sirt1) | Hoàn toàn **in vitro**; chính bài nói đây là "ứng viên", chưa phải cơ chất trong tế bào |
| **Ridgeway 2025** (Commun Chem) | 7 mô hình rời (LDA/decision tree) trên 443 đặc trưng làm tay, cửa sổ 13 aa. Precision 37–43% (SET8 và SIRT2). Dùng MusiteDeep làm bộ dự đoán phụ `[chưa kiểm]` | Chính tác giả ghi **"dùng PLM như ESM-2, ProtBERT" là việc tương lai**. Không có mô hình neural, không có mô hình đa nhãn, không dùng nhãn liên tục, không có ngữ cảnh ngoài peptide 13 aa, **không có bảo đảm thống kê** |
| **Deep-PLA 2020** (Brief Bioinform) | **Đã đọc toàn văn 08/10/2026. 9 HDAC của nó gồm HDAC1, HDAC2, HDAC3, HDAC6 và SIRT1, SIRT2, SIRT3, SIRT6, SIRT7**, ở **mức residue**, có web server (`deeppla.cancerbio.info`). Chỉ thiếu SIRT4 và SIRT5 — đúng hai isoform mà sinh học nói không phải deacetylase. Nhãn: **288 vị trí trên 134 protein** (SIRT1 184, SIRT2 52, SIRT3 30, SIRT6 10, SIRT7 12), text-mining từ PubMed | **Bản gốc của tài liệu này ghi sai "không phải sirtuin".** Nó phủ trọn SIRT1/2/3 — đúng ba isoform khả thi. Chỗ còn trống thật: báo **chỉ Sn/Sp/Pr/AUC, không có MCC, không có AUPRC**, và dữ liệu nhỏ tới mức "chỉ chạy được 5-fold CV cho SIRT3, SIRT6, SIRT7". MCC tự tính lại từ số của chính web server họ: SIRT1 0,403 · SIRT2 0,219 · SIRT3 **0,049** · SIRT6 0,321 · SIRT7 **−0,016** · HDAC gộp **0,557** `[tự đo]`. Ghi công đúng: tập test của họ là protein **không phải người**, một phép kiểm độc lập thật |
| **DeepSIRT 2021** (Comput Biol Chem 93:107514) | Dự đoán đích của **cả SIRT1–7** bằng CNN ở **mức protein**, MCC 0,82. Tác giả cuối Y.-Y. Ou `[chưa kiểm toàn văn]` | **Bài này vắng mặt trong bản scrape 14 bài danh mục GVHD**, nên bản scrape đó đã được chứng minh là không đầy đủ và **không được dùng làm bằng chứng tính mới**. Phân biệt trung thực: mức protein so với mức residue |
| **ASEB (~2012)** | Deep-PLA dẫn ASEB là đã được mở rộng thêm chức năng dự đoán cơ chất **HDAC lớp I và SIRT7** `[chưa kiểm toàn văn]` | Dự đoán cơ chất riêng cho SIRT7 có tiền lệ **trước 2020** |
| **NAD_MCNN 2025** (Chem Biol Drug Des) | **PLM + mCNN nhiều cửa sổ** cho vị trí gắn NAD+ của sirtuin, AUC 0,9733. Nhóm Prof. Ou (Yuan Ze) | Dự đoán vị trí **gắn cofactor trên chính enzyme**, không phải cơ chất. **Rất gần nền GVHD** — vừa là lợi thế (chứng minh khung PLM+mCNN chạy được trên sirtuin) vừa là cảnh báo (phải phân biệt rõ hai bài toán khi trình bày) |
| **SirtSAGE 2026** (GVHD) | Phân loại **chính protein sirtuin** ở mức toàn chuỗi, GATv2 + pLDDT + KAN | Mức protein, không phải mức residue. Cùng chủ đề, khác bài toán |

Tìm web ngày 08/10 **không ra bài nào** làm dự đoán cơ chất sirtuin đặc hiệu isoform bằng PLM, cũng không ra bài nào đánh giá dự đoán cơ chất sirtuin trên dữ liệu khối phổ trong tế bào `[chưa kiểm sâu]`.

### 2.5 Hai phép đo chuyển nhãn, cả hai cho kết quả gần như không chuyển được `[tự đo]`

Đây là số liệu quan trọng nhất của toàn bộ việc kiểm chứng, và nó **không có trong bản gốc 08/10**.

**Phép đo 1 — nhãn mảng so với sự phụ thuộc SIRT3 trong tế bào.** Nhãn SIRT3 của mảng Rauh 2013 so với Sol 2012 (U2OS): **MCC +0,047 đến +0,080** trên 1.417 vị trí khớp 13-mer, và **MCC −0,007** trên phần giao nghiêm ngặt theo UniProt + vị trí (n=718). Tập chuột cho kết quả như vậy. Giới hạn: đây là nhãn nhị phân thô của mảng, không phải một mô hình đã huấn luyện, và ngưỡng do người đo tự chọn.

**Phép đo 2 — nhãn mảng so với 289 vị trí cơ chất đã được y văn xác nhận** (Supplementary Table S1 của Deep-PLA, lọc sirtuin + người; khớp theo 13-mer trung tâm; kiểm định binomial chính xác so với tỉ lệ nền của chính isoform đó):

| Isoform | Curated | Trên mảng | Mảng gọi dương đúng isoform | % | Nền của mảng | Độ giàu | p |
|---|---|---|---|---|---|---|---|
| SIRT1 | 185 | 55 | 2 | 3,6% | 2,6% | 1,41× | 0,418 |
| SIRT2 | 52 | 18 | 5 | 27,8% | 27,9% | 0,99× | 0,595 |
| SIRT3 | 30 | 19 | 6 | 31,6% | 27,1% | 1,16× | 0,414 |
| SIRT6 | 10 | 9 | 2 | 22,2% | 17,6% | 1,26× | 0,489 |
| SIRT7 | 12 | 2 | 1 | 50,0% | 24,9% | 2,01× | 0,436 |
| **Gộp** | **289** | **103** | **16** | **15,5%** | — | **1,17×** | **0,291** |

Dương tính cho **ít nhất một** isoform: 85/103 = 82,5% so với nền toàn mảng 83,7% → **0,986×**. Tức là tập cơ chất đã được y văn xác nhận **không khác một mẫu ngẫu nhiên của mảng**, và không isoform nào đạt p < 0,05.

Phép đo 2 mạnh hơn phép đo 1 vì dương tính ở đây được xác nhận **trên protein cuộn gấp**, không suy ra từ ngưỡng fold-change, và không cần giả định ngưỡng nào. **Giới hạn phải nói kèm:** chỉ 103/289 (35,6%) vị trí curated có mặt trên mảng, nên phép kiểm bị giới hạn trong cách Rauh chọn peptide năm 2013; SIRT7 (n=2) và SIRT6 (n=9) quá nhỏ để trích riêng; khớp theo 13-mer trung tâm có thể bắt cùng trình tự ở paralog; nhãn của Deep-PLA là text-mining PubMed; tập 289 toàn dương tính nên chỉ tính được độ giàu, không tính được MCC.

Chi tiết: [sirtuin-substrate-deep-research.md](sirtuin-substrate-deep-research.md) mục 15 và ghi chú `research_notes/sirtuin-substrate/09-deep-pla-sites-vs-array.md`.

### 2.6 Lượng enzyme là biến gây nhiễu lớn chưa ai hiệu chỉnh `[tự đo]`

Rauh dùng **lượng enzyme khác nhau cho mỗi isoform** (trung vị 10–218 µg/ml) và viết thẳng rằng phép so sánh này **không thể cho biết isoform nào sẽ deacetyl hóa một vị trí một cách trội**. Đo được: Spearman **ρ = +0,811 giữa lượng enzyme và số nhãn dương, p = 0,0349** (hoán vị chính xác trên toàn bộ 5.040 phép hoán vị, vì n=7); ρ(số dương, `ratio error`) = **−0,855**. Nghịch lý SIRT5 (nhiều nhãn dương nhất) do đó có lời giải tầm thường: SIRT5 được cho nhiều enzyme nhất trong bảy.

Hai điều phải nói kèm, nếu không GVHD sẽ tìm ra: n=7 đặt p ngay ở mép, nên đây là **tín hiệu, không phải phán quyết**; và SIRT1 với SIRT7 cùng ở 20 µg/ml nhưng có 176 so với 1.692 nhãn dương, chênh ~10×. Cách nói đúng là "**lượng enzyme là một biến gây nhiễu hiệu ứng lớn chưa ai hiệu chỉnh**", **không phải** "cột SIRT5 chỉ là nồng độ enzyme".

Một lo ngại tự nêu cũng đã được **phản bác**: Supplementary Data 6 ("peptide không cho tín hiệu đáng kể ở ít nhất một đối chứng") có 220 peptide, **cả 220 vẫn nằm trong tập nhãn**, nhưng **185/220 (84,1%)** là dương với ít nhất một isoform — gần đúng tỉ lệ toàn mảng **83,7%**. Vậy chúng không làm thổi phồng chỉ số của lớp âm.

---

## 3. Vì sao đề tài chính nên đóng khung quanh "in vitro → trong tế bào"

Đây là chỗ khác biệt so với mọi bản phác trước, nên nói rõ.

**Vấn đề khoa học thật:** dữ liệu dồi dào (6.802 vị trí × 7 isoform) là **hoạt tính trên peptide 13 amino acid trong ống nghiệm**. Điều người làm sinh học cần biết là **lysine nào bị SIRT nào deacetyl hóa trong tế bào**. Hai thứ này không giống nhau: peptide không có cấu trúc, không có khu trú dưới tế bào, không có cạnh tranh enzyme, không có stoichiometry. Bằng chứng mạnh nhất cho khoảng cách này: Weinert 2015 (EMBO J) đo stoichiometry và kết luận phần lớn acetyl hóa ty thể là **tổn thương hóa học không do enzyme ở mức rất thấp**, SIRT3 đóng vai "sửa chữa" hơn là "điều hòa" `[chưa kiểm toàn văn]`. Nghĩa là một mô hình học nhãn in vitro rồi tuyên bố "đây là cơ chất sinh lý" là đang bỏ qua một bước.

**Đóng khung đề tài theo khoảng cách đó cho cả hai tính mới:**

- **Phần sinh học: KHÔNG còn tính mới, bỏ mọi tuyên bố "đầu tiên".** Dự đoán cơ chất deacetyl hóa đặc hiệu isoform ở mức residue **đã tồn tại từ 2020** (Deep-PLA, *Briefings in Bioinformatics* — tạp chí GVHD đọc), và ở mức protein từ 2021 (DeepSIRT). Tiền lệ bốn dòng: ASEB (~2012, SIRT7) → Deep-PLA (2020, residue, 5 isoform) → DeepSIRT (2021, protein, 7) → Ridgeway (2025, residue, 7). Điều còn mới là **phép đo**: chưa bài nào trong bốn bài đó báo MCC hay AUPRC, và chưa bài nào đánh giá lại trong tế bào trên một tập có nhãn âm `[chưa tìm thấy, không kết luận là chưa từng có]`. Chủ đề vẫn nằm đúng nhánh mới nhất của GVHD (sirtuin, lão hóa).
- **Mới ở phần tin học:** bài toán có đủ ba đặc tính khiến nó là bài toán máy học thật, không phải "thay đặc trưng cho đẹp":
  1. **Nhãn nhiễu và có thang độ.** Nhãn `efficiency ≥ 1` đã chuẩn hóa theo tỉ lệ tín hiệu, nên lập luận cũ "ngưỡng cứng làm mất các vị trí dương yếu của SIRT1" **không đứng được** — đó là lỗi của bản gốc, do nhận sai quy tắc nhãn. Tín hiệu thực sự chưa ai dùng là cột **`ratio error`** (SIRT1 trung vị 0,37, tệ nhất trong bảy). Có thể so trực tiếp: nhãn nhị phân vs nhãn thứ tự có trọng số theo `ratio error`.
  2. **Dịch chuyển miền (domain shift) in vitro → trong tế bào.** Huấn luyện trên mảng, đánh giá trên khối phổ. Đo được bằng recall trên 149 vị trí SIRT2 (so với 43,0%, hay 39,0% ngoài mảng, của bài 2025), và bằng MCC/AUPRC trên tập Zhang 2022 vốn đã có nhãn âm.
  3. **Đa nhãn có cấu trúc chia sẻ + hiệu chỉnh theo isoform.** 7 đầu ra, lượng enzyme khác nhau giữa các isoform nên phải hiệu chỉnh ngưỡng riêng; conformal theo từng isoform (Mondrian) trả về *tập* isoform có bảo đảm độ phủ, ví dụ "{SIRT2, SIRT3} ở mức 90%".

**Và nó giải quyết luôn điểm yếu cũ.** Trước đây "A không có tập test độc lập" là một lỗ hổng phải che. Nếu đề tài **là** câu hỏi chuyển miền, thì tập test trong tế bào là **sản phẩm đầu ra của đề tài**, và việc nó nhỏ, lệch, chỉ-một-lớp trở thành kết quả cần báo cáo, không phải điều phải giấu. GVHD đã nêu cổng dữ liệu từ buổi 1; câu trả lời "em dựng tập đánh giá trong tế bào từ dữ liệu KO/KD công khai, và đo cả độ phủ của nó" mạnh hơn câu "em tự chia 10%".

---

## 4. Đề tài chính, nói đủ để trình bày

### 4.1 Vào và ra

- **Vào:** một chuỗi protein người (dán vào website) hoặc một UniProt ID.
- **Ra:** với mỗi lysine, **7 điểm số** (một cho mỗi SIRT1–7) **và** một tập isoform có bảo đảm độ phủ ở mức tin cậy đặt trước, hoặc trả về "không đủ chắc".
- **Kiểu học:** đa nhãn 7 đầu ra, nhãn gốc là thang liên tục, mất cân bằng khác nhau theo từng isoform.

### 4.2 Hai (ba) câu hỏi nghiên cứu

- **RQ1 — biểu diễn và kiến trúc (tiêu chí 2, 3).** Thay 443 đặc trưng làm tay + 7 mô hình rời bằng **ESM-2 + mCNN nhiều cửa sổ, một mô hình 7 đầu ra**. Đo trên cùng cách chia theo protein. Bậc thang: (1) motif/PSSM, (2) one-hot + CNN, (3) đặc trưng làm tay + LDA/cây (chạy lại bài 2025), (4) ESM-2 đóng băng + mCNN, (5) ESM-2 + LoRA + mCNN, (6) thêm ngữ cảnh ngoài cửa sổ 13 aa (cửa sổ rộng hơn từ UniProt; khu trú dưới tế bào).
- **RQ2 — chuyển miền in vitro → trong tế bào (tiêu chí 1, 2). Đây là đóng góp chính, không phải RQ1.** Dạng đầy đủ: đo lại **cả ba** bộ dự đoán đã công bố (Deep-PLA, DeepSIRT, Ridgeway) cộng bậc thang baseline của đề tài, trên **một** tập đánh giá trong tế bào duy nhất có nhãn âm, bằng MCC và AUPRC, có kiểm soát rò rỉ ở mức protein và mức đồng dạng. Mô hình huấn luyện trên mảng dự đoán đúng bao nhiêu phần trăm vị trí phụ thuộc SIRT2 đo bằng khối phổ? So với **43,0%** (recall; 39,0% trên phần ngoài mảng huấn luyện) của bài 2025 trên **đúng 149 vị trí đó**. Nhãn liên tục, trọng số theo sai số, và hiệu chỉnh theo isoform có giúp không?
- **RQ3 — bảo đảm thống kê (tiêu chí 5).** Conformal theo từng isoform: độ phủ thực tế so với mức đặt trước, kích thước tập dự đoán, và **độ phủ có giữ được khi chuyển sang dữ liệu trong tế bào không**. Trả lời thẳng: **không bảo đảm nào chuyển được**, vì khoảng cách in vitro → trong tế bào là **dịch chuyển khái niệm (concept shift)**, không phải dịch chuyển hiệp biến, nên conformal có trọng số (Tibshirani 2019, arXiv:1904.06019) **không áp dụng được**. Bảo đảm trung thực duy nhất trong tế bào là **độ phủ của lớp dương cho SIRT2**, hiệu chuẩn trên một phần tập Zhang 2022. Đề cương phải nói rõ đang tuyên bố mức nào: biên (marginal), theo lớp (Mondrian), hay conformal risk control. Conformal cho PTM vẫn chưa thấy ai công bố, nhưng conformal trong QSAR đã thành thường lệ từ 2018, nên **đóng khung nó là công cụ đo cho RQ2, không phải đóng góp**.
- **Phụ — XAI có đáp án (tiêu chí 4).** Occlusion từng vị trí trong cửa sổ, rồi đối chiếu với đặc hiệu đã đo bằng thực nghiệm. **Câu về đặc hiệu SIRT7 ở vị trí −3, −2, +1 trong bản gốc đã bị xóa**: không truy được về toàn văn Rauh, có khả năng là một phát biểu về SIRT1 bị gán sai enzyme. Trước khi làm phần này phải dựng **bảng làm giàu residue theo từng vị trí trên 6.801 vị trí của mảng** để có đáp án tự đo, chứ không dẫn lại một câu không kiểm được. Lưu ý thêm: motif không khớp **không tự động** chứng minh phần diễn giải sai — có thể motif mới là thứ sai. Đây là phép kiểm trung thực mà luận văn T1 chưa có. Đáng nói kèm: Deep-PLA Figure S3 đo được AUC **không đổi đáng kể ngoài cửa sổ ±12 residue**, nên cửa sổ 13-mer có nguồn biện minh chứ không phải chọn tùy ý.

### 4.3 Cổng dừng

| Cổng | Khi nào | Ngưỡng | Làm gì nếu không qua |
|---|---|---|---|
| **Dữ liệu** | hết tuần 1 | **Cổng này coi như đã qua, không còn là cổng tồn tại mà là cổng giao thức.** Tập có cả dương và âm đã có cho SIRT2 (Zhang 2022: 152 dương / 2.694 âm) và SIRT3 (Sol 2012). Việc còn lại: chốt cách định nghĩa dương/âm/không xác định, và kiểm soát rò rỉ ở mức protein cộng mức đồng dạng (MMseqs2 `--min-seq-id 0.3 -c 0.8`) | Nếu phần kiểm soát rò rỉ làm tập test teo lại dưới mức dùng được → báo đúng điều đó như một kết quả, không chuyển đề tài |
| **Mô hình** | hết tuần 4 | ESM-2 + mCNN đa nhãn ≥ baseline đặc trưng làm tay trên cùng cách chia (MCC) cho ≥ 4/7 isoform | Báo kết quả âm, chuyển trọng tâm sang RQ2 và RQ3 |
| **SIRT1** | tuần 2 | 176 vị trí dương là ít cho một mô hình riêng, nên SIRT1 cần khoảng tin cậy và conformal theo lớp cho SIRT1 có thể thiếu lực | Giữ SIRT1 trong mô hình đa nhãn dùng biểu diễn chia sẻ, báo khoảng tin cậy thay vì một con số. **Bản gốc đặt cổng dừng sai chỗ:** SIRT1 là deacetylase chính danh nhất trong bảy; chỗ khung đề tài vỡ là **SIRT4/5/6/7** — Mathias 2014 (*Cell*) viết SIRT4 và SIRT5 ở ty thể "có rất ít hoặc không có hoạt tính deacetylase", Jiang 2013 (*Nature*) viết bốn trong bảy sirtuin "có hoạt tính deacetylase rất yếu in vitro", và SIRT7 về cơ bản chỉ deacetyl hóa H3K18ac |
| **Isoform** | tuần 2 | Phần định lượng chỉ giữ **SIRT1/2/3**. Đã đo: Spearman ρ giữa lượng enzyme dùng cho mỗi isoform và số nhãn dương là **+0,811, p = 0,0349** (hoán vị chính xác, n=7); ρ(số dương, `ratio error`) = **−0,855** `[tự đo]` | SIRT4–7 vào luận văn như **phân tích giới hạn của nhãn**, nội dung là bảng đó chứ không phải một lời xin lỗi: bốn isoform bị bỏ vì **đo được** rằng nhãn của chúng theo lượng enzyme và ngữ cảnh phép thử nhiều hơn theo đặc hiệu enzyme |

### 4.4 Câu hỏi cho GVHD tuần 6

1. **Câu quyết định (thay câu 1 của bản gốc): thầy có coi một kết quả âm — một phép đo cho thấy nhãn in vitro không chuyển được vào tế bào — là đóng góp chính của luận văn không?** Có → đề tài chính đã thu hẹp như trên. Không → chuyển sang đề tài dự phòng B, vốn thắng ở tiêu chí 4 vì có **đáp án định lượng cho XAI** (proline ở +1 trong 83% vị trí dương CDK so với 3% ở âm), còn sirtuin không có thứ tương đương.
2. Thầy có coi **tập đánh giá trong tế bào do em tự dựng từ dữ liệu khối phổ KO/KD công khai** là tập test độc lập đủ tiêu chuẩn không?
3. Nhãn huấn luyện là **hoạt tính trên peptide 13 amino acid trong ống nghiệm**, không phải trong tế bào. Thầy có chấp nhận đóng khung đề tài **chính là khoảng cách đó**, và chấp nhận kết quả có thể âm (mô hình không chuyển miền được) không?
4. Đóng góp chính nằm ở **chuyển miền + bảo đảm thống kê**, không phải "vượt SOTA về accuracy". Thầy đồng ý không?
5. Phần định lượng chỉ còn **SIRT1/2/3**, còn SIRT4–7 vào luận văn như phân tích giới hạn của nhãn (đã đo: ρ = +0,811 giữa lượng enzyme và số nhãn dương). Thầy thấy mức thu hẹp này hợp lý không?
6. **Deep-PLA 2020 đã dự đoán cơ chất cho SIRT1, 2, 3, 6, 7 ở mức residue.** Câu trả lời em chuẩn bị: đề tài này **không phải một bộ dự đoán mới**. Deep-PLA huấn luyện trên 288 vị trí curate từ y văn, Ridgeway trên 6.801 vị trí mảng peptide, DeepSIRT ở mức protein; **không bộ nào báo MCC hay AUPRC**, và không bộ nào đo lại trong tế bào với nhãn âm. Luận văn đo lại cả ba trên một tập dựng từ dữ liệu KO/KD công khai. Thầy thấy mức phân biệt này đủ để bảo vệ chưa?
7. Bài NAD_MCNN 2025 của nhóm Prof. Ou đã dùng PLM + mCNN cho **vị trí gắn NAD+ của sirtuin**. Đề tài này là **cơ chất**, khác bài toán. Thầy thấy mức phân biệt này đủ rõ chưa?

---

## 5. Vì sao không chọn những hướng còn lại

| Hướng | Vì sao không làm đề tài chính |
|---|---|
| **B (phospho theo nhóm kinase) + nén mô hình** | Vẫn là lựa chọn dự phòng tốt và đường dữ liệu rõ hơn. Nhưng: lĩnh vực đông, đối thủ trực tiếp Prot2Token (bioRxiv 2024.05.31.596915 + LMRL@ICLR 2025, **không phải NeurIPS 2025** như bản gốc ghi), GVHD chưa có bài PTM, và **tính mới sinh học mỏng** — đúng điều sinh viên nói muốn tránh. Tập train vẫn phải tự dựng từ OmniPath rồi lọc đồng dạng |
| **C6 đồng hồ methyl hóa (ComputAgeBench)** | Có benchmark chuẩn và tính mới tin học rõ. Nhưng **GVHD không có công trình methyl hóa nào** trong danh mục 14 bài, lệch xa khung PLM–mCNN, và từ khi có CpGPT/MethylGPT (2024–2025, mô hình nền cho methylome) thì "mô hình mới cho đồng hồ methyl" đã có đối thủ nặng `[chưa kiểm sâu]`. Bỏ ràng buộc GPU không cứu được phần lệch hướng GVHD |
| **C1 nén mô hình làm đóng góp chính** | Khi GPU không còn là ràng buộc, "chạy nhanh trên CPU" mất phần lớn động lực. Vẫn giữ được làm **một mục phụ** của website, không phải đóng góp chính |
| **C3 token cấu trúc (ProstT5/SaProt)** | Nhóm GVHD đã thử ProstT5 trong RAG-msCNN và ghi là không cải thiện đáng kể. Giữ làm một nhánh thí nghiệm |
| **4 hướng Cancer & Aging trước đó** | Đã loại; hướng 2 dừng sau khi chạy SenMayo trên GSE103322 thật (7/17 bệnh nhân, không đạt cổng 8, và điểm SenMayo chủ yếu phản ánh loại tế bào) |

---

## 6. Việc cần làm trước buổi gặp tuần 6, theo thứ tự

1. **Dựng tập đánh giá trong tế bào** (vẫn quan trọng nhất, nhưng không còn là câu hỏi "có hay không"). Nguồn đã xác nhận: Zhang 2022 cho SIRT2 (152 dương / 2.694 âm) và Sol 2012 cho SIRT3. Việc thật là chốt định nghĩa dương/âm/không xác định và kiểm soát rò rỉ ở mức protein cộng mức đồng dạng.
2. **Chạy lại baseline của bài 2025** trên cách chia theo protein, dùng chính file đặc trưng và nhãn trong repo của họ. Đây là mốc so sánh bắt buộc cho tiêu chí 2.
3. **Đọc ba bài:** Rauh 2013 (phần Methods, để hiểu nhãn thực sự đo gì), Ridgeway 2025 (phần sirtuin và Supplementary Data 13–15), Weinert 2015 (vì sao acetyl hóa trong tế bào khác in vitro).
4. **Mang 7 câu hỏi ở mục 4.4 đi hỏi GVHD.** Câu 1 — thầy có chấp nhận một kết quả âm làm đóng góp chính không — quyết định đi đề tài chính hay dự phòng. Chuẩn bị sẵn câu trả lời cho câu 6, vì GVHD đọc *Briefings in Bioinformatics* và có thể tự nêu Deep-PLA.
5. **Đọc toàn văn DeepSIRT và ASEB** để hoàn thiện bảng tiền lệ bốn dòng (cả hai còn `[chưa kiểm]`).

---

## 7. Điều tài liệu này chưa làm

- Chưa chạy mô hình nào, chưa có số thực nghiệm nào của riêng đề tài.
- Chưa lấy được bảng vị trí kèm fold-change cho isoform thứ hai → **cổng dữ liệu tuần 1 vẫn mở**.
- Deep-PLA **đã đọc toàn văn** (08/10/2026) và Supplementary Table S1 **đã tải và đo** (10/10/2026). Vẫn chưa đọc toàn văn Weinert 2015, NAD_MCNN, **DeepSIRT và ASEB**; chưa đọc phần Methods của Ridgeway 2025 ngoài các đoạn đã trích. Chưa mở `table_s4.xlsx` (1,6 MB, dự đoán toàn PLMD) và `table_s5.xlsx` của Deep-PLA.
- Chưa dựng **bảng làm giàu residue theo từng vị trí** trên 6.801 vị trí của mảng, nên chưa quyết được phần XAI có đáng làm hay không.
- Các nhận định "không tìm thấy bài nào làm X" chỉ dựa trên vài lượt tìm web và PubMed ngày 08/10/2026.
- Chưa đối chiếu với danh mục đầy đủ của GVHD (bản scrape chỉ có 14 bài).

## 8. Nguồn

- Rauh et al. (2013), *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327 — https://www.nature.com/articles/ncomms3327
- Ridgeway et al. (2025), *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) · mã và nhãn: https://github.com/nashirag/ML-Hybrid_Ensemble_Method
- Yu et al. (2020), *Deep learning based prediction of reversible HAT/HDAC-specific lysine acetylation*, Brief Bioinform 21(5):1798 — [DOI](https://doi.org/10.1093/bib/bbz107) (theo PubMed)
- Le, Ou et al. (2025), *NAD_MCNN: Combining Protein Language Models and Multiwindow Convolutional Neural Networks for Deacetylase NAD+ Binding Site Prediction*, Chem Biol Drug Des 105(4):e70085 — [DOI](https://doi.org/10.1111/cbdd.70085) (theo PubMed)
- Weinert et al. (2015), *Analysis of acetylation stoichiometry suggests that SIRT3 repairs nonenzymatic acetylation lesions*, EMBO J — https://doi.org/10.15252/embj.201591271
- Zhang et al. (2022), acetylome phụ thuộc SIRT2 trong tế bào — [PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)
- Sol et al. (2012), *PLoS ONE* 7:e50545 — acetylome SIRT3 (U2OS KD so với OE; MEF chuột Sirt3 KO)
- Shi, Ou et al. (2021), *DeepSIRT*, Comput Biol Chem 93:107514 — https://doi.org/10.1016/j.compbiolchem.2021.107514 (theo PubMed)
- Mathias et al. (2014), *Cell* — https://doi.org/10.1016/j.cell.2014.11.046 · Jiang et al. (2013), *Nature* — https://doi.org/10.1038/nature12038 · Barber et al. (2012), *Nature* — https://doi.org/10.1038/nature11043
- Tibshirani et al. (2019), conformal prediction under covariate shift — arXiv:1904.06019
- Prot2Token — bioRxiv 2024.05.31.596915, LMRL@ICLR 2025
- PRIDE Archive, API tìm kiếm — https://www.ebi.ac.uk/pride/archive
- CpGPT — https://www.biorxiv.org/content/10.1101/2024.10.24.619766 · MethylGPT — https://www.biorxiv.org/content/10.1101/2024.10.30.621013
