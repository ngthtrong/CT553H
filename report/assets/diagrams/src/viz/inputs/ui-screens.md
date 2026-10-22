# Ảnh giao diện thật của web tool (V0)

Chụp ngày 22/10/2026 từ **backend thật** (`make -C topics/degron-footprint/system/app dev-api`, DB SQLite dựng bằng ETL, mô hình `m3-ext4.0-platt-v1`) qua Vite dev server (`npm run dev`, proxy `/v1` tới cổng 8000), **không dùng mock**. Trình duyệt Chromium (Playwright), viewport 1280 px, `deviceScaleFactor` 2 (ảnh rộng 2560 px), theme sáng. Không sửa mã app.

Dựng lại: chạy hai server như trên, rồi
`cd topics/degron-footprint/system/app/frontend && NODE_PATH=$PWD/node_modules node ../../../../report/assets/diagrams/src/viz/capture_ui.cjs` (biến `ONLY=a,b,c,d,e,f` để chụp từng nhóm).

## Tile ví dụ và trạng thái miền thật (do API trả)

| Dùng cho | Protein / tile | Chuỗi | Trạng thái miền (API) |
|---|---|---|---|
| (b) trong miền | **COL6A6, A6NMZ7, tile 28** (residues 622–649) | `DIMFLVDSSGSIGPENFSKMKTFMKNLV` | `measured_in_domain`, PSI đo của tile **1,88**, 38,4 reads; kèm cảnh báo `TRAINING_PEPTIDE` (tile thuộc 176 peptide huấn luyện, điểm không phải ước lượng ngoài mẫu) |
| (c) ngoài miền | **A6NMZ7, tile 7** (residues 139–166) | `ASSESEDNVEEASKALRKDGVKIISVGV` | `measured_out_of_domain`, PSI đo **5,10** (> 4,0), 84,4 reads; `POST /v1/predict` trả `422 OUT_OF_DOMAIN` trừ khi `override_domain` |
| (d) chuỗi gõ tay | chuỗi của tile 28, dán vào ô nhập | `DIMFLVDSSGSIGPENFSKMKTFMKNLV` | `unknown` (không tra tile đã lưu; chưa có gate model): cảnh báo `DOMAIN_UNKNOWN` |
| bản đồ tile | A6NMZ7 (98 tile) | — | 49 `measured_in_domain`, 41 `measured_out_of_domain`, 8 `measured_unreliable` (đếm từ `GET /v1/proteins/A6NMZ7/tiles`) |

Chuỗi ở (d) cố ý trùng tile 28 để so sánh: cùng chuỗi nhưng nhập tay thì trạng thái là *unknown*, vì server không khớp chuỗi gõ với tile đã lưu (api-spec §4).

## Các file (đều trong thư mục này)

| File | Nội dung | Kích thước (px) |
|---|---|---|
| `ui-input.png` | (a) Trang nhập, tab "Paste a sequence", đã dán 28-mer, bộ đếm 28/28, cảnh báo miền | 2560 × 1640 |
| `ui-input-search.png` | Tab "Choose a protein", tìm `COL6A6`, một kết quả (98 tiles) | 2560 × 1640 |
| `ui-tile-picker.png` | Bản đồ tile COL6A6: nền xanh = trong miền, gạch chéo = ngoài miền, viền chấm = đo không tin cậy; tile 28 được chọn | 2560 × 1640 |
| `ui-result-in-domain.png` | (b) Kết quả tile 28: khối trạng thái miền, cảnh báo TRAINING_PEPTIDE, nhãn bằng chứng, heatmap 28×19, 8 dòng đầu bảng xếp hạng (cắt phần còn lại của 532 dòng) | 2560 × 4238 |
| `ui-result-out-of-domain.png` | (c) Tile 7 bị từ chối, nút "Choose another tile" và "Score anyway" | 2560 × 1640 |
| `ui-result-unknown.png` | (d) Chuỗi gõ tay: miền *unknown*, cảnh báo, heatmap, bảng xếp hạng (8 dòng đầu) | 2560 × 4342 |
| `ui-model-card.png` | (e) Thẻ mô hình, phần đầu (id, miền, bằng chứng, SHA-256, bảng hiệu năng); bản đầy đủ ở `ui-model-card-full.png` (2560 × 7108) | 2560 × 2300 |
| `ui-heatmap-crop.png` | (f) Thang màu + chú giải + heatmap 28×19 + dòng "Hatched cell = wild type" | 2156 × 1832 |
| `ui-heatmap-only.png` | Chỉ lưới heatmap, không chú giải | 1272 × 1626 |

Ảnh `ui-result-in-domain.png` và `ui-result-unknown.png` cao hơn viewport 820 vì cần cả heatmap (28 hàng) và đầu bảng xếp hạng; hai ảnh này chụp "full page" rồi cắt sau dòng thứ 8 của bảng.

## Kiểm bằng mắt
- Mọi giá trị trên màn hình là đầu ra thật của API (không có dòng "MOCK FIXTURE", model id là `m3-ext4.0-platt-v1`, SHA-256 của trọng số hiển thị ở thẻ mô hình).
- Không có lỗi, không cắt chữ ở các ảnh trên (đã xem từng ảnh). Vòng focus xanh của trình duyệt đã được bỏ trước khi chụp.
- Ô theme hiển thị "System" (đang ở chế độ sáng).

## Điều cần lưu ý khi dùng trong hình minh họa
- Heatmap dùng thang **viridis ngược** (vàng = xác suất thấp, tím đậm = cao) của chính app; nếu hình minh họa tự vẽ heatmap bằng thang khác (xanh–trắng–đỏ cam cho ΔPSI), nên nói rõ đó là hình vẽ lại, không phải ảnh chụp.
- Thẻ mô hình hiển thị khóa JSON thô (vd `p0_verdict_ridge.P1_delta_100_minus_50.delta`) và một dòng tiếng Việt (`chưa đủ bằng chứng cho giả thuyết thiếu nhãn`) lấy nguyên từ `results.json`: **không thật sự thân thiện với người đọc tiếng Anh**; nếu chèn ảnh này vào luận văn nên cắt vùng phía trên (id, miền, bằng chứng, SHA-256) và bỏ bảng hiệu năng. Đây là điểm cần sửa ở app (không sửa trong phiên này).
- Chữ trong ảnh chụp dùng phông hệ thống (DejaVu Sans trên máy này), không phải Inter.
