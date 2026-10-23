# R6 — Chuỗi đối chứng biểu diễn × đầu mạng, ngữ cảnh rộng và bộ scanning: PROTOCOL chốt trước khi chạy

Chốt ngày 23/10/2026, **trước khi** chạy bất kỳ giai đoạn nào của R6 trên Kaggle. Không sửa tiêu chí sau khi xem kết quả; nếu phải sửa thì thêm mục "sửa sau khi xem" kèm ngày và lý do, không ghi đè. SHA-256 của file này được nhúng vào notebook (`stamp_protocol.py`); notebook dừng nếu file đổi.

Nối tiếp [R1](../r1-degformer-clean-2026-10-22/PROTOCOL.md) và [R2](../r2-esm-features-2026-10-22/PROTOCOL.md) (cả hai không đạt tiêu chí "nhận"). R2 §5 cấm đổi cỡ ESM-2 hay đưa ESM vào mạng nơ-ron; R6 là PROTOCOL **mới** làm đúng việc đó, không sửa R2. R6 **không** đổi trạng thái G2/G3 và không phải kiểm chứng ngoài.

## 0. Biết trước khi chốt (nói thẳng)

- Đã biết kết quả R0–R3: ridge M3 ext 4,0 = 0,8208; Degformer sạch cụm 0,8068 (Δ −0,0140, CI [−0,0283; +0,0010]); ESM-2 650M PCA-64 cộng vào ridge Δ +0,0022 (CI [−0,0033; +0,0082]). Phân tích từng peptide của R2 cho thấy Δ do hai peptide tạo ra.
- Đã xem **một phép kiểm chéo nguồn mô tả** (23/10/2026, ngoài PROTOCOL này) trên các ô scanning và bão hòa trùng nhau: 42/88/117 peptide ở ngưỡng PSI(WT) ≤ 3,0/≤ 4,0/không ngưỡng; Pearson 0,79/0,74/0,70; κ nhị phân 0,75/0,69/0,65; AUROC gộp của ΔPSI scanning cho ô dương bão hòa 0,947/0,922/0,905. Nhãn hai nguồn **nhất quán trên cùng ô**; không ai biết trộn chúng **có lợi** cho mô hình hay không: chưa chạy mô hình nào trộn. Giai đoạn B và G là phép đo đó.
- **Phát hiện trước khi chạy R6 (23/10/2026):** thư mục [scan-sat-merge-2026-10-23](../scan-sat-merge-2026-10-23/PROTOCOL.md) do một phiên làm việc khác tạo song song — **không phải** của người soạn R6, và R6 chưa tái lập số của nó — đã tiền đăng ký và chạy ridge M3 + bộ scanning (gộp mù S1, gộp có khối riêng nguồn S2, tiên nghiệm S3) và mạng `gate_no_pap` tiền huấn luyện trên scanning (N2). Theo `results.json` của thư mục đó: không biến thể ridge nào hơn A1 = 0,8208 (S1 0,8189; S2 0,8203, Δ −0,0005, CI [−0,0009; −0,00004]; S3 0,8197); N2 0,8168 so với N1 0,8154. Hệ quả cho R6: giai đoạn B chỉ còn là **lặp độc lập** (rẻ, giữ lại) và G có kỳ vọng thấp hơn trước, nên **thứ tự chạy được đổi từ ...E, G, F thành ...E, F, G** để hạn mức GPU ưu tiên cho phép quét cỡ ESM. Việc đổi này làm **trước** khi có bất kỳ số R6 nào.
- Kiểm thử mã (`selftest_r6.py`) chỉ chạy mốc ridge M3 đã biết và chạy mạng 2 epoch trên ≤ 4.200 ô, **không in AUROC** của bất kỳ biến thể nào. Chưa có số R6 nào.
- Cỡ ESM chính (35M) chọn theo luận văn tham khảo T1 ([thesis-comparison](../../../../resources/reference-theses/thesis-comparison.md): 35M + mCNN (3,5,7) là cấu hình ưu tiên) và theo cỡ mẫu hiệu dụng nhỏ (khoảng 2.400 ô độc lập ở ext 4,0; [ladder.json](../residue-task-derisk-2026-10-15/ladder.json)), **không** theo số đo nào của đề tài.
- Siêu tham số mạng chốt **một lần** (§3), không dò theo cấu hình. Đây là lựa chọn có chủ ý để kiểm soát số lần thử; hệ quả ở §8.

## 1. Câu hỏi

| # | Câu hỏi |
|---|---|
| Q1 | Ngữ cảnh WT rộng hơn ±3 có giúp ridge không? (điều kiện để mạng tích chập có chỗ thêm thông tin) |
| Q2 | Thêm nhãn bộ scanning (4.802 peptide / 2.902 cụm) vào huấn luyện có giúp trên benchmark bão hòa không, với ridge và với mạng? |
| Q3 | Δ embedding ESM-2 đóng băng ở cỡ 8M/35M/150M/650M có giúp ridge M3 không? |
| Q4 | CNN/mCNN trên one-hot có đạt ridge M3 không? |
| **Q5 (CHÍNH)** | **ESM-2 35M đóng băng + mCNN (3,5,7) có hơn ridge M3 ext 4,0 không?** |
| Q6 | Với mCNN, cỡ ESM-2 có đổi điểm không? |

## 2. Dữ liệu và chia

- **Bão hòa:** đúng bộ gộp 92.337 ô của R2: 47.847 ô của 91 peptide gốc (outer-test duy nhất, trùng G2) + 44.490 ô của 85 peptide nới ngưỡng `PSI(WT) ≤ 4,0` (chỉ vào outer-train). 5 outer fold cov80 trùng G2; chia train/val `GroupShuffleSplit(test_size=.2, random_state=seed)` theo cụm trên pool = hàng không thuộc cụm test; seed 17/29/43. **Mọi cấu hình dùng cùng (tr, va, te) của từng (seed, fold)** (hàm `common.pool_split` của R2).
- **Scanning:** [r6-scantable.npz](../../data/README.md) dựng bởi `make_scantable.py` từ Zhang 2023 Replicate 1: ΔPSI = PSI(ô) − PSI(WT đo trực tiếp `_mut0`); giữ peptide `PSI(WT) ≤ 4,0`, ≥ 21 vị trí, reads ≥ 10; **4.802 peptide, 133.764 ô, 2.902 cụm cov80**; loại 7 peptide có accession không nằm trong file cụm. Mỗi vị trí đúng **một** thay thế, chỉ **R/A/S** (quy tắc "opposite scanning"). Ngưỡng chính **4,0**; biến thể mô tả **3,0** (2.989 peptide, 83.306 ô).
- **Quy tắc rò rỉ:** với mỗi outer fold, **loại mọi hàng scanning thuộc cụm cov80 của outer-test** (cổng §6 kiểm = 0 cụm giao). Hàng scanning **chỉ vào train, không bao giờ vào val hay test**; val luôn là ô bão hòa (như cấu hình nền) nên epoch/α chọn trên cùng loại ô mà bài toán đánh giá. Chỉ dùng cụm cov80; không áp thêm luật MMseqs2 theo hit như R1/P3 (§8).
- **Chỉ số:** AUROC mức ô, macro theo peptide trên 47.847 ô outer-test (`derisk.macro_auroc`), điểm OOF ensemble = trung bình ba seed.

## 3. Mô hình (chốt, không đổi sau khi thấy số)

**Đặc trưng ridge.** M3 = pair (WT, mut one-hot: 40) + thành phần peptide (20) + ngữ cảnh WT có thứ tự ±3 (120) = 180 cột, dựng lại bằng `r6data.cell_features` và **phải bằng cache từng bit** (cổng). Giai đoạn A thay ±3 bằng ±5/±7/±10 (240/320/440 cột ngữ cảnh; tổng 260/340/460 cột); vị trí ngoài trình tự là 0. Ridge: lưới α ∈ {1,10,100,1000} chọn bằng MSE trên val, khớp lại trên train ∪ val (đúng `common.ridge_full`).

**ESM-2** (Hugging Face, MIT theo model card, ngày đọc ghi vào `results.json`): `esm2_t6_8M_UR50D` (320 chiều), `esm2_t12_35M_UR50D` (480), `esm2_t30_150M_UR50D` (640), `esm2_t33_650M_UR50D` (1280); lớp cuối `last_hidden_state`, fp16 trên GPU. Δ = h_mut − h_wt theo từng vị trí. Hai dạng lưu: **pool** `[Δ tại điểm đột biến ; trung bình Δ 28 vị trí]` (2·d chiều; cho ridge, đúng công thức R2) và **crop** Δ ở 15 vị trí p−7..p+7 (0 ngoài trình tự; cho mạng). Cỡ chính cho mạng và scanning: **35M**.

**Ridge + ESM (giai đoạn D):** đúng R2 — PCA 64 thành phần khớp một lần mỗi outer fold trên toàn outer-train, `random_state=17`, chuẩn hóa z, ghép 180 cột M3; ridge như trên.

**Mạng `ConvHead`** (`r6nn.py`), một họ duy nhất:

| Thành phần | Chốt |
|---|---|
| Đầu vào theo vị trí (cửa sổ 15) | one-hot WT (20) + chỉ báo trung tâm (1); với ESM thêm `GELU(Linear(d→32)(dropout 0,2 (Δ embedding)))`; vị trí ngoài trình tự bị che |
| Tích chập | `Conv1d(k)` + ReLU, `padding=k//2`, mỗi cửa sổ lấy **max theo vị trí** và **giá trị tại trung tâm** |
| `cnn1` | một cửa sổ k=5, 96 bộ lọc |
| `mcnn` | ba cửa sổ k=3,5,7, mỗi cửa sổ 32 bộ lọc |
| Đầu | nối [đặc trưng tích chập ; pair (40) ; thành phần peptide (20) ; chỉ báo nguồn nếu `scan_pool`] → dropout 0,3 → Linear(·,64) → ReLU → dropout 0,3 → Linear(64,1) |
| Mất mát | MSE trên ΔPSI (nhãn liên tục), bias khởi tạo bằng trung bình nhãn train |
| Tối ưu | AdamW, lr 1e-3, weight decay 1e-2, batch 1024, tối đa 40 epoch, dừng sau 6 epoch không cải thiện MSE val, chọn epoch val tốt nhất; **không** khớp lại trên train ∪ val |
| Seed | `seed·1000 + fold` cho khởi tạo và xáo trộn; ba seed 17/29/43 |

Biểu diễn `onehot` **không** có kênh ESM; biểu diễn `esmXX` **chỉ thêm** kênh Δ embedding vào đúng đầu đó. Vì thế `esm35_mcnn` − `oh_mcnn` tách tác dụng của biểu diễn khi giữ đầu.

**Chế độ scanning cho mạng** (chỉ cho `oh_mcnn` và `esm35_mcnn`):
- `scan_pool`: huấn luyện trên bão hòa ∪ scanning (không rò cụm test), thêm chỉ báo nguồn vào đầu (0 = bão hòa, 1 = scanning; ở test luôn 0); trọng số hàng bằng nhau;
- `scan_ft`: tiền huấn luyện chỉ trên scanning (val = 20% cụm scanning giữ lại; lr 1e-3, tối đa 30 epoch, patience 4), rồi tinh chỉnh trên bão hòa từ trọng số đó (lr 3e-4, tối đa 30 epoch, patience 6, val bão hòa như nền).

**Chế độ scanning cho ridge:** `pool` = ridge trên bão hòa ∪ scanning + cột chỉ báo nguồn; `prior` = ridge trên scanning (α chọn trên 20% cụm scanning giữ lại), rồi ridge phần dư trên bão hòa, dự đoán = f_scan + g.

## 4. Giai đoạn

| GĐ | Việc | Thiết bị | Cấu hình ghi vào OOF |
|---|---|---|---|
| 0 | Cổng tái lập (§6) + kiểm chéo nguồn mô tả | CPU | `ridge_M3` |
| A | Ridge ngữ cảnh ±5/±7/±10 | CPU | `ridge_W5/W7/W10` |
| B | Ridge + scanning (`pool`, `prior`; ngưỡng 4,0 chính, 3,0 mô tả) | CPU | `ridge_scan_pool/prior[_t3]` |
| C | Trích ESM-2 (crop + pool) cho bốn cỡ trên ô bão hòa; crop cỡ 35M cho ô scanning | GPU | — |
| D | Ridge + ESM theo cỡ (PCA-64) | CPU | `ridge_esm8/35/150/650` |
| E | Mạng: `oh_cnn1`, `oh_mcnn`, `esm35_cnn1`, `esm35_mcnn` | GPU | cùng tên |
| F | `esm8_mcnn`, `esm150_mcnn`, `esm650_mcnn` | GPU | cùng tên |
| G | Mạng + scanning cho `oh_mcnn`, `esm35_mcnn` × (`scan_pool`, `scan_ft`) | GPU | `<cfg>+scan_pool/ft` |

Thứ tự chạy trong notebook: 0, A, B, C, D, E, F, G. Giai đoạn nào hết hạn mức thì dừng; kết quả giai đoạn trước đã lưu (OOF từng fold), báo giai đoạn chưa chạy là **chưa chạy**, không phải âm.

## 5. So sánh và họ kiểm định (chốt trước)

Mọi so sánh: Δ = A(X) − A(Y) ghép cặp theo peptide, bootstrap 5.000 lần **theo cụm** (`run_curve.compare`, seed 20261022). Với họ có m phép, kết luận dùng **CI Bonferroni** (phân vị 0,025/m và 1−0,025/m); CI 95% không hiệu chỉnh vẫn được báo.

| Tên | So sánh | m | Vai trò |
|---|---|---:|---|
| **P** | `esm35_mcnn` − `ridge_M3` | 1 | **CHÍNH — duy nhất xác nhận** |
| S1 | `esm35_mcnn` − `oh_mcnn` | 1 | phụ (tách biểu diễn, cùng đầu) |
| S2/S3 | `oh_mcnn` − ridge · `oh_cnn1` − ridge | 1 | phụ (đầu mạng có đạt ridge?) |
| S4 | `esm35_cnn1` − ridge | 1 | phụ |
| S5/S6 | mCNN − CNN1 (one-hot; ESM 35M) | 1 | phụ, **mô tả** (dưới ngưỡng phân giải, §8) |
| A | `ridge_W{5,7,10}` − `ridge_M3` | 3 | họ A |
| B | `ridge_scan_{pool,prior}` − `ridge_M3` (ngưỡng 4,0) | 2 | họ B |
| D | `ridge_esm{8,35,150,650}` − `ridge_M3` | 4 | họ D |
| F | `esm{8,150,650}_mcnn` − `esm35_mcnn` | 3 | họ F, mô tả |
| G | `<cfg>+scan_{pool,ft}` − `<cfg>` với cfg ∈ {`oh_mcnn`, `esm35_mcnn`} | 4 | họ G |
| mô tả | `ridge_scan_*_t3` − ridge | 1 | độ nhạy ngưỡng scanning |

## 6. Tiêu chí kết luận (chốt trước)

Gọi Δ là hiệu ensemble, [lo, hi] là CI dùng để kết luận (hiệu chỉnh nếu m > 1), Δ₁₇, Δ₂₉, Δ₄₃ là hiệu từng seed (cùng train/val):

| Điều kiện | Kết luận ghi vào báo cáo |
|---|---|
| lo > 0 **và** Δ₁₇, Δ₂₉, Δ₄₃ đều > 0 | **nhận** |
| lo > 0 nhưng có seed ≤ 0 | lợi ích chưa bền qua seed |
| hi < 0 | **âm** |
| còn lại | chưa đủ bằng chứng (CI phủ 0) |

Hàm `r6stats.verdict` cài đúng bảng này. Thêm một nhãn **mô tả**: "tương đương trong ±0,01" khi CI 95% nằm trong (−0,01; +0,01); nhãn này **không** là tiêu chí chấp nhận.

Quy tắc đọc: chỉ phép **P** được gọi là "xác nhận". "Nhận" ở một họ (A, B, D, G) là kết luận cho họ đó, không phải bằng chứng cho mô hình sản phẩm. Phép S* và F là mô tả, không dùng để chọn cấu hình rồi báo như xác nhận. Không chọn "cỡ tốt nhất" trên chính benchmark này rồi báo điểm của nó như ước lượng không chệch.

**Hệ quả cho R5 (ghi trước):** mô hình sản phẩm chỉ đổi khỏi ridge + Platt nếu **P = nhận** và (kiểm riêng, ngoài notebook) độ trễ suy luận chấp nhận được. Mọi kết quả khác giữ ridge.

## 7. Cổng tự kiểm (dừng nếu hỏng)

1. Manifest dữ liệu khớp SHA-256; PROTOCOL khớp SHA nhúng trong notebook.
2. 92.337 ô; 5 fold trùng G2 (`common.load_combined` assert); **đặc trưng dựng lại bằng `cell_features(W=3)` bằng cache từng bit**.
3. Ridge M3 qua đường chia của R6: ensemble 0,8208 (|Δ| ≤ 1e-4), từng seed 0,8204/0,8210/0,8209 (|Δ| ≤ 2e-4).
4. Bảng scanning: mọi trình tự dài 28; **số hàng scanning thuộc cụm outer-test đã đưa vào train = 0** ở cả 5 fold.
5. Embedding: không NaN/Inf; trích lại 128 ô đầu cho cùng giá trị (tương đối ≤ 1e-2, fp16) — **không chặn** (ghi lại) ở cỡ ≠ 650M.
6. Cổng mềm (ghi, không chặn): ridge + ESM 650M tái lập R2 (0,8230 ± 1e-3); không thì ghi nguyên nhân khả dĩ (phiên bản `transformers`, fp16).

## 8. Điều không làm

- Không đổi cỡ ESM chính (35M), lớp lấy đặc trưng, bán kính cắt (±7), PCA-k, siêu tham số mạng, ngưỡng scanning chính hay trọng số hàng sau khi thấy số.
- Không tinh chỉnh (fine-tune) ESM-2; không thêm bất kỳ biến thể mạng nào ngoài bảng §3–§4 (đúng tinh thần "không thử thiết kế thứ sáu").
- Không dùng nhãn scanning làm tập val hoặc test; không dùng Koren/MetaDegron/Larsen/ClinVar.
- Không chạy lại để "chọn lần đẹp". Phiên ngắt thì tiếp tục từ OOF đã lưu; kết quả vẫn là một lần.
- Không báo giai đoạn chưa chạy là âm.

## 9. Giới hạn ghi trước

- Benchmark **phát triển OOF**, không phải kiểm chứng ngoài; cùng 91 peptide đã được khảo sát nhiều lần (R0–R3, P0–P6).
- **Độ phân giải:** từ CI của R1/R2, sai số chuẩn của phép so mạng với ridge ước 0,005–0,0075, nên hiệu nhỏ nhất phát hiện được (power 80%) khoảng 0,014–0,021; với phép ghép cặp hai cấu hình gần nhau như S5/S6 thì khoảng 0,008. Một kết quả "chưa đủ bằng chứng" **không** loại trừ lợi ích nhỏ hơn mức đó.
- Một cấu hình siêu tham số cho mọi mạng: mạng âm không loại trừ mạng được tinh chỉnh tốt hơn. Bù lại, mọi so sánh giữa mạng là cùng điều kiện.
- ESM-2 đã tiền huấn luyện trên UniRef nên các protein người của đề tài rất có thể đã "được thấy"; cỡ lớn có thể nhớ nhiều hơn, nên đường cong theo cỡ trên benchmark này không phải bằng chứng tổng quát hóa sang chuỗi người dùng tự gõ.
- Scanning chỉ có thay thế R/A/S (3 trên 19 loại) nên chỉ cung cấp tín hiệu về ngữ cảnh/vị trí và ba loại thay thế đó; đo scanning→bão hòa bằng ridge trước đây (0,7273, huấn luyện chỉ trên scanning) thấp hơn nhiều so với học trực tiếp trên bão hòa.
- Rò rỉ scanning chỉ chặn bằng cụm cov80; paralog ngoài cụm không bị phát hiện (R1/P3 dùng luật chặt hơn). Chỉ 7 peptide scanning bị loại vì thiếu cụm.
- Trong `scan_pool` trọng số hàng bằng nhau nên scanning (≈ 105–134 nghìn ô) có thể áp đảo bão hòa; đó là lựa chọn chốt trước, không phải tối ưu.
- ΔPSI scanning dùng WT đo trực tiếp, bão hòa dùng WT nội tại; trên ô trùng hai thang gần nhau (chênh PSI(WT) trung bình giữa hai nguồn từ −0,01 đến +0,13) nhưng độ dốc OLS 0,70–0,77 cho thấy scanning (một replicate) có nhiễu lớn hơn.
- Không hiệu chỉnh đa so sánh giữa các họ; chỉ trong từng họ.
- Kết quả scanning của thư mục `scan-sat-merge` (phiên khác) và của giai đoạn B/G cùng dùng bộ outer-test 91 peptide đã khảo sát nhiều lần; hai nguồn số không độc lập về dữ liệu, chỉ độc lập về mã.

## 10. Dự đoán ghi trước

`[ĐỀ XUẤT]` (của người soạn, để sau này chấm đúng/sai; không dựa trên số R6):
(a) A: không độ rộng nào "nhận"; |Δ| < 0,005.
(b) B: ridge `pool` và `prior` có |Δ| < 0,01; khả năng "nhận" ở họ B dưới 25%.
(c) D: không cỡ ESM nào "nhận" sau hiệu chỉnh; |Δ| < 0,01 ở mọi cỡ.
(d) E: `oh_mcnn` − ridge nằm trong [−0,03; 0]; `esm35_mcnn` − ridge nằm trong [−0,02; +0,01] và khả năng P = "nhận" dưới 20%; `esm35_mcnn` − `oh_mcnn` trong ±0,01; mCNN − CNN1 trong ±0,005 (không phân giải được).
(e) F: chênh giữa các cỡ < 0,01 và không đơn điệu theo cỡ.
(f) G: `scan_ft` không hơn mạng huấn luyện từ đầu; `scan_pool` trong ±0,01 so với mạng huấn luyện từ đầu.
Nếu dự đoán sai, ghi rõ trong báo cáo.

## 11. Chi phí

`[ƯỚC LƯỢNG]`, chưa benchmark; ô benchmark trong notebook in số đo thật **trước** giai đoạn E. GĐ 0/A/B/D: CPU, vài chục phút tổng cộng. GĐ C: ≈ 12–20 phút T4 cho bốn cỡ + vài phút cho scanning 35M. GĐ E/F/G: 11 cấu hình mạng × 15 lượt (3 seed × 5 fold); mỗi lượt vài chục giây đến ~2 phút trên T4 ⇒ vài giờ GPU. Bộ nhớ: crop float16 của 92.337 ô là 1,8/2,7/3,5/7,1 GB cho 8M/35M/150M/650M cộng 1,9 GB cho scanning 35M; cache ghi ở `/kaggle/temp` nếu có (ngoài gói kết quả). Hạn mức GPU Kaggle theo tuần và độ dài phiên: `[CHƯA XÁC MINH]`, kiểm lại trên giao diện.

## 12. Sửa sau khi xem (23/10/2026, trước khi Trọng chạy lượt chính thức)

**Việc đã xảy ra.** Khi chạy thử notebook trên CPU (kiểm đường code), lượt thử vô tình chạy luôn **giai đoạn A và B với dữ liệu thật** (bộ lọc danh sách giai đoạn của công cụ thử không khớp sau khi đổi thứ tự §4). Người soạn **đã thấy** kết quả ridge của A và B (lưu ở [dryrun-local-stageAB.json](dryrun-local-stageAB.json)); đã thấy thêm điểm ridge + ESM-8M (≈ M3 + 0,0006; không báo vì bốn cỡ trong lượt thử đều là 8M). **Chưa thấy** điểm mạng nào có giá trị (lượt thử mạng: 1 seed × 1 fold × 2 epoch, không in AUROC). Nội dung §1–§11 **không bị sửa**; thêm như sau:

1. **Phép so phụ mới S7, S8** (mô tả, m=1): `esm35_mcnn` − `ridge_W5` và `oh_mcnn` − `ridge_W5`. Lý do: giai đoạn A (ridge ±5 so với ±3: Δ +0,0078, CI Bonferroni [+0,0021; +0,0139], ba seed dương ⇒ "nhận" trong họ A) cho thấy M3 **không còn là ridge mạnh nhất**; so mạng chỉ với M3 có thể thổi phồng. Phép **P giữ nguyên** (mạng so với ridge M3, đã chốt) và vẫn là phép xác nhận duy nhất.
2. **Hệ quả R5 (bổ sung §6):** nếu họ A "nhận" ở lượt Kaggle chính thức thì ridge_W5 trở thành đối chứng tuyến tính khi cân nhắc đổi mô hình sản phẩm; mạng chỉ được cân nhắc khi vượt cả `ridge_W5` (S7), không chỉ M3.
3. **Dự đoán §10(a) đã sai** (có |Δ| ≥ 0,005 và một độ rộng "nhận"); §10(b) (ridge + scanning |Δ| < 0,01, không "nhận") khớp với lượt thử. Các dự đoán còn lại chưa bị kiểm. Ghi nhận ở đây, không sửa §10.
4. Kiến trúc và siêu tham số mạng (§3) **không đổi**. Lưu ý đã thấy: ridge được lợi từ ngữ cảnh ±4–±5 theo **vị trí cụ thể**, còn `ConvHead` chỉ thấy các vị trí đó qua đặc trưng tối đa-theo-vị-trí và giá trị tại trung tâm (cửa sổ k=7 chỉ phủ ±3 quanh mỗi vị trí). Nếu mạng thua `ridge_W5`, đó là một giải thích cần xét; đổi kiến trúc là việc của PROTOCOL mới.

