# Chỉ mục sơ đồ của luận văn — vẽ bằng Figma (FigJam)

Mọi sơ đồ dưới đây được dựng trong FigJam bằng Figma MCP, xuất PNG từ chính bảng FigJam rồi cắt gọn, đổi nền xám của canvas sang trắng. **8 sơ đồ sinh bằng `generate_diagram` (từ Mermaid); riêng sơ đồ use case (Fig 1.1) vẽ theo chuẩn UML bằng `use_figma`**, vì `generate_diagram` không hỗ trợ loại sơ đồ này. Không có sơ đồ nào vẽ tay hay bằng công cụ khác. Ngày dựng: 22/10/2026.

- Bảng FigJam chứa bản gốc chỉnh sửa được: <https://www.figma.com/board/Eid8V6TBNoccBDfNq5papR> (9 sơ đồ, đúng bằng danh sách dưới đây; sơ đồ use case nằm ngoài cùng bên phải).
- Bảng cũ <https://www.figma.com/board/f265QPH2iqyPnvIR2RrkyD> chỉ chứa **bản nháp đã bị thay thế**; không dùng, xoá được.
- Mã nguồn của từng hình: thư mục [src/](src/), tên trùng tên ảnh. Tám hình là Mermaid (`.mmd`); sửa nội dung rồi sinh lại bằng `generate_diagram` (kiến trúc cần thêm `useArchitectureLayoutCode = "FIGMA_DIAGRAM_2026"`), sau đó xuất lại ảnh. Hình use case là mã `use_figma` ([fig-1-1-use-cases.figjam.js](src/fig-1-1-use-cases.figjam.js)).

`template/packages.tex` đặt `\graphicspath{{assets/figures/}{assets/diagrams/}}`, nên trong LaTeX chỉ cần tên file, **không** cần đường dẫn.

## Danh sách

| Hình (đề xuất) | Loại | File ảnh (từ gốc repo) | Kích thước (px) | Vị trí đề xuất | Nội dung dựa trên |
|---|---|---|---|---|---|
| **Fig 1.1** Use cases | UML use case | [report/assets/diagrams/fig-1-1-use-cases.png](fig-1-1-use-cases.png) | 1744 × 1080 | Ch.1 §Functions of the System | [srs.md](../../../topics/degron-footprint/system/srs.md) §3, UC-01…07 |
| **Fig 3.1** System architecture | architecture | [report/assets/diagrams/fig-3-1-system-architecture.png](fig-3-1-system-architecture.png) | 2920 × 1682 | Ch.3 §Architectural Components | [system/README.md](../../../topics/degron-footprint/system/README.md) §2, [db-design.md](../../../topics/degron-footprint/system/db-design.md) |
| **Fig 3.2** Prediction request sequence | sequence | [report/assets/diagrams/fig-3-2-prediction-sequence.png](fig-3-2-prediction-sequence.png) | 1496 × 1100 | Ch.3 §Interaction Between Components | [api-spec.md](../../../topics/degron-footprint/system/api-spec.md) §3–4 |
| **Fig 3.3a** ER diagram: reference data | ER | [report/assets/diagrams/fig-3-3a-erd-reference-data.png](fig-3-3a-erd-reference-data.png) | 1488 × 2128 | Ch.3 §Data Model / Relationships | [db-design.md](../../../topics/degron-footprint/system/db-design.md) §2 (rút gọn cột) |
| **Fig 3.3b** ER diagram: models and runs | ER | [report/assets/diagrams/fig-3-3b-erd-models-and-runs.png](fig-3-3b-erd-models-and-runs.png) | 849 × 2064 | Ch.3 §Data Model / Relationships | như trên |
| **Fig 3.4** Domain gate decision | flowchart | [report/assets/diagrams/fig-3-4-domain-gate-decision.png](fig-3-4-domain-gate-decision.png) | 1269 × 2132 | Ch.3 §Functional Design | [api-spec.md](../../../topics/degron-footprint/system/api-spec.md) §4 |
| **Fig 3.5** Research pipeline | flowchart | [report/assets/diagrams/fig-3-5-research-pipeline.png](fig-3-5-research-pipeline.png) | 975 × 2252 | Ch.3 §System Overview hoặc §Method and Model Design | [data/README.md](../../../topics/degron-footprint/data/README.md), [learning-curve README](../../../topics/degron-footprint/research/learning-curve-2026-10-22/README.md) |
| **Fig 4.1** Evaluation protocol | flowchart | [report/assets/diagrams/fig-4-1-evaluation-protocol.png](fig-4-1-evaluation-protocol.png) | 666 × 1968 | Ch.4 §Experimental setup | [learning-curve PROTOCOL](../../../topics/degron-footprint/research/learning-curve-2026-10-22/PROTOCOL.md) |
| **Fig A.1** Notebook training workflow | flowchart | [report/assets/diagrams/fig-a-1-notebook-workflow.png](fig-a-1-notebook-workflow.png) | 1545 × 856 | Phụ lục A (hoặc Ch.3 §Method) | [notebook-kit RUN.md](../../../topics/degron-footprint/research/notebook-kit-2026-10-22/RUN.md) |

Số hình thật do LaTeX đánh tự động; cột "Hình" chỉ là tên gợi ý.

## Caption gợi ý (tiếng Anh, khớp ngôn ngữ luận văn)

| Hình | Caption |
|---|---|
| Fig 1.1 | UML use case diagram of the Degron Footprint tool. Solid lines are associations between the actor and use cases; dashed arrows are the include and extend relations. In the main flow UC-04 leads into UC-01. |
| Fig 3.1 | Architecture of the web tool. The ETL job runs once to load public reference data; the API serves predictions and reads the database. |
| Fig 3.2 | Sequence of one successful prediction request. |
| Fig 3.3a | Entity-relationship diagram of the reference data (abridged to key columns). |
| Fig 3.3b | Entity-relationship diagram of the model registry and prediction runs (abridged to key columns). |
| Fig 3.4 | Decision logic of the domain gate. A tile outside the training domain is refused unless the user overrides. |
| Fig 3.5 | From experimental labels to the frozen model used by the tool. |
| Fig 4.1 | Evaluation protocol: cluster-grouped cross-validation with extra training peptides that never enter the outer-test. |
| Fig A.1 | Training workflow on a notebook platform and return of results to the repository. |

## Cách chèn vào LaTeX

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\textwidth]{fig-3-1-system-architecture}   % hình rộng
  \caption{Architecture of the web tool ...}\label{fig:architecture}
\end{figure}

\begin{figure}[htbp]
  \centering
  \includegraphics[height=0.82\textheight,keepaspectratio]{fig-3-4-domain-gate-decision}   % hình cao
  \caption{Decision logic of the domain gate ...}\label{fig:gate}
\end{figure}
```

Hình cao (3.3a, 3.3b, 3.4, 3.5, 4.1) nên giới hạn theo chiều cao như ví dụ thứ hai, đặt `[p]` hoặc `[htbp]`. Hai ERD có thể đặt cạnh nhau bằng `\subcaptionbox` nếu template có `subcaption`.

## Giới hạn cần biết

- `[ƯỚC LƯỢNG]` Cỡ chữ in **chưa đo**. Chữ trong ảnh cao khoảng 16–24 px (ước bằng mắt); ở các hình cao ~2100 px in cao 20 cm, chữ khoảng 5–6 pt, nhỏ hơn thân bài. Hình kiến trúc (2920 px rộng) ở chiều rộng chữ khoảng 5 pt. Nếu cần chữ to hơn thì phải tách sơ đồ hoặc bớt nút, không chỉnh được cỡ chữ trong `generate_diagram`.
- Các sơ đồ hệ thống mô tả **thiết kế bản nháp v0.1**, không phải kết quả kiểm chứng. Cổng miền áp dụng tầng "gate model" (R3) **chưa có mô hình thật**; hình ghi đúng logic đã thiết kế.
- Sơ đồ kiến trúc không vẽ tệp trọng số mô hình, vì nó nằm trong container API; nên nói bằng lời trong thân bài.
- ERD đã rút gọn cột so với [db-design.md](../../../topics/degron-footprint/system/db-design.md) (không có `etl_run`, `etl_input`, `usage_daily`); thân bài phải nói "abridged".
- Tách ERD thành hai hình (3.3a, 3.3b) vì một hình duy nhất quá rộng để đọc được trên trang A4 dọc; thực thể `tile` xuất hiện ở cả hai với tập cột khác nhau.
- Trong Fig 4.1, "91 base peptides" và "85 extra peptides" là số đo `[ĐO]` từ `learning-curve-2026-10-22/results.json`; đừng đổi số trong hình mà không đổi ở thân bài.

## Hình minh họa tổng quan (V1–V6) — **chưa hoàn tất, đang chờ hạn mức Figma**

Bộ hình có logo công cụ, biểu đồ dữ liệu thật và ảnh giao diện thật, dựng trong Figma Design theo [DESIGN-SPEC.md](src/viz/DESIGN-SPEC.md) (frame 1600 px, chữ ≥ 24 px, bảng màu Okabe–Ito). Lúc dựng, Figma MCP của gói **Starter (seat View)** báo hết hạn mức gọi công cụ (hạn mức tính theo tài khoản, dùng chung cho mọi agent), nên **chỉ V5 hoàn chỉnh**. Các hình còn lại đã có đủ nguyên liệu (biểu đồ, ảnh, logo, script dựng frame) nhưng chưa xuất được ảnh cuối. Chi tiết từng hình ở [index-parts/](index-parts/).

| Hình | File ảnh | Trạng thái | File Figma | Việc còn lại |
|---|---|---|---|---|
| **V5** Notebook training overview (Fig A.2) | [fig-a-2-notebook-training-overview.png](fig-a-2-notebook-training-overview.png) | **Xong**, đã xem lại | [Figma](https://www.figma.com/design/jEOFIW9IpOVxQog8k34T3H) | — |
| **V3** Data processing (Fig 3.8) | [fig-3-8-data-processing.png](fig-3-8-data-processing.png) | **BẢN TẠM — đừng dùng trong luận văn** (histogram cũ, panel chưa cân, khung hơi cao) | [Figma](https://www.figma.com/design/DU3N3ikRcLELYZcPK0SYxI) | Chạy [V3-pending-patch.figma.js](src/viz/V3-pending-patch.figma.js), xuất frame `1:2` scale 2 đè lên file ảnh |
| **V4** Evaluation overview (Fig 4.2) | chưa có | Biểu đồ thật đã xong (`src/viz/inputs/ev-*.png`, `ev-numbers.json`), khung Figma dở | [Figma](https://www.figma.com/design/IUICXCEcMM86JbJRUzgFOS) | Dựng lại khung ≤ 1900 px, tải 4 ảnh lên, xuất |
| **V2** Method overview (Fig 3.7) | chưa có | Biểu đồ thật xong (`src/viz/inputs/v2-*.png`, `v2-summary.json`), script khung viết xong, chưa chạy | [Figma](https://www.figma.com/design/NQRHjRziv78u033JVqPfgk) | Chạy `method_overview.figma.js`, upload 4 ảnh, xuất |
| **V1** Technology stack (Fig 3.6) | chưa có | 17 logo đã tải lên Figma, ảnh giao diện đã cắt (`src/viz/inputs/v1/`), script khung chưa chạy | [Figma](https://www.figma.com/design/wng9Yyt2PtXDQ0l2deaLaq) | Chạy `v1_compose.figma.js`, upload 2 ảnh, xuất |
| **V6** Domain gate in practice (Fig 3.9) | chưa có | Histogram thật + 3 thẻ giao diện đã xong, đã upload lên Figma, script khung chưa chạy | [Figma](https://www.figma.com/design/0dSN14jEOK397MFUyExVGw) | Chạy `domain_gate_visual.figma.js`, vẽ mũi tên, xuất |

Nguồn của ảnh giao diện: `src/viz/inputs/ui-screens.md` (backend thật, mô hình `m3-ext4.0-platt-v1`, tile A6NMZ7 số 28 và số 7). Logo: simple-icons 13.21.0 (CC0) và lucide-static 0.468.0 (ISC); nhãn thương hiệu thuộc chủ sở hữu, chỉ minh họa.

**Vấn đề đã biết của ứng dụng (không thuộc hình):** trang thẻ mô hình hiện khóa JSON thô và một dòng tiếng Việt lấy từ `results.json`; không dùng ảnh trang này trong luận văn cho tới khi sửa.
