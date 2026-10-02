# CLAUDE.md

## Giai đoạn hiện tại và vai trò

- Đây là giai đoạn **lên ý tưởng và hoàn thiện đề tài**, chưa bắt tay vào thực hiện. đang chuẩn bị gặp GVHD.
- Đề tài hiện tại **chưa được chốt**: có thể đổi đề tài hoặc chỉnh sửa hướng đi bất cứ lúc nào.
- **Vai trò của Claude:** người hướng dẫn — giúp brainstorm, cung cấp thông tin, đưa lời khuyên và gợi ý và phản biện, nếu thiếu thông tin về ngữ cảnh thì đặt lại câu hỏi trắc nghiệm để tôi cung cấp thêm thông tin, đừng tự tạo ra ngữ cảnh nếu thiếu.
- **Vai trò của tôi:** người quyết định hướng đi nhưng cũng không phải lúc nào bạn cũng nghe theo mà phải phân tích lại cho nếu chọn những hướng đi ngớ ngẫn, dựa trên những gợi ý của Claude.

### Cách áp dụng

- Đưa ra các lựa chọn kèm ưu/nhược điểm và lời khuyên, nhưng không tự ý chốt hay mặc định một hướng đi thay tôi.
- Không coi đề tài hiện tại là cố định; sẵn sàng hỗ trợ khi tôi đổi hoặc điều chỉnh hướng.
- Chưa viết code hay triển khai trừ khi tôi yêu cầu rõ ràng.

## Cấu trúc thư mục

Dự án là một monorepo **nhiều đề tài song song**: đây vẫn là giai đoạn ý tưởng, nên có thể có nhiều ý tưởng đề tài (khác lĩnh vực, khác bộ dữ liệu) được phát triển đồng thời trước khi chốt một. Mỗi đề tài đi theo quy trình riêng: ý tưởng → khảo sát → dữ liệu → đề cương → thiết kế → thí nghiệm ML → hệ thống → luận văn. Tài liệu, dữ liệu và code dùng riêng cho một đề tài nằm trong thư mục con đặt theo **slug đề tài** (chữ thường, không dấu, gạch ngang, tiếng Anh, ví dụ `personal-expense-management`); tài liệu dùng chung cho mọi đề tài (nhật ký, tài nguyên, hướng dẫn, thông tin GVHD) nằm ở `docs/common/`.

Thư mục/file đánh dấu *(chưa có)* chỉ tạo khi bắt đầu giai đoạn đó hoặc khi đề tài đó thực sự cần, không tạo sẵn thư mục rỗng. Chỉ có **một** đề tài đi tới `backend/`, `frontend/`, `ml-service/`, `thesis/` — đề tài đã được chốt.

```text
CT553H/
├── docs/
│   ├── common/                   Dùng chung cho mọi đề tài
│   │   ├── advisor/                  Công bố, chuyên môn, tài liệu khoá học của GVHD (dùng để đánh giá độ khớp mọi đề tài)
│   │   ├── deep-research/            Khảo sát sâu nhiều nguồn: reports/ (báo cáo tổng hợp), research_notes/<chủ-đề>/ (ghi chú theo nhánh). Chuyển sang docs/topics/<slug>/02-survey/ khi đề tài có slug
│   │   ├── resources.md              Artifact trên claude.ai, cache và môi trường cục bộ (không nằm trong git)
│   │   ├── work-log.md               Nhật ký theo phiên: đã làm gì, quyết định gì, còn dở gì (mọi đề tài)
│   │   └── CT553H.pdf                Yêu cầu học phần / rubric
│   ├── meeting/                  Biên bản gặp GVHD (dùng chung, một buổi có thể nói nhiều đề tài): session-NN-prep.md (trước), session-NN-minutes.md (sau), session-NN-slides/ (mã nguồn slide artifact)
│   └── topics/                   Một thư mục con theo slug cho mỗi ý tưởng đề tài
│       ├── README.md                 Danh sách đề tài đang cân nhắc và trạng thái
│       └── <slug>/                   Ví dụ: personal-expense-management/
│           ├── 01-idea/                  Brainstorm, tóm tắt quyết định riêng đề tài này
│           ├── 02-survey/                Khảo sát app/thị trường, tài liệu và bằng chứng (literature-survey.md)
│           ├── 03-data/                  Báo cáo EDA, mô tả dữ liệu, chất lượng nhãn
│           ├── 04-proposal/              Đề cương (LaTeX: proposal.tex + references.bib, biên dịch bằng xelatex + bibtex)
│           ├── 05-design/                (chưa có) Kiến trúc, CSDL, API, ghi chép quyết định kỹ thuật (ADR)
│           └── 06-experiments/           (chưa có) Nhật ký và phân tích kết quả theo từng RQ
├── data/                         KHÔNG lên git (xem .gitignore)
│   └── <slug>/
│       ├── raw/                      Dữ liệu gốc, danh sách tên thật cần ẩn danh (nếu có). Không sửa tay
│       ├── interim/                  Dữ liệu trung gian, cache embedding (dẫn xuất từ dữ liệu gốc)
│       └── processed/                Đầu ra của script: *_clean.csv (chưa ẩn danh), *_anon.csv (đã ẩn danh)
├── ml/                           Python: xử lý dữ liệu, thí nghiệm, huấn luyện
│   ├── requirements.txt          Cài vào .venv/ ở thư mục gốc (không lên git, dùng chung mọi đề tài)
│   └── <slug>/
│       ├── preprocessing/            Script làm sạch, ẩn danh, chia tập (clean_data.py)
│       ├── notebooks/                (chưa có) EDA, thử nhanh. Tên: NN-topic.ipynb
│       ├── experiments/              Mỗi RQ một thư mục: code + config + results/*.csv (kết quả nhỏ được lên git)
│       └── models/                   (chưa có) Mô hình đã huấn luyện, không lên git
├── backend/                      (chưa có) Spring Boot — chỉ đề tài đã chốt
├── frontend/                     (chưa có) React — chỉ đề tài đã chốt
├── ml-service/                   (chưa có) FastAPI phục vụ mô hình — chỉ đề tài đã chốt
├── docker-compose.yml            (chưa có)
├── .github/workflows/            (chưa có) CI
└── thesis/                       (chưa có) Luận văn chính thức, slide bảo vệ, hình vẽ — chỉ đề tài đã chốt
```

## Quy ước

- **Repo riêng tư:** repo GitHub đã chuyển sang **private** từ 01/10/2026. Nhờ vậy repo được phép chứa PDF bài báo, tài liệu khoá học của GVHD (`docs/common/advisor/`) và các phân tích kỹ thuật về bài của nhóm GVHD (`docs/common/deep-research/`). Nếu sau này đổi sang public hoặc chia sẻ repo cho người khác (kể cả GVHD), phải gỡ những phần này trước, kể cả khỏi lịch sử git.
- **Dữ liệu cá nhân:** dù repo đã private, vẫn không bao giờ commit dữ liệu (`data/`), tên thật, hay file chưa ẩn danh. Chỉ bản `*_anon.csv` mới được gửi GVHD hoặc đưa lên cloud (Colab/Kaggle).
- **Dữ liệu tái tạo được:** mọi file trong `data/<slug>/processed/` phải sinh lại được bằng script trong `ml/<slug>/preprocessing/`. Chạy từ thư mục gốc: `python ml/<slug>/preprocessing/clean_data.py`.
- **Thí nghiệm tái lập được:** cố định seed, ghi config và kết quả ra file trong `ml/<slug>/experiments/`; số liệu đưa vào tài liệu phải trỏ tới file kết quả tương ứng.
- **Tách huấn luyện và phục vụ:** `ml/` để nghiên cứu, `ml-service/` chỉ nạp mô hình đã xuất ra.
- **Tên file/thư mục:** chữ thường, không dấu, tiếng Anh, nối bằng gạch ngang (`data-report.md`, `personal-expense-management/`). Liên kết giữa các tài liệu dùng đường dẫn tương đối.
- **Khi di chuyển hoặc đổi tên file:** cập nhật các liên kết trỏ tới nó và sơ đồ cấu trúc ở trên.
- **Đề tài mới:** tạo `docs/topics/<slug>/01-idea/` khi ý tưởng đủ cụ thể để cần tài liệu riêng (không phải ngay khi vừa nảy ra ý); thêm một dòng vào `docs/topics/README.md`. Chỉ tạo `data/<slug>/` và `ml/<slug>/` khi thực sự có dữ liệu/code cho đề tài đó.

## Lưu thông tin giữa các phiên làm việc

Mỗi phiên Claude bắt đầu không nhớ gì về phiên trước, và thư mục tạm (scratchpad) của phiên sẽ mất. Vì vậy:

- **Đầu phiên:** đọc mục mới nhất của [docs/common/work-log.md](docs/common/work-log.md) để nắm tình hình và việc còn dở, và [docs/topics/README.md](docs/topics/README.md) để biết đề tài nào đang hoạt động.
- **Artifact (slide, trang web trên claude.ai):** mã nguồn đặt **trong repo** (ví dụ `docs/meeting/session-NN-slides/`), không đặt trong scratchpad; publish với `root` là thư mục đó. Mỗi artifact có một dòng trong [docs/common/resources.md](docs/common/resources.md) (URL, mã nguồn, ngày cập nhật). Muốn sửa artifact ở phiên mới: lấy URL từ đó, `read` bản trên claude.ai trước (có thể đã được sửa trực tiếp), đồng bộ vào repo, rồi mới sửa và publish với `url`.
- **Tài nguyên ngoài git** (môi trường `.venv`, cache mô hình, dịch vụ, API key đã có hay chưa): ghi vào `docs/common/resources.md`. Không ghi key hay mật khẩu vào repo.
- **Cuối phiên có thay đổi đáng kể:** thêm một mục lên đầu nhật ký chung (đã làm, quyết định, còn dở, **kèm tên đề tài** nếu làm cho một đề tài cụ thể). Quyết định về từng đề tài vẫn ghi chi tiết ở tài liệu brainstorm riêng của đề tài đó; nhật ký chung chỉ tóm tắt và dẫn liên kết.

@docs/common/resources.md

## Tài liệu chính

- Danh sách đề tài: [docs/topics/README.md](docs/topics/README.md)
- Nhật ký làm việc (mọi đề tài): [docs/common/work-log.md](docs/common/work-log.md) · Tài nguyên ngoài repo: [docs/common/resources.md](docs/common/resources.md) · GVHD: [docs/common/advisor/](docs/common/advisor/)

### Đề tài đã chốt: `rtk-atp-applicability` (02/10/2026)

**Xây dựng hệ thống dự đoán vị trí gắn ATP ở protein RTK có cảnh báo miền áp dụng, dùng PLM–MCNN và truy hồi, đánh giá bằng giao thức kiểm soát rò rỉ dữ liệu.** Quyết định của sinh viên, **chưa có phê duyệt GVHD** — buổi gặp sáng 02/10/2026.

- **[Thuyết minh chi tiết](docs/topics/rtk-atp-applicability/04-proposal/topic-proposal.md)** — đọc file này trước, nó là bản chuẩn của đề tài
- [Quyết định và phạm vi](docs/topics/rtk-atp-applicability/01-idea/topic-decision.md) · [Bài báo liên quan chính](docs/topics/rtk-atp-applicability/02-survey/key-papers.md) · [Dữ liệu đã tải và kiểm tra](docs/topics/rtk-atp-applicability/03-data/data-report.md)
- Trình bày: [dàn ý và kịch bản nói](docs/meeting/2026-10-02-rtk-atp-slide-outline.md) · slide 13 trang: https://claude.ai/artifact/GGw1vJ2wpJKF63gmoBgLYT (mã nguồn [docs/meeting/session-01-slides/](docs/meeting/session-01-slides/))
- Notion: [Đề tài chốt: Dự đoán vị trí gắn ATP ở RTK có cảnh báo miền áp dụng](https://app.notion.com/p/3ec486d98ebc8103aaa8fef200473880)
- Dữ liệu tái tạo: `python3 ml/rtk-atp-applicability/preprocessing/prepare_data.py`
- **Quy ước ngôn từ riêng của đề tài:** nói “kiểm soát rò rỉ”, không nói “chống rò rỉ”/“không rò rỉ”. Gọi identity là “tín hiệu miền áp dụng”, không gọi là “độ tin cậy”. Không tuyên bố “đầu tiên” hay “vượt SOTA”. Nhận xét mã nguồn RTK_RAG luôn kèm giới hạn “chưa kết luận đây là phiên bản tạo ra số liệu bài báo”.
- Hai RQ: (1) truy hồi giúp bao nhiêu khi kiểm soát đồng dạng, có nhánh k-NN để tách nguồn lợi ích; (2) identity có dùng được làm tín hiệu miền áp dụng không. Việc kỹ thuật kế tiếp: **chạy alignment và gom cụm đồng dạng**, chưa làm.

### Nền khảo sát dẫn tới quyết định (lịch sử, không phải bản đang dùng)

- [Khảo sát 4 đề xuất tin sinh](docs/common/deep-research/reports/bioinformatics-topic-survey.md) · [khảo sát theo trọng tâm hệ thống](docs/common/deep-research/reports/bioinformatics-application-topics.md) · [ghi chú theo nhánh](docs/common/deep-research/research_notes/bioinformatics-topic-survey/)
- Bằng chứng tự kiểm chứng: [chọn ngưỡng G-mean trong mã công khai](docs/common/deep-research/reports/rtk-rag-threshold-verification.md) · [RAG-msCNN](docs/common/deep-research/reports/rag-mscnn-verification.md)
- Bản trao đổi và so sánh hướng trước khi chốt: [session-01-prep.md](docs/meeting/session-01-prep.md) · [bioinformatics-application-pitch.md](docs/meeting/bioinformatics-application-pitch.md) · [bioinformatics-topic-ideas-notion.md](docs/meeting/bioinformatics-topic-ideas-notion.md) · [bioinformatics-proposal-notion.md](docs/meeting/bioinformatics-proposal-notion.md)

### Đề tài: quản lý chi tiêu cá nhân (`docs/topics/personal-expense-management/`), **tạm dừng từ 01/10/2026**

- Đề tài và các quyết định: [01-idea/brainstorm.md](docs/topics/personal-expense-management/01-idea/brainstorm.md)
- Hiện trạng dữ liệu: [03-data/data-report.md](docs/topics/personal-expense-management/03-data/data-report.md)
- Tài liệu và bằng chứng cho từng khẳng định: [02-survey/literature-survey.md](docs/topics/personal-expense-management/02-survey/literature-survey.md)
- Đề cương (bản nháp): [04-proposal/proposal.tex](docs/topics/personal-expense-management/04-proposal/proposal.tex)
