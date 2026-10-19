# Kiểm tra báo cáo thực nghiệm — 18/10/2026

## Phạm vi và kết quả

**Đạt đối với phần báo cáo mới.** Kiểm đọc nguồn và tổng hợp; không tái huấn luyện mô hình hay chạy lại toàn bộ nghiên cứu. Không kiểm truy cập lại các URL bên ngoài trong lượt này.

| Kiểm tra | Kết quả | Phạm vi / giới hạn |
|---|---|---|
| Cấu trúc hồ sơ | PASS | 41 mã liên tục TN-01…TN-41; mỗi mục có ngày/trạng thái, lý do, dữ liệu, cách làm, kết quả, giới hạn và bằng chứng |
| Liên kết báo cáo | PASS | 183 liên kết nội bộ trong README báo cáo tới file có thật; chỉ mục TN trỏ đúng anchor |
| Liên kết mới từ README/log đề tài | PASS | Đường dẫn báo cáo và biên bản kiểm đều tồn tại; không sửa các link lịch sử khác |
| Đối chiếu headline JSON | PASS | Ridge0,8082; Degformer0,9248; ba ứng viên E2 không đạt tiêu chí; 38 peptide PSI≤2,5; PAP map Spearman0,4130 và mức ô0,3553 |
| Manifest nguồn | PASS | 89 file được tham chiếu, SHA-256 khớp tại lượt kiểm; không chứa hash tự tham chiếu của manifest/báo cáo |
| Render Markdown | PASS | markdown-it render đủ41 hồ sơ và5 bảng; đã xem ảnh đầu báo cáo, TN-23/24 và TN-27 |
| Preview hẹp | PASS cho bản xem tạm | 390×844, không tràn ngang trang sau khi cho bảng cuộn nội bộ; không phải cam kết cho mọi Markdown viewer |
| Whitespace phần sửa | PASS | `git diff --check` trên thư mục báo cáo và README/log đề tài |
| Kiểm link toàn repo | CHƯA ĐẠT ngoài phạm vi bổ sung | 56 lượt link hỏng tại lúc kiểm; không có link thuộc README báo cáo mới bị báo lỗi |

**Link toàn repo cần phân biệt:** `topics/degron-footprint/research/g2-extension-2026-10-18/README.md` trỏ tới `e3-degformer-arch.json` chưa có khi E3 đang chạy. Lỗi đã có ở phần bài giảng: `lectures/14-xai-basics.html` trỏ `15-reading-bioinfo-papers.html`. Các lỗi còn lại gồm liên kết tài liệu/slide lịch sử; không tự sửa trong yêu cầu lưu báo cáo này.

## Mốc nguồn

Mốc chốt chính xác ở [evidence-manifest.json](evidence-manifest.json): `2026-10-18T14:30:26+00:00`, tương ứng **22:30:26 ngày18/10 theo Asia/Taipei**. E1/E2 có JSON; README nhánh mở rộng ghi E3 còn chạy; chưa có JSON cuối E3. Báo cáo không tự cập nhật khi tiến trình khác sinh thêm kết quả.

Manifest ghim phiên bản các file bằng hash, không sao chép toàn bộ nội dung nguồn. Nếu một nguồn tiếp tục thay đổi, kiểm hash sẽ báo khác snapshot; điều này không tự chứng minh báo cáo sai, nhưng cần đọc thay đổi trước khi cập nhật bằng chứng.

## Có thể kiểm lại

Từ gốc repo:

```bash
python3 tools/check_links.py
git diff --check -- topics/degron-footprint/research/experiment-report-2026-10-18 topics/degron-footprint/README.md topics/degron-footprint/log.md
```

Kiểm SHA-256 các nguồn đã ghim:

```python
from pathlib import Path
import hashlib
import json

root = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / 'DECISIONS.md').exists())
manifest_path = root / 'topics/degron-footprint/research/experiment-report-2026-10-18/evidence-manifest.json'
manifest = json.loads(manifest_path.read_text())
changed = [row['path'] for row in manifest['sources']
           if hashlib.sha256((root / row['path']).read_bytes()).hexdigest() != row['sha256']]
print({'sources': len(manifest['sources']), 'changed_since_snapshot': changed})
```

Lượt tạo báo cáo không sửa nguồn thí nghiệm, dữ liệu, slide hoặc DECISIONS; chỉ thêm ba file báo cáo/manifest/validation và liên kết ở README/log đề tài. Các thay đổi có sẵn trong workspace được giữ nguyên.
