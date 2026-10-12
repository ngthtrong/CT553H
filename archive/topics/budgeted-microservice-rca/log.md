# Nhật ký đề tài `budgeted-microservice-rca`

> Mới nhất ở trên. Các mục dưới đây được tách nguyên văn từ nhật ký chung cũ (`docs/common/work-log.md`) ngày 12/10/2026. Câu chữ "chốt/quyết định" bên dưới là lịch sử; trạng thái hiện hành chỉ nằm ở [DECISIONS.md](../../../DECISIONS.md).

---

## 12/10/2026 — cập nhật hồ sơ theo [D-021](../../../DECISIONS.md#d-021)

- Chuyển cả thư mục sang `archive/topics/budgeted-microservice-rca/`, gồm tài liệu, code và dữ liệu; cập nhật liên kết và chỉ mục tài nguyên.
- Kiểm tra: SHA-256 của 23 file dữ liệu không đổi; dữ liệu vẫn bị Git bỏ qua; script audit chạy `--help` được tại đường dẫn mới. Kiểm liên kết toàn repo chỉ còn lỗi có từ trước ở `lectures/14-xai-basics.html` trỏ tới bài 15 chưa có.
- Giữ nguyên bằng chứng audit và các mục lịch sử bên dưới. Trạng thái hiện hành: [DECISIONS.md](../../../DECISIONS.md#d-021).

---

## 12/10/2026 — khóa phạm vi RCA sau khảo sát mở, đính chính tiền lệ

- **Chọn chính `budgeted-microservice-rca`; dự phòng duy nhất degron.** [Báo cáo lựa chọn](../../../surveys/open-field-topic-selection-2026-10-12.md) đối chiếu 10 hướng, gồm DataSAIL, MaveDB và OpDEA/SCPDA ở tầng quy trình bio; áp năm tiêu chí GVHD và tách thiết kế G2 khỏi kết quả chưa có.
- Khóa [phạm vi RCA](research/topic-decision.md): học lợi ích giảm lỗi xếp hạng của truy vấn dịch vụ × nguồn × cửa sổ; so cùng ranker với fixed/random/anomaly/uncertainty và AFA; broker che dữ liệu chưa mở; split nhóm kịch bản, chuyển hệ thống/dịch vụ; ứng dụng điều tra/replay. Chưa xây app hoặc huấn luyện.
- **Đính chính mục buổi chiều phía dưới:** đã đọc toàn văn HTML arXiv 2609.27069, có RE2 Sock Shop; không gọi “mở rộng sang RE2” là khoảng trống chưa ai đo. VerifyRCA/VeriTrail-RCA đã có budget/truy hồi thích ứng. Thêm đối chứng prior-only và telemetry shuffle. Công thức hay phát hiện bias chưa bảo đảm G2 dương; các số Avg@5 của tác giả chưa tái lập.
- [Audit RCA](code/preprocessing/README.md): kiểm toàn index 735 ca + sáu ca thô, 49.463.299 B; 360 ca RE2/RE3, 359 có logs, 240 có traces; nguồn HF revision cố định, kiểm SHA/kích thước và schema. Chưa tải tất cả ca/chạy baseline. Cập nhật index, trạng thái các quyết định cũ và tài nguyên; giữ tài liệu legal QA/hub cũ.
- Kiểm tra đạt: biên dịch script, JSON/count, SHA/kích thước 22 tệp cache, raw bỏ qua Git, 37 liên kết mới và diff scoped. Có 16 lượt link hỏng lịch sử ngoài phạm vi, ghi trong báo cáo. Chưa có kết quả hiệu quả hay phê duyệt học thuật; không commit.

---

## 12/10/2026 (chiều) — **CHỐT ĐỀ TÀI CHÍNH MỚI**: `budgeted-microservice-rca`, thay cho `degron-e3-specificity`

- **Yêu cầu của sinh viên:** các đề tài tin sinh học đang xét chỉ cần còn trong lĩnh vực, không bị ép đổi tầng bài toán; nhưng Claude cũng được tìm một đề tài hoàn toàn khác, miễn đóng góp/ý nghĩa thật và dữ liệu khả thi; mục tiêu chốt được đề tài **trong ngày**; vẫn áp khung năm tiêu chí GVHD và ba cổng G1/G2/G3; Claude tự quyết toàn bộ.
- **Phát hiện:** phiên trước khi `/clear` xoá ngữ cảnh đã để lại một thư mục `archive/topics/budgeted-microservice-rca/code/` chưa có tài liệu — script audit đã tự tải và kiểm SHA-256 thật benchmark **RCAEval** (`phamquiluan/RCAEval`, MIT, 735 ca sự cố chèn lỗi có kiểm soát trên ba hệ thống vi dịch vụ mã nguồn mở). Đã hoàn thiện phần tài liệu còn thiếu đó bằng tra cứu mới và chốt chính thức.
- **Khoảng trống nghiên cứu:** tra được một tiền ấn một tác giả 09/2026 (chưa phản biện, arXiv 2609.27069) báo RCAEval chỉ chèn lỗi vào 5 dịch vụ cố định mỗi hệ thống trong khi quan trắc phủ 12–70 dịch vụ — một bộ xếp hạng không đọc telemetry đạt Avg@5 0,488 (so với 0,137 ngẫu nhiên). Đối chiếu được với chính bài báo gốc RCAEval (arXiv 2412.17015, mục 3.3: *"each dataset covers five services"*) → claim có cơ sở, không chỉ trôi nổi. **Không được nói "Claude phát hiện đầu tiên".** Đóng góp định vị ở phần chưa đo: mở rộng sang RE2/RE3 (có log/trace, Buljić chỉ rõ RE1) và câu hỏi mới — đánh đổi giữa hạn mức quan trắc (observability budget) và độ chính xác chẩn đoán.
- **So với hai ứng viên khác đã có trong ngày:** thắng `legal-qa-grounding` vì G2 có một công thức đã có sẵn để tái lập/mở rộng ngay (cụ thể hơn "đo khoảng cách đời thường↔hình thức" còn mơ hồ), và không cần GPU (15 baseline của RCAEval là thống kê/nhân quả cổ điển). Thắng `degron-e3-specificity` vì đề tài đó đã hơn một tuần audit vòng lặp mà G2 vẫn "chưa xác lập" và G3 tự nhận yếu nhất cả repo.
- **Rủi ro chưa giải, giống `legal-qa-grounding`:** khớp chuyên môn GVHD (tin sinh học/protein, không có AIOps/hệ phân tán) — phải hỏi thẳng tuần 6, nên hỏi về cả hai đề tài ngoài lĩnh vực cùng lúc. Nguồn khoảng trống chính (arXiv 2609.27069) mới lấy qua tóm tắt AI, **chưa tự đọc toàn văn và chưa tái lập độc lập số liệu 0,488/0,137/0,192** — cổng chặn phải đóng đầu tiên trước khi dùng cho đề cương chính thức.
- Tài liệu: [budgeted-microservice-rca/01-idea/topic-decision.md](research/topic-decision.md). Cập nhật [topics/README.md](../../../topics/README.md): đổi banner chính, thêm dòng bảng cho `budgeted-microservice-rca` và `degron-e3-specificity`, sửa trạng thái `legal-qa-grounding`. `degron-e3-specificity` và `legal-qa-grounding` **không bị xoá**, giữ làm phương án dự phòng.
- **Còn dở:** tự đọc toàn văn hai bài arXiv nêu trên; tải toàn bộ 735 ca (mới có index + 6 ca mẫu); chạy thử 2–3 baseline (BARO, RCD) để xác nhận tái lập được và không cần GPU; tra kỹ hơn trên ICSE/FSE/ASE/NSDI/OSDI (hôm nay chỉ tra Google tổng quát); chuẩn bị câu hỏi GVHD về việc nhận hướng dẫn ngoài chuyên môn. Chưa huấn luyện mô hình, chưa xây website.
