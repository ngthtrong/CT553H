# Kế hoạch tìm bằng chứng wet lab và hiệu quả nguồn lực — 07/11/2026

**[ĐÃ TRA CỨU VÀ BÁO KẾT QUẢ]** ARS-Codex `deep-research`, chế độ `full`, ngày
07/11/2026. [Báo cáo kết quả](findings.md) và [biên bản kiểm](validation.md) tách
tiền lệ wet lab khỏi hiệu quả thời gian/chi phí và kết quả CT553H. Có tám nghiên
cứu trong [ma trận](evidence-matrix.csv): năm gần degron, ba lân cận; 39 query
web được ghi trong [nhật ký](search-log.csv). Đây là tra cứu có giới hạn, chưa
chứng nhận bao phủ toàn lĩnh vực hoặc systematic review. Không chạy mô hình
hoặc làm thí nghiệm CT553H mới.

**Cập nhật chuyển bước ngày 07/11/2026:** người dùng yêu cầu “bắt đầu tiến hành
nghiên cứu theo kế hoạch đã lập”. Yêu cầu này xác nhận RQ và blueprint bên dưới;
không hỏi lại việc có thực hiện kế hoạch hay không. Checkpoint `review-form-note`
của ARS được mở sau xác nhận này. Sau khi note được trình bày, người dùng trả
lời nguyên văn “bắt đầu tra cứu”; theo quy tắc “a reply that keeps the current
work”, ghi nhận `skip`, đóng checkpoint và tiếp tục chế độ `full` hiện tại.
Không hỏi lại note hoặc tự gán một hình thức review. Tra cứu web đã hoàn tất
trong phạm vi lượt này; nguồn, mẫu số và access gaps được lưu ở các file trên.

Skill áp dụng: [academic-research-suite](../../.agents/skills/academic-research-suite/SKILL.md),
[workflow deep-research](../../.agents/skills/academic-research-suite/ars/deep-research/WORKFLOW.md).
Đọc các hợp đồng `research_question_agent`, `research_architect_agent` và
`devils_advocate_agent` cho giai đoạn lập kế hoạch; không kích hoạt pipeline viết
bài, screening hai reviewer hoặc dịch vụ xác minh tài liệu qua API.

## 1. Mục tiêu và câu hỏi nghiên cứu dự kiến

**RQ dự kiến:** Các nghiên cứu gốc về dự đoán degron cung cấp mức bằng chứng nào
cho giá trị ưu tiên ứng viên thực nghiệm có thể tham chiếu cho CT553H?

Ba câu hỏi phụ cùng kế thừa phạm vi ở mục 2:

1. **Wet lab:** Những dự đoán nào đã được kiểm chứng bằng phép đo thực nghiệm,
   trên đơn vị peptide, mutation hay protein tự nhiên, với đối chứng nào?
2. **Nguồn lực:** Có phép so định lượng nào cho số thí nghiệm, tỷ lệ tìm đúng,
   thời gian hoặc chi phí khi chọn ứng viên bằng mô hình?
3. **Áp dụng:** Khác biệt về endpoint, assay, cách chọn ứng viên và dữ liệu cho
   phép chuyển kết luận tới CT553H đến mức nào?

Đây là cách cụ thể hóa yêu cầu của người dùng; **RQ và blueprint đã được xác nhận
qua yêu cầu thực hiện kế hoạch, không phải protocol đã tiền đăng ký**. Nếu không tìm được bằng chứng hỗ trợ,
kết quả vẫn phải báo rõ giới hạn của phạm vi đã tìm.

| FINER | Đánh giá ở bước thiết kế |
| --- | --- |
| Khả thi | Có thể đọc nguồn công bố và tài liệu bổ sung; quyền truy cập toàn văn cần kiểm từng bài. |
| Đáng quan tâm | Trả lời trực tiếp câu hỏi mô hình giúp quyết định thực nghiệm như thế nào. |
| Tính mới | Chưa đánh giá; mục tiêu lượt nghiên cứu là xác minh bằng chứng, không tuyên bố ý tưởng đầu tiên. |
| Đạo đức | Phân tích tài liệu thứ cấp; không tuyển người tham gia, không gửi dữ liệu riêng của repo ra dịch vụ mô hình. |
| Liên quan | Giúp giới hạn claim ứng dụng và xác định phần cần kiểm chứng tiếp của đề tài. |

## 2. Phạm vi và đơn vị bằng chứng

- **Lĩnh vực:** degron, hiệu ứng mutation và protein abundance/degradation.
- **Thời gian:** từ khi có tài liệu được lập chỉ mục đến ngày thực sự chạy tìm
  kiếm; ở lượt tiếp phải ghi ngày tìm chính xác, không dùng ngày lập kế hoạch
  làm ngày đã tra cứu.
- **Địa lý:** không giới hạn; ghi ngôn ngữ và giới hạn truy cập. Ưu tiên đọc toàn
  văn tiếng Anh và các nguồn có thể kiểm chính xác; không suy rằng đã bao phủ mọi
  ngôn ngữ.
- **Đối tượng:** phương pháp dự đoán degron hoặc mutation ảnh hưởng abundance/
  stability có thực nghiệm follow-up hoặc phép so hiệu quả nguồn lực liên quan.
- **Đơn vị phân tích:** một nghiên cứu và một phép so có định nghĩa; DOI, phiên
  bản bài và supplement đi cùng. Không đếm cùng một study nhiều lần từ preprint,
  bài chính thức, website và review.

Độ gần CT553H được ghi riêng: (a) mutation-effect/peptide-reporter; (b) degron
đầu/cuối hoặc protein tự nhiên; (c) abundance/stability ở bài toán lân cận. Nhóm
(c) chỉ dùng làm tiền lệ có giới hạn, không cộng vào kết quả trực tiếp của (a).

Loại khỏi bằng chứng xác nhận: quảng cáo sản phẩm, lời hứa tiết kiệm không có số
liệu, benchmark chỉ có AUROC/MAE, simulation chưa làm wet lab, annotation đơn
thuần. Vẫn có thể giữ chúng trong sổ nguồn với đúng loại bằng chứng và lý do.
Không mở rộng sang tiết kiệm chi phí phát triển thuốc nói chung hoặc chẩn đoán
lâm sàng để thay cho bằng chứng ở bài toán degron.

## 3. Bản thiết kế phương pháp

**Cách tiếp cận:** thực dụng, dựa trên quan sát có thể kiểm; phân tích tài liệu
thứ cấp kết hợp trích số định lượng khi có. Mục tiêu là trả lời claim nào được
hỗ trợ, không chứng minh trước rằng mô hình nhất định có ích.

**Phương pháp:** tra cứu có nhật ký, đọc nguồn gốc và supplement, trích bằng
chứng theo phép so, tổng hợp tường thuật theo endpoint và thiết kế. Không gộp
hiệu ứng thành meta-analysis khi assay, đơn vị hoặc đối chứng khác nhau.

**Nguồn dữ liệu dự kiến:** PubMed/PMC, trang publisher, DOI/metadata chính thức,
preprint server và repository tác giả để kiểm bổ sung. Công cụ tìm kiếm học
thuật/web dùng để phát hiện nguồn; claim kết quả phải quay về nghiên cứu gốc.
Không xem một kết quả tìm kiếm hoặc metadata là đã đọc toàn văn.

**Tiêu chuẩn tin cậy:** ghi đúng phiên bản; có locator cho từng claim; giữ kết
quả thất bại và denominator; phân biệt mẫu độc lập với technical replicate;
ghi nguồn tài trợ/xung đột lợi ích nếu bài công bố; đánh giá đúng thiết kế
thí nghiệm sinh học thay vì áp máy móc thang đánh giá thử nghiệm lâm sàng.

## 4. Chiến lược tìm kiếm được duyệt

Các chuỗi sau là **bản kế hoạch**; query thực tế được điều chỉnh và lưu nguyên
ở [search-log.csv](search-log.csv), cùng ngày, tham số và các trang được trả về
theo batch. Không gọi query kế hoạch là truy vấn đã chạy nguyên xi.

```text
Q1: (degron OR "degron mutation" OR "degron disruption")
    AND (prediction OR "machine learning" OR "deep learning")
    AND ("experimental validation" OR "functional validation" OR reporter)

Q2: (degron OR "protein degradation" OR "protein abundance")
    AND ("variant prioritization" OR "mutation prioritization" OR "candidate selection")
    AND (validation OR experimental)

Q3: (degron OR "protein stability prediction" OR "variant effect prediction")
    AND ("cost per hit" OR "experimental budget" OR "experiments saved"
         OR "time saving" OR "cost saving" OR "sample efficiency")

Q4: (degron OR "degron prediction")
    AND ("prospective validation" OR "negative results" OR "failed validation"
         OR "selection bias" OR "publication bias")
```

- Đi từ bài hạt giống và tài liệu trích dẫn hai chiều; tìm cả tên phương pháp,
  tên tác giả, assay và các từ chi phí/thời gian trong toàn văn/supplement.
- Tìm cả bằng chứng bất lợi: dự đoán không xác nhận được, chỉ chọn case thuận
  lợi, thay đổi cellular context, hoặc chi phí tính toán/lab lấn át lợi ích.
- Trùng DOI/phiên bản được hợp theo study, giữ lịch sử phiên bản. Bài bị giới hạn
  truy cập được ghi `access_limited`; không thay nội dung chưa đọc bằng kết luận
  từ abstract hoặc bài review. Có thông báo correction/retraction thì kiểm nguồn
  publisher và ghi nhận, không suy từ việc không thấy thông báo rằng bài sạch.
- Dừng khi đã duyệt các nhóm query và nhánh trích dẫn đã định, đồng thời một
  vòng mở rộng cuối không thêm study đủ điều kiện hoặc loại bằng chứng mới.
  Nếu giới hạn công cụ/truy cập khiến phải dừng sớm, công bố phần chưa bao phủ;
  không gọi đó là đã bão hòa tài liệu toàn lĩnh vực.

### Đầu mối ban đầu ở bước lập kế hoạch

| Đầu mối | Mục cần đọc lại | Vai trò dự kiến |
| --- | --- | --- |
| Zhang 2023, DOI `10.1016/j.molcel.2023.08.022` | Assay, saturation/scanning và validation trong bài/supplement. | Kiểm endpoint và bối cảnh gần dữ liệu CT553H. |
| Voutsinos/PAP 2026, DOI `10.1126/sciadv.adz3483` | Mutation follow-up, context và cách chọn case. | Kiểm tiền lệ mutation-aware prediction. |
| Tokheim/deepDegron 2021, DOI `10.1016/j.molcel.2021.01.020` | Dự đoán trước thí nghiệm, mọi case thành công/thất bại và đối chứng. | Đầu mối tiền lệ ưu tiên ứng viên. |
| DEGRONOPEDIA 2024, DOI `10.1093/nar/gkae238` | Case validation, construct, assay và denominator. | Đầu mối công cụ dẫn tới thực nghiệm. |

Ba nguồn đầu mối đã có trong [audit tài liệu ngày 06/11](../progress-review-2026-11-06/literature-audit.md)
là Zhang, Voutsinos và DEGRONOPEDIA. deepDegron là đầu mối từ lượt trao đổi trước,
cần xác minh lại metadata và đoạn nguồn trước khi dùng. Bảng này **không tái
xác nhận số liệu tác giả hoặc mức tiết kiệm**. Không đặt trước số bài phải có
để đạt một kết luận thuận lợi.

## 5. Biểu mẫu trích bằng chứng và quy tắc kết luận

Mỗi dòng dữ liệu tương lai cần các trường:

| Nhóm | Trường bắt buộc |
| --- | --- |
| Nguồn | Study ID, DOI/URL, phiên bản, ngày đọc, phần đã đọc, vị trí bảng/hình/section/supplement và đoạn ngắn hỗ trợ claim. |
| Bài toán | Model, prediction unit, training/test exposure, nhãn, assay, construct, cell context và endpoint. |
| Lựa chọn | Candidate pool, cách chọn, có khóa lựa chọn trước thí nghiệm hay không, tiêu chí xác nhận, baseline chọn ứng viên và số case không báo kết quả nếu xác định được. |
| Kết quả | Số đã thử, số xác nhận, số thất bại, đơn vị độc lập/replicate, effect size, CI tác giả báo và mẫu số cho từng tỷ lệ. Thiếu ghi `not_reported`. |
| Nguồn lực | Chi phí cố định/biến đổi, vật tư, công lao động, tính toán, lặp thất bại; tiền tệ/năm giá; elapsed time so với person-hours; cách đo hoặc giả định ước lượng. |
| Đối chứng | Random/heuristic/không mô hình, cùng ngân sách, cùng candidate pool và endpoint; prospective hay retrospective; có phân bổ hoặc làm mù nếu tác giả báo. |
| Áp dụng | Độ gần CT553H, khác assay/source/context, giới hạn đã đọc, kết luận được phép và điều chưa chứng minh. |

Phân loại theo **hai trục riêng**, tránh biến một ca wet lab thành chứng cứ kinh tế:

| Trục | Các trạng thái và giới hạn |
| --- | --- |
| Sinh học | Chỉ prediction; đo lại assay trên case đã chọn; validation prospective có đối chứng; kiểm protein tự nhiên/cơ chế. Mỗi trạng thái giữ đúng endpoint, không phải thang đồng nhất. |
| Nguồn lực | Không báo; claim định tính; ước lượng theo giả định; phép đo thực tế có đối chứng. Số hit không tự biến thành giờ/tiền tiết kiệm. |
| Liên hệ dự án | Kết quả trực tiếp CT553H; tiền lệ bên ngoài gần bài toán; tiền lệ lân cận. Hai loại sau không được đổi nhãn thành validation CT553H. |

Quy tắc tổng hợp:

1. Có model-guided follow-up nhưng không baseline chọn ứng viên: có tiền lệ
   xác nhận sinh học; chưa chứng minh tăng hit rate nhờ model.
2. Có hit rate so đối chứng: báo effect và độ bất định đúng nguồn; chưa kết luận
   tiết kiệm tiền/thời gian nếu thiếu phép đo tương ứng.
3. Có chi phí/thời gian định lượng: tách đo thực tế với mô hình hóa, chi phí biên
   với tổng chi phí; chỉ báo phần so sánh tương thích. Không tự chuyển tỷ lệ hit
   thành số tiền hoặc quy đổi tiền tệ/năm giá khi chưa chốt giả định.
4. Nếu không tìm được: viết “chưa tìm thấy trong các nguồn và phạm vi đã duyệt”,
   liệt kê access gaps; không kết luận bằng chứng không tồn tại.
5. Kết quả nguồn ngoài chỉ cho phép nói “có tiền lệ”; claim CT553H tiết kiệm
   nguồn lực cần đánh giá trực tiếp riêng. Inference latency không thay tổng
   thời gian hoặc chi phí quy trình wet lab.

## 6. Trình tự thực hiện và sản phẩm của lượt nghiên cứu tiếp

| Bước | Công việc | Sản phẩm và điều kiện hoàn thành |
| --- | --- | --- |
| 1 — hoàn tất | Chốt RQ, phạm vi và blueprint. | Kế hoạch được duyệt; review-form note đã đóng với `skip` theo câu trả lời “bắt đầu tra cứu”. |
| 2 — hoàn tất có giới hạn | Tra cứu và kiểm metadata/phiên bản. | search-log.csv/search-receipts.json: 39 query, 95 thao tác; không phải census mọi database hit. |
| 3 — hoàn tất trong phạm vi đọc | Đọc phần nguồn gốc, trích phép so; ghi supplement thiếu. | results.json/evidence-matrix.csv: tám study; bốn candidate gap/loại trừ riêng. |
| 4 — hoàn tất | Tổng hợp sinh học/nguồn lực và phản chứng. | findings.md §§2–4; các sửa claim và giới hạn ở validation.md. |
| 5 — hoàn tất | Báo cáo tiếng Việt và claim áp dụng. | findings.md; thiếu validation trực tiếp CT553H và economic comparator được giữ rõ. |

Các đầu ra `search-log.csv`, `evidence-matrix.csv` và `findings.md` đã được tạo
sau khi thực hiện các bước tương ứng; `results.json` giữ số/nguồn máy đọc được.
Không đặt quota số bài hoặc coi file trống là bước hoàn thành.

Nếu đọc PDF local và dùng số trang làm locator, chạy structural preflight của
skill trước khi tin page anchor; thiếu dependency hoặc lỗi parser không được
ghi PASS. Không tạo dấu “tác giả đã đọc” từ việc AI trích nội dung.

## 7. Checkpoint 1: kiểm tra thiết kế ở phạm vi Phase 1

**Thực hiện inline, cùng ngữ cảnh; không phải đánh giá độc lập hoặc cross-model.**
Phán quyết thiết kế: **PASS cho kế hoạch Phase 1**, chưa cho phép tự chạy Phase 2.

| Vấn đề phát hiện | Cách xử lý đã đưa vào kế hoạch |
| --- | --- |
| Major: câu hỏi dễ giả định sẵn có lợi ích tiết kiệm. | RQ hỏi mức bằng chứng; query phản chứng; chấp nhận kết luận chưa tìm thấy. |
| Major: nêu tỷ lệ xác nhận của case đã chọn có thể che selection bias. | Ghi candidate pool, mẫu số, thất bại, comparator và thứ tự prediction→validation. |
| Major: khác reporter, terminal degron và protein tự nhiên. | Ghi endpoint/độ gần riêng, không gộp effect hoặc chuyển claim sang CT553H. |
| Minor: chỉ mục và access có thể bỏ sót nguồn. | Nhật ký phạm vi đã duyệt, vòng mở rộng cuối và access gaps. |

Phản biện mạnh nhất: tài liệu bên ngoài có thể xác nhận một số prediction
nhưng vẫn không trả lời hiệu quả kinh tế hoặc lợi ích riêng của CT553H. Bản
thiết kế giữ đây là kết quả hợp lệ, không lấy G2 làm lý do phải tìm được bằng
chứng dương. Bỏ bất kỳ một bài hạt giống nào vẫn giữ nguyên phương pháp tìm và
quy tắc kết luận; chưa có kết luận kết quả để kiểm độ bền.

Ở bước lập kế hoạch chưa có checkpoint 2/3. Sau tra cứu, các kiểm nội dung
tương ứng và giới hạn cùng-ngữ-cảnh được ghi ở [validation.md](validation.md).

## 8. Liên hệ nghiệm thu G2 và trạng thái chuyển tiếp

[Hồ sơ rà nghiệm thu G2 ngày 07/11](../g2-acceptance-2026-11-07/README.md) tách
bằng chứng cải thiện tính toán nội bộ, quyết định nghiệm thu và claim ứng dụng.
Tìm được tiền lệ wet lab không tự đóng G2; chưa tìm được số liệu tiết kiệm cũng
không tự bác bỏ đóng góp tính toán đã đo. Không tự thêm wet lab vào điều kiện
nghiệm thu nếu phạm vi đã chốt không yêu cầu.

**Checkpoint đã đóng:** `review-form-note` theo `deep-research/WORKFLOW.md`, mục
“Review-form note (#921)”. RQ/blueprint đã được xác nhận; câu trả lời “bắt đầu
tra cứu” giữ nguyên công việc, được ghi nhận `skip` đúng quy tắc của workflow.
Tiếp tục `full`, không tự chuyển sang systematic review hoặc hỏi lại note.
Không có Material Passport của pipeline được tạo trong lượt Phase 1 này; không
ghi nhận quyết định tác giả hoặc bước tìm kiếm chưa xảy ra.

**AI disclosure:** kế hoạch và báo cáo kết quả do Codex hỗ trợ. Nguồn live đã
được kiểm trong phạm vi ghi ở findings.md/validation.md; các phần chưa đọc vẫn
được giữ rõ. Không làm thay đổi nhãn, protocol, checkpoint hoặc mô hình phục vụ.
