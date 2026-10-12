# Bài toán 7 isoform có còn khả thi không — đo trực tiếp từ Supplementary Data 5 và 6 của Rauh

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

**Ngày đo:** 08/10/2026. **Câu hỏi của sinh viên:** dự đoán cơ chất cho cả 7 isoform SIRT1–7 có còn khả thi không?

**Trả lời một dòng:** khả thi **không đồng đều**, và lý do không phải thiếu dữ liệu mà là **nhãn của các isoform không cùng thang đo**. Số nhãn dương của một isoform tương quan mạnh với **lượng enzyme được nhỏ lên mảng**, không chỉ với đặc hiệu sinh học của nó.

## 1. Phép đo chính: lượng enzyme vs số nhãn dương

Nguồn: Rauh 2013 Supplementary Data 5 ("Experimental conditions"), cột `Protein concentration [µg/ml]` và `Protein (amino acids)`; nhãn từ Supplementary Data 1, quy tắc dương `efficiency ≥ 1` (xem [03-data-inventory.md](03-data-inventory.md) §quy tắc nhãn). Tải qua `media.springernature.com`, file `MOESM84` (Data 5), `MOESM85` (Data 6), `MOESM80` (Data 1).

| Isoform | Nồng độ enzyme, trung vị (µg/ml) | Dải | Số mảng trong Data 5 | Nhãn dương | % dương | `ratio error` trung vị |
|---|---|---|---|---|---|---|
| SIRT1 | 20 | 20–125 | 22 | 176 | 2,6% | **0,370** |
| SIRT2 | 115 | 20–115 | 14 | 1.901 | 27,9% | 0,220 |
| SIRT3 | 24 | 10–135 | 16 | 1.844 | 27,1% | 0,240 |
| SIRT4 | 10 | 10–20 | 8 | 1.038 | 15,3% | 0,240 |
| SIRT5 | **218** | 6–218 | 6 | **2.615** | 38,4% | 0,210 |
| SIRT6 | 60 | 20–100 | 4 | 1.199 | 17,6% | 0,270 |
| SIRT7 | 20 | 20 | 8 | 1.692 | 24,9% | 0,220 |

Bảng số: [data/rauh2013-enzyme-amount-vs-positives.csv](data/rauh2013-enzyme-amount-vs-positives.csv).

**Tương quan `[tự kiểm]`:** Spearman ρ = **+0,811** giữa nồng độ enzyme trung vị và số nhãn dương (n = 7 isoform); **p = 0,0349** hai phía bằng kiểm định hoán vị đầy đủ (176/5.040 hoán vị có |ρ| ≥ giá trị quan sát). Pearson r = +0,719. Ngoài ra Spearman(số nhãn dương, `ratio error` trung vị) = **−0,855**: isoform nào được nhỏ ít enzyme thì vừa ít nhãn dương vừa nhiễu đo cao hơn.

**Hai phản biện với chính phép đo này, phải nói kèm:**

1. **n = 7, nên tương quan này là tín hiệu, không phải bằng chứng quyết định.** Với bảy điểm, một hoán vị đủ mạnh cũng ra p < 0,05 không khó; p = 0,0349 nằm sát ngưỡng.
2. **Nồng độ enzyme không giải thích hết.** SIRT1 và SIRT7 **cùng** ở 20 µg/ml nhưng có **176** so với **1.692** nhãn dương — chênh gần 10 lần. Vậy ngoài lượng enzyme còn ít nhất một yếu tố khác (hoạt tính nội tại, hoặc thiên lệch kháng thể theo trình tự mà chính Rauh nêu). Nói "cột SIRT5 chỉ là nồng độ enzyme" là **nói quá**; phát biểu đúng là *lượng enzyme là một biến gây nhiễu có cỡ hiệu ứng lớn và chưa ai hiệu chỉnh*.

Thêm nữa, Data 5 cho thấy mỗi isoform được thử với **nhiều construct khác nhau** (ví dụ `hSirt1 (1-747)` và `hSirt1 (225-664)`; `hSirt3 (114-380)` và `(114-399)`; `hSirt7` có ba đoạn `(1-400)`, `(14-367)`, `(81-356)`), cộng các đột biến bất hoạt làm đối chứng (`hSirt1 H363A`, `hSirt3 H248Y`, `Sirt7 H188Y`). Nên "nồng độ trung vị theo isoform" là một phép gộp thô: nó gộp các construct và điều kiện ủ khác nhau. Muốn chặt hơn phải tách theo từng cặp (construct, mảng), chưa làm `[chưa kiểm]`.

## 2. Supplementary Data 6: mối lo "nhãn âm thật ra là không đo được" **không thành**

Data 6 = "Peptides that yielded no significant signal in at least one control experiment": **220 peptide**, tất cả **220/220 đều có mặt trong Supplementary Data 1**, tức chúng **không bị loại** khỏi bộ nhãn `[tự kiểm]`.

Nhưng chúng **không** bị gán âm một cách hệ thống:

| | Dương ở ≥ 1 isoform | Tỉ lệ |
|---|---|---|
| 220 peptide của Data 6 | 185 | **84,1%** |
| Toàn bộ 6.802 vị trí | 5.695 | **83,7%** |

Hai tỉ lệ gần như trùng nhau, nên **giả thuyết "một phần nhãn âm nghĩa là không đo được" bị bác bỏ ở mức tổng thể** `[tự kiểm]`. Đây là đính chính cho mối lo nêu ở [01-biology-and-labels.md](01-biology-and-labels.md) §8 — mối lo hợp lý, nhưng số liệu không đỡ nó. Chỉ **35/220** peptide âm ở cả bảy isoform, và 220 trên 6.802 là 3,2% tổng số, nên dù có xử lý thì ảnh hưởng tối đa cũng nhỏ.

## 3. Hệ quả cho câu hỏi "7 isoform còn khả thi không"

Khả thi theo ba mức, không phải một:

- **SIRT1, SIRT2, SIRT3 — khả thi.** Khung deacetylase đúng về enzymology; có bằng chứng ở mức protein nguyên trong chính bài Rauh (SIRT1→HMGB1 K12, SIRT3→MDH); có tập đánh giá trong tế bào (SIRT2: Zhang 2022; SIRT3: Sol 2012). Cặp đồng dương mạnh nhất là SIRT2–SIRT3.
- **SIRT1 là ca xấu nhất về dữ liệu, không về sinh học.** 176 nhãn dương (2,6%), `ratio error` cao nhất (0,370), và ở nồng độ enzyme thấp. Giữ được, nhưng mọi chỉ số phải kèm khoảng tin cậy, và conformal theo lớp cho SIRT1 gần như không đủ mẫu (xem [05-conformal-and-xai.md](05-conformal-and-xai.md)).
- **SIRT4, SIRT5, SIRT6, SIRT7 — không khả thi như một bài toán "dự đoán cơ chất deacetyl hóa".** Lý do không phải thiếu nhãn (SIRT5 có nhiều nhãn dương nhất) mà là nhãn **đo một thứ khác**: bốn isoform này có hoạt tính deacetylase rất yếu (Mathias 2014, Jiang 2013), SIRT6/SIRT7 cần nucleosome nên mảng peptide tự do là bối cảnh sai, và SIRT5 vừa là isoform được nhỏ nhiều enzyme nhất (218 µg/ml) vừa là isoform mà sinh học nói không nên có nhiều cơ chất acetyl.

**Đề nghị:** giữ **SIRT1/2/3** làm phần định lượng, và đưa SIRT4–7 vào luận văn như một **phân tích giới hạn của nhãn** — trong đó bảng ở §1 và tương quan ρ = +0,811 chính là nội dung, không phải lời xin lỗi. Đây là cách duy nhất mà "7 isoform" còn xuất hiện trong luận văn một cách trung thực.

## 4. Tái lập

```
# Data 1 = MOESM80, Data 5 = MOESM84, Data 6 = MOESM85 (Supplementary Data 1–7 = MOESM80–MOESM86)
curl -o MOESM84.xlsx \
 "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms3327/MediaObjects/41467_2013_BFncomms3327_MOESM84_ESM.xlsx"
```
Cột nhãn trong Data 1: 4 cột mỗi isoform theo đúng thứ tự SIRT1→SIRT7 (`substrate category`, `signal ratio (exp:ref)`, `ratio error`, `efficiency`) ở các chỉ số cột 1–28, hàng tiêu đề 3 và 4, dữ liệu từ hàng 5. Quy tắc dương: `efficiency ≥ 1`.
