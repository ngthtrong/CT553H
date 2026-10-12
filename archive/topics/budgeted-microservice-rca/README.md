# Định vị nguyên nhân sự cố microservice bằng lựa chọn bằng chứng thích ứng theo ngân sách truy vấn

> **Thẻ trạng thái nghiên cứu — tài liệu lưu trữ.** Xem [D-021](../../../DECISIONS.md#d-021). Vị trí của đề tài (chính/dự phòng/đang đào sâu) chỉ ghi ở [DECISIONS.md](../../../DECISIONS.md), không ghi ở đây. Cập nhật lần cuối: **12/10/2026**.

| | |
|---|---|
| Lĩnh vực | AIOps, kỹ nghệ phần mềm, học máy. **Ngoài tin sinh học** |
| Dữ liệu | RCAEval (Hugging Face `phamquiluan/RCAEval`, MIT), 735 ca chèn lỗi trên 3 hệ thống microservice → `archive/topics/budgeted-microservice-rca/data/` |
| Giai đoạn | Đã audit dữ liệu; chưa chạy baseline, chưa huấn luyện, chưa có app |

## Bài toán
Một dịch vụ hỏng có thể kéo theo nhiều dịch vụ khác cùng bất thường. Người trực cần tách nguồn lỗi khỏi hậu quả và quyết định xem tiếp metrics, log hay trace nào. Đề tài **học giá trị của từng truy vấn** `(dịch vụ, nguồn telemetry, cửa sổ thời gian)`, tức mức giảm lỗi xếp hạng nguyên nhân, rồi chọn truy vấn có lợi nhất trong một ngân sách cố định.

- **Đầu vào:** telemetry đa nguồn (metrics/logs/traces) của một sự cố, mốc điều tra, ngân sách.
- **Đầu ra:** thứ hạng dịch vụ nghi ngờ, truy vấn nên mở tiếp theo, đường chất lượng–ngân sách.
- **RQ1:** cùng một ranker, chính sách học giá trị truy vấn có tốt hơn các chiến lược ngẫu nhiên/cố định/theo độ bất thường/theo độ bất định không? **RQ2:** lợi ích có còn khi thiếu nguồn telemetry và khi chuyển sang hệ thống chưa thấy? **RQ3:** phần lợi đến từ chọn truy vấn hay từ dừng sớm?

## Cổng G1/G2/G3
| Cổng | Trạng thái | Bằng chứng |
|---|---|---|
| G1 nhãn độc lập | **Đạt** — nhãn sinh từ fault injection, độc lập với mô hình | [audit dữ liệu](code/preprocessing/README.md): index 735 ca + 6 ca thô; 360 ca RE2/RE3 đa nguồn |
| G2 đóng góp dương | **Chưa có kết quả** | Đã có tiền lệ gần: VerifyRCA, VeriTrail-RCA (budget/truy hồi thích ứng), AFA (ICML 2025) |
| G3 ứng dụng | Có thiết kế khả thi (công cụ điều tra/replay), chưa xây | [topic-decision.md §6](research/topic-decision.md) |

## Rủi ro chính
- **Không khớp chuyên môn GVHD** (tin sinh học), cần hỏi thẳng ở tuần 6. Bối cảnh lựa chọn trước đây: [D-016](../../../DECISIONS.md#d-016); cập nhật ở [D-021](../../../DECISIONS.md#d-021).
- Chỉ có 3 hệ thống nên bằng chứng chuyển miền yếu; có bias vị trí chèn lỗi (arXiv 2609.27069).
- Checkpoint tuần 3–4: nếu baseline mạnh đã gần dùng toàn bộ dữ liệu ở mọi mức ngân sách thì dừng, không đổi tập test để cứu đề tài.

## Các việc còn dở khi lưu trữ
1. Tải toàn bộ 735 ca (hiện mới có index + 6 ca mẫu).
2. Tái lập 2–3 baseline (BARO, RCD); xác nhận chạy được không cần GPU.
3. Tra thêm tiền lệ ở ICSE/FSE/ASE/NSDI/OSDI.

## Trong thư mục này
- [log.md](log.md) — nhật ký nghiên cứu riêng đề tài.
- [research/topic-decision.md](research/topic-decision.md) — phạm vi, RQ, đối chứng, lộ trình 8 tuần.
- [code/preprocessing/](code/preprocessing/README.md) — script audit dữ liệu và cách tái lập.
- Bối cảnh lựa chọn: [surveys/open-field-topic-selection-2026-10-12.md](../../../surveys/open-field-topic-selection-2026-10-12.md).
