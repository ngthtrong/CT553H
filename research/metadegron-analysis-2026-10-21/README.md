# MetaDegron và degron-footprint — audit 21/10/2026

1. [ĐỌC-MÃ] Nhãn chính là ΔPSI thực nghiệm = PSI(mutant) − PSI(WT); dương nghĩa là reporter bền hơn. [Nguồn pipeline](../residue-task-derisk-2026-10-15/residue_data.py).
2. [ĐỌC-MÃ] Một dự đoán ứng với một phép thay acid amin tại một vị trí; gộp thành bản đồ vị trí × acid amin. [Runner G2](../g2-saturation-2026-10-18/run.py).
3. [ĐO] Bộ quét có 2.624 footprint theo bộ lọc lịch sử; không phải số protein độc lập. [current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2.
4. [ĐO] Bão hòa thô có 249 peptide; benchmark G2 còn 91 peptide / 89 cụm / 47.847 ô. [current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2.
5. [ĐỌC-MÃ] Chỉ số chính hiện hành: AUROC mức ô, macro theo peptide, ô dương khi ΔPSI ≥ 1. [Protocol](../g2-saturation-2026-10-18/PROTOCOL.md).
6. [ĐỌC-MÃ] G2 dùng 5 outer fold theo cụm protein MMseqs2 id30/cov80; cov50 dùng kiểm độ nhạy. [Runner](../g2-saturation-2026-10-18/run.py).
7. [ĐO] Seed 17/29/43 là seed huấn luyện trên cùng outer partition; bootstrap 5.000 lần theo cụm. [current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2.
8. [ĐO] Ridge M3 0,8082; ΔPAP 0,7693; Degformer retrain 0,7500, riêng đối chứng sau chỉ một seed. [current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2.
9. [ĐO] CRISPR có 31 screen, 10 E3 được gán; chỉ 1 E3 có ít nhất 5 peptide. [current-topic-evidence.json](current-topic-evidence.json); đọc lại JSON thí nghiệm cũ, không huấn luyện lại G2.
10. [DIỄN GIẢI] G2 còn mở: lượng nhãn chưa kiểm trực tiếp, tiền huấn luyện mức túi chưa chứng minh, so pretrained Degformer sạch cụm chưa xong; định vị cần GVHD chấp thuận. Trạng thái hiện hành.

## Kết luận điều hành

- [ĐO] MetaDegron cung cấp 302 dòng curate / 240 accession; 227 dòng HUMAN, tập thuộc tính X chỉ 212 dương tính. [dataset-audit.json](dataset-audit.json), sinh bởi [audit_dataset.py](audit_dataset.py).
- [ĐO] Tái tính MetaDegron-X được AUC **0,9670** bằng đọc cây số an toàn; **8/20** dương tính kiểm tra nằm trong bảng thuộc tính fitting được cung cấp. Đây không phải kết quả GPS. [safe-x-reproduction.json](safe-x-reproduction.json), [safe-predict-x.py](safe-predict-x.py).
- [ĐO] Theo cách sampling/split của script X, **91–111** dòng test mỗi fold có cùng tọa độ với train. Logistic thành phần cov80 khoảng **0,728–0,731**, ngữ cảnh 29 aa **0,737–0,747**; chưa đạt ngưỡng shortcut mạnh đăng ký trước. [composition-baseline.json](composition-baseline.json).
- [ĐO] Giao đúng vùng với bộ quét có footprint: **2 peptide**; bão hòa: **1** (map được 248/249); CRISPR: **0** (map đủ). Số này khác giao cùng protein và khác giao với tile. [overlap-audit.json](overlap-audit.json).
- [DIỄN GIẢI] “21 E3” là lựa chọn motif gắn với classifier dùng chung; dữ liệu không tự tạo ra 21 lớp E3 có nhãn độc lập. Sau lọc HUMAN, vùng trùng và cụm G2, chỉ **2 nhóm motif** còn ≥5 mẫu; lọc bảo thủ mọi protein tham chiếu còn **1**. [overlap-audit.json](overlap-audit.json), [mã/đánh giá](model-and-evaluation.md).
- [ĐỀ XUẤT] Định vị MetaDegron là công cụ bổ sung về motif/E3 và đối chiếu ứng dụng. Ưu tiên đường cong học, prior motif và tiền huấn luyện có kiểm soát; chưa nhập nhãn nhị phân vào thang ΔPSI. [Đề xuất và tiêu chí chốt](recommendations.md).

## Mục lục

- [Nguồn, phiên bản, quyền sử dụng và truy cập](source-inventory.md) · [manifest SHA-256](source-manifest.json) · [cây toàn repo](repository-tree.md).
- [Audit dữ liệu](dataset-audit.md) · [schema mọi bảng](table-schemas.md) · [kiểm nguồn mẫu](manual-label-review.md).
- [Ứng dụng và đầu ra](application-and-outputs.md) · [mô hình/đánh giá](model-and-evaluation.md) · [kiểm từng nhận định cũ](claims-verification.md).
- [So sánh và vị thế](comparison-and-positioning.md) · [khuyến nghị và tối đa năm prompt tiếp theo](recommendations.md).
- [Đăng ký trước](PREREGISTRATION.md) · [kiểm chéo](VALIDATION.md) · [kết quả kiểm](validation.json).

## Việc không làm được và vì sao

[CHƯA XÁC MINH] Chưa chạy MetaDegron-D trên GPS hoặc ma trận đột biến. SeqVec/embedding tải lớn có endpoint trả HTTP 200, **không được gọi là mất trọng số**; bản tải thử dừng ở giới hạn dung lượng của fetcher và không giữ payload. Runtime cũ TensorFlow/Keras/allennlp chưa có trong môi trường Python hiện tại; mã web và cấu hình checkpoint còn bất nhất cửa sổ. Nhánh X chỉ tái chạy được trên bảng đặc trưng đã chuẩn bị; các tài sản tạo đặc trưng cho protein/đột biến GPS chưa đầy đủ. [code-audit.json](code-audit.json), [source-manifest.json](source-manifest.json), [external-evaluation.json](external-evaluation.json).

[CHƯA XÁC MINH] Đã kiểm truy nguồn mẫu theo protocol, nhưng chưa phân xử đầy đủ thí nghiệm sinh học gốc cho mọi dòng; tỉ lệ nhãn degron sai để `null`. Trang bảng review gốc trả trang hạn chế ELTEnet; không coi HTTP 200 là truy cập được dữ liệu. [manual-label-review.json](manual-label-review.json), [source-manifest.json](source-manifest.json).

[ĐỌC-MÃ] Không gửi chuỗi lên server: Terms.php không có, liên kết chính sách bị 403; vì vậy không thực hiện bước phụ thuộc điều khoản chưa rõ. Chỉ tải trang/tài liệu và ảnh ví dụ sẵn có. [source-manifest.json](source-manifest.json).

## Đề xuất chỉnh sửa file hiện có

[ĐỀ XUẤT] Khi bạn duyệt, sửa `lectures/degron-basics/papers/metadegron-2024.md`: hạ cách gọi “đối thủ trực tiếp nhất”; thay nhận định âm ngẫu nhiên bằng sampled protein segments, tách split D/X, bổ sung HUMAN và nhãn nguồn; sửa mô tả “ghép XGBoost với DNN”, cập nhật kết quả tái tính và các giới hạn. Không sửa file đó trong phiên này.

[ĐỀ XUẤT] Đợt đồng bộ sau nên sửa định vị kiến trúc trong tài liệu lịch sử và tránh câu tuyệt đối về ứng dụng/mức residue. Báo cáo này không đổi `topic-decision.md`, slide, hay trạng thái G2. `data/README.md` được cập nhật theo yêu cầu sổ nguồn gốc.
