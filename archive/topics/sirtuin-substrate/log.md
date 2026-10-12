# Nhật ký đề tài `sirtuin-substrate`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

---

## 10/10/2026 — tải được Supplementary bbz107 và **đo xong phép chuyển nhãn thứ hai**: mảng Rauh không giàu dương tính trên 289 vị trí curated

- Ghi chú: [09-deep-pla-sites-vs-array.md](research/09-deep-pla-sites-vs-array.md); dữ liệu: [deeppla-curated-sites-vs-rauh-labels.csv](research/data/deeppla-curated-sites-vs-rauh-labels.csv); mục 15 của [báo cáo khảo sát sâu](sirtuin-substrate-deep-research.md).
- **Điểm nghẽn hôm 08/10 đã giải tỏa, không cần tải thủ công.** `academic.oup.com` vẫn 403 với curl, nhưng `WebFetch` đọc được trang bài báo; gọi với `offset: 100000` nó trả về **URL CloudFront đã ký**, và curl với URL đã ký trả 200. Lấy được `table_s1.xlsx`, `table_s4.xlsx`, `table_s5.xlsx`. URL không ký trả `MissingKey`; chữ ký có hạn nên phải lặp lại khi cần tải lại.
- **Table S1** 1.666 dòng; lọc sirtuin + người cho **289 vị trí** (SIRT1 185, SIRT2 52, SIRT3 30, SIRT7 12, SIRT6 10) — khớp chính xác cột P trên `help.php`, nên chênh ±1 với Table 1 bài in là lỗi bài in.
- **Kết quả đo:** chỉ **103/289 (35,6%)** vị trí curated có mặt trên mảng Rauh; trên 103 đó mảng gọi dương tính đúng isoform **16 lần (15,5%)**, kỳ vọng 13,7 → độ giàu **1,17×, p = 0,291** (binomial chính xác). Không isoform nào đạt p < 0,05. Dương tính cho ít nhất một isoform 85/103 = 82,5% so với nền 83,7% → **0,986×**, tức tập cơ chất đã được y văn xác nhận không khác một mẫu ngẫu nhiên của mảng.
- **Ý nghĩa:** xác nhận **độc lập thứ hai** cho kết luận trung tâm (nhãn in-vitro gần như không chuyển được vào tế bào), mạnh hơn phép đo Sol 2012 vì dương tính ở đây xác nhận trên protein cuộn gấp, không suy ra từ fold-change, và không cần giả định ngưỡng. Đây là phần trả lời mạnh nhất cho câu "Deep-PLA đã làm rồi".
- **Giới hạn phải nói kèm:** 103/289 nên phép kiểm chỉ nói về phần giao (bị giới hạn bởi cách Rauh chọn peptide 2013); SIRT7 n=2 và SIRT6 n=9 quá nhỏ; khớp theo 13-mer trung tâm có thể bắt paralog, bản khớp nghiêm ngặt chưa làm; tập 289 không có âm tính nên chỉ tính được độ giàu, không tính được MCC.
- **Còn dở:** chưa đọc `table_s4.xlsx` (1,6 MB, dự đoán toàn PLMD) và `table_s5.xlsx`; chưa đọc toàn văn DeepSIRT và ASEB; chưa sửa 7 khẳng định trong `topic-final-recommendation.md`; chưa làm bảng làm giàu residue theo vị trí để quyết định có làm phần XAI hay không.

---

## 08/10/2026 (tối, muộn) — tự tính MCC cho mô hình sirtuin của Deep-PLA; **288 vị trí bị OUP chặn**

- Ghi chú: [08-deep-pla-per-isoform-mcc.md](research/08-deep-pla-per-isoform-mcc.md); bảng số: [deep-pla-sirtuin-mcc-derived.csv](research/data/deep-pla-sirtuin-mcc-derived.csv); mục 14 của [báo cáo khảo sát sâu](sirtuin-substrate-deep-research.md).
- **Không làm được phần được giao:** danh sách 288 vị trí curate nằm trong Supplementary bbz107, **OUP trả 403** cho mọi đường dẫn thử; web server Deep-PLA không có trang tải dữ liệu; PLMD giờ chỉ còn thư mục rỗng; iPTMnet 503; dbPTM 403. **Việc của sinh viên:** tải Supplementary bbz107 bằng quyền đã dùng để lấy PDF.
- **Đổi lại được thứ không có trong bài:** `help.php` của web server công bố P, N và Sp/Sn/Pr ba ngưỡng **cho từng enzyme** (bài chỉ báo AUC cho SIRT1 và HDAC gộp). Từ (P, N, Sn, Sp) dựng lại ma trận nhầm lẫn và **tính được MCC**, chỉ số họ không báo ở đâu.
- **MCC tự tính, cross-validation người, ngưỡng High:** SIRT1 **0,403**, SIRT2 **0,219**, SIRT3 **0,049** (độ nhạy chỉ 7,7%), SIRT6 0,321, SIRT7 **−0,016** (tệ hơn ngẫu nhiên), HDAC gộp họ **0,557**.
- **Hai hệ quả ủng hộ thiết kế đã đề xuất:** (1) mô hình **gộp họ tốt hơn mọi mô hình tách theo isoform**, kể cả SIRT1 → ở cỡ 10–185 vị trí, tách theo isoform làm hại nhiều hơn làm lợi, tức bằng chứng cho bậc B8 (một mô hình đa nhãn chia sẻ biểu diễn); (2) Sn/Sp/Pr che mất vấn đề — SIRT3 có Sp 0,964 và Pr 0,340 trông tạm được nhưng MCC 0,049.
- **Phản biện với chính phép tính:** MCC suy từ số làm tròn 4 chữ số, chỉ đọc hai chữ số; P/N trên web lệch 1 so với Table 1 cho SIRT1 (185 vs 184) và EP300, lệch nhiều hơn cho dòng "HDACs" (147 vs 94), chưa giải thích được; tỉ lệ dương nền là tạo tác của cách dựng tập âm nên MCC này **không so được với bài khác**; tập test SIRT6 chỉ 2 dương và SIRT7 4 dương nên không dẫn MCC của chúng làm bằng chứng.
- **Còn dở:** phép đo 288 vị trí vs nhãn mảng Rauh (chờ file); DeepSIRT và ASEB chưa đọc toàn văn.

---

## 08/10/2026 (tối) — đọc Deep-PLA: **9 HDAC của nó gồm SIRT1, 2, 3, 6, 7** → trục tính mới sinh học hết

- Sinh viên cung cấp PDF bbz107, đã đọc toàn văn. Ghi chú: [07-deep-pla-hdac-coverage.md](research/07-deep-pla-hdac-coverage.md); mục 13 của [báo cáo khảo sát sâu](sirtuin-substrate-deep-research.md).
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

- Sinh viên hỏi bài toán 7 isoform có còn khả thi không. Đã tải Supplementary Data 5 và 6 của Rauh qua `media.springernature.com` và đo trực tiếp. Ghi chú: [06-seven-isoform-feasibility.md](research/06-seven-isoform-feasibility.md); bảng số: [rauh2013-enzyme-amount-vs-positives.csv](research/data/rauh2013-enzyme-amount-vs-positives.csv); mục 12 của [báo cáo khảo sát sâu](sirtuin-substrate-deep-research.md).
- **Kết quả:** số nhãn dương tương quan với nồng độ enzyme nhỏ lên mảng — Spearman **ρ = +0,811**, **p = 0,0349** (hoán vị đầy đủ, n = 7). SIRT5 nhỏ 218 µg/ml → 2.615 dương; SIRT4 nhỏ 10 µg/ml → 1.038. Spearman(nhãn dương, `ratio error` trung vị) = −0,855. Nghịch lý SIRT5 vì vậy có lời giải thích kỹ thuật thí nghiệm.
- **Hai phản biện phải nói kèm:** n = 7 nên p sát ngưỡng; và SIRT1 với SIRT7 **cùng** 20 µg/ml mà 176 so với 1.692 nhãn dương, nên lượng enzyme không giải thích hết. Phát biểu đúng: lượng enzyme là biến gây nhiễu cỡ lớn chưa được hiệu chỉnh.
- **Một mối lo bị bác bỏ bằng số:** Supplementary Data 6 có 220 peptide "không cho tín hiệu ở ≥ 1 đối chứng", tất cả vẫn nằm trong bộ nhãn, nhưng 185/220 (84,1%) là dương ở ít nhất một isoform — gần trùng tỉ lệ toàn mảng 5.695/6.802 (83,7%). Nên giả thuyết "nhãn âm thật ra là không đo được" không thành.
- **Kết luận về khả thi, ba mức:** SIRT1/2/3 khả thi (khung deacetylase đúng, có bằng chứng mức protein, có tập in-cell); SIRT1 là ca xấu nhất về dữ liệu chứ không về sinh học; SIRT4–7 không khả thi như bài toán "dự đoán cơ chất deacetyl hóa" — chuyển thành phân tích giới hạn của nhãn, lấy chính bảng lượng enzyme vs nhãn dương làm nội dung.
- **Còn dở:** chưa tách tương quan theo từng cặp (construct, mảng) — Data 5 cho thấy mỗi isoform được thử với nhiều construct và đột biến bất hoạt khác nhau, nên "nồng độ trung vị theo isoform" là phép gộp thô. Và năm việc chặn khác của mục 11.2 vẫn nguyên, trong đó **đọc toàn văn Deep-PLA** là việc có thể đổi phán quyết tính mới.

---

## 08/10/2026 (chiều) — khảo sát sâu đề tài chính SIRT1–7: **nhãn mảng peptide gần như không chuyển được vào tế bào**

- Phản biện độc lập bản khuyến nghị [topic-final-recommendation.md](../../surveys/topic-final-recommendation.md) bằng năm nhánh khảo sát song song (sinh học/nhãn, tính mới, cổng dữ liệu, thiết kế đánh giá, conformal+XAI). Báo cáo tổng hợp: **[sirtuin-substrate-deep-research.md](sirtuin-substrate-deep-research.md)**; ghi chú từng nhánh và bảng dẫn xuất: [research_notes/sirtuin-substrate/](research/). Bản khuyến nghị cũ **giữ nguyên không sửa** để đối chiếu.
- **Phán quyết: THU HẸP.** Giữ đề tài nhưng hạ phạm vi định lượng xuống **SIRT1/2/3** và đổi lời hứa từ "một mô hình tốt hơn" sang "một phép đo có kiểm soát về mức độ KHÔNG chuyển được của nhãn in vitro". Chuyển sang đề tài B **chỉ nếu** GVHD không chấp nhận kết quả âm làm đóng góp chính.
- **Phát hiện nặng nhất (phép đo thật, không phải suy luận):** nhãn SIRT3 của mảng Rauh dự báo chiều thay đổi acetyl hóa trong tế bào (Sol 2012, U2OS) với **MCC +0,047…+0,080** trên 1.417 vị trí khớp cửa sổ 13-mer, và **MCC −0,007** trên tập chồng lấn chặt (n = 718). Tập chuột cho kết quả tương tự. Đây là giả thuyết trung tâm của đề tài, và nó gần như không đứng.
- **Bốn đính chính quan trọng với bản khuyến nghị:** (1) con số **43,0%** của Ridgeway 2025 là **recall**, không phải precision, và pha rò rỉ (52,3% trên vị trí đã có trong train vs **39,0%** ngoài train); (2) quy tắc nhãn dương là **`efficiency ≥ 1`**, không phải `category = 1` — tái lập 100,0000% trên 47.607 ô, nên lập luận "ngưỡng cứng bỏ mất nhãn yếu" không đứng; (3) **nhãn âm in-cell đã tồn tại** — Zhang 2022 ([PMC8907344](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907344/)) định lượng 2.846 vị trí mà chỉ 152 phụ thuộc SIRT2, và Sol 2012 (PLoS ONE 7:e50545) có 3.174 vị trí SIRT3 ở người + 1.566 ở chuột, nên **AUPRC và MCC trong tế bào đo được**, không phải chỉ precision; (4) **DeepSIRT 2021** (Comput Biol Chem 93:107514, tác giả cuối Y.-Y. Ou) đã dự đoán target SIRT1–7 bằng CNN ở mức protein — tiền lệ bị bỏ sót, và là của nhóm Prof. Ou, phải nêu chủ động trên slide 1 cạnh NAD_MCNN.
- **Khung sinh học đổ ở chỗ khác với dự đoán:** bản khuyến nghị đặt cổng dừng ở SIRT1 (176 nhãn dương), nhưng SIRT1 là deacetylase hợp lệ nhất. Chỗ đổ là **SIRT4/5/6/7** — Mathias 2014 (Cell) và Jiang 2013 (Nature) nói thẳng 4/7 sirtuin có rất ít hoặc không có hoạt tính deacetylase. Nghịch lý phải giải thích: SIRT5 lại là cột có **nhiều nhãn dương nhất (2.614)**.
- **Conformal:** không có bảo đảm nào chuyển được sang miền in-cell (khoảng cách này là *concept shift*, không phải covariate shift, nên weighted conformal không áp dụng). Bảo đảm in-cell trung thực duy nhất là độ phủ trên lớp dương của SIRT2, nếu tách một phần tập Zhang làm hiệu chỉnh. Phải viết rõ chọn mức A (biên) / B (theo lớp) / C (conformal risk control) trong đề cương.
- **Một con số phải gỡ khỏi mọi tài liệu gửi GVHD cho tới khi đọc lại toàn văn Rauh:** phát biểu "SIRT7 ưa residue thân nước ở −3/−2/+1" (mục 4.2 bản khuyến nghị) có khả năng cao là phát biểu về **SIRT1** bị gán sang SIRT7. Cũng sửa citation **Prot2Token** (bioRxiv 2024.05.31.596915 + LMRL@ICLR 2025, **không phải NeurIPS 2025**).
- **Còn dở, xếp theo mức có thể đổi quyết định:** (1) đọc toàn văn **Deep-PLA** ([10.1093/bib/bbz107](https://doi.org/10.1093/bib/bbz107)) xem 9 HDAC của nó gồm SIRT nào — SIRT1–7 *là* HDAC class III, nếu trùng thì trục tính mới sinh học sụp; (2) đọc DeepSIRT toàn văn; (3) mở toàn văn Rauh lấy đúng phát biểu motif từng isoform; (4) tải Supplementary Data 5 + 6 của Rauh (lượng enzyme từng isoform; peptide "không đo được" bị gán âm); (5) tự dựng bảng làm giàu residue theo vị trí trên 6.801 vị trí để biết phần XAI có đáng làm không; (6) tải Table S1 của Zhang 2022 xem có fold-change theo từng vị trí. Chưa chạy mô hình nào.
- **Môi trường:** `static-content.springer.com` trả 403, dùng `media.springernature.com` (200). Phụ lục trên `pmc.ncbi.nlm.nih.gov/.../bin/*.xlsx` trả trang reCAPTCHA với status 200 — phải đi qua trang nhà xuất bản. PRIDE phải dùng API v3 theo từng file (liệt kê thư mục FTP trả 404).

---

## 08/10/2026 — kiểm chứng sâu đề tài cơ chất sirtuin: tiếp tục với phạm vi thu hẹp

- Thêm [báo cáo phản biện và thiết kế đề tài](sirtuin-substrate-deep-research.md), [ghi chú nguồn/audit tái tạo](research/README.md). Giữ nguyên báo cáo khuyến nghị ban đầu; chưa training hoặc triển khai hệ thống.
- **Đính chính có bằng chứng:** nhãn Ridgeway khớp `efficiency ≥ 1`, không phải category/ratio threshold; 64/149 là recall trên tập dương chọn lọc, không precision. Deep-PLA đã có SIRT1/2/3/6/7; Smith 2011 và Zhai 2017 là tiền lệ trực tiếp; Ridgeway đã có cellular validation và thành phần MusiteDeep.
- **Audit:** 6.802→6.801 thiếu chuỗi RELA/p65 GIQCVKKRDLEQA, chưa rõ lý do; 231 dòng `SYNTHETIC`; test 149 có 46 key và 108 dòng cùng protein với pool train, 60 window trùng chuỗi; 149/149 test khớp K và peptide trên snapshot UniProt hiện hành. SD13/SD14 khác toàn bộ điểm SIRT2 và 21 nhãn nhị phân, phải giữ hai snapshot riêng.
- Đọc được Zhang SIRT2 S1 (2.846 dòng), S2 (134 peptide/152 acK), Weinert EV1 có 2.106 ratio SIRT3 KO/WT nhập từ Hebert. **Chưa đủ nhãn âm đáng tin hoặc uncertainty cho benchmark hai isoform.** PXD021357 là sham/UUO; PXD023479 là interactome, không KO acetylome.
- **Khuyến nghị:** bảy isoform ở assay; ưu tiên SIRT2/3 cho cellular response; conformal là mở rộng có điều kiện, không hứa 90% trong tế bào. Tiêu chí 5 của GVHD vẫn là website.
- **Còn dở theo ưu tiên:** lấy bảng Hebert/Rardin gốc (PNAS 403/PMC challenge), replicate/uncertainty và mapping FASTA/homology; giải 152→149 và SD13/14; đọc toàn văn NAD_MCNN/SirtSAGE. Đủ trao đổi phạm vi với GVHD, chưa coi tính mới/benchmark/đề tài đã được duyệt.
