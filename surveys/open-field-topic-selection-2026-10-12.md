# Chốt đề tài sau khảo sát mở lĩnh vực — 12/10/2026

> **Báo cáo lịch sử:** lựa chọn tại thời điểm viết thuộc [D-016](../DECISIONS.md#d-016). Trạng thái hiện hành chỉ ghi tại [DECISIONS.md](../DECISIONS.md#d-021).

> **Lịch sử quyết định:** các câu "chốt / quyết định / khuyến nghị" trong file này phản ánh thời điểm viết, có thể đã bị thay. Trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../DECISIONS.md).

**Quyết định: chọn `budgeted-microservice-rca` làm đề tài chính để xây dựng đề cương và trình GVHD.** Tên: **Định vị nguyên nhân sự cố microservice bằng lựa chọn bằng chứng thích ứng theo giá trị chẩn đoán và ngân sách truy vấn.** Phương án dự phòng duy nhất: degron với nhãn đột biến thực nghiệm, theo [audit mới](../topics/degron-footprint/research/composition-context-audit.md), bỏ tuyên bố ΔPAP hạng 1 và scanning là lề ma trận.

Đây là quyết định lựa chọn theo yêu cầu sinh viên ngày 12/10, không phải phê duyệt của GVHD hoặc xác nhận phương pháp đã cải thiện kết quả. **Dữ liệu đã kiểm tra trực tiếp; đóng góp phương pháp còn là giả thuyết.** Không tiếp tục mở danh sách ứng viên vô hạn. Kết quả khảo sát hôm nay đủ để chốt phạm vi; thí nghiệm sau đó quyết định mức tuyên bố, không được viết trước kết quả dương.

## 1. Cách đánh giá

Đã đọc CLAUDE.md, chỉ dẫn hiện hành, [bảng đề tài](../topics/README.md), nhật ký, quyết định DARKIN/degron, audit Sirtuin/RTK và ứng viên legal QA. Yêu cầu mới nhất bỏ giới hạn lĩnh vực; vẫn khảo sát nghiêm túc công cụ phục vụ quy trình tin sinh học trước khi chọn hướng ngoài lĩnh vực.

Khung GVHD là [năm tiêu chí trong biên bản, mục 4](../project/meetings/2026-10-02-session-01/minutes.md): tính mới; cải tiến phương pháp; dùng phương pháp mới; XAI; ứng dụng bắt buộc. GVHD **không quy định trọng số**. Bổ sung chuẩn đánh giá nghiên cứu: [ACM SIGSOFT](https://www2.sigsoft.org/EmpiricalStandards/) nhấn mạnh tính hợp lệ và tái lập theo loại nghiên cứu; [NeurIPS 2026](https://neurips.cc/Conferences/2026/ReviewerGuidelines) xét chất lượng, rõ ràng, ý nghĩa và tính mới, cho phép đóng góp bằng hiểu biết/hiệu quả mới từ kỹ thuật có sẵn. Không đồng nhất nghiên cứu tốt với kiến trúc mới hoặc app đẹp.

Ba cổng không được che bởi điểm tổng:

- **G1:** có đáp án/đại lượng đánh giá độc lập với mô hình đề xuất; biết dữ liệu truy cập được và đơn vị độc lập là gì.
- **G2:** có phép đo lợi ích dương, đối thủ mạnh và điều kiện bác bỏ. Hôm nay chỉ xét **thiết kế kiểm chứng G2**; chưa ứng viên nào có kết quả dương của phương pháp mới.
- **G3:** sản phẩm có người dùng và thao tác hữu ích cụ thể, triển khai trong nguồn lực hiện có.

Trọng số do người khảo sát chọn: đóng góp kiểm chứng được 30%, ý nghĩa 25%, khoảng trống còn lại 20%, dữ liệu 15%, thực hiện/sản phẩm 10%. Thang 1–5 là **phán đoán lựa chọn**, không phải số đo khách quan. Độ tin cậy chứng cứ được báo riêng. Độ khớp GVHD là yếu tố triển khai, không được dùng để bỏ qua thiếu nhãn hoặc khoảng trống đã được giải quyết.

## 2. Đối chiếu các hướng

| Hướng | Đóng góp | Ý nghĩa | Khoảng trống | Dữ liệu | Thực hiện | /100 | Chứng cứ và lý do quyết định |
|---|---:|---:|---:|---:|---:|---:|---|
| **Chọn bằng chứng cho RCA dưới ngân sách** | 4 | 4 | 3 | 5 | 4 | **79** | G1/G3 rõ; kiểm tra toàn bộ index và sáu ca thô. G2 có kiểm chứng cùng bộ xếp hạng. Tính mới vừa phải, phải so với VerifyRCA và AFA. **Chọn chính** |
| Công cụ proteomics chọn/tích hợp quy trình có ràng buộc sai phát hiện | 3 | 4 | 3 | 4 | 3 | 68 | Nhãn spike-in tốt, app tự nhiên; OpDEA/SCPDA đã tối ưu, tích hợp và cung cấp phần mềm. Cải thiện FDR cần thống kê sâu và audit dữ liệu riêng; chưa thực hiện |
| Degron hiệu ứng đột biến theo ngữ cảnh | 4 | 3 | 3 | 5 | 3 | 72 | Audit trực tiếp tốt nhất trong bio; câu hỏi có ý nghĩa thực nghiệm. Hạn chế ngữ cảnh assay, saturation chưa chuẩn hóa và app ưu tiên giả thuyết. **Dự phòng** |
| Công cụ chia benchmark bio chống rò rỉ | 2 | 4 | 2 | 4 | 4 | 60 | DataSAIL đã có chia nhiều chiều, cân bằng và nhiều loại dữ liệu; giao diện bao quanh chưa là cải tiến đủ mạnh |
| Hợp nhất/ánh xạ dữ liệu MAVE cho phân tích biến thể | 2 | 4 | 2 | 4 | 3 | 58 | MaveDB đã có mapping, provenance và tích hợp; cần tìm một lớp lỗi mới có chuẩn đáp án trước khi thành đề tài |
| Legal QA tiếng Việt có kiểm chứng trích dẫn | 3 | 4 | 2 | 2 | 4 | 60 | Câu hỏi chuẩn có sẵn; nhãn trích dẫn và truy vấn đời thường chưa được audit/thu thập. G1 cho **đóng góp chính** còn mở; chưa ưu tiên |
| Phát hiện malware khi lệch thời gian, có từ chối | 3 | 4 | 2 | 3 | 3 | 61 | EMBER2024 công khai; selective/conformal/drift đã có tiền lệ gần. Không có pilot; nhãn AV consensus và mục đích app cần giới hạn |
| Dự báo tuổi thọ pin từ giai đoạn đầu | 3 | 4 | 2 | 3 | 3 | 61 | BatteryLife có nhiều nguồn; chuyển miền đã có. Đơn vị là cell, không phải tất cả cửa sổ sinh ra; endpoint xuyên assay cần audit |
| Bản đồ ngập/hư hại từ ảnh vệ tinh | 3 | 5 | 2 | 3 | 2 | 64 | Sen1Floods11 có nhãn thủ công, ý nghĩa cao; nhiều tiền lệ, nhãn độc lập hữu hạn, GPU và dữ liệu lớn hơn; chưa có pilot |
| Phân tích nâng cấp dependency gây hỏng build | 3 | 4 | 2 | 3 | 2 | 59 | BUMP có build/test outcome; môi trường Docker và khôi phục dependency nặng, tiền lệ sửa lỗi đã sâu. Không chọn |

Các điểm khác 1 mức không làm biến mất cổng bắt buộc. Chọn RCA vì kết hợp **câu hỏi quyết định dữ liệu nào cần xem + nhãn sự cố độc lập + phép đo chi phí + sản phẩm phục vụ quy trình vận hành**. Ưu thế không đến từ lời hứa đạt SOTA hay dùng LLM. Degron đứng thứ hai theo điểm và được giữ dự phòng vì đã có audit, không phải vì đã đầu tư nhiều tài liệu.

### Khảo sát công cụ tin sinh học ở tầng quy trình

1. **Chia dữ liệu:** [DataSAIL, Nature Communications 2025](https://www.nature.com/articles/s41467-025-58606-8) đã giải bài toán tối ưu giảm tương đồng giữa các tập, hỗ trợ một/hai chiều và nhiều loại phân tử. Vì vậy “công cụ tránh rò rỉ có cân bằng lớp” chưa đủ phân biệt. Chưa tìm được trường hợp thiếu chức năng có nhãn chuẩn đủ mạnh để xếp trên RCA trong lượt này; không kết luận lĩnh vực đã hết khoảng trống.
2. **Hợp nhất MAVE:** [Mapping MAVE data, Genome Biology 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12188674/) và [tài liệu MaveDB](https://www.mavedb.org/docs/mavedb/getting-started/index.html) đã bao phủ mapping sang tham chiếu chuẩn, giữ provenance, tải và hiển thị dữ liệu. Khó bán việc nối API/đổi giao diện thành đóng góp khoa học.
3. **Proteomics:** [OpDEA 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11082229/) đã khảo sát 24 bộ spike-in, khuyến nghị và tích hợp quy trình; [SCPDA 2025](https://www.nature.com/articles/s41467-025-65174-4) tiếp tục benchmark cả xử lý thưa, điền thiếu, chuẩn hóa và batch. OpDEA thừa nhận tích hợp tăng nguy cơ false positives: đây là khoảng trống có ý nghĩa, nhưng muốn đóng góp phải kiểm chứng phương pháp kiểm soát lỗi, không chỉ xây dashboard. [Repo OpDEA](https://github.com/PennHui2016/OpDEA), commit `c75f8fbee5427478dd8ca23ed2bdd79639fc31f9`, đã có Shiny và kết quả CSV. Chỉ kiểm tra cấu trúc/code/nguồn, **chưa tải và chạy pipeline proteomics**. [Benchmark targeted proteomics tháng 7/2026](https://pubmed.ncbi.nlm.nih.gov/42492791/) cũng đã đối chiếu chiến lược điền thiếu/tích hợp; bài toán chọn quy trình không còn mới tự thân.

### Nguồn các ứng viên ngoài bio chưa chọn

- [EMBER2024](https://github.com/FutureComputing4AI/EMBER2024) và [C-GUARD 2026](https://www.mdpi.com/1999-5903/18/8/431).
- [BatteryLife](https://github.com/Ruifeng-Tan/BatteryLife), [bài benchmark](https://arxiv.org/abs/2502.18807), [domain adaptation 2025](https://www.sciencedirect.com/science/article/pii/S1364032124007615).
- [Sen1Floods11](https://github.com/cloudtostreet/Sen1Floods11); không suy diễn tất cả patch đều là nhãn thủ công độc lập.
- [BUMP](https://github.com/akago/bump_extension), [bài dữ liệu](https://arxiv.org/abs/2401.09906).
- Legal QA: [quyết định ứng viên đang có](../archive/topics/legal-qa-grounding/topic-decision.md), [ALQAC](https://alqac.github.io/). Chưa audit giấy phép/nội dung toàn bộ corpus; không coi các điểm chưa xác minh là đã qua.

## 3. Đề tài chính giải quyết việc gì?

Khi hệ thống nhiều dịch vụ gặp sự cố, nhiều nơi cùng báo bất thường. Người trực cần biết **dịch vụ nào là điểm gây lỗi và nên xem dữ liệu nào tiếp theo**, trong giới hạn thời gian/truy vấn. Đọc toàn bộ logs và traces tốn xử lý; chỉ chọn nơi bất thường nhất dễ nhầm hậu quả thành nguồn lỗi.

Đầu vào: mốc bắt đầu điều tra và telemetry đã thu thập. Đầu ra: bảng xếp hạng dịch vụ, truy vấn đề nghị tiếp theo, ngân sách đã dùng và quan sát làm thay đổi thứ hạng. Người dùng: kỹ sư vận hành hoặc người phát triển đang điều tra một sự cố. Giá trị dự kiến: đạt chất lượng định vị tương đương với ít dữ liệu phải truy xuất/xử lý hơn, hoặc định vị tốt hơn với cùng ngân sách. **Không tuyên bố giảm thời gian khắc phục thực tế, chi phí lưu trữ telemetry hay tự chứng minh quan hệ nhân quả.** Điều đó cần nghiên cứu người dùng/triển khai riêng.

## 4. Khoảng trống khoa học và đối thủ gần nhất

| Nhóm | Công trình | Phần đã có | Điều còn cần kiểm tra trong đề tài |
|---|---|---|---|
| Thống kê, graph, đa nguồn | [RCAEval và các baseline](https://github.com/phamquiluan/RCAEval) | Bộ đo và phương pháp dùng metrics/logs/traces | Chính sách chọn từng phần dữ liệu, giữ bộ xếp hạng cố định, đường chất lượng–chi phí |
| Agent có giới hạn và kiểm chứng | [VerifyRCA, bản tác giả tháng 6/2026](https://www.researchgate.net/publication/407715364_VerifyRCA_LLM-Guided_but_Evidence-Verified_Root_Cause_Analysis_for_Microservice_Backends) | Chọn truy vấn theo độ bất định và trọng số modality | So trực tiếp heuristic này với giá trị truy vấn học từ thay đổi lỗi xếp hạng; bản đã đọc chưa cung cấp bằng chứng cho chính sách đó |
| Agent kiểm tra mâu thuẫn | [VeriTrail-RCA, bản tác giả tháng 6/2026](https://www.researchgate.net/publication/406279260_VeriTrail-RCA_Evidence-Verified_Root_Cause_Localization_for_Microservice_Backends) | Truy hồi thích ứng, kiểm chứng và budget | Tách lợi ích chọn bằng chứng khỏi chất lượng LLM; không nhận budget/evidence card là ý tưởng mới |
| Sửa quy trình agent | [STAR 2026](https://arxiv.org/abs/2605.15581) | Audit giai đoạn và phân bổ Fast/Slow | Không phải cùng mục tiêu học giá trị một truy vấn telemetry; dùng để phân biệt phạm vi |
| Tách truy hồi–xếp hạng | [DecompRCA 2026](https://arxiv.org/abs/2609.36686) | Đã có phân rã lỗi và pipeline hai giai đoạn | Không lấy “tách hai giai đoạn” làm tính mới; kế thừa chẩn đoán lỗi khi đánh giá |
| Kiểm soát prior và graph | [Buljić 09/2026](https://arxiv.org/html/2609.27069v1) | Audit bias dịch vụ, schema và đối chứng graph; có RE1 và RE2 Sock Shop | Audit RE2 không mới tự thân; thêm prior-only và telemetry-shuffle làm kiểm soát cho lợi ích policy |
| Active feature acquisition | [ICML 2025](https://proceedings.mlr.press/v267/guney25a.html) | Chọn đặc trưng theo giải thích và ngân sách | Chuyển sang hành động dịch vụ × modality × cửa sổ, xử lý dữ liệu thiếu, kiểm tra chuyển hệ thống |

Hai bản ResearchGate là **nội dung do tác giả công bố**, chưa xác minh phản biện hoặc tái lập số liệu. Chúng vẫn đủ để bác bỏ tuyên bố “chưa ai RCA theo ngân sách”; không dùng performance của chúng làm số liệu đã chạy trong repo.

**Đính chính nhận định đang có trong index/nhật ký trước báo cáo này:** đã đọc toàn văn HTML Buljić, mục 3 và 8: có RE2 Sock Shop, không chỉ RE1. Vì vậy không nhận “đo thêm RE2” là khoảng trống mới. Các số 0,488/0,137 là Avg@5 do tác giả báo, không phải Top-1 và chưa tái lập ở đây. Bias nhãn là điều phải kiểm soát, không tự bảo đảm đóng góp dương G2.

**Giả thuyết hẹp:** độ bất định của một ứng viên không cho biết modality nào sẽ sửa thứ hạng. Học mức giảm kỳ vọng của lỗi xếp hạng từ các trạng thái đã quan sát có thể phân bổ truy vấn tốt hơn heuristic bất định/trọng số cố định, đặc biệt khi log/trace thiếu hoặc tín hiệu lỗi lan truyền. Đây là cải tiến ứng dụng của AFA/giá trị thông tin, **không phải cơ chế học mới và chưa có bằng chứng dương**. Khảo sát không chứng minh không tồn tại một công trình khác đã làm giống hệt; độ tin cậy khoảng trống: **vừa**.

Chi tiết thuật toán, baseline, protocol, chỉ số và sản phẩm được khóa trong [quyết định đề tài](../archive/topics/budgeted-microservice-rca/research/topic-decision.md).

## 5. Khả thi dữ liệu đã kiểm chứng

Nguồn [RCAEval trên Hugging Face](https://huggingface.co/datasets/phamquiluan/RCAEval), revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, metadata MIT, truy cập không gated. Repo thuật toán snapshot `259ea4167160256a74ad30004aa3d96a998c846e`. [Script](../archive/topics/budgeted-microservice-rca/code/preprocessing/audit_data.py) và [JSON kết quả](../archive/topics/budgeted-microservice-rca/code/preprocessing/results/data-audit.json) là bằng chứng cục bộ.

| Bộ | Ca | Dịch vụ có nhãn nguyên nhân | Có logs | Có traces |
|---|---:|---:|---:|---:|
| RE1-OB / SS / TT | 125 mỗi hệ | 5 mỗi hệ | 0 / 0 / 0 | 0 / 0 / 0 |
| RE2-OB / SS / TT | 90 mỗi hệ | 5 mỗi hệ | 90 / 90 / 89 | 90 / 0 / 90 |
| RE3-OB / SS / TT | 30 mỗi hệ | 4 / 3 / 2 | 30 / 30 / 30 | 30 / 0 / 30 |
| **Tổng** | **735** | Không cộng như protein độc lập | **359** | **240** |

**360 ca RE2/RE3** là lõi đa nguồn; 375 ca RE1 dùng kiểm tra metrics-only. Không nói 735 ca đều có ba nguồn. Nhãn nguồn lỗi đến từ kịch bản fault injection, độc lập với bộ xếp hạng; telemetry được đo trên hệ thống chạy thật nhưng lỗi được gây có chủ đích. Năm dịch vụ có nhãn mỗi hệ RE2 là hạn chế lớn: tập ứng viên phải gồm tất cả dịch vụ quan sát được, không chỉ năm dịch vụ này.

Đã tải index và sáu ca xác định trước (một ca mỗi hệ trong RE2 và RE3), xác minh kích thước/SHA từ manifest LFS, đọc Parquet và đối chiếu schema/thời điểm injection/đếm dòng với index. Tổng **49.463.299 byte ≈49,46 MB**. Mẫu trace lớn nhất 1.143.435 dòng, DataFrame khoảng 230 MB; metrics lớn nhất mẫu khoảng 4,55 MB. Máy khoảng 7,4 GiB RAM, chưa xác minh GPU. Đây là kiểm tra đọc mẫu, **chưa chứng minh mọi baseline hoặc toàn bộ pipeline chạy vừa RAM**. Upstream khuyến nghị 16 GB; lõi dự kiến xử lý từng ca và tổng hợp từng nhóm, không load toàn bộ. Chưa tải toàn bộ 735 ca, chưa huấn luyện, chưa chấm accuracy.

[OpenRCA](https://github.com/microsoft/OpenRCA) có thể làm kiểm tra bên ngoài nhưng khoảng 68,5 GB dữ liệu và khuyến nghị RAM cao hơn; **không nằm trên đường bắt buộc hoàn thành**. Không để đề tài phụ thuộc một bộ chưa tải được.

## 6. Vì sao chọn và mức đáp ứng GVHD

| Tiêu chí | Đóng góp dự kiến | Nhận định hiện tại |
|---|---|---|
| Mới của hướng | Giá trị giảm lỗi xếp hạng thay cho độ bất định để chọn nhóm telemetry | Vừa; RCA/budget/AFA đều đã có |
| Cải tiến phương pháp | Bộ dự đoán lợi ích truy vấn, chia chi phí và quyết định dừng; đối chứng cùng ranker | Trọng tâm, chưa chứng minh |
| Phương pháp mới | Kế thừa AFA gần đây, dùng học có giám sát nhẹ và mask trạng thái | Có căn cứ; không ép LLM cho đủ tiêu chí |
| XAI | Nhật ký quan sát, ablation bằng chứng, phân biệt lý do chọn truy vấn với lý do xếp hạng | Có kiểm chứng dự kiến; hiển thị log đơn thuần chưa đủ XAI |
| Ứng dụng | Workspace điều tra sự cố: nhập case, đặt budget, xem rank/bằng chứng và truy vấn tiếp theo | Tự nhiên thuộc quy trình; chưa xây app |

RCA thắng theo đánh giá tổng hợp hôm nay, **không thắng mọi tiêu chí**. Ít khớp chuyên môn GVHD hơn proteomics/degron; có ba miền hệ thống nên bằng chứng chuyển miền hạn chế; lợi ích học chính sách chưa biết. Đổi lĩnh vực giúp có endpoint và sản phẩm rõ, không làm mất rủi ro nghiên cứu. G1 đã qua ở mức truy cập/nhãn; G3 qua ở mức thiết kế; **G2 chưa qua ở mức kết quả**. Không thể bảo đảm kết quả dương bằng một cuộc khảo sát.

## 7. Quyết định hành động

Khóa tên, câu hỏi, dữ liệu lõi và app như [topic-decision.md](../archive/topics/budgeted-microservice-rca/research/topic-decision.md). Bước kế tiếp là đề cương và tái lập baseline/thiết lập broker, không tiếp tục tìm đề tài thứ mười một. Nếu đóng góp thực nghiệm không xuất hiện, báo trung thực và xử lý bằng điều kiện đã ghi; không đổi chỉ số/tập test để tạo kết quả đẹp.

Degron là dự phòng có kiểm chứng nguồn dữ liệu và khả năng chia theo protein. Các quyết định DARKIN 10/10 và degron 11/10 được giữ làm lịch sử; lựa chọn 12/10 này thay thế chúng ở cấp **đề tài chính**. Các hub/slide cũ mô tả ứng viên cũ, không phải thuyết minh của RCA.

## 8. Kiểm tra artifact ngày 12/10

- Script audit đã chạy thành công, đọc sáu ca và đối chiếu index; kiểm tra biên dịch Python đạt.
- JSON nhất quán tổng 735, đa nguồn 360, logs 359, traces 240 và sáu mẫu; 22 tệp cache khớp kích thước/SHA trong manifest. Raw cache được Git bỏ qua.
- 37 lượt liên kết cục bộ mới/thay đổi hợp lệ; phát hiện 16 lượt liên kết hỏng đã có trước trong tài liệu lịch sử (chi tiêu và đường dẫn cũ của quyết định DARKIN), chưa sửa vì ngoài phạm vi lựa chọn này. Không báo toàn bộ repo đã qua link check.
- Điểm bảng khớp trọng số; whitespace tài liệu mới và `git diff --check` cho các file liên quan đạt. Giữ thay đổi có sẵn và tài liệu ứng viên; không commit.
- Chưa tái lập baseline, đánh giá mô hình, thử RAM pipeline đầy đủ, xây app hoặc thử với người dùng. Không dùng kiểm tra artifact thay cho chứng cứ nghiên cứu dương.
