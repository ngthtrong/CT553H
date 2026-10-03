# So sánh hai hướng GVHD gợi ý: aging và cancer

> **Bản khảo sát lần 1, ngày 02/10/2026.** Phục vụ việc chọn đề tài mới sau [buổi gặp GVHD lần 1](../../../meeting/session-01-minutes.md), trước mốc **báo cáo lại đề tài ở tuần 6** (hiện tuần 4).
>
> **Trạng thái:** khảo sát bước đầu, **chưa đủ để chốt đề tài**. Mỗi khẳng định đều có cột nguồn và mức kiểm chứng. Chỗ nào chưa kiểm được thì ghi rõ là chưa kiểm, không suy đoán thành kết luận.
>
> **Mức kiểm chứng dùng trong tài liệu này:** `[PDF]` đọc trực tiếp từ PDF trong repo · `[curl]` tự kiểm bằng truy vấn mạng · `[abstract]` từ phần mô tả/abstract tra được, **chưa đọc toàn văn** · `[chưa kiểm]`.

## 1. Vì sao có tài liệu này

GVHD khuyên thay đề tài RTK–ATP, gợi ý **aging** hoặc **cancer**. Khi tra [danh mục công bố của GVHD](../../advisor/README.md) thì thấy một điểm lệch đáng chú ý: trong 14 công trình của GVHD **không có công trình nào về cancer**, còn **aging thì có mặt ở công trình mới nhất** (SirtSAGE, họ sirtuin). Nhánh neoantigen mà trước đó được đề xuất thuộc danh mục **Prof Ou**, không phải GVHD.

Vì khác biệt này chỉ là suy luận từ danh mục công bố, và bản danh mục có thể chưa đầy đủ, quyết định của sinh viên là **khảo sát cả hai hướng rồi so sánh trên cùng bộ tiêu chí** thay vì chọn ngay.

## 2. Bộ tiêu chí so sánh

Gồm [năm tiêu chí GVHD nêu](../../../meeting/session-01-minutes.md) cộng ba ràng buộc thực tế của học phần.

| # | Tiêu chí | Vì sao quan trọng ở đây |
|---|---|---|
| T1 | Tính mới của đề tài/hướng đi | Chính tiêu chí mà RTK–ATP đã không đạt |
| T2 | Đề xuất hoặc cải tiến phương pháp | |
| T3 | Sử dụng phương pháp mới (xa hơn PLM) | GVHD nhấn mạnh bằng câu chuyện PSSM → PLM |
| T4 | XAI | GVHD có tiền lệ riêng: BERT-Promoter (2022, SHAP) |
| T5 | Ứng dụng/website | **Không thể thiếu** |
| R1 | **Dữ liệu công khai có tập test độc lập** | Yếu tố loại hướng đi nhanh nhất. Hướng IL-6 từng bị loại đúng vì lý do này |
| R2 | Mức khớp với chuyên môn GVHD | Quyết định chất lượng hướng dẫn và độ sâu câu hỏi phản biện |
| R3 | Khả thi trong **8–9 tuần** thực hiện, kèm cả web app | Ngân sách thật sau khi trừ 2 tuần chốt đề tài |

## 3. Hướng A — aging

Khảo sát cho thấy aging **không chỉ có nhánh sirtuin**. Có hai nhánh con khác nhau rõ rệt về rủi ro dữ liệu.

### A1. Sirtuin — nhánh của chính GVHD

Chuỗi công trình:

| Công trình | Năm | Phương pháp | Kết quả | Nguồn |
|---|---|---|---|---|
| **DeepSIRT** — nhận diện *sirtuin target* và định vị dưới tế bào | 2021, *Comput Biol Chem* | 1D-CNN + **PSSM, AAC** | accuracy **76,69%**, MCC **0,49**, AUC **0,833** | `[abstract]` [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1476927121000815) |
| **SirtSAGE** — phân loại hợp nhất và lập bản đồ tiến hóa họ sirtuin | 2026, *J. Comput. Biophys. Chem.* | **ESM-2 → GATv2**, điểm **pLDDT làm cổng tin cậy không gian** | chưa đọc được số liệu | `[abstract]` [World Scientific](https://www.worldscientific.com/doi/abs/10.1142/S2737416527400011) — trang trả HTTP 403 khi tải trực tiếp |

Nhận xét:

- **DeepSIRT có khoảng trống rất rộng về số liệu** (MCC 0,49). Đây là điểm mà một mô hình PLM hiện đại thường cải thiện mạnh — nhưng SirtSAGE 2026 có thể đã lấy phần cải thiện đó rồi.
- **SirtSAGE chính là lời giải cho tiêu chí T3 mà GVHD gợi ý:** nó đi từ PSSM (DeepSIRT) sang ESM-2 **cộng Graph Attention + thông tin cấu trúc**, tức **ra khỏi khuôn PLM + mCNN** của nhóm. Câu hỏi "liệu có tìm thêm phương pháp nào mới mẻ hơn không?" ở buổi gặp có thể đang chỉ về chính hướng này.
- **Rủi ro T1 rất cao:** đây là bài vừa công bố của GVHD. Làm lại cùng bài toán là lặp đúng cái bẫy đã khiến RTK–ATP mất T1.
- **Rủi ro dữ liệu (R1) đã hiện ra ngay:** trang dữ liệu DeepSIRT `http://140.138.155.216/deepsirt/` **không truy cập được** — `[curl]` hết thời gian chờ sau 20 giây. Dữ liệu của SirtSAGE thì `[chưa kiểm]` vì bài bị chắn.
- Bài toán là **mức protein** (phân loại protein nào thuộc họ/đích nào), khác mức residue của RTK–ATP.

Một nhánh con còn mở: **dự đoán vị trí lysine bị deacetyl hóa bởi từng SIRT** — tức mức residue. Công trình 2025 trên *Commun Chem* làm substrate của enzyme PTM với tập **6.801 peptide dài 13 aa** và **443 đặc trưng**, nhưng precision còn thấp (SIRT2 khoảng **43,0%** khi xác nhận bằng MS) `[abstract]` [Nature Commun Chem](https://www.nature.com/articles/s42004-025-01717-6) · [PubMed 41203923](https://pubmed.ncbi.nlm.nih.gov/41203923/). Precision thấp nghĩa là **còn khoảng trống thật**, và bài toán ở **mức residue với cửa sổ quanh lysine** — trùng đúng dạng pipeline sinh viên đã quen từ RTK–ATP.

### A2. Cellular senescence — nhánh rộng hơn, dữ liệu công khai tốt hơn

| Công trình | Năm | Phương pháp | Kết quả | Dữ liệu |
|---|---|---|---|---|
| **SenSeqNet** — phát hiện lão hóa tế bào **từ trình tự protein** | 2026, *Aging Cell* | **ESM-2 + LSTM–CNN** | accuracy **86,43%** trên test độc lập | **Mã nguồn và tập benchmark công khai trên GitHub** |

Nguồn: `[abstract]` [Aging Cell](https://onlinelibrary.wiley.com/doi/full/10.1111/acel.70344) · [PubMed 41432347](https://pubmed.ncbi.nlm.nih.gov/41432347/) · [PMC12724000](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12724000/) · [bản preprint bioRxiv](https://www.biorxiv.org/content/10.1101/2024.10.28.620702v2.full).

Dữ liệu: gene lão hóa tế bào từ **CellAge**, trình tự từ **UniProtKB** làm mẫu dương; **housekeeping gene** làm mẫu âm. Quy mô công bố: **238.634 dương / 217.696 âm**.

**Một điểm cần kiểm chứng, có thể là khoảng trống thật:** CellAge là cơ sở dữ liệu gene lão hóa **quy mô khoảng vài trăm tới dưới một nghìn gene**. Con số 238.634 trình tự dương gợi ý tập dữ liệu được mở rộng rất nhiều từ một số gene gốc nhỏ — qua isoform, ortholog hoặc biến thể. Nếu đúng vậy thì **nguy cơ rò rỉ đồng dạng giữa tập huấn luyện và tập test là cao**, và con số 86,43% có thể lạc quan.

Đây **chưa phải kết luận** — mới là giả thuyết từ sự chênh lệch quy mô. Cách kiểm cụ thể, làm được trong 1–2 ngày: tải tập benchmark trên GitHub, đếm **số gene/protein gốc không trùng** so với số trình tự, rồi chạy **CD-HIT hoặc MMseqs2** giữa tập train và test ở ngưỡng 30%/40% identity. Nếu phát hiện rò rỉ thì đây là khoảng trống đúng loại **sinh viên đã có kinh nghiệm** từ giao thức kiểm soát rò rỉ của RTK–ATP, và tái dùng được phần lớn công đã làm.

## 4. Hướng B — cancer (neoantigen)

### Công trình của nhóm

| Công trình | Năm | Thuộc ai | Nội dung |
|---|---|---|---|
| **NeoGen-BC** | 2026, *BBRC* | **Prof Ou**, không phải GVHD | Thiết kế neoantigen **dùng chung** cho ung thư vú HR+ và TNBC |
| **DeepNeoAG** | 2024, *IJBM* | Prof Ou | Dự đoán epitope neoantigen từ kháng nguyên melanoma |

Chi tiết NeoGen-BC, `[PDF]` đọc trực tiếp từ [`Prof Ou/1-s2.0-S0006291X26013318-main.pdf`](../../advisor/Prof%20Ou/):

- Kiến trúc: **PLM embedding + RAG + MCNN-BiLSTM đa thang**, cộng **chiến lược cửa sổ trượt** để map epitope từ driver mutation, cộng **module sinh ProtGPT2 có kiểm soát**, rồi lọc theo đặc tính hóa lý, xác nhận cấu trúc và sàng lọc tính sinh miễn dịch.
- **AUC 0,9053** trên tập test độc lập.
- Phát hiện đúng các neoantigen dùng chung hạn chế MHC class II đã được xác nhận thực nghiệm, từ đột biến **ESR1 (Y537S, D538G)** và **PIK3CA (H1047R)** — những trường hợp mà **NetMHCIIpan 4.3** thường bỏ sót.
- Đồng tác giả lâm sàng: Trung tâm Sức khỏe Vú, Bệnh viện Cựu chiến binh Đài Bắc.

**Nhận xét về R3:** đây là pipeline **nhiều tầng và rất nặng**. Để đóng góp thêm được vào đó trong 8–9 tuần, lại còn phải kèm web app, là rủi ro cao. Phần sinh và xác nhận cấu trúc là hai khối việc lớn tách biệt.

### Mức cạnh tranh bên ngoài

Nhánh này **đông hơn nhánh aging nhiều**: `[abstract]` [NeoTImmuML](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1681396/full) (2025, *Front Immunol*) · [TransNRank](https://arxiv.org/pdf/2608.01924) (2026, Transformer cho xếp hạng neoantigen) · cùng toàn bộ dòng NetMHCpan/NetMHCIIpan. Thêm nữa, bài [*Immunity* 2023](https://www.cell.com/immunity/fulltext/S1074-7613(23)00406-5) đã làm sẵn phần **harmonize dữ liệu và so sánh phương pháp ML** — tức phần "dọn dẹp giao thức đánh giá" mà sinh viên định dùng làm đóng góp ở RTK–ATP thì **ở nhánh này đã có người làm rồi**.

### Dữ liệu — mặt mạnh nhất của hướng B

| Nguồn | Nội dung | Truy cập |
|---|---|---|
| **NEPdb** | hơn **17.000** neoepitope người đã xác nhận sinh miễn dịch / không sinh miễn dịch, kèm HLA và thông tin tế bào T | [nep.whu.edu.cn](https://nep.whu.edu.cn/) |
| **TumorAgDB2.0** | **187.223** bản ghi, có dữ liệu tới 5/2025 | `[abstract]` |
| dbPepNeo · Neodb · ITSNdb | neoantigen có xác nhận thực nghiệm; ITSNdb dành riêng cho **đánh giá công bằng các bộ dự đoán** | `[abstract]` |
| **TESLA** | benchmark mở | **Synapse syn21048999** |
| Bảng đặc trưng + nhãn sinh miễn dịch | tải được | **Figshare**, mã nguồn [NeoRanking trên GitHub](https://github.com/bassanilab/NeoRanking.git) |
| HiTIDE (dữ liệu thô) | fastq bệnh nhân 1–11 | **EGA EGAS00001007101 — kiểm soát truy cập, không mở** |

Nguồn: `[abstract]` [Immunity 2023](https://www.cell.com/immunity/fulltext/S1074-7613(23)00406-5).

**Đây là điểm thắng rõ của hướng B:** có **tập test độc lập đã được cộng đồng chấp nhận** (NCI-test, TESLA, HiTIDE), tức R1 được giải quyết sẵn — khác hẳn tình trạng dữ liệu DeepSIRT không truy cập được.

## 5. Bảng so sánh

Đánh giá của sinh viên, dựa trên khảo sát bước đầu ở trên. Chưa trao đổi với GVHD.

| | **A1. Sirtuin** | **A2. Senescence** | **B. Neoantigen** |
|---|---|---|---|
| **T1 Tính mới** | **Thấp** — GVHD vừa công bố SirtSAGE 2026 | **Trung bình–cao** — SenSeqNet mới, nhưng nghi vấn giao thức đánh giá là khoảng trống mở | **Thấp–trung bình** — rất đông, đã có bài harmonize dữ liệu |
| **T2 Cải tiến phương pháp** | Khó vượt GATv2 + pLDDT | Có đường: thay LSTM–CNN, hoặc thêm cấu trúc | Khó — NeoGen-BC đã rất nhiều tầng |
| **T3 Phương pháp mới** | GVHD đã đi trước (graph + cấu trúc) | Có chỗ đi: graph, cấu trúc, hoặc tiếp cận khác | Có, nhưng phải cạnh tranh với Transformer 2026 |
| **T4 XAI** | Có đường, GVHD có tiền lệ SHAP | **Rất phù hợp** — giải thích vì sao một protein bị xem là liên quan lão hóa | Có đường, nhưng đã đông |
| **T5 Web app** | Được | Được, dễ hình dung người dùng | Được, nhưng pipeline nặng, khó gói gọn |
| **R1 Dữ liệu + test độc lập** | **Rủi ro cao** — trang DeepSIRT không truy cập được `[curl]` | **Tốt** — mã nguồn và benchmark trên GitHub | **Tốt nhất** — NCI-test, TESLA, HiTIDE, NEPdb |
| **R2 Khớp GVHD** | **Cao nhất** — nhánh của chính thầy | **Trung bình–cao** — cùng chủ đề lão hóa, cùng họ ESM-2 | **Thấp** — không có công trình nào của GVHD |
| **R3 Khả thi 8–9 tuần** | Trung bình (nếu có dữ liệu) | **Tốt** — mức protein, dữ liệu sẵn, baseline rõ | **Thấp** — pipeline nhiều tầng |

## 6. Nhận định bước đầu

**Nhánh A2 (cellular senescence) là nhánh đáng đào sâu nhất ở bước tiếp theo.** Lý do: dung hòa được hai mặt mà A1 và B mỗi bên chỉ có một — vẫn nằm trong chủ đề lão hóa mà GVHD gợi ý và quen (R2), đồng thời có dữ liệu công khai kèm mã nguồn (R1, R3); lại có **một khoảng trống cụ thể, kiểm được trong 1–2 ngày**, đúng loại kinh nghiệm sinh viên vừa tích lũy ở RTK–ATP.

Nhưng phải nói rõ ba điều:

1. **Khoảng trống của A2 còn là giả thuyết.** Nếu kiểm ra tập SenSeqNet không rò rỉ, lý do chính để chọn A2 biến mất và phải xét lại cả ba nhánh.
2. **Rủi ro lặp lại sai lầm cũ:** đóng góp dạng "chỉ ra giao thức đánh giá của bài trước có vấn đề" **chính là trục đã làm RTK–ATP yếu** ở tiêu chí T1–T3. Nếu chọn A2 thì không được dừng ở việc kiểm toán; phải có mô hình và đóng góp phương pháp đi kèm.
3. **A1 vẫn là nhánh khớp GVHD nhất.** Nếu thầy có dữ liệu SirtSAGE và có bài toán con muốn giao, A1 lập tức mạnh lên — đây là lý do phải hỏi thầy trước khi tự quyết.

## 7. Việc tiếp theo, theo thứ tự

1. **Tải tập benchmark SenSeqNet trên GitHub, kiểm nghi vấn rò rỉ** — đếm số protein gốc không trùng so với 238.634 trình tự, chạy CD-HIT/MMseqs2 giữa train và test ở 30%/40%. Đây là việc rẻ nhất mà quyết định nhiều nhất.
2. **Hỏi GVHD** bốn câu đã ghi ở [mục 7 biên bản](../../../meeting/session-01-minutes.md), thêm hai câu từ tài liệu này: thầy có dữ liệu/bài toán con nào của nhánh sirtuin muốn giao không, và thầy nghĩ gì về nhánh senescence.
3. Tìm toàn văn **SirtSAGE** để biết chính xác bài toán, dữ liệu và phần "future work" — trang xuất bản trả 403, cần thử qua thư viện trường hoặc xin thầy bản PDF.
4. Nếu A2 đứng vững: dựng **history research theo ba bước** cho nhánh senescence, nhóm theo phương pháp (đặc trưng thủ công → PSSM + CNN → PLM + CNN/LSTM → graph/cấu trúc).
5. Xác định **ứng dụng/website** cho nhánh được chọn: người dùng là ai, nhập gì, nhận gì.

## 8. Điều tài liệu này **chưa** làm

- **Chưa tải bất kỳ tập dữ liệu nào**, nên mọi nhận xét về dữ liệu đều từ mô tả của bài báo, trừ chỗ ghi `[curl]`.
- **Chưa đọc toàn văn** SirtSAGE, DeepSIRT, SenSeqNet, NeoTImmuML, TransNRank. Chỉ NeoGen-BC là đọc từ PDF trong repo.
- **Chưa kiểm** nghi vấn rò rỉ của SenSeqNet — đây là giả thuyết, không phải phát hiện.
- **Chưa khảo sát** các nhánh aging khác ngoài sirtuin và senescence (ví dụ aging clock, SASP, telomere), và chưa khảo sát nhánh cancer nào ngoài neoantigen.
- **Chưa có ý kiến GVHD** về bất kỳ nội dung nào ở đây.
