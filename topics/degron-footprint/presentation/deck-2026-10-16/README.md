# Deck buổi gặp GVHD 16/10/2026 — bản dựng trong repo

> **26 slide**, chữ trên slide **tiếng Anh**, ghi chú người nói **tiếng Việt**.
> Dựng từ [slide-content-2026-10-15.md](../slide-content-2026-10-15.md) (brief phiên 11).
> Mở bằng `file://`, không cần mạng, không publish artifact ([D-013](../../../../DECISIONS.md#d-013)).

Mở: **[index.html](index.html)**.

Đọc và tập nói: **[script song ngữ Việt–Anh theo 26 slide](speaker-script-bilingual.md)** — kèm giải thích
thuật ngữ, cách đọc hình, hỏi đáp và đối soát các chỗ cần nói chính xác hơn trong HTML. Bản soạn
15/10/2026 từ đủ năm phần paste; các đoạn nói dùng một ngôn ngữ mỗi lần, phần đọc hiểu dùng để tự học.

Trong thư mục `presentation/` có **hai** bản deck cho cùng buổi gặp, dựng ở hai phiên khác nhau:

| Thư mục | Dựng khi | Khác biệt |
|---|---|---|
| **`deck-2026-10-16/`** (thư mục này) | phiên 15/10 theo yêu cầu "tìm mẫu slide, tìm GIF, tạo animation, dựng slide" | engine tự viết, **không** dùng lại khuôn slide cũ; 26 slide, **không có phụ lục rời**; animation **thuần SVG/CSS**, không dùng GIF |
| [`deck-external-2026-10-16/`](../deck-external-2026-10-16/README.md) | phiên khác cùng ngày | tham khảo Quarto Clean; 26 slide + **7 phụ lục**; có **hai GIF Wikimedia Commons** kèm ghi công |

Hai bản **không đồng bộ tự động**. Nội dung đều bám cùng brief và cùng các ràng buộc câu chữ của
[D-031](../../../../DECISIONS.md#d-031), [D-033](../../../../DECISIONS.md#d-033)…[D-036](../../../../DECISIONS.md#d-036).

## Điều khiển

| Phím | Việc |
|---|---|
| `→` `↓` `Space` `PageDown` | bước tiếp — hiện bước animation kế, hết bước thì sang slide |
| `←` `↑` `Backspace` `PageUp` | lùi (lùi vào slide trước ở trạng thái **đã hiện đủ**) |
| `N` | bật/tắt panel **ghi chú người nói** (tiếng Việt) |
| `O` / `Esc` | bảng tổng quan 26 slide, bấm để nhảy |
| `F` | toàn màn hình |
| `P` | chế độ in → rồi `Ctrl+P` để xuất PDF |
| số + `Enter` | nhảy tới slide theo số |
| vuốt trái / phải | tiến / lùi |

Nhấp chuột trái hoặc phải trên slide không chuyển slide hay bước animation.

Thêm `?all` vào URL (`index.html?all`) để **hiện sẵn mọi bước** — dùng khi soát bố cục hoặc khi in.

Xuất PDF không cần mở trình duyệt:

```bash
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=deck.pdf --virtual-time-budget=9000 'file:///<đường dẫn>/index.html?all'
```

Đã kiểm: ra đúng **26 trang** 1280×720.

## Cấu trúc

| File | Nội dung |
|---|---|
| [index.html](index.html) | 26 `<section class="slide">`; mỗi slide có một `.speaker-note` (ẩn, JS chép sang panel) |
| [deck.css](deck.css) | bảng màu, bố cục, trạng thái bước animation, chế độ in |
| [deck.js](deck.js) | engine: điều hướng, bước animation, ghi chú, tổng quan, `?all`, in |
| [figures/example-matrix.svg](figures/example-matrix.svg) | **sinh từ dữ liệu**, không vẽ tay — xem bên dưới |

## Hình: cái gì tự dựng, cái gì của tác giả

- **Sinh từ dữ liệu (1):** `figures/example-matrix.svg` — ma trận ΔPSI 28×20 **đo được** của
  `Q16665_HIF1A_25`, do [`research/slide-figures-2026-10-15/make_example_matrix.py`](../../research/slide-figures-2026-10-15/README.md)
  tạo ra, kèm SHA-256 của hai file đầu vào. Chạy lại:

  ```bash
  .venv/bin/python topics/degron-footprint/research/slide-figures-2026-10-15/make_example_matrix.py \
    --out-svg topics/degron-footprint/presentation/deck-2026-10-16/figures/example-matrix.svg
  ```

- **Tự dựng, inline SVG + CSS (13):** chuỗi protein gập và đột biến (slide 2), cân synthesis/degradation (3),
  UPS ba bước (4), zoom ba tầng tới footprint (5), hai nhánh cơ chế bệnh + forest plot OR 2,148 (6),
  chiều ΔPSI (7), trục độ phân giải (9), phép kiểm hoán vị PAP (10), bốn cột câu hỏi (11),
  thành phần so với ngữ cảnh kèm hai đồng hồ (12), trục thời gian 2018→2026 (13), thanh phân rã (14),
  đầu vào→đầu ra (15), hai cột AUROC kèm trần (17), phễu dữ liệu (19), split theo cụm (20),
  workflow A/B/C (21), lưới thí nghiệm (22), luồng dịch vụ (23), harness + 87,3% (24), tiến độ tuần (25).
- **Hình của tác giả, có giấy phép (2):** `voutsinos2026-f1.jpg` (slide 7) và `voutsinos2026-f4.jpg` (slide 10),
  từ [lectures/degron-footprint/assets/figures/](../../../../lectures/degron-footprint/assets/figures/NOTICE.md),
  **CC BY-NC 4.0**, caption ghi tác giả + DOI + giấy phép ngay dưới hình. Đây là **bài duy nhất** được phép sao chép hình.

### Vì sao không dùng GIF

Đã tra **Wikimedia Commons** ngày 15/10/2026 qua API cho `proteasome`, `ubiquitin`, `degron`, `E3 ligase`,
`ubiquitination animation`, `flow cytometry sorting`, `protein folding`: **không có GIF nào vừa đúng chủ đề vừa
có giấy phép dùng được**. Hai GIF tìm được (`Protein synthesis (Translation).gif`,
`I-TASSER predicted protein fold of Fam188a.gif`) là **CC BY-SA 3.0** và không đúng nội dung cần.
Các nguồn animation UPS chất lượng cao đều **không mở**: HHMI BioInteractive (CC BY-NC-SA),
WEHI.TV (xin phép từng lần), hình tạp chí (CC BY-NC-**ND**).

⇒ Animation ở đây **tự dựng bằng SVG + CSS**, đúng khuyến nghị trong brief: chỉ cần 3 khung, giữ được bảng màu,
cắt theo từng bước bấm chuột, và nét ở mọi độ phân giải. Bản `deck-external-2026-10-16/` chọn khác — có dùng
hai GIF Commons kèm ghi công; xem SOURCES.md của thư mục đó.

## Ràng buộc câu chữ đã áp (kiểm lại nếu sửa slide)

- ❌ **Không** "position beats composition" — phát biểu đúng là *composition at a ±3 neighbourhood scale beats
  composition at whole-peptide scale* ([C-17b](../../../../DECISIONS.md#c-17b)). Bảng phân rã ở slide 14 nói thẳng điều này.
- ❌ **Không** "no tool outputs a 28×20 matrix" — Degformer **đã** xuất; slide 8 và 10 ghi rõ nó có, và ghi
  "GitHub, no publication".
- ❌ **Không** "nobody has done X" khi chỉ tra qua tóm tắt — mọi chỗ viết dạng
  *"a literature search on 15 Oct 2026 did not find…"* (slide 13, 21).
- ❌ **Không** dùng ClinVar làm đích xác nhận; con số 2,148 luôn đi kèm ba dòng giới hạn và nhãn **region level**
  ([D-036](../../../../DECISIONS.md#d-036)). Slide 6, 13, 18, 24 đã áp.
- ❌ **Không** nói trần đo lường là dư địa đạt được — câu chân slide 17 bắt buộc giữ.
- ⬜ Mọi ô chưa đo để trống hoặc ghi "not measured"; **không** điền số minh họa (slide 16, 21, 22, 23).

## Việc còn lại trước buổi gặp

| # | Việc | Slide |
|---|---|---|
| 1 | **Trọng tự viết** câu hỏi 1 và 4 — bản hiện tại lấy từ brief, câu 1 đã thêm dòng xin ghi biên bản khung ba trụ | 26 |
| 2 | Đối chiếu lại từng ô bảng so sánh công cụ; ô nào chưa kiểm được thì đổi `–` thành `not checked` | 23 |
| 3 | Nếu chạy kịp đối chứng bảo tồn / độ vô trật tự thì thay dòng thứ ba của "does and does not say" | 6 |
| 4 | Chọn dùng bản nào trong hai deck, hoặc gộp | — |
