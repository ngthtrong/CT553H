# Tiền đăng ký — P3: tiền huấn luyện nhãn mức tile (Voutsinos) rồi tinh chỉnh ΔPSI

Chốt **trước khi chạy runner**, ngày 22/10/2026. Kế hoạch gốc: [next-steps-plan P3](../next-steps-plan-2026-10-22/README.md). Sau khi chạy, README chỉ **báo kết quả**, không sửa tiêu chí ở file này. Không đổi trạng thái G2/G3, không sửa đề cương hay slide.

Trước khi chốt, chỉ xem **phân bố biên của nhãn tile** (độ dài, `n`, `degron_score`, `degron_std`; 212.658 tile / ~5.300 gene) và độ nhất quán chồng lấn giữa tile liền kề. **Chưa** chạy bất kỳ mô hình nào lên outer-test.

## 1. Câu hỏi

Nhãn tile của Voutsinos 2026 (sort-seq, 30-mer, **khác assay** với GPS-PSI của Zhang) có thể dùng làm giám sát yếu để khởi tạo mạng `gate_no_pap` trước khi tinh chỉnh trên ΔPSI bão hòa, và việc đó có tạo lợi ích **ổn định** so với (a) cùng mạng khởi tạo ngẫu nhiên và (b) ridge M3 hay không?

## 2. Bất biến (giữ nguyên từ G2 / [learning-curve](../learning-curve-2026-10-22/PROTOCOL.md))

- Nhãn ΔPSI, ô dương ΔPSI ≥ 1,0, AUROC mức ô macro theo peptide, đặc trưng M3 180 chiều, seed **17, 29, 43**, bootstrap **5.000 lần theo cụm** protein, ghép cặp.
- Outer-test = đúng ô của bộ 91 peptide gốc, 5 fold `GroupKFold(5)` cov80; cổng tự kiểm danh sách cụm test trùng `folds` của G2 (dùng lại `run_curve.build` + `assert`).
- **Hai cấu hình huấn luyện, báo cả hai:**
  - **Chính:** *ext 4,0* (train = 91 gốc + 85 peptide nới ngưỡng, bỏ cụm test từng fold) — cấu hình huấn luyện chính của đề tài sau P0.
  - **Phụ:** *base 3,0* (train = 91 gốc).
- Mọi chọn siêu tham số, chuẩn hóa nhãn tile, dừng sớm chỉ trên dữ liệu **ngoài outer-test**.

## 3. Nguồn tiền huấn luyện và chống rò rỉ

- Nguồn: `data/raw/voutsinos-2026/repo/score/degrons.csv.gz` (MIT). Giữ tile có `name` dạng `ENSG…_tile####`, `aa` dài đúng 30, chỉ 20 acid amin chuẩn. Bỏ dòng điều khiển (`_APPY_WT_…`) và tile có ký tự lạ.
- Nhãn tile: **y = −`degron_score`** (đảo dấu để cùng chiều "ổn định hơn ⇒ cao hơn" với PSI), chuẩn hóa z-score trên tập tiền huấn luyện của fold đó. Mọi tile trọng số bằng nhau.
- **Loại trước mọi bước học, riêng từng outer fold:** tile của gene `g` bị loại khỏi nguồn tiền huấn luyện của fold `f` nếu **bất kỳ** điều nào sau đây đúng với một protein thuộc các cụm cov80 **outer-test** của fold `f`:
  1. **Tương đồng trình tự (chính):** MMseqs2 `easy-search` giữa trình tự gene dựng lại từ các tile liền kề (đoạn chồng 15 aa) và các protein thành viên của cụm test, `--min-seq-id 0,30 -e 1e-3`, giữ hit có `alnlen ≥ 50`. Không đặt ngưỡng phủ nên **chặt hơn** định nghĩa cụm id30/cov80 (cố ý, thiên về an toàn).
  2. **Trùng 12-mer** giữa trình tự tile 30-mer và protein thành viên cụm test.
  3. **Trùng tên gene** (`Gene name` biomart ⇄ `GN=` UniProt) với protein thành viên cụm test.
- Loại **cả gene** (mọi tile), không chỉ tile trùng. Số tile/gene bị loại từng fold ghi vào `results.json`.
- Cụm test của *mọi* fold chỉ chứa protein thuộc bộ 91 peptide gốc; peptide nới ngưỡng không tạo thêm cụm test.

## 4. Mô hình và hai nhánh so sánh

- Encoder: đúng class `Gate` của `run_curve.py` (gate sigmoid, `pair` 40→32, `context` 140→32, head 64→32→1), **không đổi kiến trúc**.
- **Tiền huấn luyện** (mỗi fold × mỗi seed, dùng chung cho cả hai cấu hình huấn luyện vì nguồn tile chỉ phụ thuộc fold): mỗi tile 30-mer thành 30 hàng M3 180 chiều ở chế độ chỉ-hoang-dã — `wt` = one-hot residue tại vị trí, `mut` = 0, `comp` = thành phần của cả tile, `ctx` = ±3 láng giềng có thứ tự (đệm 0 ngoài biên) — đúng bố cục `derisk.featurize`. Dự đoán tile = **trung bình** đầu ra `Gate` trên 30 vị trí; loss MSE với y chuẩn hóa. AdamW lr 2×10⁻³, weight decay 0,01, batch 256 tile, tối đa 10 epoch, dừng sớm kiên nhẫn 2 trên 10% gene giữ riêng (chia theo gene theo seed). Khởi tạo trọng số = khởi tạo của seed đó (`torch.manual_seed(seed)` rồi `Gate()`), nên nhánh ngẫu nhiên và nhánh tiền huấn luyện **bắt đầu từ cùng điểm**.
- Cột `mut` của lớp `pair` không nhận gradient khi tiền huấn luyện; sau tiền huấn luyện **khôi phục** chúng về giá trị khởi tạo của seed (để chúng không bị weight decay làm lệch).
- **Tinh chỉnh** (cả hai nhánh giống hệt): đúng `neural()` của `run_curve.py` (AdamW wd 0,01, batch ≈1.024, tối đa 60 epoch, kiên nhẫn 8, dừng sớm theo MSE inner validation chia theo cụm), **lưới lr ∈ {2×10⁻³, 5×10⁻⁴} chọn bằng MSE inner validation** — cùng lưới, cùng dữ liệu, cùng thứ tự batch cho hai nhánh. Chỉ khác trạng thái ban đầu.
- Ba nhánh: `rand` (khởi tạo ngẫu nhiên, = `gate_no_pap`), `pre` (khởi tạo từ tiền huấn luyện), `ridge` (M3, `run_curve.ridge`, inner chọn alpha) tính lại trên **cùng** phép chia train/val/test.

## 5. Cổng tự kiểm (dừng nếu trượt)

1. Folds trùng G2 (như learning-curve).
2. Nhánh `rand` **ở lr = 2×10⁻³**, ensemble ba seed: AUROC phải trùng **0,8015 (base)** và **0,8154 (ext)** của [learning-curve results.json](../learning-curve-2026-10-22/results.json) trong sai số 5×10⁻⁴; ridge phải ra **0,8082 / 0,8208** trong 5×10⁻⁴. Lệch → không báo kết quả P3, chỉ báo lỗi.
3. Với mỗi fold: không tile tiền huấn luyện nào có gene trong tập bị loại; ghi `assert`.

## 6. Tiêu chí quyết định, chốt trước

Hai phép so ghép cặp theo cụm trên AUROC từng peptide (bootstrap 5.000 lần), mỗi phép tính trên điểm ensemble ba seed (CI) và trên từng seed riêng (dấu).

| | Phép so | Tiêu chí |
|---|---|---|
| **A** (quy cho tiền huấn luyện) | `pre` − `rand` | CI 95% dưới > 0 **và** delta > 0 ở cả ba seed |
| **B** (tiêu chí của kế hoạch P3) | `pre` − `ridge` M3 | CI 95% dưới > 0 **và** delta > 0 ở cả ba seed |

Kết luận ánh xạ trước, ở **cấu hình chính (ext 4,0)**:

- A đạt và B đạt → **"Nhận"**: tiền huấn luyện nhãn tile tạo lợi ích ổn định và đưa mạng vượt M3.
- A đạt, B không → **"Giúp mạng nhưng chưa vượt M3"**. Không dùng để mở lại câu hỏi kiến trúc.
- A không đạt (bất kể B) → **"Chưa đủ bằng chứng cho lợi ích của tiền huấn luyện"**. Nếu CI của A phủ 0 thì ghi rõ "không phân biệt được với khởi tạo ngẫu nhiên".
- Cấu hình phụ (base 3,0) báo với cùng tiêu chí để xem tính nhất quán; **không** dùng để chọn cấu hình chính.

Báo thêm (mô tả, **không** quyết định): AUROC từng nhánh/từng seed, lr được chọn, epoch dừng, Pearson trên 10% gene giữ riêng khi tiền huấn luyện, số tile/gene bị loại từng fold.

## 7. Dự đoán tiền đăng ký

`[ĐỀ XUẤT]` Dự đoán ban đầu: **A sẽ không đạt** (CI phủ 0). Lý do: (i) nhãn tile là assay khác, mức tile chứ không mức đột biến, nên tiền huấn luyện chỉ dạy mạng phân bố "residue ở ngữ cảnh nào gắn với degron" mà không dạy chiều của một phép thay; (ii) [learning-curve](../learning-curve-2026-10-22/README.md) cho thấy mạng đã gần tiệm cận của mình ở ext 4,0 (0,8154 so với ridge 0,8208); (iii) [cross-assay gap](../reframe-options-2026-10-15/README.md) §9 đo khoảng cách qua assay 0,0773 AUROC. Nếu dự đoán sai theo chiều A đạt, vẫn đọc theo bảng ở §6 chứ không phóng đại.

## 8. Giới hạn đã biết trước

- Benchmark phát triển OOF, không phải kiểm chứng ngoài độc lập.
- Tiền huấn luyện chỉ chạm lớp `Gate`, không chạm đặc trưng; chế độ chỉ-hoang-dã (`mut`=0) khiến tiền huấn luyện **không** học nhãn của phép thay. Đây là giới hạn của thiết kế, không phải của ý tưởng giám sát yếu nói chung.
- Loại tương đồng ở mức local hit `alnlen ≥ 50`, id ≥ 30% chặt hơn cụm cov80; có thể loại cả họ paralog. Số gene bị loại sẽ được báo.
- Hai lr trong lưới là lựa chọn của người viết, không phải kết quả tìm kiếm rộng.

## 9. Chạy

```bash
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/pretrain-p3-2026-10-22/build_exclusion.py
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I topics/degron-footprint/research/pretrain-p3-2026-10-22/run_p3.py
```

Tối đa 4 thread torch; RAM ≤ 2,5 GB.
