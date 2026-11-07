# Audit khoảng trống giữa thành phần amino acid và ngữ cảnh degron

Ngày thực hiện: **12/10/2026**. Phạm vi: tải lại dữ liệu, đo giới hạn biểu diễn và kiểm tra quy mô chia tập; **không huấn luyện mô hình**. Đây là bằng chứng để khảo sát đề tài, không phải quyết định thay kiến trúc đã được duyệt.

## 1. Phán quyết

**Tiếp tục khảo sát degron với trọng tâm dự đoán ảnh hưởng đột biến có ngữ cảnh.** Khoảng trống được lượng hóa trên nhãn quét, và dữ liệu không dồn vào vài protein. Tuy nhiên, oracle của họ mô hình chỉ dựa thành phần đã khá mạnh: precision@3 tối đa kỳ vọng **0,6045**, so với oracle không ràng buộc **0,7792**. Khoảng chênh **0,1747** là dư địa trên nhãn hiện có, không phải cải thiện chắc chắn học được.

Không nói "PAP không dự đoán được footprint", "bản đồ PAP phải phẳng", "ΔPAP là ma trận hạng 1", hoặc "kiến trúc mới chắc chắn không thắng điểm toàn đoạn". Không suy ra cơ chế sinh học hay hiệu năng mô hình từ các oracle dùng nhãn đánh giá.

## 2. Nguồn và tái lập dữ liệu

- [Mendeley Data 10.17632/32h94v2yv2.2](https://data.mendeley.com/datasets/32h94v2yv2/2), CC BY 4.0.
- `I28 Scanning Mutagenesis.zip`: **27.939.862 B**, SHA-256 `a82bd1ee4bc7a2da69df06cb44dd34fe8480c6fd799340684f5058d02223df50`.
- `I28 CRL Saturation Mutagenesis.zip`: **5.224.902 B**, SHA-256 `cbda58342265dd73b7946cd091c5b558eed6e615bbcb97921e37bd50fbb5ee60`.
- Tệp chính: `Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv`.
- Dữ liệu thô, manifest và dữ liệu dẫn xuất nằm trong `topics/degron-footprint/data/{raw,interim,processed}/`, bị loại khỏi Git. Tệp kết quả nhỏ nằm trong [ghi chú audit](e3-labels-audit/).

Đếm lại bằng script cũ tái lập **đúng toàn bộ** bảng counts: 8.831 peptide có WT và đột biến đạt lọc; 3.439 degron; 3.415 đủ độ phủ; **2.624 footprint**, trong đó **2.402 khu trú**. Có 283.880 dòng và **256.711** dòng PSI/read đạt lọc. Đây là số dòng đo, không phải số mẫu sinh học độc lập.

Ngưỡng giữ nguyên audit trước: reads ≥10, PSI WT ≤3,0, ≥21 vị trí đo được; vị trí dương nếu ΔPSI = PSI(mutant) − PSI(WT) ≥1,0.

## 3. Điều kiện bất biến chính xác

Với peptide có thành phần `c`, đột biến vị trí `i` từ `a` sang `b` cho:

`Δf_i(a→b) = f(c − e_a + e_b) − f(c)`.

Trong **cùng peptide**, mọi vị trí có cùng **cặp (a,b)** phải nhận cùng dự đoán nếu mô hình chỉ dùng thành phần. Các peptide khác nhau vẫn có thể nhận giá trị khác vì `c` khác, nhất là khi `f` phi tuyến.

**Vì sao phải gom theo cặp thay thế:** kiểm tra thực tế có **876** đột biến đạt lọc khác quy tắc opposite-scanning thông thường, tại vị trí 25–27. **242/2.624** footprint có cùng residue WT nhưng nhiều residue thay vào. Gom chỉ theo WT sẽ trộn ảnh hưởng của đích thay thế với ngữ cảnh vị trí. Không có lỗi về vị trí: mọi biến thể được kiểm đều thay đúng một vị trí được khai báo.

Chẩn đoán chỉ gom WT vẫn được lưu: 2.059 peptide có khoảng chênh ≥1,0 và oracle P@3 kỳ vọng 0,6012. **Không dùng nó làm cận trên chung cho mô hình thành phần khi `b` khác nhau.**

Cận ở báo cáo này áp cho **mô hình thành phần thuần túy**. Kênh nội `cnn2w1` của PAP có tính chất này trong vùng nó đọc; PAP đầy đủ có thêm kênh C-terminal, nên không gán cận toàn bộ 28 vị trí này cho PAP đầy đủ. Cũng không gán cho các mô hình có thêm đặc trưng vị trí hoặc ngữ cảnh.

## 4. Kết quả trên 2.624 footprint

| Phép đo | Kết quả |
|---|---:|
| Peptide có cùng cặp thay thế nhưng khoảng chênh ΔPSI ≥1,0 | **2.046 / 2.624 = 78,0%** |
| Peptide có một nhóm cùng cặp chứa cả vị trí dương và không dương | **2.353 / 2.624 = 89,7%** |
| Trung vị khoảng chênh lớn nhất trong nhóm cùng cặp | **1,3068 PSI** |
| Phần phương sai ΔPSI còn lại sau oracle trung bình theo cặp — trung bình theo peptide | **35,0%** |
| Spearman của oracle trung bình ΔPSI theo cặp — trung bình theo peptide | **0,7585** |
| Spearman của oracle trung bình rank theo cặp — trung bình theo peptide | **0,7718** |
| Cận trên Spearman từ phép nới lỏng Cauchy–Schwarz — trung bình theo peptide | **0,7931** |
| Precision@3 của oracle trung bình ΔPSI theo cặp | **0,5481** |
| Cận trên **chính xác của kỳ vọng** precision@3 với score hằng trong nhóm cùng cặp | **0,6045** |
| Oracle precision@3 không ràng buộc theo nhóm | **0,7792** |
| Precision@3 kỳ vọng khi chọn ngẫu nhiên | **0,1204** |

Nguồn số: [composition-audit.json](e3-labels-audit/composition-audit.json). Các chỉ số là trung bình macro theo peptide; không coi các vị trí trong một peptide là các mẫu độc lập. Oracle dùng nhãn của chính peptide đang chấm và là đối chứng lý tưởng, **không phải kết quả test của PAP hay mô hình học được**.

### 4.1 Oracle trung bình và cận trên là hai đối tượng khác nhau

Trung bình theo nhóm tối ưu **squared error**, nhưng không tối ưu Spearman hay precision@3. Vì vậy không gọi chỉ số của oracle trung bình là "trần trên tuyệt đối".

Gọi `r` là rank trung bình khi có tie của nhãn ΔPSI, `m_g = mean(r_i | group g)`. Với mọi score dự đoán hằng trong từng nhóm, rank dự đoán cũng hằng trong nhóm. Phép chiếu trực giao và Cauchy–Schwarz cho:

`Spearman ≤ sqrt[Σ_i (m_g(i) − mean(r))² / Σ_i (r_i − mean(r))²]`.

Đây là **cận trên hợp lệ do nới lỏng**, chưa chắc có một thứ tự rank đạt được nó. Báo cả oracle đạt được và cận để không nhầm hai thứ.

Với precision@3, tie được xử lý bằng **kỳ vọng chọn đều ngẫu nhiên**, không chọn vị trí đúng bằng cách nhìn nhãn. Với nhóm có `n` vị trí, `t` dương, chọn `q` vị trí đóng góp kỳ vọng `q*t/n`. Tối ưu bằng quy hoạch động trên các nhóm được lấy trọn và một nhóm cuối lấy một phần. Đây là cận kỳ vọng chính xác trong lớp score hằng theo cặp, với oracle được tự chọn thứ tự nhóm trên từng peptide.

Oracle không ràng buộc chỉ đạt 0,7792 vì nhiều peptide có <3 vị trí dương; nó không thể chọn ba vị trí dương khi chỉ có một hoặc hai. Không lấy 1,0 làm mốc attainable cho toàn bộ tập này.

### 4.2 Giới hạn suy luận sinh học

Các khác biệt trên là khác biệt **nhãn quan sát**. Dữ liệu lấy một replicate, reads tối thiểu thấp, và nhãn genotype BAG6 của replicate này chưa rõ. Chưa tách phần ngữ cảnh có thể học khỏi nhiễu đo. Cần kiểm lặp lại, độ sâu reads và tính ổn định trước khi gọi phần dư là tín hiệu sinh học hoặc hứa cải thiện 0,1747.

Tập 2.624 đã được chọn theo tồn tại footprint; chỉ số của nó không mô tả toàn bộ proteome. Đánh giá mô hình tương lai cần cả peptide không có footprint để đo cảnh báo vị trí sai.

## 5. Protein và phép chia tập theo cụm đồng dạng

- **9.817 peptide / 6.582 accession protein** trong thư viện.
- **8.831 peptide đạt lọc / 6.081 accession protein**.
- **2.624 footprint / 2.232 accession protein**; median 1 footprint/protein, tối đa **7**, tức protein lớn nhất chỉ chiếm **0,267%** số footprint. Đây là số accession, không đồng nhất với gene phân biệt.
- Truy được trình tự UniProt hiện tại cho **6.573/6.582** accession. Chín accession chưa lấy được bị loại khỏi phép chia theo cụm, **không giả làm singleton độc lập**.
- Sau bỏ một ký hiệu stop `*` cuối khi đối chiếu: **9.759** peptide WT và **2.602** footprint nằm nguyên vẹn trong trình tự protein tham chiếu. Có **19** footprint đã map accession nhưng chưa khớp peptide, cộng **3** footprint thiếu trình tự; cần curate.
- **813** peptide WT, trong đó **336 footprint**, có stop cuối. Không coi `*` là amino acid; đầu ra ma trận phải mask vị trí không hợp lệ.

Gom cụm **protein nguyên vẹn**, MMseqs2 `6f45232ac8daca14e354ae320a4359056ec524c2`, identity ≥30%, coverage hai chiều, connected-component clustering, single step, sensitivity 7,5, max-seqs 10.000. Không gom 28-mer rồi gọi đó là kiểm soát đồng dạng protein. [Tài liệu MMseqs2](https://github.com/soedinglab/MMseqs2/wiki).

| Coverage hai chiều | Cụm protein | Protein trong cụm lớn nhất | Footprint test theo accession map | Footprint test chỉ giữ peptide khớp tham chiếu |
|---|---:|---:|---:|---:|
| ≥80% | **5.088** | **80** | **272–323** | **271–322** |
| ≥50% | **4.418** | **124** | **224–303** | **221–301** |

Chia **80/10/10 theo số cụm**, seeds `0,42,87,1001,12345`. Đây là các phép chia thử để đo quy mô, **chưa là benchmark chính thức được chốt**; không chọn seed có kết quả đẹp. Ở seed 42, test khớp tham chiếu có **274** footprint với coverage 80%, **221** với coverage 50%.

Nguồn: [cov80](e3-labels-audit/composition-audit.json), [cov50](e3-labels-audit/composition-audit-cov50.json), [metadata cụm cov80](e3-labels-audit/protein-clusters-cov80.json), [metadata cụm cov50](e3-labels-audit/protein-clusters-cov50.json).

**Kết luận về khả thi:** chưa thấy hiện tượng footprint dồn vào vài protein làm test sụp. Các cụm dùng trình tự canonical hiện tại và alignment heuristic; chưa chứng minh không có liên hệ đồng dạng giữa mọi cặp khác cụm. Trước benchmark chính thức cần kiểm cross-split ở cả protein và peptide, giữ các peptide trùng trình tự cùng phía, và liên kết với dữ liệu nhiệm vụ phụ/bão hòa.

## 6. Hướng ma trận thay thế: có lý do để thử, nhưng cần sửa phép phân rã

Đề xuất của sinh viên: chuyển đầu ra từ vector quét sang ma trận vị trí × amino acid thay vào, học từ scanning và saturation cùng lúc. **Đáng khảo sát**, vì hai nguồn nhãn cùng mô tả ảnh hưởng thay thế ở độ phủ khác nhau.

Ba điều chỉnh bắt buộc:

1. **Scanning là một ô quan sát trên mỗi hàng**, không phải marginal (tổng/trung bình hàng). Loss phải đọc đúng ô `M[i,b_i]` theo thay thế thực tế trong CSV; các ô còn thiếu không được gán 0.
2. **ΔPAP không phải hạng 1 nói chung.** Ngay mô hình tuyến tính `f(c)=w·c` cho `M[i,b]=w_b−w_a(i)`, là tổng của hai outer products nên hạng tối đa 2. Ví dụ `w(A,B,C,D)=(0,1,2,3)` cho ma trận con `[[2,3],[1,2]]` có định thức 1, hạng 2. `f` phi tuyến có thể cho hạng cao hơn. Bất biến đúng là **các hàng cùng WT có cùng đáp ứng khi so cùng cột thay vào**, không phải mọi vị trí có độ nhạy hằng.
3. Để giữ cột hóa học nhất quán, dùng nội bộ **tối đa 28×20**, đặt/mask ô WT→WT, stop và dữ liệu thiếu; giao diện có thể hiển thị 19 thay thế thật trên mỗi residue. Không xếp 19 cột khác nhau ở từng hàng rồi phân rã như thể chúng có cùng identity.

Một không gian thiết kế trung thực:

`M[i,b] = B(c,a_i,b) + Σ_q U[i,q](sequence) V[b,q](sequence)`.

`B` là nhánh chỉ dựa thành phần hoặc baseline ΔPAP phù hợp; phần sau là hiệu chỉnh theo ngữ cảnh. Ablation: **B → B + hiệu chỉnh hạng 1 → B + hạng r cao hơn**, với cùng split và ngân sách. Giữ đối chứng decoder theo vị trí/thay thế không phân rã. Đây là phương án đề xuất, chưa có kết quả và chưa xác lập tính mới.

Với chỉ một ô/hàng, các nhân tố không tự nhận diện được; cần chia sẻ tham số giữa peptide/loại amino acid hoặc prior, và nhãn saturation đủ chất lượng để kiểm chứng. Hai assay cần chuẩn hóa/đầu đo theo nguồn nếu có khác biệt điều kiện. Dữ liệu bão hòa có **249 peptide / 135.040 định danh**, chưa đồng nghĩa mọi ô đều có ΔPSI đạt chất lượng; chỉ **219** footprint được tác giả curate. Phải xử lý score và quan hệ trùng peptide/protein/cụm **trước** khi chia train/validation/test cho cả hai nguồn. Nếu saturation được dùng để train, không được tiếp tục gọi toàn bộ 249 peptide là test độc lập.

Không nói "chưa ai làm thế cho degron" như một sự thật đã xác lập. Tra cứu ngày 12/10 chưa tìm được tiền lệ đúng thiết kế trên, nhưng dự đoán ô thay thế còn thiếu đã có tiền lệ ngoài degron, ví dụ [khung DMS targeted substitution profiling, 2026](https://pubmed.ncbi.nlm.nih.gov/42157089/). Cổng cấu trúc giữ ở mở rộng, không là thành phần bắt buộc của audit này.

## 7. Chạy lại và kiểm tra

Từ root, môi trường Python có `requests`, MMseqs2 trên PATH:

```bash
python3 topics/degron-footprint/research/e3-labels-audit/fetch_scanning.py
python3 topics/degron-footprint/research/e3-labels-audit/audit_composition.py
python3 topics/degron-footprint/research/e3-labels-audit/prepare_protein_clusters.py --coverage 0.8
python3 topics/degron-footprint/research/e3-labels-audit/audit_composition.py --clusters topics/degron-footprint/data/interim/protein-id30-cov80_cluster.tsv
python3 topics/degron-footprint/research/e3-labels-audit/prepare_protein_clusters.py --coverage 0.5
python3 topics/degron-footprint/research/e3-labels-audit/audit_composition.py --clusters topics/degron-footprint/data/interim/protein-id30-cov50_cluster.tsv --output topics/degron-footprint/research/e3-labels-audit/composition-audit-cov50.json
python3 topics/degron-footprint/research/e3-labels-audit/validate_composition.py
```

`audit_composition.py` và validator chỉ dùng thư viện chuẩn. Fetcher/sequence preparation dùng `requests`. UniProt hiện tại có thể đổi ở lần tải sau; manifest ghi URL, release và SHA-256, cache cục bộ dùng lại. Raw Mendeley được pin đầy đủ SHA-256.

Đã kiểm: checksum hai ZIP; tái lập counts bằng script cũ; 200 đối chiếu exhaustive oracle P@3 với nhóm có kích thước thay đổi; 4.000 kiểm tra cận rank; đối chiếu Spearman với SciPy trong 100 trường hợp có tie; phản ví dụ hạng 2; compile bốn script. Không train, không chạy PAP để báo performance thực, không tự thay quyết định đề tài.
