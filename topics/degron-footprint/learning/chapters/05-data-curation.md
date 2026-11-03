# Dữ liệu: vì sao có file chưa có nghĩa là có nhãn dùng được?

## Bắt đầu bằng endpoint và đơn vị đo

**Endpoint** là đại lượng thực sự được ghi nhận: ví dụ PSI của reporter, điểm hoạt tính cả peptide, abundance hoặc nhãn bệnh. Hai bảng đều có cột `score` không làm chúng tương đương. **Assay** là thiết kế phép đo cụ thể: vật mang, chiều dài peptide, tế bào, điều kiện và cách biến tín hiệu thành số.

Đề tài đã khảo sát nhiều nguồn nhưng lõi full-PSI vẫn là nhãn Zhang và trình tự/nhóm UniProt. Quyết định giữ lõi hẹp giúp một thay đổi về mô hình không đồng thời kéo theo thay đổi endpoint khó kiểm soát. [NC-15, NC-21]

**UniProt** là nguồn bản ghi trình tự và chú giải protein. **ClinVar** tập hợp diễn giải về biến thể và ý nghĩa sức khỏe; **MaveDB** lưu dữ liệu các phép đo hiệu ứng biến thể quy mô lớn. Trong đề tài, vai trò thực tế của mỗi nguồn do endpoint và audit quyết định, không do tên cơ sở dữ liệu. **Abundance** là mức hiện diện/lượng tương đối; nó không mặc nhiên bằng PSI. [NC-21; NC-23]

| Nguồn | Dùng vào việc gì? | Vì sao giữ ranh giới? |
|---|---|---|
| Zhang scanning/saturation | Nhãn hiệu ứng đột biến và transfer có điều kiện | Cần WT, QC, replicate và chống chồng nhóm |
| UniProt | Trình tự tham chiếu, accession, tọa độ và tương đồng | Phiên bản trình tự ảnh hưởng ánh xạ |
| Voutsinos/PAP | Đối chứng ΔPAP và thí nghiệm tiền huấn luyện tile | Nhãn cả peptide khác nhãn phép thay |
| Koren đầu C | Audit nguồn có nhãn mutation | Khác thư viện/thang bin và ít nhóm mới |
| MaveDB/ClinVar | Khảo sát endpoint hoặc chú giải có điều kiện | Điểm chức năng/nhãn bệnh không tự là ΔPSI |
| Larsen/MetaDegron | Bối cảnh, phương pháp và phạm vi nguồn | Tile/motif/E3 không tự cung cấp nhãn residue tương ứng |

**Accession** là mã nhận diện bản ghi protein. **Provenance** là nguồn gốc có thể truy vết: lấy từ đâu, phiên bản nào, ai/công cụ nào xử lý và bằng quy tắc gì. **Giấy phép** xác định điều kiện sử dụng/phân phối, độc lập với việc file tải được.

## Từ protein dài đến peptide có tọa độ

Một **tile** là cửa sổ dọc protein. Trong quy tắc của dữ liệu chính, tile dài 28 và bước 23, nên hai tile liền nhau chồng 5 residue. Tile thứ $n$ bắt đầu ở $(n-1)\times23+1$ theo chỉ số sinh học.

Ví dụ tự đặt: tile 2 bắt đầu ở vị trí protein 24. Residue thứ 4 trong tile đó ứng với vị trí protein 27. Muốn chú giải một biến thể, phải kiểm amino acid WT ở vị trí 27 thực sự trùng với trình tự của snapshot đang dùng; chỉ trùng tên gene chưa đủ.

**Mapping** là ánh xạ các hệ tọa độ/định danh. Nếu protein đã đổi phiên bản hoặc thư viện dùng đoạn đầu C không đúng cửa sổ đầy đủ, công thức tile có thể không khớp. Quy tắc hiện hành được kiểm trên dữ liệu có trình tự; các trường hợp không khớp phải loại hoặc ghi trạng thái, không tự sửa để tăng độ phủ.

## QC: từ dữ liệu thô đến nhãn hợp lệ

**Quality control (QC)** là tập kiểm kỹ thuật trước fitting: độ sâu count, đủ WT nội tại, amino acid hợp lệ, trình tự và vị trí khớp, replicate giao nhau hợp lệ, giá trị hữu hạn. **Nonfinite** gồm NaN hoặc vô hạn; chúng có thể làm một phép fit lỗi hoặc lan thành dự đoán không dùng được.

Thiếu giá trị không có một cách xử lý duy nhất. Một ô không đủ read nên giữ lý do thiếu; một peptide không lấy được trình tự không được gán chuỗi đoán; một accession thiếu cụm không được mặc nhiên coi là một nhóm sinh học mới độc lập.

![Pipeline dữ liệu. Tách bước QC, mapping, nhãn và nhóm giúp biết lỗi nào ảnh hưởng kết luận nào.](assets/diagrams/data-pipeline.pdf){width=89%}

::: {.choice title="Vì sao không lọc theo PSI ngay từ đầu mãi mãi?"}
Ngưỡng PSI từng giúp định nghĩa miền peptide degron cho benchmark ban đầu. Nhưng bài toán hồi quy hiệu ứng có thể học được cả khi WT ổn định hơn. Vì vậy cần tách **QC kỹ thuật** khỏi **lựa chọn population khoa học**. Full-PSI giữ toàn dải sau QC, rồi thay đổi phạm vi train trong thí nghiệm có đối chứng.
:::

## Ba con số 91, 176 và 235 không mâu thuẫn

**91 peptide** là outer-test lịch sử sau ngưỡng PSI(WT)≤3. **176 peptide** là pool mở rộng tới PSI(WT)≤4, gồm thêm 85 peptide; từng fold vẫn loại nhóm test khỏi train. **235 peptide** là population saturation full-PSI sau QC kỹ thuật, với phép chia nhóm riêng. [NC-02, NC-04, NC-15]

Bạn không được nói “tập test đã tăng từ 91 lên 176” trong thiết kế P0. Cũng không được so trực tiếp AUROC 0,8208 trên test cũ với một AUROC full-PSI rồi quy toàn bộ chênh lệch cho mô hình.

Full-PSI có {{SAT_CELLS}} ô saturation và {{SCAN_CELLS}} ô scanning hỗ trợ, nhưng số nhóm độc lập hữu hiệu nhỏ hơn số ô rất nhiều. Số ô lớn chủ yếu cung cấp nhiều phép thay trong cùng các bối cảnh peptide.

## Vì sao audit nguồn ngoài có kết quả âm vẫn hữu ích?

Koren có dữ liệu mutation phù hợp để khảo sát, nhưng audit chỉ tìm được 5 nhóm mới so yêu cầu 20 nhóm đã chốt. Nguồn không được nhập vào train theo gate đó; vai trò có thể là case kiểm tra ngoài cho một lớp degron khác, với điều kiện endpoint và quyền dùng được giữ rõ. [NC-19]

Tương tự, thiếu nhãn E3 đủ điều kiện khiến đề tài không lấy nhận diện E3 làm nhiệm vụ chính. Việc pivot sang hiệu ứng mutation dựa vào nhãn đo có thể dựng được; đó là quyết định thu hẹp câu hỏi theo dữ liệu, không phải bằng chứng E3 không quan trọng. [NC-22]

Audit ClinVar cũng đã kiểm độ phủ và amino acid WT thay vì chỉ nối theo tên gene. Nó cho thấy “biến thể nằm trong tile tham chiếu” khác “biến thể có đúng ô đã đo”. Đây là căn cứ để giữ annotation như ngữ cảnh tham khảo, không biến độ phủ trên danh mục thành bằng chứng model dự đoán chính xác ngoài tập nhãn. [NC-23]

::: {.exercise title="Tự kiểm 05"}
1. Một bảng score abundance có thể nối vào ΔPSI bằng cách đổi tên cột không? Vì sao?
2. Tính vị trí protein của residue 10 trong tile 3 theo quy tắc 28/23.
3. Phân biệt QC kỹ thuật với lọc population theo WT-PSI.
4. Nếu một nguồn có 2.000 ô nhưng chỉ 5 protein groups mới, vì sao chưa thay được nguồn có nhiều nhóm độc lập?
:::
