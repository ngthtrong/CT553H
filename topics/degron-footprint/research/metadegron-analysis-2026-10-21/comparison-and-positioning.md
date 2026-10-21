# Đối chiếu và vị thế đề tài

[ĐO] Các số MetaDegron bên dưới đến từ [dataset-audit.json](dataset-audit.json), [composition-baseline.json](composition-baseline.json), [overlap-audit.json](overlap-audit.json), [safe-x-reproduction.json](safe-x-reproduction.json); script sinh kết quả ghi trong từng JSON. Số đề tài được đọc lại từ [current-topic-evidence.json](current-topic-evidence.json). Đây không phải hai benchmark cùng nhãn.

| Khía cạnh | MetaDegron ở phiên bản ghim | Degron-footprint hiện tại |
|---|---|---|
| Bài toán | [ĐỌC-MÃ] Xếp hạng motif ứng viên qua classifier binary dùng chung | [ĐỌC-MÃ] Dự đoán ảnh hưởng phép thay acid amin lên reporter |
| Đơn vị | [ĐỌC-MÃ] Một hit motif/cửa sổ, gắn E3 qua mapping | [ĐỌC-MÃ] Một ô position×replacement |
| Nguồn nhãn | [NGUỒN]/[ĐO] ELM và y văn, nguồn S2 có PMID | [ĐỌC-MÃ] GPS scanning/saturation Zhang, liên tục |
| Cỡ nhãn | [ĐO] 302 dòng, 240 accession; X 212; 227 dòng HUMAN | [ĐO] 2.624 footprint lịch sử; G2: 91 peptide/89 cụm/47.847 ô |
| Âm | [ĐỌC-MÃ] Sampled protein segments, có hoàn lại ở script X | [ĐỌC-MÃ] Ô đã đo ΔPSI dưới ngưỡng; không là “không có degron” |
| Độ phân giải | [ĐỌC-MÃ] Motif có tọa độ, không có nhãn mutant theo residue | [ĐỌC-MÃ] Mutation cell; có thể gộp mức vị trí |
| E3 | [ĐO]/[ĐỌC-MÃ] 21 lựa chọn, không có 21 head; dữ liệu có 31 motif classes | [ĐO] 10 adaptor/E3, chỉ 1 có ≥5 peptide; ca nghiên cứu |
| Split | [ĐỌC-MÃ] Random/StratifiedKFold; D có 10% holdout; X script có duplicate leakage | [ĐỌC-MÃ] GroupKFold protein id30/cov80, inner group; cov50 nhạy |
| Metric | [NGUỒN]/[ĐO] AUROC peptide; X tái tính 0,9670 trên β-TrCP | [ĐO] AUROC ô macro peptide: ridge 0,8082, ΔPAP 0,7693; không đối chiếu trực tiếp |
| Kiến trúc | [ĐỌC-MÃ] D: SeqVec/CNN/BiLSTM/token embedding; X: 10 thuộc tính | [ĐO]/[ĐỌC-MÃ] Ridge M3 mạnh; gate/FiLM/bilinear chưa thắng ổn định |
| Cấu trúc | [ĐỌC-MÃ] ASA/disorder/secondary structure vào X; MSA/PTM/domain | [DIỄN GIẢI] Exposure gate là giả thuyết, không đóng góp đã xác nhận |
| Tái lập | [ĐO] Đã khớp score-metric X chuẩn bị sẵn; pipeline D/feature chưa dựng lại | [ĐO] Có input/prediction/script/JSON G2; pretrained Degformer còn vấn đề overlap |
| Ứng dụng | [ĐỌC-MÃ]/[NGUỒN] FASTA batch, tree E3, hit, cấu trúc/MSA/mạng, export | [ĐỀ XUẤT] Bản đồ mutation, provenance, uncertainty, API; chưa chứng nhận đủ G3 |

## Đối thủ trực tiếp hay công cụ bổ sung?

[DIỄN GIẢI] MetaDegron cạnh tranh về điểm tiếp xúc người dùng: cùng bắt đầu từ protein/peptide, trả ứng viên degron và có web. Vì vậy “có web” hoặc “dùng PLM/cấu trúc” không tạo vị thế đủ mạnh. Nhưng classifier binary trên motif không được huấn luyện bằng experimental ΔPSI cho từng phép thay; nó là công cụ bổ sung và **baseline chuyển giao tiềm năng** cho nhiệm vụ này. Muốn trở thành đối thủ trực tiếp về dự đoán mutation, cần đánh giá `−ΔScore` trên cùng ô G2 và xử lý abstention; phép đó hiện chưa chạy. [PREREGISTRATION.md](PREREGISTRATION.md).

[DIỄN GIẢI] Không dùng lập luận “MetaDegron không có residue” làm ranh giới duy nhất: motif đã có tọa độ, Degpred có score residue và Degformer đã cho mutation map. Cái có thể bảo vệ ở đề tài là **nguồn nhãn, cách đánh giá, kiểm rò rỉ, baseline mạnh và mức hữu ích của công cụ**, trong phạm vi đã đo. Đây không chứng minh không có tiền lệ toàn lĩnh vực.

## Hai điểm mới ở topic-decision.md §5 còn đứng thế nào?

| Tuyên bố lịch sử | Điều audit MetaDegron xác nhận | Quyết định diễn giải trong báo cáo này |
|---|---|---|
| Exposure gate ở pooling thay đầu vào | [ĐỌC-MÃ] MetaDegron X có exposure/disorder ở input; chưa thấy gate pooling như đề xuất | [DIỄN GIẢI] Khác vị trí đặt không đủ chứng minh mới/có lợi. G2 gate đảo dấu theo seed; không tuyên bố gate giải quyết peptide–protein gap |
| Giám sát attention bằng mutation labels | [ĐỌC-MÃ] Không thấy nhánh attention-supervision đó trong MetaDegron | [DIỄN GIẢI] Chỉ chưa có trong mã được kiểm. Attention và mutation effect khác đối tượng; cần ablation fidelity và task benefit, chưa nhận là đóng góp đã có |

[DIỄN GIẢI] Bài [contribution-assessment-2026-10-15.md](../contribution-assessment-2026-10-15.md) có những câu đã cũ trước benchmark 18/10: nay ridge đã vượt ΔPAP về mốc số. Điều này **không phục hồi tính mới kiến trúc**; phần cảnh báo về Degformer, nguồn nhãn và không dùng uncertainty/provenance như lời hứa đã xong vẫn có ích. Khối trạng thái 21/10 trong topic-decision được ưu tiên khi hai tài liệu mâu thuẫn. Báo cáo này không sửa quyết định hoặc nội dung lịch sử.

## Câu hỏi hội đồng và cách trả lời có kiểm chứng

| Câu hỏi | Cách trả lời và giới hạn |
|---|---|
| Họ đã làm 21 E3, sao em chỉ 10? | [ĐO]/[ĐỌC-MÃ] Có 21 lựa chọn motif nhưng classifier dùng chung. Sau lọc còn 2 nhóm motif ≥5 mẫu dưới điều kiện G2; chưa có nhãn E3 độc lập cho các nhóm chia sẻ mẫu. Không dùng số menu làm số lớp có thể học. [overlap-audit.json](overlap-audit.json) |
| AUC 0,90/0,967 cao hơn em? | [DIỄN GIẢI] Khác nhãn/đơn vị/gộp; 0,967 đã tái tính được nhưng 8/20 dương có trong fitting population. Trả lời bằng bảng thang đo và đề xuất mutation-transfer, không chê số của họ để tự nâng mình |
| Nhãn của họ sạch hơn nhãn của em? | [ĐO]/[DIỄN GIẢI] Curate có provenance, nhưng nguồn/assay/loài pha trộn; mẫu 40 chỉ chốt 22 dòng có lineage ELM, không có biological error rate. GPS đo trực tiếp nhưng reporter và nhiễu. Chọn nhãn theo endpoint thay vì tuyên bố một bộ “sạch” toàn diện |
| Kiến trúc em mới ở đâu? | [ĐO]/[DIỄN GIẢI] Chưa có component mới thắng ridge ổn định; trình bày phát hiện, benchmark, baseline và phần ứng dụng thật sự đã kiểm. Learning curve/weak pretraining là câu hỏi còn mở |
| Tại sao cần thêm web? | [ĐỀ XUẤT] Chứng minh người dùng chọn được phép thay và controls từ matrix/provenance/uncertainty, tái xuất được kết quả. Không dùng PDB/network đẹp để thay đánh giá hữu dụng |

[ĐỀ XUẤT] Câu trình bày đề tài: “Em dự đoán ảnh hưởng của từng phép thay acid amin lên độ bền reporter bằng nhãn đột biến thực nghiệm và đánh giá theo cụm protein. MetaDegron bổ sung motif/E3 và annotation; kiểm tra chuyển giao score của nó sang ΔPSI là một thí nghiệm riêng. Hiện ridge là baseline mạnh và tính mới kiến trúc chưa được chứng minh.” Không thêm mệnh đề độc quyền nhiệm vụ.
