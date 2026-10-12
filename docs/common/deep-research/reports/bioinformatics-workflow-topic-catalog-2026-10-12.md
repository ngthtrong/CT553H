# 50 đề tài tin sinh học từ bài toán của quy trình nghiên cứu

Ngày khảo sát: **12/10/2026**. Phạm vi: tìm kiếm diện rộng, phân tích bài toán, ý nghĩa và đóng góp sơ bộ; dữ liệu được khảo sát ở mức nguồn/tài liệu. **Chưa chọn đề tài mới, chưa thực nghiệm.** `budgeted-microservice-rca` vẫn có trạng thái ghi trong [quyết định hiện hành](../../../topics/budgeted-microservice-rca/01-idea/topic-decision.md).

Bản này bổ sung [khảo sát 14 ứng viên](bioinformatics-tool-layer-candidates-2026-10-12.md) và [khảo sát mở lĩnh vực](open-field-topic-selection-2026-10-12.md). Các đề tài là **50 hướng bài toán riêng**, không phải 50 đóng góp mới đã được chứng minh. Một hướng chỉ trở thành đề tài luận văn sau khi thu hẹp, đối chiếu phương pháp gần nhất và đóng các cổng đánh giá. Không tạo 50 thư mục đề tài trước khi cần hồ sơ riêng.

## 1. Cách đọc và căn cứ đánh giá

Ưu tiên yêu cầu mới: **vấn đề có ý nghĩa → người dùng/quy trình → phần cải tiến → phép đo → ứng dụng**. Có thể dùng ML, tối ưu hóa, thống kê hoặc quy tắc; không bắt buộc xây thêm một bộ dự đoán residue/peptide. Tham khảo [chuyên môn GVHD](../../advisor/README.md), [năm tiêu chí](../../../meeting/session-01-minutes.md) và [G1/G2/G3](main-topic-decision.md).

Mọi đoạn **“đóng góp”** dưới đây mang nghĩa **[ĐỀ XUẤT]**. Sự tồn tại và chức năng của tiền lệ có nguồn sơ cấp; phần chưa được tiền lệ giải quyết là **giả thuyết khoảng trống**, chưa phải kết luận “chưa ai làm”. Không suy ra một lĩnh vực hết vấn đề chỉ vì đã có benchmark lớn.

| Ký hiệu | Cách hiểu |
|---|---|
| **P** | Ưu tiên kiểm tra sâu sớm: bài toán, sản phẩm và phép đánh giá tương đối rõ; không phải đã qua G1/G2/G3 |
| **M** | Có triển vọng, phụ thuộc thêm nhãn, chuyên gia hoặc góc cải tiến cụ thể |
| **H** | Ý nghĩa tốt nhưng phạm vi/kiến thức/tính toán nặng; cần thu hẹp mạnh |
| **D** ở nguồn | Đã mở trang nguồn và đọc phần nội dung được công cụ trích xuất; không mặc định đã đọc toàn bộ bài và phụ lục |
| **S** ở nguồn | Chỉ kiểm qua kết quả tìm kiếm từ trang nguồn sơ cấp |
| **A** ở nguồn | Đã đọc abstract và metadata bài báo; chưa đọc toàn văn |

**Độ sâu dữ liệu chung:** đã tìm và đối chiếu tài liệu kho dữ liệu, định dạng hoặc benchmark; chưa tải/audit dữ liệu thô của các hướng mới, chưa xác nhận số mẫu dùng được, giấy phép từng bộ, RAM hay baseline chạy thành công. Không trình bày số lượng toàn kho như số nhãn phù hợp cho một đề tài.

### Áp ba cổng cho đề tài công cụ

- **G1:** có chuẩn kiểm độc lập với đầu ra công cụ: spike-in thực nghiệm, assay, chú giải được rà soát độc lập, gold standard ánh xạ hoặc kết quả tham chiếu đã khóa. Với công cụ kỹ thuật, lỗi được chèn có kiểm soát giúp kiểm tra chức năng; **không thay thế** đánh giá trên lỗi/dữ liệu thực và không tự chứng minh giá trị sinh học. Đây là cách vận dụng G1 cho bài toán công cụ, cần GVHD xác nhận khi chốt.
- **G2:** phải có một cải tiến dương đo được: giảm lỗi quyết định, giảm dương tính giả ở cùng mức phát hiện, giữ kết luận đúng với ít tài nguyên hơn, hoặc giảm công rà soát với chất lượng được giữ. Một báo cáo “các mô hình hiện tại kém” chưa đáp ứng yêu cầu này. Tất cả 50 hướng **chưa có kết quả G2**.
- **G3:** mỗi hướng có một thao tác nghiên cứu làm trung tâm ứng dụng. Phạm vi đầu tiên: một miền, vài định dạng, vài baseline; chưa chứng minh thời gian hoàn thành của bất kỳ MVP nào.

**Năm tiêu chí GVHD:** tính mới nằm ở khác biệt sau đối chiếu; cải tiến phương pháp nằm ở cơ chế đề xuất; phương pháp mới phải phục vụ bài toán; XAI chỉ áp khi có mô hình và cần kiểm độ trung thực. Với thuật toán/quy tắc, truy nguyên và giải thích quyết định có ích nhưng **không tự động tương đương XAI**. Tất cả hướng có sản phẩm phần mềm; mức chấp nhận học thuật của các đề tài thiên thống kê/kỹ thuật vẫn cần trao đổi với GVHD.

## 2. Bản đồ 50 hướng

| Nhóm | Mã | Công việc nghiên cứu cần hỗ trợ |
|---|---|---|
| A. Dữ liệu và khả năng tái sử dụng | 01–05 | Tìm đúng dữ liệu, chuẩn hóa thực thể, ghép đúng mẫu và biết tác động cập nhật |
| B. Thiết kế và độ hợp lệ phân tích | 06–10 | Tránh đánh giá sai, chọn cách phân tích bền và kết hợp nghiên cứu |
| C. Gene, pathway và chuyển ngữ cảnh | 11–15 | Diễn giải danh sách gene mà không bỏ qua nền, ánh xạ hoặc isoform |
| D. Đơn bào và dữ liệu không gian | 16–20 | Gán nhãn có rà soát, giữ tín hiệu sinh học và đánh giá theo người cho mẫu |
| E. Proteomics và bằng chứng protein | 21–25 | Kiểm soát dữ liệu thiếu, peptide dùng chung, PTM và assay khác nhau |
| F. Vi sinh và metagenomics | 26–30 | Hiểu bất đồng AMR, nhiễm bẩn, thay đổi database và chất lượng genome |
| G. Perturbation, ảnh và thiết kế thí nghiệm | 31–35 | Chọn hit/thí nghiệm và phân bổ công gán nhãn một cách hiệu quả |
| H. Kỹ nghệ phần mềm cho tin sinh | 36–40 | Phát hiện lỗi ngữ nghĩa, kiểm thay đổi, chọn workflow và tái lập |
| I. Genome, khám phá chức năng và chuyển hóa | 41–45 | Đánh giá biến thể, transcript mới, plasmid, cụm gene và mô hình chuyển hóa |
| J. Tổng hợp bằng chứng và nghiên cứu nhiều điều kiện | 46–50 | Chọn module, kiểm biomarker, truy hồi perturbation, chuẩn hóa GWAS và lấy mẫu theo thời gian |

## 3. Danh mục chi tiết

### A. Dữ liệu và khả năng tái sử dụng

#### BIO-01 — Sàng lọc bộ dữ liệu theo khả năng trả lời câu hỏi nghiên cứu — P

**Bài toán/ý nghĩa:** người nghiên cứu tìm được dataset cùng bệnh nhưng thiếu đối chứng, thiếu số người độc lập, sai mô hoặc không có thiết kế phù hợp. Cần chọn **dữ liệu phân tích được**, không chỉ dữ liệu có từ khóa giống nhau.

**Đóng góp:** bộ suy luận điều kiện chọn/loại từ metadata và thiết kế, kèm đường chứng cứ, trạng thái chưa biết và thứ tự câu hỏi cần rà soát. Đánh giá khả năng giảm chọn nhầm dataset và công sàng lọc.

**Dữ liệu/đối chứng/phép đo:** GEO/recount3; bộ câu hỏi và đáp án chọn/loại do người có chuyên môn rà soát độc lập, chia theo study. So tìm kiếm từ khóa và bộ lọc thủ công; precision/recall chọn bộ, lỗi loại nhầm, số thao tác. [OmicsDI][s03], [GEO2R][s05], [GREIN][s06] đã hỗ trợ tìm/phân tích; không nhận tìm dataset hay giao diện RNA-seq là mới.

**Ứng dụng/điểm chặn:** workspace sàng lọc và xuất danh sách lý do; chỉ một nhánh RNA-seq. Phụ thuộc gold standard và xác nhận nhu cầu người dùng. Đây là phiên bản câu hỏi hẹp hơn hướng “tìm GEO” từng khảo sát, không tự mở lại đề tài cũ như đã được chọn.

#### BIO-02 — Chuẩn hóa metadata với lựa chọn bản ghi cần con người kiểm tra — M

**Bài toán/ý nghĩa:** tuổi, mô, bệnh và điều kiện thí nghiệm được ghi tự do; một chuẩn hóa sai có thể làm chọn sai cohort.

**Đóng góp:** chuẩn hóa theo ontology kèm từ chối khi mơ hồ, xếp thứ tự rà soát theo tác động tới việc chọn cohort; giữ nguyên văn bản và nguồn. So với chuẩn hóa mọi trường hoặc chỉ chọn theo độ bất định.

**Dữ liệu/đánh giá:** SRA/BioSample và một bộ trường được gán nhãn độc lập; exact/concept match, lỗi ảnh hưởng chọn cohort và chất lượng theo ngân sách rà soát. [MetaSRA][s04] đã chuẩn hóa và có provenance; ontology hay provenance không phải khoảng trống tự thân.

**Ứng dụng/điểm chặn:** hàng đợi duyệt metadata; chỉ vài trường/ontology. Cần annotation; không dùng đầu ra chuẩn hóa của hệ thống làm đáp án.

#### BIO-03 — Hòa giải định danh gene/protein có giữ quan hệ một–nhiều — P

**Bài toán/ý nghĩa:** ghép bảng UniProt, Ensembl và gene symbol có thể gộp nhầm isoform, mất hàng hoặc nhân đôi dữ liệu; kết quả downstream bị đổi mà người dùng không nhận ra.

**Đóng góp:** đồ thị ánh xạ có loại thực thể, loài và phiên bản; quyết định giữ/tách/từ chối dựa trên ngữ cảnh, rồi lan truyền sự mơ hồ tới bảng kết quả. Đo giảm ghép sai ở cùng tỷ lệ ánh xạ.

**Dữ liệu/đánh giá:** bảng cross-reference và ca khó được rà soát độc lập; so first-match, [UniProt ID mapping][s08] và [g:Profiler][s09]. Đo ánh xạ sai, tỷ lệ xử lý, sai lệch enrichment sau ghép.

**Ứng dụng/điểm chặn:** nhập hai bảng, xem quan hệ và xuất bảng có cảnh báo. Giới hạn human hoặc human/mouse; không coi một dịch vụ mapping khác là thuật toán mới. Cần kiểm các baseline đã giải quyết bao nhiêu ca khó.

#### BIO-04 — Đối soát mẫu và người cho mẫu khi tích hợp đa-omics — M

**Bài toán/ý nghĩa:** RNA, protein và metadata có tên mẫu khác nhau, lặp kỹ thuật hoặc thiếu modality; ghép nhầm có thể tạo tương quan đa-omics giả.

**Đóng góp:** đối soát dưới ràng buộc subject–sample–assay, phát hiện mâu thuẫn và đề nghị tập thao tác sửa ít nhất, giữ trường hợp chưa giải được.

**Dữ liệu/đánh giá:** ví dụ và cohort công khai có sample mapping, bổ sung lỗi chèn được khóa; đối chiếu [MultiAssayExperiment][s10] và exact joins. Đo ghép sai trên ca thực, số sửa cần thiết, ảnh hưởng tương quan downstream.

**Ứng dụng/điểm chặn:** trình duyệt map mẫu và missing modalities. Cấu trúc `sampleMap` đã có; cần tạo lợi ích hơn xác thực cấu trúc. Không hứa xác nhận danh tính sinh học từ metadata đơn thuần.

#### BIO-05 — Phân tích tác động khi cập nhật annotation sinh học — M

**Bài toán/ý nghĩa:** cùng dữ liệu đầu vào nhưng phiên bản gene/ontology khác có thể đổi danh sách hoặc kết luận; nhà nghiên cứu cần biết phần nào phải chạy lại và phần nào cần xem lại.

**Đóng góp:** lan truyền thay đổi qua đồ thị phụ thuộc từ annotation tới gene set và kết luận, ưu tiên kết quả đổi ý nghĩa thay vì chỉ báo tệp đổi.

**Dữ liệu/đánh giá:** snapshot nguồn và kết quả enrichment khóa trước; so diff bảng và chạy lại toàn bộ. Đo precision/recall phát hiện kết quả bị ảnh hưởng, số phân tích tránh chạy, sai số bỏ sót. [g:Profiler][s09] là tiền lệ mapping/enrichment; [Nextflow][s35] đã có cache.

**Ứng dụng/điểm chặn:** so hai snapshot và xuất báo cáo tác động. Cần tìm được phiên bản lịch sử cùng giấy phép; khác BIO-37 ở chỗ đối tượng thay đổi là **tri thức/annotation**, không phải phiên bản phần mềm.

### B. Thiết kế và độ hợp lệ phân tích

#### BIO-06 — Chẩn đoán và hỗ trợ sửa rò rỉ dữ liệu nhiều tầng — P

**Bài toán/ý nghĩa:** split tách peptide có thể vẫn chung protein; tách sample có thể vẫn chung subject hoặc study. Cần nối rò rỉ với loại khái quát hóa đang muốn đo.

**Đóng góp:** dựng đồ thị quan hệ mẫu–protein–homology–study, chỉ ra đường phụ thuộc và tập thay đổi split ít mất dữ liệu; đánh giá lợi ích sửa thay vì chỉ cảnh báo.

**Dữ liệu/đánh giá:** vài benchmark có nhãn thực nghiệm và metadata liên quan; so [GraphPart][s02], [DataSAIL][s01], GroupKFold. Đo vi phạm còn lại, dữ liệu giữ lại, thời gian và độ phù hợp với kịch bản sử dụng đã khóa.

**Ứng dụng/điểm chặn:** nhập manifest, chọn kịch bản, duyệt split sửa. Không nhận chia theo homology hay nhiều loại thực thể là mới; không kết luận biết toàn bộ corpus tiền huấn luyện PLM khi không có corpus.

#### BIO-07 — Chia dữ liệu dưới đồng thời ràng buộc đồng dạng, thời gian và lớp hiếm — M

**Bài toán/ý nghĩa:** holdout nghiêm ngặt có thể làm lớp hiếm biến mất hoặc mất nhiều mẫu, khiến benchmark không trả lời đúng câu hỏi.

**Đóng góp:** tối ưu nhiều mục tiêu và giải thích các ràng buộc không thể cùng thỏa; trả phương án trade-off được định trước thay vì một split tùy tiện.

**Dữ liệu/đánh giá:** benchmark sequence có date/label thật; so [DataSAIL][s01] và [GraphPart][s02]. Đo leakage theo định nghĩa khóa, coverage lớp, lượng mẫu giữ và thời gian. Tính label balance không cho phép dùng nhãn test để tối ưu mô hình.

**Ứng dụng/điểm chặn:** bộ thiết kế benchmark; chỉ 2–3 loại ràng buộc. Khác BIO-06: nghiên cứu **thuật toán phân bổ**, không chủ yếu chẩn đoán lỗi. Có thể gộp hai hướng khi viết đề cương; không coi chúng là hai đóng góp độc lập nếu dùng chung cơ chế.

#### BIO-08 — Kiểm tra thiết kế thí nghiệm trước phân tích RNA-seq — P

**Bài toán/ý nghĩa:** điều kiện bệnh trùng với batch, paired sample bị coi độc lập hoặc ma trận thiết kế không đủ hạng; chạy xong vẫn có bảng p-value nhưng câu hỏi không ước lượng được.

**Đóng góp:** suy luận từ metadata và contrast để phân biệt không ước lượng được với thiếu công suất, tìm tập thông tin còn thiếu và đề nghị thiết kế phân tích hợp lệ.

**Dữ liệu/đánh giá:** study công khai, ma trận và quyết định tham chiếu được chuyên gia duyệt; so kiểm rank, cảnh báo package và hướng dẫn [GEO2R][s05]/[RNA-seq Bioconductor][s45]. Đo lỗi thiết kế thực phát hiện, cảnh báo sai và số bước sửa.

**Ứng dụng/điểm chặn:** trình kiểm contrast và thiết kế trước chạy. Kiểm rank đã có; phần cải tiến phải hơn một tập quy tắc hiển nhiên. Khi batch trùng hoàn toàn với condition, không “sửa batch” để suy ra hiệu ứng bệnh.

#### BIO-09 — Chọn kết quả RNA-seq bền qua nhiều quyết định phân tích — P

**Bài toán/ý nghĩa:** đổi lọc gene, chuẩn hóa, covariate hay phương pháp có thể đổi hit; nhà nghiên cứu cần một tập ứng viên bền để kiểm nghiệm tiếp.

**Đóng góp:** khảo sát có giới hạn các nhánh phân tích hợp lệ, chọn gene bền và giải thích quyết định gây bất ổn; đề xuất lấy mẫu nhánh thích ứng để giảm chi phí.

**Dữ liệu/đánh giá:** processed counts và benchmark có spike-in/validation độc lập; so pipeline đơn, chạy toàn grid và [multiverse][s51]. Đo phát hiện đúng/FDR khi có truth, độ lặp ở study độc lập và cost; ổn định không đồng nghĩa đúng.

**Ứng dụng/điểm chặn:** workspace so sánh nhánh và xuất danh sách gene kèm độ nhạy. Chỉ vài quyết định có căn cứ sinh học; không thử mọi nhánh rồi chọn nhánh có kết quả đẹp.

#### BIO-10 — Meta-analysis transcriptomics có xét khả năng chuyển giữa cohort — M

**Bài toán/ý nghĩa:** gene đổi mạnh ở một cohort có thể không lặp ở cohort khác; gộp thiếu kiểm tra khác biệt làm danh sách ứng viên khó dùng.

**Đóng góp:** xếp hạng gene theo effect size, heterogeneity và ổn định leave-study-out, kèm nhóm điều kiện mà dấu hiệu còn giữ.

**Dữ liệu/đánh giá:** [recount3][s07]/GEO, vài study cùng mô và endpoint; so random-effects meta-analysis và rank aggregation. Đo tái lập dấu/effect trên study giữ riêng, coverage và độ bền khi thêm nghiên cứu.

**Ứng dụng/điểm chặn:** nhập contrasts, chọn cohort tương thích và xem gene nhất quán. Meta-analysis đã có; cần hơn cách gộp chuẩn. Thiếu covariate không được giải quyết chỉ bằng tăng số study.

### C. Gene, pathway và chuyển ngữ cảnh

#### BIO-11 — Kiểm soát ảnh hưởng của gene nền trong enrichment — P

**Bài toán/ý nghĩa:** over-representation analysis dùng toàn genome trong khi assay chỉ đo được một tập gene có thể tạo kết luận sai về pathway.

**Đóng góp:** suy luận tập gene có thể được chọn từ dấu vết tiền xử lý, lượng hóa độ nhạy và ưu tiên pathway còn bền khi nền hợp lệ thay đổi.

**Dữ liệu/đánh giá:** bảng gene được đo/test, gene set và spike-in/ca kiểm có đáp án; so default background và background do người dùng nhập trong [g:Profiler][s09]. Đo lỗi pathway và tỷ lệ kết luận đổi do nền.

**Ứng dụng/điểm chặn:** kiểm gene universe và báo cáo độ nhạy. Custom background đã có; phần tự truy nguyên/đánh giá mới là đề xuất. Với GSEA dùng danh sách xếp hạng đầy đủ, không áp máy móc quy tắc background của ORA.

#### BIO-12 — Rút gọn pathway trùng lặp nhưng giữ đầy đủ bằng chứng — M

**Bài toán/ý nghĩa:** hàng trăm GO terms cùng do vài gene dẫn dắt làm người dùng tưởng có nhiều phát hiện độc lập.

**Đóng góp:** chọn tập pathway đại diện với ràng buộc coverage gene/bằng chứng và giữ riêng kết quả mâu thuẫn; so loại dư thừa bằng similarity đơn thuần.

**Dữ liệu/đánh giá:** kết quả enrichment công khai và rubric diễn giải độc lập; so [EnrichmentMap/g:Profiler workflow][s52] và [GeneFEAST][s53]. Đo coverage bị mất, mức dư thừa và công rà soát.

**Ứng dụng/điểm chặn:** bản đồ pathway có drill-down về gene gốc. Summarization/visualization đã có; cần chứng minh không chỉ thay bố cục. Cần người kiểm ý nghĩa.

#### BIO-13 — Chuyển danh sách gene/pathway giữa loài có lượng hóa mơ hồ ortholog — M

**Bài toán/ý nghĩa:** ánh xạ gene mouse sang human kiểu lấy một ortholog có thể bỏ qua one-to-many và đổi pathway; ảnh hưởng nghiên cứu mô hình động vật.

**Đóng góp:** lan truyền nhiều ánh xạ hợp lệ thành khoảng độ nhạy kết quả, nêu gene quyết định thay đổi và chỉ đưa kết luận đủ bền.

**Dữ liệu/đánh giá:** [Ensembl Compara][s48], gene sets, dataset ghép cùng mô giữa loài; so one-to-one-only và first-match. Đo mapping, coverage và đồng thuận trên dữ liệu đối chiếu; không suy đồng thuận thành cơ chế bảo tồn.

**Ứng dụng/điểm chặn:** công cụ chuyển danh sách có bằng chứng. Thuật toán orthology đã có; chỉ nghiên cứu hệ quả của sự mơ hồ trong một loại phân tích.

#### BIO-14 — Đánh giá và chọn chữ ký lão hóa theo mô và loại tế bào — M

**Bài toán/ý nghĩa:** một signature senescence có thể tăng vì thành phần tế bào hoặc stress, khiến chọn mẫu thí nghiệm sai.

**Đóng góp:** chọn signature và mức từ chối theo bối cảnh, tách khác biệt thành phần khỏi thay đổi trong cùng loại tế bào, rồi kiểm trên perturbation/assay độc lập.

**Dữ liệu/đánh giá:** [SenMayo][s46], dữ liệu già–trẻ và can thiệp công khai; so signature cố định. Đo khả năng lặp dưới assay độc lập, không train mô hình để học chính điểm SenMayo.

**Ứng dụng/điểm chặn:** workspace so signature và bằng chứng aging. Khớp hướng aging đã ghi trong repo, nhưng tuổi không phải ground truth tế bào senescent; cần nhãn sinh học độc lập trước G1.

#### BIO-15 — Rà soát bất đồng giữa kết quả mức gene và mức isoform — M

**Bài toán/ý nghĩa:** gene không đổi tổng biểu hiện vẫn có thể đổi isoform; một báo cáo gene-level có thể bỏ qua thay đổi đáng kiểm nghiệm.

**Đóng góp:** ưu tiên bất đồng đáng tin bằng quantification uncertainty, annotation và lặp giữa mẫu; giữ riêng trường hợp đo không phân biệt được isoform.

**Dữ liệu/đánh giá:** transcript quantifications và benchmark có spike-ins/long reads; so [IsoformSwitchAnalyzeR][s47] và xếp theo p-value. Đo đúng trên transcript truth, tái lập và số ca phải rà soát.

**Ứng dụng/điểm chặn:** trình đối chiếu gene–transcript–bằng chứng chức năng. Isoform switching đã có phần mềm; phần cải tiến phải là giảm ưu tiên nhầm trong điều kiện mơ hồ.

### D. Đơn bào và dữ liệu không gian

#### BIO-16 — Phân bổ công rà soát nhãn tế bào khi gặp quần thể chưa có trong atlas — M

**Bài toán/ý nghĩa:** gán nhãn bắt buộc có thể ép tế bào mới vào lớp gần nhất; chuyên gia không đủ thời gian xem mọi tế bào.

**Đóng góp:** chọn cluster/cell cần xem dựa trên bất đồng, novelty và tính đại diện, có chế độ từ chối và dự đoán lợi ích của từng lượt rà soát.

**Dữ liệu/đánh giá:** annotation atlas và [OpenProblems][s12]; holdout study/cell type, gold độc lập. So [popV][s49], uncertainty-only và random; lỗi ở lớp chưa thấy, macro-F1/coverage và quality–review budget.

**Ứng dụng/điểm chặn:** bàn duyệt cell type kèm marker; consensus đã có. Không dùng label do chính marker-scoring pipeline tạo làm truth, và không gọi holdout một lớp là mọi kiểu tế bào mới.

#### BIO-17 — Chọn mức xử lý batch có bảo toàn khác biệt sinh học — P

**Bài toán/ý nghĩa:** tích hợp cho UMAP đẹp có thể làm mất trạng thái bệnh, quần thể hiếm hoặc trajectory cần nghiên cứu.

**Đóng góp:** chọn phương pháp/cường độ trên tập phát triển với ràng buộc bảo toàn tín hiệu định trước; nhận diện trường hợp nên giữ batch thay vì ép trộn.

**Dữ liệu/đánh giá:** [scIB][s11] và [OpenProblems][s12], vài bộ có annotation/donor; so Harmony/scVI/unintegrated cùng preprocessing. Đo batch removal, bảo toàn biology, rare populations và downstream theo donor riêng.

**Ứng dụng/điểm chặn:** công cụ so lựa chọn tích hợp và nguyên nhân loại phương án. scIB đã có cả trade-off và metric; đề xuất phải cải thiện **quyết định chọn**. Nhãn đánh giá test không được dùng để chọn tham số; batch–condition trùng hoàn toàn không thể được giải bằng metric.

#### BIO-18 — Phát hiện giả lặp và hỗ trợ chuyển phân tích đơn bào sang đơn vị donor — P

**Bài toán/ý nghĩa:** coi nghìn tế bào như nghìn người độc lập làm độ tin cậy hiệu ứng condition bị thổi phồng.

**Đóng góp:** truy nguyên đơn vị lặp, kiểm contrast và sinh phân tích pseudobulk/mixed-model tương thích; có lời giải thích tại sao một so sánh không hợp lệ.

**Dữ liệu/đánh giá:** dataset nhiều donor và simulation có thiết kế được khóa; so cell-level naïve, [muscat][s13] và pseudobulk chuẩn. Đo FDR/power khi có truth, lỗi thiết kế và thao tác sửa.

**Ứng dụng/điểm chặn:** trợ lý thiết kế differential state. Pseudobulk không mới; nếu chỉ bao một nút chạy muscat thì đóng góp yếu. Dữ liệu một donor mỗi condition không được biến thành đánh giá quần thể nhờ nhiều tế bào.

#### BIO-19 — Chọn quan hệ giao tiếp tế bào bền qua nguồn và cách phân tích — M

**Bài toán/ý nghĩa:** ligand–receptor ranking đổi theo annotation, database, biểu hiện và tỷ lệ tế bào; lab cần ít ứng viên đáng kiểm nghiệm hơn.

**Đóng góp:** phân rã độ nhạy theo donor, tài nguyên và annotation, xếp quan hệ bền với điều kiện hỗ trợ không gian/perturbation nếu có.

**Dữ liệu/đánh giá:** bộ multi-donor, spatial hoặc perturbation; so consensus [LIANA+][s14] và rank một phương pháp. Đo tái lập và hit có validation độc lập; bootstrap theo donor, không chỉ theo cell.

**Ứng dụng/điểm chặn:** workspace chọn ligand–receptor và truy nguyên nguồn. Stability/consensus đã có tiền lệ; biểu hiện đồng thời không là ground truth giao tiếp hay quan hệ nhân quả. G1 khó nếu thiếu validation.

#### BIO-20 — Định lượng độ chắc chắn của vùng sinh học trên spatial transcriptomics — H

**Bài toán/ý nghĩa:** một phân vùng duy nhất che giấu ranh giới không ổn định; chọn nhầm vùng làm sai phân tích downstream.

**Đóng góp:** tổng hợp phân vùng qua tham số/resampling thành vùng ổn định và ranh giới cần rà soát, có cơ chế ưu tiên annotation vùng khó.

**Dữ liệu/đánh giá:** mô có annotation giải phẫu từ benchmark và các lát độc lập; so một phân vùng và entropy ensemble. Đo boundary error, calibration, rare-region recall và cost. [Benchmark spatial alignment 2026][s15] là tiền lệ liên quan, **không đồng nhất** tác vụ căn chỉnh với phân vùng.

**Ứng dụng/điểm chặn:** bản đồ spatial có uncertainty overlay và vùng duyệt. Cần annotation đáng tin và hạn chế RAM; bắt đầu processed matrix của vài lát, không mô hình nền lớn.

### E. Proteomics và bằng chứng protein

#### BIO-21 — Chọn quy trình proteomics có kiểm soát sai số do dữ liệu thiếu — P

**Bài toán/ý nghĩa:** điền giá trị thiếu có thể tạo protein khác biệt giả; lab cần chọn protein thật để kiểm nghiệm tiếp.

**Đóng góp:** bộ chọn workflow theo đặc điểm missingness và thiết kế, với điều kiện giữ mức lỗi và tùy chọn từ chối khuyến nghị; phân biệt phần lợi ích chuẩn hóa, điền thiếu và phép kiểm.

**Dữ liệu/đánh giá:** spike-in từ benchmark [OpDEA][s16]/[SCPDA][s17], holdout toàn dataset/assay. So workflow mạnh nhất của tiền lệ, no-imputation và lựa chọn cố định; power ở mức FDR thực nghiệm, số false hits và runtime.

**Ứng dụng/điểm chặn:** nhận matrix + design, đề nghị workflow và xuất bằng chứng chọn protein. Recommendation và Shiny đã có; cần lợi ích hơn OpDEA/SCPDA. Không thể xác định chắc cơ chế thiếu chỉ từ một matrix; raw MS không nằm trong MVP đầu tiên.

#### BIO-22 — Lan truyền sự mơ hồ peptide–protein tới kết quả định lượng — P

**Bài toán/ý nghĩa:** peptide dùng chung cho nhiều protein/isoform làm kết luận “protein A thay đổi” có thể vượt quá khả năng đo.

**Đóng góp:** giữ nhóm protein không phân biệt được, lan truyền lựa chọn phân bổ peptide thành khoảng độ nhạy của effect/rank và đề nghị peptide bổ sung có thể phân biệt ứng viên.

**Dữ liệu/đánh giá:** benchmark protein mixtures như iPRG và bảng peptide định lượng; so unique-only, parsimony và đầu ra [EPIFANY][s50]. Đo protein attribution sai, coverage nhóm đúng, độ chính xác effect và chất lượng theo số peptide bổ sung.

**Ứng dụng/điểm chặn:** đồ thị peptide–protein và danh sách ứng viên được duyệt. Protein inference đã là lĩnh vực lâu năm; trọng tâm đề xuất là **hệ quả ở differential abundance và quyết định theo dõi**, không phát minh lại inference. Xác minh bộ có quantification thích hợp trước G1.

#### BIO-23 — Phân biệt thay đổi PTM với thay đổi lượng protein tổng — M

**Bài toán/ý nghĩa:** phosphopeptide tăng có thể vì protein tăng, không phải mức điều hòa phosphorylation tăng; ảnh hưởng ưu tiên pathway/kinase.

**Đóng góp:** đối soát PTM–protein, truyền uncertainty và missing parent protein vào kết luận, chọn site/nhóm site đủ bằng chứng cho thay đổi vượt nền protein.

**Dữ liệu/đánh giá:** study có phosphoproteomics và total proteome cùng mẫu từ [PRIDE][s18]; spike-in hoặc perturbation kiểm độc lập. So raw PTM fold-change và cách chuẩn hóa theo parent protein; false calls, sign consistency và coverage.

**Ứng dụng/điểm chặn:** workspace xem PTM và protein nền. Chuẩn hóa parent protein có tiền lệ; phải khảo sát phương pháp chuyên biệt trước khi gọi mới. Không gọi ratio intensity là occupancy nếu chưa đo điều kiện cần.

#### BIO-24 — Ánh xạ bằng chứng giữa trình tự, isoform và cấu trúc có kiểm tra tọa độ — P

**Bài toán/ý nghĩa:** số residue trên PDB, UniProt và chuỗi thí nghiệm khác nhau; gắn PTM/đột biến vào vị trí sai làm đọc sai bằng chứng.

**Đóng góp:** chuỗi ánh xạ giữ insertion, residue chưa quan sát, mutation và isoform, từ chối chuyển khi không đủ căn cứ; truy nguyên chính xác ca không đồng nhất.

**Dữ liệu/đánh giá:** [SIFTS][s19], mmCIF/FASTA và ca mapping được rà soát độc lập; so offset và alignment đơn giản, rồi so SIFTS ở phạm vi nó hỗ trợ. Đo mapping sai trên residue được kiểm, coverage và lỗi downstream.

**Ứng dụng/điểm chặn:** trình đối chiếu tọa độ và xuất annotation đã kiểm. SIFTS đã làm residue-level mapping; phần khác biệt phải nằm ở chuỗi thí nghiệm/isoform và nhiều bước chuyển. pLDDT không phải xác suất annotation đúng.

#### BIO-25 — Hòa giải assay hiệu ứng biến thể khác nhau trên cùng protein — M

**Bài toán/ý nghĩa:** một biến thể có thể giảm abundance nhưng giữ activity, hoặc ngược lại; gộp thành một nhãn “xấu” làm mất điều thực nghiệm đo được.

**Đóng góp:** lập quan hệ variant–assay–endpoint–context, phát hiện bất đồng có thể giải thích được và chọn assay cần thêm để phân biệt giả thuyết.

**Dữ liệu/đánh giá:** [MaveDB assay facts][s20], tập variant được đo ở nhiều assay; so z-score pooling và hồ sơ từng assay. Đánh giá theo assay giữ riêng, nhận diện endpoint sai và utility chọn assay trong replay.

**Ứng dụng/điểm chặn:** hồ sơ variant với bằng chứng theo endpoint. MaveDB đã có metadata, mapping và calibration; không nhận hồ sơ bằng chứng là mới. Cần số assay giao nhau đủ lớn; mục tiêu là nghiên cứu chức năng, không tự kết luận bệnh lý.

### F. Vi sinh và metagenomics

#### BIO-26 — Rà soát bất đồng giữa gene kháng thuốc và phenotype đo thực nghiệm — M

**Bài toán/ý nghĩa:** tìm thấy gene AMR không luôn đồng nghĩa phenotype kháng trong mọi loài/điều kiện; nhà nghiên cứu cần biết ca nào đáng xem lại.

**Đóng góp:** đối soát genotype–assay–loài–chất lượng assembly, phân nhóm lý do bất đồng và xếp ưu tiên kiểm nghiệm bổ sung theo bằng chứng.

**Dữ liệu/đánh giá:** [NCBI NDARO/AMRFinderPlus][s21] và isolate có AST đi kèm; so gene-presence rules. Đo recall ca bất đồng đã được rà soát, precision ưu tiên và coverage; chia theo lineage/study.

**Ứng dụng/điểm chặn:** bàn rà soát AMR. Trước G1 phải đếm isolate ghép được phenotype, chuẩn AST và missingness; không coi AMRFinder output là nhãn kháng thuốc thực nghiệm. Không hướng tới chọn thuốc điều trị.

#### BIO-27 — Lựa chọn xử lý nhiễm bẩn trong microbiome có xét chi phí mất tín hiệu — M

**Bài toán/ý nghĩa:** loại contaminant quá ít tạo tín hiệu giả; loại quá nhiều làm mất vi sinh vật thật, nhất là mẫu biomass thấp.

**Đóng góp:** chọn ngưỡng/cơ chế lọc theo control và độ nhạy downstream, trả vùng không chắc thay vì một nhãn cứng.

**Dữ liệu/đánh giá:** dilution/mock community và negative controls; so [decontam][s23] ở cấu hình chuẩn và prevalence/frequency riêng. Đo contaminant recall, mất taxon thật, sai lệch composition và quyết định association.

**Ứng dụng/điểm chặn:** trình duyệt control–sample và kịch bản lọc. Contamination detection đã có; cần dữ liệu control hợp lệ. Không nhận mọi taxon hiếm là contaminant.

#### BIO-28 — Đánh giá độ bền taxonomic profiling khi database tham chiếu thay đổi — M

**Bài toán/ý nghĩa:** nghiên cứu chạy ở hai thời điểm có thể báo thành phần khác vì taxonomy/reference đổi; việc so cohort bị lẫn với thay đổi pipeline.

**Đóng góp:** chuẩn hóa lineage và xây khoảng độ nhạy giữa snapshots, phân biệt đổi tên, độ phân giải và thay đổi bằng chứng reads; chọn phần báo cáo đủ bền.

**Dữ liệu/đánh giá:** mock communities/[CAMI][s22], outputs từ vài snapshots đã khóa. So một database và giao tập taxon đơn giản; lỗi abundance/rank theo truth, tốc độ đối soát và số kết luận còn dùng được.

**Ứng dụng/điểm chặn:** so sánh hai báo cáo microbiome. Cần lấy được database lịch sử và giới hạn dung lượng; có thể khởi đầu từ outputs có sẵn. CAMI gồm dữ liệu mô phỏng, không tự chứng minh hiệu quả trên mẫu lâm sàng.

#### BIO-29 — Chọn đặc trưng microbiome có khả năng lặp giữa nghiên cứu — P

**Bài toán/ý nghĩa:** mô hình/phát hiện có thể theo study, diet hoặc lab thay vì phenotype; cần danh sách taxa/pathway dùng được ở cohort mới.

**Đóng góp:** pipeline chọn đặc trưng có subject grouping, học preprocessing trong train và stability theo study; điều kiện từ chối khi metadata không cho tách confounder.

**Dữ liệu/đánh giá:** [curatedMetagenomicData][s24], vài cohort cùng endpoint; so pipeline trong-study và leave-study-out chuẩn. Đo AUCPR/balanced accuracy tùy tác vụ, sign stability, calibration, feature cost và kết quả từng study.

**Ứng dụng/điểm chặn:** workspace chọn cohort và xuất signature kèm miền áp dụng. Không chỉ audit điểm giảm: G2 cần chọn đặc trưng/decision tốt hơn baseline mạnh. Batch confounding không đồng nghĩa mọi trường hợp đều là leakage; CLR riêng từng mẫu không tự động nhìn test, còn transform học thống kê toàn bộ cohort thì phải audit cụ thể.

#### BIO-30 — Chọn metagenome-assembled genomes theo độ tin cậy của phân tích downstream — H

**Bài toán/ý nghĩa:** ngưỡng completeness/contamination chung có thể giữ MAG không phù hợp để phân tích một pathway hoặc gene AMR cụ thể.

**Đóng góp:** đánh giá chất lượng theo tác vụ, mô phỏng mất/ghép contig để chọn ngưỡng tối thiểu giữ kết luận pathway và ưu tiên MAG cần kiểm lại.

**Dữ liệu/đánh giá:** genome/reference và MAG benchmark [CAMI][s22]; so ngưỡng [CheckM2][s25] và QC cố định. Đo false pathway/AMR calls, coverage MAG giữ và hiệu quả rà soát.

**Ứng dụng/điểm chặn:** trình QC MAG gắn với câu hỏi phân tích. Không dùng CheckM2 output làm truth cho chính công cụ; cần kiểm lại bộ gene thật và dùng genome chuẩn độc lập. Hạn chế raw assembly ở MVP.

### G. Perturbation, ảnh và thiết kế thí nghiệm

#### BIO-31 — Chọn hit CRISPR bền với guide bất thường và khác biệt replicate — M

**Bài toán/ý nghĩa:** hit gene có thể bị dẫn dắt bởi một guide hoặc replicate; lab tốn thí nghiệm theo dõi hit không bền.

**Đóng góp:** mô hình ảnh hưởng từng guide/replicate lên thứ hạng, chọn hit theo độ bền và đề nghị guide cần kiểm nghiệm tiếp.

**Dữ liệu/đánh giá:** count matrices, controls và validation screens; so [MAGeCK][s26], leave-one-guide-out và rank chuẩn. Đo precision@k trên validation độc lập, stability và số assay để đạt số hit xác nhận.

**Ứng dụng/điểm chặn:** bàn duyệt CRISPR hits. Robust ranking đã có trong MAGeCK; phải đối chiếu các công cụ mới trước chốt. Không cần trở lại bài toán dự đoán off-target, nhưng copy-number/guide quality vẫn là yếu tố phải xét.

#### BIO-32 — Chọn perturbation tiếp theo theo khả năng kiểm nghiệm giả thuyết — H

**Bài toán/ý nghĩa:** giữa nhiều gene perturbation, nhà nghiên cứu cần chọn can thiệp phân biệt các giả thuyết, không chỉ dự đoán một vector RNA gần trung bình.

**Đóng góp:** xếp perturbation bằng hiệu ứng kỳ vọng, uncertainty và khác biệt với controls, tối ưu utility của một mục tiêu đã khóa như tìm gene đổi pathway.

**Dữ liệu/đánh giá:** Perturb-seq measured responses, giữ gene/condition/cell-line đúng kịch bản; so linear/mean baselines và policy không thích ứng. [Systema][s27] đã kiểm systematic variation; [bài 01/10/2026][s28] đã đề xuất metric calibration. Đo hit discovery/regret theo assay, không chỉ correlation toàn gene.

**Ứng dụng/điểm chặn:** chọn can thiệp và xem bằng chứng; offline replay chỉ định lượng trong pool có đo. Metric calibration không còn là novelty riêng; không được kết luận tất cả DL kém hơn linear từ các benchmark cũ.

#### BIO-33 — Kiểm chất lượng và chọn chuẩn hóa ảnh Cell Painting bảo toàn hiệu ứng perturbation — M

**Bài toán/ý nghĩa:** illumination, plate hoặc cell density có thể lấn át hình thái do perturbation; hit morphology khó lặp giữa lab.

**Đóng góp:** phát hiện nuisance và chọn normalization dưới ràng buộc giữ control/replicate biological effects; từ chối cấu hình xóa cả tín hiệu thật.

**Dữ liệu/đánh giá:** một tập profiles/metadata từ [Cell Painting Gallery][s29]; so chuẩn hóa theo controls, batch correction và uncorrected. Đo percent replicating, retrieval perturbation trên plate/study riêng và QC false alarms.

**Ứng dụng/điểm chặn:** workspace QC plate và các lựa chọn normalization. Bắt đầu numerical profiles; không tải toàn bộ ảnh của kho. Đây là phenomics/computational biology, mức khớp chuyên môn protein của GVHD cần xác nhận.

#### BIO-34 — Phân bổ lượt sửa mask tế bào theo tác động tới phép đo sinh học — M

**Bài toán/ý nghĩa:** mask sai ở vài tế bào quan trọng có thể đổi cell count/size distribution; sửa mọi ảnh tốn công.

**Đóng góp:** chọn ảnh/vùng cần sửa dựa trên lỗi dự kiến của endpoint downstream, so với chỉ chọn entropy segmentation; học từ phản hồi con người.

**Dữ liệu/đánh giá:** LIVECell hoặc benchmark microscopy có mask tay, holdout loại tế bào/nguồn ảnh; so random, uncertainty và [Cellpose/μSAM][s30]. Đo count/area error và quality–annotation budget ngoài segmentation IoU.

**Ứng dụng/điểm chặn:** trình sửa mask kèm thứ tự đề nghị. GUI và human-in-the-loop đã có; đề xuất là tiêu chí chọn theo endpoint. Cần xác nhận bioimage analysis phù hợp luận văn, và không đổi sang ảnh y khoa chỉ để có dataset.

#### BIO-35 — Chọn lô biến thể protein để thí nghiệm dưới ngân sách và ràng buộc đa dạng — M

**Bài toán/ý nghĩa:** chọn toàn biến thể có điểm dự đoán cao có thể lãng phí lô thí nghiệm ở một vùng tương tự; cần cân bằng khám phá và khai thác.

**Đóng góp:** chọn theo batch có tính cost, đa dạng và uncertainty assay; đánh giá tìm hit với ít phép đo hơn, giữ surrogate model cố định để tách lợi ích policy.

**Dữ liệu/đánh giá:** landscapes **đã đo** từ [ALDE][s31]/MaveDB phù hợp; so random, top-prediction, Bayesian optimization và policy ALDE. Đo số hit, best measured fitness, regret và cost qua nhiều seed/protein.

**Ứng dụng/điểm chặn:** thiết kế lô và nhật ký assay. Active learning protein engineering đã có; cần một ràng buộc/góc đánh giá chưa được tiền lệ giải đủ. Không dùng dự đoán của một mô hình làm “phòng thí nghiệm” rồi nhận hiệu quả sinh học; replay chỉ truy vấn pool có measured outcomes.

### H. Kỹ nghệ phần mềm cho tin sinh

#### BIO-36 — Kiểm tra hợp lệ ngữ nghĩa của workflow tin sinh trước khi chạy — P

**Bài toán/ý nghĩa:** tệp đúng CSV và công cụ chạy được vẫn có thể sai loài, genome build, count scale hoặc đơn vị lặp; phí tính toán và kết luận đều bị ảnh hưởng.

**Đóng góp:** hợp đồng dữ liệu theo thuộc tính sinh học, tìm tập ràng buộc mâu thuẫn tối thiểu và đề nghị thao tác sửa có căn cứ; tách thiếu metadata khỏi dữ liệu chắc sai.

**Dữ liệu/đánh giá:** một pipeline RNA-seq cùng ca lỗi thực và mutations được khóa; so [nf-schema][s32], [nf-core/rnaseq][s33] và quy tắc sẵn có. Đo lỗi **ngoài baseline** phát hiện, precision/recall, false blocking và compute tránh lãng phí.

**Ứng dụng/điểm chặn:** preflight checker, duyệt nguyên nhân và xuất manifest hợp lệ. nf-schema đã validate parameters/samplesheets; [APE/Workflomics][s34] đã dùng thông tin ngữ nghĩa để khám phá workflow. Không nhận “kiểm ngữ nghĩa” chung là mới, không bịa metadata để sửa tự động.

#### BIO-37 — Kiểm thử hồi quy theo kết quả sinh học khi nâng phiên bản pipeline — P

**Bài toán/ý nghĩa:** nâng package/container có thể vẫn chạy thành công nhưng đổi gene list, effect sign hoặc sample matching; người duy trì cần biết thay đổi nào đáng xem.

**Đóng góp:** thiết kế semantic assertions và phép so cho đầu ra thống kê, phân biệt biến động số nhỏ với thay đổi kết luận, ưu tiên rerun/inspection theo tác động.

**Dữ liệu/đánh giá:** fixtures có truth và pairs phiên bản pipeline thực; so checksum, numeric tolerance và kiểm thử hiện có trong nf-core. Đo missed changes, false alerts, defect recall và thời gian duy trì. [OpenProblems][s12] đã có interfaces/control methods; benchmark runner không mới.

**Ứng dụng/điểm chặn:** báo cáo regression có drill-down về gene/contrast. Cần golden cases độc lập, không định nghĩa đúng chỉ bằng giống phiên bản cũ. Khác BIO-05 ở nguồn thay đổi là **code/tool**, và không thay thế tests của pipeline.

#### BIO-38 — Chọn workflow tin sinh dưới giới hạn RAM, thời gian và chất lượng — M

**Bài toán/ý nghĩa:** một cấu hình tốt trên benchmark lớn có thể không chạy được ở lab có máy nhỏ; cần chọn cấu hình đủ chất lượng cho bài toán.

**Đóng góp:** mô hình dự báo cost–quality từ pilot và metadata, chọn ứng viên Pareto với độ không chắc, dừng pilot khi đủ thông tin.

**Dữ liệu/đánh giá:** vài workflow trên processed RNA/proteomics hoặc tập reads nhỏ; so fixed recipe, all-grid và [Workflomics][s34]. Đo quality loss, peak RAM, thời gian tổng **kể cả pilot** và thất bại vượt RAM.

**Ứng dụng/điểm chặn:** cấu hình máy → khuyến nghị → benchmark tái lập. Workflomics đã đo cả runtime/memory/scientific metrics; điểm mới phải là chính sách chọn. Không chuyển RCA sang bio rồi mặc định novelty; hardware transfer cần đo riêng.

#### BIO-39 — Chạy lại tăng dần khi thêm mẫu, với điều kiện kết quả thống kê được cập nhật đúng — M

**Bài toán/ý nghĩa:** cohort tăng dần; tái chạy tất cả tốn chi phí, nhưng giữ normalization/DE cũ có thể sai vì thống kê phụ thuộc toàn cohort.

**Đóng góp:** phân loại bước phụ thuộc từng mẫu và toàn cohort, suy ra phạm vi invalidation chính xác, tối ưu cache mà vẫn tương đương rerun hợp lệ.

**Dữ liệu/đánh giá:** sequences of cohort additions, benchmark truth khi có; so full rerun và [Nextflow resume][s35]. Đo equivalence trong tolerance khóa, hit/sign thay đổi được bắt, compute/storage thực tiết kiệm.

**Ứng dụng/điểm chặn:** thêm sample và xem kế hoạch chạy lại. Caching/invalidation đã có; cần một trường hợp cohort-dependent cụ thể mà baseline chưa xử lý đủ. Không chấp nhận kết quả cũ chỉ vì không đổi tệp count từng mẫu.

#### BIO-40 — Chẩn đoán phần thiếu và hỗ trợ phục hồi gói tái lập nghiên cứu — M

**Bài toán/ý nghĩa:** có code/PDF nhưng thiếu input snapshot, annotation, parameters hoặc environment; nghiên cứu không tái chạy được bởi người khác.

**Đóng góp:** từ manifest/run graph xác định dependency còn thiếu, xếp hạng hành động phục hồi và tạo gói tái lập kiểm được; phân biệt chạy được với lặp kết luận.

**Dữ liệu/đánh giá:** workflow công khai cùng bundles đầy đủ/thiếu và lỗi thực; so checklist, README và validator [Workflow Run RO-Crate][s36]. Đo rerun success, artifact recovery, thời gian và conclusion agreement.

**Ứng dụng/điểm chặn:** trình kiểm và hướng dẫn bổ sung gói nghiên cứu. Provenance packaging đã có chuẩn; cần hơn export RO-Crate. Đánh giá thời gian người dùng cần người dùng thật; lỗi chèn chỉ là kiểm kỹ thuật bổ trợ.

### I. Genome, khám phá chức năng và chuyển hóa

#### BIO-41 — Đánh giá variant caller theo loại vùng genome và hỗ trợ chọn pipeline — M

**Bài toán/ý nghĩa:** một F1 tổng cao có thể che lỗi ở vùng lặp hoặc loại biến thể mà nghiên cứu quan tâm; người dùng cần chọn pipeline theo mục tiêu.

**Đóng góp:** khuyến nghị pipeline theo profile lỗi, coverage và cost ở vùng mục tiêu; giải thích trade-off và từ chối ngoài miền benchmark.

**Dữ liệu/đánh giá:** VCF/BED chuẩn từ [Genome in a Bottle][s37], bắt đầu outputs có sẵn; so caller tốt nhất toàn genome và quy tắc chọn cố định. Đo precision/recall theo stratification, chất lượng vùng mục tiêu và runtime thực.

**Ứng dụng/điểm chặn:** workspace so variants và chọn cấu hình nghiên cứu. GIAB và stratified benchmarking đã có; chỉ dashboard F1 không đủ. Truth chỉ áp trong benchmark regions, không gọi mọi variant ngoài vùng đó là sai.

#### BIO-42 — Rà soát transcript mới bằng bằng chứng long-read và short-read bổ trợ — H

**Bài toán/ý nghĩa:** transcript mới có thể là artifact, truncation hoặc lỗi splice; lab cần chọn ít transcript đáng xác minh.

**Đóng góp:** hòa giải nhiều công cụ gọi transcript và bằng chứng junction/read support, xếp ưu tiên kèm uncertainty và trạng thái không phân biệt được.

**Dữ liệu/đánh giá:** [LRGASP][s38], spike-in và outputs transcript callers; so consensus đơn và một caller mạnh. Đo transcript precision/recall, abundance error và validation yield khi có dữ liệu độc lập.

**Ứng dụng/điểm chặn:** trình rà soát gene–isoform với evidence tracks. Transcript consensus và caller benchmarks đã có; cần hơn giao/union danh sách. Thu hẹp một gene set hoặc processed outputs trước, không toàn bộ long-read raw.

#### BIO-43 — Truy nguyên gene AMR nằm trên plasmid nào khi assembly còn mơ hồ — H

**Bài toán/ý nghĩa:** biết gene kháng thuốc mà không biết ngữ cảnh di truyền khiến nghiên cứu khả năng lan truyền hạn chế; short-read assembly có nhiều kết nối khả dĩ.

**Đóng góp:** giữ nhiều phương án gán contig–plasmid, xếp bằng chứng và chọn contig/reads cần bổ sung để phân biệt, thay vì đưa một host assignment chắc chắn giả.

**Dữ liệu/đánh giá:** isolate có assembly hoàn chỉnh/long-read đối chiếu và gene calls [AMRFinderPlus][s21]; so công cụ plasmid reconstruction được chọn sau khảo sát. Đo đúng vị trí gene, coverage từ chối và query cost.

**Ứng dụng/điểm chặn:** browser gene–contig–plasmid. Cần khảo sát trực tiếp MOB-suite và các phương pháp mới trước G2; hiện mới xác nhận bài toán/nguồn AMR, **tiền lệ gần nhất chưa đủ**. Không suy assembly association thành truyền ngang đã xảy ra.

#### BIO-44 — Ưu tiên cụm gene sinh tổng hợp để khảo sát dựa trên đa dạng và chất lượng bằng chứng — M

**Bài toán/ý nghĩa:** genome mining sinh nhiều BGC gần nhau; chọn top similarity có thể chỉ lặp các cụm đã biết, chọn thấp similarity có thể chỉ chọn cụm lắp ráp kém.

**Đóng góp:** chọn danh sách đa dạng theo ngân sách với điều kiện completeness/evidence, giảm chọn trùng và giữ nhóm có hoạt tính tham chiếu đáng kiểm.

**Dữ liệu/đánh giá:** [antiSMASH/MIBiG comparisons][s39], bộ cụm có chú giải sản phẩm; so similarity-only, clustering + representative và diversity sampling. Đo coverage nhóm chức năng, redundancy và retrieval trên họ giữ riêng.

**Ứng dụng/điểm chặn:** workspace duyệt BGC và xuất nhóm ứng viên. Genome mining/cluster comparisons đã có; novelty score thấp không chứng minh chất mới hay hoạt tính. G2 bước đầu là chất lượng ưu tiên, không hứa khám phá hợp chất bằng in-silico.

#### BIO-45 — Mô hình chuyển hóa với nhiều phương án gap-filling có kiểm tra phenotype — H

**Bài toán/ý nghĩa:** thêm reaction để mô hình “tăng trưởng được” có thể tạo nhiều nghiệm, trong đó một số dự đoán sai khả năng dùng chất dinh dưỡng.

**Đóng góp:** sinh ensemble phương án gap-fill, lọc bằng phenotype độc lập và chọn thí nghiệm substrate phân biệt các nghiệm; trình bày phần kết luận bền.

**Dữ liệu/đánh giá:** genome/metabolic models và growth phenotypes từ tài liệu [gapseq][s40]; so một nghiệm minimal gap-fill và pipeline chuẩn. Đo growth prediction trên điều kiện giữ riêng, reaction uncertainty và số thí nghiệm replay.

**Ứng dụng/điểm chặn:** thiết kế môi trường nuôi và đối chiếu nghiệm metabolic model. Gap-filling/ensemble đã có tiền lệ; cần khảo sát thuật toán ensemble/experimental design chuyên biệt. Kiến thức chuyển hóa và lập trình tối ưu là phần nặng.

### J. Tổng hợp bằng chứng và nghiên cứu nhiều điều kiện

#### BIO-46 — Chọn module đồng biểu hiện bền và có khả năng chuyển cohort — M

**Bài toán/ý nghĩa:** gene hub hoặc module nổi bật có thể đổi khi thêm mẫu hoặc study; lab cần module đáng chọn để nghiên cứu tiếp.

**Đóng góp:** stability selection theo donor/study, chọn module theo bảo toàn và effect độc lập, truy nguyên mẫu quyết định làm module biến mất.

**Dữ liệu/đánh giá:** processed RNA cohorts, so WGCNA và [BioNERO][s41] với module preservation chuẩn. Đo ổn định trên cohort riêng, gene coverage và liên hệ endpoint đã khóa.

**Ứng dụng/điểm chặn:** workspace chọn modules/hubs. Module preservation đã có; cần cơ chế chọn cải thiện thật. Co-expression không phải regulatory causality; không dùng hub score làm ground truth chức năng.

#### BIO-47 — Kiểm định biomarker sống còn có kiểm soát lựa chọn cut-off và chuyển cohort — H

**Bài toán/ý nghĩa:** chọn cut-off sau khi nhìn toàn bộ survival hoặc chọn gene từ cùng dữ liệu làm biomarker quá lạc quan; nghiên cứu sau khó tái lập.

**Đóng góp:** quy trình khóa lựa chọn trên development, kiểm calibration/utility trên cohort riêng và ưu tiên marker có effect ổn định, kèm phát hiện lỗi quy trình.

**Dữ liệu/đánh giá:** [GDC/TCGA clinical resource][s42], expression open-access phù hợp và cohort ngoài khi có; so Cox continuous, cut-off chọn trong train và kiểm định chuẩn. Đo discrimination, calibration và effect replication theo patient.

**Ứng dụng/điểm chặn:** workspace nghiên cứu biomarker với split và endpoint khóa. Không chỉ báo kết quả cũ giảm; G2 cần cải thiện quyết định chọn hoặc độ tin cậy. Phải audit event/censoring, treatment và số events; không là công cụ tiên lượng dùng cho người bệnh.

#### BIO-48 — Truy hồi perturbation phù hợp ngữ cảnh từ chữ ký biểu hiện gene — M

**Bài toán/ý nghĩa:** một perturbation đảo chiều signature ở cell line này có thể không làm vậy ở cell line khác, dose/time khác; người nghiên cứu cần shortlist phù hợp assay.

**Đóng góp:** xếp hạng có điều kiện cell context/dose/time và concordance replicate, từ chối nơi không đủ dữ liệu; phân biệt measured với inferred expression.

**Dữ liệu/đánh giá:** CMap/LINCS public releases trên GEO; so connectivity score và retrieval không điều kiện. Đo retrieval effect trên context/perturbagen giữ riêng và lặp assay độc lập.

**Ứng dụng/điểm chặn:** công cụ chọn perturbation để nghiên cứu tiếp. [CLUE thông báo ngừng website/tools từ 31/01/2026][s43], public data vẫn được dẫn sang GEO; không thiết kế MVP phụ thuộc API CLUE đang hoạt động. Signature reversal không chứng minh tác dụng điều trị.

#### BIO-49 — Chuẩn hóa GWAS summary statistics với chẩn đoán lỗi allele/build trước tích hợp — M

**Bài toán/ý nghĩa:** sai genome build, strand, effect allele hoặc ambiguous SNP có thể làm đảo dấu và sai phân tích tích hợp GWAS–QTL.

**Đóng góp:** liên kết kiểm allele/build với hậu quả downstream, giữ ambiguous cases và xếp thứ tự sửa theo tác động; xuất bộ summary có provenance.

**Dữ liệu/đánh giá:** [GWAS Catalog summary statistics][s44], reference variants, ca lỗi thực được kiểm; so harmonization chuẩn và validators hiện có. Đo sign/allele errors, coverage và độ đúng kết luận downstream trên truth/simulation khóa.

**Ứng dụng/điểm chặn:** preflight checker GWAS–QTL. Harmonization đã có hệ sinh thái; trước chốt phải đối chiếu công cụ chuyên biệt và pipeline GWAS Catalog, không chỉ kiểm SNP/string. Colocalization không tự chứng minh gene gây bệnh.

#### BIO-50 — Chọn thời điểm và replicate cho thí nghiệm transcriptomics theo ngân sách — M

**Bài toán/ý nghĩa:** lấy nhiều mốc thời gian nhưng ít replicate có thể khó tách tín hiệu; một lịch lấy mẫu cố định có thể bỏ qua chuyển trạng thái quan trọng.

**Đóng góp:** tối ưu phân bổ timepoints–replicates theo pilot và mục tiêu phát hiện đáp ứng/ước lượng đường cong, xét cost và uncertainty.

**Dữ liệu/đánh giá:** time-course RNA counts, ví dụ fission của [RNA-seq workflow][s45]; simulation có truth và replay measured timepoints. So uniform timepoints, replicate-first và thiết kế optimal chuẩn; power khi có truth, reconstruction error và cost.

**Ứng dụng/điểm chặn:** trình thiết kế lịch thí nghiệm và so phương án. Không dùng các mốc chưa mở để chọn trong replay; full dataset là **tham chiếu phép đo**, không là cơ chế thật. Cần khảo sát optimal experimental design gần nhất và không suy chi phí replay thành tiền lab đã tiết kiệm.

## 4. Mười hướng nên khảo sát sâu trước

Đây là **thứ tự công việc khảo sát**, không phải chốt một đề tài thắng. Ưu tiên dựa trên vấn đề cụ thể, đường đo đóng góp dương và sản phẩm tự nhiên; độ mới của tất cả hướng còn chưa chắc. Không chấm điểm tổng để che thiếu G1 hoặc baseline mạnh.

| Hướng | Vì sao đáng ưu tiên | Phần cần chứng minh vượt tiền lệ | Điều kiện làm hạ ưu tiên |
|---|---|---|---|
| **01. Chọn dữ liệu phân tích được** | Giảm lãng phí ngay từ đầu nghiên cứu; app gắn với công việc sàng lọc | Chọn/loại đúng hơn tìm kiếm + bộ lọc, với ít công hơn | Không có bộ tiêu chí/gold độc lập hoặc khác biệt chỉ là RAG trên metadata |
| **03. Hòa giải định danh mơ hồ** | Nhiều workflow cần, phạm vi dữ liệu tương đối gọn | Giảm ghép sai và ảnh hưởng downstream ở cùng coverage | UniProt/g:Profiler + quy tắc chuẩn đã giải đủ ca khó |
| **06. Sửa rò rỉ nhiều tầng** | Tận dụng kiến thức audit repo, ứng dụng có hành động cụ thể | Repair giữ nhiều dữ liệu hơn với vi phạm được kiểm độc lập | GraphPart/DataSAIL đã đáp ứng toàn bộ ràng buộc mục tiêu |
| **09. Chọn kết quả RNA bền** | Đầu ra trực tiếp là danh sách gene đáng kiểm nghiệm | Giữ power/FDR hoặc validation yield với cost thấp hơn full multiverse | Chỉ tăng stability mà không tăng chất lượng độc lập |
| **17. Chọn xử lý batch** | Giữ khác biệt sinh học quan trọng trong nghiên cứu đơn bào | Quyết định chọn tốt hơn bộ tiêu chí scIB cố định trên dataset riêng | Condition trùng batch hoặc chỉ có nhãn do model sinh ra |
| **21. Proteomics dữ liệu thiếu** | Có thể đo false positives/power bằng spike-in | Chọn workflow an toàn/tốt hơn OpDEA/SCPDA ngoài dataset phát triển | Không hơn recommender mạnh hoặc không có endpoint truth phù hợp |
| **22. Peptide–protein mơ hồ** | Gần chuyên môn protein và tác động trực tiếp tới danh sách theo dõi | Lan truyền ambiguity làm giảm kết luận sai ở abundance/validation | Dữ liệu chỉ có identification, không đủ đo đóng góp downstream |
| **29. Signature microbiome chuyển study** | Tăng khả năng tái sử dụng phát hiện, không chỉ báo điểm bị thổi phồng | Selection tốt hơn leave-study-out chuẩn trên study độc lập | Subject metadata không đủ hoặc mọi lợi ích là audit âm |
| **36. Workflow semantic preflight** | Khớp Kỹ thuật phần mềm, sửa lỗi trước khi tốn compute | Bắt được lỗi thật ngoài nf-schema/nf-core với ít false blocking | Chỉ là schema validation/nhóm rules hiển nhiên đã có |
| **37. Regression sinh học** | Hữu ích cho người duy trì workflow và kết quả nghiên cứu | Phát hiện thay đổi kết luận quan trọng hơn checksum/tolerance | Không có defects thực hoặc tiêu chí sinh học chỉ được dựng theo output cũ |

**Nhóm khác cũng nên xem tùy sở thích:** 24 nếu muốn gần protein mà ít huấn luyện; 18/11 nếu ưu tiên công cụ nhỏ và cần xác lập thêm độ mới; 35/45/50 nếu muốn thuật toán quyết định thí nghiệm; 44 nếu thích khám phá chức năng vi sinh; 14 nếu muốn nối hướng aging. Không loại các nhóm này vì không nằm trong top 10.

### Nhận định về ý nghĩa và độ khớp

- **Đóng góp cho sinh học gần nhất:** 21–25, 31–32, 35, 42–46, 48–50 tạo cách chọn protein, gene, assay hoặc thí nghiệm đáng kiểm hơn. Hầu hết cần chuyên gia/domain truth nhiều hơn nhóm công cụ dữ liệu.
- **Khớp Kỹ thuật phần mềm rõ:** 01–08, 18, 24, 36–40 có contract, algorithm/API và thao tác rà soát làm sản phẩm chính. Muốn luận văn nghiên cứu, vẫn phải chứng minh cải tiến quyết định hoặc độ tin cậy, không đo số màn hình.
- **Gần danh mục GVHD hơn theo đối tượng:** 03, 06–07, 14, 21–25, 35. Đây là suy luận từ [danh mục trong repo](../../advisor/README.md), không là xác nhận thầy nhận hướng dẫn mọi hướng proteomics/engineering. Cùng protein không tự động cùng chuyên môn phương pháp.
- **Tính mới dễ bị nói quá:** split, consensus, uncertainty, active learning, workflow validation, provenance và dashboard đều đã có. Chỉ thay miền hoặc ghép tên công nghệ chưa đủ đóng góp; cần câu hỏi và đối thủ cụ thể.

## 5. Thiết kế khảo sát tiếp để phân biệt ý tưởng tốt với đề tài đứng được

Với một hướng được chọn đọc sâu, lập hồ sơ ngắn gồm **một người dùng, một quyết định cần hỗ trợ, một endpoint và một baseline mạnh**. Đọc toàn văn/phụ lục của 2–3 tiền lệ sát nhất, đối chiếu code và ghi phần tương đương. Nếu baseline đã giải đầy đủ thì hạ hướng đó, không đổi tên phương pháp để cứu novelty.

Khảo sát dữ liệu tiếp theo cần xác minh một accession/benchmark cụ thể: input/output, nhãn là phép đo gì, đơn vị độc lập, số nhóm thực, giấy phép và lỗi metadata. Chỉ sau đó mới thiết kế proof-of-contribution. Không lấy số cell/peptide/window thay cho số donor/protein/study độc lập, không dùng pseudo-label làm ground truth.

Proof-of-contribution phải đối chiếu **cùng dữ liệu, cùng xử lý lõi và cùng ngân sách**. Tách phần lợi ích của thuật toán chọn/sửa khỏi phần baseline mới mạnh hơn. Chọn tham số bằng development/validation, giữ một test phù hợp kịch bản chưa mở. Nếu có inference uncertainty, báo cả calibration và coverage; nếu có giải thích mô hình, kiểm ablation/counterfactual hợp lệ, không lấy đẹp/motif overlap làm fidelity tự động.

Phạm vi app đầu tiên là nhập dữ liệu → kiểm/chọn phương án → rà soát bằng chứng → lưu quyết định → xuất artifact tái lập. Đánh giá chất lượng quyết định bằng benchmark độc lập; tuyên bố tiết kiệm thời gian người dùng chỉ khi có thử nghiệm người dùng. Báo riêng dữ liệu mô phỏng, replay và thực nghiệm sinh học.

## 6. Ghi nhận tra cứu và giới hạn bằng chứng

Tra cứu mới trong phiên này trải rộng: dataset discovery/metadata; DataSAIL/GraphPart; RNA design/enrichment/isoform; scIB/popV/muscat/LIANA/spatial; OpDEA/SCPDA/SIFTS/MaveDB; AMR/CAMI/decontam; CRISPR/Perturb-seq/Cell Painting/active learning; nf-schema/APE/Workflomics/Nextflow/RO-Crate; GIAB/LRGASP/BGC/metabolism; GDC/GWAS/LINCS/time-course. Chỉ dùng bài nghiên cứu, repo tác giả và tài liệu đơn vị sở hữu công cụ làm nguồn kỹ thuật.

| Nhóm bằng chứng đã kiểm | Kết quả kiểm và mức sử dụng |
|---|---|
| DataSAIL — **D** | Đọc phần định nghĩa/giới hạn trên trang bài: framework nhiều loại thực thể và stratification đã có; implementation bài mô tả hỗ trợ 1D/2D. Trang báo addendum 13/02/2026, **chưa đọc addendum**, nên không dùng bài 2025 để kết luận tính năng hiện tại còn thiếu |
| OpenProblems — **D** | Trang task structure có processor, solution/control methods, metrics và workflow; benchmark runner/interfaces không mới |
| OpDEA và SCPDA — **D (repo), S (bài)** | Repo tác giả có phần mềm, tài liệu/code và examples; OpDEA đã là Shiny recommender/analyzer. **Chưa chạy**, không nhận một app chọn workflow là mới |
| nf-schema, Workflomics, Nextflow — **D** | Đã có parameter/sample validation, khám phá/benchmark workflow, đo memory/runtime và cache/resume. Đề xuất 36–39 phải chỉ ra khác biệt ngoài các chức năng này |
| MaveDB assay facts, SIFTS — **D** | Đọc loại endpoint/context và mapping structure–sequence; đề xuất dựa trên hòa giải/uncertainty, không nhận cơ sở dữ liệu hay residue mapping là mới |
| curatedMetagenomicData/muscat — **D** | Tài liệu truy cập/ghép dữ liệu và hỗ trợ multi-sample differential state hiện diện; chưa tự tải/count cohort đủ dùng |
| Perturbation metric calibration — **A** | PubMed ghi ngày **01/10/2026** và abstract về calibration/positive controls. Full text Nature bị lỗi truy cập, nên chưa xác minh chi tiết 14 datasets/18 metrics hoặc code. Không dùng bài 2025 để khẳng định DL luôn kém baseline |
| CLUE — **D** | Trang chủ thông báo retirement từ **31/01/2026**, chuyển public data sang GEO. Chưa tải releases trên GEO |
| Nguồn còn lại — **S** | Đối chiếu kết quả tìm kiếm từ nguồn sơ cấp; chưa đọc toàn văn/phụ lục. Liên kết nguồn giúp đọc sâu, không chứng minh novelty/khả thi |

**Truy cập chưa thành công:** GEO2R và PMC OpDEA gặp CAPTCHA; một số trang Nature OpDEA/SCPDA/scIB/metric calibration gặp lỗi 500/redirect. Dùng tài liệu/repo tác giả hoặc PubMed làm nguồn thay thế ở mức được ghi, không coi lỗi truy cập là không có dữ liệu hay không có công cụ. Không tự tuyên bố đã đọc toàn văn các bài đó.

**Bản 14 ứng viên:** giữ làm tài liệu sàng lọc. Bản này không kế thừa các khẳng định “chưa ai làm”, “benchmark đã giải quyết toàn lĩnh vực”, tỷ lệ leakage từ review chưa audit, hay việc dùng oracle mô hình thay nhãn thực nghiệm. Motif/annotation overlap đo tương hợp sinh học, không tự xác nhận fidelity XAI. Việc kiểm các luận điểm đó là một khảo sát riêng nếu cần dùng làm cơ sở chốt.

## 7. Nguồn sơ cấp để đọc tiếp

**Kiểm tra artifact:** xác nhận đủ 50 mã BIO liên tiếp/không trùng; mỗi mục có bốn trường bài toán, đóng góp, dữ liệu/đánh giá và ứng dụng/điểm chặn. Kiểm 54 định nghĩa nguồn, 119 lượt tham chiếu nguồn và 9 lượt liên kết cục bộ trong báo cáo/các dòng đăng ký mới: đạt. Whitespace của file mới và `git diff --check` scoped: đạt. Đây là kiểm tài liệu, không là kết quả nghiên cứu hoặc kiểm toàn bộ liên kết lịch sử của repo.

54 liên kết nguồn dưới đây gồm bài báo, repo và tài liệu; không phải 54 bài đã đọc toàn văn. Mức D/A chỉ áp cho các trang được nêu ở mục 6; còn lại S. Ngày truy xuất/đối chiếu: **12/10/2026**.

| Nguồn | Nội dung liên quan |
|---|---|
| [S01. DataSAIL, Nature Communications 2025][s01] | Similarity-aware splitting; cần đọc addendum 2026 và code hiện hành |
| [S02. GraphPart, repo tác giả][s02] | Partitioning biological sequences, homology và label balance |
| [S03. OmicsDI][s03] | Discovery across heterogeneous omics resources |
| [S04. MetaSRA, bài nghiên cứu][s04] | Ontology normalization và provenance metadata |
| [S05. GEO2R, NCBI][s05] | Phân tích biểu hiện và caveats thiết kế/dữ liệu |
| [S06. GREIN, Scientific Reports 2019][s06] | Web reanalysis GEO RNA-seq |
| [S07. recount3, Bioconductor][s07] | Truy cập dữ liệu RNA-seq đã xử lý thống nhất |
| [S08. UniProt ID mapping][s08] | Mapping định danh protein |
| [S09. g:Profiler update 2023][s09] | Mapping, enrichment và công cụ web/API |
| [S10. MultiAssayExperiment][s10] | Mapping observations–subjects và tích hợp assays |
| [S11. scIB benchmark, Nature Methods][s11] | Batch removal và biological conservation |
| [S12. OpenProblems task structure][s12] | Benchmark interfaces, controls, metrics |
| [S13. muscat][s13] | Differential state nhiều samples/groups |
| [S14. LIANA+ documentation][s14] | So sánh cell–cell communication |
| [S15. Spatial alignment benchmark 2026][s15] | Tiền lệ căn chỉnh dữ liệu spatial và nguồn dataset |
| [S16. OpDEA, repo tác giả][s16] | Workflow recommendation, analyzer và code benchmark |
| [S17. SCPDA, repo tác giả][s17] | Workflow benchmark DIA single-cell proteomics |
| [S18. PRIDE introduction][s18] | Peptide/protein/PTM, abundance và metadata |
| [S19. SIFTS methodology][s19] | Residue mapping với structure gaps và variants |
| [S20. MaveDB assay facts][s20] | Endpoint, mechanism, model system và calibration metadata |
| [S21. AMRFinderPlus, NCBI][s21] | AMR genes và resistance-associated variants |
| [S22. CAMI FAQ][s22] | Benchmark data, gold standards, formats và download requirements |
| [S23. decontam vignette][s23] | Prevalence/frequency contaminant methods |
| [S24. curatedMetagenomicData vignette][s24] | Truy cập nhiều microbiome studies và metadata |
| [S25. CheckM2, Nature Methods 2023][s25] | Genome completeness/contamination assessment |
| [S26. MAGeCK][s26] | Robust ranking trong CRISPR screens |
| [S27. Systema, Nature Biotechnology][s27] | Perturbation evaluation ngoài systematic variation |
| [S28. Miller et al., PubMed, 01/10/2026][s28] | Positive controls và metric calibration cho perturbation models |
| [S29. Cell Painting Gallery documentation][s29] | Cách duyệt/download images, profiles và metadata |
| [S30. Segment Anything for Microscopy, Nature Methods][s30] | Segmentation và tiền lệ công cụ tương tác |
| [S31. Active learning-assisted directed evolution, 2025][s31] | Batch experiment selection, data/code ALDE |
| [S32. nf-schema][s32] | Parameter/sample sheet validation |
| [S33. nf-core/rnaseq usage][s33] | Samplesheets, preprocessing/QC và pipeline |
| [S34. Workflomics documentation][s34] | Workflow generation, runtime và scientific benchmarking |
| [S35. Nextflow caching/resuming][s35] | Hash, dependencies và resume semantics |
| [S36. Workflow RO-Crate][s36] | Chuẩn bundle và liên kết Workflow Run Crate |
| [S37. Genome in a Bottle, NIST][s37] | Benchmark variants/regions và stratifications |
| [S38. LRGASP, Nature Methods 2024][s38] | Transcript identification/quantification benchmark |
| [S39. antiSMASH ClusterCompare][s39] | So BGC với MIBiG và nguồn comparisons |
| [S40. gapseq, Genome Biology 2021][s40] | Metabolic reconstruction, gap-fill và phenotype validation |
| [S41. BioNERO][s41] | Coexpression/regulatory network tooling |
| [S42. TCGA clinical data resource, NCI GDC][s42] | Survival endpoints và clinical resource |
| [S43. CLUE announcement][s43] | Retirement và public data trên GEO |
| [S44. GWAS summary statistics documentation][s44] | Data access, validation/harmonization context |
| [S45. RNA-seq Bioconductor workflow][s45] | Designs/contrasts/time course và fission example |
| [S46. SenMayo, Nature Communications 2022][s46] | Senescence signature và context validation |
| [S47. IsoformSwitchAnalyzeR vignette][s47] | Isoform switching và functional consequences |
| [S48. Ensembl homology types][s48] | One-to-one, one-to-many và many-to-many |
| [S49. popV, Nature Genetics 2024][s49] | Consensus cell annotation |
| [S50. EPIFANY][s50] | Protein inference và iPRG ground truth context |
| [S51. multiverse package][s51] | Branching analysis choices và execution |
| [S52. EnrichmentMap/g:Profiler protocol][s52] | Pathway enrichment interpretation/visualization |
| [S53. GeneFEAST, tác giả preprint][s53] | Gene-centric summarization of enrichment |
| [S54. PRIDE SDRF Validator][s54] | Community-template metadata validation đã có |

[s01]: https://www.nature.com/articles/s41467-025-58606-8
[s02]: https://github.com/graph-part/graph-part
[s03]: https://www.omicsdi.org/
[s04]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5870770/
[s05]: https://www.ncbi.nlm.nih.gov/geo/info/geo2r.html
[s06]: https://www.nature.com/articles/s41598-019-43935-8
[s07]: https://bioconductor.org/packages/release/bioc/html/recount3.html
[s08]: https://www.uniprot.org/help/id_mapping
[s09]: https://academic.oup.com/nar/article/51/W1/W207/7152869
[s10]: https://bioconductor.org/packages/release/bioc/vignettes/MultiAssayExperiment/inst/doc/MultiAssayExperiment_cheatsheet.html
[s11]: https://www.nature.com/articles/s41592-021-01336-8
[s12]: https://www.openproblems.bio/documentation/reference/task-structure/
[s13]: https://www.bioconductor.org/packages/release/bioc/html/muscat.html
[s14]: https://liana.readthedocs.io/en/stable/tutorials/notebooks/liana_pyCrossTalkeR.html
[s15]: https://www.nature.com/articles/s43588-026-00977-z
[s16]: https://github.com/PennHui2016/OpDEA
[s17]: https://github.com/WangJianwei1991/SCPDA
[s18]: https://www.ebi.ac.uk/training/online/course/pride-quick-tour/what-pride-1
[s19]: https://www.ebi.ac.uk/pdbe/docs/sifts/methodology.html
[s20]: https://mavedb.org/docs/mavedb/reference/assay-facts.html
[s21]: https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/
[s22]: https://cami-challenge.org/faq/
[s23]: https://bioconductor.org/packages/release/bioc/vignettes/decontam/inst/doc/decontam_intro.html
[s24]: https://bioconductor.org/packages/release/data/experiment/vignettes/curatedMetagenomicData/inst/doc/curatedMetagenomicData.html
[s25]: https://www.nature.com/articles/s41592-023-01940-w
[s26]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4290824/
[s27]: https://www.nature.com/articles/s41587-025-02777-8
[s28]: https://pubmed.ncbi.nlm.nih.gov/42823510/
[s29]: https://broadinstitute.github.io/cellpainting-gallery/browsing_data.html
[s30]: https://www.nature.com/articles/s41592-024-02580-4
[s31]: https://www.nature.com/articles/s41467-025-55987-8
[s32]: https://github.com/nextflow-io/nf-schema
[s33]: https://nf-co.re/rnaseq/latest/docs/usage/
[s34]: https://workflomics.readthedocs.io/en/latest/user-guide/web-interface.html
[s35]: https://docs.seqera.io/nextflow/cache-and-resume
[s36]: https://about.workflowhub.eu/Workflow-RO-Crate/1.1/
[s37]: https://www.nist.gov/programs-projects/genome-bottle
[s38]: https://www.nature.com/articles/s41592-024-02298-3
[s39]: https://docs.antismash.secondarymetabolites.org/modules/cluster_compare/
[s40]: https://link.springer.com/article/10.1186/s13059-021-02295-1
[s41]: https://bioconductor.org/packages/release/bioc/html/BioNERO.html
[s42]: https://gdc.cancer.gov/about-data/publications/PanCan-Clinical-2018
[s43]: https://clue.io/
[s44]: https://www.ebi.ac.uk/gwas/docs/methods/summary-statistics/
[s45]: https://www.bioconductor.org/packages/devel/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html
[s46]: https://www.nature.com/articles/s41467-022-32552-1
[s47]: https://www.bioconductor.org/packages/release/bioc/vignettes/IsoformSwitchAnalyzeR/inst/doc/IsoformSwitchAnalyzeR.html
[s48]: https://static.ensembl.org/info/genome/compara/homology_types.html
[s49]: https://www.nature.com/articles/s41588-024-01993-3
[s50]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7583457/
[s51]: https://mucollective.github.io/multiverse/
[s52]: https://www.nature.com/articles/s41596-018-0103-9
[s53]: https://arxiv.org/abs/2309.00061
[s54]: https://www.ebi.ac.uk/pride/services/sdrf-validator
