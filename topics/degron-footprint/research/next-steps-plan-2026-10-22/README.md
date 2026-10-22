# Kế hoạch nghiên cứu và thử nghiệm tiếp theo — 22/10/2026

Kế hoạch này nối tiếp [G2 bão hòa](../g2-saturation-2026-10-18/README.md), [G2 mở rộng](../g2-extension-2026-10-18/README.md) và [audit MetaDegron](../metadegron-analysis-2026-10-21/README.md). Nó **không** đổi trạng thái G2/G3, không chốt kiến trúc, không thay tiêu chí nghiệm thu của bất kỳ thí nghiệm đã tiền đăng ký. Mọi mục đánh `[ĐỀ XUẤT]` cần Trọng duyệt trước khi chạy.

Phần tìm dataset bổ sung nằm riêng ở [dataset-search.md](dataset-search.md); kết quả kiểm truy cập `[ĐO]` ở [candidate-access.json](candidate-access.json), sinh bởi [check_candidate_access.py](check_candidate_access.py). Phép đếm bộ lọc bão hòa `[ĐO]` ở [sat-filter-dropoff.json](sat-filter-dropoff.json), sinh bởi [sat_filter_dropoff.py](sat_filter_dropoff.py).

**Kết quả đáng chú ý nhất của phiên lập kế hoạch này** `[ĐO]`: nguồn nhãn lớn nhất chưa khai thác **không nằm ngoài repo**. Trong 248 peptide bão hòa thô, **144 peptide bị loại chỉ bởi một ngưỡng duy nhất** — `PSI(WT) ≤ 3,0` của `residue_data.DEGRON_PSI_MAX` — chứ không phải vì thiếu dữ liệu hay lỗi trình tự. Nới ngưỡng lên 4,0 thêm **85 peptide**, gần gấp đôi bộ 91 peptide hiện dùng, **không cần tải gì và không cần quyền sử dụng mới** (§2, P0).

## 0. Cập nhật trạng thái — 22/10/2026 (cuối ngày)

Phần còn lại của file này là **kế hoạch gốc, giữ nguyên làm bản ghi lịch sử**; các mục §1–§5 viết trước khi chạy. Bảng dưới là kết quả thật. Mọi số dẫn file `results.json` tương ứng.

| # | Trạng thái | Kết quả `[ĐO]` | Chi tiết |
|---|---|---|---|
| P0 | **Đã chạy, nhận** | Nới ngưỡng `PSI(WT) ≤ 4,0`: ridge 0,8082 → 0,8208, +0,0126, CI [+0,0061; +0,0190], ba seed dương. Bền qua `RESCUE_DELTA` và 3 phân hoạch protein thật | [learning-curve](../learning-curve-2026-10-22/README.md), [recluster-sensitivity](../recluster-sensitivity-2026-10-22/README.md) |
| P1 | **Đã chạy, hỗ trợ một nửa** | Ridge phẳng từ ~35 cụm (CI phủ 0); `gate_no_pap` vẫn lên (+0,0156, CI [+0,0060; +0,0256]) | [learning-curve](../learning-curve-2026-10-22/README.md) |
| P2 | **Đã chạy, cổng KHÔNG đạt** | Koren 2018 S4 đọc được, PSI tái tính khớp 1.827/1.827 dòng, nhưng chỉ **5 cụm cov80 mới** (cần ≥ 20); 3 bin PSI (Zhang 6 bin), 23-mer đầu C. Chỉ làm tập kiểm chứng ngoài tiềm năng; nguồn không giấy phép mở | [koren-s4-audit](../koren-s4-audit-2026-10-22/README.md) |
| P3 | **Đã chạy, âm** | Tiền huấn luyện nhãn tile Voutsinos rồi tinh chỉnh: `pre` − `rand` = −0,0077 (CI [−0,016; +0,001]) ở ext 4,0, −0,028 ở base; `pre` < ridge. Chỉ bác thiết kế "tiền huấn luyện trên trình tự hoang dại rồi tinh chỉnh toàn bộ" | [pretrain-p3](../pretrain-p3-2026-10-22/README.md) |
| P4 | **Không chạy** | Phụ thuộc P2 qua cổng; điều kiện dừng đã chốt trước | — |
| P5 | **Không chạy** | Phụ thuộc P4. Phần B của learning-curve đã thực hiện một phần ý tưởng (tách "thêm cụm" khỏi "mở rộng phân bố"), kết quả chưa phân định | [learning-curve §4b](../learning-curve-2026-10-22/README.md) |
| P6 | **Đã chạy, nhận** | Platt: Brier 0,0925 so với 0,1272 (thô), CI [+0,0266; +0,0425], ba seed dương; top-10% mỗi peptide làm giàu 4,02×. Nguyên mẫu CLI `predict.py` khớp runner < 1e-9, chưa có web UI | [calibration-p6](../calibration-p6-2026-10-22/README.md) |
| — | **Phân cụm lại** (việc phụ nêu ở learning-curve §6) | Độ mịn phân cụm thật: lợi ích P0 dương ở cả 3 phân hoạch khác phân hoạch đối chứng. Lưới 7 mức chỉ cho 4 phân hoạch riêng biệt | [recluster-sensitivity](../recluster-sensitivity-2026-10-22/README.md) |

**Đính chính §1.** Dòng "Nút thắt là lượng và độ đa dạng của nhãn" ở §1 là diễn giải trước khi chạy và **không còn đứng vững nguyên dạng**: ridge phẳng ở P1 là bằng chứng chống lại cách đọc thuần "lượng", còn mức tăng của P0 đến từ nhãn ở vùng `PSI(WT)` 3,0–4,0. Cách đọc dùng được hiện nay là **độ phủ phân bố nhãn**, kèm mức dè dặt của phần B: *chưa phân định dứt khoát* giữa "thêm cụm" và "mở rộng phân bố". Lý do vẫn cần nguồn ngoài (nếu còn) là lớp degron khác, không phải số ô.

**Việc còn lại thật sự** `[ĐỀ XUẤT]`, chưa chạy:

1. Nguồn nhãn T1 khác Koren: Timms 2023 (Mol Cell) và bioRxiv "Single Amino Acid Disease Mutations Act as Genetic Glues" — cả hai còn `[CHƯA XÁC MINH]`, endpoint khác PSI ở nguồn thứ hai.
2. Tách "vùng `PSI(WT)`" khỏi "protein khác" (cần cặp peptide cùng protein ở hai vùng ngưỡng; bộ hiện có chưa chắc đủ).
3. Đối chứng Degformer sạch cụm — điều kiện còn thiếu của G2, nên **G2 vẫn chưa hoàn tất**.
4. Giao diện web cho nguyên mẫu G3, kiểm thử đầu vào và kiểm thử người dùng.
5. Kiểm chứng ngoài thật cho mô hình (hiện chỉ có benchmark phát triển OOF).

## 1. Điểm khởi hành: ba kết quả âm chỉ về cùng một chỗ

- `[ĐO]` Trên bộ bão hòa 91 peptide / 89 cụm cov80 / 47.847 ô: ridge M3 **0,8082**, ΔPAP `cnn2w1` **0,7693**, kiến trúc Degformer huấn luyện lại cùng ngân sách nhãn **0,7500** ([results.json](../g2-saturation-2026-10-18/results.json), [e3-degformer-arch.json](../g2-extension-2026-10-18/e3-degformer-arch.json)).
- `[ĐO]` **Năm** thiết kế có sức chứa lớn hơn ridge đều không đạt tiêu chí chốt trước: gate sigmoid, FiLM, song tuyến hạng 8, cross-ridge, và chính kiến trúc transformer đã công bố ([e2-candidates.json](../g2-extension-2026-10-18/e2-candidates.json)).
- `[ĐO]` Trần nhãn (độ tương hợp hai nửa replicate) là **0,9519**; E3 trong G2 chọn epoch tốt nhất là epoch 2 ở cả 5/5 fold, nên 0,7500 không do huấn luyện thiếu.
- `[DIỄN GIẢI]` Nút thắt là **lượng và độ đa dạng của nhãn**, không phải sức chứa mô hình. Nhưng thí nghiệm tách riêng yếu tố này **chưa chạy**.

`[DIỄN GIẢI]` Hệ quả cho kế hoạch: việc tiếp theo **không** phải thử biến thể lớp mạng thứ sáu. Có hai đường, chạy song song được:

- **Đường 1 — xác nhận chẩn đoán:** đo đường cong học để biết thêm nhãn có thực sự giúp (P1).
- **Đường 2 — nới nguồn nhãn:** trước hết khai thác nhãn **đã có tại máy nhưng đang bị bộ lọc chặn** (P0), rồi mới tới nhãn cùng hệ đo từ nguồn ngoài (P2, P4; chi tiết ở [dataset-search.md](dataset-search.md)).

Hai đường gặp nhau ở P5: nếu đường cong học còn dốc **và** có thêm nhãn cùng thang, thì lần đầu tiên đề tài có cơ sở để kiểm lại câu hỏi sức chứa mô hình một cách công bằng.

## 2. Thứ tự thí nghiệm

`[ĐỀ XUẤT]` Xếp theo giá trị thông tin trên chi phí. Chi phí là **ước lượng lập kế hoạch**, chưa benchmark. Giữ bất biến xuyên suốt: outer 5 fold cov80, inner validation theo cụm, seed 17/29/43, bootstrap 5.000 lần theo cụm, mọi chuẩn hóa/chọn đặc trưng/tiền huấn luyện chỉ trên outer-train, cov50 dùng kiểm độ nhạy.

| # | Thí nghiệm | Trả lời câu hỏi gì | Tiêu chí chốt trước | Chi phí ước lượng | Phụ thuộc |
|---|---|---|---|---|---|
| **P0** | Nới ngưỡng degron để mở rộng nhãn huấn luyện | 85 peptide đang bị ngưỡng `PSI(WT) ≤ 3,0` chặn có dùng được làm nhãn huấn luyện không? | **Outer-test giữ nguyên miền 91 peptide gốc** để số liệu so được với 0,8082; peptide thêm **chỉ vào outer-train**. Nhận khi AUROC trên outer-test gốc có CI delta > 0 và dương ở cả ba seed. Kèm báo tỉ lệ ô dương và phân bố ΔPSI của nhóm mới | 1–3 h CPU · 4–6 h người | Không. **Rẻ nhất, chạy cùng P1** |
| **P1** | Đường cong học theo số cụm | Nút thắt có đúng là lượng nhãn? | Hỗ trợ khi CI của AUROC(100%)−AUROC(50%) **> 0** và xu hướng tăng đơn điệu qua 25/50/75/100%; phẳng hoặc CI phủ 0 → ghi "chưa đủ bằng chứng", **không** diễn giải thành trần dữ liệu | 1–3 h CPU · 2–4 h người | Không. Chạy ngay |
| **P2** | Audit + nhập nhãn GPS cùng hệ đo (Koren 2018 S4/S7, Shimshon 2024, Bekturova 2025) | Có thêm được ô ΔPSI **cùng endpoint PSI** không, và bao nhiêu cụm *mới*? | Cổng dữ liệu: ≥ **20 cụm cov80 mới** không chồng bộ hiện có, và chiều ΔPSI tái lập được từ count/PSI thô hoặc bảng tác giả. Không đạt → chỉ dùng làm tập kiểm chứng ngoài, không nhập train | 2–6 h CPU · 10–16 h người | Quyền sử dụng từng nguồn |
| **P3** | Tiền huấn luyện nhãn mức tile rồi tinh chỉnh ΔPSI | Giám sát yếu từ Voutsinos có tạo lợi ích ổn định? | Cùng encoder random-init vs pretrained, cùng ngân sách nhãn và inner tuning; nhận lợi ích **chỉ khi** CI ghép cặp với M3 > 0 **và** dương ở cả ba seed | 6–24 h CPU hoặc 1–4 h GPU · 8–12 h người | P1 (đọc kết quả), loại cụm test trước pretrain |
| **P4** | Mở rộng nhãn liên hệ thống: hợp nhất bộ mới của P2 vào huấn luyện | Nhãn cùng thang nhưng khác thư viện có cộng dồn được? | Chỉ nhận khi (a) hiệu ứng batch/thư viện được mô hình hóa bằng chỉ báo nguồn, (b) AUROC trên outer-test **gốc** (chỉ Zhang) không giảm, (c) CI delta trên tập hợp nhất > 0 | 4–12 h CPU · 8–12 h người | **P2 qua cổng** |
| **P5** | Lặp lại P1 trên tập nhãn đã mở rộng | Thêm nhãn có dịch chuyển đường cong học, và sức chứa mô hình có bắt đầu trả cổ tức? | So độ dốc đường cong trước/sau. Chỉ mở lại câu hỏi kiến trúc khi độ dốc tại 100% **vẫn dương** trên tập đã mở rộng | 2–6 h CPU · 4–6 h người | P1 + P4 |
| **P6** | Hiệu chuẩn + G3 (nguyên mẫu công cụ) | Điểm có dùng được để ưu tiên đột biến? | Fit logistic/isotonic trong inner-train; báo Brier và reliability theo cụm trên outer-test. Chỉ gọi "đã hiệu chuẩn" khi Brier giảm so với điểm thô; mọi điểm giao diện phải tái tính khớp runner | < 1 h CPU · 16–24 h người | Mô hình G2 cố định |

`[DIỄN GIẢI]` **P0 và P1 là một cặp.** P1 hỏi "thêm nhãn có giúp không", P0 là nguồn nhãn thêm sẵn có và rẻ nhất để trả lời. Chạy chung thì P0 vừa là thí nghiệm vừa là điểm dữ liệu thứ năm cho đường cong học, nằm **bên phải** mốc 100% hiện tại — tức lần đầu tiên đường cong có điểm vượt quá 89 cụm.

`[DIỄN GIẢI]` **Rủi ro riêng của P0, phải nói trước.** Ngưỡng `PSI(WT) ≤ 3,0` không tùy tiện: nó định nghĩa "peptide này là degron". Peptide có WT bền (PSI cao) thì phần lớn phép thay không còn chỗ để làm reporter bền thêm, nên nhãn "ô dương khi ΔPSI ≥ 1" đổi nghĩa và có thể bị chặn trên. Vì vậy P0 **không phải dữ liệu miễn phí**; nó là một phép đổi định nghĩa nhiệm vụ, và chỉ an toàn theo đúng thiết kế đã ghi ở bảng: **miền đánh giá không đổi, chỉ ngân sách huấn luyện đổi**. Nếu báo AUROC trên miền đã nới rồi so với 0,8082 thì đó là phép so sai.

`[DIỄN GIẢI]` P1 đi trước (hoặc cùng P0) vì nó rẻ nhất và nó **quyết định ý nghĩa của mọi việc còn lại**: nếu đường cong đã phẳng ở 89 cụm thì P2/P4 mất phần lớn lý do tồn tại, và trọng tâm luận văn nên chuyển sang P6 cùng việc báo cáo kết quả âm cho tử tế. Nếu đường cong còn dốc thì P0 trả về giá trị trước tiên vì nó gần như không tốn gì, còn P2 là nguồn nhãn ngoài duy nhất thêm được ô ΔPSI **không** phải trả giá chuyển đổi hệ đo.

### Thứ tự chạy được đề xuất

```
P0 ─┐
    ├─> P1 ─┬─> (dốc)   ─> P2 ─> [cổng dữ liệu] ─> P4 ─> P5 ─┬─> P6 ─> viết luận văn
    │       │               └─> không qua cổng ─> kiểm chứng ngoài ─┤
    │       └─> (phẳng) ─> P3 (một lượt) ──────────────────────────┘
    └─ P3 chạy song song được (dữ liệu đã có tại máy)
```

P3 chạy được song song với P2 vì nó chỉ dùng dữ liệu đã có tại máy (`data/raw/voutsinos-2026/`), không chờ quyền sử dụng nguồn mới.

## 3. Những gì KHÔNG làm trong kế hoạch này

`[DIỄN GIẢI]` Ghi rõ để tránh trôi phạm vi:

- **Không** thử thiết kế tương tác thứ sáu (attention/gate/FiLM/bilinear biến thể) để né năm kết quả âm. Câu hỏi kiến trúc chỉ mở lại qua P5, với điều kiện định lượng.
- **Không** gán nhãn nhị phân motif (MetaDegron/ELM/DEGRONOPEDIA) thành giá trị trên thang ΔPSI. "Là degron" không phải "phép thay làm PSI đổi bao nhiêu".
- **Không** dùng điểm dự đoán (PAP, Degformer, SVM của chính Zhang, degron dự đoán trong DegronMD) làm nhãn thật.
- **Không** tăng số lần thử rồi chọn seed/CI thuận lợi. Mọi tiêu chí chốt ở `PREREGISTRATION.md` của từng thí nghiệm, trước khi chạy.
- **Không** nhập nguồn nào vào huấn luyện hay vào nguyên mẫu công khai trước khi quyền sử dụng được đọc và ghi vào `data/README.md`.
- **Không** sửa slide/deck hay nội dung trình bày trong các phiên thí nghiệm này.

## 4. Rủi ro và điều kiện dừng

| Rủi ro | Dấu hiệu nhận ra | Phản ứng đã định trước |
|---|---|---|
| P1 cho đường cong phẳng | CI(100%−50%) phủ 0 ở cả ba seed | Dừng P2/P4/P5 như đường găng; chuyển trọng tâm sang P6 + báo cáo giới hạn. Đây là **kết quả hợp lệ**, không phải thất bại của phiên |
| Nguồn mới không cùng thang PSI | Phân bố PSI/ΔPSI lệch hệ thống so với Zhang, hoặc không tái lập được từ count thô | Giữ nguồn riêng với head riêng; dùng làm kiểm chứng ngoài, không hợp nhất |
| Cụm mới thực chất không mới | Giao cov80/cov50 với 89 cụm hiện có quá cao | Báo "effective new clusters" thật, không cộng dồn số peptide thô |
| Quyền sử dụng không rõ | Repo không LICENSE, trang điều khoản 403, hoặc giấy phép không phủ file dữ liệu | Ghi blocker vào `data/README.md`, không tải hoặc không nhập; **không** coi HTTP 200 là được phép dùng |
| Rò rỉ qua tiền huấn luyện | Cụm outer-test xuất hiện trong nguồn pretrain | Loại cụm test **trước** mọi bước học, trong từng fold; ghi lại số dòng bị loại |
| P0 đổi nghĩa nhãn chứ không thêm thông tin | Tỉ lệ ô dương của nhóm peptide mới thấp bất thường, hoặc ΔPSI bị chặn trên | Báo P0 như kết quả âm có ích: "nới miền degron không thêm tín hiệu học được". Giữ ngưỡng 3,0 làm cấu hình chính |
| Hết thời gian học phần | — | P0 + P1 + P3 + P6 là lõi tối thiểu đủ cho một luận văn trung thực; P2/P4/P5 là phần mở rộng |

## 5. Việc cần làm ngay, theo đúng thứ tự

`[ĐỀ XUẤT]`

1. Tạo `research/learning-curve-2026-10-2X/` với `PROTOCOL.md` chốt trước, rồi chạy **P0 + P1 trong cùng thí nghiệm**: nested subsets 25/50/75/100% theo cụm trong outer-train cộng mốc "100% + 85 peptide nới ngưỡng", ba seed 17/29/43, chỉ M3 và một encoder chốt trước, outer-test cố định ở miền 91 peptide gốc. Cache nhãn mới cần dựng lại từ `residue_data.load_all(degron_psi_max=...)`, nên đây là lần duy nhất trong kế hoạch có sinh dữ liệu mới vào `data/processed/` — cập nhật `data/README.md` trong cùng phiên.
2. Chạy §4.1 của [dataset-search.md](dataset-search.md): đối chiếu con số "219 degron CRL saturation" với dữ liệu đã có tại máy, trước khi bỏ công đi tìm nguồn ngoài.
3. Chạy bước xác minh quyền sử dụng của P2 theo [dataset-search.md §4](dataset-search.md): quyền trước, dữ liệu sau. Nhắm **Koren 2018 Table S4** trước tiên.
4. Chỉ sau khi có kết quả P0+P1: quyết định P2/P4 có phải đường găng hay không, và cập nhật đề cương ở [proposal/](../../proposal/) nếu kết luận thay đổi phạm vi.
