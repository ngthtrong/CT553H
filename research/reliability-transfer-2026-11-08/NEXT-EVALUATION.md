# Đánh giá LoRA chuyển miền tiếp theo — thiết kế, chưa thực thi

Ngày 08/11/2026. Đây là đầu ra lập kế hoạch của đợt CPU, không phải kết quả
LoRA trên T, model phục vụ hoặc quyết định nghiệm thu. Không có lệnh GPU nào
được chạy trong môi trường hiện tại.

## 1. Câu hỏi

ESM2-35M LoRA-D có duy trì lợi ích so với frozen-D cùng head và W5-D khi chấm
mutation scanning cùng nguồn nhưng ngoài nhóm W không? Ưu tiên D vì đó là
policy full-range đã được chỉ định trong replay 07/11, không chọn lại từ các
subgroup/threshold mới của đợt CPU. B là kết quả sensitivity development đã có,
không tự mở thêm một cuộc chọn model bằng T.

T đã được xem qua W5 và diagnostic. Mọi LoRA evaluation ở đây phải gọi là
**đánh giá chuyển miền hậu kiểm trên held-source đã khảo sát**, không phải
independent external validation. Nếu cần claim độc lập, phải có nguồn/cohort
mới và protocol khóa riêng trước khi xem outcome.

## 2. Điều kiện trước thực thi

1. Lưu commit, config, source/data identity và quyết định sử dụng candidate.
2. Giữ T ngoài training, epoch selection, feature fit và calibrator fit.
3. Chọn môi trường thực thi khác được người dùng cho phép, với model weights
   và runtime đã kiểm; không tự chạy GPU tại môi trường hiện tại.
4. Chốt compute/time budget và tiêu chí thực dụng trước khi chấm, có thể kết
   thúc với kết quả âm. Không mang ngưỡng Q1 .02 PSI thành threshold LoRA chung.

## 3. Model và fit policy dự kiến

- Recipe: frozen-D và LoRA-D ESM2-35M cùng head, input, base revision,
  precision policy và seed 17/29/43 của campaign đã có.
- Không lấy 15 outer models rồi gọi là final ensemble đã được đánh giá.
- Một lựa chọn có thể khóa: với mỗi seed, lấy median của 5 selected epochs
  development đã lưu; khởi tạo lại và refit toàn W đúng số epoch đó cho mỗi
  recipe. Không xem T để đổi epoch, rank, learning rate hoặc recipe.
- Lưu epoch source, realized training groups, IDs/hash, tokenizer/revision,
  adapter/head, trained parameters và full execution provenance.
- Calibrator cuối học từ ensemble OOF W của đúng recipe; không fit bằng nhãn
  T. Phải công khai score shift giữa fold fits và final refit. Chưa xem khả
  năng này là đã được kiểm chứng chỉ vì có calibrator CV.
- Ba prediction seed được trung bình trước chấm ensemble. Nếu chỉ phục vụ
  một seed thì metric và utility của ensemble không được gán cho model đó.

Đây là **đề xuất cần khóa trước thực thi**, không sửa campaign v3 đang lưu và
không tạo quyết định serving. Nếu lựa chọn khác được tác giả chốt, tạo version
protocol mới, giải thích trước khi đọc prediction T.

## 4. Chấm và baseline

- Primary population: đúng cell T rep1 đã pin, 39.234 cell/1.410 peptide/730 nhóm.
- Primary endpoint dự kiến: peptide-macro MAE. Hai contrast LoRA-D−frozen-D
  và LoRA-D−W5-D dùng paired group bootstrap 5.000 lần, CI97,5% cho family hai.
- Zero và train-derived constant là baseline phụ cần báo, không bỏ vì AUROC tốt.
- Secondary: RMSE, AUROC/AP ±1 (đủ lớp), P@min(10,N), prevalence, Brier 3 lớp,
  ECE hai chiều, reliability theo PSI, directed pair và similarity.
- Candidate pool T nhỏ hơn W; không gọi P@10 W và T là cùng tỷ lệ sàng lọc.
- Replicate intersection chấm rep1/rep2/mean12 riêng, giữ rep1 primary.
- Báo mọi seed, no-hit peptide, lớp âm hiếm, null và case thất bại.

CI có lợi hỗ trợ superiority theo endpoint đã khóa. CI cắt 0 là chưa phân giải;
không đồng nghĩa tương đương. CI loại trừ mức lợi ích thực dụng đã khóa có thể
dẫn tới dừng promotion. Không đổi threshold hoặc model để cứu outcome trên T.

## 5. Nguồn ngoài độc lập

Trước nhập nguồn mới: kiểm endpoint/construct/chiều đơn vị, license/terms,
mapping WT/mutant, replicate/QC và protein/sequence/homology overlap với toàn
bộ nguồn đã dùng. Koren 3-bin, VAMP-seq abundance, PAP score và E3 motif label
không tự trở thành Zhang ΔPSI; không padding/scale tùy ý để gộp train hoặc test.
Nếu không có nguồn tương thích đủ nhóm, ghi limitation, không giả dữ liệu để
đóng `source_pending`.

## 6. Acceptance của bước tiếp

- Artifact/prediction đủ cohort/seed, hash và realized fit lineage.
- Inference parity, finite output, coordinate/label agreement.
- Không nhãn T trong bất kỳ fit/selection nào; báo lịch sử đã khảo sát nguồn.
- Báo cả metric thuận và bất lợi cùng CI và denominator.
- Không suy lợi ích wet lab, E3, full-protein hoặc clinical từ evaluation này.
- Không tự đóng G2/G3 hoặc đổi serving model.
