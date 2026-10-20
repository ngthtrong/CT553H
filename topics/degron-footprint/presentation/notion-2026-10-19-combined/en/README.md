# English Notion page — project overview, 19/10/2026 (rà soát trình bày cùng ngày)

Bản **tiếng Anh** của [trang tám mục](../README.md), dựng ngày 19/10/2026 và **được rà soát lại cùng
ngày** theo góc nhìn người đọc báo cáo: đổi cấu trúc mục, bỏ kiểu trình bày nhãn, bỏ emoji, số hoá
hình/bảng. Hồ sơ sản xuất, **không ghi quyết định**
([DECISIONS.md](../../../../../DECISIONS.md)).

| | |
|---|---|
| **Main page** | <https://app.notion.com/p/3fe486d98ebc811eba29eb9e0987a0e1> — tiêu đề nay là **“Residue-Level Degron Mutation Effects: Project Overview”**, **private (draft)**, chưa đặt dưới trang cha |
| **Repo source, main page** | [content-main.md](content-main.md) |
| **Repo source, bảy trang con** | [content-subpages.md](content-subpages.md) |
| **Vietnamese counterpart** | [../README.md](../README.md) · [../content-main.md](../content-main.md) · [../content-subpages.md](../content-subpages.md) |

⚠ **Ba bản không tự đồng bộ:** Notion tiếng Anh ↔ repo tiếng Anh ↔ bản tiếng Việt. Sau phiên rà soát,
bản tiếng Anh **đã lệch cấu trúc** với bản tiếng Việt (9 mục so với 8, tên trang con khác, không còn
emoji), nên không còn là bản dịch 1:1.

## Cấu trúc sau rà soát: chín mục

`1` Introduction · `2` Related work · `3` Why the work is needed · `4` Problem definition ·
`5` Data and processing (gộp mục 5+6 cũ) · `6` Proposed method · `7` Current results (tách khỏi mục
phương pháp) · `8` Product · `9` Plan, open items and limitations (**mục mới**).

Mục 9 thay cho danh sách **“Four things never to claim”** của bản cũ (vốn đếm sai: tiêu đề “four”
nhưng có năm gạch đầu dòng) và cho các câu tự nhắc rải khắp trang: nay là một mục *limitations* viết ở
thể khẳng định, có thêm phần **open items** nói rõ việc còn lại. Ràng buộc nội dung vẫn theo
[D-036](../../../../../DECISIONS.md#d-036), [D-035](../../../../../DECISIONS.md#d-035),
[D-032](../../../../../DECISIONS.md#d-032), [C-17](../../../../../DECISIONS.md#c-17),
[D-031](../../../../../DECISIONS.md#d-031); mục 7 và trang con 6–7 vẫn nói thẳng **G2 is not
complete**. Mốc thời gian **không** ghi trên trang, chỉ trỏ về `DECISIONS.md` và hồ sơ học phần.

## Bảy trang con — tên theo mục cha

Trang con nay **mang đúng số mục của trang chính**, hết tình trạng “mục 7 lại bấm vào subpage 6”.
Tiểu mục bên trong cũng dùng chung hệ số đó (`3.1`, `5.4`, `6.1`, `7.1`, `8.3` …).

| Notion title | URL | Icon | Supports |
|---|---|---|---|
| Section 1 · Biological background and the three levels of question | <https://app.notion.com/p/3fe486d98ebc81acac72ff24be0db541> | `icons/microscope_gray` | §1 |
| Section 2 · Related work, study by study | <https://app.notion.com/p/3fe486d98ebc81b5b5c5fa55b3fd19a4> | `icons/book_gray` | §2 |
| Section 3 · Why the work is needed | <https://app.notion.com/p/3fe486d98ebc81539287e95d2f8866e3> | `icons/target_gray` | §3 |
| Section 4 · The task, PSI and ΔPSI | <https://app.notion.com/p/3fe486d98ebc8187814fd7b06f9c03ca> | `icons/ruler_gray` | §4 |
| Section 5 · Data and processing pipeline | <https://app.notion.com/p/3fe486d98ebc811ca4e9dc6eac4a837b> | `icons/database_gray` | §5 |
| Sections 6–7 · Method, controls and current results | <https://app.notion.com/p/3fe486d98ebc815091e1d577f78435b5> | `icons/chart_gray` | §6 và §7 |
| Section 8 · Product, comparison and application domain | <https://app.notion.com/p/3fe486d98ebc81669f7ddd16bf32f94a> | `icons/wrench_gray` | §8 |

## Icon thay cho emoji

Trang chính và bảy trang con **không còn emoji nào** trong tiêu đề, callout hay văn xuôi. Page icon và
callout icon dùng **Notion icon identifier**; callout thu về **bốn vai**:

| Vai | Icon | Màu | Dùng khi |
|---|---|---|---|
| Orientation | `icons/document_gray` | `gray_bg` | câu mở trang: trang này là chi tiết của mục nào |
| Scope | `icons/ruler_gray` | `gray_bg` | phạm vi dự đoán, cái gì **không** thuộc bài toán |
| Limitation | `icons/warning_yellow` | `yellow_bg` | giới hạn của dữ liệu/kết quả, cách đọc số cho đúng |
| Status | `icons/clock_blue` | `blue_bg` | trạng thái: hướng chưa chốt, cổng G2 chưa xong |

Icon của trang chính là `icons/dna_blue`. **Tên icon phải thuộc bộ của Notion**: `chart-bar`,
`bar-chart`, `graph`, `info` đều bị API từ chối; các tên đã kiểm là hợp lệ: `dna`, `microscope`,
`book`, `target`, `ruler`, `database`, `chart`, `wrench`, `document`, `warning`, `clock`.

## Những gì đã sửa về nội dung (không phải chỉ câu chữ)

- **`PSI_WT` → `PSI_ref`**, kèm một câu định nghĩa reference cho từng tập (scanning có WT đo trực
  tiếp; saturation lấy trung vị ô đồng nghĩa). Ký hiệu cũ mâu thuẫn với chính mục 5.3.
- **Phễu lọc bộ quét** nói rõ: 8.831 → 3.439 (degron, PSI ≤ 3,0) → **2.994** sau khi đòi độ sâu ≥ 10
  read và ≥ 21 vị trí đo được — khớp [residue-task-derisk-2026-10-15](../../../research/residue-task-derisk-2026-10-15/README.md)
  và [D-031](../../../../../DECISIONS.md#d-031). Con số **2.624** của
  [e3-labels-audit](../../../research/e3-labels-audit/README.md) là tập cũ **đòi thêm có footprint**,
  nay được ghi chú là không so sánh trực tiếp được.
- **28×19 vs 28×20** được giải thích ngay trên trang chính (cột thứ 20 giữ acid amin gốc, không phải
  đột biến mới), không bắt người đọc mở trang con.
- **Định nghĩa `M0`/`M3`, `cov80`, `cnn2w1/w7`, `MDE`, `cell`** gom vào một toggle *Abbreviations* ở
  đầu trang chính; trước đó “Ridge M3” là số headline mà không ở đâu định nghĩa.
- **Koren et al. 2018** được thêm vào bảng related work của trang chính (trước chỉ có ở trang con).
- **Larsen 1.626 vs 1.627** ghi rõ là **hai mẫu số khác nhau** (danh mục TF so với số gene trong file
  chú giải), theo [SOURCE.md](../../../data/raw/larsen-2025/SOURCE.md).
- **Zhang 2025** (review) ghi kèm tạp chí và chú thích “không phải nguồn nhãn 2023”, để không lẫn với
  Zhang et al. 2023 và Zhang SVM 2023.
- **Tham chiếu chéo sai** ở trang con sản phẩm (“the comparison in Section 7”) nay trỏ đúng
  **Table 7.1** của trang phương pháp–kết quả.
- Dung lượng dữ liệu ghi **≈2,3 GB**, khớp [data/README.md](../../../data/README.md) (ghi chú
  `~1,9 GB` trong `resources/README.md` là số trước phiên G2).

## Những gì đã sửa về trình bày

- Bỏ **“Message:”** và toàn bộ nhãn đầu đoạn (`Why it is worth doing.`, `Who uses it.`,
  `The plain question:`, `Motivation.`, `What exists so far.`, `User flow:`, `Two messages:`,
  `A sentence to drop:`, `Stated plainly:`).
- Bỏ các câu **tự nhắc người thuyết trình**: cột bảng `What to say` (ba bảng ở trang con 2),
  `Do not say …`, `Do not add a “batch submission” row`, `Do not put the ≈1,600 variants …`,
  `Use one number on a slide and keep the other for questions`. Nội dung cần giữ đã chuyển thành câu
  khẳng định hoặc mục *limitations*.
- **Tiêu đề** không còn kể ý định người viết (`must be addressed directly`, `stated briefly`,
  `stated before being asked`, `the non-negotiable part`, `a number, not an assertion`).
- **Hình và bảng được đánh số** (Figure 1–5, Table 1–3 ở trang chính; `Figure 3.1`, `Table 5.3` …
  ở trang con) và được **gọi tên trong văn**. Bốn hình trước đây **không có caption** nay đều có.
- Bỏ `⇒` trong văn xuôi (giữ trong bảng), giảm in đậm, giảm mô-típ “N thứ”.

⚠ **Hạn chế kỹ thuật đã gặp:** khi dùng `replace_content`, Notion **giữ caption cũ** của block ảnh và
bỏ qua caption mới; với ảnh **vốn không có caption** thì không match được bằng `update_content`. Cách
đã dùng: sửa caption bằng `update_content` khớp theo chữ đầu caption cũ, và với ảnh không caption thì
thêm **một dòng in nghiêng “Figure N. …”** ngay dưới ảnh. Một lần `replace_content` còn **đẩy ảnh
không caption lên đầu trang** (trang con 5) — đã dựng lại và kiểm bằng readback.

## Hình

Dùng lại **đúng tám file ảnh** của bản tiếng Việt (không upload mới), caption đã dịch và nay có số
hình; hai hình bị Trọng loại (`biology.png`, `mutation-map.gif`) **vẫn không có mặt**.

| Vị trí | Hình | Bản trong repo | Giấy phép |
|---|---|---|---|
| Main Fig 1–2 | `translation.gif` · `ubl-2qjl.gif` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/) — ⚠ **đang bị xoá khỏi working tree** | **CC BY-SA 3.0** |
| Main Fig 3 | `example-heatmap.png` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/example-heatmap.png) — ⚠ **đang bị xoá khỏi working tree** | Tự dựng từ dữ liệu đo |
| Main Fig 4 | sơ đồ pipeline | PNG trên Notion; repo giữ **mã `mermaid`** trong [content-main.md](content-main.md) | Tự dựng |
| Main Fig 5 (§6) | sơ đồ ý tưởng phương pháp, **dựng mới 19/10** | [png/fig-method.png](png/fig-method.png) + [fig_method.py](fig_method.py) (matplotlib, tái lập được) | Tự dựng |
| Main Fig 6 · Sub 7.1 | `fig-benchmark.png` | [notion-2026-10-19/png/](../../notion-2026-10-19/png/fig-benchmark.png) | Tự dựng |
| Sub 3.1 | `fig-01-urgency-forest.png` | [notion-2026-10-16/png/](../../notion-2026-10-16/png/fig-01-urgency-forest.png) | Tự dựng; ClinVar ghi công PMID 29165669 |
| Sub 4.1 | `grid-schematic.png` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/grid-schematic.png) — ⚠ **đang bị xoá khỏi working tree** | Tự dựng, caption ghi rõ là sơ đồ |
| Sub 5.1 | `gfp-small.gif` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/gfp-small.gif) — ⚠ **đang bị xoá khỏi working tree** | **CC BY-SA 4.0**, bản đã chỉnh sửa |
| Sub 5.2–5.3 · 6.1 · 8.1 | bốn sơ đồ | PNG trên Notion; repo giữ **mã `mermaid`** trong [content-subpages.md](content-subpages.md) | Tự dựng |
| Sub 7.2 | `fig-degformer.png` | [notion-2026-10-19/png/](../../notion-2026-10-19/png/fig-degformer.png) | Tự dựng |

⚠ **Thư mục `presentation/pptx-2026-10-16/` đang bị xoá khỏi working tree** (23 file hiện ở trạng
thái ` D` trong `git status`, **chưa commit**), nên `check_links.py` báo hỏng mọi link trỏ vào
`../../pptx-2026-10-16/assets/…` — kể cả từ bản tiếng Việt và từ `resources/README.md`. **File vẫn còn
trong git** (`git ls-files` thấy đủ ảnh), nên link bản thân **không sai**: cần Trọng quyết (a) phục hồi
bằng `git checkout -- topics/degron-footprint/presentation/pptx-2026-10-16`, hay (b) xoá thật rồi sửa
link ở mọi nơi. Phiên này **không tự phục hồi và không tự xoá**. Lưu ý `resources/README.md` còn gọi
thư mục này là `deck-pptx-2026-10-16` — tên đó **chưa từng có** trong repo.

⚠ **ShareAlike:** ba GIF là CC BY-SA. Trang đang **riêng tư**; chia sẻ ra ngoài thì phải rà lại điều
khoản ShareAlike trước — áp cho cả bản tiếng Anh.

## Còn lệch với bản tiếng Việt

Bản tiếng Việt **chưa** được rà soát: vẫn 8 mục, vẫn dùng “Thông điệp/Message”, vẫn còn emoji, trang
con vẫn đánh `1 ·`…`7 ·`, chưa có mục 3.4 nguồn số, và vẫn ghi `PSI_WT`. Muốn hai bản giống nhau thì
phải áp cùng loạt sửa này sang [../content-main.md](../content-main.md),
[../content-subpages.md](../content-subpages.md) và bốn trang Notion tiếng Việt.
