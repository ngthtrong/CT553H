# Protocol phép kiểm similarity cho mục 1.15 — 17/11/2026

Khoá **trước khi tính** bất kỳ số nào của phép kiểm này. Mục đích: bổ sung phép
kiểm riêng cho giả thuyết `similarity_construct`, hiện đang là giả thuyết duy
nhất trong [error-results.json](error-results.json) không có phép kiểm
(`not_resolved_by_this_run; no new homology alignment performed`).

Đây là **phân tích chẩn đoán hậu kiểm trên T đã từng được khảo sát**. Không phải
validation độc lập, không phải kiểm định tiền đăng ký của endpoint chính, không
đóng G2/G3, không đổi mô hình phục vụ, không sửa campaign.

## 1. Giả thuyết

**H-S:** Lợi thế của LoRA-D trên T đến từ **đồng dạng trình tự** giữa peptide T
và peptide huấn luyện W, chứ không từ khả năng khái quát của recipe.

Nếu H-S đúng, lợi thế phải tập trung ở các peptide T giống W nhiều, và biến mất
ở các peptide T ít giống W nhất.

## 2. Đầu vào cố định, chỉ đọc

| Nguồn | Vai trò |
| --- | --- |
| `output/local/aa4fc2b7ce29abf9/jobs/aggregate-refit/<recipe>-per-peptide.csv` | MAE từng peptide trên T, đã tính xong ở job aggregate; **không tính lại dự đoán** |
| `research/reliability-transfer-2026-11-08/similarity.csv`, dòng `cohort == 'T'` | `max_aligned_identity` của mỗi peptide T so với **235 peptide huấn luyện W**, tính ngày 08/11 bởi `analyze.py:475` |
| `research/reliability-transfer-2026-11-08/config.json` | `identity_bins`, `bootstrap_replicates`, `bootstrap_seed` |

Không tải model, không chạy suy luận, không import torch, không GPU.

## 3. Tham số đã khoá từ trước

Lấy nguyên từ `config.json` ngày 08/11, **không chọn lại theo kết quả**:

- `identity_bins = [0.0, 0.25, 0.5, 0.75, 1.00000001]`, biên trái đóng.
- `bootstrap_replicates = 5000`, `bootstrap_seed = 1729`.
- Cụm bootstrap: `group_id` (nhóm protein), đúng như endpoint chính.

Ước lượng paired delta và CI dùng **cùng công thức** với `degron_v3/metrics.py`
`paired_ci`: ghép theo `peptide_id`, lấy hiệu MAE, bootstrap theo nhóm bằng
tổng/đếm, phân vị `[0,025; 0,975]` cho `ci95`.

## 4. Phép kiểm

**Chính:** với mỗi contrast trong {LoRA-D − frozen-D, LoRA-D − W5-D}, và mỗi bin
similarity, tính mean paired ΔMAE kèm CI theo nhóm. `ci_adjusted` dùng Bonferroni
với bội số bằng số ô (contrast × bin) có dữ liệu.

**Phụ, mô tả:** Spearman giữa `max_aligned_identity` và paired ΔMAE trên toàn bộ
1.410 peptide T, cho mỗi contrast.

**Kiểm tự chứng:** tính lại delta toàn cohort bằng chính code này và so với
`results.json` → `contrasts`. Sai lệch phải ≤ 1e-9, nếu không thì dừng.

**Bổ sung cho L3:** paired ΔMAE kèm CI theo nhóm cho contrast
{LoRA-D − zero} trong **từng strata PSI(WT)**, để khẳng định L3 (zero tốt hơn
LoRA-D ở strata gt5) có khoảng bất định, thay vì chỉ một con số điểm.

## 5. Quy tắc đọc kết quả, khoá trước

Gọi bin thấp nhất **có dữ liệu** là bin đáy.

- **H-S không giải thích được lợi thế** nếu CI của bin đáy nằm **hoàn toàn dưới 0**.
  Khi đó lợi thế vẫn còn ở nhóm peptide ít giống W nhất.
- **H-S được ủng hộ** nếu CI của bin đáy **phủ 0** trong khi có bin cao hơn với CI
  hoàn toàn dưới 0. Khi đó lợi thế phụ thuộc mức đồng dạng.
- **Chưa phân giải** trong mọi trường hợp còn lại, gồm: chỉ một bin có dữ liệu,
  bin đáy có quá ít nhóm, hoặc mọi CI đều phủ 0.

Kết luận "chưa phân giải" là kết quả hợp lệ theo tiêu chí nghiệm thu mục 1.15.
Không đổi bin, đổi contrast hay đổi quy tắc sau khi xem số.

## 6. Giới hạn đã biết trước

- `max_aligned_identity` là **proxy cục bộ** theo protocol 08/11 §4.2: căn theo
  vị trí trên chuỗi 28 aa, không thay MMseqs2 hay audit remote homology, và
  **không** bao gồm phơi nhiễm trong pretraining của ESM2.
- Phân bố similarity có thể lệch mạnh; nếu phần lớn peptide T rơi vào một bin thì
  phép kiểm mất độ phân giải và phải kết luận "chưa phân giải".
- Đây là liên hệ thống kê, **không phải cơ chế**. Không kết luận nhân quả.
- T đã từng được khảo sát; phép kiểm này không nâng T thành nguồn độc lập.
