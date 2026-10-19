# Trang Notion tám mục — trang chính mỏng + bảy trang con, 19/10/2026

Trang **tiếng Việt** gộp hai trang Notion đang có thành **một mạch báo cáo tám mục**, theo kiểu
**trang chính là khung trình bày ở mức ý tưởng, chi tiết đẩy xuống trang con**. Soạn theo yêu cầu
của Trọng ngày 19/10/2026. Hồ sơ sản xuất, **không ghi quyết định**
([DECISIONS.md](../../../../DECISIONS.md)).

| | |
|---|---|
| **Trang chính** | <https://app.notion.com/p/3fe486d98ebc8164b0e8de199d371f76> — **riêng tư (draft)**, chưa đặt dưới trang cha |
| **Bản nguồn trang chính** | [content-main.md](content-main.md) |
| **Bản nguồn bảy trang con** | [content-subpages.md](content-subpages.md) |
| **Bản tiếng Anh** | [en/README.md](en/README.md) — [main page](https://app.notion.com/p/3fe486d98ebc811eba29eb9e0987a0e1) + bảy trang con, dịch 1:1 |
| **Căn cứ nội dung** | [DECISIONS.md phần A](../../../../DECISIONS.md#hien-hanh), [D-031](../../../../DECISIONS.md#d-031), [D-032](../../../../DECISIONS.md#d-032), [D-033](../../../../DECISIONS.md#d-033), [D-035](../../../../DECISIONS.md#d-035), [D-036](../../../../DECISIONS.md#d-036), [C-11a](../../../../DECISIONS.md#c-11a), [C-20](../../../../DECISIONS.md#c-20); kết quả 18/10 ở [g2-saturation](../../research/g2-saturation-2026-10-18/README.md) và [g2-extension](../../research/g2-extension-2026-10-18/README.md) |

⚠ **Notion và repo không tự đồng bộ.** Sửa một bên thì phải sửa bên kia bằng tay.

## Bảy trang con

| # | Trang con | Đỡ cho mục nào của trang chính |
|---|---|---|
| 1 | [Nền sinh học và ba mức câu hỏi](https://app.notion.com/p/3fe486d98ebc8196823ccb7c62c6eaa0) | 1 · Introduction |
| 2 | [Nghiên cứu liên quan — chi tiết từng công trình](https://app.notion.com/p/3fe486d98ebc81868bf7cd2248556f97) | 2 · Related work |
| 3 | [Tính cấp thiết, chỗ hở và nhóm người dùng](https://app.notion.com/p/3fe486d98ebc817abeefe736dd7b5d6d) | 3 · Gap |
| 4 | [Bài toán, PSI và ΔPSI](https://app.notion.com/p/3fe486d98ebc81ee8ba6c03ad9722b9b) | 4 · Problem definition |
| 5 | [Dữ liệu và quá trình xử lý](https://app.notion.com/p/3fe486d98ebc8169b822c63f7ee8ed5a) | 5 · Dataset **và** 6 · Xử lý dataset |
| 6 | [Phương pháp, đối chứng và kết quả hiện tại](https://app.notion.com/p/3fe486d98ebc81b2a749df9aabb0d9ec) | 7 · Phương pháp tạm thời đề xuất |
| 7 | [Sản phẩm — chức năng, so sánh và miền áp dụng](https://app.notion.com/p/3fe486d98ebc813687efdb0e6e9b5ae6) | 8 · Product |

## Nguồn của nội dung

Không có số đo hay lập luận mới. Trang chính và bảy trang con được dựng từ ba hồ sơ đã có trong repo:

| Nguồn trong repo | Dùng cho |
|---|---|
| [outline-2026-10-19.md](../outline-2026-10-19.md) | Khung tám mục, và **phần lớn chi tiết của bảy trang con** (Koren 2018, Zhang SVM 0,8955, bất biến hoán vị của PAP, 4,09% rò rỉ của Degformer, phân rã thang +0,0232/+0,0057/+0,0002, chín bước xử lý, bảng so sánh sản phẩm, 87,3% OOD, bốn câu không được nói) |
| [notion-2026-10-19/content.md](../notion-2026-10-19/content.md) | Mạch dẫn, bảng tiền lệ, công thức PSI/ΔPSI, bảng quy mô hai bộ, callout giới hạn |
| [notion-2026-10-19/visual-page-0.md](../notion-2026-10-19/visual-page-0.md) … [visual-page-3.md](../notion-2026-10-19/visual-page-3.md) | Văn phong thận trọng của bản trình bày cho giáo viên; đây cũng là **readback** của hai trang Trọng gửi (xem mục *Workspace* bên dưới) |

## Tám hình, và hai hình **bị loại theo yêu cầu**

Theo yêu cầu của Trọng, trang này **không dùng lại**:

- `visuals/biology.png` — "Sơ đồ khái niệm tự dựng: một con đường qua ubiquitin–proteasome";
- `visuals/mutation-map.gif` — "GIF minh họa giả định: A4V".

Các hình còn lại là file **đã có trong repo**, dùng lại từ các khối ảnh của
[trang lộ trình 19/10](../notion-2026-10-19/README.md) trong cùng workspace (không upload mới).

| Vị trí | Hình | Nguồn trong repo | Giấy phép / ghi công |
|---|---|---|---|
| Chính, mục 1 | `translation.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/translation.gif) | **CC BY-SA 3.0**, Tekksavvy — ghi công trong caption |
| Chính, mục 1 | `ubl-2qjl.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/ubl-2qjl.gif) | **CC BY-SA 3.0**, Hsp90 — caption gọi đúng là *protein nếp gấp ubiquitin* |
| Chính, mục 4 | `example-heatmap.png` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/example-heatmap.png), từ `measured-example.json` | Tự dựng từ **dữ liệu đo** (AGRN `O00468_AGRN_82`) |
| Chính, mục 7 | `fig-benchmark.png` | [notion-2026-10-19/png/](../notion-2026-10-19/png/fig-benchmark.png) | Tự dựng từ JSON 18/10 |
| Con 3 | `fig-01-urgency-forest.png` | [notion-2026-10-16/png/](../notion-2026-10-16/png/fig-01-urgency-forest.png) ← `variant-coverage-2026-10-15/enrichment.json` | Tự dựng. ClinVar: ghi công PMID 29165669 + câu phủ nhận chẩn đoán, có trên trang |
| Con 4 | `grid-schematic.png` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/grid-schematic.png) | Tự dựng; caption ghi rõ **sơ đồ minh hoạ, không phải dữ liệu đo** |
| Con 5 | `gfp-small.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/gfp-small.gif) | **CC BY-SA 4.0**, Erik A. Rodriguez — bản **đã chỉnh sửa**, caption ghi rõ |
| Con 6 | `fig-benchmark.png` · `fig-degformer.png` | [notion-2026-10-19/png/](../notion-2026-10-19/png/) | Tự dựng từ JSON 18/10 |

Ngoài ra **bảy sơ đồ Mermaid** viết thẳng trong nội dung: mạch tám mục và pipeline xử lý (trang
chính); pipeline, chia cụm, nguồn thông tin, luồng sản phẩm (trang con).

⚠ **ShareAlike — điểm cần Trọng quyết**, giống cảnh báo của hai trang trước: ba GIF là CC BY-SA.
Trang đang **riêng tư** nên chưa phát sinh nghĩa vụ phân phối; chia sẻ ra ngoài thì phải rà lại
ShareAlike trước.

## Ràng buộc câu chữ đã áp dụng

Trang chính kết bằng mục **"Bốn câu không được nói"**, lấy nguyên từ
[outline-2026-10-19.md](../outline-2026-10-19.md):
[D-036](../../../../DECISIONS.md#d-036) (ClinVar là động lực; 2,148 là tuyên bố **mức vùng**, mức
residue chưa thiết lập được, AUC 0,5166), [D-035](../../../../DECISIONS.md#d-035) (degron tự trị,
biến thể dòng mầm; không nói "đột biến lái ung thư"),
[D-032](../../../../DECISIONS.md#d-032) (không nói "chưa ai làm" — Degformer **đã** xuất ma trận
28×20), [C-17](../../../../DECISIONS.md#c-17) (**thang lân cận ±3** thắng **thang cả peptide**),
[D-031](../../../../DECISIONS.md#d-031) (0,9519 là **trần đo lường**; MDE 0,0123 chỉ cho một cặp so
sánh). Mục 7 và trang con 6 nói thẳng **G2 chưa hoàn tất**.

⚠ Bố cục tám mục **không có chỗ** cho "kế hoạch các tuần" và "câu hỏi cho GVHD" — nếu buổi trình bày
cần xin duyệt khung ([C-5](../../../../DECISIONS.md#c-5)) thì phải thêm lại hoặc nói miệng sau mục 8.
Cảnh báo này lấy từ [outline-2026-10-19.md](../outline-2026-10-19.md).

## Workspace — chỗ cần lưu ý

Hai link Trọng gửi (`3fe4c97e…`, `9704c97e…`) nằm ở **workspace Notion khác** với kết nối của phiên
này (`ngthtrong`, `ae23eae2…`). Đã thử lại sau khi Trọng chia sẻ access và mở "anyone with link":
vẫn `object_not_found` — kết nối Notion gắn theo **một workspace**, không đọc được trang ở workspace
khác dù link công khai (fetch trang công khai qua HTTP cũng không được vì Notion render bằng JS).

Vì vậy nội dung được dựng từ **bản readback trong repo** của chính hai trang đó
([visual-page-0.md](../notion-2026-10-19/visual-page-0.md) … `visual-page-3.md`) cộng với
[outline-2026-10-19.md](../outline-2026-10-19.md), và trang mới nằm trong workspace `ngthtrong` —
cùng chỗ với các trang `3fe486d9…` ghi trong
[resources/README.md](../../../../resources/README.md). Muốn trang kết hợp nằm cạnh hai trang kia
thì phải bật kết nối Notion cho workspace đó rồi dựng lại.
