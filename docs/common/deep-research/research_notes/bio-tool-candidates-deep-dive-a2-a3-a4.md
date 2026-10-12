# Đi sâu A2, A3, A4 — bài toán, I/O, đóng góp & ý nghĩa

> Ngày: **12/10/2026**. Bổ sung cho [bioinformatics-tool-layer-candidates-2026-10-12.md](../reports/bioinformatics-tool-layer-candidates-2026-10-12.md). Theo yêu cầu sinh viên: làm rõ bài toán/đầu vào/đầu ra/đóng góp cho ba ứng viên bậc A có khớp GVHD mạnh nhất, **chưa phân tích dữ liệu**. Thêm 5 lượt `WebSearch` để làm rõ tiền lệ — **vẫn [CHƯA KIỂM]**, chưa đọc toàn văn, chưa tự tải gì.
>
> **Phát hiện quan trọng làm thay đổi A3:** tìm được một công trình 2025 (Denger & Helms, *Molecules*) đã làm gần đúng ý tưởng ban đầu của A3 cho đúng nhóm protein vận chuyển. Phải thu hẹp đóng góp ngay khi phát hiện, theo đúng quy ước đã dùng cho mọi đề tài khác trong repo (degron, DARKIN) — xem mục A3.2.

---

## A2 — Benchmark độ trung thực (fidelity) cho XAI trên mô hình điều hòa gen/protein

### Bài toán

Các bài báo (kể cả của GVHD, ví dụ BERT-Promoter dùng SHAP) coi điểm quan trọng (importance score) do SHAP/attention/Integrated Gradients sinh ra như một dạng "giải thích sinh học" — ngụ ý rằng vị trí được chấm điểm cao chính là vị trí có ý nghĩa sinh học thật (motif điều hòa, vị trí gắn ligand). Nhưng việc này **hầu như không được kiểm chứng độc lập**: một position paper ICML 2026 ([arXiv 2606.07607](https://arxiv.org/pdf/2606.07607), Zhou/Huang/Li, Exeter) tự chạy benchmark trên bài toán gắn kết yếu tố phiên mã và phát hiện **các phương pháp XAI khác nhau cho giải thích mâu thuẫn nhau trên cùng một dự đoán, không định vị đúng motif điều hòa đã biết, và không phản ánh trung thực cơ chế quyết định nội tại của mô hình**. Họ đề xuất một khung đánh giá kiểu "thử nghiệm lâm sàng" (đo tính nhất quán, độ trung thực, giá trị sinh học một cách hệ thống) nhưng đây là **bài báo quan điểm, không phải một bộ công cụ/benchmark đã triển khai cho protein**.

Câu hỏi cụ thể: khi một mô hình mCNN+PLM dự đoán đúng (ví dụ "vị trí 47 là vị trí gắn ATP"), điểm SHAP/attention gán cho vị trí đó **có thực sự trùng với vị trí đã biết từ cấu trúc/thực nghiệm độc lập hay không** — hay mô hình đoán đúng "nhờ" một tín hiệu khác (ví dụ thành phần amino acid tổng thể) và XAI chỉ đang tạo ảo giác diễn giải hợp lý?

### Đầu vào / Đầu ra

**Đầu vào:**
- Một (hoặc nhiều) mô hình đã huấn luyện `M` (ví dụ mCNN+PLM cho ATP-binding site, hoặc một bộ phân loại promoter kiểu BERT-Promoter) và dự đoán của nó trên một trình tự.
- Một phương pháp attribution `A` (SHAP, Integrated Gradients, attention weight, saliency) → sinh ra một vector điểm quan trọng theo từng vị trí/residue.
- **Ground truth độc lập, không lấy từ chính mô hình:** vị trí gắn ligand đã xác định bằng cấu trúc (PDB, UniProt feature "binding site"), hoặc motif điều hòa đã xác nhận thực nghiệm (JASPAR, ChIP-seq).

**Đầu ra:**
- Điểm **trung thực** (fidelity) cho từng cặp (mô hình, phương pháp attribution): mức độ chồng lấp giữa top-k vị trí được chấm điểm cao nhất và vị trí thật (ví dụ AUPRC, "Attribution-AUC" theo cách PNAS McCloskey et al. đã làm cho bài toán gắn kết ligand-nhỏ, hoặc precision@k).
- Điểm **nhất quán**: các phương pháp attribution khác nhau trên cùng một mô hình/ví dụ có đồng ý với nhau không (nếu không, ít nhất một trong số chúng đang "bịa" giải thích).
- Một **bảng/báo cáo** nêu rõ: với họ mô hình nào, phương pháp attribution nào đáng tin để dùng cho tuyên bố sinh học, và phương pháp nào trông hợp lý bằng mắt nhưng không bắt đúng tín hiệu thật.

### Đóng góp & ý nghĩa

1. **Chuyển "XAI cho thấy insight sinh học" từ một giả định ngầm thành một đại lượng đo được.** Đây đúng là khoảng trống mà bài ICML 2026 chỉ ra nhưng chưa triển khai cho protein — biến bài báo quan điểm thành một công cụ thật.
2. **Kiểm định trực tiếp phương pháp GVHD đang dùng.** BERT-Promoter (công trình GVHD, 2022) dùng SHAP để chọn đặc trưng và trình bày như một phần đóng góp XAI. Nếu công cụ này cho thấy SHAP trên họ mô hình đó **có** định vị đúng motif đã biết → đó là bằng chứng ủng hộ công khai cho chính công trình GVHD. Nếu **không** → đó là một phát hiện có giá trị cảnh báo cho cả nhóm nghiên cứu, và tự nó là một đóng góp (giống mẫu hình "kết quả phê phán" đã từng được chấp nhận một phần trong lịch sử repo này, miễn không bị coi là "chỉ có kết quả âm" — ở đây vẫn có phần dương: xây được công cụ kiểm định dùng lại được).
3. **Không cần dữ liệu/nhãn mới** — dùng lại chính ground truth cấu trúc/motif đã có sẵn trong các đề tài trước (`rtk-atp-applicability`), nên rủi ro về G1 rất thấp.
4. **Khớp trực diện tiêu chí 4 (XAI)** của khung GVHD — nhưng ở một mức cao hơn: không chỉ "có dùng XAI" mà "XAI này có đáng tin không", điều mà chưa công trình nào trong danh mục GVHD tự kiểm.
5. **Rủi ro cần đóng trước khi tin là khoảng trống còn mở:** tìm thấy **TPCAV** (concept attribution cho mô hình genomics, báo cáo định vị motif DNA đáng tin hơn TCAV) và một **benchmark bioRxiv 01/2025** đánh giá các mô hình sequence-function diễn giải được, có đưa "khả năng diễn giải" là một trong các tiêu chí. Hai công trình này **có thể đã làm một phần việc này cho DNA** — phải đọc toàn văn cả hai trước khi khẳng định "chưa ai làm cho protein/XAI tầng residue".

---

## A3 — Benchmark cấu trúc (AlphaFold) + trình tự (PLM) cho protein màng/vận chuyển, có kiểm soát rò rỉ

### A3.1 Bài toán (bản gốc, trước khi tìm thấy tiền lệ)

14 công trình GVHD đều dự đoán chức năng/vị trí gắn bằng **trình tự thuần** (PSSM, PLM) — không công trình nào dùng đặc trưng cấu trúc AlphaFold. Ý tưởng ban đầu: thêm cấu trúc có kiểm soát rò rỉ nghiêm ngặt, đo phần cải thiện thật.

### A3.2 PHẢI THU HẸP — tiền lệ trực tiếp vừa tìm được

**Denger & Helms, *Molecules* 2025** đã dùng AlphaFold2 kết hợp **mã hóa cấu trúc 3Di (Foldseek)** và **embedding cấu trúc ProstT5** để dự đoán **cơ chất của protein vận chuyển màng** — đúng nhóm GVHD chuyên sâu (carrier đường/amino acid ở *A. thaliana*, ba loại kênh ion ở người). Kết quả: mạng feed-forward dùng mã hóa cấu trúc cho hiệu năng **tốt và ổn định hơn** phương pháp trước, và mã hóa cấu trúc (Foldseek/ProstT5) **ngang bằng** embedding trình tự PLM tốt nhất. **Không được nói "chưa ai kết hợp cấu trúc AlphaFold với trình tự cho protein vận chuyển" — đã có, 2025.**

Thêm một cảnh báo phương pháp luận nghiêm trọng hơn: một tóm tắt hội thảo 2026 (L. Palazzolo) lập luận rằng **cấu trúc AlphaFold tĩnh không nhất thiết tương ứng với trạng thái hoạt động về chức năng** — mô hình AlphaFold cho protein vận chuyển thường giống trạng thái trung gian/bị che khuất, nên đặc trưng bề mặt/pocket **có thể không đáng tin** cho nhận diện ligand hay khả năng tiếp cận cơ chất. Protein vận chuyển đổi hình dạng liên tục khi hoạt động (nhiều trạng thái conformation) — một cấu trúc AlphaFold tĩnh chỉ là một lát cắt. Điều này **đánh trực tiếp vào đúng nhóm protein A3 muốn nhắm tới**, không phải lo ngại chung chung.

### Bài toán đã định vị lại

Không còn là "ai cũng chưa làm, tôi làm đầu tiên" — mà là: **liệu phần cải thiện mà Denger & Helms (và các công trình tương tự) báo cáo có đứng được sau khi kiểm soát hai nguồn nhiễu mà chính lĩnh vực đang bỏ qua** — (1) rò rỉ do protein kiểm tra trùng/giống dữ liệu huấn luyện AlphaFold, và (2) cấu trúc tĩnh có thể không phản ánh trạng thái liên quan tới chức năng. Đây chuyển A3 từ "thêm một đặc trưng" sang **một audit phương pháp luận có kỷ luật** — đúng dạng công cụ mà CLAUDE.md ưu tiên.

### Đầu vào / Đầu ra

**Đầu vào:**
- Trình tự protein (như các công trình GVHD hiện có) → embedding PLM.
- Cấu trúc dự đoán AlphaFold (tọa độ) → đặc trưng dẫn xuất: chuỗi 3Di (Foldseek), embedding cấu trúc (ProstT5), đặc trưng pocket/bề mặt (ví dụ qua CASTpFold).
- **Metadata bắt buộc cho kiểm soát rò rỉ:** ngày công bố cấu trúc PDB/AlphaFoldDB, họ fold/cấu trúc (không chỉ họ trình tự) để chia tập theo độ tương đồng **cấu trúc 3D**, không chỉ theo trình tự (bài ICLR 2024 về rò rỉ PPI đã chỉ ra chia theo trình tự là không đủ, phải chia theo tương đồng giao diện/cấu trúc 3D).
- Nhãn chức năng/vị trí gắn — tái dùng đúng loại nhãn GVHD đã công bố (ATP-binding, efflux, ion-transporter) nếu truy cập được, hoặc nhãn công khai tương đương.

**Đầu ra:**
- Hiệu năng dự đoán dưới **hai giao thức chia tập**: (i) chia ngẫu nhiên/theo trình tự (tái lập số liệu kiểu văn liệu hiện có — "lạc quan") và (ii) chia có kiểm soát rò rỉ (theo mốc thời gian công bố cấu trúc khớp với cutoff huấn luyện AlphaFold, cộng lọc trùng lặp theo tương đồng cấu trúc 3D). **Độ chênh giữa (i) và (ii) chính là số liệu cốt lõi của đóng góp.**
- Một **cờ "đáng tin tĩnh" / "mơ hồ về conformation"** gắn cho từng ví dụ kiểm tra: liệu đặc trưng pocket/bề mặt từ cấu trúc AlphaFold của ca đó có khớp với cấu trúc thực nghiệm đã biết (nếu có) của đúng protein ở trạng thái gắn ligand, qua đó đo xem cảnh báo của Palazzolo có biểu hiện thành sai số thật hay chỉ là lo ngại lý thuyết.

### Đóng góp & ý nghĩa (đã thu hẹp, trung thực hơn)

1. **Không tuyên bố "đầu tiên kết hợp cấu trúc+trình tự cho protein vận chuyển"** — Denger & Helms đã làm. Đóng góp là **kiểm định độc lập, có kỷ luật chống rò rỉ**, mà bài 2025 đó (và phần lớn lĩnh vực, theo bioRxiv 2024.08.02.606297) **chưa chắc đã làm đủ nghiêm ngặt**.
2. **Giá trị thực tiễn trực tiếp cho GVHD:** câu trả lời "có nên thêm cấu trúc AlphaFold vào các mô hình mCNN tương lai của nhóm không, hay phần lợi ích báo cáo trong văn liệu chỉ là nhiễu/rò rỉ" là một câu hỏi phương pháp luận thầy sẽ cần cho **mọi** công trình tiếp theo của nhóm, không chỉ một bài toán đơn lẻ.
3. **Thao tác hóa được một chỉ trích lý thuyết (Palazzolo) thành một con số đo được** — biến "cấu trúc tĩnh có thể không đáng tin cho protein đổi hình dạng" từ một lời cảnh báo định tính thành một cờ định lượng kiểm tra được trên từng ví dụ.
4. **Rủi ro còn lại:** đây là một audit, nên G2 (đóng góp dương) có hai khả năng kết cục đều có giá trị khoa học (cấu trúc vẫn giúp sau kiểm soát rò rỉ → xác nhận tích cực cho hướng GVHD; hoặc phần lợi ích biến mất → cảnh báo quan trọng, bảo vệ nhóm khỏi dùng một đặc trưng không đáng tin) — nhưng phải trình bày trung thực với GVHD rằng kết quả có thể đi theo hướng phủ nhận, giống bài học "kết quả âm" đã rút ra từ hướng sirtuin trước đây.

---

## A4 — Công cụ audit calibration/miền áp dụng cho mô hình mCNN+PLM

### Bài toán

Các mô hình mCNN+PLM (họ mô hình chính của GVHD) xuất ra một điểm số (thường qua softmax/sigmoid) được đọc như "độ tin cậy", nhưng **không công trình nào trong danh mục GVHD kiểm tra điểm số đó có được hiệu chỉnh (calibrated) hay không** — "90% tin cậy" có thực sự tương ứng với 90% chính xác thực nghiệm không? Và khi một protein đưa vào dự đoán **nằm xa mọi họ protein đã huấn luyện** (ngoài miền áp dụng), mô hình có tự động hạ độ tin cậy một cách hợp lý, hay vẫn đưa ra điểm số tự tin như bình thường (và vì vậy gây hiểu lầm)? Tra cứu hôm nay **không tìm thấy công trình 2025-2026 nào áp phương pháp conformal prediction/out-of-distribution detection cho đúng lớp mô hình PLM-classifier này** — công trình conformal gần nhất (protein-ligand affinity) là bài toán hồi quy khác hẳn, không phải phân loại vị trí/họ protein.

### Đầu vào / Đầu ra

**Đầu vào:**
- Một (hoặc nhiều) mô hình mCNN+PLM đã huấn luyện của GVHD (ATP-binding, efflux, FAD-binding...) + điểm dự đoán thô trên tập kiểm tra.
- Embedding PLM của protein kiểm tra.
- Định nghĩa rõ **"họ đã huấn luyện"** (UniProt/Pfam family nằm trong tập train) để tự dựng hai nhóm kiểm tra có kiểm soát: cùng họ (giữ lại, chưa thấy) và khác họ hẳn (ngoài miền áp dụng thật).

**Đầu ra:**
- **Đường cong/chỉ số calibration** (ví dụ Expected Calibration Error) cho mỗi mô hình: điểm tin cậy có khớp tỷ lệ đúng thật không.
- **Cờ miền áp dụng** cho từng dự đoán (trong miền / gần biên / ngoài miền), tính từ khoảng cách trong không gian embedding PLM (ví dụ tỷ lệ hàng xóm gần là trình tự "lạ", theo đúng ý tưởng Nature Methods 04/2026) hoặc điểm non-conformity kiểu conformal prediction.
- **Bằng chứng cờ có ý nghĩa:** chứng minh bằng thực nghiệm rằng nhóm bị gắn cờ "ngoài miền" có tỷ lệ lỗi thật cao hơn rõ rệt nhóm "trong miền" — nếu không chứng minh được điều này, cờ chỉ là nhiễu, phải báo đúng như vậy.
- Một **thư viện dùng lại được**, không phải kết quả của một bài toán đơn lẻ — áp được cho bất kỳ mô hình mCNN+PLM nào có cùng kiến trúc đầu vào.

### Đóng góp & ý nghĩa

1. **Tổng quát hóa đúng ý tưởng "cảnh báo miền áp dụng" mà chính sinh viên đã từng muốn làm riêng cho đề tài `rtk-atp-applicability` (bị khuyên đổi hướng 02/10/2026)** — thay vì một tính năng gắn cho một bài toán, biến nó thành công cụ kiểm định dùng chung cho **mọi** mô hình GVHD đã/sẽ công bố. Đây là lý do mạnh để coi A4 là sự "hồi sinh có kỷ luật hơn" của ý tưởng RTK-ATP cũ, không phải một hướng hoàn toàn mới.
2. **Giá trị ứng dụng thật, không chỉ lý thuyết:** nếu GVHD có máy chủ web công khai cho các mô hình đã công bố (nhiều công trình trong danh mục có khả năng có web server, theo mẫu hình chung của nhóm), công cụ này có thể **gắn trực tiếp vào các máy chủ đó** như lớp cảnh báo "protein bạn vừa nhập nằm ngoài miền mô hình đã học, kết quả có thể không đáng tin" — một đóng góp tiêu chí 5 (ứng dụng) rất cụ thể, không phải một app trình diễn tách biệt.
3. **Không cần phát minh kiến trúc mới** — dùng lại đúng mô hình GVHD đã có, chỉ thêm một lớp kiểm định bên ngoài. Điều này khớp đúng lối "đóng góp bằng cách làm phương pháp đã có đáng tin cậy hơn" (tiêu chí 2-3) mà không cần cược vào một kiến trúc chưa ai dùng.
4. **Đây là ứng viên có khoảng trống rõ nhất trong ba ứng viên**, theo tra cứu hôm nay — không tìm thấy tiền lệ trực tiếp nào kết hợp conformal/OOD với đúng bài toán phân loại PLM-classifier này, khác với A2 (có TPCAV/benchmark liền kề) và A3 (có Denger & Helms làm gần giống).

---

## So sánh nhanh ba ứng viên sau khi đi sâu

| | A2 — fidelity XAI | A3 — audit cấu trúc+trình tự | A4 — calibration/miền áp dụng |
|---|---|---|---|
| Độ mới sau khi tra thêm | Khá — có TPCAV/benchmark liền kề cần đọc kỹ trước khi tin là mở | **Giảm rõ** — Denger & Helms 2025 đã làm gần giống; phải đổi khung sang audit | **Cao nhất** — chưa tìm thấy tiền lệ trực tiếp |
| Cần dữ liệu/nhãn mới? | Không — dùng lại ground truth cấu trúc/motif đã có | Không nhiều — dùng lại nhãn GVHD/công khai, cần thêm metadata ngày công bố cấu trúc | Không — dùng lại mô hình/dữ liệu GVHD, cần tự định nghĩa tập OOD |
| Rủi ro kết quả có thể "âm" (phủ nhận chính phương pháp GVHD) | Trung bình — có thể SHAP không đáng tin trên mô hình GVHD | Trung bình-cao — có thể cấu trúc không giúp gì sau kiểm soát rò rỉ | Thấp hơn — mục tiêu là đo, không nhất thiết phủ nhận mô hình gốc |
| Cần quyền truy cập mã nguồn/trọng số GVHD? | Có lợi nếu có, không bắt buộc (có thể tự huấn luyện lại baseline tương đương) | Có lợi nếu có | Có lợi nếu có |

**Gợi ý thứ tự ưu tiên nếu phải chọn một:** A4 (khoảng trống rõ nhất, rủi ro thấp nhất) → A2 (cần đọc kỹ TPCAV trước) → A3 (đóng góp vẫn có giá trị nhưng phải trình bày đúng là một audit, không phải phát hiện đầu tiên).
