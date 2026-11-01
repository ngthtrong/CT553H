# Dataset v3 đã dựng — hợp đồng thực thi 01/11/2026

[ĐO] ZIP: `topics/degron-footprint/data/processed/packages/degron-data-v3-fullpsi.zip`, **98.748.031 byte**. SHA-256: `f4a6542f3786de420108861975eae0c58534e5f60a529bce315de9d00bd872a8`. Xem [dataset-build.json](dataset-build.json). Dữ liệu giải nén tại `data/processed/v3-fullpsi/`, mỗi file được băm trong `DATA_MANIFEST.json` (schema3, role=core_data).

- `tables/{peptides,saturation-cells,scanning-cells,observations,wt-references,sequence-table,exclusion-log}.parquet`.
- `splits/wide-outer.parquet`, `inner-seed{17,29,43}.parquet`, `scanning-partitions.parquet`, legacy folds và cross-split-audit.
- `source-snapshots/`: PSI sát/scanning/WT và sequence map; `references/`: proteome/cụm; `historical/`: kết quả nhỏ + hai NPZ để tái lập số cũ.
- `build-audit/`: source manifest và protein hit evidence. Log MMseqs có đường dẫn tuyệt đối được giữ local, không vào ZIP.

Saturation: 235 peptide/122.412 ô/221 nhóm, PSI strata ≤3:91, (3,4]:85, (4,5]:36, >5:23 peptide. Scanning:224.470 ô union replicate; partitions theo peptide: sat_overlap1278, scan_dev5489, scan_T1414. 17 peptide scan không map proteome bị loại; 45 peptide sat thiếu cụm cũ map được qua proteome đầy đủ. Không thay dữ liệu/folds lịch sử. Chỉ nguồn Zhang/UniProt CC BY4.0; không chứa weights, feature, Koren/ClinVar/MetaDegron. Notebook dùng common splits và kiểm hash khi đọc.

Builder: `build_dataset.py` (đọc raw bằng Python isolated, chỉ chạy mã nghiên cứu tin cậy). Dựng mới cần MMseqs2 và nguồn trong repo; Kaggle chỉ cần ZIP đã dựng. Weights/cache thuộc assets riêng theo [RUN.md](RUN.md). Các con số thực thi được ưu tiên hơn ước tính trong đặc tả lịch sử dưới đây.

---

## Đặc tả thiết kế 31/10 giữ để truy nguyên

# Thiết kế dataset v3 dùng chung

**Đặc tả, chưa dựng bảng/ZIP.** Không sửa `residue_data.py` hoặc ghi đè cache cũ. Khi triển khai, thêm builder mới và cập nhật `data/README.md` cùng phiên tạo dữ liệu.

## 1. Nội dung gói

```text
degron-data-v3-fullpsi/
  DATA_MANIFEST.json
  README.md
  tables/
    peptides.parquet
    saturation-cells.parquet
    scanning-cells.parquet
    observations.parquet
    wt-references.parquet
    sequence-table.parquet
    exclusion-log.parquet
  references/
    proteins.fasta.gz
    clusters-legacy-cov80.tsv
    clusters-proteome-cov80.tsv
    clusters-cov50.tsv                 # sensitivity; phải kiểm phạm vi map
  source-snapshots/
    psi-sat_a.tsv.gz
    psi-sat_b.tsv.gz
    psi-rep1.tsv.gz
    psi-rep2.tsv.gz
    scanning-sequence-map.tsv.gz
  splits/
    legacy-outer.json
    wide-outer.parquet
    inner-seed17.parquet
    inner-seed29.parquet
    inner-seed43.parquet
    scanning-partitions.parquet
    cross-split-audit.json
  historical/
    g2-reference.json
    p0-reference.json
    r6-reference.json
```

Parquet là lựa chọn thiết kế; builder phải pin engine và schema. Có thể thêm CSV.gz để inspect, không duy trì hai phiên bản nhãn tính độc lập. `observations` chứa phép đo từng replicate; `*-cells` là view tổng hợp có liên kết provenance, không phải nguồn nhãn khác.

Gói lõi chỉ gồm nguồn Zhang và trình tự/cụm UniProt đã có provenance. Model weights, embedding, Koren, MetaDegron, Larsen và nguồn mới chưa qua audit không vào core. Gói external và structure có manifest riêng. Không đưa toàn bộ repo/PDF/thông tin cá nhân vào code bundle.

## 2. Schema và grain

| Bảng | Khóa / cột bắt buộc | Quy tắc |
|---|---|---|
| `peptides` | `peptide_id`, `accession`, `wt_sequence`, `length`, `sequence_sha256`, `coordinate_origin`, `protein_start_1based`, `protein_end_1based`, `psi_wt_sat`, `psi_stratum`, `legacy_cluster_id`, `proteome_cluster_id`, `mapping_status` | Một peptide; PSI là metadata không phải input. Origin phân biệt sequence CSV / canonical tile / source-supplied |
| `saturation-cells` | `cell_id`, `peptide_id`, `position_1based`, `wt_aa`, `mut_aa`, `dpsi_a`, `dpsi_b`, `dpsi_mean`, `psi_mut_a/b`, `reads_a/b`, `wt_reference_id_a/b`, `replicate_disagreement`, `source_id`, `assay_id` | Một phép thay thực đo, có hai nửa hợp lệ. Không suy nhãn cho ô thiếu |
| `scanning-cells` | cùng khóa sinh học + `dpsi_rep1`, `dpsi_rep2`, `dpsi_rep12_mean`, `availability_mask`, `reads_rep1/2`, WT reference IDs, `scan_pair`, partition | Giữ rep1-only, rep2-only và intersection riêng; không buộc mất hàng rep1 chỉ vì không có rep2 |
| `observations` | `observation_id`, `cell_id`, `source_id`, `replicate_id`, `condition_id`, `psi_mut`, `psi_wt`, `dpsi`, `read_sum`, `nb1..nb6`, `qc_status` | Một phép đo, không trộn replicate với condition. BAG6 WT không vào rep1/rep2 mean |
| `wt-references` | `wt_reference_id`, peptide/source/replicate, estimator, `psi_wt`, số ô đồng nghĩa, `reads`, IDs của ô tạo reference | Saturation: median đồng nghĩa từng nửa; scanning: `_mut0` của đúng replicate |
| `sequence-table` | `sequence_id`, `sequence`, SHA, peptide/cell mapping, role WT/mutant | Khử trùng chuỗi cho extraction nhưng không gộp hai phép đo khác nguồn |
| `exclusion-log` | source row/key, stage, rule, reason, count | Ghi drop-off từ dữ liệu thô đến bảng dùng cho từng arm |
| `splits` | peptide/group ID, protocol, outer fold, inner seed/fold role, partition, split SHA | Một nhóm sinh học không được đi qua train/test trong cùng split |

Ô WT→WT được lưu trong bảng reference/QC, không phải 532 đột biến và không dùng để làm phình metric. Dữ liệu dài 28 chuẩn AA mới vào core sequence model; stop, residue lạ và tọa độ không chắc được mask/loại có lý do. Vị trí là 1-based; tokenizer index là một trường riêng được test, không suy ra bằng cùng một offset cho mọi model.

## 3. Lọc kỹ thuật và views theo PSI

- Saturation: kế thừa reads≥10, ≥10 ô đồng nghĩa hợp lệ mỗi nửa, WT nội tại từng nửa, hai nửa ở cùng mutation cell, kiểm chuỗi/canonical như baseline. **Chỉ bỏ ngưỡng PSI; không bỏ QC**.
- `sat_le3`, `sat_le4`, `sat_le5`, `sat_all` là **views trên cùng bảng**, không dựng nhãn lại bốn lần.
- Giữ `sat_all` **235 peptide / 122.412 ô** làm kiểm kê kỳ vọng ở nguồn hiện tại; nếu thay nguồn/QC, ghi version và counts mới, không ép số bằng cách thêm hàng.
- Strata cố định: `le3`, `gt3_le4`, `gt4_le5`, `gt5`. Chỉ là strata đánh giá, không phải nhãn degron/non-degron thật.
- Các view full-balanced/quality-weighted chỉ đổi trọng số trong train; không dùng sample weight để thay đổi population của test một cách âm thầm.

## 4. Cụm, duplicate và hai protocol

**Legacy:** giữ bảng cụm/folds/input cũ phục vụ tái lập. Cách fallback accession thành group ở lịch sử không được dùng như bằng chứng mọi accession đã được phân cụm. Những so sánh train-full mới phải audit phạm vi map và ghi rõ nếu việc chặn thêm tương đồng làm đổi train so với mốc lịch sử.

**Wide:** dùng bảng toàn proteome đã có (đủ 235 peptide) làm xuất phát; kiểm exact WT/mutant sequence và hit protein/peptide xuyên split. Nếu cần nối nhóm trùng/hit thành connected components thì tạo bảng group mới, không sửa bảng cũ. **222 cụm là số kiểm kê trước bước nối thêm**, không phải lời hứa số nhóm cuối.

Chỉ cấp 5 outer fold khi còn đủ nhóm độc lập và phân bố có thể đánh giá. Cố định group trước khi xét nhãn mutation. Có thể cân bằng metadata stratum/số peptide khi cấp fold, nhưng phải lưu thuật toán/seed/assignment. Tạo inner train/validation riêng cho seed 17/29/43; không phân lại dựa trên AUROC. Kiểm legacy folds bằng assignment đã lưu, không phụ thuộc `GroupKFold` của phiên bản sklearn trên Kaggle.

Khử trùng sequence dùng cho chống leakage phải xét **trên hợp saturation + scanning**, không khử trùng từng file riêng. Nếu hai observation cùng sequence khác assay, giữ provenance và buộc cùng phía khi có nguy cơ học cùng construct.

## 5. Scanning và tập T

- `scan_all` hiện đọc được 8.063 peptide / 224.239 ô rep1 theo bộ lọc sequence/coverage của loader, **trước** QC ánh xạ cụm mới; không mặc định toàn bộ đủ điều kiện train/test.
- Bảng proteome hiện chưa map 17 peptide của view này. Không giả singleton; audit mapping/retrieve theo workflow nguồn hoặc loại có lý do. Legacy map cũng thiếu một số accession và không thể trộn hai bảng cluster bằng cách nối tùy tiện các representative IDs.
- Chọn phần T **trước** học có giám sát trên scanning; giữ ngoài mọi data selection, quality weighting fit, pretraining, fine-tuning và calibration.
- Để tận dụng dữ liệu, ưu tiên toàn bộ phần scanning ngoài saturation groups làm T cho **recipe chỉ học saturation**. Nếu nghiên cứu transfer dùng scanning, cần khóa một phân hoạch `scan_dev/scan_T` theo nhóm trong 00; chỉ phần dev được vào 06. Hai thiết kế có population T khác nhau phải báo riêng.
- Không dùng tham số `DATA_SCOPE='scan_T'` trong extraction đại trà lúc còn chọn model. Extract cho T sau khi freeze; unlabeled shared PLM checkpoint khác với dùng nhãn T để học.

## 6. Đặc trưng và weights không rò rỉ nhãn

- Input sequence-only: WT sequence, vị trí, mutant AA. Cấm `psi_wt_sat`, `psi_mut`, read count, group ID, fold ID và stratum làm input model chính.
- `full_balanced`: ở mỗi train fold, mỗi peptide có tổng trọng số bằng nhau trong stratum; mỗi stratum **có mặt trong train** có tổng trọng số bằng nhau. Chuẩn hóa mean weight=1, ghi effective sample size. Không thể gán trọng số cho strata vắng trong train≤3.
- `quality_weighted`: ước lượng mô hình/scale độ tin cậy chỉ trên train; khóa rule/cap bằng inner validation. Không dùng replicate của test để tạo feature/weight train. Bất đồng hai nửa là chỉ dấu, không phải phương sai được biết chính xác.
- Preprocessing/PCA/feature selection fit trong inner-train khi tuning; outer final fit chỉ trên outer-train thích hợp arm. Không PCA trên hợp toàn bộ train/test.

## 7. Cache pLM và dung lượng

Core không chứa embedding. Với **122.412 ô saturation**, float16, chưa nén:

| Hidden dim d | `[Δsite; mean Δ]` = N×2d | Crop Δ = N×15×d |
|---:|---:|---:|
| 480 | 0,219 GiB | 1,642 GiB |
| 1.280 | 0,584 GiB | 4,378 GiB |
| 2.560 | 1,167 GiB | 8,756 GiB |
| 5.120 | 2,335 GiB | 17,511 GiB |

Đây là phép tính kích thước mảng, **không phải benchmark runtime**; chưa gồm scanning, checkpoint, mask/IDs, file tạm và output. Chỉ lưu crop cho ESM35 và shortlist; không lưu crop của mọi model lớn. WT representation nhỏ được lưu một lần/sequence. Nạp crop bằng memmap/minibatch, không dùng đường R6 nạp toàn bộ nhiều crop vào GPU cho model lớn.

Mỗi shard có row IDs theo thứ tự, model revision/weights SHA, tokenizer revision, dtype, input scope, hidden layer, extractor SHA, data/split ID (khi liên quan), feature kind, complete bitmap và hash. Chỉ reuse nếu toàn bộ hợp đồng khớp. Kiểm readback trên probe và WT→WT=0; resume không chỉ dựa vào file tồn tại.

## 8. Những gói chưa được phép coi là đã có

- **Core v3:** builder, bảng và ZIP chưa triển khai.
- **Code v3:** runner 00–10, bootstrap chọn bundle bằng ID/hash, runtime locks và unit checks chưa triển khai.
- **Feature bundles:** chỉ sinh sau 02/03; không phải tải sẵn một gói embedding của người khác.
- **External bundle:** chỉ sau 08 audit schema/điều khoản/truy cập; giữ đơn vị và nguồn riêng.
- **Structure bundle:** cần map residue/chain/3Di/pLDDT từ cấu trúc đủ provenance; tám PDB audit cũ không mặc định đủ cho 235 peptide.
