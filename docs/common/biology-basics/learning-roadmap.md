# Lộ trình học sinh học tối thiểu cho hướng cancer và aging

*Soạn 04/10/2026 cho giai đoạn chuẩn bị báo cáo tuần 6. Gắn với các ứng viên trong [khảo sát sâu aging và cancer](../deep-research/reports/aging-cancer-deep-dive.md): **A** (vị trí lysine bị SIRT1–7 deacetyl hóa) và **B** (vị trí phosphoryl hóa theo nhóm kinase gây ung thư).*

> **Bài giảng diễn giải đi kèm:** [docs/common/lectures/](../lectures/) — 15 bài HTML tự học, mở trực tiếp bằng trình duyệt. Lộ trình này vẫn là danh sách tài liệu gốc; bài giảng là phần giải thích và trỏ ngược về đây. Đang viết: mới có [bài 02 — enzyme và PTM](../lectures/02-enzymes-and-ptm.html) và [bài 09 — rò rỉ dữ liệu và chuỗi đồng dạng](../lectures/09-leakage-and-homology.html).

## 0. Nguyên tắc: học đủ để trả lời ba câu GVHD hỏi, không học cả ngành

GVHD yêu cầu trình bày rõ **bài toán là gì, vì sao cần nghiên cứu, và đề tài giải quyết phần nào**. Với sinh viên Kỹ thuật phần mềm, mục tiêu sinh học trong hai tuần tới chỉ là:

1. Giải thích được **đầu vào và đầu ra** của mô hình bằng ngôn ngữ sinh học (một lysine, một serine, một cửa sổ ±10 residue nghĩa là gì).
2. Nói được **vì sao nhãn đó quan trọng** đối với ung thư hoặc lão hóa, bằng một chuỗi nhân quả ngắn có trích dẫn.
3. Hiểu đủ để **đọc phần Introduction và Methods** của các bài trong khảo sát mà không bị kẹt thuật ngữ, và nhận ra khi một bài nói quá.

Cách học hiệu quả nhất là "đúng lúc": học lớp nền mỏng (mục 1), rồi đi thẳng vào sinh học của bài toán (mục 2–4), quay lại giáo trình chỉ khi gặp từ không hiểu. Đừng đọc trọn một cuốn giáo trình.

## 1. Lớp nền (2–3 ngày): từ gene đến protein đến PTM

| Chủ đề | Cần hiểu đến mức | Nguồn miễn phí |
|---|---|---|
| Học thuyết trung tâm: DNA → RNA → protein | Gene mã hóa protein; đột biến làm đổi amino acid | OpenStax *Biology 2e*, chương 14–16 ([openstax.org/details/books/biology-2e](https://openstax.org/details/books/biology-2e)); Khan Academy, phần "Central dogma" |
| 20 amino acid, chuỗi protein, cấu trúc 1–4 bậc | Nhận ra ký hiệu một chữ (K = lysine, S/T/Y = serine/threonine/tyrosine); chuỗi là chuỗi ký tự, cấu trúc 3D quyết định chức năng | OpenStax *Biology 2e*, chương 3; Berg *Biochemistry* 5th ed. chương 3 trên NCBI Bookshelf ([NBK21154](https://www.ncbi.nlm.nih.gov/books/NBK21154/)) |
| Enzyme và cơ chất | "Enzyme X tác động lên vị trí Y của protein Z" nghĩa là gì; tính đặc hiệu cơ chất | Berg chương 8 (NBK21154) |
| **Biến đổi sau dịch mã (PTM)** | PTM là gắn/gỡ một nhóm hóa học lên một residue cụ thể, có enzyme "ghi" và enzyme "xóa"; vì sao dự đoán vị trí PTM là bài toán phân loại cửa sổ quanh residue | Alberts *Molecular Biology of the Cell* 4th ed., chương 3 mục "How proteins are controlled" ([NBK21054](https://www.ncbi.nlm.nih.gov/books/NBK21054/)); Khoury et al. 2011, *Sci Rep*, "Proteome-wide post-translational modification statistics" (truy cập mở, doi:10.1038/srep00090) |
| Tín hiệu tế bào và chu kỳ tế bào | Một con đường tín hiệu là chuỗi protein bật/tắt nhau, phần lớn bằng phosphoryl hóa | Cooper *The Cell: A Molecular Approach* 2nd ed., chương 15 (tín hiệu) và 14 (chu kỳ tế bào) ([NBK9839](https://www.ncbi.nlm.nih.gov/books/NBK9839/)) |

**Nếu thích học bằng video:** MIT OpenCourseWare *7.016 Introductory Biology* (Fall 2018), các bài về protein, enzyme, tín hiệu tế bào và ung thư ([ocw.mit.edu/courses/7-016-introductory-biology-fall-2018](https://ocw.mit.edu/courses/7-016-introductory-biology-fall-2018/)). Chỉ xem những bài khớp với bảng trên, không cần xem hết.

**Tự kiểm tra:** giải thích bằng ba câu cho một bạn học CNTT vì sao "dự đoán lysine nào bị acetyl hóa" lại là bài toán phân loại nhị phân trên chuỗi ký tự, và vì sao nhãn âm lại khó tin cậy (chưa thấy bị biến đổi không có nghĩa là không bao giờ bị biến đổi).

## 2. Cancer (2 ngày): khung "hallmarks" và vai trò của kinase

| Bước | Đọc gì | Mục đích |
|---|---|---|
| 1 | Hanahan & Weinberg 2011, "Hallmarks of Cancer: The Next Generation", *Cell* 144:646–674 (doi:10.1016/j.cell.2011.02.013; bài *Cell* trên 12 tháng nằm trong kho truy cập mở của Cell Press) | Khung chuẩn để nói "vì sao ung thư": tăng sinh không kiểm soát, né apoptosis, v.v. Đọc phần mở đầu và hình tổng quan, lướt từng hallmark |
| 2 | Hanahan 2022, "Hallmarks of Cancer: New Dimensions", *Cancer Discovery* 12:31–46 (truy cập mở, doi:10.1158/2159-8290.CD-21-1059) | Bản cập nhật; chỉ cần biết danh sách mới để trích dẫn đúng năm |
| 3 | Cooper chương 15 (NBK9839), phần các con đường Ras–MAPK và PI3K–Akt | Hiểu CDK, MAPK, AKT, PKC, CK2, GSK3 là ai trong chuỗi tín hiệu, khớp đúng các nhóm kinase trong benchmark dbPTM của ứng viên B |
| 4 | Ubersax & Ferrell 2007, "Mechanisms of specificity in protein phosphorylation", *Nat Rev Mol Cell Biol* 8:530–541 (doi:10.1038/nrm2203; có thể cần quyền truy cập qua thư viện trường) | **Bài quan trọng nhất cho ứng viên B**: vì sao một kinase chọn đúng site, motif tuyến tính quanh site quan trọng đến đâu, và những gì chuỗi cửa sổ **không** thấy được (docking, định vị trong tế bào). Đây là nguồn cho phần "giới hạn của bài toán" |
| 5 (tùy chọn) | Manning et al. 2002, "The protein kinase complement of the human genome", *Science* 298:1912–1934 (doi:10.1126/science.1075762) | Nguồn gốc của khái niệm "kinome" và cây phân loại kinase; chỉ xem hình cây |

**Câu bạn phải nói được ở tuần 6 nếu chọn B:** "Đột biến trong ung thư có thể tạo hoặc phá một site phosphoryl hóa, hoặc làm kinase hoạt động sai, nên biết kinase nào phosphoryl hóa site nào giúp diễn giải đột biến." Số liệu định lượng cho câu này (ActiveDriverDB, 16–21% thay thế amino acid chạm site PTM) trong khảo sát sâu đang mang dấu `[chưa kiểm]`; đọc abstract bài NAR 46(D1):D901 để tự xác nhận trước khi đưa lên slide.

## 3. Aging (2 ngày): khung "hallmarks" và sirtuin

| Bước | Đọc gì | Mục đích |
|---|---|---|
| 1 | López-Otín et al. 2013, "The Hallmarks of Aging", *Cell* 153:1194–1217 (doi:10.1016/j.cell.2013.05.039; kho truy cập mở Cell Press) | Khung chuẩn. Để ý các hallmark "deregulated nutrient sensing", "epigenetic alterations", "loss of proteostasis": sirtuin nằm ở giao điểm của chúng |
| 2 | López-Otín et al. 2023, "Hallmarks of aging: An expanding universe", *Cell* 186:243–278 (doi:10.1016/j.cell.2022.11.001) | Bản 12 hallmark; chỉ cần đọc hình tổng quan và phần liên quan NAD⁺/sirtuin |
| 3 | Houtkooper, Pirinen & Auwerx 2012, "Sirtuins as regulators of metabolism and healthspan", *Nat Rev Mol Cell Biol* 13:225–238 (doi:10.1038/nrm3293; có thể cần thư viện trường) | Bảy isoform SIRT1–7: ở đâu trong tế bào (nhân, ty thể, bào tương), cơ chất tiêu biểu, phụ thuộc NAD⁺. **Đây là kiến thức nền trực tiếp cho ứng viên A** |
| 4 | Narita, Weinert & Choudhary 2019, "Functions and mechanisms of non-histone protein acetylation", *Nat Rev Mol Cell Biol* 20:156–174 (doi:10.1038/s41580-018-0081-3) | Acetyl hóa lysine ngoài histone: ai ghi (KAT), ai xóa (HDAC, sirtuin), và giới hạn của dữ liệu khối phổ. Đọc phần đầu và phần về sirtuin |
| 5 | Bài nguồn của ứng viên A ([PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/)), chỉ phần Introduction | Lúc này bạn sẽ đọc được; kiểm tra xem mình hiểu vì sao precision 2% của permutation array là con số đáng nói |

**Câu bạn phải nói được ở tuần 6 nếu chọn A:** "Thuốc nhắm SIRT chỉ có ý nghĩa khi biết isoform đó thực sự deacetyl hóa protein nào; thực nghiệm hiện tại xác định cơ chất với precision rất thấp, nên dự đoán theo từng isoform giúp thu hẹp danh sách cần kiểm chứng." Lưu ý cẩn trọng: liên hệ sirtuin với kéo dài tuổi thọ ở người còn gây tranh cãi; nói "liên quan con đường lão hóa", đừng nói "chống lão hóa".

## 4. Thực hành trên cơ sở dữ liệu (rải xen, khoảng nửa ngày)

Đọc lý thuyết xong thì mở dữ liệu thật; đây là chỗ sinh viên CNTT học nhanh nhất.

1. **UniProt.** Mở các mục TP53 (P04637), SIRT1 (Q96EB6), AKT1 (P31749). Xem tab "Function", "PTM/Processing" và "Subcellular location". Ghi lại: một site PTM được chú thích kèm bằng chứng gì (bài báo, suy luận theo đồng dạng).
2. **dbPTM** ([biomics.lab.nycu.edu.tw/dbPTM](https://biomics.lab.nycu.edu.tw/dbPTM/)). Tìm một protein bạn đã mở ở bước 1, xem các site acetyl hóa và phosphoryl hóa, và một cửa sổ ±10 residue trông thế nào.
3. **Dữ liệu ứng viên A.** Mở file nhãn đã ghi trong khảo sát sâu, lấy dòng `P05141_163`, tra P05141 trên UniProt, tự trả lời: protein này là gì, ở đâu trong tế bào, có hợp lý không khi nó là cơ chất của SIRT ty thể.

Bài tập này cũng là chất liệu tốt cho slide "đầu vào/đầu ra là gì" ở tuần 6.

## 5. Lịch gợi ý cho khoảng 10 ngày trước báo cáo tuần 6

| Ngày | Việc |
|---|---|
| 1–2 | Lớp nền mục 1 (central dogma, amino acid, enzyme, PTM) |
| 3 | Thực hành UniProt/dbPTM (mục 4, bước 1–2) |
| 4–5 | Cancer (mục 2, bước 1–4) |
| 6–7 | Aging (mục 3, bước 1–5) và bước 3 của mục 4 |
| 8 | Viết một trang "động cơ sinh học" cho mỗi ứng viên A và B: bài toán, vì sao quan trọng, chuỗi nhân quả có trích dẫn, giới hạn. Đây chính là phần GVHD nhấn mạnh |
| 9–10 | Đọc lại phần Introduction của các bài trong khảo sát sâu; đánh dấu thuật ngữ còn mù mờ và quay lại giáo trình đúng chỗ đó |

Nếu thiếu thời gian, ưu tiên theo thứ tự: PTM (mục 1) → sirtuin hoặc kinase tùy hướng nghiêng → hallmarks → phần còn lại.

## 6. Bảng thuật ngữ cần nắm

| Thuật ngữ | Nghĩa ngắn |
|---|---|
| Residue | Một amino acid trong chuỗi protein |
| PTM (post-translational modification) | Biến đổi hóa học trên residue sau khi protein được tổng hợp |
| Acetyl hóa / deacetyl hóa lysine | Gắn / gỡ nhóm acetyl trên K; sirtuin là enzyme gỡ, cần NAD⁺ |
| Phosphoryl hóa | Gắn nhóm phosphate lên S/T/Y; do kinase thực hiện, phosphatase gỡ |
| Isoform SIRT1–7 | Bảy protein cùng họ sirtuin, khác vị trí trong tế bào và cơ chất |
| Kinase group (CDK, MAPK, AKT…) | Nhóm kinase gần nhau về trình tự và motif nhận diện |
| Motif | Mẫu amino acid quanh site mà enzyme nhận ra (ví dụ proline ngay sau site với kinase CDK/MAPK) |
| Substrate (cơ chất) | Protein mà enzyme tác động lên |
| Oncogene / tumor suppressor | Gene khi hoạt động quá mức / mất chức năng thì thúc đẩy ung thư |
| Mass spectrometry (MS) | Kỹ thuật thực nghiệm chính để phát hiện site PTM; nguồn của phần lớn nhãn dương |
| Homology (đồng dạng) | Hai chuỗi giống nhau do cùng nguồn gốc; lý do phải gom cụm khi chia tập train/test |

## 7. Lưu ý về độ tin cậy

- Các tài liệu và DOI ở trên là nguồn kinh điển Claude biết từ kiến thức huấn luyện; **chưa mở lại từng link trong phiên này**. Nếu một link hỏng, tìm theo tên bài trên PubMed hoặc Google Scholar.
- Những bài *Nat Rev Mol Cell Biol* có thể cần đăng nhập thư viện trường; nếu không có, abstract cộng một review truy cập mở cùng chủ đề trên PMC là đủ cho mục tiêu tuần 6.
- Nếu đi theo B, nhớ rằng theo khảo sát sâu **GVHD chưa có bài PTM/phospho nào**, nên phần sinh học của B bạn phải tự đứng vững nhiều hơn A.

## 8. Danh sách tài liệu cần tải vào `papers/`

Ngày 04/10/2026 phiên làm việc trên cloud **không tải được** file nào: chính sách mạng của môi trường chặn các host xuất bản và PubMed (ebi.ac.uk, ncbi.nlm.nih.gov, nature.com, cell.com, openstax.org, doi.org đều bị proxy trả 403). Khi tải được (từ máy cá nhân hoặc sau khi mở mạng), lưu vào `docs/common/biology-basics/papers/` theo tên dưới đây rồi đánh dấu cột cuối.

| Tên file đề xuất | Tài liệu | Truy cập (theo hiểu biết, chưa kiểm lại) | Đã tải |
|---|---|---|---|
| `khoury-2011-ptm-statistics.pdf` | Khoury et al. 2011, *Sci Rep*, doi:10.1038/srep00090 | Mở | ☐ |
| `hanahan-weinberg-2011-hallmarks-cancer.pdf` | Hanahan & Weinberg 2011, *Cell*, doi:10.1016/j.cell.2011.02.013 | Kho mở Cell Press | ☐ |
| `hanahan-2022-hallmarks-cancer-new-dimensions.pdf` | Hanahan 2022, *Cancer Discov*, doi:10.1158/2159-8290.CD-21-1059 | Mở | ☐ |
| `lopez-otin-2013-hallmarks-aging.pdf` | López-Otín et al. 2013, *Cell*, doi:10.1016/j.cell.2013.05.039 | Kho mở Cell Press | ☐ |
| `lopez-otin-2023-hallmarks-aging-expanding.pdf` | López-Otín et al. 2023, *Cell*, doi:10.1016/j.cell.2022.11.001 | Kiểm lại | ☐ |
| `houtkooper-2012-sirtuins-metabolism.pdf` | Houtkooper et al. 2012, *Nat Rev Mol Cell Biol*, doi:10.1038/nrm3293 | Có thể cần thư viện; thử bản PMC | ☐ |
| `narita-2019-non-histone-acetylation.pdf` | Narita et al. 2019, *Nat Rev Mol Cell Biol*, doi:10.1038/s41580-018-0081-3 | Có thể cần thư viện | ☐ |
| `ubersax-ferrell-2007-phosphorylation-specificity.pdf` | Ubersax & Ferrell 2007, *Nat Rev Mol Cell Biol*, doi:10.1038/nrm2203 | Có thể cần thư viện | ☐ |
| `sirt-substrate-ml-2025.pdf` | Bài nguồn ứng viên A, [PMC12594832](https://pmc.ncbi.nlm.nih.gov/articles/PMC12594832/) | Mở | ☐ |

Giáo trình (OpenStax, NCBI Bookshelf) và khóa MIT OCW chỉ cần giữ link, không tải. Nhớ quy ước repo: PDF bài báo chỉ được giữ khi repo còn private.
