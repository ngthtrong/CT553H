# Khảo sát thêm đề tài tin sinh học — hướng tiếp cận khác với dự đoán residue/peptide

> Ngày: **12/10/2026 (chiều muộn)**. Yêu cầu của sinh viên: tiếp tục nghiên cứu lĩnh vực tin sinh học nhưng theo **hướng tiếp cận khác** với các ứng viên đã xét trong repo (RTK-ATP, degron, dark kinome/DARKIN, sirtuin — đều là dự đoán nhãn ở mức residue/peptide bằng mCNN/PLM). Vị trí RCA ở thời điểm khảo sát thuộc [D-016](../DECISIONS.md#d-016); trạng thái hiện hành xem [DECISIONS.md](../DECISIONS.md#d-021). Mục tiêu: liệt kê **càng nhiều ứng viên càng tốt**, mỗi ứng viên có mô tả bài toán + đóng góp sơ bộ + khảo sát sơ bộ dữ liệu, ưu tiên đóng góp/ý nghĩa hơn là đã có hồ sơ đầy đủ.
>
> **Phương pháp:** 18 lượt `WebSearch` (không phải đọc toàn văn) trên nhiều nhánh tin sinh học khác nhau, đối chiếu với [danh mục GVHD](<../project/advisor-publications/ho-quang-thai.md>) (14 công trình, chủ yếu mCNN/PLM/PSSM cho protein màng-vận chuyển và DNA điều hòa, cộng SirtSAGE 2026 dùng graph attention, RAG-msCNN 2026 dùng RAG). **Mọi trích dẫn dưới đây lấy qua tóm tắt công cụ tìm kiếm, CHƯA đọc toàn văn, CHƯA tự tải dữ liệu** — nhãn **[CHƯA KIỂM]** áp cho toàn bộ tài liệu này, khác với các đề tài đã có audit thật (degron, RTK-ATP, RCA). Đây là bước sàng lọc diện rộng, không phải quyết định.

## Cách đọc bảng

Mỗi ứng viên có: bài toán một câu, đóng góp sơ bộ (giả thuyết, chưa kiểm chứng), khoảng trống/đối thủ gần nhất đã tìm thấy, ghi chú dữ liệu, và mức khớp với hướng nghiên cứu GVHD. Xếp theo ba bậc:

- **Bậc A — khoảng trống cụ thể, mới (2025-2026), chưa có công cụ/benchmark đóng hoàn toàn.**
- **Bậc B — có cơ sở nhưng lĩnh vực đã khá đông đúc; cần góc riêng biệt rõ ràng để không trùng tiền lệ.**
- **Bậc C — lĩnh vực đã bị một benchmark toàn diện gần đây giải quyết hoặc đòi hỏi tài nguyên tính toán lớn (GPU mạnh, dữ liệu cấu trúc khổng lồ) — liệt kê để biết đã loại, không khuyến khích chọn.**

---

## Bậc A — khoảng trống mạnh nhất

### A1. Công cụ audit rò rỉ dữ liệu cho nghiên cứu học máy trên dữ liệu vi sinh (microbiome)

**Bài toán:** một review 2024 ước lượng **tới 88% nghiên cứu học máy trên dữ liệu microbiome có thể chứa rò rỉ** (bỏ sót tách tập/rò rỉ qua lặp mẫu, batch, hoặc tính chất compositional của dữ liệu), và khẳng định **chưa có pipeline chuẩn hóa nào để benchmark ML/DL trong lĩnh vực này** — [arXiv 2402.17621](https://arxiv.org/pdf/2402.17621), [arXiv 2411.01098](https://arxiv.org/pdf/2411.01098). Hiệu ứng batch khiến mô hình chẩn đoán (ví dụ ung thư đại trực tràng từ hệ vi sinh ruột) khó tái lập giữa các nghiên cứu.

**Đóng góp sơ bộ:** xây một **công cụ tự động quét rò rỉ** (phát hiện trùng mẫu/subject qua tập train-test, rò rỉ do chuẩn hóa compositional trước khi chia tập, rò rỉ do hiệu ứng batch tương quan với nhãn) và áp lại lên vài bộ dữ liệu phân loại bệnh từ microbiome đã công bố rộng rãi, báo cáo mức độ điểm số bị thổi phồng. Đây đúng dạng "công cụ kiểm soát rò rỉ cho benchmark đang dùng rộng nhưng thiếu công cụ kiểm tra" — tầng công cụ/quy trình, không phải một mô hình dự đoán mới.

**Dữ liệu [CHƯA KIỂM]:** nhiều bộ dữ liệu microbiome-bệnh công khai (ví dụ các cohort ung thư đại trực tràng dùng trong bài benchmark batch-effect tìm được), curatedMetagenomicData (R/Bioconductor, tổng hợp nhiều cohort). Cần tự kiểm quyền truy cập và định dạng.

**Khớp GVHD:** yếu — advisor không có công trình microbiome. Mạnh ở tiêu chí 5 (công cụ) và ý nghĩa thực tiễn (một con số 88% rất mạnh để mở đầu).

---

> **Đi sâu A2/A3/A4 (12/10/2026, sau yêu cầu làm rõ bài toán/I-O/đóng góp):** xem [bio-tool-candidates-deep-dive-a2-a3-a4.md](README.md). **A3 phải thu hẹp đáng kể** — tìm được tiền lệ trực tiếp (Denger & Helms, *Molecules* 2025, đã kết hợp cấu trúc AlphaFold + trình tự cho đúng protein vận chuyển). A4 vẫn là khoảng trống rõ nhất.

### A2. Benchmark độ trung thực (fidelity) cho các phương pháp XAI trên mô hình điều hòa gen/protein

**Bài toán:** một bài position paper ICML 2026 (Zhou, Huang, Li — Đại học Exeter) báo rằng nghiên cứu diễn giải mô hình gen **dựa quá nhiều vào đánh giá giai thoại, một phương pháp duy nhất**; trên benchmark gắn kết yếu tố phiên mã (transcription factor binding), các phương pháp XAI khác nhau **cho giải thích mâu thuẫn nhau trên cùng một dự đoán, không định vị được motif điều hòa đã biết, và không phản ánh trung thực quá trình quyết định nội tại của mô hình** — [ICML 2026 poster](https://icml.cc/virtual/2026/poster/67163). Đây là **bài báo quan điểm, đề xuất khung đánh giá, chưa phải một benchmark đã triển khai đầy đủ cho protein**.

**Đóng góp sơ bộ:** triển khai thật một **bộ công cụ đánh giá độ trung thực XAI** (so khớp attribution của SHAP/Integrated Gradients/attention với motif/vị trí gắn **đã biết từ thực nghiệm độc lập**, ví dụ JASPAR motif cho DNA hoặc vị trí gắn ATP đã xác định cấu trúc cho protein màng) và áp lên một họ mô hình mCNN/PLM cụ thể — kiểm tra liệu các giải thích hiện có (kể cả SHAP đã dùng trong BERT-Promoter của GVHD) có thực sự định vị đúng motif/vị trí hay không. Nối trực tiếp với tiêu chí 4 (XAI) và tiền lệ chính GVHD đã dùng (SHAP), nhưng đổi vai trò: không dùng SHAP để diễn giải một mô hình mới, mà **kiểm định SHAP/XAI có đáng tin không** trên lớp mô hình GVHD hay dùng.

**Dữ liệu [CHƯA KIỂM]:** JASPAR (motif DNA, công khai), cấu trúc/vị trí gắn ATP đã biết (PDB, UniProt — tương tự nguồn đã dùng ở `rtk-atp-applicability` cũ). Không cần nhãn mới, dùng lại ground truth đã có trong các đề tài trước.

**Khớp GVHD:** **mạnh** — kiểm định trực tiếp công cụ XAI mà một công trình GVHD (BERT-Promoter) đã dùng, và áp dụng cho đúng họ protein màng/vận chuyển GVHD chuyên sâu.

---

### A3. Benchmark kết hợp cấu trúc (AlphaFold) + trình tự (PLM) cho dự đoán chức năng protein màng, có kiểm soát rò rỉ

**Bài toán:** một bioRxiv 2024 chỉ ra nhiều nghiên cứu dự đoán chức năng dựa trên cấu trúc **không chọn protein kiểm tra đủ nghiêm ngặt để tránh trùng với dữ liệu huấn luyện AlphaFold2**, gây rò rỉ — [bioRxiv 2024.08.02.606297](https://www.biorxiv.org/content/10.1101/2024.08.02.606297.full.pdf). Một công trình 2025 cho thấy **thêm cấu trúc dự đoán bởi AlphaFold vào huấn luyện cải thiện dự đoán chức năng ở cả ba nhóm Gene Ontology**, nhưng không nói rõ phạm vi kiểm soát rò rỉ.

**Đóng góp sơ bộ:** toàn bộ 14 công trình của GVHD đều dùng **trình tự thuần** (PSSM/PLM), **không công trình nào dùng đặc trưng cấu trúc AlphaFold**. Xây benchmark **có kiểm soát rò rỉ nghiêm ngặt theo thời gian công bố cấu trúc** (loại protein có cấu trúc thật nằm trong tập huấn luyện AlphaFold2/3), so sánh trực tiếp mCNN+PLM thuần trình tự (như GVHD đã làm) với mCNN+PLM+đặc trưng cấu trúc (bề mặt tiếp xúc, pocket cấu trúc) trên **đúng bài toán GVHD đã làm** (ATP-binding site, efflux protein, ion transporter) để đo phần cải thiện thật do cấu trúc mang lại, không phải do rò rỉ.

**Dữ liệu [CHƯA KIỂM]:** AlphaFold Protein Structure DB (công khai, hàng trăm nghìn cấu trúc), các bộ nhãn ATP-binding/efflux/ion-transporter đã dùng trong công trình GVHD (có thể cần liên hệ tác giả hoặc dùng lại bộ RTK-ATP đã tải ở đề tài cũ).

**Khớp GVHD:** **mạnh nhất trong bậc A** — cùng bài toán, cùng họ protein, chỉ đổi trục đặc trưng (cấu trúc thay/cộng trình tự) và thêm kỷ luật chống rò rỉ mà 14 công trình GVHD chưa báo cáo rõ.

---

### A4. Công cụ audit độ tin cậy/calibration cho các bộ dự đoán mCNN+PLM

**Bài toán:** một bài Nature Methods 04/2026 (Prabakaran & Bromberg) đo độ tin cậy embedding PLM bằng tỷ lệ hàng xóm gần là trình tự tổng hợp/ngẫu nhiên; một bài PLOS Comp Biol 01/2025 benchmark các phương pháp định lượng độ không chắc chắn trên dữ liệu trình tự-chức năng protein (bộ FLIP) — [bioRxiv 2025.04.30.651545](https://www.biorxiv.org/content/10.1101/2025.04.30.651545.full.pdf), [PLOS Comp Biol qua tóm tắt]. **Chưa có benchmark calibration dành riêng, áp trên nhiều mô hình/nhiều tác vụ** theo đúng combo PLM+mCNN.

**Đóng góp sơ bộ:** áp hai kỹ thuật trên (đo độ tin cậy embedding + đo calibration dự đoán) lên chính lớp mô hình mCNN+PLM mà GVHD dùng cho nhiều bài toán (ATP-binding, efflux, FAD-binding) — kiểm tra điểm tin cậy cao có tương ứng với dự đoán đúng không, và liệu các mô hình này có "tự tin quá mức" ở vùng ngoài phân phối (protein xa family đã huấn luyện) hay không. Đây là một **lớp kiểm định bổ sung** gắn thêm giá trị thực tiễn (cảnh báo miền áp dụng) cho chính hướng nghiên cứu GVHD — gần giống ý tưởng "cảnh báo miền áp dụng" đã có trong đề tài RTK-ATP cũ, nhưng tổng quát hóa thành công cụ dùng lại được cho nhiều mô hình, không chỉ một bài toán.

**Dữ liệu [CHƯA KIỂM]:** cần mô hình/trọng số GVHD đã công bố (nếu có mã nguồn/trọng số mở) hoặc tự huấn luyện lại baseline tương đương trên dữ liệu công khai cùng loại.

**Khớp GVHD:** mạnh — trực tiếp kiểm định phương pháp luận GVHD đang dùng, hướng "đóng góp bằng cách làm cho phương pháp đã có đáng tin cậy hơn" khớp tiêu chí 2-3 (cải tiến) mà không cần phát minh kiến trúc mới.

---

## Bậc B — có cơ sở, cần góc riêng để tránh trùng

### B1. Benchmark độc lập, có kiểm soát rò rỉ, cho dự đoán off-target của guide RNA CRISPR

Một bài báo cũ (2016) đã ghi nhận "chưa đánh giá hệ thống, toàn diện và khách quan"; một preprint 02/2026 (Guide-Guard) báo 84% độ chính xác nhưng là một preprint đơn lẻ, không có benchmark độc lập đối chiếu. **Đóng góp:** xây benchmark độc lập dùng dữ liệu GUIDE-seq/CIRCLE-seq (đo off-target thật bằng thực nghiệm, không phải điểm dự đoán) để so sánh công khai nhiều công cụ hiện có, có kiểm soát rò rỉ theo họ gene/vị trí. **Dữ liệu [CHƯA KIỂM]:** các bộ GUIDE-seq/CIRCLE-seq công khai (NCBI/SRA). **Khớp GVHD:** yếu (DNA nhưng không phải protein màng).

### B2. Synthetic lethality theo ngữ cảnh ung thư cụ thể, có chữ ký đột biến làm đặc trưng phân tầng

Benchmark Nature Communications 2024 đã so 12 phương pháp, nhưng tự nhận còn yếu ở **cold-start** và **tính đặc hiệu theo ngữ cảnh (context-specific SL)**; chưa ai dùng chữ ký đột biến (mutational signature) làm đặc trưng phân tầng theo ngữ cảnh ung thư, theo khảo sát hôm nay. **Đóng góp:** benchmark cold-start + tích hợp chữ ký đột biến làm đặc trưng ngữ cảnh. **Dữ liệu [CHƯA KIỂM]:** TCGA, DepMap (công khai, cần đăng ký). **Khớp GVHD:** yếu — không phải hướng nghiên cứu của thầy, nhưng ung thư là một trong hai hướng thầy có gợi ý ban đầu (aging/cancer).

### B3. Benchmark thống nhất, chuẩn hóa cho dự đoán tương tác thuốc–đích (DTI) theo kịch bản cold-start

Một bài tổng quan 07/2026 kêu gọi "xây dựng tập dữ liệu chuẩn hóa và đánh giá thực tế" vì các mô hình mạnh trên benchmark quen thuộc tụt hiệu năng trên hợp chất/protein mới — lời kêu gọi này **chưa có ai đáp ứng** theo khảo sát hôm nay. **Đóng góp:** xây benchmark thống nhất đó. **Dữ liệu [CHƯA KIỂM]:** BindingDB, DrugBank, ChEMBL (đã có MCP server `chembl` sẵn trong phiên này để tra cứu nhanh). **Khớp GVHD:** yếu-trung bình.

### B4. Benchmark biến thể splicing vùng intron sâu, có kiểm soát rò rỉ, trên dữ liệu MPRA

Một benchmark 2023 ghi nhận deep-intronic region vẫn thiếu benchmark độc lập; chưa tìm thấy công trình 2025-2026 xử lý trực tiếp. **Đóng góp:** benchmark độc lập cho vùng intron sâu dùng MFASS hoặc MPRA tương tự, kiểm tra rò rỉ giữa dữ liệu huấn luyện SpliceAI/Pangolin (dựa trên annotation gene model) và tập test lâm sàng. **Dữ liệu [CHƯA KIỂM]:** MFASS (công khai, ~27.000 biến thể). **Khớp GVHD:** yếu (DNA nhưng không cùng loại bài toán).

### B5. Lớp định lượng độ không chắc chắn + kiểm định giá trị lâm sàng cho đồng hồ lão hóa biểu sinh (epigenetic clock)

ComputAgeBench (KDD 2025) và TranslAGE (10/2025) đã benchmark khá toàn diện 13+ đồng hồ; một review 12/2025 phê bình các đồng hồ "thường bỏ qua độ không chắc chắn dự đoán". **Đóng góp:** thêm lớp calibration + so với risk score lâm sàng chuẩn, như review 12/2025 yêu cầu — đây là khoảng trống được **chính một bài báo phê bình gọi tên**, chưa ai làm. **Dữ liệu [CHƯA KIỂM]:** các bộ methylation công khai mà ComputAgeBench đã hài hòa hóa (GEO). **Khớp GVHD:** **trung bình-mạnh** — nối trực tiếp với hướng aging/sirtuin mà GVHD gợi ý và đã có công trình mới nhất (SirtSAGE).

### B6. Active learning + định lượng độ không chắc chắn cho một họ protein màng cụ thể của GVHD

ProSpero (NeurIPS 2025) đã có khung active learning chung cho protein engineering (8 bài toán, oracle TAPE/FLEXS), nhưng chưa áp cho đúng họ ion transporter/efflux protein mà GVHD chuyên sâu. **Đóng góp:** áp/mở rộng khung active learning + oracle in-silico cho bài toán gần với MFPS_CNN/mCNN-GenEfflux, đo số lượng mẫu thực nghiệm (giả lập) cần thiết để đạt độ chính xác mục tiêu — hướng "thiết kế thí nghiệm hiệu quả" khác hẳn lối "dự đoán nhãn tĩnh" đã làm nhiều lần. **Dữ liệu [CHƯA KIỂM]:** cần oracle in-silico (mô hình đã huấn luyện đóng vai "phòng thí nghiệm giả") — khả thi tính toán nhưng cần thiết kế cẩn thận để không tự tạo nhãn vòng tròn. **Khớp GVHD:** trung bình-mạnh về đối tượng protein, nhưng khác hẳn về bài toán (thiết kế thí nghiệm, không phải phân loại).

---

## Bậc C — đã có benchmark toàn diện gần đây hoặc đòi hỏi tài nguyên lớn — không khuyến khích

| Hướng                                                                              | Vì sao yếu đi                                                                                                                                                                                                                                                                                 | Nguồn                                                                                                                                  |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Benchmark tích hợp đa-omics tổng quát                                           | SCMBench đã so 23 phương pháp/mô hình nền; hơn 40 công cụ đã có, nhiều benchmark 2024-2025 đã phủ nhiều khía cạnh                                                                                                                                                           | [SCMBench](https://irep.mbzuai.ac.ae/items/f63f86b6-fcf2-49b2-99a8-9bcf2e944c1f)                                                         |
| Benchmark rò rỉ dữ liệu PPI ở mức đồ thị                                    | PRING (NeurIPS 2025 Datasets & Benchmarks) đã giải đúng bài toán này: 21.484 protein, 186.818 tương tác, đa loài, có kiểm soát rò rỉ                                                                                                                                           | [PRING](https://papers.nips.cc/paper_files/paper/2025/hash/86a4ea51ccac6c830230f281a23e74c8-Abstract-Datasets_and_Benchmarks_Track.html) |
| Dự đoán độ gắn kết antibody-antigen                                           | AbBiBench, AbRank, Ab-VS-Bench đều 2025, rất đông đúc; không khớp GVHD                                                                                                                                                                                                                  | [AbRank](https://arxiv.org/html/2506.17857v2)                                                                                            |
| Benchmark mô hình nền gen (genomic foundation models)                             | OmniGenBench đã phủ 75 bộ dữ liệu, 30+ mô hình, nhiều bộ chỉ số                                                                                                                                                                                                                      | [OmniGenBench](https://arxiv.org/pdf/2410.01784)                                                                                         |
| Đánh giá protein sinh tạo (generative design)                                    | ProteinBench, Protein-SE(3), PDFBench, Genie 2 đã phủ dày; cần GPU mạnh cho mô hình diffusion/flow-matching                                                                                                                                                                              | [ProteinBench](https://arxiv.org/html/2409.06744v2)                                                                                      |
| Benchmark giải chập loại tế bào không gian (spatial deconvolution) tổng quát | Spotless (eLife 2024), SpatialCTD, và một preprint 01/2026 đã benchmark kỹ, chỉ còn khoảng trống hẹp (quần thể hiếm, mô người u miễn dịch)                                                                                                                                     | [Spotless](https://elifesciences.org/articles/88431)                                                                                     |
| RAG cho dự đoán chức năng protein                                               | Rất hot (ProtQueSt ICML 2026, PoET-2, ProtEx, RAFM đa phương thức) — đông đúc, nhưng**lưu ý: đây chính là hướng GVHD mới công bố (RAG-msCNN 2026)**, nên nếu chọn phải tìm một bài toán con GVHD chưa làm, không lặp lại chính công trình của thầy | [ProtQueSt](https://icml.cc/virtual/2026/70706)                                                                                          |
| Dự đoán đáp ứng thuốc (drug response) tổng quát                             | Đã có framework benchmark 5 bộ dữ liệu, 7 mô hình chuẩn hóa; DL không rõ hơn ML cổ điển                                                                                                                                                                                          | [PMC12794626](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12794626/)                                                                    |

---

## Nhận định tổng hợp

- **Mẫu hình chung của Bậc A:** cả bốn ứng viên mạnh nhất đều là **công cụ kiểm định/benchmark tầng quy trình** (audit rò rỉ, audit XAI, audit calibration, benchmark chống rò rỉ cấu trúc-trình tự) — đúng hướng 3 mà CLAUDE.md đã đặt làm ưu tiên khi không muốn tiếp tục dự đoán residue/peptide đơn lẻ. Khác với các lần khảo sát công cụ bio trước (DataSAIL, MaveDB, OpDEA — đều đã "chín"), bốn hướng này nhắm **đúng vào phương pháp luận GVHD đang dùng** (mCNN+PLM, SHAP, trình tự thuần) nên vừa mới, vừa dễ bán với thầy.
- **A2, A3, A4 có một đặc điểm hiếm:** đối tượng kiểm định **chính là công trình/phương pháp của GVHD**, nên tự động giải quyết rủi ro "ngoài chuyên môn thầy" mà `budgeted-microservice-rca` và `legal-qa-grounding` đang mắc phải.
- **Tất cả bậc A/B đều chưa qua cổng G1/G2 thật** — đây là kết quả của một lượt sàng lọc rộng bằng tóm tắt tìm kiếm, **chưa đọc toàn văn bất kỳ nguồn nào, chưa tự tải một byte dữ liệu nào**. Trước khi chọn một hướng để đi sâu, bắt buộc: đọc toàn văn nguồn khoảng trống chính, tự tải mẫu dữ liệu, và kiểm tra lại claim "chưa ai làm" — đúng quy trình đã áp cho mọi đề tài khác trong repo.

## Việc tiếp theo (nếu sinh viên chọn một hướng ở trên)

1. Đọc toàn văn nguồn khoảng trống chính của hướng được chọn (không chỉ tóm tắt).
2. Tự tải mẫu dữ liệu, kiểm giấy phép, ước lượng quy mô thật.
3. Áp lại ba cổng G1/G2/G3 với bằng chứng tự đo, theo đúng khung đã dùng cho `budgeted-microservice-rca` và `legal-qa-grounding`.
4. Nếu chọn A2/A3/A4 (kiểm định phương pháp GVHD): cân nhắc liên hệ hỏi GVHD sớm hơn tuần 6, vì hướng này có thể cần quyền truy cập mã nguồn/trọng số công trình thầy.
