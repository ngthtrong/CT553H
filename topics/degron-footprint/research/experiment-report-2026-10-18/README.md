# Hồ sơ thực nghiệm còn liên quan đến degron-footprint

**Cập nhật 18/10/2026 · Báo cáo tổng hợp bằng chứng, không phải sổ quyết định.** Trạng thái và điều kiện chính thức chỉ ở [DECISIONS.md](../../../../DECISIONS.md#hien-hanh). Báo cáo này không tạo hay thay quyết định, không ghi đề tài đã được duyệt, không coi G2 đã hoàn tất.

## 1. Những kết quả đang đỡ hướng hiện tại

- **Ngữ cảnh cục bộ có lợi trên bộ quét:** ridge M3 hơn baseline chỉ thành phần **+0,0289 AUROC** [0,0264;0,0313]; khoảng 80% mức tăng đến từ thành phần lân cận, không phải vị trí tuyệt đối (TN-19/20).
- **Học trực tiếp bão hòa đã vượt mốc số của frozen ΔPAP:** ridge OOF ensemble **0,8082**, ΔPAP **0,7693**, delta **+0,0389** [0,0216;0,0571] (TN-23). Đây là benchmark phát triển; phần kiến trúc có lợi ổn định/tính mới và đối chứng clean chưa được khép lại.
- **Các tương tác mạng chưa hơn ridge:** gate đảo dấu ở một seed; bilinear, FiLM và cross-ridge đều không đạt tiêu chí nhánh mở rộng đã ghi (TN-24/27). Không bỏ các kết quả âm này khỏi hồ sơ.
- **Điểm Degformer phải đọc cùng mức tiếp xúc dữ liệu:** checkpoint **0,9248** với **88,12% ô** có sequence trong train; lọc exact sequence còn **0,9227**, nhưng mọi WT đã có trong train nên vẫn không là peptide holdout sạch (TN-25/26).
- **Ý nghĩa bệnh chỉ được đỡ ở mức vùng:** OR **2,148** [2,072;2,227], chưa khử bảo tồn/vô trật tự; liên hệ bệnh mức residue chưa thiết lập (TN-37/38). Không dùng ClinVar làm nhãn xác nhận mô hình.

## 2. Cách đọc, nguồn và phạm vi

**Mục tiêu lưu trữ:** mỗi mục giữ lý do, cách làm, dữ liệu, kết quả, giới hạn và đường dẫn bằng chứng. Các TN là nhóm câu hỏi thực nghiệm, không đếm mỗi seed/fold thành một phát hiện. Gộp các phép kiểm phụ cùng câu hỏi; không tính xây slide, kiểm giao diện, tổng quan y văn hoặc tải file đơn thuần là kết quả mô hình.

**Loại bằng chứng:** `[ĐO]` là số đã lưu trong JSON/script/báo cáo của repo; `[DIỄN GIẢI]` là ý nghĩa có giới hạn ghi ngay sau số. Tại lượt tổng hợp này chỉ đọc và đối chiếu hồ sơ, **không chạy lại toàn bộ pipeline huấn luyện**. JSON tồn tại không đồng nghĩa kết quả đã qua xác nhận độc lập: nhánh mở rộng có trạng thái riêng. Chương cross-assay có script in stdout và bảng báo cáo, không phải mọi mục đều có JSON độc lập.

**Mốc chốt nguồn:** xem `snapshot_utc` trong [evidence-manifest.json](evidence-manifest.json). Manifest giữ đường dẫn/SHA-256 của các nguồn để biết báo cáo đọc phiên bản nào. Nó không sao chép raw data, không ghim nội dung HTTP hiện hành và không biến kết quả đang chạy thành hoàn tất.

| Nguồn | Phần sử dụng | Hồ sơ nguồn trong repo |
|---|---|---|
| Zhang 2023, [Mendeley v2](https://data.mendeley.com/datasets/32h94v2yv2/2), DOI 10.17632/32h94v2yv2.2 | Count quét/bão hòa để dựng ΔPSI; CRISPR để audit nhãn E3; GPS peptidome cho miền áp dụng | [Danh mục nguồn và file](../../data/README.md) |
| Zhang, [GEO GSE240610](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610) | Table S1 PSI peptidome và tọa độ tile | [Danh mục dữ liệu](../../data/README.md) |
| [Voutsinos](https://github.com/KULL-Centre/_2025_Voutsinos_degron_cytosol), commit 9b3eafa6… | Trọng số PAP, nhãn tile, danh sách train/holdout, sai số tile | [PAP baseline](../pap-baseline/README.md) |
| UniProt snapshot release 2026_03 + accession bổ sung | Trình tự tham chiếu, ánh xạ và gom cụm | [Sổ nguồn](../../data/README.md) |
| MaveDB và AlphaFold v6 | Nhãn ngoài ở protein nguyên vẹn, cấu trúc/rASA/pLDDT; chưa là nhãn chính ΔPSI | [Audit cấu trúc](../architecture-check/README.md) |
| Larsen tag v1.0, commit 2698ecc6… | Audit tile nhân, cột PAP/rASA/pLDDT và chồng gene | [SOURCE.md](../../data/raw/larsen-2025/SOURCE.md) |
| ClinVar snapshot Last-Modified 12/10/2026 | Độ phủ biến thể và liên hệ mức vùng; không làm nhãn xác nhận mô hình | [SOURCE.md](../../data/raw/clinvar/SOURCE.md) |
| Degformer commit 49ee5245… | Checkpoint epoch50, bảng train, mã kiến trúc và kiểm overlap | [Manifest nguồn](../g2-saturation-2026-10-18/source-manifest.json), [SOURCE.md](../../data/raw/degformer-isolated/SOURCE.md) |

Các URL trên là định danh nguồn, **không được kiểm truy cập lại trên web trong lượt lập báo cáo này**. Phiên bản và giấy phép chi tiết lấy từ sổ nguồn repo; không tự kết luận giấy phép Larsen đã được xác nhận.

### Đại lượng và điều kiện không được lẫn

- PSI thấp biểu thị reporter kém bền trong assay; **ΔPSI=PSI(mutant)−PSI(đối chứng)**. ΔPSI dương là reporter bền lên, không phải xác suất bệnh hay bằng chứng nhận diện trực tiếp của E3.
- Bão hòa dùng trung vị ô giữ nguyên trình tự làm đối chứng nội tại riêng từng nửa; nhãn lấy trung bình hai ΔPSI. Scanning có mut0 riêng. Một ô là một phép thay thế, không phải một peptide độc lập.
- Benchmark residue chính: PSI đối chứng≤3, đọc dữ liệu qua loader đã curate; ngưỡng ô dương ΔPSI≥1. Đánh giá **AUROC mức ô tính riêng từng peptide rồi trung bình macro**; peptide không có cả hai lớp không đóng góp AUROC, vì vậy số được chấm có thể nhỏ hơn số có nhãn.
- P@3, Spearman mức ô và Spearman map là các metric khác; không trừ chéo hoặc dùng cùng ký hiệu mà không ghi mức đo. Map trung bình hàng là tác động trung bình qua các thay thế khả dụng, không phải phép quét một thay thế duy nhất.
- Bootstrap theo cụm protein cov80, phép so ghép cặp trên cùng peptide. MDE phụ thuộc cặp mô hình/thiết kế. Trần đo lặp không phải hiệu năng chắc chắn học được.
- Phân biệt **train quét → test bão hòa** (TN-21) với **OOF học trực tiếp bão hòa** (TN-23). Không quy chênh giữa hai chế độ thành tác dụng riêng kiến trúc.

## 3. Chỉ mục thực nghiệm

| Mã | Câu hỏi / phép kiểm | Ngày | Trạng thái bằng chứng |
|---|---|---|---|
| [TN-01](#tn-01) | Dựng PSI và kiểm tái lập | 13/10/2026 | Còn dùng |
| [TN-02](#tn-02) | Quy mô, footprint và độ nhạy ngưỡng của bộ quét | 11–12/10/2026 | Còn dùng |
| [TN-03](#tn-03) | Trình tự, tọa độ, cụm protein và quy mô tập test | 12/10/2026 | Còn dùng |
| [TN-04](#tn-04) | Tính lặp lại của nhãn bộ quét | 13/10/2026 | Còn dùng |
| [TN-05](#tn-05) | Phần dư của mô hình thành phần và nhiễu đo | 12–13/10/2026 | Còn dùng |
| [TN-06](#tn-06) | Độ nhạy với độ sâu đọc | 13/10/2026 | Còn dùng |
| [TN-07](#tn-07) | Dựng đối chứng nội tại và ma trận bão hòa | 13/10/2026 | Còn dùng |
| [TN-08](#tn-08) | Cỡ mẫu hiện hành, các ngưỡng PSI và giao hai bộ | 15/10/2026 | Còn dùng |
| [TN-09](#tn-09) | Baseline thành phần, oracle, trần đo lặp, tie và lực P@3 | 12–13/10/2026 | Còn dùng |
| [TN-10](#tn-10) | Tái lập PAP và xác minh holdout | 11/10, kiểm lại 14/10/2026 | Còn dùng |
| [TN-11](#tn-11) | Kiểm đồng dạng holdout và tiếp xúc dữ liệu PAP | 11–14/10/2026 | Còn dùng |
| [TN-12](#tn-12) | Hoán vị chuỗi và thay pooling ở PAP | 11/10/2026 | Còn dùng |
| [TN-13](#tn-13) | Giới hạn mô hình thành phần trên nhãn vị trí | 12/10/2026 | Còn dùng |
| [TN-14](#tn-14) | ΔPAP trên footprint và độ nhạy nhãn | 14/10/2026 | Còn dùng |
| [TN-15](#tn-15) | ΔPAP trên ma trận và bản đồ theo vị trí | 14–15/10/2026 | Còn dùng |
| [TN-16](#tn-16) | Chấm SVM tác giả và kiểm control/MLN4924 | 13/10/2026 | Còn dùng |
| [TN-17](#tn-17) | Audit bảng train và split của Degformer | 15/10/2026 | Còn dùng |
| [TN-18](#tn-18) | Nhận diện hệ số trên nhãn ΔPSI | 15/10/2026 | Còn dùng |
| [TN-19](#tn-19) | Năm ridge và phân rã đóng góp đặc trưng | 15/10/2026 | Còn dùng |
| [TN-20](#tn-20) | So ngữ cảnh với ΔPAP trên cùng tập | 15/10/2026 | Còn dùng |
| [TN-21](#tn-21) | Chuyển scanning sang saturation | 15/10/2026 | Còn dùng |
| [TN-22](#tn-22) | Lực thống kê ghép cặp cho benchmark residue | 15/10/2026 | Còn dùng |
| [TN-23](#tn-23) | Ridge học trực tiếp bão hòa và kiểm OOF | 18/10/2026 | Còn dùng |
| [TN-24](#tn-24) | Gate theo cặp thay thế và hai ablation | 18/10/2026 | Còn dùng |
| [TN-25](#tn-25) | Checkpoint Degformer và audit overlap với tập đề tài | 18/10/2026 | Còn dùng |
| [TN-26](#tn-26) | Degformer trên ô không trùng exact sequence | 18/10/2026 | Có kết quả từng phần của nhánh mở rộng |
| [TN-27](#tn-27) | Ba mô hình tương tác: bilinear, FiLM và cross-ridge | 18/10/2026 | Có JSON kết quả; E3 của nhánh còn chạy |
| [TN-28](#tn-28) | Độ tin cậy tile và tương quan giữa hai thang điểm | 15/10/2026 | Còn dùng |
| [TN-29](#tn-29) | Ghép hai hệ đo, dải khó và đối chứng offset | 15/10/2026 | Còn dùng |
| [TN-30](#tn-30) | Cụm protein, năng lực mô hình và hệ số mức peptide | 15/10/2026 | Còn dùng |
| [TN-31](#tn-31) | Huấn luyện chuyển GPS–tile và mô hình phi tuyến | 15/10/2026 | Còn dùng |
| [TN-32](#tn-32) | Cổng phơi lộ trên protein nguyên vẹn và đối chứng bỏ PRKN | 14/10/2026 | Còn liên quan; số chính chưa đủ điều kiện dùng |
| [TN-33](#tn-33) | Liên hệ nhãn đoạn giữa Zhang và Voutsinos | 14/10/2026 | Còn dùng |
| [TN-34](#tn-34) | Audit bộ nhân Larsen và chồng gene | 15/10/2026 | Còn dùng |
| [TN-35](#tn-35) | Ánh xạ ClinVar, độ phủ đúng vị trí và đúng thay thế | 15/10/2026 | Còn dùng |
| [TN-36](#tn-36) | Miền áp dụng và mức mới so với tập nhãn | 15/10/2026 | Còn dùng |
| [TN-37](#tn-37) | Giàu biến thể gây bệnh ở mức vùng và đối chứng vị trí | 15/10/2026 | Còn dùng |
| [TN-38](#tn-38) | Tín hiệu bệnh tại vị trí/ô ΔPSI | 15/10/2026 | Còn dùng |
| [TN-39](#tn-39) | Kiểm vùng kinh điển và giới hạn assay | 15/10/2026 | Còn dùng |
| [TN-40](#tn-40) | Ví dụ ma trận HIF1A và map từ nhãn thật | 15/10/2026 | Còn dùng |
| [TN-41](#tn-41) | Khử trùng MaveDB và đo tài nguyên ESM | 11–14/10/2026 | Còn dùng |

## 4. Hồ sơ chi tiết

### Nhãn và phép chia

<a id="tn-01"></a>

#### TN-01 — Dựng PSI và kiểm tái lập

**Ngày / trạng thái:** 13/10/2026 · Còn dùng.

**Lý do:** Có cùng cách tính PSI cho quét, đối chứng BAG6 WT và bão hòa.

**Dữ liệu:** Count 6 bin của Zhang: scanning rep1/rep2, BAG6 WT, saturation S1…S12.

**Cách làm:** Chuẩn hóa nb_i=b_i×Σb_1/Σb_i; PSI=Σ(i×nb_i)/Σnb_i. So với cột PSI tác giả trên rep1.

**Kết quả [ĐO]:** 261.865 giá trị so được, sai khác tối đa 5,0×10⁻⁷. Xuất 261.868/261.999/264.036 định danh ở rep1/rep2/BAG6 WT, 134.608/134.563 ở hai nửa bão hòa. Phát hiện và xử lý lỗi header làm mất ba định danh trong pipeline cũ.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là tái lập nhãn, không phải dự đoán bằng mô hình. BAG6 WT là điều kiện riêng, không ghép thành replicate thứ ba.

**Bằng chứng và tái lập:** [build_psi.py](../full-data-audit/build_psi.py) · [psi-build.json](../full-data-audit/psi-build.json) · [README.md](../full-data-audit/README.md).

<a id="tn-02"></a>

#### TN-02 — Quy mô, footprint và độ nhạy ngưỡng của bộ quét

**Ngày / trạng thái:** 11–12/10/2026 · Còn dùng.

**Lý do:** Kiểm tra có đủ ví dụ tác động ở mức vị trí.

**Dữ liệu:** CSV scanning Replicate 1 Zhang: 283.880 dòng.

**Cách làm:** Lọc reads≥10, PSI gốc≤3, phủ≥21 vị trí; dương nếu ΔPSI≥1; quét thêm PSI 2,5/3/3,5 và ΔPSI 0,5/1/1,5.

**Kết quả [ĐO]:** 256.711 dòng PSI/read đạt lọc; 8.831 peptide có gốc và biến thể; 3.415 degron đủ phủ; 2.624 có footprint, 2.402 khu trú≤6 vị trí. Trung vị 3 vị trí dương.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Tập chọn có footprint khác tập 2.994 degron dùng benchmark sau này. Không gọi số dòng là số mẫu độc lập.

**Bằng chứng và tái lập:** [count_footprints.py](../e3-labels-audit/count_footprints.py) · [footprint-audit.json](../e3-labels-audit/footprint-audit.json) · [scanmut-audit.json](../e3-labels-audit/scanmut-audit.json).

<a id="tn-03"></a>

#### TN-03 — Trình tự, tọa độ, cụm protein và quy mô tập test

**Ngày / trạng thái:** 12/10/2026 · Còn dùng.

**Lý do:** Tránh ánh xạ sai và tránh chuỗi họ hàng rơi hai phía train/test.

**Dữ liệu:** Chuỗi Zhang và UniProt snapshot; 6.582 accession thư viện.

**Cách làm:** Đối chiếu peptide với protein canonical; xử lý stop cuối; MMseqs2 identity≥30%, coverage hai chiều 50%/80%; chia thử 80/10/10 theo cụm qua 5 seed.

**Kết quả [ĐO]:** Lấy được 6.573 protein; 2.602 footprint khớp tham chiếu. Cov80: 5.088 cụm, 271–322 footprint test; cov50: 4.418 cụm, 221–301 footprint test. Có ngoại lệ trình tự phải loại/curate.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là phân tích quy mô split lịch sử, không đồng nhất với 5-fold OOF hiện tại; cụm heuristic không chứng minh loại hết mọi họ hàng xa.

**Bằng chứng và tái lập:** [prepare_protein_clusters.py](../e3-labels-audit/prepare_protein_clusters.py) · [protein-clusters-cov80.json](../e3-labels-audit/protein-clusters-cov80.json) · [composition-audit.json](../e3-labels-audit/composition-audit.json) · [composition-context-audit.md](../composition-context-audit.md).

<a id="tn-04"></a>

#### TN-04 — Tính lặp lại của nhãn bộ quét

**Ngày / trạng thái:** 13/10/2026 · Còn dùng.

**Lý do:** Xác định mức nhiễu ngay tại đầu ra đề tài muốn dự đoán.

**Dữ liệu:** Hai replicate scanning, 85.518 cặp vị trí cho phép so ΔPSI.

**Cách làm:** So PSI, ΔPSI, footprint mức peptide và Jaccard tập vị trí dương.

**Kết quả [ĐO]:** Pearson ΔPSI=0,7229; Spearman=0,6485; SD nhiễu một replicate=0,2974. 2.104/2.356 footprint gọi lại được (89,3%), Jaccard vị trí 0,4965; 16,0% có tập vị trí dương giống hệt.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Lặp lại tốt việc có footprint không đồng nghĩa lặp lại tốt vị trí footprint.

**Bằng chứng và tái lập:** [replicate_audit.py](../full-data-audit/replicate_audit.py) · [replicate-audit.json](../full-data-audit/replicate-audit.json).

<a id="tn-05"></a>

#### TN-05 — Phần dư của mô hình thành phần và nhiễu đo

**Ngày / trạng thái:** 12–13/10/2026 · Còn dùng.

**Lý do:** Phân biệt thông tin ngữ cảnh còn thiếu với sai số thực nghiệm.

**Dữ liệu:** Scanning hai replicate và nhóm vị trí cùng cặp thay thế.

**Cách làm:** Đo oracle theo cặp; dùng Var(d1−d2)/4 cho nhiễu của nhãn trung bình; phân rã theo cùng đơn vị macro peptide.

**Kết quả [ĐO]:** Phần dư sau oracle=0,3612; 75,9% phần dư là nhiễu; cận phần phương sai có thể gắn ngữ cảnh=0,0872. Số 35% của audit một replicate không được hiểu là toàn bộ tín hiệu học được.

**Giới hạn / cách dùng [DIỄN GIẢI]:** 75,9% dùng mẫu số là PHẦN DƯ, khác 16,7% trên PHƯƠNG SAI QUAN SÁT của bão hòa; không so trực tiếp hai tỉ lệ.

**Bằng chứng và tái lập:** [label_ceiling.py](../full-data-audit/label_ceiling.py) · [label-ceiling.json](../full-data-audit/label-ceiling.json) · [composition-context-audit.md](../composition-context-audit.md).

<a id="tn-06"></a>

#### TN-06 — Độ nhạy với độ sâu đọc

**Ngày / trạng thái:** 13/10/2026 · Còn dùng.

**Lý do:** Kiểm tra có thể giảm phần lớn nhiễu bằng tăng ngưỡng reads không.

**Dữ liệu:** Scanning hai replicate.

**Cách làm:** Quét reads≥10/50/100/200/400; đếm mẫu, tính nhiễu và chỉ số vị trí.

**Kết quả [ĐO]:** Nhiễu/phần dư khoảng 0,72–0,77 từ ngưỡng 10 đến 200. Ngưỡng 100 còn 2.175 footprint, cận ngữ cảnh 0,0954; ngưỡng rất cao làm cỡ mẫu giảm mạnh.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Kết quả không ủng hộ giả thuyết nhiễu chủ yếu do reads thấp. Không chọn ngưỡng mới chỉ vì một chỉ số tốt hơn.

**Bằng chứng và tái lập:** [read_depth_sweep.py](../full-data-audit/read_depth_sweep.py) · [read-depth-sweep.json](../full-data-audit/read-depth-sweep.json).

<a id="tn-07"></a>

#### TN-07 — Dựng đối chứng nội tại và ma trận bão hòa

**Ngày / trạng thái:** 13/10/2026 · Còn dùng.

**Lý do:** Bộ bão hòa thiếu mut0 riêng nhưng cần mốc để tính ΔPSI.

**Dữ liệu:** 249 peptide bão hòa; hai nửa S1…S6 và S7…S12; chuỗi scanning/UniProt.

**Cách làm:** Lấy trung vị PSI các ô giữ nguyên axit amin gốc theo từng nửa; trừ mốc để tính ΔPSI; giữ ô hai nửa đều có. Kiểm quy tắc tile và so với gốc scanning.

**Kết quả [ĐO]:** 128/130 peptide có chuỗi thật khớp tọa độ, loại hai ca lệch. SD PSI đối chứng nội tại trung vị 0,0576; r với gốc scanning 0,7882. Dựng 235 ma trận, 122.412 ô, phủ trung bình 97,9%; r ΔPSI hai nửa 0,8335; nhiễu 16,7% phương sai quan sát; Jaccard ô dương 0,6596.

**Giới hạn / cách dùng [DIỄN GIẢI]:** 235 peptide là trước lọc PSI gốc≤3; bộ chính sau lọc còn 91. Đối chứng nội tại là ước lượng từ ô giữ nguyên trình tự, không phải một mut0 đã đo riêng.

**Bằng chứng và tái lập:** [saturation_audit.py](../full-data-audit/saturation_audit.py) · [saturation_matrix.py](../full-data-audit/saturation_matrix.py) · [saturation-matrix.json](../full-data-audit/saturation-matrix.json) · [residue_data.py](../residue-task-derisk-2026-10-15/residue_data.py).

<a id="tn-08"></a>

#### TN-08 — Cỡ mẫu hiện hành, các ngưỡng PSI và giao hai bộ

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Xác định số chuỗi/ô và đơn vị suy luận đúng trước khi so mô hình.

**Dữ liệu:** Quét và bão hòa đã curate, protein/cụm cov80.

**Cách làm:** Dùng chung loader; quét ngưỡng PSI; đếm cụm; tính ICC ô trong peptide và design effect.

**Kết quả [ĐO]:** Ở PSI≤3: scanning 2.994 peptide/2.474 protein/1.985 cụm/83.446 ô; saturation 91/91/89/47.847. Giao 42 peptide và 61 cụm. Bão hòa ICC=0,0625, design effect=33,79, khoảng 1.416 ô độc lập hiệu dụng. JSON cho 38/91/141/176/235 peptide ở PSI≤2,5/3/3,5/4/không ngưỡng.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Số độc lập hiệu dụng là ước lượng theo ICC, không thay bootstrap cụm. Bảng README cũ ghi 9 thay vì 38 ở PSI≤2,5; báo cáo này dùng JSON, xem mục đính chính.

**Bằng chứng và tái lập:** [ladder.json](../residue-task-derisk-2026-10-15/ladder.json) · [residue_data.py](../residue-task-derisk-2026-10-15/residue_data.py) · [derisk.py](../residue-task-derisk-2026-10-15/derisk.py).

<a id="tn-09"></a>

#### TN-09 — Baseline thành phần, oracle, trần đo lặp, tie và lực P@3

**Ngày / trạng thái:** 12–13/10/2026 · Còn dùng.

**Lý do:** Tránh lấy oracle đọc test làm hiệu năng mô hình và kiểm cỡ test cần thiết.

**Dữ liệu:** Scanning hai replicate; khoảng 2.403 peptide chấm được.

**Cách làm:** Ước lượng điểm nhóm từ rep1, chấm rep2; replicate chấm chéo; đổi cách phá tie; tính lực ghép cặp.

**Kết quả [ĐO]:** P@3 thành phần trung thực 0,4897; đo lặp 0,6514. Các oracle đọc nhãn 0,6045/0,7792 chỉ là đối chứng lý tưởng. Baseline theo tie bất lợi/có lợi 0,4066/0,5754. SD chênh 0,2416; cỡ mẫu tham chiếu 18 hoặc 209 tùy effect size.

**Giới hạn / cách dùng [DIỄN GIẢI]:** P@3 là thước đo lịch sử hỗ trợ, không thay AUROC mức ô hiện hành; lực phụ thuộc đúng cặp mô hình/effect size, không bảo đảm mọi so sánh tương lai.

**Bằng chứng và tái lập:** [label-ceiling.json](../full-data-audit/label-ceiling.json) · [power-analysis.json](../full-data-audit/power-analysis.json) · [power_analysis.py](../full-data-audit/power_analysis.py) · [composition-context-audit.md](../composition-context-audit.md).

### Baseline và kiểm biểu diễn

<a id="tn-10"></a>

#### TN-10 — Tái lập PAP và xác minh holdout

**Ngày / trạng thái:** 11/10, kiểm lại 14/10/2026 · Còn dùng.

**Lý do:** Có baseline suy luận đúng và tập chấm đúng.

**Dữ liệu:** Voutsinos: trọng số cnn2w1/cnn2w7, bảng điểm/train và holdout_selection.

**Cách làm:** Đối chiếu danh sách holdout với train; dựng NumPy network; kênh C-terminal áp mọi tile; so kết quả với tác giả.

**Kết quả [ĐO]:** Toàn bảng 212.658 tile/5.327 gene; train 195.629 tile/4.830 gene. 96/527 gene holdout nằm hết ở train, ba gene một phần; holdout hiệu dụng 428 gene/15.820 tile, 15.818 chấm được. Pearson nội 0,8239, đầy đủ cnn2w1 0,8690, cnn2w7 0,8722; khớp mốc 0,82/0,87.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Dùng checkpoint công bố, không huấn luyện lại PAP. Mã train nguồn có chỉ số cột DNA sai với CSV hiện có; không coi chạy thẳng mã đó là tái lập train hợp lệ.

**Bằng chứng và tái lập:** [pap-baseline.json](../pap-baseline/pap-baseline.json) · [pap_baseline.py](../pap-baseline/pap_baseline.py) · [reconcile.json](../voutsinos-2026-audit/reconcile.json) · [README.md](../voutsinos-2026-audit/README.md).

<a id="tn-11"></a>

#### TN-11 — Kiểm đồng dạng holdout và tiếp xúc dữ liệu PAP

**Ngày / trạng thái:** 11–14/10/2026 · Còn dùng.

**Lý do:** Xác định hạn chế của đối chứng và tránh tuyên bố rò rỉ quá mức.

**Dữ liệu:** Cụm tác giả; protein train/holdout; mapping ENSG–UniProt; footprint Zhang.

**Cách làm:** Kiểm singleton, alignment độc lập bằng sàng 6-mer/Smith–Waterman; tách footprint theo protein có/không trong train PAP.

**Kết quả [ĐO]:** 527 gene danh sách holdout đều singleton theo cụm tác giả. Alignment phát hiện 14/428 gene có họ hàng train ở identity≥30%, coverage≥50%, trong đó một cặp 100% trên 77 residue. P@3 ΔPAP cnn2w7 ở protein đã/chưa thấy: 0,4268 (656 peptide)/0,4270 (1.747 peptide).

**Giới hạn / cách dùng [DIỄN GIẢI]:** Sàng 6-mer bỏ sót họ hàng xa. Không thấy lợi thế ở phép tách này không chứng minh hết mọi loại rò rỉ. Không dùng giả thuyết cũ rằng tác giả không kiểm soát đồng dạng.

**Bằng chứng và tái lập:** [align-check.json](../voutsinos-2026-audit/align-check.json) · [holdout-audit.json](../voutsinos-2026-audit/holdout-audit.json) · [README.md](../pap-baseline/README.md).

<a id="tn-12"></a>

#### TN-12 — Hoán vị chuỗi và thay pooling ở PAP

**Ngày / trạng thái:** 11/10/2026 · Còn dùng.

**Lý do:** Kiểm tính phụ thuộc thứ tự và cách tổng hợp tín hiệu vị trí.

**Dữ liệu:** PAP trọng số công bố và tile Voutsinos.

**Cách làm:** Hoán vị thứ tự theo phép kiểm; so điểm trước/sau; giữ trọng số và thay average bằng max/top-3 pooling.

**Kết quả [ĐO]:** cnn2w1 ở phép hoán vị có max |Δ|≈4,8×10⁻⁷, tương quan 1,000000; cnn2w7 r=0,9018. Với cnn2w1, Pearson average/max/top-3=0,8239/0,3443/0,4847.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Bất biến của kênh thành phần không áp cho mọi phần PAP đầy đủ có C-terminal. Đổi pooling nhưng không train lại chỉ là thăm dò, không chứng minh kiến trúc max kém.

**Bằng chứng và tái lập:** [pool-test.json](../voutsinos-2026-audit/pool-test.json) · [pool_test.py](../voutsinos-2026-audit/pool_test.py) · [README.md](../voutsinos-2026-audit/README.md).

<a id="tn-13"></a>

#### TN-13 — Giới hạn mô hình thành phần trên nhãn vị trí

**Ngày / trạng thái:** 12/10/2026 · Còn dùng.

**Lý do:** Kiểm tín hiệu mà thành phần cả chuỗi không phân biệt được.

**Dữ liệu:** 2.624 footprint của scanning rep1.

**Cách làm:** Gom đúng cặp (WT, thay thế) trong từng peptide; đo nhóm có nhãn trái nhau; tính oracle và kiểm thuật toán cận.

**Kết quả [ĐO]:** 2.353/2.624=89,7% có nhóm cùng cặp chứa cả dương/không dương; 2.046/2.624=78,0% có khoảng ΔPSI≥1. Phát hiện 876 ngoại lệ thay thế ở vị trí 25–27; không được gom chỉ theo WT.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là giới hạn biểu diễn trên nhãn quan sát, không chứng minh phần chênh đều học được. Tập benchmark 2.994 degron sau này có tỉ lệ nhóm mâu thuẫn 68,9%, mẫu số khác.

**Bằng chứng và tái lập:** [composition-audit.json](../e3-labels-audit/composition-audit.json) · [validate_composition.py](../e3-labels-audit/validate_composition.py) · [composition-context-audit.md](../composition-context-audit.md).

<a id="tn-14"></a>

#### TN-14 — ΔPAP trên footprint và độ nhạy nhãn

**Ngày / trạng thái:** 14/10/2026 · Còn dùng.

**Lý do:** Chấm baseline mức đoạn trên tác động thay thế thực tế.

**Dữ liệu:** 2.403 peptide scanning; trọng số PAP; hai replicate.

**Cách làm:** PAP(mutant)−PAP(WT), đúng thay thế CSV; chấm P@3 với rep2; bootstrap ghép cặp; chấm thêm nhãn trung bình.

**Kết quả [ĐO]:** P@3 cnn2w1=0,2959; cnn2w7=0,4270; thành phần=0,4884. cnn2w7−thành phần=−0,0615 [−0,073;−0,049]. Với nhãn trung bình, cnn2w7 P@3=0,4364, Spearman=0,4747.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đối chứng PAP được dùng ngoài nhiệm vụ train gốc. Số thành phần 0,4884 khác 0,4897 do điều kiện giao peptide và phá tie, không tự chọn số thuận lợi.

**Bằng chứng và tái lập:** [pap-baseline.json](../pap-baseline/pap-baseline.json) · [README.md](../pap-baseline/README.md) · [pap_baseline.py](../pap-baseline/pap_baseline.py).

<a id="tn-15"></a>

#### TN-15 — ΔPAP trên ma trận và bản đồ theo vị trí

**Ngày / trạng thái:** 14–15/10/2026 · Còn dùng.

**Lý do:** Đặt mốc ma trận và phân biệt metric mức ô với mức vị trí.

**Dữ liệu:** 91 peptide saturation sau lọc, nhãn trung bình hai nửa.

**Cách làm:** Chấm ΔPAP mức ô; trung bình các ô thay thế hợp lệ trong mỗi hàng để tạo map; chấm Spearman theo peptide.

**Kết quả [ĐO]:** cnn2w1 AUROC 0,7692 (kiểm lại 0,7693); cnn2w7 0,7646. Spearman cnn2w1 mức ô 0,3553, mức vị trí 0,4130; cnn2w7 mức vị trí 0,4067. Mốc đo lặp AUROC 0,9519, Spearman mức ô 0,6989.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không so 0,4440 mức vị trí của ridge với 0,3553 mức ô của PAP. Các map trung bình 19 thay thế khác nhãn scanning một thay thế/vị trí.

**Bằng chứng và tái lập:** [pap-baseline.json](../pap-baseline/pap-baseline.json) · [pap_baseline.py](../pap-baseline/pap_baseline.py) · [ceiling.json](../residue-task-derisk-2026-10-15/ceiling.json).

<a id="tn-16"></a>

#### TN-16 — Chấm SVM tác giả và kiểm control/MLN4924

**Ngày / trạng thái:** 13/10/2026 · Còn dùng.

**Lý do:** Kiểm baseline mức peptide có sẵn và chất lượng nguồn GPS.

**Dữ liệu:** Dự đoán SVM Zhang train 5%/10%; GPS control rep1/rep2 và MLN4924.

**Cách làm:** So dự đoán đã công bố với PSI; đo tương quan replicate và số peptide bền lên dưới MLN4924.

**Kết quả [ĐO]:** SVM 10%: Pearson 0,8955, RMSE 0,563 trên 260.989 peptide; 5%: 0,8916/0,5708. Control r=0,9304 trên 343.236 peptide, SD nhiễu 0,3357; 1.978/260.989 tăng≥1 PSI.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không huấn luyện lại SVM. Đây là dự đoán mức peptide, không thay benchmark ΔPSI mức ô.

**Bằng chứng và tái lập:** [gps_peptidome_audit.py](../full-data-audit/gps_peptidome_audit.py) · [gps-peptidome-audit.json](../full-data-audit/gps-peptidome-audit.json).

<a id="tn-17"></a>

#### TN-17 — Audit bảng train và split của Degformer

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Xác định baseline gần nhiệm vụ nhất và hạn chế đánh giá công bố.

**Dữ liệu:** Mã và training_data.csv của Degformer.

**Cách làm:** Đếm chuỗi trùng, phân bố nhãn cùng chuỗi; tái lập arithmetic split random_state=42.

**Kết quả [ĐO]:** 569.270 dòng/554.085 chuỗi duy nhất; 9.496 chuỗi lặp, 9.443 có nhãn khác nhau; chênh nhãn tối đa 3,98. Có 1.954 chuỗi xuất hiện hai phía, tương ứng 2.330/56.927=4,09% dòng validation.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là audit bảng/split, chưa là clean benchmark checkpoint; phân biệt với kiểm 88,12% overlap của tập đề tài ngày 18/10. Các số này được ghi trong note, chưa có JSON độc lập của lượt 15/10.

**Bằng chứng và tái lập:** [06-degformer-and-error-models.md](../larsen-nuclear-and-risks-2026-10-15/notes/06-degformer-and-error-models.md).

### Mô hình ngữ cảnh 15/10

<a id="tn-18"></a>

#### TN-18 — Nhận diện hệ số trên nhãn ΔPSI

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Kiểm nhãn tác động thay thế có thông tin ngữ cảnh hơn nhãn cả đoạn.

**Dữ liệu:** Quét 2.994 peptide/1.985 cụm, bão hòa 91/89; đối chiếu audit PSI mức peptide.

**Cách làm:** Bootstrap theo cụm; kiểm |μ|/SD, đồng thuận dấu, tái lập hệ số ngữ cảnh ±3 và cặp thay thế.

**Kết quả [ĐO]:** Quét: 53,3% hệ số ngữ cảnh vượt tiêu chí |μ|/SD>2, đồng thuận dấu 0,900, so 28,9%/0,684 ở nhãn peptide. Bão hòa: 25% ngữ cảnh và 92,5% hệ số cặp thay thế vượt tiêu chí. Tỉ số ổn định thành phần/ngữ cảnh giảm khoảng 56×→2,2×.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không phải kiểm định nhân quả hoặc chứng minh tính mới. Tiêu chí hệ số là chẩn đoán thực nghiệm; cần đọc cùng bootstrap và độ phụ thuộc.

**Bằng chứng và tái lập:** [identify.json](../residue-task-derisk-2026-10-15/identify.json) · [derisk.py](../residue-task-derisk-2026-10-15/derisk.py).

<a id="tn-19"></a>

#### TN-19 — Năm ridge và phân rã đóng góp đặc trưng

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Đo ngữ cảnh/thứ tự/vị trí tuyệt đối có giúp dự đoán không.

**Dữ liệu:** 83.446 ô scanning; nhóm cov80.

**Cách làm:** 5 fold×5 seed; alpha bằng PRESS/LOO giải tích; M0 thành phần, M1 thêm vị trí, M2 thành phần ±3, M3 ±3 có thứ tự, M4 thêm vị trí vào M3.

**Kết quả [ĐO]:** AUROC M0/M1/M2/M3/M4=0,8393/0,8445/0,8625/0,8682/0,8684. M3−M0=+0,0289 [0,0264;0,0313]. Thành phần lân cận +0,0232≈80% delta, thứ tự +0,0057, vị trí tuyệt đối thêm vào M3 chỉ +0,0002.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không diễn đạt thành “vị trí thắng thành phần”; bằng chứng chủ yếu ủng hộ thành phần ở thang lân cận. Đây là thiết kế cũ khác nested inner validation của lượt 18/10.

**Bằng chứng và tái lập:** [model.json](../residue-task-derisk-2026-10-15/model.json) · [paired-diffs.json](../residue-task-derisk-2026-10-15/paired-diffs.json) · [README.md](../residue-task-derisk-2026-10-15/README.md).

<a id="tn-20"></a>

#### TN-20 — So ngữ cảnh với ΔPAP trên cùng tập

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Tránh so hai điểm khác mẫu số.

**Dữ liệu:** 2.064 peptide/1.471 cụm scanning cả ridge và PAP chấm được.

**Cách làm:** Ghép cặp AUROC theo peptide, bootstrap cụm.

**Kết quả [ĐO]:** M3−cnn2w7=+0,0300 [0,0234;0,0366]; M3−cnn2w1=+0,0714 [0,0652;0,0775]. Trên tập giao, M3=0,8657; M0−cnn2w7=+0,0008 [−0,0057;0,0074].

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không lấy M3=0,8682 trên tập lớn trừ PAP trên tập giao để thay delta ghép cặp. PAP được dùng ngoài mục tiêu gốc, baseline M0 gần hòa PAP nên rào này không cao.

**Bằng chứng và tái lập:** [headline.json](../residue-task-derisk-2026-10-15/headline.json) · [pap-per-peptide.json](../residue-task-derisk-2026-10-15/pap-per-peptide.json).

<a id="tn-21"></a>

#### TN-21 — Chuyển scanning sang saturation

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Đo khả năng dự đoán 19 thay thế và cụm chưa thấy khi chỉ học quét.

**Dữ liệu:** Train 2.849 peptide scanning sau loại 145 peptide trùng cụm; test 91 peptide/47.847 ô bão hòa.

**Cách làm:** Fit ridge trên scanning; loại mọi cụm bão hòa khỏi train; chấm saturation.

**Kết quả [ĐO]:** AUROC M0/M1/M2/M3/M4=0,7071/0,7194/0,7241/0,7273/0,7253. M3−ΔPAP cnn2w1=−0,0420 [−0,0580;−0,0256]; Spearman map M3=0,4440.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là kết quả CHUYỂN NGUỒN lịch sử, không phải điểm mô hình học trực tiếp saturation hiện tại. Bộ quét có nhiều quy tắc thay thế, không gọi toàn bộ là chỉ →R hay mọi thay thế saturation đều chưa thấy.

**Bằng chứng và tái lập:** [model.json](../residue-task-derisk-2026-10-15/model.json) · [headline.json](../residue-task-derisk-2026-10-15/headline.json) · [residue_data.py](../residue-task-derisk-2026-10-15/residue_data.py).

<a id="tn-22"></a>

#### TN-22 — Lực thống kê ghép cặp cho benchmark residue

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Thay ước lượng lực không ghép cặp bằng đúng chênh mô hình thật.

**Dữ liệu:** Dự đoán OOF quét và chuyển sang bão hòa; 89 cụm saturation.

**Cách làm:** Bootstrap cụm 4.000 lần; tính SE, MDE và lực của từng cặp.

**Kết quả [ĐO]:** Riêng M3−M0 trên saturation: delta +0,0201 [0,0117;0,0285], MDE lực 80%=0,0123, lực tại delta quan sát=0,995. Scanning MDE khoảng 0,0025–0,0036.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không dùng 0,0123 làm chuẩn đạt chung hay tái sử dụng cho mọi mô hình mới. CI phụ thuộc thiết kế và dự đoán đã có.

**Bằng chứng và tái lập:** [power.json](../residue-task-derisk-2026-10-15/power.json) · [ladder.json](../residue-task-derisk-2026-10-15/ladder.json).

### Học bão hòa 18/10

<a id="tn-23"></a>

#### TN-23 — Ridge học trực tiếp bão hòa và kiểm OOF

**Ngày / trạng thái:** 18/10/2026 · Còn dùng.

**Lý do:** Kiểm mô hình đơn giản khi có nhãn đúng 19 loại thay thế.

**Dữ liệu:** 91 peptide/89 cụm/47.847 ô saturation; không dùng scanning.

**Cách làm:** 5 outer fold cov80; inner validation theo cụm chọn alpha 1/10/100/1000; seed 17/29/43; ensemble điểm trước khi tính AUROC; bootstrap cụm 5.000 lần.

**Kết quả [ĐO]:** Ridge M3 ensemble AUROC=0,8082; ΔPAP frozen=0,7693; delta +0,0389 [0,0216;0,0571]. Điểm seed ridge 0,8062/0,8068/0,8081. Audit reload/split đã PASS trong hồ sơ.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là OOF phát triển trên dữ liệu đã khảo sát; ba seed dùng cùng outer partition. Không nhận chênh với 0,7273 là đóng góp kiến trúc vì đã thay nguồn giám sát; chưa cân bằng ngân sách nhãn với PAP.

**Bằng chứng và tái lập:** [PROTOCOL.md](../g2-saturation-2026-10-18/PROTOCOL.md) · [results.json](../g2-saturation-2026-10-18/results.json) · [audit.json](../g2-saturation-2026-10-18/audit.json) · [run.py](../g2-saturation-2026-10-18/run.py).

<a id="tn-24"></a>

#### TN-24 — Gate theo cặp thay thế và hai ablation

**Ngày / trạng thái:** 18/10/2026 · Còn dùng.

**Lý do:** Kiểm một thành phần tương tác thay thế–ngữ cảnh có lợi ổn định không.

**Dữ liệu:** Cùng saturation và folds của TN-23; 180 đặc trưng M3, không input PSI WT thực nghiệm.

**Cách làm:** Pair 40→32, composition+context 140→32, sigmoid gate, MLP; thử gate+PAP, bỏ gate, bỏ PAP; 45 lượt mạng=3 cấu hình×3 seed×5 fold.

**Kết quả [ĐO]:** Ensemble gate+PAP=0,8002; bỏ gate=0,7937; bỏ PAP=0,8015. Gate+PAP−ridge=−0,0080 [−0,0152;−0,0006]. So bỏ gate ensemble +0,0065 [0,0027;0,0102], nhưng delta từng seed +0,0089/−0,0076/+0,0064.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Gate không ổn định qua seed; residual PAP chưa có lợi rõ. Không gọi gate là kiến trúc mới đã xác lập, không dùng ensemble để che seed âm.

**Bằng chứng và tái lập:** [results.json](../g2-saturation-2026-10-18/results.json) · [audit.json](../g2-saturation-2026-10-18/audit.json) · [README.md](../g2-saturation-2026-10-18/README.md).

<a id="tn-25"></a>

#### TN-25 — Checkpoint Degformer và audit overlap với tập đề tài

**Ngày / trạng thái:** 18/10/2026 · Còn dùng.

**Lý do:** Chạy baseline chính thức và kiểm có được gọi là test sạch không.

**Dữ liệu:** Degformer epoch50 commit ghim 49ee5245…; training_data.csv; saturation 47.847 ô.

**Cách làm:** Suy luận PSI mutant−WT; dùng class đã đọc, chạy riêng python -I; so exact sequence với train.

**Kết quả [ĐO]:** Macro AUROC=0,9248. Có 42.163/47.847 ô=88,12% sequence trùng train; WT 91/91 cũng có trong train.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không gọi 0,9248 là hiệu năng peptide chưa thấy. Thư mục riêng/python -I không là sandbox bảo mật; không dùng chênh với ridge để kết luận thắng/thua trên clean holdout.

**Bằng chứng và tái lập:** [results.json](../g2-saturation-2026-10-18/results.json) · [source-manifest.json](../g2-saturation-2026-10-18/source-manifest.json) · [README.md](../g2-saturation-2026-10-18/README.md).

<a id="tn-26"></a>

#### TN-26 — Degformer trên ô không trùng exact sequence

**Ngày / trạng thái:** 18/10/2026 · Có kết quả từng phần của nhánh mở rộng.

**Lý do:** Đo overlap có giải thích toàn bộ điểm cao của checkpoint không.

**Dữ liệu:** 5.684 ô không trùng exact sequence; 85 peptide/83 cụm chấm được.

**Cách làm:** Giữ checkpoint; lọc ô không có exact sequence trong train; chấm lại và bootstrap cụm.

**Kết quả [ĐO]:** Degformer=0,9227; ridge=0,8040; ΔPAP=0,7531. Degformer−ridge=+0,1187 [0,0940;0,1446]; ridge−ΔPAP=+0,0509 [0,0239;0,0812].

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không trùng ô KHÔNG có nghĩa peptide/protein/cụm chưa thấy: mọi WT đã nằm trong train và biến thể họ hàng còn đó. Không kết luận 88,12% overlap là nguyên nhân định lượng của toàn bộ chênh lệch.

**Bằng chứng và tái lập:** [PREREGISTRATION.md](../g2-extension-2026-10-18/PREREGISTRATION.md) · [e1-overlap.json](../g2-extension-2026-10-18/e1-overlap.json) · [run_ext.py](../g2-extension-2026-10-18/run_ext.py).

<a id="tn-27"></a>

#### TN-27 — Ba mô hình tương tác: bilinear, FiLM và cross-ridge

**Ngày / trạng thái:** 18/10/2026 · Có JSON kết quả; E3 của nhánh còn chạy.

**Lý do:** Kiểm tương tác khác gate có ổn định vượt ridge M3 không.

**Dữ liệu:** Cùng 91 peptide saturation; đầu vào M3; cùng outer cov80 và seed 17/29/43.

**Cách làm:** Theo PREREGISTRATION: bilinear hạng thấp; FiLM scale+shift theo pair; ridge cộng 2.400 tích chéo (2.580 đặc trưng). Tiêu chí: thắng ridge từng seed, CI ensemble dương và thắng ΔPAP.

**Kết quả [ĐO]:** Ensemble bilinear=0,7933; FiLM=0,8028; cross-ridge=0,7924; ridge tham chiếu=0,8082. Delta với ridge lần lượt −0,0149 [−0,0227;−0,0072], −0,0054 [−0,0136;0,0028], −0,0158 [−0,0227;−0,0086]. Cả ba JSON ghi meets_preregistered_criterion=false.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Ba ứng viên đều không đạt tiêu chí đã ghi; không nhận việc vượt frozen PAP là chứng minh hơn ridge. Cross-ridge xác định nên ba seed cho cùng điểm, không phải ba lần xác nhận độc lập. Nhánh mở rộng đã có README với E3 còn đang chạy; chưa có validation tổng kết tại mốc chốt.

**Bằng chứng và tái lập:** [e2-candidates.json](../g2-extension-2026-10-18/e2-candidates.json) · [README.md](../g2-extension-2026-10-18/README.md) · [PREREGISTRATION.md](../g2-extension-2026-10-18/PREREGISTRATION.md) · [run_ext.py](../g2-extension-2026-10-18/run_ext.py).

### Cross-assay và cấu trúc

<a id="tn-28"></a>

#### TN-28 — Độ tin cậy tile và tương quan giữa hai thang điểm

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Xác định hai nhãn tile có độc lập và tin cậy không.

**Dữ liệu:** 212.658 tile Voutsinos/5.327 gene, sai số từng tile.

**Cách làm:** Ước lượng reliability=(Var tổng−Var sai số trung bình)/Var tổng và căn reliability; so degron_score với abundance_score.

**Kết quả [ĐO]:** Reliability degron_score=0,9807, mốc tương quan 0,9903; abundance_score=0,8549; Pearson giữa hai thang=−0,9558.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Các giả định về sai số đi cùng ước lượng; 0,9903 không phải độ chính xác đạt được từ chuỗi và không phải lời hứa dư địa. Hai thang không là hai assay độc lập.

**Bằng chứng và tái lập:** [probe_tile_reliability.py](../reframe-options-2026-10-15/probe_tile_reliability.py) · [README.md](../reframe-options-2026-10-15/README.md).

<a id="tn-29"></a>

#### TN-29 — Ghép hai hệ đo, dải khó và đối chứng offset

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Đo mức bất đồng nhãn giữa GPS và tile, kiểm độ nhạy ghép chuỗi.

**Dữ liệu:** 17.820 trình tự chung GPS 28-mer nằm trong tile 30-mer; 4.610 accession/4.308 cụm.

**Cách làm:** So nhãn và replicate; chỉnh suy giảm hai phía; tách PSI 2–4; phân nhóm offset 0/1/2 trên 17.680 cặp chỉ khớp một tile.

**Kết quả [ĐO]:** AUROC đo lặp GPS 0,9813, qua hệ 0,9041 (chênh 0,0773); |r| sau chỉnh nhiễu=0,7854. Dải khó AUROC=0,7839. AUROC theo offset=0,9069/0,9026/0,9040, biến thiên 0,0044.

**Giới hạn / cách dùng [DIỄN GIẢI]:** 28-mer và 30-mer không là construct giống hệt. Offset ít thay đổi không chứng minh hai residue thêm đóng góp tối đa 6%; không dùng phép chia 0,0044/0,0773 làm cận nhân quả.

**Bằng chứng và tái lập:** [cross_assay_gap.py](../reframe-options-2026-10-15/cross_assay_gap.py) · [cascade_and_offset.py](../reframe-options-2026-10-15/cascade_and_offset.py) · [README.md](../reframe-options-2026-10-15/README.md).

<a id="tn-30"></a>

#### TN-30 — Cụm protein, năng lực mô hình và hệ số mức peptide

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Kiểm đánh giá có phụ thuộc split cụm/mô hình yếu; kiểm nhãn đoạn có nhận diện vị trí không.

**Dữ liệu:** GPS mức peptide và tile ghép cặp; 43.635 peptide cho bootstrap hệ số.

**Cách làm:** 2×2 cùng/khác cụm×hệ đo bằng ridge, 5 seed; kiểm thêm boosting và 1-NN, 3 seed; bootstrap hệ số 40 lần.

**Kết quả [ĐO]:** Chênh cùng−khác cụm ridge/boosting/1-NN=−0,0032/−0,0014/−0,0094 trong phép kiểm mô hình. 1-NN khoảng 0,31, ridge khoảng 0,89. Chỉ 28,9% hệ số vị trí vượt |μ|/SD>2; đồng thuận dấu 0,684; thành phần ổn định hơn khoảng 56×.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Chỉ áp cho cấu hình, dữ liệu và mức nhãn đã thử. Không nói split cụm không bao giờ cần; không quy chênh điểm GPS/tile 0,1061 hoàn toàn thành ảnh hưởng assay.

**Bằng chứng và tái lập:** [cascade_and_offset.py](../reframe-options-2026-10-15/cascade_and_offset.py) · [method_debt.py](../reframe-options-2026-10-15/method_debt.py) · [README.md](../reframe-options-2026-10-15/README.md).

<a id="tn-31"></a>

#### TN-31 — Huấn luyện chuyển GPS–tile và mô hình phi tuyến

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Thử lợi ích thực của phối hợp nguồn nhãn trước khi chọn trụ đóng góp.

**Dữ liệu:** GPS/tile cùng đặc trưng one-hot+thành phần; split cov80.

**Cách làm:** 5 seed ridge: chỉ GPS, chỉ tile, đầu riêng–biểu diễn chung, stacking; thêm boosting 3 seed.

**Kết quả [ĐO]:** Spearman bốn ridge=0,7806/0,7955/0,7983/0,7955; chia sẻ tăng +0,0029. Boosting chỉ tile 0,7791, thêm GPS 0,7847. Hiệu trả được do đổi train GPS sang tile khoảng 0,015–0,017 theo bảng tham chiếu, không phải 0,1061.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Stacking cộng tuyến, không là một cải tiến độc lập. Không coi chênh tới mốc đo 0,9903 là phần học được; bằng chứng giữ vai trò chương đo lường theo DECISIONS.

**Bằng chứng và tái lập:** [transfer_experiment.py](../cross-assay-model-2026-10-15/transfer_experiment.py) · [README.md](../cross-assay-model-2026-10-15/README.md).

<a id="tn-32"></a>

#### TN-32 — Cổng phơi lộ trên protein nguyên vẹn và đối chứng bỏ PRKN

**Ngày / trạng thái:** 14/10/2026 · Còn liên quan; số chính chưa đủ điều kiện dùng.

**Lý do:** Kiểm cơ sở sử dụng rASA/pLDDT cho chuyển từ peptide sang protein.

**Dữ liệu:** MaveDB; 8 cấu trúc AlphaFold v6; phân tích chính 6 protein/33.718 missense khớp chuỗi.

**Cách làm:** Tính rASA Shrake–Rupley chuẩn Tien; lấy pLDDT; chia vùng; tương quan ΔPAP với nhãn; hồi quy tương tác; thử bỏ PRKN.

**Kết quả [ĐO]:** Spearman theo rASA từ −0,1928 (chôn) lên +0,3733 (phơi lộ); theo pLDDT <50/+0,3973 và ≥90/−0,1642. Hệ số tương tác ban đầu +0,6625 [0,627;0,700]; bỏ PRKN +0,5990 [0,546;0,648].

**Giới hạn / cách dùng [DIỄN GIẢI]:** KẾT QUẢ CẦN SỬA TRƯỚC KHI DÙNG: GCK khác assay, NUDT15/ASPA cần cấu trúc dimer. Giữ làm bằng chứng tiền đề có giới hạn, không dùng hệ số làm kết quả kiến trúc hoặc phát hiện mới.

**Bằng chứng và tái lập:** [architecture-check.json](../architecture-check/architecture-check.json) · [README.md](../architecture-check/README.md) · [prior-art-exposure-gate.md](../architecture-check/prior-art-exposure-gate.md).

<a id="tn-33"></a>

#### TN-33 — Liên hệ nhãn đoạn giữa Zhang và Voutsinos

**Ngày / trạng thái:** 14/10/2026 · Còn dùng.

**Lý do:** Kiểm cơ sở chia sẻ biểu diễn giữa hai nguồn nhãn.

**Dữ liệu:** PSI gốc scanning và tile Voutsinos chồng≥20 residue.

**Cách làm:** Ghép tọa độ; tính tương quan toàn bộ và trong nhóm degron; kiểm train PAP.

**Kết quả [ĐO]:** 2.726 peptide ghép được, Spearman 0,7333; chỉ degron 0,2921 (n=1.000). 770 peptide footprint có tile, 725 có tile train PAP.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Tương quan toàn cục không chứng minh có ích cho tác động vị trí hay mô hình đa nhiệm. Kết quả trong nhóm mới liên quan đến phân biệt mức độ giữa các degron.

**Bằng chứng và tái lập:** [architecture-check.json](../architecture-check/architecture-check.json) · [README.md](../architecture-check/README.md).

<a id="tn-34"></a>

#### TN-34 — Audit bộ nhân Larsen và chồng gene

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Xác định dữ liệu chuyển ngăn và hạn chế độc lập.

**Dữ liệu:** Larsen transfac_tiles.csv.gz tag v1.0; GPS Zhang; gene/library Voutsinos.

**Cách làm:** Đếm điểm hợp lệ, reliability, rASA/pLDDT; tính tương quan cột PAP; lấy giao gene/ENSG.

**Kết quả [ĐO]:** 63.258 dòng; 59.016 tile có điểm/sai số, 1.627 gene; reliability=0,9701; Pearson PAP–degron=−0,7899; 52.441 tile có rASA. Audit giao dùng danh mục 1.626 TF: 1.583 có trong GPS, 508 trong quét; 230/242 TF dùng chung với Voutsinos thuộc train PAP.

**Giới hạn / cách dùng [DIỄN GIẢI]:** 1.626 ở danh mục TF và 1.627 gene của file là hai mẫu số, không tự gộp. Giao theo gene không là trùng chuỗi chính xác. Chưa có thí nghiệm mô hình mới chuyển sang Larsen; giấy phép dữ liệu còn theo mục chờ ngoài ở DECISIONS.

**Bằng chứng và tái lập:** [README.md](../larsen-nuclear-and-risks-2026-10-15/README.md) · [SOURCE.md](../../data/raw/larsen-2025/SOURCE.md).

### Phạm vi và ý nghĩa

<a id="tn-35"></a>

#### TN-35 — Ánh xạ ClinVar, độ phủ đúng vị trí và đúng thay thế

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Đo có bao nhiêu biến thể thật nối được với nhãn ΔPSI.

**Dữ liệu:** ClinVar variant_summary snapshot 12/10; UniProt; 7 tầng quét/bão hòa/GPS.

**Cách làm:** Khử trùng VariationID; kiểm axit amin gốc; map theo tọa độ; phân biệt trong peptide, vị trí có đo và đúng ô thay thế.

**Kết quả [ĐO]:** 2.564.486 missense; 2.349.511 khớp UniProt trong phần đối chiếu, 176.901 lệch tọa độ bị loại. Bão hòa đúng ô 575 (486 VUS), quét 1.037 (871 VUS). Gọi tổng ≈1.600 vì chưa khử giao.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là độ phủ, không phải năng lực phân loại bệnh. Không cộng 575+1.037 thành số biến thể duy nhất khi chưa dedup giao.

**Bằng chứng và tái lập:** [coverage.json](../variant-coverage-2026-10-15/coverage.json) · [coverage.py](../variant-coverage-2026-10-15/coverage.py) · [README.md](../variant-coverage-2026-10-15/README.md).

<a id="tn-36"></a>

#### TN-36 — Miền áp dụng và mức mới so với tập nhãn

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Kiểm độ lớn không gian chưa có nhãn cần tổng quát hóa.

**Dữ liệu:** GPS Table S1, reads≥10; so tập residue với protein/cụm cov80.

**Cách làm:** Lọc tile PSI≤3; đếm protein, cụm, biến thể ClinVar; so đã/chưa thấy.

**Kết quả [ĐO]:** 116.702 tile/17.287 protein; 87,3% cụm chưa thấy; 67,9% tile nằm trên protein chưa thấy; 530.412 VUS ở vùng này.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không đồng nghĩa dự đoán đã đúng cho 530.412 VUS hay nhãn mức ô có sẵn cho toàn miền.

**Bằng chứng và tái lập:** [coverage.json](../variant-coverage-2026-10-15/coverage.json) · [README.md](../variant-coverage-2026-10-15/README.md).

<a id="tn-37"></a>

#### TN-37 — Giàu biến thể gây bệnh ở mức vùng và đối chứng vị trí

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Kiểm tính cấp thiết bằng số thay vì ví dụ đơn lẻ.

**Dữ liệu:** ClinVar gây bệnh/lành tính và tile GPS.

**Cách làm:** So tỉ lệ tile với tỉ lệ biến thể ở 3 ngưỡng; bảng chéo trong/ngoài degron; Mantel–Haenszel theo protein và cụm.

**Kết quả [ĐO]:** PSI≤3: 32,4% tile và 33,4% biến thể, chưa chứng minh điểm nóng. OR thô=2,096; theo protein=2,148 [2,072;2,227], 3.114 tầng; theo cụm=2,094 [2,024;2,167].

**Giới hạn / cách dùng [DIỄN GIẢI]:** OR là tỉ số chênh, không là xác suất hay bằng chứng gây bệnh vì phá degron. Chưa khử bảo tồn/vô trật tự; giữ giới hạn theo DECISIONS.

**Bằng chứng và tái lập:** [enrichment.json](../variant-coverage-2026-10-15/enrichment.json) · [enrichment.py](../variant-coverage-2026-10-15/enrichment.py) · [README.md](../variant-coverage-2026-10-15/README.md).

<a id="tn-38"></a>

#### TN-38 — Tín hiệu bệnh tại vị trí/ô ΔPSI

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Kiểm liên hệ mức vùng có giữ ở độ phân giải đầu ra mô hình không.

**Dữ liệu:** ClinVar map quét/bão hòa; 620 cụm ở tầng khớp vị trí.

**Cách làm:** Kiểm nhị phân footprint; AUC liên tục giữa gây bệnh/lành tính; bootstrap cụm 2.000 lần; so trong cùng peptide.

**Kết quả [ĐO]:** OR footprint=0,777 [0,530;1,139]. AUC scan_pos=0,5166 [0,479;0,554], scan_exact=0,5195 [0,400;0,645], sat_exact=0,6738 [0,489;0,831] (51 ca). Trong cùng peptide: +0,033 [−0,079;0,141], 51,2% dương.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Chưa thiết lập liên hệ bệnh mức residue; không dùng ClinVar làm đích xác nhận mô hình. Không trích 0,6738 bỏ CI.

**Bằng chứng và tái lập:** [delta-psi-test.json](../variant-coverage-2026-10-15/delta-psi-test.json) · [delta_psi_test.py](../variant-coverage-2026-10-15/delta_psi_test.py) · [enrichment.json](../variant-coverage-2026-10-15/enrichment.json).

<a id="tn-39"></a>

#### TN-39 — Kiểm vùng kinh điển và giới hạn assay

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Tránh chọn ví dụ/đối chứng ngoài phạm vi dữ liệu đo được.

**Dữ liệu:** GPS control hai replicate, MLN4924; vùng CTNNB1, MYC, NFE2L2, HIF1A và các vùng được audit.

**Cách làm:** Tra reads, PSI theo tile và điều kiện, tách không có dữ liệu khỏi phép đo âm.

**Kết quả [ĐO]:** CTNNB1 tile24–51 reads145/66, PSI5,27/5,36: đo được nhưng không là degron theo ngưỡng. MYC tile47–74 không có reads; NFE2L2 PSI3,59/4,46. HIF1A tile553–580 PSI1,86/1,51, tăng lên2,45 với MLN4924. Nhãn Oncogenicity trong saturation=0.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Không quy vắng reads thành âm sinh học; cơ chế giải thích cần nguồn riêng. Kết quả giữ làm ranh giới phạm vi, không hồi sinh đối chứng CTNNB1 đã không dùng theo DECISIONS.

**Bằng chứng và tái lập:** [coverage.json](../variant-coverage-2026-10-15/coverage.json) · [README.md](../variant-coverage-2026-10-15/README.md).

<a id="tn-40"></a>

#### TN-40 — Ví dụ ma trận HIF1A và map từ nhãn thật

**Ngày / trạng thái:** 15/10/2026 · Còn dùng.

**Lý do:** Minh họa đúng cấu trúc đầu ra bằng dữ liệu thực, kiểm cách đọc hình.

**Dữ liệu:** Q16665_HIF1A_25 saturation, vị trí protein553–580.

**Cách làm:** Dùng loader benchmark; chỉ peptide≥500 ô; xếp số ô dương giảm dần, hòa theo id; tạo heatmap và trung bình hàng.

**Kết quả [ĐO]:** 529 ô đo/186 ô dương; PSI đối chứng nội tại2,186; ΔPSI −0,515…+3,107; vùng10–14 nổi bật; vị trí12 có19/19 thay thế làm bền.

**Giới hạn / cách dùng [DIỄN GIẢI]:** Đây là ví dụ NHÃN, không là dự đoán hay tập test mới độc lập. Đối chiếu motif từ y văn không là phát hiện mới của đề tài.

**Bằng chứng và tái lập:** [example-matrix.json](../slide-figures-2026-10-15/example-matrix.json) · [make_example_matrix.py](../slide-figures-2026-10-15/make_example_matrix.py) · [README.md](../slide-figures-2026-10-15/README.md).

### Hỗ trợ tái lập

<a id="tn-41"></a>

#### TN-41 — Khử trùng MaveDB và đo tài nguyên ESM

**Ngày / trạng thái:** 11–14/10/2026 · Còn dùng.

**Lý do:** Đếm đúng dữ liệu ngoài và đánh giá chi phí biểu diễn trước khi dùng.

**Dữ liệu:** 26 score set/9 gene MaveDB; ESM-2 35M/650M; CPU Ryzen5 5500U.

**Cách làm:** Gộp HGVS theo gene, loại _wt/_sy; benchmark tốc độ embedding và ước lượng cache.

**Kết quả [ĐO]:** MaveDB:160.491 dòng→76.194 biến thể duy nhất theo audit mới. ESM35M/650M≈64,6/5,3 tile/s; cache residue toàn thư viện ước12,2/32,7GB.

**Giới hạn / cách dùng [DIỄN GIẢI]:** 69.209 của audit sớm dùng tập khác, không dùng làm số toàn bộ hiện tại. Benchmark ESM không chứng minh PLM tốt hơn one-hot; thời gian/cache phụ thuộc máy và biểu diễn.

**Bằng chứng và tái lập:** [mavedb-audit.json](../full-data-audit/mavedb-audit.json) · [mavedb_audit.py](../full-data-audit/mavedb_audit.py) · [esm-bench.json](../voutsinos-2026-audit/esm-bench.json).

## 5. Phần đã có thiết kế nhưng chưa có kết quả hoàn chỉnh ở mốc chốt

| Việc | Bằng chứng tại mốc chốt | Cách ghi trong báo cáo |
|---|---|---|
| E3 nhánh mở rộng: train kiến trúc Degformer từ đầu trên cùng ngân sách saturation/cov80 | [Tiền đăng ký](../g2-extension-2026-10-18/PREREGISTRATION.md) và script đã có; chưa có `e3-*.json` kết quả cuối tại lúc chốt | **Chưa đưa điểm vào bảng kết quả**. Một seed, trần 30 epoch/patience6 theo thiết kế; khi có số phải ghi rõ không tương đương retrain toàn bộ 569.270 dòng gốc |
| Sửa tiền đề cấu trúc sau bỏ GCK, dùng dimer NUDT15/ASPA | Báo cáo cấu trúc đã ghi nợ phương pháp; chưa có lượt sửa hoàn chỉnh ở hồ sơ đã đọc | Không dùng hệ số +0,6625 làm kết quả đã xác nhận |
| Đối chứng enrichment có khử bảo tồn/vô trật tự | Nợ phương pháp trong báo cáo ClinVar và [theo dõi chính thức](../../../../DECISIONS.md#doi-chung-cap-thiet) | OR2,148 chỉ là liên hệ mức vùng theo các biến đã kiểm |
| Mô hình mới đánh giá chuyển sang Larsen | Có audit dữ liệu/PAP cột có sẵn, chưa có benchmark mô hình đề tài chuyển ngăn hoàn chỉnh | Không gọi audit là kết quả chuyển ngăn của kiến trúc mới |
| PLM so với one-hot, MIL/giám sát yếu so với đầu theo vị trí | Có lập luận/khảo sát, chưa có phép so hoàn chỉnh được báo cáo | Không tính vào các thí nghiệm đã có kết quả |
| Xác nhận cuối cùng và sản phẩm dịch vụ | Chưa có untouched external benchmark hay kết quả vận hành ứng dụng trong nguồn đã đọc | Không chuyển OOF phát triển thành kết luận nghiệm thu; tra DECISIONS về điều kiện |

Đây là danh mục thiếu bằng chứng trong hồ sơ, không giao việc mới, không thay kế hoạch chính thức.

## 6. Bằng chứng lịch sử giữ để truy vết, không làm mục tiêu hiện tại

| Phép kiểm cũ | Phần còn liên quan | Điều không tiếp tục dùng |
|---|---|---|
| Gán E3 từ 31 CRISPR screen, quét 36 bộ ngưỡng | 27 peptide gán được, 25 rõ, 10 E3; số E3≥5 peptide luôn bằng1. Giải thích vì sao không dùng nhánh học đặc hiệu nhiều E3; 23 peptide có cả gán E3 và bão hòa là ca nhỏ | Không khôi phục mô hình FiLM điều kiện danh tính E3 thành nhiệm vụ chính; khác gate theo cặp thay thế của 18/10 |
| Oracle P@3 0,6045/0,7792 | Giới hạn biểu diễn lý tưởng trên nhãn, TN-09/13 | Không làm headline test hoặc “dư địa chắc chắn” |
| Phân rã cross-assay +0,1061 và “trần0,9903 là dư địa” | Phép thử đã dẫn tới đối chứng train đúng assay, TN-31 | Không quy toàn bộ +0,1061 thành effect assay; không hứa đạt trần đo |
| Đổi pooling PAP không train lại | Chẩn đoán mô hình frozen, TN-12 | Không làm bằng chứng kiến trúc max/top-k huấn luyện từ đầu sẽ kém |
| Checkpoint Degformer điểm cao | Baseline có tiếp xúc dữ liệu; TN-25/26 | Không gọi clean test theo peptide/protein/cụm, kể cả khi lọc exact ô |
| Đối chứng CTNNB1 | Phép đo âm của tile xác lập giới hạn assay, TN-39 | Không dùng làm ca kỳ vọng mô hình bắt được degron theo cơ chế ngoài assay |

Chi tiết CRISPR: [báo cáo](../e3-labels-audit/README.md), [gán E3](../e3-labels-audit/e3-assignment.json), [quét ngưỡng](../e3-labels-audit/e3-threshold-sweep.json), [giao tập](../e3-labels-audit/overlap-audit.json). Căn cứ phạm vi hiện hành tra [D-031](../../../../DECISIONS.md#d-031), [D-035](../../../../DECISIONS.md#d-035), [D-036](../../../../DECISIONS.md#d-036); không ghi lại quyết định trong báo cáo này.

## 7. Số liệu mâu thuẫn, số đã bị thay và giới hạn truy vết

| Vấn đề | Bằng chứng ưu tiên ở lượt tổng hợp | Cách sử dụng |
|---|---|---|
| Báo cáo residue ghi PAP Spearman0,3553 là mức vị trí | `pap-baseline.json`: `cell_level.dPAP_cnn2w1_spearman=0.3553`; `position_level.dPAP_cnn2w1_spearman=0.4130` | Không lặp phép so sai0,4440 vs0,3553 cùng mức vị trí. Muốn khẳng định chênh phải chấm trên cùng tập/cách gộp |
| Bảng residue PSI≤2,5 ghi9 peptide | `ladder.json`:38 peptide,20.019 ô | Dùng38 ở báo cáo tổng hợp; ngưỡng chính≤3 vẫn91 peptide thống nhất |
| MaveDB69.209 vs76.194 | Audit 13/10 trên26 score set/bảng điểm thật:76.194 sau quy tắc dedup | Số69.209 thuộc audit sớm phạm vi khác; không xem là đo lại cùng mẫu số |
| “Scanning gần như toàn bộ→R”, “19 thay thế đều chưa thấy” | Dữ liệu mô tả nhiều quy tắc opposite-scanning và ngoại lệ; TN-13 | Chỉ nói quét thử một thay thế/vị trí, ít loại thay thế hơn bão hòa; không tự ghi tỉ lệ R chưa kiểm |
| 75,9% nhiễu quét vs16,7% nhiễu bão hòa | Khác mẫu số: phần dư sau oracle vs phương sai quan sát | Ghi đầy đủ mẫu số, không trình bày thành một phép so tỉ lệ trực tiếp |
| Những câu “chưa học bão hòa”, “chưa chạy Degformer” trong báo cáo15/10 | Báo cáo/JSON18/10 và tiến độ chính thức đã có lượt mới | Chỉ còn đúng với thời điểm lịch sử; headline hiện tại dùng TN-23…27 |
| “Offset giải thích tối đa6%” | Chỉ có biến thiên theo offset0,0044 so khoảng cách0,0773 | Xem là chẩn đoán độ nhạy; phép so này không cho cận nhân quả tác dụng hai residue thêm |
| Một số tài liệu cũ ghi đề xuất còn chờ/đề tài đã chốt theo câu chữ lịch sử | DECISIONS là nguồn thẩm quyền hiện hành | Không dùng status lịch sử để đổi phạm vi hoặc ghi GVHD đã duyệt |
| JSON/README nhánh mở rộng có nhưng chưa có validation tổng kết | E1/E2 có kết quả tại mốc chốt; E3 còn thiếu kết quả cuối | Ghi rõ từng phần; không suy E3 đã xong từ tiến trình/log; cập nhật snapshot khi E3 và validation hoàn chỉnh |

Báo cáo này **không sửa lại các file nguồn lịch sử hoặc slide**. Khi trích lại vào bài viết, phải giữ phần giới hạn cạnh con số và dẫn đúng file JSON/cách chấm.

## 8. Tái lập và cập nhật hồ sơ

1. Đọc mục nguồn của thí nghiệm, script và protocol trước khi chạy; dữ liệu/raw không được thay bằng số trong báo cáo này.
2. Dùng lệnh trong README từng pipeline: [PSI/nhãn](../full-data-audit/README.md), [PAP](../pap-baseline/README.md), [residue15/10](../residue-task-derisk-2026-10-15/README.md), [bão hòa18/10](../g2-saturation-2026-10-18/README.md), [mở rộng](../g2-extension-2026-10-18/PREREGISTRATION.md), [ClinVar](../variant-coverage-2026-10-15/README.md).
3. Giữ raw data/checkpoint trong `data/`, không chép vào báo cáo. Dự đoán OOF, ensemble và nhãn phải có cùng tập ô khi so sánh.
4. Khi có kết quả mới, thêm ngày/chế độ giám sát, cập nhật bằng chứng và manifest; giữ mục lịch sử bị thay để truy vết. Không sửa điều kiện G2 trong báo cáo.
5. Lượt lập báo cáo chỉ kiểm đọc nguồn, số headline, schema hồ sơ và link; không tuyên bố tái huấn luyện. Kết quả kiểm riêng ở [VALIDATION.md](VALIDATION.md).
