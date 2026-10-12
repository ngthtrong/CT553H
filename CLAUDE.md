# CLAUDE.md

## Giai đoạn hiện tại và vai trò

- Đây là giai đoạn **lên ý tưởng và hoàn thiện đề tài**, chưa bắt tay vào thực hiện. đang chuẩn bị gặp GVHD.
- Lựa chọn hiện hành: **`budgeted-microservice-rca` (12/10/2026)**; chưa được GVHD phê duyệt, chưa bắt đầu thực nghiệm phương pháp.

> **Quyết định lựa chọn 12/10/2026:** theo yêu cầu mở lĩnh vực và chốt trong ngày, đã chọn [`budgeted-microservice-rca`](docs/topics/budgeted-microservice-rca/01-idea/topic-decision.md) làm chính, degron làm dự phòng. [Báo cáo đối chiếu](docs/common/deep-research/reports/open-field-topic-selection-2026-10-12.md) là bản hiện hành. Chưa phê duyệt GVHD; vẫn ở giai đoạn đề cương, chưa huấn luyện hay triển khai ứng dụng.

### Mục tiêu tối cao của giai đoạn này (cập nhật 12/10/2026)

**Tìm và chốt được một đề tài có đóng góp thực sự, giải quyết một vấn đề có ý nghĩa.** Mục tiêu này đứng trên mọi ràng buộc khác ở giai đoạn này — kể cả độ khớp với các ứng viên đang có sẵn trong repo. Khi quyết định hướng đi tiếp theo (khảo sát, so sánh ứng viên, chốt đề tài), ưu tiên theo thứ tự này:

1. **Vẫn nên đi theo hướng tin sinh học (bioinformatics)** — đây là chuyên môn của GVHD ([advisor/README.md](docs/common/advisor/README.md)) và là nền đã đầu tư nhiều công sức khảo sát trong repo (xem [docs/topics/README.md](docs/topics/README.md), [work-log.md](docs/common/work-log.md)).
2. **Nhưng không bó buộc vào lối dự đoán AI/ML ở mức chi tiết** (ví dụ: dự đoán nhãn ở mức residue/peptide/site như các ứng viên đã xét — `rtk-atp-applicability`, `degron-e3-specificity`, dark kinome, sirtuin). Những hướng này nhiều lần vấp cùng một vấn đề trong repo: tiêu chí 5 (ứng dụng/website) luôn là phần gắn thêm gượng ép sau khi đã có mô hình, và cổng G2 (đóng góp dương đo được) liên tục khó xác lập vì nhãn hẹp hoặc đã có nhiều tiền lệ cùng dạng.
3. **Cân nhắc nghiêm túc các bài toán ở tầng tổng quan hơn**: công cụ (tool), phần mềm, nền tảng, hoặc thuật toán phục vụ một quy trình nghiên cứu/phân tích tin sinh học rộng hơn — không phải một mô hình dự đoán đơn lẻ. Ví dụ dạng bài toán (không phải danh sách đóng): công cụ kiểm soát rò rỉ dữ liệu/đánh giá chuẩn hóa cho một benchmark đang được dùng rộng rãi nhưng thiếu công cụ kiểm tra; pipeline tái lập hoặc tổng hợp nhiều nguồn dữ liệu rời rạc trong một nhánh tin sinh học; thư viện/API làm cầu nối giữa một phương pháp mới (PLM, XAI, v.v.) với các bài toán đã có; nền tảng trực quan hóa hoặc so sánh nhiều mô hình/bộ dữ liệu. Dạng bài toán này tự nhiên khớp tiêu chí 5 (sản phẩm phần mềm là trọng tâm, không phải phụ lục) và phù hợp hơn với một luận văn khoa Kỹ thuật phần mềm.
4. **Một đề tài hoàn toàn ngoài tin sinh học** (ví dụ ứng viên `legal-qa-grounding`, 12/10/2026) vẫn là ứng viên hợp lệ, không bị loại bởi định hướng này — nhưng xếp sau các hướng 1–3; chỉ nên ưu tiên chọn nếu khảo sát kỹ các hướng tin sinh học ở tầng cao hơn mà không tìm được đóng góp/ý nghĩa đủ thuyết phục.

Vẫn tham khảo [năm tiêu chí của GVHD](docs/meeting/session-01-minutes.md) (mục 4) và ba cổng bắt buộc G1/G2/G3 (nhãn độc lập — đóng góp dương đo được — ứng dụng khả thi, xem [main-topic-decision.md](docs/common/deep-research/reports/main-topic-decision.md)) khi đánh giá một ứng viên, bất kể ứng viên đó thuộc hướng nào trong bốn hướng trên. Quy trình làm việc cụ thể, cách trình bày, và cách bố trí file cho mỗi ứng viên mới: tự quyết theo tình huống, miễn giữ đúng cấu trúc thư mục và quy ước đặt tên đã mô tả bên dưới.

## Cấu trúc thư mục

Dự án là một monorepo **nhiều đề tài song song**: đây vẫn là giai đoạn ý tưởng, nên có thể có nhiều ý tưởng đề tài (khác lĩnh vực, khác bộ dữ liệu) được phát triển đồng thời trước khi chốt một. Mỗi đề tài đi theo quy trình riêng: ý tưởng → khảo sát → dữ liệu → đề cương → thiết kế → thí nghiệm ML → hệ thống → luận văn. Tài liệu, dữ liệu và code dùng riêng cho một đề tài nằm trong thư mục con đặt theo **slug đề tài** (chữ thường, không dấu, gạch ngang, tiếng Anh, ví dụ `rtk-atp-applicability`); tài liệu dùng chung cho mọi đề tài (nhật ký, tài nguyên, hướng dẫn, thông tin GVHD) nằm ở `docs/common/`.

Thư mục/file đánh dấu *(chưa có)* chỉ tạo khi bắt đầu giai đoạn đó hoặc khi đề tài đó thực sự cần, không tạo sẵn thư mục rỗng. Chỉ có **một** đề tài đi tới `backend/`, `frontend/`, `ml-service/`, `thesis/` — đề tài đã được chốt.

```text
CT553H/
├── docs/
│   ├── common/                   Dùng chung cho mọi đề tài
│   │   ├── advisor/                  Công bố, chuyên môn, tài liệu khoá học của GVHD (dùng để đánh giá độ khớp mọi đề tài)
│   │   ├── biology-basics/           Lộ trình tự học sinh học nền (PTM, cancer, aging) cho sinh viên CNTT: learning-roadmap.md; papers/ (chưa có) chứa PDF tải về
│   │   ├── lectures/                 Bộ bài giảng HTML tự học (sinh học nền, cancer, aging, ML, CNN/MCNN, PLM, XAI), mở offline bằng file://; index.html là mục lục
│   │   ├── deep-research/            Khảo sát sâu nhiều nguồn: reports/ (báo cáo tổng hợp), research_notes/<chủ-đề>/ (ghi chú theo nhánh). Chuyển sang docs/topics/<slug>/02-survey/ khi đề tài có slug
│   │   ├── resources.md              Artifact trên claude.ai, cache và môi trường cục bộ (không nằm trong git)
│   │   ├── work-log.md               Nhật ký theo phiên: đã làm gì, quyết định gì, còn dở gì (mọi đề tài)
│   │   └── CT553H.pdf                Yêu cầu học phần / rubric
│   ├── meeting/                  Biên bản gặp GVHD (dùng chung, một buổi có thể nói nhiều đề tài): session-NN-prep.md (trước), session-NN-minutes.md (sau), session-NN-slides/ (mã nguồn slide artifact)
│   └── topics/                   Một thư mục con theo slug cho mỗi ý tưởng đề tài
│       ├── README.md                 Danh sách đề tài đang cân nhắc và trạng thái
│       └── <slug>/                   Ví dụ: rtk-atp-applicability/
│           ├── 01-idea/                  Brainstorm, tóm tắt quyết định riêng đề tài này
│           ├── learn/                    Hub học HTML của đề tài, nếu cần (hiện có ở degron-e3-specificity)
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
- **Tên file/thư mục:** chữ thường, không dấu, tiếng Anh, nối bằng gạch ngang (`data-report.md`, `rtk-atp-applicability/`). Liên kết giữa các tài liệu dùng đường dẫn tương đối.
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
- Nhật ký làm việc (mọi đề tài): [docs/common/work-log.md](docs/common/work-log.md) · Tài nguyên ngoài repo: [docs/common/resources.md](docs/common/resources.md)
- **GVHD: TS. Hồ Quang Thái (Ho Quang Thai; QT Ho), ĐH Cần Thơ** — tên được người dùng xác nhận lại ngày 05/10/2026. Prof. YY Ou **không phải** GVHD, chỉ là đồng tác giả thường xuyên. Xem [docs/common/advisor/README.md](docs/common/advisor/README.md) để biết các nhánh nghiên cứu của GVHD trước khi đánh giá tính mới của một hướng
