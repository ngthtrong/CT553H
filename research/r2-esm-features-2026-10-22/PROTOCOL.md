# R2 — Đặc trưng ESM-2 đóng băng cộng vào ridge M3: PROTOCOL chốt trước khi chạy

Chốt ngày 22/10/2026, **trước khi** trích bất kỳ đặc trưng ESM-2 nào và trước khi thấy số nào của R2. Không sửa tiêu chí sau khi xem kết quả; nếu phải sửa thì thêm mục "sửa sau khi xem" kèm ngày và lý do, không ghi đè. SHA-256 của file này được nhúng vào notebook (`stamp_protocol.py`); notebook dừng nếu file đổi.

Nối tiếp [next-phase-plan §3.2](../next-phase-plan-2026-10-22/README.md). Thí nghiệm này **không** đổi trạng thái G2/G3, không phải kiểm chứng ngoài.

## 1. Câu hỏi

Biểu diễn từ mô hình ngôn ngữ protein đóng băng có thêm tín hiệu ngoài one-hot (acid amin hoang dã, acid amin thay vào, thành phần tile, ngữ cảnh ±3) mà ridge M3 đang dùng không?

`[DIỄN GIẢI]` Đây là thay đổi **biểu diễn đầu vào**, không phải thiết kế tương tác thứ sáu: không thêm lớp mạng, không thêm cổng/FiLM/song tuyến. Mô hình học vẫn là ridge. Động cơ: đường cong học của ridge phẳng từ ~35 cụm ([learning-curve §2](../learning-curve-2026-10-22/README.md)), tức ridge chạm trần của **đặc trưng**, không phải của lượng nhãn trong vùng cũ.

## 2. Quyết định chốt trước (không đổi sau khi thấy số)

| Hạng mục | Chốt | Lý do |
|---|---|---|
| Mô hình | `facebook/esm2_t33_650M_UR50D`, **một** cỡ duy nhất | Tile chỉ 28 residue nên 650M chạy được trong GPU miễn phí (fp16, ~1,3 GB); là cỡ lớn nhất của họ ESM-2 mà không cần chia lô đặc biệt. Không thử cỡ khác |
| Giấy phép | MIT, theo model card trên Hugging Face `[ĐO]` 22/10/2026 (đọc trang model card) | Nếu card đổi, ghi lại ngày đọc trong `results.json` |
| Lớp lấy đặc trưng | `last_hidden_state` của lớp cuối (đã qua LayerNorm cuối của `EsmModel`) | Một lớp, không quét lớp |
| Cách trích | Với ô (peptide, vị trí `p`, acid amin `a`): `f = [ h_mut(p) − h_wt(p) ; mean_j (h_mut(j) − h_wt(j)) ]`, j = 1..28, `h` là embedding residue (1280 chiều), tức **2.560 chiều**, lưu float16 | Một công thức, chốt trước: Δ tại điểm đột biến + Δ trung bình toàn tile (phản ánh ảnh hưởng ngữ cảnh) |
| Giảm chiều | PCA 64 thành phần, `svd_solver='randomized'`, `random_state=17`, **khớp một lần mỗi outer fold trên toàn bộ outer-train** (train ∪ val), rồi chuẩn hóa z theo thống kê outer-train | Đúng quy ước "chuẩn hóa/chọn đặc trưng/tiền huấn luyện chỉ trên outer-train". Số thành phần 64 không điều chỉnh |
| Mô hình học | `Ridge` với lưới α ∈ {1, 10, 100, 1000} chọn bằng MSE trên inner validation theo cụm, rồi khớp lại trên train ∪ val | Đúng `run_curve.ridge` (khác ở chỗ dùng toàn bộ cột) |
| Biến thể | **M3** (180 cột; đối chứng, phải tái lập 0,8208) · **M3+ESM** (180 + 64) · **ESM** (chỉ 64; chỉ mô tả) | M3+ESM là thí nghiệm; ESM-only không dùng để kết luận |
| Dữ liệu | Tập nới ngưỡng 4,0: 176 peptide / 92.337 ô huấn luyện, outer-test là 47.847 ô của 91 peptide gốc | Cấu hình chính của đề tài (P0) |
| Chia | 5 outer fold GroupKFold cov80 trùng G2; inner `GroupShuffleSplit(test_size=.2, random_state=seed)`; seed 17/29/43; peptide nới ngưỡng chỉ vào outer-train, bỏ khỏi train nếu trùng cụm test | Sao nguyên `run_curve.py`, kịch bản `ext` |
| Chỉ số | AUROC mức ô, macro theo peptide, điểm OOF ensemble (trung bình ba seed) | Như mọi thí nghiệm trước |
| So sánh | Δ = A(M3+ESM) − A(M3), ghép cặp theo peptide, bootstrap 5.000 lần **theo cụm** (`run_curve.compare`, seed bootstrap 20261022) | Như P0/P1 |

## 3. Tiêu chí kết luận (chốt trước)

Gọi Δ là hiệu ensemble, [lo, hi] là CI 95%, Δ₁₇, Δ₂₉, Δ₄₃ là hiệu từng seed (cùng chia train/val):

| Điều kiện | Kết luận ghi vào báo cáo |
|---|---|
| lo > 0 **và** Δ₁₇, Δ₂₉, Δ₄₃ đều > 0 | **nhận**: đặc trưng ESM-2 cải thiện ridge M3 |
| lo > 0 nhưng có seed ≤ 0 | lợi ích chưa bền qua seed |
| hi < 0 | **âm**: thêm ESM-2 làm ridge kém đi |
| còn lại | chưa đủ bằng chứng (CI phủ 0) |

Hàm `run_r2.verdict` cài đúng bảng này. Không có tiêu chí thứ hai nào, không có ngưỡng "đủ lớn" nào; một Δ nhỏ nhưng thỏa điều kiện vẫn gọi là "nhận", kèm kích thước hiệu ứng trong báo cáo.

## 4. Cổng tự kiểm (dừng nếu hỏng)

1. Manifest dữ liệu khớp SHA-256; PROTOCOL khớp SHA nhúng trong notebook.
2. Bảng trình tự khớp nhãn hai cache và 5 fold trùng G2 (`common.load_combined` assert).
3. Embedding: số ô = 92.337; không NaN/Inf; token 30 (`<cls>` + 28 + `<eos>`).
4. **Tái lập đối chứng:** ridge M3 qua đường chia của `common.py` cho ensemble 0,8208 (|Δ| ≤ 1e-4) và từng seed 0,8204/0,8210/0,8209 (|Δ| ≤ 2e-4), tức khớp `learning-curve-2026-10-22/results.json`.

## 5. Điều không làm

- Không đổi cỡ ESM-2, lớp lấy đặc trưng, công thức Δ, k của PCA hay lưới α sau khi thấy số; nếu hết bộ nhớ GPU thì giảm `BATCH`, không đổi mô hình.
- Không tinh chỉnh (fine-tune) ESM-2; không thêm ESM vào mạng nơ-ron; không thử tương tác.
- Không lọc ô, không chọn seed, không chạy lại để "chọn lần đẹp". Chạy một lần; nếu phiên bị ngắt thì tiếp tục từ cache đặc trưng, kết quả vẫn là một lần.
- Không báo biến thể ESM-only như kết luận.

## 6. Giới hạn ghi trước

- `[ĐO]` sẽ là benchmark **phát triển OOF**, không phải kiểm chứng ngoài.
- ESM-2 được tiền huấn luyện không giám sát trên UniRef; các protein của đề tài rất có thể nằm trong đó. Không có nhãn PSI rò vào, nhưng trình tự thì có thể đã được "thấy". Không tách được ảnh hưởng này trong thí nghiệm.
- M3+ESM có nhiều tham số hơn M3; một Δ dương không phân biệt "thông tin pLM" với "thêm chiều". Biến thể ESM-only chỉ để mô tả thêm.
- Một cỡ mô hình, một công thức trích; âm ở đây không loại trừ mọi cách dùng pLM.
- Không hiệu chỉnh đa so sánh: chỉ một phép so chính.
- Hệ quả cho sản phẩm: nếu "nhận", suy luận cần ESM-2 (≈1,3 GB, GPU/CPU chậm) và đây là chi phí cần cân trong R5; **không** tự động thay mô hình sản phẩm.

## 7. Dự đoán ghi trước

`[ĐỀ XUẤT]` Dự đoán của người soạn, để sau này chấm đúng/sai: (a) M3+ESM − M3 nhỏ (|Δ| < 0,02) hơn là lớn; (b) khả năng đạt "nhận" **không cao** (chưa tới nửa), vì 172 cụm huấn luyện hẹp so với 64 chiều thêm vào; (c) ESM-only thấp hơn M3. Nếu dự đoán sai, ghi rõ trong báo cáo.

## 8. Cách chạy và chi phí

Notebook `r2-esm.ipynb` (xem [README](README.md)). `[ƯỚC LƯỢNG]`, chưa benchmark: giai đoạn 1 (GPU T4, fp16, batch 256) 10–30 phút cho 92.337 ô + 176 WT; giai đoạn 2 (CPU) 10–20 phút. Cache đặc trưng ~0,5 GB ghi ngoài thư mục kết quả để chạy lại giai đoạn 2 không cần GPU. Cần Internet bật để tải trọng số từ Hugging Face, **hoặc** gắn sẵn ESM-2 làm dataset/model (notebook dò thư mục chứa `config.json` có tên `esm2_t33_650M`).
