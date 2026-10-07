# Chấm điểm SenMayo trên scRNA-seq khối u — trạng thái 07/10/2026

Phục vụ hướng 2 trong [phân tích 4 hướng GVHD gợi ý](../../../docs/common/deep-research/reports/advisor-4-directions-analysis.md). Mục tiêu của bước này: **trả lời bằng số xem hướng 2 có đủ dữ liệu để huấn luyện hay không**, chứ chưa phải huấn luyện gì.

## Việc đã làm và việc chưa làm được

| | Trạng thái |
|---|---|
| Môi trường (scanpy 1.12.4, numpy, pandas, scipy, h5py) | **Đã cài** `[tự đo]` |
| Danh sách gene SenMayo | **Đã có, 117 gene** — xem cảnh báo bên dưới `[tự đo]` |
| Script đếm tế bào/bệnh nhân + chấm điểm | **Đã viết và chạy được** (`senmayo_score.py`) `[tự đo]` |
| Tải dataset scRNA-seq khối u thật | **CHƯA LÀM ĐƯỢC — bị chặn ở tầng mạng của môi trường cloud**, xem bên dưới |
| Số tế bào / số bệnh nhân / tỉ lệ dương thật | **Chưa có** |

## Chặn mạng, đã thử và ghi đúng mã trả về (07/10/2026)

Chỉ `raw.githubusercontent.com` và PyPI đi được. Mọi host dữ liệu đều bị egress policy của môi trường từ chối ở bước CONNECT:

| Host | Kết quả |
|---|---|
| `ftp.ncbi.nlm.nih.gov` (GEO) | **403 ở CONNECT** |
| `zenodo.org` | 403 |
| `datasets.cellxgene.cziscience.com`, `api.cellxgene.cziscience.com` | 403 |
| `huggingface.co` | 403 |
| `ndownloader.figshare.com` | 403 |
| `cells.ucsc.edu` | 403 |
| `ha-dkfz.github.io` | 403 |
| `raw.githubusercontent.com` | **200** |

Hai đường đi tiếp, chưa chọn: (a) thêm `ftp.ncbi.nlm.nih.gov` vào danh sách domain cho phép của môi trường cloud rồi chạy lại script; (b) tải trên máy của sinh viên.

## Cảnh báo về danh sách gene: 117, không phải 125

SenMayo công bố là **125 gene** (Saul et al. 2022, *Nat Commun*, [10.1038/s41467-022-32552-1](https://doi.org/10.1038/s41467-022-32552-1)). File `senmayo_genes.txt` ở đây có **117 gene duy nhất**, lấy từ bộ chữ ký senescence của nhóm HA-DKFZ `[tự đo]` ([senmayo.csv](https://raw.githubusercontent.com/HA-DKFZ/senesence_signatures/main/pages/senmayo.csv), HTTP 200, 669 byte).

**Chưa xác định được 8 gene chênh lệch là gì** — phụ lục của bài gốc là file xlsx, không lấy được trong môi trường này. Vì vậy:

- Không gọi file này là "SenMayo 125 gene" trong bất kỳ tài liệu nào gửi GVHD.
- Trước khi dùng cho kết quả chính thức, phải đối chiếu lại với Supplementary Table của bài gốc.

## Kiểm script trên ma trận tổng hợp

Đã chạy trên một ma trận **tổng hợp** (3.000 tế bào, 1.617 gene, 12 "bệnh nhân", cấy tín hiệu vào 334 tế bào dồn ở 3 bệnh nhân). Script trả đúng cấu trúc đã cấy: `top1_patient_share_of_positives = 0,7667`.

**Đây là phép kiểm phần mềm, không phải kết quả sinh học.** Cùng một bài học từ [T1 Hybrid Cascade](../../../docs/common/thesis/thesis-comparison.md): hiệu ứng lớn trên dữ liệu tổng hợp chỉ chứng minh code chạy.

## Ngưỡng quyết định đã đặt trước

Bốn điều kiện đi/dừng cho hướng 2 **đã được đặt trước khi có số thật**, ngày 07/10/2026, ở [mục 7.3 của tài liệu phân tích](../../../docs/common/deep-research/reports/advisor-4-directions-analysis.md): `n_patients ≥ 10`, `patients_with_ge20_positives ≥ 8`, `concentration_ratio ≤ 3,0` (≤ 1,5 là sạch), `signature_coverage ≥ 0,6`. Không nới ngưỡng sau khi nhìn số; nếu nới thì ghi rõ ở chính mục đó kèm ngày.

## Con số cần đọc khi có dữ liệu thật

Ngưỡng mặc định là **phân vị 0,95 trong chính dataset**, nên `positive_fraction` luôn ≈ 5% — **không phải** phát hiện gì. Ba con số có ý nghĩa:

1. `n_patients` và `cells_per_patient` — có đủ bệnh nhân để chia fold theo bệnh nhân không? Dưới khoảng 10 bệnh nhân thì gần như không.
2. `concentration_ratio` — phần tế bào dương của bệnh nhân dồn nhất chia cho phần tế bào của chính họ. **1,0 là mức kỳ vọng** nếu senescence rải đều; càng lớn thì tín hiệu càng gắn với một bệnh nhân. Đây là con số quyết định.
3. `positive_rate_spread` — nếu tỉ lệ dương chênh lệch rất lớn giữa các bệnh nhân, mô hình sẽ học bệnh nhân chứ không học senescence. Đây đúng là phiên bản mức bệnh nhân của lỗi lệch độ dài mà T1 phát hiện giữa hai lớp.

## Giới hạn không khắc phục được bằng script này

Điểm SenMayo là **điểm biểu hiện của một chữ ký gene, không phải nhãn thực nghiệm**. Senescence không có chuẩn vàng ở mức tế bào trong mô (xem mục 7.1 của tài liệu phân tích), nên mọi mô hình có giám sát huấn luyện trên nhãn dẫn từ điểm này **đang học lại chính bộ chấm điểm đó**. Script này chỉ dùng để đánh giá tính khả thi của dữ liệu.
