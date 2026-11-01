# Workspace UI v2 — Degron Footprint

**Bản local để kiểm duyệt giao diện, ngày 01/11/2026.** Người dùng đã chọn **B — Workspace nghiên cứu hiện đại** sau [khảo sát ứng dụng tương tự](../style-research-2026-11-01/README.md). Bản này thay thế hướng thiết kế của bộ ngày 31/10.

Mở [index.html](index.html) trực tiếp bằng trình duyệt. Prototype không cần Node, cài package, backend, mạng Internet hay Figma. Mở đầu tại analysis minh hoạ để xem ma trận và inspector ngay.

Nếu muốn dùng localhost, chạy từ gốc repo:

```bash
python3 -m http.server 8891 --bind 127.0.0.1 \
  --directory topics/degron-footprint/system/design/workspace-ui-v2
```

Sau đó mở <http://127.0.0.1:8891/>. Không bind ra mạng ngoài. `Ctrl+C` dừng máy chủ.

## 1. Phạm vi của bản review

Đây là prototype tương tác bằng HTML/CSS/JavaScript, để chốt UX và hình thức trước khi triển khai vào ứng dụng React + TypeScript/FastAPI hiện có. Không thay đổi stack sản phẩm, API, database, mô hình hoặc dữ liệu nghiên cứu.

**Mọi giá trị score/xác suất và dataset demo đều là fixture tổng hợp để duyệt giao diện.** Chuỗi A6NMZ7 tile 28 và ví dụ tọa độ lấy từ BA; các giá trị hiển thị không phải kết quả chạy mô hình. Không có weights, calibrator, gate hay reference snapshot được load vào prototype.

Thay đổi project/snapshot/job/dataset chỉ ở bộ nhớ của tab, mất khi reload/đóng tab. Phiên xem thử không chứng minh lưu bền, recovery, worker hoặc tính đúng đắn nghiên cứu. File người dùng nhập được đọc tại trình duyệt; không gửi tới API nào. Không lưu payload sinh học vào URL, localStorage hoặc sessionStorage. CSP chặn các kết nối dữ liệu từ trang.

## 2. Cách duyệt các luồng

| Luồng | Cách thử | Điều cần chú ý |
|---|---|---|
| Ma trận và shortlist | Trang mở đầu → chọn ô hoặc dùng phím mũi tên → Add to shortlist | 28 vị trí × 20 amino acid, 28 WT không score; lựa chọn đồng bộ inspector |
| Ranking | Tab Ranking → lọc position/mutant → sort → Next/Previous | 532 phép thay thế; không có phép WT→WT; shortlist là bộ lọc riêng |
| Peptide đơn | New analysis → Load example hoặc nhập chuỗi → Preview substitutions | Chuẩn hoá hoa/thường và khoảng trắng hai đầu; báo lỗi cụ thể; preview chưa lưu |
| Reference tile | New analysis → tìm COL6A6/A6NMZ7 → chọn tile 28 | 98 cửa sổ; start=(n−1)×23+1; uncovered 2260–2263; gate unknown |
| Batch | Peptide batch → chọn project → Load example → Validate & preview → xác nhận → submit | Ví dụ có 2 chuỗi hợp lệ và 1 chuỗi lỗi; job kết thúc partial; export giữ item lỗi |
| Protein FASTA | Whole protein → chọn project → dán đúng một record → validate | Chỉ cửa sổ đầy đủ 28/step 23; báo đuôi không phủ; giữ context từng tile |
| Job | Batch jobs → mở job → cancel hoặc mở matrix của item | Progress mô phỏng; cancellation giữ item đã xong; không có restart recovery thật |
| Import | Experimental data → Import CSV/TSV → Sample CSV → chọn file + metadata → Validate → acknowledge → Commit | Duplicate/conflict, WT lệch, nonfinite, missing reason, giới hạn file/row và đơn vị được kiểm tra; có SHA-256 |
| Comparison | Dataset đã commit → Compare with analysis | Match exact WT/position/substitution và replicate; n/missing/unmatched; không so xác suất với ΔPSI |
| Snapshot | Save to project → chọn project/tên → save → Run again | Save tạo bản sao; rerun mở preview mới; không ghi đè snapshot cũ |
| Project/history | Projects → Create project / Project settings / mở history | Tạo, đổi tên, empty state; xóa có tóm tắt dependency và xác nhận |
| Export | Export → CSV hoặc JSON | Dữ liệu đủ 532 hàng, không phụ thuộc trang/filter; gắn nhãn fixture, target model, domain và evidence |
| Model/source | Model & evidence / Data & sources | Ranh giới đầu ra, development evidence và tình trạng source hiển thị rõ |
| Trạng thái đặc biệt | Review states ở cuối mỗi trang | Unknown, borderline, unreliable, refusal/override, loading, service unavailable; các trạng thái ClinVar |

Sidebar và tab là điều hướng thật trong prototype; `Ctrl+K`/`Cmd+K` mở tìm kiếm workspace. Trên màn hình nhỏ, ranking là view kết quả mặc định. Theme theo hệ điều hành ở lần mở đầu, đổi bằng nút theme hoặc Review states.

## 3. Định hướng hình thức đã áp dụng

- Sidebar sáng 216 px ở desktop; điều hướng chính, project hiện tại và nguồn/mô hình tách nhóm.
- Nền xám xanh rất nhạt, chữ than, màu nhấn teal; đường phân cách nhẹ và góc bo 6–10 px. Không dùng hero trang trí hoặc số KPI không phục vụ tác vụ.
- Roboto cho UI và Roboto Mono cho amino acid/tọa độ/giá trị. Font được đóng gói local, có giấy phép OFL đi kèm.
- Hệ token ba lớp ở [tokens.css](tokens.css): primitive → semantic → component. Thang dữ liệu tách khỏi màu trạng thái: reversed Viridis cho xác suất và PuOr cho raw score theo BA.
- Ma trận có WT hatch, legend, nhãn số và mô tả đọc bằng bàn phím. Inspector và shortlist không cần mở modal.
- Chỉ modal cho xác nhận/save/search và công cụ review; flow nhập/import vẫn nằm trong trang làm việc.

## 4. Các quyết định BA và giới hạn review

Đọc [SRS](../../srs.md), [UI design](../../ui-design.md), [API](../../api-spec.md), [data design](../../db-design.md), [test plan](../../test-plan.md) và baseline deviations trước khi dựng. [screen-map.json](screen-map.json) liên kết UC và view.

**Quyết định người dùng đã duyệt:** thay lời nhắc cũ của `ui-design.md` §3.1 trong UI mới bằng quy tắc SRS/API: domain đến từ gate R3 có nguồn/estimator; nếu gate chưa có thì unknown; không áp screen PSI ≤ 4 trực tiếp. Không tự sửa BA gốc, không thay ngưỡng hay chọn lại mô hình.

Các ràng buộc giữ nguyên:

1. Warnings/domain/evidence đứng trước score trong DOM; mỗi xác suất có event `P(ΔPSI ≥ 1.0)`.
2. Development OOF không được xem là external validation; training example và dữ liệu demo có nhãn riêng.
3. Whole protein vẫn là nhiều tile; không trung bình hoá context chồng lấp hoặc tạo ranking sinh học xuyên tile.
4. ClinVar phân biệt source unavailable, mapping unavailable, no match và mapping conflict. Không gán chú giải cho custom sequence bằng suy đoán.
5. Nhập dữ liệu không retrain; missing không phải zero; replicate giữ riêng; endpoint khác không được dùng residual/MAE/Spearman ΔPSI chung.
6. Không có tài khoản, chia sẻ công khai, hosting hay suy luận bệnh.

Giới hạn còn lại của **prototype**:

- Chỉ có một reference sequence fixture (A6NMZ7 tile 28). Các tile khác có tọa độ đúng nhưng không giả tạo sequence; phân tích toàn reference protein được giải thích rõ. Protein FASTA do người dùng cung cấp có flow tiling/job đầy đủ trong phiên.
- Chưa nối gate, ClinVar hoặc measured overlay thật. State fixtures minh hoạ các nhánh lỗi; không phải đánh giá domain/annotation thật.
- Prototype cho chọn một replicate khi so sánh; mean/median aggregation của sản phẩm vẫn là refinement UX cần triển khai sau review.
- Export JSON/CSV của analysis và JSON manifest của job hoạt động trong phiên. Chưa thực thi đầy đủ hợp đồng export tổng hợp của backend.
- Không có mô phỏng persistence xuyên reload, import preview expiry, rate limiter, integrity recovery hay cross-browser acceptance của ứng dụng thật.

## 5. Kiểm tra và ảnh

[validation.json](validation.json) lưu kết quả kiểm tra browser của prototype và nêu phạm vi. Script: [scripts/validate_ui.py](scripts/validate_ui.py). Chạy với môi trường đã có Playwright và browser:

Kết quả lần kiểm tra 01/11/2026: **43/43 kiểm tra qua**, 6 view được quét axe không ghi nhận violation, không có JavaScript exception; kiểm tra responsive tại 360/768/1280 px, ma trận 532 + 28 WT và mở file trực tiếp với font offline. Có 15 ảnh render. Đây là kết quả của prototype trên Chromium, không phải nghiệm thu app hoặc xác nhận đầy đủ WCAG.

```bash
python3 scripts/validate_ui.py \
  --url http://127.0.0.1:8891/ \
  --browser /path/to/chromium
```

Nếu axe-core đã có ở frontend của repo, script tự load để kiểm tra một số view sáng/tối. Kết quả tự động không chứng minh hoàn toàn WCAG hoặc trải nghiệm với assistive technology.

Ảnh chính: [result sáng](previews/result-light.png), [result tối](previews/result-dark.png), [lịch sử dự án](previews/project-history.png), [nhập peptide](previews/new-analysis.png), [import validation](previews/import-validation.png), [comparison](previews/comparison.png), [mobile](previews/mobile-ranking.png).

## 6. Nguồn và tài sản

[sources.json](sources.json) ghim hash tài liệu BA, nguồn font và các tham chiếu nghiên cứu. Các ảnh sản phẩm đã khảo sát không được đưa vào tài sản UI. Mark và icon SVG trong prototype do tác giả bản thiết kế dựng trực tiếp; không gọi dịch vụ ảnh ngoài.

Chưa tạo/cập nhật màn hình nào trên Figma. Code sản phẩm và proposal giữ nguyên trong phần việc này. Bản cũ giữ lại với thông báo “BẢN CŨ” để tra lịch sử và tránh nhầm bản review hiện hành.
