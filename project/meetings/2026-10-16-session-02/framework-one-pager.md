# Khung đề tài xin duyệt — buổi gặp GVHD lần 2

**Ngày 16/10/2026 (cuối tuần 6)** · SV **Nguyễn Thế Trọng** (B2305615) · GVHD **TS. Hồ Quang Thái** · CT553H

> Trang mang đi họp. Mọi con số là **tự đo**, có file kết quả trong repo. Trạng thái hiện hành của đề tài chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md#hien-hanh); trang này là bản đọc nhanh cho buổi gặp, không phải nơi ghi quyết định.

## Mục đích buổi gặp

1. **Xin thầy duyệt khung đề tài gồm ba trụ** dưới đây. Tới nay đề tài chưa có căn cứ nào ghi là đã được duyệt ([C-5](../../../DECISIONS.md#c-5)).
2. **Xin ghi biên bản** cho lời thầy đã xác nhận ngày 15/10: trụ phần mềm được tính là đóng góp ([D-034](../../../DECISIONS.md#d-034) — hiện chỉ là lời truyền đạt, chưa có biên bản).

## Bài toán và phạm vi

Degron là đoạn trình tự ngắn khiến protein bị đánh dấu để phân hủy. Câu hỏi của đề tài: **residue nào trong degron quyết định độ bền**, và thay một residue thì độ bền đổi bao nhiêu.

| | |
|---|---|
| **Vào** | peptide 28 residue (kèm ngữ cảnh cấu trúc nếu có) |
| **Ra** | ma trận `28 × 20` ΔPSI + bản đồ quan trọng theo vị trí |
| **Nhãn** | ΔPSI **đo thực nghiệm** (assay GPS, Zhang 2023: bộ quét và bộ bão hòa) |
| **Phạm vi** | **degron tự trị** (hoạt động được trong một 28-mer), biến thể **dòng mầm** |

**Giới hạn của phạm vi đã được đo, không phải giả định:** trong 8 degron lái ung thư kinh điển chỉ **HIF1A** hiện ra trong assay. `CTNNB1` codon 31–48 đo tốt nhưng **không phải degron** (PSI 5,27 / 5,36); `MYC` T58/S62 vắng mặt. Ba degron đó đều **cần mồi** (phosphoryl hóa, hoặc bám hai motif cùng lúc) nên không thể hiện trong một 28-mer. Vì vậy đề tài **không** dùng "đột biến lái ung thư" làm mạch dẫn ([D-035](../../../DECISIONS.md#d-035)).

## Ba trụ của khung

| Trụ | Nội dung và số đỡ | Trạng thái |
|---|---|---|
| **1. Cấp thiết** | Vùng protein mà thực nghiệm đo được là degron **giàu biến thể gây bệnh 2,148 lần** so với lành tính (CI [2,072; 2,227]), so sánh **trong cùng một protein** (Mantel–Haenszel, **3.114 protein**, 2,56 triệu biến thể ClinVar). Trong vùng đó có **530.412 biến thể chưa rõ ý nghĩa (VUS)** mà chưa công cụ nào gán cơ chế | ✅ **đã đo** — ở **mức vùng** |
| **2. Phương pháp** | (a) **Chứng minh** lớp mô hình hiện tại không định vị được residue: 89,7% peptide có footprint, phản ví dụ hạng 2, phép kiểm hoán vị trên PAP (Pearson 1,000000). (b) **Giao thức đánh giá**: hai bộ nhãn, trần đo lường **0,9458 / 0,9519**, split theo cụm protein, ngưỡng phát hiện **0,0123** tính trước. (c) **Kết quả dương đầu tiên**: **+0,0300** AUROC so với mô hình degron công bố gần nhất trên trục ngữ cảnh. (d) **Kiến trúc mới** — chưa chạy | ✅ (a)(b)(c) đã đo · ⬜ (d) **việc chính còn lại** |
| **3. Phần mềm** | (a) **Dịch vụ dự đoán**: ma trận 28×20 + bản đồ vị trí, **bất định từng ô neo vào trần đo lường**, chấm đột biến tuỳ ý, **API**, cờ ngoài phân phối, cờ ngăn tế bào, xuất xứ nhãn. (b) **Harness đánh giá** tái lập: nạp các mô hình trước, áp **cùng một split** cụm, báo delta kèm trần và ngưỡng phát hiện. Miền áp dụng: **116.702** tile degron / **17.287** protein, **87,3%** cụm chưa thấy trong huấn luyện | ⬜ **đã thiết kế, chưa xây** (tuần 11–13) |

**Vì sao phần mềm là một đóng góp, không phải vỏ ngoài:** nút cổ chai của bài toán **không phải độ chính xác**. **75,9%** phần dư sau khi đã biết thành phần acid amin là **nhiễu đo**; hai replicate chỉ đồng ý về *residue nào* là footprint ở mức Jaccard **0,4965**. Một công cụ trả về **một câu trả lời chắc chắn là sai bản chất dữ liệu**. Cái còn thiếu là dự đoán **kèm độ bất định, đặt cạnh chính giới hạn của phép đo**.

## Giới hạn nói thẳng

1. **Trụ 1 chỉ đứng ở mức vùng.** Ở mức **residue** thì **chưa thiết lập được**: ba phép đo độc lập đều nhất quán với rỗng (tầng có lực nhất AUC **0,5166**, CI [0,479; 0,554]). ⇒ Đề tài **không** nói residue nó dự đoán là residue mang tín hiệu bệnh, và **không** dùng ClinVar làm đích xác nhận mô hình. ClinVar là **động lực** ([D-036](../../../DECISIONS.md#d-036)).
2. **Biến thể không giàu lên theo *vị trí*** — tỉ lệ trong degron bằng đúng tỉ lệ nền (33,4% so 32,4%) ⇒ không nói "degron là điểm nóng biến thể".
3. **Con số 2,148 chưa khử bảo tồn và độ vô trật tự.** Nếu khử mà nó biến mất thì nó chỉ nói "degron nằm trong vùng chức năng". Đối chứng này **chưa chạy** ([theo dõi](../../../DECISIONS.md#doi-chung-cap-thiet)).
4. **G2 chưa đạt.** Trên ma trận bão hòa mô hình hiện tại còn **thua 0,0420** so với mốc công bố (0,7273 so 0,7693; trần đo lường 0,9519). Đây là mục tiêu còn lại, có số rõ ràng.
5. **Nhiệm vụ đã có tiền lệ.** Degformer (repo GitHub, **không có bài báo**) **đã xuất đúng ma trận 28×20**. Chỗ khác biệt của đề tài là **điều kiện đánh giá** (split theo cụm protein, trần nhãn, bất định từng dự đoán), không phải "chưa ai làm". Đã đo được **4,09%** rò rỉ trình tự y hệt trong phép chia của họ.
6. **Cả hai nguồn nhãn mức residue đều của một nhóm tác giả (Zhang 2023)**, và hiện **chưa có ứng viên thay thế**. Đây là giới hạn phải nằm trong đề cương.
7. **Đề tài không có dự phòng** ([D-026](../../../DECISIONS.md#d-026)) — nên có điểm kiểm cứng ở tuần 10.

## Lộ trình

| Tuần | Việc | Đầu ra |
|---|---|---|
| **7** | Ba biến thể kiến trúc trên một lưới, nhắm mốc **0,7693** | delta đo được trên ma trận, kèm CI |
| **8** | Ablation · độ ổn định theo seed · chạy lại checkpoint Degformer dưới split cụm | bảng đối chứng có kiểm soát |
| **9** | Lưới biểu diễn (PLM so one-hot) · phân tích lỗi theo nhóm | cải thiện đến từ đâu, thất bại ở đâu |
| **10** | **Điểm kiểm cứng** | nếu không đạt mục tiêu ma trận: báo đúng là kết quả âm có biên, dồn trọng số sang benchmark + phần mềm |
| **11–13** | Phần mềm: dịch vụ dự đoán + harness đánh giá | sản phẩm cho tiêu chí 5 |
| **14–15** | Viết luận văn và bảo vệ | — |

## Câu hỏi xin thầy

*(Trọng tự viết — bốn câu, khớp slide 26 của bản nội dung trình bày.)*

1.
2.
3.
4.

## Ghi chú trong buổi gặp

> Ghi nguyên văn lời thầy vào đây, rồi chuyển vào `minutes.md` sau buổi gặp. Hệ quả cho đề tài thì ghi thành một mục mới trong [DECISIONS.md](../../../DECISIONS.md) — biên bản chỉ ghi thầy đã nói gì.

&nbsp;

&nbsp;

&nbsp;

---

**Nguồn số liệu:** [variant-coverage-2026-10-15](../../../topics/degron-footprint/research/variant-coverage-2026-10-15/README.md) (trụ 1, miền áp dụng) · [residue-task-derisk-2026-10-15](../../../topics/degron-footprint/research/residue-task-derisk-2026-10-15/README.md) (trụ 2) · [full-data-audit](../../../topics/degron-footprint/research/full-data-audit/README.md) (trần đo lường, nhiễu) · [pap-baseline](../../../topics/degron-footprint/research/pap-baseline/README.md) (phép kiểm hoán vị). Nội dung trình bày đầy đủ: [slide-content-2026-10-15.md](../../../topics/degron-footprint/presentation/slide-content-2026-10-15.md).
