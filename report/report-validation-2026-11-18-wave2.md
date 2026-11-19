# Plan-report: hoàn tất 4.5 và đợt 2 — 18/11/2026

Tiếp theo [report-validation-2026-11-18-ch3.md](report-validation-2026-11-18-ch3.md). Phạm vi: mục **4.5**
và đợt 2 (**7.1–7.4, 7.6, 7.7, 8.1**) của [plan-report.md](../plan-report.md). D-2 (7.5) vẫn để trống chờ
thông tin. Không đổi số liệu, hình, kết quả hay giới hạn bằng chứng; không chạy huấn luyện/suy luận;
không commit/push.

## 1. Đã làm

| Mục | Thay đổi | Trạng thái |
| --- | --- | --- |
| 4.5 | Mỗi thí nghiệm ở Part A (3 mục `campaign-methods`, LoRA-D, refit, ưu tiên hoá) mở bằng **Purpose**, thân là **Flow**, đóng bằng **Reported in … / Limits** (cùng kiểu với các mục tính năng ở Part B) | xong |
| 7.1 | Chương 4 có *Part A: Experimental Results* / *Part B: Software Testing*. Đầu §Results có **đoạn dẫn đọc theo RQ1–RQ5**, mỗi RQ một câu trả lời ngắn có số (macro) và trỏ mục, dẫn tới Hình 3.2 và bảng đánh giá RQ. **Giữ thứ tự thời gian** của các mục kết quả vì thiết kế sau phụ thuộc kết quả trước; nêu lý do trong đoạn dẫn | một phần, có chủ đích |
| 7.2 | Chuyển 6 bảng phụ sang Phụ lục B, số liệu giữ nguyên: `tab:priority-recall-budget`, `tab:priority-strata` (→ B *Retrospective Prioritisation Sensitivity*), `tab:newgroup`, `tab:partcrobust`, `tab:progress-effect-errors`, `tab:progress-largest-errors` (→ B *Additional Tables and Figures*). Chương 4 còn **29 bảng** (mục tiêu ≤ 30). Thêm `\FloatBarrier` trước B.7 và B.9 để bảng không trôi sang mục khác | xong |
| 7.3 | Đoạn *Testing Objectives* bỏ câu đã sai "no passing result for those additions is claimed"; Mở đầu mô tả Part A/B. Chữ "progress report" **giữ** cho đến khi chốt bản nộp chính thức | một phần (phụ thuộc bản nộp) |
| 7.4 | Kết luận: dẫn bảng giới hạn L1–L10 ở đầu §Limitations; thay đoạn ưu tiên phần mềm đã cũ bằng các bước tiếp theo của plan-system và các hướng ngoài phạm vi F-1…F-7 (ghi là ngoài phạm vi, không phải tính năng) | xong |
| 7.6 | Abstract/Tóm tắt đối chiếu lại: không mâu thuẫn với thay đổi đợt 2, vẫn mỗi bản một trang; **chưa** viết lại bản cuối (chờ bản nộp và D-2) | một phần |
| 7.7 | Danh mục viết tắt thêm 11 mục (UPS, Ub, FACS, Tile/window, ESM-2, CNN/mCNN, W/T, Arm B/D, Brier, Platt, R3 gate). Thêm `platt1999` vào `references.bib`; chú thích Hình 2.10 trích nguồn này thay cho chú thích tạm | xong |
| 8.1 | Rà có mục tiêu: bỏ câu kiểu nhật ký ở Phụ lục A ("this thesis-update review"); thống nhất tile/window qua danh mục. **Chưa** rà ngôn ngữ toàn văn | một phần |

## 2. Kiểm `[ĐO 18/11/2026]`

| Kiểm | Kết quả |
| --- | --- |
| `make -C report all` | PASS |
| `make -C report check` | PASS — 167 trang một mặt, 167 hai mặt, smoke 9 |
| `check_float_references.py` | PASS — 41 hình, 64 bảng (tổng số không đổi; 6 bảng chỉ đổi chỗ), khớp cả hai bản |
| Abstract / Tóm tắt | mỗi bản một trang |
| Mục lục | Part A/B ở cả Chương 3 và Chương 4 |
| Khoảng trống > 1/3 (50 dpi, hai bản) | 14/167 trang, giống hệt; đều là trang kết thúc có chức năng: 5–6, 10, 17, 19, 22, 24 (cuối danh mục viết tắt), 31 (cuối Phần 1), 55 (cuối Ch.2), 86 (cuối Ch.3), 137 (cuối Ch.4), 141 (cuối Kết luận), 144 (cuối tài liệu tham khảo), 167 |
| Ảnh render | trang đoạn dẫn RQ; các trang Phụ lục B nhận bảng chuyển sang |

| PDF | SHA-256 |
| --- | --- |
| `report/build/content/content.pdf` | `05bd4058340126c065617970e3ecfb669319e788562390d51f096c5d2ee22161` |
| `report/build/content-twoside/content.pdf` | `1987f7c0a76078c74b2945a9a95deea2f46097887f450c108ceb46b78ee07010` |

## 3. Còn mở

- 7.3, 7.6: chờ quyết định bản nộp chính thức (bỏ "progress report", viết lại Abstract cuối) và D-2.
- 8.1: rà ngôn ngữ toàn văn.
- Đợt 3 (6.1–6.7) chờ cổng G-SYS của plan-system; 7.5 chờ D-2; 8.2–8.3 ở bước bàn giao.
