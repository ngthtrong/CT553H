# Chạy local nhiều phiên, terminal Windows

**06/11/2026: campaign `ef138c84579c842e` đã kết thúc 633 job complete, còn hai trạng thái nguồn ngoài/cấu trúc pending.** Kết quả, kiểm artifact/OOF và giới hạn kết luận ở [local-output-analysis.md](local-output-analysis.md). Chạy lại cùng kế hoạch chỉ kiểm/bỏ qua công việc đã xong; hai nhánh pending cần đầu vào được review và triển khai riêng. Các snapshot tiến độ ngày 03/11 dưới đây giữ vai trò lịch sử. Giữ cả campaign nguồn và successor để đọc artifact kế thừa.

Đối chiếu tiến độ 03/11/2026 tại [chỉ mục/snapshot nghiên cứu](../README.md). Hướng dẫn này mô tả cách vận hành; số job complete/blocked và job đang dở phải đọc từ campaign hiện tại, không suy từ các kiểm thử phần mềm ở cuối file.

**Sửa tokenizer 03/11/2026:** ProtT5 cần `protobuf==6.33.5` để đọc/chuyển SentencePiece; Ankh dùng `tokenizer.json` gốc qua `PreTrainedTokenizerFast`, đầu vào tách residue. Ankh base có activation không hữu hạn ở FP16 trong lượt preflight sửa lỗi, nên chính sách đã khai báo là **encoder FP32**, lưu feature FP16; các model khác giữ precision trước đây. Cả hai đã đạt preflight CUDA, alignment 532 phép thay và batch 8; bằng chứng ở [tokenizer-repair-validation.json](tokenizer-repair-validation.json). Đây chưa phải metric benchmark.

Campaign kế tiếp **`ef138c84579c842e`** được tạo lúc 12:38 ngày 03/11 (UTC+8), từ cấu hình `inherit_completed_from` trong [local-plan.json](local-plan.json). Nó kế thừa **456 job hoàn tất** bằng tham chiếu artifact có kiểm SHA, và sao chép checkpoint của `tune-lora-B-17-2` đang paused. Campaign nguồn `e7097449883a51d8` giữ nguyên; không sửa identity trong tensor/checkpoint. `inheritance.json` ghi nguồn, hash plan/state, phạm vi kiểm tương thích và namespace checkpoint. Hai model sửa lỗi được reset probe/extract/Ridge; các bước tổng hợp sẽ chạy lại với tập ứng viên đầy đủ.

Chỉ lượt sửa lỗi đã được kiểm này được phép kế thừa; dữ liệu, protocol, cấu hình train/selection và runtime số học phải khớp (chỉ thêm protobuf). Bộ kiểm từ chối thay đổi khoa học hoặc artifact hỏng. Không dùng cơ chế này như cách bỏ qua fingerprint cho thay đổi bất kỳ. Để resume/tổng hợp, phải giữ **cả thư mục campaign nguồn và campaign mới**, cùng weights; không xóa nguồn sau khi thấy campaign mới có state.

**02/11/2026:** Bộ điều phối dùng `.venv` Python3.11/Torch2.13+cu130 của repo. Nó giữ output Kaggle làm tham chiếu chỉ đọc, chạy chiến dịch local riêng cho khảo sát pLM và đối chứng frozen–LoRA cùng runtime. Kiểm phần mềm dùng mẫu nhỏ không phải scientific benchmark.

Từ thư mục gốc repo, double-click **`run-local.cmd`** hoặc gọi trong PowerShell:

```powershell
.\run-local.cmd
.\run-local.cmd --hours 8
.\run-local.cmd --profile models --hours 2
.\run-local.cmd --profile core --hours 2
```

Mỗi lần gọi mở **cửa sổ terminal mới**, chạy Python `-u -I` đúng `.venv`. Mặc định `--profile all --hours 2`. Cửa sổ vẫn mở sau khi dừng; tiêu đề đổi thành SESSION ENDED. `--hours 0` bỏ giới hạn thời gian. Chỉ một supervisor và một GPU worker được giữ khóa; gọi trùng không tạo hai job GPU. Không cần giữ chat/notebook mở khi terminal đang chạy; máy vẫn phải hoạt động.

**Dừng an toàn:** nhấn Ctrl+C trong terminal đang chạy, hoặc double-click `pause-local.cmd`. Chờ PAUSED/SESSION ENDED rồi mới đóng cửa sổ. Lần sau gọi `run-local.cmd` để tiếp tục. `status-local.cmd` mở cửa sổ xem trạng thái và tiến độ gần nhất. Giới hạn giờ là mềm: PCA/Ridge đang fit hoặc một request mạng có thể cần hoàn tất trước khi dừng.

Nếu đóng cửa sổ đột ngột/mất điện, dùng checkpoint đã ghi. Train checkpoint khoảng120giây một lần, sau optimizer step; có model/optimizer, epoch, cursor trong permutation, RNG Python/NumPy/Torch/CUDA, best validation và early stopping. Hai thế hệ checkpoint giúp khôi phục khi bản mới hỏng. Inference/feature lưu prefix theo đoạn; Ridge tiếp tục cấp fit/fold. Phần tính chưa commit có thể chạy lại. Tham số resume đã khớp lượt liên tục trên mẫu kiểm frozen và LoRA thật; không bảo đảm bitwise cho mọi kernel GPU hoặc giữa các nền tảng.

**Chiến dịch và dữ liệu:**

- Cấu hình chốt trước chạy ở [local-plan.json](local-plan.json): 9 pLM, arm B/D, seed 17/29/43, 5 outer folds.
- Frozen pLM: ESM2 8M/35M/150M/650M, ESM1b 650M, ESM1v 650M `_1`, ESM-C 300M, ProtT5 encoder, Ankh base. Cùng Ridge/PCA64 head, có/không context W5; nested recipe chọn bằng inner MSE.
- Fine-tuning: chỉ ESM2-35M, frozen và LoRA, cùng batch8/FP32/lr1e-4/epoch tối đa20/patience4, refit theo inner epoch. Có60đơn vị fold, gồm chạy lại frozen seed17 trên local để đối chứng phù hợp với LoRA local.
- Tổng635đơn vị công việc (540 Ridge fold,60 fine-tune fold,27bước weights/preflight/features và các bước nhập/tổng hợp/hiệu chuẩn). Đây không phải635model độc lập.
- Preflight kiểm tokenizer 28 residue, forward hữu hạn, revision/checksum và VRAM trước khi dùng nhãn. Thiếu tài nguyên/adapter không phù hợp ghi resource_blocked/adapter_blocked; nhánh phụ thuộc ghi skipped_resource. Lỗi fit sau preflight ghi failed, không được âm thầm loại ứng viên khỏi kết luận.
- Weights 8M/650M lấy từ ZIP đã có; 35M từ output đã nhập. Weights khác tải theo revision đã pin, giữ `.partial` và SHA. Không tải/chạy remote Python. Giới hạn allocator GPU 75%, ngân sách local 50 GiB và chừa30GiB đĩa; không tự đổi precision/batch train sau lỗi.

**Đường dẫn kết quả:**

```text
output/local/
  latest.json                    chỉ mục chiến dịch hiện tại
  session.lock, worker.lock       khóa do OS quản lý
  weights/                       weights dùng chung, pin revision và checksum
  <campaign-id>/
    plan.json, queue.json         cấu hình và DAG cố định
    state.json, progress.json     trạng thái nguyên tử, tiến độ gần nhất
    sessions/<session>.log        log từng phiên
    logs/<job>.log                log tích lũy theo công việc
    jobs/<job>/                  checkpoint, feature, OOF và metadata
    inheritance.json             nguồn artifact/checkpoint nếu là successor đã kiểm
```

`complete` chỉ ghi sau khi worker xong và hash artifact được lưu. Khởi động lại kiểm file hoàn tất; artifact thay đổi khiến hệ thống dừng để kiểm tra. Code/data/registry/protocol/runtime (kể cả driver) đổi tạo campaign khác; không sửa manifest để ép nhận checkpoint. Output cũ được giữ nguyên. Job failed chỉ thử lại khi gọi `run-local.cmd --retry-failed`, sau khi kiểm nguyên nhân. Không có retry vô hạn.

Trong successor đã kiểm, job complete có `artifact_campaign` trong state: file thật nằm ở campaign nguồn, không được sao chép và đếm thành kết quả mới. Chỉ checkpoint đang paused được sao chép để tiếp tục ghi riêng trong successor. `run-local.cmd` dùng kế hoạch hiện hành và tự tiếp tục successor; không cần thêm cờ retry để khôi phục hai nhánh tokenizer đã reset.

**Lưu kết quả trên GitHub:** `.gitignore` ở gốc repo chỉ cho phép các bằng chứng nhỏ trong `output/local/`:

- Mỗi campaign: `plan.json`, `queue.json`, `state.json`, `superseded.json`/`inheritance.json` nếu có; trạng thái lỗi/blocked, nguồn kế thừa và hash artifact được giữ để giải thích phạm vi kết quả.
- JSON ngay dưới từng job: metadata fit/preflight, revision lock, manifest feature, `worker-result.json`, kết quả đánh giá, collection/comparisons và evidence/pending. `collect-*/summary.csv` và `report/benchmark.csv` được giữ khi các bước tổng hợp hoàn tất.
- Trong recipe của `calibrate-core` và `locked-transfer-w5`: `selection-lock.json`, `model-card.json`; weights dùng chung chỉ giữ `SOURCE.md` và `status.json` chứa revision/SHA.

Weights, checkpoint (kể cả `.previous`/`.tmp`), feature NumPy, bảng OOF/calibration/held-scanning Parquet, download `.partial`, log, khóa, STOP, `latest.json`, `session.json` và progress cấp campaign vẫn ở local. Output Kaggle `output/official/` tiếp tục bị bỏ qua; các bản phân tích nhỏ `output-analysis*.json`/`.md` bên cạnh runner vẫn được Git theo dõi như trước. File mới ngoài danh sách cho phép mặc định bị bỏ qua. Không dùng `git add -f output/` vì sẽ vượt các quy tắc này.

GitHub chỉ lưu bằng chứng và báo cáo; clone repo không đủ để resume hay tính lại metric từ OOF. Cần giữ bản sao đầy đủ output ở nơi lưu trữ riêng. `state.json`/`worker-result.json` có thể tham chiếu các artifact không nằm trong Git. Commit kết quả sau khi terminal báo PAUSED/SESSION ENDED để snapshot trạng thái nhất quán; campaign đang dở có thể chưa có bảng tổng hợp.

`.gitignore` không kiểm tra kích thước và không tác động lên file đã tracked hoặc lịch sử commit. Trước khi commit, sau khi stage các file cần lưu, chạy kiểm tra sau từ gốc repo trong PowerShell. Ngân sách chủ động là tối đa 10 MiB/file và 25 MiB tổng file staged (kích thước chưa nén, không phải kích thước gói push); script dừng nếu vượt để xem lại thay vì tự thêm file nặng:

```powershell
@'
import subprocess

names = subprocess.check_output(
    ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMRT', '-z']
).split(b'\0')
sizes = []
for raw in filter(None, names):
    name = raw.decode('utf-8')
    size = int(subprocess.check_output(['git', 'cat-file', '-s', ':' + name]))
    sizes.append((size, name))
total = sum(size for size, _ in sizes)
large = [(size, name) for size, name in sizes if size > 10 * 2**20]
for size, name in sorted(large, reverse=True):
    print(f'OVER BUDGET: {size / 2**20:.2f} MiB {name}')
print(f'Staged: {len(sizes)} files, {total / 2**20:.2f} MiB')
raise SystemExit(1 if large or total > 25 * 2**20 else 0)
'@ | .venv\Scripts\python.exe -I -
```

Thứ tự: kiểm output Kaggle → weights/preflight/features/Ridge từng pLM → frozen/LoRA 35M → tổng hợp → calibration CV → locked transfer W5-D → bảng benchmark chung. Profile `models`/`core` chỉ chọn việc chạy trong phiên, không thu nhỏ kế hoạch khoa học. Transfer T chờ cả hai nhánh development; kết quả T không dùng chọn model. Nguồn ngoài và cấu trúc ghi pending khi chưa có đầu vào.

`collect-family` tổng hợp OOF đầy đủ và nested selection; `collect-core` có paired bootstrap 5000 theo nhóm cho LoRA−frozen. `report/benchmark.csv` giữ platform và seed, không đếm lại output như dữ liệu độc lập. Calibration mạng hiện là CV; final refit/export CNN/LoRA/family để phục vụ vẫn riêng. Held-source evaluation tự động là recipe **W5-D đã chốt trước**, không phải T cho mọi pLM mới.

Kiểm chứng: [local-runner-validation.json](local-runner-validation.json), [local-ridge-validation.json](local-ridge-validation.json), [local-collection-validation.json](local-collection-validation.json). Kiểm resume bằng `.venv\Scripts\python.exe -I topics/degron-footprint/research/kaggle-roadmap-2026-10-31/validate-local-runner.py`; không tạo OOF official trong các kiểm thử nhỏ.
