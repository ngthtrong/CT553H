# R6 — Chuỗi đối chứng biểu diễn × đầu mạng, ngữ cảnh rộng và bộ scanning — 23/10/2026

**Trạng thái: CHƯA CHẠY.** Đã dựng xong dữ liệu, mã, PROTOCOL chốt trước và **một** notebook; chạy do Trọng thực hiện trên Kaggle rồi tải kết quả về. Tới khi có `results.json` từ lượt chạy thật, **không có con số R6 nào** trong repo, và README này không nêu kết quả mạng nào. Ngoại lệ có chủ đích: (1) phép kiểm chéo nguồn mô tả ở mục 1; (2) **kết quả ridge của giai đoạn A và B** ở mục 2, có được vì lượt chạy thử cục bộ vô tình chạy luôn hai giai đoạn này trên dữ liệu thật (PROTOCOL §12) — ridge tất định nên lượt Kaggle phải cho cùng số.

Tiêu chí, họ kiểm định, siêu tham số và dự đoán ghi trước: [PROTOCOL.md](PROTOCOL.md) (SHA-256 nhúng trong notebook). Không đổi trạng thái G2/G3.

## Câu hỏi

Sáu câu (Q1–Q6, PROTOCOL §1; thứ tự chạy 0, A, B, C, D, E, F, G), trong đó **một** phép xác nhận duy nhất: **ESM-2 35M đóng băng + mCNN (3,5,7) có hơn ridge M3 ext 4,0 (0,8208) không?** Các hướng khác là câu hỏi họ có hiệu chỉnh Bonferroni hoặc mô tả:

1. Ridge với ngữ cảnh WT rộng hơn ±3 (A).
2. Trộn bộ **scanning** (4.802 peptide, 2.902 cụm) vào huấn luyện — với ridge (B) và với mạng (G).
3. ESM-2 8M/35M/150M/650M cộng vào ridge (D), và quét cỡ với mCNN (F).
4. One-hot CNN/mCNN (đối chứng cùng đầu) và ESM + CNN/mCNN (E).

## 1. Có trộn được scanning với bão hòa không? — phép kiểm chéo mô tả `[ĐO]`

Ngoài PROTOCOL, trước khi chốt (PROTOCOL §0 ghi rõ điều này). Trên **cùng ô** (peptide, vị trí, acid amin thay) có mặt ở cả hai bộ — 42/88/117 peptide ở ngưỡng PSI(WT) ≤ 3,0/≤ 4,0/không ngưỡng; chỉ có ô thay bằng R/A/S vì scanning chỉ có ba loại này ([cross-source-audit.json](cross-source-audit.json), sinh bởi [cross_source_audit.py](cross_source_audit.py)):

| Ngưỡng PSI(WT) | Ô trùng | Pearson ΔPSI | κ nhị phân (ΔPSI ≥ 1) | AUROC gộp: ΔPSI scanning → ô dương bão hòa | Tham chiếu: nửa A bão hòa → nhãn nửa B (cùng ô) |
|---|---:|---:|---:|---:|---:|
| ≤ 3,0 | 1.172 | 0,79 | 0,75 | 0,947 | 0,950 |
| ≤ 4,0 | 2.449 | 0,74 | 0,69 | 0,922 | 0,966 |
| không ngưỡng | 3.228 | 0,70 | 0,65 | 0,905 | 0,968 |

- `[DIỄN GIẢI]` **Nhãn hai bộ nhất quán trên cùng ô, và thang WT trùng nhau**: ở ngưỡng 3,0 scanning cho thứ hạng ô dương bão hòa tốt ngang một replicate bão hòa khác; chênh PSI(WT) trung bình giữa hai nguồn chỉ −0,01 đến +0,13. Độ nhất quán giảm khi nới vùng PSI(WT), và độ dốc OLS 0,70–0,77 cho thấy scanning (một replicate) nhiễu hơn.
- `[ĐO]` **Đính chính một diễn giải ở [r3-domain-gate/README.md](../r3-domain-gate-2026-10-22/README.md) mục 1:** độ lệch ≈ 0,9 PSI là giữa **sàng peptidome GPS** và (cả bão hòa lẫn scanning `_mut0`), **không** phải giữa scanning và bão hòa. Các con số của R3 không đổi; chỉ câu "bão hòa cao hơn **cả hai** thang kia" là không đúng với thang scanning.
- `[ĐO]` Thách thức còn lại không phải nhãn mà là **độ phủ thay thế**: scanning chỉ có R (64%), A (23%), S (12%), tức 3/19 loại thay thế của ô test; ridge học chỉ trên scanning chuyển sang bão hòa đạt 0,7273 ([residue-task-derisk](../residue-task-derisk-2026-10-15/README.md) §5) so với 0,8082 khi học trực tiếp trên bão hòa.
- `[ĐO]` **Thang WT trùng về trung bình nhưng phân tán theo peptide**: Pearson giữa PSI(WT) hai nguồn chỉ 0,58/0,63/0,79 (≤ 3,0/≤ 4,0/không ngưỡng); audit song song của phiên khác ghi 31% peptide lệch > 0,5 PSI ở mốc WT. Nên ΔPSI scanning là nhãn **cùng tín hiệu, không cùng thang** (độ dốc OLS 0,70–0,77).
- `[ĐO]` **Một phiên khác đã chạy sẵn phép trộn bằng ridge và một mạng** — [scan-sat-merge-2026-10-23](../scan-sat-merge-2026-10-23/PROTOCOL.md), có PROTOCOL riêng chốt trước khi chạy; **tôi không viết và chưa tái lập số của nó** (một tiến trình của phiên đó còn đang chạy lúc tôi đọc). Theo `results.json` ở đó, trên đúng outer-test 91 peptide, mốc A1 = ridge ext 4,0 = 0,8208: chỉ-scanning 0,7277; gộp mù (S1) 0,8189; gộp có khối riêng nguồn (S2) 0,8203 (Δ −0,0005, CI [−0,0009; −0,00004]); tiên nghiệm (S3) 0,8197; mạng `gate_no_pap` từ đầu 0,8154 so với tiền huấn luyện trên scanning 0,8168. **Không biến thể ridge nào hơn A1.**
- `[DIỄN GIẢI]` Câu trả lời cho "có trộn được không": **trộn được về mặt nhãn (không rò, nhãn nhất quán), nhưng với ridge M3 thì không thêm lợi ích đo được**; với mạng mới chỉ có một phép đo nhỏ, chưa phân định. Giai đoạn B của R6 là lặp độc lập rẻ tiền; giai đoạn G (mạng mCNN/ESM + scanning) được đặt **cuối cùng** vì kỳ vọng thấp nhất (PROTOCOL §0). Hàng scanning thuộc cụm outer-test bị loại ở từng fold (**61/89 cụm bão hòa của bộ 91 peptide cũng có trong scanning**, nên điều này loại một phần đáng kể).

## 2. Điều đã thấy trước khi Trọng chạy lượt chính thức (PROTOCOL §12) `[ĐO]`

Nguồn: [dryrun-local-stageAB.json](dryrun-local-stageAB.json) (CPU, 3 seed × 5 fold, đúng mã và tiêu chí của notebook). **Không phải lượt chính thức** nhưng ridge tất định nên lượt Kaggle phải trùng đến sai số làm tròn; vẫn nên chạy để có `env.json`/`gates.json` của nền tảng.

| Cấu hình | AUROC | Δ so với ridge M3 (0,8208) | CI (Bonferroni nếu m>1) | Ba seed | Kết luận theo §6 |
|---|---:|---:|---|---|---|
| ridge ngữ cảnh **±5** | **0,8286** | **+0,0078** | [+0,0021; +0,0139] (m=3) | dương | **nhận** (họ A) |
| ridge ±7 | 0,8255 | +0,0046 | [−0,0028; +0,0121] | dương | chưa đủ bằng chứng |
| ridge ±10 | 0,8182 | −0,0026 | [−0,0117; +0,0067] | không đồng nhất | chưa đủ bằng chứng |
| ridge + scanning `pool` (ngưỡng 4,0) | 0,8138 | −0,0071 | [−0,0157; +0,0020] (m=2) | âm | chưa đủ bằng chứng |
| ridge + scanning `prior` (ngưỡng 4,0) | 0,8190 | −0,0018 | [−0,0040; +0,0004] (m=2) | âm | chưa đủ bằng chứng |

- `[DIỄN GIẢI]` **Ngữ cảnh ±5 là cải thiện thật đầu tiên của ridge kể từ P0** (+0,0078 so với +0,0126 của P0), nhưng đường cong không đơn điệu (±10 kém hơn ±3): lợi ích nằm ở vị trí ±4–±5, không phải "càng rộng càng tốt". Giả thuyết trước đó (dự đoán (a): không độ rộng nào "nhận") **sai**. Hệ quả: M3 không còn là ridge mạnh nhất; PROTOCOL §12 thêm phép so phụ mạng − `ridge_W5` và ghi hệ quả cho R5.
- `[DIỄN GIẢI]` **Scanning không giúp ridge**, khớp với phiên khác (mục 1): hai cách trộn đều ≤ ridge M3 ext, CI phủ 0. Ngưỡng scanning 3,0 cho kết quả cùng hướng (0,8173/0,8192).
- `[ĐO]` Lượt thử còn chạy C–G ở quy mô thu nhỏ (ESM-2 8M thay cho cả bốn cỡ — nên điểm ridge+ESM của bốn cỡ trong lượt đó giống nhau và **không** được báo; mạng 1 seed × 1 fold × 2 epoch) chỉ để chắc đường code. Chưa có điểm nào của `esm35_mcnn` hay các mạng khác có giá trị.

## File

| File | Vai trò |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | Tiêu chí chốt trước |
| [r6-ladder-scan.ipynb](r6-ladder-scan.ipynb) | **Một** notebook cho toàn bộ giai đoạn 0, A–G; sạch outputs, đã stamp SHA-256 PROTOCOL |
| [build_notebook.py](build_notebook.py) | Sinh lại notebook (sau đó chạy `stamp_protocol.py`) |
| [run_r6.py](run_r6.py) | Điều phối giai đoạn, ridge, huấn luyện mạng có tiếp tục được, tổng hợp (`python -I run_r6.py <thư-mục-OOF>` để tổng hợp lại ngoài notebook) |
| [r6data.py](r6data.py) · [r6esm.py](r6esm.py) · [r6nn.py](r6nn.py) · [r6stats.py](r6stats.py) | Dữ liệu và đặc trưng · trích ESM-2 · `ConvHead` · bootstrap theo cụm và quy tắc kết luận |
| [make_scantable.py](make_scantable.py) → `data/processed/r6-scantable.npz` | Bảng ô scanning (sổ nguồn gốc ở `data/README.md`); [scantable-summary.json](scantable-summary.json) |
| [cross_source_audit.py](cross_source_audit.py) → [cross-source-audit.json](cross-source-audit.json) | Phép kiểm chéo mục 1 |
| [dryrun-local-stageAB.json](dryrun-local-stageAB.json) | Kết quả ridge giai đoạn A và B từ lượt thử cục bộ (mục 2) |
| [selftest_r6.py](selftest_r6.py) | Kiểm đường code (15 kiểm; **không** phải thí nghiệm) |
| [data-needs.json](data-needs.json) | File dữ liệu notebook cần cho `make_data_package.py` |

## Đã kiểm cục bộ `[ĐO]` (không huấn luyện thật, không in AUROC của biến thể nào)

- `selftest_r6.py`: 15/15 kiểm. Đặc trưng dựng lại bằng `cell_features(W=3)` **bằng cache từng bit** trên 92.337 ô; ridge M3 qua đường chia của R6 cho 0,820822 (ensemble) khớp P0 đến 0; không hàng scanning nào thuộc cụm test ở cả 5 fold; `compare` trùng `run_curve.compare`; **cắt cửa sổ ESM-2 8M thật khớp tính tay ở vị trí 1, 2, 14, 27, 28** (kể cả biên); mạng tất định theo seed trên CPU, tiếp tục được khi phiên ngắt.
- Chạy thử notebook trên CPU trong cây thư mục ghép từ hai gói zip: đường SMOKE, rồi toàn bộ các ô 0–15 (ESM-2 8M thay cho cả bốn cỡ; mạng 1 seed × 1 fold × 2 epoch) — **tất cả ô chạy hết, không lỗi**, kể cả trích embedding cho 92.337 ô bão hòa + 133.764 ô scanning, ridge+ESM, nạp crop, mạng ở cả bảy cấu hình và bốn chế độ scanning, tổng hợp, đóng gói `r6-results.zip` (một lỗi đầu tiên là do công cụ thử của tôi, không phải notebook). Điểm của mạng trong lượt này không có giá trị khoa học và không lưu.
- Hạn chế: chưa chạy trên GPU thật; tốc độ, bộ nhớ và hạn mức Kaggle là `[ƯỚC LƯỢNG]` cho tới khi ô benchmark chạy.

## Việc Trọng làm tay

1. Dựng lại **cả hai gói** (đã có file dữ liệu mới nên `degron-data-v1` không đủ): từ gốc repo
   ```bash
   K=topics/degron-footprint/research/notebook-kit-2026-10-22
   python3 -I $K/make_data_package.py --list          # duyệt danh sách trước khi upload
   python3 -I $K/make_data_package.py --version v2    # -> degron-data-v2.zip
   python3 -I $K/make_code_package.py
   ```
   Trên Kaggle: *New Version* của dataset dữ liệu với `degron-data-v2.zip` và của dataset mã với zip mới. Chỉ gắn **một** gói dữ liệu vào notebook (nbkit lấy gói đầu tiên tìm thấy).
2. Import `r6-ladder-scan.ipynb`, gắn hai dataset, *Accelerator* = GPU T4, **Internet bật**. Chạy lần đầu với `SMOKE = True`, rồi `SMOKE = False`.
3. Đọc ô benchmark (giờ GPU ước lượng theo số đo thật) **trước** khi để chạy hết; thiếu hạn mức thì bỏ `'G'` rồi `'F'` khỏi `STAGES` (không bỏ 'E').
4. Tải `r6-results.zip`, giải nén vào `run-<phiên>/` cạnh README này. Rồi báo tôi: tôi đối chiếu tiêu chí chốt trước, viết kết quả vào README này (kể cả khi âm), chấm lại các dự đoán PROTOCOL §10 và cập nhật sổ `data/README.md`.

## Chi phí `[ƯỚC LƯỢNG]`, chưa benchmark

CPU (0, A, B, D): vài chục phút. GĐ C: ≈ 12–20 phút T4 cho bốn cỡ + scanning 35M; cache ≈ 10,5 GB. GĐ E/G/F: 11 cấu hình mạng × 15 lượt; vài giờ GPU. Ô benchmark thay ước lượng này bằng số đo trước khi chạy thật.

## Giới hạn (chi tiết ở PROTOCOL §9)

Benchmark phát triển OOF, không phải kiểm chứng ngoài; ngưỡng phân giải ≈ 0,014–0,021 cho phép so mạng với ridge, ≈ 0,008 cho cặp cấu hình gần nhau, nên "chưa đủ bằng chứng" không loại trừ lợi ích nhỏ; một cấu hình siêu tham số cho mọi mạng; ESM-2 đã thấy các protein người lúc tiền huấn luyện; rò rỉ scanning chỉ chặn bằng cụm cov80; scanning chỉ có thay thế R/A/S.
