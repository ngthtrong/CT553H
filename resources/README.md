# Tài nguyên — một chỗ duy nhất

> Chỉ mục **mọi tài nguyên**: tài liệu tham khảo trong repo, artifact và trang Notion trên mạng, dữ liệu, môi trường và cache cục bộ, dịch vụ ngoài. File này được nạp tự động qua [CLAUDE.md](../CLAUDE.md). Mỗi khi thêm hoặc đổi trạng thái một tài nguyên, cập nhật bảng tương ứng. Không ghi key hay mật khẩu.

## 1. Tài liệu tham khảo trong repo

| Thư mục | Nội dung |
|---|---|
| [Script Việt–Anh cho deck 16/10/2026](../topics/degron-footprint/presentation/deck-2026-10-16/speaker-script-bilingual.md) | 26 slide: lời nói song ngữ, giải thích để tự học, cách đọc hình, hỏi đáp, từ điển và nguồn; có đối soát metric và giới hạn của bản HTML, soạn từ năm phần paste ngày 15/10 |
| [Slide PowerPoint cho 16/10/2026](../topics/degron-footprint/presentation/deck-pptx-2026-10-16/README.md) | `.pptx` 26 slide + 2 phụ lục, animation bấm chuột, ghi chú người nói; ba GIF Commons CC BY-SA (Tekksavvy, Hsp90, Erik A. Rodriguez), tra mẫu *assertion–evidence* / Beamer *metropolis* (chỉ nguyên tắc, không tải mẫu); [nguồn, giấy phép, SHA-256 và các chỗ lệch brief](../topics/degron-footprint/presentation/deck-pptx-2026-10-16/SOURCES.md) |
| [Deck bên ngoài cho 16/10/2026](../topics/degron-footprint/presentation/deck-external-2026-10-16/README.md) | 26 slide + 7 phụ lục, HTML offline / PDF; tham khảo Quarto Clean (MIT), hai GIF Commons có ghi công, SVG tự dựng; [nguồn và giấy phép](../topics/degron-footprint/presentation/deck-external-2026-10-16/SOURCES.md), [manifest SHA-256](../topics/degron-footprint/presentation/deck-external-2026-10-16/assets/asset-manifest.json) |
| [course/CT553H.pdf](course/CT553H.pdf) | Yêu cầu học phần / rubric. Tóm tắt ở [project/course.md](../project/course.md) |
| [papers/ho-quang-thai/](papers/ho-quang-thai/) | PDF bài báo của GVHD (TS. Hồ Quang Thái). Danh mục 14 công trình: [project/advisor-publications/ho-quang-thai.md](../project/advisor-publications/ho-quang-thai.md) |
| [Phân tích trình bày Trọng gửi, 14/10/2026](papers/ho-quang-thai/advisor-presentation-analysis-2026-10-14.txt) | Bản paste giữ nguyên; [hướng dẫn sử dụng khi làm slide/báo cáo](../project/advisor-presentation-guide.md) đã đối chiếu chọn lọc PDF và ghi các điểm cần giới hạn |
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

Dữ liệu nằm trong từng thư mục đề tài: `topics/<ten-de-tai>/data/{raw,interim,processed}/` (đề tài đã đóng: `archive/topics/<ten-de-tai>/data/`), bị `.gitignore` chặn, trừ `data/README.md` ghi nguồn gốc từng file và nhật ký xử lý (ví dụ [degron-footprint/data/README.md](../topics/degron-footprint/data/README.md)). Chuyển vào đây từ thư mục `data/` ở gốc ngày 12/10/2026.

| Thứ | Vị trí | Cách tạo lại |
|---|---|---|
| Môi trường Python | `.venv/` ở thư mục gốc | `python3 -m venv .venv`, rồi `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu`, rồi `.venv/bin/pip install -r requirements.txt` |
| **RCAEval** (`budgeted-microservice-rca`, [D-021](../DECISIONS.md#d-021)) | `archive/topics/budgeted-microservice-rca/data/raw/` — `cases.parquet` (index 735 ca, SHA-256 đã kiểm) + 6 ca mẫu | `.venv/bin/python archive/topics/budgeted-microservice-rca/code/preprocessing/audit_data.py` — Hugging Face `phamquiluan/RCAEval`, revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, MIT. Chưa tải hết 735 ca; xem [README tái lập](../archive/topics/budgeted-microservice-rca/code/preprocessing/README.md) |
| **Degron** (`degron-footprint`) — **~1,9 GB, đã tải đủ 13/10/2026** | `topics/degron-footprint/data/`. `raw/`: **cả 5 file Mendeley** (gồm GPS Peptidome + MLN4924 + SVM 393 MB), `geo-gse240610/` (Table S1 52,9 MB + RAW.tar), `voutsinos-2026/repo/` (50 file @ `9b3eafa6`), `mavedb/` (26 score set), manifest SHA-256 đầy đủ `full-download-manifest.json`, snapshot UniProt, **8 cấu trúc AlphaFold v6** (`alphafold/`, kèm `manifest.txt`); `interim/`: ba ZIP đã giải nén, cụm MMseqs2, **trọng số PAP đã giải nén** (`pap-weights/`); `processed/`: **5 bảng PSI** (`psi-rep1/rep2/wt/sat_a/sat_b.tsv`), bảng audit theo peptide, FASTA protein | [fetch_all.py](../topics/degron-footprint/research/full-data-audit/fetch_all.py) rồi các lệnh trong [full-data-audit §10](../topics/degron-footprint/research/full-data-audit/README.md). Bảng PSI dựng lại bằng `build_psi.py --condition all --validate` (có cổng kiểm). Cấu trúc AlphaFold: **EBI trả 403 nếu không có User-Agent**, dùng `curl -A "Mozilla/5.0"` (lệnh đầy đủ trong [architecture-check](../topics/degron-footprint/research/architecture-check/README.md)). Trọng số PAP: `tar -xzf` từ `voutsinos-2026/repo/models/pap_weights.tgz`. Cụm MMseqs2 trong `interim/` ghi đường dẫn tuyệt đối cũ; nếu cần, chạy lại `prepare_protein_clusters.py`. **Zenodo `16925278` trả 403 từ mạng này**; dùng repo GitHub cùng tác giả |
| Sirtuin (đã đóng) | `archive/topics/sirtuin-substrate/data/raw/` | Script trong [archive/topics/sirtuin-substrate/research/](../archive/topics/sirtuin-substrate/research/README.md) |
| RTK–ATP (đã đóng) | `archive/topics/rtk-atp-applicability/data/raw/`, `processed/` | `python3 archive/topics/rtk-atp-applicability/code/preprocessing/prepare_data.py` — snapshot `b7bd4c2` của [B1607/RTK_RAG](https://github.com/B1607/RTK_RAG) |
| GSE103322 HNSCC scRNA-seq (đã đóng) | `archive/topics/tme-senescence-scrnaseq/data/` — **hiện không có trên máy này** | Lệnh trong [archive/topics/tme-senescence-scrnaseq/code/preprocessing/README.md](../archive/topics/tme-senescence-scrnaseq/code/preprocessing/README.md) |
| **Bộ nhân Larsen 2025** (`degron-footprint`) — **đã tải 15/10/2026** ([D-028](../DECISIONS.md#d-028) mục 6) | `topics/degron-footprint/data/raw/larsen-2025/` — `transfac_tiles.csv.gz` (5,77 MB, **63.258 dòng**, SHA-256 `0c31057d…`) + `LICENSE` | `git clone --depth 1 --branch v1.0` [KULL-Centre/_2025_Larsen_degron_transcriptionfactors](https://github.com/KULL-Centre/_2025_Larsen_degron_transcriptionfactors) (commit `2698ecc6`, **MIT**), copy `annotations/transfac_tiles.csv.gz` + `LICENSE`. Sổ xuất xứ: [SOURCE.md](../topics/degron-footprint/data/raw/larsen-2025/SOURCE.md). Audit khi tải: 59.016 tile / 1.627 gene, độ tin cậy 0,9701, **Pearson(`pap`,`degron_score`) = −0,7899 tái lập mốc 0,79 của tác giả**, rASA SD **0,2334** (49,4% tile > 0,7 — **chỗ duy nhất rASA có phương sai**). ⚠ **Zenodo trả 403 từ mạng này** → dùng GitHub, trích DOI [10.5281/zenodo.20490355](https://doi.org/10.5281/zenodo.20490355). ⚠ Archive ERDA 120,79 GB FASTQ **không có giấy phép** — không dùng. ⚠ Số 63.258 **không khớp con số nào in trong bài**. ⚠ Chờ [C-11a](../DECISIONS.md): email xác nhận MIT phủ cả file dữ liệu |
| **ClinVar** (`degron-footprint`) — **đã tải 15/10/2026** ([D-033](../DECISIONS.md#d-033)) | `topics/degron-footprint/data/raw/clinvar/variant_summary.txt.gz` — 455.785.525 byte, SHA-256 `a5198a11…28218`, `Last-Modified` 12/10/2026 | `curl` từ `ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/`. Sổ xuất xứ: [SOURCE.md](../topics/degron-footprint/data/raw/clinvar/SOURCE.md). ⚠ **Không có số phiên bản, ghi đè mỗi tuần** → muốn tái lập đúng số phải dùng `archive/variant_summary_2026-10.txt.gz`. ⚠ **Không có giấy phép kiểu CC**: chỉ **yêu cầu ghi công** (trích PMID 29165669) và một câu phủ nhận chẩn đoán **phải đi theo đầu ra của ứng dụng** — nguyên văn trong SOURCE.md. ⚠ `ftp.ncbi.nlm.nih.gov` cần thêm vào Allowed domains ở môi trường cloud. Đã dùng: 2.564.486 biến thể missense, khớp toạ độ UniProt **93,0%**, tỉ số chênh gây bệnh/lành tính trong degron **2,148** ([báo cáo](../topics/degron-footprint/research/variant-coverage-2026-10-15/README.md)) |
| **Degformer** (tiền lệ/baseline, `degron-footprint`) — **chưa tải** | sẽ về thư mục riêng, **biệt lập** | `git clone` [Alpine2048/Degformer](https://github.com/Alpine2048/Degformer) (Apache-2.0). Repo ship cả **3 checkpoint** (~2,2 MB mỗi cái) và **`training_data.csv` 19,9 MB / 569.270 dòng**. ⚠ **Checkpoint là pickle** (`torch.load(..., weights_only=False)` kèm một `StandardScaler`) ⇒ nạp nó **thực thi mã tuỳ ý**: để trong thư mục riêng và trống, script của mình để chỗ khác, chạy `python3 -I`. ⚠ **Tập blind vắng mặt khỏi repo** nên con số headline của nó không tái lập được. Cần [C-11](../DECISIONS.md) |
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
