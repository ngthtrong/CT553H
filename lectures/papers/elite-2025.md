[← Danh mục bài báo](README.md) · Về hub

# ELITE 2025 và E3TargetPred — xếp hạng E3 cho substrate

| | |
|---|---|
| **ELITE** | bioRxiv 11/2025 — <https://doi.org/10.1101/2025.11.05.686884> |
| **E3TargetPred** | cùng nhóm bài toán |
| **Mức kiểm** | **[CHƯA KIỂM]** — chỉ thấy qua tóm tắt |

---

## Hai bài này làm gì

Xếp hạng **E3 nào** nhắm vào một protein cho trước, ở **mức cặp protein–protein**. Kiến trúc: ProtBERT kiểu Siamese, giải thích bằng Integrated Gradients.

Nhãn: dương từ mạng tương tác tổ chức theo mô, âm từ **Negatome**. Đánh giá bằng kiểm chứng chéo, **không có tập kiểm tra kiểm soát đồng dạng**.

## Vì sao có trong danh mục này

**Không phải vì chúng là baseline** — đơn vị dự đoán khác hẳn:

| | ELITE / E3TargetPred | Đề tài |
|---|---|---|
| Đơn vị dự đoán | cặp **protein – E3** | **residue** trong peptide |
| Nhãn | mạng tương tác + Negatome | ΔPSI thực nghiệm |
| Câu hỏi | E3 nào nhắm protein này | residue nào quyết định độ bền |

→ **Không phải baseline cùng thang.** Không được so chỉ số trực tiếp.

**Lý do có trong danh mục:** chúng chiếm cùng **khung ứng dụng** — người dùng muốn biết "protein của tôi bị phân hủy thế nào" có thể tìm đến chúng. Nên chúng phải nằm trong bảng khảo sát nghiên cứu trước, ở nhóm riêng.

## Điểm yếu đáng nêu

**Nhãn âm từ Negatome** và **không kiểm soát đồng dạng** — cùng kiểu điểm yếu với [MetaDegron](metadegron-2024.md). Đây là điểm mà đề tài làm tốt hơn thật (nhãn âm là vị trí đo được nhưng ΔPSI thấp; chia tập theo cụm MMseqs2), và nên nêu trong phần đối chiếu.

Nhưng **chỉ nêu sau khi đọc toàn văn**. Hiện là [CHƯA KIỂM].

---

[← Danh mục bài báo](README.md) · Về hub
