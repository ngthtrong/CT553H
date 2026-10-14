[← Bài trước](07-evaluation.md) · Bài 8/10 · [Bài sau: Rủi ro →](09-risks.md)

# Bài 8 — Đóng góp nếu nghiên cứu hoàn thiện thành công

> Bài này viết ở **thể điều kiện**: *nếu* làm xong thì đóng góp là gì. Hiện **chưa huấn luyện mô hình nào**, nên chưa có đóng góp nào đã xác lập. Cổng G2 vẫn ở trạng thái **chưa xác lập** ([thẻ đề tài](../../topics/degron-footprint/README.md)).

---

## 1. Câu đóng góp, viết một dòng

> Em xây một mô hình dự đoán **vị trí nào trong degron quyết định độ bền protein**, trên nhãn đột biến thực nghiệm. Mô hình đạt precision@3 = **X**, so với **0,6045** là trần đã chứng minh của lớp mô hình chỉ dùng thành phần acid amin, và **0,7792** là mức tối đa đạt được trên tập này.

Giá trị `X` là thứ chưa biết. Toàn bộ đề tài là để tìm ra nó.

Câu này tốt ở ba điểm:

1. **Có mốc so sánh đã chứng minh**, không phải "tốt hơn baseline" chung chung.
2. **Có trần**, nên không hứa quá.
3. **Nhãn là thực nghiệm**, nên không ai hỏi "nhãn ở đâu ra".

---

## 2. Đóng góp đối chiếu năm tiêu chí GVHD

Nguồn năm tiêu chí: [course.md](../../project/course.md).

| # | Tiêu chí | Đề tài đáp ứng thế nào | Mức |
|---|---|---|---|
| 1 | **Tính mới** | Khoảng trống **đã chứng minh**, không phải phỏng đoán: 89,7% peptide mà mô hình thành phần không tách được. Nhưng tính mới của *kiến trúc* chỉ ở chỗ ghép, không ở cơ chế | Trung bình–cao |
| 2 | **Đề xuất / cải tiến phương pháp** | MIL + attention có cổng + cổng phơi lộ đặt ở bước gộp, thay global average pooling của PAP | **Có** |
| 3 | **Sử dụng phương pháp mới** | Embedding PLM **mức residue**, không gộp trước — khác mọi mô hình degron đã công bố | **Có** |
| 4 | **XAI** | **Thoả mãn bởi chính bài toán.** Đầu ra *là* điểm quan trọng theo residue. Không cần gắn thêm SHAP hay IG | **Mạnh nhất** |
| 5 | **Ứng dụng / website** | Web nhập peptide → bản đồ residue + ma trận 28×20 + top-3. **Không thể thiếu** | Yếu nhất, phải thiết kế |

![Đóng góp đối chiếu năm tiêu chí và ba cổng](figures/fig-13-contribution.svg)

*Sơ đồ tự dựng.*

**Tiêu chí 4 đáng nói riêng.** Ở các ứng viên khác trong repo, XAI phải gắn thêm như một phần phụ. Ở degron, **đầu ra của mô hình chính là lời giải thích** — "vị trí 8, 11, 17 là chỗ quyết định" vừa là dự đoán vừa là diễn giải. Đây là lợi thế thật, và nên nhấn mạnh khi báo cáo.

---

## 3. Ba cổng bắt buộc

| Cổng | Trạng thái | Căn cứ |
|---|---|---|
| **G1** nhãn độc lập | **ĐẠT, mạnh nhất repo** | Toàn bộ là nhãn thực nghiệm: điểm tile từ reporter assay, PSI từ sàng lọc, 219 footprint từ bão hòa. Không nhãn nào do pipeline của đề tài sinh ra |
| **G2** đóng góp dương | **CHƯA XÁC LẬP** | Chưa huấn luyện mô hình nào. Khoảng trống đã chứng minh, nhưng *khoảng trống* khác *đóng góp đã đo được* |
| **G3** ứng dụng | **ĐẠT, nhưng yếu nhất** | Ba sản phẩm đã tồn tại, nên phải khác biệt được |

Về G1, một so sánh đáng nhớ: hướng **TME senescence** của repo đã **bị đóng** vì trượt đúng cổng này — nhãn SenMayo của nó do chính pipeline sinh ra ([D-008](../../DECISIONS.md#d-008)). Degron không có vấn đề đó.

---

## 4. Đóng góp cho ai, dùng vào gì

### Cho nhà sinh học thực nghiệm

Họ chỉ làm được vài thí nghiệm trên mỗi peptide. Mô hình nói "thử vị trí 8, 11, 17" giúp họ **giảm số thí nghiệm phải làm**. Đây là giá trị trực tiếp nhất và cũng dễ giải thích nhất.

### Cho việc diễn giải biến thể gây bệnh

Các mô hình như [AlphaMissense](papers/alphamissense-2023.md) nói "biến thể này có hại" nhưng **không nói vì sao**. Nếu mô hình của đề tài chỉ ra rằng biến thể đó **tạo ra hoặc phá vỡ một degron**, thì đó là một **cơ chế cụ thể** — không chỉ một điểm số.

Đây là bổ sung, **không phải thay thế**. Phải nói rõ điều này.

### Cho hướng thuốc phân hủy protein đích

Có một hướng thuốc cố tình dán degron vào protein gây bệnh để tế bào tự phá nó. Hiểu residue nào làm degron mạnh là kiến thức nền cho việc thiết kế. Nhưng đây là **ý nghĩa xa**, không phải thứ luận văn chứng minh được — nên nhắc một câu, không hứa.

---

## 5. Sản phẩm cụ thể khi bảo vệ

| Sản phẩm | Nội dung |
|---|---|
| **Mô hình** | Trọng số + mã huấn luyện, chạy lại được |
| **Benchmark** | Giao thức chia tập theo cụm protein, kèm cả baseline thành phần và các oracle/cận. Đây là thứ người sau có thể dùng lại |
| **Ứng dụng web** | Nhập peptide → bản đồ residue, heatmap 28×20, top-3 vị trí |
| **Báo cáo tái lập** | Script + config + seed cố định, mọi số trong luận văn trỏ được về một file kết quả |
| **Ca nghiên cứu E3** | 23 peptide, định tính |

Phần **benchmark** có giá trị riêng đáng nhắc: hiện chưa có giao thức chuẩn nào cho bài toán footprint degron có kiểm soát đồng dạng. Kể cả khi mô hình không thắng nhiều, giao thức và các cận (0,1204 / 0,6045 / 0,7792) vẫn là thứ dùng được cho người sau.

Nhưng **không được đặt đó làm đóng góp chính** — GVHD không nhận một bảng đối chứng làm đóng góp chính ([D-012](../../DECISIONS.md#d-012)).

---

## 6. Kết quả âm thì sao

Phải nghĩ trước, vì khả năng này thật.

**Nếu mô hình không vượt 0,6045:** đó là kết quả âm, và GVHD **không nhận kết quả âm làm đóng góp chính** ([D-012](../../DECISIONS.md#d-012)). Khi đó phải:

1. Kiểm xem lý do là **lực thống kê** (n ≈ 250 quá nhỏ) hay **tín hiệu không có** (phần dư 35,0% chỉ là nhiễu).
2. Nếu là nhiễu đo → chuyển sang bộ bão hòa chất lượng cao hơn, hoặc bộ nhân của [Larsen 2025](papers/larsen-2025.md) (58.781 đoạn / 1.626 TF, **chưa tải**, cần kiểm giấy phép CC BY-NC-ND trước).
3. Nếu vẫn không được → kích hoạt đề tài dự phòng [plm-calibration-audit](../../topics/plm-calibration-audit/README.md) ([D-023](../../DECISIONS.md#d-023)).

**Nếu đầu hồi quy theo vị trí đơn thuần đã đủ tốt, không cần MIL:** đó vẫn là kết quả **phải báo**, không phải thất bại cần che. Khi đó đóng góp chuyển sang "mô hình đơn giản này đủ, và đây là mốc" — yếu hơn, nhưng trung thực và vẫn vượt 0,6045.

---

[← Bài trước](07-evaluation.md) · [Bài sau: Rủi ro →](09-risks.md)
