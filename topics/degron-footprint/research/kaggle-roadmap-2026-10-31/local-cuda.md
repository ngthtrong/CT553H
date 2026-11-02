# Môi trường local CUDA cho v3

Chạy thí nghiệm nhiều phiên với terminal Windows: [local-runner.md](local-runner.md).

**[ĐO] Cập nhật 02/11/2026:** Đã cài wheel Torch `2.13.0+cu130` từ cache vào `.venv` riêng của repo và cài dependency theo `requirements-local-cuda-reuse.txt`. [readiness.json](run-local-2026-11-02/readiness.json) đạt `status=pass`, `ready_for_esm35_training=true`, `official_jobs_started=false`. CUDA, dữ liệu/splits, Ridge, inference ESM35 và update frozen/LoRA/checkpoint resume đều qua kiểm tra. Hai môi trường nguồn không bị sửa; lượt tải Torch2.11 dở vẫn được giữ nguyên. Xem [reuse-local-cuda.md](reuse-local-cuda.md); các lệnh Torch2.11 bên dưới chỉ dành cho phương án giữ đúng phiên bản Torch gốc của Kaggle.

Môi trường riêng ở `.venv/` của repository, Python 3.11.9 trên Windows. Runtime đang dùng được ghim tại [requirements-local-cuda-reuse.txt](requirements-local-cuda-reuse.txt); phương án Torch gốc của Kaggle ở [requirements-local-cuda.txt](requirements-local-cuda.txt). Các dependency còn lại kế thừa [requirements-kaggle.txt](requirements-kaggle.txt). Không dùng Python toàn cục để chạy tiếp campaign.

**Đầu vào đã khôi phục:**

- Core ZIP: `topics/degron-footprint/data/processed/packages/degron-data-v3-fullpsi.zip`.
- Data root đã giải nén: `topics/degron-footprint/data/processed/degron-data-v3-fullpsi/`.
- Data manifest SHA-256: `b0376e05d690d991c95143d6122b5418e457318394da032928d0d1e53f914738`, trùng data identity của lượt Kaggle `369cb2fe6a1e31e0`.
- Weights ESM2-35M: `output/weights/esm2_35m/6fbf070e65b0b7291e7bbcd451118c216cff79d8/`, có `status.json` complete và đủ checksum; không cần tải lại.
- Output/checkpoint cũ: `output/official/369cb2fe6a1e31e0/`. Không ghi đè để chạy kiểm môi trường.

Lệnh từ gốc repository (PowerShell), khi cần dựng lại môi trường:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r topics/degron-footprint/research/kaggle-roadmap-2026-10-31/requirements-local-cuda.txt
```

Chạy kiểm tra sẵn sàng:

```powershell
.\.venv\Scripts\python.exe -I topics/degron-footprint/research/kaggle-roadmap-2026-10-31/check-local-cuda.py --requirements topics/degron-footprint/research/kaggle-roadmap-2026-10-31/requirements-local-cuda-reuse.txt
```

Sau khi chạy, kết quả sẽ ở `run-local-2026-11-02/readiness.json`. Chỉ coi môi trường đã đạt khi `status=pass` và `ready_for_esm35_training=true`. Script kiểm:

1. Dependency/version và `pip check` trong đúng interpreter.
2. CUDA thực: phép nhân ma trận, backward và gradient hữu hạn.
3. Checksum data, nhãn saturation, 15 tổ hợp seed/fold và nhóm train/validation/test không giao nhau; scan_dev/scan_T tách khỏi saturation. Không đánh giá hiệu năng trên T.
4. Load một Ridge checkpoint đã kiểm hash và đối chiếu dự đoán với OOF đã lưu.
5. Checksum pretrained weights, tokenizer đúng 28 residue, inference ESM35 FP16 trên GPU.
6. Một batch 8 mẫu thuộc train, 28 AA, FP32 cho frozen và LoRA: forward/backward/optimizer update, gradient và tham số LoRA có thay đổi; đo peak VRAM.
7. Đọc checkpoint LoRA-B/seed17/fold0 đang dở, khôi phục adapter/head và optimizer rồi thử một update trong RAM. Không ghi lại checkpoint.

Các phép đo là kiểm chức năng/tài nguyên với một batch, không phải hiệu năng dự đoán, thời gian full run hay hoàn tất một official job. Báo cáo ghi rõ `official_jobs_started=false`.

**Khi chuẩn bị chạy tiếp:** Dùng các đường dẫn local trên thay `/kaggle/...`, chạy preflight trên runtime hiện tại và giữ nguyên các tham số khoa học nếu tiếp tục recipe cũ. Python/OS/GPU khác Kaggle nên không bảo đảm tiếp diễn giống từng bit. Nội dung runner hiện tại khớp bản embedded Kaggle khi chuẩn hóa newline, nhưng hash byte CRLF/LF và đường dẫn trong config khác nhau; orchestration cần cấu hình resume riêng để tái sử dụng artifact có kiểm chứng, tránh vô tình chạy lại job đã xong hoặc giả cùng signature.

Môi trường này phục vụ nhánh ESM2-35M. Stage08/09 vẫn cần nguồn ngoài/mapping cấu trúc thật; CNN final refit/export vẫn là phần triển khai riêng. Không suy từ readiness của 35M sang khả năng chạy mọi checkpoint lớn. Nhật ký giải nén dữ liệu nằm trong [data/README.md](../../data/README.md).
