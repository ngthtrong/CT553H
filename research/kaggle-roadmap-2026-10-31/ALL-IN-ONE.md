# Một notebook cho toàn bộ luồng v3

Hướng dẫn từng phiên, snapshot dataset, Save Version và resume: [MULTI-SESSION.md](MULTI-SESSION.md).

File: [12-all-in-one.ipynb](notebooks/12-all-in-one.ipynb).
Notebook chứa sẵn mã runner, registry ghim revision và protocol/dependency; chỉ cần
**dataset core v3** và Internet khi cài thư viện/tải model. Không cần dataset code
hoặc dataset weights riêng. Có thể gắn weights/output cũ để giảm tải lại.

Notebook này điều phối đúng các chức năng đã có trong12 notebook đơn. Nó không tự
tạo thêm dữ liệu wet-lab, nguồn ngoài hoặc mapping cấu trúc; cũng không bổ sung
final promotion tự động ngoài W5. Mọi giới hạn khoa học của runner gốc được giữ.

## Chạy lần đầu trên Kaggle

1. Upload `degron-data-v3-fullpsi.zip` thành dataset private nếu chưa có.
2. New Notebook → Import Notebook → chọn `12-all-in-one.ipynb`.
3. Add Input → gắn core v3. Session Options → Internet On, GPU cho các nhánh pLM.
4. Giữ cấu hình smoke ban đầu:

   ```python
   SMOKE = True
   INSTALL_DEPENDENCIES = True
   AUTO_DOWNLOAD = True
   SECTIONS = None
   MAX_NEW_TASKS = None
   RESUME_FROM = ""
   ```

5. Save Version → Save & Run All. Đây là phiên mới nên giữ cell cài dependency.
6. Kiểm bảng trạng thái, `pipeline-manifest.json`, biểu đồ và output checkpoint ZIP.

### Lỗi thiếu `references/proteins.fasta.gz` ở bước chuẩn bị

Log `Successfully installed ...` rồi `FileNotFoundError` trong `Dataset` là lỗi
kiểm dữ liệu sau cài dependency. Nếu input có `references/proteins.fasta` thay cho
`references/proteins.fasta.gz`, file gzip đã được giải nén nhưng manifest vẫn ghi
tên/checksum của bản nén. Điều tương tự có thể xảy ra với năm source snapshot TSV.

Import lại **bản `12-all-in-one.ipynb` đã sửa**, restart session/kernel, giữ
`SMOKE=True`, `RESUME_FROM=""`, gắn core input hiện có rồi chạy từ đầu. Không cần
upload lại core nếu đủ các file đã giải nén đúng nội dung. Bootstrap sẽ in
`Verified expanded gzip members: ...` khi dùng nhánh này. Chỉ sửa `.py` hoặc gắn
code dataset mới không cập nhật runner đã nhúng trong notebook cũ.

Runner kiểm SHA-256 và kích thước của nội dung đã giải nén bằng registry
`degron_v3/gzip-content-hashes.json`, được sinh từ ZIP core gốc đã kiểm checksum
bằng `build_gzip_hashes.py`. Registry ghim đúng SHA của `DATA_MANIFEST.json` và
từng gzip gốc; data identity, nhãn và splits giữ nguyên. File gzip còn tồn tại vẫn
phải khớp checksum gốc. Thiếu file hoặc sai checksum vẫn dừng; không bỏ kiểm hash.
Nếu chỉ có log thiếu gzip mà chưa thấy danh sách file input, việc nền tảng đã giải
nén là chẩn đoán cần xác nhận, chưa phải quan sát trực tiếp trên runtime Kaggle.

Smoke dùng ESM2-8M thật cho preflight/feature/fine-tuning, head04/05 dùng fixture
ghi rõ tên. Không báo điểm smoke như hiệu năng model. Chuyển `SMOKE=False` tạo
campaign official khác; để `RESUME_FROM=""`, không phục hồi smoke vào official.

## Các bước được tự nối

Thứ tự: **00 → 01 → 02 → 03 → 04 → 05 → 06 → 11 → 08 → 09 → 07 → 10**.

- 00: audit và official historical reproduction. 01: fit Ridge A–E/controls/curve.
- 02: tìm weights đã có; nếu thiếu thì kiểm ngân sách, tải revision đã pin và probe.
- 03: tự nhận preflight, trích pooled/crop. Official05 tự nhận crop anchor35M.
- 04: so family/scale với head chung; candidate chưa xử lý xong không bị âm thầm bỏ.
- 05: train pointwise/CNN/mCNN; official tách job theo head/arm/seed.
- 06: quality/source-aware Ridge và scanning-pretrain→sat-fine-tune CNN.
- 11: frozen comparator/LoRA, optional full tuning8M/35M; tách job mode/arm/seed.
- 08/09: thiếu input thật ghi source_pending/structure_pending.
- 07: chờ các job development trong kế hoạch, calibration recipe đã định sẵn trước T.
- 10: gộp OOF theo recipe và cùng cohort; báo mỗi seed và ensemble thực, CI theo nhóm.

Mỗi job có config/data/code/protocol signature, file hashes và trạng thái. Kết quả
cohort cấu trúc con tách khỏi full W. Nested family selection vẫn là quy trình chọn
được đánh giá, không tự chuyển bảng outer scores thành tuyên bố model thắng độc lập.

## Chạy official qua nhiều Save Versions

Một notebook không có nghĩa mọi checkpoint/fold/seed chạy vừa một phiên. Mặc định
official khảo sát ESM35 anchor; có thể chọn các model khác, hoặc `MODEL_IDS="all"`
để lập kế hoạch toàn bộ sequence families/scales. Các model3B/6B/15B có thể bị chặn
bởi disk/VRAM; runner chưa tự dispatch/offload/quantization. Model15B weights hiện
lớn hơn ngân sách output mặc định: cần tài sản input/phần cứng phù hợp, không bỏ gate.

Ví dụ phiên official đầu chỉ hoàn thành hai job mới:

```python
SMOKE = False
MODEL_IDS = ["esm2_35m"]
SECTIONS = None
MAX_NEW_TASKS = 2
SESSION_HOURS = 8.0
MAX_OUTPUT_GIB = 16.0
RESUME_FROM = ""
```

Kết thúc phiên, **Save Version phải có output**. Phiên sau gắn output trước làm
input (hoặc tải checkpoint ZIP rồi upload như private dataset), rồi đặt:

```python
RESUME_FROM = "/kaggle/input/.../<campaign-folder>"
# Folder này chứa pipeline-manifest.json, tasks/, aggregate/...
# Hoặc đặt tới file <campaign>-checkpoint.zip.
MAX_NEW_TASKS = 3
```

Giữ OUTPUT_ROOT mặc định, SMOKE/MODEL_IDS/FINETUNE_MODEL/OVERRIDES và các input
khoa học như trước. Thay SECTIONS, MAX_NEW_TASKS, thời lượng/storage budget và
AUTO_DOWNLOAD được phép mà không đổi scientific plan. Nếu code/data/plan đổi,
notebook tạo campaign mới và từ chối ghép resume cũ. Khi đang có campaign cùng phiên,
để RESUME_FROM="" để tiếp tục cache local; không copy đè một campaign đang tồn tại.

`SESSION_HOURS` chỉ là soft stop **giữa các job**. Job đang chạy có thể dài hơn phần
thời gian còn lại; chưa có watchdog tự ngắt giữa epoch. Checkpoint lưu mỗi epoch;
muốn resume sau khi session mất phải có output đã được Save Version bảo toàn.

## Tùy chọn và ngân sách

```python
# Chỉ chạy nhóm đã chọn trong phiên, không thay danh sách thí nghiệm của campaign:
SECTIONS = ["00", "01", "02", "03"]

# Giữ protocol nhưng chia job fine-tuning thành nhiều phiên bằng MAX_NEW_TASKS.
# OVERRIDES là lựa chọn khoa học, thay đổi nó sẽ tạo campaign mới:
OVERRIDES = {"11": {"finetune_modes": ["frozen", "lora"]}}

# Nguồn thật đã review (chỉ thêm khi đã có):
EXTERNAL_TABLE = None
STRUCTURE_TABLE = None
RUN_SAPROT = False
```

MODEL_IDS không tự tải SaProt; nó đi nhánh cấu trúc với SAPROT_MODEL. Official05
cần ESM35 crop nên anchor này được thêm vào preflight/extraction ngay cả khi family
screen chọn họ khác. FINETUNE_MODEL là checkpoint fine-tune riêng. Đổi precision,
grid, mode/full tuning hoặc source không được reuse kết quả dưới cùng campaign.

CALIBRATION_TASK mặc định `"01"`, recipe `ordered-w5-D`. Có thể chọn task khác
chứa recipe bằng CALIBRATION_TASK và OVERRIDES["07"]["selected_recipe"], nhưng
CNN/LoRA/family hiện chỉ calibration CV; final refit/export phục vụ cần triển khai riêng.

## Output và trạng thái

```text
/kaggle/working/degron-v3-all/
├── code/<embedded-sha>/         # mã giải nén và manifest, không phải weights
├── weights/<model>/<revision>/  # checkpoint gốc tải trong phiên
└── {smoke,official}/<plan-id>/
    ├── pipeline-manifest.json
    ├── pipeline-status.csv
    ├── tasks/<job>-<config-hash>/
    ├── aggregate/evidence.{json,csv}
    └── summary.png
```

- `complete`: job runner hoàn tất; đọc thêm outcome. Source_pending/structure_pending
  chỉ nói route audit đã ghi nhận thiếu đầu vào, không có thí nghiệm source đó.
- `waiting_dependency`: chưa đủ đầu ra phù hợp của bước trước.
- `weights_pending`: cần weights/tài nguyên storage hoặc thay cách cung cấp input.
- preflight outcome `resource_blocked`: checkpoint chưa chạy được; không suy là model kém.
- `session_stop_reason`: dừng soft budget, không coi là hoàn tất nghiên cứu.

ZIP checkpoint mặc định chứa model, báo cáo và state, **bỏ pool.npy/crop.npy và
pretrained weights** để giảm nhân bản. Full output directory vẫn có feature; resume
bằng directory giữ được chúng. Resume ZIP sẽ kiểm trạng thái và trích lại feature
thiếu. `EXPORT_FEATURES_IN_ZIP=True` giữ cả feature nếu đủ disk. Nếu tạo ZIP sẽ vượt
MAX_OUTPUT_GIB, notebook giữ full directory và báo archive_skipped_storage_budget.
Không tự xóa weights hoặc output người dùng.

Snapshot chỉ khôi phục artifact tin cậy do chính pipeline sinh ra. Các file/checkpoint
đổi hash không được dùng lại như kết quả hợp lệ. Dataset core không thay và không
đóng G2/G3 tự động. Kiểm chứng cục bộ xem [all-in-one-validation.json](all-in-one-validation.json);
GPU/CUDA và toàn bộ official benchmark vẫn cần chạy trên Kaggle.
