[← Danh mục bài báo](README.md) · Về hub

# Degformer 2026 — tiền lệ trực diện nhất, và yếu nhất

| | |
|---|---|
| **Nơi công bố** | **Không có bài báo.** Chỉ là repo GitHub: [Alpine2048/Degformer](https://github.com/Alpine2048/Degformer) |
| **Giấy phép** | Apache-2.0 |
| **Thời gian** | Tạo **24/03/2026**, push cuối **30/09/2026** |
| **Mức kiểm** | **[TỰ KIỂM]** đọc toàn bộ 15 file trong repo (README, 3 file Python, 2 CSV, LICENSE) + GitHub API; **tự chạy script đo rò rỉ trên CSV đã ship** |

---

## Vì sao bài này quan trọng

Vì nó **đã làm đúng cái mà đề tài định nhận là điểm mới**: xuất **ma trận 28 vị trí × 20 acid amin** của ΔPSI, từ **đúng** nguồn nhãn của đề tài (bảng S1 + S4 scanning + S7 saturation của [Zhang 2023](zhang-2023.md)), với `MAX_LEN = 28`.

> **Hệ quả bắt buộc:** câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20 trên nhãn đột biến thực nghiệm" **phải bị xoá** khỏi mọi tài liệu của repo. Xem bài 9 rủi ro 3.

Nó là **tiền lệ thứ năm**, sau DEGRONOPEDIA, MetaDegron, Colab của nhóm PAP, và SVM của chính nhóm Zhang.

---

## Nhưng nó yếu ở đúng những chỗ đề tài mạnh

Đây là phần quan trọng: nó là **cơ hội**, không phải án tử.

| Điểm | Degformer | Đề tài |
|---|---|---|
| Phép chia train/test | `train_test_split(test_size=0.1, random_state=42)` — **ngẫu nhiên thuần**, trên bảng S1+S4+S7 đã trộn | split **cụm protein cov80** (D-025) |
| Rò rỉ | **4,09% rò rỉ trình tự y hệt** — 2.330/56.927 dòng validation có đúng 28-mer đó trong train (1.954 trình tự phân biệt). **[TỰ KIỂM]** tái lập phép chia index-for-index | — |
| Nhãn trùng lặp | **9.496** trình tự xuất hiện nhiều lần; **9.443** trong đó mang **giá trị `controlPSI` khác nhau** (spread trung vị 0,48, tối đa 3,98 trên thang 1–6). Không dedup, không trung bình replicate | trung bình hai replicate (D-025 mục 3) |
| Đầu ra mức residue | **Không có.** Chỉ `self.head(x[:, 0])` — đọc CLS token. Ma trận heatmap dựng bằng **532 lượt forward mỗi peptide**, không phải một đầu theo vị trí | đầu mức residue, giám sát mức residue |
| Trần nhãn | không nhắc | báo kèm mọi bảng |
| Cấu trúc / phơi lộ / PLM | **không dùng gì cả** — chỉ trình tự mã hoá số nguyên | rASA/pLDDT (ở mức tile) |
| Xử lý `*` | `*` là **token thứ 21** đưa thẳng vào `nn.Embedding`, **không mask**; scan bão hòa không bao giờ thăm nó | phải **mask** |
| Tập blind | **vắng mặt khỏi repo**, cùng script chia và script đánh giá ⇒ **con số headline không tái lập được** | — |

**Về con số nó tự báo:** e50 cho S1 **0,9420** / S4 0,9463 / S7 **0,9162**. Hai lưu ý. (a) README gọi là "Correlation (ρ)" nhưng **hàm tương quan duy nhất trong repo là `scipy.stats.pearsonr`**, nên rất có thể là **Pearson, không phải Spearman** `[TỰ KIỂM]`. (b) Vì S7 là bão hòa, mỗi mutant bị giữ lại có **~500 anh em** trong train — nên con số đó đo **nội suy trong degron đã biết**, không phải tổng quát hoá.

**Mục tiêu của nó cũng không phải ΔPSI.** `predict.py` ghi chú "UPDATED: 1 OUTPUT" và chỉ xuất `pred_controlPSI`; README nói "predicts deltaPSI and controlPSI" là **lạc hậu**. ΔPSI trong heatmap tính hậu kỳ bằng mutant − WT `[TỰ KIỂM]`.

---

## Bối cảnh repo: dấu hiệu đây là bài tập cá nhân

Tác giả **Oliver Hong** (`Alpine2048`): **26 trong 27 commit nằm trong một giờ** ngày 24/03/2026, upload qua web UI, lịch sử còn file `lol.md` và `temp.md`; một lần sửa README 30/09/2026. **0 star, 0 fork, 0 issue**, không preprint, không lab, không yêu cầu trích dẫn. Repo liên quan duy nhất của tác giả là `Degron-prediction-by-composition-seq-motifs` (2024) — có lẽ là thứ mà README so sánh khi nói "performs better than composition or motif-search based methods" `[TỰ KIỂM]`.

Không fix seed torch (`torch.manual_seed` **không có**), không file requirements, không test, và `StandardScaler` được fit **trước** phép chia (rò rỉ tiền xử lý nhẹ).

---

## Cách dùng nó

1. **Phải trích trong đề cương và luận văn** như tiền lệ thứ năm, kèm mô tả trung thực: "tự báo, chưa công bố, split ngẫu nhiên, 4,09% rò rỉ đo được".
2. **Nhận làm baseline** là thí nghiệm giá-trị-trên-giờ cao nhất đang có: chạy lại `peptide_model_epoch50.pt` **dưới split cov80** và thước đo mức residue của đề tài. Repo đã ship cả **ba checkpoint** (~2,2 MB mỗi cái) và cả **`training_data.csv` 19,9 MB / 569.270 dòng** `[TỰ KIỂM]`. Việc này **cần Trọng quyết** — xem bài 9 tóm lại.
3. ⚠ **An toàn khi nạp:** checkpoint là **pickle** (`torch.load(..., weights_only=False)`) kèm một `StandardScaler` đã pickle. Nạp nó **thực thi mã tuỳ ý**. Xử lý repo như **dữ liệu không tin cậy**: thư mục riêng và trống, script của mình để chỗ khác, chạy `python3 -I`.

---

## Phát biểu đúng mức sau khi có bài này

Claim còn sống **không phải** "ma trận 28×20 là thứ chưa ai làm", mà là điều kiện đánh giá:

> Ma trận 28 × 20 **đã từng được tạo** — bởi Degformer trên cùng nhãn, và bởi [Larsen 2025](larsen-2025.md) cho từng protein đơn lẻ — nhưng **chưa bao giờ dưới một split theo cụm protein, chưa bao giờ kèm trần nhãn đã đo, chưa bao giờ kèm bất định từng ô, và chưa bao giờ có điều kiện theo lớp phơi lộ.**

Chi tiết: [báo cáo 15/10](../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/README.md) mục 6.1.

---

[← Danh mục bài báo](README.md) · Về hub
