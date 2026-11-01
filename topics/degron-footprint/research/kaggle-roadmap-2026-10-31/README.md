# Kaggle v3 — full-PSI, khảo sát pLM và huấn luyện model mới

**Trạng thái 01/11/2026: đã triển khai 12 notebook và runner, đã dựng dataset v3; 12/12 notebook đơn đã qua kiểm thử smoke CPU; đã bổ sung notebook tổng tự chứa và kiểm CPU/resume. Trạng thái weights ghi riêng theo snapshot.** Kết quả chính thức trên Kaggle chưa chạy. File số liệu: [dataset-build.json](dataset-build.json), [notebook-validation.json](notebook-validation.json), [weights-status.json](weights-status.json), [code-build.json](code-build.json).

Mục tiêu là benchmark/phương pháp/đánh giá/phần mềm. Không cần kiến trúc mới hoặc bắt buộc mạng thắng Ridge. Dữ liệu saturation dự đoán **ΔPSI của đột biến đơn mức residue**, không đổi thành phân loại peptide. Phạm vi chỉ dữ liệu, model và thực nghiệm; không triển khai app/UX hay phần luận văn trong gói này.

## Bắt đầu

**Có thể dùng một notebook duy nhất:** [12-all-in-one.ipynb](notebooks/12-all-in-one.ipynb) chứa sẵn runner, chỉ cần core data v3 + Internet để tải weights. Tự nối các bước, chia job/cache/resume qua Save Versions; xem [ALL-IN-ONE.md](ALL-IN-ONE.md). Các notebook đơn bên dưới vẫn được giữ.

Đọc [RUN.md](RUN.md), upload hai ZIP code/data trong `data/processed/packages/`, import notebook tại [notebooks/](notebooks/). **Notebook có huấn luyện model mới**:

- **01:** fit Ridge mới, arms PSI A/B/C/D/E, đối chứng ngữ cảnh và learning curve theo nhóm.
- **04:** fit Ridge/PCA head mới để so họ/cỡ pLM, chọn recipe bằng inner validation.
- **05:** train pointwise, CNN và mCNN từ đầu, one-hot hoặc frozen ESM feature.
- **06:** train Ridge có quality/source weighting; pretrain CNN bằng scanning rồi fine-tune saturation, kèm CNN scratch.
- **11:** train head với frozen backbone và **fine-tune pLM bằng LoRA**; tùy chọn full tuning ESM2-8M/35M. Checkpoint chứa tham số mới học, có kiểm tham số LoRA thực sự thay đổi.
- **07:** calibration/refit/export final W5; **09** có route fit head SaProt true/masked khi đã có mapping cấu trúc thật.

Pretrained pLM được dùng làm khởi tạo; gói này không pretrain pLM từ đầu. Default `SMOKE=True` kiểm hạ tầng. Đặt `SMOKE=False` để chạy đủ dữ liệu/fold/seed theo [EXECUTION-PROTOCOL.md](EXECUTION-PROTOCOL.md).

## Dataset và model

[ĐO] Builder v3 giữ **235 peptide / 122.412 ô saturation**, **224.470 ô scanning** sau QC/mapping, không lọc ngưỡng PSI. W có 221 nhóm protein sau hợp cụm/hits/sequence; splits và scan_dev/T được cấp trước fitting. ZIP **98.748.031 byte**, SHA và chi tiết tại [dataset-build.json](dataset-build.json). Chỉ dùng nguồn Zhang/UniProt đã có trong repo; không tạo phép đo mới. Xem [DATASET.md](DATASET.md).

20 checkpoint/7 họ: ESM2 8M/35M/150M/650M/3B/15B, ESM1b, 5 ESM1v, ESM-C 300M/600M/6B, ProtT5 encoder, Ankh base/large, SaProt35M/650M. [Registry](model-registry.json) đã pin revision; tải weights, adapter preflight và đánh giá task là ba trạng thái khác nhau. Model lớn cần GPU đủ RAM; runner hiện không tự sharding/offload/quantization.

## Tài liệu và giới hạn

[NOTEBOOKS.md](NOTEBOOKS.md) là ma trận thực thi. [EXECUTION-PROTOCOL.md](EXECUTION-PROTOCOL.md) là lựa chọn đang được runner dùng; [PROTOCOL.md](PROTOCOL.md) giữ bản thiết kế ban đầu chưa khóa. [MODEL-CATALOG.md](MODEL-CATALOG.md) ghi nguồn model. [VALIDATION.md](VALIDATION.md) ghi bằng chứng kiểm thử và phần chưa kiểm.

Nguồn ngoài/cấu trúc thiếu thì stage08/09 ghi `source_pending`/`structure_pending`; weights SaProt không thay mapping 3Di. Final promotion tự động hiện hỗ trợ W5; CNN/LoRA/family có model từng fold và calibration CV, cần final refit/export riêng trước phục vụ. Learning curve mạng và chẩn đoán sâu 20/360 cặp còn là bước bổ sung. Không gọi tạo notebook/smoke là hoàn tất G2/G3; không dùng số smoke để chọn model hay báo hiệu năng.

Chưa upload lên Kaggle, chưa thực hiện official GPU experiment. Các thay đổi presentation/system đang có sẵn được giữ nguyên.
