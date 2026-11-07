# Sơ đồ kết quả campaign — 06/11/2026

Hai sơ đồ bổ sung cho Chương 3, dựng từ [JSON audit](../../../../research/output-review-2026-11-06/results.json) và protocol v3. Đây là sơ đồ draw.io mới, độc lập với bộ FigJam lịch sử 22/10.

| Sơ đồ | Nguồn chỉnh sửa | PDF vector | Xem trước |
|---|---|---|---|
| Dòng kế thừa campaign và phần còn lại | [drawio](campaign-lineage.drawio) | [PDF](campaign-lineage.pdf) | [PNG](campaign-lineage.png) |
| Chia nhóm, chọn ở inner, OOF/ensemble và T giữ riêng | [drawio](nested-evaluation.drawio) | [PDF](nested-evaluation.pdf) | [PNG](nested-evaluation.png) |

Sinh XML bằng [build_campaign_assets.py](../../ch4/build_campaign_assets.py); export native bằng draw.io Desktop 32.6.10. PDF dùng `-x -f pdf --crop -e --border 10`; PNG dùng `-x -f png --scale 2 --border 10`. Thêm `-o <đích> <nguồn.drawio>` cho từng file. Không đổi đồng thời width và scale.

Đã chạy `validate.py --score`: mỗi sơ đồ 0 error, 0 warning, không overlap/crossing được phát hiện. Đã xem PNG trước export cuối và xem vị trí trong PDF luận văn. Màu xanh là luồng đánh giá, xanh lá kết quả đã hoàn tất, cam nhánh cần phân biệt, xám giới hạn/đầu vào riêng. Nội dung và nhãn tiếng Anh tương ứng luận văn.
