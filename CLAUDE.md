# CLAUDE.md

## Giai đoạn hiện tại và vai trò

- Đây là giai đoạn **lên ý tưởng và hoàn thiện đề tài**, chưa bắt tay vào thực hiện. Đã có dữ liệu thật và script làm sạch, đang chuẩn bị gặp GVHD.
- Đề tài hiện tại **chưa được chốt**: có thể đổi đề tài hoặc chỉnh sửa hướng đi bất cứ lúc nào.
- **Vai trò của Claude:** người hướng dẫn — giúp brainstorm, cung cấp thông tin, đưa lời khuyên và gợi ý và phản biện.
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
│   ├── 02-khao-sat/              Khảo sát app/thị trường, tài liệu liên quan, công bố của GVHD
│   ├── 03-du-lieu/               Báo cáo EDA, mô tả dữ liệu, chất lượng nhãn
│   ├── 04-de-cuong/              (chưa có) Đề cương chính thức nộp khoa
│   ├── 05-thiet-ke/              (chưa có) Kiến trúc, CSDL, API, ghi chép quyết định kỹ thuật (ADR)
│   ├── 06-thi-nghiem/            (chưa có) Nhật ký và phân tích kết quả theo từng RQ
│   └── meeting/                  buoi-NN-chuan-bi.md (trước buổi gặp), buoi-NN-bien-ban.md (sau buổi gặp)
├── data/                         KHÔNG lên git (xem .gitignore)
│   ├── raw/                      Bản xuất gốc Notion, danh sách tên thật cần ẩn danh. Không sửa tay
│   ├── interim/                  (chưa có) Dữ liệu trung gian
│   └── processed/                Đầu ra của script: *_clean.csv (chưa ẩn danh), *_anon.csv (đã ẩn danh)
├── ml/                           Python: xử lý dữ liệu, thí nghiệm, huấn luyện
│   ├── requirements.txt
│   ├── preprocessing/            Script làm sạch, ẩn danh, chia tập (clean_data.py)
│   ├── notebooks/                (chưa có) EDA, thử nhanh. Tên: NN-chu-de.ipynb
│   ├── experiments/              (chưa có) Mỗi RQ một thư mục: code + config + results/*.csv (kết quả nhỏ được lên git)
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

## Tài liệu chính

- Đề tài và các quyết định: [docs/01-y-tuong/de-tai-1-brainstorm.md](docs/01-y-tuong/de-tai-1-brainstorm.md)
- Hiện trạng dữ liệu: [docs/03-du-lieu/bao-cao-du-lieu.md](docs/03-du-lieu/bao-cao-du-lieu.md)
- Buổi gặp GVHD gần nhất: [docs/meeting/buoi-01-chuan-bi.md](docs/meeting/buoi-01-chuan-bi.md)
