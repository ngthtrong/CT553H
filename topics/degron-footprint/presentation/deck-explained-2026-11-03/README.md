# DỰ ĐOÁN HIỆU ỨNG ĐỘT BIẾN DEGRON Ở MỨC RESIDUE VÀ XÂY DỰNG CÔNG CỤ HỖ TRỢ PHÂN TÍCH

Mở [index.html](index.html) trực tiếp bằng Chrome hoặc Edge. Deck tiếng Việt gồm **31 slide chính và 5 phụ lục**, có GIF, video proteasome, sơ đồ chuyển động, các bước hiện dần và biểu đồ đổi metric. Tất cả tài sản chạy offline, không cần backend hoặc Node.

[slides.pdf](slides.pdf) là bản tĩnh 36 trang. [Ảnh tổng quan](previews/contact-main.png) giúp tra cứu nhanh. [Ghi chú người trình bày](speaker-notes.md) chứa lời giải thích, điều kiện so sánh và nguồn.

## Nội dung

- 1–7: protein, degron, WT/mutant, nhu cầu dự đoán từng phép thay, GPS và ΔPSI.
- 8–13: saturation/scanning, đơn vị mẫu, QC, pipeline và chống leakage.
- 14–20: Ridge, one-hot CNN, ESM2, pointwise/CNN/mCNN, frozen/LoRA và metric.
- 21–25: ba nhóm thí nghiệm về phạm vi PSI, ESM/CNN và chuyển giao.
- 26–31: công cụ, trạng thái, đóng góp, kiểm chứng tiếp theo và slide kết.
- 32–36: thuật ngữ, tạo nhãn, heatmap HIF1A, metric đầy đủ và nguồn.

Đã áp dụng hai annotation của người dùng: bỏ slide lộ trình học sáu buổi; phần dữ liệu trình bày trực tiếp, không phân chia hoặc so sánh các phiên bản dữ liệu. Tên model phục vụ được giữ đúng định danh trong tài liệu.

## Điều khiển

| Thao tác | Phím / nút |
| --- | --- |
| Hiện bước tiếp, sau đó chuyển slide | → / Space / Page Down |
| Bước trước | ← / Page Up |
| Chuyển thẳng slide | Shift + ← / → |
| Mục lục / ghi chú và nguồn | O / N |
| Dừng hoặc tiếp tục chuyển động | M |
| Toàn màn hình | F |
| Về mở đầu / slide kết | Home / End |

Vuốt ngang trên thiết bị cảm ứng. Nút đổi metric trên slide 23 chuyển giữa MAE, AUROC dương và AP dương. Video có nút phát/dừng riêng. Deck tôn trọng `prefers-reduced-motion`, dừng media khi slide ẩn và dùng poster khi in PDF. PDF hiển thị đủ mọi bước.

## Bằng chứng và phạm vi

Số liệu lấy từ JSON nghiên cứu đã lưu; không huấn luyện, đọc locked T hoặc thay model sản phẩm trong phiên dựng deck. Benchmark trình bày ESM2-35M, ensemble ba seed, năm outer folds; frozen/LoRA có phạm vi riêng. Chênh lệch MAE nhỏ giữa mCNN và CNN đi kèm CI và điều kiện train.

Heatmap HIF1A là nhãn đo. Chuỗi L4P, histogram GPS và các sơ đồ vector là minh họa. Điểm trong screenshot giao diện là fixture tổng hợp. Snapshot tiến độ local chỉ nằm trong notes, không là trạng thái live. Giới hạn suy luận nằm ở mỗi slide và trong [slide-sources.json](slide-sources.json).

Giữ nguyên deck nguồn `../deck-research-overview-2026-11-02/`; danh sách hash trước khi dựng nằm ở [reuse-manifest.json](reuse-manifest.json). Theme, font, một số SVG kết quả và ảnh giao diện được dùng lại. Các sơ đồ giải thích và engine hiện từng bước nằm riêng trong thư mục này.

## Tái dựng và kiểm tra

Từ gốc repo, dựng nội dung bằng Python chuẩn:

```bash
python3 -I topics/degron-footprint/presentation/deck-explained-2026-11-03/build-deck.py
```

Chỉ khi cần chuẩn bị lại media hoặc kiểm tra/render, tạo môi trường riêng; không cài vào môi trường campaign:

```bash
python3 -m venv /tmp/degron-deck-tools
/tmp/degron-deck-tools/bin/pip install -r topics/degron-footprint/presentation/deck-explained-2026-11-03/requirements-preview.txt
/tmp/degron-deck-tools/bin/python -m playwright install chromium
/tmp/degron-deck-tools/bin/python topics/degron-footprint/presentation/deck-explained-2026-11-03/prepare-media.py
python3 -I topics/degron-footprint/presentation/deck-explained-2026-11-03/build-deck.py
/tmp/degron-deck-tools/bin/python topics/degron-footprint/presentation/deck-explained-2026-11-03/validate-deck.py
```

Validator kiểm tra 36 slide, tràn chữ/hình, đường dẫn, ảnh, video thật, điều hướng từng bước, mục lục, notes, đổi metric, dừng chuyển động, reduced-motion, desktop/mobile, PDF, hash bằng chứng và nguyên trạng deck cũ. Kết quả ở [validation.json](validation.json); ảnh từng slide ở [previews/](previews/). Cần xem ảnh/PDF để đánh giá bố cục ngoài kiểm tra hình học tự động.
