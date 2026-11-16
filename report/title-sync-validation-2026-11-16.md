# Đổi tên đề tài tiếng Anh và chuyển nguồn tên tiếng Việt — 16/11/2026

Tác giả chọn phương án thu hẹp phạm vi tên ngày 16/11/2026: thay `Degron Assays`
bằng `Degron Reporter Assays`, **không** thêm `Local` vào phần công cụ. Lý do:
nhãn huấn luyện/đánh giá là ΔPSI của peptide reporter 28 AA trong assay GPS,
không phải protein tự nhiên; tên cũ dễ bị đọc thành claim rộng hơn bằng chứng.

- **Tiếng Anh (mới):** Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Reporter Assays and Development of an Analysis Tool
- **Tiếng Anh (cũ, 07–08/11):** Sequence-Based Prediction of Single-Residue Mutation Effects on PSI in Degron Assays and Development of an Analysis Tool
- **Tiếng Việt:** Dự đoán ảnh hưởng của đột biến amino acid đơn lên chỉ số PSI trong nghiên cứu degron và xây dựng công cụ phân tích — **giữ nguyên từng ký tự** bản đã đăng ký.

## Nguồn tên

`proposal/` đã được tác giả xoá khỏi working tree (12 tệp, chưa commit; bản cuối
còn trong lịch sử git tại `788851c`). Tên tiếng Việt trước đây đọc từ
`proposal/proposal.md` (`subtitle`), nên slide không còn dựng được.

Từ lượt này, **cả hai tên nằm trong `report/config/metadata.tex`**:
`\ThesisTitle` (tiếng Anh, được typeset) và `\ThesisTitleVI` (tiếng Việt, chỉ là
metadata, không được typeset trong template). `presentation/research-report/manage.py`
đọc tên tiếng Việt từ `\ThesisTitleVI` thay cho `proposal/proposal.md`.

**Chưa thống nhất:** tên tiếng Việt chưa được sửa theo tên tiếng Anh mới. Nếu
muốn khớp nghĩa thì cụm `trong nghiên cứu degron` nên thành `trong assay reporter
degron`. Việc này cần quyết định của tác giả/GVHD vì đây là tên đã đăng ký; lượt
này giữ nguyên bản đăng ký.

## Kết quả kiểm [ĐO 16/11/2026]

| Kiểm | Lệnh | Kết quả |
| --- | --- | --- |
| Dựng luận văn hai bản | `make -C report all` | PASS, references resolved |
| Template/PDF/A4/phông | `make -C report check` → `check_template.py` | PASS — 121 trang một mặt, 121 trang hai mặt, smoke 9 trang |
| Danh mục/nhãn/tham chiếu float | `check_float_references.py` | PASS — 12 hình, 58 bảng, khớp ở cả hai bản |
| Đọc tên từ nguồn mới | `manage.py project_titles()` | PASS — trả đúng cặp tên EN/VI |
| Kiểm slide | `manage.py check` | **FAIL có chủ đích** (xem dưới) |

Số trang không đổi (121/121) nên bố cục không bị xô; đã xem lại bìa ngoài ở cỡ
đọc được: tên mới ngắt thành ba dòng cân đối, không tràn khung, không chạm khối
thông tin sinh viên. Không sửa nội dung, số liệu, hình, bảng hay giới hạn bằng chứng.

### Trạng thái slide sau lượt này

`manage.py check` **không còn lỗi `FileNotFoundError`** như trước 16/11, nhưng
vẫn báo hai mục chưa đạt vì deck chưa được dựng lại:

- `input_hashes` lệch ở `manage.py`, `report/config/metadata.tex` và
  `proposal/proposal.md` (đường dẫn cũ ghi trong build manifest).
- `language_validation_passed: false` — bìa deck vẫn mang tên tiếng Anh cũ.
- `text_layout_passed: true`, `numerical_evidence_passed: true` (16 kiểm) — không đổi.

Deck **chưa** được dựng lại trong lượt này vì môi trường hiện không còn
LibreOffice (`/tmp/isds-lo/root` không tồn tại) nên không xuất được PDF khớp với
PPTX; dựng PPTX mà để PDF cũ sẽ tạo ra hai bản lệch tên. Việc đồng bộ tên trên
deck được gộp vào lượt dựng lại deck bảo vệ, khi cài lại LibreOffice.

## Tệp đã sửa

| Tệp | SHA-256 sau sửa |
| --- | --- |
| `report/config/metadata.tex` | `a881e9171a9b50a5404597a78b7657e6e25b5f597ac7df1fd10213761f144547` |
| `presentation/research-report/manage.py` | `04f86c4e0806de27390f551aa7b56bb9381ac81cb7830c0317a3209c2154535d` |
| `report/build/content/content.pdf` | `d33b3be7e4587293031059a87889c0060eb52b5f3dd5ec9b2e22e20aac560be5` |
| `report/build/content-twoside/content.pdf` | `ec2c66c8442288cc2be59714ef7cbd0a2d147c155b84dbba3bdaea325f706499` |

Ngoài ra: `README.md` và `report/README.md` bỏ liên kết tới `proposal/` đã xoá và
ghi nguồn tên mới. Không chạm `proposal/` (không khôi phục, không xoá thêm).

## Phạm vi và giới hạn

Lượt này chỉ đổi tên và nguồn tên. Không chạy huấn luyện, suy luận, bootstrap
hay campaign; không đọc/sửa `state.json`, checkpoint, manifest campaign; không
đổi model phục vụ; không đóng G2/G3; không commit/push. Biên bản
[08/11](title-sync-validation-2026-11-08.md) giữ nguyên. Dựng được PDF không
đồng nghĩa nghiệm thu nghiên cứu.
