[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# MetaDegron 2024 — công cụ bổ sung về motif/E3, không phải đối thủ cùng bài toán

| | |
|---|---|
| **Nơi công bố** | *Briefings in Bioinformatics*, 2024 |
| **DOI** | <https://doi.org/10.1093/bib/bbae519> · toàn văn [PMC11491831](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/) |
| **Giấy phép** | Bài CC BY; **repo không có LICENSE**; nhãn gốc từ ELM (Academic License). Chỉ dẫn link, chưa sao chép hình/dữ liệu |
| **Mức kiểm** | **[ĐỌC-MÃ]/[ĐO]** — nâng từ [NGUỒN] ngày 21/10/2026 sau khi đọc toàn văn, đọc mã (commit `ca12c0cf…`) và đếm số liệu. Không kiểm mọi thí nghiệm sinh học gốc, không chạy mô hình D |
| **Báo cáo gốc** | [metadegron-analysis-2026-10-21](../../../topics/degron-footprint/research/metadegron-analysis-2026-10-21/README.md) |

> **Đính chính 21/10/2026.** Bản ghi chép trước (chỉ đọc tóm tắt) gọi bài này là "đối thủ trực tiếp nhất" và mô tả "21 E3 theo từng E3", "nhãn âm là peptide ngẫu nhiên", "chia 90/10 không kiểm soát đồng dạng". Audit cho thấy các câu đó **đúng một phần hoặc sai**; bảng kiểm từng câu ở [claims-verification.md](../../../topics/degron-footprint/research/metadegron-analysis-2026-10-21/claims-verification.md). Nội dung dưới đây thay bản cũ.

---

## Bài này làm gì

Dự đoán **motif degron ứng viên** trong protein, gắn với một trong **21 lựa chọn E3** trên máy chủ web (cây chọn E3, FASTA batch, bảng hit có tọa độ và điểm, cấu trúc 3D/MSA/mạng). `[ĐỌC-MÃ]`

- Hai nhánh: **MetaDegron-D** (trình tự: SeqVec 29×1024 + Conv1D + BiLSTM + embedding token, ghép ở tầng dense) và **MetaDegron-X** (XGBoost trên **10 thuộc tính**: ASA, disorder, conservation, coil, ANCHOR, số PTM flank, số lysine ubiquitin flank, helix, rigidity, domain Pfam). Web chọn X cho accession có sẵn thuộc tính, D cho chuỗi khác. `[ĐỌC-MÃ]`
- **Không có 21 classifier.** Một bộ phân loại nhị phân dùng chung; E3 được chọn chỉ quyết định **regex motif nào được quét**. Sau lọc HUMAN, vùng trùng và cụm của đề tài, chỉ còn **2 nhóm motif ≥ 5 mẫu**. `[ĐỌC-MÃ]`/`[ĐO]`
- Đầu ra là xác suất nhị phân theo hit; **không** có ΔPSI hay điểm theo từng phép thay. `[ĐỌC-MÃ]`

## Dữ liệu (đếm từ file)

- **302 dòng curate / 240 accession / 31 loại motif**; 227 dòng HUMAN; tập X dùng 212 dương tính. Nguồn: ELM (166 dòng) và y văn; nhãn **nhị phân, hỗn hợp loài và hệ đo** (binding/degradation/PTM). `[ĐO]`
- Nhãn âm: **đoạn protein thật được lấy mẫu** làm background (có hoàn lại trong script X), không chứng minh là chuỗi ngẫu nhiên tổng hợp và không có thí nghiệm xác nhận bất hoạt. `[ĐỌC-MÃ]`
- Mẫu truy nguồn 40 dòng: 22 có ELM true-positive cùng class; 18 chưa chốt lineage — **không phải tỉ lệ nhãn sai**. `[ĐO]`

## So sánh với đề tài

| Khía cạnh | MetaDegron | Đề tài |
|---|---|---|
| **Nhãn** | 302 dòng curate, nhị phân, theo motif | ΔPSI liên tục từ GPS; G2: 91 peptide / 47.847 ô |
| **Nhãn âm** | background sampled, không xác nhận | ô đã đo ΔPSI dưới ngưỡng |
| **Chia tập** | D: random 90/10; X: StratifiedKFold trên mẫu có hoàn lại (91–111 dòng test trùng tọa độ với train mỗi fold); **không thấy** group split | cụm protein MMseqs2 id30 cov80 (cov50 kiểm nhạy) |
| **Thước đo** | AUROC peptide: X 0,87 CV / 0,86 ind; D 0,90 / 0,90 | AUROC mức ô macro theo peptide: ridge M3 0,8082, ΔPAP 0,7693 |
| **Đơn vị dự đoán** | hit motif/cửa sổ trong protein | phép thay acid amin tại một vị trí |

Hai con số AUC **không cùng thang** (khác nhãn, đơn vị, cách gộp). Đừng nói "inflated"; nói "không so sánh được".

## Những gì đã tái lập

- Đọc cây XGBoost từ checkpoint X bằng parser tĩnh (không `pickle.load`) và tái tính **AUC 0,9670** trên β-TrCP khớp số công bố — nhưng **8/20 dương tính "independent" nằm trong bảng fitting**, nên không phải holdout sạch. `[ĐO]`
- **Chưa** chạy D, chưa có điểm zero-shot trên GPS hay ΔScore trên ma trận bão hòa (thiếu runtime SeqVec; cửa sổ web 49 khác cấu hình 29; điều khoản server chưa rõ nên không gửi chuỗi). `[CHƯA XÁC MINH]`

## Hệ quả cho đề tài

- MetaDegron cạnh tranh về **điểm tiếp xúc người dùng** (FASTA → hit → web), không cạnh tranh về bài toán ΔPSI. Là **công cụ bổ sung và baseline chuyển giao tiềm năng**; muốn thành đối thủ trực tiếp phải được chấm bằng `−ΔScore` trên cùng ô G2 (chưa chạy).
- **Không nhập** nhãn nhị phân của nó vào thang ΔPSI; giao với dữ liệu của đề tài rất nhỏ (2 peptide quét, 1 bão hòa — HIF1A, 0 CRISPR) nên không dùng làm kiểm chứng ngoài cho footprint.
- "Batch" không phải điểm khác biệt G3 (MetaDegron có FASTA batch).

## Việc còn mở

Chạy MetaDegron-D/X trên GPS và ma trận mutant (cần runtime hoặc xin phép dùng server); xác minh quyền dùng nhãn ELM; adjudicate nguồn thực nghiệm cho toàn bộ dòng. Xem [recommendations.md](../../../topics/degron-footprint/research/metadegron-analysis-2026-10-21/recommendations.md).

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
