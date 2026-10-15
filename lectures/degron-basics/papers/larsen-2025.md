[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# Larsen 2025 — degron của yếu tố phiên mã

| | |
|---|---|
| **Nơi công bố** | bioRxiv, 05/2025 |
| **DOI** | <https://doi.org/10.1101/2025.05.16.654404> |
| **Giấy phép** | **Bài báo: CC BY-NC-ND** → không tạo bản phái sinh, **không sao chép hình**. **Dữ liệu: MIT** qua repo GitHub của nhóm (xác minh 15/10, xem mục giấy phép dưới) |
| **Mức kiểm** | **[ĐÃ ĐỌC]** toàn văn — đây là "cổng chặn 1" của đề tài. **[TỰ KIỂM]** giấy phép, nơi lưu và chồng lặp trình tự (15/10) |

---

## Vì sao phải đọc bài này trước mọi thứ khác

Vì nó là bài **gần đề tài nhất**. Nếu nó đã làm đúng việc đề tài định làm thì đề tài hết chỗ. Đọc toàn văn là một trong ba **cổng chặn** phải qua trước khi chốt đề tài ([topic-decision.md mục 7](../../../topics/degron-footprint/research/topic-decision.md)).

## Kết quả: cổng chặn **ĐÃ QUA, theo hướng thuận**

Bài này **không** làm bốn việc mà đề tài định làm:

| Việc | Larsen 2025 |
|---|---|
| Mô hình hóa đặc hiệu E3 | **không** |
| Đề xuất kiến trúc mới | **không** |
| Dùng nhãn E3 hay nhãn CRISPR | **không** |
| Có phần giải thích mô hình | **không** |

Họ dùng PAP cùng ESM-1b chỉ để **so sánh biến thể CRX**. Phần nhắc CRL4-DCAF12 và FEM1b nằm ở mục Thảo luận, là **suy đoán theo y văn**, không phải kết quả.

→ **Trục của đề tài còn trống.**

## Nhưng bài này thu hẹp tính mới ở hai chỗ

Đây là phần quan trọng, và nó bắt buộc:

**1. Họ đã dùng cấu trúc.** Đã tính **rASA và pLDDT** từ AlphaFold2 kèm DSSP. Điểm degron so với rASA \|r\| = **0,41**, so pLDDT \|r\| = **0,36** trên toàn thư viện; 32% degron có rASA > 0,7 và 40% có pLDDT < 70.

**1b. Họ đã tìm ra hiện tượng ΔPAP đổi dấu** (bổ sung 14/10/2026, [tra y văn](../../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md)). Trên CRX, tách theo vùng: ΔPAP Pearson **0,54** trong vùng vô định hình so với **−0,19** trong homeodomain đã gấp (ESM-1b đi ngược: 0,31 và 0,52). Nên phép đo của repo ngày 14/10 trên 6 protein MaveDB là **xác nhận lại ở quy mô lớn hơn**, không phải phát hiện. Nhãn của họ là transactivation, không phải độ dồi dào, và chính họ ghi là khó tách hai thứ.
→ **"Dùng cấu trúc" không còn là phần mới của đề tài.**

**2. Họ đã làm bản đồ thay thế *in silico*.** Đã tính ΔPAP cho **mọi đột biến điểm** trong một vùng của HSF1.
→ **"Giải thích biến thể bằng bản đồ thay thế" không còn là phần mới.**

Hệ quả cho đề tài: chỗ mới phải nằm ở **nơi đặt** cổng phơi lộ (tại bước gộp, không phải đầu vào) và ở **chỗ ghép** các cơ chế — xem [bài 6 mục 4](../06-proposed-solution.md).

## Một bộ dữ liệu bài này mở ra — đã kiểm giấy phép và nội dung, 15/10

Thư viện **nhân** (nuclear), khác khoang tế bào so với bộ bào tương của [Voutsinos 2026](voutsinos-2026.md):

| | Số lượng |
|---|---:|
| Đoạn có điểm | **58.781** ⚠ xem ghi chú dưới |
| Yếu tố phiên mã | **1.626** |
| Đoạn chồng lấn với thư viện bào tương | 8.645 / 234 protein |

> ⚠ **Con số 58.781 không nhất quán trong chính bài báo.** Các chỗ khác in **62.992 / 63.230 / 63.011 / 58.992**, và 58.781 có lúc gọi là "tiles", lúc là "scores mapped to 58.992 tiles" `[đọc]`. **Đừng trích 58.781 như một con số dứt khoát** — phải đếm số dòng trong CSV rồi ghi chú chỗ mâu thuẫn.

### ✅ Giấy phép: cổng chặn đã qua, và đường tải sạch hơn mong đợi

Điểm mức tile **không** nằm sau giấy phép CC BY-NC-ND của bài báo. Nó nằm trong repo GitHub của chính nhóm, dưới **giấy phép MIT** — cùng số đo, giấy phép khác hẳn `[đọc]`:

| Nơi lưu | Nội dung | Giấy phép | Từ máy này |
|---|---|---|---|
| **GitHub** `KULL-Centre/_2025_Larsen_degron_transcriptionfactors` | `annotations/transfac_tiles.csv.gz` **5,77 MB** (đã chú giải sẵn **PAP, ADPred, rASA, pLDDT**), `transfac_proteins.csv.gz`, `score/degrons.csv.gz` | **MIT** | **200**, đọc được |
| **Zenodo** 10.5281/zenodo.20490355 | ảnh lưu trữ repo, ZIP 87,1 MB, tag `v1.0` | **MIT** | **403** — dùng GitHub, trích DOI Zenodo |
| **ERDA** (ĐH Copenhagen) | FASTQ + FACS thô, **120,79 GB** | **KHÔNG CÓ giấy phép nào** | 200 — **không cần, và nên tránh** |
| **SRA** `PRJNA1276444` | 136 experiment | mặc định NCBI | 200 |
| Phụ lục bioRxiv (`media-2.xlsx`) | bài gọi đây là bản phát hành chính thức | **CC BY-NC-ND** | 200 |

**Không có deposit GEO/figshare/ArrayExpress** — `elink` từ BioProject sang GEO trả linkset rỗng, tìm GEO theo tác giả trả 0. **Đừng đi tìm mã GSE nữa** `[đọc]`.

**Chỗ mơ hồ duy nhất còn lại:** MIT nominally là giấy phép *phần mềm*, và Zenodo đăng ký loại "Software". Lập luận phản lại mạnh hơn: file `LICENSE` ở gốc repo **không có ngoại lệ**, và README gọi hai file CSV là *"the main resulting data"*. Trên cân, MIT đọc ra là phủ toàn repo `[phân tích]` — nhưng **một email xác nhận xoá sạch chỗ này**, gửi `rhpetersen@bio.ku.dk` (cc `lindorff@bio.ku.dk`) `[đề xuất]`.

**An toàn / rủi ro, xét trên thực tế repo đang private** ([D-004](../../../DECISIONS.md#d-004)) `[phân tích]`, **không phải tư vấn pháp lý**:

- **An toàn:** tải CSV từ GitHub, huấn luyện trên điểm, báo chỉ số tổng hợp, trích DOI. Nếu phát hành lại bảng đã xử lý thì kèm thông báo MIT (`data/raw/SOURCE.md`) — nhưng quy ước repo đã chặn `data/` khỏi git nên câu hỏi chưa phát sinh.
- **Rủi ro, nên tránh:** phát hành lại **chính `SupplementalDataFile.xlsx` của bioRxiv** (mang CC BY-NC-ND); **sao panel hình** rồi cắt/đổi màu/dịch chú thích — đó là bản phái sinh mà ND cấm chia sẻ, nên cách an toàn là **tự vẽ lại từ dữ liệu**; và dùng archive ERDA cho bất cứ việc gì ngoài đọc.

### ⚠ Nội dung: nó **không** phải thứ repo từng kỳ vọng

**Không phải GPS.** Đây là **sort-seq abundance reporter**: tile gắn đầu C của GFP (GFP mang NLS đầu N), mCherry chuẩn hoá qua IRES, landing pad Bxb1 trong HEK293T, sort vào **4 cổng 25%**. Tile **30 acid amin, bước 15**. Điểm vẫn gọi là PSI nhưng **đảo chiều** so với PSI của GPS và được chuẩn hoá lại theo replicate — còn bảng GPS mà đề tài dùng có **6 bin**. Ghép nhãn phải **chuẩn hoá theo quantile**, không phải map tuyến tính `[đọc]`.

**Nhãn chỉ ở mức tile, chỉ trên trình tự hoang dã.** Không bão hòa, không alanine scan, không deletion series hệ thống. Đột biến thực nghiệm chỉ vài ca lẻ (ASCL1 Δ23–40, HSF1 Δ198–217, ZNF140 H323Y…). **Mọi** phân tích mức residue trong bài là *in silico* (ΔPAP cho HSF1, ESM-1b cho CRX) `[đọc]`.

| Điều đề tài từng kỳ vọng | Thực tế |
|---|---|
| Nguồn nhãn mức residue bổ sung | ❌ **không một nhãn mức residue nào**; độ mịn tốt nhất **15 residue** |
| Test ngoại độc lập về trình tự | ❌ **1.583/1.626 (97,4%) TF đã có trong peptidome GPS** của Zhang 2023 `[đo]` |
| Cứu rủi ro lực thống kê | ❌ không nâng n của bậc 2 hay 3, không cải thiện Jaccard 0,4965 |
| Mốc mức residue để so | ❌ bài **không có một con số mức residue nào** |

**Reproducibility của nó rất tốt — nhưng không so sánh được với con số của đề tài.** Bài báo: *"average PSI Pearson correlation of **0.97** between all replicate pairs (range 0.91–0.99)"*, 3 sinh học × 2 FACS, lọc **≥100 read**, và **SD từng tile được công bố** `[đọc]`. Nhưng đó là tương quan **mức tile trên toàn dải động**, **không** so được với Jaccard **0,4965** mức residue của đề tài — khác mẫu số hoàn toàn. Bài **không báo một phép đo lặp lại mức residue nào**.

### Vậy nó vẫn giúp được gì

Ba giá trị thật `[phân tích]`:

1. **Test chuyển assay / chuyển ngăn ở mức tile, rất rẻ** — chú giải PAP/ADPred/rASA/pLDDT **đã tính sẵn**, nên không cần chạy AlphaFold hay DSSP. Mốc phải vượt: **PAP Pearson 0,79 / Spearman 0,80** trên tile TF, do chính tác giả đo (so với 0,87 trên holdout bào tương của PAP) — một **ước lượng chi phí chuyển ngăn** mà đề tài có thể trích. Phải gọi đúng tên là "test chuyển assay/chuyển ngăn", **không** phải "test trình tự chưa thấy".
2. **Chỗ duy nhất rASA/pLDDT *có phương sai*** — và đây là phát hiện giá trị nhất. Cổng phơi lộ không huấn luyện được trên nhiệm vụ chính vì peptide 28-mer gắn GFP đều phơi lộ như nhau ([C-8](../../../DECISIONS.md)). Bộ nhân thì khác: **32%** tile degron có rASA > 0,7, **40%** có pLDDT < 70, tương quan 0,41 / 0,36 `[nguồn]`. Đó biến "cơ chế chuyển giao" từ một lời khẳng định thành một con số đo được, ở mức tile.
3. **Hai phép so chưa tìm thấy ai làm, đều rẻ:** QCDPred ↔ thư viện nhân (QCDPred **không xuất hiện** trong bài Larsen), và PAP tính lại trên **≈ 50.136 tile không chồng** để có con số 0,79 "sạch".

**Rủi ro rò rỉ phải nêu:** 230/242 protein dùng chung với thư viện bào tương nằm trong **tập train của PAP** `[đo]`. Nhưng rò rỉ thực tế cho đề tài **thấp hơn** con số 97,4% gợi ý, vì nhãn footprint mức residue chỉ nằm trên bộ quét và bộ bão hòa — ở đó chỉ **31,2%** TF có mặt, với 688 peptide WT. Và kiểm theo tên: **ASCL1, FOXC1, TP73, KMT2A** có trong bộ quét; **HSF1, CRX, ZNF140, YBX1, NFE2L1 không có** — phần lớn ví dụ chính của bài Larsen **không** trùng nhãn footprint của đề tài `[đo]`.

> **Và nó vẫn là tiền ấn phẩm chưa bình duyệt sau 17 tháng** (Crossref `relation: {}`, bioRxiv `published: "NA"`, kiểm 15/10). Phải trích là preprint. Bài **chị em** về bào tương thì **đã công bố**: Voutsinos et al., *Science Advances* 12(6), 06/02/2026, giấy phép **CC BY-NC** (không ND) `[đọc]`.

Chi tiết đầy đủ: [báo cáo 15/10](../../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/README.md) mục 2–4.

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
