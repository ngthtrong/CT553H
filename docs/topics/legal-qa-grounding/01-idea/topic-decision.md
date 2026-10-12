# Quyết định và phạm vi đề tài: hỏi–đáp pháp luật tiếng Việt có kiểm chứng trích dẫn

> Ngày: **12/10/2026**. Trạng thái: **sinh viên chốt làm đề tài ứng viên hàng đầu, cần Claude tự tìm hoàn toàn ngoài phạm vi các đề tài đang xét trong repo (bỏ ràng buộc lĩnh vực và khớp GVHD)** — theo đúng yêu cầu của sinh viên cùng ngày. **Chưa có phê duyệt GVHD.** Đây là lần đầu tiên repo này rời khỏi lĩnh vực tin sinh học/protein; mọi đề tài trước (`rtk-atp-applicability`, `degron-e3-specificity`, dark kinome DARKIN, sirtuin, senescence scRNA-seq) đều là dự đoán trên trình tự/omics protein.
>
> Nhãn bằng chứng dùng theo quy ước đã có trong repo ở [main-topic-decision.md](../../../common/deep-research/reports/main-topic-decision.md): **[ĐO]** tự chạy/tự tải trong phiên này, **[NGUỒN]** tác giả/tổ chức công bố, **[PHÂN TÍCH]** suy luận của Claude, **[ĐỀ XUẤT]** chưa thực nghiệm, **[CHƯA XÁC MINH]** chưa truy cập hoặc chưa kiểm được.

## 0. Yêu cầu của sinh viên dẫn tới tài liệu này

Nguyên văn yêu cầu (12/10/2026): không còn giới hạn về lĩnh vực hay các đề tài đang xem xét trong repo; có thể tìm một đề tài hoàn toàn khác; tiêu chí là **đóng góp và ý nghĩa thực sự**, **dữ liệu đủ khả thi và xử lý được**; mục tiêu là **chốt được đề tài trong ngày**; vẫn tham khảo **khung năm tiêu chí của GVHD** ([session-01-minutes.md, mục 4](../../../meeting/session-01-minutes.md)) và cách đánh giá một đề tài nghiên cứu nói chung; Claude quyết định toàn bộ, đóng vai nhà nghiên cứu tìm đề tài.

**Hệ quả cho cách áp khung cũ:** bảng trọng số ở [main-topic-decision.md mục 2](../../../common/deep-research/reports/main-topic-decision.md) có cột "khớp GVHD: lĩnh vực, phương pháp, năm tiêu chí" nặng 20%. Vòng này **tách đôi** cột đó — phần "khớp năm tiêu chí" (tính mới, phương pháp, XAI, website) vẫn giữ và áp đầy đủ; phần "khớp lĩnh vực chuyên môn của GVHD" **chủ động gác qua một bên** theo đúng yêu cầu hôm nay, nhưng được ghi lại thành rủi ro tường minh ở mục 8, không bị giấu đi.

## 1. Tên đề tài

> **Hệ thống hỏi–đáp pháp luật tiếng Việt có truy hồi bằng chứng và kiểm chứng trích dẫn, xử lý khoảng cách từ vựng giữa câu hỏi đời thường và văn bản luật.**
> (Vietnamese Legal Question Answering with Citation-Grounded Retrieval: Bridging the Colloquial-to-Statutory Lexical Gap)

Slug: `legal-qa-grounding`.

**Bài toán một câu:** người dân hỏi một câu luật bằng ngôn ngữ đời thường (không trích đúng thuật ngữ, không biết số điều/luật) → hệ thống phải (1) truy hồi đúng điều luật liên quan trong kho hàng nghìn điều, (2) sinh câu trả lời có trích dẫn điều luật cụ thể, (3) **tự kiểm chứng** câu trả lời sinh ra có thực sự được điều luật trích dẫn hậu thuẫn hay không trước khi hiển thị, và báo cho người dùng biết mức độ tin cậy.

## 2. Vì sao hình dạng này — khảo sát nhanh và loại các ứng viên khác

Trước khi chốt, đã khảo sát bốn hướng hoàn toàn khác lĩnh vực bioinformatics đang có trong repo:

| Hướng | Ý nghĩa thực tế | Dữ liệu | Tính mới | Quyết định |
|---|---|---|---|---|
| Phát hiện sâu bệnh lúa bằng ảnh (gắn với ĐBSCL, Cần Thơ) | Cao, gắn địa phương | **[NGUỒN]** không tìm thấy bộ dữ liệu ảnh sâu bệnh lúa Việt Nam/ĐBSCL công khai; gần nhất là dữ liệu Ấn Độ, Bangladesh | **Thấp** — mô hình quốc tế đã đạt 98,07% accuracy trên bài toán cùng dạng (EfficientNetB0, dữ liệu Uttarakhand 2022–2023) | **Loại** — bài toán gần như đã giải, không có dữ liệu bản địa |
| Chấm điểm tín dụng / phát hiện gian lận tài chính | Trung bình | Chỉ có bộ dữ liệu học thuật đã dùng lại rất nhiều (German Credit, Give Me Some Credit) | Thấp, đã bão hòa | **Loại** |
| Hỏi–đáp y tế tiếng Việt | Cao nhưng nhạy cảm (rủi ro sai lệch y khoa) | Dữ liệu công khai nhỏ, rải rác | Trung bình | **Gác lại** — mức độ nghiêm trọng khi trả lời sai cao hơn, cần thận trọng hơn phạm vi luận văn 8–9 tuần |
| **Hỏi–đáp pháp luật tiếng Việt có kiểm chứng trích dẫn** | **Cao, cụ thể: tiếp cận công lý cho dân thường** | **[ĐO] đã tải thử thành công, xem mục 4** | **Trung bình, có khoảng trống cụ thể đã xác minh (mục 3)** | **Chọn** |

## 3. Bằng chứng về khoảng trống nghiên cứu — tra cứu 12/10/2026

- **ALQAC** (Automated Legal Question Answering Competition) đang ở **lần tổ chức thứ 5**, đồng tổ chức với KSE 2025 tại Đà Lạt, 6–8/11/2025 — **[NGUỒN]** [alqac.github.io](https://alqac.github.io/). Cộng đồng vẫn hoạt động, không phải hướng đã nguội.
- **DRILL (VLSP 2025)** — shared task truy hồi văn bản luật tiếng Việt, **hơn 50 đội tham gia**. Chính ban tổ chức ghi nhận các hệ thống hiện tại **còn yếu** ở: suy luận thường thức (commonsense), ngữ cảnh rất dài, và suy luận thời gian — **[NGUỒN]** [DRILL Shared Task 2025, ACL Anthology](https://preview.aclanthology.org/setup/2025.vlsp-1.16).
- **Khoảng cách từ vựng câu hỏi đời thường ↔ thuật ngữ luật chưa được giải quyết hệ thống.** Bằng chứng gián tiếp: một chatbot pháp luật trên Hugging Face Spaces xử lý vấn đề này bằng một **prompt thủ công** yêu cầu LLM viết lại câu hỏi nhưng giữ nguyên thuật ngữ/số điều — **[NGUỒN, PHÂN TÍCH]** đây là một "patch" kỹ thuật, không phải một giải pháp được đo đạc có hệ thống trong một nghiên cứu. Không tìm thấy bài báo đánh giá trực tiếp độ chênh hiệu năng giữa câu hỏi hình thức (kiểu ALQAC, do người có kiến thức luật soạn) và câu hỏi đời thường thật.
- **Độ tin cậy của trích dẫn (citation faithfulness) là hướng đang hình thành, chưa chốt lời giải.** `RegRAG-VN` — benchmark đo hallucination/độ trung thực trích dẫn của mô hình ngôn ngữ nhỏ (≤7B) trên quy định ngân hàng tiếng Việt, nhắm nộp **IEEE-RIVF 2026** — **[NGUỒN]** [github.com/alitonia/regrag-vn](https://github.com/alitonia/regrag-vn). Việc một nhóm khác đang làm đúng hướng liền kề (ngân hàng, không phải luật dân sự/hình sự nói chung) vừa xác nhận ý nghĩa của bài toán, vừa là đối thủ cần trích dẫn và phân biệt rõ phạm vi khi viết khảo sát.
- **Không được nói "chưa ai làm RAG pháp luật tiếng Việt"** — đã có ít nhất `VietLegal-RAG`, `vietnam-legal-rag` (GitHub), một chương Springer 01/2026 về chiến lược truy hồi cho RAG pháp luật tiếng Việt, và một pipeline GraphRAG (FPT). **Đóng góp phải định vị ở chỗ cụ thể**: đo định lượng khoảng cách đời thường↔hình thức trên cùng một hệ thống, cộng module kiểm chứng trích dẫn tích hợp vào sản phẩm đầu cuối — không phải "làm RAG luật đầu tiên".

## 4. Dữ liệu — đã kiểm tra khả thi thật trong phiên này

**[ĐO], chạy `curl` trực tiếp trong phiên 12/10/2026, không chỉ đọc mô tả:**

- `huggingface.co`, `github.com`, `api.github.com`, `raw.githubusercontent.com` đều trả **HTTP 200/401** (401 nghĩa là tới được server, chỉ thiếu quyền truy cập file gated — không phải chặn mạng). Khác với tình trạng "403 ở bước CONNECT" ghi nhận cho một môi trường cloud khác trong [resources.md](../../../common/resources.md) ngày 07/10/2026 — **đây là lần đo riêng của phiên này, không suy ra tình trạng mạng của mọi môi trường**.
- Tìm thấy ba repo GitHub của sinh viên dự thi mỗi năm, mỗi repo có thư mục `data/` chứa dữ liệu ALQAC gốc: `DucLong06/ALQAC2023` (đội đạt **giải nhất Task 2**, có bài IEEE KSE 2023), `pynterest83/ALQAC2024`, `phongvt2004/ALQAC-2025`.
- **Tải thử thành công** từ `DucLong06/ALQAC2023`:
  - `data/training/all_articles_2023.json` — **2.249 điều luật**, 2,6 MB, định dạng `{"Tên luật@số điều": "nội dung điều"}`.
  - `data/raw/train.json` — **100 câu hỏi** kèm `relevant_articles` (law_id + article_id) và đáp án, định dạng JSON sạch.
  - `data/raw/public_test.json` — **100 câu**; `data/raw/private_test.json` — **110 câu**.
  - Tổng riêng năm 2023: **2.249 điều luật, 310 câu hỏi có nhãn vàng** (câu hỏi Đúng/Sai và trắc nghiệm, do ban tổ chức ALQAC soạn và gán nhãn độc lập — không phải nhãn tự sinh bởi pipeline của đề tài → thỏa **G1**).
  - Cộng dồn được với ALQAC 2021, 2022, 2024, 2025 (cùng cấu trúc theo README các repo) → ước lượng vài trăm đến ~1.000 câu hỏi có nhãn, kho điều luật hàng nghìn mục — đủ để huấn luyện/đánh giá truy hồi kiểu contrastive và tinh chỉnh nhẹ, dù **không lớn bằng dữ liệu ảnh/omics** đã dùng ở các đề tài trước.
- **Mẫu dữ liệu thật đã xem** (câu DS-1): *"Người nghiện ma túy từ đủ 18 tuổi trở lên bị áp dụng biện pháp xử lý hành chính đưa vào cơ sở cai nghiện bắt buộc theo quy định của Luật Xử lý vi phạm hành chính khi bị phát hiện sử dụng chất ma túy một cách trái phép trong thời gian cai nghiện ma túy tự nguyện, đúng hay sai?"* → nhãn: Đúng, điều 32 Luật Phòng, chống ma túy. Đây là **câu hỏi hình thức** (văn phong luật), không phải câu hỏi đời thường thật — xác nhận đúng khoảng trống ở mục 3: cần **tự thu thập thêm** một tập câu hỏi đời thường để đo độ chênh.

### 4.1 Phần dữ liệu CHƯA xác minh — phải làm trước khi đi sâu

- **[CHƯA XÁC MINH] Điều khoản tái sử dụng dữ liệu ALQAC ngoài phạm vi cuộc thi.** Dữ liệu lấy được qua mirror GitHub của thí sinh, không phải nguồn phát hành chính thức ghi rõ giấy phép. Phải đọc kỹ trang chính thức [alqac.github.io](https://alqac.github.io/) hoặc liên hệ ban tổ chức (Nguyễn Lê Minh và cộng sự, nhóm JAIST/VNU) trước khi dùng rộng cho luận văn — đây là cổng cần đóng sớm, tương tự cách các đề tài trước phải kiểm giấy phép MIT/CC0/CC-BY-NC-ND.
- **[ĐỀ XUẤT] Tập câu hỏi đời thường thật:** cần tự thu thập ~100–300 câu hỏi pháp luật do dân thường đặt (ví dụ mục Hỏi–đáp pháp luật công khai trên cổng thông tin chính phủ hoặc `thuvienphapluat.vn`), **ẩn danh người hỏi** trước khi lưu — áp đúng quy ước bảo vệ dữ liệu cá nhân đã có trong [CLAUDE.md](../../../../CLAUDE.md). Chưa thực hiện.
- Chưa kiểm dữ liệu DRILL/VLSP 2025, MLQA-TSR có công khai được không hay chỉ dành cho đội đăng ký.

## 5. Phương pháp đề xuất

Ba thành phần, mỗi thành phần gắn một câu hỏi nghiên cứu đo được — theo đúng yêu cầu GVHD đã nêu với đề tài trước ("mỗi thành phần gắn một phép đo tự thực hiện", [work-log 11/10/2026 khuya](../../../common/work-log.md)):

1. **Truy hồi lai (hybrid retrieval):** BM25 + embedding câu tiếng Việt (PhoBERT/Vietnamese-SBERT hoặc đa ngữ BGE-m3 đã có sẵn trong `ml/requirements.txt` của repo) + một bước **viết lại câu hỏi** từ văn phong đời thường sang gần văn phong luật trước khi truy hồi.
2. **Sinh câu trả lời có trích dẫn:** một LLM tiếng Việt cỡ nhỏ (có bản fine-tune luật sẵn, ví dụ `Qwen2.5-3B-legal-vn` trên Friendli — **[NGUỒN]**, cần kiểm license trước khi dùng) sinh câu trả lời kèm trích dẫn điều luật đã truy hồi.
3. **Kiểm chứng trích dẫn (citation verification):** một bước hậu kiểm kiểu NLI (entailment) giữa câu trả lời sinh ra và nội dung điều luật được trích, gắn nhãn tin cậy hiển thị cho người dùng (đạt/không đạt/không chắc).

**RQ1 (tiêu chí 2–3 — phương pháp):** truy hồi lai có cải thiện Recall@k / F2 so với BM25-only và embedding-only hay không, đo **riêng** trên tập câu hỏi hình thức (ALQAC) và tập câu hỏi đời thường tự thu thập — độ chênh giữa hai tập chính là con số định lượng khoảng trống ở mục 3.

**RQ2 (tiêu chí 4 — XAI):** module kiểm chứng trích dẫn có phát hiện được câu trả lời không được điều luật hậu thuẫn hay không, đo trên một tập nhỏ do người gán nhãn thủ công (so với đối chứng: hiển thị thẳng output LLM không qua kiểm chứng).

## 6. Áp khung đánh giá — năm tiêu chí GVHD + ba cổng G1/G2/G3 (đã điều chỉnh)

| Tiêu chí GVHD | Đánh giá |
|---|---|
| 1. Tính mới | **Trung bình.** Không phải RAG luật đầu tiên (mục 3 đã nêu rõ đối thủ); mới ở chỗ đo định lượng khoảng cách đời thường↔hình thức trên cùng hệ thống, cộng kiểm chứng trích dẫn tích hợp sản phẩm cuối — không được bán như "đầu tiên" |
| 2–3. Đề xuất/cải tiến + dùng phương pháp mới | **Khá** — truy hồi lai có viết lại câu hỏi, kiểm chứng trích dẫn kiểu NLI là tổ hợp cụ thể, đo được qua RQ1/RQ2 |
| 4. XAI | **Tốt, tự nhiên** — kiểm chứng trích dẫn chính là phần XAI, không phải phần gắn thêm |
| 5. Website/ứng dụng | **Tốt nhất trong mọi đề tài đã xét ở repo này** — sản phẩm nghiên cứu chính **là** một hệ thống hỏi–đáp web, không phải phụ lục đi kèm mô hình dự đoán |

| Cổng | Kết quả | Căn cứ |
|---|---|---|
| **G1** nhãn thực nghiệm/độc lập | **ĐẠT** | Nhãn ALQAC do ban tổ chức/chuyên gia luật gán, không do pipeline đề tài tự sinh — đã tải và xem mẫu thật |
| **G2** đóng góp dương đo được | **CHƯA XÁC LẬP** | Cần chạy baseline thật trong 1–2 tuần đầu để biết độ chênh đời thường/hình thức và hiệu quả module kiểm chứng có đo được rõ hay không — giống hệt tình trạng G2 của `degron-e3-specificity` lúc mới chốt |
| **G3** ứng dụng/website khả thi | **ĐẠT, mạnh** | Không có sản phẩm cạnh tranh trực tiếp làm đúng tổ hợp "truy hồi lai câu hỏi đời thường + kiểm chứng trích dẫn hiển thị cho người dùng cuối" |
| *(gác lại hôm nay)* khớp lĩnh vực chuyên môn GVHD | **YẾU, biết trước, xem mục 8** | GVHD chuyên tin sinh học/protein, không có công bố nào về NLP/pháp luật |

## 7. Tài nguyên tính toán — ước lượng, chưa đo thật

**[ĐỀ XUẤT], chưa chạy:** embedding tiếng Việt cỡ nhỏ (PhoBERT-base, Vietnamese-SBERT) chạy được trên CPU cho vài nghìn điều luật trong vài phút; LLM sinh câu trả lời 3B tham số chạy suy luận được trên GPU đã có theo xác nhận trước đó của sinh viên ([main-topic-decision.md mục 0](../../../common/deep-research/reports/main-topic-decision.md)); không cần huấn luyện mô hình ngôn ngữ từ đầu. Nhẹ hơn đáng kể so với các đề tài tin sinh học đã xét (không cần ProtT5/ESM-2 hàng chục GB cache).

## 8. Rủi ro phải nói thẳng, không giấu

- **Khớp GVHD là rủi ro lớn nhất, không phải rủi ro kỹ thuật.** 14 công trình trong danh mục GVHD ([advisor/README.md](../../../common/advisor/README.md)) đều là tin sinh học/protein; không có công trình nào về NLP, truy hồi thông tin, hay pháp luật. Đây là lựa chọn của sinh viên hôm nay nhằm mở rộng tìm kiếm hoàn toàn ngoài khung đó — **bắt buộc phải hỏi thẳng GVHD ở buổi báo cáo tuần 6 liệu thầy có nhận hướng dẫn đề tài ngoài chuyên môn hay không**, trước khi đầu tư thêm công sức.
- Dữ liệu ALQAC quy mô khiêm tốn (hàng trăm câu hỏi có nhãn mỗi năm) so với các bộ omics đã dùng ở đề tài trước (hàng trăm nghìn phép đo) — đủ cho một luận văn kỹ thuật phần mềm tập trung vào hệ thống, nhưng **không đủ** nếu hội đồng kỳ vọng độ sâu thực nghiệm kiểu học máy thuần.
- Trả lời sai về pháp luật có hậu quả thật với người dùng — sản phẩm phải có cảnh báo rõ "không thay thế tư vấn pháp lý", và đây là lý do chọn luật thay vì y tế (mức độ nghiêm trọng khi sai thấp hơn, nhưng không phải bằng không).
- License dữ liệu ALQAC ngoài phạm vi thi đấu **chưa xác minh** — nêu ở mục 4.1, phải đóng trước khi dùng dữ liệu cho báo cáo chính thức.

## 9. Việc còn phải làm trước khi trình GVHD tuần 6

1. Xác minh điều khoản sử dụng dữ liệu ALQAC ngoài phạm vi thi (liên hệ ban tổ chức hoặc đọc kỹ trang chính thức).
2. Gộp dữ liệu ALQAC 2021–2025 (nếu các năm khác cũng mirror công khai như 2023), đếm thật tổng số câu hỏi/điều luật dùng được — hiện mới đếm riêng năm 2023.
3. Chạy baseline BM25-only và embedding-only thật để có số liệu đầu tiên cho G2.
4. Thu thập và ẩn danh một tập nhỏ câu hỏi đời thường thật (~100–300 câu) để đo khoảng cách đời thường/hình thức.
5. Chuẩn bị câu hỏi xin ý kiến GVHD về việc hướng dẫn một đề tài ngoài chuyên môn protein của thầy — đây là câu hỏi quan trọng nhất, quan trọng hơn mọi chi tiết kỹ thuật ở trên.
