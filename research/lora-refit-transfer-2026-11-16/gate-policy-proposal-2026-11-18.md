# Đề xuất chính sách cổng miền theo model — 18/11/2026

Mục 1.6 của [plan-system.md](../../plan-system.md) (đợt 3, phần **chuẩn bị**). Đây là biên bản đề xuất để Trọng và GVHD
quyết định; **không** có thay đổi mã nào được triển khai từ tài liệu này. Trạng thái khoa học giữ
`development_not_gate_closure`; không đóng G3.

## 1. Bối cảnh

- Cổng miền R3 (DEVIATIONS §7) được xây cho model npz, huấn luyện trên tile có PSI(WT) nội tại ≤ 4,0. Ứng dụng áp R3
  cho **mọi** model, kể cả LoRA-D (DEVIATIONS §12: "conservative; changing the gate per model would be a scientific
  decision").
- LoRA-D (arm D) được huấn luyện trên peptide bão hoà ở **mọi** mức PSI(WT). Câu hỏi: có nên để LoRA-D dùng cổng khác
  (nới) hay giữ R3?

## 2. Số liệu theo tầng PSI(WT) trên T `[ĐO]`

Nguồn: [results.json](results.json) (`metrics.*.strata`, sha256 `9a5b0036eb2b43b7…`) và
[similarity-results.json](similarity-results.json) (`strata_lora_minus_zero`, sha256 `0c1bfca1abb5a67a…`). T là nguồn đã
từng được xem: đánh giá chuyển miền hậu kiểm, không phải validation độc lập (giới hạn L1 của biên bản D-4).

| Tầng PSI(WT) | Peptide | MAE zero | MAE W5-D | MAE frozen-D | MAE LoRA-D | Spearman LoRA-D | LoRA-D − zero (MAE) [CI hiệu chỉnh ×4] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ≤ 3 | 524 | 0,4319 | 0,3819 | 0,3654 | **0,3303** | 0,525 | −0,1016 [−0,1136; −0,0895] |
| (3; 4] | 323 | 0,4158 | 0,3918 | 0,3759 | **0,3505** | 0,558 | −0,0653 [−0,0789; −0,0517] |
| (4; 5] | 306 | 0,3843 | 0,3998 | 0,3906 | **0,3589** | 0,480 | −0,0253 [−0,0348; −0,0161] |
| > 5 | 257 | **0,3470** | 0,4428 | 0,4436 | 0,3622 | 0,201 | **+0,0152 [+0,0051; +0,0260]** |

`[DIỄN GIẢI]` Lợi thế của LoRA-D so với dự đoán "không đổi" (zero) giảm dần khi PSI(WT) tăng và **đảo chiều** ở tầng
> 5: tại đó dự đoán zero có MAE thấp hơn, CI hiệu chỉnh nằm hoàn toàn trên 0. Thứ hạng trong tầng > 5 yếu (Spearman
0,201). Bằng chứng hiện có **không ủng hộ** việc nới cổng cho LoRA-D ra các tile ổn định cao.

Lưu ý thang: tầng ở trên dùng PSI(WT) nội tại của peptide T; cổng R3 tầng 1 dùng PSI đo trong màn hình GPS (in
≤ 2,687; out ≥ 3,110). Hai thang không so trực tiếp được (srs.md §2.3) — đây là một lý do nữa để không suy ngưỡng cổng
mới từ bảng trên.

## 3. Hệ quả với người dùng

| Phương án | Người dùng thấy gì | Rủi ro |
| --- | --- | --- |
| **A. Giữ nguyên R3 cho mọi model** (hiện tại) | Tile ngoài miền bị từ chối trừ khi override, với mọi model | LoRA-D không được dùng cho các tile mà nó đã thấy khi train ở PSI cao — nhưng chính ở đó nó kém zero |
| B. Cảnh báo mạnh hơn cho LoRA-D ở vùng PSI cao | Như A, thêm cảnh báo riêng khi tile measured/predicted PSI cao được chấm bằng LoRA-D (kể cả sau override) | Cần chốt ngưỡng hiển thị; thêm một mã cảnh báo; không thay đổi kết quả |
| C. Chính sách riêng theo model (`gate_policy` trong registry) | LoRA-D có thể chấm tile mà R3 từ chối | Trái với số liệu tầng > 5; cần đánh giá và biên bản khoa học riêng; dễ bị hiểu là "LoRA-D đúng cho mọi tile" |

## 4. Đề xuất

`[DIỄN GIẢI]` Giữ **phương án A**; có thể bổ sung **B** (chỉ là cảnh báo, không đổi điểm) nếu Trọng/GVHD thấy cần.
Không làm **C** khi chưa có đánh giá mới cho tầng PSI cao. Nếu chọn B, triển khai sau quyết định: mã cảnh báo mới,
test `DOM-` cho từng chính sách, ghi DEVIATIONS — theo plan-system 1.6.

## 5. Quyết định

- Phương án chọn: ……… (A / A + B / C)
- Người quyết định: Nguyễn Thanh Trọng — ngày ………
- Ghi nhận của GVHD (TS. Hồ Quang Thái): ………
- Cho tới khi có quyết định: ứng dụng giữ nguyên R3 cho mọi model (không triển khai gì từ tài liệu này).
