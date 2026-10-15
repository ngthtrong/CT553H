[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# AlphaMissense 2023 — và chỗ đề tài khác nó

| | |
|---|---|
| **Nơi công bố** | *Science*, 2023 |
| **PubMed** | <https://pubmed.ncbi.nlm.nih.gov/37733863/> |
| **Mức kiểm** | **[NGUỒN]** — đọc tóm tắt |
| **Giấy phép** | không mở → chỉ dẫn link |

---

## Bài này làm gì

Dự đoán **độc tính** của biến thể missense ở quy mô proteome: biến thể này có khả năng gây bệnh hay lành tính. Là một trong những mô hình mạnh nhất cho bài toán đó.

## Vì sao có trong danh mục

Vì nó là chỗ dễ bị hỏi nhất: *"đã có AlphaMissense rồi, em làm thêm gì?"*

Câu trả lời nằm ở **loại câu hỏi**, không ở chất lượng mô hình:

| | AlphaMissense | Đề tài |
|---|---|---|
| Trả lời | biến thể này **có hại không** | biến thể này **làm gì** với độ bền |
| Đơn vị | biến thể trên protein nguyên vẹn | residue trong một đoạn degron |
| Đầu ra | một điểm độc tính | bản đồ theo residue + ma trận thay thế |
| Cơ chế | **không nói vì sao** | **nói vì sao**: tạo ra hoặc phá vỡ degron |

**Câu phát biểu đúng:** đề tài **bổ sung cơ chế**, **không thay thế** mô hình độc tính biến thể. Điều này ghi rõ trong phạm vi đề tài ([topic-decision.md mục 3](../../../topics/degron-footprint/research/topic-decision.md)): *"Không thay thế mô hình dự đoán độc tính biến thể; chỉ bổ sung cơ chế."*

## Một bối cảnh đáng biết

Cùng nhóm bài toán này còn có **ESM1b** của Brandes 2023 (*Nature Genetics*), đã tính sẵn điểm cho **toàn bộ ~450 triệu biến thể missense** của người, công khai.

Điều đó là lý do một ứng viên đề tài khác của repo — [budgeted-plm-variant-scoring](../../../archive/topics/budgeted-plm-variant-scoring/README.md) — gặp vấn đề về lý do nghiên cứu: với biến thể đơn, bảng điểm đã có sẵn. Degron **không** gặp vấn đề đó, vì nó trả lời câu hỏi khác (cơ chế mức residue trên nhãn độ bền thực nghiệm), và vì nhãn của nó là ΔPSI đo được, không phải điểm độc tính.

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
