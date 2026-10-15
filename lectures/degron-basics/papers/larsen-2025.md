[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# Larsen 2025 — degron của yếu tố phiên mã

| | |
|---|---|
| **Nơi công bố** | bioRxiv, 05/2025 |
| **DOI** | <https://doi.org/10.1101/2025.05.16.654404> |
| **Giấy phép** | **CC BY-NC-ND** → không tạo bản phái sinh, **không sao chép hình** |
| **Mức kiểm** | **[ĐÃ ĐỌC]** toàn văn — đây là "cổng chặn 1" của đề tài |

---

## Vì sao phải đọc bài này trước mọi thứ khác

Vì nó là bài **gần đề tài nhất**. Nếu nó đã làm đúng việc đề tài định làm thì đề tài hết chỗ. Đọc toàn văn là một trong ba **cổng chặn** phải qua trước khi chốt đề tài ([topic-decision.md mục 7](../../../topics/degron-footprint/research/topic-decision.md)).

## Kết quả: cổng chặn **ĐÃ QUA, theo hướng thuận**

Bài này **không** làm bốn việc mà đề tài định làm:

| Việc | Larsen 2025 |
|---|---|
| Mô hình hóa đặc hiệu E3 | **không** |
| Đề xuất kiến trúc mới | **không** |
| Dùng nhãn E3 hay nhãn CRISPR | **không** |
| Có phần giải thích mô hình | **không** |

Họ dùng PAP cùng ESM-1b chỉ để **so sánh biến thể CRX**. Phần nhắc CRL4-DCAF12 và FEM1b nằm ở mục Thảo luận, là **suy đoán theo y văn**, không phải kết quả.

→ **Trục của đề tài còn trống.**

## Nhưng bài này thu hẹp tính mới ở hai chỗ

Đây là phần quan trọng, và nó bắt buộc:

**1. Họ đã dùng cấu trúc.** Đã tính **rASA và pLDDT** từ AlphaFold2 kèm DSSP. Điểm degron so với rASA \|r\| = **0,41**, so pLDDT \|r\| = **0,36** trên toàn thư viện; 32% degron có rASA > 0,7 và 40% có pLDDT < 70.

**1b. Họ đã tìm ra hiện tượng ΔPAP đổi dấu** (bổ sung 14/10/2026, [tra y văn](../../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md)). Trên CRX, tách theo vùng: ΔPAP Pearson **0,54** trong vùng vô định hình so với **−0,19** trong homeodomain đã gấp (ESM-1b đi ngược: 0,31 và 0,52). Nên phép đo của repo ngày 14/10 trên 6 protein MaveDB là **xác nhận lại ở quy mô lớn hơn**, không phải phát hiện. Nhãn của họ là transactivation, không phải độ dồi dào, và chính họ ghi là khó tách hai thứ.
→ **"Dùng cấu trúc" không còn là phần mới của đề tài.**

**2. Họ đã làm bản đồ thay thế *in silico*.** Đã tính ΔPAP cho **mọi đột biến điểm** trong một vùng của HSF1.
→ **"Giải thích biến thể bằng bản đồ thay thế" không còn là phần mới.**

Hệ quả cho đề tài: chỗ mới phải nằm ở **nơi đặt** cổng phơi lộ (tại bước gộp, không phải đầu vào) và ở **chỗ ghép** các cơ chế — xem [bài 6 mục 4](../06-proposed-solution.md).

## Một bộ dữ liệu bài này mở ra, chưa tải

Thư viện **nhân** (nuclear), khác khoang tế bào so với bộ bào tương của [Voutsinos 2026](voutsinos-2026.md):

| | Số lượng |
|---|---:|
| Đoạn có điểm | **58.781** |
| Yếu tố phiên mã | **1.626** |
| Đoạn chồng lấn với thư viện bào tương | 8.645 / 234 protein |

**Vì sao đáng quan tâm:** đây là lựa chọn **rẻ hơn** để mở rộng bậc 2 của phép đánh giá — cùng assay, khác khoang tế bào, nên là phép kiểm tổng quát hóa tự nhiên. Nếu [rủi ro lực thống kê](../09-risks.md) thành hiện thực, đây là nguồn bổ sung đầu tiên nên nghĩ tới.

> **Phải kiểm giấy phép trước khi dùng.** Tiền ấn là CC BY-NC-**ND**. Điều khoản ND (no derivatives) áp cho *bài báo*, nhưng điều kiện dùng *dữ liệu* phải kiểm riêng trước khi đưa vào kế hoạch. **Chưa kiểm.**

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
