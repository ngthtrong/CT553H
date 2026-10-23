# Protocol của lần chạy 18/10/2026

Đây là thí nghiệm phát triển trên bộ nhãn đã từng được khảo sát; không gọi là test ngoài chưa từng xem. Không thay ngưỡng sau khi xem kết quả. Không điều chỉnh mô hình bằng nhãn outer fold. Đối chiếu các yêu cầu hiện hành ở D-031, D-028.

- Nhãn, lọc và cụm dùng nguyên `residue_data.py`: PSI WT nội tại ≤3, reads ≥10, trung bình ΔPSI hai nửa, ô dương ΔPSI≥1; loại ô đồng nghĩa.
- 5 outer fold GroupKFold theo cov80; inner GroupShuffleSplit 20% cụm của phần train. Không dùng scanning trong phiên này nên không có đường rò từ scanning.
- 3 seed 17/29/43; cùng outer fold, seed thay inner validation và khởi tạo mạng. Báo rõ đây không phải ba outer partition độc lập.
- Ridge M3: alpha 1/10/100/1000 chọn MSE inner; fit lại toàn outer train. Mạng: AdamW lr .002, weight decay .01, batch khoảng 1024, tối đa 60 epoch, patience 8; checkpoint chọn bằng MSE inner; không fit lại để tránh chọn số epoch từ outer.
- Kiến trúc ứng viên: pair WT/mut 40 chiều →32; composition+ordered ±3 context 140 chiều →32; sigmoid gate theo pair nhân context; head 64→32→1; cộng residual ΔPAP đóng băng. Ablation bỏ gate hoặc bỏ nhánh PAP; cùng lịch học. Đây là thiết kế thử nghiệm, chưa được xác lập tính mới.
- Macro AUROC mức ô theo peptide; ensemble điểm của 3 seed rồi mới tính AUROC; cũng giữ kết quả từng seed. Bootstrap 5.000 lần theo cụm, ghép cặp peptide; không coi ô là độc lập. CI là CI có điều kiện trên các dự đoán OOF, không bao hết phương sai tái huấn luyện.
- ΔPAP mutant−WT, đúng chiều pipeline cũ. Kiểm tái lập mốc 0,7693. Degformer epoch50 ghim commit, dự đoán PSI mutant−WT; kiểm chồng exact sequence với training_data.csv, không gọi điểm checkpoint là clean holdout khi có chồng.
- Không tự biến một ridge vượt mốc thành đạt điều kiện thành phần kiến trúc mới. Không suy ra tính mới từ một lượt tìm kiếm. Mọi phép so trong lần chạy là exploratory; không điều chỉnh đa kiểm định nên không dùng CI đơn lẻ như bằng chứng xác nhận kiến trúc cuối cùng.
