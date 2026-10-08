# Kiểm chứng đề tài dự đoán cơ chất deacetyl hóa SIRT1–7

Ngày khảo sát: **08/10/2026**. Phạm vi: phản biện [khuyến nghị ban đầu](topic-final-recommendation.md), đọc nguồn gốc và kiểm tra bảng dữ liệu; **chưa huấn luyện mô hình hoặc triển khai hệ thống**.

**Khuyến nghị: tiếp tục nhưng thu hẹp.** Có cơ sở để nghiên cứu khả năng khái quát hóa của mô hình học hoạt tính trên peptide sang các vị trí acetyl hóa phụ thuộc sirtuin trong tế bào. Chưa đủ cơ sở để chốt đề tài “dự đoán cơ chất sinh lý SIRT1–7 với bảo đảm 90%”. Giữ bảy đầu ra cho khảo sát nội miền; ưu tiên **SIRT2 và SIRT3** cho đánh giá ngoài miền, với hai endpoint riêng. Tính mới phải nằm ở giao thức chống rò rỉ, mô hình hóa bằng chứng và đánh giá chuyển endpoint; không nằm ở việc lần đầu dự đoán cơ chất sirtuin hay lần đầu kiểm chứng bằng acetylome.

Mức chắc chắn: **cao** với các lỗi nhãn, metric và tiền lệ trực tiếp đã kiểm tra; **vừa** với phạm vi phương pháp có thể đóng góp; **chưa đạt cổng dữ liệu** cho benchmark tế bào có dương–âm đáng tin ở hai isoform. Đủ mang tới GVHD để thảo luận có điều kiện, chưa đủ trình bày như đề tài đã xác nhận tính mới và khả thi.

Nhãn bằng chứng trong tài liệu:

- **[TG]**: tác giả nguồn gốc báo cáo; không phải kết quả của đề tài này.
- **[KT]**: tự tải và kiểm tra bảng/mã trong phiên này; có [script và kết quả audit](../research_notes/sirtuin-substrate/README.md).
- **[SL]**: suy luận hoặc thiết kế đề xuất, cần thí nghiệm kiểm chứng.
- **[CK]**: chưa xác minh, không dùng để kết luận chắc chắn.

## 1. Bối cảnh và câu hỏi cần bảo vệ

Đã đọc `CLAUDE.md`, [danh sách đề tài](../../../topics/README.md), [nhật ký](../../work-log.md), [biên bản lần 1](../../../meeting/session-01-minutes.md), [hồ sơ GVHD](../../advisor/README.md), bản phác phương pháp B và khảo sát hướng tin học. Các tài liệu trước còn ưu tiên cancer/aging hoặc kinase; theo yêu cầu phiên này, khuyến nghị SIRT1–7 là phạm vi khảo sát. Không dùng các giới hạn GPU/thời gian cũ làm lý do loại phương pháp.

Biên bản ghi **tiêu chí 5 là ứng dụng/website bắt buộc**. Conformal là một hướng phương pháp, không thay cho tiêu chí 5. GVHD là **Ho Quang Thai**; không mặc định các công trình của nhóm **Yu-Yen Ou** là của GVHD. SirtSAGE có tên Ho trong danh mục địa phương, nhưng toàn văn chưa lấy được để kiểm tra chi tiết kiến trúc.

Vấn đề có giá trị: “mẫu chuỗi thuận lợi cho enzyme trên peptide có giúp tìm vị trí acetyl hóa đáp ứng can thiệp enzyme trong tế bào, khi protein/họ protein chưa được thấy?” Giá trị này gắn với sinh học sirtuin nhưng chưa chứng minh tác dụng chống lão hóa, nguy cơ ung thư hoặc điều trị.

## 2. Nền sinh học: ba loại bằng chứng không đồng nhất

**Acetyl hóa** là gắn nhóm acetyl lên lysine (K), một amino acid trong protein. **Deacetyl hóa** là loại nhóm này; sirtuin sử dụng NAD+ trong phản ứng. **Isoform SIRT1–7** ở đây chỉ bảy thành viên họ enzyme, cần phân biệt với các biến thể trình tự của một protein cơ chất.

| Endpoint | Đo được | Không tự suy ra được |
|---|---|---|
| Peptide in vitro | Enzyme tái tổ hợp làm giảm acetyl trên đoạn chuỗi trong điều kiện thử | Protein nguyên có bị tác động trong tế bào không |
| Protein nguyên, enzyme tinh sạch | Bằng chứng phản ứng trực tiếp trên protein trong phép thử đó | Tầm quan trọng sinh lý trong mô/tế bào cụ thể |
| Acetylome KO/KD/OE | Mức peptide acetyl thay đổi sau mất gen, giảm biểu hiện hoặc tăng biểu hiện enzyme | Mọi vị trí thay đổi đều là cơ chất trực tiếp |

Một site MS tăng sau KO có thể phản ánh mất deacetyl hóa trực tiếp, thay đổi enzyme khác, chuyển hóa, hoặc lượng protein. **Hiệu chỉnh lượng protein** giúp tách nhiều protein hơn khỏi tỷ lệ acetyl cao hơn, nhưng chưa chứng minh quan hệ nhân quả trực tiếp. Ngược lại, site không tăng có thể do ít công suất thống kê, enzyme bù trừ hoặc site vốn hầu như không acetyl hóa. [SL]

**Stoichiometry** là tỷ lệ phân tử protein được acetyl hóa tại một vị trí. [Weinert 2015](https://doi.org/10.15252/embj.201591271), Results/Fig. 3 và Appendix S2–S3, dùng định lượng hóa học và dữ liệu SIRT3 đã công bố để lập luận rằng nhiều acetyl hóa ty thể có occupancy thấp, phù hợp với vai trò sửa tổn thương acetyl hóa không enzyme của SIRT3. Đây là diễn giải ở phạm vi dữ liệu ty thể, không kết luận mọi acetyl hóa vô nghĩa hoặc mọi sirtuin có cùng vai trò. Cần phân biệt cột stoichiometry được ước lượng trực tiếp với cột **predicted stoichiometry** tính từ fold-change nhập từ Hebert. [TG]

### Khác biệt giữa bảy thành viên

| Nhóm | Điều cần tính đến khi thiết kế |
|---|---|
| SIRT1/2/3 | Có cơ sở mạnh cho deacetyl hóa; vẫn cần khu trú, biểu hiện và bối cảnh tế bào |
| SIRT4 | Có hoạt tính loại các nhóm acyl khác: không dùng một assay acetyl-peptide để đại diện toàn bộ chức năng. [Anderson 2017](https://doi.org/10.1016/j.cmet.2017.03.003) |
| SIRT5 | Ưu tiên demalonyl/desuccinyl trong nghiên cứu động học; số nhãn acetyl dương cao ở Rauh không có nghĩa enzyme deacetyl hóa ưu thế trong tế bào. [Du 2011](https://doi.org/10.1126/science.1207861), Fig. 1/Table S2 |
| SIRT6 | Hoạt tính trên nucleosome phụ thuộc ngữ cảnh khác peptide tự do. [Nghiên cứu nucleosome](https://pmc.ncbi.nlm.nih.gov/articles/PMC3794599/) |
| SIRT7 | Các nghiên cứu hoạt hóa bởi acid nucleic cho thấy điều kiện assay có thể quan trọng. [Nghiên cứu RNA](https://pmc.ncbi.nlm.nih.gov/articles/PMC5326686/), [cấu trúc 2025](https://doi.org/10.1038/s41467-025-56529-y) |

Hai dòng SIRT6/7 là đối chiếu nguồn liên quan, chưa audit dữ liệu thực nghiệm của các bài đó trong phiên này. Không loại nhãn Rauh cho SIRT4–7; chỉ giữ tên endpoint chính xác: **đáp ứng deacetyl hóa peptide trong điều kiện assay**.

## 3. Rauh 2013: assay và nhãn thực sự là gì?

Đã đọc toàn văn [Rauh 2013](https://doi.org/10.1038/ncomms3327), Methods và Supplementary Methods, cùng SD1/2/5/6/7. Mảng có peptide acetyl và đối chứng không acetyl, spot lặp; dùng antibody để đọc mất tín hiệu sau xử lý enzyme. Có đối chứng không NAD+, buffer và mutant thích hợp. Lượng enzyme **6–218 µg/ml**, thời gian xử lý 2 giờ; lượng và construct khác theo isoform. [TG]

| Cột SD1 | Ý nghĩa | Cách dùng hợp lý |
|---|---|---|
| `signal ratio (exp:ref)` | Tín hiệu xử lý/chứng; thấp hơn thường tương ứng mất acetyl mạnh hơn | Không đặt “ratio ≥ 1 là dương”; không gọi là tốc độ phản ứng |
| `ratio error` | Biến thiên giữa spot triplicate và lần lặp, theo mô tả bài | Chỉ là proxy độ tin cậy; chưa phải phương sai của nhãn efficiency |
| `substrate category` | Tổng hợp kết quả mất tín hiệu có ý nghĩa, Welch P < .01, thành thang 0–1 qua nhiều thí nghiệm | Có thể khảo sát thang thứ tự; không xem là xác suất đã calibration |
| `efficiency` | `category / ratio`, dùng xếp hạng/clustering trong bài | Nhãn liên tục dẫn xuất; không đồng nhất với `kcat/Km` |

Tác giả tránh diễn giải chi tiết ratio vì thay đổi nhỏ khó đo. Do đó, “bảng có số thực” chưa đủ chứng minh hồi quy sẽ tốt hơn phân loại. Category có các mức rời rạc và độ phân giải khác theo isoform; efficiency chịu ảnh hưởng cả category lẫn mẫu số. Đề xuất kiểm tra thang thứ tự, biến đổi ổn định và xếp hạng **trong từng isoform**, không hồi quy một thang hoạt tính chung cho cả bảy. Trọng số `1/error²` cần kiểm tra và chặn cực trị; error của ratio không tự truyền thành error của category/ratio. [SL]

### Audit số liệu và chênh lệch 6.802/6.801

[KT], từ SD1 và Ridgeway SD15, đối chiếu theo chuỗi sau chuẩn hóa **Z → X**, không ghép theo số dòng:

- SD1: **6.802 chuỗi khác nhau**, đều dài 13, K ở giữa; không thiếu ô trong 28 cột đo; **249** có ký tự Z; **473** dòng thiếu accession; **5.251** dòng liệt kê nhiều accession.
- SD15: **6.801 chuỗi khác nhau**, không thiếu ô trong chín cột sử dụng; **249** còn X. Bài Ridgeway nói thay residue masked bằng alanine, nhưng bảng phân phối vẫn có X; chưa xác minh đầy đủ chuỗi ở bước sinh đặc trưng.
- Chính xác một chuỗi SD1 không có trong SD15: **GIQCVKKRDLEQA**. SD2 gắn chuỗi với **Q04206/RELA/p65 K123** và nhiều accession/position khác. **Đã xác định dòng mất; chưa xác định lý do loại.**
- SD15 có **2.999 chuỗi accession khác nhau**, trong đó có placeholder **SYNTHETIC** trên **231 dòng**. Vì vậy không được gọi là 2.999 protein đã ánh xạ chắc chắn; 2.998 là số accession khác placeholder, cũng chưa phải số protein sinh học đã chuẩn hóa.
- **Toàn bộ 47.607 nhãn** SD15 khớp `efficiency ≥ 1` của SD1. `category ≥ 1` sai ở 172/1.079/673/27/0/462/10 dòng cho SIRT1→7; ngưỡng ratio ≥ 1 cũng không khớp. Đây là bất nhất giữa mô tả Methods và dữ liệu, không suy đoán động cơ hoặc sửa nhãn tác giả.

| Isoform | SIRT1 | SIRT2 | SIRT3 | SIRT4 | SIRT5 | SIRT6 | SIRT7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dương SD15 (`efficiency ≥ 1`) | 176 | 1.901 | 1.844 | 1.038 | 2.614 | 1.199 | 1.692 |
| Chỉ dương với isoform đó | 21 | 319 | 289 | 162 | 1.088 | 269 | 282 |
| Trung vị ratio error SD1 | .37 | .22 | .24 | .24 | .21 | .27 | .22 |

Phân bố số nhãn dương/site từ 0→6: **1.107, 2.430, 2.087, 902, 226, 44, 5**; không có site dương cả bảy. Đây là tương quan trong assay, chưa chứng minh mô hình chia sẻ sẽ tốt hơn mô hình độc lập. SIRT1 mất cân bằng nặng, nhưng **176 không tự động là lý do bỏ**: cần đếm protein/họ chứa các dương sau split, kiểm tra độ bất định và learning curve. [SL]

## 4. Kiểm kê dữ liệu tế bào và trạng thái cổng dữ liệu

| Nguồn / accession | Loài, bối cảnh, can thiệp | Lặp và định lượng | File đã đọc / tình trạng |
|---|---|---|---|
| [Zhang 2022](https://doi.org/10.1038/s41598-022-06793-5); [Synapse syn26134616](https://doi.org/10.7303/syn26134616) | Người, HCT116; SIRT2 KD/OE và chứng | S1 có bốn cột mẫu 1/3/5/7; đã chuẩn hóa lượng protein; không có p/q khác biệt từng site | S1 **2.846 dòng dữ liệu**; S2 **134 peptide hit, tổng 152 acK**; đã tải XLSX |
| Ridgeway SD14, cùng nguồn Zhang | Người, HCT116; tập chọn KD↑ và OE↓ | Dữ liệu dương chọn lọc, không có lớp âm | **149 site key / 123 accession / 134 tryptic peptide**; không phải nghiên cứu MS độc lập mới |
| [Weinert 2015 EV1](https://doi.org/10.15252/embj.201591271); PXD000885 cho dữ liệu nghiên cứu Weinert | Gan chuột; bảng nhập SIRT3 KO/WT từ [Hebert 2013](https://doi.org/10.1016/j.molcel.2012.10.024) | Có ratio KO/WT, CR KO/WT, CR WT/WT; bảng nhập không có site p/q hoặc cột lặp KO | **17.871 dòng EV1**, trong đó **2.106** có ratio SIRT3 KO/WT; đã tải/đọc ZIP và XLSX |
| [Rardin 2013](https://doi.org/10.1073/pnas.1302961110) | Gan chuột, ty thể, WT/SIRT3 KO, nhịn ăn 24 giờ | **5 động vật/nhóm**, có process/injection replicates; chuẩn peptide; bảng protein riêng | [TG] 2.187 site, 283 tăng ≥2 lần, P≤.01; **bảng S3–S5 chưa đọc được**: PMC trả HTML challenge, PNAS 403 |
| [PXD021357](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD021357) | Chuột, ống thận, sham vs UUO ngày 1 | Metadata ghi hiệu chỉnh protein, FC 2, t-test P<.05; số lặp chưa xác minh qua bảng định lượng | Metadata tải được; **acetylome không phải KO SIRT3**. Không dùng làm nhãn cơ chất SIRT3 |
| [PXD023479](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD023479) | HEK293T; SIRT3-FLAG vs Luc-FLAG | Co-IP/interactome theo protocol | Metadata tải được; **không phải acetylome KO**; tương tác không đồng nghĩa deacetyl hóa |
| [PXD012796](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD012796) | Chuột, T CD3+ từ lách; WT/Sirt2 KO, naive/kích hoạt 3 ngày | Enrichment acK, định lượng tương đối; số lặp/site table chưa kiểm | Ứng viên phù hợp về can thiệp; chưa nhận bảng định lượng |
| [PXD019763](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD019763) | Cùng nhánh công bố chuyển hóa tế bào T/Sirt2 | Cần xác định vai trò từng file và liên hệ các accession | Không đếm cùng nghiên cứu thành hai validation độc lập; chưa đủ xác nhận endpoint site |

Nguồn số đếm [KT]: [audit-results.json](../research_notes/sirtuin-substrate/audit-results.json). Nguồn metadata: [manifest](../research_notes/sirtuin-substrate/download-manifest.json). API liệt kê file PRIDE thử trong phiên trả body rỗng dù HTTP 200; đây là lỗi/giới hạn truy xuất, **không phải bằng chứng kho không có file**.

### Những giới hạn cụ thể đã kiểm tra

**SIRT2:** S1 có intensity thô, hệ số protein và intensity đã chuẩn hóa; cần tính ratio theo đúng cặp 3/1 và 7/5. Không suy FDR định danh 1% thành FDR khác biệt acetyl hóa. [Ghi chú của người cung cấp dữ liệu trên Synapse](https://www.synapse.org/Synapse:syn26134616/discussion/threadId=9116) giải thích mẫu chẵn có xử lý bổ sung, dùng hỗ trợ nhận diện trong MaxQuant và không đưa vào phân tích downstream; không được tính chúng thành lặp sinh học của mẫu lẻ. Chưa có bảng replicate đủ để ước lượng công suất hoặc khoảng tin cậy từng site. OE có đồng biểu hiện acetyltransferases theo ghi chú nguồn; endpoint rộng hơn “chỉ thay SIRT2”. [TG/CK]

Ridgeway mô tả WT/H187Y trong đoạn validation, nhưng Zhang dùng H187Y ở kiểm chứng BCL9 trong tế bào 293; global acetylome HCT116 là KD/OE. Không gộp hai thí nghiệm. Chênh **152 → 149** vẫn cần truy vết ánh xạ; không tuyên bố ba vị trí mất do lý do đã biết.

**SIRT3:** EV1 là đường tải thực tế cho dữ liệu định lượng isoform thứ hai. **483/2.106 ratio ≥2** chỉ là đếm theo ngưỡng, **không phải 483 cơ chất dương đã xác nhận**. Không có p/q và lặp KO trong bảng nhập; phải lấy Hebert gốc hoặc Rardin để lập luận uncertainty, total-protein correction và mapping isoform. Không xem Weinert và Hebert là hai thí nghiệm KO độc lập. Hebert gốc báo 3.285 site được định lượng, 2.193 ty thể; tập giao EV1 nhỏ hơn tập nguồn. [KT/TG]

**Kết luận cổng:** đã có assay train và bảng định lượng cho **SIRT2 + SIRT3**; chưa có benchmark tế bào dương–âm đủ bằng chứng ở hai isoform. Cổng “file tải được” đạt một phần; cổng “nhãn trả lời được câu hỏi cơ chất” còn mở.

### Quy tắc dương, âm, chưa xác định

| Loại | Quy tắc đề xuất | Hạn chế phải giữ |
|---|---|---|
| Dương phụ thuộc isoform | Hướng thay đổi phù hợp, effect-size đủ ý nghĩa sinh học đặt trước, kiểm định/uncertainty hợp lệ, chỉnh protein nếu có | Vẫn có thể gián tiếp; chỉ thí nghiệm trực tiếp mới nâng cấp nhãn cơ chất trực tiếp |
| Âm theo bối cảnh | Định lượng tốt, assay có lực, khoảng tin cậy nằm trong biên tương đương quanh 0 được biện minh trước | Chỉ “không đáp ứng đáng kể trong bối cảnh này”, không phải enzyme không bao giờ tác động |
| Unknown | Không đo được, missing/imputed, localization/mapping mơ hồ, CI rộng hoặc chỉ P>.05 | Không cho vào loss như âm; giữ mask và báo độ phủ |

Biên tương đương cần dựa độ biến thiên assay và thay đổi tối thiểu có ý nghĩa sinh học, bàn với chuyên gia; không tự chọn 1.5/2 lần cho mọi bộ. Nếu chưa có âm đáng tin, dùng bài toán positive–unlabeled/ranking có giả định rõ, hoặc hồi quy đáp ứng định lượng; không hợp thức hóa MCC bằng gán unknown thành 0. [SL]

## 5. 43,0%, rò rỉ và bất nhất giữa các bảng

**64/149 = 42,953%** là tỷ lệ phát hiện lại trên tập positive-only tại ngưỡng .5. Có thể gọi recall trên tập dương tham chiếu chọn lọc, không phải recall tổng thể mọi cơ chất. **Precision = TP/(TP+FP)** cần FP trong một tập đo thích hợp; 149 dương không cung cấp FP. Không xác định được specificity/MCC/AUROC; AUPRC trên toàn dương không có ý nghĩa phân biệt. Mô hình đoán tất cả dương đạt 100% recall ở đây, nên “vượt 43%” đơn độc không chứng minh tốt hơn. [KT/SL]

Audit SD14 và CSV đặc trưng Ridgeway: **46/149** site key `(accession, position)` có trong train; **108/149** nằm trên accession đã có trong train. Chỉ **41** dòng còn lại ở accession chưa thấy theo cách ánh xạ này; chúng vẫn có thể đồng dạng. Đây là trùng với **pool huấn luyện công bố**, chưa xác định từng dòng thuộc fold nào khi mô hình được fit. Counts là dựa annotation, chưa kiểm lại toàn bộ residue bằng FASTA có phiên bản. Deep-PLA S1 cũng có **73** key trong pool train và **1** key trong SD14; chưa tính đầy đủ biến thể accession/homology. [KT]

Kiểm tra bổ sung trên trình tự UniProt tải ngày 08/10/2026: **149/149** vị trí SD14 có residue K và peptide tryptic khớp tại site; lấy riêng isoform P06753-2. [Kết quả mapping và hash snapshot](../research_notes/sirtuin-substrate/mapping-audit-results.json). Đây là kiểm tra trình tự hiện hành cho test, chưa kiểm toàn bộ train hoặc phục hồi RefSeq v54 của nghiên cứu gốc. [KT]

So chuỗi ngắn SD13 với 6.552 window train không có X: **60/149** window trùng đủ 13 residue; **63/149** có ít nhất 10/13 residue khớp ở cùng vị trí. Đây là so không gap trên peptide, **không phải clustering đồng dạng toàn protein**; 60 chuỗi trùng lớn hơn 46 key trùng cho thấy accession–position chưa bắt hết trùng trình tự. [KT]

SD13 có **145.461 key khác nhau**, là tập dự đoán cho proteome được chọn theo quy trình tác giả, không phải nhãn thực nghiệm cho tất cả lysine người. Cả 149 key SD14 có trong SD13 nhưng **0/149 điểm SIRT2 khớp ở sai số 1e-8**; **21 nhãn nhị phân khác**, SD13 cho **61** dương còn SD14 cho **64**. Ví dụ ANXA1 P04083 K312: SD13 **.709550397**, SD14 **.801009919762105**. Nguyên nhân/phiên bản model chưa xác định. Vì thế phải báo hai snapshot riêng; không lấy SD13 để tái tạo 64/149 rồi khẳng định thành công. [KT]

Ridgeway Supplementary Materials S1 dùng holdout peptide stratified 10%, rồi chia 90% còn lại cho base/meta training, CV stratified lặp. Không có bằng chứng protein/homology grouping trong protocol đã đọc. Mã `model_fitting.py` ở commit **e7cb6d7eb8837c770bd1638dcd45c59688535cfa** có `train_test_split` không `groups`, một số split không đặt `random_state`. Đây là kiểm tra mã snapshot, không chứng minh chính snapshot đó sinh toàn bộ bảng bài báo. Cần kiểm soát cả feature selection, scaler, negative sampling và hyperparameter search trong fold. [TG/KT]

## 6. Tiền lệ và tính mới

Chiến lược, truy vấn và giới hạn: [search-log.md](../research_notes/sirtuin-substrate/search-log.md). Khảo sát đến ngày 08/10/2026, ưu tiên paper/Methods/supplement/code và dữ liệu chính thức.

| Công trình | Đích và phương pháp | Hệ quả cho đề tài |
|---|---|---|
| [Smith 2011](https://doi.org/10.1021/cb100218d), *SIRT3 Substrate Specificity Determined by Peptide Arrays and Machine Learning* | Array peptide, hồi quy chuỗi cho SIRT3; có kiểm chứng động học. Đọc PDF tác giả | ML dự đoán cơ chất sirtuin có từ trước Rauh; endpoint binding trên analog khác endpoint Rauh |
| [Zhai 2017](https://doi.org/10.1038/s41598-017-04847-7) | Site SIRT1; SVM + chuỗi + GO/PPI/Pfam; chia theo protein khi dùng chức năng; kiểm chứng thực nghiệm | Ngữ cảnh sinh học và protein split không mới tự thân; âm nền vẫn là lysine chưa được biết |
| [Deep-PLA 2020](https://doi.org/10.1093/bib/bbz107), online 2019 | HAT/HDAC-specific DNN; **SIRT1/2/3/6/7**; AAC/CKSAAP/PSSM/BE, PSO; human train/nonhuman test | Đối thủ cơ chất trực tiếp; không được nói “HDAC không phải sirtuin” |
| [Ridgeway 2025](https://doi.org/10.1038/s42004-025-01717-6) | 7 model isoform riêng, 443 feature, LDA/tree + MusiteDeep và meta-ensemble; 149 site tế bào | Đã đánh giá chuyển assay→cellular; ensemble có thành phần DL. PLM và regression được tác giả nêu hướng tương lai |
| [NAD_MCNN 2025](https://doi.org/10.1111/cbdd.70085) | Vị trí gắn NAD+ trên enzyme, PLM + multiwindow CNN theo abstract | Bài toán khác; không so AUC trực tiếp. Chưa đọc toàn văn/không audit data; không gắn với Ho |
| [SirtSAGE](https://doi.org/10.1142/S2737416527400011) | Phân loại/lập bản đồ tiến hóa protein sirtuin theo tiêu đề và danh mục địa phương | Cùng họ enzyme, khác cơ chất residue. Publisher không truy cập được: kiến trúc/benchmark **chưa kiểm bằng toàn văn** |
| [AIPred 2025](https://doi.org/10.1186/s12915-025-02418-1) | Acetyl hóa nonhistone, PLM + ML giải thích | PLM cho acetyl-site đã có; acetylation propensity khác enzyme-specific deacetylation |
| [DeepPTMPred 2026](https://doi.org/10.1093/bib/bbag321) | PTM-site đa phương thức, có PLM/cấu trúc | Thêm PLM hoặc cấu trúc vào PTM không tự đủ mới; mới kiểm toàn văn web ở mức kiến trúc tổng quát |
| [CLASPP 2026](https://doi.org/10.1371/journal.pcbi.1014616) | PLM, contrastive learning, cân bằng nhiều PTM; unified predictor | Chia sẻ biểu diễn/mất cân bằng/motif đã có tiền lệ; multi-PTM không đồng nhất bảy enzyme cùng endpoint |

[KT] S1 Deep-PLA có annotation SIRT người: **185/52/30/10/12** lần lượt cho SIRT1/2/3/6/7; chuột **30/6/16/2/4**. Đây là số dòng annotation theo enzyme, không cộng thành số site duy nhất vì site có thể nhiều enzyme. Đọc Methods cho thấy âm lấy từ lysine chưa được ghi modified; human/nonhuman split không tự loại protein đồng dạng. Cần audit mapping và nguồn từng PMID trước khi coi các nhãn này là test độc lập.

Chưa tìm thấy trong phạm vi truy vấn một nghiên cứu **PLM bảy đầu ra trên Rauh, đánh giá cellular có kiểm soát họ protein và uncertainty endpoint**. Đây là khoảng trống **ứng viên**, không kết luận chưa từng có. Các bài tên DeepSIRT/ASEB cũng cần kiểm thêm trước literature review cuối; không coi tên có “SIRT” là cùng đích.

Ba tầng đóng góp:

1. **Đã có bằng chứng trong phiên:** audit nhãn, endpoint, metric và provenance; phát hiện bất nhất SD13/14. Hữu ích cho đề xuất và tái lập, chưa mặc định đủ thành đóng góp phương pháp luận văn.
2. **Dự kiến:** học nhiều isoform với mask/độ tin cậy phù hợp từng assay; tách tín hiệu chuỗi và khả năng tiếp cận trong tế bào; benchmark không rò rỉ có danh mục dương/âm/unknown.
3. **Cần thí nghiệm:** PLM, sharing, ordinal target hoặc context cải thiện dự đoán; conformal có coverage hữu ích; XAI phản ánh motif/động học. Chưa có kết quả để hứa.

## 7. Giao thức đánh giá đề xuất

### Ánh xạ và chia dữ liệu

1. Giữ chuỗi gốc, Z/X và toàn bộ mapping từ Rauh SD2. Pin FASTA/UniProt release và checksum; kiểm K đúng position, cửa sổ khớp, isoform/canonical, accession lỗi thời và loài. Một peptide có nhiều protein không được nhân thành nhiều mẫu độc lập.
2. Xây nhóm liên thông gồm các protein có chung peptide/mapping và protein đồng dạng; giữ cả nhóm trong một split. Dùng MMseqs2/CD-HIT hoặc alignment có **identity + coverage**, lưu phiên bản/tham số; khảo sát độ nhạy theo mức họ, không chọn ngưỡng dựa performance test.
3. Audit thêm chuỗi cửa sổ giống nhau giữa nhóm; mọi peptide masked/mapping mơ hồ để pool riêng. Không gộp tất cả `SYNTHETIC` thành một protein thật và cũng không tự xem chúng độc lập.
4. Chia **train / validation / calibration / test** theo nhóm. Validation chọn kiến trúc/ngưỡng; calibration chỉ chọn quantile uncertainty sau khi đóng model; test giữ kín. Nếu split khiến isoform không có đủ positive clusters, báo metric không ước lượng được và dùng nested/group CV thích hợp; không ép tỷ lệ 80/10/10.
5. Cellular test giữ riêng theo nghiên cứu, protein và homology với toàn bộ training/calibration; báo các tầng **site đã thấy / site mới cùng protein / protein mới / họ mới**. SIRT3 chuột là chuyển loài **cộng** chuyển assay, không quy mọi suy giảm cho domain shift in vitro→cell.

Audit trong phiên đã đo annotation overlap và kiểm chuỗi ngắn; **chưa chạy clustering toàn protein, chưa khóa FASTA toàn bộ train và chưa tạo split chính thức**. Bảo đảm protein không trùng chỉ loại một nguồn rò rỉ, không bảo đảm các site trong cùng protein là mẫu iid.

### Metric theo endpoint

| Dữ liệu | Metric chính | Bổ sung/đối chứng |
|---|---|---|
| Nhị phân assay có hai lớp | AUPRC theo isoform; MCC/F1 ở ngưỡng chọn trên validation | AUROC, calibration/Brier, prevalence; macro và từng isoform, CI bootstrap theo nhóm |
| Liên tục/thứ tự assay | Spearman/Kendall theo isoform; ordinal loss/error; MAE nếu thang có nghĩa | Constant/median predictor, rank enrichment; không so trực tiếp trị số giữa isoform |
| Bảy nhãn đầy đủ | Macro-AUPRC, Hamming loss; micro và per-label | Exact match/Jaccard, cardinality; label masks với cellular thiếu nhãn |
| 149 site dương | Recall tại ngưỡng đã khóa; positive enrichment/recall@budget nếu có universe nền hợp lệ | Always-positive, số dự đoán trên nền, CI theo protein; không precision/MCC |
| Cellular quantitative | Tương quan/ranking đáp ứng; effect-size sau protein correction | Giữ unknown, localization và missingness; đánh giá phân loại chỉ trên nhãn được biện minh |

Không tune ngưỡng bằng 149 dương rồi báo recall trên cùng 149. Khi so cùng site, dùng CI của **chênh lệch ghép cặp theo protein**; không coi 149 site là 149 thử nghiệm sinh học độc lập. Với nhãn tế bào chỉ có một isoform, không báo exact-match vector bảy nhãn.

### Baseline và ablation tối thiểu

| So sánh | Giữ cố định | Hiệu ứng được tách |
|---|---|---|
| Constant/prior; motif/PSSM; 443 feature + LDA/tree | Split, nhãn và tuning budget | Độ khó thật và lợi ích ML |
| Ridgeway chạy lại base + MusiteDeep/meta khi tái lập được | Protocol chung; tách model có/không secondary score | So baseline đầy đủ, tránh đối thủ yếu hơn bản công bố |
| One-hot + CNN; frozen PLM + linear/MLP; frozen PLM + mCNN | Head size/selection hợp lý | Biểu diễn PLM và tác dụng mCNN |
| 7 head độc lập vs shared backbone | Cùng encoder/loss/target | Chia sẻ isoform; negative transfer |
| Binary efficiency threshold vs ordinal category vs derived efficiency | Cùng split/encoder | Ý nghĩa nhãn; cần endpoint đánh giá chung để so |
| Có/không error weighting; có/không mask uncertainty | Cùng nhãn và model | Lợi ích độ tin cậy; sensitivity với weight cap |
| Peptide-only vs context-only vs sequence+context | Context chỉ lấy từ nguồn độc lập đã pin | Tác dụng localization/structure/PPI; kiểm leakage annotation |
| Frozen vs LoRA | Kiến trúc và split | Lợi ích fine-tuning; chỉ làm sau baseline đơn giản |

Deep-PLA có thể chạy lại trên dữ liệu riêng đã khóa hoặc dùng như external published predictor với audit overlap. **Dự đoán công bố SD13/14 chỉ là mốc lịch sử**, vì training pool/split/snapshot khác. Không tuyên bố “vượt Ridgeway” từ một model mới dùng thêm context trong khi đối thủ được fit theo protocol khác. Không cần chạy toàn bộ tổ hợp: ưu tiên ablation trả lời RQ, báo chi phí và seed.

## 8. Conformal: bảo đảm điều gì và trong miền nào?

[Angelopoulos–Bates](https://arxiv.org/abs/2107.07511) trình bày split conformal: model cố định, calibration và test exchangeable, quantile hữu hạn mẫu. “Không giả định phân phối” **không có nghĩa không cần giả định exchangeability**. Protein được chọn theo assay và site MS được chọn theo đáp ứng có thể phá điều kiện này.

Đầu ra dễ diễn giải cho mỗi isoform là **C_j(x) ⊆ {0,1}**: `{1}` dương, `{0}` âm trong endpoint được calibrate, `{0,1}` chưa phân biệt được. Tập rỗng cần xử lý/chẩn đoán, không tự chứng minh OOD. [SL]

| Bảo đảm muốn có | Điều cần thiết |
|---|---|
| 90% marginal cho từng isoform | Calibration hợp lệ cho isoform j; có thể chủ yếu che phủ lớp âm nếu mất cân bằng |
| Coverage riêng cho positive/negative | Mondrian theo **lớp thực** và isoform; mỗi lớp phải đủ mẫu; grouping isoform đơn độc chưa đủ |
| 90% cho toàn vector bảy nhãn | Score joint hoặc điều chỉnh sai số đồng thời, ví dụ α/7; bảy mức 90% riêng không cho joint 90% |
| Tập isoform chứa cơ chất thực | Phải định nghĩa chứa tất cả isoform dương hay ít nhất một; kiểm cả missing-label và false inclusion |
| 90% trong tế bào | Calibration đích hợp lệ hoặc định lý phù hợp; không chuyển bảo đảm của nhãn assay sang nhãn cellular |

Các site trong protein phụ thuộc nhau: định nghĩa đơn vị coverage là protein rồi site, hay cả cluster, và dùng thiết kế hierarchical/group conformal phù hợp. Xem [Dunn–Wasserman–Ramdas, two-layer models](https://robinmdunn.github.io/publication/conformal/). Chia protein riêng giúp chống leakage nhưng không tự cho theorem iid-site. Dùng [Barber và cộng sự, beyond exchangeability](https://doi.org/10.1214/23-AOS2276) để đánh giá giới hạn, không viện dẫn như bảo đảm miễn điều kiện.

[Weighted conformal dưới covariate shift](https://arxiv.org/abs/1904.06019) cần cùng quan hệ Y|X và tỷ lệ mật độ thích hợp. Ở đây **Y assay và Y cellular khác định nghĩa**, nên weighting đầu vào chưa sửa được concept/endpoint shift. Nếu có cellular calibration, phải giữ cellular test khác nhóm/nghiên cứu; 149 dương chỉ hỗ trợ coverage cho lớp dương chọn lọc, không negative coverage hoặc vector bảy nhãn.

Ít positive clusters khiến quantile thô và set lớn; số mẫu cần hoạch định từ độ chính xác CI mong muốn và effective sample size, không từ một ngưỡng tùy ý. Báo coverage theo isoform/lớp, set size, tỷ lệ `{0,1}`, utility và CI; không dùng set luôn `{0,1}` để tuyên bố thành công. **RQ conformal nên là phần mở rộng có điều kiện**, không lời hứa trong tên đề tài cốt lõi.

## 9. XAI: kiểm độ trung thực trước khi diễn giải cơ chế

Đề xuất occlusion/attribution trên window, so với motif và vị trí quan trọng thực nghiệm; cần giữ central K và thử nhiều cách perturbation tránh chuỗi ngoài phân phối. Đối chứng gồm model trọng số ngẫu nhiên, hoán nhãn rồi fit, motif thành phần amino acid nền, thay residue matched và motif xáo vị trí. [Adebayo 2018](https://papers.nips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html) cung cấp cơ sở cho sanity checks bằng randomization.

Motif Rauh lấy top 50 efficiency của **chính array**, nên agreement có thể là học lại dữ liệu, không validation sinh học độc lập. Ưu tiên kinetics/mutagenesis hoặc thí nghiệm protein khác nguồn; kiểm fidelity qua thay đổi score khi perturbation, độ ổn định theo seed và fold. Không khớp motif có thể do model sai, nhãn nhiễu, context khác hoặc phương pháp XAI; không tự kết luận “XAI sai”. Saliency không chứng minh cơ chế hay quan hệ nhân quả. [SL]

## 10. Khẳng định ban đầu cần sửa

| Khẳng định trong báo cáo cũ | Bằng chứng | Kết luận sửa |
|---|---|---|
| Category ≥1 cho 176 SIRT1 dương | SD1↔SD15 khớp efficiency≥1; category≥1 chỉ tương ứng 4 trong tập aligned | Dùng tên nhãn đúng; giữ bất nhất Methods để truy vết |
| 64/149 là precision | 149 đều KD↑/OE↓, không FP | Recall trên dương chọn lọc |
| SD13 đủ thay chạy lại baseline | SD13/14 khác điểm và 21 binary calls; split mới khác | Mốc lịch sử; baseline công bằng cần chạy cùng protocol |
| Deep-PLA không có sirtuin | Methods + S1 có SIRT1/2/3/6/7 | Đối thủ trực tiếp |
| Chưa ai làm ML cơ chất sirtuin / cellular validation | Smith 2011, Zhai 2017, Deep-PLA, Ridgeway | Bỏ tính mới “lần đầu”; tìm khác biệt hẹp |
| Ridgeway không neural | MusiteDeep làm predictor phụ | Base model cổ điển, hybrid có DL |
| Không đổi có ý nghĩa là âm sạch | Thiếu lực/compensation/missingness; chưa có equivalence test | Unknown mặc định; âm theo bối cảnh cần chứng cứ |
| PXD021357/PXD023479 là KO acetylome SIRT3 | Sham/UUO và FLAG co-IP trong metadata | Loại khỏi benchmark cơ chất KO |
| 2.999 protein đã ánh xạ | 231 dòng SYNTHETIC; SD1 nhiều accession | Số accession strings; cần mapping phiên bản |
| Nhãn liên tục sẽ giải quyết SIRT1 | Category/ratio là derived assay score, chưa kinetics | Giả thuyết phải thử; không tự bỏ hoặc cứu isoform |
| Bảy output + conformal là tập isoform đúng 90% trong tế bào | Marginal/joint/endpoint khác nhau | Định nghĩa C_j và miền bảo đảm; cellular cần cơ sở riêng |
| Motif không khớp ⇒ XAI sai | Motif cùng array, endpoint/context khác | Kiểm fidelity và đối chứng, không suy nhân quả |
| Conformal đạt tiêu chí 5 | Biên bản: tiêu chí 5 là ứng dụng/website | Thiết kế sản phẩm riêng, bảo đảm ghi đúng phạm vi |

## 11. Phạm vi có thể bảo vệ và cổng đi/dừng

Tên tạm đề xuất: **“Học đặc hiệu deacetyl hóa của sirtuin từ peptide và đánh giá khả năng khái quát hóa sang acetylome phụ thuộc SIRT2/SIRT3.”** Bảy isoform là phạm vi assay; hai isoform là phạm vi cellular. Phần sinh học đóng góp ở đánh giá ranh giới giữa peptide preference và cellular response trên protein mới; chưa hứa phát hiện cơ chất sinh lý mới.

| Câu hỏi | Giả thuyết kiểm chứng | Cách bác bỏ |
|---|---|---|
| **RQ1:** PLM và chia sẻ isoform có cải thiện trên protein/họ chưa thấy? | Biểu diễn chia sẻ giúp một số isoform so baseline cùng split | Paired group CI/ablation không cho lợi ích hoặc cho negative transfer; vẫn là kết quả cần báo |
| **RQ2:** Nhãn thang độ và context giúp khái quát sang cellular response? | Score assay cộng context liên quan hơn peptide-only với đáp ứng protein-normalized SIRT2/3 | Hiệu ứng mất trên protein mới, context-only ngang combined hoặc chỉ có nguồn/mapping bias |
| **RQ3, có điều kiện:** uncertainty có utility dưới các miền đánh giá? | Calibration nội miền cho coverage/set size hữu ích; ngoài miền cần hiệu chỉnh đích | Coverage thất bại hoặc set vô dụng; không diễn giải thất bại là theorem bị bác bỏ khi giả định sai |

Đóng góp tin học nên chọn **một cơ chế có lý do** — ví dụ objective ordinal/masked sharing theo assay và uncertainty — rồi chứng minh bằng ablation. Chỉ thay ESM-2/LoRA/mCNN vào baseline là đóng góp ứng dụng, có thể chưa đủ mức phương pháp GVHD mong muốn. Context không mới tự thân và không nên chứa annotation “known SIRT substrate” của test.

| Cổng | Bằng chứng cần có trước khi đi tiếp | Hiện trạng / xử lý nếu thiếu |
|---|---|---|
| Mapping và độc lập | FASTA pin, site verified, multi-mapping xử lý, protein/homology overlap quantified, split đủ positive groups | Chưa đạt toàn bộ; hoàn tất trước fit, tách pool mơ hồ |
| Cellular endpoint | Site table + design/replicates, uncertainty/protein correction, quy tắc dương/âm/unknown có lý do | SIRT2 và SIRT3 quantitative tải được; full binary benchmark chưa đạt |
| Giá trị khoa học | Ít nhất RQ1 hoặc RQ2 trả lời được bằng endpoint hợp lệ và CI đủ hẹp cho effect cần đánh giá | Nếu chỉ còn positive recall trên nguồn rò rỉ, thu hẹp sang assay/generalization hoặc tạm dừng RQ2 |
| Tính mới phương pháp | So đối thủ trực tiếp, objective rõ, ablation tách hiệu ứng và mức kỳ vọng GVHD | Chưa có chứng minh thực nghiệm; không đặt “thắng 4/7” làm gate tùy ý |
| Conformal | Đối tượng và đơn vị sampling rõ; calibration đủ thông tin, set có utility | Giữ mở rộng; bỏ lời hứa cellular nếu thiếu điều kiện |

Không dùng “phải có âm cho hai isoform” như gate duy nhất: continuous response/ranking có thể là endpoint khoa học hợp lệ. Nhưng nếu GVHD yêu cầu phân loại **cơ chất trực tiếp** với specificity, dữ liệu response hiện tại chưa đáp ứng. Nếu mapping/replicate không giải được và không còn RQ hợp lệ, mới xét [dự phòng kinase](b-method-layer-draft.md); chưa có trở ngại quyết định buộc chuyển ngay.

### Câu hỏi ưu tiên cho GVHD

1. Thầy chấp nhận endpoint **acetyl hóa phụ thuộc isoform** và kết quả âm về chuyển miền, hay yêu cầu cơ chất trực tiếp? Có cộng tác sinh học để xác thực/tư vấn equivalence margin không?
2. Benchmark theo protein/homology và SIRT3 chuột có đáp ứng yêu cầu test độc lập? Có cần cellular người cho isoform thứ hai?
3. Đóng góp phương pháp ở objective bằng chứng/ordinal/multitask cần ở mức nào so với việc dùng PLM? Thầy ưu tiên RQ nào?
4. Có nên giữ bảy head assay nhưng chỉ SIRT2/3 cellular, và báo SIRT1 theo uncertainty thay vì loại theo số 176?
5. Xin toàn văn SirtSAGE và dữ liệu/nguồn phù hợp từ nhóm; xác định phạm vi website bắt buộc và người dùng.

### Sản phẩm hệ thống phù hợp

Website nhập protein/UniProt ID, kiểm lysine/mapping rồi hiển thị điểm **assay-specific** cho bảy isoform, bằng chứng liên quan, trạng thái context/unknown và phạm vi calibration. Nếu có model cellular được xác thực thì hiển thị ở mục riêng, kèm tế bào/loài và endpoint. Có tải bảng kết quả, provenance và giải thích amino acid; không ghi “cơ chất sinh lý xác nhận” hoặc “90% đúng” trên protein ngoài miền chưa kiểm. Đây là đặc tả cho tiêu chí 5, chưa triển khai trong khảo sát.

## 12. Mức sẵn sàng và thứ tự việc tiếp theo

**Sẵn sàng trình bày như đề xuất cần chốt phạm vi, chưa sẵn sàng bảo vệ các khẳng định mạnh của bản cũ.** Có dữ liệu và vấn đề thật, nhưng tính mới “lần đầu” bị phản bác; benchmark tế bào đầy đủ và bảo đảm conformal vẫn chưa được thiết lập.

1. **Ưu tiên 1:** truy vết SIRT2 Synapse và bảng Hebert/Rardin gốc: metadata mẫu/lặp, site p/q/CI, protein correction; giải 152→149 và SD13/14. Nếu thiếu uncertainty, chốt continuous/positive–unlabeled endpoint với GVHD trước xây nhãn.
2. **Ưu tiên 2:** pin FASTA, mapping site và grouping homology; công bố exclusions/split/cardinality theo isoform. Đếm effective positive proteins; quyết định phạm vi SIRT1 từ bằng chứng đó.
3. **Ưu tiên 3:** hoàn tất full-text NAD_MCNN/SirtSAGE và khảo sát trực tiếp bổ sung, khóa giả thuyết/metric/ablation; chọn đóng góp phương pháp đủ hẹp.
4. **Ưu tiên 4, phiên thực nghiệm sau:** chạy baseline đơn giản rồi PLM/sharing/label/context theo giao thức chung; model selection trên validation, giữ test kín. Không dùng kết quả khảo sát này thay kết quả training.
5. **Ưu tiên 5:** chỉ thêm conformal khi sampling/calibration hợp lệ; kiểm XAI; sau đó triển khai website phản ánh đúng giới hạn đã đo.

Các phần còn thiếu được ghi cụ thể trong [ghi chú bằng chứng](../research_notes/sirtuin-substrate/README.md) và [nhật ký công việc](../../work-log.md). Báo cáo khuyến nghị ban đầu được giữ nguyên để đối chiếu.
