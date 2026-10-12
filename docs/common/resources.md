# Tài nguyên nằm ngoài repo

> Danh sách những thứ **không nằm trong git** nhưng cần dùng lại ở các phiên làm việc sau: artifact trên claude.ai, cache và môi trường cục bộ. File này được nạp tự động qua [CLAUDE.md](../../CLAUDE.md). Mỗi khi tạo mới hoặc đổi trạng thái một tài nguyên, cập nhật bảng tương ứng.

## 1. Artifact trên claude.ai

| Tên | URL | Loại | Mã nguồn trong repo | Cập nhật gần nhất | Chia sẻ |
|---|---|---|---|---|---|
| **Slide buổi gặp GVHD lần 1 — đề tài RTK–ATP** | https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT | Slides (13 trang) | [meeting/session-01-slides/](../meeting/session-01-slides/) | 02/10/2026, bản 8: thêm 2 slide `landscape` (tính cấp thiết + 7 công trình 2023–2026) và `evidence` (bằng chứng A kho RAG/CD-HIT, bảng dropout-vs-RAG), đổi `scope` sang ví dụ thật P34891, `metrics` thêm mốc accuracy 99,04%, đánh số lại 15 trang. Trước đó bản 4: viết lại hoàn toàn cho đề tài đã chốt (phạm vi mức residue, bốn loại rò rỉ, giao thức 9 bước, 2 RQ, chỉ số, sản phẩm, 3 đóng góp, kế hoạch 14 tuần, 6 câu hỏi GVHD). Bỏ 5 slide cũ: framing, gap, proposal, backup, research-questions | Riêng tư. Muốn gửi GVHD thì chia sẻ qua menu Share |
| **Slide diễn giải đề tài RTK–ATP (6 phần)** | https://claude.ai/artifact/A7kgUgsr28RBUSd59knh1q | Slides (15 trang) | [rtk-atp-applicability/04-proposal/explainer-slides/](../topics/rtk-atp-applicability/04-proposal/explainer-slides/) | 02/10/2026, bản 3 (tạo mới): deck chỉ diễn giải theo bố cục mô tả bài toán → tính cấp thiết + nghiên cứu đã có + vì sao cần làm → input → output → dữ liệu → cách đánh giá. Có 3 hình minh họa (biểu đồ cột điểm ATP theo residue, sơ đồ RTK/màng/túi ATP bằng SVG, đường coverage–risk). Bản 4 thêm phần 7: trang `risks` (4 rủi ro kèm dấu hiệu nhận biết và cổng dừng, 2 giới hạn không khắc phục được, rủi ro định vị) và trang `questions` (7 câu xin ý kiến GVHD). Dùng lại bảng màu và font của deck buổi gặp | Riêng tư |
| ~~Báo cáo ứng viên đề tài degron~~ | https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc | Trang HTML (12 mục) | [deep-research/reports/degron-topic-report/](deep-research/reports/degron-topic-report/) | **LẠC HẬU từ 11/10/2026.** Đây là bản 1; bản đang dùng là **bản 3 nằm trong repo**, không publish. Từ 11/10/2026 sinh viên yêu cầu **tạo HTML trực tiếp trên hệ thống, không dùng artifact** — xem mục 1.1 bên dưới | Riêng tư |
| Slide đề tài chi tiêu (lưu trữ) | https://claude.ai/artifact/YRqpuZNbzNdsBQFRnx7bCn | Slides (8 trang) | [personal-expense-management/01-idea/slides-draft/](../topics/personal-expense-management/01-idea/slides-draft/) | 29/09/2026, bản 4. **Không dùng nữa**: soạn cho đề tài chi tiêu, đã tạm dừng. Mã nguồn chuyển về thư mục đề tài ngày 01/10/2026 | Riêng tư |

Artifact đang ở chế độ riêng tư: chỉ chủ tài khoản mở được link. Repo GitHub cũng đã chuyển sang private từ 01/10/2026.

### 1.1 Quy ước mới từ 11/10/2026: HTML nằm trong repo, không dùng artifact

Sinh viên yêu cầu **tạo file HTML trực tiếp trên hệ thống** thay vì publish artifact. Hai trang đang dùng cho đề tài đã chốt, mở bằng `file://` (không cần server):

| Trang | Đường dẫn | Nội dung |
|---|---|---|
| **Trình bày đề tài** | [topics/degron-e3-specificity/01-idea/presentation.html](../topics/degron-e3-specificity/01-idea/presentation.html) | 7 mục theo bố cục sinh viên yêu cầu: giới thiệu → lược sử → giải pháp → dữ liệu → đóng góp theo 5 tiêu chí → hướng đi tiếp → tham khảo. **Có 5 sơ đồ SVG tự vẽ** |
| **Báo cáo kiểm chứng chi tiết** | [deep-research/reports/degron-topic-report/index.html](deep-research/reports/degron-topic-report/index.html) | Bản 3, 13 mục: kết quả kiểm chứng 10 điểm, kiến trúc CMIL-E3, audit dữ liệu, rủi ro, tham khảo |

Cả hai trang nạp font từ Google Fonts nên **cần mạng để hiển thị đúng font**; không có mạng thì vẫn đọc được bằng font hệ thống. Không có JavaScript, không phụ thuộc thư viện ngoài.

### Cách sửa một artifact ở phiên mới
1. Lấy URL từ bảng trên.
2. Dùng Artifact `read` để đọc **bản đang có trên claude.ai**, vì có thể đã được sửa trực tiếp trên trang. Nếu khác với file trong repo, chép bản trên claude.ai đè vào repo trước.
3. Sửa file trong thư mục mã nguồn ở repo.
4. Publish với `url` là URL trên và `root` là thư mục mã nguồn (ví dụ `docs/meeting/session-01-slides`). Chỉ gửi những file đã đổi.
5. Cập nhật cột "Cập nhật gần nhất" ở bảng trên.

Artifact mới: đặt mã nguồn ngay trong repo (không để trong thư mục tạm của phiên), publish từ đó, rồi thêm một dòng vào bảng.

## 2. Môi trường và cache cục bộ (không lên git)

**Cập nhật 12/10/2026 — dữ liệu degron đã tải lại trên máy này:** `data/degron-e3-specificity/raw/` có ZIP quét 27.939.862 B và ZIP bão hòa 5.224.902 B, manifest SHA-256; snapshot UniProt hiện tại và response bổ sung cũng được cache. `interim/` có CSV quét và cụm protein MMseqs2; `processed/` có bảng audit theo peptide và FASTA protein. Tái tạo bằng [fetch_scanning.py](deep-research/research_notes/degron-e3-labels/fetch_scanning.py) và các lệnh trong [báo cáo audit](deep-research/reports/degron-composition-context-audit.md). Đây là dữ liệu audit, không phải trọng số hay kết quả huấn luyện. Các trạng thái máy/cloud cũ bên dưới là lịch sử, không xác nhận trạng thái tài nguyên hiện tại.

| Thứ | Vị trí | Cách tạo lại |
|---|---|---|
| Môi trường Python | `.venv/` ở thư mục gốc | `python3 -m venv .venv`, rồi `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu`, rồi `.venv/bin/pip install -r ml/requirements.txt` |
| **Dữ liệu RCAEval (`budgeted-microservice-rca`)** | `data/budgeted-microservice-rca/raw/` — `cases.parquet` (index 735 ca, SHA-256 đã kiểm) + 6 thư mục ca mẫu (`re2ob_checkoutservice_cpu_1`, v.v.) | `.venv/bin/python ml/budgeted-microservice-rca/preprocessing/audit_data.py` — tải từ Hugging Face `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, MIT. Chỉ audit, chưa tải hết 735 ca; xem [README tái lập](../../ml/budgeted-microservice-rca/preprocessing/README.md) |
| **Dữ liệu RTK–ATP (gốc + chuẩn hóa)** | `data/rtk-atp-applicability/raw/` và `processed/` | `python3 ml/rtk-atp-applicability/preprocessing/prepare_data.py` — tải snapshot `b7bd4c2` của [B1607/RTK_RAG](https://github.com/B1607/RTK_RAG), kiểm SHA-256, giải nén, đếm và xuất FASTA/JSONL/CSV. Chạy lại được từ mạng, hoặc dùng ZIP có sẵn qua `--archive` |
| **Trọng số ProtT5** | chưa tải | Sẽ về `~/.cache/huggingface/` khi chạy bước trích embedding (tuần 3–4). Chưa đo thời gian GPU thực tế |
| Mô hình embedding | `~/.cache/huggingface/` (bge-m3 khoảng 2,2 GB; multilingual-e5-small, e5-base) | Tự tải khi chạy script thí nghiệm lần đầu |
| Cache embedding ghi chú | `data/personal-expense-management/interim/emb_bge-m3_titles.npz` | Tự sinh khi chạy `ml/personal-expense-management/experiments/rq2-baseline-recall/run.py`; xóa khi đổi mô tả danh mục |
| Dữ liệu gốc và danh sách tên cần ẩn danh | `data/personal-expense-management/raw/` | Chỉ có trên máy của người làm đề tài; không tạo lại được |
| Dữ liệu đã làm sạch | `data/personal-expense-management/processed/` | `python ml/personal-expense-management/preprocessing/clean_data.py` |
| LaTeX | XeLaTeX, polyglossia, font TeX Gyre Termes (TeX Live 2023) | Biên dịch đề cương: xem dòng đầu của `docs/topics/personal-expense-management/04-proposal/proposal.tex` |

## 3. Dịch vụ bên ngoài

| Dịch vụ | Trạng thái |
|---|---|
| API LLM để sinh dữ liệu tổng hợp | Chưa chọn, chưa có key |
| Ollama / LLM chạy cục bộ | Chưa cài; máy không có GPU |
| Colab / Kaggle | Chưa dùng; chỉ đưa bản `*_anon.csv` lên |
| **Mạng của môi trường cloud** | **Chặn gần hết host dữ liệu** (07/10/2026, đã thử và ghi mã trả về): `ftp.ncbi.nlm.nih.gov` (GEO), `zenodo.org`, `cellxgene`, `huggingface.co`, `figshare`, `cells.ucsc.edu`, `ha-dkfz.github.io` đều **403 ở bước CONNECT**. Đi được: `raw.githubusercontent.com` và PyPI. Chi tiết và hệ quả: [ml/tme-senescence-scrnaseq/preprocessing/README.md](../../ml/tme-senescence-scrnaseq/preprocessing/README.md) |
| **Mạng của môi trường cloud** | Từ 07/10/2026 (khuya), sau khi sinh viên thêm Allowed domains: `ftp.ncbi.nlm.nih.gov` và `www.ncbi.nlm.nih.gov` trả 200. Trước đó mọi host dữ liệu (GEO, `zenodo.org`, `cellxgene`, `huggingface.co`, `figshare`, `cells.ucsc.edu`) đều 403 ở bước CONNECT. Host khác ngoài NCBI chưa kiểm lại. Thread đang chạy không nhận cấu hình mạng mới, phải mở thread mới |
| **Dữ liệu GSE103322 (HNSCC scRNA-seq)** | `data/tme-senescence-scrnaseq/raw/` (txt.gz 90 MB) và `processed/GSE103322.h5ad`. Cách tạo lại: lệnh trong [ml/tme-senescence-scrnaseq/preprocessing/README.md](../../ml/tme-senescence-scrnaseq/preprocessing/README.md), mục "Chạy lại" |
| Notion (kết nối từ 29/09/2026; trong Claude Code cần bật server `plugin:design:notion`) | Trang gốc **Ý tưởng luận văn**: https://app.notion.com/p/3ec486d98ebc80fd9ecceaf626d5a3e6 — chứa 4 trang con, xem bảng đối chiếu bên dưới. Trang đang dùng là **Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng**. Sửa nội dung trên Notion thì file trong repo không tự cập nhật, và ngược lại |

### Bản nội dung chờ nhập Notion

### Trang Notion và bản nguồn tương ứng trong repo

| Trang Notion | Bản nguồn trong repo | Trạng thái |
|---|---|---|
| [Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880) | [topic-proposal.md](../topics/rtk-atp-applicability/04-proposal/topic-proposal.md) | **Đã tạo 02/10/2026. Bản đang dùng.** ⚠️ **Notion đang đi trước repo** từ 02/10/2026: trang Notion đã thêm mục ★ (tính cấp thiết, 7 công trình 2023–2026, bằng chứng A/B/C), ví dụ thật P34891, câu hỏi GVHD thứ 7 và tài liệu [10]–[16]; `topic-proposal.md` **chưa có** các phần này. 14 mục: tên đề tài, phạm vi, mô hình nền, bốn loại rò rỉ, giao thức, 2 RQ, chỉ số, dữ liệu, sản phẩm, đóng góp, kế hoạch, câu hỏi GVHD, bài báo, điều chưa có |
| [Đề xuất chốt: vị trí gắn ATP + dự phòng efflux](https://app.notion.com/p/3ec486d98ebc813bb56eface997a23a9) | [bioinformatics-proposal-notion.md](../meeting/bioinformatics-proposal-notion.md) | Đã nhập 01/10/2026. **Đã bị thay thế** — giữ làm lịch sử bước có dự phòng efflux |
| [bioinformatics-topic-ideas-notion](https://app.notion.com/p/3ec486d98ebc80a79ce1f6765bbf93ed) | [bioinformatics-topic-ideas-notion.md](../meeting/bioinformatics-topic-ideas-notion.md) | Đã nhập trước đó. **Đã bị thay thế** — giữ làm lịch sử bước so sánh ba hướng; hướng IL-6 bị loại 01/10/2026 |
| [Đề tài quản lý chi tiêu cá nhân](https://app.notion.com/p/3ea486d98ebc8101ad92c0786e2797fc) | — | Lưu làm lịch sử, đề tài đã tạm dừng |
