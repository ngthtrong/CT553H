# Tài nguyên — một chỗ duy nhất

> Chỉ mục **mọi tài nguyên**: tài liệu tham khảo trong repo, artifact và trang Notion trên mạng, dữ liệu, môi trường và cache cục bộ, dịch vụ ngoài. File này được nạp tự động qua [CLAUDE.md](../CLAUDE.md). Mỗi khi thêm hoặc đổi trạng thái một tài nguyên, cập nhật bảng tương ứng. Không ghi key hay mật khẩu.

## 1. Tài liệu tham khảo trong repo

| Thư mục | Nội dung |
|---|---|
| [course/CT553H.pdf](course/CT553H.pdf) | Yêu cầu học phần / rubric. Tóm tắt ở [project/course.md](../project/course.md) |
| [papers/ho-quang-thai/](papers/ho-quang-thai/) | PDF bài báo của GVHD (TS. Hồ Quang Thái). Danh mục 14 công trình: [project/advisor-publications/ho-quang-thai.md](../project/advisor-publications/ho-quang-thai.md) |
| [papers/yu-yen-ou/](papers/yu-yen-ou/) | PDF bài báo của Prof. YY Ou (đồng tác giả, không phải GVHD). Danh mục: [project/advisor-publications/yu-yen-ou.md](../project/advisor-publications/yu-yen-ou.md) |
| [reference-theses/](reference-theses/thesis-comparison.md) | Hai luận văn tham khảo cùng GVHD + [bản phân tích](reference-theses/thesis-comparison.md) |
| [../lectures/](../lectures/index.html) | Bài giảng tự học (để riêng, không nằm trong `resources/`) |

Repo private ([D-004](../DECISIONS.md#d-004)) nên được chứa PDF. Nếu đổi sang public thì phải gỡ `papers/`, `reference-theses/` và các phân tích về bài của nhóm GVHD, kể cả khỏi lịch sử git.

## 2. Artifact trên claude.ai — **tất cả là lịch sử**

Từ 11/10/2026, trang HTML được tạo trực tiếp trong repo, không publish artifact nữa ([D-013](../DECISIONS.md#d-013)). Các artifact dưới đây vẫn ở chế độ riêng tư.

| Tên | URL | Mã nguồn trong repo | Ghi chú |
|---|---|---|---|
| Slide buổi gặp GVHD lần 1 — RTK–ATP | https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT | [project/meetings/2026-10-02-session-01/slides/](../project/meetings/2026-10-02-session-01/slides/) | Bản 8, 02/10/2026, 15 trang |
| Slide diễn giải đề tài RTK–ATP | https://claude.ai/artifact/A7kgUgsr28RBUSd59knh1q | [archive/topics/rtk-atp-applicability/04-proposal/explainer-slides/](../archive/topics/rtk-atp-applicability/04-proposal/explainer-slides/) | Bản 4, 02/10/2026; đề tài đã đóng |
| Báo cáo ứng viên degron (bản 1) | https://claude.ai/artifact/XAXzVcA6ot1eVVk4927suc | — | **Lạc hậu.** Bản 3 nằm trong repo: [topic-report/index.html](../topics/degron-footprint/research/topic-report/index.html) |
| Slide đề tài chi tiêu | https://claude.ai/artifact/YRqpuZNbzNdsBQFRnx7bCn | đã gỡ khỏi repo | Đề tài đã đóng ([D-019](../DECISIONS.md#d-019)) |

Nếu cần sửa lại một artifact: `read` bản trên claude.ai trước (có thể đã được sửa trực tiếp), đồng bộ vào thư mục mã nguồn trong repo, rồi publish với `url` cũ và `root` là thư mục đó.

## 3. Notion — **tất cả là lịch sử**

Trang gốc **Ý tưởng luận văn**: https://app.notion.com/p/3ec486d98ebc80fd9ecceaf626d5a3e6. Trong Claude Code cần bật server Notion. Notion và repo không tự đồng bộ với nhau.

| Trang Notion | Bản nguồn trong repo | Trạng thái |
|---|---|---|
| [Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK…](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880) | [topic-proposal.md](../archive/topics/rtk-atp-applicability/04-proposal/topic-proposal.md) | **Lỗi thời** — RTK–ATP đã đóng ([D-006](../DECISIONS.md#d-006)). Tiêu đề "Đề tài chốt" trên Notion **không còn đúng**; nên sửa trên Notion. Bản Notion có phần ★ (tính cấp thiết, 7 công trình 2023–2026) mà repo không có |
| [Đề xuất chốt: vị trí gắn ATP + dự phòng efflux](https://app.notion.com/p/3ec486d98ebc813bb56eface997a23a9) | [bioinformatics-proposal-notion.md](../archive/meetings/bioinformatics-proposal-notion.md) | Lịch sử |
| [bioinformatics-topic-ideas-notion](https://app.notion.com/p/3ec486d98ebc80a79ce1f6765bbf93ed) | [bioinformatics-topic-ideas-notion.md](../archive/meetings/bioinformatics-topic-ideas-notion.md) | Lịch sử |
| [Đề tài quản lý chi tiêu cá nhân](https://app.notion.com/p/3ea486d98ebc8101ad92c0786e2797fc) | — | Lịch sử, đề tài đã đóng |

## 4. Dữ liệu, môi trường và cache cục bộ (không lên git)

Dữ liệu nằm trong từng thư mục đề tài: `topics/<ten-de-tai>/data/{raw,interim,processed}/` (đề tài đã đóng: `archive/topics/<ten-de-tai>/data/`), bị `.gitignore` chặn. Chuyển vào đây từ thư mục `data/` ở gốc ngày 12/10/2026.

| Thứ | Vị trí | Cách tạo lại |
|---|---|---|
| Môi trường Python | `.venv/` ở thư mục gốc | `python3 -m venv .venv`, rồi `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu`, rồi `.venv/bin/pip install -r requirements.txt` |
| **RCAEval** (`budgeted-microservice-rca`, [D-021](../DECISIONS.md#d-021)) | `archive/topics/budgeted-microservice-rca/data/raw/` — `cases.parquet` (index 735 ca, SHA-256 đã kiểm) + 6 ca mẫu | `.venv/bin/python archive/topics/budgeted-microservice-rca/code/preprocessing/audit_data.py` — Hugging Face `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, MIT. Chưa tải hết 735 ca; xem [README tái lập](../archive/topics/budgeted-microservice-rca/code/preprocessing/README.md) |
| **Degron** (`degron-footprint`) | `topics/degron-footprint/data/` (đổi tên từ `data/degron-e3-specificity/` ngày 12/10/2026). `raw/`: ZIP quét 27.939.862 B, ZIP bão hòa 5.224.902 B, manifest SHA-256, snapshot UniProt; `interim/`: CSV quét, cụm MMseqs2; `processed/`: bảng audit theo peptide, FASTA protein | [fetch_scanning.py](../topics/degron-footprint/research/e3-labels-audit/fetch_scanning.py) và các lệnh trong [composition-context-audit.md](../topics/degron-footprint/research/composition-context-audit.md). Cụm MMseqs2 trong `interim/` ghi đường dẫn tuyệt đối cũ; nếu cần, chạy lại `prepare_protein_clusters.py` |
| Sirtuin (đã đóng) | `archive/topics/sirtuin-substrate/data/raw/` | Script trong [archive/topics/sirtuin-substrate/research/](../archive/topics/sirtuin-substrate/research/README.md) |
| RTK–ATP (đã đóng) | `archive/topics/rtk-atp-applicability/data/raw/`, `processed/` | `python3 archive/topics/rtk-atp-applicability/code/preprocessing/prepare_data.py` — snapshot `b7bd4c2` của [B1607/RTK_RAG](https://github.com/B1607/RTK_RAG) |
| GSE103322 HNSCC scRNA-seq (đã đóng) | `archive/topics/tme-senescence-scrnaseq/data/` — **hiện không có trên máy này** | Lệnh trong [archive/topics/tme-senescence-scrnaseq/code/preprocessing/README.md](../archive/topics/tme-senescence-scrnaseq/code/preprocessing/README.md) |
| Trọng số ProtT5 / PLM | chưa tải | Sẽ về `~/.cache/huggingface/` khi cần |
| Mô hình embedding văn bản | `~/.cache/huggingface/` (bge-m3 ~2,2 GB; multilingual-e5-small, e5-base) | Dùng cho đề tài chi tiêu cũ; có thể xoá để lấy chỗ |
| LaTeX | XeLaTeX, polyglossia, TeX Gyre Termes (TeX Live 2023) | Dùng khi viết `topics/<ten-de-tai>/proposal/` |

## 5. Dịch vụ bên ngoài

| Dịch vụ | Trạng thái |
|---|---|
| API LLM | Chưa chọn, chưa có key |
| Ollama / LLM cục bộ | Chưa cài; máy không có GPU |
| Colab / Kaggle | Chưa dùng |
| GPU | Ngày 10/10/2026 Trọng cho biết có GPU ổn định hơn Colab/Kaggle miễn phí; chưa ghi cụ thể |
| Mạng của môi trường **cloud** (Claude Code web) | 07/10/2026: hầu hết host dữ liệu (`zenodo.org`, `huggingface.co`, `figshare`, `cellxgene`, `cells.ucsc.edu`) bị **403 ở bước CONNECT**; đi được `raw.githubusercontent.com`, PyPI, và sau khi thêm Allowed domains thì có `ftp.ncbi.nlm.nih.gov`, `www.ncbi.nlm.nih.gov`. Thread đang chạy không nhận cấu hình mạng mới. Máy cục bộ (WSL) không bị giới hạn này |
