# Kiến trúc, đánh giá và tái lập

## MetaDegron có những mô hình nào?

[ĐỌC-MÃ] Hai nhánh sản phẩm là **MetaDegron-D** và **MetaDegron-X**. D dùng hai kiểu biểu diễn trình tự, ghép ở tầng dense; X dùng các thuộc tính thủ công. Mã web chọn X cho accession có trong danh sách tài sản thuộc tính, chọn D cho chuỗi khác. Không có bằng chứng trong mã cho một mạng ghép đầu ra XGBoost với DNN, hay vector E3 được đưa vào classifier. E3 lựa chọn quyết định regex nào được quét. [Mã prediction ghim](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Webserver/Degron_prediction.py), [code-audit.json](code-audit.json).

[ĐỌC-MÃ] **D, theo builder và JSON checkpoint**: đầu vào SeqVec/ELMo kích thước 29×1024; một nhánh Conv1D 128 filters, kernel 8, ReLU, max-pool 2; song song hai BiLSTM có 20 rồi 10 unit mỗi chiều. Nhánh sequence token có Embedding(input_dim=27, output_dim=10), BiLSTM 20 unit mỗi chiều. Mỗi nhánh chiếu Dense(20), LeakyReLU(0,01), flatten; concatenate → Dense(20) → LeakyReLU → Dense(1, sigmoid). [code-audit.json](code-audit.json) → `serialized_architecture_layers`, [Build_deep_learning_model.py](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Build_deep_learning_model.py).

[ĐỌC-MÃ] Alphabet gồm ký tự A–Z và dấu padding, được LabelEncoder sắp thứ tự; không phải one-hot 20 aa hoặc ESM. Embedding 27 là **số token**, không phải 27 chiều ở đầu ra. SeqVec là BLSTM/ELMo, không phải Transformer như vài mô tả marketing trên website. Elmo_embedder lấy trung bình các layer của SeqVec, giữ chiều residue. Không có vector E3 hoặc head riêng theo E3 trong builder. [AA_encoding.py](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/AA_encoding.py), [Elmo_embedder.py](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Elmo_embedder.py).

[ĐỌC-MÃ] Loss binary cross-entropy; Adam mặc định thư viện; nodes=20, dropout=0,5, batch=64, tối đa 100 epoch, patience=15 theo val_accuracy. Recurrent dropout lần lượt 0,2 và 0,5; L2 LSTM 10⁻⁶, dense 10⁻³; class weights balanced. CV dùng chính outer test của lượt đó làm `validation_data` cho early stopping/checkpoint: validation này không tách riêng khỏi fold dùng báo điểm. [Training_MetaDegron-D.py](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Training_MetaDegron-D.py), [code-audit.json](code-audit.json).

## Đúng mười đặc trưng X

| Thứ tự | Cột thật dùng train | Ý nghĩa và nguồn tác giả nêu |
|---|---|---|
| 1 | ASA_SCORE | [ĐỌC-MÃ] Mean solvent accessibility của đoạn; [NGUỒN] Spider2 |
| 2 | DSS_SCORE | [ĐỌC-MÃ] Mean disorder; [NGUỒN] IUPred |
| 3 | FCONS_SCORE | [ĐỌC-MÃ] Conservation tương đối với vùng flank; [NGUỒN] MSA ortholog/Gopher |
| 4 | COIL | [ĐỌC-MÃ] Cột coil trong bảng secondary structure; [NGUỒN] Spider2; bài gọi coiled-coil |
| 5 | ANCHOR_SCORE | [ĐỌC-MÃ] Binding stabilization/disorder interaction score; [NGUỒN] ANCHOR |
| 6 | nflanking_ptms | [ĐỌC-MÃ] Số PTM flank; [NGUỒN] EPSD phosphorylation |
| 7 | nflanking_ub_lysines | [ĐỌC-MÃ] Số lysine ubiquitination flank; [NGUỒN] PLMD |
| 8 | HELIX | [ĐỌC-MÃ] Mean alpha-helix probability; [NGUỒN] Spider2 |
| 9 | RIG_SCORE | [ĐỌC-MÃ] Rigidity/flexibility theo tên bảng; [NGUỒN] DynaMine |
| 10 | Domain_pfam | [ĐỌC-MÃ] Indicator đoạn giao miền cấu trúc; [NGUỒN] Pfam |

[ĐỌC-MÃ] Thứ tự được khóa trong `Training_MetaDegron-X.py` và phần predict X của notebook; [safe-x-reproduction.json](safe-x-reproduction.json) ghi lại danh sách. `CONS_SCORE` không nằm trong mười cột này dù dùng để lọc. `STRAND` xuất hiện trong danh sách **11 cột** của script web nhưng checkpoint được phân tích chỉ có **10 feature**. Không sửa lỗi đó trong nguồn tải về.

[CHƯA XÁC MINH] Chưa tái dựng pipeline sinh mọi thuộc tính gốc; tài sản per-protein và PTM/ortholog dùng ở web không đầy đủ trong repo. Không đánh đồng ASA_SCORE với rASA AlphaFold/DSSP, không đồng nhất secondary-structure coil với coiled-coil oligomerization, và không tự suy ra phép đảo thang RIG_SCORE. Tên/nguồn công cụ trên là mô tả tác giả cộng cách mã đọc cột, chưa phải tái lập vật lý của từng thuộc tính. [Toàn văn Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/), [code-audit.json](code-audit.json).

## Split và chỉ số công bố

[NGUỒN] Bài báo nêu 90% train/10% independent, CV 5 fold, AUROC/AUPRC/accuracy/recall/F1. X có mean CV 0,87, independent 0,86; D có mean CV 0,90, independent 0,90. X có ablation loại từng feature; so sánh bổ sung với Degpred trên β-TrCP. Chưa thấy bài dùng ELITE làm baseline; không biến tài nguyên liệt kê trong S1 thành mô hình đã được benchmark. [Methods/Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC11491831/).

[ĐỌC-MÃ] D permutation seed202310, holdout seed202309, StratifiedKFold seed202310. Chưa đặt đầy đủ seed TensorFlow/Python cho mọi tầng. `stratify=y` vẫn dùng vector trước permutation trong khi X/y1 đã permutation; không khẳng định holdout có cùng tỷ lệ lớp kỳ vọng nếu chưa đọc an toàn được object-NPY. X standalone chỉ CV toàn bộ bảng sau sampling có hoàn lại; notebook Figure 2 còn có holdout random10%, seed2023102. Không có GroupKFold/protein homology grouping trong các đoạn split đọc được. [code-audit.json](code-audit.json).

[ĐỌC-MÃ] X script dùng n_estimators=380, max_depth=40, learning_rate=0,01, min_child_weight=3, gamma=0,1, subsample≈0,7526, colsample_bytree≈0,66. Checkpoint đi kèm lại có **300 cây**, nên không mặc định script và checkpoint là cùng lần fit. Bài nói trung bình mười XGBoost bootstrap; repo được ghim chỉ có một classifier pickle, không xác nhận được mười mô hình đã ghép như mô tả. [Training_MetaDegron-X.py](https://github.com/BioDataStudy/MetaDegron/blob/ca12c0cf9d2e2d76655689973ac45c6c063a899d/Training_MetaDegron-X.py), [safe-x-reproduction.json](safe-x-reproduction.json).

| Vì sao khác thang | MetaDegron | G2 hiện hành |
|---|---|---|
| Nhãn dương | [NGUỒN] Curate degron vs background | [ĐỌC-MÃ] Thay thế làm ΔPSI ≥1 |
| Mẫu nhận điểm | [ĐỌC-MÃ] Motif/cửa sổ trong protein | [ĐỌC-MÃ] Vị trí × acid amin thay vào |
| Negative | [ĐỌC-MÃ] Background sampled, không xác nhận bất hoạt | [ĐỌC-MÃ] Các phép thay thế đo được dưới ngưỡng |
| Mức gộp AUROC | [ĐỌC-MÃ] Pool mẫu peptide | [ĐỌC-MÃ] Tính AUROC ô từng peptide, rồi macro |
| Split | [ĐỌC-MÃ] Random/stratified ở mã được cung cấp | [ĐỌC-MÃ] Outer protein cov80, inner group |
| Hệ đo | [DIỄN GIẢI] Hỗn hợp binding/degradation/PTM trong nhiều ngữ cảnh | [ĐỌC-MÃ] Reporter peptide GPS, continuous ΔPSI |

[DIỄN GIẢI] Không xếp AUC công bố 0,90 hay tái tính 0,9670 cạnh 0,8082 để kết luận công cụ nào mạnh hơn. Muốn cùng thang phải sinh điểm mutation trên cùng ô, cùng coverage, chiều điểm, fold và bootstrap như pre-registration.

## Đã tái lập được gì?

[ĐO] [safe-predict-x.py](safe-predict-x.py) đọc opcode pickle bằng `pickletools` để lấy **literal byte UBJSON**, không chạy GLOBAL/REDUCE/BUILD; bộ parser cục bộ giới hạn kích thước/độ sâu, chỉ sinh số, list và dict. Bộ tính cây tự viết cộng leaf score float32 rồi sigmoid. Không gọi `pickle.load`, không import XGBoost/mã nguồn tải về. Payload cây giải mã giữ dưới raw/derived bị gitignore. [safe-x-reproduction.json](safe-x-reproduction.json).

[ĐO] Trên **20 dương / pool733 âm**, mỗi repeat lấy 20 âm theo seed tác giả1–10: mean AUROC **0,9670000000000002**, sai lệch làm tròn so 0,9670 khoảng **2,2×10⁻¹⁶**. Seed audit17/29/43 cho mean **0,9375**; độ thay đổi này gắn với các tập âm rất nhỏ, không phải ba mô hình train khác nhau. Tái tính Degpred từ điểm sẵn có cũng đúng mean **0,9540**. [safe-x-reproduction.json](safe-x-reproduction.json), [composition-baseline.json](composition-baseline.json).

[ĐO] **8/20** dương tính β-TrCP có khóa accession/start/end trùng cả danh sách302 và bảng212 dùng fitting trong script X. Chưa có danh sách train thực tế của checkpoint để xác nhận từng dòng đã được fit, nhưng không thể gọi population này là independent sạch. [safe-x-reproduction.json](safe-x-reproduction.json).

[DIỄN GIẢI] Đây là tái lập **suy luận từ checkpoint trên bảng đặc trưng chuẩn bị sẵn và tái tính metric**, không tái lập từ FASTA→MSA/PTM/structure, không retrain và không kiểm chứng sinh học mới. Việc khớp từng repeat với S5 được kiểm ở [validation.json](validation.json).

## Phần ngoài nguồn và điểm mạnh/yếu

[CHƯA XÁC MINH] Zero-shot GPS và ΔScore mutation của D chưa chạy: runtime legacy và SeqVec chưa tái dựng, source web dùng49 residue trong khi JSON nhận29. X có thể chấm bảng10 feature nhưng chưa có đặc trưng mutant hợp lệ cho GPS. Header accession giữ nguyên có thể khiến web dùng thuộc tính protein snapshot, không phản ánh chuỗi mutant mới. Không dùng trạng thái “không có regex hit” làm score0. [external-evaluation.json](external-evaluation.json), [PREREGISTRATION.md](PREREGISTRATION.md).

[DIỄN GIẢI] Điểm mạnh: có source/checkpoint nhỏ, thông tin nguồn và motif, nhánh D dùng sequence, nhánh X có PTM/conservation/structure; score X chuẩn bị sẵn tái tính khớp. Điểm yếu ở phiên bản kiểm: dòng curated ít và thiên motif; không có negatives thực nghiệm theo E3; rò rỉ duplicate ở split script X; tập được gọi independent có giao population; route X/D và phiên bản mã/checkpoint chưa đồng nhất. Không suy từ các điểm yếu này rằng mọi kết quả bài báo sai hoặc mọi nhãn curate kém sạch hơn GPS.

[ĐỀ XUẤT] PLM đóng băng, đa nhiệm và calibration là phương án cần kiểm; không phải lợi ích đã chứng minh của MetaDegron trên G2. Cổng/FiLM/bilinear của đề tài đã không thắng ridge ổn định; không dùng tên mô hình mới để thay bằng chứng. [comparison-and-positioning.md](comparison-and-positioning.md), [recommendations.md](recommendations.md).
