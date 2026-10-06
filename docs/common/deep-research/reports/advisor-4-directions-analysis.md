# Phân tích 4 hướng GVHD gợi ý (giao thoa Cancer & Aging)

**Ngày 06/10/2026.** Phân tích theo đúng khung trình bày GVHD yêu cầu ở [biên bản lần 1](../../../meeting/session-01-minutes.md) (mục 2: bài toán / lý do / phần sẽ giải quyết; mục 3: history research ba bước; mục 4: năm tiêu chí), cộng hai cổng chặn mà biên bản nói phải kiểm sớm nhất: **dữ liệu công khai có tập test độc lập hay không** và **khả thi trong 8–9 tuần**.

> **Mức kiểm chứng** — giữ đúng quy ước của [khảo sát sâu 02/10/2026](aging-cancer-deep-dive.md): `[toàn văn]` · `[abstract]` · `[đã thử link]` · `[tự đo]` · `[chưa kiểm]` (chỉ có từ search snippet, **chưa xác nhận ở nguồn gốc**). Phiên này **chưa tự tải file dữ liệu nào**, nên mọi con số dưới đây cao nhất là `[abstract]` hoặc `[chưa kiểm]`, trừ chỗ dẫn lại khảo sát 02/10 đã `[tự đo]`.

---

## 0. Kết luận trước, để đọc phần sau có định hướng

Bốn hướng này **không ở cùng một mức trừu tượng** với sáu ứng viên A–F trong [khảo sát sâu](aging-cancer-deep-dive.md). A–F là **bài toán** (vào gì, ra gì, nhãn ở đâu). Bốn hướng này là **chủ đề** — mỗi hướng còn phải chọn một bài toán cụ thể bên trong. Đây không phải lỗi của ai: ở mức chủ đề thì cả bốn đều hợp lý; nhưng **không hướng nào trong bốn hướng này, ở dạng đang được phát biểu, đi qua được cổng dữ liệu + 8–9 tuần mà không bị thu hẹp lại**.

Xếp hạng, nói thẳng:

| | Hướng | Phán quyết một dòng |
|---|---|---|
| **1** | **Hướng 2 — phát hiện tế bào lão hóa trong khối u** | **Khả thi nhất**, nhưng chỉ sau khi chọn **một** modality và thu hẹp thành một bài toán có tập test độc lập. Rủi ro lớn nhất: đã có 3–4 công cụ 2024–2026 làm đúng việc này |
| **2** | **Hướng 4 — RAG giải thích cơ chế đa tầng** | Khả thi về **sản phẩm** (đạt tiêu chí 5 rất tốt), nhưng **phần "giải thích" gần như không đánh giá được định lượng** → tiêu chí 1–2 khó bảo vệ, dễ thành "một con chatbot có citation" |
| **3** | **Hướng 1 — đồng hồ sinh học & nguy cơ ung thư** | **Đã bị loại to tiếng trong khảo sát 02/10 và lý do vẫn đứng:** đầu vào không phải chuỗi amino acid → toàn bộ lineage PLM → mCNN → RAG của GVHD **không áp dụng được**, nên tiêu chí 2 và 3 không đạt được. Thêm nữa, `tDamAge` **không tra được** (xem 1.1) |
| **4** | **Hướng 3 — thiết kế tân kháng nguyên bằng generative PLM + RAG** | **Rủi ro cao nhất, khuyên không chọn.** Ba cổng rớt độc lập nhau: định vị (đúng lane Prof Ou), đánh giá (không có ground truth cho chuỗi sinh ra), và chỉ số (benchmark sạch cho AUC 0,52–0,60) |

**Khuyến nghị:** nếu phải chọn trong đúng bốn hướng này thì chọn **hướng 2**, thu hẹp thành *"phân loại tế bào lão hóa trong TME từ scRNA-seq, với split gom nhóm theo bệnh nhân/dataset và một tập test độc lập nguồn"*. **Nhưng** khuyến nghị thật của tôi là mang bốn hướng này tới buổi tuần 6 **cùng với** ứng viên A hoặc B của khảo sát 02/10, và để GVHD chọn — vì A và B đã qua cổng dữ liệu, bốn hướng này thì chưa.

---

## 1. Hướng 1 — Đồng hồ sinh học & đánh giá nguy cơ ung thư (Damage/Aging Clocks)

### 1.1. Một việc phải làm rõ trước: `tDamAge` không tra được

Tra `"tDamAge"` không trả về bất kỳ bài báo, repo hay dataset nào `[đã thử — search không có kết quả khớp]`. Ba khả năng, chưa phân biệt được:

- tên viết tắt nội bộ của một bài rất mới hoặc một preprint GVHD đọc được mà công cụ tìm kiếm chưa index;
- tên GVHD tự đặt khi mô tả ý tưởng, không phải tên một công cụ đã có;
- nhớ sai một tên gần giống.

**Việc phải làm:** đây là **câu hỏi số một cho GVHD về hướng này** — xin thầy tên bài báo hoặc DOI của tDamAge. Không có nó thì toàn bộ phần "có công cụ đo tổn thương phiên mã để dựa vào" là **giả định chưa kiểm**.

Những gì **tra được** trong cùng địa hạt, để thấy hướng này có thật dù tDamAge chưa xác định: tổn thương phiên mã theo tuổi là một dòng nghiên cứu sống — RNA polymerase bị stalling định hình transcriptome khi lão hóa `[chưa kiểm]` ([Nat Genet 2023](https://www.nature.com/articles/s41588-022-01279-6)), mất cân bằng biểu hiện theo **chiều dài gene** `[chưa kiểm]` ([Nat Aging 2022](https://www.nature.com/articles/s43587-022-00317-6), [Trends Genet 2024](https://www.cell.com/trends/genetics/fulltext/S0168-9525(24)00027-1)), và thay đổi phiên mã + bộ gene ở não người già đo ở mức đơn bào `[chưa kiểm]` ([Nature 2025](https://www.nature.com/articles/s41586-025-09435-8)). Phía clock thì có Pasta (age-shift transcriptomic clock) `[chưa kiểm]` ([bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.06.04.657785v2.full)) và một bài nối trực tiếp hai đầu mà hướng này muốn nối — entropy phiên mã theo mô, dùng để **dự đoán tiến triển ung thư** `[chưa kiểm]` ([bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.06.29.662218v1.full)). Hallmark phiên mã của lão hóa và tử vong ở động vật có vú cũng vừa lên Nature `[chưa kiểm]` ([Nature 2026](https://www.nature.com/articles/s41586-026-10542-3)).

### 1.2. Bài toán — vào gì, ra gì

**Vào:** một profile biểu hiện gene của một mẫu mô (bulk RNA-seq hoặc single-cell), có thể kèm các biến cố cấu trúc đọc ra từ RNA (đột biến kết thúc sớm, tandem duplication, gene fusion). **Ra:** một số đo "tốc độ lão hóa phân tử" của mô đó, và/hoặc một điểm nguy cơ chuyển dạng ác tính.

**Chú ý:** đây là bài toán **hồi quy (hoặc sinh tồn) trên vector biểu hiện của một mẫu**, không phải phân loại cửa sổ quanh một residue. Khác hẳn mọi thứ sinh viên đã dựng cho RTK–ATP.

### 1.3. Vì sao cần nghiên cứu

Lập luận mạnh và thật: lão hóa là yếu tố nguy cơ lớn nhất của phần lớn ung thư, nhưng **tuổi thời gian không phải tuổi sinh học** — hai người 60 tuổi có nguy cơ rất khác nhau. Một thước đo tổn thương phân tử theo mô sẽ cho phép phân tầng nguy cơ sớm hơn tuổi. Framing này tốt cho phần mở đầu, và khảo sát 02/10 cũng nói đúng điều đó: **cách dùng duy nhất đúng của aging clock trong luận văn này là làm framing ở mở đầu, không phải làm task**.

### 1.4. History research — phân nhóm theo phương pháp

| Nhóm phương pháp | Công trình tiêu biểu | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. Clock methylation (epigenetic)** | Horvath, PhenoAge, GrimAge; DeepStrataAge (12.234 CpG × 29.167 người) `[chưa kiểm]` | Chuẩn mực của field, rất chính xác về tuổi | **Dữ liệu cohort sau đơn xin**; đầu vào là beta value, không phải chuỗi |
| **2. Clock phiên mã** | Pasta `[chưa kiểm]`; clock transcriptome gần ngưỡng chính xác lý thuyết `[chưa kiểm]`; hallmark phiên mã của lão hóa/tử vong `[chưa kiểm]` | Dữ liệu GEO/GTEx công khai hơn | Nhiễu theo batch rất nặng; nhãn là tuổi người, không phải tuổi mô |
| **3. Clock proteomic theo cơ quan** | Clock huyết tương theo cơ quan trên UK Biobank n = 43.616 `[chưa kiểm]` | Diễn giải lâm sàng tốt | **UK Biobank cần đơn duyệt có phí, xét hàng tháng** — ngoài cửa sổ 8–9 tuần |
| **4. Chỉ số tổn thương/entropy phiên mã** | Entropy phiên mã theo mô → tiến triển ung thư `[chưa kiểm]`; stalling polymerase `[chưa kiểm]`; mất cân bằng theo chiều dài gene `[chưa kiểm]` | **Đúng chỗ hướng này muốn đứng**, và chưa đông | Phần lớn là preprint; định nghĩa "tổn thương" chưa thống nhất → **không có benchmark chung** |
| **5. Nối clock với nguy cơ ung thư** | tDamAge `[không tra được]` | — | **Chưa xác định được công trình nền** |

**Điểm đề tài dự kiến cải thiện:** chưa xác định được, vì nhóm 5 chưa tra được. Đây là một **lỗ trong lập luận**, không phải một khoảng trống nghiên cứu.

### 1.5. Dữ liệu — cổng chặn

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| GEO / GTEx (biểu hiện theo mô, có tuổi) | Công khai | Nhãn là **tuổi người hiến**, không phải tuổi mô; batch effect xuyên dataset |
| TCGA (bulk RNA-seq ung thư) | Tầng mở công khai; tầng lâm sàng chi tiết **controlled-access** | Không có nhãn "tốc độ lão hóa" |
| UK Biobank | **Đơn duyệt + phí, xét hàng tháng** | Khảo sát 02/10 đã kết luận: **không thể trong 8–9 tuần** |
| Tập test độc lập cho "nguy cơ chuyển dạng ác tính" | **Không tìm được** | Đây là cổng rớt nặng nhất |

### 1.6. Năm tiêu chí

| Tiêu chí | Đánh giá | Lý do |
|---|---|---|
| 1. Tính mới | **Trung bình–cao** | Nối clock với nguy cơ ung thư thì chưa đông, nhưng cũng chưa xác định được bài nền để nói "cải thiện ở đâu" |
| 2. Cải tiến phương pháp | **Thấp** | Không có mCNN/cửa sổ nào để cải tiến. Đầu vào là vector/bảng → về kiến trúc là MLP, gradient boosting, hoặc VAE |
| 3. Phương pháp mới | **Thấp** | PLM không áp dụng được: **không có chuỗi amino acid nào trong bài toán này** |
| 4. XAI | **Trung bình** | SHAP trên feature gene thì làm được, nhưng đó đúng là dạng SHAP-chọn-đặc-trưng mà GVHD đã có tiền lệ (BERT-Promoter 2022) → khó gọi là mới |
| 5. Web app | **Cao** | Upload bảng biểu hiện → trả điểm tuổi sinh học. Dễ làm, demo tốt |

**Tổng: đạt rõ 1 và 5, thiếu 2 và 3** — đúng kết luận khảo sát 02/10 đã nêu khi loại aging clock, và lý do đó **không thay đổi** khi đổi từ methylation clock sang damage clock, vì lý do loại là **hình dạng đầu vào**, không phải chủ đề.

### 1.7. Nếu vẫn muốn làm, phạm vi tối thiểu khả thi

Phiên bản thu hẹp duy nhất tôi thấy đứng được: **một task hồi quy tuổi trên GTEx/GEO cho 2–3 mô, cộng một phân tích "điểm tổn thương phiên mã có tách được mô ung thư với mô lành kề cận trong TCGA hay không"**, và **nói thẳng là không dùng PLM**. Phải chấp nhận trước rằng tiêu chí 2–3 sẽ không đạt, và phải hỏi GVHD xem như vậy có chấp nhận được không.

---

## 2. Hướng 2 — Phát hiện tế bào lão hóa trong khối u (Cellular Senescence in TME)

**Hướng khả thi nhất trong bốn hướng.** Nhưng nó đang gộp **hai bài toán khác nhau hoàn toàn** trong một câu, và phải chọn một.

### 2.1. Hai nhánh, phải chọn một

**Nhánh ảnh (hình thái nhân tế bào).** Vào: ảnh nhân tế bào (DAPI/Hoechst). Ra: nhãn senescent / không. Đây là nhánh **đã có bài nền rõ và mạnh**: hình thái nhân là biomarker deep learning của senescence, công bố trên Nature Aging 2022 `[chưa kiểm]` ([s43587-022-00263-3](https://www.nature.com/articles/s43587-022-00263-3)), kèm một bài companion "dự đoán senescence xuyên mô và xuyên loài" `[chưa kiểm]` ([s43587-022-00265-1](https://www.nature.com/articles/s43587-022-00265-1)); sau đó có thêm phát hiện senescence bằng ML trên đặc trưng nhân `[chưa kiểm]` ([Nat Commun 2024](https://www.nature.com/articles/s41467-024-45421-w)) và nuclear morphometrics + ML cho các trạng thái senescence động theo tuổi `[chưa kiểm]` ([Nat Commun 2025](https://www.nature.com/articles/s41467-025-60975-z)).

**Nhánh phiên mã đơn bào (scRNA-seq).** Vào: vector biểu hiện của một tế bào. Ra: điểm senescence. Nhánh này **cũng đã có công cụ**: DeepScence (phát hiện tế bào senescent ở mức đơn bào và không gian, Cell Genomics 2026) `[chưa kiểm]` ([Cell Genomics](https://www.cell.com/cell-genomics/fulltext/S2666-979X(25)00291-5), [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.11.21.568150v3.full)) và SenCID (Cell Metabolism 2024, nhận diện senescence đơn bào kèm tính không đồng nhất và quỹ đạo) `[chưa kiểm]` ([Cell Metab](https://www.cell.com/cell-metabolism/fulltext/S1550-4131(24)00088-3)). Có cả một review 2025 về AI trong nghiên cứu senescence `[chưa kiểm]` ([Aging Advances](https://journals.lww.com/aa/fulltext/2025/12000/artificial_intelligence_in_cellular_senescence.4.aspx)).

**Nói thẳng về mức đông đúc:** cả hai nhánh **đều đã có 2–4 công trình trên tạp chí tốt trong 2022–2026**. Đây **không phải** niche trống như ứng viên A (substrate SIRT theo isoform). Đóng góp phải cụ thể hơn là "dùng DL để phân loại tế bào lão hóa".

### 2.2. Bài toán — vào gì, ra gì (phiên bản tôi khuyên)

**Vào:** profile biểu hiện của một tế bào trong khối u (scRNA-seq), lấy từ các dataset TME công khai. **Ra:** nhãn nhị phân senescent / không, cộng một **cảnh báo miền áp dụng** (tế bào này có giống phân phối huấn luyện hay không).

Lý do chọn nhánh scRNA-seq thay vì nhánh ảnh: dataset scRNA-seq khối u trên GEO **tải được ngay, không cần đơn xin**, trong khi bộ ảnh nhân của các bài Nature Aging thường đi kèm điều kiện truy cập và dung lượng lớn `[chưa kiểm — chưa thử link]`.

### 2.3. Vì sao cần nghiên cứu

Lập luận thật và dễ nói: tế bào senescent trong khối u **có hai mặt** — chúng chặn tăng sinh, nhưng SASP của chúng lại thúc đẩy viêm và kháng trị. Biết **ở đâu, bao nhiêu** tế bào senescent trong một khối u là điều kiện để nói liệu senolytic có nên dùng cho bệnh nhân đó. Và không có marker đơn lẻ nào đủ: senescence là **trạng thái không có một dấu chuẩn vàng**, nên bài toán vốn dĩ là bài toán tổng hợp nhiều tín hiệu — tức đúng chỗ ML có lý do tồn tại.

### 2.4. History research — phân nhóm theo phương pháp

| Nhóm phương pháp | Công trình tiêu biểu | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. Chữ ký gene đếm tay** | SenMayo, CellAge, các panel SASP | Minh bạch, dùng được ngay, được chấp nhận rộng | Chỉ là tổng điểm; không hiệu chuẩn; không xử lý được tính không đồng nhất giữa các kiểu senescence |
| **2. DL trên hình thái nhân** | Nature Aging 2022 ×2 `[chưa kiểm]`; Nat Commun 2024, 2025 `[chưa kiểm]` | Đo trực tiếp, không phụ thuộc marker; đã xuyên mô và xuyên loài | **Modality ảnh** — rời hoàn toàn khỏi lane trình tự của GVHD; dữ liệu ảnh nặng |
| **3. Mô hình đơn bào chuyên dụng** | DeepScence `[chưa kiểm]`; SenCID `[chưa kiểm]` | **Đối thủ trực tiếp**, đã công bố ở tạp chí mạnh, có code | Chủ yếu huấn luyện trên tế bào in vitro rồi áp sang mô/khối u — **đây là khe hở** |
| **4. ML trên transcriptome bulk/in vitro** | Một bài ML nhận diện senescence trên transcriptome tế bào người in vitro `[chưa kiểm]` ([PMC12181610](https://pmc.ncbi.nlm.nih.gov/articles/PMC12181610/)) | Dữ liệu sạch | In vitro → khoảng cách miền tới TME rất lớn |
| **5. Phân loại protein liên quan senescence từ chuỗi** | SenSeqNet (= **ứng viên E** của khảo sát 02/10) | Đúng lane PLM của GVHD | Bài toán khác (mức protein, không phải mức tế bào); và khảo sát 02/10 **đã tự đo được rò rỉ nặng** trong bản v1 `[tự đo]` |

**Điểm đề tài dự kiến cải thiện — ba ứng viên, xếp theo độ chắc:**

1. **Khoảng cách miền in vitro → khối u.** Các công cụ hiện có huấn luyện phần lớn trên senescence gây ra in vitro. Một đóng góp thật: **đo xem chúng rơi bao nhiêu khi áp lên TME thật, rồi dựng một bộ phân loại có cảnh báo miền áp dụng**. Đây là chỗ sinh viên **tái dùng được đúng tài sản đã có từ RTK–ATP** (giao thức kiểm soát rò rỉ + tín hiệu miền áp dụng) mà không mang theo cái bẫy "đề tài chỉ là kiểm toán".
2. **Split gom nhóm theo bệnh nhân/dataset.** Cùng một lỗi đã thấy ở SenSeqNet ở mức gene, ở đây là mức bệnh nhân: tế bào từ cùng một bệnh nhân nằm cả trong train và test thì chỉ số bị lạm phát. **Chưa kiểm** các công cụ hiện có có làm đúng điều này hay không — **đây là việc tra cứu giá trị nhất trước tuần 6**.
3. **Tính không đồng nhất của kiểu senescence.** Senescence do oncogene, do trị liệu, do telomere — các công cụ hiện có phần lớn cho một điểm duy nhất. Phân loại đa nhãn theo kiểu là một bài toán sạch, nhưng **chưa kiểm có nhãn công khai nào đủ cho nó**.

### 2.5. Dữ liệu — cổng chặn

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| scRNA-seq khối u trên GEO | Công khai, tải được | **Chưa thử link trong phiên này** |
| SenNet (consortium) | Có trang tài nguyên công nghệ `[chưa kiểm]` ([SenNet](https://sennetconsortium.org/technology-resources/)) | Chưa kiểm điều kiện truy cập |
| CellAge / GenAge (HAGR) | **Tải được, không đăng ký** — `cellAge.zip` 21.540 B / 866 gene `[tự đo 02/10]` | Dùng làm nhãn gene, không phải nhãn tế bào |
| Code + nhãn của DeepScence / SenCID | `[chưa kiểm]` | **Phải kiểm ngay**: có repo không, có nhãn benchmark không |
| **Tập test độc lập** | **Chưa xác định** | Cổng quyết định. Nguồn khả dĩ nhất: một dataset khối u của **một trung tâm khác**, giữ nguyên ngoài huấn luyện |

### 2.6. Năm tiêu chí

| Tiêu chí | Đánh giá | Lý do |
|---|---|---|
| 1. Tính mới | **Trung bình** | Chủ đề đã có 3–4 công cụ. Tính mới phải nằm ở **góc độ** (miền áp dụng, split theo bệnh nhân), không ở bài toán |
| 2. Cải tiến phương pháp | **Trung bình** | Có đường đi (ví dụ hiệu chuẩn + từ chối dự đoán ngoài miền), nhưng **không phải đường mCNN** — dữ liệu không có trục chuỗi để chạy cửa sổ |
| 3. Phương pháp mới | **Trung bình** | scRNA-seq có họ foundation model riêng (scGPT, Geneformer…) — dùng cái đó là "phương pháp mới" hợp lý, **nhưng đó là một field GVHD không có bài nào**, nên sinh viên tự chịu phần kỹ thuật |
| 4. XAI | **Cao** | Gene đóng góp vào điểm senescence đối chiếu được với chữ ký đã biết (SenMayo) → **giải thích kiểm chứng được**, không trang trí |
| 5. Web app | **Cao** | Upload một ma trận đếm → trả điểm senescence theo từng tế bào + cảnh báo miền áp dụng. Rõ ràng, có người dùng thật |

**Tổng: đạt 4 và 5 mạnh, 1–3 ở mức trung bình.** Khá hơn hướng 1 và 3, kém hơn ứng viên A của khảo sát 02/10 (A đạt rõ cả năm).

### 2.7. Rủi ro và cổng dừng

- **Rủi ro 1 — nhãn senescence không có chuẩn vàng.** Phải nói trung thực: nhãn là *proxy* (chữ ký gene, hoặc nhãn của chính DeepScence/SenCID). Nói "phát hiện tế bào lão hóa" mà nhãn là đầu ra của một công cụ khác là **đòn tấn công hiển nhiên nhất**.
- **Rủi ro 2 — đối thủ ở tạp chí rất mạnh.** Cell Genomics và Cell Metabolism. Không được đóng khung là "vượt SOTA".
- **Rủi ro 3 — compute.** scRNA-seq hàng trăm nghìn tế bào; một foundation model đơn bào sẽ không chạy nổi trên CPU. **Phải xác nhận nguồn GPU trước khi cam kết** (câu 6 trong danh sách câu hỏi GVHD).
- **Cổng dừng đề xuất:** nếu đến **hết tuần 7** không xác định được một dataset khối u độc lập nguồn làm tập test, chuyển sang ứng viên A hoặc B của khảo sát 02/10.

---

## 3. Hướng 3 — Thiết kế tân kháng nguyên dùng chung bằng generative PLM + RAG

**Khuyên không chọn.** Khảo sát 02/10 đã loại nhánh neoantigen qua bốn cổng; hướng này **cộng thêm** hai vấn đề mới của phần sinh (generative). Tôi giữ nguyên kết luận cũ và nói rõ hai cái mới.

### 3.1. Bài toán — và vì sao chính cách phát biểu đã là vấn đề

**Vào:** một tập đột biến tái phát (ví dụ các hotspot thường gặp ở bệnh nhân lớn tuổi). **Ra:** các chuỗi peptide/tân kháng nguyên *được sinh ra* kèm dự đoán khả năng trình diện và sinh miễn dịch.

Vấn đề cốt lõi, nói một câu: **một chuỗi được sinh ra thì không có nhãn thật.** Mọi bài toán trong khảo sát 02/10 đi qua cổng dữ liệu đều là bài toán **phân loại trên nhãn thực nghiệm đã có**. Ở đây, đầu ra là chuỗi mới → đánh giá nó chỉ còn ba cách, và cả ba đều yếu ở mức luận văn:

1. **Chấm bằng một predictor khác** (NetMHCpan, v.v.) → vòng tròn: mô hình sinh được tối ưu theo đúng thứ dùng để chấm nó.
2. **Đối chiếu với epitope đã kiểm chứng** (IEDB) → khi đó bài toán thật là **truy hồi**, không phải thiết kế: nếu chuỗi sinh ra phải trùng với epitope đã biết mới được coi là tốt, thì sinh ra để làm gì?
3. **Thực nghiệm** → ngoài phạm vi luận văn CNTT hoàn toàn.

Đây là **cổng rớt mới, chưa có trong khảo sát 02/10**, và nó độc lập với mọi lý do cũ.

### 3.2. Bốn cổng cũ, vẫn đứng (dẫn lại [khảo sát 02/10 §10](aging-cancer-deep-dive.md))

- **Cổng định vị.** PLM + multi-window CNN cho neoantigen **đã được chính nhóm Prof Ou công bố**: DeepNeoAG (2024) và NeoGen-BC (09/09/2026). Pitch hướng này vào tháng 10/2026 là đọc lại abstract của NeoGen-BC cho một giáo sư đồng tác giả thường xuyên với tác giả cuối của nó.
- **Cổng hướng dẫn.** GVHD **không có bài cancer/neoantigen nào** trong danh mục 14 bài `[tự đo 02/10]`. Sinh học MHC, nhận diện tế bào T, và điều gì làm một nhãn immunogenicity đáng tin — đúng chỗ cần người hướng dẫn nhất, và đúng chỗ không có.
- **Cổng đóng góp giao thức — đã bị chiếm.** Immunity 2023 đã reprocess 131 bệnh nhân, 46.017 SNV, 1.781.445 neo-peptide, 178 neo-peptide immunogenic, và phát hành ma trận mở **tự tuyên bố mục đích là để benchmark các thuật toán đi sau** `[abstract]`.
- **Cổng chỉ số.** Trên benchmark sạch ITSNdb, **bảy predictor đã công bố có ROC AUC 0,52–0,60**, và phương pháp xếp hạng tốt nhất tạo **100% (297) false positive trên TESLA** `[toàn văn]`. Sinh viên không thể biết mình đang cạnh tranh với con số nào.

### 3.3. Thêm một cổng nữa: "shared neoantigen ở bệnh nhân lớn tuổi"

Phần "dùng chung" và phần "lớn tuổi" **kéo ngược nhau về mặt dữ liệu**. Shared neoantigen là các hotspot tái phát (KRAS G12D, TP53 R175H…) — số lượng **rất nhỏ**, vài chục đến vài trăm, nên không đủ để huấn luyện. Còn phân tầng theo tuổi thì cần **metadata tuổi trên từng bệnh nhân trong dataset immunogenicity**, và `[chưa kiểm]` liệu các dataset đó có công bố tuổi hay không. Nếu không có, phần "bệnh nhân lớn tuổi" chỉ còn là một câu trong phần mở đầu, không phải một phần của bài toán.

### 3.4. Năm tiêu chí

| Tiêu chí | Đánh giá |
|---|---|
| 1. Tính mới | **Thấp về định vị** — đúng lane nhóm Prof Ou vừa công bố tháng 9/2026 |
| 2. Cải tiến phương pháp | Trung bình, nhưng **không đo được** (xem 3.1) |
| 3. Phương pháp mới | Cao trên giấy (generative PLM + RAG), nhưng **RAG cũng đã là lane của nhóm** (RAG-msCNN, RTK_RAG) |
| 4. XAI | **Thấp** — giải thích một chuỗi được sinh ra nghĩa là gì? |
| 5. Web app | Cao về hình thức |

### 3.5. Chỗ duy nhất còn mở trong nhánh này, nói ra cho công bằng

Mọi negative trong các dataset neoantigen là "chưa được chứng minh là immunogenic", không phải "đã chứng minh là không" — chính tập validation của ITSNdb có **113/120 negative thiếu xác nhận binding** `[toàn văn]`. Tức đây là bài toán **positive-unlabelled learning mà cả field đang xử lý như phân loại nhị phân có giám sát**, và khảo sát 02/10 **không tìm được bài nào đóng khung nó là PU learning**. Đó là một ý tưởng thật — nhưng nó là **bài toán phân loại**, không phải thiết kế bằng mô hình sinh, và nó không cứu được cổng định vị.

---

## 4. Hướng 4 — RAG hỗ trợ suy luận cơ chế đa tầng (Explainable Multi-omics AI)

Hướng này **hấp dẫn nhất về sản phẩm** và **yếu nhất về tính đo được**. Nó thực chất là **hai đề tài ghép lại**.

### 4.1. Hai nửa, và nửa nào là vấn đề

**Nửa A — dự đoán.** ML dự đoán đáp ứng thuốc hoặc đột biến sinh ung từ dữ liệu omics. Nửa này **đo được** (AUC, correlation), nhưng khảo sát 02/10 đã loại nó: *DTI/drug response trong oncology — **240 bản ghi PubMed 2024–2026**, đông nhất trong mọi task đã xét; và URL bulk download của GDSC trả **HTTP 410 Gone*** `[đã thử link 02/10]`.

**Nửa B — giải thích.** RAG truy hồi knowledge graph + y văn để tự động giải thích vì sao tổ hợp biến đổi gene gây kháng thuốc. **Đây là nửa không đo được**, và đó là vấn đề trung tâm: làm sao chứng minh một lời giải thích là **đúng**, chứ không chỉ là **nghe hợp lý**?

Ba cách đánh giá thường gặp, và điểm yếu của từng cách:
- **Con người chấm** → cần chuyên gia ung thư phân tử, nhiều người, có thước đo đồng thuận. Ngoài tầm một luận văn.
- **Đối chiếu với cơ chế đã biết** (ví dụ các mục trong CIViC/OncoKB) → khi đó bài toán là **truy hồi có đáp án**, đo được bằng recall@k — **và đây chính là phiên bản khả thi duy nhất của hướng này**.
- **Chấm bằng LLM khác** → không đáng tin ở mức luận văn tin sinh, và GVHD gần như chắc chắn sẽ hỏi lại.

### 4.2. Mức đông đúc — nhánh này đang rất nóng

Phải nói trước với GVHD, vì đây là nhánh dễ bị trùng nhất trong năm 2025–2026: KG + LLM cho hỏi đáp pan-cancer `[chưa kiểm]` ([GigaScience](https://academic.oup.com/gigascience/article/doi/10.1093/gigascience/giae082/7943459)), Medical Graph RAG (ACL 2025) `[chưa kiểm]` ([ACL](https://aclanthology.org/2025.acl-long.1381.pdf)), agentic medical knowledge graph (EMNLP 2025 Findings) `[chưa kiểm]` ([ACL](https://aclanthology.org/2025.findings-emnlp.679.pdf)), mô hình AI giải thích được cho tổ hợp trị liệu `[chưa kiểm]` ([PMC12564325](https://pmc.ncbi.nlm.nih.gov/articles/PMC12564325/)), và tổng quan LLM trên omics `[chưa kiểm]` ([ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2211383525007129)). **Đây là nhánh đông nhất trong bốn hướng.**

### 4.3. History research — phân nhóm theo phương pháp

| Nhóm phương pháp | Đại diện | Ưu điểm | Hạn chế |
|---|---|---|---|
| **1. ML dự đoán đáp ứng thuốc từ omics** | Các mô hình trên GDSC/CCLE/DepMap | Đo được rõ ràng | **240 bài 2024–26**; GDSC bulk download **410 Gone** `[đã thử link 02/10]` |
| **2. Mô hình visible-neuron / pathway-informed** | Các mô hình gắn neuron với pathway | Giải thích có cấu trúc sinh học | Kiến trúc nặng; giải thích vẫn là post-hoc |
| **3. KG embedding / link prediction** | KG sinh y học | Đo được bằng recall@k | Giải thích là một đường đi trong đồ thị, không phải một lập luận |
| **4. LLM + RAG trên y văn/KG** | Medical Graph RAG, KG-thought `[chưa kiểm]` | Đọc được, đúng kỳ vọng "tự động giải thích" | **Không có benchmark chuẩn cho chất lượng giải thích**; rủi ro bịa |
| **5. XAI trên mô hình omics** | SHAP/IG trên feature gene | Dễ làm | Dễ thành trang trí nếu không đối chiếu nguồn độc lập |

### 4.4. Năm tiêu chí

| Tiêu chí | Đánh giá | Lý do |
|---|---|---|
| 1. Tính mới | **Thấp–trung bình** | Nhánh đông nhất trong bốn hướng |
| 2. Cải tiến phương pháp | **Thấp nếu không đo được** | Không thể nói "cải tiến" khi không có thước đo |
| 3. Phương pháp mới | Trung bình | RAG **đã là lane của nhóm** (RAG-msCNN, RTK_RAG) → khó bán là mới cho chính GVHD |
| 4. XAI | **Cao trên giấy, nhưng đây chính là chỗ cần chứng minh** | Nếu không đổi thành bài toán truy hồi có đáp án thì không chứng minh được |
| 5. Web app | **Cao nhất trong bốn hướng** | Đây là thứ nhìn giống một sản phẩm thật nhất |

### 4.5. Phiên bản khả thi duy nhất, nếu chọn hướng này

Đổi phát biểu từ *"RAG tự động giải thích"* sang *"**truy hồi bằng chứng cơ chế có đánh giá định lượng**"*: cho một tổ hợp (gene + biến thể + thuốc), hệ thống trả về các mục bằng chứng từ KG/y văn; đánh giá bằng **recall@k và precision@k so với các mục đã curate trong CIViC/OncoKB** làm đáp án. Lúc đó hướng này **có thước đo**, và phần sinh văn bản chỉ là lớp trình bày trên một hệ truy hồi đã đo được. Nhưng phải kiểm `[chưa kiểm]` điều kiện dùng lại dữ liệu curate của CIViC/OncoKB, và phải chấp nhận rằng đây **không còn là** đề tài "giải thích cơ chế" nữa.

---

## 5. Bảng so sánh bốn hướng

| | **1. Damage/Aging clock** | **2. Senescence trong TME** | **3. Tân kháng nguyên generative** | **4. RAG giải thích đa tầng** |
|---|---|---|---|---|
| Hướng | aging | aging ∩ cancer | cancer | cancer |
| Đầu vào | Vector biểu hiện / bảng | Ảnh **hoặc** vector đơn bào | Chuỗi peptide | Bảng omics + đồ thị + văn bản |
| **Có trục chuỗi amino acid?** | **Không** | **Không** | Có | Không |
| **Dùng được lane PLM/mCNN của GVHD?** | **Không** | Không | Có — **nhưng đã bị chiếm** | Không |
| Dữ liệu công khai | GEO/GTEx có; UK Biobank **không** (đơn duyệt) | GEO scRNA-seq **có** `[chưa thử link]` | Có qua figshare Immunity 2023 `[đã thử link 02/10]` | GDSC bulk **410 Gone** `[đã thử link 02/10]` |
| **Tập test độc lập** | **Không xác định được** | **Chưa xác định** — phải tự dựng theo trung tâm | Có (TESLA/ITSNdb) **nhưng AUC 0,52–0,60** | Không cho phần giải thích |
| Mức đông đúc | Trung bình | **Đã có 3–4 công cụ ở tạp chí mạnh** | Cao + đúng lane Prof Ou | **Đông nhất** |
| Khớp GVHD — phương pháp | **Thấp** | Thấp–trung bình | Cao (nhưng là lane Prof Ou) | Trung bình (RAG đã có) |
| Khớp GVHD — sinh học | Không có bài | Không có bài (gần SirtSAGE về chủ đề aging) | **Không có bài cancer** | Không có bài |
| Khả thi 8–9 tuần | Trung bình | **Cao** (nếu chọn scRNA-seq) | Thấp | Trung bình (nếu đổi thành truy hồi) |
| Tiêu chí đạt rõ | 1, 5 | **4, 5** (1–3 trung bình) | 5 | 5 |
| Rủi ro lớn nhất | **Không có trục chuỗi → tiêu chí 2–3 không đạt**; tDamAge không tra được | Nhãn không có chuẩn vàng; đối thủ ở Cell Genomics / Cell Metabolism | **Chuỗi sinh ra không có nhãn thật** + định vị | **Phần giải thích không đo được** |

### So với sáu ứng viên A–F của khảo sát 02/10

Nói thẳng, vì đây là điều quan trọng nhất trong tài liệu này: **ứng viên A (substrate SIRT theo isoform) và B (site phospho theo nhóm kinase) đều đạt rõ cả năm tiêu chí và đều đã qua cổng dữ liệu** — A có file nhãn 6.801 site đã tải về và đếm được `[tự đo]`, B có benchmark non-homologous do chính dbPTM công bố `[toàn văn]`. **Không hướng nào trong bốn hướng mới làm được cả hai việc đó.** Lý do rất hệ thống, và đã được nêu trong khảo sát 02/10: ba trong bốn hướng mới **không có trục chuỗi amino acid**, nên pipeline cửa sổ-residue + PLM mà sinh viên đã dựng và GVHD hiểu rõ **không dùng lại được**, và hai tiêu chí 2–3 mất theo.

---

## 6. Khuyến nghị và việc cần làm trước tuần 6

**Khuyến nghị:** mang **cả hai nhóm** tới buổi tuần 6 và để GVHD chọn, trình bày theo đúng ba bước ở mục 3 biên bản:

1. **Nhóm đã qua cổng dữ liệu:** ứng viên A hoặc B của [khảo sát 02/10](aging-cancer-deep-dive.md). Đây là nhóm tôi khuyên.
2. **Trong bốn hướng GVHD gợi ý:** **hướng 2**, thu hẹp thành *"phân loại tế bào lão hóa trong vi môi trường khối u từ scRNA-seq, có cảnh báo miền áp dụng, đánh giá bằng split gom nhóm theo bệnh nhân và một tập test độc lập nguồn"*. Phương án hai: **hướng 4** đổi thành bài toán truy hồi bằng chứng có đáp án (4.5).

**Cách nói ở buổi gặp, một câu:** "Em đã phân tích cả bốn hướng thầy gợi ý theo đúng khung thầy yêu cầu. Ba trong bốn hướng có đầu vào không phải chuỗi amino acid, nên không dùng lại được pipeline PLM–mCNN, và em e là tiêu chí 2 và 3 sẽ khó đạt. Hướng 2 thì khả thi, nhưng đã có 3–4 công cụ. Em xin thầy cho ý kiến giữa hướng 2 và hai ứng viên em đã kiểm được dữ liệu."

**Năm việc phải làm trước tuần 6, xếp theo giá trị:**

1. **Hỏi GVHD tên bài báo / DOI của `tDamAge`** — không tra được, và nó là nền của hướng 1.
2. **Thử link và kiểm code + nhãn của DeepScence và SenCID**, và kiểm xem chúng **có split theo bệnh nhân hay không**. Đây là việc tra cứu giá trị cao nhất còn lại: nếu chúng không làm, hướng 2 có một đóng góp cụ thể ngay.
3. **Chọn một dataset scRNA-seq khối u công khai, tải thật, đếm số tế bào và số bệnh nhân** — y hệt cách khảo sát 02/10 đã làm với ứng viên A. Không có bước này thì "khả thi" chỉ là phỏng đoán.
4. **Xác nhận nguồn GPU** (câu 6 trong [danh sách câu hỏi GVHD](aging-cancer-deep-dive.md#13-câu-hỏi-đặt-cho-gvhd-ở-tuần-6)). Hướng 2 nhánh foundation model đơn bào **không chạy trên CPU**.
5. **Chuẩn bị một trang brief sinh học** cho hướng được chọn, vì GVHD không có bài ở ba trong bốn hướng — sinh viên là người phải mang phần sinh học tới.

**Hai câu hỏi mới cho GVHD, thêm vào danh sách ở [khảo sát 02/10 §13](aging-cancer-deep-dive.md):**

- **Với hướng 1 và 4, thầy có chấp nhận một đề tài không dùng PLM/mCNN không?** Nếu không, hai hướng đó rụng vì kiến trúc, không vì chủ đề.
- **Với hướng 4, thầy đo chất lượng "giải thích tự động" bằng gì?** Nếu không có thước đo thì em xin đổi thành truy hồi bằng chứng có đáp án.

---

## 7. Những điều tài liệu này **chưa** kiểm chứng

- **`tDamAge`: không tra được bất kỳ nguồn nào.** Mọi phân tích hướng 1 đặt trên giả định rằng nó là một công cụ đo tổn thương phiên mã.
- **Phiên này chưa tải file dữ liệu nào.** Mọi trạng thái truy cập trong tài liệu này là `[chưa kiểm]`, trừ các dòng dẫn lại khảo sát 02/10 (`[tự đo]`, `[đã thử link]`). Cụ thể: **chưa thử link** GEO scRNA-seq, SenNet, DeepScence, SenCID, CIViC, OncoKB.
- **Chưa đọc toàn văn bài nào trong phiên này.** Các bài Nature Aging / Nat Commun / Cell Genomics / Cell Metabolism ở trên chỉ có từ tiêu đề và snippet tìm kiếm.
- **Chưa biết các công cụ senescence hiện có split theo bệnh nhân hay không** — đây là trụ chính của đóng góp đề xuất cho hướng 2, và nó **chưa được kiểm**.
- **Chưa kiểm** liệu các dataset immunogenicity có công bố tuổi bệnh nhân hay không (ảnh hưởng phần "lớn tuổi" của hướng 3).
- **Chưa kiểm** điều kiện dùng lại dữ liệu curate của CIViC/OncoKB cho phiên bản khả thi của hướng 4.
- Bốn hướng này là **cách sinh viên ghi lại lời GVHD**, không phải văn bản GVHD viết. Nếu cách ghi lệch so với ý thầy thì phân tích này lệch theo.
