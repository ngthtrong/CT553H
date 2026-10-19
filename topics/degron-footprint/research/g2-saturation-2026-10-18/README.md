# G2 — học trực tiếp trên ma trận bão hòa, 18/10/2026

**[ĐO] Đã vượt mốc số 0,7693, nhưng chưa đủ căn cứ ghi hoàn tất toàn bộ G2.** Ridge M3 OOF đạt **0,8082**; ứng viên mạng có gate đạt **0,8002**, song thua ridge và hiệu ứng gate đảo dấu ở một seed. Tính mới kiến trúc chưa được xác lập. Trạng thái và điều kiện chính thức: [DECISIONS.md](../../../../DECISIONS.md#hien-hanh). Đây là báo cáo thực nghiệm, không thay đổi điều kiện nghiệm thu.

## 1. Đã thực hiện và tái lập

- Học **trực tiếp** trên bộ bão hòa: **91 peptide / 89 cụm cov80 / 47.847 ô**. Nguồn nhãn, lọc và chiều ΔPSI giữ nguyên pipeline cũ. Không dùng scanning nên không có chồng cụm qua nhánh scanning.
- 5 outer fold theo cov80; inner validation theo cụm để chọn alpha ridge/epoch mạng; 3 seed **17, 29, 43**. Cùng outer partition ở ba seed; không gọi là ba phép chia độc lập.
- Huấn luyện ridge, mạng điều kiện theo cặp thay thế và hai ablation: bỏ gate; bỏ residual ΔPAP. Tổng **45 lượt huấn luyện mạng**, ngoài 15 lượt ridge và chọn alpha inner.
- Tái lập ΔPAP `cnn2w1` **0,7692837467**, đúng mốc cũ. Chạy checkpoint chính thức Degformer epoch50 và kiểm exact-sequence overlap.
- Ghép cặp AUROC theo peptide; bootstrap **5.000 lần theo cụm**, giữ mọi peptide của cụm được lấy mẫu. Không lấy ô làm đơn vị độc lập.

Chi tiết: [protocol](PROTOCOL.md), [runner](run.py), [kết quả](results.json), [kiểm độc lập](audit.py), [kết quả kiểm](audit.json), [biên bản validation](VALIDATION.md). Điểm trong bảng là **ensemble điểm của ba seed trước khi tính AUROC**, không phải trung bình AUROC ba mô hình đơn.

## 2. Kết quả chính [ĐO]

| Mô hình | AUROC mức ô macro theo peptide | Điều kiện |
|---|---:|---|
| ΔPAP `cnn2w1` | 0,7693 | Frozen, tái lập mốc |
| Ridge M3 | **0,8082** | Học bão hòa; OOF theo cụm |
| Gate + residual ΔPAP | 0,8002 | Học bão hòa; OOF theo cụm |
| Bỏ gate, giữ ΔPAP | 0,7937 | Ablation |
| Giữ gate, bỏ ΔPAP | 0,8015 | Ablation |
| Degformer epoch50 | 0,9248 | **Có chồng dữ liệu huấn luyện lớn**, không phải clean holdout |

| Phép so ghép cặp | Delta | CI 95% theo cụm |
|---|---:|---|
| Ridge − ΔPAP | **+0,0389** | **[+0,0216; +0,0571]** |
| Gate+PAP − ΔPAP | +0,0309 | [+0,0125; +0,0501] |
| Gate+PAP − ridge | **−0,0080** | [−0,0152; −0,0006] |
| Gate+PAP − bỏ gate | +0,0065 | [+0,0027; +0,0102] |
| Gate+PAP − bỏ PAP | −0,0013 | [−0,0048; +0,0023] |

**Giới hạn phép so với 0,7273 cũ:** con số cũ học chỉ từ scanning rồi chuyển sang saturation; con số mới có nhãn saturation của outer-train. Không lấy chênh mới−cũ làm đóng góp kiến trúc: nó thay chế độ giám sát. ΔPAP frozen là cùng một đối chứng trên cùng ô nên phép so mới với ΔPAP có ý nghĩa, nhưng không cân bằng ngân sách nhãn.

## 3. Kiến trúc và độ ổn định [ĐO / DIỄN GIẢI]

Đầu vào 180 đặc trưng M3: WT/mut one-hot 40; thành phần peptide 20; ngữ cảnh có thứ tự ±3 dài 120. Pair và context được chiếu riêng về 32 chiều; sigmoid của pair nhân biểu diễn context; MLP 64→32→1; tùy ablation cộng ΔPAP đóng băng. Không đưa PSI WT thực nghiệm vào input. Checkpoint và dự đoán từng seed nằm trong `data/processed/`, được sinh lại bằng runner.

| Seed | Ridge | Gate+PAP | Bỏ gate | Gate+PAP − bỏ gate |
|---|---:|---:|---:|---:|
| 17 | 0,8062 | 0,7895 | 0,7806 | +0,0089 |
| 29 | 0,8068 | 0,7762 | 0,7838 | **−0,0076** |
| 43 | 0,8081 | 0,7881 | 0,7816 | +0,0064 |

**Không che sự đảo dấu bằng ensemble.** Tại seed 29, CI delta gate **[−0,0152; −0,0005]**, trong khi hai seed kia dương. CI gate−ΔPAP cũng chứa 0 ở seed 17 và 29. Bằng chứng cho ridge vượt mốc mạnh hơn bằng chứng cho thành phần gate. Residual PAP chưa có lợi rõ ràng; ablation bỏ nó còn tăng nhẹ.

Không coi gate là kiến trúc mới đã được chứng minh. [Deep temporal convolutional network](https://academic.oup.com/bioinformatics/article/36/7/2047/5634146) đã dùng attention/residual cho mutation effects; [một preprint về drug resistance](https://www.preprints.org/manuscript/202604.0069) mô tả mutation-conditioned gated injection. Các tiền lệ này đủ bác cách nói “gate theo đột biến tự nó là mới”, **chưa** đủ để xác định toàn bộ đóng góp đặc thù nhiệm vụ này. Lượt tra này là khảo sát sơ bộ, không phải tổng quan hệ thống. Không đưa thiết kế thử thành quyết định mới.

## 4. Degformer [ĐO]

Nguồn [repo tác giả](https://github.com/Alpine2048/Degformer), commit `49ee524599671f2b5e30d9cd052ce6baa55c06d8`, Apache-2.0; [manifest ghim](source-manifest.json), [sổ nguồn/giấy phép](../../data/raw/degformer-isolated/SOURCE.md). Chỉ lấy class kiến trúc đã đọc từ AST; không chạy top-level predict/train của nguồn; nạp checkpoint trong thư mục nguồn riêng bằng `python -I`, đúng ràng buộc D-028.8. Thư mục riêng và `-I` không phải sandbox bảo mật.

**42.163/47.847 ô đột biến (88,12%)** có đúng sequence trong `training_data.csv`; WT của **91/91 peptide** cũng có. Vì vậy **0,9248 không chứng minh tổng quát hóa sang peptide chưa thấy**, và không dùng nó để kết luận kiến trúc đề tài kém Degformer đúng 0,1246 trên clean test. Chưa đo overlap đồng dạng; exact overlap đã đủ bác giả định clean holdout. Chưa huấn luyện lại Degformer loại các cụm outer test. Con số Pearson tác giả tự báo 0,9162/0,9420 vẫn là Pearson; không so trực tiếp với AUROC ở đây.

Khi nạp StandardScaler, scikit-learn cảnh báo checkpoint tạo bằng 1.8.0 còn môi trường là 1.9.1. Inference hoàn tất, dự đoán hữu hạn; AUROC không phụ thuộc phép đổi thang affine dương của scaler. Hạn chế phiên bản được giữ trong [run.log](run.log), không coi đây là tái lập headline của tác giả.

## 5. Đánh giá mức hoàn thành

| Điều kiện / đầu việc | Bằng chứng phiên này |
|---|---|
| Học trực tiếp trên bão hòa | Đã thực hiện |
| Vượt mốc ΔPAP 0,7693 | **Đạt về phép đo phát triển**: ridge +0,0389, CI dương |
| Đối chứng Degformer chính thức | Đã chạy checkpoint và audit overlap; **chưa có bản retrain cov80 sạch** |
| Thành phần kiến trúc có lợi ổn định | **Chưa thiết lập**: gate thua ridge, một seed đảo dấu |
| Tính mới kiến trúc | **Chưa xác lập**, không tự nhận từ việc viết code mới |
| Bằng chứng xác nhận cuối cùng | **Chưa có**: đây là benchmark phát triển OOF trên dữ liệu từng được khảo sát |

**Việc nghiên cứu còn mở:** có thiết kế học tương tác thay thế–ngữ cảnh có lợi vượt baseline đơn giản và ổn định; đối chiếu tiền lệ để xác lập đóng góp cụ thể; huấn luyện lại Degformer theo cov80 nếu muốn tuyên bố so sánh tổng quát hóa sạch. Không tăng số lần thử chỉ để chọn một seed/CI thuận lợi. Không nới cổng hay tự ghi đề tài đã được GVHD duyệt.

## 6. Dựng lại và kiểm

Từ thư mục gốc, dùng CPU, khoảng vài phút trong môi trường phiên này:

```bash
.venv/bin/python -I topics/degron-footprint/research/g2-saturation-2026-10-18/download.py
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/g2-saturation-2026-10-18/run.py
.venv/bin/python -I topics/degron-footprint/research/g2-saturation-2026-10-18/audit.py
```

Runner tự tạo cache nếu chưa có. Cache nối từ `residue_data.load_all()` và trọng số PAP hiện có, không phải một nguồn dữ liệu mới. Muốn dựng lại cache từ đầu, di chuyển riêng `data/processed/g2-saturation-input.npz` sang nơi lưu tạm rồi chạy lại; không xóa nguồn thô. Trường/schema và lineage ở [data/README](../../data/README.md). Kết quả nhỏ JSON/log nằm ở đây; ma trận, dự đoán, checkpoint nằm ở data và bị gitignore.
