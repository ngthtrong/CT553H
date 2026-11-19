# Rà soát tổng thể CT553H — nghiên cứu, ứng dụng, báo cáo

**Ngày:** 17/11/2026. **Phạm vi:** chỉ đọc. Không chạy campaign, không train,
không load model, không sửa `research/**/output/`, `state.json`, manifest,
checkpoint hay `data/`. Không sửa `report/`, `presentation/`, `reportTemplate/`
trong lượt này; Phần C chỉ bắt đầu sau khi Trọng duyệt.

**Nhãn bằng chứng:** `[ĐO]` = đọc trực tiếp file kết quả trong repo và trích số
nguyên trạng · `[DIỄN GIẢI]` = nhận định của Claude từ các số đó ·
`[NGUỒN]` = số/khẳng định của tác giả khác · `[ĐỀ XUẤT]` = kiến nghị chờ Trọng
duyệt · `[CHƯA XÁC MINH]` = chỉ thấy qua tóm tắt, chưa đối chiếu nguồn gốc.

Mỗi phát hiện dẫn `path:line`. Phát hiện đã kiểm (đọc được file, đếm được, so
được) tách khỏi nhận định đánh giá.

**Giới hạn của chính hồ sơ này.** Đây là rà soát tài liệu và artifact đã lưu,
không phải audit số học độc lập: không tái tính bootstrap, không mở Parquet OOF,
không chạy test của app. Các số được trích từ JSON/README đã có; chỗ nào tái
tính thì ghi rõ. Trạng thái khoa học giữ `development_not_gate_closure`
(`research/lora-refit-transfer-2026-11-16/results.json:4`). Hồ sơ này không đóng
G2/G3, không đổi model phục vụ.

---

## 0. Mười phát hiện cần Trọng đọc trước

| # | Phát hiện | Loại | Bằng chứng |
| --- | --- | --- | --- |
| F-1 | Mục 2.12 (đổi model phục vụ sang LoRA-D) trong `plan.md:163` ghi `[ ]`, nhưng trong `system/app/` **đã có** code phục vụ LoRA-D chưa commit: `backend/degron_footprint/lora.py`, `etl/export_lora.py`, `tests/test_lora.py`, `backend/LORA.md` (`git status --short` cho `??`). Trạng thái thật là "đã triển khai dạng tuỳ chọn, chưa đặt mặc định", không phải "chưa làm" | đã kiểm | `plan.md:163`; `system/app/backend/LORA.md:1-9` |
| F-2 | `system/app/backend/LORA.md:67` dẫn `tests/results/latency-lora.json` cho latency/RAM/kích thước image, **file không tồn tại** (`tests/results/` chỉ có 6 file). Đây là một số liệu được hứa mà chưa có | đã kiểm | `system/app/backend/LORA.md:67`; `ls system/app/tests/results/` |
| F-3 | Parity khác runtime — việc mà `d4-decision-2026-11-17.md:144` và L10 ghi là "chưa làm" — **thực tế đã có** ở phía app: CUDA (Windows) ↔ CPU (WSL), 3 seed, max diff 3,0e-6 (`tests/results/lora-bundle.json`). Biên bản D-4 và `plan.md` chưa phản ánh | đã kiểm | `system/app/tests/results/lora-bundle.json`; `research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md:111,144` |
| F-4 | Kết quả âm ở `gt5` là **kết quả bắt buộc giữ** và đã có phép kiểm riêng: LoRA-D − zero = **+0,0152** [+0,0070; +0,0238], CI hiệu chỉnh [+0,0051; +0,0260], hoàn toàn trên 0 | đã kiểm | `research/lora-refit-transfer-2026-11-16/similarity-findings-2026-11-17.md:65-74` |
| F-5 | Báo cáo đang mâu thuẫn với kết quả 17/11 ở ít nhất 3 chỗ: `report/chapters/conclusion.tex:64` và `report/chapters/sections/question-assessment.tex:33` còn viết "LoRA has not been evaluated on T"; `report/frontmatter/research-status.tex:21` còn liệt "LoRA transfer" là open work | đã kiểm | 3 đường dẫn nêu trong ô |
| F-6 | 5 dấu `[PENDING]` khớp đúng mục 3.1 của `plan.md:178`: `frontmatter/acknowledgements.tex:7`, `appendices/a-installation-user-guide.tex:36,49`, `appendices/b-supplementary-materials.tex:5`, và `chapters/04-testing-evaluation.tex:687` (dòng này là câu văn, không phải marker `[PENDING:` — xem §C-note) | đã kiểm | `grep -rn PENDING report/{chapters,frontmatter,appendices}` |
| F-7 | Tỉ lệ hình/bảng lệch mạnh: PDF hiện tại có **12 hình / 58 bảng** (`content.lof` 12 dòng, `content.lot` 58 dòng), trong đó Chương 4 một mình chiếm **37 bảng**. Đây là vấn đề trình bày lớn nhất của báo cáo | đã kiểm | `report/build/content/content.lof`, `content.lot` |
| F-8 | `research/` có **36 thư mục**; theo phân loại ở §A-6: **16 CHÍNH · 16 PHỤ LỤC · 4 LỊCH SỬ**. Vấn đề không phải số lượng mà là **thành phần**: Chương 4 đang trình bày ở mạch chính 4 thí nghiệm thuộc nhóm PHỤ LỤC (`pretrain-p3`, `recluster-sensitivity`, `r2-esm-features`, `metadegron-analysis`), trong khi kết quả nhánh 1 — căn cứ của D-4 — chưa có mặt | đã kiểm + nhận định | §A-6; `report/chapters/04-testing-evaluation.tex:320-494` |
| F-9 | UC-01…10 không đồng đều về giá trị: UC-02 (ranking trong tile) là tính năng mà **chỉ** nó có bằng chứng định lượng về ích lợi (`oof-prioritization-2026-11-07/results.json`), còn UC-05/09 (import/comparison) chưa có bằng chứng nhu cầu nào trong repo ngoài thiết kế | đã kiểm + nhận định | §B-3 |
| F-10 | Nhóm người dùng trong `system/srs.md:43` nêu 4 nhóm, nhưng chỉ **1** nhóm có bằng chứng quy trình thật trong repo (người thiết kế thư viện đột biến / chọn biến thể để đo). Hai nhóm còn lại là vai trò dự án, không phải người dùng công cụ | đã kiểm + nhận định | `system/srs.md:43`; §B-1 |

---

## Phần A — Đánh giá nghiên cứu

### A-1. Ý tưởng bài toán

**Bài toán đang làm `[ĐO]`.** Hồi quy `ΔPSI = PSI(mutant) − PSI(WT)` cho **một**
phép thay amino acid tại **một** vị trí trên peptide reporter 28 residue, trong
hệ assay GPS của Zhang 2023; gộp 532 ô khác WT thành ma trận 28 × 19/20
(`research/README.md:3`, `research/model-selection-pipeline-2026-10-24/README.md:11`).
Đầu ra phụ là xác suất hiệu chuẩn `P(ΔPSI ≥ 1)`.

**Điều này không phải cái gì `[ĐO]`.** Không phải xác định E3 cụ thể, không
phải phân loại degron/non-degron cho một peptide bất kỳ, không phải dự đoán
kiểu hình protein nguyên vẹn
(`research/model-selection-pipeline-2026-10-24/README.md:11`, `system/srs.md:15,19`).

#### Câu hỏi hội đồng và trạng thái bằng chứng

| Câu hỏi khả năng cao được hỏi | Repo có trả lời chưa | Dẫn chứng |
| --- | --- | --- |
| "ΔPSI là gì, và nó có ý nghĩa sinh học gì?" | **Có**, đủ cho mức luận văn | `report/chapters/02-theoretical-background.tex:74-144` (GPS/PSI, cách dựng hiệu ứng); `research/README.md:3` |
| "Dự đoán trên peptide reporter 28-mer thì nói được gì về protein thật?" | **Có một phần, và giới hạn đã được ghi thẳng** | `system/srs.md:15,48`; `research/wet-lab-evidence-plan-2026-11-07/findings.md:97-101` ghi `[NGUỒN]` rằng một số mutation proline và đuôi PTEN **không** tuân quan hệ đơn giản peptide → abundance |
| "Vì sao không làm luôn mức protein?" | **Có**, bằng số: nhãn mức residue chỉ tồn tại ở thư viện peptide; Larsen cho độ mịn tốt nhất 15 residue, không có nhãn residue | `research/larsen-nuclear-and-risks-2026-10-15/README.md:1,3` |
| "Đã có ai làm đúng việc này chưa?" | **Có, và câu trả lời là CÓ — repo đã tự bác bỏ tuyên bố mới lạ** | `resources/papers/analyzed-papers/degformer-2026.md:18` buộc xoá câu "chưa sản phẩm nào xuất ma trận 28×20" khỏi mọi tài liệu; đã đếm 5 tiền lệ (DEGRONOPEDIA, MetaDegron, Colab PAP, SVM của Zhang, Degformer) |

`[DIỄN GIẢI]` Điểm mạnh nhất của phần ý tưởng **không** phải tính mới của bài
toán, mà là **chất lượng đối chứng**: Degformer dùng `train_test_split` ngẫu
nhiên trên bảng đã trộn và có 4,09% rò rỉ trình tự y hệt đo được, còn đề tài
chia theo cụm protein cov80
(`resources/papers/analyzed-papers/degformer-2026.md:30-36`). Đây là lập luận
đóng góp nên dùng, và nó đã được D-4 chốt đúng hướng: đóng góp thuộc nhóm
**phương pháp và đánh giá**, không phải kiến trúc
(`research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md:16-21`).

`[ĐỀ XUẤT]` Khi bảo vệ, câu đầu tiên về tính mới nên là so sánh **thiết kế đánh
giá** với Degformer, không phải "chưa ai làm". Repo đã có đủ số để làm việc đó.

### A-2. Tính cấp thiết

**Bằng chứng mạnh nhất `[ĐO]`.** Tỉ số chênh gây bệnh/lành tính của biến thể
ClinVar trong vùng degron là **2,15**, sống sót qua Mantel–Haenszel phân tầng
theo protein với 3.114 tầng
(`research/variant-coverage-2026-10-15/README.md:10-11`).

**Hai kết quả âm phải nói kèm `[ĐO]`.** Degron lái ung thư kinh điển phần lớn
**không** hiện ra trong assay này (chỉ HIF1A); và biến thể ClinVar **không**
giàu lên theo *vị trí* trong degron
(`research/variant-coverage-2026-10-15/README.md:15,143`).

**Bằng chứng tiền lệ wet lab `[NGUỒN]`.** 8 nghiên cứu đã được kiểm phần liên
quan: 5 gần degron, 3 protein engineering lân cận. Có tiền lệ model-guided
follow-up (deepDegron 16/21 ca xác nhận; Degpred CBX6/SPOP; PAP PNPO D33V), và
có số nguồn lực (SAMPLE ~6 tháng/5.200 USD chi phí run; ALDE 6 plate/3 vòng)
(`research/wet-lab-evidence-plan-2026-11-07/findings.md:55-140`).

| Câu hỏi hội đồng | Trạng thái | Dẫn chứng |
| --- | --- | --- |
| "Bài toán này có đáng làm không?" | **Có bằng chứng đo được**, không chỉ khẳng định | `variant-coverage-2026-10-15/README.md:10` |
| "Công cụ của em tiết kiệm được bao nhiêu thời gian/chi phí cho phòng thí nghiệm?" | **Chưa có, và đã được ghi là chưa có** | `wet-lab-evidence-plan-2026-11-07/findings.md:9-21`: "Chưa có bằng chứng trực tiếp rằng CT553H tiết kiệm thời gian, chi phí thực nghiệm" |
| "Ít nhất có bằng chứng hồi cứu nào không?" | **Có** | `oof-prioritization-2026-11-07/results.json`: với 10 lựa chọn/peptide, LoRA-D Precision 53,62% (1.260 hit) so W5-D 46,26% và random kỳ vọng 9,78%; cả 2 CI hiệu chỉnh trên 0 (`oof-prioritization-2026-11-07/README.md:9-13`) |

`[DIỄN GIẢI]` Đây là chỗ hội đồng dễ ép nhất, và cách phòng đã có sẵn: tách ba
mức rõ ràng — (1) bài toán cấp thiết: OR 2,15 `[ĐO]`; (2) ưu tiên ứng viên có
ích hồi cứu: Precision@10 53,62% so 9,78% `[ĐO]`; (3) tiết kiệm nguồn lực thật:
**chưa đo, không tuyên bố**. Trả lời đúng ba mức này mạnh hơn mọi cách phóng đại.
`findings.md:119-140` đã phân biệt sẵn số đo / dự báo / mô phỏng của SAMPLE và
ALDE để không bị dẫn sai.

### A-3. Lập luận khoa học

**Trạng thái sau D-4 `[ĐO]`.** Trọng chốt phương án A ngày 17/11: đóng G2 trong
phạm vi development, cho đóng góp nhóm **phương pháp và đánh giá**
(`research/g2-acceptance-2026-11-07/d4-decision-2026-11-17.md:16-21`). GVHD chưa
ghi nhận (`:5`). G3 không đóng, model phục vụ không đổi, `scientific_status` giữ
nguyên (`:126-133`).

**Câu claim được phép dùng, nguyên văn `[ĐO]`** (`:38-41`):

> Trên benchmark development của đề tài, LoRA adaptation của ESM2-35M cho sai số
> thấp hơn cả encoder đóng băng cùng cấu hình và baseline W5-D, trên dữ liệu OOF
> của tập W và khi chuyển sang tập T hậu kiểm cùng nguồn assay.

**Câu bị cấm `[ĐO]`** (`:52-53`): "đã được xác nhận trên nguồn độc lập", "tổng
quát hoá cho degron nói chung", "sẵn sàng triển khai", hoặc bất kỳ câu hàm ý G3
đã đóng.

| Câu hỏi hội đồng | Trạng thái | Dẫn chứng |
| --- | --- | --- |
| "Đóng góp khoa học của em là gì, khi không có kiến trúc mới?" | **Đã có phạm vi chốt trước**: protocol v3 ghi "Không cần kiến trúc mới để đóng góp benchmark/phương pháp/đánh giá/phần mềm" | `research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md:68` |
| "Tại sao LoRA tốt hơn? Cơ chế là gì?" | **Chưa phân giải, và được phép nói vậy** | `research/lora-refit-transfer-2026-11-16/error-results.json:2` `"descriptive_not_causal"`; `plan.md:126` ghi "Cơ chế đầy đủ vẫn **chưa phân giải**" |
| "Lợi thế đó có phải do peptide T giống peptide train không?" | **Đã có phép kiểm, và H-S bị bác trong phạm vi proxy** | `similarity-findings-2026-11-17.md:36-55`: ở bin identity đáy [0; 0,25), 1.093 peptide / 627 nhóm, lợi thế vẫn còn, CI hoàn toàn dưới 0 cả hai contrast; Spearman identity↔ΔMAE ≈ 0 và lệch **ngược** chiều H-S |
| "Vậy có rò rỉ không?" | **Không chứng minh được là không** — ghi rõ | `similarity-findings-2026-11-17.md:57-58`; `reliability-transfer-2026-11-08/README.md:116` ghi hash không phát hiện mọi remote homology / PLM pretraining exposure |
| "Kết quả nào bất lợi?" | **Có, và đã được kiểm riêng** | xem A-5 bảng `gt5` |

`[DIỄN GIẢI]` Chất lượng lập luận ở đây cao hơn mức thường thấy của luận văn đại
học: protocol khoá trước khi chấm (`PROTOCOL.md:1-6` ghi "Khoá trước prediction
LoRA/frozen refit mới trên T"), protocol similarity cũng khoá trước khi tính
(`similarity-findings-2026-11-17.md:3-5` có sha256), và quy ước bất đối xứng của
Koren được ghi **trước** 22/10 rồi tôn trọng sau khi có kết quả yếu
(`d4-decision-2026-11-17.md:113-120`). Đây là điểm nên trình bày thành một mục
riêng, không chỉ nhắc ngang.

**Rủi ro lập luận còn lại `[DIỄN GIẢI]`.** Khoảng cách giữa hai câu "LoRA tốt
hơn frozen trên T" và "công cụ này hữu ích" chưa được lấp bằng bằng chứng, chỉ
bằng suy luận. Phần A-7 xếp đây là khoảng trống quan trọng nhất còn lại.

### A-4. Dữ liệu và xử lý dữ liệu

**Nguồn `[ĐO]`.** Bốn nguồn đã tải đủ với SHA-256 ghim: Mendeley 5/5 file
(~430 MB), GEO GSE240610, repo Voutsinos @`9b3eafa6` (MIT), MaveDB API 26 score
set (`research/full-data-audit/README.md:30-40`). ClinVar 2,56 triệu biến thể
missense (`variant-coverage-2026-10-15/README.md:6`). Koren 2018 S4 có hash khớp
(`plan.md:126` và `lora-refit-transfer-2026-11-16/koren-results.json:320`).

**Dataset v3 đang dùng `[ĐO]`** (`kaggle-roadmap-2026-10-31/DATASET.md:3,10`):

| Thành phần | Số liệu |
| --- | --- |
| ZIP | 98.748.031 byte, sha256 `f4a6542f…` |
| Saturation (W) | 235 peptide / 122.412 ô / 221 nhóm |
| Strata PSI(WT) | ≤3: 91 · (3,4]: 85 · (4,5]: 36 · >5: 23 peptide |
| Scanning | 224.470 ô union replicate |
| Partition scanning | `sat_overlap` 1.278 · `scan_dev` 5.489 · `scan_T` 1.414 peptide |
| T primary cohort | 39.234 ô / 1.410 peptide / 730 nhóm, rep1, chỉ R/A/S |

**Chống rò rỉ — ba lớp `[ĐO]`:**

1. **Chia fold theo cụm protein MMseqs2** id30/cov80, 5 outer fold; cov50 dùng
   kiểm độ nhạy (`metadegron-analysis-2026-10-21/README.md:6`). Một nhóm sinh
   học không đi qua cả train và test trong cùng split
   (`DATASET.md:76`).
2. **Khử trùng sequence trên hợp saturation + scanning**, không theo từng file
   (`DATASET.md:96`). Kiểm được: 351.825 sequence duy nhất, **0** exact
   sequence bị gán vào hai group khác nhau
   (`reliability-transfer-2026-11-08/README.md:31-32`).
3. **Cấm nhãn làm input**: `psi_wt_sat`, `psi_mut`, read count, group ID,
   fold ID, stratum không được là input model chính (`DATASET.md:108`).

**Nhãn T và cách giữ nó sạch `[ĐO]`.** T được chọn **trước** mọi bước học có
giám sát trên scanning, và giữ ngoài data selection, quality weighting,
pretraining, fine-tuning và calibration (`DATASET.md:102`). Khi chấm: assert
`target_columns_passed_to_model: []` và `T_fit_cells: 0` ở cả 6 job score và 6
job refit (`plan.md:106`), calibrator fit từ `fit_population: ensemble_OOF_W`
(`plan.md:109`).

**Nhưng T không phải external độc lập `[ĐO]`.** T đã từng được xem qua W5 và
diagnostic 08/11; `results.json:2897` ghi `limitations[0]`: *"T was previously
examined; not independent external validation."* Protocol cũng ghi điều này
ngay dòng đầu (`PROTOCOL.md:3-6`).

| Câu hỏi hội đồng | Trạng thái | Dẫn chứng |
| --- | --- | --- |
| "Chia train/test thế nào, có rò rỉ không?" | **Trả lời được bằng ba lớp + một phép đếm kiểm được** | 3 mục trên |
| "T là tập test độc lập chứ?" | **Không, và repo nói thẳng là không** — đây là câu trả lời tốt, không phải điểm yếu | `results.json:2897`; `PROTOCOL.md:3-6` |
| "Sao lại bỏ ngưỡng PSI(WT) ≤ 3,0 cũ?" | **Có thí nghiệm riêng, có đăng ký trước, có kiểm độ nhạy 3 phân hoạch** | `learning-curve-2026-10-22/README.md` (P0: +0,0126, CI [+0,0061; +0,0190]); `recluster-sensitivity-2026-10-22/README.md:3` (dương ở cả 3 phân hoạch khác thật) |
| "Dữ liệu tải về có đáng tin không?" | **Có sổ nguồn gốc + hash + quy ước đọc an toàn** | `data/README.md`; `CLAUDE.md` quy ước `python -I`, không chạy mã trong `data/raw/` |
| "Bộ bão hoà và bộ quét có cùng thang không?" | **Đã đo: cùng thang biên, đồng thuận từng ô thấp hơn trần** | `scan-sat-merge-2026-10-23/README.md:11-16`: Pearson quét↔bão hoà 0,70–0,72 so trần 0,82/0,85; mốc WT lệch >0,5 PSI ở 31% peptide |

`[DIỄN GIẢI]` Phần dữ liệu là phần mạnh nhất của đề tài và cũng là phần dễ trình
bày nhất. Đề nghị dành cho nó một mục riêng ở Chương 3 với một sơ đồ funnel duy
nhất (đã có `report/assets/ch4/tab-funnel.tex`, nên chuyển thành hình).

### A-5. Phương pháp và kết quả

**Trình tự thời gian thật, lấy từ tên thư mục / manifest / `git log` `[ĐO]`:**

| Mốc | Việc | Kết quả một dòng | Nguồn ngày |
| --- | --- | --- | --- |
| 11–14/10 | Audit 4 nguồn nhãn, dựng lại PSI từ read thô | 4 nguồn tải đủ, hash ghim; cổng E3 **không** qua | `git log` (`e3-labels-audit` 12/10, `full-data-audit` 14/10) |
| 14/10 | Baseline PAP tái lập | `cnn2w1` 0,8239/0,8690, khớp bài báo 0,82/0,87 đến 4 chữ số | `pap-baseline/README.md:1` |
| 15/10 | Giảm rủi ro mức residue | Ngữ cảnh cục bộ đáng **+0,0289** AUROC [+0,0264; +0,0313]; nhưng thua ΔPAP trên ma trận bão hoà −0,0420 | `residue-task-derisk-2026-10-15/README.md:1` |
| 15/10 | Độ phủ ClinVar | OR 2,15; 2 kết quả âm | `variant-coverage-2026-10-15/README.md:1` |
| 18/10 | G2 học trực tiếp trên ma trận bão hoà | Ridge M3 **0,8082** > ΔPAP 0,7693 (+0,0389 [+0,0216; +0,0571]); mạng có gate **thua** ridge | `g2-saturation-2026-10-18/README.md:1` |
| 18/10 | G2 mở rộng, 3 câu hỏi còn mở | **Cả ba trả lời bất lợi cho tuyên bố kiến trúc**; nút thắt là lượng nhãn, không phải sức chứa | `g2-extension-2026-10-18/README.md:1,5` |
| 22/10 | P0/P1 đường cong học + nới ngưỡng | P0 nhận: 0,8082 → **0,8208**; P1 chỉ hỗ trợ một nửa (ridge đã phẳng từ ~35 cụm) | `learning-curve-2026-10-22/README.md:1` |
| 22/10 | P2 Koren S4 | **Cổng không đạt**: chỉ 5 cụm cov80 mới (cần ≥20) | `koren-s4-audit-2026-10-22/README.md:1,5` |
| 22/10 | P3 pretrain nhãn tile | **Âm**: `pre` 0,8098 < `rand` 0,8175 < ridge 0,8208 | `pretrain-p3-2026-10-22/README.md:1,5` |
| 22/10 | P6 calibration Platt | **Nhận**: Brier 0,0925 so 0,1272 thô, CI [+0,0266; +0,0425]; top-10% làm giàu 4,02× | `calibration-p6-2026-10-22/README.md:1,5` |
| 22/10 | R0 tái lập trên Kaggle | 12/12 cổng, tái lập bit-bit trên nền tảng khác | `r0-reproduce-notebook-2026-10-22/README.md:3` |
| 22/10 | R2 ESM-2 650M frozen + ridge | **Chưa đủ bằng chứng**: +0,0022 [−0,0033; +0,0082]; bỏ 2 peptide thì Δ = −0,0004 | `r2-esm-features-2026-10-22/README.md:1,9` |
| 22/10 | R3 cổng miền | **Cả hai tầng dùng được**: AUROC 0,911 / 0,815; ~65% tile sàng out-of-domain | `r3-domain-gate-2026-10-22/README.md:1,13` |
| 22–23/10 | R1 Degformer sạch cụm | **Không phân biệt được**: 0,8068 so ridge 0,8208 (−0,0140 [−0,0283; +0,0010]); checkpoint công bố bị rò, phồng 0,118 | `r1-degformer-clean-2026-10-22/README.md:1,24-28` |
| 23/10 | R6 ladder scan, 23 cấu hình | **Phép xác nhận P chưa đạt**; ridge ±5 = 0,8286 được nhận ở mức họ | `r6-ladder-scan-2026-10-23/README.md:1`; `next-phase-plan-2026-10-22/README.md:28` |
| 23/10 | Trộn scanning + bão hoà | **Không giúp**: S1−A1 = −0,0019 [−0,0057; +0,0017] | `scan-sat-merge-2026-10-23/README.md:11-16` |
| 31/10–06/11 | Campaign v3 full-PSI, 633 job, 88 cấu hình OOF | LoRA−frozen cùng runtime: B/MAE −0,0397, D/MAE −0,0254, CI hiệu chỉnh không cắt 0 | `kaggle-roadmap-2026-10-31/local-output-analysis.md:1,23-29` |
| 06/11 | W5-D trên T | **Chưa đủ bằng chứng** giảm MAE so zero: −0,003256 [−0,009249; +0,002760] | `local-output-analysis.md:93-104` |
| 07/11 | Ưu tiên mutation cùng ngân sách | Precision@10: 53,62% / 46,26% / 9,78%; 2/2 CI hiệu chỉnh trên 0 | `oof-prioritization-2026-11-07/README.md:9-13` |
| 08/11 | Độ tin cậy + giới hạn chuyển miền (CPU) | Matched LoRA–frozen bền; W5 trên T **chưa** xác nhận lợi thế so zero | `reliability-transfer-2026-11-08/README.md:19-26` |
| 16–17/11 | Refit/transfer nhánh 1, 17 mục | **LoRA-D trên T: MAE 0,3470**; hai contrast chính CI hiệu chỉnh dưới 0 | `lora-refit-transfer-2026-11-16/results.json:1109` |
| 17/11 | Phân rã sai số + similarity | H-S bị bác; **kết quả âm gt5 được xác nhận** | `similarity-findings-2026-11-17.md:50,72` |
| 17/11 | Koren khảo sát | macro Spearman LoRA 0,061 / frozen 0,022 trên 9 substrate / 1.739 mutant | `koren-results.json:304-318` |
| 17/11 | D-4 | Phương án A, đóng G2 phạm vi development | `d4-decision-2026-11-17.md:16` |

**Kết quả nhánh 1 trên T, đầy đủ `[ĐO]`** (`results.json`, 1.410 peptide / 730
nhóm / 39.234 ô):

| Recipe | MAE | RMSE | Spearman | AUROC+ | Brier 3 lớp |
| --- | ---: | ---: | ---: | ---: | ---: |
| LoRA-D | **0,3470** | 0,4297 | 0,4637 | 0,9083 | 0,1100 |
| frozen-D | 0,3875 | 0,4798 | 0,4134 | 0,8745 | 0,1271 |
| W5-D | 0,3991 | 0,4942 | 0,3781 | 0,8405 | 0,1291 |
| zero | 0,4024 | 0,5142 | — | 0,5 | — |
| constant-W-mean | 0,4175 | 0,5215 | — | 0,5 | — |

| Contrast (family 2, Bonferroni, CI 97,5%) | ΔMAE | CI hiệu chỉnh |
| --- | ---: | --- |
| LoRA-D − frozen-D | −0,0405 | [−0,0455; −0,0356] |
| LoRA-D − W5-D | −0,0522 | [−0,0577; −0,0469] |

**Kết quả âm, phải giữ nguyên `[ĐO]`** (`results.json` → `metrics.*.strata`,
`similarity-findings-2026-11-17.md:65-74`):

| Strata PSI(WT) | n peptide | zero MAE | LoRA-D MAE | LoRA-D − zero, CI hiệu chỉnh |
| --- | ---: | ---: | ---: | --- |
| le3 | 524 | 0,4319 | 0,3303 | −0,1016 |
| gt3_le4 | 323 | 0,4158 | 0,3505 | −0,0653 |
| gt4_le5 | 306 | 0,3843 | 0,3589 | −0,0253 |
| **gt5** | **257** | **0,3470** | **0,3622** | **+0,0152 [+0,0051; +0,0260]** |

`[ĐO]` Ở gt5, baseline đoán 0 **tốt hơn** LoRA-D, CI hoàn toàn trên 0 kể cả sau
hiệu chỉnh. W5-D (0,4428) và frozen-D (0,4436) còn kém hơn nữa. Bảng bias giải
thích liên hệ: ở gt5 target mean là **−0,176** trong khi prediction mean là
**+0,181** (`error-results.json:30-42`), tức mô hình vẫn dự đoán chiều dương ở
vùng hiệu ứng đo được là âm. `[DIỄN GIẢI]` Đây là liên hệ mô tả, chưa phải cơ
chế; `error-results.json:2` giữ `"descriptive_not_causal"`.

| Câu hỏi hội đồng | Trạng thái | Dẫn chứng |
| --- | --- | --- |
| "Vì sao chọn LoRA mà không fine-tune toàn bộ?" | **Có lý do chi phí ghi trước** (~40 h GPU, cắt khỏi phạm vi) nhưng **chưa có phép so** | `plan.md:129`; `question-assessment.tex:28` ghi "Full fine-tuning is not evaluated" |
| "Ba seed có phải ba lần thí nghiệm độc lập không?" | **Không, và được ghi rõ ở nhiều nơi** | `results.json:2897` L2; `g2-acceptance-2026-11-07/README.md:43`; `r2-esm-features-2026-10-22/README.md:11` |
| "Khoảng tin cậy của em bao gồm bất định nào?" | **Chỉ điều kiện trên dự đoán đã fit**, không gồm bất định train/chọn model — ghi rõ | `results.json` → `limitations`; `PROTOCOL.md:62-63` |
| "Mô hình có hiệu chuẩn tốt không?" | **Hỗn hợp, và được báo cả hai chiều** | Brier LoRA 0,1100 < W5 0,1291 nhưng ECE+ LoRA 0,0523 **kém** W5 0,0384 (`d4-decision-2026-11-17.md:106` L5) |
| "Chiều ΔPSI âm (đột biến làm mất ổn định) thì sao?" | **Yếu, và được báo** | AUROC− 0,5932, chỉ 85 peptide đủ điều kiện (L6) |
| "Cổng R3 đã dùng trong đánh giá nghiên cứu chưa?" | R3 là cổng **miền áp dụng cho công cụ**, không phải bước của pipeline đánh giá | `r3-domain-gate-2026-10-22/README.md:1` |

### A-6. Phân loại 36 thư mục `research/`

Ngày lấy từ: tên thư mục · `git log --diff-filter=A` cho đường dẫn lịch sử
`topics/degron-footprint/research/<tên>` (các thư mục không có ngày trong tên) ·
README của chính thư mục.

**Phân loại:** `CHÍNH` = thuộc mạch lập luận luận văn, phải có trong Chương 3/4 ·
`PHỤ LỤC` = cần cho tái lập hoặc minh bạch, xuống phụ lục · `LỊCH SỬ` = đã bị
thay thế, là ngõ cụt không mang thông tin mới, hoặc trùng lặp.

| Thư mục | Ngày (nguồn) | Mục đích | Kết luận | Phân loại | Lý do |
| --- | --- | --- | --- | --- | --- |
| `e3-labels-audit` | 11–12/10 (`git log`) | Đếm nhãn E3 dùng được | **Cổng E3 không qua**; nhãn residue lớn hơn tài liệu cũ | PHỤ LỤC | Lý do **chuyển hướng** khỏi đề tài E3-specificity; cần để giải thích phạm vi, nhưng không thuộc mạch kết quả |
| `voutsinos-2026-audit` | 11/10 (`git log`) | Audit nguồn Voutsinos + tái lập | Nguồn MIT dùng được; holdout 527 gene thực tế chỉ 428 hiệu dụng | PHỤ LỤC | Cung cấp baseline PAP và cảnh báo holdout; chi tiết thuộc phụ lục |
| `composition-context-audit.md` | 12/10 (file) | Khoảng trống thành phần ↔ ngữ cảnh | 2.046/2.624 footprint cùng vị trí+thay thế nhưng chênh ΔPSI ≥1 | **CHÍNH** | Đây là **lập luận nền** cho việc bài toán cần ngữ cảnh, không chỉ thành phần |
| `full-data-audit` | 13–14/10 (`git log`) | Tải đủ 4 nguồn, dựng lại PSI | 4 nguồn đủ hash; PSI dựng lại được | **CHÍNH** | Sổ dữ liệu gốc của luận văn |
| `architecture-check` | 14/10 (README:3) | Kiểm tiền đề kiến trúc MIL | 2/4 tiền đề kiểm được; **tiền đề đã có trong y văn**; 2 lỗi phương pháp tự phát hiện | LỊCH SỬ | Kiến trúc MIL đã bị bỏ; README tự cảnh báo không dùng số +0,6625. Giữ làm bản ghi |
| `pap-baseline` | 14/10 (README:3) | Tái lập ΔPAP + chấm trên footprint | Khớp bài báo 4 chữ số; ΔPAP yếu hơn baseline thành phần | **CHÍNH** | Baseline đối chứng công bố duy nhất; `pap_baseline.py` còn được import |
| `residue-task-derisk-2026-10-15` | 15/10 | Giảm rủi ro nhiệm vụ mức residue | **+0,0289** ngữ cảnh; nhưng thua ΔPAP trên ma trận | **CHÍNH** | Con số dương đầu tiên + `residue_data.py` là loader dùng chung của nhiều script |
| `variant-coverage-2026-10-15` | 15/10 | Tính cấp thiết bằng ClinVar | OR 2,15 + 2 kết quả âm | **CHÍNH** | Lập luận cấp thiết duy nhất dựa trên số đo |
| `larsen-nuclear-and-risks-2026-10-15` | 15/10 | Bộ nhân Larsen + 9 rủi ro | Dùng được (MIT) nhưng **không có nhãn residue**; Degformer là tiền lệ thứ 5 | PHỤ LỤC | Nguồn của nhiều cảnh báo phương pháp; nội dung chính đã hấp thu vào quy ước repo |
| `slide-figures-2026-10-15` | 15/10 | Sinh ma trận ví dụ từ dữ liệu | HIF1A 553–580, 529 ô / 186 dương | PHỤ LỤC | Hình minh hoạ ma trận; hữu ích cho báo cáo/slide |
| `g2-saturation-2026-10-18` | 18/10 | Benchmark G2 gốc | Ridge M3 **0,8082**; mạng gate thua ridge | **CHÍNH** | Benchmark nền của mọi so sánh sau; nhưng population khác W v3 — phải trình bày riêng |
| `g2-extension-2026-10-18` | 18/10 | 3 câu hỏi còn mở của G2 | **Cả 3 bất lợi**; nút thắt là lượng nhãn | **CHÍNH** | Ba kết quả âm có giá trị lập luận cao; là lý do bỏ hướng kiến trúc |
| `metadegron-analysis-2026-10-21` | 21/10 | Audit MetaDegron | Trùng 2 peptide (quét) / 1 (bão hoà); "21 E3" không có nhãn độc lập | PHỤ LỤC | Định vị so với công cụ khác; 47 file chi tiết không thuộc mạch chính |
| `learning-curve-2026-10-22` | 22/10 | P0 nới ngưỡng + P1 đường cong học | P0 **nhận**; P1 hỗ trợ một nửa | **CHÍNH** | P0 là quyết định dữ liệu lớn nhất của đề tài (91 → 176 → 235 peptide) |
| `recluster-sensitivity-2026-10-22` | 22/10 | Độ nhạy phân hoạch của P0 | Dương ở cả 3 phân hoạch khác thật | PHỤ LỤC | Kiểm độ nhạy của P0 — cần cho minh bạch, không cần ở mạch chính |
| `koren-s4-audit-2026-10-22` | 22/10 | Audit Koren + cổng P2 | Dữ liệu đọc được, khớp 1.827/1.827; **cổng P2 không đạt** | PHỤ LỤC | Nền cho quy ước bất đối xứng Koren (dùng ở D-4) và cho mục 1.14 |
| `pretrain-p3-2026-10-22` | 22/10 | Pretrain nhãn tile Voutsinos | **Âm** | PHỤ LỤC | Kết quả âm có đăng ký trước — đáng giữ, nhưng là ngõ cụt đã đóng |
| `calibration-p6-2026-10-22` | 22/10 | Platt + nguyên mẫu G3 | **Nhận**; làm giàu 4,02× | **CHÍNH** | Nguồn gốc của mô hình phục vụ `m3-ext4.0-platt-v1` đang chạy trong app |
| `r0-reproduce-notebook-2026-10-22` | 22/10 | Tái lập mốc trên Kaggle | 12/12 cổng, bit-bit | PHỤ LỤC | Bằng chứng tái lập — thuộc mục reproducibility ở phụ lục |
| `r1-degformer-clean-2026-10-22` | 22–23/10 | Degformer sạch cụm | **Không phân biệt được**; rò rỉ phồng 0,118 | **CHÍNH** | Đối chứng với tiền lệ trực diện nhất; con số 0,118 là lập luận mạnh |
| `r2-esm-features-2026-10-22` | 22/10 | ESM-2 650M frozen + ridge | **Chưa đủ bằng chứng** (+0,0022) | PHỤ LỤC | Kết quả null đã bị v3 thay bằng khảo sát 9 pLM đầy đủ |
| `r3-domain-gate-2026-10-22` | 22/10 | Cổng miền cho công cụ | **Cả hai tầng dùng được** | **CHÍNH** | Cổng này **đang chạy trong app** (`gate-r3-v1.npz`); thuộc cả Chương 3 và 4 |
| `r6-ladder-scan-2026-10-23` | 23/10 | 23 cấu hình biểu diễn × đầu | Phép xác nhận P **chưa đạt**; ridge ±5 nhận ở mức họ | PHỤ LỤC | Là nguồn của baseline W5 dùng ở v3; chi tiết 8 giai đoạn không cần ở mạch chính |
| `scan-sat-merge-2026-10-23` | 23/10 | Trộn hai nguồn nhãn | **Không giúp**; nhưng scanning là tập chấm điểm 1.514 cụm | PHỤ LỤC | Lý do T là scanning chứ không phải train data — cần một câu ở mạch chính, chi tiết ở phụ lục |
| `model-selection-pipeline-2026-10-24` | 24/10 | Khung tổ chức lập luận | Chỉ mục, không phải thí nghiệm mới | LỊCH SỬ | README tự ghi là "vai trò đối chiếu 03/11"; đã bị `research/README.md` thay |
| `next-steps-plan-2026-10-22` | 22/10 | Kế hoạch P0–P6 | P0/P6 nhận, P2/P3 âm, P4/P5 không chạy | LỊCH SỬ | Kế hoạch đã thực hiện xong; kết quả nằm ở thư mục riêng |
| `next-phase-plan-2026-10-22` | 22/10 | Kế hoạch R0–R6 | Đã thực hiện R0–R3, R6 | LỊCH SỬ | Như trên; chỉ 1 file README |
| `notebook-kit-2026-10-22` | 22/10 | Hạ tầng notebook v1/v2 | Gói mã + dữ liệu, PROTOCOL khoá bằng sha256 | PHỤ LỤC | Cơ chế khoá protocol bằng hash đáng nhắc một câu ở phần phương pháp |
| `kaggle-roadmap-2026-10-31` | 31/10–17/11 | **Campaign v3 full-PSI**, 633 job | 88 cấu hình OOF; LoRA−frozen CI không cắt 0; W5-D trên T chưa hơn zero | **CHÍNH** | Thí nghiệm chủ lực của luận văn |
| `output-review-2026-11-06` | 06/11 | Rà soát toàn bộ output | 88 cấu hình, kiểm kê vật lý, hash | PHỤ LỤC | Bằng chứng toàn vẹn — thuộc phụ lục reproducibility |
| `progress-review-2026-11-06` | 06/11 | Audit độc lập + sửa báo cáo | Tái tính OOF local trực tiếp | PHỤ LỤC | Audit chéo; `experiment-history.md` và `literature-audit.md` hữu ích cho Phần C1 |
| `g2-acceptance-2026-11-07` | 07/11 + 17/11 | Rà nghiệm thu G2 + **biên bản D-4** | Phương án A, L1–L10 | **CHÍNH** | `d4-decision-2026-11-17.md` quyết định phạm vi mọi claim của Chương 4 |
| `wet-lab-evidence-plan-2026-11-07` | 07/11 | Tra cứu bằng chứng wet lab | 8 nghiên cứu; có tiền lệ, **chưa** có hiệu quả kinh tế CT553H | **CHÍNH** | Nguồn duy nhất trả lời câu hỏi "ai dùng và để làm gì"; cần cho Chương 1 và Phần B |
| `oof-prioritization-2026-11-07` | 07/11 | Ưu tiên mutation cùng ngân sách | Precision@10 53,62% so 9,78% | **CHÍNH** | Bằng chứng ích lợi gần người dùng nhất mà đề tài có |
| `reliability-transfer-2026-11-08` | 08/11 (`git log` 13/11) | Độ tin cậy + giới hạn chuyển miền | Matched bền; W5 trên T chưa xác nhận; `NEXT-EVALUATION.md` thiết kế bước sau | PHỤ LỤC | `NEXT-EVALUATION.md` là nguồn của protocol refit — nhắc một câu; diagnostic chi tiết xuống phụ lục |
| `lora-refit-transfer-2026-11-16` | 16–17/11 | **Nhánh 1: refit/transfer/parity/Koren/similarity** | LoRA-D trên T MAE 0,3470; gt5 âm; H-S bị bác | **CHÍNH** | Kết quả mới nhất và là căn cứ của D-4 |

**Tổng: 16 CHÍNH · 16 PHỤ LỤC · 4 LỊCH SỬ** = 36 (tính cả
`composition-context-audit.md`). Đếm bằng `grep -c` trên chính bảng trên.

> **Đính chính 18:40.** Bản đầu của hồ sơ này ghi sai "8 CHÍNH · 13 PHỤ LỤC ·
> 15 LỊCH SỬ" ở dòng tổng kết và ở F-8 — đó là lỗi cộng của Claude, **không**
> phải thay đổi phân loại. Từng dòng trong bảng trên giữ nguyên, không ô nào bị
> sửa. Chỉ có 4 thư mục thuộc nhóm LỊCH SỬ: `architecture-check`,
> `model-selection-pipeline-2026-10-24`, `next-steps-plan-2026-10-22`,
> `next-phase-plan-2026-10-22`. Trọng đã duyệt D-A dựa trên bảng, nên phạm vi
> duyệt không đổi; chỉ con số tổng được sửa.

`[DIỄN GIẢI]` Chương 4 hiện tại đi ngược tỉ lệ này: nó trình bày chi tiết cả
`pretrain-p3`, `recluster-sensitivity`, `r2-esm-features`, `metadegron-analysis`
ở mạch chính (`report/chapters/04-testing-evaluation.tex:320-494`), trong khi kết
quả nhánh 1 — thứ mà D-4 dựa vào — chưa có mặt. Đây là việc chính của C1.

### A-7. Còn thiếu gì, và có thật sự cần không

| # | Việc còn thiếu | Cần GPU/train? | Chi phí | Có cần cho phạm vi luận văn? | Nếu bỏ qua thì sao |
| --- | --- | --- | --- | --- | --- |
| G-1 | **Ghi nhận của GVHD cho biên bản D-4** | Không | 1 buổi gặp | **CẦN — đây là việc chặn duy nhất của nghiên cứu** | D-4 ghi "GVHD chưa ghi nhận" (`d4-decision-2026-11-17.md:5`); claim G2 trong luận văn thiếu một bên xác nhận |
| G-2 | **Đồng bộ trạng thái parity khác runtime** giữa `plan.md`/D-4 và bằng chứng thật ở app | Không | 1–2 h đọc + sửa tài liệu | **CẦN** | L10 và `plan.md` đang nói "chưa làm" trong khi `tests/results/lora-bundle.json` đã có; bị hỏi sẽ không trả lời được nhất quán |
| G-3 | `tests/results/latency-lora.json` bị dẫn nhưng không tồn tại | Không (CPU) | ~30 phút chạy `tests/measure_latency_lora.py` | **CẦN** nếu còn trình bày LoRA-D ở báo cáo | Một số liệu được hứa mà không có file — đúng loại lỗi hội đồng hay bắt |
| G-4 | Cơ chế của kết quả âm `gt5` | Không bắt buộc GPU (phân tích CPU được) | 1–2 ngày | **KHÔNG BẮT BUỘC** — được phép kết luận "chưa phân giải" | `plan.md:126` và `error-results.json:2` đã cho phép; chỉ cần trình bày trung thực. Rủi ro: hội đồng hỏi "sao không giải thích được" → trả lời bằng 4 giả thuyết đã kiểm |
| G-5 | `source_pending` (nguồn ngoài thật) | Có, nếu nhập train | — | **KHÔNG** — đã được D-4 giữ nguyên trạng thái | `d4-decision-2026-11-17.md:129`: "Không đóng `source_pending`". Koren là khảo sát, không thay nguồn ngoài. Bỏ qua là **đúng phạm vi**, không phải thiếu sót |
| G-6 | `structure_pending` / SaProt | Có | — | **KHÔNG** — đã cắt khỏi phạm vi có lý do | `plan.md:129`: chỉ có 8 cấu trúc AlphaFold, giả định WT-3Di yếu |
| G-7 | Full fine-tuning so với LoRA | **Có, ~40 h GPU** | — | **KHÔNG** — đã cắt | `plan.md:129`. Nhưng nên viết **một câu** ở phần giới hạn: lợi ích LoRA so full-FT chưa được đo |
| G-8 | Wet lab / prospective validation | Không áp dụng | — | **KHÔNG** — đã cắt, và không được tự thêm thành điều kiện | `plan.md:129`; `CLAUDE.md` cấm tự thêm wet lab vào điều kiện ghi nhận đóng góp |
| G-9 | Ablation: LoRA rank / vị trí adapter | Có | 4–8 h GPU | **KHÔNG BẮT BUỘC** | Protocol đã khoá r=8/alpha=16/query+value (`PROTOCOL.md:27`). `[DIỄN GIẢI]` Nếu hội đồng hỏi "sao chọn r=8", trả lời là lựa chọn khoá trước, không phải tối ưu — trung thực hơn là chạy thêm |
| G-10 | G3 (nghiệm thu nghiên cứu cho model phục vụ) | Có nếu đổi model | — | **KHÔNG trong lượt này** | `d4-decision-2026-11-17.md:126`: G3 thuộc refit/export/tích hợp + nghiệm thu phần mềm, đi theo quy trình riêng |

`[DIỄN GIẢI]` Kết luận Phần A-7: **không có khoảng trống nghiên cứu nào cần GPU
hay train thêm để bảo vệ được**. Ba việc chặn (G-1, G-2, G-3) đều là tài liệu và
chạy CPU. Đây là tin tốt cho lịch còn lại.

---

(Phần B tiếp theo trong cùng file — xem dưới.)

## Phần B — Đánh giá ứng dụng

### B-1. Đối tượng người dùng

**SRS đang nêu `[ĐO]`** (`system/srs.md:43`): (a) researcher cần shortlist có
truy vết và đối chiếu với phép đo của họ; (b) computational researcher cần
export có cấu trúc; (c) tác giả duy trì model/dữ liệu/phần mềm; (d) GVHD đánh
giá bằng chứng và phạm vi. Thêm: *"The local workspace has one trusted operator,
with no account/permission model."*

`[DIỄN GIẢI]` Bốn nhóm này **không cùng loại**. (c) và (d) là **vai trò trong dự
án CT553H**, không phải người dùng của công cụ dự đoán — GVHD không dùng tool để
chọn đột biến. Giữ họ trong danh sách stakeholder là đúng theo mẫu SRS, nhưng
khi viết Chương 1/3 của luận văn thì **không** được đếm họ thành "đối tượng
người dùng", vì sẽ bị hỏi ngay "GVHD dùng tính năng nào?".

**Nhóm thực sự dùng công cụ dự đoán PSI cho peptide reporter degron
`[DIỄN GIẢI, dựa trên `[NGUỒN]` đã kiểm]`:**

| Nhóm | Dùng ở bước nào | Bằng chứng nhóm này tồn tại |
| --- | --- | --- |
| **U-1. Người thiết kế thư viện đột biến / chọn biến thể để đo** (nhóm chính) | Trước khi làm thực nghiệm: có ngân sách N giếng/biến thể, cần chọn N ô nào trong 532 ô của một tile | **Tiền lệ đã kiểm:** deepDegron chọn mutation theo tiêu chí mô hình rồi thử 21 peptide (`wet-lab-evidence-plan-2026-11-07/findings.md:57-66`); ALDE dành 2/6 plate cho model-proposed variants (`:135-139`). **Bằng chứng ích lợi của chính đề tài:** `oof-prioritization-2026-11-07/results.json` |
| **U-2. Người diễn giải dữ liệu DMS/saturation đã có** | Sau khi đo: có ma trận đo, cần biết ô nào lệch dự đoán, ô nào chưa đo | UC-05/UC-09 (`system/srs.md:89,105`). `[DIỄN GIẢI]` Chưa tìm thấy bằng chứng **nhu cầu** của nhóm này trong repo — chỉ có thiết kế đáp ứng nó |
| **U-3. Người sàng vùng degron trên một protein quan tâm** | Thăm dò: có một accession, muốn biết vùng nào đáng làm reporter | UC-04/UC-08 (`:85,101`). **Cảnh báo định lượng:** cổng R3 cho ~65% tile tự chọn là out-of-domain (`r3-domain-gate-2026-10-22/README.md:13,22`) ⇒ nhóm này sẽ bị từ chối phần lớn truy vấn |
| **U-4. Người đọc luận văn / tái lập** | Sau khi nộp: xem model card, nguồn, giới hạn | UC-07 (`:97`) |

`[ĐỀ XUẤT]` Trong báo cáo, nêu **U-1 là nhóm người dùng chính**, U-2 và U-3 là
phụ, U-4 là yêu cầu minh bạch. Không nêu 4 nhóm ngang hàng như SRS hiện tại.

### B-2. Tính thực tế của nhu cầu

**Đã kiểm chứng `[NGUỒN]`:**

1. **Có tiền lệ model-guided follow-up trong chính lĩnh vực degron.** 5 nghiên
   cứu degron được kiểm phần liên quan đều có đối chứng sinh học
   (`findings.md:9-21,55-115`).
2. **Có công cụ tương tự đang tồn tại** — tức nhu cầu tra cứu degron là thật, đã
   được thị trường xác nhận: DEGRONOPEDIA, MetaDegron, Colab của nhóm PAP, SVM
   của nhóm Zhang, Degformer
   (`resources/papers/analyzed-papers/degformer-2026.md:18-22`).
3. **Nhưng không công cụ nào trong số đó làm đúng việc này tốt.** DEGRONOPEDIA
   là tra cứu cái đã biết, **không** dự đoán ảnh hưởng đột biến mức residue và
   **không** xuất ma trận vị trí × amino acid
   (`resources/papers/analyzed-papers/degronopedia-2024.md:31`). Degformer có
   xuất ma trận 28×20 nhưng chia train/test ngẫu nhiên và có 4,09% rò rỉ trình
   tự y hệt đo được, tập blind vắng khỏi repo nên số headline không tái lập được
   (`degformer-2026.md:30-40`).

**Chưa kiểm chứng / là giả định `[DIỄN GIẢI]`:**

4. **Chưa có bằng chứng CT553H tiết kiệm thời gian hay chi phí**
   (`findings.md:9-21` nói thẳng). Bằng chứng gần nhất là hồi cứu OOF
   (Precision@10 53,62% so random 9,78%), **không** phải phép đo nguồn lực.
5. **Chưa có người dùng thật nào dùng app này.** Không tìm thấy bất kỳ bản ghi
   phỏng vấn, khảo sát hay phiên dùng thử nào trong repo.
   `[DIỄN GIẢI]` Đây là giới hạn phải ghi, không phải lỗi phải che.
6. `[CHƯA XÁC MINH]` Không tra web trong lượt này, nên không có đối chiếu cập
   nhật về công cụ mới xuất hiện sau các bản audit của repo.

**Giới hạn phải nêu thẳng trong báo cáo `[ĐO]`:**

| Giới hạn | Nguồn |
| --- | --- |
| Model phục vụ là `m3-ext4.0-platt-v1` ở mức **development**, không phải validated | `system/app/etl/params.yaml:9`; `system/srs.md:47` |
| Chạy **local, một người dùng tin cậy**, không có tài khoản/phân quyền | `system/srs.md:43,65` (CON-8: một instance loopback) |
| **Không xếp hạng sinh học xuyên tile** — ranking chỉ có nghĩa trong một tile | `system/srs.md:77` (UC-02); `plan.md:118` (2.5) |
| ~65% tile tự chọn từ proteome bị cổng R3 xếp out-of-domain | `r3-domain-gate-2026-10-22/README.md:22` |
| Không dự đoán kiểu hình protein nguyên vẹn; không xác định E3; không suy diễn bệnh/điều trị | `system/srs.md:15,19` |
| Import **không bao giờ** retrain; dữ liệu import không tự thành validation độc lập | `system/srs.md:19,105`; CON-3 (`:60`) |

### B-3. Đối chiếu 10 UC với nhu cầu

| UC | Nội dung | Phục vụ nhóm nào | Có bằng chứng ích lợi? | Xếp loại |
| --- | --- | --- | --- | --- |
| UC-01 Ma trận hiệu ứng | 532 ô + cảnh báo miền trước điểm | U-1, U-2, U-3 | Gián tiếp: đây là đầu ra của mô hình đã benchmark | **CỐT LÕI** |
| UC-02 Xếp hạng + shortlist | Sắp/lọc trong tile, top 10%, shortlist | **U-1** | **Có, định lượng**: Precision@10 53,62% so 46,26% (W5-D) và 9,78% (random), 2/2 CI hiệu chỉnh trên 0 (`oof-prioritization-2026-11-07/README.md:9-13`) | **CỐT LÕI — mạnh nhất** |
| UC-03 Export có provenance | CSV/JSON/bundle, model id, nguồn, nhãn development | U-1, U-2, U-4 | Gián tiếp: điều kiện để kết quả dùng được ngoài app | **CỐT LÕI** |
| UC-04 Chọn protein + tile | Tìm theo gene/accession, trạng thái miền | U-3 | Gián tiếp | PHỤ TRỢ |
| UC-05 So với dữ liệu đo | Đối chiếu dự đoán ↔ phép đo, residual | U-2 | **Chưa có bằng chứng nhu cầu trong repo** | PHỤ TRỢ |
| UC-06 ClinVar + annotation | Biến thể missense, classification, disclaimer | U-2, U-3 | **Có, định lượng về mức liên quan**: OR 2,15 (`variant-coverage-2026-10-15/README.md:10`) — nhưng kèm 2 kết quả âm (`:15`) | PHỤ TRỢ (quan trọng cho lập luận cấp thiết) |
| UC-07 Model/data provenance | Model card, nguồn, giấy phép, giới hạn | U-4, GVHD | Gián tiếp: bắt buộc theo CON-1…3, NFR-15 | **CỐT LÕI (bắt buộc)** |
| UC-08 Batch / toàn protein | Tiling step 23, job bền, huỷ, phục hồi | U-1, U-3 | Gián tiếp. **Nhưng đây là nơi tập trung công sức kỹ thuật lớn nhất** (job bền + phục hồi sau SIGKILL) | **CỐT LÕI** |
| UC-09 Import dữ liệu thực nghiệm | CSV/TSV, map về ô, commit bất biến | U-2 | **Chưa có bằng chứng nhu cầu trong repo** | PHỤ TRỢ |
| UC-10 Projects + history | CRUD, snapshot, mở lại sau restart | mọi nhóm | Gián tiếp: điều kiện để công cụ dùng được nhiều lần | **CỐT LÕI (hạ tầng)** |

**UC nào nên bỏ hoặc thay `[ĐỀ XUẤT]`:**

- **Không bỏ UC nào** — cả 10 đã triển khai và đã nghiệm thu phần mềm
  (`system/app/acceptance-2026-11-17.md:11-20`); bỏ bây giờ là phí công đã làm.
- **Nhưng FR-20 (public share link) đã retired** mà code `SharedPage` và router
  `/v1/runs/{run_id}` vẫn còn (`system/app/frontend/src/App.tsx:35`;
  `system/app/backend/api/routers/runs.py:1`). `[ĐỀ XUẤT]` Không trình bày phần
  này trong báo cáo, và nói rõ trong `DEVIATIONS.md` rằng đây là endpoint legacy
  giữ cho tương thích, không phải tính năng của v0.2.

**3–5 tính năng chính đề nghị trình bày trong báo cáo `[ĐỀ XUẤT]`:**

| # | Tính năng | Vì sao chọn |
| --- | --- | --- |
| **T-1** | **Ma trận hiệu ứng 28×20 + footprint track, có cảnh báo miền đứng trước điểm số** (UC-01 + 2.11) | Đầu ra cốt lõi của đề tài; `footprint track` khớp ma trận trong 1e-9 (`plan.md:124`); quy tắc "cảnh báo trước điểm" là một quyết định thiết kế khoa học đáng trình bày (`plan.md:76`) |
| **T-2** | **Xếp hạng trong tile + shortlist + panel ưu tiên top-k có nhãn "hồi cứu, development"** (UC-02 + 2.11) | Tính năng **duy nhất** có bằng chứng định lượng về ích lợi; nhãn đứng trước số trong DOM là chi tiết trung thực đáng nêu (`system/app/DEVIATIONS.md:184`) |
| **T-3** | **Job bền cho batch/toàn protein: tiling step 23, huỷ, phục hồi sau restart** (UC-08) | Công sức kỹ thuật lớn nhất và có bằng chứng mạnh nhất: SIGKILL ở 60/382 tile, khởi động lại 1,44 s, job hoàn tất 382/382 không trùng (`system/app/acceptance-2026-11-17.md:37-38`) |
| **T-4** | **Cổng miền R3 ba trạng thái** (`measured_borderline` / `predicted_borderline`) (FR-09…11) | Đây là chỗ nghiên cứu **trực tiếp** quyết định hành vi phần mềm: `P = σ(10,187 − 3,275·x)` tier-1, `σ(8,457 − 1,911·x̂)` tier-2; đã bỏ hẳn phép so sai `psi ≤ 4,0` (`plan.md:122`; `system/app/etl/params.yaml:4`) |
| **T-5** | **Provenance và export: model card, snapshot bất biến, bundle có nhãn development** (UC-03 + UC-07 + UC-10) | Là cách phần mềm **thực thi** các giới hạn khoa học; trả lời trực tiếp câu "làm sao người dùng không đọc sai kết quả" |

`[DIỄN GIẢI]` Import/comparison (UC-05/09) nên trình bày **ngắn**, như một mục
con của T-5, chứ không thành tính năng chính: nó đã làm xong và có test, nhưng
không có bằng chứng nhu cầu, và nó là nơi dễ bị hỏi "dữ liệu import có thành
validation không" nhất — câu trả lời đã có sẵn (không, CON-3) nhưng càng nhấn
mạnh càng mời câu hỏi.

### B-4. Cần hoàn thiện thêm gì — xếp theo ưu tiên

**Phát hiện mới về trạng thái 2.12 `[ĐO]`.** `plan.md:163` ghi 2.12 là `[ ]` với
ghi chú "Cần thêm `torch`+`transformers` vào backend (hiện chỉ có numpy)".
Nhưng trong `system/app/` đã có, chưa commit (`git status` cho `??`):

- `backend/degron_footprint/lora.py` — code phục vụ LoRA-D, **viết lại từ
  recipe** thay vì import `degron_v3`, nên test parity so **hai triển khai**
  (`backend/LORA.md:19-20`)
- `etl/export_lora.py` + `backend/requirements-lora.txt` + `.venv-lora/`
- `tests/test_lora.py` — `test_lora_parity_with_the_research_implementation`
- `backend/LORA.md` — tài liệu đầy đủ

Và bằng chứng đã đo (`system/app/tests/results/lora-bundle.json`):

| Phép kiểm | Kết quả |
| --- | --- |
| Calibrator sklearn `predict_proba` ↔ softmax dùng khi phục vụ, 2.401 điểm lưới | max diff **0,0** |
| **Parity khác runtime**: triển khai nghiên cứu, 32 hàng W, CUDA (Windows) ↔ CPU (WSL), 3 seed | max diff **3,0e-6** (atol 1e-5) |
| Phục vụ ↔ triển khai nghiên cứu, 2 tile × 532 ô, từng seed / ensemble / xác suất | max diff **0,0** |
| Bundle | 139.119.046 byte, 11 file, manifest sha256 `bd8fd7e0…` |

**Và nó được cài đúng cách `[ĐO]`:** LoRA-D được đăng ký là model đóng băng
nhưng **không phải mặc định**; npz trả lời mọi request không nêu model, cho tới
khi một quyết định phục vụ riêng đặt `DF_DEFAULT_MODEL_ID`
(`backend/LORA.md:3-7`). Model card ghi
`serving_promotion: not_authorized_by_research_execution`
(`tests/results/lora-bundle.json`). `[DIỄN GIẢI]` Đây đúng là cách D-4 yêu cầu
(`d4-decision-2026-11-17.md:127-128`): không đổi model phục vụ, nhưng có sẵn
đường bật.

**Danh sách việc còn lại, xếp theo giá trị cho người dùng và cho buổi bảo vệ:**

| # | Việc | Loại | Giá trị người dùng | Giá trị bảo vệ | Chi phí | Đề nghị |
| --- | --- | --- | --- | --- | --- | --- |
| **P-1** | **Cập nhật `plan.md` 2.12 và biên bản D-4/L10 cho khớp trạng thái thật của LoRA-D** (F-1, F-3) | Tài liệu | — | **Cao** — đang có mâu thuẫn nội bộ ai cũng tra được | 1–2 h | **Làm trước mọi việc khác** |
| **P-2** | **Sinh `tests/results/latency-lora.json`** bằng `tests/measure_latency_lora.py` (F-2) | Đo, CPU | Thấp | **Cao** — số được dẫn mà file không có | ~30 phút | Làm |
| **P-3** | **Chạy lại bộ test PostgreSQL** sau migration 0004 + SEC-03 + sửa race worker | Kiểm thử | Trung bình | **Cao** — `acceptance-2026-11-17.md:16` tự ghi là số 16/11, trước 3 thay đổi của 17/11 | ~1 h (cần Docker) | Làm |
| **P-4** | **Kiểm tay a11y** (bàn phím + trình đọc màn hình) | Kiểm thử | Trung bình | Trung bình — NFR-11 nêu WCAG 2.1 AA; luồng bàn phím tự động đã có | 1–2 h | Làm, ghi là kiểm tay có giới hạn |
| **P-5** | **Quyết định có đặt LoRA-D làm mặc định hay không** | Quyết định (Trọng) | **Cao** nếu bật | **Hai chiều** — xem D-2 ở §cuối | — | **Cần Trọng chốt** |
| **P-6** | Đo lại NF-01…07 trên máy chính (hiện đo trên máy tác giả) | Đo | Thấp | Thấp — `acceptance-2026-11-17.md:60` đã ghi giới hạn | 1 h | Tuỳ thời gian |
| **P-7** | Gỡ hoặc ghi rõ `SharedPage`/`/v1/runs` legacy | Dọn dẹp | Thấp | Trung bình — tránh bị hỏi "FR-20 retired mà sao còn code" | 30 phút (chỉ ghi tài liệu) | Ghi tài liệu, **không gỡ code** |

**Khoảng trống chức năng phát hiện được `[DIỄN GIẢI]`:**

1. **Không có cách nào trong app để thấy kết quả âm `gt5`.** App cho điểm và xác
   suất cho mọi tile in-domain, nhưng người dùng không được cảnh báo rằng ở
   PSI(WT) > 5 thì baseline đoán 0 tốt hơn model. Cổng R3 lọc theo *độ giống
   miền huấn luyện*, không theo *strata PSI nơi model kém*.
   `[ĐỀ XUẤT]` Đây là khoảng trống đáng nêu trong báo cáo như **việc tương lai**,
   không nhất thiết phải làm: thêm một cảnh báo theo strata PSI(WT). Nếu không
   làm, phải nói rõ trong phần giới hạn.
2. **Không có gì trong app đo được ích lợi ưu tiên.** Bằng chứng Precision@10
   nằm ở nghiên cứu (`oof-prioritization`), còn panel top-k trong app chỉ xếp
   hạng. `[DIỄN GIẢI]` Không cần sửa — chỉ cần panel dẫn đúng nguồn bằng chứng,
   việc mà nhãn "hồi cứu, development" đã làm.

---

## Quyết định cần Trọng chốt

| # | Quyết định | Vì sao cần Trọng | Khuyến nghị của Claude |
| --- | --- | --- | --- |
| **D-A** | **Duyệt phân loại 36 thư mục `research/` ở §A-6** (8 CHÍNH / 13 PHỤ LỤC / 15 LỊCH SỬ) | Quyết định nội dung nào vào mạch chính Chương 4 và nội dung nào xuống phụ lục — ảnh hưởng toàn bộ Phần C1 | Duyệt như đề xuất; nếu muốn giữ `pretrain-p3` hoặc `r2-esm-features` ở mạch chính thì nói rõ để em giữ |
| **D-B** | **Duyệt 5 tính năng chính T-1…T-5 ở §B-3** để trình bày ở Chương 3/4 | Quyết định phạm vi C3; mỗi tính năng cần sơ đồ + luồng + test dẫn chứng | Duyệt; đưa UC-05/09 thành mục con của T-5 |
| **D-C** | **Có cập nhật `plan.md` 2.12 và biên bản D-4 cho khớp trạng thái LoRA-D thật không** (F-1, F-3, P-1) | Sửa biên bản quyết định đã ký cần Trọng đồng ý; em không tự sửa `d4-decision` | **Nên làm**: không sửa nội dung quyết định D-4, chỉ thêm một mục "Cập nhật trạng thái 17/11" ghi rằng parity khác runtime **đã có** ở `system/app/tests/results/lora-bundle.json`, và sửa `plan.md:163` thành `[~]` kèm phạm vi |
| **D-D** | **LoRA-D có được đặt làm model mặc định của app không** (P-5) | Đây là **quyết định phục vụ**, D-4 đã tách riêng khỏi quyết định nghiên cứu (`d4-decision-2026-11-17.md:127-128`) | **Khuyến nghị KHÔNG đổi mặc định.** Lý do: (a) latency/RAM chưa có file đo (F-2); (b) kết quả âm `gt5` chưa có cảnh báo trong UI; (c) giữ npz mặc định + LoRA-D bật được bằng cấu hình đúng như rủi ro đã dự phòng ở `plan.md:252`. Trình bày LoRA-D như **ứng viên đã export và kiểm parity**, mạnh hơn là đổi mặc định mà chưa đủ đo |
| **D-E** | **Tên đề tài (D-1 cũ): bản NGẮN hay DÀI** | Chưa chốt từ 16/11 (`plan.md:17`); chặn mục 3.7 | **Bản DÀI**, vì phạm vi phần mềm đã thành ứng dụng web đầy đủ 19 bảng/37 operation/13 màn hình — đúng như `plan.md:43` đã khuyến nghị |
| **D-F** | **Ngày bảo vệ + 3 thành viên hội đồng cho `report/config/metadata.tex`** (D-2 cũ) | Chỉ Trọng có thông tin; chặn mục 3.7 và toàn bộ lịch | Cần gấp để biết lịch 9 tuần ở `plan.md:239` có vừa không |
| **D-G** | **Có xin GVHD ghi nhận biên bản D-4 trước khi nộp không** (G-1) | `d4-decision-2026-11-17.md:5,143` ghi "chưa ghi nhận; đề nghị xác nhận trước khi nộp" | **Nên xin** — đây là việc chặn duy nhất còn lại của nhánh 1 |
| **D-H** | **Có thêm cảnh báo theo strata PSI(WT) vào app không** (khoảng trống §B-4.1) | Thêm tính năng ngoài phạm vi v0.2 đã nghiệm thu | **Khuyến nghị KHÔNG làm** trong lượt này; ghi vào phần "việc tương lai" của luận văn. App đã nghiệm thu 17/11, thêm tính năng sẽ phải nghiệm thu lại |

---

## Trạng thái và bước tiếp theo

**Đã làm trong lượt này:** Phần A (đánh giá nghiên cứu, phân loại 36 thư mục,
kiểm kê khoảng trống) và Phần B (người dùng, tính thực tế, 10 UC, việc còn lại).
Chỉ đọc; không sửa `report/`, `system/`, `plan.md`, `research/*/output/`.

**Đang chờ:** Trọng duyệt D-A và D-B (bắt buộc để sang Phần C), và trả lời
D-C…D-H.

**Phần C sẽ làm sau khi duyệt:** C1 (nội dung + trích dẫn + trình tự thời gian +
xoá 5 `[PENDING]`), C3 (sơ đồ dựng từ code thật: use case, kiến trúc, CDM→LDM→PDM
từ migration `0001`–`0004` và ORM 19 bảng, sequence/state cho job và
import/comparison), C2 (bố cục, 12 hình / 58 bảng), C4 (`make -C report all`,
`make -C report check`, `check_float_references.py`, biên bản
`report/review-validation-2026-11-17.{md,json}` mới).

---

## Phụ lục cập nhật 18:06 — trả lời "đã có model mới sau refit chưa"

Phần thân trên viết theo trạng thái lúc ~17:30. Phía ứng dụng đã thay đổi trong
lúc em viết; mục này đọc lại lúc 18:06 và **thay thế F-2**.

### Có — refit đã sinh ra model mới, đầy đủ `[ĐO]`

6 model cuối trong campaign `aa4fc2b7ce29abf9`
(`research/kaggle-roadmap-2026-10-31/output/local/aa4fc2b7ce29abf9/jobs/`):

| Nhóm | Seed | Epoch | File | Kích thước |
| --- | --- | --- | --- | ---: |
| `esm2_35m-lora-D` | 17 / 29 / 43 | 2 / 2 / 2 | `refit-lora-D-{17,29,43}/model.pt` | 1.016.583 B mỗi file |
| `esm2_35m-frozen-D` | 17 / 29 / 43 | 1 / 2 / 2 | `refit-frozen-D-{17,29,43}/model.pt` | 1.016.583 B mỗi file |

`[ĐO]` SHA-256 của 3 checkpoint LoRA-D **khớp đúng** `model-card.json`:
`3a0027ec…` (17), `40360237…` (29), `86ed1a33…` (43). `model_ids` nay đã đủ 3
mục, không còn rỗng như mốc 06/11.

Kèm theo: 2 calibrator cuối
(`calibrate-final-{lora,frozen}-D/final-calibrator.joblib`,
`fit_population: ensemble_OOF_W`, `T_fit_cells: 0`), quy tắc ensemble là **trung
bình 3 raw prediction rồi mới hiệu chuẩn một lần**
(`model-card.json` → `ensemble`), base `facebook/esm2_t12_35M_UR50D` @
`6fbf070e…` FP32, adapter r=8 / alpha=16 trên `query`+`value`.

### Và đã được đóng gói để phục vụ `[ĐO]`

`data/processed/lora-d-serving-v1/` — **133 MB, 12 file**: 3 `adapter-seed*.npz`
(1.026.320 B mỗi file), `calibrator.npz`, `base/`, `parity-fixture.npz`,
`training-sequences.txt`. Manifest `esm2-35m-lora-d-v1.json` sha256
`d6729faf…` (7.241 B), được ghim ở `system/app/etl/sources.yaml:101` — khớp.
Bundle đã được **xuất lại** trong phiên này (hash trước đó em đọc được là
`bd8fd7e0…`/6.922 B); bản trên đĩa và bản ghim hiện nhất quán với nhau.

Model được đăng ký trong app là `esm2-35m-lora-d-aa4fc2b7`
(`system/app/etl/params.yaml:17-20`).

### Nhưng nó KHÔNG phải model đang phục vụ `[ĐO]`

- `default_model_id` vẫn là `m3-ext4.0-platt-v1`
  (`tests/results/latency-lora.json` → `health`).
- `serving_promotion: not_authorized_by_research_execution`;
  `G2_G3: not_closed` (`model-card.json:81-82`).
- `scientific_status: development_not_gate_closure` (`:4`).

### F-2 đã được giải quyết, và có một số liệu quyết định (F-11) `[ĐO]`

`tests/results/latency-lora.json` nay **đã tồn tại** (tạo 18:01; mốc đo trong
file là `2026-11-17T09:53:29+00:00`). Đo trên WSL2 / Ryzen 5 5500U / 12 luồng /
7.619 MB RAM, `DF_LORA_THREADS=4`, protein A6NMZ7, 10 tile tuần tự, cache ấm,
qua nginx + API:

| Model | p50 | **p95** | Request đầu |
| --- | ---: | ---: | ---: |
| `m3-ext4.0-platt-v1` (ridge+Platt) | 18,2 ms | **20,2 ms** | 30,7 ms |
| `esm2-35m-lora-d-aa4fc2b7` (torch LoRA) | 37.674,8 ms | **39.148,9 ms** | 41.697,7 ms |

`[ĐO]` Chậm hơn khoảng **1.938×**, và **trượt** ngưỡng đề xuất NFR-01
(p95 ≤ 300 ms) khoảng 130 lần. Chính file kết quả ghi
`threshold_proposed.NFR-01...: {m3: true, lora: false}`. Lý do ghi trong
`caveats`: LoRA-D chạy **3 seed × (1 + 532) lượt forward ESM-2 35M trên CPU cho
mỗi tile**. RAM container API 514,5 MiB / 7,44 GiB; image backend 1.767.655.826 B
(~1,77 GB).

`[ĐO]` Mặt khác parity rất tốt: API trong container `WITH_LORA=1` qua nginx so
với fixture của triển khai nghiên cứu cho **max diff 0,0** cả score và xác suất,
trên 2 tile × 532 ô (F-12).

### Hệ quả cho các quyết định

- **D-D (có đặt LoRA-D làm mặc định không) — nay đã có câu trả lời bằng số:
  KHÔNG.** p95 ~39 s/tile khiến UC-08 (toàn protein, 382 tile) không dùng được
  trên CPU, và NF-06 (click → heatmap p95 ≤ 1,5 s) chắc chắn trượt. Giữ npz làm
  mặc định đúng như dự phòng ở `plan.md:252`.
- **F-2 và P-2 đóng.** `plan.md` 2.12 nên ghi `[~]` với phạm vi: *đã export,
  đăng ký, kiểm parity cùng/khác runtime và đo latency; **không** đặt mặc định vì
  p95 trượt NFR-01* — thay vì `[ ]`.
- **G-3 đóng**; G-2 (đồng bộ tài liệu parity) vẫn còn.
- `[DIỄN GIẢI]` Trình bày trong luận văn mạnh hơn khi nói thẳng: model nghiên
  cứu tốt hơn về sai số nhưng **chưa dùng được để phục vụ trên CPU**, và đã đo
  được vì sao. Đây là một kết quả engineering thật, không phải thiếu sót.
