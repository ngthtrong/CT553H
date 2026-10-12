# Dữ liệu RTK–ATP đã tải và kiểm tra

> **LƯU TRỮ — không dùng để ra quyết định.** Tài liệu lịch sử; mọi câu "chốt / quyết định / khuyến nghị" bên dưới đã hết hiệu lực. Trạng thái hiện hành: [DECISIONS.md](../../../../DECISIONS.md).

Kiểm tra ngày 01/10/2026. **Đã tải dữ liệu thực**, chưa trích xuất embedding, huấn luyện, căn chỉnh đồng dạng hoặc tạo split cuối.

## 1. Nguồn và khả năng tái lập

- Repo tác giả: [B1607/RTK_RAG](https://github.com/B1607/RTK_RAG).
- Snapshot: [`b7bd4c2347c7d44d24ae3d13e42082ba6cd62627`](https://github.com/B1607/RTK_RAG/tree/b7bd4c2347c7d44d24ae3d13e42082ba6cd62627).
- ZIP gốc: `archive/topics/rtk-atp-applicability/data/raw/rtk-rag-b7bd4c2347c7d44d24ae3d13e42082ba6cd62627.zip`.
- SHA-256 ZIP: `a82015b5b8a23ef0634decc22bd27f00392e34fd40f4f3e10a21365f686287d4`.
- Bản giải nén: `archive/topics/rtk-atp-applicability/data/raw/rtk-rag/`; giữ nguyên dữ liệu, README, LICENSE và mã nguồn đi kèm. Không thực thi mã tác giả.
- Giấy phép được repo công bố: Academic Free License v3.0; bản LICENSE gốc được giữ cùng dữ liệu.
- [Manifest từng tệp](source-manifest.json), [kết quả kiểm tra máy đọc được](audit-summary.json), [bảng thống kê CSV](dataset-summary.csv).

Chạy lại từ thư mục gốc, dùng Python 3 và thư viện chuẩn:

```bash
python3 archive/topics/rtk-atp-applicability/code/preprocessing/prepare_data.py
```

Script dùng ZIP đã có; trên máy mới sẽ tải đúng snapshot và kiểm SHA-256. Có thể cung cấp ZIP có sẵn bằng `--archive /path/to/archive.zip`. Nếu mạng của môi trường bị chặn, phải cho phép tải mạng trước. Script không tự sửa tệp raw đã thay đổi.

## 2. Quy mô thực đo

| Bộ dữ liệu | Số bản ghi | Chuỗi duy nhất trong bộ | Residue | Nhãn 1 | Nhãn 0 | Tỷ lệ dương |
|---|---:|---:|---:|---:|---:|---:|
| ATP-549 | 549 | 549 | 213.537 | 8.502 | 205.035 | 3,9815% |
| RTK-69 | 69 | 69 | 73.981 | 711 | 73.270 | 0,9611% |
| RAG-244 | 244 | 243 | 263.764 | Không có tệp nhãn | Không có tệp nhãn | Chưa kiểm chứng từ nhãn |
| Tổng | **862** | **861 trên cả ba bộ** | **551.282** | — | — | — |

Các số trên được script đếm từ tệp tải về, không phải kết quả mô hình. README/bài báo ghi kho RAG có 2.676 residue dương và 261.088 âm, nhưng snapshot **chỉ cung cấp FASTA của kho này**; không chuyển các số công bố đó thành ground truth có sẵn.

| Bộ | Min / trung vị / max chiều dài | Số chuỗi > 1.000 aa |
|---|---|---:|
| ATP-549 | 105 / 356 / 1.164 | 2 |
| RTK-69 | 488 / 977 / 2.594 | 30 |
| RAG-244 | 292 / 993 / 2.554 | 115 |

## 3. Kiểm tra chất lượng đã hoàn thành

- Toàn bộ **618 protein có nhãn** có số nhãn bằng chiều dài chuỗi, nhãn chỉ gồm 0/1; không thiếu cặp FASTA–label; mỗi protein đều có ít nhất một nhãn dương.
- Không phát hiện chuỗi trùng hoàn toàn giữa ATP-549, RTK-69 và RAG-244; không có ID chung giữa các bộ.
- Một cặp trùng **nội bộ kho RAG**: `A0M8S8` và `Q07E37`. Phải gộp thành một chuỗi khi dựng kho thực nghiệm; giữ bảng alias để truy nguyên.
- Không phát hiện xung đột nhãn giữa các chuỗi trùng có nhãn trong snapshot. Kết quả này không xác minh tính đúng sinh học của nhãn.
- Kho RAG có **36 ký tự X**. Giữ nguyên vị trí; không xóa residue hoặc dịch nhãn. Ghi lại quy tắc tokenization của ProtT5 khi trích xuất.
- **Chưa kiểm tra homolog bằng alignment.** “Không trùng hoàn toàn” không có nghĩa đã độc lập ở ngưỡng 30%/40% identity.

## 4. Vai trò trong đề tài

| Tài nguyên | Vai trò dự kiến | Điều kiện sử dụng |
|---|---|---|
| ATP-549 | Nguồn có nhãn để học MCNN và làm baseline k-NN | Chia theo protein/cluster, chỉ training partition được cung cấp nhãn cho k-NN |
| RTK-69 | Dữ liệu đích để phát triển cảnh báo và đánh giá RTK | Tách RTK-development và RTK-test trước khi huấn luyện; không còn gọi toàn bộ 69 là independent test của đề tài |
| RAG-244 | Kho embedding ngoài, không dùng nhãn | Gộp trùng, loại self-match, lọc homolog theo từng giao thức, đóng băng phiên bản |

Không cần tải thêm DNA/RNA/FAD/GEO cho phạm vi đã chốt. ATP-202 từ [ATP-Deep](https://github.com/jerry1984Y/ATP-Deep) chỉ là phương án mở rộng đánh giá ATP nói chung nếu cần; **chưa tải, không phải bộ RTK thay thế và không mặc định độc lập với dữ liệu hiện có**.

## 5. Tệp đã chuẩn hóa

Trong `archive/topics/rtk-atp-applicability/data/processed/`:

- `atp-549.fasta`, `rtk-69.fasta`, `rag-244.fasta`: FASTA gộp theo bộ, ID có tiền tố tên bộ.
- `proteins.jsonl`: mỗi dòng là một protein, chứa sequence, labels hoặc `null`, độ dài, số dương, hash chuỗi và nguồn.
- `protein-index.csv`: bảng chỉ mục, không nhân bản thành hàng trăm nghìn cửa sổ residue.

Đây là **bản chuẩn hóa bảo toàn toàn bộ bản ghi**, chưa loại cặp trùng RAG, chưa chia tập, chưa thay đổi nhãn. Raw và processed đều được `.gitignore` loại khỏi Git; manifest và thống kê nhỏ được lưu trong tài liệu để kiểm chứng.

## 6. Chi phí và việc còn phải làm

551.282 residue × 1.024 chiều × 2 byte ≈ **1,129 GB thập phân** embedding float16 trước khi gộp trùng; float32 gấp đôi. Đây là tính toán dung lượng mảng, không phải đo RAM/VRAM hay thời gian thực tế. Không lưu tensor cửa sổ mở rộng cho toàn bộ dữ liệu; tạo cửa sổ theo batch.

Việc tiếp theo: kiểm provenance nhãn/ánh xạ accession, dựng alignment và báo identity/coverage toàn chuỗi cùng vùng kinase, lập manifest split, đo GPU trên chuỗi dài, rồi mới tải trọng số ProtT5 và trích xuất embedding. Việc tải dữ liệu lần này không bao gồm trọng số PLM hoặc mô hình đã huấn luyện.
