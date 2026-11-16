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
phạm vi v0.2**; toàn bộ tính toán chạy trên **một máy CUDA khác**, không phải môi
trường WSL hiện tại.

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
| **WSL hiện tại** | Soạn script, phân tích CPU, viết báo cáo, dựng app | Không có CUDA; `node` chưa có; LibreOffice đã mất |
| **Máy CUDA khác** | Chạy toàn bộ refit/scoring GPU **và** các bước CPU của campaign | Đã có sẵn OOF/`results`/`status` giống repo ⇒ **không cần gói bàn giao** |

Nguyên tắc: mọi thứ chạy trên máy CUDA phải khởi động được bằng **một lệnh**, tự
checkpoint, tạm dừng và chạy tiếp được, không cần tôi can thiệp.

**Cảnh báo định danh campaign:** thêm code vào `degron_v3/` làm đổi `code_sha256`
⇒ đổi fingerprint. Campaign `ef138c84579c842e` **đã kết thúc 633 job** nên không
có gì đang chờ resume; tuyệt đối **không** resume campaign cũ sau khi thêm code.
Công việc mới nhận thư mục output riêng theo fingerprint của plan mới.

---

## 4. Nhánh 1 — Thực nghiệm (script chạy trên máy CUDA khác)

Tái dùng bộ máy campaign đã có (`degron_v3/local_campaign.py`, `local_jobs.py`,
`local_control.py`, `local_training.py`): `STOP`-file để tạm dừng, checkpoint mỗi
120 s khi train, `worker` chạy từng job theo deadline, `state.json` ghi tiến độ.
**Không viết runner song song.**

### 4.1 Viết script (tôi làm trên WSL)

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.1 | `research/lora-refit-transfer-2026-11-16/PROTOCOL.md` — khoá recipe, epoch nguồn, seed, endpoint, 2 contrast, CI97,5% Bonferroni, **trước khi nhìn T** | Có `protocol_sha256`; khớp `NEXT-EVALUATION.md` §2–§4 | 0,5 ngày | [ ] |
| 1.2 | Job kind **`refit`** trong `degron_v3/local_jobs.py` — refit toàn W ở epoch cố định (LoRA-D median 2, frozen-D median 1), 3 seed | Đọc `selected_epoch` từ `fit.json` của campaign cũ; không chọn lại epoch bằng T | 1 ngày | [ ] |
| 1.3 | Job kind **`score-held`** — chấm T (39.234 cell / 1.410 peptide / 730 nhóm) bằng model vừa refit | Assert 0 nhãn T trong mọi bước fit/selection; output finite đủ cohort × seed | 0,75 ngày | [ ] |
| 1.4 | Job kind **`calibrate-final`** — calibrator học **chỉ** từ OOF W của đúng recipe | Công khai score shift giữa fold-fit và final refit | 0,5 ngày | [ ] |
| 1.5 | `refit-plan.json` — plan mới sinh fingerprint riêng, liệt kê 6 refit + 6 score + 2 calibrate + 1 aggregate | `initialize()` tạo thư mục output mới, không đụng `ef138c84579c842e` | 0,5 ngày | [ ] |
| 1.6 | `preflight.py` — kiểm máy đích: CUDA/torch/VRAM, hash data tables, có đủ `fit.json` + `oof.parquet` của 30 fold job, dung lượng trống | Thiếu bất kỳ thứ gì thì dừng với thông báo rõ, không chạy nửa vời | 0,5 ngày | [ ] |
| 1.7 | Launcher: `run-refit.cmd` / `run-refit.sh`, `status-refit.*`, `pause-refit.*` | Chạy được cả Windows PowerShell lẫn Linux bash; `pause` tạo `STOP`, xác nhận `PAUSED` rồi mới thoát | 0,5 ngày | [ ] |
| 1.8 | `RUNBOOK.md` — thứ tự chạy, ngân sách giờ, cách resume sau mất điện, cách đọc `status` | Trọng chạy được mà không hỏi lại | 0,25 ngày | [ ] |
| 1.9 | Validator `validate-refit-plan.py` — kiểm invariants trên CPU trước khi giao | PASS trên WSL; smoke bằng ESM2-8M | 0,5 ngày | [ ] |

### 4.2 Chạy trên máy CUDA (Trọng bấm, script tự lo phần còn lại)

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.10 | `preflight` PASS trên máy đích | Báo cáo môi trường ghi vào `env.json` | 15 phút | [ ] |
| 1.11 | Chạy refit + score + calibrate (tạm dừng/chạy tiếp tuỳ ý) | 15/15 job `complete`; `state.json` không có job `failed` chưa giải thích | **~4–6 h GPU** *(ước lượng từ `output-review-2026-11-06/results.json`: tune-lora median 4.398 s/fold ≈ 12 phút/epoch)* | [ ] |

### 4.3 Phân tích và viết (tôi, CPU, sau khi có output)

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 1.12 | `analyze-refit.py` → `results.json`: paired group bootstrap 5.000×, CI97,5% cho family 2 contrast | Báo **cả** metric thuận và bất lợi kèm denominator; kết quả âm được giữ | 1,5 ngày | [ ] |
| 1.13 | Model card cuối cho LoRA-D (hiện `model_ids` đang rỗng) + inference parity | Parity giữa 2 triển khai suy luận; lineage hash đủ | 0,75 ngày | [ ] |
| 1.14 | Koren 2018 S4 — đánh giá **rank-only trong từng substrate** (9 substrate) | Không trộn thang 3-bin với 6-bin; gọi đúng là *nguồn lân cận*, **không** đóng `source_pending`; không đưa bảng gốc lên git (license NIHMS) | 1 ngày | [ ] |
| 1.15 | Phân rã cơ chế sai số ở PSI(WT) cao (T strata gt5: W5-D **tệ hơn** zero +0,0958) | Mỗi giả thuyết có phép kiểm riêng; được phép kết luận "chưa phân giải" | 1,5 ngày | [ ] |
| 1.16 | 3–4 hình kết quả mới cho Chương 4 | `check_float_references.py` PASS | 1 ngày | [ ] |
| 1.17 | Biên bản quyết định phạm vi G2 (D-4) | Có chữ ký/ghi nhận của Trọng hoặc GVHD | 0,5 ngày | [ ] |

**Bỏ khỏi phạm vi:** `structure_pending`/SaProt (chỉ có 8 cấu trúc AlphaFold, giả định
WT-3Di yếu) `[-]`; full fine-tuning (~40 h GPU) `[-]`; wet lab `[-]`.

---

## 5. Nhánh 2 — Ứng dụng v0.2 đầy đủ

Giao diện dựng bằng skill **`ui-ux-pro-max`** kết hợp token Workspace UI v2.

> **Quy tắc hoà giải hai nguồn thiết kế:** thang màu khoa học là **bằng chứng**,
> không phải thẩm mỹ. Viridis đảo cho xác suất, PuOr cho raw score, hatch ô WT,
> cảnh báo đứng trước điểm số trong DOM — **giữ nguyên** dù skill gợi ý khác.
> Mọi thứ còn lại (typography, spacing, sidebar, state, motion, icon) theo skill.

Hiện trạng đo được 16/11: **13 endpoint, 11 bảng, 1 migration, 277 file test**.
Không có bảng/router nào cho projects, jobs, import, comparison.

| # | Việc | Tiêu chí nghiệm thu | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 2.1 | Node 24 trong WSL (`package.json` yêu cầu `>=24.22.1 <25`) | `npm run build` và `npm test` chạy xong, ghi số case thực tế | 0,5 ngày | [ ] |
| 2.2 | Hệ thiết kế: chạy `ui-ux-pro-max` + token v2 3 lớp + AppShell + sáng/tối | 0 axe violation trên các view chính ở 360/768/1280 px | 2–3 ngày | [ ] |
| 2.3 | Schema mới: `project`, `project_item`, `job`, `job_event`, `import_dataset`, `import_cell`, `comparison` + migration `0002…` | Migration up/down chạy sạch trên DB rỗng và trên `dev.db` hiện có | 1,5 ngày | [ ] |
| 2.4 | Durable job runner: hàng đợi bền, tiến độ, huỷ, **phục hồi sau restart** + API | Kill tiến trình giữa chừng rồi khởi động lại → job tiếp tục, không mất/không nhân đôi | 2–3 ngày | [ ] |
| 2.5 | Whole-protein flow: tiling step 23 toàn chuỗi → batch predict → footprint cấp protein | Toạ độ 1-based khớp `dev.db` (482.216 tile); không xếp hạng sinh học xuyên tile | 2 ngày | [ ] |
| 2.6 | Projects & history: CRUD, gắn run vào dự án, lịch sử, snapshot | Khởi động lại app vẫn còn dữ liệu; snapshot tái hiện đúng kết quả cũ | 2 ngày | [ ] |
| 2.7 | Import + comparison: nạp CSV thực nghiệm, map về tile/ô, đối chiếu dự đoán ↔ đo | **Import không bao giờ retrain**; ô không map được phải hiện rõ, không im lặng bỏ | 3 ngày | [ ] |
| 2.8 | Export mở rộng: CSV/JSON/bundle provenance theo run và theo project | Bundle chứa model id, nguồn, phiên bản, nhãn development | 1,5 ngày | [ ] |
| 2.9 | PostgreSQL 16 local + parity SQLite↔PG | Bộ test chạy xanh trên **cả hai** DB | 1,5 ngày | [ ] |
| 2.10 | Cổng R3 đúng: `P = σ(10.187 − 3.275·x)`, tier-2 `P = σ(8.457 − 1.911·x̂)`, trạng thái `measured_borderline`/`predicted_borderline` | Golden test khớp `run_r3.py`; bỏ hẳn so sánh sai `psi <= 4.0` | 1,5 ngày | [ ] |
| 2.11 | View phân tích: ma trận 28×20, **footprint track 1D (mới)**, ranking, inspector, shortlist, panel ưu tiên top-k | 532 ô + 28 WT; track tái tính khớp ma trận trong 1e-9; panel ưu tiên có nhãn "hồi cứu, development" **trước** số | 3 ngày | [ ] |
| 2.12 | Đổi model phục vụ sang LoRA-D *(phụ thuộc 1.13)* | Cần thêm `torch`+`transformers` vào backend (hiện chỉ có numpy) + đo lại latency + kích thước cài đặt; giữ npz làm mặc định bật/tắt bằng cấu hình | 2–4 ngày | [ ] |
| 2.13 | Kiểm thử: pytest + vitest + Playwright cho flow mới, axe, đối chiếu `system/test-plan.md` | Ghi **số case thực tế**, không trích số lịch sử 22/10 | 3 ngày | [ ] |
| 2.14 | Ảnh chụp + clip demo (cho `report/appendices/a-installation-user-guide.tex`) | Ảnh từ app thật với dữ liệu thật, không phải fixture | 0,5 ngày | [ ] |

**Tổng ≈ 26–30 ngày làm việc.** Đây là đường găng của toàn bộ luận văn.

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

| Tuần | Nhánh 1 | Máy CUDA | Nhánh 2 | Nhánh 3–4 |
| --- | --- | --- | --- | --- |
| T1 | 1.1–1.9 viết script | — | 2.1, 2.2 | — |
| T2 | 1.12 phân tích | **1.10, 1.11 chạy** | 2.3, 2.4 | — |
| T3 | 1.13, 1.14 | — | 2.5, 2.6 | khung chương |
| T4 | 1.15, 1.16, 1.17 | — | 2.7, 2.8 | — |
| T5 | — | — | 2.9, 2.10, 2.11 | — |
| T6 | 🚦 | — | 2.12, 2.13, 2.14 🚦 | — |
| T7 | — | — | sửa lỗi | 3.1–3.6 |
| T8 | — | — | — | 3.7, 3.8, 4.2–4.5 |

**≈ 8 tuần.** Phụ thuộc D-2 (ngày bảo vệ) để biết có vừa hay không.

| Rủi ro | Dự phòng |
| --- | --- |
| 8 tuần vượt deadline | Thứ tự cắt: 2.9 PostgreSQL → giữ SQLite + ghi `DEVIATIONS.md`; 2.7 → chỉ import, bỏ comparison; 2.12 → giữ npz, LoRA-D chỉ là candidate đã export; 2.5 → giới hạn số tile |
| Máy CUDA khác dừng giữa chừng | Đã có `STOP`/checkpoint 120 s/resume; `RUNBOOK.md` hướng dẫn chạy tiếp; **không** sửa `state.json` bằng tay |
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
