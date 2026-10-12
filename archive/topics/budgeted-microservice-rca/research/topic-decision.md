# Quyết định đề tài: lựa chọn bằng chứng cho RCA theo ngân sách

> **Lịch sử quyết định:** các câu "chốt / quyết định / khuyến nghị" trong file này phản ánh thời điểm viết, có thể đã bị thay. Trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

**Chọn chính ngày 12/10/2026 theo yêu cầu sinh viên mở lĩnh vực và chốt trong ngày. Chưa phê duyệt GVHD.**

**Tên:** Định vị nguyên nhân sự cố microservice bằng lựa chọn bằng chứng thích ứng theo giá trị chẩn đoán và ngân sách truy vấn.

**Slug:** `budgeted-microservice-rca`. [Báo cáo lựa chọn](../../../surveys/open-field-topic-selection-2026-10-12.md) ghi đối chiếu ứng viên và tiền lệ; [README audit](../code/preprocessing/README.md) ghi cách tái lập dữ liệu. Đây là đề tài cải tiến thuật toán phục vụ một công cụ điều tra sự cố, chưa phải kết quả hoàn thành.

## 1. Vấn đề và người dùng

Một dịch vụ hỏng có thể làm nhiều dịch vụ phía sau cùng bất thường. Người trực cần phân biệt nguồn lỗi với hậu quả và quyết định xem metrics, log hoặc trace nào tiếp theo. Công cụ nhận telemetry và mốc điều tra; đề nghị dịch vụ nghi ngờ, quan sát cần truy xuất tiếp và giới hạn xử lý.

Ví dụ **minh họa**, không phải kết quả đo: hai dịch vụ cùng tăng latency; ngân sách còn đủ xem một nhóm trace. Công cụ ưu tiên trace của nơi dự kiến giúp phân biệt hai ứng viên, thay vì chọn nơi có điểm bất thường cao nhất. Khi không đủ bằng chứng, hiển thị thứ hạng/giới hạn và đề nghị truy vấn, không tự khắc phục sự cố.

Giá trị cần chứng minh: ít truy xuất/xử lý dữ liệu hơn với chất lượng định vị gần tương đương, hoặc chính xác hơn trong cùng budget. Không đồng nhất lợi ích offline này với giảm MTTR, phí lưu trữ hoặc quan hệ nhân quả thật.

## 2. Câu hỏi nghiên cứu và phương pháp

**RQ1, chính:** Khi giữ cùng bộ xếp hạng dịch vụ, chính sách học giá trị của truy vấn có cải thiện đường chất lượng–ngân sách so với ngẫu nhiên, thứ tự cố định, độ bất thường và heuristic độ bất định không?

**RQ2:** Lợi ích còn giữ khi nguồn telemetry thiếu và hệ thống/dịch vụ gây lỗi chưa xuất hiện trong huấn luyện không? Báo riêng hai kiểu chuyển, không gộp thành một tuyên bố khái quát hóa.

**RQ3, giải thích:** Dữ liệu được truy xuất có làm thay đổi thứ hạng đúng như lời giải thích của chính sách không; phần tăng hiệu quả đến từ chọn nhóm hay dừng sớm?

Mỗi hành động `a = (service, modality, time_window)` mở một nhóm dữ liệu chưa xem. Trạng thái `h` chứa **chỉ** quan sát đã mở, mask nhóm chưa mở/không tồn tại, thứ hạng hiện tại và budget còn lại. Bộ ranker nhẹ dùng đặc trưng bất thường đã tổng hợp của các nguồn được mở; dùng các mô tả dịch vụ dùng chung, không học nhãn từ ID dịch vụ. Ranker được huấn luyện trên các mask nguồn để hoạt động khi dữ liệu chưa đầy đủ.

Tạo dữ liệu học giá trị truy vấn trên ca **train**: từ trạng thái che nguồn, lần lượt mở một nhóm, tính thay đổi loss xếp hạng của nguyên nhân thật. Ranker tạo nhãn lợi ích bằng dự đoán out-of-fold theo nhóm ca, giảm nguy cơ fit quá lạc quan. Huấn luyện một mô hình nhỏ dự đoán lợi ích này từ trạng thái trước truy vấn và mô tả hành động. Tất cả trạng thái cùng một ca thuộc cùng fold; hàng rollout không phải sự cố độc lập.

Mục tiêu thiết kế:

```text
g(h,a) = E[ loss(rank(h), y) - loss(rank(h + reveal(a)), y) | h,a ]
utility(h,a) = predicted_g(h,a) / expected_cost(a)
```

Chọn hành động có utility cao nhất trong budget. Loss huấn luyện sơ bộ dùng `1 - reciprocal_rank(y)`; tham số và lựa chọn loss khóa trên validation. Chi phí kỳ vọng lấy từ metadata được phép biết hoặc thống kê train, không nhìn dữ liệu chưa truy xuất để chọn. Trừ chi phí thực tế trước khi đưa kết quả truy vấn vào trạng thái. Tách cost theo số truy vấn và byte/record trả về; nếu dùng trọng số tổng hợp thì công bố và kiểm tra độ nhạy.

**Chính sách dừng là ablation**, không phải nơi giấu độ chính xác: thí nghiệm chính dùng budget cố định, báo cả khi chưa tin cậy. Bản dừng sớm chỉ dùng ngưỡng đã chọn trên validation. Không dùng nhãn thật để dừng khi test. Không bắt buộc GPU, PLM hoặc API LLM; cấu hình đầu tiên là ranker/chính sách cây boosting hoặc tuyến tính tùy baseline validation.

## 3. Khoảng trống và tuyên bố cho phép

RCA, nhiều nguồn, truy vấn thích ứng và budget đã có. [VerifyRCA](https://www.researchgate.net/publication/407715364_VerifyRCA_LLM-Guided_but_Evidence-Verified_Root_Cause_Analysis_for_Microservice_Backends), bản tác giả tháng 6/2026, có controller ưu tiên độ bất định kết hợp trọng số nguồn. [AFA tại ICML 2025](https://proceedings.mlr.press/v267/guney25a.html) đã chọn đặc trưng dựa trên giải thích. Không nhận các ý tưởng đó là mới.

Phần đề xuất là **học lợi ích giảm lỗi xếp hạng cho truy vấn nhóm telemetry, rồi đánh giá chuyển hệ thống/thiếu nguồn với cùng ranker và cùng accounting**. Cần đối chiếu cả heuristic gần nhất lẫn AFA thích nghi sang nhóm. Độ bất định cao có thể tồn tại ở ứng viên mà một modality không mang thêm thông tin; giả thuyết là nhãn lợi ích trực tiếp giúp phân biệt tình huống này. Chưa xác nhận giả thuyết.

Tuyên bố dự kiến nếu thí nghiệm đạt: “cải thiện phân bổ truy vấn trong thiết lập RCAEval được mô tả”. Không nói “đầu tiên”, “SOTA”, “chứng minh nguyên nhân”, “giảm chi phí vận hành thực tế”. Audit bằng chứng là khả năng truy nguyên; độ trung thực với mô hình cần ablation riêng, không suy ra từ giao diện.

## 4. Dữ liệu và tách thông tin đánh giá

Lõi: [RCAEval](https://huggingface.co/datasets/phamquiluan/RCAEval), revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`. Index 735 ca, 360 ca RE2/RE3 đa nguồn, 359 có logs, 240 có traces. Đã đọc sáu ca; xem [kết quả JSON](../code/preprocessing/results/data-audit.json). Lỗi được injection vào hệ thống thực nghiệm; chỉ ba hệ thống, RE2 chỉ năm dịch vụ có nhãn mỗi hệ. Không coi 735 ca như 735 hệ thống độc lập.

- `root_service`, fault label, case ID/tên file và `root_cause.txt` nằm trong vùng **evaluation-only**. Case ID mã hóa đáp án, phải đổi sang ID mù trước broker; không đưa vào feature/prompt.
- Nhãn injection được dùng để huấn luyện trên train và chấm test, không lẫn vào ranker/policy lúc inference. Mốc injection dùng làm incident anchor chung trong benchmark, **không suy ra thời gian phát hiện thực tế**; kiểm tra thêm anchor trễ định trước.
- Số liệu và nội dung fault window chưa mở không được dùng để xây topology, chọn truy vấn hoặc tính đặc trưng trước budget. Topology nếu dùng phải từ cấu hình hoặc normal window có nguồn gốc/cost khai báo; có cấu hình không topology.
- Dataset không có trace/log là nhóm không khả dụng; khác với nhóm chưa truy vấn. Không điền cùng một số và giả định đã đo.
- Giữ tất cả dịch vụ quan sát được trong tập ứng viên, không lọc bằng danh sách dịch vụ có nhãn nguyên nhân.

Chia chính theo **nhóm kịch bản** `(system, root_service, fault_type)` giữ mọi replica trong một nhóm. Khóa train/validation/test bằng manifest trước tuning; trước khi gọi “replica” cần kiểm tra metadata/time range, near-duplicate và quan hệ kịch bản. Nếu còn ca gần trùng, gom nhóm và báo số lượng sau gom. Không chia các cửa sổ hoặc hàng log thành train/test độc lập.

Chuyển hệ thống: leave-one-system-out; hyperparameter chọn chỉ từ hai hệ train bằng grouped inner-validation. Dịch vụ chưa thấy: giữ toàn bộ ca của dịch vụ bị holdout ngoài train; tính khả thi mỗi fold phải kiểm lại nhãn/fault balance. Chỉ có ba hệ, nên báo từng hệ và không dùng CI theo ca để tuyên bố độ tin cậy toàn ngành. RE1 bổ trợ metrics-only; không trộn ngầm với RE2/RE3 để tăng mẫu. OpenRCA là mở rộng, không bắt buộc.

## 5. Đối chứng và phép đo đã định trước

| Đối chứng | Mục đích |
|---|---|
| All available telemetry, cùng ranker | Tham chiếu full-data; **không** gọi là oracle hoặc trần tối ưu |
| Metrics-only; BARO official pinned | Mốc đơn giản và khả năng tái lập; chuẩn hóa hướng metric/service rõ ràng |
| Prior-only theo tần suất dịch vụ trên train; telemetry bị hoán đổi giữa ca | Kiểm tra nhớ vị trí injection và lợi ích có thực sự phụ thuộc bằng chứng; ties ngẫu nhiên với seed, không dùng nhãn test |
| Fixed modality order và random nhóm dưới cùng cost | Lợi ích chọn thích ứng so với tiết kiệm thuần túy |
| Chọn nhóm theo độ bất thường đã quan sát | Kiểm tra policy chỉ đang theo tín hiệu lớn |
| Heuristic bất định × trọng số modality của VerifyRCA | Đối thủ trực tiếp cho nguyên tắc phân bổ; bản thích nghi cùng ranker, **không** gọi là tái lập toàn VerifyRCA |
| Một phương pháp AFA gần đây thích nghi theo nhóm | Kiểm tra học giá trị có hơn chọn nhóm theo importance/explainability; ghi đầy đủ thay đổi |
| Learned gain không chia cost; learned gain không dừng sớm | Ablation phần đóng góp |

Phương pháp đa nguồn mạnh trong RCAEval (ví dụ TORAI/EventADL) là đối chiếu bổ sung nếu cài và tái lập được; không báo đã chạy. Lợi ích RQ1 phải so cùng ranker; đối chiếu end-to-end với published methods báo riêng để tránh gán công lao ranker cho policy. Nếu chưa chạy được baseline gần nhất, thu hẹp tuyên bố; không thay nó bằng đối thủ yếu.

[Buljić 09/2026](https://arxiv.org/html/2609.27069v1) đã audit prior và có phân tích RE2 Sock Shop; không lấy “mở rộng sang RE2” làm điểm mới. Prior-only dùng train và tập ứng viên đầy đủ; dịch vụ chưa thấy có cùng prior không thông tin, phải báo tie convention. Báo riêng policy/score dùng và không dùng prior; không tính lợi ích telemetry bằng so với uniform random duy nhất. Avg@5 của bài đó khác Top-1 chính của đề tài, không đối chiếu trực tiếp hai con số.

Chính: Top-1 theo dịch vụ và diện tích dưới đường Top-1–budget ở grid khóa trước; phụ: MRR, Top-3, bytes/records/truy vấn và thời gian xử lý đo trên cùng máy. Grid dự kiến 10/25/50/75/100% cost đầy đủ, khóa chính thức sau audit cost trên train. Starter package (nếu có) cũng bị tính cost; không cấp mọi metrics miễn phí rồi nhận tiết kiệm toàn bộ telemetry. Với budget quá nhỏ cho package, báo không thực hiện được và điều chỉnh grid trước test.

**Mục tiêu thực tiễn dự kiến:** giảm ít nhất 30% bytes được trả về ở mức Top-1 giảm không quá 3 điểm phần trăm so với full-data cùng ranker, đồng thời tốt hơn baseline budget mạnh nhất. Đây là ngưỡng do đề tài chọn, chưa đạt; báo chất lượng tuyệt đối để tránh “giữ nguyên một ranker rất kém”. Dùng paired differences, CI theo nhóm kịch bản, báo từng fault/hệ; không lấy cửa sổ làm đơn vị bootstrap. Nếu CI quá rộng thì kết luận chưa đủ chứng cứ, không nhận non-inferiority chỉ vì kiểm định không có ý nghĩa.

Chi phí tạo/cache feature và huấn luyện báo riêng. Nếu replay dùng summary tính trước toàn bộ, đó là mô phỏng cost truy xuất dữ liệu; chưa là lợi ích compute thực. App cần một đường thực thi chỉ đọc phần được chọn để kiểm tra chi phí xử lý. Quan sát truy vấn ngẫu nhiên/cùng budget là đối chứng cho explanation ablation; không cần nhãn “evidence ground truth” tự tạo.

## 6. Sản phẩm tối thiểu và đóng góp

Ứng dụng điều tra sự cố gồm: nạp case với schema chuẩn; nhập mốc điều tra/budget; xếp hạng ứng viên; xem nguồn dữ liệu đã mở; chấp nhận truy vấn tiếp theo; so sánh chính sách; xuất báo cáo và nhật ký. Hai chế độ: replay có đáp án ẩn để benchmark và phân tích case không có đáp án. Khi replay kết thúc mới mở đáp án; không đưa tên file có nguyên nhân vào màn hình trước đó. Đề nghị truy vấn thủ công dùng cùng broker/accounting.

Ba sản phẩm nghiên cứu dự kiến:

1. Chính sách học giá trị truy vấn và thí nghiệm giải thích phần lợi ích.
2. Broker/API tách dữ liệu chưa mở, manifest chống rò rỉ và protocol quality–budget tái lập.
3. Workspace dùng chính broker, cho phép điều tra và truy nguyên kết quả.

Broker/protocol là đóng góp kỹ thuật; chỉ được gọi đóng góp khoa học khi đánh giá tạo hiểu biết hoặc lợi ích có chứng cứ. App là trung tâm của thao tác chọn bằng chứng, không chỉ form nhập và hiển thị một score.

## 7. Lộ trình thực hiện dự kiến 8 tuần

| Tuần | Kết quả phải có |
|---|---|
| 1 | Audit toàn bộ RE2/RE3, nhóm kịch bản/near-duplicate, split khóa, baseline BARO tái lập, kiểm tra RAM |
| 2 | Feature/broker không nhìn nguồn chưa mở, ranker cùng mask và baseline full/metrics-only |
| 3 | Heuristic budget mạnh, đường chất lượng–cost; phát hiện ceiling/missingness trước xây policy |
| 4 | Rollout train bằng cross-fitting, policy học lợi ích, ablation và kiểm tra inference không dùng nhãn |
| 5 | Grouped test, leave-system/root-service-out, thiếu nguồn, thống kê theo nhóm |
| 6 | App replay và case chưa có nhãn, thực thi đọc dữ liệu theo query, export provenance |
| 7 | Kiểm thử schema/cost/broker, explanation ablation, sửa các lỗi được phát hiện |
| 8 | Báo cáo, đóng gói tái lập, demo và ghi đầy đủ giới hạn |

Đây là kế hoạch phạm vi, không cập nhật lịch học kỳ theo mốc cũ. Không dựng Kubernetes hoặc tạo lỗi mới trên đường bắt buộc. Không tự sửa hệ thống, triển khai production hoặc gọi LLM trả phí trong MVP.

## 8. Điều kiện làm thay đổi lựa chọn

Không thể bảo đảm G2 dương trước thí nghiệm. Đặt checkpoint tuần 3–4: nếu fixed/random/VerifyRCA-style đã gần full-data ở mọi budget, hoặc learned gain không cải thiện so baseline mạnh trong validation sau sửa lỗi có căn cứ, không mở rộng kiến trúc/đổi test để cứu đề tài. Đánh giá một lần thu hẹp đã định trước vào loại lỗi đa nguồn khó (báo rõ exploratory, sau đó cần test độc lập); nếu không còn phần cải tiến đủ mạnh thì kích hoạt **degron dự phòng** theo audit 12/10. Nếu GVHD không chấp nhận hướng ngoài bio, dùng đúng dự phòng này, không tái mở toàn bộ danh sách.

Hiện tại **đã chốt lựa chọn chính**, không chờ “tìm thêm đề tài tốt hơn”. Chưa có baseline accuracy, tiết kiệm, app hoàn chỉnh hoặc xác nhận chấp thuận học thuật. Rủi ro chính: số miền nhỏ, bias vị trí injection, chuyển hệ thống của policy và tiền lệ AFA/RCA gần. Mọi công bố lợi ích phải ghi thiết lập giới hạn đó.
