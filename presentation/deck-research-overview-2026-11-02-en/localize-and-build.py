"""Build the English edition from the Vietnamese source without changing it.

Run from the repository root. Requires the same Python plotting dependencies as
the original edition. All fonts, scripts and images are copied from that edition.
"""
from pathlib import Path
import ast
import hashlib
import json
import re
import runpy
import shutil

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.with_name('deck-research-overview-2026-11-02')

# Translation happens before diagram labels are wrapped and figures are drawn.
# Tabs separate original text and English copy. Statistical values are unchanged.
COPY = r'''
Sơ đồ minh họa	Schematic illustration
Ma trận nhãn đo HIF1A dùng làm hình mở đầu	Measured HIF1A mutation effects used as the opening image
Từ trình tự đến bản đồ hiệu ứng	From sequence to a map of effects
Minh họa đo lặp và kiểm độ tin cậy	Repeated measurements and label reliability
Hai hướng nghiên cứu và phát triển công cụ được thực hiện theo điều kiện phụ thuộc	Research and software development follow their respective dependencies
Ba nội dung trao đổi với giảng viên	Three topics for discussion with the lecturer
Một phép thay tại một vị trí tạo một ô trong ma trận hiệu ứng	One substitution at one position corresponds to one matrix cell
Minh họa nguyên lý nhận diện degron, gắn ubiquitin và phân hủy protein	Schematic of degron recognition, ubiquitination and protein degradation
Chỉ số độ bền reporter	Reporter stability index
Minh họa reporter, phân bin và chỉ số PSI; histogram chỉ minh họa nguyên lý	Reporter, sorting bins and PSI; the histogram is schematic
Ưu tiên để kiểm chứng	Prioritize for experiments
Sơ đồ ưu tiên một số phép thay theo ngân sách thí nghiệm; không phải số dự đoán cụ thể	Schematic prioritization under an experimental budget; no model scores are shown
Sơ đồ thiết kế scanning và saturation; ô xanh biểu thị loại phép thay được khảo sát	Scanning and saturation designs; green cells indicate assayed substitution types
PSI từng lần đo	PSI per replicate
Hiệu ứng ΔPSI	Effect: ΔPSI
QC rồi giữ ô hợp lệ	QC retains valid cells
Tái dựng nhãn với mốc WT đúng theo từng thiết kế thí nghiệm	Reconstructing labels with the appropriate WT reference for each assay
Bốn nguồn dữ liệu độc lập, mỗi nguồn có một vai trò khác nhau	Four distinct data sources with different roles
Giữ nguyên nhóm protein	Keep protein groups intact
Train và validation	Training and validation
Fit / chọn tham số trong phần này	Fit and tune here
Nhóm kiểm tra ngoài	Outer test groups
Chỉ dùng đánh giá	Evaluation only
Nhóm protein được giữ nguyên khi chia train, validation và nhóm kiểm tra ngoài	Protein groups remain intact across training, validation and outer test sets
Cửa sổ ngữ cảnh quanh vị trí đột biến	A local context window around the mutation site
Các bộ lọc tích chập quét qua representation	Convolution filters scan the representation
Đánh giá miền dẫn đến dự đoán hoặc cảnh báo phù hợp	Domain assessment determines the appropriate prediction or warning
Kiểm tra yêu cầu / điều phối	Validation / orchestration
Phiên bản / phạm vi	Version / scope
Nguồn / annotation / snapshot	Sources / snapshot
Kiến trúc ứng dụng local và nguồn gốc kết quả	Local application architecture and result provenance
Sai số, xếp hạng và ưu tiên thí nghiệm là ba mục tiêu đánh giá khác nhau	Error, ranking and experimental prioritization are distinct evaluation goals
Hiệu ứng đột biến degron ở mức residue	Degron mutation effects at residue level
Degron tham gia quá trình phân hủy protein	Degrons participate in protein degradation
Một phép thay amino acid có thể làm thay đổi tín hiệu nhận diện.	An amino acid substitution can alter the recognition signal.
Một phép thay tạo một ô trong bản đồ hiệu ứng	One substitution corresponds to one cell in the effect map
Đầu vào: trình tự WT, vị trí và amino acid thay vào. Đầu ra: ΔPSI.	Input: WT sequence, position and replacement amino acid. Output: ΔPSI.
GPS chuyển tín hiệu reporter thành nhãn ΔPSI	GPS converts reporter measurements into ΔPSI labels
Dương: reporter bền hơn trong assay.	Positive: a more stable reporter in this assay.
Ví dụ HIF1A cho thấy hiệu ứng tập trung theo vị trí	HIF1A illustrates position-specific mutation effects
Cùng một peptide, những vị trí khác nhau phản ứng rất khác với đột biến.	Within one peptide, mutation effects differ substantially across positions.
Giá trị sử dụng là ưu tiên đột biến để kiểm chứng	The practical goal is to prioritize mutations for experiments
Ma trận → danh sách ưu tiên → thí nghiệm xác nhận.	Effect map → shortlist → experimental validation.
Công trình liên quan trả lời các câu hỏi khác nhau	Related approaches address different questions
Trọng tâm: bằng chứng dự đoán và đánh giá, cùng công cụ hỗ trợ phân tích.	Focus: predictive evidence, evaluation and a useful analysis tool.
Ba mục tiêu nối nghiên cứu với công cụ	Three objectives connect research to an analysis tool
Phạm vi chính: hiệu ứng đột biến đơn trên reporter peptide 28 amino acid.	Main scope: single-substitution effects in 28-residue reporter peptides.
Các câu hỏi đang dẫn dắt hướng nghiên cứu	Questions guiding the current research
Mỗi câu hỏi được kiểm bằng phép so phù hợp và giới hạn suy luận rõ ràng.	Each question needs an appropriate comparison and clear limits of inference.
Nguồn dữ liệu được dùng đúng vai trò	Each data source serves a defined role
Nguồn mức tile và annotation không tự trở thành nhãn mutation.	Tile-level scores and annotations are not mutation-effect labels.
Hai thiết kế đột biến có độ phủ bổ sung	The two mutation designs provide complementary coverage
Scanning mở rộng ngữ cảnh; saturation kiểm được đầy đủ các kiểu thay thế.	Scanning expands context coverage; saturation covers all substitution types.
Mốc WT phải phù hợp với từng thí nghiệm	Each assay needs the correct WT reference
Giữ riêng nguồn, điều kiện và replicate trước khi tạo nhãn hiệu ứng.	Keep sources, conditions and replicates separate when deriving effect labels.
Độ lặp lại của nhãn đặt giới hạn cho cách đọc kết quả	Label reproducibility constrains how results should be interpreted
Phần dư sau mô hình có thể chứa cả tín hiệu và nhiễu đo.	Model residuals can contain both signal and measurement noise.
Chia theo nhóm protein để kiểm khả năng tổng quát hóa	Split by protein group to assess generalization
Miền hẹp: 91 peptide. Toàn dải: 235 peptide thuộc 221 nhóm protein.	Restricted domain: 91 peptides. Full range: 235 peptides in 221 protein groups.
Sai số, xếp hạng và ngân sách thí nghiệm là các mục tiêu riêng	Prediction error, ranking and experimental budget are distinct goals
Tính theo peptide; khoảng tin cậy lấy mẫu lại theo nhóm protein.	Compute metrics per peptide; bootstrap confidence intervals by protein group.
Ngữ cảnh cục bộ bổ sung thông tin ngoài phép thay	Local context adds information beyond the substitution itself
Đây là lý do cần baseline ngữ cảnh trước khi thử mô hình phức tạp.	A context baseline is essential before adding model complexity.
Học toàn dải PSI giảm sai số hồi quy của Ridge	Training across the PSI range reduces Ridge regression error
Cải thiện có bằng chứng; mức giảm tối thiểu 0,02 PSI chưa được bảo đảm trên toàn CI.	Error improves, but the adjusted interval does not establish a minimum 0.02 PSI reduction.
Lợi ích toàn dải tập trung ở miền PSI cao	Full-range training benefits high-PSI peptides most
Chọn phân bố train cần xét cả mục tiêu toàn tập và miền sử dụng.	Choose the training distribution for both the overall objective and the intended domain.
ESM bổ sung tín hiệu cho baseline ngữ cảnh	ESM adds signal to the context baseline
Trong benchmark toàn dải, mới ESM2-35M có kết quả; chưa kết luận được họ pLM tốt nhất.	Only ESM2-35M was evaluated on the full-range benchmark; pLM families cannot yet be ranked.
CNN cải thiện thêm sau representation ESM	A CNN adds value after the ESM representation
Phép so cùng đầu vào hỗ trợ giá trị trộn vị trí; kết quả one-hot còn chưa phân giải.	The matched-input comparison supports position mixing; one-hot results remain unresolved.
Nhiều cửa sổ chưa chứng minh vượt một cửa sổ	Multiple windows have not shown a clear advantage over one
Đứng đầu MAE trong bảng development chưa đủ để chốt ứng viên.	The best development MAE alone is insufficient to select a final model.
Học tốt nhãn tile chưa bảo đảm chuyển sang mutation effect	Learning tile scores well does not guarantee mutation-effect transfer
Kết quả âm giới hạn một thiết kế chuyển giao cụ thể, không bác bỏ mọi cách tiền huấn luyện.	The negative result applies to the tested transfer design, not to all pretraining strategies.
Scanning pretrain có lợi cả ngoài các kiểu thay đã thấy	Scanning pretraining helps beyond the observed substitution types
Quality weighting hiện làm tăng sai số; trung bình replicate chưa hơn rep1 rõ ràng.	Quality weighting increases error; averaging replicates has no clear advantage over replicate 1.
Đối chiếu Degformer cần kiểm cả chồng mẫu và ngân sách nhãn	Degformer comparisons require overlap and training-data audits
Retrain sạch cụm đạt AUROC 0,8068; chưa có bằng chứng vượt Ridge trên phép so này.	Group-clean retraining reaches AUROC 0.8068, with no demonstrated advantage over Ridge.
Xếp hạng giúp tập trung ngân sách vào đột biến đáng thử	Ranking focuses the experimental budget on promising substitutions
Đây là khả năng ưu tiên thí nghiệm, chưa phải xác suất đã được hiệu chuẩn.	This demonstrates prioritization utility, not calibrated probabilities.
Độ ổn định và chi phí cùng tham gia lựa chọn mô hình	Model selection also depends on stability and cost
Ensemble giúp giảm phương sai; seed và fold không phải các bộ dữ liệu độc lập.	Ensembling reduces variance; seeds and folds are not independent datasets.
Hiệu chuẩn nối điểm hồi quy với xác suất sự kiện	Calibration maps regression scores to event probabilities
Bằng chứng hiệu chuẩn thuộc model đã kiểm; CNN mới cần quy trình hiệu chuẩn riêng.	Calibration evidence belongs to the tested model; the CNN needs its own calibration procedure.
Miền áp dụng cần được đánh giá cùng với dự đoán	Assess the applicability domain alongside predictions
PSI giữa các nguồn đo khác nhau; mô hình học peptide chưa xác nhận hiệu ứng protein nguyên vẹn.	PSI differs across sources; a peptide model does not establish whole-protein effects.
Công cụ đưa ma trận và danh sách ưu tiên vào cùng một luồng	The tool combines the effect map and shortlist in one workflow
Nhập peptide → xem ma trận → chọn phép thay → chú giải → xuất kết quả.	Enter a peptide → inspect the map → select substitutions → annotate → export.
Một ứng dụng local giữ kết quả cùng nguồn gốc	A local application keeps results with their provenance
Mỗi kết quả đi cùng phiên bản model, nguồn dữ liệu và phạm vi sử dụng.	Each result carries its model version, data sources and intended scope.
Phần mềm có nền tảng để tiếp tục mở rộng	The software baseline provides a foundation for extension
Các kiểm thử baseline được giữ đúng phạm vi; chức năng mở rộng cần kiểm chứng riêng.	Baseline tests retain their original scope; extensions require separate verification.
Những gì đã thực hiện tạo nền tảng cho hướng nghiên cứu	Completed work provides a foundation for the next research steps
Đã có kết quả development đáng chú ý và các giới hạn đủ rõ để chọn bước tiếp theo.	Development findings and explicit limitations now guide the next steps.
Ưu tiên tiếp theo là khóa lựa chọn và kiểm chứng khả năng chuyển giao	Next priorities: lock the model choice and evaluate transfer
LoRA và cấu trúc là các nhánh cân nhắc theo câu hỏi và nguồn lực.	LoRA and structure remain optional branches, guided by the question and available resources.
Trao đổi về hướng nghiên cứu và bước tiếp theo	Discussion: research direction and next steps
Cách đọc các thuật ngữ trong bài toán	Terminology and how to read the metrics
Residue: amino acid tại một vị trí. WT: trình tự tham chiếu. OOF: dự đoán ngoài fold.	Residue: an amino acid at a position. WT: reference sequence. OOF: out-of-fold predictions.
Chi tiết tạo nhãn và kiểm chất lượng	Label construction and quality-control details
Đồng nghĩa dùng làm WT nội tại; ô thiếu được mask; điều kiện đo được giữ riêng.	Synonymous constructs provide intrinsic WT references; missing cells are masked and conditions kept separate.
Độ tin cậy phụ thuộc mức phân tích	Reliability depends on the level of analysis
Các cohort và mức vị trí/ô khác nhau; không diễn giải như phép so ghép cặp.	Cohorts and position/cell definitions differ; this is not a paired comparison.
Mô hình composition không phân biệt mọi vị trí	Composition models cannot distinguish every position
Trong cùng peptide, cùng cặp thay thế nhận cùng score nếu đầu vào chỉ có thành phần.	Within a peptide, a composition-only model assigns the same score to the same substitution type.
Learning curve cần tách model đơn và ensemble	Learning curves must distinguish individual models from ensembles
Độ nhạy phân cụm là phép kiểm riêng; không đếm phân hoạch trùng nhau như bằng chứng mới.	Clustering sensitivity is a separate check; identical partitions are not additional evidence.
Các thiết kế tương tác chưa vượt baseline ổn định	The tested interaction designs did not consistently beat the baseline
Đây là những thiết kế đã thử, không phải phủ định mọi tương tác phi tuyến.	These results concern the tested designs, not all possible nonlinear interactions.
Lọc trùng mức ô chưa loại được chồng mức peptide	Removing duplicate cells does not remove peptide-level overlap
Cần đánh giá theo peptide/nhóm protein được giữ riêng.	Evaluate on held-out peptides or protein groups.
Khảo sát cỡ ESM thuộc các thiết kế riêng	ESM scale comparisons belong to a separate evaluation design
Không so trực tiếp bảng này với AUROC của benchmark toàn dải.	Do not directly compare these AUROCs with the full-range benchmark.
Đọc nhiều tiêu chí trên cùng các ứng viên	Inspect several metrics for the same candidates
Các điểm là ensemble dự đoán ba seed; vẫn là phân tích development.	Scores use mean predictions from three seeds and remain development analysis.
Scanning transfer: tách các kiểu thay thế để kiểm chuyển giao	Scanning transfer: assess observed and remaining substitution types
Cohort 20 có 6.433 ô; cohort 360 có 115.979 ô. Cùng 235 peptide.	The 20-type cohort has 6,433 cells; the 360-type cohort has 115,979 cells. Both cover 235 peptides.
ClinVar hỗ trợ động lực ở mức vùng, chưa xác nhận mức residue	ClinVar supports region-level motivation, not residue-level validation
ClinVar phục vụ bối cảnh và annotation, không là ground truth ΔPSI.	ClinVar provides context and annotation, not ΔPSI ground truth.
Nhãn E3 chưa đủ cho nhiệm vụ có điều kiện E3	E3 labels are too sparse for an E3-conditioned task
Chỉ một nhóm có ít nhất năm peptide; không dùng số E3 trong menu thay cho số lớp có thể học.	Only one group has at least five peptides; menu choices are not learnable class counts.
Nguồn ngoài cần được đánh giá theo endpoint và khả năng sử dụng	External sources need endpoint and usability audits
Khảo sát nguồn không đồng nghĩa đã có kết quả kiểm chứng ngoài cho model hiện tại.	Auditing a source does not establish external validation of the current model.
Calibration và domain gate trả lời hai câu hỏi khác nhau	Calibration and domain assessment answer different questions
Cả hai cần được kiểm lại khi đổi model hoặc thay phạm vi dữ liệu.	Reassess both when the model or data scope changes.
Tính tái lập nối dữ liệu, model và kết quả phục vụ	Reproducibility connects data, models and served results
Đã đối chiếu 2.986 file theo manifest; kiểm thử app nền không nghiệm thu chức năng mới.	The manifest verified 2,986 files; baseline app tests do not validate new features.
Tài liệu và bằng chứng có thể tra cứu theo chủ đề	References and evidence are organized by topic
Mở “Ghi chú” để xem nguồn và giới hạn của slide đang trình bày.	Open Notes for the current slide's sources and interpretation limits.
Quy trình: 	Process:
Trình tự tham chiếu	Reference sequence
Thay P bằng D	Replace P with D
Tại vị trí 12	At position 12
Một phép thay	One substitution
một ô hiệu ứng	one effect-map cell
Nhận diện	Recognition
và gắn ubiquitin	and ubiquitination
Đo tỷ lệ huỳnh quang	Fluorescence ratio
Phân vào sáu bin	Sort into six bins
Nhiều phép thay có thể thử	Many substitutions to test
Một phép thay ở mỗi vị trí	One substitution per position
20 kiểu WT → mutant	20 WT-to-mutant types
Nhiều phép thay ở mỗi vị trí	Many substitutions per position
380 kiểu WT → mutant	380 WT-to-mutant types
WT đo trực tiếp	Measured WT
WT từ ô đồng nghĩa	WT from synonymous cells
Nhãn mutation	Mutation labels
Trình tự / nhóm	Sequences / groups
Chú giải	Annotations
Cùng phép thay	Same substitution
ngữ cảnh lân cận có thể khác	local contexts may differ
Dự đoán ΔPSI	Predict ΔPSI
Học head trên nhãn mutation	Train the mutation head
Nhãn tile	Tile labels
Hoạt tính cả đoạn	Whole-tile activity
Hiệu ứng phép thay	Substitution effects
Tiền huấn luyện	Pretraining
Học tốt nhiệm vụ tile	Learns the tile task well
Tinh chỉnh	Fine-tuning
Peptide đầu vào	Input peptide
Trong miền	In domain
Giáp ranh	Borderline
Ngoài miền	Out of domain
Nhập / xem / xuất	Input / inspect / export
và model card	and model card
Dữ liệu local	Local data
và provenance	and provenance
Peptide gắn	Peptide-linked
Giao diện	Interface
Sai số	Error
Xếp hạng	Ranking
Ưu tiên thử nghiệm	Experimental priorities
Nguồn truy vết	Evidence sources
Mỗi ô là một phép thay	One substitution per cell
Heatmap ΔPSI thực nghiệm của peptide HIF1A	Measured ΔPSI heatmap for the HIF1A peptide
Hướng tiếp cận	Approach
Đối tượng chính	Main target
Liên hệ với đề tài	Role in this project
Đo lần thứ nhất	First measurement
Đo lần thứ hai	Second measurement
Độ tin cậy mức peptide khác với độ tin cậy từng vị trí.	Peptide-level reliability differs from position-level reliability.
Ablation giá trị ngữ cảnh trên scanning	Context ablation on scanning data
Phần lớn lợi ích	Most of the gain
đến từ thành phần của vùng lân cận.	comes from local amino acid composition.
Giữ thêm thứ tự có lợi nhỏ hơn.	Retaining order adds a smaller benefit.
MAE của Ridge theo miền PSI train	Ridge MAE by the training PSI range
Chênh MAE:	MAE difference:
CI điều chỉnh:	Adjusted CI:
MAE của ba cách train trên bốn miền PSI	MAE across four PSI strata for three training distributions
Miền PSI cao được cải thiện rõ hơn.	High-PSI peptides benefit more.
Cân bằng dữ liệu	Balancing the data
có thể đánh đổi chất lượng miền PSI thấp.	can trade off performance in the low-PSI domain.
AUROC dương Ridge ngữ cảnh, Ridge với ESM và nested selection	Positive-event AUROC for context Ridge, ESM features and nested selection
ESM-only và context+ESM có đánh đổi giữa MAE và xếp hạng.	ESM-only and context-plus-ESM trade off MAE against ranking.
Chọn bằng validation	Validation-based selection
đánh giá một quy trình lựa chọn.	evaluates a selection procedure.
MAE của head one-hot và ESM trên train toàn dải	MAE of one-hot and ESM heads trained across the full PSI range
So với pointwise:	Compared with pointwise:
MAE giảm 0,00534 PSI.	MAE decreases by 0.00534 PSI.
MAE CNN scratch và CNN pretrain scanning	MAE of scratch and scanning-pretrained CNNs
20 kiểu đã có:	20 observed types:
MAE giảm 0,00772.	MAE decreases by 0.00772.
360 kiểu còn lại:	360 remaining types:
MAE giảm 0,00631.	MAE decreases by 0.00631.
Đối chiếu Degformer retrain sạch cụm và Ridge trên cùng 91 peptide	Group-clean Degformer and Ridge evaluated on the same 91 peptides
Che ô trùng chưa tạo thành peptide chưa thấy.	Masking duplicate cells does not create unseen peptides.
Precision dương theo ngân sách top-k so Ridge và ESM CNN	Positive-event precision by top-k budget for Ridge and the ESM CNN
Ridge ngữ cảnh:	Context Ridge:
Phía âm vẫn khó hơn; cần đọc cùng độ hiếm sự kiện.	Negative events remain harder; consider their lower prevalence.
MAE Ridge và CNN ESM qua năm nhóm kiểm tra ngoài	Ridge and ESM CNN MAE across five outer folds
task đã hoàn tất.	of completed task time.
Hai task frozen chiếm 7,23 giờ.	The two frozen tasks account for 7.23 hours.
LoRA chưa có OOF hoàn chỉnh.	LoRA has no complete OOF results yet.
Đã có nền tảng	Implemented baseline
Đang phát triển / cần tích hợp	In development / integration needed
Mức độ phát triển công cụ	Software scope
Đại lượng	Measure
MAE trung bình seed theo tỷ lệ nhóm train	Mean single-seed MAE by the fraction of training groups
Thiết kế	Design
AUROC trên miền 91 peptide	AUROC on the 91-peptide domain
Cách đọc	Interpretation
Degformer retrain sạch cụm so đối chứng	Group-clean Degformer retraining and baselines
Biểu diễn Ridge bổ sung	Additional Ridge representation
AUROC · miền 91 peptide	AUROC · 91-peptide domain
Kết luận	Finding
CI lợi ích scanning trên 20 và 360 kiểu thay thế	Confidence intervals for scanning transfer across 20 and 360 substitution types
Đã phân tầng theo protein.	Stratified by protein.
Mắt nối ΔPSI với bệnh ở mức residue chưa được thiết lập.	A residue-level link between ΔPSI and pathogenicity has not been established.
Số peptide trong audit	Peptides in the audit
Giá trị khảo sát	Potential use
Giới hạn	Limitations
Vùng	Region
nổi bật trong bản đồ.	stands out in the measured map.
Nhãn thực nghiệm, không phải dự đoán	Measured labels, not predictions
Hoạt tính cả peptide	Whole-peptide activity
Lấy chênh điểm khi thay amino acid	Score difference after a substitution
PSI từ trình tự	PSI from sequence
Đã có ma trận hiệu ứng đột biến	Already provides mutation-effect maps
Motif / ứng viên degron	Motifs / candidate degrons
Bổ sung chú giải và ngữ cảnh E3	Adds annotations and E3 context
Đề tài hiện tại	This project
Hiệu ứng từng phép thay	Effects of individual substitutions
Nhãn đo + đối chứng + đánh giá theo nhóm	Measured labels, baselines and group-based evaluation
Dữ liệu có truy vết	Traceable data
Phương pháp được kiểm	Evaluated methods
Tái dựng và kiểm chất lượng	Reconstruction / QC
Đối chứng / độ ổn định	Baselines / stability
Ma trận / ranking / export	Effect map / ranking / export
Phân bố nhãn	Label distribution
Ngữ cảnh và ESM	Context and ESM
Đầu mô hình	Prediction head
Chuyển nguồn	Source transfer
Giá trị sử dụng	Practical utility
Nên học miền nào?	Which training domain?
Thông tin nằm ở đâu?	Where is the signal?
Cần tích chập không?	Does convolution help?
Có học thêm được?	Can transfer help?
Hữu ích và đáng tin?	Useful and reliable?
tương quan ΔPSI giữa hai nửa saturation	correlation of ΔPSI across the two saturation halves
Đánh giá trên scanning	Evaluation on scanning
giảm MAE: toàn dải so với chỉ PSI ≤ 4	lower MAE: full range versus training only at PSI ≤ 4
CI chênh lệch MAE giữa nhiều cửa sổ cân bằng và CNN toàn dải	MAE-difference CI: balanced multi-window model versus full-range CNN
AUROC sau tiền huấn luyện tile	AUROC after tile pretraining
cùng encoder, khởi tạo ngẫu nhiên	same encoder, random initialization
CI mô tả đều ở phía cải thiện	Both descriptive CIs favor improvement
WT peptide có trong train của checkpoint công bố	WT peptides seen in the published checkpoint's training data
precision dương khi chọn top 5%	positive-event precision in the top 5%
peptide có MAE tốt hơn Ridge	peptides with lower MAE than Ridge
Ridge trên miền đánh giá 91 peptide	Ridge evaluated on the 91-peptide domain
Đường reliability của Ridge với Platt	Reliability plot for Ridge with Platt calibration
Brier của tần suất nền và Ridge đã hiệu chuẩn	Brier scores for prevalence and calibrated Ridge
Peptide đơn · ma trận · ranking	Single peptide · effect map · ranking
Batch và xử lý toàn protein	Batch and whole-protein workflows
Xuất kết quả · model/source pages	Exports · model and source pages
Project và lịch sử bền vững	Persistent projects and history
Inference đối chiếu với runner	Inference checked against the runner
Nhập và so dữ liệu thí nghiệm	Import and compare experimental data
Mã nền React / FastAPI	React / FastAPI baseline code
Model mới · calibration · domain gate	New model · calibration · domain assessment
Dữ liệu và đánh giá	Data and evaluation
Bằng chứng thực nghiệm	Experimental findings
Công cụ phân tích	Analysis tool
Nhãn / QC / nhóm protein	Labels / QC / protein groups
Ngữ cảnh / ESM / chuyển nguồn	Context / ESM / source transfer
Workflow và lưu trữ	Workflows and storage
Nguồn và mức độ tổng quát hóa nào phù hợp?	Which source and generalization scope are appropriate?
ΔPSI giữa các lần đo	ΔPSI across replicates
Nhãn dương lặp lại	Reproducibility of positive labels
Jaccard vị trí 0,4965	Position Jaccard: 0.4965
Jaccard ô 0,6596	Cell Jaccard: 0.6596
Theo bộ lọc scanning	Scanning-specific filters
Baseline cùng thiết kế	Baseline under the same design
Hiệu ứng gate đảo dấu theo seed	The gate effect changes sign across seeds
Chưa vượt Ridge	No demonstrated improvement over Ridge
Kết quả thấp hơn Ridge	Lower performance than Ridge
CI chưa phân giải	Confidence interval remains inconclusive
odds ratio gây bệnh / lành tính ở mức vùng	region-level pathogenic-versus-benign odds ratio
2 mỗi nhóm	2 per group
Các nhóm còn lại	Other groups
Phần lớn 1 peptide	Mostly one peptide each
Mutation ở degron đầu C	Mutations in C-terminal degrons
Khác thang / độ dài; chỉ 5 nhóm mới	Different scale / length; only 5 new groups
Hoạt tính tile trong nhân	Nuclear tile activity
Không bổ sung nhãn mutation ΔPSI	No additional mutation ΔPSI labels
Hiệu ứng biến thể protein	Whole-protein variant effects
Endpoint và cấu trúc cần audit riêng	Endpoint and structure need separate audits
Xác suất sự kiện có phù hợp không?	Are event probabilities reliable?
Reliability của model Ridge	Reliability of the Ridge model
Peptide có thuộc miền áp dụng không?	Is the peptide within the applicability domain?
Nguồn đã băm	Hashed sources
OOF và checkpoint	OOF and checkpoints
Phiên bản dữ liệu	Data version
Cấu hình / split	Configuration / splits
phép thay có nhãn đo	substitutions with measured labels
Phạm vi kiểm chứng	Validation scope
Tích hợp model	Model integration
Ưu tiên nghiên cứu	Research priorities
Sai số toàn dải hay ưu tiên hiệu ứng mạnh?	Full-range accuracy or prioritizing strong effects?
Phát triển công cụ	Software development
Đánh giá chuyển nguồn	Evaluate transfer
Refit và hiệu chuẩn	Refit and calibrate
Nghiên cứu mô hình	Model research
Khóa ứng viên	Lock the candidate
Kiểm chứng sử dụng	Verify practical use
Nguồn	Sources
Đánh giá miền	Domain assessment
Đánh giá	Evaluation
Giới thiệu	Introduction
Cơ sở và mục tiêu	Background and objectives
Dữ liệu và cách tiếp cận	Data and approach
Kết quả và phân tích	Findings and interpretation
Công cụ hỗ trợ phân tích	Analysis tool
Tiến độ và hướng tiếp theo	Progress and next steps
Trao đổi với giảng viên	Faculty discussion
Phụ lục tra cứu	Reference appendix
Mô hình protein Fam188a quay, minh họa protein gấp cuộn	Rotating Fam188a model illustrating a folded protein
Mô hình protein Fam188a tĩnh	Static Fam188a protein model
Protein gấp cuộn	Folded protein
Ảnh prototype giao diện workspace với ma trận và bảng thông tin ô	Workspace design prototype showing the substitution map and cell inspector
Prototype giao diện · dữ liệu minh họa · chưa nối backend	Design prototype · illustrative data · no backend connection
Sai số MAE	MAE
AUROC dương	Positive-event AUROC
AP dương	Positive-event AP
Biểu đồ tương tác so sánh các recipe, chuyển metric bằng ba nút	Interactive comparison of model configurations; switch metrics using the three buttons
So sánh MAE và AUROC của các ứng viên	MAE and AUROC comparison of model candidates
Công trình liên quan	Related work
Số liệu và hash nguồn	Results and source hashes
JSON nghiên cứu, các figure và dữ liệu biểu đồ	Research JSON, standalone figures and chart data
Truy vết từng slide	Slide-level evidence
Điều kiện so sánh, ghi chú diễn giải và nguồn kết quả	Comparison conditions, interpretation notes and result sources
Khảo sát template và style	Template and style research
Nguồn ảnh và giấy phép	Asset credits and licenses
GIF protein · font · Chart.js · sơ đồ tự dựng	Protein GIF · fonts · Chart.js · original diagrams
Phạm vi phần mềm	Software scope
Baseline hiện có và các chức năng đang phát triển	Existing baseline and features in development
CT553H · Trao đổi nghiên cứu	CT553H · Research briefing
Hiệu ứng đột biến<br>degron ở mức residue	Predicting degron<br>mutation effects<br>at residue level
Giới thiệu đề tài, kết quả hiện có<br>và hướng nghiên cứu tiếp theo	Topic introduction, current findings<br>and next research steps
GVHD: TS. Hồ Quang Thái	Supervisor: Dr. Hồ Quang Thái
Đại học Cần Thơ	Can Tho University
Điều khiển trình chiếu	Presentation controls
Slide trước	Previous slide
Slide tiếp	Next slide
Mục lục · 34 slide chính + 16 phụ lục	Overview · 34 main slides + 16 appendices
Hướng dẫn phím tắt	Keyboard shortcuts
chuyển slide	change slides
O: mục lục · N: ghi chú và nguồn	O: overview · N: notes and sources
M: dừng / tiếp tục chuyển động · F: toàn màn hình	M: pause / resume motion · F: fullscreen
Home: về đầu · End: phần trao đổi	Home: first slide · End: discussion
Trên điện thoại: vuốt ngang hoặc dùng nút mũi tên.	On a phone: swipe horizontally or use the arrow buttons.
In từ trình duyệt để xuất PDF tĩnh toàn bộ 50 slide.	Print from the browser for a static PDF of all 50 slides.
Bộ slide giới thiệu và trao đổi nghiên cứu	Topic introduction and research discussion slide deck
Degron-footprint · Giới thiệu và trao đổi nghiên cứu	Degron-footprint · Introduction and research discussion
Dừng chuyển động	Pause motion
Tiếp tục chuyển động	Resume motion
Toàn màn hình	Fullscreen
Phụ lục	Appendix
Ghi chú người trình bày	Speaker notes
Ghi chú	Notes
Mục lục	Overview
Đóng	Close
Ứng	Pick
viên
AUROC trong peptide · cao hơn tốt hơn	Within-peptide AUROC · higher is better
MAE (PSI) · thấp hơn tốt hơn	MAE (PSI) · lower is better
Chênh lệch MAE · CI 97,5% đã điều chỉnh	MAE difference · adjusted 97.5% CI
Ridge ngữ cảnh	Context Ridge
AUROC dương · toàn dải PSI	Positive-event AUROC · full PSI range
MAE (PSI) · cùng train toàn dải	MAE (PSI) · matched full-range training
Chênh lệch MAE · CI 95% mô tả	MAE difference · descriptive 95% CI
MAE (PSI) · cùng kiến trúc one-hot	MAE (PSI) · matched one-hot architecture
Chênh lệch MAE so với học trực tiếp · CI 95% mô tả	MAE difference versus training from scratch · descriptive 95% CI
AUROC · đánh giá trên 91 peptide	AUROC · evaluation on 91 peptides
Precision dương (%)	Positive-event precision (%)
Xác suất dự đoán	Predicted probability
Tần suất quan sát	Observed frequency
Vị trí trong peptide HIF1A	Position in the HIF1A peptide
ΔPSI đo được	Measured ΔPSI
Brier · thấp hơn tốt hơn	Brier score · lower is better
% nhóm train của một lượt fit	% of training groups in a single fit
MAE trung bình các seed	Mean single-seed MAE
ESM + nhiều cửa sổ	ESM + multiple windows
AUROC dương · cao hơn tốt hơn	Positive-event AUROC · higher is better
Ridge · toàn dải	Ridge · full range
Ridge · chỉ PSI ≤ 4	Ridge · PSI ≤ 4 only
Ridge · cân bằng	Ridge · balanced
ESM + CNN · toàn dải	ESM + CNN · full range
ESM + CNN · chỉ PSI ≤ 4	ESM + CNN · PSI ≤ 4 only
ESM + nhiều cửa sổ · cân bằng	ESM + multiple windows · balanced
ESM + pointwise · toàn dải	ESM + pointwise · full range
One-hot + CNN · toàn dải	One-hot + CNN · full range
Scanning → CNN · toàn dải	Scanning → CNN · full range
Ridge + ESM · toàn dải	Ridge + ESM · full range
Phép thay + thành phần peptide	Substitution + peptide composition
Thêm thành phần lân cận	Add local composition
Thêm thứ tự trong lân cận	Add local order
Chỉ PSI ≤ 3	PSI ≤ 3 only
Chỉ PSI ≤ 4	PSI ≤ 4 only
Chỉ PSI ≤ 5	PSI ≤ 5 only
Toàn dải PSI	Full PSI range
Toàn dải, cân bằng	Full range, balanced
Toàn dải so với chỉ PSI ≤ 4	Full range versus PSI ≤ 4 only
Cân bằng so với chỉ PSI ≤ 4	Balanced versus PSI ≤ 4 only
Toàn dải	Full range
CNN so với pointwise	CNN versus pointwise
Nhiều cửa sổ, cân bằng\nso với CNN, toàn dải	Balanced multi-window model\nversus full-range CNN
CNN học trực tiếp	CNN from scratch
CNN khởi tạo từ scanning	Scanning-pretrained CNN
CNN từ trung bình replicate	CNN pretrained on replicate means
20 kiểu thay có trong scanning	20 types observed in scanning
360 kiểu thay còn lại	360 remaining types
Ridge cùng miền đánh giá	Ridge on the same test domain
Degformer sạch cụm	Group-clean Degformer
Khởi tạo 17	Seed 17
Khởi tạo 29	Seed 29
Khởi tạo 43	Seed 43
Trung bình dự đoán	Mean predictions
Tần suất nền	Prevalence baseline
Ridge + hiệu chuẩn	Calibrated Ridge
'''

def normalize_vi_numbers(value):
    value=re.sub(r'(?<!\d)(0),([0-9]+)',r'\1.\2',value)
    value=re.sub(r'(?<=\d),([0-9]{1,2}|[0-9]{4,})(?![0-9])',r'.\1',value)
    value=re.sub(r'(?<![\w.])([1-9][0-9]{0,2})\.([0-9]{3})(?![0-9.])',r'\1,\2',value)
    return value

EXTRA={
    '235 peptide · 122.412 ô':'235 peptides · 122,412 cells',
    '235 peptide / 122.412 ô':'235 peptides / 122,412 cells',
    '9,33 giờ':'9.33 hours',
    'CI điều chỉnh: −0,0338 đến −0,0183.':'Adjusted CI: −0.0338 to −0.0183.',
    'Checkpoint công bố có 42.163 / 47.847 ô mutation trong train.':'The published checkpoint contains 42,163 / 47,847 mutation cells in training.',
    'Chức năng nào nên được ưu tiên tiếp theo?':'Which features should be prioritized next?',
    'Cần đối chứng cùng encoder':'Match the encoder baseline',
    'Ensemble có thể thấy hợp dữ liệu lớn hơn mỗi thành viên.':'An ensemble may see a larger union of data than each member.',
    'Nhãn mức tile và nhãn mutation có mục tiêu khác nhau':'Tile labels and mutation labels have different targets',
    'Subset train khác nhau giữa các seed.':'Training subsets differ across seeds.',
    'WT của cả 91 peptide đều đã xuất hiện.':'WT sequences of all 91 peptides have already been seen.',
    'AP dương · cao hơn tốt hơn':'Positive-event AP · higher is better'
}
translations={}
for line in COPY.splitlines():
    if not line or '\t' not in line:
        continue
    left,right=line.split('\t',1)
    translations[normalize_vi_numbers(left.replace('\\n','\n'))]=right.replace('\\n','\n')
translations.update({normalize_vi_numbers(k):v for k,v in EXTRA.items()})
ordered=sorted(translations,key=len,reverse=True)

def translate(value):
    value=normalize_vi_numbers(value)
    if value in translations:
        return translations[value]
    # Simultaneous replacement avoids re-translating words introduced in English.
    return re.sub('|'.join(re.escape(s) for s in ordered),lambda m:translations[m.group()],value)

class EnglishLiterals(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str):
            node.value=translate(node.value)
        return node
    def visit_List(self,node):
        if all(isinstance(x,ast.Constant) and isinstance(x.value,str) for x in node.elts):
            if [x.value for x in node.elts]==['Ứng','viên']:
                return ast.copy_location(ast.List(elts=[ast.Constant('Pick')],ctx=ast.Load()),node)
        return self.generic_visit(node)

def source_hashes():
    return {str(p.relative_to(ORIGINAL)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ORIGINAL.rglob('*') if p.is_file() and 'previews' not in p.parts}

before=source_hashes()
for directory in ['vendor','assets']:
    shutil.copytree(ORIGINAL/directory,HERE/directory,dirs_exist_ok=True)
for name in ['tokens.json','asset-notices.md','prototype-capture.json']:
    shutil.copy2(ORIGINAL/name,HERE/name)

notes=json.loads((HERE/'english-notes.json').read_text(encoding='utf8'))
for name in ['prepare-assets.py','build-deck.py']:
    source=(ORIGINAL/name).read_text(encoding='utf8')
    tree=EnglishLiterals().visit(ast.parse(source))
    if name=='build-deck.py':
        for statement in tree.body:
            if isinstance(statement,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NOTE_OVERRIDES' for t in statement.targets):
                statement.value=ast.parse(repr({int(k):v for k,v in notes.items()}),mode='eval').body
    ast.fix_missing_locations(tree)
    code=ast.unparse(tree)+'\n'
    if name=='prepare-assets.py':
        code=code.replace("format(v, fmt).replace('.', ',')",'format(v, fmt)')
        code=code.replace("f'{v:.1f}%'.replace('.', ',')","f'{v:.1f}%'")
    else:
        code=code.replace('lang="vi"','lang="en"')
    (HERE/name).write_text(code,encoding='utf8')

css=(ORIGINAL/'deck.css').read_text(encoding='utf8')
css=css.replace('font-size:57px','font-size:54px').replace('.hero h1{max-width:13ch}', '.hero h1{max-width:18ch}')
(HERE/'deck.css').write_text(css+'\n/* English labels may wrap differently; the visual system is shared. */\n',encoding='utf8')
(HERE/'deck.js').write_text(translate((ORIGINAL/'deck.js').read_text(encoding='utf8')),encoding='utf8')
(HERE/'validate-deck.cjs').write_text((ORIGINAL/'validate-deck.cjs').read_text(encoding='utf8'),encoding='utf8')

runpy.run_path(str(HERE/'prepare-assets.py'),run_name='__main__')
runpy.run_path(str(HERE/'build-deck.py'),run_name='__main__')
evidence=json.loads((HERE/'evidence.json').read_text(encoding='utf8'))
evidence.update(language='en',edition='English translation of the Vietnamese research briefing',
                original_edition=ORIGINAL.name,localization_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
after=source_hashes()
assert before==after,'The original edition changed during localization'
(HERE/'localization-validation.json').write_text(json.dumps(dict(
    original_edition_unchanged=True,original_files_checked=len(before),
    translation_entries=len(translations),english_notes=len(notes),
    numeric_source_hashes=evidence['source_hashes'],language='en'),indent=2)+'\n',encoding='utf8')
print(f'English edition built; {len(translations)} translations; original edition unchanged.')
