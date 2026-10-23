# Trộn nhãn bộ quét (scanning) và bộ bão hòa (saturation) — 23/10/2026

Câu hỏi của Trọng: mở rộng bộ dữ liệu bằng cách trộn hai bộ có được không; nếu không thì hướng nào khác, và nhận định "ưu tiên audit 2.994 peptide scanning làm dữ liệu giám sát bổ sung" đúng đến đâu.

Tiêu chí phần B chốt trước ở [PROTOCOL.md](PROTOCOL.md). Phần A chạy trước và được phép ảnh hưởng thiết kế (đã ghi ở PROTOCOL §2). Mục 4 là **thăm dò không tiền đăng ký**. Không đổi trạng thái G2/G3, không sửa đề cương hay slide, không ghi gì vào `data/`.

Nhãn: `[ĐO]` tự đo, trỏ `.json` · `[DIỄN GIẢI]` · `[ĐỀ XUẤT]` · `[CHƯA XÁC MINH]`.

## 0. Kết luận một màn hình

| Câu hỏi | Trả lời `[ĐO]` |
|---|---|
| Hai bộ có **cùng thang nhãn** không? | **Cùng thang biên, đồng thuận từng ô thấp hơn trần.** Trên 3.228 ô là *cùng một đột biến đo ở hai thí nghiệm*, trung bình và SD ΔPSI gần bằng nhau (0,28 / 0,34; 0,71 / 0,72) nhưng Pearson quét↔bão hòa chỉ **0,70–0,72**, trong khi trần mỗi bộ là 0,82 / 0,85. Mốc WT lệch >0,5 PSI ở 31% peptide. Điều kiện quét "BAG6 WT" có PSI WT thấp hơn **1,13** nên không dùng được |
| **Trộn thẳng** có hại không? | Không chứng minh được là hại: S1 − A1 = −0,0019, CI [−0,0057; +0,0017]. Cũng **không có lợi** |
| Trộn **có nhận diện nguồn** hoặc dùng làm **tiên nghiệm** có giúp không? | **Không** (ridge): S2 − A1 = **−0,0005** CI [−0,0009; −0,0000]; S3 − A1 = −0,0011. Mức đó nhỏ hơn MDE 0,0123 hàng chục lần, đọc là "không có lợi", không phải "có hại" |
| Mạng `gate_no_pap` tiền huấn luyện trên quét rồi tinh chỉnh? | N2 − N1 = +0,0015, CI [−0,0046; +0,0077], một seed âm → **không đạt** tiêu chí chốt trước |
| Vậy bộ quét **vô dụng**? | Không. Nó **vô dụng làm nhãn huấn luyện thêm** ở thiết kế này, nhưng là **tập chấm điểm có 1.514 cụm cov80 rời** so với 89 cụm của benchmark hiện tại (mục 4, thăm dò) |

`[DIỄN GIẢI]` Nhận định đã dán xếp "bổ sung scanning" là hướng **đáng ưu tiên nhất**. Với ridge M3 và mạng gate đang dùng, phép đo **không ủng hộ** thứ hạng đó. Phần còn lại của nhận định (số liệu, cách đặt bài toán, các cảnh báo) phần lớn đúng; đối chiếu từng điểm ở mục 5.

## 1. Hai bộ khác nhau ở đâu

| | Bộ quét | Bộ bão hòa |
|---|---|---|
| Nhãn ô | PSI(mutant) − PSI(`mut0`), **một** phép đo WT trực tiếp, **replicate 1** | PSI − trung vị ~28 ô đồng nghĩa, trung bình hai nửa độc lập |
| Thay thế mỗi vị trí | **1, và là hàm tất định của WT** | 19 |
| Ma trận (WT, đột biến) | **20/380 cặp** | 380/380 |
| Quy mô (PSI WT ≤ 4,0) | 4.809 peptide · 133.960 ô · 2.909 cụm cov80 | 176 peptide · 92.337 ô · 172 cụm |
| Quy mô (PSI WT ≤ 3,0) | 2.994 · 83.446 · 1.985 | 91 · 47.847 · 89 |

`[ĐO]` ([audit-labels.json](audit-labels.json), `scanning_design`) **Đính chính mô tả cũ.** Các README trước ghi bộ quét "gần như toàn bộ là →R". Thực tế: **R 64,8%, A 22,7%, S 12,5%**, theo ánh xạ cố định: A,C,D,E,G,I,L,S,T,V → **R**; H,K,N,Q,R,Y → **A**; F,M,P,W → **S**. Hệ quả: đặc trưng "đột biến thành gì" trong bộ quét là hàm của "WT là gì"; bộ quét không dạy gì về 360 cặp còn lại. Chỉ **5,26%** ô outer-test của bão hòa thuộc 20 cặp này.

## 2. Phần A — nhãn có cùng thang không `[ĐO]`

[audit_labels.py](audit_labels.py) → [audit-labels.json](audit-labels.json). Chỉ đọc. **117 peptide** chung hai bộ (sau lọc kỹ thuật, chưa áp ngưỡng degron; 111 cụm), **3.237 ô** là cùng (peptide, vị trí, acid amin) đo ở hai thí nghiệm. Số dưới là nhóm PSI WT ≤ 4,0 (97 peptide, 2.684 ô); nhóm ≤ 3,0 và toàn bộ có kết quả cùng bậc.

| Cặp so | Pearson | Spearman | Độ dốc OLS (y trên x) | Kappa nhị phân | AUROC |
|---|---:|---:|---:|---:|---:|
| quét rep1 ↔ bão hòa (trung bình hai nửa) | **0,716** | 0,563 | 0,728 | 0,658 | 0,903 / 0,937 |
| quét rep2 ↔ bão hòa | 0,686 | 0,540 | 0,701 | 0,622 | 0,888 / 0,901 |
| *trần quét: rep1 ↔ rep2* | *0,822* | *0,730* | *0,818* | *0,724* | *0,949* |
| *trần bão hòa: nửa A ↔ nửa B* | *0,850* | *0,736* | *0,876* | *0,804* | *0,965* |
| quét điều kiện **BAG6 WT** ↔ bão hòa | 0,739 | 0,601 | 0,680 | **0,324** | 0,936 / 0,790 |

- `[ĐO]` Trung bình ΔPSI hai bộ gần nhau (chênh +0,035 đến +0,098) và SD gần bằng nhau (0,711 so với 0,722) → **không có lệch cộng, không có lệch co giãn đáng kể**. Độ dốc OLS 0,73 chỉ là r · SD_y/SD_x = 0,716 · 1,016: nó phản ánh đồng thuận từng ô chưa trọn (regression dilution), **không** phải một hệ số quy đổi thang. Vì vậy hiệu chỉnh tuyến tính hai bộ sẽ không sửa được khoảng cách này.
- `[ĐO]` BAG6 WT: PSI WT thấp hơn bão hòa **1,13**; kéo theo ΔPSI trung bình 1,13 so với 0,34 và tỉ lệ ô dương 0,49 so với 0,17 → khẳng định lại quy tắc D-028 "không trộn BAG6 WT".
- `[ĐO]` Mốc WT: trung vị ô đồng nghĩa (bão hòa) so với `mut0` (quét rep1) trên 117 peptide: Pearson **0,788**, SD chênh 0,58, **30,8%** peptide lệch >0,5 PSI. Nhãn quét mang nhiễu mốc WT chung cho cả 28 vị trí của peptide; nhãn bão hòa thì ít hơn nhiều.
- `[DIỄN GIẢI]` Giả định cổ điển (độ tin cậy ≈ tương quan giữa hai replicate; độ tin cậy của trung bình hai nửa theo Spearman–Brown = 2·0,85/1,85 ≈ 0,92): nếu hai assay đo cùng một tín hiệu thật thì Pearson quét-rep1 ↔ trung bình-bão-hòa kỳ vọng ≈ √(0,82 · 0,92) ≈ **0,87**. Quan sát **0,72** ⇒ tương quan giữa hai tín hiệu thật ≈ 0,72/0,87 ≈ **0,82**, tức còn khác biệt hệ thống giữa hai thí nghiệm (thư viện, mốc WT, replicate, có thể cả điều kiện tế bào), không chỉ nhiễu đo. Ước lượng thô, giả định hai replicate trong mỗi bộ không chia sẻ sai lệch hệ thống; không phải kết quả đã kiểm.
- `[ĐO]` Chồng lặp theo cụm khiêm tốn: **10.046 / 133.960** ô quét (ngưỡng 4,0, **7,5%**) nằm ở cụm có mặt trong bộ bão hòa ext4.0; 92,5% là cụm mới. Nên kết quả null ở mục 3 không do bộ quét "thực chất là bộ bão hòa".

## 3. Phần B — trộn có giúp huấn luyện không `[ĐO]`

[run_merge.py](run_merge.py) → [results.json](results.json). Outer-test = đúng 91 peptide / 89 cụm của G2 (cổng tự kiểm folds trùng G2: đạt). Mốc chính **A1 = ridge ext4.0 = 0,8208** (cổng tái lập: A1 và A0 khớp P0/G2 đúng đến 4 chữ số); bộ giải ridge tự viết khớp sklearn tới 8e-14. Peptide quét thuộc cụm test **và cụm validation** bị loại (số bị loại từng fold: `meta.scan.thr4.0.excluded_by_fold`, 28–73 peptide/fold).

| Arm | AUROC (ensemble 3 seed) | − A1 | CI95 theo cụm | Ba seed | Nhận? |
|---|---:|---:|---|---|---|
| A1 chỉ bão hòa ext4.0 (ridge) | 0,8208 | — | — | — | mốc |
| S0 chỉ quét → bão hòa | 0,7277 | −0,0931 | [−0,1085; −0,0777] | — | tham chiếu |
| S1 gộp, **không** nhận diện nguồn | 0,8189 | −0,0019 | [−0,0057; +0,0017] | −,−,− | không |
| **S2 gộp + nhận diện nguồn (CHÍNH)** | 0,8203 | **−0,0005** | [−0,0009; −0,0000] | −,−,− | **không** |
| S2d như S2, chỉ peptide quét ở cụm *không* thuộc bão hòa | 0,8203 | −0,0005 | [−0,0009; −0,0000] | −,−,− | không |
| S3 quét làm tiên nghiệm (phần dư) | 0,8197 | −0,0011 | [−0,0027; +0,0006] | −,−,− | không |
| N1 `gate_no_pap` ext4.0 | 0,8154 | −0,0054 | [−0,0107; −0,0005] | −,−,− | mốc mạng |
| **N2 gate tiền huấn luyện quét → tinh chỉnh** (lr 2e-3, chính) | 0,8168 | (so N1) **+0,0015** | [−0,0046; +0,0077] | −,+,+ | **không** |
| N2 lr 5e-4 | 0,8160 | (so N1) +0,0006 | [−0,0063; +0,0072] | −,−,+ | không |

Độ nhạy ngưỡng quét 3,0: S1/S2/S3 − A1 = −0,0006 / −0,0001 / −0,0016, cùng kết luận. Lặp lại P0: A1 − A0 = +0,0126, CI [+0,0061; +0,0190], đúng số đã báo.

`[DIỄN GIẢI]` Hai điều cần đọc đúng:

1. **S2 − A1 có CI loại trừ 0 ở phía âm** (biên −0,0000) nhưng |Δ| = 0,0005 ≈ 4% của MDE 0,0123. Đừng đọc là "bộ quét làm hại"; đọc là "bộ quét không thêm gì". S2d giống hệt S2 → việc 10.046 ô quét trùng cụm bão hòa không phải lý do của kết quả null.
2. **N2 − N1 dương nhỏ và không bền**: chỉ ba seed riêng lẻ −0,0047 / +0,0010 / +0,0012. Epoch tốt nhất khi tinh chỉnh là 1–2 (N1 là 2–6), tức mạng đã tiền huấn luyện thích nghi nhanh về bão hòa và bỏ phần lớn thứ học từ quét. Hợp với kết quả âm của [P3](../pretrain-p3-2026-10-22/README.md) (tiền huấn luyện tile).

**Dự đoán ghi trước ([PROTOCOL §6](PROTOCOL.md)) so với kết quả:** (1) S1 ≲ A1 — đúng. (2) S2 − A1 trong [0; +0,01], P(đạt) ≈ 30% — kết quả −0,0005, nằm ngay mép dưới, không đạt. (3) N2 dương hơn S2 — đúng về dấu, không đạt tiêu chí. (4) Lợi ích tập trung ở ô thuộc 20 cặp của bộ quét — **chỉ gợi ý, chỉ ở mạng**; chi tiết và mọi arm ở mục 3b.

`[DIỄN GIẢI]` Vì sao null (giả thuyết, chưa tách): (a) ridge đã phẳng từ ~50% số cụm ([P1](../learning-curve-2026-10-22/README.md)), thêm ~2.900 cụm cho 180 tham số tuyến tính ít có chỗ cải thiện; (b) bộ quét chỉ phủ 20 cặp, 5,26% ô test; (c) đồng thuận từng ô giữa hai bộ chỉ ~0,72 so với trần 0,82–0,85 và mốc WT lệch ở 31% peptide (mục 2). Phép đo này **không** phân biệt ba nguyên nhân.

### 3b. Quy trình "quét học ngữ cảnh → tinh chỉnh bão hòa → chấm cụm giữ riêng", tách 20 cặp / 360 cặp `[ĐO]`

Đề xuất này **đã được chạy**, dưới tên S3 (ridge: khớp trên quét rồi khớp bão hòa trên phần dư, tương đương phạt kéo về w₀ của quét) và N2 (mạng: tiền huấn luyện trên quét rồi tinh chỉnh bão hòa), chấm trên đúng outer-test cụm giữ riêng. PROTOCOL §5(iii) đã chốt trước việc báo riêng 20 cặp có trong quét và 360 cặp còn lại. Phần dưới **mở rộng báo cáo này cho mọi arm có dùng bộ quét** (làm sau khi đã thấy kết quả chính; chỉ thêm báo cáo, không thêm arm, không đổi tiêu chí). Chạy lại với phần mở rộng tái lập đúng mọi AUROC và Δ ở mục 3 (chênh lệch lớn nhất = 0).

Ô test thuộc 20 cặp = **5,26%**. AUROC macro trên từng nhóm chỉ tính peptide có ≥ 3 ô dương và ≥ 3 ô âm *trong nhóm đó*: 59 peptide cho nhóm 20 cặp, 89 cho nhóm còn lại. Mỗi peptide chỉ có ≤ 28 ô trong nhóm 20 cặp (một cặp mỗi vị trí) nên 59 peptide này thiên về peptide nhiều ô dương; mức tuyệt đối của hai nhóm không so trực tiếp được, chỉ so Δ ghép cặp so với mốc cùng nhóm.

| Arm (ngưỡng quét 4,0) | Mốc | Nhóm | AUROC mốc → arm | Δ | CI95 theo cụm |
|---|---|---|---|---:|---|
| S3 quét làm tiên nghiệm (ridge) | A1 | 20 cặp | 0,8045 → 0,8033 | −0,0013 | [−0,0053; +0,0027] |
| | | 360 cặp còn lại | 0,8230 → 0,8219 | −0,0010 | [−0,0026; +0,0005] |
| S2 gộp + nhận diện nguồn (ridge) | A1 | 20 cặp | 0,8045 → 0,8039 | −0,0006 | [−0,0020; +0,0007] |
| | | 360 cặp còn lại | 0,8230 → 0,8225 | −0,0005 | [−0,0009; −0,0001] |
| S1 gộp mù (ridge) | A1 | 20 cặp | 0,8045 → 0,8021 | −0,0024 | [−0,0106; +0,0055] |
| | | 360 cặp còn lại | 0,8230 → 0,8210 | −0,0020 | [−0,0058; +0,0016] |
| **N2 tiền huấn luyện quét → tinh chỉnh** (gate, lr 2e-3) | N1 | 20 cặp | 0,7953 → 0,8041 | **+0,0088** | [−0,0040; +0,0204] |
| | | 360 cặp còn lại | 0,8167 → 0,8157 | −0,0010 | [−0,0073; +0,0053] |
| N2 lr 5e-4 | N1 | 20 cặp | 0,7953 → 0,8044 | +0,0091 | [−0,0026; +0,0202] |
| | | 360 cặp còn lại | 0,8167 → 0,8150 | −0,0017 | [−0,0088; +0,0051] |

Ngưỡng quét 3,0 cho cùng hình dạng (S2/S3 mọi Δ trong [−0,003; +0,0003]; đủ trong [results.json](results.json) → `diagnostic_pair_split`).

`[DIỄN GIẢI]` Đọc theo quy tắc mà đề xuất đã nêu:

- **Nhóm 360 cặp còn lại không cải thiện ở bất kỳ arm nào** (Δ từ −0,0020 đến −0,0005). Vậy phép đo hiện tại **không có bằng chứng** cho chuyển kiến thức ngữ cảnh sang các phép thay chưa xuất hiện trong bộ quét.
- **Nhóm 20 cặp**: ridge không cải thiện (Δ ≤ 0). Chỉ mạng có dấu dương, +0,009 ở cả hai lr, nhưng CI phủ 0 rộng (±0,012–0,016) và ở nhóm 59 peptide thiên lệch. Đây là **gợi ý nhất quán với "cải thiện các phép thay đã quan sát nhiều hơn"**, chưa phải kết luận.
- `[DIỄN GIẢI, chưa kiểm]` Hình dạng "chỉ nhóm 20 cặp nhích lên" hợp với một cơ chế: mạng tiền huấn luyện thấy 20 cặp này 133.960 lần (mọi ô quét chỉ thuộc 20 cặp), rồi toàn mạng được tinh chỉnh trên đủ 380 cặp. Cơ chế đó không để lại dấu ở ridge. Phép đo không tách được cơ chế này khỏi nhiễu.
- **Hạn chế đối với việc dùng kết quả này để quyết định thiết kế pLM + mCNN**: mọi mô hình ở đây là ridge M3 và `Gate` nhỏ. "Không có bằng chứng ở ridge/gate" không bác được khả năng mCNN/ESM-2 — có sức chứa lớn hơn và đọc được ngữ cảnh rộng hơn ±3 — hưởng lợi từ 2.900 cụm quét. Nó chỉ nói rằng kỳ vọng nền cho hướng này **thấp**, và nếu thử thì phải báo tách 20/360 cặp từ đầu.
- Một biến thể sát ý tưởng "quét chỉ học ngữ cảnh" hơn N2: tiền huấn luyện **chỉ nhánh ngữ cảnh** (hoặc đóng băng nhánh đó khi tinh chỉnh), vì ở N2 nhánh `pair` cũng bị quét huấn luyện trên 20 cặp bị ràng buộc với WT. Biến thể này **chưa chạy**: PROTOCOL §7 cấm thêm arm sau khi thấy kết quả, nên nó cần PROTOCOL mới. `[ĐỀ XUẤT]`

## 4. Thăm dò: bộ quét làm tập chấm điểm `[ĐO, thăm dò]`

[sat_to_scan_eval.py](sat_to_scan_eval.py) → [results-sat-to-scan.json](results-sat-to-scan.json). **Không tiền đăng ký; không chọn gì dựa trên số này.** Học ridge trên toàn bộ 176 peptide bão hòa ext4.0, chấm trên peptide quét có cụm cov80 **không thuộc bất kỳ cụm bão hòa nào**.

| Peptide quét (cụm rời) | Mô hình | AUROC mức ô, macro | CI95 theo cụm |
|---|---|---:|---|
| PSI WT ≤ 3,0 · 2.107 peptide đủ hai lớp · 1.514 cụm | M3 học trên bão hòa | **0,8216** | [0,8132; 0,8292] |
| | M0 (chỉ thành phần) học trên bão hòa | 0,8046 | [0,7967; 0,8119] |
| | M3 học **trên chính bộ quét** (CV theo cụm) | 0,8705 | [0,8620; 0,8783] |
| PSI WT ≤ 4,0 · 3.124 peptide · 2.103 cụm | M3 học trên bão hòa | 0,8317 | [0,8250; 0,8381] |
| | M3 − M0 (ghép cặp) | +0,0143 | [+0,0114; +0,0171] |

`[DIỄN GIẢI]` Mô hình học từ 176 peptide đạt ~0,82–0,83 trên hàng nghìn peptide chưa thấy ở cụm rời — **cùng bậc** với OOF trong bộ bão hòa (0,8208), và phần thêm của ngữ cảnh ±3 (M3 − M0 ≈ +0,014 đến +0,017) **tái xuất hiện** ở một thiết kế thay thế khác. Với 1.500–2.100 cụm, MDE theo [derisk](../residue-task-derisk-2026-10-15/README.md) cỡ 0,003 thay vì 0,0123, nên đây là chỗ bộ quét có giá trị lớn nhất.

Giới hạn, nói thẳng: (i) cùng phòng thí nghiệm, cùng hệ GPS, cùng pipeline, **không** phải kiểm chứng độc lập; (ii) chỉ kiểm 20 cặp R/A/S, không kiểm ma trận thay thế; (iii) nhãn một replicate với mốc WT đo trực tiếp, nhiễu hơn; (iv) khoảng cách 0,8216 → 0,8705 so với học trong miền quét gộp chênh lệch thiết kế thay thế và chênh lệch assay, không tách được ở đây. Nếu dùng làm tập chấm chính thức thì phải **tiền đăng ký** và tuyệt đối không chỉnh siêu tham số trên nó.

## 5. Đối chiếu với nhận định đã dán

| Điểm trong nhận định | Kiểm |
|---|---|
| 91 peptide gốc, 176 ở ngưỡng 4,0; 47.847 ô; chia theo cụm | **Đúng** ([ladder.json](../residue-task-derisk-2026-10-15/ladder.json): 91/89/47.847; 176/172/92.337) |
| 248 peptide thô, 235 qua bước kỹ thuật | **Đúng** ([sat-filter-dropoff.json](../next-steps-plan-2026-10-22/sat-filter-dropoff.json); ladder `psi_wt_max: null` → 235) |
| Quy tắc pipeline (reads ≥ 10; ≥ 10 ô đồng nghĩa mỗi nửa; hai nửa; 3,0/4,0) | **Đúng** với [residue_data.py](../residue-task-derisk-2026-10-15/residue_data.py) `build_saturation` |
| Cần chuỗi + WT/mutant + ΔPSI; nhãn nhị phân suy từ nhãn liên tục | **Đúng**; chỉ lưu ý nhãn bão hòa dùng WT **nội tại**, nhãn quét dùng `mut0` — hai định nghĩa khác nhau (mục 2) |
| Scanning: 2.994 peptide / 83.446 ô / 1.985 cụm | **Đúng**; ngưỡng 4,0 cho 4.809 / 133.960 / 2.909 |
| "Mỗi vị trí thường chỉ có một phép thay" | **Đúng nhưng chưa đủ**: là một phép thay **tất định theo WT**, R/A/S, 20/380 cặp |
| "**Đáng ưu tiên nhất** để tăng chuỗi nền có nhãn đột biến" | **Không được ủng hộ** cho mục đích huấn luyện (mục 3). Được ủng hộ cho mục đích **chấm điểm** (mục 4) |
| Ba chế độ: chỉ bão hòa / quét rồi tinh chỉnh / học kết hợp có nhận diện nguồn | **Đã chạy đủ** ở dạng ridge (A1, S3, S2) và mạng nhỏ (N1, N2) |
| Loại peptide quét chạm cụm outer-test | **Đã làm**, thêm cả cụm validation (rò rỉ chọn siêu tham số) |
| "Repo từng thử ridge scanning → saturation, kém hơn học trực tiếp" | **Đúng** (0,7273 ở G2; S0 = 0,7277 ở đây) — nhưng đó là chuyển miền thuần, chưa phải trộn; trộn nay đã đo |
| Peptidome WT "học biểu diễn hoặc tác vụ phụ" | **Đã thử và âm**: [P3](../pretrain-p3-2026-10-22/README.md) `pre − rand` = −0,0077, CI [−0,016; +0,001]. Thêm: thang PSI sàng lệch ≈ 0,88 so với bão hòa ([R3](../r3-domain-gate-2026-10-22/README.md)) |
| Koren S4: 9 substrate, 5 cụm mới, không qua cổng | **Đúng** ([audit](../koren-s4-audit-2026-10-22/README.md)); lưu ý thêm: bản NIHMS không có giấy phép mở |
| "219 degron" chưa thể cộng thêm 219 | **Đúng, và có thể nói chắc hơn**: 219 là tập tác giả **curate** từ chính thư viện bão hòa; dữ liệu thô đã tải đỡ **239–247** peptide ([e3-labels-audit §4.3](../e3-labels-audit/README.md)). `[CHƯA XÁC MINH]` bằng ID: trang PMC của Zhang chặn đọc tự động (reCAPTCHA), nên danh sách 219 chưa được đối chiếu |
| Shimshon 2024 "có saturation mutagenesis… cần mở bảng" | Đọc PMC11178506 ngày 23/10 `[ĐO lượt đọc]`: saturation chỉ ở **vị trí 2–10 của N24mer** (9 vị trí × 19 = **171** biến thể/peptide, số tính, bài không nêu), trên "selected substrates" (số lượng **không có trong văn bản**), dữ liệu ở supplementary Table S1, **không có accession GEO/SRA**. Cùng readout PSI 6 bin, nhưng là N-degron, cửa sổ 9 vị trí: không gộp được với 28-mer nội vùng |
| Lấy thêm UniProt / sinh mutant / ESM không tạo nhãn thật | **Đúng** |

## 6. Hướng còn lại, xếp theo bằng chứng

| # | Hướng | Căn cứ | Việc |
|---|---|---|---|
| 1 | **Bộ quét làm tập chấm cụm rời** | Mục 4: 1.500–2.100 cụm, M3 − M0 tái xuất hiện | `[ĐỀ XUẤT]` Viết PROTOCOL: chọn trước mô hình/siêu tham số chỉ trên bão hòa, chấm một lần trên quét cụm rời, báo theo cụm. Kèm cảnh báo "cùng phòng thí nghiệm" |
| 2 | **Hỏi nhóm Zhang/Elledge** | Ba câu cụ thể có thể trả lời bằng email: (a) danh sách ID 219 footprint; (b) thư viện quét có biến thể nào ngoài R/A/S không; (c) thư mục đặt tên *"Replicate 1 (BAG6 genotype unclear)"* — điều kiện tế bào nào, và nó có cùng dòng tế bào với bão hòa không | `[ĐỀ XUẤT]` Mục (c) ảnh hưởng trực tiếp mục 2 ở trên |
| 3 | Nhãn T1 ngoài (Timms 2023; preprint "genetic glues" 09/2026; Shimshon 2024) | [dataset-search](../next-steps-plan-2026-10-22/dataset-search.md); Shimshon đã đọc ở mục 5 | Chỉ như nhánh riêng/kiểm chứng; kiểm giấy phép trước; **không** gộp N-degron vào miền 28-mer |
| 4 | Thêm cụm bão hòa bằng **thực nghiệm** | Mạng còn dốc theo số cụm ([P1](../learning-curve-2026-10-22/README.md)), ridge thì phẳng | Chỉ đáng khi có hợp tác ướt-lab; trước đó nên vẽ đường cong học của mạng **vượt** 172 cụm để biết lợi ích kỳ vọng |
| 5 | Nới ngưỡng thêm / tiền huấn luyện tile / trộn quét vào huấn luyện | P0 đỉnh ở 4,0; P3 âm; mục 3 null | Không đáng làm tiếp ở thiết kế hiện tại |

## 7. Những gì phiên này **không** làm / chưa biết

- **Không** thử PLM (R2 chưa chạy), mCNN, hay mạng lớn. Kết luận "quét không giúp" áp cho **ridge M3 và `Gate` 64→32→1**; mô hình có sức chứa lớn hơn hoặc biểu diễn ESM-2 là câu hỏi mở, và khả năng chúng hưởng lợi từ 2.900 cụm quét **không bị phép đo này loại trừ**.
- **Không** giảm nhiễu nhãn quét (trung bình rep1+rep2) và không tận dụng 3.228 ô đo hai lần để ước lượng nhiễu nhãn từng nguồn. Hợp lý nhưng chưa làm; cần PROTOCOL riêng.
- Toàn bộ vẫn là benchmark **phát triển** OOF trên dữ liệu từng được khảo sát, không phải kiểm chứng ngoài.
- Một phiên song song đã tạo [r6-ladder-scan-2026-10-23](../r6-ladder-scan-2026-10-23/README.md), chưa chạy, có hai arm trộn bộ quét (B ridge, G mạng mCNN/ESM). Phép đo ở đây đã trả lời arm B cho ridge (null), nên arm đó có thể bỏ khỏi ngân sách Kaggle; arm G vẫn mở. Tôi không sửa các file của R6. Lưu ý: R6 README mục 1 viết nhãn quét "cùng tín hiệu, không cùng thang (độ dốc OLS 0,70–0,77)"; theo mục 2 ở đây độ dốc đó chỉ là r · SD_y/SD_x, không phải lệch thang.
- Một mô tả cũ trong repo (bộ quét "gần như toàn bộ →R") không đúng chính xác như mục 1; các README lịch sử **không bị sửa**, theo quy ước repo.

## 8. Tái lập

```bash
cd /home/ngthtrong/CT553H
.venv/bin/python -I topics/degron-footprint/research/scan-sat-merge-2026-10-23/audit_labels.py        # ~6 s
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/scan-sat-merge-2026-10-23/run_merge.py   # ~7 phút, thêm --no-neural để chỉ chạy ridge (~3 phút)
.venv/bin/python -I topics/degron-footprint/research/scan-sat-merge-2026-10-23/sat_to_scan_eval.py   # ~9 phút (bootstrap)
```

Cổng tự kiểm trong `run_merge.py`: folds trùng G2; A1 = 0,8208 và A0 = 0,8082 tái lập; bộ giải thống kê đủ khớp `sklearn.Ridge`. Cần cache `data/processed/learning-curve-sat-{base,ext4.0}.npz` (runner của learning-curve tự dựng). Seed 17/29/43, bootstrap 5.000 lần theo cụm.
