# Tạo nhãn ΔPSI và đọc ma trận đột biến

## WT không có nghĩa là “không có degron”

**WT**, viết tắt của *wild type*, là trình tự tham chiếu trước phép thay. **Mutant** là trình tự sau thay đổi. WT có thể đã mang degron mạnh; nó không mặc nhiên bền nhất, khỏe nhất hoặc không có hiệu ứng.

Ta cần WT để trả lời câu hỏi tương đối: so với cùng peptide trước thay, mutant ổn định hơn hay kém hơn bao nhiêu? Định nghĩa nhãn là:

$$\Delta\mathrm{PSI}=\mathrm{PSI}_{mutant}-\mathrm{PSI}_{WT}.$$

Trong ví dụ minh họa ở chặng trước, mutant 4,5 trừ WT 2,5 bằng **+2,0 điểm PSI**. Đây không phải xác suất 200%. Nếu mutant 1,8 còn WT 2,5, hiệu là −0,7: reporter mutant kém bền hơn trong assay.

## Vì sao scanning và saturation cần hai cách lấy WT?

**Scanning mutagenesis** khảo sát một phép thay theo quy tắc ở từng vị trí. Dữ liệu quét có construct `_mut0` làm mốc WT trong cùng điều kiện. Các loại amino acid thay vào chủ yếu là R/A/S, nên scanning không phủ đều 19 thay thế có thể có ở mỗi residue.

**Saturation mutagenesis** khảo sát nhiều amino acid tại mỗi vị trí. Bộ saturation không có `_mut0` riêng. Ở mỗi vị trí có một ô giữ nguyên loại amino acid WT, gọi là ô **đồng nghĩa ở mức protein**; nó có thể đổi codon nhưng không đổi amino acid.

Pipeline lấy median PSI của các ô này trong từng nửa replicate để làm WT nội tại. **Median** là trung vị, giá trị giữa sau sắp xếp; nó ít nhạy với một vài giá trị cực đoan hơn trung bình. Mốc WT của nửa A chỉ dùng với PSI mutant A; tương tự nửa B. Sau khi tạo hai ΔPSI, nhãn dùng trung bình hai lần đo hợp lệ. [NC-01, NC-02]

::: {.worked title="Vì sao phải trừ WT riêng từng replicate?"}
Ví dụ tự đặt: A có mutant 3,8, WT 2,2 ⇒ ΔA=1,6. B có mutant 3,5, WT 2,0 ⇒ ΔB=1,5. Nhãn trung bình là 1,55. Không lấy WT từ một điều kiện BAG6 khác vì cùng tên protein; điều kiện đo là một phần của định nghĩa nhãn.
:::

## 560 ô thiết kế, tối đa 532 phép thay thật

Với peptide 28 residue và 20 amino acid đích, bảng vị trí × amino acid có $28\times20=560$ ô. Ở mỗi vị trí, một ô trùng loại WT. Bỏ 28 ô không đổi amino acid còn $28\times19=532$ thay thế thật tối đa.

Số đo hợp lệ thực tế có thể thấp hơn do thiếu count hoặc không đạt QC. Không được điền 0 cho ô thiếu: 0 nghĩa đo được hiệu ứng gần không đổi, còn thiếu nghĩa chưa biết. Khi giao diện để ô WT trống, cần phân biệt đó là ô không chấm phép thay với một ô đo thất bại.

![Ký hiệu một phép thay. Hình dùng chuỗi tự đặt dài 7 residue để dễ đếm, không phải dữ liệu assay 28-mer.](assets/diagrams/mutation-unit.pdf){width=90%}

## Footprint là cách tổng hợp, không phải nhãn cơ chế

Một ô dương trong benchmark lịch sử được định nghĩa bằng $\Delta\mathrm{PSI}\ge1$. Nghĩa là mutant làm reporter bền hơn ít nhất một điểm theo thang này. Một **footprint** có thể được dựng từ các vị trí nhạy đột biến theo quy tắc cụ thể. Phải nêu rõ quy tắc: tính trên phép thay nào, ngưỡng nào và có yêu cầu độ phủ gì.

Ô dưới ngưỡng không đồng nghĩa “không có ảnh hưởng sinh học”. Một thay đổi +0,9 vẫn là thay đổi liên tục; nó chỉ thuộc phía âm của nhãn nhị phân đang dùng. Hồi quy học giá trị ΔPSI, còn AUROC chỉ xét thứ hạng so nhãn sự kiện được định nghĩa thêm.

Giới hạn vật lý từ PSI∈[1,6] là $1-PSI_{WT}\le\Delta PSI\le6-PSI_{WT}$. WT rất cao khó tạo ΔPSI dương lớn; điều đó không làm các peptide ấy vô ích cho hồi quy hoặc hiệu ứng âm. Đây là một lý do chuyển sang full-PSI phải thay đổi cách đọc metric.

## Đọc một hình có nhãn đo thật

![Dữ liệu đã lưu: peptide HIF1A tile 25. Màu biểu thị ΔPSI đo, xám là ô không có giá trị trong ma trận đã curate. Ví dụ được chọn để minh họa nhiều ô dương; không phải peptide đại diện ngẫu nhiên hoặc kiểm chứng mô hình.](assets/figures/hif-measured.pdf){width=100%}

Ví dụ HIF1A có trình tự `QDTDLDLEMLAPYIPMDDDFQLRSFDQL`. Trục ngang là 28 vị trí; trục dọc là amino acid thay vào. Đi theo một cột cho thấy các phép thay khác nhau tại cùng vị trí; đi theo một hàng cho thấy cùng amino acid đích ở nhiều vị trí. Tính nhạy phụ thuộc cả hai chiều. Hình là nhãn thực nghiệm đã xử lý theo pipeline lịch sử, không phải output CNN. [NC-18]

::: {.exercise title="Tự kiểm 04"}
1. WT=2,4 và mutant=3,1 cho ΔPSI bao nhiêu? Có đạt sự kiện ≥1 không?
2. Đọc khác nhau giữa “ô thiếu”, “ΔPSI=0” và “WT→WT”.
3. Với peptide 10 residue, có bao nhiêu ô thiết kế và bao nhiêu thay thế thật tối đa?
:::
