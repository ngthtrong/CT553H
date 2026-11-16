# Koren S4 bổ sung — 16/11/2026

Trọng cung cấp XLSX và yêu cầu pause/chạy lại không giới hạn giờ. File đã khớp
SHA-256 `c96973f2b2781b35a822527fa875e38df82f75da9ac327668d1d10114fdbcbeb`.
Đây là phân tích bổ sung sau refit, không sửa code/protocol/config/queue hoặc
checkpoint của campaign refit đang dở. Lịch sử job Koren source_pending trong
queue cũ được giữ nguyên; kết quả bổ sung có identity/provenance riêng.

Nguồn: Koren et al. 2018, DOI 10.1016/j.cell.2018.04.028, Table S4,
NIHMS967427-supplement-11.xlsx. Bảng đã được xem và audit ngày 22/10: không gọi
đây là nguồn độc lập chưa từng khảo sát. Chỉ sử dụng nội bộ, không xuất bảng
gốc/sequence/cell-level derivative lên Git. Xuất metric tổng hợp theo substrate.

1. Đọc cached cell values trong XLSX bằng zipfile/ElementTree chuẩn Python,
   không chạy macro, công thức hoặc mã tải về. Kiểm đủ 9 substrate, 1.827 dòng
   đã có substitution, 1.739 nonsynonymous mutants; tái tính PSI ba bin, sai số
   <=1e-6. Tái dựng WT từ substitution, kiểm mọi mutant khác đúng một residue;
   WT PSI là median các ô đồng nghĩa của cùng substrate.
2. Chỉ chấm 1.739 nonsynonymous mutants. Giữ nguyên chuỗi thật 12/23 aa, bỏ
   đúng một stop terminal *, kiểm mask tokenizer có đúng L residue. Không pad
   amino acid giả, không kéo dài thành 28 aa, không gộp thang 3-bin với Zhang.
3. Tái dùng nguyên backbone/LoRA/head final của frozen-D và LoRA-D, ba seed
   17/29/43. Adapter inference riêng chỉ tổng quát hoá chiều dài: delta-site,
   delta-mean và pair/composition 60 chiều tính trên chuỗi thật. Không train,
   calibrate hoặc chọn model/epoch bằng Koren. Kiểm parity với inference 28-aa
   gốc trên fixture W trước khi dùng, atol/rtol 1e-5.
4. Mean raw prediction ba seed trước xếp hạng. Primary descriptive metric là
   Spearman giữa raw ensemble score và ΔPSI trong từng substrate; báo cả từng
   seed, đủ mẫu và trường hợp constant/null. Báo mean rho của 9 substrate như
   tổng hợp mô tả, không gộp mọi cell để giả có mẫu độc lập. Không p-value/CI
   bằng bootstrap theo cell. Không dùng probability calibrator Zhang, không
   báo MAE cùng đơn vị với Zhang.
5. Đây là extrapolation về chiều dài, construct và nguồn lân cận. Không đóng
   source_pending/G2/G3, không promotion model phục vụ. Dataset từng có P2
   không đạt do chỉ 9 substrate/5 cụm mới; không diễn giải lại cổng đó.
6. Giữ cùng OS locks/STOP/checkpoint prefix của bộ máy local. Sau khi core
   refit hoàn tất, launcher gọi phân tích bổ sung trong cùng terminal; không
   tạo scheduler hoặc GPU worker song song. Pause chờ global locks; resume
   bằng run-local sẽ bỏ qua core đã xong rồi tiếp tục prefix Koren đã commit.

Identity bổ sung chứa code phân tích/protocol/raw SHA, plan ID và SHA các model
final. Artifact nặng ở local/koren-<identity>/; báo cáo nhỏ ở koren-results.json,
koren-run-status.json và koren-handoff-manifest.json. Status bổ sung được in
sau status của campaign core, không ghi đè state/queue lịch sử.
