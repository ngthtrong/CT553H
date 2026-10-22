# Hiệu chuẩn điểm (P6) và nguyên mẫu G3 tối giản — 22/10/2026

Tiêu chí chốt **trước khi chạy** ở [PROTOCOL.md](PROTOCOL.md). Kết quả đầy đủ: [results.json](results.json); kiểm khớp nguyên mẫu: [verify.json](verify.json). Không đổi trạng thái G2/G3, không sửa đề cương hay slide. Đây là OOF trên **benchmark phát triển**, không phải kiểm chứng ngoài độc lập.

**[ĐO] Kết quả một dòng.** Hiệu chuẩn Platt biến điểm ridge M3 (mức nới ngưỡng 4,0, AUROC 0,8208) thành xác suất `P(ΔPSI ≥ 1)` **đạt cả hai tiêu chí chốt trước** ("đã hiệu chuẩn" và "có kỹ năng hơn tần suất nền"); xếp hạng top-10% mỗi peptide làm giàu ô dương **4,0 lần** so với ngẫu nhiên. Nguyên mẫu offline `predict.py` tái tính khớp runner với chênh tối đa **< 1e-9**.

## 1. Cổng tự kiểm đã qua `[ĐO]`

- Macro-AUROC điểm thô từng seed tái tạo: **0,8204 / 0,8210 / 0,8209**, bằng `results.json` của [P0](../learning-curve-2026-10-22/results.json) (sai lệch < 1e-9); ensemble **0,8208**. Runner `assert` điều kiện này.
- 5 outer fold trùng `folds` của G2 (assert kế thừa từ `run_curve`).
- Hệ số ridge tái khớp từ pool cho dự đoán trùng `run_curve.ridge` (< 1e-9) ở cả 15 (seed, fold).

## 2. Hiệu chuẩn — chỉ số trên outer-test `[ĐO]`

47.847 ô, 91 peptide, 89 cụm; tần suất dương quan sát **0,1310**. CI 95% bootstrap 5.000 lần theo cụm.

| Cách chuyển điểm → xác suất | Brier | CI 95% | Kỹ năng Brier so với tần suất nền | ECE (10 thùng) | slope / intercept hiệu chuẩn lại |
|---|---:|---|---:|---:|---|
| raw `clip(điểm, 0, 1)` | 0,1272 | [0,1186; 0,1360] | **−0,116** | 0,1437 | 0,35 / −1,42 |
| **platt** | **0,0925** | [0,0809; 0,1046] | **+0,188** | 0,0163 | 1,06 / +0,28 |
| iso | 0,0925 | [0,0810; 0,1045] | +0,188 | 0,0164 | 1,03 / +0,23 |
| const (tần suất nền của pool) | 0,1139 | [0,1011; 0,1276] | — | 0,0154 | — |

Macro-AUROC của xác suất: raw 0,8204, platt 0,8208, iso 0,8209 — iso không phá thứ hạng đáng kể.

### Phán quyết theo PROTOCOL §5

| So sánh | Hiệu Brier | CI 95% theo cụm | Ba seed |
|---|---:|---|---|
| raw − platt | **+0,0346** | **[+0,0266; +0,0425]** | +0,0346 · +0,0347 · +0,0347 |
| raw − iso | +0,0346 | [+0,0267; +0,0424] | đều dương |
| const − platt | **+0,0214** | **[+0,0175; +0,0253]** | đều dương |
| platt − iso | +0,00002 | [−0,0002; +0,0002] | — |

- **Platt: "đã hiệu chuẩn"** — (a) CI > 0 và (b) dương ở cả ba seed. Iso cũng đạt.
- **Kỹ năng so với tần suất nền:** CI của const − platt > 0 → "xác suất có kỹ năng hơn tần suất nền".
- **Bộ hiệu chuẩn cho nguyên mẫu: platt** (platt − iso có CI phủ 0, nên theo quy tắc chốt trước giữ cái đơn giản).

`[DIỄN GIẢI]` **Thanh "giảm Brier so với điểm thô" thấp hơn tên gọi của nó.** Điểm thô `clip(ΔPSI dự đoán)` là một đại lượng hồi quy được đọc như xác suất, và nó **tệ hơn cả việc luôn đoán tần suất nền** (kỹ năng −0,116; ước lượng quá cao: trung bình 0,262 so với 0,131 quan sát). Vì vậy tiêu chí (a) gần như chắc chắn đạt (đúng dự đoán 1 trong PROTOCOL §6). Con số có nghĩa hơn là phép so với **tần suất nền**: platt giảm Brier ~19% so với luôn đoán 0,12, mức của một bộ phân loại có AUROC ~0,82 trên lớp dương 13%.

`[DIỄN GIẢI]` Dự đoán chốt trước, đối chiếu: (1) platt hơn raw ở cả ba seed — **đúng**; (2) kỹ năng Brier 0,05–0,20 — **đúng, sát biên trên** (0,188); (3) iso ≈ platt, chênh < 0,002 — **đúng** (0,00002); (4) enrichment@10% cỡ 3–5, CI > 1 — **đúng** (4,02); (5) ECE < 0,02 — **đúng** (0,016), nhưng xem §3 vì ECE không phân biệt tốt trong bài toán này.

## 3. Hiệu chuẩn cục bộ và độ lệch miền `[ĐO]`

Biểu đồ độ tin cậy của platt (10 thùng cùng khối lượng, ~4.785 ô/thùng, cả 89 cụm có mặt ở mọi thùng):

| Thùng | p̂ trung bình | Tần suất quan sát | CI 95% theo cụm |
|---:|---:|---:|---|
| 0 | 0,011 | 0,013 | [0,005; 0,024] |
| 3 | 0,043 | 0,050 | [0,034; 0,068] |
| 6 | 0,105 | 0,116 | [0,095; 0,139] |
| 8 | 0,221 | 0,266 | [0,233; 0,299] |
| 9 | 0,434 | 0,495 | [0,449; 0,538] |

Đủ 10 thùng ở [results.json](results.json). `[ĐO]` Platt **thấp hơn quan sát một cách nhất quán ở mọi thùng**: trung bình xác suất **0,1146** so với **0,1310**; thùng cao nhất 0,434 so với 0,495 (CI quan sát **không** chứa 0,434).

`[DIỄN GIẢI]` Nguyên nhân khớp với một hiệu ứng đã biết: bộ hiệu chuẩn khớp trên **toàn pool** (gồm 85 peptide nới ngưỡng, tần suất dương 0,114) còn outer-test là miền 91 peptide gốc (0,131). Đó là **dịch chuyển miền** do chính P0 gây ra. **Độ nhạy theo miền (PROTOCOL §3, không dùng cho phán quyết)** xác nhận: khớp bộ hiệu chuẩn chỉ trên ô thuộc 91 peptide gốc cho Brier **0,0921** (platt) / 0,0922 (iso), kỹ năng 0,191, trung bình xác suất **0,1313**, ECE **0,0044 / 0,0024**, intercept hiệu chuẩn lại 0,03 / 0,00. Chênh Brier với bản chính nhỏ (~0,0004), nhưng cho thấy xác suất chính **thiên thấp** ở miền gốc.

`[DIỄN GIẢI]` Hệ quả cho nguyên mẫu: xác suất của `predict.py` (khớp trên toàn pool, đúng PROTOCOL §7) **hơi thiên thấp ~13% tương đối** nếu tile cần chấm thuộc miền degron đúng như 91 peptide gốc, và phù hợp hơn cho miền rộng (PSI(WT) ≤ 4,0). Dùng xác suất để **xếp thứ tự** thì không ảnh hưởng (hàm đơn điệu); dùng như giá trị tuyệt đối thì phải nhớ độ thiên này.

`[ĐO]` Hai ghi chú về ECE: (i) tần suất nền `const` có ECE 0,0154, cỡ platt, nên ECE đơn lẻ không chứng minh kỹ năng — phải đọc cùng Brier và reliability; (ii) ECE bootstrap có thiên lệch dương nhỏ (ECE điểm 0,0044 nằm dưới cận dưới CI [0,0045; 0,0187] của bản theo miền).

## 4. Tiện ích xếp hạng (G3) `[ĐO]`

Xếp 19 × 28 thay thế của từng peptide theo điểm thô ensemble, lấy top-k%. Macro theo 91 peptide có cả ô dương lẫn ô âm; CI theo cụm; ngẫu nhiên có enrichment = 1.

| k | ô/peptide | Precision | Recall | **Enrichment** | CI 95% enrichment |
|---:|---:|---:|---:|---:|---|
| 5% | 27 | 0,551 | 0,241 | **4,75** | [4,23; 5,28] |
| **10%** | 54 | 0,466 | 0,407 | **4,02** | **[3,70; 4,35]** |
| 20% | 107 | 0,371 | 0,611 | **3,04** | [2,86; 3,21] |

**Tiêu chí "có làm giàu"** (CI enrichment@10% > 1): **đạt**. Enrichment theo từng seed ổn định (4,02 / 4,01 / 4,02 ở top-10%).

`[DIỄN GIẢI]` Đọc thực dụng: nếu chỉ thử nghiệm 54 đột biến có điểm cao nhất mỗi peptide 28-mer (10% trong 532), khoảng **47%** là ô dương thật và bắt được **41%** tổng ô dương, so với 13% khi chọn ngẫu nhiên. Không có chuẩn so sánh nào khác ngoài ngẫu nhiên được tiền đăng ký, nên con số này **không** cho biết mô hình hơn một quy tắc đơn giản (ví dụ ưu tiên đột biến sang acid amin kỵ nước) bao nhiêu; câu đó chưa được đo ở đây.

## 5. Nguyên mẫu G3 tối giản (offline) `[ĐO]`

[predict.py](predict.py) — CLI Python chỉ cần numpy, mô hình đọc từ `data/processed/calibration-p6-model.npz` (dựng bằng [build_model.py](build_model.py), không lên git, sinh lại được). Mô hình: ridge M3 khớp trên toàn bộ **176 peptide / 172 cụm / 92.337 ô** (alpha 10, chọn bằng inner validation theo cụm seed 17) + Platt khớp trên OOF cross-fit toàn pool.

```bash
.venv/bin/python -I topics/degron-footprint/research/calibration-p6-2026-10-22/predict.py \
    --uniprot P60484 --tile 3 --out pten-tile3.csv        # một tile của protein trong snapshot UniProt
... predict.py --uniprot P60484 --all-tiles --out pten.csv  # mọi tile (bước 23 aa, dài 28)
... predict.py --seq <28 acid amin chuẩn>                   # chuỗi tự nhập, ra stdout
```

Ra CSV 532 dòng/tile: `peptide, tile, position, wt_aa, mut_aa, score_dpsi_raw, p_dpsi_ge_1_calibrated, rank_in_tile, top10pct_in_tile`. Mẫu: [example-output.csv](example-output.csv) (tile của `A6NMZ7_28`, một peptide **có trong train** của nguyên mẫu, chỉ để minh họa định dạng). Luôn in cảnh báo phạm vi ra stderr.

### Kiểm khớp với runner (`verify.py`, [verify.json](verify.json)) `[ĐO]`

| Phép đối chiếu | Max \|Δ\| |
|---|---:|
| `nhãn y`: `load_all` vs cache | 0 |
| Đặc trưng 180 chiều dựng độc lập trong `predict.py` vs cache X (92.337 ô) | 1,1e-16 |
| Điểm thô qua `predict.py` vs `Ridge.predict` (92.337 ô) | 4,4e-16 |
| Xác suất platt / iso qua `predict.py` vs sklearn | 3,3e-16 / 1,7e-13 |
| Đường UniProt → tile → `predict_tile` vs đường huấn luyện, **mọi** ô của 176 peptide | 0 |
| Đặc trưng bộ gốc 91 peptide vs cache X0 | 1,1e-16 |
| Điểm outer-test của **cả 15** (seed, fold) tái tạo từ hệ số fold bằng đường `predict` vs `score_by_seed` của runner | 4,4e-16 |
| CSV do CLI ghi vs `predict_tile` (định dạng `%.10g`) | 4,4e-10 (điểm), 4,8e-11 (xác suất) |

Mọi phép < 1e-9. `[ĐO]` Lưu ý nhỏ: dòng CSV được `assert` với dung sai 5e-9 trong code (giới hạn do làm tròn 10 chữ số khi ghi), còn số đo thực tế đều < 1e-9.

`[ĐO]` Phép đặc trưng khớp cache tức `predict.py` **không** dùng `derisk.featurize`: đây là hai cài đặt độc lập cho cùng một đặc trưng, nên phép đối chiếu có nội dung.

## 6. Giới hạn

- `[ĐO]` OOF trên benchmark phát triển, đã khảo sát nhiều lần; xác suất chưa được kiểm trên nhãn ngoài. Không được gọi nguyên mẫu là "đã xác nhận".
- `[ĐO]` Mô hình cuối khớp trên 100% pool còn bộ hiệu chuẩn học từ điểm của mô hình 80% pool (hạn chế cross-fit ghi trước ở PROTOCOL §3); độ lệch này chưa được tách khỏi dịch chuyển miền ở §3.
- `[ĐO]` Miền áp dụng: tile 28-mer nội vùng, hệ GPS của Zhang, peptide có PSI(WT) ≤ 4,0. Nguyên mẫu **không biết** PSI(WT) của tile người dùng nhập; tile bền sẽ vẫn nhận điểm. Cảnh báo in ra nhưng không có cổng chặn.
- `[ĐO]` Chuẩn tiện ích duy nhất là ngẫu nhiên (§4). Không có đối chiếu với PAP/Degformer trên chuẩn này.
- `[DIỄN GIẢI]` Nhãn "đã hiệu chuẩn" ở đây nghĩa là **Brier tốt hơn điểm thô có CI > 0**, đúng tiêu chí P6; nó không có nghĩa là hiệu chuẩn hoàn hảo (xem §3: thiên thấp ở miền gốc).
- `[ĐO]` Không dùng Koren 2018 hay nguồn chưa có quyền ở bất kỳ bước nào. Chưa có web UI.

## 7. Dựng lại

```bash
export OPENBLAS_NUM_THREADS=2
D=topics/degron-footprint/research/calibration-p6-2026-10-22
.venv/bin/python -I $D/run_calibration.py   # ~1 phút, RAM ~1 GB; cần cache learning-curve-sat-{base,ext4.0}.npz
.venv/bin/python -I $D/build_model.py        # ghi calibration-p6-model.npz / -trainpath.npz
.venv/bin/python -I $D/verify.py             # nạp lại toàn bộ bộ bão hòa; RAM ~1,2 GB
```

Lineage file sinh ra: [data/README](../../data/README.md). Cả ba NPZ bị gitignore.
