# Nhật ký làm việc

> Mỗi phiên làm việc có thay đổi đáng kể thì thêm **một mục lên đầu** (mới nhất ở trên). Ghi ngắn: đã làm gì, quyết định gì, còn dở gì. Chi tiết nằm trong các tài liệu được liên kết, không chép lại ở đây. Đầu phiên mới, đọc mục mới nhất để nắm tình hình.

---

## 02/10/2026 (tiếp) — khảo sát tính cấp thiết và tình hình nghiên cứu, cập nhật Notion và slide (`rtk-atp-applicability`)

**Đã làm**
- Trả lời bốn câu của người dùng (input, output, dữ liệu, tính cấp thiết) **kèm trích dẫn kiểm chứng được**, tra cứu qua PubMed.
- Lấy **ví dụ thật** từ `proteins.jsonl`: protein `P34891` (RTK-69, 488 aa) có đúng 10 residue dương (2,05%) ở đoạn **150–158** (`LGSGFFGEV`, glycine-rich loop G-x-G-x-x-G) và **183** (`K`, lysine xúc tác VAIK) — nhãn khớp sinh học đã biết.
- Khảo sát mức cạnh tranh: **7 công trình dự đoán ATP site 2023–2026** (E2EATP, ATP_mCNN, Multiview-ATPBind, GPSite, RTK_RAG, PFDCNN, Transformer+DQN); hai trong đó của nhóm GVHD. Chuỗi công trình nhóm GVHD: DeepATP 2019 → mCNN-PSSM 2022 → ATP_mCNN 2024 → RTK_RAG 2025.
- **Ba bằng chứng đọc trực tiếp từ `ci5c00766.pdf`:**
  - **A:** Methods ghi 313 chuỗi RTK → một lần CD-HIT 40% → 69 protein đánh giá, **244 chuỗi còn lại thành kho RAG**. Theo định nghĩa CD-HIT, chuỗi bị loại có identity ≥ ngưỡng với đại diện cụm → kho RAG có thể chứa họ hàng ≥40% của mọi protein kiểm tra. **Chưa xác nhận bằng alignment.**
  - **B:** Dòng Bảng 5 `RAG_ProtTrans` (mô hình cuối) **trùng từng chữ số** với dòng dropout = 0,9 của Bảng 4 (0,9747/0,9896/0,9895/0,6782/0,9868); baseline không RAG ở Bảng 5 lại là dòng Bảng 2 (MCC 0,3181), không được hưởng cùng lượt quét. Riêng dropout 0,7 → 0,9 đã đưa MCC 0,2983 → 0,6782. Lợi ích truy hồi và lợi ích dropout bị trộn.
  - **C:** RTK-69 có 73.270/73.981 residue âm → mô hình rỗng đạt accuracy **99,04%**. Cả năm phương pháp ở Bảng 6 (0,9851 · 0,9885 · 0,9814 · 0,9873 · 0,9895) **đều thấp hơn mốc đó**.
- **Cập nhật trang Notion** (2 lượt `update_content`): thêm mục **★ Tính cấp thiết, tình hình nghiên cứu và khoảng trống** (A/B/C), ví dụ thật P34891 vào mục 2, mốc 99,04% vào mục 7, **câu hỏi GVHD thứ 7** (về 244/69 CD-HIT), tài liệu **[10]–[16]**, và hai dòng giới hạn mới vào mục 14.
- **Tạo deck thứ hai — slide diễn giải 13 trang:** https://claude.ai/artifact/A7kgUgsr28RBUSd59knh1q, mã nguồn [explainer-slides/](../topics/rtk-atp-applicability/04-proposal/explainer-slides/). Bố cục do người dùng chỉ định: mô tả bài toán (2 trang) → tính cấp thiết / nghiên cứu đã có / vì sao cần làm (4 trang) → input → output → dữ liệu (2 trang) → cách đánh giá (2 trang). Ba hình minh họa: biểu đồ cột điểm ATP theo 20 residue của P34891, sơ đồ RTK–màng–túi ATP (SVG, nhãn đặt bằng HTML để dùng đúng font), đường đánh đổi coverage–risk. Bảng `prior-work` liệt kê 10 công trình 2018–2026 kèm tạp chí và số trang. Sau đó thêm **phần 7** theo yêu cầu: trang `risks` (4 rủi ro × dấu hiệu nhận biết × cổng dừng, cộng 2 giới hạn không khắc phục được và rủi ro định vị) và trang `questions` (7 câu xin ý kiến GVHD, chia hai nhóm phạm vi/đóng góp và dữ liệu/phương pháp) — deck thành **15 trang, 6 section**.
- **Cập nhật slide buổi gặp lên bản 8, 13 → 15 trang:** thêm `landscape` (vị trí 3) và `evidence` (vị trí 9); `scope` đổi sang bảng P34891 thật; `metrics` đổi thẻ accuracy thành mốc 99,04%; đánh số lại footer toàn deck.

**Quyết định**
- **Không cạnh tranh bằng độ chính xác.** Lĩnh vực đã có ensemble Transformer+DQN và geometric DL; một người 14 tuần không thắng được. Giữ trục giao thức + miền áp dụng + hệ thống.
- **Tự nói ra điểm công bằng:** benchmark ATP kinh điển (ATP-388/41, ATP-227/17) **đã** lọc CD-HIT 40%. Không được nói "các bài trước không kiểm soát đồng dạng" — sẽ bị bác. Khoảng trống thật hẹp hơn: rò rỉ qua kho truy hồi, rò rỉ khi chọn cấu hình, và việc không ai báo kết quả phân tầng theo identity.
- Bằng chứng A trình bày **dạng câu hỏi cho GVHD**, không phải cáo buộc; B và C mới là nội dung chính vì kiểm chứng được tại chỗ.
- Tính cấp thiết của **lĩnh vực** (48/94 thuốc kinase FDA nhắm RTK) không phải tính cấp thiết của **đóng góp** — không mở đầu buổi gặp bằng số liệu FDA.

**Còn dở**
- **`topic-proposal.md` trong repo chưa được cập nhật** theo Notion: thiếu mục ★, ví dụ P34891, câu hỏi thứ 7, tài liệu [10]–[16]. Notion đang đi trước repo.
- Chưa tạo `02-survey/related-work-and-motivation.md`; `key-papers.md` vẫn chỉ có 9 tài liệu, chưa có [10]–[16].
- Vẫn còn: điền tên và MSSV vào slide bìa; chưa tự xem lại 15 trang trên claude.ai.
- Việc kỹ thuật đầu tiên không đổi: **chạy alignment và gom cụm đồng dạng** — đây cũng là việc duy nhất xác nhận được Bằng chứng A.

## 02/10/2026 — chốt đề tài RTK–ATP, viết lại thuyết minh, Notion và slide (`rtk-atp-applicability`)

**Đã làm**
- **Chốt đề tài** (quyết định của sinh viên, chưa có phê duyệt GVHD): *Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu.* Slug: `rtk-atp-applicability`.
- Viết [thuyết minh chi tiết 14 mục](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md): phạm vi mức residue và danh sách "không làm", mô hình nền RTK_RAG, bốn loại rò rỉ, giao thức 9 bước + hai kịch bản, hai RQ, chỉ số, dữ liệu, sản phẩm, ba đóng góp, kế hoạch 14 tuần, sáu câu hỏi GVHD, điều chưa có.
- Viết [dàn ý và kịch bản trình bày](../meeting/2026-10-02-rtk-atp-slide-outline.md): mạch 13 slide, sáu câu hỏi dễ gặp kèm câu trả lời, checklist trước buổi.
- **Viết lại artifact slide** thành 13 trang cho đề tài đã chốt (bản 4): https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT. Bỏ 5 slide cũ (`framing`, `gap`, `proposal`, `backup`, `research-questions`), thêm 7 slide mới (`scope`, `pipeline`, `data`, `leakage`, `protocol`, `rq1`, `rq2`, `metrics`, `contributions`).
- **Tạo trang Notion mới** dưới *Ý tưởng luận văn*: [Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880). Đã kiểm lại render: callout, 11 bảng và sơ đồ mermaid đúng.
- Chạy lại `ml/rtk-atp-applicability/preprocessing/prepare_data.py` để xác nhận dữ liệu tái tạo được: exit 0, `validation_errors` rỗng, số liệu khớp [báo cáo dữ liệu](../topics/rtk-atp-applicability/03-data/data-report.md).
- Đọc trực tiếp mã nền để slide không nói sai: `Dataset/rag_prottrans_GPU.py` dùng `cdist` tới mọi residue trong kho, lấy 5 gần nhất, trộn `(query + trung bình)/2` — tức k=5 **ở mức residue**, 1:1. Cấu hình MCNN trong notebook: `WINDOW=6`, `WINDOW_SIZES=[6,8,10]`, `NUM_FILTER=256`, `DROP=0.0`, `EPOCHS=3`, `K_Fold=5`.

**Quyết định**
- Dùng cụm **"kiểm soát rò rỉ"**, không dùng "chống rò rỉ"/"không rò rỉ": PLM có thể đã gặp các chuỗi này khi tiền huấn luyện và đề tài không đo được ảnh hưởng đó.
- **Thu từ ba RQ xuống hai.** RQ1: truy hồi giúp bao nhiêu khi kiểm soát đồng dạng (ba nhánh A/B/C, nhánh C k-NN là nhánh không được cắt). RQ2: identity có dùng được làm **tín hiệu miền áp dụng** không — không gọi là "độ tin cậy". RQ3 cũ gộp vào RQ2; so sánh chọn ngưỡng test/validation hạ thành thí nghiệm kiểm toán phụ.
- Tách "rò rỉ" thành **bốn loại** riêng (giữa protein, đồng dạng, qua kho truy hồi, khi chọn mô hình) thay vì gộp một tên.
- Phân biệt **hai kịch bản đánh giá**: nghiêm ngặt (không láng giềng quá 30%) và sử dụng thực tế (cho phép homolog trong kho, báo kết quả chia theo mức identity). Đồng dạng trong kho không tự động là rò rỉ.
- **Không còn gọi toàn bộ 69 RTK là independent test**; tách RTK-development và RTK-test để khóa ngưỡng cảnh báo.
- **Cách định vị khi trình bày:** mở đầu bằng "em muốn đo điều kiện mà truy hồi thật sự hữu ích", không mở đầu bằng "bài cũ bị rò rỉ". Phần kiểm toán mã dùng để thiết kế giao thức của mình.
- Bỏ hướng dự phòng efflux khỏi phạm vi; bỏ claim "+3 tập ATP ngoài nhóm 388/41/17" khỏi slide vì chưa tải và không phải bộ RTK thay thế.
- Đính chính claim cũ: repo RTK_RAG **có** mã dựng đặc trưng truy hồi; tài liệu khảo sát trước ghi là thiếu.

**Còn dở**
- **Điền tên và MSSV vào slide bìa** (đang là `[Họ tên sinh viên]` / `[MSSV]`).
- Chưa tự xem lại deck 13 trang trên claude.ai — nếu có chỗ tràn hoặc xuống dòng xấu thì nói để sửa.
- Việc kỹ thuật đầu tiên: **chạy alignment và gom cụm đồng dạng**. Hiện chỉ biết ba bộ không trùng chuỗi hoàn toàn, chưa biết có độc lập ở 30%/40% identity hay không.
- Sau buổi gặp: ghi `docs/meeting/session-01-minutes.md` với câu trả lời của GVHD cho sáu câu hỏi.
- `05-design/` và `06-experiments/` chưa tạo; chưa có `backend/`, `frontend/`, `ml-service/`, `thesis/`.

## 01/10/2026 — khảo sát lại tin sinh theo trọng tâm ứng dụng/hệ thống

- **Người dùng xác nhận:** luận văn một người, 14 tuần, sáng 02/10 trình bày ý tưởng; RAG hoặc CNN/MCNN đều được, ưu tiên phù hợp bài toán. Chưa chọn đề tài.
- Đọc trực tiếp rubric CT553H: phát triển ứng dụng 40%, báo cáo khoa học 40%, thái độ/trình bày 20%. Đối chiếu nguồn chính thức và tiền lệ GeneGPT, BioChatter, 2D-ProteinRAG, RTK_RAG, semantic search GEO, ScIRGen và Cellpose.
- Lưu [khảo sát thiên về hệ thống](deep-research/reports/bioinformatics-application-topics.md): năm hướng, phân tích sâu ba hướng, dữ liệu, MVP, đối chứng, đánh giá và kế hoạch 14 tuần. Ưu tiên đề xuất A (hồ sơ bằng chứng protein/RAG) theo mong muốn người dùng; B (rà soát ATP/CNN) nếu thầy hỗ trợ pipeline; C (sàng lọc GEO) là lựa chọn thứ ba. Chưa có đo thực nghiệm hoặc xác minh nhu cầu người dùng.
- Soạn [bản trình bày sáng mai](../meeting/bioinformatics-application-pitch.md): lời mở đầu, so sánh, dàn ý năm slide, trả lời phản biện và câu hỏi cho thầy. Cập nhật trạng thái trong danh sách đề tài; tài liệu/slide/Notion cũ chưa được viết lại.
- Còn cần thầy xác nhận: loại đóng góp chấp nhận được, người kiểm tra bằng chứng/nhãn, pipeline khả dụng, GPU/ngân sách API. Không coi đề xuất ATP trước đó là đã chốt.

## 01/10/2026 — kiểm chứng G-mean trong notebook RTK_RAG

- Tải và đọc trực tiếp notebook tại commit `b7bd4c2347c7d44d24ae3d13e42082ba6cd62627`; xác nhận `model_test` chọn ngưỡng G-mean từ nhãn của tập đang đánh giá rồi tính MCC/F1 trên cùng tập.
- Lưu [bằng chứng và liên kết cố định](deep-research/reports/rtk-rag-threshold-verification.md): vị trí ô/dòng, lời gọi cross/independent, output lưu sẵn, thiếu module nạp dữ liệu và lỗi số giá trị trả về. Chưa chạy lại mô hình hoặc xác nhận phiên bản tạo kết quả bài báo.
- Cập nhật checklist và RQ2 trong [prep](../meeting/session-01-prep.md): đổi ngưỡng đơn thuần không làm thay đổi AUPRC/AUROC; xáo nhãn kho không tác động tới phép trộn embedding không dùng nhãn.
- Còn lại: người trình bày tự mở đoạn mã được dẫn; hỏi GVHD về phiên bản đánh giá dùng trong bài và nguồn chọn ngưỡng.

## 01/10/2026 (tối, tiếp) — slide buổi gặp và bản nguồn Notion

**Đã làm**
- Tạo **artifact slide mới** 9 trang cho buổi gặp tin sinh: https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT. Mã nguồn ở [meeting/session-01-slides/](../meeting/session-01-slides/). Nội dung theo khung trình bày trong prep: khung đóng góp → ba điểm trong giao thức → đề xuất ATP → ba RQ → sản phẩm → kế hoạch và cổng dừng → dự phòng efflux → năm câu hỏi cho GVHD.
- Chuyển mã nguồn slide cũ (đề tài chi tiêu) sang [personal-expense-management/01-idea/slides-draft/](../topics/personal-expense-management/01-idea/slides-draft/). Artifact cũ giữ nguyên URL, không ghi đè, vì nó là bản ghi của đề tài đã tạm dừng.
- Soạn [bioinformatics-proposal-notion.md](../meeting/bioinformatics-proposal-notion.md): bản nguồn Markdown trình bày đề xuất chính và dự phòng, để dán vào trang tổng luận văn trên Notion.

**Quyết định**
- Slide dùng Source Serif 4 + IBM Plex Sans, bảng màu xanh mòng két và cam đất. Deck mới là artifact riêng, không ghi đè artifact của đề tài chi tiêu.
- Nội dung slide theo **bản prep đã được sửa**: phần ngưỡng nêu kèm giới hạn ("chưa kết luận đây là phiên bản tạo số liệu bài báo"), và RQ2 nói rõ đổi riêng ngưỡng chỉ làm đổi MCC/F1.

**Notion** (sau khi server được bật trong phiên)
- Đã tạo trang con [Đề xuất chốt: vị trí gắn ATP + dự phòng efflux](https://app.notion.com/p/3ec486d98ebc813bb56eface997a23a9) dưới trang **Ý tưởng luận văn**. Đã kiểm tra lại: callout, ba bảng và mention trang cũ render đúng.
- Phát hiện resources.md ghi sai: bản ba ý tưởng **đã** được nhập Notion từ trước. Đã sửa, và thêm bảng đối chiếu trang Notion với bản nguồn trong repo.

**Còn dở**
- Điền tên và MSSV vào slide bìa (đang là `[Họ tên sinh viên]` / `[MSSV]`).
- Số tuần thực tế vẫn chưa có; slide kế hoạch đang ghi theo phần trăm thời gian.
- Chưa tự xem lại deck trên trang — nếu có chỗ tràn hoặc xuống dòng xấu thì nói để sửa.

## 01/10/2026 (tối) — chốt đề xuất chính cho buổi gặp, soạn lại prep

**Đã làm**
- Đánh giá đối chiếu [trang so sánh ba hướng](../meeting/bioinformatics-topic-ideas-notion.md) với [bản khảo sát sâu](deep-research/reports/bioinformatics-topic-survey.md). Kết luận: ba hướng trong trang Notion thật ra dùng chung **một** RQ áp lên ba bộ dữ liệu, nên việc cần quyết không phải chọn bài toán mà chọn nơi đặt đóng góp.
- Soạn lại [session-01-prep.md](../meeting/session-01-prep.md) hoàn toàn theo hướng tin sinh (bản cũ soạn cho đề tài chi tiêu).

**Quyết định**
- **Đề xuất chính:** ATP ở RTK + giao thức đánh giá chống rò rỉ + quy tắc từ chối dự đoán theo identity láng giềng (RQ3 là phần mới và cũng sinh ra sản phẩm). **Dự phòng:** efflux (Đề xuất 2 của bản khảo sát), mở ra bằng đúng một câu hỏi về bộ GenEfflux.
- **Bỏ hướng IL-6**: dữ liệu công khai không có test độc lập và CONTRA-IL6 (2026) đã làm kiểm tra độc lập.
- Chuyển RQ của Đề xuất 1 (DNA/RNA) sang bộ ATP: giữ phần giá trị về phương pháp, bỏ rủi ro quan hệ, vì RTK_RAG truy hồi ở mức chuỗi và không dùng nhãn (mục 3.2 của khảo sát).
- **Không nêu** phát hiện mục 3.1 trong buổi gặp đầu. Lập luận của RQ2 chỉ dựa vào ba điểm tự kiểm chứng được: ngưỡng G-mean chọn trên tập đang đánh giá, AUC sát trần trên dữ liệu ≈0,96% dương, CD-HIT 40% so với chuẩn 25–30%.
- Học phần **bắt buộc có sản phẩm hệ thống** (người làm đề tài xác nhận) — đã đưa vào phạm vi và lịch.

**Còn dở**
- Checklist trước buổi gặp trong prep: tự xác nhận chỗ chọn ngưỡng trong notebook RTK_RAG, xem quota Kaggle, thử tải ATP-388/41/17.
- **Số tuần thực tế chưa biết** — lịch trong prep đang để theo phần trăm, phải quy đổi sau khi hỏi thầy.
- Chưa đọc hết bằng chứng mục 3.1 của bản khảo sát.
- Slide cho buổi gặp chưa soạn (artifact hiện tại vẫn là bản đề tài chi tiêu).
- Sau buổi gặp: đặt slug, tạo `docs/topics/<slug>/01-idea/`, chuyển báo cáo liên quan sang `02-survey/`.

## 01/10/2026 — trang so sánh đề tài tin sinh

**Đã làm**
- Soạn [trang so sánh ba hướng tin sinh để nhập Notion](../meeting/bioinformatics-topic-ideas-notion.md): vị trí gắn ATP ở RTK, peptide kích thích IL-6, và họ protein efflux.
- Đối chiếu mô tả với README/bài báo công khai; đánh dấu dữ kiện đã xác minh, đề xuất, điểm cần hỏi; thêm câu hỏi nghiên cứu, luồng sản phẩm demo, đánh giá, rủi ro và lịch dự kiến 14 tuần cho mỗi hướng.
- Cập nhật [danh sách đề tài](../topics/README.md) và [resources](resources.md) để dùng trang mới làm điểm vào hướng tin sinh.

**Quyết định / giả định**
- Chưa chọn đề tài. Ưu tiên mang ATP và IL-6 ra trao đổi trước; efflux phụ thuộc việc GVHD xác nhận dữ liệu hiếm và bộ GenEfflux.
- Trang Notion chưa được tạo/cập nhật; giữ Markdown trong repo làm bản chuẩn bị để nhập.

**Còn dở**
- Hỏi GVHD về dataset, weights, phép chia độc lập, quyền dùng dữ liệu và quota GPU.
- Sau khi trao đổi, chọn hướng rồi soạn lại buổi gặp/slide theo đề tài tin sinh.

## 01/10/2026 — hướng tin sinh học

**Đã làm**
- Khảo sát sâu hướng tin sinh theo chuyên môn nhóm thầy Ho–Ou: [bioinformatics-topic-survey.md](deep-research/reports/bioinformatics-topic-survey.md), cùng 4 bộ ghi chú trong `deep-research/research_notes/`. Kết quả: 4 đề xuất xếp hạng, 10 điểm chưa kiểm chứng (mục 6 của báo cáo).
- Tự kiểm chứng mục 3.1 (RAG-msCNN) trực tiếp từ GitHub và bản PDF bài báo: dòng 1–7 khớp, dòng 8 khớp một phần. Có thêm 2 điểm mới. Xem [rag-mscnn-verification.md](deep-research/reports/rag-mscnn-verification.md).
- Cập nhật CLAUDE.md (repo private, sơ đồ có thêm `deep-research/`, bỏ `brainstorming-guide.md`), [topics/README.md](../topics/README.md) và [resources.md](resources.md).

**Quyết định**
- Repo GitHub chuyển sang **private**. Giữ nguyên `deep-research/` và tài liệu GVHD trong repo, không thêm vào `.gitignore`.
- **Tạm dừng** đề tài quản lý chi tiêu cá nhân. Hướng chính bây giờ là tin sinh, chưa chọn đề xuất nào.

**Còn dở**
- Người làm đề tài tự đọc lại các link trong file kiểm chứng.
- Chọn một trong 4 đề xuất. Claude khuyên không lấy Đề xuất 1 làm trục chính, mà đưa giao thức đánh giá chặt vào làm phần phương pháp của Đề xuất 2 hoặc 3.
- Soạn lại [session-01-prep.md](../meeting/session-01-prep.md) và slide theo hướng tin sinh. Bản hiện tại soạn cho đề tài chi tiêu.
- Kiểm tra lại mấy điểm trong báo cáo: "nền sinh học cơ bản" có đúng với người làm đề tài không; số chuỗi efflux (2394/18 hay 1670/15); quota Kaggle.

## 29/09/2026

**Đã làm**
- Báo cáo trạng thái brainstorm; phản biện 7 điểm thiếu sót của đề tài.
- Bổ sung dòng mẫu ẩn danh và câu hỏi cho GVHD trong [session-01-prep.md](../meeting/session-01-prep.md). Làm slide 8 trang ([resources.md](resources.md)).
- Thí nghiệm thô [rq1-quick-check](../../ml/personal-expense-management/experiments/rq1-quick-check/README.md): embedding zero-shot trên dev đạt 50,1% với tên + mô tả, 17,9% nếu chỉ có tên.
- Thí nghiệm thô [rq2-baseline-recall](../../ml/personal-expense-management/experiments/rq2-baseline-recall/README.md): B1 đạt 71,5%, riêng ghi chú chưa gặp chỉ 37,0%; bản thô của TN5.
- Khảo sát tài liệu, đối chiếu 18 khẳng định với bằng chứng: [literature-survey.md](../topics/personal-expense-management/02-survey/literature-survey.md).
- Đề cương bản nháp 1 bằng LaTeX: [proposal.tex](../topics/personal-expense-management/04-proposal/proposal.tex).
- Tạo cơ chế lưu thông tin giữa các phiên: file này và [resources.md](resources.md).

**Quyết định** (chi tiết ở [brainstorm.md](../topics/personal-expense-management/01-idea/brainstorm.md), mục 0.2)
- B0/B1 (nhớ lại) là mốc bắt buộc. RQ2 đo mức cải thiện so với B1 trên ghi chú chưa gặp.
- RQ3 mở rộng thành dự báo khoảng và lan truyền lỗi phân loại (phương án 1 + 3).
- Thêm biến thể đặc trưng ngữ cảnh (+ctx). Chốt TN5 về phản hồi thiếu.
- Tìm tình nguyện viên sau buổi gặp GVHD, nếu đề tài được chốt.

**Còn dở**
- Người làm đề tài tự viết lại mô tả 25 danh mục. Bản hiện tại là nháp của Claude, có nguy cơ rò rỉ.
- Điền thông tin cá nhân và kiểm tra tên đơn vị trên trang bìa đề cương.
- Tìm lại tài liệu trên Google Scholar; tự đọc toàn văn các bài chính; đối chiếu `references.bib`.
- Soạn và phát khảo sát người dùng.
- Buổi gặp GVHD lần 1: chưa diễn ra. Sau buổi gặp: viết `session-01-minutes.md`.

## 27/09/2026
- Đổi trọng tâm: dữ liệu cá nhân chỉ dùng để đánh giá bằng phát lại; mô hình ban đầu dùng LLM zero-shot và dữ liệu tổng hợp; đa tiền tệ hạ xuống tính năng phụ. Làm bản tóm tắt 2 trang ([topic-summary.pdf](../topics/personal-expense-management/01-idea/topic-summary.pdf)).

## 24/09/2026
- Khởi tạo repo; báo cáo dữ liệu ([data-report.md](../topics/personal-expense-management/03-data/data-report.md)) và script làm sạch, ẩn danh.
