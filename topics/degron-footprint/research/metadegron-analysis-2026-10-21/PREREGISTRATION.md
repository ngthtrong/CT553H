# Tiêu chí chốt trước phép đo mô hình — 21/10/2026

[ĐỀ XUẤT] Văn bản này được ghi trước khi chạy bộ phân loại thành phần hoặc tính chỉ số dự đoán. Đây là audit phát triển, không phải đăng ký trên dịch vụ bên ngoài. Việc đọc schema, số dòng và độ dài trước đăng ký được công khai; chưa xem AUROC của baseline mới.

## 1. Audit nhãn âm

[ĐỀ XUẤT] Tái dựng tập đặc trưng X từ 212 dòng dương tính trong `annotated_degrons_properties.tsv` và nguồn âm mà `Training_MetaDegron-X.py` chỉ định. Đọc chuỗi bằng accession và tọa độ từ snapshot UniProt của họ; không gán ngẫu nhiên chuỗi mới. Phép đo dùng toàn bộ âm hợp lệ không lặp để tránh bootstrap nhân bản; ghi riêng phép tái dựng sampling có hoàn lại của tác giả để kiểm rò rỉ.

[ĐỀ XUẤT] Logistic L2, C=1, chuẩn hóa chỉ trên train; ba biểu diễn: độ dài; 20 tần suất acid amin; 20 số đếm + độ dài. Chạy thêm cửa sổ ngữ cảnh 29 aa với padding không tính vào thành phần. Seed 17, 29, 43; random stratified holdout 10% và 5-fold theo cụm protein identity 30%, cov80/cov50. Không chọn mô hình bằng test. Nếu AUROC thành phần ≥0,75 ở cả ba seed cov80 thì gọi là dấu hiệu shortcut đáng kiểm; <0,60 thì không có bằng chứng shortcut mạnh với baseline này; ở giữa là không chốt. Độ dài ≥0,65 gợi ý cần đối chứng khớp độ dài. Bootstrap 5.000 lần theo cụm cho OOF; CI không sửa được split bị rò rỉ.

[ĐỀ XUẤT] Kiểm số AUROC Degpred công bố bằng tính lại từ `supporting_file/Degpred_result.csv`. Đây chỉ là tái tính chỉ số từ điểm có sẵn, không tái chạy Degpred hoặc MetaDegron.

## 2. MetaDegron ngoài nguồn, chỉ chạy nếu đạt điều kiện

[ĐỀ XUẤT] Điều kiện: có đầu vào/trọng số và phép nạp an toàn, tái lập đúng cửa sổ/encoding cùng chiều điểm; không nạp pickle hoặc object NPY bằng cơ chế thực thi tùy ý; không gọi server khi điều khoản chưa rõ. Không thay MetaDegron bằng một surrogate rồi gắn tên MetaDegron. Nếu thiếu điều kiện, ghi `blocked` cùng bằng chứng và không sinh điểm giả.

[ĐỀ XUẤT] (a) Peptide zero-shot: bỏ giao chính xác và giao cụm protein cov80 với tập curated có thể đã dùng train; báo nhạy cov50, báo riêng nhóm chồng lấn. Điểm suy thoái càng cao dự kiến PSI càng thấp, nên Spearman(score, PSI) kỳ vọng âm. AUROC dùng `PSI <= 3` làm dương, báo cả cỡ từng lớp. Với dữ liệu chỉ gồm degron, không tính AUROC lớp hoạt tính khi chỉ có một lớp. Cửa sổ motif trùng nhau gộp bằng max đã chốt trước; không có regex hit là abstention, không tự gán xác suất 0. Thắng thăm dò nếu CI cụm của tương quan định hướng vượt 0 và AUROC >0,60; chưa phải G2.

[ĐỀ XUẤT] (b) Ma trận bão hòa: giữ nguyên `g2-saturation-input.npz`, fold cov80, nhãn `y >= 1`, metric macro AUROC mức ô theo peptide. Tính và lưu `ΔScore = score(mutant)-score(WT)`; điểm xếp hạng phá degron chính là `-ΔScore` do chiều PSI ngược chiều hoạt tính degron. Báo cả hai chiều, coverage và abstention, không chọn chiều sau xem kết quả. Nếu mutation phá regex, phép so chính giữ tọa độ/cửa sổ WT để tránh trộn mất ứng viên với thay đổi classifier; báo thêm chế độ pipeline motif. Không có đủ mô hình để chấm cửa sổ cố định thì không chạy phép so này.

[ĐỀ XUẤT] So ghép cặp trên cùng ô với ΔPAP và ridge M3, bootstrap cụm 5.000 lần, seed 17/29/43 cho các thao tác có ngẫu nhiên. Chỉ gọi thắng ridge khi cận dưới CI delta >0; chỉ gọi có ích làm teacher nếu được xác nhận trong outer-train, không chọn teacher hay hyperparameter từ fold test. So Degformer retrain một seed chỉ là đối chứng tham chiếu. Bảng khác coverage phải báo coverage và tính lại mọi baseline trên giao ô.

## 3. Mẫu kiểm nguồn nhãn

[ĐỀ XUẤT] Lấy ngẫu nhiên đơn 40/302 dòng với seed 17, giữ chỉ số dòng và PMID. Kiểm từng tọa độ, chuỗi gốc, liên kết nguồn, phạm vi HUMAN; tìm chứng cứ ELM/thí nghiệm gốc. Nhãn `confirmed`, `wrong`, `ambiguous` và `unresolved-access` tách riêng. Không tính không truy cập được thành nhãn sai. Báo Wilson 95% cho tỉ lệ trên mẫu; nếu chỉ kiểm metadata thì không gọi là ước lượng sai nhãn sinh học.

## 4. Bổ sung trước tính điểm: checkpoint X bằng bộ đọc tĩnh

[ĐỀ XUẤT] Sau khi nhận diện một khối UBJSON trong pickle bằng `pickletools` (chưa tính điểm), bổ sung kiểm tra nhánh X trên bảng thuộc tính có sẵn. Không unpickle, không import XGBoost hoặc mã tải về: chỉ đọc opcode để lấy đúng một literal byte payload, parse UBJSON với giới hạn kích thước/độ sâu, kiểm cấu trúc cây số, tự tính tổng lá và logistic. Giữ thứ tự 10 cột của `Training_MetaDegron-X.py`; đối chiếu số feature/objective từ payload trước khi dự đoán.

[ĐỀ XUẤT] Tái dựng phép so β-TrCP trong `Performance_benchmarking.ipynb`: 20 dương tính từ `test_properties.tsv`, âm từ `simulated_degron2.csv`, mỗi lần lấy số âm bằng số dương; seed tác giả 1–10 để tái tính con số công bố, đồng thời seed audit 17/29/43. So AUC trung bình với 0,9670; chênh tuyệt đối ≤0,005 được gọi khớp gần ở mức tái tính, không xác nhận độc lập. Nếu khác thì báo nguyên sai lệch. Không tinh chỉnh để khớp. Phải kiểm giao 20 dương tính với dữ liệu curated và bảng 212 dòng: từ “independent” của bài báo không tự thành holdout sạch.
