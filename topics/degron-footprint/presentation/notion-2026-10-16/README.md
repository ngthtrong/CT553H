# Trang Notion tóm tắt đề tài — 16/10/2026

Trang Notion **tiếng Anh**, một màn hình cuộn, ưu tiên hình ảnh / GIF / biểu đồ thay vì chữ.
Soạn theo yêu cầu của Trọng ngày 16/10/2026. Hồ sơ sản xuất, **không ghi quyết định**
([DECISIONS.md](../../../../DECISIONS.md)).

| | |
|---|---|
| **Trang Notion** | <https://app.notion.com/p/3fb486d98ebc81b382abc2df429660d8> — **riêng tư (draft)**, chưa đặt dưới trang cha nào |
| **Bản nguồn trong repo** | [content.md](content.md) |
| **Script sinh biểu đồ** | [figures.py](figures.py) → [png/](png/) |
| **Căn cứ nội dung** | [DECISIONS.md phần A](../../../../DECISIONS.md#hien-hanh), [D-031](../../../../DECISIONS.md#d-031), [D-033](../../../../DECISIONS.md#d-033)…[D-036](../../../../DECISIONS.md#d-036); brief [slide-content-2026-10-15.md](../slide-content-2026-10-15.md) |

⚠ **Notion và repo không tự đồng bộ.** `content.md` là bản đọc được trong repo; trang Notion
là bản đã dựng. Sửa một bên thì phải sửa bên kia bằng tay.

## Dựng lại

```bash
.venv/bin/python topics/degron-footprint/presentation/notion-2026-10-16/figures.py
```

Sinh lại cả bốn PNG trong `png/`. Mọi con số đọc trực tiếp từ file kết quả trong
[research/](../../research/); bốn mốc bị khoá bởi quyết định (`0.7693`, `0.9519`, `0.0123`,
`+0.0300`) là hằng số có tên ở đầu script, nguồn ghi ở bảng dưới.

## Chín hình trên trang

| # | Hình | Nguồn | Giấy phép / ghi công |
|---|---|---|---|
| 1 | `translation.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/translation.gif) · [Commons](https://commons.wikimedia.org/wiki/File:Protein_synthesis_(Translation).gif), Tekksavvy | **CC BY-SA 3.0** — ghi công trong caption |
| 2 | `ubl-2qjl.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/ubl-2qjl.gif) · [Commons](https://commons.wikimedia.org/wiki/File:2qjl_animated.gif), Hsp90 — URM1, PDB 2QJL | **CC BY-SA 3.0** — caption gọi đúng là *ubiquitin-fold protein*, không gọi là ubiquitin người |
| 3 | `gfp-small.gif` | [pptx-2026-10-16/assets/](../pptx-2026-10-16/assets/gfp-small.gif) · [Commons](https://commons.wikimedia.org/wiki/File:GFP_Fluorescent_Protein_Movie.gif), Erik A. Rodriguez | **CC BY-SA 4.0** — bản **đã chỉnh sửa** (thu nhỏ, giảm khung); caption ghi rõ |
| 4 | `example-heatmap.png` | [pptx-2026-10-16/figs.py](../pptx-2026-10-16/figs.py), từ `measured-example.json` | Tự dựng từ **dữ liệu đo** (HIF1A tile 25, `Q16665`, 529 ô) |
| 5 | `fig-01-urgency-forest.png` | [figures.py](figures.py) ← `variant-coverage-2026-10-15/enrichment.json` | Tự dựng. ClinVar: ghi công PMID 29165669 + câu phủ nhận chẩn đoán, có trên trang |
| 6 | `voutsinos2026-f4.jpg` | [lectures/degron-footprint/assets/figures/](../../../../lectures/degron-footprint/assets/figures/NOTICE.md) | **CC BY-NC 4.0** — Voutsinos 2026, DOI 10.1126/sciadv.adz3483, ghi công trong caption |
| 7 | `fig-02-scale-decomposition.png` | [figures.py](figures.py) ← `residue-task-derisk-2026-10-15/model.json` | Tự dựng |
| 8 | `fig-03-g2-target.png` | [figures.py](figures.py) ← `model.json`, `ceiling.json` | Tự dựng |
| 9 | `fig-04-roadmap.png` | [figures.py](figures.py) | Tự dựng; **suy ra** từ D-029 + D-031 + D-033, chưa phải một quyết định riêng |

⚠ **ShareAlike — điểm cần Trọng quyết.** [SOURCES.md của bản PPTX](../pptx-2026-10-16/SOURCES.md)
ghi: *“Ba GIF chỉ nằm trong thư mục này và trong file `.pptx`. Không dùng chung với phần còn
lại của luận văn khi chưa xử lý điều khoản ShareAlike.”* Trang Notion này là **một bề mặt mới**
ngoài phạm vi đó. Đã bù bằng ghi công + tên giấy phép ngay dưới mỗi hình và một bảng nguồn ở
cuối trang, và trang đang ở chế độ **riêng tư**, nên chưa phát sinh nghĩa vụ phân phối. Nếu chia
sẻ trang ra ngoài thì phải rà lại điều khoản ShareAlike (và CC BY-**NC** của hình 6) trước.

## Cách dựng biểu đồ

Bốn biểu đồ dựng bằng **matplotlib**, không đặt toạ độ SVG bằng tay (yêu cầu của Trọng,
16/10/2026). Dạng hình chọn theo việc của dữ liệu: forest plot cho khoảng tin cậy, thanh xếp
chồng cho phân rã một tổng, thanh ngang có vạch mốc cho so với đích, và Gantt cho lịch.

Bảng màu lấy nguyên từ brief slide ([slide-content-2026-10-15.md](../slide-content-2026-10-15.md)):
nền `#FAFBFC`, chữ `#15323F`, degron/bất ổn định `#D1495B`, bền `#2A9D8F`, mô hình `#386FA4`,
trung tính `#8FA3AD`, cảnh báo `#E9C46A`. Font Calibri nếu có, nếu không thì DejaVu Sans
(Calibri thiếu `✓ ⚠ □`, nên các nhãn đó viết bằng chữ).

⚠ **Đã chạy validator màu của skill `dataviz` trên năm màu này:** FAIL hai mục
(`#E9C46A` ngoài dải độ sáng, `#8FA3AD` dưới sàn chroma) và WARN tách màu CVD cho cặp
`#2A9D8F ↔ #D1495B` (ΔE 7,7 deutan). **Không đổi bảng màu** vì đây là quy ước đã áp dụng cho
cả ba deck; bù bằng điều kiện mà chính validator đòi: **mọi mark đều có nhãn số trực tiếp**,
khe nền 2 px giữa các đoạn xếp chồng, và amber/xám chỉ dùng làm màu trạng thái kèm chữ, không
làm màu chuỗi dữ liệu. Nếu sau này muốn một bảng màu đạt validator thì đó là một quyết định
trình bày riêng, phải ghi vào `DECISIONS.md`.

## Ràng buộc câu chữ đã áp dụng

Trang bám đúng các câu cấm đang hiệu lực; mục **“What this work does not claim”** liệt kê bảy
câu đó ra mặt trang, không giấu xuống cuối:

- [D-036](../../../../DECISIONS.md#d-036): ClinVar là **động lực**, không phải đích xác nhận; không
  nói “residue đề tài dự đoán là residue mang tín hiệu bệnh”; không trích AUC 0,674 rời CI.
- [D-033](../../../../DECISIONS.md#d-033): con số **2,148** luôn đi kèm hai kết quả âm và chỗ chưa
  khử bảo tồn / vô trật tự.
- [D-035](../../../../DECISIONS.md#d-035): phạm vi **degron tự trị**, biến thể **dòng mầm**; bỏ mạch
  “đột biến lái ung thư”.
- [C-17](../../../../DECISIONS.md#c-17): nói **“thành phần ở thang lân cận ±3 thắng thành phần ở
  thang cả peptide”**, không nói “vị trí thắng thành phần”.
- Degformer giữ trong trang như **baseline chính thức phải vượt**, không bỏ ra.

Trang **không** nêu: bốn hướng đã bị loại bằng số, tranh luận nội bộ về mức đóng góp, lịch sử các
lần đổi hướng, và việc đề tài không có dự phòng — cùng ranh giới “giữ tối thiểu” như brief slide.
