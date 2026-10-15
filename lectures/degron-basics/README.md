# Hiểu đề tài degron — bản giải thích đơn giản

> **Dành cho ai:** chính Trọng, khi cần nhớ lại đề tài mà không phải đọc tài liệu nghiên cứu. Viết từ con số không, không giả định bạn nhớ gì về sinh học.
>
> **Đây là tài liệu học, không phải tài liệu quyết định.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md) — hiện degron là **đề tài chính** theo [D-023](../../DECISIONS.md#d-023). Số liệu lấy từ các báo cáo audit trong [topics/degron-footprint/research/](../../topics/degron-footprint/research/); mỗi chỗ đều dẫn link tới nguồn gốc.
>
> Có một hub HTML chi tiết hơn ở [lectures/degron-footprint/](../degron-footprint/index.html). Bản này **đơn giản hơn hẳn** và viết bằng markdown để đọc nhanh.

---

> **Cập nhật 15/10/2026 — hub đã được viết lại sau khi lập luận lại đề tài.** Nguồn:
> [lập luận lại 15/10](../../topics/degron-footprint/research/topic-argument-2026-10-15.md), dựa trên
> [audit dữ liệu](../../topics/degron-footprint/research/full-data-audit/README.md) (13/10),
> [baseline PAP](../../topics/degron-footprint/research/pap-baseline/README.md) và
> [tiền đề kiến trúc](../../topics/degron-footprint/research/architecture-check/README.md) (14/10), và
> [tra y văn](../../topics/degron-footprint/research/architecture-check/prior-art-exposure-gate.md) (14/10).
>
> **Năm thay đổi lớn:**
>
> 1. **Mô hình degron công bố gần nhất thua baseline thành phần.** ΔPAP `cnn2w7` đạt precision@3 **0,4270**, baseline thành phần **0,4884**, p ≈ 6 × 10⁻¹⁹. Nên mốc phải vượt (**0,4897**) nằm **trên** state-of-the-art.
> 2. **Trục ngữ cảnh chưa cạn.** Đổi kernel 1 → 7 cho **+0,1311** precision@3 mức residue, so với chỉ +0,0032 trên điểm đoạn. Đây là bằng chứng dương đầu tiên của repo.
> 3. **Cổng phơi lộ mất vai trò.** Nó **không huấn luyện được** trên nhiệm vụ chính, vì mọi peptide huấn luyện đều phơi lộ như nhau. Đã hạ xuống cơ chế chuyển giao ([bài 6](06-proposed-solution.md)).
> 4. **Chỗ đặt tính mới chuyển** từ "kiến trúc mới" sang "**benchmark mức residue đầu tiên** + mô hình thắng trên nó" ([bài 8](08-contribution.md)), hợp lệ nhờ [D-022](../../DECISIONS.md#d-022).
> 5. **Nguồn nhãn chính là bộ bão hòa** ([D-025](../../DECISIONS.md#d-025)), thước đo là **AUROC mức ô**, và cỡ mẫu thật là **91 peptide** — việc chặn duy nhất còn lại.
>
> Ba thay đổi của 13/10 vẫn đứng: lực đủ (cho bộ quét), hai mốc 0,6045 / 0,7792 là oracle, và nhãn mức residue chỉ lặp lại khoảng một nửa.

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

**Mỗi bài báo liên quan có một file riêng:** xem [papers/](papers/README.md) — **13** công trình (thêm [Schulze 2026](papers/schulze-2026.md) ngày 14/10), mỗi file nói rõ bài đó làm gì, liên quan đến đề tài ở đâu, và **chiếm chỗ nào** của mình.

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

**Câu trả lời ngắn nhất: chưa có mô hình nào được huấn luyện cho đúng nhiệm vụ này.** Bốn sản phẩm đã có
(DEGRONOPEDIA, MetaDegron, Colab của nhóm PAP, SVM của chính nhóm Zhang) đều xuất điểm ở mức **peptide
hoặc motif**, không ở mức residue.

Bằng chứng mạnh nhất cho điều đó, đo ngày 14/10: lấy mô hình tốt nhất hiện có (PAP) và dùng nó đúng cách
cho bài toán này — tính **ΔPAP** trên đúng những thay thế thí nghiệm đã làm — thì nó chỉ đạt precision@3
**0,4270**, **thấp hơn** một baseline chỉ đếm thành phần acid amin (0,4884), với p ≈ 6 × 10⁻¹⁹.

> Đừng đọc đó là "PAP tồi". PAP được huấn luyện cho **điểm của cả đoạn**, không cho **ảnh hưởng đột biến
> theo vị trí**. Đó chính là chỗ trống.

Và lý do cơ chế: PAP về cơ bản chỉ **đếm xem peptide có những acid amin nào**, không quan tâm chúng nằm ở đâu. Mình đã tự kiểm: đảo ngược thứ tự toàn bộ peptide thì điểm của nó **không đổi một chút nào** (Pearson giữa bản gốc và bản đảo = 1,000000).

Hệ quả: nếu trong cùng một peptide ta thay `A → V` ở hai vị trí khác nhau, mô hình đó **buộc phải** cho hai điểm giống hệt nhau — dù thí nghiệm nói một chỗ rất quan trọng và chỗ kia không. Chuyện này xảy ra ở **89,7% peptide** (2.353 trên 2.624).

Đây là điểm mạnh nhất của đề tài: khoảng trống **đã được chứng minh bằng toán và kiểm bằng script**, không phải phỏng đoán từ việc đọc tóm tắt bài báo.

![Khoảng trống đã chứng minh](figures/fig-07-composition-vs-context.svg)

*Sơ đồ tự dựng. Chi tiết và cách kiểm ở [bài 5](05-the-gap.md).*

### Con số phải vượt

| Mốc | precision@3 | Nghĩa là |
| --- | ---: | --- |
| Đoán ngẫu nhiên | 0,1232 | sàn |
| **ΔPAP `cnn2w7`** | **0,4270** | **mô hình degron công bố gần nhất, trên đúng nhiệm vụ này** |
| **Baseline thành phần, ước lượng trung thực** | **0,4897** | **mốc thật phải vượt** ([D-025](../../DECISIONS.md#d-025)) |
| **Trần nhãn thực nghiệm** | **0,6514** | một lần đo chấm trên nhãn lần đo kia — giới hạn trên |
| ~~0,6045~~ · ~~0,7792~~ | — | oracle **nhìn nhãn test**, không đạt được. Không dùng nữa |

Dư địa thật là **0,1617**, không phải 0,1747.

**Nếu dùng bộ bão hòa** (nguồn nhãn chính theo [D-025](../../DECISIONS.md#d-025)) thì thước đo là **AUROC
mức ô**, và dư địa còn lớn hơn:

| Mốc trên ma trận bão hòa | AUROC mức ô |
| --- | ---: |
| ΔPAP tốt nhất | **0,7692** |
| **Trần nhãn** | **0,9519** |
| **Dư địa** | **0,1827** |

Nhãn ở đây **ít nhiễu hơn nhiều** (16,7% so với 75,9%). Giá phải trả: chỉ **91 peptide**.
Nguồn: [full-data-audit mục 4–6](../../topics/degron-footprint/research/full-data-audit/README.md),
[pap-baseline](../../topics/degron-footprint/research/pap-baseline/README.md); giải thích dễ hiểu ở
[bài 5](05-the-gap.md) và [bài 10](10-data-up-close.md).

### Trạng thái thật, không tô hồng

|                        |                                                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Dữ liệu              | **Đã tải đủ bốn nguồn, kiểm SHA-256, đã audit** (13/10). Thêm **4 bảng PSI mới** repo chưa từng có. Xem [bài 10](10-data-up-close.md) |
| Mô hình              | **Chưa huấn luyện gì cả.** Chưa có một kết quả mô hình nào                                        |
| Khoảng trống         | **Đã chứng minh** (89,7%, cận chính xác, kiểm bằng script)                                             |
| Kiến trúc đề xuất | **Chỉ là đề xuất.** Có tiền lệ cho từng cơ chế. **Cổng phơi lộ đã mất vai trò** (không huấn luyện được trên nhiệm vụ chính). Lý lẽ chính nay là **ngữ cảnh vị trí**, có +0,1311 làm bằng chứng |
| Chỗ đặt đóng góp | **Đề xuất chuyển** sang benchmark + mô hình thắng trên nó ([C-7](../../DECISIONS.md)) — chờ Trọng |
| Dự phòng | **Không còn** ([D-026](../../DECISIONS.md#d-026)). Nên điểm kiểm G2 phải đặt sớm |
| Rủi ro lớn nhất     | **Nhãn mức residue chỉ lặp lại khoảng một nửa** giữa hai lần đo (Jaccard 0,4965) — đúng chỗ đề tài làm |
| ~~Lực thống kê~~ | ~~Chưa biết n ≈ 250 có đủ~~ → **đã giải quyết 13/10: đủ lực** (0,82–0,94 ở n = 221–322). Dùng split cov80 |
| ~~Việc chặn: Trọng xác nhận C-6~~ | ✅ **xong 14/10** → [D-025](../../DECISIONS.md#d-025) |
| **Việc chặn gần nhất** | **Tính lực trên n = 91** (bộ bão hòa sau ngưỡng degron). Việc chặn duy nhất còn lại trước khi huấn luyện |

---

## Ba điều đừng bao giờ nói sai

Đây là quy ước ngôn từ của đề tài, chép từ [topic-decision.md mục 8](../../topics/degron-footprint/research/topic-decision.md):

1. **Không nói "chưa ai dùng MIL cho protein".** [BioBlobs](papers/bioblobs-2025.md) (10/2025) đã dùng attention-MIL trên protein. Nói đúng: *mới ở chỗ ghép và ở **nhiệm vụ**, chưa thấy áp cho degron ở mức residue*.
2. **Không nói "dùng cấu trúc là phần mới".** [Larsen 2025](papers/larsen-2025.md) đã tính rASA và pLDDT từ AlphaFold2, và đã làm bản đồ thay thế *in silico*.
3. **Không nói "cổng phơi lộ là điểm mới" (mới 15/10).** Tiền đề đã được Voutsinos 2026, Larsen 2025, QCDPred, DEGRONOPEDIA và JoGo công bố; **hiện tượng ΔPAP đổi dấu thì Larsen 2025 đã tìm ra trên CRX** (0,54 ở IDR so với −0,19 ở vùng gấp). Và cổng **không huấn luyện được** trên nhiệm vụ chính.
4. **Không nói "PAP là mô hình tồi" (mới 15/10).** Nó thua trên nhiệm vụ residue vì **được huấn luyện cho việc khác**. Câu đúng: *chưa có mô hình nào được huấn luyện cho đúng nhiệm vụ này*.
5. **Không nói "mô hình thành phần cho bản đồ phẳng".** Ràng buộc đúng là: *trong cùng peptide, các vị trí có cùng cặp (acid amin gốc, acid amin thay vào) buộc phải nhận cùng điểm*. Bản đồ của nó không bắt buộc phẳng.

Và một điều về số liệu, **đã mạnh hơn sau 13/10**: không chỉ là "chưa hứa 0,1747", mà **con số 0,1747 đã bị bác bỏ** — nó dựa trên oracle 0,7792 đọc nhãn test. Đã tách nhiễu: **75,9%** phần dư là nhiễu đo, phần học được tối đa **8,7%** phương sai, không phải 35%. Xem [bài 10 mục 6](10-data-up-close.md).

---

## Hình trong hub này

Tất cả 16 sơ đồ trong [figures/](figures/) đều là **sơ đồ tự dựng** (SVG, mình vẽ), và đều mang nhãn `SƠ ĐỒ TỰ DỰNG` ở góc trên phải để không lẫn với hình của tác giả bài báo.

Hình gốc của tác giả nằm riêng ở [lectures/degron-footprint/assets/figures/](../degron-footprint/assets/figures/NOTICE.md), chỉ gồm hình của Voutsinos 2026 vì bài đó giấy phép CC BY-NC cho phép dùng lại. Các bài khác chỉ được dẫn link, không sao chép hình — lý do ghi trong [NOTICE.md](../degron-footprint/assets/figures/NOTICE.md).
