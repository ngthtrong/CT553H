# Kế hoạch hoàn thiện hệ thống Degron Footprint — nhóm 1 đến 5

Tạo ngày **18/11/2026** theo yêu cầu của Trọng, từ bản phân tích "tính năng để thành hệ thống hoàn thiện" ngày 17/11.
Đây là **biên bản todo** riêng cho phần mở rộng ứng dụng (`system/app/`), bổ sung cho [plan.md](plan.md) (nhánh 2 phạm vi
v0.2 đã xong). Đánh dấu `[x]` chỉ khi đạt **toàn bộ** tiêu chí nghiệm thu, kèm ngày và đường dẫn bằng chứng; mục bị cắt
ghi `[-]` kèm lý do, không xoá dòng. Thay đổi phạm vi ghi vào [§10 Nhật ký](#10-nhật-ký-thay-đổi).

Nhóm 6 trong bản phân tích (tài khoản/đa người dùng, triển khai công khai, suy luận bệnh hoặc E3 cụ thể, tự train lại)
và tính năng đa đột biến được lưu ở [§9 Hướng phát triển tương lai](#9-hướng-phát-triển-tương-lai); chỉ xem xét **sau
khi** hoàn thành nhóm 1–5.

---

## 0. Ràng buộc áp dụng cho mọi gói việc

Kế thừa [CLAUDE.md](CLAUDE.md), [plan.md](plan.md), [system/srs.md](system/srs.md); không mục nào dưới đây được vi phạm.

| # | Ràng buộc | Hệ quả khi làm |
| --- | --- | --- |
| R-1 | Trạng thái khoa học giữ `development_not_gate_closure`; không đóng G3; mọi kết quả mang nhãn domain/event/evidence (NFR-15) | Màn hình mới hiển thị số phải có nhãn giới hạn **trước** con số trong DOM |
| R-2 | Thang màu khoa học cố định: Viridis đảo (xác suất), PuOr (raw score), hatch ô WT | Thang mới (phân tán seed, chênh lệch model) phải chốt trong `system/ui-design.md` và kiểm tương phản |
| R-3 | NFR-09: không gửi chuỗi/quan sát ra ngoài; không chuỗi trong log/URL; chỉ lưu khi người dùng chủ động | Truy cập dịch vụ ngoài là **opt-in**, chỉ gửi accession; cache bền phải bật bằng cấu hình |
| R-4 | Contract-first (A-1): sửa `system/openapi.yaml` → `npm run gen:api` → viết code | Mỗi endpoint/trường mới có schema và test contract |
| R-5 | Migration có phiên bản, up/down sạch trên SQLite **và** PostgreSQL 16 | Migration mới đánh số từ `0005`; chạy `make docker-test` cả hai backend |
| R-6 | Dữ liệu mới qua cổng giấy phép ETL (ETL-03), ghim SHA-256 trong `etl/sources.yaml`, ghi `data/README.md` cùng phiên | Nguồn chưa rõ giấy phép thì **không nạp** |
| R-7 | Không tự train lại; dữ liệu nhập không vào benchmark (SRS §1.3) | Tính năng gợi ý chỉ xếp hạng, không cập nhật model |
| R-8 | Đổi model phục vụ mặc định cần biên bản (mục 4.3); không suy ra từ thứ hạng | Không tự đổi `DF_DEFAULT_MODEL_ID` trong code hay test |
| R-9 | Docker là cấu hình chính: mỗi gói việc kết thúc bằng build lại image, `make docker-test` (PG + SQLite), e2e mock, `make docker-e2e` với **cả hai** model mặc định | Ghi số case thực tế, không trích số cũ |
| R-10 | Mỗi lệch khỏi thiết kế ghi `system/app/DEVIATIONS.md`; mỗi đợt kết thúc bằng biên bản **mới** `system/app/acceptance-system-<ngày>.{md,json}` | Không ghi đè biên bản cũ |

Quy ước ID test mới (bổ sung `system/test-plan.md` khi làm): `MSEL-` chọn model, `CACHE-`, `UNC-` phân tán seed,
`PERF-`, `VIZ-`, `CMP-`, `DATA-`, `CLI-`, `RPT-`, `OPS-`, `UX-`; `ANN-`, `BATCH-`, `DOM-` tiếp số hiện có.

---

## 1. Tổng quan và thứ tự

| Đợt | Mục | Ước lượng | Mốc | Trạng thái 19/11 |
| --- | --- | --- | --- | --- |
| **Đợt 1 — trước bảo vệ** | 1.1, 1.2, 1.3, 1.5, 1.7, 2.1, 2.3, 3.5, 4.1, 4.3, 4.6 | ≈ 19,5 ngày (~4 tuần) | Ứng dụng đủ để trình bày; ảnh Phụ lục A chụp lại | 10/11 xong; dở 4.6 |
| **Đợt 2** | 1.4, 2.2, 2.6, 3.3, 3.4, 4.2, 4.5, 5.1, 5.4 | ≈ 21 ngày (~4 tuần) | Hiệu năng LoRA-D, so sánh model, công cụ dòng lệnh | 9/9 xong |
| **Đợt 3** | 1.6 (sau quyết định), 2.4, 2.5, 3.1, 3.2, 3.6, 4.4, 5.2, 5.3 | ≈ 28 ngày (~6 tuần) | Chú giải mở rộng, cấu trúc 3D, song ngữ, gói dự án | 2/9 xong; dở 1.6; chưa 2.4, 2.5, 3.1, 3.2, 3.6, 5.3 |
| Tích hợp, sửa lỗi, nghiệm thu (≈ 10 %) | — | ≈ 7 ngày | `acceptance-system-<ngày>` mỗi đợt | 3 biên bản `acceptance-system-2026-11-18{,b,c}` |

**Tổng ≈ 75 ngày làm việc (~15 tuần).** Phụ thuộc D-2 (ngày bảo vệ, [plan.md](plan.md) §1): đợt 1 cạnh tranh thời gian
với nhánh 3 (báo cáo) và nhánh 4 (slide). Nếu deadline gần thì **chỉ làm đợt 1**, đợt 2–3 đưa vào phần "Hướng phát
triển" của Kết luận.

Phụ thuộc chính:

```text
1.1 chọn model ──┬─> 2.2 so sánh model ──> 2.6 gợi ý thí nghiệm
1.3 phân tán seed ┘
2.3 biểu đồ so sánh ──> 4.4 theo dõi đồng thuận
1.2 cache ──> 1.4 tăng tốc (đo trước/sau) ──> 4.5 nhiều worker
4.3 quy trình phục vụ ──> 1.6 cổng miền theo model (chỉ khi được duyệt)
3.5 báo cáo + 4.6 ảnh/kiểm tay ──> Phụ lục A, slide
```

---

## 2. Nhóm 1 — Lấp khoảng trống của hệ thống hiện tại

### 1.1 Bộ chọn model trên giao diện · 2 ngày · FE+BE · đợt 1 — ✅ xong 18/11

Hiện trạng: API nhận `model_id`, giao diện không gửi; đổi model phải sửa `.env` và khởi động lại.

| Việc | Chi tiết |
| --- | --- |
| BE | `GET /v1/models` thêm `serving` (bool), `not_serving_reason`, `expected_tile_seconds` (trung bình trượt đo trong tiến trình; `null` khi chưa có mẫu) |
| Contract | Sửa `openapi.yaml` (`ModelSummary`), chạy `npm run gen:api` |
| FE | Ô chọn model ở New analysis (cả 3 chế độ) và nút "Chạy lại với model khác" ở trang kết quả — tạo phân tích **mới** (A-5). Lựa chọn giữ trong query `?model=` (chỉ id). Model không phục vụ hiện ra nhưng bị vô hiệu kèm lý do |
| FE | Hộp xác nhận khi model chậm: "≈ N tile × M s ≈ T phút" trước khi gửi job |
| FE | Route `/model/:id` cho model card từng model; `/model` vẫn là model mặc định |
| Test | `MSEL-01` API trả `serving`; `MSEL-02` e2e mock chọn model → provenance đổi; `MSEL-03` model không phục vụ không chọn được; `MSEL-04` e2e real với cả hai model |
| Nghiệm thu | Chạy một tile bằng cả hai model từ giao diện, không sửa `.env`; snapshot lưu đúng model đã chọn |

### 1.2 Cache kết quả dự đoán · 1,5 ngày · BE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| Khoá | `sha256(chuỗi · model_id · weights_sha256 · calibrator · CODE_VERSION)`; **chỉ cache điểm của model**, không cache domain/cảnh báo (phụ thuộc CSDL tham chiếu) |
| Lưu trữ | Mặc định LRU trong RAM mỗi tiến trình (`DF_PREDICTION_CACHE=memory`, có giới hạn số mục). Cache trên đĩa chỉ khi đặt `DF_PREDICTION_CACHE=disk`, ghi rõ trong INSTALL và DEVIATIONS vì nó lưu chuỗi ngầm (R-3, NFR-10) |
| Quan sát | Đếm hit/miss trong log có cấu trúc (không chuỗi) và trong trang quản trị 4.2 |
| Test | `CACHE-01` kết quả cache **bằng bit** kết quả tính mới (NFR-05); `CACHE-02` đổi model/hash/calibrator → miss; `CACHE-03` không chuỗi trong log; `CACHE-04` mặc định không ghi đĩa |
| Nghiệm thu | Mở lại hoặc xuất lại cùng tile LoRA-D lần hai < 1 s; số đo ghi vào `tests/results/` |

### 1.3 Hiển thị độ phân tán giữa 3 seed của LoRA-D · 2 ngày · BE+FE+DB · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `TilePrediction` thêm `score_seed_sd` (độ lệch chuẩn ddof = 0 của 3 điểm thô, ghi rõ định nghĩa); `null` với model không có seed |
| Contract/DB | Trường tuỳ chọn trong `cells`; migration `0005` thêm cột nullable; CSV/JSON export thêm cột, giữ 9 cột gốc (FR-12) đứng trước |
| FE | Chế độ xem thứ ba "Seed spread" (chỉ hiện khi có dữ liệu), thang tuần tự **riêng** (đề xuất đơn sắc xám–xanh; chốt trong `ui-design.md`, R-2); inspector hiện khoảng min–max của 3 seed |
| Nhãn | "Độ phân tán giữa 3 seed huấn luyện — không phải khoảng tin cậy, không phải sai số dự đoán", đặt trước số |
| Test | `UNC-01` SD khớp chính xác `parity-fixture.npz` (mảng per-seed); `UNC-02` npz trả `null` và UI ẩn chế độ; `UNC-03` export có cột; `UNC-04` axe hai theme |
| Nghiệm thu | Snapshot cũ (không có SD) vẫn mở được (FR-22) |

### 1.4 Tăng tốc LoRA-D · 3 ngày · BE · đợt 2 · phụ thuộc 1.2 — ✅ xong 18/11

| Bước | Chi tiết | Quy tắc |
| --- | --- | --- |
| a | Đo từng phần một tile (tokenize, forward, head); thử batch 128/256, số luồng, `torch.inference_mode`, tính WT một lần dùng chung cho các seed | Không đổi số: parity 0,0 với fixture |
| b | Gộp LoRA vào trọng số (`W + α/r·BA`) lúc nạp | Parity ≤ 1e-5 với fixture **và** với CUDA → giữ nguyên model id; vượt ngưỡng → phải là model id mới |
| c | Tuỳ chọn ONNX Runtime FP32 trong `requirements-lora.txt` | Như b; ghi lại kích thước image và RAM |
| d | Tuỳ chọn GPU (image CUDA, chỉ máy có GPU) | Như b; không bắt buộc |
| — | **Không** lượng tử hoá int8 ở kế hoạch này: đó là model khác, phải đánh giá lại trên T | Muốn làm thì chuyển sang §9 |
| Test | `PERF-01` p50/p95 trước–sau trên cùng máy, cùng `measure_latency_lora.py`; `PERF-02` parity sau mỗi bước |
| Nghiệm thu | Ghi số thật kể cả khi không đạt. Mục tiêu **đề xuất** p95 ≤ 15 s/tile (CPU 4 luồng); NFR-01 (300 ms) vẫn ghi là không đạt nếu không đạt |

### 1.5 Cảnh báo `TRAINING_PEPTIDE` cho chuỗi gõ tay với model npz · 0,5 ngày · BE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `RidgePlattModel` nhận `training_sequences` = tập trình tự tile của 176 peptide train (đọc từ CSDL khi nạp registry); `Predictor` đã dùng tập riêng của từng model từ 17/11 |
| Test | Chuỗi gõ tay trùng tile train → có cảnh báo với **cả hai** model; chuỗi ngoài tập → không có |
| Ghi | DEVIATIONS: hành vi cảnh báo thay đổi cho đầu vào gõ tay |

### 1.6 Cổng miền theo từng model · 1 ngày chuẩn bị + **chờ quyết định** · đợt 3 — ◐ một phần

Hiện trạng: LoRA-D huấn luyện trên mọi PSI(WT) (arm D) nhưng vẫn đi qua cổng R3 vốn dành cho miền PSI ≤ 4. Bằng chứng
hiện có **không ủng hộ** việc nới cổng: ở tầng PSI(WT) > 5, dự đoán zero có MAE thấp hơn LoRA-D
(`research/lora-refit-transfer-2026-11-16/results.json`, `metrics.*.strata.gt5`).

| Việc | Chi tiết |
| --- | --- |
| Chuẩn bị | Biên bản đề xuất `research/.../gate-policy-proposal-<ngày>.md`: số liệu theo tầng PSI, hệ quả với người dùng, các phương án (giữ nguyên / cảnh báo mạnh hơn / chính sách riêng theo model) |
| Quyết định | Trọng và GVHD; **không triển khai** khi chưa có biên bản |
| Nếu được duyệt | `gate_policy` gắn theo model trong registry, mặc định là R3 hiện tại; thêm test `DOM-` cho từng chính sách |

### 1.7 Thông báo và ước lượng thời gian job · 1 ngày · FE+BE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | Job trả `eta_seconds` tính từ thời lượng trung bình mỗi item đã xong (worker đã ghi `ms`); `null` khi chưa đủ mẫu |
| FE | Trang Job hiện ETA; tiêu đề tab mang tiến độ; thông báo trình duyệt **opt-in** khi job xong (Notification API cục bộ, không dịch vụ đẩy) |
| Test | `BATCH-` mới: ETA hợp lệ; chỉ thông báo khi người dùng đã cho phép; nội dung thông báo không chứa chuỗi |

---

## 3. Nhóm 2 — Phân tích và trực quan hoá khoa học

### 2.1 Footprint cấp protein · 3 ngày · BE+FE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `GET /v1/jobs/{id}/footprint`: với job protein đã xong, trả giá trị theo vị trí protein (1-based) cho **từng tile riêng** — mỗi vị trí là trung bình 19 thay thế tại đó (cùng định nghĩa với footprint track của tile), kèm trạng thái miền của tile và cờ peptide train |
| Quy tắc | **Không lấy trung bình vùng chồng lấn** (tile bước 23, chồng 5 residue): vẽ thành các làn xen kẽ; vùng không phủ hiện rõ |
| FE | Biểu đồ dọc theo protein trên trang Job: các làn tile, dải trạng thái miền bên dưới, trục toạ độ protein; bấm vào một tile mở phân tích tile đó; có bảng thay thế cho màn hẹp và trình đọc màn hình |
| Nhãn | "Mỗi tile được chấm độc lập trong ngữ cảnh 28 residue; đây không phải kiểu hình của cả protein" (SRS §1.2) |
| Test | `VIZ-01` giá trị bằng tính lại từ ô của từng tile (< 1e-9); `VIZ-02` không có điểm trộn ở vùng chồng lấn; `VIZ-03` e2e + axe; `VIZ-04` ở 360 px không cuộn ngang trang |

### 2.2 So sánh hai phân tích / hai model · 3 ngày · BE+FE · đợt 2 · phụ thuộc 1.1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `POST /v1/analyses/compare` nhận hai phân tích trên cùng chuỗi tile: trả Spearman, Pearson, chênh lệch tuyệt đối trung bình, độ trùng top-k (k = 54, Jaccard) và danh sách ô bất đồng lớn nhất; lưu được thành một bản so sánh trong dự án (bảng mới, migration) |
| FE | Màn so sánh: scatter điểm A–B, heatmap chênh lệch (thang phân kỳ riêng, chốt trong `ui-design.md`), bảng top bất đồng; nút "So sánh với model khác" từ trang kết quả |
| Nhãn | "So sánh mô tả giữa hai model; không cho biết model nào đúng" |
| Test | `CMP-01` chỉ số khớp với tính bằng numpy; `CMP-02` từ chối hai tile khác chuỗi; `CMP-03` export CSV/JSON mang provenance của cả hai |

### 2.3 Biểu đồ cho màn so sánh với dữ liệu nhập · 2 ngày · FE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| FE | Bổ sung cho bảng hiện có: scatter dự đoán–quan sát kèm đường đồng nhất, histogram residual, Bland–Altman, và đường calibration theo bin (chỉ khi endpoint tương thích P(ΔPSI ≥ 1)). Dùng SVG + `d3-scale` sẵn có, **không** thêm thư viện biểu đồ |
| Quy tắc | Chỉ vẽ trên quan sát **ghép được và cùng loại endpoint** (FR-30), luôn hiện n; nhãn "không phải validation độc lập" đứng trước biểu đồ |
| Test | `CMP-04` điểm trên đồ thị khớp bảng matched; `CMP-05` endpoint không tương thích thì không vẽ calibration và nêu lý do; axe |

### 2.4 Lớp chú giải mở rộng · 4 ngày · ETL+BE+FE · đợt 3 — ☐ chưa làm

| Nguồn | Nội dung | Điều kiện |
| --- | --- | --- |
| UniProt features (release 2026_03, CC BY 4.0) | Modified residue, cross-link (ubiquitin), region/motif | Tải mới, ghim SHA-256, ghi `data/README.md` |
| Motif degron đã biết | Chỉ từ nguồn có giấy phép mở | ELM/MetaDegron **đang bị chặn** (`redistribution_ok: false`) → không dùng |
| Tần suất biến thể quần thể (ví dụ gnomAD) | Allele frequency theo vị trí | **Kiểm giấy phép trước**; không rõ thì không nạp |

| Việc | Chi tiết |
| --- | --- |
| ETL+DB | Bảng chú giải mới theo từng nguồn; migration; cổng giấy phép như các nguồn hiện có |
| BE+FE | Endpoint lớp phủ; toggle kèm ghi công đặt cạnh nút (giống ClinVar); snapshot lưu kèm phiên bản nguồn (A-6) |
| Test | `ANN-` mới: cổng giấy phép, ánh xạ toạ độ, ghi công hiển thị trên giao diện và trong export |

### 2.5 Xem cấu trúc 3D · 4 ngày · ETL+FE · đợt 3 — ☐ chưa làm

| Việc | Chi tiết |
| --- | --- |
| Dữ liệu | AlphaFold DB (CC BY 4.0): ETL tải sẵn cho protein đã chọn, **hoặc** nút tải theo yêu cầu (opt-in, chỉ gửi accession, báo rõ cho người dùng — R-3) |
| FE | Viewer tự host (Mol\* MIT hoặc 3Dmol.js BSD; chốt sau khi kiểm CSP vì cần WebGL/worker/wasm); tô màu residue theo footprint, hiện pLDDT, chọn residue đồng bộ với ô ma trận |
| Nhãn | "Mô hình dự đoán bằng AlphaFold; vùng pLDDT < 70 là không tin cậy" |
| Rủi ro | Nếu phải nới CSP (`wasm-unsafe-eval`) thì ghi DEVIATIONS và cân nhắc bỏ tính năng; kích thước bundle tăng đáng kể |
| Test | `VIZ-05` tô màu khớp giá trị footprint; `VIZ-06` không có request ra ngoài khi chưa opt-in; CSP không có `unsafe-inline`/`unsafe-eval` cho script |

### 2.6 Gợi ý đột biến nên đo · 2 ngày · BE+FE · đợt 2 · phụ thuộc 1.3, 2.2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | Xếp hạng ứng viên trong một tile theo: (a) điểm cao nhưng phân tán seed lớn, (b) hai model bất đồng mạnh, (c) có biến thể ClinVar ở vị trí đó. Trả kèm lý do từng ứng viên |
| FE | Panel "Ứng viên để kiểm chứng", xuất CSV để đưa vào hồ sơ thí nghiệm |
| Nhãn | "Danh sách ưu tiên hồi cứu, mang tính development; không phải thiết kế thí nghiệm đã được kiểm chứng" đứng trước danh sách |
| Quy tắc | Chỉ xếp hạng; **không** dùng kết quả đo quay lại cập nhật model (R-7) |
| Test | Thứ hạng tái lập được với cùng đầu vào; mỗi ứng viên có lý do; không có ứng viên nào từ tile ngoài miền trừ khi override |

---

## 4. Nhóm 3 — Dữ liệu và tích hợp

### 3.1 Nhập trực tiếp từ MaveDB theo URN · 3 ngày · BE+FE · đợt 3 — ☐ chưa làm

| Việc | Chi tiết |
| --- | --- |
| BE | Ô nhập URN → tải score set (opt-in, chỉ gửi URN — R-3), ánh xạ sang schema import hiện có, giữ nguyên quy trình kiểm tra và xác nhận trước khi lưu (FR-28) |
| Dữ liệu | 26 score set CC0 đã có trong `data/raw/mavedb` dùng làm fixture offline cho test |
| Quy tắc | Ghi lại URN, phiên bản, ngày tải, hash tệp; dữ liệu đặt trong dự án, không trộn vào dữ liệu tham chiếu (NFR-13) |
| Test | `DATA-01` fixture offline ánh xạ đúng; `DATA-02` không có request khi chưa opt-in; `DATA-03` endpoint không tương thích bị tách riêng (FR-30) |

### 3.2 Cập nhật dữ liệu tham chiếu có phiên bản · 3 ngày · ETL+BE+FE · đợt 3 — ☐ chưa làm

| Việc | Chi tiết |
| --- | --- |
| ETL | Nạp được snapshot ClinVar mới bên cạnh bản cũ, giữ `clinvar_file_date`; báo cáo khác biệt (thêm/bớt/đổi phân loại) trong vùng tile |
| Quy tắc | Snapshot phân tích cũ **không đổi** (A-6): vẫn đọc đúng phiên bản chú giải tại thời điểm chạy |
| FE | Trang Data & sources hiện phiên bản đang dùng và bản mới có sẵn, kèm tóm tắt khác biệt |
| Test | `DATA-04` mở lại phân tích cũ sau khi cập nhật → chú giải không đổi; `DATA-05` báo cáo khác biệt khớp với đếm trực tiếp trên dữ liệu |

### 3.3 FASTA nhiều bản ghi / nhiều protein trong một job · 2 ngày · BE+FE · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | Chế độ job nhận nhiều bản ghi FASTA hoặc nhiều accession; mỗi protein là một nhóm item, giữ nguyên giới hạn tổng (NFR-07) và báo trước khối lượng |
| FE | Xem trước theo từng protein (số tile, vùng không phủ, trạng thái miền), kết quả nhóm theo protein |
| Test | `BATCH-` mới: giới hạn tổng được áp dụng; một protein lỗi không làm hỏng các protein khác; manifest xuất ra có cột protein |

### 3.4 CLI và client Python kèm notebook mẫu · 3 ngày · BE · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| CLI | `python -m api.cli predict|job|export|compare` dùng **chung** gói `degron_footprint`, gọi API local hoặc chạy trực tiếp (chế độ offline) |
| Client | Module Python mỏng + notebook mẫu: chấm một tile, gửi job, lấy kết quả kèm provenance |
| Quy tắc | Không thêm đường chấm điểm song song (D-9/RG-01): CLI gọi lại đúng mã của service |
| Test | `CLI-01` kết quả CLI bằng kết quả API (< 1e-9); `CLI-02` CLI không in chuỗi vào log; `CLI-03` notebook chạy được từ đầu đến cuối trên fixture |

### 3.5 Báo cáo PDF/HTML cho một phân tích · 2,5 ngày · BE+FE · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `GET /v1/analyses/{id}/report?format=html` dựng HTML tự chứa: ma trận (SVG nội tuyến), footprint track, bảng top-k, provenance đầy đủ, nhãn giới hạn, ghi công nguồn |
| PDF | Người dùng in từ trình duyệt (có CSS in). **Không** thêm trình dựng PDF phía server để giữ cài đặt gọn; ghi DEVIATIONS |
| Quy tắc | Báo cáo mang cùng nhãn và cảnh báo như trên màn hình, cảnh báo đứng trước số; có hash model và phiên bản nguồn |
| Test | `RPT-01` số trong báo cáo khớp API; `RPT-02` có đủ cảnh báo và ghi công; `RPT-03` HTML không gọi tài nguyên ngoài |

### 3.6 Gói dự án xuất/nhập · 3 ngày · BE+FE · đợt 3 — ☐ chưa làm

| Việc | Chi tiết |
| --- | --- |
| BE | Xuất `.zip` gồm: metadata dự án, snapshot phân tích, job, dataset nhập (kèm tệp gốc), manifest SHA-256 và phiên bản schema |
| BE | Nhập: kiểm manifest, kiểm tương thích schema, **luôn tạo dự án mới** (không ghi đè), báo rõ mục nào không nhập được |
| Quy tắc | Không chứa trọng số model (có thể dựng lại); ghi rõ model id + hash để máy nhận kiểm tra |
| Test | `DATA-06` xuất rồi nhập trên máy sạch cho cùng số; `DATA-07` manifest hỏng bị từ chối; `DATA-08` schema cũ hơn báo lỗi rõ ràng |

---

## 5. Nhóm 4 — Vận hành, quản trị và chất lượng

### 4.1 Sao lưu và khôi phục một lệnh · 1,5 ngày · Ops · đợt 1 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| Script | `make backup` → một thư mục/tệp nén gồm: dump CSDL (`pg_dump` hoặc bản sao SQLite ở trạng thái nhất quán) + volume `workspace` + manifest SHA-256 + phiên bản schema và model id |
| Script | `make restore BACKUP=...` → kiểm manifest trước, từ chối khi schema không khớp, báo rõ cái gì sẽ bị ghi đè và **hỏi xác nhận** |
| Quy tắc | Không sao lưu trọng số model (dựng lại bằng ETL); bản sao lưu chứa chuỗi và dữ liệu nhập nên tài liệu phải nói rõ cách bảo quản |
| Test | `OPS-01` sao lưu → xoá volume → khôi phục → dữ liệu và số liệu khớp; `OPS-02` manifest hỏng bị từ chối; `OPS-03` không ghi đè khi chưa xác nhận |
| Nghiệm thu | Thực hiện trọn vòng trên Docker, ghi thời gian và dung lượng vào `tests/results/` |

### 4.2 Trang quản trị local · 2 ngày · BE+FE · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | `GET /v1/admin/status` (chỉ loopback): lần chạy ETL gần nhất và kết quả, model đã nạp + lý do model không nạp được, tình trạng worker và hàng đợi, số liệu cache, dung lượng CSDL/workspace, phiên bản migration |
| FE | Trang Admin hiển thị các mục trên kèm hành động an toàn: làm mới registry, chạy lại kiểm hash. **Không** có nút chạy ETL hay xoá dữ liệu từ giao diện |
| Quy tắc | Không hiển thị chuỗi, không hiển thị dữ liệu nhập; chỉ đếm và trạng thái |
| Test | `OPS-04` phản ánh đúng trạng thái sau khi dừng worker; `OPS-05` không có payload sinh học; `OPS-06` chặn truy cập không phải loopback |

### 4.3 Quy trình đưa model lên phục vụ có biên bản · 1,5 ngày · Tài liệu+BE · đợt 1 — ✅ xong 18/11

Đây là khoảng trống hiện tại: LoRA-D đang là model mặc định trên máy Trọng theo `.env`, nhưng chưa có biên bản.

| Việc | Chi tiết |
| --- | --- |
| Tài liệu | `system/serving-policy.md`: các bước candidate → kiểm parity → đo latency/RAM → đối chiếu giới hạn claim → **chữ ký/ghi nhận của Trọng và GVHD** → đổi mặc định. Nêu rõ: thứ hạng development không tự cho phép đổi model phục vụ (R-8) |
| BE | Khi khởi động, ghi log một dòng: model mặc định, nguồn (registry hay `DF_DEFAULT_MODEL_ID`), hash; `/healthz` hoặc trang Admin hiện thông tin này |
| Biên bản | Mẫu `system/app/serving-decision-<ngày>.md` (model, bằng chứng, giới hạn, người quyết định, ngày) |
| Nghiệm thu | Cấu hình hiện tại (LoRA-D mặc định) có **một** biên bản tương ứng, hoặc quay về npz; không để trạng thái không khớp hồ sơ |

### 4.4 Theo dõi mức đồng thuận với dữ liệu nhập · 2,5 ngày · BE+FE · đợt 3 · phụ thuộc 2.3 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | Với mỗi bản so sánh đã lưu, ghi lại MAE/Spearman/n và thời điểm; endpoint trả chuỗi thời gian theo dự án |
| FE | Biểu đồ theo thời gian kèm n từng điểm; cảnh báo khi chỉ số xấu đi đáng kể so với các lần trước |
| Quy tắc | **Chỉ cảnh báo**; không tự đổi model, không tự train lại (R-7, R-8). Cảnh báo ghi rõ "có thể do assay/điều kiện khác, không nhất thiết là model sai" |
| Test | `CMP-06` chuỗi thời gian khớp các bản so sánh đã lưu; `CMP-07` không có hành động tự động nào được kích hoạt |

### 4.5 Nhiều worker và ưu tiên job · 2 ngày · BE+Ops · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| BE | Hàng đợi hiện đã hỗ trợ nhiều worker (lease, `SKIP LOCKED` trên PG; `BEGIN IMMEDIATE` trên SQLite) — kiểm bằng chạy thật nhiều container worker |
| BE | Thêm `priority` cho job (tile đơn trước job dài), giới hạn số item đang chạy mỗi job để một job lớn không chiếm hết |
| Ops | `docker compose up -d --scale worker=N`; tài liệu nêu rõ RAM mỗi worker khi dùng LoRA-D (~500 MiB) |
| Test | `BATCH-` mới: 3 worker không xử lý trùng item; huỷ job vẫn đúng khi nhiều worker; ưu tiên được tôn trọng |

### 4.6 Kiểm accessibility thủ công và hồi quy giao diện bằng ảnh · 2 ngày · T · đợt 1 — ◐ một phần

| Việc | Chi tiết |
| --- | --- |
| A11Y | Kiểm tay toàn bộ UC-01…10: chỉ dùng bàn phím, kiểm với trình đọc màn hình (NVDA hoặc Orca), kiểm tín hiệu không dựa màu; ghi biên bản `system/app/a11y-manual-<ngày>.md` (A11Y-01…04) |
| Ảnh | Playwright snapshot ảnh cho các màn chính (light/dark, 1440/360) với ngưỡng sai khác nhỏ, dùng mock API để ổn định |
| Chụp lại | `e2e/screenshots.spec.ts` chụp lại bộ ảnh Phụ lục A sau khi đổi font Roboto (ảnh hiện tại là bản Fira) |
| Test | `UX-01` ảnh hồi quy; `UX-02` biên bản A11Y đầy đủ các mục đã kiểm, nêu rõ ai kiểm và ngày |

---

## 6. Nhóm 5 — Trải nghiệm người dùng

### 5.1 Hướng dẫn lần đầu và chú giải thuật ngữ · 2 ngày · FE · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| FE | Bảng chú giải tại chỗ cho PSI, ΔPSI, tile, cổng miền, calibration, top 10 % (nút "?" mở popover, có thể đóng bằng bàn phím) |
| FE | Hướng dẫn 4 bước khi mở lần đầu (tạo dự án → chọn protein → chấm tile → lưu), bỏ qua được, nhớ bằng `localStorage` |
| Quy tắc | Nội dung lấy từ `srs.md` §1.4 để không lệch định nghĩa; không thay cho nhãn giới hạn (R-1) |
| Test | `UX-03` popover đóng/mở bằng bàn phím, có `aria-describedby`; `UX-04` hướng dẫn chỉ hiện lần đầu; axe |

### 5.2 Phím tắt, nhớ bộ lọc và ghim shortlist · 2 ngày · FE · đợt 3 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| FE | Phím tắt: di chuyển trong ma trận bằng phím mũi tên (đã có), thêm chuyển chế độ xem, mở bảng, tìm kiếm; bảng phím tắt mở bằng `?` |
| FE | Nhớ bộ lọc bảng xếp hạng và shortlist theo từng phân tích (`localStorage`, chỉ id và tuỳ chọn hiển thị — **không** lưu chuỗi, NFR-09) |
| Test | `UX-05` phím tắt không xung đột với trình đọc màn hình; `UX-06` không có chuỗi trong `localStorage` |

### 5.3 Song ngữ Anh–Việt · 4 ngày · FE · đợt 3 — ☐ chưa làm

| Việc | Chi tiết |
| --- | --- |
| FE | Lớp i18n nhẹ (từ điển JSON, không thêm thư viện nặng), bộ chọn ngôn ngữ, `lang` trên `html` |
| Quy tắc | **Nhãn khoa học và cảnh báo**: dịch phải giữ nguyên ý nghĩa và mức độ; mỗi nhãn giới hạn có bản dịch được duyệt, không rút gọn. Thuật ngữ bám `srs.md` §1.4. Export và provenance giữ tiếng Anh để khớp hồ sơ |
| Test | `UX-07` không còn chuỗi cứng tiếng Anh trong giao diện chính; `UX-08` nhãn cảnh báo có đủ hai ngôn ngữ; `UX-09` axe ở cả hai ngôn ngữ |
| Rủi ro | Công sức lớn, dễ lệch nghĩa ở nhãn khoa học. Cắt trước tiên nếu thiếu thời gian |

### 5.4 Chế độ trình bày cho buổi bảo vệ · 1 ngày · FE · đợt 2 — ✅ xong 18/11

| Việc | Chi tiết |
| --- | --- |
| FE | Bật/tắt bằng phím tắt: ma trận và footprint phóng to, ẩn bảng phụ, chữ lớn hơn; **giữ nguyên** nhãn giới hạn và cảnh báo (R-1) |
| Test | `UX-10` ở chế độ trình bày vẫn còn banner miền, cảnh báo và nhãn bằng chứng; axe |

---

## 7. Rủi ro và phương án cắt

| Rủi ro | Dấu hiệu | Phương án |
| --- | --- | --- |
| Deadline bảo vệ (D-2) đến sớm | Chưa xong đợt 1 trước tuần cuối | Cắt theo thứ tự: 2.3 → 3.5 → 1.3 → 2.1; giữ 1.1, 1.2, 4.3, 4.6 vì liên quan tính đúng đắn hồ sơ |
| LoRA-D vẫn chậm sau 1.4 | p95 > 15 s/tile | Ghi số thật; giữ npz làm mặc định; quét protein dài coi là ngoài phạm vi thực dụng |
| Tối ưu làm đổi số | Parity > 1e-5 | Bắt buộc model id mới và đánh giá lại; không im lặng đổi hành vi (R-8) |
| Nguồn dữ liệu mới không rõ giấy phép | gnomAD/ELM | Không nạp; ghi lý do vào `data/README.md` và DEVIATIONS |
| Viewer 3D xung đột CSP | Cần `wasm-unsafe-eval` | Cân nhắc bỏ 2.5; nếu giữ, ghi DEVIATIONS và giới hạn phạm vi |
| Test hồi quy ảnh hay báo động giả | Khác biệt do font/antialias | Ngưỡng sai khác theo từng màn, chỉ chạy trên Chromium |
| Cache đĩa làm lộ chuỗi | Bật nhầm trong bản cài của người khác | Mặc định tắt, có cảnh báo trong INSTALL, test `CACHE-04` |
| i18n làm lệch nghĩa nhãn khoa học | Bản dịch rút gọn | Duyệt từng nhãn giới hạn; cắt 5.3 nếu không đủ thời gian |

---

## 8. Mốc nghiệm thu từng đợt

Mỗi đợt kết thúc bằng:

1. `make docker-test` (PostgreSQL) và `make docker-test DF_TEST_BACKEND=sqlite` — ghi số case thực tế.
2. `npx vitest run`, `npx playwright test` (mock, gồm axe và ma trận trình duyệt).
3. `make docker-e2e` với **cả hai** model mặc định (npz và LoRA-D).
4. `npx tsc --noEmit`, `npx eslint .`, `ruff`, `mypy`.
5. Cập nhật `system/openapi.yaml`, `system/test-plan.md`, `system/db-design.md`, `system/ui-design.md`, `DEVIATIONS.md`,
   `INSTALL.md` cho phần đã đổi.
6. Biên bản `system/app/acceptance-system-<ngày>.{md,json}`: số case thực tế, số đo hiệu năng, những gì **chưa** kiểm.
7. Cập nhật §10 nhật ký của tệp này và mục liên quan trong [plan.md](plan.md).

Không đợt nào được phép đổi `scientific_status`, đóng G3 hay đổi model phục vụ mặc định nếu thiếu biên bản 4.3.

---

## 9. Hướng phát triển tương lai

**Chỉ xem xét sau khi hoàn thành nhóm 1–5.** Mỗi mục dưới đây **vượt phạm vi** đã chốt trong
[system/srs.md](system/srs.md) §1.3, nên trước khi làm phải có quyết định đổi phạm vi của Trọng và GVHD, ghi thành
biên bản riêng. Ghi vào phần "Hướng phát triển" của Kết luận luận văn, **không** ghi là tính năng đã có.

| # | Hướng | Vì sao hấp dẫn | Vì sao hiện bị loại | Điều kiện tiên quyết |
| --- | --- | --- | --- | --- |
| F-1 | Tài khoản, nhiều người dùng, chia sẻ dự án trong nhóm | Nhiều người cùng dùng một bản cài | SRS §1.3 loại; cần xác thực, phân quyền, cách ly dữ liệu, kiểm toán | Quyết định đổi phạm vi; rà bảo mật riêng; mô hình đe doạ mới |
| F-2 | Triển khai công khai (VPS/TLS/SLA), giới hạn tần suất theo người dùng | Người ngoài dùng thử | SRS §1.3 loại; app là local-first, NFR-09 dựa trên giả định loopback | F-1; rà quyền riêng tư dữ liệu người dùng gửi lên; profile `vps` hiện **chưa kiểm** |
| F-3 | Suy luận bệnh, hoặc xác định E3 ligase cụ thể | Giá trị sinh học cao | **Model không có bằng chứng cho kết luận này**; vi phạm NFR-15 nếu trình bày như kết quả | Nghiên cứu và nhãn thực nghiệm mới; không phải việc của phần mềm |
| F-4 | Tự động train lại / đưa dữ liệu người dùng vào benchmark | Model "tự cải thiện" | R-7, SRS §1.3; phá tách biệt benchmark ↔ dữ liệu người dùng, làm mất khả năng tái lập | Quy trình MLOps riêng, bộ test giữ nguyên benchmark, biên bản khoa học |
| F-5 | Đa đột biến và thiết kế ngược (tổ hợp làm tăng/giảm độ ổn định) | Ứng dụng thiết kế protein | Model chỉ được đánh giá cho **một** thay thế; chưa có nhãn đa đột biến | Dữ liệu đa đột biến; đánh giá riêng; nhiều khả năng cần kiến trúc khác |
| F-6 | Lượng tử hoá int8 cho LoRA-D | Nhanh và nhẹ hơn | Là **model khác** về mặt số học, phải đánh giá lại trên T | Chạy lại đánh giá, model id mới, biên bản phục vụ (4.3) |
| F-7 | Nguồn dữ liệu bị chặn giấy phép (ELM, MetaDegron, Koren S4) | Chú giải phong phú hơn | `redistribution_ok: false`; R-6 cấm nạp | Giấy phép rõ ràng bằng văn bản từ chủ sở hữu |

Nguyên tắc chung cho §9: một hướng chỉ rời khỏi mục này khi có (a) quyết định đổi phạm vi, (b) kế hoạch đánh giá
riêng nếu nó đụng tới khoa học, (c) biên bản tương ứng. Không hướng nào được "làm thử rồi tính sau" trong mã nguồn
chính.

---

## 10. Nhật ký thay đổi

| Ngày | Thay đổi | Người |
| --- | --- | --- |
| 18/11/2026 | Tạo biên bản từ bản phân tích 17/11. Nhóm 1–5 chia thành 3 đợt (≈ 75 ngày); nhóm 6 và đa đột biến chuyển sang §9 "Hướng phát triển tương lai", chỉ xem xét sau khi xong nhóm 1–5 | Trọng + Claude |
| 18/11/2026 | Bắt đầu đợt 1: code + test cho 1.1, 1.2, 1.3, 1.5, 1.7 và phần BE/tài liệu của 4.3; migration `0005`. Trọng đồng ý chạy Docker: dựng lại image, sao lưu rồi nâng CSDL PG + `dev.db` lên `0005`; 1.1/1.2/1.3/1.5/1.7 đạt. Trọng chọn soạn biên bản phục vụ LoRA-D (nháp chờ xác nhận) | Trọng + Claude |
| 18/11/2026 | Đợt 1, lượt 2: đạt 2.1, 2.3, 3.5, 4.1 (Docker PG/SQLite + e2e). Vòng sao lưu Docker làm trên project tạm, không ghi đè CSDL thật. Còn 4.3 (chờ Trọng ký) và 4.6 (kiểm tay a11y) | Claude |
| 18/11/2026 | Đóng đợt 1 (4.3 có hiệu lực; 4.6 phần tự động, chờ kiểm tay). Đợt 2 xong cả 9 mục (1.4 không đạt mục tiêu 15 s, ghi số thật). Đợt 3 bắt đầu: 4.4, 5.2 xong; 1.6 có biên bản đề xuất chờ quyết định. Migration 0006–0008. Biên bản `system/app/acceptance-system-2026-11-18c.md` | Trọng + Claude |
| 19/11/2026 | Cập nhật trạng thái: §11 sắp theo đợt, đủ 29 mục (đợt 1: 10/11, đợt 2: 9/9, đợt 3: 2/9), thêm bảng việc chờ người; cột trạng thái ở §1; dấu trạng thái ở tiêu đề từng mục | Claude |

---

## 11. Trạng thái thực hiện

Cập nhật **19/11/2026**. `[x]` đạt toàn bộ tiêu chí nghiệm thu (kèm bằng chứng); `[~]` đã làm một phần, nêu phần còn
thiếu; `[ ]` chưa bắt đầu. Biên bản nghiệm thu (không ghi đè nhau):
[acceptance-system-2026-11-18.md](system/app/acceptance-system-2026-11-18.md) (đợt 1, lượt 1),
[acceptance-system-2026-11-18b.md](system/app/acceptance-system-2026-11-18b.md) (đợt 1, lượt 2),
[acceptance-system-2026-11-18c.md](system/app/acceptance-system-2026-11-18c.md) (đóng đợt 1, đợt 2, đầu đợt 3).

| Đợt | Xong `[x]` | Một phần `[~]` | Chưa `[ ]` |
| --- | --- | --- | --- |
| Đợt 1 — trước bảo vệ | 10/11 | 4.6 | — |
| Đợt 2 | 9/9 | — | — |
| Đợt 3 | 2/9 | 1.6 | 2.4, 2.5, 3.1, 3.2, 3.6, 5.3 |

Lần chạy kiểm cuối (18/11, Docker, sau migration `0008`): backend PostgreSQL 344 pass / 19 skip, SQLite 363 pass;
Vitest 211/211; Playwright mock lượt đầy đủ 40/41 — ca hỏng là ảnh hồi quy UX-01 do thanh tiêu đề dính, đã sửa, chạy lại
riêng 4/4 hai lần (24 ảnh chuẩn); e2e backend thật 14 + 1 skip (LoRA-D mặc định), 15/15 (npz
mặc định). Chi tiết ở `acceptance-system-2026-11-18c.json`.

### Đợt 1 — trước bảo vệ

| Mục | Trạng thái | Bằng chứng | Còn thiếu |
| --- | --- | --- | --- |
| 1.1 | [x] 18/11 | `/v1/models` thêm `serving`, `not_serving_reason`, `expected_tile_seconds`; `ModelSelect`, `?model=`, hộp xác nhận model chậm, "Run with another model", `/model/:id`. MSEL-01…04; MSEL-04 pass trên Docker với cả hai model mặc định | — |
| 1.2 | [x] 18/11 | `degron_footprint/cache.py`; CACHE-01…04; `system/app/tests/results/cache-lora.json`: lần hai ≤ 30,2 ms (lần đầu ≥ 33,1 s) | Số hit/miss trên trang quản trị làm cùng 4.2 |
| 1.3 | [x] 18/11 | Migration `0005`; `Cell.score_seed_sd/min/max`; chế độ "Seed spread", thang chốt ở `ui-design.md` §5; UNC-01…04; snapshot 17/11 mở/xuất được | — |
| 1.5 | [x] 18/11 | DOM-02 pass trên PG và SQLite (container) | — |
| 1.7 | [x] 18/11 | `job_item.duration_ms`, `Job.eta_seconds`; ETA, tiến độ trên tiêu đề tab, thông báo opt-in; BATCH-08/09 | ETA giả định một worker (xem lại ở 4.5) |
| 2.1 | [x] 18/11 | `GET /v1/jobs/{id}/footprint`; `ProteinFootprint` trên trang Job (làn xen kẽ, dải miền, bảng thay thế). VIZ-01…04 | — |
| 2.3 | [x] 18/11 | `ComparisonCharts`: scatter + đường đồng nhất, histogram residual, Bland–Altman, calibration theo bin (chỉ endpoint tương thích). CMP-04/05; axe trong e2e UC-09 | — |
| 3.5 | [x] 18/11 | `GET /v1/analyses/{id}/report?format=html` (`api/report.py`), nút "Report" ở thẻ Export; PDF qua hộp in của trình duyệt. RPT-01…03 | — |
| 4.1 | [x] 18/11 | `ops/backup.py`, `make backup` / `make restore BACKUP=`; OPS-01…03 `tests/test_backup.py`; vòng Docker có xoá volume `tests/results/backup-roundtrip.json` (sao lưu 15 s / khôi phục 29 s, ≈ 63 MB) | Hướng dẫn bảo quản bản sao lưu đã ghi ở INSTALL §6 |
| 4.3 | [x] 18/11 | `system/serving-policy.md`; log khởi động + `/healthz` (OPS-07); [serving-decision-2026-11-18.md](system/app/serving-decision-2026-11-18.md) có hiệu lực: Trọng xác nhận 18/11, GVHD đã ghi nhận (theo Trọng) | — |
| 4.6 | [~] | UX-01 hồi quy ảnh `frontend/e2e/visual.spec.ts` (24 ảnh chuẩn: 6 màn × 2 theme × 1440/360, Chromium); chụp lại bộ ảnh `system/app/docs/screenshots/` (thêm footprint protein, báo cáo, biểu đồ so sánh; trên bản sao `dev.db`); mẫu [a11y-manual-2026-11-18.md](system/app/a11y-manual-2026-11-18.md) | **Người** điền biên bản kiểm tay (UX-02); chép ảnh mới vào `report/assets/screenshots/` nếu muốn Phụ lục A có các màn mới (việc của nhánh 3) |

### Đợt 2

| Mục | Trạng thái | Bằng chứng | Còn thiếu |
| --- | --- | --- | --- |
| 1.4 | [x] 18/11 | Bước a–b: đo từng phần (forward backbone ≈ toàn bộ), batch không có tác dụng, 6 luồng, gộp LoRA (`DF_LORA_MERGE`, sai khác 5,0e-6 ≤ 1e-5 → giữ model id). PERF-01 Docker `measure_latency_lora.py`: p95 39,1 s → **28,1 s/tile** (`tests/results/latency-lora.json`, `latency-lora-after.json`); `lora-speed.json` | Mục tiêu đề xuất ≤ 15 s **không đạt** (ghi nhận, theo tiêu chí). Bước c (ONNX), d (GPU) tuỳ chọn chưa làm; mặc định `.env` chưa đổi |
| 2.2 | [x] 18/11 | `POST /v1/analyses/compare`, `/v1/model-comparisons/*`, bảng `model_comparison` (migration 0006); tab "Other model" + trang so sánh (BrBG, scatter, bất đồng lớn nhất, export). CMP-01…03; e2e mock + axe + 360 px; e2e thật CMP real | — |
| 2.6 | [x] 18/11 | `GET /v1/analyses/{id}/suggestions` (+CSV); tab "Candidates". SUG-01…03 | — |
| 3.3 | [x] 18/11 | `JobRequest.proteins` (1–20), giới hạn tổng residue, protein lỗi thành một item refused; xem trước từng protein; coverage và footprint theo protein. BATCH-10 | — |
| 3.4 | [x] 18/11 | `python -m api.cli`, `api/client.py`, `docs/notebooks/degron-footprint-client.ipynb`. CLI-01…03 | — |
| 4.2 | [x] 18/11 | `/v1/admin/status`, reload registry, trang Admin; heartbeat worker (migration 0007). OPS-04…06 | — |
| 4.5 | [x] 18/11 | `analysis_job.priority` (migration 0008), tối đa 2 item đang chạy mỗi job, ETA theo số worker sống; BATCH-11; chạy thật `--scale worker=3`: 36 item, 15/13/8 mỗi worker, không trùng (`tests/results/workers-scale.json`) | — |
| 5.1 | [x] 18/11 | Hàng thuật ngữ + popover "?", hướng dẫn 4 bước lần đầu. UX-03/04 | — |
| 5.4 | [x] 18/11 | Chế độ trình bày (nút, Alt+Shift+P). UX-10 | — |

### Đợt 3

| Mục | Trạng thái | Bằng chứng | Còn thiếu |
| --- | --- | --- | --- |
| 1.6 | [~] | Biên bản đề xuất [gate-policy-proposal-2026-11-18.md](research/lora-refit-transfer-2026-11-16/gate-policy-proposal-2026-11-18.md) (số theo tầng PSI, phương án A/B/C, khuyến nghị A) | **Quyết định của Trọng/GVHD**; không triển khai trước đó |
| 2.4 | [ ] | — | Cần tải UniProt features (CC BY 4.0) và kiểm giấy phép nguồn biến thể quần thể; hỏi Trọng trước khi tải |
| 2.5 | [ ] | — | Cần AlphaFold DB (opt-in/ETL) và chọn viewer tự host (Mol\* hoặc 3Dmol.js) sau khi kiểm CSP; hỏi trước khi tải |
| 3.1 | [ ] | — | Truy cập MaveDB theo URN (opt-in, chỉ gửi URN); fixture offline từ 26 score set CC0 có sẵn |
| 3.2 | [ ] | — | Nạp snapshot ClinVar mới song song bản cũ + báo cáo khác biệt |
| 3.6 | [ ] | — | Gói dự án xuất/nhập `.zip` có manifest SHA-256 |
| 4.4 | [x] 18/11 | `GET /v1/projects/{id}/agreement` từ các bản so sánh đã lưu; tab "Agreement over time". CMP-06/07 | — |
| 5.2 | [x] 18/11 | Phím tắt v/t/'/'/? có công tắc tắt (WCAG 2.1.4); ghim trong bảng xếp hạng; nhớ bộ lọc/sắp xếp/ghim theo id. UX-05/06 | — |
| 5.3 | [ ] | — | Song ngữ Anh–Việt; rủi ro lệch nghĩa nhãn khoa học, cắt trước tiên nếu thiếu thời gian |

### Việc chờ người

| Việc | Ai | Ghi chú |
| --- | --- | --- |
| Kiểm tay accessibility (4.6, UX-02) | Người kiểm | Điền [a11y-manual-2026-11-18.md](system/app/a11y-manual-2026-11-18.md): bàn phím K1–K12, trình đọc màn hình S1–S6, màu C1–C4 |
| Quyết định chính sách cổng miền (1.6) | Trọng + GVHD | Chọn A / A + B / C trong [gate-policy-proposal-2026-11-18.md](research/lora-refit-transfer-2026-11-16/gate-policy-proposal-2026-11-18.md); khuyến nghị A |
| Bật 6 luồng + gộp LoRA trong `.env` (1.4) | Trọng | p95 28,1 s thay vì 39,1 s; điểm lệch ≤ 5e-6 so với số trong biên bản phục vụ — nên ghi một dòng vào biên bản nếu bật |
| Tải dữ liệu ngoài cho 2.4, 2.5, 3.1 | Trọng | Đồng ý trước khi tải UniProt features, AlphaFold DB, MaveDB |
| Chép ảnh mới vào `report/assets/screenshots/` | Nhánh 3 | Ảnh ở `system/app/docs/screenshots/` (thêm 06b, 07b, 08b) |
