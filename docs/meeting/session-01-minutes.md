# Biên bản buổi gặp GVHD lần 1 — 02/10/2026

> Nội dung được tổng hợp từ ghi chép của sinh viên sau buổi gặp, cập nhật theo phần bổ sung ngày 02/10/2026 (mốc thời gian ở mục 5 và hướng ưu tiên ở mục 6); không phải bản chép nguyên văn lời GVHD.
>
> Đề tài trình bày: **Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu** (`rtk-atp-applicability`). Xem [thuyết minh đề tài](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md) và [dàn ý trình bày](2026-10-02-rtk-atp-slide-outline.md).

## 1. Nhận xét về định hướng đề tài

Đề tài RTK–ATP **không bị từ chối**. Tuy nhiên, sau khi xem yêu cầu học phần, GVHD góp ý rằng nếu có thể thì sinh viên **nên thay đề tài này bằng đề tài khác** — không phải tìm thêm để so sánh rồi tự chọn; hướng **aging (lão hóa)** hoặc **cancer (ung thư)** sẽ phù hợp hơn hướng ATP đang trình bày.

**Định hướng của sinh viên sau buổi gặp (cập nhật 02/10/2026): đề tài RTK–ATP gần như chắc chắn sẽ được thay thế; hai hướng aging và cancer đang được khảo sát song song để so sánh, chưa chọn hướng nào.** Việc “chốt đề tài” trong các tài liệu trước buổi gặp chỉ phản ánh lựa chọn ở thời điểm chuẩn bị. Đây là định hướng của sinh viên, phân biệt với góp ý của GVHD ở trên. Chi tiết ở mục 6.

## 2. Yêu cầu về cách trình bày và động cơ nghiên cứu

Phần trình bày cần rõ ràng, thể hiện sinh viên hiểu bài toán và giúp người nghe nắm được:

- **Bài toán nghiên cứu là gì?** Cần giải quyết nhiệm vụ nào, đầu vào và đầu ra là gì?
- **Vì sao cần thực hiện nghiên cứu này?** Vấn đề nào còn tồn đọng, vì sao vấn đề đó cần được giải quyết?
- **Nghiên cứu dự kiến giải quyết phần nào của vấn đề?** Cần làm rõ mối liên hệ giữa hạn chế hiện có và đóng góp đề xuất.

GVHD đặc biệt nhấn mạnh lý do thực hiện nghiên cứu. Khi chỉnh sửa bản trình bày RTK–ATP hoặc chuẩn bị hướng khác, cần làm rõ động cơ nghiên cứu trước khi đi sâu vào mô hình và kỹ thuật.

## 3. Yêu cầu về khảo sát các nghiên cứu trước (history research)

Phần khảo sát cần có phân tích theo trình tự:

1. **Phân nhóm nghiên cứu theo phương pháp:** sắp xếp các công trình có liên quan thành những nhóm phương pháp phù hợp với bài toán.
2. **Đánh giá từng nhóm và từng công trình:** phân tích ưu điểm, nhược điểm và những hạn chế còn tồn tại.
3. **Đối chiếu với đề tài đã chọn:** chỉ rõ đề tài dự kiến cải thiện ở điểm nào so với các nghiên cứu trước.

Khi biên soạn lại phần khảo sát, có thể dùng bảng gồm: nhóm phương pháp, công trình tiêu biểu, ưu điểm, hạn chế và điểm đề tài dự kiến cải thiện. Đây là gợi ý tổ chức tài liệu sau buổi gặp; các điểm cải thiện vẫn cần được chứng minh bằng khảo sát và thực nghiệm.

## 4. Năm tiêu chí lựa chọn và đánh giá đóng góp của đề tài

| STT | Tiêu chí | Nội dung góp ý của GVHD |
|---|---|---|
| 1 | **Tính mới của đề tài hoặc hướng nghiên cứu** | Tìm đề tài mới, hướng đi mới hoặc vấn đề chưa có người thực hiện. |
| 2 | **Đề xuất hoặc cải tiến phương pháp** | Đóng góp có thể nằm ở việc phát triển phương pháp, chẳng hạn chuyển từ CNN sang mCNN hoặc tiếp tục cải tiến mCNN. |
| 3 | **Sử dụng phương pháp mới** | Xem xét khả năng áp dụng phương pháp mới cho bài toán. GVHD minh họa bằng sự chuyển dịch từ PSSM sang PLM trong nghiên cứu chuỗi amino acid, rồi đặt câu hỏi liệu có thể tìm thêm phương pháp nào mới mẻ hơn hay không. |
| 4 | **XAI — khả năng giải thích của mô hình** | Giải thích được cách mô hình hoạt động và vì sao mô hình đạt kết quả cao cũng là một dạng đóng góp nghiên cứu. |
| 5 | **Xây dựng ứng dụng hoặc website** | Vì đây là luận văn thuộc khoa Kỹ thuật phần mềm, cần xây dựng ứng dụng hoặc website để đưa kết quả nghiên cứu vào sử dụng. Đây là thành phần **không thể thiếu**. |

**Ghi chú về ví dụ ở tiêu chí 3:** Theo ghi chép của sinh viên, GVHD đề cập PSSM dưới dạng ma trận, hạn chế liên quan đến tính thứ tự của chuỗi amino acid và thời gian so sánh, rồi đối chiếu với việc sử dụng PLM phổ biến trong giai đoạn gần đây. Đây là phần ghi lại cách diễn giải trong buổi trao đổi; nội dung kỹ thuật cần được đối chiếu tài liệu gốc khi đưa vào phần khảo sát chính thức.

**Kỳ vọng của GVHD về số tiêu chí: càng đạt nhiều tiêu chí càng tốt.** Đây không phải danh sách để chọn lấy một trục, và tiêu chí 5 là thành phần không thể thiếu.

Ghi chép không xác định trọng số từng tiêu chí, ngưỡng tối thiểu, hay điểm đánh giá cụ thể cho RTK–ATP; chưa có căn cứ để kết luận đề tài đạt hay không đạt theo bộ tiêu chí này.

**Lưu ý của sinh viên về tính khả thi:** với phần thực hiện còn khoảng 8–9 tuần (mục 5), nhắm đồng thời cả bốn tiêu chí 1–4 cộng tiêu chí 5 là rủi ro cao. Việc cần làm là bàn với GVHD về **thứ tự ưu tiên** giữa các tiêu chí, chứ không tự ý giảm số tiêu chí — xem mục 7.

## 5. Mốc thời gian GVHD nêu

| Mốc | Nội dung |
|---|---|
| **Tuần 4** | Thời điểm hiện tại, tức buổi gặp này |
| **Tuần 6** | **Báo cáo lại đề tài rõ ràng với GVHD** |
| **Tuần 14 hoặc 15** | Tuần báo cáo |

Những điểm cần tính tới khi lập kế hoạch:

- Từ tuần 4 đến mốc báo cáo tuần 6 còn **khoảng hai tuần** để chốt hướng và trình bày lại cho rõ. Trong khoảng thời gian này, khảo sát song song nhiều hướng sẽ khó đạt độ sâu mà mục 2 và mục 3 yêu cầu.
- **Kế hoạch 14 tuần trong [thuyết minh trước buổi gặp](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md) không còn khớp mốc thực tế.** Tính từ tuần 4 tới tuần 14–15 còn khoảng **10–11 tuần**, trong đó hai tuần đầu dành cho việc chốt và báo cáo lại đề tài. Phần thực hiện còn lại vào khoảng **8–9 tuần**, và phải chứa cả ứng dụng/website ở tiêu chí 5.
- Báo cáo tuần 6 nên đáp ứng đúng yêu cầu ở mục 2 và mục 3: rõ bài toán, rõ lý do cần nghiên cứu, và phần khảo sát đã phân nhóm theo phương pháp kèm đánh giá ưu/nhược điểm.
- Ghi chép chưa xác định **hình thức và mức chi tiết** của báo cáo tuần 6 (slide, văn bản, hay đề cương sơ bộ); xem mục 7.

## 6. Hướng xử lý dự kiến sau buổi gặp

**RTK–ATP gần như chắc chắn sẽ được thay thế. Hai hướng GVHD gợi ý — aging và cancer — đang được khảo sát song song để so sánh, chưa chọn hướng nào.** Quyết định cập nhật ngày 02/10/2026, sau khi đối chiếu danh mục công bố của GVHD (xem [advisor/README.md](../common/advisor/README.md)): hướng **aging** có điểm neo ngay ở công trình mới nhất của GVHD (SirtSAGE, họ sirtuin), còn hướng **cancer** chưa tra được công trình nào của GVHD — nhánh neoantigen thuộc danh mục Prof Ou. Vì khác biệt này chỉ là suy luận từ danh mục công bố và danh mục có thể chưa đầy đủ, sinh viên chọn khảo sát cả hai rồi so sánh trên cùng bộ tiêu chí.

Các việc dự kiến dưới đây phục vụ việc tìm đề tài mới trong hai hướng được gợi ý; chưa phải phân công đã được GVHD xác nhận:

- Khảo sát các bài toán thuộc **cả hai hướng aging và cancer**, rồi so sánh trên cùng bộ tiêu chí: vấn đề tồn đọng, đóng góp dự kiến, **dữ liệu công khai có tập test độc lập hay không**, mức khớp với danh mục GVHD, và khả năng hoàn thành trong thời gian còn lại.
- Viết lại phần giới thiệu để làm rõ bài toán, động cơ nghiên cứu và vấn đề cần giải quyết.
- Tổ chức lại phần khảo sát theo nhóm phương pháp, đánh giá ưu/nhược điểm và xác định điểm cải thiện dự kiến của đề tài.
- Làm rõ đóng góp đề xuất liên quan đến những tiêu chí nào trong mục 4; tránh mặc định rằng dùng một mô hình mới hoặc thêm tính năng giải thích đã đủ tạo thành đóng góp.
- Xác định ứng dụng hoặc website dự kiến, người dùng và cách kết quả nghiên cứu được sử dụng trong sản phẩm.

Hai lưu ý về thứ tự thực hiện, do giới hạn thời gian ở mục 5:

- **Kiểm tra dữ liệu công khai có sẵn hay không nên làm sớm nhất** trong hướng được chọn, vì đây là yếu tố có thể loại một hướng đi nhanh nhất. Hướng peptide kích thích IL-6 trước đây bị loại chính vì dữ liệu công khai không có tập kiểm tra độc lập.
- Với mỗi hướng, cần **đọc trước các công trình của GVHD trong cùng nhánh** để xác định phần đã được thực hiện, trước khi xác định đóng góp dự kiến. Việc này liên quan trực tiếp tới tiêu chí 1 ở mục 4.

Đối với RTK–ATP, bản đề xuất hiện có tập trung vào giao thức đánh giá kiểm soát rò rỉ, tín hiệu miền áp dụng và hệ thống dự đoán. Tài liệu này được giữ làm tham khảo cho hướng cũ; trọng tâm tiếp theo là xác định đề tài mới trong hai hướng aging và cancer.

## 7. Những nội dung cần làm rõ ở lần trao đổi tiếp theo

- GVHD có gợi ý bài toán hoặc dữ liệu cụ thể nào trong hướng cancer, phù hợp với định hướng hiện tại của sinh viên không?
- Các tiêu chí 1–4 được áp dụng như thế nào đối với phạm vi luận văn này?
- Phạm vi tối thiểu của ứng dụng/website và tiến độ chuẩn bị đề xuất tiếp theo là gì?

Cần bổ sung vào danh sách trên:

- GVHD có **bài toán hoặc đề tài nào đang mở trong nhóm** mà sinh viên có thể nhận, hay sinh viên tự đề xuất?
- **Hình thức và mức chi tiết của báo cáo tuần 6** (mục 5).
- **Thứ tự ưu tiên giữa năm tiêu chí** nếu không thể đạt hết trong 8–9 tuần: tiêu chí nào quan trọng nhất?
- **Hướng cancer cụ thể là nhánh nào**, khi danh mục công bố của GVHD (xem [advisor/README.md](../common/advisor/README.md)) không có công trình về cancer — nhánh neoantigen là công trình của Prof Ou, không phải của GVHD.
- **Nguồn GPU** sinh viên có thể sử dụng — câu này giữ lại từ thuyết minh trước buổi gặp vì vẫn còn giá trị với mọi hướng.

**Về các câu hỏi trong [thuyết minh trước buổi gặp](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md):** ghi chép không xác định được câu nào đã được trao đổi trực tiếp trong buổi gặp. Sinh viên đánh giá các câu còn lại — đóng góp dạng giao thức có đủ hay không, kết quả âm có được chấp nhận, phiên bản đánh giá nào tạo ra số liệu RTK_RAG, có trọng số hoặc embedding RTK_RAG để đối chiếu không, nhãn của kho RAG-244 — **không còn phù hợp để hỏi lại**, vì tất cả đều gắn với phạm vi RTK–ATP. Ghi lại ở đây để thấy các câu này đã được cân nhắc và gác lại, không phải bị bỏ sót; nếu sau này quay lại hướng RTK–ATP thì cần đưa trở lại.

## Tài liệu liên quan

- [Chuẩn bị buổi gặp lần 1](session-01-prep.md).
- [Dàn ý và kịch bản trình bày](2026-10-02-rtk-atp-slide-outline.md).
- [Thuyết minh đề tài RTK–ATP](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md).
- [Quyết định và phạm vi đề tài trước buổi gặp](../topics/rtk-atp-applicability/01-idea/topic-decision.md).
- [Danh sách và trạng thái các đề tài](../topics/README.md).
