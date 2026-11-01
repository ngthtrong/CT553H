
Bạn có thể giữ **một notebook Kaggle**, chạy thành nhiều **Save Versions**. Mỗi phiên sẽ đọc snapshot gần nhất, bỏ qua các job đã hoàn tất, chạy thêm vài job rồi xuất snapshot mới.

Tôi đã viết hướng dẫn đầy đủ tại [MULTI-SESSION.md](/home/ngthtrong/CT553H/topics/degron-footprint/research/kaggle-roadmap-2026-10-31/MULTI-SESSION.md). Hãy dùng **[notebook tổng bản hiện tại](/home/ngthtrong/CT553H/topics/degron-footprint/research/kaggle-roadmap-2026-10-31/notebooks/12-all-in-one.ipynb)**: tôi đã bổ sung xử lý snapshot sau khi Kaggle giải nén ZIP, giữ nguyên runner và mã campaign nên không yêu cầu huấn luyện lại các kết quả hợp lệ.

Nếu bạn **đã bắt đầu một campaign official**, giữ cấu hình khoa học cũ và đi tới bước khôi phục bên dưới. Cấu hình mẫu sau dành cho campaign mới.

1. **Chuẩn bị notebook và input**

   Import notebook tổng vào Kaggle, rồi gắn [dataset core v3](/home/ngthtrong/CT553H/topics/degron-footprint/data/processed/packages/degron-data-v3-fullpsi.zip).

   Bật **Internet** và chọn **GPU** cho chuỗi có pLM. Không cần dataset code hoặc weights riêng.

   Nếu chưa chạy smoke, có thể chạy một version với `SMOKE=True` trước. Khi chuyển sang official, bắt đầu campaign mới với `SMOKE=False` và `RESUME_FROM=""`.
2. **Phiên official đầu tiên: chạy audit và Ridge**

   Trong cell tham số có sẵn, đặt:

   ```python
   SMOKE = False
   INSTALL_DEPENDENCIES = True
   AUTO_DOWNLOAD = True

   MODEL_IDS = ["esm2_35m"]
   FINETUNE_MODEL = "esm2_35m"
   OVERRIDES = {}
   SECTIONS = None

   OUTPUT_ROOT = ""
   EXTRA_WEIGHT_ROOTS = []
   RESUME_FROM = ""

   MAX_NEW_TASKS = 2
   SESSION_HOURS = 8.0
   MAX_OUTPUT_GIB = 16.0
   EXPORT_FEATURES_IN_ZIP = True
   ```

   Giữ các biến khác ở mặc định.

   **`EXPORT_FEATURES_IN_ZIP=True` rất quan trọng khi chuyển phiên bằng checkpoint ZIP:** nó giữ feature để phiên sau không phải trích lại.

   Bấm **Save Version → Save & Run All**, đặt ghi chú như `official-batch-01`, rồi chờ hoàn tất. Lựa chọn này chạy từ đầu trong một phiên sạch; giữ bước cài dependency trong notebook. [Tài liệu Kaggle](https://www.kaggle.com/docs/notebooks).

   Với cấu hình trên, hai job mới dự kiến là:

   ```text
   RUN 00
   RUN 01
   ```

   Sau đó notebook dừng nhận job mới, tổng hợp và xuất snapshot. Các bước còn lại ở trạng thái `pending` hoặc `waiting_dependency` là bình thường.
3. **Lấy snapshot của phiên vừa hoàn tất**

   Mở **version đã lưu → Output**, tìm:

   ```text
   degron-v3-all/official/<plan-id>/pipeline-manifest.json
   degron-v3-all/official/<plan-id>/pipeline-status.csv
   degron-v3-all/official/<plan-id>-checkpoint.zip
   ```

   Ghi lại `<plan-id>` và tải file **`<plan-id>-checkpoint.zip`** của version này.

   Đây là snapshot tích lũy: phiên sau sẽ tiếp tục từ kết quả đã có trong snapshot.
4. **Mang snapshot sang phiên tiếp theo**

   Cách dễ theo dõi là tạo một private dataset tên chẳng hạn:

   ```text
   degron-v3-checkpoints
   ```

   Upload checkpoint ZIP vào dataset đó. Kaggle tự giải nén ZIP; trong dataset cần thấy `pipeline-manifest.json`, `tasks/`, `SNAPSHOT.json` và các file kết quả. [Tài liệu Kaggle Datasets](https://www.kaggle.com/docs/datasets).

   Trở lại notebook → **Add Input** → gắn dataset checkpoint.

   Nếu giao diện cho phép gắn trực tiếp **output version trước** làm input, bạn có thể dùng thư mục campaign đầy đủ để tránh tải/upload. Quy trình private dataset ở trên giúp bạn tiếp tục sử dụng cùng một notebook mà không phụ thuộc lựa chọn đó.
5. **Tìm đúng đường dẫn `RESUME_FROM`**

   Thêm một cell chỉ đọc sau cell tham số, chạy riêng cell này:

   ```python
   from pathlib import Path
   import json

   for path in Path("/kaggle/input").rglob("pipeline-manifest.json"):
       saved = json.loads(path.read_text())
       done = sum(
           item.get("status") == "complete"
           for item in saved.get("tasks", {}).values()
       )

       print("mode:", saved.get("plan", {}).get("mode"))
       print("plan_id:", saved.get("plan_id"))
       print("completed tasks:", done)
       print("RESUME_FROM =", repr(str(path.parent)))
       print()
   ```

   Chọn kết quả có:

   - `mode: official`;
   - đúng plan ID của campaign;
   - số task hoàn tất tương ứng snapshot mới nhất.

   Copy dòng `RESUME_FROM = ...` vào cell tham số. Giá trị phải trỏ tới **thư mục chứa `pipeline-manifest.json`**, không phải chính file JSON.
6. **Phiên official thứ hai: preflight, feature và head**

   Giữ nguyên cấu hình của phiên đầu, chỉ đổi:

   ```python
   RESUME_FROM = "/kaggle/input/.../thu-muc-snapshot-that"
   MAX_NEW_TASKS = 3
   EXPORT_FEATURES_IN_ZIP = True
   ```

   Thay đường dẫn minh họa bằng dòng vừa in ra.

   Bấm **Save Version → Save & Run All**, ghi chú `official-batch-02-resume`.

   Khi runtime và cấu hình phù hợp, bạn sẽ thấy:

   ```text
   CACHED 00
   CACHED 01
   RUN 02-esm2_35m
   RUN 03-esm2_35m
   RUN 04
   ```

   `CACHED` nghĩa là kết quả cũ đã được kiểm và dùng lại.

   Phiên này sẽ tự tải weights còn thiếu, trích feature và truyền chúng sang bước học head. Hết ba job mới, notebook tiếp tục tới phần báo cáo và xuất snapshot.
7. **Cập nhật checkpoint sau mỗi phiên**

   Sau phiên 2:

   1. Tải checkpoint ZIP mới từ Output.
   2. Mở dataset `degron-v3-checkpoints`.
   3. Chọn **New Version/Create New Version**, thay nội dung bằng snapshot mới.
   4. Chờ dataset xử lý xong.
   5. Trong notebook, cập nhật input checkpoint sang version mới bằng **Update to latest**, hoặc gỡ rồi gắn lại.
   6. Chạy cell kiểm tra đường dẫn và tiến độ lần nữa.

   **Đường dẫn input có thể giữ nguyên dù dataset đã đổi version.** Vì vậy, kiểm thêm plan ID và số task hoàn tất; đừng chỉ nhìn tên thư mục.

   Snapshot mới đã chứa kết quả tích lũy trước đó. Bạn thường chỉ cần gắn snapshot mới nhất đã xác nhận.
8. **Phiên thứ ba và những phiên sau**

   Đặt:

   ```python
   RESUME_FROM = "/kaggle/input/.../snapshot-moi-nhat"
   MAX_NEW_TASKS = 1
   EXPORT_FEATURES_IN_ZIP = True
   ```

   Bắt đầu với một job mới mỗi phiên khi tới phần GPU nặng. Sau khi biết thời gian thực tế, có thể tăng lên hai hoặc ba.

   Với cấu hình mặc định ESM‑2 35M, lịch sẽ tiến như sau:

   | Phiên minh họa       | Job mới                                                                    |
   | ---------------------- | --------------------------------------------------------------------------- |
   | Phiên 1, giới hạn 2 | `00`, `01`                                                              |
   | Phiên 2, giới hạn 3 | `02-esm2_35m`, `03-esm2_35m`, `04`                                    |
   | Phiên 3, giới hạn 1 | `05-pointwise-B-s17`                                                      |
   | Phiên 4, giới hạn 1 | `05-pointwise-D-s17`                                                      |
   | Các phiên tiếp      | Các job `05` còn lại → `06` → `11` → `08` → `09` → `07` |

   Cuối mỗi phiên đều có phần tổng hợp và xuất snapshot.

   Kế hoạch mặc định này có **48 task**, gồm 27 job head, 12 job fine-tuning và 9 job khác. Đây là số job được lập kế hoạch, chưa phải số thực nghiệm đã chạy. Chi tiết tại [session-plan-example.json](/home/ngthtrong/CT553H/topics/degron-footprint/research/kaggle-roadmap-2026-10-31/session-plan-example.json).

   **Một job không đồng nghĩa một epoch hoặc một fold.** Ví dụ, một job LoRA chạy một tổ hợp mode/arm/seed qua năm fold. `SESSION_HOURS` chỉ kiểm giữa các job; nó không tự ngắt job đang chạy.

Trong suốt chuỗi phiên, giữ nguyên `SMOKE`, `MODEL_IDS`, `FINETUNE_MODEL`, `OVERRIDES`, core data và mã embedded. Giữ `OUTPUT_ROOT=""` như ví dụ để đường dẫn ổn định. Bạn có thể thay `MAX_NEW_TASKS`, `SECTIONS` và ngân sách vận hành mà không đổi kế hoạch khoa học.

Hai trường hợp cần chú ý:

- **ZIP thiếu feature:** nếu giữ `EXPORT_FEATURES_IN_ZIP=False`, mỗi phiên có thể phải trích lại bước 03. Với giới hạn một job, bạn có thể chỉ lặp trích feature. Chuyển sang `True`; phiên đầu có thể trích lại một lần, rồi snapshot mới sẽ giữ chúng.
- **Campaign đã tồn tại trong phiên đang mở:** để `RESUME_FROM=""` nếu muốn tiếp tục cache local. Dùng **Save & Run All** cho lượt khôi phục từ input trong phiên sạch; restart kernel không bảo đảm xóa thư mục working.

Vòng thao tác cần lặp là: **Save & Run All → kiểm Output → lấy snapshot mới → cập nhật checkpoint dataset/input → đặt `RESUME_FROM` → Save & Run All**.

Tôi đã kiểm tra CPU việc chạy tiếp và hai vòng snapshot giải nén–xuất lại; chưa chạy toàn bộ official GPU trên Kaggle.
