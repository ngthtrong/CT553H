# Kiểm chứng 18/10/2026

- **PASS — chạy thật hai lần:** huấn luyện ridge và 45 mạng CPU, chạy checkpoint Degformer, tạo results và dự đoán. Lần thứ hai dùng runner cuối cùng có lưu checkpoint; toàn bộ headline AUROC trùng lần đầu. Không dùng kết quả cũ thay cho chạy thật. Hash runner và phiên bản Python/NumPy/PyTorch nằm trong [results.json](results.json).
- **PASS — audit độc lập:** [audit.json](audit.json) xác nhận 91 peptide, 89 cụm, 47.847 ô, score hữu hạn, ΔPAP tái lập 0,7692837467; tính lại macro và CI ghép cặp cụm, giữ kết quả từng seed.
- **PASS — reload 45 checkpoint:** mọi train/validation/test rời cụm cov80, phủ đủ các ô; load lại state_dict và tính lại điểm test khớp dự đoán lưu (`rtol=atol=1e-6`).
- **PASS — nguồn/ignore:** downloader kiểm SHA-256 từng file Degformer theo commit ghim. `git status --untracked-files=all` trong nguồn Degformer chỉ liệt kê SOURCE.md; checkpoint, training CSV, cache NPZ và mọi checkpoint mô hình đều bị ignore.
- **PASS — liên kết mới:** kiểm mọi link tương đối của các Markdown mới và link thay đổi trong A/D, README/log đề tài, data README, journal và resources: không thêm link hỏng. Đối chiếu target đã tồn tại trong HEAD khi phát hiện link cũ hỏng.
- **PASS — diff phạm vi G2:** `git diff --check` trên các file G2 và tài liệu cập nhật đạt.
- **Chưa đạt ở toàn repo:** `python3 tools/check_links.py` báo **55 lượt link hỏng**, gồm `lectures/14-xai-basics.html → 15-reading-bioinfo-papers.html` và các đường dẫn deck/presentation cũ. Không sửa ngoài phạm vi G2. `git diff --check` toàn repo còn whitespace ở deck HTML đang có thay đổi độc lập; không sửa slide trong phiên này.
- **Giới hạn khoa học:** chưa retrain Degformer theo cov80 sạch; chưa xác lập novelty; hiệu ứng gate đảo dấu ở một seed. Bootstrap có điều kiện trên OOF và các phép so exploratory không phải xác nhận cuối cùng. Các hạn chế này là lý do giữ G2 mở, dù mốc số đã vượt.
