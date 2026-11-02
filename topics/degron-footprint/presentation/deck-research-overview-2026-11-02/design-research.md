# Khảo sát thiết kế trước khi dựng deck

Ngày khảo sát: 02/11/2026. Ngữ cảnh: giới thiệu đề tài và trao đổi tiến độ với giảng viên. Skill áp dụng: [slides](../../../../.agents/skills/slides/SKILL.md).

| Nguồn khảo sát | Điều đã xem | Quyết định sử dụng |
|---|---|---|
| [Assertion–Evidence, Penn State](https://writing.engr.psu.edu/assertion_evidence_EA.html), [checklist](https://www.writing.engr.psu.edu/AE_checklist.pdf) | Thông điệp ngắn, bằng chứng hình ảnh, nội dung phụ ở notes | Áp dụng cho các slide phân tích; phần giới thiệu dùng hình giải thích và tên chủ đề tự nhiên. Không ép mọi tiêu đề thành câu hỏi. |
| [Harvard Catalyst: scientific slides](https://catalyst.harvard.edu/writing-communication-center/visualize-science/slides/) | Trình bày khoa học hướng tới người nghe, ví dụ và template Assertion–Evidence | Hình trung tâm, ít chữ, ghi chú người nói tách khỏi màn chiếu. |
| [Slidev Academic](https://github.com/alexanderdavide/slidev-theme-academic) | Theme dành cho báo cáo học thuật, phân cấp nội dung và bố cục | Tham khảo cấu trúc học thuật; không dùng nguyên theme hoặc mặc định Slidev. |
| [EMBL design](https://www.embl.org/guidelines/design/), [màu](https://www.embl.org/guidelines/design/design-guidelines/colours/) | Bảng xanh khoa học sự sống, khoảng trắng, thứ bậc thị giác | Lấy cảm hứng xanh rừng và bố cục thoáng. Không dùng logo, roundel hay nhận diện để ngụ ý liên kết EMBL. |

Kho tìm kiếm CSV của skill cục bộ thiếu `slide-layouts.csv` và `styles.csv`; khảo sát trực tiếp các nguồn trên được dùng thay thế. Template HTML của skill chỉ được tham khảo về điều hướng và responsive, không dùng palette hoặc layout mặc định.

## Art direction được chọn

Scientific editorial: nền giấy rất sáng, mảng xanh rừng sâu cho tiêu đề mở đầu, chữ sans tiếng Việt, đường biểu đồ mảnh và số liệu rõ. Bảng màu: ink `#193A2B`, forest `#0A5032`, green `#18974C`, coral `#C76242`, blue `#477CA7`, paper `#F6F7F2`. Coral dùng cho phép thay/đánh đổi, xanh cho tín hiệu hỗ trợ; luôn có chữ/ký hiệu đi cùng màu.

Không lặp bố cục thẻ thông tin trên mọi slide. Các dạng chính: hình lớn + chú thích trực tiếp, sơ đồ toàn chiều ngang, hai mô hình song song, heatmap, biểu đồ với CI, ảnh giao diện và timeline phụ thuộc công việc. Không dùng footnote trên màn chiếu. Nguồn, điều kiện chi tiết và lời giải thích lưu trong notes và `evidence.json`.

## Chuyển động

Vòng chuyển động có ý nghĩa: nhận diện và phân hủy protein; dòng tế bào vào bin; phép thay điền một ô ma trận; dữ liệu qua QC; nhóm protein đi vào fold; cửa sổ CNN quét qua representation; chuyển nguồn rồi fine-tune; chọn ứng viên thí nghiệm. Chuyển động tạm dừng khi slide ẩn; có nút dừng chung và `prefers-reduced-motion`. GIF đi kèm poster cho chế độ tĩnh/in.

## Hình ảnh và tính đúng

GIF Fam188a chỉ minh họa protein gấp cuộn, không phải cấu trúc degron/HIF1A. Nhãn HIF1A và mọi biểu đồ kết quả lấy từ JSON nghiên cứu được băm. Sơ đồ nguyên lý được ghi rõ là minh họa. Màn hình sản phẩm nếu lấy từ prototype thiết kế được ghi đúng trạng thái, không coi số mẫu trong giao diện là dự đoán thật. Ma trận thay thế giữ mask WT và ô thiếu.
