# Script thuyết trình và tài liệu đọc hiểu đề tài — Việt / English

**Buổi gặp GVHD 16/10/2026 · 26 slide · bản soạn ngày 15/10/2026.**

Tài liệu bám theo **toàn bộ năm phần paste** của Trọng, ghép thành 26 slide của [index.html](index.html). Khi bắt đầu, bản ghép và file trong repo khớp khi bỏ khoảng trắng. Khi rà cuối, HTML đã có sửa nhãn **A7V** ở slide 2; lời nói dưới đây dùng đúng A7V. Các đoạn **VI** và **EN** là hai phiên bản để chọn một ngôn ngữ khi nói; phần **Đọc hiểu / Study notes** dùng để học và chuẩn bị trả lời. Không cần đọc hai bản liên tiếp trong buổi trình bày.

Trạng thái và phạm vi lấy từ [sổ quyết định hiện hành](../../../../DECISIONS.md#hien-hanh); số liệu lấy từ [các nguồn cuối tài liệu](#sources). Đây là bản biên soạn lời nói, không ghi quyết định nghiên cứu mới. HTML, dữ liệu và mô hình không được sửa trong lần soạn này.

## Cách dùng / How to use

- **Tập nói:** đọc VI để hiểu, sau đó luyện EN bằng chính hình trên slide. Các câu chuyển giúp nối mạch, không phải nội dung mới trên slide.
- **Tự học:** đi theo thứ tự sinh học → cách đo → tiền lệ → giới hạn biểu diễn → dữ liệu → phương pháp → phần mềm. Dừng ở câu hỏi cuối mỗi slide và tự trả lời trước khi xem đáp án.
- **Khi trình bày:** phân biệt “tác giả đo”, “em tính lại từ dữ liệu tác giả”, “em đã huấn luyện”, và “em dự kiến thử”. Chữ **chưa đo / not measured** phải giữ nguyên trạng thái.
- **Khi cập nhật:** nếu dữ liệu hoặc slide đổi, kiểm lại nguồn tương ứng; các con số dưới đây là ảnh chụp trạng thái ngày 15/10/2026.

## Những điểm cần biết trước khi dùng / Source corrections

Các chỗ dưới đây được xử lý trong lời nói; **người soạn script không chỉnh HTML**. Ngoại lệ về trạng thái nguồn: nhãn A7V ở slide 2 đã được sửa trong HTML khi rà cuối.

| Slide          | Điểm cần đọc chính xác / Reading to use                                                                                                                                                                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1              | Tên sinh viên trong HTML là “Nguyễn Thanh Trọng”, trong `CLAUDE.md` là “Nguyễn Thế Trọng”. Script chỉ xưng “em”; cần Trọng kiểm lại thông tin bìa. Không tự chọn một tên làm hồ sơ chính thức. / Check the title-page name against the official record.                                                                                                                              |
| 2              | Chuỗi minh họa `MKTAYIAK` có **A ở vị trí 7**, nên ví dụ đúng là **A7V**. Bản paste ghi M7V; HTML khi rà cuối đã sửa phần chữ/nhãn thành A7V. / In this displayed sequence, the substitution is A7V; the final source check found the label corrected.                                                                                                                              |
| 3              | Lượng protein không bằng hiệu hai tốc độ. Công thức đúng về đơn vị là **dP/dt = tốc độ tổng hợp − tốc độ phân hủy**. / The difference of rates is the rate of change of abundance.                                                                                                                                                                                                    |
| 8–10, 13–14  | Degformer đã có ma trận 28×20; không nói đề tài đầu tiên tạo ma trận, hoặc mọi tiền lệ đều không có đầu ra mức residue. Cận bất biến chỉ áp cho **lớp chỉ dùng thành phần / kênh nội `cnn2w1`**, không cho PAP đầy đủ hay `cnn2w7`. / Bound the claim to the composition-only class and the tested channel.                                                        |
| 12             | Hình có `+1.8`, `−0.1`, `+0.62` nhưng không gắn định danh phép đo. Tài liệu này không coi chúng là kết quả thực nghiệm; dùng lập luận ký hiệu và ví dụ HIF1A có nguồn ở slide 16. / The untraced numbers are not used as evidence.                                                                                                                                                 |
| 14, 17, 21–22 | **MDE 0,0123** thuộc phép so **M3−M0 trên bộ bão hòa**, không phải ngưỡng nghiệm thu chung. Được tính trước các thử kiến trúc sắp tới, từ phương sai của phép so đã chạy; không phải đăng ký trước mọi thí nghiệm. / MDE is comparison-specific.                                                                                                                  |
| 17, 26         | **0,3553 là Spearman mức ô của ΔPAP**, không phải mức vị trí. JSON của PAP ghi mức vị trí **0,4130**; M3 ghi **0,4440**. Chưa có phép so ghép cặp đồng nhất cho hai số mức vị trí trong lần soạn này, nên không dùng chúng để tuyên bố thắng có kiểm định hay “đảo hạng” đã xác nhận. / Do not compare cell-level and position-level correlations. |
| 17             | `0.8682 − 0.8357` không cho delta đã báo `+0.0300`, vì các trung bình đến từ tập peptide khác nhau. Trên **cùng 2.064 peptide**, M3 = **0,8657**, ΔPAP = **0,8357**; delta ghép cặp = **+0,0300**. / Compare on the matched subset.                                                                                                                                       |
| 18             | Tiêu đề “all licence-checked” không đồng nghĩa đã đóng mọi xác nhận. Phạm vi MIT cho file Larsen còn chờ email theo [C-11a](../../../../DECISIONS.md#c-11a). / The Larsen data-licence clarification remains pending.                                                                                                                                                                                 |
| 20             | “130 peptide chồng lặp” là con số ở tập đối chiếu rộng hơn; với **tập bão hòa đã lọc**, dùng **42 peptide trùng tên, 61/89 cụm trùng**. / Keep overlap counts tied to their filtered population.                                                                                                                                                                                   |
| 23             | Dấu `–` trong bảng công cụ không chứng minh tính năng không tồn tại; các ô chưa đủ bằng chứng phải đọc là **chưa kiểm / not checked**. Bất định đã hiệu chỉnh là **mục tiêu thiết kế**, chưa phải kết quả. / Proposed features are not implemented features.                                                                                                     |
| 24             | **87,3% = 13.814/15.819 cụm** chưa thấy, không phải 87,3% số tile. Tỉ lệ tile trên protein chưa thấy là **67,9%**. / The denominator is protein clusters.                                                                                                                                                                                                                                       |
| 25–26         | G2 **chưa hoàn tất**; lịch chi tiết từng tuần là cách triển khai dự kiến. Q1/Q4 đang là câu trong bản nguồn, chờ Trọng hoàn thiện. HTML này **không có phụ lục rời**, dù chân slide 26 nhắc A1–A6; dùng phần nguồn bên dưới để tra. / Do not announce appendices that are absent from this deck.                                                                     |

## Bản đồ nội dung / Slide map

| Phần / Part                                                             | Slide                                                                                                    |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Nền tảng sinh học / Biological foundations                            | [1](#slide-01) · [2](#slide-02) · [3](#slide-03) · [4](#slide-04) · [5](#slide-05) · [6](#slide-06)       |
| Cách đo và tiền lệ / Measurement and prior work                     | [7](#slide-07) · [8](#slide-08) · [9](#slide-09) · [10](#slide-10) · [11](#slide-11)                      |
| Khoảng trống và đóng góp / Gap and contribution                    | [12](#slide-12) · [13](#slide-13) · [14](#slide-14)                                                       |
| Bài toán và dữ liệu / Task and datasets                             | [15](#slide-15) · [16](#slide-16) · [17](#slide-17) · [18](#slide-18) · [19](#slide-19) · [20](#slide-20) |
| Phương pháp, phần mềm, trao đổi / Method, software and discussion | [21](#slide-21) · [22](#slide-22) · [23](#slide-23) · [24](#slide-24) · [25](#slide-25) · [26](#slide-26) |

---

<a id="slide-01"></a>

## Slide 1 — Đề tài / Residue-level prediction of degron mutation effects

**Thông điệp / Message:** Dự đoán hiệu ứng thay một amino acid trong peptide degron, bằng nhãn độ bền thực nghiệm. / Predict single-substitution effects using experimental stability labels.

### VI — Lời thuyết trình

Em xin trình bày hướng nghiên cứu dự đoán hiệu ứng đột biến degron ở mức từng residue, tức từng vị trí amino acid trong chuỗi protein. Thay vì chỉ hỏi một đoạn protein có tín hiệu phân hủy hay không, em muốn dự đoán thay một amino acid tại một vị trí sẽ làm độ bền của peptide thay đổi như thế nào.

Bài trình bày đi từ sinh học và cách đo, đến các công trình gần nhất, bằng chứng em đã kiểm và phần phương pháp còn phải làm. Hiện em đã dựng lại nhãn và huấn luyện các mô hình ridge có kết quả dương trên bộ quét. Tuy nhiên, mục tiêu trên ma trận đầy đủ chưa đạt, kiến trúc mới chưa được kiểm chứng và ứng dụng chưa xây. Mục đích buổi gặp là xin góp ý và xác nhận khung đề tài.

### EN — Speaker script

Today I will present my proposed thesis on predicting degron mutation effects at residue resolution. Rather than asking only whether a protein segment contains a degradation signal, I ask how replacing one amino acid at a particular position changes the stability of the peptide.

I will first introduce the biology and the experimental measurement, then review prior work and the evidence collected so far. I have reconstructed the experimental labels and trained ridge models, with a positive result on the scanning dataset. The full substitution-matrix target remains unmet; the new architecture and software are still work ahead. The purpose of this meeting is to discuss and seek approval of the thesis framework.

### Đọc hiểu / Study notes

- **Residue-level** nói về độ phân giải đầu ra: một vị trí hoặc một thay thế cụ thể. Nó không tự có nghĩa là giải thích được cơ chế phân tử.
- **Experimental protein-stability data** là dữ liệu người khác đo trong tế bào; công việc của em gồm xử lý, kiểm chứng lại và học từ dữ liệu đó, không phải tự thực hiện thí nghiệm ướt.
- **EN:** Separate the source of experimental measurements from the computational work performed in this thesis. “Proposed thesis” describes the approval state, not an absence of completed analysis.

**Hỏi sâu / Q&A:** “Đã có mô hình cuối cùng chưa?” — “Chưa. Em đã có các baseline ridge, còn thiết kế kiến trúc và phép so cuối.” / “Is there a final model?” — “Not yet. The ridge baselines are measured; architecture selection and final comparisons remain open.”

**Chuyển / Transition:** “Trước hết, em làm rõ đối tượng mà mô hình sẽ đọc.” / “First, let me define the object the model operates on.”

**Nguồn / Sources:** [Trạng thái](../../../../DECISIONS.md#hien-hanh) · [Kết quả ridge](../../research/residue-task-derisk-2026-10-15/README.md).

---

<a id="slide-02"></a>

## Slide 2 — Protein, residue và đột biến / Proteins are chains of residues

**Thông điệp / Message:** Tách vị trí trong chuỗi khỏi loại amino acid chiếm vị trí đó. / Distinguish a sequence position from the amino acid at that position.

### VI — Lời thuyết trình

Protein là chuỗi amino acid, tham gia các công việc như xúc tác, truyền tín hiệu và vận chuyển trong tế bào. Khi một amino acid đã nằm trong chuỗi, ta gọi nó là một residue. Trong bài toán này, em dùng số thứ tự để chỉ vị trí residue và ký tự để chỉ loại amino acid ở vị trí đó.

Ví dụ chuỗi trên hình là MKTAYIAK. Vị trí thứ bảy chứa A, tức alanine. Nếu thay A bằng V, tức valine, ta viết A7V; chuỗi mới là MKTAYIVK. Độ dài chuỗi vẫn giữ nguyên, chỉ một phần tử thay đổi.

Phân biệt này dẫn tới ma trận đầu ra: 28 hàng là 28 vị trí; 20 cột là 20 loại amino acid có thể đặt tại mỗi vị trí. Trình tự và ngữ cảnh ảnh hưởng cấu trúc, chức năng, nhưng đề tài này tập trung vào một đầu ra cụ thể: thay đổi độ bền trong assay.

### EN — Speaker script

Proteins are amino acid chains that carry out cellular functions such as catalysis, signalling and transport. An amino acid incorporated into the chain is called a residue. Here, a number identifies the residue position, while a letter identifies the amino acid occupying it.

In the displayed sequence, MKTAYIAK, position seven contains alanine, A. Replacing it with valine gives A7V and produces MKTAYIVK. The chain length stays the same; one element changes.

This distinction defines our output matrix: 28 rows for positions and 20 columns for amino acid types. Sequence and context influence structure and function, while this thesis predicts a specific measured consequence: peptide stability in the assay.

### Đọc hiểu / Study notes

- Ví von phần mềm: chuỗi giống một mảng; **index** khác **value**. `A7V` mô tả phần tử cần sửa, giá trị cũ và giá trị mới. Trong sinh học vị trí thường đếm từ **1**; trong code mảng thường bắt đầu từ **0**.
- **28×20 không phải 28×28:** đây là bản đồ vị trí × loại thay thế, không phải ma trận tương tác giữa hai vị trí. Mỗi hàng có 19 thay thế khác WT và một ô giữ nguyên amino acid.
- **EN:** A residue is the chemical unit within a chain; “position” is how we index it computationally. The matrix describes single substitutions, not pairwise interactions or simultaneous multiple mutations.

**Hỏi sâu / Q&A:** “Thay hai vị trí cùng lúc có nằm trong đầu ra này không?” — “Không. Đầu ra hiện tại là các thay thế đơn; không cộng hai điểm để mặc nhiên suy ra hiệu ứng kép.” / “Does the matrix cover double mutants?” — “No. Single-mutant effects do not establish additive double-mutant effects.”

**Chuyển / Transition:** “Vậy vì sao thay đổi độ bền của một protein lại quan trọng?” / “Why does a change in protein stability matter?”

**Lưu ý hình / Figure note:** Khi trỏ chuỗi này, đọc **A7V**; bản HTML khi rà cuối đã sửa nhãn, khác bản paste ban đầu.

---

<a id="slide-03"></a>

## Slide 3 — Tổng hợp và phân hủy / Synthesis against degradation

**Thông điệp / Message:** Độ dồi dào phụ thuộc cả tạo mới lẫn loại bỏ protein. / Abundance depends on production and removal.

### VI — Lời thuyết trình

Lượng protein có mặt trong tế bào không chỉ do tế bào sản xuất bao nhiêu. Nó còn phụ thuộc protein bị phân hủy nhanh đến mức nào. Diễn đạt đúng bằng công thức: tốc độ thay đổi lượng protein bằng tốc độ tổng hợp trừ tốc độ phân hủy.

Nếu lượng tạo mới giữ nguyên nhưng tốc độ phân hủy tăng, lượng protein có thể giảm. Khi hai tốc độ cân bằng, lượng protein có thể ổn định dù tế bào vẫn liên tục tạo và phá protein.

Phân hủy là một tầng điều hòa: tế bào cần tắt tín hiệu đúng lúc, loại bỏ protein hỏng và thích ứng với điều kiện mới. Vì vậy, một biến thể có thể ảnh hưởng chức năng mà không làm protein ngừng được tổng hợp; nó có thể làm protein tồn tại lâu hơn hoặc ngắn hơn. Đề tài tập trung vào tầng điều hòa độ bền đó.

### EN — Speaker script

Protein abundance is determined by both synthesis and degradation. More precisely, the rate of change of protein amount equals the synthesis rate minus the degradation rate.

If production stays constant while degradation increases, protein abundance can fall. At steady state, production and removal balance, even though both processes continue.

Degradation is therefore a regulatory layer. Cells use it to switch signals off, clear damaged proteins and respond to changing conditions. A variant may affect a protein without stopping its production: it may change how long that protein persists. This thesis focuses on sequence-dependent effects on that stability layer.

### Đọc hiểu / Study notes

`dP/dt = s − d` là phương trình cân bằng đơn giản: `P` là lượng protein, `s` và `d` cùng đơn vị lượng/thời gian. Nếu thêm giả định minh họa `d = kP`, thì thời gian tồn tại liên quan đến `k`; đây là mô hình giải thích, **không phải phép fit của đề tài**.

Ví von: một hàng đợi có luồng thêm việc và luồng lấy việc ra. Độ dài hàng đợi là trạng thái; hiệu hai tốc độ là mức tăng/giảm trạng thái. Bởi vậy dòng “amount = rate − rate” trên slide cần được đọc thành “change in amount”.

**EN:** Abundance is a state; synthesis and degradation are rates. A fluorescence-based abundance measurement is not automatically a direct half-life measurement, because other cellular processes can also affect the reporter.

**Hỏi sâu / Q&A:** “Đo độ dồi dào có bằng đo tốc độ phân hủy không?” — “Không hoàn toàn. Assay cung cấp chỉ số độ bền tương đối trong điều kiện kiểm soát; đề tài không đổi PSI thành thời gian bán hủy.” / “Does abundance directly give degradation rate?” — “No. PSI is a relative assay score, not a half-life in hours.”

**Chuyển / Transition:** “Một hệ thống giúp tế bào loại bỏ protein có chọn lọc là UPS.” / “One major system for selective removal is the UPS.”

---

<a id="slide-04"></a>

## Slide 4 — Hệ ubiquitin–proteasome / The ubiquitin–proteasome system

**Thông điệp / Message:** Tín hiệu nhận diện nối trình tự protein với quá trình phân hủy có chọn lọc. / Recognition signals connect sequence to selective degradation.

### VI — Lời thuyết trình

Hệ ubiquitin–proteasome, viết tắt UPS, là một cơ chế phân hủy protein có chọn lọc. Em tóm tắt thành ba bước theo hình. Thứ nhất, bộ máy chứa E3 nhận diện tín hiệu phù hợp trên protein đích. Thứ hai, hệ enzyme gắn ubiquitin lên đích; một số kiểu chuỗi ubiquitin tạo tín hiệu cho bước xử lý tiếp theo. Thứ ba, proteasome nhận diện đích thích hợp, tháo cuộn và phân cắt thành các peptide ngắn.

Sơ đồ lược bỏ E1 và E2 để tập trung vào câu hỏi nhận diện; E3 không làm toàn bộ quá trình một mình. Theo công trình DegronMD được trích trên slide, người có hơn 600 E3 ligase, với các tập đích khác nhau và có thể chồng lặp.

Đề tài không dự đoán E3 nào nhận protein nào. Em đi vào tín hiệu trình tự mà hệ thống có thể đọc: degron, và các residue góp phần tạo nên tín hiệu đó.

### EN — Speaker script

The ubiquitin–proteasome system, or UPS, supports selective protein degradation. The diagram simplifies it into three stages. First, E3-containing machinery recognises a suitable signal on a target. Second, the ubiquitination enzyme system attaches ubiquitin; particular chain configurations can support downstream degradation. Third, the proteasome recognises an appropriate substrate, unfolds it and cuts it into shorter peptides.

E1 and E2 are omitted here to keep the focus on recognition; E3 does not perform every stage alone. DegronMD reports more than 600 human E3 ligases with different, potentially overlapping target sets.

This thesis does not predict E3 identity. It studies the sequence signal and the residues that influence its measured activity.

### Đọc hiểu / Study notes

- **Ubiquitin:** protein nhỏ được gắn lên đích. Không phải mọi dấu ubiquitin đều có nghĩa “phân hủy”; hình chỉ minh họa nhánh liên quan tới proteasome.
- **E3 ligase:** thành phần giúp tạo tính chọn lọc của ubiquitination; không phải tên gọi khác của proteasome.
- **Proteasome:** bộ máy phân cắt protein; degron là tín hiệu trên đích, không phải bộ máy phân cắt.
- **EN:** The three-stage drawing is explanatory, not a measured mechanistic pathway for every peptide in the dataset. Reporter stabilisation alone cannot identify an E3 or establish direct binding.

**Hỏi sâu / Q&A:** “Dự đoán residue có suy ra được E3 không?” — “Không. Nhiệm vụ này thiếu nhãn E3 đủ rộng; điểm ΔPSI mô tả thay đổi reporter, không xác định phân tử nhận diện.” / “Can the prediction identify an E3?” — “No. Mutation-effect labels do not establish E3 identity or direct recognition.”

**Chuyển / Transition:** “Tín hiệu trên protein mà sơ đồ vừa nhắc tới được gọi là degron.” / “The recognition signal on the target is called a degron.”

**Nguồn / Sources:** Tiền lệ sinh học được trích trong [slide nguồn](index.html); [phạm vi đề tài](../../../../DECISIONS.md#d-031).

---

<a id="slide-05"></a>

## Slide 5 — Từ degron đến footprint / A degron is the recognition signal

**Thông điệp / Message:** Xác định đoạn degron chưa trả lời residue nào góp phần vào hoạt tính của nó. / Locating a degron does not identify each residue's contribution.

### VI — Lời thuyết trình

Degron là tín hiệu trên protein góp phần khiến protein được bộ máy phân hủy nhận diện. Có thể hình dung nó như nhãn địa chỉ, nhưng nhãn này chỉ hoạt động trong bối cảnh sinh học phù hợp. Tín hiệu có thể ở đầu N, đầu C hoặc bên trong chuỗi, và hoạt tính có nhiều mức độ.

Hình phóng từ cả protein xuống đoạn peptide dài 28 residue, rồi xuống từng residue. Câu hỏi của em nằm ở tầng cuối: thay một amino acid tại từng vị trí làm độ bền thay đổi bao nhiêu? Một tập vị trí nhạy với thay thế tạo nên footprint đo được của degron.

Phạm vi cần nói ngay là peptide gắn reporter trong assay. Đề tài ưu tiên các tín hiệu biểu hiện hoạt tính trong ngữ cảnh đó, gọi là degron tự trị theo phạm vi đang dùng. Tín hiệu cần bối cảnh bị thiếu trong assay có thể không hiện ra. Dự đoán này chưa xác nhận tác động trên protein nguyên vẹn.

### EN — Speaker script

A degron is a signal that contributes to a protein being recognised by degradation machinery. An address label is a useful analogy, but the signal still depends on its biological context. It may occur at either terminus or internally, and its activity is graded.

The diagram zooms from the whole protein to a 28-residue peptide, then to individual positions. My question concerns that final scale: how much does each substitution change stability? Positions that respond strongly to substitutions form a measured degron footprint.

The scope is the peptide–reporter assay. We study signals active in that context. A degron requiring context absent from the assay may be missed, and peptide-level predictions do not establish effects in intact proteins.

### Đọc hiểu / Study notes

**Footprint ở đây là định nghĩa thao tác bằng đột biến**, không phải ảnh chụp các nguyên tử tiếp xúc E3. Một residue có thể làm tín hiệu yếu đi khi bị thay vì nhiều lý do: tương tác, khả năng tiếp cận hoặc bối cảnh cục bộ. Phép đo một mình không phân biệt hết các lý do.

“Tự trị” không có nghĩa là không cần bất kỳ enzyme hay điều kiện tế bào nào. Nó có nghĩa tín hiệu có thể biểu hiện trong đoạn reporter đang xét. HIF1A ở slide 16 có liên quan hydroxyl hóa nhưng vẫn hiện ra trong assay; vì vậy không nói mọi degron cần biến đổi sau dịch mã đều tuyệt đối không đo được.

**EN:** A mutational footprint is an operational phenotype, not a direct contact map. Assay activity depends on the cellular context retained by the experiment.

**Hỏi sâu / Q&A:** “Một vị trí không có hiệu ứng có chắc không quan trọng không?” — “Chưa chắc. Có thể thay thế được thử vẫn bảo toàn tín hiệu, hoặc điều kiện assay không thể hiện vai trò đó.” / “Does a weak effect prove irrelevance?” — “No. It is conditional on the substitution, assay and measurement precision.”

**Chuyển / Transition:** “Tiếp theo là bằng chứng cho thấy vùng degron đáng được nghiên cứu.” / “Next, I will show why degron regions are worth studying.”

**Nguồn / Sources:** [D-035](../../../../DECISIONS.md#d-035) · [đối chiếu phạm vi assay](../../research/variant-coverage-2026-10-15/README.md).

---

<a id="slide-06"></a>

## Slide 6 — Ý nghĩa ở mức vùng / Disease variants in degron regions

**Thông điệp / Message:** Có liên hệ với phân loại gây bệnh ở mức vùng; chưa xác lập mắt nối ở mức residue. / Region-level enrichment does not establish residue-level disease prediction.

### VI — Lời thuyết trình

Để kiểm động lực của bài toán, em ánh xạ khoảng 2,56 triệu biến thể missense ClinVar lên bản đồ peptide đã đo. So sánh biến thể gây bệnh với lành tính trong cùng protein, phép phân tầng Mantel–Haenszel cho odds ratio 2,148, khoảng tin cậy 95% từ 2,072 đến 2,227. Nghĩa là trong thiết kế so sánh này, vị trí nằm trong vùng degron có liên hệ với chênh lệch phân loại gây bệnh/lành tính.

Em giữ ba giới hạn cạnh con số: đây là mức vùng; biến thể không tập trung theo vị trí vào degron vượt nền một cách đã thiết lập; và chưa kiểm soát bảo tồn cùng độ vô trật tự.

Trong các vùng đó có 530.412 VUS, tức biến thể chưa rõ ý nghĩa. Chúng tạo động lực nghiên cứu hiệu ứng peptide, nhưng không là nhãn xác nhận mô hình. Các phép đối chiếu hiện có chưa xác lập rằng residue phá degron mạnh hơn cũng mang tín hiệu bệnh mạnh hơn. Em không dùng kết quả để phân loại gây bệnh hay suy ra hiệu quả điều trị.

### EN — Speaker script

To examine the motivation, I mapped approximately 2.56 million ClinVar missense variants onto the experimentally measured peptide map. A within-protein Mantel–Haenszel analysis gives an odds ratio of 2.148, with a 95% interval of 2.072 to 2.227, for the pathogenic-versus-benign association with degron-region membership.

Three limits accompany that result: it is region-level evidence; there is no established positional over-representation beyond the background; and conservation and disorder have not yet been controlled for.

These regions contain 530,412 variants of uncertain significance. They motivate studying peptide effects, but they are not model-validation labels. Our residue-level analyses have not established a disease association. The thesis does not classify pathogenicity or claim therapeutic effects.

### Đọc hiểu / Study notes

- **Missense:** biến thể làm đổi amino acid. **VUS:** variant of uncertain significance, chưa đủ bằng chứng để phân loại ý nghĩa lâm sàng.
- **Odds ratio không phải risk ratio:** 2,148 không có nghĩa “mỗi biến thể trong degron có xác suất gây bệnh cao gấp 2,148”, càng không phải 214,8% nguy cơ.
- **Phân tầng theo protein:** so bên trong các protein để hạn chế việc gene bệnh được chú ý nhiều hơn. Nó không tự loại các yếu tố gây nhiễu khác.
- Mắt nối residue: tầng có lực nhất cho AUC **0,5166 [0,479; 0,554]**; tầng khớp đúng ô chỉ **51 ca**, AUC **0,6738 [0,489; 0,831]**. Cả hai CI chứa 0,5; không chọn riêng 0,6738 để kể như kết quả dương.
- **EN:** The analysis is observational and region-level. It supports motivation, not a causal disease mechanism or a clinical validation endpoint.

**Hỏi sâu / Q&A:** “Vậy mô hình có giải thích được VUS không?” — “Nó có thể gợi ý hiệu ứng độ bền của peptide để ưu tiên nghiên cứu tiếp. Nó chưa giải thích vì sao VUS gây bệnh.” / “Can it explain a VUS?” — “It can suggest a peptide-stability hypothesis, not establish pathogenicity.”

**Chuyển / Transition:** “Để hiểu chính xác mô hình dự đoán gì, cần nhìn cách nhãn độ bền được đo.” / “To define the prediction, we need to examine how stability labels are measured.”

**Nguồn / Sources:** [Báo cáo độ phủ, §6 và §8b](../../research/variant-coverage-2026-10-15/README.md) · [D-036](../../../../DECISIONS.md#d-036).

---

<a id="slide-07"></a>

## Slide 7 — GPS, PSI và ΔPSI / How stability is measured

**Thông điệp / Message:** PSI là chỉ số thực nghiệm; chiều hiệu ứng phải luôn nhất quán. / PSI is an assay score with a fixed direction.

### VI — Lời thuyết trình

Trong GPS, Global Protein Stability profiling, thư viện peptide được gắn với reporter huỳnh quang. Tế bào còn có reporter đối chiếu để giảm ảnh hưởng của khác biệt biểu hiện. FACS, tức phân loại tế bào bằng huỳnh quang, chia tế bào vào các bin theo tỉ số tín hiệu; giải trình tự sau đó cho biết mỗi construct nằm ở các bin nào.

Với dữ liệu Zhang em dùng, có sáu bin và chỉ số PSI nằm từ 1 đến 6. PSI thấp nghĩa reporter kém bền hơn; PSI cao nghĩa reporter bền hơn. WT, hay wild type, là trình tự tham chiếu chưa thay thế trong phép so, không có nghĩa là không có degron.

Hiệu ứng đột biến là ΔPSI bằng PSI mutant trừ PSI WT. Giá trị dương nghĩa thay thế làm reporter bền hơn trong assay. Đó là bằng chứng vị trí có thể góp phần vào hoạt tính phân hủy của trình tự ban đầu; chưa đủ để kết luận E3 trực tiếp nhận vị trí đó.

### EN — Speaker script

In Global Protein Stability profiling, peptides are fused to a fluorescent reporter. A reference reporter helps control for differences in expression. Fluorescence-activated cell sorting, or FACS, separates cells into bins using the reporter ratio. Sequencing then identifies the distribution of each construct across bins.

The Zhang dataset uses six bins and a PSI scale from one to six. Low PSI means a less stable reporter; high PSI means a more stable reporter. Wild type, or WT, is the reference sequence for the comparison.

Mutation effect is defined as PSI of the mutant minus PSI of WT. Positive ΔPSI indicates reporter stabilisation. This supports a contribution to the measured degradation phenotype, but it does not prove direct E3 recognition.

### Đọc hiểu / Study notes

- **Construct:** đơn vị trình tự được thiết kế và đo, ví dụ một peptide WT hay một mutant. Nó không đồng nhất với một người bệnh, một protein độc lập hay một mẫu sinh học độc lập.
- **Ví dụ giả định để học:** WT PSI = 2, mutant PSI = 4 thì ΔPSI = +2. Reporter bền hơn; degron ban đầu có thể bị suy yếu. Đây là phép tính minh họa, không phải số thực nghiệm mới.
- **Hai ngưỡng đang dùng:** peptide degron nếu `PSI_WT ≤ 3.0`; ô “rescue” dương nếu `ΔPSI ≥ 1.0`. Dương theo nhãn benchmark khác với chỉ `ΔPSI > 0`.
- **EN:** A positive numerical effect and a positive binary benchmark label are different. The benchmark uses a rescue threshold of one PSI unit; PSI is neither a probability nor a time measurement. Bin counts and score directions differ across datasets and must be checked before transfer.

**Hỏi sâu / Q&A:** “ΔPSI = +0,2 có được tính là ô dương không?” — “Nó là hiệu ứng hướng làm bền, nhưng chưa đạt ngưỡng rescue +1,0 của benchmark.” / “Is +0.2 a positive benchmark label?” — “It is a stabilising signed effect, but it is below the benchmark's +1.0 rescue threshold.”

**Chuyển / Transition:** “Với quy ước đó, em phân nhóm các tiền lệ theo nhãn và đơn vị đầu ra.” / “With that convention established, I will compare prior work by labels and output unit.”

**Nguồn / Sources:** [Từ điển dữ liệu](../../data/README.md) · [bộ nạp nhãn](../../research/residue-task-derisk-2026-10-15/residue_data.py).

---

<a id="slide-08"></a>

## Slide 8 — Bản đồ tiền lệ / Prior work at a glance

**Thông điệp / Message:** So sánh theo câu hỏi, nhãn và đơn vị đầu ra, không chỉ theo tên mô hình. / Compare tasks, labels and outputs before comparing model scores.

### VI — Lời thuyết trình

Em chia tiền lệ thành ba nhóm. Nhóm thứ nhất tìm vùng hoặc motif degron từ các chú giải và đặc trưng đã biết, như Degpred, DegronMD, DEGRONOPEDIA và MetaDegron. Nhóm thứ hai cung cấp bản đồ thực nghiệm và mô hình điểm toàn đoạn: Koren, Zhang, Voutsinos với PAP, cùng bộ tile của Larsen. Nhóm thứ ba, ở slide sau, là các mô hình hiệu ứng biến thể liên quan nhưng khác đích dự đoán.

Cột cần đọc nhất là nhãn và đơn vị đầu ra. Điểm cả peptide không tự thành một đầu ra mức vị trí được giám sát trực tiếp. Tuy nhiên, có thể chạy lại mô hình trên các mutant để tạo bản đồ hiệu ứng. Degformer đã làm điều đó và đã xuất ma trận 28×20 từ dữ liệu Zhang. Vì vậy, em không nhận ma trận này là đầu ra chưa ai có. Phần em cần chứng minh nằm ở mục tiêu học, điều kiện đánh giá, lợi ích phương pháp và cách báo bất định.

### EN — Speaker script

I organise prior work by the question it answers. Motif and database tools locate degron candidates using curated knowledge and sequence or structural features. Experimental mapping studies provide measured segment-level labels and models such as PAP. Adjacent variant-effect methods address related but different endpoints.

The key columns are label type and output unit. A peptide-level score is not a directly supervised residue-level output, although repeated scoring of mutants can produce a mutation map. Degformer already produces a 28-by-20 matrix from Zhang's data. I therefore do not claim that this matrix format is new. The contribution must be demonstrated through the learning objective, evaluation conditions, method and uncertainty reporting.

### Đọc hiểu / Study notes

Đọc bảng theo ba câu: **đo cái gì → học cái gì → xuất cái gì**. “Có đầu ra theo vị trí” và “được huấn luyện bằng nhãn hiệu ứng theo vị trí” là hai thuộc tính khác nhau. Một mô hình cho điểm toàn đoạn vẫn có thể được đánh giá trên các thay thế đơn bằng phép lấy hiệu.

Larsen được nguồn của deck ghi là **preprint**; Degformer là **repo GitHub, không bài báo trong hồ sơ đã đọc**. Không dùng các nhãn này để đánh giá chất lượng thay cho kiểm chứng. Dòng chú giải “only the last row” ở HTML không được dùng để phủ nhận ma trận của Degformer.

**EN:** Resolution, supervision and evidence status are separate dimensions. The table is a map of prior work, not a fair leaderboard of methods evaluated on the same benchmark.

**Hỏi sâu / Q&A:** “Vậy khác Degformer ở đâu?” — “Cần kiểm bằng cùng giao thức: học và đánh giá hiệu ứng residue, split cụm, bất định và xuất xứ. Kết quả thắng Degformer hiện chưa có.” / “How is this different from Degformer?” — “The proposed distinction concerns evaluation, learning and uncertainty; a performance advantage has not yet been measured.”

**Chuyển / Transition:** “Em đi vào điểm mạnh và giới hạn của nhóm motif trước.” / “I will start with the strengths and limits of motif-based tools.”

**Nguồn / Sources:** [Bảng tiền lệ trong deck](index.html) · [đối soát Degformer](../../research/larsen-nuclear-and-risks-2026-10-15/README.md).

---

<a id="slide-09"></a>

## Slide 9 — Công cụ motif và cơ sở dữ liệu / Motif and database tools

**Thông điệp / Message:** Công cụ tìm vùng degron hữu ích, nhưng endpoint khác dự đoán ΔPSI từng thay thế. / Degron annotation and measured mutation-effect prediction are different endpoints.

### VI — Lời thuyết trình

Điểm mạnh của nhóm này là đưa việc tìm degron từ các motif rời rạc tới mức protesome và cung cấp công cụ có thể sử dụng. Chúng kết hợp các thông tin như motif, vị trí ubiquitination, cấu trúc, vùng vô trật tự hoặc E3. Đây là tiền lệ quan trọng cho cả phương pháp và phần mềm của đề tài.

Giới hạn liên quan tới bài toán của em là loại nhãn. Nhãn chú giải “đây là degron” khác với phép đo “đổi amino acid này làm PSI tăng bao nhiêu”. Tương tự, phân biệt degron đã biết với peptide ngẫu nhiên không đồng nhất với phân biệt các đột biến có và không làm bền reporter trong cùng một degron.

Vì vậy, không lấy AUC công bố của các công cụ rồi xếp cạnh AUROC của em để kết luận thắng hoặc thua. Em cũng chỉ nói rò rỉ đồng dạng chưa được loại trừ trong hồ sơ đã đọc, không nói đã chứng minh các công cụ đó bị rò rỉ.

### EN — Speaker script

These tools have made degron annotation more scalable and usable. They combine information such as motifs, ubiquitination sites, disorder, structure and E3 associations. They are meaningful precedents for both the scientific task and the software.

For this thesis, the relevant limitation is the label endpoint. A curated degron annotation does not measure the PSI change caused by a particular substitution. Distinguishing known degrons from random peptides also differs from distinguishing stabilising and non-stabilising mutations within one degron.

Their published AUCs therefore cannot be directly ranked against this benchmark. Where similarity control was not verified, I describe an unresolved question, rather than claiming demonstrated leakage.

### Đọc hiểu / Study notes

**Curated** nghĩa là được tổng hợp, chú giải và sàng lọc từ nguồn tri thức; không có nghĩa “sai” hay “không có thực nghiệm ở nguồn gốc”. Vấn đề là nhãn đó có trả lời đúng endpoint đang học hay không.

Chất lượng đối chứng âm ảnh hưởng độ khó: peptide ngẫu nhiên có thể khác mẫu dương theo nhiều đặc trưng dễ học; biến thể trong cùng một peptide kiểm tra một khác biệt tinh hơn. Không suy từ đó rằng mọi AUC của tiền lệ đều bị thổi phồng.

**EN:** Endpoint mismatch is the reason to build a task-specific comparison. Absence of a documented feature or split protocol is not proof of absence. Degpred remains abstract-level evidence in the source notes and should not support detailed architecture claims.

**Hỏi sâu / Q&A:** “Tại sao không chỉ dùng MetaDegron?” — “Nó có ích cho câu hỏi nhận diện degron; muốn dùng cho ΔPSI phải xây phép chuyển điểm và đánh giá trên nhãn đột biến, không dùng nguyên AUC của bài.” / “Why not use MetaDegron directly?” — “Its scores need task-specific evaluation before they support mutation-effect claims.”

**Chuyển / Transition:** “Nhóm tiếp theo gần bài toán hơn vì cung cấp dữ liệu đo.” / “The next group is closer because it supplies measured data.”

**Nguồn / Sources:** Ghi chú mức bằng chứng của [slide 9](index.html) · [khảo sát rủi ro và công cụ](../../research/larsen-nuclear-and-risks-2026-10-15/README.md).

---

<a id="slide-10"></a>

## Slide 10 — Bản đồ thực nghiệm và PAP / Measured maps and sequence models

**Thông điệp / Message:** Ghi nhận tiền lệ gần nhất; khoanh đúng giới hạn của kênh mô hình đã kiểm. / Recognise the closest precedent and bound the tested architectural limitation.

### VI — Lời thuyết trình

Koren đặt nền cho sàng lọc độ bền; Zhang bổ sung đột biến quét và bão hòa, là nguồn nhãn hiệu ứng chính ở đây. Voutsinos cung cấp bản đồ tile quy mô lớn và PAP, còn Larsen mở sang tile của các yếu tố phiên mã. Các số hiệu năng toàn đoạn trên slide là số tác giả báo, không phải kết quả residue của đề tài.

Em đã dựng lại PAP từ trọng số công bố và kiểm một tính chất cụ thể: kênh nội cnn2w1 dùng convolution cửa sổ 1 rồi gộp trung bình. Trong phạm vi kênh đó, hoán vị thứ tự residue không đổi điểm. Đây là giới hạn của biểu diễn thành phần, không phải kết luận PAP đầy đủ không nhìn được vị trí.

Degformer là tiền lệ trực tiếp cần đối chứng vì đã xuất ma trận thay thế. Audit hiện có ghi nhận 4,09% trùng trình tự trong phép chia ngẫu nhiên đã kiểm. Con số tự báo của repo là tương quan Pearson; em chưa có kết quả tái đánh giá công bằng để tuyên bố thắng nó.

### EN — Speaker script

Zhang's scanning and saturation experiments supply the main mutation-effect labels. Voutsinos provides the tile map and PAP model, while Larsen extends mapping to transcription-factor tiles. The segment-level performance numbers shown here are the authors' results.

I reconstructed PAP from released weights and tested a specific property: its internal cnn2w1 channel uses a width-one convolution followed by average pooling. That channel is invariant to residue permutation. This is a limitation of the composition-only representation, not a claim about the full PAP model or cnn2w7.

Degformer is the most direct precedent because it already generates substitution matrices. The existing audit measured 4.09% identical-sequence overlap in the investigated random split. Its reported correlations are Pearson correlations. A controlled performance comparison remains outstanding.

### Đọc hiểu / Study notes

`Conv1D(kernel=1)` xử lý mỗi amino acid bằng cùng một hàm; `GlobalAveragePooling` lấy trung bình các kết quả. Đổi chỗ phần tử không đổi tổng. Thêm nhánh đầu C hoặc dùng cửa sổ lớn hơn làm giả thiết “chỉ có thành phần” không còn tự động đúng.

**ΔPAP** là `PAP(mutant) − PAP(WT)`, được dùng làm điểm đối chứng hiệu ứng. Đây là cách áp dụng mô hình điểm toàn đoạn ngoài mục tiêu huấn luyện ban đầu. Việc tạo ma trận bằng nhiều lần suy luận không tự là lỗi; phải so độ đúng, chi phí và điều kiện đánh giá.

**EN:** Do not transfer the invariance proof to a larger architecture that violates its assumptions. Likewise, 4.09% exact overlap does not quantify all possible homology leakage and does not prove every prediction is invalid.

**Hỏi sâu / Q&A:** “PAP chỉ dùng thành phần thì vì sao vẫn có bản đồ không phẳng?” — “Các vị trí có WT hoặc amino acid thay vào khác nhau vẫn có thể cho điểm khác. Ràng buộc bằng nhau chỉ áp cho cùng peptide và cùng cặp thay thế.” / “Why can its map vary?” — “Different substitution pairs may score differently; only equal pairs are forced to tie.”

**Chuyển / Transition:** “Ngoài lĩnh vực degron, có các chuẩn đối chứng phương pháp cần học.” / “Adjacent fields also provide useful methodological controls.”

**Nguồn / Sources:** [Tái lập PAP](../../research/pap-baseline/README.md) · [cận thành phần, §3](../../research/composition-context-audit.md) · [audit Degformer](../../research/larsen-nuclear-and-risks-2026-10-15/README.md).

---

<a id="slide-11"></a>

## Slide 11 — Các mô hình hiệu ứng biến thể lân cận / Adjacent variant-effect models

**Thông điệp / Message:** Học đối chứng và cách đánh giá từ bài gần lĩnh vực, giữ endpoint riêng. / Adopt relevant controls while keeping endpoints distinct.

### VI — Lời thuyết trình

AlphaMissense hỏi về tính gây bệnh; các phép đo VAMP-seq và nghiên cứu của Schulze cùng Lindorff-Larsen tập trung vào độ dồi dào protein; LeBlanc phân tích hoạt tính miền kích hoạt. Chúng không cùng endpoint với ΔPSI peptide degron nên không phải bảng đối thủ trực tiếp.

Điều em tiếp thu là chuẩn đánh giá: so với baseline đơn giản, kiểm mô hình có học được ngữ cảnh hay chỉ thành phần, tách theo cụm protein, và báo độ ổn định cùng mức lặp lại của nhãn. Nếu cấu trúc thực sự có thông tin phù hợp, baseline theo mức chôn vùi hoặc phơi lộ cũng cần được xem xét ở phần chuyển giao.

Đề tài chỉ bổ sung một giả thuyết hiệu ứng độ bền trong hệ đo cụ thể. Em không nói nó cung cấp lời giải cơ chế gây bệnh mà AlphaMissense thiếu. Khi mượn quy ước phân tích từ tiền lệ, em ghi nguồn; đó không phải phát minh của đề tài.

### EN — Speaker script

AlphaMissense addresses pathogenicity, abundance studies address protein levels, and LeBlanc examines activation-domain behaviour. These endpoints differ from peptide degron ΔPSI, so their headline scores are not direct competitors.

What I adopt is the evaluation discipline: compare against simple baselines, separate composition from context, split by protein cluster, and report stability across seeds and bootstraps alongside label reproducibility. Structural baselines are relevant where the structural information and transfer endpoint support them.

This thesis adds a hypothesis about an assay-specific stability effect. It does not establish a disease mechanism. Methods adopted from prior work are attributed rather than claimed as new contributions.

### Đọc hiểu / Study notes

**rASA** là độ tiếp cận dung môi tương đối, mô tả amino acid nằm lộ hay bị chôn trong cấu trúc; **pLDDT** là điểm độ tin cậy cục bộ của cấu trúc dự đoán, không phải xác suất degron. Cấu trúc protein nguyên vẹn không tự mô tả cấu trúc peptide đã tách ra gắn reporter.

**Seed stability** kiểm sự nhạy với ngẫu nhiên của quy trình; **bootstrap stability** kiểm sự nhạy với việc lấy lại mẫu dữ liệu. Trọng số ổn định không tự chứng minh cơ chế đúng.

**EN:** Structural exposure, confidence in a predicted structure and experimental mutation effects are different quantities. More features are useful only if their biological context and validation support the intended claim.

**Hỏi sâu / Q&A:** “Đã có AlphaMissense thì có cần đề tài này?” — “Có một câu hỏi khác cần đo: thay thế có làm bền reporter chứa degron không. Điểm đó có thể bổ sung nghiên cứu chức năng, nhưng không thay phân loại bệnh.” / “Why study this alongside AlphaMissense?” — “It measures a different functional endpoint and does not replace pathogenicity prediction.”

**Chuyển / Transition:** “Từ các tiền lệ, em có thể phát biểu một giới hạn biểu diễn cụ thể.” / “These comparisons lead to a specific representation limit.”

**Nguồn / Sources:** [Khảo sát tiền lệ và rủi ro](../../research/larsen-nuclear-and-risks-2026-10-15/README.md) · [giới hạn tuyên bố bệnh](../../../../DECISIONS.md#d-036).

---

<a id="slide-12"></a>

## Slide 12 — Giới hạn có thể chứng minh / The provable gap

**Thông điệp / Message:** Cùng thành phần và cùng cặp thay thế buộc mô hình thành phần cho cùng dự đoán, dù nhãn khác nhau. / Composition-only models must tie equal substitution pairs within a peptide.

### VI — Lời thuyết trình

Giả sử mô hình chỉ đọc số lượng từng loại amino acid trong peptide, gọi là vector thành phần c. Thay a thành b làm vector đó đổi thành c trừ một a, cộng một b. Hiệu dự đoán bằng f của thành phần mới trừ f của thành phần ban đầu; công thức không chứa chỉ số vị trí.

Vì vậy, trong cùng peptide, thay cùng a thành b ở hai vị trí khác nhau bắt buộc có cùng dự đoán. Nhưng trên tập audit gồm 2.624 peptide có footprint, có 2.353 peptide, tức 89,7%, chứa nhóm cùng cặp thay thế mà nhãn có cả dương và không dương. Lớp mô hình này không thể tách hoàn toàn các ô đó.

Đây là giới hạn đối với nhãn quan sát và giả thiết mô hình, không phải bằng chứng rằng toàn bộ khác biệt là tín hiệu sinh học học được. Kết quả huấn luyện sau đó cung cấp bằng chứng bổ sung: ngữ cảnh ±3 giúp tăng AUROC 0,0289. Phần lớn mức tăng đến từ thành phần lân cận, không phải chỉ số vị trí tuyệt đối.

### EN — Speaker script

Suppose a model sees only the amino acid composition vector, c. Replacing a with b changes it to c minus one a plus one b. The predicted effect is the new score minus the original score; the expression contains no position index.

Within one peptide, equal substitution pairs must therefore receive equal predictions. In the audited set of 2,624 footprint peptides, 2,353, or 89.7%, contain an equal-pair group with both positive and non-positive measured labels. A composition-only model cannot perfectly separate those cells.

This is a limit under explicit model assumptions, not proof that all observed differences are learnable biology. The trained context model adds separate evidence: a gain of 0.0289 AUROC, driven mainly by local-neighbourhood composition.

### Đọc hiểu / Study notes

`Δf_i(a→b) = f(c − e_a + e_b) − f(c)`.

Điều kiện gồm **cùng peptide**, **cùng a→b**, và mô hình **chỉ dùng thành phần**. Nếu khác peptide thì c có thể khác; nếu khác b thì phép thay vector khác; nếu có đặc trưng ngữ cảnh thì mô hình không còn thuộc lớp bị ràng buộc này.

Ví dụ logic không cần số: một peptide có hai A. Hai phép A→V tạo cùng vector thành phần; mô hình phải cho điểm bằng nhau. Nếu assay gán một ô rescue và một ô không rescue, ít nhất một quyết định sẽ không khớp khi dùng cùng ngưỡng cho điểm đồng hạng đó. **89,7% không phải tỉ lệ lỗi của PAP**, cũng không phải tỉ lệ peptide mô hình hoàn toàn vô dụng.

**EN:** The proof concerns an equivalence class of inputs. It establishes a representational restriction against observed labels; noise analysis and held-out learning are needed to assess its practical importance.

**Hỏi sâu / Q&A:** “Tăng dữ liệu có gỡ được giới hạn không?” — “Không nếu vẫn giữ đầu vào chỉ có thành phần. Cần thông tin làm hai ngữ cảnh phân biệt được, rồi kiểm xem có học được lợi ích trên dữ liệu chưa thấy không.” / “Will more data remove the restriction?” — “Not within the same representation class; distinguishable inputs and held-out evidence are required.”

**Chuyển / Transition:** “Giới hạn này gợi ra một nhiệm vụ cụ thể và nhóm người dùng cụ thể.” / “This restriction motivates a specific task and intended users.”

**Nguồn / Sources:** [Lập luận và 2.353/2.624](../../research/composition-context-audit.md) · [kết quả ngữ cảnh](../../research/residue-task-derisk-2026-10-15/README.md).

---

<a id="slide-13"></a>

## Slide 13 — Vì sao làm lúc này, ai cần? / Why now, and who needs it?

**Thông điệp / Message:** Nhãn đột biến và baseline hiện có cho phép hỏi một câu có thể kiểm chứng. / Available mutation labels and baselines make the task testable.

### VI — Lời thuyết trình

Điểm thuận lợi hiện nay là đã có nhãn đột biến quy mô lớn của Zhang và bản đồ cùng baseline PAP để xây phép đối chứng. Trong hồ sơ khảo sát của repo, tiền lệ gần nhất đã có đầu ra ma trận nhưng chưa cung cấp đầy đủ điều kiện đánh giá mà đề tài muốn thực hiện: tách cụm, báo mức lặp lại của nhãn và bất định dự đoán.

Em không dựa vào câu “chưa ai làm” để nhận tính mới. Phần cần kiểm là một mô hình học hiệu ứng residue có tạo lợi ích dương dưới giao thức đủ rõ hay không.

Ba nhóm người dùng là người nghiên cứu biến thể cần giả thuyết chức năng; nhà sinh học muốn ưu tiên vị trí để thử; và người nghiên cứu học máy cần benchmark tái lập. Con số 530.412 VUS mô tả một miền có nhu cầu nghiên cứu, không chứng minh công cụ sẽ giải thích được tất cả các biến thể đó.

### EN — Speaker script

The task is now testable using Zhang's mutation-effect labels and the PAP map and baseline. The closest precedent already provides a matrix output, while the repository's survey identifies evaluation questions concerning cluster separation, label reproducibility and prediction uncertainty.

I do not base novelty on saying that nobody has done this. The question is whether a model trained for residue-level effects delivers a positive benefit under an explicit evaluation protocol.

The intended users are variant researchers seeking functional hypotheses, experimental biologists prioritising mutations, and ML researchers needing a reproducible benchmark. The 530,412 VUS describe a relevant research domain; they do not establish that the proposed service can explain every variant.

### Đọc hiểu / Study notes

**Người dùng → hành động → đầu ra:** nhà sinh học nhập peptide, xem điểm và bất định, rồi chọn biến thể để đo tiếp. “Ưu tiên thử” khác “kết luận đúng”. Người nghiên cứu benchmark cần biết split, nhãn, đối chứng và cách tái chạy, không chỉ ảnh heatmap.

Câu tìm kiếm ngày 15/10/2026 trên slide là **hồ sơ khảo sát đã ghi trong nguồn**, không phải một cuộc tìm kiếm mới của lần biên soạn này. Không tìm thấy trong phạm vi khảo sát không chứng minh không tồn tại; tránh dùng “đầu tiên”, “duy nhất” hoặc “không ai có” làm trụ.

**EN:** The user need is hypothesis prioritisation and reproducible comparison. The documented literature search is time-bounded evidence of coverage, not proof of universal novelty or a current service audit.

**Hỏi sâu / Q&A:** “530.412 VUS có phải 530.412 nhãn huấn luyện?” — “Không. Nhãn huấn luyện là ΔPSI thực nghiệm; VUS là chú giải trong miền ứng dụng, không phải đáp án của mô hình.” / “Are those VUS training labels?” — “No. Experimental ΔPSI is the learning target; VUS counts describe the application domain.”

**Chuyển / Transition:** “Từ đó em tách đóng góp thành ba trụ, với trạng thái riêng.” / “This leads to three contribution pillars with separate evidence states.”

**Nguồn / Sources:** [Báo cáo độ phủ](../../research/variant-coverage-2026-10-15/README.md) · [tiền lệ và giới hạn](../../research/larsen-nuclear-and-risks-2026-10-15/README.md).

---

<a id="slide-14"></a>

## Slide 14 — Ba trụ đóng góp / Three contribution pillars

**Thông điệp / Message:** Phân biệt bằng chứng hiện có với đóng góp kiến trúc và phần mềm còn phải tạo. / Distinguish measured evidence from contributions still to be delivered.

### VI — Lời thuyết trình

Khung gồm ba trụ: động lực có số đo ở mức vùng; phương pháp dự đoán hiệu ứng residue; và phần mềm có bất định cùng khả năng tái lập. Trong phần phương pháp, em đã có audit giới hạn biểu diễn, giao thức đánh giá hiện tại và kết quả dương của các mô hình ridge. Kiến trúc khép khoảng cách trên ma trận và dịch vụ phần mềm vẫn chưa hoàn thành.

Phân rã giúp nói đúng bản chất kết quả: thêm thành phần của lân cận ±3 tăng 0,0232 AUROC; thêm thứ tự trong lân cận tăng tiếp 0,0057. Hai phần đó tạo mức tăng 0,0289. Sau khi đã có ngữ cảnh, thêm chỉ số vị trí tuyệt đối chỉ tăng khoảng 0,0002.

Vì vậy, kết luận là thành phần ở thang lân cận hữu ích hơn chỉ thành phần cả peptide. So với ΔPAP cnn2w7, delta ghép cặp trên bộ quét là +0,0300. Em đồng thời nói rõ đây là mô hình được dùng ngoài mục tiêu huấn luyện gốc, và kết quả đó chưa đóng G2 trên ma trận bão hòa.

### EN — Speaker script

The framework has three pillars: measured region-level motivation, residue-level methodology, and software with uncertainty and reproducibility. Existing evidence includes the representation audit, the current evaluation protocol and a positive ridge-model result. The matrix architecture and software deliverables remain unfinished.

The decomposition is important. Local-neighbourhood composition adds 0.0232 AUROC; order within that neighbourhood adds another 0.0057, giving the 0.0289 context gain. Adding absolute position after context contributes only about 0.0002.

The conclusion concerns the scale of composition, rather than a general victory of position over composition. The matched scanning gain over ΔPAP cnn2w7 is 0.0300, but ΔPAP is used outside its original training objective, and the saturation-matrix target remains unmet.

### Đọc hiểu / Study notes

| So sánh / Comparison | Đại lượng / Interpretation                                               |
| --------------------- | ---------------------------------------------------------------------------- |
| M2−M0 = +0,0232      | Thành phần cửa sổ không thứ tự / Unordered local composition          |
| M3−M2 = +0,0057      | Thêm thứ tự lân cận / Additional local order                            |
| M3−M0 = +0,0289      | Tổng lợi ích ngữ cảnh đang báo / Reported context gain                |
| M4−M3 ≈ +0,0002     | Thêm vị trí tuyệt đối sau ngữ cảnh / Absolute position after context |

Không cộng cả ba dòng thành phần rồi gọi tổng là 0,0289: dòng cuối thuộc M4, ngoài tổng M3−M0. Khoảng 80% là `0.0232 / 0.0289`, không phải 80% mọi tín hiệu sinh học trong degron. Một chênh lệch rất nhỏ cũng không tự chứng minh hai mô hình tương đương.

**EN:** C1–C5 are contribution labels on this slide, separate from C-numbered proposal anchors in the decision log. A finished audit is not a finished thesis, and proposed software is not implemented software.

**Hỏi sâu / Q&A:** “Đóng góp mới đã đủ chưa?” — “Đã có bằng chứng để tiếp tục, nhưng thành phần kiến trúc và mục tiêu ma trận còn mở. Em xin xác nhận khung, không báo hoàn thành toàn bộ đóng góp.” / “Is the contribution complete?” — “No. The architecture and matrix goal remain open; this meeting seeks approval of the framework.”

**Chuyển / Transition:** “Em định nghĩa chính xác đầu vào, đầu ra và cách chấm bài toán đó.” / “I will now define its inputs, outputs and evaluation units.”

**Nguồn / Sources:** [Phân rã M0–M4, §4](../../research/residue-task-derisk-2026-10-15/README.md) · [khung hiện hành](../../../../DECISIONS.md#d-033) · [yêu cầu kiến trúc](../../../../DECISIONS.md#d-027).

---

<a id="slide-15"></a>

## Slide 15 — Đầu vào, đầu ra, nhãn / Input, output, label

**Thông điệp / Message:** Một ô là một thay thế; đơn vị dự đoán và đơn vị suy luận thống kê khác nhau. / One cell represents one substitution; prediction units are not independent statistical units.

### VI — Lời thuyết trình

Đầu vào trực tiếp là peptide tham chiếu dài 28 residue. Đầu ra thứ nhất là ma trận 28×20 giá trị ΔPSI dự đoán. Mỗi ô mô tả thay amino acid tại một vị trí bằng loại ở cột đó. Đầu ra thứ hai là bản đồ theo vị trí, thu được khi gộp các thay thế hợp lệ tại mỗi residue.

Nhãn được suy từ hai phép đo độ bền mutant và tham chiếu. Giá trị ΔPSI dương biểu thị làm bền; benchmark gọi rescue khi giá trị ít nhất +1,0. Thước đo chính là AUROC mức ô, tính trong từng peptide rồi lấy trung bình macro. Các chỉ số mức vị trí là bổ sung và phải được báo riêng.

Đầu ra có hàng chục nghìn ô nhưng chúng không phải hàng chục nghìn mẫu độc lập. Các ô thuộc cùng peptide và các peptide thuộc protein liên quan có phụ thuộc. Vì vậy, tách train/test và bootstrap dựa trên cụm protein. Phạm vi dự đoán vẫn là peptide–reporter; cấu trúc protein nguyên vẹn chỉ là thông tin bổ sung cần kiểm riêng.

### EN — Speaker script

The direct input is a reference 28-residue peptide. The first output is a 28-by-20 matrix of predicted ΔPSI values, one for each position and replacement amino acid. The second is a position-level map obtained by aggregating valid substitutions.

Labels come from mutant and reference stability measurements. The rescue benchmark uses ΔPSI of at least plus one. Its primary metric is cell-level AUROC computed within each peptide and then macro-averaged. Position-level metrics are reported separately.

The many cells are not independent samples. Cells are nested within peptides, and related proteins can share information. We therefore split and bootstrap by protein cluster. Predictions describe the peptide–reporter system; intact-protein structural context requires separate validation.

### Đọc hiểu / Study notes

- **28×20 = 560 ô hiển thị; 28×19 = 532 thay thế khác WT.** Ô giữ nguyên amino acid là mốc tham chiếu, không được đếm như một mutant mới. Ô thiếu phép đo phải có mask, không điền 0 rồi coi là “không hiệu ứng”.
- **AUROC:** khả năng xếp ô rescue cao hơn ô không rescue; 0,5 là xếp hạng ngẫu nhiên, 1 là phân biệt hoàn hảo theo nhãn đang dùng. Nó không phải phần trăm dự đoán đúng tại một ngưỡng.
- **Macro theo peptide:** peptide đủ điều kiện có trọng số ngang nhau. Peptide chỉ có một lớp không xác định AUROC và cần được loại/ghi rõ theo bộ chấm; đây là lý do số peptide có dữ liệu khác số peptide tham gia một phép so.
- **EN:** The position aggregation rule must be specified. A mean over substitutions, a maximum and a rescue fraction answer different questions. The real example uses means over measured valid substitutions.

**Hỏi sâu / Q&A:** “Tại sao không bootstrap từng ô cho CI hẹp hơn?” — “Vì như vậy giả sử sai rằng các ô độc lập. CI cần phản ánh phụ thuộc theo peptide/cụm, không chỉ số lượng dòng.” / “Why not bootstrap cells?” — “That would ignore dependence and can understate uncertainty.”

**Chuyển / Transition:** “Sau đây là một ma trận thật để cụ thể hóa từng ô và từng hàng.” / “A real measured matrix makes each cell and row concrete.”

**Nguồn / Sources:** [Bộ chấm AUROC và M3](../../research/residue-task-derisk-2026-10-15/derisk.py) · [quy tắc nhãn](../../research/residue-task-derisk-2026-10-15/residue_data.py).

---

<a id="slide-16"></a>

## Slide 16 — Đọc một ví dụ thật / Worked example: HIF1A tile 25

**Thông điệp / Message:** Đây là nhãn được tính lại từ thực nghiệm, không phải bản đồ dự đoán. / This is a measured-label map, not a model prediction.

### VI — Lời thuyết trình

Ví dụ là peptide Q16665_HIF1A_25, tương ứng residue 553 đến 580 của HIF1A. PSI tham chiếu nội tại khoảng 2,19, nằm trong ngưỡng degron. Hình có 529 ô thay thế được đo, trong tối đa 532 ô khác WT.

Em đọc một ô trước: vị trí 12 của peptide là P; thay P thành D cho ΔPSI khoảng +2,58. Reporter chứa mutant bền hơn đáng kể trên thang PSI. Ở toàn hàng 12, cả 19 thay thế đều đạt ngưỡng rescue. Ngược lại, vị trí 23 là R có hiệu ứng trung bình khoảng −0,31 và không ô nào đạt rescue.

Vùng 10–14 là một vùng đáp ứng nổi bật, không phải toàn bộ các vị trí có hiệu ứng trên ma trận. Đối chiếu tài liệu, P tại vị trí 12 ứng với P564 của HIF1A, một vị trí đã biết liên quan nhận diện bởi phức E3 có VHL. Đây là đối chiếu kiến thức cũ, không phải phát hiện cơ chế mới. Slide chỉ minh họa nhãn đo, không chứng minh mô hình dự đoán đúng.

### EN — Speaker script

The example is HIF1A tile 25, spanning protein residues 553 to 580. Its internal reference PSI is about 2.19, within the degron range. The map contains 529 measured non-WT substitutions out of a possible 532.

At peptide position 12, replacing proline with aspartate gives ΔPSI of approximately plus 2.58. All 19 substitutions at that position meet the rescue threshold. Position 23, arginine, provides a contrast: its mean effect is about minus 0.31, with no rescue-positive cells.

Positions 10–14 form one prominent responsive region, but not the only positions with effects. The reference P12 corresponds to HIF1A P564, a known site linked to VHL-containing E3 recognition. That is a literature cross-check, not a new mechanistic discovery or evidence of model performance.

### Đọc hiểu / Study notes

1. **Đổi tọa độ:** tile bắt đầu tại 553 nên vị trí peptide 12 là `553 + 12 − 1 = 564`. Không dùng số 12 như tọa độ toàn protein.
2. **Đọc màu cùng legend:** màu biểu diễn ΔPSI, không phải xác suất E3 nhận diện hoặc độ tin cậy. Ô trống không đồng nghĩa hiệu ứng bằng 0.
3. **Đọc hàng:** trung bình hàng P12 trong JSON là **1,9638**; **2,5810 là riêng ô P12D**. Các trung bình cao còn có vị trí 7, 19 và 22. Không mô tả “footprint chỉ có 10–14”.
4. **Đối chiếu motif:** vị trí 7–12 là `LEMLAP`, khớp dạng `LXXLAP`; P564 liên quan hydroxyl hóa. Assay phát hiện hiệu ứng trong điều kiện tế bào đang có, không chứng minh hoạt tính độc lập mọi điều kiện.
5. **Chọn ví dụ:** quy tắc chọn ưu tiên nhiều ô rescue, nên đây là ví dụ dễ đọc, không đại diện cho hiệu năng trung bình. Nó nằm phía đánh giá của phép chuyển nguồn hiện có; không dùng để tinh chỉnh mô hình rồi tiếp tục gọi là test chưa đụng tới.

**EN:** Cell, row and protein coordinates are distinct. The figure is selected for illustration from measured labels; it is not an unbiased performance example or a direct binding assay.

**Hỏi sâu / Q&A:** “Em có tự phát hiện degron HIF1A không?” — “Không. Em tính lại dữ liệu Zhang, chọn ví dụ bằng quy tắc cố định và đối chiếu vị trí đã biết.” / “Did you discover this HIF1A degron?” — “No. I reconstructed existing measurements and cross-checked a known site.”

**Chuyển / Transition:** “Một ví dụ dễ đọc chưa đủ; cần nhìn kết quả trên toàn tập.” / “A clear example is not enough; we need the dataset-level benchmark.”

**Nguồn / Sources:** [JSON từng ô](../../research/slide-figures-2026-10-15/example-matrix.json) · [quy tắc chọn và xuất xứ](../../research/slide-figures-2026-10-15/README.md) · [hình đo](figures/example-matrix.svg).

---

<a id="slide-17"></a>

## Slide 17 — Kết quả hai phía / What the data permits

**Thông điệp / Message:** Thắng ở bộ quét, còn thua ở ma trận bão hòa; G2 chưa hoàn tất. / Positive scanning evidence coexists with an unmet saturation target.

### VI — Lời thuyết trình

Trên bộ quét, mô hình ngữ cảnh M3 đạt AUROC macro khoảng 0,8682; M0 chỉ thành phần đạt 0,8393. Delta ghép cặp là +0,0289, CI 95% từ 0,0264 đến 0,0313. Khi so với ΔPAP cnn2w7 trên đúng tập peptide chung, M3 đạt 0,8657 so với 0,8357, chênh +0,0300.

Nhưng trên bộ bão hòa, mô hình học từ bộ quét chỉ đạt 0,7273, thấp hơn ΔPAP cnn2w1 là 0,7693. Chênh −0,0420 có CI từ −0,0580 đến −0,0256. Kết quả này xác định phần việc còn lại, thay vì được che bởi kết quả thắng ở nguồn khác.

Hai mốc lặp lại nhãn là 0,9458 và 0,9519; chúng là mốc trần đo lường ước lượng, không phải hiệu năng chắc chắn học được. MDE 0,0123 được tính cho cặp M3−M0 trên bộ bão hòa; phép so kiến trúc mới cần đánh giá lại phương sai. Với Spearman mức vị trí, em chưa dùng phép so trên slide vì số PAP đang bị ghi nhầm cấp độ.

### EN — Speaker script

On scanning, M3 reaches macro AUROC 0.8682 versus 0.8393 for M0, with a paired gain of 0.0289 and a 95% interval of 0.0264 to 0.0313. On the matched subset used for ΔPAP comparison, the values are 0.8657 and 0.8357, giving a gain of 0.0300.

On saturation, however, M3 reaches 0.7273 versus 0.7693 for ΔPAP cnn2w1. The difference is minus 0.0420, with an interval entirely below zero. This is the remaining target.

Replicate-based measurement references are 0.9458 and 0.9519, not promises of achievable performance. The 0.0123 MDE belongs to the M3-minus-M0 comparison and must not be generalised to every new ablation. I also withhold the slide's position-level correlation comparison because the PAP value is mislabelled.

### Đọc hiểu / Study notes

| Phép so / Comparison    | Tập ghép cặp / Matched population | Delta và CI 95%              |
| ------------------------ | ------------------------------------ | ----------------------------- |
| M3−M0, scanning         | 2.288 peptide / 1.599 cụm           | +0,0289 [0,0264; 0,0313]      |
| M3−ΔPAP w7, scanning   | 2.064 peptide / 1.471 cụm           | +0,0300 [0,0234; 0,0366]      |
| M3−ΔPAP w1, saturation | 91 peptide / 89 cụm                 | −0,0420 [−0,0580; −0,0256] |

**Vì sao tập khác nhau?** Một phép so chỉ dùng những peptide cả hai cách chấm được. Trừ hai trung bình khác tập không tạo thành phép so ghép cặp. Cũng không nhầm 2.994 peptide có nhãn bộ quét với 2.288 peptide có AUROC hợp lệ trong phép so M3−M0.

**Lỗi Spearman:** [PAP JSON](../../research/pap-baseline/pap-baseline.json) đặt **0,3553** dưới `cell_level`, còn `position_level` là **0,4130**. [M3 JSON](../../research/residue-task-derisk-2026-10-15/model.json) ghi mức vị trí **0,4440**. Hai số sau gợi ý cần đối chiếu cùng cách gộp và cùng đơn vị; không có CI delta mức vị trí ở đây để tuyên bố thắng hoặc tương đương.

**EN:** Confidence intervals quantify uncertainty under the resampling design. A narrow CI does not remove systematic bias. A difference smaller than a past MDE is not automatically zero or non-significant; inspect the interval and power of the actual comparison.

**Hỏi sâu / Q&A:** “Tại sao có +0,0300 mà G2 chưa đạt?” — “Vì nó là kết quả bộ quét. Mục tiêu ma trận vẫn thua baseline, nghĩa vụ đối chứng Degformer và kiến trúc mới còn mở.” / “Why is G2 still incomplete?” — “The positive result is on scanning; the matrix target and required comparisons remain unresolved.”

**Chuyển / Transition:** “Để hiểu độ tin cậy của các số này, em trình bày nguồn và cách dựng dữ liệu.” / “Next, I will show the data provenance and reconstruction.”

**Nguồn / Sources:** [Delta ghép cặp](../../research/residue-task-derisk-2026-10-15/headline.json) · [M0–M4](../../research/residue-task-derisk-2026-10-15/model.json) · [lực từng phép so](../../research/residue-task-derisk-2026-10-15/power.json) · [trạng thái G2](../../../../DECISIONS.md#d-031).

---

<a id="slide-18"></a>

## Slide 18 — Nguồn dữ liệu và vai trò / Data sources and provenance

**Thông điệp / Message:** Tải được dữ liệu, kiểm tính toàn vẹn và xác nhận phạm vi sử dụng là các việc khác nhau. / Availability, integrity and usage conditions require separate evidence.

### VI — Lời thuyết trình

Dữ liệu hiện có khoảng 2,3 GB, với nguồn gốc và checksum được ghi lại. Hai bộ đột biến Zhang là nhãn hiệu ứng chính. Bảng GPS peptidome cung cấp bối cảnh mức peptide và miền ứng dụng. Repo Voutsinos cung cấp PAP cùng dữ liệu tile cho các phép đối chứng.

MaveDB được dùng cho câu hỏi chuyển giao sang protein nguyên vẹn; bộ Larsen dành cho chuyển assay hoặc ngăn tế bào ở mức tile. UniProt giúp xác định trình tự tham chiếu và tọa độ; AlphaFold cung cấp cấu trúc dự đoán khi phù hợp. ClinVar chỉ cung cấp động lực mức vùng, không phải nhãn đánh giá ΔPSI.

Em phân biệt giấy phép bài báo với điều kiện dữ liệu và mã nguồn. Với Larsen, repo có MIT nhưng email xác nhận phạm vi áp dụng cho file dữ liệu vẫn đang chờ. Vì vậy, tiêu đề “đã kiểm giấy phép” trên slide không được hiểu là mọi điểm mơ hồ đã được đóng. Mọi số mô tả dữ liệu cần gắn với đúng bản tải và bước lọc.

### EN — Speaker script

Approximately 2.3 GB of material is available, with recorded provenance and checksums. Zhang's two mutagenesis datasets supply the main effect labels. The GPS peptidome defines segment-level context and the application domain. The Voutsinos repository supplies PAP and tile data.

MaveDB supports an intact-protein transfer question, while Larsen supports tile-level assay or compartment transfer. UniProt provides reference sequences and coordinates; AlphaFold supplies predicted structures where appropriate. ClinVar is motivation only, not a ΔPSI validation target.

Paper, code and data permissions are tracked separately. The Larsen repository has an MIT notice, but clarification of its coverage of the data file is still pending. The slide's heading therefore should not imply that every licensing question is settled.

### Đọc hiểu / Study notes

- **Accession / DOI / URN:** định danh nguồn; **version / commit / release:** ghim một trạng thái; **SHA-256:** kiểm đúng chuỗi byte đã tải. Hash giống nhau chứng minh file giống nhau, không chứng minh nhãn sinh học đúng.
- File ClinVar dạng mới nhất thay đổi theo thời gian. Muốn tái lập số đo phải giữ đúng bản hoặc archive tương ứng; không tải “latest” rồi mặc nhiên coi là đầu vào cũ.
- MaveDB không phải mọi bộ đều đo cùng readout; Larsen không cung cấp nhãn đột biến từng residue. Không gộp các nguồn chỉ vì đều có chữ “stability” hoặc đều là protein.
- **EN:** A reproducible dataset needs identity, version, integrity and processing history. A licence label is source-specific; the pending clarification remains a source limitation, not an inferred approval.

**Hỏi sâu / Q&A:** “Có thể trộn mọi nhãn để tăng dữ liệu không?” — “Chưa. Cần xét endpoint, chiều điểm, bối cảnh assay và chồng lặp. Nguồn khác nhau đang có vai khác nhau.” / “Can all labels be pooled?” — “Not without validating endpoint compatibility, direction, context and overlap.”

**Chuyển / Transition:** “Sau khi giữ nguyên bản thô, em dựng lại nhãn bằng một pipeline có cổng kiểm.” / “From the preserved raw data, I reconstruct labels through a validated pipeline.”

**Nguồn / Sources:** [Sổ dữ liệu](../../data/README.md) · [nguồn Larsen](../../data/raw/larsen-2025/SOURCE.md) · [nguồn ClinVar](../../data/raw/clinvar/SOURCE.md) · [C-11a](../../../../DECISIONS.md#c-11a).

---

<a id="slide-19"></a>

## Slide 19 — Dựng nhãn từ read thô / From raw reads to validated labels

**Thông điệp / Message:** Tái lập phép tính PSI cho phép kiểm pipeline và khai thác replicate. / Reconstructing PSI checks the computation and enables replicate analysis.

### VI — Lời thuyết trình

Pipeline có ba tầng. Raw giữ dữ liệu gốc; interim chứa phần giải nén và các bước trung gian; processed là bảng được script tạo ra. Với mỗi construct, em đọc số đếm ở sáu bin, chuẩn hóa theo hệ số riêng của điều kiện, rồi tính trung bình chỉ số bin có trọng số để ra PSI.

Cổng kiểm là so PSI Replicate 1 tính lại với bảng tác giả. Trên 261.865 giá trị đối chiếu, sai lệch lớn nhất là 5 nhân 10 mũ trừ 7, phù hợp độ làm tròn. Audit cũng truy được ba construct bị ảnh hưởng bởi lỗi đọc header trong pipeline công bố, và bảng xuất ra đã xử lý đúng số đọc gốc.

Cùng quy trình dựng được năm điều kiện, giúp tính mức lặp lại giữa hai replicate. Tuy nhiên, BAG6 WT vẫn là điều kiện riêng. Phễu trên hình cho thấy số lượng thay đổi theo lọc; số 91 là số peptide bão hòa đạt điều kiện degron, không phải toàn bộ cỡ mẫu của nhiệm vụ residue.

### EN — Speaker script

The pipeline separates raw, interim and processed data. For each construct, it reads counts from six bins, normalises them using condition-specific factors, and computes a weighted average of bin indices to obtain PSI.

The validation gate compares reconstructed Replicate-1 values with the authors' table. Across 261,865 comparable values, the maximum deviation is five times ten to the minus seven, consistent with rounding. The audit also traced three affected constructs to a header-reading error; the exported tables use the raw counts correctly.

The reconstruction produces five conditions and enables replicate analysis. BAG6 WT remains a separate condition. The funnel describes successive filters; 91 is the filtered saturation size, not the total residue-task sample size.

### Đọc hiểu / Study notes

`nb_i = b_i × factor_i`; `PSI = Σ(i × nb_i) / Σ(nb_i)`.

Trong đó `b_i` là số read ở bin i, `nb_i` là read đã chuẩn hóa. Với sáu bin đánh số 1–6 và trọng số không âm, PSI nằm trong [1,6] khi tổng trọng số dương. Không có read thì không có PSI có nghĩa; không gán 0 vào thang 1–6.

Mốc lệch cực nhỏ chứng minh **tái lập phép tính trên tập đối chiếu**, không chứng minh assay không nhiễu hay từng điều kiện còn lại được xác nhận độc lập bằng một bảng công bố. Đặc biệt, kiểm bản công bố và sửa lỗi header là hai bước: audit có mô phỏng lỗi để truy nguyên, còn dữ liệu xuất dùng cách đọc đã sửa.

Phễu **8.831 → 3.439 → 2.624** thuộc audit bộ quét ở phạm vi lọc ban đầu; số **2.994** là bộ quét hai-replicate sau xử lý hiện hành. Hai con số không thay nhau và không cần bằng nhau.

**EN:** Computational agreement and biological reproducibility are separate validation layers. Raw construct counts, retained peptides and evaluable peptides must not be treated as one population.

**Hỏi sâu / Q&A:** “Sai lệch 5×10⁻⁷ có nghĩa nhãn gần như hoàn hảo?” — “Không. Phép tính khớp bảng; nhiễu thực nghiệm vẫn phải đo giữa replicate.” / “Does the tiny reconstruction error imply perfect labels?” — “No. It validates the calculation, not experimental precision.”

**Chuyển / Transition:** “Sau pipeline, hai thiết kế đột biến cho hai loại thông tin bổ sung nhau.” / “The two mutagenesis designs then provide complementary information.”

**Nguồn / Sources:** [Audit pipeline, §2](../../research/full-data-audit/README.md) · [kết quả kiểm PSI](../../research/full-data-audit/psi-build.json) · [từ điển các điều kiện](../../data/README.md).

---

<a id="slide-20"></a>

## Slide 20 — Hai tập nhãn và split / Dataset fields, samples and split

**Thông điệp / Message:** Bộ quét rộng theo ngữ cảnh; bộ bão hòa rộng theo loại thay thế. / Scanning provides contextual breadth; saturation provides substitution breadth.

### VI — Lời thuyết trình

Bộ quét đo một thay thế tại mỗi vị trí theo thiết kế opposite-scanning. Sau lọc hiện hành, có 2.994 peptide, 1.985 cụm và 83.446 ô. Bộ này giúp học hiệu ứng trong nhiều ngữ cảnh khác nhau, nhưng không đo đủ 19 thay thế cho mỗi vị trí.

Bộ bão hòa đo nhiều loại thay thế tại mỗi residue. Tập degron hiện dùng có 91 peptide, 89 cụm và 47.847 ô. Nhãn WT của bộ quét là construct tham chiếu riêng; với bão hòa, WT nội tại được suy từ các ô đồng nghĩa giữ nguyên amino acid.

Đối với phép chuyển từ quét sang bão hòa đã chạy, 61 trong 89 cụm bão hòa cũng có ở bộ quét. Các peptide quét thuộc cụm đó được loại khỏi train. Đây là quy tắc chống chồng lặp theo cụm, mạnh hơn chỉ loại các peptide trùng tên. Nhãn lấy trung bình hai replicate phù hợp; không trộn BAG6 WT và không coi ký tự stop cuối chuỗi là amino acid thứ 21.

### EN — Speaker script

Scanning measures one designed substitution per position. After the current filters it contains 2,994 peptides, 1,985 clusters and 83,446 cells. It provides many sequence contexts, but not all 19 replacements at each position.

Saturation provides broader substitution coverage: 91 degron peptides, 89 clusters and 47,847 cells. Scanning uses a separate reference construct; saturation derives an internal reference from synonymous constructs that preserve the amino acid sequence.

For the completed cross-source test, 61 of the 89 saturation clusters overlap scanning. Scanning peptides in those clusters are excluded from training. Labels average the appropriate two replicates. BAG6 WT is not pooled, and terminal stop symbols are masked rather than treated as a twenty-first amino acid.

### Đọc hiểu / Study notes

| Khái niệm / Concept | Cách hiểu / Meaning                                                                                                                                                            |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scanning              | Một thay thế thiết kế/vị trí; quy tắc phụ thuộc WT, không phải mọi vị trí đều →R. / One designed substitution per position, not universal arginine replacement. |
| Saturation            | Các amino acid thay thế tại mỗi vị trí; có thể thiếu ô sau lọc. / Broad substitution coverage, with missing cells after filtering.                                    |
| Cov80                 | Cụm protein xây bằng MMseqs2, identity ≥30% và coverage 80% theo cấu hình repo; không có nghĩa “80% identity”. / Coverage and identity are distinct parameters.      |
| Split cụm            | Cả cụm nằm một phía trong phép so; loại chồng lặp cụm khi chuyển nguồn. / Keep cluster membership consistent across sources.                                         |
| WT nội tại          | Trung vị PSI các construct giữ nguyên amino acid trong từng nửa, rồi tạo ΔPSI phù hợp. / Internal reference from amino-acid-preserving constructs.                    |

Ví dụ định danh `..._mut10a` là thay vị trí peptide 10 thành alanine; không mặc nhiên nói amino acid gốc là A. Tọa độ tile thường bắt đầu `(n−1)×23+1`, nhưng vẫn cần đối chiếu chuỗi: isoform hay lệch tham chiếu có thể làm công thức không khớp.

**EN:** The 130 shared-peptide count belongs to a broader comparison. For the filtered saturation experiment, use 42 shared peptide identifiers and 61 shared clusters. If future work trains on saturation, it needs an explicit cluster-separated train/validation/test design; today's all-saturation transfer evaluation is not automatically that future test.

**Hỏi sâu / Q&A:** “G1 độc lập nghĩa là hai nhóm tác giả độc lập?” — “Không. Nó nghĩa nhãn thực nghiệm không do mô hình của đề tài sinh ra. Cả hai nguồn residue đều của Zhang, nên rủi ro cùng nhóm tác giả vẫn còn.” / “Does G1 imply independent laboratories?” — “No. The labels are independent of our model, but both residue datasets come from the same study group.”

**Chuyển / Transition:** “Với hai nguồn bổ sung nhau, câu hỏi kiến trúc là học thông tin mức residue từ nhãn ở những thang nào.” / “This leads to the question of learning residue information from different supervision scales.”

**Nguồn / Sources:** [Hai vai nhãn và chồng lặp](../../research/residue-task-derisk-2026-10-15/README.md) · [từ điển định danh](../../data/README.md) · [D-025](../../../../DECISIONS.md#d-025).

---

<a id="slide-21"></a>

## Slide 21 — Các phương án kiến trúc / Proposed approach

**Thông điệp / Message:** MIL là một giả thuyết giám sát yếu cần đối chứng, chưa là kiến trúc được xác nhận. / MIL is a weak-supervision hypothesis to test, not a validated architecture.

### VI — Lời thuyết trình

Phần đã xác định là đầu vào, nhãn, metric và split; phần còn mở là kiến trúc. Phương án A dùng đầu theo vị trí học trực tiếp từ nhãn mức ô. Phương án B xem peptide như một túi các cửa sổ cục bộ, dùng attention-MIL để khai thác nhãn toàn peptide hoặc tile. Phương án C kết hợp loss mức túi và mức ô.

Động lực là nhãn toàn đoạn dồi dào hơn nhãn ma trận đầy đủ. Câu hỏi không phải attention hay MIL có mới không; các cơ chế đó đã có tiền lệ. Câu hỏi là nhãn mức túi có giúp dự đoán đúng hiệu ứng residue trong nhiệm vụ này, và có tốt hơn đầu được giám sát trực tiếp hay không.

Cả A, B và C đều chưa chạy. Cần đối chứng cùng split, dữ liệu được phép dùng, biểu diễn và ngân sách phù hợp. Mô hình dự đoán tốt ở mức túi vẫn có thể định vị sai. Nếu nhánh MIL không giúp, kết quả âm đó có giá trị phân tích, nhưng không tự thay yêu cầu đóng góp dương và thành phần kiến trúc của đề tài.

### EN — Speaker script

The task, labels, metrics and split are defined; the architecture remains open. Variant A predicts each position using cell-level supervision. Variant B treats a peptide as a bag of local windows and uses attention-MIL to exploit segment-level labels. Variant C combines bag and cell losses.

The motivation is that segment-level labels are more abundant than full mutation matrices. Attention and MIL are established methods. The question is whether their bridge transfers useful information to residue-level effects and improves on direct supervision.

None of A, B or C has been run. Comparisons need controlled splits, representations, permitted data and budgets. Good bag prediction does not establish good localisation. A negative MIL result would inform the analysis, but would not by itself satisfy the positive-contribution requirement.

### Đọc hiểu / Study notes

- **Bag / túi:** một peptide có một nhãn chung; **instance:** cửa sổ quanh một residue. Nhãn “peptide không bền” không chỉ ra cửa sổ nào là nguyên nhân.
- **Attention:** cách tính trọng số khi gộp các instance. Trọng số lớn không mặc nhiên bằng ΔPSI lớn, xác suất đúng hay bằng chứng E3 tiếp xúc trực tiếp.
- **Hybrid loss:** dạng giải thích `L = L_cell + λL_bag`; λ điều chỉnh mức đóng góp của hai nguồn giám sát. Đây là ý tưởng trong phương án, không phải cấu hình đã chọn.
- **28,9% → 53,3%** là tỉ lệ hệ số vượt tiêu chí ổn định trong các phân tích cụ thể, không phải định lý “nhãn túi hoàn toàn không có thông tin vị trí” hay phần trăm residue đã giải thích được.
- **EN:** Weak supervision concerns missing fine-grained labels, not a proven immunity to noisy labels. Pretraining must respect the declared evaluation boundary. Intact-protein accessibility features belong to the transfer question and do not create new variation in the isolated-peptide assay.

**Hỏi sâu / Q&A:** “Vì sao cần MIL nếu đã có nhãn residue?” — “Để kiểm xem có khai thác được nguồn nhãn toàn đoạn lớn hơn không; A là đối chứng để phát hiện trường hợp MIL không có ích.” / “Why MIL with residue labels available?” — “To test whether additional coarse labels help; direct supervision remains the essential control.”

**Chuyển / Transition:** “Mỗi ý tưởng sẽ được gắn với một phép so có thể bác bỏ nó.” / “Each architectural idea needs a comparison that can falsify its benefit.”

**Nguồn / Sources:** [Lý lẽ giám sát yếu, §5.1](../../research/residue-task-derisk-2026-10-15/README.md) · [phạm vi đã ghi](../../../../DECISIONS.md#d-035) · [các tiền đề kiến trúc](../../research/architecture-check/README.md).

---

<a id="slide-22"></a>

## Slide 22 — Kế hoạch đánh giá / Evaluation plan

**Thông điệp / Message:** Mỗi tuyên bố đi với đối chứng, metric và độ bất định. / Each claim needs a controlled comparison, a metric and uncertainty.

### VI — Lời thuyết trình

Em tổ chức đánh giá theo câu hỏi. Bốn dòng đầu đã có bằng chứng: lợi ích ngữ cảnh so với thành phần, phép so ΔPAP ở hai nguồn, phân rã thang thông tin và độ ổn định trọng số. Những dòng về MIL, one-hot so với PLM, Degformer và phân tích lỗi còn là kế hoạch.

Để tách lợi ích của biểu diễn khỏi kiến trúc, em cần lưới đối chứng thay một thành phần mỗi lần hoặc so các tổ hợp dưới điều kiện tương đương. Các mô hình được so ghép cặp trên cùng peptide; bootstrap lấy lại mẫu theo cụm protein. Chọn cấu hình trên train/validation trước khi dùng test cuối.

Mỗi bảng sẽ báo metric riêng, delta, CI và mức lặp lại nhãn phù hợp. MDE cần tính theo phép so thật; không tự loại mọi delta nhỏ hơn 0,0123. Hiện chưa có kết quả đủ để kết luận kiến trúc, PLM hay MIL nào tốt hơn. Các ô trống ở lưới trên slide thực sự là chưa đo.

### EN — Speaker script

The evaluation is organised by question. Existing evidence covers the context gain, ΔPAP comparisons on both sources, scale decomposition and weight stability. MIL, one-hot versus PLM, Degformer and error analysis remain planned work.

A representation-by-model grid will separate representation benefits from architectural effects under comparable conditions. Models are paired on the same peptides, with bootstrap resampling by protein cluster. Configuration selection belongs on training and validation data before final testing.

Reports should show separate metrics, paired differences, confidence intervals and the relevant label-reproducibility reference. MDE must match the actual comparison. Empty cells remain unmeasured; we cannot yet conclude that PLM, MIL or another architecture wins.

### Đọc hiểu / Study notes

**Ablation** là bỏ/thay một thành phần để hỏi nó có ích không. Nếu đổi cả biểu diễn, dữ liệu và kiến trúc cùng lúc, delta không quy riêng được cho một thành phần. Ngân sách học tương đương không nhất thiết là cùng số epoch nếu kích thước mô hình quá khác; điều kiện thực tế phải được công bố.

**CI của delta:** lấy hiệu trong cùng peptide rồi bootstrap theo cụm; không trừ hai CI của từng mô hình. **Không phát hiện khác biệt** không đồng nghĩa **đã chứng minh tương đương**. Muốn nói tương đương cần thiết kế và biên tương đương phù hợp, hiện chưa có.

**EN:** The current weight-stability percentages describe a specific estimator and resampling procedure. They are not calibrated probabilities that a biological mechanism is real. Meaningful evidence includes effect size, uncertainty, fairness and where the model fails.

**Hỏi sâu / Q&A:** “Chỉ cần p-value nhỏ là đủ?” — “Không. Cần mức cải thiện có ích, CI đúng đơn vị phụ thuộc, đối chứng công bằng và test đúng phạm vi.” / “Is a small p-value enough?” — “No. We also need a meaningful effect size, valid uncertainty and a fair evaluation.”

**Chuyển / Transition:** “Phần mềm sẽ đưa cả dự đoán và giới hạn của phép đo đến người dùng.” / “The software should expose predictions together with the limits of measurement.”

**Nguồn / Sources:** [Kết quả và lực](../../research/residue-task-derisk-2026-10-15/README.md) · [nghĩa vụ đối chứng Degformer](../../../../DECISIONS.md#d-028).

---

<a id="slide-23"></a>

## Slide 23 — Dịch vụ dự đoán / The software deliverable

**Thông điệp / Message:** Giá trị dự kiến nằm ở dự đoán có giới hạn rõ và có thể truy vết; dịch vụ chưa xây. / The proposed service makes uncertainty and provenance usable; it is not yet built.

### VI — Lời thuyết trình

Phần mềm dự kiến nhận peptide hoặc cửa sổ protein cùng đột biến người dùng chọn, trả ma trận ΔPSI, bản đồ vị trí, bất định, cờ ngữ cảnh và nguồn nhãn. Web phục vụ xem trực tiếp; API phục vụ tích hợp vào phân tích khác.

Lý do cần báo bất định xuất phát từ dữ liệu. Audit bộ quét ước lượng 75,9% phần phương sai dư sau oracle thành phần là nhiễu đo; Jaccard giữa hai tập residue footprint là 0,4965. Các số này không nói mọi dự đoán đều sai một nửa, mà cho thấy một đáp án đơn lẻ quá chắc có thể che khuất giới hạn nhãn.

Hiện đây là thiết kế. Chưa có phương pháp hiệu chỉnh bất định được chọn, chưa có độ phủ khoảng dự đoán được đo. Degformer đã có ma trận 28×20; điểm khác biệt phần mềm phải được kiểm theo từng tính năng. Em không đọc dấu gạch ở bảng thành kết luận chắc chắn công cụ khác thiếu API hay chức năng tương ứng. Dịch vụ cũng không phát ra phân loại gây bệnh.

### EN — Speaker script

The proposed service accepts a peptide or protein window and a specified mutation. It returns a ΔPSI matrix, a position map, uncertainty, context flags and label provenance. A web interface supports inspection, while an API supports integration.

The motivation for uncertainty comes from the data. The scanning audit attributes 75.9% of the residual variance after a composition oracle to measurement noise, and replicate footprint sets have a Jaccard of 0.4965. These are not per-prediction error probabilities; they show why overconfident reporting is problematic.

The service is designed, not built. No uncertainty calibration method or coverage result is established. Degformer already has the matrix output, and unverified feature-table entries must remain unknown. The service does not classify pathogenicity.

### Đọc hiểu / Study notes

**75,9% có mẫu số cụ thể:** phần dư sau oracle thành phần trong audit bộ quét, không phải 75,9% toàn bộ dữ liệu hoặc mọi lỗi mô hình. Oracle dùng nhãn để phân tích, không phải mô hình triển khai.

**Ba loại bất định cần phân biệt:** (1) dao động của phép đo thực nghiệm; (2) dao động của mô hình/ước lượng; (3) sự không chắc khi truy vấn khác phân bố. Một khoảng dự đoán có độ phủ được kiểm khác với CI của hiệu năng trung bình. Chạy nhiều seed chỉ cho một tín hiệu biến thiên; chưa đủ tự gọi là calibrated.

Mốc trần AUROC **không cùng đơn vị với ΔPSI** và không tự biến thành sai số cho mỗi ô. API cần ghi metric, nguồn và phạm vi của mốc trần, thay vì dùng `0.9519` như độ tin cậy 95,19% của từng dự đoán. Sơ đồ opacity trên slide là minh họa, chưa có ánh xạ độ tin cậy đã hiệu chỉnh.

**EN:** Calibration is a measurable goal: intervals or probabilities must be checked against appropriate held-out outcomes. A benchmark-level AUROC reference is not a per-cell probability or a ΔPSI interval. Proposed ensemble or conformal approaches remain options in the source notes, not selected methods.

**Hỏi sâu / Q&A:** “Đây có chỉ là giao diện bọc model?” — “Đóng góp dự kiến gồm truy vết nhãn, báo bất định có kiểm chứng, giới hạn miền áp dụng và giao thức tái lập. Giá trị đó vẫn phải được triển khai và đánh giá, không chỉ liệt kê tính năng.” / “Is this only a model wrapper?” — “Its intended value is validated uncertainty, provenance and reproducibility, which still need implementation and evaluation.”

**Chuyển / Transition:** “Harness là phần giúp người dùng kiểm lại các phép so đó.” / “The harness is what makes the comparisons inspectable and repeatable.”

**Nguồn / Sources:** [Phân rã nhiễu, §3](../../research/full-data-audit/README.md) · [trụ phần mềm](../../../../DECISIONS.md#d-033) · [trạng thái xác nhận](../../../../DECISIONS.md#d-034) · [nguồn tính năng công cụ](../../research/larsen-nuclear-and-risks-2026-10-15/README.md).

---

<a id="slide-24"></a>

## Slide 24 — Harness và miền áp dụng / Evaluation harness and application domain

**Thông điệp / Message:** Một báo cáo phải tái chạy được; miền ngoài cụm đã học cần được nhận diện rõ. / Reports should be reproducible, with explicit coverage of unseen clusters.

### VI — Lời thuyết trình

Harness dự kiến nạp các baseline thành phần, ΔPAP, Degformer và mô hình luận văn; chuẩn hóa cách chấm và xuất báo cáo truy được về cấu hình, seed, split và file kết quả. Mục tiêu là cùng câu hỏi đánh giá có một quy trình chạy lại được, thay vì chỉ có bảng số.

Miền ứng dụng GPS hiện có 116.702 tile đạt ngưỡng degron trên 17.287 protein. Trong 15.819 cụm của miền này, có 13.814 cụm, tức 87,3%, chưa thấy ở tập huấn luyện residue dùng để đối chiếu. Đây là tỉ lệ theo cụm; không phải nói 87,3% các tile chưa thấy. Theo tile trên protein chưa thấy, con số là 67,9%.

Vì vậy, đánh giá theo cụm và cờ ngoài phân bố là phần liên quan trực tiếp tới cách sử dụng dịch vụ. Cờ này cho biết giới hạn bằng chứng, không chứng minh mọi truy vấn mới đều sai. Harness và dịch vụ vẫn chưa được xây; ClinVar vẫn chỉ là động lực, không trở thành benchmark gây bệnh.

### EN — Speaker script

The proposed harness loads composition baselines, ΔPAP, Degformer and the thesis model, then produces comparable reports linked to configurations, seeds, splits and result files. Its goal is a repeatable evaluation process rather than a table that must be taken on trust.

The application domain contains 116,702 degron tiles on 17,287 proteins. Of its 15,819 clusters, 13,814, or 87.3%, are unseen relative to the residue-training set used in this analysis. This is a cluster proportion, not a tile proportion. The tile proportion on unseen proteins is 67.9%.

Cluster-based evaluation and distribution flags are therefore directly relevant to use. They identify evidence limits, not guaranteed prediction failure. The harness and service remain unbuilt, and ClinVar remains motivation rather than a pathogenicity benchmark.

### Đọc hiểu / Study notes

- **Harness:** chương trình điều phối nạp dữ liệu, gọi mô hình, chấm và ghi báo cáo theo giao thức; không phải một mô hình dự đoán khác.
- **OOD:** out of distribution, truy vấn khác phạm vi đã học. “Cụm chưa thấy” là cờ thao tác được đề xuất; khoảng cách phân bố không chỉ có một kiểu.
- **Checkpoint có sẵn:** chạy lại trên một danh sách test mới không xóa những gì checkpoint đã học. Cần kiểm chồng lặp dữ liệu huấn luyện gốc; nếu không có model được huấn luyện lại phù hợp, chỉ báo đúng phạm vi phép kiểm, không gọi là test sạch theo split mới.
- **Degformer pickle:** hồ sơ yêu cầu thư mục riêng và `python3 -I`. Chế độ `-I` cô lập môi trường import Python, **không phải sandbox bảo đảm an toàn cho mã pickle**. Đây là lưu ý kỹ thuật khi triển khai harness, không phải phần cần đọc nguyên trên slide.
- **EN:** Every denominator and model-training boundary must be explicit. A common report format does not by itself make pretrained models comparable or remove their training overlap.

**Hỏi sâu / Q&A:** “87,3% có chứng minh mô hình tổng quát hóa kém không?” — “Không. Nó cho biết phần lớn cụm của miền dùng chưa thấy; chất lượng trên miền đó cần được đo bằng test phù hợp.” / “Does 87.3% prove poor generalisation?” — “No. It motivates measuring performance on unseen clusters.”

**Chuyển / Transition:** “Em dùng tiến độ và điểm kiểm để quản lý phần việc còn lại.” / “The remaining work is organised around explicit progress checks.”

**Nguồn / Sources:** [Đúng mẫu số ở báo cáo độ phủ, §2](../../research/variant-coverage-2026-10-15/README.md) · [nghĩa vụ Degformer](../../../../DECISIONS.md#d-028) · [phần mềm dự kiến](../../../../DECISIONS.md#d-033).

---

<a id="slide-25"></a>

## Slide 25 — Tiến độ và phần việc tiếp theo / Remaining work

**Thông điệp / Message:** Đã có bằng chứng để tiếp tục, chưa có đủ kết quả để nhận hoàn thành đề tài. / There is evidence to proceed, with major requirements still open.

### VI — Lời thuyết trình

Theo ba kiểm tra sẵn sàng nội bộ, G1 có nhãn thực nghiệm độc lập với pipeline dự đoán; G2 có kết quả dương ban đầu nhưng chưa hoàn tất; G3 mới ở thiết kế phần mềm. Ba kiểm tra này là khung làm việc của dự án, không phải tên các cổng chính thức của học phần.

Thứ tự trước mắt là huấn luyện và so sánh các phương án cho ma trận, làm ablation, kiểm seed và đối chứng Degformer. Phần chuyển assay hoặc ngăn tế bào cần được giữ đúng vai trò đánh giá riêng. Điểm kiểm cuối tuần 10 đã được ghi trong sổ quyết định. Sau đó là ứng dụng và viết; lịch chi tiết tuần 7, 8 và 9 trên slide là cách phân bổ dự kiến.

Nếu chưa vượt mục tiêu ma trận, em cần báo kết quả giới hạn cùng nguyên nhân và trao đổi lại hướng xử lý. Chuyển trọng tâm sang benchmark và ứng dụng không tự có nghĩa G2 được miễn hay yêu cầu kiến trúc mới biến mất. Mọi thay đổi phạm vi cần được ghi đúng quy trình quyết định của dự án.

### EN — Speaker script

Under the project's internal readiness checks, G1 has experimental labels independent of our prediction pipeline. G2 has an initial positive result but is incomplete. G3 is currently a software design. These are project checks, not official course gates.

The immediate work is matrix-model training, controlled architectural comparisons, ablations, seed stability and the Degformer comparison. Transfer evaluation remains a separate task. The end-of-week-ten checkpoint is recorded in the decision log; the detailed allocation across weeks seven to nine is provisional.

If the matrix target is unmet, I will report the bounded result and discuss the next direction. Shifting emphasis towards the benchmark and application does not automatically waive G2 or the architecture requirement.

### Đọc hiểu / Study notes

| Trạng thái / State | Điều có thể nói / Supported statement                                                                                                                                                      |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| G1                   | Nhãn được đo bên ngoài mô hình; chưa có nghĩa nhãn không nhiễu hoặc đến từ nhiều nhóm độc lập. / Experimental origin does not imply noise-free or multi-lab validation. |
| G2                   | Bộ quét dương; ma trận còn thua 0,0420; chưa có kiến trúc mới được chứng minh. / Positive scanning evidence, unresolved matrix and architectural goals.                          |
| G3                   | Thiết kế dịch vụ/harness có vai trò rõ; chưa có triển khai để nghiệm thu. / Defined software scope, no completed implementation.                                                   |

**Rủi ro nguồn:** cả hai tập residue của Zhang; đối chứng CTNNB1 đã không dùng theo [D-035](../../../../DECISIONS.md#d-035), chưa có nguồn thay thế phù hợp. Nếu được hỏi, trả lời thẳng. Không nói bộ Larsen hay MaveDB tự động đóng rủi ro này.

**EN:** A progress plan is not an approval record. Reproducible analysis, advisor approval and accepted thesis contributions are separate milestones.

**Hỏi sâu / Q&A:** “Kết quả âm có đủ làm trụ không?” — “Theo khung hiện hành thì không. Nó giúp phân tích và giới hạn kết luận, còn đóng góp dương cùng yêu cầu kiến trúc vẫn giữ.” / “Can a negative result replace the main contribution?” — “Not under the current framework; it informs analysis but does not waive the remaining requirements.”

**Chuyển / Transition:** “Em xin trao đổi bốn điểm để xác nhận khung và mức đóng góp.” / “I would like to discuss four points about the framework and contribution.”

**Nguồn / Sources:** [Điểm kiểm và kế hoạch](../../../../DECISIONS.md#d-029) · [nhiệm vụ hiện hành](../../../../DECISIONS.md#d-031) · [README nghiên cứu](../../README.md).

---

<a id="slide-26"></a>

## Slide 26 — Câu hỏi với GVHD / Questions for discussion

**Thông điệp / Message:** Xin xác nhận phạm vi và kỳ vọng; không tự ghi cuộc gặp đã duyệt đề tài. / Seek confirmation without inventing approval.

**Trạng thái / Status:** Câu 1 và 4 dưới đây diễn đạt lại câu đang có trên slide để tập nói; **chờ Trọng hoàn thiện lời hỏi cuối** theo ghi chú nguồn. Đây không phải biên bản hoặc quyết định mới. Câu 3 bỏ phép so Spearman sai cấp độ đã giải thích ở slide 17.

### VI — Lời thuyết trình

Em xin kết thúc bằng bốn điểm cần xin ý kiến thầy.

1. **Khung đóng góp:** Với bằng chứng giới hạn của lớp chỉ dùng thành phần, giao thức đánh giá và phần kiến trúc residue còn phải thực hiện, khung ba trụ động lực–phương pháp–phần mềm có phù hợp luận văn không? Nếu được chấp nhận, em xin ghi nhận vào biên bản, gồm cả xác nhận về trụ phần mềm.
2. **Mức đặt tính mới:** Em đặt câu hỏi ở giám sát yếu: nhãn toàn đoạn dồi dào có giúp đầu ra residue qua cầu nối MIL/attention và tốt hơn đầu được giám sát trực tiếp không? Các cơ chế thành phần đã có tiền lệ. Mức phát biểu như vậy có phù hợp kỳ vọng kiến trúc của thầy không?
3. **Đọc kết quả hai phía:** Hiện em hơn ΔPAP ở bộ quét +0,0300 và còn thua ở ma trận −0,0420. Em giữ AUROC mức ô là metric chính, báo chỉ số vị trí riêng và sửa phép đối chiếu Spearman đang lẫn cấp độ. Thầy góp ý thế nào về cách trình bày kết quả hai phía này trong luận văn?
4. **Phạm vi ứng dụng:** Web cùng API trả ma trận, bản đồ vị trí, bất định và xuất xứ có phù hợp tiêu chí ứng dụng không? Những phần nào cần được ưu tiên để tạo giá trị sử dụng rõ trong thời gian còn lại?

Em cảm ơn thầy. Các nguồn dữ liệu, script và kết quả có trong repo; em sẽ ghi lại chính xác phản hồi của buổi gặp.

### EN — Speaker script

I would like to close with four discussion points.

1. **Contribution framework:** Does the three-pillar framework—motivation, method and software—fit this thesis, given the composition-only limitation, evaluation protocol and residue architecture still to be developed? If accepted, may we record that framework, including the software contribution, in the meeting minutes?
2. **Architecture novelty:** I frame the question as weak supervision: can abundant segment-level labels improve residue outputs through an MIL/attention bridge beyond direct supervision? The component mechanisms are established. Is this an appropriate level for the architectural contribution?
3. **Two-sided evidence:** The current model gains 0.0300 on scanning and loses 0.0420 on the matrix. I retain cell-level AUROC as the primary metric and report position-level measures separately, correcting the mixed-level Spearman comparison. How should this two-sided result be presented in the thesis?
4. **Application scope:** Is a web service and API returning the matrix, position map, uncertainty and provenance an appropriate application? Which capabilities should receive priority within the remaining time?

Thank you. Data sources, scripts and result files are available in the repository, and I will record the meeting feedback accurately.

### Đọc hiểu / Study notes

Ba loại câu cần phân biệt khi trao đổi: **xin phê duyệt khung**, **xin góp ý phương pháp**, và **báo trạng thái đã có**. Thầy đồng ý rằng phần mềm được tính là đóng góp không tự có nghĩa toàn bộ đề tài đã duyệt hoặc G2 đã đạt.

Sau buổi gặp, phản hồi thực tế mới là đầu vào của biên bản. Nếu có hệ quả quyết định, ghi ở `DECISIONS.md` theo quy ước; không điền sẵn lời chấp thuận vào script hay log. Bản deck này có 26 slide, không có A1–A6 để bấm sang; khi được hỏi sâu có thể mở nguồn liên quan dưới đây.

**EN:** These are rehearsal questions, not answers from the advisor. Record the actual response and its authority; do not convert a software endorsement into blanket topic approval.

**Hỏi sâu / Q&A:** “Cần lấy gì về từ buổi gặp?” — “Xác nhận rõ khung có được duyệt không, kỳ vọng kiến trúc và phạm vi phần mềm; xin ghi biên bản thay vì tự suy diễn.” / “What should this meeting resolve?” — “The framework's approval state and concrete expectations, recorded rather than inferred.”

**Nguồn / Sources:** [C-5: mục đích buổi gặp](../../../../DECISIONS.md#c-5) · [D-034: xác nhận phần mềm được truyền đạt](../../../../DECISIONS.md#d-034) · [ghi chú slide gốc](index.html).

---

<a id="glossary"></a>

## Thuật ngữ tra nhanh / Quick glossary

| Thuật ngữ / Term             | Nghĩa dùng trong tài liệu / Meaning here                                                                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Amino acid / amino acid type   | Loại đơn vị hóa học, ký hiệu A, V, P… / The chemical type, represented by a letter.                                                                                                                 |
| Residue                        | Amino acid đã nằm trong chuỗi; gắn với vị trí khi lập bản đồ. / An amino acid unit incorporated in the chain.                                                                                    |
| Peptide / tile                 | Đoạn chuỗi ngắn; tile là cửa sổ lấy từ protein theo thiết kế thư viện. / A short segment; a tile is a designed protein window.                                                                  |
| Degron                         | Tín hiệu góp phần tạo nhận diện phân hủy trong ngữ cảnh phù hợp. / A context-dependent degradation signal.                                                                                      |
| Footprint                      | Các vị trí có đáp ứng đột biến theo định nghĩa assay/benchmark. / Positions identified by the mutational phenotype definition.                                                                  |
| WT / wild type                 | Trình tự tham chiếu của phép so, không có nghĩa không có degron. / The reference sequence, which may itself be a degron.                                                                           |
| Mutant / substitution          | Trình tự sau thay thế / phép thay một amino acid. / The altered construct / a single amino acid replacement.                                                                                            |
| GFP / reporter                 | Protein huỳnh quang / cấu phần giúp đo hệ đang xét. / A fluorescent protein / a measurable experimental reporter.                                                                                    |
| GPS / FACS                     | Profiling độ bền / phân loại tế bào theo tín hiệu huỳnh quang. / Stability profiling / fluorescence-activated cell sorting.                                                                        |
| PSI / ΔPSI                    | Chỉ số bin độ bền / hiệu mutant trừ WT; không phải xác suất. / Stability-bin index / mutant-minus-reference difference.                                                                           |
| Rescue-positive cell           | Ô có ΔPSI ≥1,0 trong benchmark hiện tại. / A cell meeting the benchmark's stabilisation threshold.                                                                                                     |
| Composition / context          | Số lượng loại amino acid / môi trường residue quanh vị trí. / Amino acid counts / neighbouring sequence information.                                                                                |
| One-hot / PLM                  | Biểu diễn rời rạc một loại bằng một vector / protein language model. / Discrete categorical encoding / protein language model.                                                                       |
| Ridge                          | Hồi quy tuyến tính có phạt L2, dùng làm mô hình kiểm khối đặc trưng. / L2-regularised linear regression used for feature comparisons.                                                          |
| MIL / bag / instance           | Học nhiều instance từ nhãn túi / peptide / cửa sổ quanh residue trong phương án này. / Multiple-instance learning / peptide / local window here.                                                  |
| rASA / pLDDT                   | Độ tiếp cận dung môi tương đối / độ tin cậy cục bộ của cấu trúc dự đoán. / Relative solvent accessibility / local predicted-structure confidence.                                        |
| Cluster / cov80                | Nhóm protein theo cấu hình tương đồng của repo; 80% là coverage. / Protein similarity cluster; 80% refers to coverage.                                                                              |
| AUROC / Spearman / precision@3 | Phân biệt ô dương–âm / tương quan thứ hạng / tỉ lệ vị trí dương trong top 3. / Ranking discrimination / rank correlation / positive fraction among top-three positions.                     |
| CI / bootstrap                 | Khoảng tin cậy / lấy lại mẫu để ước lượng biến thiên, ở đây theo cụm. / Confidence interval / resampling, here at cluster level.                                                            |
| MDE / power                    | Chênh lệch tối thiểu có lực phát hiện theo thiết kế / xác suất phát hiện hiệu ứng giả định. / Design-specific minimum detectable effect / detection probability under a specified effect. |
| Measurement ceiling            | Mốc tham chiếu ước lượng từ đối chiếu replicate; phụ thuộc metric, nhãn và tập. / A replicate-based reference, not a universal hard bound.                                                    |
| Calibration                    | Kiểm quan hệ giữa mức bất định báo ra và kết quả quan sát phù hợp. / Checking uncertainty statements against relevant held-out outcomes.                                                       |
| VUS / pathogenicity            | Biến thể chưa rõ ý nghĩa / tính gây bệnh; không phải endpoint ΔPSI. / Uncertain clinical significance / disease pathogenicity, distinct from ΔPSI.                                              |
| Provenance / harness / OOD     | Nguồn gốc / quy trình điều phối đánh giá / khác phân bố học. / Traceability / evaluation orchestration / distribution shift.                                                                    |

<a id="rehearsal"></a>

## Tự kiểm trước buổi gặp / Rehearsal checks

Các câu dưới đây là câu tự học, không phải đánh giá đã thực hiện và không thay hồ sơ hỏi đáp đang có.

1. **ΔPSI tăng thì peptide hay degron mạnh hơn?** — Reporter bền hơn; hoạt tính phân hủy của trình tự ban đầu có thể bị suy yếu. / Higher ΔPSI means reporter stabilisation, consistent with reduced degradation activity in context.
2. **2,148 nói gì?** — OR mức vùng, đã phân tầng protein, chưa khử mọi gây nhiễu; chưa xác lập tín hiệu bệnh ở residue. / A region-level odds ratio, not residue-level clinical validation.
3. **89,7% nói gì?** — Trong tập footprint đã audit, có nhóm cùng cặp thay thế mà nhãn khác lớp; không phải tỉ lệ lỗi mô hình. / A representation conflict rate in the audited subset, not predictive error.
4. **+0,0289 khác +0,0300 thế nào?** — M3−M0 và M3−ΔPAP w7, trên hai tập ghép cặp khác nhau. / Different controls and matched populations.
5. **Còn thiếu gì để nói G2 hoàn tất?** — Mục tiêu ma trận, thành phần kiến trúc cùng đối chứng cần thiết vẫn còn. / Matrix, architecture and required comparison evidence remain open.
6. **0,9519 có phải CI95 của một ô?** — Không; đó là AUROC tham chiếu đo lường ở bộ bão hòa. / It is a benchmark-level AUROC reference, not a cell's interval or confidence.
7. **Vì sao không nói thắng Spearman mức vị trí 0,4440 so với 0,3553?** — 0,3553 là mức ô; PAP mức vị trí ghi 0,4130 và chưa có CI delta đồng nhất. / The levels are mixed, and a matched position-level comparison is not established here.
8. **Đã có phần mềm chưa?** — Chưa, mới thiết kế; chưa đo calibration hay độ phủ khoảng dự đoán. / Designed only, with no measured calibration coverage.

<a id="sources"></a>

## Nguồn để mở khi hỏi sâu / Source map

Tài liệu này biên soạn từ bản paste và chứng cứ sẵn có trong repo; **không thực hiện khảo sát web mới, không huấn luyện, không chạy benchmark mới**. Một số báo cáo giữ đoạn lịch sử hoặc đề xuất cũ; khi xung đột về trạng thái, tra sổ quyết định. Với metric, truy trường cụ thể trong JSON và code thay vì dùng lại câu diễn giải sai.

| Nguồn / Source                                                                                                                                                                                                           | Dùng cho / Use                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [index.html](index.html) và [README deck](README.md)                                                                                                                                                                       | Thứ tự, hình và ghi chú gốc của 26 slide. / Original slide order and notes.                                                                                              |
| [DECISIONS.md](../../../../DECISIONS.md#hien-hanh)                                                                                                                                                                         | Trạng thái, phạm vi và hiệu lực; đặc biệt D-025, D-028, D-031, D-033–D-036. / Current decision authority.                                                             |
| [Composition-context audit](../../research/composition-context-audit.md)                                                                                                                                                   | Công thức cận thành phần và mẫu số 2.624; không dùng các oracle cũ làm baseline huấn luyện. / Representation proof and audited population.                       |
| [Residue-task report](../../research/residue-task-derisk-2026-10-15/README.md)                                                                                                                                             | Hai bộ nhãn, M0–M4, phân rã và chuyển nguồn; đoạn Spearman phải đối chiếu lại JSON. / Model and transfer evidence, subject to the metric correction above.       |
| [model.json](../../research/residue-task-derisk-2026-10-15/model.json), [headline.json](../../research/residue-task-derisk-2026-10-15/headline.json), [power.json](../../research/residue-task-derisk-2026-10-15/power.json) | Hiệu năng, tập ghép cặp, CI và MDE theo phép so. / Numeric performance, matched cohorts and power.                                                                       |
| [PAP report](../../research/pap-baseline/README.md) và [PAP JSON](../../research/pap-baseline/pap-baseline.json)                                                                                                           | Tái lập PAP; phân biệt `cell_level` với `position_level`. Trạng thái lịch sử trong report không thay quyết định hiện hành. / Reproduction and metric levels. |
| [Full-data audit](../../research/full-data-audit/README.md) và [psi-build.json](../../research/full-data-audit/psi-build.json)                                                                                             | Tính PSI, lỗi header, Jaccard và phân rã nhiễu. / Reconstruction and measurement variability.                                                                             |
| [Variant-coverage report](../../research/variant-coverage-2026-10-15/README.md)                                                                                                                                            | OR mức vùng, ba phép kiểm residue, 530.412 VUS và mẫu số 87,3%. / Motivation and application-domain counts.                                                              |
| [Example-matrix JSON](../../research/slide-figures-2026-10-15/example-matrix.json) và [README hình](../../research/slide-figures-2026-10-15/README.md)                                                                    | Nhãn HIF1A từng ô, quy tắc chọn, WT và đối chiếu P564. / Exact example values and provenance.                                                                          |
| [Data README](../../data/README.md)                                                                                                                                                                                        | Schema, định danh, chiều nhãn, mask và nguồn từng file. / Dataset dictionary and processing history.                                                                     |
| [Larsen and risks](../../research/larsen-nuclear-and-risks-2026-10-15/README.md)                                                                                                                                           | Hồ sơ Degformer, tính năng công cụ và giới hạn chuyển ngăn. / Precedent and transfer audit.                                                                          |
| [Advisor presentation guide](../../../../project/advisor-presentation-guide.md)                                                                                                                                            | Cách nối câu hỏi–phép so–kết quả–giới hạn; hướng dẫn tham khảo, không phải yêu cầu mới của GVHD. / Evidence-oriented presentation guidance.               |

**Các giới hạn còn giữ / Remaining limits:** chưa xác nhận toàn bộ tính năng công cụ bằng kiểm tra mới; chưa khép xác nhận Larsen; chưa có kiến trúc sâu hoặc ứng dụng; chưa xác lập liên hệ bệnh mức residue. Script không biến các việc đó thành kết quả đã có.
