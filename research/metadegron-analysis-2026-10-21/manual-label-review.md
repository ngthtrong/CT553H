# Kiểm truy nguồn mẫu dương tính

[ĐO] Đã chọn ngẫu nhiên 40 dòng bằng seed17 trước tính điểm, giữ chỉ số mẫu ở [label-sample.json](label-sample.json). Đã đọc từng dòng: protein/tọa độ/chuỗi từ S2, PMID nguồn, và Methods/References của record ELM hiện hành cùng class/giao tọa độ. Bản ghi từng dòng và nhận xét nằm ở đường dẫn `details_path` trong [manual-label-review.json](manual-label-review.json), dưới raw bị gitignore để không phân phối dữ liệu nguồn.

[ĐO] Có **22/40** truy được ELM true-positive; **18/40** chưa chốt lineage, **45,0%**, Wilson 95% **[30,7%;60,2%]**; **11/40** không phải HUMAN theo hậu tố, **27,5% [16,1%;42,8%]**. **4/40** có metadata assay ubiquitination. [manual-label-review.json](manual-label-review.json), [review-labels.py](review-labels.py).

[DIỄN GIẢI] “True-positive” của ELM là bằng chứng cho motif/tương tác mà ELM curate, không tự xác nhận protein nguồn bị phân hủy qua motif trong mọi hệ đo. Motif APC/C TPR có thể thuộc co-activator; BUB1B liên quan phức hợp checkpoint, nên đặc biệt cần thí nghiệm đo degradation, không chỉ cấu trúc/binding.

[CHƯA XÁC MINH] Chưa đọc đủ thí nghiệm gốc của mọi dòng; review 2017 có bảng gốc bị hạn chế ELTEnet, và nguồn S2 phần lớn trỏ bài tổng hợp. Không tìm được record ELM hiện hành không có nghĩa nhãn sai ở snapshot cũ. Do đó **tỉ lệ nhãn degron sinh học sai/mơ hồ chưa định lượng được**, để `null`; không trình bày 18/40 là false-positive rate. Các khoảng Wilson mô tả mẫu metadata, không chữa được thiếu thẩm định sinh học và không điều chỉnh phụ thuộc giữa motif.

[ĐỀ XUẤT] Vòng adjudication tiếp theo cần hai người đọc độc lập PMID thí nghiệm gốc, chốt loại assay (half-life/reporter, mutation rescue, E3 perturbation, binding-only), PTM, loài và isoform. Mỗi nhãn không đủ chứng cứ để ngoài training; không đổi thành âm. Dừng nhập nhãn nếu không có giấy phép và lineage đủ rõ.
