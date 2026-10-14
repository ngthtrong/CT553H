# Hiểu đề tài degron — bản giải thích đơn giản

> **Dành cho ai:** chính Trọng, khi cần nhớ lại đề tài mà không phải đọc tài liệu nghiên cứu. Viết từ con số không, không giả định bạn nhớ gì về sinh học.
>
> **Đây là tài liệu học, không phải tài liệu quyết định.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md) — hiện degron là **đề tài chính** theo [D-023](../../DECISIONS.md#d-023). Số liệu lấy từ các báo cáo audit trong [topics/degron-footprint/research/](../../topics/degron-footprint/research/); mỗi chỗ đều dẫn link tới nguồn gốc.
>
> Có một hub HTML chi tiết hơn ở [lectures/degron-footprint/](../degron-footprint/index.html). Bản này **đơn giản hơn hẳn** và viết bằng markdown để đọc nhanh.

---

> **Cập nhật 13/10/2026 — một số con số bên dưới đã đổi.** Sau [audit dữ liệu đầy đủ](../../topics/degron-footprint/research/full-data-audit/README.md), ba điều quan trọng nhất: **(1)** việc chặn "tính lực thống kê" **đã xong, tập test đủ lực**; **(2)** hai mốc 0,6045 và 0,7792 là **oracle đọc nhãn test**, không mô hình nào đạt, nên cách đọc "dư địa 0,1747 / +28,9%" không còn dùng; **(3)** rủi ro số một **đổi** thành "nhãn mức residue chỉ lặp lại khoảng một nửa". Chỗ nào còn số cũ đều có ghi chú chỉ sang [bài 10](10-data-up-close.md).

---

## Đọc theo thứ tự này

Mỗi bài 5–10 phút. Bài 1–3 là nền, bài 4–6 là đề tài, bài 7–9 là đánh giá và rủi ro, bài 10 là dữ liệu thật.

| # | Bài                                                                    | Trả lời câu hỏi                                                                                                           |
| - | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1 | [Protein, degron và chuyện phân hủy](01-protein-and-degron.md)       | Protein là gì? Degron là gì? Vì sao nó quan trọng với bệnh?                                                          |
| 2 | [Người ta đo degron bằng cách nào](02-how-degrons-are-measured.md) | PSI là gì? Tile là gì? Footprint là gì? Nhãn ở đâu ra?                                                              |
| 3 | [Bài toán của đề tài](03-the-problem.md)                           | Chính xác thì máy tính phải dự đoán cái gì? Đầu vào, đầu ra                                                   |
| 4 | [Bốn bộ dữ liệu](04-datasets.md)                                     | Dùng dữ liệu nào, bao nhiêu, lấy ở đâu, giấy phép gì                                                              |
| 5 | [Khoảng trống: vì sao đề tài có chỗ đứng](05-the-gap.md)       | **Bài quan trọng nhất.** Vì sao mô hình hiện có không đủ, và điều đó đã được chứng minh thế nào |
| 6 | [Giải pháp đề xuất](06-proposed-solution.md)                        | Kiến trúc MIL-Degron, 5 thành phần, và giới hạn phải tự nói ra                                                      |
| 7 | [Đánh giá thế nào](07-evaluation.md)                                | precision@3 là gì? Ba bậc đánh giá. Con số phải vượt                                                                |
| 8 | [Đóng góp nếu thành công](08-contribution.md)                      | Nếu làm xong thì đóng góp là gì, cho ai, đo bằng gì                                                                |
| 9 | [Rủi ro và điều có thể làm đề tài sụp](09-risks.md)           | Chỗ nào dễ chết nhất, và cách biết sớm                                                                               |
| 10 | [Dữ liệu thật trông như thế nào](10-data-up-close.md)       | **Mới 13/10.** Mở file ra xem: một dòng gồm gì, PSI tính ra sao, dữ liệu tốt đến đâu |

**Mỗi bài báo liên quan có một file riêng:** xem [papers/](papers/README.md) — 12 công trình, mỗi file nói rõ bài đó làm gì, liên quan đến đề tài ở đâu, và **chiếm chỗ nào** của mình.

---

## Tóm tắt một trang

Nếu chỉ đọc một chỗ thì đọc đoạn này.

### Đề tài làm gì

Protein là chuỗi acid amin. Một số đoạn trong chuỗi đó, gọi là **degron**, khiến protein bị tế bào đem đi phân hủy. Nếu đổi một acid amin trong degron, protein có thể bị phá nhanh hơn hoặc bền hơn.

Người ta đã đo thực nghiệm hàng trăm nghìn đột biến như vậy. Hoá ra trong một degron dài 28 vị trí, **thường chỉ khoảng 3 vị trí** là thật sự quan trọng — đổi ở đó thì độ bền thay đổi rõ, đổi ở chỗ khác thì gần như không. Ba vị trí đó gọi là **footprint**.

> **Đề tài:** cho một peptide chưa từng thấy, dự đoán vị trí nào là footprint, và đổi sang acid amin nào thì ảnh hưởng bao nhiêu.

![Footprint: chỉ vài vị trí quan trọng](figures/fig-05-footprint.svg)

*Sơ đồ tự dựng. Giải thích đầy đủ ở [bài 2](02-how-degrons-are-measured.md).*

### Vì sao có chỗ cho đề tài

Mô hình tốt nhất hiện có cho bài này (PAP, của nhóm Voutsinos 2026) về cơ bản chỉ **đếm xem peptide có những acid amin nào**, không quan tâm chúng nằm ở đâu. Mình đã tự kiểm: đảo ngược thứ tự toàn bộ peptide thì điểm của nó **không đổi một chút nào** (Pearson giữa bản gốc và bản đảo = 1,000000).

Hệ quả: nếu trong cùng một peptide ta thay `A → V` ở hai vị trí khác nhau, mô hình đó **buộc phải** cho hai điểm giống hệt nhau — dù thí nghiệm nói một chỗ rất quan trọng và chỗ kia không. Chuyện này xảy ra ở **89,7% peptide** (2.353 trên 2.624).

Đây là điểm mạnh nhất của đề tài: khoảng trống **đã được chứng minh bằng toán và kiểm bằng script**, không phải phỏng đoán từ việc đọc tóm tắt bài báo.

![Khoảng trống đã chứng minh](figures/fig-07-composition-vs-context.svg)

*Sơ đồ tự dựng. Chi tiết và cách kiểm ở [bài 5](05-the-gap.md).*

### Con số phải vượt

Bảng này **đã được sửa ngày 13/10** sau khi dựng được lần đo thứ hai. Hai con số cũ (0,6045 và 0,7792) là **oracle đọc chính nhãn test**, nên không mô hình nào đạt được chúng:

| Mốc | precision@3 | Nghĩa là |
| --- | ---: | --- |
| Đoán ngẫu nhiên | 0,1204 | sàn |
| **Baseline thành phần, ước lượng trung thực** | **0,4897** | **mốc thật phải vượt** |
| ~~Cận của lớp thành phần~~ | ~~0,6045~~ | oracle — **nhìn nhãn test**, không đạt được |
| **Trần nhãn thực nghiệm** | **0,6514** | một lần đo chấm trên nhãn lần đo kia |
| ~~Oracle không ràng buộc~~ | ~~0,7792~~ | oracle — **nhìn nhãn test**, không đạt được |

Dư địa thật là **0,1617** (từ 0,4897 lên 0,6514), không phải 0,1747. Nguồn: [full-data-audit mục 4](../../topics/degron-footprint/research/full-data-audit/README.md); giải thích dễ hiểu ở [bài 10](10-data-up-close.md).

> Mốc **cam kết** cuối cùng của đề tài vẫn **chờ Trọng xác nhận** ở [DECISIONS.md phần C-6](../../DECISIONS.md). Bảng trên là **bằng chứng đo được**, không phải quyết định.

### Trạng thái thật, không tô hồng

|                        |                                                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Dữ liệu              | **Đã tải đủ bốn nguồn, kiểm SHA-256, đã audit** (13/10). Thêm **4 bảng PSI mới** repo chưa từng có. Xem [bài 10](10-data-up-close.md) |
| Mô hình              | **Chưa huấn luyện gì cả.** Chưa có một kết quả mô hình nào                                        |
| Khoảng trống         | **Đã chứng minh** (89,7%, cận chính xác, kiểm bằng script)                                             |
| Kiến trúc đề xuất | **Chỉ là đề xuất.** Có tiền lệ cho từng cơ chế; mới ở chỗ ghép                                  |
| Rủi ro lớn nhất     | **Nhãn mức residue chỉ lặp lại khoảng một nửa** giữa hai lần đo (Jaccard 0,4965) — đúng chỗ đề tài làm |
| ~~Lực thống kê~~ | ~~Chưa biết n ≈ 250 có đủ~~ → **đã giải quyết 13/10: đủ lực** (0,82–0,94 ở n = 221–322). Dùng split cov80 |
| Việc chặn gần nhất | **Trọng xác nhận C-6** ở [DECISIONS.md](../../DECISIONS.md) — gồm mốc G2 và nguồn nhãn chính |

---

## Ba điều đừng bao giờ nói sai

Đây là quy ước ngôn từ của đề tài, chép từ [topic-decision.md mục 8](../../topics/degron-footprint/research/topic-decision.md):

1. **Không nói "chưa ai dùng MIL cho protein".** [BioBlobs](papers/bioblobs-2025.md) (10/2025) đã dùng attention-MIL trên protein. Nói đúng: *mới ở chỗ ghép và ở chỗ đặt cổng phơi lộ tại bước gộp, chưa thấy áp cho degron*.
2. **Không nói "dùng cấu trúc là phần mới".** [Larsen 2025](papers/larsen-2025.md) đã tính rASA và pLDDT từ AlphaFold2, và đã làm bản đồ thay thế *in silico*.
3. **Không nói "mô hình thành phần cho bản đồ phẳng".** Ràng buộc đúng là: *trong cùng peptide, các vị trí có cùng cặp (acid amin gốc, acid amin thay vào) buộc phải nhận cùng điểm*. Bản đồ của nó không bắt buộc phẳng.

Và một điều về số liệu, **đã mạnh hơn sau 13/10**: không chỉ là "chưa hứa 0,1747", mà **con số 0,1747 đã bị bác bỏ** — nó dựa trên oracle 0,7792 đọc nhãn test. Đã tách nhiễu: **75,9%** phần dư là nhiễu đo, phần học được tối đa **8,7%** phương sai, không phải 35%. Xem [bài 10 mục 6](10-data-up-close.md).

---

## Hình trong hub này

Tất cả 16 sơ đồ trong [figures/](figures/) đều là **sơ đồ tự dựng** (SVG, mình vẽ), và đều mang nhãn `SƠ ĐỒ TỰ DỰNG` ở góc trên phải để không lẫn với hình của tác giả bài báo.

Hình gốc của tác giả nằm riêng ở [lectures/degron-footprint/assets/figures/](../degron-footprint/assets/figures/NOTICE.md), chỉ gồm hình của Voutsinos 2026 vì bài đó giấy phép CC BY-NC cho phép dùng lại. Các bài khác chỉ được dẫn link, không sao chép hình — lý do ghi trong [NOTICE.md](../degron-footprint/assets/figures/NOTICE.md).
