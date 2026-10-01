# Tài nguyên nằm ngoài repo

> Danh sách những thứ **không nằm trong git** nhưng cần dùng lại ở các phiên làm việc sau: artifact trên claude.ai, cache và môi trường cục bộ. File này được nạp tự động qua [CLAUDE.md](../../CLAUDE.md). Mỗi khi tạo mới hoặc đổi trạng thái một tài nguyên, cập nhật bảng tương ứng.

## 1. Artifact trên claude.ai

| Tên | URL | Loại | Mã nguồn trong repo | Cập nhật gần nhất | Chia sẻ |
|---|---|---|---|---|---|
| **Slide buổi gặp GVHD lần 1 — tin sinh** | https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT | Slides (9 trang) | [meeting/session-01-slides/](../meeting/session-01-slides/) | 01/10/2026, bản 3: deck đầy đủ cho đề xuất ATP + dự phòng efflux | Riêng tư. Muốn gửi GVHD thì chia sẻ qua menu Share |
| Slide đề tài chi tiêu (lưu trữ) | https://claude.ai/artifact/YRqpuZNbzNdsBQFRnx7bCn | Slides (8 trang) | [personal-expense-management/01-idea/slides-draft/](../topics/personal-expense-management/01-idea/slides-draft/) | 29/09/2026, bản 4. **Không dùng nữa**: soạn cho đề tài chi tiêu, đã tạm dừng. Mã nguồn chuyển về thư mục đề tài ngày 01/10/2026 | Riêng tư |

Artifact đang ở chế độ riêng tư: chỉ chủ tài khoản mở được link. Repo GitHub cũng đã chuyển sang private từ 01/10/2026.

### Cách sửa một artifact ở phiên mới
1. Lấy URL từ bảng trên.
2. Dùng Artifact `read` để đọc **bản đang có trên claude.ai**, vì có thể đã được sửa trực tiếp trên trang. Nếu khác với file trong repo, chép bản trên claude.ai đè vào repo trước.
3. Sửa file trong thư mục mã nguồn ở repo.
4. Publish với `url` là URL trên và `root` là thư mục mã nguồn (ví dụ `docs/meeting/session-01-slides`). Chỉ gửi những file đã đổi.
5. Cập nhật cột "Cập nhật gần nhất" ở bảng trên.

Artifact mới: đặt mã nguồn ngay trong repo (không để trong thư mục tạm của phiên), publish từ đó, rồi thêm một dòng vào bảng.

## 2. Môi trường và cache cục bộ (không lên git)

| Thứ | Vị trí | Cách tạo lại |
|---|---|---|
| Môi trường Python | `.venv/` ở thư mục gốc | `python3 -m venv .venv`, rồi `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu`, rồi `.venv/bin/pip install -r ml/requirements.txt` |
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
| Notion (kết nối từ 29/09/2026; trong Claude Code cần bật server `plugin:design:notion`) | Trang gốc **Ý tưởng luận văn**: https://app.notion.com/p/3ec486d98ebc80fd9ecceaf626d5a3e6 — chứa 3 trang con: đề tài chi tiêu (cũ), `bioinformatics-topic-ideas-notion` (bản ba ý tưởng), và **Đề xuất chốt: vị trí gắn ATP + dự phòng efflux** (bản đang dùng). Sửa nội dung trên Notion thì file trong repo không tự cập nhật, và ngược lại |

### Bản nội dung chờ nhập Notion

### Trang Notion và bản nguồn tương ứng trong repo

| Trang Notion | Bản nguồn trong repo | Trạng thái |
|---|---|---|
| [Đề xuất chốt: vị trí gắn ATP + dự phòng efflux](https://app.notion.com/p/3ec486d98ebc813bb56eface997a23a9) | [bioinformatics-proposal-notion.md](../meeting/bioinformatics-proposal-notion.md) | **Đã nhập 01/10/2026.** Bản đang dùng |
| [bioinformatics-topic-ideas-notion](https://app.notion.com/p/3ec486d98ebc80a79ce1f6765bbf93ed) | [bioinformatics-topic-ideas-notion.md](../meeting/bioinformatics-topic-ideas-notion.md) | Đã nhập trước đó. **Đã bị thay thế** — giữ làm lịch sử bước so sánh ba hướng; hướng IL-6 bị loại 01/10/2026 |
| [Đề tài quản lý chi tiêu cá nhân](https://app.notion.com/p/3ea486d98ebc8101ad92c0786e2797fc) | — | Lưu làm lịch sử, đề tài đã tạm dừng |
