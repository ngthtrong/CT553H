# Độ nhạy theo độ mịn phân cụm của lợi ích P0 — 22/10/2026

Tiêu chí chốt **trước khi chạy** ở [PROTOCOL.md](PROTOCOL.md). Kết quả: [results.json](results.json) (runner [run.py](run.py)), phân hoạch phân cụm mới [cluster.py](cluster.py) → [cluster-manifest.json](cluster-manifest.json), kiểm trùng phân hoạch [partition_equivalence.py](partition_equivalence.py) → [partition-equivalence.json](partition-equivalence.json). Không đổi trạng thái G2/G3, không sửa đề cương hay slide.

**[ĐO] Kết quả một dòng.** Lợi ích P0 (ridge M3, nới ngưỡng degron lên 4,0, test giữ 91 peptide gốc) **giữ CI > 0 và dương ở cả ba seed trên cả 3 phân hoạch khác thật** (mịn hơn: theo accession; thô hơn: hai mức phân cụm), delta từ **+0,0096 đến +0,0166**. Theo PROTOCOL §5: **"Lợi ích P0 bền theo độ mịn"**.

## 1. Cổng tự kiểm đã qua

- `[ĐO]` L1 (id 0,3 · cov 0,8) tái lập base **0,8082** và ext **0,8208**, và 5 fold trùng `folds` của G2. Runner `assert` điều kiện này (PROTOCOL §4).
- `[ĐO]` Phân cụm mới chạy cùng đầu vào `proteins-full.fasta` (6.573 protein, SHA-256 trong manifest) và cùng cờ MMseqs2 như bản gốc, chỉ đổi `--min-seq-id` và `-c`. Cờ `--split-memory-limit` phải nâng từ 1G lên 1500M vì bản 1G dừng với lỗi "Cannot fit databases into 1023M"; đây không đổi kết quả phân cụm.

## 2. Phân hoạch: bảy mức nhưng chỉ có bốn phân hoạch riêng biệt `[ĐO]`

Đây là điều đầu tiên cần nói: lưới 7 mức chốt trước **không** cho 7 phân hoạch khác nhau.

| Phân hoạch riêng biệt | Mức cho cùng phân hoạch | Nhóm trên 91 base | Nhóm trên 176 (base+ext) |
|---|---|---:|---:|
| P-acc | L0 | 91 | 176 |
| P-80 | L1, L2 | 89 | 172 |
| P-mid | L3, L4 | 87 | 163 |
| P-coarse | L5, L6 | 71 | 133 |

`[ĐO]` Hạ `--min-seq-id` từ 0,2 xuống 0,1 (L3 → L4) và từ 0,1 xuống 0,0 (L5 → L6) **không đổi một nhóm nào** trên 176 peptide ([partition-equivalence.json](partition-equivalence.json)). Số cụm toàn proteome khác nhau chút ít (L3 3.823 so với L4 3.810; L5 và L6 đều 3.038), nhưng các chênh lệch đó không chạm 176 peptide đang xét.

`[DIỄN GIẢI]` Độ phủ (`-c`) và e-value mặc định quyết định phân hoạch ở vùng này; ngưỡng identity dưới 0,2 gần như không có tác dụng thêm. Vì vậy số mức **khác thật** là **ba** (P-acc, P-mid, P-coarse), không phải năm như bảng ở PROTOCOL. Bảng kết quả dưới vẫn báo đủ cả bảy mức, nhưng cặp trùng nhau chỉ đếm một lần khi nói về độ vững.

## 3. Kết quả P0 theo từng mức `[ĐO]`

Ridge M3, AUROC macro theo peptide, điểm OOF gộp ba seed. Delta = ext − base, CI 95% bootstrap 5.000 lần theo nhóm **của mức đó**.

| Mức | Phân hoạch | Base | Ext | **Delta** | CI 95% | Delta từng seed | Cả 3 seed dương |
|---|---|---:|---:|---:|---|---|:--:|
| L0 | P-acc | 0,8036 | 0,8202 | **+0,0166** | [+0,0099; +0,0240] | +0,0236 · +0,0146 · +0,0176 | Có |
| L1 | P-80 (tham chiếu) | 0,8082 | 0,8208 | **+0,0126** | [+0,0061; +0,0190] | +0,0142 · +0,0142 · +0,0128 | Có |
| L2 | P-80 (fold chia khác) | 0,8116 | 0,8212 | **+0,0096** | [+0,0032; +0,0159] | +0,0099 · +0,0104 · +0,0091 | Có |
| L3 | P-mid | 0,8051 | 0,8185 | **+0,0134** | [+0,0074; +0,0199] | +0,0135 · +0,0220 · +0,0099 | Có |
| L4 | P-mid | 0,8051 | 0,8185 | **+0,0134** | [+0,0074; +0,0199] | +0,0135 · +0,0220 · +0,0099 | Có |
| L5 | P-coarse | 0,8096 | 0,8209 | **+0,0113** | [+0,0037; +0,0184] | +0,0070 · +0,0126 · +0,0173 | Có |
| L6 | P-coarse | 0,8096 | 0,8209 | **+0,0113** | [+0,0037; +0,0184] | +0,0070 · +0,0126 · +0,0173 | Có |

`[ĐO]` L2 có đúng phân hoạch của L1 trên 176 peptide nhưng cho số khác (base 0,8116) vì `GroupKFold` xếp cụm theo nhãn đại diện nên 5 fold bị gán lại; kết quả này là con số "cov50" đã báo ở [learning-curve §4c](../learning-curve-2026-10-22/README.md) và được dựng lại ở đây. L3 = L4 và L5 = L6 giống nhau đến chữ số cuối vì phân hoạch giống nhau và mọi thứ khác cố định.

## 4. Rò rỉ tiềm ẩn: peptide ext cùng nhóm với test `[ĐO]`

Peptide ext (85) cùng nhóm với test của một fold bị loại khỏi train của fold đó (và loại luôn các peptide base cùng nhóm, vốn đã nằm trong test). Số liệu theo fold 0–4:

| Phân hoạch | Ext chung nhóm với **bất kỳ** peptide base | Peptide ext bị loại theo fold | Ô ext bị loại theo fold | Tỉ lệ ô ext bị loại (TB) |
|---|---:|---|---|---:|
| P-acc | 0 | 0 · 0 · 0 · 0 · 0 | 0 | 0,0% |
| P-80 | 2 | 1 · 0 · 0 · 1 · 0 | 531 · 0 · 0 · 532 · 0 | 0,5% |
| P-mid | 6 | 3 · 1 · 0 · 0 · 2 | 1.594 · 532 · 0 · 0 · 1.061 | 1,4% |
| P-coarse | 22 | 18 · 1 · 3 · 0 · 0 | 9.517 · 532 · 1.527 · 0 · 0 | 5,2% |

`[DIỄN GIẢI]` Phân cụm càng thô thì càng nhiều peptide ext bị coi là "họ hàng" của test và bị loại, nhưng ngay ở mức thô nhất vẫn chỉ mất 5,2% ô ext. Mọi mức đều "còn thông tin" theo ngưỡng 50% đã chốt. Lợi ích của P0 **không** đến từ việc ext lẻn vào train các protein tương đồng với test, vì khi gom nhóm thô hơn để ngăn việc đó, lợi ích vẫn ở lại.

## 5. Kết luận theo PROTOCOL §5

`[ĐO]` Các mức khác L1 thật và còn thông tin: L0, L3, L4, L5, L6. Cả năm đều CI95 > 0 và cả ba seed dương, nên **"Lợi ích P0 bền theo độ mịn"**. Không mức nào bị loại vì hết thông tin.

`[DIỄN GIẢI]` Cách đọc đúng của kết luận này: *vị trí* của lợi ích (dương, ~0,01–0,017) không nhạy với độ mịn phân cụm trong dải đã kiểm. Nó **không** nói lợi ích bằng nhau ở mọi mức: delta dao động từ +0,0096 đến +0,0166, nhưng CI của các mức chồng nhau nhiều và không có phép kiểm nào về hiệu giữa hai mức.

## 6. Giới hạn

- `[ĐO]` Chỉ có **ba** phân hoạch khác L1 thật, và phân hoạch thô nhất vẫn còn 71 nhóm trên 91 base. Không thử được "cực thô" (vài chục nhóm) vì lưới identity/coverage chốt trước không đẩy xa hơn; đi tiếp cần đổi chiến lược gom (ví dụ theo họ domain Pfam) và sẽ là một thí nghiệm khác.
- `[ĐO]` Ở P-coarse, fold 0 có **một** nhóm test duy nhất: cụm đại diện Q9NQZ8 gom **20 trong 91** peptide base (10.141 ô), và 18 peptide ext (9.517 ô) phải loại khỏi train của fold đó. Số liệu fold đó nhạy với cách cụm lớn đó rơi vào train/test; CI theo nhóm phản ánh điều này (rộng hơn ở L5/L6).
- `[ĐO]` Mức L2 không phải phép kiểm độ mịn (cùng phân hoạch với L1); chỉ là phép chia lại fold, như đã ghi ở learning-curve §4c. Không đếm L2 vào số mức "khác thật".
- `[ĐO]` Không điều chỉnh đa so sánh cho bảy CI; mỗi CI là 95% riêng. Điều kiện kết luận ("mọi mức CI > 0") đã tự chặt hơn một CI đơn, nhưng đây vẫn không phải một phép kiểm giả thuyết.
- `[ĐO]` Benchmark phát triển OOF, **không** phải kiểm chứng ngoài độc lập. Chỉ ridge M3; không chạy `gate_no_pap` ở thí nghiệm này (PROTOCOL §3).
- `[ĐO]` Chỉ ngưỡng degron 4,0 (cấu hình chính đã chốt ở phần A của learning-curve), không quét lại lưới ngưỡng.
- `[DIỄN GIẢI]` Kết quả này khép được câu hỏi "độ nhạy theo độ mịn phân cụm" của [learning-curve §5](../learning-curve-2026-10-22/README.md) **cho ridge ở ngưỡng 4,0** trong dải phân hoạch đã nêu; nó không khép các giới hạn khác của phần đó (tách "vùng PSI(WT)" khỏi "protein khác").

## 7. Dựng lại

```bash
.venv/bin/python -I topics/degron-footprint/research/recluster-sensitivity-2026-10-22/cluster.py            # ~35 phút CPU, 2 thread, ≤1,1 GB RAM
OPENBLAS_NUM_THREADS=2 .venv/bin/python -I \
  topics/degron-footprint/research/recluster-sensitivity-2026-10-22/run.py                                 # ~6 phút
.venv/bin/python -I topics/degron-footprint/research/recluster-sensitivity-2026-10-22/partition_equivalence.py
```

`cluster.py` ghi vào `data/interim/recluster-sensitivity/` (32 MB, gitignore, sinh lại được); `run.py` đọc lại hai cache `learning-curve-sat-{base,ext4.0}.npz` (cần phần A của learning-curve đã chạy) và dừng nếu cổng L1 không đạt. Truyền một danh sách mã mức làm đối số (ví dụ `run.py L1,L3`) chỉ để thử nhanh và **không** ghi `results.json`.
