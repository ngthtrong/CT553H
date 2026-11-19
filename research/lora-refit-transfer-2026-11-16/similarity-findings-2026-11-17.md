# Phép kiểm similarity và bất định theo strata — mục 1.15

**Ngày:** 17/11/2026. Protocol khoá trước khi tính:
[SIMILARITY-PROTOCOL.md](SIMILARITY-PROTOCOL.md),
sha256 `d74dc18d24bc25804f8bcf226647897ab40f3a13f896818818b201964ea7393e`.
Số liệu: [similarity-results.json](similarity-results.json),
[similarity-contrasts.csv](similarity-contrasts.csv), sinh bởi
[analyze-similarity.py](analyze-similarity.py).

Chẩn đoán hậu kiểm trên T đã từng được khảo sát. Chạy CPU trên WSL, chỉ đọc
kết quả per-peptide đã có; không nạp model, không suy luận, không sửa campaign.
Giữ `development_not_gate_closure`. Không đóng G2/G3, không đổi mô hình phục vụ.

## 1. Kiểm tự chứng

Tái tạo contrast toàn cohort bằng chính code này rồi so với
[results.json](results.json) → `contrasts`:

| Contrast | Delta tái tạo | Delta đã công bố | Sai lệch |
| --- | ---: | ---: | ---: |
| LoRA-D − frozen-D | −0,04054776776860308 | −0,04054776776860308 | 0,0 |
| LoRA-D − W5-D | −0,05217578925156808 | −0,05217578925156808 | 0,0 |

Sai lệch CI tối đa 1,4e-17. Công thức bootstrap theo nhóm trùng đúng
`degron_v3/metrics.py:paired_ci`.

## 2. Giả thuyết similarity `[ĐO]`

**H-S:** lợi thế của LoRA-D trên T đến từ đồng dạng trình tự với peptide
huấn luyện W. `max_aligned_identity` của mỗi peptide T tính so với **235 peptide
W**, lấy từ `similarity.csv` ngày 08/11. Bin đã khoá trong `config.json` 08/11.

Bootstrap theo nhóm protein, 5.000 lần, seed 1729. `ci_adjusted` Bonferroni
bội số 4 (2 contrast × 2 bin có dữ liệu).

| Contrast | Bin identity | Peptide | Nhóm | ΔMAE | CI95 | CI hiệu chỉnh |
| --- | --- | ---: | ---: | ---: | --- | --- |
| LoRA-D − frozen-D | [0; 0,25) | 1.093 | 627 | −0,0399 | [−0,0445; −0,0353] | [−0,0457; −0,0342] |
| LoRA-D − frozen-D | [0,25; 0,5) | 317 | 239 | −0,0427 | [−0,0534; −0,0324] | [−0,0564; −0,0293] |
| LoRA-D − W5-D | [0; 0,25) | 1.093 | 627 | −0,0542 | [−0,0595; −0,0488] | [−0,0609; −0,0472] |
| LoRA-D − W5-D | [0,25; 0,5) | 317 | 239 | −0,0452 | [−0,0561; −0,0349] | [−0,0588; −0,0318] |

Spearman giữa `max_aligned_identity` và ΔMAE từng peptide, mô tả:

| Contrast | rho | p |
| --- | ---: | ---: |
| LoRA-D − frozen-D | +0,0164 | 0,54 |
| LoRA-D − W5-D | +0,0502 | 0,059 |

**Kết luận theo quy tắc khoá trước (protocol §5): `H-S_does_not_explain_advantage`.**
Ở bin đáy [0; 0,25), tức nhóm 1.093 peptide T ít giống W nhất, lợi thế của
LoRA-D vẫn còn và CI nằm hoàn toàn dưới 0 ở cả hai contrast, kể cả sau hiệu
chỉnh. Tương quan giữa mức đồng dạng và lợi thế gần 0 và đổi dấu nhẹ theo
chiều **ngược** với H-S. Vậy đồng dạng trình tự cục bộ với W không giải thích
được lợi thế quan sát được.

`[DIỄN GIẢI]` Đây là bằng chứng chống lại H-S trong phạm vi proxy đã dùng. Nó
**không** chứng minh không có rò rỉ: xem giới hạn ở §4.

## 3. Bất định của kết quả bất lợi ở PSI(WT) cao `[ĐO]`

Contrast LoRA-D − zero theo từng strata, cùng bootstrap theo nhóm. Số âm nghĩa
là LoRA-D tốt hơn zero; số dương nghĩa là **tệ hơn**.

| Strata | Peptide | Nhóm | ΔMAE | CI95 | CI hiệu chỉnh |
| --- | ---: | ---: | ---: | --- | --- |
| le3 | 524 | 343 | −0,1016 | [−0,1108; −0,0921] | — |
| gt3_le4 | 323 | 253 | −0,0653 | [−0,0759; −0,0545] | — |
| gt4_le5 | 306 | 238 | −0,0253 | [−0,0326; −0,0180] | — |
| **gt5** | 257 | 204 | **+0,0152** | **[+0,0070; +0,0238]** | **[+0,0051; +0,0260]** |

**Kết quả âm được xác nhận, không phải nhiễu.** Ở strata PSI(WT) > 5, baseline
zero tốt hơn LoRA-D, và CI nằm hoàn toàn **trên** 0 kể cả sau hiệu chỉnh
Bonferroni. Lợi thế của LoRA-D giảm đơn điệu khi PSI(WT) tăng, rồi đổi dấu.

`[DIỄN GIẢI]` Phù hợp với bảng bias trong [error-results.json](error-results.json):
ở gt5, target mean là −0,176 trong khi prediction mean là +0,181, tức mô hình
vẫn dự đoán theo chiều dương trong vùng mà hiệu ứng đo được là âm. Đây là mô tả
liên hệ, chưa phải cơ chế.

## 4. Giới hạn

- **Dải similarity rất hẹp.** Toàn bộ 1.410 peptide T có
  `max_aligned_identity` trong khoảng 0,143–0,357, nên hai bin trên cùng
  ([0,5; 0,75) và [0,75; 1]) **không có dữ liệu**. Phép kiểm chỉ phân biệt được
  "ít giống" với "hơi giống hơn", **không** kiểm được vùng đồng dạng cao.
  Đây là giới hạn độ phân giải, phải nêu kèm kết luận §2.
- `max_aligned_identity` là **proxy cục bộ** căn theo vị trí trên chuỗi 28 aa.
  Không thay MMseqs2 hay audit remote homology, và **không** bao gồm phơi nhiễm
  trình tự trong pretraining của ESM2. Rò rỉ qua pretraining vẫn chưa được loại.
- Liên hệ thống kê, không phải cơ chế. Không kết luận nhân quả.
- T đã từng được khảo sát; phép kiểm này không nâng T thành nguồn độc lập.
- Chẩn đoán thứ cấp sau khi đã xem kết quả chính; bin và quy tắc đọc được khoá
  trước khi tính, nhưng thiết kế tổng thể là hậu kiểm.

## 5. Trạng thái bốn giả thuyết của mục 1.15

| Giả thuyết | Phép kiểm | Kết quả |
| --- | --- | --- |
| `target_distribution` | Bảng bias và prevalence theo strata | `error-results.json`; có |
| `score_shift` | Quantile OOF W / final W in-sample / T | `results.json` → `score_shift`; có, không hiệu chỉnh bằng T |
| `replicate_noise` | Giao hai replicate | `results.json` → `replicate_intersection`; có |
| `similarity_construct` | **Bin similarity + CI theo nhóm (tài liệu này)** | **Đã kiểm; H-S không giải thích được lợi thế, trong giới hạn §4** |

Cơ chế đầy đủ của sai số ở PSI(WT) cao **vẫn chưa phân giải**. Tài liệu này xác
nhận kết quả bất lợi có ý nghĩa thống kê và loại một giả thuyết, không thay thế
một thiết kế đối chứng cho câu hỏi cơ chế.

## 6. Dựng lại

```bash
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  research/lora-refit-transfer-2026-11-16/analyze-similarity.py
```

Cần numpy/pandas/scipy theo `research/reliability-transfer-2026-11-08/requirements-analysis.txt`.
Script tự kiểm hash protocol và tự so contrast với `results.json`; lệch là dừng.
