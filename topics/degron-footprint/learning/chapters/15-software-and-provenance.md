# Phần mềm: biến nghiên cứu thành công cụ có nguồn gốc rõ

## Ba lớp đang ở ba trạng thái

| Lớp | Đã có gì | Cần hiểu đúng |
|:--|:--|:--|
| Research offline | Dữ liệu, runner, kết quả development, audit | Chưa tự trở thành model phục vụ |
| Baseline ứng dụng | React/TypeScript, FastAPI, ETL, suy luận baseline | Chưa triển khai đủ phạm vi workspace mới |
| Workspace UI v2 | Prototype tương tác với fixture tổng hợp | Chưa nối API, lưu bền hoặc inference thật |

**API** là hợp đồng trao đổi giữa giao diện và backend. **ETL** là trích xuất, biến đổi, nạp dữ liệu tham chiếu. **Persistence/lưu bền** nghĩa là dữ liệu còn sau đóng/mở lại, khác biến JavaScript đang ở bộ nhớ tab. [PM-01; PM-02; PM-03]

![Ranh giới thực thi. Các hộp xanh là thành phần baseline/nghiên cứu đã có hồ sơ; hộp vàng là mở rộng cần triển khai và kiểm. Mũi tên tới lưu trữ thể hiện hướng tích hợp.](assets/diagrams/software-boundaries.pdf){width=95%}

## Vì sao giữ công cụ chạy local?

Phạm vi đã chọn là một workspace trên máy người dùng: giao diện React + TypeScript cho ma trận tương tác; FastAPI tái sử dụng suy luận Python; PostgreSQL local là đích lưu trữ của phần mở rộng. SQLite đã dùng trong baseline/test. Quyết định này tập trung vào chuỗi công việc nghiên cứu, lưu nguồn và khả năng mở lại phân tích. Nó chưa là bằng chứng PostgreSQL đã nghiệm thu. [PM-01]

Không cần biến công cụ thành hệ thống tài khoản, chia sẻ công khai hay dịch vụ hosting để đáp ứng mục tiêu hiện hành. Các giới hạn thực tế như kích thước batch, tốc độ và RAM vẫn cần đo trên ứng dụng local, không suy từ kích cỡ mô hình.

## Một phân tích peptide cần giữ những gì?

Đầu vào là 28 amino acid chuẩn. Mỗi vị trí có 19 phép thay khác WT, tổng **532 mutation**; ma trận thiết kế 28×20 có 28 ô WT→WT không phải dự đoán mutation. Snapshot cần giữ chuỗi, tọa độ, model/calibrator/gate version, thời điểm, nguồn annotation và score tương ứng. [PM-01; PM-03]

**Immutable snapshot** là bản chụp đã lưu không bị thay âm thầm khi model đổi hoặc người dùng chạy lại. Chạy lại tạo kết quả mới để so; lịch sử cũ còn giải thích được. Chỉ giữ một ảnh heatmap thiếu version không đủ tái lập số.

**ClinVar** bổ sung thông tin biến thể đã được nguồn tham chiếu ghi nhận. Cần ánh xạ accession, phiên bản, tọa độ và kiểm amino acid gốc. “Không khớp”, “không có nguồn”, “không có mapping” và “mapping mâu thuẫn” là các trạng thái khác nhau. Score ΔPSI không phải xác suất bệnh.

## Whole protein vẫn là nhiều tile

Với cửa sổ 28 và bước 23, tile thứ n bắt đầu tại $s_n=1+23(n-1)$; residue j trong tile ánh xạ thành $s_n+j-1$ trên protein, theo tọa độ 1-based. Chỉ cửa sổ đầy đủ được xét; đuôi thiếu độ dài phải báo là không phủ. [PM-01]

Ví dụ **tự đặt** protein dài 80: các tile bắt đầu 1, 24, 47; tile cuối kết thúc 74, còn 75–80 chưa phủ. Residue protein 25 có thể ở hai tile với ngữ cảnh khác. Không gộp trung bình các context rồi coi là hiệu ứng của protein nguyên vẹn nếu chưa có định nghĩa và validation cho phép gộp.

## Import thí nghiệm không tự trở thành dữ liệu train

Luồng thiết kế gồm: nhập CSV/TSV → kiểm schema/đơn vị/replicate/WT → preview lỗi và trùng → người dùng commit → so khớp chính xác mutation key với dự đoán. Thiếu không là 0; replicate chưa được gộp âm thầm; một phép đo ở endpoint khác không được gọi là ΔPSI rồi tính residual chung. [PM-01; PM-03]

**Residual** là dự đoán trừ số đo của cùng đại lượng và đúng đơn vị. So một probability với ΔPSI để tính MAE là sai endpoint. Dữ liệu import dùng cho công việc người dùng; chưa đủ điều kiện để retrain hoặc chứng minh external validity nếu chưa audit độc lập và provenance.

## Batch job cần nhiều hơn thanh progress

**Job** là tác vụ nền có trạng thái và kết quả từng item. Cần lưu trạng thái đang chờ/đang chạy/hoàn tất/lỗi/hủy, xử lý thành công một phần và quy tắc khôi phục sau restart. **Idempotence** nghĩa là lặp thao tác theo hợp đồng không tạo tác dụng phụ ngoài ý muốn, chẳng hạn nạp lại cùng dataset không nhân đôi âm thầm.

Một thanh progress mô phỏng chỉ chứng minh cách trình bày. Muốn nghiệm thu cần backend/worker thật, lưu bền, kiểm mất kết nối, hủy, khởi động lại và provenance kết quả.

![Ảnh Workspace UI v2 dùng fixture tổng hợp. Mọi số trong ảnh là dữ liệu trình diễn giao diện, không phải kết quả inference hoặc số đo nghiên cứu.](assets/figures/workspace-fixture.png){width=100%}

## Những gì đã kiểm và những gì phải kiểm lại

Baseline có hồ sơ test backend/frontend và đối chiếu suy luận trước đây. Prototype có hồ sơ review trình duyệt riêng. Sách này không chạy lại các bộ kiểm đó và không dùng chúng để nghiệm thu các chức năng đang bổ sung. [PM-01; PM-02; PM-03]

Hướng tiếp theo là triển khai projects/history, jobs peptide/protein, import/comparison, export mở rộng, PostgreSQL local và cổng R3 đúng nguồn. Sau đó mới kiểm toàn luồng, numerical agreement, recovery và tài nguyên. Mô hình mới chỉ được nối vào sau quyết định artifact riêng.

::: {.exercise title="Tự kiểm 15"}
1. Vì sao prototype thao tác được chưa chứng minh lưu bền?
2. Với tile bắt đầu ở 24, vị trí 5 trong tile ở tọa độ protein nào?
3. Tại sao import không tự tạo một benchmark external?
4. Một export muốn giải thích được sau sáu tháng cần những metadata nào?
:::
