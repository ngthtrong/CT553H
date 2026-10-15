# Nhật ký đề tài `scalable-metagenomic-binning`

> Mới nhất ở trên. Trạng thái hiện hành chỉ ghi ở [DECISIONS.md](../../DECISIONS.md).

---

## 12/10/2026 — mở hồ sơ, đọc mã nguồn COMEBin

- Nguồn: Trọng dán bản mô tả "Lựa chọn 2" vào phiên làm việc. Bản mô tả không rõ nguồn gốc (link có `utm_source=chatgpt.com`); mọi đóng góp trong đó là giả thuyết cần kiểm chứng.
- **[TỰ KIỂM]** Clone `ziyewang/COMEBin` commit `1b476a4` (23/08/2026) và đọc `cluster.py`, `leiden_grid.py`, `main.py`. Hai phát hiện:
  1. **Đóng góp A của bản mô tả đã nằm trong baseline.** COMEBin dùng `hnswlib` (HNSW = ANN): `init_index(ef_construction=max_edges*10, M=16)` rồi `knn_query(..., max_edges+1)`, mặc định `max_edges = 100`. Không được nói "baseline xây ma trận toàn cặp" — bản mô tả gốc đã tự cảnh báo điều này và cảnh báo đó đúng.
  2. **Nút thắt thật là lưới 120 lần Leiden:** `LEIDEN_PARTGRAPH_RATIOS` (3) × `LEIDEN_BANDWIDTHS` (5) × `LEIDEN_RESOLUTIONS` (8), mỗi lần `n_iterations=-1`. Cắt cạnh hiện tại là **một ngưỡng phân vị toàn cục** (`np.percentile(distances, partgraph_ratio)`), chưa thích nghi theo contig — nên hướng B của bản mô tả còn chỗ.
- Bằng chứng độc lập về quy mô: Han et al. *Nat Commun* 2025 — COMEBin (GPU) **không xong trong 2 tuần** ở 6,3 triệu contig; QuickBin 2026 — **COMEBin lỗi 129/297 mẫu thật (43%)**. Đây là vấn đề thật, đo được.
- Đối thủ trực tiếp cần đọc kỹ: **QuickBin** (Bushnell & Villada 2026) **bỏ hẳn đồ thị kNN**, dùng lưới chỉ mục GC + log-coverage với cascade bộ lọc thoát sớm; 55 triệu contig xong trong 10 h 56 phút. Yếu hơn rõ trên PacBio (76 MAG so với 206 của SemiBin2).
- Nút thắt coverage đa mẫu **đã bị giải quyết** bởi Fairy (*Microbiome* 2024, nhanh hơn >250×). Không nhắm vào bước đó.
- **Rủi ro lớn nhất không phải kỹ thuật:** trong 14 công trình của GVHD **không có bài nào về metagenomics**. Đây là ứng viên khớp GVHD yếu nhất trong repo. Câu hỏi này phải trả lời trước khi tải vài trăm GB dữ liệu CAMI II.
- Chi tiết ở [research/deep-dive-2026-10-12.md](research/deep-dive-2026-10-12.md). Chưa tải dữ liệu, chưa chạy baseline.
