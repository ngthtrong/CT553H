# Đối chiếu 7 ứng viên đang đào sâu

> Ngày **12/10/2026**. Lập khi thêm hai ứng viên mới (`budgeted-plm-variant-scoring`, `scalable-metagenomic-binning`) vào `topics/`. Mục đích: cho Trọng thấy hai ứng viên mới đứng ở đâu so với 5 ứng viên đang có, **trước khi đầu tư thêm công sức**.
>
> **Đây không phải quyết định.** Vị trí của từng đề tài chỉ ghi ở [DECISIONS.md](../DECISIONS.md). Đề xuất của Claude nằm ở phần C của file đó.
>
> Thước đo: 3 cổng bắt buộc G1/G2/G3 và 5 tiêu chí GVHD, xem [course.md](../project/course.md).

---

## 1. Bảng ba cổng bắt buộc

Trượt một cổng là loại, không bù bằng điểm cao ở chỗ khác ([D-012](../DECISIONS.md#d-012)).

| Ứng viên | G1 nhãn độc lập | G2 đóng góp dương | G3 ứng dụng |
|---|---|---|---|
| [degron-footprint](../topics/degron-footprint/README.md) | **Đạt, mạnh nhất repo** — toàn bộ nhãn thực nghiệm | **Chưa xác lập** — baseline thành phần amino acid đã đạt precision@3 0,6045, trần 0,7792, dư địa 0,1747 | **Yếu nhất** |
| [dark-kinome-zero-shot](../archive/topics/dark-kinome-zero-shot/README.md) | Đạt — nhãn chú giải từ CSDL | **Yếu** — trụ tính mới đã sụp, cả 3 trục phương pháp đều có tiền lệ | Khả thi |
| [xai-fidelity-benchmark](../archive/topics/xai-fidelity-benchmark/README.md) (A2) | Khả quan, chưa audit | **Chưa rõ** — có thể ra kết quả âm | Khả thi |
| [structure-sequence-leakage-audit](../archive/topics/structure-sequence-leakage-audit/README.md) (A3) | Khả quan, chưa audit | **Rủi ro trung bình–cao** — kết quả âm | Làm được, không tự nhiên |
| [plm-calibration-audit](../archive/topics/plm-calibration-audit/README.md) (A4) | Khả quan, chưa audit | **Khả quan nhất nhóm A** | **Tự nhiên** |
| **[budgeted-plm-variant-scoring](../archive/topics/budgeted-plm-variant-scoring/README.md)** (LC1, mới) | **Đạt** — DMS thực nghiệm, chỉ dùng để đánh giá | **Chưa rõ, rủi ro cao** — phần tốc độ đã có tiền lệ; phần cascade phụ thuộc chênh lệch rẻ–đắt mà bằng chứng nói là nhỏ | **Tốt** |
| **[scalable-metagenomic-binning](../archive/topics/scalable-metagenomic-binning/README.md)** (LC2, mới) | **Đạt** — CAMI II có ground truth theo genome | **Khả quan** — thời gian và RAM là đại lượng dương, dễ đo, chỗ cải thiện rõ | Trung bình |

## 2. Hai trục quyết định ngoài G1/G2/G3

Hai trục này không nằm trong G1/G2/G3 nhưng đang chi phối việc chọn đề tài mạnh hơn.

| Ứng viên | Khớp danh mục GVHD | Đáp ứng "kiến trúc chưa ai dùng" (GVHD, 11/10) |
|---|---|---|
| degron-footprint | Trung bình — protein, mức residue | Có thể, nếu đề xuất kiến trúc mới |
| dark-kinome-zero-shot | Trung bình — PTM, không phải nhánh GVHD | Có thể |
| A2 xai-fidelity-benchmark | **Mạnh** — BERT-Promoter của GVHD dùng SHAP | **Không** (dạng benchmark) |
| A3 structure-sequence-leakage-audit | **Mạnh nhất** — protein màng/vận chuyển là nhánh dày nhất của GVHD | **Không** (dạng audit) |
| A4 plm-calibration-audit | **Mạnh** — dùng lại chính mô hình mCNN+PLM của GVHD | **Không** (dạng công cụ) |
| **LC1 budgeted-plm-variant-scoring** | **Trung bình** — đúng protein + PLM, nhưng 14 công trình GVHD là phân loại có giám sát, **không có bài nào về dự đoán hiệu ứng đột biến** | **Không** (thuật toán/hệ thống) |
| **LC2 scalable-metagenomic-binning** | **Yếu nhất** — **không có công trình nào về metagenomics** trong danh mục GVHD | **Không** (thuật toán đồ thị) |

Nguồn cho cột khớp GVHD: [advisor-research.md](../project/advisor-research.md), 14 công trình. Nguồn cho cột kiến trúc: [people.md](../project/people.md), mục 11/10/2026.

→ **Hai ứng viên mới không giải được vấn đề đang chặn A2/A3/A4.** Cả hai đều là đề tài tầng công cụ/thuật toán, đúng loại mà GVHD nói ngày 11/10 là không nhận. Thêm vào đó, cả hai **khớp danh mục GVHD yếu hơn** A2/A3/A4. Nếu [C-3](../DECISIONS.md) được GVHD trả lời là "không nhận đóng góp dạng công cụ", thì 5 trong 7 ứng viên bị loại cùng lúc, kể cả hai ứng viên mới.

## 3. Điều hai ứng viên mới làm tốt hơn

Dù vậy, hai ứng viên mới có hai điểm mạnh thật mà 5 ứng viên cũ không có:

1. **G1 đạt sẵn, không cần audit.** Ba ứng viên A2/A3/A4 vẫn ở trạng thái "khả quan, chưa audit" — chưa ai biết nhãn của chúng có sạch không. LC1 (nhãn DMS của ProteinGym) và LC2 (ground truth genome của CAMI II) đều có nhãn độc lập sẵn sàng, đã được cộng đồng dùng làm benchmark.
2. **G2 không phụ thuộc kết quả âm.** Đây là điểm yếu chung của A2 và A3: đóng góp của chúng có thể là "SHAP không đáng tin" hoặc "cấu trúc không giúp gì" — tức kết quả âm, mà GVHD không nhận ([D-012](../DECISIONS.md#d-012)). Thời gian chạy và bộ nhớ thì **luôn là đại lượng dương**: giảm 3× là giảm 3×, không có phiên bản âm của nó. LC2 mạnh nhất ở điểm này.

## 4. Trạng thái tra cứu: hai ứng viên mới non hơn hẳn

| Ứng viên | Đã làm được gì |
|---|---|
| degron-footprint | Đã tải dữ liệu, audit nhãn, audit thành phần amino acid, cụm protein MMseqs2 |
| dark-kinome-zero-shot | Đã audit split/nhãn, 6 phép kiểm tính mới, đối chiếu SOTA |
| A2, A3, A4 | Mới khảo sát qua tóm tắt, chưa đọc toàn văn nguồn nào |
| **LC1** | Tra 6 lượt, **chưa đọc toàn văn bài nào**, chưa tải dữ liệu |
| **LC2** | Tra 4 lượt + **đã tự đọc mã nguồn COMEBin**, chưa tải dữ liệu, chưa chạy baseline |

So sánh ở mục 1 và 2 vì vậy **không cùng độ tin cậy**: degron và dark kinome bị đánh giá thấp một phần vì đã bị kiểm kỹ và đã lộ điểm yếu, còn hai ứng viên mới chưa bị kiểm ở mức tương đương. Mỗi ứng viên cũ đều từng trông hấp dẫn hơn trước khi bị đào sâu.

## 5. Thí nghiệm rẻ nhất để quyết định [ĐỀ XUẤT]

Cả hai ứng viên mới đều có một phép kiểm làm sụp hoặc đứng được chúng, rẻ và nhanh:

| Ứng viên | Phép kiểm | Chi phí | Sụp nếu |
|---|---|---|---|
| **LC1** | Dùng bảng điểm có sẵn trên ProteinGym, so bộ chấm rẻ (650M, VespaG) với bộ chấm đắt (3B/15B, ensemble) theo Spearman và top-K recall | 1–2 ngày, **CPU, không cần GPU** | Chênh lệch nhỏ trên phần lớn assay → tầng 2 của cascade vô nghĩa |
| **LC2** | Chạy COMEBin trên một mẫu CAMI II nhỏ, đo thời gian từng bước (học biểu diễn / HNSW / 120 lần Leiden) | 2–3 ngày, cần GPU và vài chục GB | Lưới Leiden chiếm phần nhỏ thời gian → nút thắt nằm ở chỗ khác, ngoài tầm đề tài |

Nhưng với **LC2, câu hỏi phải trả lời trước cả thí nghiệm** là câu hỏi cho GVHD: một đề tài metagenomics, ngoài hẳn nhánh nghiên cứu của thầy, có được hướng dẫn và nhận không. Tải vài trăm GB dữ liệu trước khi hỏi là đặt cược sai thứ tự.

## 6. Điều cần nói với GVHD ở tuần 6 [ĐỀ XUẤT]

Hai ứng viên mới làm cho câu hỏi [C-3](../DECISIONS.md) trở nên gấp hơn, chứ không bớt. Đề xuất gộp thành một câu hỏi duy nhất cho GVHD:

> Thầy có nhận đóng góp dạng **công cụ, thước đo, hoặc thuật toán tối ưu** (không có kiến trúc mạng mới) làm đóng góp chính của luận văn không? Nếu không, em cần chuyển sang hướng đề xuất kiến trúc, và khi đó 5 trong 7 ứng viên hiện tại phải loại.

Câu trả lời này quyết định số phận của A2, A3, A4, LC1 và LC2 cùng lúc — nên nó đáng được hỏi trước mọi thí nghiệm nào ở mục 5.
