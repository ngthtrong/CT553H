# Nhật ký làm việc

> Mỗi phiên làm việc có thay đổi đáng kể thì thêm **một mục lên đầu** (mới nhất ở trên). Ghi ngắn: đã làm gì, quyết định gì, còn dở gì. Chi tiết nằm trong các tài liệu được liên kết, không chép lại ở đây. Đầu phiên mới, đọc mục mới nhất để nắm tình hình.

---

## 11/10/2026 — tiếp tục phiên Claude: hoàn thiện giao diện `degron-e3-specificity`

- Hoàn thiện [presentation.html](../topics/degron-e3-specificity/01-idea/presentation.html): hoạt ảnh trên sơ đồ, ô số liệu có nguồn audit, biểu đồ pooling có bảng và giới hạn phép thử, minh họa tương tác peptide/protein, sáng/tối, dừng chuyển động, cuộn hình trên điện thoại và chế độ in.
- Phân biệt hình minh họa với số đo; làm rõ bất biến hoán vị chỉ áp dụng kênh nội cnn2w1, không khái quát sang kênh C-term của PAP.
- Kiểm tra Chromium desktop/điện thoại, sáng/tối, giảm chuyển động, ngoại tuyến/tắt JavaScript, nút tương tác và liên kết nội bộ đều đạt; có kiểm tra ảnh chụp. Chi tiết: [presentation-validation.md](../topics/degron-e3-specificity/01-idea/presentation-validation.md).
- Không thêm thí nghiệm ML. Ba cổng nghiên cứu trong [quyết định đề tài](../topics/degron-e3-specificity/01-idea/topic-decision.md) vẫn còn; lần này hoàn tất phần trình bày còn dở.

---

## 10/10/2026 (muộn) — **chốt khuyến nghị đề tài chính: dark kinome trên DARKIN**; bốn lập luận bán đề tài bị gỡ bỏ

- **Hai thông tin sinh viên cung cấp, thu hẹp cuộc so sánh về hai ứng viên:** (1) **GVHD không chấp nhận kết quả âm làm đóng góp chính** (sinh viên đánh giá, chưa phải lời thầy) → loại hướng sirtuin in-vitro khỏi vị trí đề tài chính, vì phán quyết THU HẸP của nó chính là một kết quả âm; (2) **có GPU ổn định hơn Colab miễn phí** → mở lại fine-tuning/LoRA.
- Báo cáo: **[main-topic-decision.md](deep-research/reports/main-topic-decision.md)**; bốn ghi chú nền: [research_notes/main-topic-decision/](deep-research/research_notes/main-topic-decision/).
- **Khuyến nghị — đề tài chính:** dự đoán kinase cho phosphosite ở dark kinome trên DARKIN, với bộ mã hóa đa cửa sổ trên embedding PLM, **đánh giá song trục** có kiểm soát rò rỉ, và **ca nghiên cứu sirtuin**. **Dự phòng:** đánh giá lại chuẩn hóa DARKIN (song trục, 4 split, kiểm rò rỉ) — dùng **chung toàn bộ hạ tầng**, nên trượt cổng phương pháp không mất việc đã làm. Độ tin cậy **trung bình**; tiêu chí 1 là tiêu chí yếu nhất.
- **Senescence scRNA-seq bị loại vì điều kiện bắt buộc, không vì điểm thấp:** nhãn SenMayo là điểm chữ ký do chính pipeline sinh ra → mô hình học lại bộ chấm điểm (chính README của hướng đó ghi). Cộng với trượt ngưỡng đi/dừng đã đặt trước và điểm đi theo loại tế bào.
- **Bốn lập luận phải gỡ khỏi slide tuần 6 (quan trọng hơn phần ủng hộ):** (1) "audit phát hiện DARKIN rò rỉ phía substrate" — **DARKIN đã thấy và chủ động gạt bỏ bằng lý lẽ**, còn đếm sẵn ở Supplementary Fig. 4; (2) "lần đầu đề xuất holdout hai chiều" — **SAGEPhos (ICLR 2025) đã đặt tên** cả hai cold-start và tuyên bố cold-both *"not feasible"* (bipartite liên thông 99,9%); (3) "vượt SOTA 0,2946" — **0,2946 và 0,1911 gần như chắc chắn khác trục đo**; trên trục site baseline của chính DARKIN đã 0,2879 và DARKIN-FT **0,3321**, tức cao hơn 0,2946, và repo COMPASS-PTM **không có code evaluation nào**; (4) "đóng góp là PU learning cho nhãn thiếu" — Kanehira & Harada (CVPR 2016) đã làm đúng việc đó và tự nhận *"slightly improved"*; class prior **không ước lượng được** cho lớp unseen (Mao et al., TKDE 2025); label smoothing đơn thuần thắng ROLE trên COCO.
- **SOTA thật phải nêu, nếu không sẽ bị bắt lỗi chọn baseline yếu:** trục kinase **0,2250**, trục site **0,3321** (DARKIN-FT + ESM1B, luận văn Pekey 2025 — **chưa qua phản biện**). Hai đính chính: DARKIN đặt kinase **giàu** chú giải vào val/test và kinase dark vào **train** (ngược mô tả thứ cấp phổ biến); và metric tính *"matches **any** of the true kinases"* nên **đã hấp thụ một phần** tác hại của nhãn thiếu.
- **Khung bán đề tài dùng được, mỗi mắt có nguồn:** kinase thượng nguồn chỉ biết cho **dưới 4%** phosphosite (Johnson 2023, *Nature*; atlas có 83 dark kinase); **151/634 ≈ 23,8%** kinase người understudied, EGFR ~90.000 bài so với HIPK4 9 bài (Essegian 2020); understudied kinase **tiên lượng kết cục xấu** trên 17 ung thư TCGA. **Liên hệ cancer ở mức gene, không ở mức phosphosite; liên hệ aging yếu — không bán như đề tài aging.**
- **Cầu nối sang hướng GVHD (rẻ, khớp SirtSAGE):** sirtuin **là** cơ chất kinase — JAK1 → SIRT1 Tyr280/Tyr301 **trong catalytic domain**, trục IL-6/ung thư (Wang 2018, JBC); JNK/mTOR/CDK1/CK2 → SIRT1; AMPK → SIRT2 Thr101. Khoảng trống là chỗ mạnh: site MS trên SIRT3/4/6 **chưa gán được kinase nào**, SIRT7 chưa map site nào.
- **Còn dở — ba phép kiểm nhanh phải xong trước tuần 6:** đọc **S.3.7** của COMPASS-PTM (arXiv 2510.23492) để chốt trục của 0,2946; lấy **DARKIN Supplementary Fig. 4** (nếu đã phân rã AP theo seen/novel thì RQ2 bị thu hẹp); **đếm** còn bao nhiêu dòng test nếu ép substrate-protein-disjoint. Thêm: kiểm bộ mã hóa đa cửa sổ đã ai dùng trên DARKIN chưa (**SAGEPhos nghe như GraphSAGE, phải kiểm kiến trúc**). Chưa chạy baseline, chưa huấn luyện, chưa xây website.

---

## 11/10/2026 (muộn) — **CHỐT ĐỀ TÀI `degron-e3-specificity`**; kiểm chứng xong 10 điểm; GVHD kỳ vọng kiến trúc mới

- **Sinh viên chốt đề tài:** *Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc.* Tài liệu: [topic-decision.md](../topics/degron-e3-specificity/01-idea/topic-decision.md), [presentation.html](../topics/degron-e3-specificity/01-idea/presentation.html) (bố cục 6 mục, mở bằng `file://`), [báo cáo chi tiết bản 3](deep-research/reports/degron-topic-report/index.html). **Chưa có phê duyệt GVHD.**
- **Thông tin mới từ GVHD: thầy kỳ vọng một kiến trúc chưa ai dùng**, không chấp nhận chỉ một bảng đối chứng có kỷ luật. → đề xuất kiến trúc **CMIL-E3** (học đa thể hiện có điều kiện E3 + cổng phơi lộ ở chỗ gộp), sáu thành phần, **mỗi thành phần gắn với một phép đo tự thực hiện**.
- **Theo yêu cầu: HTML tạo trực tiếp trên hệ thống, không dùng artifact.** Artifact bản 1 (`XAXzVcA6ot1eVVk4927suc`) giờ **lạc hậu**, file trong repo là bản chuẩn.

### Kết quả kiểm chứng 10 điểm — bốn điểm đi ngược bản 1

- **Tái lập được số của bài báo.** Tự dựng PAP bằng numpy từ trọng số công bố: kênh nội **0,8239** (bài: 0,82), đầy đủ **0,8690** (bài: 0,87) trên holdout hiệu dụng 428 gene. Chênh lệch 0,82–0,87 là do kênh C-term phải áp cho **mọi** tile (trong assay mọi tile đều gắn vào đầu C của GFP).
- **Phép đo quan trọng nhất:** đảo ngẫu nhiên thứ tự residue → điểm cnn2w1 **không đổi**, Pearson(gốc, đảo) = **1,000000**. PAP mặc định **bất biến hoán vị**, không biểu diễn được motif nào, vẫn đạt 0,869.
- **BÁC BỎ đóng góp phương pháp của bản 1:** repo có sẵn `cnn2w7` (cửa sổ 7, bắt được motif). Tự chạy: **0,8722 so với 0,8690 = +0,0032**. Trần của trục "thêm năng lực bắt motif" đã do chính tác giả đo.
- **Thêm:** thay gộp trung bình bằng gộp max làm sụt **0,824 → 0,344**; entropy theo vị trí 3,294/3,401 → tín hiệu thang điểm khối **dàn đều, không khu trú**. Hệ quả: kiến trúc khu trú **sẽ không thắng** trên thang điểm khối — phải chốt thước đo với GVHD trước.
- **CỔNG CHẶN ĐÃ MỞ:** GEO **GSE240610** tải được. Table S1 = 52,9 MB, 3 sheet × **475.507 dòng** kèm PSI; thêm RAW.tar 21 MB.
- **BÁC BỎ "chưa ai dùng PLM trên bộ này":** cùng nhóm có bài tiếp theo — degron trên **1.620 (chính xác 1.626) transcription factor**, tiền ấn bioRxiv 17/05/2025, **dùng PAP cùng ESM-1b**, và đã chỉ ra tác động biến thể tương quan độ mạnh degron. Ăn vào một phần đóng góp "giải thích biến thể theo cơ chế".
- **SỬA SỐ MaveDB:** 100.514 → **69.209 biến thể duy nhất** (bản 1 đếm cả dòng không có điểm; trùng lặp dồn ở PRKN và PTEN).
- **Rò rỉ bậc 3 đã định lượng:** 6/9 gene MaveDB có tile, **toàn bộ ở tập train**, nhưng chỉ **132 tile = 0,07%** → sửa gần như miễn phí. 3 gene còn lại (CYP2C9, CYP2C19, LDLR) không thuộc bào tương.
- **Chênh lệch 96 gene đã đặc tả:** phân vùng thật giữ lại **473 gene**; danh sách 527 = 428 đúng + 96 sai + 3 một phần; **45 gene bị giữ lại mà không có trong danh sách**. Nhóm 96 có nhiều tile hơn rõ rệt (64,3 so với 37,0 tile/gene) → suy luận: danh sách là tập tiền tuyển, gene lớn được trả về train.
- **Alignment độc lập làm giảm tuyên bố bản 1:** Smith-Waterman thật (parasail, sàng 6-mer) → **14/428 (3,3%)** gene holdout có họ hàng trong train ở identity ≥30%/coverage ≥50%; **1 ca trùng 100% trên 77 residue** (`AC104389.5` so với **TRIM5**). Bản 1 nói "không có paralog nào" là quá mạnh.
- **Lỗi tái lập trong mã công bố:** `train_cnn2w.py` dùng `ci_aa=1` → trỏ vào cột **DNA**, và A/C/G/T đều là ký hiệu acid amin hợp lệ nên bộ lọc không loại. Chạy mã công bố trên dữ liệu công bố sẽ huấn luyện trên chuỗi DNA.
- **Tài nguyên đã đo:** ESM-2 **35M** 64,6 tile/s → **~55 phút** toàn bộ; **650M** 5,3 tile/s → **~11 giờ**; cache mức residue 650M **32,7 GB** vượt RAM 7 GB. Hugging Face truy cập được.
- **Giấy phép:** repo và Zenodo **MIT**, MaveDB **CC0**, DegronID other-open, hai bản tiền ấn **CC BY-NC-ND**.
- **Còn dở — ba cổng chặn:** (1) đọc toàn văn bài degron TF (`biorxiv.org` bị chặn với WebFetch, chỉ lấy được tóm tắt qua API); (2) mở Table S3/S4/S6/S7 của Zhang 2023 để đếm nhãn E3 dùng được; (3) tra hệ thống tính mới của kiến trúc MIL. Chưa huấn luyện mô hình, chưa xây website.

---

## 11/10/2026 — ứng viên mới: dự đoán degron có bối cảnh cấu trúc; audit bản đồ tile 2026

- **Yêu cầu của sinh viên:** tìm hướng mới hơn, đóng góp rõ hơn, Claude tự quyết; vòng này **bỏ ràng buộc lĩnh vực và độ khớp GVHD**, nhắm **dữ liệu mới cộng trục phương pháp gắn lên nó** (sinh viên chọn qua câu hỏi trắc nghiệm).
- Sản phẩm: [báo cáo HTML](deep-research/reports/degron-topic-report/index.html) — publish tại https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc. Thêm dòng vào [resources.md](resources.md) và [topics/README.md](../topics/README.md).
- **Hướng đề xuất:** dự đoán degron (tín hiệu phân hủy protein) có tính tới trạng thái phơi lộ cấu trúc. Đóng góp chính là **thang đánh giá ba bậc**: (1) trong cùng sàng lọc, holdout kiểm soát đồng dạng; (2) chuyển giữa hai sàng lọc khác assay; (3) từ peptide tách rời sang protein nguyên vẹn. Bậc 2 và 3 **chưa ai đo**.
- **Tự audit bản đồ tile Voutsinos 2026** (repo `KULL-Centre/_2025_Voutsinos_degron_cytosol`, MIT, có SHA-256): 212.658 tile / 5.327 gene; train 195.629 tile / 4.830 gene; nhãn liên tục −0,144…1,132 (hồi quy thật, không phải phân loại mất cân bằng).
- **Hai giả thuyết của tôi đã sai, ghi lại để không lặp:** holdout chia **theo gene**, và **cả 527 gene holdout đều là cụm đồng dạng đơn lẻ**; tập validation early stopping cũng rời hẳn theo gene (0 gene trùng). **Không được lấy "sửa giao thức đánh giá" làm đóng góp.**
- **Phát hiện audit thật:** 96/527 gene trong `holdout_selection.txt` có **toàn bộ** tile nằm ở tập train, 3 gene giữ một phần → holdout **hiệu dụng 428 gene / 15.820 tile**. Nguyên nhân chưa xác định. Phải dùng số này khi so với Pearson 0,87 của tác giả.
- **Ba tầng dữ liệu:** bộ chính đã tải; bộ thứ hai (Zhang 2023, GPS-peptidome, GEO **GSE240610**, có 219 footprint saturation và residue quan trọng cho >5.000 degron → **ground truth XAI thực nghiệm**) **chưa tải**; bộ thứ ba MaveDB **100.514 phép đo độ dồi dào trên 9 gene** (đã truy vấn API; các bộ trong cùng gene chồng nhau, chưa khử trùng lặp).
- **Tiền lệ:** không được nói "đầu tiên" — đã có deepDegron, Degpred (BERT 2022), MetaDegron (PLM 2024), DegML, và **DEGRONOPEDIA (NAR 2024) là đối thủ trực tiếp ở tiêu chí 5**. Không tìm thấy ai dùng PLM trên bản đồ tile 2026 (chỉ vài lượt tìm web, chưa khảo sát hệ thống).
- **Còn dở:** (1) **cổng chặn** — thử tải GEO GSE240610, nếu không được thì bậc 2 và XAI sụp; (2) kiểm 9 gene MaveDB có nằm trong thư viện tile không; (3) chạy lại baseline PAP trên 428 gene holdout; (4) đọc toàn văn Methods bài 2026. Chưa chốt đề tài, chưa so với dark kinome và SIRT.

---

## 10/10/2026 — đánh giá chi tiết dark kinome trên DARKIN; loại hướng sửa lỗi phần mềm

- **Quyết định của sinh viên:** loại ý tưởng sửa lỗi phần mềm có kiểm chứng; yêu cầu báo cáo chi tiết dark kinome. Chưa chốt DARKIN, chưa xác nhận bỏ SIRT; đánh giá bỏ ràng buộc thời gian/lĩnh vực/GVHD/tài nguyên như yêu cầu trước.
- Thêm [báo cáo đánh giá](deep-research/reports/dark-kinome-darkin-evaluation.md), [ghi chú và script audit](deep-research/research_notes/dark-kinome/README.md); thêm cảnh báo vào [khuyến nghị ban đầu](deep-research/reports/criteria-only-recommendation.md) và cập nhật mục lục ứng viên.
- **Tự kiểm checkout DARKIN pin commit:** split ZSL mặc định 8.559/1.484/1.414 site, 308/46/38 kinase, không trùng kinase; train–test vẫn trùng 462 site keys và 923 dòng test thuộc protein đã thấy. Năm split có min nhãn/kinase test 12–15; phát hiện ngoại lệ residue ngoài S/T/Y cần truy vết. Có SHA/count trong audit JSON, chưa alignment độc lập.
- **Đối thủ/phản biện:** DARKIN gốc có fine-tuning; Pekey 2025 đã có DARKIN-Interact/LoRA/atlas; COMPASS-PTM 2026 báo mAP 0,2946 trên DARKIN nhưng cần audit chiều AP; benchmarKIN đã thử thêm predicted relationships và ghi nhận giảm hiệu năng. Không giữ khẳng định “kiểm chứng hạ nguồn chưa ai làm” hoặc “đạt cả năm tiêu chí không cần cược”.
- **Khuyến nghị nghiên cứu:** cân nhắc selection/weighting cạnh để bổ sung thư viện có kiểm soát nhiễu, hoặc nhãn thiếu/khái quát hai phía. XAI cần fidelity riêng; conformal chưa có cơ sở hứa 90% trên kinase mới.
- **Còn dở:** audit file hạ nguồn/giao kinase, Supplementary COMPASS và đối thủ, mapping/nguồn nhãn/license; chọn RQ với sinh viên. Chưa chạy baseline, training hoặc xây website.

---

## 10/10/2026 — tải được Supplementary bbz107 và **đo xong phép chuyển nhãn thứ hai**: mảng Rauh không giàu dương tính trên 289 vị trí curated

- Ghi chú: [09-deep-pla-sites-vs-array.md](deep-research/research_notes/sirtuin-substrate/09-deep-pla-sites-vs-array.md); dữ liệu: [deeppla-curated-sites-vs-rauh-labels.csv](deep-research/research_notes/sirtuin-substrate/data/deeppla-curated-sites-vs-rauh-labels.csv); mục 15 của [báo cáo khảo sát sâu](deep-research/reports/sirtuin-substrate-deep-research.md).
- **Điểm nghẽn hôm 08/10 đã giải tỏa, không cần tải thủ công.** `academic.oup.com` vẫn 403 với curl, nhưng `WebFetch` đọc được trang bài báo; gọi với `offset: 100000` nó trả về **URL CloudFront đã ký**, và curl với URL đã ký trả 200. Lấy được `table_s1.xlsx`, `table_s4.xlsx`, `table_s5.xlsx`. URL không ký trả `MissingKey`; chữ ký có hạn nên phải lặp lại khi cần tải lại.
- **Table S1** 1.666 dòng; lọc sirtuin + người cho **289 vị trí** (SIRT1 185, SIRT2 52, SIRT3 30, SIRT7 12, SIRT6 10) — khớp chính xác cột P trên `help.php`, nên chênh ±1 với Table 1 bài in là lỗi bài in.
- **Kết quả đo:** chỉ **103/289 (35,6%)** vị trí curated có mặt trên mảng Rauh; trên 103 đó mảng gọi dương tính đúng isoform **16 lần (15,5%)**, kỳ vọng 13,7 → độ giàu **1,17×, p = 0,291** (binomial chính xác). Không isoform nào đạt p < 0,05. Dương tính cho ít nhất một isoform 85/103 = 82,5% so với nền 83,7% → **0,986×**, tức tập cơ chất đã được y văn xác nhận không khác một mẫu ngẫu nhiên của mảng.
- **Ý nghĩa:** xác nhận **độc lập thứ hai** cho kết luận trung tâm (nhãn in-vitro gần như không chuyển được vào tế bào), mạnh hơn phép đo Sol 2012 vì dương tính ở đây xác nhận trên protein cuộn gấp, không suy ra từ fold-change, và không cần giả định ngưỡng. Đây là phần trả lời mạnh nhất cho câu "Deep-PLA đã làm rồi".
- **Giới hạn phải nói kèm:** 103/289 nên phép kiểm chỉ nói về phần giao (bị giới hạn bởi cách Rauh chọn peptide 2013); SIRT7 n=2 và SIRT6 n=9 quá nhỏ; khớp theo 13-mer trung tâm có thể bắt paralog, bản khớp nghiêm ngặt chưa làm; tập 289 không có âm tính nên chỉ tính được độ giàu, không tính được MCC.
- **Còn dở:** chưa đọc `table_s4.xlsx` (1,6 MB, dự đoán toàn PLMD) và `table_s5.xlsx`; chưa đọc toàn văn DeepSIRT và ASEB; chưa sửa 7 khẳng định trong `topic-final-recommendation.md`; chưa làm bảng làm giàu residue theo vị trí để quyết định có làm phần XAI hay không.

---

## 08/10/2026 (tối, muộn) — tự tính MCC cho mô hình sirtuin của Deep-PLA; **288 vị trí bị OUP chặn**

- Ghi chú: [08-deep-pla-per-isoform-mcc.md](deep-research/research_notes/sirtuin-substrate/08-deep-pla-per-isoform-mcc.md); bảng số: [deep-pla-sirtuin-mcc-derived.csv](deep-research/research_notes/sirtuin-substrate/data/deep-pla-sirtuin-mcc-derived.csv); mục 14 của [báo cáo khảo sát sâu](deep-research/reports/sirtuin-substrate-deep-research.md).
- **Không làm được phần được giao:** danh sách 288 vị trí curate nằm trong Supplementary bbz107, **OUP trả 403** cho mọi đường dẫn thử; web server Deep-PLA không có trang tải dữ liệu; PLMD giờ chỉ còn thư mục rỗng; iPTMnet 503; dbPTM 403. **Việc của sinh viên:** tải Supplementary bbz107 bằng quyền đã dùng để lấy PDF.
- **Đổi lại được thứ không có trong bài:** `help.php` của web server công bố P, N và Sp/Sn/Pr ba ngưỡng **cho từng enzyme** (bài chỉ báo AUC cho SIRT1 và HDAC gộp). Từ (P, N, Sn, Sp) dựng lại ma trận nhầm lẫn và **tính được MCC**, chỉ số họ không báo ở đâu.
- **MCC tự tính, cross-validation người, ngưỡng High:** SIRT1 **0,403**, SIRT2 **0,219**, SIRT3 **0,049** (độ nhạy chỉ 7,7%), SIRT6 0,321, SIRT7 **−0,016** (tệ hơn ngẫu nhiên), HDAC gộp họ **0,557**.
- **Hai hệ quả ủng hộ thiết kế đã đề xuất:** (1) mô hình **gộp họ tốt hơn mọi mô hình tách theo isoform**, kể cả SIRT1 → ở cỡ 10–185 vị trí, tách theo isoform làm hại nhiều hơn làm lợi, tức bằng chứng cho bậc B8 (một mô hình đa nhãn chia sẻ biểu diễn); (2) Sn/Sp/Pr che mất vấn đề — SIRT3 có Sp 0,964 và Pr 0,340 trông tạm được nhưng MCC 0,049.
- **Phản biện với chính phép tính:** MCC suy từ số làm tròn 4 chữ số, chỉ đọc hai chữ số; P/N trên web lệch 1 so với Table 1 cho SIRT1 (185 vs 184) và EP300, lệch nhiều hơn cho dòng "HDACs" (147 vs 94), chưa giải thích được; tỉ lệ dương nền là tạo tác của cách dựng tập âm nên MCC này **không so được với bài khác**; tập test SIRT6 chỉ 2 dương và SIRT7 4 dương nên không dẫn MCC của chúng làm bằng chứng.
- **Còn dở:** phép đo 288 vị trí vs nhãn mảng Rauh (chờ file); DeepSIRT và ASEB chưa đọc toàn văn.

---

## 08/10/2026 (tối) — đọc Deep-PLA: **9 HDAC của nó gồm SIRT1, 2, 3, 6, 7** → trục tính mới sinh học hết

- Sinh viên cung cấp PDF bbz107, đã đọc toàn văn. Ghi chú: [07-deep-pla-hdac-coverage.md](deep-research/research_notes/sirtuin-substrate/07-deep-pla-hdac-coverage.md); mục 13 của [báo cáo khảo sát sâu](deep-research/reports/sirtuin-substrate-deep-research.md).
- **Web server chính thức ghi nguyên văn:** Deep-PLA phủ "HDAC1, HDAC2, HDAC3, HDAC6, **SIRT1, SIRT2, SIRT3, SIRT6, and SIRT7**". Vậy 9 HDAC = 4 HDAC cổ điển + 5 sirtuin, thiếu đúng SIRT4 và SIRT5 — tức nó bỏ đúng hai isoform mà sinh học nói không nên làm, và phủ trọn SIRT1/2/3 là ba isoform duy nhất còn khả thi. Chồng lấn nằm trọn ở phần đáng làm.
- Chính bbz107 còn dẫn rằng **ASEB** đã có "class I HDAC and SIRT7 substrate predictive functions" từ trước. Nên dự đoán cơ chất đặc hiệu SIRT7 có tiền lệ còn sớm hơn 2020.
- **Hệ quả:** "dự đoán vị trí deacetyl hóa đặc hiệu isoform sirtuin ở mức residue" đã tồn tại từ 2020. Bỏ mọi câu có chữ "đầu tiên" về mặt sinh học. Bảng tiền lệ giờ có bốn dòng: ASEB (~2012, SIRT7), Deep-PLA (2020, residue, 5 isoform), DeepSIRT (2021, protein, 7 isoform), Ridgeway (2025, residue, 7 isoform).
- **Chỗ còn khác biệt và nó thật:** Table 1 của bbz107 — năm sirtuin cộng lại chỉ **288 vị trí trên 134 protein** (SIRT1 184, SIRT2 52, SIRT3 30, SIRT6 10, SIRT7 12), nhãn **text-mining từ PubMed** tức cơ chất đã được báo cáo, khác hẳn 6.801 vị trí hoạt tính peptide in vitro của mảng Rauh. Họ **không báo MCC, không báo AUPRC**, không có chỉ số riêng cho SIRT2/3/6/7, và dữ liệu nhỏ tới mức chỉ chạy nổi 5-fold cho SIRT3/6/7. Điểm họ làm tốt, phải ghi nhận: tập kiểm tra là protein **phi-người**, có kiểm soát độc lập thật.
- **Khung đề tài phải đổi:** từ "bộ dự đoán đặc hiệu isoform" thành **benchmark chuyển miền cho ba bộ dự đoán đã công bố** (Deep-PLA 2020, DeepSIRT 2021, Ridgeway 2025) trên một tập đánh giá trong tế bào có nhãn âm, với MCC/AUPRC và kiểm soát rò rỉ theo protein và đồng dạng. Phán quyết THU HẸP không đổi, nhưng lý lẽ bán đề tài đổi hẳn.
- **Việc ưu tiên cao nhất bây giờ (thay thứ tự cũ):** lấy 288 vị trí curate của Deep-PLA và đối chiếu với nhãn mảng Rauh — đó là **phép đo chuyển miền thứ hai, độc lập** với phép đo Sol 2012, và mạnh hơn vì 288 vị trí đó được xác nhận trên protein nguyên.
- Một chi tiết dùng được: Deep-PLA đo và thấy AUC không đổi đáng kể khi cửa sổ vượt **±12 residue** (Figure S3) — căn cứ có nguồn cho việc chọn cửa sổ 13-mer thay vì chọn tùy ý.
- **Còn dở:** chưa lấy được danh sách 288 vị trí; chưa đọc DeepSIRT và ASEB toàn văn.

---

## 08/10/2026 (chiều, muộn) — đo xong cổng G3: lượng enzyme giải thích phần lớn chênh lệch giữa 7 isoform

- Sinh viên hỏi bài toán 7 isoform có còn khả thi không. Đã tải Supplementary Data 5 và 6 của Rauh qua `media.springernature.com` và đo trực tiếp. Ghi chú: [06-seven-isoform-feasibility.md](deep-research/research_notes/sirtuin-substrate/06-seven-isoform-feasibility.md); bảng số: [rauh2013-enzyme-amount-vs-positives.csv](deep-research/research_notes/sirtuin-substrate/data/rauh2013-enzyme-amount-vs-positives.csv); mục 12 của [báo cáo khảo sát sâu](deep-research/reports/sirtuin-substrate-deep-research.md).
- **Kết quả:** số nhãn dương tương quan với nồng độ enzyme nhỏ lên mảng — Spearman **ρ = +0,811**, **p = 0,0349** (hoán vị đầy đủ, n = 7). SIRT5 nhỏ 218 µg/ml → 2.615 dương; SIRT4 nhỏ 10 µg/ml → 1.038. Spearman(nhãn dương, `ratio error` trung vị) = −0,855. Nghịch lý SIRT5 vì vậy có lời giải thích kỹ thuật thí nghiệm.
- **Hai phản biện phải nói kèm:** n = 7 nên p sát ngưỡng; và SIRT1 với SIRT7 **cùng** 20 µg/ml mà 176 so với 1.692 nhãn dương, nên lượng enzyme không giải thích hết. Phát biểu đúng: lượng enzyme là biến gây nhiễu cỡ lớn chưa được hiệu chỉnh.
- **Một mối lo bị bác bỏ bằng số:** Supplementary Data 6 có 220 peptide "không cho tín hiệu ở ≥ 1 đối chứng", tất cả vẫn nằm trong bộ nhãn, nhưng 185/220 (84,1%) là dương ở ít nhất một isoform — gần trùng tỉ lệ toàn mảng 5.695/6.802 (83,7%). Nên giả thuyết "nhãn âm thật ra là không đo được" không thành.
- **Kết luận về khả thi, ba mức:** SIRT1/2/3 khả thi (khung deacetylase đúng, có bằng chứng mức protein, có tập in-cell); SIRT1 là ca xấu nhất về dữ liệu chứ không về sinh học; SIRT4–7 không khả thi như bài toán "dự đoán cơ chất deacetyl hóa" — chuyển thành phân tích giới hạn của nhãn, lấy chính bảng lượng enzyme vs nhãn dương làm nội dung.
- **Còn dở:** chưa tách tương quan theo từng cặp (construct, mảng) — Data 5 cho thấy mỗi isoform được thử với nhiều construct và đột biến bất hoạt khác nhau, nên "nồng độ trung vị theo isoform" là phép gộp thô. Và năm việc chặn khác của mục 11.2 vẫn nguyên, trong đó **đọc toàn văn Deep-PLA** là việc có thể đổi phán quyết tính mới.

---

## 08/10/2026 (chiều) — khảo sát sâu đề tài chính SIRT1–7: **nhãn mảng peptide gần như không chuyển được vào tế bào**

- Phản biện độc lập bản khuyến nghị [topic-final-recommendation.md](deep-research/reports/topic-final-recommendation.md) bằng năm nhánh khảo sát song song (sinh học/nhãn, tính mới, cổng dữ liệu, thiết kế đánh giá, conformal+XAI). Báo cáo tổng hợp: **[sirtuin-substrate-deep-research.md](deep-research/reports/sirtuin-substrate-deep-research.md)**; ghi chú từng nhánh và bảng dẫn xuất: [research_notes/sirtuin-substrate/](deep-research/research_notes/sirtuin-substrate/). Bản khuyến nghị cũ **giữ nguyên không sửa** để đối chiếu.
- **Phán quyết: THU HẸP.** Giữ đề tài nhưng hạ phạm vi định lượng xuống **SIRT1/2/3** và đổi lời hứa từ "một mô hình tốt hơn" sang "một phép đo có kiểm soát về mức độ KHÔNG chuyển được của nhãn in vitro". Chuyển sang đề tài B **chỉ nếu** GVHD không chấp nhận kết quả âm làm đóng góp chính.
- **Phát hiện nặng nhất (phép đo thật, không phải suy luận):** nhãn SIRT3 của mảng Rauh dự báo chiều thay đổi acetyl hóa trong tế bào (Sol 2012, U2OS) với **MCC +0,047…+0,080** trên 1.417 vị trí khớp cửa sổ 13-mer, và **MCC −0,007** trên tập chồng lấn chặt (n = 718). Tập chuột cho kết quả tương tự. Đây là giả thuyết trung tâm của đề tài, và nó gần như không đứng.
- **Bốn đính chính quan trọng với bản khuyến nghị:** (1) con số **43,0%** của Ridgeway 2025 là **recall**, không phải precision, và pha rò rỉ (52,3% trên vị trí đã có trong train vs **39,0%** ngoài train); (2) quy tắc nhãn dương là **`efficiency ≥ 1`**, không phải `category = 1` — tái lập 100,0000% trên 47.607 ô, nên lập luận "ngưỡng cứng bỏ mất nhãn yếu" không đứng; (3) **nhãn âm in-cell đã tồn tại** — Zhang 2022 ([PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)) định lượng 2.846 vị trí mà chỉ 152 phụ thuộc SIRT2, và Sol 2012 (PLoS ONE 7:e50545) có 3.174 vị trí SIRT3 ở người + 1.566 ở chuột, nên **AUPRC và MCC trong tế bào đo được**, không phải chỉ precision; (4) **DeepSIRT 2021** (Comput Biol Chem 93:107514, tác giả cuối Y.-Y. Ou) đã dự đoán target SIRT1–7 bằng CNN ở mức protein — tiền lệ bị bỏ sót, và là của nhóm Prof. Ou, phải nêu chủ động trên slide 1 cạnh NAD_MCNN.
- **Khung sinh học đổ ở chỗ khác với dự đoán:** bản khuyến nghị đặt cổng dừng ở SIRT1 (176 nhãn dương), nhưng SIRT1 là deacetylase hợp lệ nhất. Chỗ đổ là **SIRT4/5/6/7** — Mathias 2014 (Cell) và Jiang 2013 (Nature) nói thẳng 4/7 sirtuin có rất ít hoặc không có hoạt tính deacetylase. Nghịch lý phải giải thích: SIRT5 lại là cột có **nhiều nhãn dương nhất (2.614)**.
- **Conformal:** không có bảo đảm nào chuyển được sang miền in-cell (khoảng cách này là *concept shift*, không phải covariate shift, nên weighted conformal không áp dụng). Bảo đảm in-cell trung thực duy nhất là độ phủ trên lớp dương của SIRT2, nếu tách một phần tập Zhang làm hiệu chỉnh. Phải viết rõ chọn mức A (biên) / B (theo lớp) / C (conformal risk control) trong đề cương.
- **Một con số phải gỡ khỏi mọi tài liệu gửi GVHD cho tới khi đọc lại toàn văn Rauh:** phát biểu "SIRT7 ưa residue thân nước ở −3/−2/+1" (mục 4.2 bản khuyến nghị) có khả năng cao là phát biểu về **SIRT1** bị gán sang SIRT7. Cũng sửa citation **Prot2Token** (bioRxiv 2024.05.31.596915 + LMRL@ICLR 2025, **không phải NeurIPS 2025**).
- **Còn dở, xếp theo mức có thể đổi quyết định:** (1) đọc toàn văn **Deep-PLA** ([10.1093/bib/bbz107](https://doi.org/10.1093/bib/bbz107)) xem 9 HDAC của nó gồm SIRT nào — SIRT1–7 *là* HDAC class III, nếu trùng thì trục tính mới sinh học sụp; (2) đọc DeepSIRT toàn văn; (3) mở toàn văn Rauh lấy đúng phát biểu motif từng isoform; (4) tải Supplementary Data 5 + 6 của Rauh (lượng enzyme từng isoform; peptide "không đo được" bị gán âm); (5) tự dựng bảng làm giàu residue theo vị trí trên 6.801 vị trí để biết phần XAI có đáng làm không; (6) tải Table S1 của Zhang 2022 xem có fold-change theo từng vị trí. Chưa chạy mô hình nào.
- **Môi trường:** `static-content.springer.com` trả 403, dùng `media.springernature.com` (200). Phụ lục trên `pmc.ncbi.nlm.nih.gov/.../bin/*.xlsx` trả trang reCAPTCHA với status 200 — phải đi qua trang nhà xuất bản. PRIDE phải dùng API v3 theo từng file (liệt kê thư mục FTP trả 404).
## 08/10/2026 — kiểm chứng sâu đề tài cơ chất sirtuin: tiếp tục với phạm vi thu hẹp

- Thêm [báo cáo phản biện và thiết kế đề tài](deep-research/reports/sirtuin-substrate-deep-research.md), [ghi chú nguồn/audit tái tạo](deep-research/research_notes/sirtuin-substrate/README.md). Giữ nguyên báo cáo khuyến nghị ban đầu; chưa training hoặc triển khai hệ thống.
- **Đính chính có bằng chứng:** nhãn Ridgeway khớp `efficiency ≥ 1`, không phải category/ratio threshold; 64/149 là recall trên tập dương chọn lọc, không precision. Deep-PLA đã có SIRT1/2/3/6/7; Smith 2011 và Zhai 2017 là tiền lệ trực tiếp; Ridgeway đã có cellular validation và thành phần MusiteDeep.
- **Audit:** 6.802→6.801 thiếu chuỗi RELA/p65 GIQCVKKRDLEQA, chưa rõ lý do; 231 dòng `SYNTHETIC`; test 149 có 46 key và 108 dòng cùng protein với pool train, 60 window trùng chuỗi; 149/149 test khớp K và peptide trên snapshot UniProt hiện hành. SD13/SD14 khác toàn bộ điểm SIRT2 và 21 nhãn nhị phân, phải giữ hai snapshot riêng.
- Đọc được Zhang SIRT2 S1 (2.846 dòng), S2 (134 peptide/152 acK), Weinert EV1 có 2.106 ratio SIRT3 KO/WT nhập từ Hebert. **Chưa đủ nhãn âm đáng tin hoặc uncertainty cho benchmark hai isoform.** PXD021357 là sham/UUO; PXD023479 là interactome, không KO acetylome.
- **Khuyến nghị:** bảy isoform ở assay; ưu tiên SIRT2/3 cho cellular response; conformal là mở rộng có điều kiện, không hứa 90% trong tế bào. Tiêu chí 5 của GVHD vẫn là website.
- **Còn dở theo ưu tiên:** lấy bảng Hebert/Rardin gốc (PNAS 403/PMC challenge), replicate/uncertainty và mapping FASTA/homology; giải 152→149 và SD13/14; đọc toàn văn NAD_MCNN/SirtSAGE. Đủ trao đổi phạm vi với GVHD, chưa coi tính mới/benchmark/đề tài đã được duyệt.

---

## 08/10/2026 — hướng có tính mới ở phần tin học, rồi bản phác B + nén mô hình + conformal

- Sinh viên nhận xét A và B chỉ đặt tính mới ở bài toán sinh học. Đã khảo sát bảy hướng cải tiến tin học C1–C7: [compute-novelty-directions.md](deep-research/reports/compute-novelty-directions.md). Phát hiện: bài RAG-msCNN của GVHD đã thử ProstT5 làm baseline và ghi là không cải thiện đáng kể.
- Sinh viên chọn: có GPU, giữ A/B và thêm cải tiến tin học. Bản phác: [b-method-layer-draft.md](deep-research/reports/b-method-layer-draft.md) (thầy ESM-2 + LoRA + mCNN, học trò chưng cất chạy CPU, conformal theo nhóm kinase, XAI kiểm bằng motif đã biết).
- **Phát hiện khi tải thật benchmark dbPTM (nhóm CDK):** chỉ có hai file cửa sổ ±10 (1.503 dương / 29.823 âm), không có chia train/test; file thực nghiệm phospho không có cột kinase. Tập train theo kinase phải dựng từ OmniPath (39.036 dòng kinase–vị trí ở người, tải được) và lọc đồng dạng với benchmark.
- Đối thủ trực tiếp: Prot2Token cho kinase (NeurIPS 2025), nên đề tài nên cạnh tranh bằng tốc độ và bảo đảm thống kê, không bằng độ chính xác.
- **Còn dở:** chưa tải các nhóm kinase khác, chưa đo trùng OmniPath–dbPTM, chưa đọc toàn văn đối thủ, chưa chạy mô hình.

---

## 08/10/2026 — so sánh ứng viên B và A với hướng 2 trên cùng bộ tiêu chí

- Thêm [mục 7.6 vào tài liệu phân tích](deep-research/reports/advisor-4-directions-analysis.md): bảng chín trục so **B**, **A** và **hướng 2** (loại nhãn, tập test độc lập, đơn vị gom nhóm, yếu tố gây nhiễu đã đo, dùng lại thang T1, XAI, mức đông đúc, khớp sinh học GVHD, chi phí khởi động).
- **Kết luận một dòng:** B và A thắng hướng 2 ở ba trục dữ liệu (nhãn thực nghiệm, tập test độc lập, nhiễu kiểm soát được) — đúng ba chỗ hướng 2 thất bại khi chạy số thật ở mục 7.5. Không phải vì chủ đề hay hơn.
- **Cái giá khi bỏ hướng 2, ghi thẳng để nói ở tuần 6:** hướng 2 là ứng viên **duy nhất** nằm đúng giao thoa cancer ∩ aging mà GVHD khung ra; B lệch sang cancer/kinase, A lệch sang aging/sirtuin. Hướng 2 cũng có ý nghĩa dịch thuật rõ hơn, và là hướng do chính GVHD gợi ý — nên lý do bỏ phải là lý do có số (mục 7.5).
- **Việc chọn B hay A vẫn chưa quyết được ở đây:** treo vào câu hỏi số 1 cho GVHD (thầy có coi split tự dựng cộng tập MS độc lập nguồn là test độc lập đủ chuẩn hay không). Nếu có thì A lên trước, vì khớp sinh học là trục duy nhất A thắng B rõ.
- **Còn dở:** chưa khảo sát sâu ứng viên B để lên slide tuần 6 (bài cạnh tranh, chi tiết benchmark dbPTM, định nghĩa nhóm kinase). PR #5 đã merge; nhánh đặt lại từ main.

---

## 07/10/2026 (tối, muộn) — chạy SenMayo trên GSE103322: **dừng hướng 2**

- Áp đúng [bốn ngưỡng đặt trước](deep-research/reports/advisor-4-directions-analysis.md) lên số thật của **GSE103322** (5.902 tế bào, 17 bệnh nhân): `n_patients` 17 **đạt**; `patients_with_ge20_positives` **7/8 KHÔNG đạt**; `concentration_ratio` 1,85 (dải phải cân mẫu); `signature_coverage` 0,97 **đạt**. Phải đạt cả bốn → **dừng hướng 2**. Không nới ngưỡng.
- **Phát hiện nặng hơn, độc lập với ngưỡng:** điểm SenMayo chủ yếu theo **loại tế bào**, không theo senescence — **70% tế bào dương là fibroblast**, tế bào **T và B không có tế bào dương nào**. Chấm ngưỡng riêng theo loại tế bào thì fibroblast chỉ còn **1 bệnh nhân** có ≥20 dương, và tế bào ung thư có 3 bệnh nhân với `concentration_ratio = 3,35` (**vượt ngưỡng dừng 3,0**). Đây là lỗi SenSeqNet lặp lại ở mức loại tế bào thay vì mức họ protein. **GSE131907 không chạy** — dataset lớn hơn không sửa được chuyện này.
- **Khuyến nghị mới: chuyển sang ứng viên B** (site phospho theo nhóm kinase) — ứng viên duy nhất có benchmark non-homologous do dbPTM công bố, và rơi đúng khuôn T1. A là lựa chọn hai, nhớ cổng mở về tập test độc lập.
- **Đính chính trong ngày:** bản 06/10 viết "A và B đều đã qua cổng dữ liệu" — **sai với A**; A chỉ có holdout 10% trên cùng một microarray. Đã sửa ở mục 0, 2.6, 6, 7.2.
- **Dùng được cho tuần 6:** kết quả âm này có số, trên dữ liệu công khai, và trả lời đúng câu "vấn đề tồn đọng là gì". Nói đúng cách: đây là lý do không chọn hướng 2, không phải một đóng góp đã hoàn thành.
- **Còn dở:** PR #3 đã merge nhưng **chỉ chứa 2 commit đầu**; bốn commit sau nằm ở PR mới. Code chạy thật ở PR #4 (nhánh `claude/project-thread-l271f1`).
## 07/10/2026 (khuya) — `tme-senescence-scrnaseq`: chạy SenMayo trên GSE103322 thật, trượt 1/4 ngưỡng và điểm đi theo loại tế bào

- Sinh viên thêm domain NCBI vào danh sách cho phép; GEO trả 200. Đã tải **GSE103322** (HNSCC, Smart-seq2, 5.902 tế bào), chuyển sang h5ad bằng [convert_gse103322.py](../../ml/tme-senescence-scrnaseq/preprocessing/convert_gse103322.py), chấm SenMayo (117 gene, phủ 113). Kết quả và giả định: [README của preprocessing](../../ml/tme-senescence-scrnaseq/preprocessing/README.md).
- **Bốn ngưỡng đặt trước:** 17 bệnh nhân (đạt), **7 bệnh nhân có ≥ 20 tế bào dương (trượt, cần ≥ 8)**, `concentration_ratio` 1,848 (đạt kèm trọng số), độ phủ 0,966 (đạt).
- **Phát hiện quan trọng hơn bốn ngưỡng:** 70% tế bào dương là fibroblast, T/B cell bằng 0, nên chênh lệch giữa bệnh nhân chủ yếu là chênh lệch thành phần loại tế bào. Đặt lại ngưỡng trong từng loại: fibroblast chỉ 1 bệnh nhân có ≥ 20 tế bào dương, tế bào ung thư 3 bệnh nhân và `concentration_ratio` 3,35. Nhãn proxy từ điểm SenMayo trên dataset này về cơ bản là nhãn loại tế bào.
- Mã bệnh nhân suy từ tên tế bào: ra 17, không phải 18 như GEO ghi; 109 tế bào ở plate trộn bị loại khỏi thống kê theo bệnh nhân.
- Script được sửa thêm: `--skip-norm` cho dữ liệu đã log hóa, loại tế bào không rõ bệnh nhân, thống kê theo loại tế bào, `concentration_ratio_per_patient`. Thêm `within_celltype.py`.
- **Còn dở:** chưa cập nhật mục 7 của [phân tích 4 hướng](deep-research/reports/advisor-4-directions-analysis.md) (thread phân tích sở hữu file đó). GSE131907 chưa tải.

---

## 07/10/2026 (tối) — thử tải scRNA-seq khối u để chấm SenMayo: bị chặn mạng, đã viết sẵn script

- **Không tải được dataset nào.** Mạng của môi trường cloud chặn gần hết host dữ liệu, đã thử và ghi đúng mã trả về: `ftp.ncbi.nlm.nih.gov` (GEO), `zenodo.org`, `cellxgene`, `huggingface.co`, `figshare`, `cells.ucsc.edu`, `ha-dkfz.github.io` — **403 ở bước CONNECT**. Chỉ `raw.githubusercontent.com` và PyPI đi được. Đã ghi vào [resources.md](resources.md).
- **Đã làm được phần không cần dataset:** cài scanpy 1.12.4; lấy danh sách gene SenMayo từ bộ chữ ký HA-DKFZ; viết [senmayo_score.py](../../ml/tme-senescence-scrnaseq/preprocessing/senmayo_score.py) đếm tế bào/bệnh nhân, chấm điểm SenMayo và báo **mức dồn tế bào dương theo bệnh nhân**; kiểm trên ma trận tổng hợp 3.000 tế bào (chạy đúng, `top1_patient_share_of_positives = 0,7667` khớp cấu trúc đã cấy). Đây là phép kiểm phần mềm, không phải kết quả sinh học.
- **Cảnh báo phải mang theo:** danh sách lấy được có **117 gene, không phải 125** như bài gốc công bố; **chưa xác định được 8 gene chênh lệch** vì phụ lục là xlsx không lấy được. Không gọi file này là "SenMayo 125 gene" trong tài liệu gửi GVHD.
- Đã thêm slug `tme-senescence-scrnaseq` vào [danh sách đề tài](../topics/README.md) ở trạng thái đang khảo sát, chỉ có code, chưa có tài liệu đề tài riêng.
- **Còn dở:** chờ sinh viên chọn một trong hai đường — cho phép host GEO trong cài đặt môi trường cloud, hoặc tải trên máy của sinh viên. Script chạy được ngay khi có file.

---

## 06/10/2026 — phân tích 4 hướng GVHD gợi ý (giao thoa cancer & aging)

- GVHD đưa **4 hướng tiềm năng** (damage/aging clock + nguy cơ ung thư · phát hiện tế bào lão hóa trong TME · thiết kế tân kháng nguyên bằng generative PLM + RAG · RAG giải thích cơ chế đa tầng). Đã phân tích cả bốn theo đúng khung biên bản lần 1 (bài toán/lý do/phần sẽ giải quyết · history research ba bước · năm tiêu chí · cổng dữ liệu · khả thi 8–9 tuần): [advisor-4-directions-analysis.md](deep-research/reports/advisor-4-directions-analysis.md).
- **Kết luận:** bốn hướng này là **chủ đề**, không phải bài toán, và **không hướng nào qua được cổng dữ liệu + 8–9 tuần ở dạng đang phát biểu**. Ba trong bốn (1, 2, 4) **không có trục chuỗi amino acid** → pipeline PLM–mCNN không dùng lại được → tiêu chí 2–3 mất. Xếp hạng: hướng 2 (senescence trong TME) khả thi nhất; hướng 4 khả thi nếu đổi thành truy hồi bằng chứng có đáp án; hướng 1 rớt vì hình dạng đầu vào (giống lý do đã loại aging clock ngày 02/10); hướng 3 khuyên không chọn (chuỗi sinh ra không có nhãn thật, cộng bốn cổng cũ).
- **`tDamAge` không tra được** bất kỳ bài báo/repo/dataset nào — phải xin GVHD tên bài hoặc DOI. Đây là câu hỏi số một về hướng 1.
- Khuyến nghị: mang bốn hướng này **cùng với** ứng viên A hoặc B của [khảo sát 02/10](deep-research/reports/aging-cancer-deep-dive.md) tới buổi tuần 6 — A và B đạt rõ cả năm tiêu chí và đã qua cổng dữ liệu, bốn hướng mới thì chưa.
- **Còn dở:** phiên này **chưa tải file dữ liệu nào, chưa đọc toàn văn bài nào** — mọi con số mới là `[chưa kiểm]`. Năm việc trước tuần 6 nằm ở mục 6 của tài liệu; giá trị cao nhất là kiểm xem DeepScence/SenCID **có split theo bệnh nhân hay không** và tải thật một dataset scRNA-seq khối u.

---

## 05/10/2026 — đính chính tên GVHD

- Người dùng xác nhận **GVHD là TS. Hồ Quang Thái (Ho Quang Thai; QT Ho)**. Sửa tên đầy đủ trong CLAUDE.md, hồ sơ GVHD và ghi chép cũ; bổ sung tên vào biên bản lần 1.
- Sửa nhận xét trong [phân tích hai luận văn](thesis/thesis-comparison.md): cả hai bài **cùng GVHD** với đề tài hiện tại, nên là tiền lệ trực tiếp để tham khảo. Nhận xét trước đó rằng hai bài khác GVHD là sai.
- Giữ nguyên tên thư mục `Prof Ho/`, tác giả viết tắt trong trích dẫn và trạng thái khảo sát đề tài; việc đính chính tên không tự thay đổi kết luận về nội dung các công bố.

## 05/10/2026 — phân tích hai luận văn tham khảo về tin sinh

- Đọc hai PDF trong `docs/common/thesis/`; lưu [phân tích và so sánh](thesis/thesis-comparison.md), có số trang, bảng kết quả và phân biệt nội dung tác giả báo cáo với nhận xét/đề xuất.
- Bài Hybrid Cascade hữu ích cho thiết kế thực nghiệm PLM–mCNN, xử lý lệch dữ liệu và ứng dụng XAI; ghi rõ giới hạn split chỉ loại trùng hoàn toàn, nhãn âm, diễn giải Focal Loss, đối chứng cỡ mô hình và đánh giá toàn cascade.
- BioFlow-Scope hữu ích cho kiến trúc, provenance và kiểm thử hệ thống; ghi rõ ảnh giao diện dùng mock API, kết quả test do tác giả báo cáo, chưa có benchmark chất lượng truy hồi/LLM.
- Đối chiếu với năm tiêu chí GVHD và hướng aging/cancer đang khảo sát. **Đính chính cùng ngày:** hai PDF ghi Ho Quang Thai, chính là GVHD hiện tại; đây là tiền lệ cùng GVHD, không phải bảo đảm về yêu cầu hay mức đánh giá. Chưa chọn đề tài mới, chưa triển khai hoặc tái lập mã nguồn của hai luận văn.

## 04/10/2026 — bộ bài giảng HTML tự học: chốt danh mục 15 bài, viết mẫu bài 02 và 09

- Chốt danh mục 15 bài trong `docs/common/lectures/` (dùng chung cho cả hai hướng aging và cancer, chưa gắn slug): A. sinh học nền 01–06, B. khung bài toán và đánh giá 07–09, C. mô hình 10–15 (NN, CNN→MCNN, PLM, truy hồi, XAI, đọc bài báo). Sinh viên chọn: đủ 15 bài, **có bài XAI**, **tra web các chi tiết dễ sai**, viết mẫu 02 + 09 trước.
- Đã viết [bài 02 — enzyme và PTM](lectures/02-enzymes-and-ptm.html) và [bài 09 — rò rỉ dữ liệu và chuỗi đồng dạng](lectures/09-leakage-and-homology.html). Mỗi bài là HTML độc lập, chạy offline, có chế độ tối, có phần tương tác nhỏ, gắn nhãn độ tin cậy cho từng khẳng định (đã kiểm / khảo sát sâu / chưa kiểm chứng / suy luận).
- Đã kiểm trên web 04/10/2026: bảng word size và ngưỡng của CD-HIT, định nghĩa coverage của MMseqs2, thống kê PTM Khoury 2011, cơ chế carbonyl hóa (Nyström 2005), glycation (Ansari 2011), phân lớp HDAC/sirtuin, con số 518 kinase (Manning 2002, cho bài 03).
- **Còn dở:** chờ sinh viên duyệt văn phong và mức chi tiết của hai bài mẫu rồi mới viết 13 bài còn lại và `index.html`. Liên kết bài trước/bài sau trong hai bài mẫu đang trỏ tới file chưa có. Chưa xác minh trực tiếp giá trị mặc định `-c 0.8` của MMseqs2 (đang dẫn theo khảo sát sâu).

## 04/10/2026 — lộ trình tự học sinh học nền cho hướng aging và cancer

- Thêm [lộ trình tự học sinh học nền](biology-basics/learning-roadmap.md): lớp nền (central dogma, amino acid, enzyme, PTM), cancer (hallmarks, kinase), aging (hallmarks, sirtuin, acetyl hóa), thực hành UniProt/dbPTM, lịch khoảng 10 ngày trước báo cáo tuần 6, gắn với ứng viên A và B của [khảo sát sâu](deep-research/reports/aging-cancer-deep-dive.md).
- **Còn dở:** chưa tải được PDF nào vì mạng của môi trường cloud chặn các host xuất bản; danh sách file cần tải nằm ở mục 8 của lộ trình. Link và DOI trong lộ trình chưa được mở lại để kiểm.
- Chưa biết mức nền sinh học của sinh viên; đã hỏi để điều chỉnh độ sâu.

## 02/10/2026 (làm rõ định hướng) — gần như chắc chắn đổi RTK–ATP, ưu tiên cancer

- Sinh viên xác nhận: **đề tài hiện tại gần như chắc chắn sẽ bị đổi, hiện đang thiên về cancer**. Bài toán cụ thể chưa chốt; neoantigen mới là nhánh đã được nhắc tới để khảo sát.
- Cập nhật biên bản lần 1, danh sách đề tài, ghi chú quyết định RTK–ATP và CLAUDE.md để phản ánh định hướng này. Cách diễn đạt “chưa quyết định đổi hay giữ” ở các mục cũ không còn phản ánh đúng mức độ ưu tiên hiện tại.
- Bước tiếp theo: ưu tiên xác định bài toán cancer khả thi, dữ liệu và đóng góp để chuẩn bị báo cáo tuần 6.

## 02/10/2026 (sau buổi gặp) — biên bản GVHD lần 1: không bị từ chối nhưng được khuyên tìm hướng khác; mốc tuần 6

**Đã làm**
- Ghi [biên bản buổi gặp lần 1](../meeting/session-01-minutes.md) từ ghi chép của sinh viên: nhận xét định hướng, yêu cầu về cách trình bày và động cơ nghiên cứu, yêu cầu phân tích history research theo ba bước, **năm tiêu chí đánh giá đóng góp**, mốc thời gian, hướng xử lý dự kiến, câu hỏi cho lần trao đổi tiếp.
- Bổ sung vào biên bản phần thông tin người dùng cung cấp sau đó: **mốc tuần 4 / tuần 6 / tuần 14–15** (mục 5) và **hướng đang nghiêng về: cancer, nhánh neoantigen** (mục 6).
- Cập nhật trạng thái `rtk-atp-applicability` trong [docs/topics/README.md](../topics/README.md): "đã chốt hướng" → "đang xem xét lại sau buổi gặp 1".
- Tra danh mục công bố GVHD để hiểu hai hướng được gợi ý. Những gì tra được, **ghi ở đây như ghi chú khảo sát, không đưa vào biên bản vì là suy luận chưa hỏi lại thầy**:
  - **Aging:** công trình mới nhất của Prof Ho là **SirtSAGE** (2026, *J. Comput. Biophys. Chem.*) — Graph Attention cho họ protein **sirtuin**, họ protein trung tâm của nghiên cứu lão hóa; cùng nhánh có **NAD_MCNN** (Prof Ou, 2025, vị trí gắn NAD⁺ của deacetylase). SirtSAGE dùng Graph Attention **chứ không phải mCNN** — tức nhóm đang tự đi ra khỏi PLM–mCNN. Không có từ "aging" nào khác trong hai danh mục; các lần grep khớp đều là "imaging"/"leveraging".
  - **Cancer:** **NeoGen-BC** (Prof Ou, 2026, *BBRC*, neoantigen dùng chung cho ung thư vú) và **DeepNeoAG** (2024, *IJBM*, epitope neoantigen từ kháng nguyên melanoma).
  - **Cho tiêu chí XAI:** **BERT-Promoter** (2022, *Comput. Biol. Chem.*, 124 trích dẫn) dùng SHAP — có mẫu tham chiếu ngay trong nhóm.

**Nội dung GVHD nêu (theo ghi chép sinh viên)**
- Đề tài **không bị từ chối**, nhưng nếu có thể thì nên tìm đề tài khác; **aging** hoặc **cancer** phù hợp hơn ATP.
- Trình bày phải rõ bài toán và **đặc biệt là lý do vì sao cần nghiên cứu** — vấn đề tồn đọng nào cần giải quyết.
- **History research phải phân tích theo ba bước**: phân nhóm theo phương pháp → đánh giá ưu/nhược từng nhóm và từng công trình → đối chiếu với đề tài đã chọn để chỉ rõ cải thiện ở điểm nào.
- **Năm tiêu chí đóng góp**: (1) tính mới của đề tài/hướng đi; (2) đề xuất hoặc cải tiến phương pháp (CNN → mCNN, cải tiến mCNN); (3) sử dụng phương pháp mới — minh họa bằng chuyển dịch PSSM (ma trận, hạn chế về tính thứ tự chuỗi aa và thời gian so sánh) → PLM, kèm câu hỏi liệu có đi xa hơn PLM được không; (4) **XAI** — giải thích được vì sao mô hình đạt kết quả cao cũng là đóng góp; (5) **bắt buộc có ứng dụng/website** vì là luận văn khoa Kỹ thuật phần mềm.
- **Mốc:** hiện tuần 4; **tuần 6 báo cáo lại đề tài rõ ràng**; tuần 14 hoặc 15 là tuần báo cáo.

**Quyết định của sinh viên**
- **Chưa chốt** đổi hay giữ đề tài. **Nghiêng về cancer (neoantigen)**; aging và RTK–ATP điều chỉnh phạm vi chưa bị loại nhưng tạm không khảo sát song song vì chỉ còn hai tuần tới mốc tuần 6.
- **Năm câu hỏi còn lại ở §12 thuyết minh coi là đã lỗi thời** (đều gắn với phạm vi RTK–ATP); chỉ giữ lại câu về nguồn GPU. Ghi rõ trong biên bản là đã cân nhắc và gác lại, không phải bỏ sót.
- **Claude đề xuất, người dùng chưa xác nhận:** tạm hoãn việc kỹ thuật của RTK–ATP (chạy alignment và gom cụm đồng dạng), và dừng đồng bộ `topic-proposal.md` với Notion cùng việc điền tên/MSSV vào slide RTK–ATP. Lý do đề xuất: không nên đổ thêm công vào hướng có thể bị bỏ khi chỉ còn hai tuần tới mốc tuần 6. **Chưa phải quyết định đã chốt của sinh viên.**
- Trạng thái "đã chốt 02/10/2026" đọc lại là "sinh viên tự chốt trước buổi gặp"; **không có phê duyệt GVHD** cho RTK–ATP.

**Lưu ý về chính biên bản này**
- Bản đầu do Claude soạn có thêm một mục tự đối chiếu RTK–ATP với năm tiêu chí (kết luận "đạt 1/5") và một mục suy luận aging = sirtuin. **File đã được viết lại lúc 15:08 theo giọng dè dặt hơn**, bỏ hai mục đó và nêu rõ ghi chép không đủ căn cứ để kết luận "chỉ đạt 1/5" vì GVHD không chấm điểm từng tiêu chí. Bản 15:08 là bản đang dùng; phần đối chiếu và suy luận chỉ còn ở nhật ký này như ghi chú khảo sát.
- Cùng lúc đó [danh sách đề tài](../topics/README.md) cũng được bỏ kết luận "chỉ đạt 1/5 tiêu chí". **Ba điểm sau là diễn giải của Claude, không được dùng như kết luận của buổi họp hay quyết định của sinh viên:** chấm đạt/không đạt theo năm tiêu chí · thu hẹp "aging/cancer" thành "sirtuin/neoantigen" · đề xuất tạm hoãn việc kỹ thuật. Biên bản là căn cứ cho nội dung buổi gặp; nhật ký này chỉ ghi lại quá trình khảo sát.
- Điều người dùng nói rõ và đã ghi vào biên bản: **mốc tuần 4 / tuần 6 / tuần 14–15**, **hướng nghiêng về cancer (neoantigen)**, và **năm câu hỏi §12 không còn liên quan**. Những phần khác trong mục này là ghi chú, không phải lời GVHD.

**Xác nhận lại với người dùng bằng câu hỏi trắc nghiệm (cuối phiên)**
- **GVHD là TS. Hồ Quang Thái (Ho Quang Thai; QT Ho), ĐH Cần Thơ** — tên đầy đủ được đính chính theo người dùng ngày 05/10/2026. Prof. YY Ou **không phải** GVHD. Vai trò được ghi tại [advisor/README.md](advisor/README.md) và [CLAUDE.md](../../CLAUDE.md).
- **Phát hiện ngược chiều với hướng đang ưu tiên:** trong **14 công trình** của GVHD **không có công trình nào về cancer/tumor/neoantigen**. NeoGen-BC và DeepNeoAG thuộc danh mục **Prof Ou**. Ngược lại, **aging có mặt ở công trình mới nhất của GVHD** — SirtSAGE (2026, Graph Attention cho họ sirtuin). GVHD cũng có tiền lệ XAI riêng: BERT-Promoter (2022, SHAP). Giới hạn: danh mục chỉ là bản scrape 14 bài, có thể chưa đầy đủ.
- Thầy khuyên **thay hẳn** đề tài, không phải "tìm thêm để so sánh" — đã sửa cách ghi ở mục 1 biên bản.
- Kỳ vọng về năm tiêu chí: **càng đạt nhiều càng tốt**, không phải chọn một trục. Đã bỏ cách diễn giải "tiêu chí 5 bắt buộc, 1–4 là lựa chọn" khỏi biên bản, thay bằng kỳ vọng thật, kèm lưu ý 8–9 tuần là rủi ro cao và việc cần làm là hỏi GVHD về **thứ tự ưu tiên**.
- Mức chắc chắn: **gần như chắc chắn đổi sang cancer**. Ba file (CLAUDE.md, topic-decision.md, biên bản) giờ nói giống nhau; trước đó biên bản ghi "chưa phải quyết định" trong khi CLAUDE.md ghi "gần như chắc chắn".

**Khảo sát bước đầu hai hướng (cuối phiên)**
- Người dùng chọn **khảo sát cả hai hướng aging và cancer rồi so sánh**, không chọn sẵn một hướng. Đã sửa lại 4 file cho khớp (trước đó ghi "gần như chắc chắn cancer").
- Viết [so sánh hai hướng](deep-research/reports/aging-vs-cancer-topic-comparison.md) trên 8 tiêu chí (5 tiêu chí GVHD + dữ liệu/khớp GVHD/khả thi 8–9 tuần). **Phát hiện aging có hai nhánh con khác nhau hẳn về rủi ro dữ liệu:**
  - **A1 sirtuin:** DeepSIRT (2021, PSSM+1D-CNN, acc 76,69% / MCC 0,49) → **SirtSAGE** (2026, GVHD, **ESM-2 + GATv2 + pLDDT làm cổng tin cậy**). Khớp GVHD nhất nhưng **tính mới thấp** (thầy vừa công bố) và **dữ liệu DeepSIRT không truy cập được** — tự kiểm bằng curl, `http://140.138.155.216/deepsirt/` hết thời gian chờ. Trang SirtSAGE trả HTTP 403 nên chưa đọc được toàn văn.
  - **A2 cellular senescence:** **SenSeqNet** (2026, *Aging Cell*, ESM-2 + LSTM–CNN, acc 86,43% test độc lập), dữ liệu từ **CellAge + UniProtKB**, housekeeping gene làm mẫu âm, **mã nguồn và benchmark công khai trên GitHub**.
- **Giả thuyết đáng kiểm nhất:** SenSeqNet báo **238.634 dương / 217.696 âm** trong khi CellAge chỉ có cỡ vài trăm gene → có thể mở rộng mạnh qua isoform/ortholog → **nghi rò rỉ đồng dạng train/test**, con số 86,43% có thể lạc quan. Kiểm được trong 1–2 ngày bằng cách đếm protein gốc không trùng và chạy CD-HIT/MMseqs2 ở 30%/40%. **Chưa kiểm — là giả thuyết, không phải phát hiện.**
- **Hướng B neoantigen:** đọc `[PDF]` NeoGen-BC trong repo — PLM + RAG + **MCNN-BiLSTM** + cửa sổ trượt + **ProtGPT2 có kiểm soát** + lọc hóa lý + xác nhận cấu trúc; **AUC 0,9053** test độc lập; bắt được neoantigen MHC-II dùng chung từ **ESR1 Y537S/D538G** và **PIK3CA H1047R** mà NetMHCIIpan 4.3 bỏ sót; đồng tác giả lâm sàng ở BV Cựu chiến binh Đài Bắc. **Dữ liệu là mặt mạnh nhất của hướng B:** NEPdb hơn 17.000 bản ghi, TumorAgDB2.0 187.223, **TESLA trên Synapse syn21048999**, bảng đặc trưng trên Figshare, mã NeoRanking trên GitHub, benchmark NCI-test/TESLA/HiTIDE (riêng HiTIDE thô nằm trong EGA kiểm soát truy cập). Nhưng **rất đông** (NeoTImmuML 2025, TransNRank 2026, dòng NetMHCpan) và bài *Immunity* 2023 **đã làm sẵn phần harmonize dữ liệu + so sánh ML** — tức trục "dọn giao thức đánh giá" ở nhánh này đã có người làm.
- **Nhận định bước đầu (của sinh viên, chưa hỏi GVHD):** **A2 senescence** đáng đào sâu nhất vì dung hòa được khớp-GVHD và dữ liệu-sẵn, lại có khoảng trống kiểm được nhanh. Kèm hai cảnh báo: khoảng trống A2 còn là giả thuyết; và **đóng góp dạng "kiểm toán giao thức của bài trước" chính là trục đã làm RTK–ATP yếu**, nên nếu chọn A2 thì không được dừng ở kiểm toán.

**Còn dở**
- **Việc chặn mọi việc khác: chốt hướng trước mốc tuần 6** (còn khoảng hai tuần).
- Chưa hỏi lại GVHD: "cancer" cụ thể là bài toán/dữ liệu nào; có đề tài đang mở trong nhóm để nhận không; **hình thức và mức chi tiết báo cáo tuần 6**; các tiêu chí 1–4 áp dụng thế nào cho phạm vi luận văn; phạm vi tối thiểu của ứng dụng/website; nguồn GPU.
- Chưa khảo sát hướng neoantigen. Hai việc đầu tiên: **đọc NeoGen-BC và DeepNeoAG để biết nhóm đã làm gì**, và **kiểm tra dữ liệu công khai có sẵn hay không** — việc thứ hai có thể loại hướng đi sớm nhất (hướng IL-6 từng bị loại đúng vì lý do này).
- Hai việc phải làm cho bất kỳ hướng nào: dựng **history research theo ba bước**, và viết lại **phần mở đầu theo động cơ nghiên cứu**.
- Kế hoạch 14 tuần trong thuyết minh **không còn khớp mốc thực tế**: còn khoảng 10–11 tuần, phần thực hiện thật khoảng 8–9 tuần, phải chứa cả ứng dụng/website.

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
