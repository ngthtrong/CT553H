# Kiểm môi trường CUDA local — 02/11/2026

**[ĐO]** [readiness.json](readiness.json) đạt `status=pass`, `ready_for_esm35_training=true`. Interpreter: `D:\thanhtrong\CT553H\.venv\Scripts\python.exe`, Python 3.11.9, Torch 2.13.0+cu130, CUDA 13.0, RTX 5060 Laptop GPU. `pip check` không phát hiện dependency hỏng. Wheel Torch lấy từ cache local và kiểm lại size/SHA-256 theo [cached-cuda-wheel.json](../cached-cuda-wheel.json); không tải lại wheel Torch, không sửa hai môi trường nguồn.

Các kiểm tra đạt trong báo cáo:

- CUDA matrix forward/backward và gradient hữu hạn.
- 32 checksum dữ liệu, data identity trùng Kaggle; 15 tổ hợp seed/fold có nhóm train/validation/test tách biệt; scan_dev/scan_T tách khỏi saturation.
- Ridge artifact khớp dự đoán OOF trên 8 mẫu, sai lệch tối đa 0.
- Weights ESM35 đủ checksum; tokenizer đúng 28 residue; GPU inference FP16 đạt.
- Một batch 8 mẫu train, FP32: frozen, LoRA mới và LoRA khôi phục checkpoint epoch 12 đều forward/backward/update thành công. Peak allocated VRAM lần lượt khoảng 203, 410 và 412 MiB; đây chỉ là bộ nhớ tensor do Torch đo trên batch này.

`official_jobs_started=false`; không ghi checkpoint từ các update chẩn đoán, không chạy official training. Runtime khác Kaggle Torch 2.11+cu128; kernel attention backward có cảnh báo không deterministic. Không bảo đảm tiếp diễn giống từng bit, không suy từ một batch sang throughput/bộ nhớ full run. Log Transformers có các key `lm_head` dư khi nạp backbone ESM; các kiểm tokenizer/inference/update vẫn đạt.

Stage08/09 vẫn cần nguồn ngoài/mapping cấu trúc thật. Orchestration resume campaign và CNN final refit/export là công việc riêng.

Evidence: [log cài](install-cuda-reuse.log), [log readiness](readiness-console.log), [package đã cài](installed-packages.json), [preflight](preflight.json), [readiness](readiness.json). [environment-reuse-audit.json](environment-reuse-audit.json) là bản ghi lịch sử trước lượt cài; trạng thái hiện tại nằm trong readiness.
