# PROTOCOL — kiểm độ mịn phân cụm thật cho lợi ích P0 (22/10/2026)

**Chốt trước khi chạy.** Lưới phân cụm, tiêu chí và quy tắc xử lý dưới đây được viết trước khi chạy bất kỳ mô hình nào trên phân hoạch mới. Bước đếm số cụm là mô tả, không dùng để sửa lưới.

## 1. Câu hỏi

[learning-curve §4c C2 và §5](../learning-curve-2026-10-22/README.md): cov50 và cov80 cho **cùng một phân hoạch** trên 91 peptide base (89 cụm) và trên base + 85 peptide (ngưỡng 4,0; 172 cụm), nên dòng "cov50" không kiểm được độ nhạy theo độ mịn phân cụm. Câu hỏi ở đây: lợi ích +0,0126 của P0 (ridge M3, train mở rộng lên 4,0, test giữ 91 peptide gốc) có còn khi phân hoạch protein **khác thật** không, cả mịn hơn lẫn thô hơn?

## 2. Lưới phân hoạch (cố định, 7 mức)

Mọi mức dùng cùng tập protein đầu vào `data/processed/proteins-full.fasta` (6.573 protein), cùng cờ MMseqs2 như bản gốc (`--cov-mode 0 --seq-id-mode 0 --alignment-mode 3 --cluster-mode 1 --single-step-clustering 1 -s 7.5 --max-seqs 10000`), chỉ đổi `--min-seq-id` (id) và `-c` (cov).

| Mã | Phân hoạch | Nguồn | Vai trò |
|---|---|---|---|
| L0 | mỗi **UniProt accession** là một nhóm (không phân cụm) | tính trực tiếp | mịn nhất; peptide cùng protein vẫn chung nhóm |
| L1 | id 0,3 · cov 0,8 | file có sẵn `protein-id30-cov80_cluster.tsv` | **tham chiếu chính**; phải tái lập 0,8082 / 0,8208 |
| L2 | id 0,3 · cov 0,5 | file có sẵn `protein-id30-cov50_cluster.tsv` | đã biết trùng L1 trên bộ này; chạy lại làm đối chứng |
| L3 | id 0,2 · cov 0,5 | chạy mới | thô hơn một bậc |
| L4 | id 0,1 · cov 0,5 | chạy mới | thô hơn |
| L5 | id 0,1 · cov 0,3 | chạy mới | thô |
| L6 | id 0,0 · cov 0,3 | chạy mới | thô nhất (gom theo tương đồng cục bộ bất kỳ phát hiện được ở ngưỡng e-value mặc định) |

Phân hoạch được tính trên **hợp base ∪ ext4.0** (176 peptide); nhóm của peptide = đại diện cụm của accession cha.

**Quy tắc "khác thật".** Hai phân hoạch được coi là **trùng** khi cùng chia 176 peptide thành đúng cùng các nhóm (so tập con, không so nhãn đại diện). Mức nào trùng với L1 thì ghi "trùng L1", **không** tính vào số mức khác thật, nhưng vẫn báo số liệu.

## 3. Phép đo (mỗi mức)

Cho từng mức, giữ nguyên mọi thứ khác phép so P0 của [run_curve.py](../learning-curve-2026-10-22/run_curve.py):

- Miền test = đúng 47.847 ô của 91 peptide base. Outer fold = `GroupKFold(5)` trên nhóm của mức đang xét (nên fold đổi theo mức).
- Hai cánh: **base** (chỉ nhãn 91 peptide, bỏ peptide cùng nhóm với test) và **ext** (thêm 85 peptide ext4.0, bỏ mọi peptide base lẫn ext cùng nhóm với test trong fold).
- Ridge M3 (180 đặc trưng, α ∈ {1,10,100,1000}), validation trong = `GroupShuffleSplit(0,2)` theo nhóm của mức, seed 17/29/43, điểm OOF trung bình ba seed.
- AUROC macro theo peptide (`dr.macro_auroc`, ô dương khi ΔPSI ≥ 1,0).
- Delta = AUROC(ext) − AUROC(base); CI 95% bằng bootstrap 5.000 lần **theo nhóm của mức đó**, `compare()` của run_curve, seed bootstrap 20261022. Thêm delta theo từng seed.
- Báo cáo kèm: số nhóm trên 91 base và trên 176 hợp; số peptide ext **bị loại khỏi train mỗi fold vì cùng nhóm với test** (rò rỉ tiềm ẩn, tính theo peptide và theo ô); số peptide ext chung nhóm với **bất kỳ** peptide base.

## 4. Cổng tự kiểm

L1 phải tái lập AUROC base **0,8082** và ext **0,8208** (sai lệch ≤ 0,0001) và 5 fold phải trùng `folds` của G2. Không đạt thì dừng và báo lỗi, không đọc tiếp các mức khác.

## 5. Tiêu chí kết luận (chốt trước)

Gọi *mức khác thật* là mức không trùng L1 (mục 2). Gọi mức *còn thông tin* là mức mà trung bình trên 5 fold, ext bị loại vì chung nhóm với test ít hơn 50% số ô ext.

- **"Lợi ích P0 bền theo độ mịn"**: mọi mức khác thật **và** còn thông tin đều có CI95 của delta > 0 **và** delta dương ở cả ba seed.
- **"Bền một phần"**: các mức mịn hơn hoặc bằng một ngưỡng nào đó đạt, các mức thô hơn không đạt hoặc hết thông tin; ghi chính xác ranh giới.
- **"Không bền"**: có một mức khác thật và còn thông tin mà CI95 phủ hoặc dưới 0. Đây là kết quả âm hợp lệ, báo nguyên văn.
- Mức hết thông tin (loại ≥ 50%) không được dùng để ủng hộ hay bác kết luận; chỉ ghi số.

Không chọn lại lưới, không bỏ mức, không đổi ngưỡng 4,0 sau khi thấy số. Benchmark phát triển OOF, không phải kiểm chứng ngoài.

## 6. Ghi chú trung thực trước khi chạy

- Các mức thô gom nhiều protein vào cùng nhóm, nên số nhóm trong bootstrap giảm và CI rộng ra; CI > 0 khó đạt hơn, không phải lỗi.
- L0 (theo accession) mịn hơn L1 nhưng chỉ khác L1 nếu có protein tương đồng trong 176 peptide; có thể trùng L1 về cấu trúc nhóm.
- Phân cụm toàn proteome 6.573 protein dùng cùng đầu vào bản gốc, nên thay đổi nhóm chỉ do `--min-seq-id`/`-c`.
