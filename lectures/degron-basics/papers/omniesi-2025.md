[← Danh mục bài báo](README.md) · [Về hub](../README.md)

# OmniESI 2025 — tiền lệ cho điều biến có điều kiện

| | |
|---|---|
| **Nơi công bố** | arXiv, 2025 |
| **Link** | <https://arxiv.org/abs/2506.17963> |
| **Mức kiểm** | **[NGUỒN]** — đọc tóm tắt trên trang gốc |

---

## Bài này làm gì

Dự đoán tương tác **enzyme–cơ chất**, dùng **điều biến có điều kiện hai chiều** giữa biểu diễn enzyme và biểu diễn cơ chất. Đây là cùng ý tưởng với **FiLM** (Feature-wise Linear Modulation): một nhánh sinh ra tham số để điều tiết nhánh kia.

## Liên quan đến đề tài ở đâu

Bản thiết kế **trước** của đề tài có một thành phần **điều kiện E3**: dùng biểu diễn của E3 để điều tiết mô hình degron. OmniESI cho thấy cơ chế đó **đã có tiền lệ**.

Thành phần điều kiện E3 sau đó **đã bị bỏ** vì lý do khác — chỉ có 1 E3 đủ mẫu ([Zhang 2023](zhang-2023.md)). Nên bài này giờ ảnh hưởng gián tiếp: nó nhắc rằng **cơ chế điều biến có điều kiện nói chung không phải thứ mới**.

Cổng phơi lộ của đề tài (rASA và pLDDT nhân vào logit attention) cũng là một dạng điều biến có điều kiện. Vậy nên:

> **Không được nói "cổng điều biến là cơ chế mới".** Phần mới chỉ ở **chỗ đặt** nó — tại bước gộp, không phải đầu vào — và ở việc nó cho **cùng một mô hình** giải thích được cả chế độ peptide tách rời và chế độ protein nguyên vẹn.

## Ghi chú về mức bằng chứng

Chỉ đọc tóm tắt, **chưa đọc toàn văn**. Trước khi dẫn bài này trong luận văn, nên đọc kỹ phần phương pháp để mô tả đúng cách họ điều biến — tránh mô tả sai một bài mình chưa đọc.

---

[← Danh mục bài báo](README.md) · [Về hub](../README.md)
