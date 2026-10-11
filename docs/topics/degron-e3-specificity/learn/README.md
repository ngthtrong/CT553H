# Hub học đề tài degron

Mở [index.html](index.html) trực tiếp bằng trình duyệt. Hub dẫn qua năm chặng: kiến thức nền → cơ chế và phép đo → bài toán tính toán → chín bài báo chính → phạm vi đề tài. Các trang là tài liệu tự học, không phải kết quả thí nghiệm mới.

## Phạm vi hiện hành

Đọc [quyết định đề tài](../01-idea/topic-decision.md) trước khi dùng nội dung kỹ thuật: từ tối 11/10/2026, mục tiêu chính là **footprint độ nhạy đột biến theo residue**. Nhánh dự đoán E3 đã bỏ vì audit chỉ có một E3 đạt ít nhất năm peptide; E3 còn là ca nghiên cứu. Trang [vì sao bỏ nhánh E3](foundations/e3-conditioning.html) giữ ý tưởng cũ để giải thích quyết định thiết kế.

## Kiểm tra

Từ gốc repo:

```bash
python3 docs/topics/degron-e3-specificity/learn/check_links.py
git diff --check
```

`check_links.py` kiểm file/anchor tương đối trong 22 trang và nhãn truy cập của ảnh, sơ đồ. Trang vẫn đọc được khi tắt JavaScript; font ngoài có thể thay bằng font hệ thống khi offline. Trong phiên hoàn thiện, đã xem ảnh chụp hub, trang kiến trúc, trang Zhang và hình gốc trong trang Voutsinos ở độ rộng 500 px; hub cũng được xem ở 780 px. Hình gốc được giữ kích thước đọc được và cuộn trong khung trên màn hình hẹp.

## Nguồn và giới hạn

- Audit PAP và tile: [ghi chú degron](../../../common/deep-research/research_notes/degron/README.md).
- Audit nhãn E3 và residue: [ghi chú và script](../../../common/deep-research/research_notes/degron-e3-labels/README.md).
- Nguồn hình tác giả và giấy phép: [NOTICE.md](assets/figures/NOTICE.md).
- Table S5 của Zhang 2023 chưa lấy được; số E3 tự đếm là giới hạn dưới. Giao của 27 peptide được gán E3 và 27 peptide có bản đồ bão hòa chỉ có **23 peptide**, theo hai JSON audit. Bốn bài lõi đã đọc toàn văn theo nhật ký repo; các trang còn lại ghi rõ khi mới có tóm tắt hoặc thông tin thư mục.
- MIL-Degron chưa cài đặt, huấn luyện hoặc đánh giá. Các sơ đồ kiến trúc là minh họa đề xuất.
