# Thiết kế thí nghiệm và nội dung dữ liệu của thư viện degron NUCLEAR (Larsen et al., bioRxiv 2025)

> Đối tượng: Fia B. Larsen, Vasileios Voutsinos, …, Kresten Lindorff-Larsen, Rasmus Hartmann-Petersen,
> "Comprehensive degron mapping in human transcription factors", bioRxiv, DOI
> [10.1101/2025.05.16.654404](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full).
> Hiện trạng tháng 10/2026: **chưa tìm thấy bản bình duyệt**; mọi số dưới đây là của bản tiền ấn phẩm v1.
>
> **Nhãn bằng chứng dùng trong file này** (theo quy ước repo):
> `[bài báo]` = đọc trực tiếp trong toàn văn bioRxiv v1 qua WebFetch · `[README repo]` = đọc trong README
> GitHub của nhóm tác giả · `[tóm tắt]` = chỉ thấy qua tóm tắt tìm kiếm, **chưa xác minh** ·
> `[tự đo]` = tôi tự tính trong phiên này trên dữ liệu đã có trên máy / file metadata nhỏ tải từ GitHub ·
> `[suy luận]` = diễn giải của tôi, không phải câu của tác giả.

## 1. Thiết kế assay: hệ báo cáo, tile, số bin, công thức điểm, quan hệ với PSI của GPS

### Takeaway

Đây **không phải GPS**. Đây là sort-seq trên hệ báo cáo độ dồi dào GFP–tile (GFP có NLS ở đầu N) chuẩn hoá
bằng mCherry, tích hợp đơn bản sao qua landing pad Bxb1 trong HEK293T, phân loại vào **4 gate FACS mỗi
gate 25% dân số**. Tile dài **30 residue, bước 15 residue**. Điểm thô vẫn gọi là **PSI** (protein stability
index) tính từ tần suất tile trong 4 gate, nhưng sau đó được **chuẩn hoá lại thành "degron score" trên
thang 0–1**, hướng **ngược** với PSI của GPS: gần 1 = degron mạnh.

### Cited Findings

- Hệ báo cáo: vector gắn mỗi tile vào **đầu C của GFP**, GFP có **NLS ở đầu N**; **mCherry biểu hiện cùng
  qua IRES** làm chuẩn hoá; tích hợp bằng **Bxb1 vào landing pad trong HEK293T**. Bài báo **không dùng
  GPS**. `[bài báo]` — [bioRxiv v1 full text](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full)
- Số bin: tế bào được "sorted into 4 bins based on their GFP:mCherry ratio ensuring 25% of the population
  in each bin." `[bài báo]`
- Tile: "The library was designed as 90 nt (30 residues) tiles overlapping with 45 nt (15 residues)" →
  **bước 15 residue**. Tile đầu C dài **29 residue**. `[bài báo]`
- Ba thư viện con **không chồng nhau**: **odds 31.080 tile**, **evens 30.292 tile**, **C-terminal 1.620
  tile**. Oligo Twist + lắp Gibson, **5 lần biến nạp mỗi thư viện**, độ phủ **≥ 100 lần**. `[bài báo]`
- Quy mô: **1.626 TF**, **62.992 tile** trong thân bài; Methods ghi **63.230 tile thiết kế**, trong đó
  **62.992 / 62.808 là duy nhất ở mức nucleotide / acid amin** (không tính peptide đối chứng). `[bài báo]`
- Công thức: "the protein stability index (PSI) was calculated per tile using: [công thức là ảnh nhúng,
  không render trong HTML] where f_t,g is the frequency of tile t in FACS gate g." `[bài báo]`
- Chuẩn hoá: "normalizing each replicate such that the median of the stable peak has degron score zero"
  và đỉnh bất ổn nhất nhận điểm 1; "The three libraries are combined by averaging normalized scores over
  replicates." `[bài báo]`
- Hướng và thang: "Degron scores close to zero indicate low degron potency, while scores close to one
  indicate high degron potency." `[bài báo]`
- Điểm thứ hai: "An abundance score is obtained by transforming (non-linearly) the degron scores to the
  fluorescence distribution" — abundance score đi **ngược** chiều degron score. `[bài báo]`
- Độ phủ cuối: **có điểm cho 58.781 tile**, được mô tả là **93% của TF proteome**; Methods nói các điểm
  này ứng với **58.992 tile** trong thư viện có dư thừa. `[bài báo]`
- Ngưỡng degron của bài chị em (bào tương) để tham chiếu: "Degron thresholds in the paper are given in
  Abundance score units, **0.04 and 0.22**, but may be translated to the degron score, **0.93 and 0.43**,
  because the non-linear transformation is monotonic." `[README repo]` —
  [_2025_Voutsinos_degron_cytosol](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol)
- Thư viện bào tương (Voutsinos, cùng assay): phân bố ba lớp **19% strong degron, 30% intermediate, 51%
  non-degron** trên >200.000 peptide của >5.000 protein bào tương. `[tóm tắt]` —
  [kết quả tìm kiếm](https://www.biorxiv.org/content/10.1101/2025.05.10.653233.full.pdf)

### Inferences

- `[suy luận]` Khái niệm PSI là **cùng họ** với PSI của GPS (đều là trung bình có trọng số vị trí gate /
  bin của một peptide), nhưng **không cùng thang**: Larsen dùng **4 gate** rồi chuẩn hoá tuyến tính về
  0–1 với dấu đảo, còn bảng PSI của bộ GPS Zhang 2023 mà đề tài đang dùng có **6 bin** (`nb1…nb6` trong
  `data/processed/psi-rep1.tsv` `[tự đo]`) và thang xấp xỉ 1–6 với **giá trị thấp = bất ổn**. Muốn ghép hai
  nguồn nhãn phải chuẩn hoá lại theo phân vị, **không** map tuyến tính.
- `[suy luận]` Vì đây là **abundance reporter nội bào có NLS**, nhãn mang nghĩa "độ dồi dào ở trạng thái
  dừng trong môi trường nhân", không phải "tốc độ phân rã". Dùng làm test ngoại không đổi định nghĩa bài
  toán của đề tài (degron footprint), nhưng khác **ngăn tế bào** và khác **dòng tế bào** so với GPS.
- `[suy luận]` 58.781 / 62.992 ≈ **93,3%** tile thiết kế có điểm — khớp với con số "93% of the TF proteome"
  tác giả nêu.

### Gaps

- Công thức PSI chính xác là **ảnh nhúng** trong HTML nên tôi không đọc được dạng đại số; muốn có thì phải
  mở PDF hoặc `score/` trong repo GitHub. Không mở trong phiên này.
- Không rõ tỷ lệ tile rơi vào ba lớp strong/intermediate/non-degron cho **thư viện nhân** (bài chỉ cho
  21.970 tile có degron score > 0,5 — xem mục 5; `21.970 / 58.781 = 37,4%` `[tự đo, phép chia]`).

## 2. Lặp lại và nhiễu — câu hỏi then chốt

### Takeaway

Độ lặp **mức tile** rất cao: **Pearson trung bình 0,97, khoảng 0,91–0,99** giữa mọi cặp replicate, 3
replicate sinh học × 2 replicate FACS = 6 replicate mỗi thư viện con, lọc **≥ 100 read trên 4 gate**, và
tác giả **công bố SD giữa các replicate làm sai số từng tile**. Nhưng **mọi con số này là mức tile trên
toàn dải động**, nên **không so sánh trực tiếp** được với Jaccard ≈ 0,50 mức residue mà đề tài đã đo: bài
báo **không** báo bất kỳ thước đo lặp lại nào ở mức residue, vì thí nghiệm không có nhãn mức residue.

### Cited Findings

- Replicate: **3 replicate sinh học** (các lần transfection riêng), mỗi cái có **2 replicate FACS** → **6
  replicate mỗi thư viện con**; **một replicate của thư viện C-terminal bị lỗi**. `[bài báo]`
- Tương quan: "with an average PSI Pearson correlation of **0.97** between all replicate pairs (range
  **0.91-0.99**)." `[bài báo]`
- Lọc read: "We require **100 or more reads across the four gates**." Chỉ "sequencing reads with an exact
  match to the library (or controls) were counted". `[bài báo]`
- Sai số công bố: "We require **two or more replicate measurements** per tile and report the **standard
  deviation between replicates as score uncertainties**." `[bài báo]`
- Độ phủ mỗi replicate: **96–98%** thành viên thư viện. `[bài báo]`
- Kiểm chứng thông lượng thấp: **Pearson −0,93** với flow cytometry trên **82 tile** đo riêng (dấu âm vì
  hai thang ngược chiều). `[bài báo]`
- Bài chị em (bào tương, cùng assay, để làm mốc): technical replicate theo read **Pearson trung bình 0,98
  (khoảng 0,79–0,99)**; cặp replicate PSI **Pearson trung bình 0,98 (0,96–0,99)**; **4.573 cặp tile giống
  nhau hoàn toàn** được đo ở hai thư viện khác nhau cho **PSI Pearson > 0,99**; kiểm flow trên **164 tile**
  cho **Spearman ρ = −0,968**. `[bài báo]` —
  [Voutsinos bioRxiv v1](https://www.biorxiv.org/content/10.1101/2025.05.10.653233v1.full)
- Mốc nhiễu của assay GPS mà đề tài đã tự đo (để đối chiếu, không phải của bài Larsen): SD nhiễu một
  replicate **0,3357** PSI trên 343.236 peptide của sàng peptidome, 0,2974 ở bộ quét, 0,2645 ở bộ bão hoà,
  và chính Zhang ghi trung vị |sai số| **0,239**. `[tự đo, phiên trước]` —
  [full-data-audit §7](../../topics/degron-footprint/research/full-data-audit/README.md)

### Inferences

- `[suy luận]` **Đây là điểm mạnh nhất của thư viện này làm test ngoại, và cũng là cái bẫy diễn giải lớn
  nhất.** Pearson 0,97 là tương quan **giữa các tile khác nhau trên toàn dải động**, bị kéo lên bởi phương
  sai giữa tile (stable vs strong degron cách nhau cả thang 0–1). Jaccard 0,50 của đề tài là độ trùng của
  **tập residue dương trong cùng một peptide** — mẫu số hoàn toàn khác. Không được viết "thư viện Larsen
  lặp lại tốt hơn nên nhiễu residue nhỏ hơn".
- `[suy luận]` Thước đo **dùng được** để nối hai bên là SD giữa replicate mà tác giả công bố cho **từng
  tile** (có trong `annotations/transfac_tiles.csv.gz`). Nếu lấy SD đó chia cho phương sai **sau khi trừ
  thành phần amino acid** (đúng cách đề tài đã làm cho bộ GPS) thì mới so sánh được "76% phương sai dư là
  nhiễu đo". Việc này **chưa ai làm** và phải làm trước khi tuyên bố gì về chất lượng nhãn.
- `[suy luận]` Vì bước tile là 15 residue, mỗi residue nội bộ được 2 tile phủ. Hai tile đó **không phải
  replicate kỹ thuật** (khác bối cảnh trình tự), nên **không** dùng độ nhất quán giữa chúng làm trần nhãn
  mức residue; nó lẫn cả hiệu ứng bối cảnh thật.

### Gaps

- Bài **không** báo bất kỳ thước đo lặp lại nào ở mức residue, cũng không báo tỷ lệ phương sai do nhiễu
  đo, cũng không báo phân bố SD theo dải điểm (ví dụ SD có lớn hơn ở vùng giữa thang không). Phải tự tính
  từ cột SD trong `transfac_tiles.csv.gz`.
- Không tìm thấy phát biểu nào về **drift giữa 3 replicate sinh học** hay về ảnh hưởng của việc một
  replicate C-terminal bị lỗi lên 1.620 tile đầu C.

## 3. Độ mịn của nhãn: chỉ mức tile, hay có mức residue / đột biến?

### Takeaway

**Chỉ nhãn mức tile, chỉ trình tự hoang dã.** Không có bão hoà, không có alanine scan, không có loạt xoá
hệ thống. Độ mịn thực nghiệm tốt nhất là **15 residue** (bước tile). Toàn bộ phân tích mức residue trong
bài là **dự đoán in-silico** (bản đồ ΔPAP cho HSF1; ESM-1b cho CRX), cộng với **một nhúm** đột biến/xoá
kiểm chứng riêng lẻ.

### Cited Findings

- "The screen itself uses only wild-type tile sequences. There is no saturation mutagenesis or alanine
  scan." `[bài báo]`
- Đột biến/xoá làm riêng: **ASCL1 Δ23–40**, **HSF1 Δ198–217**, và **ZNF140 tile 21** với **H323Y** rồi
  **F310D / L316D trên nền H323Y**; thêm biến thể khác ở **Fig. S9**. `[bài báo]`
- Mức residue trong bài là **dự đoán**: **ΔPAP cho toàn bộ thay thế đơn của HSF1** (file bổ sung) và
  **so sánh ESM-1b cho CRX**. `[bài báo]`
- Dữ liệu chính công bố ở mức tile và mức protein: `annotations/transfac_tiles.csv.gz` và
  `annotations/transfac_proteins.csv.gz`. `[README repo]` —
  [_2025_Larsen_degron_transcriptionfactors](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)
- `transfac_proteins.csv.gz` trong thư mục `library/` có **1.627 dòng** (1 header + **1.626 TF**) với cột
  `ID,Name,DBD,TF.assessment,Binding.mode,Motif.status,aa` — tức **kèm trình tự protein đầy đủ**.
  `[tự đo]`
- Thư mục `library/` còn có **`Lambert18_TableS1.csv` (1,2 MB)** — danh sách TF gốc lấy từ Lambert 2018.
  `[tự đo]`

### Inferences

- `[suy luận]` **Hệ quả cho mục (b) "nguồn nhãn huấn luyện thêm":** thư viện này **không** cho thêm nhãn
  nào ở mức residue và **không** cho thêm nhãn hiệu ứng đột biến. Nó chỉ có thể dùng làm (i) nhãn mức tile
  để huấn luyện/tinh chỉnh phần "degron hay không" của mô hình, hoặc (ii) nhãn yếu (weak supervision) cho
  footprint với độ mịn 15 residue.
- `[suy luận]` **Hệ quả cho mục (a) "test ngoại":** dùng được, nhưng **chỉ ở mức tile**. Một mô hình
  footprint mức residue muốn được chấm trên bộ này phải **gộp** dự đoán residue lên điểm tile (ví dụ max
  hoặc trung bình trên 30 residue) — và phép gộp đó tự nó là một lựa chọn thiết kế phải báo cáo, vì nó có
  thể che mất lỗi định vị mức residue.
- `[suy luận]` Bản đồ ΔPAP cho HSF1 trong file bổ sung là **đầu ra của PAP**, không phải nhãn thực nghiệm.
  Không được dùng làm ground truth; nếu dùng thì chỉ như "dự đoán của baseline đã công bố" để so bản đồ.

### Gaps

- Không biết **Fig. S9** có bao nhiêu biến thể và có đủ để làm một tập kiểm chứng đột biến nhỏ hay không
  (tôi không mở `SupplementalMaterial.pdf`).
- Không biết cột cụ thể nào trong `transfac_tiles.csv.gz` chứa SD/uncertainty (README không mô tả cột);
  phải tải file 2,4 MB để biết — **chưa làm**, vì bài giao hạn chế tải dữ liệu.

## 4. So sánh ngăn tế bào: 8.645 tile dùng chung với thư viện bào tương

### Takeaway

Tương quan giữa đo trong nhân và đo trong bào tương cho **cùng trình tự** rất cao (**Pearson 0,95 / 0,92**
theo thân bài), nên **phần lớn degron không phụ thuộc ngăn**. Nhưng **thân bài và chú thích Fig. 5A không
khớp nhau** về việc con số nào là Pearson, con số nào là Spearman. Tác giả **không** đưa ra tỷ lệ degron
đặc thù theo ngăn; họ chỉ chứng minh **hai mô-típ đuôi** có hành vi khác nhau giữa hai ngăn.

### Cited Findings

- Quy mô chồng nhau: **234 protein ứng với 8.645 tile dùng chung**. `[bài báo]`
- Thân bài: "Pearson correlation **0.95** and **0.92**, respectively" cho degron score và abundance score.
  `[bài báo]`
- Chú thích Fig. 5A: "absolute Pearson |r|: **0.92**, absolute Spearman |ρ|: **0.95**" cho abundance
  score. **Hai chỗ này mâu thuẫn** về nhãn thống kê. `[bài báo]`
- Khác biệt theo ngăn: tile **kết thúc bằng EE** ít dồi dào hơn **trong nhân** (**p < 10⁻⁶**); tile **kết
  thúc bằng PP** ít dồi dào hơn **trong bào tương** (**p < 10⁻³**). Kiểm định: **paired two-sided
  t-test**. `[bài báo]`
- Kiểm chứng riêng lẻ (Welch's t-test, **p < 0,001**): tile EE của **NFE2L1 (226–255)**, **CENPT
  (331–360)**, **KMT2A (466–495)**; tile PP của **FOXC1 (166–195)**, **YBX1 (166–195)**, **TP73
  (376–405)**. `[bài báo]`
- Tác giả phát biểu rằng **"most degrons"** hành xử giống nhau ở hai ngăn. `[bài báo]`
- `[tự đo]` Giao theo mã ENSG: **242 / 1.626** gene TF của Larsen cũng có trong danh sách gene của thư
  viện bào tương Voutsinos (`library/cytosol_genes.csv.gz`, 5.321 dòng). Con số của bài là **234
  protein** — chênh 8, `[suy luận]` khả năng vì 234 đếm theo protein **thực sự có tile được chấm điểm ở cả
  hai bên**, còn 242 đếm theo gene có trong thiết kế.

### Inferences

- `[suy luận]` **8.645 tile này là tập test ngoại tệ nhất và tập "nhãn lặp lại" tốt nhất cùng lúc.** Tệ
  nhất vì chúng đã nằm trong thư viện bào tương (và phần lớn trong tập train của PAP — xem mục 7). Tốt
  nhất vì đây là **cùng trình tự, cùng assay, hai lần đo độc lập, trong hai ngăn** — tức một ước lượng
  trần lặp lại **mức tile** sạch hơn cả replicate nội bộ, và nó cũng hoà lẫn hiệu ứng ngăn thật.
- `[suy luận]` Để làm test ngoại **sạch** cho đề tài thì phải **loại 8.645 tile đó** (hoặc toàn bộ 234–242
  protein) ra, còn lại ≈ **50.136 tile / ≈ 1.384 protein** làm phần không chồng. `58.781 − 8.645 = 50.136`
  `[tự đo, phép trừ]`.
- `[suy luận]` Tỷ lệ chồng nhau tính theo tile là `8.645 / 58.781 = 14,7%`, theo protein là
  `242 / 1.626 = 14,9%` `[tự đo, phép chia]` — tức **85% thư viện nhân là trình tự chưa từng đo trong
  assay bào tương**.

### Gaps

- **Không có con số "tỷ lệ degron đặc thù theo ngăn".** Bài chỉ cho bằng chứng mô-típ (EE/PP) và 6 ví dụ
  kiểm chứng. Nếu báo cáo cần con số này thì phải tự tính từ hai bảng điểm công bố.
- Mâu thuẫn 0,95 / 0,92 giữa thân bài và chú thích hình **chưa giải quyết được** từ bản HTML; cần đọc PDF
  hoặc script `analyses/` để biết con số nào là Pearson.

## 5. Đặc trưng cấu trúc: rASA, pLDDT, và đảo dấu ở CRX

### Takeaway

Dùng **AlphaFold DB v4** (pLDDT theo residue) và **DSSP** cho rASA. Trên **21.970 tile degron (điểm >
0,5)**: **rASA |r| = 0,41, |ρ| = 0,38**; **pLDDT |r| = 0,36, |ρ| = 0,36** — đúng hai con số mà đề tài đã
ghi nhận. Đảo dấu quan sát ở CRX là giữa **vùng vô định hình** (ΔPAP tốt) và **homeodomain gấp** (ESM-1b
tốt, ΔPAP đổi dấu).

### Cited Findings

- Nguồn cấu trúc: **AlphaFold DB v4**, pLDDT theo residue; **rASA tính bằng DSSP**; diện tích dung môi
  tham chiếu cực đại trích ref. 69 (Rost & Sander) — bản HTML không nêu tên trong thân bài. Các tham chiếu
  liên quan: ref 65 AlphaFold, ref 66 bản cập nhật AlphaFold DB 2024, ref 68 Kabsch & Sander (DSSP).
  `[bài báo]`
- Tương quan với degron score, trên **21.970 tile có điểm > 0,5**: **rASA |r| 0,41 · |ρ| 0,38**;
  **pLDDT |r| 0,36 · |ρ| 0,36**. `[bài báo]`
- Trong số tile degron đó: **6.992 (32%) có rASA > 0,7**; **8.817 (40%) có pLDDT < 70**. `[bài báo]`
- Zinc finger: **690 TF**, **6.136 mô-típ ZnF**; sau khi tile hoá còn **4.282 ZnF nguyên vẹn**, bằng
  **6,8% thư viện đã tile**. `[bài báo]`
- CRX: ΔPAP tương quan với hiệu ứng biến thể **ở vùng IDR: Pearson 0,54** (ESM-1b 0,31); **ở homeodomain:
  ESM-1b 0,52 còn ΔPAP −0,19**. `[bài báo]`
- Tóm tắt bài: degron ở **vùng vô định hình lộ ra** điều hoà độ dồi dào TF, còn **đột biến soma thường gặp
  trong melanoma làm lộ một degron bị chôn trong zinc finger**. `[tóm tắt]` —
  [kết quả tìm kiếm](https://www.biorxiv.org/content/10.1101/2025.05.16.654404.full.pdf)
- Bài chị em bào tương **không** cho hệ số số học cho rASA/pLDDT trong phần tôi đọc được, chỉ định tính;
  có một phân tích phụ: tương quan giữa degron score trung bình và PSI protein cho **173 protein có rASA >
  0,7**, và tương quan **tăng khi nâng ngưỡng rASA** (Fig. S9). `[bài báo]` —
  [Voutsinos bioRxiv v1](https://www.biorxiv.org/content/10.1101/2025.05.10.653233v1.full)
- Ghi chú đối chiếu nội bộ: hai con số 0,41 / 0,36 đã được ghi trong
  [architecture-check](../../topics/degron-footprint/research/architecture-check/README.md) của đề tài, và
  lần này **đọc được trực tiếp từ toàn văn**, nên có thể nâng nhãn từ `[qua tóm tắt]` lên `[đọc]`.
  `[tự đo]`

### Inferences

- `[suy luận]` **"Đảo dấu" không phải là đảo dấu của tương quan rASA–degron;** nó là đảo dấu **của chất
  lượng dự đoán**: ở vùng gấp (homeodomain) ΔPAP **tương quan nghịch** với hiệu ứng biến thể thật
  (−0,19), nghĩa là mô hình degron thuần trình tự **dự đoán sai hướng** khi peptide bị chôn. Đây là lập
  luận trực tiếp cho việc đề tài đưa đặc trưng lộ/chôn vào mô hình, nhưng cũng là cảnh báo: cùng một
  trình tự có thể mang nhãn trái dấu tuỳ bối cảnh cấu trúc.
- `[suy luận]` |r| ≈ 0,41 nghĩa là rASA giải thích ≈ **17%** phương sai degron score (r² = 0,168); tức đặc
  trưng cấu trúc là **tín hiệu phụ**, không phải tín hiệu chính. Không được trình bày như "degron được
  quyết định bởi độ lộ".
- `[suy luận]` Lưu ý **bước tile 15 phá 30% mô-típ ZnF** (6.136 → 4.282). Với một mô hình mức residue,
  điều này nói rằng ranh giới tile của thư viện này **cắt ngang** đơn vị cấu trúc — thêm một lý do để
  không coi điểm tile là nhãn residue.

### Gaps

- Bài không nêu **phiên bản DSSP** cụ thể, cũng không nêu bảng ASA cực đại dùng tên gì (chỉ trích ref 69).
  Muốn tái lập chính xác rASA phải đọc script `annotations/` trong repo.
- Repo degron của đề tài đang có **8 cấu trúc AlphaFold v6**, còn bài dùng **v4** `[bài báo]` + `[tự đo,
  đọc resources/README.md]` — **khác phiên bản**, nên pLDDT/rASA tự tính sẽ không trùng số của bài.

## 6. Dùng PAP / QCDPred / ESM-1b và các mốc dự đoán được báo cáo

### Takeaway

PAP (huấn luyện trên tile **bào tương**) đạt **Pearson 0,79 / Spearman 0,80** trên degron score của TF —
đây là mốc chuyển vùng (cytosol → nucleus) mạnh nhất bài báo đưa ra. **QCDPred không được nhắc** trong
toàn văn tôi đọc. ESM-1b chỉ xuất hiện trong phân tích CRX. Không có mô hình nào được huấn luyện mới trên
dữ liệu TF.

### Cited Findings

- **PAP** (peptide abundance predictor, huấn luyện trên tile bào tương) so với degron score của TF:
  **Pearson 0,79 · Spearman 0,80** (Fig. 5B). `[bài báo]`
- **ESM-1b**: dùng cho CRX — xem mục 5 (0,31 ở IDR, 0,52 ở homeodomain). `[bài báo]`
- **QCDPred**: **không xuất hiện** trong phần toàn văn tôi đọc được (ref 38 Johansson 2023 có trong danh
  mục tham chiếu nhưng thân bài không nói dùng thế nào). `[bài báo]`
- **ADpred** (dự đoán vùng kích hoạt phiên mã): **1.570 tile TAD** (điểm > 0,8); trong đó **1.515 (97%)**
  có degron score, **1.017 (67%)** có điểm > 0,5, **407 (27%)** có điểm > 1,0; theo PAP thì **892 (57%)**
  có điểm < 0,2. `[bài báo]`
- Tóm tắt bài: **>60% vùng kích hoạt phiên mã dự đoán chồng với degron mạnh**, và **residue acid trong
  phần còn lại làm giảm tiềm năng degron**. `[tóm tắt]`
- Cách PAP được huấn luyện (từ bài bào tương): tập holdout dựng bằng **MMseqs2 clustering trên trình tự
  protein đầy đủ**, chọn ~**10% protein (527)**, rồi **99 protein bị chuyển về train** vì tile của chúng
  giống tile train → tập test **15.815 tile (7,5%)**. Validation = 20% peptide train, early stopping.
  Hiệu năng holdout: **Pearson 0,82** (chỉ kênh nội) và **0,87** (mô hình đầy đủ). Kiểm thông lượng thấp:
  **r = 0,85** trên 164 tile. Mô hình tuyến tính "human30" **Pearson 0,80 (Spearman 0,86)**; logistic
  "human25" tương quan **−0,81**. `[bài báo]` —
  [Voutsinos bioRxiv v1](https://www.biorxiv.org/content/10.1101/2025.05.10.653233v1.full)
- `[tự đo]` Cột `set` trong `library/cytosol_genes.csv.gz` của repo Voutsinos: **4.845 `train`, 428
  `test`, 48 `copy`** — khớp với 527 − 99 = 428.
- Ngưỡng PAP công bố: abundance 0,04 / 0,22 ↔ degron score 0,93 / 0,43 ↔ **PAP score 0,14 / 0,23** qua hai
  phân tích Youden/ROC; strong degron **86% TP / 18% FP**, weak degron **89% TP / 17% FP**.
  `[README repo]`

### Inferences

- `[suy luận]` **Pearson 0,79 của PAP trên tile TF là mốc mà bất kỳ mô hình nào của đề tài phải vượt nếu
  muốn dùng thư viện này làm test ngoại mức tile** — và nó là mốc **đã được tác giả đo**, nên rất dễ bị
  hỏi khi bảo vệ. Lưu ý 0,79 **thấp hơn** 0,87 trên holdout bào tương, tức mất ≈ 0,08 Pearson khi chuyển
  ngăn; `[suy luận]` khoảng mất đó là ước lượng thô cho "chi phí chuyển vùng" của đề tài.
- `[suy luận]` Vì không có QCDPred trong bài, so sánh QCDPred ↔ thư viện nhân là **việc chưa ai làm** —
  một đóng góp nhỏ nhưng rẻ, nếu đề tài cần.
- `[suy luận]` Mốc mạnh nhất cho **nhiệm vụ mức residue** vẫn **không nằm trong bài này**. Đề tài đã tự đo
  ΔPAP `cnn2w7` precision@3 = 0,4270 so với baseline thành phần 0,4884 trên bộ quét GPS
  ([pap-baseline](../../topics/degron-footprint/research/pap-baseline/README.md), `[tự đo, phiên trước]`).
  Thư viện Larsen **không** thay thế được mốc đó.

### Gaps

- Không có bất kỳ số **mức residue** nào trong bài để làm mốc (không có precision@k, không có AUROC gọi
  residue dương). Đây là khoảng trống lớn nhất nếu muốn dùng bài này làm đối chứng cho nhiệm vụ của đề
  tài.
- Không rõ ΔPAP của HSF1 trong file bổ sung dùng cấu hình PAP nào (`cnn2w1` hay `cnn2w7`, có kênh C-term
  hay không).

## 7. Rủi ro chồng trình tự: TF của thư viện này so với peptidome GPS, và rò rỉ train của PAP

### Takeaway

**Rủi ro chồng trình tự là rất cao và bài báo hoàn toàn không nói đến nó.** Tôi tự đo: **1.583 / 1.626
(97,4%)** TF của Larsen **có mặt trong sàng peptidome GPS nội bộ của Zhang 2023**, chiếm **40.891 /
475.506 dòng (8,6%)** của bảng đó; **508 / 1.626 (31,2%)** TF có mặt trong **bộ quét đột biến (scanning
mutagenesis)** với **688 peptide hoang dã**. Về PAP: **242 TF nằm trong thư viện bào tương, trong đó 230
thuộc tập `train` của PAP và chỉ 12 thuộc `test`** — tức mốc PAP 0,79 **có rò rỉ, nhưng bị chặn ở ≈ 15%
protein**.

### Cited Findings

- `[tự đo]` Giao theo **ký hiệu gene**, danh sách TF lấy từ
  `library/transfac_proteins.csv.gz` (1.626 gene) của repo Larsen:
  | So sánh | Số gene | Tỷ lệ trên 1.626 TF | Khối lượng peptide |
  |---|---:|---:|---|
  | TF có trong **peptidome GPS I28** (Zhang 2023, `I28 Control Replicate 1.csv`, 475.506 dòng) | **1.583** | **97,4%** | **40.891 dòng (8,6%)** |
  | TF có trong **bộ quét đột biến** của Zhang 2023 (`psi-rep1.tsv`, 6.454 gene) | **508** | **31,2%** | **688 peptide WT** |
  | TF có trong **thư viện bào tương** Voutsinos (giao theo ENSG, 5.321 gene) | **242** | **14,9%** | 8.645 tile theo bài báo |
- `[tự đo]` Trong 242 TF dùng chung với thư viện bào tương: **230 thuộc `train`** của PAP, **12 thuộc
  `test`**. Nguồn cột `set`: `library/cytosol_genes.csv.gz` của
  [repo Voutsinos](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol).
- Kiểm theo tên cụ thể `[tự đo]`: **ASCL1, FOXC1, TP73, KMT2A** có trong bộ quét Zhang; **HSF1, CRX,
  ZNF140, YBX1, NFE2L1 không có** trong bộ quét. Tức các ví dụ chính của bài Larsen **phần lớn không**
  trùng với các peptide mà đề tài dùng làm nhãn footprint.
- Bài Larsen: tìm các từ khoá "GPS", "Global Protein Stability", "peptidome", "clustering" trong toàn văn
  → **không có kết quả nào trong thân bài**; "Koren" và "Zhang" **chỉ xuất hiện trong danh mục tham
  chiếu** (ref 20 Koren 2018, ref 21 Zhang 2023, ref 16 Timms & Koren, ref 37 Voutsinos 2025). "homolog"
  chỉ xuất hiện trong một tiêu đề tham chiếu. `[bài báo]`
- Bài Larsen **có** nói về dư thừa nội bộ: "63,230 tiles of which 62,992/62,808 are unique at
  nucleotide/amino acid level (excl. control peptides)" — nhưng **không** có bước clustering hay tách
  holdout theo đồng dạng, vì bài không huấn luyện mô hình. `[bài báo]`
- Ngược lại, bài bào tương **có** xử lý đồng dạng: MMseqs2 trên protein đầy đủ, chuyển 99 protein về
  train, dùng **211.444 tile có trình tự acid amin duy nhất**, và ghi nhận "small overlaps from isoforms
  and shared domains". `[bài báo]`
- Kiểm rò rỉ thực nghiệm mà đề tài đã làm trên **nhiệm vụ residue**: tách peptide theo việc protein của nó
  có trong gene train của PAP hay không → ΔPAP `cnn2w7` cho **0,4268** (656 peptide, có trong train) so
  với **0,4270** (1.747 peptide, không) → **không có lợi thế**. `[tự đo, phiên trước]` —
  [pap-baseline §B.3](../../topics/degron-footprint/research/pap-baseline/README.md)

### Inferences

- `[suy luận]` **Kết luận cứng về mục (a):** thư viện nhân **không phải test ngoại độc lập về trình tự**
  so với bộ GPS peptidome — 97,4% protein đã có mặt ở đó. Nó độc lập về **assay** (sort-seq abundance
  reporter vs GPS), về **ngăn** (nhân vs toàn bào), về **dòng tế bào**, và về **cách tile** (30-mer bước 15
  vs 23-mer của I28). Phải phát biểu đúng là "**test chuyển assay**", **không** phải "test trình tự chưa
  thấy".
- `[suy luận]` Nhưng rủi ro rò rỉ **thực tế** cho đề tài là **thấp hơn** con số 97,4% gợi ý, vì nhãn
  footprint mức residue của đề tài chỉ nằm trên **bộ quét** và **bộ bão hoà**, không phải toàn peptidome.
  Ở đó chỉ **31,2% TF** có mặt với **688 peptide WT** — và tile 30-mer bước 15 của Larsen **không trùng
  khít** peptide 23-mer của I28, nên chồng là **chồng nội dung trình tự**, không phải chồng mẫu.
- `[suy luận]` Cách xử lý đúng, rẻ: khi dùng thư viện nhân làm test, **loại theo cụm protein** (MMseqs2,
  cùng quy ước cov80 mà đề tài đã dùng) đối chiếu với tập train, chứ không loại theo tên gene. Phải báo
  hai con số: hiệu năng trên toàn bộ 58.781 tile, và trên phần **không chồng** (≈ 50.136 tile sau khi bỏ
  8.645 tile bào tương, rồi bỏ thêm cụm trùng với train của đề tài).
- `[suy luận]` Về mốc PAP 0,79: **có rò rỉ** (230/242 protein dùng chung thuộc train của PAP), nhưng vì
  chỉ 14,9% protein / 14,7% tile, con số 0,79 **không bị thổi phồng nghiêm trọng**. Nếu cần con số sạch,
  tính lại PAP trên **50.136 tile không chồng** — việc này chưa ai làm và làm được bằng dữ liệu đã có trên
  máy (trọng số PAP đã giải nén) cộng với một file 2,4 MB cần tải.

### Gaps

- Bài Larsen **không** nói gì về dư thừa/đồng dạng/clustering so với dữ liệu ngoài, nên **không có phát
  biểu của tác giả** để trích; mọi con số chồng lặp ở trên là **tôi tự đo**, và chúng giao theo **ký hiệu
  gene**, không phải theo **trình tự thực** — nên là **chặn trên** của mức chồng mẫu, không phải mức chồng
  trình tự chính xác.
- Chưa đo chồng ở **mức trình tự** (ví dụ bao nhiêu trong 58.781 tile 30-mer chứa trọn một peptide 23-mer
  của I28). Việc này cần tải `annotations/transfac_tiles.csv.gz` (2,4 MB) — nằm ngoài phạm vi "không tải
  dữ liệu lớn" của nhiệm vụ này, nhưng là bước tiếp theo rõ ràng và rẻ.

## 8. Dữ liệu, mã nguồn, và trạng thái công bố

### Takeaway

Mã nguồn công khai (MIT) trên GitHub, dữ liệu thô trên ERDA + SRA, kết quả mức tile và mức protein nằm
trong hai file `.csv.gz` nhỏ trong repo. **Chưa tìm thấy bản bình duyệt** của bài TF tính đến 10/2026;
bài chị em (bào tương) thì theo tóm tắt tìm kiếm đã ra Science Advances 02/2026 — **chưa xác minh**.

### Cited Findings

- Repo: [KULL-Centre/_2025_Larsen_degron_transcriptionfactors](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors),
  giấy phép MIT. Thư mục: `library` (dựng thư viện DNA, dựa trên Lambert18), `counts` (xử lý FASTQ),
  `score` (tính điểm), `plots`, `annotations` (ánh xạ điểm vào thư viện và chú giải bằng **PAP, ADPred và
  đặc trưng cấu trúc**), `analyses`. `[README repo]`
- Kết quả chính: **`annotations/transfac_tiles.csv.gz`** và **`annotations/transfac_proteins.csv.gz`**.
  `[README repo]`
- Dữ liệu: counts + FASTQ + dữ liệu FACS trên **ERDA, DOI
  10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943**; FASTQ cũng ở **NCBI SRA BioProject
  PRJNA1276444**; có badge **Zenodo 10.5281/zenodo.20490354** (README không nói nội dung). `[README repo]`
- Phát biểu trong bài: "All data is included in the figures and supplemental files." Bổ sung gồm
  **`SupplementalMaterial.pdf`** và **`SupplementalDataFile.xlsx`**. `[bài báo]`
- Repo PAP (dùng cho chú giải): [_2025_Voutsinos_degron_cytosol](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol);
  trọng số ở `models/pap_weights.tgz`, **từ 13/01/2026 đã chuyển sang định dạng H5 nên PAP.py chạy với mọi
  phiên bản Keras3 đã thử**; có webservice Colab qua `PapLab.ipynb`. `[README repo]`
- Trạng thái công bố: hai lần tìm kiếm (10/2026) **không thấy** bản bình duyệt của bài TF; chỉ thấy tiền
  ấn phẩm 05/2025. `[tóm tắt]` — [tìm kiếm 1](https://www.biorxiv.org/content/10.1101/2025.05.16.654404.full.pdf),
  [tìm kiếm 2](https://twistbioscience.com/resources/publication/comprehensive-degron-mapping-human-transcription-factors)
- Bài chị em (bào tương) **"was later published in Science Advances in February 2026"** `[tóm tắt]` —
  **chưa xác minh**, chỉ là câu trong kết quả tìm kiếm.
- `[tự đo]` Tôi đã tải **chỉ một file metadata nhỏ** (`library/transfac_proteins.csv.gz`, 519 KB) để đếm
  và giao danh sách gene; **không** tải `transfac_tiles.csv.gz` hay bất kỳ file ERDA/SRA nào.

### Inferences

- `[suy luận]` Vì repo có `annotations/` đã chú giải sẵn **PAP + ADPred + rASA/pLDDT**, nếu đề tài muốn
  dùng thư viện này thì **không cần tự chạy AlphaFold/DSSP** — chỉ cần tải một file 2,4 MB. Đây là lý do
  mạnh để coi đây là test ngoại **rẻ**.
- `[suy luận]` Tình trạng tiền ấn phẩm (chưa bình duyệt) là **rủi ro phải nêu rõ** khi dùng làm test ngoại
  trong luận văn: số có thể đổi giữa các bản.

### Gaps

- Không xác minh được bài chị em đã ra Science Advances (chỉ có tóm tắt tìm kiếm). Nếu báo cáo cần trích,
  phải tra lại.
- **Không nghiên cứu** Schulze & Lindorff-Larsen eLife 2026 (doi 10.7554/eLife.103721) trong phiên này —
  hết ngân sách gọi công cụ. Đây là khoảng trống đã biết trong các nguồn được gợi ý.
- Không mở `SupplementalDataFile.xlsx` nên **không biết danh sách sheet** của file bổ sung.
