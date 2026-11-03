# Baseline: biến câu hỏi sinh học thành các đối chứng kiểm được

## Hồi quy và feature

**Hồi quy** dự đoán một giá trị liên tục, ở đây là ΔPSI. **Feature** là cách biểu diễn đầu vào bằng số. Model không nhìn chữ A/V như người đọc; ta phải đưa chuỗi, vị trí và phép thay về các vector hoặc tensor có cấu trúc.

**Baseline** là đối chứng có vai trò rõ. Baseline hằng 0 hỏi mô hình có hơn “không dự đoán thay đổi” không. Ridge hỏi một quan hệ tuyến tính có điều chuẩn đã giải thích được bao nhiêu. ΔPAP hỏi chênh score toàn peptide có thay được học nhãn mutation không. Baseline mạnh làm phép so khó hơn nhưng giúp biết đóng góp thực sự.

WT-PSI, read count, tầng PSI và fold là **metadata**, thông tin mô tả để QC, chọn miền hoặc đánh giá. Protocol v3 không đưa chúng vào feature trình tự. Khi chấm peptide mới, ta không mặc định có PSI đo sẵn. Tương tự, không dùng PSI(WT) thật để ép dự đoán vào giới hạn vật lý rồi coi đó là dự đoán chỉ từ trình tự. [KH-02]

## One-hot và composition

**One-hot** mã hóa một loại thành vector: trong 20 amino acid, phần tử tương ứng loại ấy là 1, các phần tử khác bằng 0. Ghép WT amino acid và mutant amino acid cho 40 chiều. Đây là feature của **cặp thay thế**, có hướng: A→V khác V→A.

**Composition** đếm hoặc biểu diễn tỉ lệ từng loại amino acid trong peptide. Nó giữ thông tin thành phần nhưng làm mất thứ tự. Đối chứng tên M0 trong hồ sơ lịch sử thực tế có cặp thay thế **và** composition; không được hiểu là composition thuần. [NC-24]

::: {.worked title="Tại sao thành phần không phân biệt mọi vị trí?"}
WT tự đặt `MALAKLA` có hai phép A2V và A4V. Mutant lần lượt là `MVLAKLA` và `MALVKLA`: cùng cặp A→V, cùng composition. Model chỉ dùng hai khối đó phải cho cùng dự đoán dù vị trí khác nhau. Nếu nhãn đo khác, model bị thiếu thông tin cần thiết; đây là hạn chế biểu diễn, không phải thí nghiệm tự mâu thuẫn.
:::

## Ngữ cảnh có thứ tự và không thứ tự

**Cửa sổ ngữ cảnh** là các residue quanh vị trí đột biến. Cửa sổ ±3 nhìn ba residue trước và ba residue sau. Ngữ cảnh **không thứ tự** có thể đếm thành phần của cửa sổ; nó không giữ amino acid nằm bên trái hay bên phải. Ngữ cảnh **có thứ tự** giữ từng offset thành một kênh riêng.

Ridge M3 dùng 40 chiều cặp thay, 20 chiều composition và $6\times20=120$ chiều ngữ cảnh có thứ tự ±3, tổng 180 feature. Intercept của hồi quy là hệ số chặn, phải phân biệt với các feature sinh học khi đọc một ma trận cache. W5 mở ngữ cảnh tới ±5, tổng 260 feature trong thiết kế tương ứng.

![Chuỗi đối chứng feature. Mũi tên nghĩa là thêm một khối thông tin để so công bằng, không phải huấn luyện mô hình trước rồi truyền trọng số sang mô hình sau.](assets/diagrams/feature-controls.pdf){width=91%}

Lý do làm chuỗi đối chứng là tách câu hỏi: cặp thay đã giải thích được gì; thêm thành phần giúp gì; biết các amino acid gần nhau giúp gì; biết **thứ tự** giúp gì? Nhảy từ một đối chứng yếu sang mạng lớn dễ gán nhầm lợi ích cho architecture.

## Ridge học gì và α dùng để làm gì?

Ridge là hồi quy tuyến tính có phạt độ lớn trọng số. Dạng đơn giản là:

$$\hat y=b+w^Tx,\qquad
\min_{w,b}\sum_j(y_j-\hat y_j)^2+\alpha\lVert w\rVert_2^2.$$

Số hạng đầu muốn dự đoán sát nhãn; số hạng sau hạn chế trọng số quá lớn. **Regularization**, điều chuẩn, là ràng buộc giúp giảm việc học quá sát nhiễu. α lớn làm phạt mạnh hơn. Không có α tốt cho mọi dataset; lựa chọn được thực hiện bằng validation ở trong từng fold.

**Overfitting** là học tốt những chi tiết của tập fit nhưng kém trên dữ liệu giữ lại. **Underfitting** là biểu diễn hoặc model quá hạn chế để học quan hệ cần thiết. Một mạng kém hơn Ridge không chứng minh dữ liệu không có tương tác; nó có thể phản ánh ngân sách nhãn, tối ưu, nhiễu hoặc phương sai.

MSE thường dùng để chọn cấu hình vì đo độ sai bình phương. Metric báo cáo có thể là macro MAE hoặc AUROC; cần biết loss tối ưu và metric đánh giá không nhất thiết trùng nhau.

## ΔPAP và Degformer là hai phép đối chiếu khác

PAP dự đoán score cả peptide. Lấy score mutant trừ WT tạo **ΔPAP**. Nó là proxy cho hiệu ứng, không phải model đã học nhãn ΔPSI saturation của đề tài theo cùng protocol. Điều này khiến nó là đối chứng hữu ích nhưng cần nói rõ nguồn pretrained và overlap.

Degformer là kiến trúc transformer dự đoán PSI. Checkpoint tác giả, architecture train lại chỉ bằng saturation, và run train lại có nguồn dữ liệu rộng hơn nhưng loại cụm test là ba tình huống khác nhau. Một score từ checkpoint đã thấy peptide test không phải cùng câu hỏi với train sạch cụm. Chặng lịch sử sẽ chỉ rõ kết quả nào thuộc tình huống nào.

::: {.exercise title="Tự kiểm 07"}
1. Tại sao A→V và V→A cần được phân biệt?
2. Tự tính số chiều nếu dùng cặp thay, composition và ngữ cảnh ±2 có thứ tự.
3. α là trọng số học từ gradient hay hyperparameter do quy trình lựa chọn?
4. Viết đối chứng cần có trước khi kết luận “CNN cần thiết”.
:::
