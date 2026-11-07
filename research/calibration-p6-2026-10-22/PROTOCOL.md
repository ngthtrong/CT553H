# Tiền đăng ký — hiệu chuẩn điểm (P6) và nguyên mẫu G3 tối giản

Chốt **trước khi chạy**, ngày 22/10/2026. Kế hoạch gốc: [next-steps-plan-2026-10-22](../next-steps-plan-2026-10-22/README.md) §2, dòng P6. Sau khi chạy, README chỉ **báo kết quả**, không sửa tiêu chí ở file này. Không đổi trạng thái G2/G3, không sửa đề cương hay slide.

## 1. Câu hỏi

1. Điểm ridge M3 (cấu hình huấn luyện chính: nới ngưỡng degron 4,0) có thể chuyển thành **xác suất ô dương** `P(ΔPSI ≥ 1,0)` đủ tin cậy để ưu tiên đột biến không? Tức: hiệu chuẩn có làm **Brier** giảm so với điểm thô, với CI theo cụm > 0?
2. Khi dùng điểm để **xếp hạng** đột biến trong từng peptide (top-k%), mô hình làm giàu ô dương hơn ngẫu nhiên bao nhiêu? Đây là tiện ích thực tế của G3.
3. Nguyên mẫu offline có tái tính **đúng bằng** runner không?

## 2. Mô hình cố định và dữ liệu (không thay đổi)

- Mô hình: **ridge M3** (180 chiều), tái dùng nguyên `run_curve.build`/`run_curve.ridge` của [learning-curve-2026-10-22](../learning-curve-2026-10-22/run_curve.py), mức `ext` (train = cụm trong outer-train của bộ 91 peptide + 85 peptide nới ngưỡng 4,0, đã loại cụm test từng fold).
- Outer-test = đúng 47.847 ô của bộ 91 peptide / 89 cụm cov80, 5 fold `GroupKFold(5)` trùng G2; seed 17/29/43.
- **Cổng tự kiểm:** macro-AUROC từng seed của điểm thô tái tạo phải bằng `results.json` (ridge, `ext`, `macro_auroc_per_seed`) sai lệch < 1e-9. Lệch → dừng, không báo kết quả.
- Không dùng nhãn từ nguồn không có giấy phép mở (Koren 2018 và các nguồn khác chưa qua cổng quyền) ở bất kỳ bước nào của thí nghiệm hay nguyên mẫu.

## 3. Hiệu chuẩn, chốt trước

Mục tiêu nhãn nhị phân `y = 1[ΔPSI ≥ 1,0]` (`RESCUE_DELTA` giữ nguyên).

**Cross-fit trong outer-train.** Với mỗi (seed, outer fold): pool huấn luyện của mức `ext` được chia lại thành 5 inner fold **theo cụm** (cụm xếp ngẫu nhiên bằng `default_rng(seed*1000+fold+7)` rồi gán vòng tròn). Với mỗi inner fold, ridge được khớp trên 4 phần với **alpha đã chọn ở bước chính** (chọn bằng inner validation theo cụm, không bao giờ xem outer-test), dự đoán phần còn lại. Điểm out-of-fold (OOF) của toàn pool là dữ liệu duy nhất để khớp bộ hiệu chuẩn. Outer-test không bao giờ xuất hiện trong khớp hiệu chuẩn.

`[ĐỀ XUẤT]` Giới hạn đã biết, ghi trước: mô hình cuối (khớp trên 100% pool) thấy nhiều dữ liệu hơn mô hình inner (80% pool), nên điểm thật có thể hơi tự tin hơn điểm OOF. Chấp nhận như hạn chế chuẩn của cross-fit; không chỉnh.

Ba cách chuyển điểm thành xác suất, **chỉ ba, không thêm**:

| Ký hiệu | Định nghĩa |
|---|---|
| **raw** | `clip(điểm / 1,0; 0; 1)` — đọc điểm ΔPSI dự đoán như phần đường tới ngưỡng dương. Đây là "điểm thô" của tiêu chí P6. |
| **platt** | `LogisticRegression(C=1e4)` một biến (điểm), khớp trên OOF của pool. **Bộ hiệu chuẩn chính** (đơn giản, 2 tham số). |
| **iso** | `IsotonicRegression(y_min=0, y_max=1, out_of_bounds='clip')`, khớp trên OOF của pool. |
| **const** | tần suất ô dương của pool (mốc tham chiếu cho kỹ năng Brier, không phải bộ hiệu chuẩn) |

Độ nhạy (báo, **không** dùng cho phán quyết): khớp bộ hiệu chuẩn chỉ trên các ô thuộc 91 peptide gốc trong pool ("khớp theo miền"), thay vì toàn pool.

Tổng hợp qua seed: điểm thô = trung bình điểm ba seed rồi clip (trùng ensemble của `run_curve`); xác suất hiệu chuẩn = trung bình xác suất ba seed; const = trung bình ba hằng.

## 4. Chỉ số trên outer-test

Tất cả tính trên ô, gộp 5 fold; **CI 95% bằng bootstrap 5.000 lần theo cụm cov80** (rút 89 cụm có hoàn lại, giữ mọi peptide/ô của cụm), seed bootstrap 20261022.

- **Brier** của raw / platt / iso / const; **kỹ năng Brier** `BSS = 1 − Brier(c)/Brier(const)`.
- **ECE** 10 thùng cùng khối lượng (phân vị của chính phương pháp trên toàn outer-test; thùng cố định khi bootstrap), hiệu chuẩn cục bộ: báo thêm intercept và slope của hồi quy logistic `logit(P) ~ a + b·logit(p̂)` (mô tả).
- **Biểu đồ độ tin cậy (reliability)** 10 thùng: `p̂` trung bình, tần suất dương quan sát, số ô, số cụm có mặt.
- **Chuẩn mực tiện ích (xếp hạng):** cho từng peptide, xếp ô theo điểm; lấy top-k% với k ∈ {5, 10, 20} (làm tròn lên, ≥ 1 ô). Với peptide có ít nhất một ô dương và một ô âm: `precision@k`, `recall@k`, `enrichment@k = precision@k / tần suất dương của peptide`. Macro theo peptide, CI theo cụm. Mốc ngẫu nhiên: enrichment = 1.
  Xếp hạng không đổi dưới hiệu chuẩn đơn điệu (platt); iso có thể tạo hạng đồng; tiện ích báo trên **điểm thô**, và macro-AUROC của xác suất platt/iso báo kèm để thấy iso có phá hạng không.

## 5. Tiêu chí kết luận, chốt trước

**"Đã hiệu chuẩn" (cho bộ hiệu chuẩn c ∈ {platt, iso})** khi *cả hai*:

- (a) CI95 theo cụm của `Brier(raw) − Brier(c)` **> 0** trên ensemble;
- (b) `Brier(raw) − Brier(c) > 0` ở **cả ba seed** tính riêng.

Không đạt (a) hoặc (b) → ghi "**chưa đủ bằng chứng là đã hiệu chuẩn**"; không dùng nhãn "đã hiệu chuẩn" cho điểm ở nguyên mẫu, hiển thị điểm thô kèm cảnh báo.

**Giá trị so với tần suất nền (nhãn riêng, độc lập với trên):** `Brier(const) − Brier(c)` CI95 > 0 → "xác suất có kỹ năng hơn tần suất nền"; ngược lại → "hiệu chuẩn nhưng không có kỹ năng hơn tần suất nền". Một điểm hiệu chuẩn tốt hơn điểm thô chưa chắc có ích; đây là phép tách hai phát biểu.

**Chọn bộ hiệu chuẩn cho nguyên mẫu:** dùng `platt`, trừ khi `Brier(platt) − Brier(iso)` có CI95 > 0 theo cụm (iso tốt hơn rõ), khi đó dùng `iso`.

**Tiện ích xếp hạng:** "có làm giàu" khi CI95 theo cụm của `enrichment@10%` **> 1**. Con số cụ thể là mô tả, không có ngưỡng thành công khác.

## 6. Dự đoán đã ghi trước khi chạy

`[ĐỀ XUẤT]`

1. platt giảm Brier so với raw với CI > 0 ở cả ba seed (raw là cách chuyển điểm hồi quy → xác suất rất thô, gần như chắc chắn lệch).
2. platt có kỹ năng Brier dương so với const nhưng **nhỏ** (BSS cỡ 0,05–0,20), vì AUROC macro ≈ 0,82 trên tỉ lệ dương ≈ 13%.
3. iso ≈ platt, chênh Brier dưới 0,002, CI phủ 0.
4. enrichment@10% cỡ 3–5, CI > 1.
5. ECE sau hiệu chuẩn nhỏ (< 0,02) nhưng reliability ở thùng cao nhất ít ô, CI rộng.

## 7. Nguyên mẫu G3 tối giản

- CLI Python offline `predict.py`: nhập chuỗi 28-mer (`--seq`) hoặc UniProt ID + chỉ số tile (`--uniprot`, `--tile`, hoặc mọi tile) lấy từ snapshot UniProt cache `data/raw/human-reviewed-2026-10-12.fasta.gz`; trả CSV mọi thay thế (28 vị trí × 19) với điểm thô, xác suất hiệu chuẩn, hạng trong peptide.
- Mô hình của nguyên mẫu: ridge M3 khớp trên **toàn bộ 176 peptide** của mức `ext`, alpha chọn bằng inner validation theo cụm (seed 17), bộ hiệu chuẩn theo §5 khớp trên OOF cross-fit toàn bộ cụm. Mô hình **sinh lại được** bằng `build_model.py`; file mô hình không lên git.
- **Kiểm khớp (bắt buộc):** `verify.py` tái tính điểm thô và xác suất qua đường `predict.py` (từ chuỗi) cho mọi ô của 176 peptide và so với đường huấn luyện (ma trận đặc trưng cache + `Ridge.predict` + bộ hiệu chuẩn); chênh lệch tuyệt đối tối đa phải **< 1e-9**. Thêm: các điểm outer-test của một fold chọn tái tạo từ mô hình fold phải khớp điểm trong runner.
- Nguyên mẫu **luôn in cảnh báo**: huấn luyện chỉ trên Zhang 2023 (thư viện GPS 28-mer nội vùng, PSI 1–6), miền peptide có PSI(WT) ≤ 4,0; xác suất không dùng được cho peptide bền hay hệ đo khác; không có Koren.
- Chưa làm giao diện web.

## 8. Việc không làm

- Không thêm mô hình, không đổi ngưỡng, không đổi chỉ số hay `RESCUE_DELTA`, không chọn lại bộ hiệu chuẩn sau khi thấy kết quả.
- Không gọi kết quả là xác nhận ngoài: đây vẫn là OOF trên benchmark phát triển.
- Không nhập nguồn ngoài chưa có quyền; không sửa slide.
