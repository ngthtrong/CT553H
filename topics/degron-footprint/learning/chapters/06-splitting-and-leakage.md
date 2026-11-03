# Chia dữ liệu: mô hình đã thấy “họ hàng” của mẫu test chưa?

## Rò rỉ dữ liệu không chỉ là trùng một dòng

**Train** là phần dùng học tham số; **validation** là phần dùng chọn cấu hình; **test** là phần dùng đánh giá sau lựa chọn. **Data leakage**, rò rỉ dữ liệu, xảy ra khi thông tin lẽ ra bị giữ lại lại tác động vào fitting hoặc lựa chọn.

Ví dụ minh họa: một peptide có 500 phép thay đo. Nếu chia ngẫu nhiên từng ô, 400 ô của cùng WT có thể vào train, 100 ô vào test. Mô hình đã thấy bối cảnh gần như nguyên vẹn của peptide test. Score cao khi đó trả lời câu hỏi nội suy các phép thay còn lại, chưa chắc trả lời tổng quát hóa sang peptide khác.

Ngay cả hai peptide có accession khác nhau vẫn có thể thuộc protein tương đồng. **Homology** nói về quan hệ nguồn gốc tiến hóa; **sequence similarity** là mức giống trình tự đo được. Các heuristic tương đồng giúp gom đối tượng có nguy cơ chia sẻ tín hiệu, nhưng không chứng minh mọi protein ngoài nhóm đều độc lập hoàn toàn.

## MMseqs2 và cov80/cov50 có nghĩa gì?

**Clustering** là gom thành nhóm theo quy tắc. **Sequence identity** là tỉ lệ residue giống nhau trong vùng được căn chỉnh; **coverage** là mức phần trình tự được vùng căn chỉnh phủ. MMseqs2 là công cụ tìm kiếm/phân cụm trình tự được pipeline sử dụng.

Tên cov80 trong hồ sơ dự án liên quan ngưỡng coverage 80%, với identity chính 30%; cov50 dùng mức coverage thấp hơn trong một số kiểm độ nhạy/hits bổ sung. Đây không phải “80% amino acid giống nhau”. Cần đọc cùng identity, chiều coverage và độ dài căn chỉnh tối thiểu.

V3 bắt đầu từ cụm toàn proteome, bổ sung hits cov50 hai chiều và hợp trình tự trùng. **Union** nghĩa là nếu hai đối tượng được nối bởi quan hệ phải giữ cùng phía, nhóm của chúng được hợp. Quan hệ có tính bắc cầu: A nối B, B nối C có thể làm A/B/C cùng nhóm dù A/C không phải cặp giống nhất trực tiếp. [NC-15; KH-02]

## Nested evaluation diễn ra theo thứ tự nào?

**Fold** là một phần trong phép chia đánh giá. Năm outer fold cho phép mỗi nhóm lần lượt nằm ở test, trong khi các nhóm khác tạo phần học. **Outer** chỉ lớp đánh giá ngoài. **Inner** là chia train/validation bên trong phần được phép học để chọn siêu tham số.

![Luồng nested evaluation. Outer-test không đi vào bước chọn α/epoch; nó chỉ được dùng tại khối đánh giá cuối.](assets/diagrams/nested-splits.pdf){width=91%}

Trong một outer fold:

1. Giữ riêng outer-test theo nhóm.
2. Chia outer-train thành inner-train và inner-validation theo nhóm.
3. Fit mọi phép xử lý cần học, rồi fit ứng viên trên inner-train.
4. Chọn α hoặc epoch bằng loss inner-validation.
5. Refit trên phần outer-train hợp lệ bằng cấu hình đã chọn.
6. Dự đoán outer-test; lưu khóa mẫu, nhãn, score, seed, fold và identity.

**Hyperparameter** là cấu hình do quy trình lựa chọn quyết định, như α Ridge hoặc số epoch. Nó khác trọng số mô hình học bằng tối ưu. Nếu nhìn test để thử nhiều α rồi chọn cái tốt nhất, test đã trở thành validation dù tên file vẫn ghi test.

## Những bước cũng có thể rò rỉ

**Scaler** học mức trung bình/độ lệch của feature; **PCA** học trục giảm chiều. Fit chúng trên toàn bộ dữ liệu trước chia fold cũng cho chúng nhìn phân bố test. Vì vậy chúng thuộc pipeline fit, không phải bước chuẩn bị “vô hại” có thể đặt tùy ý.

Pre-training bằng scanning cũng phải loại nhóm ngoài được giữ lại. Nếu một peptide test có mặt ở scanning và saturation, chỉ đổi tên nguồn không làm nó độc lập. V3 tách scanning development, nguồn giữ lại và phần chồng saturation trước fitting. [KH-02]

::: {.worked title="Một ví dụ kiểm nhóm, không phải kiểm dòng"}
Ví dụ tự đặt: nhóm G1 có peptide A và B; G2 có C. A ở train, B ở test là không đạt luật chia nhóm, dù sequence của A không trùng hoàn toàn B. Khi lấy G1 làm test, cả A và B phải rời phần dùng fit và chọn cấu hình của fold đó.
:::

## OOF, seed và ensemble

**Out-of-fold (OOF)** là dự đoán cho mỗi mẫu khi mẫu ấy ở outer-test, từ model không học nhóm test tương ứng. Ghép các fold tạo bộ OOF phủ population. OOF đầy đủ là dữ liệu để tính metric, không có nghĩa một model duy nhất đã được train toàn bộ dữ liệu để phục vụ.

**Seed** là giá trị khởi tạo bộ sinh số giả ngẫu nhiên. Seed 17/29/43 là các hằng số giúp tái lập, không có ý nghĩa sinh học đặc biệt. Chúng có thể thay inner split, khởi tạo mạng hoặc thứ tự batch; chúng không tự tạo ba bộ dữ liệu độc lập.

**Ensemble** lấy trung bình dự đoán của nhiều thành viên rồi mới tính metric. Trung bình ba AUROC không bằng AUROC của score trung bình. Một lợi ích ensemble có thể phản ánh giảm phương sai, không nhất thiết là một architecture đơn lẻ đã mạnh hơn.

## Development, held-source và external

**Development** là dữ liệu đã tham gia hình thành lựa chọn trong quá trình nghiên cứu. CV có kiểm soát vẫn có thể là development nếu ta khảo sát nó nhiều lần. **Held-source** là nguồn/nhóm giữ lại theo thiết kế hiện hành; nếu đã từng thăm dò nguồn trong lịch sử thì không gọi hoàn toàn chưa xem. **External validation** cần mô tả độc lập về nguồn, assay, mẫu và quyết định lựa chọn.

Một test tốt không chỉ là file có tên `test`. Ý nghĩa nằm ở luồng thông tin và lịch sử quyết định.

::: {.exercise title="Tự kiểm 06"}
1. Vì sao shuffle từng ô dễ làm bài toán trông dễ hơn?
2. Scaler không dùng y; fit scaler trên test có luôn được chấp nhận không?
3. Vẽ một outer fold và đánh dấu nơi được chọn epoch.
4. Vì sao 3 seed và 5 fold không phải 15 thí nghiệm sinh học độc lập?
:::
