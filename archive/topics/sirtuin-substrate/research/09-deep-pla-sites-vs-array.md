# 09 — Phép đo chuyển nhãn thứ hai: 289 vị trí curated của Deep-PLA so với nhãn mảng Rauh

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

> Ngày đo: 10/10/2026. Người đo: phiên này, `[tự kiểm]` trừ nơi ghi khác.
> Dữ liệu ra: [`data/deeppla-curated-sites-vs-rauh-labels.csv`](data/deeppla-curated-sites-vs-rauh-labels.csv) (289 dòng).
> Tiếp nối [07](07-deep-pla-hdac-coverage.md) và [08](08-deep-pla-per-isoform-mcc.md). Đây là **phép đo chuyển nhãn thứ hai**, độc lập với phép đo Sol 2012 ở [03](03-data-inventory.md).

## 1. Vì sao phép đo này mạnh hơn phép đo thứ nhất

Phép đo thứ nhất (§03, báo cáo §9) so nhãn mảng Rauh với **sự phụ thuộc SIRT3 trong tế bào** suy ra từ fold-change của Sol 2012 (KD so với OE ở U2OS). Nhược điểm: "dương tính trong tế bào" ở đó là một suy luận từ mức acetyl thay đổi, có thể do hiệu ứng gián tiếp.

Phép đo này so nhãn mảng Rauh với **289 vị trí mà Deep-PLA đã text-mine từ PubMed** — tức là các vị trí đã được báo cáo trong y văn là cơ chất của một sirtuin cụ thể, phần lớn bằng thực nghiệm **trên protein nguyên vẹn hoặc trong tế bào**. Đây là chuẩn vàng gần nhất mà lĩnh vực này có. Nếu nhãn mảng peptide có giá trị dự đoán cơ chất thật, thì trên chính tập này nó phải giàu dương tính rõ rệt.

## 2. Nguồn và cách lấy (giải tỏa điểm nghẽn cũ)

Báo cáo trước ghi "**cần sinh viên tải Supplementary của bbz107**" vì `academic.oup.com` trả 403 với curl trong môi trường cloud. **Điều đó không còn đúng**: `WebFetch` đọc được trang bài báo bình thường; gọi với `offset: 100000` thì nó trả về **URL CloudFront đã ký đầy đủ** (`Expires=…&Signature=…&Key-Pair-Id=APKAIE5G5CRDK6RD3PGA`), và curl với URL đã ký đó trả 200.

| File | Base URL | Kích thước | Mã |
|---|---|---|---|
| `table_s1.xlsx` | `https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/bib/21/5/10.1093_bib_bbz107/7/` | 111.188 B | 200 |
| `table_s4.xlsx` | nt | 1.589.346 B | 200 |
| `table_s5.xlsx` | nt | 12.452 B | 200 |

URL CDN **không có chữ ký** trả `<Error><Code>MissingKey</Code>`. Chữ ký có hạn, nên cách làm này phải lặp lại khi cần tải lại, không lưu được URL.

## 3. Table S1 là gì

1.666 dòng, cột `UniProt | Gene | Position | Type | Sequence Window | Enzyme | Organism | Pmids`. Trong đó 1.171 acetylation, 495 deacetylation; 1.381 *Homo sapiens*, 285 *Mus musculus*. Mọi `Sequence Window` dài **15 aa** (±7).

Lọc `Enzyme ∈ {SIRT1,2,3,6,7}` và `Organism == Homo sapiens` cho **289 vị trí**: SIRT1 185, SIRT2 52, SIRT3 30, SIRT7 12, SIRT6 10.

Con số này **khớp chính xác** với cột P (số dương tính) trên `help.php` đã dùng ở [08](08-deep-pla-per-isoform-mcc.md), và giải thích được chênh lệch ±1 với Table 1 của bài báo (ở đó SIRT1 là 184). Tức là web server và Supplementary nhất quán với nhau, còn Table 1 trong bài in lệch — một chi tiết nhỏ nhưng nên nói nếu GVHD hỏi vì sao hai nguồn khác nhau.

## 4. Cách đối chiếu

Mảng Rauh dùng peptide 13 aa; Table S1 dùng cửa sổ 15 aa. Khớp bằng **13-mer trung tâm**:

```python
def core13(w):
    w = str(w).strip().upper()
    if len(w) == 15: return w[1:14]
    if len(w) == 13: return w
    return None
```

Nhãn dương tính của mảng dùng đúng quy tắc đã xác thực ở [03](03-data-inventory.md): `efficiency >= 1` (tái tạo Suppl Data 15 của Ridgeway ở mức 100,0000%).

Hai đại lượng được đếm cho mỗi vị trí curated có mặt trên mảng:
- `array_label_same_isoform` — mảng có gọi dương tính **cho đúng isoform đó** không;
- `array_label_any_isoform` — mảng có gọi dương tính cho **ít nhất một** trong 7 isoform không.

## 5. Kết quả

**103 trong 289 vị trí (35,6%) có mặt trên mảng.** Trên 103 vị trí đó, mảng gọi dương tính đúng isoform chỉ **16 lần (15,5%)**.

| Isoform | Curated | Trên mảng | Mảng gọi dương đúng isoform | % | Tỷ lệ nền của mảng | Kỳ vọng | Độ giàu | p (binom một phía) |
|---|---|---|---|---|---|---|---|---|
| SIRT1 | 185 | 55 | 2 | 3,6% | 2,6% | 1,4 | 1,41× | 0,418 |
| SIRT2 | 52 | 18 | 5 | 27,8% | 27,9% | 5,0 | 0,99× | 0,595 |
| SIRT3 | 30 | 19 | 6 | 31,6% | 27,1% | 5,2 | 1,16× | 0,414 |
| SIRT6 | 10 | 9 | 2 | 22,2% | 17,6% | 1,6 | 1,26× | 0,489 |
| SIRT7 | 12 | 2 | 1 | 50,0% | 24,9% | 0,5 | 2,01× | 0,436 |
| **Gộp** | **289** | **103** | **16** | **15,5%** | — | **13,7** | **1,17×** | **0,291** |

Dương tính cho **ít nhất một** isoform: 85/103 = 82,5%, so với tỷ lệ toàn mảng 5.695/6.802 = **83,7%** → độ giàu 0,986×. Nghĩa là tập cơ chất đã được y văn xác nhận **không khác gì một mẫu ngẫu nhiên của mảng**.

Kiểm định là binomial chính xác (không xấp xỉ chuẩn, vì n nhỏ), tỷ lệ nền lấy từ chính cột của isoform đó trong mảng.

## 6. Đọc kết quả này thế nào

**Phát hiện chính:** trên những vị trí mà y văn đã xác nhận là cơ chất của một sirtuin cụ thể, mảng peptide Rauh **không giàu dương tính một cách có ý nghĩa** cho đúng isoform đó. Không isoform nào đạt p < 0,05; gộp lại độ giàu 1,17× với p = 0,291.

Đây là **xác nhận độc lập thứ hai** cho kết luận trung tâm của báo cáo (MCC ≈ 0 khi chuyển nhãn in-vitro sang in-cell), và mạnh hơn xác nhận thứ nhất ở hai điểm: (a) dương tính ở đây được xác nhận trên protein cuộn gấp, không suy ra từ fold-change; (b) nó không cần giả định nào về ngưỡng fold-change.

**Nó cũng là chứng cứ bổ sung cho §14:** Deep-PLA huấn luyện trên chính 289 vị trí này, và MCC suy ra từ số của họ là 0,049 cho SIRT3, −0,016 cho SIRT7. Hai nhãn mạnh nhất mà lĩnh vực có — mảng 6.802 vị trí và 289 vị trí curated — không đồng ý với nhau, và cả hai đều cho mô hình yếu. Đó chính là lý do tồn tại của một benchmark chuyển miền.

## 7. Giới hạn phải nói kèm, nếu không GVHD sẽ tìm ra

1. **Chỉ 103/289 (35,6%) vị trí curated có mặt trên mảng.** Phép kiểm chỉ nói về phần giao, tức là bị giới hạn trong cách Rauh chọn 6.802 peptide (họ chọn từ các vị trí acetyl đã biết tại thời điểm 2013). 186 vị trí còn lại không nói được gì.
2. **SIRT7 (n=2) và SIRT6 (n=9) quá nhỏ**, không được trích riêng. Độ giàu 2,01× của SIRT7 đến từ 1 trên 2 vị trí.
3. **Khớp theo 13-mer trung tâm, không theo (UniProt, position).** Cách này bắt được cùng một trình tự ở protein khác (paralog), nên có thể khớp quá rộng vài vị trí. Phiên bản khớp nghiêm ngặt chưa làm `[chưa kiểm]`.
4. Nhãn của Deep-PLA là **text-mining PubMed**, không phải curation thủ công có kiểm tra lại; có thể lẫn vị trí được nêu trong bài mà không phải kết luận thực nghiệm.
5. Không có **âm tính** trong tập 289 này (toàn dương tính), nên không tính được MCC ở đây — chỉ tính được độ giàu so với nền. Đây đúng là vấn đề đã mô tả ở [04](04-evaluation-design.md) về tập chỉ-dương-tính.
