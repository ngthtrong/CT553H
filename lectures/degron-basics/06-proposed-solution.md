[← Bài trước](05-the-gap.md) · Bài 6/10 · [Bài sau: Đánh giá thế nào →](07-evaluation.md)

# Bài 6 — Giải pháp đề xuất: MIL-Degron

> **Đây là ĐỀ XUẤT, chưa kiểm chứng.** Chưa huấn luyện gì cả. Mọi câu trong bài này về hiệu quả của kiến trúc là giả thuyết, không phải kết quả. Nguồn: [topic-decision.md mục 5](../../topics/degron-footprint/research/topic-decision.md), kèm đính chính từ [audit 12/10](../../topics/degron-footprint/research/composition-context-audit.md).
>
> ⚠ **Sửa lớn ngày 15/10/2026.** Bản trước gọi **cổng phơi lộ** là "Điểm mới 1". Khi [lập luận lại](../../topics/degron-footprint/research/topic-argument-2026-10-15.md) đã phát hiện: toàn bộ nhãn huấn luyện chính là **peptide tách rời gắn vào đầu C của GFP**, nên **mọi peptide phơi lộ như nhau** và rASA **không có phương sai** để học — **cổng không huấn luyện được trên nhiệm vụ chính**. Nó đã bị hạ xuống thành **cơ chế chuyển giao** (mục 3). Lý lẽ kỹ thuật chính nay là **ngữ cảnh vị trí**, nơi có bằng chứng đo được: **+0,1311** precision@3 ([bài 5 mục 5.2](05-the-gap.md)). Đề xuất đang chờ Trọng xác nhận: [C-8](../../DECISIONS.md).

---

## 1. Hai khái niệm cần biết trước

### MIL — học đa thể hiện (Multiple Instance Learning)

Tình huống thường gặp: bạn có nhãn cho **cả nhóm** nhưng muốn biết **phần tử nào** trong nhóm gây ra nhãn đó.

> **Ví dụ ngoài sinh học:** bạn có 100 bức ảnh chụp một bệnh viện, và nhãn duy nhất là "trong tập ảnh này có một con mèo". Bạn không biết ảnh nào có mèo. MIL là cách học để vừa đoán được nhãn của cả tập, vừa chỉ ra được **ảnh nào** đóng góp vào nhãn đó.

Thuật ngữ: tập gọi là **túi** (bag), từng phần tử gọi là **thể hiện** (instance).

Áp vào đề tài: **túi = một peptide**, **thể hiện = một cửa sổ quanh mỗi vị trí**. Nhãn đoạn (điểm degron) là nhãn của túi; nhãn vị trí (ΔPSI) là nhãn của từng thể hiện.

### Attention có cổng (gated attention)

Thay vì lấy **trung bình** mọi thể hiện (như PAP làm, và đó chính là chỗ nó mất thông tin vị trí), attention học một **trọng số** cho từng thể hiện rồi lấy trung bình có trọng số. Thể hiện nào quan trọng thì được trọng số cao.

Đây chính là chỗ chữa điểm yếu của PAP ở [bài 5](05-the-gap.md).

---

## 2. Năm thành phần

![Kiến trúc MIL-Degron](figures/fig-10-architecture.svg)

*Sơ đồ tự dựng. Nhãn trên hình ghi rõ: ĐỀ XUẤT, CHƯA KIỂM CHỨNG.*

| # | Thành phần | Phép đo nào buộc phải có nó |
|---|---|---|
| 1 | Mỗi vị trí sinh một cửa sổ ứng viên; peptide là một **túi** cửa sổ | Mô hình hiện có bất biến hoán vị (Pearson gốc–đảo = 1,000000), còn footprint thật khu trú ở trung vị **3/28** vị trí |
| 2 | Embedding PLM **mức residue**, không gộp trước | Mọi mô hình degron đã công bố đều gộp trung bình hoặc chỉ dùng thành phần |
| 3 | **Attention có cổng** thay cho global average pooling | Cấu trúc túi là chỗ nối nhãn **yếu** mức đoạn (212.658) với nhãn **mạnh** mức residue (256.711) trong **một** mô hình |
| 4 | **Cổng phơi lộ**: rASA và pLDDT nhân vào logit attention. ⚠ **Chỉ hoạt động ở chế độ protein nguyên vẹn** — xem mục 3 | Trên protein nguyên vẹn, ΔPAP **đổi dấu** giữa vùng chôn và vùng phơi lộ. Nhưng trên nhiệm vụ chính (peptide tách rời) cổng này **bất động** |
| 5 | **Hai đầu ra**, huấn luyện đa nhiệm: điểm khối (phụ) và **bản đồ theo residue** (mục tiêu) | Nhãn đoạn thì nhiều, nhãn residue là thứ cần đo |

Thành phần **điều kiện E3** của bản thiết kế trước **đã bỏ**, vì chỉ có 1 E3 đủ mẫu — xem [bài 4 mục 5](04-datasets.md).

---

## 3. Cổng phơi lộ: vì sao nó **không** là điểm mới, và vai thật của nó

Đây là phần bị sửa nhiều nhất ngày 15/10. Hai lý do, cả hai đều quan trọng.

### 3.1 Lý do thứ nhất: tiền đề không mới

Bản trước lập luận rằng mọi mô hình trước đưa cấu trúc vào **đầu vào**, còn đề tài đưa vào **logit của
attention**, nên mới ở *nơi đặt*. Phần "nơi đặt" thì vẫn chưa tìm thấy tiền lệ. Nhưng **tiền đề** — rằng
tín hiệu degron phụ thuộc mức phơi lộ — thì **đã được công bố nhiều lần**:

| Ai | Họ đã báo gì |
|---|---|
| [Voutsinos 2026](papers/voutsinos-2026.md) | Điểm degron so với rASA: **ρ = −0,47** trên 173 protein phơi lộ nhất. ΔPAP ở vùng phơi lộ: Kruskal–Wallis **P = 5,4 × 10⁻⁶** |
| [Larsen 2025](papers/larsen-2025.md) | Điểm degron so với rASA \|r\| = **0,41**; so pLDDT \|r\| = **0,36** |
| [Schulze 2026](papers/schulze-2026.md) | Gộp 6 thí nghiệm VAMP-seq, tách chôn/phơi lộ ở rASA **0,1**, dựng ma trận thay thế theo lớp |
| JoGo, DEGRONOPEDIA | Dùng đúng tổ hợp rASA + pLDDT để phân loại bối cảnh degron |

Và quan trọng nhất: **Larsen 2025 đã tìm ra hiện tượng ΔPAP đổi dấu.** Trên CRX, họ báo ΔPAP Pearson
**0,54** trong vùng vô định hình so với **−0,19** trong homeodomain đã gấp. Phép đo của repo ngày 14/10
trên 6 protein MaveDB (−0,19 ở residue chôn, +0,37 ở phơi lộ) là **xác nhận lại ở quy mô lớn hơn trên nhãn
sạch hơn**, không phải phát hiện. Chi tiết: [tra y văn](../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md).

### 3.2 Lý do thứ hai, nặng hơn: cổng **không huấn luyện được** trên nhiệm vụ chính

Đây là lỗi lập luận mà ba báo cáo trước đều không phát hiện.

Nhớ lại [bài 2](02-how-degrons-are-measured.md): mọi nhãn huấn luyện của nhiệm vụ chính đến từ **peptide
28-mer tách rời, gắn vào đầu C của GFP** — cả bộ quét (256.711 phép đo) và bộ bão hòa (134.608 định danh).

Trong thiết kế thí nghiệm đó, **mọi peptide đều phơi lộ như nhau**. Peptide không nằm trong một protein gấp
lại; nó lủng lẳng ở đầu C của GFP. Nên rASA và pLDDT **là hằng số** trên toàn bộ tập huấn luyện chính.

> **Hệ quả cứng:** một cổng nhân rASA vào logit attention sẽ nhân **cùng một con số** vào mọi thể hiện của
> mọi peptide. Tham số của nó **không nhận diện được** từ dữ liệu — không có phương sai để học.

Cổng chỉ có phương sai khi dùng **nhãn protein nguyên vẹn** (MaveDB). Nhưng đó là **loại nhãn khác** (độ
dồi dào, không phải ΔPSI), và ở đó đã có baseline mạnh hơn: [Schulze 2026](papers/schulze-2026.md) cho thấy
**rASA một mình** đạt Spearman **0,45** với độ dồi dào.

### 3.3 Vậy vai thật của cổng là gì

**Cơ chế chuyển giao**, không phải thành phần của mô hình chính:

- Huấn luyện trên **peptide tách rời** → cổng đặt ở "phơi lộ hoàn toàn", bất động.
- Suy ra **protein nguyên vẹn** → cắm rASA thật vào, và cổng mới có việc.

Ý tưởng "cùng một mô hình giải thích cả hai chế độ" **vẫn giữ giá trị** — nó biến khoảng cách
peptide-so-với-protein thành một tham số. Nhưng nó thuộc phần **chuyển giao và thảo luận**, **không nằm
trên đường găng của G2**, và **không nên** dành tuần 7–8 cho nó.

### 3.4 Điểm còn lại: attention giám sát bằng nhãn đột biến theo residue

Thường attention học gián tiếp. Ở đây ta **có** nhãn mức residue nên có thể hướng dẫn nó trực tiếp.

> **Phải nói rõ:** trọng số attention và ảnh hưởng đột biến là **hai đối tượng khác nhau**. Không được gọi
> nhãn đột biến là ground truth trực tiếp của attention, và không được coi riêng cách nối hai thứ đó là một
> phương pháp mới. Cần đối chứng và kiểm giá trị của cách nối này.

## 4. Tính mới **không** nằm ở đâu

Ba điều đã có người làm. Phải nói trước, đừng để GVHD phát hiện:

| Việc | Ai đã làm | Hệ quả |
|---|---|---|
| Attention-MIL trên protein | [BioBlobs](papers/bioblobs-2025.md) (10/2025) — túi là protein, thể hiện là cấu trúc con học được, có cổng attention | **Không được nói "chưa ai dùng MIL cho protein"** |
| Điều biến có điều kiện hai chiều | [OmniESI](papers/omniesi-2025.md) (2025) — cùng ý tưởng với FiLM | Cơ chế không mới |
| Dùng cấu trúc + giải thích biến thể | [Larsen 2025](papers/larsen-2025.md) — đã tính rASA/pLDDT từ AlphaFold2 + DSSP, đã làm bản đồ thay thế *in silico* ΔPAP cho HSF1, **và đã tìm ra hiện tượng ΔPAP đổi dấu trên CRX** (0,54 ở IDR so với −0,19 ở vùng gấp) | **"Dùng cấu trúc" và "giải thích biến thể" không còn là phần mới**, kể cả hiện tượng đổi dấu |
| Gộp VAMP-seq rồi tách theo chôn/phơi lộ | [Schulze 2026](papers/schulze-2026.md) — 31.614 biến thể, **đúng 6 protein** mà repo dùng; rASA một mình cho ρ 0,45 | **Baseline bắt buộc** cho mọi phần dùng nhãn độ dồi dào |
| Dự đoán degron theo từng E3 | [MetaDegron](papers/metadegron-2024.md) (2024) — 21 E3, có máy chủ web | Chiếm cùng khung ứng dụng |

**Câu phát biểu đúng mức:**

> Mới ở **chỗ ghép**, và ở **nhiệm vụ** — chưa có mô hình nào được huấn luyện cho ảnh hưởng đột biến degron
> ở mức residue. **Không mới ở cơ chế**, và **không mới ở việc dùng cấu trúc**.

**Và theo [đề xuất C-7](../../DECISIONS.md), chỗ đặt tính mới nên chuyển hẳn**: từ "kiến trúc mới" sang
"**benchmark mức residue đầu tiên** + mô hình thắng trên nó". Lý do: mọi cơ chế đều có tiền lệ, còn bộ trần
nhãn + baseline + đối chứng + lực + split thì đã đo xong và không bài nào trong sáu bài đã đọc có. Xem
[bài 8](08-contribution.md).

---

## 5. Giới hạn lớn nhất của lập luận MIL — phải tự nói ra

Đây là phản biện mạnh nhất chống lại kiến trúc này, và nó đến từ chính tài liệu của đề tài:

> Khi đã có nhãn ở **mức residue**, thì một **đầu hồi quy theo từng vị trí** là mô hình tự nhiên, và MIL **không còn bắt buộc**.

Nói cách khác: nếu đã biết ΔPSI của từng vị trí, tại sao phải vòng qua cơ chế "túi"? Cứ hồi quy trực tiếp từng vị trí là xong.

**Lý do giữ cấu trúc túi:** để dùng được **cả hai** bộ nhãn trong **một** mô hình. Đầu khối gộp các thể hiện (đọc nhãn đoạn, 212.658 mẫu), đầu residue đọc thẳng từng thể hiện (đọc nhãn vị trí, 256.711 mẫu). Nhãn đoạn nhiều hơn và phủ rộng hơn, nên nó có thể giúp mô hình học biểu diễn tốt hơn.

**Nhưng lợi ích đó chưa được chứng minh bằng thực nghiệm.** Và:

> Nếu phép thử cho thấy một **đầu hồi quy theo vị trí đơn thuần** đã đủ, thì **đó là kết quả phải báo, không phải thất bại cần che**.

Câu trên chép nguyên từ [topic-decision.md](../../topics/degron-footprint/research/topic-decision.md). Nó là một cam kết về tính trung thực, và nên giữ.

---

## 6. Hướng ma trận thay thế — đề xuất của Trọng, 12/10

Ngoài bản đồ 28 chiều, Trọng đề xuất đầu ra là **ma trận vị trí × acid amin thay vào**, học từ cả bộ quét và bộ bão hòa cùng lúc. Audit kết luận: **đáng khảo sát**, nhưng có **ba điều chỉnh bắt buộc**.

**1. Bộ quét là MỘT ô quan sát trên mỗi hàng, không phải marginal.**
Loss phải đọc đúng ô `M[i, b_i]` tương ứng với thay thế thực tế trong CSV. Các ô còn thiếu **không được gán 0** — thiếu dữ liệu khác với "ảnh hưởng bằng 0".

**2. ΔPAP không phải ma trận hạng 1.**
Ngay cả mô hình tuyến tính `f(c) = w·c` cũng cho `M[i,b] = w_b − w_{a(i)}`, là tổng hai outer product, nên hạng tối đa **2**. Có phản ví dụ cụ thể: `w(A,B,C,D) = (0,1,2,3)` cho ma trận con `[[2,3],[1,2]]` có định thức 1, tức hạng 2. Mô hình phi tuyến còn cho hạng cao hơn.

**Bất biến đúng là:** *các hàng cùng residue gốc có cùng đáp ứng khi so cùng cột thay vào* — **không phải** "mọi vị trí có độ nhạy hằng".

**3. Dùng nội bộ tối đa 28 × 20, có mask.**
Mask các ô `WT → WT`, ô stop `*`, và ô thiếu dữ liệu. Giao diện có thể hiển thị 19 thay thế thật trên mỗi residue, nhưng **không được xếp 19 cột khác nhau ở từng hàng rồi phân rã như thể chúng cùng identity**.

**Không gian thiết kế trung thực được đề xuất:**

```
M[i,b] = B(c, a_i, b)  +  Σ_q U[i,q](sequence) · V[b,q](sequence)
```

trong đó `B` là nhánh baseline chỉ dựa thành phần, phần sau là **hiệu chỉnh theo ngữ cảnh**.

**Thang ablation bắt buộc:** `B` → `B + hiệu chỉnh hạng 1` → `B + hạng r cao hơn`, với **cùng split và cùng ngân sách tính toán**. Giữ thêm đối chứng decoder theo vị trí/thay thế không phân rã.

> **Cảnh báo về khả năng nhận diện:** với chỉ một ô quan sát mỗi hàng, các nhân tố `U` và `V` **không tự nhận diện được**. Cần chia sẻ tham số giữa các peptide / loại acid amin, hoặc một prior, hoặc nhãn bão hòa đủ chất lượng để kiểm chứng.
>
> Và: **không nói "chưa ai làm ma trận thay thế cho degron"**. Dự đoán ô thay thế còn thiếu đã có tiền lệ ngoài degron, ví dụ [khung DMS targeted substitution profiling 2026](https://pubmed.ncbi.nlm.nih.gov/42157089/).

---

## 7. Đối chứng bắt buộc

Không được chỉ so với PAP. Ba đối chứng phải có:

1. **ΔPAP tính trên đúng thay thế thực nghiệm** — **đã chạy ngày 14/10**: precision@3 **0,4270**, AUROC mức ô **0,7692**. Xem [pap-baseline](../../topics/degron-footprint/research/pap-baseline/README.md).
2. **Mô hình thành phần** — mốc **0,4897** (không phải 0,6045, vốn là oracle).
3. **Đầu hồi quy theo vị trí, không MIL** — đối chứng quan trọng nhất, vì nó kiểm trực tiếp giới hạn ở mục 5.
4. **Chỉ cho phần dùng nhãn độ dồi dào protein nguyên vẹn:** ma trận thay thế theo lớp phơi lộ của [Schulze 2026](papers/schulze-2026.md) **và** ThermoMPNN ΔΔG. Hai cái này là **bắt buộc**, không phải tùy chọn — chính tác giả đề nghị dùng ma trận của họ làm baseline.

> Lưu ý về các oracle và cận ở [bài 5](05-the-gap.md): chúng dùng **nhãn đánh giá**, nên **không phải** performance đã đo của các baseline này. Đừng trộn hai loại con số.

---

[← Bài trước](05-the-gap.md) · [Bài sau: Đánh giá thế nào →](07-evaluation.md)
