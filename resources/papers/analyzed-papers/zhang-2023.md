[← Danh mục bài báo](README.md) · Về hub

# Zhang 2023 — đột biến quét và bão hòa trên degron

| | |
|---|---|
| **Nơi công bố** | *Molecular Cell*, 2023 |
| **Dữ liệu** | Mendeley Data [`10.17632/32h94v2yv2.2`](https://data.mendeley.com/datasets/32h94v2yv2/2), **CC BY 4.0** |
| **Giấy phép bài báo** | **All rights reserved** (Elsevier) → **không sao chép hình**, chỉ dẫn link |
| **Mức kiểm** | **[TỰ KIỂM]** — đã tải, kiểm SHA-256, tự đếm lại toàn bộ |

---

## Bài này làm gì

Đo ảnh hưởng của **đột biến** lên sức mạnh degron, ở quy mô lớn. Hai thí nghiệm:

- **Quét (scanning):** mỗi vị trí thử một acid amin thay vào, trên rất nhiều peptide
- **Bão hòa (saturation):** mỗi vị trí thử cả 19 acid amin, trên ít peptide hơn

Kèm theo: 31 sàng lọc CRISPR để tìm **E3 nào** phụ trách degron nào.

## Vì sao đây là bài quan trọng nhất về dữ liệu

Vì nó là **nguồn nhãn chính của đề tài**. Nhãn của Voutsinos là nhãn *mức đoạn* (một điểm cho cả tile), còn nhãn của Zhang là nhãn *mức residue* — đúng thứ đề tài cần dự đoán.

## File đã tải và kiểm [TỰ KIỂM]

| File | Kích thước | SHA-256 |
|---|---:|---|
| `I28 Scanning Mutagenesis.zip` | 27.939.862 B | `a82bd1ee4bc7a2da69df06cb44dd34fe8480c6fd799340684f5058d02223df50` |
| `I28 CRL Saturation Mutagenesis.zip` | 5.224.902 B | `cbda58342265dd73b7946cd091c5b558eed6e615bbcb97921e37bd50fbb5ee60` |

File chính: `Replicate 1 (BAG6 genotype unclear)/I28 Scanning Mutagenesis Replicate 1.csv`.

## Con số tự đếm (không dẫn lại từ bài báo)

**Bộ quét:**

| | Số đếm |
|---|---:|
| Dòng thô | 283.880 |
| Dòng đạt lọc (reads ≥ 10) | **256.711** |
| Peptide có WT và đột biến đạt lọc | 8.831 |
| Peptide là degron | 3.439 |
| **Peptide có footprint** | **2.624** |
| Footprint **khu trú** | 2.402 |
| **Trung vị vị trí quan trọng** | **3 trên 28** |

**Bộ bão hòa:** 135.040 định danh / **249 peptide** (239 phủ ≥ 27 vị trí). Nhưng chỉ **219 footprint** được tác giả curate — xem cảnh báo ở bài 4.

**Nhãn E3 — và đây là phát hiện buộc đổi trục đề tài:**

| | Số đếm |
|---|---:|
| Sàng lọc CRISPR | 31 |
| Gán được adaptor | 27 (gán rõ: 25) |
| **Số E3 khác nhau** | **10** |
| **Số E3 có ≥ 5 peptide** | **1** (KLHL15, 13 peptide) |
| Số E3 có đúng 1 peptide | **6** |

Bền với **36 tổ hợp ngưỡng**: số E3 có ≥ 5 peptide **luôn đúng bằng 1**.

> **Vì sao phải lấy dữ liệu thô:** Table S1–S7 trên PMC bị chặn bằng reCAPTCHA, và Europe PMC trả về *"not open access"*. Nên phải đếm từ dữ liệu MAGeCK **thô** trên Mendeley mà chính bài khai báo.
>
> **Giới hạn:** chưa lấy được **Table S5** (bảng gán E3 do tác giả curate, gồm cả "individual testing"), nên **10 E3 là giới hạn dưới**. Nhưng Table S5 chỉ thêm peptide, không đổi được việc 6 lớp có một mẫu.

## Cái bài này buộc đề tài phải bỏ

Trục **"dự đoán đặc hiệu E3"** — tức dự đoán E3 nào nhận ra degron nào. Với 10 lớp mà 6 lớp có một mẫu, không huấn luyện được. Trục này **đã bỏ ngày 11/10/2026**. E3 chỉ còn vai trò **ca nghiên cứu** trên 23 peptide có cả nhãn E3 và bản đồ bão hòa.

## Chồng lấn cần biết khi chia tập

- **27/31** peptide CRISPR có bản đồ bão hòa; 4 peptide thiếu là 4 peptide BAG6
- Trong 27 peptide được gán E3, chỉ **23** có bản đồ bão hòa
- **130/248** peptide bão hòa có mặt trong bộ quét → **phải giữ cùng phía khi chia tập**

## Quy ước ngôn từ

- **Không nói "16 E3 có nhãn CRISPR"** — con số đó sai
- Không gọi 135.040 định danh là 135.040 ΔPSI đã xác nhận
- 256.711 là **số dòng đo**, không phải số mẫu sinh học độc lập

## Nguồn trong repo

- [e3-labels-audit/](../../topics/degron-footprint/research/e3-labels-audit/README.md) — 7 script đếm + JSON kết quả
- [composition-context-audit.md](../../topics/degron-footprint/research/composition-context-audit.md) — audit thành phần, cận, chia cụm

---

[← Danh mục bài báo](README.md) · Về hub
