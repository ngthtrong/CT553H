# Kiểm các nhận định trong ghi chép MetaDegron cũ

[ĐỌC-MÃ] Đối tượng kiểm là `lectures/degron-basics/papers/metadegron-2024.md`, không chỉnh file đó. Bằng chứng nguồn ghim: [source-manifest.json](source-manifest.json), code locations: [code-audit.json](code-audit.json).

| Nhận định | Xác minh | Kết quả | Nhãn | Ghi chú/bằng chứng |
|---|---|---|---|---|
| ≈300 degron | Đếm cả repo/S2 | **Đúng một phần**: 302 record; X chỉ 212; không tất cả HUMAN | [ĐO] | [dataset-audit.json](dataset-audit.json), audit_dataset.py |
| Dương tính curate từ ELM/y văn | S2 PMID/source | **Đúng** ở provenance; chưa đủ bảo đảm mọi dòng là degron đã đo trực tiếp | [ĐO]/[DIỄN GIẢI] | 166 ELM_TP; [manual-label-review.json](manual-label-review.json) |
| Nhãn âm là peptide ngẫu nhiên | Mã sampling + tọa độ/UniProt | **Đúng một phần**: sampled protein segments; không chứng minh random AA tổng hợp | [ĐỌC-MÃ]/[ĐO] | Generator tọa độ ban đầu thiếu; histogram độ dài dịch+1: [dataset-audit.json](dataset-audit.json) |
| Âm chắc chắn dễ phân biệt hơn âm thật | Baseline thành phần/độ dài | **Không kiểm được** như kết luận chung; có tín hiệu khoảng0,73, chưa đủ tiêu chí shortcut mạnh | [ĐO]/[CHƯA XÁC MINH] | Không có tập “âm thật” đối chứng cùng population; [composition-baseline.json](composition-baseline.json) |
| Chia90/10 không kiểm soát đồng dạng | Đọc D/X và notebook | **Đúng một phần**: D random 90/10, X standalone CV 5 fold; không thấy group split trong mã | [ĐỌC-MÃ] | Cột cluster upstream không được dùng; exact split D chưa dựng lại |
| Gần như chắc chắn rò rỉ homology | MMseqs và mô phỏng | **Đúng một phần**: rủi ro đo được trong mô phỏng, chưa đo exact D split; X có duplicate leakage đo trực tiếp từ cách split | [ĐO] | [overlap-audit.json](overlap-audit.json), [composition-baseline.json](composition-baseline.json) |
| AUC0,87–0,90 | Đọc toàn văn | **Đúng một phần**: X CV 0,87/ind 0,86; D CV/ind 0,90; β-TrCP khác bộ có 0,9670 | [NGUỒN]/[ĐO] | [Bài](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/), [safe-x-reproduction.json](safe-x-reproduction.json) |
| SeqVec+BLSTM+conv-pooling+XGBoost10features | Đọc builder/train/predict | **Đúng một phần**: các thành phần tồn tại nhưng X/D là hai route, không một mạng joint X+D; hai biểu diễn sequence được ghép trong D | [ĐỌC-MÃ] | [model-and-evaluation.md](model-and-evaluation.md) |
| 21 E3 được mô hình hóa riêng | Input/head/mapping | **Sai** nếu hiểu 21 classifier/head học đặc hiệu; **đúng** nếu hiểu 21 lựa chọn motif ở web | [ĐỌC-MÃ]/[ĐO] | Mô hình dùng chung; số mẫu tương thích motif có cả0; [overlap-audit.json](overlap-audit.json) |
| rASA/disorder ở đầu vào | Danh sách cột10/biểu diễn D | **Đúng một phần**: ASA_SCORE/DSS_SCORE vào X, không trực tiếp vào D; chưa đồng nhất ASA với rASA | [ĐỌC-MÃ] | [code-audit.json](code-audit.json), phần10features |
| Bản đồ residue của đề tài tự khác mọi công cụ | So nhiệm vụ/tiền lệ | **Sai** nếu dùng độ phân giải làm duy nhất: Degpred có residue score; Degformer có mutation map | [DIỄN GIẢI] | Khác biệt cần ở nhãn/điều kiện đánh giá, không tuyên bố độc quyền đầu ra |
| Cổng exposure của đề tài là đóng góp đã có lợi | Đối chiếu trạng thái21/10 | **Sai** ở trạng thái hiện tại: hiệu ứng đảo theo seed và thua ridge | [ĐO] | [current-topic-evidence.json](current-topic-evidence.json) |

[DIỄN GIẢI] Mức kiểm được nâng trong **báo cáo này**: toàn văn, mã, số đếm và tái tính nhánh X. Không suy ra đã kiểm mọi thí nghiệm sinh học, mọi endpoint live hoặc mọi phiên bản MetaDegron. Các ghi chép Degpred/ELITE/DEGRONOPEDIA đã đọc làm bối cảnh nhưng những nhận định chưa được kiểm trực tiếp vẫn không nâng mức bằng chứng.
