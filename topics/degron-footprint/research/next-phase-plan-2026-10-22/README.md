# Kế hoạch giai đoạn tiếp theo: nghiên cứu, huấn luyện bằng notebook, và xây dựng hệ thống — 22/10/2026

Nối tiếp [next-steps-plan](../next-steps-plan-2026-10-22/README.md) (§0 là trạng thái đã đo). Kế hoạch này **không** đổi trạng thái G2/G3, không sửa tiêu chí đã chốt của thí nghiệm nào, và không sửa slide. Mọi mục `[ĐỀ XUẤT]` cần Trọng duyệt trước khi chạy; chi phí là **ước lượng lập kế hoạch**, chưa benchmark.

**Mốc thời gian dùng để lập lịch** `[CHƯA XÁC MINH]`: buổi gặp 02/10 là tuần 4, nên tuần 1 bắt đầu 14/09 và hôm nay (22/10) là tuần 6. Giả định học kỳ 15 tuần thì tuần 15 là 21–27/12/2026. Ngày nộp thật chưa có trong repo (`resources/course/CT553H.pdf` không có lịch; đề cương cũng ghi "sẽ bổ sung"). Nếu ngày thật khác, chỉ cần dịch §5.

## 0. Tóm tắt

- `[ĐO]` Mô hình hiện tại là **ridge M3 + Platt**, AUROC 0,8208 trên benchmark phát triển OOF (outer-test 91 peptide), đã hiệu chuẩn (Brier 0,0925 so với 0,1272). Suy luận chỉ cần `numpy`, nên **hệ thống không cần GPU để chạy**; GPU chỉ phục vụ phần nghiên cứu.
- `[DIỄN GIẢI]` Có hai luồng gần như độc lập, nối với nhau qua **một giao diện mô hình cố định** (§4.2): luồng A (nghiên cứu, notebook) có thể trượt tiến độ mà không chặn luồng B (hệ thống), vì hệ thống chỉ cần "một mô hình đã đóng băng + cổng miền áp dụng".
- `[ĐỀ XUẤT]` **Lõi tối thiểu** (đủ cho một luận văn kỹ thuật phần mềm trung thực): R0 tái lập trong notebook, R3 cổng miền áp dụng, R5 đóng băng mô hình + model card, SRS, API + giao diện web cho UC-01..03, bộ kiểm thử, Chương 3–4 và các phần còn `[PENDING]`. **Phần mở rộng** (cắt được nếu trượt): R1 Degformer sạch cụm, R2 đặc trưng ESM-2, R4 kiểm chứng ngoài.
- `[ĐỀ XUẤT]` Phát hiện thiết kế đáng giá nhất của lượt phân tích này: **cổng miền áp dụng** (`R3`) hiện chưa có. Mô hình chỉ học trên peptide có `PSI(WT) ≤ 4,0`, nhưng công cụ chưa biết tile người dùng nhập có thuộc miền đó hay không. Dữ liệu để làm cổng **đã có tại máy** (§3.2, R3).

## 1. Phân tích hiện trạng

### 1.1 Khoa học: vững chỗ nào, hổng chỗ nào

| Hạng mục | Trạng thái | Nhãn |
|---|---|---|
| Ridge M3 vượt PAP và các thiết kế sức chứa lớn hơn | 0,8208 (ext 4,0) so với ΔPAP 0,7693 (tính ở base); năm thiết kế tương tác âm | `[ĐO]` |
| Lợi ích nới ngưỡng 4,0 | +0,0126, bền qua `RESCUE_DELTA`, chia lại fold và 3 phân hoạch protein thật | `[ĐO]` |
| Hiệu chuẩn | Platt đạt tiêu chí chốt trước; thiên thấp ~13% tương đối ở miền gốc | `[ĐO]` |
| Tiền huấn luyện nhãn tile | Âm với thiết kế đã thử | `[ĐO]` |
| Nguồn nhãn ngoài | Koren S4 không qua cổng (5 cụm mới < 20); Timms 2023 / Genetic Glues chưa xác minh | `[ĐO]` / chưa xác minh |
| **G2: đối chứng Degformer sạch cụm** | **Chưa làm** | điều kiện còn thiếu |
| **Kiểm chứng ngoài thật** | **Chưa có.** Mọi con số là phát triển OOF trên dữ liệu đã khảo sát nhiều lần | giới hạn lớn nhất |
| **Cổng miền áp dụng cho công cụ** | **Chưa có** | lỗ hổng thiết kế |

`[DIỄN GIẢI]` Hai lỗ hổng cuối quyết định mức tin được của sản phẩm: không có kiểm chứng ngoài thì "đã hiệu chuẩn" chỉ đúng **trong miền phát triển**, và không có cổng miền thì giao diện có thể đưa ra điểm đẹp cho một tile bền (ngoài miền) mà không cảnh báo. Ch.1 đã đòi "out-of-domain phải báo rõ" nhưng chưa có cơ chế.

### 1.2 Hệ thống: có gì, thiếu gì

- `[ĐO]` Có: [predict.py](../calibration-p6-2026-10-22/predict.py) (CLI, chỉ `numpy`, 28-mer, đặc trưng 180 chiều), [verify.py](../calibration-p6-2026-10-22/verify.py) (11 phép đối chiếu với runner, chênh < 1e-9).
- Thiếu: SRS, thiết kế dữ liệu (Ch.3 mục *Data Model/Dictionary/Relationships* còn `[PENDING]`), API, giao diện, triển khai, bộ ca kiểm thử UI/API (Ch.4 §4.3–4.6 còn một phần `[PENDING]`), và các ngưỡng phi chức năng (Ch.1 *Non-Functional Requirements* còn `[PENDING]`).
- Ràng buộc có sẵn từ Ch.1 phải giữ: không lưu chuỗi người dùng quá phiên trừ khi nêu rõ; mọi đầu ra kèm phiên bản mô hình, nguồn dữ liệu, miền hỗ trợ; điểm chưa hiệu chuẩn không được gọi là xác suất; không khẳng định nguyên nhân bệnh.

## 2. Nguyên tắc xuyên suốt `[ĐỀ XUẤT]`

1. **Giữ nguyên quy ước nghiên cứu** của `CLAUDE.md`: seed 17/29/43, fold theo cụm cov80, bootstrap theo cụm, tiêu chí chốt trong `PROTOCOL.md` **trước** khi chạy, kết quả âm báo thẳng, không biến kết quả cục bộ thành "hoàn tất G2".
2. **Mã nguồn thật vẫn là file `.py` trong repo**; notebook chỉ là lớp mỏng gọi chúng. Không nhân đôi logic vào notebook, để `verify.py` và runner vẫn là một nguồn sự thật duy nhất.
3. **Một triển khai suy luận duy nhất** dùng chung cho CLI, API và test (đóng gói thành package, §4.3). Hiện `predict.py` là bản độc lập có chủ đích để đối chiếu với `derisk.featurize`; giữ cả hai, đừng gộp.
4. **Giấy phép quyết định cái gì được vào sản phẩm và vào dataset upload.** Được: Zhang (CC BY 4.0), Voutsinos (MIT), UniProt/AlphaFold (CC BY 4.0), ClinVar (ghi công + câu phủ nhận chẩn đoán đi theo đầu ra). **Không được:** Koren (chỉ dùng nội bộ), MetaDegron (repo không LICENSE), Larsen (chờ xác nhận email).
5. **Không có tài khoản người dùng** và mặc định không lưu chuỗi nhập (theo Ch.1). Lưu chỉ khi người dùng chọn chia sẻ liên kết, có hạn.

## 3. Luồng A: nghiên cứu và huấn luyện bằng notebook

### 3.1 Hạ tầng notebook

`[ĐỀ XUẤT]` Mọi bước **huấn luyện** chạy trên nền tảng notebook từ xa, không chạy cục bộ. Chạy cục bộ chỉ còn: kiểm cú pháp notebook, viết `PROTOCOL.md`, đọc `results.json`, sinh bảng/hình cho luận văn.

| Hạng mục | Đề xuất | Lý do / ghi chú |
|---|---|---|
| Nền tảng chính | **Kaggle Notebooks** (GPU T4/P100, dataset riêng tư có phiên bản, đầu ra versioned) | Dataset có phiên bản gắn SHA nên tái lập tốt hơn Drive; không phải ủy quyền Drive. Hạn mức và độ dài phiên `[CHƯA XÁC MINH]`, kiểm lại trước khi lên lịch |
| Dự phòng | Google Colab | Notebook viết **không phụ thuộc nền tảng**: ô 0 tự dò `/kaggle/input` hay Drive |
| Đưa mã lên | Gói `degron-code-<commit>` tạo bằng `git archive` thành dataset | Repo private: **không dán token vào notebook**. Ô 0 so commit băm với commit ghi trong PROTOCOL |
| Đưa dữ liệu lên | Gói `degron-data-v1`, chỉ chứa nguồn được phép (§2.4), kèm `manifest.json` SHA-256 | Ước lượng kích thước: cache ngưỡng ~10 MB, `gps-peptidome-rep1.tsv` 21 MB, `degrons.csv.gz` 16 MB, FASTA 7 MB, `training_data.csv` 20 MB → dưới 100 MB |
| Đầu ra mang về | `results.json`, `env.json`, notebook đã thực thi (đầu ra đã lược), checkpoint ngoài git | Đặt vào `research/<tên>/`, cập nhật `data/README.md` trong cùng phiên |

`[ĐỀ XUẤT]` **Tải dữ liệu lên dịch vụ ngoài là hành động hướng ra bên ngoài** (có thể bị lưu/chỉ mục). Tôi sẽ chỉ **dựng gói cục bộ** bằng script `make_data_package.py` và liệt kê file + giấy phép; **việc upload do Trọng xác nhận** sau khi xem danh sách.

**Cấu trúc một notebook** (mọi thí nghiệm theo mẫu này):

```
0. Môi trường: in phiên bản python/numpy/torch/GPU; dò nền tảng; so commit và SHA dữ liệu với PROTOCOL
1. Cổng tái lập: dựng lại mốc đã biết (ridge 0,8082 / 0,8208), assert dung sai; dừng nếu lệch
2. Tham số: seed 17/29/43, fold từ results.json của G2 (không tự chia lại)
3. Chạy thí nghiệm bằng hàm của runner .py (import, không sao chép)
4. Ghi results.json + env.json; bootstrap 5.000 theo cụm; in bảng tiêu chí chốt trước
5. Kết luận chỉ in theo đúng điều kiện trong PROTOCOL (không diễn giải thêm trong notebook)
```

- Tên file: `research/<thí-nghiệm>/notebooks/NN-tên.ipynb`; `PROTOCOL.md` commit **trước** khi chạy, ô 0 in hash commit đó.
- Tính tất định: đặt seed cho `numpy`/`torch`, bật cờ deterministic; GPU vẫn có thể lệch cuối số thập phân, nên cổng ở ô 1 đặt dung sai (đề xuất AUROC ±1e-4) và phép so ridge luôn chạy trên CPU.
- Kiểm cục bộ **không huấn luyện**: `nbformat` validate, biên dịch từng ô code (`compile`), và một cờ `SMOKE=1` chỉ chạy vài bước trên nền tảng.

### 3.2 Danh sách thí nghiệm

Thứ tự theo giá trị cho hệ thống trên chi phí. **Cả R1 và R2 là thăm dò, và ridge có khả năng vẫn thắng**; kế hoạch được viết để hệ thống không phụ thuộc kết quả đó.

| # | Thí nghiệm | Câu hỏi | Tiêu chí chốt trước (phác) | Tài nguyên | Phụ thuộc |
|---|---|---|---|---|---|
| **R0** | Tái lập trong notebook | Môi trường nền tảng có tái lập đúng mốc? | |ΔAUROC| ≤ 1e-4 so với 0,8082 và 0,8208; `predict.py` khớp runner < 1e-9 | CPU, vài phút | Gói dữ liệu |
| **R3** | **Cổng miền áp dụng** | Tile này có thuộc miền `PSI(WT) ≤ 4,0` không? | Phân loại `PSI ≤ 4,0` trên **tile cụm giữ riêng**: AUROC có CI theo cụm, báo precision/recall tại ngưỡng cảnh báo; chỉ gọi "dùng được" nếu CI dưới > 0,5 và Brier < tần suất nền | CPU hoặc GPU nhỏ | R0 |
| **R2** | Đặc trưng ESM-2 đóng băng | Biểu diễn pLM có thêm tín hiệu ngoài one-hot + ngữ cảnh? | Ridge trên `M3 ∪ PCA(Δembedding)` (PCA khớp chỉ trên outer-train) so M3 ext 4,0: nhận khi CI ghép cặp > 0 **và** dương ở cả ba seed | GPU ~vài chục phút trích đặc trưng (ước lượng) | R0 |
| **R1** | Degformer sạch cụm (đóng điều kiện G2) | Với dữ liệu tiền huấn luyện đã loại cụm test, kiến trúc đã công bố có vượt ridge? | Chạy lại kiến trúc trên bảng 569.270 dòng sau khi loại mọi chuỗi chạm cụm outer-test (từng fold); chấm ΔPSI bằng hiệu điểm; so ridge ext 4,0 ghép cặp theo cụm. Báo cả hai chiều, kể cả âm | GPU, vài đến chục giờ (**chưa benchmark**) | R0; đọc mã Degformer cách ly |
| **R4** | Kiểm chứng ngoài (thăm dò, **không** xác nhận) | Mô hình đóng băng có đúng chiều trên dữ liệu chưa dùng? | (a) Koren S4: tỉ lệ ô cùng dấu và Spearman theo vị trí cuối, đã cảnh báo lệch thang 3 bin/6 bin và thư viện 23-mer; (b) kiểm xem **scanning mutagenesis** của Zhang còn peptide nào ngoài 176 peptide huấn luyện không | CPU, chỉ đánh giá | R5 |
| **R5** | Đóng băng mô hình + model card | Phiên bản nào được vào sản phẩm? | Quy tắc chọn ghi trước: mặc định `ridge M3 ext 4,0 + Platt`; chỉ thay nếu R1 hoặc R2 đạt tiêu chí của chính nó. Sinh `weights.npz`, SHA-256, `model-card.md` | CPU | R3 (cổng), R1/R2 nếu có |

**Chi tiết R3** `[ĐỀ XUẤT]`: nguồn nhãn đã có tại máy là **sàng peptidome GPS của Zhang** (`interim/gps-peptidome-rep1.tsv`, 475.506 peptide, CC BY 4.0) cho PSI đo của tile toàn proteome. Hai tầng: (i) tile **có trong sàng** thì cổng là **tra cứu PSI đo** (không cần dự đoán); (ii) tile ngoài sàng, ví dụ chuỗi người dùng tự gõ, dùng bộ dự đoán `PSI(WT)` huấn luyện trên chính sàng này với chia cụm protein. `[CHƯA XÁC MINH]`: cần kiểm tile 28-mer của sàng có khớp tile 28-mer mà mô hình ΔPSI dùng, và kiểm thang PSI giữa hai nguồn trùng. Kết quả P3 không phải bỏ phí: bộ tiền huấn luyện đạt Pearson 0,864 trên gene giữ riêng cho nhãn Voutsinos, nhưng thang khác Zhang, nên chỉ dùng làm đặc trưng phụ nếu R3 cần, không thay nhãn Zhang.

**Chi tiết R2** `[ĐỀ XUẤT]`: đây là thay đổi **biểu diễn đầu vào**, không phải thiết kế tương tác thứ sáu, nên không vi phạm quy tắc "không thử biến thể lớp mạng" của kế hoạch trước. Chốt trước một cỡ mô hình duy nhất (không chọn sau khi thấy số) và ghi: trọng số ESM-2 cần kiểm giấy phép trước khi dùng `[CHƯA XÁC MINH]`; ESM-2 được tiền huấn luyện không giám sát trên UniRef có thể chứa các protein này, ghi vào giới hạn.

**Điều kiện dừng và hệ quả cho hệ thống** `[ĐỀ XUẤT]`:

| Tình huống | Phản ứng |
|---|---|
| R1 và R2 đều âm | Mô hình sản phẩm giữ nguyên ridge + Platt; báo hai kết quả âm trong Ch.4. Đây là kết quả hợp lệ |
| R3 không đạt (cổng yếu) | Sản phẩm chỉ cảnh báo định tính ("chỉ đúng cho tile đã đo trong sàng GPS") và chỉ phục vụ UniProt tile có trong sàng. Ghi thành giới hạn |
| Hết hạn mức GPU | Bỏ R1 trước (đắt nhất, ít ảnh hưởng sản phẩm), giữ R3 và R5 |
| Notebook lệch mốc ở R0 | Dừng mọi thí nghiệm sau đó; sửa môi trường trước |

## 4. Luồng B: hệ thống (SRS, giao diện, CSDL, API, kiểm thử, triển khai)

### 4.1 Tài liệu cần viết, theo thứ tự

Thư mục mới đề xuất: `topics/degron-footprint/system/` (`srs.md`, `db-design.md`, `ui-design.md`, `api-spec.md`, mã trong `app/`). `[ĐỀ XUẤT]` Viết **bằng tiếng Anh**, vì chúng nạp thẳng vào Ch.1 và Ch.3 của luận văn (viết tiếng Anh); các ghi chú kế hoạch vẫn tiếng Việt. Cần Trọng xác nhận.

| # | Tài liệu | Nội dung chính | Đầu ra trong luận văn |
|---|---|---|---|
| S1 | **SRS** (khung IEEE 29148) | Phạm vi, giả định, danh sách yêu cầu có ID, truy vết yêu cầu → ca kiểm thử | Ch.1 (điền `[PENDING]` các ngưỡng phi chức năng) |
| S2 | Thiết kế dữ liệu | ERD, từ điển dữ liệu, ràng buộc, kế hoạch nạp dữ liệu có SHA | Ch.3 *Data Design* |
| S3 | Thiết kế giao diện | Sơ đồ trang, wireframe, quy tắc hiển thị cảnh báo, truy cập | Ch.3 *Functional Design* |
| S4 | Đặc tả API | OpenAPI, mã lỗi, giới hạn kích thước | Ch.3 *Architecture* |
| S5 | Kế hoạch và ca kiểm thử | Ma trận truy vết SRS → test | Ch.4 §4.3–4.6 |

### 4.2 Phạm vi chức năng `[ĐỀ XUẤT]`

Giữ UC-01..03 của Ch.1 và thêm bốn ca, tất cả đã khớp với dữ liệu có thể dùng hợp pháp:

| ID | Ca | Ghi chú |
|---|---|---|
| UC-01 | Dự đoán ma trận hiệu ứng | Mặc định tile 28-mer; nhập chuỗi hoặc UniProt + vị trí tile |
| UC-02 | Xếp hạng thay thế | Lọc theo vị trí, acid amin; cột xác suất hiệu chuẩn |
| UC-03 | Xuất kết quả kèm provenance | CSV/JSON; trường bắt buộc: `model_id`, `weights_sha256`, `data_sources`, `domain_status`, `generated_at`, câu phủ nhận |
| **UC-04** | Chọn tile từ protein UniProt | Hiển thị thanh dọc theo protein, tô màu trạng thái miền (từ cổng R3) |
| **UC-05** | So với dữ liệu đo | Phủ ΔPSI đo của Zhang lên ma trận khi tile thuộc 176 peptide (CC BY 4.0); đây là phần *Extend* của UC-01 |
| **UC-06** | Phủ biến thể ClinVar | Đánh dấu biến thể missense tại ô, kèm câu phủ nhận và ngày phát hành; **không** diễn giải thành chẩn đoán |
| **UC-07** | Xem thẻ mô hình | Phiên bản, chỉ số OOF kèm CI, miền áp dụng, giới hạn, nguồn và giấy phép |

**Ngoài phạm vi** (ghi vào SRS): tài khoản, xử lý lô nhiều protein, hệ đo khác (N-degron, ổn định protein khác), khẳng định nguyên nhân bệnh, ứng dụng di động.

**Yêu cầu phi chức năng, ngưỡng đề xuất** (sẽ **đo rồi mới chốt**, như yêu cầu của Ch.1): tính tất định (cùng đầu vào + phiên bản → cùng điểm; khớp runner < 1e-9, đã có), độ trễ p95 cho một tile 28-mer và cho protein 1.000 aa (khoảng 44 tile × 532 ô) trên máy cấu hình thấp, kích thước đầu vào tối đa, tỉ lệ yêu cầu, tương phản/bàn phím theo WCAG 2.1 AA, thông điệp cảnh báo luôn hiển thị cùng điểm.

### 4.3 Kiến trúc `[ĐỀ XUẤT]`

```
Trình duyệt (React + TypeScript, SPA)
        │ HTTPS / JSON (OpenAPI)
FastAPI (Python 3.11, Pydantic v2)  ──  gói degron_footprint: featurize · ridge · Platt · gate · provenance
        │ SQLAlchemy 2 + Alembic
PostgreSQL 16 (dev/test: SQLite)   ←  ETL nạp từ data/ (ghi SHA mỗi nguồn)
```

| Lớp | Chọn | Lý do | Phương án khác |
|---|---|---|---|
| Suy luận | `numpy` thuần, mô hình `weights.npz` | Đã có, không phụ thuộc framework; tải mô hình lúc khởi động | Không dùng `torch` trong hệ thống |
| API | FastAPI | Sinh OpenAPI tự động, dễ kiểm hợp đồng | Flask |
| Giao diện | React + Vite + TypeScript, heatmap bằng Plotly.js hoặc D3 | Kiểm thử e2e chuẩn (Playwright) | HTMX + Jinja: ít mã hơn; chọn nếu muốn rút gọn |
| CSDL | PostgreSQL | Ràng buộc và chỉ mục đủ cho bảng ClinVar vài triệu dòng | SQLite cho bản demo một file |
| Đóng gói | Docker Compose (api, db, web) | Một lệnh dựng lại | — |
| Kiểm thử | pytest, hypothesis, schemathesis, vitest, Playwright, axe | Xem §4.6 | — |

`[DIỄN GIẢI]` **Giao diện mô hình (`ModelAdapter`)** là chỗ tách hai luồng: `featurize(seq, pos, aa)`, `score(...)`, `calibrate(...)`, `domain(seq)`, kèm `model_id`. Mô hình v1 là ridge; nếu R1/R2 đạt tiêu chí thì v2 chỉ cần thêm một adapter, không sửa API hay giao diện.

### 4.4 Thiết kế CSDL (phác) `[ĐỀ XUẤT]`

Hệ thống chủ yếu **đọc**. Không precompute điểm cho mọi đột biến (116.702 tile × 532 ô ≈ 62 triệu dòng, không cần vì suy luận là phép nhân vector), mà tính khi yêu cầu.

| Bảng | Khóa / trường chính | Ghi chú |
|---|---|---|
| `data_source` | `source_id`, tên, phiên bản, DOI/URL, **giấy phép**, `redistribution_ok`, SHA-256, ngày tải, trích dẫn | Mọi bảng dữ liệu tham chiếu tới đây; đầu ra provenance lấy từ đây |
| `protein` | `uniprot_acc`, gene, độ dài, chuỗi, release | Swiss-Prot 2026_03, ~20k dòng |
| `tile` | `tile_id`, `uniprot_acc`, `start`, `end`, chuỗi, `psi_wt_measured` (có thể NULL), `psi_wt_pred` (có thể NULL), `in_domain`, `domain_source` | Từ sàng peptidome (R3); duy nhất `(acc, start, end)` |
| `measured_cell` | `(tile_id, pos, mut_aa)`, `psi_mut`, `delta_psi`, `n_rep`, `source_id` | Chỉ Zhang saturation (CC BY); ~92k dòng |
| `clinvar_variant` | `(accession)`, `uniprot_acc`, `pos`, `wt`, `mut`, `clinsig`, `review_status`, `release_date`, `source_id` | Chỉ missense đã ánh xạ UniProt; kèm câu phủ nhận ở tầng hiển thị |
| `model_version` | `model_id`, loại, `weights_sha256`, `feature_spec`, chỉ số OOF + CI (JSON), hiệu chuẩn (JSON), miền, **trạng thái** {candidate, frozen, retired}, đường dẫn model card | Khóa ngoại từ mọi lần chạy |
| `prediction_run` | `run_id` (UUID), loại đầu vào, chuỗi, `model_id`, `domain_status`, cảnh báo (JSON), `created_at`, `expires_at`, `share_token` | **Chỉ tạo khi người dùng chọn chia sẻ**; mặc định phi trạng thái; hạn mặc định 7 ngày |
| `prediction_cell` | `(run_id, pos, mut_aa)`, điểm, xác suất, hạng | Xoá theo `expires_at` |

Ràng buộc: khóa ngoại + `CHECK` cho tập acid amin chuẩn, `pos` trong `[1, độ dài]`, `wt` khớp chuỗi tile. Không có bảng người dùng. Nạp dữ liệu bằng một script ETL có kiểm SHA và có thể chạy lại; mọi migration qua Alembic.

### 4.5 Giao diện (phác) `[ĐỀ XUẤT]`

| Trang | Thành phần chính |
|---|---|
| **Nhập** | Hai tab: *Dán chuỗi 28-mer* / *Chọn protein UniProt* (tìm theo gene hoặc accession, thanh tile có màu miền). Kiểm tra đầu vào ngay khi gõ (độ dài, ký tự), thông báo lỗi cụ thể |
| **Kết quả** | (1) khối **trạng thái miền** + cảnh báo luôn ở đầu trang; (2) heatmap 28×19, hàng dưới là acid amin hoang dã, thang màu phân kỳ an toàn cho mù màu, chuyển đổi *điểm* / *xác suất hiệu chuẩn*; (3) bảng xếp hạng (lọc theo vị trí/acid amin, sắp xếp); (4) lớp phủ tùy chọn: ΔPSI đo (UC-05), ClinVar (UC-06); (5) chân trang provenance |
| **Xuất** | Nút CSV/JSON; tên file chứa `model_id` và ngày; kiểm tra tệp ghi được, nếu lỗi thì giữ kết quả trên màn hình (đúng luồng ngoại lệ UC-03) |
| **Thẻ mô hình** | Chỉ số, miền, giới hạn, nguồn, giấy phép, lịch sử phiên bản |

Quy tắc giao diện bắt buộc: không bao giờ hiển thị điểm **mà không** kèm trạng thái miền và phiên bản mô hình; từ "xác suất" chỉ dùng cho giá trị đã hiệu chuẩn và luôn ghi sự kiện đang được dự đoán (`ΔPSI ≥ 1,0`); mọi lớp ClinVar kèm câu phủ nhận. Wireframe sẽ viết trước bằng markdown/ASCII trong `ui-design.md`; mockup HTML chạy được hoặc file Figma chỉ làm khi Trọng muốn.

### 4.6 API (phác) `[ĐỀ XUẤT]`

| Phương thức | Đường dẫn | Mục đích |
|---|---|---|
| `POST` | `/v1/predict` | `{sequence \| uniprot_id + tile_start, model_id?}` → ma trận, hạng, trạng thái miền, provenance |
| `GET` | `/v1/proteins/{acc}/tiles` | Danh sách tile + trạng thái miền |
| `GET` | `/v1/tiles/{id}/measured` · `/clinvar` | Lớp phủ (UC-05/06) |
| `GET` | `/v1/models` · `/v1/models/{id}` | Thẻ mô hình |
| `POST` | `/v1/runs` · `GET /v1/runs/{id}` | Chia sẻ có hạn (tùy chọn) |
| `GET` | `/v1/runs/{id}/export?format=csv\|json` | Xuất kèm provenance |
| `GET` | `/healthz` | Sức khỏe, phiên bản |

Lỗi trả về cố định `{code, message, field?}`; giới hạn độ dài và tần suất; không ghi chuỗi người dùng vào nhật ký.

### 4.7 Kiểm thử (nạp Ch.4 §4.3–4.6) `[ĐỀ XUẤT]`

| Tầng | Công cụ | Nội dung |
|---|---|---|
| Đơn vị | pytest | `featurize` so độc lập với `derisk.featurize`; hiệu chuẩn; xử lý biên (vị trí 1 và 28, ký tự lạ) |
| Thuộc tính | hypothesis | Sinh chuỗi ngẫu nhiên hợp lệ/không hợp lệ: hợp lệ luôn ra 28×19 ô hữu hạn, không hợp lệ luôn ra lỗi có mã |
| Hồi quy so với runner | script kế thừa `verify.py` | Điểm API = điểm runner (< 1e-9) trên mẫu cố định + tệp golden `example-output.csv` |
| Hợp đồng API | schemathesis theo OpenAPI | Mọi endpoint, mọi mã lỗi |
| Đầu-cuối | Playwright | UC-01..07 theo đúng luồng chính và ngoại lệ của Ch.1 |
| Phi chức năng | locust nhẹ, axe | Độ trễ p95, truy cập; ghi số đo **kèm cấu hình máy** |
| Bảo mật | fuzz đầu vào, giới hạn kích thước | Không thực thi, không lưu chuỗi quá phiên |

## 5. Lịch `[ĐỀ XUẤT]`

Theo giả định tuần 15 = 21–27/12. Tuần 6 hiện tại là 19–25/10.

| Tuần | Luồng A (nghiên cứu) | Luồng B (hệ thống) | Cổng |
|---|---|---|---|
| **7** · 26/10–1/11 | Dựng gói dữ liệu/mã cục bộ; `PROTOCOL` cho R0, R3, R2, R1; **upload sau khi Trọng duyệt**; chạy **R0** | **S1 SRS v1** + thiết kế dữ liệu v1 | R0 qua |
| **8** · 2–8/11 | **R3** cổng miền; R2 trích đặc trưng | S2 CSDL, S4 API; khung `app/` + ETL | |
| **9** · 9–15/11 | R2 chạy; khởi động R1 nếu hạn mức cho phép | S3 giao diện, nối API; trang nhập + kết quả | |
| **10** · 16–22/11 | R1 kết quả hoặc dừng; **R5 đóng băng mô hình** | Ma trận, bảng hạng, xuất; UC-05/06 | **Đóng băng mô hình** |
| **11** · 23–29/11 | R4 (đánh giá, không huấn luyện) | Kiểm thử tầng đơn vị/thuộc tính/API; thẻ mô hình | |
| **12** · 30/11–6/12 | Báo cáo kết quả R1–R5 vào Ch.4 | Playwright, hiệu năng, triển khai | Hệ thống chạy được đầu-cuối |
| **13** · 7–13/12 | Ch.3 + Ch.4 phần còn lại | Sửa lỗi, tài liệu cài đặt (Phụ lục A) | |
| **14** · 14–20/12 | Abstract, Tóm tắt, Kết luận, Lời cảm ơn | Dừng tính năng | Bản nháp gửi GVHD |
| **15** · 21–27/12 | Đệm / sửa theo góp ý | Đệm | Nộp |

`[DIỄN GIẢI]` Đường găng là **R3 → R5 (đóng băng) → hệ thống nối mô hình thật → kiểm thử → triển khai**. R1, R2, R4 đều nằm ngoài đường găng; trượt thì cắt, không dồn vào các tuần cuối.

## 6. Rủi ro

| Rủi ro | Phản ứng |
|---|---|
| Hạn mức hoặc phiên notebook ngắn hơn dự tính | Chia R1 theo fold, lưu checkpoint từng fold; nếu vẫn thiếu thì bỏ R1 |
| GPU không tất định làm lệch cổng | Ridge luôn chạy CPU; dung sai nêu trước |
| Cổng miền R3 yếu hoặc thang PSI không khớp giữa sàng và nhãn bão hòa | Hạ xuống cảnh báo định tính, ghi giới hạn; không giả vờ có cổng |
| Số "hiệu chuẩn" bị đọc thành xác suất bệnh | Câu phủ nhận bắt buộc + chỉ hiển thị sự kiện `ΔPSI ≥ 1,0`; test e2e kiểm chuỗi cảnh báo luôn có mặt |
| Rò dữ liệu không phép vào dataset upload hoặc sản phẩm | Gói dữ liệu chỉ từ danh sách phép (§2.4), kiểm bằng script; Koren/MetaDegron bị chặn cứng trong ETL |
| Phạm vi hệ thống phình ra (tài khoản, lô, nhiều hệ đo) | Danh sách "ngoài phạm vi" trong SRS; thêm tính năng chỉ qua thay đổi có ghi |
| Đọc benchmark phát triển như kiểm chứng ngoài | Mọi trang và Ch.4 gắn nhãn "phát triển OOF"; R4 báo là thăm dò |
| Mã ESM-2 / Degformer tải về chứa mã không tin cậy | Chạy trong notebook cô lập, không chạy mã nằm trong `data/raw/` trên máy chính |

## 7. Quyết định cần Trọng duyệt

1. **Nền tảng notebook:** Kaggle (đề xuất) hay Colab? Trọng đã có tài khoản và hạn mức GPU nào?
2. **Ngôn ngữ tài liệu hệ thống:** tiếng Anh (đề xuất, vì nạp thẳng vào Ch.1/Ch.3) hay tiếng Việt?
3. **Ngăn xếp:** FastAPI + React/TypeScript + PostgreSQL (đề xuất) hay phương án rút gọn FastAPI + HTMX + SQLite?
4. **Nơi triển khai:** máy của khoa/ĐHCT, dịch vụ miễn phí, hay chỉ Docker cục bộ cho buổi bảo vệ?
5. **Phần mở rộng:** có làm R1 (đắt GPU nhất) và R2 hay cắt về lõi tối thiểu?
6. **Upload dữ liệu lên dịch vụ notebook:** đồng ý theo danh sách phép ở §2.4 (xem trước khi upload)?
7. **Ngày nộp thật** để dịch lịch §5.

## 8. Việc làm ngay sau khi duyệt, theo thứ tự `[ĐỀ XUẤT]`

1. Soạn **SRS v1** (S1) và điền các ngưỡng phi chức năng ở Ch.1 bằng số tạm, ghi rõ "chờ đo".
2. Viết `make_data_package.py` + `make_code_package.sh` (cục bộ, chưa upload) và `PROTOCOL.md` của R0/R3.
3. Dựng khung notebook mẫu `00-reproduce.ipynb` theo mẫu §3.1 và kiểm cú pháp.
4. Dựng khung `app/` (package `degron_footprint` tách từ `predict.py`) kèm bộ test đối chiếu với `verify.py`.
