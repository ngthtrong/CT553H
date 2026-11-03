# Đọc metric và khoảng tin cậy trước khi chọn người thắng

## MAE, MSE và RMSE đo những mặt khác nhau

Gọi nhãn thật là $y$ và dự đoán là $\hat y$. **MAE** là trung bình $|\hat y-y|$; đơn vị vẫn là điểm PSI. **MSE** là trung bình $(\hat y-y)^2$, phạt sai lớn mạnh hơn và có đơn vị PSI bình phương. **RMSE** là căn bậc hai MSE, quay về đơn vị PSI.

Ví dụ minh họa: sai số ba ô là 0,1; −0,2; 1,2. MAE bằng $(0,1+0,2+1,2)/3=0,5$. MSE bằng $(0,01+0,04+1,44)/3\approx0,4967$; RMSE khoảng 0,7047. Cùng dữ liệu nhưng số khác nhau, nên không so một MSE inner-validation 0,26 với một MAE test 0,38 để tuyên bố mô hình tốt hơn.

**Macro theo peptide** nghĩa là tính metric trong từng peptide rồi lấy trung bình peptide. **Micro/gộp ô** cho nhiều trọng lượng hơn tới peptide có nhiều ô. V3 ưu tiên macro MAE để mỗi peptide đóng góp tương đương ở bước trung bình, trong population hợp lệ.

## AUROC và AP trả lời câu hỏi xếp hạng

Nhãn nhị phân dương là sự kiện được định nghĩa, chẳng hạn $\Delta PSI\ge1$. **AUROC** đo khả năng xếp một ô dương cao hơn ô âm; score vẫn có thể là số hồi quy, chưa cần là xác suất. AUROC 0,5 là mức không phân biệt trong nghĩa xếp hạng; AUROC 0,85 không có nghĩa 85% mọi dự đoán đúng.

**Precision** là tỉ lệ ô dương trong những ô được chọn. **Recall** là tỉ lệ ô dương thật được lấy ra. **AP** tóm tắt precision theo quá trình thay ngưỡng/xếp hạng, nhạy với tần suất dương. Không so AP giữa hai cohort có tỉ lệ dương khác nhau rồi gán hết chênh lệch cho mô hình.

Ở full-PSI, AUROC/AP yêu cầu ít nhất 3 ô mỗi lớp. Vì thế {{SAT_PEPTIDES}} peptide góp MAE nhưng AUROC dương chỉ có 184 peptide đủ điều kiện. Một giá trị AUROC `null` vì thiếu hai lớp là trạng thái đúng, không phải 0. [NC-16; KH-02]

## Top-k và enrichment gắn với mục đích thực nghiệm

Nếu chỉ có ngân sách thử một ít mutation, metric toàn tập chưa nói rõ shortlist hữu ích thế nào. **Top 10%** lấy nhóm score cao nhất trong mỗi peptide. **Enrichment** bằng precision top-k chia tần suất dương nền của chính peptide, rồi tổng hợp đúng population.

Ví dụ tự đặt: peptide có 10% ô dương; top-k có 40% ô dương ⇒ enrichment=4. Điều này hữu ích cho ưu tiên thử nghiệm, nhưng không bảo đảm mỗi phép thay trong shortlist có xác suất đúng bằng 0,4 ở mọi assay.

## Paired comparison: so cùng peptide

**Ghép cặp** nghĩa là hai model được chấm trên cùng đơn vị đánh giá. Với MAE, tính $MAE_A-MAE_B$ trên các peptide chung; âm có lợi cho A. Với AUROC, dương có lợi cho A. Không chỉ đặt hai số trung bình cạnh nhau mà bỏ mất việc chúng cùng sai hay khác sai ở peptide nào.

**Confidence interval (CI)** mô tả độ bất định theo thủ tục ước lượng đã dùng. Trong dự án, bootstrap lấy lại **nhóm protein có hoàn lại**, giữ các peptide trong nhóm, rồi tính chênh lệch. Lặp 5.000 lần cho phân bố chênh lệch. **Có hoàn lại** nghĩa là cùng nhóm có thể được chọn nhiều lần trong một mẫu bootstrap.

::: {.worked title="Đọc dấu và CI"}
Ví dụ tự đặt: ΔMAE=−0,01, CI [−0,02; +0,005]. Điểm ước lượng có lợi cho A nhưng khoảng chứa 0, nên chưa phân giải rõ. ΔMAE=−0,01, CI [−0,015; −0,004] hỗ trợ giảm sai số trong thiết kế đó. Cả hai vẫn chưa tự chứng minh mức giảm tối thiểu 0,02 PSI.
:::

CI hiện điều kiện trên các dự đoán OOF đã lưu; nó không bao hết phương sai nếu train lại toàn bộ quá trình nhiều lần. Năm fold có tập train giao nhau; ba seed chia sẻ outer partition. Không coi chúng là các mẫu độc lập để làm khoảng tin cậy quá hẹp.

## Ý nghĩa thống kê và mức cải thiện đáng dùng

Một chênh lệch rất nhỏ có thể có CI không chứa 0 nhưng ít giá trị thực tế. Ngược lại, một chênh lệch trung bình đáng quan tâm có thể chưa đủ chính xác để kết luận. V3 đặt trước ngưỡng diễn giải giảm MAE 0,02 PSI và guardrail ranking ở miền PSI thấp. Cần đọc CI và guardrail, không chỉ xem số đứng đầu.

**Multiple comparisons** là việc xem nhiều phép so. Càng thử nhiều, khả năng có một kết quả thuận lợi do ngẫu nhiên càng tăng. **Bonferroni** điều chỉnh mức tin cậy theo số phép trong một họ đã định. Hai phép phạm vi PSI của v3 được điều chỉnh; các phép CNN/transfer tiếp nối chủ yếu là mô tả. Không gắn nhãn “đã xác nhận” cho toàn bộ leaderboard.

**Preregistration/protocol trước run** ghi lựa chọn trước khi xem kết quả mục tiêu. Một protocol viết sau khi đã biết dữ liệu hoặc lịch sử vẫn có ích để tái lập, nhưng phải công bố tính development đó. Một **ablation** là bỏ/đổi một thành phần có đối chứng để tìm nguồn lợi ích; nó không tự giải quyết mọi khác biệt dung lượng model.

::: {.exercise title="Tự kiểm 08"}
1. MAE thấp hơn 0,01 và AUROC thấp hơn 0,01 có cùng nghĩa tốt/xấu không?
2. AUROC=0,85 có phải accuracy 85% không?
3. Vì sao bootstrap từng ô quá lạc quan?
4. Một CI hoàn toàn âm đã đủ chứng minh model dùng được ngoài assay chưa?
:::
