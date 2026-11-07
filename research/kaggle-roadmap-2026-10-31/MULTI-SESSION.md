# Chạy notebook tổng qua nhiều phiên Kaggle

Một phiên = một lượt **Save Version → Save & Run All**. Một campaign = toàn bộ kế
hoạch cùng code/data/model/thiết kế; campaign được tích lũy qua nhiều phiên bằng
snapshot. Giữ một notebook Kaggle và một core dataset. Dùng thêm một private dataset
checkpoint để mang kết quả phiên trước sang phiên sau khi không gắn trực tiếp
Notebook Output. Hướng dẫn này không chạy thêm thực nghiệm official.

**Dùng bản [12-all-in-one.ipynb](notebooks/12-all-in-one.ipynb) hiện tại.** Bản này
xử lý chỉ mục SNAPSHOT.json khi Kaggle tự giải nén checkpoint ZIP; embedded runners
không đổi nên vẫn nhận campaign cũ có cùng cấu hình khoa học. Kiểm chứng bổ sung:
[multi-session-validation.json](multi-session-validation.json).

## 1. Chuẩn bị một lần

1. New Dataset → upload `degron-data-v3-fullpsi.zip`, giữ Private.
2. New Notebook → File → Import Notebook → chọn `12-all-in-one.ipynb` hiện tại.
3. Add Input → gắn core v3. Không cần code/weights dataset.
4. Session Options → Internet On, chọn GPU đang có cho chuỗi có pLM. Giữ cùng
   loại accelerator và image/environment giữa các phiên nếu có thể.
5. Luôn sửa **cell tham số có sẵn**. Giữ nguyên cell mã embedded và các cell runner.

Nếu muốn smoke trước: `SMOKE=True`, `MAX_NEW_TASKS=None`, `RESUME_FROM=""`, chạy
Save & Run All. Smoke chỉ kiểm luồng. Khi chuyển official, đặt SMOKE=False và
RESUME_FROM="" để bắt đầu campaign official mới; không phục hồi smoke vào official.

## 2. Phiên official 1: audit và linear baseline

Giữ các biến khác ở mặc định, sửa:

```python
SMOKE = False
INSTALL_DEPENDENCIES = True
AUTO_DOWNLOAD = True
DATA_DIR = ""
OUTPUT_ROOT = ""
EXTRA_WEIGHT_ROOTS = []

MODEL_IDS = ["esm2_35m"]
FINETUNE_MODEL = "esm2_35m"
CALIBRATION_TASK = "01"
OVERRIDES = {}
SECTIONS = None

RESUME_FROM = ""
MAX_NEW_TASKS = 2
SESSION_HOURS = 8.0
MAX_OUTPUT_GIB = 16.0
EXPORT_FEATURES_IN_ZIP = True
```

MODEL_IDS=[35M] là ví dụ anchor để chạy ổn định toàn luồng; không có nghĩa đã khảo
sát cả20 checkpoint. Muốn khảo sát nhiều model, chốt danh sách trước campaign đầu.
Thêm model sau đó làm đổi plan ID; không ghép vào campaign cũ sau khi xem điểm test.

Save Version → Save & Run All, ghi chú `official-batch-01`. Không cần chạy full
training bằng tay trước khi Save & Run All vì background sẽ chạy lại từ đầu.
Chờ version hoàn tất rồi mở **version đã lưu → Output**.

Với mặc định trên, hai job mới là `00` và `01`. Có thể thấy session_stop_reason=
max_tasks và nhiều task pending/waiting_dependency; đó là dừng theo lịch đã chọn.
Kaggle Completed xác nhận batch kết thúc, còn tiến độ toàn kế hoạch đọc trong
pipeline-status.csv. Lưu plan ID được in ở dòng Campaign.

## 3. Lưu snapshot phiên 1

Trong Output tìm:

```text
degron-v3-all/official/<plan-id>/pipeline-manifest.json
degron-v3-all/official/<plan-id>/pipeline-status.csv
degron-v3-all/official/<plan-id>-checkpoint.zip
```

Tải **đúng file `<plan-id>-checkpoint.zip` của version vừa hoàn tất**. Snapshot chứa
trạng thái tích lũy, model, OOF, báo cáo và feature khi EXPORT_FEATURES_IN_ZIP=True.
Không cần tải/upload core data lại mỗi phiên.

Tạo private dataset `degron-v3-checkpoints`, upload ZIP vừa tải. Kaggle giải nén ZIP;
trong dataset cần thấy pipeline-manifest.json, tasks/, aggregate/ và SNAPSHOT.json.
Chờ xử lý xong, rồi trở lại notebook → Add Input → gắn dataset checkpoint này.

Nếu Add Input cho phép gắn trực tiếp output version trước, có thể dùng thư mục
campaign đầy đủ thay cho bước tải/upload; nó giữ cả feature. Không dựa vào khả năng
tự gắn output của cùng notebook nếu giao diện tài khoản không cung cấp lựa chọn đó.

## 4. Tìm đường dẫn RESUME_FROM thật

Đường dẫn mount có thể khác theo giao diện/version. Không copy nguyên đường dẫn
minh họa. Thêm cell chỉ đọc sau cell tham số và chạy riêng cell đó:

```python
from pathlib import Path
import json

for path in Path("/kaggle/input").rglob("pipeline-manifest.json"):
    saved = json.loads(path.read_text())
    states = saved.get("tasks", {})
    done = sum(item.get("status") == "complete" for item in states.values())
    print("mode:", saved.get("plan", {}).get("mode"))
    print("plan_id:", saved.get("plan_id"))
    print("completed tasks:", done)
    print("RESUME_FROM =", repr(str(path.parent)))
    print()
```

Chọn đúng mode=official, plan ID của phiên1 và snapshot mới nhất đã xác nhận. Copy
nguyên dòng RESUME_FROM in ra vào cell tham số. Giá trị là **thư mục cha** chứa
pipeline-manifest.json, không phải đường dẫn tới chính file JSON. Nếu input giữ ZIP
nguyên thay vì giải nén thì cũng có thể trỏ trực tiếp tới checkpoint ZIP.

## 5. Phiên official 2: preflight, features và family head

Giữ nguyên cấu hình khoa học của phiên1; chỉ thay:

```python
RESUME_FROM = "/kaggle/input/<duong-dan-that-tu-cell-tren>"
MAX_NEW_TASKS = 3
EXPORT_FEATURES_IN_ZIP = True
```

Save Version → Save & Run All, ghi chú `official-batch-02-resume`.

Kết quả mong đợi khi runtime/cấu hình không đổi:

```text
CACHED 00
CACHED 01
RUN 02-esm2_35m
RUN 03-esm2_35m
RUN 04
```

Notebook tự tìm weights đã gắn; nếu chưa có thì tải. Feature được truyền thẳng sang
head04. Hết3 job mới, phần sau được giữ pending rồi báo cáo/xuất ZIP. Đầu ra phiên2
đã bao gồm kết quả phiên1, nên phiên sau chỉ cần snapshot tích lũy mới nhất.

Tải checkpoint ZIP mới → mở dataset checkpoint → **New Version/Create New Version**
→ thay nội dung bằng snapshot mới → lưu/chờ xử lý. Trong notebook, cập nhật input
checkpoint sang dataset version mới (Update to latest hoặc gỡ/gắn lại nếu cần).
Giữ nguyên version của core data. Kiểm đường dẫn/plan ID/số task complete lại.

## 6. Phiên official 3 và các phiên sau

```python
RESUME_FROM = "/kaggle/input/<snapshot-moi-nhat>"
MAX_NEW_TASKS = 1
EXPORT_FEATURES_IN_ZIP = True
```

Giữ MAX_NEW_TASKS=1 lúc bắt đầu các job GPU nặng; tăng2–3 sau khi đã quan sát thời
gian và dung lượng thực. Không có thời gian cố định cho một job.

Với MODEL_IDS=[35M], OVERRIDES={} và snapshot đầy đủ, thứ tự tiếp theo:

| Batch minh họa | Job mới dự kiến |
|---|---|
| 1, giới hạn2 | 00,01 |
| 2, giới hạn3 | 02-esm2_35m,03-esm2_35m,04 |
| 3, giới hạn1 | 05-pointwise-B-s17 |
| 4, giới hạn1 | 05-pointwise-D-s17 |
| Các batch sau | Các job05 còn lại →06→11→08→09→07 |
| Cuối mỗi batch | Tổng hợp10, trạng thái và xuất snapshot |

Kế hoạch mặc định có48 task: 27 job05,12 job11 và9 job khác; route tổng hợp10 không
tính vào MAX_NEW_TASKS. Đây là số job lập kế hoạch, không phải số thí nghiệm đã đo.
Nguồn: [session-plan-example.json](session-plan-example.json).

Một job05 chạy cả one-hot/ESM cho một head/arm/seed qua5fold. Một job11 chạy một
mode/arm/seed qua5fold. MAX_NEW_TASKS=1 không có nghĩa chỉ một epoch hoặc một fold.
SESSION_HOURS kiểm **giữa job**, không tự ngắt job đang chạy; một job vẫn có thể
vượt thời gian phiên. Nếu riêng một job không vừa, cần điều chỉnh cách chia runner;
không tự giảm epoch/grid rồi tiếp tục dưới cùng campaign.

Lặp đúng vòng: **Save & Run All → kiểm Output → lấy snapshot mới → cập nhật checkpoint
dataset/input → RESUME_FROM mới → Save & Run All**. Chỉ dùng snapshot đã xác nhận
là mới nhất. Không chọn snapshot dựa vào điểm MAE/AUROC cao hơn.

## 7. Tham số nào được đổi?

| Có thể đổi giữa các phiên của cùng campaign | Giữ nguyên để resume |
|---|---|
| RESUME_FROM theo snapshot mới | SMOKE=False |
| MAX_NEW_TASKS | MODEL_IDS, FINETUNE_MODEL |
| SECTIONS để chọn nhóm trong phiên | OVERRIDES, CALIBRATION_TASK |
| SESSION_HOURS, MAX_OUTPUT_GIB trong quota thật | Core data và mã embedded |
| EXPORT_FEATURES_IN_ZIP | Source/structure inputs và SAPROT settings |

Giữ OUTPUT_ROOT="" và EXTRA_WEIGHT_ROOTS=[] như ví dụ để các đường dẫn cấu hình
ổn định. Notebook tự tìm weights trong /kaggle/input; không cần thêm đường dẫn cho
mỗi version. Giữ INSTALL_DEPENDENCIES=True và Internet On cho background mới.

Không phục hồi source snapshot vào campaign đã có trong cùng /kaggle/working.
Save & Run All tạo phiên sạch nên phù hợp cho resume input. Nếu chạy tay tiếp trong
phiên hiện tại còn campaign local, để RESUME_FROM="" để dùng cache local. Restart
kernel chỉ xóa RAM, không bảo đảm xóa thư mục working. Không xóa checkpoint để né assert.

## 8. Feature, storage và các lỗi thường gặp

**Nếu dùng checkpoint ZIP làm input, giữ EXPORT_FEATURES_IN_ZIP=True.** Giá trị False
làm ZIP nhỏ hơn nhưng bỏ pool.npy/crop.npy. Phiên sau sẽ trích lại feature và tính
việc đó là một job mới; với MAX_NEW_TASKS=1 có thể chỉ lặp trích feature mà chưa
tới head mới. Nếu trước đây dùng False, đổi sang True có thể phải trích lại feature một lần rồi snapshot mới sẽ giữ chúng. Restore full output directory cũng giữ feature, không cần ZIP feature.

Nếu export báo archive_skipped_storage_budget: output directory vẫn còn. Dùng
thư mục campaign đầy đủ từ version đã lưu, hoặc tải/zip riêng thư mục đó thành input.
Không tăng budget vượt quota thật chỉ để tạo bản ZIP trùng dữ liệu. Pretrained weights
không có trong checkpoint ZIP; AUTO_DOWNLOAD=True sẽ tải lại khi một job mới cần chúng.

| Hiện tượng | Cách xử lý |
|---|---|
| Chạy lại00/01 | Kiểm snapshot có phải official và mới nhất; code/config/đường dẫn có đổi không |
| Chỉ trích lại03 mỗi phiên | Snapshot thiếu pool/crop; dùng feature ZIP hoặc full directory |
| Changed scientific plan/code/data | Giữ cấu hình gốc, hoặc chấp nhận campaign mới; không bỏ assert |
| Resume only into an empty campaign directory | Dùng Save & Run All mới; nếu cùng phiên local thì RESUME_FROM="" |
| Input chỉ có snapshot cũ | Cập nhật dataset version đã gắn; kiểm lại task complete và plan ID |
| weights_pending/resource_blocked | Đọc lý do tài nguyên/weights; không coi đó là hiệu năng model |
| waiting_dependency | Hoàn tất nhóm trước; giữ SECTIONS=None nếu muốn tự nối toàn luồng |
| Phiên lỗi/ngắt trước cell export | Chỉ resume từ artifact thực sự được lưu; không giả định RAM/checkpoint chưa Save đã được giữ |

Khi hoàn thành core, planned/complete đạt48/48 cho ví dụ mặc định; đọc thêm outcome.
08/09 vẫn có thể là source_pending/structure_pending khi chưa có input thật. Không
tự coi các scientific gates đã đóng vì job queue hết. Toàn bộ official GPU vẫn cần
người dùng chạy/kiểm kết quả; các kiểm chứng trong repo là CPU smoke và archive resume.

Nguồn hành vi nền tảng: [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks),
[Kaggle Datasets — ZIP được giải nén](https://www.kaggle.com/docs/datasets).
