# Chốt đề tài trước buổi gặp tuần 6: một đề tài chính, một dự phòng

Ngày: **08/10/2026**. Yêu cầu của sinh viên: chốt **một** đề tài hiểu rõ trước buổi gặp tuần 6, cộng **một** dự phòng; ưu tiên đề tài có tính mới **cả phần sinh học lẫn phần tin học**; **không còn ràng buộc GPU và thời gian**; tiêu chí quyết định là **ý nghĩa và giá trị khoa học thật**.

Nhãn bằng chứng: `[tự đo]` = số Claude tự tải file và đếm trong phiên này; `[chưa kiểm]` = chỉ thấy qua tóm tắt hoặc suy luận.

Tài liệu nền: [compute-novelty-directions.md](compute-novelty-directions.md) · [b-method-layer-draft.md](b-method-layer-draft.md) · [advisor-4-directions-analysis.md](advisor-4-directions-analysis.md) · candidates-a-b-explained.md (chỉ có trong thư mục dự án, không nằm trong repo)

---

## 1. Kết luận: khuyến nghị gì

**Đề tài chính (khuyến nghị): dự đoán cơ chất deacetyl hóa theo từng isoform SIRT1–7, với câu hỏi trung tâm là chuyển từ nhãn in vitro sang dự đoán trong tế bào.**

Tên đề tài tạm: *Dự đoán cơ chất deacetyl hóa đặc hiệu isoform của SIRT1–7 bằng PLM–mCNN đa nhãn, học từ dữ liệu mảng peptide in vitro và đánh giá trên dữ liệu khối phổ trong tế bào, kèm dự đoán có bảo đảm thống kê.*

**Đề tài dự phòng: B + lớp cải tiến tin học** — dự đoán vị trí phospho theo nhóm kinase, mô hình thầy ESM-2+LoRA+mCNN chưng cất thành mô hình nhỏ chạy CPU, kèm conformal. Bản phác đã có: [b-method-layer-draft.md](b-method-layer-draft.md) (PR #8).

Khác biệt quan trọng so với bản phác trước: đề tài chính **không còn là "A + thêm vài kỹ thuật tin học"**. Điểm yếu lớn nhất của A trước đây — *không có tập test độc lập* — được chuyển thành **chính câu hỏi nghiên cứu**. Lý do ở mục 3.

---

## 2. Số liệu tự đo trong phiên này

Tất cả tải được từ môi trường cloud ngày 08/10/2026.

### 2.1 Nhãn huấn luyện: mảng peptide Rauh 2013

File `Supplementary Data 1` của [Rauh et al. 2013, Nat Commun 4:2327](https://www.nature.com/articles/ncomms3327) (2,1 MB, tải trực tiếp từ Springer, mã 200) `[tự đo]`:

- **6.802 vị trí acetyl hóa**, mỗi vị trí là một peptide 13 amino acid (6 residue mỗi bên).
- Mỗi vị trí có **4 cột cho mỗi isoform**: `substrate category`, `signal ratio (exp:ref)`, `ratio error`, `efficiency`. Tức là **nhãn liên tục**, không chỉ nhị phân.
- Nhãn nhị phân mà bài 2025 dùng (`category ≥ 1`) cho số dương rất lệch nhau giữa các isoform:

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| Số vị trí dương (`category = 1`) | **176** | 1.901 | 1.844 | 1.038 | 2.614 | 1.199 | 1.692 |
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
- Mô hình của bài 2025 dự đoán dương **64/149**, đúng mức **precision 43,0%** họ báo.

`Supplementary Data 13` là **dự đoán cho toàn bộ proteome: 145.461 vị trí × 7 isoform, có cả điểm số liên tục** `[tự đo]`. Nghĩa là baseline của bài 2025 **có sẵn dự đoán để so trực tiếp từng vị trí**, không cần chạy lại mô hình của họ. Đây là lợi thế lớn cho tiêu chí 2 của GVHD.

**Ý nghĩa:** tập test độc lập nguồn **tồn tại và tải được**, nhưng **thiếu nhãn âm**. Với 149 vị trí dương, đo được precision (so trực tiếp 43,0%) nhưng chưa đo được MCC/AUPRC.

### 2.3 Nhãn âm trong tế bào: nguồn có, chưa xác nhận file

- PRIDE có hàng chục bộ acetylome liên quan sirtuin: tìm theo từ khóa, **SIRT1 23 bộ, SIRT2 15, SIRT3 24, SIRT5 9, SIRT6 9, SIRT7 7** có nhắc acetyl/succinyl/acyl trong tiêu đề hoặc mô tả `[tự đo, qua API PRIDE]`. Trong đó có đúng loại cần: ví dụ `PXD021357` (SIRT3 điều hòa acetyl hóa ty thể), `PXD023479` (SIRT3 nhân, lão hóa tế bào gốc), `PXD019763`/`PXD012796` (ức chế SIRT2, acetylome).
- **Nhãn âm định nghĩa được một cách sạch:** vị trí **được định lượng trong cùng thí nghiệm KO/KD nhưng không đổi** là âm trong tế bào cho isoform đó. Đây là nhãn âm có nghĩa, khác hẳn nhãn âm "chưa từng thấy" vẫn dùng trong các bài PTM.
- **Chưa xác nhận:** chưa lấy được bảng vị trí kèm fold-change từ các bài SIRT3 KO kinh điển (Rardin 2013 PNAS và Chen 2012 MCP bị reCAPTCHA chặn khi tải phụ lục từ PMC; bản mở trên Europe PMC không có). Một bài SIRT3-deficiency mở (`PMC9741511`) tải được phụ lục nhưng chỉ có hình, không có bảng vị trí `[tự đo]`. **Đây là việc tuần 1 phải làm xong.**

### 2.4 Người khác đã làm tới đâu

| Công trình | Làm gì | Chỗ còn trống |
|---|---|---|
| **Rauh 2013** (Nat Commun) | Mảng peptide, 6.802 vị trí × 7 isoform. Xác nhận lại trên **protein nguyên** cho 3 trường hợp (MDH với Sirt3; Prx1 với Sirt5; HMG-B1 với Sirt1) | Hoàn toàn **in vitro**; chính bài nói đây là "ứng viên", chưa phải cơ chất trong tế bào |
| **Ridgeway 2025** (Commun Chem) | 7 mô hình rời (LDA/decision tree) trên 443 đặc trưng làm tay, cửa sổ 13 aa. Precision 37–43% (SET8 và SIRT2). Dùng MusiteDeep làm bộ dự đoán phụ `[chưa kiểm]` | Chính tác giả ghi **"dùng PLM như ESM-2, ProtBERT" là việc tương lai**. Không có mô hình neural, không có mô hình đa nhãn, không dùng nhãn liên tục, không có ngữ cảnh ngoài peptide 13 aa, **không có bảo đảm thống kê** |
| **Deep-PLA 2020** (Brief Bioinform) | Dự đoán acetyl hóa đặc hiệu **HAT/HDAC** (không phải sirtuin), mạng neural + đặc trưng chuỗi, có web server | Khác họ enzyme; không phải isoform sirtuin. Cho thấy bài toán "đặc hiệu enzyme" đã có tiền lệ 2020, nên phải nói "mới ở họ sirtuin", không nói "mới hoàn toàn" |
| **NAD_MCNN 2025** (Chem Biol Drug Des) | **PLM + mCNN nhiều cửa sổ** cho vị trí gắn NAD+ của sirtuin, AUC 0,9733. Nhóm Prof. Ou (Yuan Ze) | Dự đoán vị trí **gắn cofactor trên chính enzyme**, không phải cơ chất. **Rất gần nền GVHD** — vừa là lợi thế (chứng minh khung PLM+mCNN chạy được trên sirtuin) vừa là cảnh báo (phải phân biệt rõ hai bài toán khi trình bày) |
| **SirtSAGE 2026** (GVHD) | Phân loại **chính protein sirtuin** ở mức toàn chuỗi, GATv2 + pLDDT + KAN | Mức protein, không phải mức residue. Cùng chủ đề, khác bài toán |

Tìm web ngày 08/10 **không ra bài nào** làm dự đoán cơ chất sirtuin đặc hiệu isoform bằng PLM, cũng không ra bài nào đánh giá dự đoán cơ chất sirtuin trên dữ liệu khối phổ trong tế bào `[chưa kiểm sâu]`.

---

## 3. Vì sao đề tài chính nên đóng khung quanh "in vitro → trong tế bào"

Đây là chỗ khác biệt so với mọi bản phác trước, nên nói rõ.

**Vấn đề khoa học thật:** dữ liệu dồi dào (6.802 vị trí × 7 isoform) là **hoạt tính trên peptide 13 amino acid trong ống nghiệm**. Điều người làm sinh học cần biết là **lysine nào bị SIRT nào deacetyl hóa trong tế bào**. Hai thứ này không giống nhau: peptide không có cấu trúc, không có khu trú dưới tế bào, không có cạnh tranh enzyme, không có stoichiometry. Bằng chứng mạnh nhất cho khoảng cách này: Weinert 2015 (EMBO J) đo stoichiometry và kết luận phần lớn acetyl hóa ty thể là **tổn thương hóa học không do enzyme ở mức rất thấp**, SIRT3 đóng vai "sửa chữa" hơn là "điều hòa" `[chưa kiểm toàn văn]`. Nghĩa là một mô hình học nhãn in vitro rồi tuyên bố "đây là cơ chất sinh lý" là đang bỏ qua một bước.

**Đóng khung đề tài theo khoảng cách đó cho cả hai tính mới:**

- **Mới ở phần sinh học:** chưa có mô hình nào dự đoán cơ chất **theo từng isoform** SIRT1–7 bằng biểu diễn học sâu, và chưa có bài nào **đo xem dự đoán từ mảng in vitro có đúng trong tế bào không** ở mức hệ thống. Chủ đề nằm đúng nhánh mới nhất của GVHD (sirtuin, lão hóa).
- **Mới ở phần tin học:** bài toán có đủ ba đặc tính khiến nó là bài toán máy học thật, không phải "thay đặc trưng cho đẹp":
  1. **Nhãn nhiễu và có thang độ.** Dùng `signal ratio` và `ratio error` làm trọng số hoặc làm nhãn thứ tự, thay vì ngưỡng cứng `category ≥ 1` làm mất 2.438 vị trí dương yếu của SIRT1. Có thể so trực tiếp: nhãn nhị phân vs nhãn thứ tự có trọng số sai số.
  2. **Dịch chuyển miền (domain shift) in vitro → trong tế bào.** Huấn luyện trên mảng, đánh giá trên khối phổ. Đo được bằng precision trên 149 vị trí SIRT2 (so với 43,0% của bài 2025), và bằng MCC khi dựng được nhãn âm.
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
- **RQ2 — chuyển miền in vitro → trong tế bào (tiêu chí 1, 2).** Mô hình huấn luyện trên mảng dự đoán đúng bao nhiêu phần trăm vị trí phụ thuộc SIRT2 đo bằng khối phổ? So với **43,0%** của bài 2025 trên **đúng 149 vị trí đó**. Nhãn liên tục, trọng số theo sai số, và hiệu chỉnh theo isoform có giúp không?
- **RQ3 — bảo đảm thống kê (tiêu chí 5).** Conformal theo từng isoform: độ phủ thực tế so với mức đặt trước, kích thước tập dự đoán, và **độ phủ có giữ được khi chuyển sang dữ liệu trong tế bào không** (dự đoán: không, và đó là kết quả đáng báo cáo).
- **Phụ — XAI có đáp án (tiêu chí 4).** Occlusion từng vị trí trong cửa sổ, rồi đối chiếu với đặc hiệu đã đo bằng thực nghiệm: Rauh báo SIRT7 ưa residue thân nước không tích điện hoặc tích điện âm ở vị trí −3, −2, +1; SIRT6 có túi gắn phần lớn thân dầu. Nếu bản đồ occlusion không khớp, XAI đang sai. Đây là phép kiểm trung thực mà luận văn T1 chưa có.

### 4.3 Cổng dừng

| Cổng | Khi nào | Ngưỡng | Làm gì nếu không qua |
|---|---|---|---|
| **Dữ liệu** | hết tuần 1 | Dựng được tập đánh giá trong tế bào có **cả dương và âm** cho **ít nhất 2 isoform** (SIRT2 từ bài 2025, cộng ≥1 isoform từ acetylome KO công khai) | RQ2 chỉ còn đo precision trên 149 vị trí dương. Nếu cả việc đó cũng không được → **chuyển sang đề tài dự phòng** |
| **Mô hình** | hết tuần 4 | ESM-2 + mCNN đa nhãn ≥ baseline đặc trưng làm tay trên cùng cách chia (MCC) cho ≥ 4/7 isoform | Báo kết quả âm, chuyển trọng tâm sang RQ2 và RQ3 |
| **SIRT1** | tuần 2 | 176 vị trí dương là quá ít cho mô hình riêng | Bỏ SIRT1 khỏi phần định lượng, hoặc chỉ dùng nhãn liên tục cho SIRT1, và nói rõ trong luận văn |

### 4.4 Câu hỏi cho GVHD tuần 6

1. Thầy có coi **tập đánh giá trong tế bào do em tự dựng từ dữ liệu khối phổ KO/KD công khai** là tập test độc lập đủ tiêu chuẩn không? (Đây là câu quan trọng nhất; nó quyết định đề tài chính hay dự phòng.)
2. Nhãn huấn luyện là **hoạt tính trên peptide 13 amino acid trong ống nghiệm**, không phải trong tế bào. Thầy có chấp nhận đóng khung đề tài **chính là khoảng cách đó**, và chấp nhận kết quả có thể âm (mô hình không chuyển miền được) không?
3. Đóng góp chính nằm ở **chuyển miền + bảo đảm thống kê**, không phải "vượt SOTA về accuracy". Thầy đồng ý không?
4. SIRT1 chỉ có 176 vị trí dương ở ngưỡng công bố. Thầy muốn bỏ SIRT1 hay giữ với nhãn thang liên tục?
5. Bài NAD_MCNN 2025 của nhóm Prof. Ou đã dùng PLM + mCNN cho **vị trí gắn NAD+ của sirtuin**. Đề tài này là **cơ chất**, khác bài toán. Thầy thấy mức phân biệt này đủ rõ chưa?

---

## 5. Vì sao không chọn những hướng còn lại

| Hướng | Vì sao không làm đề tài chính |
|---|---|
| **B (phospho theo nhóm kinase) + nén mô hình** | Vẫn là lựa chọn dự phòng tốt và đường dữ liệu rõ hơn. Nhưng: lĩnh vực đông, đối thủ trực tiếp Prot2Token (NeurIPS 2025), GVHD chưa có bài PTM, và **tính mới sinh học mỏng** — đúng điều sinh viên nói muốn tránh. Tập train vẫn phải tự dựng từ OmniPath rồi lọc đồng dạng |
| **C6 đồng hồ methyl hóa (ComputAgeBench)** | Có benchmark chuẩn và tính mới tin học rõ. Nhưng **GVHD không có công trình methyl hóa nào** trong danh mục 14 bài, lệch xa khung PLM–mCNN, và từ khi có CpGPT/MethylGPT (2024–2025, mô hình nền cho methylome) thì "mô hình mới cho đồng hồ methyl" đã có đối thủ nặng `[chưa kiểm sâu]`. Bỏ ràng buộc GPU không cứu được phần lệch hướng GVHD |
| **C1 nén mô hình làm đóng góp chính** | Khi GPU không còn là ràng buộc, "chạy nhanh trên CPU" mất phần lớn động lực. Vẫn giữ được làm **một mục phụ** của website, không phải đóng góp chính |
| **C3 token cấu trúc (ProstT5/SaProt)** | Nhóm GVHD đã thử ProstT5 trong RAG-msCNN và ghi là không cải thiện đáng kể. Giữ làm một nhánh thí nghiệm |
| **4 hướng Cancer & Aging trước đó** | Đã loại; hướng 2 dừng sau khi chạy SenMayo trên GSE103322 thật (7/17 bệnh nhân, không đạt cổng 8, và điểm SenMayo chủ yếu phản ánh loại tế bào) |

---

## 6. Việc cần làm trước buổi gặp tuần 6, theo thứ tự

1. **Dựng tập đánh giá trong tế bào** (quan trọng nhất, quyết định đề tài). Lấy 149 vị trí SIRT2 từ Supplementary Data 14; tìm bảng vị trí kèm fold-change cho ≥1 isoform nữa từ acetylome KO công khai (ưu tiên các bộ PRIDE đã liệt kê ở 2.3, hoặc phụ lục Rardin 2013 / Chen 2012 nếu tải được từ máy sinh viên — môi trường cloud bị reCAPTCHA chặn).
2. **Chạy lại baseline của bài 2025** trên cách chia theo protein, dùng chính file đặc trưng và nhãn trong repo của họ. Đây là mốc so sánh bắt buộc cho tiêu chí 2.
3. **Đọc ba bài:** Rauh 2013 (phần Methods, để hiểu nhãn thực sự đo gì), Ridgeway 2025 (phần sirtuin và Supplementary Data 13–15), Weinert 2015 (vì sao acetyl hóa trong tế bào khác in vitro).
4. **Mang 5 câu hỏi ở mục 4.4 đi hỏi GVHD.** Câu 1 quyết định đi đề tài chính hay dự phòng.

---

## 7. Điều tài liệu này chưa làm

- Chưa chạy mô hình nào, chưa có số thực nghiệm nào của riêng đề tài.
- Chưa lấy được bảng vị trí kèm fold-change cho isoform thứ hai → **cổng dữ liệu tuần 1 vẫn mở**.
- Chưa đọc toàn văn Weinert 2015, Deep-PLA, NAD_MCNN (chỉ đọc tóm tắt); chưa đọc phần Methods của Ridgeway 2025 ngoài các đoạn đã trích.
- Các nhận định "không tìm thấy bài nào làm X" chỉ dựa trên vài lượt tìm web và PubMed ngày 08/10/2026.
- Chưa đối chiếu với danh mục đầy đủ của GVHD (bản scrape chỉ có 14 bài).

## 8. Nguồn

- Rauh et al. (2013), *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327 — https://www.nature.com/articles/ncomms3327
- Ridgeway et al. (2025), *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem — [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) · mã và nhãn: https://github.com/nashirag/ML-Hybrid_Ensemble_Method
- Yu et al. (2020), *Deep learning based prediction of reversible HAT/HDAC-specific lysine acetylation*, Brief Bioinform 21(5):1798 — [DOI](https://doi.org/10.1093/bib/bbz107) (theo PubMed)
- Le, Ou et al. (2025), *NAD_MCNN: Combining Protein Language Models and Multiwindow Convolutional Neural Networks for Deacetylase NAD+ Binding Site Prediction*, Chem Biol Drug Des 105(4):e70085 — [DOI](https://doi.org/10.1111/cbdd.70085) (theo PubMed)
- Weinert et al. (2015), *Analysis of acetylation stoichiometry suggests that SIRT3 repairs nonenzymatic acetylation lesions*, EMBO J — https://doi.org/10.15252/embj.201591271
- PRIDE Archive, API tìm kiếm — https://www.ebi.ac.uk/pride/archive
- CpGPT — https://www.biorxiv.org/content/10.1101/2024.10.24.619766 · MethylGPT — https://www.biorxiv.org/content/10.1101/2024.10.30.621013
