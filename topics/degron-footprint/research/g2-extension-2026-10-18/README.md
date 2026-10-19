# G2 — mở rộng, 18/10/2026: ba câu hỏi còn mở của báo cáo bão hoà

Tiếp nối [benchmark bão hoà cùng ngày](../g2-saturation-2026-10-18/README.md) §5. Tiêu chí của cả ba thí nghiệm được chốt **trước khi chạy** ở [PREREGISTRATION.md](PREREGISTRATION.md); phần này chỉ báo kết quả, không sửa tiêu chí. Trạng thái và điều kiện chính thức vẫn ở [DECISIONS.md](../../../../DECISIONS.md#hien-hanh).

**[ĐO] Kết quả một dòng.** Mốc số 0,7693 **đã vượt** và vẫn vững, nhưng cả ba câu hỏi còn lại đều trả lời **theo hướng bất lợi cho tuyên bố kiến trúc**: (E1) bỏ hết phần dữ liệu trùng khít, Degformer vẫn **0,9227** nên chồng khít **không** giải thích được khoảng cách; (E2) **cả ba** ứng viên tương tác tiền đăng ký đều **thua ridge thường** ở mọi seed; (E3) chính kiến trúc Degformer, huấn luyện lại dưới cov80 với cùng ngân sách nhãn, chỉ đạt **0,7500** — thua ridge **và** thua cả ΔPAP đóng băng.

**[DIỄN GIẢI] Ba kết quả âm này chỉ về cùng một phía.** Ở n = 89 cụm, nút thắt **không phải sức chứa của mô hình mà là lượng nhãn** (§3b). **G2 vẫn chưa hoàn tất**, và nay lý do đã cụ thể hơn: không phải thiếu số, mà là **chưa có thành phần kiến trúc nào kiếm được chỗ đứng**, và bốn lần thử thêm sức chứa đều đi sai hướng.

## 1. E1 — Degformer trên tập con không chồng huấn luyện [ĐO]

Câu hỏi: bỏ 88,12% ô có **đúng sequence** trong `training_data.csv` thì còn lại gì?

| Mô hình | Toàn bộ 47.847 ô | Chỉ 5.684 ô không chồng | Chênh |
|---|---:|---:|---:|
| Degformer, checkpoint epoch50 | 0,9248 | **0,9227** | −0,0021 |
| Ridge M3 | 0,8082 | 0,8040 | −0,0042 |
| Gate + ΔPAP | 0,8002 | 0,7956 | −0,0046 |
| ΔPAP `cnn2w1` | 0,7693 | 0,7531 | −0,0162 |

Phép so ghép cặp **trên riêng tập con** (85 peptide còn đủ hai lớp, 83 cụm, bootstrap 5.000 lần theo cụm): Degformer − ridge = **+0,1187** [+0,0940; +0,1446]; Degformer − ΔPAP = +0,1696 [+0,1421; +0,2005]; ridge − ΔPAP = +0,0509 [+0,0239; +0,0812].

**Đọc đúng kết quả này, kể cả khi nó bất lợi.** Báo cáo buổi sáng ngụ ý rằng 88,12% chồng khít là lý do khiến 0,9248 không đáng tin. **Phép đo này bác cách đọc đó:** bỏ hết phần chồng khít, điểm chỉ rụng **0,0021**. Vậy chồng khít ở mức **ô** không phải nguồn của khoảng cách.

**Nhưng tập con này vẫn không phải clean holdout**, và lý do thì rõ hơn trước: rò rỉ nằm ở **mức peptide**, không phải mức ô. WT của **91/91** peptide có trong tập huấn luyện của Degformer, mỗi peptide còn trung vị **57** ô giữ lại trên nền ~500 ô đã thấy, và **không peptide nào** có 0 ô chồng. Mô hình đã học gần trọn ma trận của từng peptide; che vài chục ô không tạo ra peptide mới. Vì vậy E1 **không** cho phép nói "Degformer tổng quát hoá tốt", chỉ cho phép nói: **giả thuyết "khoảng cách do trùng khít" đã bị loại, và câu hỏi về tổng quát hoá phải trả lời bằng một bản huấn luyện lại, không bằng cách lọc ô.**

Kết quả đầy đủ: [e1-overlap.json](e1-overlap.json).

## 2. E2 — ba ứng viên tương tác thay thế × ngữ cảnh [ĐO]

Cùng đặc trưng M3 180 chiều, cùng lịch học, cùng 3 seed 17/29/43, cùng phép chia; không nhánh ΔPAP để đọc riêng đóng góp của tương tác.

| Ứng viên | AUROC ensemble | So với ridge M3 (ghép cặp) | Ba seed so với ridge | Đạt tiêu chí? |
|---|---:|---:|---|:--:|
| Ridge M3 *(mốc so sánh)* | **0,8082** | — | — | — |
| `film` — FiLM, pair sinh scale và shift | 0,8028 | −0,0054 [−0,0136; +0,0028] | −0,0104 · −0,0162 · −0,0091 | **Không** |
| `bilinear` — song tuyến hạng 8 | 0,7933 | −0,0149 [−0,0227; −0,0072] | −0,0212 · −0,0275 · −0,0335 | **Không** |
| `cross_ridge` — ridge + 2.400 chiều tích chéo | 0,7924 | −0,0158 [−0,0227; −0,0086] | tất định, một giá trị | **Không** |

So với ΔPAP đóng băng thì **cả ba đều dương**: FiLM +0,0335 [+0,0179; +0,0498], bilinear +0,0240 [+0,0058; +0,0433], cross_ridge +0,0231 [+0,0048; +0,0420].

**Kết luận, đúng theo tiêu chí đã chốt trước:** **không ứng viên nào đạt**. Điều kiện (a) — dương ở cả ba seed — hỏng ngay ở ứng viên tốt nhất. Cộng với cổng sigmoid của báo cáo buổi sáng, nay đã thử **bốn** cơ chế tương tác khác nhau, và **cả bốn** đều không vượt được một mô hình tuyến tính có hiệu chuẩn trên cùng bộ đặc trưng.

**Điều này nói lên cái gì, và không nói lên cái gì.** Nó **không** chứng minh rằng tương tác thay thế × ngữ cảnh là không tồn tại; nó cho thấy ở **cỡ mẫu này** (89 cụm, trần nhãn 0,9519, ICC cao) phần tương tác học thêm được **không bù nổi** phương sai mà nó mang vào. Hệ quả cho đề cương: tuyên bố "kiến trúc mới" **không được** dựa vào bất kỳ thiết kế nào trong bốn thiết kế đã thử, và nếu còn theo đuổi hướng này thì phải đổi **nguồn lực thống kê** (thêm nhãn, thêm replicate, hoặc học chuyển tiếp từ nhãn mức túi), không phải đổi thêm một biến thể lớp mạng nữa.

Kết quả đầy đủ và từng seed: [e2-candidates.json](e2-candidates.json), log [e2.log](e2.log).

## 3. E3 — kiến trúc Degformer dưới cùng ngân sách nhãn [ĐO]

Dựng lại **đúng** class `PeptideTransformer` (d_model 128, 4 lớp, 8 head, ff 256, dropout 0,1) và **đúng** siêu tham số công bố (Adam lr 1e-4, batch 512), huấn luyện **từ đầu** trên nhãn bão hoà của đề tài, 5 outer fold cov80, inner validation chọn epoch, seed 17. Trung thành với công thức tác giả: hồi quy **PSI tuyệt đối** chuẩn hoá z theo outer-train, điểm ô = `pred(mutant) − pred(WT)`.

| Mô hình | AUROC mức ô macro | Điều kiện |
|---|---:|---|
| Ridge M3 | **0,8082** | học bão hoà, OOF cov80 |
| ΔPAP `cnn2w1` | 0,7693 | frozen |
| **Kiến trúc Degformer, cov80, cùng ngân sách nhãn** | **0,7500** | học bão hoà, OOF cov80, 1 seed |
| Degformer, checkpoint công bố | 0,9248 | **có chồng dữ liệu lớn**, không phải clean holdout |

| Phép so ghép cặp | Delta | CI 95% theo cụm | Peptide thắng |
|---|---:|---|---:|
| Kiến trúc Degformer − ridge | **−0,0582** | [−0,0734; −0,0426] | 15/91 |
| Kiến trúc Degformer − ΔPAP | **−0,0193** | [−0,0330; −0,0058] | 31/91 |

**Giới hạn đã tiền đăng ký, nay kiểm được:** trần 30 epoch **không bị chạm ở fold nào**. Cả **5/5 fold** đều có epoch tốt nhất là **2**, rồi validation MSE tăng đơn điệu cho tới khi patience cắt ở epoch 8. Vậy con số 0,7500 **không phải do huấn luyện thiếu**; nó là điểm tốt nhất mà inner validation chọn được. Giới hạn còn lại và vẫn đúng: **1 seed**, siêu tham số **không** hiệu chỉnh lại cho cỡ dữ liệu nhỏ hơn, và E3 **không** tái lập tiền huấn luyện 569.270 dòng của tác giả.

**Phát biểu được rút ra, đúng phạm vi đã chốt trước:** *ở ngân sách nhãn này, transformer không hơn ridge* — và ở đây nó còn **thua cả ΔPAP đóng băng**. **Không** được đọc thành "Degformer kém".

## 3b. Ba thí nghiệm hợp lại nói một điều [DIỄN GIẢI]

E1 và E3 kẹp chặt câu hỏi về Degformer từ hai phía. E1 loại giả thuyết "khoảng cách là do chồng khít mức ô" — bỏ hết phần trùng, điểm gần như không đổi. E3 loại giả thuyết "khoảng cách là do kiến trúc transformer" — cùng kiến trúc, cùng phép chia, cùng nhãn thì nó **tụt xuống 0,7500**. Phần còn lại, và là phần duy nhất chưa bị loại, là thứ E3 cố ý **không** tái lập: **569.270 dòng tiền huấn luyện**.

Ghép với E2 — bốn cơ chế tương tác đều thua một mô hình tuyến tính — thì cả ba thí nghiệm chỉ về **cùng một phía**: ở n = 89 cụm với trần nhãn 0,9519, nút thắt **không phải sức chứa của mô hình mà là lượng nhãn**. Mọi thiết kế có sức chứa lớn hơn trong phiên này đều trả giá bằng phương sai nhiều hơn phần nó học thêm được.

Đây là **diễn giải**, không phải phép đo: nó dựa trên ba kết quả âm nhất quán chứ không trên một thí nghiệm được thiết kế để tách riêng yếu tố "lượng nhãn". Thí nghiệm tách riêng đó — đường cong học theo số cụm huấn luyện, hoặc tiền huấn luyện trên nhãn mức túi rồi tinh chỉnh — **chưa chạy**, và nó là việc tiếp theo mà ba kết quả này chỉ tới.

## 4. Mức hoàn thành G2 sau phiên này

| Điều kiện | Trước 18/10 | Sau E1–E2 |
|---|---|---|
| Vượt mốc ΔPAP 0,7693 | chưa | **đạt**, ridge +0,0389, và vẫn đạt trên tập con không chồng (+0,0509) |
| Thành phần kiến trúc có lợi ổn định | chưa | **vẫn chưa** — đã loại **bốn** thiết kế có tiền đăng ký, cộng kiến trúc transformer đã công bố (E3) là **năm** |
| Tính mới kiến trúc | chưa | **vẫn chưa**, và cơ sở để tuyên bố đã **hẹp lại** |
| Đối chứng Degformer sạch | chưa | **một nửa**: kiến trúc của nó dưới cov80 cùng ngân sách nhãn đã đo (**0,7500**, E3); bản **giữ nguyên tiền huấn luyện 569k dòng nhưng loại cụm test** thì vẫn chưa — ước lượng ≈70 giờ CPU trên máy này |
| Bằng chứng xác nhận cuối cùng | chưa | vẫn chưa; tất cả vẫn là benchmark phát triển OOF |

**Việc tiếp theo mà ba kết quả này chỉ tới** (đề xuất, chưa được Trọng quyết — xem [C](../../../../DECISIONS.md#cho-xac-nhan)): đo **đường cong học theo số cụm huấn luyện** để xác nhận trực tiếp rằng nút thắt là lượng nhãn, rồi thử **tiền huấn luyện trên nhãn mức túi** (260k peptide / 212k tile) và tinh chỉnh trên bão hoà. Đây đúng là giả thuyết "giám sát yếu" mà [D-031](../../../../DECISIONS.md#d-031) đã đặt làm chỗ của tính mới; ba kết quả âm trên phiên này khiến nó thành **đường găng**, không còn là một nhánh tuỳ chọn.

Không nới cổng G2. Không ghi G2 hoàn tất. Không ghi quyết định mới ở B1/B2 trong phiên này.

## 5. Dựng lại

```bash
.venv/bin/python -I topics/degron-footprint/research/g2-extension-2026-10-18/run_ext.py overlap
OMP_NUM_THREADS=4 .venv/bin/python -I topics/degron-footprint/research/g2-extension-2026-10-18/run_ext.py candidates
OMP_NUM_THREADS=4 .venv/bin/python -I topics/degron-footprint/research/g2-extension-2026-10-18/run_ext.py degformer_arch
```

Dùng lại cache `data/processed/g2-saturation-input.npz` của báo cáo buổi sáng, không tạo nguồn dữ liệu mới. Checkpoint và dự đoán ghi vào `data/processed/` và bị gitignore; JSON kết quả nằm trong thư mục này. Nguồn Degformer vẫn đọc từ `data/raw/degformer-isolated/` theo commit ghim, chạy bằng `python -I`, đúng ràng buộc [D-028](../../../../DECISIONS.md#d-028) mục 8.
