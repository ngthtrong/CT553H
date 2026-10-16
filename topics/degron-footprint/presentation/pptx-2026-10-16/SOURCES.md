# Nguồn thiết kế, GIF và hình trong bản PPTX

Tra cứu ngày **15/10/2026**. Hồ sơ sản xuất, không ghi quyết định nghiên cứu ([DECISIONS.md](../../../../DECISIONS.md)). Yêu cầu của Trọng: **không dùng lại mẫu slide đã có trong repo** (Quarto Clean, reveal.js White, SlidesCarnival "Biology Thesis" và engine HTML riêng của hai deck kia).

## Mẫu / khuôn thiết kế đã tra (khác các mẫu trong repo)

| Nguồn | Mức đã kiểm | Cách vận dụng |
|---|---|---|
| [Assertion-evidence approach — Michael Alley, Penn State](https://www.assertion-evidence.com/) (mẫu PowerPoint tại [craftscicom.org/ae_templates](http://www.craftscicom.org/ae_templates.html)) | Mở trang chủ, xác nhận có mục *Templates* và *A-E Tutorial*. **Không tải template**, chưa đọc điều khoản dùng | **Chỉ vận dụng nguyên tắc**: tiêu đề là một câu khẳng định, phần còn lại là bằng chứng hình/bảng thay vì gạch đầu dòng. Không sao chép layout hay tài nguyên |
| [Beamer *metropolis* (Matthias Vogelgesang / mtheme)](https://trybibby.com/latex/template/beamer-metropolis) | Chỉ đọc kết quả tìm kiếm và trang giới thiệu. ⚠ **Hai nguồn ghi giấy phép khác nhau** (MIT so với CC-BY-SA-4.0); `LICENSE` ở GitHub trả 404 khi thử, **chưa xác minh** | **Chỉ vận dụng ý tưởng**: nền tối cho slide mở đầu, tiêu đề lớn, thanh tiến độ là điểm nhấn duy nhất, tối giản. Thanh tiến độ ở đây là hàng mười **ô residue** của riêng đề tài. Không dùng mã hay font Fira |

Không dùng template `.pptx` tải về nên không có ghi công mẫu. Toàn bộ bố cục được viết trực tiếp bằng [lib.py](lib.py) / [comp.py](comp.py).

## GIF (Wikimedia Commons, tra qua API ngày 15/10/2026)

Tìm theo `proteasome`, `ubiquitin`, `protein folding`, `GFP`, `ribosome`, `DNA`, `hemoglobin`, … Loại bỏ hai GIF đã dùng ở deck ngoài (`Protein translation.gif`, `1chc animated.gif`). **Không có GIF proteasome/E3 hay degron nào trên Commons**; animation cơ chế UPS ở slide 4 tự dựng bằng hình khối.

| Tệp (slide) | Tác giả · giấy phép | Nguồn · SHA-256 | Phạm vi đúng |
|---|---|---|---|
| [translation.gif](assets/translation.gif) · slide 2 | **Tekksavvy**, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) | [File:Protein synthesis (Translation).gif](https://commons.wikimedia.org/wiki/File:Protein_synthesis_(Translation).gif) · `dfc2162aa567…` (nguyên byte) | Ribosome nối acid amin thành chuỗi: minh họa "protein là chuỗi residue". Không phải đo đạc |
| [ubl-2qjl.gif](assets/ubl-2qjl.gif) · slide 4 | **Hsp90**, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) | [File:2qjl animated.gif](https://commons.wikimedia.org/wiki/File:2qjl_animated.gif) · `f9e2e64ebd69…` (nguyên byte) | **URM1** (PDB 2QJL), protein **họ giống ubiquitin** (nếp β-grasp). Caption ghi đúng là "ubiquitin-fold protein", **không** gọi là ubiquitin hay E3 người |
| [gfp-small.gif](assets/gfp-small.gif) · slide 7 | **Erik A. Rodriguez** (Commons: *Erin Rod*), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [File:GFP Fluorescent Protein Movie.gif](https://commons.wikimedia.org/wiki/File:GFP_Fluorescent_Protein_Movie.gif) (UCSF Chimera, PDB 1EMA) · bản gốc 24,6 MB, SHA `8607c57c2b9b…` · **bản dùng** `3f155b439381…` | GFP, reporter của assay GPS. **Đã chỉnh sửa**: thu nhỏ 600×766 → 300×383 và lấy một khung trong ba (187 → 63 khung). Caption ghi "reduced size and frame rate"; bản chỉnh sửa **kế thừa CC BY-SA 4.0** (ShareAlike) |

Ba GIF chỉ nằm trong thư mục này và trong file `.pptx`. **Không** dùng chung với phần còn lại của luận văn khi chưa xử lý điều khoản ShareAlike. Ba GIF chạy ở chế độ Slide Show; đã mở bằng Pillow để đếm khung và xem khung mẫu.

## Hình khác

| Hình | Nguồn |
|---|---|
| Slide 10, hình giữa | [`voutsinos2026-f4.jpg`](../../../../lectures/degron-footprint/assets/figures/voutsinos2026-f4.jpg), Voutsinos et al., *Sci Adv* 2026, DOI 10.1126/sciadv.adz3483, **CC BY-NC 4.0**; caption ghi tác giả, DOI, giấy phép ([NOTICE.md](../../../../lectures/degron-footprint/assets/figures/NOTICE.md)) |
| Slide 16, heatmap + thanh theo vị trí | **Dữ liệu đo**, `O00468_AGRN_82`, từ [measured-example.json](../deck-external-2026-10-16/assets/measured-example.json) (SHA-256 `db0fc13e…`, 532 ô); vẽ bằng [figs.py](figs.py). Vòng tròn / khung chữ nhật quanh ô và hàng là hình khối pptx dựng ở toạ độ tính từ bố cục hình |
| Slide 7, 15 (thang màu), 15 (lưới) | Tự dựng, `own diagram`: lưới 28×20 ở slide 15 là **sơ đồ, không có số** (các ô tô màu là minh hoạ vị trí, không phải dữ liệu) |
| Mọi sơ đồ còn lại | Tự dựng bằng hình khối pptx; bản chất minh họa, nhãn `own diagram` / `proposed, not built` theo brief |

Không sao chép hình từ Zhang 2023 (Elsevier, bảo lưu quyền) hay Larsen 2025 (CC BY-NC-**ND**).

## Chỗ lệch khỏi brief (có chủ ý)

| Chỗ | Brief | Bản PPTX | Lý do |
|---|---|---|---|
| Slide 16, "peptide trong tập train" | chọn peptide train | peptide bão hòa nằm phía **đánh giá**; ghi rõ là minh họa nhãn đo | Thiết kế cross-source hiện hành ([D-031](../../../../DECISIONS.md#d-031)); cùng cách xử lý như exporter của deck ngoài |
| Slide 17, "Committed in advance" | MDE 0,0123 cho bộ bão hòa nói chung | gắn với cặp ghép **M3 − M0**; phép so mới ước lượng lại | [CLAUDE.md](../../../../CLAUDE.md): không biến MDE của một phép so thành ngưỡng nghiệm thu chung |
| Slide 18, ô Larsen | "MIT (data file)" | "MIT in repo; coverage of the data file awaiting author reply" | [C-11a](../../../../DECISIONS.md#c-11a) còn chờ |
| Slide 25, nhãn G1/G2/G3 | "Gate" | "readiness check (internal)" | Ghi chú sản xuất của brief: ba cổng là khung nội bộ, không phải của học phần |
| Slide 26, Q1 và Q4 | văn bản cũ | hai ô giữ chỗ | Việc 9 của brief: Trọng tự viết |
| Slide 8, cột "Prediction unit" | icon thay chữ | chữ; tô nền theo nhóm phương pháp | Không có icon bản quyền sạch; bảng đủ rõ |
| Slide 23, hình luồng và slide 24, sơ đồ harness | hình riêng | gộp vào slide, viền nét đứt hổ phách `[proposed, not built]` | Giữ 26 slide đúng mục lục |
| Ký tự `✓ △ ⇒` | trong brief | đổi sang `● ▲ →` | Calibri không có ba ký tự đầu; tránh ô vuông trên máy không có font dự phòng |
