[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# BioBlobs 2025 — bài làm hẹp tuyên bố MIL của đề tài

| | |
|---|---|
| **Nơi công bố** | arXiv, 10/2025 |
| **Link** | <https://arxiv.org/abs/2510.01632> |
| **Mức kiểm** | **[NGUỒN]** — đọc tóm tắt trên trang gốc |

---

## Vì sao bài này quan trọng dù không liên quan degron

Vì nó **đã làm đúng cơ chế mà đề tài định đề xuất**, chỉ khác bài toán.

BioBlobs dùng **attention-based MIL kiểu Ilse 2018 trên protein**:

| Thành phần | BioBlobs |
|---|---|
| Túi (bag) | một protein |
| Thể hiện (instance) | cấu trúc con **học được** |
| Cơ chế gộp | **có cổng attention** |
| Bài toán | dự đoán **chức năng** protein |

So với đề tài: túi là peptide, thể hiện là cửa sổ quanh mỗi vị trí, cũng attention có cổng, bài toán là footprint degron.

→ **Cơ chế là một. Bài toán khác.**

## Hệ quả bắt buộc cho cách phát biểu

**Không được nói:**

- ❌ "Chưa ai dùng MIL cho protein"
- ❌ "Attention-based MIL là kiến trúc mới"
- ❌ "Đề tài đề xuất một cơ chế gộp chưa từng có"

**Phải nói:**

- ✅ *Chưa thấy ai dùng học đa thể hiện cho **degron***
- ✅ *Mới ở **chỗ ghép** và ở **chỗ đặt cổng phơi lộ tại bước gộp***
- ✅ ***Không mới ở cơ chế***

Đây là một trong hai lần tính mới của đề tài bị thu hẹp — xem [bài 9 rủi ro 5](../09-risks.md).

## Mặt tốt của phát hiện này

Phát hiện sớm (11/10/2026, trước khi chốt đề tài) nên không phải sửa muộn. Và nó cho một **tiền lệ kỹ thuật** để dẫn: nếu attention-MIL đã chạy được trên protein cho bài toán chức năng, thì việc nó chạy được cho bài toán footprint là hợp lý — không phải một cược vào cơ chế chưa ai thử.

Khi viết phần khảo sát nghiên cứu trước, bài này nên nằm ở nhóm "tiền lệ phương pháp", không phải nhóm "đối thủ".

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
