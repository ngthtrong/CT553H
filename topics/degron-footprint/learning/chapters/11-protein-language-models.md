# Từ trình tự đến ESM, CNN và mCNN

## “Ngôn ngữ protein” là phép tương tự có giới hạn

**Protein language model (pLM)** học quy luật thống kê của chuỗi amino acid. Một cách huấn luyện là che một residue rồi dự đoán residue đó từ ngữ cảnh. Mô hình có thể tạo vector giàu thông tin về trình tự; không có nghĩa nó hiểu assay ΔPSI hoặc biết E3 của một peptide. ESM2 là họ mô hình được xây dựng theo hướng học từ dữ liệu trình tự quy mô lớn. [TL-04]

**Tokenizer** chuyển ký tự amino acid thành chỉ số token; mô hình có thể thêm token đầu/cuối chuỗi. Do đó, “28 residue” không nhất thiết đồng nghĩa tensor dài 28 token. Khi lấy vector ở vị trí mutation, phải bù đúng offset token đặc biệt, kiểm alphabet, chiều tensor và trường hợp ký tự không hợp lệ.

**Backbone** là khối pLM tạo biểu diễn; **head** là khối nhỏ biến biểu diễn thành dự đoán nhiệm vụ. Cùng backbone nhưng khác head là các mô hình khác nhau. Tên “ESM2-35M” chỉ quy mô/họ backbone, không xác định hết pipeline.

## Frozen feature và PCA/Ridge

Với một WT và mutant, runner lấy biểu diễn theo quy ước đã khóa: chênh lệch tại residue và chênh lệch biểu diễn trung bình là một dạng feature được sử dụng. Vector có thể lớn; **PCA** tìm các trục biến thiên chính rồi giảm xuống 64 chiều trong nhánh Ridge phù hợp. PCA chỉ được fit trên train của fold. [KH-02; KH-03]

Lý do dùng head chung PCA/Ridge khi khảo sát nhiều pLM là giảm số yếu tố thay đổi cùng lúc. Tuy nhiên số chiều gốc, dữ liệu pretrain và tokenizer vẫn khác. Kết quả của phép so đó chỉ trả lời “pipeline frozen với head chung nào tốt hơn ở đây”, chưa tách hoàn toàn mọi nguyên nhân của khác biệt.

## Pointwise, convolution và nhiều thang cửa sổ

Một **kênh** là một tọa độ đặc trưng ở từng residue. **Convolution/tích chập một chiều** trượt bộ lọc dọc chiều trình tự; cùng trọng số được dùng tại nhiều vị trí. **Kernel size** là độ rộng cửa sổ của bộ lọc.

- **Pointwise, kernel 1:** biến đổi từng vị trí ở bước tích chập, chưa trộn vị trí lân cận tại bước đó.
- **CNN, kernel 5:** có thể kết hợp feature của các vị trí gần nhau.
- **mCNN, kernel 3/5/7:** nhiều nhánh nhận các độ rộng khác nhau, sau đó kết hợp.

**Pooling** gộp biểu diễn nhiều vị trí thành vector để hồi quy. **ReLU** đưa giá trị âm về 0 trong bước phi tuyến; nó giúp head biểu diễn quan hệ vượt hồi quy tuyến tính. **Dropout** tạm bỏ ngẫu nhiên một phần activation khi train để regularize; lúc đánh giá cần đúng chế độ đã quy định.

![Đối chứng đầu mạng trên ESM2-35M. Hình thể hiện ba đường dùng cùng loại backbone; nó không khẳng định các head có số tham số bằng nhau.](assets/diagrams/esm-heads.pdf){width=95%}

::: {.limit title="Kernel 1 vẫn có ngữ cảnh từ ESM"}
Đầu pointwise không trộn vị trí tại convolution, nhưng vector ESM đầu vào đã phụ thuộc ngữ cảnh chuỗi. Vì thế CNN thắng pointwise chỉ hỗ trợ ích lợi tăng thêm của head trong thiết kế đó; không chứng minh pointwise hoàn toàn không biết vị trí lân cận.
:::

## Số tham số, seed và ensemble

Head phức tạp hơn có thể có nhiều tham số hơn. Cải thiện có thể đến từ độ rộng ngữ cảnh, dung lượng, regularization hoặc cách tối ưu. Muốn suy luận hẹp hơn, cần ablation khớp số tham số/budget. Full-PSI hiện cung cấp bằng chứng đối chứng hữu ích, chưa loại hết các khả năng này.

Seed và ensemble đã được giải thích ở chặng 6. Khi so kiến trúc, giữ số thành viên tương ứng: không gán mức tăng của ensemble ba seed so với một seed đơn hoàn toàn cho head. [NC-14; NC-16]

**Vận dụng:** giải thích vì sao cùng backbone chưa đủ xác định model và kernel 1 trên ESM vẫn có ngữ cảnh. Dùng khung so sánh ở [chặng thực hành](#practice) để kiểm câu trả lời.
