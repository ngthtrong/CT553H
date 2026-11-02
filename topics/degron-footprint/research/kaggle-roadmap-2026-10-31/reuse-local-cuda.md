# Dùng Torch CUDA sẵn có cho repo — 02/11/2026

Chạy thí nghiệm nhiều phiên với terminal Windows: [local-runner.md](local-runner.md).

**[ĐO] Đã thiết lập xong môi trường repo ngày 02/11/2026.** Torch `2.13.0+cu130` được cài từ wheel cache đã kiểm SHA-256 vào `.venv` riêng, cùng dependency theo `requirements-local-cuda-reuse.txt`. [readiness.json](run-local-2026-11-02/readiness.json) có `status=pass`, `ready_for_esm35_training=true`, `official_jobs_started=false`. Xem [kết quả và giới hạn](run-local-2026-11-02/README.md). Hai môi trường nguồn không bị sửa.

**Trạng thái trước khi tiếp tục:** Torch 2.11 CUDA12.8 tải dở khoảng 54,8% theo các range hoàn tất; file `.incomplete` cùng state vẫn giữ tại `.venv/wheelhouse/`, không sử dụng cho lượt cài này. Trước lượt cài, `.venv` repo chỉ có pip/setuptools.

**[ĐO] Cả hai môi trường được kiểm trực tiếp bằng Python 3.11.9:**

| Python environment | Torch / CUDA | RTX 5060, matrix forward/backward |
|---|---|---|
| `D:\ctut_chatbox_kiot_main\.venv` | 2.13.0+cu130 / 13.0 | pass |
| `D:\Taiwan Cat and Dog\From-CNN-to-Bioinformatic\1.Explore_CNN\.venv` | 2.7.1+cu128 / 12.8 | pass |

Đã chọn bản 2.13.0+cu130. Runtime này khác bản Kaggle 2.11.0+cu128; ESM35/checkpoint và dependency đã được kiểm trên môi trường repo trong báo cáo readiness ở trên. Không bảo đảm tiếp diễn giống từng bit giữa hai runtime.

**[ĐO] Wheel CUDA 2.13 đầy đủ trong pip cache** có **1.915.488.103 byte**, tag **cp311-cp311-win_amd64**. SHA-256 đã đối chiếu đúng với index chính thức PyTorch: `45e97bd9bc0416f4f4190b5098c55119a389fa5a7c8bbf2639f08f1d04e0a0dc`. Đường dẫn/hash ở [cached-cuda-wheel.json](cached-cuda-wheel.json). Đã sao chép wheel vào repo, kiểm lại size/hash và cài thành công.

Không chuyển nguyên `.venv` của dự án khác: script/pip/activation có thể chứa đường dẫn tuyệt đối. Dùng wheel cache để cài lại vào `.venv` của repo sẽ giữ hai dự án độc lập. Tài liệu Python: https://docs.python.org/3/library/venv.html#how-venvs-work.

**Các lệnh dưới đây ghi lại cách cài đã dùng**, từ PowerShell tại `D:\thanhtrong\CT553H`. Lệnh copy chỉ sao chép cache, không di chuyển/xóa môi trường nguồn.

```powershell
Set-Location -LiteralPath 'D:\thanhtrong\CT553H'
$taskResearch = 'topics/degron-footprint/research/kaggle-roadmap-2026-10-31'
$taskWheelInfo = Get-Content -LiteralPath "$taskResearch/cached-cuda-wheel.json" -Raw | ConvertFrom-Json
$taskWheel = Join-Path '.venv/wheelhouse' $taskWheelInfo.filename
Copy-Item -LiteralPath $taskWheelInfo.cache_path -Destination $taskWheel
if ((Get-FileHash -LiteralPath $taskWheel -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskWheelInfo.sha256) { throw 'Wheel checksum mismatch' }
```

Repo đã có `.venv` Python3.11 nên không cần chuyển `python.exe`, `Scripts/` hay `site-packages/` từ dự án khác. Nếu dựng lại ở máy khác, phải có wheel đúng Python/platform và môi trường mới tương ứng.

Sau đó cài vào đúng môi trường repo:

```powershell
.\.venv\Scripts\python.exe -m pip install "$taskWheel" -r "$taskResearch/requirements-local-cuda-reuse.txt"
.\.venv\Scripts\python.exe -m pip check
```

Torch lấy từ file local, không tải lại wheel CUDA. **Các dependency nhỏ còn thiếu vẫn có thể được tải từ PyPI**, gồm pandas/pyarrow/transformers5.17/accelerate1.15 và các thư viện khác theo requirements. Không dùng `requirements-local-cuda.txt` trong phương án này vì file đó ghim Torch2.11+cu128. Bản reuse ghim Torch2.13+cu130 và giữ các phiên bản số học quan trọng theo Kaggle.

Kiểm GPU và toàn bộ điều kiện local:

```powershell
.\.venv\Scripts\python.exe -I -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
.\.venv\Scripts\python.exe -I "$taskResearch/check-local-cuda.py" --requirements "$taskResearch/requirements-local-cuda-reuse.txt"
```

Chỉ sau khi báo cáo `run-local-2026-11-02/readiness.json` có `status=pass` và `ready_for_esm35_training=true` mới coi repo đã đủ điều kiện cho nhánh 35M. Script kiểm dữ liệu/splits, GPU, inference ESM35 và một batch update frozen/LoRA/checkpoint resume trong RAM; không chạy job official. Không cam kết tiếp diễn giống từng bit giữa Kaggle và runtime 2.13/Windows/RTX5060.

Data core đã giải nén và qua 32 checksum, cùng manifest SHA với Kaggle. Weights ESM35 có sẵn, qua đủ sáu checksum. Stage08/09 vẫn cần nguồn ngoài/mapping cấu trúc thật; readiness môi trường không thay thế các điều kiện khoa học đó.
