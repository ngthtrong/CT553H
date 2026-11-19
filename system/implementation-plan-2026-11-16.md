# Kế hoạch triển khai chi tiết — Nhánh 2: ứng dụng v0.2

Ngày lập **16/11/2026**. Tài liệu con của [plan.md](../plan.md) §5; tiến độ tổng
vẫn đánh dấu ở `plan.md`, còn đây là phân rã công việc chi tiết đến mức file,
requirement và test case.

Phạm vi lấy nguyên từ thiết kế đã duyệt ngày 29/10, **không tự thêm hay bớt**:
[README.md](README.md) §1, [srs.md](srs.md) (UC-01…10, FR-01…36, NFR-01…20),
[db-design.md](db-design.md) §11, [openapi.yaml](openapi.yaml) (operation có
`x-implementation-status: planned`), [api-spec.md](api-spec.md),
[ui-design.md](ui-design.md) §12, [test-plan.md](test-plan.md),
[Workspace UI v2](design/workspace-ui-v2/README.md). Chỗ nào kế hoạch này đề xuất
vượt thiết kế thì ghi rõ **[bổ sung đề xuất]**.

---

## 0. Định nghĩa hoàn thành nhánh 2

Nhánh 2 xong khi **tất cả** điều sau đúng và có bằng chứng đo được:

1. Cài sạch từ một bản clone mới, chuẩn bị dữ liệu tham chiếu, khởi động và chạy
   đủ **UC-01…10** trên một máy local (DEP-01).
2. Dừng/khởi động lại cùng instance: lịch sử, dataset và job đã lưu **phục hồi
   đúng** (DEP-02, HIST-02, BATCH-05).
3. Các nhóm test trong `test-plan.md` — UT, PB, RG, API, ETL, E2E, DOM, ANN,
   BATCH, IMP, HIST, NF, SEC, A11Y, DEP — đều có kết quả **chạy thật**, ghi số
   case thực tế. Không trích số lịch sử 22/10.
4. Thông số NFR được **đo và ghi lại** kèm cấu hình máy (OS, CPU, RAM, phiên bản).
   Ngưỡng trong SRS là *đề xuất*; trượt ngưỡng thì báo, không giấu.
5. `openapi.yaml` đổi `planned` → `implemented` cho đúng các operation đã làm;
   `DEVIATIONS.md` cập nhật mọi chỗ code lệch thiết kế.
6. Biên bản nghiệm thu `system/app/acceptance-<ngày>.{md,json}`.

Nhánh 2 **không** đổi model phục vụ trừ WP10, **không** đóng G2/G3, **không** gọi
so sánh với dữ liệu import là "independent validation" (D-8).

---

## 1. Hiện trạng đo được ngày 16/11/2026

| Hạng mục | Hiện có | Còn thiếu |
| --- | --- | --- |
| API | **13 path**: 9 baseline + `healthz` + 3 legacy `/v1/runs*` | **24 operation planned**: projects 5, analyses 5, jobs 6, datasets 5, comparisons 3 |
| CSDL | **11 bảng**, **1 migration** (`0001_initial_schema`) | **8 bảng**: `project`, `analysis_job`, `job_item`, `analysis_run`, `analysis_cell`, `import_dataset`, `import_observation`, `comparison` |
| Màn hình | 7 page, 18 component (single-tile) | **13 màn hình** theo `screen-map.json` v2; 14 component §12.5 |
| Model | `m3-ext4.0-platt-v1.npz`, backend **chỉ numpy** | — |
| Dữ liệu | `.data/dev.db` 453 MB (20.431 protein, 482.216 tile, 2,34 M ClinVar) | — |
| Test | 277 file test | Số pass hiện tại **chưa biết** — chưa chạy lại từ 22/10 |
| Công cụ FE | React 19.3, react-router 7.18, TanStack Query 5, d3-scale, MSW, openapi-typescript, Playwright + axe, Vitest | — |
| Môi trường | backend `.venv` Python 3.12 | `node` **không có** trong WSL; PostgreSQL **chưa từng chạy** |
| Khoa học | — | Cổng R3 sai estimator (`psi <= 4.0`), chưa có `borderline` |

---

## 2. Nguyên tắc kiến trúc

| # | Nguyên tắc | Lý do / nguồn |
| --- | --- | --- |
| A-1 | **Contract-first**: sửa `openapi.yaml` trước → `npm run gen:api` sinh type → mới viết code | D-12; tránh FE/BE lệch nhau |
| A-2 | Worker là **tiến trình riêng** (`python -m api.worker`) dùng **cùng** gói `degron_footprint` | §5 README: "local job worker using the same inference package" |
| A-3 | Hàng đợi **nằm trong CSDL** (lease trên `job_item`), **không** Celery/Redis | NFR-16: không cần cloud orchestration; ít thành phần phải cài |
| A-4 | Claim item: PostgreSQL `SELECT … FOR UPDATE SKIP LOCKED`; SQLite `BEGIN IMMEDIATE` | Một mã nguồn, hai backend |
| A-5 | `analysis_run` **bất biến**; "Run again" luôn tạo bản ghi mới | FR-32, D-13 |
| A-6 | Snapshot lưu **kèm** chú giải ClinVar/UniProt tại thời điểm chạy | §11 db-design: thay bản ClinVar đang dùng không được làm đổi kết quả cũ |
| A-7 | Không để chuỗi sinh học trong log, URL, `localStorage` | NFR-09, SEC-01 |
| A-8 | Polling bằng TanStack Query `refetchInterval` cho tiến độ job; **không** SSE/WebSocket | Đơn giản, đủ cho local; ít bề mặt lỗi |
| A-9 | Giữ runner kiểm tra độc lập với service | D-9; RG-01 |
| A-10 | Legacy `/v1/runs*`: giữ route để không vỡ test, ẩn khỏi UI, đánh dấu `deprecated` | D-7 |

---

## 3. Hệ thiết kế — dùng `ui-ux-pro-max` cùng Workspace UI v2

### 3.1 Cách chạy skill

```bash
# 1) Sinh và lưu hệ thiết kế (chỉ chạy khi chưa có MASTER.md; không dùng --force nếu chưa được duyệt)
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "scientific research data analysis dashboard" \
  --design-system --density 8 --variance 3 --motion 2 \
  --persist --tokens css -p "Degron Workspace" --output-dir system/design/ui-ux-pro-max-2026-11-16

# 2) Truy vấn bổ sung, mỗi truy vấn một mục đích
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "heatmap matrix legend" --domain chart
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "data table sorting pagination" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "error summary validation" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "progress indicator long task" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "file upload wizard steps" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "focus not obscured" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "rerender memo list" --stack react

# 3) Trước khi bàn giao: đọc references/pro-rules.md, chạy Pre-Delivery Checklist
```

### 3.2 Bảng hoà giải — đã chạy thử không persist ngày 16/11

| Đầu ra skill | Quyết định | Lý do |
| --- | --- | --- |
| Style **Minimalism & Swiss** | ✅ **Nhận** | Hợp công cụ chuyên môn dày dữ liệu; rủi ro a11y thấp |
| Density 8 (thang spacing 8–32 px) | ✅ **Nhận** | Ma trận 28×20 + bảng xếp hạng cần mật độ cao |
| Pattern **Enterprise Gateway** (Contact Sales, logo carousel, mega menu) | ❌ **Bỏ** | Mẫu landing page marketing, không phải ứng dụng local |
| Primary navy `#1E40AF` | ⚠️ **Xét lại** | Phải kiểm không trùng vùng màu của Viridis đảo |
| Accent hổ phách `#D97706` | ❌ **Bỏ** | **Trùng tông cam của thang PuOr** → nút UI có thể bị đọc thành "raw score dương". Giữ teal của v2 |
| Font Fira Code + Fira Sans **qua Google Fonts CDN** | ✅ **Nhận font, bỏ CDN** | App loopback, NFR-09 cấm gửi gì ra bên thứ ba → tự host `woff2` (giấy phép OFL). **16/11: Trọng chọn Fira Sans/Fira Code** thay Roboto của v2. **17/11: đổi lại Roboto/Roboto Mono** theo yêu cầu, tự host `@fontsource-variable` ([hồ sơ](design/ui-ux-pro-max-2026-11-17/README.md)) |
| GSAP scroll reveal | ❌ **Bỏ** | Thừa với công cụ phân tích; không thêm dependency; chỉ dùng CSS transition 150–250 ms + `prefers-reduced-motion` |
| Icon SVG (Lucide/Heroicons), không emoji | ✅ **Nhận** | Thêm `lucide-react` (giấy phép ISC) — dependency mới, ghi vào DEVIATIONS |
| Breakpoint 375/768/1024/1440 | ✅ **Gộp** với 360/768/1280 của v2 và NFR-12 → kiểm **360 / 768 / 1280 / 1440** | |
| Contrast 4.5:1, focus ring, keyboard | ✅ **Nhận** | Trùng NFR-11 |

**Quy tắc bất khả xâm phạm** (thang màu là bằng chứng khoa học, không phải thẩm mỹ):
Viridis đảo cho xác suất · PuOr cho raw score · hatch ô WT · cảnh báo đứng **trước**
điểm số trong DOM · nhãn sự kiện `P(ΔPSI ≥ 1.0)` cạnh mọi xác suất · không màu UI
nào được trùng vùng màu của hai thang dữ liệu.

---

## 4. Gói công việc (WP)

Ký hiệu: **BE** backend · **FE** frontend · **T** test. Mỗi WP xong khi đạt toàn bộ
cột tiêu chí và đã cập nhật tài liệu liên quan.

### WP0 — Nền móng và đo lại baseline · 1 ngày

| Việc | Chi tiết |
| --- | --- |
| [x] 0.1 Cài Node 24 trong WSL | Qua `nvm` trong thư mục người dùng (không `sudo`); khớp `engines` `>=24.22.1 <25` — 16/11: Node 24.22.3 |
| [x] 0.2 `npm ci` ở `frontend/` | Không nâng phiên bản dependency — 16/11: 447 gói; 7 moderate chỉ ở devDependencies, không `audit fix --force` |
| [x] 0.3 **Đo lại baseline trước khi sửa gì** | `make test lint typecheck contract`; `npm run typecheck lint test build`; `npm run e2e` |
| [x] 0.4 Ghi `system/app/rebaseline-2026-11-xx.json` | Số pass/fail/skip thật, phiên bản, thời gian. Đây là mốc so sánh cho mọi thay đổi sau — 16/11: [`rebaseline-2026-11-16.json`](app/rebaseline-2026-11-16.json): pytest 173/173 (cov 96%), Vitest 131/131, e2e mock 12/12, e2e real 11/11; đỏ sẵn: `check:api` (lệch thiết kế, WP3 xử lý) |
| [x] 0.5 Sao lưu `dev.db` | Tạo bản sao làm việc; **mọi migration chạy thử trên bản sao**, không đụng file gốc 453 MB — 16/11: `.data/backup/dev-2026-11-16.db` (chỉ đọc, sha256 `f7d36dfc…`) |

**Tiêu chí:** biết chính xác bao nhiêu test đang xanh/đỏ **trước** khi đụng code.

### WP1 — Hệ thiết kế và khung ứng dụng · 3 ngày · FE

| Việc | File / sản phẩm |
| --- | --- |
| [x] 1.1 Chạy skill có `--persist` (mục 3.1) | `system/design/ui-ux-pro-max-2026-11-16/design-system/degron-workspace/MASTER.md`, `tokens.css` |
| [x] 1.2 Hoà giải theo bảng 3.2, ghi quyết định | `system/design/ui-ux-pro-max-2026-11-16/README.md` |
| [x] 1.3 Gộp token vào cấu trúc 3 lớp của v2 (primitive → purpose → component) | `frontend/src/styles/tokens.css` |
| [x] 1.4 Tự host font `woff2` | `frontend/public/fonts/` + `@font-face` |
| [x] 1.5 Theme sáng/tối qua `data-theme` + `prefers-color-scheme` | |
| [x] 1.6 Primitive dùng chung: `Button`, `IconButton`, `Field`, `Select`, `Tabs`, `DataTable` (sort + paginate), `StatusPill`, `Banner`, `Dialog`, `Toast`/`LiveRegion`, `ProgressBar`, `EmptyState`, `Skeleton` | `frontend/src/components/ui/` |
| [x] 1.7 `AppShell` mới: sidebar 216 px — Projects · New analysis · Model · Sources (ui-design §12.1); không menu tài khoản | `components/AppShell.tsx` |
| [x] 1.8 Trang `/__styleguide` chỉ bật khi `import.meta.env.DEV` để rà mọi primitive ở cả hai theme | `pages/StyleguidePage.tsx` |

**Tiêu chí:** 0 axe violation trên `/__styleguide` ở cả hai theme và 4 breakpoint; contrast ≥ 4.5:1 cho chữ; bảng 3.2 đã chốt.

**Kết quả 16/11:** đạt — `frontend/e2e/design.spec.ts` 4/4; `tests/contrast.test.ts` 46/46. Hoà giải ghi ở [`design/ui-ux-pro-max-2026-11-16/README.md`](design/ui-ux-pro-max-2026-11-16/README.md). Primitive: `components/ui/` (Button, IconButton, Field, Select, Tabs, DataTable, StatusPill, Banner, Dialog, LiveRegion/Toast, ProgressBar, EmptyState, Skeleton). Shell sidebar mới; Vitest 152/152, e2e mock 16/16 sau khi đổi shell. **Chưa** restyle từng màn hình cũ — thuộc WP9.

### WP2 — Schema và migration · 2 ngày · BE

| Việc | Chi tiết |
| --- | --- |
| [x] 2.1 `0002_workspace.py` | 8 bảng đúng **tên và bất biến** ở `db-design.md` §11; FK chặn liên kết khác project; index theo §11 |
| [x] 2.2 `0003_domain_borderline.py` | Thêm `measured_borderline`, `predicted_borderline` vào ràng buộc trạng thái domain (`DEVIATIONS.md` §7) |
| [x] 2.3 SQLAlchemy model + repository | `backend/db/models.py`, `backend/api/repository.py` — 16/11: 8 model xong; hàm repository viết cùng router ở WP4–WP6 |
| [x] 2.4 Thư mục workspace cho file import | `.data/workspace/<project_id>/` — không bao giờ ghép đường dẫn từ input (NFR-08) — 16/11: `backend/api/workspace.py`, `Settings.workspace_dir` |
| [x] 2.5 Test migration | up/down trên DB rỗng **và** trên bản sao `dev.db`; bảng tham chiếu không đổi số dòng — 16/11: `tests/test_workspace_schema.py` 27 case (gồm PG 16 qua `DF_TEST_PG_URL`); pytest toàn bộ 199 pass + 1 skip; chi tiết `DEVIATIONS.md` §8 |

**Tiêu chí:** `alembic upgrade head` rồi `downgrade` sạch trên cả hai DB; số dòng `protein`/`tile`/`clinvar_variant` trước = sau.

### WP3 — Hợp đồng API · 1 ngày · BE + FE

| Việc | Chi tiết |
| --- | --- |
| [x] 3.1 Rà lại 24 operation planned trong `openapi.yaml` với `api-spec.md` | Mã lỗi, giới hạn NFR-07, phân trang ≤ 200 mục, tie-breaker ổn định |
| [x] 3.2 Đánh dấu legacy `/v1/runs*` là `deprecated` | A-10 — đã có sẵn trong contract (3 operation `deprecated: true`) |
| [x] 3.3 `npm run gen:api` | Sinh `frontend/src/api/schema.d.ts` — 16/11: `check:api` xanh (baseline đỏ) |
| [x] 3.4 Handler MSW cho mọi operation mới | Để FE làm song song khi BE chưa xong — 16/11: `frontend/mock/workspace.ts` (mock dùng chung cho dev:mock và MSW trong Vitest) + 11 test |

**Tiêu chí:** `make contract` PASS; `npm run typecheck` PASS với type mới.

**Kết quả 16/11:** sửa contract theo `app/DEVIATIONS.md` §9; `make contract`, `npm run typecheck lint check:api test build`, e2e mock 12/12 đều PASS; pytest 199 pass + 1 skip; Vitest 142/142.

### WP4 — Projects và lịch sử · 2 ngày · BE · UC-10

| Việc | Requirement → test |
| --- | --- |
| [x] 4.1 Router `projects.py`: list / create / get / rename / delete | FR-31 → HIST-01 |
| [x] 4.2 Router `analyses.py`: save snapshot / list / get / delete / export | FR-14, FR-22, FR-32 → HIST-02 |
| [x] 4.3 Snapshot bất biến kèm provenance **và** chú giải tại thời điểm chạy | A-5, A-6 |
| [x] 4.4 Xoá: tóm tắt phụ thuộc → xác nhận → xoá dòng sở hữu + file → **thử lại khi dọn file lỗi** | FR-33, NFR-10 → HIST-03 |
| [x] 4.5 Preview chưa lưu **không** xuất hiện trong CSDL/log | NFR-09 → HIST-01, SEC-01 |

**Tiêu chí:** lưu → khởi động lại API → mở lại đúng snapshot; đổi model/ClinVar đang dùng → snapshot cũ **không đổi**.

**Kết quả 16/11:** `routers/projects.py`, `workspace_store.py`, `snapshot.py`, `exports.py`; `tests/test_workspace_api.py` 23 case (HIST-01/02/03, gồm khởi động lại API, xoá ClinVar sau khi lưu, dọn file lỗi rồi thử lại). Contract: thêm `SavedAnalysisSummary`, `Project.deletion_pending`, 400 cho 24 operation (`app/DEVIATIONS.md` §9).

### WP5 — Job bền và worker · 4 ngày · BE · UC-08

| Việc | Requirement → test |
| --- | --- |
| [x] 5.1 Nhận input: danh sách peptide / FASTA nhiều bản ghi → ID ổn định; preview đếm hợp lệ/không hợp lệ/trùng | FR-24, FR-36 → BATCH-01 |
| [x] 5.2 Chế độ whole-protein: accession đã nạp hoặc một bản ghi FASTA → tile 28 AA bước 23; báo đoạn **không phủ** (kể cả hai đầu), cửa sổ không chấm được; **không** gộp ngữ cảnh chồng lấn | FR-25, FR-16 → BATCH-04 (độ dài 27/28/50/51) |
| [x] 5.3 Ghim model / calibrator / gate / source hash lúc submit | FR-27 → BATCH-02 |
| [x] 5.4 Worker `python -m api.worker`: claim `job_item` có lease (owner, expiry), heartbeat, ghi `analysis_run` theo từng item trong transaction | A-2, A-3, A-4 |
| [x] 5.5 Huỷ: cờ huỷ được kiểm giữa các item; item đã xong được giữ | FR-26 → BATCH-03 |
| [x] 5.6 Phục hồi: lease hết hạn được claim lại; item đã xong **không** tính lại; không nhân đôi run | FR-26 → BATCH-05 |
| [x] 5.7 Trạng thái job: pending → running → completed / partial / failed / cancelled | ui-design §12.5 |
| [x] 5.8 Log có cấu trúc: job ID, số lượng, trạng thái, thời lượng — **không** payload | NFR-19 |
| [x] 5.9 Giới hạn: 100 peptide hoặc 1 protein ≤ 10.000 residue (đề xuất NFR-07) | FR-36 → NF-04/05 |

**Tiêu chí:** kill worker giữa job → khởi động lại → job chạy tiếp và tổng đếm khớp; mọi tile thành công trong batch khớp chấm single-tile.

**Kết quả 16/11:** `jobs.py`, `worker.py` (`python -m api.worker`, `make dev-worker`, tuỳ chọn `DF_EMBEDDED_WORKER`), `routers/jobs.py`; `tests/test_jobs.py` 29 case gồm `SIGKILL` tiến trình worker thật giữa job 100 peptide rồi chạy lại → 100/100, 100 analysis, không trùng; ô của mọi tile trong job bằng chấm single-tile. Claim = compare-and-set `UPDATE` (+ `SKIP LOCKED` trên PG); kiểm 2 worker song song trên PG để WP8.

### WP6 — Import và so sánh · 3 ngày · BE · UC-05, UC-09

| Việc | Requirement → test |
| --- | --- |
| [x] 6.1 `previewImport`: CSV/TSV ≤ 10 MiB / 100.000 dòng → dataset `staged` + báo cáo kiểm từng dòng + SHA-256 file | FR-28, FR-36 → IMP-01 |
| [x] 6.2 Metadata bắt buộc: assay, endpoint, đơn vị, nguồn, replicate | FR-28 |
| [x] 6.3 Lỗi chặn → không cho commit; cảnh báo → phải xác nhận; preview hết hạn được báo rõ | FR-28, NFR-10 → IMP-02 |
| [x] 6.4 `commitDataset`: revision **bất biến**; file mới = revision mới, không ghi đè | IMP-02 |
| [x] 6.5 Căn hàng theo WT sequence + vị trí + đột biến; kiểm accession/release/residue WT khi có; giữ dòng thiếu/không khớp/trùng xung đột, **không** điền 0 | FR-29 → IMP-03 |
| [x] 6.6 So sánh: endpoint không tương thích → tách riêng; MAE/Spearman/residual chỉ trên cặp tương thích, kèm n và cách gộp replicate; lý do khi metric không xác định | FR-30, FR-17 → IMP-04 |
| [x] 6.7 An toàn: không thực thi nội dung, không ghép vào path/SQL, vô hiệu hoá công thức spreadsheet khi export | NFR-08 → SEC-02 |
| [x] 6.8 Import **không bao giờ** retrain, không đổi bảng tham chiếu | D-8, D-11 |

**Tiêu chí:** metric khớp **fixture tính tay**; import lỗi → bảng tham chiếu không đổi.

**Kết quả 16/11:** `importer.py` (multipart bằng thư viện chuẩn, không thêm dependency), `datasets.py`, `routers/datasets.py`; `tests/test_import.py` 16 case. Fixture tính tay độc lập với model: observed = predicted − d, d = [0,5; −1; 0,25; 2] → MAE = 0,9375 và residual = d (sai lệch < 1e-12); thứ tự đảo → Spearman = −1; mean/median trên 4 replicate. Import lỗi hoặc thành công đều giữ nguyên số dòng bảng tham chiếu.

### WP7 — Cổng R3, chú giải và export · 2,5 ngày · BE

| Việc | Requirement → test |
| --- | --- |
| [x] 7.1 Nạp gate model R3: tier-1 `P = σ(10.187 − 3.275·x)` (in ≤ 2.687 / out ≥ 3.110 / còn lại borderline); tier-2 `P = σ(8.457 − 1.911·x̂)` (3.700 / 4.426) | FR-09 → DOM-01, ETL-05 |
| [x] 7.2 **Bỏ hẳn** so sánh screen PSI với 4.0 | `DEVIATIONS.md` §7 |
| [x] 7.3 Golden test khớp `research/r3-domain-gate-2026-10-22/run_r3.py` | DOM-01 |
| [x] 7.4 ClinVar / UniProt / GPS: phân biệt *không có biến thể* · *không map được* · *nguồn không khả dụng* · *xung đột mapping* | FR-18, FR-35 → ANN-01 |
| [x] 7.5 Export analysis, manifest job nhiều trang, bảng so sánh — đủ mọi item, không chỉ trang đang xem | FR-34 → BATCH-06 |
| [x] 7.6 Attribution + disclaimer ClinVar trên view và export | NFR-14 → E2E-06 |

**Tiêu chí:** tỉ lệ tile ~26% in / 9% borderline / 65% out tái hiện được trên tile screen (theo `DEVIATIONS.md` §7).

**Kết quả 16/11:** ETL thật: 347.780 tile sàng tin cậy → **25,35% / 8,73% / 65,93%** (`app/.data/etl-report.json`, ghim trong `tests/test_regression.py::test_etl05_real_report`). Golden test so với `run_r3.feats` (`tests/test_gate.py`). 7.4: 5 trạng thái chú giải lưu trong snapshot; 7.5: export analysis(+comparison) và manifest job dạng stream. Chi tiết `app/DEVIATIONS.md` §7.

### WP8 — PostgreSQL 16 local · 2 ngày · BE

| Việc | Chi tiết |
| --- | --- |
| [x] 8.1 PostgreSQL 16 qua Docker (`postgres:16-alpine`, cùng image với `docker-compose.yml`) | 16/11: đổi từ `sudo apt` sang Docker; image đã tải, chỉ bind `127.0.0.1` |
| [x] 8.2 `DATABASE_URL` chọn backend; SQLite vẫn là mặc định dev/test | README §1 |
| [x] 8.3 `alembic upgrade head` từ baseline trên PG | DEP-01 |
| [x] 8.4 Nạp ETL tham chiếu vào PG, **đo thời gian** (2,34 M dòng ClinVar) | |
| [x] 8.5 Tham số hoá pytest chạy trên **cả hai** backend | |
| [x] 8.6 Kiểm đường claim `SKIP LOCKED` với 2 worker song song | A-4 |

**Tiêu chí:** toàn bộ test backend xanh trên SQLite **và** PostgreSQL.

**Kết quả 16/11:** đạt — SQLite 285 pass + 1 skip; PostgreSQL 16.16 (Docker, `make pg-up`, `make test-pg`) 273 pass + 12 skip (`sqlite_only`/`realdata`). Database test tạo bằng `CREATE DATABASE … TEMPLATE`. ETL thật vào PG: 465,6 s, 482.216 tile, 2.338.863 ClinVar, cùng số trạng thái domain với SQLite. 2 worker song song: 60/60 item, không trùng (cả hai backend).

### WP9 — 13 màn hình · 8 ngày · FE

Theo `design/workspace-ui-v2/screen-map.json`. Mỗi màn hình phải có đủ trạng thái
loading / empty / error / partial, đi được bằng bàn phím, có thông báo
`aria-live` lịch sự cho tiến độ.

| # | Màn hình | Route | UC | Component chính | Ngày |
| --- | --- | --- | --- | --- | --- |
| [x] 9.1 | Projects | `/projects` | 10 | `ProjectList`, thẻ project (tên, cập nhật, số analysis/job/dataset) | 0,5 |
| [x] 9.2 | Project workspace / history | `/projects/:id` | 10 | `ProjectWorkspace`, 3 tab History · Jobs · Datasets, `HistoryTable`, `DeleteConfirmation` | 1 |
| [x] 9.3 | New analysis (single / batch / protein) | `/new` | 01, 08 | `SequenceInput`, `BatchInput`, preview giới hạn + ước lượng công việc | 1 |
| [x] 9.4 | Protein tile picker | `/protein/:acc` | 04 | `ProteinSearch`, `TileMap`, `ProteinCoverage` | 0,5 |
| [x] 9.5 | Matrix / ranking / shortlist | `/result` | 01, 02 | `Heatmap` 28×20, `RankTable`, inspector cạnh (không modal), shortlist, top 10% | 1,5 |
| [x] 9.5b | **Footprint track 1D** dưới ma trận, dùng chung trục vị trí | trong `/result` | 01 | `FootprintTrack` **[bổ sung đề xuất]** — chưa có trong `ui-design.md`, cần bổ sung tài liệu | 0,5 |
| [x] 9.6 | Saved snapshot / rerun / export | `/analyses/:id` | 03, 10 | `SaveAnalysisDialog`, `ExportMenu`, nút "Run again" tạo bản ghi mới | 0,5 |
| [x] 9.7 | Comparison | tab trong result | 05 | `ComparisonPanel`: dự đoán · đo · residual · đơn vị · n · lý do metric không xác định | 1 |
| [x] 9.8 | ClinVar / annotations | tab trong result | 06 | `AnnotationStatus` 4 trạng thái tách biệt | 0,5 |
| [x] 9.9 | Job progress / cancel / manifest | `/jobs/:id` | 08, 03 | `JobProgress`, `JobItemTable` phân trang, mở ma trận từng tile theo yêu cầu | 1 |
| [x] 9.10 | Import / validation / commit | `/import` | 09 | `ImportWizard`, `ValidationReport`, câu *"comparison only; not used to retrain the model"* | 1 |
| [x] 9.11 | Dataset / deletion | `/datasets/:id` | 09, 10 | `DatasetList`, phân biệt rõ `staged` với `committed` | 0,5 |
| [x] 9.12 | Model & evidence · Data & sources | `/model`, `/sources` | 07 | Restyle `ModelCardPage`, `AboutPage` | 0,5 |

**Tiêu chí:** mỗi màn hình có ít nhất một test Vitest + một luồng Playwright; 0 axe violation; không chuỗi sinh học nào lọt vào URL hay `localStorage`.

**Kết quả 17/11:** đạt.
- Trang mới: `ProjectsPage`, `ProjectPage`, `InputPage` (3 chế độ), `JobPage`, `AnalysisPage` (tab Ma trận · So sánh · Chú giải), `ImportPages` (`ImportPage`, `DatasetPage`).
- Component mới: `BatchInput`, `ProteinCoverage`, `JobItemTable`, `SaveAnalysisDialog`, `ComparisonPanel`, `AnnotationStatus`, `DeleteConfirmation`, `FootprintTrack` (đã bổ sung vào `ui-design.md` §12.4b).
- 9.4 Tile picker và 9.12 Model/Sources giữ component cũ, dùng token và shell mới.
- Test: `frontend/tests/workspace-screens.test.tsx` 18 case (gồm footprint khớp ma trận < 1e-9); `e2e/workspace.spec.ts` 8 luồng (UC-01/03/05/08/09/10 + axe 2 theme); e2e backend thật 12/12, gồm luồng workspace với worker nhúng; log API không chứa chuỗi sinh học.
- Tổng: Vitest 170/170, e2e mock 24/24.
- Giới hạn: jsdom gửi `File` trong `FormData` thành rỗng, nên bước commit import chỉ kiểm ở trình duyệt thật.

### WP10 — Đổi model phục vụ sang LoRA-D · 3 ngày · BE · *phụ thuộc nhánh 1 mục 1.13*

| Việc | Chi tiết |
| --- | --- |
| [x] 10.1 Loại model mới `torch-lora` trong registry | FR-22: snapshot cũ vẫn gắn model gốc — 17/11: kind `torch_lora`, `degron_footprint/lora.py`; ETL đăng ký frozen, không mặc định |
| [x] 10.2 Dependency tách riêng `requirements-lora.txt` (`torch` CPU, `transformers`) | Cài mặc định vẫn nhẹ; npz vẫn chạy khi không cài — 17/11: image Docker `WITH_LORA=0` 399 MB / `=1` 1,77 GB; thiếu torch → LoRA-D báo không nạp, healthz vẫn `ok` |
| [x] 10.3 Nạp lười (lazy load), kiểm hash trước khi phục vụ | NFR-06 → UT-09 — kiểm SHA-256 mọi file bundle lúc khởi động, digest learned state từng seed lúc dựng mạng (request đầu) |
| [x] 10.4 Parity với output refit của nhánh 1 | NFR-04 → RG-01 — `app/tests/results/lora-bundle.json`: CUDA→CPU 3,0e-6; serving↔research 0,0 trên 2 tile; API trong Docker 0,0 (`latency-lora.json`) |
| [x] 10.5 **Đo** latency CPU cho 532 biến thể/tile, RAM, kích thước cài đặt | NFR-01 **không đạt**: p95 39,1 s/tile (Docker, 4 luồng), RAM container 514 MiB, image 1,77 GB — `app/tests/results/latency-lora.json` |
| [x] 10.6 Cờ cấu hình chọn model mặc định; npz là mặc định cho đến khi có quyết định serving riêng | `DF_DEFAULT_MODEL_ID` (rỗng = npz); `/healthz`, `/v1/models` báo mặc định thực tế; `development_not_gate_closure` |

**Kết quả WP10 (17/11):** [`app/backend/LORA.md`](app/backend/LORA.md), [`app/docker-validation-2026-11-17.md`](app/docker-validation-2026-11-17.md). Chưa có quyết định đổi model phục vụ; LoRA-D chỉ bật khi được chọn.

**Tiêu chí:** cả hai model chạy được; chuyển qua lại bằng cấu hình; số đo latency/RAM được ghi.

### WP11 — Kiểm thử và nghiệm thu · 3 ngày · T

| Việc | Test ID |
| --- | --- |
| [x] 11.1 E2E từng UC-01…10, luồng chính và luồng lỗi | E2E-01…12 |
| [x] 11.2 Ma trận trình duyệt Chromium / Firefox / WebKit × 360 / 768 / 1280 / 1440 | NFR-12 |
| [~] 11.3 axe + **kiểm tay** bàn phím hoàn thành UC-01…10, tín hiệu không dựa màu | A11Y-01…04 — 17/11: axe + luồng bàn phím tự động xong; **kiểm tay do người** còn mở |
| [x] 11.4 Hiệu năng có ghi cấu hình máy | NF-01…07 |
| [x] 11.5 Canary chuỗi/quan sát không xuất hiện trong log/URL | SEC-01 |
| [x] 11.6 Bind loopback, kiểm origin/content-type, header bảo mật | SEC-03 |
| [x] 11.7 `npm audit` + `pip-audit` | SEC-05 |
| [x] 11.8 Cài sạch từ clone mới theo hướng dẫn | DEP-01 |
| [x] 11.9 Dừng/khởi động lại, phục hồi | DEP-02 |
| [x] 11.10 Coverage backend (mục tiêu đề xuất ≥ 85%) | NFR-17 |
| [x] 11.11 Cập nhật `openapi.yaml`, `DEVIATIONS.md`, `system/README.md` §4, `ui-design.md` (footprint track) | |
| [x] 11.12 Biên bản `system/app/acceptance-<ngày>.{md,json}` | |

**Kết quả WP11 (17/11):** biên bản [`app/acceptance-2026-11-17.md`](app/acceptance-2026-11-17.md) / `.json`. Sửa 8 lỗi phát hiện trong nghiệm thu (gồm index ClinVar `0004`, race worker/huỷ, chặn ghi cross-site 403/415). Còn mở: kiểm tay a11y, chạy lại PG sau thay đổi 17/11.

### WP12 — Ảnh chụp và hướng dẫn · 1 ngày

| Việc | Chi tiết |
| --- | --- |
| [x] 12.1 Ảnh chụp từ app thật, dữ liệu thật, cả hai theme | Cho `report/appendices/a-installation-user-guide.tex` (đang `[PENDING]` dòng 36, 49) |
| [x] 12.2 Kịch bản demo 3–5 phút ~~+ clip dự phòng~~ | Cho slide và buổi bảo vệ |
| [x] 12.3 Hướng dẫn cài đặt/chạy local | Nguồn cho Phụ lục A |


**Kết quả 17/11:** 14 ảnh × 2 theme từ app thật, dữ liệu thật (`app/docs/screenshots/`; ảnh so sánh dùng dataset minh hoạ có ghi chú); kịch bản [`app/DEMO.md`](app/DEMO.md) (clip dự phòng bỏ theo yêu cầu của Trọng 17/11); hướng dẫn cài [`app/INSTALL.md`](app/INSTALL.md) (nguồn cho Phụ lục A).
---

## 5. Ma trận truy vết UC → WP → test

| UC | Nội dung | WP | Test chính |
| --- | --- | --- | --- |
| UC-01 | Dự đoán ma trận | 7, 9.3, 9.5, 9.5b | PB-01, RG-01, E2E-01, DOM-01 |
| UC-02 | Xếp hạng | 9.5 | UT-04, E2E-02 |
| UC-03 | Export có provenance | 4.2, 7.5, 9.6 | RG-02, API-30/31, E2E-03, E2E-10 |
| UC-04 | Chọn protein / tile | 5.2, 9.4 | UT-05, API-20/21, E2E-04 |
| UC-05 | So sánh với dữ liệu đo | 6.5, 6.6, 9.7 | IMP-03, IMP-04, E2E-05 |
| UC-06 | ClinVar / chú giải | 7.4, 7.6, 9.8 | ANN-01, E2E-06 |
| UC-07 | Model / nguồn | 9.12 | API-24/25, E2E-07 |
| UC-08 | Batch / whole protein | 5, 9.3, 9.9 | BATCH-01…06, NF-07 |
| UC-09 | Import thực nghiệm | 6, 9.10, 9.11 | IMP-01, IMP-02 |
| UC-10 | Projects / lịch sử | 4, 9.1, 9.2, 9.6 | HIST-01…03, DEP-02 |

---

## 6. Thứ tự và lịch

```
WP0 ──► WP2 ──► WP3 ──┬─► WP4 ──► WP5 ──► WP6 ──► WP7 ──► WP8 ──┐
                      │                                         ├─► WP11 ──► WP12
WP1 ──────────────────┴─► WP9 (dùng MSW khi BE chưa xong) ──────┘
                                         WP10 (chờ nhánh 1 mục 1.13) ──┘
```

| Tuần | Công việc | Mốc kiểm |
| --- | --- | --- |
| T1 | WP0, WP1, WP2 | Baseline đo lại; hệ thiết kế chốt; migration chạy trên bản sao `dev.db` |
| T2 | WP3, WP4, bắt đầu WP5 | Contract PASS; projects/history lưu và mở lại được |
| T3 | WP5, WP9.1–9.4 | Kill worker → job chạy tiếp, không nhân đôi |
| T4 | WP6, WP9.5–9.6 | Metric so sánh khớp fixture tính tay |
| T5 | WP7, WP9.7–9.12 | Golden test R3 PASS; đủ 13 màn hình |
| T6 | WP8, WP10 | Test xanh trên SQLite **và** PG; số đo LoRA-D |
| T7 | WP11, WP12 | Biên bản nghiệm thu; ảnh chụp sẵn sàng → **cổng 🚦** |

**Tổng ≈ 35 ngày làm việc ≈ 7 tuần.** Cao hơn ước lượng 26–30 ngày trong
`plan.md` vì phân rã chi tiết lộ thêm WP0 (đo lại baseline), WP3 (contract),
WP8 (PG) và kiểm thử trên 3 trình duyệt × 4 breakpoint.

---

## 7. Quy trình cho mỗi WP

1. Đọc lại đoạn thiết kế tương ứng (SRS/api-spec/db-design/ui-design).
2. Sửa contract trước nếu WP đụng API (A-1).
3. Viết test cùng lúc với code; mỗi FR có ít nhất một test có ID từ `test-plan.md`.
4. Chạy `make test lint typecheck contract` và `npm run typecheck lint test`.
5. So với baseline WP0: **không được làm đỏ** test đang xanh mà không giải thích.
6. Cập nhật `DEVIATIONS.md` nếu lệch thiết kế.
7. Đánh dấu ô trong tài liệu này **và** mục tương ứng trong `plan.md`, kèm ngày + bằng chứng.
8. Không commit/push khi chưa được yêu cầu.

---

## 8. Rủi ro và phương án cắt

| Rủi ro | Dấu hiệu sớm | Phương án |
| --- | --- | --- |
| 7 tuần vượt deadline | Trễ quá 3 ngày ở T3 | Cắt theo thứ tự: WP8 (giữ SQLite, ghi DEVIATIONS) → WP10 (npz, LoRA-D chỉ là candidate) → 6.6 comparison (chỉ import + xem) → 5.2 giới hạn số tile |
| Job runner bền sai ở trường hợp biên | BATCH-05 đỏ | Làm WP5 sớm; test kill/restart ngay khi viết xong claim/lease |
| Migration làm hỏng `dev.db` | Số dòng tham chiếu đổi | Chỉ chạy trên bản sao (0.5); đối chiếu số dòng trong test 2.5 |
| PostgreSQL cần `sudo` | Không được phép cài | Dừng WP8, xin phép; nếu không thì giữ SQLite và ghi giới hạn |
| Baseline WP0 đã có test đỏ | 0.3 | Ghi rõ, không sửa lan man; chỉ sửa khi đụng tới vùng đó |
| Đổi UI làm vỡ hàng loạt test | Vitest đỏ hàng loạt | Giữ `data-testid` và thứ tự DOM (cảnh báo trước điểm số); đổi từng màn hình |
| Skill đề xuất màu đè thang dữ liệu | Bảng 3.2 | Quy tắc bất khả xâm phạm mục 3.2 |
| LoRA-D CPU quá chậm cho NFR-01 | 10.5 | Ghi số thật; giữ npz mặc định; LoRA-D bật bằng cấu hình |

---

## 9. Giả định cần xác nhận

| # | Giả định | Ảnh hưởng nếu sai |
| --- | --- | --- |
| G-1 | Được cài Node 24 bằng `nvm` trong thư mục người dùng | WP0 phải đổi cách cài |
| G-2 | ~~Được cài PostgreSQL 16 bằng `sudo apt` trong WSL~~ → **đã giải quyết 16/11**: dùng Docker | — |
| G-3 | Được thêm dependency `lucide-react` và font tự host (OFL) | WP1 dùng SVG tự vẽ |
| G-4 | Footprint track 1D được chấp nhận là bổ sung vào `ui-design.md` | Bỏ 9.5b |
| G-5 | Ngưỡng NFR trong SRS chỉ là đề xuất, được phép báo trượt | Phải tối ưu thêm trước nghiệm thu |
