# Rà UI/UX và đổi sang Roboto — 17/11/2026

Yêu cầu của Trọng ngày 17/11: dùng skill `ui-ux-pro-max` phân tích và tối ưu UI/UX frontend hiện tại, chuyển sang font
**Roboto**. Hồ sơ này **bổ sung**, không thay [hồ sơ 16/11](../ui-ux-pro-max-2026-11-16/README.md); `MASTER.md` 16/11
giữ nguyên làm lịch sử (không chạy lại `--persist --force`).

Quy tắc hoà giải trong [plan.md](../../../plan.md) mục 5 vẫn áp dụng: thang màu khoa học (Viridis đảo cho xác suất, PuOr
cho raw score, hatch ô WT) và thứ tự "cảnh báo trước điểm số" trong DOM **không đổi**.

## 1. Truy vấn skill đã dùng

| Truy vấn | Kết quả dùng được |
| --- | --- |
| `"Roboto Roboto Mono technical dashboard" --domain typography` | Cặp "Material You MD3 (Roboto System)": thang Headline 32/500, Title 22/500, Body 16/400, Label 12/500; cặp "Science/Tech" dùng Roboto Mono cho dữ liệu |
| `"Roboto variable sans" --domain google-fonts` | Roboto có trục `wght` 100–900 → giữ được 500/600/700 mà không tổng hợp đậm giả |
| `"heatmap legend color not only" --domain chart` | Heatmap: luôn có legend số, không chỉ dựa vào màu, có bảng thay thế (đã có: colour bar, hatch WT, "Show as a table") |
| `"alert severity icon color" --domain ux` (truy vấn lại) | Không truyền thông tin chỉ bằng màu; tương phản ≥ 4,5:1 |
| `"font loading layout shift" --stack react` | **Không có kết quả** trong cơ sở dữ liệu → dùng mặc định chung: tự host, `font-display: swap` |
| `references/quick-reference.md` §6 | `font-scale`, `weight-hierarchy`, `line-height` 1,5, `number-tabular` |

Hai truy vấn đầu tiên về banner/toolbar trả kết quả lệch chủ đề (hover state, carousel) nên không dùng.

## 2. Phát hiện khi rà (ảnh chụp `app/docs/screenshots/`, light/dark, 1440/360 px)

| # | Vấn đề | Mức |
| --- | --- | --- |
| F-1 | Banner domain và nhãn bằng chứng cùng kiểu (nền trắng, viền xám): trạng thái miền không nổi bật hơn chú thích | Cao: rule W-1 muốn trạng thái miền đọc được trước điểm |
| F-2 | Khối "Before you submit": `dd.num` căn phải cho văn bản → hai dòng đầu lệch phải, các dòng sau lệch trái | Trung bình (lỗi hiển thị) |
| F-3 | Điều khiển ma trận (View / Layers / Table) là ba dòng rời, không có nhóm | Trung bình |
| F-4 | Hai hệ style song song: control/banner/card cũ (`button`, `.banner`, `.card`) không có hover, input nền `--bg` xám trên panel trắng, bo góc lệch token | Trung bình |
| F-5 | Kích thước/weight chữ viết cứng (`1.05rem`, `600`…) rải rác, không có thang chữ | Thấp |
| F-6 | Radio/checkbox giữ màu xanh dương mặc định của trình duyệt, lệch màu accent | Thấp |
| F-7 | Test font yếu: `document.fonts.check('16px "Fira Sans"')` trả `true` cả khi font không được khai báo | Thấp (chất lượng test) |

## 3. Thay đổi

| Phần | Thay đổi | File |
| --- | --- | --- |
| Font | `@fontsource-variable/roboto@5.3.0`, `@fontsource-variable/roboto-mono@5.3.0` (OFL-1.1, tự host); gỡ `@fontsource/fira-*` | `package.json`, `src/main.tsx` |
| Token chữ | `--text-xs…2xl` (12/14/16/18/22/28), `--weight-regular/medium/semibold/bold`, `--leading-tight/body`; heading 600, line-height 1,25 | `src/styles/tokens.css`, `src/styles.css`, `src/styles/ui.css` |
| F-1 | Banner domain theo `data-status`: trong miền → tông success, ranh giới / không tin cậy / không rõ → caution, ngoài miền → danger; nhãn bằng chứng → tông info. Glyph và chữ giữ nguyên, màu chỉ nhắc lại | `src/styles.css` |
| F-2 | `.kv .num { text-align: start }` | `src/styles.css` |
| F-3 | `.matrix-toolbar` gom View / Table / Layers; nhãn nhỏ viết hoa; thứ tự DOM không đổi | `ResultView.tsx`, `ScaleToggle.tsx`, `LayerToggles.tsx` |
| F-4 | Control cũ dùng `--field-bg`, `--radius-sm`, hover; `aria-pressed` có trạng thái; bảng dữ liệu có header nền `--subtle`, hover hàng, số tabular | `src/styles.css` |
| F-6 | `accent-color: var(--accent)`; `legend` đậm như nhãn trường | `src/styles.css` |
| F-7 | Test yêu cầu face `Roboto Variable` và `Roboto Mono Variable` ở trạng thái `loaded` | `e2e/design.spec.ts` |

## 4. Kiểm `[ĐO]`

| Kiểm | Kết quả |
| --- | --- |
| Vitest (gồm `tests/contrast.test.ts`, kiểm tương phản token hai theme) | 172/172 |
| Playwright mock: flows, workspace, narrow 360 px, design (axe WCAG 2.1 AA ở 360/768/1280/1440 × light/dark), ma trận Firefox/WebKit | 28/28 |
| tsc, eslint | sạch |
| Bản production trong container `web` (nginx, CSP) | 0 lỗi console; font tải từ `/assets/roboto-*.woff2`, không request ra ngoài |
| Tràn ngang ở 360 px (kết quả, dự án, protein) | không |

Còn mở: kiểm tay bàn phím / trình đọc màn hình (A11Y) do người thực hiện; ảnh chụp tài liệu `app/docs/screenshots/` vẫn
là bản Fira ngày 17/11 sáng, cần chụp lại bằng `e2e/screenshots.spec.ts` khi chốt giao diện.
