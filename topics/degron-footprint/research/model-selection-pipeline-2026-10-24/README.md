# Pipeline lựa chọn mô hình degron-footprint theo từng câu hỏi

Ngày tổng hợp: 24/10/2026. Đây là khung tổ chức lập luận và chỉ mục bằng chứng cho sáu điểm Trọng đã chọn; không phải một thí nghiệm mới hay bản thay thế protocol R2/R6. Phiên này chỉ đọc mã/kết quả và sinh bảng tổng hợp, không huấn luyện hoặc chọn lại mô hình sản phẩm. Trạng thái G2/G3 giữ nguyên.

## 1. Bài toán và đầu ra cố định

Một mẫu là `(trình tự WT, vị trí i, amino acid thay vào a)`. WT (*wild type*) là trình tự tham chiếu trước thay thế. Mô hình học nhãn liên tục `ΔPSI = PSI(mutant) − PSI(WT)`; điểm cao biểu thị phép thay làm reporter bền hơn trong hệ đo Zhang. Khi đánh giá AUROC, ô dương được định nghĩa bằng nhãn đo `ΔPSI ≥ 1`, không phải bằng ngưỡng 1 áp vào mọi điểm mô hình. Nguồn định nghĩa: [dataset-guide](../../../../resources/dataset-guide.md).

Chạy suy luận cho các phép thay khác WT tạo ma trận hiệu ứng 28 vị trí × 19 phép thay. Nhãn đo có thể thiếu ô; chỉ chấm trên ô hợp lệ. Đây là dự đoán hiệu ứng đột biến trên peptide trong miền áp dụng, không trực tiếp xác định E3 hay phân loại một peptide bất kỳ thành degron/non-degron. Nếu cần gộp thành điểm mỗi residue, phải ghi trước phép gộp và tiêu chí đánh giá; không chọn max/mean sau khi xem kết quả.

## 2. Dữ liệu và phép so sánh chung

`[ĐỌC-MÃ]` Thiết kế R6 dùng [r6data.py](../r6-ladder-scan-2026-10-23/r6data.py), [common.py của R2](../r2-esm-features-2026-10-22/common.py) và [protocol R6 §2](../r6-ladder-scan-2026-10-23/PROTOCOL.md):

- Pool bão hòa: **176 peptide / 172 cụm / 92.337 ô**; trong đó 91 peptide gốc có 47.847 ô, 85 peptide mở rộng có 44.490 ô. Các số được ghi trong protocol R6 và `posthoc-r6.json`; sổ nguồn nằm trong [evidence.json](evidence.json).
- Outer-test: **91 peptide / 89 cụm** gốc ở ngưỡng PSI(WT) ≤ 3,0, chia năm fold theo cụm cov80 trùng G2. Nhóm mở rộng tới PSI(WT) ≤ 4,0 chỉ vào pool huấn luyện/validation sau khi loại cụm test. Không có 176 peptide test độc lập.
- Cùng `(seed, fold)` thì dùng cùng tập train/validation/test cho mọi đối chứng mới; seed 17, 29, 43. Đầu ra test là dự đoán ngoài fold (OOF).
- Ridge hiện có chọn α bằng MSE validation rồi khớp lại trên train ∪ validation; mạng chọn epoch bằng MSE validation và không khớp lại trên train ∪ validation. Cùng phép chia chưa có nghĩa cùng số hàng dùng khớp mô hình cuối. Khi so hai họ, ghi rõ khác biệt này.
- Chỉ số chính kế thừa: AUROC mức ô, tính riêng từng peptide rồi lấy trung bình. Báo từng seed, trung bình AUROC các seed và AUROC của điểm trung bình ba seed thành các cột riêng; ba đại lượng không đồng nhất.
- So mô hình bằng chênh lệch ghép cặp trên cùng peptide; bootstrap theo cụm protein. Giữ nguyên họ kiểm định/CI/kết luận lịch sử của R6. Mọi phép so mới phải ghi vai trò và cách xử lý đa so sánh trước lượt chạy.
- Các bước có học từ dữ liệu (chuẩn hóa, PCA, chọn siêu tham số) phải được mô tả theo fold. Với thí nghiệm mới, khớp biến đổi trên train khi chọn mô hình; sau khi chốt lựa chọn có thể khớp lại trên train ∪ validation theo quy tắc đã ghi. Không đưa outer-test vào bước khớp nào. Không suy diễn rằng mọi runner lịch sử đã dùng đúng cùng quy trình này.

## 3. Chuỗi câu hỏi và các mô hình đối chứng

Mỗi hàng là một mô hình huấn luyện riêng, không truyền điểm dự đoán từ hàng trước vào hàng sau. Các mã L/N dưới đây chỉ là tên trong tài liệu này, không đổi tên M0–M4 hay cấu hình R6.

| Bước | Mô hình/đầu vào | Câu hỏi cụ thể | Phép so cần có | Bằng chứng hiện có |
|---|---|---|---|---|
| L0 | One-hot WT tại i + one-hot amino acid thay vào → Ridge | Chỉ xu hướng chung của amino acid gốc và amino acid thay vào giải thích được bao nhiêu? | Mốc tối thiểu có thông tin về phép thay | Chưa có arm riêng trong bảng R6 đã đọc |
| L1 | L0 + composition peptide WT → Ridge | Thành phần toàn peptide bổ sung gì ngoài xu hướng thay thế? | L1 − L0, kèm giới hạn ở §3.1 | Tương ứng khối đặc trưng `M0_composition_only`; chưa có kết quả riêng theo thiết kế R6 |
| L2 | L1 + composition cửa sổ quanh i, bỏ thứ tự → Ridge | Vùng gần điểm đột biến có hữu ích hơn toàn peptide không? | L2 − L1 | Có trong thí nghiệm lịch sử; chưa cùng thiết kế bão hòa R6 |
| L3 | L1 + one-hot từng vị trí tương đối quanh i → Ridge | Giữ thứ tự/ngữ cảnh tương đối có hơn chỉ đếm amino acid không? | L3 − L2 ở cùng bán kính; L3 − L1 | Ridge ±3 và ±5 có trong R6; chưa có L2 ghép tương ứng trên R6 |
| N1 | One-hot cửa sổ WT + chỉ báo trung tâm → single-window CNN hoặc MCNN, ghép cặp thay thế và composition | Học tổ hợp phi tuyến từ nhãn có vượt Ridge ngữ cảnh không? | `oh_cnn1`, `oh_mcnn` − Ridge ngữ cảnh | Đã đo trong R6 |
| N2 | ESM đóng băng, embedding WT/mutant → đầu không trộn vị trí | ESM đã đủ hữu ích khi không học tổ hợp các vị trí liên tiếp chưa? | Đối chứng tương ứng N3 ở §5 | R2 có embedding gộp + PCA + Ridge, nhưng chưa tương ứng hoàn toàn với đầu CNN R6 |
| N3 | Cùng đầu vào của N2 → CNN một cửa sổ | Học các tổ hợp embedding liên tiếp giúp thêm gì? | N3 − N2 | `esm35_cnn1` đã có; thiếu đầu N2 tương ứng |
| N4 | Cùng biểu diễn/thông tin phụ → MCNN | Nhiều cửa sổ bổ sung cho nhau không? ESM bổ sung gì cho đầu one-hot? | N4 − N3; N4 − `oh_mcnn`; N4 − `ridge_W5` | Đã đo trong R6, với giới hạn diễn giải ở §4 |

### 3.1 Giới hạn của baseline composition cần nêu trong luận văn

`[ĐỌC-MÃ]` [derisk.featurize và MODELS](../residue-task-derisk-2026-10-15/derisk.py) định nghĩa `M0_composition_only = {pair, comp}`: 40 chiều one-hot gốc/thay + 20 chiều composition, không phải chỉ 20 chiều composition. Hai one-hot trong Ridge học tác động cộng, không có một hệ số tự do cho từng cặp WT→mutant.

`[DIỄN GIẢI từ dạng mô hình]` Với L1 tuyến tính:

```text
f(S, i, a) = hệ số amino acid gốc + hệ số amino acid thay
             + w_comp · composition(S) + bias
```

Trong cùng peptide S, phần composition là hằng số nên triệt tiêu khi so hai ô. Nó không trực tiếp đổi thứ hạng trong peptide với các hệ số còn lại cố định. L1 và L0 huấn luyện riêng vẫn có thể khác AUROC vì các hệ số gốc/thay được ước lượng lại; chênh lệch ấy không chứng minh composition đã giúp phân biệt hai vị trí có cùng phép thay. Muốn kết luận về giá trị composition đối với mức ΔPSI giữa peptide, cần chỉ số phù hợp như sai số hồi quy đã ghi trước, thay vì chỉ AUROC trong peptide.

L3 so với L2 giữ họ Ridge nhưng đổi số chiều và sức biểu diễn. Kết quả dương hỗ trợ ích lợi của biểu diễn có vị trí tương đối trong điều kiện đã thử; chưa phải bằng chứng cơ chế E3 hay phép tách duy nhất tác động của thứ tự.

### 3.2 Không ghép các con số khác thiết kế thành một đường tăng dần

`[ĐO đã lưu]` [model.json lịch sử](../residue-task-derisk-2026-10-15/model.json) có L1/L2/L3 tương ứng M0/M2/M3. Hai nhánh là CV trên scanning và học scanning rồi chuyển sang saturation. Chúng không phải các arm học trên pool bão hòa ext4.0 theo phép chia R6. Bảng [results.md](results.md) đặt chúng riêng, không dùng chênh AUROC giữa các bảng để chứng minh một thành phần tốt hơn.

`[ĐỌC-MÃ]` Chú thích cũ trong `model.json` mô tả scanning gần như toàn bộ →R đã lỗi thời; đối chiếu [audit scanning](../scan-sat-merge-2026-10-23/README.md) và [posthoc-r6.json](../r6-ladder-scan-2026-10-23/posthoc-r6.json): phép thay chỉ thuộc R/A/S và bị ràng buộc bởi WT. Giữ file lịch sử nguyên trạng; không sao chép chú thích này thành mô tả dữ liệu mới.

## 4. Dùng R6 trả lời đúng những câu đã đo

`[ĐO đã lưu]` Xem [bảng tự sinh từ JSON](results.md) cho toàn bộ điểm từng seed, ensemble, chênh lệch và CI; nguồn gốc là [results.json R6](../r6-ladder-scan-2026-10-23/run-kaggle-20261023/results.json), không phải số mới đo trong phiên này.

- **Ngữ cảnh rộng hơn:** họ A nhận `ridge_W5` so với `ridge_M3` theo tiêu chí của R6. Đây là bằng chứng trong benchmark phát triển; chưa tự đổi mô hình sản phẩm.
- **ESM bổ sung cho one-hot MCNN:** S1 dương theo tiêu chí phụ. `ConvHead` vẫn giữ one-hot WT, chỉ báo trung tâm, cặp thay thế và composition khi thêm Δ embedding ESM. Đây là lợi ích của kênh ESM bổ sung, không phải phép thay thế thuần one-hot bằng ESM và cũng chưa tách hoàn toàn tác động thêm tham số.
- **MCNN so với single-window:** S5/S6 chưa đủ bằng chứng; single-window R6 cố định k=5, 96 bộ lọc, MCNN k=3/5/7, mỗi nhánh 32 bộ lọc. Tổng số bộ lọc bằng nhau và tổng tham số tích chập bằng nhau trong cùng biểu diễn (tổng k bằng nhau), nhưng hai kiến trúc không đồng nhất. R6 chưa chọn single-window tốt nhất từ nhiều k bằng validation.
- **ESM MCNN so với Ridge:** P so với Ridge ±3 chưa đạt tiêu chí xác nhận. S7 so với Ridge ±5 cũng chưa đủ bằng chứng. S1 dương không thay thế cho P hoặc S7.
- **Hiệu ứng ensemble:** báo điểm từng mạng cùng điểm gộp. Kết quả hậu kiểm về ensemble phải mang nhãn hậu kiểm; không coi ba seed là ba bộ dữ liệu độc lập.

Không chọn cấu hình đứng đầu tất cả các hàng R6 rồi báo điểm đó như ước lượng tổng quát hóa không chệch. Các thí nghiệm dùng thêm scanning chỉ là nhánh về nguồn nhãn; không dùng để thay đổi phép so kiến trúc/biểu diễn mà không nêu rõ đã đổi dữ liệu huấn luyện.

## 5. Khoảng trống ưu tiên nếu bổ sung thí nghiệm

`[ĐỀ XUẤT — chưa chạy, chưa phải protocol chốt]` Một đối chứng **không học tổ hợp liên vị trí** tương ứng với `esm35_cnn1` trả lời rõ hơn việc thêm nhiều cỡ ESM.

Giữ đầu vào của R6: ESM-2 35M đóng băng, lớp cuối; `ΔH = H_mutant − H_WT`; cắt ±7 quanh i; cùng one-hot WT, chỉ báo trung tâm, mask padding, cặp thay thế và composition. Giữ phép chiếu Δ embedding d→32 và phần hồi quy cuối.

```text
Nhánh không trộn vị trí: Linear áp riêng mỗi vị trí → ReLU → [max hợp lệ; trung tâm]
Nhánh CNN:              Conv k=5              → ReLU → [max hợp lệ; trung tâm]
                                               ↓
                              cùng thông tin phụ và đầu hồi quy
```

Nhánh đầu tương đương phép biến đổi pointwise (kernel 1), không học quan hệ giữa hai vị trí liên tiếp ở tầng này. ESM trước đó vẫn có ngữ cảnh; không gọi nhánh này là "không có thông tin thứ tự". Dùng cùng 96 kênh đầu ra để giữ cùng kích thước đầu hồi quy; số tham số tầng trích xuất vẫn khác và phải được báo. Đây là phép đo giá trị bổ sung của bộ lọc trộn vị trí trong một kiến trúc đã xác định, chưa loại hết ảnh hưởng sức chứa.

Mean pooling toàn chuỗi kiểu DeepNeoAg có thể là một đối chứng mô tả riêng, nhưng không thay cho phép so trên: đổi đồng thời phạm vi cửa sổ, pooling, PCA và đầu mạng sẽ làm mất khả năng quy chênh lệch cho CNN.

Các arm L0/L1/L2 cần có kết quả theo đúng thiết kế R6 nếu muốn hoàn thiện bảng đối chứng tuyến tính chung. Tài liệu này chỉ ghi khoảng trống, không gán số lịch sử hoặc số giả cho các arm đó. Trước một lượt chạy bổ sung cần protocol riêng ghi cấu hình, phép so chính, ngân sách, tiêu chí và vai trò phát triển; benchmark đã được xem nên không gọi là kiểm chứng trên tập chưa đụng tới.

## 6. Khóa lựa chọn trước khi kiểm tra peptide mới

`[ĐỀ XUẤT]` Tách hai mục tiêu:

1. **Lập luận nghiên cứu:** báo câu hỏi nào đã trả lời, câu nào chưa đủ bằng chứng; giữ kết quả âm và chi phí tương ứng. Ridge ±5 là đối chứng mạnh cần được so sánh, không phải quyết định triển khai mới.
2. **Lựa chọn để kiểm chứng:** chốt danh sách ứng viên hữu hạn, một phép so chính, toàn bộ siêu tham số, cách ghép seed/hiệu chuẩn và tiêu chí trước khi xem kết quả đánh giá tiếp theo. Đánh giá cả chất lượng, độ ổn định và chi phí suy luận theo ngân sách được xác định trước. Phép trộn điểm từng xuất hiện ở hậu kiểm phải được khai báo là giả thuyết sinh từ dữ liệu phát triển.

Nguồn đánh giá tiếp theo đang được đề xuất ở [R6 §3.5](../r6-ladder-scan-2026-10-23/README.md): scanning ngoài cụm saturation. [evidence.json](evidence.json) lưu số kiểm kê theo cov80 từ `posthoc-r6.json`; đây là **kiểm kê có sẵn**, chưa phải kết quả một lượt kiểm chứng mô hình mới.

Trước khi dùng nguồn đó:

- Kiểm tra nguồn và lịch sử tiếp xúc. [sat_to_scan_eval.py/results-sat-to-scan.json](../scan-sat-merge-2026-10-23/README.md) đã có đánh giá thăm dò trên miền scanning ngoài cụm; vì thế không gọi toàn bộ nguồn scanning là tập test hoàn toàn chưa xem. Có thể khai báo là kiểm chứng theo protocol mới trên một nguồn đã thăm dò; nếu muốn kiểm chứng hoàn toàn chưa xem thì cần nguồn khác hoặc tập con chứng minh được chưa tham gia lựa chọn.
- Nếu mô hình/tiền huấn luyện dùng scanning, loại khỏi mọi giai đoạn huấn luyện/validation những cụm đã dành cho đánh giá. Không chấm một mạng `scan_pool`/`scan_ft` đã học các peptide đánh giá rồi gọi đó là peptide mới.
- Chốt mức kiểm soát tương đồng: ngoài cov80 cần đánh giá cov50 hoặc luật loại theo hit; sau khi lọc lại, kiểm kê lại kích thước, không mặc định số cov80 còn đúng.
- Ghi rõ cùng phòng thí nghiệm và hệ đo, nhãn scanning khác thiết kế saturation, chỉ có R/A/S, không kiểm toàn bộ 19 phép thay mỗi vị trí. So chênh lệch mô hình trên cùng tập scanning; không so thẳng AUROC tuyệt đối scanning với saturation để kết luận tiến bộ.
- Chỉ chấm một lượt theo protocol đã khóa. Nếu dùng kết quả để chọn/đổi mô hình thì nguồn đó trở thành dữ liệu phục vụ lựa chọn và cần lượt xác nhận tiếp theo phù hợp với phạm vi tuyên bố.

## 7. Dàn ý lập luận cho luận văn

1. **Đích dự đoán và giới hạn:** vì sao cần ma trận hiệu ứng thay thế, nhãn ΔPSI đo gì và không đo gì.
2. **Đối chứng tối thiểu:** xu hướng amino acid gốc/thay, thành phần toàn peptide và giới hạn thứ hạng trong peptide.
3. **Ngữ cảnh:** phân biệt đếm amino acid vùng gần với vị trí tương đối; giải thích vì sao Ridge ngữ cảnh phải có trước đối chứng mạng.
4. **Biểu diễn và kiến trúc:** trình bày R2/R6 theo từng phép so, giữ riêng ESM bổ sung, tích chập và nhiều cửa sổ.
5. **Độ ổn định:** từng seed, ensemble, CI theo cụm và giới hạn do khảo sát lặp benchmark phát triển.
6. **Lựa chọn và khả năng chuyển miền:** đóng băng lựa chọn, đánh giá peptide mới trong phạm vi nguồn cho phép, rồi ghi model card/chi phí trước quyết định sản phẩm.

## 8. Tái tạo bảng bằng chứng

```bash
python3 -I topics/degron-footprint/research/model-selection-pipeline-2026-10-24/build_evidence.py
```

[build_evidence.py](build_evidence.py) chỉ đọc JSON/mã/protocol đã có, không import runner nghiên cứu hoặc truy cập `data/`; ghi [evidence.json](evidence.json) và [results.md](results.md) trong thư mục này. JSON chứa đường dẫn tương đối, SHA-256 nguồn, điểm chọn lọc và kết luận nguyên bản; không tái tính bootstrap từ OOF. Bảng giữ CI đã hiệu chỉnh khi nguồn có `ci_adj`; các phép phụ vẫn mang vai trò phụ.
