# Kaggle v3 — full-PSI, khảo sát pLM và huấn luyện model mới

**Rà nghiệm thu 07/11:** [hồ sơ G2 hiện hành](../g2-acceptance-2026-11-07/README.md)
ghi nhận bằng chứng LoRA cải thiện trong development và phần quyết định còn
chờ; chưa ghi nhận đóng G2. [Tra cứu bằng chứng wet lab/nguồn lực](../wet-lab-evidence-plan-2026-11-07/findings.md)
đã ghi tiền lệ bên ngoài và giới hạn claim CT553H; không có thí nghiệm mới.
Các snapshot và kết quả bên dưới giữ mốc riêng.

**Rà soát và đưa vào luận văn 06/11:** [audit toàn bộ output](../output-review-2026-11-06/README.md), [JSON 88 cấu hình](../output-review-2026-11-06/results.json), [luận văn và PDF](../../report/README.md). Bản audit chỉ đọc, bổ sung kiểm kê vật lý, epoch/chi phí và nguồn hash; không tạo một lượt huấn luyện mới.

**Cập nhật 06/11/2026:** local `ef138c84579c842e` đã hoàn tất **633 job**, còn nguồn ngoài/cấu trúc pending. [Phân tích local hoàn tất](local-output-analysis.md), [JSON bằng chứng](local-output-analysis.json) và [biểu đồ](local-output-analysis.png) kiểm artifact, đủ OOF ba seed, pLM/Ridge, frozen–LoRA, calibration CV và locked T W5-D. Chưa đóng G2/G3 hoặc thay model sản phẩm. Các mục ngày 03/11 bên dưới là snapshot lịch sử, không còn là trạng thái chạy hiện tại.

**Trạng thái 03/11/2026:** đã có output Kaggle full-data được nhập và [phân tích ngày 02/11](output-analysis.md); campaign CUDA Windows mở rộng pLM/frozen–LoRA đang dở. [Chỉ mục nghiên cứu](../README.md) ghi snapshot local và phần còn thiếu. Chưa hoàn tất pipeline hoặc đóng G2/G3. Bộ công cụ có 12 notebook đơn và notebook tổng; 12/12 notebook đơn từng qua smoke CPU. Bằng chứng dựng/kiểm gói: [dataset-build.json](dataset-build.json), [notebook-validation.json](notebook-validation.json), [weights-status.json](weights-status.json), [code-build.json](code-build.json); các file này có mốc riêng, không thay trạng thái campaign.

**Cập nhật tokenizer local lúc 12:38 (UTC+8):** ProtT5 và Ankh đã qua kiểm tokenizer/GPU/batch 8 sau sửa lỗi. ProtT5 dùng FP16; Ankh base khai báo encoder FP32 vì FP16 tạo embedding không hữu hạn. Campaign successor `ef138c84579c842e` giữ 456 job hoàn tất và checkpoint LoRA của nguồn, đưa hai nhánh bị chặn trở lại hàng đợi. Xem [hướng dẫn kế thừa/resume](local-runner.md), [kiểm chứng](tokenizer-repair-validation.json) và [inheritance.json](output/local/ef138c84579c842e/inheritance.json). Chưa có kết quả chất lượng dự đoán mới của hai model tại mốc tạo successor. Notebook embedded/code ZIP cũ chưa được dựng lại trong lượt sửa local này.

Mục tiêu là benchmark/phương pháp/đánh giá/phần mềm. Không cần kiến trúc mới hoặc bắt buộc mạng thắng Ridge. Dữ liệu saturation dự đoán **ΔPSI của đột biến đơn mức residue**, không đổi thành phân loại peptide. Phạm vi chỉ dữ liệu, model và thực nghiệm; không triển khai app/UX hay phần luận văn trong gói này.

## Bắt đầu

**Máy Windows đang dùng:** xem [local-runner.md](local-runner.md), [local-cuda.md](local-cuda.md) và [local-plan.json](local-plan.json). Từ gốc repo gọi `run-local.cmd`, `status-local.cmd`, `pause-local.cmd`; dùng `.venv` CUDA hiện có. Campaign local ghi `output/local/<campaign-id>/`, giữ output Kaggle `output/official/369cb2fe6a1e31e0/` làm tham chiếu chỉ đọc. Không gộp OOF giữa hai runtime thành mẫu độc lập.

**Chạy trên Kaggle:** các hướng dẫn notebook dưới đây vẫn dùng để dựng/chạy lại; xem [MULTI-SESSION.md](MULTI-SESSION.md) nếu cần chia phiên và resume.

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

## Kết quả đã có và phần tiếp theo

[output-analysis.json](output-analysis.json) ghi snapshot Kaggle `369cb2fe6a1e31e0`: 35 task complete, một task dở, 47 recipe từ 83 file OOF. [Phân tích chi tiết](output-analysis-details.md) tách fold, cặp thay thế và learning curve; không dùng số smoke để báo hiệu năng. Snapshot chưa có stage07/08/09/10 cuối, LoRA chưa đủ OOF.

Campaign local là mở rộng development sau khi biết kết quả Kaggle, theo kế hoạch 9 pLM và đối chứng ESM2-35M frozen–LoRA cùng runtime. Một số adapter bị chặn; số hoàn tất/blocked và job đang dở ở [snapshot hiện hành](../README.md). Chờ tổng hợp, calibration và locked-transfer theo DAG; T được chốt cho W5-D, không dùng T chọn mọi pLM mới. CNN/LoRA/family cần final refit/export riêng trước phục vụ. Phạm vi phần mềm vẫn ở [system/](../../system/README.md).
