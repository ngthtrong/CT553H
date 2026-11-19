# Nhánh 1: kế hoạch thực thi trên Windows/CUDA hiện tại

**Koren đã sẵn sàng:** Trọng cung cấp lại S4 đúng hash. Parser/QC và adapter
inference chiều dài đã PASS tại [koren-validation.json](koren-validation.json).
Launcher hiện nối scoring bổ sung sau core theo [KOREN-PROTOCOL.md](KOREN-PROTOCOL.md),
giữ nguyên checkpoint/code/identity core; xem [RUNBOOK.md](RUNBOOK.md).
Các mô tả thiếu đầu vào ở kế hoạch/snapshot cũ bên dưới là lịch sử.

**Cập nhật triển khai 16/11:** runner đã hỗ trợ refit, các script local dùng
được theo [RUNBOOK.md](RUNBOOK.md). Protocol/config/source lock đã khoá;
[preflight.json](preflight.json), [refit-validation.json](refit-validation.json)
và [analysis-validation.json](analysis-validation.json) ghi phạm vi kiểm.
Phần kế hoạch bên dưới giữ lịch sử thiết kế; các câu “chưa triển khai” ở đó
thuộc lượt lập kế hoạch trước. Trạng thái chạy thật xem `launch-status.json`
khi có, rồi dùng status-local để lấy tiến độ mới nhất.

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent.
- Origin Mode: plan, thực hiện inline; không dùng sub-agent.
- Origin Date: 2026-11-16, Asia/Taipei.
- Verification Status: **ANALYZED cho inventory; UNVERIFIED cho refit mới**.
- Version Label: branch1_windows_plan_v1.
- Phạm vi: triển khai và hoàn thành nhánh 1 của [plan.md](../../plan.md).
- Bằng chứng máy và đầu vào: [environment-audit.json](environment-audit.json),
  sinh bởi [audit-environment.py](audit-environment.py).
- Bằng chứng bảo vệ staging: [git-safety-validation.json](git-safety-validation.json),
  sinh bởi [validate-git-staging.py](validate-git-staging.py).

Đây là kế hoạch triển khai, **chưa phải protocol đã khoá, preflight GPU hay kết
quả thí nghiệm**. Các lệnh refit/status/pause mới ở dưới là giao diện cần thực
hiện. Hiện tại chỉ các lệnh audit và kiểm staging đã chạy được. Chưa thay đổi
launcher/runner, chạy train, chấm LoRA trên T, commit hoặc push trong lượt lập kế
hoạch này.

## 1. Kết luận và phạm vi máy này

Máy hiện tại đủ nền tảng để chạy refit ESM2-35M, đã có dữ liệu và artifact
development cần thiết. Tái dùng supervisor/worker/checkpoint hiện có; thêm loại
campaign refit vào cùng bộ máy. Chạy riêng campaign mới; campaign đã kết thúc
`ef138c84579c842e` và nguồn kế thừa của nó là đầu vào chỉ đọc.

Máy này làm cả code, GPU và CPU cần cho nhánh 1: refit, scoring, calibration,
thống kê, model card, inference parity, Koren khi có nguồn, phân rã sai số và
3–4 hình. Máy chính nhận artifact do Trọng tự copy, nhận code/kết quả chọn lọc
qua GitHub, rồi làm app/báo cáo/slide. Không triển khai nhánh 2–4 tại đây.

Nhánh 1 tính toán xong không tự thay model phục vụ hoặc đóng G2/G3. D-4 là quyết
định của Trọng/GVHD. Nếu thiếu Koren, có thể hoàn thành core nhưng **không ghi
hoàn thành toàn bộ nhánh 1**; thiếu quyết định D-4 phải ghi riêng.

## 2. Hiện trạng đã kiểm `[ĐO]`

Mọi số máy/đầu vào trong mục này lấy từ [environment-audit.json](environment-audit.json);
thời điểm và giới hạn phép kiểm nằm trong file đó. GPU/đĩa trống là snapshot.

| Hạng mục | Kết quả | Ý nghĩa |
| --- | --- | --- |
| Workspace/Git | `D:\thanhtrong\CT553H`, branch thực tế `run`, HEAD `f4640b5` | Không mặc định đang ở main hoặc tự chuyển branch |
| GPU | RTX 5060 Laptop, khoảng 8 GiB, CUDA khả dụng | Chưa kiểm forward/backward của refit mới |
| CPU/RAM | i9-14900HX, 24 core/32 luồng, khoảng 31,7 GiB RAM | Giữ 2 luồng toán như runtime nguồn; bootstrap chia chunk |
| Python/Torch | `.venv`, Python 3.11.9, Torch 2.13.0+cu130, driver 582.05 | Giữ nguyên; không cài requirements CPU lên đây |
| Gói chính | transformers 5.17.0, NumPy 2.1.3, pandas 2.3.3, pyarrow 23.0.1, sklearn 1.6.1 | LoRA đã tự cài trong `finetune.py`; không cần thêm peft |
| Đĩa | D còn khoảng 299 GiB; C khoảng 61 GiB | Đặt output/cache mới trên D, không chuyển mặc định sang C |
| Dữ liệu v3 | `data/processed/degron-data-v3-fullpsi/`, đủ 32 file đúng hash | Manifest khớp identity `b0376e05…` của nguồn |
| W | 122.412 cell, 235 peptide, 221 nhóm | Mỗi recipe × seed OOF phủ đúng tập W, không trùng cell |
| Campaign nguồn | 633 complete, 1 source_pending, 1 structure_pending | Không có job train cũ đang chờ tiếp tục |
| Artifact D | Đủ 30 cặp `fit.json`/`oof.parquet`, hash khớp state nguồn | Có cả artifact kế thừa nằm ở `e7097449883a51d8` |
| Base ESM2-35M | `output/weights/esm2_35m/`, revision `6fbf070e65b0b7291e7bbcd451118c216cff79d8` | Đã kiểm hash các file; không cần tải lại |
| W5-D trên T | `locked-transfer-w5/ordered-w5-D/held-scanning.parquet` khớp hash | Có baseline đã chốt để ghép theo cell ID |
| Storage v3 | local khoảng 19,78 GiB; official 2,86 GiB; weights 35M khoảng 130 MiB | Giữ nguyên nguồn; campaign mới không cần copy toàn bộ |
| Koren | Thiếu cả XLSX S4 và bảng interim; thiếu openpyxl | Là chặn đầu vào cho mục 1.14 |

Audit không load checkpoint model, không chạy inference/train và không đọc cột
outcome T. Nó chỉ kiểm byte/hash, metadata và cell ID. T trước lọc rep1 có
39.380 cell/1.414 peptide/733 nhóm; **đó không phải cohort primary**. Cohort
primary sau lọc rep1 phải giữ 39.234/1.410/730 như protocol đánh giá nguồn.

### Những điểm phải sửa so với kế hoạch cũ

1. `local-plan.json` đang trỏ `data/processed/v3-fullpsi`, thư mục không tồn tại.
   Plan refit mới phải trỏ data thực có ở trên. Không sửa `plan.json` lịch sử.
2. `output/local/latest.json` chứa đường dẫn tuyệt đối trước khi bỏ
   `topics/degron-footprint/`, hiện không tồn tại. `status`/`pause` mặc định sẽ
   tìm sai đường dẫn. Không gọi run cũ để chữa latest vì run sẽ initialize.
3. `state.json` nguồn có `artifact_campaign` tuyệt đối cũ. Resolver phải đọc
   theo campaign ID và kiểm source-plan/file hash; không tìm file đầu tiên cùng
   tên, không sửa chuỗi trong state lịch sử.
4. `initialize()` hiện buộc arms B/D, luôn sinh DAG 635 job và hash protocol v3
   cũ. Truyền `--config` mới **chưa đủ**: cần nhánh schema/DAG refit trong chính
   `local_campaign.py`, cùng dispatch các job mới.
5. `status-local.cmd`/`pause-local.cmd` chưa forward `%*`; CLI status/pause chưa
   có selector. Pause hiện chỉ tạo STOP rồi thoát, chưa đợi checkpoint xong.
6. Calibration hiện có đã tạo final calibrator từ ensemble OOF W, nhưng model
   card LoRA còn thiếu final model IDs. Không gọi lại toàn `calibration_stage()`
   rồi coi như đã có final neural refit/scoring.
7. `features()` assert WT dài đúng 28. Koren có peptide 12/23 aa và stop `*`;
   không thể chấm trực tiếp bằng đường inference hiện có.
8. `implementation_hash()` hiện **đã khác** hash lưu trong campaign nguồn;
   hash dùng byte nguồn, máy có `core.autocrlf=true`. Không quy chênh lệch này
   cho riêng newline khi chưa audit nguyên nhân, không ép resume nguồn cũ.
   Không đổi line ending/code/runtime khi campaign đang chạy. Máy chính có thể dùng
   inference artifact, nhưng không mặc định resume checkpoint qua OS/checkout.

### Epoch refit đã đối chiếu

Median lấy **riêng theo recipe × seed**, mỗi median từ 5 outer-fold epochs.
Đây là chính sách dự kiến trong [NEXT-EVALUATION.md](../reliability-transfer-2026-11-08/NEXT-EVALUATION.md)
§3; không gộp 15 fold để ấn một epoch cho cả recipe.

| Recipe | Seed | Epoch nguồn của 5 fold | Epoch refit |
| --- | --- | --- | --- |
| LoRA-D | 17 | 2, 2, 1, 2, 3 | 2 |
| LoRA-D | 29 | 4, 1, 1, 2, 2 | 2 |
| LoRA-D | 43 | 2, 1, 3, 3, 2 | 2 |
| frozen-D | 17 | 1, 1, 1, 2, 1 | 1 |
| frozen-D | 29 | 2, 3, 1, 1, 2 | 2 |
| frozen-D | 43 | 2, 3, 1, 1, 3 | 2 |

Vì vậy câu frozen-D median 1 trong `plan.md` cũ không đúng với cách khoá từng
seed. Đã điều chỉnh thành 1/2/2. Không có epoch nào được chọn từ outcome T.

## 3. Thiết kế thí nghiệm cần khoá trước execution

T đã được khảo sát bằng W5 và diagnostic. Tên kết quả là **đánh giá chuyển miền
hậu kiểm trên held-source đã khảo sát**, không phải kiểm chứng ngoài độc lập.
Giữ `development_not_gate_closure`.

Tạo `PROTOCOL.md`, `refit-plan.json`, `source-lock.json` trước scoring mới;
runner ghi `protocol_sha256` cùng mọi identity. Proposal ở đây không tự tạo
quyết định tác giả về mức lợi ích thực dụng. Nếu cần ngưỡng promotion, Trọng
chốt trước khi nhìn prediction mới; nếu chưa có, báo delta/CI và để promotion
chưa quyết, không mượn ngưỡng Q1 .02 PSI.

- Hai recipe ESM2-35M frozen-D và LoRA-D, seeds 17/29/43, đúng base revision,
  tokenizer, head và input của development. LoRA rank 8, alpha 16, query/value;
  FP32, batch 8, AdamW lr 1e-4, weight_decay .01, clip_grad 1 như code nguồn.
  Không tự đổi batch, precision, LR hoặc dùng full fine-tuning để cứu OOM.
- Refit **khởi tạo lại** từ base weights và head/adapter theo seed, toàn W
  122.412 cell. D dùng toàn dải; saturation PSI(WT) chỉ là metadata, không là
  feature. Không train thêm từ checkpoint outer-fold hay ghép 15 outer models
  thành final ensemble.
- Gọi `local_training.fit(..., refit=True, epochs=<median>)` với validation
  rỗng có schema hợp lệ; không dùng T làm validation dù nhánh refit không đọc
  loss của nó. Khẳng định không early stopping/chọn epoch mới.
- Chỉ scoring mới mở cohort T. Nhãn T không truyền vào model forward/fit,
  calibrator fit hoặc feature preprocessing. Ưu tiên tách frame feature khỏi
  bảng outcome; aggregate ghép nhãn sau bằng ID, kiểm 1–1.
- Ensemble regression là trung bình **ba raw predictions trước khi chấm**.
  Calibrator final đúng recipe fit từ raw ensemble OOF W và event labels W;
  sau đó áp lên raw ensemble final. Không lấy trung bình ba probability rồi
  gọi là cùng policy. Công bố score shift OOF → final, không tự fit correction
  bằng T. Có thể tái dùng calibrator cũ nếu chứng minh cùng input/hash/policy;
  job mới vẫn ghi provenance mới.
- Primary: peptide-macro MAE trên T rep1. Hai contrast:
  LoRA-D−frozen-D và LoRA-D−W5-D, delta âm có lợi. Paired group bootstrap
  5.000 lần, seed 1729, resample cùng group cho các model; CI hai phía 97,5%
  cho mỗi contrast của family 2 (Bonferroni), percentile 1,25%–98,75%.
  Tính mean trên peptide, không vô tình đổi thành group-macro/cell-micro.
- Giữ zero và constant từ W làm baseline phụ. Đề xuất constant cố định bằng
  mean `dpsi_mean` toàn W, ghi cách tính vào protocol trước T; không chọn giữa
  mean/median/zero sau khi thấy metric T.
- Secondary: RMSE, AUROC/AP hai chiều ở ±1, precision tại min(10,N), prevalence,
  no-hit peptide, Brier ba lớp, ECE hai chiều, PSI stratum, directed pair và
  similarity. Giữ cách phá tie seed 1729 như diagnostic cũ; lớp thiếu/metric
  không xác định ghi null + lý do + denominator, không điền 0.
- Replicate intersection: rep1/rep2/mean12 chấm trên cùng giao tập, rep1 toàn
  cohort vẫn primary. Không tăng số mẫu bằng cách coi seed/replicate là nhóm
  sinh học độc lập. CI conditional trên predictions đã fit; không bao trùm
  toàn bộ training/selection uncertainty. Secondary/diagnostic là exploratory.

## 4. Kiến trúc thực thi: mở rộng bộ máy hiện có

| File | Thay đổi cần làm | Tiêu chí |
| --- | --- | --- |
| `degron_v3/local_campaign.py` | Nhận `campaign_kind=refit_transfer_v1`, build DAG mới; identity chứa protocol refit, source lock, config và runtime; giữ schema campaign cũ | Không rơi vào DAG 635 job; mới và cũ khác fingerprint |
| `degron_v3/local_jobs.py` | Dispatch refit, score-held, calibrate-final, aggregate và job hoàn thiện; resolver nguồn theo allowlist ID/hash | Không sửa artifact nguồn, không dùng inheritance tokenizer-repair cho nghiên cứu mới |
| `degron_v3/local_training.py` | Tái dùng fit/predict/checkpoint; kiểm refit với validation rỗng và prediction prefix | Resume không mất optimizer/RNG/cursor; không đọc T lúc fit |
| `degron_v3/local_control.py` | Tái dùng STOP, atomic write, `.previous`, OS locks | Chỉ thay khi validator chỉ ra thiếu hỗ trợ cần thiết |
| `local-runner.py` | Thêm resolver selector cho status/pause, `pause --wait --timeout`; default refit chỉ chuyển sau khi plan/validator sẵn sàng | Status chỉ đọc, không initialize; campaign ID/path không thoát output root |
| `run-local.cmd` | Giữ entry point và forward `%*`; dùng config refit mặc định khi hoàn tất triển khai | Một supervisor và một worker; Python `-u -I` trong `.venv` |
| `status-local.cmd`, `pause-local.cmd` | Forward `%*` và giữ terminal dễ đọc | Target rõ campaign; không dùng latest sai đường dẫn |
| Thư mục nghiên cứu này | Protocol/config/preflight/validator/analysis/runbook/export manifest | Kết quả gọn cạnh script, artifact nặng dưới output hoặc `local/` |

Không tạo `run-refit.cmd`, runner Python song song hoặc launcher Linux khi chỉ
cần vận hành Windows hiện tại. Inference bundle cho máy chính có thể dùng đa
nền tảng, nhưng không phát sinh yêu cầu train trên máy chính.

`source-lock.json` liệt kê ID nguồn, source-plan SHA, file path **tương đối**,
bytes/SHA của 30 fit/OOF, weights và W5 baseline. Resolver ánh xạ tiền tố cũ
qua campaign ID đã allowlist dưới `output/local`; kiểm parent/source-plan hash
và từng file trước dùng. Chỉ cần subset đầu vào này cho refit, không gọi đó là
clone đủ để resume cả campaign cũ.

Plan mới dùng `data/processed/degron-data-v3-fullpsi`; vị trí thật được giải
tương đối từ repo marker `CLAUDE.md`. Timestamp audit/preflight không được đưa
vào phần fingerprint bất biến làm mỗi lần run sinh ID mới. Đường dẫn máy chỉ
lưu như provenance, không thay cho identity dữ liệu. Bất kỳ source/data/code/
recipe/runtime số học thay đổi đều phải bị phát hiện; không dùng cờ bỏ hash.

### DAG và điều kiện kết thúc

**Core 15 job**, xếp theo thứ tự topology trong queue hiện có:

| Nhóm | Số | Đầu vào/phụ thuộc | Artifact chính |
| --- | --- | --- | --- |
| `refit-{lora,frozen}-D-{seed}` | 6 | Preflight/source-lock/protocol hợp lệ | `model.pt`, checkpoint 2 thế hệ, `fit.json`, ID/hash train W |
| `calibrate-final-{recipe}` | 2 | OOF nguồn đã kiểm; không phụ thuộc outcome T | calibrator + policy/source hash/model-card metadata |
| `score-held-{recipe}-{seed}` | 6 | Model refit tương ứng và lock cohort | Raw prediction T + prefix progress, coverage/hash metadata |
| `aggregate-refit` | 1 | Cả 6 score và 2 calibrator complete; W5 baseline hợp lệ | Ensemble, results/CI, per-seed, denominator, score shift |

**5 job hoàn thiện** sau core, vẫn cùng supervisor/worker:

| Job | Việc | Mapping plan.md |
| --- | --- | --- |
| `model-card-parity` | Export 3 adapter/head LoRA + base reference; reload bằng đường inference dùng trên máy chính, so raw/probability/coordinates | 1.13 |
| `analyze-errors` | Kiểm riêng các giả thuyết PSI cao; giữ kết quả âm/chưa phân giải | 1.15 |
| `koren-rank-only` | Chuẩn hoá nguồn nội bộ, inference có policy chiều dài riêng, chấm từng substrate | 1.14 |
| `figure-export` | Sinh 3–4 hình và caption từ JSON/bảng đã khoá; xem render | 1.16 |
| `finalize-branch1` | Kiểm đủ artifact, hash manifest bàn giao, trạng thái checklist và giới hạn claim | 1.12–1.17, không thay quyết định D-4 |

Toàn bộ tính toán cần 20/20 job complete. Không dùng `source_pending` hoặc
`skipped_resource` để biến thiếu Koren thành đã xong; core-only có nhãn
`core_complete_branch1_incomplete`. Nếu tính toán đủ nhưng chưa có D-4, ghi
`compute_complete_decision_pending`, giữ mục 1.17 chưa đánh dấu.

Các job CPU phân tích/bootstrap cũng phải có điểm lưu tiến độ theo contrast/
chunk. Bootstrap resume giữ đúng RNG state hoặc index resample đã pin; không
vẽ lại CI khác sau pause. Parity/Koren/figure-export có bước kiểm artifact đã
xong và chạy lại an toàn sau crash. Deadline là mềm tại checkpoint; không hứa
tạm dừng tức thời trong một phép tính thư viện đang chạy.

## 5. Các giai đoạn thực hiện và kiểm chứng

| Bước | Công việc | Bằng chứng đủ để chuyển bước |
| --- | --- | --- |
| A — sửa đường dẫn/đầu vào | Tạo resolver, source-lock; xác minh Koren; kiểm disk/weights; ghi rõ scope core/toàn nhánh | Không sửa hash/state nguồn; source/data checks pass; thiếu đầu vào có danh sách |
| B — khoá protocol | Chốt policy ở §3, epoch từng seed, event labels, cohort IDs, 2 contrast, phiên bản code/config | PROTOCOL + source lock + protocol SHA đã ghi trước scoring mới |
| C — triển khai | Mở rộng chính runner/job/CLI hiện có; cấu hình refit; staging guard và export nhỏ | DAG đúng 15+5, không sinh lại family/fold jobs cũ |
| D — kiểm phần mềm | CPU invariants; ESM2-8M smoke trên subset W riêng; CUDA probe 35M W; resume/parity/CLI | Validation JSON; không ghi smoke vào campaign official |
| E — chạy core | Refit 6 model, score 6 seed, calibrate, aggregate | 15/15 complete, coverage T đúng, finite, không silent skip failed |
| F — hoàn thiện | Parity/model card, Koren, error diagnostics, hình, manifest | 20/20 complete; acceptance summary gọn và artifact SHA đầy đủ |
| G — bàn giao | Pause/đợi idle, copy file được manifest liệt kê, Trọng kiểm hash ở máy chính | Code/results Git-ready; inference parity từ bundle; D-4 riêng |

### Validator bắt buộc trước chạy thật

- Schema/config/DAG: ID duy nhất, không cycle, đúng seeds/epochs và dependencies;
  source/protocol/recipe thay đổi làm identity mới, runtime timestamp không gây
  ID trôi; thiếu source/Koren hoặc hash sai phải fail rõ.
- Phân hoạch: W và T không giao group theo split đã pin; train IDs chỉ W;
  calibrator IDs chỉ OOF W; pipeline fit không nhận outcome T; không âm thầm
  thêm scan_dev vào train. Cohort rep1 IDs đúng, join baseline 1–1.
- Resume: chạy liên tục so với pause giữa minibatch/epoch rồi resume; kiểm
  model/optimizer/RNG và prediction prefix. Phá một bản checkpoint thử nghiệm
  để kiểm fallback `.previous`; sai identity không được fallback sang run khác.
- CLI: status/pause đúng ID kể cả latest có đường dẫn cũ; pause đợi worker và
  supervisor dừng; timeout trả lỗi rõ; gọi run hai lần không có GPU worker thứ
  hai. Chỉ thử trong campaign smoke mới, không thử lên campaign lịch sử.
- Statistics: test paired group resampling/peptide denominator bằng ví dụ có
  các group khác số peptide; kiểm family size 2, dấu delta, null/rare class.
- Inference: reload artifact final, so hai đường inference trên cùng fixture
  W và cùng coordinate/AA order; đề xuất atol 1e-5, rtol 1e-5 FP32 trên cùng
  runtime, khoá trước kiểm. Cross-runtime ở máy chính phải đo và ghi riêng.
- Git: file nặng vẫn ignored; `results.json`/model card/manifest nhẹ được đưa
  lên Git theo danh sách; thử staging guard bằng repo tạm riêng.

### Ngân sách `[ĐỀ XUẤT, CHƯA ĐO]`

Triển khai/validator/protocol khoảng 4–6 ngày công; phân tích/Koren/hình/parity
khoảng 3–5 ngày khi đủ đầu vào. Các khoảng này có thể chồng lấp theo phụ thuộc,
không phải cam kết hoàn tất trong một phiên chat.

GPU core tạm dự phòng **4–8 giờ**, chạy từng phiên 2 giờ. Không giữ phép suy
4398 s/fold ≈ 12 phút/epoch của plan cũ: fold job gồm inner fit, early stopping,
outer refit và inference, không có số epoch cố định để chia. Sau refit đầu,
đọc thời gian/row/epoch thật để cập nhật ETA cho 6+5 epoch full-W và 6 lượt T;
cộng parity/Koren và checkpoint overhead. Lưu predicted và measured riêng.

Giữ VRAM fraction .75, batch 8/FP32; không đồng thời GPU job khác trong campaign.
Đề xuất reserve 5 GiB output mới và 30 GiB disk trống; preflight tính optimizer,
hai checkpoint thế hệ và file tạm, không chỉ weights. Budget local hiện có
50 GiB còn dư theo inventory; nếu vượt thì báo và chọn phương án có ghi nhận,
không tự xoá nguồn. Cắm nguồn, giữ máy thức; GPU chạy không phụ thuộc chat mở.

## 6. Run/status/pause/resume sau khi triển khai

**Các lệnh dưới đây là hợp đồng CLI cần triển khai, chưa dùng để chạy refit ở
trạng thái code hiện tại.** Trước khi chuyển default, luôn dùng `--config` rõ.

```powershell
# Chuẩn bị/preflight; không train. Lệnh preflight chưa được triển khai.
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\preflight.py --scope branch1

# Một lệnh chạy toàn DAG, gồm CPU/GPU theo dependencies.
.\run-local.cmd --config research\lora-refit-transfer-2026-11-16\refit-plan.json --hours 2

# Thay <campaign-id> bằng ID runner in ra; đừng gõ nguyên dấu <>.
.\status-local.cmd --campaign <campaign-id>
.\pause-local.cmd --campaign <campaign-id> --wait --timeout 300

# Resume bằng cùng lệnh, cùng bytes code/config/runtime/source.
.\run-local.cmd --config research\lora-refit-transfer-2026-11-16\refit-plan.json --hours 2
```

Sau khi validator pass, có thể chuyển default của entry point sang refit-plan
để chỉ cần `run-local.cmd --hours 2`; status/pause mặc định resolve campaign mới
bằng ID tương đối trong latest. Vẫn cho chỉ định ID để không nhầm target.

Pause tạo STOP đúng thư mục campaign, đợi bước train/predict/analysis commit và
worker/supervisor không còn chạy; cuối cùng báo `PAUSED` hoặc xác nhận campaign
đã idle. Hết timeout phải nói chưa pause xong, không báo thành công. Không đóng
terminal hoặc copy checkpoint trước xác nhận đó. `run` cùng config xoá STOP
qua luồng hiện có rồi tiếp tục; không chỉnh state/manifest bằng tay.

Mất điện/đóng terminal: chờ chắc worker cũ đã thoát, run lại cùng config để
kiểm identity/checkpoint, chấp nhận tính lại phần chưa commit. Job failed cần
đọc lỗi trước; không tự retry vô hạn. Dùng `--retry-failed` có chủ đích khi đã
giải quyết nguyên nhân. Nếu phải sửa code/runtime/recipe, tạo campaign mới;
không hứa giữ checkpoint qua thay đổi đó hoặc tự kế thừa kiểu sửa tokenizer.

Status nên in: ID/kind/protocol, complete/pending/paused/failed, job đang chạy,
epoch/cursor hoặc prediction rows, checkpoint age, thời gian/ETA đo thực, disk
và last error. Không báo overall complete chỉ vì supervisor đã SESSION ENDED.

## 7. Hoàn thiện ba phần dễ bị bỏ sót

### Koren S4: thiếu dữ liệu và khác chiều dài

Đầu vào cần Trọng copy nội bộ từ máy có sẵn:
`data/raw/koren-2018/NIHMS967427-supplement-11.xlsx`, hash pin tại
[data/README.md](../../data/README.md),
`c96973f2b2781b35a822527fa875e38df82f75da9ac327668d1d10114fdbcbeb`.
Không tự tải lại/đưa file gốc lên Git. Nếu dùng bảng chuẩn hoá phải có chain
hash tới XLSX và source parser, không coi bảng thiếu sequence là đủ scoring.

Parser an toàn dùng read_only/data_only, không chạy mã từ data/raw. Có thể tạo
env parser nhẹ dưới `local/koren-env/` để pin openpyxl mà không sửa `.venv`
CUDA; main env đọc Parquet/bảng đã chuẩn hoá. Nếu sinh/sửa file trong data/,
cập nhật sổ nguồn trong cùng phiên. Không chạy nguyên audit cũ nếu nó làm lại
MMseqs/đụng nguồn ngoài không cần cho rank-only.

Cần khoá adapter inference giữ chuỗi thực 12/23 aa: xử lý stop `*` ở cuối,
kiểm WT/mutant/coordinate, pooled embedding và 60 feature phụ tính theo chuỗi
thực; giữ đường 28-aa gốc và kiểm parity. Không pad peptide bằng acid amin giả
để vượt assert, không retrain bằng Koren. Đây là extrapolation chiều dài và
construct phải ghi limitation, không đồng nhất với Zhang 28-aa reporter.

Chấm Spearman/ranking trong từng substrate; báo số ô hợp lệ/loại trừ và tie
policy. Chỉ 9 substrate nên báo kết quả từng substrate và tổng hợp mô tả, không
coi 1.739 cell là 1.739 mẫu độc lập. Không scale 3-bin thành 6-bin, không dùng
calibrator Zhang để diễn giải xác suất/MAE cùng đơn vị trên Koren. Chỉ đưa metric
tổng hợp/chú thích được phép lên Git, không xuất sequence/bảng gốc qua kết quả.
Giữ vai trò nguồn lân cận; `source_pending` lịch sử không tự được đóng.

### Phân rã sai số PSI(WT) cao

Lập riêng file protocol diagnostic trước khi đọc prediction refit mới; phân
biệt diagnostic đã xem từ 08/11 với phép kiểm bổ sung. Ít nhất:

| Giả thuyết | Phép kiểm | Giới hạn |
| --- | --- | --- |
| Khác phân phối target và giới hạn thang PSI | Residual signed/MAE theo scan WT PSI, nhãn và prevalence/no-hit; so zero/constant/W5/frozen/LoRA | Association, không suy cơ chế sinh học |
| Score shift giữa outer-fit và final refit | Distribution/quantile W OOF vs prediction final trên W và T; reliability final trên T chỉ đánh giá | Prediction final trên W là in-sample, không gọi là generalization |
| Khác replicate/noise | Cùng intersection rep1/rep2/mean12 và disagreement strata | Không coi disagreement là measurement variance đã biết |
| Khác similarity/construct/cohort | Áp bins/policy đã pin, kiểm denominator và group counts | Không chọn subgroup thắng để đổi primary outcome |

Nếu cần prediction final trên W cho shift, ghi rõ đó là output phụ của refit
job, không dùng nó để fit calibrator final. Mọi thay đổi có đọc T để sửa model
chuyển sang nghiên cứu mới, không lẫn vào evaluation đã khoá. Được kết luận
"chưa phân giải"; giữ cả tầng LoRA/W5 tệ hơn zero.

### Hình và model card

Xuất 3–4 hình: hai primary contrasts kèm CI; performance theo PSI và baseline;
reliability/score shift; rank-only Koren nếu hợp lệ. Figure có caption, source
JSON/hash, denominators và nhãn development. File dữ liệu dùng vẽ phải nhỏ và
đủ tái tạo; chỉ xuất PDF/PNG/SVG chọn lọc, không dump mọi exploratory plot.
Không chỉnh `report/` trên máy này; kiểm LaTeX/float references khi máy chính
tích hợp nhánh 3.

Model card LoRA ghi cả 3 model IDs, epoch/seed, adapter/head SHA, base revision/
weights SHA, tokenizer, feature/AA/coordinate contract, calibrator SHA/policy,
input cohort IDs/hash và runtime. Ghi model ensemble ba seed; không gán metric
ensemble cho một seed. Parity kiểm từ artifact đã reload theo đường inference
thứ hai, không chỉ so hai lần gọi cùng object trong bộ nhớ.

## 8. Git: giữ bằng chứng nhỏ, chặn payload nặng

Audit cho thấy **không có model tensor `.pt`/`.safetensors` đang tracked**.
Một số ZIP/PDF lịch sử lớn hơn 10 MiB đã tracked; chúng là hồ sơ cũ, không tự
xoá/untrack/rewrite. `git fsck --connectivity-only` trả 0; có dangling trees và
6 `tmp_pack_*` khoảng 77 MiB do Git báo. Chưa có bằng chứng mất object liên kết;
đây không phải full content fsck. Không tự dọn `.git/objects`, reset, prune hoặc
force push trong campaign.

| Nhóm | Giữ tại máy chạy/copy thủ công | Đưa GitHub có chọn lọc |
| --- | --- | --- |
| Code và điều kiện tái lập | `.venv`, cache gói | `.py/.cmd`, config, protocol, dependency lock, README/RUNBOOK |
| Dữ liệu | raw/interim/processed, Koren nội bộ | data/README.md, SOURCE.md, hash/source inventory không chứa bảng nguồn |
| Model | checkpoint/optimizer/RNG, adapter/head, base weights, calibrator nhị phân | Model card, model ID, revision, bytes/SHA, inference parity report |
| Prediction | Cell-level Parquet/NPY, full OOF, W final in-sample predictions | Metrics JSON, per-seed/stratum/substrate summaries gọn, denominator |
| Vận hành | STOP/locks/session/latest/logs/progress tạm | Plan/DAG/source lock, milestone status snapshot, validation/acceptance |
| Trình bày/bàn giao | Bundle ZIP nếu cần copy nội bộ | 3–4 hình, caption, plot-data nhỏ, handoff-manifest.json |

Tái dùng layout heavy hiện có:

```text
research/kaggle-roadmap-2026-10-31/output/
  local/<new-id>/jobs/...       checkpoint/prediction/calibrator, vẫn ignored
  local/<old-id>/...            nguồn chỉ đọc, không di chuyển/xoá
  weights/esm2_35m/...          base weights, vẫn ignored
research/lora-refit-transfer-2026-11-16/
  README.md, PROTOCOL.md, RUNBOOK.md, refit-plan.json
  source-lock.json, validation.json, results.json, model-card.json
  figures/, tables/             chỉ output nhỏ được chọn
  handoff-manifest.json         đường dẫn tương đối + vai trò + size + SHA
  local/                       raw derivatives/tmp/parser env, ignored hẹp
```

`.gitignore` hiện đã giữ ngoại lệ plan/queue/state/fit metadata dưới output;
nhưng **model-card/results trong job mới chưa chắc được mở ngoại lệ**. Audit
canary đã chứng minh hai đường mới đó còn ignored. Cách ưu tiên: job ghi bản
máy móc vào output, finalize copy/ghi atomic **những báo cáo được đặt tên rõ**
ra thư mục nghiên cứu này và kiểm hash. Không mở mọi `*.json`/CSV dưới output,
không ignore toàn bộ thư mục nghiên cứu. `.gitignore` riêng ở đây chỉ chặn
`local/`; `environment-audit.json` và kết quả nhỏ vẫn hiện trong git status.

Guard đã có: [check-git-staging.py](check-git-staging.py), đọc **blob đang nằm
trong index**, không chỉ kích thước working file. Policy dự án cho thay đổi mới:
mỗi file ≤10 MiB, tổng staging ≤25 MiB; cấm model/checkpoint, data payload,
prediction arrays/archives của experiment, runtime/cache và control files.
Đổi đuôi JSON không tránh được kiểm size. Đây là guard thủ công, chưa cài hook;
không bảo vệ nếu bỏ qua nó và không phải bộ kiểm bí mật/giấy phép.

```powershell
# Đã có và dùng được ngay; không stage/commit bất kỳ file nào.
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\check-git-staging.py

# Chỉ khi Trọng yêu cầu commit: add các path cụ thể đã review, chạy guard,
# xem diff --cached rồi mới commit/push. Không dùng git add -f output/.
git diff --cached --stat
git diff --cached --check
```

Không commit mọi lần checkpoint hoặc stage toàn output; snapshot ở milestone
pause/core-complete/branch1-complete. Nếu file nặng bị staged, bỏ **chính file
đó** khỏi index, giữ nguyên local; đừng xoá dữ liệu để làm sạch status. Nếu file
nặng đã vào commit, dừng push để xử lý commit đó có review; không nghĩ thêm
gitignore sẽ xoá nó khỏi lịch sử. Không tự thay pre-commit hook đang có.

## 9. Copy sang máy chính và điều kiện đóng nhánh

Không cần làm một gói ZIP khổng lồ. `handoff-manifest.json` có ba nhóm rõ để
Trọng tự copy theo nhu cầu, mỗi file có relative path, bytes, SHA, license/source
reference và role:

1. **Code/kết quả nhẹ**: commit đã thống nhất, protocol/config/source-lock,
   metrics/tables/figures, model card, validation và parity, acceptance summary.
   GitHub đủ cho review bằng chứng, không đủ để tự resume train.
2. **Inference**: base snapshot 35M khoảng 130 MiB dùng chung, 3 LoRA adapter/
   head, calibrator final, preprocessing/AA/coordinate contract, manifest và
   fixture parity nhỏ có nguồn được phép. Frozen artifacts copy nếu cần đối
   chiếu. Không cần optimizer để suy luận; không copy `.venv` hoặc `.git`.
3. **Tái phân tích/resume**: prediction T/W phụ cần thiết, OOF D subset, input
   data đúng manifest và checkpoint 2 thế hệ nếu muốn resume **trên môi trường
   tương thích**. Không mặc định phải copy toàn bộ 633 job hoặc mọi pLM weights.
   Muốn tái lập toàn campaign lịch sử cần giữ thêm mọi source campaign được
   tham chiếu; muốn chạy inference không cần kéo chúng theo.

Pause/xác nhận idle trước copy checkpoint hoặc state đang biến động. Metadata
đặt tên relative; absolute paths chỉ là provenance cũ. Máy đích kiểm SHA **sau
copy**, cài runtime từ lock riêng và chạy inference parity trước tích hợp app.
Koren raw chỉ chuyển nội bộ nếu cần, không đưa vào bundle/Git public hay repo
private bằng cách bỏ qua quy tắc nguồn. Giữ bản gốc trên máy chạy cho tới khi
copy đã được kiểm và Trọng quyết định dọn.

Checklist đóng tính toán:

Checklist cập nhật 17/11/2026:

- [x] PROTOCOL/source lock/final plan có SHA và dấu thời gian trước scoring mới.
- [x] Core 15/15 complete, 0 failed. Tổng queue 19 complete + 1 `source_pending`:
  placeholder `koren-rank-only` giữ nguyên làm lịch sử, phần Koren chạy bổ sung
  riêng và đã complete (`koren-run-status.json`). Xem `completion-check-2026-11-17.json`.
- [x] Prediction đủ cohort/seed, ensemble/calibration đúng policy; primary CI
  family 2 và baselines/denominators/kết quả bất lợi đều được báo (`results.json`).
- [x] Model card không rỗng model IDs; inference parity cùng runtime pass
  (max diff 0,0). **Parity khác runtime trên máy chính vẫn chưa chạy.**
- [x] Koren rank-only đủ đầu vào/adapter/mapping; QC 9 substrate / 1.739 mutant,
  parity 28 aa 0,0. Không dùng nguồn lân cận để đóng `source_pending`; D-4 ngày
  17/11 xếp Koren là **bằng chứng khảo sát**.
- [x] Error analysis có phép kiểm từng giả thuyết: 3 giả thuyết ở
  `error-results.json`, `similarity_construct` ở `similarity-results.json` và
  [similarity-findings-2026-11-17.md](similarity-findings-2026-11-17.md).
  Hình/caption tái tạo từ JSON (`figure-results.json` khớp hash `results.json`).
- [ ] Git staged guard pass khi có staging thật; kết quả Git chọn lọc và manifest
  copy nặng được review; không có payload Koren hoặc tensor trong Git mới.
  *Chưa chạy: chưa commit/push gì trong lượt 17/11.*
- [x] Trọng ghi D-4 ngày 17/11 (phương án A, đóng G2 phạm vi development):
  [d4-decision-2026-11-17.md](../g2-acceptance-2026-11-07/d4-decision-2026-11-17.md).
  Không suy từ thắng/thua trên T. **Ghi nhận của GVHD chưa có.**

## 10. Việc đã làm trong lượt lập kế hoạch này

- Đọc plan/quy tắc/code runner, đo máy và kiểm đầu vào cần thiết.
- Lưu audit tái chạy được; kiểm hash data/30 cặp fit-OOF/weights/W5 baseline,
  chỉ đọc IDs T để kiểm metadata, không chấm outcome mới.
- Điều chỉnh plan tổng theo máy Windows hiện tại, median epoch thực, reuse
  launcher và phạm vi bàn giao; các mục nghiên cứu vẫn chưa đánh `[x]`.
- Thêm guard staging và validator 9 tình huống trong repo tạm: metadata nhỏ
  được phép; checkpoint kể cả `.previous`, raw data, payload prediction, STOP,
  file >10 MiB và tổng >25 MiB bị chặn. Không sửa index/objects repo thật.
- Chưa triển khai runner refit, PROTOCOL khoá, CUDA preflight, train/scoring
  hoặc quyết định khoa học. Bước tiếp theo là A–D ở §5, rồi mới chạy nặng.

Chạy lại inventory (chỉ viết báo cáo được chỉ định, không khởi tạo campaign):

```powershell
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\audit-environment.py
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\validate-git-staging.py
```
