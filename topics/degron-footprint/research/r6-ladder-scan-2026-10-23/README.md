# R6 — Chuỗi đối chứng biểu diễn × đầu mạng, ngữ cảnh rộng và bộ scanning — 23/10/2026

**Trạng thái: ĐÃ CHẠY trên Kaggle (23/10/2026, 2×T4), đủ 8 giai đoạn, 23/23 cấu hình, 12/12 cổng đạt.** Kết quả ở [run-kaggle-20261023/](run-kaggle-20261023/) và **mục 3** bên dưới; mục 1–2 là phần viết **trước** lượt chạy, giữ nguyên làm bản ghi (kể cả hai kết quả ridge giai đoạn A, B đã thấy từ lượt thử cục bộ, PROTOCOL §12 — lượt Kaggle cho đúng cùng số). Kết luận ngắn: **phép xác nhận duy nhất (P) không đạt** (chưa đủ bằng chứng); điều mới duy nhất được nhận ở mức họ là **ridge ngữ cảnh ±5**.

Tiêu chí, họ kiểm định, siêu tham số và dự đoán ghi trước: [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Không đổi trạng thái G2/G3.

## Câu hỏi

Sáu câu (Q1–Q6, PROTOCOL §1; thứ tự chạy 0, A, B, C, D, E, F, G), trong đó **một** phép xác nhận duy nhất: **ESM-2 35M đóng băng + mCNN (3,5,7) có hơn ridge M3 ext 4,0 (0,8208) không?** Các hướng khác là câu hỏi họ có hiệu chỉnh Bonferroni hoặc mô tả:

1. Ridge với ngữ cảnh WT rộng hơn ±3 (A).
2. Trộn bộ **scanning** (4.802 peptide, 2.902 cụm) vào huấn luyện — với ridge (B) và với mạng (G).
3. ESM-2 8M/35M/150M/650M cộng vào ridge (D), và quét cỡ với mCNN (F).
4. One-hot CNN/mCNN (đối chứng cùng đầu) và ESM + CNN/mCNN (E).

## 1. Có trộn được scanning với bão hòa không? — phép kiểm chéo mô tả `[ĐO]`

Ngoài PROTOCOL, trước khi chốt (PROTOCOL §0 ghi rõ điều này). Trên **cùng ô** (peptide, vị trí, acid amin thay) có mặt ở cả hai bộ — 42/88/117 peptide ở ngưỡng PSI(WT) ≤ 3,0/≤ 4,0/không ngưỡng; chỉ có ô thay bằng R/A/S vì scanning chỉ có ba loại này ([cross-source-audit.json](cross-source-audit.json), sinh bởi [cross_source_audit.py](cross_source_audit.py)):

| Ngưỡng PSI(WT) | Ô trùng | Pearson ΔPSI | κ nhị phân (ΔPSI ≥ 1) | AUROC gộp: ΔPSI scanning → ô dương bão hòa | Tham chiếu: nửa A bão hòa → nhãn nửa B (cùng ô) |
|---|---:|---:|---:|---:|---:|
| ≤ 3,0 | 1.172 | 0,79 | 0,75 | 0,947 | 0,950 |
| ≤ 4,0 | 2.449 | 0,74 | 0,69 | 0,922 | 0,966 |
| không ngưỡng | 3.228 | 0,70 | 0,65 | 0,905 | 0,968 |

- `[DIỄN GIẢI]` **Nhãn hai bộ nhất quán trên cùng ô, và thang WT trùng nhau**: ở ngưỡng 3,0 scanning cho thứ hạng ô dương bão hòa tốt ngang một replicate bão hòa khác; chênh PSI(WT) trung bình giữa hai nguồn chỉ −0,01 đến +0,13. Độ nhất quán giảm khi nới vùng PSI(WT), và độ dốc OLS 0,70–0,77 cho thấy scanning (một replicate) nhiễu hơn.
- `[ĐO]` **Đính chính một diễn giải ở [r3-domain-gate/README.md](../r3-domain-gate-2026-10-22/README.md) mục 1:** độ lệch ≈ 0,9 PSI là giữa **sàng peptidome GPS** và (cả bão hòa lẫn scanning `_mut0`), **không** phải giữa scanning và bão hòa. Các con số của R3 không đổi; chỉ câu "bão hòa cao hơn **cả hai** thang kia" là không đúng với thang scanning.
- `[ĐO]` Thách thức còn lại không phải nhãn mà là **độ phủ thay thế**: scanning chỉ có R (64%), A (23%), S (12%), tức 3/19 loại thay thế của ô test; ridge học chỉ trên scanning chuyển sang bão hòa đạt 0,7273 ([residue-task-derisk](../residue-task-derisk-2026-10-15/README.md) §5) so với 0,8082 khi học trực tiếp trên bão hòa.
- `[ĐO]` **Thang WT trùng về trung bình nhưng phân tán theo peptide**: Pearson giữa PSI(WT) hai nguồn chỉ 0,58/0,63/0,79 (≤ 3,0/≤ 4,0/không ngưỡng); audit song song của phiên khác ghi 31% peptide lệch > 0,5 PSI ở mốc WT. Nên ΔPSI scanning là nhãn **cùng tín hiệu, không cùng thang** (độ dốc OLS 0,70–0,77).
- `[ĐO]` **Một phiên khác đã chạy sẵn phép trộn bằng ridge và một mạng** — [scan-sat-merge-2026-10-23](../scan-sat-merge-2026-10-23/PROTOCOL.md), có PROTOCOL riêng chốt trước khi chạy; **tôi không viết và chưa tái lập số của nó** (một tiến trình của phiên đó còn đang chạy lúc tôi đọc). Theo `results.json` ở đó, trên đúng outer-test 91 peptide, mốc A1 = ridge ext 4,0 = 0,8208: chỉ-scanning 0,7277; gộp mù (S1) 0,8189; gộp có khối riêng nguồn (S2) 0,8203 (Δ −0,0005, CI [−0,0009; −0,00004]); tiên nghiệm (S3) 0,8197; mạng `gate_no_pap` từ đầu 0,8154 so với tiền huấn luyện trên scanning 0,8168. **Không biến thể ridge nào hơn A1.**
- `[DIỄN GIẢI]` Câu trả lời cho "có trộn được không": **trộn được về mặt nhãn (không rò, nhãn nhất quán), nhưng với ridge M3 thì không thêm lợi ích đo được**; với mạng mới chỉ có một phép đo nhỏ, chưa phân định. Giai đoạn B của R6 là lặp độc lập rẻ tiền; giai đoạn G (mạng mCNN/ESM + scanning) được đặt **cuối cùng** vì kỳ vọng thấp nhất (PROTOCOL §0). Hàng scanning thuộc cụm outer-test bị loại ở từng fold (**61/89 cụm bão hòa của bộ 91 peptide cũng có trong scanning**, nên điều này loại một phần đáng kể).

## 2. Điều đã thấy trước khi Trọng chạy lượt chính thức (PROTOCOL §12) `[ĐO]`

Nguồn: [dryrun-local-stageAB.json](dryrun-local-stageAB.json) (CPU, 3 seed × 5 fold, đúng mã và tiêu chí của notebook). **Không phải lượt chính thức** nhưng ridge tất định nên lượt Kaggle phải trùng đến sai số làm tròn; vẫn nên chạy để có `env.json`/`gates.json` của nền tảng.

| Cấu hình | AUROC | Δ so với ridge M3 (0,8208) | CI (Bonferroni nếu m>1) | Ba seed | Kết luận theo §6 |
|---|---:|---:|---|---|---|
| ridge ngữ cảnh **±5** | **0,8286** | **+0,0078** | [+0,0021; +0,0139] (m=3) | dương | **nhận** (họ A) |
| ridge ±7 | 0,8255 | +0,0046 | [−0,0028; +0,0121] | dương | chưa đủ bằng chứng |
| ridge ±10 | 0,8182 | −0,0026 | [−0,0117; +0,0067] | không đồng nhất | chưa đủ bằng chứng |
| ridge + scanning `pool` (ngưỡng 4,0) | 0,8138 | −0,0071 | [−0,0157; +0,0020] (m=2) | âm | chưa đủ bằng chứng |
| ridge + scanning `prior` (ngưỡng 4,0) | 0,8190 | −0,0018 | [−0,0040; +0,0004] (m=2) | âm | chưa đủ bằng chứng |

- `[DIỄN GIẢI]` **Ngữ cảnh ±5 là cải thiện thật đầu tiên của ridge kể từ P0** (+0,0078 so với +0,0126 của P0), nhưng đường cong không đơn điệu (±10 kém hơn ±3): lợi ích nằm ở vị trí ±4–±5, không phải "càng rộng càng tốt". Giả thuyết trước đó (dự đoán (a): không độ rộng nào "nhận") **sai**. Hệ quả: M3 không còn là ridge mạnh nhất; PROTOCOL §12 thêm phép so phụ mạng − `ridge_W5` và ghi hệ quả cho R5.
- `[DIỄN GIẢI]` **Scanning không giúp ridge**, khớp với phiên khác (mục 1): hai cách trộn đều ≤ ridge M3 ext, CI phủ 0. Ngưỡng scanning 3,0 cho kết quả cùng hướng (0,8173/0,8192).
- `[ĐO]` Lượt thử còn chạy C–G ở quy mô thu nhỏ (ESM-2 8M thay cho cả bốn cỡ — nên điểm ridge+ESM của bốn cỡ trong lượt đó giống nhau và **không** được báo; mạng 1 seed × 1 fold × 2 epoch) chỉ để chắc đường code. Chưa có điểm nào của `esm35_mcnn` hay các mạng khác có giá trị.

## 3. Kết quả lượt Kaggle chính thức `[ĐO]`

Nguồn: [run-kaggle-20261023/results.json](run-kaggle-20261023/results.json) (kết luận theo PROTOCOL §6, cài trong `r6stats.verdict`), [gates.json](run-kaggle-20261023/gates.json), [env.json](run-kaggle-20261023/env.json); phần **hậu kiểm** ở [posthoc-r6.json](posthoc-r6.json) (sinh bởi [posthoc_r6.py](posthoc_r6.py), tái tổng hợp từ OOF khớp `results.json` đến 0). Kiểm provenance: SHA-256 của năm file `.py` trong `results.json` **trùng** file trong repo; SHA PROTOCOL trùng bản nhúng trong notebook; gói mã dựng từ commit `f76ab59` **dirty** (ghi trong `env.json`; nội dung mã đã băm nên không lệch). Cổng: 12/12 đạt; ridge M3 tái lập P0 đến 0; ridge+ESM 650M lệch R2 9e-7; độ lệch trích lại embedding fp16 là 0,0045/0,0087/0/0 (8M/35M/150M/650M) — **35M sát dung sai 0,01**. Chạy ≈ 1 giờ 25 phút (07:22–08:47 UTC theo dấu thời gian), ít hơn ước lượng cũ (E/F/G ước 2,4 giờ).

### 3.1 Bảng chính (AUROC macro theo peptide, ensemble ba seed; mốc ridge M3 = 0,8208)

| Cấu hình | AUROC ens. | Trung bình từng seed | Δ so đối chứng của họ | CI dùng kết luận | Kết luận §6 |
|---|---:|---:|---:|---|---|
| ridge ±5 (A) | 0,8286 | 0,8285 | +0,0078 | [+0,0021; +0,0139] (m=3) | **nhận** (ba seed + ) |
| ridge ±7 (A) · ±10 (A) | 0,8255 · 0,8182 | | +0,0046 · −0,0026 | [−0,0028; +0,0121] · [−0,0117; +0,0067] | chưa đủ bằng chứng |
| ridge + scanning `pool` · `prior` (B) | 0,8138 · 0,8190 | | −0,0071 · −0,0018 | [−0,0157; +0,0020] · [−0,0040; +0,0004] (m=2) | chưa đủ bằng chứng (cả ba seed âm) |
| ridge + ESM 8M/35M/150M/650M (D) | 0,8214/0,8234/0,8207/0,8230 | | +0,0006/+0,0026/−0,0001/+0,0022 | rộng nhất [−0,0084; +0,0100] (m=4) | không cỡ nào nhận; CI 95% đều trong ±0,01 |
| `oh_cnn1` · `oh_mcnn` | 0,8127 · 0,8168 | 0,8051 · 0,8086 | −0,0081 · −0,0040 (so M3) | [−0,0173; +0,0014] · [−0,0135; +0,0055] | chưa đủ bằng chứng |
| `esm35_cnn1` | 0,8264 | 0,8181 | +0,0056 (so M3) | [−0,0061; +0,0186] | chưa đủ bằng chứng |
| **`esm35_mcnn` (P, chính)** | **0,8305** | 0,8222 | **+0,0097** (so M3) | **[−0,0025; +0,0233]** | **chưa đủ bằng chứng**; Δ từng seed +0,0076 / −0,0008 / −0,0026 |
| `esm8` · `esm150` · `esm650` + mCNN (F) | 0,8265 · 0,8212 · 0,8243 | 0,8193 · 0,8131 · 0,8141 | −0,0040 · −0,0092 · −0,0062 (so 35M) | rộng nhất [−0,0199; +0,0066] (m=3) | chưa đủ bằng chứng; **35M cao nhất nhưng đã chọn trước** |
| `oh_mcnn` + scan `pool` · `ft` (G) | 0,8242 · **0,8315** | 0,8150 · 0,8216 | +0,0073 · **+0,0147** (so tự đầu) | [−0,0107; +0,0254] · **[+0,0027; +0,0276]** (m=4) | `pool`: chưa đủ · **`ft`: nhận** (ba seed +) |
| `esm35_mcnn` + scan `pool` · `ft` (G) | 0,8367 · 0,8299 | 0,8237 · 0,8231 | +0,0062 · −0,0006 | [−0,0086; +0,0211] · [−0,0122; +0,0109] | chưa đủ bằng chứng |

Phép phụ (mô tả, m=1): **S1** `esm35_mcnn` − `oh_mcnn` = **+0,0137** [+0,0025; +0,0262], ba seed dương ⇒ nhận; **S8** `oh_mcnn` − `ridge_W5` = **−0,0118** [−0,0226; −0,0012] ⇒ âm; **S7** `esm35_mcnn` − `ridge_W5` = +0,0019 [−0,0115; +0,0164], seed +0,0004 / −0,0085 / −0,0108 ⇒ chưa đủ; S5/S6 (mCNN − CNN1) = +0,0041/+0,0041, trong ngưỡng không phân giải được. Hệ quả §6/§12 cho R5: **P không nhận ⇒ mô hình sản phẩm không đổi sang mạng**; mạng cũng không vượt `ridge_W5` (S7).

### 3.2 Điều đo thêm, ngoài tiêu chí chốt trước `[ĐO]` (hậu kiểm, chỉ mô tả — [posthoc-r6.json](posthoc-r6.json))

1. **Ensemble ba seed làm phồng điểm mạng, không làm phồng ridge.** Cùng một mạng, ensemble hơn trung bình từng seed **+0,007 đến +0,013** (`esm35_mcnn` +0,0083; `esm35_mcnn+scan_pool` +0,0130; `oh_mcnn+scan_ft` +0,0099), còn ridge +0,0000…+0,0016 (seed chỉ đổi cách chia train/val). Bởi vậy Δ của P (+0,0097) gần như **toàn là giảm phương sai**: mạng đơn lẻ so ridge M3 chỉ +0,0014 và **so `ridge_W5` là −0,0063** (CI 95% [−0,0195; +0,0079]). Bốn cấu hình mạng tốt nhất đều **dưới** `ridge_W5` khi không ensemble ở 11/12 lượt (−0,0020…−0,0120; ngoại lệ duy nhất `esm35_mcnn` seed 17: +0,0004). Dao động giữa seed của một mạng (đến 0,016, vd `esm650_mcnn` 0,8086–0,8245) lớn hơn mọi hiệu giữa cấu hình mạng, nên một lượt đơn không xếp hạng được cấu hình.
2. **Δ của P không phải do vài peptide**, khác R2: 63% peptide dương, trung vị +0,0099; nhưng phân bố đuôi nặng hai phía (5 peptide tốt nhất cộng +0,0092 vào trung bình, 5 xấu nhất −0,0059; bỏ 5 tốt nhất thì Δ còn +0,0004). So với `ridge_W5` thì **chỉ còn đuôi**: 51% dương, trung vị +0,0028, bỏ 5 tốt nhất còn −0,0075.
3. **Mạng và ridge sai khác nhau.** Trung bình điểm `ridge_W5` và `esm35_mcnn` (ensemble) cho 0,8384, hơn `ridge_W5` **+0,0098** [+0,0031; +0,0171] (seed +0,0117/+0,0060/+0,0053) và hơn `esm35_mcnn` +0,0079 [+0,0004; +0,0148]. Phép thứ hai, `ridge_W5` + `esm35_mcnn+scan_pool`, cho 0,8471 (+0,0184 so W5, CI [+0,0090; +0,0288]) **nhưng cấu hình này được chọn vì đứng đầu bảng nên chệch lạc quan**; chỉ phép thứ nhất (mạng chính của PROTOCOL) có thể đọc tương đối thẳng — và vẫn là hậu kiểm trên đúng 91 peptide đã khảo sát nhiều lần.
4. **Có sẵn một tập đánh giá rộng gấp ~30 lần:** peptide scanning nằm ngoài mọi cụm bão hòa còn **4.441 peptide / 2.779 cụm / 123.718 ô** (3.120 peptide có đủ hai lớp), so với 91 peptide / 89 cụm của benchmark hiện tại; chỉ thay R/A/S (64%/23%/12%), tỉ lệ dương ΔPSI ≥ 1 là 7,7% trên 123.718 ô này.

### 3.3 Diễn giải `[DIỄN GIẢI]`

- **Một thông điệp xuyên suốt: ngữ cảnh cục bộ là phần dễ học, và các nguồn bổ sung đều trùng nó.** Ridge có ±5 thì ESM thêm ≤ +0,0026 (D) và mạng ESM không hơn (S7); mạng one-hot (không có ngữ cảnh xa) thì ESM thêm +0,0137 (S1) và tiền huấn luyện scanning thêm +0,0147 (G ft); mạng ESM thì `scan_ft` không thêm gì (−0,0006) và `scan_pool` +0,0062 chưa đủ bằng chứng. Phù hợp giả thuyết "ESM, scanning và cửa sổ rộng cùng cung cấp một tín hiệu ngữ cảnh/vị trí; có một trong ba là đủ" — **giả thuyết, chưa kiểm trực tiếp**.
- **Mỗi họ mô hình đứng riêng dừng quanh 0,82–0,83** (ridge ±5 0,8286; ridge+ESM ≤ 0,8234; mạng đơn 0,81–0,83; ensemble ba mạng 0,8305 và 0,8367 cho điểm cao nhất bảng); chỉ phép trộn điểm hậu kiểm (3.2 điểm 3) vượt 0,83. Mọi khác biệt giữa các họ riêng lẻ nhỏ hơn độ phân giải (PROTOCOL §9: 0,014–0,021 cho mạng-so-ridge). Thêm biến thể mô hình trên 91 peptide này sẽ tiếp tục ra "chưa đủ bằng chứng" và làm tăng số đường rẽ đã đi (R0–R3, P0–P6, R6). Cái thiếu là **độ phân giải và tính độc lập của dữ liệu**, không phải thêm mô hình.
- **Ridge ±5 là cải thiện thật duy nhất, nhưng được chọn trên benchmark phát triển** (một trong ba độ rộng, đã hiệu chỉnh Bonferroni, ba seed dương, tái lập bit-bit giữa CPU cục bộ và Kaggle). Đường cong không đơn điệu (±7 ít hơn, ±10 âm) nên đừng đọc là "càng rộng càng tốt".
- **Kết quả không nên trích:** `esm35_mcnn+scan_pool` = 0,8367 là điểm cao nhất bảng nhưng Δ so tự đầu không nhận (+0,0062, CI phủ 0) và PROTOCOL §6 cấm báo "cấu hình tốt nhất" như ước lượng không chệch.

### 3.4 Chấm lại dự đoán PROTOCOL §10 và §12

| Dự đoán | Kết quả |
|---|---|
| (a) A: không độ rộng nào nhận; \|Δ\| < 0,005 | **Sai** (±5 nhận, +0,0078) — đã ghi ở §12 |
| (b) B: \|Δ\| < 0,01, khả năng nhận < 25% | **Đúng** (−0,0071; −0,0018; không nhận) |
| (c) D: không cỡ nào nhận, \|Δ\| < 0,01 | **Đúng** (cao nhất +0,0026) |
| (d) `oh_mcnn` − ridge ∈ [−0,03; 0] · `esm35_mcnn` − ridge ∈ [−0,02; +0,01], P không nhận · mCNN − CNN1 ∈ ±0,005 | **Đúng** (−0,0040 · +0,0097 sát biên, P chưa đủ · +0,0041/+0,0041) |
| (d) `esm35_mcnn` − `oh_mcnn` trong ±0,01 | **Sai** (+0,0137, nhận) |
| (e) F: chênh < 0,01 và không đơn điệu theo cỡ | **Đúng** (−0,0040/−0,0092/−0,0062; thứ tự 35M > 8M > 650M > 150M) |
| (f) G: `scan_pool` trong ±0,01 so với tự đầu | **Đúng** (+0,0073; +0,0062) |
| (f) G: `scan_ft` không hơn tự đầu | **Sai với `oh_mcnn`** (+0,0147, nhận); đúng với `esm35_mcnn` (−0,0006) |

### 3.5 Hướng đi `[ĐỀ XUẤT]` (cần Trọng duyệt trước khi chạy)

1. **Không thêm biến thể mô hình trên benchmark 91 peptide** (không sửa `ConvHead` theo gợi ý ở §12.4, không thêm cỡ ESM, không thêm chế độ scanning): hiệu còn lại < độ phân giải, và đó là "thiết kế thứ sáu".
2. **R7 — kiểm chứng ngoài mức peptide trên scanning ngoài mọi cụm bão hòa** (mục 3.2 điểm 4). Mô hình đóng băng, huấn luyện trên toàn bộ 92.337 ô bão hòa, đánh giá trên 4.441 peptide scanning không thuộc cụm cov80 nào của bão hòa; so `ridge_M3`, `ridge_W5`, ridge+ESM 35M, `esm35_mcnn` (ensemble ba seed) và **một** phép trộn khai báo trước (`ridge_W5` + `esm35_mcnn`). Trả lời ba câu mà R6 không phân giải được: W5 có tái lập trên peptide mới không, mạng/trộn có thật hơn ridge không, và giả thuyết "các nguồn ngữ cảnh trùng nhau" có đứng không. CI theo cụm trên 2.779 cụm thay vì 89 ⇒ sai số chuẩn nhỏ hơn cỡ 5–6 lần `[ƯỚC LƯỢNG]`. Hạn chế phải ghi trước: **cùng phòng thí nghiệm, cùng hệ đo** (không phải kiểm chứng độc lập thật), chỉ ba loại thay thế (AUROC tuyệt đối không so được với 0,82), scanning một replicate nhiễu hơn (Pearson 0,70–0,79 trên ô trùng bão hòa), ESM-2 đã thấy các protein này, và vẫn phải loại thêm paralog ngoài cụm cov80 (chạy cov50 hoặc luật MMseqs2 theo hit như R1/P3).
3. **R5 chốt mô hình sớm hơn lịch** (lịch cũ: tuần 10): nếu R7 xác nhận W5 thì chuyển `ridge_M3` → `ridge_W5` + Platt (260 cột thay 180; `predict.py`/`verify.py` đã có khung đối chiếu), còn không giữ M3. Mạng và phép trộn chỉ vào sản phẩm nếu R7 cho thấy hơn `ridge_W5` **và** suy luận numpy ba mạng chấp nhận được; mặc định là không.
4. **Luận văn:** kết quả R6 là một câu chuyện nhất quán cho Ch.4 — ridge có ngữ cảnh ±5 là đối chứng mạnh; pLM đóng băng và CNN thêm tối đa ~0,01, không phân giải được ở 91 peptide; ensemble ba mạng chỉ ngang ridge nhờ giảm phương sai.

## File

| File | Vai trò |
|---|---|
| [run-kaggle-20261023/](run-kaggle-20261023/) | `results.json`, `gates.json`, `env.json`, `r6-stage*.json`, `r6-benchmark.json` của lượt chính thức (OOF `.npz` nằm trong `r6-results.zip`, không lên git) |
| [posthoc_r6.py](posthoc_r6.py) → [posthoc-r6.json](posthoc-r6.json) | Phân tích hậu kiểm mục 3.2 (ensemble, theo peptide, trộn điểm, lượt đơn, độ phủ scanning ngoài cụm) |
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước |
| [r6-ladder-scan.ipynb](r6-ladder-scan.ipynb) | **Một** notebook cho toàn bộ giai đoạn 0, A–G; sạch outputs, đã stamp SHA-256 PROTOCOL |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook (sau đó chạy `stamp_protocol.py`) |
| [run_r6.py](run_r6.py) | Điều phối giai đoạn, ridge, huấn luyện mạng có tiếp tục được, tổng hợp (`python -I run_r6.py <thư-mục-OOF>` để tổng hợp lại ngoài notebook) |
| [r6data.py](r6data.py) · [r6esm.py](r6esm.py) · [r6nn.py](r6nn.py) · [r6stats.py](r6stats.py) | Dữ liệu và đặc trưng · trích ESM-2 · `ConvHead` · bootstrap theo cụm và quy tắc kết luận |
| [make_scantable.py](make_scantable.py) → `data/processed/r6-scantable.npz` | Bảng ô scanning (sổ nguồn gốc ở `data/README.md`); [scantable-summary.json](scantable-summary.json) |
| [cross_source_audit.py](cross_source_audit.py) → [cross-source-audit.json](cross-source-audit.json) | Phép kiểm chéo mục 1 |
| [dryrun-local-stageAB.json](dryrun-local-stageAB.json) | Kết quả ridge giai đoạn A và B từ lượt thử cục bộ (mục 2) |
| [selftest_r6.py](selftest_r6.py) | Kiểm đường code (15 kiểm; **không** phải thí nghiệm) |
| [data-needs.json](data-needs.json) | File dữ liệu notebook cần cho `make_data_package.py` |

## Đã kiểm cục bộ `[ĐO]` (không huấn luyện thật, không in AUROC của biến thể nào)

- `selftest_r6.py`: 15/15 kiểm. Đặc trưng dựng lại bằng `cell_features(W=3)` **bằng cache từng bit** trên 92.337 ô; ridge M3 qua đường chia của R6 cho 0,820822 (ensemble) khớp P0 đến 0; không hàng scanning nào thuộc cụm test ở cả 5 fold; `compare` trùng `run_curve.compare`; **cắt cửa sổ ESM-2 8M thật khớp tính tay ở vị trí 1, 2, 14, 27, 28** (kể cả biên); mạng tất định theo seed trên CPU, tiếp tục được khi phiên ngắt.
- Chạy thử notebook trên CPU trong cây thư mục ghép từ hai gói zip: đường SMOKE, rồi toàn bộ các ô 0–15 (ESM-2 8M thay cho cả bốn cỡ; mạng 1 seed × 1 fold × 2 epoch) — **tất cả ô chạy hết, không lỗi**, kể cả trích embedding cho 92.337 ô bão hòa + 133.764 ô scanning, ridge+ESM, nạp crop, mạng ở cả bảy cấu hình và bốn chế độ scanning, tổng hợp, đóng gói `r6-results.zip` (một lỗi đầu tiên là do công cụ thử của tôi, không phải notebook). Điểm của mạng trong lượt này không có giá trị khoa học và không lưu.
- Hạn chế (lúc đó): chưa chạy trên GPU thật. **Đã giải quyết bằng lượt Kaggle 23/10 (mục 3).**

## Việc Trọng làm tay — **đã xong 23/10/2026** (giữ để dựng lại)

1. Dựng lại **cả hai gói** (đã có file dữ liệu mới nên `degron-data-v1` không đủ): từ gốc repo
   ```bash
   K=topics/degron-footprint/research/notebook-kit-2026-10-22
   python3 -I $K/make_data_package.py --list          # duyệt danh sách trước khi upload
   python3 -I $K/make_data_package.py --version v2    # -> degron-data-v2.zip
   python3 -I $K/make_code_package.py
   ```
   Trên Kaggle: *New Version* của dataset dữ liệu với `degron-data-v2.zip` và của dataset mã với zip mới. Chỉ gắn **một** gói dữ liệu vào notebook (nbkit lấy gói đầu tiên tìm thấy).
2. Import `r6-ladder-scan.ipynb`, gắn hai dataset, *Accelerator* = GPU T4, **Internet bật**. Chạy lần đầu với `SMOKE = True`, rồi `SMOKE = False`.
3. Đọc ô benchmark (giờ GPU ước lượng theo số đo thật) **trước** khi để chạy hết; thiếu hạn mức thì bỏ `'G'` rồi `'F'` khỏi `STAGES` (không bỏ 'E').
4. Tải `r6-results.zip`, giải nén vào `run-<phiên>/` cạnh README này. Rồi báo tôi: tôi đối chiếu tiêu chí chốt trước, viết kết quả vào README này (kể cả khi âm), chấm lại các dự đoán PROTOCOL §10 và cập nhật sổ `data/README.md`.

## Chi phí `[ĐO]` (lượt Kaggle 23/10, 2×T4, 4 CPU, 31 GB RAM)

Tổng ≈ 1 giờ 25 phút (07:22–08:47 UTC theo dấu thời gian file; [env.json](run-kaggle-20261023/env.json)). Ô benchmark ([r6-benchmark.json](run-kaggle-20261023/r6-benchmark.json)): 1,29 s/epoch (`oh_mcnn`), 1,59 s/epoch (`esm35_mcnn`); ước lượng của ô đó là E 0,53 giờ, G 1,32 giờ, F 0,60 giờ (tổng 2,4 giờ) — thực tế E+F+G xong trong khoảng một giờ. Trích ESM-2 ([r6-stage-c.json](run-kaggle-20261023/r6-stage-c.json)): 38 s / 111 s / 130 s / 383 s cho 8M / 35M / 150M / 650M (cộng ≈ 11 phút, thấp hơn ước 12–20 phút). Kết luận cho kế hoạch: một lượt tương tự (một cấu hình mạng × 15 lượt) rẻ, nên R7 không bị chặn bởi hạn mức GPU.

## Giới hạn (chi tiết ở PROTOCOL §9)

Benchmark phát triển OOF, không phải kiểm chứng ngoài; ngưỡng phân giải ≈ 0,014–0,021 cho phép so mạng với ridge, ≈ 0,008 cho cặp cấu hình gần nhau, nên "chưa đủ bằng chứng" không loại trừ lợi ích nhỏ; một cấu hình siêu tham số cho mọi mạng; ESM-2 đã thấy các protein người lúc tiền huấn luyện; rò rỉ scanning chỉ chặn bằng cụm cov80; scanning chỉ có thay thế R/A/S.

Thêm sau khi có kết quả: (i) điểm ensemble của mạng và ridge **không cùng loại** (mạng được giảm phương sai ≈ +0,008…+0,013, ridge không), nên mọi so sánh mạng-so-ridge ở ensemble đều thiên lợi cho mạng — xem 3.2 điểm 1; (ii) phép trộn điểm 3.2 là hậu kiểm, một trong hai phép chọn theo kết quả; (iii) `ridge_W5` được chọn trên chính benchmark phát triển; (iv) benchmark vẫn là 91 peptide đã khảo sát nhiều lần, nay thêm một lượt R6.
