# Tiền đăng ký B — tách "thêm cụm" khỏi "mở rộng phân bố"

Chốt **trước khi chạy** phần B, sau khi đã có kết quả phần A ([PROTOCOL.md](PROTOCOL.md), [results.json](results.json)). Viết riêng vì đây là **câu hỏi mới**, không phải sửa tiêu chí của phần A.

## 1. Câu hỏi

Phần A `[ĐO]`: thêm 85 peptide nới ngưỡng cho **+0,0126** (ridge), nhưng việc đó tăng **đồng thời** số cụm train (71 → 154) và độ phủ phân bố PSI(WT) (thêm vùng 3,0–4,0). [README §4](README.md) ghi rõ phần A **không** tách được hai yếu tố.

Câu hỏi B: ở cùng một mức số cụm tăng thêm, **một cụm thuộc vùng PSI(WT) 3,0–4,0 có giá trị biên khác một cụm thuộc vùng ≤ 3,0 hay không?**

## 2. Vì sao câu hỏi này nhận dạng được

`[ĐO]` Phần A đã đo giá trị biên của cụm **vùng cũ** ở quanh mốc 71 cụm: đi từ 35–36 lên 70–72 cụm cho ridge chỉ **+0,0038**, CI **[−0,0009; +0,0087]** phủ 0. Tức ở vùng cũ, cụm thứ 36 đến thứ 71 gần như **không còn giá trị biên**.

`[ĐỀ XUẤT]` Vậy nếu thêm **cùng số cụm** nhưng lấy từ vùng mới mà AUROC tăng rõ hơn hẳn 0,0038, thì yếu tố quyết định là **cụm đó ở đâu trong phân bố**, không phải việc có thêm một cụm.

## 3. Thiết kế

- Phần cũ **giữ nguyên 100%**: mọi cụm outer-train của bộ 91 peptide luôn có trong train, ở mọi mức.
- Thêm cụm mới theo **tập con lồng nhau** 25/50/75/100% của 83 cụm nới ngưỡng, trộn thứ tự bằng seed, lấy tiền tố. Mức 100% chính là mức `ext` đã chạy ở phần A.
- Outer-test, outer fold, nhãn, chỉ số, đặc trưng M3, hai mô hình (ridge, `gate_no_pap`), ba seed 17/29/43, bootstrap 5.000 lần theo cụm: **giữ y nguyên phần A**. Cổng tự kiểm trùng `folds` của G2 vẫn áp dụng.
- Peptide mới thuộc cụm test của fold nào thì vẫn bị loại khỏi train fold đó, như phần A.

## 4. Tiêu chí, chốt trước

Gọi B(f) là AUROC macro ensemble ba seed khi thêm f% cụm mới; B(0) = mức 100% của phần A.

- **Tiêu chí chính — giá trị biên khác nhau.** Lấy mức thêm cụm mới **gần nhất với 36 cụm** (tức f = 50%, khoảng 41 cụm). Ủng hộ cách đọc "mở rộng phân bố" khi CI95 ghép cặp theo cụm của B(50%) − B(0) **nằm hoàn toàn trên +0,0038** — là giá trị biên đo được của 36 cụm vùng cũ ở phần A.
  - CI dương nhưng **chứa** 0,0038 → "cụm vùng mới có giá trị, nhưng **chưa** chứng minh được giá trị biên cao hơn cụm vùng cũ".
  - CI phủ 0 → "chưa đủ bằng chứng rằng một phần nhỏ dữ liệu vùng mới là đủ".
- **Tiêu chí phụ — hình dạng đường cong B.** Nếu phần lớn lợi ích (≥ 60% của B(100%) − B(0)) đã đạt ở f = 25%, ghi là **"bão hòa sớm"**, ủng hộ cách đọc phân bố. Nếu lợi ích tăng gần tuyến tính theo f tới 100%, ghi là **"tỉ lệ theo số cụm"**, ủng hộ cách đọc số lượng.
- Hai tiêu chí có thể cho kết luận khác nhau; nếu vậy **báo cả hai** và ghi là chưa phân định, **không** chọn cái thuận lợi.

## 5. Việc không làm

- Không đổi ngưỡng nới (vẫn 4,0), không đổi mô hình, không thêm mô hình thứ ba.
- Không chạy lại phần A. Mức `ext` của phần A được dùng lại làm B(100%) **chỉ khi** số liệu tái lập đúng; nếu lệch thì báo lệch.
- Không dùng kết quả B để sửa kết luận phần A; phần A đã chốt theo tiêu chí của nó.
