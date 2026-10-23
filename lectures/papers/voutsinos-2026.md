[← Danh mục bài báo](README.md) · Về hub

# Voutsinos 2026 — bản đồ degron bào tương người và mô hình PAP

| | |
|---|---|
| **Tên** | *A near-complete map of human cytosolic degrons and their relevance for disease* |
| **Tác giả** | Voutsinos V, Johansson KE, Larsen FB, Grønbæk-Thygesen M, Jonsson N, Holm-Olesen E, Tesei G, Stein A, Fowler DM, Lindorff-Larsen K, Hartmann-Petersen R |
| **Nơi công bố** | *Science Advances*, 02/2026 (bioRxiv 05/2025) |
| **DOI** | <https://doi.org/10.1126/sciadv.adz3483> |
| **Toàn văn mở** | <https://pmc.ncbi.nlm.nih.gov/articles/PMC12880521/> |
| **Mã nguồn** | `KULL-Centre/_2025_Voutsinos_degron_cytosol`, giấy phép **MIT** |
| **Dữ liệu** | Zenodo `10.5281/zenodo.16925278`, SRA `PRJNA1277273` |
| **Giấy phép** | **CC BY-NC 4.0** — hình được phép dùng lại có ghi nguồn |
| **Mức kiểm** | **[TỰ KIỂM]** — đã tải dữ liệu, đọc hết mã nguồn, **tái lập PAP bằng numpy** |

---

## Bài này làm gì

Hai việc. **Một:** dựng bản đồ degron gần hoàn chỉnh cho protein bào tương người — cắt 5.672 protein thành 214.158 tile dài 30 acid amin, đo độ bền từng tile bằng sàng lọc GPS (bài 2). **Hai:** huấn luyện một mô hình dự đoán điểm degron từ trình tự, gọi là **PAP**.

## Vì sao bài này quan trọng nhất với đề tài

Vì nó cung cấp **cả bộ dữ liệu 1 lẫn baseline phải vượt**. Toàn bộ lập luận về khoảng trống ở bài 5 là lập luận về điểm yếu của PAP.

## Kiến trúc PAP — đã đọc hết mã nguồn [TỰ KIỂM]

Ba bước huấn luyện, hai kênh cộng thẳng:

- **Kênh nội:** `Conv1D(filters=25, kernel=1)` → `GlobalAveragePooling1D` → `Dense(50)` → `Dense(50)` → `Dense(1)`, trên **25 residue đầu**
- **Kênh C-terminal:** 5 residue cuối one-hot (100 chiều) → `Dense(25)` → `Dense(50)` → `Dense(50)` → `Dense(1)`
- **Đầu ra:** `Add()` — **thuần cộng, không có tương tác giữa hai kênh**
- Siêu tham số: elu, L2 1e-6, dropout 0,2, batch 1024, Adam lr 1e-4 (bước 3: 1e-5), epochs 2000, patience 100

Để ý `kernel=1`: convolution chỉ xem **một residue mỗi lần**, rồi `GlobalAveragePooling` lấy trung bình. Đó là nguồn gốc của tính bất biến hoán vị.

## Con số đáng nhớ

**Tái lập PAP — khớp cả hai số công bố** [TỰ KIỂM]:

| Cấu hình | Mình tái lập | Bài báo |
|---|---:|---:|
| Chỉ kênh nội | **0,8239** | 0,82 |
| Đầy đủ | **0,8690** | 0,87 |

> Chênh lệch ban đầu (0,8245) là do lúc đầu chỉ áp kênh C-term cho tile cuối mỗi gene. Nhưng trong assay **mọi tile đều gắn vào đầu C của GFP**, nên đầu C của tile luôn là đầu tự do → phải áp cho **mọi** tile. Việc khớp được cả hai con số xác nhận bản tái lập là đúng.

**Ba phép đo quyết định thiết kế đề tài** [TỰ KIỂM]:

| Phép đo | Kết quả | Hệ quả |
|---|---|---|
| Đảo thứ tự residue, `cnn2w1` | max \|Δ\| = 4,8 × 10⁻⁷ · **Pearson = 1,000000** | **Bất biến hoán vị** — không biểu diễn được motif nào |
| Đảo thứ tự, `cnn2w7` | Pearson = 0,9018 | Bản này *có* dùng thứ tự |
| `cnn2w7` so với `cnn2w1` | **+0,0032** | Trần của trục "bắt motif" **đã do chính tác giả đo** |
| Đổi phép gộp | 0,824 → max 0,344 → top-3 0,485 | Tín hiệu điểm khối **dàn đều, không khu trú** |

Entropy theo vị trí: 3,294 / 3,401 — gần tối đa.

## Hai phát hiện khi tự kiểm, đáng đưa vào luận văn

**1. Một lỗi trong mã công bố.** `train_cnn2w.py` dùng `ci_aa = 1`, nhưng header thật là `name, dna, aa, n, …` → **cột 1 là DNA**. Vì A/C/G/T đều là ký hiệu acid amin hợp lệ, bộ lọc không loại chúng: cả 5.000 dòng thử đều lọt. **Chạy mã công bố trên dữ liệu công bố sẽ huấn luyện trên chuỗi DNA.** Chú thích trong script ghi một bố cục cột khác, nên có lẽ nó viết cho một file trung gian khác.

**2. Danh sách holdout công bố không dùng được nguyên.** Bài công bố 527 gene holdout, nhưng **96 gene** trong đó thực ra nằm hết trong tập huấn luyện. Tập test hiệu dụng tính lại từ dữ liệu: **428 gene / 15.820 tile**.

Cả hai là lý do phải **tự tái lập** thay vì tin mã có sẵn.

## Hình của tác giả được phép dùng

Sáu hình, CC BY-NC 4.0, tải ngày 11/10/2026 — ở assets/figures/:

| File | Nội dung |
|---|---|
| `voutsinos2026-f1.jpg` | Thư viện tile và hệ sàng lọc GPS |
| `voutsinos2026-f2.jpg` | Ảnh hưởng của **loại acid amin** và **vị trí** |
| `voutsinos2026-f3.jpg` | Bối cảnh cấu trúc: điểm degron so với rASA và pLDDT (ρ = −0,47 trên 173 protein phơi lộ nhất) |
| `voutsinos2026-f4.jpg` | **Kiến trúc PAP** và hai biểu đồ holdout (0,82 / 0,87) |
| `voutsinos2026-f5.jpg` | ΔPAP so với độ dồi dào biến thể ở ASPA, PRKN, PTEN |
| `voutsinos2026-f6.jpg` | ΔPAP ở vùng phơi lộ (Kruskal–Wallis P = 5,4 × 10⁻⁶) và ca **PNPO D33V** |

## Chỗ bài này chừa lại cho đề tài

Tác giả dùng cấu trúc (rASA, pLDDT) **chỉ để phân tích sau**, không đưa vào mô hình. Và mô hình của họ bất biến hoán vị ở kênh chính. Hai chỗ đó là chỗ đứng của đề tài — xem bài 6.

## Nguồn trong repo

- [voutsinos-2026-audit/](../../topics/degron-footprint/research/voutsinos-2026-audit/README.md) — ghi chú audit, script, JSON kết quả
- NOTICE.md — giấy phép hình

---

[← Danh mục bài báo](README.md) · Về hub
