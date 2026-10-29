[← Về README repository](../../../README.md)

# Các công trình liên quan — mỗi bài một file

> Mỗi file trả lời bốn câu: **bài đó làm gì**, **liên quan đến đề tài ở đâu**, **chiếm chỗ nào của mình**, và **con số nào đáng nhớ**.
>
> **Nhãn bằng chứng:** [TỰ KIỂM] đã tự tải dữ liệu / đọc mã nguồn / tự đếm · [ĐÃ ĐỌC] đã đọc toàn văn · [NGUỒN] đã đọc tóm tắt trên trang gốc · [CHƯA KIỂM] chỉ thấy qua tóm tắt tìm kiếm.

## Nhóm 1 — nguồn dữ liệu của đề tài

| Bài | Vai trò | Mức kiểm |
|---|---|---|
| [Voutsinos 2026](voutsinos-2026.md) | Bộ dữ liệu 1 + **baseline PAP** mà đề tài phải vượt | [TỰ KIỂM] tái lập PAP, khớp cả hai số công bố |
| [Zhang 2023](zhang-2023.md) | **Bộ dữ liệu 2 và 3 — nguồn nhãn chính** | [TỰ KIỂM] tải, checksum, tự đếm toàn bộ |
| [Larsen 2025](larsen-2025.md) | Bộ dữ liệu thứ tư (chưa tải); **đã thu hẹp tính mới** của đề tài — kể cả hiện tượng ΔPAP đổi dấu. **Mới 15/10: giấy phép đã kiểm (dữ liệu là MIT qua GitHub), và nó KHÔNG có nhãn mức residue nào** | [ĐÃ ĐỌC] toàn văn + [TỰ KIỂM] giấy phép, chồng lặp |
| [Schulze 2026](schulze-2026.md) | **Baseline bắt buộc** cho nhãn độ dồi dào (ma trận theo lớp phơi lộ + ThermoMPNN); tự nêu khoảng trống neo-degron | [ĐÃ ĐỌC] toàn văn |
| [MaveDB](mavedb.md) | Bộ dữ liệu 4 — kiểm trên protein nguyên vẹn | [TỰ KIỂM] đã đếm qua API |

## Nhóm 2 — đối thủ trực tiếp, chiếm cùng khung ứng dụng

| Bài | Chiếm chỗ nào | Mức kiểm |
|---|---|---|
| [MetaDegron 2024](metadegron-2024.md) | Hit motif/degron ứng viên với **21 lựa chọn E3** (một classifier dùng chung), **có máy chủ web** — công cụ bổ sung hơn là đối thủ cùng bài toán | [ĐỌC-MÃ]/[ĐO] 21/10 |
| [DEGRONOPEDIA 2024](degronopedia-2024.md) | Cơ sở dữ liệu + web tra cứu degron | [NGUỒN] |
| [Degpred 2022](degpred-2022.md) | Dự đoán degron quy mô lớn trên proteome. ⚠ **Công cụ duy nhất chưa xác minh được mức xuất ra** — phải giải quyết trước khi viết phần văn liệu | [CHƯA KIỂM] |
| [ELITE 2025](elite-2025.md) | Xếp hạng E3 cho substrate, cùng khung ứng dụng | [CHƯA KIỂM] |
| **[Degformer 2026](degformer-2026.md)** | **Tiền lệ thứ năm, trực diện nhất: đã xuất ma trận 28 × 20 ΔPSI từ đúng nhãn của đề tài.** Nhưng split ngẫu nhiên, 4,09% rò rỉ, không có đầu mức residue ⇒ **baseline nên đánh bại** | **[TỰ KIỂM]** đọc toàn bộ mã nguồn, tự đo rò rỉ |

## Nhóm 3 — tiền lệ phương pháp, làm hẹp tuyên bố tính mới

| Bài | Thu hẹp điều gì | Mức kiểm |
|---|---|---|
| [BioBlobs 2025](bioblobs-2025.md) | **Đã dùng attention-MIL trên protein** → không được nói MIL là mới | [NGUỒN] |
| [OmniESI 2025](omniesi-2025.md) | Đã dùng điều biến có điều kiện hai chiều (ý tưởng FiLM) | [NGUỒN] |
| **[LeBlanc 2026](leblanc-2026.md)** | **Không phải bài degron**, nhưng hạ **ba lập luận hỗ trợ** xuống "thực hành chuẩn" (tách abundance/function trên thư viện tile, split cụm protein, đối chiếu trần replicate). Và kết quả **"thành phần > vị trí"** của họ là **rủi ro khoa học** cho mô hình mức residue | **[ĐÃ ĐỌC]** toàn văn |

## Nhóm 4 — bối cảnh rộng

| Bài | Liên quan | Mức kiểm |
|---|---|---|
| [Koren 2018](koren-2018.md) | Công trình nền, lập ra phương pháp sàng lọc GPS peptidome | [NGUỒN] |
| [Tokheim 2021](tokheim-2021.md) | Đột biến degron trong ung thư — lý do nghiên cứu | [NGUỒN] |
| [AlphaMissense 2023](alphamissense-2023.md) | Dự đoán độc tính biến thể; đề tài **bổ sung cơ chế**, không thay thế | [NGUỒN] |

---

## Hình của tác giả: được dùng bài nào

Chỉ **Voutsinos 2026** có giấy phép cho phép sao chép hình (CC BY-NC 4.0, xác minh qua PMC ngày 11/10/2026). Đường dẫn cũ `lectures/degron-footprint/assets/figures/` đã được gỡ khỏi cây làm việc; tài sản lịch sử còn trong nhánh `backup-before-clean`.

> **Phân biệt quan trọng (rõ ra ngày 15/10):** giấy phép của **bài báo** và giấy phép của **dữ liệu** có thể khác nhau. Larsen 2025 là ví dụ: bài CC BY-NC-ND nhưng dữ liệu mức tile nằm trong repo GitHub dưới **MIT**. Nên khi đánh giá một nguồn mới, **kiểm cả hai**, và nhớ rằng điều khoản ND cấm *chia sẻ* bản phái sinh, không cấm *tạo ra* nó ([CC FAQ](https://creativecommons.org/faq/)).

Các bài khác **chỉ được dẫn link, không sao chép hình**:

| Bài | Giấy phép | Hệ quả |
|---|---|---|
| Zhang 2023 (*Molecular Cell*) | All rights reserved (Elsevier) | chỉ dẫn link |
| Larsen 2025 (bioRxiv) | Bài báo CC BY-NC-**ND**; **dữ liệu mức tile là MIT** qua [repo GitHub của nhóm](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors) (kiểm 15/10) | **không sao chép hình, không phát hành lại phụ lục bioRxiv**; nhưng **được tải và dùng CSV** từ repo MIT, kèm giữ thông báo MIT. Nếu cần hình thì **tự vẽ lại từ dữ liệu** |
| Voutsinos 2026 (*Science Advances*) | CC BY-**NC** (không có ND) | được dùng hình, đã tải 6 hình |
| Degformer 2026 (GitHub) | Apache-2.0 | được dùng mã và trọng số; ⚠ checkpoint là **pickle**, nạp nó thực thi mã tuỳ ý |
| LeBlanc 2026 (*Cell Systems*) | bản thảo tác giả trên PMC | chỉ dẫn link, **chưa kiểm** điều kiện dùng hình |
| Koren 2018, Tokheim 2021, AlphaMissense 2023 | không mở | chỉ dẫn link |
| Degpred 2022, DEGRONOPEDIA 2024, MetaDegron 2024 | mở nhưng **chưa kiểm từng bài** | chỉ dẫn link cho tới khi kiểm |

`NOTICE.md` thuộc bộ tài sản lịch sử, hiện không nằm trong thư mục này.

---

[← Về README repository](../../../README.md)
