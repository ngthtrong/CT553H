# Tiền đăng ký — mở rộng G2, 18/10/2026

Viết **trước khi chạy** bất kỳ phép đo nào của phiên này. Không sửa tiêu chí sau khi xem kết quả; nếu phải sửa thì ghi thêm mục "sửa sau khi xem" kèm ngày và lý do, không ghi đè.

Căn cứ: ba việc còn mở ở [báo cáo 18/10 §5](../g2-saturation-2026-10-18/README.md), điều kiện G2 ở D-031, ràng buộc nguồn ngoài ở D-028 mục 8.

## Dùng chung cho cả ba thí nghiệm

Nhãn, lọc, chiều ΔPSI, 5 outer fold GroupKFold theo cụm cov80, inner GroupShuffleSplit 20% cụm: **giữ nguyên** `g2-saturation-2026-10-18/run.py`. Cache đầu vào dùng lại `data/processed/g2-saturation-input.npz` (SHA-256 đã ghi ở `results.json` cũ). Thước đo: AUROC mức ô, macro theo peptide; bootstrap 5.000 lần **theo cụm**, ghép cặp theo peptide. Không coi ô là độc lập. Không chọn seed sau khi xem.

## E1 — Degformer trên tập con **không chồng** huấn luyện

**Câu hỏi.** Bỏ 88,12% ô có đúng sequence trong `training_data.csv` của Degformer thì điểm còn lại là bao nhiêu, và các mô hình của đề tài trên **đúng tập con đó** là bao nhiêu?

**Cách làm.** Mask ô = sequence đột biến **không** xuất hiện trong `training_data.csv`. Tính lại macro AUROC của cả 6 bộ điểm đã lưu trên riêng tập con, chỉ giữ peptide còn đủ hai lớp trong tập con. Phép so ghép cặp Degformer − ridge và Degformer − ΔPAP trên tập con.

**Tuyên bố được phép rút ra.** Đây **vẫn không phải clean holdout**: WT của 91/91 peptide có trong train của Degformer, và chưa khử đồng dạng (homolog), chỉ khử trùng khít. Vì vậy E1 chỉ dùng để **thu hẹp** con số 0,9248, không dùng để kết luận Degformer tổng quát hóa tốt. Nếu điểm tập con vẫn cao thì kết luận hợp lệ duy nhất là "chồng khít không giải thích hết khoảng cách", không phải "Degformer sạch".

## E2 — Ba ứng viên tương tác thay thế × ngữ cảnh

**Câu hỏi.** Có thành phần kiến trúc nào mô hình hóa tương tác giữa **thay thế** và **ngữ cảnh cục bộ** mà **ổn định** vượt ridge M3 không? Cổng sigmoid của phiên trước đã **không** đạt (đảo dấu ở seed 29).

**Ba ứng viên, chốt trước, không thêm không bớt.** Cùng đầu vào 180 chiều M3, cùng lịch học (AdamW lr .002, wd .01, batch ~1024, tối đa 60 epoch, patience 8, chọn checkpoint bằng MSE inner), cùng 3 seed 17/29/43, không nhánh ΔPAP để đọc riêng đóng góp của tương tác:

1. `bilinear` — tương tác song tuyến hạng thấp: chiếu pair→32, context→32, lấy tích Hadamard của hai phép chiếu hạng 8 rồi nối vào head. Khác cổng sigmoid ở chỗ tương tác **có dấu**, không bị bóp về (0,1).
2. `film` — pair sinh **cả scale và shift** cho biểu diễn context (FiLM), thay vì chỉ một cổng nhân.
3. `cross_ridge` — **không phải mạng**: ridge trên M3 cộng tích chéo tường minh giữa one-hot acid amin thay vào (20) và ngữ cảnh có thứ tự ±3 (120) = 2.400 chiều chéo. Đây là mô hình tương tác **tuyến tính đơn giản nhất có thể**; nếu nó thắng thì mạng không được nhận công của tương tác.

**Tiêu chí thành công, chốt trước.** Một ứng viên chỉ được gọi là "thành phần kiến trúc có lợi ổn định" khi đạt **cả ba**: (a) delta ghép cặp so với ridge M3 **dương ở cả ba seed**; (b) CI 95% bootstrap theo cụm của delta ensemble **không chứa 0**; (c) delta so với ΔPAP frozen cũng dương với CI không chứa 0. Không đạt đủ ba thì ghi **không đạt**, kể cả khi điểm tuyệt đối cao hơn.

**Báo cáo.** Báo **cả ba** ứng viên bất kể kết quả. Đây là 3 phép so chính, không điều chỉnh đa kiểm định, nên kết quả dương vẫn là **phát triển**, không phải xác nhận cuối cùng. Không coi "viết code mới" là tính mới; tính mới phải tra tiền lệ riêng.

## E3 — Kiến trúc Degformer dưới cùng ngân sách nhãn và cùng phép chia

**Câu hỏi.** Khi transformer của Degformer được huấn luyện **từ đầu** trên đúng nhãn bão hòa của đề tài, với đúng phép chia cov80, nó hơn hay kém ridge M3?

**Cách làm.** Dựng lại **đúng** class `PeptideTransformer` đã đọc từ AST (d_model 128, 4 lớp, 8 head, ff 256, dropout .1) và **đúng** siêu tham số công bố (Adam lr 1e-4, batch 512). Trung thành với công thức của tác giả: hồi quy **PSI tuyệt đối** của sequence (ô đột biến `psi_wt + ΔPSI`, cộng hàng WT `psi_wt`), chuẩn hóa z theo outer-train; điểm ô = `pred(mut) − pred(WT)`. 5 outer fold, inner validation chọn epoch.

**Giới hạn chấp nhận trước.** (i) **1 seed (17)**, vì CPU; không suy ra độ ổn định theo seed từ E3. (ii) **Trần 30 epoch, patience 6** — ghi lại đường validation để người đọc thấy đã phẳng hay chưa; nếu chưa phẳng thì E3 là **chặn dưới** của kiến trúc đó, phải nói rõ. (iii) E3 **không** tái lập tiền huấn luyện 569.270 dòng của tác giả: ước lượng trên máy này khoảng 17 phút/epoch × 50 epoch × 5 fold ≈ **70 giờ**, ngoài tầm phiên. Vì vậy E3 trả lời "kiến trúc nào hơn ở cùng ngân sách nhãn", **không** trả lời "Degformer sạch mạnh thế nào".

**Tuyên bố được phép rút ra.** Nếu ridge thắng E3, phát biểu hợp lệ là "ở ngân sách nhãn này, transformer không hơn ridge", **không** phải "Degformer kém". Nếu transformer thắng, phải đọc kèm giới hạn 1 seed và trần epoch.

## Điều không được làm trong phiên này

Không nới điều kiện G2. Không tự ghi G2 hoàn tất. Không tự ghi tính mới kiến trúc. Không ghi quyết định mới vào B1/B2 — kết quả đi vào báo cáo, A và D ([CLAUDE.md](../../../../CLAUDE.md) quy tắc ghi quyết định).
