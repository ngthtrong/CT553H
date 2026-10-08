# Kiểm chứng cổng dữ liệu cho đề tài dự đoán cơ chất SIRT1–7

Ngày kiểm: **08/10/2026**. Tất cả file được tải và đếm trong phiên này trên môi trường cloud.

Nhãn bằng chứng: `[tự kiểm]` = Claude tự tải file và tự đếm · `[tác giả báo cáo]` = con số do bài báo nêu · `[suy luận]` = diễn giải từ số đã đếm · `[chưa kiểm]` = chưa xác nhận được.

Bảng dẫn xuất đã lưu: [data/](data/) — `dataset-inventory.csv`, `rauh2013-per-isoform-counts.csv`, `rauh2013-isoform-copositive-matrix.csv`, `rauh2013-positives-per-site.csv`, `ridgeway2025-suppdata14-sirt2-incell-149sites.csv`, `sol2012-u2os-sirt3kd-sites.csv.gz`.

---

## Kết luận ngắn trước khi vào chi tiết

1. **Cổng dữ liệu MỞ ĐƯỢC.** Có thể dựng tập đánh giá trong tế bào cho **hai isoform**: SIRT2 (149 vị trí, chỉ dương, từ Ridgeway 2025) và **SIRT3 (3.174 vị trí người có định lượng, trong đó dựng được cả âm, từ Sol 2012 PLoS ONE)**. Cả hai đều tải được từ môi trường cloud `[tự kiểm]`.
2. **Nhưng kết quả sơ bộ rất xấu cho giả thuyết của đề tài.** Trên 1.417 vị trí khớp cửa sổ 13-mer giữa mảng Rauh và tập SIRT3 trong tế bào, nhãn SIRT3 của mảng **gần như không có giá trị dự báo** chiều biến đổi acetyl hóa trong tế bào: MCC từ **+0,047 đến +0,080** tùy ngưỡng, precision 14,0% so với base rate 10,6% ở ngưỡng 1,5× `[tự kiểm]`. Đây là tin tốt cho việc *đóng khung* đề tài quanh khoảng cách in vitro → trong tế bào, nhưng cần nói trước với GVHD rằng câu trả lời có khả năng cao là **âm**.
3. **Ba con số trong [topic-final-recommendation.md](../../reports/topic-final-recommendation.md) phải sửa** (chi tiết ở mục 6): quy tắc sinh nhãn nhị phân, bản chất của Supplementary Data 13, và cách diễn giải "6.802 vs 6.801".

---

## 1. Rauh et al. 2013, Supplementary Data 1 (nhãn huấn luyện)

### Takeaway
Tải được, **6.802 vị trí × 7 isoform**, mỗi isoform **4 cột**. Nhãn gốc là **thang liên tục**, và `substrate category` **không** phải nhị phân như tên gọi gợi ý — nó nhận 41 giá trị phân số rời rạc.

### Lệnh tái lập
Trang bài: https://www.nature.com/articles/ncomms3327 (HTTP 200). Supplementary Data 1 = `MOESM80` (2.122.503 byte ≈ 2,12 MB — khớp "2,1 MB" trong báo cáo).

```bash
curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64)" -o MOESM80.xlsx \
 "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms3327/MediaObjects/41467_2013_BFncomms3327_MOESM80_ESM.xlsx"
```

Lưu ý: host `static-content.springer.com` trả **403**; host `media.springernature.com` trả **200** `[tự kiểm]`. Supplementary Data 1–7 = `MOESM80`–`MOESM86`.

### Cấu trúc đúng (bố cục cột)
Một sheet duy nhất tên `Tabelle1`, **6.806 dòng × 31 cột**; 4 dòng đầu là tiêu đề, còn **6.802 dòng dữ liệu** `[tự kiểm]`.

| Chỉ số cột | Nội dung |
|---|---|
| 0 | `Sequence` — peptide **13 amino acid** (6 residue mỗi bên lysine trung tâm) |
| 1–4 | Sirt1: `substrate category`, `signal ratio (exp:ref)`, `ratio error`, `efficiency` |
| 5–8 / 9–12 / 13–16 / 17–20 / 21–24 / 25–28 | Sirt2 / Sirt3 / Sirt4 / Sirt5 / Sirt6 / Sirt7, cùng 4 cột đó |
| 29 | `Protein names (position of acetylation site)` — tên protein kèm vị trí trong ngoặc |
| 30 | `Uniprot Accession Codes` — danh sách accession cách nhau bằng `;` |

**Cảnh báo kỹ thuật:** dòng tiêu đề thứ hai (dòng Excel 3) **lệch một cột** so với dữ liệu — nó đặt `Protein names` ở cột 28, trong khi cột 28 thực tế là `efficiency` của Sirt7. Đọc file bằng `header=2` sẽ gán sai tên cho 3 cột cuối `[tự kiểm]`. Tổng số cột là 31 (= 1 + 7×4 + 2), **không** có cột `Name..Pos.` riêng dù dòng tiêu đề có ghi chữ đó.

### Thiếu, trùng, mã hóa
- **Độ dài chuỗi:** cả 6.802 dòng đều đúng 13 ký tự `[tự kiểm]`.
- **Trùng chuỗi:** **0** — cả 6.802 peptide là duy nhất `[tự kiểm]`.
- **Ký tự đệm:** Rauh dùng **`Z`** để đệm khi lysine nằm gần đầu/cuối protein (ví dụ `ZZMSILKIHAREI`). **249 dòng** có `Z` `[tự kiểm]`.
- **Giá trị thiếu:** **không thiếu** ở 29 cột đầu (Sequence + 28 cột isoform). Riêng `Protein names` và `Uniprot Accession Codes` **thiếu ở 473 dòng** `[tự kiểm]` — tức 7,0% vị trí **không truy được protein/vị trí residue** từ chính file này.
- **Mã hóa accession:** nhiều accession mỗi dòng, phân cách `;`, **trung vị 2–3** accession/dòng, nhiều nhất tới 12+ (ví dụ P34897 có 12). Phân bố: 1 accession 1.078 dòng, 2 accession 1.176, 3 accession 916, 4 accession 844, 5 accession 630, 6 accession 483, 7 accession 283, 8 accession 240 `[tự kiểm]`. **2.937 accession đầu tiên khác nhau** (coi là "protein"); tổng **13.240 accession** xuất hiện ở đâu đó trong file `[tự kiểm]`.
- **Mã hóa vị trí residue:** **không có cột số riêng.** Vị trí nằm trong ngoặc của chuỗi text `Protein names`, và **một dòng có thể mang nhiều vị trí**, ví dụ `Liprin-beta-1 ( 310;138 );cDNA FLJ54647, highly similar to Liprin-beta-1 ( 138 )`. Đây là điểm bẩn nhất của file.
- **Trùng vị trí (accession đầu + vị trí đầu):** **475 dòng trùng** với một dòng khác; ví dụ `P78329_4` xuất hiện **3 lần**, `Q32P41_37` 2 lần `[tự kiểm]`. Nghĩa là "một vị trí" không map 1–1 với "một dòng" — phải xử lý khi chia tập theo protein.
- Sau khi gỡ, số cặp **(UniProt, vị trí)** khôi phục được là **17.170** cho 6.801 dòng `[tự kiểm]` — nhiều hơn số dòng vì mỗi dòng mang nhiều protein × nhiều vị trí.

### Phân bố `substrate category` theo isoform
`substrate category` nhận **41 giá trị rời rạc** trong [0; 1], rõ ràng là **tỉ lệ k/n** (0; 0,04; 0,07; 0,10; 0,11; 0,14; 0,17; …; 0,33; 0,50; 0,67; 0,83; 1,00). Giá trị dày nhất: `0` 9.362 lần, `1` 8.042, `0,33` 6.276, `0,50` 5.047, `0,67` 4.899 (gộp cả 7 isoform) `[tự kiểm]`.

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| `category = 1` | **4** | 822 | 1.171 | 1.011 | 2.615 | 737 | 1.682 |
| `category = 0` | 27 | 637 | 1.302 | 1.428 | 2.538 | 954 | 2.476 |
| `category > 0` | 6.775 | 6.165 | 5.500 | 5.374 | 4.264 | 5.848 | 4.326 |
| trung vị `signal ratio` | 1,07 | 0,99 | 1,06 | 1,01 | 0,96 | 1,06 | 1,03 |
| trung vị `ratio error` | **0,37** | 0,22 | 0,24 | 0,24 | 0,21 | 0,27 | 0,22 |
| trung vị `efficiency` | 0,371 | 0,522 | 0,407 | 0,340 | 0,521 | 0,441 | 0,320 |

`[tự kiểm]` — xem `data/rauh2013-per-isoform-counts.csv`.

Quan hệ giữa các cột: **`efficiency` = `substrate category` / `signal ratio`** (kiểm trên dòng đầu: 0,14 / 1,84 = 0,07609, đúng giá trị trong file) `[tự kiểm]`.

---

## 2. Nhãn nhị phân: quy tắc đúng là `efficiency ≥ 1`, KHÔNG phải `category = 1`

### Takeaway
Đây là đính chính quan trọng nhất của phiên này. Nhãn nhị phân mà bài 2025 dùng được sinh bằng **`efficiency ≥ 1`** (tương đương **`substrate category ≥ signal ratio`**), tái lập **100,0000% chính xác** trên cả 47.607 ô (6.801 vị trí × 7 isoform), **0 bất đồng** `[tự kiểm]`.

### Bằng chứng
Ridgeway 2025 **Supplementary Data 15** (sheet `Table 13`) là chính bảng nhãn nhị phân kèm chuỗi 13-mer: **6.801 dòng × 9 cột** (`Uniprot ID`, `Site`, `SIRT1`…`SIRT7`), 0 giá trị thiếu, 6.801 chuỗi duy nhất, **2.999 UniProt ID** `[tự kiểm]`. File này dùng **`X`** để đệm (696 ký tự `X` tổng cộng) nơi Rauh dùng `Z`. Sau khi đổi `Z` → `X`, merge theo chuỗi khớp **6.801/6.801** `[tự kiểm]`.

So sánh các quy tắc, trên 6.801 dòng merge được:

| Quy tắc | Số ô bất đồng / 47.607 | % khớp |
|---|---|---|
| `efficiency ≥ 1` | **0** | **100,0000%** |
| `substrate category ≥ signal ratio` | **0** | **100,0000%** |
| `category ≥ 0,795` (ngưỡng toàn cục tốt nhất) | 712 | 98,506% |
| `category = 1` | 2.423 | 94,910% |

`[tự kiểm]`

Theo quy tắc `efficiency ≥ 1`, số dương mỗi isoform khớp tuyệt đối với Supplementary Data 15: SIRT1 **176**, SIRT2 **1.901**, SIRT3 **1.844**, SIRT4 **1.038**, SIRT5 **2.614**, SIRT6 **1.199**, SIRT7 **1.692** `[tự kiểm]`.

### Vì sao điều này quan trọng cho đề tài
- Bảng trong [topic-final-recommendation.md](../../reports/topic-final-recommendation.md) mục 2.1 ghi các số 176/1.901/… dưới nhãn "`category = 1`". **Số thì đúng, nhãn thì sai.** `category = 1` chỉ cho SIRT1 **4** vị trí dương, không phải 176.
- Hệ quả thực chất: nhãn nhị phân **đã chuẩn hóa theo `signal ratio`** rồi, nên nó **không phải** một phép ngưỡng cứng thô như báo cáo mô tả. Luận điểm "ngưỡng cứng `category ≥ 1` làm mất 2.438 vị trí dương yếu của SIRT1" **không đứng được** như đã viết — phải viết lại.
- Mặt khác, **`ratio error` thật sự chưa được dùng ở đâu cả**. Đó mới là chỗ trống hợp lệ cho đề xuất "nhãn thứ tự có trọng số sai số": SIRT1 có trung vị `ratio error` 0,37, cao nhất trong 7 isoform, tức 176 nhãn dương của SIRT1 là loại nhiễu nhất.
- Nhãn **không tách được** theo `category` một mình: với SIRT1, `category` nhỏ nhất trong nhóm dương là 0,68 còn lớn nhất trong nhóm âm là 0,86 — chồng lấn `[tự kiểm]`. Chỉ SIRT5 tình cờ tách được (`category ≥ 0,505` cho đúng 2.614).

### Cấu trúc đa nhãn
Phân bố số isoform dương trên mỗi vị trí (Supplementary Data 15, `data/rauh2013-positives-per-site.csv`) `[tự kiểm]`:

| số isoform dương | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| số vị trí | 1.107 | 2.430 | 2.087 | 902 | 226 | 44 | **5** | **0** |

Khớp đúng con số trong báo cáo `[tự kiểm]`. Dương độc quyền một isoform: SIRT1 21, SIRT2 319, SIRT3 289, SIRT4 162, **SIRT5 1.088**, SIRT6 269, SIRT7 282 `[tự kiểm]`.

Cặp đồng dương mạnh nhất: **SIRT2–SIRT3 1.136** vị trí, SIRT5–SIRT7 816, SIRT3–SIRT7 534 `[tự kiểm]` — xem `data/rauh2013-isoform-copositive-matrix.csv`. Đây là cơ sở định lượng cho mô hình 7 đầu ra.

---

## 3. Chênh lệch 6.802 vs 6.801: đã tìm ra nguyên nhân

### Takeaway
**Đúng là chênh một dòng, và dòng đó xác định được.** Rauh Supplementary Data 1 có 6.802 dòng dữ liệu; Ridgeway Supplementary Data 15 và `All_Sirts_Feature_Y_labels.csv` đều có 6.801 dòng. Dòng bị loại là:

```
Sequence   : GIQCVKKRDLEQA
Protein    : Transcription factor p65 ( 123;134;114;92 ); RELA protein ( 123 );
             cDNA FLJ57698, highly similar to Transcription factor p65 ( 134 )
Accessions : Q04206;Q2TAM5;B4E082;Q96CP1;E9PKH5;E9PMD5;Q96F54;E9PQS6;E9PKV4;E9PI38
```

`[tự kiểm]` — sau khi đổi `Z`→`X`, đây là **chuỗi duy nhất** của Rauh không có trong Supplementary Data 15, và Supplementary Data 15 không có chuỗi nào ngoài Rauh.

**Lý do bị loại: `[chưa kiểm]`.** Bài báo không nói. Dòng này có đặc điểm bất thường: **4 vị trí** trong một ngoặc (`123;134;114;92`) và **10 accession** — nhiều nhất về số vị trí trong file. `[suy luận]` khả năng cao là bước phân giải vị trí/accession của Ridgeway bỏ dòng này vì không giải được một vị trí duy nhất, chứ không phải lỗi đếm. Không có bằng chứng xác nhận.

### `All_Sirts_Feature_Y_labels.csv` — xác nhận và kiểm tính nhất quán
```bash
curl -sSL -o labels.csv \
 "https://raw.githubusercontent.com/nashirag/ML-Hybrid_Ensemble_Method/HEAD/SIRT1-7_Investigation/ML_Components/All_Sirts_Feature_Y_labels.csv"
```
HTTP **200**, 224.234 byte, **6.802 dòng text = 1 header + 6.801 dòng dữ liệu** `[tự kiểm]`.

- **9 cột:** `Unnamed: 0` (chỉ số chạy), `uid_pos`, và 7 cột `SIRT_<n>_EXPERIMENTALLY_ACTIVE` **theo thứ tự lộn xộn 5,4,1,7,2,6,3** `[tự kiểm]` — rất dễ gán sai isoform nếu đọc theo vị trí cột.
- `uid_pos` dạng `P05141_163_c0`: accession + vị trí + hậu tố `_c<k>` để phân biệt trùng. 6.801 `uid_pos` **duy nhất**, 0 trùng; **2.999 accession** khác nhau `[tự kiểm]`.
- **Tổng số dương khớp Supplementary Data 15 tuyệt đối** cho cả 7 isoform (176 / 1.901 / 1.844 / 1.038 / 2.614 / 1.199 / 1.692) `[tự kiểm]`.
- **Nhưng thứ tự dòng khác nhau:** so theo chỉ số dòng, hai file bất đồng 338–3.160 dòng tùy isoform `[tự kiểm]`. `[suy luận]` `labels.csv` là cùng tập nhãn đã **xáo trộn** (hoặc sắp theo khóa khác). **Hệ quả thực hành: phải join theo `uid_pos`, tuyệt đối không join theo chỉ số dòng.**

**Kết luận kiểm tính nhất quán: ĐẠT.** `labels.csv` khớp hoàn toàn với nhãn dẫn ra từ Rauh Supplementary Data 1 bằng quy tắc `efficiency ≥ 1`, và khớp với bảng nhãn công bố của chính bài 2025 `[tự kiểm]`.

---

## 4. Ridgeway et al. 2025 — Supplementary Data 13, 14, 15

### Takeaway
Cả ba tải được, **nhưng chỉ từ Springer, không từ PMC**. PMC trả về trang HTML "Preparing to download…" (reCAPTCHA interstitial, 1.817–21.395 byte) thay vì xlsx `[tự kiểm]`.

### Lệnh tái lập
Ánh xạ: **Supplementary Data N = `MOESM(N+2)`** (xác nhận bằng caption trên trang PMC) `[tự kiểm]`.

```bash
# KHÔNG dùng PMC: pmc.ncbi.nlm.nih.gov/articles/instance/12594832/bin/... -> HTML reCAPTCHA
for n in 15 16 17; do
  curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64)" -o MOESM$n.xlsx \
   "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs42004-025-01717-6/MediaObjects/42004_2025_1717_MOESM${n}_ESM.xlsx"
done
# MOESM15 = Supp Data 13 (19.196.393 B) ; MOESM16 = Supp Data 14 (21.114 B) ; MOESM17 = Supp Data 15 (357.224 B)
```

### Supplementary Data 13 (`MOESM15`, sheet `Table 11`) — dự đoán
- **145.461 dòng × 17 cột** `[tự kiểm]`.
- Cột: `Uniprot ID`, `Position`, `Site` (13-mer), rồi **7 cặp** `SIRT<n> Ensemble ML Score` + `SIRT<n> Deacetylation Prediction (0 = no, 1 = yes)`. **0 giá trị thiếu.**
- **2.737 protein** `[tự kiểm]`. **Đây KHÔNG phải "toàn bộ proteome"** như báo cáo viết — proteome người có ~20.400 protein. `[suy luận]` đây là tập lysine acetyl hóa đã biết của 2.737 protein, không phải mọi lysine của mọi protein. 145.461 cặp (protein, vị trí) duy nhất, 142.510 chuỗi 13-mer duy nhất.
- `Position` chạy từ 2 đến **34.271** (trung vị 498) — giá trị 34.271 cho thấy có cả protein khổng lồ (titin).
- **Khoảng điểm (rất khác nhau giữa isoform)** `[tự kiểm]`:

| | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---|---|---|---|---|---|---|
| min | 0,0600 | 0,0335 | 0,0336 | 0,0478 | **0,1612** | 0,0600 | 0,0323 |
| max | 0,9280 | 0,9150 | 0,9493 | 0,8688 | **0,7779** | 0,9273 | 0,9280 |
| trung vị | **0,1280** | 0,3548 | 0,3207 | 0,3742 | 0,3586 | 0,3187 | 0,4159 |
| số dự đoán dương | 3.946 (2,71%) | 40.563 (27,89%) | 39.385 (27,08%) | 30.059 (20,66%) | 39.717 (27,30%) | 18.902 (12,99%) | **52.407 (36,03%)** |

Số isoform được dự đoán dương trên mỗi vị trí: 0 → 25.932; 1 → 50.667; 2 → 43.078; 3 → 17.723; 4 → 5.768; 5 → 1.854; 6 → 428; 7 → 11 `[tự kiểm]`.

**Rò rỉ trong chính file dự đoán này:** **3.226 / 145.461** vị trí có 13-mer **trùng đúng** một 13-mer huấn luyện; và **55.703 vị trí (38,3%)** nằm trên **973 / 2.737 protein** cũng có trong tập huấn luyện `[tự kiểm]`. Nghĩa là nếu dùng Supplementary Data 13 làm baseline so sánh, **phải lọc** 3.226 vị trí đó ra.

**Giá trị cho đề tài:** đúng như báo cáo nói, đây là baseline **có sẵn điểm số từng vị trí**, không cần chạy lại mô hình của họ `[tự kiểm]`.

### Supplementary Data 14 (`MOESM16`, sheet `Table 12`) — tập SIRT2 trong tế bào
- **149 dòng × 8 cột**, **0 giá trị thiếu** `[tự kiểm]`.
- Cột: `Uniprot ID`, `Gene`, `Position`, `Tryptic Peptide Sequence`, `log2(FC) in SIRT2 OE`, `log2(FC) in SIRT2 KD`, `SIRT2 ML-Hybrid Ensemble Score`, `Predicted SIRT2 Deacetylation (0=no, 1=yes)`.
- **149 cặp (UniProt, Position) duy nhất**, **123 protein** duy nhất `[tự kiểm]`.
- **`log2FC` ở OE: cả 149 đều < 0** (min −6,12; max −0,60; trung vị −1,82). **`log2FC` ở KD: cả 149 đều > 0** (min +0,59; max +5,98; trung vị +1,76). Số vị trí thỏa đồng thời OE<0 và KD>0: **149/149** `[tự kiểm]`. **Xác nhận báo cáo: đây là tập chỉ-có-nhãn-dương.**
- Điểm mô hình: **0,0944 – 0,9182**, trung vị 0,4398. Dự đoán dương = **64**, và `score ≥ 0,5` cũng đúng **64** → **ngưỡng là 0,5** `[tự kiểm]`. Precision = 64/149 = **42,95%**, khớp "43,0%" `[tác giả báo cáo]`.
- **Không có cột p-value, không có cột số replicate, không có cột hiệu chỉnh theo mức protein** trong bảng này `[tự kiểm]`. Số replicate và phép kiểm thống kê: `[chưa kiểm]` — phải đọc Methods, chưa làm.

### Supplementary Data 15 (`MOESM17`, sheet `Table 13`)
Đã mô tả ở mục 2: 6.801 × 9, bảng nhãn nhị phân chuẩn kèm 13-mer và UniProt ID. **Đây là file nên dùng làm nhãn**, tốt hơn `labels.csv` vì có kèm chuỗi và thứ tự khớp Rauh.

---

## 5. Tìm tập đánh giá trong tế bào cho isoform thứ hai

### Takeaway
**Tìm được và tải được.** Nguồn tốt nhất không nằm trong 4 accession PRIDE mà báo cáo nêu, mà là **Sol et al. 2012, PLoS ONE 7(12):e50545** — có **hai bảng "tất cả vị trí acetyl hóa được định lượng"** cho SIRT3, một ở chuột, một ở người. Vì bảng liệt kê **mọi vị trí được định lượng** (không chỉ vị trí thay đổi), nó cho **cả nhãn âm**.

### 5.1 Bốn accession PRIDE mà báo cáo nêu — kiểm lại

```bash
curl -sS "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD021357"
```

| Accession | Loài | Mô/tế bào | Can thiệp | PTM khai báo | Bảng vị trí trong PRIDE? |
|---|---|---|---|---|---|
| PXD021357 | **Chuột** | tế bào biểu mô ống thận (xơ hóa thận) | SIRT3 giảm biểu hiện (bệnh lý), không phải KO di truyền | `acetylated residue` | Chỉ `txt.zip` **216,7 MB** (MaxQuant output) + 6 file `.raw` |
| PXD023479 | Người | hMSC (lão hóa tế bào gốc) | SIRT3 thiếu hụt | **"No PTMs are included in the dataset"** | Không phải acetylome vị trí |
| PXD019763 | **Chuột** | tế bào T (TME) | **ức chế** SIRT2 bằng chất ức chế (không KO/KD) | `acetylated residue` | Chỉ `.raw` + `.zip` |
| PXD012796 | **Chuột** | tế bào T | **ức chế** SIRT2 | `Acetyl` | Chỉ `.raw` |

`[tự kiểm, PRIDE API v3]`

**Nhận xét phê phán:** 3/4 là **chuột**, 2/4 là **ức chế bằng thuốc** chứ không phải KO/KD di truyền (chọn lọc thuốc ≠ chọn lọc isoform), và **không accession nào cung cấp bảng vị trí nhỏ gọn** — chỉ có raw file và MaxQuant output cỡ hàng trăm MB. Dùng được nhưng tốn công xử lý lại từ `evidence.txt`/`modificationSpecificPeptides.txt`.

### 5.2 Kiểm kê PRIDE rộng hơn

```bash
curl -sS -G "https://www.ebi.ac.uk/pride/ws/archive/v3/search/projects" \
  --data-urlencode "keyword=SIRT3" --data-urlencode "pageSize=100"
```

Tổng số bộ trả về theo từ khóa, và số bộ có từ acetyl/succinyl/acyl/knockout/deficient trong tiêu đề `[tự kiểm, 08/10/2026]`:

| từ khóa | tổng | lọc được |
|---|---|---|
| SIRT1 | 38 | 9 |
| SIRT2 | 20 | 6 |
| SIRT3 | 31 | **17** |
| SIRT5 | 10 | 8 |
| SIRT6 | 15 | **2** |
| SIRT7 | 10 | 3 |

Các con số này **khác** bảng trong báo cáo ("SIRT1 23, SIRT2 15, SIRT3 24, SIRT5 9, SIRT6 9, SIRT7 7") — `[suy luận]` khác do endpoint/thời điểm/bộ lọc khác, không kết luận bên nào sai.

Ứng viên đáng chú ý chưa khai thác `[tự kiểm, chỉ metadata]`:
- **PXD000885** — *Analysis of acetylation stoichiometry suggests that SIRT3 repairs nonenzymatic acetylation lesions* (Weinert 2015, chuột). PRIDE chỉ có 99 file `.raw` + `MaxQuant_Output.zip` **129,2 MB**. Chính là bài làm nền lập luận "acetyl hóa phần lớn là tổn thương hóa học" trong báo cáo.
- **PXD008728** — *Ablation of Sirtuin5 in the postnatal mouse heart* (SIRT5 KO chuột, succinylome). File xlsx duy nhất là `Hershberger_2018_RawFileDescription.xlsx` (10,7 KB) — **chỉ mô tả raw file, không phải bảng vị trí** `[tự kiểm]`.
- **PXD009509** (SIRT3, chuột cống), **PXD013056** (SIRT3, mỡ nâu chuột — có 2 file `ac-evidence.txt` cỡ 61–76 MB), **PXD061654** (*The mammalian longevity associated acetylome*, chuột).
- **PXD009994** / **PXD005903** — acetylation **stoichiometry** ở tế bào người. `[suy luận]` quan trọng cho lập luận "ngưỡng phát hiện", chưa tải.

### 5.3 Nguồn thực sự dùng được: Sol et al. 2012 (PLoS ONE)

Bài: *Proteomic Investigations of Lysine Acetylation Identify Diverse Substrates of Mitochondrial Deacetylase Sirt3*, PLoS ONE 7(12):e50545 — https://doi.org/10.1371/journal.pone.0050545 (truy cập được, HTTP 200; PLOS **không** bị reCAPTCHA).

```bash
for s in s001 s002; do
  curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64)" -o $s.xlsx \
   "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0050545.$s&type=supplementary"
done
# s001 = Table S1 (1.495.258 B), s002 = Table S2 (940.487 B)
```

**Table S1 — chuột, MEF, Sirt3 knockout (di truyền)** `[tự kiểm]`
- Sheet: `Acetylation sites`, `Protein groups`, `Sites regulated in MEF and U2OS`.
- **1.566 vị trí acetyl hóa được định lượng**, 22 cột, **846 protein**, 1.552 cặp (protein, vị trí) duy nhất.
- Có cột `Sequence window` **13 amino acid** (1.558/1.566 dòng dài đúng 13) — **khớp đúng kích thước cửa sổ của mảng Rauh**, không cần tự dựng.
- **Replicate: 2** (`Experiment 1` 1.303 vị trí, `Experiment 2` 1.196). Định lượng ở **cả hai replicate: 933 vị trí**; chỉ một replicate: **633** `[tự kiểm]`.
- `Combined` = SILAC H/L (Sirt3 KO / WT), có ở **cả 1.566** vị trí. log2: trung vị **−0,041**, phân vị 5% −1,35, 95% +1,12. Tăng >2× : **103** vị trí; giảm >2×: 147; tăng >1,5×: **284**; nằm trong 0,67–1,5× (**ứng viên nhãn âm**): **942** `[tự kiểm]`.
- `[tác giả báo cáo]` "Over one hundred acetylation sites showed more than 2-fold increase in Sirt3 knockout" — khớp 103 `[tự kiểm]`. `[tác giả báo cáo]` tái lập ~60% vị trí ở cả hai replicate, ρ Spearman = 0,75.
- **Hiệu chỉnh theo mức protein: KHÔNG.** Bài ghi rõ: *"protein abundance levels were not substantially altered between the wild-type and Sirt3 knockout cells (Table S1); therefore, individual acetylation ratios provided here were not normalized for protein abundances"* `[tác giả báo cáo]`. Có sheet `Protein groups` để tự kiểm lại.
- **Phép kiểm thống kê ở mức từng vị trí: không có trong bảng.** Bài chỉ báo một phép kiểm **ở mức phân bố** (ty thể vs không ty thể, p = 3,28e-31) `[tác giả báo cáo]`. Không có p-value/FDR theo vị trí `[tự kiểm]`.

**Table S2 — người, U2OS, SIRT3 knockdown so với SIRT3 overexpression** `[tự kiểm]`
- **3.174 vị trí acetyl hóa được định lượng**, 19 cột, **1.498 protein**, 3.168 cặp (protein, vị trí) duy nhất.
- Một cột tỉ lệ duy nhất: `Ratio H/L (Sirt3 knockdown/Sirt3 overexpression)`, có ở **cả 3.174** vị trí. **Chỉ một phép so sánh SILAC, không có cột replicate** `[tự kiểm]` — điểm yếu thống kê rõ ràng.
- log2(KD/OE): trung vị **−0,031**, 5% −1,20, 95% +0,85. >2×: 111; <0,5×: 200; >1,5× (**tăng khi mất SIRT3 → phụ thuộc SIRT3**): **303**; trong 0,67–1,5× (**ứng viên nhãn âm**): **2.456** `[tự kiểm]`.
- Thiết kế KD-vs-OE (không phải KD-vs-WT) nên tỉ lệ là **hiệu ứng kép**, biên độ phóng đại so với KO/WT.

**Đây là bảng dùng được: cùng loài (người) với mảng Rauh, có cửa sổ 13 aa, có cả vị trí thay đổi và không thay đổi.** Đã lưu bản gọn: `data/sol2012-u2os-sirt3kd-sites.csv.gz` (144 KB).

---

## 6. Nhãn dương / âm / chưa xác định, và phê phán về công suất thống kê

### Takeaway
"Không thay đổi đáng kể sau knockout" **không phải bằng chứng mạnh cho không-phải-cơ-chất**, và ở hai bộ dữ liệu này có thể định lượng được tại sao.

### Định nghĩa đề nghị

| Nhãn | Định nghĩa | Số lượng tính được |
|---|---|---|
| **Dương** | định lượng được, tăng rõ khi mất isoform | SIRT2: **149** (Supp Data 14, cả OE và KD cùng chiều) · SIRT3 người: **303** (>1,5×) hoặc **111** (>2×) · SIRT3 chuột: **284** (>1,5×) hoặc **103** (>2×) `[tự kiểm]` |
| **Âm** | định lượng được **trong cùng thí nghiệm** nhưng không đổi | SIRT3 người: **2.456** (0,67–1,5×) · SIRT3 chuột: **942** `[tự kiểm]`. **SIRT2: 0** — Supp Data 14 không liệt kê vị trí không đổi |
| **Chưa xác định** | không được định lượng | mọi lysine còn lại. Tập người chỉ phủ **3.174 / ~145.461** vị trí acetyl hóa đã biết = **2,2%** `[tự kiểm, dùng Supp Data 13 làm mẫu số]` |

### Phê phán: nhãn âm này yếu đến mức nào

1. **Không có phép kiểm cho từng vị trí.** Cả hai bảng Sol 2012 chỉ có tỉ lệ SILAC, **không p-value, không FDR theo vị trí** `[tự kiểm]`. Ngưỡng 1,5× là **ngưỡng tôi tự đặt**, không phải của tác giả. Vì vậy "không đổi" ở đây nghĩa là *"tỉ lệ nằm trong một khoảng tôi chọn"*, chứ không phải *"đã kiểm và không bác bỏ được H0"*.
2. **Công suất rất thấp.** Tập người: **1 phép so sánh SILAC, không replicate** → không thể tính độ biến thiên, không thể tính công suất. Tập chuột: **2 replicate**, và **633 / 1.566 vị trí (40,4%) chỉ được định lượng ở một replicate** `[tự kiểm]`. Một vị trí đo một lần duy nhất rồi gán nhãn âm là nhãn rất yếu.
3. **Nhiễu nền lớn so với hiệu ứng.** Phân vị 5–95% của log2 tỉ lệ là **−1,35 … +1,12** ở chuột và **−1,20 … +0,85** ở người `[tự kiểm]` — tức ±2,2–2,5× chỉ do nhiễu + biến đổi không liên quan SIRT3. Ngưỡng 1,5× (log2 = 0,58) **nằm sâu trong dải nhiễu**. Đây là lập luận định lượng mạnh nhất cho thấy nhãn âm ở đây là nhãn nhiễu.
4. **Giới hạn phát hiện và khu trú.** SIRT3 là enzyme **ty thể**; một vị trí trong nhân không đổi khi mất SIRT3 **không** cho biết gì về đặc hiệu trình tự — nó chỉ cho biết enzyme và cơ chất không gặp nhau. Nhãn âm kiểu này trộn hai nguyên nhân khác hẳn: *"trình tự không phù hợp"* và *"không cùng khu trú"*. `[suy luận]` Nếu dùng làm nhãn âm mà không lọc theo khu trú, mô hình sẽ học khu trú chứ không học đặc hiệu — và đó lại chính là thứ mảng peptide in vitro **không thể** chứa.
5. **Dư thừa (redundancy) và stoichiometry.** Nếu một vị trí bị acetyl hóa ở mức stoichiometry rất thấp, mất SIRT3 có thể không tạo thay đổi đo được dù nó **là** cơ chất. Weinert 2015 (PXD000885) là chỗ để định lượng lập luận này — `[chưa kiểm]`, chưa tải.

**Kết luận phê phán:** nhãn âm ở đây **dùng được nhưng phải khai báo là nhãn yếu**, và nên báo kết quả ở nhiều ngưỡng thay vì một ngưỡng. Khẳng định trong báo cáo rằng đây là "nhãn âm có nghĩa, khác hẳn nhãn âm chưa-từng-thấy" **đúng về nguyên lý nhưng lạc quan quá** so với chất lượng thống kê thực tế của các bảng tải được.

---

## 7. Chồng lấn và rò rỉ

### 7.1 Supplementary Data 14 (SIRT2, 149 vị trí) vs mảng Rauh

| Mức | Số lượng |
|---|---|
| Vị trí có **(UniProt, position) khớp đúng** trong mảng | **44 / 149** `[tự kiểm]` |
| Vị trí nằm trên protein **cũng là protein chính của mảng** | **108 / 149**, thuộc **83 / 123** protein `[tự kiểm]` |
| Vị trí nằm trên protein xuất hiện ở **bất kỳ** accession nào của mảng | **107 / 149** (82 protein) `[tự kiểm]` |
| Protein **hoàn toàn mới** so với mảng | **41 vị trí / 40 protein** `[tự kiểm]` |

Báo cáo ghi "46 trong 149" và "108 vị trí thuộc protein đã từng xuất hiện". **108 khớp đúng; 46 thì tôi đếm được 44** `[tự kiểm]`. Chênh 2 `[suy luận]` do cách khôi phục vị trí từ cột text của Rauh (tôi lấy mọi số trong mọi ngoặc của dòng); không kết luận bên nào đúng.

**Precision của mô hình 2025 tách theo mức chồng lấn** `[tự kiểm]`:
- trên 44 vị trí **có trong mảng**: 23/44 = **52,3%**
- trên 105 vị trí **không có trong mảng**: 41/105 = **39,0%**
- trên 108 vị trí **thuộc protein của mảng**: 48/108 = **44,4%**
- trên 41 vị trí **protein mới**: 16/41 = **39,0%**

`[suy luận]` Chênh 52,3% vs 39,0% là **dấu hiệu rò rỉ ở mức vị trí**: mô hình làm tốt hơn trên đúng những vị trí nó đã thấy nhãn. Chênh ở mức protein nhỏ hơn nhiều (44,4% vs 39,0%). **Nghĩa là con số 43,0% của bài 2025 là con số đã pha rò rỉ, và nếu đề tài muốn một mốc sạch thì mốc đó là 39,0% trên 105 vị trí ngoài mảng** `[tự kiểm]`.

Thêm một con số đáng chú ý: trong 44 vị trí chồng lấn đó, **nhãn SIRT2 của mảng chỉ dương ở 17/44** `[tự kiểm]`. Tức chính mảng peptide đã **bỏ sót 61%** các vị trí phụ thuộc SIRT2 trong tế bào mà nó có đo.

### 7.2 Sol 2012 SIRT3 vs mảng Rauh — và một dạng rò rỉ xuyên loài

| | người U2OS (3.174 vị trí) | chuột MEF (1.566 vị trí) |
|---|---|---|
| Vị trí trên **protein của mảng** | **1.473** (557 / 1.498 protein) | **0** |
| Vị trí có **(UniProt, position) khớp đúng** | **718** | **0** |
| Vị trí có **13-mer khớp đúng** một 13-mer của mảng | **1.417** | **513** |

`[tự kiểm]`

**Phát hiện quan trọng:** tập chuột có **0** chồng lấn ở mức accession/vị trí (accession chuột ≠ accession người), nhưng **513 / 1.566 vị trí (32,8%) có cửa sổ 13 amino acid trùng ĐÚNG TỪNG CHỮ** với một peptide trong mảng. Đó là vị trí **bảo tồn (orthologous)**. `[suy luận]` **"Nguồn độc lập" ≠ "protein độc lập" ≠ "trình tự độc lập".** Một tập "chuột" nghe như độc lập hoàn toàn, nhưng với mô hình chỉ nhìn cửa sổ 13 aa thì một phần ba tập đó là **chính input huấn luyện**, dán nhãn mới. Phải lọc ở mức **chuỗi**, không chỉ ở mức accession.

Tương tự, phải lọc **cùng họ protein**: tôi chưa chạy alignment, nên mức đồng dạng dưới 100% (ví dụ paralog, isoform splice, họ histone, họ tubulin, họ HSP) **`[chưa kiểm]`**. Riêng con số khớp 100% đã là 32,8% ở chuột và 44,6% (1.417/3.174) ở người — cận dưới của mức chồng lấn thật.

Và với chính file dự đoán của bài 2025 (Supplementary Data 13): **3.226 / 145.461** vị trí có 13-mer trùng tập huấn luyện; **55.703 vị trí trên 973 protein** chia sẻ protein với tập huấn luyện `[tự kiểm]`.

### 7.3 Nhãn mảng có chuyển sang trong tế bào không — thử luôn

Đây là phép thử trực tiếp nhất cho RQ2 của đề tài, chạy được ngay vì cả hai bảng đều đã có. So nhãn **SIRT3 của mảng** với **chiều thay đổi acetyl hóa trong tế bào**, trên các vị trí khớp 13-mer `[tự kiểm]`:

**Người (U2OS, KD/OE), n = 1.417 vị trí khớp cửa sổ; nhãn mảng dương 307 (21,7%)**

| ngưỡng "phụ thuộc SIRT3" | số dương trong tế bào | base rate | precision của nhãn mảng | MCC |
|---|---|---|---|---|
| tỉ lệ > 1,2× | 371 | 26,2% | 32,9% | **+0,080** |
| tỉ lệ > 1,5× | 150 | 10,6% | 14,0% | **+0,058** |
| tỉ lệ > 2,0× | 62 | 4,4% | 6,2% | **+0,047** |
| tỉ lệ > 3,0× | 22 | 1,6% | 2,6% | **+0,045** |

**Chuột (MEF, KO/WT), n = 513; nhãn mảng dương 97 (18,9%)**

| ngưỡng | số dương | base rate | precision | MCC |
|---|---|---|---|---|
| > 1,2× | 164 | 32,0% | 33,0% | **+0,011** |
| > 1,5× | 84 | 16,4% | 22,7% | **+0,082** |
| > 2,0× | 22 | 4,3% | 4,1% | **−0,004** |
| > 3,0× | 4 | 0,8% | 0,0% | **−0,043** |

Trên tập chồng lấn chặt hơn (khớp đúng UniProt + vị trí, n = 718 ở người): TP 17, FP 150, FN 59, TN 492 → **MCC = −0,007**, precision 10,2% so với base rate 10,6% `[tự kiểm]`.

**Đọc kết quả này một cách trung thực:** nhãn SIRT3 của mảng peptide in vitro **gần như không mang thông tin** về việc vị trí đó có phụ thuộc SIRT3 trong tế bào hay không, ở mọi ngưỡng tôi thử. MCC cao nhất là +0,082. Đây **không** phải phép đo cuối cùng — nó dùng nhãn nhị phân của mảng chứ không phải mô hình, dùng ngưỡng tôi tự chọn, không hiệu chỉnh khu trú, không hiệu chỉnh mức protein, và bảng người là KD-vs-OE. Nhưng nó đủ để nói: **đừng vào buổi gặp tuần 6 với giả định rằng chuyển miền sẽ thành công.** Phải chuẩn bị trình bày kết quả âm như một kết quả.

---

## 8. Cái gì bị chặn, cái gì chưa kiểm

### Bị chặn (đã thử, ghi mã trả về)
- **`static-content.springer.com`** → **403** cho `MOESM80_ESM.xlsx` của Rauh. Đi được qua **`media.springernature.com`** (200) `[tự kiểm]`.
- **`pmc.ncbi.nlm.nih.gov/articles/instance/.../bin/*.xlsx`** → **HTTP 200 nhưng trả về HTML** `<title>Preparing to download ...</title>` (reCAPTCHA interstitial), 1.817 B cho hai file, 21.395 B cho file thứ ba `[tự kiểm]`. Khẳng định trong nhiệm vụ rằng PMC bị chặn — **xác nhận**, và nó chặn cả Springer/Commun Chem chứ không chỉ PNAS/MCP. Trang HTML của PMC thì tải được bình thường (288.849 B).
- **`ftp.pride.ebi.ac.uk` liệt kê thư mục** → **404** (không cho browse directory). Phải đi qua API `/projects/<acc>/files` để lấy URL từng file `[tự kiểm]`.

### Đi được
`www.nature.com` (200) · `media.springernature.com` (200) · `journals.plos.org` kể cả file phụ lục (200) · `raw.githubusercontent.com` (200) · `www.ebi.ac.uk/pride/ws/archive/v3` (200) · `pmc.ncbi.nlm.nih.gov` HTML (200) `[tự kiểm]`.

### Chưa kiểm / chưa làm
- **Rardin 2013 (PNAS, SIRT3 KO) và Chen 2012 (MCP)** — **chưa thử lại** trong phiên này. Chưa biết publisher site (pnas.org, mcponline.org) có đi được hay không. Đây là việc đáng thử tiếp vì cả hai là acetylome SIRT3 KO kinh điển có bảng vị trí.
- **Weinert 2015 (EMBO J / PXD000885)** — chưa tải phụ lục, chưa tải `MaxQuant_Output.zip` (129 MB). Đây là nguồn cho cả lập luận "tổn thương không do enzyme" và lập luận "ngưỡng phát hiện / stoichiometry". **Nên là việc tiếp theo.**
- **Isoform thứ ba và thứ tư.** Chưa tìm được bảng vị trí mức site cho **SIRT1, SIRT5, SIRT6, SIRT7**. PRIDE có ứng viên (PXD008728 SIRT5 KO tim chuột; PXD061654 acetylome liên quan trường thọ) nhưng **không bộ nào có bảng vị trí nhỏ gọn** — đều phải xử lý lại từ output MaxQuant `[tự kiểm]`.
- **PhosphoSitePlus / CPLM / dbPTM** — chưa thử. Các nguồn này tổng hợp vị trí nhưng `[suy luận]` thường **không** mang fold-change theo thí nghiệm KO, nên có thể không giải được vấn đề nhãn âm.
- **Đồng dạng ở mức họ protein** — chưa chạy alignment (BLAST/CD-HIT/MMseqs2). Các con số chồng lấn ở mục 7 chỉ là **khớp 100%**, tức cận dưới.
- **Số replicate và phép kiểm thống kê của Supplementary Data 14** (Ridgeway 2025) — chưa đọc Methods.
- **Lý do dòng `GIQCVKKRDLEQA` / Q04206 bị loại** — chỉ suy luận, bài không nói.

---

## 9. Việc nên làm ngay, theo thứ tự

1. **Sửa ba chỗ trong [topic-final-recommendation.md](../../reports/topic-final-recommendation.md):** (a) nhãn nhị phân là `efficiency ≥ 1`, không phải `category = 1`, và kéo theo đó luận điểm "ngưỡng cứng làm mất 2.438 vị trí dương yếu của SIRT1" phải viết lại; (b) Supplementary Data 13 là 145.461 vị trí trên **2.737 protein**, không phải "toàn bộ proteome"; (c) chênh 6.802/6.801 là **một dòng cụ thể** (RELA/p65), không phải lỗi đếm.
2. **Dùng Supplementary Data 15 làm nhãn**, không dùng `labels.csv` (thiếu chuỗi, thứ tự cột isoform lộn xộn, thứ tự dòng xáo trộn). Nếu dùng `labels.csv`, join theo `uid_pos`.
3. **Dựng tập đánh giá SIRT3 người** từ Sol 2012 Table S2 (3.174 vị trí, 718 khớp đúng vị trí, 1.417 khớp cửa sổ). Đây là cổng dữ liệu đã **mở được cho isoform thứ hai** `[tự kiểm]`.
4. **Đưa mốc 39,0% (105 vị trí ngoài mảng) vào bên cạnh mốc 43,0% (149 vị trí)** khi so với bài 2025 — vì 43,0% có pha rò rỉ ở mức vị trí.
5. **Lọc rò rỉ ở mức chuỗi, không chỉ accession.** 32,8% tập chuột và 44,6% tập người trùng 13-mer với tập huấn luyện.
6. **Thêm một câu hỏi cho GVHD:** kết quả sơ bộ cho thấy nhãn mảng in vitro gần như không chuyển được sang trong tế bào (MCC ≤ +0,08). Thầy có chấp nhận một luận văn mà kết quả chính là **định lượng mức độ không chuyển được**, kèm phân tích nguyên nhân (khu trú, stoichiometry, công suất thống kê), thay vì một mô hình tốt hơn?

## 10. Nguồn

- Rauh D. et al. (2013), *An acetylome peptide microarray reveals specificities and deacetylation substrates for all human sirtuin isoforms*, Nat Commun 4:2327 — https://www.nature.com/articles/ncomms3327
- Ridgeway N. et al. (2025), *Machine learning-driven prediction of substrates for enzymes introducing or removing protein post-translational modifications*, Commun Chem — https://doi.org/10.1038/s42004-025-01717-6 · [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) · mã: https://github.com/nashirag/ML-Hybrid_Ensemble_Method
- Sol E.M. et al. (2012), *Proteomic Investigations of Lysine Acetylation Identify Diverse Substrates of Mitochondrial Deacetylase Sirt3*, PLoS ONE 7(12):e50545 — https://doi.org/10.1371/journal.pone.0050545
- PRIDE Archive API v3 — https://www.ebi.ac.uk/pride/ws/archive/v3/
- Weinert B.T. et al. (2015), EMBO J — PRIDE [PXD000885](https://www.ebi.ac.uk/pride/archive/projects/PXD000885) `[chưa kiểm nội dung]`
