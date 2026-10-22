# Hình và GIF dùng trong deck này — nguồn, giấy phép, băm

> ⚠ **22/10/2026:** cột "Slide" bên dưới là số slide của bản cũ; deck nay có 20 slide lõi + A1–A41 (xem README, mục *Bản 22/10/2026*). Slide cũ 2–14 nay là A21–A33 và 16–20 là A34–A38 (ví dụ RING gif: A23; FACS: A25; Fig. 4: A28). Hình mới tự dựng (SVG trong `index.html`), không thêm tài nguyên ngoài.
>
> Cập nhật **18/10/2026**, khi rút gọn chữ trên slide và bổ sung ảnh.
> **Deck dùng nội bộ** (báo cáo tiến độ với GVHD), repo private ([D-004](../../../../DECISIONS.md#d-004)).
> Trọng đã chỉ đạo ngày 18/10/2026: ở phạm vi nội bộ này **không chặn theo giấy phép**, nhưng vẫn
> ghi lại nguồn ở đây để sau này muốn công bố thì biết phải gỡ hoặc xin phép cái nào.

## 1. Ảnh của tác giả bài báo (có sẵn trong repo)

| File | Slide | Nguồn | Giấy phép | Ghi công trên slide |
|---|---|---|---|---|
| `lectures/.../voutsinos2026-f1.jpg` | 7 | Voutsinos et al., *Sci Adv* 2026, Fig. 1 — DOI 10.1126/sciadv.adz3483 | **CC BY-NC 4.0** | ✅ figcaption dưới hình |
| `assets/voutsinos2026-f4.jpg` | 8 (bản 23 slide) | Voutsinos et al., *Sci Adv* 2026, Fig. 4 — cùng DOI | **CC BY-NC 4.0** | ✅ figcaption dưới hình |

**Sửa đường dẫn slide 8 — 21/10/2026:** hình Fig. 4 (kiến trúc PAP và hai biểu đồ
holdout) được khôi phục nguyên bản từ lịch sử Git tại commit
`8c6c53ae448a5f57f75d948943f6d6fdfed517e5`, đường dẫn cũ
`lectures/degron-footprint/assets/figures/voutsinos2026-f4.jpg`.
Lưu hình ngay trong `assets/` của deck để dùng offline sau khi thư mục bài giảng bị xóa.
Nguồn: [bài báo gốc](https://doi.org/10.1126/sciadv.adz3483),
[toàn văn XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12880521/fullTextXML).
SHA-256: `455604ed104d11996ea678f57c3b0e2c734659eca946158268043c5492d19418`.

Hai caption này **thêm mới 18/10/2026**: trước đó phần ghi công nằm ở `.foot`, mà `.foot` đã bị gỡ
khỏi slide, nên ghi công không còn hiển thị. Caption là điều kiện của CC BY-NC, không bỏ được.

## 2. Ảnh và GIF tải từ Wikimedia Commons

| File | Slide | Trang gốc | Giấy phép | SHA-256 (16 ký tự đầu) | Ngày tải |
|---|---|---|---|---|---|
| `assets/ring-domain.gif` | 5 | `File:1chc_animated.gif` — miền RING finger C3HC4, PDB 1chc, tác giả **Hsp90** | **CC BY-SA 3.0** | `c9ba053c19f9daf1` | 15/10/2026 |
| `assets/fam188a.gif` | — | `File:I-TASSER_predicted_protein_fold_of_Fam188a.gif` | **CC BY-SA 3.0** | `0e37f44b52235448` | 15/10/2026 |
| `assets/ubiquitin.gif` | 4 | `File:2qjl_animated.gif` — cấu trúc họ ubiquitin, PDB 2QJL | **CC BY-SA 3.0** | `f9e2e64ebd694fe4` | **18/10/2026** |
| `assets/proteasome.png` | 4 | `File:Proteasome (NIH BioArt 667 - 758783).png` | **Public domain** (NIH BioArt) | `92fd5e869c772919` | **18/10/2026** |
| `assets/facs-scheme.png` | 7 | `File:Flow_cytometry_scheme.png` | **CC BY-SA 3.0** | `b058adba99058da1` | **18/10/2026** |

⚠ **ShareAlike:** bốn file CC BY-SA 3.0 ở trên đòi ghi công và điều khoản chia sẻ tương tự nếu
tạo bản phái sinh. Deck chỉ **nhúng nguyên hình** kèm ghi công ngắn trên slide, nên ở mức hiện tại
là dùng dạng sưu tập, không phải phái sinh. Trước khi đưa deck ra ngoài (nộp, đăng, gửi file cho
người khác) thì rà lại mục này.

> `fam188a.gif` đã **thử rồi gỡ** ngày 18/10: nền đen của hình chọi với bảng màu sáng của deck, và ở cỡ vừa slide thì nó không thêm thông tin nào so với sơ đồ tự dựng. File giữ lại trong `assets/`, hiện **không dùng trên slide nào**.
>
> Hình Fig. 1 của Voutsinos cũng đã **chuyển từ slide 7 xuống phụ lục A5**: ở cỡ vừa cột slide thì sáu panel của nó không đọc nổi. Slide 7 nay dùng sơ đồ FACS đơn giản.

## 3. Hình tự dựng

Mọi sơ đồ còn lại là **SVG + CSS tự dựng trong `index.html`**, không tải về. Riêng
`figures/example-matrix.svg` **sinh từ dữ liệu đo được** bằng
[`make_example_matrix.py`](../../research/slide-figures-2026-10-15/README.md).

Sơ đồ ClinVar ở slide 6 **vẽ lại 18/10/2026** (phễu độ phủ → phép so 2×2 → tỉ số chênh), số lấy từ
[`research/variant-coverage-2026-10-15/`](../../research/variant-coverage-2026-10-15/README.md):
2.564.486 → 2.349.511 (93,0%) → 630.401 trong vùng degron (530.412 VUS); 2×2 thô
26.078/28.940 so với 33.131/77.052; MH theo protein **2,148 [2,072; 2,227]** trên 3.114 protein.
