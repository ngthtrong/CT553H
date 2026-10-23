[← Danh mục bài báo](README.md) · Về hub

# MaveDB — bộ dữ liệu 4, kiểm trên protein nguyên vẹn

| | |
|---|---|
| **Là gì** | Cơ sở dữ liệu các thí nghiệm MAVE (multiplexed assays of variant effect) |
| **Truy cập** | qua API |
| **Giấy phép** | **CC0** |
| **Mức kiểm** | **[TỰ KIỂM]** — đã đếm qua API |
| **Đã tải?** | ❌ **chưa** |

---

## Vai trò trong đề tài

Đây là bộ dữ liệu **thứ tư**, dùng để kiểm mô hình trên **protein nguyên vẹn** thay vì peptide tách rời.

| | Số lượng |
|---|---:|
| Biến thể duy nhất | **69.209** |
| **Gene dùng được** | **chỉ 9** |
| Đơn vị nhãn | độ dồi dào protein |

## Vì sao cần bộ này dù chỉ có 9 gene

Vì nó giải quyết **giới hạn lớn nhất của dữ liệu chính**: nhãn của bộ 2 và 3 là peptide **tách rời** (cắt ra khỏi protein, gắn vào GFP). Một peptide tách rời luôn lộ ra hoàn toàn, nên E3 luôn thấy nó. Nhưng trong protein nguyên vẹn, cùng đoạn đó có thể bị **gập vào bên trong** và không bao giờ bị nhận ra.

MaveDB cho phép kiểm: mô hình học từ peptide tách rời có nói được gì về protein thật không?

Đây cũng là lý do thiết kế **cổng phơi lộ** ở bài 6: peptide tách rời → đặt cổng "phơi lộ hoàn toàn"; protein nguyên vẹn → đặt rASA thật. Cùng một mô hình chạy cả hai chế độ.

## Giới hạn phải nói rõ

**9 gene là rất ít.** Không thể dùng bộ này làm thước đo chính. Nó là **phép kiểm định tính** về khả năng chuyển sang protein thật, không phải benchmark.

Và: thang đo khác (độ dồi dào protein, không phải PSI 1–6), nên không so chỉ số trực tiếp giữa bộ này và bộ 2.

## Việc cần làm

1. **Tải** — chưa làm.
2. Kiểm xem 9 gene đó có trùng với protein nào trong tập huấn luyện không. Nếu trùng thì phải giữ cùng phía khi chia tập, giống cách xử lý 130/248 peptide trùng giữa bộ quét và bộ bão hòa (bài 4).
3. Đối chiếu thang đo giữa hai nguồn trước khi so sánh bất cứ con số nào.

---

[← Danh mục bài báo](README.md) · Về hub
