# Tối ưu bước đồ thị và phân cụm cho phân nhóm contig metagenomics

> **Thẻ trạng thái nghiên cứu.** Vị trí của đề tài chỉ ghi ở [DECISIONS.md](../../DECISIONS.md). Cập nhật lần cuối: **12/10/2026** (mới mở hồ sơ).

| | |
|---|---|
| Lĩnh vực | Tin sinh học, metagenomics; tầng thuật toán đồ thị và phân cụm |
| Dữ liệu | CAMI II (mô phỏng, có ground truth theo genome) + mẫu thật. Chưa tải |
| Giai đoạn | Đã đọc mã nguồn COMEBin; khảo sát tiền lệ qua tóm tắt; **chưa tải dữ liệu, chưa chạy baseline** |

## Bài toán

Gom các contig (đoạn DNA đã lắp ráp) cùng nguồn gốc bộ gen vào một nhóm (bin), để khôi phục bộ gen từ mẫu hỗn hợp nhiều vi sinh vật. Câu hỏi tính toán: làm bước xây đồ thị và phân cụm **ít bộ nhớ và thời gian hơn** mà vẫn giữ chất lượng bin.

- **Đầu vào:** contig FASTA; coverage qua một hoặc nhiều mẫu; embedding từ bộ học biểu diễn có sẵn; (tuỳ chọn) đồ thị lắp ráp GFA.
- **Đầu ra:** bảng gán `contig_id → bin_id` kèm danh sách contig chưa gán; FASTA từng bin; thời gian từng bước, RAM cực đại, số cạnh.

## Cổng G1/G2/G3

| Cổng | Trạng thái | Ghi chú |
|---|---|---|
| G1 nhãn độc lập | **Đạt** — CAMI II biết contig thuộc genome nào, nhãn độc lập với pipeline | Chưa audit |
| G2 đóng góp dương | **Khả quan hơn LC1**: thời gian và RAM là đại lượng dương, dễ đo, và có chỗ cải thiện rõ — COMEBin **lỗi 129/297 mẫu thật (43%)** theo QuickBin 2026 | Chưa tự đo |
| G3 ứng dụng | **Trung bình**: công cụ CLI tự nhiên hơn web. Phải thiết kế thêm để đạt tiêu chí 5 | Chưa thiết kế |

## Phát hiện làm thay đổi bài toán

**Đóng góp A của bản mô tả gốc ("dùng tìm kiếm láng giềng gần đúng để tránh O(n²)") đã nằm sẵn trong baseline** — [TỰ KIỂM], đọc mã nguồn `ziyewang/COMEBin` commit `1b476a4` (23/08/2026):

- `COMEBin/cluster.py` dùng **hnswlib** (HNSW, tức ANN): `init_index(ef_construction=max_edges*10, M=16)` rồi `knn_query(..., max_edges+1)`, mặc định `max_edges = 100`.
- Chỗ tốn kém thật nằm ở `COMEBin/leiden_grid.py`: lưới **3 partgraph_ratio × 5 bandwidth × 8 resolution = 120 lần chạy Leiden**, rồi mới chọn kết quả. Cộng với phần học biểu diễn đối sánh đa view trên GPU.

Khoảng trống đã **dịch sang chỗ khác nhưng vẫn còn**: chọn tham số phân cụm có nguyên tắc thay cho lưới 120 lần, và làm bước này chạy nổi ở quy mô triệu contig.

## Rủi ro chính

- **Khớp GVHD yếu nhất trong mọi ứng viên:** trong 14 công trình của GVHD **không có bài nào về metagenomics** ([advisor-research.md](../../project/advisor-research.md)). Đây là rủi ro lớn hơn cả G2.
- **Không đáp ứng kỳ vọng "kiến trúc chưa ai dùng"** (GVHD, 11/10) — cùng rủi ro với [C-3](../../DECISIONS.md).
- Hướng "chọn cạnh thích nghi theo độ dài contig" có tiền lệ gần: **CoCoBin** (bioRxiv 08/2025) gom contig theo khoảng độ dài trước khi tính tương đồng rồi chạy Louvain; **METAMVGL** (2021) học trọng số giữa hai loại đồ thị.
- Nút thắt coverage đa mẫu **đã được giải quyết** bởi Fairy (*Microbiome* 2024): thay alignment bằng sketch k-mer, nhanh hơn >250×. Không nên nhắm vào bước này.
- **Hạ tầng:** CAMI II cần vài trăm GB dung lượng và RAM lớn. Chưa kiểm máy của Trọng có đủ không.
- Quy ước ngôn từ: **không nói "baseline xây ma trận toàn cặp"** — COMEBin không làm vậy. Không nói "đầu tiên dùng ANN cho binning".

## Việc tiếp theo

1. Quyết định xem rủi ro "GVHD không có nền trong metagenomics" có chấp nhận được không. Nếu không thì đóng hướng này ngay, trước khi tải dữ liệu.
2. Nếu tiếp tục: đo nút thắt COMEBin trên một mẫu CAMI II nhỏ — thời gian từng bước (học biểu diễn, HNSW, 120 lần Leiden) để xác nhận nút thắt thật.
3. Đọc toàn văn QuickBin 2026 và bảng runtime/RAM của Han et al. *Nat Commun* 2025 (Supplementary Table 6).

## Trong thư mục này

- [log.md](log.md) — nhật ký nghiên cứu
- [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md) — kiểm giả định bản mô tả gốc, đọc mã nguồn COMEBin, bảng tiền lệ
