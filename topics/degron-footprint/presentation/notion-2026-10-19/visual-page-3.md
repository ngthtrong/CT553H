![Kết quả nội bộ 18/10/2026: AUROC mức ô, macro theo peptide. Trục bắt đầu ở 0,70. Trần 0,9519 là trần đo lường, không phải hiệu năng có thể cam kết từ trình tự. Degformer học lại mới có một seed; không đọc chú thích ba seed như áp dụng cho mọi hàng.](notion-file-block://90696630-05d5-47a4-b5f7-394bee5c430f/7f759dfe-04ed-4a5f-973a-3073058095f1?space_id=e28cf6fd-fc68-4d6f-a1fc-146177044888&name=fig-benchmark.png)
**Kết quả nội bộ ngày 18/10/2026.** AUROC mức ô, macro theo peptide; chia cụm cov80, ghép cặp theo peptide và bootstrap theo cụm.
- **Học trực tiếp saturation:** ridge M3 **0,8082**; ΔPAP **0,7693**. Chênh lệch **+0,0389**, CI 95% **\[0,0216; 0,0571\]**.
- **Chuyển giao:** M3 **0,7273**; phải trình bày riêng vì khác ngân sách nhãn.
- **Nguồn thông tin:** thành phần lân cận ±3 có ích hơn thành phần cả peptide trong phân tích hiện có; chưa thể gọi đó là bằng chứng vị trí thắng thành phần.
- **Năm mô hình sức chứa lớn hơn** đã thử đều thua ridge M3. Kiến trúc Degformer học lại dưới cov80 đạt **0,7500**; kết quả này còn giới hạn một seed và chưa hiệu chỉnh siêu tham số.
**Đối chứng Degformer:** checkpoint có chồng lặp peptide với tập test. Bỏ các ô trùng khít vẫn không tạo tập peptide độc lập; không dùng điểm checkpoint để tuyên bố tổng quát hóa sạch.
**G2 chưa hoàn tất:** cần thành phần kiến trúc mới có lợi ổn định so baseline mạnh, ablation và khoảng bất định. Học từ nhãn mức túi và tăng lượng nhãn vẫn là hướng cần kiểm nghiệm.
**Ứng dụng dự kiến:** nhập peptide → ma trận hiệu ứng → chọn đột biến và đối chứng → xuất kết quả kèm bất định, nguồn nhãn và phạm vi áp dụng. Harness cho phép chạy lại mô hình cùng điều kiện. Phần mềm chưa xây dựng.
**Giới hạn:** nhãn residue hiện cùng nguồn Zhang; chưa xác lập liên hệ hiệu ứng residue với tính gây bệnh. Đề tài chưa được GVHD duyệt khung chính thức theo hồ sơ hiện tại.
[Nghiên cứu PAP](https://doi.org/10.1126/sciadv.adz3483) · [Mã nguồn Degformer](https://github.com/Alpine2048/Degformer)
Số thực nghiệm nội bộ được đối soát từ `research/g2-saturation-2026-10-18/` và `research/g2-extension-2026-10-18/` trong repo CT553H; trạng thái chính thức theo `DECISIONS.md`.
## Các thử nghiệm kiến trúc nói gì?
Các mô hình đã thử gồm cổng sigmoid, FiLM, bilinear, ridge có tích chéo và kiến trúc Degformer huấn luyện lại. Chúng chưa vượt ridge M3 trong các điều kiện đã chạy. Đây là bằng chứng về **những thiết kế và giao thức đã thử**, chưa chứng minh mọi kiến trúc phức tạp đều vô ích.
Kết quả gợi ý nên khảo sát vai trò lượng nhãn, nhưng nguyên nhân do lượng nhãn chưa được tách riêng bằng một thí nghiệm kiểm soát. Hướng khảo sát này còn là đề xuất chờ xác nhận.
## Vì sao phải kiểm tra Degformer riêng?
Ngay cả khi bỏ các ô có trình tự trùng khít với dữ liệu huấn luyện, các phép thay thế khác của cùng peptide vẫn có thể đã xuất hiện trong train. Vì vậy, “không trùng đúng ô” không tương đương “peptide chưa thấy”.
Huấn luyện lại kiến trúc dưới cov80 giúp kiểm tra một câu hỏi khác: kiến trúc đó hoạt động ra sao với ngân sách nhãn hiện tại? Nó không tái lập toàn bộ lợi ích tiền huấn luyện của checkpoint công bố.
## Một thành phần phương pháp cần vượt qua kiểm tra nào?
1. So sánh với ridge M3 và ΔPAP trong cùng chế độ nhãn và cách chia tập.
2. Bỏ hoặc thay thành phần bằng ablation để đo lợi ích riêng.
3. Kiểm tra tính ổn định giữa các seed, báo chênh lệch ghép cặp cùng khoảng bất định theo cụm.
4. Đối chiếu tiền lệ để xác định phần nào thực sự mới.
Các bước này là cách diễn giải yêu cầu kiểm chứng hiện có; không tạo ngưỡng nghiệm thu hoặc quyết định nghiên cứu mới.
<mention-page url="https://app.notion.com/p/3fe4c97ef69581ed968df52b445de084">Degron — Lộ trình dự đoán hiệu ứng đột biến</mention-page>
