# Koren et al. 2018 — thử truy cập supplementary, 22/10/2026

Thư mục này **không chứa dữ liệu nghiên cứu**. Nó chỉ giữ bằng chứng của một lần thử truy cập thất bại, theo đúng cách [MetaDegron 21/10](../../../research/metadegron-analysis-2026-10-21/README.md) đã làm với các URL XLSX trả trang challenge.

## Nguồn nhắm tới

Koren, I.; Timms, R. T.; Kula, T.; Xu, Q.; Li, M. Z.; Elledge, S. J. (2018). *The Eukaryotic Proteome Is Shaped by E3 Ubiquitin Ligases Targeting C-Terminal Degrons*. **Cell** 173(7), 1622–1635.e14. DOI [10.1016/j.cell.2018.04.028](https://doi.org/10.1016/j.cell.2018.04.028). PMID 29779948 · PMC6003881.

Quan tâm tới **Table S4 — saturation mutagenesis data** (chấm điểm bằng PSI, cùng hệ GPS với nhãn chính của đề tài) và **Table S7** (GPS-peptidome 23-mer đầu C, điểm ổn định từng peptide). Lý do chọn: [dataset-search §2](../../../research/next-steps-plan-2026-10-22/dataset-search.md).

## Trạng thái truy cập `[ĐO]` 22/10/2026

| Mục | Kết quả |
|---|---|
| Trang bài trên cell.com | HTTP **403** từ mạng này |
| Trang bài trên PMC | HTTP **200**, đọc được |
| Danh sách file supplementary trên trang PMC | Đọc được: **15 file** — `NIHMS967427-supplement-{1..7}.pdf` và `{8..15}.xlsx` |
| Tải từng file `.xlsx` qua HTTP | **Không được.** Mọi lần thử trả HTTP 200 nhưng body là trang chờ `Preparing to download ...` dài 1.817 byte, không phải XLSX |
| Thử lại kèm cookie session + `Referer` trang bài | Vẫn trả đúng trang chờ đó |
| Dịch vụ PMC Open Access `oa.fcgi?id=PMC6003881` | HTTP **404** |

Bằng chứng: [pmc-download-interstitial.html](pmc-download-interstitial.html) (nguyên văn trang chờ). Trang này nạp `secure-cookie-*.js` của NCBI, tức cần một bước bắt tay cookie bằng JavaScript. **Không thực hiện bước đó**: đây là cơ chế chống bot mà nhà cung cấp đặt ra có chủ đích, và vượt qua nó không phải việc được làm trong đề tài này.

**Không coi HTTP 200 là truy cập được dữ liệu** — đúng quy ước đã dùng cho MetaDegron.

## Giấy phép `[ĐO]`

`oa.fcgi` trả **404** nghĩa là PMC6003881 **không thuộc PMC Open Access Subset**. Bản trên PMC là **author manuscript (NIHMS)** được công bố theo NIH Public Access Policy: **đọc được tự do, nhưng không có giấy phép mở để phân phối lại**. Bài gốc trên Cell/Elsevier là *all rights reserved*.

`[DIỄN GIẢI]` Hệ quả cho đề tài, kể cả khi sau này tải được:

- Dùng **nội bộ** để phân tích/huấn luyện: nằm trong phạm vi sử dụng học thuật thông thường, và `data/` đã bị gitignore nên không phát hành lại. Giống thế đứng của ClinVar trong [sổ nguồn gốc](../../README.md).
- **Không** được đưa bảng gốc hay bản sao gần nguyên vẹn của nó lên git, lên nguyên mẫu công khai, hay vào phụ lục luận văn. Chỉ được trích số liệu tổng hợp kèm ghi công đầy đủ.
- Vì không có giấy phép mở, bất kỳ việc nhập nguồn này vào **sản phẩm phần mềm công khai** đều phải hỏi lại, không suy ra từ việc bài báo đọc được.

## Đường đi còn lại `[ĐỀ XUẤT]`

1. Tải bằng **trình duyệt thật** từ trang PMC (bước bắt tay cookie chạy được ở đó), rồi đặt file vào `data/raw/koren-2018/` kèm SHA-256 và cập nhật sổ nguồn gốc.
2. Hoặc dùng **quyền truy cập của ĐHCT** vào ScienceDirect để lấy `mmc*.xlsx` gốc.
3. Hoặc hỏi tác giả tương ứng (selledge@genetics.med.harvard.edu) — chậm hơn nhưng dứt điểm cả chuyện quyền sử dụng.

`[ĐO]` **Cập nhật 22/10/2026 (sau khi người dùng tải tay bằng trình duyệt):** sáu file `supplement-{10..15}.xlsx` đã tải được và được sao (không di chuyển) sang `data/raw/koren-2018/`. Ánh xạ **đã xác nhận bằng cách mở file**: `10` = S3 (thế Ala, 5 clone), **`11` = S4 (saturation mutagenesis, 9 substrate)**, `12` = S5, `13` = S6 (S6A = sàng G-end), `14` = S7 (S7A = sàng 23-mer đầu C), `15` = S8 (CRISPR). `supplement-8`, `-9` chưa tải. Kết quả audit và cổng P2: [koren-s4-audit-2026-10-22](../../../research/koren-s4-audit-2026-10-22/README.md). Thư mục `koren-2018-probe/` giữ nguyên làm bằng chứng của lần thử tự động thất bại.
