# Ba ý tưởng đề tài tin sinh để trao đổi với GVHD

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../DECISIONS.md).

> **Mục đích:** so sánh các hướng nghiên cứu có thể làm thành sản phẩm minh họa trong khoảng 14 tuần. Đây là tài liệu chuẩn bị thảo luận, chưa phải đề cương và chưa chốt hướng nào. Bản này dành cho người mới bắt đầu tin sinh; số liệu dưới đây chỉ được nêu khi có thể đối chiếu với bài báo hoặc kho mã nguồn được dẫn.
>
> **Bối cảnh mặc định:** một người thực hiện, máy cá nhân chủ yếu dùng CPU, GPU miễn phí khi có thể. Thời gian và quota GPU thực tế chưa được xác nhận.

## Cách đọc thông tin

- **Đã xác minh:** được ghi trong bài báo hoặc dữ liệu / README của kho được liên kết.
- **Đề xuất:** câu hỏi, quy trình và sản phẩm nghiên cứu dự kiến; chưa phải kết quả.
- **Cần hỏi / kiểm tra:** dữ liệu, quyền sử dụng, khả năng tái lập hoặc lựa chọn khoa học còn thiếu bằng chứng.

## Một vài thuật ngữ trước khi so sánh

- **Protein** là chuỗi các axit amin. Mỗi axit amin trong chuỗi còn được gọi là một **residue**; với bài toán dự đoán vị trí gắn, mô hình gán điểm cho từng vị trí.
- **FASTA** là định dạng văn bản đơn giản thường dùng để lưu chuỗi protein. Một bản ghi có dòng tên bắt đầu bằng `>` rồi đến chuỗi axit amin.
- **PLM** (protein language model) học biểu diễn số (*embedding*) từ chuỗi protein, tương tự cách mô hình ngôn ngữ biểu diễn từ và câu. Embedding theo từng residue giữ thông tin cho mỗi vị trí; embedding toàn chuỗi tóm tắt cả protein.
- **CNN** nhận các đoạn lân cận trong embedding để học mẫu cục bộ. **mCNN / MCNN** áp dụng nhiều kích thước cửa sổ, giúp nhìn các mẫu ngắn và dài khác nhau.
- Trong các bài của nhóm đang xét, **RAG thường là truy hồi embedding protein gần với mẫu đầu vào rồi trộn thông tin embedding** trước khi phân loại. Tên này không đồng nghĩa với hệ thống hỏi đáp tạo văn bản bằng LLM: mô hình dự đoán nhãn hoặc điểm, không viết câu trả lời sinh học.
- **Validation** là tập dùng để chọn cấu hình/ngưỡng; **test** là tập giữ riêng để chấm điểm cuối cùng. Không dùng test để chọn ngưỡng hoặc điều chỉnh mô hình.
- **AUPRC** tóm tắt độ chính xác của các dự đoán dương và khả năng tìm đủ mẫu dương qua nhiều ngưỡng; hữu ích khi mẫu dương hiếm. **MCC** cân nhắc cả dự đoán đúng lẫn sai ở hai lớp; **F1** cân bằng precision và recall tại một ngưỡng. Với nhiều lớp, macro-F1 tính F1 từng lớp rồi lấy trung bình để lớp hiếm không bị lớp phổ biến lấn át.
- **Độ đồng dạng chuỗi** là tỷ lệ axit amin giống nhau sau khi căn chỉnh hai chuỗi; dùng để tránh train và test có protein gần như trùng nhau. **PSSM** là bảng điểm theo vị trí rút ra từ so sánh với các chuỗi họ hàng, nhằm biểu diễn thông tin tiến hóa.

## 1. Dự đoán và trực quan hóa vị trí gắn ATP

### Vấn đề sinh học và nghiên cứu nền

ATP là phân tử mang năng lượng và tham gia nhiều phản ứng của protein. Dự đoán residue nào trong protein kinase gắn ATP có thể giúp nghiên cứu chức năng protein và khảo sát vùng đích của thuốc. Hướng hẹp ở đây là **receptor tyrosine kinases (RTK)**, một họ kinase có liên quan đến truyền tín hiệu tế bào.

**Đã xác minh:** bài [RTK_RAG](https://pubmed.ncbi.nlm.nih.gov/40531492/) kết hợp protein language model, truy hồi và mạng tích chập nhiều cửa sổ để dự đoán residue gắn ATP của RTK. README của [kho RTK_RAG](https://github.com/B1607/RTK_RAG) liệt kê ATP-549 gồm 549 protein dùng huấn luyện, 69 protein RTK làm kiểm tra độc lập, và 244 protein trong kho truy hồi. README liệt kê ở tập RTK độc lập 711 residue gắn và 73.270 residue không gắn. Các con số này mô tả đúng bộ dữ liệu của repo, chưa chứng minh đánh giá mới sẽ tổng quát sang protein kinase khác.

### Phần kế thừa và đề xuất

- **Kế thừa:** dùng biểu diễn protein của PLM và mCNN; có đối chứng với/không có truy hồi; trả điểm dự đoán cho từng residue.
- **Đề xuất đóng góp:** đo xem truy hồi cải thiện dự đoán bao nhiêu khi truy vấn và kho tham chiếu được tách chặt; kiểm tra lợi ích theo độ tương đồng tới protein huấn luyện. Đây là mở rộng có kiểm soát, chưa tuyên bố là hướng đầu tiên hay chắc chắn tốt hơn bài gốc.
- **Câu hỏi nghiên cứu 1:** so với cùng PLM + mCNN không truy hồi, thêm truy hồi làm thay đổi AUPRC và MCC bao nhiêu trên protein chưa dùng khi huấn luyện?
- **Câu hỏi nghiên cứu 2:** mức lợi hoặc suy giảm của truy hồi thay đổi ra sao giữa protein có láng giềng gần và protein ít tương đồng? Một quy tắc bỏ qua truy hồi khi không tìm được láng giềng đủ gần có cải thiện độ tin cậy không?

### Dữ liệu, phương pháp và sản phẩm tối thiểu

- **Dữ liệu:** bắt đầu bằng FASTA và nhãn theo residue của RTK_RAG. Tập độc lập 69 protein là điểm xuất phát; cần kiểm tra độ trùng, độ tương đồng giữa tập kiểm tra, tập huấn luyện và kho truy hồi trước khi dùng. Cần hỏi liệu GVHD có bộ dữ liệu RTK bổ sung hoặc cho phép dùng bộ ngoài nhóm để xác nhận kết quả.
- **Luồng xử lý:** FASTA → embedding theo residue từ PLM → mCNN, có hoặc không có embedding truy hồi → điểm gắn ATP theo residue → hiển thị chuỗi với residue được tô màu. Bảng kết quả cũng hiển thị các protein tham chiếu gần nhất và độ tương đồng của chúng; không trình bày điểm mô hình như xác nhận thực nghiệm hay khuyến nghị điều trị.
- **Sản phẩm tối thiểu:** trang web nhận một hay nhiều chuỗi FASTA, kiểm tra định dạng, hiển thị chuỗi amino acid được tô màu theo điểm dự đoán, tải kết quả bảng xuống và xem tối đa vài chuỗi tham chiếu. Không cần dựng mô hình 3D.
- **Đánh giá:** AUPRC là chỉ số chính ở mức residue; MCC/F1 là chỉ số bổ sung tại ngưỡng chọn trên validation. So sánh cùng một cách chia dữ liệu cho mô hình không truy hồi và có truy hồi; báo kết quả theo mức đồng dạng và nhiều lần khởi tạo khi ngân sách cho phép. Với tập nhỏ, tính khoảng bất định bằng cách lấy mẫu lại theo protein, không coi mọi residue là quan sát độc lập. Tập test giữ nguyên, kho truy hồi không được chứa test. Kiểm tra lọc đồng dạng bằng một công cụ căn chỉnh phù hợp và báo rõ ngưỡng thực tế.
- **Khả thi:** trung bình. Repo có dữ liệu/nhãn và hướng dẫn demo Colab, nhưng trọng số mô hình và embedding không nằm sẵn trong repo theo ghi chú khảo sát. Việc tái lập PLM và lấy embedding có thể tốn GPU, thời gian và dung lượng.
- **Rủi ro / điểm dừng:** chỉ 69 protein kiểm tra độc lập và số residue dương thấp so với âm; khoảng bất định có thể lớn. Nếu đến cuối tuần 2 chưa dựng được baseline, lấy được trọng số mô hình, hoặc không xác lập được tập test tách khỏi kho truy hồi, dừng tuyên bố nghiên cứu về lợi ích RAG; chuyển trọng tâm sang demo tái lập có ghi rõ giới hạn, hoặc chọn hướng IL-6.

### Lịch dự kiến 14 tuần

| Tuần | Việc chính |
|---|---|
| 1–2 | Đọc lại bài và repo; kiểm tra nhãn, weights, quyền dùng dữ liệu, trùng lặp/đồng dạng; chạy thử pipeline trên một mẫu nhỏ. **Cổng quyết định:** xác nhận có thể dựng baseline và tập kiểm tra hợp lệ. |
| 3–5 | Dựng pipeline embedding và baseline PLM + mCNN không truy hồi; khóa cách chia train/validation/test. |
| 6–8 | Thêm đúng một nhánh truy hồi; so sánh có/không truy hồi và phân tích theo độ tương đồng. |
| 9–11 | Hoàn thiện đánh giá, bảng và biểu đồ; xây giao diện FASTA → bản đồ residue từ mô hình đã huấn luyện. |
| 12–14 | Kiểm tra demo, ghi giới hạn và kết quả; hoàn thiện báo cáo và slide trao đổi/bảo vệ. |

## 2. Sàng lọc peptide có khả năng kích thích IL-6

### Vấn đề sinh học và nghiên cứu nền

IL-6 là cytokine liên quan đến điều hòa miễn dịch và viêm. Hướng này dự đoán peptide nào có thể kích thích tạo IL-6, nhằm sàng lọc danh sách peptide cho bước nghiên cứu tiếp theo. Mô hình chỉ phân loại dữ liệu đã gán nhãn; nó không xác nhận một peptide sẽ gây ra đáp ứng sinh học trong thí nghiệm.

**Đã xác minh:** [bài RAG_MCNNIL6](https://pubmed.ncbi.nlm.nih.gov/39967508/) và [kho mã nguồn](https://github.com/B1607/RAG_MCNNIL6) mô tả pipeline ProtTrans + truy hồi tương đồng + MCNN. README liệt kê 2.685 mẫu huấn luyện (292 dương), 671 mẫu validation (73 dương), và kho truy hồi 9.892 chuỗi (513 dương). README có demo Colab nhận FASTA và xuất nhãn peptide.

**Giới hạn đã thấy:** số liệu README mới xác nhận train, validation và kho truy hồi; chưa đủ căn cứ để gọi validation là test độc lập. Cần tìm bộ kiểm tra ngoài hoặc thiết kế chia cụm protein/peptide trước khi phát biểu khả năng tổng quát. Một nghiên cứu IL-6 mới hơn, [CONTRA-IL6 (2026)](https://pubmed.ncbi.nlm.nih.gov/42281397/), cũng kết hợp biểu diễn PLM với Transformer/CNN và báo cáo kiểm tra trên bộ độc lập; vì vậy cần rà soát tài liệu mới trước khi chốt tính mới.

### Phần kế thừa và đề xuất

- **Kế thừa:** peptide ngắn, biểu diễn PLM, bộ phân loại nhiều cửa sổ và nhánh truy hồi embedding.
- **Đề xuất đóng góp:** đánh giá công bằng phần truy hồi bằng đối chứng cùng dữ liệu/seed, kiểm tra ảnh hưởng của peptide tương tự trong kho tham chiếu. Có thể làm demo sàng lọc hàng loạt nhẹ hơn hệ thống phân tích protein dài.
- **Câu hỏi nghiên cứu 1:** trên tập kiểm tra được tách theo cụm tương đồng, mô hình có truy hồi thay đổi AUPRC và MCC bao nhiêu so với cùng mô hình không truy hồi?
- **Câu hỏi nghiên cứu 2:** tác dụng của truy hồi có tập trung ở peptide có láng giềng gần trong kho tham chiếu không, và có giảm rõ trên peptide ít tương đồng không?

### Dữ liệu, phương pháp và sản phẩm tối thiểu

- **Dữ liệu:** bắt đầu từ tập train/validation trong repo RAG_MCNNIL6. Tuần 1–2 kiểm tra định dạng nhãn, chuỗi trùng và căn chỉnh giữa train, validation và kho truy hồi. Tìm bộ ngoài có quyền dùng; nếu không có, tạo phép chia theo cụm tương đồng từ dữ liệu có sẵn và ghi rõ đây chưa phải kiểm chứng độc lập bên ngoài.
- **Luồng xử lý:** FASTA nhiều bản ghi → biểu diễn PLM cho từng peptide → MCNN không truy hồi hoặc cộng/trộn embedding của peptide gần → xác suất lớp → bảng xếp hạng và danh sách chuỗi tham chiếu.
- **Sản phẩm tối thiểu:** nhập/tải lên nhiều peptide FASTA/CSV, nhận điểm xác suất và nhãn ở ngưỡng đã chọn, lọc/sắp theo điểm và xem vài mẫu truy hồi. Giao diện gọi mô hình đã huấn luyện; không cần đưa LLM sinh văn bản vào hệ thống.
- **Đánh giá:** AUPRC chính vì nhãn dương chiếm tỷ lệ nhỏ trong các bảng dữ liệu đã công bố; MCC/F1 bổ sung. Chọn ngưỡng trên validation, khóa trước khi chấm test. Chia theo cụm đồng dạng để peptide gần như giống nhau không rơi vào hai phía. Kiểm tra kho truy hồi không lấy chuỗi/nhãn từ test.
- **Khả thi:** trung bình đến khá nếu dữ liệu đủ dùng và weights tái lập được; peptide ngắn làm sản phẩm trình diễn gọn. Tuy nhiên pipeline vẫn cần PLM và GPU lúc tạo embedding. Việc tìm tập độc lập và quyền sử dụng dữ liệu là điều kiện quan trọng.
- **Rủi ro / điểm dừng:** nhãn “có khả năng kích thích” phụ thuộc phép đo thí nghiệm và không có nghĩa mọi peptide tương tự đều gây đáp ứng. Nếu không tìm được test ngoài hoặc phép chia theo cụm làm số mẫu dương quá ít, thu hẹp kết luận thành so sánh có kiểm soát trên bộ chuẩn hiện có; không tuyên bố dùng được để phát triển vaccine.

### Lịch dự kiến 14 tuần

| Tuần | Việc chính |
|---|---|
| 1–2 | Kiểm tra dataset, nhãn, giấy phép, overlap và khả năng tái lập; tìm/thiết kế test theo cụm. **Cổng quyết định:** số dương còn đủ cho validation và test có ý nghĩa. |
| 3–5 | Dựng baseline peptide PLM + MCNN không truy hồi và xác nhận metric. |
| 6–8 | Thêm truy hồi embedding; so sánh có/không truy hồi và phân tích theo độ tương đồng. |
| 9–11 | Làm trang sàng lọc nhiều peptide, lịch sử kết quả trong phiên và tải CSV. |
| 12–14 | Hoàn thiện đánh giá, kiểm tra đầu vào và báo cáo giới hạn, viết báo cáo/slide. |

## 3. Phân loại protein efflux và các họ chức năng

### Vấn đề sinh học và nghiên cứu nền

Protein efflux giúp tế bào đưa một số chất ra ngoài; một số hệ vận chuyển liên quan đến khả năng kháng thuốc của vi khuẩn. Dự đoán protein thuộc họ vận chuyển nào giúp sàng lọc trình tự cho bước chú giải tiếp theo.

**Đã xác minh:** bài [mCNN-GenEfflux](https://pubmed.ncbi.nlm.nih.gov/40690811/) của nhóm Ho–Ou kết hợp chuỗi do ProtGPT2 tạo, đặc trưng PSSM và mCNN để nhận dạng protein efflux/họ của chúng; trang [bài báo của nhà xuất bản](https://www.sciencedirect.com/science/article/pii/S1476927125002567) mô tả hướng xử lý mất cân bằng lớp và giải thích UMAP/Grad-CAM. Bài nền [DeepEfflux](https://academic.oup.com/bioinformatics/article/34/18/3111/4970514) ghi nhận dữ liệu các họ rất lệch: sau lọc đồng dạng dưới 20%, lớp SMR chỉ có 5 chuỗi, trong đó 4 train và 1 test; các lớp khác cũng khác nhau nhiều về số lượng.

**Cần kiểm tra:** báo cáo khảo sát trong repo chưa tìm được bảng công khai xác nhận dữ liệu/chuỗi sinh của GenEfflux hoặc quyền sử dụng. Không dùng các số liệu kết quả nổi bật của bài GenEfflux làm mục tiêu hay giả định có thể tái lập cho đến khi xác nhận được dữ liệu và giao thức.

### Phần kế thừa và đề xuất

- **Kế thừa:** PLM/mCNN cho mẫu cục bộ ở nhiều kích thước cửa sổ; bài toán phân loại protein theo họ; ProtGPT2 là một phương án tăng cường dữ liệu đã có tiền lệ trong nhóm.
- **Đề xuất đóng góp:** so sánh baseline mCNN với cách gán trọng số lớp (tăng mức phạt cho lỗi ở họ hiếm) và, nếu có đủ dữ liệu/chuỗi sinh hợp lệ, thêm một nhánh tăng cường dữ liệu sinh. Trọng tâm là báo cáo chất lượng từng họ hiếm, không chỉ độ chính xác chung.
- **Câu hỏi nghiên cứu 1:** class weighting có cải thiện macro-F1/MCC và recall của họ hiếm so với baseline mCNN không, trong khi giảm bao nhiêu hiệu năng ở họ phổ biến?
- **Câu hỏi nghiên cứu 2:** nếu lấy được chuỗi ProtGPT2 và curation tương ứng, thêm chuỗi sinh có cải thiện kết quả trên họ hiếm hơn class weighting không, khi tập test giữ nguyên hoàn toàn?

### Dữ liệu, phương pháp và sản phẩm tối thiểu

- **Dữ liệu:** bắt đầu bằng cách xin bộ dữ liệu và giao thức chia của GenEfflux từ GVHD; song song kiểm tra khả năng tái tạo tập DeepEfflux từ bài gốc. Trước khi huấn luyện phải xác nhận đủ số chuỗi cho mỗi họ, nhãn, cách nhóm thành lớp và quyền dùng. Nếu chỉ có 1–2 mẫu của một họ trong test, không kết luận hiệu quả cho họ đó.
- **Luồng xử lý:** FASTA → PLM embedding và mCNN → điểm từng họ; so sánh baseline với class weighting. Chỉ thêm nhánh ProtGPT2 nếu chuỗi sinh và quy trình kiểm soát chất lượng (trùng/đồng dạng với test, tính hợp lệ chiều dài/chuỗi) có thể tái lập trong ngân sách.
- **Sản phẩm tối thiểu:** tải FASTA, xem họ dự đoán và điểm của từng lớp, các lớp cạnh tranh, cảnh báo khi điểm không đủ phân biệt và bảng thống kê chuỗi. Không diễn giải kết quả thành bằng chứng lâm sàng về kháng kháng sinh.
- **Đánh giá:** macro-F1, MCC và precision/recall theo từng lớp; AUPRC kiểu “mỗi lần xem một lớp là lớp dương” nếu đủ mẫu. Dùng phép chia theo protein và độ đồng dạng, giữ test bất biến giữa các cách so sánh; báo khoảng bất định. Không dùng chuỗi sinh gần test để huấn luyện.
- **Khả thi:** thấp hơn hai hướng kia. Dữ liệu họ thiểu số cực ít trong bộ DeepEfflux đã công bố; GenEfflux dùng thêm sinh dữ liệu và PSSM, làm tăng công sức, tính toán và kiểm soát rò rỉ.
- **Rủi ro / điểm dừng:** nếu GVHD không thể cung cấp/giới thiệu dữ liệu GenEfflux và không dựng được bộ DeepEfflux có phép chia đủ mẫu cho đánh giá trước cuối tuần 2, bỏ nhánh này. Nếu dữ liệu đủ cho baseline nhưng không đủ cho tăng cường sinh, giữ class-weighting làm RQ1 và biến RQ2 thành đo độ ổn định theo lần chia/seed; ghi rõ phạm vi đóng góp nhỏ hơn.

### Lịch dự kiến 14 tuần

| Tuần | Việc chính |
|---|---|
| 1–2 | Xin/kiểm tra dataset, nhãn, license, chia tập và số mẫu mỗi họ. **Cổng quyết định:** xác nhận có tập đánh giá đủ để đo họ hiếm; quyết định giữ hay bỏ nhánh dữ liệu sinh. |
| 3–5 | Làm baseline mCNN và class weights; khóa tập test và báo cáo theo từng lớp. |
| 6–8 | Nếu đủ điều kiện, thêm chuỗi sinh đã lọc và so sánh với class weighting; nếu chưa, dùng thời gian này đánh giá độ ổn định. |
| 9–11 | Làm công cụ FASTA, bảng điểm theo họ và cảnh báo độ tin cậy. |
| 12–14 | Kiểm tra demo, tổng hợp sai số từng họ, nêu giới hạn dữ liệu và hoàn thiện báo cáo/slide. |

## So sánh nhanh

| Hướng | Mức phù hợp với 14 tuần* | Dữ liệu đã thấy | Câu hỏi nghiên cứu | Sản phẩm minh họa | Rủi ro chính |
|---|---|---|---|---|---|
| Vị trí gắn ATP ở RTK | Trung bình | Repo có FASTA/nhãn và tập RTK độc lập 69 protein; cần audit đồng dạng và weights | Đóng góp của truy hồi và độ nhạy theo tương đồng | Chuỗi protein tô màu theo residue, tham chiếu gần nhất | Test nhỏ, mất cân bằng rất cao, GPU/weights |
| Peptide kích thích IL-6 | Trung bình–khá nếu hoàn tất kiểm tra tập | Repo có train/validation và kho truy hồi; test độc lập cần xác nhận | Đóng góp truy hồi và phụ thuộc vào peptide gần | Sàng lọc, xếp hạng nhiều peptide | Nguy cơ overlap và thiếu test độc lập; nhãn sinh học phụ thuộc assay |
| Họ protein efflux | Thấp–trung bình | Bài gốc có mô tả lớp nhưng lớp hiếm quá nhỏ; GenEfflux data cần hỏi | Class weighting; thêm dữ liệu sinh nếu khả thi | FASTA → điểm theo họ | Dữ liệu thiếu/lớp hiếm, PSSM và tạo chuỗi tốn công |

\* Đây là **ước lượng định tính để chọn hướng cần hỏi tiếp**, không phải cam kết về số giờ GPU. Dù là hướng nào, tuần 1–2 cần chứng minh có thể tái lập ít nhất một baseline và dựng phép chia đánh giá không rò rỉ.

## Nhận định để mang vào buổi gặp

**Ưu tiên đem ATP và IL-6 làm hai lựa chọn chính để GVHD phản biện.** ATP có đầu ra trực quan nhất: người xem nhìn được điểm dự đoán theo từng vị trí trên chuỗi, và có repo kèm dữ liệu/demo. Đổi lại, 69 protein độc lập cùng tỷ lệ residue dương thấp khiến độ chắc của kết luận nghiên cứu cần được xử lý cẩn thận. IL-6 có luồng demo nhiều peptide dễ hiểu và dữ liệu được liệt kê rõ trong README; điểm phải làm rõ trước khi chốt là một tập test độc lập, phép chia theo tương đồng và ranh giới với nghiên cứu mới.

Để đặt câu hỏi có ý nghĩa khoa học, sản phẩm web nên là **cách minh họa một pipeline đo được**, không thay cho đóng góp nghiên cứu. Dùng cùng PLM/mCNN ở các đối chứng, chỉ bật/tắt module truy hồi hoặc thay đúng một cách xử lý dữ liệu; báo cáo AUPRC cùng MCC/F1, theo từng lớp khi phù hợp. Không tìm ngưỡng trên test; không cho protein tương đồng quá gần giữa train, validation, test và kho tham chiếu; ghi rõ nguồn và phiên bản dữ liệu.

Efflux phù hợp làm phương án thứ ba nếu GVHD chia sẻ được bộ dữ liệu đã tuyển chọn của GenEfflux. Với một người, 14 tuần và GPU miễn phí, hiện chưa nên cam kết nhánh tạo protein mới trước khi có dữ liệu, trọng số mô hình, quy trình PSSM và số mẫu từng họ.

## Câu hỏi cần mang hỏi GVHD

1. Trong ba bài toán này, bài nào phù hợp hơn với hướng nghiên cứu đang làm và thời gian một học kỳ?
2. Thầy/cô có thể chia sẻ dữ liệu, nhãn, weights và cách chia tập nào; có giới hạn nào khi dùng hoặc đưa dữ liệu vào demo/báo cáo không?
3. Với ATP/IL-6, nhóm có benchmark ngoài hoặc phép chia theo độ tương đồng để kiểm chứng độc lập không? Có thể dùng thêm dữ liệu ngoài nhóm chứ?
4. Thầy/cô muốn phần nghiên cứu tập trung vào phép truy hồi, kiểm soát đồng dạng/mất cân bằng, hay khả năng giải thích đầu ra?
5. Với lớp rất hiếm như SMR, có đủ dữ liệu để đặt câu hỏi so sánh sinh dữ liệu hay nên chọn một bài toán khác?
6. Quy mô sản phẩm nào là vừa: demo chạy notebook/Colab hay một trang web có tải FASTA và tải kết quả xuống?
7. Nguồn GPU và thời gian chạy thực tế nào có thể dùng trong 14 tuần? Có máy/phòng lab hoặc quota Colab/Kaggle nào đã được xác nhận?

## Nguồn để đọc tiếp

- **ATP / RTK:** [bài báo RTK_RAG trên PubMed](https://pubmed.ncbi.nlm.nih.gov/40531492/) · [repo và dataset README](https://github.com/B1607/RTK_RAG)
- **IL-6:** [bài báo RAG_MCNNIL6 trên PubMed](https://pubmed.ncbi.nlm.nih.gov/39967508/) · [repo, bảng dữ liệu và demo](https://github.com/B1607/RAG_MCNNIL6) · [CONTRA-IL6 (2026)](https://pubmed.ncbi.nlm.nih.gov/42281397/)
- **Efflux:** [mCNN-GenEfflux trên PubMed](https://pubmed.ncbi.nlm.nih.gov/40690811/) · [toàn văn/trang nhà xuất bản](https://www.sciencedirect.com/science/article/pii/S1476927125002567) · [bài DeepEfflux và dữ liệu gốc](https://academic.oup.com/bioinformatics/article/34/18/3111/4970514)
- Khảo sát tổng hợp và ghi chú xác minh nội bộ: `archive/surveys/bioinformatics-topic-survey/bioinformatics-topic-survey.md`, `archive/surveys/bioinformatics-topic-survey/rag-mscnn-verification.md`.
