# Hệ thiết kế Degron Workspace — hoà giải `ui-ux-pro-max` với Workspace UI v2

Ngày 16/11/2026, WP1 của [kế hoạch triển khai](../../implementation-plan-2026-11-16.md). Đầu ra gốc của skill nằm ở
[design-system/degron-workspace/](design-system/degron-workspace/) (`MASTER.md`, `tokens.css`, `tokens.json`), sinh bằng:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "scientific research data analysis dashboard" \
  --design-system --density 8 --variance 3 --motion 2 --persist --tokens css -p "Degron Workspace" \
  --output-dir system/design/ui-ux-pro-max-2026-11-16
```

Token đang dùng trong app: [`frontend/src/styles/tokens.css`](../../app/frontend/src/styles/tokens.css) (3 lớp
primitive → purpose → component), primitive giao diện ở `frontend/src/components/ui/`, shell ở
`frontend/src/components/AppShell.tsx`, trang rà soát `/__styleguide` (chỉ bản dev).

## Quyết định

| Đầu ra skill | Quyết định | Lý do |
| --- | --- | --- |
| Style Minimalism & Swiss | Nhận | Công cụ chuyên môn dày dữ liệu |
| Density 8 (thang 4–32 px) | Nhận | `--space-1…8` = 4/8/12/16/24/32 px |
| Pattern Enterprise Gateway (Contact Sales, logo carousel) | Bỏ | Mẫu landing page, không phải app local |
| Primary navy `#1E40AF`, secondary `#3B82F6` | Bỏ | Giữ teal của v2 (`#12634f` sáng / `#6cc9ab` tối) như `plan.md` §5 |
| Accent hổ phách `#D97706` | Bỏ | Trùng tông cam của thang PuOr (raw score) |
| Fira Code + Fira Sans qua Google Fonts | Nhận font, bỏ CDN — **đã thay bằng Roboto/Roboto Mono ngày 17/11** ([hồ sơ 17/11](../ui-ux-pro-max-2026-11-17/README.md)) | Trọng chọn Fira 16/11; tự host `@fontsource/fira-sans@5.3.0`, `@fontsource/fira-code@5.3.0` (OFL-1.1); NFR-09 |
| Fira Code cho **tiêu đề** | Đổi | Tiêu đề dùng Fira Sans; Fira Code dành cho chuỗi, ID, số (tắt ligature để `--`/`>=` trong chuỗi không bị ghép) |
| GSAP scroll reveal | Bỏ | Chỉ CSS transition 150–250 ms, tắt theo `prefers-reduced-motion` |
| Icon SVG, không emoji | Nhận | `lucide-react@1.73.0` (ISC); icon trang trí `aria-hidden`, icon-only button bắt buộc có nhãn |
| Breakpoint 375/768/1024/1440 | Gộp | Kiểm 360/768/1280/1440; sidebar thu thành menu dưới 1024 px |
| Contrast 4.5:1, focus ring, bàn phím | Nhận | `tests/contrast.test.ts` (46 cặp, cả 2 theme); chữ thấp nhất 5,98:1 (sáng) / 7,69:1 (tối) |

**Bất khả xâm phạm:** Viridis đảo cho xác suất, PuOr cho raw score, hatch ô WT, cảnh báo đứng trước điểm số trong DOM,
nhãn `P(ΔPSI ≥ 1.0)` cạnh mọi xác suất. Thang dữ liệu không nằm trong token theme và không đổi theo theme.

Ghi nhận còn mở: teal của UI nằm gần vùng giữa của Viridis (`#21918c`). Hai thứ không đứng cạnh nhau như cùng một nghĩa
(ô heatmap không bao giờ là nút), và chú giải màu luôn đi kèm; nếu rà soát người dùng thấy nhầm, đổi primitive teal,
không đổi thang dữ liệu.

## Bằng chứng

`frontend/e2e/design.spec.ts` (16/11): 0 vi phạm axe WCAG 2.1 AA trên `/__styleguide` ở sáng/tối × 360/768/1280/1440 px,
không cuộn ngang, font Fira Sans nạp từ chính app (không request ra ngoài), menu màn hẹp mở/đóng đúng `aria-expanded`.
