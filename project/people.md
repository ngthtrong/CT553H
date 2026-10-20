# Con người trong dự án

> Thông tin thô, dùng chung cho mọi đề tài. Quyết định không ghi ở đây, xem [DECISIONS.md](../DECISIONS.md).

## Sinh viên

| Trường   | Giá trị                                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Họ tên   | **Nguyễn Thanh Trọng**                                                                                                   |
| MSSV       | *B2305615*                                                                                                                    |
| Học phần | CT553H, luận văn tốt nghiệp ngành Kỹ thuật phần mềm, Đại học Cần Thơ. Làm một người. Xem[course.md](course.md) |
| GitHub     | `ngthtrong` (repo private từ 01/10/2026)                                                                                     |

## Giảng viên hướng dẫn (GVHD)

| Người                                                                    | Vai trò       | Ghi chú                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TS. Hồ Quang Thái** (Ho Quang Thai; QT Ho), Đại học Cần Thơ | **GVHD** | Tên được Trọng xác nhận lại ngày 05/10/2026. Chuyên môn: tin sinh học, protein (mCNN, PLM, RAG, protein màng/vận chuyển, sirtuin). Nhánh nghiên cứu:[advisor-research.md](advisor-research.md); danh mục 14 công trình: [ho-quang-thai.md](advisor-publications/ho-quang-thai.md); PDF: [resources/papers/ho-quang-thai/](../resources/papers/ho-quang-thai/) |

## Người liên quan

| Người                                     | Vai trò                                                               | Ghi chú                                                                                                                      |
| ------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Prof. Yu-Yen Ou (YY Ou), Yuan Ze University | Đồng tác giả thường xuyên của GVHD.**Không phải GVHD** | Danh mục:[yu-yen-ou.md](advisor-publications/yu-yen-ou.md); PDF: [resources/papers/yu-yen-ou/](../resources/papers/yu-yen-ou/) |
| Hồ Quốc Bảo (B2203539)                   | Tác giả luận văn tham khảo, cùng GVHD                            | *Hybrid Cascade Framework… PLM + multi-scale CNN* — [phân tích](../resources/reference-theses/thesis-comparison.md)      |
| Nguyễn Duy Khánh (B2205944)               | Tác giả luận văn tham khảo, cùng GVHD                            | [phân tích](../resources/reference-theses/thesis-comparison.md)                                                              |

## Những điều GVHD đã nói (nguyên liệu thô)

Ghi ngắn, dẫn tới biên bản gốc. Hệ quả cho việc chọn đề tài nằm ở [DECISIONS.md](../DECISIONS.md).

- **02/10/2026, buổi gặp 1:** RTK–ATP không bị từ chối nhưng nên đổi; aging/cancer hợp hơn. Cần trình bày rõ bài toán và lý do; history research làm theo 3 bước; áp năm tiêu chí; tiêu chí 5 (ứng dụng/website) không thể thiếu; tuần 6 báo cáo lại. Xem [minutes.md](meetings/2026-10-02-session-01/minutes.md).
- **07/10/2026 (Trọng truyền đạt):** đầu vào có thể là ma trận biểu hiện gene, không bắt buộc là chuỗi amino acid.
- **10/10/2026 (Trọng đánh giá):** GVHD không chấp nhận kết quả âm làm đóng góp chính. Đây là rủi ro cho mọi đề tài dạng audit.
- **11/10/2026 (Trọng truyền đạt, ghi trong [nhật ký degron](../topics/degron-footprint/log.md)):** GVHD kỳ vọng **một kiến trúc chưa ai dùng**, không chấp nhận đóng góp chỉ là một bảng đối chứng có kỷ luật. Đây là rủi ro lớn cho các đề tài dạng audit/benchmark (A2, A3, A4).
- **12/10/2026 (Trọng truyền đạt):** **GVHD vẫn chấp nhận đóng góp dạng công cụ** (công cụ, thước đo, audit, benchmark, thuật toán tối ưu). Chưa rõ GVHD nói vào lúc nào và bằng hình thức gì; **chưa có biên bản**.
  - Hai lời 11/10 và 12/10 **được giữ nguyên cả hai**, không xoá lời nào. Cách đọc đang dùng: lời 11/10 là **mong muốn**, không phải điều kiện loại — ghi ở [D-022](../DECISIONS.md#d-022). Đây là cách đọc của Claude, **chưa được GVHD xác nhận trực tiếp**; câu hỏi xác nhận ở C-5 của [DECISIONS.md](../DECISIONS.md).
  - Điều này **không** nới cổng G2: GVHD nhận dạng công cụ không có nghĩa là nhận kết quả âm ([D-012](../DECISIONS.md#d-012), lời ngày 10/10 vẫn giữ).
- **15/10/2026 (Trọng trao đổi trực tiếp với GVHD, Trọng truyền đạt):** **GVHD xác nhận trụ phần mềm được tính là đóng góp** — cụ thể là **dịch vụ dự đoán có bất định** và **harness đánh giá**. Trọng cho biết đã trao đổi trực tiếp và được xác nhận. Hệ quả ghi ở [D-034](../DECISIONS.md#d-034).
  - ⚠ **Vẫn chưa có biên bản**, và chưa rõ GVHD có nói kèm điều kiện nào không. Buổi gặp **16/10/2026** là chỗ xin duyệt **khung đề tài**, nên đây là chỗ để lấy xác nhận có biên bản — xem [C-5](../DECISIONS.md#c-5).
  - Lời này **không** thay lời 11/10 ("kỳ vọng một kiến trúc chưa ai dùng"): cả hai được giữ. Cách đọc đang dùng: trụ phần mềm là **một** đóng góp được tính, **không** phải thứ thay cho yêu cầu kiến trúc mới của [D-027](../DECISIONS.md#d-027). Nó cũng **không** nới cổng G2.
