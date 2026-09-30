# Tài nguyên nằm ngoài repo

> Danh sách những thứ **không nằm trong git** nhưng cần dùng lại ở các phiên làm việc sau: artifact trên claude.ai, cache và môi trường cục bộ. File này được nạp tự động qua [CLAUDE.md](../../CLAUDE.md). Mỗi khi tạo mới hoặc đổi trạng thái một tài nguyên, cập nhật bảng tương ứng.

## 1. Artifact trên claude.ai

| Tên | URL | Loại | Mã nguồn trong repo | Cập nhật gần nhất | Chia sẻ |
|---|---|---|---|---|---|
| Slide buổi gặp GVHD lần 1 | https://claude.ai/artifact/YRqpuZNbzNdsBQFRnx7bCn | Slides (8 trang) | [meeting/buoi-01-slide/](../meeting/buoi-01-slide/) | 29/09/2026, bản 4: chuyển mã nguồn vào repo (bản 3 sửa slide RQ theo RQ2/RQ3 mới) | Riêng tư. Muốn gửi GVHD thì chia sẻ qua menu Share |

Artifact đang ở chế độ riêng tư: chỉ chủ tài khoản mở được link, nên để URL trong repo public không làm lộ nội dung.

### Cách sửa một artifact ở phiên mới
1. Lấy URL từ bảng trên.
2. Dùng Artifact `read` để đọc **bản đang có trên claude.ai**, vì có thể đã được sửa trực tiếp trên trang. Nếu khác với file trong repo, chép bản trên claude.ai đè vào repo trước.
3. Sửa file trong thư mục mã nguồn ở repo.
4. Publish với `url` là URL trên và `root` là thư mục mã nguồn (ví dụ `docs/meeting/buoi-01-slide`). Chỉ gửi những file đã đổi.
5. Cập nhật cột "Cập nhật gần nhất" ở bảng trên.

Artifact mới: đặt mã nguồn ngay trong repo (không để trong thư mục tạm của phiên), publish từ đó, rồi thêm một dòng vào bảng.

## 2. Môi trường và cache cục bộ (không lên git)

| Thứ | Vị trí | Cách tạo lại |
|---|---|---|
| Môi trường Python | `.venv/` ở thư mục gốc | `python3 -m venv .venv`, rồi `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu`, rồi `.venv/bin/pip install -r ml/requirements.txt` |
| Mô hình embedding | `~/.cache/huggingface/` (bge-m3 khoảng 2,2 GB; multilingual-e5-small, e5-base) | Tự tải khi chạy script thí nghiệm lần đầu |
| Cache embedding ghi chú | `data/quan-ly-chi-tieu-ca-nhan/interim/emb_bge-m3_titles.npz` | Tự sinh khi chạy `ml/quan-ly-chi-tieu-ca-nhan/experiments/rq2-baseline-nho-lai/run.py`; xóa khi đổi mô tả danh mục |
| Dữ liệu gốc và danh sách tên cần ẩn danh | `data/quan-ly-chi-tieu-ca-nhan/raw/` | Chỉ có trên máy của người làm đề tài; không tạo lại được |
| Dữ liệu đã làm sạch | `data/quan-ly-chi-tieu-ca-nhan/processed/` | `python ml/quan-ly-chi-tieu-ca-nhan/preprocessing/clean_data.py` |
| LaTeX | XeLaTeX, polyglossia, font TeX Gyre Termes (TeX Live 2023) | Biên dịch đề cương: xem dòng đầu của `docs/de-tai/quan-ly-chi-tieu-ca-nhan/04-de-cuong/de-cuong.tex` |

## 3. Dịch vụ bên ngoài

| Dịch vụ | Trạng thái |
|---|---|
| API LLM để sinh dữ liệu tổng hợp | Chưa chọn, chưa có key |
| Ollama / LLM chạy cục bộ | Chưa cài; máy không có GPU |
| Colab / Kaggle | Chưa dùng; chỉ đưa bản `*_anon.csv` lên |
| Notion (đã kết nối với Claude từ 29/09/2026) | Trang tóm tắt đề tài quản lý chi tiêu cá nhân: https://app.notion.com/p/3ea486d98ebc8101ad92c0786e2797fc (bản nháp riêng tư, tạo 29/09/2026). Nội dung gốc: [tom-tat-de-tai-notion.md](../de-tai/quan-ly-chi-tieu-ca-nhan/01-y-tuong/tom-tat-de-tai-notion.md). Sửa trên Notion thì file trong repo không tự cập nhật |
