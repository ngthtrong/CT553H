# Chấm điểm SenMayo trên scRNA-seq khối u — trạng thái 07/10/2026

Phục vụ hướng 2 trong [phân tích 4 hướng GVHD gợi ý](../../../docs/common/deep-research/reports/advisor-4-directions-analysis.md). Mục tiêu của bước này: **trả lời bằng số xem hướng 2 có đủ dữ liệu để huấn luyện hay không**, chứ chưa phải huấn luyện gì.

## Kết quả trên dữ liệu thật: GSE103322 (07/10/2026)

Dataset: [GSE103322](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE103322), ung thư biểu mô vảy đầu cổ (khoang miệng), Smart-seq2, Puram et al. 2017. GEO ghi 5.902 tế bào từ 18 bệnh nhân. Mọi số dưới đây là `[tự đo]`, trỏ về file trong [results/](results/).

### Bốn ngưỡng đi/dừng đặt trước (mục 7.3 tài liệu phân tích), không nới

| Điều kiện | Ngưỡng | Đo được | Kết quả |
|---|---|---|---|
| `n_patients` | ≥ 10 | **17** | Đạt |
| `patients_with_ge20_positives` | ≥ 8 | **7** | **Trượt** |
| `concentration_ratio` | ≤ 1,5 đạt; 1,5–3,0 đạt kèm trọng số theo bệnh nhân; > 3,0 dừng | **1,848** (HNSCC25: 23,1% tế bào dương, 12,5% tế bào) | Đạt kèm trọng số |
| `signature_coverage` | ≥ 0,6 | **0,966** (113/117; thiếu BEX3, KITL, SERPINB3C, SPX) | Đạt |

Nguồn: [GSE103322.h5ad.senmayo-report.json](results/GSE103322.h5ad.senmayo-report.json). Ngưỡng dương là phân vị 0,95 toàn dataset (296 tế bào dương).

### Điều các ngưỡng trên không bắt được: điểm SenMayo đi theo loại tế bào

- **70% tế bào dương là fibroblast** (207/296); 38 là tế bào ung thư, 32 là macrophage; **T cell và B cell: 0**. Tỉ lệ dương theo loại: macrophage 32,7%, fibroblast 14,4%, tế bào ung thư 1,7% (cùng file JSON, `positive_rate_per_celltype`).
- Nghĩa là chênh lệch giữa các bệnh nhân phần lớn là **chênh lệch thành phần loại tế bào**: bệnh nhân nhiều fibroblast có nhiều tế bào "dương". Bốn bệnh nhân có 0 tế bào dương. `concentration_ratio` tính cho mọi bệnh nhân (`concentration_ratio_per_patient`) lên tới **5,46** (HNSCC24) và trên 3,0 ở 3 bệnh nhân, nhưng ngưỡng 7.3 chỉ xét bệnh nhân có nhiều tế bào dương nhất nên không bắt được.
- **Đặt lại ngưỡng trong từng loại tế bào** ([within-celltype-summary.csv](results/GSE103322.h5ad.within-celltype-summary.csv), [per-patient](results/GSE103322.h5ad.within-celltype-per-patient.csv)):

| Loại tế bào | Tế bào | Bệnh nhân | Dương (top 5%) | Bệnh nhân có ≥ 20 dương | `concentration_ratio` |
|---|---|---|---|---|---|
| Fibroblast | 1.417 | 16 | 71 | **1** | 2,10 |
| Tế bào ung thư | 2.200 | 15 | 110 | **3** | **3,35** |
| Macrophage | 95 | 11 | 5 | 0 | 4,75 |

Khi chỉ so tế bào cùng loại, dataset này **trượt rõ** cả điều kiện số bệnh nhân có đủ tế bào dương lẫn (với tế bào ung thư) điều kiện dồn.

### Giả định khi xử lý, cần biết khi đọc số

- **Mã bệnh nhân suy từ tên tế bào**, vì file GEO không có cột bệnh nhân và trang GSM chỉ ghi enzyme và vị trí khối u. Giả định `HN26_...` và `HNSCC26_...` cùng một bệnh nhân. Ra **17 bệnh nhân, không phải 18** như GEO ghi; **109 tế bào** ở hai plate `HNSCC_combo1/2` trộn nhiều bệnh nhân, không xác định được của ai, nên bị loại khỏi thống kê theo bệnh nhân (vẫn được chấm điểm).
- **Giá trị trên GEO đã log hóa sẵn** (log2(TPM/10+1) theo bài gốc `[chưa kiểm trong bài báo]`), nên chạy với `--skip-norm`.
- Loại tế bào lấy từ chú thích của tác giả trong file GEO; 324 tế bào không phải ung thư nhưng không có loại được gộp là `unresolved`.

### Chạy lại

```bash
# tải (khoảng 90 MB)
curl -o data/tme-senescence-scrnaseq/raw/GSE103322_HNSCC_all_data.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE103nnn/GSE103322/suppl/GSE103322_HNSCC_all_data.txt.gz
python3 ml/tme-senescence-scrnaseq/preprocessing/convert_gse103322.py \
  --input data/tme-senescence-scrnaseq/raw/GSE103322_HNSCC_all_data.txt.gz \
  --out data/tme-senescence-scrnaseq/processed/GSE103322.h5ad
python3 ml/tme-senescence-scrnaseq/preprocessing/senmayo_score.py \
  --input data/tme-senescence-scrnaseq/processed/GSE103322.h5ad \
  --patient-key patient --celltype-key celltype --skip-norm \
  --out ml/tme-senescence-scrnaseq/preprocessing/results/
python3 ml/tme-senescence-scrnaseq/preprocessing/within_celltype.py \
  --scores ml/tme-senescence-scrnaseq/preprocessing/results/GSE103322.h5ad.senmayo-scores.csv \
  --celltypes Fibroblast cancer Macrophage
```

Môi trường: `.venv/` với scanpy 1.12.4, seed 42.

### Việc tiếp theo chưa làm

- GSE131907 (phổi, khoảng 208 nghìn tế bào, 10x) chưa tải: chỉ chạy khi hướng 2 còn được cân nhắc sau kết quả này. Dataset lớn hơn có thể sửa điều kiện "≥ 8 bệnh nhân có ≥ 20 tế bào dương", nhưng **không sửa được việc điểm đi theo loại tế bào**.

## Lịch sử: chặn mạng trước khi mở domain (07/10/2026)

Trước khi sinh viên thêm domain vào danh sách cho phép, mọi host dữ liệu (GEO, Zenodo, cellxgene, HuggingFace, figshare, UCSC) trả 403 ở bước CONNECT. Sau khi thêm, `ftp.ncbi.nlm.nih.gov` và `www.ncbi.nlm.nih.gov` trả 200.

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
