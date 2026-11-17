# Kế hoạch thực hiện CT553H — biên bản theo dõi

Tạo ngày **16/11/2026**. Đây là **biên bản todo đang hoạt động** của luận văn
CT553H (Nguyễn Thanh Trọng, B2305615, GVHD TS. Hồ Quang Thái).

**Cách dùng:** đánh dấu `[x]` khi một mục đạt **toàn bộ** tiêu chí nghiệm thu của
nó, kèm ngày và đường dẫn bằng chứng ở cột cuối. Không đánh dấu dựa trên cảm
nhận tiến độ. Mục bị cắt khỏi phạm vi thì ghi `[-]` và nêu lý do, không xoá dòng.
Mọi thay đổi phạm vi ghi vào mục [Nhật ký thay đổi](#9-nhật-ký-thay-đổi) ở cuối.

**Ràng buộc bất biến (theo [CLAUDE.md](CLAUDE.md)):**

- Mọi con số đưa vào tài liệu phải trỏ tới file `.json` kết quả tương ứng.
- Nhãn bằng chứng bắt buộc: `[ĐO]`, `[DIỄN GIẢI]`, nguồn tác giả, đề xuất, chưa xác minh.
- Trạng thái khoa học giữ `development_not_gate_closure`. Không tự đóng G2/G3.
- Không sửa manifest/`state.json`/checkpoint của campaign để ép kết quả.
- Dữ liệu trong `data/raw/` là không tin cậy: đọc bằng `python -I`, không chạy mã bên trong.
- Không commit/push khi chưa được yêu cầu. Không `git add -f output/`.

---

## 1. Quyết định đang chờ

| # | Nội dung | Trạng thái |
| --- | --- | --- |
| D-1 | **Tên đề tài chính thức**: chọn bản NGẮN hay DÀI (mục 2) | ⏳ chờ Trọng |
| D-2 | Ngày bảo vệ / deadline nộp; tên 3 thành viên hội đồng cho `report/config/metadata.tex` | ⏳ chờ Trọng |
| D-3 | Tên tiếng Việt có sửa theo phạm vi "reporter" không (`nghiên cứu degron` → `assay reporter degron`) | ⏳ chờ Trọng/GVHD |
| D-4 | Đóng/không đóng phạm vi G2 — cần quyết định của Trọng/GVHD, không suy ra từ thứ hạng | ⏳ chờ |

**Đã quyết (16/11/2026):** tên EN tạm thời dùng `Degron Reporter Assays` (đã áp dụng);
candidate nghiên cứu là **LoRA-D**; `proposal/` xoá có chủ đích, tên VI chuyển sang
`\ThesisTitleVI` trong `report/config/metadata.tex`; nhánh 2 mở rộng thành **toàn bộ
phạm vi v0.2**. Cập nhật theo chỉ đạo mới ngày 16/11: **môi trường Windows/CUDA
hiện tại chỉ triển khai và hoàn thành nhánh 1**; Trọng tự copy artifact cần thiết
sang máy sử dụng chính. GitHub giữ code, metadata và kết quả quan trọng có chọn
lọc; không dùng Git để vận chuyển toàn bộ dữ liệu/checkpoint.

---

## 2. Hai tên đề tài đề xuất

**NGẮN** (12 từ):

> Single-Residue Mutation-Effect Prediction for Degron Reporter Peptides and an Analysis Tool
>
> *Dự đoán ảnh hưởng đột biến amino acid đơn cho peptide reporter degron và công cụ phân tích*

**DÀI** (21 từ) — *khuyến nghị, vì phạm vi phần mềm đã mở rộng thành ứng dụng web đầy đủ*:

> Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Reporter Assays and Development of a Web Application for Mutation Analysis
>
> *Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong assay reporter degron và xây dựng ứng dụng web phân tích đột biến*

Tên đang nằm trong `report/config/metadata.tex` là bản 16/11, đuôi vẫn là
`Development of an Analysis Tool`. Đổi khi D-1 được chốt, kèm biên bản
`report/title-sync-validation-<ngày>.md` mới.

---

## 3. Môi trường thực thi

| Môi trường | Vai trò | Ghi chú |
| --- | --- | --- |
| **WSL hiện tại** | Soạn script, phân tích CPU, viết báo cáo, dựng app | Không có CUDA; Node 24.22.3 (nvm), Docker 29.8.1, Playwright 3 trình duyệt (16/11); LibreOffice đã mất |
| **Windows/CUDA hiện tại**, `D:\thanhtrong\CT553H` | Toàn bộ công việc nhánh 1: chuẩn bị code, refit/scoring GPU, phân tích CPU, parity, xuất kết quả | RTX 5060 Laptop 8 GB, Python 3.11.9, Torch 2.13.0+cu130; xem audit bên dưới |
| **Máy sử dụng chính** do Trọng quản lý | Nhận code/kết quả từ GitHub và artifact được Trọng tự copy; triển khai nhánh 2–4 | Không copy `.venv` hoặc `.git`; model/data nặng dùng manifest SHA-256 riêng |

**Kế hoạch triển khai chi tiết và bằng chứng kiểm máy:**
[nhánh 1 trên Windows local](research/lora-refit-transfer-2026-11-16/README.md),
[environment-audit.json](research/lora-refit-transfer-2026-11-16/environment-audit.json).
Audit đã kiểm dữ liệu và artifact nguồn; **chưa** phải preflight CUDA forward/backward
hoặc kết quả refit. Hiện còn đường dẫn cũ cần resolver, thiếu đầu vào Koren S4,
và runner chưa hỗ trợ DAG refit mới.

Nguyên tắc: mọi thứ chạy trên máy CUDA phải khởi động được bằng **một lệnh**, tự
checkpoint, tạm dừng và chạy tiếp được, không cần tôi can thiệp.

**Cảnh báo định danh campaign:** thêm code vào `degron_v3/` làm đổi `code_sha256`
⇒ đổi fingerprint. Campaign `ef138c84579c842e` **đã kết thúc 633 job** nên không
có gì đang chờ resume; tuyệt đối **không** resume campaign cũ sau khi thêm code.
Công việc mới nhận thư mục output riêng theo fingerprint của plan mới.

---

## 4. Nhánh 1 — Thực nghiệm trên Windows/CUDA hiện tại

Tái dùng bộ máy campaign đã có (`degron_v3/local_campaign.py`, `local_jobs.py`,
`local_control.py`, `local_training.py`): `STOP`-file để tạm dừng, checkpoint mỗi
120 s khi train, `worker` chạy từng job theo deadline, `state.json` ghi tiến độ.
**Không viết runner song song.**

Kế hoạch chi tiết tách **15 job refit/transfer cốt lõi** và **5 job hoàn thiện
nhánh 1**. Quyết định D-4 vẫn do Trọng/GVHD, không phải job tự động. Bản kế hoạch
chi tiết hiện là đề xuất triển khai, chưa thay cho `PROTOCOL.md` khoá trước chấm T.

### 4.1 Chuẩn bị script trên máy hiện tại

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.1 | `research/lora-refit-transfer-2026-11-16/PROTOCOL.md` — khoá recipe, epoch nguồn, seed, endpoint, 2 contrast, CI97,5% Bonferroni, trước prediction refit mới trên T đã từng được khảo sát | Có protocol_sha256; khớp NEXT-EVALUATION §2–§4, giữ lịch sử đã xem T | 0,5 ngày | [x] 16/11 — PROTOCOL.md, source-lock.json, preflight.json |
| 1.2 | Job kind **`refit`** trong runner hiện có, code tách ở `degron_v3/local_refit.py` — refit toàn W, median riêng từng seed: LoRA-D **2/2/2**, frozen-D **1/2/2** cho 17/29/43 | Đọc selected_epoch từ 30 fit.json đã kiểm hash; không dùng median gộp hoặc T | 1 ngày | [x] 16/11 — source-lock.json, refit-validation.json; full-W đang chạy ở 1.11 |
| 1.3 | Job kind **`score-held`** — chấm T (39.234 cell / 1.410 peptide / 730 nhóm) bằng model vừa refit | Assert 0 nhãn T trong mọi bước fit/selection; output finite đủ cohort × seed | 0,75 ngày | [ ] |
| 1.4 | Job kind **`calibrate-final`** — calibrator học **chỉ** từ OOF W của đúng recipe | Công khai score shift giữa fold-fit và final refit | 0,5 ngày | [ ] |
| 1.5 | `refit-plan.json` — schema/DAG mới trong runner hiện có: 6 refit + 6 score + 2 calibrate + 1 aggregate; thêm 5 job parity/diagnostic/Koren/hình/finalize | Output mới theo fingerprint; source chỉ đọc, không inheritance checkpoint cũ | 0,5 ngày | [x] 16/11 — campaign aa4fc2b7ce29abf9, refit-validation.json |
| 1.6 | `preflight.py` — kiểm CUDA forward/backward, VRAM, data hash, 30 cặp fit/OOF, weights 35M, baseline W5, resolver đường dẫn và dung lượng | Phân biệt core/toàn nhánh; Koren thiếu đầu vào được báo rõ | 0,5 ngày | [x] 16/11 — preflight.json, source-lock.json; scope branch1 vẫn bị chặn |
| 1.7 | Tái dùng **run-local.cmd / status-local.cmd / pause-local.cmd**; CLI --config, --campaign, pause --wait | Một runner; pause đúng campaign, đợi checkpoint/OS locks, timeout không báo thành công | 0,5 ngày | [x] 16/11 — refit-validation.json và launch-status.json: pause/resume campaign thật |
| 1.8 | RUNBOOK.md — chạy, ngân sách giờ, resume, status và copy artifact | Có lệnh Windows thực dùng được | 0,25 ngày | [x] 16/11 — research/lora-refit-transfer-2026-11-16/RUNBOOK.md |
| 1.9 | validate-refit-plan.py — invariants CPU/ESM2-8M CUDA, cộng validator analysis/Git | Không outcome T trong smoke; tách output local, không gọi là benchmark | 0,5 ngày | [x] 16/11 — refit-validation.json, analysis-validation.json, git-safety-validation.json |

### 4.2 Chạy trên máy hiện tại (Trọng bấm, script tự lo phần còn lại)

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.10 | preflight PASS trên máy hiện tại | preflight.json chứa runtime/CUDA tests và source lock đầy đủ | 15–30 phút | [x] 16/11 — preflight.json: ESM2-35M frozen/LoRA forward-backward finite |
| 1.11 | Chạy refit + score + calibrate bằng script local hiện có | 15/15 core job complete; completion/Koren và D-4 có trạng thái riêng; không bỏ qua failed | Dự phòng 4–8 h chưa phải thời gian đo đầy đủ | [ ] Đang chạy 16/11 — aa4fc2b7ce29abf9, --hours 0; xem launch-status.json và status-local |

### 4.3 Phân tích và hoàn thiện artifact nhánh 1 trên máy hiện tại

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.12 | `analyze-refit.py` → `results.json`: paired group bootstrap 5.000×, CI97,5% cho family 2 contrast | Báo **cả** metric thuận và bất lợi kèm denominator; kết quả âm được giữ | 1,5 ngày | [ ] |
| 1.13 | Model card cuối cho LoRA-D (hiện `model_ids` đang rỗng) + inference parity | Parity giữa 2 triển khai suy luận; lineage hash đủ | 0,75 ngày | [ ] |
| 1.14 | Koren 2018 S4 — rank-only trong từng substrate; nguồn đã có đúng hash, parser chuẩn Python và adapter 12/23 aa đã kiểm CUDA | Chạy bổ sung sau core, giữ checkpoint/core identity; không padding/đổi thang, không đóng source_pending, không đưa bảng gốc lên Git | Tự nối sau core bằng launcher hiện hành | [ ] 16/11: koren-validation.json PASS; scoring thật đang chờ model refit, xem KOREN-PROTOCOL.md |
| 1.15 | Phân rã cơ chế sai số ở PSI(WT) cao (T strata gt5: W5-D **tệ hơn** zero +0,0958) | Mỗi giả thuyết có phép kiểm riêng; được phép kết luận "chưa phân giải" | 1,5 ngày | [ ] |
| 1.16 | Xuất 3–4 hình, bảng dữ liệu gọn, caption và dẫn nguồn JSON để máy chính đưa vào Chương 4 | Kiểm render, số liệu/hình khớp results.json; `check_float_references.py` thuộc bước tích hợp báo cáo tại nhánh 3 trên máy chính | 1 ngày | [ ] |
| 1.17 | Biên bản quyết định phạm vi G2 (D-4) | Có chữ ký/ghi nhận của Trọng hoặc GVHD | 0,5 ngày | [ ] |

**Bỏ khỏi phạm vi:** `structure_pending`/SaProt (chỉ có 8 cấu trúc AlphaFold, giả định
WT-3Di yếu) `[-]`; full fine-tuning (~40 h GPU) `[-]`; wet lab `[-]`.

---

## 5. Nhánh 2 — Ứng dụng v0.2 đầy đủ

**Kế hoạch chi tiết:** [system/implementation-plan-2026-11-16.md](system/implementation-plan-2026-11-16.md) — 13 gói công việc WP0–WP12, truy vết UC → FR → test ID. Bảng dưới là mức tổng; đánh dấu ở cả hai nơi.

Giao diện dựng bằng skill **`ui-ux-pro-max`** kết hợp token Workspace UI v2.

> **Quy tắc hoà giải hai nguồn thiết kế:** thang màu khoa học là **bằng chứng**,
> không phải thẩm mỹ. Viridis đảo cho xác suất, PuOr cho raw score, hatch ô WT,
> cảnh báo đứng trước điểm số trong DOM — **giữ nguyên** dù skill gợi ý khác.
> Mọi thứ còn lại (typography, spacing, sidebar, state, motion, icon) theo skill.

Hiện trạng đo được 16/11: **13 endpoint, 11 bảng, 1 migration, 277 file test**.
Không có bảng/router nào cho projects, jobs, import, comparison.

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 2.1 | Node 24 trong WSL (`package.json` yêu cầu `>=24.22.1 <25`) | `npm run build` và `npm test` chạy xong, ghi số case thực tế | 0,5 ngày | [x] 16/11 — `system/app/rebaseline-2026-11-16.json` |
| 2.2 | Hệ thiết kế: chạy `ui-ux-pro-max` + token v2 3 lớp + AppShell + sáng/tối | 0 axe violation trên các view chính ở 360/768/1280 px | 2–3 ngày | [~] 16/11 — hệ thiết kế + shell + `/__styleguide` đạt (`system/app/frontend/e2e/design.spec.ts`); restyle từng màn hình ở 2.11 |
| 2.3 | Schema mới theo `db-design.md` §11: `project`, `analysis_job`, `job_item`, `analysis_run`, `analysis_cell`, `import_dataset`, `import_observation`, `comparison` + migration `0002_workspace`, `0003_domain_borderline` | Migration up/down chạy sạch trên DB rỗng và trên `dev.db` hiện có | 1,5 ngày | [x] 16/11 — `system/app/tests/test_workspace_schema.py`, `system/app/DEVIATIONS.md` §8 (chạy trên bản sao `dev.db` và PG 16) |
| 2.4 | Durable job runner: hàng đợi bền, tiến độ, huỷ, **phục hồi sau restart** + API | Kill tiến trình giữa chừng rồi khởi động lại → job tiếp tục, không mất/không nhân đôi | 2–3 ngày | [x] 16/11 — `system/app/tests/test_jobs.py::test_batch05_sigkill_worker_process_then_restart` |
| 2.5 | Whole-protein flow: tiling step 23 toàn chuỗi → batch predict → footprint cấp protein | Toạ độ 1-based khớp `dev.db` (482.216 tile); không xếp hạng sinh học xuyên tile | 2 ngày | [ ] |
| 2.6 | Projects & history: CRUD, gắn run vào dự án, lịch sử, snapshot | Khởi động lại app vẫn còn dữ liệu; snapshot tái hiện đúng kết quả cũ | 2 ngày | [x] 16/11 (backend) — `system/app/tests/test_workspace_api.py`; màn hình ở WP9 |
| 2.7 | Import + comparison: nạp CSV thực nghiệm, map về tile/ô, đối chiếu dự đoán ↔ đo | **Import không bao giờ retrain**; ô không map được phải hiện rõ, không im lặng bỏ | 3 ngày | [x] 16/11 (backend) — `system/app/tests/test_import.py`; màn hình ở WP9 |
| 2.8 | Export mở rộng: CSV/JSON/bundle provenance theo run và theo project | Bundle chứa model id, nguồn, phiên bản, nhãn development | 1,5 ngày | [x] 16/11 (backend) — `system/app/backend/api/exports.py`, test BATCH-06/HIST-02/IMP-04 |
| 2.9 | PostgreSQL 16 local (Docker) + parity SQLite↔PG | Bộ test chạy xanh trên **cả hai** DB | 1,5 ngày | [x] 16/11 — SQLite 285 pass; PG 273 pass + 12 skip SQLite-only (`make test-pg`) |
| 2.10 | Cổng R3 đúng: `P = σ(10.187 − 3.275·x)`, tier-2 `P = σ(8.457 − 1.911·x̂)`, trạng thái `measured_borderline`/`predicted_borderline` | Golden test khớp `run_r3.py`; bỏ hẳn so sánh sai `psi <= 4.0` | 1,5 ngày | [x] 16/11 — `system/app/tests/test_gate.py`, `system/app/DEVIATIONS.md` §7 (25,35/8,73/65,93%) |
| 2.11 | View phân tích: ma trận 28×20, **footprint track 1D (mới)**, ranking, inspector, shortlist, panel ưu tiên top-k | 532 ô + 28 WT; track tái tính khớp ma trận trong 1e-9; panel ưu tiên có nhãn "hồi cứu, development" **trước** số | 3 ngày | [ ] |
| 2.12 | Đổi model phục vụ sang LoRA-D *(phụ thuộc 1.13)* | Cần thêm `torch`+`transformers` vào backend (hiện chỉ có numpy) + đo lại latency + kích thước cài đặt; giữ npz làm mặc định bật/tắt bằng cấu hình | 2–4 ngày | [ ] |
| 2.13 | Kiểm thử: pytest + vitest + Playwright cho flow mới, axe, đối chiếu `system/test-plan.md` | Ghi **số case thực tế**, không trích số lịch sử 22/10 | 3 ngày | [ ] |
| 2.14 | Ảnh chụp + clip demo (cho `report/appendices/a-installation-user-guide.tex`) | Ảnh từ app thật với dữ liệu thật, không phải fixture | 0,5 ngày | [ ] |

**Tổng ≈ 35 ngày làm việc (≈ 7 tuần)** theo phân rã chi tiết — cao hơn ước lượng 26–30 ngày ban đầu vì thêm đo lại baseline (WP0), contract (WP3), PostgreSQL (WP8) và kiểm thử 3 trình duyệt × 4 breakpoint. Đây là đường găng của toàn bộ luận văn.

---

## 6. Nhánh 3 — Báo cáo LaTeX

Chỉ bắt đầu sau khi nhánh 1 chốt số và nhánh 2 đạt tiêu chí. Khung chương rỗng và
sơ đồ không chứa số được phép làm sớm.

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 3.1 | Xoá 5 dấu `[PENDING]` (`acknowledgements.tex:7`, `b-supplementary:5`, `a-installation:36,49`, `04-testing:687`) | `grep -c PENDING` = 0 trên `chapters/ frontmatter/ appendices/` | 1 ngày | [ ] |
| 3.2 | Chương 4: đánh giá phần mềm thật — input validation, interface, response time, usability | Mỗi số trỏ tới file kết quả của 2.13 | 1,5 ngày | [ ] |
| 3.3 | Kết quả T + phân rã sai số vào Chương 4 và Kết luận | Giữ nguyên kết quả âm; nhãn `[ĐO]`/`[DIỄN GIẢI]` đúng | 1,5 ngày | [ ] |
| 3.4 | Sơ đồ mới: ERD cập nhật (7 bảng mới), kiến trúc có job runner, sequence diagram job/import, user flow | Hình đánh số theo chương, `\label` ngay sau `\caption`, có `Figure~\ref` dẫn | 1,5 ngày | [ ] |
| 3.5 | Chương 3 mở rộng: thiết kế job bền, import/comparison, PostgreSQL | Khớp thiết kế thực thi, không mô tả thứ chưa làm | 2 ngày | [ ] |
| 3.6 | Cân lại hình/bảng (đang **12 hình / 58 bảng**) | Không trang nào trống > ~1/3 vùng nội dung mà không ghi lý do | 1 ngày | [ ] |
| 3.7 | Đổi tên theo D-1 + biên bản title-sync mới | Bìa/đầu trang/metadata PDF/slide trùng từng ký tự | 0,5 ngày | [ ] |
| 3.8 | `make -C report all` + `make -C report check` + `scripts/check_float_references.py` + rà PDF **một mặt và hai mặt** ở cỡ đọc được | Cả 3 lệnh PASS; lưu phạm vi kiểm + hash PDF vào hồ sơ validation **mới**, không ghi đè biên bản cũ | 1 ngày | [ ] |

---

## 7. Nhánh 4 — Slide PPTX (tiếng Anh)

Một deck duy nhất: `presentation/Degron_Research_Report.pptx` (hiện 94 slide).
Không tạo deck `v2`/`final`/HTML song song.

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 4.1 | Chuyển nguồn tên tiếng Việt khỏi `proposal/` đã xoá | `manage.py` đọc `\ThesisTitleVI`; hết `FileNotFoundError` | — | [x] 16/11 — `report/title-sync-validation-2026-11-16.md` |
| 4.2 | Cài lại LibreOffice (`/tmp/isds-lo/root` đã mất) | `manage.py render --soffice …` xuất được PDF | 0,25 ngày | [ ] |
| 4.3 | ⛔ Dàn ý deck bảo vệ ~22 slide chính + phần còn lại xuống appendix | **Trọng duyệt dàn ý trước khi dựng** | 0,5 ngày | [ ] |
| 4.4 | Dựng tại chỗ: đồng bộ tên, **không footnote**, ưu tiên hình/sơ đồ/ảnh app, chữ tối thiểu | `manage.py check` PASS gồm `input_hashes`, `language_validation`, `numerical_evidence` | 2 ngày | [ ] |
| 4.5 | Rà ảnh render từng slide | Không tràn chữ, không thiếu glyph, tương phản đủ | 0,5 ngày | [ ] |

---

## 8. Thứ tự và rủi ro

Nhánh 1 ‖ nhánh 2 chạy song song → cổng 🚦 (số liệu chốt **và** app đạt tiêu chí)
→ nhánh 3, rồi nhánh 4.

| Tuần | Nhánh 1 | Máy CUDA | Nhánh 2 (WP theo kế hoạch chi tiết) | Nhánh 3–4 |
| --- | --- | --- | --- | --- |
| T1 | 1.1–1.9 viết script | — | WP0, WP1, WP2 | — |
| T2 | 1.12 phân tích | **1.10, 1.11 chạy** | WP3, WP4, bắt đầu WP5 | — |
| T3 | 1.13, 1.14 | — | WP5, WP9.1–9.4 | khung chương |
| T4 | 1.15, 1.16, 1.17 | — | WP6, WP9.5–9.6 | — |
| T5 | 🚦 số liệu chốt | — | WP7, WP9.7–9.12 | — |
| T6 | — | — | WP8, WP10 | — |
| T7 | — | — | WP11, WP12 🚦 | — |
| T8 | — | — | sửa lỗi | 3.1–3.6 |
| T9 | — | — | — | 3.7, 3.8, 4.2–4.5 |

**≈ 9 tuần.** Phụ thuộc D-2 (ngày bảo vệ) để biết có vừa hay không.

| Rủi ro | Dự phòng |
| --- | --- |
| 8 tuần vượt deadline | Thứ tự cắt: 2.9 PostgreSQL → giữ SQLite + ghi `DEVIATIONS.md`; 2.7 → chỉ import, bỏ comparison; 2.12 → giữ npz, LoRA-D chỉ là candidate đã export; 2.5 → giới hạn số tile |
| Máy CUDA hiện tại dừng giữa chừng | Tái dùng STOP/checkpoint 120 s/resume; bổ sung selector đúng campaign và xác nhận pause; không sửa state bằng tay |
| Thêm code vào `degron_v3/` đổi fingerprint | Plan mới có thư mục output riêng; **không** resume `ef138c84579c842e` |
| LoRA trên T **không** hơn zero/W5-D | Kết quả âm hợp lệ; đóng góp chuyển sang benchmark/phương pháp/phần mềm. **Không** đổi threshold hay model để cứu outcome |
| `ui-ux-pro-max` đề xuất palette đè thang màu khoa học | Quy tắc hoà giải ở mục 5 |
| 277 file test vỡ hàng loạt khi đổi UI | Giữ `data-testid` và thứ tự DOM; sửa từng bước nhỏ |
| `torch` trong backend làm vỡ contract 13 path | Giữ npz làm mặc định, LoRA-D bật bằng cấu hình |

---

## 9. Nhật ký thay đổi

| Ngày | Thay đổi | Người |
| --- | --- | --- |
| 16/11/2026 | Tạo biên bản. Tên EN đổi sang `Degron Reporter Assays`; tên VI chuyển sang `\ThesisTitleVI`; `proposal/` xác nhận xoá có chủ đích | Trọng + Claude |
| 16/11/2026 | Nhánh 2 mở rộng từ "demo 4 tính năng" thành **toàn bộ phạm vi v0.2**; giao diện dùng skill `ui-ux-pro-max` | Trọng |
| 16/11/2026 | Nhánh 1 chuyển từ Kaggle sang **máy CUDA local khác**, tái dùng bộ máy campaign có sẵn thay vì viết runner mới | Trọng |
| 16/11/2026 | Thêm kế hoạch chi tiết nhánh 2 (`system/implementation-plan-2026-11-16.md`). Sửa tên bảng mục 2.3 cho khớp `db-design.md` §11. Tổng nhánh 2 tăng lên ≈ 35 ngày; timeline toàn bộ ≈ 9 tuần | Claude |
| 16/11/2026 | WP0 xong: baseline đo lại tại `system/app/rebaseline-2026-11-16.json`. PostgreSQL 16 chạy bằng Docker thay `sudo apt` (G-2). Sửa shebang `.venv` của app còn trỏ đường dẫn `topics/degron-footprint/` cũ | Claude |
| 16/11/2026 | Nhánh 2: xong WP0, WP2–WP8 (backend đủ 24 operation, job bền, import/so sánh, cổng R3, PostgreSQL) và WP1 (hệ thiết kế Fira Sans/Fira Code, shell sidebar). Còn WP9 (13 màn hình), WP10 (chờ nhánh 1), WP11, WP12. `dev.db` đã migrate `0003` và nạp lại nhãn R3; bản trước giữ ở `.data/backup/dev-2026-11-16.db` | Claude |
| 16/11/2026 | Cập nhật theo môi trường thật: Windows/CUDA hiện tại chỉ làm nhánh 1; tái dùng run/status/pause-local, Git giữ kết quả nhẹ chọn lọc, Trọng copy artifact nặng. Audit phát hiện đường dẫn cũ, frozen-D epoch theo seed 1/2/2 và thiếu Koren; kế hoạch chi tiết ở research/lora-refit-transfer-2026-11-16/ | Trọng + Codex |
| 16/11/2026 | Trọng yêu cầu triển khai và chạy nặng. Thêm refit_transfer_v1 vào runner hiện có, khoá protocol/source, CUDA/resume/analysis checks PASS; khởi chạy aa4fc2b7ce29abf9 không giới hạn giờ. Koren/diagnostic similarity đầy đủ/D-4 chưa hoàn tất | Trọng + Codex |
| 16/11/2026 | Trọng cung cấp lại S4 đúng hash và yêu cầu pause/chạy lại không giới hạn. Giữ nguyên core/checkpoint aa4fc2b7ce29abf9; launcher nối phân tích Koren riêng sau core bằng cùng locks/STOP. Parser/QC và parity chiều dài PASS; source_pending trong queue cũ giữ lịch sử, scoring bổ sung có trạng thái riêng | Trọng + Codex |
