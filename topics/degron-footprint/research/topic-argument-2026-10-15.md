# Lập luận lại đề tài sau khi đối chiếu y văn — 15/10/2026

> **Đồng bộ 21/10/2026 — bản ghi lịch sử; khối "Trạng thái 21/10/2026" trong [topic-decision.md](topic-decision.md) được ưu tiên khi mâu thuẫn.** Đã lỗi thời sau G2 (18/10) và audit MetaDegron (21/10):
>
> - **Mục 4 (cổng phơi lộ) và mục 7.2 (kiến trúc):** cổng + ΔPAP đạt 0,8002, thua ridge M3 0,8082 và đảo dấu ở seed 29; FiLM, bilinear, cross-ridge cũng thua ridge ở mọi seed — [g2-extension-2026-10-18](g2-extension-2026-10-18/README.md). Cổng không còn là hướng được ủng hộ bằng phép đo.
> - **Mục 3.1 "trục ngữ cảnh chưa bão hòa" (+0,1311 precision@3):** đo trên kernel của PAP; G2 chưa cho thấy mô hình học sâu có ngữ cảnh vượt ridge. Số precision@3 ở đây **không cùng thang** với AUROC mức ô của G2.
> - **Mục 7.1 (câu đóng góp "Chưa có mô hình nào được huấn luyện cho…"):** chuyển sang dạng có điều kiện; [audit MetaDegron](metadegron-analysis-2026-10-21/claims-verification.md) cho thấy ranh giới "mức residue" không độc quyền (Degpred có score residue, Degformer có mutation map).
> - **Mục 7.4 "tính lực trên n = 91 — việc chặn duy nhất":** đã xong ([residue-task-derisk](residue-task-derisk-2026-10-15/README.md), G2); thứ còn mở là đường cong học, tiền huấn luyện nhãn mức túi và Degformer sạch cụm.
> - **MetaDegron (bảng "chỗ đứng", mục 6):** "chỉ trình tự" đúng cho nhánh D; nhánh X dùng ASA/disorder ở đầu vào. Không có 21 head riêng; xem [model-and-evaluation.md](metadegron-analysis-2026-10-21/model-and-evaluation.md).

> Viết lại mạch lập luận của đề tài dựa trên **mọi** thứ đã đo và đã đọc, gồm ba đợt mới nhất:
> [audit dữ liệu đầy đủ](full-data-audit/README.md) (13/10), [baseline PAP + đối chứng ΔPAP](pap-baseline/README.md)
> và [tiền đề kiến trúc](architecture-check/README.md) (14/10), và [tra y văn](architecture-check/prior-art-exposure-gate.md) (14/10).
>
> **Tài liệu phân tích, không phải quyết định.** Phần kết luận ở mục 7 là **đề xuất**, đã ghi vào
> [DECISIONS.md phần C](../../../DECISIONS.md) và **chờ Trọng xác nhận**. Bản thay thế cho mạch lập luận ở
> [topic-decision.md](topic-decision.md) (11/10), vốn viết trước cả ba đợt trên.

## Nhãn bằng chứng

**[đo]** tự đo, có file kết quả · **[nguồn]** số của tác giả, đã đọc toàn văn · **[phân tích]** suy luận ·
**[đề xuất]** chờ xác nhận · **[chưa xác minh]** chỉ thấy qua tóm tắt.

---

## 1. Vì sao phải lập luận lại

Mạch cũ (11/10) có hình dạng: *PAP chỉ dùng thành phần → không tách được vị trí → dư địa 0,1747 → xây mô
hình có ngữ cảnh, điểm mới là cổng phơi lộ đặt ở bước gộp*.

Bốn trong năm mắt của mạch đó nay đã đổi:

| Mắt của mạch cũ | Trạng thái sau ba đợt mới |
|---|---|
| "Dư địa 0,1747 / +28,9%" | **Sai.** Hai mốc 0,6045 và 0,7792 là oracle đọc nhãn test. Số đúng: 0,4897 → 0,6514, dư địa **0,1617** |
| "Điểm mới 1: cổng phơi lộ đặt ở bước gộp" | **Tiền đề không mới** (Voutsinos, Larsen, QCDPred, DEGRONOPEDIA, JoGo), và **hiện tượng đổi dấu Larsen 2025 đã tìm ra**. Thêm nữa: mục 4 dưới đây cho thấy cổng này **không huấn luyện được trên nhiệm vụ chính** |
| "Trần thang điểm khối đã cạn (+0,0032) nên đừng đặt đóng góp ở đó" | **Đúng về kết luận, sai về tầm.** Trên nhiệm vụ residue, cùng thay đổi kiến trúc đó cho **+0,1311** — trục ngữ cảnh **chưa bão hòa** |
| "PAP là baseline phải vượt" | **ΔPAP yếu hơn cả baseline thành phần** (0,4270 so với 0,4884). Baseline phải vượt là 0,4897, và nó **cao hơn mô hình công bố** |
| Cơ chế khoảng trống: 89,7% peptide bị ràng buộc | **Vẫn đúng, không đổi.** Đây là tài sản bền nhất của đề tài |

---

## 2. Trụ thứ nhất: khoảng trống đã chứng minh — **giữ nguyên**

Không có gì trong ba đợt mới làm yếu trụ này. **[đo]**

- **2.353/2.624 peptide (89,7%)** có một nhóm cùng cặp thay thế chứa **cả** vị trí dương và không dương.
  Với những nhóm đó, mô hình chỉ dùng thành phần **bị chứng minh bằng toán** là không thể tách.
- Ràng buộc: `Δf_i(a→b) = f(c − e_a + e_b) − f(c)` — bên phải **không có `i`**.
- Kiểm bằng script: 200 đối chiếu exhaustive, 4.000 kiểm cận rank, phản ví dụ hạng 2.
- Kênh nội PAP bất biến hoán vị: Pearson(gốc, đảo) = **1,000000**.

**[phân tích]** Đây vẫn là điều mà **không ứng viên nào khác trong repo có**: một khoảng trống chứng minh
được, không phải "chưa thấy ai làm". Mọi bản trình bày nên mở bằng trụ này.

---

## 3. Trụ thứ hai, **mới và mạnh**: trục ngữ cảnh chưa bão hòa, và mô hình công bố thua baseline tầm thường

Hai phép đo ngày 14/10 ([pap-baseline](pap-baseline/README.md)) đổi hẳn phần định lượng. **[đo]**

### 3.1 Cùng một thay đổi kiến trúc, hai thang đo cho hai kết luận trái ngược

| Thang đo | `cnn2w1` (kernel 1, chỉ thành phần) | `cnn2w7` (kernel 7, có ngữ cảnh cục bộ) | Chênh |
|---|---:|---:|---:|
| Pearson điểm khối, holdout 428 gene | 0,8690 | 0,8722 | **+0,0032** |
| **precision@3 footprint mức residue** | 0,2959 | 0,4270 | **+0,1311** |

**[phân tích]** Con số +0,0032 là thứ tác giả tự đo và là lý do mạch cũ lo rằng "thêm năng lực bắt ngữ cảnh
gần như không còn gì để ăn". Nhưng nó được đo **trên thang điểm khối**. Trên đúng thang đo của đề tài, cùng
thay đổi đó cho **gấp 41 lần** mức cải thiện. Trần "+0,0032" **không chuyển sang** nhiệm vụ mức residue.

Đây là **bằng chứng dương đầu tiên trong repo** cho hướng mô hình có ngữ cảnh, và nó thay thế cổng phơi lộ
ở vị trí lý lẽ kỹ thuật chính. Giới hạn phải nói kèm: cả hai đều là mô hình **đã công bố**, không phải mô
hình của đề tài; nó nói trục này đáng đi, **không** nói mô hình nào sẽ thắng.

### 3.2 Mô hình degron công bố gần nhất thua baseline thành phần

| Mốc, trên 2.403 peptide, nhãn replicate 2 | precision@3 |
|---|---:|
| Ngẫu nhiên | 0,1232 |
| ΔPAP `cnn2w1` | 0,2959 |
| **ΔPAP `cnn2w7`** | **0,4270** |
| **Baseline thành phần, ước lượng trung thực** | **0,4884** |
| Trần nhãn thực nghiệm | 0,6514 |

Kiểm ghép cặp: ΔPAP `cnn2w7` **thấp hơn** baseline thành phần **−0,0615**, bootstrap 95% [−0,073; −0,049],
Wilcoxon **p ≈ 6 × 10⁻¹⁹**. Không có lợi thế rò rỉ: 0,4268 (protein nằm trong tập train của PAP) so với
0,4270 (không nằm).

**[phân tích]** Hai hệ quả cho cách trình bày:

1. **Mốc cam kết 0,4897 của [D-025](../../../DECISIONS.md#d-025) nằm trên mô hình công bố**, không dưới.
   Nên câu "đề tài phải vượt mốc khó hơn cả state-of-the-art" là **phát biểu đúng**, đo được, và mạnh.
2. **Nhưng phải nói ngay vì sao PAP thua**: PAP được huấn luyện cho **điểm của cả đoạn**, không cho
   **ảnh hưởng đột biến theo vị trí**. Dùng nó qua ΔPAP là **dùng ngoài mục đích**. Không được trình bày
   như "PAP là mô hình tồi" — phải nói là **chưa có mô hình nào được huấn luyện cho đúng nhiệm vụ này**.
   Đó mới là câu dẫn nhập đúng, và nó mạnh hơn.

---

## 4. Phát hiện quan trọng nhất của lần lập luận lại: **cổng phơi lộ không huấn luyện được trên nhiệm vụ chính**

Đây là chỗ mạch cũ sai mà chưa ai phát hiện, kể cả ba báo cáo trước.

**Lập luận. [phân tích]** Toàn bộ nhãn huấn luyện của nhiệm vụ chính là **peptide 28-mer tách rời, gắn vào
đầu C của GFP** — cả bộ quét (256.711 phép đo) và bộ bão hòa (134.608 định danh). Trong thiết kế đó **mọi
peptide đều phơi lộ như nhau**. Nghĩa là rASA và pLDDT **không có phương sai** trên tập huấn luyện chính.

Hệ quả cứng: tham số của cổng phơi lộ **không nhận diện được** từ dữ liệu của nhiệm vụ chính. Cổng chỉ có
phương sai để học khi:

- dùng nhãn **protein nguyên vẹn** (MaveDB) — nhưng đó là **loại nhãn khác** (độ dồi dào, không phải ΔPSI),
  và theo [tra y văn §3](architecture-check/prior-art-exposure-gate.md) thì ở đó đã có baseline mạnh hơn
  (ma trận theo lớp phơi lộ của Schulze 2026; rASA một mình cho Spearman **0,45**);
- hoặc dùng tile của Voutsinos — nhưng tile cũng là **peptide tách rời**, cũng phơi lộ hoàn toàn.

**Kết luận:** thành phần 4 **không thể đóng góp vào G2 trên benchmark chính**. Nó là **cơ chế chuyển giao**
cho nhiệm vụ phụ (suy ra protein nguyên vẹn), không phải thành phần của mô hình chính.

**[phân tích] Ba việc phải sửa theo:**

1. **Bài 6 của hub học** đang gọi cổng phơi lộ là "Điểm mới 1". Phải hạ xuống thành cơ chế chuyển giao, và
   nói rõ nó bất động trên nhiệm vụ chính.
2. **Không dành tuần 7–8 cho cổng phơi lộ.** Dư địa đo được nằm ở **ngữ cảnh vị trí** (+0,1311), không ở
   cấu trúc. Ưu tiên theo đúng chỗ có bằng chứng.
3. **Phép đo ngày 14/10 vì vậy đổi vai**: nó không còn là "kiểm tiền đề của một thành phần kiến trúc" mà là
   **bằng chứng cho phần chuyển giao/thảo luận** — và ở vai đó nó vẫn có giá trị, vì cho thấy mô hình degron
   không có cấu trúc **sai dấu** ở 47% residue của protein nguyên vẹn.

---

## 5. Trụ thứ ba: nên chuyển trọng tâm sang **ma trận thay thế**, vì dư địa lớn hơn trên nhãn sạch hơn

[D-025](../../../DECISIONS.md#d-025) đã chốt bộ bão hòa là nguồn nhãn chính. Hai phép đo 14/10 ủng hộ mạnh
hơn mức lúc chốt, nhưng cũng thêm một điều kiện. **[đo]**

| | Bộ quét (precision@3) | Bộ bão hòa, mức ô (AUROC) |
|---|---:|---:|
| ΔPAP tốt nhất | 0,4270 | **0,7692** |
| Trần nhãn | 0,6514 | **0,9519** |
| **Dư địa** | 0,1617 | **0,1827** |
| Tỉ lệ nhiễu | 75,9% phần dư | **16,7%** phương sai |
| Cỡ mẫu peptide | 2.403 | **91** |

**[phân tích] Bốn điều:**

1. **AUROC là thước đo đúng cho ma trận, không phải Spearman.** Trần Spearman mức ô chỉ 0,6989 còn trần
   AUROC đạt 0,9519: xếp hạng **mọi** ô khó hơn hẳn việc **tách ô dương khỏi ô âm**, và nhiệm vụ của đề tài
   là cái sau. Mạch cũ đặt Spearman làm chỉ số chính — nên sửa.
2. **Dư địa lớn hơn (0,1827) trên nhãn ít nhiễu hơn (16,7% so với 75,9%).** Đây là lý lẽ mạnh nhất để theo
   D-025: không chỉ nhãn sạch hơn, mà chỗ để chứng minh đóng góp cũng rộng hơn.
3. **Nhưng cỡ mẫu thật là 91, không phải 235.** Sau khi áp đúng ngưỡng peptide degron (PSI WT ≤ 3,0), chỉ
   **91/235** peptide còn lại. Đây là **việc chặn duy nhất** còn lại trước khi huấn luyện.
4. **Gộp 19 thay thế lên mức vị trí làm Spearman tăng** (0,3553 → 0,4130), đúng như kỳ vọng nếu nhiễu mức ô
   bị triệt tiêu khi gộp. Nên ứng dụng nên trình bày **cả hai tầng**: ma trận ô để tra chi tiết, bản đồ vị
   trí để đọc nhanh và chắc hơn.

---

## 6. Chỗ đứng so với y văn, phát biểu đúng mức

Tổng hợp từ [tra y văn](architecture-check/prior-art-exposure-gate.md). Đây là phần phải nói trước khi GVHD
hỏi.

### 6.1 Những gì **không** còn là tính mới

| Điều | Ai đã làm | Nhãn |
|---|---|---|
| Degron phụ thuộc mức phơi lộ | Voutsinos 2026 (ρ = −0,47; Kruskal–Wallis P = 5,4 × 10⁻⁶), Larsen 2025 (\|r\| 0,41) | **[nguồn]** |
| ΔPAP đổi dấu giữa vùng gấp và vùng vô định hình | Larsen 2025, trên CRX: **0,54** ở IDR so với **−0,19** ở homeodomain | **[nguồn]** |
| Dùng rASA + pLDDT để phân loại bối cảnh degron | JoGo; DEGRONOPEDIA | **[chưa xác minh]** |
| Gộp nhiều VAMP-seq rồi tách theo chôn/phơi lộ | Schulze & Lindorff-Larsen 2026, 31.614 biến thể, **đúng 6 protein** | **[nguồn]** |
| Attention-MIL trên protein | BioBlobs 10/2025 | **[chưa xác minh]** |
| Dự đoán PSI toàn peptidome | SVM của chính nhóm Zhang, Pearson 0,8955 | **[đo]** từ file Mendeley |

### 6.2 Những gì **chưa tìm thấy tiền lệ**

| Điều | Bằng chứng ngược đã kiểm |
|---|---|
| **Đầu ra là ma trận 28×20 trên nhãn đột biến thực nghiệm** | Cả bốn sản phẩm đều xuất mức **peptide/motif**: DEGRONOPEDIA (annotation motif), MetaDegron (phân loại degron theo E3), PAP/Colab (điểm khối), SVM Zhang (PSI peptide). **[đo]** và **[nguồn]** |
| **Benchmark mức residue có trần nhãn và kiểm soát đồng dạng** | Không bài nào trong sáu bài đã đọc báo **trần nhãn**; PAP chia theo gene nhưng không có trần, Zhang không chia theo protein | **[nguồn]** |
| Cổng phơi lộ **bên trong** mô hình học được, tại bước gộp | PAP: cấu trúc chỉ phân tích sau. **MetaDegron-D: chỉ trình tự**, cấu trúc chỉ vào nhánh XGBoost, không attention, chỉ max-pooling. Schulze: cấu trúc để chia lớp | **[nguồn]** |

**Phát biểu đúng mức, dùng được trước GVHD:** cả ba dòng trên là **chưa tìm thấy sau một lần tra**, không
phải "chưa ai làm". Và theo mục 4, dòng thứ ba **không nên** đặt ở vị trí tính mới chính.

---

## 7. **[đề xuất]** Lập luận mới, và chỗ đặt đóng góp

Ba trụ ở mục 2, 3, 5 dẫn tới một cách đặt đóng góp khác mạch cũ. Đây là **đề xuất**, chờ Trọng xác nhận.

### 7.1 Câu đóng góp, viết lại

> Chưa có mô hình nào được huấn luyện cho nhiệm vụ **ảnh hưởng đột biến degron ở mức residue**: bốn sản
> phẩm đã có đều xuất điểm ở mức peptide hoặc motif. Em dựng **benchmark đầu tiên cho nhiệm vụ đó** — có
> trần nhãn đo được (precision@3 **0,6514**; AUROC mức ô **0,9519**), baseline trung thực (**0,4897**), đối
> chứng là mô hình degron công bố gần nhất (ΔPAP **0,4270**), split theo cụm protein và phân tích lực — rồi
> xây một mô hình **vượt baseline đó**, và một ứng dụng xuất **ma trận 28×20** mà không sản phẩm nào trong
> bốn cái kia xuất.

### 7.2 Vì sao chuyển trọng tâm từ "kiến trúc mới" sang "benchmark + mô hình thắng trên nó"

**[phân tích]** Bốn lý do:

1. **[D-022](../../../DECISIONS.md#d-022) đã gỡ rào**: GVHD **chấp nhận** đóng góp dạng công cụ, thước đo,
   benchmark. Trước ngày 12/10 thì cách đặt này không hợp lệ; nay thì hợp lệ.
2. **Tính mới kiến trúc là chỗ yếu nhất và dễ bị bắt lỗi nhất.** Mọi cơ chế đều có tiền lệ (BioBlobs,
   OmniESI, Ilse 2018), và mục 4 vừa làm mất một trong hai "điểm mới" đã nêu.
3. **Benchmark là chỗ bằng chứng đã có sẵn và đã kiểm.** Trần nhãn, baseline, đối chứng ΔPAP, phân tích
   lực, split cụm — tất cả **đã đo xong** và có file kết quả. Không bài nào trong sáu bài đã đọc có bộ này.
4. **Nó khớp tiêu chí 4 (XAI) sẵn**, vì đầu ra là điểm quan trọng theo residue, và khớp tiêu chí 5 qua ma
   trận 28×20.

**Rủi ro của cách đặt này, phải nhận:** [D-012](../../../DECISIONS.md#d-012) vẫn đòi một **đóng góp dương
đo được** — benchmark một mình **không đủ**. Nên mô hình vượt 0,4897 (hoặc AUROC vượt 0,7692) **vẫn là điều
kiện bắt buộc**, benchmark chỉ là thứ làm cho con số đó có nghĩa. Và GVHD từng nói kỳ vọng "một kiến trúc
chưa ai dùng" (11/10) — nên cần hỏi lại ở buổi gặp (đã có ở C-5).

### 7.3 Năm tiêu chí, đối chiếu lại

| # | Tiêu chí | Sau khi lập luận lại | Đổi gì so với mạch cũ |
|---|---|---|---|
| 1 | Tính mới | Nhiệm vụ và benchmark chưa có tiền lệ; **kiến trúc thì có** | Chuyển chỗ đặt tính mới |
| 2 | Đề xuất/cải tiến phương pháp | Ngữ cảnh vị trí thay gộp trung bình, có **+0,1311 làm bằng chứng trục** | Thay lý lẽ: từ cổng phơi lộ sang ngữ cảnh vị trí |
| 3 | Phương pháp mới | PLM mức residue, không gộp trước | Giữ |
| 4 | XAI | Đầu ra **là** lời giải thích; fidelity đo được bằng footprint thực nghiệm | Giữ, thêm phép đo fidelity |
| 5 | Ứng dụng | Ma trận 28×20 + bản đồ vị trí — **chỗ khác biệt duy nhất đã kiểm** với cả bốn tiền lệ | Mạnh hơn: nay đã kiểm cả bốn |

### 7.4 Thứ tự ưu tiên tám tuần còn lại, theo chỗ có bằng chứng

1. **Tính lực trên n = 91** — việc chặn duy nhất.
2. **Baseline thành phần thật** rồi **mô hình ngữ cảnh vị trí** (chỗ có +0,1311).
3. **Ablation** `B → B + hạng 1 → B + hạng r` trên ma trận, thước đo **AUROC mức ô**.
4. **Ứng dụng** xuất ma trận 28×20 + bản đồ vị trí.
5. **Cổng phơi lộ và nhãn protein nguyên vẹn**: để ở phần chuyển giao/thảo luận, kèm hai đối chứng bắt buộc
   (Schulze 2026, ThermoMPNN). **Không** nằm trên đường găng của G2.

---

## 8. Những gì lần lập luận lại này **không** làm

- **Không** huấn luyện mô hình nào; G2 vẫn chưa xác lập.
- **Không** quyết định — mục 7 là đề xuất, đã ghi vào [DECISIONS.md phần C](../../../DECISIONS.md).
- **Không** đọc toàn văn QCDPred, DEGRONOPEDIA, JoGo (vẫn **[chưa xác minh]**).
- **Không** chạy lại phép đo cổng phơi lộ với hai sửa đã biết (bỏ GCK, dùng homodimer) — xem
  [tra y văn §5](architecture-check/prior-art-exposure-gate.md).
- **Không** sửa `presentation/` theo yêu cầu của Trọng ngày 14/10.
