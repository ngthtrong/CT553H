# Bộ nhân Larsen dùng được, nhưng không cứu nhãn residue

Đường tải bộ nhân (nuclear tile library) của Larsen 2025 **hợp lệ và sạch hơn mong đợi**: điểm mức tile không nằm sau giấy phép CC BY-NC-ND của bản tiền ấn phẩm mà nằm trong repo GitHub của nhóm tác giả dưới **giấy phép MIT**, một file `annotations/transfac_tiles.csv.gz` 5,77 MB đã chú giải sẵn PAP, ADPred, rASA và pLDDT — không cần chạm vào 120,79 GB FASTQ trên ERDA (nơi **không có giấy phép nào**), và Zenodo thì trả 403 từ mạng này nên dùng GitHub rồi trích DOI Zenodo. Nhưng nội dung của bộ dữ liệu đó bác bỏ kỳ vọng lớn nhất đặt vào nó: **1.583 / 1.626 (97,4%) TF của Larsen đã có mặt trong sàng peptidome GPS của Zhang 2023, và 230 / 242 protein dùng chung với thư viện bào tương nằm trong tập train của PAP** — nên nó **không phải test ngoại độc lập về trình tự**, mà là **test chuyển assay và chuyển ngăn tế bào ở mức tile**; nó đóng góp **đúng không nhãn mức residue nào** (chỉ trình tự hoang dã, tile 30-aa bước 15, không bão hòa, không alanine scan), và Pearson 0,97 giữa các replicate của nó **không so sánh được** với Jaccard 0,4965 mức residue của đề tài vì khác mẫu số hoàn toàn. Về bảy rủi ro ở bài 9: phép tính Spearman–Brown cho thấy việc huấn luyện/đánh giá trên **trung bình hai replicate** nâng trần Pearson khả đạt từ ≈ 0,295 lên ≈ 0,374 (**+27% tương đối**) trên bộ quét — và đó chính là điều D-025 mục 3 **đã chốt**, nên giá trị mới của phép tính là để *biện luận*, không phải để quyết; mô hình sai số của DiMSum cho một câu trích dẫn chính xác giải thích vì sao siết read 10 → 200 thất bại (**số hạng sai số cộng không phụ thuộc số đọc**, và cách chữa là *thêm replicate, không phải thêm read*); còn một tiền lệ mới — **Degformer**, repo GitHub Apache-2.0 — đã xuất đúng ma trận 28 × 20 ΔPSI từ đúng bảng S1+S4+S7 của Zhang, nhưng với **4,09% rò rỉ trình tự y hệt** trong phép chia ngẫu nhiên của chính nó và **9.443 trình tự trùng mang nhãn trái nhau**, nên nó trở thành cơ hội (baseline để đánh bại dưới split cov80) hơn là án tử. Việc chặn duy nhất vẫn là **tính lực thống kê ở n = 91**.

---

## 1. Tóm lại ngắn

1. **Đường tải sạch là GitHub (MIT), không phải phụ lục bioRxiv (CC BY-NC-ND)** — cùng số đo, giấy phép khác hẳn; chỉ còn một chỗ mơ hồ (MIT là giấy phép *software*) cần một email xác nhận. `[đọc]`
2. **Bộ nhân không phải test ngoại độc lập về trình tự**: 97,4% TF của nó đã nằm trong peptidome GPS; phải gọi đúng là **test chuyển assay / chuyển ngăn ở mức tile**. `[đo]`
3. **Nó cho đúng không nhãn mức residue nào** — chỉ tile 30-aa bước 15 trên trình tự hoang dã; độ mịn thực nghiệm tốt nhất là 15 residue. `[đọc]`
4. **Nhưng nó là chỗ duy nhất rASA/pLDDT *có phương sai*** (32% tile degron có rASA > 0,7; 40% có pLDDT < 70) — tức là nơi khả dĩ để kiểm cổng phơi lộ vừa bị hạ cấp ở C-8, ở mức tile. `[nguồn]` + `[phân tích]`
5. **Trung bình hai replicate mua được +27% trần tương đối trên bộ quét, nhưng chỉ ≈ +4,5% trên bộ bão hòa** (nhiễu 16,7%) — tức lợi ích lớn nhất của việc này đã bị thu hẹp bởi chính D-025 khi đổi nguồn nhãn chính. `[phân tích]`
6. **DiMSum và Enrich2 cho hai câu trích dẫn độc lập** biến thất bại "siết read 10 → 200" từ một kết quả âm thành một kết quả *đã được tiên đoán bởi lý thuyết* — và kê thuốc là thêm replicate. `[đọc]`
7. **Degformer là tiền lệ thứ năm, và nó đã xuất ma trận 28 × 20** từ đúng nhãn của đề tài — câu "chưa tiền lệ nào xuất ma trận" phải bị xóa khỏi mọi tài liệu. `[đọc]`
8. **LeBlanc 2026 (Cell Systems) hạ ba lập luận hỗ trợ xuống "thực hành chuẩn"** (tách abundance khỏi function trên thư viện tile, split theo cụm protein, đối chiếu trần replicate) và kết quả "thành phần quan trọng hơn vị trí" của họ là **rủi ro khoa học** trực tiếp cho một mô hình mức residue. `[đọc]`
9. **Bất kỳ phép so sánh mô hình nào ở n = 91 phải lấy đơn vị resample là cụm protein**, vì bỏ qua lồng nhau cho tỉ lệ dương giả **trên 45%** ở mức danh nghĩa 5%. `[đọc]`

---

## 2. Bộ nhân Larsen 2025: giấy phép và đường tải

### 2.1 Bốn nơi lưu, ba giấy phép khác nhau

Bài báo là **Larsen FB, Voutsinos V, Jonsson N, Johansson KE, Ethelberg FD, Lindorff-Larsen K, Hartmann-Petersen R, "Comprehensive degron mapping in human transcription factors", bioRxiv, DOI [10.1101/2025.05.16.654404](https://doi.org/10.1101/2025.05.16.654404)**, đăng 17/05/2025, **vẫn là bản v1 và chưa tìm thấy bản bình duyệt** tính đến 15/10/2026: Crossref trả `relation: {}` (không đăng ký quan hệ `is-preprint-of` với bài báo nào), API bioRxiv trả `published: "NA"`, và API khớp-công-bố của chính bioRxiv trả nguyên văn *"no articles found for published version"* ([Crossref](https://api.crossref.org/works/10.1101/2025.05.16.654404), [bioRxiv API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.05.16.654404), [bioRxiv pubs API](https://api.biorxiv.org/pubs/biorxiv/10.1101/2025.05.16.654404)) `[đọc]`. Europe PMC cũng chỉ có một bản ghi tiền ấn phẩm `PPR1022363`, `license: "cc by-nc-nd"`, `isOpenAccess: "N"` `[đọc]`. Bài **chị em** về thư viện bào tương thì **đã công bố**: Voutsinos et al., *Science Advances* 12(6), 06/02/2026, DOI [10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483), và Europe PMC ghi giấy phép **CC BY-NC** (không có ND) `[đọc]` — tức hai nửa của cùng một chương trình sàng mang điều kiện tái sử dụng **khác nhau**.

| Nơi lưu | Nội dung | Giấy phép | Trạng thái từ máy này (15/10) |
|---|---|---|---|
| **GitHub** `KULL-Centre/_2025_Larsen_degron_transcriptionfactors` | script + **điểm mức tile và mức protein**; `annotations/transfac_tiles.csv.gz` **5.771.779 B**, `transfac_proteins.csv.gz` 8.302.989 B, `score/degrons.csv.gz` 4.563.816 B, `transfac_struc.csv.gz` 10.155.511 B, `transfac_proteins_pap.txt.gz` 15.530.333 B | **MIT** (file `LICENSE` 1.127 B ở gốc repo, GitHub API báo `spdx_id: MIT`) | **200**, đọc được bằng HTTP range request |
| **Zenodo** DOI [10.5281/zenodo.20490355](https://doi.org/10.5281/zenodo.20490355) | ảnh lưu trữ của repo, một file ZIP **87,1 MB**, `md5:ab2a5546e7b3913baea4660bc3f007d5`, bản `v1.0`, phát hành 01/06/2026 | **MIT** (`rightsList` của DataCite ghi `MIT License`, SPDX `mit`) | **403** — cả trang và REST API; siêu dữ liệu lấy qua [DataCite](https://api.datacite.org/dois/10.5281/zenodo.20490355) |
| **ERDA** (ĐH Copenhagen) DOI 10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943 | FASTQ + FACS, **6 file, 120.785.019.615 B = 120,79 GB** (DataCite ghi `sizes: ["113 GB"]`) | **KHÔNG CÓ** — `rightsList: []`, `descriptions: []`; trang archive không có dòng giấy phép nào | **200** |
| **NCBI SRA** BioProject [PRJNA1276444](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1276444) | **136** bản ghi experiment, "Screen for degrons in human transcription factors", đăng ký 13/06/2025 | mặc định NCBI | **200** |
| **Phụ lục bioRxiv** `media-1.pdf` (SupplementalMaterial.pdf) và `media-2.xlsx` (SupplementalDataFile.xlsx) | theo bài, đây là **bản phát hành dữ liệu chính thức** | **CC BY-NC-ND 4.0** | **200**, nhưng **không có `content-length`** nên không biết kích thước |

Ba điều đáng ghi riêng. Thứ nhất, **không có deposit nào khác**: `elink` từ BioProject 1276444 sang GEO trả về linkset rỗng, tìm GEO DataSets với `degron AND "transcription factors" AND Hartmann-Petersen[Author]` trả `count: "0"`, và figshare trả tập rỗng ([NCBI eLink](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=bioproject&db=gds&id=1276444&retmode=json)) `[đọc]` — **đừng đi tìm mã GSE nữa**, đây là sàng amplicon/FACS nên SRA + lưu trữ cơ quan là khuôn thường gặp `[phân tích]`. Thứ hai, câu "Data and code availability" của bài **cực ngắn**: *"All data is included in the figures and supplemental files."* cộng một trỏ về GitHub; **chính README của GitHub, không phải bản thảo, mới là nơi nêu ERDA, SRA và Zenodo** `[đọc]`. Thứ ba, giấy phép **ERDA rỗng là deposit rủi ro nhất** — "public archive" cộng một DOI DataCite thể hiện ý định mở, nhưng *truy cập được* ≠ *được cấp phép*; may là đề tài **không cần nó** `[phân tích]`.

### 2.2 Chỗ mơ hồ còn lại, và email cần gửi

MIT cho phép *"use, copy, modify, merge, publish, distribute, sublicense, and/or sell"* với điều kiện duy nhất là giữ kèm thông báo bản quyền và thông báo cho phép ([LICENSE](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/LICENSE)) `[đọc]`. Vấn đề: **MIT là giấy phép phần mềm**, và deposit Zenodo đăng ký `resourceTypeGeneral: "Software"`. Một người đọc nghiêm khắc có thể lập luận rằng MIT được trao cho các script, còn các file `.csv.gz` chỉ đi kèm. Lập luận phản lại cũng mạnh: file `LICENSE` nằm ở gốc repo **không có ngoại lệ**, bộ phát hiện giấy phép của GitHub áp cho toàn repo, và chính README gọi hai file CSV là *"the main resulting data"* `[phân tích]`. Trên cân, MIT đọc ra là phủ toàn bộ repo — nhưng **một câu xác nhận bằng văn bản của tác giả xóa sạch chỗ mơ hồ này**, và nó rẻ.

**Email nên gửi** `[đề xuất]` — tới `rhpetersen@bio.ku.dk` (Rasmus Hartmann-Petersen, tác giả liên hệ được API bioRxiv chỉ định), cc `lindorff@bio.ku.dk`, `vasileios.voutsinos@bio.ku.dk` và `kristoffer.johansson@bio.ku.dk` (người tạo archive ERDA) `[đọc]`, hỏi đúng bốn việc:

1. Xác nhận **MIT trong repo có ý định phủ cả các file dữ liệu đầu ra** (`annotations/*.csv.gz`, `score/degrons.csv.gz`), không chỉ script.
2. Xin phép (nếu cần) **tái hiện một số panel hình** trong một luận văn tiếng Việt.
3. Hỏi có **bản bình duyệt đang in** và ở tạp chí nào, để luận văn trích bản chính thức.
4. Hỏi **archive ERDA có giấy phép dự kiến** nào không.

### 2.3 An toàn và rủi ro, xét trên thực tế repo đang **private**

Phân tầng dưới đây là `[phân tích]`, **không phải tư vấn pháp lý**. Hai sự thật pháp lý khung: Creative Commons tự phát biểu rằng giấy phép CC *"operative only when applied to material in which a copyright exists"* và rằng với cơ sở dữ liệu thì **dữ liệu thuần sự kiện thường không được bảo hộ**; và điều khoản ND **cấm *chia sẻ* bản phái sinh, không cấm *tạo ra* nó** ([CC FAQ](https://creativecommons.org/faq/)) `[đọc]`.

- **An toàn rõ, không cần xin phép:** đọc mọi deposit; **tải** `transfac_tiles.csv.gz` và các file CSV khác từ GitHub hoặc ZIP Zenodo (MIT cho phép sao chép tường minh); huấn luyện/khớp mô hình trên điểm; báo cáo chỉ số tổng hợp (Pearson/Spearman/AUROC, ma trận nhầm lẫn); trích DOI bài báo và DOI Zenodo; dẫn một số điểm lẻ làm ví dụ kèm ghi nguồn — đây là sự kiện, và trích dẫn ngắn phục vụ nghiên cứu còn nằm trong giới hạn hợp lý của luật Việt Nam `[phân tích]`.
- **An toàn kèm một điều kiện:** **phát hành lại bảng đã xử lý trong repo công khai của luận văn** — được, *nếu* nguồn là repo MIT và *nếu* thông báo MIT đi kèm (ví dụ một file `data/raw/SOURCE.md` hoặc `LICENSE-THIRD-PARTY` ghi lại thông báo, tên repo thượng nguồn, commit/tag và DOI Zenodo). Trên thực tế, quy ước của repo này đã chặn `data/` khỏi git nên câu hỏi **không phát sinh** chừng nào quy ước còn giữ `[phân tích]`.
- **Rủi ro, nên tránh:** phát hành lại **chính file `SupplementalDataFile.xlsx` của bioRxiv** (nó mang CC BY-NC-ND; ngay cả chia sẻ nguyên vẹn cũng chỉ được phi thương mại kèm ghi công, và mọi định dạng lại đều có thể bị coi là "đã sửa"); **sao panel hình** rồi cắt, đổi màu, đổi nhãn hay dịch chú thích sang tiếng Việt — đó là hành vi tạo bản phái sinh mà ND cấm chia sẻ, nên **cách an toàn là tự vẽ lại từ dữ liệu**; và **dùng archive ERDA** cho bất cứ việc gì ngoài đọc, vì nó không có giấy phép `[phân tích]`.
- **Riêng trạng thái private của repo** (D-004) làm nhẹ mọi câu hỏi "chia sẻ" ở trên, vì ND và NC đều điều chỉnh hành vi **phân phối**. Nhưng điều đó cũng có nghĩa: **nếu repo đổi sang public hay được chia sẻ cho GVHD**, đúng những mục ở tầng "rủi ro" là thứ phải gỡ trước, cùng với các PDF bài báo mà D-004 đã liệt kê `[phân tích]`.
- **Chuyển vùng pháp lý đáng lưu ý:** quyền *sui generis* về cơ sở dữ liệu của EU (Directive 96/9/EC) có thể tồn tại trên bảng do ĐH Copenhagen biên soạn, nhưng quyền đó **không được công nhận ở Việt Nam hay Mỹ** và bảo hộ theo nguyên tắc có đi có lại (Art. 11) — nên một tác giả luận văn ở Việt Nam trích xuất bảng tại Việt Nam ở vị thế tốt hơn hẳn người ở EU; vị thế đó đổi nếu bảng phái sinh về sau được đăng/host ở EU `[phân tích]`.

---

## 3. Bộ nhân Larsen 2025: dữ liệu thực chất chứa gì

### 3.1 Đây không phải GPS, và thang điểm chạy ngược

Đây là **sort-seq trên hệ báo cáo độ dồi dào**, không phải GPS. Mỗi tile được gắn vào **đầu C của GFP**, GFP có **NLS ở đầu N**, **mCherry biểu hiện cùng qua IRES** làm chuẩn hoá, tích hợp **đơn bản sao bằng Bxb1 vào landing pad trong HEK293T**; tế bào được phân vào **4 gate FACS, mỗi gate 25% dân số** ([toàn văn bioRxiv v1](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full)) `[đọc]`. Thư viện: tile **30 residue, bước 15 residue** (tile đầu C dài 29), ba thư viện con không chồng nhau — **odds 31.080 tile, evens 30.292 tile, C-terminal 1.620 tile** — oligo Twist, lắp Gibson, 5 lần biến nạp mỗi thư viện, độ phủ ≥ 100 lần `[nguồn]`.

Điểm thô vẫn gọi là **PSI** và tính theo tần suất tile trong 4 gate, nhưng sau đó được **chuẩn hoá lại về thang 0–1 với dấu đảo**: *"normalizing each replicate such that the median of the stable peak has degron score zero"*, đỉnh bất ổn nhất nhận 1, và *"Degron scores close to zero indicate low degron potency, while scores close to one indicate high degron potency"* `[đọc]`. Một điểm thứ hai, **abundance score**, là biến đổi **phi tuyến đơn điệu** của degron score và chạy ngược chiều nó `[đọc]`. Hệ quả thực hành là cụ thể: bảng PSI của bộ GPS Zhang 2023 mà đề tài đang dùng có **6 bin** (`nb1…nb6` trong `data/processed/psi-rep1.tsv`) với thang xấp xỉ 1–6 và **giá trị thấp = bất ổn** `[đo]`; muốn ghép hai nguồn nhãn thì phải **chuẩn hoá theo phân vị hoặc theo neo đối chứng, không map tuyến tính** `[phân tích]`. Ngưỡng tham chiếu của bài chị em cho thấy phép đổi thang là chuyện có thật và đã được tác giả làm bằng tay: abundance 0,04 / 0,22 ↔ degron score **0,93 / 0,43** ↔ PAP score 0,14 / 0,23 ([README repo Voutsinos](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol)) `[đọc]`.

### 3.2 Pearson 0,97 là thật, và là cái bẫy diễn giải lớn nhất

| Phép đo lặp lại | Giá trị | Mức |
|---|---:|---|
| Pearson trung bình giữa mọi cặp replicate (khoảng 0,91–0,99) | **0,97** | **tile** |
| Số replicate | 3 sinh học × 2 FACS = **6 mỗi thư viện con** (một replicate C-terminal bị lỗi) | — |
| Lọc read | **≥ 100 read trên 4 gate**, chỉ read khớp chính xác thư viện | — |
| Sai số công bố | **SD giữa các replicate**, yêu cầu ≥ 2 phép đo mỗi tile | **từng tile** |
| Độ phủ mỗi replicate | 96–98% thành viên thư viện | — |
| Kiểm chứng thông lượng thấp | Pearson **−0,93** trên 82 tile (dấu âm vì hai thang ngược chiều) | tile |

Mọi con số trên là `[nguồn]`, đọc trực tiếp từ toàn văn. **Cái bẫy**: Pearson 0,97 là tương quan **giữa các tile khác nhau trên toàn dải động**, bị kéo lên bởi phương sai giữa tile (tile ổn định và tile degron mạnh cách nhau cả thang 0–1). Jaccard 0,4965 của đề tài là độ trùng của **tập residue dương bên trong cùng một peptide** — mẫu số khác hoàn toàn. **Không được viết "thư viện Larsen lặp lại tốt hơn nên nhiễu mức residue nhỏ hơn"** `[phân tích]`. Bài báo **không** báo bất kỳ thước đo lặp lại nào ở mức residue, cũng không báo tỉ lệ phương sai do nhiễu đo, vì thí nghiệm không có nhãn mức residue `[đọc]`.

Thứ **dùng được** để nối hai bên là cột **SD giữa replicate cho từng tile** trong `transfac_tiles.csv.gz` (header đã xác minh: `name,gene,first_resi,last_resi,copyof_dna,copyof_aa,lib,aa,dna,zf,n,degron_score,degron_std,abundance_score,abundance_std,pap_ct,pap,locnes,locnes_score,tile_rasa_median,tile_plddt_median`) `[đọc]`. Nếu lấy `degron_std` chia cho phương sai **sau khi trừ thành phần acid amin** — đúng cách đề tài đã làm cho bộ GPS — thì mới so sánh được phát biểu "75,9% phương sai dư là nhiễu đo". **Chưa tìm thấy ai công bố phép tính đó cho bộ nhân**; nó phải được làm trước khi tuyên bố gì về chất lượng nhãn của bộ này `[phân tích]`.

Một cạm bẫy thứ hai, nhỏ hơn nhưng dễ mắc: vì bước tile là 15 residue, **mỗi residue nội bộ được 2 tile phủ**. Hai tile đó **không phải replicate kỹ thuật** (khác bối cảnh trình tự), nên **không** được dùng độ nhất quán giữa chúng làm trần nhãn mức residue — nó lẫn cả hiệu ứng bối cảnh thật `[phân tích]`.

### 3.3 Chỉ mức tile, chỉ trình tự hoang dã

*"The screen itself uses only wild-type tile sequences. There is no saturation mutagenesis or alanine scan."* `[đọc]`. Toàn bộ phân tích mức residue trong bài là **dự đoán in-silico**: bản đồ ΔPAP cho mọi thay thế đơn của **HSF1** (trong file bổ sung, giới hạn residue 412–420), và so sánh ESM-1b cho **CRX**; cộng một **nhúm** đột biến/xoá kiểm chứng riêng lẻ — **ASCL1 Δ23–40**, **HSF1 Δ198–217**, và **ZNF140 tile 21** với **H323Y** rồi **F310D / L316D** trên nền H323Y, thêm vài biến thể ở **Fig. S9** `[đọc]`. Profile theo residue trong Fig. 3 và 6C là **trung bình trượt cửa sổ 5 trên điểm tile**, tức một phép làm trơn đầu ra mức peptide, không phải mô hình mức residue `[đọc]`. Bản đồ ΔPAP của HSF1 là **đầu ra của PAP**, không phải nhãn thực nghiệm — không được dùng làm ground truth `[phân tích]`.

Hệ quả cho hai mục đích mà đề tài có thể nhắm: **(a) nguồn nhãn huấn luyện thêm** → bộ này cho **0 nhãn mức residue và 0 nhãn hiệu ứng đột biến**; nhiều nhất nó là nhãn mức tile cho phần "degron hay không", hoặc nhãn yếu (weak supervision) cho footprint với **độ mịn 15 residue**. **(b) test ngoại** → dùng được, nhưng **chỉ ở mức tile**, và một mô hình mức residue muốn được chấm trên nó phải **gộp** dự đoán residue lên điểm tile (max hay trung bình trên 30 residue), và chính phép gộp đó là một lựa chọn thiết kế phải báo cáo vì nó **có thể che mất lỗi định vị** `[phân tích]`.

### 3.4 Chồng ngăn tế bào, và những chỗ bài báo tự mâu thuẫn

Giao với thư viện bào tương là **234 protein ứng với 8.645 tile dùng chung**, và tương quan giữa đo trong nhân với đo trong bào tương cho cùng trình tự rất cao — thân bài ghi **Pearson 0,95 và 0,92** cho degron score và abundance score `[nguồn]`. Nhưng **chú thích Fig. 5A ghi ngược nhãn thống kê**: *"absolute Pearson |r|: 0,92, absolute Spearman |ρ|: 0,95"* cho abundance score — **hai chỗ trong cùng bài mâu thuẫn** về con số nào là Pearson `[đọc]`. Khác biệt theo ngăn mà tác giả chứng minh được chỉ là **hai mô-típ đuôi**: tile kết thúc bằng **EE** ít dồi dào hơn **trong nhân** (p < 10⁻⁶), tile kết thúc bằng **PP** ít dồi dào hơn **trong bào tương** (p < 10⁻³), paired two-sided t-test, kèm 6 ví dụ Welch p < 0,001 (NFE2L1 226–255, CENPT 331–360, KMT2A 466–495; FOXC1 166–195, YBX1 166–195, TP73 376–405) `[nguồn]`. Tác giả phát biểu **"most degrons"** hành xử giống nhau ở hai ngăn, và **không** đưa ra tỉ lệ degron đặc thù theo ngăn `[đọc]`.

Danh sách mâu thuẫn nội tại về số tile thì dài hơn, và **nó nằm trong nguồn, không phải lỗi chép**:

| Con số tile trong bài | Chỗ xuất hiện |
|---|---|
| **62.992** | thân bài: *"tiled library encompassing 62,992 tiles"*; cũng là số duy nhất ở mức nucleotide |
| **63.230** | Methods: tổng số tile thiết kế |
| 62.808 | Methods: duy nhất ở mức acid amin |
| **63.011** | Methods: *"We attained data for 58,781 tiles out of the initial 63,011 tiles"* |
| **58.781** | số tile có điểm; được mô tả là **93% của TF proteome** |
| **58.992** | Methods: *"58,781 scores which are mapped to 58,992 tiles"* |

`[đọc]` cho cả bảng. **Cách xử lý đúng** là nạp `annotations/transfac_tiles.csv.gz`, **đếm số dòng có `degron_score` không NA**, trích file đó, và ghi mâu thuẫn của bài vào một chú thích — chứ **không** dẫn "58.781" như một con số không mơ hồ `[đề xuất]`. Phép chia cũng khớp với phát biểu của tác giả: 58.781 / 62.992 ≈ **93,3%** `[đo]`.

### 3.5 Cấu trúc: rASA, pLDDT, và đảo dấu ở CRX

Nguồn cấu trúc là **AlphaFold DB v4** (pLDDT theo residue) và **DSSP** cho rASA, diện tích dung môi tham chiếu trích ref 69 `[đọc]`. Trên **21.970 tile có degron score > 0,5** (= 37,4% của 58.781 `[đo]`): **rASA |r| 0,41 · |ρ| 0,38** và **pLDDT |r| 0,36 · |ρ| 0,36** `[nguồn]`. Trong số tile degron đó, **6.992 (32%) có rASA > 0,7** và **8.817 (40%) có pLDDT < 70** `[nguồn]`. Zinc finger: **690 TF, 6.136 mô-típ ZnF**, sau khi tile hoá chỉ còn **4.282 ZnF nguyên vẹn** = 6,8% thư viện — tức **bước tile 15 phá khoảng 30% mô-típ ZnF**, thêm một lý do nữa để không coi điểm tile là nhãn residue `[nguồn]` + `[phân tích]`.

|r| ≈ 0,41 nghĩa là rASA giải thích ≈ **17% phương sai** degron score (r² = 0,168) — **tín hiệu phụ, không phải tín hiệu chính**; không được trình bày như "degron được quyết định bởi độ lộ" `[phân tích]`. "Đảo dấu" ở CRX **không phải** đảo dấu của tương quan rASA–degron mà là đảo dấu **của chất lượng dự đoán**: ở vùng vô định hình, ΔPAP tương quan **0,54** với hiệu ứng biến thể (ESM-1b 0,31); ở homeodomain gấp thì **ESM-1b 0,52 còn ΔPAP −0,19** `[nguồn]`. Đây vừa là lập luận cho việc đưa đặc trưng lộ/chôn vào mô hình, vừa là cảnh báo rằng **cùng một trình tự có thể mang nhãn trái dấu tuỳ bối cảnh cấu trúc** `[phân tích]`.

Mốc mô hình mạnh nhất bài đưa ra là **PAP (huấn luyện trên tile bào tương) đạt Pearson 0,79 · Spearman 0,80** trên degron score của TF (Fig. 5B) `[nguồn]`. **QCDPred không xuất hiện** trong phần toàn văn đã đọc `[đọc]`. ADPred: **1.570 tile TAD** (điểm > 0,8), trong đó 1.515 (97%) có degron score, 1.017 (67%) có điểm > 0,5, 407 (27%) có điểm > 1,0 `[nguồn]`. Hai lưu ý phiên bản: đề tài đang có **8 cấu trúc AlphaFold v6** còn bài dùng **v4**, nên pLDDT/rASA tự tính **sẽ không trùng số của bài** `[đo]` + `[phân tích]`; và bài **không nêu phiên bản DSSP** nên muốn tái lập chính xác rASA phải đọc script trong `annotations/` `[đọc]`.

---

## 4. Bộ nhân giúp được gì, và không giúp được gì

### 4.1 Con số quyết định: 97,4%

Bài Larsen **hoàn toàn không nói gì về chồng lặp trình tự với dữ liệu ngoài** — tìm "GPS", "Global Protein Stability", "peptidome", "clustering" trong toàn văn không ra kết quả nào trong thân bài; "Koren" và "Zhang" chỉ xuất hiện trong danh mục tham chiếu `[đọc]`. Nên mọi con số dưới đây là **tự đo**, giao theo **ký hiệu gene**, tức là **chặn trên** của mức chồng mẫu, không phải mức chồng trình tự chính xác `[đo]`:

| So sánh | Số gene | Tỉ lệ trên 1.626 TF | Khối lượng peptide |
|---|---:|---:|---|
| TF có trong **peptidome GPS I28** (Zhang 2023, `I28 Control Replicate 1.csv`, 475.506 dòng) | **1.583** | **97,4%** | **40.891 dòng (8,6%)** |
| TF có trong **bộ quét đột biến** của Zhang 2023 (`psi-rep1.tsv`, 6.454 gene) | **508** | **31,2%** | **688 peptide WT** |
| TF có trong **thư viện bào tương** Voutsinos (giao theo ENSG, 5.321 gene) | **242** | **14,9%** | 8.645 tile theo bài báo |
| Trong 242 TF dùng chung: thuộc tập **`train` của PAP** | **230** | — | cột `set` trong `library/cytosol_genes.csv.gz` |
| Trong 242 TF dùng chung: thuộc tập **`test` của PAP** | **12** | — | — |

**Kết luận cứng**: bộ nhân **không phải test ngoại độc lập về trình tự** so với bộ GPS peptidome. Nó độc lập về **assay** (sort-seq abundance reporter vs GPS), về **ngăn tế bào** (nhân vs toàn bào), về **dòng tế bào**, và về **cách tile** (30-mer bước 15 vs 23-mer của I28). Phải phát biểu đúng là **"test chuyển assay / chuyển ngăn"**, không phải "test trình tự chưa thấy" `[phân tích]`.

Nhưng rủi ro rò rỉ **thực tế** cho đề tài **thấp hơn** con số 97,4% gợi ý, vì nhãn footprint mức residue của đề tài chỉ nằm trên **bộ quét** và **bộ bão hoà**, không phải toàn peptidome: ở đó chỉ **31,2% TF** có mặt với **688 peptide WT**, và tile 30-mer bước 15 **không trùng khít** peptide 23-mer của I28 — nên đây là **chồng nội dung trình tự**, không phải chồng mẫu `[phân tích]`. Kiểm theo tên cụ thể: **ASCL1, FOXC1, TP73, KMT2A** có trong bộ quét Zhang; **HSF1, CRX, ZNF140, YBX1, NFE2L1 không có** — tức phần lớn ví dụ chính của bài Larsen **không** trùng với peptide đề tài dùng làm nhãn footprint `[đo]`.

Về mốc PAP 0,79: **có rò rỉ** (230/242 protein dùng chung thuộc train của PAP), nhưng vì chỉ 14,9% protein / 14,7% tile nên **0,79 không bị thổi phồng nghiêm trọng** `[phân tích]`. Một chứng cứ thực nghiệm độc lập củng cố điều này: trên **nhiệm vụ residue**, tách peptide theo việc protein của nó có trong gene train của PAP hay không cho ΔPAP `cnn2w7` = **0,4268** (656 peptide, có trong train) so với **0,4270** (1.747 peptide, không) — **không có lợi thế** `[đo, phiên trước]` ([pap-baseline §B.3](../pap-baseline/README.md)).

### 4.2 Nó đóng góp **0** nhãn mức residue — và đó là điều quan trọng nhất

Rủi ro 1 ở bài 9 nêu "bổ sung bộ nhân của Larsen 2025" như một đường thoát nếu nhãn mức residue sụp. **Đường đó không tồn tại.** Bộ nhân không có nhãn mức residue, không có nhãn đột biến, và độ mịn tốt nhất của nó (15 residue) thô hơn cả mục tiêu của đề tài (1 residue trong cửa sổ 28) một bậc. Nó **không** nâng n của bậc 2 hay bậc 3, **không** cải thiện Jaccard 0,4965, và **không** thay thế mốc ΔPAP mức residue — vì bài **không có bất kỳ số mức residue nào** (không precision@k, không AUROC gọi residue dương) `[đọc]` + `[phân tích]`. Câu ở bài 9 nên được sửa cho đúng.

### 4.3 Nó **là** một test chuyển ngăn mức tile rẻ, và một chỗ để kiểm cổng phơi lộ

Ba giá trị thật, xếp theo độ chắc:

**Một — test chuyển ngăn mức tile với chú giải đã tính sẵn.** Repo có `annotations/` đã chú giải **PAP + ADPred + rASA/pLDDT**, nên đề tài **không cần chạy AlphaFold hay DSSP**: chỉ cần tải một file 5,77 MB. Mốc phải vượt là **PAP Pearson 0,79**, một con số **do chính tác giả đo** nên rất dễ bị hỏi khi bảo vệ; và khoảng mất **0,87 → 0,79** khi chuyển từ holdout bào tương sang tile TF là một **ước lượng thô cho "chi phí chuyển ngăn"** mà đề tài có thể trích `[nguồn]` + `[phân tích]`. Để làm test **sạch** thì phải loại **8.645 tile** bào tương (hoặc cả 234–242 protein), còn **≈ 50.136 tile / ≈ 1.384 protein** `[đo, phép trừ]`, rồi loại thêm theo **cụm protein MMseqs2 cov80** đối chiếu tập train của đề tài — **không loại theo tên gene** — và phải **báo hai con số**: trên toàn bộ tile có điểm, và trên phần không chồng `[đề xuất]`.

**Hai — chỗ duy nhất rASA/pLDDT có phương sai.** Đây là phát hiện có giá trị nhất cho rủi ro 4c. Lý do cổng phơi lộ không huấn luyện được trên nhiệm vụ chính là nhãn chính gồm peptide 28-mer tách rời gắn đầu C của GFP, nên **mọi residue phơi lộ như nhau** và rASA **không có phương sai** (C-8). Bộ nhân thì **có**: 32% tile degron có rASA > 0,7 và 40% có pLDDT < 70, và tác giả đã đo tương quan 0,41 / 0,36 `[nguồn]`. Đó biến bộ nhân thành **nơi kiểm được tham số cổng ở mức tile** — không cứu được cổng ở mức residue, nhưng đủ để biến "cơ chế chuyển giao" từ một lời khẳng định thành một con số `[phân tích]` `[đề xuất]`.

**Ba — hai phép so sánh chưa tìm thấy ai làm, và đều rẻ.** (i) **QCDPred ↔ thư viện nhân**: QCDPred không xuất hiện trong bài Larsen, nên so sánh này còn trống; (ii) **PAP tính lại trên 50.136 tile không chồng**, để có một con số 0,79 "sạch". Cả hai làm được bằng dữ liệu đã có trên máy (trọng số PAP đã giải nén, xem resources) cộng một file 5,77 MB cần tải `[phân tích]`.

Cuối cùng, một rủi ro phải nêu rõ nếu dùng bộ này làm test ngoại trong luận văn: **nó vẫn là tiền ấn phẩm chưa bình duyệt sau 17 tháng**, nên số có thể đổi giữa các bản; phải trích là preprint và **không** giả định đã được tạp chí kiểm `[phân tích]`.

---

## 5. Rủi ro 1–7: phân tích và cách xử lý

### 5.1 Rủi ro 1 — lực thống kê và nhãn mức residue chỉ lặp ~một nửa

**Điều mới biết mà bài 9 chưa nói.** Thứ nhất, có một **phép tính lượng hoá được** cho câu "nhãn chỉ lặp một nửa". Viết `y = t + e` với độ tin cậy `ρ = Var(t)/Var(y)`, một mô hình dự đoán *hoàn hảo* `t` tương quan với **một** replicate quan sát ở mức `sqrt(ρ)`, và Spearman–Brown cho biết độ tin cậy của **trung bình k replicate** là `ρ_k = kρ₁/(1+(k−1)ρ₁)`. Áp vào các số đã audit của **bộ quét** `[phân tích]` (phép tính của tôi, đầu vào phải trích file audit của repo):

| Lượng | Giá trị |
|---|---:|
| Tỉ lệ nhiễu trong phương sai dư (bộ quét) | 0,759 |
| Độ tin cậy **một** replicate `ρ₁` | **0,241** |
| Trần Pearson của một mô hình hoàn hảo so với **một** replicate | 0,491 |
| Độ tin cậy **trung bình 2 replicate** `ρ₂` | **0,388** |
| Trần Pearson của một mô hình hoàn hảo so với **trung bình 2 replicate** | 0,623 |
| Trần của **phần ngữ cảnh học được** (R² = 0,087) so với một replicate | **0,295** |
| Cùng trần đó, so với trung bình 2 replicate | **0,374** (R² ≈ 0,140) |
| **Lợi ích tương đối của việc dùng trung bình 2 replicate** | **+27%** (hệ số `sqrt(ρ₂/ρ₁)` = 1,2695) |

**Nhưng phải nói ngay hai điều.** (a) Phép tính này cho **bộ quét**, mà D-025 đã chuyển nguồn nhãn chính sang **bộ bão hòa**, nơi nhiễu chỉ **16,7%** → `ρ₁ ≈ 0,833`, `ρ₂ ≈ 0,909`, và lợi ích của việc lấy trung bình chỉ còn **≈ +4,5% tương đối** `[phân tích]`. (b) **Việc "chuyển sang trung bình hai replicate" đã được chốt rồi** — D-025 mục 3: *"Nhãn là trung bình hai replicate; mọi bảng kết quả báo kèm trần nhãn."* Nên giá trị mới của phép tính **không phải** là một quyết định cần ra, mà là **con số để biện luận** trong luận văn cho một quyết định đã có `[phân tích]`. Ghi chú này cũng là một chỗ cần sửa trong ghi chép nghiên cứu, vì note 03 trình bày nó như "việc rẻ nhất chưa làm".

Thứ hai, có **tiền lệ công bố** cho cách trình bày trần nhãn: LeBlanc et al. 2026 ghi thẳng *"The abundance data was much noisier than the GFP data (**replicate Pearson correlation of 0.568**), and our best performing NN **approached this ceiling (Pearson correlation of 0.555**, p < 10⁻³⁰⁰)"* ([PMC13596073](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596073/)) `[đọc]`; RECOVER báo *"0.47 Spearman … while the highest achievable Spearman correlation is estimated to be 0.64"* ([arXiv:2202.04202](https://arxiv.org/pdf/2202.04202)) `[đọc]`; và ProteinGym nói thẳng *"one cannot expect perfect correlation between experiment and model"* ([ProteinGym](https://www.biorxiv.org/content/10.1101/2023.12.07.570727v1.full)) `[đọc]`. Năm 2026, **báo r của mô hình mà không báo r giữa replicate sẽ bị đọc là một lỗi trình bày** `[phân tích]`.

Thứ ba, **thước đo mềm có tiền lệ** để thay cho "trùng khít tập vị trí" (16,0%): benchmark túi gắn protein–ligand coi hai túi là **cùng một túi** khi *"overlap is at least 3/4 (≥ 75%) residues"*, tức **Jaccard ≥ 0,75** ([J Cheminform 2024](https://link.springer.com/article/10.1186/s13321-024-00923-z)); **Binding-site Distance Test** cho **điểm thưởng từng phần theo khoảng cách** — *"residues predicted to be close to the observed binding site residues receive higher scores than more distant residues"* ([FunFOLDQA, PMC3364224](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3364224/)); **Hit-Rate@TopK** đang được dùng ([arXiv:2605.24045](https://arxiv.org/pdf/2605.24045)); và **Top-K recall ở K = 10% cao nhất** cùng **NDCG** là chỉ số chính thức của ProteinGym `[đọc]`. QCDPred — tiền lệ gần nhất, cùng họ dữ liệu — báo **Spearman mức peptide ρ = −0,74 / −0,78**, chưa bao giờ báo khớp-chính-xác mức residue, và nó **trung bình điểm qua bảy tâm acid amin trong mỗi peptide 23-aa** ([degronome paper](https://www.biorxiv.org/content/10.1101/2022.04.06.487275v2.full)) `[đọc]`.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí, làm trước tiên — tính lực ở n = 91 và *đếm số cụm protein*.** Đây là việc chặn duy nhất. Lưu ý quan trọng chưa có trong bài 9: đơn vị resample phải là **cụm protein** (khớp đơn vị split), nên con số cần báo không phải 91 mà là **số cụm**; nếu số cụm < ~20 thì phải nói rõ và coi mọi p-value là **chỉ báo**, trích cảnh báo "ít cụm → suy luận mức cụm không đáng tin" ([arXiv:2609.06330](https://arxiv.org/pdf/2609.06330)) `[đề xuất]`.
2. **Miễn phí — phát biểu trước mức chênh phát hiện được.** Với SD ghép cặp đo thật 0,2416 trên bộ quét, SE ở n = 91 là ≈ 0,0253 và **mức chênh tối thiểu phát hiện được ở lực 80% ≈ 2,8 × SE ≈ 0,071** `[phân tích]` (minh hoạ: SD của AUROC mức ô chưa đo, phải đo lại). So với dư địa đã đo **0,1827** (AUROC mức ô, ΔPAP 0,7692 → trần 0,9519) thì phép so với ΔPAP **phát hiện được**; nhưng **mọi khác biệt ablation cỡ 0,02–0,05 thì không**. Luận văn nên **cam kết trước** rằng phần lớn ablation ở n ≈ 91–322 sẽ **không phân biệt được về mặt thống kê**, thay vì về sau công bố một "người thắng" `[đề xuất]`.
3. **Một ngày — bootstrap phân cấp mức cụm.** Resample cụm có hoàn lại, rồi peptide trong cụm, rồi (nếu chỉ số ở mức residue) residue trong peptide, B = 10.000, theo Saravanan, Berman & Sober, những người báo rằng với dữ liệu lồng nhau *"traditional statistical tests can result in a **false positive rate of over 45%**, even if the Type-I error rate is set at 5%"* ([bioRxiv 819334](https://www.biorxiv.org/content/10.1101/819334v2.full)). Báo **khoảng tin cậy của hiệu ghép cặp**, không phải hai khoảng rời — đọc hai khoảng chồng nhau là lỗi kinh điển. ProteinGym cũng dùng *"the non-parametric bootstrap standard error of the difference"* `[đọc]` `[đề xuất]`.
4. **Một ngày — bộ thước đo ba tầng.** Chính: AUROC mức ô trên bộ bão hòa (đề xuất C-9, đang chờ Trọng) và precision@3 mức residue trên bộ quét. Phụ: top-k có **sai số ±1 vị trí**, Jaccard/F1 sau khi **nở ±1** cả hai tập, và hồi quy trên cửa sổ trung bình 5–7 residue theo đúng cách QCDPred làm. Chẩn đoán (không phải chỉ số): trùng khít tập vị trí, báo cạnh con số 16,0% của replicate để **chứng minh** vì sao không dùng nó `[đề xuất]`.
5. **Vài ngày — tính Spearman theo cách của Kermut**: một hệ số cho mỗi tập mỗi split trên dự đoán gộp các fold, **không** lấy trung bình Spearman từng fold, vì ở n ≈ 91 mỗi fold thì Spearman từng fold cực kỳ bất ổn ([Kermut](https://arxiv.org/pdf/2407.00002)) `[đọc]` `[đề xuất]`.

**Điều vẫn có thể giết nó:** nếu phép tính lực ở n = 91 cho thấy **không phát hiện được** cả dư địa 0,1827 ở mức cụm (ví dụ chỉ có 8–12 cụm protein trong 91 peptide), thì bậc 3 không còn là bậc chính được, và vì D-026 đã bỏ dự phòng, **không còn đường lùi nào trong đề tài này** — sẽ phải mở lại câu hỏi phạm vi với GVHD. Bộ nhân Larsen **không** cứu được tình huống đó (mục 4.2).

### 5.2 Rủi ro 2 — phần dư có thể chỉ là nhiễu

**Điều mới biết.** Bài 9 đã ghi rằng lo ngại này "phần lớn là đúng" (75,9% phần dư là nhiễu trên bộ quét) và rằng siết read 10 → 200 thất bại. Điều mới là **giờ đã có lời giải thích trích dẫn được, từ hai nguồn độc lập, và cả hai kê cùng một thuốc**.

**DiMSum** (Faure, Schmiedel, Baeza-Centurion, Lehner, *Genome Biology* 2020;21:207, [PMC7429474](https://pmc.ncbi.nlm.nih.gov/articles/PMC7429474/)) phân rã phương sai điểm fitness của một replicate thành **hai số hạng phụ thuộc số đọc cộng một số hạng cộng không phụ thuộc số đọc**:

`σ²(f_{r,i}) = m_r^input / N_{r,i}^input + m_r^output / N_{r,i}^output + a_r`

và viết nguyên văn: *"**Additive error terms are independent of variant read counts** … However, if such highly abundant variants are of interest, **increasing sequencing coverage will not lead to reductions in the measurement errors of their fitness scores.**"* Thuốc họ kê cũng nguyên văn: *"increasing the number of replicate experiments … **even at similar overall sequencing coverage**"* `[đọc]`. Đây **chính xác** là lời giải thích cho "10 → 200 không giảm tỉ lệ nhiễu mà mất một nửa dữ liệu": siết ngưỡng chỉ thu nhỏ hai số hạng `m_r/N`, còn `a_r` thì không chạm được; khi các biến thể còn lại đủ dồi dào để `m_r/N ≪ a_r` thì tỉ lệ nhiễu đo được **bị sàn bởi `a_r`** và trơ với mọi ngưỡng tiếp theo `[phân tích]`.

**Enrich2** (Rubin et al., *Genome Biology* 2017;18:150, [PMC5547491](https://pmc.ncbi.nlm.nih.gov/articles/PMC5547491/)) cho một mũi độc lập, và còn mạnh hơn vì nó là **kết quả thực nghiệm**: *"Read count cutoffs eliminate low-count variants that may be unreliably scored due to sampling error, **but ignore other sources of noise** and may introduce a bias against variants that become depleted after selection."* Và bằng số: trên E4B, lọc theo sai số chuẩn ngẫu nhiên cho r² = 0,80 so với **lọc theo số đếm thư viện đầu vào r² = 0,58**; còn trên C2 domain, *"input count filtering selected a subset of variants whose scores were **more poorly correlated** than the unfiltered set"* `[đọc]`. Tức **siết ngưỡng read đã từng làm *xấu* đi độ tương đồng giữa replicate trong một bộ dữ liệu đã công bố** — đúng hướng với kết quả âm của repo `[phân tích]`.

Điều mới thứ hai: **bộ nhân Larsen công bố SD từng tile**, nên phép phân rã "bao nhiêu phần dư là nhiễu" **có thể làm lại trên một bộ dữ liệu thứ hai, độc lập, cùng họ assay** — một phép kiểm tính vững mà bài 9 chưa có `[phân tích]`. Điều mới thứ ba là một **rủi ro khoa học mới cùng họ**: LeBlanc et al. 2026, với 30 seed × 200 bootstrap trên 17.732 tile, báo rằng ma trận tham số của họ có *"**horizontal streaks, indicating that composition is more important than individual positions**"* và rằng *"The convolutional filters are **not picking up on specific protein motifs** and instead are picking up composition patterns"* `[đọc]`. Nếu điều đó cũng đúng cho tile degron thì **một mô hình mức residue có thể đang khớp nhiễu vị trí** — và bài báo của họ cung cấp luôn **khuôn thí nghiệm** để kiểm: báo độ ổn định của trọng số theo từng vị trí qua các seed và bootstrap `[phân tích]`.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí — viết lại kết quả âm thành một phát hiện có trích dẫn.** Mục "đừng thử lại hướng này" ở bài 9 nên dẫn DiMSum (số hạng `a_r`) và Enrich2 (C2 domain) `[đề xuất]`.
2. **Miễn phí — ghi nhận rằng D-025 đã giảm rủi ro này đi rất nhiều.** Trên bộ bão hòa, nhiễu là **16,7%** và Jaccard nhãn là **0,6596**, so với 75,9% và 0,4965 trên bộ quét. Lo ngại "phần dư là nhiễu" **mất phần lớn sức nặng** sau khi đổi nguồn nhãn chính `[đo]` + `[phân tích]`.
3. **~1 ngày — huấn luyện có trọng số theo độ chính xác.** `w_i = 1/σ̂_i²` lấy từ hai replicate, với **Huber** thay MSE. Tiền lệ: WLS của Enrich2 *"replicate agreement for scores calculated using the weighted least squares regression model is **higher** than agreement for scores calculated using ordinary least squares"* `[chưa xác minh — Genome Biology bị chặn, chỉ có tóm tắt]`, và phép trung bình có trọng số nghịch phương sai của DiMSum `[đọc]`. **Chế độ thất bại phải phòng:** với chỉ 2 replicate, phương sai từng mẫu tự nó cực nhiễu và trọng số có thể **khuếch đại** nhiễu — đúng lý do DiMSum chia sẻ phương sai giữa các biến thể; nên **khớp một đường cong phương sai–độ sâu toàn cục** thay vì dùng SD thô của 2 replicate `[đề xuất]`.
4. **~1 ngày — nhãn mềm có cơ sở.** Label smoothing cho đầu phân loại "có footprint" với `ε ≈ 1 − 0,893 = 0,107` lấy từ tỉ lệ bất đồng đo được, thay cho con số 0,1 tuỳ ý `[đề xuất]`.
5. **2–3 ngày — đầu heteroscedastic Gaussian NLL** (`torch.nn.GaussianNLLLoss`, dự đoán `log σ²`), theo Kendall & Gal, những người gọi nó là *"learned attention"* và nói nó *"makes the loss more robust to noisy data"* ([arXiv:1703.04977](https://arxiv.org/abs/1703.04977)) `[đọc]`. Ba chế độ thất bại: mạng có thể tối thiểu hoá loss bằng cách **khai báo mọi thứ đều bất định**; nó có thể làm **xấu** độ chính xác điểm khi trần đã bị nhiễu chi phối; và nó bắt luận văn phải **đánh giá hiệu chuẩn**, việc mà Kermut cho thấy là khó thuyết phục `[đọc]` + `[phân tích]`.
6. **Không nên làm:** tái phân tích Bayes phân cấp đầy đủ trên read thô (một bản sao Rosace). Đó là câu trả lời thống kê đúng nhưng ngoài phạm vi vài tuần CPU của một sinh viên; **trích Rosace như phương án nguyên lý trong phần hạn chế/hướng phát triển** `[đề xuất]`. Cũng **không nên** co-teaching hay bất kỳ phương pháp chọn mẫu theo "small-loss": chúng cần hai mạng, một lịch tỉ lệ nhiễu, và đủ dữ liệu để bỏ phần loss cao vẫn còn tập dùng được; ở n hàng trăm, chúng sẽ **chọn đúng những peptide dễ, độ sâu cao** — chính phép chọn mà audit đã chứng minh **không** giảm tỉ lệ nhiễu `[phân tích]`.

**Điều vẫn có thể giết nó:** nếu phép kiểm độ ổn định theo seed/bootstrap (ý 3 ở trên, theo khuôn LeBlanc) cho thấy trọng số theo vị trí **không ổn định** trong khi tổng theo acid amin thì ổn định — tức "thành phần > vị trí" cũng đúng cho degron — thì nhiệm vụ mức residue mất cơ sở khoa học, bất kể thước đo hay kiến trúc nào.

### 5.3 Rủi ro 3 — G3, ứng dụng không khác biệt được

**Điều mới biết.** Bốn tiền lệ ở bài 9 **đã thành năm**: Degformer (xem mục 6) xuất **ma trận 28 × 20 ΔPSI** từ đúng bảng S1+S4+S7 của Zhang, **locally, bằng một script Python** `[đọc]`. Thêm nữa, **DegronMD** (*Mol Biol Evol* 2023, msad253) là một tiền lệ **đã công bố** có module đột biến mà repo bỏ sót hoàn toàn `[đọc]`. Và hai khẳng định trong danh sách khác biệt hoá của repo **sai**: **MetaDegron và DegronMD đều có batch submission**, nên "batch" **không phải** điểm khác biệt và phải bị gỡ khỏi dòng G3 `[đọc]`.

Nhưng phép kiểm từng tính năng, đọc từ tài liệu/bài báo của từng công cụ, cũng xác nhận **năm khoảng trống thật**:

| Tính năng | DEGRONOPEDIA | MetaDegron | DegronMD | PAP/QCDPred | Degformer |
|---|---|---|---|---|---|
| Batch | **Không** (*"only one protein at a time"*) | **Có** | **Có** | Colab/GitHub | script cục bộ |
| API lập trình | không nêu | không nêu | không nêu | không | không |
| Chấm **đột biến tuỳ ý** | **Không** — chỉ tra COSMIC | **Không** có module | **Không** — chỉ đột biến soma đã quan sát | ΔPAP người dùng tự tính | **Có, cục bộ** |
| Xuất **ma trận vị trí × acid amin** | không nêu | không nêu | không nêu | Larsen dựng tay cho HSF1 | **Có** |
| **Bất định từng dự đoán** | Không | Không | chỉ cho degron, không cho đột biến | Không | Không |
| **Xuất xứ nhãn thực nghiệm** từng dự đoán | không nêu | không nêu | không nêu | — | Không |
| **Dự đoán theo ngăn tế bào** | không nêu | không nêu | không nêu | **chỉ bào tương** (hạn chế do Larsen 2025 nêu) | Không |

Tất cả `[đọc]`, từ [tài liệu DEGRONOPEDIA](https://degronopedia.com/degronopedia/documentation), [MetaDegron, Brief Bioinform 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723), [DegronMD, MBE 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958), và mã nguồn Degformer.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí — sửa tài liệu.** Gỡ "batch" khỏi danh sách G3; thêm Degformer và DegronMD vào bảng tiền lệ; đổi câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20" thành câu đúng về **điều kiện đánh giá** (mục 5.5) `[đề xuất]`.
2. **Rẻ, và đây là chỗ giá trị thật nằm — bốn tính năng không công cụ nào có:** (a) **API** — khoảng trống đã xác minh ở cả ba server, và là thứ dễ biện minh nhất cho một luận văn **Kỹ thuật phần mềm**; (b) **chấm đột biến tuỳ ý kèm xuất ma trận** qua web (Degformer chỉ làm được cục bộ); (c) **bất định từng dự đoán neo vào trần nhãn đã đo** — một công cụ trả về "ΔPSI = −1,2, nhưng nhãn mức residue của assay này chỉ lặp ở Jaccard 0,50 nên hãy coi danh tính residue là bất định" sẽ là **duy nhất và trung thực**, và nó **tiền tệ hoá** đúng phần mạnh nhất của repo; (d) **xuất xứ nhãn** — repo đã tính được rằng **725/770 peptide footprint có một tile trong tập train của PAP**, đúng loại thông tin người dùng cần để biết dự đoán là nội suy hay ngoại suy `[phân tích]` `[đề xuất]`.
3. **Rẻ và do chính lĩnh vực nêu — cờ áp dụng theo ngăn tế bào.** PAP là mô hình **chỉ bào tương** theo chính lời tác giả Larsen; một dòng cảnh báo kiểu "dự đoán này đến từ mô hình huấn luyện trên dữ liệu bào tương; protein của bạn nằm trong nhân" là tính năng **rẻ, trung thực và chưa thấy ở đâu** `[phân tích]`.
4. **Lựa chọn chiến lược chưa được xét — MAVISp.** *Protein Sci* 2026-01-22 ([10.1002/pro.70548](https://doi.org/10.1002/pro.70548)) là "modular structure-based framework for protein variant effects" và **đã trích Larsen**. Tích hợp thành một module của MAVISp có thể là câu chuyện ứng dụng tốt hơn một server đứng riêng, vì nó thừa hưởng người dùng sẵn có và **vô hiệu hoá hoàn toàn** phản biện "lại một web server nữa" `[chưa xác minh — chỉ có bản ghi thư mục]` `[đề xuất]`.

**Điều vẫn có thể giết nó:** nếu GVHD giữ kỳ vọng "kiến trúc chưa ai dùng" (đã nói 11/10) thì một tập tính năng ứng dụng — kể cả tập trên — **không đáp được** tiêu chí đó. Đây là lý do C-7 (chuyển chỗ đặt đóng góp sang nhiệm vụ và benchmark) **cần Trọng quyết, và nên hỏi GVHD cùng C-5**.

### 5.4 Rủi ro 4 — kiến trúc có thể không cần thiết, hoặc không thắng

**Điều mới biết, 4a (MIL không cần thiết).** Lý lẽ của Ilse, Tomczak & Welling cho gộp ở mức embedding là *"avoids the extra error that comes from training an instance classifier without instance labels"* ([PMLR v80](https://proceedings.mlr.press/v80/ilse18a/ilse18a.pdf)) `[đọc]` — nhưng đó là lý lẽ về nhãn **vắng mặt**, không phải nhãn **nhiễu**. **Không tìm thấy** bài nào so sánh có kiểm soát giữa giám sát mức túi và giám sát mức thể hiện **theo tỉ lệ nhiễu nhãn**; nên luận văn **không được** viết "MIL được biết là bền hơn với nhiễu nhãn mức thể hiện" — khẳng định đó, theo những gì kiểm được, **không có nguồn** `[phân tích]`. Ngược lại, văn liệu WSI nói thẳng chiều phản: *"State-of-the-art MIL models achieve competitive performance at the bag level. However, **instance-level prediction** … remains unsatisfactory."* ([arXiv:2307.02249](https://arxiv.org/html/2307.02249v2)) `[đọc]` — tức đe doạ trực tiếp đúng khẳng định "vị trí nào" của đề tài. Và trong phạm vi degron, **mọi** mô hình đã khảo sát đều dùng mục tiêu scalar mức cửa sổ với phép gộp đơn giản: PAP **global average pooling**, MetaDegron-D **max-pooling**, Degformer **CLS token**, DEGRONOPEDIA/DegronMD hồi quy không tuần tự — **chưa thấy** mô hình degron nào dùng attention pooling hay đầu giám sát mức residue `[đọc]`.

**Điều mới biết, 4b (phép gộp).** Nhận xét 2012 trên calmodulin rằng *"phép chọn cửa sổ quan trọng ngang với khuôn học"* là cảnh báo cụ thể: **ablation MIL-vs-đầu-vị-trí phải giữ cửa sổ cố định** `[chưa xác minh — chỉ tóm tắt]`. Và đừng dùng **max**: max pooling đặt toàn bộ gradient lên một residue mỗi peptide, mà với nhãn thể hiện ở Jaccard 0,50 thì việc đó gần như tung xu; **top-k (soft bag)** và **noisy-OR** phân tán gradient, và cả hai đều có tiền lệ đối chứng trực tiếp ([soft bags/top instances](http://www.svcl.ucsd.edu/publications/conference/2015/softbag/softbag_final.pdf), [max vs noisy-OR](https://arxiv.org/pdf/1804.01146)) `[đọc]`.

**Điều mới biết, 4c (cổng phơi lộ) — và đây là phần đổi nhiều nhất.** Hai điều. Một, **phản biện bắt buộc phải chuẩn bị**: trong Yang et al., *PLOS Comput Biol* 22(8):e1014552 ([10.1371/journal.pcbi.1014552](https://doi.org/10.1371/journal.pcbi.1014552)), **rASA là đặc trưng node đầu vào** (cùng DSSP 8 lớp), **đặc trưng cạnh là hình học thuần** (khoảng cách Euclid + vector hướng đơn vị), và **attention pooling được điều khiển bởi một vector truy vấn học được** — *"we incorporated a **learnable query vector** into the attention-based residue pooling mechanism to adaptively focus feature aggregation on functionally relevant regions"* `[đọc]`. Tức **không** phải cổng theo độ lộ. **Nhưng** một attention pooling học được, trên các node mà đặc trưng **đã bao gồm rASA** và đã đi qua 4 lớp GAT, **về nguyên tắc có thể biểu diễn một cổng phơi lộ** — nó là **tập mẹ thực sự** của cổng đặt tay. Nên luận văn **không thể** dựa vào "chưa ai đặt độ lộ gần bước gộp"; nó phải dựa vào **một ablation** cho thấy cổng tường minh thắng attention pooling học được **khi cả hai nhận cùng đặc trưng rASA/pLDDT**. Bảng ablation của chính Yang et al. là khuôn: thay attention pooling bằng average pooling làm MCC rơi **0,83 → 0,71**; bỏ RSA làm ROC-AUC giảm **4%**; và họ **chưa bao giờ chạy ô chéo** (pooling học được *không* có RSA đầu vào so với pooling có điều kiện RSA) — **đúng ô trống mà luận văn có thể chiếm** `[phân tích]`.

Hai, **bộ nhân Larsen cho nơi để chạy ablation đó** (mục 4.3): nó là bộ dữ liệu duy nhất trong tầm với mà rASA/pLDDT **có phương sai** và đã được chú giải sẵn ở mức tile `[phân tích]`.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí — phát biểu lại khung.** Không trình bày MIL như một kết quả đã biết; trình bày như **một thí nghiệm có tiên đoán ghi trước**. Audit nói nhãn mức túi (có footprint) lặp 89,3% còn nhãn mức thể hiện (vị trí nào) chỉ Jaccard 0,4965 — lý lẽ của Ilse et al. khớp gần như từng chữ với hai con số đó. Đó là **động lực trích dẫn được**; **kết quả thì phải đo** `[đề xuất]`.
2. **Vài ngày — ablation 3 nhánh trên cùng backbone, cùng cửa sổ, cùng loss Huber có trọng số:** (1) đầu hồi quy/phân loại theo vị trí, huấn luyện trên nhãn thể hiện; (2) attention-MIL mức embedding với **gated attention** theo Ilse et al., chỉ huấn luyện trên nhãn túi, đọc trọng số attention làm footprint; (3) lai: loss túi + loss thể hiện hạ trọng số (λ ≈ 0,1–0,3). Chấm **cả ba** trên **cả** chỉ số túi **và** chỉ số thể hiện có sai số ±1. Đầu MIL là ~50 dòng trên một đầu theo vị trí sẵn có `[đề xuất]`.
3. **Chuẩn bị trước chế độ thất bại mà văn liệu WSI đã ghi:** attention-MIL rất có thể **thắng chỉ số túi** và **thua hoặc hoà** ở định vị thể hiện. Nếu đúng vậy, kết luận trung thực và vẫn có giá trị là "giám sát mức túi là mục tiêu đúng cho đích lặp lại được; định vị thể hiện cần loss lai", trích arXiv:2307.02249 cho việc đây là khuôn mẫu **được dự kiến**, và ItS2CLR làm thuốc đã công bố `[đọc]` `[đề xuất]`.
4. **Vài ngày — ablation ô chéo cho cổng phơi lộ, ở mức tile, trên bộ nhân Larsen.** Bốn ô: pooling học được ± rASA đầu vào × cổng tường minh ± rASA. Đây là đóng góp kiến trúc khả thủ duy nhất còn lại sau khi C-8 hạ cổng xuống cơ chế chuyển giao `[đề xuất]`.
5. **Quan trọng — cổng phải *học được và có dấu*, không phải mặt nạ cứng.** Sinh học 2026 chống lại một tiên đề đơn điệu: *"BAG6 and RNF126 promote the degradation of cytosolic misfolded proteins that contain **buried** degron motifs"* (bioRxiv 2026-04-25) `[chưa xác minh — chỉ tiêu đề]`, và Schulze 2026 có **PRKN S109**, một residue **phơi lộ** mà đột biến có vẻ *tạo ra* một degron kiểm soát chất lượng `[đọc, qua prior-art của repo]`. Phép đo đảo dấu của chính repo (−0,1928 vùng chôn so với +0,3733 vùng phơi lộ) khớp với tính **không đơn điệu**, không khớp với một mặt nạ `[đo]`.

**Điều vẫn có thể giết nó:** nếu ablation ô chéo cho thấy pooling attention học được **có cùng rASA đầu vào** đạt bằng hoặc hơn cổng tường minh, thì thành phần 4 mất lý do tồn tại hoàn toàn — và vì C-8 đã hạ nó xuống cơ chế chuyển giao, điều đó **không giết đề tài**, nhưng giết **thành phần** đó và phải ghi vào luận văn như một kết quả âm.

### 5.5 Rủi ro 5 — tính mới bị thu hẹp thêm

**Điều mới biết.** Bảng thu hẹp ở bài 9 có năm dòng; phiên này thêm **bốn dòng nữa**:

| Ngày | Phát hiện | Mất gì |
|---|---|---|
| 15/10 | **Degformer** (GitHub, Apache-2.0, 2026-03 → 2026-09) huấn luyện trên **đúng** S1+S4+S7 của Zhang, `MAX_LEN = 28`, và ship `saturation_mut_heatmap.py` xuất **ΔPSI trên 28 vị trí × 20 acid amin** `[đọc]` | **Claim "ma trận 28×20 là thứ không tiền lệ nào xuất" chết như đang viết** |
| 15/10 | **DegronMD** (MBE 2023) là tiền lệ **đã công bố** có module đột biến (rule-weighted, chỉ đột biến soma đã quan sát, mức instance) `[đọc]` | Một tiền lệ bị bỏ sót, phải trích |
| 15/10 | **LeBlanc et al., Cell Systems 17(9):101701** đã làm: tách abundance khỏi function trên thư viện tile; **split theo cụm protein phân cấp** trên tile chồng 35/40 residue, kèm kiểm "tương đồng test–train vs độ chính xác"; và **đối chiếu trần replicate bằng số (0,555 so với 0,568)** `[đọc]` | Ba lập luận hỗ trợ **hạ xuống "thực hành chuẩn"**, phải viết "theo LeBlanc et al. 2026" |
| 15/10 | **Yang et al., PLOS Comput Biol 2026** kết hợp **rASA đầu vào** với **attention pooling** trong một mô hình, và pooling học được là **tập mẹ** của cổng đặt tay `[đọc]` | Tính mới của claim 3 co lại thành **một ablation bắt buộc**, không còn là một tuyên bố |

Hai điều **không** thu hẹp nó, và đáng ghi nhận rõ. **Một**, LeBlanc et al. **không** pre-empt claim về mô hình mức residue: grep triệt toàn văn tìm `per-residue`, `residue-level`, `single-residue`, `saturation`, `variant effect`, `mutagenesis` trả về **không kết quả nào** trong thân bài; mọi chỉ số của họ là **Pearson/Spearman mức tile** trên n = 2.521; và khi có đối thủ mức residue họ **gộp nó về mức tile** (*"To get a single value for ADPred, we averaged the predictions for the 40aa tile"*) `[đọc]`. **Hai**, **không có công cụ dự đoán degron mới nào được công bố trong 2025–2026** qua hai cơ sở dữ liệu độc lập: PubMed `degron AND (prediction OR machine learning OR deep learning OR predictor)`, 2025/01/01–2026/10/31, **41 bản ghi**, đọc 21 tiêu đề, **không có** công cụ hay web server dự đoán degron mới; Europe PMC `TITLE_ABS:"degron"` + từ khoá ML, 2025–2026, **100 hit**, và `TITLE:"degron"` **127 hit**, đọc 40 tiêu đề mỗi lần, **cũng không** `[đọc]`. Đây là **tín hiệu thời điểm tốt nhất trong cả báo cáo**, và phải viết đúng dạng "đã chạy truy vấn X, không tìm thấy", **không** viết "chưa ai làm".

Thêm một tín hiệu củng cố: Larsen 2025 có **9 citation** và Voutsinos 2026 có **11**, và trong **19 bài trích khác nhau, không bài nào** là mô hình dự đoán degron, làm footprint degron mức residue, hay dựng ma trận thay thế cho degron — cộng đồng trích dẫn là sinh học TF, lý sinh/mô phỏng và proteostasis `[đọc]` ([Semantic Scholar](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1101/2025.05.16.654404)).

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí và bắt buộc — sửa câu chữ ở ba chỗ.** Xoá "thứ cả bốn/năm tiền lệ đều không có" khỏi `topics/degron-footprint/README.md` (dòng G3), `research/topic-decision.md §7` và `full-data-audit §6.2`; thay bằng: *"ma trận 28 × 20 đã từng được tạo — bởi Degformer trên cùng nhãn, và bởi Larsen 2025 cho từng protein đơn lẻ — nhưng **chưa bao giờ dưới một split theo cụm protein, chưa bao giờ kèm trần nhãn đã đo, chưa bao giờ kèm bất định từng ô, và chưa bao giờ có điều kiện theo lớp phơi lộ"*` `[đề xuất]`.
2. **Miễn phí — phát biểu claim 1 theo đúng điều kiện còn sống:** *"mô hình degron mức residue đầu tiên được **giám sát ở mức residue** và **đánh giá ở mức residue** dưới split cụm protein, đối chiếu một trần nhãn đã đo"* — không phải "dự đoán degron mức residue đầu tiên" `[đề xuất]`.
3. **Miễn phí — chấp nhận [C-7] hay không là quyết định của Trọng.** Đề xuất C-7 (chuyển chỗ đặt tính mới sang **nhiệm vụ và benchmark**) đang chờ xác nhận và **không được coi là đã chốt**; nó cũng kèm một rủi ro đã ghi: D-012 vẫn đòi một đóng góp **dương đo được**, nên mô hình vượt 0,4897 (hoặc AUROC vượt 0,7692) **vẫn bắt buộc** — benchmark một mình không đủ `[đọc]`.
4. **Nửa ngày đọc — ba bài còn phải đọc trước đề cương**, theo thứ tự: *Nat Chem Biol* 2025-11 "beyond short linear motifs" (rủi ro phạm vi, mục 6); *Nat Commun* 2026-05-15 "coarse-to-fine PTM" (nơi khả dĩ nhất có tiền lệ bag→residue); và toàn văn QCDPred/DEGRONOPEDIA/JoGo mà bài 9 đã ghi là còn `[qua tóm tắt]` `[đề xuất]`.

**Điều vẫn có thể giết nó:** một bài mới xuất hiện trong 8 tuần tới làm đúng "giám sát mức residue trên nhãn degron thực nghiệm, split theo cụm". Không kiểm soát được; cách giảm thiểu duy nhất là **đặt điểm kiểm G2 sớm** (đề xuất cuối tuần 10, theo phần A của DECISIONS) và chạy lại hai truy vấn PubMed/Europe PMC ở trên trước khi nộp.

### 5.6 Rủi ro 6 — thước đo không thống nhất với GVHD

**Điều mới biết.** Bài 9 đặt đây là "hỏi ở buổi gặp tuần 6", và **tuần 6 là 16/10** — tức ngày mai. Phiên này cho ba thứ làm câu hỏi đó sắc hơn.

Một, **con số mà GVHD rất có thể neo vào đã có tên và chủ**: **PAP Pearson 0,79 trên tile TF**, do chính Larsen đo và in `[nguồn]`. Đó là một con số mức tile, trên thang mà trần cải thiện của đề tài chỉ **+0,0032** — nên nếu không thống nhất trước, buổi bảo vệ sẽ diễn ra trên thang sai `[phân tích]`.

Hai, **có tiền lệ công bố cho chính cách trình bày mà đề tài cần**: LeBlanc et al. đặt **0,555 cạnh 0,568** trong câu kết quả `[đọc]`; RECOVER đặt 0,47 cạnh 0,64 `[đọc]`; ProteinGym chọn Spearman làm chỉ số chính *"because of the often non-linear relationship between protein function and organism fitness"* và bổ sung AUC, MCC, NDCG và **Top-K recall ở K = 10%** cho trường hợp phân bố hai đỉnh `[đọc]`. Và QCDPred — tiền lệ gần nhất về dữ liệu — báo **Spearman mức peptide**, không bao giờ báo khớp chính xác mức residue `[đọc]`. Tức "chỉ số chính ở mức peptide/ô, chỉ số phụ ở mức vị trí có sai số" **không phải phát minh của đề tài**, nó là thực hành của lĩnh vực.

Ba, **điều nên nói rõ là trần, không phải chỉ số**: trần nhãn Spearman mức ô chỉ **0,6989** còn trần **AUROC mức ô đạt 0,9519** — xếp hạng *mọi* ô thì khó, nhưng *tách ô dương khỏi ô âm* thì nhãn làm rất tốt, và nhiệm vụ của đề tài là cái sau `[đo]`. Đó là lý lẽ đứng sau đề xuất C-9, **đang chờ Trọng**.

**Cách xử lý — ba câu cụ thể nên đưa vào bản chuẩn bị buổi gặp** `[đề xuất]`:

1. "Thầy muốn con báo **Pearson trên thang điểm đoạn** (thang mà PAP đạt 0,79 và trần cải thiện là +0,003), hay **AUROC mức ô / precision@3 mức residue** (thang mà dư địa đo được là 0,1827 và 0,1617)?" — và kèm bảng ba dòng cho thấy hai thang cho hai kết luận trái nhau.
2. "Con dự định đặt **một dòng replicate-vs-replicate trong mọi bảng kết quả** làm trần nhãn, theo cách LeBlanc et al. 2026 và RECOVER làm. Thầy có đồng ý đó là cách trình bày đúng, hay thầy muốn con báo số thô?"
3. "Vì n thật của bộ bão hòa là **91 peptide** và đơn vị suy luận là **cụm protein**, con dự định **cam kết trước** rằng phần lớn ablation sẽ không phân biệt được về thống kê, và chỉ báo **một phép so sánh chính**. Thầy có chấp nhận cách đó?"

**Điều vẫn có thể giết nó:** nếu GVHD khẳng định Pearson mức đoạn là thước đo duy nhất ông chấp nhận, thì trần đóng góp của đề tài là **+0,003** và **toàn bộ thiết kế phải làm lại** — đây là lý do câu hỏi này không được để trượt khỏi buổi 16/10.

### 5.7 Rủi ro 7 — nợ kỹ thuật nhỏ

**Điều mới biết.** Năm mục ở bài 9 vẫn đúng, và phiên này thêm bảy mục nữa — hầu hết do chạm vào dữ liệu/mã bên thứ ba:

| Việc | Chi tiết | Chi phí |
|---|---|---|
| 19 footprint đã map accession nhưng chưa khớp peptide + 3 thiếu trình tự | **cần curate** (từ bài 9) | giờ |
| 9 accession chưa lấy được trình tự UniProt | đã loại khỏi split, **không được giả làm singleton** (từ bài 9) | — |
| 813 peptide có stop `*` cuối (336 là footprint) | phải **mask**, không coi `*` là acid amin (từ bài 9). **Điểm đối chứng mới:** Degformer đặt `*` làm **token thứ 21** đưa thẳng vào `nn.Embedding`, không mask, không nhánh riêng, và scan bão hòa **không bao giờ** thăm nó — một khác biệt phương pháp cụ thể để nêu `[đọc]` | giờ |
| Cụm MMseqs2 trong `interim/` ghi đường dẫn tuyệt đối cũ | chạy lại `prepare_protein_clusters.py` (từ bài 9) | phút |
| Split 80/10/10 qua 5 seed | là **phép thử đo quy mô**, chưa phải benchmark chính thức (từ bài 9) | — |
| **Đếm và báo số cụm protein** ở n = 91 và n = 271–322 | đơn vị suy luận, không phải số peptide (mục 5.1) | giờ |
| **Báo cỡ split đã thực hiện ở mức trình tự**, không chỉ tỉ lệ dự định | vì cụm lệch cỡ: *"this cluster-wise 80/20 split produces a sequence-wise 83/17 distribution"* ([AMPBench-MT](https://arxiv.org/pdf/2607.25518)) `[đọc]` | giờ |
| **Báo cả `--min-seq-id` và `-c` (coverage)** của MMseqs2 trong Methods | ngưỡng trong lĩnh vực chạy từ 20%/30%/50% (MMseqs2) tới 40% (CD-HIT) `[đọc]` | phút |
| **Thêm một baseline split ngẫu nhiên cạnh kết quả split cụm** | khoảng cách giữa hai cái **là** ước lượng rò rỉ; và PepBenchmark ghi nhận có bộ dữ liệu mà split MMseqs2 lại **cao hơn** split ngẫu nhiên `[đọc]` | giờ |
| **Nếu tải CSV của Larsen:** thêm `data/raw/SOURCE.md` với thông báo MIT + tên repo + tag/commit + DOI Zenodo | điều kiện duy nhất của MIT (mục 2.3) | phút |
| **Nếu nạp checkpoint Degformer:** `torch.load(..., weights_only=False)` + một `StandardScaler` đã pickle | nạp nó **thực thi mã pickle tuỳ ý**, và sklearn phải có mặt dù `predict.py` không import — xử lý như dữ liệu không tin cậy, chạy trong thư mục riêng `[đọc]` | phút |
| **Tra lại Crossref `relation` và API pubs của bioRxiv trước khi nộp** | để trích bản chính thức nếu Larsen 2025 được công bố trong 8 tuần tới (repo được push 01/10/2026, Zenodo có tag "publication release" 01/06/2026 → **có thể đang in**) `[phân tích]` | phút |

**Điều vẫn có thể giết nó:** không mục nào trong bảng này giết được đề tài; nhưng mục `*` và mục "số cụm" đều có thể **làm sai một con số đã công bố trong luận văn**, nên chúng nên xong trước khi chạy benchmark chính thức.

---

## 6. Tiền lệ mới phải tính vào

### 6.1 Degformer — đối thủ trực diện nhất, và yếu nhất

`Alpine2048/Degformer`, Apache-2.0, tạo **24/03/2026**, push cuối **30/09/2026**, **0 star, 0 fork, 0 issue**, không bài báo, không preprint, không liên kết lab; tác giả **Oliver Hong**, 26/27 commit trong **một giờ** qua upload web UI, còn file `lol.md`/`temp.md` trong lịch sử `[đọc]` ([GitHub API](https://api.github.com/repos/Alpine2048/Degformer)). README tự nhận: *"Performs better than current composition or motif-search based methods and is applicable for protein degron mapping (internal + C-degrons only), in silico scanning/saturation mutagenesis for degron motif detection"* `[đọc]`.

Nó **thật và hoạt động được**: repo ship **ba checkpoint PyTorch** commit thẳng vào git (~2,2 MB mỗi cái) và **toàn bộ bảng huấn luyện 569.270 dòng** `training_data.csv` (19,9 MB, hai cột `sequence,controlPSI`, mọi trình tự đúng 28 residue, `controlPSI` trong 1,000–6,000, trung bình 3,6836) `[đo]`. Và nó xuất đúng artefact đề tài nhắm: `saturation_mut_heatmap.py` lấy `ΔPSI = pred(mutant) − pred(WT)` rồi pivot thành heatmap trên `residue_groups` 20 acid amin × 28 vị trí `[đọc]`.

Nhưng **điểm yếu của nó đã được đo, không phải suy đoán**:

| Điểm yếu | Bằng chứng | Nhãn |
|---|---|---|
| **Rò rỉ trình tự y hệt trong split của chính nó** | Tái lập đúng số học `ShuffleSplit` của sklearn (`RandomState(42).permutation(569270)`, n_test = 56.927): **1.954 trình tự 28-mer nằm ở cả hai nửa**, **2.330/56.927 = 4,09% dòng validation** là bản sao chính xác của một dòng train | `[đo]` |
| **9.443 trình tự trùng mang nhãn trái nhau** | 554.085 trình tự duy nhất / 569.270 dòng; 9.496 trình tự xuất hiện > 1 lần; trong đó **chỉ 53** có `controlPSI` giống nhau, **9.443** khác nhau; độ giãn trung vị 0,48, p90 1,41, **max 3,98** trên thang 1,00–6,00 | `[đo]` |
| **Không gộp nhóm gì cả** | Một lệnh `train_test_split(..., test_size=0.1, random_state=42)`, không `groups=`, không clustering, không dedup; `training_data.csv` **không có cột định danh protein** nên split theo cụm **không biểu diễn được** trên dữ liệu đã ship | `[đọc]` |
| **Đọc ra chỉ ở CLS token** | `return self.head(x[:, 0])` — 28 trạng thái ẩn của residue bị **bỏ đi**; không `need_weights`, không saliency, không đầu thứ hai | `[đọc]` |
| **Không cấu trúc, không PLM, không MIL** | Vocab 21 token `"ACDEFGHIKLMNPQRSTVWY*"` qua `nn.Embedding`; không rASA, không pLDDT, không disorder, không embedding PLM | `[đọc]` |
| **Tập blind vắng mặt** | README nói 10% để "final blind testing", nhưng **không có tập đó, không có script chia, không có script đánh giá** trong repo (cây file đầy đủ 15 entry, `truncated: false`) → **con số headline không tái lập được từ repo** | `[đọc]` |
| **"Correlation (ρ)" có lẽ là Pearson** | Hàm tương quan duy nhất trong repo là `scipy.stats.pearsonr`; không có `spearmanr` ở đâu. Trích 0,9420/0,9162 như Spearman **không có cơ sở** | `[đọc]` + `[phân tích]` |
| **Ship trọng số dạng pickle** | `torch.load(..., weights_only=False)` vì checkpoint mang một object scikit-learn → nạp là **thực thi pickle** | `[đọc]` |
| **Thêm: rò rỉ tiền xử lý** | `StandardScaler` được fit trên **toàn bộ** `training_data.csv` **trước** khi split | `[đọc]` |
| **Không seed** | `random_state=42` là seed duy nhất trong cả repo; **không** `torch.manual_seed`, `np.random.seed`, `torch.use_deterministic_algorithms` → hai file `epoch30` và `epoch30_run1` khác nhau và README không gán được cho file nào | `[đọc]` |

Số nó báo: Degformer e50 **S1 0,9420 · S4 0,9463 · S7 0,9162**, so với dòng baseline duy nhất "Elledge lab" **S1 0,8955**, hai ô S4/S7 **để trống**, và chú thích rằng baseline tính trên **toàn bộ 260K của S1** chứ không trên holdout 10% của Degformer — tức **0,8955 so với 0,9420 không phải so sánh tương đương** `[đọc]` + `[phân tích]`.

**Cách đọc đúng** `[phân tích]`: S7 là bão hòa, khoảng 28 × 19 đột biến mỗi degron, nên một mutant được giữ lại gần như **luôn** có ~500 anh em trong train; ρ = 0,9162 của nó do đó gần một **chặn trên của nội suy bên trong một degron đã biết**, không phải phép đo khả năng tổng quát hoá sang degron mới. Kết hợp với Livesey & Marsh — hai bộ DMS độc lập của **cùng một protein** chỉ tương đồng ở **ρ 0,34–0,94, trung bình 0,66** (2020), và các assay **thật sự khác điều kiện** thì **trung vị 0,54, phần lớn 0,4–0,6, < 0,3 khi điều kiện khác mạnh** (bản cập nhật 2023) `[đọc]` — thì một ρ = 0,94 trên một holdout ngẫu nhiên của **một** assay đang đo **sự ghi nhớ đặc thù của assay đó**, không phải sinh học.

**Hệ quả hành động:** **nhận Degformer làm baseline và đánh bại nó dưới cov80**, đừng im lặng về nó. Nó public, Apache-2.0, được index, và là kết quả đầu cho truy vấn hiển nhiên — GVHD hay người phản biện có thể tìm ra trong một lần tìm. Checkpoint và `predict.py` đã có trong repo nên **chạy lại `peptide_model_epoch50.pt` dưới split cov80 và thước đo mức residue là thí nghiệm giá-trị-trên-giờ cao nhất đang có** `[phân tích]` `[đề xuất]`.

### 6.2 Năm tiền lệ còn lại, và một rủi ro phạm vi

**DegronMD** (*Mol Biol Evol* 2023, msad253) — đầu ra là **per-degron-instance** (trình tự, phân loại, E3, start/end, xác suất DegML > 0,5), **per-mutation** (điểm DegMF 0–1, ngưỡng "actionable" 0,5) và **per-treatment**; **không có track điểm theo residue**. Module đột biến chỉ chấm **đột biến soma missense đã quan sát** trong TCGA/COSMIC/ICGC/CCLE/GDSC, và **DegMF là một tổng có trọng số theo luật, không phải mô hình huấn luyện trên đột biến thực nghiệm**; kiểm chứng chỉ in-silico (DynaMut). DegML huấn luyện trên **133 degron instance qua 23 motif**; quy mô 53.291 motif match, 18.007 degron dự đoán, 288.345 bản ghi đột biến `[đọc]`. **Nó không giết claim 2** — nó bị đánh bại trên ba trục nói được sạch (chỉ đột biến đã quan sát, điểm theo luật, mức instance) — nhưng nó **phải được trích** `[phân tích]`.

**LeBlanc et al.**, *Cell Systems* 17(9):101701, DOI [10.1016/j.cels.2026.101701](https://doi.org/10.1016/j.cels.2026.101701), PMID 42607673 (preprint bioRxiv 2025.09.19.677413 có trước một năm) — **không chạm vào degron**: từ "degron" xuất hiện đúng **ba lần**, toàn bộ trong văn xuôi về chồng lấp activation-domain/degron; nó trích Larsen (ref 47) và Voutsinos (ref 48) **chỉ như văn liệu hỗ trợ** cho một xu hướng thành phần trình tự `[đọc]`. Dữ liệu là sàng Sort-seq *S. cerevisiae* của chính họ, tile **40 aa cách nhau 5 aa** từ homolog của Gcn4, **20.731 tile thiết kế / 17.732 tile có dữ liệu**, và **tile có ở cả hai replicate thì lấy trung bình** `[đọc]`. Kiến trúc: **một** filter convolution (nhiều filter "rapidly became uninterpretable"), **138 tham số** cho ShallowNN so với 96.769 của ADhunter và 8 × 80.005 của PADDLE; đầu ra **một scalar mỗi tile**; tham số "biophysical" là **hằng số cân bằng mức tile, không phải năng lượng mức residue** `[đọc]`. Ba điều nó lấy đi của đề tài, và một điều nó **không** lấy: nó **không** pre-empt claim mức residue (mục 5.5). Nó cũng cho một lý lẽ biện minh tốt: họ có **hai phép đo ghép cặp mỗi tile** (mCherry và GFP) nên mới nhận diện được hằng số cân bằng hai/ba trạng thái; một thư viện tile degron với **một** readout độ ổn định **không** nhận diện được chúng — nên đường biophysical-NN **không khả dụng**, vì lý do phương pháp, không phải vì thiếu sót `[phân tích]`.

**Yang et al.**, *PLOS Comput Biol* 22(8):e1014552, 11/08/2026 — "Edge-aware GAT-based protein binding sites prediction", mở hoàn toàn. Đã trả lời xong câu hỏi quyết định: **rASA chỉ là đặc trưng node đầu vào** (cùng DSSP 8 lớp, chuẩn hoá về [0,1]), **đặc trưng cạnh là hình học thuần**, và attention pooling do **vector truy vấn học được** điều khiển; `pLDDT` **không xuất hiện ở đâu** trong bài (đầu vào là cấu trúc PDB thực nghiệm). Ablation của họ xử lý rASA và pooling như **hai thành phần rời**: bỏ secondary structure/−3% ROC-AUC, bỏ RSA/−4%; thay attention pooling bằng average pooling thì **MCC 0,83 → 0,71** `[đọc]`. Kết quả: ROC-AUC **0,93** so với PeSTo 0,91. **Phản biện bắt buộc trả lời** đã nêu ở mục 5.4: pooling học được trên node có rASA là **tập mẹ** của cổng đặt tay, nên ablation là **bắt buộc**, không phải tuỳ chọn. Một điểm an ủi: họ **tự nói** *"we did not construct an additional independent homology-controlled benchmark in this study"* và xếp CD-HIT/MMseqs2 vào future work — nên một luận văn ship split MMseqs2 **đi trước họ về vệ sinh đánh giá** `[đọc]`.

**BoM-Pooling** (Hoang & Singh, *Bioinformatics* 41(Suppl 1):i217, 15/07/2025, DOI 10.1093/bioinformatics/btaf178) — cascade trình tự thành k-mer chồng nhau, Avg-Pooling cục bộ trong mỗi cửa sổ, rồi **attention pooling** nén về vector cố định; động lực **thuần tính toán** (attention pooling đầy đủ là bậc hai theo độ dài; BoM-Pooling bậc hai theo số k-mer → nhanh 5–12×). Grep triệt tìm `solvent`, `accessib`, `rASA`, `RSA`, `pLDDT`, `exposure`, `buried` trả về **một hit tình cờ** duy nhất — **không có đầu vào cấu trúc nào** `[đọc]`. Cải thiện tới **11,4%** trung vị so với các phép pooling cùng cỡ tham số, thắng 15/17 thí nghiệm. **Không** pre-empt cổng, nhưng là tiền lệ cho "attention pooling trên embedding PLM mức residue" mà thành phần 3 của đề tài dùng `[phân tích]`.

**Wang & Zheng**, "Degrons and degradation signals beyond short linear motifs", *Nature Chemical Biology* 22(3):355–368, online 14/11/2025, DOI [10.1038/s41589-025-02056-2](https://doi.org/10.1038/s41589-025-02056-2), PMID 41238838 — **paywall, chỉ đọc được tóm tắt**; nature.com trả **303** về `idp.nature.com/authorize`, không có preprint, không có bản PMC `[chưa xác minh]`. Tóm tắt nguyên văn: *"While short linear motifs are frequently identified as degrons, an increasing number of degrons have recently been mapped to **high-order protein structures**, underscoring the architectural diversity and cryptic nature of degradation signals. Furthermore, **nonproteinaceous signals beyond degrons** often facilitate the precise control of protein ubiquitination."* `[đọc, tóm tắt]`. **Phân rã rủi ro này làm hai** `[phân tích]`: (i) degron "cấu trúc bậc cao" vẫn **nằm trong trình tự** — một cửa sổ 28-mer có thể chứa chúng, chỉ không biểu diễn được bối cảnh 3D làm chúng hoạt động hay bị che; lập luận này **tấn công mô hình 28-mer thuần trình tự** và **được trả lời, không bị phủ định**, bằng việc điều kiện hoá theo cấu trúc — nên bài này nên trích làm **động lực** cho cổng, chứ không phải làm mối đe doạ; (ii) **tín hiệu không-protein** (cofactor/ligand/cue cạnh PTM nằm trong substrate, trong E3, hay ở mặt tiếp xúc) thì **thật sự nằm ngoài mọi cửa sổ peptide, dài bao nhiêu cũng vậy** — đây là **trần không thể giảm** của dữ liệu tile và phải nêu như một **ranh giới ngoài phạm vi**, không tranh luận. Điểm then chốt: **chính assay nguồn nhãn cũng mang đúng giả định phạm vi đó** — Voutsinos 2026 tự ghi *"many degrons are buried and likely become active upon protein unfolding"* `[chưa xác minh — chỉ tóm tắt]`. Nên khung đúng là: **luận văn mô hình hoá đúng những gì assay tile 30-residue đo được**, và bài Wang & Zheng định nghĩa cái nằm ngoài phép đo đó — một hạn chế **chia sẻ với dữ liệu gốc**, dễ bảo vệ hơn hẳn việc khẳng định cửa sổ là đủ. Hai review 2025 chỉ **hai hướng hơi trái nhau** (Wang & Zheng: motif là không đủ; Zhang et al. *Nat Rev Mol Cell Biol* 2025: sàng thông lượng cao đang **mở rộng** số degron định nghĩa ở độ phân giải cao), nên **trích cả hai** là cách trung thực và giải toả phản biện phạm vi tốt hơn trích một cái `[phân tích]`.

**Ba tiền lệ phụ nên có mặt trong bảng related work** `[đọc]` trừ chỗ ghi khác: **Rosace** (*Genome Biology* 2024;25:138, [PMC11127319](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127319/)) đã thiết lập rằng **gộp thông tin giữa các vị trí cải thiện FDR và lực** trong DMS — *"Rosace leverages amino acid position information to increase power and control the false discovery rate by sharing information across parameters via shrinkage"* — nên đóng góp của luận văn phải phát biểu là **dự đoán nhận biết vị trí từ trình tự**, không phải "lần đầu dùng vị trí", và nên ghi thêm **Rosace-AA** 2026 `[chưa xác minh — chỉ siêu dữ liệu]`; **PTM-Mamba** (khối Mamba **có cổng**, nhận biết PTM, [PMC12074982](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12074982/)) là tiền lệ cơ học cho "gate một mô hình học được bằng một nhãn mức residue bên ngoài" `[chưa xác minh]`; và **ProSST** (NeurIPS 2024) ghi nhận rằng **vùng vô định hình bị AlphaFold2 dự đoán kém, điều này có thể làm hại các mô hình nhận biết cấu trúc** — đúng cảnh báo cần nêu khi dùng pLDDT `[chưa xác minh]`.

---

## 7. Việc nên làm, xếp theo thứ tự

**Nhóm A — không tốn gì, không cần tải, không cần GPU. Làm trước.**

1. **Tính lực thống kê ở n = 91, và đếm số cụm protein** trong 91 peptide đó (và trong 271–322 của bộ quét). Đây là **việc chặn duy nhất** theo phần A của DECISIONS.md, và số cụm là con số thật sự quyết định, không phải 91.
2. **Chuẩn bị ba câu hỏi thước đo cho buổi gặp 16/10** (mục 5.6). Cửa sổ này đóng trong một ngày.
3. **Sửa câu chữ ở bốn chỗ:** thêm Degformer làm tiền lệ **thứ năm** và DegronMD làm tiền lệ đã công bố; xoá khẳng định "không tiền lệ nào xuất ma trận 28×20" khỏi `topics/degron-footprint/README.md`, `research/topic-decision.md §7`, `full-data-audit §6.2`; gỡ "batch submission" khỏi danh sách khác biệt G3; và **sửa câu ở bài 9 rủi ro 1** nói rằng bộ nhân Larsen là đường thoát nếu nhãn residue sụp — **nó không phải** (mục 4.2).
4. **Viết lại kết quả âm "read 10 → 200" thành một phát hiện có trích dẫn**, dẫn DiMSum (`a_r` không phụ thuộc số đọc) và Enrich2 (C2 domain xấu đi khi lọc theo count).
5. **Ghi phép tính Spearman–Brown vào file audit** như lý lẽ cho D-025 mục 3 (đã chốt), kèm ghi chú rằng lợi ích là **+27% trên bộ quét nhưng chỉ ≈ +4,5% trên bộ bão hòa**.
6. **Chốt bộ thước đo ba tầng và cam kết trước về ablation không phân biệt được** (mục 5.1 ý 2 và 4).
7. **Dọn ba mục nợ kỹ thuật rẻ nhất:** mask `*`, chạy lại `prepare_protein_clusters.py`, và ghi `--min-seq-id` + `-c` vào Methods.

**Nhóm B — cần tải, vẫn không cần GPU.**

8. **Tải `annotations/transfac_tiles.csv.gz`** (5,77 MB) từ GitHub tag `v1.0`, kèm `data/raw/SOURCE.md` giữ thông báo MIT + DOI Zenodo. Rồi **đếm số dòng có `degron_score`** để có con số tile đúng thay cho 58.781 đang mâu thuẫn.
9. **Đo chồng lặp ở mức trình tự** (chưa làm): bao nhiêu trong số tile 30-mer **chứa trọn** một peptide 23-mer của I28. Đây là con số thay cho 97,4% theo-tên-gene, và là con số sẽ bị hỏi khi bảo vệ.
10. **Phân rã nhiễu trên bộ nhân** bằng cột `degron_std`, theo đúng cách đã làm cho bộ GPS — phép kiểm tính vững trên một bộ dữ liệu thứ hai.
11. **Tải và chạy lại `peptide_model_epoch50.pt` của Degformer dưới split cov80** và thước đo mức residue. Thí nghiệm giá-trị-trên-giờ cao nhất đang có. Xử lý repo như **dữ liệu không tin cậy** (pickle, thư mục riêng, `python3 -I`).
12. **Tính lại PAP trên ≈ 50.136 tile không chồng** để có con số 0,79 "sạch", và **so QCDPred với thư viện nhân** (chưa tìm thấy ai làm).

**Nhóm C — cần huấn luyện.**

13. **Ablation 3 nhánh MIL-vs-đầu-theo-vị-trí**, cùng cửa sổ, cùng Huber có trọng số theo độ chính xác, chấm trên cả chỉ số túi và chỉ số thể hiện có sai số ±1.
14. **Ablation ô chéo cho cổng phơi lộ ở mức tile trên bộ nhân Larsen** (pooling học được ± rASA × cổng tường minh ± rASA).
15. **Kiểm độ ổn định trọng số theo vị trí qua seed và bootstrap**, theo khuôn LeBlanc et al., để trả lời rủi ro "thành phần > vị trí".
16. (Nếu còn thời gian) **đầu heteroscedastic NLL** như mục tiêu với tới, kèm đánh giá hiệu chuẩn.

**Cần Trọng quyết — thuộc phần C của DECISIONS.md, không được coi là đã chốt:**

- **[C-7]** chuyển chỗ đặt đóng góp sang nhiệm vụ + benchmark (và nên hỏi GVHD cùng C-5, vì GVHD từng nói kỳ vọng "kiến trúc chưa ai dùng").
- **[C-8]** hạ cổng phơi lộ xuống cơ chế chuyển giao — báo cáo này **thêm bằng chứng ủng hộ** nó (rASA chỉ có phương sai trên bộ nhân, không trên nhãn chính) nhưng vẫn là đề xuất chờ xác nhận.
- **[C-9]** đổi thước đo chính của ma trận sang AUROC mức ô.
- **Mới, cần quyết:** có **tải và dùng bộ nhân Larsen** làm test chuyển ngăn mức tile hay không (chi phí 5,77 MB + vài giờ, lợi ích là một mốc PAP 0,79 do tác giả đo và một nơi kiểm cổng), và có **gửi email xin xác nhận giấy phép MIT** hay không (mục 2.2). Cả hai là `[đề xuất]`, chưa phải quyết định.
- **Mới, cần quyết:** có **nhận Degformer làm baseline chính thức trong luận văn** hay không. Nếu có thì phải trích rõ là "tự báo, chưa công bố, split ngẫu nhiên", và con số 0,9162/0,9420 phải được gọi là **Pearson**, không phải Spearman.

---

## 8. Chỗ còn chưa kiểm được

Phần này cố ý liệt kê mọi thứ **không** được dùng để lập luận trong luận văn mà chưa kiểm thêm.

- **Wang & Zheng (*Nat Chem Biol* 2025-11) chỉ đọc được tóm tắt.** Paywall, 303 về `idp.nature.com`, không preprint, không PMC. **Không biết** thân bài có định lượng *bao nhiêu phần* degron là không-tuyến-tính, có nêu một độ dài cửa sổ cụ thể là không đủ, hay có phê bình trực tiếp phương pháp sàng tile (kiểu Larsen/Voutsinos). Mọi phát biểu vượt quá hai câu tóm tắt đã trích là **chưa xác minh**. Cần lấy PDF qua thư viện trường.
- **Mendeley Data chưa kiểm.** Endpoint thử (`https://data.mendeley.com/public-api/datasets?query=…`) trả **404 "Cannot GET /public-api/datasets"** — sai endpoint, nên Mendeley là **chưa xác minh**, **không phải** đã xác nhận không có. OSF, ArrayExpress và PRIDE cũng chưa truy vấn trực tiếp (bằng chứng gián tiếp: cả Data Availability của bài và README đều chỉ nêu ERDA, SRA, GitHub, Zenodo).
- **Chồng lặp ở mức trình tự chưa đo.** Con số 97,4% là **giao theo ký hiệu gene**, tức **chặn trên**. Việc đếm bao nhiêu tile 30-mer chứa trọn một peptide 23-mer của I28 **chưa làm** (mục 7 ý 9).
- **Toàn văn Larsen chưa đọc hết.** Toàn văn dài ≈ 160.600 ký tự, lần fetch phủ 100.000 đầu; một dòng giấy phép hay dữ liệu trong 60.600 ký tự cuối (Methods muộn / chú thích phụ lục) **chưa đọc**. Công thức PSI là **ảnh nhúng** trong HTML nên **chưa đọc được dạng đại số**. **Fig. S9** chưa mở nên không biết có bao nhiêu biến thể kiểm chứng. `SupplementalDataFile.xlsx` **không mở** nên không biết danh sách sheet. Mâu thuẫn 0,95 / 0,92 giữa thân bài và chú thích Fig. 5A **chưa giải quyết được** từ bản HTML.
- **Tập blind của Degformer vắng mặt**, cùng script chia và script đánh giá — nên **con số headline của nó không tái lập được từ repo**. Năm file PNG trong `media/` chưa xem, nên số in bên trong hình là **chưa biết**. Cột cụ thể nào của phụ lục Zhang trở thành `controlPSI` **không có tài liệu ở đâu**.
- **Nội dung ZIP Zenodo chưa xác minh** (có byte-identical với tag `v1.0` của GitHub hay không), vì zenodo.org bị **403** từ mạng này; trang chỉ đọc được qua proxy fetch. Chưa thử Zenodo từ mạng khác.
- **Clause §2/§3 của CC BY-NC-ND 4.0 chưa đọc từ legal code** trong phiên này; số thứ tự clause là từ hiểu biết sẵn, phải kiểm lại trước khi đưa vào luận văn. Mục FAQ sát nhất ("If I use a CC-licensed database to produce a new database, does the ShareAlike/NoDerivatives clause apply?") **không xuất hiện** trong phần trang đọc được — đây là một khoảng trống thật. Văn bản Luật Sở hữu trí tuệ Việt Nam **chưa đối chiếu nguồn gốc**.
- **Enrich2 và Rosace**: công thức chính xác của Enrich2 nay đã đọc được từ PMC (mục 5.2), nhưng câu về WLS cải thiện độ tương đồng replicate vẫn là **tóm tắt tìm kiếm**; giá trị số của `m_r`/`a_r` trong DiMSum nằm ở Table 2/Additional file 1 **chưa trích**.
- **Chưa đọc:** *Nat Commun* 2026-05-15 "coarse-to-fine PTM" (nơi khả dĩ nhất có tiền lệ bag→residue); PTM-Mamba; giao diện module của MAVISp; độ mịn đầu ra của **DegPred** (Springer vòng lặp xác thực, PMC trả reCAPTCHA) — đây là công cụ duy nhất chưa xác minh được mức xuất ra, **phải giải quyết trước khi viết phần văn liệu**; và bản *Science Advances* của Voutsinos 2026 (science.org trả 403 từ mạng này).
- **Chưa kiểm server đang chạy** của DEGRONOPEDIA/MetaDegron/DegronMD để xác nhận không có API không tài liệu hoá. Khẳng định "không có API" hiện chỉ từ tài liệu và bài báo — **đáng 15 phút kiểm** trước khi đề cương khẳng định.
- **Trạng thái công bố của Larsen 2025 là một "chưa tìm thấy", không phải một "không có".** Chưa tra Google Scholar hay giao diện PubMed riêng, nên một công bố rất mới (vài tuần) **có thể bị bỏ sót**; phải tra lại trước khi nộp.

---

## Nguồn

**Bộ nhân Larsen và dữ liệu liên quan**
- Larsen FB, Voutsinos V, Jonsson N, Johansson KE, Ethelberg FD, Lindorff-Larsen K, Hartmann-Petersen R. "Comprehensive degron mapping in human transcription factors". bioRxiv, DOI [10.1101/2025.05.16.654404](https://doi.org/10.1101/2025.05.16.654404) · [toàn văn v1](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.full) · [phụ lục](https://www.biorxiv.org/content/10.1101/2025.05.16.654404v1.supplementary-material)
- Repo MIT: [KULL-Centre/_2025_Larsen_degron_transcriptionfactors](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors) · [LICENSE](https://raw.githubusercontent.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors/main/LICENSE) · [GitHub API](https://api.github.com/repos/KULL-Centre/_2025_Larsen_degron_transcriptionfactors)
- Zenodo DOI [10.5281/zenodo.20490355](https://doi.org/10.5281/zenodo.20490355) (concept DOI 10.5281/zenodo.20490354) · [DataCite](https://api.datacite.org/dois/10.5281/zenodo.20490355)
- ERDA DOI 10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943 · [archive](https://erda.ku.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-archive.html) · [published-files.json](https://www.erda.dk/archives/a3c1d52583efe41f448642006ceb8f6f/published-files.json) · [DataCite](https://api.datacite.org/dois/10.17894/ucph.e6ff0116-3fb4-4f71-8a7f-2ab162b6a943)
- NCBI SRA BioProject [PRJNA1276444](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1276444)
- Voutsinos V et al. "A near-complete map of human cytosolic degrons and their relevance for disease". *Science Advances* 12(6), 2026, DOI [10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483) · preprint [10.1101/2025.05.10.653233](https://doi.org/10.1101/2025.05.10.653233) · [repo PAP](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol)
- [Crossref](https://api.crossref.org/works/10.1101/2025.05.16.654404) · [bioRxiv details API](https://api.biorxiv.org/details/biorxiv/10.1101/2025.05.16.654404) · [bioRxiv pubs API](https://api.biorxiv.org/pubs/biorxiv/10.1101/2025.05.16.654404) · [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ) · [CC FAQ](https://creativecommons.org/faq/) · [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)

**Tiền lệ degron và mô hình đối thủ**
- Degformer: [Alpine2048/Degformer](https://github.com/Alpine2048/Degformer) · [train_v2.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/train_v2.py) · [saturation_mut_heatmap.py](https://raw.githubusercontent.com/Alpine2048/Degformer/HEAD/saturation_mut_heatmap.py) · [GitHub API](https://api.github.com/repos/Alpine2048/Degformer)
- Zhang Y et al. (Elledge lab) 2023, *Mol Cell*, DOI [10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022)
- Zhang Y, Mena J, Timms R, Koren I, Elledge SJ. "Degrons: defining the rules of protein degradation". *Nat Rev Mol Cell Biol* 2025, DOI [10.1038/s41580-025-00870-z](https://doi.org/10.1038/s41580-025-00870-z)
- Wang B, Zheng N. "Degrons and degradation signals beyond short linear motifs". *Nat Chem Biol* 22(3):355–368, DOI [10.1038/s41589-025-02056-2](https://doi.org/10.1038/s41589-025-02056-2) · [Europe PMC](https://europepmc.org/article/MED/41238838)
- [DEGRONOPEDIA documentation](https://degronopedia.com/degronopedia/documentation) · [MetaDegron, *Brief Bioinform* 2024](https://academic.oup.com/bib/article/25/6/bbae519/7828723) · [DegronMD, *MBE* 2023](https://academic.oup.com/mbe/article/40/12/msad253/7441958) · [QCDPred, *JMB*](https://www.sciencedirect.com/science/article/pii/S0022283622005411) · [degronome paper](https://www.biorxiv.org/content/10.1101/2022.04.06.487275v2.full) · [yGPS-P, *Biomolecules* 13:987](https://doi.org/10.3390/biom13060987) · [Biol Direct 2026 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13455158/)
- LeBlanc CJ et al. *Cell Systems* 17(9):101701, DOI [10.1016/j.cels.2026.101701](https://doi.org/10.1016/j.cels.2026.101701) · [PMC13596073](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596073/)
- Yang W, Zhang H, Qiu W, Xiao X, Lin W. "Edge-aware GAT-based protein binding sites prediction". *PLOS Comput Biol* 22(8):e1014552, DOI [10.1371/journal.pcbi.1014552](https://doi.org/10.1371/journal.pcbi.1014552) · [PMC13460574](https://pmc.ncbi.nlm.nih.gov/articles/PMC13460574/)
- Hoang M, Singh M. "Locality-aware pooling enhances protein language model performance". *Bioinformatics* 41(Suppl 1):i217, DOI [10.1093/bioinformatics/btaf178](https://doi.org/10.1093/bioinformatics/btaf178) · [PMC12261463](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261463/)
- Schulze & Lindorff-Larsen, *eLife* 2026, DOI [10.7554/eLife.103721](https://doi.org/10.7554/eLife.103721) · MAVISp, *Protein Sci* 2026, DOI [10.1002/pro.70548](https://doi.org/10.1002/pro.70548)

**Mô hình sai số, nhãn nhiễu và thống kê**
- Faure AJ, Schmiedel JM, Baeza-Centurion P, Lehner B. "DiMSum". *Genome Biology* 2020;21:207, DOI [10.1186/s13059-020-02091-3](https://doi.org/10.1186/s13059-020-02091-3) · [PMC7429474](https://pmc.ncbi.nlm.nih.gov/articles/PMC7429474/)
- Rubin AF et al. "A statistical framework for analyzing deep mutational scanning data" (Enrich2). *Genome Biology* 2017;18:150, DOI [10.1186/s13059-017-1272-5](https://doi.org/10.1186/s13059-017-1272-5) · [PMC5547491](https://pmc.ncbi.nlm.nih.gov/articles/PMC5547491/)
- Rao J et al. "Rosace". *Genome Biology* 2024;25:138, DOI [10.1186/s13059-024-03279-7](https://doi.org/10.1186/s13059-024-03279-7) · [PMC11127319](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127319/)
- Livesey BJ, Marsh JA. *Mol Syst Biol* 2020;16(7):e9380, DOI [10.15252/msb.20199380](https://doi.org/10.15252/msb.20199380) · [PMC7336272](https://pmc.ncbi.nlm.nih.gov/articles/PMC7336272/); bản cập nhật 2023;19(8):e11474, DOI [10.15252/msb.202211474](https://doi.org/10.15252/msb.202211474) · [PMC10407742](https://pmc.ncbi.nlm.nih.gov/articles/PMC10407742/)
- Saravanan V, Berman GJ, Sober SJ. "Application of the hierarchical bootstrap to multi-level data in neuroscience". [bioRxiv 819334](https://www.biorxiv.org/content/10.1101/819334v2.full) · [arXiv:2007.07797](https://arxiv.org/pdf/2007.07797)
- [ProteinGym](https://www.biorxiv.org/content/10.1101/2023.12.07.570727v1.full) · [Kermut, arXiv:2407.00002](https://arxiv.org/pdf/2407.00002) · [Kendall & Gal, arXiv:1703.04977](https://arxiv.org/abs/1703.04977) · [RECOVER, arXiv:2202.04202](https://arxiv.org/pdf/2202.04202) · [Ghosh et al., arXiv:1712.09482](https://arxiv.org/pdf/1712.09482) · [Normalized loss functions, arXiv:2006.13554](https://arxiv.org/pdf/2006.13554)
- MIL: [Ilse, Tomczak & Welling, PMLR v80](https://proceedings.mlr.press/v80/ilse18a/ilse18a.pdf) · [Rethinking MIL for WSI, arXiv:2307.02249](https://arxiv.org/html/2307.02249v2) · [ItS2CLR, CVPR 2023](https://openaccess.thecvf.com/content/CVPR2023/papers/Liu_Multiple_Instance_Learning_via_Iterative_Self-Paced_Supervised_Contrastive_Learning_CVPR_2023_paper.pdf) · [soft bags, CVPR 2015](http://www.svcl.ucsd.edu/publications/conference/2015/softbag/softbag_final.pdf) · [max vs noisy-OR, arXiv:1804.01146](https://arxiv.org/pdf/1804.01146)
- Thước đo và split: [J Cheminform 2024, binding-site benchmarking](https://link.springer.com/article/10.1186/s13321-024-00923-z) · [FunFOLDQA / BDT, PMC3364224](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3364224/) · [CAID2](https://www.sciencedirect.com/science/article/pii/S2001037024004318) · [AMPBench-MT, arXiv:2607.25518](https://arxiv.org/pdf/2607.25518) · [PepBenchmark, arXiv:2604.10531](https://arxiv.org/pdf/2604.10531) · [Fast-Part](https://www.biorxiv.org/content/10.1101/2024.11.13.623463v1.full.pdf) · [MaveDB 2024](https://link.springer.com/article/10.1186/s13059-025-03476-y) · [arXiv:2609.06330 (ít cụm)](https://arxiv.org/pdf/2609.06330)

**Nguồn nội bộ của repo** (số `[đo]` trích từ đây): [full-data-audit](../full-data-audit/README.md) · [pap-baseline](../pap-baseline/README.md) · [architecture-check](../architecture-check/README.md) · [prior-art-exposure-gate](../architecture-check/prior-art-exposure-gate.md) · [voutsinos-2026-audit](../voutsinos-2026-audit/README.md) · bài 9 — Rủi ro · bài 7 — Đánh giá · bài 10 — Dữ liệu thật · DECISIONS.md
