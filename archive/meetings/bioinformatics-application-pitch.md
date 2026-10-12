# Ý tưởng luận văn tin sinh thiên về phát triển hệ thống — buổi gặp 02/10/2026

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../DECISIONS.md).

**Một người · 14 tuần · chưa chốt đề tài · RAG hoặc CNN/MCNN tùy bài toán.**

Bản này phản ánh yêu cầu mới nhất. [Báo cáo khảo sát và nguồn](../surveys/bioinformatics-application-topics.md). Bản ATP + giao thức đánh giá và slide trước đó là phương án cũ để tham khảo, không phải lựa chọn đã được xác nhận.

## Phát biểu mở đầu khoảng 60–90 giây

“Em muốn làm luận văn tin sinh nhưng đặt trọng tâm vào xây dựng một hệ thống hỗ trợ công việc cụ thể. Trong 14 tuần và một người thực hiện, em dự định kế thừa mô hình phù hợp, rồi đánh giá cả chất lượng AI và hiệu quả sử dụng của hệ thống.

Hướng thứ nhất là hệ thống lập và rà soát hồ sơ bằng chứng về chức năng protein bằng RAG. Người dùng nhập mã protein, hệ thống thu thập chú giải và tài liệu, tạo bảng nhận định kèm nguồn để người dùng kiểm tra, chỉnh sửa và xuất hồ sơ. Phần nghiên cứu là đánh giá truy hồi đúng bằng chứng, mức độ nhận định được nguồn hỗ trợ và thời gian hoàn thành hồ sơ.

Hướng thứ hai gần các công trình của nhóm hơn: hệ thống phân tích và rà soát vị trí gắn ATP bằng CNN/MCNN. Hệ thống xử lý FASTA theo lô, hiển thị điểm theo residue, đối chiếu chú giải và lưu kết quả rà soát cùng phiên bản mô hình. Em muốn xin ý kiến thầy về nhu cầu thực tế, dữ liệu có thể dùng và mức đóng góp hệ thống cần đạt.”

## Hai phương án mang ra trao đổi

| | A — Hồ sơ bằng chứng protein | B — Rà soát vị trí gắn ATP |
|---|---|---|
| Tên đề tài dự kiến | Xây dựng hệ thống hỗ trợ tổng hợp và rà soát bằng chứng về chức năng protein sử dụng RAG | Xây dựng hệ thống hỗ trợ phân tích và rà soát vị trí gắn ATP trên protein RTK sử dụng CNN đa cửa sổ |
| Người dùng dự kiến | Sinh viên/thành viên lab tổng hợp thông tin protein | Người nghiên cứu rà soát kết quả dự đoán trên lô protein |
| Đầu vào | Danh sách accession thuộc một họ/loài xác định | FASTA trong phạm vi RTK đã thống nhất |
| Đầu ra | Hồ sơ có nhận định, nguồn và trạng thái duyệt | Bản đồ residue, bảng điểm, annotation và ghi chú |
| Công việc cốt lõi | Đối chiếu nguồn → duyệt → xuất báo cáo | Xử lý lô → đối chiếu vị trí → ghi nhận rà soát |
| AI | Truy hồi bằng chứng và sinh theo mẫu | CNN/MCNN có sẵn hoặc baseline tái lập được |
| Đánh giá chính | Truy hồi, dẫn nguồn đúng, mức hoàn thành hồ sơ | Chất lượng dự đoán, lỗi ánh xạ, mức hoàn thành rà soát |
| Điều kiện quyết định | Có nguồn đủ, ngân sách suy luận và người chấm bằng chứng | Có pipeline/nhãn và tài nguyên chạy được |

**Khuyến nghị để thảo luận:** A hợp mong muốn thiên về hệ thống; B hợp hơn nếu thầy cung cấp nền mô hình và xác nhận quy trình rà soát có nhu cầu. Đây là đề xuất, chưa phải quyết định của sinh viên/GVHD.

Phương án thứ ba nếu thầy không chọn A/B: **hệ thống tìm kiếm và sàng lọc bộ dữ liệu GEO theo tiêu chí nghiên cứu bằng RAG**; sản phẩm là shortlist dataset kèm bằng chứng đạt/không đạt/chưa rõ từng tiêu chí. Giới hạn vào một miền và metadata, chưa làm pipeline RNA-seq.

## Dàn ý 5 slide, khoảng 5 phút

1. **Bài toán và phạm vi:** một người/14 tuần; người dùng thực hiện một công việc tin sinh; AI là thành phần của hệ thống.
2. **Hướng A:** accession → bảng bằng chứng → hồ sơ có dẫn nguồn → người dùng duyệt → xuất. Minh họa bằng wireframe/mô tả, không nói đã có sản phẩm.
3. **Hướng B:** FASTA → job → bản đồ residue + annotation → rà soát → xuất có model version.
4. **Đóng góp và đánh giá:** một RQ về chất lượng AI, một RQ về tác vụ người dùng; baseline và bộ chấm; nhận thức rõ công cụ đã có.
5. **Kế hoạch và việc xin thầy quyết:** tuần 1–2 xác nhận dữ liệu/baseline, tuần 3–8 MVP, tuần 9–12 đánh giá/hoàn thiện, tuần 13–14 báo cáo/bảo vệ.

## Câu trả lời cho các câu hỏi dễ gặp

**“Mới ở đâu khi RAG/CNN đã có?”**

“Em chưa đặt mục tiêu tạo kiến trúc mới. Em đề xuất một quy trình có thể kiểm tra nguồn và lưu quyết định trong phạm vi người dùng cụ thể, rồi so sánh với cách làm hiện tại. Em cần thầy xác nhận mức đóng góp ứng dụng và thực nghiệm này phù hợp luận văn.”

**“A có phải chỉ là chatbot?”**

“Đầu ra chính là hồ sơ có cấu trúc và bảng bằng chứng để người dùng duyệt. Hệ thống phải xử lý đúng định danh/loài, gắn nguồn từng nhận định, lưu phiên bản và xuất hồ sơ. Chat tự do không phải tính năng bắt buộc.”

**“Đã có ai làm chưa?”**

“Có các tiền lệ như [GeneGPT](https://pmc.ncbi.nlm.nih.gov/articles/PMC10904143/), [BioChatter](https://github.com/biocypher/biochatter), bản thảo [2D-ProteinRAG](https://arxiv.org/abs/2605.17261) và [RTK_RAG](https://github.com/B1607/RTK_RAG). Em không khẳng định đây là ý tưởng đầu tiên. Em sẽ đối chiếu chức năng và đánh giá trên công việc cụ thể của nhóm.”

**“Chứng minh hệ thống tốt thế nào?”**

“Đánh giá riêng chất lượng AI trên test giữ lại, rồi đo tính đúng đắn và thời gian hoàn thành tác vụ bằng cùng một bộ tình huống. Nếu tuyển được người dùng phù hợp em làm nghiên cứu thử nghiệm nhỏ; nếu chưa có, em sẽ ghi rõ giới hạn thay vì tuyên bố cải thiện năng suất.”

**“14 tuần có quá rộng không?”**

“Em chỉ làm một họ protein hoặc một miền dữ liệu, một chức năng AI chính, một quy trình xuyên suốt. Cuối tuần 2 phải có dữ liệu và baseline chạy được. Em không đưa sinh protein, 3D hay pipeline omics tổng quát vào MVP.”

## Năm điều cần hỏi và ghi lại

- Thầy ưu tiên A hay B, và có chấp nhận đóng góp hệ thống + đánh giá thực nghiệm khi kế thừa mô hình không?
- Ai có thể cung cấp tình huống sử dụng và kiểm tra nhãn/bằng chứng?
- Nếu chọn B, nhóm có pipeline, trọng số và dữ liệu nào cho phép dùng?
- Nếu chọn A, chọn họ protein nào và có thể dùng LLM qua API không?
- Thầy đồng ý mốc kiểm tra cuối tuần 2 và phương án thu hẹp khi dữ liệu/tài nguyên không đủ chứ?

## Điều đã biết và chưa được nói như kết quả

Đã biết: theo [đề cương CT553H](../../resources/course/CT553H.pdf), phát triển ứng dụng 40%, báo cáo khoa học 40%, thái độ/trình bày 20%; các nguồn/công trình nêu trên tồn tại; phạm vi cá nhân/14 tuần đã được xác nhận.

Chưa có: demo, số đo độ chính xác/tốc độ, khảo sát nhu cầu, gold set được chuyên gia duyệt, xác nhận pipeline chạy được hoặc cam kết công bố. Không nói “đã chứng minh RAG tốt hơn”, “GPU chỉ cần vài giờ”, “chưa có công cụ nào làm” hay “AI xác nhận chức năng sinh học”.
