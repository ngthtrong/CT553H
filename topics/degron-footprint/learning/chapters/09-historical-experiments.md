# Các thực nghiệm đầu: học được gì từ mô hình đơn giản?

## Vì sao bắt đầu bằng đối chứng nhỏ?

Trước khi dùng mạng lớn, cần biết bài toán có tín hiệu vượt một quy tắc đơn giản hay không. Nếu chỉ biết amino acid gốc, amino acid mới và vài residue lân cận đã dự đoán khá tốt, một mô hình phức tạp phải chứng minh giá trị tăng thêm trên cùng phép chia. Đối chứng nhỏ còn giúp phát hiện lỗi nhãn, lỗi chiều score và rò rỉ trước khi chi nhiều GPU.

**ΔPAP** là hiệu hai score PAP của mutant và WT. Đây là cách chuyển một bộ chấm trình tự sang score cho phép thay thế; không phải nhãn ΔPSI được đo trực tiếp. Ridge học từ nhãn saturation của đề tài, còn ΔPAP đóng vai trò đối chứng khác loại. Phải kiểm hướng score trước khi tính AUROC. [NC-02; NC-24]

## Mốc saturation ban đầu

Benchmark ban đầu có **91 peptide, 89 nhóm, 47.847 ô hợp lệ**. Ridge đạt macro AUROC {{BASE_AUC}}, ΔPAP đạt {{DPAP_AUC}}. Đây là kết quả trên population PSI thấp và protocol lịch sử; không đại diện ngay cho full-PSI hoặc mọi protein người. [NC-02; NC-03]

::: {.evidence title="Kết quả đã có và kết luận vừa đủ"}
Một mô hình hồi quy có regularization khai thác được tín hiệu mutation trên phép chia nhóm đã dựng. Nó tạo baseline có thể tái lập để kiểm các ý tưởng sau. Chưa có căn cứ từ riêng kết quả này để xác định E3, cơ chế gắn trực tiếp hoặc ý nghĩa bệnh lý của mutation.
:::

## P0: thêm nhãn train, giữ nguyên nơi chấm

**Learning curve** là đường biểu diễn chất lượng theo lượng dữ liệu train. Khi muốn biết thiếu dữ liệu có phải nút thắt không, hãy tăng dữ liệu nhưng giữ tập đánh giá và cách tính metric ổn định.

Ở nhánh mở rộng, tập train có thể dùng 176 peptide thay cho 91; 85 peptide thêm cung cấp 44.490 ô. Tập chấm lịch sử vẫn là 91 peptide. Ridge mở rộng đạt macro AUROC {{EXT_AUC}}, cao hơn khoảng 0,0126; CI ghép cặp của độ tăng là [0,0061; 0,0190]. Không phải cả 176 peptide đều trở thành dữ liệu test. [NC-04]

![Đường cong lịch sử và mốc train mở rộng. Các điểm cùng màu thuộc thí nghiệm lấy bớt dữ liệu; đường đứt là cấu hình mở rộng. Không suy ra “trần” của mọi kiến trúc từ hình này.](assets/figures/historical-learning-curve.pdf){width=92%}

Mức 75% và 100% gần nhau gợi ý lợi ích biên đã giảm trong thiết kế đó. Tuy nhiên, mở thêm miền nhãn vẫn có thể hữu ích. Vì vậy hướng tiếp theo là kiểm tra **nguồn nhãn và phân bố**, thay vì khẳng định đã hết tín hiệu. Các nhánh kiểm soát lượng nhãn/ngưỡng được lưu riêng để tránh gán mọi cải thiện cho số mẫu. [NC-04; NC-05; NC-06]

**Sensitivity analysis/kiểm độ nhạy** thay một giả định rồi xem kết luận có còn giữ không. Audit phân cụm cho lợi ích P0 vẫn dương ở ba phân hoạch khác thật ngoài mốc tham chiếu. Bảy mức tham số chỉ tạo bốn phân hoạch riêng biệt; không đếm các nhóm trùng nhau thành bảy xác nhận độc lập. Đây là độ bền trong dải đã kiểm, chưa bảo đảm mọi cách chia hoặc assay đều giống vậy. [NC-20]

## R0, R1 và R2: mỗi nhánh kiểm một nghi vấn

**Reproduction/tái lập** là chạy lại cấu hình có hồ sơ để kiểm đường tính toán, không phải tự tạo một câu hỏi nghiên cứu mới. R0 ghi nhận 12/12 gate kiểm tra đạt trong run Kaggle đã lưu. Thành công này xác nhận các điều kiện kiểm của notebook đó; không tự đóng mọi gate nghiên cứu. [NC-10]

R1 kiểm Degformer khi chia sạch theo cụm protein. Với ba seed và năm fold, ensemble đạt AUROC {{R1_AUC}}, thấp hơn Ridge mở rộng khoảng 0,8208. Không dùng điểm của checkpoint đã thấy protein tương đồng trong train làm đối chứng công bằng. Điểm checkpoint công bố và điểm retrain sạch trả lời hai câu hỏi khác nhau. [NC-11]

R2 dùng **embedding ESM đóng băng**, giảm chiều PCA rồi đưa vào Ridge. Embedding là vector biểu diễn chuỗi do mô hình học từ lượng lớn trình tự. “Đóng băng” nghĩa là không cập nhật trọng số ESM trong thí nghiệm này. Kết hợp đặc trưng đạt khoảng 0,8230, so với 0,8208 của Ridge; CI chênh lệch còn chứa 0. ESM riêng cũng không thắng mặc định. [NC-12]

::: {.choice title="Từ kết quả tới quyết định"}
Không bỏ baseline chỉ vì có mô hình lớn hơn. Các kết quả dẫn tới câu hỏi hẹp hơn: lợi ích đến từ cửa sổ có thứ tự, biểu diễn pLM, đầu mạng học được, hay ensemble? R6 và full-PSI được dùng để tách dần các yếu tố này.
:::

::: {.exercise title="Tự kiểm 09"}
1. Vì sao “train 176, test 91” không mâu thuẫn?
2. Learning curve gần phẳng đã chứng minh mọi mô hình đều hết khả năng cải thiện chưa?
3. Với 0,8230 và 0,8208 nhưng CI chênh lệch chứa 0, nên viết kết luận thế nào?
:::
