# Kiểm chứng v3 — 01/11/2026

## Kiểm output local hoàn tất — 06/11/2026

[analyze-local-output.py](analyze-local-output.py) ghi [local-output-analysis.json](local-output-analysis.json), [báo cáo](local-output-analysis.md) và hình tổng hợp. Đã kiểm size/SHA toàn bộ artifact của 633 job complete, giữ nguyên trạng thái nguồn kế thừa, đối chiếu đủ OOF ba seed và nhãn/fold với bundle; tái tính metric ensemble, phép so frozen–LoRA, Brier ba lớp và kết quả T. Kiểm lại artifact Kaggle làm nguồn tham chiếu; không coi hai platform là mẫu độc lập. Nguồn/hash và dung sai đối chiếu nằm trong JSON. Các helper metric được dùng lại từ runner, không gọi đây là một implementation metric độc lập.

Campaign đã kết thúc, còn `source_pending`/`structure_pending`; LoRA chưa có locked T hoặc final serving export. Phần bên dưới giữ các mốc kiểm thử trước đây, không thay thế phân tích hoàn tất này.

## Trạng thái đối chiếu ngày 03/11/2026

**Sửa tokenizer local sau khi dừng an toàn:** [validate-tokenizer-repair.py](validate-tokenizer-repair.py) và [tokenizer-repair-validation.json](tokenizer-repair-validation.json) ghi kiểm alignment 532 phép thay/model, token ID khớp artifact gốc, không token lạ, từ chối chiều dài sai; preflight CUDA và delta embedding batch 8 đạt cho ProtT5 FP16/Ankh FP32. FP16 của Ankh từng tạo hidden state không hữu hạn trong preflight, nên FP32 là cấu hình khai báo riêng, không phải fallback âm thầm sau OOM. Hai phép kiểm này không đánh giá hiệu năng ΔPSI.

Kiểm kế thừa từ chối thay dữ liệu/protocol/train hoặc artifact hỏng; giữ nguyên source và byte checkpoint. LoRA CUDA trên mẫu nhỏ tiếp tục qua thư mục successor cho tham số khớp lượt liên tục (max abs 0). Đã chạy lại [local-runner-validation.json](local-runner-validation.json): frozen/LoRA pause–resume, khôi phục checkpoint dự phòng, khóa tiến trình, feature prefix và DAG đều đạt. Successor `ef138c84579c842e` kế thừa 456 job và một checkpoint paused qua manifest riêng; không đổi model sản phẩm/G2/G3. Các notebook embedded và code ZIP cũ chưa được dựng lại.

Các mục bên dưới giữ **bản ghi kiểm thử CPU ngày 01/11**, trước khi nhập/phân tích output GPU. Những câu “chưa chạy official/Kaggle GPU” chỉ áp dụng tại mốc kiểm thử đó.

- Output Kaggle full-data đã được nhập: [output-analysis.json](output-analysis.json) và [output-analysis.md](output-analysis.md) ghi kiểm artifact/OOF và giới hạn snapshot, không thay bằng chứng smoke.
- CUDA local đã qua readiness ngày 02/11: [readiness.json](run-local-2026-11-02/readiness.json). `official_jobs_started=false` trong file này mô tả riêng lượt chẩn đoán môi trường.
- Campaign Windows sau readiness đã có các job Ridge/frozen/LoRA hoàn tất và job còn dở; xem [snapshot 03/11 và nguồn state/queue](../README.md). [local-runner-validation.json](local-runner-validation.json), [local-ridge-validation.json](local-ridge-validation.json), [local-collection-validation.json](local-collection-validation.json) là kiểm phần mềm bằng mẫu nhỏ, không phải benchmark full-data.
- Chưa hoàn tất tổng hợp/calibration/locked-transfer của campaign local; chưa có nguồn ngoài/mapping cấu trúc thật hoặc final promotion tự động cho CNN/LoRA/family. G2/G3 vẫn mở.

## Bản ghi smoke CPU ngày 01/11

**[ĐO] 12/12 notebook đã execute từ đầu tới cuối trên CPU ở SMOKE mode**, bằng nbclient/kernel `.venv`, output được lưu và export HTML. Notebook gốc sạch, notebook đã execute/HTML/model/PNG tại `data/processed/v3-validation/verified/`. [notebook-validation.json](notebook-validation.json) ghim SHA của từng file gốc, trạng thái, thời gian và số PNG inline. Stage08/09 pass là nhánh pending được xử lý đúng khi thiếu nguồn/cấu trúc.

## Bằng chứng đã có

- Dataset ZIP98.748.031 byte; CRC và toàn bộ file SHA khớp manifest. Bảng full-PSI/split/WT/replicate/nguồn có thật; không ghi đè bảng lịch sử. [dataset-build.json](dataset-build.json).
- Tái lập historical Ridge: base **0.8081859035**, ext4 **0.8208223589**, nằm trong dung sai1e-4. Đây là tái lập số cũ, không phải kết quả xác nhận mới. File gốc `.../verified/results/smoke/00-*/legacy-reproduction.json`.
- Invariants: kiểm15 tổ hợp seed/fold không giao nhóm; T held_source; feature không đổi khi thay metadata PSI/label/fold; trọng số E cân bằng strata/peptide; merge shard kích thước lệch và row reorder đúng; overlap/smoke vào official/config resume thay đổi bị chặn. [invariant-validation.json](invariant-validation.json).
- Stage02 ESM2-8M thật: tokenizer đúng28 residue, mutation positions1/2/14/27/28, finite/repeated forward. Stage03 ESM2-35M thật trích pooled/crop trên12 ô smoke.
- Stage01 fit Ridge mới; 05 fit6 head/one-hot-fixture recipes; 06 fit Ridge và CNN scratch/pretrain/fine-tune. Không dùng các điểm này làm bằng chứng hiệu năng.
- Stage11 train **ESM2-8M thật + nhãn ΔPSI thật**, armsB/D, frozen/LoRA, seed17/fold0/epoch1. Frozen head44.929 trainable parameters; LoRA+head106.369. Mỗi LoRA arm cập nhật24 tensor adapter; các checkpoint mới được lưu và SHA ghim trong [training-smoke.json](training-smoke.json). Không gọi đây là pretrain từ đầu hoặc full-data benchmark.
- Stage07 đã fit calibrator/refit W5 và test held-source trên smoke; stage10 tổng hợp đúng identity/mode. Full inference/final refit cho CNN/LoRA/family chưa được triển khai tự động.
- 10 notebook có biểu đồ inline; 08/09 pending chỉ có bảng/trạng thái. Ảnh được lưu như `summary.png`; kiểm trực tiếp nhãn/không clipping/SMOKE marker và đơn vị. HTML đã export; chưa kiểm toàn bộ HTML trong trình duyệt (môi trường không có browser), kiểm nội dung/ảnh render riêng.
- Model registry pin20 revisions; complete weights được đối chiếu hash, các file tải dở không load được. [weights-status.json](weights-status.json) là snapshot, có thể cũ hơn tiến trình tải nền; chạy `weights_status.py --verify` để cập nhật.

## Giới hạn còn lại

**Chưa chạy official trên Kaggle/GPU**, chưa có bằng chứng CUDA/VRAM/throughput cho mọi family/scale hoặc hiệu năng model mới trên full W. Local environment ghi trong từng `env.json`; image Kaggle cần kiểm lại dependency/runtime. Các model lớn chưa có dispatch/offload/quantization adapter.

Không có external table mới được tải/audit hoặc structure bundle thật; nhánh SaProt conditional chưa được execute với true3Di. Chưa có ensemble5 ESM1v chuyên biệt, W5-neural blend, learning curve mạng, phân tích sâu20/360 cặp hoặc final promotion tự động ngoài W5. Các công việc này được giữ rõ trong coverage và RUN, không coi là đã làm nhờ có notebook.

Gói code được dựng sau kiểm chứng, có CODE_MANIFEST và protocol hash. Sau bất kỳ sửa code/protocol nào cần rebuild/reconnect Kaggle dataset version và restart kernel; không bypass hash/fold gates. Các scientific gates G2/G3 giữ mở.

## Notebook tổng tự chứa bổ sung 01/11

[ĐO] `12-all-in-one.ipynb` đã thực thi các cell tuần tự bằng IPython CPU: lượt dừng
sau2 job và lượt resume ZIP chạy các route còn lại đều pass.11 task + route tổng hợp
bao phủ12 notebook đơn; source/structure ghi pending khi thiếu input. ESM2-8M thật
được trích feature và train frozen/LoRA trên nhãn ΔPSI thật. Kiểm tiếp ZIP không có
feature: trích lại feature, dùng lại head/LoRA đã train; changed plan bị từ chối.
Bằng chứng: [all-in-one-validation.json](all-in-one-validation.json).

Môi trường sandbox không cho socket Jupyter; lượt nbclient không khởi động được.
Một lượt yêu cầu quyền đã timeout ở bộ duyệt tự động. Kiểm CPU hoàn tất bằng IPython
không cần TCP kernel, có notebook outputs/HTML/PNG/ZIP thật. Vì vậy không gọi đây là
lượt Save & Run All đã xác minh trên Kaggle. Biểu đồ summary đã xem trực tiếp; HTML
đã export/parse, chưa xem toàn trang bằng browser. Official GPU/CUDA vẫn chưa chạy.

Master giữ runner gốc và protocol, bổ sung task signatures/input-feature hashes,
cache theo artifact SHA, soft budget, download khi cần và resume. Không đổi core data
hoặc các scientific gates. ZIP code mới có13 notebook (12 đơn + master), còn master
có mã embedded nên không cần gắn code dataset riêng.

## Snapshot qua Kaggle Dataset nhiều phiên

[ĐO] Hai vòng actual bootstrap→export ZIP→giải nén→bootstrap đều giữ feature,11 task
smoke đã xong và nguyên campaign ID, không chạy thêm job huấn luyện. Mỗi ZIP có đúng
một SNAPSHOT.json mới. File index import được bootstrap giữ trong resume-indexes;
embedded runner SHA vẫn là3e0b8aeb7e20a752dc030a67bdef7f2546df3f6a35d854ba8e8f26f24c81d738.
Bằng chứng: [multi-session-validation.json](multi-session-validation.json). Notebook
được execute lại CPU/IPython, budget stop và ZIP resume đều pass; chưa chạy Kaggle GPU.
Hướng dẫn [MULTI-SESSION.md](MULTI-SESSION.md) dùng EXPORT_FEATURES_IN_ZIP=True cho
checkpoint dataset để tránh lặp trích feature khi giới hạn một job mỗi phiên.

## Sửa input gzip đã giải nén — 01/11

[ĐO] Kiểm hồi quy bằng `validate_data_transport.py`: bundle gzip gốc, cả sáu
member đã giải nén, và input hỗn hợp đều qua SHA; identity/bảng saturation/scanning
khớp bản gốc. Thiếu FASTA/Parquet, nội dung giải nén bị sửa, manifest khác và gzip
hỏng dù còn bản giải nén đều bị từ chối. Đã chạy bootstrap embedded của notebook
mới và stage00 với layout input lồng như log Kaggle. Bằng chứng:
[data-transport-validation.json](data-transport-validation.json).

Registry SHA nội dung được dựng từ ZIP core hiện có sau kiểm SHA ZIP và từng gzip;
không sửa core ZIP hoặc manifest. Notebook mới nhúng registry và runner đã sửa,
vì vậy embedded SHA khác bản kiểm snapshot nhiều phiên ở trên. Kết quả smoke/resume
của bản mới nằm trong [all-in-one-validation.json](all-in-one-validation.json).
Việc Kaggle đã giải nén file là chẩn đoán phù hợp với log, chưa xác minh qua danh
sách input thật; kiểm hồi quy cục bộ không thay thế lượt chạy lại trên Kaggle/GPU.
