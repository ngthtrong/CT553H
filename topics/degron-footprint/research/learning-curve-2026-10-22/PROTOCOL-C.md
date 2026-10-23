# Tiền đăng ký C — độ nhạy ngưỡng degron, cov50 và `RESCUE_DELTA`

Chốt **trước khi chạy** phần C. Nối tiếp [PROTOCOL.md](PROTOCOL.md) (phần A) và [PROTOCOL-B.md](PROTOCOL-B.md) (phần B). Phần C **không** sửa tiêu chí hay kết luận của A/B.

## 1. Vì sao cần một lưới duy nhất, báo cùng lúc

`[ĐO]` Phần A chạy **một** ngưỡng nới duy nhất, 4,0, chốt trước, và nó đạt (+0,0126 ở ridge). Nguy cơ hiển nhiên nếu đi tiếp mà không ràng buộc: chạy lần lượt 3,5 rồi 4,5 rồi 5,0, thấy cái nào đẹp thì báo cái đó. Đó là **dò ngưỡng**, và nó sẽ làm mọi CI trong báo cáo mất nghĩa.

`[ĐỀ XUẤT]` Ràng buộc chốt trước, gồm ba điều:

1. **Cả bốn ngưỡng 3,5 / 4,0 / 4,5 / 5,0 được chạy trong một lượt và báo đầy đủ trong cùng một bảng**, kể cả ngưỡng cho kết quả xấu. Không có ngưỡng nào được bỏ khỏi báo cáo sau khi đã thấy số.
2. **Không chọn cấu hình từ lưới này.** Cấu hình đã tiền đăng ký của đề tài vẫn là **4,0** theo phần A. Phần C là **phân tích độ nhạy**, mục đích là biết *hình dạng* của quan hệ ngưỡng–lợi ích, không phải để tìm ngưỡng tốt nhất. Nếu sau này muốn đổi cấu hình chính sang ngưỡng khác, việc đó phải qua một thủ tục chọn **lồng trong outer-train** hoặc một tiền đăng ký mới, không được lấy số trong bảng này.
3. Mọi mức dùng **đúng outer-test của benchmark G2** (91 peptide, miền ngưỡng 3,0); peptide nới ngưỡng **chỉ vào outer-train**, như phần A.

## 2. Lưới, chốt trước

| Trục | Giá trị | Vai trò |
|---|---|---|
| Ngưỡng `DEGRON_PSI_MAX` của nhãn **thêm vào train** | base (không thêm), 3,5, **4,0**, 4,5, 5,0 | Chính |
| Phân cụm định nghĩa fold và bootstrap | **cov80** (chính), cov50 (độ nhạy) | Độ nhạy |
| `RESCUE_DELTA` khi nhị phân hóa ô để tính AUROC | 0,5, **1,0**, 1,5 | Độ nhạy |
| Mô hình | **ridge M3** (chính), `gate_no_pap` (phụ) | — |
| Seed | 17, 29, 43 | — |

`[ĐỀ XUẤT]` Để giới hạn chi phí mà không mất phép so chính:

- **ridge** chạy **toàn lưới** ngưỡng × {cov80, cov50}; AUROC được tính lại ở cả ba `RESCUE_DELTA` **từ cùng một bộ dự đoán** (đổi `RESCUE_DELTA` chỉ đổi cách nhị phân hóa nhãn khi đánh giá, **không** đổi việc huấn luyện, vì mô hình hồi quy trên ΔPSI liên tục).
- **`gate_no_pap`** chỉ chạy trục ngưỡng ở **cov80**, đánh giá ở cả ba `RESCUE_DELTA`.
- Phân cụm cov50 đọc trực tiếp `interim/protein-id30-cov50_cluster.tsv`; **không** sửa `residue_data.load_clusters()` vì nhiều script khác phụ thuộc nó.

`[ĐO]` Lưu ý về cov50, phải nói trước: đổi phân cụm **đổi cả phép chia outer**, nên AUROC tuyệt đối dưới cov50 **không** so trực tiếp được với 0,8082. Dưới cov50, đại lượng có nghĩa là **delta trong cùng thiết kế cov50** (ext − base), không phải giá trị tuyệt đối.

## 3. Tiêu chí kết luận, chốt trước

Gọi Δ(t) = A(ext ở ngưỡng t) − A(base), ghép cặp theo cụm, bootstrap 5.000 lần, trên cấu hình chính (cov80, `RESCUE_DELTA` = 1,0, ridge).

**C1 — hình dạng quan hệ ngưỡng–lợi ích.**
- **"Lợi ích còn tăng theo ngưỡng"** khi Δ(3,5) ≤ Δ(4,0) ≤ Δ(4,5) ≤ Δ(5,0) (không giảm) **và** CI của cả bốn đều > 0.
- **"Bão hòa tại t\*"** khi CI của Δ(t\*) > 0 và các ngưỡng cao hơn t\* không tăng thêm quá 0,002 điểm AUROC.
- **"Suy giảm sau t\*"** khi tồn tại t > t\* với Δ(t) < Δ(t\*) − 0,002.
- Hình dạng không thuộc ba dạng trên → mô tả nguyên trạng, không ép vào khuôn.

**C2 — độ bền của cấu hình đã tiền đăng ký (ngưỡng 4,0).** Gọi là **"bền"** khi Δ(4,0) có CI > 0 ở **tất cả** các điều kiện sau:
- cov80 với `RESCUE_DELTA` ∈ {0,5; 1,0; 1,5};
- cov50 với `RESCUE_DELTA` = 1,0.

Nếu một điều kiện nào không đạt → ghi **"bền có điều kiện"**, nêu đúng điều kiện nào hỏng và số của nó. Không được gọi là bền nếu chỉ cấu hình chính đạt.

**C3 — nhất quán giữa hai mô hình.** Chỉ ghi "hai mô hình đồng thuận về hình dạng" khi dấu và thứ tự của Δ(t) trùng nhau ở cả hai mô hình. Lệch → báo lệch.

## 4. Bắt buộc báo kèm

Với từng ngưỡng: số peptide thêm, số **cụm cov80 mới**, tỉ lệ ô dương (ở `RESCUE_DELTA` = 1,0), trung vị PSI(WT) của nhóm thêm, số ô bị loại từng fold do trùng cụm test. Với cov50: số cụm của bộ 91 peptide dưới cov50 và danh sách cụm test từng fold.

## 5. Việc không làm

- Không chạy ngưỡng nào ngoài bốn giá trị trên; không chạy thêm ngưỡng sau khi đã xem kết quả.
- Không đổi cấu hình chính của đề tài dựa vào bảng này (§1.2).
- Không thêm mô hình thứ ba, không sửa `residue_data.py`, không tính lại ΔPAP.
- Không chuyển sang nguồn dữ liệu ngoài trong phần C; đó là việc sau, theo [kế hoạch](../next-steps-plan-2026-10-22/README.md) P2.
- Không sửa đề cương, slide, hay trạng thái G2/G3.
