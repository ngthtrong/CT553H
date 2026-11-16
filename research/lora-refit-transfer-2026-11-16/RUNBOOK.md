# Vận hành refit Windows — 16/11/2026

**Bổ sung Koren 16/11:** File S4 đã có và khớp hash; `run-local.cmd` nay qua
launcher mỏng `session-entry.py`, vẫn gọi nguyên runner đã khoá để resume cùng
checkpoint. Sau core/finalize, launcher tự gọi `score-koren.py` trong cùng
terminal, cùng OS locks/STOP. Không có scheduler/GPU worker song song và không
thay byte code/protocol/state/queue của campaign core đang dở.
`status-local.cmd` in thêm trạng thái bổ sung Koren. Kết quả riêng là
`koren-results.json`/`koren-run-status.json`; job source_pending trong queue cũ
là lịch sử giữ nguyên, không phải trạng thái mới của phân tích bổ sung.
Protocol: [KOREN-PROTOCOL.md](KOREN-PROTOCOL.md), kiểm thử: [koren-validation.json](koren-validation.json).

Runner hiện có đã hỗ trợ `refit_transfer_v1`. Default của `run-local.cmd` là
`refit-plan.json` ở đây. Không gọi config v3 cũ để chạy refit.

## Chạy, xem, tạm dừng

Từ `D:\thanhtrong\CT553H` trong PowerShell:

```powershell
.\run-local.cmd --hours 0
.\status-local.cmd
.\pause-local.cmd
```

`--hours 0` chạy đến khi hàng đợi hết việc hoặc có lỗi/pause. Mặc định nếu không
truyền hours là phiên 2 giờ. Các file cmd mở terminal riêng. Giữ máy thức và
cắm nguồn; không sửa code `degron_v3/`, `local-runner.py`, config/protocol/source
lock, packages hoặc driver trong lúc campaign đang chạy.

Để chỉ rõ target, thay ID bằng giá trị từ latest/status:

```powershell
.\status-local.cmd --campaign <campaign-id>
.\pause-local.cmd --campaign <campaign-id> --wait --timeout 300
```

Pause mặc định chờ checkpoint và xác nhận OS locks của supervisor/worker đã
được thả. Timeout trả lỗi, không phải xác nhận đã pause. Ctrl+C trong terminal
run cũng yêu cầu pause an toàn. Sau PAUSED/SESSION ENDED có thể chạy lại cùng
`run-local.cmd --hours 0` để resume. Không sửa state/manifest bằng tay.

Đóng terminal đột ngột/mất điện có thể mất phần chưa commit; runner dùng hai
thế hệ checkpoint và prediction prefix. Không khởi chạy hai GPU worker; OS
lock từ chối session trùng. Failed dừng campaign mới; đọc lỗi trước khi dùng
`--retry-failed`, không tự đổi batch/precision/epoch.

Nếu muốn status trong chính terminal đang mở:

```powershell
.venv\Scripts\python.exe -I research\kaggle-roadmap-2026-10-31\local-runner.py status
```

## Chuẩn bị lại khi code/runtime thay đổi

Không dùng quy trình này để ép checkpoint cũ nhận code mới. Code đổi dẫn tới
campaign mới. Thứ tự khi chưa có campaign đang chạy:

```powershell
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\prepare-refit.py
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\validate-refit-plan.py
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\validate-analysis.py
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\preflight.py --scope core
.\run-local.cmd --hours 0
```

Preflight/validator CUDA dùng cùng session/worker locks để không chạy GPU cạnh
campaign thật. Scope `branch1` hiện bị từ chối rõ vì Koren thiếu dữ liệu/adapter
chiều dài. Scope core là cho phép chạy toàn phần công việc khả dụng, không phải
tuyên bố toàn nhánh đã đủ điều kiện nghiệm thu.

## Output và giới hạn

Output mới: `research/kaggle-roadmap-2026-10-31/output/local/<id>/`.
Nguồn `ef138c84579c842e` và `e7097449883a51d8` chỉ đọc.

15 job đầu là core. Queue còn parity/model card, diagnostic, Koren pending,
3 hình và manifest. Nếu mọi việc khả dụng chạy xong, dự kiến 19 complete và
1 source_pending; điều đó **không phải hoàn thành toàn nhánh 1**. Diagnostic
similarity/causal mechanism chưa đầy đủ và D-4 vẫn phải ghi outstanding.

Khi aggregate/completion xong, báo cáo nhỏ xuất cạnh runbook này:
`results.json`, `model-card.json`, `parity-results.json`, `error-results.json`,
`error-strata.csv`, `figures/`, `acceptance-results.json`, `handoff-manifest.json`.
Đây là development/post-hoc transfer; không tự đóng G2/G3 hoặc đổi serving.

Checkpoint, arrays, Parquet, calibrator và logs vẫn ignored. Chỉ commit file
nhẹ đã review khi Trọng yêu cầu; chạy guard trước commit:

```powershell
.venv\Scripts\python.exe -I research\lora-refit-transfer-2026-11-16\check-git-staging.py
```

Copy thủ công theo manifest sau pause/idle; kiểm SHA sau copy. Không copy
`.git`/`.venv`; không đẩy model/data lên Git chỉ vì cần chuyển máy. Báo cáo
`launch-status.json` là snapshot vận hành, xem status/state để biết tiến độ mới.
