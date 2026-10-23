# Audit dữ liệu MetaDegron

## Cỡ dữ liệu và đơn vị nhãn

[ĐO] Bảng curate có **302 dòng**, **240 accession**, **241 chuỗi protein phân biệt**, **274 chuỗi motif phân biệt**, **302 khóa accession/start/end** và **31 loại motif/class**. Đây không phải 302 protein, không phải số nhãn ΔPSI, và không phải 31 E3. Cột nguồn có 166 ELM_TP, 93 signal, 16 natcancer, 13 natcomm, 9 natcancer,signal và 5 natcomm,natcancer,signal. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).

[ĐO] S2 và file repo khớp toàn bộ accession và chuỗi degron theo thứ tự. S2 có PMID nguồn nhưng thường là bài tổng hợp/resource, không phải PMID thí nghiệm riêng từng dòng. Không có cột kiểu thí nghiệm/PTM requirement có cấu trúc. Phân bố loài từ hậu tố Entry name: **227 HUMAN, 75 khác**; đây là kiểm metadata, chưa xác minh taxonomy hiện tại từng accession. Tiêu đề S2 nói dữ liệu người nên không được dùng tiêu đề thay phép đếm. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).

[ĐO] Chuỗi báo cáo dài **5–18 aa**, trong khi khoảng tọa độ dài **2–18 aa**. Có **243/302** dòng mà chuỗi cắt theo tọa độ khớp chuỗi báo cáo; cả **302/302** khoảng cắt đều nằm trong chuỗi báo cáo. Các motif ngắn có thêm flank trong chuỗi; không coi mọi chênh độ dài là sai tọa độ. Có **80** accession và **77** chuỗi protein khớp chính xác với `proteins-full.fasta`. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).

[ĐỌC-MÃ] Dòng curate là motif/đoạn gắn với protein, tọa độ 1-based inclusive, nguồn và class; không có nhãn thực nghiệm “mỗi phép thay AA”. `DEGRON=Known-INTERNAL` trong bảng thuộc tính là tên loại record, không phải chuỗi. UniProt hỗ trợ join accession nhưng phải kiểm isoform/chuỗi; một accession có nhiều chuỗi trong bản nguồn nên không join chỉ bằng số dòng.

[ĐO] Tập X có **212 dòng dương / 158 protein**, toàn bộ join được về danh sách curate theo accession/start/end. Nguồn âm file `data/simulated_degrons.tsv.gz` có **1.510 dòng / 1.457 accession**, còn **1.428** sau `CONS_SCORE>0` và drop missing; baseline chuỗi dùng **1.421** âm có chuỗi/tọa độ hợp lệ, loại **7** dòng không tái dựng được. Không tự điền chuỗi thiếu. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).

## Âm được dựng ra sao

[ĐỌC-MÃ] `Training_MetaDegron-X.py`: lấy 212 positives, lọc background như trên, sample **5×N có hoàn lại**, `random_state=2024509`, shuffle 42, StratifiedKFold 5 fold với RandomState 527. Đây là script CV X; nó không giữ riêng 10% holdout như script D. [Mã ghim](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Training_MetaDegron-X.py), [code-audit.json](code-audit.json).

[ĐO] Tái dựng đúng phép sampling này tạo **212 dương + 1.060 âm**, chỉ **748** hàng âm gốc phân biệt. Mỗi fold có **91–111** dòng test trùng khóa nhãn/accession/start/end với train. Đây là rò rỉ bản sao trong cách chạy script được cung cấp, chưa chứng minh số liệu bài báo được tạo bằng đúng script này. [composition-baseline.json](composition-baseline.json) → `author_x_sampling`; [audit_dataset.py](audit_dataset.py) → `sampling`.

[ĐO] Background là đoạn có accession/tọa độ trên protein thật: tái dựng được chuỗi cho các dòng đủ mapping. Histogram độ dài tọa độ âm đúng bằng 5 lần histogram dương toàn danh sách nhưng **dịch +1 aa**. Không có giao tọa độ chính xác với positive; có 14 protein chung. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).

[CHƯA XÁC MINH] Không tìm được vòng lặp tạo ban đầu từng tọa độ âm trong mã/notebook đã kiểm. `random.seed(2023)` và `N=5` trong code tính thuộc tính không đủ chứng minh thuật toán tạo âm. Vì vậy giả thuyết “peptide ngẫu nhiên” chỉ đúng ở mức sampled background theo tác giả; **không có căn cứ gọi là chuỗi amino acid tổng hợp i.i.d.** hoặc biết chính xác quy tắc loại motif thật. [code-audit.json](code-audit.json).

## Thành phần và độ dài có phân biệt được không?

[ĐO] Logistic L2 C=1, chuẩn hóa trên train, 5 fold theo cụm protein, seed 17/29/43; không oversample âm và không chọn C bằng test. Quần thể tái dựng là bảng X, không phải object-NPY training của D. Bảng dưới là OOF pooled AUROC, CI bootstrap 5.000 cụm ở seed 17; khác metric macro theo peptide của G2. [composition-baseline.json](composition-baseline.json), [PREREGISTRATION.md](PREREGISTRATION.md).

| Biểu diễn | cov80: seed 17 / 29 / 43 | CI95 seed17 |
|---|---|---|
| length | 0.5866 / 0.5869 / 0.5825 | [0.5323; 0.6388] |
| core-frequency | 0.7278 / 0.7276 / 0.7310 | [0.6885; 0.7684] |
| core-count-length | 0.7235 / 0.7211 / 0.7286 | [0.6838; 0.7629] |
| context29-frequency | 0.7461 / 0.7375 / 0.7467 | [0.7087; 0.7821] |

[DIỄN GIẢI] Thành phần có tín hiệu, song chưa đạt tiêu chí ≥0,75 ở cả ba seed; length-only dưới ngưỡng 0,65. Không được kết luận mô hình chỉ học thành phần, hoặc âm “dễ” hoàn toàn giải thích AUC công bố. Cửa sổ ngữ cảnh bằng độ dài vẫn có tín hiệu; phép so với AUC 0,87/0,90 chỉ là đối chiếu mức độ, không kiểm định ghép cặp cùng test. Kết quả cov50 và random 10% nằm trong JSON.

## Đồng dạng nội bộ

[ĐO] Phân cụm trên protein đầy đủ của các dòng dương tính, giữ các phiên bản chuỗi: **183 cụm cov80, 158 cụm cov50**. Dùng motif rất ngắn để gọi protein-homology sẽ không cùng điều kiện với G2. Tập hợp reference + positive + background có **8.333 record** và **5.793 / 4.969 cụm** tương ứng cov80/cov50. [clusters.json](clusters.json).

[ĐO] Khi mở rộng population, runner đọc lại **cả hai TSV cụm cũ** và ràng buộc mọi thành viên của mỗi cụm cũ phải cùng nhóm; không ghi lại TSV cũ hoặc đổi fold G2. Số cụm gốc, SHA và kiểm không tách nhóm được ghi trong [frozen-group-reuse.json](frozen-group-reuse.json). Baseline mới dùng nhóm mở rộng có ràng buộc này; count protein dương tính riêng dùng phép phân cụm riêng để mô tả dư thừa.

[ĐO] Mô phỏng 90/10 random trên danh sách dương, cov80 có **11–20/31** dòng test có họ hàng trong train; số cặp train–test cùng cụm **23–51/8.401**. Cov50 là **14–20/31**, **35–68/8.401**. Báo cả hai mẫu số để tránh tỉ lệ cặp nhỏ che số test bị ảnh hưởng. [overlap-audit.json](overlap-audit.json) → `internal_positive_homology`.

[CHƯA XÁC MINH] Đây là mô phỏng độ nhạy, **không phải split D thực tế**. Mã D dùng permutation seed 202310, split 10% seed 202309, stratification vector không được permutation đồng bộ; chưa tái dựng thứ tự object-NPY nên chưa biết giao thực tế. Bảng curate có cột `cluster` với các giá trị fold-like nhưng không được dùng làm group trong script train đã công bố; nguồn sinh cột đó chưa rõ. [code-audit.json](code-audit.json).

[ĐO] Riêng split X có thể tái dựng population và seed: đã đếm số dòng test chung cụm, số cặp train–test chung cụm và mẫu số mapped ở **từng fold**, cov50/cov80; xem `author_x_sampling.homology_by_cov` trong [composition-baseline.json](composition-baseline.json). Dòng thiếu mapping được loại khỏi mẫu số homology và báo coverage, không tự coi là singleton sạch.

## Chồng lấn với đề tài

[ĐO] Bảng sau phân biệt giao cùng accession và giao **đúng đoạn**: tile phải khớp toàn chuỗi trong protein nguồn, rồi khoảng degron phải giao tọa độ tile. Không tìm motif ngắn tự do trên protein không liên quan. Đã chuẩn hóa tên CRISPR thiếu accession bằng hậu tố tên peptide; không suy luận giao từ số tổng bằng nhau. [overlap-audit.json](overlap-audit.json).

| Bộ | Tổng peptide/tile | Dòng curate cùng accession | Dòng curate giao vùng | Peptide/tile giao vùng | Đồng thuận nhãn theo cặp | Cặp giao vị trí quan trọng |
|---|---|---|---|---|---|---|
| footprint | 2624 | 34 | 2 | 2 | 2 / 0 | 2 |
| saturation | 249 | 12 | 1 | 1 | 1 / 0 | 1 |
| crispr | 31 | 2 | 0 | 0 | 0 / 0 | 0 |
| g2 | 91 | 8 | 1 | 1 | 1 / 0 | 1 |
| voutsinos | 212658 | xem JSON | 146 | 318 | score≥0,5: 83; thấp: 252 | không có ΔPSI residue |
| larsen | 63258 | xem JSON | 49 | 108 | score≥0,5: 39; thấp: 71 | không có ΔPSI residue |

[ĐO] Coverage chuỗi: footprint **2624/2.624**, bão hòa **248/249**, CRISPR **31/31**, G2 **91/91**. Peptide chỉ có trong bão hòa dùng snapshot UniProt người đã ghim/17 accession bổ sung và quy tắc tile của pipeline gốc; CRISPR thiếu accession được map GN nếu duy nhất. Một record bão hòa chưa map được, nên phép giao của bộ249 có giới hạn coverage; không coi record đó là không trùng. [overlap-audit.json](overlap-audit.json).

[ĐO] Hai giao footprint nằm ở HIF3A và HIF1A, đều PSI WT thấp và có vị trí đột biến làm bền reporter nằm trong khoảng curate. Giao bão hòa/G2 là cùng ca HIF1A: PSI WT nội tại **2,186493579**, **13/13** vị trí giao có ít nhất một thay thế ΔPSI ≥1. Không gọi đó là 13 ô: mỗi vị trí có nhiều acid amin thay thế. Số chi tiết và accession nằm trong [overlap-audit.json](overlap-audit.json), sinh từ file PSI hai nửa và NPZ G2.

[DIỄN GIẢI] Concordance ở giao nhỏ không đo được độ nhạy/đặc hiệu toàn quần thể và không xác nhận E3 trực tiếp. Voutsinos/Larsen dùng score khác PSI; mốc score 0,5 là ngưỡng thăm dò, không hoán đổi với PSI=3. Larsen có **3 cặp thiếu score**, đã để missing. [overlap-audit.json](overlap-audit.json). Một motif được annotate trong protein nguyên vẹn có thể yếu ở reporter tách rời và ngược lại; đó chưa phải nhãn curate sai.

## “21 E3” có cứu nhiệm vụ E3 không?

[ĐỌC-MÃ] Danh sách dưới lấy từ mapping E3→motif của prediction source, join class của bảng curate; **đếm tương thích motif**, không gán thêm nhãn thực nghiệm phân biệt E3. CBL gom các subtype về class CBL; CUL3 chồng KLHL; SIAH1/2 và NEDD4/ITCH chia sẻ cùng mẫu. Không cộng các cột để làm số degron độc lập.

[ĐO] Mỗi ô số dưới do `e3_after_filter` trong [overlap-audit.json](overlap-audit.json). Cột “G2” bỏ vùng trùng mọi bộ đang audit và protein cùng cụm với các peptide G2. Cột “toàn reference” bảo thủ hơn: bỏ mọi cụm chứa protein trong `proteins-full.fasta`, gồm cả protein không thuộc tập G2. Hai điều kiện này không tương đương.

| E3 lựa chọn | Mẫu motif | HUMAN | Không trùng vùng/cụm G2 cov80 | Toàn reference cov80 | Toàn reference cov50 |
|---|---|---|---|---|---|
| CBL | 28 | 25 | 10 | 1 | 1 |
| CDC20 | 125 | 104 | 27 | 13 | 12 |
| COP1 | 12 | 9 | 1 | 1 | 0 |
| DTL | 7 | 4 | 2 | 1 | 1 |
| CUL3 | 6 | 5 | 1 | 0 | 0 |
| KLHL3 | 4 | 4 | 0 | 0 | 0 |
| KLHL2 | 4 | 4 | 0 | 0 | 0 |
| KEAP1 | 16 | 11 | 3 | 1 | 1 |
| KLHL17 | 2 | 1 | 1 | 0 | 0 |
| MDM2 | 5 | 5 | 2 | 0 | 0 |
| VHL | 8 | 6 | 0 | 0 | 0 |
| FBXW7 | 12 | 11 | 1 | 0 | 0 |
| SKP2 | 3 | 2 | 1 | 1 | 1 |
| BTRC | 21 | 18 | 3 | 2 | 1 |
| SIAH2 | 9 | 8 | 1 | 0 | 0 |
| SIAH1 | 9 | 8 | 1 | 0 | 0 |
| SPOP | 16 | 10 | 2 | 1 | 1 |
| FBXL2 | 0 | 0 | 0 | 0 | 0 |
| FBXO31 | 1 | 1 | 0 | 0 | 0 |
| NEDD4 | 1 | 1 | 0 | 0 | 0 |
| ITCH | 1 | 1 | 0 | 0 | 0 |

[ĐO] Số lựa chọn ≥5 mẫu: trước lọc **13**, HUMAN **12**, bỏ vùng trùng **2**, thêm bỏ cụm G2 **2**, toàn reference **1** ở cả hai coverage. Chỉ **21** dòng curate HUMAN còn lại trong phép lọc toàn reference cov80, **18** ở cov50. [overlap-audit.json](overlap-audit.json).

[DIỄN GIẢI] Số đếm này chưa đủ tái mở nhiệm vụ E3 của luận văn: cần nhãn liên kết E3 riêng từng dòng, đủ **cụm** cho train/test, và negatives có ý nghĩa theo E3. Nhóm APC/C không tự phân biệt được CDC20/Cdh1. Số 21 của web không phải chứng cứ có 21 bộ train sạch.

## Chất lượng nhãn và mức dùng được

[ĐO] Mẫu truy nguồn: **40** dòng ngẫu nhiên seed17; **22/40** có ELM true-positive cùng class/giao tọa độ, **18/40** chưa chốt lineage qua nguồn hiện hành. Wilson cho tỉ lệ chưa chốt **45,0% [30,7%; 60,2%]**. Đây **không phải tỉ lệ sai nhãn**. [manual-label-review.json](manual-label-review.json), [review-labels.py](review-labels.py).

[DIỄN GIẢI] Rủi ro cao: gộp nhãn từ hệ đo khác; suy E3 từ motif; shortcut/duplicate split; quyền dữ liệu chưa rõ. Rủi ro trung bình: flank/isoform và metadata loài. Nhãn binary curate bổ sung vị trí/cơ chế/PTM nhưng thiên về motif kinh điển; ΔPSI lớn hơn về số phép đo nhưng là reporter, có nhiễu và nhiều ô chung protein. Không gán 0/1 curate vào cột ΔPSI hay coi background ngẫu nhiên là thí nghiệm không phân hủy.
