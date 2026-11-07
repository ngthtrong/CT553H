# Kiểm chứng tài liệu và lập luận sinh học — 06/11/2026

Phạm vi: các nguồn trọng yếu đang dùng trong phần mở đầu/cơ sở lý thuyết và các nguồn mới cần để giải thích tính cấp thiết. Đây là rà soát có mục tiêu, **không phải systematic review** và không chứng minh toàn bộ tính mới. Đọc nguồn trực tuyến, đối chiếu thông tin thư mục với Crossref khi có DOI; dùng nguồn gốc/tác giả và bài báo, không dùng trang tổng hợp để xác lập kết quả khoa học. Không tải dataset mới, không thay dữ liệu huấn luyện, không chạy mô hình.

Nhãn: **[NGUỒN]** là nội dung nguồn hỗ trợ; **[DIỄN GIẢI]** là áp dụng cho CT553H; **[CHƯA KIỂM CHỨNG]** là giới hạn còn lại. Báo cáo vẫn viết tiếng Anh theo quy ước hiện có; hồ sơ kiểm toán đi kèm viết tiếng Việt.

## Các sửa sai cụ thể

- Tác giả thứ nhất Zhang 2023 và Mendeley là **Zhiqian Zhang**, không phải Zhiwei Zhang; đối chiếu PubMed, Crossref và Mendeley version 2.
- Larsen 2025 là **Fia B. Larsen**, không phải Frederik B.; đối chiếu Crossref và repository của nhóm tác giả. Giữ đúng phiên bản preprint được dẫn, không suy diễn rằng phần dữ liệu đã được nhập vào benchmark ΔPSI.
- MetaDegron là **Mengqiu Zheng**, không phải Mingxuan Zheng; đối chiếu metadata DOI và bản bài báo được lập chỉ mục tại PMC.
- DEGRONOPEDIA và DegronMD được thay các bản ghi trang web/TO VERIFY bằng bài báo gốc và DOI xác minh được. Đã bổ sung DOI/URL gốc cho các nguồn nền tảng có thể kiểm chứng; không còn marker TO VERIFY trong bibliography.
- Không giữ khẳng định quá rộng rằng các nghiên cứu trước chỉ làm peptide/motif và chưa nghiên cứu hiệu ứng biến thể: PAP đã có ΔPAP và khảo sát/kiểm chứng một số biến thể. Degformer có chế độ dự đoán mutant PSI. Phần gap được viết lại thành câu hỏi đánh giá có phạm vi cụ thể.
- PAP là **Peptide Abundance Predictor**. Chênh lệch điểm mutant–WT là một reference score; không mặc định nó đã cùng đơn vị hay đã hiệu chuẩn thành ΔPSI.
- Degformer được dẫn là phần mềm ở commit đã dùng trong nghiên cứu; không gán năm công bố học thuật khi chưa xác lập được. Ngày kiểm tra nguồn không được thay cho năm công bố.

## Danh mục nguồn được đối chiếu

Mọi URL dưới đây được truy cập hoặc tra cứu trong lượt này ngày 06/11/2026. “Metadata” nghĩa là đã kiểm thông tin thư mục, không đồng nghĩa đã đọc lại toàn bộ bài hoặc tái lập kết quả của tác giả.

| Khóa BibTeX | Nguồn có DOI/URL | Mức kiểm và vai trò hợp lệ |
|---|---|---|
| `zhang2023` | Zhang et al., *Molecular Cell* 83(18), 3377–3392.e6, 2023. [DOI](https://doi.org/10.1016/j.molcel.2023.08.022); [toàn văn PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10594193/); [PubMed](https://pubmed.ncbi.nlm.nih.gov/37738965/) | [NGUỒN] Kiểm phần assay sáu bin, mutagenesis, giới hạn peptide/cell context và validation. Không chuyển 219 motif tác giả curate thành số peptide QC của CT553H. |
| `zhang2023data` | [Mendeley Data v2](https://data.mendeley.com/datasets/32h94v2yv2/2), DOI 10.17632/32h94v2yv2.2 | [NGUỒN] Trang nhà cung cấp xác nhận phiên bản, tác giả, loại dữ liệu và CC BY 4.0. Không tải lại hoặc thay hash dữ liệu local. |
| `geo240610` | [GSE240610](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240610) | **Không thể truy cập nội dung live**: reCAPTCHA. Giữ link từ hồ sơ nguồn của repo; không gọi đây là một lần kiểm lại nội dung GEO thành công. |
| `voutsinos2026` | Voutsinos et al., *Science Advances* 12(6), eadz3483, 2026. [DOI](https://doi.org/10.1126/sciadv.adz3483); [toàn văn](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880521/); [PubMed](https://pubmed.ncbi.nlm.nih.gov/41650254/) | [NGUỒN] Kiểm PAP/CNN, ΔPAP, buried/exposed context và một số biến thể được follow-up. Không dùng tương quan tác giả như metric của CT553H. |
| `larsen2025` | Larsen et al., *Comprehensive degron mapping in human transcription factors*, bioRxiv v1. [DOI](https://doi.org/10.1101/2025.05.16.654404); [repo tác giả](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors) | Metadata DOI và tác giả/repo được kiểm. Trang bioRxiv v1 trả 403; không khẳng định đã đọc lại toàn văn live. README nhóm vẫn dẫn Preprint. Có archive dữ liệu 2026 không tự biến thành một bài peer-reviewed đã xác minh. |
| `zheng2024` | Zheng et al., *Briefings in Bioinformatics* 25(6), bbae519, 2024. [DOI](https://doi.org/10.1093/bib/bbae519); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/) | Metadata Crossref và nội dung bài được lập chỉ mục: PLM/feature integration, E3-targeted degron task. Một số lần mở PMC/OUP trả reCAPTCHA/redirect; không coi việc mở URL bị chặn là full-text review mới. Không dùng nhãn motif để thay ΔPSI. |
| `degronopedia` | Szulc et al., *Nucleic Acids Research* 52(W1), W221–W232, 2024. [DOI](https://doi.org/10.1093/nar/gkae238); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11223883/); [trang tác giả](https://degronopedia.com/degronopedia/about) | [NGUỒN] Kiểm chức năng motif/context và thông tin thư mục; một lần PMC đọc được, lần khác bị reCAPTCHA. Công cụ annotation không phải benchmark substitution regression cùng endpoint. |
| `degronmd` | Xu, Hu & Zhao, *Molecular Biology and Evolution* 40(12), msad253, 2023. [DOI](https://doi.org/10.1093/molbev/msad253); [PubMed](https://pubmed.ncbi.nlm.nih.gov/37992195/); [nguồn dữ liệu tác giả](https://bioinfo.uth.edu/degronmd/download.html) | Metadata, mục tiêu và bảng tài nguyên mutation được đối chiếu; PMC full-text bị reCAPTCHA. Không dẫn để khẳng định cơ chế một biến thể CT553H. |
| `degformer` | [Alpine2048/Degformer](https://github.com/Alpine2048/Degformer), snapshot nghiên cứu `49ee52459967` | [NGUỒN] README live có prediction PSI, saturation/scanning/protein scanning. Năm công bố học thuật và peer-review chưa xác lập; không tạo publication record. Commit thí nghiệm vẫn là commit audit trong repo, không mặc định HEAD live giống snapshot. |
| `varshavsky2019` | Varshavsky, *PNAS* 116(2), 358–366, 2019. [DOI](https://doi.org/10.1073/pnas.1816596116); [PubMed](https://pubmed.ncbi.nlm.nih.gov/30622213/) | [NGUỒN] N-/C-degron, phụ thuộc sequence context; tài liệu perspective/review được ghi đúng loại, không nhận làm kết quả riêng của CT553H. |
| `koren2018` | Koren et al., *Cell* 173(7), 1622–1635.e14, 2018. [DOI](https://doi.org/10.1016/j.cell.2018.04.028); [PubMed](https://pubmed.ncbi.nlm.nih.gov/29779948/) | Metadata và nghiên cứu thực nghiệm C-terminal degron; sửa dải trang đủ hậu tố .e14. |
| `yen2008` | Yen et al., *Science* 322(5903), 918–923, 2008. [DOI](https://doi.org/10.1126/science.1160489); [PubMed](https://pubmed.ncbi.nlm.nih.gov/18988847/) | [NGUỒN] GPS nguyên thủy. Công thức tái dựng sáu-bin cụ thể của CT553H được kiểm thêm bằng code, không gán toàn bộ lựa chọn preprocessing của CT553H cho bài năm 2008. |
| `hoerl1970` | Hoerl & Kennard, *Technometrics* 12(1), 55–67, 1970. [DOI](https://doi.org/10.1080/00401706.1970.10488634); [bản bài gốc](https://www.stat.cmu.edu/technometrics/70-79/VOL-12-01/v1201055.pdf) | Metadata DOI Crossref và bài gốc; không nhầm với bản in lại năm 2000 có DOI/dải trang khác. |
| `steinegger2017` | Steinegger & Söding, *Nature Biotechnology* 35(11), 1026–1028, 2017. [DOI](https://doi.org/10.1038/nbt.3988); [PubMed](https://pubmed.ncbi.nlm.nih.gov/29035372/) | Metadata và chức năng công cụ. Ngưỡng cov80/cov50 và các union là thiết kế CT553H, không phải bảo đảm độc lập sinh học từ bài MMseqs2. |
| `vaswani2017` | Vaswani et al., *NeurIPS 30*, 2017. [Trang proceedings](https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) | Metadata và transformer/attention gốc; không thêm DOI từ các bản ghi trùng không phải proceedings. |
| `efron1979` | Efron, *Annals of Statistics* 7(1), 1–26, 1979. [DOI](https://doi.org/10.1214/aos/1176344552) | Metadata DOI và nguyên lý bootstrap. Resampling theo cụm/paired và chỉnh multiplicity được mô tả là lựa chọn protocol của CT553H. |
| `lin2023esm` | Lin et al., *Science* 379(6637), 1123–1130, 2023. [DOI](https://doi.org/10.1126/science.ade2574) | Metadata Crossref; cơ sở ESM-2/contextual protein representations. Không dùng structure-prediction performance trong bài để chứng minh ΔPSI performance. Science live trả 403, không khẳng định đã đọc lại toàn bộ bài live. |
| `hu2022lora` | Hu et al., ICLR 2022. [Bài conference](https://openreview.net/pdf?id=nZeVKeeFYf9); [arXiv](https://arxiv.org/abs/2106.09685) | [NGUỒN] Kiểm low-rank adaptation/base frozen và publication ICLR; không chuyển mức giảm bộ nhớ NLP thành số tiết kiệm GPU của CT553H. |
| `balch2008` (mới) | Balch et al., *Science* 319(5865), 916–919, 2008. [DOI](https://doi.org/10.1126/science.1141448); [PubMed](https://pubmed.ncbi.nlm.nih.gov/18276881/) | [NGUỒN] Proteostasis network; metadata và abstract được đối chiếu. Là review nền, không bằng chứng hiệu quả triển khai CT553H. |
| `fowler2010` (mới) | Fowler et al., *Nature Methods* 7(9), 741–746, 2010. [DOI](https://doi.org/10.1038/nmeth.1492); [PubMed](https://pubmed.ncbi.nlm.nih.gov/20711194/); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2938879/) | [NGUỒN] Bài thực nghiệm sequence–function mapping; hỗ trợ nhu cầu đo nhiều substitution và giữ phenotype/assay scope. |
| `matreyek2018` (mới) | Matreyek et al., *Nature Genetics* 50(6), 874–882, 2018. [DOI](https://doi.org/10.1038/s41588-018-0122-z); [toàn văn](https://pmc.ncbi.nlm.nih.gov/articles/pmid/29785012/) | [NGUỒN] 7.801 variant PTEN/TPMT, replicate/QC và giới hạn protein phù hợp assay; không đồng nhất VAMP-seq abundance với Zhang PSI. |
| `bernett2024` (mới) | Bernett et al., *Nature Methods* 21(8), 1444–1453, 2024. [DOI](https://doi.org/10.1038/s41592-024-02362-y) | [NGUỒN] Guiding questions về leakage trong biological ML; perspective phương pháp, không phải chứng minh cụ thể split CT553H không rò rỉ. |

Crossref có một số phản hồi 429 khi lặp lại kiểm metadata; các trường hợp Varshavsky/Koren/MMseqs2 có PubMed/nguồn publisher đối chiếu thành công. Không coi response 429 là “DOI không tồn tại”.

## Ma trận lập luận: nguồn hỗ trợ gì và CT553H được nói đến đâu

| Luận điểm | Bằng chứng nguồn | Áp dụng và giới hạn |
|---|---|---|
| Protein amount/lifetime phải được điều hòa | Balch 2008; Yen 2008 | [NGUỒN] Cơ sở proteostasis và đo turnover. Không suy ra mọi thay đổi abundance là thay đổi degradation rate. |
| Degron và mutation đáng khảo sát | Zhang 2023; Koren 2018; PAP 2026 | [NGUỒN] Có nghiên cứu thực nghiệm/mô hình trước. [DIỄN GIẢI] Hợp lý để đặt bài toán dự đoán mutation-effect trên endpoint cụ thể. |
| Wet-lab có giới hạn độ phủ/context | Zhang limitations; VAMP-seq applicability; Fowler map | [NGUỒN] Coverage, sequence context, phenotype và assay compatibility hữu hạn. Không nêu chi phí/thời gian định lượng khi chưa có dữ liệu. |
| Model có thể hỗ trợ chọn biến thể | PAP có khảo sát và follow-up variant; công cụ annotation có ca kiểm chứng | [DIỄN GIẢI] Có tiền lệ tương tự, nhưng CT553H chỉ có bằng chứng prediction/software. Tiết kiệm wet-lab và tăng yield là giả thuyết cần prospective study. |
| Higher PSI/positive ΔPSI | Zhang six-bin assay + `build_psi.py`; WT references trong `residue_data.py` | [ĐỐI CHIẾU CODE] Index reporter và dấu effect, không half-life/ΔΔG/E3 identification. |
| Degron peptide không đại diện đầy đủ protein tự nhiên | Zhang limitations; Voutsinos buried/exposed analysis | [NGUỒN] Cần giữ structural/cellular context và các ngoại lệ. Không gọi tiling whole protein là full-protein validation. |
| PLM/CNN/LoRA đáng thử | ESM-2; PAP CNN; LoRA gốc | [DIỄN GIẢI] Cơ sở lựa chọn kiểm thử, không bằng chứng chúng mặc định tốt hơn ridge hoặc một kiến trúc mới. |
| Cần tránh tương đồng train/test và chọn model trên test | Bernett 2024 + protocol CT553H | [DIỄN GIẢI] Grouped/nested procedure giảm các kênh rò rỉ đã nêu. Không chứng minh loại hết remote homology, motif overlap hoặc corpus pLM exposure. |

## Nội dung báo cáo được bổ sung hoặc điều chỉnh

1. Mở đầu đi từ protein → proteostasis → selective degradation → degron/mutation → đo thực nghiệm → giới hạn → mô hình → câu hỏi riêng của CT553H. Tách lý do khoa học khỏi giả định lợi ích triển khai.
2. Năm RQ gắn coverage, representation/head, transfer, adaptation, generalisation/calibration; ghi rõ đây là cách hệ thống hóa tiến độ và protocol hiện có, không phải preregistration độc lập trước các kết quả lịch sử.
3. Cơ sở lý thuyết bổ sung protein/peptide/residue/WT/mutant; UPS E1/E2/E3 và degron context; phân biệt abundance, turnover, half-life, thermodynamic stability; PSI sáu-bin và WT baseline; measurement cell không phải biological cell; one-hot/ridge/pLM/CNN/mCNN/frozen/LoRA; leakage/nested/MAE/ranking/calibration/CI.
4. Hai sơ đồ TikZ là minh họa khái niệm do CT553H tự vẽ; chú thích nêu rõ không phải cơ chế được đo hay kết quả wet-lab. Không sao chép hình của tác giả, không dùng PSI giả làm số liệu thực.
5. Giữ tên đề tài, ngôn ngữ và cấu trúc nguồn báo cáo hiện có; không sửa proposal, template, presentation hoặc model serving.

## Phần chưa đủ bằng chứng và nguồn đã tìm

| Nội dung còn thiếu | Trạng thái | Ảnh hưởng | Nguồn đã kiểm tra | Cách bổ sung | Ưu tiên |
|---|---|---|---|---|---|
| Hiệu quả ưu tiên biến thể trong wet-lab thật của CT553H | Chưa tìm thấy kết quả trong phạm vi báo cáo/audit được giao | Chưa chứng minh tiết kiệm thời gian/chi phí hay tăng hit rate | Report hiện có, protocol v3; các bài nguồn ở trên chỉ là tiền lệ | Protocol prospective, đo số biến thể thử, số hit, thời gian và chi phí với đối chứng; không chạy tự động trong lượt sửa tài liệu | Cao nếu muốn claim ứng dụng; không chặn báo cáo tiến độ |
| Tính mới tuyệt đối hoặc “đầu tiên” | Chưa được kiểm chứng | Không được kết luận novelty chỉ từ ESM-2+CNN hoặc bảng xếp hạng | PAP, MetaDegron, DEGRONOPEDIA/DegronMD, Degformer; tìm thêm deepDegron và mutational-degron studies | Systematic scoping search có query/date/inclusion criteria và bảng task/endpoint/split; đối chiếu bài mới trước chốt novelty | Cao trước khi công bố |
| Literature trong nước | Chưa hoàn thành | Không đủ cơ sở claim đầu tiên ở Việt Nam | Mục Domestic Context bản cũ là PENDING; lượt này không có scoped national search hoàn chỉnh | Tra cứu học thuật có chủ đích và ghi search log; giữ hạn chế công khai | Thấp đối với phân tích model, trung bình đối với related work cuối |
| Full text live Larsen v1 | Không thể truy cập (403) | Không gọi lượt này là reread toàn văn; không suy status peer-review mới | Crossref DOI; GitHub tác giả; bioRxiv URL | Đọc bản đã lưu hợp lệ hoặc truy cập nguồn chính thức khi khả dụng; không cần tải dữ liệu lại | Trung bình |
| Nội dung live GEO GSE240610 | Không thể truy cập (reCAPTCHA) | Không xác minh lại metadata/nội dung GEO qua URL live trong lượt này | URL GEO; sổ nguồn của repository | Truy cập provider khi khả dụng, so sánh manifest đã ghim; giữ bằng chứng local riêng | Trung bình |
| Bài mới 2026 ngoài corpus đang dùng | Chưa được kiểm chứng đầy đủ | Bằng chứng bổ sung cần trước claim novelty, không thay kết quả dự án | Tìm kiếm thấy [preprint Sep 2026 về disease mutation/neo-substrate degrons](https://www.biorxiv.org/content/10.64898/2026.09.17.752235v1.full) và [deepDegron-associated study](https://www.nature.com/articles/s41467-021-26871-y) | Đọc và đánh giá endpoint/data/assay/split khi chốt systematic related work; chưa nhập citation để chống lưng kết luận chưa đọc đủ | Trung bình |

Không có nguồn ngoài nào được dùng để điền metric, fold, kết quả local hay thí nghiệm thiếu của CT553H.
