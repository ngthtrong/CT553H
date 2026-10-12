# Quyết định của dự án — nơi duy nhất

> **Quy tắc.** Đây là **file duy nhất** ghi quyết định đã chốt. Mọi tài liệu khác (báo cáo, nhật ký, thẻ đề tài, biên bản) chỉ được **dẫn link** tới đây (`DECISIONS.md#d-0xx`), không tự viết "đã chốt / quyết định". Câu "chốt" trong tài liệu cũ là **lịch sử**, không có hiệu lực nếu không khớp phần A.
>
> - **Phần A** ghi trạng thái hiện hành, dài tối đa một màn hình. Khi có thay đổi thì **sửa đè**, không cộng dồn.
> - **Phần B** là sổ quyết định. Thêm mục mới **lên đầu**. Mục cũ không xoá: chỉ đổi trạng thái thành `Bị thay bởi D-0yy`.
> - **Phần C** chứa đề xuất **chưa được Trọng xác nhận**. Đề xuất của Claude chỉ chuyển sang phần B khi Trọng đồng ý.

---

## A. Hiện hành — cập nhật 12/10/2026

| Mục | Giá trị | Căn cứ |
|---|---|---|
| Giai đoạn | Chọn và hoàn thiện đề tài. **Chưa có đề tài nào được GVHD duyệt**; chưa huấn luyện mô hình hay xây ứng dụng | — |
| Đề tài chính | [`budgeted-microservice-rca`](topics/budgeted-microservice-rca/README.md), **chưa được GVHD duyệt** | [D-016](#d-016) |
| Dự phòng | [`degron-footprint`](topics/degron-footprint/README.md) | [D-016](#d-016) |
| Đang đào sâu (6) | [budgeted-microservice-rca](topics/budgeted-microservice-rca/README.md) · [xai-fidelity-benchmark](topics/xai-fidelity-benchmark/README.md) (A2) · [structure-sequence-leakage-audit](topics/structure-sequence-leakage-audit/README.md) (A3) · [plm-calibration-audit](topics/plm-calibration-audit/README.md) (A4) · [degron-footprint](topics/degron-footprint/README.md) · [dark-kinome-zero-shot](topics/dark-kinome-zero-shot/README.md) | [D-019](#d-019) |
| Thứ tự tiềm năng | Là **số đầu tên thư mục** trong `topics/` (ví dụ `1-ten-de-tai`), do Trọng tự đặt. **Chưa đặt** | [D-019](#d-019) |
| Định hướng chọn đề tài | 1) ưu tiên tin sinh học; 2) không bó vào dự đoán residue/peptide; 3) ưu tiên tầng công cụ/benchmark/nền tảng; 4) đề tài ngoài tin sinh học vẫn hợp lệ nhưng xếp sau | [D-017](#d-017) |
| Thước đo một ứng viên | 5 tiêu chí GVHD + 3 cổng bắt buộc G1/G2/G3, xem [course.md](project/course.md) | [D-006](#d-006), [D-012](#d-012) |
| Đã đóng (lưu trữ) | RTK–ATP, TME senescence, cơ chất sirtuin, legal QA, quản lý chi tiêu, efflux, IL-6, sửa lỗi phần mềm. Xem [archive/](archive/README.md) | D-003, D-006, D-008, D-010, D-011, D-019 |
| Quy ước đang áp dụng | HTML để trong repo, không dùng artifact ([D-013](#d-013)). Repo private ([D-004](#d-004)) | — |

**Mốc tiếp theo:** tuần 6 báo cáo lại đề tài với GVHD (xem [course.md](project/course.md)).

---

## C. Đề xuất chờ Trọng xác nhận

| # | Đề xuất | Người đề xuất | Ghi chú |
|---|---|---|---|
| C-1 | Xác nhận lại RCA có còn là đề tài chính không | Claude, 12/10/2026 | D-016 do Claude chọn theo ủy quyền, **trước** khi có D-017 (ưu tiên tin sinh) và D-019 (6 đề tài ngang hàng đang đào sâu). Hai quyết định này có thể mâu thuẫn với D-016. Nếu bỏ "đề tài chính" thì sửa phần A |
| C-2 | Thứ tự tạm trong nhóm A: A4 → A2 → A3 | Claude, 12/10/2026 | Chỉ là gợi ý trong [deep-dive](topics/plm-calibration-audit/research/deep-dive-2026-10-12.md), chưa phải quyết định. Thay bằng số đầu tên thư mục khi Trọng đặt |
| C-3 | Hỏi GVHD ở tuần 6: đóng góp dạng công cụ/audit/benchmark (A2, A3, A4, một phần RCA) có được nhận không | Claude, 12/10/2026 | Ngày 11/10 GVHD kỳ vọng kiến trúc mới, không nhận chỉ một bảng đối chứng ([people.md](project/people.md)). Điều này **mâu thuẫn** với mức 3 của D-017 |

---

## B. Sổ quyết định (mới nhất ở trên)

Trường "Ai quyết": **Trọng** (sinh viên), **GVHD**, **Claude (ủy quyền)** — Trọng giao cho Claude tự quyết, **Claude (khuyến nghị)** — chỉ là khuyến nghị nhưng đã được dùng như quyết định.

### D-020
**12/10/2026 · Trọng · Hiệu lực.** Bỏ thư mục `data/` ở gốc. Dữ liệu của mỗi đề tài nằm trong chính thư mục đề tài, ở `topics/<ten-de-tai>/data/` (đề tài đã đóng: `archive/topics/<ten-de-tai>/data/`), và bị `.gitignore` chặn. Dữ liệu của đề tài đã đóng được giữ, không xoá.

### D-019
**12/10/2026 · Trọng · Hiệu lực.** Tổ chức lại repo. Từ nay quyết định chỉ ghi ở file này. Sáu đề tài đang đào sâu có thư mục riêng trong `topics/`: RCA, A2, A3, A4, degron, dark kinome zero-shot (mở lại hướng này). **Đóng hai đề tài không liên quan tin sinh học**: `legal-qa-grounding` và `personal-expense-management`. RCA vẫn giữ trong `topics/`. Các hướng cũ chuyển vào `archive/`. Thứ tự tiềm năng được mã hóa bằng số đầu tên thư mục, do Trọng tự đặt.

### D-018
**12/10/2026 (tối) · Trọng · Hiệu lực.** Từ 14 ứng viên tầng công cụ trong [khảo sát](surveys/bioinformatics-tool-layer-candidates-2026-10-12.md), đi sâu ba ứng viên bậc A khớp GVHD: A2 (fidelity XAI), A3 (cấu trúc + trình tự, **phải thu hẹp** thành audit vì đã có Denger & Helms 2025), A4 (calibration/miền áp dụng). Nguồn: [journal 12/10](journal/2026-10.md).

### D-017
**12/10/2026 · Trọng · Hiệu lực.** Định hướng chọn đề tài có 4 mức, tóm tắt ở phần A. Mục tiêu tối cao là tìm một đề tài có đóng góp thật, giải quyết vấn đề có ý nghĩa. Mục tiêu này đứng trên độ khớp với các ứng viên đang có.

### D-016
**12/10/2026 (chiều) · Claude (ủy quyền: "Claude tự quyết toàn bộ, chốt trong ngày") · Hiệu lực, chưa GVHD duyệt, xem C-1.** Chọn `budgeted-microservice-rca` làm đề tài chính, thay [D-014](#d-014). Degron là dự phòng duy nhất. Căn cứ: [báo cáo lựa chọn mở lĩnh vực](surveys/open-field-topic-selection-2026-10-12.md).

### D-015
**12/10/2026 · Trọng · Bị thay bởi D-016, đóng ở D-019.** Đưa `legal-qa-grounding` (hỏi–đáp pháp luật tiếng Việt) lên làm ứng viên hàng đầu ngoài lĩnh vực.

### D-014
**11/10/2026 · Trọng · Bị thay bởi D-016.** Chốt degron làm đề tài chính. Khuya cùng ngày tái định tâm: bỏ trục đặc hiệu E3 (chỉ 1 E3 đủ mẫu), chuyển sang dự đoán footprint mức residue trên nhãn đột biến. Slug cũ `degron-e3-specificity`, nay là `degron-footprint`.

### D-013
**11/10/2026 · Trọng · Hiệu lực.** Trang HTML được tạo trực tiếp trong repo và mở bằng `file://`, không publish artifact nữa.

### D-012
**10/10/2026 · Claude (khuyến nghị), được dùng làm chuẩn từ đó · Hiệu lực.** Ba cổng bắt buộc: G1 nhãn độc lập, G2 đóng góp dương đo được, G3 ứng dụng khả thi. Định nghĩa đầy đủ ở [course.md](project/course.md).

### D-011
**10/10/2026 · Claude (khuyến nghị) · Bị thay bởi D-014.** Khuyến nghị dark kinome trên DARKIN làm đề tài chính. Loại sirtuin khỏi vị trí chính vì Trọng cho biết **GVHD không nhận kết quả âm làm đóng góp chính**. Ngày 11/10, sáu phép kiểm đã làm sụp trụ tính mới (xem [thẻ đề tài](topics/dark-kinome-zero-shot/README.md)).

### D-010
**10/10/2026 · Trọng · Hiệu lực.** Loại hướng "sửa lỗi phần mềm có kiểm chứng".

### D-009
**08/10/2026 · Claude (khuyến nghị) · Bị thay bởi D-011.** Đề tài chính là cơ chất deacetyl hóa theo isoform SIRT1–7, dự phòng là phospho theo nhóm kinase. Nguồn: [archive](archive/surveys/topic-final-recommendation.md).

### D-008
**07/10/2026 · ghi trong nhật ký · Hiệu lực.** Dừng hướng TME senescence (scRNA-seq), vì điểm SenMayo là nhãn do chính pipeline sinh ra (trượt điều kiện về nhãn, về sau thành G1).

### D-007
**07/10/2026 · GVHD · Hiệu lực.** GVHD chấp nhận đề tài có đầu vào là ma trận biểu hiện gene, không bắt buộc phải là chuỗi amino acid (theo Trọng truyền đạt).

### D-006
**02/10/2026 (sau buổi gặp 1) · GVHD góp ý → Trọng · Hiệu lực.** RTK–ATP không bị từ chối, nhưng GVHD khuyên đổi sang đề tài khác. RTK–ATP coi như bỏ. Áp dụng **năm tiêu chí của GVHD**; tiêu chí 5 (ứng dụng/website) không thể thiếu. Biên bản: [minutes.md](project/meetings/2026-10-02-session-01/minutes.md).

### D-005
**02/10/2026 · Trọng (tự chốt trước buổi gặp) · Bị thay bởi D-006.** Trình GVHD đề tài RTK–ATP.

### D-004
**01/10/2026 · Trọng · Hiệu lực.** Repo GitHub chuyển sang private, nên được phép chứa PDF bài báo và phân tích về bài của nhóm GVHD. Nếu đổi sang public thì phải gỡ các phần này, kể cả khỏi lịch sử git.

### D-003
**01/10/2026 · Trọng · Hiệu lực (đã đóng).** Loại hướng peptide IL-6. Efflux giữ làm dự phòng cho RTK–ATP, sau đó bỏ cùng RTK–ATP.

### D-002
**01/10/2026 · Trọng · Hiệu lực.** Chuyển sang lĩnh vực tin sinh học (chuyên môn GVHD). Tạm dừng đề tài quản lý chi tiêu; đề tài này đóng hẳn ở D-019.

### D-001
**24–29/09/2026 · Trọng · Bị thay bởi D-002.** Đề tài quản lý chi tiêu cá nhân có bộ phân loại giao dịch tự thích nghi.
