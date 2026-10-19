# English version of the eight-section Notion page — 19/10/2026

Bản **tiếng Anh** của [trang tám mục](../README.md), dựng cùng ngày 19/10/2026 theo yêu cầu của
Trọng. Cùng cấu trúc: **trang chính là khung ở mức ý tưởng, chi tiết nằm trong bảy trang con**. Hồ sơ
sản xuất, **không ghi quyết định** ([DECISIONS.md](../../../../../DECISIONS.md)).

| | |
|---|---|
| **Main page** | <https://app.notion.com/p/3fe486d98ebc811eba29eb9e0987a0e1> — **private (draft)**, chưa đặt dưới trang cha |
| **Repo source, main page** | [content-main.md](content-main.md) |
| **Repo source, seven subpages** | [content-subpages.md](content-subpages.md) |
| **Vietnamese counterpart** | [../README.md](../README.md) · [../content-main.md](../content-main.md) · [../content-subpages.md](../content-subpages.md) |

⚠ **Ba bản không tự đồng bộ:** Notion tiếng Anh ↔ repo tiếng Anh ↔ bản tiếng Việt. Sửa một chỗ thì
phải sửa hai chỗ còn lại bằng tay.

## Seven subpages

| # | Subpage | Supports which section |
|---|---|---|
| 1 | [Biological background and the three levels of question](https://app.notion.com/p/3fe486d98ebc81acac72ff24be0db541) | 1 · Introduction |
| 2 | [Related work, study by study](https://app.notion.com/p/3fe486d98ebc81b5b5c5fa55b3fd19a4) | 2 · Related work |
| 3 | [Urgency, the demonstrable gap, and the user groups](https://app.notion.com/p/3fe486d98ebc81539287e95d2f8866e3) | 3 · Gap |
| 4 | [The task, PSI and ΔPSI](https://app.notion.com/p/3fe486d98ebc8187814fd7b06f9c03ca) | 4 · Problem definition |
| 5 | [Data and processing pipeline](https://app.notion.com/p/3fe486d98ebc811ca4e9dc6eac4a837b) | 5 · Dataset **and** 6 · Data processing |
| 6 | [Method, controls and current results](https://app.notion.com/p/3fe486d98ebc815091e1d577f78435b5) | 7 · Proposed method (provisional) |
| 7 | [Product — features, comparison and application domain](https://app.notion.com/p/3fe486d98ebc81669f7ddd16bf32f94a) | 8 · Product |

## Quan hệ với bản tiếng Việt

Dịch 1:1 theo mục, **không thêm nội dung, không thêm số đo**. Những chỗ khác biệt duy nhất:

- **Định dạng số** chuyển sang quy ước tiếng Anh: `2,148×` → `2.148×`, `0,8082` → `0.8082`,
  `530.412` → `530,412`, `5,0 × 10⁻⁷` → `5.0 × 10⁻⁷`. Giá trị không đổi.
- **Nhãn mức bằng chứng** dịch sang `[UNVERIFIED]` / `[SOURCE]` (tiếng Việt: `[CHƯA KIỂM]` /
  `[NGUỒN]`).
- Callout đầu trang chính nói rõ đây là bản tiếng Anh của trang cùng ngày.
- **Trang con 3 có thêm mục `3.4 · Sources behind every number on this page`** (19/10, theo yêu cầu
  của Trọng): bảng ánh xạ từng con số → nguồn ngoài (study / dataset / release) → report nội bộ
  trong repo, kèm callout ghi công và giấy phép. Các bảng ở 3.2–3.3 cũng được bổ sung dẫn nguồn
  tại chỗ. ⚠ **Bản tiếng Việt chưa có phần này** — nếu muốn giống nhau thì phải thêm sang
  [../content-subpages.md](../content-subpages.md) và trang Notion tiếng Việt.
- Tiêu đề trang dùng dấu hai chấm (`Residue-Level Degron Mutation Effects: Eight-Section Overview`)
  — lần publish đầu dùng dấu gạch dài `—` thì Notion **cắt mất phần sau dấu gạch**; đã sửa bằng
  `update_properties`.

## Hình

Dùng lại **đúng tám file ảnh** của bản tiếng Việt, tham chiếu lại cùng file trong workspace
`ngthtrong` (không upload mới). Caption đã dịch, giữ nguyên ghi công và tên giấy phép. Hai hình bị
loại theo yêu cầu của Trọng (`biology.png` — sơ đồ ubiquitin–proteasome tự dựng; `mutation-map.gif`
— GIF A4V giả định) **vẫn không có mặt**.

| Vị trí | Hình | Nguồn trong repo | Giấy phép |
|---|---|---|---|
| Main §1 | `translation.gif` · `ubl-2qjl.gif` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/) | **CC BY-SA 3.0** |
| Main §4 | `example-heatmap.png` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/example-heatmap.png) | Tự dựng từ dữ liệu đo |
| Main §7 · Sub 6 | `fig-benchmark.png` | [notion-2026-10-19/png/](../../notion-2026-10-19/png/fig-benchmark.png) | Tự dựng |
| Sub 3 | `fig-01-urgency-forest.png` | [notion-2026-10-16/png/](../../notion-2026-10-16/png/fig-01-urgency-forest.png) | Tự dựng; ClinVar ghi công PMID 29165669 |
| Sub 4 | `grid-schematic.png` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/grid-schematic.png) | Tự dựng, caption ghi rõ là sơ đồ |
| Sub 5 | `gfp-small.gif` | [pptx-2026-10-16/assets/](../../pptx-2026-10-16/assets/gfp-small.gif) | **CC BY-SA 4.0**, bản đã chỉnh sửa |
| Sub 6 | `fig-degformer.png` | [notion-2026-10-19/png/](../../notion-2026-10-19/png/fig-degformer.png) | Tự dựng |

⚠ **ShareAlike:** ba GIF là CC BY-SA. Trang đang **riêng tư**; chia sẻ ra ngoài thì phải rà lại điều
khoản ShareAlike trước — áp cho cả bản tiếng Anh.

## Ràng buộc câu chữ

Giữ nguyên toàn bộ các câu cấm của bản tiếng Việt, gồm mục cuối trang chính **"Four things never to
claim"**: [D-036](../../../../../DECISIONS.md#d-036),
[D-035](../../../../../DECISIONS.md#d-035), [D-032](../../../../../DECISIONS.md#d-032),
[C-17](../../../../../DECISIONS.md#c-17), [D-031](../../../../../DECISIONS.md#d-031). Mục 7 và trang
con 6 nói thẳng **G2 is not complete**.
