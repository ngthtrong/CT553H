# Quy chuẩn thiết kế cho hình minh họa tổng quan (illustrated figures)

Áp dụng cho mọi hình `V1…V6` dựng trong **Figma Design** (không phải FigJam) bằng Figma MCP. Mục tiêu: hình **trực quan**, không chỉ là flowchart — có logo công cụ, biểu đồ dữ liệu thật, ảnh/giao diện thật, hình minh họa từng bước.

## 1. Khung và kích thước
- Mỗi hình là **một frame** trong một file Figma Design riêng (tên file: `Thesis figure Vn <tên>`), nền trắng, rộng **1600 px cố định**, cao ≤ 1500 px (tối đa 1900 nếu bắt buộc), lề 48 px.
- Dùng **auto-layout** cho mọi cụm có quan hệ cấu trúc; không đặt toạ độ tay trừ khi cần.
- Bố cục đọc từ trái sang phải hoặc trên xuống dưới, **đánh số bước** bằng huy hiệu tròn (1, 2, 3…) màu xanh `#0072B2`, chữ trắng.

## 2. Chữ (quan trọng cho bản in)
- Phông **Inter**. Kiểm tên style bằng `listAvailableFontsAsync` ("Semi Bold", không phải "SemiBold").
- Khi in rộng 16 cm, 1 px ≈ 0,1 mm, nên: **tiêu đề 40 px (Bold), tiêu đề cụm 30 px (Semi Bold), thân 26 px, nhỏ nhất 24 px**. **Cấm chữ nhỏ hơn 24 px** (trong frame, kể cả nhãn trục biểu đồ sau khi đặt vào).
- Nhãn ngắn, tiếng Anh (luận văn viết tiếng Anh). Không viết đoạn văn trong hình.

## 3. Màu (bảng Okabe–Ito, an toàn cho mù màu)
| Vai trò | Hex |
|---|---|
| Chữ chính | `#1E1E1E` |
| Chữ phụ | `#4A5563` |
| Đường nét | `#7A8594` |
| Nền panel | `#F5F7FA`, viền `#D5DBE3` |
| Xanh chủ đạo | `#0072B2` (nền nhạt `#E1EFF8`) |
| Xanh trời | `#56B4E9` |
| Cam | `#E69F00` (nền nhạt `#FBEFD0`) |
| Đỏ cam | `#D55E00` (nền nhạt `#F8E0D0`) |
| Xanh lá | `#009E73` (nền nhạt `#D5EFE7`) |
| Tím hồng | `#CC79A7` |
- Heatmap ΔPSI: thang phân kỳ **xanh `#0072B2` – trắng – đỏ cam `#D55E00`**, tâm 0, chú giải luôn có.
- Màu mang ý nghĩa: xanh lá = trong miền/được chấp nhận, cam = cảnh báo, đỏ cam = từ chối/ngoài miền, xanh dương = dữ liệu/mô hình.

## 4. Logo và biểu tượng
- **Logo công cụ**: tải SVG từ gói `simple-icons` (CC0) bản ghim `simple-icons@13.21.0` qua `https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/<slug>.svg`; kiểm file thật sự là SVG. Tô màu thương hiệu (hex dưới đây) bằng cách thêm `fill` vào thẻ `<svg>` trước khi nhập vào Figma. Đặt trong ô trắng bo góc 96×96 px, logo 56–64 px, tên công cụ bên dưới (24 px). Slug và màu: fastapi `009688`, react `61DAFB`, typescript `3178C6`, vite `646CFF`, postgresql `4169E1`, sqlite `003B57`, docker `2496ED`, nginx `009639`, python `3776AB`, numpy `013243`, scikitlearn `F7931E`, pytorch `EE4C2C`, kaggle `20BEFF`, googlecolab `F9AB00`, github `181717`, huggingface `FFD21E`, playwright `2EAD33`, openapiinitiative `6BA539`, uniprot (không có: dùng chữ), pandas `150458`, jupyter `F37626`, matplotlib (không có: bỏ qua). Nếu slug không tồn tại, **bỏ logo đó** và dùng ô chữ, không bịa logo.
- **Biểu tượng chung** (máy tính, đám mây, tệp, khiên, bảng…): SVG từ `lucide-static@0.468.0` (ISC) tại `https://cdn.jsdelivr.net/npm/lucide-static@0.468.0/icons/<tên>.svg`, nét 2 px, màu `#4A5563` hoặc màu vai trò.
- Nhập SVG vào Figma bằng `figma.createNodeFromSvg(svg)` (SVG phải có `viewBox` và `width`/`height`); tuyệt đối không dựng icon bằng đường thẳng xoay tay.
- Ghi nguồn/giấy phép logo và icon trong index-part (nhãn thương hiệu thuộc chủ sở hữu, chỉ minh họa).

## 5. Biểu đồ và ảnh thật
- Biểu đồ vẽ bằng **matplotlib** (nạp skill `dataviz` trước khi viết mã biểu đồ), từ **dữ liệu thật** trong repo (JSON/npz/tsv kết quả). Mọi con số trong hình phải truy được về file nguồn; không bịa, không làm tròn khác file. Lưu script vào `report/assets/diagrams/src/viz/<tên>.py` (chạy bằng `.venv/bin/python -I`, ghi ra `src/viz/inputs/`).
- Xuất PNG gấp đôi kích thước đặt (đặt 640 px thì PNG ≥ 1280 px), nền trong suốt hoặc trắng, phông trong biểu đồ ≥ 24 px **sau khi đặt vào frame** (tính theo tỉ lệ), thang màu như §3, bỏ khung thừa, có đơn vị trục.
- Đưa ảnh vào Figma bằng công cụ `upload_assets` (nạp schema qua ToolSearch), rồi đặt vào ô bo góc, kèm chú thích 24 px; ảnh giao diện thật (từ `src/viz/inputs/ui-*.png`) đặt trong khung "cửa sổ trình duyệt" đơn giản.
- Chỉ dùng ảnh/biểu đồ có thật; mọi ví dụ phải nói rõ là *ví dụ* (tên peptide/tile).

## 6. Trung thực học thuật (không thương lượng)
- Số liệu là **benchmark phát triển OOF**, không phải kiểm chứng ngoài; không ghi "validated", không ghi "state-of-the-art", không so sánh với mô hình khác ngoài những gì có trong file kết quả.
- Không đổi trạng thái G2/G3; không nói "chưa ai làm".
- Không dùng dữ liệu Koren/MetaDegron/Larsen trong hình công khai; nguồn Koren chỉ nhắc như "audited, not imported" nếu cần.
- Không dùng nhãn "probability of disease"; sự kiện là `ΔPSI ≥ 1,0`.

## 7. Đầu ra mỗi hình
1. `report/assets/diagrams/<tên-hình>.png` (xuất frame ở scale 2 → rộng 3200 px; kiểm bằng mắt, không cắt chữ).
2. `report/assets/diagrams/index-parts/<Vn>.md`: id hình, caption tiếng Anh gợi ý, hình thể hiện gì, file dữ liệu/script nguồn, URL file Figma + node id frame, nguồn/giấy phép logo-icon, giới hạn.
3. Script biểu đồ trong `src/viz/`.
- Không sửa chương LaTeX, không sửa `diagram-index.md` (tôi gộp), không sửa slide, không git commit.
