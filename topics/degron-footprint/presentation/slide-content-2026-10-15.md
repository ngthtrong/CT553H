# Nội dung slide trình bày với GVHD — bản viết lại 15/10/2026

> **Đây là nội dung, chưa phải slide.** File này giữ **chữ sẽ lên slide (tiếng Anh)** cùng **ghi chú sản xuất
> (tiếng Việt)** cho từng trang. Chưa dựng HTML/PPTX.
>
> **Căn cứ trạng thái:** [DECISIONS.md](../../../DECISIONS.md) phần A và C. Số liệu trích từ các báo cáo
> trong [research/](../research/), sổ dữ liệu [data/README.md](../data/README.md), và danh mục bài
> [lectures/degron-basics/papers/](../../../lectures/degron-basics/papers/README.md).
> Khuôn trình bày tham khảo [advisor-presentation-guide.md](../../../project/advisor-presentation-guide.md).
>
> **Bản này thay** [session-02-prep.md](session-02-prep.md) và [presentation.html](presentation.html) (cả hai
> là bản 11/10, còn gọi cổng phơi lộ là "Điểm mới 1" — điều [D-028](../../../DECISIONS.md#d-028) mục 1 đã hạ).
> Hai file cũ **chưa xoá**, để đối chiếu.

## Bốn lựa chọn Trọng đã chốt cho bản này (15/10/2026)

| # | Lựa chọn | Hệ quả trong file |
|---|---|---|
| 1 | **Đóng khung bài toán theo hướng C-15**: nhiệm vụ **mức residue** là trụ, cross-assay hạ xuống chương đo lường | Phần 5 (slide 15–17) viết đầy đủ cho mức residue. ✅ **Nay đã là quyết định: [D-031](../../../DECISIONS.md#d-031)** |
| 2 | **15–20 phút, 24 slide** | Phân bổ ở bảng mục lục |
| 3 | **Tiêu đề mô tả nhiệm vụ, không đặt tên mô hình** | Slide 1 |
| 4 | **Độ trung thực "giữ tối thiểu"**: chỉ nêu giới hạn trực tiếp của bài toán và dữ liệu; không nêu các hướng đã bị loại, không nêu tranh luận nội bộ về mức đóng góp | Giải thích cách áp dụng ở mục "Ranh giới của lựa chọn 4" |

### ✅ Cập nhật sau phiên 8 (cùng ngày 15/10/2026) — bản này đã được sửa theo

Bản đầu của file này viết **trước** phiên 8. Phiên 8 đã chạy và **đổi sáu con số** cùng **một phát biểu**;
toàn bộ file đã được sửa theo. Ghi lại để truy vết, vì mấy chỗ này nếu dùng số cũ thì sai:

| Chỗ | Bản đầu (sai hoặc lạc hậu) | Sau phiên 8 — [D-031](../../../DECISIONS.md#d-031) |
|---|---|---|
| Trạng thái C-15 | chờ xác nhận | ✅ **đã chốt thành D-031** |
| Con số dương cho G2 | *chưa có* | ✅ **có: +0,0289** AUROC (ngữ cảnh ±3 so với chỉ-thành-phần), **+0,0300** so với ΔPAP `cnn2w7` ⇒ điều kiện [D-030](../../../DECISIONS.md#d-030) mục 1 **đã đạt** |
| MDE ở n = 91 | 0,071 | **0,0123** — con số cũ suy từ phương sai **không ghép cặp**, thiết kế thật là ghép cặp |
| Số cụm trong n = 91 | "chưa đếm" | **89 cụm** / 91 protein |
| Cỡ mẫu phần mức residue | "n = 91" | **sai** — bộ quét **cũng** là nhãn hiệu ứng đột biến: **2.994 peptide / 1.985 cụm / 83.446 ô** |
| Rủi ro LeBlanc | "chưa giải quyết" | **đã khoanh**: 28,9% → **53,3%** hệ số tách khỏi 0; áp đảo của thành phần 56× → **2,2×** |
| Lý lẽ kiến trúc | "MIL so với đầu theo vị trí, chưa có tiền lệ" | **đổi** sang **giám sát yếu** ([C-17](../../../DECISIONS.md#c-17) mục a) |

⚠ **Một ràng buộc câu chữ mới, bắt buộc — [C-17](../../../DECISIONS.md#c-17) mục b.**
**Không được viết "vị trí thắng thành phần"** ở bất kỳ slide nào. Phân rã của chính phép đo cho thấy cái
mua được hiệu năng là **lân cận cục bộ**, và phần lớn là **thành phần của lân cận**:

| Thành phần của +0,0289 | Giá trị |
|---|---:|
| chỉ số vị trí tuyệt đối, một mình | +0,0052 |
| **thành phần cửa sổ ±3, không thứ tự** | **+0,0232 — 80% của tổng** |
| thêm thứ tự trong cửa sổ | +0,0057 |
| thêm vị trí tuyệt đối lên trên ngữ cảnh | **+0,0002 — bằng 0** |

⇒ Phát biểu đúng: **"composition at a ±3 neighbourhood scale beats composition at whole-peptide scale"**.
Nói "position beats composition" là **sai bản chất phép đo của chính mình**, và GVHD đọc bảng trên sẽ thấy
ngay.

### Ranh giới của lựa chọn 4 ("giữ tối thiểu")

Giữ tối thiểu **không phải** nói sai. Danh sách "đừng nói" ở
[thẻ đề tài](../README.md) và [hub học](../../../lectures/degron-basics/README.md) vẫn áp dụng nguyên vẹn.
Cụ thể trong file này:

| Giữ lại dù chọn "tối thiểu" | Vì sao |
|---|---|
| **Degformer trong bảng tiền lệ (slide 8, 10)** | Nó **đã xuất đúng ma trận 28×20** từ đúng nguồn nhãn. GVHD yêu cầu history research ba bước, nên bỏ nó ra là **thiếu khảo sát**, và nếu GVHD tự tìm ra thì nặng hơn nhiều. Trình bày nó như **tiền lệ có điểm yếu đo được**, không như "đối thủ đã giết đề tài" |
| **Trần nhãn, n = 91, Jaccard 0,4965** (slide 17, 20) | Đây là **giới hạn của dữ liệu và bài toán** — đúng loại mà lựa chọn 4 giữ lại |
| **Nhãn bằng chứng ở chú thích hình** | Bắt buộc theo quy ước repo: phân biệt tự đo, số tác giả, đề xuất |
| **Bỏ ra** | Bốn hướng đã bị loại bằng số (cross-assay, trình tự lạ, ngữ cảnh mức peptide, cổng phơi lộ); đánh giá mức đóng góp ở [contribution-assessment](../research/contribution-assessment-2026-10-15.md); lịch sử các lần đổi hướng |

**Năm câu không được xuất hiện trên slide** (đã bị bác bỏ bằng đo hoặc bằng tra y văn trong repo):

1. ❌ "no tool outputs a 28×20 matrix" — Degformer đã xuất
2. ❌ "MIL is more robust to noisy labels" — Ilse 2018 nói về nhãn **vắng mặt**, không phải nhãn **nhiễu**
3. ❌ "nobody has placed an exposure gate at the pooling step" — Yang et al. 2026 là **tập mẹ**
4. ❌ **"position beats composition"** — xem bảng phân rã ở trên ([C-17](../../../DECISIONS.md#c-17))
5. ❌ mọi dạng "nobody has done X" khi chỉ tra qua tóm tắt — viết *"a PubMed/Europe PMC query run on
   15 Oct 2026 returned no…"*

Và một câu **mới phải bỏ** sau phiên 8: ❌ *"the saturation set is the only source that can support
residue-level claims"* — bộ quét cũng là nhãn hiệu ứng đột biến, và lớn hơn 22 lần
([D-031](../../../DECISIONS.md#d-031) mục 2, sửa [D-028](../../../DECISIONS.md#d-028) mục 5).

---

## Mục lục 24 slide

| # | Phần | Slide | Trạng thái nội dung |
|---|---|---|---|
| 1 | Title | 1 | ✅ đầy đủ |
| 2 | Introduction | 2–6 | ✅ đầy đủ |
| 3 | Related work | 7–11 | ✅ đầy đủ |
| 4 | Gap, urgency, contribution | 12–14 | ✅ đầy đủ — slide 14 nay **có con số dương**, chỉ ô C4 còn mở |
| 5 | Problem definition | 15–17 | ✅ đầy đủ |
| 6 | Datasets | 18–20 | ✅ đầy đủ (một ô cần sinh hình) |
| 7 | Method | 21–22 | **sườn** — mốc và lý lẽ đã có số, kiến trúc chưa chạy |
| 8 | Next steps | 23 | ✅ đầy đủ |
| 9 | Questions | 24 | ✅ đầy đủ |

Ngân sách thời gian 15–20 phút: phần 1–2 ≈ 3 phút · phần 3 ≈ 4 phút · phần 4 ≈ 3 phút ·
phần 5 ≈ 3 phút · phần 6 ≈ 3 phút · phần 7–9 ≈ 3 phút.

---

## Phong cách thiết kế (áp dụng cho cả 24 slide)

**Tone màu tin sinh học, tối giản hiện đại.** Bảng màu đề xuất, dùng nhất quán:

| Vai | Màu | Hex | Dùng ở đâu |
|---|---|---|---|
| Nền | trắng ngà | `#FAFBFC` | nền slide |
| Chữ chính | xanh đen | `#15323F` | tiêu đề, body |
| Nhấn 1 — **degron / bất ổn định** | đỏ san hô | `#D1495B` | vị trí footprint, PSI thấp, degron mạnh |
| Nhấn 2 — **bền / an toàn** | xanh mòng | `#2A9D8F` | PSI cao, không phải degron |
| Nhấn 3 — **mô hình / tính toán** | xanh thép | `#386FA4` | khối workflow, kiến trúc |
| Trung tính | xám xanh | `#8FA3AD` | lưới, trục, nhãn phụ |
| Cảnh báo / chưa đo | hổ phách | `#E9C46A` | ô "not yet measured", nhãn [proposed] |

Quy ước: thang PSI **thấp = bị phân hủy = đỏ**, **cao = bền = xanh mòng** — giữ đúng chiều này ở **mọi**
hình, vì chiều PSI là chỗ đã nhầm một lần trong repo. Mỗi hình có **thang màu** và **nhãn bằng chứng** ở
caption. Font: một font sans (Inter / Source Sans) cho chữ, một font mono (JetBrains Mono) cho trình tự
peptide và tên file. Hình tự dựng ghi `own diagram`; hình của tác giả ghi tên, DOI, giấy phép.

**Hình được phép sao chép:** chỉ **Voutsinos 2026** (CC BY-NC 4.0), 6 hình đã tải ở
[lectures/degron-footprint/assets/figures/](../../../lectures/degron-footprint/assets/figures/NOTICE.md).
Mọi bài khác **chỉ dẫn link, không sao chép hình** — nhất là Zhang 2023 (Elsevier, all rights reserved) và
Larsen 2025 (CC BY-NC-**ND**). Sơ đồ SVG tự dựng có sẵn ở
[lectures/degron-basics/figures/](../../../lectures/degron-basics/figures/) (16 file), dùng lại được.

---

# PHẦN 1 — TITLE

## Slide 1 — Title

**Chữ lên slide:**

> # Residue-Level Prediction of Degron Mutation Effects from Experimental Protein-Stability Data
>
> **Undergraduate thesis proposal · CT553H**
> Software Engineering, College of Information and Communication Technology
> Can Tho University
>
> **Student:** Nguyễn Thế Trọng — B2305615
> **Advisor:** Dr. Hồ Quang Thái
>
> Progress report, week 6 · October 2026

**Ghi chú sản xuất.** Tiêu đề theo khuôn `[bài toán] bằng [nguồn nhãn]` của
[hướng dẫn §2](../../../project/advisor-presentation-guide.md); **chưa đặt tên mô hình** vì kiến trúc chưa
chốt — đặt tên ngắn sau khi có kiến trúc, theo lựa chọn 3 của Trọng. Không dùng chữ "enhanced",
"improved", "novel" ở tiêu đề khi chưa có kết quả so sánh.

**Hình:** nền tối giản — một dải peptide 28 ô mono, vài ô tô đỏ san hô (vị trí footprint), mờ dần về phải.
Không dùng ảnh stock DNA/ống nghiệm.

---

# PHẦN 2 — INTRODUCTION

> **Mạch:** phân tử → tế bào → cơ chế → bệnh lý → bài toán tính toán. Năm slide, mỗi slide **một** ý.
> Theo khuôn [§2 của hướng dẫn](../../../project/advisor-presentation-guide.md): định nghĩa thuật ngữ
> **trước** khi dùng, và ý nghĩa y sinh phải nằm trong phạm vi dữ liệu.

## Slide 2 — Proteins are chains of amino acid residues

**Chữ lên slide:**

> **Proteins do the work of the cell** — catalysis, signalling, structure, transport.
>
> A protein is a **linear chain of amino acids**. Each link in the chain is called a **residue**.
> - 20 standard amino acid types
> - Order of residues is written as a **sequence**: `MKTAYIAKQR…`
> - The sequence determines the 3-D fold, and the fold determines the function
>
> **Two words used throughout this talk:**
> | Term | Meaning |
> |---|---|
> | **Residue** | one position in the chain — "position 7" |
> | **Amino acid type** | what sits at that position — "valine" |
>
> A **mutation** changes the amino acid type at one residue: `M7V` = methionine → valine at position 7.

**Ghi chú sản xuất.** Phân biệt *residue* và *loại acid amin* phải nói ngay ở đây — đây là chỗ hay lẫn, và
cả đề tài đứng trên phân biệt đó (ma trận 28 **vị trí** × 20 **loại**).

**Hình — cần trực quan hoá, không để trang toàn chữ.**
Dùng lại [`fig-01-protein-chain.svg`](../../../lectures/degron-basics/figures/fig-01-protein-chain.svg).
**Animation 3 bước** (bấm chuột từng bước):
1. Chuỗi hạt thẳng, mỗi hạt một chữ cái, đánh số 1…n dưới chân.
2. Chuỗi gập lại thành khối cầu — nhãn "fold".
3. Một hạt đổi màu sang đỏ san hô kèm nhãn `M7V` — nhãn "mutation".

Nếu không làm animation thì ba panel cạnh nhau, có mũi tên. `own diagram`.

## Slide 3 — Protein level is set by a balance: synthesis against degradation

**Chữ lên slide:**

> A protein's concentration in the cell is not set by production alone.
>
> **amount in cell = rate of synthesis − rate of degradation**
>
> Cells destroy proteins on purpose, and constantly:
> - to switch signals **off** on schedule (cell-cycle regulators, transcription factors)
> - to clear **misfolded** or damaged copies before they aggregate
> - to adjust quickly to changed conditions
>
> **Consequence:** a protein that is *made* correctly but *destroyed* too fast is just as absent as one
> that was never made. Degradation is a control layer in its own right.

**Ghi chú sản xuất.** Slide này tồn tại để người nghe hiểu **vì sao độ bền là một đại lượng đáng dự đoán**.
Không có con số nào ở đây — cố ý, vì mọi con số định lượng về độ bền sẽ xuất hiện từ slide 7 trở đi khi đã
giải thích cách đo.

**Hình.** Cân hai đĩa: đĩa trái "synthesis" (mũi tên vào, xanh mòng), đĩa phải "degradation" (mũi tên ra,
đỏ san hô), ở giữa là mức protein. **Animation:** đĩa phải nặng dần → mức protein tụt xuống. `own diagram`.

## Slide 4 — The ubiquitin–proteasome system (UPS) performs targeted degradation

**Chữ lên slide:**

> Selective degradation in eukaryotes runs through the **ubiquitin–proteasome system**.
>
> | Step | What happens |
> |---|---|
> | 1. **Recognition** | an **E3 ubiquitin ligase** binds a specific signal in the target protein |
> | 2. **Tagging** | the E3 transfers chains of **ubiquitin**, a small marker protein, onto the target |
> | 3. **Degradation** | the **26S proteasome** recognises the ubiquitin chain, unfolds the target and cuts it into peptides |
>
> **Scale of the recognition problem:** the human genome encodes **over 600 E3 ligases**, and each one
> recognises its own set of targets. Specificity of the whole system therefore lives in step 1.
>
> <small>Mechanism established in the literature; E3 count as reported in DegronMD, Xu et al., *Mol Biol Evol* 40(12), 2023.</small>

**Ghi chú sản xuất.** Con số "**over 600 E3 ligases**" lấy từ DegronMD (*Mol Biol Evol* 2023,
[DOI 10.1093/molbev/msad253](https://doi.org/10.1093/molbev/msad253)) — bài đó viết "The human genome
encodes over 600 E3 ligases; however, only a small number of targeted degron instances have been identified
so far". Câu thứ hai chính là câu dẫn nhập của đề tài, dùng lại ở slide 13.

**Hình — bắt buộc trực quan hoá.** Dùng lại
[`fig-02-ubiquitin-pathway.svg`](../../../lectures/degron-basics/figures/fig-02-ubiquitin-pathway.svg).
**Animation 3 bước** khớp đúng ba dòng của bảng:
1. E3 (xanh thép) tiến tới và khớp vào một đoạn ngắn trên protein đích — đoạn đó tô đỏ san hô.
2. Ba–bốn hình tròn ubiquitin nhỏ nối thành chuỗi gắn lên protein.
3. Proteasome (hình trụ xám xanh) hút protein vào, nhả ra các đoạn peptide ngắn.

Nếu tìm GIF ngoài: **phải kiểm giấy phép trước** và ghi nguồn. Khuyến nghị tự dựng, vì chỉ cần 3 khung và
giữ được bảng màu.

## Slide 5 — A degron is the recognition signal — and the question is which residues carry it

**Chữ lên slide:**

> A **degron** is the short segment of a protein that an E3 ligase recognises in order to mark it for
> degradation. It is the "address label" of step 1.
>
> - Typically a **short linear motif**, a few to a few tens of residues
> - Can sit at the protein's N-terminus, C-terminus, or **internally**
> - Degron **strength** is graded, not binary: segments range from strong to intermediate to inactive
>
> **The question this thesis asks is one level finer:**
>
> > Within a degron, **which individual residues** determine its strength — and by how much does the
> > strength change when one of them is substituted?
>
> **Scope statement.** Labels in this work are measured on **isolated 28-residue peptides** fused to a
> reporter. Predictions therefore describe peptide-level stability, and do **not** by themselves establish
> an effect on the intact protein or any therapeutic effect.

**Ghi chú sản xuất.** Câu scope statement là yêu cầu cứng của
[hướng dẫn §2](../../../project/advisor-presentation-guide.md) và phải nằm **ngay** ở slide định nghĩa bài
toán, không để xuống phần giới hạn. Gradation "19% strong / 30% intermediate / 51% non-degron" là số của
Voutsinos 2026 — để dành tới slide 10, ở đây chỉ nói "graded".

**Hình — zoom ba tầng, đây là hình quan trọng nhất của phần dẫn nhập.**
Dùng lại [`fig-05-footprint.svg`](../../../lectures/degron-basics/figures/fig-05-footprint.svg).
**Animation zoom liên tục:**
1. Cả protein đã gập (xám xanh), một vùng sáng lên.
2. Zoom vào: đoạn 28 residue dạng ô vuông mono.
3. Zoom tiếp: 3–4 ô tô đỏ san hô đậm = residue quyết định; các ô còn lại nhạt.
4. Hiện câu hỏi "which residues?" cạnh các ô đỏ.

## Slide 6 — Why this matters: mutations that create or destroy degrons cause disease

**Chữ lên slide:**

> Degrons are a **disease mechanism in both directions**.
>
> | Direction | Consequence | Reported in |
> |---|---|---|
> | A mutation **destroys** an existing degron | an oncoprotein escapes degradation and **accumulates** → uncontrolled proliferation | Tokheim et al., *Mol Cell* 2021 · Liu et al., *Nat Commun* 2021 |
> | A mutation **creates** a new degron | a healthy protein is destroyed prematurely → **loss of function** | Voutsinos et al., *Sci Adv* 2026 (PNPO D33V) |
>
> Scale reported across human tumours:
> - **over 19%** of cancer driver genes affect ubiquitin–proteasome function — Tokheim et al. 2021
> - **2,406** degron-exchange events identified in gene fusions, enriched for oncogene stabilisation — Liu et al. 2021
> - **89,318** mutations predicted to disrupt degron function across the pan-cancer degrome — DegronMD, 2023
>
> **And degrons are also a drug-design target:** targeted protein degradation works by *recruiting* the
> degradation machinery to a protein of interest. Knowing which residues control degron strength is
> upstream of that design problem.
>
> <small>Figures as reported by the cited authors; this thesis does not predict disease or claim therapeutic effect.</small>

**Ghi chú sản xuất.** Đây là slide trả lời câu GVHD **nhấn mạnh nhất** ở buổi gặp 1 — *vì sao cần nghiên
cứu* ([biên bản mục 2](../../../project/meetings/2026-10-02-session-01/minutes.md)). Ba con số đều là **số
của tác giả**, nhãn `[nguồn]`, không phải tự đo. Câu cuối (disclaimer) **giữ nguyên**, vì
[contribution-assessment §4.3](../research/contribution-assessment-2026-10-15.md) đã cảnh báo nhóm người dùng
PROTAC là chỗ dễ bị bắt lỗi thổi phồng nhất — nên nói "upstream of that design problem", **không** nói đề
tài phục vụ thiết kế thuốc.

Trích dẫn đầy đủ (dùng cho slide phụ lục references):
- Tokheim C, Wang X, Timms RT, … Elledge SJ, Brown M, Liu XS. *Systematic characterization of mutations
  altering protein degradation in human cancers.* **Mol Cell** 81(6):1292–1308.e11, 2021.
  [DOI 10.1016/j.molcel.2021.01.020](https://doi.org/10.1016/j.molcel.2021.01.020)
- Liu J, Tokheim C, Lee JD, … Pandolfi PP, Wei W. *Genetic fusions favor tumorigenesis through degron loss
  in oncogenes.* **Nat Commun** 12:6704, 2021.
  [DOI 10.1038/s41467-021-26871-y](https://doi.org/10.1038/s41467-021-26871-y)
- Xu H, Hu R, Zhao Z. *DegronMD: Leveraging Evolutionary and Structural Features…* **Mol Biol Evol**
  40(12), 2023. [DOI 10.1093/molbev/msad253](https://doi.org/10.1093/molbev/msad253)

**Hình.** Hai nhánh đối xứng, mũi tên ngược chiều nhau: nhánh trên "degron destroyed → protein accumulates"
(đỏ san hô dần đậm, cột protein cao lên), nhánh dưới "degron created → protein cleared" (xanh mòng, cột
thấp xuống). Ở giữa là protein hoang dã. **Animation:** hai nhánh chạy lần lượt. `own diagram`.

---

# PHẦN 3 — RELATED WORK (HISTORY RESEARCH)

> **Khuôn ba bước GVHD yêu cầu** ([biên bản mục 3](../../../project/meetings/2026-10-02-session-01/minutes.md)):
> phân nhóm theo phương pháp → đánh giá ưu/nhược từng nhóm và từng công trình → đối chiếu với đề tài.
> Slide 7 là slide **điều kiện** để đọc được bảng: phải giải thích cách đo trước khi so sánh nhãn.

## Slide 7 — How degron data is measured: the GPS stability assay

**Chữ lên slide:**

> Every dataset in the next slide comes from one experimental idea, **Global Protein Stability (GPS)**
> profiling, introduced by Koren et al., *Cell* 2018.
>
> | Step | What is done |
> |---|---|
> | 1 | Synthesise a library of short peptides, each **fused to a fluorescent reporter** (GFP) |
> | 2 | Express one peptide per cell, alongside a second, stable reporter as internal control |
> | 3 | Sort cells by the **reporter ratio** using FACS, into stability bins |
> | 4 | Sequence each bin; a peptide's bin distribution gives its stability score |
>
> **The resulting label — Protein Stability Index (PSI):**
> - scale **1 … 6** (6 bins) in the dataset used here
> - **low PSI = degraded quickly = strong degron**
> - high PSI = stable = not a degron
>
> **Mutation effect** is then a difference between two measured constructs:
> **ΔPSI = PSI(mutant) − PSI(wild type)**, so ΔPSI > 0 means the mutation **stabilised** the peptide —
> evidence that the substituted residue was part of a working degron.
>
> <small>Koren I, Timms RT, Kula T, Xu Q, Li MZ, Elledge SJ. *Cell* 173(7):1622–1635.e14, 2018. DOI 10.1016/j.cell.2018.04.028</small>

**Ghi chú sản xuất.** Chiều của PSI và chiều của ΔPSI là **hai chỗ đã nhầm** trong tài liệu học của repo —
in to, tô màu, và giữ đúng chiều này ở mọi hình sau. Nói rõ "in the dataset used here" vì số bin khác nhau
giữa các bài (Zhang 6 bin, Voutsinos 4 bin, Larsen 4 cổng và thang **đảo chiều**).

**Hình — dùng hình của tác giả, có giấy phép.**
[`voutsinos2026-f1.jpg`](../../../lectures/degron-footprint/assets/figures/voutsinos2026-f1.jpg) (Fig. 1),
CC BY-NC 4.0 — caption bắt buộc: *"Voutsinos et al., Sci Adv 2026, Fig. 1. DOI 10.1126/sciadv.adz3483.
CC BY-NC 4.0."*
Hoặc sơ đồ tự dựng [`fig-03-gps-assay.svg`](../../../lectures/degron-basics/figures/fig-03-gps-assay.svg)
nếu muốn giữ bảng màu. **Khuyến nghị:** hình tác giả ở slide này (tăng độ tin cậy, và cho thấy đã đọc bài
gốc), sơ đồ tự dựng cho phần PSI bên phải.

Thêm một **thanh PSI** 1→6 tô gradient đỏ san hô → xanh mòng, đặt cạnh, có nhãn hai đầu. Thanh này tái sử
dụng ở slide 16 và 20.

## Slide 8 — Prior work at a glance

**Chữ lên slide** (bảng chính của phần history research):

> | Work | Year · venue | Method group | Prediction unit | Labels | Output |
> |---|---|---|---|---|---|
> | **Koren et al.** | 2018 · *Cell* | experimental screen | peptide (C-terminal) | GPS, measured | degron catalogue |
> | **Degpred**, Hou et al. | 2022 · *BMC Biol* | BERT sequence model | degron location in protein | curated motifs + E3 interactions | proteome-wide degron map |
> | **Zhang et al.** | 2023 · *Mol Cell* | experimental screen + ML | peptide | GPS + **mutagenesis**, measured | degron fingerprints, DegronID; SVM for PSI |
> | **DegronMD**, Xu et al. | 2023 · *Mol Biol Evol* | pattern + ML knowledgebase | degron location; mutation impact | curated + evolutionary/structural features | degrome map, 89,318 mutations, drug response |
> | **DEGRONOPEDIA**, Szulc et al. | 2024 · *NAR* | database + ML web server | degron motif, terminus stability | curated motifs, structure | annotation, proteolysis simulation |
> | **MetaDegron**, Zheng et al. | 2024 · *Brief Bioinform* | PLM + multimodal features | is this peptide an E3 degron | ~300 curated degrons, 21 E3s | per-E3 degron classification |
> | **Voutsinos et al. (PAP)** | 2026 · *Sci Adv* | experimental map + CNN | 30-aa tile | GPS, measured, >200k tiles | tile degron score |
> | **Larsen et al.** | 2025 · bioRxiv | experimental map | 30-aa tile (TFs) | sort-seq abundance, measured | TF degron map |
> | **Degformer** | 2026 · GitHub, no paper | transformer | peptide (28-mer) | Zhang 2023 tables | PSI; 28×20 ΔPSI matrix |
> | **This thesis** | — | — | **individual residue** | **GPS mutagenesis, measured** | **28×20 ΔPSI matrix + per-position map** |
>
> <small>Evidence level per work recorded in the thesis bibliography; Degformer assessed by reading its full source code, not a publication.</small>

**Ghi chú sản xuất — đây là slide dễ sai tên nhất, dùng đúng danh sách tác giả dưới đây.**

Đã đối chiếu qua PubMed ngày 15/10/2026 (và bioRxiv API cho Larsen). **Trích dẫn chuẩn:**

| Work | Trích dẫn đầy đủ |
|---|---|
| Koren 2018 | Koren I, Timms RT, Kula T, Xu Q, Li MZ, Elledge SJ. *The Eukaryotic Proteome Is Shaped by E3 Ubiquitin Ligases Targeting C-Terminal Degrons.* **Cell** 173(7):1622–1635.e14. [DOI 10.1016/j.cell.2018.04.028](https://doi.org/10.1016/j.cell.2018.04.028) |
| Degpred 2022 | Hou C, Li Y, Wang M, Wu H, Li T. *Systematic prediction of degrons and E3 ubiquitin ligase binding via deep learning.* **BMC Biol** 20(1):162. [DOI 10.1186/s12915-022-01364-6](https://doi.org/10.1186/s12915-022-01364-6) |
| Zhang 2023 | Zhang Z, Sie B, Chang A, Leng Y, Nardone C, Timms RT, Elledge SJ. *Elucidation of E3 ubiquitin ligase specificity through proteome-wide internal degron mapping.* **Mol Cell** 83(18):3377–3392.e6. [DOI 10.1016/j.molcel.2023.08.022](https://doi.org/10.1016/j.molcel.2023.08.022) |
| DegronMD 2023 | Xu H, Hu R, Zhao Z. **Mol Biol Evol** 40(12). [DOI 10.1093/molbev/msad253](https://doi.org/10.1093/molbev/msad253) |
| DEGRONOPEDIA 2024 | Szulc NA, Stefaniak F, Piechota M, Soszyńska A, Piórkowska G, Cappannini A, Bujnicki JM, Maniaci C, Pokrzywa W. *DEGRONOPEDIA: a web server for proteome-wide inspection of degrons.* **Nucleic Acids Res** 52(W1):W221–W232. [DOI 10.1093/nar/gkae238](https://doi.org/10.1093/nar/gkae238) |
| MetaDegron 2024 | Zheng M, Lin S, Chen K, Hu R, Wang L, Zhao Z, Xu H. *MetaDegron: multimodal feature-integrated protein language model for predicting E3 ligase targeted degrons.* **Brief Bioinform** 25(6). [DOI 10.1093/bib/bbae519](https://doi.org/10.1093/bib/bbae519) |
| Voutsinos 2026 | Voutsinos V, Johansson KE, Larsen FB, Grønbæk-Thygesen M, Jonsson N, Holm-Olesen E, Tesei G, Stein A, Fowler DM, Lindorff-Larsen K, Hartmann-Petersen R. *A near-complete map of human cytosolic degrons and their relevance for disease.* **Sci Adv** 12(6):eadz3483. [DOI 10.1126/sciadv.adz3483](https://doi.org/10.1126/sciadv.adz3483) |
| Larsen 2025 | Larsen FB, Voutsinos V, Jonsson N, Johansson KE, Ethelberg FD, Lindorff-Larsen K, Hartmann-Petersen R. *Comprehensive degron mapping in human transcription factors.* **bioRxiv** 2025.05.16.654404. [DOI 10.1101/2025.05.16.654404](https://doi.org/10.1101/2025.05.16.654404) — **preprint, chưa phản biện** |
| Degformer 2026 | Repo GitHub `Alpine2048/Degformer`, Apache-2.0, tạo 24/03/2026. **Không có bài báo** — phải ghi rõ điều này trên slide |

⚠ **Hai điều phải giữ đúng:** (a) Larsen 2025 là **preprint**, ghi nhãn; (b) Degformer **không có bài báo**,
nên viết "GitHub, no publication" ở cột venue — nếu không, bảng sẽ gợi ý sai rằng nó đã được phản biện.

**Hình/layout.** Bảng 10 dòng là nhiều chữ nhưng **ở đây chữ chính là nội dung** — bù bằng:
- tô nền nhạt theo **nhóm phương pháp** (3 nhóm, 3 màu nhạt);
- cột "Prediction unit" vẽ **icon nhỏ** thay chữ: protein (khối), tile/peptide (dải ô), residue (một ô
  đơn tô đỏ) — người nghe thấy ngay rằng chỉ dòng cuối có icon một ô;
- dòng cuối ("This thesis") tô viền đậm, chữ `#15323F` đậm.

**Animation:** hiện 9 dòng trước, dừng, rồi mới hiện dòng "This thesis" — để người nghe tự thấy chỗ trống
ở cột prediction unit trước khi mình nói.

## Slide 9 — Group 1: motif and database tools — broad coverage, curated labels

**Chữ lên slide:**

> **Degpred (2022) · DegronMD (2023) · DEGRONOPEDIA (2024) · MetaDegron (2024)**
>
> **What they achieved**
> - Moved degron identification from a handful of known motifs to **proteome scale**: Degpred predicts
>   degrons directly from sequence; DegronMD reports **18,000+** new degron instances
> - Added the surrounding biology: ubiquitination sites, disordered regions, structural context,
>   E3 assignment — DEGRONOPEDIA also simulates proteolysis to find post-cleavage degrons
> - **Delivered usable web tools**, with batch submission — a genuine strength, and the state of the art
>   for the "where are the degrons in my protein?" question
> - MetaDegron shows a **protein language model** beats earlier feature-based prediction, and covers 21 E3s
>
> **Where they fall short for the question in this thesis**
> | Limitation | Why it matters here |
> |---|---|
> | Labels are **curated motifs**, a few hundred instances; negatives often **random peptides** | measured negatives are much harder than random ones, so reported AUCs are not comparable to a measured-label benchmark |
> | Prediction unit is **a motif or a protein region** | they answer *where is a degron*, not *which residue inside it matters* |
> | Similarity control between train and test **not reported** for the small curated sets | homologous leakage cannot be excluded |
>
> **The gap this group leaves:** these tools locate degrons. None of them is trained on **measured
> mutation effects**, so none ranks residues inside a degron.

**Ghi chú sản xuất.** Mức bằng chứng từng bài khác nhau rất nhiều, và slide **không** được nói quá:
Degpred và ELITE là **[CHƯA KIỂM]** (chỉ tóm tắt), DEGRONOPEDIA và MetaDegron là **[NGUỒN]** (tóm tắt trang
gốc), DegronMD **[NGUỒN]**. Vì vậy ba dòng "where they fall short" phải viết ở mức *"not reported"* /
*"often random peptides"*, **không** viết *"they leak"* hay *"their numbers are wrong"*. Câu về nhãn âm ngẫu
nhiên và AUC 0,87–0,90 của MetaDegron: nói "not comparable", đừng nói "inflated".

Việc phải làm trước khi dùng slide này trong **luận văn** (không chặn buổi gặp): đọc toàn văn Degpred, kiểm
mức xuất ra của nó, kiểm cách chia tập của MetaDegron.

**Hình.** Một trục dọc "resolution of the answer": từ trên xuống — *protein* → *region* → *motif* →
**residue**. Bốn công cụ của nhóm này đặt ở ba mức trên; mức dưới cùng để **trống**, tô hổ phách. Đây là
hình sẽ lặp lại ở slide 10 và 12 với thêm công cụ — **một hình, ba lần dùng**, giúp người nghe thấy chỗ
trống thu hẹp dần. `own diagram`.

## Slide 10 — Group 2: large-scale measured maps and sequence models — the closest prior work

**Chữ lên slide:**

> **Koren 2018 · Zhang 2023 · Voutsinos 2026 (PAP) · Larsen 2025 · Degformer 2026**
>
> **What they achieved — this is where the field's labels come from**
> - **Koren 2018** established GPS peptidome screening: thousands of peptides with degron activity,
>   plus the "C-end rule" E3 adaptors
> - **Zhang 2023** added **mutagenesis** on top of the screen — scanning (one substitution per position)
>   and saturation (all 20 amino acids per position) — and derived mutational fingerprints for 219 degrons;
>   their own SVM predicts peptidome PSI at Pearson **0.8955** (RMSE 0.563) over 260,989 peptides
> - **Voutsinos 2026** produced a near-complete cytosolic map: **>200,000** 30-residue tiles from
>   **>5,000** proteins, 99.7% coverage — **19%** strong degrons, **30%** intermediate, **51%** non-degrons —
>   and trained **PAP**, a two-channel CNN reaching Pearson **0.82 / 0.87** on held-out tiles
> - **Larsen 2025** extended the approach to all **1,626** human transcription factors, with pre-computed
>   PAP / rASA / pLDDT annotation (preprint)
> - **Degformer 2026** is the most direct precedent: a transformer trained on Zhang's tables that
>   **does output a 28×20 ΔPSI matrix**. Self-reported correlations 0.9162–0.9463
>
> **Where they fall short for the residue-level question**
> | Work | Limitation relevant here |
> |---|---|
> | Zhang SVM, PAP, Larsen | prediction unit is the **whole peptide or tile** — one score per segment, so no ranking of residues within it |
> | **PAP specifically** | its internal channel uses `Conv1D(kernel=1)` + global average pooling ⇒ **permutation-invariant**: shuffling residue order leaves its score unchanged (own measurement: Pearson 1.000000) |
> | **Degformer** | random train/test split with **4.09%** identical-sequence leakage; duplicate sequences kept with conflicting labels; prediction head reads the **CLS token** only — the matrix is assembled from 532 forward passes, not from a residue-level head; blind test set absent from the repo, so headline numbers are not reproducible |
>
> <small>PAP architecture and permutation test: own re-implementation from the authors' MIT-licensed code. Degformer: own reading of full source + own leakage measurement on its shipped CSV.</small>

**Ghi chú sản xuất — slide quan trọng nhất của phần 3, và chỗ dễ sai nhất.**

1. **Phải nói Degformer đã xuất ma trận 28×20.** Câu "chưa sản phẩm nào xuất ma trận 28×20" **đã bị bác bỏ**
   và không được xuất hiện ở bất kỳ đâu. Cách trình bày đúng: *nhiệm vụ không còn trống, nhưng **điều kiện
   đánh giá** còn trống* — đó là cầu nối sang slide 12–13.
2. **Nhãn bằng chứng cho con số Degformer:** 0,9162/0,9420/0,9463 là **self-reported**, và repo chỉ có
   `scipy.stats.pearsonr` nên rất có thể là **Pearson**, không phải Spearman. Trên slide ghi
   "self-reported correlations", **không** ghi "ρ".
3. **Phép đo bất biến hoán vị của PAP là tự đo** — đây là một trong hai con số tự đo mạnh nhất của đề tài,
   nên nhãn nguồn phải rõ để GVHD biết đó là việc của sinh viên, không phải trích lại.
4. Larsen 2025: ghi **preprint**. Và **không** nói nó là test trình tự chưa thấy — 1.583/1.626 (97,4%) TF
   của nó đã có trong peptidome GPS, nên nếu dùng thì gọi đúng là **cross-assay / cross-compartment test ở
   mức tile**. Slide này không cần nêu chi tiết đó; chỉ đừng phát biểu sai.

**Hình — hai panel.**
- **Panel trái, dùng hình tác giả:**
  [`voutsinos2026-f4.jpg`](../../../lectures/degron-footprint/assets/figures/voutsinos2026-f4.jpg) (Fig. 4,
  kiến trúc PAP + hai scatter holdout). Caption bắt buộc ghi tác giả, DOI, CC BY-NC 4.0.
- **Panel phải, tự dựng — "the permutation test":** một peptide 28 ô; mũi tên "shuffle"; peptide đã xáo
  trộn; hai hộp điểm số bằng nhau, nối bởi dấu `=` to, kèm `Pearson(original, shuffled) = 1.000000`.
  **Animation:** các ô bay đổi chỗ, điểm số **không đổi** — đây là hình kể được cả lập luận của slide 12
  trong 3 giây. `own diagram`.

## Slide 11 — Group 3: adjacent variant-effect models — different question, strong baselines

**Chữ lên slide:**

> These are **not** competitors on the same task, but they set the bar for any claim about variant effects.
>
> | Work | What it predicts | Relation to this thesis |
> |---|---|---|
> | **AlphaMissense** (2023, *Science*) | is a missense variant **pathogenic** | different question — pathogenicity, no mechanism. This thesis **adds mechanism**, it does not replace it |
> | **Schulze & Lindorff-Larsen** (2026, *eLife*) | effect of substitutions on **cellular abundance**, from 6 VAMP-seq experiments, **31,614** variants | amino-acid substitution matrices conditioned only on **buried vs exposed** already predict abundance well; the authors propose them as a **strong baseline**. rASA alone gives Spearman **0.45** |
> | **LeBlanc et al.** (2026, *Cell Systems*) | activation-domain strength on a tile library; separates **abundance** from **coactivator binding** | not a degron paper, but sets the methodological bar: report **weight stability across seeds/bootstraps**, compare against the **replicate ceiling** (their best model 0.555 vs ceiling 0.568), and split by protein cluster |
>
> **What this group tells us:** any residue-level claim has to be measured against a **simple structural
> baseline** and reported **next to the experimental noise ceiling** — otherwise the number means little.
>
> <small>Schulze & Lindorff-Larsen, eLife 13, DOI 10.7554/eLife.103721 · LeBlanc et al., Cell Systems 17(9):101701, DOI 10.1016/j.cels.2026.101701 — both read in full.</small>

**Ghi chú sản xuất.** Nhóm này có mặt vì nó là nguồn của **hai quy ước đánh giá** đề tài sẽ dùng, và theo
LeBlanc 2026 thì **phải ghi "theo LeBlanc et al. 2026"** khi dùng ba cách làm đó — không trình bày như lựa
chọn riêng của đề tài. Trích dẫn đầy đủ cho phụ lục:

- Schulze TK, Lindorff-Larsen K. *Effects of residue substitutions on the cellular abundance of proteins.*
  **eLife** 13, 2026. [DOI 10.7554/eLife.103721](https://doi.org/10.7554/eLife.103721)
- LeBlanc CJ, Agarwal P, Demaray JE, Hu G, Zintel MA, Lam AWY, Castro Hernandez JE, Staller MV.
  *Interpretable biophysical neural networks of transcriptional activation domains separate roles of
  protein abundance and coactivator binding.* **Cell Syst** 17(9):101701, 2026.
  [DOI 10.1016/j.cels.2026.101701](https://doi.org/10.1016/j.cels.2026.101701)

**Hình.** Ba cột "what is predicted": *pathogenic?* / *how abundant?* / *how strong an activation domain?*,
và cột thứ tư tô đỏ san hô *"which residue controls degradation?"*. Mũi tên từ cột 2 và 3 xuống một hộp
"evaluation conventions we adopt: structural baseline · replicate ceiling · cluster split · seed stability".
`own diagram`.

---

# PHẦN 4 — GAP, URGENCY, CONTRIBUTION

## Slide 12 — The gap is provable, not merely unexplored

**Chữ lên slide:**

> The closest published model for degron strength, **PAP**, cannot answer the residue-level question —
> and this is a **mathematical property of the model class**, not a shortfall in training.
>
> **The argument**
> - PAP's internal channel is `Conv1D(kernel=1)` → `GlobalAveragePooling`, so its score is a function of
>   **amino acid composition only**
> - For such a model, the predicted effect of substituting `a → b` is
>   `Δf(a→b) = f(c − eₐ + e_b) − f(c)` — the right-hand side **contains no position index**
> - Therefore: for any group of substitutions sharing the same amino acid pair, the model must assign
>   **identical** effects, whatever the positions
>
> **How often that breaks the task** — own measurement on the scanning mutagenesis set:
>
> | | Count |
> |---|---:|
> | Peptides with a measured footprint | 2,624 |
> | …of which have a same-substitution-pair group containing **both** a positive and a non-positive position | **2,353 (89.7%)** |
>
> On those peptides a composition-only model is **provably unable** to separate the residues that matter
> from the ones that do not.
>
> **Verification:** 200 exhaustive comparisons, 4,000 rank-bound checks, an explicit rank-2 counterexample,
> and the permutation test on PAP itself — Pearson(original, shuffled) = **1.000000**.
>
> **And the gap now has a price, not only a proof.** Adding local-neighbourhood features to an otherwise
> composition-only model is worth **+0.0289** cell-level AUROC — 95% CI [0.0264, 0.0313], 1,599 protein
> clusters, 2,288 peptides, measured on the scanning mutagenesis set.
>
> <small>Own measurement; scripts and JSON results in the thesis repository.</small>

**Ghi chú sản xuất — đây là tài sản mạnh nhất của đề tài, và là slide nên mở đầu phần lập luận.**
Không đợt audit nào trong bốn đợt 13–15/10 làm yếu trụ này. Nói rõ **"provable"**, và nói rõ đây là **tự đo**
— GVHD cần thấy đâu là việc của sinh viên.

⚠ **Hai con số đừng lẫn:** **89,7%** là trên 2.624 peptide **có footprint**; **68,9%** là tỉ lệ tương ứng
trên **bộ quét** đo ở phiên 8. Slide dùng 89,7% (trụ đã công bố nội bộ từ 12/10); nếu GVHD hỏi về bộ quét
thì đưa 68,9%.

⚠ **Khi nói câu "+0,0289" phải nói kèm** rằng 80% của nó là **thành phần của lân cận ±3**, không phải thứ
tự và không phải vị trí tuyệt đối ([C-17](../../../DECISIONS.md#c-17)). Nếu chỉ nói "+0,0289 nhờ thêm ngữ
cảnh vị trí" thì GVHD sẽ hiểu sai theo đúng hướng mà phép đo đã bác.

Cách nói **đúng mức** ở câu chuyển tiếp: *"PAP is not a bad model — it was trained for a segment-level score.
Using it for residue-level effects is using it outside its design."* Đây là câu dẫn mạnh hơn hẳn việc nói
PAP yếu, và nó dẫn thẳng sang slide 13.

**Hình — bắt buộc trực quan hoá, đây là ý trừu tượng nhất của cả bài.**
Dùng lại [`fig-07-composition-vs-context.svg`](../../../lectures/degron-basics/figures/fig-07-composition-vs-context.svg).
Thiết kế: hai peptide **cùng thành phần acid amin, khác thứ tự**. Bên trái, nhãn thực nghiệm khác nhau
(một ô đỏ ở vị trí 7 / một ô đỏ ở vị trí 19). Bên phải, mô hình composition cho **cùng một điểm** — vẽ hai
đồng hồ đo chỉ đúng một số. **Animation:** đổi chỗ hai residue → nhãn thật thay đổi (đỏ chuyển vị trí) →
kim đồng hồ **không nhích**. Dưới cùng: `89.7% of 2,624 peptides are in this situation`. `own diagram`.

## Slide 13 — Why now, and who needs it

**Chữ lên slide:**

> **Why the question is answerable only now**
> - Measured residue-level labels at scale **did not exist before 2023**: Zhang et al.'s scanning and
>   saturation mutagenesis is the first large set of **measured mutation effects** on degrons
> - The reference map and the baseline model appeared in **2026** (Voutsinos et al.) — so there is now
>   both a benchmark population and a model to beat
> - Yet the recognition problem remains open: **over 600** human E3 ligases, only a small number of
>   degron instances characterised (DegronMD, 2023)
>
> **What is still missing — the opening this thesis targets**
> | Missing piece | Current state |
> |---|---|
> | A model **trained on the residue-level objective** | published degron models are trained on segment scores; applying them per-residue is use outside design |
> | **Evaluation conditions** for residue-level claims | the closest precedent (Degformer) uses a random split with measurable leakage, reports no label ceiling and no per-prediction uncertainty |
> | A **measured noise ceiling** attached to reported numbers | own measurement: cell-level measurement ceilings are **0.9458** (scanning) and **0.9519** (saturation); residue-set agreement between replicates is Jaccard **0.4965** — an honest tool must report both |
> | Knowing **at which scale** the information actually sits | own decomposition: whole-peptide composition → ±3 neighbourhood → order within it → absolute position. Nobody has published this breakdown for degrons |
>
> **Intended users**
> | User | What they get |
> |---|---|
> | **Experimental biologists** designing degron mutations | a **prioritisation tool**: "test these 3 residues first", with calibrated uncertainty |
> | **Bioinformatics / ML researchers** | a reference task with measured ceiling, honest baselines and a homology-controlled split |
> | **Variant interpretation** | a mechanistic complement to pathogenicity scores — *why* a variant destabilises |
>
> <small>Search statement: PubMed and Europe PMC queries run on 15 Oct 2026 returned no degron-prediction tool published in 2025–2026 beyond those listed; of 19 papers citing Larsen 2025 and Voutsinos 2026, none is a residue-level footprint model.</small>

**Ghi chú sản xuất.**
1. **Câu "intended users" đã được chấm lại** ở
   [contribution-assessment §4](../research/contribution-assessment-2026-10-15.md): nhà sinh học thực nghiệm
   phải gọi đúng là **prioritisation tool**, không phải công cụ quyết định — vì Jaccard 0,50 ở mức residue.
   Nhóm PROTAC/molecular glue **đã bị gỡ** khỏi danh sách người dùng theo đúng khuyến nghị ở §4.3; đừng thêm
   lại.
2. **Câu search statement ở chân slide là bắt buộc** và phải viết đúng dạng *"queries run on 15 Oct 2026
   returned no…"*, tuyệt đối **không** viết "nobody has done this".
3. Nếu GVHD hỏi "đã có Degformer rồi thì sao" — câu trả lời chuẩn bị sẵn, **không** cần lên slide:
   *"nhiệm vụ đã có người làm, nhưng chưa ai làm dưới điều kiện đánh giá đứng được: split theo cụm protein,
   trần nhãn, bất định từng dự đoán. Em đo được 4,09% rò rỉ trình tự y hệt trong phép chia của họ."*

**Hình.** Trục thời gian ngang 2018 → 2026, bốn mốc dữ liệu (Koren 2018 · Zhang 2023 · Larsen 2025 ·
Voutsinos 2026) ở trên trục, hai mốc công cụ (DEGRONOPEDIA/MetaDegron 2024 · Degformer 2026) ở dưới trục.
Cuối trục, một ô hổ phách rỗng nhãn "residue-level model + evaluation conditions". **Animation:** các mốc
hiện dần theo năm; ô hổ phách hiện cuối. `own diagram`.

## Slide 14 — Contribution ⟨phần lớn đã đo; một ô còn mở⟩

> ✅ **Cập nhật sau phiên 8.** Bản đầu ghi C3 là "chưa có gì". Nay C3 **đã có con số dương** trên trục ngữ
> cảnh, và chỗ **chưa thắng** cũng đã được đo thành một mục tiêu có số. Chỉ ô C4 còn là kế hoạch.

**Chữ lên slide:**

> **Four contributions — status as of October 2026**
>
> | # | Contribution | Status |
> |---|---|---|
> | **C1** | **Proof that the current model class cannot localise** degron residues — 89.7% of footprint peptides, explicit rank-2 counterexample, permutation test on PAP (Pearson 1.000000) | ✅ **measured** |
> | **C2** | **An evaluation protocol for the residue-level task** — two mutation-effect label sets with distinct roles, measured ceilings (**0.9458** / **0.9519**), honest composition baseline, published-model control, protein-cluster split, and a **pre-computed detection threshold** (MDE **0.0123**) | ✅ **measured** |
> | **C3** | **A decomposition of where the predictive information sits**, and a model that beats the closest published control on the context axis: **+0.0300** over ΔPAP `cnn2w7` (CI [0.0234, 0.0366]) | ✅ **first positive result** |
> | **C4** | **An architecture** closing the remaining gap on the substitution matrix — currently **−0.0420** behind ΔPAP `cnn2w1` (target: beat **0.7693**, ceiling 0.9519) — plus the application | ⬜ **open — this is the work ahead** |
>
> **The decomposition is the part worth stating carefully:**
>
> | Where the information sits | Contribution to the +0.0289 gain |
> |---|---:|
> | whole-peptide composition | *baseline* |
> | **±3 neighbourhood composition** | **+0.0232 — 80% of the gain** |
> | order within that neighbourhood | +0.0057 |
> | absolute position in the peptide | **+0.0002 — nil** |
>
> ⇒ The right question is **not** "composition or position?" but **"composition at which scale?"**
>
> <small>✅ own measurement with result files · ⬜ open. Beating ΔPAP is beating a model used outside its design: no model has been trained for this task — that is the gap claimed here.</small>

**Ghi chú sản xuất.**
- ⚠ **Câu chân slide là bắt buộc.** ΔPAP được huấn luyện cho **độ dồi dào của tile 30-mer**, nên thắng nó
  **không** phải thắng một mô hình huấn luyện cho nhiệm vụ này. Thêm bằng chứng rào này thấp: mốc M0
  chỉ-thành-phần **hoà** ΔPAP `cnn2w7` (+0,0008, CI [−0,0057; 0,0074]). Nếu không nói, câu "+0,0300" bị
  đọc quá mạnh.
- **Bảng phân rã là chỗ mạnh nhất của slide này** và là chỗ thể hiện tính trung thực: nó **tự hạ** cách nói
  "vị trí thắng thành phần" mà chính repo từng dùng. Đây là loại trình bày
  [hướng dẫn §5](../../../project/advisor-presentation-guide.md) khuyến khích.
- **Chỗ còn phải điền:** ô C4 — kiến trúc + delta đo được + độ bất định; và nếu GVHD chấp nhận khung ở
  [C-5](../../../DECISIONS.md) thì thêm một dòng ghi nhận.
- Mốc đã khoá, **đừng đổi khi chưa có quyết định mới**: **0,7693** (AUROC mức ô của ΔPAP `cnn2w1` trên bộ
  bão hòa — tái lập mốc 0,7692 ngày 14/10), trần **0,9519**, ngưỡng phát hiện **0,0123**.

**Hình.** Bốn ô xếp hàng: ba ô đầu tô đầy (xanh mòng, dấu ✓), ô C4 viền nét đứt hổ phách. Dưới đó, bảng phân
rã vẽ thành **thanh xếp chồng ngang** dài đúng tỉ lệ: đoạn `±3 composition` dài 80%, `order` ngắn, `absolute
position` gần như không thấy — hình này **tự nói** thông điệp mà không cần đọc số. `own diagram`.

---

# PHẦN 5 — PROBLEM DEFINITION

## Slide 15 — Input, output, label

**Chữ lên slide:**

> **Task.** Given a degron peptide, predict the effect of every possible single substitution on its
> stability, at residue resolution.
>
> | | |
> |---|---|
> | **Input** | a **28-residue peptide** sequence (optionally its structural context: rASA, pLDDT) |
> | **Output 1** | a **28 × 20 matrix** of predicted ΔPSI — one value per (position, amino acid type) |
> | **Output 2** | a **per-position importance map** — the 19 substitutions at each position aggregated |
> | **Label** | **ΔPSI = PSI(substituted) − PSI(wild type)**, both **measured** in the GPS assay |
> | **Label sign** | ΔPSI **> 0** ⇒ the substitution **stabilised** the peptide ⇒ that residue was part of a working degron |
> | **Unit of inference** | the **protein cluster** (MMseqs2, ≥30% identity, 80% coverage) — not the peptide, and not the residue |
>
> **Two framings of the same output, both reported**
> - **cell-level**: is this one (position, amino acid) substitution stabilising? → **AUROC**
> - **position-level**: which positions carry the degron? → **precision@3**
>
> **Scope.** Peptides are measured in isolation, fused to a reporter, in the cytosol. Results describe
> that system. Transfer to intact proteins is a separate question with its own labels.

**Ghi chú sản xuất.**
- **"Unit of inference is the protein cluster"** là điểm phương pháp phải nói sớm. Nhưng sau phiên 8 thì
  **mức phạt đã đo được và nó nhỏ hơn lo ngại**: thư viện bão hòa chọn **mỗi protein một peptide**, nên
  91 peptide nằm trên 91 protein / **89 cụm** ⇒ lồng nhau ở mức protein gần như không tồn tại. Phạt thật
  nằm ở **ô lồng trong peptide**: ICC 0,0625, cỡ cụm trung bình 526 ⇒ hệ số thiết kế **33,79**, tức
  ≈ **1.416 ô độc lập hiệu dụng** (không phải 47.847, và cũng **không phải** 91). Con số "dương giả trên
  45%" của phiên trước là cảnh báo chung từ y văn, **không** phải phép đo trên dữ liệu này — đừng trích nó
  như số của đề tài.
- **Hai thước đo, hai vai** theo [D-028](../../../DECISIONS.md#d-028) mục 2: thước đo chính của ma trận là
  **AUROC mức ô** (trần 0,9519), **không** phải Spearman (trần chỉ 0,6989). Đừng đảo lại.

**Hình — bắt buộc, và đây là hình "đầu vào/đầu ra" mà hướng dẫn §3 đòi.**
Dùng lại [`fig-06-input-output.svg`](../../../lectures/degron-basics/figures/fig-06-input-output.svg).
Bố cục ngang ba khối: **[peptide 28 ô, mono]** → **[model, xanh thép, hộp mờ nhãn `architecture: see slide 21`]**
→ **[ma trận 28×20 heatmap + thanh bar per-position]**. Thang màu ΔPSI: âm = đỏ san hô, 0 = trắng ngà,
dương = xanh mòng, có colorbar ghi số.

## Slide 16 — One worked example

> ⚠ **Ô dữ liệu của slide này cần sinh từ dữ liệu trước khi dựng.** Dữ liệu đã nằm trên máy
> (`data/processed/psi-sat_a.tsv`, `psi-sat_b.tsv`) nhưng **chưa có script xuất hình ví dụ**. Đừng đặt số
> minh họa vào chỗ này. Việc cần làm: viết một script nhỏ trong `research/` chọn một peptide **trong tập
> train** (không phải test), xuất ma trận 28×20 từ nhãn đo được trung bình hai replicate, kèm SHA của file
> đầu vào.

**Chữ lên slide (khung, số liệu điền sau):**

> **A single degron peptide, as the data actually sees it**
>
> - Peptide ID: `⟨ACCESSION⟩_⟨GENE⟩_⟨tile⟩` — ⟨28-residue sequence, mono font⟩
> - Wild-type PSI: **⟨value⟩** (low ⇒ this peptide is a degron)
> - Measured matrix: **28 positions × 20 amino acids**, averaged over two replicates
>
> **Reading one cell:** substituting position ⟨p⟩ to ⟨aa⟩ gives ΔPSI = **⟨value⟩** ⇒ the peptide became
> ⟨more / less⟩ stable ⇒ that residue ⟨is / is not⟩ part of the working degron.
>
> **Reading a column:** positions where *most* substitutions stabilise are the degron's **footprint** —
> these are the residues the E3 ligase depends on.
>
> <small>Own rebuild from Zhang et al. 2023 raw counts; PSI reconstruction validated against the authors' own table to a maximum deviation of 5.0 × 10⁻⁷ over 261,865 values.</small>

**Ghi chú sản xuất.**
- **Con số kiểm 5,0 × 10⁻⁷ là tài sản trình bày mạnh** — nó chứng minh pipeline dựng lại nhãn từ read thô
  là đúng, và nó **đã đo** (`research/full-data-audit/psi-build.json`). Giữ ở chân slide.
- ⚠ **Không dùng ví dụ `M7V ΔPSI = +1,4`** đã xuất hiện trong
  [hồ sơ học tập](../learning/assessment-log.md) — đó là **ví dụ số giả định** dùng để dạy, không phải phép
  đo. Mọi số trên slide phải sinh từ file dữ liệu.
- Chọn peptide ví dụ **trong tập train**, và nói rõ điều đó — tránh việc minh họa bằng mẫu test.

**Hình.** Heatmap 28×20 thật, trục x = 20 loại acid amin (nhóm theo tính chất: hydrophobic / polar /
charged / special, có vạch phân nhóm), trục y = 28 vị trí. Ô đồng nghĩa (WT nội tại) viền đen. Bên phải,
bar chart per-position. **Animation:** (1) hiện heatmap; (2) khoanh **một ô** + hiện số; (3) khoanh **một
hàng** + hiện bar tương ứng. Đi từ một ô đến cả hàng là cách giải thích hai tầng đầu ra nhanh nhất.

## Slide 17 — Feasibility: what the data permits, and what it does not

**Chữ lên slide:**

> **Measured benchmark constants — cell-level AUROC, own measurements, all with result files**
>
> | | Scanning set | Saturation matrix |
> |---|---:|---:|
> | Clusters / peptides / cells | 1,985 / 2,994 / 83,446 | 89 / 91 / 47,847 |
> | ΔPAP `cnn2w1` (published control) | 0.7943 | **0.7693** |
> | ΔPAP `cnn2w7` | 0.8357 | — |
> | **M0 — composition only** | 0.8393 | 0.7071 |
> | **M3 — ±3 neighbourhood context** | **0.8682** | 0.7273 |
> | **Measurement ceiling** | **0.9458** | **0.9519** |
>
> **Where the model is ahead** — paired by peptide, bootstrapped by cluster:
> - M3 − M0 = **+0.0289**, CI [0.0264, 0.0313], wins on 72.5% of peptides
> - M3 − ΔPAP `cnn2w7` = **+0.0300**, CI [0.0234, 0.0366]
>
> **Where it is still behind — and this is the stated target:**
> - on the substitution matrix, M3 − ΔPAP `cnn2w1` = **−0.0420**, CI [−0.0580, −0.0256]
> - **but the ranking reverses by metric**: at position level M3 gives Spearman **0.4440** against ΔPAP's
>   **0.3553** ⇒ claims are reported **per metric**, never pooled
>
> **Statistical power, computed in advance**
> | Quantity | Value |
> |---|---:|
> | Minimum detectable difference, saturation set (paired, bootstrap by cluster, 80% power) | **0.0123** |
> | …unpaired equivalent | 0.0491 |
> | …scanning set | **0.0025 – 0.0036** |
> | Power at the measured delta | **0.995** |
> | Cell-within-peptide ICC / design effect | 0.0625 / **33.79** ⇒ ≈ **1,416** effective independent cells |
>
> **Committed in advance:** an ablation worth **≥ 0.012** is detectable on the saturation set; anything
> below that is **not**, and will be reported as indistinguishable rather than as a win.
>
> **Remaining limits of the labels**
> | Limit | Number | Consequence |
> |---|---:|---|
> | Residue-set agreement between replicates (Jaccard) | **0.4965** | report uncertainty, not one confident answer |
> | Measurement noise is **not** fixable by read-depth filtering | — | consistent with DiMSum (*Genome Biol* 2020): a read-independent variance term remains; the remedy is more replicates |
>
> <small>All values: own measurements, scripts and JSON in the repository. These are <strong>measurement</strong> ceilings — an upper bound on what the labels can score, not a promise of achievable performance.</small>

**Ghi chú sản xuất — đây là slide trung thực nhất, và theo lựa chọn 4 nó được giữ vì toàn bộ là giới hạn
của bài toán và dữ liệu.**

1. ⚠ **Câu chân slide về "measurement ceiling ≠ achievable performance" là bắt buộc.** Đây là đúng loại lỗi
   đã mắc **hai lần** trong repo (D-025 mục 1, rồi lặp lại ở phiên 7). Không viết "headroom to the ceiling"
   ở bất kỳ đâu như thể trần là mức đạt được.
2. ⚠ **Không dùng 0,6045 và 0,7792** — hai số đó là **oracle đọc nhãn test**, đã bị D-025 loại.
3. ⚠ **Slide này đã đổi thước đo chính so với bản đầu.** Bản đầu dựng quanh **precision@3** (0,4270 /
   0,4897 / 0,6514). Thước đo chính nay là **AUROC mức ô** theo [D-028](../../../DECISIONS.md#d-028) mục 2,
   và phiên 8 đo mọi mô hình trên thang đó. Bộ số precision@3 vẫn đúng và vẫn dùng được làm **thước đo phụ**
   — để ở phụ lục A2, đừng trộn hai thang trên cùng một bảng.
4. **Dòng "committed in advance" là điểm mạnh trình bày.** Nói ngưỡng 0,012 **trước** khi chạy ablation thì
   mạnh; nói sau khi ablation không có ý nghĩa thì thành biện hộ. MDE cũ 0,071 **đã sai** — nó suy từ phương
   sai không ghép cặp; thiết kế thật là ghép cặp theo peptide.
5. **Dòng "ranking reverses by metric" phải giữ.** Đây là chỗ dễ bị hỏi nhất, và tự nêu thì mạnh: cùng một
   mô hình thắng ở thang mức vị trí và thua ở thang mức ô. Nó cũng là lý do
   [D-028](../../../DECISIONS.md#d-028) mục 2 khoá **một** thước đo chính.

**Hình.** Một **thang dọc 0,70 → 0,96** (không phải 0 → 1, vì mọi số nằm trong dải hẹp này), hai cột cạnh
nhau cho hai bộ nhãn:
- cột *scanning*: ΔPAP `cnn2w1` 0,7943 · ΔPAP `cnn2w7` 0,8357 · M0 0,8393 · **M3 0,8682** · trần 0,9458
- cột *saturation*: M0 0,7071 · M3 0,7273 · **ΔPAP `cnn2w1` 0,7693** (đỏ san hô — "the bar still to clear") · trần 0,9519

Trần vẽ **nét đứt đen** có nhãn `measurement ceiling`. **Animation:** cột trái hiện trước (M3 vượt lên trên
ΔPAP — thắng), rồi cột phải (M3 **nằm dưới** ΔPAP — chưa thắng), rồi hiện mũi tên khoảng cách −0,0420 nhãn
`target`. Hai cột cạnh nhau kể được cả câu "thắng ở đây, chưa thắng ở kia" mà không cần nói. `own diagram`.

---

# PHẦN 6 — DATASETS

## Slide 18 — Data sources: all downloaded, all licence-checked

**Chữ lên slide:**

> **≈ 1.9 GB on disk, four primary sources, every file checksummed**
>
> | # | Source | Identifier pinned | Licence | Role in the thesis |
> |---|---|---|---|---|
> | 1 | **Zhang et al. 2023** — scanning + saturation mutagenesis | Mendeley Data `10.17632/32h94v2yv2.2` (v2), all 5 files | **CC BY 4.0** | **primary labels** — measured mutation effects |
> | 2 | **Zhang et al. 2023** — GPS peptidome PSI table | NCBI GEO `GSE240610` | GEO terms | peptide-level context, author SVM comparison |
> | 3 | **Voutsinos et al. 2026** — cytosolic tile library + PAP model | GitHub `KULL-Centre/_2025_Voutsinos_degron_cytosol` @ `9b3eafa6` | **MIT** (code + data in repo) | **baseline model** + benchmark population |
> | 4 | **MaveDB** — 26 score sets, 9 genes | API, URNs recorded | **CC0** | intact-protein transfer check |
> | 5 | **Larsen et al. 2025** — transcription-factor tile library | GitHub `KULL-Centre/_2025_Larsen_…` @ tag `v1.0` | **MIT** (data file) | cross-assay / cross-compartment test at tile level |
> | 6 | UniProtKB/Swiss-Prot human, release **2026_03** · AlphaFold DB **v6**, 8 structures | REST, snapshot pinned | CC BY 4.0 | wild-type sequences; structural context |
>
> **Integrity:** SHA-256 recorded for every file; the Mendeley set **matches the publisher's published
> checksums**. Download dates, pinned revisions, per-file provenance and a reprocessing log are kept in a
> data provenance file in the repository.
>
> <small>Licences verified per source on 13–15 Oct 2026. Paper licence and data licence can differ: Larsen et al. is CC BY-NC-ND as a preprint, while its tile-level data file is MIT in the authors' GitHub repository.</small>

**Ghi chú sản xuất.**
- **Câu cuối về "paper licence ≠ data licence" nên giữ** — nó cho thấy mức cẩn thận về giấy phép, và là một
  điểm mạnh thật của repo.
- ⚠ **Giấy phép Larsen còn một chỗ mơ hồ chưa đóng:** MIT nominally là giấy phép phần mềm; Trọng **đã gửi
  email** xin xác nhận MIT phủ cả file dữ liệu ([D-030](../../../DECISIONS.md#d-030) mục 2) và **đang chờ
  trả lời**. Nếu GVHD hỏi, trả lời đúng trạng thái đó. **Không** đưa chỗ mơ hồ này lên slide (theo lựa chọn
  4), nhưng phải biết để trả lời.
- Nguồn 5 là **mức tile, trình tự hoang dã, không có nhãn mức residue nào** — nên vai của nó là test chuyển
  assay, **không** phải nguồn nhãn residue. Đừng để bảng gợi ý sai.

**Hình.** Bản đồ dữ liệu dạng khối: 6 hộp nguồn (icon + logo chữ), mỗi hộp có **nhãn giấy phép** như một
chip màu (CC BY 4.0 / MIT / CC0 / GEO), mũi tên vào một hộp chung `data/raw/` kèm `SHA-256 ✓`. Dùng lại
[`fig-16-data-map.svg`](../../../lectures/degron-basics/figures/fig-16-data-map.svg). `own diagram`.

## Slide 19 — From raw reads to labels: pipeline and validation gate

**Chữ lên slide:**

> **Three tiers, every derived file regenerable from a script**
>
> `raw/` (never edited, checksummed) → `interim/` (unpacked, clustering) → `processed/` (script output)
>
> **The rebuild — labels are reconstructed from raw counts, not taken on trust**
> | Step | What was done |
> |---|---|
> | 1 | Read per-bin raw counts: one file per bin per condition, 6 bins |
> | 2 | Normalise: `nbᵢ = bᵢ × factorᵢ`, factors computed per condition with bin 1 as reference |
> | 3 | Compute `PSI = Σᵢ i × nbᵢ / Σᵢ nbᵢ` for every construct |
> | 4 | **Validation gate**: compare the rebuilt Replicate-1 PSI against the authors' own table |
>
> **Gate result: maximum deviation 5.0 × 10⁻⁷ across 261,865 values** ⇒ the reconstruction is correct, and
> the same code can therefore build the conditions the authors did **not** publish PSI tables for.
>
> **Why that matters:** the authors released a PSI table only for Replicate 1. Rebuilding from counts
> yields **all five conditions** — including the second replicate, which is what makes a measured noise
> ceiling computable at all.
>
> **Also found and corrected:** three constructs mis-scored in the authors' released table due to a header
> error — two with `Sum = 0 / PSI = NA` despite having reads, one with PSI off by 0.62.
>
> <small>Own measurement. Rebuild command, per-condition normalisation factors and the validation JSON are in the repository.</small>

**Ghi chú sản xuất.** Slide này trả lời câu hỏi *"em đã làm gì với dữ liệu"* bằng một con số kiểm được —
đúng loại bằng chứng GVHD nhóm bài hay đưa. Ba dòng bị sai trong bảng tác giả là chi tiết nhỏ nhưng **đáng
nêu**: nó chứng minh đã đọc dữ liệu đến mức từng dòng.

**Hình — phễu dữ liệu, đây là hình "data funnel" hướng dẫn §3 đòi.**
Phễu dọc với số đếm ở mỗi tầng:
`raw counts (6 bins × 5 conditions)` → `PSI built: 261,868 / 261,999 / 264,036 / 134,608 / 134,563 ids` →
`scanning peptides 8,831` → `degrons (PSI_WT ≤ 3.0) 3,439` → `with footprint 2,624` →
`saturation matrices 235` → `degron matrices (PSI_WT ≤ 3.0) 91`.
Bên cạnh mỗi mũi tên ghi **tiêu chí lọc**. Cổng kiểm vẽ như một **dấu ✓ xanh mòng** chen giữa tầng 1 và 2,
có nhãn `max dev 5.0 × 10⁻⁷`. **Animation:** phễu hẹp dần theo từng bước — người nghe thấy ngay 91 đến từ
đâu, và đó là cách trung thực nhất để giới thiệu con số nhỏ đó. `own diagram`.

## Slide 20 — The resulting dataset: fields, samples, split

**Chữ lên slide:**

> **Two mutation-effect label sets, two distinct roles** — they are complementary, not interchangeable
>
> | | **Scanning set** | **Saturation set** |
> |---|---|---|
> | Design | **one** substitution per position, almost all **→R** (20 distinct WT→mut pairs) | all **20** amino acids at each of 28 positions — a full matrix |
> | Raw size | ≈ 262,000 constructs × 2 replicates, 9,590 peptides | 134,608 / 134,563 constructs, 249 peptides |
> | Degron peptides (PSI_WT ≤ 3.0) | **2,994** | **91** |
> | **Protein clusters** | **1,985** | **89** |
> | Scored cells | **83,446** | **47,847** |
> | Measurement ceiling (cell-level AUROC) | **0.9458** | **0.9519** |
> | Replicate agreement | residue-set Jaccard **0.4965** | PSI **0.9544**, ΔPSI **0.8335**; noise **16.7%** of variance |
> | **Role** | **sample size and the context axis** | **the 19-substitution matrix**, and confirmation of transfer across label sources |
>
> **Design consequence:** learn the context axis on the **scanning** set, confirm the matrix on the
> **saturation** set. **61 of 89** saturation clusters also occur in the scanning set, so overlapping
> clusters are **removed from training** for every cross-source evaluation.
>
> **Record format** (`processed/psi-*.tsv`, one row per construct)
>
> | Field | Type | Meaning |
> |---|---|---|
> | `id` | string | `⟨ACCESSION⟩_⟨GENE⟩_⟨tile⟩_mut⟨pos⟩⟨aa⟩` — e.g. `A2RUQ5_C17orf102_2_mut10a` |
> | `psi` | float, 1…6 | Protein Stability Index — **low = degraded = strong degron** |
> | `sum` | float | normalised read depth, used for filtering (scanning: `sum ≥ 10`) |
> | `nb1…nb6` | float | normalised reads in stability bins 1…6 |
>
> **Identifier decoding:** accession → wild-type sequence; `tile n` starts at residue `(n−1)×23 + 1`,
> length 28; `mut10a` = position 10 substituted to alanine. Tile rule verified on **128/130** peptides with
> known sequence; the 2 mismatches are excluded.
>
> **Split design**
> - by **protein cluster**, MMseqs2, ≥30% identity, 80% coverage — **5,088 clusters** over 6,573 proteins
> - labels are the **mean of two replicates**; every results table reports the **label ceiling** alongside
> - **130** peptides appear in both sets ⇒ forced to the same side of the split
> - the BAG6-WT condition is a **different condition**, not a third replicate ⇒ never pooled
>
> <small>Own counts and own measurements throughout. Cluster-level, not peptide-level, is the unit of inference: ignoring nesting inflates false positives above 45% at a nominal 5% level.</small>

**Ghi chú sản xuất.**
- ⚠ **Bảng này đã sửa sau phiên 8 và là chỗ sai nặng nhất của bản đầu.** [D-028](../../../DECISIONS.md#d-028)
  mục 5 từng nói bộ bão hòa là nguồn **duy nhất** đỡ được mức residue; [D-031](../../../DECISIONS.md#d-031)
  mục 2 **sửa**: bộ quét **cũng** là nhãn hiệu ứng đột biến, và lớn hơn — **1.985 cụm so với 89**. Hệ quả
  câu chữ: **bỏ** câu "n = 91 là cỡ mẫu của phần mức residue"; n = 91 chỉ là cỡ mẫu của **phần ma trận 19
  thay thế**.
- Nhãn mức **tile** (Voutsinos, Larsen) thì vẫn **không** đỡ được tuyên bố mức residue — đó là phần của
  D-028 mục 5 **vẫn đúng**. Đừng lẫn hai việc: *tile không đỡ được*, nhưng *bộ quét thì đỡ được*.
- Bộ bão hòa **không có phép đo hoang dã riêng**: ô đồng nghĩa (đổi codon, giữ protein) làm **WT nội tại**,
  28 ô mỗi peptide, SD PSI trong peptide trung vị 0,0576. Nếu GVHD hỏi "lấy WT ở đâu" thì đây là câu trả lời.
- `*` ở cuối trình tự (813 peptide 27 aa, tile chạm đầu C) **phải được mask**, không đưa vào embedding như
  token thứ 21 — đó là một trong những điểm yếu đã đo được của Degformer.

**Hình.** Hai cột so sánh (saturation | scanning) với **icon thiết kế thí nghiệm**: bên trái lưới 28×20 đầy
ô, bên phải 28 ô mỗi ô một dấu. Dưới cùng là **ba dòng dữ liệu mẫu thật** ở font mono (lấy từ file, không
tự bịa), bôi màu từng trường khớp với bảng field. Bên cạnh, sơ đồ split: các chấm peptide nhóm thành cụm
protein, đường cắt train/test **đi quanh cụm, không cắt qua cụm** — và 130 chấm hai màu nằm **cùng phía**.
`own diagram`.

---

# PHẦN 7 — METHOD ⟨SKELETON⟩

> ⚠ **Cả hai slide của phần này là sườn**, nhưng **lý lẽ đã đổi sau phiên 8**. Theo
> [D-027](../../../DECISIONS.md#d-027) đề tài **vẫn phải có một kiến trúc mới**. Cách đặt cũ — *"MIL so với
> đầu theo vị trí, chưa tìm thấy tiền lệ"* — **đã bị chính tra y văn của repo hạ**
> ([C-17](../../../DECISIONS.md#c-17) mục a): mô típ chuẩn trong y văn là **đầu theo residue khi có nhãn mức
> residue, MIL khi chỉ có nhãn mức túi**, nên đặt MIL làm tính mới là **yếu** — với nhãn mức ô đã có, đầu
> theo vị trí mới là lựa chọn tự nhiên.
>
> **Lý lẽ thay thế, có số đỡ: giám sát yếu (weak supervision).**
>
> | Thang nhãn | Cỡ | Nhận diện được tham số vị trí? |
> |---|---:|---|
> | mức peptide / tile (GPS 260k, tile 212k) | **rất lớn** | **Không** — 28,9% hệ số tách khỏi 0 |
> | hiệu ứng đột biến, bộ quét | 83.446 ô / 1.985 cụm | **Có** — 53,3% |
> | hiệu ứng đột biến, ma trận bão hòa | 47.847 ô / **89 cụm** | cặp thay thế **có** (92,5%); ngữ cảnh **yếu** (25%) |
>
> ⇒ Câu hỏi kiến trúc đúng: **nhãn mức túi dồi dào có moi được thông tin mức residue qua một cầu nối
> MIL/attention hay không, và có thắng được đầu theo vị trí huấn luyện trên nhãn mức ô ít hơn?** Đây là
> đúng chỗ MIL sinh ra để dùng, và **câu trả lời âm cũng là kết quả dùng được**.

## Slide 21 — Proposed approach ⟨SKELETON⟩

**Chữ lên slide (bản sườn):**

> **What is already fixed and measured** ✅
> | Element | Decision |
> |---|---|
> | Task | residue-level mutation effect; 28×20 matrix + per-position map |
> | Labels | measured ΔPSI, mean of two replicates; **two sets, two roles** (slide 20) |
> | Primary metric | **cell-level AUROC** — ceilings **0.9458** / **0.9519**; secondary: position-level Spearman, precision@3 |
> | Split | protein cluster, MMseqs2 ≥30% id / 80% cov; overlapping clusters removed for cross-source tests |
> | Baselines established | composition-only **0.8393** · ΔPAP `cnn2w1` **0.7943** · ΔPAP `cnn2w7` **0.8357** · best current model **0.8682** |
> | Detection threshold | **0.0123** (saturation) · **0.0025–0.0036** (scanning), computed in advance |
> | Where the information sits | ±3 neighbourhood composition (80% of the gain); absolute position ≈ 0 |
>
> **What is open — the architecture** ⬜ `[proposed, not yet validated]`
>
> **The target is a number, not a sentence:** beat **0.7693** cell-level AUROC on the substitution matrix,
> where the current model is **0.0420** behind, with a measurement ceiling of 0.9519.
>
> The design question is **whether abundant bag-level labels can be mined for residue-level output**:
>
> | Variant | Idea | Status |
> |---|---|---|
> | **A** | **per-position head** trained on cell-level labels — the standard choice, and the one to beat | to be run |
> | **B** | **attention-MIL bridge** — peptide as bag, ±3 windows as instances, pre-trained on the large bag-level sets (260k peptides / 212k tiles) | to be run |
> | **C** | **hybrid** — bag loss + cell loss with weight λ | to be run |
>
> All variants share window size, loss, budget, seeds and split, and are scored on **both** a bag-level and
> an instance-localisation metric.
>
> **Novelty stated at the level the evidence supports.** The open question is one of **weak supervision**:
> the bag-level labels are abundant but, as measured here, do **not** identify positional parameters
> (28.9% of coefficients separable from zero); the cell-level labels identify them (53.3%) but are smaller.
> Whether an MIL/attention bridge recovers residue-level information from bag-level labels is, after a
> literature search on 15 Oct 2026, **not something we found reported** — and a **negative answer is also a
> usable result**. Component mechanisms — attention-MIL on proteins, conditional modulation, accessibility
> as an input feature — **are established prior art** and are not claimed as new.
>
> <small>⬜ proposed, no measurement yet. Representation choice (PLM vs one-hot) is part of the same experiment grid.</small>

**Ghi chú sản xuất — chỗ cần điền và chỗ không được nói.**

**Cần điền sau:** (a) chọn A/B/C sau khi chạy; (b) sơ đồ kiến trúc chi tiết với kích thước tensor
(`L = 28`, `D = ?`, cửa sổ `w = ±3` đã đo là thang có tín hiệu); (c) delta đo được so với **0,7693**, kèm
bất định; (d) kết quả ablation ô chéo cho đặc trưng phơi lộ.

⚠ **Năm câu không được lên slide** (đã bị bác bỏ trong repo):
- ❌ "we propose a novel aggregation mechanism" — attention-MIL trên protein đã có tiền lệ (BioBlobs 2025)
- ❌ "MIL is more robust to noisy labels" — lý lẽ của Ilse 2018 là về nhãn **vắng mặt**, không phải nhãn
  **nhiễu**; không tìm thấy phép so sánh có kiểm soát theo tỉ lệ nhiễu
- ❌ "nobody has placed an exposure gate at the pooling step" — Yang et al. (*PLOS Comput Biol* 22(8):e1014552,
  2026) dùng rASA làm đặc trưng node **cộng** attention pooling có vector truy vấn học được, và đó là **tập
  mẹ** của cổng đặt tay ⇒ phải dựa vào **ablation ô chéo**, không dựa vào việc không tìm thấy tiền lệ
- ❌ **"MIL vs per-position head has no precedent"** — mô típ chuẩn đã có; tính mới phải đặt ở **giám sát
  yếu** ([C-17](../../../DECISIONS.md#c-17) mục a)
- ❌ mọi dạng "nobody has done X" — viết "a literature search on 15 Oct 2026 did not find…"

**Lưu ý thêm về đặc trưng phơi lộ:** rASA/pLDDT **không có phương sai** trên nhãn chính (peptide tách rời
đều phơi lộ như nhau), nên tham số của một cổng phơi lộ **không nhận diện được** từ dữ liệu nhiệm vụ chính.
Nó là **cơ chế chuyển giao** cho phần protein nguyên vẹn, **không** nằm trên đường găng
([D-028](../../../DECISIONS.md#d-028) mục 1). Nếu đưa lên slide thì đặt ở phần chuyển giao, không ở phần
đóng góp chính.

**Hình.** Workflow tổng thể 5 khối theo đúng khuôn hướng dẫn §3:
`data sources + counts` → `filter / label / cluster split` → `representation` → `model (+ 3 variants)` →
`evaluation + ceiling`. Khối `model` vẽ **nét đứt hổ phách** với nhãn `[proposed]`, ba nhánh A/B/C rẽ ra
rồi gộp lại ở khối evaluation. Ghi **số mẫu** trên các mũi tên. Nhãn hình: `own diagram — proposed, not yet validated`.

## Slide 22 — Evaluation plan ⟨SKELETON — planning table, not results⟩

**Chữ lên slide:**

> **Each row is one question with one controlled comparison. Cells marked "not measured" are not yet run.**
>
> | Question | What is held fixed | Metric | Status |
> |---|---|---|---|
> | Does a residue-level model beat the composition baseline? | split, labels, window | cell-level AUROC | ✅ **+0.0289**, CI [0.0264, 0.0313] |
> | Does it beat the closest published control (ΔPAP)? | same test clusters, paired | paired diff + bootstrap CI | ✅ **+0.0300** (scanning) · ⬜ **−0.0420** (matrix) |
> | At which scale does the information sit? | one feature block changed at a time | same split, same metric | ✅ decomposed — slide 14 |
> | Are context weights **stable** across bootstraps? | — | sign agreement, \|μ\|/SD per coefficient | ✅ 53.3% separable, sign agreement 0.90 |
> | Does the **MIL bridge** recover residue information from bag-level labels? | window, loss, budget, seeds | bag metric **and** localisation metric | ⬜ **not measured** |
> | Does representation or architecture drive the gain? | representation × model grid | same split, same metric | ⬜ **not measured** |
> | Does it beat the closest precedent (Degformer) **under a cluster split**? | re-run its checkpoint on our split | same metrics | ⬜ **not measured** |
> | Where does the model fail? | per-group sample counts | error analysis by group | ⬜ **not measured** |
>
> **Committed in advance:** the minimum detectable difference is **0.0123** on the saturation matrix and
> **0.0025–0.0036** on the scanning set. An ablation below that threshold will be reported as
> **indistinguishable**, not as a win. Bootstrap resampling is done at the **protein-cluster** level, paired
> by peptide.
>
> **Every results table reports the measured ceiling next to the model number**, and reports **each metric
> separately** — the model ranking is known to reverse between cell-level and position-level scoring.
> Ceiling-reporting convention follows LeBlanc et al. 2026.
>
> <small>✅ measured, with result files · ⬜ planned, no number yet.</small>

**Ghi chú sản xuất.**
- ⚠ **Bảng này đã đổi tính chất sau phiên 8**: bản đầu là **bảng kế hoạch** toàn ô "chưa đo"; nay **bốn
  dòng đầu đã có kết quả**. Giữ ký hiệu ✅/⬜ để GVHD đọc được ngay đâu là đã đo.
- **Rủi ro LeBlanc "thành phần > vị trí" nay trả lời được bằng số**, và đây là câu trả lời chuẩn bị sẵn nếu
  GVHD hỏi: *"kết luận của LeBlanc không bị bác, nó bị khoanh lại. Trên nhãn mức peptide/tile thì đúng —
  thành phần ổn định hơn vị trí ≈ 56 lần. Trên nhãn hiệu ứng đột biến, tỉ lệ đó còn 2,2 lần, và tỉ lệ hệ số
  ngữ cảnh tách khỏi 0 tăng từ 28,9% lên 53,3%. Em đã đo cả hai bằng đúng khuôn kiểm của họ."*
- ⚠ **Và phải nói kèm điều ngược lại**, nếu không thì thành thổi phồng: bộ bão hòa **một mình thiếu lực**
  cho tham số ngữ cảnh (chỉ 25% ô tách khỏi 0 trên 89 cụm) — đó chính là lý do thiết kế **học ngữ cảnh trên
  bộ quét, xác nhận ma trận trên bộ bão hòa**.
- Hướng dẫn §4: khi chưa chạy thì ô ghi "chưa đo", không điền số minh họa. Dòng ⬜ giữ đúng vậy.

**Hình.** Bảng này đã là hình. Thêm **ma trận đối chứng nhỏ** bên cạnh: trục ngang = representation
(one-hot / PLM), trục dọc = model (composition / per-position / MIL / hybrid); mọi ô tô hổ phách nhạt với
chữ `—`, trừ ô composition×one-hot tô xanh mòng (đã có baseline). Người nghe thấy ngay đâu là việc đã làm
và đâu là việc sẽ làm.

---

# PHẦN 8 — NEXT STEPS

## Slide 23 — Plan for the remaining weeks

**Chữ lên slide:**

> **Where the thesis stands (week 6)**
> | Gate | Criterion | Status |
> |---|---|---|
> | **G1** | labels are independent experimental measurements | ✅ **met** — all labels measured, none generated by this pipeline |
> | **G2** | a measurable **positive** contribution | ✅ **first positive result**: +0.0289 over the composition class, +0.0300 over the published control, both with CIs excluding zero. ⬜ The matrix gap (−0.0420) is the remaining target |
> | **G3** | a feasible application | ⚠ **in design** — five precedents exist; differentiation is API, arbitrary-mutation scoring, uncertainty anchored to the measured ceiling, label provenance |
>
> **Plan**
> | Week | Work | Output |
> |---|---|---|
> | **7** | architecture variants A / B / C on one grid, aimed at the **0.7693** target | a measured delta on the matrix, with CI |
> | **8** | ablations · seed stability · Degformer checkpoint re-run under the cluster split | controlled comparison table |
> | **9** | representation grid (PLM vs one-hot) · error analysis by group | where the gain comes from, where it fails |
> | **10** | **hard checkpoint** | if the matrix target is not met, report it as a bounded negative and shift weight to benchmark + application |
> | **11–13** | application: 28×20 matrix, per-position map, uncertainty, API | the deliverable for criterion 5 |
> | **14–15** | thesis write-up and defence | — |
>
> **Reproducibility commitments:** fixed seeds; configuration and results written to files; every number
> in the thesis traceable to a result file; all derived data regenerable by script from checksummed raw data.

**Ghi chú sản xuất.**
- Thứ tự tuần đã **dịch lên một bậc** so với [D-029](../../../DECISIONS.md#d-029): việc của tuần 7 trong
  D-029 (lực trên n = 91 + baseline) **đã làm xong ở phiên 8**, nên tuần 7 nay là kiến trúc.
  **Điểm kiểm cứng cuối tuần 10** giữ nguyên theo [D-028](../../../DECISIONS.md#d-028) mục 3, và **nói ra
  trước GVHD** là điểm mạnh: nó cho thấy có kế hoạch cho trường hợp xấu, trong khi đề tài **không có dự
  phòng** ([D-026](../../../DECISIONS.md#d-026)).
- ⚠ **Nếu Trọng muốn bảng tuần này thành căn cứ** thì cần một mục quyết định mới sửa D-029 — hiện bảng trên
  là **suy ra** từ D-029 + D-031, không phải một quyết định đã ghi.
- **Một việc tuỳ chọn chưa đưa vào bảng:** [C-16](../../../DECISIONS.md#c-16) — dùng dữ liệu `CTNNB1` của
  Krishna 2026 (*Nat Genet* 58:366–375) làm **đối chứng ngoài độc lập** (nhóm tác giả khác, assay khác,
  protein chưa thấy). Nó đóng được rủi ro "cả hai nguồn nhãn đều của một nhóm tác giả". Nhưng **giấy phép
  chưa rõ** và readout là **tín hiệu Wnt**, không phải độ bền ⇒ chỉ gọi được là **đối chứng hội tụ**. Đang
  chờ Trọng; nếu nhận thì chèn vào tuần 8–9.
- **Không** nêu trên slide rằng không có đề tài dự phòng. Nếu GVHD hỏi thì trả lời thẳng.
- Ba cổng G1/G2/G3 là khung nội bộ của repo, **không phải** của học phần — nếu dùng từ "gate" trên slide thì
  nói rõ đây là tiêu chí tự đặt, hoặc đổi nhãn thành "readiness check" để tránh gợi ý sai rằng học phần có
  ba cổng này.

**Hình.** Thanh tiến độ ngang tuần 6 → 15, ba chip trạng thái G1/G2/G3 (xanh mòng ✓ / hổ phách ⬜ / hổ phách
⚠) ở đầu, và một **cờ đỏ san hô ở tuần 10** nhãn "checkpoint: pivot if no positive delta". `own diagram`.

## Slide 24 — Questions for discussion

**Chữ lên slide:**

> **1. Contribution shape.** Does a contribution framed as *"a proof that the current model class cannot
> localise, an evaluation protocol for the task, and a new architecture for residue-level supervision"*
> meet expectations for this thesis?
>
> **2. Architecture novelty.** The intended novelty is a **weak-supervision question**: can abundant
> bag-level labels (260k peptides, 212k tiles), which do **not** identify positional parameters, be mined
> for residue-level output through an MIL/attention bridge — and beat a per-position head trained on the
> smaller cell-level set? Component mechanisms are established prior art. Is that the right level at which
> to place the novelty claim?
>
> **3. Reading the two-sided result.** The model is **ahead** of the published control on the context axis
> (+0.0300) and **behind** it on the substitution matrix (−0.0420), and the ranking **reverses** between
> cell-level and position-level metrics. Should the thesis commit to **one** headline metric, or report the
> split result as the finding?
>
> **4. Application scope.** For criterion 5, is a **web tool with an API** returning the 28×20 matrix with
> per-prediction uncertainty an adequate application, given that five tools already exist in the
> neighbourhood?
>
> ---
>
> **Thank you.** Data, scripts, result files and the decision log are in the project repository.

**Ghi chú sản xuất.**
- **Câu hỏi 1 là [C-5](../../../DECISIONS.md)** — việc phải làm, chưa làm, và không hoãn được thêm: toàn bộ
  cách đặt đóng góp hiện nay dựa trên [D-022](../../../DECISIONS.md#d-022), là thông tin Trọng truyền đạt và
  **chưa có biên bản**. Hỏi xong thì ghi vào `project/meetings/` và cập nhật `DECISIONS.md`.
- **Câu hỏi 2** cũng xin xác nhận lại lời GVHD ngày 11/10 ("kỳ vọng một kiến trúc chưa ai dùng") so với lời
  12/10 (chấp nhận đóng góp dạng công cụ). Hai lời được giữ cả hai ở
  [people.md](../../../project/people.md); cách đọc hiện tại là **của Claude, chưa được GVHD xác nhận**.
- **Câu hỏi 3 đã đổi sau phiên 8.** Bản đầu hỏi về **cỡ mẫu** (n = 91, MDE 0,071) — câu đó nay **đã tự trả
  lời được**: MDE thật là 0,0123, và bộ quét cho 1.985 cụm. Câu hỏi đáng hỏi hơn là **cách đọc một kết quả
  hai mặt**, vì đó là chỗ GVHD có kinh nghiệm hơn và là chỗ quyết định cách viết chương kết quả.
- Nếu còn thời gian, hỏi thêm hai điều: (a) có nên dành ngân sách cho phần chuyển giao sang protein nguyên
  vẹn (MaveDB, 9 gene) hay dồn hết vào nhiệm vụ chính; (b) có nên theo
  [C-16](../../../DECISIONS.md#c-16) lấy một đối chứng ngoài từ nhóm tác giả khác.

---

## Phụ lục slide (để sau phần Q&A, không trình bày)

| # | Nội dung | Nguồn |
|---|---|---|
| A1 | **References** — đầy đủ 12 công trình, đúng danh sách tác giả ở slide 8 và 11 | — |
| A2 | Bảng hằng số benchmark đầy đủ, kèm đường dẫn file kết quả | `research/*/[*.json]` |
| A3 | Sổ nguồn gốc dữ liệu: URL/DOI, revision ghim, giấy phép, ngày tải, SHA-256 | [data/README.md](../data/README.md) |
| A4 | Giải thích đầy đủ các trường của tập huấn luyện, quy tắc tile, quy tắc giải mã id | [data/README.md §4](../data/README.md) |
| A5 | Kiến trúc PAP đọc từ mã nguồn, và phép kiểm bất biến hoán vị | [pap-baseline/](../research/pap-baseline/README.md) |
| A6 | Phân tích lực và MDE | [full-data-audit/](../research/full-data-audit/README.md) |

---

## Việc phải làm trước khi dựng slide

| # | Việc | Chặn slide nào | Chi phí |
|---|---|---|---|
| ~~1~~ | ~~Trọng chốt C-15~~ | — | ✅ **xong** — [D-031](../../../DECISIONS.md#d-031) |
| ~~3~~ | ~~Đếm số cụm protein trong n = 91~~ | — | ✅ **xong** — 89 cụm |
| 2 | **Sinh hình ví dụ** từ `psi-sat_*.tsv`: chọn peptide trong tập train, xuất heatmap 28×20 + bar per-position | **slide 16** | 1 script nhỏ |
| 4 | Dựng các sơ đồ tự dựng, hoặc chỉnh lại từ [`lectures/degron-basics/figures/`](../../../lectures/degron-basics/figures/) | 2, 3, 4, 5, 6, 9, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23 | **phần lớn thời gian** |
| 5 | Kiểm lại caption + giấy phép cho 2 hình của Voutsinos (slide 7, 10) | 7, 10 | rẻ |
| 6 | Quyết định định dạng xuất: HTML trong repo (theo [D-013](../../../DECISIONS.md#d-013)) hay PPTX để trình bày | — | quyết định |
| 7 | **Mới:** quyết định có ghi bảng tuần ở slide 23 thành một mục sửa [D-029](../../../DECISIONS.md#d-029) hay không | 23 | quyết định |
| 8 | **Mới:** nếu nhận [C-16](../../../DECISIONS.md#c-16) thì thêm một dòng đối chứng ngoài vào slide 22 | 22, 23 | quyết định |

**Chưa làm trong phiên này:** chưa dựng slide, chưa sinh hình, chưa sửa
[presentation.html](presentation.html) hay [session-02-prep.md](session-02-prep.md), chưa ghi quyết định nào
vào [DECISIONS.md](../../../DECISIONS.md), chưa huấn luyện hay đo thêm bất cứ thứ gì. Mọi con số trong file
này **trích** từ các báo cáo đã có, không có con số nào đo mới trong phiên này.
