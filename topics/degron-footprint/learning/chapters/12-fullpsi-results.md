# Full-PSI: kết quả mới nhất đã phân tích đầy đủ

## Vì sao mở toàn miền PSI?

Cohort cũ tập trung peptide có WT PSI thấp. Điều này phù hợp câu hỏi làm suy yếu degron, nhưng bỏ bớt miền ổn định hơn và giới hạn độ phủ. V3 xây bundle **{{SAT_PEPTIDES}} peptide, {{SAT_GROUPS}} nhóm, {{SAT_CELLS}} ô saturation**, kèm {{SCAN_CELLS}} ô scanning. Dữ liệu nhiều hơn không tự đồng nghĩa mọi nhãn đồng chất hoặc bài toán đã dễ hơn. [NC-15]

Các **arm/nhánh thiết kế** thay cách dùng dữ liệu train, trong khi cùng chấm trên cohort full-PSI hợp lệ:

| Nhánh | Cách dùng train | Câu hỏi chính |
|:--|:--|:--|
| B | Chỉ WT PSI ≤ 4 | Giữ miền train thấp thì ra toàn miền thế nào? |
| D | Toàn miền PSI | Mở miền train có giảm sai số không? |
| E | Toàn miền, cân bằng theo tầng PSI rồi peptide | Giảm chênh trọng lượng giữa các tầng có ích không? |

**Stratum/tầng** là khoảng PSI dùng phân nhóm; **sample weighting/trọng số mẫu** làm mẫu đóng góp nhiều hoặc ít hơn vào loss. E thay mục tiêu tối ưu bằng trọng số; không tạo ra nhãn mới. Inner-validation của nhánh B vẫn theo miền đánh giá đã quy định, không tự cắt theo tên nhánh. [KH-02]

## Bảng kết quả phải đọc theo cùng endpoint

Các giá trị sau là macro MAE trên dự đoán ensemble đã lưu của Kaggle, ba seed 17/29/43. Thấp hơn là tốt hơn. Đây là kết quả development, chưa đóng gate khoa học. [NC-16]

| Pipeline | MAE | Điều cần nhớ |
|:--|--:|:--|
| Ridge W5, B | {{W5_B}} | Train miền WT PSI ≤ 4 |
| Ridge W5, D | {{W5_D}} | Train toàn miền |
| Ridge W5, E | {{W5_E}} | Thêm cân bằng tầng |
| ESM2-35M + pointwise, D | {{POINT_D}} | Đối chứng head kernel 1 |
| ESM2-35M + CNN, D | {{CNN_D}} | Head kernel 5 |
| ESM2-35M + mCNN, E | {{MCNN_E}} | Nhiều kernel, có cân bằng tầng |
| CNN one-hot scratch, D | {{SCRATCH_D}} | Chưa pretrain scanning |
| CNN one-hot pretrain scanning rep1, D | {{SCAN_PRETRAIN_D}} | Chuyển giao cùng loại ΔPSI |

![Kết quả full-PSI theo đúng pipeline. Hình là giá trị trung bình đã lưu; cần đọc CI ghép cặp bên dưới trước khi xếp hạng.](assets/figures/fullpsi-mae.pdf){width=96%}

Một model có thể giảm MAE nhưng không tăng AUROC ở mọi miền. Ví dụ Ridge B/D/E có AUROC dương toàn cohort đủ điều kiện khoảng 0,8312/0,8319/0,8275; CNN-D khoảng 0,8488 và mCNN-E khoảng 0,8470. Population AUROC chỉ gồm peptide đủ hai lớp, khác population MAE. [NC-16]

## Bằng chứng mạnh nhất: mở miền train giảm lỗi

So trên cùng dữ liệu test, D−B có ΔMAE ≈ −0,02577, CI điều chỉnh [−0,03381; −0,01829]. E−B có ΔMAE ≈ −0,02996, CI [−0,04166; −0,01882]. Cả hai hỗ trợ giảm sai số trung bình, nhưng cận gần 0 chưa vượt mức −0,02. Vì vậy không phát biểu chắc rằng mức giảm tối thiểu 0,02 đã được chứng minh trên toàn khoảng tin cậy. [NC-16]

![CI chênh lệch full-PSI. Âm có lợi cho mô hình đứng trước; đường tại 0 chỉ mốc không khác biệt. Các phép phạm vi PSI và phép mô tả kiến trúc có mức điều chỉnh khác nhau.](assets/figures/fullpsi-intervals.pdf){width=96%}

CNN-D so pointwise-D giảm MAE khoảng 0,00534, CI mô tả [−0,01017; −0,00090]. Điều này hỗ trợ bước trộn lân cận của head trong cấu hình đã chạy. mCNN-E và CNN-D chỉ cách nhau khoảng 0,00051 ở trung bình: chưa có căn cứ chọn một “người thắng” ổn định từ thứ hạng đó. [NC-16; NC-17]

## Trung bình toàn tập có thể che sự đánh đổi

![MAE theo tầng PSI. Mỗi tầng chứa số peptide khác nhau; các điểm là sai số macro trong tầng.](assets/figures/psi-strata.pdf){width=95%}

Phần cải thiện lớn nằm ở PSI cao. Ở tầng PSI ≤ 3 có 91 peptide, MAE B/D/E khoảng 0,4227/0,4215/0,4269; E không tốt nhất. Ở tầng >5 có 23 peptide, các giá trị khoảng 0,5094/0,3718/0,3207. Một mô hình cân bằng tầng có thể ưu tiên miền trước đây yếu hơn và đổi lại một phần chất lượng miền thấp. [NC-16]

**Guardrail** là tiêu chí bảo vệ một thuộc tính quan trọng khi tối ưu mục tiêu chính. AUROC dương miền PSI ≤3 của E so B giảm khoảng 0,0057, với CI [−0,0101; −0,0014]; cận chạm qua ngưỡng giảm 0,01. Không bỏ guardrail chỉ vì MAE toàn tập đẹp hơn. [NC-16]

## Chuyển giao scanning có ích ở đây, nhưng không phải mọi cách thêm nhãn

CNN one-hot pretrain scanning rep1 giảm MAE so scratch từ {{SCRATCH_D}} xuống {{SCAN_PRETRAIN_D}}. Dùng trung bình hai lần đo cho số gần tương đương; chưa chứng minh vượt rep1. Ngược lại, một cách trộn nhãn có trọng số chất lượng cho Ridge có MAE khoảng 0,4118, kém saturation-only D khoảng 0,4078. [NC-16]

Audit hậu nghiệm tách ô thành 20 kiểu thay thế có ở scanning và 360 kiểu còn lại. Nhánh pretrain cải thiện ở cả hai phần trong thiết kế đã lưu. Điều này gợi ý chuyển giao vượt đúng các kiểu đã thấy, nhưng là phân tích hậu nghiệm và chưa xác nhận cơ chế sinh học. [NC-17]

## Cạm bẫy đường cong ensemble

![Learning curve full-PSI của Ridge. Đường trung bình seed và đường ensemble trả lời hai câu hỏi khác nhau.](assets/figures/ensemble-learning-curve.pdf){width=94%}

Ở mức 25%, MAE trung bình seed khoảng 0,4413 nhưng ensemble khoảng 0,4154. Mỗi seed có thể dùng một tập con khác; hợp các tập con phủ hơn 25%. Vì vậy không viết “chỉ cần một phần tư nhãn đã bằng toàn bộ dữ liệu” từ đường ensemble. Để bàn hiệu quả mẫu của một model, phải xem đường trung bình seed và cấu trúc lấy mẫu. [NC-17]

**Hướng tiếp tục:** giữ W5 làm đối chứng; kiểm chuyển giao và head ngữ cảnh. Kết quả mở miền có lợi cho MAE chưa đủ để thay model phục vụ, suy rộng sang mọi pLM hoặc gọi là kiểm chứng held-source T.

::: {.exercise title="Tự kiểm 12"}
1. Vì sao E có MAE toàn tập tốt hơn B nhưng chưa qua mọi guardrail?
2. CI D−B hoàn toàn âm đã chứng minh giảm ít nhất 0,02 chưa?
3. Tại sao ensemble 25% không tương đương một model train 25%?
4. Một kết quả của ESM2-35M có chứng minh Ankh/ProtT5 cũng tương tự không?
:::
