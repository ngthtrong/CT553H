# Trang Notion lộ trình đề tài — 19/10/2026

> **Bổ sung trực quan:** [VISUALS.md](VISUALS.md) ghi nguồn, sơ đồ/GIF mới, ảnh dữ liệu dùng lại và kiểm tra. Bản readback mới nhất: [trang chính](visual-page-0.md), [residue](visual-page-1.md), [dataset](visual-page-2.md), [kết quả](visual-page-3.md).

> **Bản đang dùng để trình bày ý tưởng với giáo viên:** [Notion](https://app.notion.com/p/3fe4c97ef69581ed968df52b445de084) · [nguồn trang chính](advisor-overview.md). Đã mở rộng chín phần và bổ sung chiều sâu cho ba trang con theo phản hồi của Trọng. Các URL `3fe486…` phía dưới là hồ sơ phiên trước; chúng trả NOT_FOUND ở kết nối hiện tại. `published-concise.md` giữ bản cô đọng trước khi mở rộng. Trạng thái chính thức vẫn theo `DECISIONS.md`.

Trang Notion **tiếng Việt** dùng như một **khung lộ trình để follow**: chín mục theo đúng thứ tự
lập luận của đề tài, mỗi mục kết bằng một câu hỏi bắc cầu; chi tiết đẩy xuống **ba trang con**.
Soạn theo yêu cầu của Trọng ngày 19/10/2026. Hồ sơ sản xuất, **không ghi quyết định**
([DECISIONS.md](../../../../DECISIONS.md)).

| | |
|---|---|
| **Trang chính** | <https://app.notion.com/p/3fe486d98ebc81fc9ac2c4794a452cd3> — **riêng tư (draft)**, chưa đặt dưới trang cha |
| **Trang con 1** | [Vì sao cần dự đoán hiệu ứng đột biến ở mức residue?](https://app.notion.com/p/3fe486d98ebc815e9314c3076cd76ff2) |
| **Trang con 2** | [Dataset và quá trình xử lý](https://app.notion.com/p/3fe486d98ebc8139819dd8682a49c8ef) |
| **Trang con 3** | [Kết quả hiện tại, đối chứng và chỗ còn hở](https://app.notion.com/p/3fe486d98ebc81b18331cf1c39b852b4) |
| **Bản nguồn trong repo** | [content.md](content.md) |
| **Script sinh biểu đồ** | [figures.py](figures.py) → [png/](png/) |
| **Căn cứ nội dung** | [DECISIONS.md phần A](../../../../DECISIONS.md#hien-hanh), [D-031](../../../../DECISIONS.md#d-031), [D-033](../../../../DECISIONS.md#d-033), [D-035](../../../../DECISIONS.md#d-035), [D-036](../../../../DECISIONS.md#d-036); kết quả 18/10 ở [g2-saturation](../../research/g2-saturation-2026-10-18/README.md) và [g2-extension](../../research/g2-extension-2026-10-18/README.md) |

⚠ **Notion và repo không tự đồng bộ.** `content.md` là bản đọc được trong repo; trang Notion là
bản đã dựng. Sửa một bên thì phải sửa bên kia bằng tay.

## Khác gì [trang Notion 16/10](../notion-2026-10-16/README.md)?

Trang 16/10 là **bản tóm tắt tiếng Anh một màn hình cuộn**. Trang này là **lộ trình tiếng Việt
có trang con**, mục đích khác: follow theo từng bước thay vì đọc một lượt. **Cả hai cùng tồn
tại**; trang 16/10 **không bị thay thế**, nhưng hình `fig-03-g2-target.png` của nó **đã lạc hậu**
(nó vẽ M3 chuyển giao 0,7273, trước kết quả học trực tiếp 0,8082 ngày 18/10). Trang 19/10 dùng
hình mới dựng từ JSON 18/10.

## Dựng lại hai biểu đồ

```bash
.venv/bin/python topics/degron-footprint/presentation/notion-2026-10-19/figures.py
```

Mọi con số đọc trực tiếp từ JSON kết quả trong [research/](../../research/); hằng số duy nhất
viết tay trong script là **trần đo lường 0,9519** (`residue-task-derisk-2026-10-15/ceiling.json`),
có tên và chú nguồn ở đầu file.

## Tám hình trên ba trang

| Trang | Hình | Nguồn trong repo | Giấy phép / ghi công |
|---|---|---|---|
| Chính, mục 1 | `translation.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/translation.gif) · [Commons](https://commons.wikimedia.org/wiki/File:Protein_synthesis_(Translation).gif), Tekksavvy | **CC BY-SA 3.0** — ghi công trong caption |
| Chính, mục 1 | `ubl-2qjl.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/ubl-2qjl.gif) · [Commons](https://commons.wikimedia.org/wiki/File:2qjl_animated.gif), Hsp90 — PDB 2QJL | **CC BY-SA 3.0** — caption gọi đúng là *protein nếp gấp ubiquitin*, không gọi là ubiquitin người |
| Chính, mục 3 | `fig-01-urgency-forest.png` | [notion-2026-10-16/png/](../notion-2026-10-16/png/fig-01-urgency-forest.png) ← `variant-coverage-2026-10-15/enrichment.json` | Tự dựng. ClinVar: ghi công PMID 29165669 + câu phủ nhận chẩn đoán, có trên trang |
| Chính, mục 5 | `example-heatmap.png` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/example-heatmap.png), từ `measured-example.json` | Tự dựng từ **dữ liệu đo** |
| Con 1 | `grid-schematic.png` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/grid-schematic.png) | Tự dựng; caption ghi rõ **sơ đồ minh hoạ, không phải dữ liệu đo** |
| Con 2 | `gfp-small.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/gfp-small.gif) · [Commons](https://commons.wikimedia.org/wiki/File:GFP_Fluorescent_Protein_Movie.gif), Erik A. Rodriguez | **CC BY-SA 4.0** — bản **đã chỉnh sửa** (thu nhỏ, giảm khung); caption ghi rõ |
| Con 3 | `fig-benchmark.png` | [png/](png/fig-benchmark.png) ← `g2-saturation-2026-10-18/`, `g2-extension-2026-10-18/` | Tự dựng, **mới 19/10** |
| Con 3 | `fig-degformer.png` | [png/](png/fig-degformer.png) ← `g2-extension-2026-10-18/e1-overlap.json`, `e3-degformer-arch.json` | Tự dựng, **mới 19/10** |

Ngoài ra hai sơ đồ **Mermaid** (lộ trình 9 bước ở trang chính; pipeline 7 bước ở trang con 2)
viết thẳng trong nội dung trang, không phải file ảnh.

⚠ **ShareAlike / NC — điểm cần Trọng quyết, giống [cảnh báo của trang 16/10](../notion-2026-10-16/README.md).**
Ba GIF là CC BY-SA. Trang đang ở chế độ **riêng tư** nên chưa phát sinh nghĩa vụ phân phối; nếu
chia sẻ ra ngoài thì phải rà lại điều khoản ShareAlike trước. Đã bù sẵn bằng ghi công + tên giấy
phép ngay trong caption từng hình.

## Ràng buộc câu chữ đã áp dụng

Trang bám đúng các câu cấm đang hiệu lực, và liệt kê chúng ra mặt trang ở mục cuối
**“Đề tài không tuyên bố điều gì”**:

- [D-036](../../../../DECISIONS.md#d-036): ClinVar là **động lực**, không phải đích xác nhận;
  cấm nói “residue đề tài dự đoán là residue mang tín hiệu bệnh”; con số 2,148 là tuyên bố
  **mức vùng**, mức residue thì chưa thiết lập được (AUC 0,5166 [0,479; 0,554]).
- [D-033](../../../../DECISIONS.md#d-033): 2,148 luôn đi kèm hai kết quả âm và chỗ chưa khử
  bảo tồn / vô trật tự.
- [D-035](../../../../DECISIONS.md#d-035): phạm vi **degron tự trị**, biến thể **dòng mầm**.
- [C-17](../../../../DECISIONS.md#c-17): nói **“thành phần ở thang lân cận ±3 thắng thành phần ở
  thang cả peptide”**, không nói “vị trí thắng thành phần”.
- [D-031](../../../../DECISIONS.md#d-031): trần 0,9519 là **trần đo lường**; MDE 0,0123 là ước
  lượng của **một cặp so sánh**, không phải ngưỡng nghiệm thu chung.
- **G2 chưa hoàn tất** — mục 8 và trang con 3 nói thẳng mốc số đã vượt nhưng điều kiện kiến
  trúc thì chưa.

## Nguồn nội dung

Mạch chín bước và nội dung hai trang con 1–2 do **Trọng soạn** và paste vào phiên 19/10/2026;
Claude chỉ dựng trang, chèn hình/sơ đồ/liên kết và đối soát số với `research/`.
**Trang con 3 là phần Claude thêm** (chưa có trong brief của Trọng) để đỡ cho mục 7–8, dựng
hoàn toàn từ JSON kết quả 18/10 — nếu không muốn giữ thì xoá riêng trang đó, lộ trình vẫn đủ.
