# Audit dữ liệu RCAEval cho lựa chọn đề tài

Audit index đầy đủ và sáu ca thô xác định trước, không huấn luyện hay chấm mô hình. [Quyết định đề tài](../../research/topic-decision.md) và [báo cáo khảo sát](../../../../../surveys/open-field-topic-selection-2026-10-12.md).

## Nguồn và tái lập

- Dataset: <https://huggingface.co/datasets/phamquiluan/RCAEval>, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, metadata MIT.
- Repo thuật toán đối chiếu: <https://github.com/phamquiluan/RCAEval/tree/259ea4167160256a74ad30004aa3d96a998c846e>.
- Index SHA-256: `c49a288920dbba2e8e724679a14636d5c7eb2b8b45426bba14007ef79a6c0ab1bb`.
- Script đối chiếu kích thước/SHA file thô với metadata LFS ở revision cố định; manifest nằm trong raw cache bị Git bỏ qua.

Từ root repository, với virtual environment đã có:

```bash
.venv/bin/python -m pip install -r archive/topics/budgeted-microservice-rca/code/preprocessing/requirements-audit.txt
.venv/bin/python archive/topics/budgeted-microservice-rca/code/preprocessing/audit_data.py
```

Lần đầu cần mạng tới Hugging Face; lần sau tái sử dụng file nhưng vẫn kiểm SHA và truy vấn metadata ở revision. Không cam kết offline hoàn toàn. Input tại `archive/topics/budgeted-microservice-rca/data/raw/` không commit; kết quả nhỏ [results/data-audit.json](results/data-audit.json) có thể kiểm tra vào Git. Thời gian đọc trong JSON thay đổi theo máy/cache, không phải benchmark hiệu năng.

## Kết quả ngày 12/10/2026

735 ca trong index; 360 ca RE2/RE3; 359 có logs và 240 có traces. Không gọi mọi ca là đa nguồn đầy đủ. Sáu mẫu là ca đầu theo tên trong mỗi `(suite RE2/RE3, system OB/SS/TT)`; xác định trước bằng index, không chọn theo hiệu quả mô hình. Tải 49.463.299 bytes gồm index; đã đọc schema, đếm dòng và đối chiếu injection/normal window. Mẫu không đánh giá tất cả 735 ca.

Nhãn nguyên nhân do fault injection; tên case chứa đáp án. `root_service`, loại lỗi, tên file/case và `root_cause.txt` chỉ dành cho audit/huấn luyện có giám sát/chấm kết quả; phải tách khỏi inference. Script không tải `root_cause.txt`. **Chỉ năm dịch vụ có nhãn mỗi hệ RE2**; pipeline phải giữ mọi dịch vụ quan sát được trong tập ứng viên. Mọi rollout/window cùng một ca và replica cùng kịch bản phải giữ cùng fold; manifest chia chưa được tạo trong audit này.

Kiểm soát prior dịch vụ phải dùng train-only và có đối chứng không đọc telemetry. [Audit Buljić 09/2026](https://arxiv.org/html/2609.27069v1) đã có cả RE1 và RE2 Sock Shop; audit bộ RE2 mới ở repo này không tự tạo tính mới khoa học.

Đọc mẫu lớn nhất khoảng 230 MB DataFrame trace khả thi trên máy hiện tại. Upstream khuyến nghị 16 GB RAM; chưa chạy pipeline/baseline hoàn chỉnh nên không suy ra mọi cấu hình vừa máy. Chưa cài toàn RCAEval, chưa tái lập BARO/TORAI/EventADL, chưa download OpenRCA. Audit là bằng chứng dữ liệu truy cập và xử lý mẫu được, không phải bằng chứng G2 hay sản phẩm sẵn sàng.
