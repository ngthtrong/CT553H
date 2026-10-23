# Đường cong học theo cụm (P1) và nới ngưỡng degron (P0) — 22/10/2026

Tiêu chí chốt **trước khi chạy** ở [PROTOCOL.md](PROTOCOL.md) (phần A), [PROTOCOL-B.md](PROTOCOL-B.md) (phần B) và [PROTOCOL-C.md](PROTOCOL-C.md) (phần C) — mỗi phần chốt trước khi chạy phần đó. Các phần sau **không** sửa tiêu chí hay kết luận của phần trước. Kết quả đầy đủ: [results.json](results.json), [results-b.json](results-b.json), [results-c.json](results-c.json). Không đổi trạng thái G2/G3, không sửa đề cương hay slide.

**[ĐO] Kết quả một dòng.** Hai câu trả lời đi ngược nhau, và cả hai đều có ích. **P1:** với ridge, đường cong học **đã phẳng** từ ~35 cụm — *không* đủ bằng chứng cho giả thuyết thiếu nhãn; với mạng `gate_no_pap` sức chứa lớn hơn thì đường cong **vẫn đang lên**, đạt tiêu chí hỗ trợ. **P0:** nới ngưỡng degron lên 4,0 **đạt cả hai tiêu chí ở cả hai mô hình** — ridge lên **0,8208** trên *đúng những ô test* của benchmark G2, tức **+0,0126** so với mốc 0,8082.

**[ĐO] Phần B** tách tiếp hai cách giải thích lợi ích của P0 và **chưa phân định dứt khoát**: tiêu chí chính ủng hộ "mở rộng phân bố" ở ridge nhưng không ở mạng, còn tiêu chí hình dạng đường cong thì không đạt ở cả hai (§4b).

**[ĐO] Phần C** chạy cả bốn ngưỡng 3,5/4,0/4,5/5,0 trong một lượt: lợi ích **đạt đỉnh đúng ở 4,0** rồi suy giảm, và lợi ích ở 4,0 **bền** qua cả ba `RESCUE_DELTA` và qua phép chia lại fold (§4c). Ngưỡng 4,0 đã được chốt trước ở phần A, **trước khi** thấy lưới này.

**[DIỄN GIẢI]** Cách đọc thận trọng nhất mà số liệu chịu được: ngưỡng `PSI(WT) ≤ 3,0` đã **kiểm duyệt tập huấn luyện** về một vùng hẹp, và cụm thuộc vùng bị cắt có giá trị biên **ít nhất là bằng, có dấu hiệu cao hơn** cụm thuộc vùng cũ. Đây là lần đầu tiên từ sau G2 có một thay đổi vượt 0,8082 theo tiêu chí chốt trước.

## 1. Cổng tự kiểm đã qua

- `[ĐO]` 5 outer fold tính lại bằng `GroupKFold(5)` trên bộ 91 peptide **trùng khớp từng cụm** với `folds` trong [results.json của G2](../g2-saturation-2026-10-18/results.json). Runner `assert` điều kiện này và dừng nếu lệch (PROTOCOL §3).
- `[ĐO]` Ở mức 100%, ridge cho **0,8082** và `gate_no_pap` cho **0,8015** — **đúng** hai con số headline của G2. Hai mô hình tái lập chính xác mốc cũ nên mọi phép so trong bảng dưới là so trên cùng ô test, cùng nhãn, cùng chỉ số.
- `[ĐO]` Peptide nới ngưỡng bị loại khỏi train vì trùng cụm test: fold 0 là 531 ô, fold 3 là 532 ô, ba fold còn lại 0. Tức **83/85** peptide mới nằm trong cụm cov80 thật sự mới.

## 2. P1 — đường cong học `[ĐO]`

AUROC mức ô, macro theo peptide, điểm OOF gộp ba seed. Cột "cụm train" là khoảng qua 5 fold × 3 seed.

| Mức | Cụm train | Ô train | **ridge M3** | **gate_no_pap** |
|---|---:|---:|---:|---:|
| 25% | 18 | 9.068–10.314 | 0,7776 | 0,7529 |
| 50% | 35–36 | 18.635–19.877 | 0,8044 | 0,7859 |
| 75% | 52–54 | 28.145–29.048 | 0,8088 | 0,7949 |
| 100% | 70–72 | 38.233–38.290 | **0,8082** | **0,8015** |
| **+ nới ngưỡng (P0)** | 153–155 | 82.191–82.780 | **0,8208** | **0,8154** |

| Mô hình | A(100%) − A(50%) | CI 95% theo cụm | Đơn điệu? | Kết luận theo PROTOCOL §5 |
|---|---:|---|:--:|---|
| ridge M3 | +0,0038 | **[−0,0009; +0,0087]** | Không (0,8088 > 0,8082) | **Chưa đủ bằng chứng cho giả thuyết thiếu nhãn** |
| gate_no_pap | +0,0156 | **[+0,0060; +0,0256]** | Có | **Hỗ trợ** |

**[DIỄN GIẢI] Hai đường cong khác nhau nói lên điều mà một đường cong không nói được.** Đây đúng là lý do PROTOCOL §4 chốt trước hai mô hình khác sức chứa. Ridge chạm tiệm cận của **chính nó** ở khoảng 35–53 cụm: thêm nhãn trong cùng vùng phân bố không giúp nó nữa. Mạng thì vẫn đang leo ở 71 cụm. Vậy phát biểu đúng không phải "đề tài thiếu nhãn" hay "đề tài đủ nhãn", mà là: **ridge thắng ở n = 89 cụm vì ở đó mạng còn chưa tới tiệm cận của mình**, chứ không vì tương tác thay thế × ngữ cảnh không tồn tại.

**[DIỄN GIẢI]** Điều này **không** phục hồi bất kỳ ứng viên nào trong năm thiết kế đã bị loại ở [G2 mở rộng](../g2-extension-2026-10-18/README.md). Khoảng cách ridge − mạng là +0,0067 ở mức 100% và vẫn +0,0054 ở mức nới ngưỡng; mạng **thu hẹp** chứ chưa vượt. Không được đọc kết quả này thành "thêm nhãn thì kiến trúc sẽ thắng" — đó là ngoại suy, và PROTOCOL §5 không cho phép.

## 3. P0 — nới ngưỡng degron `[ĐO]`

Thêm 85 peptide (44.490 ô, 83 cụm cov80 mới) vào **chỉ outer-train**; outer-test giữ nguyên miền 91 peptide.

| Mô hình | A(ext) − A(100%) | CI 95% theo cụm | Delta từng seed | Tiêu chí (a) CI > 0 | (b) ba seed dương | Kết luận |
|---|---:|---|---|:--:|:--:|---|
| ridge M3 | **+0,0126** | **[+0,0061; +0,0190]** | +0,0142 · +0,0142 · +0,0128 | Đạt | Đạt | **Nhận** |
| gate_no_pap | **+0,0139** | **[+0,0059; +0,0218]** | +0,0184 · +0,0311 · +0,0227 | Đạt | Đạt | **Nhận** |

### Dự đoán tiền đăng ký số 2 đã **sai**, và cách nó sai là phần đáng giá nhất

`[ĐO]` PROTOCOL §6.2 dự đoán P0 sẽ thất bại vì nhóm peptide mới có PSI(WT) cao nên "ô dương = ΔPSI ≥ 1" gần như không còn chỗ xảy ra. Số đo bác dự đoán đó:

| | Nhóm 91 peptide gốc | Nhóm 85 peptide mới |
|---|---:|---:|
| PSI(WT) trung vị | 2,593 | 3,346 (khoảng 3,002–3,980) |
| Tỉ lệ ô dương (ΔPSI ≥ 1) | 0,1310 | **0,1140** |
| ΔPSI trung vị | 0,125 | 0,083 |
| ΔPSI phân vị 95 | 1,697 | 1,507 |

`[DIỄN GIẢI]` Tỉ lệ ô dương chỉ giảm từ 13,1% xuống 11,4%, **không** sụp về gần 0 như đã lo. Nghĩa là peptide có PSI(WT) trong khoảng 3,0–4,0 vẫn là degron hoạt động theo thang đo: chúng vẫn còn chỗ để một phép thay làm reporter bền thêm. Ngưỡng 3,0 vì thế là một đường cắt **bảo thủ hơn mức cần thiết** đối với bài toán hiệu ứng đột biến, dù nó có thể vẫn đúng cho bài toán "peptide này có phải degron" mà nó được đặt ra để phục vụ.

## 4. Hai kết quả của phần A ghép lại `[DIỄN GIẢI]`

Ridge phẳng trong khoảng 35 → 71 cụm (+0,0038, CI phủ 0) nhưng tăng rõ khi đi 71 → 154 cụm (+0,0126, CI dương). Thoạt nhìn là nghịch lý: lợi ích giảm dần rồi lại tăng. Cách đọc nhất quán: **hai đoạn đó không thêm cùng một thứ.**

- Đoạn 25% → 100% lấy thêm cụm **từ chính vùng PSI(WT) ≤ 3,0**. Nó làm dày một phân bố, và ridge đã hút hết thông tin của phân bố đó.
- Đoạn nới ngưỡng thêm cụm **từ vùng PSI(WT) 3,0–4,0** chưa từng có trong train. Nó **mở rộng miền đầu vào**, không làm dày miền cũ.

Phần A **không** tách được hai yếu tố, vì mức nới ngưỡng tăng đồng thời số cụm (71 → 154) và độ phủ phân bố. Phần B được tiền đăng ký riêng để tách.

## 4b. Phần B — tách "thêm cụm" khỏi "mở rộng phân bố" `[ĐO]`

Thiết kế: phần cũ **giữ nguyên 100%** ở mọi mức; chỉ thay tỉ lệ cụm **mới** thêm vào train (lồng nhau, 85 cụm khả dụng). B(0) là mức 100% của phần A, **đọc lại** từ `results.json`, không chạy lại.

| Mức | Cụm mới thêm (trung bình) | **ridge M3** | Lợi ích so B(0) | **gate_no_pap** | Lợi ích so B(0) |
|---|---:|---:|---:|---:|---:|
| B(0) — không thêm | 0 | 0,8082 | — | 0,8015 | — |
| +25% cụm mới | ~21 | 0,8143 | +0,0061 | 0,8090 | +0,0075 |
| +50% cụm mới | ~42 | 0,8196 | +0,0114 | 0,8118 | +0,0103 |
| +75% cụm mới | ~63 | 0,8204 | +0,0122 | 0,8168 | +0,0153 |
| +100% cụm mới | ~84 | 0,8208 | +0,0126 | 0,8154 | +0,0139 |

**Tiêu chí chính** (PROTOCOL-B §4): so B(50%) − B(0) với **+0,0038**, là giá trị biên đo được của 36 cụm **vùng cũ** ở phần A.

| Mô hình | B(50%) − B(0) | CI 95% theo cụm | So mốc +0,0038 | Kết luận chốt trước |
|---|---:|---|---|---|
| ridge M3 | +0,0114 | **[+0,0063; +0,0166]** | CI **nằm trọn trên** mốc | **Ủng hộ mở rộng phân bố** |
| gate_no_pap | +0,0103 | [+0,0033; +0,0172] | CI **chứa** mốc | **Có giá trị, nhưng chưa hơn cụm vùng cũ** |

**Tiêu chí hình dạng** (PROTOCOL-B §4): lợi ích tại 25% chiếm **48,4%** tổng lợi ích ở ridge và **54,4%** ở mạng — cả hai **dưới** ngưỡng 60% đã chốt, nên theo đúng tiêu chí này phải ghi là **"tỉ lệ theo số cụm"**, tức ủng hộ cách đọc số lượng.

**[ĐO] Hai tiêu chí cho kết luận khác nhau, nên theo PROTOCOL-B §4 ghi là chưa phân định; không chọn cái thuận lợi.**

**[DIỄN GIẢI] Nhưng ngưỡng 60% ở mốc 25% là một phép thao tác hóa thô, và nó đặt sai chỗ.** Mô tả đường cong cho thấy lợi ích **có bão hòa**, chỉ là muộn hơn mốc mà tiêu chí giả định: ở ridge, các mức tăng liên tiếp là **+0,0061 → +0,0053 → +0,0008 → +0,0004**, tức **90% tổng lợi ích đã đạt ở 50% cụm mới** (~42 cụm) và hai mức cuối gần như không thêm gì. Đây là phần mô tả, **không** phải tiêu chí chốt trước, và nó không được dùng để lật kết luận "chưa phân định".

**[DIỄN GIẢI] Quan sát mô tả đáng ghi riêng:** ở ridge, **~21 cụm vùng mới** mua được **+0,0061**, trong khi **36 cụm vùng cũ** chỉ mua được **+0,0038** (phần A). Ít cụm hơn, lợi ích lớn hơn. Không có phép kiểm CI nào được tiền đăng ký cho mức 25%, nên đây là dấu hiệu chứ không phải kết luận.

**[DIỄN GIẢI] Tổng hợp trung thực:** ba chỉ dấu — CI của ridge vượt mốc, bão hòa ở ~42 cụm, và quan sát 21-cụm-mới-hơn-36-cụm-cũ — đều nghiêng về **độ phủ phân bố**. Chỉ dấu ngược lại là CI của mạng chứa mốc và tiêu chí hình dạng đã chốt không đạt. Phát biểu dùng được: *cụm thuộc vùng PSI(WT) 3,0–4,0 có giá trị biên **ít nhất bằng** cụm vùng cũ, và ở ridge có bằng chứng là **cao hơn***. Phát biểu **không** dùng được: "lợi ích hoàn toàn do mở rộng phân bố, không do số cụm".

## 4c. Phần C — độ nhạy ngưỡng, `RESCUE_DELTA` và phép chia lại `[ĐO]`

Cả bốn ngưỡng chạy **một lượt** và báo đầy đủ, theo PROTOCOL-C §1. Cấu hình chính của đề tài **vẫn là 4,0** theo phần A; lưới này là phân tích độ nhạy và **không** được dùng để chọn cấu hình.

### Dữ liệu thêm theo từng ngưỡng

| Ngưỡng | Peptide thêm | Ô thêm | Cụm cov80 mới | Tỉ lệ ô dương (ΔPSI ≥ 1) | PSI(WT) trung vị |
|---:|---:|---:|---:|---:|---:|
| *base 3,0* | — | — | — | *0,1310* | *2,593* |
| 3,5 | +50 | 26.234 | 48 | 0,1197 | — |
| **4,0** | **+85** | **44.490** | **83** | **0,1140** | **3,346** |
| 4,5 | +106 | 55.362 | 102 | 0,1028 | — |
| 5,0 | +121 | 63.009 | 117 | 0,0918 | — |

`[DIỄN GIẢI]` Tỉ lệ ô dương **giảm đơn điệu** theo ngưỡng. Đây là cơ chế nhìn thấy được của hiện tượng ở bảng dưới: càng nới, càng thêm peptide thực sự **không phải degron**, mà ô của chúng mang ít tín hiệu "phép thay làm reporter bền thêm" nên bắt đầu làm loãng tập huấn luyện.

### C1 — hình dạng quan hệ ngưỡng–lợi ích (ridge, cov80, `RESCUE_DELTA` = 1,0)

| Ngưỡng | AUROC | Δ so với base | CI 95% theo cụm | Ba seed |
|---:|---:|---:|---|---|
| *base* | *0,8082* | — | — | — |
| 3,5 | 0,8185 | +0,0103 | [+0,0043; +0,0164] | đều dương |
| **4,0** | **0,8208** | **+0,0126** | **[+0,0061; +0,0190]** | đều dương |
| 4,5 | 0,8183 | +0,0101 | [+0,0028; +0,0172] | đều dương |
| 5,0 | 0,8175 | +0,0093 | [+0,0016; +0,0169] | đều dương |

**Kết luận chốt trước: "suy giảm sau 4,0"** — đỉnh ở 4,0, và hai ngưỡng cao hơn thấp hơn đỉnh quá dung sai 0,002 đã chốt. Cả bốn CI đều > 0, nên **mọi** ngưỡng vẫn tốt hơn base.

**[ĐO] Ngưỡng 4,0 được chốt ở phần A trước khi lưới này được chạy, và nó trùng với đỉnh.** Đây là một sự trùng hợp may mắn, **không** phải bằng chứng rằng cách chọn ban đầu là đúng phương pháp — lúc đó 4,0 được chọn chỉ vì nó thêm khoảng gấp đôi số peptide. Theo PROTOCOL-C §1.2, cấu hình chính **không** được chọn lại từ bảng này.

**[DIỄN GIẢI] Giới hạn của chính phép kết luận C1:** hình dạng được phán theo **điểm ước lượng cộng dung sai 0,002 đã chốt trước**, *không* theo một CI cho hiệu-của-hiệu Δ(4,0) − Δ(4,5). Các CI của bốn ngưỡng chồng nhau rất nhiều, nên "suy giảm sau 4,0" là phát biểu về hình dạng ước lượng, **chưa** phải một phép kiểm có ý nghĩa thống kê về việc 4,0 hơn 4,5.

### C2 — độ bền của ngưỡng 4,0

| Điều kiện | Δ(4,0) | CI 95% | Đạt CI > 0 |
|---|---:|---|:--:|
| cov80, `RESCUE_DELTA` = 0,5 | +0,0110 | [+0,0051; +0,0169] | Đạt |
| cov80, `RESCUE_DELTA` = 1,0 *(chính)* | +0,0126 | [+0,0061; +0,0190] | Đạt |
| cov80, `RESCUE_DELTA` = 1,5 | +0,0094 | [+0,0037; +0,0149] | Đạt |
| cov50, `RESCUE_DELTA` = 1,0 | +0,0096 | [+0,0032; +0,0159] | Đạt |

**Kết luận chốt trước: "bền"** — cả bốn điều kiện đều có CI > 0.

**[ĐO] Nhưng điều kiện cov50 không kiểm được thứ nó định kiểm, và phải nói rõ.** Kiểm lại sau khi chạy: trên bộ 91 peptide, phân cụm cov50 và cov80 cho **đúng cùng một phân hoạch** (89 cụm, cấu trúc nhóm trùng khít); 23 peptide chỉ đổi *nhãn đại diện* chứ không đổi nhóm. Trên hợp base + 85 peptide của ngưỡng 4,0 cũng vậy: **172 cụm, phân hoạch trùng khít**. Chỉ ở ngưỡng 5,0 cov50 mới gộp thêm một cặp (206 → 205 cụm).

`[DIỄN GIẢI]` Vì vậy dòng "cov50" ở bảng trên **không** phải phép kiểm độ nhạy theo độ mịn phân cụm; nó là phép kiểm **chia lại fold**: vì `GroupKFold` xếp cụm theo nhãn, 23 nhãn đổi làm 5 fold được gán khác đi (base AUROC 0,8116 thay vì 0,8082). Lợi ích +0,0096 sống qua một phép gán fold khác là kết quả có ích, nhưng nó **không** trả lời được câu "lợi ích có bền khi phân cụm thô hơn không". Câu đó **không trả lời được trên bộ peptide này**, vì ở đây cov50 và cov80 không khác nhau.

### C3 — hai mô hình

| Ngưỡng | ridge Δ | `gate_no_pap` Δ |
|---:|---:|---:|
| 3,5 | +0,0103 | +0,0115 |
| **4,0** | **+0,0126** | **+0,0139** |
| 4,5 | +0,0101 | +0,0125 |
| 5,0 | +0,0093 | +0,0133 |

**Kết luận chốt trước: "hai mô hình đồng thuận về hình dạng"** — cùng dấu ở mọi ngưỡng, cùng đỉnh ở 4,0.

**[DIỄN GIẢI] Mức đồng thuận này mỏng hơn tên gọi của nó.** Tiêu chí chỉ đòi trùng dấu và trùng đỉnh. Thực tế đường của mạng gần như **phẳng** từ 3,5 đến 5,0 (+0,0115 … +0,0139 … +0,0133), không có suy giảm rõ. Vậy "suy giảm sau 4,0" là hiện tượng của **ridge**, không phải của cả hai mô hình.

**[ĐO] Hình dạng cũng đổi theo `RESCUE_DELTA`.** Ở `RESCUE_DELTA` = 1,5, Δ của ridge là +0,0061 / +0,0094 / +0,0094 / **+0,0098** — đỉnh chuyển sang 5,0 và không còn suy giảm. Tức "suy giảm sau 4,0" chỉ xuất hiện khi định nghĩa ô dương **lỏng hơn hoặc bằng** ΔPSI ≥ 1. `[DIỄN GIẢI]` Hợp với cơ chế ở trên: nhóm peptide thêm ở ngưỡng cao có ít ô vượt 1,0, nhưng những ô vượt thì vẫn vượt xa, nên chúng đóng góp tốt hơn khi ngưỡng đánh giá khắt khe.

## 5. Giới hạn

- `[ĐO]` Benchmark **phát triển OOF** trên dữ liệu đã được khảo sát nhiều lần, **không** phải kiểm chứng ngoài độc lập. Con số 0,8208 không được trình bày như kết quả xác nhận cuối cùng.
- `[ĐO]` Bốn ngưỡng 3,5/4,0/4,5/5,0 đã chạy **một lượt và báo đầy đủ** ở phần C; không có ngưỡng nào bị bỏ khỏi báo cáo sau khi thấy số, và cấu hình chính không được chọn lại từ lưới đó.
- `[ĐO]` Chỉ hai mô hình chốt trước. Không thử kiến trúc mới; năm kết quả âm của G2 mở rộng **vẫn nguyên giá trị**.
- `[ĐO]` Không tính lại ΔPAP cho peptide mới; mốc 0,7693 chỉ được dẫn lại từ G2 trên bộ 91 peptide, không tính lại trong phiên này.
- `[ĐO]` Lợi ích ở ngưỡng 4,0 đã kiểm qua ba `RESCUE_DELTA` và một phép gán fold khác, đều giữ CI > 0 (§4c C2).
- `[ĐO]` **Độ nhạy theo độ mịn phân cụm vẫn chưa kiểm được**, vì cov50 và cov80 cho cùng phân hoạch trên bộ peptide này (§4c C2). Muốn kiểm thật thì phải phân cụm lại ở ngưỡng đồng nhất/độ phủ khác, hoặc dùng bộ peptide rộng hơn.
- `[ĐO]` Phần B tách được giá trị biên theo **vùng phân bố**, nhưng vẫn **không** tách được "vùng PSI(WT) khác" khỏi "protein khác": 83 cụm mới vừa ở vùng PSI(WT) cao hơn vừa là protein khác. Phép tách đó cần cặp peptide cùng protein ở hai vùng ngưỡng, và bộ dữ liệu hiện có **chưa chắc đủ** cho thiết kế đó.
- `[DIỄN GIẢI]` Nhóm 85 peptide mới đi qua đúng pipeline nhãn cũ, nên kế thừa mọi giả định của nó (mốc WT từ ô đồng nghĩa, trung bình hai nửa replicate).

## 6. Hướng chỉnh sửa tài liệu — **đề xuất, chưa thực hiện**

`[ĐỀ XUẤT]` Không sửa file nào trong phiên này. Khi bạn duyệt:

1. **`research/next-steps-plan-2026-10-22/README.md`** — P0 và P1 đã chạy, cần cập nhật trạng thái: P0 **nhận**, P1 **hỗ trợ một nửa** (tùy mô hình). Quan trọng hơn: §1 của kế hoạch hiện viết nút thắt là "lượng và độ đa dạng của nhãn"; nên sửa thành **độ phủ phân bố nhãn**, kèm đúng mức dè dặt mà phần B cho phép (§4b: chưa phân định dứt khoát), và ghi rằng đường cong phẳng của ridge là bằng chứng *chống lại* cách đọc thuần "lượng". P5 trong kế hoạch (lặp P1 trên tập mở rộng) **đã được phần B thực hiện một phần** nên nên viết lại thành việc còn thiếu: tách "vùng PSI(WT)" khỏi "protein khác" (§5).
2. **`research/next-steps-plan-2026-10-22/dataset-search.md`** — §0 nên dẫn kết quả thật thay cho dự tính: 85 peptide đã nhập và cho +0,0126. Đồng thời **hạ mức ưu tiên của P2 (nguồn ngoài) một bậc**: đường cong ridge phẳng cho thấy thêm nhãn *cùng vùng phân bố* ít tác dụng, nên giá trị của Koren 2018 Table S4 nằm ở chỗ nó là **lớp degron khác** (đầu C) — tức mở rộng phân bố — chứ không ở số ô nó thêm. Lập luận ủng hộ P2 vẫn còn, nhưng lý do đã khác.
3. **Đề cương `proposal/proposal.md`** — `[ĐỀ XUẤT]` chỉ nêu, **không** sửa theo yêu cầu của bạn. Hai chỗ nay đã lệch với số đo: (a) §I.3 ghi phạm vi "bộ bão hòa sau lọc hiện có 91 peptide, 89 cụm, 47.847 ô" — nếu nhận cấu hình nới ngưỡng thì con số huấn luyện thành 176 peptide, và cần nói rõ miền đánh giá vẫn là 91; (b) §III.1 ghi "khảo sát đường cong học để kiểm giả thuyết thiếu nhãn" như việc **sắp làm** — nay đã làm, và kết quả không đơn giản như giả thuyết. Đề nghị: chờ đủ phép tách ở §4 rồi sửa một lần, thay vì sửa hai lần.
4. **Không** đổi trạng thái G2. P0 cải thiện số liệu trên benchmark phát triển; nó **không** giải quyết điều kiện "thành phần kiến trúc có lợi ổn định" hay "đối chứng Degformer sạch cụm", nên G2 vẫn chưa hoàn tất.

`[ĐO]` Ba việc được nêu ở phiên trước đã làm xong trong phần C: độ nhạy ngưỡng (báo toàn bộ cùng lúc), `RESCUE_DELTA`, và cov50 — trong đó cov50 hóa ra không kiểm được điều cần kiểm (§4c C2).

`[ĐỀ XUẤT]` Việc nghiên cứu tiếp theo, theo thứ tự:

1. **Nguồn ngoài P2 — bước quyền/truy cập đã chạy cuối phiên này và cho kết quả âm về mặt thao tác.** `[ĐO]` Koren 2018 Table S4: trang PMC đọc được nhưng file `.xlsx` **không tải được** (trang chờ đòi bắt tay cookie bằng JavaScript, không thực hiện), và `oa.fcgi` 404 nghĩa là nguồn **không có giấy phép mở** — chi tiết ở [dataset-search §2b](../next-steps-plan-2026-10-22/dataset-search.md) và [SOURCE.md](../../data/raw/koren-2018-probe/SOURCE.md). Việc còn lại là **việc tay của người**: tải bằng trình duyệt thật, hoặc dùng quyền ScienceDirect của ĐHCT, hoặc hỏi tác giả. Lý do vẫn cần nguồn này đã sửa theo phần C: giá trị của nó là **lớp degron khác** (đầu C), tức mở rộng phân bố, chứ không phải số ô — vì phần C cho thấy mở rộng phân bố *trong cùng thư viện Zhang* đã hết lợi ích quanh ngưỡng 4,0.
2. **Phân cụm lại** ở ngưỡng đồng nhất hoặc độ phủ khác để có một phép kiểm độ mịn phân cụm thật (§4c C2 nêu vì sao cov50 không đủ). Rẻ, cần MMseqs2.
3. **Tách "vùng PSI(WT)" khỏi "protein khác"** (§5), nếu tìm được cặp peptide cùng protein ở hai vùng ngưỡng.

## 7. Dựng lại

```bash
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  topics/degron-footprint/research/learning-curve-2026-10-22/run_curve.py      # phần A
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  topics/degron-footprint/research/learning-curve-2026-10-22/run_curve_b.py    # phần B
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  topics/degron-footprint/research/learning-curve-2026-10-22/run_sensitivity.py # phần C
```

Phần A và B khoảng 10 phút CPU mỗi phần, phần C khoảng 25 phút, trong môi trường phiên này. Phần B và C `import run_curve` để dùng lại đúng hàm `build`/`ridge`/`neural`/`compare` của phần A; phần B còn **đọc lại** `results.json` để lấy B(0) thay vì chạy lại, nên phải chạy phần A trước. Phần C tự dựng thêm ba cache `learning-curve-sat-ext{3.5,4.5,5.0}.npz`. Runner tự dựng hai cache `data/processed/learning-curve-sat-{base,ext4.0}.npz` nếu chưa có (chỉ đặc trưng M3 + nhãn, **không** có cột ΔPAP). Lineage và cách xoá/dựng lại: [data/README](../../data/README.md). Cache NPZ bị gitignore; `results.json` nằm ở đây.
