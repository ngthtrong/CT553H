# Audit lợi ích của cấu trúc AlphaFold + trình tự PLM cho protein màng/vận chuyển, có kiểm soát rò rỉ — ứng viên A3

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026**.

| | |
|---|---|
| Lĩnh vực | Tin sinh học, protein màng/vận chuyển (nhánh dày nhất của GVHD), tầng benchmark |
| Dữ liệu | Nhãn của GVHD hoặc nhãn công khai (ATP-binding, efflux, kênh ion) + cấu trúc AlphaFoldDB + metadata ngày công bố cấu trúc. Chưa tải |
| Giai đoạn | Mới khảo sát qua tóm tắt tìm kiếm; **đã phải thu hẹp** |

## Bài toán (đã định vị lại)
Ý tưởng ban đầu là thêm cấu trúc AlphaFold vào mô hình trình tự. **Ý tưởng này đã có người làm:** Denger & Helms (*Molecules* 2025) dùng Foldseek 3Di + ProstT5 để dự đoán cơ chất protein vận chuyển. Câu hỏi còn lại: **phần cải thiện mà các nghiên cứu báo cáo có còn đứng được không** sau khi kiểm soát (1) rò rỉ do test trùng dữ liệu huấn luyện AlphaFold hoặc tương đồng cấu trúc 3D, và (2) việc cấu trúc tĩnh có thể không phản ánh trạng thái chức năng (cảnh báo Palazzolo 2026)?

- **Đầu vào:** trình tự → embedding PLM; cấu trúc AlphaFold → 3Di, ProstT5, đặc trưng pocket; metadata để chia tập theo thời gian và theo tương đồng cấu trúc.
- **Đầu ra:** hiệu năng dưới hai giao thức chia tập (lạc quan và kiểm soát rò rỉ) cùng độ chênh giữa hai giao thức; cờ "mơ hồ về conformation" cho từng ví dụ.

## Cổng G1/G2/G3
| Cổng | Trạng thái | Ghi chú |
|---|---|---|
| G1 nhãn độc lập | Khả quan — nhãn thực nghiệm/chú giải | Chưa audit |
| G2 đóng góp dương | **Rủi ro trung bình–cao.** Có thể cấu trúc không giúp gì sau khi kiểm soát rò rỉ, tức kết quả "âm" | GVHD không nhận kết quả âm làm đóng góp chính |
| G3 ứng dụng | Có thể làm, nhưng không tự nhiên bằng A4 | — |

## Rủi ro chính
- **Không được nói "đầu tiên kết hợp cấu trúc + trình tự cho protein vận chuyển".**
- Dạng audit có thể không đáp ứng kỳ vọng "kiến trúc mới" của GVHD ([C-3](../../DECISIONS.md)).

## Việc tiếp theo
1. Đọc toàn văn Denger & Helms 2025 và tóm tắt hội thảo Palazzolo 2026.
2. Kiểm tra xem bài 2025 đã chia tập theo tương đồng cấu trúc/mốc thời gian chưa. Nếu đã làm đủ thì A3 gần như hết chỗ.

## Trong thư mục này
- [log.md](log.md) · [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md)
- Nguồn danh mục: [surveys/bioinformatics-tool-layer-candidates-2026-10-12.md](../../surveys/bioinformatics-tool-layer-candidates-2026-10-12.md) (mục A3)
