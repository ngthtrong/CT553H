# Kế hoạch hoàn thiện báo cáo luận văn — `report/`

Tạo ngày **18/11/2026** theo yêu cầu của Trọng. Tách **nhánh 3** của [plan.md](plan.md) thành biên bản todo
riêng, chỉ tập trung vào việc hoàn thiện báo cáo LaTeX trong `report/`. Phần mở rộng ứng dụng nằm ở
[plan-system.md](plan-system.md); slide nằm ở nhánh 4 của [plan.md](plan.md).

Đánh dấu `[x]` chỉ khi mục đạt **toàn bộ** tiêu chí nghiệm thu, kèm ngày và đường dẫn bằng chứng. Mục bị cắt
ghi `[-]` kèm lý do, không xoá dòng. Thay đổi phạm vi ghi vào [§12 Nhật ký](#12-nhật-ký-thay-đổi).

**Đã xong ở nhánh 3 cũ (không làm lại):** 3.1–3.6 và 3.8, xem `report/review-validation-2026-11-17.md` và
`report/branch3-validation-2026-11-18.md`. Hai mục còn mở được chuyển sang đây: 3.7 (đồng bộ tên trên slide,
→ mục 8.4) và D-2 (metadata ngày bảo vệ/hội đồng, → mục 7.5).

**Tình trạng ngày 19/11/2026:** đợt 1 xong (5.2 bỏ theo yêu cầu); §8b (V-1…V-6) xong; đợt 2 xong 7.2, 7.4,
7.7, còn một phần ở 7.1, 7.3, 7.6, 8.1; đợt 3 chờ cổng G-SYS (riêng sơ đồ kiến trúc đã làm sớm ở V-3); 7.5 chờ
D-2; 8.2–8.4 ở bước bàn giao. Bản dựng mới nhất: 168 trang, 41 hình, 64 bảng, `make all`/`make check`/kiểm float
PASS cả hai bản (§12, 19/11).

---

## 0. Ràng buộc áp dụng cho mọi mục

Kế thừa [CLAUDE.md](CLAUDE.md) (nhất là *Quy tắc bố cục và đánh số của `report/`*) và
[plan.md](plan.md). Không mục nào dưới đây được vi phạm.

| # | Ràng buộc | Hệ quả khi làm |
| --- | --- | --- |
| Q-1 | Mọi con số trỏ tới file `.json` kết quả, qua generator trong `report/assets/ch4/` (macro `\n...`), không gõ tay | Số mới cần generator đọc JSON. Tên macro không chứa chữ số |
| Q-2 | Giữ trạng thái `development_not_gate_closure`; G2 chỉ đóng trong phạm vi development (D-4, GVHD chưa ghi nhận); không đóng G3; giữ kết quả âm (gt5, negative transfer) | Câu claim theo biên bản D-4 kèm giới hạn L1–L10 |
| Q-3 | Sơ đồ sinh học/model là **hình tự vẽ**, có trích nguồn kiến thức trong chú thích. Không chép hình từ bài báo. Ảnh bên thứ ba chỉ dùng khi giấy phép cho phép (CC BY/CC0) và ghi nguồn + giấy phép | Chú thích dạng "Original schematic, informed by [x]" hoặc "Source: …, CC BY 4.0" |
| Q-4 | Hình là **vector** (TikZ, hoặc PDF sinh từ script). Phông khớp thân bài; một bảng màu chung, an toàn với mù màu; chữ trong hình không nhỏ hơn khoảng 8 pt khi in | Dùng style chung `report/assets/figures/style.tex` (mục 2.0) |
| Q-5 | Sơ đồ mô tả model phải **khớp code đã chạy** (`degron_v3/`, `research/lora-refit-transfer-2026-11-16/model-card.json`): kích thước, rank, kernel, đặc trưng | Ghi file/hàm nguồn trong comment cạnh `tikzpicture` |
| Q-6 | Phần ứng dụng: chỉ trình bày chi tiết **tính năng chính**. Sơ đồ tổng thể (use case tổng thể, kiến trúc, CDM/LDM/PDM, triển khai) **đóng băng** đến khi xong [plan-system.md](plan-system.md) | Không vẽ lại/mở rộng sơ đồ tổng thể trước cổng G-SYS (mục 6) |
| Q-7 | Hình/bảng: float `[htbp]`, `\label` ngay sau `\caption`, dẫn bằng `Figure~\ref`; tên ngắn khớp mở đầu chú thích; không dùng `[H]`/`\clearpage` hàng loạt để che lỗi bố cục | Kiểm bằng `scripts/check_float_references.py` |
| Q-8 | Mỗi đợt kết thúc bằng `make -C report all`, `make -C report check`, kiểm float, đo khoảng trống cả hai bản, xem ảnh render; biên bản **mới** `report/report-validation-<ngày>.{md,json}` | Không ghi đè biên bản cũ; build không phải nghiệm thu nghiên cứu |
| Q-9 | Luận văn viết tiếng Anh, Tóm tắt tiếng Việt; tên chương/phần viết hoa trong nguồn; khung Part 1/2/3 theo mẫu của Khoa | Đổi khung chương cần quyết định D-R1 (mục 1.3) |
| Q-10 | Không sửa `presentation/` khi chưa được yêu cầu; không commit/push khi chưa được yêu cầu | Mục 8.4 chỉ làm khi Trọng yêu cầu |

---

## 1. Tham khảo cấu trúc từ ba luận văn trước

Nguồn: `resources/reference-theses/` và phân tích cũ
[thesis-comparison.md](resources/reference-theses/thesis-comparison.md). Đọc lại mục lục và danh mục hình ngày
18/11/2026. Số trang tính theo PDF.

### 1.1 Cấu trúc đã quan sát

| | T1 — Hồ Quốc Bảo (PLM + mCNN, 96 tr.) | T2 — Nguyễn Duy Khánh (BioFlow-Scope, 212 tr.) | T3 — Thạch Thanh Nhi (genomic prediction, 142 tr.) |
| --- | --- | --- | --- |
| Khung | 5 chương: Intro, Literature, System Design & Methodology, Results, Deployment & Conclusion | **Part 1/2/3 theo mẫu Khoa**: Ch.1 Problem & Requirements, Ch.2 Theory & Technologies, Ch.3 Solution Design, Ch.4 Testing; Part 3 Conclusion | 5 chương: Intro, Theory, **Construction/Training/Experiments**, **Software Implementation & Testing**, Contributions |
| Cơ sở lý thuyết | Peptide → ML truyền thống → PLM → fine-tuning → CNN/mCNN; **7 hình** (luồng đặc trưng, one-hot, transformer embedding, chiến lược đóng băng, mCNN) | Sinh học phân tử → dữ liệu → DAG → provenance → embedding → agent; **18 hình**, có ảnh Wikimedia **ghi nguồn + giấy phép** và **bảng thuật ngữ sinh học** | Bệnh/gene → genomic prediction → biểu diễn → model → đánh giá (GroupKFold vs StratifiedKFold); **3 hình** |
| Nghiên cứu | Chương phương pháp riêng + chương kết quả theo giai đoạn (stage 1→3, ROI, data-centric) | Không có model mới | Một chương riêng: dữ liệu → tiền xử lý → từng pipeline (mục đích, luồng, kết quả, giới hạn) → diễn giải chéo |
| Phần mềm | Ngắn (Ch.5): kiến trúc, 2 kiểu triển khai | Rất dài: C4 container/component, CDM/PDM, từ điển dữ liệu, thiết kế theo vai trò | Chương riêng: kiến trúc, CLI, dashboard theo tab, use case, kiểm thử golden sample, truy vết use case → test |
| Điểm nên học | Mỗi bước tăng độ phức tạp có đối chứng; hình kiến trúc đơn giản, dễ đọc | Bảng thuật ngữ; trích nguồn hình; kế hoạch test theo mẫu Khoa | "Mục đích → luồng → kết quả → giới hạn" cho từng pipeline; bảng truy vết use case → test |
| Điểm tránh | Claim vượt bằng chứng ("paradox", "safe") | Ảnh giao diện chụp từ mock khi backend lỗi | Nhiều mục vận hành (checklist, log) làm loãng chương chính |

### 1.2 Hiện trạng báo cáo (sau 18/11)

157 trang, 28 hình, 63 bảng. Khung Part 1/2/3, Ch.1–4 giống T2.

- **Chương 2 có 2 hình**, cả hai là sơ đồ khối chữ. Đây là khoảng trống lớn nhất so với T1/T2, ở đúng phần
  GVHD và hội đồng dùng để đánh giá mức hiểu sinh học và model.
- **Chương 3 trộn hai mạch:** thiết kế ứng dụng (§3.1–3.3, §3.6–3.7) và phương pháp nghiên cứu (§3.4
  *Research Progress and Data Evolution*, §3.5 *Method and Model Design* gồm `campaign-methods`,
  `prioritization-methods`).
- **Chương 4 rất nặng:** 34 bảng (32 bảng kết quả thực nghiệm), sau đó là kế hoạch test và nghiệm thu phần mềm.
  Mạch nghiên cứu dài và khó theo dõi.

### 1.3 Quyết định cấu trúc — D-R1 ✅ 18/11/2026: Trọng chốt **phương án A**

| Phương án | Mô tả | Ưu | Nhược |
| --- | --- | --- | --- |
| **A — giữ 4 chương, tách mạch bên trong** *(khuyến nghị)* | Ch.3 chia hai phần rõ: **3A Research Method Design** (dữ liệu, nhãn, split, model, giao thức, refit) và **3B Software Design** (tính năng chính; tổng thể sau G-SYS). Ch.4: **4A Experimental Results** (theo câu hỏi nghiên cứu) và **4B Software Testing**. Bảng phụ chuyển Phụ lục B | Đúng mẫu Khoa và template; T2 cùng khung đã được chấp nhận; ít xáo trộn nhãn/tham chiếu | Ch.3/Ch.4 vẫn dài; tiêu đề chương không nói rõ phần nghiên cứu |
| B — 5 chương như T1/T3 | Theory → Method → Results → Software → Conclusion | Mạch nghiên cứu liền; giống hai luận văn tin sinh cùng GVHD | Lệch dàn ý của Khoa; đổi nhiều `\include`, nhãn, generator; cần GVHD duyệt |

**Đã chốt phương án A** (Trọng, 18/11/2026); GVHD chưa ghi nhận. Các mục 2–5 viết theo phương án A. Phần lớn nội dung (hình Ch.2, hình phương pháp,
tính năng chính) dùng được cho cả hai phương án.

---

## 2. Công cụ vẽ sơ đồ — kết quả tìm kiếm ngày 18/11/2026

| Nguồn | Kết quả | Dùng vào đâu |
| --- | --- | --- |
| claude.ai skills (`SearchSkills`: scientific diagram, tikz, biology illustration, architecture, thesis) | **Không có** skill phù hợp | — |
| Skill có sẵn `artifact-diagramming` | Hướng dẫn vẽ sơ đồ thể hiện **cơ chế thật**, nhưng xuất HTML/SVG cho Artifact, không phải LaTeX | Chỉ dùng nguyên tắc (mỗi mũi tên là một bước có thật, nhãn nằm trên đối tượng), không dùng đầu ra |
| Plugin **Diagrams** (Anthropic Directory, cộng đồng) | PlantUML, Mermaid, GraphViz, D2, C4, ERD qua **Kroki.io**; xuất PNG/SVG | Sơ đồ phần mềm ở đợt 3. **Lưu ý:** gửi mã sơ đồ lên kroki.io (dịch vụ ngoài). Chỉ dùng cho sơ đồ không chứa dữ liệu riêng, hoặc tự host Kroki bằng Docker (máy đã có Docker) |
| TeX Live trên WSL | Có `tikz` (đang dùng), `chemfig`, `pgfplots`, `tikz-3dplot`, `forest`, `smartdiagram`, `tikz-network`, `circuitikz` | Mọi sơ đồ sinh học/model (mục 3–4) |
| Python | `matplotlib` 3.11 có trong `.venv` ở gốc repo (không có ở Python hệ thống) | Hình minh hoạ dựa trên dữ liệu, xuất PDF vector |
| Chưa cài | graphviz, inkscape, plantuml, mermaid-cli, pymol | Chỉ cài khi cần (mục 2.0) |

**Khuyến nghị theo loại hình:**

| Loại hình | Công cụ | Lý do |
| --- | --- | --- |
| Cơ chế sinh học (UPS, degron, GPS/FACS) | TikZ, style chung | Vector, phông khớp, sửa được, không vướng bản quyền |
| Amino acid, liên kết peptide, nhóm tính chất | `chemfig` + TikZ | Công thức hoá học chuẩn trong LaTeX |
| Kiến trúc model (ESM-2, LoRA, head CNN/mCNN) | TikZ (khối + kích thước tensor ghi trên cạnh) | Khớp code được (Q-5); T1 dùng kiểu khối tương tự |
| Minh hoạ có số liệu (phân bố PSI, xây nhãn ΔPSI, reliability) | `matplotlib`/`pgfplots` từ JSON, qua generator | Q-1: số trỏ JSON |
| Cấu trúc 3D protein (tuỳ chọn) | PyMOL bản mở hoặc ảnh AlphaFold DB (CC BY 4.0, ghi nguồn) | Chỉ khi thật sự minh hoạ được điều cần nói |
| Sơ đồ phần mềm (đợt 3) | TikZ như hiện tại; tuỳ chọn PlantUML qua Kroki tự host | Giữ đồng bộ với 6 sơ đồ TikZ đã có |

### 2.0 Hạ tầng hình · 1 ngày · đợt 1 · [x] 18/11 — `report/report-validation-2026-11-18.md`

| Việc | Chi tiết |
| --- | --- |
| Style | `report/assets/figures/style.tex`: bảng màu (Okabe–Ito), kiểu node (protein, enzyme, tensor, dữ liệu, quyết định), mũi tên, cỡ chữ `\footnotesize`; nạp trong `template/packages.tex` của bản làm việc |
| Thư mục | Mỗi hình phức tạp một file `report/assets/figures/<tên>.tex`, chương chỉ `\input`, để kiểm tra riêng được |
| Xem nhanh | `report/scripts/preview_figure.py <tên>`: dựng một hình đứng riêng ra PNG để xem, không cần build toàn bộ |
| Cài thêm (nếu chọn) | Lệnh để Trọng tự chạy: `sudo apt install graphviz` (sơ đồ phần mềm), `sudo apt install pymol` (cấu trúc 3D) |
| Nghiệm thu | Hai hình Ch.2 hiện có chuyển sang style mới mà nội dung không đổi; build PASS |

---

## 3. Chương 2 — Cơ sở lý thuyết: bổ sung sơ đồ · đợt 1

Mục tiêu: **2 → khoảng 9–10 hình**, mỗi hình gắn với một khái niệm mà Ch.3/Ch.4 dùng lại. Mỗi hình có chú
thích nêu nguồn kiến thức và giới hạn (Q-3). Thêm **bảng thuật ngữ sinh học** như T2.

| # | Hình | Nội dung bắt buộc | Công cụ | Nguồn kiến thức | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | Amino acid và tile peptide | 20 amino acid theo nhóm tính chất (kỵ nước, phân cực, tích điện ±, đặc biệt G/P/C); liên kết peptide; tile 28 residue với vị trí 1–28 và một phép thay thế | `chemfig` + TikZ | giáo trình hoá sinh chuẩn | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.2 | Hệ ubiquitin–proteasome chi tiết | Thay hình 2.1 hiện tại: E1 hoạt hoá Ub → E2 → E3 nhận degron → chuỗi poly-Ub → proteasome 26S tháo gấp và phân giải → tái chế Ub; ghi chú Ub có vai trò không phân giải | TikZ | Varshavsky 2019; Koren 2018 | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.3 | Loại degron và hiệu ứng đột biến | N-degron, C-degron, degron nội; tile reporter nằm ở đâu; thay thế có thể làm mạnh/yếu tín hiệu → PSI giảm/tăng; điều kiện che khuất (gấp, đối tác, PTM) | TikZ | Varshavsky 2019; Zhang 2023 | 0,75 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.4 | **Thí nghiệm GPS** | Cấu trúc reporter (DsRed – IRES – GFP–peptide); thư viện → tế bào → FACS theo tỉ số GFP/DsRed vào 6 bin → giải trình tự → đếm read theo bin → công thức PSI (phương trình `eq:psi-bins`) | TikZ | Yen 2008; Zhang 2023; `research/full-data-audit/build_psi.py` | 1,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.5 | Từ đột biến bão hoà đến nhãn ΔPSI | Thay hình 2.2 hiện tại: WT tile → 28×19 biến thể → PSI từng biến thể → ΔPSI = PSI(mut) − PSI(WT) → ma trận; scanning khác saturation ở đâu; khoảng giới hạn vật lý 1−PSI(WT) ≤ ΔPSI ≤ 6−PSI(WT) | TikZ (+ heatmap nhỏ minh hoạ) | `EXECUTION-PROTOCOL.md` | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.6 | Protein language model | Tiền huấn luyện masked LM; encoder transformer; embedding từng residue; cách lấy Δsite và meanΔ giữa mutant và WT | TikZ | Lin 2023; Vaswani 2017; `degron_v3` | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.7 | Frozen, fine-tune toàn phần và LoRA | Ba cột so sánh khối nào được học; LoRA trên Wq, Wv: W′ = W + (α/r)·BA với **r = 8, α = 16** (macro `\nTAdapterRank`, `\nTAdapterAlpha`); số tham số học | TikZ | Hu 2022; `model-card.json` | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.8 | Head pointwise, CNN, mCNN | k = 1, k = 5, nhánh song song k = 3/5/7 trên chuỗi đặc trưng; chỗ ghép đầu vào tâm/cặp chuỗi | TikZ | `degron_v3` (hàm định nghĩa head) | 0,75 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.9 | Chia dữ liệu theo nhóm protein | Chia ngẫu nhiên theo ô (rò rỉ do peptide/protein đồng dạng) so với chia theo cụm MMseqs2 cov80; fold ngoài, validation trong, bootstrap theo cụm | TikZ | `EXECUTION-PROTOCOL.md`; T3 Hình 2.3 (ý tưởng) | 0,75 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.10 | Hiệu chuẩn xác suất | Reliability diagram khái niệm; Platt: P = σ(a + b·score); Brier và ECE đọc thế nào | `pgfplots` (dữ liệu minh hoạ tổng hợp, ghi rõ) | Platt 1999 (**chưa có** trong `references.bib`, cần thêm); `tab-cal-*` | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |
| 3.11 | Bảng thuật ngữ sinh học | Degron, E3, PSI, ΔPSI, tile, saturation, scanning, WT, reporter, FACS bin, cụm cov80… mỗi mục một câu theo nghĩa **trong đề tài** | bảng `longtable` | — | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18.md` |

**Nghiệm thu chương:** mỗi hình được dẫn trong thân bài trước hoặc cùng trang; Ch.2 không thêm claim mới về
kết quả; Q-5 đã đối chiếu code cho 3.6–3.8 (ghi file/hàm trong comment); ảnh render ở cỡ đọc được không có chữ
chồng.

---

## 4. Chương 3A — Thiết kế phương pháp nghiên cứu · đợt 1

| # | Việc | Chi tiết | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 4.1 | Tách mạch | Gom §3.4 *Research Progress and Data Evolution*, §3.5 *Method and Model Design*, `campaign-methods`, `prioritization-methods` và phần refit của `transfer-refit` vào phần 3A, đứng trước phần ứng dụng (theo D-R1) | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 4.2 | Sơ đồ quy trình nghiên cứu tổng thể | Nguồn (Zhang 2023, Voutsinos 2026, …) → dựng nhãn/QC → split W/T theo nhóm → arm B/D/E → họ model (ridge W5, frozen pLM, CNN/mCNN, LoRA) → OOF + calibration → refit cuối → chấm T một lần → model card → ứng dụng. Ghi rõ mốc **khoá protocol trước khi xem T** | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 4.3 | Sơ đồ kiến trúc LoRA-D đầy đủ | Đầu vào (tile WT + mutant), ESM2-35M với adapter, đặc trưng, head, ensemble 3 seed, calibrator 3 lớp; ghi kích thước tensor; khớp `model-card.json` và code (Q-5) | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 4.4 | Sơ đồ thiết kế thí nghiệm | Ma trận câu hỏi → so sánh ghép cặp → khoảng tin cậy (Bonferroni, bootstrap cụm); giúp đọc Ch.4A | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 4.5 | Viết theo khuôn "mục đích → luồng → kết quả trỏ Ch.4 → giới hạn" (học T3) | Mỗi thí nghiệm chính một đoạn ngắn; chi tiết vận hành (runner, checkpoint) chuyển Phụ lục A §campaign | 1 ngày | [x] 18/11 — `report/report-validation-2026-11-18-wave2.md` |

---

## 5. Chương 3B — Ứng dụng: chỉ tính năng chính · đợt 1

Chỉ đào sâu **5 tính năng mang luận văn** (đang có ở `sec:app-features`). Mỗi tính năng theo cùng khuôn:
mục đích/người dùng → luồng → quy tắc khoa học phải tôn trọng → bằng chứng (test/số đo) → ảnh chụp.

| # | Tính năng | Bổ sung | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 5.1 | Ma trận hiệu ứng + footprint | Sơ đồ luồng riêng: nhập → chuẩn hoá → cổng miền → chấm 532 ô → hiệu chuẩn → hiển thị (cảnh báo trước số) | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 5.2 | Cổng miền hai tầng R3 | Sơ đồ quyết định: tầng 1 (PSI đo) / tầng 2 (PSI dự đoán) → σ(…) → in/borderline/out → từ chối/override có ghi lại | 0,5 ngày | [-] 18/11 — bỏ theo yêu cầu của Trọng; cổng đã mô tả đủ bằng chữ |
| 5.3 | Xếp hạng, shortlist, panel top-k | Nối với kết quả replay ngân sách cố định ở Ch.4A; quy tắc chỉ xếp hạng trong một tile | 0,25 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 5.4 | Job bền (batch, cả protein) | Giữ sơ đồ sequence/state đã có (thuộc tính năng, không phải sơ đồ tổng thể); thêm hình chia tile bước 23 | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 5.5 | Provenance, export, import/so sánh | Giữ sơ đồ import–comparison; nêu ba quy tắc bắt buộc (không train lại, chỉ so endpoint tương thích, missing không thành 0) | 0,25 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |
| 5.6 | **Đóng băng sơ đồ tổng thể** | Use case tổng thể (Hình 3.1), kiến trúc/triển khai, CDM/LDM/PDM (bảng 19 bảng), §Local Execution View: giữ nguyên, thêm comment `% FROZEN until plan-system G-SYS` trong nguồn, không đầu tư thêm | 0,1 ngày | [x] 18/11 — `report/report-validation-2026-11-18-ch3.md` |

---

## 6. Đợt 3 — cập nhật sau khi hoàn thành hệ thống (cổng G-SYS)

**Cổng G-SYS:** [plan-system.md](plan-system.md) đạt mốc nghiệm thu của đợt được chọn đưa vào luận văn
(`system/app/acceptance-system-<ngày>.json` tồn tại). Trước cổng, không làm các mục dưới đây.

| # | Việc | Chi tiết | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 6.1 | Use case tổng thể | Vẽ lại từ SRS mới (thêm use case của plan-system: chọn model, so sánh, báo cáo…) | 0,5 ngày | [ ] |
| 6.2 | Kiến trúc hệ thống và triển khai | Từ `docker-compose.yml` và code thực tế; có thể theo kiểu C4 container như T2 | 1 ngày | [ ] |
| 6.3 | CDM/LDM/PDM | Chạy lại `dump_app_schema.py` → `build_app_assets.py`; migration mới (từ `0005`) | 0,5 ngày | [ ] |
| 6.4 | Chương 1 đặc tả | Cập nhật use case/FR/NFR theo SRS mới; FR-20 giữ trạng thái retired | 1 ngày | [ ] |
| 6.5 | Ch.4B số test và hiệu năng | Generator đọc biên bản `acceptance-system-<ngày>.json` mới; giữ nguyên số cũ nếu đợt hệ thống không đổi chúng | 0,5 ngày | [ ] |
| 6.6 | Tính năng mới đủ quan trọng | Chỉ thêm vào 3B nếu là tính năng chính (ví dụ 1.3 phân tán seed, 2.1 footprint cấp protein); còn lại một dòng trong bảng chức năng | 1 ngày | [ ] |
| 6.7 | Phụ lục A | Chụp lại ảnh bằng `e2e/screenshots.spec.ts` trên **bản sao** DB; cập nhật hướng dẫn | 0,5 ngày | [ ] |

---

## 7. Chương 4A, mở đầu, kết luận, phần đầu · đợt 2

| # | Việc | Chi tiết | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 7.1 | Ch.4A theo câu hỏi nghiên cứu | Xếp lại kết quả theo câu hỏi (độ phủ nhãn, biểu diễn, LoRA, hiệu chuẩn, ưu tiên hoá, chuyển nguồn T); mỗi mục mở bằng câu trả lời ngắn có nhãn bằng chứng | 2 ngày | [~] 18/11 — đoạn dẫn theo RQ + Part A/B; giữ thứ tự thời gian có chủ đích (`report/report-validation-2026-11-18-wave2.md`) |
| 7.2 | Giảm bảng trong mạch chính | Mục tiêu đề xuất: Ch.4 ≤ 30 bảng; bảng seed/epoch/inventory/kiểm tra phụ chuyển Phụ lục B; ưu tiên hình cho kết quả chính | 1,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-wave2.md` |
| 7.3 | Mở đầu (Part 1) | Mục tiêu, phạm vi, đóng góp khớp đúng những gì Ch.3/Ch.4 chứng minh; bỏ chữ "progress report" khi bản nộp chính thức | 0,5 ngày | [~] 18/11 — sửa câu sai, mô tả Part A/B; bỏ "progress report" khi chốt bản nộp |
| 7.4 | Kết luận (Part 3) | Đóng góp, giới hạn L1–L10, hướng phát triển (gồm nhóm 6 của plan-system) | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-wave2.md` |
| 7.5 | Metadata (D-2) | `\ThesisDate`, `\DefenseDate`, hội đồng — **chờ thông tin**, không tự điền | 0,1 ngày | [ ] |
| 7.6 | Abstract/Tóm tắt bản cuối | Viết lại sau 7.1–7.4; mỗi bản một trang | 0,5 ngày | [~] 18/11 — đã đối chiếu, vẫn một trang; viết lại bản cuối sau D-2/bản nộp |
| 7.7 | Danh mục thuật ngữ và tài liệu tham khảo | Bổ sung thuật ngữ từ 3.11; kiểm mọi nguồn trích trong chú thích hình có trong `references.bib` | 0,5 ngày | [x] 18/11 — `report/report-validation-2026-11-18-wave2.md` |

---

## 8. Hình thức, ngôn ngữ, bàn giao

| # | Việc | Chi tiết | Ước lượng | Trạng thái |
| --- | --- | --- | --- | --- |
| 8.1 | Rà ngôn ngữ tiếng Anh | Thống nhất thuật ngữ (tile/window, arm, recipe); bỏ câu lặp và câu mang tính nhật ký ("this review", ngày tháng không cần thiết) | 2 ngày | [~] 18/11 — mới sửa có mục tiêu; chưa rà toàn văn |
| 8.2 | Rà bố cục cuối | Một mặt và hai mặt; trang có hình/bảng và trang liền kề; khoảng trống > 1/3 phải có lý do | 0,5 ngày | [ ] |
| 8.3 | Biên bản validation cuối | `report/report-validation-<ngày>.{md,json}`, hash PDF | 0,25 ngày | [ ] |
| 8.4 | Đồng bộ tên trên slide (3.7 cũ) | Chỉ khi Trọng yêu cầu làm nhánh 4 (Q-10) | — | [ ] |

---

## 8b. Phản hồi trực quan và bố cục — 18/11/2026

Yêu cầu của Trọng ngày 18/11/2026 sau khi xem bản dựng đợt 1–2. Mục **V-3 mở ngoại lệ cho Q-6**: sơ đồ kiến trúc
tổng thể được làm lại ngay theo yêu cầu, không chờ G-SYS. Khi plan-system thêm thành phần mới, sơ đồ vẫn cập nhật
lại ở đợt 3 (6.2).

| # | Việc | Chi tiết | Tiêu chí nghiệm thu | Trạng thái |
| --- | --- | --- | --- | --- |
| V-1 | Trực quan hoá các khối chữ | (a) khối *Bounds* của Hình 2.5 → trục PSI 1–6 có PSI(WT) và đoạn ΔPSI khả dĩ; (b) khối *Thousands of cells…* của Hình 2.9 → minh hoạ ô so với nhóm và phép bootstrap theo nhóm; (c) Hình 3.1 → mỗi bước có biểu tượng (dữ liệu, ống nghiệm/đọc trình tự, cụm, mô hình, khoá, hộp model, ứng dụng); (d) Hình 3.2 → ma trận câu hỏi × yếu tố có biểu tượng "thay đổi/giữ cố định" | Ý chính đọc được từ hình, không chỉ từ chữ; không chồng chữ | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |
| V-2 | Vẽ lại Hình 3.3 (lỗi thời) | `nested-evaluation.pdf` (06/11, ghi "T chỉ đánh giá W5-D") → TikZ theo style chung; thêm nhánh refit LoRA-D chấm T một lần (17/11) | Khớp `EXECUTION-PROTOCOL.md` và `PROTOCOL.md` refit; nhãn `fig:campaign-nested` giữ nguyên | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |
| V-3 | Sơ đồ kiến trúc hệ thống chi tiết | Làm lại Hình kiến trúc: trình duyệt, nginx, API, worker, PostgreSQL/SQLite, volume, ETL, model registry (npz + LoRA-D), cổng R3, nguồn tham chiếu; **logo công nghệ** (React, Vite, nginx, FastAPI, Python, PostgreSQL, SQLite, Docker, PyTorch) vẽ từ dữ liệu SVG của Simple Icons (CC0) bằng TikZ `svg.path`; chú thích ghi logo là nhãn hiệu của chủ sở hữu | Khớp `docker-compose.yml` và code; vector; không chồng chữ | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |
| V-4 | Sửa chữ chồng và mũi tên nhỏ | Hình 3.8 (trạng thái job/item) và mọi sơ đồ TikZ cũ của Chương 3; đầu mũi tên chung ≥ 2,2 mm | Xem ảnh render từng hình ở cỡ đọc được | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |
| V-5 | Hình/bảng cắt ngang đoạn văn | Kiểm tự động bằng toạ độ dòng (`pdftotext -bbox-layout`): float nằm giữa hai phần của cùng một đoạn, trong trang hoặc qua ranh giới trang. Sửa bằng vị trí float trong nguồn, kích thước, hoặc chính sách float chung; không dùng `[H]` hàng loạt | 0 chỗ cắt đoạn còn lại, hoặc mỗi chỗ còn lại có lý do ghi trong biên bản | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |
| V-6 | Bảng tràn lề | Kiểm tự động mực ngoài vùng chữ (lề trái 3,5 cm, phải 2 cm) ở cả hai bản. Lần kiểm đầu: chỉ Bảng 4.29 (bộ test) tràn → chuyển sang `tabularx` có cột xuống dòng | 0 trang có mực ngoài vùng chữ, trừ bìa | [x] 18/11 — `report/report-validation-2026-11-18-visual.md` |

## 9. Tổng quan thứ tự và ước lượng

| Đợt | Mục | Ước lượng | Mốc | Trạng thái 19/11 |
| --- | --- | --- | --- | --- |
| **Đợt 1 — ngay** | 1.3 (D-R1), 2.0, 3.1–3.11, 4.1–4.5, 5.1–5.6 | ≈ 17 ngày | Ch.2 đủ hình; Ch.3 tách mạch; tính năng chính hoàn chỉnh | [x] xong 18/11; 5.2 `[-]` |
| **Đợt 2** | 7.1–7.4, 7.6, 7.7, 8.1 | ≈ 8 ngày | Mạch nghiên cứu gọn; mở đầu/kết luận khớp | [~] 7.2, 7.4, 7.7 xong; 7.1, 7.3, 7.6, 8.1 một phần |
| **Đợt 3 — sau G-SYS** | 6.1–6.7 | ≈ 5 ngày | Phần hệ thống tổng thể cập nhật một lần | [ ] chờ G-SYS; kiến trúc làm sớm ở V-3 |
| Hoàn tất | 7.5 (khi có D-2), 8.2, 8.3 | ≈ 1 ngày | Bản nộp | [ ] chờ D-2 |

**Tổng ≈ 31 ngày làm việc.** Đợt 1 có thể chạy song song với đợt 1 của plan-system, vì hai phần không chạm
cùng tệp. Nếu deadline gần: giữ 3.2, 3.4, 3.5, 3.7, 4.2, 4.3, 5.1–5.6 và 7.6; các hình còn lại của Ch.2 thay
bằng đoạn văn.

```text
D-R1 ──> 4.1 tách mạch ──> 4.2–4.5 ──> 7.1 Ch.4A theo câu hỏi ──> 7.3/7.4 ──> 7.6 Abstract cuối
2.0 style ──> 3.1–3.10 hình Ch.2 ──> 7.7 thuật ngữ/tham khảo
5.1–5.5 tính năng chính        G-SYS (plan-system) ──> 6.1–6.7
                                     D-2 ──> 7.5 ──> 8.2/8.3
```

---

## 10. Rủi ro và phương án cắt

| Rủi ro | Phương án |
| --- | --- |
| Hình sinh học sai chi tiết cơ chế | Chỉ vẽ điều có nguồn; chú thích ghi "conceptual"; nhờ GVHD xem trước bộ hình Ch.2 |
| Sơ đồ model lệch code | Q-5: đối chiếu từng con số với `model-card.json`/code trước khi build |
| D-R1 chọn phương án B muộn | Viết nội dung theo đơn vị mục, nhãn ổn định, để chuyển chương chỉ là đổi `\include` |
| plan-system kéo dài, G-SYS không kịp | Bản nộp dùng sơ đồ tổng thể hiện có (đã khớp code ngày 17/11) và ghi phạm vi v0.2 |
| Thêm hình làm vỡ bố cục | Q-7, Q-8: xem ảnh render sau mỗi hình; ưu tiên chỉnh kích thước trước khi ép trang |
| Dùng Kroki.io làm lộ nội dung | Chỉ dùng bản tự host, hoặc giữ TikZ |

---

## 11. Mốc nghiệm thu

| Mốc | Điều kiện | Trạng thái 19/11 |
| --- | --- | --- |
| M-R1 (hết đợt 1) | D-R1 có quyết định; Ch.2 ≥ 8 hình theo Q-3/Q-4/Q-5; Ch.3 tách 3A/3B; 5 tính năng chính theo khuôn; biên bản validation mới | **Đạt 18/11** — D-R1 = A; Ch.2 có 10 hình; Part A/B; `report-validation-2026-11-18*.md` |
| M-R2 (hết đợt 2) | Ch.4A theo câu hỏi; Ch.4 ≤ 30 bảng (hoặc ghi lý do); mở đầu/kết luận/Abstract khớp; biên bản validation mới | Một phần — Ch.4 29 bảng, đoạn dẫn theo RQ; chưa rà ngôn ngữ toàn văn, Abstract bản cuối chờ bản nộp |
| M-R3 (sau G-SYS) | 6.1–6.7 xong; số liệu hệ thống trỏ biên bản nghiệm thu hệ thống mới | Chưa — chờ G-SYS |
| M-R4 (bản nộp) | D-2 điền; validation cuối PASS cả hai bản; hash PDF lưu | Chưa — chờ D-2 |

---

## 12. Nhật ký thay đổi

| Ngày | Thay đổi | Người |
| --- | --- | --- |
| 18/11/2026 | Tạo biên bản: tách nhánh 3 khỏi [plan.md](plan.md). Tham khảo cấu trúc T1/T2/T3; đề xuất D-R1 phương án A; tìm công cụ vẽ (không có claude.ai skill phù hợp; plugin Diagrams/Kroki chỉ cho sơ đồ phần mềm và nên tự host; chọn TikZ/chemfig/pgfplots/matplotlib); sơ đồ ứng dụng tổng thể đóng băng đến G-SYS | Trọng + Claude |
| 18/11/2026 | **D-R1: Trọng chốt phương án A** (4 chương; 3A/3B, 4A/4B). Bắt đầu đợt 1: mục 2.0 style + preview, hình Ch.2 | Trọng + Claude |
| 18/11/2026 | Xong 2.0 và 3.1–3.11: style hình + `preview_figure.py`; Chương 2 từ 2 lên 10 hình tự vẽ (đối chiếu code cho PLM/LoRA/head) và bảng thuật ngữ; build/check/float PASS; biên bản `report/report-validation-2026-11-18.md` | Claude |
| 18/11/2026 | Chương 3 tách Part A/Part B; xong 4.1–4.4, 5.1, 5.3–5.6 (5 hình mới: quy trình nghiên cứu, thiết kế thí nghiệm, kiến trúc LoRA-D, luồng ma trận, chia tile); 4.5 một phần; 5.2 bỏ theo yêu cầu. Build/check/float PASS; biên bản `report/report-validation-2026-11-18-ch3.md` | Trọng + Claude |
| 18/11/2026 | Xong 4.5, 7.2 (Ch.4 còn 29 bảng), 7.4, 7.7 (11 thuật ngữ, `platt1999`); 7.1/7.3/7.6/8.1 một phần; Ch.4 tách Part A/B. Build/check/float PASS; biên bản `report/report-validation-2026-11-18-wave2.md` | Trọng + Claude |
| 18/11/2026 | Thêm §8b theo phản hồi của Trọng: V-1 trực quan hoá khối chữ và Hình 3.1/3.2, V-2 vẽ lại Hình 3.3, V-3 kiến trúc chi tiết có logo (ngoại lệ Q-6), V-4 chữ chồng/mũi tên, V-5 float cắt đoạn, V-6 bảng tràn lề | Trọng + Claude |
| 18/11/2026 | Xong V-1…V-6: biểu tượng và ma trận cho Hình 2.5/2.9/3.1/3.2, vẽ lại Hình 3.3, kiến trúc chi tiết có 11 logo (Simple Icons CC0), vẽ lại use case/sequence/trạng thái/CDM (sửa quan hệ CDM sai), 0 float cắt đoạn, 0 bảng tràn lề; số liệu hợp đồng API ghim ở bản nghiệm thu. Biên bản `report/report-validation-2026-11-18-visual.md` | Trọng + Claude |
| 19/11/2026 | Biên dịch lại theo yêu cầu: `make -C report all` exit 0; `make -C report check` PASS (168/168 trang, smoke 9); `check_float_references.py` PASS (41 hình, 64 bảng); nguồn không đổi so với biên bản V-1…V-6. SHA-256 PDF một mặt `6c37bdad…07aa`, hai mặt `d8e31355…190d`. Cập nhật cột trạng thái ở §9, §11 và tóm tắt đầu file | Trọng + Claude |
