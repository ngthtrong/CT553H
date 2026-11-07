# Kiểm chéo và dựng lại

[ĐO] Kết quả từng kiểm nằm ở [validation.json](validation.json), sinh bằng [validate.py](validate.py). Mỗi số chính trong README có bảng `readme_number_ledger`, JSON nguồn và đường dẫn khóa. Số G2 là phép đọc/tính lại artifact sẵn có, không phải train lại trong audit này.

## Kiểm độc lập đã thực hiện

- [ĐO] Đếm bảng 302 bằng csv chuẩn và pandas; đối chiếu supplementary bằng openpyxl riêng. Đếm 240 accession/HUMAN bằng set và hậu tố độc lập. Schema/missing/duplicate: [dataset-audit.json](dataset-audit.json).
- [ĐO] Tái dựng footprint lịch sử và tên 249 saturation/31 CRISPR từ nguồn; phân biệt giao accession, exact tile và khoảng tọa độ. HIF1A có kiểm PSI WT từ median native-AA hai nửa; không dùng PSI scanning cho nhãn bão hòa. [overlap-audit.json](overlap-audit.json).
- [ĐO] Tái tính ΔPAP/ridge macro AUROC trực tiếp từ NPZ trên 91 peptide/89 cụm, so JSON cũ; không chỉ chép số từ README. [validation.json](validation.json).
- [ĐO] Baseline thành phần chạy đủ seed 17/29/43 ở cov80/cov50; kiểm lại seed 29 bằng một đoạn fit/readback riêng, xác nhận cụm train/test rời nhau. CI lấy mẫu 5.000 cụm ở seed 17 cho từng biểu diễn, không lấy ô/dòng độc lập. [composition-baseline.json](composition-baseline.json), [validation.json](validation.json).
- [ĐO] MetaDegron-X được so **từng repeat** với S5, ngoài việc khớp mean 0,9670. Tám giao β-TrCP với fitting population đếm cả bằng tập khóa và merge dataframe. Degpred 0,9540 chỉ tái tính từ score sẵn có. [safe-x-reproduction.json](safe-x-reproduction.json), [validation.json](validation.json).
- [ĐO] Kiểm SHA-256 từng file trong manifest; giữ nguyên hash mọi file đã dirty ở đầu phiên, giữ HEAD và kiểm đường dẫn mới trong phạm vi. Không đưa dữ liệu/trọng số/ảnh nguồn vào git. [baseline-worktree.json](baseline-worktree.json), [validation.json](validation.json).

## Lệnh từ gốc repo

```bash
# Chỉ khi cần dựng lại nguồn: clone riêng, checkout commit ghi trong source-manifest.json.
# Không chạy bất kỳ mã/notebook nào từ thư mục clone.
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py topics/degron-footprint/research/metadegron-analysis-2026-10-21/additional-sources.json
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py topics/degron-footprint/research/metadegron-analysis-2026-10-21/label-sources.json
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py topics/degron-footprint/research/metadegron-analysis-2026-10-21/elm-sources.json
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py topics/degron-footprint/research/metadegron-analysis-2026-10-21/manual-label-sources.json
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/fetch-sources.py topics/degron-footprint/research/metadegron-analysis-2026-10-21/candidate-sources.json
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/audit_dataset.py --stage all
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/safe-predict-x.py
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/review-labels.py
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/inventory-sources.py
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/write-report.py
.venv/bin/python -I topics/degron-footprint/research/metadegron-analysis-2026-10-21/validate.py
```

[ĐỌC-MÃ] Fetcher giữ cache, không ghi đè file nguồn. MMseqs2 cần trong PATH; tham số đầy đủ và phiên bản nằm trong [clusters.json](clusters.json). Nếu đổi FASTA/phiên bản/tham số, không tái dùng cache cluster cũ. Rerun nguồn live có thể thay ELM snapshot/website và metadata truy cập; giữ bản tải ghim để tái tạo đúng audit hiện tại.

## Giới hạn kiểm chứng

[CHƯA XÁC MINH] Chưa có điểm D zero-shot GPS/ma trận mutant, chưa có adjudication toàn bộ assay gốc cho mẫu nhãn. Không có API call hay validation web job mới. Việc khớp metric X trên bảng chuẩn bị sẵn không chứng minh generalization. Báo cáo không thay đổi quyết định đề tài/G2 và không đóng các cổng khoa học còn mở.
