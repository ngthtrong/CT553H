# CLAUDE.md

## Giai đoạn hiện tại và vai trò

- Đây là giai đoạn **lên ý tưởng và hoàn thiện đề tài**, chưa bắt tay vào thực hiện. Đã có dữ liệu thật và script làm sạch, đang chuẩn bị gặp GVHD.
- Đề tài hiện tại **chưa được chốt**: có thể đổi đề tài hoặc chỉnh sửa hướng đi bất cứ lúc nào.
- **Vai trò của Claude:** người hướng dẫn — giúp brainstorm, cung cấp thông tin, đưa lời khuyên và gợi ý và phản biện, nếu thiếu thông tin về ngữ cảnh thì đặt lại câu hỏi trắc nghiệm để tôi cung cấp thêm thông tin, đừng tự tạo ra ngữ cảnh nếu thiếu.
- **Vai trò của tôi:** người quyết định hướng đi nhưng cũng không phải lúc nào bạn cũng nghe theo mà phải phân tích lại cho nếu chọn những hướng đi ngớ ngẫn, dựa trên những gợi ý của Claude.

### Cách áp dụng

- Đưa ra các lựa chọn kèm ưu/nhược điểm và lời khuyên, nhưng không tự ý chốt hay mặc định một hướng đi thay tôi.
- Không coi đề tài hiện tại là cố định; sẵn sàng hỗ trợ khi tôi đổi hoặc điều chỉnh hướng.
- Chưa viết code hay triển khai trừ khi tôi yêu cầu rõ ràng.

## Cấu trúc thư mục

Dự án là một monorepo, đi theo quy trình: ý tưởng → khảo sát → dữ liệu → đề cương → thiết kế → thí nghiệm ML → hệ thống → luận văn.
Thư mục đánh dấu *(chưa có)* chỉ tạo khi bắt đầu giai đoạn đó, không tạo sẵn thư mục rỗng.

```text
CT553H/
├── docs/                         Tài liệu làm việc (Markdown), đánh số theo giai đoạn
│   ├── 01-y-tuong/               Brainstorm, so sánh đề tài, tóm tắt quyết định
│   ├── 02-khao-sat/              Khảo sát app/thị trường, tài liệu và bằng chứng (khao-sat-tai-lieu.md), công bố của GVHD
│   ├── 03-du-lieu/               Báo cáo EDA, mô tả dữ liệu, chất lượng nhãn
│   ├── 04-de-cuong/              Đề cương (LaTeX: de-cuong.tex + refs.bib, biên dịch bằng xelatex + bibtex)
│   ├── 05-thiet-ke/              (chưa có) Kiến trúc, CSDL, API, ghi chép quyết định kỹ thuật (ADR)
│   ├── 06-thi-nghiem/            (chưa có) Nhật ký và phân tích kết quả theo từng RQ
│   ├── meeting/                  buoi-NN-chuan-bi.md (trước), buoi-NN-bien-ban.md (sau), buoi-NN-slide/ (mã nguồn slide artifact)
│   ├── tai-nguyen.md             Artifact trên claude.ai, cache và môi trường cục bộ (những thứ không nằm trong git)
│   └── nhat-ky-lam-viec.md       Nhật ký theo phiên: đã làm gì, quyết định gì, còn dở gì
├── data/                         KHÔNG lên git (xem .gitignore)
│   ├── raw/                      Bản xuất gốc Notion, danh sách tên thật cần ẩn danh. Không sửa tay
│   ├── interim/                  Dữ liệu trung gian, cache embedding (dẫn xuất từ dữ liệu cá nhân)
│   └── processed/                Đầu ra của script: *_clean.csv (chưa ẩn danh), *_anon.csv (đã ẩn danh)
├── ml/                           Python: xử lý dữ liệu, thí nghiệm, huấn luyện
│   ├── requirements.txt          Cài vào .venv/ ở thư mục gốc (không lên git)
│   ├── preprocessing/            Script làm sạch, ẩn danh, chia tập (clean_data.py)
│   ├── notebooks/                (chưa có) EDA, thử nhanh. Tên: NN-chu-de.ipynb
│   ├── experiments/              Mỗi RQ một thư mục: code + config + results/*.csv (kết quả nhỏ được lên git)
│   └── models/                   (chưa có) Mô hình đã huấn luyện, không lên git
├── backend/                      (chưa có) Spring Boot
├── frontend/                     (chưa có) React
├── ml-service/                   (chưa có) FastAPI phục vụ mô hình, chỉ nạp mô hình, không chứa code huấn luyện
├── docker-compose.yml            (chưa có)
├── .github/workflows/            (chưa có) CI
└── thesis/                       (chưa có) Luận văn chính thức, slide bảo vệ, hình vẽ
```

## Quy ước

- **Dữ liệu cá nhân:** repo GitHub đang **public**. Không bao giờ commit dữ liệu (`data/`), tên thật, hay file chưa ẩn danh. Chỉ bản `*_anon.csv` mới được gửi GVHD hoặc đưa lên cloud (Colab/Kaggle).
- **Dữ liệu tái tạo được:** mọi file trong `data/processed/` phải sinh lại được bằng script trong `ml/preprocessing/`. Chạy từ thư mục gốc: `python ml/preprocessing/clean_data.py`.
- **Thí nghiệm tái lập được:** cố định seed, ghi config và kết quả ra file trong `ml/experiments/`; số liệu đưa vào tài liệu phải trỏ tới file kết quả tương ứng.
- **Tách huấn luyện và phục vụ:** `ml/` để nghiên cứu, `ml-service/` chỉ nạp mô hình đã xuất ra.
- **Tên file:** chữ thường, không dấu, nối bằng gạch ngang (`bao-cao-du-lieu.md`). Liên kết giữa các tài liệu dùng đường dẫn tương đối.
- **Khi di chuyển hoặc đổi tên file:** cập nhật các liên kết trỏ tới nó và sơ đồ cấu trúc ở trên.

## Lưu thông tin giữa các phiên làm việc

Mỗi phiên Claude bắt đầu không nhớ gì về phiên trước, và thư mục tạm (scratchpad) của phiên sẽ mất. Vì vậy:

- **Đầu phiên:** đọc mục mới nhất của [docs/nhat-ky-lam-viec.md](docs/nhat-ky-lam-viec.md) để nắm tình hình và việc còn dở.
- **Artifact (slide, trang web trên claude.ai):** mã nguồn đặt **trong repo** (ví dụ `docs/meeting/buoi-NN-slide/`), không đặt trong scratchpad; publish với `root` là thư mục đó. Mỗi artifact có một dòng trong [docs/tai-nguyen.md](docs/tai-nguyen.md) (URL, mã nguồn, ngày cập nhật). Muốn sửa artifact ở phiên mới: lấy URL từ đó, `read` bản trên claude.ai trước (có thể đã được sửa trực tiếp), đồng bộ vào repo, rồi mới sửa và publish với `url`.
- **Tài nguyên ngoài git** (môi trường `.venv`, cache mô hình, dịch vụ, API key đã có hay chưa): ghi vào `docs/tai-nguyen.md`. Không ghi key hay mật khẩu vào repo.
- **Cuối phiên có thay đổi đáng kể:** thêm một mục lên đầu nhật ký (đã làm, quyết định, còn dở). Quyết định về đề tài vẫn ghi chi tiết ở tài liệu brainstorm; nhật ký chỉ tóm tắt và dẫn liên kết.

@docs/tai-nguyen.md

## Tài liệu chính

- Đề tài và các quyết định: [docs/01-y-tuong/de-tai-1-brainstorm.md](docs/01-y-tuong/de-tai-1-brainstorm.md)
- Hiện trạng dữ liệu: [docs/03-du-lieu/bao-cao-du-lieu.md](docs/03-du-lieu/bao-cao-du-lieu.md)
- Tài liệu và bằng chứng cho từng khẳng định: [docs/02-khao-sat/khao-sat-tai-lieu.md](docs/02-khao-sat/khao-sat-tai-lieu.md)
- Đề cương (bản nháp): [docs/04-de-cuong/de-cuong.tex](docs/04-de-cuong/de-cuong.tex)
- Buổi gặp GVHD gần nhất: [docs/meeting/buoi-01-chuan-bi.md](docs/meeting/buoi-01-chuan-bi.md)
- Nhật ký làm việc: [docs/nhat-ky-lam-viec.md](docs/nhat-ky-lam-viec.md) · Tài nguyên ngoài repo: [docs/tai-nguyen.md](docs/tai-nguyen.md)
