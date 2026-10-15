[← Bài trước](08-contribution.md) · Bài 9/10 · [Bài sau: Dữ liệu thật →](10-data-up-close.md)

# Bài 9 — Rủi ro và điều có thể làm đề tài sụp

Bài này tồn tại để bạn không bị bất ngờ. Xếp theo mức nguy hiểm.

> **Cập nhật 15/10/2026 (phiên chiều) — sau khi đào sâu bộ nhân Larsen 2025 và cả bảy rủi ro này.**
> Nguồn: [báo cáo đầy đủ](../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/README.md),
> kèm [ghi chép nghiên cứu](../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/notes/).
>
> **Bốn điều đổi cách hành động:**
>
> 1. **Đường thoát ghi ở rủi ro 1 không tồn tại.** Bộ nhân Larsen **không có một nhãn mức residue nào** — nó không cứu được nhãn residue nếu nhãn sụp. Câu cũ đã sai, đã sửa ở dưới.
> 2. **Tiền lệ thứ năm: [Degformer](papers/degformer-2026.md)** đã xuất **đúng** ma trận 28 × 20 ΔPSI từ đúng nhãn của đề tài. Câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20" ở rủi ro 3 **đã sai** và đã sửa.
> 3. **Kết quả âm "siết read 10 → 200" nay có lời giải thích trích dẫn được** (DiMSum + Enrich2), và thuốc chữa là **thêm replicate, không phải thêm read**.
> 4. **Đơn vị suy luận là cụm protein, không phải peptide.** Bỏ qua lồng nhau cho tỉ lệ dương giả **trên 45%** ở mức danh nghĩa 5%.

---

![Rủi ro xếp theo mức nguy hiểm](figures/fig-14-risks.svg)

*Sơ đồ tự dựng. Chi tiết từng rủi ro ở dưới.*

---

## Rủi ro 1 — ~~lực thống kê~~ → **đã giải quyết 13/10/2026**

**Vấn đề đã nêu:** chia test theo cụm protein chỉ còn **221–322 footprint**. Với n ≈ 250, một cải thiện nhỏ có thể không chứng minh được.

**✅ Đã tính, và tập test đủ lực.** So với baseline thành phần trung thực (0,4897) thì chỉ cần **18** peptide. So với mốc oracle 0,6045 thì cần **209**, và n = 221–322 cho lực **0,82–0,94**. Kết luận vững ở cả ba cách xử lý tie.

**Việc còn lại từ rủi ro này:** dùng **split coverage 80%** (271–322) chứ không phải cov50, vì ở n = 221 lực chỉ 0,82. Và khi có mô hình thật thì phải tính lại lực bằng độ lệch chuẩn của chính cặp so sánh đó.

Nguồn: [full-data-audit mục 5](../../topics/degron-footprint/research/full-data-audit/README.md), giải thích dễ hiểu ở [bài 10](10-data-up-close.md).

> **Rủi ro số một mới: nhãn mức residue chỉ lặp lại khoảng một nửa.** Hai lần đo độc lập đồng ý "peptide này có footprint" ở mức **89,3%**, nhưng đồng ý **đúng vị trí nào** chỉ ở mức **Jaccard 0,4965**, và chỉ **16,0%** peptide có tập vị trí dương giống hệt. Đề tài dự đoán đúng ở mức residue đó, nên đây là trần cứng cho mọi mô hình. Không chữa được bằng siết ngưỡng reads (đã thử, thất bại).

**Nếu sụp:** giảm độ chặt của phép chia cụm (cov80 cho 271–322 thay vì 221–301), hoặc nới ngưỡng PSI WT lên 3,5 (141 peptide, phải biện minh), hoặc chấm ở mức ô kèm xử lý phụ thuộc trong peptide. ⚠ **Không còn dự phòng để kích hoạt** — [D-026](../../DECISIONS.md#d-026) (14/10) đã bỏ.

> ⚠ **SỬA 15/10 — bỏ một đường thoát đã ghi sai.** Bản trước nói có thể "bổ sung bộ nhân của [Larsen 2025](papers/larsen-2025.md)" nếu rủi ro này thành hiện thực. **Đường đó không tồn tại.** Bộ nhân chỉ có nhãn **mức tile 30 acid amin, bước 15**, trên trình tự **hoang dã**: không bão hòa, không alanine scan, **không một nhãn mức residue nào**, và bài **không có một con số mức residue nào**. Nó không nâng n, không cải thiện Jaccard 0,4965, không thay được mốc ΔPAP mức residue. Chi tiết: [papers/larsen-2025.md](papers/larsen-2025.md).

> ⚠ **Rủi ro này đã trở lại ở dạng khác, 15/10.** Phép tính lực trên chỉ áp cho **bộ quét**. Sau khi [D-025](../../DECISIONS.md#d-025) chuyển nguồn nhãn chính sang **bộ bão hòa**, cỡ mẫu là **91 peptide** (không phải 235, vì ngưỡng PSI WT ≤ 3,0 cắt bớt), và **lực cho cỡ đó chưa tính**. Đây là **việc chặn duy nhất** còn lại.

### Mới 15/10 — ba điều làm rủi ro này sắc hơn

**Một, "nhãn lặp một nửa" nay quy ra được thành một con số trần.** Gọi độ tin cậy của một lần đo là `ρ`. Một mô hình dự đoán **hoàn hảo** vẫn chỉ tương quan với **một** replicate ở mức `sqrt(ρ)`, và công thức Spearman–Brown cho biết trung bình `k` replicate có độ tin cậy `ρ_k = kρ₁/(1+(k−1)ρ₁)`. Áp vào bộ quét `[phân tích]`:

| Lượng | Giá trị |
|---|---:|
| Tỉ lệ nhiễu trong phương sai dư (bộ quét) | 0,759 |
| Độ tin cậy **một** replicate `ρ₁` | **0,241** |
| Độ tin cậy **trung bình 2 replicate** `ρ₂` | **0,388** |
| Trần Pearson của phần ngữ cảnh học được, so với **một** replicate | **0,295** |
| Cùng trần đó, so với **trung bình 2 replicate** | **0,374** |
| **Lợi ích tương đối của việc lấy trung bình** | **+27%** |

Hai điều phải nói ngay. (a) Phép tính này cho **bộ quét**; trên **bộ bão hòa** — nguồn nhãn chính theo [D-025](../../DECISIONS.md#d-025) — nhiễu chỉ 16,7% nên lợi ích chỉ còn **≈ +4,5%**. (b) Việc dùng trung bình hai replicate **đã được chốt rồi** ([D-025](../../DECISIONS.md#d-025) mục 3), nên con số này dùng để **biện luận trong luận văn**, không phải để ra quyết định mới.

**Hai, đơn vị suy luận là cụm protein.** Con số cần báo ở bộ bão hòa không phải "91 peptide" mà là **số cụm protein** trong 91 peptide đó. Với dữ liệu lồng nhau, phép kiểm thường cho tỉ lệ dương giả **trên 45%** dù đặt mức danh nghĩa 5% (Saravanan, Berman & Sober) `[đọc]`. Nếu số cụm dưới ~20 thì mọi p-value chỉ nên đọc là **chỉ báo**.

**Ba, thước đo "trùng khít tập vị trí" (16,0%) có cách thay có tiền lệ.** Benchmark túi gắn protein–ligand coi hai túi là cùng một túi khi **Jaccard ≥ 0,75**; Binding-site Distance Test cho **điểm thưởng từng phần theo khoảng cách**; ProteinGym dùng **Top-K recall ở K = 10%** và NDCG. Và QCDPred — tiền lệ gần nhất, cùng họ dữ liệu — báo **Spearman mức peptide**, chưa bao giờ báo khớp chính xác mức residue `[đọc]`.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí, làm trước tiên — tính lực ở n = 91 *và đếm số cụm protein*.**
2. **Miễn phí — phát biểu trước mức chênh phát hiện được.** Với SD ghép cặp 0,2416, ở n = 91 thì SE ≈ 0,0253 và mức chênh tối thiểu phát hiện được ở lực 80% là **≈ 0,071**. So với dư địa 0,1827 thì phép so với ΔPAP **phát hiện được**; nhưng **ablation cỡ 0,02–0,05 thì không**. Nên **cam kết trước** rằng phần lớn ablation sẽ không phân biệt được về thống kê `[đề xuất]`.
3. **Một ngày — bootstrap phân cấp mức cụm.** Resample cụm → peptide → residue, B = 10.000, và báo **khoảng tin cậy của hiệu ghép cặp**, không phải hai khoảng rời (đọc hai khoảng chồng nhau là lỗi kinh điển).
4. **Một ngày — bộ thước đo ba tầng.** Chính: AUROC mức ô (bộ bão hòa) + precision@3 mức residue (bộ quét). Phụ: top-k có **sai số ±1 vị trí**, Jaccard sau khi nở ±1, hồi quy trên cửa sổ 5–7 residue (đúng cách QCDPred làm). Chẩn đoán (không phải chỉ số): trùng khít tập vị trí `[đề xuất]`.

---

## Rủi ro 2 — phần dư 35% có thể chỉ là nhiễu

**Vấn đề:** đề tài trông cậy vào việc 35,0% phương sai ΔPSI còn lại sau oracle thành phần là **ngữ cảnh học được**. Nhưng:

- dữ liệu dùng **một replicate**, không phải trung bình nhiều lần
- ngưỡng reads tối thiểu **thấp**
- nhãn genotype BAG6 của replicate này **chưa rõ**
- **chưa ai tách** phần ngữ cảnh khỏi phần nhiễu đo

Nếu phần lớn 35% đó là nhiễu thí nghiệm, thì **không mô hình nào học được nó**, và dư địa 0,1747 là ảo.

> **⚠ Cập nhật 13/10/2026 — đã kiểm, và lo ngại này phần lớn là đúng.** Dựng được lần đo thứ hai từ read thô nên tách được trực tiếp:
>
> | | |
> |---|---:|
> | Phần dư sau oracle thành phần | 0,3612 |
> | Trong đó là **nhiễu đo** | **75,9%** |
> | **Ngữ cảnh học được, cận trên** | **0,0872** |
>
> Tức phần có thể học thêm là khoảng **8,7%** phương sai, **không phải 35,0%**. Dư địa 0,1747 thì **đúng là ảo**, nhưng vì một lý do khác nữa: nó là hiệu của hai oracle đọc nhãn test. Dư địa thật là **0,1617** so với baseline thành phần trung thực.
>
> **Đã thử chữa và thất bại:** siết ngưỡng reads từ 10 lên 200 **không** giảm tỉ lệ nhiễu (giữ 0,72–0,77) mà mất một nửa dữ liệu. Nhiễu ~0,24–0,34 được xác nhận **bốn lần độc lập** ⇒ là tính chất của thí nghiệm GPS. **Đừng thử lại hướng này.**
>
> Chi tiết dễ hiểu: [bài 10 mục 6](10-data-up-close.md). Số liệu: [full-data-audit](../../topics/degron-footprint/research/full-data-audit/README.md).

### Mới 15/10 — kết quả âm đó nay là một phát hiện có trích dẫn

Trước đây "siết read không giúp" chỉ là một kết quả âm tự đo. Nay có **hai nguồn độc lập giải thích vì sao, và cả hai kê cùng một thuốc.**

**DiMSum** (Faure và cộng sự, *Genome Biology* 2020) phân rã phương sai điểm fitness thành hai số hạng phụ thuộc số đọc **cộng một số hạng cộng không phụ thuộc số đọc**:

```text
σ²(f) = m_input/N_input + m_output/N_output + a
                                              ↑ không phụ thuộc số đọc
```

và viết nguyên văn: *"increasing sequencing coverage **will not lead to reductions** in the measurement errors of their fitness scores"*, với thuốc chữa là *"increasing the number of **replicate** experiments"* `[đọc]`. Đây **chính xác** là lý do 10 → 200 thất bại: siết ngưỡng chỉ thu nhỏ hai số hạng `m/N`, còn `a` thì không chạm được. Khi các biến thể còn lại đủ dồi dào để `m/N ≪ a` thì tỉ lệ nhiễu **bị sàn bởi `a`** và trơ với mọi ngưỡng tiếp theo.

**Enrich2** (Rubin và cộng sự, *Genome Biology* 2017) cho một mũi độc lập và mạnh hơn, vì là **kết quả thực nghiệm**: trên domain C2, *"input count filtering selected a subset of variants whose scores were **more poorly correlated** than the unfiltered set"* `[đọc]`. Tức siết ngưỡng read đã từng làm **xấu đi** độ tương đồng replicate trong một bộ dữ liệu đã công bố.

**Và một rủi ro khoa học mới cùng họ.** [LeBlanc và cộng sự 2026](papers/leblanc-2026.md) (*Cell Systems*), với 30 seed × 200 bootstrap trên 17.732 tile, báo rằng ma trận tham số của họ có *"horizontal streaks, indicating that **composition is more important than individual positions**"* và rằng các bộ lọc *"are **not picking up on specific protein motifs**"* `[đọc]`. Nếu điều đó cũng đúng cho tile degron thì **một mô hình mức residue có thể đang khớp nhiễu vị trí**. Bài đó cho luôn khuôn thí nghiệm để kiểm: báo **độ ổn định của trọng số theo từng vị trí qua seed và bootstrap**.

**Cách xử lý, xếp theo chi phí:**

1. **Miễn phí — ghi nhận rằng [D-025](../../DECISIONS.md#d-025) đã giảm rủi ro này rất nhiều.** Trên bộ bão hòa, nhiễu là **16,7%** và Jaccard **0,6596**, so với 75,9% và 0,4965 trên bộ quét.
2. **~1 ngày — huấn luyện có trọng số theo độ chính xác.** `w = 1/σ̂²` với **Huber** thay MSE. **Chế độ thất bại phải phòng:** với chỉ 2 replicate, phương sai từng mẫu tự nó cực nhiễu và trọng số có thể **khuếch đại** nhiễu — nên khớp một **đường cong phương sai–độ sâu toàn cục** thay vì dùng SD thô `[đề xuất]`.
3. **~1 ngày — nhãn mềm có cơ sở.** Label smoothing cho đầu "có footprint" với `ε ≈ 1 − 0,893 = 0,107` lấy từ tỉ lệ bất đồng **đo được**, thay cho con số 0,1 tuỳ ý `[đề xuất]`.
4. **Không nên làm:** co-teaching hay bất kỳ phương pháp chọn "small-loss" nào — ở n hàng trăm, chúng sẽ chọn đúng những peptide dễ, độ sâu cao, chính phép chọn mà audit đã chứng minh **không** giảm nhiễu. Bayes phân cấp đầy đủ (kiểu Rosace) đúng về nguyên lý nhưng ngoài phạm vi; **trích trong phần hạn chế** `[đề xuất]`.

**Điều vẫn có thể giết nó:** nếu phép kiểm độ ổn định theo seed/bootstrap cho thấy trọng số **theo vị trí** không ổn định trong khi tổng **theo acid amin** thì ổn định — tức "thành phần > vị trí" cũng đúng cho degron — thì nhiệm vụ mức residue mất cơ sở khoa học, bất kể thước đo hay kiến trúc nào.

---

## Rủi ro 3 — G3, ứng dụng không khác biệt được

**Vấn đề:** đã có **bốn** tiền lệ — [DEGRONOPEDIA](papers/degronopedia-2024.md), máy chủ web [MetaDegron](papers/metadegron-2024.md), Colab của nhóm PAP, và — **mới phát hiện 13/10** — **mô hình học máy của chính nhóm Zhang 2023**, dự đoán PSI toàn peptidome (Pearson 0,8955, RMSE 0,563 trên 260.989 peptide), nằm trong file Mendeley 393 MB mà repo chưa từng tải. Cái thứ tư **khác phạm vi** (dự đoán ở mức peptide, không phải mức residue) nên không phải đối thủ trực tiếp, nhưng **phải nêu** trong đề cương. Tiêu chí 5 của GVHD không thể thiếu, nhưng "làm thêm một web nữa" không phải đóng góp.

**Cách xử lý:** nhắm vào thứ cả bốn đều không có — **ma trận vị trí × acid amin thay vào, dựa trên nhãn đột biến thực nghiệm**.

> ✅ **Đã kiểm ngày 14–15/10** ([tra y văn](../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md)): cả bốn đều xuất ở mức **peptide hoặc motif**. DEGRONOPEDIA là annotation motif; MetaDegron phân loại degron theo E3 (**nhánh học sâu chỉ dùng trình tự**, không attention); PAP/Colab xuất điểm khối; SVM Zhang xuất PSI mức peptide.

> ❌ **BÁC BỎ 15/10 — câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20" đã sai.**
> **[Degformer](papers/degformer-2026.md)** (repo GitHub Apache-2.0, tạo 24/03/2026, không bài báo) huấn luyện trên **đúng** bảng S1 + S4 + S7 của Zhang 2023, `MAX_LEN = 28`, và ship `saturation_mut_heatmap.py` xuất **ΔPSI trên 28 vị trí × 20 acid amin** `[đọc]`. Đây là **tiền lệ thứ năm**.
> Thêm nữa, **DegronMD** (*Mol Biol Evol* 2023) là một tiền lệ **đã công bố** có module đột biến mà repo bỏ sót hoàn toàn `[đọc]`.
> **Và hai câu trong tài liệu repo phải gỡ:** **MetaDegron và DegronMD đều có batch submission**, nên "batch" **không phải** điểm khác biệt `[đọc]`.

### Năm khoảng trống thật, đã kiểm từng công cụ (15/10)

| Tính năng | DEGRONOPEDIA | MetaDegron | DegronMD | PAP/QCDPred | Degformer |
|---|---|---|---|---|---|
| Batch | **Không** | Có | Có | Colab | script cục bộ |
| **API lập trình** | không nêu | không nêu | không nêu | không | không |
| Chấm **đột biến tuỳ ý** | Không — chỉ tra COSMIC | Không | Không — chỉ đột biến đã quan sát | tự tính ΔPAP | **Có, cục bộ** |
| Xuất **ma trận vị trí × acid amin** | không nêu | không nêu | không nêu | dựng tay cho HSF1 | **Có** |
| **Bất định từng dự đoán** | Không | Không | chỉ cho degron | Không | Không |
| **Xuất xứ nhãn thực nghiệm** | không nêu | không nêu | không nêu | — | Không |
| **Dự đoán theo ngăn tế bào** | không nêu | không nêu | không nêu | **chỉ bào tương** | Không |

Tất cả `[đọc]`, từ tài liệu/bài báo của từng công cụ và từ mã nguồn Degformer.

**Chỗ giá trị thật nằm ở bốn tính năng không công cụ nào có** `[đề xuất]`:

1. **API** — khoảng trống đã xác minh ở cả ba server, và là thứ dễ biện minh nhất cho một luận văn **Kỹ thuật phần mềm**.
2. **Chấm đột biến tuỳ ý kèm xuất ma trận qua web** — Degformer chỉ làm được cục bộ.
3. **Bất định từng dự đoán neo vào trần nhãn đã đo** — một công cụ trả về *"ΔPSI = −1,2, nhưng nhãn mức residue của assay này chỉ lặp ở Jaccard 0,50 nên hãy coi danh tính residue là bất định"* sẽ **duy nhất và trung thực**, và nó **tiền tệ hoá** đúng phần mạnh nhất của repo.
4. **Xuất xứ nhãn** — repo đã tính được **725/770** peptide footprint có một tile trong tập train của PAP, đúng loại thông tin người dùng cần để biết dự đoán là nội suy hay ngoại suy.

Thêm một tính năng rẻ do chính lĩnh vực nêu: **cờ cảnh báo theo ngăn tế bào** ("dự đoán này từ mô hình huấn luyện trên dữ liệu bào tương; protein của bạn nằm trong nhân") — PAP là mô hình **chỉ bào tương** theo chính lời tác giả Larsen.

**Điều vẫn có thể giết nó:** nếu GVHD giữ kỳ vọng "kiến trúc chưa ai dùng" (đã nói 11/10) thì một tập tính năng ứng dụng **không đáp được** tiêu chí đó. Đây là lý do [C-7](../../DECISIONS.md) cần Trọng quyết, và nên hỏi GVHD cùng C-5.

---

## Rủi ro 4 — kiến trúc có thể không thắng, hoặc không cần thiết

Hai nhánh:

**4a. MIL không cần thiết.** Khi đã có nhãn mức residue, một đầu hồi quy theo vị trí là mô hình tự nhiên. Nếu nó đã đủ thì cơ chế túi là phức tạp không cần thiết. Đây là **đối chứng bắt buộc**, không phải việc có thể bỏ qua.

**4b. Kiến trúc khu trú không thắng trên thang điểm đoạn.** Có dấu hiệu: đổi phép gộp làm Pearson sụt 0,824 → 0,344, entropy theo vị trí gần tối đa (3,294/3,401). Nhưng **phép thử đó không công bằng** (dùng trọng số huấn luyện cho gộp trung bình), nên chưa kết luận được.

**Cách xử lý:** không đặt đóng góp lên thang điểm đoạn. Dùng bậc 2 và 3 ([bài 7](07-evaluation.md)).

> ✅ **Có bằng chứng dương cho trục này, đo 14/10.** Đổi kernel 1 → 7 cho **+0,1311** precision@3 ở mức residue, so với chỉ **+0,0032** Pearson trên điểm đoạn. Nên lo ngại "trục ngữ cảnh đã cạn" **không áp cho thang đo của đề tài**. Xem [bài 5 mục 5.2](05-the-gap.md).

**4c. ⚠ Cổng phơi lộ không huấn luyện được — rủi ro này đã thành hiện thực, 15/10.** Mọi nhãn huấn luyện chính là **peptide tách rời gắn đầu C của GFP**, nên rASA **không có phương sai** và tham số của cổng **không nhận diện được**. Thành phần 4 đã bị hạ xuống **cơ chế chuyển giao** và đưa ra khỏi đường găng của G2 ([bài 6 mục 3.2](06-proposed-solution.md), đề xuất [C-8](../../DECISIONS.md)).

### Mới 15/10 — một câu phải bỏ, và một ablation thành bắt buộc

**Về 4a: đừng nói "MIL bền hơn với nhãn nhiễu".** Lý lẽ của Ilse, Tomczak & Welling cho gộp mức embedding là nó *"avoids the extra error that comes from training an instance classifier **without instance labels**"* `[đọc]` — đó là lý lẽ về nhãn **vắng mặt**, không phải nhãn **nhiễu**. **Không tìm thấy** bài nào so sánh có kiểm soát giữa giám sát mức túi và mức thể hiện **theo tỉ lệ nhiễu nhãn**. Ngược lại, văn liệu ảnh bệnh học nói thẳng chiều phản: *"instance-level prediction … remains unsatisfactory"* `[đọc]` — đe doạ trực tiếp đúng khẳng định "vị trí nào" của đề tài.

Nhưng cùng chỗ đó là **cơ hội**: trong phạm vi degron, **mọi** mô hình đã khảo sát đều dùng mục tiêu scalar mức cửa sổ với phép gộp đơn giản — PAP **global average pooling**, MetaDegron-D **max-pooling**, Degformer **CLS token**. **Chưa thấy** mô hình degron nào dùng attention pooling hay đầu giám sát mức residue `[đọc]`. Và phép so MIL-vs-đầu-theo-vị-trí **chưa tìm thấy ai làm** ở đâu trong dự đoán mức residue của protein — đây là **đóng góp chưa ai chiếm, và đề tài có đủ tài sản để làm**.

**Về phép gộp: đừng dùng max.** Max pooling đặt toàn bộ gradient lên một residue mỗi peptide, mà với nhãn thể hiện ở Jaccard 0,50 thì việc đó gần như tung xu. **top-k (soft bag)** và **noisy-OR** phân tán gradient, và cả hai đều có tiền lệ đối chứng trực tiếp `[đọc]`.

**Về cổng phơi lộ — phản biện phải chuẩn bị.** Trong Yang và cộng sự (*PLOS Comput Biol* 2026), **rASA là đặc trưng node đầu vào**, đặc trưng cạnh là hình học thuần, và attention pooling điều khiển bởi **một vector truy vấn học được** — **không** phải cổng theo độ lộ `[đọc]`. **Nhưng** một attention pooling học được, trên node mà đặc trưng **đã gồm rASA** và đã đi qua 4 lớp GAT, **về nguyên tắc biểu diễn được một cổng phơi lộ** — nó là **tập mẹ** của cổng đặt tay.

→ Nên luận văn **không thể** dựa vào "chưa ai đặt độ lộ gần bước gộp". Nó phải dựa vào **một ablation** cho thấy cổng tường minh thắng attention pooling học được **khi cả hai nhận cùng đặc trưng rASA/pLDDT**. Chính Yang và cộng sự **chưa bao giờ chạy ô chéo đó** — đúng ô trống đề tài có thể chiếm. (Ablation của họ là khuôn: thay attention pooling bằng average pooling làm MCC rơi **0,83 → 0,71**; bỏ RSA làm ROC-AUC giảm **4%**.)

**Cách xử lý:**

1. **Miễn phí — phát biểu lại khung.** Không trình bày MIL như kết quả đã biết; trình bày như **một thí nghiệm có tiên đoán ghi trước**. Nhãn túi lặp 89,3% còn nhãn thể hiện chỉ Jaccard 0,4965 — lý lẽ của Ilse khớp gần như từng chữ với hai con số đó. Đó là **động lực trích dẫn được**; **kết quả thì phải đo** `[đề xuất]`.
2. **Vài ngày — ablation 3 nhánh** trên cùng backbone, cùng cửa sổ, cùng Huber có trọng số: (1) đầu theo vị trí trên nhãn thể hiện; (2) attention-MIL mức embedding chỉ trên nhãn túi, đọc trọng số attention làm footprint; (3) lai (loss túi + loss thể hiện hạ trọng số, λ ≈ 0,1–0,3). Chấm **cả ba** trên **cả** chỉ số túi **và** chỉ số thể hiện có sai số ±1 `[đề xuất]`.
3. **Chuẩn bị trước chế độ thất bại đã được ghi nhận:** attention-MIL rất có thể **thắng chỉ số túi** và **thua hoặc hoà** ở định vị thể hiện. Nếu vậy, kết luận trung thực và vẫn có giá trị là *"giám sát mức túi là mục tiêu đúng cho đích lặp lại được; định vị thể hiện cần loss lai"*.
4. **Vài ngày — ablation ô chéo cho cổng phơi lộ, ở mức tile, trên bộ nhân Larsen.** Bốn ô: pooling học được ± rASA × cổng tường minh ± rASA. Đây là đóng góp kiến trúc khả thủ duy nhất còn lại sau khi C-8 hạ cổng xuống cơ chế chuyển giao `[đề xuất]`.
5. **Cổng phải *học được và có dấu*, không phải mặt nạ cứng.** Sinh học 2026 chống lại một tiên đề đơn điệu: có báo cáo rằng BAG6 và RNF126 thúc đẩy phân hủy protein mang degron **bị chôn** `[chưa xác minh — chỉ tiêu đề]`, và Schulze 2026 có **PRKN S109**, một residue **phơi lộ** mà đột biến có vẻ *tạo ra* degron. Phép đo đảo dấu của chính repo (−0,1928 vùng chôn so với +0,3733 vùng phơi lộ) khớp với tính **không đơn điệu**, không khớp với một mặt nạ `[đo]`.

**Điều vẫn có thể giết nó:** nếu ablation ô chéo cho thấy pooling học được **có cùng rASA đầu vào** đạt bằng hoặc hơn cổng tường minh, thì thành phần đó mất lý do tồn tại. Vì C-8 đã hạ nó xuống cơ chế chuyển giao, điều đó **không giết đề tài**, nhưng giết **thành phần** và phải ghi vào luận văn như một kết quả âm.

---

## Rủi ro 5 — tính mới bị thu hẹp thêm

Đã bị thu hẹp hai lần rồi:

| Lần | Phát hiện | Mất gì |
|---|---|---|
| 11/10 | [BioBlobs](papers/bioblobs-2025.md) đã dùng attention-MIL trên protein; [OmniESI](papers/omniesi-2025.md) đã dùng điều biến có điều kiện | Không được nói cơ chế là mới |
| 11/10 | [Larsen 2025](papers/larsen-2025.md) đã dùng rASA/pLDDT và đã làm bản đồ ΔPAP *in silico* | "Dùng cấu trúc" và "giải thích biến thể" không còn mới |
| **14/10** | **Larsen 2025 còn đã tìm ra hiện tượng ΔPAP đổi dấu** trên CRX: Pearson **0,54** ở IDR so với **−0,19** ở vùng gấp | Phép đo 14/10 của repo chỉ là **xác nhận lại**, không phải phát hiện |
| **14/10** | [Schulze & Lindorff-Larsen 2026](papers/schulze-2026.md) đã gộp 6 VAMP-seq / 31.614 biến thể trên **đúng 6 protein** repo dùng, tách chôn/phơi lộ | Thành **baseline bắt buộc**; và tiết lộ hai lỗi phương pháp của phép đo 14/10 |
| **15/10** | Tự phát hiện: **cổng phơi lộ không huấn luyện được** trên nhiệm vụ chính | Mất một trong hai "điểm mới" đã nêu |
| **15/10 (chiều)** | **[Degformer](papers/degformer-2026.md)** huấn luyện trên **đúng** S1+S4+S7 của Zhang, `MAX_LEN = 28`, ship script xuất **ΔPSI trên 28 vị trí × 20 acid amin** `[đọc]` | **Claim "ma trận 28×20 là thứ không tiền lệ nào xuất" chết như đang viết** |
| **15/10 (chiều)** | **DegronMD** (*MBE* 2023) là tiền lệ **đã công bố** có module đột biến | Một tiền lệ bị bỏ sót, phải trích |
| **15/10 (chiều)** | **[LeBlanc 2026](papers/leblanc-2026.md)** đã làm: tách abundance khỏi function trên thư viện tile; **split theo cụm protein phân cấp**; **đối chiếu trần replicate bằng số** (0,555 so với 0,568) `[đọc]` | Ba lập luận hỗ trợ **hạ xuống "thực hành chuẩn"**, phải viết "theo LeBlanc et al. 2026" |
| **15/10 (chiều)** | **Yang 2026** (*PLOS Comput Biol*) kết hợp **rASA đầu vào** với **attention pooling**, và pooling học được là **tập mẹ** của cổng đặt tay `[đọc]` | Tính mới của cổng co lại thành **một ablation bắt buộc** |

### Hai điều **không** thu hẹp nó — tín hiệu tốt nhất của phiên 15/10

**Một, LeBlanc 2026 không chiếm claim mức residue.** Grep toàn văn tìm `per-residue`, `residue-level`, `saturation`, `variant effect`, `mutagenesis` trả về **không kết quả nào** trong thân bài; mọi chỉ số của họ là mức tile (n = 2.521); và khi có đối thủ mức residue họ **gộp nó về mức tile** `[đọc]`.

**Hai, không có công cụ dự đoán degron mới nào được công bố trong 2025–2026**, qua hai cơ sở dữ liệu độc lập: PubMed `degron AND (prediction OR machine learning OR deep learning)` 2025–2026 cho **41 bản ghi**, không có công cụ mới; Europe PMC `TITLE_ABS:"degron"` + từ khoá ML cho **100 hit**, `TITLE:"degron"` **127 hit**, cũng không `[đọc]`. Củng cố: Larsen 2025 có **9 citation**, Voutsinos 2026 có **11**, và trong **19 bài trích khác nhau, không bài nào** là mô hình dự đoán degron hay làm footprint mức residue `[đọc]`.

> **Phải viết đúng dạng:** *"đã chạy truy vấn X trên PubMed và Europe PMC ngày 15/10/2026, không tìm thấy"* — **không** viết "chưa ai làm".

**Việc còn chưa làm:** đọc toàn văn QCDPred, DEGRONOPEDIA, JoGo (hiện chỉ **[qua tóm tắt]**); và **DegPred** — công cụ duy nhất chưa xác minh được mức xuất ra, **phải giải quyết trước khi viết phần văn liệu**.

**Cách xử lý, đã đổi 15/10:** vì tính mới kiến trúc đã bị thu hẹp nhiều lần, [C-7](../../DECISIONS.md) đề xuất **chuyển chỗ đặt tính mới** sang **nhiệm vụ và benchmark** — nơi chưa tìm thấy tiền lệ và nơi bằng chứng đã đo xong. Xem [bài 8 mục 1.2](08-contribution.md). Thêm ba việc câu chữ `[đề xuất]`:

1. **Sửa ba chỗ** (`topics/degron-footprint/README.md` dòng G3, `research/topic-decision.md §7`, `full-data-audit §6.2`): thay "thứ cả bốn tiền lệ đều không có" bằng *"ma trận 28 × 20 đã từng được tạo — bởi Degformer trên cùng nhãn, và bởi Larsen 2025 cho từng protein đơn lẻ — nhưng **chưa bao giờ dưới một split theo cụm protein, chưa bao giờ kèm trần nhãn đã đo, chưa bao giờ kèm bất định từng ô, và chưa bao giờ có điều kiện theo lớp phơi lộ**"*.
2. **Phát biểu claim theo đúng điều kiện còn sống:** *"mô hình degron mức residue đầu tiên được **giám sát ở mức residue** và **đánh giá ở mức residue** dưới split cụm protein, đối chiếu một trần nhãn đã đo"* — không phải "dự đoán degron mức residue đầu tiên".
3. **Lưu ý [D-012](../../DECISIONS.md) vẫn đòi một đóng góp dương đo được**, nên mô hình vượt 0,4897 (hoặc AUROC vượt 0,7692) **vẫn bắt buộc** — benchmark một mình không đủ.

**Điều vẫn có thể giết nó:** một bài mới xuất hiện trong 8 tuần tới làm đúng "giám sát mức residue trên nhãn degron thực nghiệm, split theo cụm". Không kiểm soát được; cách giảm thiểu duy nhất là **đặt điểm kiểm G2 sớm** và **chạy lại hai truy vấn trên trước khi nộp**.

---

## Rủi ro 6 — thước đo không thống nhất với GVHD

**Vấn đề:** GVHD có thể quen nhìn Pearson trên thang điểm đoạn, vì đó là con số bài báo in. Nhưng ở đó trần chỉ còn **+0,0032**.

**Cách xử lý:** hỏi và thống nhất **trước khi bắt đầu**, ở buổi gặp tuần 6. Đây là một câu cụ thể nên đưa vào bản chuẩn bị.

### Mới 15/10 — ba thứ làm câu hỏi đó sắc hơn

**Một, con số mà GVHD rất có thể neo vào đã có tên và chủ: PAP Pearson 0,79 trên tile TF**, do chính Larsen đo và in `[nguồn]`. Đó là con số **mức tile**, trên thang mà trần cải thiện của đề tài chỉ **+0,0032**.

**Hai, có tiền lệ công bố cho đúng cách trình bày đề tài cần.** [LeBlanc 2026](papers/leblanc-2026.md) đặt **0,555 cạnh 0,568** ngay trong câu kết quả; RECOVER đặt 0,47 cạnh 0,64; ProteinGym nói thẳng *"one cannot expect perfect correlation between experiment and model"* `[đọc]`. Năm 2026, **báo r của mô hình mà không báo r giữa replicate sẽ bị đọc là một lỗi trình bày**.

**Ba, điều nên nói rõ là trần, không phải chỉ số:** trần nhãn Spearman mức ô chỉ **0,6989** còn trần **AUROC mức ô đạt 0,9519** — xếp hạng *mọi* ô thì khó, nhưng *tách ô dương khỏi ô âm* thì nhãn làm rất tốt, và nhiệm vụ của đề tài là cái sau `[đo]`. Đó là lý lẽ đứng sau [C-9](../../DECISIONS.md), đang chờ Trọng.

**Ba câu cụ thể nên đưa vào bản chuẩn bị buổi gặp** `[đề xuất]`:

1. "Thầy muốn con báo **Pearson trên thang điểm đoạn** (thang mà PAP đạt 0,79 và trần cải thiện là +0,003), hay **AUROC mức ô / precision@3 mức residue** (thang mà dư địa đo được là 0,1827 và 0,1617)?" — kèm bảng ba dòng cho thấy hai thang cho hai kết luận trái nhau.
2. "Con dự định đặt **một dòng replicate-vs-replicate trong mọi bảng kết quả** làm trần nhãn, theo cách LeBlanc et al. 2026 và RECOVER làm. Thầy đồng ý đó là cách trình bày đúng, hay muốn con báo số thô?"
3. "Vì n thật của bộ bão hòa là **91 peptide** và đơn vị suy luận là **cụm protein**, con dự định **cam kết trước** rằng phần lớn ablation sẽ không phân biệt được về thống kê, và chỉ báo **một phép so sánh chính**. Thầy chấp nhận cách đó?"

**Điều vẫn có thể giết nó:** nếu GVHD khẳng định Pearson mức đoạn là thước đo duy nhất ông chấp nhận, thì trần đóng góp của đề tài là **+0,003** và **toàn bộ thiết kế phải làm lại**. Đây là lý do câu hỏi này không được để trượt.

---

## Rủi ro 7 — nợ kỹ thuật nhỏ cần dọn

Không nguy hiểm nhưng sẽ gây rắc rối nếu để lâu:

| Việc | Chi tiết |
|---|---|
| 19 footprint đã map accession nhưng chưa khớp peptide, cộng 3 footprint thiếu trình tự | **cần curate** |
| 9 accession chưa lấy được trình tự UniProt | đã loại khỏi phép chia cụm, **không được giả làm singleton** |
| 813 peptide có stop `*` cuối (336 là footprint) | phải mask, **không coi `*` là acid amin**. **Điểm đối chứng mới 15/10:** Degformer đặt `*` làm **token thứ 21** đưa thẳng vào `nn.Embedding`, không mask, và scan bão hòa **không bao giờ** thăm nó — một khác biệt phương pháp cụ thể để nêu `[đọc]` |
| Cụm MMseqs2 trong `interim/` ghi đường dẫn tuyệt đối cũ | chạy lại `prepare_protein_clusters.py` nếu cần ([resources](../../resources/README.md)) |
| Phép chia 80/10/10 qua 5 seed | là **phép thử đo quy mô**, **chưa phải benchmark chính thức được chốt** |
| **Đếm và báo số cụm protein** ở n = 91 và n = 271–322 | **mới 15/10** — đơn vị suy luận, không phải số peptide (rủi ro 1) |
| **Báo cỡ split đã thực hiện ở mức trình tự**, không chỉ tỉ lệ dự định | **mới 15/10** — vì cụm lệch cỡ: một split cụm 80/20 có thể ra 83/17 ở mức trình tự `[đọc]` |
| **Báo cả `--min-seq-id` và `-c` (coverage)** của MMseqs2 trong Methods | **mới 15/10** — ngưỡng trong lĩnh vực chạy từ 20–50% (MMseqs2) tới 40% (CD-HIT) |
| **Thêm một baseline split ngẫu nhiên cạnh kết quả split cụm** | **mới 15/10** — khoảng cách giữa hai cái **là** ước lượng rò rỉ |
| **Nếu tải CSV của Larsen:** thêm `data/raw/SOURCE.md` giữ thông báo MIT + tên repo + tag + DOI Zenodo | **mới 15/10** — điều kiện duy nhất của giấy phép MIT |
| **Nếu nạp checkpoint Degformer:** nó là **pickle** (`weights_only=False`) kèm một `StandardScaler` | **mới 15/10** — nạp nó **thực thi mã tuỳ ý**; xử lý như dữ liệu không tin cậy, thư mục riêng, `python3 -I` |
| **Tra lại Crossref và API pubs của bioRxiv trước khi nộp** | **mới 15/10** — để trích bản chính thức nếu Larsen 2025 được công bố (repo push 01/10/2026, Zenodo có tag "publication release" → **có thể đang in**) `[phân tích]` |

**Điều vẫn có thể giết nó:** không mục nào giết được đề tài; nhưng mục `*` và mục "số cụm" đều có thể **làm sai một con số đã công bố trong luận văn**, nên phải xong trước khi chạy benchmark chính thức.

---

## Tóm lại: việc trước khi viết dòng code huấn luyện đầu tiên

Bản 12/10 có ba việc. Hai đã xong:

| Việc | Trạng thái |
|---|---|
| ~~Tính lực thống kê trên n = 221–322~~ | ✅ **xong 13/10, đủ lực** (0,82–0,94) — nhưng chỉ cho **bộ quét** |
| ~~Kiểm tính ổn định của nhãn~~ | ✅ **xong 13/10**: 75,9% phần dư là nhiễu, phần học được tối đa 8,7% |
| **Tính lực trên n = 91** (bộ bão hòa, nguồn nhãn chính theo [D-025](../../DECISIONS.md#d-025)) | ⬜ **việc chặn duy nhất còn lại** |
| **Thống nhất thước đo với GVHD** ở tuần 6 | ⬜ chưa, và tuần 6 là **16/10** |
| Trọng xác nhận [C-7, C-8, C-9](../../DECISIONS.md) | ⬜ chờ |

Cả ba việc còn lại đều **không cần GPU** và **không cần tải thêm dữ liệu**.

### Thêm 15/10 — danh sách việc đầy đủ, xếp theo chi phí

**Nhóm A — không tốn gì, không cần tải, không cần GPU:**

1. **Tính lực ở n = 91, và đếm số cụm protein.** Việc chặn duy nhất.
2. **Chuẩn bị ba câu hỏi thước đo cho buổi gặp** (rủi ro 6). Cửa sổ này hẹp.
3. **Sửa câu chữ:** thêm Degformer làm tiền lệ **thứ năm** và DegronMD làm tiền lệ đã công bố; xoá khẳng định "không tiền lệ nào xuất ma trận 28×20"; gỡ "batch submission" khỏi danh sách khác biệt G3.
4. **Viết lại kết quả âm "read 10 → 200" thành phát hiện có trích dẫn** (DiMSum + Enrich2).
5. **Chốt bộ thước đo ba tầng và cam kết trước về ablation không phân biệt được.**
6. **Dọn ba mục nợ kỹ thuật rẻ nhất:** mask `*`, chạy lại `prepare_protein_clusters.py`, ghi `--min-seq-id` + `-c` vào Methods.

**Nhóm B — cần tải, vẫn không cần GPU:**

7. **Tải `annotations/transfac_tiles.csv.gz`** (5,77 MB, **giấy phép MIT**) rồi **đếm số dòng có `degron_score`** để có con số tile đúng thay cho 58.781 đang mâu thuẫn.
8. **Đo chồng lặp ở mức trình tự:** bao nhiêu tile 30-mer **chứa trọn** một peptide 23-mer của I28. Con số này sẽ bị hỏi khi bảo vệ.
9. **Chạy lại checkpoint Degformer dưới split cov80** và thước đo mức residue. Thí nghiệm giá-trị-trên-giờ cao nhất đang có.
10. **Tính lại PAP trên ≈ 50.136 tile không chồng** để có con số 0,79 "sạch", và **so QCDPred với thư viện nhân** (chưa tìm thấy ai làm).

**Nhóm C — cần huấn luyện:** ablation 3 nhánh MIL-vs-đầu-theo-vị-trí; ablation ô chéo cổng phơi lộ trên bộ nhân; kiểm độ ổn định trọng số theo vị trí qua seed/bootstrap.

**Cần Trọng quyết (phần C của [DECISIONS.md](../../DECISIONS.md), chưa phải quyết định):** C-7, C-8, C-9 như cũ; **mới:** có **tải và dùng bộ nhân Larsen** làm test chuyển ngăn mức tile hay không; có **gửi email xin xác nhận giấy phép MIT** hay không; và có **nhận Degformer làm baseline chính thức** hay không (nếu có thì phải trích rõ "tự báo, chưa công bố, split ngẫu nhiên", và con số 0,9162/0,9420 phải gọi là **Pearson**, không phải Spearman).

---

[← Bài trước](08-contribution.md) · [Bài sau: Dữ liệu thật →](10-data-up-close.md) · [Về hub](README.md)
