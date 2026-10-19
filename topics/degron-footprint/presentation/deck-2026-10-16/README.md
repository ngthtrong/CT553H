# Deck buổi gặp GVHD 16/10/2026 — bản dựng trong repo

> **34 slide lõi + 7 phụ lục A1–A7**, chữ trên slide **tiếng Anh**, ghi chú người nói **tiếng Việt**.
> Dựng từ [slide-content-2026-10-15.md](../slide-content-2026-10-15.md) (brief phiên 11).
> Mở bằng `file://`, không cần mạng, không publish artifact ([D-013](../../../../DECISIONS.md#d-013)).
>
> **Bản rút gọn 18/10/2026** — theo yêu cầu của Trọng: mỗi slide chỉ mang **ý chính**, không giải
> thích dài; chữ cắt đi dồn vào **ghi chú người nói** và **phụ lục**; thêm ảnh/GIF minh hoạ. Chi tiết
> ở mục [Bản rút gọn 18/10/2026](#ban-rut-gon-18102026).

Mở: **[index.html](index.html)**.

Đọc và tập nói: **[script song ngữ Việt–Anh theo 26 slide](speaker-script-bilingual.md)** — kèm giải thích
thuật ngữ, cách đọc hình, hỏi đáp và đối soát các chỗ cần nói chính xác hơn trong HTML. Bản soạn
15/10/2026 từ đủ năm phần paste; các đoạn nói dùng một ngôn ngữ mỗi lần, phần đọc hiểu dùng để tự học.

Trong thư mục `presentation/` có **hai** bản deck cho cùng buổi gặp, dựng ở hai phiên khác nhau:

| Thư mục | Dựng khi | Khác biệt |
|---|---|---|
| **`deck-2026-10-16/`** (thư mục này) | phiên 15/10, rút gọn 18/10 | engine tự viết, **không** dùng lại khuôn slide cũ; 34 slide + **7 phụ lục A1–A7**; animation SVG/CSS tự dựng, **có thêm 3 GIF + 2 ảnh Commons** từ 18/10 |
| [`pptx-2026-10-16/`](../pptx-2026-10-16/README.md) | phiên khác cùng ngày | bản PowerPoint `.pptx` 26 slide + 2 phụ lục, animation bấm chuột, ghi chú người nói; ba GIF Commons kèm ghi công |

Hai bản **không đồng bộ tự động**. Nội dung đều bám cùng brief và cùng các ràng buộc câu chữ của
[D-031](../../../../DECISIONS.md#d-031), [D-033](../../../../DECISIONS.md#d-033)…[D-036](../../../../DECISIONS.md#d-036).

## Điều khiển

| Phím | Việc |
|---|---|
| `→` `↓` `Space` `PageDown` | bước tiếp — hiện bước animation kế, hết bước thì sang slide |
| `←` `↑` `Backspace` `PageUp` | lùi (lùi vào slide trước ở trạng thái **đã hiện đủ**) |
| `N` | bật/tắt panel **ghi chú người nói** (tiếng Việt) |
| `O` / `Esc` | bảng tổng quan 34 slide + 7 phụ lục, bấm để nhảy |
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

Đã kiểm 18/10/2026: ra đúng **41 trang** 1280×720 (34 lõi + 7 phụ lục). Thanh HUD và vạch tiến độ
vẫn đếm theo **34 slide lõi**; slide phụ lục hiện `A1 / 6 · phụ lục`.

## Cấu trúc

| File | Nội dung |
|---|---|
| [index.html](index.html) | 41 `<section class="slide">` — 34 lõi + 7 mang `data-appendix="1…7"`; mỗi slide có một `.speaker-note` (ẩn, JS chép sang panel) |
| [SOURCES.md](SOURCES.md) | nguồn, giấy phép và SHA-256 của mọi ảnh/GIF dùng trên slide |
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
  thành phần so với ngữ cảnh kèm hai đồng hồ (12), **biểu đồ năm × đơn vị dự đoán (8, vẽ lại 18/10)**, trục thời gian 2018→2026 (13), thanh phân rã (14),
  đầu vào→đầu ra (15), hai cột AUROC kèm trần (17), phễu dữ liệu (19), split theo cụm (20),
  workflow A/B/C (21), lưới thí nghiệm (22), luồng dịch vụ (23), harness + 87,3% (24), tiến độ tuần (25).
- **Hình của tác giả, có giấy phép (2):** `voutsinos2026-f4.jpg` (slide 10) và `voutsinos2026-f1.jpg`
  (**phụ lục A5** từ 18/10 — ở cỡ cột slide thì sáu panel của nó không đọc nổi),
  từ [lectures/degron-footprint/assets/figures/](../../../../lectures/degron-footprint/assets/figures/NOTICE.md),
  **CC BY-NC 4.0**, caption ghi tác giả + DOI + giấy phép ngay dưới hình. Đây là **bài duy nhất** được phép sao chép hình.

### GIF và ảnh (cập nhật 18/10/2026)

Bản 15/10 **không** dùng GIF: tra Wikimedia Commons ngày đó không thấy GIF nào vừa đúng chủ đề vừa
có giấy phép thoải mái. Ngày 18/10 Trọng chỉ đạo rằng deck này **dùng nội bộ**, không phải công bố,
nên không chặn theo giấy phép nữa — chỉ cần ghi nguồn. Đã thêm:

| Slide | Hình | Vì sao |
|---|---|---|
| 2 | `assets/fam188a.gif` | chuỗi gập lại thành khối ba chiều — điều SVG tĩnh không nói được |
| 4 | `assets/ubiquitin.gif` (bước 2) + `assets/proteasome.png` (bước 3) | cho thấy ubiquitin và 26S proteasome là **vật thật**, không phải ô vuông trong sơ đồ |
| 5 | `assets/ring-domain.gif` | miền **RING finger**, miền xúc tác của phần lớn E3 ligase |
| 19 | `assets/facs-scheme.png` | "bin" là **cổng phân loại tế bào**, không phải khái niệm tính toán |

Nguồn, giấy phép và SHA-256: [SOURCES.md](SOURCES.md). Ghi công in ngay dưới mỗi hình.

<a id="ban-rut-gon-18102026"></a>
## Bản rút gọn 18/10/2026

**Yêu cầu:** mỗi slide chỉ trình bày ý chính và câu hỏi chính; không liệt kê hết số liệu; giữ nguyên
bố cục, hình và animation. Chỉ động vào slide trung bình/nặng — **slide 1 và 3 giữ nguyên**, slide 2
và 4 chỉ **thêm ảnh**, không cắt chữ.

**Ba chỗ chứa phần cắt đi** (`.foot` đã bị gỡ khỏi slide từ trước, nên không dùng lại):

1. **Ghi chú người nói** — mỗi slide bị cắt có thêm một đoạn mở đầu bằng *"Chữ đã cắt khỏi slide —
   nói miệng"*, giữ nguyên văn câu dài và các số thứ cấp.
2. **Phụ lục A1–A6** — A1 trích dẫn · A2 toàn bộ hằng số benchmark · A3 xuất xứ dữ liệu ·
   A4 từ điển trường · A5 kiến trúc PAP + phép kiểm hoán vị + audit Degformer + hình Fig. 1 của tác giả ·
   A6 phân tích lực và MDE · A7 bảng công trình trước đầy đủ.
   Chân slide 26 đã hứa sáu phụ lục này từ bản trước mà deck chưa có; nay có thật.
3. **Thư mục `research/`** — số gốc vẫn ở đó, slide chỉ trỏ tới.

**Chữ trên sân khấu, trước → sau** (đếm bằng script, bỏ SVG, bỏ ghi chú):

| Slide | Trước | Sau | | Slide | Trước | Sau |
|---|---:|---:|---|---|---:|---:|
| 5 | 184 | 112 | | 16 | 208 | 165 |
| 6 | 171 | 118 | | 20 *(cũ 17)* | 247 | 175 |
| 7 | 217 | 189 | | 21 *(cũ 18)* | 277 | 189 |
| 8 | 252 | 61 | | 22 *(cũ 19)* | 212 | 130 |
| 9 | 232 | 140 | | 23 *(cũ 20)* | 284 | 194 |
| 10 | 282 | 174 | | 24 *(cũ 21)* | 359 | 217 |
| 11 | 201 | 157 | | 25 *(cũ 22)* | 261 | 172 |
| 12 | 215 | 155 | | 26 *(cũ 23)* | 245 | 194 |
| 13 | 269 | 168 | | 27 *(cũ 24)* | 169 | 138 |
| 14 | 321 | 199 | | 28 *(cũ 25)* | 238 | 199 |
| 15 | 187 | 122 | | 29 *(cũ 26)* | 263 | 136 |
| **Tổng 22 slide** | **5.294** | **3.504** <br>**−34%** | | *3 slide thực nghiệm mới (17–19)* | — | **417** |

> Cột "Slide" theo **đánh số hiện hành**; từ 18/10 lượt ba, ba slide thực nghiệm chen vào trước phần
> *the honest slide* nên mọi slide từ 17 trở đi **dịch +3**, ghi kèm số cũ để đối chiếu.

Đếm lại bất cứ lúc nào: script trong `/tmp` của phiên đó không giữ lại; đếm thủ công bằng cách bỏ
`<svg>`, bỏ `.speaker-note`, bỏ chú thích HTML rồi đếm từ.

**Sơ đồ slide 6 vẽ lại.** Bản cũ chỉ có một dòng chữ "ClinVar 2,56 M" và một forest plot trơ. Bản mới
là ba tầng: (1) phễu độ phủ 2.564.486 → 2.349.511 (93,0%) → 630.401 trong vùng degron, trong đó
530.412 VUS; (2) phép so **gây bệnh / lành tính, trong cùng một protein** vẽ bằng bốn thanh tỉ lệ
(26.078 · 28.940 so với 33.131 · 77.052 ⇒ tỉ lệ 0,90 so với 0,43); (3) tỉ số của hai tỉ lệ = **OR
2,148** đặt trên trục có mốc "no effect = 1,0" kèm CI. Nguồn số:
[variant-coverage-2026-10-15](../../research/variant-coverage-2026-10-15/README.md).

<a id="ra-bo-cuc-18102026"></a>
## Rà bố cục từng slide — 18/10/2026 (lượt thứ hai)

Yêu cầu: mỗi slide **một ý chính**, trình bày **trực quan** thay vì liệt kê trong hộp, dùng bố cục
chuẩn (chia cột, lưới, trục thời gian) và **để khoảng trắng làm việc** thay vì dồn chữ lên đỉnh.
Đã soi **từng trang** bằng ảnh render thật (PDF → PNG), không đoán.

**Lỗi tìm thấy và đã sửa**

| Slide | Lỗi bố cục | Đã làm |
|---|---|---|
| 1 | chữ dồn vào 55% bên trái, dải peptide ngắn | tiêu đề lớn hơn, **dải peptide thành băng ngang gần hết trang**, thông tin người làm xếp **3 cột** dưới một đường kẻ |
| 2 | GIF nền đen chọi bảng màu, không thêm thông tin | **gỡ GIF**, ba từ khoá thành chip, căn giữa theo chiều dọc |
| 5 | GIF + chip trôi rời rạc, đáy trống | gom GIF và ba chip vào **một card**, các khối dàn đều theo chiều dọc |
| 7 | hình Fig. 1 của tác giả **không đọc nổi** ở cỡ cột slide | đổi sang **sơ đồ FACS** đơn giản, cỡ lớn, caption ở dưới; Fig. 1 chuyển xuống **phụ lục A5** |
| 8 | chỉ là bảng 10 dòng × 5 cột, chiếm nửa trang trên | **vẽ lại thành biểu đồ hai trục**: năm × đơn vị dự đoán, chấm đặc = nhãn đo được, chấm rỗng = nhãn curated, **cột `residue` để trống** và chỉ có đề tài đứng đó. Bảng đầy đủ → **phụ lục A7** |
| 13 | hai cột hộp, trục thời gian bị nén nhỏ ở góc | **trục thời gian thành băng hero** trên cùng + ba chip mốc, hai bảng xuống **hai cột** bên dưới |
| 25 | đáy trống 35% | **lưới ba card G1/G2/G3** trên cùng, bảng tuần + hai card ở giữa, **thanh tiến độ tuần chạy ngang dưới cùng** |
| 26 | bốn câu hỏi nhỏ ở đỉnh, hố trống giữa trang | bốn câu hỏi thành **lưới 2×2 giãn đầy khung**, cỡ chữ 16px, "Thank you" thành thanh dưới cùng |
| 6 · 19 | khối cuối bị đẩy ra ngoài khung | chuyển khối sang cột trái / xuống ghi chú |

**Hai tiện ích CSS mới** (dùng lại được, khai báo ở `deck.css`):

- `.slide.fill` — dàn đều các khối theo chiều dọc, **chỉ khi khối ≥ 3** (dùng `:has(> :nth-child(3))`),
  vì với 2 khối thì `space-between` tạo hố ở giữa. Đang dùng ở slide 5, 7, 10, 11, 14, 15, 18, 20, 22, 23.
- `.slide.mid` — căn giữa theo chiều dọc khi nội dung ngắn hơn khung, để khoảng trắng **chia đều trên dưới**
  thay vì dồn hết xuống đáy. Đang dùng ở slide 2, 10, 11, 14, 15, 22, 23.

**Cách kiểm tràn khung** (chạy lại khi sửa bố cục): nhân bản `index.html` thành một file tạm, chèn CSS
cho mọi `.slide` hiện cùng lúc ở `height:720px`, chèn script bật hết `[data-step]` rồi đo
`getBoundingClientRect().bottom` của mọi phần tử so với mép trên slide, ghi kết quả vào `document.title`,
chạy Chrome `--headless --dump-dom` và đọc `OVF=`. Lần cuối: **`OVF=none`** trên cả 41 slide.

<a id="slide-thuc-nghiem-18102026"></a>
## Ba slide thực nghiệm trong phần Feasibility — 18/10/2026 (lượt thứ ba)

Theo yêu cầu Trọng: phần *Feasibility* phải **trình bày các thực nghiệm**, không chỉ đưa ra bảng hằng số.
Thêm **ba slide** trước slide "the honest slide"; phần này nay là **6 slide** (`Problem definition · 1…6 of 6`).

| # | Slide | Ý chính | Hình |
|---|---|---|---|
| 17 | **The four models being compared** | M0/M1/M2/M3 và ΔPAP `cnn2w1`/`cnn2w7` **nhìn thấy gì** quanh residue bị thay | bốn dải 28 ô, tô vùng mỗi mô hình đọc được |
| 18 | **Experiment 1 — the scanning set** | ngữ cảnh ±3 đáng bao nhiêu, so với chỉ số vị trí và với đối chứng đã công bố | thanh ngang 6 mô hình + trần 0,9458, kèm thang delta ghép cặp |
| 19 | **Experiment 2 — the saturation matrix: two regimes** | chế độ A chuyển giao từ bộ quét (**vẫn thua**, và hai thang đo **đảo chiều**); chế độ B học trực tiếp trên ma trận (**vượt mốc**) — viết lại 18/10 | hai bảng thanh: mức ô (AUROC, 4 cột) và mức vị trí (Spearman) |
| 20 | Feasibility (slide cũ) | **rút gọn**: bỏ bảng hằng số trùng (nay ở slide 18–19 và phụ lục A2), giữ hai KPI, trần, MDE 0,0123 và giới hạn nhãn | giữ nguyên biểu đồ cột cũ |

Số trên ba slide này lấy nguyên từ
[residue-task-derisk-2026-10-15](../../research/residue-task-derisk-2026-10-15/README.md) và
[pap-baseline](../../research/pap-baseline/README.md): M0 0,8393 · M1 0,8445 · M2 0,8625 · M3 0,8682 ·
M4 0,8684 · ΔPAP `cnn2w1` 0,7943 · `cnn2w7` 0,8357 · trần 0,9458 (bộ quét); M0 0,7071 · M3 0,7273 ·
ΔPAP `cnn2w1` 0,7693 · trần 0,9519 và Spearman 0,4368 / 0,4440 / 0,3553 · trần 0,6989 (bộ bão hoà).

⚠ **Cập nhật 18/10/2026 — số của chế độ B lấy từ chỗ khác.** Ridge M3 **0,8082**, gate+ΔPAP 0,8002, ba ứng
viên FiLM 0,8028 / bilinear 0,7933 / cross-ridge 0,7924, **kiến trúc Degformer huấn luyện lại dưới cov80
0,7500**, Degformer checkpoint 0,9248 (0,9227 trên tập con không chồng) và mọi CI ghép cặp lấy từ
[g2-saturation-2026-10-18](../../research/g2-saturation-2026-10-18/README.md) và
[g2-extension-2026-10-18](../../research/g2-extension-2026-10-18/README.md). **Không trộn** số chế độ A
(M0/M3 chuyển giao) với số chế độ B thành một chuỗi tiến bộ: hai chế độ khác **ngân sách nhãn**.

⚠ **Trục hoành của hai biểu đồ thanh không bắt đầu từ 0** (0,75 và 0,65) để thấy được chênh lệch; điều này
**in ngay trên hình**. Nếu GVHD hỏi, nói thẳng.

⚠ Thêm ba slide làm **số thứ tự dịch +3** từ slide 17 trở đi; các câu tham chiếu chéo trong deck
(“slides 17 and 22”, “slides 23–24”, eyebrow của phụ lục A2/A3/A4) đã được sửa theo.

<a id="tach-slide-va-bo-emoji-18102026"></a>
## Tách slide theo ý chính và bỏ emoji — 18/10/2026 (lượt thứ tư)

**Tách năm slide** bị dồn hai ý trở lên. Tiêu chí: slide có ≥ 6 khối (card + bảng) **và** ≥ 170 từ, mà hai
phần nói hai chuyện khác nhau.

| Slide cũ | Tách thành | Vì sao |
|---|---|---|
| Group 2 — measured maps | **10** nguồn nhãn của cả lĩnh vực · **11** vì sao không bài nào trả lời mức residue (kèm phép kiểm hoán vị tự đo) | hai ý: "data của họ" và "giới hạn của họ"; phép kiểm hoán vị là **phép đo của mình**, cần chỗ riêng |
| Contribution: three pillars | **15** ba trụ + năm đóng góp · **16** phân rã *where the information sits* | phân rã là một **phép đo**, không phải một dòng trong bảng |
| The resulting dataset | **25** hai bộ nhãn, hai vai · **26** split theo cụm + định dạng bản ghi | thiết kế nhãn và cách cắt dữ liệu là hai quyết định khác nhau |
| Proposed approach | **27** phần đã chốt · **28** phần mở (A/B/C + giám sát yếu) | "đã chốt" và "còn mở" không nên nằm chung một khung |
| The software deliverable | **30** vì sao phần mềm là đóng góp · **31** dịch vụ trả về gì + đối chứng công cụ | lý lẽ và đặc tả là hai nhịp nói khác nhau |

Slide **15 (ba trụ) vẽ lại cho có trọng tâm**: bỏ bảng C1–C5 nhiều chữ, thay bằng **ba cột trụ**, mỗi đóng
góp là một card ngắn có dấu trạng thái và **một con số** (OR 2.148 · +0.0300 · −0.0420), kết lại bằng một
dòng: *bốn trong năm đã đo, phần mở là C4 và nó có một con số để đạt*.

**Bỏ hết emoji khỏi mặt slide.** Trước đây dùng `✓` `⬜` `⚠` (31 chỗ). Nay:

- `.chip::before` vẽ **một ô vuông nhỏ** cùng màu chữ của chip — vuông đặc cho *đã đo*, vòng tròn rỗng cho
  *còn mở*, chấm tròn cho *cảnh báo*. Không ký tự nào, nên không phụ thuộc font emoji của máy.
- Bảng đối chứng công cụ dùng `.mark` (ô vuông xanh) thay cho `✓`.
- Chữ `G1 ✓ / G2 ⬜ / G3 ⚠` trong SVG rút còn `G1 / G2 / G3`, vẫn giữ màu phân biệt.
- Ghi chú người nói **giữ nguyên** `⚠` vì đó là ghi chú làm việc, không chiếu lên màn hình.

⚠ Tách slide làm số thứ tự đổi lần nữa; đã rà lại **toàn bộ 33 tham chiếu chéo** trong deck (gồm eyebrow
các phụ lục, nhãn `slide N` trong hình và trong ghi chú người nói) bằng cách liệt kê rồi sửa từng cái.

<a id="quy-uoc-khung-18102026"></a>
## Quy ước khung và chữ trong khung — 18/10/2026 (lượt thứ năm)

**Một kiểu khung duy nhất.** Trước đây mỗi loại card tô một mảng nền riêng (xanh / đỏ / vàng / xanh dương)
cộng thêm viền trái 3px, nên slide trông loang lổ. Nay:

| | Trước | Sau |
|---|---|---|
| `.card` | nền trắng + viền | **nền trong suốt** + viền mảnh `--rule` |
| `.card.key / .good / .alert / .open` | **tô nền** + viền trái 3px | chỉ **đổi màu chữ tiêu đề** `.card-t` và màu viền nhạt; `.open` dùng viền **gạch đứt** |
| `.chip` | tô nền theo loại | **viền mảnh + chữ màu**, nền trong suốt |
| hàng bảng nhấn | tô nền `--degron-bg` / `--model-bg` | `tr.hi` / `tr.mine`: **viền trái màu + chữ đậm** |
| 12 chỗ `style="border-left:3px solid …"` nội tuyến | rải rác trong HTML | **xoá hết**, chuyển thành class `key/good/alert/open` |

Quy tắc khi thêm slide mới: **không bao giờ tô nền một khối chữ**. Muốn phân loại thì đổi màu `.card-t`,
hoặc dùng `.chip`. Màu nền chỉ còn xuất hiện **bên trong sơ đồ SVG**, nơi mảng màu mang nghĩa (thanh, ô
ma trận, vùng nhấn).

**Viết lại 26 khối chữ.** Mọi đoạn văn ≥ 22 từ trên slide đã được viết lại thành câu nhãn ngắn, ngắt dòng
theo ý, số tách ra khỏi câu. Ví dụ:

> *Trước:* “Own measurement: shuffle the residue order of a peptide and PAP's score does not move — Pearson
> 1.000000 between original and shuffled predictions. That is the formal gap, stated again on slide 13.”
>
> *Sau:* **Shuffle the residues, the score does not move.** / Pearson **1.000000**, original vs shuffled ·
> the formal gap: slide 13

Cách đếm lại: bỏ `<svg>`, bỏ `.speaker-note`, bỏ comment, rồi liệt kê mọi `<p>`/`<li>` dài ≥ 22 từ — hiện
**không còn khối nào**.

<a id="noi-dung-khung-18102026"></a>
## Thang chữ và cách viết trong khung — 18/10/2026 (lượt thứ sáu)

Lượt năm mới đổi **kiểu khung**; lượt này đổi **chữ bên trong khung**.

**Một thang chữ, ba cỡ.** Trước đây mỗi khung tự đặt `font-size` nội tuyến — có **11 cỡ khác nhau**
(11 · 11,5 · 12 · 12,5 · 12,8 · 13 · 13,5 · 14 · 14,5 · 15 · 16px), nên hai khung cạnh nhau lệch cỡ.
Đã thay **101 chỗ** nội tuyến bằng ba class trong `deck.css`:

| Class | Cỡ | Dùng cho |
|---|---|---|
| `.t-lead` | 15px | một câu dẫn trong khung, tối đa một câu |
| mặc định `.card` / `.t-body` | 13,5px | thân khung |
| `.t-note` | 12px | dòng phụ, chú giải trong khung |

Ngoài thang này chỉ còn `.cap` 10,5px, `.lblx` 9,5px, `.kpi .v` (34px, `.kpi.sm` 26px, `.kpi.xs` 20px),
`.lede` 17px và `h1/h2`. Các `.stat` 17px, `.pillar-h` 20px, `.seqline` 17px, `.thanks` 18px cũng đã thành
class. **Thuộc tính `font-size` bên trong `<svg>` không thuộc thang này** — sửa chúng sẽ phá tỉ lệ sơ đồ.
Hiện ngoài SVG chỉ còn 9 / 9,5 / 10,5px (chú thích hình, mono trong bảng), một `<tspan>` chỉ số dưới và
54px của tiêu đề trang bìa.

**Mẫu `.lines` — mỗi dòng một ý.** Thay cho đoạn văn trong khung. Nhãn in đậm đứng trước, dấu `·` do CSS
sinh ra (không gõ tay), số tách khỏi câu bằng `.v`:

```html
<div class="lines">
  <div><span class="k">Ridge − ΔPAP</span><span class="x"><span class="v">+0.0389</span>
    <span class="lblx">CI [+0.0216, +0.0571]</span></span></div>
</div>
```

Dùng `.lines.sm` khi khung chật. Giới hạn thực tế: **một dòng khoảng 12 từ**. Đã áp cho **23 khung** ở các
slide 8, 11, 16, 17, 18, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32 và phụ lục A2.

**Gộp khung.** Slide 22 (*Feasibility*) trước có **bảy** khung nhỏ ở cột trái; nay còn **ba**, mỗi khung trả
lời một câu hỏi: ba delta · cái đã xác lập · bốn giới hạn. Slide 15 gộp hai chip của C4 vào cùng hàng với
con số để cột trụ 2 không đè lên khung tổng kết.

**Lỗi đã sửa nhân tiện:** sáu khung ở slide 15 khai báo `class` **hai lần**
(`<div class="card" … class="good">`), nên bản thứ hai bị trình duyệt bỏ qua và viền phân loại chưa bao giờ
hiện. Nay gộp thành một thuộc tính.

<a id="kiem-18102026"></a>
### Cách kiểm sau khi sửa khung

Probe cũ chỉ bắt **tràn khỏi mép slide**, không bắt **hai khung đè lên nhau** trong lòng slide — đúng lỗi
mà slide 15 mắc phải ở lượt này. Probe nay đo cả hai: với mỗi slide, (1) mọi phần tử so với `rect` của
slide, (2) mọi cặp `.card` / `.fig` / `table` **không lồng nhau** có phần giao > 2px. Kết quả ghi vào
`document.title` dạng `OVF=… LAP=…`, chạy bằng Chrome `--headless --dump-dom`.
Lần cuối 18/10/2026: **`OVF=none LAP=none` trên cả 41 slide**, PDF headless ra đúng **41 trang**.

⚠ Probe này bắt **tràn** và **đè**, **không** bắt được chỗ chữ quá dài bị cắt bên trong một `<svg>` (text SVG
không wrap và không làm phần tử cha nở ra). Chỗ đó phải **soi ảnh render**; lượt này đã sửa hai ca như vậy ở
slide 22 (chú giải dưới biểu đồ) và slide 29 (chú giải lưới).

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
