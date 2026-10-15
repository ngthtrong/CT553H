# Nhật ký hỏi đáp và đánh giá hiểu biết — degron-footprint

## Mục đích và cách tiếp tục

Theo yêu cầu của Trọng ngày **15/10/2026**: hỏi đáp từ sinh học cơ bản đến tin sinh học và kỹ thuật phần mềm của đề tài; đánh giá trung thực theo câu trả lời; ghi lại quá trình và lặp lại để khắc phục lỗ hổng.

Đây là **hồ sơ học tập**, không ghi quyết định nghiên cứu. Trạng thái và đề xuất của dự án được tra tại [DECISIONS.md](../../../DECISIONS.md). Không suy ra năng lực từ việc đã có tài liệu trong repo.

Mỗi vòng: đặt 4–6 câu → lưu nguyên văn câu trả lời → đánh giá từng câu và trích bằng chứng → giải thích chỗ thiếu → giao bài sửa → kiểm tra lại bằng tình huống khác ở vòng sau. Ghi rõ câu nào có gợi ý hoặc có tra tài liệu. Không xem câu bỏ trống là bằng chứng rằng người học hiểu sai.

Thang cho **từng câu đã trả lời**: **0** = sai trọng tâm hoặc sai cơ chế chính; **1** = có ý đúng nhưng thiếu/mâu thuẫn đáng kể; **2** = đúng cốt lõi, còn thiếu chi tiết hoặc giới hạn; **3** = đúng, giải thích được và áp dụng được trong phạm vi câu hỏi. Chọn đúng trắc nghiệm nhưng chưa giải thích chưa đủ chứng minh mức 3. “Chưa kiểm tra” và “chưa đủ bằng chứng” tách riêng khỏi điểm 0.

Mức tự tin của người học (thấp/vừa/cao) chỉ dùng để phát hiện đoán đúng hoặc tự tin sai; không cộng điểm. Chỉ ghi một nội dung **đã nắm vững trong phạm vi đã kiểm tra** sau ít nhất hai lần giải thích/vận dụng độc lập đúng, có một lần ở vòng sau và không cần gợi ý. Không hứa suy ra việc hiểu mọi chi tiết từ một tổng điểm.

Khi tiếp tục ở phiên khác: đọc chỉ dẫn repo, trạng thái hiện hành, nhật ký này và vòng gần nhất; bắt đầu từ câu đang chờ hoặc bài cần kiểm tra lại. Không tự sinh câu trả lời hay kết quả khi người học chưa phản hồi.

## Phạm vi cần kiểm tra dần

| Mảng | Nội dung | Bằng chứng hiện có |
|---|---|---|
| Nền tảng sinh học | Gene, protein, acid amin, residue, peptide, gấp cuộn, đột biến | V2: đã gọi đúng phiên mã/dịch mã sau phản hồi; thay thế aa đúng qua ví dụ khác. Chưa kiểm tra nhớ lại không gợi ý |
| Cơ chế degron | E3, ubiquitin, proteasome; phụ thuộc bối cảnh, giới hạn cơ chế | V2: biết chưa chứng minh tiếp xúc trực tiếp nhưng vẫn gọi E3-X là E3 nhận diện; cần phân biệt phụ thuộc chức năng/nhận diện |
| Thí nghiệm và nhãn | Reporter GFP, GPS/FACS, PSI/ΔPSI đúng chiều, WT, replicate, quét/bão hòa | V2: tính +1,4 đúng và đúng chiều làm bền; tự nêu chưa biết WT/hiệu ứng đo; chưa phân biệt rõ ΔPSI với xác suất |
| Bài toán tính toán | Đầu vào/ra theo vị trí và theo thay thế, thành phần/ngữ cảnh, ΔPAP | V2: đọc đúng ô M7V, hiểu đầu vào đếm thành phần không chứa thứ tự; chưa nối tới Δ dự đoán và khác biệt thực nghiệm |
| Thiết kế nghiên cứu | Nguồn dữ liệu, split cụm protein, rò rỉ, baseline/oracle, ablation, trần thực nghiệm | Chưa kiểm tra |
| Thống kê và đánh giá | Precision@3, AUROC, Spearman, bất định, lực, phụ thuộc trong cụm | Chưa kiểm tra |
| Kỹ thuật phần mềm | Pipeline tái lập, provenance, hợp đồng API, xử lý đầu vào, ứng dụng hữu ích | Chưa kiểm tra |
| Bảo vệ đề tài | Ý nghĩa, G1/G2/G3, tiền lệ, đóng góp dự kiến, giới hạn và trạng thái | V1: nêu được người dùng, chưa huấn luyện và đóng góp còn chưa rõ; chưa nêu các đối chứng đã chạy/G1–G3 |

## Căn cứ đọc ngày 15/10/2026 và xung đột cần tránh khi chấm

- [DECISIONS.md phần A/C và D-025](../../../DECISIONS.md): căn cứ trạng thái. Các C-7 đến C-11 vẫn là đề xuất, không dùng làm đáp án “đã chốt”.
- [Thẻ đề tài](../README.md), [nhật ký nghiên cứu](../log.md), [lập luận 15/10](../research/topic-argument-2026-10-15.md), [audit dữ liệu](../research/full-data-audit/README.md), [đối chứng ΔPAP](../research/pap-baseline/README.md), [báo cáo mới nhất](../research/larsen-nuclear-and-risks-2026-10-15/README.md), [sổ dữ liệu](../data/README.md).
- **Lỗi tài liệu học:** [bài 2](../../../lectures/degron-basics/02-how-degrons-are-measured.md) §2–3 ghi ngược chiều PSI/ΔPSI so với sổ dữ liệu §4 và [mã gọi footprint](../research/e3-labels-audit/count_footprints.py). Trong dữ liệu Zhang đang dùng: **PSI thấp = kém bền; ΔPSI = PSI(mut) − PSI(WT) dương = làm bền reporter**, phù hợp đột biến làm yếu tác dụng degron trong assay. Không dùng chiều sai để chấm người học. Bài 2 còn dùng vai trò bộ quét/bão hòa và replicate cũ, trái D-025; tra nguồn hiện hành. Chưa sửa bài giảng trong hoạt động hỏi đáp này.
- **Tính mới:** lập luận 15/10 §6–7 vẫn có câu chưa cập nhật về ma trận 28×20. Báo cáo cùng ngày và thẻ đề tài đã nêu Degformer là tiền lệ xuất ma trận, DegronMD có module đột biến. Không chấm phát biểu “chưa ai xuất ma trận” là đúng.
- **Nhãn và suy luận:** không coi footprint đo bằng reporter là bản đồ tiếp xúc trực tiếp với E3; không coi độ lặp giữa replicate là trần toán học tuyệt đối; không coi mọi ô đột biến hoặc mọi peptide cùng protein là quan sát độc lập. Lực trên bộ quét không giải quyết lực cho bộ bão hòa 91 peptide; còn phải xét số cụm và tập test thực tế.

## Vòng 1 — 15/10/2026 — chẩn đoán nền tảng

**Trạng thái:** Đã nhận và đánh giá câu trả lời; chuyển sang vòng 2. Chưa có nội dung nào đủ hai lần kiểm tra độc lập để ghi nắm vững.

Hướng dẫn: trả lời bằng hiểu biết hiện tại; có thể viết “chưa biết”. Với câu trắc nghiệm, nêu lựa chọn và lý do ngắn. Ghi tự tin thấp/vừa/cao cho từng câu; nếu tra tài liệu thì ghi rõ.

### Câu hỏi đã đặt

**1. Protein là gì? Chọn mô tả đúng nhất và giải thích.**

A. Một đoạn DNA trực tiếp đi thực hiện mọi chức năng trong tế bào.

B. Một phân tử gồm một hoặc nhiều chuỗi acid amin, có thể gấp thành cấu trúc và thực hiện các chức năng trong tế bào.

C. Một chuỗi nucleotide luôn được dùng để lưu thông tin di truyền.

D. Một loại enzyme chỉ có nhiệm vụ phân hủy các phân tử khác.

**2. Đọc một đột biến.** Cho chuỗi `MKTALVA`, đánh số từ 1. `A4V` có nghĩa gì? Viết chuỗi sau đột biến. “Residue ở vị trí 4” khác “loại acid amin A” ở điểm nào?

**3. Từ gene đến protein.** Bằng lời của bạn, gene liên quan thế nào đến protein? Nếu hai protein có cùng số lượng từng loại acid amin nhưng thứ tự khác nhau, chúng có bắt buộc hoạt động giống nhau không? Vì sao?

**4. Cơ chế phân hủy.** Trong con đường ubiquitin–proteasome thường được xét ở đề tài, mô tả nào đúng nhất? Giải thích vai trò của degron, E3 và proteasome.

A. Degron là tín hiệu có thể được hệ nhận diện cơ chất của E3 nhận ra; E3 tham gia gắn ubiquitin; proteasome phân giải protein đích phù hợp.

B. Degron là enzyme cắt protein; E3 cung cấp ánh sáng; proteasome tạo gene mới.

C. E3 và proteasome là hai tên gọi của cùng một phân tử.

D. Chỉ cần một chuỗi có degron thì nó chắc chắn bị phân hủy như nhau trong mọi tế bào.

**5. Diễn giải thí nghiệm.** Người ta gắn một peptide vào GFP. Bản gốc cho tín hiệu xanh thấp; thay một acid amin thì tín hiệu xanh tăng. Giả sử đã kiểm soát các yếu tố khác và tín hiệu phản ánh lượng reporter: bạn giải thích thay đổi này thế nào? Kết quả có đủ chứng minh cùng đột biến cũng làm protein nguyên vẹn bền hơn, hoặc xác định E3 nào nhận diện, không? Vì sao?

**6. Hiểu đề tài bằng lời của bạn.** Trong 3–5 câu, hãy nói: đề tài muốn giúp ai làm việc gì; đầu vào và đầu ra dự kiến là gì; nó khác thế nào với việc chỉ chấm một điểm cho cả peptide. Nếu biết, nói thêm đâu là việc đã làm và đâu là việc còn dự kiến. Không cần nhớ số liệu.

### Câu trả lời nguyên văn

Lưu nguyên nội dung câu trả lời, giữ lỗi gõ và ký hiệu của người học. Người học chưa cung cấp mức tự tin hoặc thông tin có tra tài liệu hay không; **không tự suy ra**.

```text
vòng 1:

1. &#x20;B; trong tế bào protein sẽ liên tục được sinh ra và phá hủy và mức này phải được giữ ở mức cân bằng
2. A4V nghĩa là thay vị trí aa thứ 4 từ A -> V; residue ở vị trí thứ 4 là đang xét trên một chuỗi aa nào đó và có ý nghĩa về mặt vị trí, còn loại aa A chỉ có nghĩa nói về loại aa A không có thông tin về mặt vị trí
3. gen được cấu trành từ chuỗi DNA gồm 4 loại  a t g x, sau quá trình dịch mã thành RNA gồm 4 loại a u g x, thứ tự của các thành phần này sẽ quyết định các loại aa sau quá trình phiên mã, từ đó quyết định thứ tự chuỗi amino acid cấu thành nền protein; nếu 2 protein có cùng số lượng của các loại aa nhưng có thứ tự khác nhau thì chúng có thể giống hoặc khác nhau về các hoạt động vì về bản chất thứ tự của chuỗi aa sẽ quyết định chức năng của protein đó;
4. A, vai trò của degron giống như một cờ hiệu nằm trên protein để E3 có thể nhận diện và gắn vào protein một lá cờ ubiquitin khi gặp proteasome nếu protein đã được gắn ubiquitin thì sẽ bị phân hủy, mức độ bền của protein phụ thuộc vào việc degron có dễ bị E3 nhận ra hay không
5. \- khi thay một aa và làm tín hiệu xanh tăng có tức là thay đổ này làm độ bên của protein tăng lên, tức là sau thay đổ degron khó bị nhận biết hơn => vị trí đó ban đầu tỉ lệ cao à degron sau khi thay đổi thì làm degron khó nhận diện hơn từ đó protein bền hơn; kết quả này chỉ đang thí nghiệm ở peptide chưa kết luận được ở protein nguyên vẹn thì trong thực tế cấu trúc protein có văn xoắn và gắp khúc nên cùng là chuỗi mang đi thí nghiệp có kết quả cao nhưng trong môi trường thực tế có thể nằm khuất không các vặn xoắn khiến E3 khó nhận ra ; chưa kết luận được E3 nào nhận hiện, tôi chưa nắm rõ về các xác định được E3 nào nhận diện được degron
6. Đề tài muốn giúp ai làm việc gì? giúp các nhà khoa học đặc biệt là trong lĩnh vực tin sinh học khi các nhà khoa học về tin sinh học đặc biệt là đang nghiên cứu về việc nhận diện degron trong việc xác định đâu là vị trí quan trong gây phân hủy và độ tin cậy của các vị trí này;

- Đầu vào dự kiến là chuỗi peptide \~28-30 aa, một số thông tin khác về độ mức độ lộ ra của chuỗi; đầu ra là giá xem chuỗi này có tỉ lệ bao nhiều là degron, đâu là vị trí quan trọng của chuỗi này ảnh hưởng nhiều đến mức độ phân hủy, và ma trận 28x28 về thể hiện mức độ ảnh hưởng của việc thay đổi một aa tại một vị trí;
- nó khác với việc chấm điểm cho cả peptide ở chỗ chỉ ra đâu là vị trí quan trọng, để giúp các nhà nghiên cứu có một chỉ số để xếp mức độ ưu tiên trong thí nghiệm, và chỉ ra được sự khác nhau về mặc vị trí của aa thay vì dự đoán tỉ lệ chung cho cả đoạn;
- Việc là làm tải và phân tích dữ liệu của các nghiên cứu liên quan như của voutsino và zhang từ đó đang xác định khoảng trống; việc chưa làm là chưa bắt tay vào huống luyện mô hình và đặc tả ứng dụng vì còn chưa thực sự xác định được đóng góp cốt lỗi của đề tài và chưa thực sự xác định vấn đề mà bài toán đang hướng đến để giải quyết
```

### Đánh giá, giải thích sửa sai và bài kiểm tra lại

| Câu | Điểm /3 | Bằng chứng và đánh giá | Nội dung cần sửa/kiểm tra |
|---|---:|---|---|
| 1 | 2 | Chọn B đúng; giải thích thêm về sinh/phá hủy protein, nhưng chưa giải thích bản chất chuỗi acid amin/cấu trúc. Không kết luận chưa hiểu cấu tạo chỉ vì chưa nói | Phân biệt cấu tạo protein với điều hòa lượng protein; cân bằng là động, không phải lượng mọi protein luôn cố định |
| 2 | 2 | “A -> V” ở vị trí 4 và phân biệt residue/loại aa đều đúng. Chưa viết chuỗi sau đột biến | Đáp án phần còn thiếu: `MKTVLVA`. Kiểm tra vận dụng bằng chuỗi khác; không coi phần bỏ trống là đáp án sai |
| 3 | 1 | Nêu được đường DNA → RNA → chuỗi aa và vai trò thứ tự, nhưng gọi DNA → RNA là “dịch mã”, RNA → protein là “phiên mã”: đảo đúng hai tên quá trình trọng tâm | Sửa: DNA —phiên mã→ RNA; mRNA —dịch mã→ chuỗi aa. C/X đều chỉ cytosine theo cách ký hiệu tương ứng, không chấm X là sai. Chưa đủ biết là nhầm tên hay nhầm sâu cơ chế; V2 kiểm tra lại |
| 4 | 2 | Chọn A và đúng vai trò chính; câu “đã được gắn ubiquitin thì sẽ bị phân hủy” quá tuyệt đối. Độ bền không chỉ phụ thuộc nhận diện degron | Ub còn có vai trò khác; kiểu tín hiệu Ub, cơ chất và bối cảnh ảnh hưởng kết cục. E1/E2 là kiến thức mở rộng sẽ học dần, không trừ điểm chỉ vì câu hỏi chưa yêu cầu |
| 5 | 2 | Đúng chiều reporter sáng hơn phù hợp làm bền trong điều kiện đề bài; đúng giới hạn peptide/protein và chưa xác định E3. Câu “tức là ... degron khó bị nhận biết hơn” biến một giả thuyết thành kết luận | Đo hiệu ứng reporter không đo trực tiếp liên kết E3. Không gọi một residue đơn lẻ là “một degron” chỉ từ phép đo đó. Việc chưa biết cách gán E3 là lỗ hổng do người học tự nêu, không trừ thêm vì câu hỏi không yêu cầu thiết kế thí nghiệm |
| 6 | 2 | Đúng đối tượng nghiên cứu, đầu ra mức vị trí, ưu tiên thí nghiệm và chưa huấn luyện; nhầm 28×28, chưa phân biệt xác suất degron với ΔPSI | Ma trận L×20, với L=28 có 28×19=532 thay thế khác WT; điểm chính là hiệu ứng đột biến. Đặc trưng cấu trúc là tùy phạm vi, không mặc định bắt buộc. Khoảng trống đã có audit và đối chứng, nhưng đóng góp dương chưa được xác lập |

Không dùng tổng điểm sáu câu để suy ra “phần trăm hiểu đề tài”. Bằng chứng hiện tại: có nền nhận diện thuật ngữ và mục đích bài toán; cần sửa thuật ngữ biểu hiện gene, hợp đồng đầu ra và mức độ chắc chắn của suy luận cơ chế. Thống kê, leakage, kiến trúc, baseline/oracle, pipeline và API **chưa được kiểm tra**.

### Giải thích đã cung cấp sau chấm V1

1. Với gene mã hóa protein: thông tin DNA được **phiên mã** sang RNA; mRNA được ribosome **dịch mã** thành chuỗi aa. Không hiểu là toàn bộ DNA biến vật chất thành RNA, hoặc mọi RNA đều mã hóa protein. Nguồn: [NHGRI RNA fact sheet](https://www.genome.gov/about-genomics/educational-resources/fact-sheets/ribonucleic-acid-fact-sheet).
2. `A4V` trên `MKTALVA` cho `MKTVLVA`. Với peptide L residue, ma trận L×20 có hàng là vị trí, cột là aa đích; tại cột aa gốc, ΔPSI=0 theo định nghĩa so với cùng WT. Có L×19 thay thế khác aa gốc, chưa tính stop/indel. Ma trận này không mô tả tương tác giữa từng cặp vị trí. Nguồn đề tài: [sổ dữ liệu](../data/README.md), [đối chứng ΔPAP](../research/pap-baseline/README.md).
3. Trong thang Zhang đang dùng: PSI thấp tương ứng kém bền; ΔPSI dương nghĩa reporter bền hơn, phù hợp giảm tác dụng degron trong assay. Một điểm ΔPSI liên tục không phải xác suất “là degron”. Bản đồ vị trí cần quy tắc gộp/định nghĩa nhãn, không tự đồng nhất với xác suất.
4. GFP tăng trong điều kiện đề bài phù hợp reporter tích lũy/bền hơn. “Giảm nhận diện E3” là một cơ chế có thể có, **chưa được chứng minh**. Một residue gây hiệu ứng không tự nó là một degron hoàn chỉnh hoặc vị trí tiếp xúc trực tiếp E3. Không suy ra thời gian bán hủy định lượng từ một điểm fluorescence.
5. Nhập môn xác định E3: thí nghiệm gợi ý là làm mất chức năng E3/adaptor ứng viên, xem reporter có được làm bền hay không, rồi phục hồi gene để kiểm tra hiệu ứng trở lại; kèm đối chứng biểu hiện và perturbation. Đó là bằng chứng phụ thuộc chức năng, chưa tự chứng minh tương tác trực tiếp. Để chứng minh trực tiếp cần thêm bằng chứng liên kết và/hoặc ubiquitination tái lập với thành phần tinh sạch thích hợp. Đây là mô tả nguyên tắc, không phải protocol được triển khai. Bài gốc [Zhang 2023](https://pubmed.ncbi.nlm.nih.gov/37738965/) dùng CRISPR để tìm tính đặc hiệu E3.
6. Sửa quy tắc Ub: có gắn Ub không đồng nghĩa chắc chắn sẽ bị phân hủy. [Spence và cộng sự 1995](https://pubmed.ncbi.nlm.nih.gov/7862120/) phân biệt tác dụng của kiểu chuỗi Ub liên quan sửa DNA với turnover protein. Không yêu cầu học chi tiết liên kết K48/K63 ở vòng này.
7. Trạng thái được đọc lại trong lượt này: phần C đã thêm C-12/C-13; hướng phân rã khoảng cách tổng quát hóa và đổi nhãn chính **chưa được xác nhận**. Không lấy đề xuất đó thay đáp án trạng thái theo [D-025](../../../DECISIONS.md#d-025). Các số “trần chính xác” trong phân tích mới chưa được tái kiểm định trong hoạt động hỏi đáp này; không coi là chân lý tuyệt đối để chấm người học.

### Nội dung cần ôn và lịch kiểm tra

- Ngay V2: gọi đúng hai bước, mô tả ma trận và dấu ΔPSI, phân biệt quan sát/giả thuyết, bắt đầu kiểm quan hệ thành phần/ngữ cảnh.
- Sau đó: hỏi lại bằng ví dụ mới không có lời giải ngay trước; chưa đánh dấu nắm vững chỉ vì lặp lại được đáp án vừa đọc.
- Vòng sau nữa khi nền vững hơn: assay/replicate, nguồn quét–bão hòa, baseline và split, metrics/uncertainty, rồi kiến trúc và kỹ thuật phần mềm. Không vội sang thống kê nâng cao chỉ vì biết mục tiêu chung.

## Vòng 2 — củng cố sau phản hồi và nối sang bài toán tính toán

**Trạng thái:** Đã nhận và đánh giá năm câu, chuyển sang vòng 3. Người học vừa nhận giải thích trước vòng này, vì vậy kết quả chưa đủ xác nhận ghi nhớ bền vững.

**1. Sửa lại đường đi thông tin.** Điền tên quá trình vào `DNA —(?)→ RNA` và `mRNA —(?)→ chuỗi acid amin`. Ribosome đọc DNA hay mRNA để tổng hợp chuỗi aa?

**2. Đọc ma trận và thang điểm.** Một peptide 28 aa có ma trận dự đoán 28×20. Ô ở hàng 7, cột V có nghĩa gì nếu aa gốc ở vị trí 7 là M? Nếu PSI(WT)=1,8 và PSI(M7V)=3,2 thì ΔPSI bằng bao nhiêu, reporter bền hơn hay kém bền hơn? Con số ΔPSI có phải xác suất “là degron” không?

**3. Phân biệt đo được và suy đoán.** Thay một aa làm GFP tăng trong điều kiện đã kiểm soát như V1. Chọn phát biểu được dữ liệu hỗ trợ tốt nhất và giải thích vì sao hai phát biểu còn lại đi quá xa:

A. Đã chứng minh E3 không còn liên kết trực tiếp với vị trí đó.

B. Trong assay này, reporter đột biến tích lũy nhiều hơn; giảm tác dụng degron là cách giải thích phù hợp, nhưng cơ chế nhận diện E3 chưa được xác định.

C. Cùng đột biến chắc chắn làm protein nguyên vẹn bền hơn trong mọi loại tế bào.

**4. Bắt đầu suy luận về E3.** Giả sử làm mất chức năng E3-X khiến reporter sáng hơn; đưa E3-X hoạt động trở lại khiến reporter giảm sáng; các đối chứng cần thiết đều đạt. Kết quả ủng hộ E3-X tham gia kiểm soát độ bền reporter thế nào? Nó đã đủ chứng minh E3-X tiếp xúc trực tiếp với peptide chưa? Giải thích ngắn; không cần biết kỹ thuật phòng thí nghiệm cụ thể.

**5. Từ thành phần sang ngữ cảnh.** Cho chuỗi `MALAKLA`. Xét `A2V` và `A4V`: viết hai chuỗi sau thay thế. Một mô hình **chỉ nhận số lượng từng loại aa**, bỏ toàn bộ thông tin thứ tự, có thể cho hai chuỗi đó điểm khác nhau không (giả sử dự đoán xác định)? Δ dự đoán so với cùng WT có thể khác nhau không? Hiệu ứng đo thật có bắt buộc giống nhau không? Vì sao?

### Câu trả lời nguyên văn và đánh giá V2

Người học gửi trước câu 1: `1. DNA phiên mã -> RNA; mRNA -> dịch mã tại ribosome -> chuỗi aa;`. Lượt bị ngắt trước khi có phản hồi hoặc thay đổi hồ sơ. Sau đó người học gửi bản đầy đủ dưới đây; chỉ chấm một lần từ bản đầy đủ, không tính câu gửi trước là một lần kiểm tra độc lập.

```text
1. &#x20;DNA phiên mã -> RNA; mRNA -> dịch mã tại ribosome -> chuỗi aa;
2. \- ô hàng 7 cột V có nghĩa là giả trị dự đoán của `Δ`  PSI khi M7V; ΔPSI = 3,2 - 1,8 = 1,4; reporter bền hơn; có xác xuất là degron, nhưng chưa hiểu để giải thích một cách chi tiết;
3. B; 2 nhận định còn lại nhận định rằng chắc chắn đã là một nước đi quá xa;&#x20;
4. Kêt quà này ủng hoojv iệc E3-X chính là E3 nhận diện degron trong peptide trên, nhưng chưa chắc E3-X tiếp xúc trực tiếp với peptide&#x20;
5. MVLAKlA và MALVKLA; một hình chỉ nhận số lượng từ loại aa đương nhiên không phân biệt được thứ tự vì không có chế để xét đến thứ tự vị trí của mỗi aa trên chuỗi; WT là gì?; không hiểu lắm hiểu ứng đo bằng thi nghiệm là gì?
```

Chưa có mức tự tin hay thông tin tra tài liệu. Không coi lỗi gõ/viết hoa `l` trong `MVLAKlA` là nhầm residue khi các vị trí thay thế được viết đúng.

### Đánh giá V2

| Câu | Điểm /3 | Bằng chứng và giới hạn nhận định |
|---|---:|---|
| 1 | 3 | Đã gọi đúng hai bước và đặt dịch mã tại ribosome với đầu vào mRNA. Sửa được lỗi V1 ngay sau phản hồi; cần hỏi lại sau một khoảng nội dung khác trước khi ghi nắm vững |
| 2 | 2 | Đúng ô M7V, phép trừ +1,4 và chiều làm bền. Câu “có xác xuất là degron” chưa phân biệt rõ “ΔPSI là xác suất” với “kết quả cung cấp bằng chứng về tác dụng degron”; cần giải thích và yêu cầu diễn đạt lại, không tự gán ý định chính xác cho câu mơ hồ |
| 3 | 2 | Chọn B đúng, nhận ra kết luận quá chắc. Chưa giải thích hai lỗi chứng cứ khác nhau: A suy ra liên kết trực tiếp từ đo lượng reporter; C khái quát sang protein/cell type ngoài phạm vi đo. Không xem chỉ thêm từ “có thể” là đã sửa được loại kết luận |
| 4 | 2 | Biết chưa chứng minh tiếp xúc trực tiếp. “Chính là E3 nhận diện” vẫn mạnh hơn dữ liệu mất chức năng/phục hồi: có thể gián tiếp qua một thành phần khác. Đúng mức hiện tại là tham gia điều hòa độ bền reporter trong điều kiện thí nghiệm |
| 5 | 2 | Hai chuỗi thay thế đúng về vị trí; hiểu giới hạn đầu vào đếm thành phần. Các phần WT/Δ dự đoán/hiệu ứng đo chưa có câu trả lời; người học tự nêu thiếu thuật ngữ. Đây là bằng chứng cần giảng lại, không ghi các phần chưa trả lời thành đáp án sai |

**Điều chỉnh cách giảng:** người dạy đã dùng WT mà chưa khai triển rõ ngay trong câu hỏi và chưa định nghĩa cụ thể “hiệu ứng đo thật”. Bổ sung định nghĩa và ví dụ trước khi kiểm tra lại. Không quy lỗi thiếu lời giải thích của câu hỏi thành lỗi suy luận của người học.

**Tiến bộ có bằng chứng:** sửa đúng tên hai bước biểu hiện gene; đọc được một ô ma trận; tính đúng hiệu số PSI và chiều làm bền; hiểu vì sao đầu vào đếm thành phần mất thông tin thứ tự. **Chưa vững:** ΔPSI/xác suất, WT và phép đối chiếu WT–mutant, quan sát–cơ chế, phụ thuộc E3–nhận diện trực tiếp. Không chuyển sang thống kê nâng cao trong vòng kế tiếp.

### Giải thích bổ sung sau V2

- **WT = wild type**, thường dịch “kiểu hoang dại”. Trong ví dụ thay thế đơn của bài học, WT là trình tự gốc đang dùng làm mốc đối chiếu; mutant là phiên bản thay một aa so với mốc đó. Không suy ra WT nghĩa là không có degron, bền nhất, lành tính, hoặc hoàn toàn không có biến dị so với mọi người. Nguồn thuật ngữ: [MGI/Jackson Laboratory](https://www.informatics.jax.org/glossary/wild_type); cách dùng trong dữ liệu đề tài: [data/README.md](../data/README.md). Trong bộ bão hòa của repo, WT tham chiếu có cách dựng nội tại từ các construct đồng nghĩa; chi tiết đó để vòng sau, chưa cần dùng cho bài tập nhập môn.
- Với `MALAKLA` làm WT: `A2V` cho `MVLAKLA`, `A4V` cho `MALVKLA`. Tương tự phần mềm: giữ một bản gốc, tạo hai bản mỗi bản sửa một vị trí, so kết quả mỗi bản với cùng mốc. Đây là phép tương tự về thiết kế đối chiếu, không đồng nhất protein với chương trình xác định.
- **Hiệu ứng đột biến đo bằng thí nghiệm** trong bài học là chênh lệch PSI suy từ tín hiệu reporter giữa mutant và WT trong cùng thiết kế assay. Phân biệt: tín hiệu/GPS → tính PSI → trừ WT cho ΔPSI thực nghiệm; còn mô hình nhận chuỗi → đưa ΔPSI dự đoán. ΔPSI thực nghiệm cũng có sai số đo và không tự chứng minh cơ chế E3. Không đồng nhất tín hiệu đo với dự đoán của máy.
- **ΔPSI = +1,4** là tăng **1,4 điểm PSI** so với WT, không phải 1,4%, 14%, 140% hay xác suất bất kỳ. Nó có thể âm. Từ hiệu ứng đủ lớn, có đối chứng và độ lặp phù hợp có thể suy ra bằng chứng về vai trò degron trong assay, nhưng muốn một xác suất phải định nghĩa sự kiện và mô hình xác suất riêng, có hiệu chuẩn/đánh giá phù hợp. Chưa cần học hiệu chuẩn ở vòng này.
- **Giới hạn thành phần:** hai mutant trên có cùng số lượng từng aa. Nếu f chỉ nhận vector số lượng, f(A2V)=f(A4V); trừ cùng f(WT) vẫn bằng nhau. Đây là ràng buộc của mô hình, không buộc hai phép đo thực nghiệm bằng nhau. Mỗi vị trí có hàng xóm/bối cảnh khác nhau nên hiệu ứng thật có thể khác; sai số đo cũng có thể tạo khác biệt, cần lặp và đối chứng để phân biệt. Không hứa thêm thứ tự chắc chắn sẽ cải thiện mô hình.
- **Phụ thuộc không đồng nghĩa nhận diện trực tiếp:** sơ đồ giả định `E3-X → thành phần Y → độ bền reporter` cũng có thể tạo kết quả mất chức năng/phục hồi như đã cho. Trong phần mềm, tắt dịch vụ A gây thay đổi ở C không chứng minh A gọi trực tiếp C nếu còn B ở giữa. Vì vậy sửa câu V2.4 thành “kết quả ủng hộ E3-X tham gia điều hòa độ bền reporter; chưa xác định cơ chế hay tiếp xúc trực tiếp”. Đây là phản ví dụ logic, không phải cơ chế đã phát hiện trong dữ liệu.

### Cập nhật căn cứ trạng thái khi đọc lại repo trong lượt chấm V2

[D-027](../../../DECISIONS.md#d-027) đã được thêm: khung đóng góp đo/phân rã kèm thành phần kiến trúc mới; đây là quyết định của Trọng, không phải phê duyệt của GVHD. C-13 về thay nhãn chính vẫn chờ xác nhận. Một số tài liệu khác còn ghi chỉ có một việc chặn; phần A của DECISIONS hiện nêu hai. Chỉ ghi nhận để tránh dùng trạng thái cũ khi hỏi bảo vệ đề tài; không thay thiết kế nghiên cứu hay mở thí nghiệm trong phiên học tập này. Những số đo và suy luận mới chưa được audit lại trong hoạt động hỏi đáp.

## Vòng 3 — WT, hiệu ứng đo và giới hạn suy luận

**Trạng thái:** Đã đặt bốn câu, đang chờ trả lời. Các số dưới đây **hoàn toàn giả định để học**, không phải kết quả của đề tài. WT ở đây nghĩa là chuỗi gốc làm mốc so sánh; PSI thấp = kém bền, cao = bền trong thang đang xét.

| Phiên bản | Chuỗi | PSI thực nghiệm giả định |
|---|---|---:|
| Gốc | `MALAKLA` | 1,8 |
| A2V | `MVLAKLA` | 3,2 |
| A4V | `MALVKLA` | 1,9 |

**1.** Phiên bản nào là WT? Tính ΔPSI thực nghiệm của A2V và A4V so với WT. Phiên bản nào được làm bền nhiều hơn so với WT trong ví dụ này?

**2.** Một người đọc kết quả A2V rồi nói: “Đột biến này có 140% xác suất là degron.” Bạn sửa câu đó thế nào để nêu đúng đại lượng, mức thay đổi và giới hạn kết luận? Không chỉ trả lời “vì xác suất không vượt 100%”.

**3.** Mô hình chỉ nhận số lượng từng aa có thể dự đoán ΔPSI của A2V và A4V khác nhau không? Nếu không, vì sao bảng thí nghiệm ở trên vẫn có thể cho hai giá trị khác nhau? Đây là hạn chế của mô hình hay mâu thuẫn của bảng? Giả sử bảng đã đo lặp đủ để tin chênh lệch không chỉ do nhiễu.

**4.** Hãy viết lại câu “E3-X chính là E3 nhận diện degron này” thành một kết luận phù hợp với bằng chứng: mất chức năng E3-X làm reporter sáng hơn, phục hồi E3-X làm giảm sáng. Giải thích ngắn vì sao một thành phần trung gian Y có thể khiến kết luận nhận diện trực tiếp chưa được bảo đảm.

### Câu trả lời nguyên văn và đánh giá V3

Chưa nhận được. Chưa đánh dấu nắm vững; sẽ kiểm tra lại nội dung đã sửa bằng ví dụ khác ở vòng sau.
