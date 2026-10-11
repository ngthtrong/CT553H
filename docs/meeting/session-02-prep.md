# Chuẩn bị buổi gặp GVHD lần 2 (tuần 6) — đề tài `degron-e3-specificity`

> Lập ngày 11/10/2026, **cập nhật cùng ngày (khuya)** sau khi đếm xong nhãn E3. Đề tài trình bày: **Dự đoán footprint degron ở mức residue bằng học đa thể hiện với cổng phơi lộ cấu trúc, trên nhãn đột biến thực nghiệm.** Quyết định của sinh viên; **chưa có phê duyệt GVHD**.
>
> **Đề tài đã tái định tâm.** Tên cũ *"dự đoán đặc hiệu E3–degron… có điều kiện"* đã bỏ: phép đếm từ dữ liệu thô cho thấy chỉ **một** E3 có đủ 5 peptide. Chi tiết: [audit nhãn](../common/deep-research/research_notes/degron-e3-labels/README.md).
>
> Tài liệu trình bày chính là [presentation.html](../topics/degron-e3-specificity/01-idea/presentation.html) (mở bằng `file://`, 7 mục, đúng bố cục GVHD yêu cầu ở [biên bản lần 1, mục 2 và 3](session-01-minutes.md)). File này chỉ là kịch bản nói và cây quyết định; **không lặp lại nội dung của trang trình bày**.

## 1. Hai việc buổi gặp phải đạt được

Theo [biên bản lần 1, mục 5](session-01-minutes.md), tuần 6 là mốc "báo cáo lại đề tài rõ ràng". Nhưng với trạng thái hiện tại, buổi này cần ra **hai quyết định**, không chỉ là báo cáo:

1. **Chốt thước đo chính.** Đây là việc quan trọng nhất và không thể hoãn. Nếu GVHD yêu cầu thắng trên thang điểm khối thì đề tài phải thiết kế lại — và phải biết điều đó ở tuần 6, không phải tuần 12.
2. **Biết mức đóng góp tối thiểu ở tiêu chí 2.** Kiến trúc của em ghép các cơ chế đã có và áp vào một bài toán chưa ai làm. Cần biết thầy coi mức đó là đủ hay không, vì nếu không đủ thì phải đổi ngay ở tuần 6, không phải tuần 12.

Mọi câu khác có thể trả lời sau buổi gặp.

## 2. Trạng thái trung thực phải nói ra, không chờ thầy phát hiện

| Điều | Nói thế nào |
|---|---|
| **Đề tài đã đổi trục trong một ngày, và vì sao** | Em chốt đề tài sáng 11/10 với trục "đặc hiệu E3". Tối cùng ngày em đếm nhãn từ dữ liệu thô và thấy chỉ **1 trong 10 E3** có đủ 5 peptide, 6 E3 có đúng 1 peptide. Nên em bỏ trục đó thay vì để lộ ra ở tuần 12. **Đây là điểm mạnh của cách làm, không phải điểm yếu** — nhưng phải trình bày đúng thứ tự: phép đo trước, quyết định sau |
| **Đóng góp dương giờ đã có cơ sở** | Thước đo chính là **bản đồ độ nhạy đột biến theo residue**, có **256.711 phép đo** để huấn luyện và **2.624 peptide có footprint** để chấm. Không còn phụ thuộc con số chưa đếm nào |
| **Kiến trúc mới sẽ không thắng trên thang điểm khối** | Đã biết trước: gộp max làm sụt 0,824 → 0,344, entropy theo vị trí 3,294 trên tối đa 3,401. Thang đó không thưởng cho việc khu trú. Nhưng footprint thật **khu trú ở median 3 trên 28 vị trí** — đó là chỗ kiến trúc có đất |
| **Tính mới của kiến trúc là ở chỗ ghép, không ở cơ chế** | BioBlobs (10/2025) đã dùng MIL có cổng attention trên protein; OmniESI (2025) đã dùng điều biến có điều kiện. Em không nói "chưa ai dùng" cho toàn bộ kiến trúc |
| **Và MIL không còn bắt buộc khi đã có nhãn mức residue** | Em tự nói ra: một đầu hồi quy theo vị trí là mô hình tự nhiên. Lý do giữ cấu trúc túi là để dùng được **cả** nhãn yếu mức đoạn (212.658) lẫn nhãn mạnh mức residue (256.711) trong một mô hình. Em sẽ chạy **đối chứng không có MIL**, và nếu nó đủ thì em báo đúng như vậy |
| **Đặc hiệu E3 đã có công cụ** | MetaDegron (2024) dự đoán degron theo từng E3 cho 21 E3 và đã có máy chủ web. Khác biệt của em không còn nằm ở chữ "đặc hiệu E3" nữa, mà ở **đơn vị dự đoán** (bản đồ theo residue) và **nguồn nhãn** (phép đo thực nghiệm thay cho ~300 degron curate) |
| **Tiêu chí 5 là tiêu chí yếu nhất** | Ba sản phẩm đã tồn tại: DEGRONOPEDIA, máy chủ MetaDegron, Colab của tác giả PAP |
| **Một phản biện phải tự nêu** | Trên trục "dự đoán bản đồ thay thế" nói chung, một khung học máy 2025 báo rằng **6 điểm thay thế mỗi residue đủ suy ra phần còn lại với ~90%** độ chính xác trên dữ liệu quét đột biến sâu. Em phải trích và nói rõ bài toán của em khác ở chỗ nào |

Không dùng chữ "đầu tiên" ở bất kỳ đâu. Giữ đúng [quy ước ngôn từ của đề tài](../topics/degron-e3-specificity/01-idea/topic-decision.md) (mục 8).

## 3. Nếu thầy hỏi "vì sao đề tài này, không phải hướng khác"

Câu này có khả năng được hỏi, và trả lời trung thực là:

- **Mạnh nhất ở chất lượng và quy mô nhãn.** Mọi nhãn là nhãn thực nghiệm: điểm tile từ reporter assay, PSI từ sàng lọc, và **256.711 phép đo đột biến theo từng vị trí** mà em đã tự tải và đếm. Không nhãn nào do pipeline của đề tài tự sinh. Đây là lý do hướng senescence scRNA-seq bị loại — nhãn ở đó là điểm chữ ký do chính pipeline sinh ra.
- **Mạnh nhất ở tiêu chí 4, và giờ nó không còn là "chỉ XAI".** Bản đồ theo residue là **đầu ra được giám sát**, chấm bằng 2.624 footprint cộng 249 bản đồ thay thế đầy đủ, kèm một đối chứng âm đã đo được (mô hình bất biến hoán vị phải cho bản đồ phẳng). Các hướng còn lại trong repo chỉ đối chiếu được với cơ sở dữ liệu motif.
- **Yếu nhất ở tiêu chí 2 so với kỳ vọng "kiến trúc chưa ai dùng".** Nói thẳng mức độ: mới ở cách ghép và chỗ đặt cổng.

**Không nói** rằng đề tài này đã thắng một cuộc so sánh có hệ thống với các hướng khác — [phép so sánh đó chưa được làm](../common/work-log.md). Nếu thầy muốn thấy các hướng đã cân nhắc thì dẫn [khảo sát aging và cancer](../common/deep-research/reports/aging-cancer-deep-dive.md) và [đánh giá dark kinome](../common/deep-research/reports/main-topic-decision.md).

## 4. Câu hỏi xin ý kiến, xếp theo mức đổi kế hoạch

| # | Câu hỏi | Câu trả lời đổi gì |
|---|---|---|
| 1 | **Thước đo nào tính?** Em đề nghị bản đồ độ nhạy theo residue (Spearman theo peptide + precision@3 trên 2.624 footprint), không phải Pearson trên thang điểm khối | Nếu thầy yêu cầu thắng thang điểm khối → **thiết kế lại**, xem mục 5 |
| 2 | **Mức đóng góp tối thiểu ở tiêu chí 2:** một kiến trúc ghép từ các cơ chế đã có nhưng chưa ai áp cho bài toán này có đủ không? | Nếu không đủ → phải tìm một cơ chế mới thật, hoặc đổi hướng |
| 3 | **Nếu đối chứng không có MIL đã đủ tốt**, thầy coi đó là kết quả dùng được hay là thất bại? | Quyết định em có dám chạy đối chứng trung thực hay không — em sẽ chạy dù sao, nhưng cần biết cách trình bày |
| 4 | **Nguồn GPU.** Kiến trúc cần embedding mức residue: ESM-2 650M mất ~11 giờ một lượt trên máy em, cache cần 32,7 GB so với RAM 7 GB | Không có GPU → chỉ dùng được bản 35M, phải ghi giới hạn trong luận văn |
| 5 | **Phạm vi tối thiểu của website**, khi đã có ba sản phẩm tồn tại | Quyết định ngân sách thời gian tuần 12–13 |
| 6 | **Hình thức báo cáo tuần 6** — câu này còn treo từ biên bản lần 1 | Chỉ ảnh hưởng cách trình bày |

Một việc nhỏ cần làm rõ trong nội bộ trước buổi gặp: ngày 10/10 ghi nhận **có GPU ổn định hơn Colab**, nhưng mục 9 của [topic-decision.md](../topics/degron-e3-specificity/01-idea/topic-decision.md) ghi máy **không có GPU**. Phải thống nhất trước khi hỏi câu 4.

## 5. Cây quyết định sau buổi gặp

| Thầy trả lời câu 1 | Việc tiếp theo |
|---|---|
| Chấp nhận thước đo theo residue | **Trường hợp tốt nhất.** Chạy kế hoạch tuần 7–15 ở mục 6.2 của trang trình bày. Việc đầu tiên: pipeline dữ liệu cho bộ đột biến quét, chia theo peptide, cộng baseline PAP và đối chứng không có MIL |
| Yêu cầu thắng thang điểm khối | Thiết kế lại. Thang đó đã bão hòa ở +0,0032 theo phép đo của chính tác giả, nên không nhận lời hứa thắng nó. Đưa lại bảng so sánh các hướng và chọn lại |
| Muốn giữ trục đặc hiệu E3 | Trình bày bảng đếm: 10 E3, 1 lớp đủ mẫu, 6 lớp một mẫu, bền với 36 ngưỡng. Nếu thầy vẫn muốn, phạm vi phải thu về **một** E3 (KLHL15, 13 peptide) và nói rõ đó là ca nghiên cứu |

## 6. Việc phải làm trước buổi gặp

- [ ] Thống nhất tình trạng GPU (mục 4).
- [ ] Mở `presentation.html` kiểm một lượt trên máy sẽ dùng để trình bày, gồm chế độ in nếu cần bản PDF.
- [ ] Đọc lại [mục 3 biên bản lần 1](session-01-minutes.md): thầy yêu cầu phần khảo sát **phân nhóm theo phương pháp kèm ưu, nhược, hạn chế** — bảng ở mục 2.2 của trang trình bày đã đúng định dạng này, gồm bảy nhóm A–G.
- [x] ~~Đếm nhãn E3~~ — **đã xong 11/10/2026 (khuya)**, và kết quả đã đổi trục đề tài. Kết quả nằm trong trang trình bày mục 4 và mục 6.
- [ ] Chuẩn bị trả lời câu "vì sao đổi đề tài trong một ngày" — xem mục 2, dòng đầu.

## 7. Sau buổi gặp

Ghi `session-02-minutes.md` theo cùng cấu trúc biên bản lần 1: nhận xét về định hướng, yêu cầu về trình bày, yêu cầu về khảo sát, cách áp năm tiêu chí, mốc thời gian, và những điều cần làm rõ lần sau. Phân biệt rõ **lời GVHD** với **đánh giá của sinh viên** — biên bản lần 1 làm đúng việc này và cần giữ.
