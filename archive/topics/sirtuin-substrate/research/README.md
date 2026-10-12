# Bằng chứng và tái tạo audit SIRT1–7

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Kết quả khảo sát: [báo cáo](../sirtuin-substrate-deep-research.md). Ngày truy xuất 08/10/2026. Đây là kiểm tra dữ liệu và nguồn, **không huấn luyện mô hình**.

## Các artifact trong Git

| File | Vai trò |
|---|---|
| [audit_data.py](audit_data.py) | Đọc SD1, SD13–15, bảng Zhang, Weinert EV1 và Deep-PLA; đối chiếu nhãn/overlap; không sinh nhãn sinh học mới |
| [audit_mapping.py](audit_mapping.py) / [mapping-audit-results.json](mapping-audit-results.json) | Kiểm 149 site tế bào với UniProt snapshot có hash; residue K và peptide tryptic đều khớp; chưa kiểm toàn bộ train |
| [audit-results.json](audit-results.json) | Số đếm thực tế và SHA256 các bảng; là nguồn của các số `[KT]` trong báo cáo |
| [fetch_sources.py](fetch_sources.py) | Tải URL công khai, lưu HTTP/bytes/hash; kiểm signature XLSX/PDF và giải nén Weinert |
| [sources.json](sources.json) | URL cho các nguồn đã dùng; GitHub data/code pin commit e7cb6d7eb8837c770bd1638dcd45c59688535cfa |
| [download-manifest.json](download-manifest.json) | Bản ghi các lượt tải còn lưu; bao gồm lỗi/response không hợp lệ. Không phải log web đầy đủ hoặc bằng chứng mọi HTTP200 là tài liệu thật |
| [search-log.md](search-log.md) | Chiến lược khảo sát, mức đọc và giới hạn |

Toàn văn/PDF/Excel/mã bên thứ ba ở **`archive/topics/sirtuin-substrate/data/raw/`**, bị Git ignore. Không đưa dữ liệu gốc hoặc toàn văn publisher vào commit. Một số link CDN của Deep-PLA có chữ ký công khai hết hạn: nếu tải lại lỗi, mở DOI bài, lấy link Supplementary Data/Methods mới; kiểm checksum trước so sánh. Chữ ký này là link tải publisher, không phải thông tin xác thực cá nhân.

## Tái tạo từ repository root

Dùng môi trường Python có `pandas`, `numpy`, `openpyxl` (đã dùng pandas trong `.venv`, openpyxl cài tạm ngoài repo ở phiên này). Có thể tạo môi trường riêng:

```bash
python3 -m venv /tmp/sirtuin-audit-venv
/tmp/sirtuin-audit-venv/bin/pip install pandas numpy openpyxl
/tmp/sirtuin-audit-venv/bin/python archive/topics/sirtuin-substrate/research/fetch_sources.py
/tmp/sirtuin-audit-venv/bin/python archive/topics/sirtuin-substrate/research/audit_data.py
/tmp/sirtuin-audit-venv/bin/python archive/topics/sirtuin-substrate/research/audit_mapping.py
```

Lệnh đã thực thi audit trong phiên:

```bash
PYTHONPATH=/tmp/nckh2-guideline-tools .venv/bin/python archive/topics/sirtuin-substrate/research/audit_data.py
PYTHONPATH=/tmp/nckh2-guideline-tools .venv/bin/python archive/topics/sirtuin-substrate/research/audit_mapping.py
```

Không cần network khi đủ input cache. Fetch bảo toàn file đã có nếu server trả nội dung khác, lưu snapshot mới với hậu tố hash; vì vậy khi upstream đổi, audit mặc định vẫn đọc snapshot đầu. So hash JSON/manifest trước khi kết luận tái tạo được. File giả `.xlsx` chứa HTML CAPTCHA từ thử tải Rardin/PMC được giữ ở raw cache để nhận biết lỗi, không đưa vào audit. Các lần tải trước khi thêm kiểm signature chỉ có HTTP/bytes/hash; không có trường `valid_file_signature`.

Weinert ZIP tải từ Europe PMC; script giải nén các file `embj0034-*` thành `weinert-zip-*`. SD1 Rauh đọc sau bốn dòng header; SD15 chỉ dùng chín cột dữ liệu. Đối chiếu bằng chuỗi Z→X, **không dùng thứ tự dòng**. Zhang S1 lọc `Order` số để loại legend/footer; S2 lọc `UniquePepID` để loại dòng chú thích. EV1 dùng header hàng38 Excel. SD13 được đọc streaming, không coi formatting/max_row của spreadsheet là số dữ liệu.

## Cách diễn giải audit

- 6.802/6.801 là số **chuỗi peptide khác nhau**, không số protein phân biệt chắc chắn. Chuỗi thiếu là GIQCVKKRDLEQA; Rauh SD2 xác nhận Q04206 K123 và mapping khác. Chưa biết lý do Ridgeway bỏ dòng.
- `mismatches_efficiency_ge1` toàn 0 là kiểm chứng bảng nhãn; không chứng minh quy trình tạo feature hoặc model đã đúng như Methods.
- Overlap `(accession, position)` dựa `uid_pos` trong CSV và annotation SD14, chưa resolve toàn bộ accession/biến thể hoặc accession cũ.
- Audit window dùng **13 residue**, so không gap, loại train có X: số trùng ngắn/ngưỡng 10/13 là mô tả độ giống chuỗi. **Không phải full-protein homology**; có thể bị ảnh hưởng composition và central K chung.
- Deep-PLA đếm annotation theo enzyme/loài, không unique biological site đã hợp nhất tất cả enzyme. Overlap chỉ key; chưa kiểm homology hoặc toàn bộ PMID.
- Weinert EV1 2.106 ratio SIRT3 nhập từ Hebert là dữ liệu định lượng, không gold standard cơ chất. 483 ratio≥2 không phải positive calls có kiểm định.
- SD13/14 khác score cho cùng149 key; không lấy một snapshot thay snapshot khác. Không có fitting nào được chạy để giải thích chênh lệch.

## Những phần chưa xác minh / trạng thái tải

1. Rardin S3–S5: PMC trả challenge HTML; Europe PMC supplementaryFiles trả XML lỗi; các đường PNAS đã thử trả403. Các bảng site-level chưa đọc được. Không có rejection của auto-review: đây là phản hồi server.
2. Hebert fullTextXML trả500 và PMC challenge; mới đọc abstract và dữ liệu dẫn xuất EV1. Chưa có replicate/uncertainty của KO gốc, không coi EV1 thành một nghiên cứu KO mới.
3. PRIDE files/byProject v2/v3 trả body rỗng200; metadata của bốn accession tải được. Chưa lập danh sách raw/processed đầy đủ và chưa xác nhận số lặp PXD012796/PXD019763.
4. SIRT2: Synapse [syn26134616](https://doi.org/10.7303/syn26134616), [acetylome](https://www.synapse.org/Synapse:syn26134618), [global](https://www.synapse.org/Synapse:syn26134617), [bảng S1](https://www.synapse.org/Synapse:syn26134636). Chưa tải raw spectra/MaxQuant tổng; không tái phân tích MS. [Ghi chú mẫu](https://www.synapse.org/Synapse:syn26134616/discussion/threadId=9116) xác định mẫu lẻ1/3/5/7 dùng downstream; mẫu chẵn không phải replicates tương ứng.
5. Chênh Zhang152↔Ridgeway149 và nguyên nhân SD13↔SD14 khác model score chưa giải được; giữ nguyên nguồn, không chuẩn hóa về số mong muốn.
6. Đã kiểm 149/149 test có K và peptide tryptic khớp trên UniProt hiện hành, có hash snapshot; chưa phục hồi RefSeq v54. Chưa kiểm mapping mọi train trên FASTA pin release, chưa chạy MMseqs2/CD-HIT toàn protein, chưa tạo benchmark/split chính thức.
7. Chưa đọc toàn văn NAD_MCNN/SirtSAGE; không xác nhận kiến trúc chi tiết SirtSAGE từ bài đăng mạng xã hội.
8. Chưa có model training, kết quả ablation, conformal calibration/coverage hoặc XAI thực nghiệm của đề tài.

Báo cáo kết luận có điều kiện dựa trên chính những giới hạn này; không xem file tải được là đã đạt cổng nhãn sinh học.

UniProt query ban đầu vượt giới hạn100 điều kiện OR và trả400; chia thành80+43 accession đã tải được. Lấy isoform P06753-2 riêng. Có124 sequences lưu (123canonical cùng một isoform bổ sung), dùng accession chính xác cho149 test sites. Snapshot được pin bằng SHA256/ngày tải, chưa có release header trong bản ghi cũ; không xem live FASTA là trình tự lịch sử của thí nghiệm.

## Kiểm tra hoàn tất trong phiên

Đã chạy audit bảng và mapping, kiểm cú pháp cả ba script bằng `python3 -m py_compile`, kiểm liên kết Markdown địa phương/whitespace và `git diff --check`. Đã kiểm báo cáo khuyến nghị ban đầu không có diff. Các kiểm tra này xác nhận artifact khảo sát, không xác nhận chất lượng mô hình hoặc độ đúng của nhãn sinh học.
