# Ghi chú audit: bản đồ degron bào tương (Voutsinos 2026)

> Ngày: **11/10/2026**. Phục vụ [báo cáo ứng viên đề tài degron](../../reports/degron-topic-report/index.html) ([bản publish](https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc)). Chỉ audit dữ liệu và mã công khai; **chưa huấn luyện mô hình nào, chưa chạy lại baseline**.

## Nguồn dữ liệu

Repo `KULL-Centre/_2025_Voutsinos_degron_cytosol`, nhánh `main`, giấy phép MIT, 50 file / 83,4 MB, lần đẩy gần nhất 06/03/2026. Bài: *A near-complete map of human cytosolic degrons and their relevance for disease*, **Science Advances 02/2026** (bioRxiv 05/2025). Dữ liệu cũng có trên Zenodo `10.5281/zenodo.16925278`, SRA `PRJNA1277273`.

File đã tải (**không đưa lên git**, tải lại từ `raw.githubusercontent.com`):

| File | SHA-256 (32 ký tự đầu) |
|---|---|
| `score/degrons.csv.gz` | `1e8cdd9d3bfe876705160b70de606129` |
| `models/degron_train.csv.gz` | `ef091ba473660c43a0fbae8dce5cbf41` |

Ngoài ra: `library/holdout_selection.txt`, `library/cytosol_uniq_clust_c60_e-3.tsv`, `models/train_cnn2w.py`, `models/PAP.py`.

## Chạy lại

Tải các file trên vào một thư mục riêng, rồi:

```bash
# đếm tile/gene/nhãn và cụm đồng dạng
python3 -I audit_degron.py  <degron_train.csv.gz> <cytosol_uniq_clust_c60_e-3.tsv> <holdout_selection.txt> degron-audit.json

# kiểm rò rỉ đồng dạng giữa train và holdout
python3 -I audit_holdout.py <degron_train.csv.gz> <cytosol_uniq_clust_c60_e-3.tsv> <holdout_selection.txt> holdout-audit.json

# phân bố cỡ cụm của các gene holdout
python3 -I singleton.py <cytosol_uniq_clust_c60_e-3.tsv> <holdout_selection.txt>

# đối chiếu bảng điểm đầy đủ với file huấn luyện và danh sách holdout
python3 -I reconcile.py <degrons.csv.gz> <degron_train.csv.gz> <holdout_selection.txt> reconcile.json
```

Script chỉ dùng thư viện chuẩn Python, không cần cài gì.

## Cập nhật 11/10/2026 (muộn): tái lập mô hình và ba phép đo quyết định

**Đề tài đã chốt** — xem [topic-decision.md](../../../../topics/degron-e3-specificity/01-idea/topic-decision.md).

### Tái lập PAP bằng numpy, khớp cả hai con số công bố

`rerun_pap.py` và `test_allct.py` dựng lại PAP từ `pap_weights.tgz` chỉ bằng numpy cộng h5py:

| Cấu hình | Kết quả | Bài báo |
|---|---:|---:|
| Chỉ kênh nội | **0,8239** | 0,82 |
| Đầy đủ, kênh C-term áp cho **mọi** tile | **0,8690** | 0,87 |

Chênh lệch ban đầu (0,8245) là do ban đầu chỉ áp kênh C-term cho tile cuối mỗi gene. Trong assay **mọi tile đều gắn vào đầu C của GFP**, nên đầu C của tile luôn là đầu tự do → phải áp cho mọi tile. Việc khớp cả hai con số xác nhận bản tái lập đúng.

### Ba phép đo quyết định thiết kế đề tài

| Phép đo | Kết quả | Hệ quả |
|---|---|---|
| **Đảo thứ tự residue**, cnn2w1 | max \|Δ\| = 4,8 × 10⁻⁷; Pearson(gốc, đảo) = **1,000000** | PAP mặc định **bất biến hoán vị** — không biểu diễn được motif nào |
| Đảo thứ tự, cnn2w7 (cửa sổ 7) | Pearson(gốc, đảo) = 0,9018 | Bản này *có* dùng thứ tự |
| **cnn2w7 so với cnn2w1** | 0,8722 so với 0,8690 = **+0,0032** | Trần của trục "thêm năng lực bắt motif" đã do chính tác giả đo |
| **Đổi phép gộp** (`pool_test.py`) | trung bình 0,824 → max 0,344 → top-3 0,485; entropy theo vị trí 3,294/3,401 | Tín hiệu thang điểm khối **dàn đều, không khu trú**. Kiến trúc khu trú **sẽ không thắng** trên thang này |

Lưu ý giới hạn: phép đổi phép gộp dùng trọng số đã huấn luyện *cho* phép gộp trung bình, nên **không phải** phép thử công bằng cho kiến trúc max pooling huấn luyện từ đầu. Trong `train_cnn2w.py` có một dòng `GlobalMaxPooling1D` **bị chú thích lại** — tác giả đã nghĩ tới, lý do bỏ không nêu.

### Lỗi tái lập trong mã công bố

`train_cnn2w.py` dùng `ci_aa = 1`. Header thật là `name, dna, aa, n, …` nên cột 1 là **DNA**. Vì A/C/G/T đều là ký hiệu acid amin hợp lệ, bộ lọc của script không loại chúng: cả 5.000 dòng thử đều lọt thành chuỗi dài 90 ký tự. **Chạy mã công bố trên dữ liệu công bố sẽ huấn luyện trên chuỗi DNA.** Chú thích trong script ghi một bố cục cột khác → viết cho file trung gian khác.

### Kiến trúc PAP, đã đọc mã đầy đủ

Ba bước huấn luyện. Kênh nội: `Conv1D(filters=25, kernel=1)` → `GlobalAveragePooling1D` → `Dense(50)` → `Dense(50)` → `Dense(1)`, huấn luyện trên **25 residue đầu**. Kênh C-term: 5 residue cuối one-hot (100 chiều) → `Dense(25)` → `Dense(50)` → `Dense(50)` → `Dense(1)`. Đầu ra = `Add()`, **thuần cộng, không có tương tác giữa hai kênh**. Siêu tham số: elu, L2 1e-6, dropout 0,2, batch 1024, Adam lr 1e-4 (bước 3: 1e-5), epochs 2000, patience 100.

`human25`, `human30`, `yeast17` trong `PAP.py` đều là **GLM trên thành phần acid amin** (human25 link sigmoid size 25; human30 link linear size 30). Mặc định dòng lệnh là `cnn2w1`.

### Bộ dữ liệu thứ hai và thứ ba

- **GEO GSE240610 tải được.** Table S1: 52.913.858 byte, SHA-256 bắt đầu `7b669e1ca249f0a3`, 3 sheet (Control Rep 1, Rep 2, MLN4924), mỗi sheet **475.507 dòng** với cột Peptide / Sum of Reads (Normalized) / PSI. Thêm `GSE240610_RAW.tar` 21 MB.
- **MaveDB** (`mave_overlap.py`): 87.125 bản ghi có điểm hợp lệ → **69.209 biến thể duy nhất** trên 9 gene (không phải 100.514; con số cũ lấy từ metadata `numVariants` gồm cả dòng NA). Trùng lặp dồn ở PRKN (18.424→9.283) và PTEN (14.400→5.634).
- **Rò rỉ bậc 3:** 6/9 gene có tile và **toàn bộ ở tập train** — PTEN 26, TPMT 16, NUDT15 10, ASPA 20, PRKN 30, GCK 30 = **132 tile = 0,07%**. CYP2C9, CYP2C19, LDLR không có trong thư viện (không thuộc bào tương).

### Alignment độc lập (`align_check.py`)

Dịch CDS sang protein, sàng 6-mer, Smith-Waterman bằng parasail (BLOSUM62, gap 11/1): 428 protein holdout so với 4.830 protein train, 1.998 cặp ứng viên.

| Ngưỡng | Gene holdout có họ hàng trong train |
|---|---:|
| identity ≥30%, coverage ≥50% | 14 / 428 (3,3%) |
| identity ≥40%, coverage ≥50% | 4 / 428 (0,9%) |
| identity ≥60%, coverage ≥50% | 2 / 428 (0,5%) |

Ca thật đáng chú ý: **`AC104389.5` (holdout) trùng 100% trên 77 residue, phủ 96,2%, với `TRIM5` (train)**. Phần lớn cặp identity 100% khác chỉ là đoạn 7–11 residue, tức nhiễu. Đây là **giới hạn dưới** vì phép sàng dùng 6-mer khớp chính xác, bỏ sót họ hàng xa.

### Chênh lệch 96 gene (`explain96.py`)

Phân vùng thật giữ lại **473 gene** (5.303 − 4.830). Danh sách 527 = **428** đúng + **96** sai (toàn bộ tile ở train) + **3** một phần. Có **45 gene bị giữ lại mà không có trong danh sách**. Thêm 228 gene thiếu *một phần* tile (trung bình 25%) → nhất quán với bộ lọc chất lượng theo từng tile. Nhóm 96 có nhiều tile hơn rõ rệt (64,3 so với 37,0 tile/gene; số lần đo như nhau 6,14 so với 6,04) → **suy luận**: danh sách là tập tiền tuyển, gene lớn được trả về train để giữ dữ liệu. Tác giả không nêu nguyên nhân.

### Tài nguyên tính toán (`bench_esm.py`)

Máy: AMD Ryzen 5 5500U, 12 luồng, 7 GB RAM, không GPU. Hugging Face truy cập được.

| Mô hình | Thông lượng | Toàn bộ 212.658 tile | Cache mức residue |
|---|---:|---:|---:|
| ESM-2 35M (hidden 480) | 64,6 tile/s | **~55 phút** | 12,2 GB fp32 |
| ESM-2 650M (hidden 1280) | 5,3 tile/s | **~11 giờ** | **32,7 GB fp32** — vượt RAM |

Gộp ở mức tile thì cache chỉ 408 MB (35M) và 1,1 GB (650M). Kiến trúc CMIL-E3 **cần mức residue** → phải xử lý theo luồng hoặc xin GPU.

### Giấy phép

Repo và Zenodo `16925278`: **MIT**. MaveDB: **CC0**. DegronID Zenodo `8103915`: other-open. Hai bản tiền ấn bioRxiv: **CC BY-NC-ND** (áp cho văn bản bài báo, không phải dữ liệu).

---

## Kết quả chính (vòng đầu)

| Phép đo | Giá trị |
|---|---:|
| Tile trong bảng đầy đủ | 212.658 |
| Gene trong bảng đầy đủ | 5.327 |
| Tile ở tập train | 195.629 |
| Gene ở tập train | 4.830 |
| Nhãn `degron_score`: trung bình · sd · khoảng | 0,481 · 0,376 · −0,144…1,132 |
| Cụm đồng dạng (phủ 60%, e < 10⁻³) | 5.273 gene → 3.242 cụm |
| Cụm nhiều thành viên · cụm lớn nhất | 834 · 69 gene |
| Gene trong `holdout_selection.txt` | 527 |
| **Gene holdout là cụm đơn lẻ** | **527 / 527** |
| Gene trùng giữa train và validation (early stopping) | 0 |
| Gene holdout có **toàn bộ** tile ở tập train | 96 |
| Gene holdout giữ một phần tile | 3 |
| **Holdout hiệu dụng** | **428 gene / 15.820 tile** |

## Hai giả thuyết đã bị chính dữ liệu bác bỏ

Ghi lại để không ai lặp lại, kể cả Claude ở phiên sau:

1. **"Tile chồng nhau 15 acid amin nên holdout bị rò rỉ" — sai.** Holdout chia theo **gene**, không theo tile.
2. **"Tác giả không kiểm soát đồng dạng" — sai.** Cả 527 gene holdout đều là cụm đơn lẻ, tức được chọn có chủ ý từ gene không có paralog trong thư viện. Tập validation dùng cho early stopping (`validation_split=0.2` của Keras trên file đã sắp theo ENSG) cũng rời hẳn theo gene: 3.666 gene phần train, 1.164 gene phần validation, 0 gene trùng.

**Hệ quả: không được lấy "sửa giao thức đánh giá" làm đóng góp của đề tài.** Giao thức của tác giả đã tốt.

## Phát hiện audit còn giá trị

**96/527 gene** trong danh sách holdout thực tế **không được giữ lại** (toàn bộ tile của chúng nằm trong file huấn luyện), 3 gene nữa chỉ giữ một phần. Holdout hiệu dụng là **428 gene / 15.820 tile**. Nguyên nhân **chưa xác định** — có thể là bộ lọc chất lượng áp dụng sau khi chọn, hoặc danh sách là tập ứng viên trước lọc. Đây là con số phải dùng khi so sánh với Pearson 0,87 mà tác giả báo, và là lý do phải tự chạy lại baseline thay vì chép số.

Ngoài ra: 17.029 tile có trong bảng đầy đủ nhưng không có trong file huấn luyện, trải trên 728 gene, trong đó **297 gene không nằm trong danh sách holdout** — chưa truy được vì sao bị loại.

## Giới hạn của audit này

- Kết luận về đồng dạng dựa trên **file gom cụm do tác giả cung cấp**, ngưỡng phủ 60% / e < 10⁻³; **chưa chạy alignment độc lập**. Ngưỡng này vẫn cho phép quan hệ họ hàng xa tồn tại dưới ngưỡng.
- **Chưa đọc toàn văn Methods**; kiến trúc PAP và siêu tham số chỉ biết qua `train_cnn2w.py` và phần đầu bài.
- **Chưa tải GEO GSE240610** (Zhang 2023, sàng lọc thứ hai) — đây là cổng chặn cho bậc 2 và phần XAI của đề tài.
- Con số **100.514** phép đo độ dồi dào trên 9 gene lấy từ API MaveDB (`POST https://api.mavedb.org/api/v1/score-sets/search`, body `{"targets":["<GENE>"]}`, khóa trả về là `scoreSets`). Các bộ trong cùng một gene **chồng nhau** và **chưa khử trùng lặp**.
