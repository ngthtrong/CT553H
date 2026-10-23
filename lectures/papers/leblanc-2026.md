[← Danh mục bài báo](README.md) · Về hub

# LeBlanc 2026 — mạng nơ-ron lý sinh giải thích được trên thư viện tile

| | |
|---|---|
| **Nơi công bố** | *Cell Systems* **17(9):101701**, 2026 |
| **DOI** | [10.1016/j.cels.2026.101701](https://doi.org/10.1016/j.cels.2026.101701) · PMID 42607673 · [PMC13596073](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596073/) |
| **Tiền ấn** | bioRxiv `2025.09.19.677413` (21/09/2025) |
| **Tác giả** | LeBlanc CJ, Agarwal P, Demaray JE, Hu G, Zintel MA, Lam AWY, Castro Hernandez JE, **Staller MV** |
| **Mức kiểm** | **[ĐÃ ĐỌC]** toàn văn từ bản thảo tác giả trên PMC |

Tên đầy đủ: *"Interpretable biophysical neural networks of transcriptional activation domains separate roles of protein abundance and coactivator binding."*

---

## Bài này **không** phải bài degron

Điều quan trọng nhất phải nói trước: dữ liệu của họ là **miền hoạt hoá phiên mã (AD)** trong nấm men, **không** phải degron. Sàng riêng của họ: tile **40 acid amin**, bước 5, 20.731 trình tự thiết kế / 17.732 đo được, Sort-seq với mCherry (độ dồi dào) ghép GFP (độ mạnh AD). "Degron" xuất hiện **3 lần** trong toàn bài, và [Larsen 2025](larsen-2025.md) (ref 47) cùng [Voutsinos 2026](voutsinos-2026.md) (ref 48) chỉ được trích **hai lần**, làm y văn hỗ trợ cho một nhận xét về thành phần `[đọc]`.

Nên nó **không chiếm** claim mức residue của đề tài. Grep toàn văn tìm `per-residue`, `residue-level`, `single-residue`, `saturation`, `variant effect`, `mutagenesis` trả về **không kết quả nào** trong thân bài; mọi chỉ số là **mức tile** (n = 2.521); và khi có đối thủ mức residue, họ **gộp nó về mức tile** (*"To get a single value for ADPred, we averaged the predictions for the 40aa tile"*) `[đọc]`.

---

## Nhưng nó hạ **ba lập luận hỗ trợ** của đề tài xuống "thực hành chuẩn"

Đây là lý do bài này phải có mặt trong danh mục. Ba thứ đề tài từng tính là điểm trình bày riêng, nay đã có tiền lệ **đã công bố, cùng họ dữ liệu (thư viện tile)**:

| Thứ đề tài định làm | LeBlanc 2026 đã làm |
|---|---|
| Tách **độ dồi dào** khỏi **chức năng** trên thư viện tile | **Đây là headline của họ** (ngay trong tiêu đề) |
| **Split theo cụm protein** trên tile chồng lấn | Clustering phân cấp trên ortholog nguyên vẹn, tile gán theo protein mẹ, **kèm kiểm "tương đồng test–train vs độ chính xác"** |
| **Đối chiếu trần replicate bằng số** | Nguyên văn: *"replicate Pearson correlation of **0.568** … our best performing NN **approached this ceiling** (Pearson correlation of **0.555**, p < 10⁻³⁰⁰)"* |

→ **Phải viết "theo LeBlanc et al. 2026"** khi dùng ba cách làm này, không trình bày như chọn lựa riêng của đề tài.

Mặt tốt: điều này **có lợi** cho rủi ro 6. Cách trình bày "đặt trần nhãn cạnh số của mô hình" nay có **tiền lệ công bố ở tạp chí tốt**, nên rất dễ bảo vệ trước GVHD.

---

## Và nó nêu một rủi ro khoa học trực tiếp: **thành phần > vị trí**

Kiến trúc của họ cực nhỏ — một filter tích chập → LeakyReLU → một lớp linear một đầu ra → LeakyReLU, **138 tham số** — và các đầu lý sinh dự đoán **hằng số cân bằng mức tile** (mô hình hai trạng thái, và ba trạng thái "acidic exposure") ghép qua hàm Hill. Đầu ra là **một số vô hướng cho mỗi 40-mer** `[đọc]`.

Với **30 seed × 200 bootstrap**, họ kết luận về ma trận trọng số của filter:

> *"horizontal streaks, indicating that **composition is more important than individual positions**"*, và các filter *"are **not picking up on specific protein motifs** and instead are picking up composition patterns"* — với trọng số theo từng vị trí *"highly variable"* qua các seed.

**Nếu điều đó cũng đúng cho tile degron**, thì một mô hình mức residue có thể đang **khớp nhiễu vị trí** — và đó là đe doạ trực tiếp cho rủi ro 2, độc lập với mọi chuyện nhiễu đo.

**Nhưng họ cũng cho luôn khuôn để kiểm:** báo **độ ổn định của trọng số theo từng vị trí qua seed và bootstrap**. Đây là một phép thử đề tài **nên chạy**, và nó rẻ `[đề xuất]`.

Một điểm đáng lưu: trục của đề tài **không** rơi vào bẫy đó theo bằng chứng đã đo — đổi kernel 1 → 7 cho **+0,1311** precision@3 mức residue (bài 5), tức ngữ cảnh vị trí **có** tín hiệu trên nhãn degron. Nhưng đó là bằng chứng của repo trên dữ liệu khác; **không** triệt tiêu được lo ngại, chỉ làm nó bớt nặng `[phân tích]`.

---

## Con số đáng nhớ

| | |
|---|---:|
| Tile đo được | 17.732 |
| Tham số mô hình | **138** |
| Trần replicate (độ dồi dào) | **0,568** |
| Mô hình tốt nhất của họ | **0,555** |
| Tập test mức tile | n = 2.521 |

Chi tiết: [báo cáo 15/10](../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/README.md) mục 6 và [ghi chép 05](../../topics/degron-footprint/research/larsen-nuclear-and-risks-2026-10-15/notes/05-gap-close-prior-art.md).

---

[← Danh mục bài báo](README.md) · Về hub
