# Sinh học nền: từ thông tin đến một protein có thể bị phân hủy

## DNA, gene, RNA và protein khác nhau thế nào?

**DNA** là phân tử lưu thông tin di truyền. **Gene** là một vùng thông tin có thể được biểu hiện thành sản phẩm chức năng. Ở phạm vi đơn giản cần cho sách này, gene mã hóa protein được dùng để tạo **mRNA**, bản RNA mang thông tin mã hóa, rồi tạo chuỗi protein. Không phải mọi gene đều mã hóa protein.

**Phiên mã** là tạo RNA từ khuôn DNA; **dịch mã** là ribosome đọc thông tin mRNA để xây chuỗi amino acid. **Ribosome** là bộ máy tổng hợp protein trong tế bào. Đừng đảo hai thuật ngữ: DNA → RNA là phiên mã, mRNA → chuỗi amino acid là dịch mã. [TL-01, TL-02]

Có thể liên tưởng DNA như kho công thức, mRNA như bản hướng dẫn đang được sử dụng và ribosome như bộ máy lắp ráp. Liên tưởng dừng ở đó: tế bào không phải chương trình chỉ có một đầu ra tất định; mức biểu hiện, cấu trúc và tương tác phân tử ảnh hưởng kết quả.

## Amino acid, residue, peptide và vị trí

**Amino acid** là loại đơn vị cấu tạo protein; trong bài toán ta xét 20 loại chuẩn. Ký tự `A`, `V`, `M` là mã một chữ của các loại amino acid, không phải nucleotide DNA. **Residue** là một amino acid ở một vị trí cụ thể trong chuỗi. A ở vị trí 2 và A ở vị trí 4 cùng loại nhưng là hai residue khác nhau.

Ví dụ, A là alanine, V là valine, M là methionine, L là leucine và K là lysine. Mã một chữ giúp viết ngắn cả chuỗi; không cần suy tính chất hóa học chỉ từ việc hai ký tự đứng gần nhau trong bảng chữ cái. Trong heatmap, mỗi hàng là một loại thay vào, không phải một tế bào hoặc một lần đo.

**Peptide** là đoạn chuỗi ngắn; ở assay chính của đề tài, cửa sổ dài 28 residue. **Protein** thường dài hơn và có tổ chức cấu trúc/chức năng rộng hơn. Một đoạn peptide tách khỏi protein không bảo toàn mọi tương tác và cấu trúc vốn có.

::: {.worked title="Ví dụ xuyên suốt: chuỗi tự đặt"}
WT minh họa: `M A L A K L A`. Đánh số từ 1: M là vị trí 1, A thứ hai trong chuỗi là vị trí 4. `A4V` tạo chuỗi `M A L V K L A`. Đây là thay một loại amino acid tại một vị trí, không thêm hoặc xóa residue. Ví dụ ngắn để học ký hiệu, không thuộc dữ liệu 28-mer.
:::

Trong sách, vị trí sinh học dùng chỉ số bắt đầu từ 1. Mảng Python thường bắt đầu từ 0. Vì thế residue vị trí 4 tương ứng phần tử chỉ số 3. Nhầm một đơn vị có thể tạo ma trận trông hợp lệ nhưng gán nhãn sai toàn bộ.

## Vì sao protein cần được phân hủy?

Lượng protein trong tế bào phụ thuộc cả tạo mới lẫn mất đi. **Phân hủy protein** là quá trình loại bỏ protein thông qua các hệ thống tế bào; nó góp phần kiểm soát chất lượng và điều hòa hoạt động. Reporter tích lũy nhiều hơn có thể liên quan thay đổi độ bền, nhưng tín hiệu cũng cần được hiểu trong thiết kế đo và các đối chứng.

**Ubiquitin** là một protein nhỏ tham gia đánh dấu và điều hòa nhiều quá trình. Trong hệ **ubiquitin–proteasome**, các enzyme cùng phối hợp để gắn ubiquitin; **E3 ligase** góp phần vào tính chọn lọc cơ chất. **Proteasome** là phức hợp có thể phân giải các protein được đưa tới phù hợp. Không phải mọi dạng gắn ubiquitin đều mang cùng ý nghĩa hoặc chắc chắn dẫn tới phân hủy.

**Degron** là tín hiệu góp phần vào việc một protein được nhận diện để phân hủy trong bối cảnh phù hợp. Tín hiệu có thể nằm trong chuỗi hoặc ở đầu protein. Trong đề tài, đối tượng đo là đoạn peptide gắn vào reporter; không phải toàn bộ đường điều hòa trong tế bào người. [TL-03]

![Sơ đồ khái niệm. Nhánh UPS mô tả một đường có thể liên quan phân hủy; không khẳng định mọi protein đều đi theo chuỗi này.](assets/diagrams/gene-protein-degradation.pdf){width=88%}

## “Degron tự trị” giải quyết gì và bỏ qua gì?

Một peptide có thể tự mang đủ tín hiệu làm reporter kém bền trong hệ đo, nên hữu ích để nghiên cứu ở quy mô lớn. Lựa chọn này giúp tách một đoạn ngắn thành đầu vào có chiều dài ổn định và đo được hàng loạt đột biến.

Đổi lại, peptide mất nhiều bối cảnh của protein nguyên vẹn: cấu trúc ba chiều, khả năng lộ bề mặt, tương tác với đối tác, vị trí trong tế bào và các sửa đổi sau dịch mã. **Bối cảnh** ở đây là điều kiện xung quanh ảnh hưởng hoạt tính; nó không chỉ là vài ký tự lân cận trong chuỗi.

Vì vậy, việc ứng dụng chia toàn protein thành nhiều tile chỉ tăng số cửa sổ được chấm. Nó không tạo ra một mô hình đã đo thời gian sống của protein nguyên vẹn.

## Quan sát không đồng nghĩa cơ chế trực tiếp

Giả sử đột biến làm tín hiệu GFP tương đối tăng. Cách nói được phép là reporter tích lũy hoặc bền hơn theo phép đo được kiểm soát. Giả thuyết “đột biến làm E3 khó nhận diện trực tiếp” cần bằng chứng thêm. Có thể có protein trung gian hoặc một cơ chế khác ảnh hưởng tín hiệu.

Ngay cả khi làm mất E3-X rồi phục hồi E3-X làm hiệu ứng biến mất rồi xuất hiện lại, kết quả vẫn cần được phân biệt giữa **E3-X tham gia điều hòa** và **E3-X gắn trực tiếp vị trí đó**. Đề tài tính toán hiện không thực hiện chuỗi xác nhận cơ chế này.

::: {.exercise title="Tự kiểm 02"}
1. Viết đúng hai mũi tên phiên mã và dịch mã.
2. Với WT `MALAKLA`, viết mutant A2V và A4V; đếm số residue thay đổi.
3. Nêu hai lý do peptide assay chưa đại diện chắc chắn cho protein nguyên vẹn.
4. Sửa câu “GFP tăng chứng minh E3 không gắn được”.
:::
