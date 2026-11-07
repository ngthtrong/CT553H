# Biên bản kiểm nguồn và đầu ra — 07/11/2026

## Phạm vi thực thi

ARS `deep-research/full`, tiếp tục kế hoạch đã duyệt. `review-form-note` đã đóng
theo câu trả lời nguyên văn **“bắt đầu tra cứu”**, tức giữ nguyên công việc và
`skip` note. Không chuyển sang systematic review, không có Material Passport của
academic-pipeline và không cấp dấu người dùng đã đọc nguồn.

| Giai đoạn | Đầu ra thực tế |
| --- | --- |
| Phase 1 | RQ/blueprint và kiểm tra thiết kế trong README kế hoạch; người dùng đã yêu cầu thực hiện. |
| Phase 2 | 39 query web, 95 thao tác search/open/find/click được ghi trong 19 batch; tám study trong results.json, bốn đầu mối/loại trừ nêu riêng. |
| Phase 3 | Tổng hợp theo validation sinh học, mức bằng chứng nguồn lực và khả năng áp dụng; kết quả bất lợi giữ ở findings.md §§2–4. |
| Phase 4 | Bản báo cáo findings.md với bảng claim, giới hạn và danh mục nguồn. |
| Phase 5 | Kiểm nội dung/attribution cùng session dưới đây; không phản biện độc lập hoặc hội đồng. |
| Phase 6 | Giữ các sửa phân loại và claim có giới hạn trong bản giao; kiểm JSON/CSV/link/hash ở cuối. |

Các vai trò nghiên cứu được dùng inline theo hợp đồng trong skill. Hai worker
native `gpt-6-astra` đã khởi động cho Phase 2 nhưng dừng vì usage limit trước
khi ghi file cuối; kết quả chấp nhận được session chính đọc lại từ nguồn.
Không đổi model để lặp lại dispatch; không ghi hai worker là hoàn tất.
39 query và 95 thao tác chỉ đếm receipt của session chính; không dựng lại số
lần tìm của worker bị ngắt từ các thông báo tiến độ không có nhật ký đầy đủ.

## Kiểm nguồn Phase 2

Đọc phần nguồn hỗ trợ claim, không chỉ xác nhận DOI tồn tại. Title/DOI/year
được đối chiếu với trang bài/PMC/PubMed trong phạm vi access đã ghi. Phân loại
thiết kế theo câu hỏi sinh học; không coi case laboratory là clinical RCT.

| ID | Loại bằng chứng phù hợp | Giới hạn nguồn lực/utility | Disclosure đã kiểm |
| --- | --- | --- | --- |
| S01 | Follow-up peptide có WT/mutant control; model-guided selection | Không có nhánh chọn random để xác lập lợi ích lựa chọn; S4G chưa đọc độc lập | Quan hệ tài chính/công ty và vai trò biên tập được công bố |
| S02 | Case protein đầy đủ, có biological replicate | FBXL15 đã có prior assay; server runtime không là wet-lab savings | Vai trò Executive Editor NAR |
| S03 | Case CBX6 với turnover và binding perturbation | Một case, binding chưa mất hết; claim annotation effort định tính | Tác giả báo không có competing interests |
| S04 | Mutation-aware abundance follow-up, kèm context limits | Các case chọn; 164 tile là validation khác; supplement chưa audit | Peptone consulting/stock options |
| S05 | Screen/DegronID và hypothesis follow-up | Nguồn nhãn CT553H; nhiều tiêu chí cùng chọn sáu protein; không binary hit rate | Quan hệ công ty/advisory/editorial |
| S06 | Lab automation thực, kèm retrospective strategy comparison | Duration thực khác forecast; cost estimate khác savings; model và robotics cùng thay | Patent application liên quan |
| S07 | Wet-lab workload thực và simulation | Đối chứng DE về nguồn lực là counterfactual; không lượng hóa tiền tiết kiệm | PubMed báo không có competing interests |
| S08 | Benchmark hồi cứu có greedy/random controls | Không wet lab mới; không tổng quát kết quả âm sang mọi active learning | Không competing interests; funding Microsoft/NSF được công bố |

Mức sử dụng: S01–S05 là bằng chứng gốc cho các phép đo/case được mô tả;
S06–S07 chỉ hỗ trợ tiền lệ lĩnh vực lân cận; S08 là phản chứng hồi cứu có giới
hạn. Không có nguồn nào được chấm là đã xác nhận hiệu quả kinh tế của CT553H.
Không chạy xác minh API/Semantic Scholar/OpenAlex, không kiểm blacklist có phí,
không cấp trạng thái retraction “clean”. Đã ghi metadata erratum S05; hình sửa
chưa đọc đủ. Các hạn chế truy cập không được chuyển thành kết luận tiêu cực.

## Kiểm phản biện và sửa diễn giải

**Cùng ngữ cảnh và cùng session; đây là kiểm nội dung, không phải một reviewer
độc lập.** Checkpoint 1 giữ ở kế hoạch. Checkpoint 2/3 kiểm các vấn đề sau:

| Checkpoint | Vấn đề cụ thể | Xử lý trong bản giao |
| --- | --- | --- |
| 2 — Major | Dùng tỷ lệ xác nhận của selected cases như lợi ích model so random | S01 ghi 16/21 và năm ca không xác nhận, nhưng không suy causal utility hoặc tiết kiệm; S02 ghi prior-data selection. |
| 2 — Major | Chuyển một kết quả mutation/full-length sang mọi protein | S03 giữ residual binding; S04 giữ PTEN/proline exceptions; không đổi endpoint. |
| 2 — Major | Nhầm thời gian dự báo với thời gian thực | S06 báo gần sáu tháng thực, tách hai tháng dự báo và comparator thủ công ước lượng. |
| 3 — Major | Nhầm ngân sách run với số tiền tiết kiệm | S06 giữ 5.200 USD là estimate một run, không có giá trị tiền tiết kiệm đo được. |
| 3 — Minor | 96 wells bị diễn giải như 96 biến thể độc lập hoặc hit | S07 giữ đơn vị plate và không suy số mutation/hit. |
| 3 — Minor | Tra cứu có giới hạn bị gọi là systematic/exhaustive | Phần phương pháp/giới hạn ghi query xếp hạng, off-topic results, candidate gaps và supplement thiếu. |

Kết quả kiểm: các sửa diễn giải trên hiện có trong `findings.md`; không còn
claim CT553H đã wet-lab validated hoặc đã tiết kiệm tiền/giờ. Kết luận tìm kiếm
vẫn là kết luận có phạm vi; thiếu supplement và các đầu mối chưa đọc là hạn
chế còn lại, không được xóa bằng một vòng tự chấm điểm.

## Attribution, disclosure và tính toàn vẹn

- Mọi study trong ma trận có DOI, URL và locator; danh mục tác giả đầy đủ giữ
  trong JSON để tránh gộp sai metadata. Bản report dùng citations ngắn kèm DOI.
- Không trích dài bài báo; số liệu là số tác giả đã báo, không phải kết quả mới
  của CT553H. 16/21 và năm ca còn lại là phép cộng/trừ minh bạch từ 8/12 + 8/9.
- Không can thiệp dataset, checkpoint, runtime, nhãn hoặc serving model. Dữ liệu
  riêng và manuscript không được gửi tới external model; chỉ truy cập nguồn
  công khai để tìm tài liệu.
- Không có người tham gia được tuyển hoặc dữ liệu cá nhân mới được thu thập.
  Các kết luận không mở rộng thành chẩn đoán bệnh, nghiệm thu G2/G3 hoặc quyết
  định hành chính của tổ chức.

## PDF và giới hạn lưu trữ

PDF Zhang được tải từ URL trang tác giả trong `search-receipts.json`, SHA-256
`851201eaea1f22648ebafac147b4b9435971af29022fd7d43d24ddc57f279d55`, 12.552.014 byte.
`pdf_read_preflight.py` báo **UNAVAILABLE: pypdf-not-installed**; không ghi PASS.
Đọc text bằng Poppler và chỉ dùng section/figure locators. PDF/text tạm ở
`/tmp/ct553h-wetlab-aphnht89/`, không đưa bản toàn văn lớn vào bộ đầu ra Git.

Không coi việc clone repo là có mọi toàn văn. Các trang công khai có thể thay
đổi hoặc bị challenge; receipt lưu URL và phạm vi đọc, không chứng nhận lưu
trữ đủ mọi byte của bài báo.

## Kiểm đầu ra

Các kiểm thực tế gồm: JSON parse, tám ID không trùng, DOI/URL không rỗng,
CSV đọc lại khớp số hàng và giá trị gốc, 39 query/95 thao tác khớp receipt,
đối chiếu 16/21 và tổng dự toán SAMPLE, local links và `git diff --check`.
Hash của bộ file giao nằm trong [artifact-manifest.json](artifact-manifest.json).
Đây là kiểm cấu trúc/tính nhất quán, không xác nhận độc lập mọi diễn giải.

Đã chạy `check_acronyms.py` trên report. Phủ kiểm là **body/partial** vì công cụ
chỉ có en/zh-TW còn bản này tiếng Việt. Đã giải thích WT, CHX và OOF; nhiều
finding còn lại là tên protein/công cụ, tên file hoặc token do chữ hoa tiếng
Việt. Advisory được lưu ở [acronym-advisory.json](acronym-advisory.json), không
đổi thành chứng nhận ngôn ngữ “clean” hoặc yêu cầu trả lời từ người dùng.
