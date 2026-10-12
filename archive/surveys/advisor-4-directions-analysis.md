# Phân tích 4 hướng GVHD gợi ý (giao thoa Cancer & Aging)

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../DECISIONS.md).

**Ngày 06/10/2026.** Phân tích theo đúng khung trình bày GVHD yêu cầu ở [biên bản lần 1](../../project/meetings/2026-10-02-session-01/minutes.md) (mục 2: bài toán / lý do / phần sẽ giải quyết; mục 3: history research ba bước; mục 4: năm tiêu chí), cộng hai cổng chặn mà biên bản nói phải kiểm sớm nhất: **dữ liệu công khai có tập test độc lập hay không** và **khả thi trong 8–9 tuần**.

> **Mức kiểm chứng** — giữ đúng quy ước của [khảo sát sâu 02/10/2026](aging-cancer/aging-cancer-deep-dive.md): `[toàn văn]` · `[abstract]` · `[đã thử link]` · `[tự đo]` · `[chưa kiểm]` (chỉ có từ search snippet, **chưa xác nhận ở nguồn gốc**). Phiên này **chưa tự tải file dữ liệu nào**, nên mọi con số dưới đây cao nhất là `[abstract]` hoặc `[chưa kiểm]`, trừ chỗ dẫn lại khảo sát 02/10 đã `[tự đo]`.

---

## 0. Kết luận trước, để đọc phần sau có định hướng

Bốn hướng này **không ở cùng một mức trừu tượng** với sáu ứng viên A–F trong [khảo sát sâu](aging-cancer/aging-cancer-deep-dive.md). A–F là **bài toán** (vào gì, ra gì, nhãn ở đâu). Bốn hướng này là **chủ đề** — mỗi hướng còn phải chọn một bài toán cụ thể bên trong. Đây không phải lỗi của ai: ở mức chủ đề thì cả bốn đều hợp lý; nhưng **không hướng nào trong bốn hướng này, ở dạng đang được phát biểu, đi qua được cổng dữ liệu + 8–9 tuần mà không bị thu hẹp lại**.

Xếp hạng, nói thẳng:

| | Hướng | Phán quyết một dòng |
|---|---|---|
| **1** | **Hướng 2 — phát hiện tế bào lão hóa trong khối u** | ~~Khả thi nhất~~ → **ĐÃ DỪNG ngày 07/10 sau khi chạy trên GSE103322**: không đạt ngưỡng đặt trước, và **điểm SenMayo chủ yếu theo loại tế bào chứ không theo senescence** (70% tế bào dương là fibroblast, tế bào T/B không có tế bào dương nào). Xem [mục 7.5](#75-kết-quả-trên-dữ-liệu-thật-và-phán-quyết-dừng-hướng-2-0710) |
| **2** | **Hướng 4 — RAG giải thích cơ chế đa tầng** | Khả thi về **sản phẩm** (đạt tiêu chí 5 rất tốt), nhưng **phần "giải thích" gần như không đánh giá được định lượng** → tiêu chí 1–2 khó bảo vệ, dễ thành "một con chatbot có citation" |
| **3** | **Hướng 1 — đồng hồ sinh học & nguy cơ ung thư** | **Đã bị loại to tiếng trong khảo sát 02/10 và lý do vẫn đứng:** đầu vào không phải chuỗi amino acid → toàn bộ lineage PLM → mCNN → RAG của GVHD **không áp dụng được**, nên tiêu chí 2 và 3 không đạt được. Thêm nữa, `tDamAge` **không tra được** (xem 1.1) |
| **4** | **Hướng 3 — thiết kế tân kháng nguyên bằng generative PLM + RAG** | **Rủi ro cao nhất, khuyên không chọn.** Ba cổng rớt độc lập nhau: định vị (đúng lane Prof Ou), đánh giá (không có ground truth cho chuỗi sinh ra), và chỉ số (benchmark sạch cho AUC 0,52–0,60) |

**Khuyến nghị ban đầu (06/10), đã bị chính dữ liệu đảo lại ngày 07/10 — đọc [mục 7.5](#75-kết-quả-trên-dữ-liệu-thật-và-phán-quyết-dừng-hướng-2-0710) trước:** nếu phải chọn trong đúng bốn hướng này thì chọn **hướng 2**, thu hẹp thành *"phân loại tế bào lão hóa trong TME từ scRNA-seq, với split gom nhóm theo bệnh nhân/dataset và một tập test độc lập nguồn"*. **Nhưng** khuyến nghị thật của tôi là mang bốn hướng này tới buổi tuần 6 **cùng với** ứng viên A hoặc B của khảo sát 02/10, và để GVHD chọn. **Đính chính 07/10:** trong hai ứng viên đó, **chỉ B qua được cổng tập test độc lập**; A thì chưa (xem gạch đầu dòng dưới). Dù vậy cả hai vẫn ở trên bốn hướng mới về mặt dữ liệu, vì nhãn của chúng là nhãn thực nghiệm đã có.

> **Cập nhật 07/10/2026 sau hai kiểm chứng ở [mục 7](#7-kiểm-chứng-bổ-sung-và-phán-quyết-hướng-2-0710) — xếp hạng không đổi, nhưng hai lý do đổi, và cả hai đều bất lợi cho hướng 2:**
>
> - **Đóng góp đề xuất cho hướng 2 phải viết lại.** Lập luận "các công cụ hiện có không gom nhóm theo bệnh nhân" **đặt trên tiền đề sai**: DeepScence không giám sát (không có split nào), SenePy là chấm điểm theo chữ ký, SenCID có giám sát nhưng huấn luyện trên **bulk in vitro** nên không có bệnh nhân nào trong tập huấn luyện. Khoảng trống thật hẹp hơn: **chưa có mô hình có giám sát nào trên scRNA-seq khối u người với split theo bệnh nhân** — và lý do chưa có là **không có nhãn chuẩn vàng**, tức đúng rủi ro trung tâm của hướng 2.
> - **Không có tiền lệ cùng GVHD cho đầu vào không phải trình tự.** Cả hai luận văn thầy đã hướng dẫn (T1 peptide + ESM-2, T2 tìm kiếm protein + ESM-2) đều là bài toán trên trình tự. **Điều này không còn là cổng loại** sau xác nhận ở gạch đầu dòng dưới, nhưng vẫn là lý do thang đóng góp phải tự dựng.
> - **Cập nhật 07/10 cùng ngày, muộn hơn:** sinh viên xác nhận **GVHD chấp nhận đề tài có đầu vào là ma trận biểu hiện, không bắt buộc chuỗi amino acid** (đã ghi vào [biên bản lần 1 mục 1](../../project/meetings/2026-10-02-session-01/minutes.md)). **Cổng "phải có trục chuỗi amino acid" bỏ.** Hướng 2 nhánh scRNA-seq được lợi nhiều nhất; hướng 1 và 4 **vẫn rụng vì các cổng khác** (tDamAge không tra được và không có tập test độc lập cho nguy cơ chuyển dạng; phần giải thích không đo được). Điều **không đổi**: tiêu chí 2 và 3 vẫn phải tự lập luận, vì thang đối chứng của T1 không chuyển sang được.
> - **Tin tốt, áp dụng cho mọi hướng:** mức thực tế của tiêu chí 2 là **một thang đối chứng có kỷ luật**, không phải kiến trúc chưa ai dùng; và mức thực tế của tiêu chí 4 là **occlusion + hiển thị + đối chiếu motif**, thấp hơn mức tôi đã viết ở mục 2.6 và trong khảo sát 02/10.

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

**Tổng: đạt rõ 1 và 5, thiếu 2 và 3.**

**Cập nhật 07/10:** GVHD chấp nhận đầu vào ma trận biểu hiện, nên hướng này **không còn bị loại vì loại dữ liệu**. Nhưng hai cổng khác vẫn đứng và đủ để loại: **`tDamAge` không tra được nguồn nào** (mục 1.1) và **không tìm được tập test độc lập cho "nguy cơ chuyển dạng ác tính"** (mục 1.5). Và tiêu chí 2–3 vẫn yếu, vì không có cửa sổ residue nào để cải tiến — đó là đặc tính của bài toán, không phải của sở thích GVHD.

### 1.7. Nếu vẫn muốn làm, phạm vi tối thiểu khả thi

Phiên bản thu hẹp duy nhất tôi thấy đứng được: **một task hồi quy tuổi trên GTEx/GEO cho 2–3 mô, cộng một phân tích "điểm tổn thương phiên mã có tách được mô ung thư với mô lành kề cận trong TCGA hay không"**, và **nói thẳng là không dùng PLM**. Phải chấp nhận trước rằng tiêu chí 2–3 sẽ không đạt, và phải hỏi GVHD xem như vậy có chấp nhận được không.

---

## 2. Hướng 2 — Phát hiện tế bào lão hóa trong khối u (Cellular Senescence in TME)

**Hướng khả thi nhất trong bốn hướng.** Nhưng nó đang gộp **hai bài toán khác nhau hoàn toàn** trong một câu, và phải chọn một.

> **Cập nhật 07/10/2026 — sinh viên đã chốt: nếu chọn hướng 2 thì dùng scRNA-seq, không dùng ảnh hình thái nhân.** Phần 2.1 dưới đây giữ lại nhánh ảnh để thấy căn cứ của lựa chọn. **Và hai điểm trong mục 2.4 đã bị đính chính bởi khảo sát 07/10 — đọc [mục 7](#7-kiểm-chứng-bổ-sung-và-phán-quyết-hướng-2-0710) trước khi dùng mục 2.4.**

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

**Tổng: đạt 4 và 5 mạnh, 1–3 ở mức trung bình.** Khá hơn hướng 1 và 3, kém hơn ứng viên A của khảo sát 02/10 (A được đánh giá đạt cả năm tiêu chí trong khảo sát đó, **nhưng A chưa có tập test độc lập** — xem đính chính ở mục 0 và 7.2).

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

### 3.2. Bốn cổng cũ, vẫn đứng (dẫn lại [khảo sát 02/10 §10](aging-cancer/aging-cancer-deep-dive.md))

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
| Đầu vào | Vector biểu hiện / bảng | **Vector đơn bào (scRNA-seq, chốt 07/10)** | Chuỗi peptide | Bảng omics + đồ thị + văn bản |
| **Có trục chuỗi amino acid?** | **Không** | **Không** | Có | Không |
| **Dùng được lane PLM/mCNN của GVHD?** | **Không** | Không | Có — **nhưng đã bị chiếm** | Không |
| **Bị loại vì loại đầu vào?** | **Không** (GVHD chấp nhận ma trận biểu hiện, 07/10) | **Không** | — | **Không** |
| Dữ liệu công khai | GEO/GTEx có; UK Biobank **không** (đơn duyệt) | GEO scRNA-seq **có** `[chưa thử link]` | Có qua figshare Immunity 2023 `[đã thử link 02/10]` | GDSC bulk **410 Gone** `[đã thử link 02/10]` |
| **Tập test độc lập** | **Không xác định được** | **Chưa xác định** — phải tự dựng theo trung tâm | Có (TESLA/ITSNdb) **nhưng AUC 0,52–0,60** | Không cho phần giải thích |
| Mức đông đúc | Trung bình | **Đã có 3–4 công cụ ở tạp chí mạnh** | Cao + đúng lane Prof Ou | **Đông nhất** |
| Khớp GVHD — phương pháp | **Thấp** | Thấp–trung bình | Cao (nhưng là lane Prof Ou) | Trung bình (RAG đã có) |
| Khớp GVHD — sinh học | Không có bài | Không có bài (gần SirtSAGE về chủ đề aging) | **Không có bài cancer** | Không có bài |
| Khả thi 8–9 tuần | Trung bình | **Cao** (nếu chọn scRNA-seq) | Thấp | Trung bình (nếu đổi thành truy hồi) |
| Tiêu chí đạt rõ | 1, 5 | **4, 5** (1–3 trung bình) | 5 | 5 |
| Rủi ro lớn nhất | **Không có trục chuỗi → tiêu chí 2–3 không đạt**; tDamAge không tra được | **Nhãn không có chuẩn vàng** (mục 7.1); không có tiền lệ cùng GVHD cho đầu vào không phải trình tự (mục 7.2) | **Chuỗi sinh ra không có nhãn thật** + định vị | **Phần giải thích không đo được** |

### So với sáu ứng viên A–F của khảo sát 02/10

Nói thẳng, vì đây là điều quan trọng nhất trong tài liệu này: **ứng viên A (substrate SIRT theo isoform) và B (site phospho theo nhóm kinase) được khảo sát 02/10 đánh giá đạt cả năm tiêu chí, và nhãn của cả hai là nhãn thực nghiệm đã tồn tại** — A có file nhãn 6.801 site đã tải về và đếm được `[tự đo]` (nguồn: repo công khai của Ridgeway 2025, nhãn gốc từ microarray Rauh 2013), B có benchmark non-homologous do chính dbPTM công bố `[toàn văn]`.

**Đính chính 07/10, bản 06/10 của tài liệu này nói sai:** bản đó viết A và B "đều đã qua cổng dữ liệu". **Không đúng với A.** Theo chính khảo sát 02/10 (bảng mục 9 và rủi ro 1 ở mục 3), **A KHÔNG có tập test độc lập** — split công bố chỉ là holdout 10% trên cùng một microarray, và khảo sát đặt sẵn một cổng dừng: *nếu đến hết tuần 7 không dựng được tập test độc lập nguồn với cả hai lớp thì chuyển sang ứng viên B*. Khảo sát cũng xếp **A và B ngang nhau**, không xếp A trên B; việc chọn giữa hai cái treo vào một câu hỏi cho GVHD (thầy có coi split tự dựng cộng tập MS độc lập nguồn là "test độc lập" đủ chuẩn hay không).

**Vậy phát biểu đúng là:** **B là ứng viên duy nhất có benchmark cộng đồng đã tồn tại**; A mạnh hơn về mức khớp GVHD và dư địa đóng góp nhưng **còn một cổng mở**. Cả hai vẫn ở trên bốn hướng mới ở chỗ nhãn là nhãn thực nghiệm, không phải proxy tính toán. Lý do rất hệ thống, và đã được nêu trong khảo sát 02/10: ba trong bốn hướng mới **không có trục chuỗi amino acid**, nên pipeline cửa sổ-residue + PLM mà sinh viên đã dựng và GVHD hiểu rõ **không dùng lại được**, và hai tiêu chí 2–3 mất theo.

---

## 6. Khuyến nghị và việc cần làm trước tuần 6

**Khuyến nghị:** mang **cả hai nhóm** tới buổi tuần 6 và để GVHD chọn, trình bày theo đúng ba bước ở mục 3 biên bản:

1. **Nhóm có nhãn thực nghiệm đã tồn tại:** ứng viên A hoặc B của [khảo sát 02/10](aging-cancer/aging-cancer-deep-dive.md). Đây là nhóm tôi khuyên. **Trong đó chỉ B có benchmark cộng đồng sẵn**; A còn cổng mở về tập test độc lập (đính chính 07/10, xem mục 0 và 7.2).
2. **Trong bốn hướng GVHD gợi ý:** **hướng 2**, thu hẹp thành *"phân loại tế bào lão hóa trong vi môi trường khối u từ scRNA-seq, có cảnh báo miền áp dụng, đánh giá bằng split gom nhóm theo bệnh nhân và một tập test độc lập nguồn"*. Phương án hai: **hướng 4** đổi thành bài toán truy hồi bằng chứng có đáp án (4.5).

**Cách nói ở buổi gặp, một câu:** "Em đã phân tích cả bốn hướng thầy gợi ý theo đúng khung thầy yêu cầu. Ba trong bốn hướng có đầu vào không phải chuỗi amino acid, nên không dùng lại được pipeline PLM–mCNN, và em e là tiêu chí 2 và 3 sẽ khó đạt. Hướng 2 thì khả thi, nhưng đã có 3–4 công cụ. Em xin thầy cho ý kiến giữa hướng 2 và hai ứng viên em đã kiểm được dữ liệu."

**Năm việc phải làm trước tuần 6, xếp theo giá trị:**

1. **Hỏi GVHD tên bài báo / DOI của `tDamAge`** — không tra được, và nó là nền của hướng 1.
2. ~~**Thử link và kiểm code + nhãn của DeepScence và SenCID**, và kiểm xem chúng **có split theo bệnh nhân hay không**.~~ **Đã làm 07/10 — xem [mục 7.1](#71-deepscence-sencid-và-senepy-chia-tập-thế-nào--và-vì-sao-câu-hỏi-ban-đầu-đặt-sai). Kết quả đảo lại tiền đề: không công cụ nào chia theo bệnh nhân, nhưng vì phần lớn không phải mô hình có giám sát, nên đó không phải một đóng góp sẵn.** Còn lại: code và nhãn benchmark của DeepScence vẫn chưa kiểm được (Cell Genomics trả 403).
3. **Chọn một dataset scRNA-seq khối u công khai, tải thật, đếm số tế bào và số bệnh nhân** — y hệt cách khảo sát 02/10 đã làm với ứng viên A. Không có bước này thì "khả thi" chỉ là phỏng đoán.
4. **Xác nhận nguồn GPU** (câu 6 trong [danh sách câu hỏi GVHD](aging-cancer/aging-cancer-deep-dive.md#13-câu-hỏi-đặt-cho-gvhd-ở-tuần-6)). Hướng 2 nhánh foundation model đơn bào **không chạy trên CPU**.
5. **Chuẩn bị một trang brief sinh học** cho hướng được chọn, vì GVHD không có bài ở ba trong bốn hướng — sinh viên là người phải mang phần sinh học tới.
6. **Quyết định cách lấy nhãn cho hướng 2 và nói thẳng nó là proxy** — đây là việc mới, phát sinh từ [mục 7.1](#71-deepscence-sencid-và-senepy-chia-tập-thế-nào--và-vì-sao-câu-hỏi-ban-đầu-đặt-sai): senescence không có chuẩn vàng ở mức tế bào trong mô, nên mọi mô hình có giám sát trên khối u đều học lại một bộ chấm điểm đã có. Phải có câu trả lời cho câu hỏi này trước khi pitch hướng 2.

**Hai câu hỏi mới cho GVHD, thêm vào danh sách ở [khảo sát 02/10 §13](aging-cancer/aging-cancer-deep-dive.md):**

- **Với hướng 1 và 4, thầy có chấp nhận một đề tài không dùng PLM/mCNN không?** Nếu không, hai hướng đó rụng vì kiến trúc, không vì chủ đề.
- **Với hướng 4, thầy đo chất lượng "giải thích tự động" bằng gì?** Nếu không có thước đo thì em xin đổi thành truy hồi bằng chứng có đáp án.
- ~~**Thêm 07/10:** **Thầy có chấp nhận một đề tài có đầu vào là ma trận biểu hiện, không phải chuỗi amino acid, không?**~~ **Đã có câu trả lời ngày 07/10: GVHD chấp nhận** (sinh viên xác nhận; đã ghi vào [biên bản lần 1 mục 1](../../project/meetings/2026-10-02-session-01/minutes.md)). Câu còn lại, hẹp hơn và vẫn phải hỏi: **với đầu vào dạng đó, thầy kỳ vọng tiêu chí 2 và 3 được chứng minh bằng gì**, khi thang "đặc trưng thủ công → CNN → mCNN → PLM" không áp dụng được?

---

## 7. Kiểm chứng bổ sung và phán quyết hướng 2 (07/10)

Hai việc sinh viên yêu cầu làm ngay, vì cả hai làm được mà không cần chờ GVHD. Kết quả **đảo lại một phần mục 2.4**, nên đọc mục này trước khi dùng mục đó.

### 7.1. DeepScence, SenCID và SenePy chia tập thế nào — và vì sao câu hỏi ban đầu đặt sai

**Kết quả ngắn: không công cụ nào trong ba công cụ chia tập theo bệnh nhân, nhưng không phải vì chúng làm sai — mà vì phần lớn chúng không phải mô hình có giám sát.** Đây là **đính chính cho đề xuất đóng góp số 2 ở mục 2.4**: lập luận "các công cụ hiện có không gom nhóm theo bệnh nhân nên chỉ số bị lạm phát" **đặt trên tiền đề sai** và không được mang tới buổi gặp GVHD ở dạng đó.

| Công cụ | Loại mô hình | Dữ liệu huấn luyện | Chia tập | Nguồn |
|---|---|---|---|---|
| **DeepScence** (Cell Genomics 2026) | **Không giám sát** — autoencoder ZINB, cộng bộ gene nhân `CoreScence` **39 gene** (gene có mặt ở ≥ 5 bộ chữ ký đã công bố) | Không có nhãn | **Không có train/test split nào.** Đánh giá bằng cách áp lên các dataset độc lập, lấy β-gal staining và IHC làm chuẩn so | `[toàn văn — bản bioRxiv v3]` |
| **SenCID** (Cell Metabolism 2024) | **Có giám sát — SVM** | **Bulk RNA-seq đã công bố, từ các nghiên cứu *in vitro*** | Không tìm được mô tả split; **tập huấn luyện không có bệnh nhân nào** vì toàn bộ là bulk in vitro | `[toàn văn — trích trong DeepScence]` |
| **SenePy** (Nat Commun 2025) | **Chấm điểm theo chữ ký**, chữ ký dựng không giám sát (gene động theo tuổi → mạng đồng biểu hiện → hub) | **72 chữ ký chuột + 64 chữ ký người**, từ atlas mô lành, người hiến 1–92 tuổi, **37 mô** | Không có split theo người hiến. Kiểm chứng bằng chuột báo cáo p16-CreERT2-tdTomato, dataset senolytic, mô hình OIS | `[toàn văn]` ([Nat Commun](https://www.nature.com/articles/s41467-025-57047-7)) |

**Ba hệ quả, xếp theo mức quan trọng:**

1. **Khoảng cách in vitro → in vivo đã được đo và công bố, không còn là khoảng trống để nhận.** DeepScence viết thẳng rằng *"a major limitation of SenCID is that its training data were collected from in vitro studies"* và báo rằng SenCID, **dù ngang DeepScence trên dữ liệu in vitro, rớt hẳn trên dữ liệu in vivo với AUROC ≤ 0,2 ở năm loại tế bào** `[toàn văn]`. Con số này là **lý lẽ sẵn có cho phần động cơ** của hướng 2 — nhưng nếu đề tài tự nhận "đóng góp của em là chỉ ra khoảng cách miền", GVHD có thể đáp rằng bài Cell Genomics đã chỉ ra rồi.
2. **Chỗ trống thật, và nó hẹp hơn mục 2.4 đã nói:** SenePy **không dùng dữ liệu khối u người**, chỉ mô lành; SenCID huấn luyện trên bulk in vitro; DeepScence không giám sát. Nên **chưa có mô hình có giám sát nào được huấn luyện trên scRNA-seq khối u người với split gom nhóm theo bệnh nhân** — đó là câu phát biểu chính xác của khoảng trống. Nhưng phải nói kèm **vì sao chưa có**: xem điểm 3.
3. **Lý do chưa có là vì không có nhãn, và đó là rủi ro trung tâm của hướng 2.** Cả ba công cụ đều tránh học có giám sát trên mô thật **đúng vì senescence không có chuẩn vàng ở mức tế bào trong mô**. Một đề tài có giám sát trên khối u buộc phải lấy nhãn từ một proxy (chữ ký gene, hoặc đầu ra của DeepScence/SenePy), và khi đó **"phát hiện tế bào lão hóa" thật ra là "học lại một bộ chấm điểm đã có"**. Đây là đòn tấn công mạnh nhất vào hướng 2, và nó **chưa được nêu đủ nặng ở mục 2.7**.

**Việc còn phải kiểm, chưa làm được trong phiên này:** `[chưa kiểm]` mã nguồn và nhãn benchmark của DeepScence (trang Cell Genomics trả **HTTP 403**, bản bioRxiv đọc được nhưng không có mục code availability); `[chưa kiểm]` SenCID có công bố mô tả split ở phần methods hay supplementary hay không (trang Cell Metabolism **403**, ScienceDirect chặn robots). Riêng **mã huấn luyện SenCID thì chưa phát hành**: trong issue #3 của repo, tác giả chỉ nói đang *"considering to add a new option for users to train a new SID"* `[toàn văn]` ([SenCID issue #3](https://github.com/JackieHanLab/SenCID/issues/3)).

### 7.2. Đối chiếu bốn hướng với hai luận văn cùng GVHD

Nguồn: [phân tích hai luận văn](../../resources/reference-theses/thesis-comparison.md) (05/10/2026) — **T1 Hybrid Cascade** (PLM–mCNN cho peptide, 08/2026) và **T2 BioFlow-Scope** (nền tảng web tin sinh, 08/2026), cả hai **cùng GVHD**. Mọi nhận xét dưới đây là đọc lại từ phân tích đó, **không phải chấm điểm của GVHD**.

**Tiêu chí 2 (cải tiến phương pháp) — mức thực tế dễ hơn tôi đã viết, và đây là tin tốt.** T1 không phát minh kiến trúc mới. Nó đạt tiêu chí 2 bằng một **thang đối chứng có kỷ luật**: đặc trưng thủ công (AAC/DPC/one-hot + RF/SVM) → CNN một cửa sổ → mCNN nhiều cửa sổ → ESM-2 ở bốn cỡ 8M/35M/150M/650M, frozen và fine-tune; cộng kiểm tra lệch độ dài giữa hai lớp (AMP ~22 aa, âm ~44 aa) và Focal Loss cho mất cân bằng; rồi chọn cấu hình theo cả kết quả và chi phí triển khai. **Mức cần đạt là "mỗi bước thêm độ phức tạp đều có đối chứng", không phải "kiến trúc chưa ai dùng".**

**Tiêu chí 4 (XAI) — mức thực tế thấp hơn tôi đã viết.** T1 đạt tiêu chí 4 bằng **occlusion**: che lần lượt từng residue, đo thay đổi đầu ra, hiển thị vùng nhạy cảm trên giao diện, đối chiếu **55 motif**. Không SHAP, không integrated gradients. Và chính phân tích 05/10 ghi rằng T1 **thiếu đánh giá hệ thống về độ trung thực và ổn định của giải thích**. Nghĩa là: một đóng góp XAI chỉ cần **occlusion + hiển thị + đối chiếu nguồn độc lập, cộng một phép kiểm so che vị trí quan trọng với vị trí ngẫu nhiên** là đã **nhỉnh hơn tiền lệ cùng GVHD**.

**Tiêu chí 5 (ứng dụng) — phạm vi linh hoạt hơn tôi nghĩ.** T1 dùng **FastAPI + Streamlit**, cài cục bộ hoặc Docker; T2 dùng Spring Boot + Next.js + PostgreSQL + Redis + Qdrant + FastAPI. **Cả hai đều được chấp nhận**, nên một predictor chuyên biệt gọn gàng là đủ; không bắt buộc kiến trúc ba tầng. Câu hỏi 7 trong danh sách câu hỏi GVHD vì vậy **hạ mức ưu tiên**.

**Và đây là phát hiện khó chịu nhất, phải nói thẳng: cả hai luận văn cùng GVHD đều là bài toán trên trình tự.** T1 ăn chuỗi peptide qua ESM-2; T2 dùng ESM-2 cho tìm kiếm protein. **Không có tiền lệ nào cùng GVHD với đầu vào là ma trận biểu hiện hay vector omics.** Hệ quả cho bốn hướng:

- Nó **củng cố** phản đối cấu trúc với hướng 1 và 4 — đã nêu ở mục 1.6 và 4.4.
- **Sau xác nhận cuối ngày 07/10 (GVHD chấp nhận đầu vào ma trận biểu hiện), đây không còn là cổng loại** — nhưng nó vẫn áp lên hướng 2 nhánh scRNA-seq ở mức khác: chọn scRNA-seq nghĩa là **không có tiền lệ cùng GVHD**, và **thang đối chứng của T1 không chuyển sang được nguyên vẹn**: thang tương đương cho scRNA-seq sẽ là *điểm chữ ký marker → hồi quy logistic/SVM → autoencoder → foundation model đơn bào (scGPT/Geneformer)*. Thang đó hợp lý về mặt phương pháp, nhưng là **thang sinh viên tự dựng**, không phải thang GVHD đã nhìn thấy hoạt động.
- Ngược lại, **ứng viên A và B của [khảo sát 02/10](aging-cancer/aging-cancer-deep-dive.md) rơi đúng vào khuôn T1** (lưu ý cổng dữ liệu còn mở của A, đính chính ở trên): cùng đầu vào trình tự, cùng họ PLM + mCNN, cùng dạng cửa sổ quanh residue, cùng kiểu XAI occlusion trên cửa sổ. Với A hoặc B, **thang đối chứng của T1 dùng lại gần như nguyên vẹn** — tức tiêu chí 2 có đường đi đã được chính GVHD chấp nhận một lần.

**Ba thứ nên lấy từ T1 bất kể chọn hướng nào:** (a) thang baseline → biểu diễn → head → ablation, mỗi bước một đối chứng; (b) kiểm xem mô hình có đang học tín hiệu ngoài mục tiêu hay không (T1 phát hiện lệch độ dài giữa hai lớp — tương đương ở hướng 2 là **lệch loại tế bào hoặc lệch bệnh nhân giữa hai lớp**); (c) XAI nối trực tiếp vào giao diện, không để rời thành một hình trong báo cáo. Từ T2 nên lấy: lưu mỗi lần chạy kèm phiên bản mô hình, hash đầu vào, cấu hình và log.

**Hai điều T1 bị phê trong phân tích 05/10 mà đề tài này phải tránh lặp lại:** split chỉ `drop_duplicates` rồi chia ngẫu nhiên 80/10/10 — **không kiểm soát đồng dạng**, nên chữ "independent" trong bảng kết quả của T1 chỉ là holdout; và F1 được đọc rời khỏi confusion matrix trong khi lớp dương là lớp đa số. Hai lỗi này **đúng là hai lỗi hướng 2 dễ mắc nhất** (gom nhóm theo bệnh nhân, và báo MCC/AUPRC thay vì accuracy trên dữ liệu mất cân bằng nặng).

### 7.3. Ngưỡng quyết định đi/dừng cho hướng 2, **đặt trước khi có số** (07/10)

Mục này viết **trước khi chạy script trên dữ liệu thật**, và đó là chủ ý: nếu đặt ngưỡng sau khi nhìn số thì ngưỡng nào cũng đạt. Ngày đặt: 07/10/2026. Dataset đầu tiên dự kiến: GSE103322 (ung thư đầu cổ).

**Bốn điều kiện, phải đạt cả bốn mới đi tiếp hướng 2:**

| # | Điều kiện | Ngưỡng | Vì sao đúng ngưỡng này |
|---|---|---|---|
| 1 | **Số bệnh nhân** `n_patients` | **≥ 10** | Chia 5 fold theo bệnh nhân cần ≥ 2 bệnh nhân mỗi fold. Dưới 10 thì một bệnh nhân đổi fold là đổi kết quả |
| 2 | **Số bệnh nhân có ≥ 20 tế bào dương** `patients_with_ge20_positives` | **≥ 8** | Nếu tế bào dương chỉ có ở 2–3 bệnh nhân thì fold không chứa dương nào sẽ xuất hiện, và MCC không tính được trên fold đó |
| 3 | **Mức dồn** `concentration_ratio` | **≤ 1,5 → đi · 1,5–3,0 → đi nhưng phải báo per-patient và cân mẫu theo bệnh nhân · > 3,0 → DỪNG** | Đây là tỉ số giữa phần tế bào dương và phần tế bào của chính bệnh nhân dồn nhất, nên 1,0 là mức kỳ vọng nếu senescence rải đều. Trên 3 nghĩa là mô hình sẽ học *bệnh nhân*, không học senescence |
| 4 | **Độ phủ chữ ký** `signature_coverage` | **≥ 0,6** | Script tự từ chối dưới mức này. Dưới 60% gene thì điểm không còn là SenMayo |

**Nếu không đạt:** dừng hướng 2, chuyển sang ứng viên A hoặc B của [khảo sát 02/10](aging-cancer/aging-cancer-deep-dive.md). Không nới ngưỡng để cứu hướng 2 — nếu phải nới thì ghi rõ nới cái nào và vì sao, ở chính mục này, kèm ngày.

**Một điều kiện phụ, không phải cổng dừng nhưng phải báo:** `positive_rate_spread`. Nếu `max / median` > 10 thì tín hiệu gần như chắc chắn gắn với bệnh nhân hoặc với batch, và phải thêm một phân tích theo loại tế bào trước khi nói bất cứ điều gì về senescence.

**Lưu ý đọc số, nhắc lại vì dễ sai:** `positive_fraction` luôn ≈ 5% vì ngưỡng là phân vị 0,95 **trong chính dataset**. Nó không phải tỉ lệ tế bào lão hóa trong khối u, và **không được đưa vào slide như một phát hiện**.

### 7.4. Nhãn proxy: định nghĩa đề xuất, và cách nói trung thực về nó

Đây là rào chính còn lại của hướng 2 (mục 7.1). Dưới đây là **đề xuất**, chưa chạy, chưa kiểm.

**Định nghĩa đề xuất — nhãn đồng thuận ba tín hiệu độc lập:**

- **Tín hiệu 1:** điểm SenMayo (chữ ký 117 gene hiện có), lấy phân vị cao.
- **Tín hiệu 2:** điểm DeepScence (**không giám sát**, nên không mang theo nhãn của ai), hoặc SenePy nếu DeepScence không chạy được.
- **Tín hiệu 3:** bằng chứng marker trực tiếp — biểu hiện `CDKN1A` và `CDKN2A`. Lưu ý: **hai gene này không thuộc SenMayo**, nên chúng là tín hiệu trực giao thật, không phải vòng tròn.

**Dương** = ít nhất **2 trong 3** tín hiệu đồng thuận. **Âm** = nằm ở phân vị thấp của **cả ba**. Tế bào ở giữa **bỏ ra khỏi tập huấn luyện**, không gán âm — đây đúng là lỗi mà [khảo sát 02/10](aging-cancer/aging-cancer-deep-dive.md) đã bắt ở các bộ dữ liệu neoantigen ("chưa chứng minh là dương" bị dùng như "đã chứng minh là âm").

**Phải báo kèm:** mức đồng thuận giữa ba tín hiệu (Cohen's kappa từng cặp). Nếu kappa rất thấp thì ba tín hiệu đang nói ba chuyện khác nhau, và "đồng thuận 2/3" chỉ là một phép bỏ phiếu may rủi — khi đó phải nói ra, không được che.

**Kiểm chéo:** áp định nghĩa sang **GSE131907** (ung thư phổi, 58 mẫu) và xem tỉ lệ dương cùng mức dồn có giữ được hay không. Dataset thứ hai là **tập test độc lập nguồn** mà mục 2.5 nói là chưa xác định — đây là ứng viên cụ thể đầu tiên cho chỗ đó.

**Cách gọi tên, bắt buộc:** gọi nhãn là **"nhãn đồng thuận SenMayo–DeepScence–marker"**, không gọi là "tế bào lão hóa". Và trong mọi tài liệu phải có một câu: *nhãn này là proxy tính toán, không phải xác nhận thực nghiệm; senescence chưa có chuẩn vàng ở mức tế bào trong mô*. Nói "phát hiện tế bào lão hóa" với nhãn dạng này là **đòn tấn công dễ nhất** mà GVHD hoặc hội đồng sẽ dùng.

**Điều này đổi gì về đóng góp:** với nhãn đồng thuận, đóng góp **không còn là** "phát hiện tế bào lão hóa chính xác hơn". Nó là: *một bộ phân loại có cảnh báo miền áp dụng, huấn luyện trên nhãn đồng thuận nhiều nguồn, đánh giá bằng split gom nhóm theo bệnh nhân, cộng một phép đo xem nhãn của ba công cụ hiện có đồng thuận tới đâu trên mô khối u thật*. Phần in nghiêng cuối **là một kết quả có giá trị dù mô hình không thắng ai** — và theo mục 7.2, một kết quả âm được làm tử tế vẫn cần GVHD chấp nhận trước, nên đó là câu phải hỏi ở tuần 6.

### 7.5. Kết quả trên dữ liệu thật và phán quyết: **DỪNG hướng 2** (07/10)

Số từ GSE103322 (ung thư đầu cổ, **5.902 tế bào**, **17 bệnh nhân** suy ra được, GEO ghi 18), do thread chạy script trên môi trường có mạng; code và báo cáo ở PR #4 (nhánh `claude/project-thread-l271f1`). Dưới đây là **áp đúng bốn ngưỡng đã đặt trước ở mục 7.3**, không sửa ngưỡng.

| # | Điều kiện | Ngưỡng đặt trước | Số thật | Kết quả |
|---|---|---|---|---|
| 1 | `n_patients` | ≥ 10 | **17** | **ĐẠT** |
| 2 | `patients_with_ge20_positives` | ≥ 8 | **7** | **KHÔNG ĐẠT** |
| 3 | `concentration_ratio` | ≤ 1,5 sạch · 1,5–3,0 đi kèm cân mẫu · > 3,0 dừng | **1,85** | Đi kèm cân mẫu theo bệnh nhân |
| 4 | `signature_coverage` | ≥ 0,6 | **0,97** (113/117 gene) | **ĐẠT** |

Mục 7.3 nói **phải đạt cả bốn**. Điều kiện 2 không đạt → **theo đúng cam kết, dừng hướng 2.**

**Và 7 so với 8 là sát, nên phải nói rõ vì sao không nới ngưỡng:** vì có một phát hiện thứ hai, độc lập và nặng hơn nhiều.

#### Phát hiện quyết định: điểm SenMayo chủ yếu đang theo **loại tế bào**, không theo senescence

- **70% tế bào dương là fibroblast**, còn **tế bào T và B không có tế bào dương nào**.
- Khi chấm ngưỡng **riêng theo từng loại tế bào** để bỏ ảnh hưởng đó: **fibroblast chỉ còn 1 bệnh nhân** có ≥ 20 tế bào dương; **tế bào ung thư có 3 bệnh nhân** nhưng `concentration_ratio = 3,35`, **vượt ngưỡng dừng 3,0**.

Nói cách khác: hai lớp "dương" và "âm" khác nhau **theo loại tế bào**, không theo trạng thái senescence. **Đây đúng là lỗi mà khảo sát 02/10 đã tự đo được ở SenSeqNet**, chỉ là lặp lại ở một mức khác — ở đó hai lớp khác nhau theo **họ protein**, ở đây theo **loại tế bào**. Và nó cũng đúng là phiên bản mức tế bào của lỗi lệch độ dài mà T1 phát hiện giữa hai lớp AMP/non-AMP.

Một dataset lớn hơn **không sửa được chuyện này** — GSE131907 vì vậy không được chạy, và đó là quyết định đúng: thêm tế bào không làm nhãn bớt gắn với loại tế bào.

#### Ba điều phán quyết này **không** nói

1. **Không nói "senescence trong khối u là hướng tồi".** Nó nói: *với nhãn dẫn từ chữ ký SenMayo, trên dataset này, trong 8–9 tuần*, bài toán không qua được cổng dữ liệu.
2. **Không bác bỏ DeepScence hay SenePy.** Cả hai **không giám sát hoặc chấm điểm theo chữ ký** (mục 7.1), nên chúng không mắc đúng lỗi này; chính vì vậy chúng tránh học có giám sát.
3. **Không nói nhãn đồng thuận ở mục 7.4 là vô ích.** Nhưng nó cho thấy nhãn đồng thuận **phải chấm theo từng loại tế bào** ngay từ đầu, và sau khi làm vậy thì **số bệnh nhân còn lại quá nhỏ** để chia fold — đó mới là lý do thật để dừng.

#### Kết quả này **dùng được** ở buổi tuần 6

Đây là một **kết quả âm tự đo được**, có số, trên dữ liệu công khai, và nó trả lời đúng câu GVHD quan tâm nhất ("vì sao cần nghiên cứu / vấn đề tồn đọng là gì"): *chữ ký senescence phổ biến nhất, áp lên mô khối u thật, phân tách loại tế bào chứ không phân tách trạng thái senescence*. Một slide về chuyện này mạnh hơn hẳn một slide hứa hẹn, và nó cho thấy sinh viên đã kiểm dữ liệu trước khi chọn đề tài. **Cách nói đúng:** đây là lý do em không chọn hướng 2, không phải một đóng góp đã hoàn thành.

#### Khuyến nghị sau phán quyết

**Chuyển sang ứng viên B** (vị trí phosphoryl hóa theo nhóm kinase gây ung thư) — đây là ứng viên duy nhất có **benchmark non-homologous do chính dbPTM công bố**, tức cổng dữ liệu đã đóng sẵn, và nó rơi đúng khuôn T1 về phương pháp (mục 7.2). **Ứng viên A** vẫn là lựa chọn thứ hai, nhưng nhớ cổng mở của nó (mục 0): phải tự dựng tập test độc lập, và câu hỏi số 1 cho GVHD quyết định chuyện đó. **So sánh đầy đủ B và A với hướng 2 trên chín trục: [mục 7.6](#76-so-sánh-ứng-viên-b-và-a-với-hướng-2-trên-cùng-một-bộ-tiêu-chí-0710).**

### 7.6. So sánh ứng viên B và A với hướng 2 trên **cùng một bộ tiêu chí** (07/10)

Mục 5 so bốn hướng với nhau; mục này trả lời câu khác và quan trọng hơn: **nếu bỏ hướng 2 để sang B hoặc A thì được gì và mất gì**. Chín trục dưới đây là những trục thật sự phân biệt được ba ứng viên, không phải năm tiêu chí GVHD (cả ba đều đạt tiêu chí 5, nên tiêu chí 5 không phân biệt gì).

| Trục | **B — site phospho theo nhóm kinase** | **A — substrate SIRT theo isoform** | **Hướng 2 — senescence trong TME (scRNA-seq)** |
|---|---|---|---|
| **1. Loại nhãn** | **Thực nghiệm** (MS phosphoproteomics, dbPTM tổng hợp) `[toàn văn]` | **Thực nghiệm** (microarray Rauh 2013, 6.801 site đếm được) `[tự đo]` | **Proxy tính toán** — điểm biểu hiện của một chữ ký gene, không ai đo trạng thái senescence của từng tế bào (mục 7.1) |
| **2. Tập test độc lập** | **Có sẵn** — benchmark non-homologous do chính dbPTM công bố `[toàn văn]` | **Chưa có** — split công bố chỉ là holdout 10% trên cùng microarray; phải tự dựng, cổng dừng tuần 7 | **Không có và không dựng được** trong 8–9 tuần: dựng được thì cũng là nhãn proxy ở cả hai đầu |
| **3. Đơn vị gom nhóm khi chia tập** | Protein (và cụm đồng dạng qua CD-HIT/MMseqs2) — **đã có công cụ chuẩn** | Protein — cùng công cụ | Bệnh nhân — **không có công cụ chuẩn**, và sau khi chấm riêng theo loại tế bào thì **chỉ còn 1–3 bệnh nhân** đủ tế bào dương (mục 7.5) |
| **4. Yếu tố gây nhiễu đã đo được** | Đồng dạng trình tự — **kiểm soát được** bằng ngưỡng identity | Đồng dạng trình tự — kiểm soát được | **Loại tế bào** — `[tự đo]` 70% tế bào dương là fibroblast, T/B bằng 0. **Không kiểm soát được bằng cách chia tập**, vì nó nằm trong chính nhãn |
| **5. Dùng lại được thang đối chứng của T1?** | **Được gần như nguyên vẹn** (đặc trưng thủ công → CNN → mCNN → PLM, cùng dạng cửa sổ residue) | **Được** | **Không** — phải tự dựng thang cho dữ liệu đơn bào, và tiêu chí 2–3 phải tự lập luận (mục 7.2) |
| **6. XAI (tiêu chí 4)** | Occlusion theo vị trí trong cửa sổ → **sequence logo đối chiếu motif kinase đã biết** = có chuẩn ngoài để kiểm tính trung thực | Tương tự, đối chiếu motif substrate sirtuin | **Vòng tròn luận lý**: nhãn sinh ra từ chữ ký SenMayo, nên XAI chỉ ra các gene SenMayo là **tautology**, không phải phát hiện |
| **7. Mức đông đúc** | **Thấp nhất** — 14 bài DL 2024–26, có một preprint cạnh tranh | Gần như trống ở mức isoform | **Đã có 3–4 công cụ ở tạp chí mạnh** (DeepScence, SenCID, SenePy) |
| **8. Khớp chuyên môn sinh học GVHD** | Trung bình (kinase/cancer, thầy chưa làm) | **Cao nhất** (sirtuin/aging, gần SirtSAGE) | Thấp — thầy không có bài; sinh viên phải mang toàn bộ phần sinh học |
| **9. Chi phí khởi động** | **Thấp nhất** — dbPTM phát hành dữ liệu đã cắt cửa sổ ±10, CPU chạy được | Thấp — file nhãn đã tải về | Trung bình–cao: tải, QC, chú giải loại tế bào, và nhánh foundation model **không chạy trên CPU** |

**Đọc bảng này theo một dòng:** B và A thắng hướng 2 **không phải vì chủ đề hay hơn**, mà vì ở trục 1, 2 và 4 chúng có nhãn người khác đã đo bằng thực nghiệm và một yếu tố gây nhiễu kiểm soát được bằng công cụ có sẵn. Đó đúng là ba chỗ hướng 2 thất bại khi chạy số thật.

#### Ba điểm hướng 2 **vẫn hơn**, nói ra cho công bằng

1. **Hướng 2 là hướng duy nhất nằm đúng giao thoa cancer ∩ aging mà GVHD đã khung ra.** B là cancer/kinase, A là aging/sirtuin — **cả hai đều lệch khỏi giao thoa**. Đây là **cái giá thật** của việc chuyển, và là điều phải nói thẳng ở buổi tuần 6 chứ không che đi.
2. **Hướng 2 có ý nghĩa dịch thuật rõ hơn**: đếm tế bào lão hóa trong khối u nối trực tiếp tới senolytics, dễ trả lời câu "để làm gì" hơn một bảng điểm phosphosite.
3. **Hướng 2 là do chính GVHD gợi ý.** Bỏ nó cần một lý do có số — và giờ đã có, chính là mục 7.5. Không có mục 7.5 thì việc bỏ sẽ nghe như sinh viên chọn cái dễ.

#### Điều bảng này **không** quyết định

Ba trục quyết định (1, 2, 4) đều là trục **dữ liệu**, không phải trục khoa học. Cách đọc đúng: *trong 8–9 tuần, với nhãn hiện có, B và A đo được còn hướng 2 thì không* — chứ không phải *hướng 2 là câu hỏi kém*. Và **chọn giữa B và A vẫn treo vào một câu hỏi cho GVHD** (câu số 1, mục 0): thầy có coi split tự dựng cộng một tập MS độc lập nguồn là test độc lập đủ chuẩn hay không. Nếu thầy nói có thì A lên trước, vì trục 8 là trục duy nhất A thắng B rõ ràng, và nó quyết định việc thầy có hướng được phần sinh học hay không.

---

## 8. Những điều tài liệu này **chưa** kiểm chứng

- **`tDamAge`: không tra được bất kỳ nguồn nào.** Mọi phân tích hướng 1 đặt trên giả định rằng nó là một công cụ đo tổn thương phiên mã.
- **Phiên này chưa tải file dữ liệu nào.** Mọi trạng thái truy cập trong tài liệu này là `[chưa kiểm]`, trừ các dòng dẫn lại khảo sát 02/10 (`[tự đo]`, `[đã thử link]`). Cụ thể: **chưa thử link** GEO scRNA-seq, SenNet, DeepScence, SenCID, CIViC, OncoKB.
- **Chưa đọc toàn văn bài nào trong phiên 06/10.** Các bài Nature Aging / Nat Commun / Cell Genomics / Cell Metabolism ở mục 1–6 chỉ có từ tiêu đề và snippet tìm kiếm. **Phiên 07/10 đọc thêm được toàn văn bản bioRxiv v3 của DeepScence và bài SenePy trên Nat Commun** — các khẳng định ở mục 7.1 gắn nhãn theo đó.
- **Phần đối chiếu hai luận văn (mục 7.2) đọc lại từ [phân tích 05/10](../../resources/reference-theses/thesis-comparison.md), không đọc trực tiếp hai PDF.** Mọi số trang và con số trong đó thừa hưởng độ tin cậy của phân tích ấy, và chính phân tích ấy ghi rõ là **chưa kiểm toán mã nguồn hay tái lập thực nghiệm** của hai luận văn.
- ~~**Chưa biết các công cụ senescence hiện có split theo bệnh nhân hay không.**~~ **Đã kiểm 07/10, xem [mục 7.1](#71-deepscence-sencid-và-senepy-chia-tập-thế-nào--và-vì-sao-câu-hỏi-ban-đầu-đặt-sai).** Còn chưa kiểm: **mô tả split trong phần methods/supplementary của SenCID** (Cell Metabolism trả 403, ScienceDirect chặn robots) và **mục code/data availability của DeepScence** (Cell Genomics trả 403; bản bioRxiv v3 đọc được nhưng không có mục đó).
- **Chưa kiểm** liệu các dataset immunogenicity có công bố tuổi bệnh nhân hay không (ảnh hưởng phần "lớn tuổi" của hướng 3).
- **Chưa kiểm** điều kiện dùng lại dữ liệu curate của CIViC/OncoKB cho phiên bản khả thi của hướng 4.
- Bốn hướng này là **cách sinh viên ghi lại lời GVHD**, không phải văn bản GVHD viết. Nếu cách ghi lệch so với ý thầy thì phân tích này lệch theo.
