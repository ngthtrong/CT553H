# Bắt đầu từ câu hỏi, không bắt đầu từ mô hình

## Bạn sẽ học được gì?

Sau chặng này, bạn cần kể lại được đề tài trong một phút: ta muốn dự đoán đại lượng nào, một mẫu là gì, kết quả dùng để làm gì và bằng chứng hiện tại dừng ở đâu. Chưa cần biết mạng neural hoạt động ra sao.

Đề tài nghiên cứu **hiệu ứng của một phép thay amino acid lên độ ổn định của reporter mang peptide**, rồi xây công cụ giúp người nghiên cứu ưu tiên đột biến. “Reporter” là hệ đo có tín hiệu quan sát được; “peptide” là một đoạn chuỗi amino acid ngắn. Hai khái niệm này sẽ được giải thích từ đầu ở các chặng sau.

::: {.concept title="Đơn vị dự đoán của đề tài"}
Một đầu vào gồm **trình tự gốc + vị trí + amino acid thay vào**. Đầu ra chính là một số liên tục, ký hiệu ΔPSI, biểu thị thay đổi chỉ số ổn định trong assay. Một phép thay thế là một mẫu của bài toán; một peptide cung cấp nhiều mẫu có liên hệ với nhau.
:::

## Bốn câu hỏi cần tách riêng

“Peptide có thúc đẩy phân hủy không?” là câu hỏi mức peptide. “Thay A ở vị trí 4 thành V làm reporter thay đổi thế nào?” là câu hỏi mức đột biến. “E3 nào trực tiếp nhận diện đoạn này?” là câu hỏi cơ chế. “Biến thể này gây bệnh không?” là câu hỏi lâm sàng. Chúng có thể liên quan nhưng cần nhãn, thiết kế và bằng chứng khác nhau.

Đề tài hiện tập trung câu hỏi thứ hai. Một mô hình làm tốt câu đó chưa tự trở thành công cụ nhận diện E3 hoặc chẩn đoán bệnh. Việc nối ClinVar vào giao diện bổ sung ngữ cảnh tham khảo, không biến score thành xác suất bệnh.

Một ví dụ **tự đặt để học**: hai phép thay ở hai vị trí có cùng loại amino acid gốc và thay vào nhưng tạo hiệu ứng khác nhau. Nếu mô hình chỉ đếm thành phần chuỗi, nó có thể bỏ mất thông tin vị trí. Từ đó xuất hiện câu hỏi nghiên cứu về ngữ cảnh, thay vì thêm CNN chỉ vì CNN phổ biến.

![Lộ trình học. Mũi tên chỉ thứ tự nên hiểu; ô vàng cuối là hướng tiếp tục, không phải kết quả đã hoàn thành.](assets/diagrams/learning-map.pdf){width=90%}

## Ba lớp bằng chứng khi đọc tài liệu này

::: {.evidence title="ĐÃ ĐO / ĐÃ LƯU"}
Một số liệu có nguồn tính toán trong repository: dữ liệu được xét, protocol, metric, seed/fold và kết quả đã ghi. Tài liệu này đọc lại kết quả; không tạo lượt train mới. Các mã NC trong sách trỏ tới danh mục bằng chứng ở cuối.
:::

::: {.choice title="DIỄN GIẢI"}
Là điều có thể rút ra từ phép so đã làm. Ví dụ, “train toàn dải giảm MAE trong benchmark này” có phạm vi hẹp hơn “mô hình này tốt cho mọi protein”. Diễn giải phải đi kèm population, phép chia và độ bất định.
:::

::: {.roadmap title="HƯỚNG ĐI / CHƯA HOÀN TẤT"}
Là thiết kế hoặc việc cần làm tiếp. Đặc biệt, phần local đang dở chỉ giải thích kế hoạch và lý do lựa chọn. Sách không dùng inner-validation hay checkpoint chưa đủ để công bố hiệu năng local.
:::

Các ví dụ tự đặt luôn mang nhãn **minh họa**. Các ảnh giao diện dùng dữ liệu tổng hợp được ghi là **fixture**. Một hình vẽ đẹp không nâng cấp mức bằng chứng.

## Thứ tự phát triển của đề tài

Đầu tiên là kiểm xem nguồn công khai thực sự có nhãn nào dùng được. Sau đó dựng lại phép đo và nhãn, thiết lập baseline, phát hiện chồng lặp, rồi mới khảo sát các cải tiến. Các mốc lịch sử dùng outer-test 91 peptide; việc nới train lên pool 176 peptide không làm outer-test thành 176 peptide.

Luồng hiện hành full-PSI dùng {{SAT_PEPTIDES}} peptide, {{SAT_CELLS}} ô saturation và {{SAT_GROUPS}} nhóm protein. Đây là **population và protocol mới**, không phải một điểm số có thể ghép trực tiếp vào bảng cũ. Kết quả là development: dữ liệu đã tham gia quá trình chọn hướng nghiên cứu. [NC-02, NC-04, NC-15, NC-16]

Đến mốc 03/11/2026, đã có nghiên cứu, baseline ứng dụng và luận văn đang viết. Các cổng G2/G3 vẫn chưa được xác nhận hoàn tất; model phục vụ vẫn là baseline đã cố định. Tên cổng chỉ là nhãn quản lý dự án, không phải chứng nhận khoa học độc lập.

## Cách học có đầu ra cụ thể

Đọc theo thứ tự, ghi lại bốn dòng sau mỗi chặng: **đầu vào là gì; thao tác gì; tại sao làm vậy; chưa được kết luận gì**. Khi gặp công thức, tính một ví dụ nhỏ trước khi nhìn score thật. Khi gặp kết quả, tìm đối chứng trước khi nhìn giá trị lớn nhất.

Bạn có thể chia thành sáu buổi: nền tảng và phép đo; nhãn và dữ liệu; chia tập và baseline; metric và lịch sử; ESM/full-PSI; local/phần mềm/tổng hợp. Thời lượng tùy nền tảng, không có yêu cầu học xong trong một ngày.

::: {.exercise title="Tự kiểm 01"}
1. Viết một đầu vào cụ thể của mô hình bằng ba thành phần.
2. Vì sao một heatmap dự đoán chưa xác nhận E3 trực tiếp gắn vào residue?
3. Phân biệt “đã train một fold”, “có OOF đầy đủ” và “đã kiểm chứng ngoài”.
:::
