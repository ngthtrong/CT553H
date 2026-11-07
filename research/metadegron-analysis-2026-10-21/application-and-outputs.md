# Ứng dụng và đầu ra

[NGUỒN] Tác giả hướng MetaDegron tới người nghiên cứu điều hòa protein, E3–degron và ứng dụng cancer/drug discovery. Đây là mục đích công bố, không phải kết quả chứng minh có ích lâm sàng. [Bài báo](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/), [Tutorial](http://modinfor.com/MetaDegron/Tutorial.php).

| Chức năng | Điều đã kiểm | Mức bằng chứng |
|---|---|---|
| Đầu vào | Job ID, chọn một/nhiều E3, một/nhiều chuỗi FASTA; header có thể mang accession | [ĐỌC-MÃ] `Prediction.php`, `Degron_prediction.py`; không thấy workflow chỉ nhập ID rồi tự tải sequence |
| Batch và giới hạn | JS `limit=20` là giới hạn **E3 được chọn**, không phải 20 chuỗi; chưa xác nhận cap độ dài/số FASTA | [ĐỌC-MÃ] `Prediction.php`; [CHƯA XÁC MINH] giới hạn vận hành server |
| Candidate | Quét regex motif của E3; trích cửa sổ quanh hit và chấm classifier dùng chung | [ĐỌC-MÃ] Prediction source, [code-audit.json](code-audit.json) |
| Score | Xác suất nhị phân từ sigmoid hoặc predict_proba; không phải ΔPSI, thời gian bán hủy, xác suất E3 riêng đã hiệu chuẩn | [ĐỌC-MÃ] Builder/prediction; [CHƯA XÁC MINH] hiệu chuẩn thực tế |
| Bảng kết quả | Entry, E3 ligase, Degron instance, Degron type, Start, End, Score; code còn có cờ ID_in_UniProt | [ĐỌC-MÃ] TSV `prediction.txt`; [NGUỒN] ảnh Tutorial |
| File xuất | TSV prediction.txt và prediction_properties.txt; giao diện có link ZIP công việc | [ĐỌC-MÃ] Prediction/result source; [CHƯA XÁC MINH] ZIP live sau job chưa thử |
| Ngưỡng | Source xuất các candidate cùng score rồi sắp hạng; chưa thấy cutoff mặc định để lọc toàn cục | [ĐỌC-MÃ] Phần ghi prediction; không suy ra 0,5 là ngưỡng vận hành |
| Cấu trúc/MSA | 3Dmol.js, link PDB/RCSB; ProViz cho alignment | [ĐỌC-MÃ] `Degron.php`; không có căn cứ gắn mặc định nguồn AlphaFold |
| Mạng | Có Cytoscape.js và bảng E3/DUB | [ĐỌC-MÃ]/[NGUỒN] Web source và bài; [CHƯA XÁC MINH] nguồn cạnh mạng, không gọi nó là STRING chỉ vì dùng Cytoscape |
| Giải thích | Annotation thuộc tính và motif; paper có feature ablation | [ĐỌC-MÃ]/[NGUỒN] Chưa xác nhận attention/SHAP theo query hoặc calibration plot |
| Lưu kết quả | Source giao diện nói giữ job 30 ngày | [ĐỌC-MÃ] `result.php`; [CHƯA XÁC MINH] chính sách server đang thực thi |

[ĐO] Đã tải và xem ảnh Output.png sẵn có của Tutorial, không gửi chuỗi: [ảnh nguồn](http://modinfor.com/MetaDegron/images/Output.png), bản cục bộ `data/raw/metadegron/demo-output.png`. Ảnh minh họa bảng candidate CDC20/FBXW7 có nhiều score cho các motif khác nhau trên cùng protein. Bản tải/hash và số lần submit bằng0 trong [source-manifest.json](source-manifest.json). Ảnh không được sao chép vào phần đưa lên git do quyền tài sản web chưa rõ.

[DIỄN GIẢI] MetaDegron trả lời “motif ứng viên nào tương thích tập motif của E3 được chọn và có đặc trưng giống degron curate?”. Đề tài trả lời “thay acid amin nào tại vị trí nào làm reporter ổn định hơn bao nhiêu?”. Score theo hit có tọa độ chưa phải bản đồ hiệu ứng của từng thay thế. Hai câu hỏi bổ sung nhau.

[ĐỀ XUẤT] Có thể ánh xạ qua một **thí nghiệm** in-silico: giữ cửa sổ/tọa độ WT, sinh mutant, tính `ΔScore(mutant−WT)`, dùng `−ΔScore` để xếp hạng phá degron so với ΔPSI dương. Cần báo abstention khi không có candidate, cùng khả năng áp dụng, và giữ riêng thay đổi regex với thay đổi classifier. Quét cửa sổ đơn thuần đo mức ứng viên đoạn; không biến nó thành mutation prediction đã được thực nghiệm xác nhận. [PREREGISTRATION.md](PREREGISTRATION.md).

| Giá trị sử dụng | MetaDegron đã có trong source/tài liệu | G3 của đề tài cần làm và kiểm |
|---|---|---|
| Tìm motif/E3 | [ĐỌC-MÃ] Cây chọn E3, regex, bảng hit | [ĐỀ XUẤT] Dùng làm annotation tham chiếu, không đổi E3 thành nhiệm vụ chính |
| Ưu tiên đột biến | [CHƯA XÁC MINH] Chưa kiểm thấy ma trận ΔPSI theo mutation trên web này | [ĐỀ XUẤT] Ma trận thay thế, xếp hạng phép thay cụ thể và mutant controls |
| Ngữ cảnh protein | [ĐỌC-MÃ] MSA, PDB, mạng, PTM annotations | [ĐỀ XUẤT] Chỉ thêm khi giúp quyết định phép thử, không lấy đồ họa làm tính mới |
| Độ tin cậy | [CHƯA XÁC MINH] Chưa xác nhận calibration/uncertainty theo query | [ĐỀ XUẤT] Khoảng bất định, cụm gần train, provenance nhãn, cảnh báo ngữ cảnh assay |
| Tái lập | [ĐỌC-MÃ] Download nguồn/checkpoint, xuất job | [ĐỀ XUẤT] Export machine-readable, model/data version, API, script tái tính và metric nhất quán |

[CHƯA XÁC MINH] Bảng G3 là yêu cầu/đề xuất, không chứng nhận ứng dụng của luận văn đã triển khai đủ các tính năng. Không tuyên bố một tính năng chưa có ở bất kỳ công cụ nào từ việc chỉ đọc MetaDegron.

[ĐỌC-MÃ] Điều khoản riêng của dịch vụ chưa xác nhận: Terms.php404 và link chính sách403. Không submit dù số chuỗi ít; nếu bước sau cần server phải làm rõ điều khoản và xin chấp thuận theo giới hạn người dùng đã đặt. Phiên này chỉ đọc trang và tài sản mẫu. [source-manifest.json](source-manifest.json).
