# Bằng chứng wet lab và hiệu quả nguồn lực cho hướng degron-footprint

Ngày tra cứu: **07/11/2026**, múi giờ Asia/Taipei. Phạm vi: kế hoạch đã được duyệt
trong [README](README.md). Dữ liệu trích: [results.json](results.json),
[ma trận bằng chứng](evidence-matrix.csv), [nhật ký](search-log.csv).

## Tóm tắt

**Có bằng chứng wet lab từ các công trình khác cho việc dùng dự đoán degron để
đề xuất và kiểm tra mutation hoặc vùng protein. Chưa có bằng chứng trực tiếp
rằng CT553H tiết kiệm thời gian, chi phí thực nghiệm.** Năm nghiên cứu degron
được kiểm phần liên quan có đối chứng sinh học, nhưng không cung cấp phép đo
tiết kiệm nguồn lực bằng so sánh hai chiến lược chọn ứng viên trong những phần
đã đọc. Ba nghiên cứu protein engineering lân cận giúp phân biệt khả thi trong
phòng thí nghiệm với hiệu quả nguồn lực: SAMPLE có thời gian chạy thực và dự
toán chi phí, ALDE có số lượt sàng lọc thực cùng đối chứng ước lượng, còn một
benchmark cho thấy phương pháp dùng bất định không luôn hơn cách chọn đơn giản.
Các kết quả này hỗ trợ lập luận về tiềm năng ưu tiên ứng viên của đề tài, với
giới hạn về endpoint, lựa chọn case và mức độc lập dữ liệu. Chúng không thay
kiểm chứng CT553H, không cấp quyết định nghiệm thu G2 và không xác nhận ứng dụng
đã hoàn chỉnh. [S01–S08 trong danh mục dưới](#tai-lieu).

## 1. Câu hỏi và cách thực hiện

RQ: **Các nghiên cứu gốc về dự đoán degron cung cấp mức bằng chứng nào cho giá
trị ưu tiên ứng viên thực nghiệm có thể tham chiếu cho CT553H?**

Đã thực hiện tra cứu web theo các nhóm prediction/validation, ưu tiên mutation,
nguồn lực và phản chứng của kế hoạch; tìm thêm theo tên bài/DOI và các công
trình lân cận. Nhật ký giữ nguyên query và các trang được công cụ trả về. Đây
là **tra cứu có phạm vi, có kiểm nguồn**, không phải systematic review, không
có screening hai người độc lập hoặc ước lượng tỷ lệ bao phủ mọi cơ sở dữ liệu.
Khi query rộng trả nhiều kết quả ngoài degron, đã dùng các query có từ khóa
degron cụ thể; các kết quả ngoài phạm vi không được dùng để suy lợi ích dự án.

Tám nghiên cứu được đưa vào ma trận: năm gần degron và ba minh họa protein
engineering lân cận. Cùng study ở nhiều URL/phiên bản chỉ tính một lần. Bằng
chứng số được giữ theo đúng study, endpoint và mẫu số; không gộp tỷ lệ hoặc
tạo meta-analysis. Các đoạn đọc, phiên bản, xung đột lợi ích và giới hạn truy
cập nằm trong `results.json` và [biên bản kiểm](validation.md).

Mỗi claim được phân theo ba chiều: **đo sinh học gì**, **đo hoặc ước lượng nguồn
lực thế nào**, và **có phải kết quả trực tiếp của CT553H không**. Đối chứng WT
so với mutant trả lời chức năng sinh học; đối chứng model so với random/
heuristic mới trả lời lợi ích của cách chọn ứng viên. [DIỄN GIẢI PHƯƠNG PHÁP]

Cách đọc thuật ngữ: **wild type (WT)** là chuỗi gốc đối chiếu với chuỗi đột biến;
**cycloheximide (CHX)** dùng trong phép đo turnover; **out-of-fold (OOF)** là
dự đoán cho mẫu không nằm trong tập fit của fold đó. Tên protein như CBX6,
PNPO hoặc PTEN là định danh ca nghiên cứu. HiBiT, GPS, PAP, SAMPLE và ALDE là
tên assay/công cụ/phương pháp của từng bài; không phải phiên bản mô hình CT553H.

## 2. Những tiền lệ wet lab đã xác minh

### S01 — deepDegron: dự đoán dẫn tới chọn mutation để thử

Tokheim và cộng sự thử **21 peptide đầu/cuối dài 23 residue**: mutation làm
ổn định **8/12 ca C-terminal và 8/9 ca N-terminal**. Tổng là **16 ca xác nhận,
5 ca không xác nhận theo kết quả tác giả báo**; không gọi cả 21 ca là thành
công. Methods mô tả 10 loại motif mới, khác số peptide/protein được thử.

WT được so với double mutant; việc chọn mutation còn ràng buộc thay đổi điểm
composition. Đây là tiền lệ rõ cho model-guided follow-up. Mẫu được lựa chọn
theo tiêu chí mô hình, không phải phép so hit rate model–random trên cùng
candidate pool; không suy số giờ hay tiền tiết kiệm từ 16/21.
[Nguồn: Fig.4G; STAR Methods, Selection of deepDegron motifs for experimental validation](https://pmc.ncbi.nlm.nih.gov/articles/PMC9245451/).

### S02 — DEGRONOPEDIA: kiểm protein đầy đủ, nhưng case đã có dữ liệu trước

FBXL15 được kiểm bằng HiBiT, CHX chase và ức chế proteasome. Cách đặt tag ở hai
đầu cho kết quả phù hợp vai trò của C-terminus. **Tác giả nói rõ chọn FBXL15 vì
đã có dữ liệu ổn định của peptide C-terminal 23-mer**. Vì vậy đây là case
follow-up trên protein đầy đủ, không phải phép thử mù khả năng tìm mục tiêu mới.

Fig.4 có ba biological replicate; chúng không tạo thành ba protein ứng viên.
Case SDE2 kiểm lại cơ chế processing đã biết. Mục thời gian tính toán báo giây
chạy server, không đo thời gian wet lab giảm nhờ công cụ.
[Nguồn: FBXL15/SDE2 applications; Fig.4; Computation times](https://pmc.ncbi.nlm.nih.gov/articles/PMC11223883/).

### S03 — Degpred: mutation dự đoán liên quan turnover và tương tác

Với **một case CBX6/SPOP**, sửa vùng dự đoán làm CBX6 bền hơn trong phép đo
turnover và làm yếu tín hiệu co-immunoprecipitation. Tác giả cũng ghi nhận
tương tác chưa mất hoàn toàn. Kết quả hỗ trợ dùng dự đoán để kiểm vị trí chức
năng, không xác lập độ đúng của mọi cặp E3–degron hoặc lợi ích kinh tế. Lời
nêu tiết kiệm bước annotation là định tính, không phải đo chi phí/thời gian
thực nghiệm so đối chứng.
[Nguồn: Fig.5c,d; Discussion; CHX/co-IP Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC9281121/).

### S04 — PAP/Voutsinos: gần mutation-effect nhất, có giới hạn chuyển context

PAP được dùng để chọn/giải thích các mutation trong vùng lộ ra dung môi. Bài
báo có follow-up **PNPO D33V** trên protein đầy đủ và **hai mutation LAP3** làm
tăng abundance. Đây không phải thí nghiệm CT553H và không có mẫu số để tính
hit rate đại diện toàn bộ prediction.

Giới hạn cần giữ: một số mutation proline và vùng đuôi PTEN không tuân theo
quan hệ đơn giản giữa điểm peptide và abundance protein. **164 tile** đo ở
low throughput là validation riêng của screen/model, không phải 164 mutation
được mô hình ưu tiên thành công. Các số lượng tế bào FACS không thay số biological
replicate. [Nguồn: Results/Figs.5–6; Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880521/).

### S05 — Zhang/DegronID: dữ liệu và mô hình hỗ trợ kiểm giả thuyết sinh học

Nghiên cứu chọn **sáu protein** dựa trên motif, tương tác KLHL15 và độ nhạy trong
screen. ZNF511 được ổn định rõ khi knockout KLHL15; các protein khác thay đổi
nhẹ hơn. Có đối chứng protein không có motif/tương tác tương ứng. Không tự
chuyển mô tả này thành “6/6 hit” vì bài không đặt một ngưỡng thành công nhị phân
cho phép so đó.

Đây là nguồn nhãn của CT553H và tiền lệ dùng dữ liệu để kiểm giả thuyết; nó
không phải validation độc lập của mô hình CT553H. Đã phát hiện erratum liên
quan Fig.2A; báo cáo này không dựa vào hình chưa đối chiếu bản sửa.
[Nguồn: DegronID section/Fig.S5D, Limitations](https://www.timmslab.com/media/papers/2023_Mol_Cell_Elucidation_of_E3_ubiquitin_ligase_specificity_through_proteome-wide_internal_degron_mapping_naf6vNE.pdf);
[erratum](https://pubmed.ncbi.nlm.nih.gov/37977122/).

## 3. Bằng chứng nguồn lực: có số liệu, nhưng cần đọc đúng loại

### S06 — SAMPLE: số thực tế, dự báo và mô phỏng là ba lớp khác nhau

Nghiên cứu enzyme thermostability có **20 vòng thực nghiệm**, thời gian thực
**gần sáu tháng**, gồm **2,5 tháng chờ vận chuyển**. **Hai tháng** là ước lượng
cho lượt chạy được tổ chức tốt hơn; **6–12 tháng làm thủ công** cũng là ước
lượng, không phải nhánh đối chứng được chạy đồng thời.

Chi phí **5.200 USD** là dự toán một run 20 vòng, batch 3: DNA 2.400, thuốc thử
1.300 và cloud lab 1.500 USD. Đây là **chi phí run**, không phải 5.200 USD tiết
kiệm. Kết quả dùng ít mẫu hơn 3–4 lần thuộc **10.000 trial mô phỏng P450**,
tách với campaign GH1 wet lab. Quy trình kết hợp model, assay và robotics;
không gán toàn bộ hiệu quả cho predictor hoặc CT553H.
[Nguồn: Fig.1c,d; Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC10926838/).

### S07 — ALDE: workload đã đo, đối chứng chi phí còn mang tính giả định

ALDE báo **sáu plate 96-well qua ba vòng**: bốn plate random variants và hai
plate model-proposed. Không đổi số well thành số mutation độc lập hay số hit.
Tác giả so với khoảng năm vòng greedy directed evolution **sẽ cần thực hiện**;
phần đối chứng này là phản thực tế/ước lượng, không phải hai campaign được đo
song song. Tổng hợp DNA chính xác góp phần giảm sequencing và overscreening.

Kết quả là tiền lệ cho vòng model→thử→cập nhật và đo workload thực. Chưa có
phép so tiền/giờ có thể chuyển thẳng sang dự đoán ΔPSI.
[Nguồn: Discussion; Fig.4 phân biệt simulation](https://pmc.ncbi.nlm.nih.gov/articles/PMC11739421/).

### S08 — Phản chứng: thêm bất định không tự làm chọn ứng viên hiệu quả hơn

Benchmark của Greenman và cộng sự là **retrospective**, không làm wet lab mới.
Trong các phép so được xét, chọn bằng bất định không vượt greedy; một thiết
lập AAV còn kém random. Vì vậy cần giữ baseline chọn ứng viên đơn giản khi
đánh giá utility. Kết quả không có nghĩa mọi active learning đều thất bại.
[Nguồn: Bayesian optimization/Fig.6; Conclusions](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012639).

## 4. Kết luận cho CT553H và việc còn cần chứng minh

| Luận điểm | Mức được bằng chứng hỗ trợ |
| --- | --- |
| Dự đoán degron có thể dẫn tới mutation/vùng protein được kiểm chứng | **Có tiền lệ thực nghiệm bên ngoài**, với giới hạn chọn case và endpoint như S01–S05. |
| Mô hình CT553H đã được wet lab xác nhận | **Chưa có trong hồ sơ dự án**; không chuyển validation của PAP/deepDegron sang CT553H. |
| CT553H giảm số thí nghiệm cần làm | **Chưa đo trực tiếp**; metric OOF và enrichment chưa tương đương utility prospective. |
| CT553H tiết kiệm giờ hoặc tiền | **Chưa có số đo**; S06–S07 chỉ cung cấp cách báo nguồn lực và tiền lệ lân cận. |

[DIỄN GIẢI] Đóng góp hiện được bảo vệ bằng bằng chứng của CT553H vẫn là phương
pháp dự đoán/đánh giá có kiểm soát, cùng khả năng ưu tiên mutation **cần kiểm
chứng tiếp**. Nguồn ngoài bổ sung tính khả thi sinh học, không làm mô hình thành
công cụ quyết định wet lab đã được nghiệm thu.
[Hồ sơ G2](../g2-acceptance-2026-11-07/README.md) ghi bằng chứng development và
quyết định còn chờ; nghiên cứu tài liệu này không tự đóng G2 hoặc G3.

[ĐỀ XUẤT, CHƯA THỰC THI] Nếu cần lượng hóa utility ngay từ dữ liệu đã có, có
thể thiết kế replay việc ưu tiên mutation bằng **OOF**: cùng candidate pool,
cùng ngân sách chọn; so model đã khóa với random và baseline đơn giản; báo hit
rate/precision và số phép đo để đạt mức recall định trước. Chốt cách tính và
đơn vị bootstrap trước khi chấm. Vì dữ liệu development đã được khảo sát, phải
gọi đây là **đánh giá hồi cứu**, không phải kiểm chứng ngoài hoặc giờ/tiền tiết
kiệm thực tế. Lượt này không chạy replay.

[ĐỀ XUẤT, CHƯA THỰC THI] Muốn claim lợi ích thực nghiệm của CT553H cần lượt
chọn ứng viên và kiểm tra riêng: cùng ngân sách, có đối chứng chọn, quy tắc hit
chốt trước, giữ case thất bại. Đo tổng elapsed time, công lao động, vật tư,
tính toán, lần lặp lại và overhead; tách phần cố định/biến đổi. Nếu chỉ dùng
đơn giá giả định để quy đổi số assay thì kết quả là **ước lượng theo giả định**,
chưa phải tiết kiệm đã đo. Chưa có đối tác, ngân sách hay cam kết làm wet lab
được suy ra từ bản nghiên cứu này.

## 5. Giới hạn tìm kiếm và mức xác minh

- Đây là kiểm chứng có mục tiêu bằng web và nguồn gốc. Kết quả tìm có xếp hạng,
  nhiều trang không liên quan và không cung cấp tổng hit của từng database;
  không tuyên bố đã bão hòa toàn bộ literature.
- Phần chính của năm nguồn degron và ba nguồn lân cận đã được kiểm theo locator;
  không đọc hết mọi supplement, không tái phân tích blots hoặc số liệu tác giả.
  S01 Table S4G và S04 supplement bị challenge; S07 truy cập trực tiếp chập chờn.
- Bài ACS 2024 về thiết kế epitope bằng degron prediction là đầu mối liên quan,
  nhưng chưa đọc đủ bản journal vì giới hạn truy cập. Bản preprint khác không
  được dùng thay thế. Preprint genetic-glue tháng 09/2026 trả 403. Hai bài nằm
  ở `candidate_gaps`, chưa làm nguồn cho tỷ lệ hay kết luận định lượng.
- PDF Zhang tải từ trang tác giả có hash; preflight của skill báo **UNAVAILABLE**
  vì thiếu `pypdf`. Chỉ dùng section/figure locators, không chứng nhận page
  anchor. Erratum mới xác nhận metadata, chưa đối chiếu nội dung hình sửa.
- Các disclosure về công ty, patent và vai trò biên tập được giữ trong ma trận;
  không dùng disclosure để tự bác bỏ kết quả. Không thực hiện kiểm blacklist
  thương mại hoặc cấp chứng nhận không retraction cho các bài.
- Hai worker native dừng vì hạn mức trước khi hoàn tất file. Nguồn được chấp
  nhận cuối cùng do session chính kiểm lại; review/tổng hợp cùng ngữ cảnh,
  không độc lập và không cross-model. Không có API resolver tự động hoặc dữ
  liệu riêng của repo gửi tới dịch vụ mô hình ngoài.

**AI disclosure:** Codex hỗ trợ tra cứu, trích metadata/số liệu, tổng hợp và soạn
bản ghi này. Không có xác nhận người dùng đã đọc toàn bộ nguồn. Không chạy train,
suy luận mới, làm wet lab hoặc thay mô hình phục vụ. Các đề xuất trên chưa tạo
kết quả nghiên cứu mới của CT553H.

<a id="tai-lieu"></a>
## Tài liệu đã dùng

Thông tin tác giả đầy đủ theo nguồn đọc được giữ trong `results.json`; bảng
dưới dùng trích dẫn ngắn để dễ đối chiếu.

| ID | Nguồn gốc |
| --- | --- |
| S01 | Tokheim et al. (2021). *Systematic Characterization of Mutations Altering Protein Degradation in Human Cancers*. Molecular Cell, 81(6), 1292–1308.e11. [DOI](https://doi.org/10.1016/j.molcel.2021.01.020). |
| S02 | Szulc et al. (2024). *DEGRONOPEDIA: a web server for proteome-wide inspection of degrons*. Nucleic Acids Research, 52(W1), W221–W232. [DOI](https://doi.org/10.1093/nar/gkae238). |
| S03 | Hou et al. (2022). *Systematic prediction of degrons and E3 ubiquitin ligase binding via deep learning*. BMC Biology, 20, 162. [DOI](https://doi.org/10.1186/s12915-022-01364-6). |
| S04 | Voutsinos et al. (2026). *A near-complete map of human cytosolic degrons and their relevance for disease*. Science Advances, 12(6), eadz3483. [DOI](https://doi.org/10.1126/sciadv.adz3483). |
| S05 | Zhang et al. (2023). *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping*. Molecular Cell, 83(18), 3377–3392.e6. [DOI](https://doi.org/10.1016/j.molcel.2023.08.022). Erratum: [DOI](https://doi.org/10.1016/j.molcel.2023.10.021). |
| S06 | Rapp, J. T., Bremer, B. J., & Romero, P. A. (2024). *Self-driving laboratories to autonomously navigate the protein fitness landscape*. Nature Chemical Engineering, 1, 97–107. [DOI](https://doi.org/10.1038/s44286-023-00002-4). |
| S07 | Yang et al. (2025). *Active learning-assisted directed evolution*. Nature Communications, 16, 714. [DOI](https://doi.org/10.1038/s41467-025-55987-8). |
| S08 | Greenman, K. P., Amini, A. P., & Yang, K. K. (2025). *Benchmarking uncertainty quantification for protein engineering*. PLOS Computational Biology, 21(1), e1012639. [DOI](https://doi.org/10.1371/journal.pcbi.1012639). |
