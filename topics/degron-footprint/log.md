# Nhật ký đề tài `degron-footprint`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../DECISIONS.md).

---

## 16/10/2026 — trang Notion tóm tắt đề tài (tiếng Anh, ưu tiên hình)

Theo yêu cầu Trọng: soạn **một trang Notion cô đọng, chỉ thông tin cốt lõi, ưu tiên hình ảnh / GIF / sơ đồ thay vì chữ**; trong phiên Trọng đổi sang **tiếng Anh** và yêu cầu **dựng biểu đồ bằng code/thư viện, không đặt toạ độ SVG bằng tay**. Sản phẩm: [notion-2026-10-16](presentation/notion-2026-10-16/README.md) và trang <https://app.notion.com/p/3fb486d98ebc81b382abc2df429660d8> (riêng tư). Không đo mới, không huấn luyện, không đổi quyết định nghiên cứu. Không đọc hay sửa `deck-2026-10-16/` và `pptx-2026-10-16/` (chỉ **dùng lại** ba GIF, `example-heatmap.png` và hình Voutsinos Fig. 4 đã có).

- **Chín hình, mười mục chữ ngắn.** Ba GIF Commons (dịch mã · protein họ ubiquitin PDB 2QJL · GFP reporter), ma trận ΔPSI **đo thật** của HIF1A tile 25, hình PAP của Voutsinos 2026, và **bốn biểu đồ mới** dựng bằng **matplotlib**: forest plot OR 2,148/2,094 · thanh xếp chồng phân rã +0,0289 (±3 composition 80% · thứ tự 20% · vị trí tuyệt đối ≈ 0) · thanh ngang G2 (M0 0,7071 · M3 0,7273 · đích 0,7693 · trần 0,9519) · Gantt tuần 6→15 có điểm kiểm cứng tuần 10.
- **Số đọc từ file kết quả, không gõ tay:** [figures.py](presentation/notion-2026-10-16/figures.py) nạp `variant-coverage-2026-10-15/enrichment.json` và `residue-task-derisk-2026-10-15/model.json`; bốn mốc bị khoá bởi quyết định là hằng số có tên, nguồn ghi trong README của thư mục.
- **Lần đầu viết SVG tay rồi bỏ:** bản dựng đầu đặt toạ độ SVG trực tiếp và dính một lỗi thật — `.replace(".", ",")` áp lên cả chuỗi chứa toạ độ làm `x1="689.4"` thành `x1="689,4"`, vẽ vạch CI từ mép trái. Sau khi Trọng yêu cầu dùng thư viện thì lỗi loại này không còn chỗ phát sinh.
- **Ràng buộc câu chữ:** trang có hẳn một mục **“What this work does not claim”** liệt kê bảy câu cấm ([D-033](../../DECISIONS.md#d-033), [D-035](../../DECISIONS.md#d-035), [D-036](../../DECISIONS.md#d-036), [C-17](../../DECISIONS.md#c-17)); con số 2,148 luôn đi kèm ba giới hạn; ClinVar ghi vai **motivation only**; Degformer giữ làm baseline phải vượt.
- ⚠ **Hai điểm cần Trọng biết.** (1) **ShareAlike:** [SOURCES.md của bản PPTX](presentation/pptx-2026-10-16/SOURCES.md) ghi ba GIF *“không dùng chung với phần còn lại của luận văn khi chưa xử lý điều khoản ShareAlike”*; trang Notion là bề mặt mới, hiện **riêng tư** và đã ghi công đầy đủ, nhưng chia sẻ ra ngoài thì phải rà lại (cùng với CC BY-**NC** của hình Voutsinos). (2) **Bảng màu của repo trượt validator màu** của skill `dataviz` (amber ngoài dải độ sáng, xám dưới sàn chroma, cặp teal↔đỏ ΔE 7,7 deutan); giữ nguyên vì là quy ước chung ba deck, bù bằng nhãn số trực tiếp trên mọi mark — đổi bảng màu sẽ là một quyết định trình bày riêng.

---

## 15/10/2026 — script Việt–Anh và tài liệu đọc hiểu cho 26 slide

Theo yêu cầu Trọng, đọc đủ **năm phần paste** của `index.html` trong `deck-2026-10-16/`; bản ghép khớp file repo khi bỏ khoảng trắng. Soạn [speaker-script-bilingual.md](presentation/deck-2026-10-16/speaker-script-bilingual.md): mỗi slide có thông điệp, lời nói VI/EN, giải thích, hỏi đáp và nguồn; thêm bảng thuật ngữ, câu tự kiểm và bảng đối soát nguồn. Không điền câu trả lời vào hồ sơ đánh giá học tập.

- **Đối soát đáng chú ý:** PAP Spearman **0,3553 là mức ô**, còn mức vị trí ghi **0,4130** trong `pap-baseline.json`; không dùng cặp 0,4440/0,3553 để tuyên bố đảo hạng. Delta scanning **+0,0300** dùng tập chung 2.064 peptide (M3 0,8657 / PAP 0,8357), khác tập của M3 0,8682. **87,3%** tính theo cụm (13.814/15.819), MDE 0,0123 thuộc cặp M3−M0, xác nhận Larsen vẫn chờ C-11a. Script nêu các giới hạn này; người soạn script không sửa HTML. Khi rà cuối thấy HTML đã đổi phần chữ/nhãn M7V→A7V ở slide 2; lời nói đã dùng A7V.
- **Giới hạn biên soạn:** số minh họa slide 12 chưa gắn định danh không được coi là phép đo; bảng công cụ không chuyển “chưa kiểm” thành “không có”. Q1/Q4 slide 26 vẫn chờ Trọng hoàn thiện. Không có khảo sát web, benchmark, huấn luyện hay quyết định mới.
- **Kiểm cuối:** đủ 26 mục slide với lời nói VI/EN, đọc hiểu và Q&A; **119 link/fragment mới** trong năm file đều hợp lệ; Pandoc chuyển thành HTML đủ 26 anchor slide, 8 bảng, 78 mục ngôn ngữ/đọc hiểu; đối chiếu số HIF1A, cấp metric PAP và delta ghép cặp với JSON; `git diff --check` trong phạm vi đạt. Không sửa `index.html`, CSS/JS hoặc `DECISIONS.md`.

---

## 15/10/2026 — dựng slide PowerPoint `deck-pptx-2026-10-16/` (26 slide + 2 phụ lục, GIF, animation)

Theo yêu cầu Trọng: **tìm mẫu slide (không dùng lại mẫu trong repo) → tìm GIF → tạo animation → dựng slide từ [brief](presentation/slide-content-2026-10-15.md), định dạng `.pptx`, không phải deck HTML** ([D-037](../../DECISIONS.md#d-037)). Không đo mới, không huấn luyện, không đổi quyết định nghiên cứu. Sản phẩm: [deck-pptx-2026-10-16](presentation/deck-pptx-2026-10-16/README.md). Không đọc, sửa hay ghi `deck-2026-10-16/` và `deck-external-2026-10-16/` (chỉ **đọc** file [measured-example.json](presentation/deck-external-2026-10-16/assets/measured-example.json) làm đầu vào cho slide 16).

- **Mẫu:** Quarto Clean, reveal.js White và SlidesCarnival đã dùng ở repo nên **loại**. Tra thêm *assertion–evidence* (Alley, Penn State) và Beamer *metropolis*; chỉ vận dụng **nguyên tắc** (tiêu đề là câu khẳng định, nền tối cho slide mở đầu, thanh tiến độ tối giản), không tải mẫu. ⚠ Giấy phép metropolis có hai nguồn mâu thuẫn, chưa xác minh. Bố cục viết bằng `python-pptx` ([lib.py](presentation/deck-pptx-2026-10-16/lib.py)).
- **GIF (Commons, tra qua API):** ba GIF **mới** so với deck ngoài, **CC BY-SA** — dịch mã (slide 2), URM1 họ ubiquitin (slide 4; ghi đúng là *ubiquitin-fold*, không phải E3), GFP reporter (slide 7; bản 24,6 MB được **thu nhỏ** còn 1 MB). **Không có GIF proteasome/E3/degron nào** trên Commons, nên cơ chế UPS dựng bằng hình khối. Ghi công, SHA-256 và điều khoản ShareAlike ở [SOURCES.md](presentation/deck-pptx-2026-10-16/SOURCES.md).
- **Animation:** hiệu ứng *fade* theo bấm chuột, viết thẳng XML `p:timing` ([lib.py](presentation/deck-pptx-2026-10-16/lib.py)); **21 slide** có bước hiện dần (chuỗi → gập → M7V; E3 → ubiquitin → proteasome; phễu dữ liệu; cột AUROC bộ quét → bộ bão hòa → khoảng cách −0,0420; …). GIF chạy ở Slide Show.
- **Hình từ dữ liệu:** slide 16 là ma trận ΔPSI **đo** của `O00468_AGRN_82` (532 ô, 86/95 thay thế làm bền ở vị trí 15–19), dựng bằng [figs.py](presentation/deck-pptx-2026-10-16/figs.py). Ma trận bão hòa nằm **phía đánh giá** nên slide ghi là *minh họa nhãn đo*, không phải ví dụ huấn luyện.
- **Kiểm tra:** `validate.py` của skill pptx **PASSED**; quét chữ không còn câu cấm của brief (vị trí thắng thành phần, "nobody has", "validated against ClinVar", 0,6045 / 0,7792, …); 28 slide đều có ghi chú người nói. ⚠ **Chưa mở bằng PowerPoint thật, chưa phát thử animation**: máy không có LibreOffice. Bố cục xem bằng bộ vẽ lại tự viết ([render_preview.py](presentation/deck-pptx-2026-10-16/render_preview.py)), nên có thể lệch nhẹ so với PowerPoint. Ký tự `✓ △ ⇒` đổi thành `● ▲ →` vì Calibri không có.
- **Chỗ lệch brief có chủ ý** (bảng đầy đủ ở SOURCES.md): ô giấy phép Larsen ghi *đang chờ xác nhận* (C-11a); MDE 0,0123 gắn với cặp M3 − M0; G1–G3 gọi *readiness check*; Q1/Q4 slide 26 là **ô giữ chỗ**, Trọng tự viết (việc 9).
- **Việc tiếp theo (Trọng):** mở file một lần và bấm qua 26 slide; viết Q1/Q4; chọn một trong ba bản hoặc gộp.

## 15/10/2026 — dựng deck `deck-2026-10-16/` (26 slide, animation tự dựng, hình sinh từ dữ liệu)

Theo yêu cầu Trọng trong phiên: **tìm mẫu slide → tìm GIF → tạo animation → dựng slide từ
[brief](presentation/slide-content-2026-10-15.md)**, kèm hai ràng buộc Trọng nói giữa chừng:
**không dùng lại mẫu slide cũ** và **không đụng vào `deck-external-2026-10-16/`**. Không đo mới, không huấn
luyện, không ghi quyết định nghiên cứu mới. Sản phẩm: [deck-2026-10-16/](presentation/deck-2026-10-16/README.md).

- **Mẫu slide:** tra các framework HTML (reveal.js, Slidev, Marp, impress.js, Slipshow; mẫu khoa học của IPGP).
  **Không dùng cái nào** — reveal.js từ CDN cần mạng khi mở `file://`, và yêu cầu "không dùng lại mẫu cũ" loại
  cả `deck.json`/`slides/` lẫn `presentation.html`. Viết **engine riêng** ~190 dòng: sân khấu 16:9 cố định,
  bước animation theo `data-step`, panel ghi chú, bảng tổng quan, chế độ `?all`, in ra PDF.
- **GIF: tra xong và quyết định không dùng.** Tra Wikimedia Commons qua API cho `proteasome`, `ubiquitin`,
  `degron`, `E3 ligase`, `ubiquitination animation`, `flow cytometry sorting`, `protein folding`: **không có
  GIF nào vừa đúng chủ đề vừa có giấy phép dùng được**. Hai GIF tìm được là CC BY-SA 3.0 và sai nội dung.
  Nguồn animation UPS tốt đều không mở: HHMI BioInteractive (CC BY-NC-SA), WEHI.TV (xin phép từng lần),
  hình tạp chí (CC BY-NC-**ND**). ⇒ Animation **tự dựng bằng SVG + CSS**, đúng khuyến nghị của brief.
- **Hình sinh từ dữ liệu cho slide 16** (việc số 2 của brief, nay **xong**):
  [`research/slide-figures-2026-10-15/`](research/slide-figures-2026-10-15/README.md) — ma trận ΔPSI 28×20 **đo
  được** của `Q16665_HIF1A_25`, chọn bằng quy tắc cố định, kèm SHA-256 hai file đầu vào. Footprint rơi đúng
  **vị trí 10–14** = `L562-A563-P564-Y565-I566`, tức lõi **LXXLAP** mà VHL nhận diện; vị trí 12 có **19/19**
  thay thế đều làm bền, vị trí 23 là đối chứng âm (−0,31). ⚠ Mắt nối LXXLAP/P564 là **tra y văn**
  (PMID 11504942), đã gắn nhãn `literature cross-check` trên slide, **không** trình bày như phát hiện mới.
  ⚠ Cả 91 peptide bão hòa đều ở phía đánh giá nên không có peptide "trong tập train" như brief giả định;
  script **ghi rõ trạng thái split** thay vì giả định, và slide chỉ hiện nhãn đo nên không rò rỉ.
- **26 slide, 13 sơ đồ tự dựng + 2 hình tác giả** (Voutsinos 2026 Fig. 1 và Fig. 4, CC BY-NC 4.0, caption đủ
  tác giả/DOI/giấy phép). Chữ trên slide tiếng Anh, ghi chú người nói tiếng Việt kèm các câu cấm.
- **Ba lỗi kỹ thuật tìm ra khi soát bằng ảnh chụp thật**, đã sửa và đáng ghi vì dễ lặp lại:
  (1) quy tắc `[data-step][data-anim="…"]` đặt **sau** `[data-step].on` nên mọi khối có hướng bay **kẹt ở vị
  trí lệch** — SVG cắt mất chữ; (2) `code, .mono { font-size: .92em }` đè lên thuộc tính `font-size` của
  `<text>` trong SVG làm **mọi sơ đồ phóng to**; (3) `.cols` không khoá chiều cao hàng grid nên hình **tràn
  khỏi sân khấu**. Đã soát lại từng slide bằng Chrome headless ở chế độ `?all`.
- **Kiểm:** HTML cân bằng thẻ, 26 `<section>` / 26 ghi chú, mọi đường dẫn tài nguyên tồn tại, xuất PDF ra
  đúng **26 trang** 1280×720.
- **Chưa làm:** câu hỏi 1 và 4 của slide 26 vẫn **chờ Trọng viết** (bản hiện tại lấy từ brief, câu 1 đã thêm
  dòng xin ghi biên bản khung ba trụ); chưa đối chiếu lại từng ô bảng so sánh công cụ ở slide 23; chưa chạy
  đối chứng bảo tồn/vô trật tự cho con số 2,148. Nay `presentation/` có **hai** deck cho cùng buổi gặp —
  chọn một hoặc gộp là việc của Trọng.

---

## 15/10/2026 — dựng deck bên ngoài cho buổi gặp 16/10

Theo yêu cầu Trọng: tra mẫu ngoài repo, tìm GIF và tạo animation, dựng từ [brief](presentation/slide-content-2026-10-15.md) **chỉ trong [deck-external-2026-10-16/](presentation/deck-external-2026-10-16/README.md)**. Không đọc, sao chép hoặc ghi vào thư mục `deck-2026-10-16/` đang được Trọng chỉnh sửa. Không huấn luyện, chạy benchmark mới hay ghi quyết định nghiên cứu mới.

- **Thiết kế:** tra Quarto Clean của Grant McDermott (MIT), Reveal.js White (MIT) và Biology Thesis của SlidesCarnival; tham khảo Clean để viết bố cục HTML riêng, dùng Inter cục bộ. [SOURCES.md](presentation/deck-external-2026-10-16/SOURCES.md) ghi mức truy cập từng nguồn, giấy phép, những ứng viên không dùng và SHA tài nguyên.
- **Sản phẩm:** 26 slide chính + 7 phụ lục, tách nội dung thành 7 file; `index.html` nhỏ, chạy `file://` không cần mạng. Hai GIF Commons (dịch mã, domain RING) có ghi công và poster tĩnh; RING ghi rõ domain virus PDB 1CHC, không gọi là E3 người. SVG tự dựng cho gập chuỗi, cân bằng, UPS, zoom, forest plot, hoán vị PAP, so sánh benchmark, luồng xử lý và split cụm.
- **Nội dung:** giữ hai phía kết quả (+0,0300 bộ quét / −0,0420 bão hòa), G2 chưa đạt, A/B/C chưa chạy và phần mềm chưa xây. Q1/Q4 slide 26 chừa cho Trọng. Ghi chú trích brief có phần đối chiếu trước đoạn nguồn để không đưa chữ cũ lên slide.
- **Đồng bộ trạng thái:** sửa hai dòng cũ trong README vẫn gọi C-16/C-17 là đang chờ hoặc gọi `CTNNB1` là ứng viên hiện hành; chúng mâu thuẫn với [D-035](../../DECISIONS.md#d-035). Chỉ dẫn lại quyết định đã có, không tạo quyết định mới.
- **Đối chiếu khi dựng:** ví dụ AGRN là nhãn đo ở phía đánh giá, không gọi là mẫu train; MDE gắn cặp M3−M0 theo [D-031](../../DECISIONS.md#d-031); giấy phép Larsen vẫn chờ email theo [C-11a](../../DECISIONS.md#c-11a); bảng tính năng công cụ dùng “not documented / not checked” theo mức nguồn, không biến chưa kiểm thành vắng mặt. Chi tiết ở SOURCES, không sửa brief gốc.
- **Kiểm tra / bản mang theo:** kết quả, lệnh tái kiểm và giới hạn ở [VALIDATION.md](presentation/deck-external-2026-10-16/VALIDATION.md); [PDF](presentation/deck-external-2026-10-16/exports/degron-footprint-external-2026-10-16.pdf). Tiến độ trình bày cập nhật ở [sổ theo dõi](../../DECISIONS.md#tai-lieu-trinh-bay); không thêm D mới.

---

## 15/10/2026 (phiên 11) — cập nhật brief slide theo khung ba trụ

Tài liệu: [presentation/slide-content-2026-10-15.md](presentation/slide-content-2026-10-15.md). Căn cứ: [D-033](../../DECISIONS.md#d-033), [D-034](../../DECISIONS.md#d-034), [D-035](../../DECISIONS.md#d-035), [D-036](../../DECISIONS.md#d-036). **Chỉ sửa brief; không dựng slide, không đo mới, không ghi quyết định mới.**

- **Vì sao phải sửa:** brief viết ở phiên 9, **trước** khi khung có trụ cấp thiết và trụ phần mềm. Phần A của sổ quyết định ghi "nội dung slide đã cập nhật theo D-033/D-034/D-035" — câu đó **chưa đúng tại thời điểm viết**, nay mới đúng; đã sửa lại A và mục D cho khớp.
- **Thêm phần "Product" (slide 23–24)** đặt trước Next steps, theo yêu cầu của Trọng. Slide 23: dịch vụ dự đoán — ma trận 28×20, bất định neo vào trần đo lường, chấm đột biến tuỳ ý, API, cờ ngoài phân phối và cờ ngăn tế bào, xuất xứ nhãn; lý lẽ "vì sao là phần mềm" dựa trên nhiễu đo 75,9% và Jaccard 0,4965. Slide 24: harness đánh giá (một split cho mọi mô hình, một khuôn báo cáo kèm trần và MDE) + miền áp dụng 116.702 tile / 17.287 protein, **87,3% cụm cov80 chưa thấy**.
- **Đánh số lại:** 24 → **26 slide**. Next steps thành slide 25, Questions thành slide 26. Mục lục và ngân sách thời gian chia lại: phần Product lấy 2 phút từ phần 3, 5, 6.
- **Slide 6 viết lại theo [D-035](../../DECISIONS.md#d-035):** bỏ mạch dẫn "đột biến lái ung thư" (Tokheim 2021, Liu 2021, DegronMD), thay bằng con số **tự đo 2,148×** ở **mức vùng**. Trích dẫn cũ chuyển xuống ghi chú sản xuất để trả lời nếu GVHD hỏi.
- **Ràng buộc [D-036](../../DECISIONS.md#d-036) đã áp vào câu chữ:** trụ 1 ghi rõ "region level"; ClinVar là **động lực**, không phải đích xác nhận; ≈1.600 là con số **độ phủ**, không đặt cạnh harness; không trích AUC 0,674 (n = 51) rời khỏi CI [0,489; 0,831]. Thêm **năm câu cấm**: "degrons are mutation hotspots", mọi khung "cancer driver mutations", "the residues we predict carry disease signal", "validated against ClinVar", "pathogenic because it breaks a degron".
- **Các chỗ sửa khác:** slide 5 (phạm vi **degron tự trị**), slide 13 (diễn giải biến thể lên đầu, gọi đúng là *mechanistic hypothesis*), slide 14 (bảng **ba trụ** + dòng **C5 phần mềm** ⬜), slide 18 (nguồn thứ 7 **ClinVar** kèm yêu cầu ghi công PMID 29165669 và câu phủ nhận chẩn đoán; peptidome GPS thêm vai miền áp dụng; dung lượng ≈ 1,9 → **2,3 GB**, đo bằng `du`), slide 25 (dòng G3 thành "designed, not built"; tuần 11–13 trỏ sang slide 23–24; việc C-16 đánh dấu đã đóng).
- **Việc còn lại, ghi ở bảng cuối brief:** Trọng tự viết **câu hỏi 1 và 4 của slide 26** (Q1 xin duyệt khung ba trụ, Q4 phạm vi phần mềm); đối chiếu lại từng ô bảng so sánh tiền lệ ở slide 23; nếu chạy kịp đối chứng bảo tồn/vô trật tự thì thay một dòng ở slide 6.
- **Trang khung một trang mang đi buổi gặp 16/10:** [framework-one-pager.html](../../project/meetings/2026-10-16-session-02/framework-one-pager.html) (HTML in vừa một trang A4, mở bằng `file://` theo [D-013](../../DECISIONS.md#d-013)) kèm [bản Markdown](../../project/meetings/2026-10-16-session-02/framework-one-pager.md) để đọc nhanh. Nội dung: mục đích buổi gặp (duyệt khung + xin biên bản cho D-034) · bài toán và phạm vi · bảng ba trụ kèm số đỡ · khối "vì sao phần mềm là đóng góp" · **bảy giới hạn nói thẳng** · lộ trình tới điểm kiểm tuần 10 · ô trống cho câu hỏi và ghi chú biên bản. Bốn câu hỏi xin GVHD **để trống, Trọng tự viết**.

---

## 15/10/2026 (phiên 10) — độ phủ biến thể ClinVar: lập luận cấp thiết đầu tiên có số đo

Căn cứ: [D-033](../../DECISIONS.md#d-033). Báo cáo: [variant-coverage-2026-10-15](research/variant-coverage-2026-10-15/README.md). Trọng hỏi *phần mềm có giải quyết được vấn đề ý nghĩa bài toán không* và *degron có là ngách quan trọng không*; câu đầu là **không** (hai trục độc lập), câu sau đi đo.

- **Tải ClinVar** `variant_summary.txt.gz` (455.785.525 byte, `Last-Modified` 12/10/2026), sổ xuất xứ ở [clinvar/SOURCE.md](data/raw/clinvar/SOURCE.md). Kiểm chứng toạ độ bắt buộc: acid amin hoang dã phải khớp UniProt — **93,0%** khớp (2.349.511/2.526.412), 7,0% bị loại vì lệch transcript.
- **Dùng peptidome GPS làm miền áp dụng, lần đầu.** Repo có Table S1 từ 13/10 nhưng chưa dùng. Bảy tầng: 91 bão hòa · 2.994 quét · 9.817 thư viện · **116.702 tile degron / 17.287 protein** · 360.724 tile đo được. Ba tầng đầu tái lập đúng D-031 nên loader đáng tin. **87,3% cụm cov80** của miền degron **chưa thấy** trong tập huấn luyện.
- **Con số quyết định:** vùng degron giàu biến thể **gây bệnh** so với **lành tính** gấp **2,148×** (CI [2,072; 2,227]), Mantel–Haenszel phân tầng **theo protein**, 3.114 tầng; theo cụm cov80 là 2,094. Thô là 2,096 ⇒ **không** phải tạo tác mức gene. Đây là lập luận cấp thiết đầu tiên của đề tài dựa trên số đo.
- **Độ phủ đạt ngưỡng cam kết trước:** **≈1.600** biến thể chấm được bằng **đúng ô thực nghiệm** (575 bão hòa + 1.037 quét), ≈1.350 là VUS. Phân biệt quan trọng: bộ quét có 18.691 biến thể rơi vào peptide nhưng chỉ **1.037** trùng đúng acid amin, vì thư viện quét chỉ có một thay thế mỗi vị trí (≈1/19).
- **Kết quả âm 1 — không giàu lên theo vị trí.** Tỉ lệ biến thể trong degron bằng đúng tỉ lệ nền ở cả ba ngưỡng (33,4%/32,4%; 13,2%/12,8%; 3,9%/3,8%). ⇒ **Không nói “degron là điểm nóng biến thể”**. Và ngưỡng PSI ≤ 3,0 cho 32,4% tile toàn proteome là degron ⇒ câu “nằm trong degron” gần như không mang thông tin.
- **Kết quả âm 2 — degron lái ung thư phần lớn không hiện ra.** Chỉ **HIF1A** (PSI 1,86/1,51; MLN4924 → 2,45). `CTNNB1` codon 31–48 **đo tốt mà không phải degron** (reads 145/66, PSI 5,27/5,36); `MYC` T58/S62 vắng mặt; `NFE2L2` ETGE không phải degron. Assay GPS chỉ thấy degron **tự trị**. ⇒ Mạch "đột biến lái ung thư" mà Claude đề xuất đầu phiên **bị chính phép đo bác bỏ**; phạm vi đúng là **degron tự trị + biến thể dòng mầm**.
- **Mạch soma không có dữ liệu:** cột `Oncogenicity` chỉ có ~800 giá trị trên 2,56 triệu, trong đó 145 trong tile degron, 5 trong bộ quét, **0** trong bộ bão hòa.
- **Việc đe doạ kết luận nhiều nhất, chưa làm:** khử **bảo tồn** và **độ vô trật tự**. Nếu 2,148 biến mất sau khi khử thì nó chỉ nói "degron nằm trong vùng chức năng". Ghi ở [D](../../DECISIONS.md#doi-chung-cap-thiet).
- **Cuối phiên — khung đề tài được chốt:** Trọng cho biết đã **trao đổi trực tiếp với GVHD** và được xác nhận **trụ phần mềm được tính là đóng góp** ([D-034](../../DECISIONS.md#d-034); nguyên liệu thô ở [people.md](../../project/people.md), **chưa có biên bản**). Trọng **ủy quyền cho Claude trong phiên này** xác nhận các mục C về khung và đóng góp ⇒ [D-035](../../DECISIONS.md#d-035) nhận **C-18** (phạm vi degron tự trị + dòng mầm), **C-17** (a + b), **C-19** ⇒ **C-16 chuyển sang không dùng**. **Hàng đợi C nay trống**; còn chờ bên ngoài là [C-5](../../DECISIONS.md#c-5) (GVHD duyệt khung, buổi gặp **16/10**) và C-11a (email giấy phép).
- ⚠ **Giá phải trả của C-19, ghi để không quên:** rủi ro *"cả hai nguồn nhãn mức residue đều của Zhang 2023"* **vẫn mở và nay không có ứng viên nào**. Yêu cầu cho ứng viên thay thế: readout là **độ bền**, trên **degron tự trị**, **nhóm tác giả khác**, nhãn **mức residue**.
- **Đo thêm cuối phiên: mắt nối trụ 1 → trụ 2 CHƯA thiết lập được** ([D-036](../../DECISIONS.md#d-036), [báo cáo §8b](research/variant-coverage-2026-10-15/README.md)). Ba phép, đều nhất quán với rỗng: (1) nhị phân footprint/không, **OR 0,777** [0,530; 1,139]; (2) ΔPSI liên tục khớp **vị trí**, tầng có lực nhất (n = 1.624, 620 cụm), **AUC 0,5166** [0,479; 0,554]; (3) ΔPSI khớp **đúng ô**, nhãn sạch nhất nhưng n = 51, AUC 0,6738 [0,489; 0,831] — **CI vẫn chạm 0,5**. Ghép cặp trong cùng peptide: +0,033 [−0,079; +0,141], 51,2% dương.
  - Mạch đáng theo: hiệu ứng **tăng đơn điệu** khi khớp chặt hơn và nhãn sạch hơn (0,517 → 0,520 → 0,674; trung vị ΔPSI gây bệnh **gấp 4,6 lần** lành tính ở tầng sạch nhất) — đúng dạng hiệu ứng thật bị nhiễu nhãn làm suy giảm. Nhưng n = 51 không chở được tuyên bố.
  - **Không đóng được bằng dữ liệu hiện có:** bộ bão hòa chỉ 91 peptide ⇒ số ca khớp đúng ô chặn ở ≈51. Việc này **gộp** với lỗ mà D-035 để lại khi bỏ `CTNNB1`: cần **một nguồn nhãn mức residue mới**.
  - Hệ quả câu chữ: giữ trụ 1 ở **mức vùng**; **cấm** nói "residue đề tài dự đoán là residue mang tín hiệu bệnh"; ClinVar chỉ là **động lực**, không phải đích xác nhận mô hình.
- Không huấn luyện mô hình; **mục tiêu G2 vượt 0,7693 không đổi và chưa đạt**. **Không sửa `presentation/`** — Trọng yêu cầu chốt khung trước, việc slide để sau.

---

## 15/10/2026 — tổ chức lại sổ quyết định và đồng bộ thẻ trạng thái

Căn cứ: [D-032](../../DECISIONS.md#d-032). Đây là phiên biên tập tài liệu; không huấn luyện, không đo mới và không sửa dữ liệu.

- Sổ quyết định có [bản đọc nhanh](../../DECISIONS.md#hien-hanh), hiệu lực theo khoản, lịch sử thu gọn và phần theo dõi riêng; giữ nguyên mã và nguyên văn 31 hồ sơ cũ.
- Đồng bộ README với bằng chứng đã có: ridge đã huấn luyện, nội dung slide đã cập nhật; việc tải Larsen đã làm, phản hồi giấy phép vẫn đang chờ.
- Làm rõ phạm vi MDE và dẫn tới nghĩa vụ đối chứng Degformer; C-16/C-17 còn ở phần chờ xác nhận, không ghi thêm phê duyệt nghiên cứu.
- Cập nhật quy ước trong `CLAUDE.md` và các liên kết; giữ nguyên `AGENTS.md`. Các mục nhật ký cũ bên dưới giữ làm lịch sử.
- Kiểm tra: nguyên văn 31 hồ sơ và mã D cũ còn đủ; anchor trỏ sổ quyết định hợp lệ; render Markdown giữ đúng bảng/khối thu gọn; `git diff --check` đạt. Kiểm link toàn repo còn đúng một lỗi có sẵn tại `lectures/14-xai-basics.html` → `15-reading-bioinfo-papers.html`, ngoài phạm vi phiên này.

---

## 15/10/2026 (phiên 9) — viết nội dung slide trình bày với GVHD, bằng tiếng Anh

Tài liệu: [presentation/slide-content-2026-10-15.md](presentation/slide-content-2026-10-15.md).
**Không huấn luyện, không đo mới, không dựng slide** — chỉ viết nội dung. Theo yêu cầu của Trọng, nên
[D-030](../../DECISIONS.md#d-030) mục 1 (lùi tài liệu trình bày) và ghi chú học tập "chỉ sửa tài liệu trình
bày khi được yêu cầu" **đều đã được gỡ chặn bằng lời yêu cầu trực tiếp**. Điều kiện số của D-030 mục 1 cũng
đã đạt từ phiên 8 (+0,0289).

- **Bốn lựa chọn Trọng chốt khi được hỏi:** đóng khung theo hướng C-15 (mức residue); 15–20 phút / 24 slide;
  tiêu đề **mô tả nhiệm vụ, không đặt tên mô hình**; độ trung thực **"giữ tối thiểu"** (chỉ giới hạn trực
  tiếp của bài toán và dữ liệu; không nêu các hướng đã bị loại hay tranh luận nội bộ về mức đóng góp).
- **Nội dung 24 slide theo chín phần Trọng yêu cầu**, chữ slide **tiếng Anh**, ghi chú sản xuất tiếng Việt.
  Phần đầy đủ: 1–13, 15–20, 23–24. Phần **sườn có cắm mốc**: slide 14 (ô C4) và 21–22 (kiến trúc).
  Mỗi slide có **đặc tả hình/animation** riêng, và 7 trong số đó dùng lại SVG có sẵn ở
  [lectures/degron-basics/figures/](../../lectures/degron-basics/figures/).
- **Trích dẫn đã đối chiếu lại qua PubMed và bioRxiv API ngày 15/10**, vì bảng tiền lệ là chỗ GVHD yêu cầu
  chính xác tên và tác giả: lấy đúng danh sách tác giả, tạp chí, volume/trang, DOI cho 9 công trình. Hai
  điều phải ghi trên slide: **Larsen 2025 là preprint**, và **Degformer không có bài báo**.
- **Phát hiện khi viết: bản nháp đầu đã lạc hậu ngay trong ngày.** Viết trước khi đọc phiên 8, nên sáu con
  số và một phát biểu bị sai; đã sửa toàn bộ và ghi bảng đối chiếu ở đầu file. Chỗ sai: C-15 còn "chờ"
  (nay là D-031) · "chưa có con số dương" (nay +0,0289 / +0,0300) · MDE **0,071 → 0,0123** · "chưa đếm cụm"
  (nay 89) · "n = 91 là cỡ mẫu phần mức residue" (**sai** — bộ quét cho 1.985 cụm) · rủi ro LeBlanc "chưa
  giải quyết" (nay đã khoanh, 56× → 2,2×) · lý lẽ MIL (nay là **giám sát yếu**).
- **Áp [C-17](../../DECISIONS.md#c-17) mục b vào toàn bộ tài liệu trình bày:** cấm câu "vị trí thắng thành
  phần"; thay bằng *"composition at a ±3 neighbourhood scale beats composition at whole-peptide scale"*,
  kèm bảng phân rã +0,0232 / +0,0057 / +0,0002 ngay trên slide 14. Danh sách "không được nói" trên slide
  tăng từ 3 lên **6 câu**, thêm cả *"bộ bão hòa là nguồn duy nhất đỡ được mức residue"* (D-031 mục 2 đã sửa).
- **Hai chỗ cố ý không đưa lên slide theo lựa chọn "giữ tối thiểu", nhưng đã soạn câu trả lời sẵn** trong
  ghi chú: rủi ro LeBlanc, và chỗ mơ hồ giấy phép MIT của bộ Larsen đang chờ email.
- **Việc còn chặn dựng slide:** sinh hình ví dụ 28×20 từ `psi-sat_*.tsv` (chưa có script), và dựng các sơ đồ.

---

## 15/10/2026 (phiên 8) — thực hiện C-15: hai việc chặn đóng lại, và con số dương đầu tiên cho G2

Trọng ra lệnh *"tiến hành thực hiện đề xuất C-15, nghiên cứu thêm để giảm thiểu rủi ro và trình bày được đóng góp rõ ràng"* ⇒ [D-031](../../DECISIONS.md#d-031). Báo cáo đầy đủ: [residue-task-derisk-2026-10-15](research/residue-task-derisk-2026-10-15/README.md). Sáu lệnh đo, mọi lệnh **chỉ đọc** `data/`.

- **Việc chặn 1 — lực trên n = 91: giải quyết, và rủi ro nhỏ hơn đã tưởng 6 lần.** 91 peptide nằm trên **91 protein / 89 cụm** cov80 (thư viện bão hòa chọn mỗi protein một peptide ⇒ lồng nhau mức protein gần như không tồn tại). Ghép cặp theo peptide + bootstrap theo cụm: SE 0,0040–0,0044 ⇒ **MDE 0,0123** ở lực 80%, lực tại delta đo được **0,995**. Con số **0,071** của phiên trước sai vì suy từ phương sai **không ghép cặp**; MDE không ghép cặp cũng chỉ 0,0491. ICC ô-trong-peptide 0,0625 ⇒ **≈ 1.416 ô độc lập hiệu dụng** (không phải 47.847, cũng không phải 91). Bậc thang ngưỡng: 3,5 cho 141 peptide / 137 cụm, 4,0 cho 176 / 172.
- **Việc chặn 2 — rủi ro LeBlanc: khoanh được bằng số.** Chạy đúng khuôn §11.2 (bootstrap theo cụm, |μ|/SD từng hệ số) nhưng trên nhãn **hiệu ứng đột biến** và véc-tơ **ngữ cảnh cục bộ ±3**: % hệ số tách khỏi 0 **28,9% → 53,3%**, đồng thuận dấu **0,684 → 0,90**, tỉ lệ áp đảo của thành phần **≈ 56× → 2,2×**. ⇒ Kết luận LeBlanc đúng cho **nhãn mức tile**, không phải cho nhãn đột biến. Bộ bão hòa một mình **yếu** cho tham số ngữ cảnh (25%, 89 cụm) nhưng **mạnh nhất bảng** cho cặp thay thế (92,5%).
- **Phát hiện đổi thiết kế: có HAI nguồn nhãn mức residue, không phải một.** Bộ quét cũng là nhãn hiệu ứng đột biến: **2.994 peptide degron / 1.985 cụm / 83.446 ô**, trần đo lường AUROC **0,9458**. Nó đỡ **trục ngữ cảnh**; bộ bão hòa đỡ **ma trận 19 thay thế**. Sửa [D-028](../../DECISIONS.md#d-028) mục 5 ("nguồn duy nhất"). Chồng lặp 61/89 cụm nên mọi phép chuyển nguồn phải loại cụm trùng — đã làm (bỏ 145/2.994 peptide).
- **Con số dương đầu tiên cho G2 [đo].** Năm mô hình ridge, split cụm cov80, 5 fold × 5 seed, AUROC mức ô macro theo peptide: M0 chỉ-thành-phần **0,8393** → M3 có ngữ cảnh **0,8682** ⇒ **+0,0289** (CI [0,0264; 0,0313], 1.599 cụm, Wilcoxon 8 × 10⁻¹²⁹). So **ΔPAP `cnn2w7`** (0,8357) thì **+0,0300** (CI [0,0234; 0,0366], ghép cặp 2.064 peptide / 1.471 cụm). Trụ 89,7% nay **có một con số**: trên bộ quét, 68,9% peptide có nhóm cùng cặp thay thế bị chia dương/không-dương, và giá của việc không tách được chúng là +0,0289.
- **Nhưng phân rã delta đổi cách phát biểu, và đây là chỗ phải nói thật.** Vị trí **tuyệt đối** một mình: +0,0052; **thành phần cửa sổ ±3 không thứ tự**: **+0,0232** (80% của tổng); thêm thứ tự: +0,0057; thêm vị trí tuyệt đối lên trên ngữ cảnh: **+0,0002** ⇒ bằng 0. Nên **không** được nói "vị trí thắng thành phần". Câu đúng: *thành phần ở thang **lân cận ±3** thắng thành phần ở thang **cả peptide*** — **tinh chỉnh** LeBlanc chứ không chống. Ghi thành [C-17](../../DECISIONS.md#c-17).
- **Chỗ vẫn thua, và nay là mục tiêu G2 có số.** Chuyển sang ma trận bão hòa (huấn luyện chỉ trên bộ quét, cụm rời, **19 thay thế chưa thấy**): M3 **0,7273** so với ΔPAP `cnn2w1` **0,7693** ⇒ **−0,0420** (CI [−0,0580; −0,0256]). Trên thang **mức vị trí** thì **đảo**: 0,4440 so 0,3553 ⇒ phải báo theo từng thước đo. Mục tiêu G2 còn lại: **vượt 0,7693**, trần đo lường 0,9519.
- **Lý lẽ cho MIL phải đổi [chưa xác minh — tra qua tóm tắt].** Không tìm thấy phép so trực tiếp MIL ↔ đầu theo residue trên cùng nhiệm vụ mức residue; mô típ chuẩn là **đầu theo residue khi có nhãn mức residue, MIL khi chỉ có nhãn mức túi**. ⇒ "Chưa tìm thấy tiền lệ" là lý lẽ **yếu**. Lý lẽ thay thế có số đỡ: **giám sát yếu** — nhãn mức túi rất dồi dào nhưng không nhận diện được tham số vị trí (28,9%), nhãn mức ô nhận diện được nhưng ít (89 cụm).
- **Nguồn nhãn độc lập đã tìm được [chưa xác minh — chưa tải].** Krishna 2026 (*Nat Genet* 58:366–375): SGE nội sinh, **342 đột biến missense**, **codon 31–48** của degron `CTNNB1`. Đã kiểm **[đo]**: `P35222` **không** có trong bảng PSI của Zhang, **không** có trong thư viện TF của Larsen, và codon 31–48 nằm **trọn** trong tile 2 (residue 24–51 theo quy tắc `(n−1)·23`) ⇒ chấm được bằng đúng mô hình 28-mer. ⚠ Readout là **tín hiệu Wnt**, không phải độ bền; giấy phép bảng điểm **chưa rõ**. Đề xuất [C-16](../../DECISIONS.md#c-16).
- **Nợ kỹ thuật đã trả trong phiên:** `ridge_fit` đổi từ SVD sang phân rã Gram (nhanh ≈ 15 lần), khớp `sklearn.linear_model.Ridge` tới **7 × 10⁻¹⁴**. Kiểm chéo đường ống: n = 91, trần 0,9519 và ΔPAP `cnn2w1` 0,7693 **tái lập đúng** [pap-baseline §C](research/pap-baseline/README.md) ngày 14/10.
- **Đính chính đã dán:** [reframe-options](research/reframe-options-2026-10-15/README.md) nay có khối đính chính ở đầu cho ba chỗ (+0,1061 nhiễu lẫn, "dư địa đến trần", §11.2 chỉ đúng cho nhãn peptide).

---

## 15/10/2026 — đánh giá vòng học tập 2, giải thích WT và hiệu ứng thực nghiệm

- Lưu nguyên văn câu trả lời và đánh giá năm câu trong [hồ sơ học tập](learning/assessment-log.md). Không tính câu 1 gửi trước lượt bị ngắt thành một lần kiểm tra độc lập.
- Tiến bộ: đã sửa tên phiên mã/dịch mã, đọc đúng ô M7V, tính ΔPSI +1,4 và đúng chiều làm bền; hiểu mất thông tin thứ tự ở mô hình đếm thành phần. Chưa vững: WT, hiệu ứng đo/dự đoán, ΔPSI/xác suất và vai trò E3/nhận diện trực tiếp.
- Bổ sung định nghĩa và ví dụ số **giả định**, nhận diện thiếu sót khi người dạy dùng WT chưa giải nghĩa; đặt bốn câu vòng 3, đang chờ phản hồi. Đọc lại [D-027](../../DECISIONS.md#d-027) để giữ đúng căn cứ trạng thái; không đổi thiết kế nghiên cứu trong phiên học tập.

---

## 15/10/2026 — đánh giá vòng học tập 1, đặt câu hỏi vòng 2

- Lưu nguyên văn sáu câu trả lời và chấm từng câu trong [hồ sơ học tập](learning/assessment-log.md), không suy ra phần trăm hiểu cả đề tài từ tổng điểm.
- Bằng chứng tích cực: phân biệt residue/loại aa, hiểu vai trò thứ tự, mục đích định vị/ưu tiên thí nghiệm và giới hạn chuyển peptide sang protein. Nội dung cần sửa: đảo tên phiên mã/dịch mã, ma trận 28×28, lẫn ΔPSI với xác suất và suy luận trực tiếp về nhận diện E3.
- Đã giải thích sửa sai và đặt năm câu vòng 2; đang chờ phản hồi, chưa ghi nội dung nào nắm vững qua kiểm tra lặp. Đọc lại phần C của [DECISIONS.md](../../DECISIONS.md) để giữ C-12/C-13 đúng vai đề xuất chờ xác nhận khi đánh giá trạng thái đề tài.

---

## 15/10/2026 (tối, phiên 7) — lần thử G2 đầu tiên: **hướng cross-assay không đứng được**, và hai con số của phiên trước bị quy sai

Tài liệu: [cross-assay-model-2026-10-15/](research/cross-assay-model-2026-10-15/README.md). Script: [transfer_experiment.py](research/cross-assay-model-2026-10-15/transfer_experiment.py). Đề xuất mới: **[C-15](../../DECISIONS.md)**. Chạy theo [D-030](../../DECISIONS.md#d-030) mục 1 (Trọng: chốt hướng đóng góp cụ thể **trước** khi làm tài liệu trình bày) — và phép đo đã làm đúng việc đó, theo hướng phủ định.

- **Kết quả, 5 seed, chấm trên nhãn tile ở cụm test:** A chỉ-GPS **0,7806 ± 0,0029** · B chỉ-tile **0,7955 ± 0,0043** · **C biểu diễn dùng chung + đầu riêng mỗi assay 0,7983 ± 0,0022** · D stacking 0,7955. **C − B = +0,0029** (SD 0,0024, thắng 5/5 seed) — dấu ổn định nhưng chỉ bằng **1,5%** phần còn lại.
- **Kiểm năng lực, 3 seed:** gradient boosting trên nhãn tile **0,7791 ± 0,0048** — **thấp hơn ridge tuyến tính**; gộp thêm GPS cho boosting **0,7847** (+0,0057), vẫn thấp hơn ridge chỉ-tile. **Mô hình phi tuyến mạnh không mở được dư địa.**
- **Lỗi 1 của Claude — nhánh D vô nghĩa ngay từ thiết kế.** Dự đoán của A là `X·wA`, tổ hợp tuyến tính của chính các cột `X`, nên ridge trên `[pA, X]` **cộng tuyến hoàn toàn** với ridge trên `X`: D buộc phải bằng B. SD 0,0000 xác nhận.
- **Lỗi 2 — con số +0,1061 của phiên 4 bị nhiễu lẫn và quy sai nguyên nhân.** Học GPS → chấm GPS: 0,8848. Học GPS → chấm tile: 0,7786. **Học tile → chấm tile: 0,7955.** Nếu 0,1061 là dịch chuyển assay thì học đúng assay phải lấy lại gần hết — nó chỉ lấy lại **0,0169**. Phần còn lại là **nhãn tile vốn khó dự đoán hơn nhãn GPS**. Phần **vẫn đúng**: phép đo nhãn-so-nhãn ở phiên 3 (tương quan thật hai assay **0,785** so với trần nhiễu 0,978) không cần mô hình nên không bị ảnh hưởng — hai assay **thật sự bất đồng hệ thống**, chỉ là **giá mô hình phải trả** thì nhỏ.
- **Lỗi 3 — lặp lại đúng loại lỗi [D-025](../../DECISIONS.md#d-025) mục 1 đã sửa một lần.** Coi **trần độ tin cậy** (0,9903) là **dư địa đạt được**. Trần đó là chặn trên của **phép đo**, không phải lời hứa về mức dự đoán được từ trình tự. Bằng chứng: ba lớp mô hình đều dừng quanh **0,78–0,80**. Phải sửa mọi chỗ viết "dư địa đến trần".
- **Kết luận: không có chỗ cho một kiến trúc mới có delta dương cỡ luận văn ở hướng cross-assay.** Trần của ý tưởng đó ≈ **+0,017**; chuyển giao cho +0,003…+0,006; biểu diễn tốt hơn thì có dư địa nhưng đó là **sân của PAP** (tác giả báo Pearson 0,82/0,87 trên tile giữ lại).
- **Điều vẫn giữ giá trị:** phần đo và phân rã **chặn** được những gì người khác tuyên bố (split cụm không mua gì; tương quan thật hai assay 0,785; ba lớp mô hình dừng ở 0,78–0,80). Xứng làm **một chương đo lường**, không xứng làm câu đóng góp chính.
- **[C-15](../../DECISIONS.md) đề nghị quay lại nhiệm vụ mức residue làm trụ đóng góp** — nơi duy nhất còn lại có khoảng trống **chứng minh bằng toán** (89,7%), **chưa có mô hình nào huấn luyện đúng nhiệm vụ**, và nhãn **hiệu ứng đột biến** là loại duy nhất nhận diện được tham số vị trí. Nhận lại rủi ro **n = 91** và rủi ro LeBlanc. Khác biệt so với 14/10: nay **năm hướng thay thế đã bị loại bằng số**.

---

## 15/10/2026 (tối, phiên 6) — chốt tám đề xuất, xếp thứ tự tám tuần, tải bộ nhân Larsen

Quyết định mới: **[D-028](../../DECISIONS.md#d-028)** (Trọng, chấp nhận cả tám đề xuất) và **[D-029](../../DECISIONS.md#d-029)** (Claude ủy quyền, thứ tự tám tuần). **Phần C của DECISIONS.md nay trống**, chỉ còn [C-5](../../DECISIONS.md) là việc phải làm chứ không phải việc phải quyết.

- **D-028 chấp nhận:** C-8 (hạ cổng phơi lộ) · C-9 (AUROC mức ô) · C-12 (hai việc chặn + điểm kiểm tuần 10) · C-14 (split cụm thôi là điểm thiết kế chính) · **C-13 bản đã sửa** (tile và bộ bão hòa **hai vai riêng**, sửa một phần [D-025](../../DECISIONS.md#d-025) đề xuất 2) · C-10 (tải Larsen) · C-11a (email giấy phép) · C-11b (Degformer làm baseline, kèm điều kiện trích dẫn). **C-7 đóng** vì [D-027](../../DECISIONS.md#d-027) đã giải quyết.
- **D-029 — thứ tự tám tuần,** căn cứ: rủi ro lớn nhất không phải kỹ thuật mà là **chưa đề tài nào được GVHD duyệt**. Tuần 6–7 tài liệu + hỏi GVHD (⚠ **chờ Trọng bật đèn xanh** vì đã dặn không tự sửa `presentation/`) · 7–8 mô hình cross-assay (lần thử G2 thật đầu tiên) · 8 bộ nhân Larsen → mức 5 bậc thang · 9 chương mức residue (lực trên n = 91) · **10 điểm kiểm cứng** · 11–13 ứng dụng và viết. Thứ tự này **hoãn G2 thêm một tuần** — đánh đổi có ý thức.
- **Đã thực hiện C-10 ngay trong phiên.** `git clone` tag **`v1.0`** (commit `2698ecc6`), lấy `transfac_tiles.csv.gz` (5.771.779 byte, SHA-256 `0c31057d…`) + `LICENSE` vào `data/raw/larsen-2025/`, kèm [SOURCE.md](data/raw/larsen-2025/SOURCE.md).
- **Audit khi tải cho hai kết quả đáng giá.** (1) **Mốc PAP 0,79 của tác giả đã tái lập độc lập**: Pearson(`pap`, `degron_score`) = **−0,7899** trên 59.000 tile, khớp bốn chữ số (dấu âm vì `degron_score` ngược chiều PAP). (2) **Đây là chỗ duy nhất rASA/pLDDT có phương sai thật** — rASA trung vị **0,6900**, SD **0,2334**, **49,4%** tile > 0,7 — nên là nơi duy nhất kiểm được cổng phơi lộ, đúng như [C-8](../../DECISIONS.md) dự đoán. Độ tin cậy `degron_score` **0,9701** (trần r 0,9849) trên **59.016** tile / **1.627** gene.
- **Giải quyết một câu hỏi treo từ phiên chiều:** số tile thật là **63.258 dòng**, và nó **không khớp bất kỳ con số nào in trong bài** (58.781 / 58.992 / 62.992 / 63.011 / 63.230) ⇒ bài không nhất quán với chính nó; khi trích phải dùng số đếm được từ file.

---

## 15/10/2026 (tối, phiên 5) — dọn hai món nợ phương pháp: Phát hiện 2 **vững**, rủi ro LeBlanc **là thật**, và C-13 phải sửa

Tài liệu: [reframe-options §11](research/reframe-options-2026-10-15/README.md). Script: [method_debt.py](research/reframe-options-2026-10-15/method_debt.py). Theo lựa chọn của Trọng: dọn nợ trước khi chốt các đề xuất C.

- **Nợ 1 — Phát hiện 2 không phải tạo tác của mô hình yếu.** Ba mô hình, 3 seed: ridge dịch chuyển cụm **−0,0032**, **gradient boosting −0,0014** (*nhỏ hơn cả* ridge), **1-NN theo đồng nhất vị trí −0,0094**. Lời giải thích "mô hình quá đơn giản để ghi nhớ định danh protein" **bị bác bỏ**; điều kiện kèm [C-14](../../DECISIONS.md) đã thực hiện.
- **Và đã tìm ra cơ chế:** 1-NN đồng dạng chỉ đạt **ρ ≈ 0,31** so với **0,89** của ridge ⇒ tra cứu theo đồng dạng trình tự **gần như vô dụng** cho nhiệm vụ này, nên **không có tín hiệu đồng dạng nào để rò rỉ**. Split cụm cov80 không mua được gì **vì tín hiệu là thành phần, không phải họ hàng trình tự**. Thêm: **gradient boosting (0,8813) không thắng ridge (0,8858)** — tín hiệu mức peptide là đơn giản, cộng tính.
- **Nợ 2 — rủi ro LeBlanc là thật, ở mức tham số.** Bootstrap ×40 trên 43.635 peptide: véc-tơ **560 ô (vị trí, acid amin)** có \|μ\|/SD trung vị **1,24**, chỉ **28,9%** hệ số tách được khỏi 0, đồng thuận dấu **0,684**; còn **tổng theo acid amin** đạt trung vị **69,02**, 100% tách khỏi 0, đồng thuận dấu **1,000** — ổn định hơn ≈ **56 lần**. Tái lập nửa–nửa của véc-tơ 560 chiều **nhìn cao (0,9801)** nhưng đó là vì nó **thừa hưởng** thành phần mức acid amin; phép kiểm phân biệt được là **từng hệ số**.
- **Hệ quả buộc phải sửa [C-13](../../DECISIONS.md), và nó cứu lại bộ bão hòa.** Nhãn dùng ở nợ 2 là PSI **cả peptide** — cùng loại với nhãn **mức tile**. Nên **tile không đỡ được bất kỳ tuyên bố mức residue nào**. Hai nguồn có **hai vai riêng, không thay thế nhau**: tile đỡ benchmark + phân rã + cỡ mẫu + trần nhãn; **bộ bão hòa là nguồn duy nhất** đỡ mức residue vì nhãn của nó là **hiệu ứng đột biến**. ⇒ **Việc chặn "lực trên n = 91" KHÔNG mất đi** như phiên 3–4 đã nói, nó **thu hẹp vào chương mức residue**.
- **Và nó không mâu thuẫn trụ 89,7% mà giải thích trụ đó:** chứng minh 89,7% nói mô hình thành phần *không thể* định vị; nợ 2 nói nhãn peptide *cũng không đủ để học* định vị. Hai việc khác nhau, cùng chỉ về một chỗ — muốn nói về residue thì **buộc** phải có nhãn đột biến.

---

## 15/10/2026 (tối, phiên 4) — đối chứng offset **đạt**, bậc thang 2×2 cho ba phát hiện; chỗ đặt đóng góp hẹp lại lần nữa

Tài liệu: [reframe-options-2026-10-15/ §10](research/reframe-options-2026-10-15/README.md). Script: [cascade_and_offset.py](research/reframe-options-2026-10-15/cascade_and_offset.py). Đề xuất mới: **[C-14](../../DECISIONS.md)**. **Chưa huấn luyện mô hình sâu nào** (chỉ ridge tuyến tính làm thước đo).

- **Trọng xác nhận [D-027](../../DECISIONS.md#d-027) là quyết định của chính mình**, không phải lời GVHD truyền đạt ⇒ đã sửa nhãn provenance; [C-5](../../DECISIONS.md) **vẫn mở**.
- **(a) Đối chứng offset: ĐẠT, giới hạn số 1 ở §9.4 đã đóng.** Biến thiên theo offset chỉ **0,0044 AUROC** (offset 0/1/2 cho 0,9069 / 0,9026 / 0,9040) so với khoảng cách **0,0773** ⇒ ngữ cảnh 2 residue giải thích nhiều nhất **≈ 6%**. Chỉ 140/17.820 trình tự khớp nhiều hơn một tile. **Con số 0,0773 dùng được trước GVHD.**
- **(b) Bậc thang 2×2, 5 seed, cả hai ô ngoài mẫu.** Đã sửa hai lỗi của bản nháp: ô "cùng cụm" trước đó là **trong mẫu**, và trước đó chỉ **một** split (bài học từ chính bài PROTAC: rank-1 một seed tụt 0,161). Giữ nguyên trình tự, cụm và mô hình, chỉ đổi một thứ mỗi lần.
- **Phát hiện 1 — toàn bộ khoảng cách tổng quát hóa là dịch chuyển assay; trình tự lạ đóng góp bằng 0.** Dịch chuyển cụm **−0,0039** (cụm chưa thấy *hơi tốt hơn*, ổn định qua 5 seed, SD 0,0016–0,0028) so với dịch chuyển assay **+0,1061** ⇒ tỉ lệ **27×**. Cộng với §9 (hai assay tin cậy 0,975 và 0,981) ⇒ đây là loại **thứ ba** chưa ai đặt tên: **thiên lệch hệ thống giữa định dạng assay** — không phải nhiễu, không phải trình tự lạ. Bài PROTAC quy 81% khoảng cách cho nhiễu đo; ở đây nhiễu gần như **không đóng góp gì**.
- **Phát hiện 2 — split cụm protein cov80 không mua được gì trên nhiệm vụ này.** **Mâu thuẫn với [D-025](../../DECISIONS.md#d-025) đề xuất 4** của chính repo, và với phần phân tích lực vốn chọn cov80 thay cov50. ⇒ [C-14](../../DECISIONS.md) đề nghị **xét lại**, không phải bỏ. ⚠ Giới hạn: mô hình là **ridge tuyến tính trên one-hot**, có thể quá đơn giản để ghi nhớ định danh protein; **phải chạy lại khi có mô hình mạnh** trước khi sửa D-025.
- **Phát hiện 3 — kênh theo vị trí chỉ thêm +0,0028 đến +0,0030** so với chỉ thành phần ⇒ **xác nhận độc lập cho LeBlanc 2026** trên assay khác, 5 seed. Rủi ro số một của [C-12](../../DECISIONS.md) **đã được đo và nó là thật — ở mức peptide**. Nhưng **không** bác bỏ trụ thứ nhất: repo đã chứng minh bằng toán rằng mô hình chỉ-thành-phần **không thể định vị** residue (89,7%). Hai điều cùng đúng — *thành phần đủ để chấm cả đoạn, nhưng bị chứng minh không thể định vị bên trong đoạn*. ⇒ Luận văn **không được** nói "vị trí giúp chấm điểm peptide"; lý lẽ vị trí chỉ sống **ở mức residue**.
- **Chỗ đặt đóng góp hẹp lại ba lần nhờ loại trừ.** Không phải: trình tự lạ (−0,0039), ngữ cảnh vị trí mức peptide (+0,0030), cổng phơi lộ (không nhận diện được). Còn lại **đúng hai**: **dịch chuyển định dạng assay** (+0,1061, hệ thống) và **định vị mức residue** (bất khả thi cho mô hình thành phần).
- **Mục tiêu số mới:** cross-assay Spearman **0,7786 ± 0,0065**, trần nhiễu **0,9778** ⇒ dư địa **0,1992** trên **4.308 cụm protein**. So mốc cũ (0,4897 → 0,6514, n = 91): dư địa lớn hơn, cỡ mẫu gấp **47 lần**, baseline **không phải oracle**.

---

## 15/10/2026 (tối, phiên 3) — đọc toàn văn bài PROTAC, đo khoảng cách qua assay: **H1 có thông điệp**, và nó đảo kết luận của bài mẫu

Tài liệu: [reframe-options-2026-10-15/ §9](research/reframe-options-2026-10-15/README.md). Quyết định mới: **[D-027](../../DECISIONS.md#d-027)**.

- **Trọng cho biết: đóng góp dạng "đo và phân rã trần của một lớp bài toán" được nhận, nhưng đề tài vẫn nên có kiến trúc mới** → ghi thành [D-027](../../DECISIONS.md#d-027), giải quyết [C-7](../../DECISIONS.md) theo hướng **thuận có điều kiện**: mạch benchmark + phân rã làm **khung**, kiến trúc mới **vẫn bắt buộc**. ⚠ Chưa rõ đây là lời GVHD truyền đạt hay quyết định của Trọng — nếu là lời GVHD thì phải đổi nhãn mục và đóng C-5.
- **Đã đọc toàn văn arXiv 2605.11764** (Klamt, Nejdl, Tang; nộp 12/05/2026; **preprint chưa phản biện**). Thứ chuyển sang được không phải con số mà là **bậc thang**: random-CV **0,802** → cross-lab **0,678** → LOTO **0,653** trên cùng cohort 36 target, ghép cặp n = 35. Mấu chốt: mức giữa **giữ nguyên định danh target** nên dịch chuyển cấu trúc bị loại, hiệu số cô lập đúng một nguyên nhân. Phân tích **chính** của họ là **ω² = 0,256** (hiệu chỉnh chệch), không phải bậc thang. Họ viết thẳng bốn chặn là *"partially-overlapping bounds rather than a strict additive identity"*, và phần giới hạn **tự hạ** hiệu ứng warhead +0,042 của chính mình xuống dưới sai số seed.
- **Đo bậc thang hai mức cho degron** — chuyển "cùng hợp chất, hai phòng" thành **"cùng trình tự, hai assay"**. Ghép 28-mer của GPS làm chuỗi con đúng của 30-mer của Voutsinos: **17.820 trình tự dùng chung, 4.610 accession, 4.308 cụm protein cov80**. Script: [cross_assay_gap.py](research/reframe-options-2026-10-15/cross_assay_gap.py).
- **Kết quả: trần trong assay 0,9813 → qua assay 0,9041 ⇒ khoảng cách 0,0773 AUROC.** Và nó **đảo kết luận của bài PROTAC**: ở đó phương sai đo chiếm **81%** khoảng cách, ở đây **gần như 0%** — hai assay đều rất tin cậy (0,9749 và 0,9807), trần nhiễu 0,9778, nhưng tương quan **thật** sau chỉnh suy giảm chỉ **0,7854** ⇒ **≈ 0,215 còn thiếu là hệ thống, không phải nhiễu**. Đây là kết quả **trái chiều, không phải lặp lại**, và nó mạnh hơn cho đề tài vì nói **có thứ thật để mô hình hóa**.
- **Khoảng cách tập trung đúng chỗ cần dự đoán:** trên dải khó 2,0 < PSI < 4,0 (n = 7.601) AUROC rơi **0,9041 → 0,7839** và |r| rơi **0,768 → 0,5291**; con số toàn dải được làm đẹp bởi hai đuôi dễ. Trên 10.219 ca **tự tin** vẫn **19,10% bất đồng ý hoàn toàn**.
- ⇒ **Nhiệm vụ của kiến trúc mới đã được định nghĩa bằng số:** xử lý **dịch chuyển định dạng assay**, chấm trên **dải khó**. Mục tiêu hẹp, đo được, có mốc sẵn.
- **Năm giới hạn của chính phép đo, đã ghi:** (1) 28-mer là chuỗi con của 30-mer nên tile mang thêm tới **2 residue ngữ cảnh** — **phải chạy đối chứng theo offset**; (2) hai assay khác nhau nhiều trục cùng lúc, phép đo chỉ chặn **tổng**; (3) trần 0,9813 là tái lập **kỹ thuật**, nên lạc quan; (4) `setdefault` giữ tile đầu tiên; (5) cả hai assay đều bào tương ⇒ **chưa phải chuyển ngăn tế bào**.
- **Bậc thang còn thiếu hai mức:** mức 4 (qua assay + qua cụm cov80) **phải có** để phát biểu đóng góp, cần huấn luyện; mức 5 (qua ngăn tế bào) cần [C-10](../../DECISIONS.md).

---

## 15/10/2026 (tối) — đánh giá lại mức đóng góp, và một phép đo đổi bài toán

Tài liệu: [contribution-assessment-2026-10-15.md](research/contribution-assessment-2026-10-15.md) và [reframe-options-2026-10-15/](research/reframe-options-2026-10-15/README.md). **Không huấn luyện mô hình nào.** Hai đề xuất mới ghi vào [DECISIONS.md phần C](../../DECISIONS.md): **C-12**, **C-13**.

- **Đánh giá trung thực mức đóng góp theo yêu cầu của Trọng.** Chấm từng thành phần: khoảng trống 89,7% **cao về lập luận nhưng bằng 0 về đóng góp** (nó biện minh cho đề tài, không *là* đề tài); kiến trúc **gần 0** (Degformer đã xuất ma trận 28×20, Yang 2026 là tập mẹ của cổng phơi lộ); benchmark **trung bình và là chỗ thật nhất**, nhưng từng món đều là **thực hành chuẩn** trong DMS nên tính mới là "chưa ai lấp cho nhiệm vụ này", không phải "phương pháp luận mới"; **mô hình thắng baseline chưa tồn tại**. Kết luận: nếu mọi việc còn lại thành công thì mức tương đương **một bài short paper tốt**, không phải đóng góp khoa học mới.
- **Ba nhóm người dùng được chấm lại.** Nhà nghiên cứu khác lợi nhất nhưng vẫn trung bình (n = 91 làm benchmark **thiếu lực để xếp hạng phương pháp** — MDE ≈ 0,071 so với ablation 0,02–0,05); nhà sinh học thực nghiệm **thấp hơn vẻ ngoài** (Jaccard 0,50 buộc công cụ tự hạ tin cậy ⇒ phải gọi đúng là **công cụ sàng lọc ưu tiên**); người làm PROTAC **gần 0** (peptide 28-mer gắn GFP trong bào tương) ⇒ đề nghị gỡ khỏi đề cương. Ghi thành **C-12**, kèm: gỡ chữ "việc chặn duy nhất" (có **hai** việc chặn — rủi ro LeBlanc "thành phần > vị trí" nghiêm trọng hơn lực trên n = 91), đưa phép kiểm ổn định seed/bootstrap **lên trước** huấn luyện, và đặt **điểm kiểm cứng cuối tuần 10**.
- **Phép đo mới, và nó đổi bài toán.** Mở `data/raw/voutsinos-2026/repo/score/degrons.csv.gz` — file đã nằm trên máy từ 13/10 nhưng chưa ai dùng đúng cách. Nó có **212.658 tile / 5.327 gene** và **có sẵn cột sai số từng tile**, nên trần nhãn tính được **chính xác**, không phải ước lượng qua replicate: reliability `degron_score` **0,9807** → trần r = **0,9903**; `abundance_score` 0,8549 → **0,9246**. So với nhiệm vụ chính đang bị chặn ở **n = 91, trần 0,6514**. Script: [probe_tile_reliability.py](research/reframe-options-2026-10-15/probe_tile_reliability.py).
- **Phép đo đó cũng loại một hướng trước khi nó được đề xuất:** `degron_score` và `abundance_score` tương quan **−0,9558** ⇒ gần như cùng một lượng, **không** dùng được như hai assay độc lập.
- **Tra bên ngoài 15/10:** dạng đóng góp "đo trần, phân rã khoảng cách, chứng minh kiến trúc không phá được, rồi đưa một can thiệp có delta dương" **đang được nhận và công bố trong chính năm 2026** — [arXiv 2605.11764](https://arxiv.org/abs/2605.11764) cho PROTAC (random split 0,85–0,91 so với LOTO ≈ 0,67; chặn **0,124 AUROC** do phương sai đo giữa phòng; 8 kiến trúc + ESM-2 3B + 2.000 lượt tinh chỉnh không phá được trần; rank-1 một seed **tụt 0,161** khi kiểm nhiều seed; phần dương few-shot 0,668 → **0,7050**) và bioRxiv 2026.06.29.735309 cho protein–ligand. **Chưa ai làm cho degron.** Cả hai **chưa đọc toàn văn**.
- **Chưa tìm thấy tiền lệ** (tra web + PubMed + Consensus ngày 15/10, **không** phải "chưa ai làm"): phân rã khoảng cách tổng quát hóa cho dự đoán degron; chuẩn hóa hiệu năng theo trần nhãn từ replicate rồi cho thấy **thứ hạng mô hình đổi** (chuẩn mực trong khoa học thần kinh, trong DMS chỉ dùng làm phép kiểm lành mạnh — ProteinGym **tự nêu** vấn đề nhưng không chuẩn hóa); benchmark chuyển assay cho bộ dự đoán degron. Nhưng **ý tưởng trần nhãn có tiền lệ** trong protein ML (arXiv 1809.10389, trần ΔΔG 0,73–0,83; FLIGHTED) ⇒ **không được nói là phát minh**.
- **Voutsinos 2026 là baseline cứng hơn tưởng:** mô hình của chính họ đạt **Pearson 0,82/0,87** so với độ dồi dào đo được **trên tile giữ lại**, và họ báo **phần lớn degron nằm ở vùng bị chôn**. Họ cũng đã công bố một **kết quả âm** trên nhiệm vụ chuyển giao: điểm tile trung bình tương quan **kém** với độ dồi dào protein nguyên vẹn, tốt hơn ở vị trí phơi lộ/vô định hình.
- **Đề xuất C-13:** nhận **H1 (phân rã khoảng cách qua assay/qua ngăn tế bào)** làm mạch chính, **H2 (chuẩn hóa theo trần nhãn)** làm chương phương pháp, **H3 (chuyển giao peptide → protein nguyên vẹn, có điều kiện phơi lộ)** làm chương chuyển giao; H4 (chuyển sang mức tile đơn thuần) **không khuyến nghị** vì phải thắng tác giả bộ dữ liệu trên sân của họ. Giữ tên đề tài và trụ 89,7%; bộ bão hòa chuyển sang vai **sản phẩm ứng dụng**. Việc này **sửa một phần [D-025](../../DECISIONS.md#d-025) đề xuất 2** nên cần Trọng quyết. Mạch trình bày đã điền theo khuôn mười trang của [hướng dẫn trình bày](../../project/advisor-presentation-guide.md).

---

## 15/10/2026 — bắt đầu hỏi đáp đánh giá hiểu biết theo vòng

- Theo yêu cầu của Trọng, tạo [hồ sơ học tập](learning/assessment-log.md): lưu câu hỏi, câu trả lời nguyên văn, đánh giá có bằng chứng, giải thích sửa sai và kiểm tra lại qua các vòng.
- Vòng 1 có sáu câu từ protein/residue/đột biến đến cơ chế degron, diễn giải reporter và mục tiêu đề tài; **đang chờ câu trả lời, chưa đánh giá năng lực**.
- Đối chiếu nguồn hiện hành, ghi cảnh báo lỗi chiều PSI/ΔPSI và trạng thái nhãn cũ trong bài giảng 2, cùng nhận định tính mới ma trận đã bị tiền lệ Degformer cập nhật. Hồ sơ dùng sổ dữ liệu, audit và trạng thái tại [DECISIONS.md](../../DECISIONS.md) làm căn cứ tương ứng; chưa sửa các bài giảng hay thiết kế nghiên cứu.

---

## 15/10/2026 (chiều) — bộ nhân Larsen: giấy phép đã qua, nhưng nó không cứu nhãn residue; và một tiền lệ thứ năm

Tài liệu: [research/larsen-nuclear-and-risks-2026-10-15/](research/larsen-nuclear-and-risks-2026-10-15/README.md), kèm sáu file ghi chép trong `notes/`. **Không huấn luyện mô hình nào.** Hai đề xuất mới ghi vào [DECISIONS.md phần C](../../DECISIONS.md): C-10, C-11.

- **Giấy phép bộ nhân Larsen: cổng chặn đã qua, và đường tải sạch hơn mong đợi.** Điểm mức tile **không** nằm sau CC BY-NC-ND của bài báo mà nằm trong repo GitHub `KULL-Centre/_2025_Larsen_degron_transcriptionfactors` dưới **giấy phép MIT** — một file `annotations/transfac_tiles.csv.gz` **5,77 MB** đã chú giải sẵn **PAP, ADPred, rASA, pLDDT**. Zenodo (cũng MIT) trả **403** từ mạng này; archive ERDA 120,79 GB **không có giấy phép nào** và không cần tới. **Không có deposit GEO/figshare** — đừng đi tìm mã GSE nữa. Chỗ mơ hồ duy nhất còn lại: MIT nominally là giấy phép phần mềm (đề xuất **C-11**: gửi một email xác nhận).
- **Nhưng nội dung bộ nhân bác bỏ kỳ vọng lớn nhất đặt vào nó.** Nó **không phải GPS** mà là sort-seq abundance reporter, tile **30-aa bước 15**, 4 cổng, thang PSI **đảo chiều** và chuẩn hoá lại (bảng GPS của đề tài có 6 bin). Nhãn **chỉ ở mức tile, chỉ trên trình tự hoang dã**: không bão hòa, không alanine scan, **không một nhãn mức residue nào**, và bài **không có một con số mức residue nào**. Reproducibility của nó (Pearson 0,97 giữa replicate) là **mức tile trên toàn dải động**, **không so được** với Jaccard 0,4965 mức residue của đề tài.
- **Và nó không phải test ngoại độc lập về trình tự: 1.583/1.626 (97,4%) TF của Larsen đã có trong peptidome GPS I28 của Zhang 2023**, còn **230/242** protein dùng chung với thư viện bào tương nằm trong **tập train của PAP** (tự đo, giao theo ký hiệu gene nên là **chặn trên**). Phải gọi đúng là **test chuyển assay / chuyển ngăn ở mức tile**. Rò rỉ thực tế thấp hơn con số đó gợi ý, vì nhãn footprint chỉ nằm trên bộ quét và bão hòa — ở đó chỉ **31,2%** TF có mặt, và HSF1, CRX, ZNF140, YBX1, NFE2L1 (ví dụ chính của Larsen) **không có**.
- **⚠ Hệ quả phải sửa: đường thoát ghi ở [bài 9](../../lectures/degron-basics/09-risks.md) rủi ro 1 không tồn tại.** Câu "bổ sung bộ nhân của Larsen 2025 nếu nhãn residue sụp" **đã sai** và đã sửa. Nó không nâng n, không cải thiện Jaccard, không thay mốc ΔPAP mức residue.
- **Nó vẫn giúp ba việc rẻ:** (1) test chuyển assay/chuyển ngăn mức tile với chú giải đã tính sẵn, mốc **PAP Pearson 0,79 / Spearman 0,80** do chính tác giả đo (so 0,87 trên holdout bào tương — ước lượng "chi phí chuyển ngăn"); (2) **chỗ duy nhất rASA/pLDDT có phương sai** (32% tile degron rASA > 0,7; 40% pLDDT < 70) ⇒ nơi kiểm được cổng phơi lộ ở mức tile, biến C-8 từ khẳng định thành số đo được; (3) hai phép so chưa tìm thấy ai làm — QCDPred ↔ thư viện nhân, và PAP tính lại trên ≈ 50.136 tile không chồng (đề xuất **C-10**).
- **⚠ Con số 58.781 không nhất quán trong chính bài báo** (các chỗ khác in 62.992 / 63.230 / 63.011 / 58.992). Đừng trích như con số dứt khoát; phải đếm dòng trong CSV.
- **TIỀN LỆ THỨ NĂM, và nó giết một claim: [Degformer](../../lectures/degron-basics/papers/degformer-2026.md)** (repo GitHub Apache-2.0, tạo 24/03/2026, **không bài báo**) huấn luyện trên **đúng** bảng S1+S4+S7 của Zhang, `MAX_LEN = 28`, và ship script xuất **ΔPSI trên 28 vị trí × 20 acid amin**. ⇒ Câu "chưa tìm thấy sản phẩm nào xuất ma trận 28×20" **phải bị xoá khỏi mọi tài liệu**. **Nhưng nó yếu ở đúng chỗ đề tài mạnh** (đọc toàn bộ mã nguồn + tự đo trên CSV nó ship): split `train_test_split(random_state=42)` **ngẫu nhiên thuần** với **4,09% rò rỉ trình tự y hệt** (2.330/56.927 dòng validation), **9.443** trình tự trùng mang **nhãn trái nhau**, đầu đọc **CLS token** (không có đầu mức residue; heatmap là 532 lượt forward), không cấu trúc, không trần nhãn, **tập blind vắng mặt** ⇒ con số headline **không tái lập được từ repo**, và ρ của nó rất có thể là **Pearson** (hàm duy nhất trong repo là `scipy.stats.pearsonr`), không phải Spearman. ⇒ **Cơ hội, không phải án tử**: baseline nên đánh bại dưới cov80.
- **Thêm hai tiền lệ nữa phải tính:** **DegronMD** (*MBE* 2023) là tiền lệ **đã công bố** có module đột biến mà repo bỏ sót; và **[LeBlanc 2026](../../lectures/degron-basics/papers/leblanc-2026.md)** (*Cell Systems* 17(9):101701) hạ **ba lập luận hỗ trợ** xuống "thực hành chuẩn" (tách abundance/function trên thư viện tile, split cụm protein phân cấp, đối chiếu trần replicate bằng số 0,555 so 0,568). **Và hai câu trong tài liệu repo sai:** MetaDegron và DegronMD **đều có batch submission** nên "batch" không phải điểm khác biệt G3.
- **Rủi ro khoa học mới từ LeBlanc 2026:** với 30 seed × 200 bootstrap họ kết luận *"composition is more important than individual positions"* và filter *"not picking up on specific protein motifs"*. Nếu đúng cho tile degron thì mô hình mức residue có thể đang **khớp nhiễu vị trí**. Họ cho luôn khuôn kiểm: báo độ ổn định trọng số theo vị trí qua seed/bootstrap.
- **Kết quả âm "siết read 10 → 200" nay là phát hiện có trích dẫn.** **DiMSum** (*Genome Biol* 2020) phân rã phương sai thành hai số hạng `m/N` **cộng một số hạng `a` không phụ thuộc số đọc**, và viết thẳng *"increasing sequencing coverage will not lead to reductions in the measurement errors"*, thuốc chữa là *"increasing the number of replicate experiments"*. **Enrich2** (*Genome Biol* 2017) cho mũi độc lập mạnh hơn vì là kết quả thực nghiệm: trên domain C2, lọc theo input count cho điểm **tương đồng *xấu hơn*** tập không lọc. ⇒ Đừng thử lại hướng ngưỡng read; muốn giảm nhiễu thì thêm replicate.
- **Phép tính Spearman–Brown lượng hoá "nhãn lặp một nửa":** độ tin cậy một replicate `ρ₁ ≈ 0,241`, trung bình hai replicate `ρ₂ ≈ 0,388` ⇒ trần Pearson của phần ngữ cảnh học được là **0,295** so với một replicate và **0,374** so với trung bình hai (**+27% tương đối**). Nhưng (a) đó là **bộ quét**; trên bộ bão hòa (nhiễu 16,7%) lợi ích chỉ **≈ +4,5%**, và (b) việc dùng trung bình hai replicate **đã chốt** ở [D-025](../../DECISIONS.md#d-025) mục 3 ⇒ con số này để **biện luận**, không phải để quyết.
- **Đơn vị suy luận là cụm protein, không phải peptide.** Bỏ qua lồng nhau cho tỉ lệ dương giả **trên 45%** ở mức danh nghĩa 5% (Saravanan, Berman & Sober) ⇒ con số cần báo ở bộ bão hòa là **số cụm**, không phải 91; và mức chênh tối thiểu phát hiện được ở n = 91 là **≈ 0,071**, nên **phần lớn ablation (0,02–0,05) sẽ không phân biệt được** — nên cam kết trước điều đó.
- **Tính mới của cổng phơi lộ co lại thành một ablation bắt buộc.** Yang và cộng sự (*PLOS Comput Biol* 22(8):e1014552, 2026) dùng **rASA làm đặc trưng node đầu vào** cộng **attention pooling với vector truy vấn học được** — không phải cổng theo độ lộ, **nhưng** pooling học được trên node đã chứa rASA là **tập mẹ** của cổng đặt tay. ⇒ Không được dựa vào "chưa ai đặt độ lộ gần bước gộp"; phải chạy **ablation ô chéo** (pooling học được ± rASA × cổng tường minh ± rASA) — đúng ô mà chính họ để trống.
- **Tín hiệu thời điểm tốt nhất của phiên:** **không tìm thấy công cụ dự đoán degron mới nào công bố 2025–2026** — PubMed 41 bản ghi, Europe PMC 100 + 127 hit, đọc tiêu đề từng cái; và trong **19 bài trích** Larsen 2025 (9) + Voutsinos 2026 (11), **không bài nào** là mô hình dự đoán degron hay footprint mức residue. Phải viết đúng dạng "đã chạy truy vấn X ngày 15/10, không tìm thấy".
- **Hub học `degron-basics/` đã cập nhật:** [bài 9](../../lectures/degron-basics/09-risks.md) (cả bảy rủi ro, mỗi rủi ro thêm phần "mới 15/10" + cách xử lý xếp theo chi phí + "điều vẫn có thể giết nó"; bảng nợ kỹ thuật từ 5 lên 12 dòng), [papers/larsen-2025.md](../../lectures/degron-basics/papers/larsen-2025.md) (viết lại phần dữ liệu + giấy phép), hai file mới [degformer-2026.md](../../lectures/degron-basics/papers/degformer-2026.md) và [leblanc-2026.md](../../lectures/degron-basics/papers/leblanc-2026.md), [papers/README.md](../../lectures/degron-basics/papers/README.md) (13 → 15 công trình, bảng giấy phép tách "bài báo" khỏi "dữ liệu"), README hub (khối cập nhật mới, danh sách "đừng nói sai" từ 5 lên 8 mục).
- **Chỗ chưa kiểm được, không được dùng để lập luận:** toàn văn Wang & Zheng (*Nat Chem Biol* 2025-11, "degrons beyond short linear motifs") **bị paywall** — chỉ đọc được tóm tắt, và nó là **rủi ro phạm vi** cho khung 28-mer; chồng lặp ở **mức trình tự** (tile 30-mer chứa trọn peptide 23-mer) **chưa đo**; ~60.600 ký tự cuối của toàn văn Larsen chưa đọc; mức xuất ra của **DegPred** vẫn chưa xác minh.

---

## 15/10/2026 — lập luận lại đề tài, và một lỗi lập luận bị phát hiện

Tài liệu: [research/topic-argument-2026-10-15.md](research/topic-argument-2026-10-15.md), thay mạch cũ ở [topic-decision.md](research/topic-decision.md) (11/10). **Không huấn luyện mô hình nào.** Ba đề xuất ghi vào [DECISIONS.md phần C](../../DECISIONS.md): C-7, C-8, C-9.

- **Lỗi lập luận quan trọng nhất, tự phát hiện: cổng phơi lộ không huấn luyện được trên nhiệm vụ chính.** Toàn bộ nhãn huấn luyện là **peptide 28-mer tách rời gắn vào đầu C của GFP**, nên **mọi peptide phơi lộ như nhau** và rASA/pLDDT **không có phương sai** — tham số của cổng **không nhận diện được** từ dữ liệu. Ba báo cáo trước đều không thấy điều này. Hệ quả: thành phần 4 hạ xuống **cơ chế chuyển giao**, ra khỏi đường găng của G2, và **không dành tuần 7–8 cho nó** (đề xuất **C-8**).
- **Lý lẽ kỹ thuật chính đổi sang ngữ cảnh vị trí**, nơi có bằng chứng đo được: đổi kernel 1 → 7 cho **+0,1311** precision@3 mức residue so với chỉ **+0,0032** Pearson trên điểm đoạn — **gấp ~41 lần**. Trần "+0,0032" mà chính tác giả đo **không chuyển sang** nhiệm vụ mức residue. Đây là bằng chứng dương đầu tiên của repo cho hướng mô hình có ngữ cảnh.
- **Cách kể chuyện về PAP được sửa cho đúng.** ΔPAP thua baseline thành phần không phải vì PAP tồi mà vì nó **được huấn luyện cho điểm cả đoạn**, không cho ảnh hưởng đột biến theo vị trí. Câu dẫn nhập đúng và mạnh hơn: **chưa có mô hình nào được huấn luyện cho đúng nhiệm vụ này**. Bốn tiền lệ đều xuất ở mức peptide/motif — đã kiểm, kể cả MetaDegron-D chỉ dùng trình tự.
- **Đề xuất chuyển chỗ đặt đóng góp** từ "kiến trúc mới" sang "**benchmark mức residue đầu tiên** + mô hình thắng trên nó" (**C-7**). Lý do: [D-022](../../DECISIONS.md#d-022) đã cho phép đóng góp dạng công cụ; tính mới kiến trúc đã bị thu hẹp **bốn lần**; còn bộ trần nhãn + baseline + đối chứng + lực + split thì **đã đo xong** và không bài nào trong sáu bài đã đọc có. Rủi ro nhận kèm: [D-012](../../DECISIONS.md#d-012) vẫn đòi đóng góp dương, nên mô hình vượt 0,4897 **vẫn bắt buộc**.
- **Đề xuất đổi thước đo ma trận từ Spearman sang AUROC mức ô** (**C-9**): trần nhãn Spearman chỉ 0,6989 còn trần AUROC đạt 0,9519, và nhiệm vụ của đề tài là tách ô dương chứ không phải xếp hạng mọi ô. Dư địa AUROC **0,1827** lớn hơn dư địa bộ quét (0,1617) trên nhãn ít nhiễu hơn nhiều.
- **Hub học `degron-basics/` đã viết lại theo mạch mới:** bài 5 (bảng mốc mới + hai mục 5.1/5.2 mới), bài 6 (mục 3 viết lại hoàn toàn để hạ cổng phơi lộ), bài 7 (bậc 3 thành bậc chính, AUROC, n = 91), bài 8 (câu đóng góp mới + lý do chuyển tính mới), bài 9 (rủi ro 4c mới, bảng thu hẹp tính mới thêm 3 dòng), README (5 thay đổi lớn, bảng mốc mới, danh sách "đừng nói sai" từ 3 lên 5 mục).
- **Mốc tuần 6 là 16/10** (buổi gặp 1 là 02/10, tuần 4) — tính ra ngày mai, và buổi gặp **chưa định ngày**. Tài liệu trình bày vẫn **chưa sửa** theo yêu cầu của Trọng ngày 14/10.

---

## 14/10/2026 — kiểm lại baseline PAP, chạy đối chứng ΔPAP, kiểm tiền đề cổng phơi lộ

Báo cáo: [research/pap-baseline/](research/pap-baseline/README.md) và
[research/architecture-check/](research/architecture-check/README.md). **Không huấn luyện mô hình nào.**

- **Trọng xác nhận C-6** (bảy đề xuất audit 13/10) → [D-025](../../DECISIONS.md#d-025), và **chấp nhận không có đề tài dự phòng** → [D-026](../../DECISIONS.md#d-026). Mốc G2 từ nay là baseline thành phần **0,4897** kèm trần nhãn **0,6514**; nguồn nhãn chính là **bộ bão hòa**.
- **Tái lập PAP khớp tuyệt đối** sau khi tải lại repo @`9b3eafa6`: kênh nội 0,8239, đầy đủ 0,8690, `cnn2w7` 0,8722 — trùng bốn chữ số với phiên 11/10 **và** khớp hai số công bố (0,82 / 0,87). Đóng việc còn thiếu của audit 13/10.
- **Đối chứng ΔPAP, chưa ai chạy trước đây:** trên nhãn footprint bộ quét, ΔPAP `cnn2w7` đạt precision@3 **0,4270**, `cnn2w1` 0,2959 — **thấp hơn baseline thành phần 0,4884**, kiểm ghép cặp p ≈ 6 × 10⁻¹⁹. Nên mốc 0,4897 của D-025 là mốc khó hơn ΔPAP và đúng để cam kết.
- **Bằng chứng dương đầu tiên cho trục "thêm ngữ cảnh cục bộ":** `cnn2w1` → `cnn2w7` chỉ +0,0032 Pearson trên thang điểm khối (chính tác giả đo), nhưng **+0,1311** precision@3 trên nhiệm vụ residue. Trần "+0,0032" **không áp được** cho thang đo của đề tài.
- **Không có rò rỉ từ tập train PAP:** 0,4268 (protein có trong train) so với 0,4270 (không có). Nên ΔPAP dùng được làm đối chứng toàn tập test.
- **Việc chặn mới, phát hiện ngoài dự tính:** bộ bão hòa sau khi áp đúng ngưỡng peptide degron (PSI WT ≤ 3,0) chỉ còn **91 peptide**, không phải 235. D-025 đề xuất 2 kèm điều kiện tính lại lực; cỡ mẫu thật để tính là **91**. Đường ra nếu thiếu lực: nới ngưỡng lên 3,5 (141 peptide) hoặc chấm mức ô.
- **Thước đo cho ma trận nên là AUROC, không phải Spearman:** trần nửa-chấm-nửa là Spearman 0,6989 so với **AUROC 0,9519**; ΔPAP đạt AUROC 0,7692 nên dư địa 0,1827. Gộp 19 thay thế lên mức vị trí làm Spearman tăng 0,3553 → 0,4130.
- **Tiền đề cổng phơi lộ đúng, hiệu ứng mạnh.** Trên 33.718 biến thể missense của 6 protein bào tương MaveDB kèm AlphaFold v6: Spearman(ΔPAP, độ dồi dào) đi từ **−0,1928** ở residue chôn lên **+0,3733** ở phơi lộ ≥ 0,7; theo pLDDT còn mạnh hơn (−0,1642 ở ≥ 90 lên **+0,3973** ở < 50). Hệ số tương tác ΔPAP × rASA **+0,6625**, bootstrap [0,627; 0,700]. Bỏ PRKN ra vẫn còn **+0,5990** [0,546; 0,648].
- **ΔPAP đổi dấu ở residue chôn** — mô hình degron không có cấu trúc sai dấu ở 47% residue. Cổng phơi lộ không chỉ tăng điểm, nó sửa một lỗi hệ thống. **pLDDT phân tách mạnh hơn rASA** nên nếu chỉ chọn một thì chọn pLDDT (cũng rẻ hơn).
- **Ràng buộc thiết kế mới cho nhiệm vụ phụ:** PSI hoang dã Zhang so với điểm tile Voutsinos cho Spearman 0,7333 toàn cục nhưng chỉ **0,2921** trong nhóm peptide degron → nhãn đoạn phân biệt "có degron hay không" tốt, phân biệt **mức độ** kém. Nhiệm vụ phụ nên là **phân loại**, không phải hồi quy ngang hàng.
- **Rò rỉ chéo nhiệm vụ phải ghi vào benchmark:** 725/770 peptide footprint có tile trong tập train của PAP (dù đo ra không có lợi thế nào).
- Hai tiền đề kiến trúc **vẫn chưa kiểm được** vì cần huấn luyện: cấu trúc túi so với đầu hồi quy theo vị trí, và PLM mức residue so với one-hot.
- Phát hiện vận hành: **AlphaFold DB trả 403 nếu không có User-Agent**; thêm `-A "Mozilla/5.0"` thì tải được. 8 cấu trúc kèm SHA-256 ở `data/raw/alphafold/manifest.txt`.
- **Tra y văn cho cổng phơi lộ (cùng ngày, sau phép đo) — và nó sửa lại kết luận:** [prior-art-exposure-gate.md](research/architecture-check/prior-art-exposure-gate.md). **Tiền đề không mới**: Voutsinos 2026 (ρ = −0,47; Kruskal–Wallis P = 5,4 × 10⁻⁶), Larsen 2025 (\|r\| 0,41 với rASA), QCDPred, DEGRONOPEDIA, JoGo đều đã báo. **Hiện tượng đổi dấu cũng đã có người tìm ra**: Larsen 2025 báo ΔPAP Pearson **0,54** ở IDR của CRX so với **−0,19** ở homeodomain đã gấp. Phép đo của repo là xác nhận lại ở quy mô lớn hơn trên nhãn độ dồi dào, **không phải phát hiện** — đã sửa câu nói quá trong báo cáo và thẻ đề tài.
- **Tìm được tiền lệ phương pháp sát nhất, và nó là baseline bắt buộc:** [Schulze & Lindorff-Larsen, *eLife* 2026](https://doi.org/10.7554/eLife.103721) (cùng nhóm Voutsinos), gộp **6 thí nghiệm VAMP-seq / 31.614 biến thể** trên **đúng 6 protein** mà repo dùng, tách chôn/phơi lộ ở ngưỡng rASA **0,1**, dựng ma trận thay thế theo lớp, đối chứng ThermoMPNN ΔΔG. **rASA một mình cho Spearman 0,45** — mạnh hơn ΔPAP ở khoảng phơi lộ nhất (0,3733). Ghi chú: [schulze-2026.md](../../lectures/degron-basics/papers/schulze-2026.md).
- **Bài đó phát hiện hai lỗi phương pháp của phép đo 14/10:** (a) bộ **GCK** dùng trong tập đo bằng **DHFR-PCA**, không phải VAMP-seq — trộn hai phenotype; (b) **NUDT15 và ASPA là homodimer**, rASA tính trên AlphaFold monomer phân loại sai residue ở mặt tiếp xúc. **Con số hệ số tương tác +0,6625 chưa dùng được** cho tới khi chạy lại.
- **Nhưng Schulze 2026 tự nêu khoảng trống đúng là hướng đề tài:** framework cấu trúc của họ không bắt được **neo-degron ở vị trí phơi lộ**, và họ mời đưa vào "đặc trưng sinh hóa phức tạp hơn". Kèm ca cụ thể **PRKN S109** — residue phơi lộ có profile thay thế giống residue chôn. Dùng làm dẫn nhập.
- **Nơi đặt cổng vẫn chưa tìm thấy tiền lệ:** PAP dùng cấu trúc chỉ để phân tích sau; **MetaDegron-D chỉ dùng trình tự** (khả năng tiếp cận dung môi từ Spider2 chỉ vào nhánh XGBoost, không có attention, chỉ max-pooling); DEGRONOPEDIA dùng ở bước annotation; Schulze 2026 dùng để chia lớp. Ghi là **chưa tìm thấy**, không phải "chưa ai làm", và tính mới của đề tài **không nên** dựa chính vào điểm này.
- Sửa mâu thuẫn trong thẻ đề tài: nhãn mức residue được gọi là "rủi ro số hai" ở một chỗ và "nay là rủi ro số một" ở chỗ khác.

---

## 13/10/2026 — tải đủ bốn nguồn dữ liệu; dựng PSI cho mọi điều kiện; **đo được trần nhãn và lực thống kê**

Báo cáo đầy đủ: [research/full-data-audit/](research/full-data-audit/README.md). Không huấn luyện mô hình nào.

- **Tải đủ:** Mendeley cả **5/5** file (trước có 2), GEO GSE240610, repo Voutsinos @ `9b3eafa6` (trước **đã mất khỏi máy**), 26 score set MaveDB. SHA-256 khớp checksum Mendeley công bố. Zenodo `16925278` trả 403 từ mạng này. Manifest: `data/raw/full-download-manifest.json`.
- **Dựng PSI từ read thô cho mọi điều kiện**, thứ repo chưa từng có: Replicate 2, mẫu BAG6 WT, và cả hai nửa bão hòa. Công thức suy ra và kiểm trên **261.865** giá trị của Replicate 1, lệch ≤ **5,0 × 10⁻⁷**. Tái lập đúng **2.624** footprint.
- **Lỗi trong pipeline công bố của Zhang 2023:** script gộp đọc `header=TRUE` trên file count không có header nên **ăn mất dòng đầu của cả 6 file**; lan cả vào hệ số chuẩn hóa. Ảnh hưởng nhỏ (3 định danh, không có footprint nào) nhưng phải mô phỏng lại mới khớp số tác giả.
- **Rủi ro số hai đã đo được.** ΔPSI rep1 vs rep2 Pearson **0,7229**; nhiễu một replicate SD **0,2974**. Footprint lặp lại ở mức peptide **89,3%**, nhưng **mức vị trí Jaccard chỉ 0,4965** — tức *residue nào* là footprint chỉ lặp lại khoảng một nửa, và đó chính là thứ đề tài dự đoán. Phân rã lại cùng cơ sở macro: dư sau oracle 0,3612, **75,9% là nhiễu**, ngữ cảnh học được cận trên chỉ **0,0872** (không phải 35%). Quét ngưỡng reads 10→200 cho thấy **nhiễu không phải tạo tác của ngưỡng**.
- **Trần thực nghiệm do nhãn đặt ra:** rep1 chấm trên nhãn rep2 cho precision@3 **0,6514**. Baseline thành phần **ước lượng trung thực** chỉ **0,4897**, không phải 0,6045 — cả 0,6045 và 0,7792 đều là oracle đọc nhãn test. Dư địa thật **0,1617**, không phải 0,1747 theo cách đọc cũ.
- **Việc chặn đã trả lời: tập test đủ lực.** Kiểm ghép cặp, SD đo thật 0,2416, d_z 0,669. So baseline trung thực: cần **18** peptide, lực ≈1,00. So mốc 0,6045: cần **209**, lực **0,82–0,94** ở n = 221–322 — đạt nhưng sát biên ở cov50, nên **nên dùng split cov80**.
- **Bộ bão hòa tốt hơn bộ quét trên mọi trục**, và là nguồn duy nhất cho ma trận 28×20: nhiễu chiếm **16,7%** (so 75,9%), ΔPSI giữa hai nửa Pearson **0,8335**, Jaccard ô dương **0,6596**, ma trận phủ **97,9%** của 28×19 trên **235** peptide. Nhưng bộ này **không có phép đo hoang dã nào** — giải bằng ô đồng nghĩa (amino acid thay vào trùng WT) làm WT nội tại, 28 ô/peptide, SD trong peptide 0,031; quy tắc tile (28-mer, bước 23) khớp **128/130** trình tự thật. **130/248** peptide có cả hai nguồn nhãn nên phải cùng phía train/test.
- **Phát hiện ảnh hưởng tới G3:** file Mendeley 393 MB lần đầu tải chứa **mô hình học máy của chính nhóm Zhang** dự đoán PSI toàn peptidome (Pearson **0,8955** ở 10% train, RMSE 0,563 trên 260.989 peptide). Thẻ đề tài trước chỉ biết DEGRONOPEDIA, MetaDegron, PAP. Khác phạm vi (peptide so với residue) nên không phải đối thủ trực tiếp, nhưng phải nêu.
- Nhiễu ~0,30 được xác nhận **bốn lần độc lập**: quét 0,2974, bão hòa 0,2645, peptidome 0,3357, và chính tác giả ghi 0,239 ⇒ tính chất của assay GPS. MLN4924: chỉ **0,76%** peptide bền lên ≥1 PSI khi chặn CRL. MaveDB: **76.194** biến thể duy nhất (ước lượng cũ từ metadata 69.209).
- **Mẫu BAG6 WT không trộn được** với hai replicate kia: ΔPSI chỉ tương quan 0,56–0,58 (so 0,72 giữa hai replicate) và lệch hệ thống −0,11 PSI.
- Bảy đề xuất ghi vào [DECISIONS.md](../../DECISIONS.md) phần C (C-6), **chờ Trọng xác nhận** — gồm sửa cách phát biểu mục tiêu G2 và chuyển trọng tâm nhãn sang bộ bão hòa.
- **Hub học đã đồng bộ:** thêm [bài 10 "Dữ liệu thật trông như thế nào"](../../lectures/degron-basics/10-data-up-close.md) (mô tả dữ liệu dễ hiểu: một dòng gồm gì, PSI tính ra sao, dữ liệu tốt đến đâu) kèm 2 sơ đồ mới. Đồng thời chèn ghi chú cập nhật vào bài 4, 5, 7, 9 và thẻ README của hub, vì các bài đó đang ghi mốc 0,6045 / dư địa 0,1747 và "rủi ro số một là lực thống kê" — nay đều đã lỗi.

---

## 12/10/2026 (tiếp) — tạo hub markdown đơn giản giải thích đề tài

- **Yêu cầu của Trọng:** đọc lại hub HTML ở [lectures/degron-footprint/](../../lectures/degron-footprint/index.html) thấy quá khó hiểu và phức tạp. Cần một hub markdown đơn giản, từ khái niệm cơ bản nhất đến đóng góp, mỗi phần quan trọng có hình, mỗi bài báo một file riêng, trích dẫn dẫn link ngay tại chỗ liên quan.
- Tạo [lectures/degron-basics/](../../lectures/degron-basics/README.md): **9 bài** (khái niệm → cách đo → bài toán → dữ liệu → khoảng trống → giải pháp → đánh giá → đóng góp → rủi ro), **14 sơ đồ tự dựng** dạng SVG, **12 file bài báo** + chỉ mục. Tổng 38 file. Hub HTML cũ giữ nguyên, hai bản trỏ lẫn nhau.
- Nội dung không viết mới mà **rút từ các báo cáo audit đã có**; mỗi con số dẫn link về nguồn gốc trong `research/`. Giữ nguyên nhãn bằng chứng và toàn bộ quy ước ngôn từ của đề tài (không nói "chưa ai dùng MIL", không nói "dùng cấu trúc là phần mới", không nói bản đồ mô hình thành phần phải phẳng, không hứa cải thiện 0,1747).
- Mỗi sơ đồ mang nhãn `SƠ ĐỒ TỰ DỰNG` ở góc trên phải theo quy ước trong [NOTICE.md](../../lectures/degron-footprint/assets/figures/NOTICE.md), để không lẫn với hình của tác giả bài báo. Sơ đồ kiến trúc MIL-Degron mang thêm nhãn `ĐỀ XUẤT, CHƯA KIỂM CHỨNG`.
- Thêm một dòng trỏ tới hub mới trong [lectures/index.html](../../lectures/index.html). Kiểm: 14 SVG hợp lệ XML, mọi hình được tham chiếu đều tồn tại và mọi hình đều được dùng, `check_links.py` không sinh link hỏng mới.

---

## 12/10/2026 (tiếp) — degron được chốt làm **đề tài chính** ([D-023](../../DECISIONS.md#d-023))

- Trọng chốt: degron là đề tài chính, [`plm-calibration-audit`](../../archive/topics/plm-calibration-audit/README.md) (A4) là dự phòng. Kèm thông tin mới: **GVHD vẫn chấp nhận đóng góp dạng công cụ** ([D-022](../../DECISIONS.md#d-022)), nên rào cản C-3 với nhóm A được gỡ.
- Căn cứ chọn degron, tóm từ [khảo sát 7 ứng viên](../../surveys/seven-candidates-comparison-2026-10-12.md): degron là ứng viên **duy nhất có khoảng trống đã chứng minh** chứ không phải "chưa kiểm" — 89,7% peptide (2.353/2.624) có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương, nên mô hình chỉ dùng thành phần bị **chứng minh** không tách được. Thêm: G1 mạnh nhất repo; TC4 (XAI) thỏa mãn bởi chính bài toán vì đầu ra là điểm quan trọng theo residue; có kiến trúc để đề xuất (mục 6 của audit); dữ liệu đã trên máy nên khả thi trong 8–9 tuần.
- **Sửa thẻ trạng thái:** dòng G2 trước đây viết "dư địa chỉ 0,1747" làm đề tài trông yếu hơn mức bằng chứng cho phép. Đã viết lại theo đúng số của [audit](research/composition-context-audit.md): cận chính xác 0,6045 cho lớp mô hình thành phần, oracle không ràng buộc 0,7792, ngẫu nhiên 0,1204, tức +28,9% tương đối nếu đạt trần. Câu "G2 chưa xác lập" **giữ nguyên** vì chưa huấn luyện mô hình nào.
- Dòng G3 cũng được sửa cho đúng: **ba** sản phẩm đã tồn tại (DEGRONOPEDIA, máy chủ web MetaDegron, Colab nhóm PAP), không phải hai. Ứng dụng phải khác biệt được; chỗ khác biệt khả thi là ma trận 28×20 trên nhãn thực nghiệm.
- **Việc chặn gần nhất:** tính lực thống kê trên tập test 221–322 footprint trước khi cam kết huấn luyện. Chưa chạy.

---

## 12/10/2026 — `degron-e3-specificity`: đo giới hạn thành phần và quy mô test theo protein

- Theo đề xuất của sinh viên, tải lại scanning và saturation từ Mendeley v2 vào `topics/degron-footprint/data/raw/`, kiểm đầy đủ SHA-256; script cũ tái lập chính xác 8.831 peptide đạt lọc và 2.624 footprint. Báo cáo: [audit thành phần–ngữ cảnh](research/composition-context-audit.md); script/JSON tại [ghi chú audit](research/e3-labels-audit/README.md).
- **Đo:** 2.046/2.624 footprint có cùng cặp thay thế nhưng khoảng chênh ΔPSI ≥1; oracle trung bình theo cặp P@3 **0,5481**, cận kỳ vọng chính xác **0,6045**, oracle không ràng buộc **0,7792**. Cận Spearman do nới lỏng **0,7931**. Nhãn đánh giá được dùng để tính oracle; chưa là performance mô hình học được và chưa tách nhiễu đo.
- **Protein:** 9.817 peptide / 6.582 accession; footprint trên 2.232 accession, tối đa 7/protein. UniProt hiện tại cung cấp 6.573 accession; có 2.602 footprint khớp trình tự sau bỏ stop cuối. Chia thử 80/10/10 theo cụm full protein, identity 30%: test khớp tham chiếu **271–322** footprint (coverage hai chiều 80%), **221–301** (50%) qua 5 seed. Chưa là benchmark chính thức hoặc bằng chứng không rò rỉ đồng dạng.
- **Đính chính đề xuất:** scanning là ô quan sát từng hàng, không phải marginal; ΔPAP không phải hạng 1 nói chung (mô hình thành phần tuyến tính đã có thể hạng 2). Phương án ma trận đề xuất dùng nhánh thành phần cộng hiệu chỉnh ngữ cảnh hạng thấp, mask WT→WT/stop/nhãn thiếu. Đã sửa các lập luận PAP/phẳng, pooling và nhãn saturation trong [topic-decision.md](research/topic-decision.md), giữ tên và kiến trúc ở trạng thái cũ; phương án ma trận vẫn là đề xuất. Cần xử lý score saturation và chia cả hai nguồn trước khi train.
- **Kiểm:** 200 đối chiếu exhaustive P@3, 4.000 kiểm cận rank, đối chiếu Spearman có tie với SciPy; checksum, tái lập pipeline counts và compile script đạt. Không huấn luyện mô hình. Thay đổi `CLAUDE.md` xuất hiện đồng thời từ ngoài công việc này được giữ nguyên.

---

## 11/10/2026 — hoàn thiện hub học `degron-e3-specificity` sau phiên Claude bị ngắt

- Hoàn thiện [hub năm chặng](../../lectures/degron-footprint/index.html) và [ghi chú vận hành](../../lectures/degron-footprint/README.md): 22 trang HTML gồm 6 bài nền, danh mục/chín trang bài báo và 5 trang đào sâu đề tài. Nối từng phần của [presentation.html](presentation/presentation.html) tới bài đọc sâu; thêm đường về hub từ báo cáo kiểm chứng và danh sách đề tài.
- Đồng bộ phần dạy đề tài với quyết định tái định tâm cùng ngày: footprint theo residue là mục tiêu chính; nhãn toàn đoạn là phụ trợ; E3 là ca nghiên cứu. Viết lại các trang dữ liệu, kiến trúc, đánh giá, câu hỏi mở, Zhang 2023, Larsen 2025, MetaDegron 2024 và phần giải thích vì sao bỏ điều kiện hóa E3. Bổ sung tiền lệ BioBlobs, OmniESI, ELITE ngoài danh mục chín bài chính; sửa tác giả MetaDegron và tên BioBlobs trong trình bày.
- Kiểm [liên kết và nhãn ảnh](../../lectures/degron-footprint/check_links.py): 22 trang, 360 tham chiếu tương đối, không file/anchor hỏng; `git diff --check` đạt. Đã xem ảnh chụp Chrome của hub, hai trang trọng tâm và hình gốc Voutsinos ở độ rộng 500 px, hub ở 780 px: chữ, điều hướng và chú thích đọc được; hình lớn cuộn trong khung. Không chạy thí nghiệm hoặc huấn luyện mô hình.
- **Còn thiếu:** Table S5 do tác giả curate chưa truy được; chưa kiểm toàn bộ tiền lệ mới, chưa dùng thử DEGRONOPEDIA; chưa có kết quả mô hình footprint. Các trang ghi rõ đây là giới hạn, không suy ra kết quả còn thiếu.
- **Đính chính audit:** hai số 27 peptide (được gán E3; có bản đồ bão hòa) không chỉ cùng một tập. Giao của `e3-assignment.json` và `overlap-audit.json` là **23 peptide**; đã sửa [ghi chú audit](research/e3-labels-audit/README.md), quyết định đề tài, presentation và hub. Mục cũ bên dưới ghi “27 có cả hai” là sai theo hai JSON đã lưu.

---

## 11/10/2026 (khuya) — **CỔNG CHẶN 2 KHÔNG QUA**: chỉ 1 E3 đủ mẫu; nhưng nhãn theo residue lớn gấp nhiều lần tài liệu ghi

- **Yêu cầu của sinh viên:** đếm nhãn E3/adaptor thực sự dùng được, và đọc đầy đủ công trình gần nhất có thể trùng ý tưởng.
- **Vòng được paywall:** Table S1–S7 trên PMC trả `Checking your browser - reCAPTCHA`; Europe PMC trả *"not open access"*. Lấy được dữ liệu thô từ **Mendeley Data 10.17632/32h94v2yv2.2** mà chính bài khai báo (3 file ZIP, có SHA-256 trong ghi chú). Zenodo 8103915 chỉ có mã DegronID, không có nhãn.
- **Ghi chú và 7 script tái tạo:** [research_notes/degron-e3-labels/](research/e3-labels-audit/README.md).

### Cổng chặn 2 — kết quả: KHÔNG QUA cho thành phần có điều kiện E3

- **31 screen CRISPR** trong dữ liệu (trừ 3 control) → **27 gán được adaptor**, **25 gán rõ**, **10 E3 khác nhau**.
- **Phân bố giết thiết kế:** KLHL15 **13** peptide · BAG6 **4** · ASB7 **2** · FEM1B **2** · ASB3, KLHL9, FBXW5, FBXO21, FBXO38, DCAF5 **1 mỗi cái**.
- **Bền với ngưỡng:** quét 36 tổ hợp (fdr × lfc × goodsgrna) → gán được 16–29, số E3 8–10, và **số E3 có ≥5 peptide LUÔN đúng bằng 1**. Không ngưỡng nào cứu được.
- **Hệ quả:** thành phần 3 của CMIL-E3 (điều kiện E3 kiểu FiLM) **không huấn luyện được**, và không khái quát sang E3 mới vì chỉ có 10 E3 để học quan hệ trình tự–đặc hiệu. **Không được nói "16 E3 có nhãn CRISPR" như thể đó là 16 lớp dùng được** — con số phải nói là số peptide trên mỗi E3, tức 1–13.
- Một sai sót đã tự sửa trong phiên: lần chạy đầu loại hit theo **tần suất** nên **loại oan KLHL15** (13/31 screen); đã đổi sang loại bộ máy chung theo danh sách tường minh. `APPBP2` xuất hiện ~17/31 screen nhưng lfc 0,8–1,6 nên tự rơi dưới ngưỡng; bài báo cũng tự thừa nhận có nhiễm sgRNA ở một số lô.
- **Chưa lấy được Table S5** (gán E3 do tác giả curate, gồm cả "individual testing") → con số trên là **giới hạn dưới**.

### Phát hiện ngoài dự kiến: nhãn theo residue lớn hơn repo ghi rất nhiều

- **Đột biến quét:** 9.817 peptide trong thư viện, **8.831** có cả hoang dã và biến thể được chấm, **256.711 phép đo** có PSI và reads ≥10, median **28/28 vị trí** mỗi peptide.
- **Peptide thực sự CÓ footprint học được: 2.624** (degron PSI≤3, phủ ≥21 vị trí, có ≥1 vị trí mà đột biến làm PSI tăng ≥1,0); trong đó **2.402 khu trú** (≤6 vị trí quan trọng). **Median 3 vị trí quan trọng trên 28.**
- **Đột biến bão hòa:** **249 peptide × median 560 biến thể = 135.040** định danh, 239 peptide phủ ≥27 vị trí sau lọc reads. Bài báo nói "219 footprint" — đó là tập tác giả curate; dữ liệu thô đỡ được 239–247.
- **Chồng lấn:** **27/31** peptide CRISPR có bản đồ đột biến bão hòa; 25 có cả hai. Bốn peptide thiếu đúng là bốn peptide BAG6 (screen riêng, không phải CRL).
- **Median 3 vị trí quan trọng trên 28** là con số quan trọng nhất của vòng audit: tín hiệu **khu trú thật**, trong khi PAP bất biến hoán vị (Pearson gốc–đảo = 1,000000) nên về nguyên lý không biểu diễn được nó.

### Đọc công trình gần nhất

- **Zhang 2023, toàn văn.** Mô hình của họ là **SVM trên 20 đặc trưng thành phần**, cộng **DegronID** — chấm độ giống motif bằng PSSM dựng từ footprint **đã đo**, rồi gom cụm thứ bậc 40 nhóm. **Không** dự đoán bản đồ đột biến từ trình tự, **không** dùng PLM, **không** có mô hình có điều kiện E3.
- **Bài transcription factor 05/2025, toàn văn.** Đột biến thực nghiệm của họ **có đích, không bão hòa** (xóa đoạn ASCL1 23–40, HSF1 198–217; điểm ZNF140 H323Y); bản đồ thay thế đầy đủ là **in silico** ΔPAP, không phải đo.
- **Tra tiền lệ cho bài toán tái định tâm:** không tìm được ai dự đoán bản đồ độ nhạy đột biến theo residue cho degron. Mọi mô hình degron đã có đều ở mức peptide/protein và phần lớn dựa trên thành phần (PAP kernel=1, SVM-20, QCDPred hồi quy logistic, Degpred BERT, MetaDegron SeqVec, deepDegron chỉ hai đầu chuỗi). **Phản biện phải trích:** một khung học máy 2025 báo rằng 6 điểm thay thế mỗi residue đủ suy ra phần còn lại với ~90% độ chính xác trên dữ liệu quét đột biến sâu nói chung.

### Quyết định của sinh viên: TÁI ĐỊNH TÂM — đã thực hiện xong trong phiên

**Tên mới:** *Dự đoán footprint degron ở mức residue bằng học đa thể hiện với cổng phơi lộ cấu trúc, trên nhãn đột biến thực nghiệm.* Slug giữ `degron-e3-specificity` để không vỡ liên kết.

- **Kiến trúc đổi tên CMIL-E3 → MIL-Degron, 6 thành phần → 5.** Bỏ thành phần điều kiện E3. Lý do giữ cấu trúc túi đổi hẳn: không còn là "nhãn chỉ ở mức peptide" mà là **nối nhãn yếu mức đoạn (212.658) với nhãn mạnh mức residue (256.711) trong một mô hình**. Attention giờ **được giám sát trực tiếp** bằng nhãn đột biến, không chỉ dùng để diễn giải.
- **Thước đo chính mới:** Spearman theo từng peptide trên vector 28 chiều, cộng **precision@3** (chọn 3 vì median số vị trí quan trọng là 3/28), chia **theo peptide** trên 2.624 footprint. Tập kiểm tra khác thư viện: 249 bản đồ thay thế đầy đủ. Đối chứng âm có sẵn: mô hình bất biến hoán vị phải cho bản đồ phẳng.
- **Đối chứng bắt buộc tự đặt ra:** đầu hồi quy theo vị trí **không có MIL**. Khi đã có nhãn mức residue thì MIL không còn bắt buộc — phải tự nói ra điều này, và nếu đối chứng đủ tốt thì báo đúng như vậy.
- **E3 còn lại ở vai trò ca nghiên cứu** trên 27 peptide có cả nhãn E3 và bản đồ đột biến đầy đủ; KLHL15 (13 peptide) là lớp duy nhất đủ thử một đầu ra theo E3.
- **Đã cập nhật:** [topic-decision.md](research/topic-decision.md) (viết lại mục 1–6, thêm 2.1 và 7.1–7.2, thêm 4 quy ước ngôn từ), [presentation.html](presentation/presentation.html) (đổi tiêu đề, bảng đầu vào/đầu ra, phạm vi, bảng kiến trúc 5 thành phần, hộp giới hạn lập luận MIL, bảng dữ liệu + hộp số liệu tự đếm, ba bậc thước đo, bảng năm tiêu chí, mục cổng chặn, thêm tài liệu 14 và đánh số lại 15–18 — kiểm cấu trúc HTML và ID: không lỗi, không trùng), [session-02-prep.md](presentation/session-02-prep.md), [topics/README.md](../README.md), [CLAUDE.md](../../CLAUDE.md).
- **Còn dở:** chưa lấy được Table S5 (gán E3 do tác giả curate — chỉ thêm peptide, không đổi kết luận); sơ đồ SVG luồng dữ liệu vẫn vẽ nhánh điều kiện E3 đã bỏ, hiện chỉ ghi chú bằng chữ trong figcaption, **chưa vẽ lại**; chưa chạy phép đảo thứ tự residue trên sàng lọc 2; chưa chạy baseline, chưa huấn luyện, chưa xây website.

---

## 11/10/2026 (cuối phiên) — khảo sát lại đề tài một cách trung thực; **cổng chặn 1 đã qua**, hai tuyên bố bị thu hẹp

- **Yêu cầu của sinh viên:** khảo sát và đánh giá trung thực lại `degron-e3-specificity` so với các ứng viên còn lại trong repo. Sau đó sinh viên chọn **chuẩn bị slide tuần 6 luôn**, không đếm nhãn E3 trước.
- **Phát hiện về quy trình:** quyết định chốt đề tài ngày 11/10 **không có phép so sánh nào**. `grep` xác nhận tài liệu degron không nhắc DARKIN, và `main-topic-decision.md` cùng bốn ghi chú nền không nhắc degron. Ba cổng bắt buộc G1/G2/G3 chưa từng được áp cho degron. Đã áp lại trong phiên này.
- **Kết quả áp lại ba cổng cho degron:** **G1 (nhãn) đạt, mạnh nhất cả repo** — mọi nhãn là nhãn thực nghiệm. **G2 (đóng góp dương) chưa xác lập** — phụ thuộc số nhãn E3 chưa đếm, và phần bằng chứng vững nhất lại là một kết quả phê phán, đúng loại đã dùng để loại hướng sirtuin. **G3 (website) đạt nhưng yếu nhất** — ba sản phẩm đã tồn tại, không phải hai.
- **CỔNG CHẶN 1 ĐÃ QUA, theo hướng thuận.** Đọc được toàn văn bài degron transcription factor (Larsen và cộng sự, bioRxiv 05/2025): **không** mô hình hóa đặc hiệu E3, **không** kiến trúc mới, **không** nhãn E3 hay CRISPR, **không** có XAI. PAP cùng ESM-1b chỉ dùng so biến thể CRX. Trục của đề tài còn trống.
- **Nhưng cùng bài đó buộc sửa hai chỗ:** họ đã tính rASA và pLDDT từ AlphaFold2 kèm DSSP, và đã làm bản đồ thay thế in-silico ΔPAP → "dùng cấu trúc" và "giải thích biến thể" không còn là phần mới. Và có **bộ dữ liệu thứ tư**: thư viện nhân **58.781 đoạn / 1.626 TF**, cộng **8.645 đoạn / 234 protein** chồng lấn với thư viện bào tương — lựa chọn rẻ hơn cho bậc 2 (cùng assay, khác khoang).
- **PHẢI THU HẸP tuyên bố về nhãn E3.** Đọc toàn văn MetaDegron (*Brief Bioinform* 2024): **đã dự đoán degron theo từng E3 cho 21 E3 ligase**, có máy chủ web với cây chọn E3. Nên không nói "chưa ai làm đặc hiệu E3". Phát biểu đúng: chưa ai huấn luyện trên nhãn adaptor CRL theo CRISPR ở quy mô sàng lọc. Chỗ đó thật sự còn trống — MetaDegron huấn luyện trên **~300 degron curate**, âm tính là **peptide ngẫu nhiên**, chia 90/10, AUC 0,87–0,90, không kiểm soát đồng dạng. Nó cũng đã dùng độ phơi lộ nhưng ở **đầu vào**, không ở bước gộp.
- **PHẢI THU HẸP tuyên bố tính mới kiến trúc (cổng chặn 3).** Chưa thấy ai dùng MIL cho degron — phần đó giữ. Nhưng **BioBlobs** (arXiv 2510.01632, 10/2025) đã dùng đúng attention-based MIL kiểu Ilse 2018 trên protein, và **OmniESI** (arXiv 2506.17963, 2025) đã dùng điều biến có điều kiện enzyme–cơ chất. Kết luận: **mới ở chỗ ghép và chỗ đặt cổng phơi lộ, không mới ở cơ chế** — đúng mức novelty đã dùng để hạ dark kinome ở phép kiểm 6.5b.
- **Hai đối thủ mới chưa có trong repo:** **ELITE** (bioRxiv 11/2025, ProtBERT Siamese xếp hạng E3 cho substrate, Integrated Gradients, âm tính từ Negatome) và **E3TargetPred**. Ở mức cặp protein–protein, không mức residue → không giết đề tài, nhưng chiếm khung và phải vào bảng khảo sát.
- **Phán quyết:** degron **vẫn đứng đầu** các ứng viên trong repo, nhưng vì **G1 và tiêu chí 4**, không vì kiến trúc. Bài bán đề tài đang sai trọng tâm và đã được sửa.
- **Đã làm:** sửa [presentation.html](presentation/presentation.html) — đóng cổng 1, thêm nhóm G vào bảng khảo sát (giờ bảy nhóm A–G), số thật của MetaDegron, hộp giới hạn tuyên bố tính mới, bộ dữ liệu thứ tư, sửa ba ô trong bảng năm tiêu chí, viết lại mục 6.1, thêm bốn tài liệu tham khảo (14–17). Kiểm cấu trúc HTML và ID: không lỗi, không trùng. Thêm [session-02-prep.md](presentation/session-02-prep.md) — kịch bản nói, cây quyết định theo câu trả lời của GVHD, danh sách điều phải tự nói ra.
- **Còn dở:** **đếm nhãn E3 trong Table S3/S4/S6/S7 của Zhang 2023** — giờ là cổng duy nhất còn lại và là con số quyết định G2. Chưa thống nhất tình trạng GPU (10/10 ghi có GPU; mục 9 của topic-decision.md ghi máy không có GPU). Chưa tra danh sách trích dẫn bài 2026 và nội bộ MetaDegron. Chưa huấn luyện mô hình, chưa xây website.

---

## 11/10/2026 — tiếp tục phiên Claude: hoàn thiện giao diện `degron-e3-specificity`

- Hoàn thiện [presentation.html](presentation/presentation.html): hoạt ảnh trên sơ đồ, ô số liệu có nguồn audit, biểu đồ pooling có bảng và giới hạn phép thử, minh họa tương tác peptide/protein, sáng/tối, dừng chuyển động, cuộn hình trên điện thoại và chế độ in.
- Phân biệt hình minh họa với số đo; làm rõ bất biến hoán vị chỉ áp dụng kênh nội cnn2w1, không khái quát sang kênh C-term của PAP.
- Kiểm tra Chromium desktop/điện thoại, sáng/tối, giảm chuyển động, ngoại tuyến/tắt JavaScript, nút tương tác và liên kết nội bộ đều đạt; có kiểm tra ảnh chụp. Chi tiết: [presentation-validation.md](presentation/presentation-validation.md).
- Không thêm thí nghiệm ML. Ba cổng nghiên cứu trong [quyết định đề tài](research/topic-decision.md) vẫn còn; lần này hoàn tất phần trình bày còn dở.

---

## 11/10/2026 (muộn) — **CHỐT ĐỀ TÀI `degron-e3-specificity`**; kiểm chứng xong 10 điểm; GVHD kỳ vọng kiến trúc mới

- **Sinh viên chốt đề tài:** *Dự đoán đặc hiệu E3–degron ở mức residue bằng học đa thể hiện có điều kiện và cổng phơi lộ cấu trúc.* Tài liệu: [topic-decision.md](research/topic-decision.md), [presentation.html](presentation/presentation.html) (bố cục 6 mục, mở bằng `file://`), [báo cáo chi tiết bản 3](research/topic-report/index.html). **Chưa có phê duyệt GVHD.**
- **Thông tin mới từ GVHD: thầy kỳ vọng một kiến trúc chưa ai dùng**, không chấp nhận chỉ một bảng đối chứng có kỷ luật. → đề xuất kiến trúc **CMIL-E3** (học đa thể hiện có điều kiện E3 + cổng phơi lộ ở chỗ gộp), sáu thành phần, **mỗi thành phần gắn với một phép đo tự thực hiện**.
- **Theo yêu cầu: HTML tạo trực tiếp trên hệ thống, không dùng artifact.** Artifact bản 1 (`XAXzVcA6ot1eVVk4927suc`) giờ **lạc hậu**, file trong repo là bản chuẩn.

### Kết quả kiểm chứng 10 điểm — bốn điểm đi ngược bản 1

- **Tái lập được số của bài báo.** Tự dựng PAP bằng numpy từ trọng số công bố: kênh nội **0,8239** (bài: 0,82), đầy đủ **0,8690** (bài: 0,87) trên holdout hiệu dụng 428 gene. Chênh lệch 0,82–0,87 là do kênh C-term phải áp cho **mọi** tile (trong assay mọi tile đều gắn vào đầu C của GFP).
- **Phép đo quan trọng nhất:** đảo ngẫu nhiên thứ tự residue → điểm cnn2w1 **không đổi**, Pearson(gốc, đảo) = **1,000000**. PAP mặc định **bất biến hoán vị**, không biểu diễn được motif nào, vẫn đạt 0,869.
- **BÁC BỎ đóng góp phương pháp của bản 1:** repo có sẵn `cnn2w7` (cửa sổ 7, bắt được motif). Tự chạy: **0,8722 so với 0,8690 = +0,0032**. Trần của trục "thêm năng lực bắt motif" đã do chính tác giả đo.
- **Thêm:** thay gộp trung bình bằng gộp max làm sụt **0,824 → 0,344**; entropy theo vị trí 3,294/3,401 → tín hiệu thang điểm khối **dàn đều, không khu trú**. Hệ quả: kiến trúc khu trú **sẽ không thắng** trên thang điểm khối — phải chốt thước đo với GVHD trước.
- **CỔNG CHẶN ĐÃ MỞ:** GEO **GSE240610** tải được. Table S1 = 52,9 MB, 3 sheet × **475.507 dòng** kèm PSI; thêm RAW.tar 21 MB.
- **BÁC BỎ "chưa ai dùng PLM trên bộ này":** cùng nhóm có bài tiếp theo — degron trên **1.620 (chính xác 1.626) transcription factor**, tiền ấn bioRxiv 17/05/2025, **dùng PAP cùng ESM-1b**, và đã chỉ ra tác động biến thể tương quan độ mạnh degron. Ăn vào một phần đóng góp "giải thích biến thể theo cơ chế".
- **SỬA SỐ MaveDB:** 100.514 → **69.209 biến thể duy nhất** (bản 1 đếm cả dòng không có điểm; trùng lặp dồn ở PRKN và PTEN).
- **Rò rỉ bậc 3 đã định lượng:** 6/9 gene MaveDB có tile, **toàn bộ ở tập train**, nhưng chỉ **132 tile = 0,07%** → sửa gần như miễn phí. 3 gene còn lại (CYP2C9, CYP2C19, LDLR) không thuộc bào tương.
- **Chênh lệch 96 gene đã đặc tả:** phân vùng thật giữ lại **473 gene**; danh sách 527 = 428 đúng + 96 sai + 3 một phần; **45 gene bị giữ lại mà không có trong danh sách**. Nhóm 96 có nhiều tile hơn rõ rệt (64,3 so với 37,0 tile/gene) → suy luận: danh sách là tập tiền tuyển, gene lớn được trả về train.
- **Alignment độc lập làm giảm tuyên bố bản 1:** Smith-Waterman thật (parasail, sàng 6-mer) → **14/428 (3,3%)** gene holdout có họ hàng trong train ở identity ≥30%/coverage ≥50%; **1 ca trùng 100% trên 77 residue** (`AC104389.5` so với **TRIM5**). Bản 1 nói "không có paralog nào" là quá mạnh.
- **Lỗi tái lập trong mã công bố:** `train_cnn2w.py` dùng `ci_aa=1` → trỏ vào cột **DNA**, và A/C/G/T đều là ký hiệu acid amin hợp lệ nên bộ lọc không loại. Chạy mã công bố trên dữ liệu công bố sẽ huấn luyện trên chuỗi DNA.
- **Tài nguyên đã đo:** ESM-2 **35M** 64,6 tile/s → **~55 phút** toàn bộ; **650M** 5,3 tile/s → **~11 giờ**; cache mức residue 650M **32,7 GB** vượt RAM 7 GB. Hugging Face truy cập được.
- **Giấy phép:** repo và Zenodo **MIT**, MaveDB **CC0**, DegronID other-open, hai bản tiền ấn **CC BY-NC-ND**.
- **Còn dở — ba cổng chặn:** (1) đọc toàn văn bài degron TF (`biorxiv.org` bị chặn với WebFetch, chỉ lấy được tóm tắt qua API); (2) mở Table S3/S4/S6/S7 của Zhang 2023 để đếm nhãn E3 dùng được; (3) tra hệ thống tính mới của kiến trúc MIL. Chưa huấn luyện mô hình, chưa xây website.

---

## 11/10/2026 — ứng viên mới: dự đoán degron có bối cảnh cấu trúc; audit bản đồ tile 2026

- **Yêu cầu của sinh viên:** tìm hướng mới hơn, đóng góp rõ hơn, Claude tự quyết; vòng này **bỏ ràng buộc lĩnh vực và độ khớp GVHD**, nhắm **dữ liệu mới cộng trục phương pháp gắn lên nó** (sinh viên chọn qua câu hỏi trắc nghiệm).
- Sản phẩm: [báo cáo HTML](research/topic-report/index.html) — publish tại https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc. Thêm dòng vào [resources.md](../../resources/README.md) và [topics/README.md](../README.md).
- **Hướng đề xuất:** dự đoán degron (tín hiệu phân hủy protein) có tính tới trạng thái phơi lộ cấu trúc. Đóng góp chính là **thang đánh giá ba bậc**: (1) trong cùng sàng lọc, holdout kiểm soát đồng dạng; (2) chuyển giữa hai sàng lọc khác assay; (3) từ peptide tách rời sang protein nguyên vẹn. Bậc 2 và 3 **chưa ai đo**.
- **Tự audit bản đồ tile Voutsinos 2026** (repo `KULL-Centre/_2025_Voutsinos_degron_cytosol`, MIT, có SHA-256): 212.658 tile / 5.327 gene; train 195.629 tile / 4.830 gene; nhãn liên tục −0,144…1,132 (hồi quy thật, không phải phân loại mất cân bằng).
- **Hai giả thuyết của tôi đã sai, ghi lại để không lặp:** holdout chia **theo gene**, và **cả 527 gene holdout đều là cụm đồng dạng đơn lẻ**; tập validation early stopping cũng rời hẳn theo gene (0 gene trùng). **Không được lấy "sửa giao thức đánh giá" làm đóng góp.**
- **Phát hiện audit thật:** 96/527 gene trong `holdout_selection.txt` có **toàn bộ** tile nằm ở tập train, 3 gene giữ một phần → holdout **hiệu dụng 428 gene / 15.820 tile**. Nguyên nhân chưa xác định. Phải dùng số này khi so với Pearson 0,87 của tác giả.
- **Ba tầng dữ liệu:** bộ chính đã tải; bộ thứ hai (Zhang 2023, GPS-peptidome, GEO **GSE240610**, có 219 footprint saturation và residue quan trọng cho >5.000 degron → **ground truth XAI thực nghiệm**) **chưa tải**; bộ thứ ba MaveDB **100.514 phép đo độ dồi dào trên 9 gene** (đã truy vấn API; các bộ trong cùng gene chồng nhau, chưa khử trùng lặp).
- **Tiền lệ:** không được nói "đầu tiên" — đã có deepDegron, Degpred (BERT 2022), MetaDegron (PLM 2024), DegML, và **DEGRONOPEDIA (NAR 2024) là đối thủ trực tiếp ở tiêu chí 5**. Không tìm thấy ai dùng PLM trên bản đồ tile 2026 (chỉ vài lượt tìm web, chưa khảo sát hệ thống).
- **Còn dở:** (1) **cổng chặn** — thử tải GEO GSE240610, nếu không được thì bậc 2 và XAI sụp; (2) kiểm 9 gene MaveDB có nằm trong thư viện tile không; (3) chạy lại baseline PAP trên 428 gene holdout; (4) đọc toàn văn Methods bài 2026. Chưa chốt đề tài, chưa so với dark kinome và SIRT.
