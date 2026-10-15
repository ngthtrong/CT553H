# Lần thử G2 đầu tiên trên nhiệm vụ cross-assay — và nó **không** đứng được

> **Tài liệu phân tích, không phải quyết định.** Đề nghị ở §5 đã ghi thành
> [C-15](../../../../DECISIONS.md) và **chờ Trọng xác nhận**.
>
> Chạy 15/10/2026 (tối, phiên 7) theo [D-030](../../../../DECISIONS.md#d-030) mục 1: Trọng yêu cầu
> **chốt hướng đóng góp cụ thể trước khi làm tài liệu trình bày**. Đây là phép đo để chốt — và kết quả là
> **hướng cross-assay không chứa một đóng góp cỡ luận văn**.
>
> Script: [transfer_experiment.py](transfer_experiment.py).

## Nhãn bằng chứng
**[đo]** tự đo, có lệnh tái lập · **[nguồn]** số của tác giả · **[phân tích]** suy luận · **[đề xuất]** chờ xác nhận.

---

## 1. Câu hỏi và thiết kế

Câu hỏi quyết định: **nhãn GPS có giúp được gì trên chính nhiệm vụ tile không?** Nếu có thì "chuyển giao qua
assay" là đóng góp dương đo được và kiến trúc mới có việc rõ ràng ([D-027](../../../../DECISIONS.md#d-027)).

Bốn mô hình, cùng đặc trưng (one-hot 28×20 + thành phần), cùng ngân sách, cùng split cụm cov80, 5 seed,
**tất cả chấm trên nhãn tile ở cụm TEST**.

## 2. Kết quả **[đo]**

| Mô hình | ρ trên nhãn tile, cụm test | % của trần |
|---|---:|---:|
| A chỉ-GPS (nhiều dữ liệu, sai assay) | 0,7806 ± 0,0029 | 78,8% |
| **B chỉ-tile** (ít dữ liệu, đúng assay) | **0,7955 ± 0,0043** | 80,3% |
| **C biểu diễn dùng chung + đầu riêng mỗi assay** | **0,7983 ± 0,0022** | 80,6% |
| D stacking | 0,7955 ± 0,0043 | 80,3% |
| *trần nhiễu của nhãn tile* | *0,9903* | |

| Phép so | Giá trị |
|---|---:|
| B − A (học đúng assay so với nhiều dữ liệu sai assay) | **+0,0149** |
| **C − B (chuyển giao có giúp?)** | **+0,0029**, SD 0,0024, thắng **5/5** seed |
| D − B (stacking) | −0,0000 |

**Kiểm năng lực mô hình, 3 seed [đo]:** gradient boosting trên nhãn tile đạt **0,7791 ± 0,0048** —
**thấp hơn ridge tuyến tính**. Gộp thêm nhãn GPS cho boosting: **0,7847 ± 0,0051** (+0,0057), vẫn thấp hơn
ridge chỉ-tile. ⇒ **Mô hình phi tuyến mạnh không mở được dư địa.**

## 3. Hai lỗi của chính các phiên trước, phải ghi lại

### 3.1 Nhánh D vô nghĩa ngay từ thiết kế **[phân tích]**

Dự đoán của A là `X·wA` — một tổ hợp tuyến tính của chính các cột của `X`. Nên ridge trên `[pA, X]` **cộng
tuyến hoàn toàn** với ridge trên `X`, và D **buộc phải** đồng nhất với B. Số −0,0000 với SD 0,0000 xác nhận.
Một nhánh bị đốt vô ích.

### 3.2 Con số **+0,1061** ở [§10](../reframe-options-2026-10-15/README.md) **bị nhiễu lẫn và đã bị quy sai nguyên nhân**

| | ρ |
|---|---:|
| ridge học GPS → chấm nhãn **GPS** | 0,8848 |
| ridge học GPS → chấm nhãn **tile** (qua assay) | 0,7786 |
| **ridge học tile → chấm nhãn tile** (đúng assay) | **0,7955** |

Nếu 0,1061 là **dịch chuyển assay** thì học đúng assay phải lấy lại gần hết. Nó chỉ lấy lại **0,0169**.
Phần còn lại **không** phải dịch chuyển assay mà là: **nhãn tile vốn khó dự đoán hơn nhãn GPS**. Hai thứ đã
bị gộp vào một con số và gọi sai tên.

**Phần vẫn đúng:** [§9](../reframe-options-2026-10-15/README.md) đo **nhãn so với nhãn** trên trình tự giống
nhau, không cần mô hình — tương quan thật giữa hai assay là **0,785** so với trần nhiễu 0,978. Hai assay
**thật sự bất đồng một cách hệ thống**. Nhưng **cái giá mô hình phải trả vì dùng sai assay chỉ là 0,0169**.

### 3.3 Và một lỗi loại cũ đã lặp lại: coi **trần độ tin cậy** là **dư địa đạt được**

Trần 0,9903 là chặn trên của **phép đo**, **không** phải lời hứa về mức dự đoán được từ trình tự. Khi em viết
*"dư địa 0,1992"* là đã ngầm coi nó là dư địa đạt được. Đây **đúng loại lỗi** mà repo đã sửa một lần ở
[D-025](../../../../DECISIONS.md#d-025) mục 1 (bỏ "dư địa 0,1747" vì mốc là oracle). Lần này là biến thể:
**trần đo lường ≠ trần học được**. Phải viết lại mọi chỗ dùng "dư địa đến trần".

Bằng chứng cho điều đó: **ba lớp mô hình** (ridge, boosting, ghép hai đầu) đều dừng quanh **0,78–0,80**.
Khoảng 0,19 còn lại phần lớn **không xác định được từ 28-mer** — có thể do 2 residue thêm của tile, hiệu ứng
thư viện, hoặc ngữ cảnh vị trí trong protein nguyên vẹn.

## 4. Vì sao hướng cross-assay không đứng được **[phân tích]**

| Nguồn dư địa khả thi | Đo được | Đủ làm đóng góp luận văn? |
|---|---:|---|
| Kiến trúc xử lý **dịch chuyển định dạng assay** | **≈ +0,017** (toàn bộ giá của việc dùng sai assay) | **Không** |
| Chuyển giao / gộp hai assay | +0,003 … +0,006 | **Không** |
| Mô hình phi tuyến mạnh hơn | **−0,016** (boosting thua ridge) | **Không** |
| Biểu diễn tốt hơn (PLM, cấu trúc) | PAP của chính nhóm Voutsinos: Pearson **0,82/0,87** trên tile giữ lại **[nguồn]** | Có dư địa, nhưng là **sân của tác giả bộ dữ liệu** |

Cộng với [D-012](../../../../DECISIONS.md#d-012) (đòi đóng góp **dương** đo được) và
[D-027](../../../../DECISIONS.md#d-027) (đòi **kiến trúc mới**): ở đây **không có chỗ cho một kiến trúc mới
có delta dương cỡ luận văn**.

**Điều vẫn giữ giá trị:** phần **đo và phân rã** là việc thật và trung thực — nó **chặn** những gì người khác
có thể tuyên bố (split cụm không mua được gì; tương quan thật giữa hai assay chỉ 0,785; ba lớp mô hình đều
dừng ở 0,78–0,80). Nó xứng làm **một chương đo lường**, **không** xứng làm câu đóng góp chính.

## 5. **[đề xuất]** → [C-15](../../../../DECISIONS.md)

**Quay lại nhiệm vụ mức residue làm trụ đóng góp**, và hạ phần cross-assay xuống chương đo lường.

Lý do, theo đúng tiêu chí "dư địa có chứng minh được hay chỉ là hy vọng":

| | Nhiệm vụ tile / cross-assay | **Nhiệm vụ mức residue** |
|---|---|---|
| Bản chất khoảng trống | **Thực nghiệm** — ba mô hình dừng ở 0,78–0,80, không biết vì sao | **Chứng minh bằng toán** — 89,7% peptide có nhóm cùng cặp thay thế chứa cả vị trí dương và không dương ⇒ mô hình chỉ-thành-phần **không thể** tách |
| Đã có mô hình huấn luyện đúng nhiệm vụ | **Có** (PAP, 0,82/0,87) | **Không có** — ΔPAP là dùng ngoài mục đích, và nó **thua** baseline thành phần (0,4270 so với 0,4884) |
| Nhãn có nhận diện được tham số vị trí | **Không** ([§11.2](../reframe-options-2026-10-15/README.md): 28,9% ô tách khỏi 0) | **Có** — nhãn là **hiệu ứng đột biến**, đo trực tiếp từng vị trí |
| Việc của kiến trúc | ≈ +0,017, quá nhỏ | **MIL so với đầu theo vị trí** — chưa tìm thấy tiền lệ trong dự đoán mức residue |
| Rủi ro | không có đóng góp để thắng | **n = 91 (lực), và rủi ro LeBlanc** |

**Rủi ro phải nhận:** điều này đưa đề tài về đúng chỗ nó đứng ngày 14/10, với **n = 91** chưa giải quyết.
Khác biệt là nay **bốn hướng thay thế đã bị loại bằng số**, nên lựa chọn này là **kết luận có bằng chứng**
chứ không phải mặc định.

**Việc chặn đầu tiên nếu nhận C-15:** tính lực trên n = 91 và đếm số cụm protein trong đó — đúng việc mà
[C-12](../../../../DECISIONS.md) đã nêu và chưa làm.

## 6. Những gì tài liệu này **không** làm

- **Không** quyết định; §5 là đề xuất.
- **Không** thử PLM hay đặc trưng cấu trúc trên nhiệm vụ tile (có thể mở được dư địa, nhưng là sân của PAP).
- **Không** huấn luyện mô hình nào trên nhiệm vụ **mức residue** — đó là việc tiếp theo nếu C-15 được nhận.
- **Không** sửa `presentation/`.
