# Protocol thực thi đã khóa — OOF mutation prioritization

Ngày 07/11/2026, người dùng yêu cầu thực hiện các phép so cùng ngân sách và `tmp.md`.
Cấu hình chuẩn là [config.json](config.json), khóa trước khi tính utility.
Đây là phân tích hồi cứu trên development, không phải tiền đăng ký độc lập.
Các mục ghi “đề xuất/chưa thực thi” trong bản nguồn bên dưới mô tả thời điểm lập kế hoạch;
yêu cầu thực thi hiện tại cho phép triển khai toàn bộ các bước đó.

Chi tiết triển khai khóa thêm: curve k=1,2,5,10,20,30,50,75,100,150,200,300,400,532;
100 tie seed là 0..99. Phân tầng số hit 0,1–2,>=3 là mô tả độ thưa endpoint,
không phải đánh giá độ khó sinh học hay điều kiện lọc Precision chính.
Toàn bộ seed, policy, hướng và ngân sách được báo, không chọn lại sau kết quả.

SHA-256 bản nguồn `tmp.md`: `8f0df3414ecdfc2774d05464d4b2678249b22e55d68e56ccd90d6a8eb1a58630`.

---

# Kế hoạch đánh giá hồi cứu khả năng ưu tiên mutation bằng OOF

Ngày lập: **07/11/2026**. Trạng thái: **KẾ HOẠCH, CHƯA THỰC THI ĐÁNH GIÁ**.
Các lựa chọn dưới đây là thiết kế đề xuất để khóa trước khi tính metric utility;
không phải quyết định nghiệm thu, kết quả mới hoặc tiền đăng ký độc lập với dữ
liệu development đã được khảo sát.

## 1. Mục tiêu và phạm vi

**Câu hỏi:** Với cùng tập mutation và cùng số lựa chọn cho mỗi peptide, điểm
OOF của LoRA có tìm được nhiều mutation đạt tiêu chí thực nghiệm hơn chọn ngẫu
nhiên và Ridge W5 không?

**Giả thuyết cần kiểm:** LoRA-D cải thiện precision khi chọn 10 mutation/peptide
so với cả hai đối chứng. MAE/AUROC tốt hơn trước đây không tự xác nhận giả thuyết
này; kết quả utility có thể dương, âm hoặc chưa phân giải.

- Đánh giá trên **W full-PSI v3**, cùng cohort/split đã dùng: hồ sơ hiện có ghi
  235 peptide, 221 nhóm protein và 122.412 ô mutation. Phải kiểm lại các số này
  từ input trước khi chạy; không coi chúng là kết quả đã kiểm trong kế hoạch.
- **Đơn vị lựa chọn:** một phép thay amino acid đơn tại một vị trí trên một
  peptide. Một ô dữ liệu không phải một biological replicate độc lập.
- **Quyết định được mô phỏng:** ưu tiên mutation bên trong từng peptide đã có
  danh sách ứng viên; không xếp hạng toàn bộ protein hoặc ngân sách toàn proteome.
- Chỉ sử dụng dự đoán/nhãn đã lưu. Không train lại, refit, chạy inference model,
  sửa checkpoint, mở T hoặc thêm nguồn ngoài trong phép đánh giá này.
- Đây là phân tích hồi cứu trên development; OOF không xóa lịch sử chọn model
  và khảo sát dữ liệu. Không đổi kết quả thành prospective wet-lab validation.

## 2. Cơ sở hiện có và phần sẽ bổ sung

[Metric v3](../../research/kaggle-roadmap-2026-10-31/degron_v3/metrics.py) đã tính
precision/enrichment theo peptide ở top 5%, 10%, 20%. Phân tích local tổng hợp
hiện chủ yếu báo MAE, RMSE, Spearman, AUROC/AP; không mặc định các trường utility
đang thiếu là 0.

Phần bổ sung: ngân sách cố định 10 mutation/peptide, random expectation minh
bạch, đối chứng W5 trên cùng candidate pool, recall/budget-to-recall, paired
cluster CI, cách xử lý tie và phân biệt số assay giả lập với tiền/giờ thực tế.
Giữ các tỷ lệ top 5/10/20% để đối chiếu cách tính đã có, không công bố lại chúng
như một benchmark độc lập mới.

## 3. Dữ liệu đầu vào và kiểm tính toàn vẹn

Quy ước đường dẫn để đọc bảng dưới:

```text
ROAD = research/kaggle-roadmap-2026-10-31
LOCAL = ROAD/output/local/ef138c84579c842e
KAGGLE = ROAD/output/official/369cb2fe6a1e31e0
DATA = data/processed/v3-fullpsi
```

| Input | Đường dẫn tính từ quy ước trên | Vai trò |
| --- | --- | --- |
| OOF LoRA-D | `LOCAL/jobs/collect-core/esm2_35m-lora-D-oof.parquet` | Mô hình chính |
| OOF W5-D | `KAGGLE/tasks/01-78cc356ba4f4/ordered-w5-D-oof.parquet` | Baseline chính |
| OOF frozen-D | `LOCAL/jobs/collect-core/esm2_35m-frozen-D-oof.parquet` | Đối chứng phụ cùng runtime/head |
| OOF LoRA-B | `LOCAL/jobs/collect-core/esm2_35m-lora-B-oof.parquet` | Phân tích độ nhạy, không chọn lại model chính |
| Manifest/bảng gốc | `DATA/DATA_MANIFEST.json`, `tables/saturation-cells.parquet`, `splits/wide-outer.parquet`, `splits/inner-seed{17,29,43}.parquet` | Nhãn, metadata, split và identity |
| Provenance | Plan/state/collection local; pipeline manifest và `output-analysis.json` của Kaggle; `local-output-analysis.json` | Kiểm recipe, seed, nguồn artifact và hash |

**Đã kiểm khi lập kế hoạch:** bốn file OOF local trong bảng, file OOF W5-D và
DATA_MANIFEST hiện tồn tại, có dung lượng khác 0. Chưa đọc lại toàn bộ Parquet,
chưa rehash, chưa chấm utility. Identity được hồ sơ hiện có ghi là
`b0376e05d690d991c95143d6122b5418e457318394da032928d0d1e53f914738`.

Trước thực thi phải qua các cổng dữ liệu:

1. Pin Git commit/working diff, protocol/config, phiên bản thư viện và SHA-256
   của mọi input dùng thực sự. Kiểm với manifest gốc; giữ bản nguồn và successor.
   Map đường dẫn Windows sang bản local theo lineage đã biết, không sửa manifest
   hoặc thay hash để ép khớp.
2. Chỉ nhận bản full-data, không phải smoke/fixture. Kiểm `mode`, data identity,
   recipe, seed 17/29/43 và outer fold 0–4 theo schema của từng nguồn.
3. Mỗi `(seed, cell_id)` duy nhất; prediction/nhãn hữu hạn; cùng một `cell_id`
   phải khớp peptide, vị trí, WT/mutant, group, fold và nhãn ở mọi phương pháp.
   Không join theo thứ tự dòng. Kiểm đủ ba prediction/ô rồi mới ensemble.
4. Kiểm tập `cell_id` chính xác bằng W cho mỗi seed. Nếu thiếu baseline hoặc
   lệch cohort: dừng và báo chênh, không âm thầm lấy intersection để có kết quả.
5. Dùng split và role đã lưu xác nhận cụm outer-test không được fit/select epoch/
   calibrator của model tương ứng. OOF label không dùng cho lựa chọn tiếp theo.
   Kiểm trên split lưu sẵn không chứng minh loại hết mọi remote homology.

Có thể tham khảo [audit chỉ đọc](../../research/progress-review-2026-11-06/local-audit.py)
và [analyzer local](../../research/kaggle-roadmap-2026-10-31/analyze-local-output.py),
nhưng không chạy nguyên script có tác dụng ghi đè hồ sơ phân tích cũ.

## 4. Candidate pool và tiêu chí hit

- Giữ tất cả mutation không đồng nghĩa đã qua QC trong W; không dựng thêm
  các ô chưa có phép đo, không lọc theo dấu nhãn hoặc điểm dự đoán.
- **Endpoint chính:** `hit_plus = (dpsi_mean >= 1)`. Đây là tăng tín hiệu PSI
  trong peptide-reporter, không tự xác nhận half-life hoặc E3 cụ thể.
- **Endpoint phụ:** `hit_minus = (dpsi_mean <= -1)`; xếp theo chiều giảm ΔPSI.
  Đánh giá riêng hai chiều; không cộng dương/âm để che chiều dự đoán yếu.
- `dpsi_mean` và QC giữ nguyên bundle. PSI(WT), group/fold và stratum chỉ dùng
  kiểm/phân tầng, không được dùng thêm vào chính sách chọn mutation.
- Precision và số hit chính tính trên **mọi peptide đủ candidate**, kể cả peptide
  không có hit. Không áp điều kiện AUROC “ít nhất 3 event và 3 non-event”.
- Recall, enrichment và budget-to-recall chỉ có định nghĩa khi có ít nhất một
  hit của chiều đó. Khi không có hit: ghi `null` kèm lý do, giữ chúng trong
  bảng precision; luôn công bố denominator của từng metric.

## 5. Chính sách chọn và ngân sách được đề xuất

| Chính sách | Điểm và cách chọn | Vai trò |
| --- | --- | --- |
| LoRA-D | Trung bình prediction OOF ba seed, xếp giảm dần cho hit_plus | Chính |
| Ridge W5-D | Cùng cách ensemble/xếp hạng; dùng OOF đã có | Baseline chính, tuyến tính dùng pair/composition/ngữ cảnh ±5 |
| Random | Chọn đều, không hoàn lại trong candidate pool của peptide | Đối chứng không dùng prediction |
| Frozen-D | Điểm OOF ba seed, cùng runtime/head với LoRA-D | Phụ, làm rõ lợi ích adaptation |
| LoRA-B | Cùng policy trên W; không dùng kết quả replay để thay D trong phân tích chính | Độ nhạy theo training arm |

Chọn D làm recipe chính vì mục tiêu là W toàn dải, giữ thống nhất training arm
với W5-D. Đây là lựa chọn thiết kế đề xuất, không kết luận D vượt B. Không duyệt
88 recipe rồi lấy recipe có utility cao nhất. Phép so local LoRA–Kaggle W5 là
so hai workflow đã lưu; khác runtime/head nên không cô lập riêng tác động LoRA.

**Ngân sách chính:** `k_p = min(10, N_p)` mutation/peptide, với `N_p` là số ô
của peptide p. Nếu có peptide dưới 10 candidate phải báo ngân sách thực; không
gọi mọi hàng là Precision@10 nếu mẫu đó chỉ chọn được ít hơn.

**Ngân sách phụ:** fixed k = 5, 20 và các tỷ lệ 5%, 10%, 20%, dùng
`k_p = max(1, ceil(q * N_p))` cho tỷ lệ q. Không chọn ngân sách bằng đường cong
cho kết quả thuận lợi. Tổng ngân sách là tổng `k_p` trên cohort, không mặc định
mọi mutation là một thí nghiệm có cùng giá tiền.

**Tie:** so score bằng nhau chính xác, không dùng nhãn phá tie. Khóa trước
thứ tự bằng hash của `(tie_seed, peptide_id, cell_id)`, cùng tie key cho mọi
phương pháp; không dựa thứ tự Parquet hoặc tên amino acid. Chọn `tie_seed=1729`.
Báo tỷ lệ tie cắt ngang ngưỡng top-k và kiểm độ nhạy với 100 tie seed cố định;
không chọn tie seed tốt nhất. Score cho hit_minus là `-prediction`.

Chỉ rank bên trong peptide. Không gộp prediction từ các outer model vào một
global ranking chưa kiểm scale/calibration. Phân tích chính không dùng xác suất
đã hiệu chuẩn hoặc fit calibrator mới; utility của xác suất là câu hỏi riêng.

## 6. Metric và random reference

Gọi `H_p` là tổng hit đã đo, `h_p(k)` là hit trong top-k của peptide p:

| Metric | Định nghĩa và cách báo |
| --- | --- |
| Precision@k | `h_p(k) / k_p`; lấy trung bình theo peptide trên cohort chính |
| Hits@k | `h_p(k)`; báo trung bình theo peptide và tổng số hit dưới cùng tổng ngân sách |
| Recall@k | `h_p(k) / H_p` trên peptide có hit; báo riêng số peptide/nhóm đủ điều kiện |
| Enrichment@k | Precision của peptide chia `H_p/N_p`; macro trên peptide có hit. Không thay bằng tỷ số hai macro khác nhau. |
| Budget-to-recall | Số lựa chọn ít nhất trong ranking để thu được `ceil(r * H_p)` hit, với r = 0,5 và 0,8; báo cả số và tỷ lệ trên `N_p` |

**Primary endpoint:** peptide-macro Precision với ngân sách 10 mutation cho
hit_plus. Recall, enrichment, ngân sách khác, event âm và các phân tầng là phụ.

Random có kỳ vọng tính trực tiếp, không cần gọi một lần random là chuẩn:

- Expected Hits@k = `k_p * H_p / N_p`; expected Precision@k = `H_p / N_p`.
- Khi `H_p > 0`, expected Recall@k = `k_p / N_p`.
- Với permutation random đều và đích `j = ceil(r * H_p)`, kỳ vọng số lựa chọn
  để gặp hit thứ j là `j * (N_p + 1) / (H_p + 1)`.

Ở bước triển khai, kiểm các công thức bằng trường hợp nhỏ liệt kê được; thêm
2.000 lượt random để minh họa phân phối có điều kiện và kiểm số học. Dùng seed
gốc `20261107`, dẫn xuất stream theo peptide bằng hash ổn định, không dùng
`hash()` của Python. Có thể lấy mẫu hypergeometric cho Hits@k để giảm tính toán;
không cần tạo hàng nghìn bảng Parquet/full permutation.

Với đường cong ngân sách, cùng một random permutation/peptide phải cho các
prefix lồng nhau. Dải dao động random được gắn nhãn riêng với CI theo protein.
2.000 lượt random không phải 2.000 biological replicate.

Budget-to-recall dùng tổng hit thật **chỉ để chấm hồi cứu**; không phải quy tắc
dừng triển khai vì khi đi thử thật chưa biết tổng hit. “Số phép đo tránh được”
chỉ là chênh ngân sách trong replay trên những ô đã có nhãn.

## 7. So sánh thống kê và giới hạn diễn giải

Hai contrast chính, cùng primary endpoint/candidate pool/ngân sách:

1. LoRA-D − Ridge W5-D.
2. LoRA-D − kỳ vọng random.

- Lấy paired difference theo peptide, bootstrap **5.000 lần theo group_id**,
  seed `1729`; mỗi lần lấy một nhóm phải mang toàn bộ peptide của nhóm, dùng
  cùng draw cho hai chính sách. Estimand vẫn là peptide-macro, không đổi sang
  group-macro hoặc cell-micro trong quá trình bootstrap.
- Báo effect bằng điểm phần trăm precision và số hit thêm; CI95 mô tả và CI
  Bonferroni **97,5%** cho hai contrast chính. Random chính dùng kỳ vọng giải
  tích; không trộn Monte Carlo noise vào CI protein mà không mô tả.
- Phân tích phụ dùng CI95 có nhãn mô tả; không gọi mọi hàng dương là phát hiện
  xác nhận độc lập. Hiệu chỉnh hai contrast mới không sửa được selection bias
  của toàn bộ lịch sử phát triển model.
- Với precision/recall/hit count, delta dương tốt hơn; với số lựa chọn để đạt
  recall, delta âm tốt hơn. CI phủ 0 là chưa phân giải, không chứng minh ngang nhau.
- Báo cả mỗi seed 17/29/43 và ensemble prediction. Các seed dùng chung outer
  folds/cohort; không lấy seed/fold làm số nghiên cứu độc lập.
- Báo phân tầng PSI(WT), fold và peptide khó, có denominator; không chọn riêng
  subgroup tốt để đưa ra kết luận toàn W. Miền không có hit ghi đúng `null` ở
  metric không định nghĩa, không loại khỏi Precision chính.
- CI bootstrap điều kiện trên prediction đã lưu; chưa bao gồm toàn bộ bất định
  do đổi outer split, huấn luyện lại hoặc assay mới.

**Quy tắc kết luận đề xuất:** chỉ nói “hỗ trợ ưu tiên tốt hơn cả hai đối chứng
trong replay này” khi cả hai CI điều chỉnh của contrast chính nằm trên 0. Nếu
chỉ hơn random thì ghi rõ chưa hơn W5; nếu CI cắt 0 thì giữ chưa phân giải.
Vẫn báo effect/CI và chi phí tính toán quan sát được, không chỉ nhãn đạt/chưa đạt.
Chưa có mức cải thiện tối thiểu do yêu cầu thực nghiệm đặt ra, nên không tự
thêm ngưỡng tiết kiệm hoặc đổi threshold nghiệm thu G2.

## 8. Các bước triển khai sau khi được yêu cầu thực hiện

1. **Khóa thiết kế:** lưu protocol/config v1, recipe, cohort, endpoint, ngân
   sách, tie/random/bootstrap seeds và quy tắc kết luận. Ghi đây là phân tích
   hậu kiểm; thay đổi sau khi xem utility phải là amendment, giữ kết quả cũ.
2. **Kiểm input/runtime:** thực hiện mục 3, ghi manifest/hash và dependency
   versions. `python3` hệ thống hiện chưa có `pyarrow`; xác minh môi trường phân
   tích đã có hoặc chuẩn bị môi trường riêng. Không cài đè môi trường CUDA.
3. **Dựng bảng chuẩn:** join trên ID, kiểm metadata và ensemble; tạo bảng dự
   đoán/nhãn chỉ đọc. Không load `.pt`/pickle và không tái sinh nhãn.
4. **Triển khai scorer nhỏ:** top-k, tie handling, random expectation, recall,
   budget-to-recall và bootstrap. Kiểm trường hợp không hit, toàn hit, tie toàn
   bộ, N<k, thiếu seed, đảo thứ tự dòng và duplicate ID. Đối chiếu top 5/10/20%
   với helper cũ ở điều kiện cùng denominator/tie; ghi khác biệt có chủ đích.
5. **Chạy và lưu đầy đủ:** kết quả chính trước, phụ sau; giữ peptide bất lợi,
   source hashes, thông báo thiếu dữ liệu và resource logs; không chọn lại recipe.
6. **Kiểm và báo:** đối chiếu JSON/CSV/plots, xác nhận số mẫu và denominator,
   kiểm vài ranking bằng tay; viết kết luận có giới hạn và bảng việc chưa làm.

Script dự kiến `research/oof-prioritization-2026-11-07/evaluate.py` **chưa tồn
tại theo kế hoạch này**; chỉ tạo khi triển khai. Chạy từ gốc repo bằng Python
của môi trường phân tích đã kiểm, CPU; không cần model/GPU để chấm OOF.
Không chạy `run-local.cmd` để thực hiện kế hoạch phân tích.

## 9. Đầu ra dự kiến và tiêu chí hoàn thành

Thư mục dự kiến: `research/oof-prioritization-2026-11-07/`. Đề xuất tên ngày lập
kế hoạch; ngày chạy thực ghi riêng trong manifest. Không tạo output rỗng để
đánh dấu một bước đã hoàn thành.

| Đầu ra | Nội dung phải kiểm được |
| --- | --- |
| `PROTOCOL.md`, `config.json` | Thiết kế khóa, amendment nếu có; phân biệt ngày lập/ngày chạy |
| `input-manifest.json`, `validation.json` | Source paths/hash, recipe/identity/seeds/folds, cohort alignment và kiểm scorer |
| `per-peptide.csv` | Candidate/hit/selected counts, policy, direction, budget, metric và lý do null |
| `results.json`, `summary.csv` | Primary contrasts/CI, random reference, secondary strata và denominator |
| `budget-curves.png` | Hit/recall theo ngân sách; dải random và CI có chú giải đúng loại |
| `README.md` | Phương pháp, kết quả kể cả âm, ví dụ ranking, giới hạn và cách tái tạo |
| `runtime.json` | Máy/runtime, phiên bản, thời gian/RAM đo được; không gọi là chi phí wet lab |

Các bảng ranking chi tiết theo cell và log nặng giữ local; Git chỉ nhận tài
liệu, script/config, manifest và kết quả nhỏ sau review kích thước. Không ghi
đè `output-analysis*`, `local-output-analysis*`, state/manifest campaign hoặc
bộ nghiên cứu wet lab đã lưu.

**Hoàn thành kỹ thuật:** input qua cổng; đủ chính sách/seed/budget đã chốt;
không mất mẫu im lặng; phép tính kiểm được; kết quả tái tạo theo input/config
đã pin; báo đầy đủ trường hợp metric thiếu. Kết quả âm vẫn là một đánh giá
hoàn tất, không phải lỗi cần đổi cách chấm.

**Giới hạn claim:** được báo khả năng ưu tiên và chênh số lựa chọn **hồi cứu**.
Chưa được báo CT553H tiết kiệm bao nhiêu giờ/tiền hoặc nâng tỷ lệ thành công
wet lab mới; chưa nghiệm thu model phục vụ, G2 hay G3. Tiền/giờ cần dữ liệu
quy trình thực hoặc kịch bản đơn giá có giả định tách riêng.

## 10. Nguồn trong repo và thông tin bàn giao

- [Đề xuất từ nghiên cứu wet lab](../../research/wet-lab-evidence-plan-2026-11-07/findings.md).
- [Protocol thực thi v3](../../research/kaggle-roadmap-2026-10-31/EXECUTION-PROTOCOL.md).
- [Phân tích local](../../research/kaggle-roadmap-2026-10-31/local-output-analysis.md) và
  [JSON](../../research/kaggle-roadmap-2026-10-31/local-output-analysis.json).
- [Phân tích Kaggle](../../research/kaggle-roadmap-2026-10-31/output-analysis.md) và
  [JSON](../../research/kaggle-roadmap-2026-10-31/output-analysis.json).
- [Kiểm độc lập OOF đã lưu](../../research/progress-review-2026-11-06/local-audit.md).

Metadata bàn giao theo template [ARS experiment plan](../../.agents/skills/academic-research-suite/ars/experiment-agent/templates/code_experiment_plan.md):
origin mode `plan`; version `oof_priority_plan_v1`; verification status
`UNVERIFIED` đối với thí nghiệm chưa chạy. RQ và mục đích đã có từ trao đổi;
các lựa chọn số trong tài liệu là đề xuất, không gán thành tác giả đã xác nhận.
Đây là một file kế hoạch, không tạo Material Passport JSON hoặc run ledger của
pipeline và không đánh dấu experiment complete.

**Phạm vi lượt này:** chỉ soạn `tmp.md` sau khi đọc mã/metadata và kiểm sự tồn
tại file input. Không chạy replay, bootstrap hoặc tính metric mới; không train
và không sửa các hồ sơ/kết quả khác của repo.
