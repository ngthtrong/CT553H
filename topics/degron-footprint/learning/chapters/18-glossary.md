# Từ điển tra nhanh

Định nghĩa dưới đây phục vụ cách dùng trong đề tài; khi quay lại một chương, vẫn cần đọc điều kiện cụ thể của phép đo và protocol.

| Thuật ngữ | Nghĩa trong tài liệu |
|:--|:--|
| Amino acid / residue | Đơn vị cấu tạo protein; residue là đơn vị đã nằm trong chuỗi. |
| Peptide / protein | Peptide là đoạn chuỗi ngắn trong bài toán; protein nguyên vẹn có bối cảnh cấu trúc và chức năng rộng hơn. |
| WT / mutant | Trình tự gốc được chọn làm mốc / trình tự đã thay một amino acid. WT không mặc định là non-degron. |
| Degron / footprint | Tín hiệu liên quan phân hủy / mẫu hiệu ứng theo vị trí và phép thay; chưa tự xác nhận cơ chế E3. |
| E3 / UPS | Thành phần đặc hiệu trong quá trình gắn ubiquitin / hệ ubiquitin–proteasome, một con đường phân hủy protein. |
| Construct / reporter | Thiết kế DNA được đưa vào hệ đo / phân tử cung cấp tín hiệu quan sát để suy ra đại lượng nghiên cứu. |
| Assay / endpoint | Phép thử thực nghiệm / đại lượng hoặc sự kiện cụ thể được đo, dự đoán hay chấm. |
| FACS / bin | Phân loại tế bào dựa trên tín hiệu huỳnh quang / nhóm tín hiệu đã phân loại. |
| Read / read count | Một đoạn trình tự máy đọc / số read được quy về một thiết kế trong bin. |
| PSI / ΔPSI | Chỉ số ổn định có trọng số bin / PSI mutant trừ PSI WT theo quy tắc cùng điều kiện. |
| Replicate / QC | Lần đo lặp / kiểm chất lượng với quy tắc giữ, loại và lý do thiếu. |
| Saturation / scanning | Thử nhiều loại thay tại các vị trí / quét một tập loại thay trên nhiều vị trí, trong nguồn này. |
| Tile / stride | Cửa sổ peptide cắt từ protein / bước dịch cửa sổ, ở đây thiết kế 28 và bước 23. |
| Accession / mapping | Định danh bản ghi nguồn / quan hệ ánh xạ giữa trình tự, vị trí và annotation. |
| Provenance / manifest | Nguồn gốc và lịch sử tạo dữ liệu / bản kê phiên bản, thành phần và hash phục vụ tái lập. |
| Feature / label | Thông tin đưa vào mô hình / giá trị mục tiêu được học hoặc đánh giá. |
| Baseline / ablation | Đối chứng làm mốc / đổi một thành phần có kiểm soát để tìm nguồn khác biệt. |
| Ridge / regularization | Hồi quy tuyến tính có phạt L2 / ràng buộc làm giảm khả năng fit quá mức. |
| Hyperparameter / epoch | Tham số thiết kế như α, learning rate / một lượt qua tập train theo cách lấy batch. |
| Split / fold / seed | Cách chia dữ liệu / một lượt chia đánh giá / giá trị khởi tạo ngẫu nhiên có kiểm soát. |
| Homology / coverage | Tương đồng có nguồn gốc tiến hóa / phần độ dài được alignment phủ, không phải phần trăm identity. |
| Leakage / OOF | Thông tin vượt ranh giới đánh giá / dự đoán cho mẫu không dùng fit model tương ứng. |
| Inner / outer | Vòng trong để chọn cấu hình / vòng ngoài để ước lượng chất lượng quy trình. |
| MAE / RMSE | Sai số tuyệt đối trung bình / căn sai số bình phương trung bình; thấp hơn thường tốt hơn. |
| AUROC / AP | Metric xếp hạng hai lớp / tổng hợp precision theo recall; không phải probability đã hiệu chuẩn. |
| Macro / micro | Tổng hợp từ đơn vị như peptide / tổng hợp ô, có thể tăng trọng lượng peptide nhiều ô. |
| CI / bootstrap | Khoảng bất định theo thủ tục / lấy lại mẫu có hoàn lại, ở đây theo nhóm protein. |
| pLM / embedding | Mô hình học quy luật chuỗi protein / vector biểu diễn được trích từ mô hình. |
| Tokenizer / backbone / head | Đổi ký tự thành token / khối tạo biểu diễn / khối dự đoán nhiệm vụ. |
| PCA / channel / kernel | Giảm chiều tuyến tính / kênh đặc trưng / độ rộng bộ lọc tích chập. |
| Frozen / fine-tune / LoRA | Không cập nhật backbone / học tiếp trọng số / học cập nhật hạng thấp cho một số ma trận. |
| Ensemble / checkpoint | Gộp dự đoán nhiều model / trạng thái model và tối ưu để lưu hoặc tiếp tục. |
| Calibration / Brier / ECE | Khớp xác suất với tần suất / sai số bình phương xác suất / độ lệch theo bin. |
| Domain / guardrail | Miền dữ liệu phù hợp / tiêu chí bảo vệ một thuộc tính khi tối ưu mục tiêu khác. |
| Development / held-source | Dữ liệu tham gia quá trình phát triển / nguồn giữ lại trong protocol, có lịch sử cần công bố. |
| ETL / migration | Trích xuất–biến đổi–nạp / thay đổi cấu trúc CSDL có quản lý phiên bản. |
| Snapshot / fixture / job | Bản chụp kết quả / dữ liệu dựng cho kiểm giao diện / tác vụ có trạng thái và kết quả. |
| Export / promotion | Tạo gói suy luận / quyết định đưa một phiên bản vào phục vụ sau kiểm chứng. |

Không cần học thuộc toàn bộ bảng trước khi đọc. Mỗi lần gặp một từ mới, quay lại chương đã giới thiệu từ đó và tự gắn nó vào một ví dụ của đề tài.
