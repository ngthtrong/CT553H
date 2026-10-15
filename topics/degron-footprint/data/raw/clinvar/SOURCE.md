# Xuất xứ — ClinVar `variant_summary.txt.gz`

> Sổ xuất xứ của riêng bộ này. Bản tổng hợp ở [../../README.md](../../README.md).
> File này **được lên git** (ngoại lệ `!**/data/**/SOURCE.md`, [D-030](../../../../../DECISIONS.md#d-030) mục 3).

## 1. Nguồn gốc

| Mục | Giá trị |
|---|---|
| Nguồn | NCBI **ClinVar**, báo cáo dạng bảng |
| URL | `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz` |
| Trang chủ | https://www.ncbi.nlm.nih.gov/clinvar/ |
| Phiên bản | **Không có số phiên bản.** File sinh **mỗi tuần**, ghi đè. `Last-Modified` của bản đã tải: **12/10/2026 22:21:13 GMT** |
| Bản lưu trữ ghim được | `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/` — lưu theo tháng, thứ Năm đầu tháng. **Nếu cần tái lập chính xác thì phải dùng bản archive**, xem mục 5 |
| Ngày tải | **15/10/2026** |
| Kích thước | 455.785.525 byte |
| SHA-256 | `a5198a11b0e871c324fd5e800082fb1d4418301323b806cf9c98ee2421828218` |
| Lệnh tải | `curl -sS -o variant_summary.txt.gz "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"` |
| Mạng | Tải được từ WSL cục bộ. ⚠ `ftp.ncbi.nlm.nih.gov` **cần thêm vào Allowed domains** ở môi trường cloud ([resources §5](../../../../../resources/README.md)) |

## 2. Giấy phép và điều khoản — nguyên văn

ClinVar **không phát hành kèm một giấy phép kiểu CC**. Hai đoạn dưới đây là **nguyên văn**
trích từ https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/ (đọc ngày 15/10/2026),
mục *"Disclaimer and data use policy"*:

> The information on this website is not intended for direct diagnostic use or medical
> decision-making without review by a genetics professional. Individuals should not change
> their health behavior solely on the basis of information contained on this website. NIH
> does not independently verify the submitted information.

> If you distribute or copy data from ClinVar, we ask that you provide attribution to
> ClinVar as a data source in publications and websites. You can cite of one the ClinVar
> publications (e.g. PMID: 29165669).

**Hệ quả cho đề tài — hai điều, không được bỏ:**

1. **Ghi công bắt buộc** khi dùng lại: nêu ClinVar là nguồn dữ liệu trong luận văn **và**
   trên trang web/ứng dụng, kèm trích dẫn (PMID 29165669 = Landrum et al., *Nucleic Acids
   Res* 2018).
2. **Câu phủ nhận chẩn đoán phải đi theo đầu ra.** Chính ClinVar nói dữ liệu của họ *"not
   intended for direct diagnostic use or medical decision-making"*. Mọi chỗ ứng dụng của đề
   tài hiển thị chú giải ClinVar phải mang câu phủ nhận tương đương. Điều này **trùng** với
   giới hạn mà [contribution-assessment §4.2](../../../research/contribution-assessment-2026-10-15.md)
   đã chốt: công cụ của đề tài là **công cụ sàng lọc ưu tiên**, không phải công cụ quyết định.

⚠ **Chưa xác minh:** chưa tìm được một phát biểu rõ ràng của NCBI rằng bản thân bộ
`variant_summary.txt.gz` thuộc phạm vi công cộng. Lời trên là *"we ask that you provide
attribution"* — một **yêu cầu ghi công**, không phải một giấy phép cấp quyền tường minh.
Trong phạm vi luận văn (dùng lại để phân tích, có ghi công) thì không thấy trở ngại; nếu
sau này muốn **phân phối lại chính file dữ liệu** thì phải hỏi lại.

## 3. Nội dung và định dạng

Bảng phân cách tab, dòng đầu là header bắt đầu bằng `#`. Theo
[README của ClinVar FTP](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/README.txt) (bản
13/01/2026, mục *2. variant_summary.txt*):

> A tab-delimited report based on each variant at a location on the genome for which data
> have been submitted to ClinVar. The data for the variant are reported for each assembly,
> so most variants have a line for GRCh37 (hg19) and another line for GRCh38 (hg38).

Các cột đề tài dùng:

| Cột | Dùng để |
|---|---|
| `VariationID` | **Bỏ trùng.** Mỗi biến thể có một dòng cho mỗi assembly ⇒ không bỏ trùng là đếm đôi |
| `Name` | Lấy thay đổi mức protein, dạng `NM_000546.6(TP53):c.818G>A (p.Arg273His)` |
| `GeneSymbol` | Ánh xạ sang accession UniProt |
| `ClinicalSignificance` | Phân loại **dòng mầm** (germline). Nhiều nhãn trong một ô, phân cách bằng dấu `;` |
| `Oncogenicity` | Phân loại **soma**, cột riêng. ⚠ **Rất thưa**: chỉ ~800/2,56 triệu biến thể missense có giá trị |

## 4. Đã dùng vào việc gì

| Script | Đầu ra | Việc |
|---|---|---|
| [`research/variant-coverage-2026-10-15/coverage.py`](../../../research/variant-coverage-2026-10-15/coverage.py) | `coverage.json`, `scan-hits.json`, `driver-variants.json` | Độ phủ biến thể trên bảy tầng thư viện peptide |
| [`research/variant-coverage-2026-10-15/enrichment.py`](../../../research/variant-coverage-2026-10-15/enrichment.py) | `enrichment.json` | Tỉ số chênh gây bệnh/lành tính trong vùng degron, Mantel–Haenszel phân tầng theo protein và theo cụm cov80 |

Phép kiểm chứng toạ độ bắt buộc trong cả hai script: acid amin hoang dã mà ClinVar ghi
phải **khớp** acid amin tại đúng vị trí đó trong trình tự UniProt, vì toạ độ ClinVar theo
transcript RefSeq **không** đương nhiên bằng toạ độ UniProt canonical.
Tỉ lệ khớp đo được: **2.349.511/2.526.412 = 93,0%**; **176.901 (7,0%) bị loại** vì lệch.

## 5. Dựng lại từ đầu

```bash
mkdir -p topics/degron-footprint/data/raw/clinvar
curl -sS -o topics/degron-footprint/data/raw/clinvar/variant_summary.txt.gz \
  "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
sha256sum topics/degron-footprint/data/raw/clinvar/variant_summary.txt.gz
```

⚠ **File này ghi đè mỗi tuần, nên SHA-256 ở mục 1 sẽ KHÔNG khớp lại.** Muốn tái lập đúng
con số của phiên 15/10/2026 thì lấy bản archive gần nhất trước ngày đó:

```bash
curl -sS -O "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/variant_summary_2026-10.txt.gz"
```

và ghi rõ trong Methods rằng số liệu dựa trên bản archive tháng nào — **không** nói "ClinVar"
mà không nêu ngày.

## 6. Nhật ký

| Ngày | Việc |
|---|---|
| 15/10/2026 | Tải lần đầu (455.785.525 byte). Chạy `coverage.py` và `enrichment.py`. Ghi sổ xuất xứ này |
