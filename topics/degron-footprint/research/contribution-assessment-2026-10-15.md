# Đánh giá trung thực mức đóng góp thực tế của đề tài — 15/10/2026

> **Đồng bộ 21/10/2026 — đọc khối này trước; phần còn lại là bản ghi lịch sử (viết trước G2 ngày 18/10).** Số liệu hiện hành nằm ở khối "Trạng thái 21/10/2026" của [topic-decision.md](topic-decision.md). Những chỗ dưới đây đã lỗi thời:
>
> - **§1, §2, §6 "mô hình thắng baseline chưa tồn tại":** ridge M3 đạt AUROC mức ô **0,8082**, vượt ΔPAP **0,7693** (+0,0389, CI 95% theo cụm [+0,0216; +0,0571]) trên benchmark phát triển OOF 91 peptide / 89 cụm cov80 — [g2-saturation-2026-10-18](g2-saturation-2026-10-18/README.md). Đây chưa phải xác nhận cuối và **G2 chưa hoàn tất**.
> - **§2 "Kiến trúc gần 0" nay được các phép đo củng cố:** cổng + ΔPAP 0,8002, FiLM 0,8028, bilinear 0,7933, cross-ridge 0,7924 đều thua ridge; Degformer huấn luyện lại dưới cov80 là 0,7500 — [g2-extension-2026-10-18](g2-extension-2026-10-18/README.md). Checkpoint Degformer công bố (0,9248) có rò rỉ mức peptide nên không phải holdout sạch.
> - **Các số 0,4270 / 0,4884 / 0,4897 (§2, §6)** là precision@3 trên thang bộ quét; **không so trực tiếp** với AUROC mức ô của G2.
> - **§3.1 "n = 91 không đủ lực":** G2 báo CI bootstrap theo cụm trên 89 cụm; nút thắt "lượng nhãn" vẫn là [DIỄN GIẢI], chưa kiểm trực tiếp (đường cong học còn mở).
> - **§2 hàng Ứng dụng, §4.2 ("bốn tính năng không ai có"; "họ đã có … MetaDegron"):** batch submission không phải điểm khác biệt (MetaDegron, DegronMD đều có). [Audit MetaDegron 21/10](metadegron-analysis-2026-10-21/README.md): đây là công cụ bổ sung motif/E3 (302 dòng nhãn nhị phân, một classifier dùng chung, không có ΔPSI theo phép thay), **không phải đối thủ cùng bài toán**; việc chấm `−ΔScore` của nó trên ma trận G2 **chưa chạy**.
> - **§5, §6 "chưa có mô hình nào…":** tránh dạng tuyệt đối; Degformer đã xuất ma trận 28×20 và Degpred có điểm theo residue. Phần bảo vệ được là nguồn nhãn, cách đánh giá (split cụm, kiểm rò rỉ), baseline mạnh và ứng dụng, trong phạm vi đã đo.
> - Liên kết tới `DECISIONS.md` trỏ vào file đã xoá ở `f03d80d` (xem [CLAUDE.md](../../../CLAUDE.md)); giữ nguyên làm lịch sử.

> **Tài liệu phân tích, không phải quyết định.** Đề nghị đi kèm đã ghi thành
> [C-12](../../../DECISIONS.md) và **chờ Trọng xác nhận**.
>
> Viết sau khi đọc: thẻ đề tài, [DECISIONS.md](../../../DECISIONS.md) phần A/B/C,
> [mạch lập luận 15/10](topic-argument-2026-10-15.md), [báo cáo rủi ro 15/10](larsen-nuclear-and-risks-2026-10-15/README.md),
> [pap-baseline](pap-baseline/README.md). Câu hỏi của Trọng: mức đóng góp **thực tế** theo nhiều khía cạnh,
> và ý nghĩa cho **từng nhóm người dùng** mà đề tài hướng tới.

## Nhãn bằng chứng

**[đo]** tự đo, có file kết quả · **[nguồn]** số của tác giả, đã đọc · **[phân tích]** suy luận ·
**[đề xuất]** chờ xác nhận.

---

## 1. Câu trả lời ngắn

Mức đóng góp thực tế **nếu mọi việc còn lại thành công**: một **công trình kỹ thuật cẩn thận lấp một chỗ
trống đo lường trong một lĩnh vực hẹp**, cộng một ứng dụng có vài tính năng chưa ai có. Đó là một luận văn
Kỹ thuật phần mềm **vững**. Nó **không phải** một đóng góp khoa học mới, và hiện tại **chưa có đóng góp dương
nào tồn tại** — 100% phần tính điểm của [G2](../../../project/course.md) vẫn nằm ở tương lai. **[phân tích]**

Điều quan trọng hơn con số: **đề tài đã dịch chuyển từ "mô hình mới" sang "đo lường cẩn thận" mà chưa tài
liệu nào nói thẳng điều đó.** Ba đợt audit 13–15/10, mỗi đợt đều **lấy đi** một phần tính mới và **thêm vào**
một phần trung thực. Xu hướng đó tốt cho sự trung thực và xấu cho tiêu chí 1. **[phân tích]**

---

## 2. Theo khía cạnh phương pháp

Chấm từng thành phần theo nguyên tắc "cái gì còn lại sau khi trừ hết tiền lệ".

| Thành phần | Mức đóng góp thật | Vì sao |
|---|---|---|
| **Khoảng trống chứng minh được** (89,7% peptide bị ràng buộc) | **Cao về lập luận, bằng 0 về đóng góp** | Tài sản mạnh nhất repo và là lý do chọn đề tài đúng. Nhưng nó chứng minh một *lớp mô hình đã có* không làm được việc — nó **biện minh** cho đề tài, không **là** đề tài. Rubric không cho điểm cho một chứng minh bất khả thi |
| **Kiến trúc** | **Gần 0** | Mọi cơ chế có tiền lệ (BioBlobs, OmniESI, Ilse 2018). Cổng phơi lộ mất vai vì không nhận diện được trên nhãn peptide tách rời ([§4](topic-argument-2026-10-15.md)); Yang 2026 là **tập mẹ** của nó. Degformer đã xuất đúng ma trận 28×20 từ đúng bảng dữ liệu. Chỗ còn trống duy nhất là **MIL vs đầu theo vị trí** — đó là một ablation, không phải một kiến trúc |
| **Benchmark / đo lường** | **Trung bình — và là chỗ thật nhất** | Trần nhãn + baseline trung thực + đối chứng ΔPAP + split cụm + lực: **đã đo xong**, có file, không bài nào trong sáu bài đã đọc có đủ. Nhưng từng món **đều là thực hành chuẩn** trong DMS — LeBlanc 2026 đã đối chiếu trần replicate, split cụm protein là mặc định. Tính mới là **"chưa ai lấp cho nhiệm vụ này"**, không phải **"phương pháp luận mới"** |
| **Phát hiện thực nghiệm** | **Trung bình, nhưng là phát hiện âm** | ΔPAP (0,4270) **thua** baseline thành phần (0,4884), p ≈ 6 × 10⁻¹⁹ **[đo]**; và +0,1311 khi đổi kernel 1 → 7. Cả hai đo **trên mô hình của người khác** ⇒ quan sát, không phải sáng tạo. [D-012](../../../DECISIONS.md#d-012) không nhận kết quả âm làm đóng góp chính |
| **Mô hình thắng baseline** | **Chưa tồn tại — toàn bộ rủi ro nằm đây** | Xem §3 |
| **Ứng dụng** | **Thấp–trung bình, nhưng dễ đạt nhất** | Bốn tính năng không ai có (API, chấm đột biến tuỳ ý qua web, bất định neo vào trần nhãn, xuất xứ nhãn), xác minh từng công cụ **[nguồn]**. Với luận văn **Kỹ thuật phần mềm**, API dễ biện minh nhất. Nhưng đây là đóng góp **công nghệ**, và một tập tính năng không đáp được câu "kiến trúc chưa ai dùng" |

---

## 3. Ba thứ có thể làm sụp phần phương pháp

Cả ba đều **đã biết** và **chưa giải quyết**. **[phân tích]**

1. **n = 91, và đơn vị suy luận còn nhỏ hơn.** MDE ở n = 91 là ≈ 0,071, trong khi phần lớn ablation cho
   0,02–0,05 ⇒ **benchmark không phân biệt được những thứ nó được dựng ra để phân biệt**, tức thất bại ở
   chính chức năng chính của một benchmark. Đơn vị thật là **số cụm protein**, chưa đếm, chắc chắn < 91.
2. **LeBlanc 2026: *"composition is more important than individual positions"*.** Nếu đúng cho tile degron thì
   nhiệm vụ mức residue **mất cơ sở khoa học**, bất kể thước đo hay kiến trúc. Đây là rủi ro nghiêm trọng
   nhất và nó mâu thuẫn trực tiếp với trụ thứ nhất của đề tài.
3. **Nghịch lý trung thực.** Nhãn mức residue lặp ở Jaccard **0,4965**; chỉ 16,0% peptide có tập vị trí dương
   giống nhau giữa hai replicate **[đo]**. Càng trung thực thì công cụ càng phải tự nói "đừng tin danh tính
   residue" — và công cụ nói vậy thì giá trị sử dụng thấp. **Phần mạnh nhất về học thuật cũng là phần làm
   yếu nhất tính hữu dụng.**

---

## 4. Theo nhóm người dùng

Xếp theo **ai thật sự được lợi**, không theo ai được nêu trong đề cương. **[phân tích]**

### 4.1 Nhà nghiên cứu tin sinh học / ML khác — được lợi thật nhất, vẫn chỉ trung bình

Nhận được một chỗ so sánh có trần nhãn, baseline trung thực và split không rò rỉ — đúng thứ lĩnh vực đang
thiếu. Nhưng n = 91 làm benchmark **không đủ lực để xếp hạng phương pháp**, nên giá trị thật là *"một mốc
tham chiếu và một bộ quy ước đánh giá"*, không phải *"một leaderboard"*. Và nhóm này nhỏ.

### 4.2 Nhà sinh học thực nghiệm thiết kế đột biến degron — giá trị thấp hơn vẻ ngoài

Họ **đã có** Degformer (script cục bộ, đúng ma trận 28×20), DegronMD, MetaDegron **[nguồn]**. Cái được thêm
là **bất định, xuất xứ nhãn, cờ ngăn tế bào** — ba thứ trung thực và chưa ai có. Nhưng với Jaccard 0,50 ở
mức residue, lời khuyên trung thực nhất là *"thử 3 residue này, kỳ vọng ~1 trong 3 đúng"*. Có ích hơn đoán
ngẫu nhiên (0,1204) rất nhiều; **không** đủ thay một vòng thí nghiệm ⇒ phải gọi đúng là **công cụ sàng lọc
ưu tiên**, không phải công cụ quyết định.

### 4.3 Người làm thuốc PROTAC / molecular glue — gần như 0 trong phạm vi luận văn

Nhãn là peptide 28-mer gắn đuôi GFP, đo trong **bào tương**. Khoảng cách tới ngữ cảnh điều trị quá xa.
**Đề nghị:** nếu đề cương có nêu nhóm này thì **gỡ hoặc hạ xuống "hướng phát triển"** — đây là chỗ dễ bị bắt
lỗi "thổi phồng ứng dụng" nhất, và [hướng dẫn trình bày §2](../../../project/advisor-presentation-guide.md)
nói thẳng: *"dự đoán trên peptide không tự chứng minh tác động trên protein nguyên vẹn hay hiệu quả điều trị"*.

### 4.4 GVHD và hội đồng — đáp đủ, nhưng lệch chỗ

TC4 (XAI) **đạt tự nhiên** vì đầu ra chính *là* lời giải thích, và fidelity đo được bằng footprint thực
nghiệm — điểm mạnh thật, ít đề tài có. TC5 đạt qua ma trận + API. **TC1 (tính mới) là chỗ hở**, đúng ở chỗ
GVHD đã phát biểu kỳ vọng ngày 11/10. [C-7](../../../DECISIONS.md) lách chỗ hở này bằng cách **thừa nhận**
nó ⇒ câu hỏi với GVHD ([C-5](../../../DECISIONS.md)) không thể trì hoãn.

### 4.5 Trọng — giá trị cao nhất trong danh sách, và không được tính điểm

Repo đã cho: một audit dữ liệu thật, một phép đo lực thật, kinh nghiệm phát hiện oracle rò rỉ trong chính
lập luận của mình, phản xạ gỡ tuyên bố khi tìm ra tiền lệ. Năng lực nghiên cứu thật, nhưng rubric không có ô.

---

## 5. Ba chỗ không đồng ý với tài liệu hiện tại

**[đề xuất]** — đã ghi thành [C-12](../../../DECISIONS.md).

1. **"Việc chặn duy nhất"** (thẻ đề tài; [§7.4](topic-argument-2026-10-15.md)) — **không đúng**. Lực trên
   n = 91 là việc chặn *gần nhất*; rủi ro LeBlanc là việc chặn **nghiêm trọng hơn**, và nó đang nằm ở vị trí
   không tương xứng. Phép kiểm ổn định theo seed/bootstrap nên **lên trước** việc huấn luyện.
2. **Câu đóng góp [§7.1](topic-argument-2026-10-15.md)** vẫn mở bằng *"Chưa có mô hình nào được huấn luyện cho
   nhiệm vụ…"*. Sau Degformer, câu này cần mệnh đề giới hạn **ngay trong câu**: chỗ còn trống là **điều kiện
   đánh giá** (split cụm, trần nhãn, bất định), **không phải nhiệm vụ**.
3. **Tám tuần không khớp sáu việc** nếu mỗi việc đều có khả năng đổi kết luận. Với [D-026](../../../DECISIONS.md#d-026)
   (không có dự phòng), cần **điểm kiểm cứng cuối tuần 10**.

---

## 6. Phát biểu trung thực, dùng được trước hội đồng

> Em chứng minh được lớp mô hình degron hiện có không tách được vị trí; dựng bộ quy ước đánh giá đầu tiên cho
> nhiệm vụ mức residue có trần nhãn và kiểm soát đồng dạng; cho thấy mô hình công bố gần nhất thua một
> baseline thành phần; và xây một mô hình vượt baseline đó cùng một công cụ web có API trả kết quả kèm bất định.

Mức đó tương đương **một bài short paper / workshop tốt**, hoặc một luận văn tốt nghiệp vững. Không phải bài
tạp chí. Và mệnh đề thứ tư — mệnh đề **duy nhất** tính điểm G2 — hiện **chưa có gì**.

---

## 7. Những gì tài liệu này **không** làm

- **Không** quyết định; §5 là đề xuất, đã ghi vào [DECISIONS.md phần C](../../../DECISIONS.md).
- **Không** huấn luyện hay đo thêm bất cứ thứ gì; mọi con số đều trích từ bốn báo cáo đã có.
- **Không** đọc toàn văn LeBlanc 2026, Yang 2026, DegronMD (dựa trên ghi chép của
  [báo cáo 15/10](larsen-nuclear-and-risks-2026-10-15/README.md)).
- **Không** sửa `presentation/`.
