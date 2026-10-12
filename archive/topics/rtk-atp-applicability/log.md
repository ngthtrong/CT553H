# Nhật ký đề tài `rtk-atp-applicability`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

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
- **Tạo deck thứ hai — slide diễn giải 13 trang:** https://claude.ai/artifact/A7kgUgsr28RBUSd59knh1q, mã nguồn [explainer-slides/](04-proposal/explainer-slides/). Bố cục do người dùng chỉ định: mô tả bài toán (2 trang) → tính cấp thiết / nghiên cứu đã có / vì sao cần làm (4 trang) → input → output → dữ liệu (2 trang) → cách đánh giá (2 trang). Ba hình minh họa: biểu đồ cột điểm ATP theo 20 residue của P34891, sơ đồ RTK–màng–túi ATP (SVG, nhãn đặt bằng HTML để dùng đúng font), đường đánh đổi coverage–risk. Bảng `prior-work` liệt kê 10 công trình 2018–2026 kèm tạp chí và số trang. Sau đó thêm **phần 7** theo yêu cầu: trang `risks` (4 rủi ro × dấu hiệu nhận biết × cổng dừng, cộng 2 giới hạn không khắc phục được và rủi ro định vị) và trang `questions` (7 câu xin ý kiến GVHD, chia hai nhóm phạm vi/đóng góp và dữ liệu/phương pháp) — deck thành **15 trang, 6 section**.
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

---

## 02/10/2026 — chốt đề tài RTK–ATP, viết lại thuyết minh, Notion và slide (`rtk-atp-applicability`)

**Đã làm**
- **Chốt đề tài** (quyết định của sinh viên, chưa có phê duyệt GVHD): *Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu.* Slug: `rtk-atp-applicability`.
- Viết [thuyết minh chi tiết 14 mục](04-proposal/topic-proposal.md): phạm vi mức residue và danh sách "không làm", mô hình nền RTK_RAG, bốn loại rò rỉ, giao thức 9 bước + hai kịch bản, hai RQ, chỉ số, dữ liệu, sản phẩm, ba đóng góp, kế hoạch 14 tuần, sáu câu hỏi GVHD, điều chưa có.
- Viết [dàn ý và kịch bản trình bày](../../../project/meetings/2026-10-02-session-01/slide-outline.md): mạch 13 slide, sáu câu hỏi dễ gặp kèm câu trả lời, checklist trước buổi.
- **Viết lại artifact slide** thành 13 trang cho đề tài đã chốt (bản 4): https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT. Bỏ 5 slide cũ (`framing`, `gap`, `proposal`, `backup`, `research-questions`), thêm 7 slide mới (`scope`, `pipeline`, `data`, `leakage`, `protocol`, `rq1`, `rq2`, `metrics`, `contributions`).
- **Tạo trang Notion mới** dưới *Ý tưởng luận văn*: [Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880). Đã kiểm lại render: callout, 11 bảng và sơ đồ mermaid đúng.
- Chạy lại `archive/topics/rtk-atp-applicability/code/preprocessing/prepare_data.py` để xác nhận dữ liệu tái tạo được: exit 0, `validation_errors` rỗng, số liệu khớp [báo cáo dữ liệu](03-data/data-report.md).
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
- Sau buổi gặp: ghi `project/meetings/2026-10-02-session-01/minutes.md` với câu trả lời của GVHD cho sáu câu hỏi.
- `05-design/` và `06-experiments/` chưa tạo; chưa có `backend/`, `frontend/`, `ml-service/`, `thesis/`.

---

## 01/10/2026 — kiểm chứng G-mean trong notebook RTK_RAG

- Tải và đọc trực tiếp notebook tại commit `b7bd4c2347c7d44d24ae3d13e42082ba6cd62627`; xác nhận `model_test` chọn ngưỡng G-mean từ nhãn của tập đang đánh giá rồi tính MCC/F1 trên cùng tập.
- Lưu [bằng chứng và liên kết cố định](research/rtk-rag-threshold-verification.md): vị trí ô/dòng, lời gọi cross/independent, output lưu sẵn, thiếu module nạp dữ liệu và lỗi số giá trị trả về. Chưa chạy lại mô hình hoặc xác nhận phiên bản tạo kết quả bài báo.
- Cập nhật checklist và RQ2 trong [prep](../../../project/meetings/2026-10-02-session-01/prep.md): đổi ngưỡng đơn thuần không làm thay đổi AUPRC/AUROC; xáo nhãn kho không tác động tới phép trộn embedding không dùng nhãn.
- Còn lại: người trình bày tự mở đoạn mã được dẫn; hỏi GVHD về phiên bản đánh giá dùng trong bài và nguồn chọn ngưỡng.
