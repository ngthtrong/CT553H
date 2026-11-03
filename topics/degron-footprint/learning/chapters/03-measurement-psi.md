# Từ tế bào phát sáng đến PSI

## Vì sao thí nghiệm dùng reporter?

Để đo trực tiếp mọi tương tác phân hủy ở quy mô hàng nghìn peptide là khó. Một **reporter** tạo tín hiệu dễ quan sát khi mang peptide cần khảo sát. Ở dữ liệu Zhang được pipeline dùng, peptide gắn ở đầu C của **GFP**, protein phát huỳnh quang xanh. **DsRed** cung cấp tín hiệu tham chiếu trong thiết kế đo.

**Construct** là thiết kế DNA quy định reporter mang một peptide/đột biến cụ thể. Nó khác một tế bào: nhiều tế bào có thể biểu hiện cùng construct. **Thư viện** là tập nhiều construct để đo song song. Một mutant trong thư viện vẫn phải có định danh để sau cùng nối phép đo về đúng trình tự. [TL-03; NC-01]

Tỉ lệ GFP/DsRed giúp xét tín hiệu GFP tương đối với kênh chuẩn. Nếu peptide làm reporter bị loại bỏ mạnh hơn trong bối cảnh đo, GFP tương đối thường thấp hơn. Tỉ lệ không phải số lượng phân tử tuyệt đối hoặc thước đo cơ chế trực tiếp.

## FACS, bin và read là ba lớp khác nhau

**FACS** là phương pháp phân loại tế bào theo tín hiệu huỳnh quang. Từng tế bào được đo rồi thu vào một **bin**, tức nhóm theo khoảng tín hiệu. Thiết kế chính dùng sáu bin, từ reporter kém bền hơn đến bền hơn theo GFP/DsRed.

Sau thu bin, DNA được tách, phần mã hóa liên quan được khuếch đại bằng **PCR** và giải trình tự. Một **read** là một lượt đọc trình tự DNA. Sau ánh xạ read về construct, ta có count cho mỗi construct ở mỗi bin.

::: {.limit title="Không đánh đồng đơn vị"}
Một read không bằng một tế bào, một tế bào không bằng một peptide và một peptide không bằng một mẫu độc lập. Count phụ thuộc các bước chuẩn bị và đọc. Cùng construct xuất hiện ở nhiều bin vì quần thể tế bào có phân bố tín hiệu, không phải tất cả tế bào giống hệt nhau.
:::

![Luồng từ construct đến nhãn. Đây là sơ đồ diễn giải quy trình; không phải ảnh chụp một lượt thí nghiệm mới của sinh viên.](assets/diagrams/gps-measurement.pdf){width=87%}

## Tại sao không lấy count thô tính luôn?

Giả sử một bin được giải trình tự sâu gấp đôi các bin khác. Nó có thể có nhiều read hơn ngay cả khi không có nhiều construct tương đối hơn. Để giảm ảnh hưởng tổng độ sâu giữa các bin, pipeline dựng lại count chuẩn hóa theo tổng read của từng bin trong điều kiện được xét.

Gọi $T_i$ là tổng read ở bin $i$, $b_i$ là read thô của construct đang xét. Công thức đang dùng là:

$$f_i=\frac{T_1}{T_i},\qquad nb_i=b_i f_i,\qquad
\mathrm{PSI}=\frac{\sum_{i=1}^{6}i\,nb_i}{\sum_{i=1}^{6}nb_i}.$$

`nb` là count đã chuẩn hóa. Vì nhân một hệ số thực, tổng `nb` có thể không nguyên. Ngưỡng đọc áp vào tổng chuẩn hóa cần được hiểu đúng, không được đổi tên thành “ít nhất 10 tế bào”. [NC-01]

## Một phép tính nhỏ, làm từ đầu

Giả sử count sau chuẩn hóa là $[0,50,50,0,0,0]$. Tổng là 100; tử số $2\times50+3\times50=250$; PSI bằng 2,5. Nếu mutant có $[0,0,0,50,50,0]$, PSI bằng 4,5. Cả hai quần thể không nằm ở một bin duy nhất; PSI tóm tắt phân bố bằng trung bình có trọng số.

![Ví dụ tự đặt. Các count trong hình chỉ phục vụ tính toán, không lấy từ một mẫu đã đo.](assets/figures/psi-worked-example.pdf){width=96%}

Vì bin chạy từ 1 tới 6, PSI nằm trong khoảng đó khi các count không âm và tổng dương. Tổng bằng 0 thì công thức không có nghĩa; không được tự gán PSI=0 vì 0 nằm ngoài thang đo.

**Chiều cần nhớ:** PSI thấp tương ứng reporter kém bền hơn trong thiết kế Zhang; PSI cao tương ứng bền hơn. PSI không phải thời gian bán hủy theo giờ. Nó cũng không phải xác suất: PSI=4 không có nghĩa 400% hay 4%.

## Đề tài đã kiểm phép dựng này ra sao?

Pipeline đã dựng PSI từ count thô, rồi đối chiếu với bảng tác giả. Trên 261.865 giá trị so được, sai lệch tuyệt đối lớn nhất xấp xỉ $5\times10^{-7}$, dưới dung sai $10^{-6}$. Hồ sơ cũng giữ các trường hợp lỗi header và cách xử lý, thay vì sửa yên lặng rồi bỏ dấu vết. [NC-01]

Đây là phép kiểm rất hữu ích: nếu dựng sai đại lượng đích thì mô hình mạnh đến đâu cũng học sai câu hỏi. Tuy nhiên, khớp bảng tác giả chỉ xác nhận đường tính toán đã kiểm; nó không chứng minh assay đo được mọi cơ chế sinh học cần quan tâm.

**Vì sao giữ nguồn và điều kiện riêng?** Các file thuộc điều kiện tế bào khác nhau không tự trở thành replicate. BAG6 WT không phải “lần đo thứ ba” của saturation. Gộp nhầm điều kiện sẽ thay đổi ý nghĩa nhãn.

::: {.exercise title="Tự kiểm 03"}
1. Với count chuẩn hóa $[0,0,20,60,20,0]$, tự tính PSI.
2. Vì sao dùng tổng read từng bin để chuẩn hóa, thay vì chỉ chia count của mỗi construct cho tổng của riêng nó?
3. Một file có đủ cột và không lỗi cú pháp đã đủ để biết đó là replicate chưa?
:::
