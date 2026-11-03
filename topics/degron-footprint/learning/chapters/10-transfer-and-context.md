# Chuyển giao tri thức và vai trò ngữ cảnh

## Pretrain, fine-tune và scratch khác nhau ở đâu?

**Pretraining/tiền huấn luyện** là học trên nhiệm vụ hoặc nguồn dữ liệu trước nhiệm vụ đích. **Fine-tuning/tinh chỉnh** là tiếp tục cập nhật một phần hoặc toàn bộ trọng số trên dữ liệu đích. **Scratch** là bắt đầu từ trọng số ngẫu nhiên. Muốn kiểm giá trị chuyển giao, cần hai nhánh cùng kiến trúc và cùng quy tắc chọn epoch; khác biệt có chủ đích là giai đoạn học trước.

Vì sao chuyển giao có thể hữu ích? Nhãn đích ít, còn nguồn phụ có thể giúp nhận ra mẫu trình tự. Vì sao có thể thất bại? Nguồn phụ đo đại lượng khác, có batch effect, hoặc học đặc điểm không dùng được cho mutation. Pretraining là giả thuyết cần đối chứng.

## P3: học độ ổn định của tile chưa đủ giúp hiệu ứng mutation

**Tile** là đoạn cắt có độ dài cố định từ một protein. P3 dùng 212.616 tile ở nguồn bổ sung để tiền huấn luyện encoder, sau đó học saturation. AUROC khoảng 0,8098 cho nhánh pretrain, 0,8175 cho scratch và 0,8208 cho Ridge trong thiết kế đó. CI pretrain trừ scratch còn chứa 0; không có bằng chứng lợi ích từ cách chuyển giao này. [NC-07]

::: {.concept title="Đại lượng tuyệt đối và hiệu số"}
Học “đoạn này ổn định tới mức nào” không đồng nghĩa học “thay A bằng V tại đây làm thay đổi độ ổn định bao nhiêu”. Nhiệm vụ thứ hai đòi hỏi so hai trình tự gần nhau. Nguồn có nhiều tile vẫn có thể lệch mục tiêu dù số dòng rất lớn.
:::

Không diễn giải kết quả âm thành “mọi pretraining đều vô ích”. Bài học cụ thể là cần kiểm **độ khớp endpoint**: đại lượng nguồn có gần ΔPSI đích không?

## Tại sao chuyển sang scanning ΔPSI?

Scanning đo hiệu ứng của một số phép thay dọc nhiều đoạn. Nó gần bài toán mutation hơn nhãn PSI tuyệt đối. Tuy vậy, scanning chỉ phủ một tập kiểu thay thế, còn saturation phủ rộng hơn; hai nguồn cũng có điều kiện đo riêng. Vì thế hướng scanning pretrain phải đi kèm đối chứng scratch, chia nhóm và đánh giá trên saturation. [NC-15; NC-25]

![Hai nhánh chuyển giao được so trên cùng outer-test. Dữ liệu saturation train được cấp cho cả hai nhánh; scanning không được trộn tùy ý với test. Đây là cấu trúc đối chứng, không phải sơ đồ mọi nguồn đã hợp nhất tương đương.](assets/diagrams/scanning-transfer.pdf){width=90%}

Một cách khác là **joint training/trộn cùng lúc** các nguồn. Cách này dễ để nguồn lớn áp đảo loss và học bias assay. Audit trộn scanning–saturation là một thử nghiệm riêng; không dùng tên chung “thêm dữ liệu” để đánh đồng nó với pretrain rồi fine-tune. [NC-25]

## R6: cửa sổ có thứ tự là một đóng góp rõ hơn

Ridge M3 đã giữ ngữ cảnh **có thứ tự ±3**. Ridge **W5** mở rộng tới ±5, vẫn giữ amino acid ở từng offset và bỏ vị trí trung tâm khỏi khối context vì cặp thay đã mô tả nó. Phép so này kiểm ích lợi của hai residue xa hơn ở mỗi phía; không phải phép so đếm thành phần với ngữ cảnh có thứ tự.

Trên cohort lịch sử 91 peptide, W5 đạt AUROC {{R6_W5_AUC}} so với M3 khoảng 0,8208. Độ tăng 0,0078 có CI đã điều chỉnh [0,0021; 0,0139]. Đây là bằng chứng hỗ trợ ích lợi của cửa sổ có thứ tự trong phạm vi phép so. [NC-14]

![Các phép so R6. Điểm là chênh lệch AUROC; đoạn ngang là CI được ghi trong kết quả. A-window, P-primary và S1-secondary có vai trò giả thuyết khác nhau.](assets/figures/r6-intervals.pdf){width=95%}

ESM2-35M + mCNN đạt AUROC {{R6_MCNN_AUC}}. Chênh lệch với M3 khoảng 0,0097 nhưng CI chính còn chứa 0; so với một đối chứng mạng khác có kết quả thuận lợi hơn. Không chọn phép so có lợi nhất rồi kết luận tổng quát “pLM đã thắng Ridge”. W5 so với mCNN cũng chưa có phân giải rõ trong run này. [NC-14]

::: {.choice title="Hướng đi cụ thể sau R6"}
Giữ W5 làm baseline mạnh, nhỏ và dễ kiểm tra. Tiếp tục tách đầu pointwise khỏi CNN/mCNN trên cùng feature và cohort; mở PSI để xem chất lượng thay đổi theo miền. Không quy toàn bộ mức tăng cho cơ chế sinh học chỉ từ một ablation kiến trúc.
:::

::: {.exercise title="Tự kiểm 10"}
1. Nếu nhánh pretrain có nhiều epoch hơn scratch, phép so còn kiểm riêng chuyển giao không?
2. Vì sao nhãn scanning ΔPSI gần mục tiêu hơn nhãn tile PSI nhưng vẫn chưa tương đương hoàn toàn?
3. R6 hỗ trợ mạnh hơn cho cửa sổ W5 hay cho tuyên bố mọi pLM đều tốt hơn?
:::
