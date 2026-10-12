# Nhật ký đề tài `legal-qa-grounding`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

---

## 12/10/2026 — ứng viên mới hoàn toàn ngoài lĩnh vực: `legal-qa-grounding` (hỏi–đáp pháp luật tiếng Việt)

- **Yêu cầu của sinh viên:** bỏ ràng buộc lĩnh vực và các đề tài đang xét trong repo, tìm một đề tài hoàn toàn khác, tập trung vào đóng góp/ý nghĩa thực sự và dữ liệu khả thi, Claude tự quyết toàn bộ, mục tiêu chốt trong ngày; vẫn áp khung năm tiêu chí GVHD.
- Đã khảo sát nhanh bốn hướng ngoài protein (sâu bệnh lúa ĐBSCL, tín dụng, hỏi–đáp y tế, hỏi–đáp pháp luật) — ba hướng đầu loại vì bão hòa tính mới hoặc thiếu dữ liệu bản địa công khai. Chọn **hỏi–đáp pháp luật tiếng Việt có kiểm chứng trích dẫn**, giải quyết khoảng cách từ vựng giữa câu hỏi đời thường của dân và văn phong luật.
- **Đã tự tải thật dữ liệu để kiểm khả thi** (không chỉ đọc mô tả): từ mirror GitHub của đội dự thi ALQAC 2023 (`DucLong06/ALQAC2023`, giải nhất Task 2) — **2.249 điều luật** (2,6 MB) và **310 câu hỏi có nhãn vàng** (train/public_test/private_test), định dạng JSON sạch, nhãn do ban tổ chức gán độc lập → **G1 đạt**. Xác nhận `huggingface.co`, `github.com`, `raw.githubusercontent.com` đều tới được từ phiên này (khác tình trạng chặn mạng ghi nhận trước đó cho một môi trường cloud khác).
- Xác nhận khoảng trống nghiên cứu thật qua tra cứu: ALQAC vẫn hoạt động (lần 5, KSE 2025 Đà Lạt); shared task DRILL/VLSP 2025 (50+ đội) ghi nhận hệ thống hiện tại còn yếu ở suy luận thường thức/ngữ cảnh dài; chưa tìm thấy nghiên cứu đo định lượng độ chênh truy hồi giữa câu hỏi hình thức và câu hỏi đời thường thật. **Không được nói "đầu tiên làm RAG luật tiếng Việt"** — đã có VietLegal-RAG, RegRAG-VN (ngân hàng, nhắm IEEE-RIVF 2026), GraphRAG (FPT).
- **G2 (đóng góp dương) chưa xác lập** — cần baseline thật. **G3 (website) mạnh nhất trong mọi đề tài đã xét ở repo này**: sản phẩm chính là hệ thống web, không phải phụ lục.
- **Rủi ro lớn nhất và chưa có lời giải: khớp chuyên môn GVHD.** 14 công trình của thầy đều tin sinh học/protein, không có NLP/pháp luật. Đây là rủi ro tường minh, không che giấu — phải hỏi thẳng GVHD ở tuần 6 trước khi đầu tư thêm.
- Tài liệu: [legal-qa-grounding/01-idea/topic-decision.md](topic-decision.md). Đã thêm dòng vào [topics/README.md](../../../topics/README.md).
- **Còn dở:** xác minh license dữ liệu ALQAC ngoài phạm vi thi; gộp dữ liệu nhiều năm (mới đếm riêng 2023); chưa chạy baseline; chưa thu thập câu hỏi đời thường thật; chưa hỏi GVHD về việc nhận hướng dẫn ngoài chuyên môn. `degron-e3-specificity` vẫn là đề tài đã chốt trước đó trong repo — tài liệu này là một **ứng viên song song**, chưa thay thế.
