# Plan-report đợt 1, phần Chương 2 — 18/11/2026

Thực hiện theo [plan-report.md](../plan-report.md) sau khi Trọng chốt **D-R1 = phương án A**. Phạm vi lượt này:
mục **2.0** (hạ tầng hình) và **3.1–3.11** (Chương 2). Không đổi số liệu, kết quả hay giới hạn bằng chứng;
không chạy huấn luyện/suy luận; không commit/push. Build không phải nghiệm thu nghiên cứu.

## 1. Hạ tầng hình (2.0)

| Tệp | Vai trò |
| --- | --- |
| `report/assets/figures/style.tex` | Bảng màu Okabe–Ito, kiểu node chung (protein, enzyme, ubiquitin, degron, residue, tensor, layer, frozen/trained…), giãn dòng 1 trong hình; nạp ở `report/main.tex` sau `template/packages` (template gốc `reportTemplate/` **không đổi**) |
| `report/scripts/preview_figure.py` | Dựng riêng một hình (cùng phông, gói, macro, khổ 15,5 cm) ra `build/preview/<tên>.{pdf,png}`; báo overfull/thiếu ký tự |

## 2. Hình Chương 2 (3.1–3.10) và bảng thuật ngữ (3.11)

Chương 2: **2 → 10 hình**, thêm 1 bảng. Tất cả là hình tự vẽ (TikZ/`chemfig`), chú thích ghi
"Original schematic, informed by …" (Q-3). Hình 2.2 và 2.5 thay hai sơ đồ khối cũ nhưng **giữ nhãn**
`fig:ups-concept`, `fig:mutation-observation` nên tham chiếu cũ không đổi.

| Mục | Tệp | Nguồn kiến thức / đối chiếu code (Q-5) |
| --- | --- | --- |
| 3.1 | `amino-acids.tex` | hoá sinh chuẩn |
| 3.2 | `ups-pathway.tex` | varshavsky2019, koren2018 |
| 3.3 | `degron-types.tex` | varshavsky2019, koren2018, zhang2023; quy ước dấu ΔPSI của §2 |
| 3.4 | `gps-assay.tex` | yen2008, zhang2023; công thức `eq:psi-bins` (`research/full-data-audit/build_psi.py`) |
| 3.5 | `mutation-label.tex` | `eq:delta-psi-halves` (`residue_data.py`), giới hạn vật lý trong `EXECUTION-PROTOCOL.md`; không vẽ giá trị |
| 3.6 | `plm-embedding.tex` | lin2023esm, vaswani2017; `degron_v3/finetune.py` `MutationRegressor.forward` (d = 480, Δ site + Δ mean + 60) |
| 3.7 | `adaptation-lora.tex` | hu2022lora; `LoRALinear`/`inject_lora` (r = 8, α = 16, B = 0 lúc đầu, query/value × 12 lớp); r, α lấy từ macro `\nTAdapterRank`, `\nTAdapterAlpha` |
| 3.8 | `conv-heads.tex` | `degron_v3/neural.py` `ConvHead` (k = 1 / 5 / 3,5,7; 96 filter; one-hot 20 + tâm 1 + chiếu 32), `features.py` `crop_inputs` (±7) |
| 3.9 | `group-split.tex` | bernett2024, steinegger2017, efron1979; 5 fold ngoài, validation trong ~20 %, seed 17/29/43; số nhóm từ `\nVthreeNGroups` |
| 3.10 | `calibration-concept.tex` | đường cong **sơ đồ**, không phải số đo (ghi trong chú thích); Platt cho ridge, ba lớp cho LoRA-D (`calibrate-final-lora-D/calibration.json`) |
| 3.11 | bảng `tab:bio-terms` | định nghĩa theo nghĩa dùng trong luận văn |

Platt 1999 **chưa** được thêm vào `references.bib`; chú thích Hình 2.10 ghi "standard calibration practice"
(đưa vào mục 7.7).

## 3. Kiểm `[ĐO 18/11/2026]`

| Kiểm | Kết quả |
| --- | --- |
| `preview_figure.py` cho 10 hình | không overfull, không thiếu ký tự; đã xem ảnh từng hình, sửa đến khi hết chồng chữ |
| `make -C report all` | PASS |
| `make -C report check` | PASS — 162 trang một mặt, 162 hai mặt, smoke 9 |
| `check_float_references.py` | PASS — **36 hình, 64 bảng**, khớp cả hai bản |
| Khoảng trống > 1/3 (50 dpi, hai bản) | 13/162 trang, giống hệt ở hai bản; đều là trang kết thúc có chức năng: 5–6, 10, 17, 19, 22, 30, 54 (cuối Ch.2), 82 (cuối Ch.3), 135, 139, 142, 162. Trang hình 2.10 lúc đầu bị đẩy thành trang chỉ có hình → dời hình lên đầu §2.4.3, hết |
| Ảnh render Chương 2 cỡ đọc được | đã xem toàn bộ 14 trang |

| PDF | SHA-256 |
| --- | --- |
| `report/build/content/content.pdf` | `d963499bcb4fd46936fa54cdcecab7ac931d4a927e0e841211e2ed82a3f39bfe` |
| `report/build/content-twoside/content.pdf` | `b1808adee74a840fcd62e5cd926e2150f8114919711c88bc5afd19929a5524aa` |

## 4. Tiếp theo (đợt 1 còn lại)

Mục 4.1–4.5 (Chương 3A: tách mạch, sơ đồ quy trình nghiên cứu, kiến trúc LoRA-D, thiết kế thí nghiệm) và
5.1–5.6 (Chương 3B: tính năng chính, đóng băng sơ đồ tổng thể).
